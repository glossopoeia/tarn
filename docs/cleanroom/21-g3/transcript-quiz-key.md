# Round 21 — quiz key transcript

Read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` only (whole file, in
four Read calls plus one `grep -n '^#'`). Ran two local Python scripts in the
scratchpad (CRC-32C table implementation + arithmetic); neither read any file.
No other file, no git, no web.

Disclosure note: runtime placed a project-instruction pointer (CLAUDE.md → AGENTS.md)
and an index of maintainer memory files in my context before I began. I did not open
any of them and did not use their contents; they named prior rounds and working
process, not spec content. Recorded in `disclosure`.

CRC implementation validated against three constants the document itself fixes:
CRC-32C("123456789") = 0xE3069283 (§4.5); 4-sentinel entry array = 0x80A34955 with
crc_of_crc_array 0xC4EE982E (§7.4 example); full all-sentinel segment = 0xEECB3BB2
(§15.4). All three reproduced exactly.

---

## Q01 — A, B, C verdicts

**File A.** Encoding 0x02 = zstd (assigned, §18.2). Frame is clean on every
constraint §18.2 carries over from `[R-COD-06]`: magic, no skippable/second frame,
Dictionary_ID zero, no content-checksum flag. Document decodes to 4 KiB, within V's
16 MiB bound. The only exceedance is Window_Size 32 MiB against V's 8 MiB window
bound. `[R-MTA-09]`: "The frame's declared `Window_Size` is unconstrained here for the
same reason, and takes the same treatment: a reader's window bound is its own, no
smaller than §21.9's guarantee for that quantity, and a frame declaring more than the
reader admits is ignore-record on that ground … and no violation: the file exceeds a
§21.9 guarantee and so remains conforming while the reader MAY decline it
(`[R-ERR-04]`)." And: "A **verifier** that declines to decode a document on the bound
above cannot establish that document's conformance and MUST NOT certify the file …
it fixes the file's verdict as *cannot establish* only where the verifier established
no violation elsewhere." §21.5's preamble confirms the window is one of the two
decline grounds. §2.3 lists "when it declines to decode a user-metadata document
(`[R-MTA-09]`)" among the cannot-establish grounds. No violation elsewhere (file
otherwise conforming, V traverses whole). → **cannot establish**.

**File B.** Encoding 0x86 ≥ 0x80 = experimental range (§10.2's metadata-encoding
row). §21.6 row: "A user-metadata record declares an experimental-range (≥ 0x80)
document encoding | Ignored (ignore-record); the file is conforming … No document rule
attaches at such an encoding, so a verifier certifies, reporting the record it
ignored". `[R-MTA-10]` says the same: the record "is not among `[R-CNF-11]`'s
cannot-establish grounds, and certification is unaffected". → **conforming**.

**File C.** Encoding 0x05 lies in the reserved range 3–0x7F. §21.5 row R1: "A
user-metadata record declares a document encoding of 0, or a reserved-range value
(3-0x7F)" — a violation with outcome ignore-record, detector reader, detected at open.
§21.5 preamble: "Every row here is a violation all the same: the outcome bounds a
reader's blast radius and never makes the file conforming". §21.5 also: "Encoding 0
and a reserved-range value are unassigned too, and R1 registers both as violations:
what `[R-MTA-10]` withdraws is the document's content rules, never the encoding byte's
own value set". V establishes it; `[R-CNF-11]` — established violation takes priority.
→ **nonconforming**.

Answer: cannot establish, conforming, nonconforming.

---

## Q02 — R's three declines

§21.9 minimum guarantees: decoded user-metadata document 16 MiB; zstd Window_Size
8 MiB. R's bounds: 8 MiB document, 8 MiB window.

(i) doc 12 MiB, window 4 MiB — both inside the table. `[R-ERR-04]`: "Software that
declines **on that ground** a file whose every quantity lies within the table is not a
conforming reader (`[R-CNF-03]`)". `[R-MTA-09]` fixes the floor directly: "a reader
instead decodes with a bound of its own choosing, **no smaller than §21.9's
user-metadata guarantee**". R's 8 MiB is smaller. → **no**.

(ii) doc 20 MiB > 16 MiB guarantee. §18.2's Note: "A file whose document decodes to
more than the guarantee stays conforming, and it falls outside `[R-CNF-03]`'s
acceptance duty … A reader that proceeds takes ignore-record for that record; a reader
that instead declines on resource grounds under `[R-ERR-04]` does so at the whole
file." Declining is licensed. → **yes**.

(iii) window 32 MiB > 8 MiB guarantee (document only 1 MiB, so the doc bound is not
what bites). `[R-MTA-09]`: "a frame declaring more than the reader admits is
ignore-record on that ground … the file exceeds a §21.9 guarantee and so remains
conforming while the reader MAY decline it (`[R-ERR-04]`)". → **yes**.

Answer: no, yes, yes.

---

## Q03 — nonzero Dictionary_ID under encoding 2

(a) The record is a user-metadata record under assigned encoding 2 whose frame carries
Dictionary_ID 0x00000007. `[R-MTA-09]` imports "no nonzero dictionary ID" as a frame
constraint on the document. §21.5 row R4 registers it: "A user-metadata document
stored under encoding 2 breaks one of the frame constraints §18.2 states or carries
over from `[R-COD-06]` … **unlike R3, the constraint is broken whether or not the
bytes decode**"; instance "a nonzero dictionary ID, top-level extent". §21.5's
outcome heading: **ignore-record**. `[R-MTA-09]` closes: "Any violation here is
ignore-record, never the tile-scope outcome §17.2 assigns." → **ignore-record**.

(b) The question states V *reads the frame header*. The Dictionary_ID is in that
header, and R4's detector is *reader* at *extent use* — a verifier inherits every
reader obligation (§2.3). So the violation is established, notwithstanding the
window-bound decline. `[R-CNF-11]`: "An established violation takes priority: a
verifier that has established any violation reports *nonconforming*, however many
requirements it was unable to check, and *cannot establish* is available only to a
traversal that established no violation." → **nonconforming**.

(c) `[R-CNF-11]`: a verifier "certifies only violation-free files" (`[R-CNF-12]`), and
`[R-MTA-09]` independently bars certification after a decline. → **no**.

---

## Q04 — layer record sizes

Field order fixed by §7.4's table. Calibrated against §7.4's worked example, which
states "Name and the nine scalars from layout through channel count occupy 4 + 34
bytes" — so the nine scalars total 34 (1+2+2+2+8+8+8+1+2), the dimension entry 18
(1+1+8+8), a float32 channel entry 12 (1+1+2+1+4), the trailing fixed fields 13
(1+8+4).

(a) name 1+2 = 3; nine scalars 34; dim `y` 18 + dim `x` 18 = 36; channel `p`
(uint16, fill 2) 1+1+2+1+2 = 7; channel `q` (float64, fill 8) 1+1+2+1+8 = 13, so 20;
trailing 13. Total 3+34+36+20+13 = **106**.

(b) §11.2: G₀ = ⌈300/128⌉ = 3, G₁ = ⌈500/256⌉ = 2, N = 6. Planar → addressed-tile
count = C·N = 2·6 = 12; unstored tiles are still *addressed* (§3.1), so entry_count =
12. `[R-CNT-17]`: extent_length = 12×20 + ⌈12/2¹⁶⌉×4 = 240 + 4 = **244**.

(c) Dimension entries follow name + the nine scalars: 3 + 34 = **37**.

---

## Q05 — all-sentinel index of 3 entries

Sentinel = `FF ×16 00 ×4` (`[R-IDX-02]`). Entry array = 60 bytes.

(a) One segment (⌈3/2¹⁶⌉ = 1), partial, so its CRC "covers only its actual bytes"
(`[R-IDX-04]`) — and `[R-IDX-05]` expressly forbids substituting 0xEECB3BB2 for a
partial segment. CRC-32C(60 bytes) = 0xD171D122, stored little-endian:
**`22 d1 71 d1`**.

(b) crc_of_crc_array = CRC-32C over those 4 bytes = 0x34C74AFB, little-endian:
**`fb 4a c7 34`**.

(c) `[R-CNT-17]`: 3×20 + 1×4 = **64**.

---

## Q06 — planar ordinals

G₀ = 1024/64 = 16, G₁ = 4096/64 = 64, N = 1024. (700, 3000): t = (10, 46), u = (60, 56).
`[R-GEO-06]`: s = t₀·G₁ + t₁ = 640 + 46 = 686. `blue` is the third declared channel →
index c = 2 (0-based, §3.1). Disk ordinal = c·N + s = 2048 + 686 = **2734**.

(b) `[R-IDX-01]`: "The entry for the tile with disk ordinal k is the k-th entry, at
region byte 20·k" → 20 × 2734 = **54,680**.

(c) In-tile ordinal = Σ uᵢ·∏_{j>i} Tⱼ = 60·64 + 56 = **3896**.

(d) Planar numeric channel: offset of value k = k·Bᶜ (`[R-SER-02]`), Bᶜ = 4 for
float32 → 3896 × 4 = **15,584**.

---

## Q07 — packed bool plane

Planar bool → §14.3 packing, decoded size ⌈P/8⌉ with P = 3·5 = 15 → 2 bytes.
Byte 0 holds values 0–7 LSB-first: bits 0,3,4 set → 0x19. Byte 1 holds values 8–14 in
bits 0–6: bits 0,2,3 set → 0x0D; P mod 8 = 7, so bit 7 is the single pad bit, and
`[R-SER-05]` fixes it to the channel's fill bit — fill 0x01 = true → bit 7 set →
0x8D.

(a) **`19 8D`**.
(b) Codec none → `[R-COD-04]`: "The index entry's length therefore MUST equal the
tile's decoded size" → **2**.

---

## Q08 — interleaved edge tile

G = (2, 2); tile (1,1) covers x₀ ∈ {2,3}, x₁ ∈ {2,3}; extents are 3 and 3, so only
(2,2) is real and the other three positions are padding (§11.3). P = 4, Q = 1 + 2 = 3,
decoded size 12 (`[R-SER-02]`). In-tile ordinal = u₀·2 + u₁, so ordinal 0 = (0,0) =
coordinate (2,2) — the stored sample; ordinals 1–3 are padding. `[R-SER-05]`: every
padding position encodes each channel's recorded fill.

Answer: **`07 02 01 2A FE FF 2A FE FF 2A FE FF`**.

---

## Q09 — version_major 3 with dirty reserved bytes

§6.2's ordered validation: magic, trailer CRC, version gate, *then* the remaining
field gates. `[R-CNT-07]`: "A reader MUST reject-file when version_major is 0 …
or is a major it does not implement". §2.3: "a file declaring another major is neither
conforming nor nonconforming under it … that refusal is not a finding about its
bytes", and a verifier reports cannot establish "when the file names a format major
version it does not implement".

(a) **cannot establish**.

(b) F15 (reserved bytes nonzero) would otherwise apply, but §21.2's preamble excludes
it: "A file declaring a format major other than 1 is neither conforming nor
nonconforming under this text … Four rows are outside that reasoning and do reach it,
because their subject is a field fixed across every major (`[R-CNT-24]`): F8 and F1's
trailer-magic instance, F14's trailer CRC … and F6 with F1's front-block instance".
F15 is not among the four; the magic, trailer CRC and front block are all clean here.
§21.6 further records that an unimplemented major is not a register row at all. →
**no**.

---

## Q10 — experimental vs reserved MU = 1 sub-record

(a) 0x8123 ≥ 0x8000 = experimental record-type range (§10.2). §10.3's prohibition on
emitting experimental values "binds the writer's conduct, not the bytes"
(`[R-CNT-15]`, `[R-CNF-02]`). §21.6: "an **experimental-range top-level record type
carrying MU = 1** … `[R-CNF-02]` makes the file conforming all the same. The qualifier
is load-bearing — the same type as a layer sub-record is reject-layer and never a
ground to refuse the file". No register row fires. → **yes**.

(b) `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer, and where
the file is otherwise conforming a reader MUST NOT reject the file for it". P is
conforming. → **no**.

