# Round 33 — quiz key transcript

Sole source read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(read in full, via the Read tool, in four passes covering lines 1–4806).

Scratch files written (mine alone, in
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r33-round/scratch/quiz-keyer/`):
- `qk_crc33.py` — CRC-32C implementation + spec self-checks + Q02/Q10 computations
- `qk_geom33.py` — grid/ordinal/packing arithmetic for Q01, Q03, Q08, Q15

## CRC calibration (before trusting any CRC answer)

My CRC-32C reproduces four values the document itself publishes:
- CRC-32C("123456789") = 0xE3069283 (§4.5 check vector) — matched
- CRC-32C(zero bytes) = 0x00000000 (§4.5) — matched
- Appendix A's trailer CRC 0x402F157E, bytes `7E 15 2F 40`, over that file's
  trailer bytes [0,60) — matched, built from my own trailer serializer
- §7.4's worked example: CRC over 80 bytes of 4 sentinel entries = 0x80A34955,
  and crc_of_crc_array of its 4-byte array = 0xC4EE982E — both matched
- §15.4's full all-sentinel segment constant 0xEECB3BB2 — recomputed and matched

That last one is the one Q10 leans on, and it is derived here rather than taken
on the document's word.

## Search discipline

The document is hard-wrapped and blockquotes wrap with `> `. Every phrase search
I ran was against a whitespace-normalised copy of the file (blockquote markers
stripped, all runs of whitespace collapsed to one space), so a phrase spanning a
line break still matches. Each search batch included a known-present control
phrase ("cannot establish", 8 hits) so that a zero would have been meaningful.
No answer below rests on a zero-hit search.

---

## Q01 — 36, 724, 620

Planar, C = 3, rank 2, (E,T) = (1000,256) and (700,256).

G0 = ⌈1000/256⌉ = 4, G1 = ⌈700/256⌉ = 3 (§11.2, `[R-GEO-03]`: "the **grid
count** Gᵢ is the ceiling division ⌈Eᵢ / Tᵢ⌉"). N = ∏Gᵢ = 12.

(a) §11.2: "its **addressed-tile count** — the number of its tile-index entries
(§15) — is N for an interleaved layer and C · N for a planar layer". §7.4 fixes
entry_count as "equals the addressed-tile count". So entry_count = 3 × 12 = 36.

(b) `[R-CNT-17]`: "Under index_encoding 1, extent_length MUST equal
entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4". = 36×20 + 1×4 = 720 + 4 = 724.

(c) §11.4 `[R-GEO-06]`: spatial tile ordinal s = Σᵢ tᵢ · ∏_{j>i} Gⱼ
= 2·G1 + 1 = 2·3 + 1 = 7; disk tile ordinal = c·N + s = 2·12 + 7 = 31.
§15.1 `[R-IDX-01]`: "The entry for the tile with disk ordinal k (§11.4) is the
k-th entry, at region byte 20·k". 20 × 31 = 620.

## Q02 — d6 b1 a0 57

Trailer occupies [128,192); §6.2's layout puts the trailer CRC at trailer offset
60, i.e. file [188,192), "CRC-32C over trailer bytes [0, 60)" = file [128,188).

Trailer bytes [0,60), built from §6.2's table:
`8a 4e 52 41 54 0d 0a 1a 01 00 00 00 00 00 00 00 10 00 00 00 00 00 00 00
04 00 00 00 00 00 00 00 c0 00 00 00 00 00 00 00 ef cd ab 89 67 45 23 01
00 00 00 00 00 00 00 00 00 00 00 00`
(magic; version_major 1; version_minor 0; flags 0; dir_offset 16; dir_length 4;
committed_file_length 192 = 0xC0; file_id 0x0123456789ABCDEF little-endian;
12 zero reserved bytes.)

CRC-32C = 0x57A0B1D6, stored little-endian (`[R-ENC-09]`) → `d6 b1 a0 57`.

Sanity: the only byte differing from Appendix A's trailer is
committed_file_length (0x80 → 0xC0); my serializer reproduces Appendix A's
0x402F157E exactly, so the difference is the only thing driving the new value.
The 108-byte pre-trailer pad is longer than a conforming commit produces, but
§6.2 says outright "a longer gap is conforming" — and it is outside the CRC
input regardless.

## Q03 — E4 FF

Planar bool plane, so §14.3 governs: "value k occupies bit k mod 8 of byte
k div 8 (§4.4), with 0 = false and 1 = true, and the decoded size is ⌈P/8⌉".

T = (3,3) → P = 9, decoded size ⌈9/8⌉ = 2. E = (2,2) → G = (1,1), one tile.
In-tile ordinal = u0·T1 + u1 = 3u0 + u1 (§11.4).

Ordinals 0,1,3,4 are the real positions (u0,u1 < 2) — all false = 0.
Ordinals 2,5,6,7,8 are padding positions (§11.3), and `[R-SER-05]` fixes them:
"at every padding position, a writer MUST encode, for each channel the position
carries, that channel's fill value … the fill bit in a packed plane". Fill = 0x01
= true, so each is 1.
P mod 8 = 1, so bits 1–7 of byte 1 are pad bits, and `[R-SER-05]`: "Every pad bit
(§14.3) MUST carry the plane's channel's fill bit" → all 1.

Byte 0 = bits {2,5,6,7} = 0x04+0x20+0x40+0x80 = 0xE4. Byte 1 = bit 0 (ordinal 8)
plus pad bits 1–7 = 0xFF.

Cross-check against §14.3's own example: fill true there sets the pad bits
(`55 FD`), which is the same mechanism.

## Q04 — cannot establish

Order of validation (§6.2): magic — ok; trailer CRC — ok (the u32 at 252 covers
[192,252) = trailer [0,60)); version gate — version_major 2 is a major this
verifier does not implement, `[R-CNT-07]` reject-file. Validation stops there;
the reserved-bytes gate is among the ones §6.2 orders after "those gates passed".

The nonzero reserved bytes would be F15, and §2.3's Note is explicit: "F15 does
not reach although its Governing rule cell cites `[R-CNT-24]`: the trailer bytes
it requires be zero are inside the 48 that rule lets a future major redefine."
`[R-CNF-13]`: conditions that do not reach are "not assessed against a file
declaring another major, no violation of it is established there".

§21.2 derives the reaching set: "F8, F14, F6 and both of F1's instances … and no
other row" — all four are satisfied here (front block byte-identical, magic
byte-identical, CRC matching, nothing byte-reversed).

So no violation is established, and the file "names a format major version it
does not implement" — §2.3's first-named cannot-establish ground.

## Q05 — nonconforming

Top-level record, encoding 0x80: metadata-encoding experimental range is ≥ 0x80
(§10.2). §21.6: "A user-metadata record declares an experimental-range (≥ 0x80)
document encoding | Ignored (ignore-record); the file is conforming … so a
verifier certifies, reporting the record it ignored". No bar.

Layer sub-record, encoding 0x03: reserved range 3–0x7F. §21.5 R1 registers "A
user-metadata record declares a document encoding of 0, or a reserved-range value
(3-0x7F)". §21.5's preamble: "Every row here is a violation all the same: the
outcome bounds a reader's blast radius and never makes the file conforming".
§18.2/`[R-MTA-10]`: "encoding 0 and a reserved value being R1's violations".

`[R-CNF-11]`: "a verifier that has established any violation reports
*nonconforming*". Ignore-record is the reader's blast radius, not a verdict.

## Q06 — reject-tile; no; no

(a) §15.3's table: "length = 0 (non-sentinel) | *structural*: reject-tile —
absence is spelled sentinel; no codec emits zero bytes". (Registered as T24's
neighbour T10.) The outcome class name in §2.4's vocabulary is **reject-tile**.

(b) §9.7 `[R-LIF-08]`: "(an entry `[R-IDX-03]` classifies reject-tile on a
*structural* ground contributes no stored extent to the walk; one whose stored
bytes alone fail its crc keeps its extent)". No claimant.

(c) §5.2 `[R-CNT-21]`: "An entry `[R-IDX-03]` classifies reject-tile on a
structural ground leaves it complete too, and for the opposite reason: it
contributes no claimant, the walk passes over it, and its bytes fall to slack".
So the walk stays complete and the total is not partial. (The stipulation that
no structure lies at [2000, 2000+n) matters only to make the entry's nominal
bytes genuinely slack; the walk's completeness does not turn on it.)

## Q07 — yes; yes; no

(a) §20.3 step 4 lists, for a layer that stored a tile in the superseded
generation: "its name, and its dimension and channel names, MAY change; an extent
MAY grow, and MUST NOT shrink; a planar layer's channel list MAY be extended at
its end or shortened from its end, but not both in one commit; … A commit MAY
make several of these changes at once, an extension and a shortening of one
channel list excepted". A grow + a shortening + a name change is three of the
permitted changes and no forbidden pair. Yes.

(b) §20.3 step 4: "A channel removed from the end … changes the layer's index
content, the entries the removed channel held ceasing to denote its tiles, so the
region is re-emitted under the clause above whether or not entry_count changes
with it (`[R-CNT-17]`) and whether or not a retained ordinal moves". Step 4's
clause: re-emitted "in full … necessarily at a new placement (`[R-LIF-01]`)", and
`[R-LIF-01]` makes a new placement an append. L stores a tile, so N ≥ 1 and the
new entry_count = 2N > 0: the region is non-empty. Yes.

(c) "but not both in one commit"; and "a commit that shortens a planar layer's
channel list appends no channel to it and one that extends it removes none,
whatever the counts, so replacing the last channel, or any run of channels at the
end, is two commits or a rewrite". No.

## Q08 — yes; no

File A: G = ⌈20000/16384⌉ = 2 each, P = 16384² = 268,435,456. Planar float64
plane decoded size = P·8 = 2,147,483,648; packed bool plane = ⌈P/8⌉ =
33,554,432. `[R-COD-07]`: "Writers MUST NOT declare this codec for a layer any of
whose addressed tiles' decoded size exceeds 0x7E000000 bytes … in a planar layer
each channel's plane carries its own decoded size … and the largest governs — and
a reader MUST treat such a declaration as a validity error at layer scope".
0x7E000000 = 2,113,929,216 < 2,147,483,648. Violation (L44). Yes.

File B: E0 = 0 → G0 = 0 → N = 0 → addressed-tile count C·N = 0. §17.2's Note:
"The cap is quantified over the layer's *addressed* tiles, so a layer that
addresses none — any dimension extent 0 (`[R-GEO-02]`, §21.6) — satisfies it
whatever its tile shape declares, and codec 4 is conforming there." The same Note
keeps `[R-ENC-04]`'s ceiling in force, but P·8 = 2³¹ and ⌈P/8⌉ are both far below
2⁶³ − 1. `[R-GEO-02]`: "A dimension with extent 0 is valid … Readers MUST accept
such a layer". No.

## Q09 — F35; reader; open

Type 0x0100 = 256 lies in the record-type reserved range 0x0003–0x7FFF (§10.2).
MU (flags bit 0) = 1.

Two rows are candidates: F35 ("A top-level record has a reserved-range type value
(0x0003-0x7FFF, §10.2) with MUST_UNDERSTAND (flags bit 0) set to 1", detector
reader, detected open) and F36 (same type range "whatever its MU bit", detector
verifier, detected certification).

§21.1: "where every file exhibiting one row's condition … necessarily exhibits
another's, the file is recorded against the narrower row, whose detector and
detection point are the ones that apply. F1's front-block instance of F6 and its
trailer-magic instance of F8, **F35 of F36**, L24 of L25, F21 of F22 and L10 of
L11 stand in that relation". F35 is the named specialization, so F35's cells
govern: Detector = reader, Detected = open.

PE = 1 is consistent with `[R-CNT-12]` and changes nothing here.

## Q10 — 1; 3a173c06

(a) §15.1: segment CRC array is "⌈entry_count / 2¹⁶⌉ × 4 bytes". ⌈65536/65536⌉ =
1, so one u32.

(b) The single segment is full and all-sentinel. §15.4 `[R-IDX-05]`: "The CRC-32C
of a segment consisting of 2¹⁶ sentinel entries is `0xEECB3BB2`". I recomputed it
from 65,536 copies of §15.2's 20-byte sentinel `FF ×16 00 ×4` and got 0xEECB3BB2.
Stored little-endian, the 4-byte array is `b2 3b cb ee`. `[R-CNT-19]`: "All
checksums are CRC-32C over bytes exactly as stored." crc_of_crc_array =
CRC-32C(`b2 3b cb ee`) = 0x3A173C06 → **3a173c06**.

(Method cross-checked on §7.4's worked example, where the same two-step derivation
reproduces the document's 0x80A34955 and 0xC4EE982E.)

## Q11 — no; cannot establish

(a) §5.2 `[R-CNT-21]`: "The walk is incomplete where a scope-level rejection ends
that scope's enumeration, where the verifier declined a layer on resource grounds
(`[R-ERR-04]`) … or where the verifier elected under `[R-CNF-11]` to stop at the
first violation; **a tile's or a document's decode declined leaves the walk
complete**, that claimant being enumerated from its index entry or extent slot."
Neither decline here is a layer decline, and the premise says every claimant was
enumerated. Not partial.

(b) §2.3: cannot establish covers "when it declines a layer's or a tile's decode
on resource grounds and so cannot check §14's decoded-content obligations
(`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`), or when it declines to decode a
user-metadata document (`[R-MTA-09]`)". §9.7: "one that declines a tile's decode
on resource grounds reports that check unmade and cannot certify". §18.2: "A
**verifier** that declines to decode a document on either bound above cannot
establish that document's conformance and MUST NOT certify the file". No violation
established, so cannot establish is available — and mandatory, since certification
is barred.

## Q12 — yes; no

§18.2's "Finite numbers only" restriction: "A document is unreadable if it
contains a number whose binary64 interpretation is not finite — which covers a
magnitude that overflows on that conversion, `1e400` being the ordinary case".

File A: 1e400 overflows binary64 under roundTiesToEven → infinity → not finite →
unreadable (R8). Yes.

File B: 1e-400 *underflows*; under roundTiesToEven it converts to +0.0, which is
finite. Nothing in §18.2 makes an inexact or underflowing number unreadable — the
nearest text is a writer SHOULD ("Writers SHOULD NOT emit a number binary64 cannot
represent exactly"), and §2.4 `[R-CNF-12]`: "Deviation from a SHOULD is not a
violation for this purpose". Every other stipulated property (object top level,
UTF-8, no BOM, no duplicate keys, name rules, sorted members) is satisfied. Not
unreadable. No.

## Q13 — yes; yes; no

(a) §21.9 `[R-ERR-03]`: "The table below states **minimum guarantees**, not
caps"; `[R-ERR-04]`: "A file exceeding any of these remains conforming". 5000
channels is under §7.4/`[R-ERR-05]`'s hard cap of 65,535 (a u16 field). The
premise says every requirement holds. Yes.

(b) `[R-ERR-04]`: "a reader MAY decline it: at the whole file, or at the narrowest
scope whose stated or derived quantities exceed what it can serve, be that a
layer, a tile, the record carrying a user-metadata document …, or the file
itself". C is a per-layer declaration, so the layer is the narrowest such scope.
"a refusal on resource grounds MUST be reported as a resource limit and not as a
validity error". Yes.

(c) `[R-ERR-04]`: "Software that declines **on that ground** a file whose every
quantity lies within the table is not a conforming reader (`[R-CNF-03]`) … the
guarantees are the floor, not a suggestion." No.

## Q14 — yes; no

The entry (offset 4096, length 0, crc 0) is a non-sentinel with length 0, so
§15.3 classifies it *structural*: reject-tile. The chosen placement moves a stored
extent of L, so §20.5 `[R-WRT-07]` obliges the compactor to regenerate L's index
region.

§20.5: "Regenerating a region means classifying every entry in it: a sentinel is
re-emitted unchanged, and every other entry is re-pointed … An entry §15.3
classifies reject-tile on a structural ground is neither — `[R-IDX-03]` gives it
no stored extent for a re-pointing to target — so regenerating the region cannot
proceed without meeting it, and the violation is thereafter one the compactor has
detected. `[R-WRT-06]` then obliges refusal".

(a) Yes — refusal is mandatory. (b) "no drop is available, a tile-index entry
being no record §20.4's table licenses dropping". No.

## Q15 — 13; 02 01

Planar, C = 3, rank 2, E = (10,10), T = (4,4). G = (⌈10/4⌉, ⌈10/4⌉) = (3,3),
N = 9. Coordinate (5,6): tᵢ = xᵢ div Tᵢ = (1,1); s = t0·G1 + t1 = 1·3 + 1 = 4.
Channel `g` is the second declared, so its index is 1 (§3.1: "a channel's
**index** is its 0-based position in that order"). §11.4 `[R-GEO-06]`: disk tile
ordinal = c·N + s = 1·9 + 4 = **13**.

The entry is the sentinel, so §13.3 `[R-TYP-08]` applies: "in a planar layer
exactly the entry's channel reads as fill there". `[R-TYP-06]`: a reader "MUST
take a channel's fill from its channel entry, MUST NOT substitute a type-derived
default or any other value, and MUST return fill bit-exactly as recorded". The
recorded fill field is the two bytes `02 01` (a valid uint16 fill; every bit
pattern of the element size is valid, `[R-TYP-05]`). Returned bytes: **02 01**.
(As a uint16 that is 0x0102 = 258 little-endian, but the question asks for the
bytes as returned.)

---

## Underdetermination

None of the fifteen. Every answer resolves to a single reading on the document's
own text; the two that came closest to a fork were Q04 (settled decisively by
§2.3's Note naming F15 as non-reaching, and doubly by §6.2's validation order
stopping at the version gate) and Q09 (settled by §21.1 naming "F35 of F36"
explicitly among the strict-specialization pairs).
