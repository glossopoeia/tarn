# Cleanroom round 32 — quiz answerer transcript

Sole source read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4754 lines, 287,719 bytes), read in full via the Read tool in four chunks
(lines 1–700, 700–1500, 1500–2300, 2300–3100, 3100–3700, 3700–4260, 4259–4459).
No other file was opened. No directory listing, no git, no web.

Scratch directory (mine alone):
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-round/scratch/quiz-answerer/`
Files written there: `qa_crc32c.py`, `qa_arith.py`.

CRC implementation validated against three constants the document itself states,
before any answer relied on it:
- CRC-32C(`"123456789"`) = 0xE3069283 (§4.5) — reproduced.
- Appendix A's trailer CRC 0x402F157E over that file's trailer bytes [0,60) — reproduced.
- CRC-32C of a full all-sentinel segment = 0xEECB3BB2 (§15.4) — reproduced.

---

## Q01 — planar `sst` layer record offsets and derived values

Field order is §7.4's table. Widths: name = u8 len + bytes; layout u8;
linearization u16; codec u16; filter u16; A u64; S u64; A_slab u64; rank u8;
C u16; each dimension entry = name + u64 extent + u64 tile extent; each channel
entry = name + u16 type + u8 fill len + fill bytes; then index_encoding u8,
entry_count u64, crc_of_crc_array u32.

Cross-checked against §7.4's own worked example, whose annotated offsets
(name 0, layout 4, linearization 5, codec 7, filter 9, A 11, S 19, A_slab 27,
rank 35, C 36, dim 38, channel 56, index_encoding 68, entry_count 69,
crc 77, total 81) match this packing exactly.

Running offset:
- name `sst` 1+3 = 4 → [0,4)
- layout 1 → 4; linearization 2 → 5; codec 2 → 7; filter 2 → 9
- A 8 → 11; S 8 → 19; A_slab 8 → 27
- rank 1 → 35; C 2 → 36; end of fixed head at 38
- dim `y` 1+1+8+8 = 18 → [38,56); dim `x` 18 → [56,74)
- channel `a` uint16: 1+1+2+1+2 = 7 → [74,81)
- channel `b` float32: 1+1+2+1+4 = 9 → [81,90)
- **index_encoding at offset 90**

inline_length = 90 + 1 + 8 + 4 = **103** (no sub-records; §7.4 "sub-records …
to the end of the inline payload", §7.2 framing, none here).

Geometry: G_y = ⌈4/2⌉ = 2, G_x = ⌈6/3⌉ = 2, N = 4 (§11.2). Planar →
addressed-tile count = C·N = 2·4 = **8** = entry_count (`[R-CNT-17]`).

extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 = 160 + 4 = **164**
(`[R-CNT-17]`).

Decisive: "Under index_encoding 1, extent_length MUST equal entry_count × 20 +
⌈entry_count / 2¹⁶⌉ × 4".

**Answer: 90, 103, 8, 164**

---

## Q02 — packed planar bool tile images

Planar bool → §14.3 packing: "value k occupies bit k mod 8 of byte k div 8
(§4.4), with 0 = false and 1 = true, and the decoded size is ⌈P/8⌉ bytes."
§4.4: bit 0 is the LSB.

G = (⌈3/2⌉, ⌈3/4⌉) = (2, 1); N = 2; P = 2·4 = 8; decoded size = ⌈8/8⌉ = 1 byte;
P mod 8 = 0 so there are no pad bits.

In-tile ordinal (§11.4) = u₀·T₁ + u₁ = 4u₀ + u₁.

§14.5 fixes padding content: "at every padding position, a writer MUST encode …
the fill bit in a packed plane." Fill byte 0x01 = true → fill bit 1.
A position is padding where its coordinate along an axis is ≥ that axis's
extent (§11.3). E = (3,3).

Tile (0,0): x₀ ∈ {0,1}, x₁ ∈ {0,1,2,3}.
| ord | (u₀,u₁) | coord | real? | bit |
|---|---|---|---|---|
|0|(0,0)|(0,0)|real|0|
|1|(0,1)|(0,1)|real|0|
|2|(0,2)|(0,2)|real|0|
|3|(0,3)|(0,3)|pad (x₁=3≥3)|1|
|4|(1,0)|(1,0)|real|0|
|5|(1,1)|(1,1)|real|0|
|6|(1,2)|(1,2)|real|0|
|7|(1,3)|(1,3)|pad|1|
Byte 0 = bits 3,7 set = 0b1000_1000 = **0x88**.

Tile (1,0): x₀ ∈ {2,3}, x₁ ∈ {0,1,2,3}. x₀ = 3 ≥ 3 is padding.
ords 0,1,2 real (coords (2,0),(2,1),(2,2)) → 0; ord 3 pad → 1;
ords 4–7 all have x₀ = 3 → pad → 1.
Byte 0 = bits 3,4,5,6,7 = 0b1111_1000 = **0xF8**.

Both tiles stored under codec 1 / filter 1, so the stored bytes are the decoded
image verbatim and each entry's length is 1 (`[R-COD-04]`) — consistent.

**Answer: 88, F8**

---

## Q03 — trailer CRC bytes

Trailer bytes [0,60) built from §6.2's layout table:
```
8a 4e 52 41 54 0d 0a 1a  01 00  00 00  00 00 00 00
10 00 00 00 00 00 00 00  44 00 00 00 00 00 00 00
c0 00 00 00 00 00 00 00  ef be ad de 00 00 00 00
00 ×12
```
CRC-32C = 0x092F02D6, stored little-endian (`[R-ENC-09]`: "stored as a
little-endian `u32`"), i.e. bytes `d6 02 2f 09` at trailer offset 60.

Sanity: dir_offset 16 ≥ 16, dir_length 68 ≥ 4, 16+68 = 84 ≤ 192−64 = 128,
F = 192 is a multiple of 64, file_id ≠ 0 — a self-consistent live trailer,
though the CRC does not depend on that.

**Answer: d6 02 2f 09**

---

## Q04 — interleaved decoded size and channel offset

§14.2: interleaved decoded size = P · Q, offset of value k =
(k div C)·Q + F_{k mod C}; "channel c's value at in-tile ordinal u sits at byte
u · Q + Fᶜ".

P = 3·4·5 = 60. B = (bool 1, float64 8, int16 2) → Q = 11. Decoded size =
60·11 = **660**.

In-tile ordinal of (2,1,3) = Σ uᵢ·∏_{j>i} Tⱼ = 2·(4·5) + 1·5 + 3 = 48.
F_c for channel index 2 = 1 + 8 = 9.
Offset = 48·11 + 9 = **537**.

**Answer: 660, 537**

---

## Q05 — planar disk ordinal, entry offset, segment, extent_length

G = (⌈5000/50⌉, ⌈4000/40⌉) = (100, 100); N = 10,000.
t = (2475 div 50, 1234 div 40) = (49, 30).
s = t₀·G₁ + t₁ = 49·100 + 30 = 4930 (`[R-GEO-06]`, linearization 1).
Planar disk ordinal = c·N + s = 7·10,000 + 4930 = **74,930**.

§15.1: "The entry for the tile with disk ordinal k is the k-th entry, at region
byte 20·k" → 20 · 74,930 = **1,498,600**.

§15.4: "Segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count))" →
74,930 div 65,536 = **1**.

entry_count = C·N = 80,000; extent_length = 80,000·20 + ⌈80,000/65,536⌉·4 =
1,600,000 + 8 = **1,600,008**.

**Answer: 74930, 1498600, 1, 1600008**

---

## Q06 — codec-1 entry lengths in a mixed planar layer

G = (⌈25/10⌉, ⌈7/10⌉) = (3, 1); N = 3; C = 2 → entry_count = 6; P = 100.

`[R-COD-04]`: "A **non-sentinel** index entry's length therefore MUST equal the
tile's decoded size."

Disk ordinal 1: c = 1 div N = 0 → channel `m` (bool). Planar bool plane packs
(§14.3): decoded size ⌈100/8⌉ = **13**.

Disk ordinal 4: c = 4 div 3 = 1 → channel `v` (uint8). Planar numeric (§14.2):
P·Bᶜ = 100·1 = **100**.

extent_length = 6·20 + ⌈6/65536⌉·4 = 120 + 4 = **124**.

**Answer: 13, 100, 124**

---

## Q07 — slack total and its completeness

Claimants of the coverage walk (§9.7, `[R-LIF-08]`; §5.2 `[R-CNT-02]`):
- front signature block [0,16) — 16 bytes
- entry 0's stored extent [16,316) — 300 bytes
- the layer record's extent = the tile-index region [800,844) — 44 bytes
  (44 = 2·20 + 4, matching `[R-CNT-17]` for entry_count = 2)
- the directory [900,960) — 60 bytes
- the live trailer [960,1024) — 64 bytes
Sum = 484. Slack = 1024 − 484 = **540**.

Entry 1 (offset = S, length = S, crc = 5 ≠ 0) is §15.3's row
"offset = S ∧ length = S ∧ crc ≠ 0 | *structural*: reject-tile" (register row
T6). §9.7 settles its effect on the walk: "An entry `[R-IDX-03]` classifies
reject-tile on a *structural* ground does not make the walk incomplete: the
walk passes over it, and the bytes it nominally addresses fall to slack."
The verifier does not elect to stop at the first violation, no layer was
declined on resource grounds, and no scope-level rejection ended an
enumeration — so the walk is complete and §5.2's partial-total clause does not
engage. §5.2: "a verifier that reaches a live state MUST report the total
number of slack bytes."

**Answer: 540, total**

---

## Q08 — entry_count against geometry

Rank 1, extent 100, tile extent 32 → G₀ = ⌈100/32⌉ = 4, N = 4. Planar with
C = 3 → addressed-tile count = C·N = 12 (§11.2). Declared entry_count = 4 ≠ 12.

The extent_length check is *satisfied*: 4·20 + ⌈4/65536⌉·4 = 84, which is what
the slot declares — so L22 is not the row. The violated row is L21,
"entry_count does not equal the geometry-derived addressed-tile count
(N interleaved, C·N planar)", Detector *reader*, Detected *layer access*,
governing rule `[R-CNT-17]`. §21.3's heading fixes the outcome: "Outcome:
reject-layer".

**Answer: L21, reject-layer, reader, layer access**

---

## Q09 — a file declaring format major 3

§21.2's preamble derives the reach set: "Deriving it there yields F8, F14, F6
and both of F1's instances — each asserting an invariant `[R-CNT-24]` fixes in
every major — and no other row." Here the trailer magic is exact (F8, F1's
trailer instance clear), the trailer CRC verifies (F14 clear), and the front
16 bytes are byte-identical to the constant, with the reader holding them
resident (F6, F1's front instance clear).

The two defects present — 12 nonzero bytes at trailer offset 48, and
dir_length = 2 — restate F15 and F16, neither of which reaches. §2.3's Note
says so of F15 expressly: "F15 does not reach although its Governing rule cell
cites `[R-CNT-24]`: the trailer bytes it requires be zero are inside the 48
that rule lets a future major redefine." F16 is simply not in the reach set,
and §2.3: "Every other condition … is not assessed against a file declaring
another major, no violation of it is established there, and no §21 row
restating it records such a file." → **0 rows**.

Reader's refusal: §6.3 — "A reader MUST reject-file when version_major is 0
(invalid) or is a major it does not implement" — `[R-CNT-07]`. §2.3 confirms
"a reader refuses such a file on capability grounds (§6.3, `[R-CNT-07]`)".

Verifier's verdict: §2.3 lists *cannot establish* as owed "where some
requirement is one it is unable to check on a capability or resource ground,
as when the file names a format major version it does not implement". No
violation was established (every reaching condition passes), and *cannot
establish* "is available only to a traversal that established no violation".

**Answer: 0, [R-CNT-07], cannot establish**

---

## Q10 — user-metadata frame content size 4096 vs a 4097-byte document

§18.2: "The frame's content-size field, unlike the decoded size and the window,
is *not* left to the reader: it MAY be present, and when present it MUST equal
the byte length of the decoded document. A mismatch is one of the frame
constraints R4 registers, not a failure to decode under R3."

R4's instance list names exactly this: "the content-size field declared smaller
than the decoded length, top-level extent". R4's Detector is *reader* and its
Detected cell is *extent use*. §21.5's heading fixes the outcome:
"Outcome: ignore-record".

Certification: §21.5 — "Every row here is a violation all the same: the outcome
bounds a reader's blast radius and never makes the file conforming." §2.3 —
"a verifier that has established any violation reports *nonconforming*". So no.

**Answer: R4, ignore-record, extent use, no**

---

## Q11 — an interleaved bool byte of 0x7F at a real position

`[R-SER-08]`: "A reader that does not reject the tile and returns the value …
MUST return 0x00 as false and every other byte as true — the value, encoded
0x00 or 0x01 as above, and not the stored byte." 0x7F ≠ 0x00 → true → the
returned byte is **0x01**.

Row: T2 — "In an interleaved tile, a bool channel's single value byte at a real
(non-padding) sample position is neither 0x00 nor 0x01". The coordinate lies
inside the extents, so it is a real position, not T4's padding case.
T2's Detector is **verifier**.

Conformance: `[R-SER-08]` — "Writers MUST NOT emit any byte other than 0x00 or
0x01 as an interleaved bool value. Any other byte makes the file
nonconforming." → **no**.

**Answer: 01, T2, verifier, no**

---

## Q12 — what one commit may do to a layer that stored a tile

§20.3 step 4 is the closed list: "A layer that stores a tile **in the generation
this commit supersedes** keeps its declarations, with these exceptions and no
other: its name, and its dimension and channel names, MAY change; an extent MAY
grow, and MUST NOT shrink; a planar layer's channel list MAY be extended at its
end, or shortened from its end; and a slab or alignment declaration MAY be
declared, re-established or cleared … A commit MAY make several of these
changes at once."

And the fixed side: "the layout, the linearization and the index encoding, the
codec and the filter, the rank and the dimension order, every tile extent,
every channel's type and fill, an interleaved layer's channel list, and the
position of every planar channel but the last."

(a) grow E₀ 100→200 — an extent MAY grow → **yes**
(b) shrink E₁ 50→40 — "MUST NOT shrink" → **no**
(c) filter 2→1 — the filter is fixed → **no**
(d) clear the slab declaration (S 8→0, A_slab 4096→0) plus a name change — both
    permitted, and several at once are permitted; clearing is the alternative
    `[R-SLB-04]` names → **yes**
(e) remove `g` from (r,g,b) leaving (r,b) — shortening is licensed only "from
    its end"; "the position of every planar channel but the last" is fixed →
    **no**
(f) append `a` at the end plus grow E₀ — both permitted, several at once → **yes**

**Answer: yes, no, no, yes, no, yes**

---

## Q13 — grow E₀ and shorten the planar channel list in one commit

Superseded generation: G₀ = ⌈21/10⌉ = 3, N = 3, C = 4 → entry_count = C·N =
**12**.
New generation: G₀ = ⌈60/10⌉ = 6, N = 6, C = 2 → entry_count = **12**.

New disk ordinal of channel `c1` at spatial ordinal 0 = c·N + s = 1·6 + 0 = **6**
(`[R-GEO-06]`).

Re-emission: `[R-WRT-04]` step 4 — "Every layer whose stored-tile set or index
content this commit changes has its tile-index region re-emitted in full —
entry_count entries plus the segment CRC array — necessarily at a new placement
(`[R-LIF-01]`) … (a growth renumbers ordinals wherever `[R-GEO-06]` moves them
…)". Both antecedents hold: the stored-tile set changes (c2's and c3's tiles
leave the addressed set; c0 gains three unstored tiles at s = 3,4,5), and the
index content changes (old ordinals 3–5 held c1's stored tiles, new ordinals
3–5 hold c0's new tiles; c1's tiles move to ordinals 6–8). → **yes**.

*Oddity worth flagging.* Two non-normative passages generalise in a way this
case falsifies: §13.3's Note ("… which, among the declaration changes §20.3
permits a layer that stores a tile, only a change to entry_count does") and
§11.1's Rationale ("Growth that leaves **entry_count** unchanged touches the
directory alone"). Here entry_count is unchanged at 12 because the growth and
the shortening cancel, yet the index content plainly changes. §2.1 makes both
passages non-normative ("All text in this document is normative except: … any
text labeled *Note*, *Example*, or *Rationale*"), so `[R-WRT-04]`'s own
condition governs and the answer is yes.

**Answer: 12, 12, 6, yes**

---

## Q14 — lz4 on a layer that addresses no tile

Geometry: G = (⌈0/16384⌉, ⌈1000/16384⌉) = (0, 1); N = 0. Interleaved →
addressed-tile count = N = 0, so entry_count = 0, extent slot (0,0),
crc_of_crc_array = 0 — all consistent with `[R-CNT-17]` and `[R-CNT-23]`.
P = 16384² = 268,435,456; Q = 8; P·Q = 2,147,483,648 = 2³¹ ≤ 2⁶³ − 1, so
`[R-ENC-04]` is satisfied.

(1) `[R-COD-07]` bars codec 4 "for a layer any of whose addressed tiles'
decoded size exceeds 0x7E000000 bytes". This layer addresses none, so the cap
is vacuously satisfied; §17.2's Note confirms the reading — "a layer that
addresses none — any dimension extent 0 — satisfies it whatever its tile shape
declares, and codec 4 is conforming there." → **yes**, conforming.

(2) L44 restates that same cap, so no file exhibiting no addressed tile is
recorded against it → **no**.

(3) §21.9: "*Decoded size of one tile* ranges over a layer's **addressed**
tiles, stored or not … A layer addressing no tile (§11.2) therefore has no tile
whose decoded size the table bounds." So this file has no instance of that
quantity at all, and every quantity it does have lies within the table.
`[R-ERR-04]`: "Software that declines **on that ground** a file whose every
quantity lies within the table is not a conforming reader (`[R-CNF-03]`)."
→ **no**.

**Answer: yes, no, no**

---

## Q15 — compaction

**Scenario A.** Entry 3 has offset = S with length = 40 ≠ S → §15.3 row
"offset = S ∧ length ≠ S, or offset ≠ S ∧ length = S | *structural*:
reject-tile". §20.5: "An entry §15.3 classifies reject-tile on a structural
ground is neither … so regenerating the region cannot proceed without meeting
it, and the violation is thereafter one the compactor has detected.
`[R-WRT-06]` then obliges refusal: the compactor can neither reproduce the
entry nor invent a replacement, and no drop is available, a tile-index entry
being no record §20.4's table licenses dropping." → one word: **refuse**.

**Scenario B.** `[R-WRT-07]`: the compactor "regenerates each tile-index region
any of whose stored extents the output relocates (entry offsets new; entry
lengths, entry crcs, and sentinel entries unchanged; segment CRCs recomputed
over the entries as re-emitted), and updates the layer-record fields covering a
regenerated region (crc_of_crc_array)". Also "every stored tile's bytes
verbatim — each index entry's crc is unchanged". Geometry is untouched, so
entry_count is carried forward with the record's other declaration fields.

- (i) stored tile's entry crc — unchanged → **included**
- (ii) offset — "entry offsets new" → excluded
- (iii) length — "entry lengths … unchanged" → **included**
- (iv) the sentinel entry's 20 bytes — "sentinel entries unchanged"; "a
  sentinel is re-emitted unchanged" → **included**
- (v) entry_count — not among the fields the regeneration updates; the layer's
  geometry and channel list are preserved → **included**
- (vi) crc_of_crc_array — expressly the field the regeneration "updates", the
  segment CRCs having been recomputed over re-pointed entries → excluded

**Answer: refuse; i, iii, iv, v**

---

## Notes on what was *not* determined by the document

None of the fifteen questions turned out to be underdetermined on my reading.
The two closest calls, both resolved by the normative/non-normative split of
§2.1, are recorded above at Q13 (the §13.3 Note and §11.1 Rationale generalise
falsely about entry_count) and at Q14 (§17.2's Note, which merely restates the
vacuous quantification `[R-COD-07]` already carries).