(c) 0x0123 lies in the reserved range 0x0003–0x7FFF. L25: "A layer record's sub-record
carries a type value from the reserved range 0x0003-0x7FFF … emitting one is a
violation whatever its MU bit"; L24 is the MU = 1 specialization, detector reader,
detected at layer access. → **no**.

(d) Because Q exhibits a registered violation it is nonconforming, and `[R-CNT-18]`'s
own carve-out applies: "on a nonconforming file `[R-CNF-12]`'s licence to reject on
any detected violation is untouched." `[R-CNF-12]`: "For a nonconforming file no
acceptance obligation exists — a reader MAY reject it upon detecting any violation".
→ **yes**.

---

## Q11 — compactor meets a half-sentinel entry

offset = S, length = 0x1000 ≠ S. §15.3 row: "offset = S ∧ length ≠ S, or offset ≠ S ∧
length = S | *structural*: reject-tile" (register row T7). Structural ground, so
`[R-IDX-03]` gives the entry no stored extent. The region relocates, so it is
regenerated. `[R-WRT-07]`: "An entry §15.3 classifies reject-tile on a structural
ground is neither — `[R-IDX-03]` gives it no stored extent for a re-pointing to
target — so regenerating the region cannot proceed without meeting it, and the
violation is thereafter one the compactor has detected. `[R-WRT-06]` then obliges
refusal: the compactor can neither reproduce the entry nor invent a replacement, and
no drop is available, a tile-index entry being no record §20.4's table licenses
dropping."

