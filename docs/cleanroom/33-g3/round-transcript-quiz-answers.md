# Round 33 — quiz answerer transcript

Source read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` only (4805 lines, 290,982 bytes).
Local computation only; scripts in `.../r33-round/scratch/quiz-answerer/` (`crc_qa.py`, `geo.py`).

CRC implementation self-validated against four spec-stated constants before use:
CRC-32C("123456789") = 0xE3069283; CRC-32C("") = 0; §7.4's 80-byte four-sentinel array
= 0x80A34955 and its crc_of_crc_array = 0xC4EE982E; §15.4's full all-sentinel segment
= 0xEECB3BB2; Appendix A's trailer CRC 0x402F157E. All reproduced exactly.

---

## Q01 — 36, 724, 620

§11.2 `[R-GEO-03]`: Gᵢ = ⌈Eᵢ/Tᵢ⌉; N = ∏Gᵢ; addressed-tile count = C·N planar.
G₀ = ⌈1000/256⌉ = 4, G₁ = ⌈700/256⌉ = 3, N = 12, C = 3 → entry_count = 36 (`[R-CNT-17]`:
entry_count "equals the addressed-tile count").

§7.4 `[R-CNT-17]`: "Under index_encoding 1, extent_length MUST equal entry_count × 20 +
⌈entry_count / 2¹⁶⌉ × 4". 36×20 + 1×4 = 720 + 4 = **724**.

§11.4 `[R-GEO-06]`: s = Σ tᵢ·∏_{j>i}Gⱼ = 2·3 + 1 = 7; disk ordinal = c·N + s = 2·12 + 7 = 31.
§15.1 `[R-IDX-01]`: "The entry for the tile with disk ordinal k … is the k-th entry, at
region byte 20·k" → 20·31 = **620**.

## Q02 — d6 b1 a0 57

Trailer occupies [128, 192); its CRC field is at trailer offset 60, size 4 → file
[188, 192). §6.2 layout table: "60 | 4 | u32 | trailer CRC | structural | CRC-32C over
trailer bytes [0, 60)".

Trailer bytes [0,60) =
`8a 4e 52 41 54 0d 0a 1a 01 00 00 00 00 00 00 00 10 00 …(dir_offset 16)… 04 00 …(dir_length 4)…
c0 00 00 00 00 00 00 00 (committed_file_length 192) ef cd ab 89 67 45 23 01 (file_id) 00×12`.

CRC-32C = 0x57A0B1D6, stored little-endian (§4.5 `[R-ENC-09]`) → **d6 b1 a0 57**.
(Cross-check: the same construction with committed_file_length 128 reproduces Appendix A's
`7e 15 2f 40`.)

## Q03 — E4 FF

C = 1, G₀ = ⌈2/3⌉ = 1, G₁ = 1, N = 1, one addressed tile. P = ∏Tᵢ = 9.
Planar bool → §14.3 `[R-SER-03]`: "value k occupies bit k mod 8 of byte k div 8 … the
decoded size is ⌈P/8⌉ bytes" = 2.
In-tile ordinal (§11.4) = u₀·3 + u₁. Real positions (E = (2,2)) are ordinals 0,1,3,4 → false → 0.
Padding positions (ordinals 2,5,6,7,8) take fill per §14.5 `[R-SER-05]`: "a writer MUST
encode, for each channel the position carries, that channel's fill value — … the fill bit in
a packed plane." Fill byte 0x01 = true → bit 1.
Byte 0 bits set: 2,5,6,7 → 0xE4. Byte 0 bit 0 = ordinal 8 = 1; P mod 8 = 1 so pad bits are
positions 1–7 and "Every pad bit MUST carry the plane's channel's fill bit" → all 1 → 0xFF.
Codec 1 / filter 1, so the stored bytes equal the image; the question asks for the image: **E4 FF**.

## Q04 — cannot establish

Ordered gates (§6.2 `[R-CNT-06]`): magic ✓, trailer CRC ✓, version gate → version_major 2 is
a major this verifier does not implement, so `[R-CNT-07]` rejects on capability grounds.
`[R-CNF-13]` fixes which conditions still reach: §21.2's preamble — "Deriving it there yields
F8, F14, F6 and both of F1's instances … and no other row." All four are satisfied here.
The nonzero reserved bytes are F15, and §2.3's Note is explicit: "F15 does not reach although
its Governing rule cell cites `[R-CNT-24]`: the trailer bytes it requires be zero are inside
the 48 that rule lets a future major redefine."
So no violation is established. §2.3 `[R-CNF-11]` lists as a *cannot establish* ground
"when the file names a format major version it does not implement". Verdict: **cannot establish**.

## Q05 — nonconforming

Record 1: encoding byte 0x80 → experimental range (≥ 0x80, §10.2). §21.6: "A user-metadata
record declares an experimental-range (≥ 0x80) document encoding | Ignored (ignore-record);
the file is conforming". Not a violation.
Record 2: encoding byte 0x03 → reserved range 3–0x7F. §21.5 R1: "A user-metadata record
declares a document encoding of 0, or a reserved-range value (3-0x7F)" — a registered
violation. §21.5 preamble: "Every row here is a violation all the same: the outcome bounds a
reader's blast radius and never makes the file conforming".
§2.3 `[R-CNF-11]`: "a verifier that has established any violation reports *nonconforming*".
Verdict: **nonconforming**.

## Q06 — reject-tile; no; no

offset = 2000 ≠ S and length = 0 → §15.3 `[R-IDX-03]` row "length = 0 (non-sentinel) |
*structural*: reject-tile — absence is spelled sentinel". Outcome class name (§2.4): **reject-tile**.
(b) §9.7 `[R-LIF-08]`: "an entry `[R-IDX-03]` classifies reject-tile on a *structural* ground
contributes no stored extent to the walk". → **no**.
(c) §5.2 `[R-CNT-21]`: "An entry `[R-IDX-03]` classifies reject-tile on a structural ground
leaves it complete too, and for the opposite reason: it contributes no claimant, the walk
passes over it, and its bytes fall to slack". → **no**.

## Q07 — yes; yes; no

§20.3 `[R-WRT-04]` step 4: "its name, and its dimension and channel names, MAY change; an
extent MAY grow, and MUST NOT shrink; a planar layer's channel list MAY be extended at its end
or shortened from its end, but not both in one commit … A commit MAY make several of these
changes at once, an extension and a shortening of one channel list excepted".
(a) grow + shorten + rename are three permitted changes, none of them the excepted pair → **yes**.
(b) "A channel removed from the end … changes the layer's index content … so the region is
re-emitted under the clause above whether or not entry_count changes with it"; re-emission is
"necessarily at a new placement (`[R-LIF-01]`)", i.e. appended → **yes**.
(c) the excepted pair exactly: "a commit that shortens a planar layer's channel list appends no
channel to it and one that extends it removes none" → **no**.

## Q08 — yes; no

P = 16384² = 268,435,456. Largest plane = float64: P·8 = 2,147,483,648 > 0x7E000000 =
2,113,929,216.
File A: G = (2, 2), N = 4, C·N = 8 addressed tiles. §17.2 `[R-COD-07]`: "Writers MUST NOT
declare this codec for a layer any of whose addressed tiles' decoded size exceeds 0x7E000000
bytes … and a reader MUST treat such a declaration as a validity error at layer scope"
(register L44, Detector reader, Detected layer access) → **yes**.
File B: E₀ = 0 → G₀ = 0, N = 0, zero addressed tiles. §17.2 Note: "The cap is quantified over
the layer's *addressed* tiles, so a layer that addresses none — any dimension extent 0 …
satisfies it whatever its tile shape declares, and codec 4 is conforming there."
`[R-ENC-04]`'s ceiling is still checked but 2³¹ ≪ 2⁶³ − 1 → **no**.

## Q09 — F35; reader; open

Type 0x0100 lies in the reserved record-type range 0x0003–0x7FFF (§10.2); MU bit = 1.
F35 = "reserved-range type value … with MUST_UNDERSTAND (flags bit 0) set to 1" (reader, open);
F36 = "type value from the reserved range … whatever its MU bit" (verifier, certification).
§21.1: "Some rows are strict specializations of others: where every file exhibiting one row's
condition … necessarily exhibits another's, the file is recorded against the narrower row,
whose detector and detection point are the ones that apply. … F35 of F36 … stand in that
relation." → **F35; reader; open**.

## Q10 — 1; 3a173c06

(a) §15.1 `[R-IDX-01]`: segment CRC array is ⌈entry_count / 2¹⁶⌉ × 4 bytes → ⌈65536/65536⌉ = **1** u32.
(b) The one segment covers exactly 2¹⁶ entries, all sentinels. §15.4 `[R-IDX-05]`: "The CRC-32C
of a segment consisting of 2¹⁶ sentinel entries is `0xEECB3BB2`" (independently recomputed here
over 65536 × `FF×16 00×4`). Stored little-endian → array bytes `b2 3b cb ee`.
§7.4: crc_of_crc_array = "CRC-32C over the index's segment-CRC array". CRC-32C(`b2 3b cb ee`)
= **0x3a173c06** → `3a173c06`.

## Q11 — no; cannot establish

(a) §5.2 `[R-CNT-21]`: "a tile's or a document's decode declined leaves the walk complete, that
claimant being enumerated from its index entry or extent slot." The walk enumerated every
claimant, no scope was rejected, no layer declined, no stop-at-first-violation → **no**.
(b) §2.3 `[R-CNF-11]` names as *cannot establish* grounds "when it declines a layer's or a
tile's decode on resource grounds and so cannot check §14's decoded-content obligations
(`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`), or when it declines to decode a user-metadata
document (`[R-MTA-09]`)"; §18.2 `[R-MTA-09]`: "A **verifier** that declines to decode a
document on either bound above cannot establish that document's conformance and MUST NOT
certify the file". No violation established → **cannot establish**.

## Q12 — yes; no

§18.2 `[R-MTA-04]`, "Finite numbers only": "A document is unreadable if it contains a number
whose binary64 interpretation is not finite — which covers a magnitude that overflows on that
conversion, `1e400` being the ordinary case".
A: 1e400 overflows binary64 under roundTiesToEven → +∞, not finite → unreadable → **yes**.
B: 1e-400 underflows to 0.0, which is finite; no restriction addresses underflow, and the other
three restrictions are satisfied by the premises (object, no BOM, no duplicate keys, well-formed
UTF-8, key rules; ordering is not an unreadability ground per `[R-MTA-05]`) → **no**.

## Q13 — yes; yes; no

§21.9 guarantees "channels per layer, C | 4096"; 5000 exceeds it. C = 5000 ≤ 65,535, the hard
`u16` limit (§21.9 `[R-ERR-05]`), so nothing is violated.
(a) `[R-ERR-04]`: "A file exceeding any of these remains conforming" → **yes**.
(b) `[R-ERR-04]`: "a reader MAY decline it: at the whole file, or at the narrowest scope whose
stated or derived quantities exceed what it can serve, be that a layer …" and the refusal "MUST
be reported as a resource limit" → **yes**.
(c) `[R-ERR-04]`: "Software that declines **on that ground** a file whose every quantity lies
within the table is not a conforming reader (`[R-CNF-03]`)" → **no**.

## Q14 — yes; no

Entry offset 4096, length 0, non-sentinel → §15.3 structural reject-tile. The output relocates
at least one of L's stored extents, so §20.5 `[R-WRT-07]` regenerates L's region.
"Regenerating a region means classifying every entry in it … An entry §15.3 classifies
reject-tile on a structural ground is neither — `[R-IDX-03]` gives it no stored extent for a
re-pointing to target — so regenerating the region cannot proceed without meeting it, and the
violation is thereafter one the compactor has detected. `[R-WRT-06]` then obliges refusal: the
compactor can neither reproduce the entry nor invent a replacement, and no drop is available, a
tile-index entry being no record §20.4's table licenses dropping."
(a) **yes**; (b) **no**.

## Q15 — 13; 02 01

G₀ = ⌈10/4⌉ = 3, G₁ = 3, N = 9. Coordinate (5, 6): t = (5 div 4, 6 div 4) = (1, 1).
§11.4 `[R-GEO-06]`: s = t₀·G₁ + t₁ = 1·3 + 1 = 4; `g` has channel index c = 1 → disk ordinal
c·N + s = 1·9 + 4 = **13**.
Sentinel → §13.3 `[R-TYP-08]`: "in a planar layer exactly the entry's channel reads as fill
there"; §13.1 `[R-TYP-06]`: a reader "MUST return fill bit-exactly as recorded". Recorded fill
field bytes are `02 01` → returned **02 01** (uint16 0x0102 little-endian).
