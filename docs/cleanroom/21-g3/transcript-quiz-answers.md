# Cleanroom round 21 — quiz answerer transcript

## Disclosure

Files read: exactly one — `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
read whole in sequential chunks via `sed -n`. No other file, no directory listing,
no git history, no ADR, no conformance vector, no registry, no web access.

Local computation only: one Python CRC-32C implementation (bitwise, Castagnoli
0x82F63B78 reflected, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) that reads no files,
plus integer arithmetic. The implementation was validated against three constants
the specification itself publishes before I trusted it on anything new:

- CRC-32C("123456789") = 0xE3069283 (§4.5 check vector) — reproduced.
- CRC-32C(zero bytes) = 0x00000000 (§4.5) — reproduced.
- §7.4's worked example: CRC-32C over 4 sentinel entries = 0x80A34955, and
  crc_of_crc_array over those 4 bytes = 0xC4EE982E — both reproduced.
- Appendix B / §15.4: CRC-32C of a full 2^16-entry all-sentinel segment
  = 0xEECB3BB2 — reproduced.

**Context I did not ask for.** My runtime placed material in context before I
began: a project instruction file pointer, an index of the maintainer's memory
notes with descriptive titles, a task list, and a git status block carrying
recent commit subject lines. I did not open any of those files. Some of the
commit subject lines and memory-index titles name topics that overlap this
slate. I disregarded them as evidence; every answer below is derived from and
cited to the specification text, which I quote. Disclosing their presence per
the brief.

---

## Q01 — three user-metadata files, verifier verdicts

Common facts: each file has one top-level type 0x0002 record, inline_length 1,
nonzero extent slot, extent_length well above 5, terminal CRC verifies. So the
structural gates that precede the document (F21, F22, F23, R2) all pass.
V implements every core codec/filter, applies a 16 MiB document bound and an
8 MiB Window_Size bound, does not stop at first violation, traverses whole.

Both of V's bounds are legal: §21.9's guarantees are 16 MiB for a document and
8 MiB for `Window_Size`, and §18.2 requires a reader's bounds be "no smaller
than" those. V's are exactly at the floor.

**File A — encoding 0x02, all encoding-2 frame constraints met, Window_Size
32 MiB, document 4 KiB of well-formed sorted duplicate-free JSON object.**

No violation exists. §18.2 removes any constraint on the declared window for a
metadata document:

> "The frame's declared `Window_Size` is unconstrained here for the same reason,
> and takes the same treatment: a reader's window bound is its own, no smaller
> than §21.9's guarantee for that quantity, and a frame declaring more than the
> reader admits is ignore-record on that ground — the reader's capability, not a
> failure to decode within the meaning of R3, and no violation" `[R-MTA-09]`

32 MiB > V's 8 MiB, so V declines. §18.2 then fixes the verdict:

> "A **verifier** that declines to decode a document on the bound above cannot
> establish that document's conformance and MUST NOT certify the file ... The
> decline is one of the unchecked requirements `[R-CNF-11]` obliges the verifier
> to report, and it fixes the file's verdict as *cannot establish* only where
> the verifier established no violation elsewhere" `[R-MTA-09]`

"The bound above" reaches the window bound: the window sentence says it "takes
the same treatment", §21.5's preamble names both explicitly ("declines the
decode on the size bound **or on the frame's declared window**"), and §2.3 lists
"when it declines to decode a user-metadata document (`[R-MTA-09]`)" without
distinguishing. → **cannot establish**.

**File B — encoding 0x86.** ≥ 0x80 is the experimental range (§10.2, §18.2).
§21.6:

> "A user-metadata record declares an experimental-range (≥ 0x80) document
> encoding | Ignored (ignore-record); the file is conforming ... No document
> rule attaches at such an encoding, so a verifier certifies, reporting the
> record it ignored | `[R-MTA-03]`, `[R-EXT-03]`, `[R-CNF-02]`, `[R-MTA-10]`"

→ **conforming**.

**File C — encoding 0x05.** 3–0x7F is the reserved range. §21.5 row R1:

> "R1 | A user-metadata record declares a document encoding of 0, or a
> reserved-range value (3-0x7F)"

R1 is a register row, i.e. a violation ("Every row here is a violation all the
same: the outcome bounds a reader's blast radius and never makes the file
conforming"). §21.5's preamble is explicit that `[R-MTA-10]` does not rescue it:
"Encoding 0 and a reserved-range value are unassigned too, and R1 registers both
as violations: what `[R-MTA-10]` withdraws is the document's content rules,
never the encoding byte's own value set". V establishes it → **nonconforming**
(§2.3: "An established violation takes priority").

**Answer: cannot establish, conforming, nonconforming.**

---

## Q02 — a reader with an 8 MiB document bound

§21.9 guarantees: user-metadata document 16 MiB; zstd `Window_Size` 8 MiB.
§18.2 requires a reader's document bound be "no smaller than §21.9's
user-metadata guarantee" — R's 8 MiB is below that floor. §21.9's closing rule
states the disqualification instance-wise:

> "A file exceeding any of these remains conforming, and a reader MAY decline
> it ... Software that declines **on that ground** a file whose every quantity
> lies within the table is not a conforming reader (`[R-CNF-03]`)" `[R-ERR-04]`

(i) Window 4 MiB (≤ 8 MiB guarantee), document 12 MiB (≤ 16 MiB guarantee).
Every quantity lies within the table, and R declines on a resource ground.
That is precisely the disqualifying case → **no**.

(ii) Window 4 MiB, document 20 MiB. 20 MiB exceeds the 16 MiB guarantee, so
the file "exceeds any of these" and "a reader MAY decline it". A conforming
reader holding the legal 16 MiB bound would decline this same document → **yes**.

(iii) Window 32 MiB, document 1 MiB. 32 MiB exceeds the 8 MiB `Window_Size`
guarantee; §18.2 makes the window bound the reader's own capability and the
decline "no violation" → **yes**.

*Competing reading, recorded.* One could read §18.2's "no smaller than §21.9's
user-metadata guarantee" as a flat per-reader requirement, so that R's illegal
bound makes *every* decline it produces inconsistent with conformance, giving
no/no/yes. I reject it because `[R-ERR-04]` frames the disqualification as
declining *a file whose every quantity lies within the table*, and pairs it with
an express MAY for files that exceed. (ii) is where the two readings part.

**Answer: no, yes, yes.**

---

## Q03 — nonzero Dictionary_ID on a metadata frame

Encoding 0x02 is assigned (zstd), so §18.2's frame constraints attach:

> "Encoding 2 stores it as exactly one RFC 8878 compressed frame occupying the
> extent's bytes before its terminal CRC, under the frame constraints of
> `[R-COD-06]` that do not reference a tile: the frame magic; no skippable frame
> and no second frame; **no nonzero dictionary ID**; no content-checksum flag."
> `[R-MTA-09]`

Dictionary_ID 0x00000007 breaks it. Register row R4:

> "R4 | A user-metadata document stored under encoding 2 breaks one of the frame
> constraints §18.2 states or carries over from `[R-COD-06]` ... a nonzero
> dictionary ID ...; **unlike R3, the constraint is broken whether or not the
> bytes decode**"

V read the frame header, which is where Dictionary_ID lives, so V established
the violation notwithstanding its decline to decode.

(a) R4's outcome class is §21.5's: **ignore-record**. §18.2 confirms: "Any
violation here is ignore-record, never the tile-scope outcome §17.2 assigns."

(b) V also declines on the window bound (64 MiB > 8 MiB), which would be a
cannot-establish ground — but §2.3 orders them:

> "An established violation takes priority: a verifier that has established any
> violation reports *nonconforming*, however many requirements it was unable to
> check, and *cannot establish* is available only to a traversal that
> established no violation." `[R-CNF-11]`

→ **nonconforming**.

(c) "a verifier certifies only violation-free files" (`[R-CNF-12]`) → **no**.

**Answer: (a) ignore-record; (b) nonconforming; (c) no.**

---

## Q04 — layer record sizes

§7.4's field order and widths, packed with no padding ("fields are packed in
table order with no alignment or padding between them", `[R-CNT-18]`):

| Field | Bytes |
|---|---|
| name `ab` (u8 len + 2) | 3 |
| layout u8 | 1 |
| linearization u16 | 2 |
| codec u16 | 2 |
| filter u16 | 2 |
| alignment A u64 | 8 |
| slab S u64 | 8 |
| A_slab u64 | 8 |
| rank d u8 | 1 |
| channel count C u16 | 2 |
| dim 0: name(1+1) + extent u64 + tile extent u64 | 18 |
| dim 1: same | 18 |
| ch 0 `p` uint16: name(1+1) + type u16 + fill(1+2) | 7 |
| ch 1 `q` float64: name(1+1) + type u16 + fill(1+8) | 13 |
| index_encoding u8 | 1 |
| entry_count u64 | 8 |
| crc_of_crc_array u32 | 4 |

(a) 3+1+2+2+2+8+8+8+1+2 = 37; +36 dims = 73; +20 channels = 93; +13 trailing
= **106**.

Cross-check against §7.4's worked example, which reports "Name and the nine
scalars from layout through channel count occupy 4 + 34 bytes, the dimension
entry 18, the channel entry 12, and the trailing fixed fields 13 — 81 exactly".
My scalar block is the same 34; my name field is 3 not 4; 18 per dimension and
13 trailing match exactly.

(b) §11.2: G₀ = ⌈300/128⌉ = 3, G₁ = ⌈500/256⌉ = 2, N = 6. Planar, so the
addressed-tile count is C·N = 2·6 = 12 (`[R-GEO-03]`), and entry_count equals it
(`[R-CNT-17]`). Then `[R-CNT-17]`: extent_length = 12 × 20 + ⌈12/2¹⁶⌉ × 4
= 240 + 4 = **244**. Storedness is irrelevant: the region is entry_count entries
plus the segment CRC array whether or not any tile is stored (§15.1), and the
sentinel occupies a full 20-byte entry (§15.2).

(c) Dimension 0's entry begins after name + the nine scalars = 3 + 34 = **37**.
(Example cross-check: there the same boundary is 4 + 34 = 38, and the example
shows the dimension name at offset 38.)

**Answer: (a) 106; (b) 244; (c) 37.**

---

## Q05 — a 3-entry all-sentinel index

Sentinel entry = `FF ×16 00 ×4` (§15.2, `[R-IDX-02]`). entry_count = 3 →
⌈3/2¹⁶⌉ = 1 segment, covering entries [0, 3), i.e. 60 bytes.

§15.4: "the s-th u32 of the segment CRC array is the CRC-32C over exactly those
entries' bytes as stored — the final partial segment's CRC covers only its
actual bytes." And `[R-IDX-05]`: the 0xEECB3BB2 constant is licensed only for a
**full** segment — "one covering exactly 2¹⁶ entries" — and "a partial segment's
CRC MUST be computed." So the constant does **not** apply here.

Computed: CRC-32C over 60 bytes (3 × sentinel) = 0xD171D122.
Stored little-endian (`[R-ENC-09]`) → (a) **`22 d1 71 d1`**.

crc_of_crc_array = CRC-32C over the 4-byte segment CRC array as stored (§7.4,
§8.1) = CRC-32C(`22 d1 71 d1`) = 0x34C74AFB, little-endian → (b)
**`fb 4a c7 34`**.

(c) `[R-CNT-17]`: 3 × 20 + ⌈3/2¹⁶⌉ × 4 = 60 + 4 = **64**.

Method cross-check: the same code on §7.4's 4-sentinel example returns
0x80A34955 (`55 49 a3 80`) and crc_of_crc_array 0xC4EE982E, byte-for-byte what
the specification prints; on 2¹⁶ sentinels it returns 0xEECB3BB2, matching
§15.4.

---

## Q06 — planar disk ordinal and offsets

G₀ = 1024/64 = 16, G₁ = 4096/64 = 64, N = 16·64 = 1024 (§11.2).
(700, 3000): t = (700 div 64, 3000 div 64) = (10, 46); u = (60, 56).

`[R-GEO-06]`: "Under linearization 1, the **spatial tile ordinal** ... is
s = Σᵢ tᵢ · ∏_{j>i} Gⱼ" → s = 10·64 + 46 = 686.
"The **disk tile ordinal** ... is s for an interleaved layer, and **c · N + s**
for a planar layer ... where c is the channel's index" — index is "its 0-based
position in that order" (§3.1), so the third declared channel has c = 2.

(a) 2·1024 + 686 = **2734**.
(b) §15.1: "The entry for the tile with disk ordinal k ... is the k-th entry, at
region byte 20·k" → 20 × 2734 = **54680**.
(c) `[R-GEO-06]`: in-tile ordinal = Σᵢ uᵢ · ∏_{j>i} Tⱼ = 60·64 + 56 = **3896**.
(d) §14.2 table, planar numeric channel: offset of value k is k · Bᶜ; float32
Bᶜ = 4 → 3896 × 4 = **15584**.

**Answer: (a) 2734; (b) 54680; (c) 3896; (d) 15584.**

---

## Q07 — packed planar bool plane

P = ∏Tᵢ = 3·5 = 15. Planar bool → §14.3 packing, decoded size ⌈15/8⌉ = 2.
No padding positions exist here: G₀·T₀ = 2·3 = 6 = E₀ and G₁·T₁ = 2·5 = 10 = E₁,
so §11.3's condition Gᵢ·Tᵢ > Eᵢ fails on both axes.

`[R-SER-03]`: "value k occupies bit k mod 8 of byte k div 8 (§4.4), with
0 = false and 1 = true".

Byte 0, values 0–7 = T F F T T F F F → bits 0,3,4 set → 0x19.
Byte 1, values 8–14 = T F T T F F F → bits 0,2,3 set → 0x0D.

P mod 8 = 7 ≠ 0, so bit position 7 of the final byte is a pad bit. `[R-SER-05]`:
"Every pad bit (§14.3) MUST carry the plane's channel's fill bit." Fill byte is
0x01 = true (§13.2), so the fill bit is 1 → byte 1 = 0x0D | 0x80 = 0x8D.

This mirrors §14.3's worked example exactly ("with fill true, `55 FD` (pad bits
2–7 set)").

(a) **`19 8D`**.
(b) Codec none → `[R-COD-04]`: "The index entry's length therefore MUST equal
the tile's decoded size" → **2**.

---

## Q08 — interleaved edge tile with padding

G₀ = ⌈3/2⌉ = 2, G₁ = 2. Tile (1,1) covers coordinates 2–3 on both axes; with
extents 3 and 3, only (2,2) is real and (2,3), (3,2), (3,3) are padding
positions (§11.3).

P = 4, C = 2, Q = ΣBᵢ = 1 + 2 = 3 (§14.2), decoded size P·Q = 12.
In-tile ordinals u₀·T₁ + u₁: (0,0)→0 [real], (0,1)→1, (1,0)→2, (1,1)→3 [padding].
Interleaved value order is sample-major, "each sample's channel values are
adjacent, in declared channel order" (`[R-SER-01]`).

`[R-SER-05]`: "at every padding position, a writer MUST encode, for each channel
the position carries, that channel's fill value — the recorded fill bytes for a
numeric channel". So each padding sample is `2A FE FF`.

Bytes [0,3) = 07 02 01; [3,6) = [6,9) = [9,12) = 2A FE FF.

**Answer: `07 02 01 2A FE FF 2A FE FF 2A FE FF`.**

(This is §14.5's example shape — "values 1–15 are each the bytes `CD AB`" — with
two channels instead of one.)

---

## Q09 — version_major 3 with nonzero trailer reserved bytes

§6.2 fixes the order: "A reader MUST validate, in order: the trailer magic; the
trailer CRC; the version gate (§6.3) ... and then, those gates passed, MUST
validate all of the following ... reserved bytes zero." Magic and CRC pass; the
version gate fires: `[R-CNT-07]` obliges reject-file for "a major it does not
implement". The reserved-byte check is *behind* that gate and never runs.

(a) §2.3: a verifier reports "*cannot establish* — the last where some
requirement is one it is unable to check on a capability or resource ground,
**as when the file names a format major version it does not implement**".
Also `[R-CNF-02]`: "a file declaring another major is neither conforming nor
nonconforming under it ... that refusal is not a finding about its bytes."
→ **cannot establish**.

(b) §21.2's preamble is decisive:

> "A file declaring a format major other than 1 is neither conforming nor
> nonconforming under this text ... **Four rows are outside that reasoning and
> do reach it**, because their subject is a field fixed across every major
> (`[R-CNT-24]`): F8 and F1's trailer-magic instance, F14's trailer CRC — the two
> checks §6.2 places before the gate — and F6 with F1's front-block instance"

F15 ("The 4 reserved bytes at trailer offset 56 are not all zero") is not among
the four, and its subject is not fixed across majors: `[R-CNT-24]` pins only the
magic, version_major/minor, and the CRC at offset 60, and lets "A future major
... redefine only the remaining 48 trailer bytes" — offsets [12, 60), which
contains [56, 60). Magic, CRC and every stated field are sound; the question
says nothing amiss in bytes [0, 16), so F6/F1 do not apply either. → **no**.

**Answer: (a) cannot establish; (b) no.**

---

## Q10 — experimental vs reserved sub-record type, MU = 1

(a) File P, sub-record type 0x8123, experimental range (≥ 0x8000, §10.2).
`[R-CNF-03]` presupposes exactly this file:

> "A reader MUST accept every conforming file ... carrying no record of a type it
> does not implement with MUST_UNDERSTAND = 1 — **in a conforming file such a
> type is necessarily from the experimental range**, since a reserved-range type
> carrying MU = 1 is itself a violation"

and `[R-CNF-02]`/`[R-EXT-03]`: §10.3's prohibition on publishing experimental
values "binds the writer's conduct, not the bytes". Flags are MU = 1 / PE = 1
(so `[R-CNT-12]`'s barred combination is absent), reserved bits zero, extent
slot (0,0) = no extent, which §7.2 expressly permits. → **yes**.

(b) `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer, and
**where the file is otherwise conforming a reader MUST NOT reject the file for
it** — on a nonconforming file `[R-CNF-12]`'s licence to reject on any detected
violation is untouched". §21.6 makes the same point about the top-level/sub-record
split: "The qualifier is load-bearing — the same type as a layer sub-record is
reject-layer and never a ground to refuse the file". P is conforming → **no**.