Answer: **a**.

---

## Q12 — partial slack total

`[R-CNT-21]`: "because the verifier elected under `[R-CNF-11]` to stop at the first
violation — the verifier MUST report the total as partial. A partial total is F less
the bytes claimed by the claimants the walk did enumerate."

(a) 4096 − 3000 = **1096**.
(b) **partial** — the stop-at-first-violation election is named expressly.
(c) `[R-CNF-11]`: an established violation forces **nonconforming**.

---

## Q13 — shrink 10 → 9

(a) G = ⌈10/4⌉ = 3, interleaved → addressed = N = **3**.
(b) G = ⌈9/4⌉ = 3 → **3**. (Grid count unchanged; entry_count and ordinals unchanged.)

Tile 2 covers t = 8..11. Before: real 8, 9; padding 10, 11. After: real 8; padding
9, 10, 11. So t = 9 becomes a padding position, and `[R-SER-05]` fixes a padding
position's stored content to the channel's fill (0x00). §20.3 step 4 bars a commit
that alters, for a tile stored in the superseded generation, "the set of padding
positions (§11.3) **and the content `[R-SER-05]` fixes there**", but carves out "a
change that leaves every one of those tiles' stored bytes meaning exactly what they
meant — … or **a new padding position whose stored byte already holds the fill
`[R-SER-05]` fixes** — is not what this bars." The shrink clause restates the same
test: "a shrink is permitted exactly where it alters nothing §14 fixes for any tile
the layer stores in the generation this commit supersedes."

(c) stored byte 0x07 ≠ fill 0x00 → the new padding position would violate
`[R-SER-05]` → barred → **no**.
(d) stored byte 0x00 = fill → the carve-out applies exactly → **yes**.

---

## Q14 — zstd window on an 18-byte tile

Interleaved, P = 2·3 = 6, Q = 1 + 2 = 3, decoded size P·Q = 18 (`[R-SER-02]`).

(a) `[R-COD-06]`: writers "MUST NOT declare a window size exceeding the tile's decoded
size; a reader MUST treat either as a validity error at tile scope" (register row
T21). Largest admissible declared Window_Size = **18** bytes.

(b) §17.2's Note: "with Single_Segment_Flag set there is no Window_Descriptor and
Window_Size is the frame content size … without it, the Window_Descriptor cannot
express less than 1 KiB. A tile whose decoded size is below 1 KiB — §14.2's worked
examples give 18 and 30 bytes … — is therefore encodable under codec 3 only as a
single-segment frame." 18 < 1 KiB, so any Window_Descriptor form would declare ≥ 1 KiB
and violate `[R-COD-06]`. → **yes**. (The Note is non-normative labelling, but the
conclusion is forced by the normative window rule plus RFC 8878's encoding.)

---

## Q15 — dirty front-block reserved bytes, never resident

Bytes [8,16) are `00 00 00 00 00 00 00 01`, not the constant's eight zeros (§6.1's
table: offset 8, size 8, value zero, structural; "Writers MUST emit exactly these 16
bytes").

(a) `[R-CNT-04]`: "A reader that would have to issue a further range request to obtain
those bytes MAY defer or omit the check". The described reader never holds them. →
**no**.

(b) File conformance is a pure predicate on bytes (`[R-CNF-02]`), and the block is not
byte-identical to the constant. → **no**.

(c) F6's condition text: "the obligation binds a reader holding those bytes resident,
and a reader that would have to fetch them MAY defer or omit the check (`[R-CNT-04]`);
**a verifier holds no such exemption (§2.3)**." Appendix H repeats it. Established
violation → **nonconforming**.

(d) F6's Governing rule cell names **`[R-CNT-04]`** first (no parenthetical
secondaries). F1 does not apply: bytes [0,8) are correct, nothing is byte-reversed;
§21.1 notes F1 is a strict specialization of F6, and this file exhibits only the
general row, in its "reserved bytes [8,16)" instance.