(c) File Q, type 0x0123, reserved range 0x0003–0x7FFF. Rows L24 (reserved-range
sub-record type with MU = 1, reader, layer access) and L25 ("emitting one is a
violation whatever its MU bit") both fire. `[R-EXT-03]`: "a value from a reserved
range MUST NOT be emitted at all before this specification assigns it". → **no**.

(d) Q is nonconforming, and the reader detects L24 at layer access. `[R-CNF-12]`:
"For a nonconforming file no acceptance obligation exists — a reader MAY reject
it upon detecting any violation, including violations whose assigned detector is
the verifier." `[R-CNT-18]`'s carve-out is conditioned on "where the file is
otherwise conforming", which Q is not. → **yes**.

**Answer: (a) yes; (b) no; (c) no; (d) yes.**

---

## Q11 — compactor meets a half-sentinel entry

offset = 0xFFFF_FFFF_FFFF_FFFF = S, length = 0x1000 ≠ S. §15.3's third row:
"offset = S ∧ length ≠ S, or offset ≠ S ∧ length = S | *structural*:
reject-tile". So this is an entry `[R-IDX-03]` classifies reject-tile on a
structural ground — it yields no usable extent.

The output relocates layer A's index region, so the region must be regenerated,
and `[R-WRT-07]` states the consequence directly:

> "An entry §15.3 classifies reject-tile on a structural ground is neither —
> `[R-IDX-03]` gives it no stored extent for a re-pointing to target — so
> regenerating the region cannot proceed without meeting it, and the violation is
> thereafter one the compactor has detected. `[R-WRT-06]` then obliges refusal:
> the compactor can neither reproduce the entry nor invent a replacement, and no
> drop is available, a tile-index entry being no record §20.4's table licenses
> dropping."

(b) is barred by "MUST NOT emit a file carrying a violation it has detected"
(§20.5); (c) is barred by `[R-CNF-04]`'s no-heuristic-repair rule and by
`[R-WRT-06]`'s "neither ... nor invent a replacement"; (d) is barred because
§20.4 licenses dropping only MU = 0 / PE = 0 records and "No commit therefore
removes a layer record".

**Answer: a.**

---

## Q12 — partial slack total

F = committed_file_length = 4096. Claimants enumerated total 3000 bytes,
pairwise disjoint, front block and live trailer included.

(a) `[R-CNT-21]`: "A partial total is F less the bytes claimed by the claimants
the walk did enumerate — an upper bound on the file's true slack, never an
under-count". 4096 − 3000 = **1096**.

(b) `[R-CNT-21]`: "Where the walk of §9.7 does not enumerate every region's
claimants — ... or because the verifier elected under `[R-CNF-11]` to stop at
the first violation — the verifier MUST report the total as partial." →
**partial**. (The exemption for "no live state to walk" does not apply: the live
trailer validated, so there is an F and a live state.)

(c) A violation was established → §2.3's priority rule gives **nonconforming**.
"*Unexamined* is neither a verdict nor *cannot establish* — it constrains the
report, not the verdict."

**Answer: (a) 1096; (b) partial; (c) nonconforming.**

---

## Q13 — a shrink that turns a real position into padding

Rank 1, interleaved, one uint8 channel, fill 0x00.

(a) Before: G = ⌈10/4⌉ = 3, N = 3; interleaved → addressed-tile count N = **3**.
(b) After: G = ⌈9/4⌉ = 3 → **3**. (Grid count unchanged, so entry_count and
extent_length are unchanged too.)

Geometry of the last tile, ordinal 2, covering coordinates 8–11:
- before: 8 and 9 real, 10 and 11 padding;
- after: 8 real, 9, 10 and 11 padding.

So coordinate 9 becomes a padding position of a tile stored in the superseded
generation. §20.3 step 4's bar:

> "A commit MUST NOT change a layer's declarations in a way that alters, for any
> tile that layer stores **in the generation this commit supersedes**, what §14
> fixes for its stored bytes or how they decode — **the set of padding positions
> (§11.3) and the content `[R-SER-05]` fixes there**, the decoded size, the byte
> offset of any sample within the decoded tile image, or the codec and filter
> that produced the stored bytes."

and its own exception:

> "a change that leaves every one of those tiles' stored bytes meaning exactly
> what they meant — a filter whose mandated stride makes it the identity
> (`[R-COD-10]`), or **a new padding position whose stored byte already holds the
> fill `[R-SER-05]` fixes** — is not what this bars."

§20.3 also confirms shrinks are governed by exactly this test: "a shrink is
permitted exactly where it alters nothing §14 fixes for any tile the layer
stores in the generation this commit supersedes."

(c) Stored byte at t = 9 is 07 ≠ fill 0x00. The new padding position would carry
a non-fill byte, breaking `[R-SER-05]` for a stored tile → barred → **no**.
(d) Stored byte is 00 = the recorded fill. The exception applies verbatim →
**yes**. Decoded size (P·Q = 4·1 = 4), sample offsets, codec and filter are all
unchanged, so nothing else in the bar's list is reached.

**Answer: (a) 3; (b) 3; (c) no; (d) yes.**

---

## Q14 — zstd window on an 18-byte tile

Interleaved, P = 2·3 = 6, Q = 1 + 2 = 3, decoded size P·Q = 18 (§14.2) — this is
literally §14.2's worked example ("tile extents (2, 3), P = 6, channels `a`
(uint8) and `b` (uint16): Q = 3, decoded size 18").

(a) `[R-COD-06]`: writers "MUST NOT declare a window size exceeding the tile's
decoded size; a reader MUST treat either as a validity error at tile scope".
The largest permitted is therefore the decoded size itself: **18** bytes.
(Register row T21 states the same condition: "the frame declares a window size
larger than the tile's decoded size".)

(b) §17.2's Note:

> "with Single_Segment_Flag set there is no Window_Descriptor and Window_Size is
> the frame content size ... without it, the Window_Descriptor cannot express
> less than 1 KiB. A tile whose decoded size is below 1 KiB — **§14.2's worked
> examples give 18 and 30 bytes**, §14.3's gives 2 — is therefore encodable under
> codec 3 only as a single-segment frame"

18 < 1 KiB → **yes**.

**Answer: (a) 18; (b) yes.**

---

## Q15 — a corrupt front block a remote reader never fetches

Bytes [0,16) end `... 00 00 00 01`; §6.1 requires bytes [8,16) to be zero
("Writers MUST emit exactly these 16 bytes"). Byte 15 = 0x01 breaks it.

(a) `[R-CNT-04]`: "A reader that would have to issue a further range request to
obtain those bytes MAY defer or omit the check: its open path is anchored at the
trailer (§6.2), and the two-request accounting of §6.4 does not include the front
block. **The test is residency, not transport.**" This reader's two ranges never
make [0,16) resident, and everything else in the file is conforming → **no**.

(b) File conformance is "a pure predicate on bytes" (`[R-CNF-02]`), independent
of any reader. F6 applies → **no**.

(c) F6's own text: "the obligation binds a reader holding those bytes resident,
and a reader that would have to fetch them MAY defer or omit the check
(`[R-CNT-04]`); **a verifier holds no such exemption (§2.3)**." Appendix H
repeats it. The verifier establishes the violation → **nonconforming**.

(d) The condition is F6 ("The 16-byte front signature block is not
byte-identical to the constant", instance "reserved bytes [8,16)"), not F1 —
F1's condition is a *byte-reversed* signature constant, which this is not.
F6's Governing rule cell holds a single identifier and §21.1 says "A Governing
rule cell names that requirement first" → **`[R-CNT-04]`**.

**Answer: (a) no; (b) no; (c) nonconforming; (d) [R-CNT-04].**

---

## Underdetermination summary

I found no question the document leaves genuinely open. The nearest miss is
Q02(ii), where §18.2's flat "no smaller than §21.9's user-metadata guarantee"
could be read as disqualifying R categorically rather than instance-wise;
`[R-ERR-04]`'s explicit pairing of "a reader MAY decline" an over-guarantee file
against "declines on that ground a file whose every quantity lies within the
table" resolves it, and I recorded the competing reading above rather than
suppressing it. Confidence there is medium; everywhere else the decisive
sentence is quoted.
