# Round 25 — quiz keyer transcript

## Access disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(present at the path the brief named). Read it in full, sequentially, via
`sed -n` ranges. No other file in the repository was read, listed, or grepped;
no ADRs, no conformance corpus, no registry.json, no git history, no web.

Local computation only: three Python scripts I authored in my own scratchpad
(`work.py`, `work2.py`, `work3.py`), reading no repository files.

**Toolchain validation.** Before using my CRC-32C implementation for any
answer I checked it against every constant the document itself publishes:

| Constant | §  | Expected | Computed |
|---|---|---|---|
| CRC-32C("123456789") | §4.5 | 0xE3069283 | 0xE3069283 |
| CRC-32C(zero bytes) | §4.5 | 0x00000000 | 0x00000000 |
| Appendix A trailer CRC | App. A | 0xE00938D2 | 0xE00938D2 |
| 4-sentinel segment CRC | §7.4 example | 0x80A34955 | 0x80A34955 |
| crc_of_crc_array of that | §7.4 example | 0xC4EE982E | 0xC4EE982E |
| full all-sentinel segment | §15.4 | 0xEECB3BB2 | 0xEECB3BB2 |

Byte-shuffle implementation checked against §17.3's worked example
(`00 00 80 3F 00 00 00 40 00 00 40 40` → `00 00 00 00 00 00 80 00 40 3F 40 40`): match.

**Unrequested context.** My runtime placed a project instruction file and an
index of maintainer memory notes in context before I began. I did not open any
file they named and did not use their content. Reported in `disclosure`.

---

## Q01 — trailer CRC bytes

Layout forced by the stem: front block [0,16); directory region at 16 with an
empty record sequence, so 4 bytes holding CRC-32C of zero bytes = 0x00000000,
[16,20); §9.2 step 5 pads to the next 64-byte boundary → pad [20,64);
trailer [64,128). F = 128, a multiple of 64 (§6.2). dir_offset = 16,
dir_length = 4, dir_offset+dir_length = 20 ≤ F−64 = 64. ✓

Trailer bytes [0,60) per §6.2's layout table:

```
8a 4e 52 41 54 0d 0a 1a   magic
01 00                     version_major = 1
00 00                     version_minor = 0
00 00 00 00               flags = 0
03 00 00 00 00 00 00 00   generation = 3
10 00 00 00 00 00 00 00   dir_offset = 16
04 00 00 00 00 00 00 00   dir_length = 4
80 00 00 00 00 00 00 00   committed_file_length = 128
88 77 66 55 44 33 22 11   file_id = 0x1122334455667788 (LE)
00 00 00 00               reserved
```

CRC-32C = 0xF33C1F65, stored little-endian (§4.5) at offset 60.

**Answer: `65 1f 3c f3`**

Method cross-check: substituting generation 1 / file_id 0x0123456789ABCDEF into
the same builder reproduces Appendix A's 0xE00938D2 exactly.

---

## Q02 — planar bool edge tile

G_y = ⌈3/2⌉ = 2, G_x = ⌈3/4⌉ = 1 (§11.2). N = 2, P = T_y·T_x = 2·4 = 8.
Planar bool ⇒ §14.3 packed plane, decoded size ⌈P/8⌉ = 1 byte.

Tile (1,0) covers y ∈ [2,4), x ∈ [0,4). In-tile ordinal = u_y·T_x + u_x (§11.4).

| ord | (u_y,u_x) | (y,x) | class | bit |
|---|---|---|---|---|
| 0 | (0,0) | (2,0) | real | 1 |
| 1 | (0,1) | (2,1) | real | 0 (the one false sample) |
| 2 | (0,2) | (2,2) | real | 1 |
| 3 | (0,3) | (2,3) | padding (x ≥ 3) | 1 (fill bit, `[R-SER-05]`) |
| 4–7 | (1,·) | (3,·) | padding (y ≥ 3) | 1 each |

LSB-first packing (§14.3): bits 0..7 = 1,0,1,1,1,1,1,1 → 0xFD.
P mod 8 = 0, so there are no pad bits.

(a) `fd`
(b) codec 1 + filter 1 ⇒ stored bytes = decoded image; `[R-COD-04]` forces
    length = decoded size = **1**
(c) CRC-32C(`FD`) = 0x1E3B70F7 → stored `f7 70 3b 1e`

---

## Q03 — interleaved byte-shuffle

P = 2, C = 2, Q = 1+2 = 3, decoded size P·Q = 6 (§14.2).
Value sequence (§14.1): value k = channel (k mod C) at ordinal k div C.
k=0 a[0]=0x11; k=1 b[0]=0x2233; k=2 a[1]=0x44; k=3 b[1]=0x5566.
Decoded image = `11 33 22 44 66 55`.

Filter 2, interleaved ⇒ stride s = Q = 3 (§17.3). L = 6, n = L/s = 2.
Byte i of group j goes to offset i·n + j:

```
group0 = 11 33 22 ; group1 = 44 66 55
offsets: 0←11, 1←44, 2←33, 3←66, 4←22, 5←55
```

Codec 1 ⇒ stored = filtered image.

(a) `11 44 33 66 22 55`
(b) CRC-32C of those stored bytes = 0x38EB4FC5 → `c5 4f eb 38`
    (§8.1: the entry's crc covers "the tile's stored bytes", i.e. post-filter,
    post-codec, as stored.)

---

## Q04 — inline_length, entry_count, extent_length

§7.4 field order, packed with no padding:

| field | bytes | run |
|---|---|---|
| name `ab` (1+2) | 3 | 3 |
| layout u8 | 1 | 4 |
| linearization u16 | 2 | 6 |
| codec u16 | 2 | 8 |
| filter u16 | 2 | 10 |
| A u64 | 8 | 18 |
| S u64 | 8 | 26 |
| A_slab u64 | 8 | 34 |
| rank u8 | 1 | 35 |
| C u16 | 2 | 37 |
| 2 dim entries (1+1+8+8 each) | 36 | 73 |
| chan `p` int16 (1+1+2+1+2) | 7 | 80 |
| chan `q` bool (1+1+2+1+1) | 6 | 86 |
| index_encoding u8 | 1 | 87 |
| entry_count u64 | 8 | 95 |
| crc_of_crc_array u32 | 4 | 99 |

Structure validated against §7.4's own 81-byte worked example
(4 + 34 + 18 + 12 + 13 = 81): my per-field widths reproduce it.

(a) **99**
(b) G = (⌈10/4⌉, ⌈10/4⌉) = (3,3), N = 9; planar ⇒ addressed-tile count C·N
    = 2·9 = **18** (§11.2)
(c) `[R-CNT-17]`: 18×20 + ⌈18/2¹⁶⌉×4 = 360 + 4 = **364**

(A = 0 with S = 4 is fine — `[R-CNT-16]` bars only A ≠ 0 *and* S ≠ 0.)

---

## Q05 — planar geometry, ordinals, entry offset

G = (⌈100/4⌉, ⌈200/8⌉, ⌈300/16⌉) = (25, 25, 19). N = 25·25·19 = 11,875.

(a) planar ⇒ entry_count = C·N = 6 · 11,875 = **71,250**
(b) 71,250×20 + ⌈71,250/65,536⌉×4 = 1,425,000 + 2·4 = **1,425,008**
(c) tile coords = (99 div 4, 199 div 8, 299 div 16) = (24, 24, 18).
    s = Σ tᵢ·∏_{j>i} Gⱼ = 24·(25·19) + 24·19 + 18 = 11,400 + 456 + 18 = 11,874.
    disk ordinal = c·N + s = 5·11,875 + 11,874 = **71,249**
    (= entry_count − 1, as the maximal coordinate on the maximal channel should be)
(d) entry k lies at region byte 20·k (§15.1) → 20 · 71,249 = **1,424,980**

---

## Q06 — interleaved offsets

P = 3·5 = 15; Q = 2 + 1 + 8 = 11 (bool counts 1 in interleaved arithmetic, §14.2).

(a) P·Q = **165**
(b) in-tile ordinal = u₀·T₁ + u₁ = 2·5 + 3 = **13**
(c) channel `c` has index 2, F₂ = B_a + B_b = 2 + 1 = 3;
    offset = u·Q + Fᶜ = 13·11 + 3 = **146**
(d) planar bool ⇒ §14.3 packed: ⌈P/8⌉ = ⌈15/8⌉ = **2**

---

## Q07 — empty layer with overflowing P

E₀ = 0 ⇒ G₀ = 0 ⇒ N = 0, so the layer addresses no tile; entry_count 0,
extent slot (0,0) and crc_of_crc_array 0 are all consistent (`[R-CNT-17]`,
`[R-CNT-23]`). L44 (the lz4 0x7E000000 cap) does **not** fire — §17.2's note:
the cap "is quantified over the layer's *addressed* tiles, so a layer that
addresses none … satisfies it whatever its tile shape declares".

But the same note continues: "`[R-ENC-04]`'s overflow rule carries no such
quantifier — it binds any sum or product a file yields — so P·Q and P·Bᶜ are
checked in an empty layer even though this cap is not."

P = ∏Tᵢ = 2,097,152³ = (2²¹)³ = 2⁶³ = 9,223,372,036,854,775,808,
which exceeds 2⁶³ − 1 = 9,223,372,036,854,775,807 by exactly 1.
(P·Q = P·1 is the same value.)

`[R-ENC-04]`: a derived product above 2⁶³ − 1 is a validity error at the
owning scope; §11.2 `[R-GEO-03]` makes that scope the layer.

(a) **reject-layer** (b) **L2** — whose Instances cell names `P = ∏Tᵢ` and
`P·Q` explicitly, detector reader, detected at layer access.

---

## Q08 — fill change against stored pad bits

G = ⌈10/5⌉ = 2, P = T = 5. Planar bool ⇒ packed plane, decoded size
⌈5/8⌉ = 1 byte. G·T = 10 = E, so there are **no padding positions** — but
P mod 8 = 5 ≠ 0, so bit positions 5–7 of the single byte **are pad bits**
(§14.3), and `[R-SER-05]` fixes them: "Every pad bit (§14.3) MUST carry the
plane's channel's fill bit."

Both tiles are stored in the superseded generation and carried forward with
pad bits = 0 (fill 0x00). Setting fill to 0x01 makes the required pad bit 1,
so the carried-forward bytes would be falsified (T5 would fire on them).

§20.3 step 4's bar is decided by effect, not by its illustrative list — "The
test is the effect on such a tile, and the list names where that effect arises
rather than standing on its own" — and §20.3's example (c) states this case in
terms: "changing a channel's fill value on a layer with no padding position and
no pad bit… A fill change on a layer that **stores** a tile carrying either is
not an appender's operation at all (step 4)."

(a) **barred** (b) **[R-SER-05]**

---

## Q09 — zstd Frame_Content_Size mismatch

Everything structural passes: encoding byte 2 is assigned, extent CRC verifies,
the frame is a single dictionary-free checksum-free RFC 8878 frame with no
trailing bytes, and the decoded document satisfies every §18.2 content rule
including `[R-MTA-05]`'s sort order. The only defect: FCS declares 100, the
decoded document is 120 bytes.

§18.2: "The frame's content-size field … MAY be present, and when present it
MUST equal the byte length of the decoded document. A mismatch is one of the
frame constraints R4 registers, not a failure to decode under R3: the bytes
decode, and what is wrong is what the header said about them."

Quarantine (`[R-CNT-25]`) fixes the reader outcome regardless of scope.
R4's instance list carries "the content-size field declared smaller than the
decoded length, top-level extent" verbatim.

§21.5 preamble: "Every row here is a violation all the same: the outcome bounds
a reader's blast radius and never makes the file conforming." The verifier
implements zstd, the 120-byte document is far inside §21.9's 16 MiB guarantee,
so nothing is declined and the violation is *established*. §2.3: "An established
violation takes priority."

(a) **ignore-record** (b) **R4** (c) **nonconforming**

---

## Q10 — slab packing

Interleaved ⇒ one block [0, N) = [0,8) (§16.2 `[R-SLB-02]`). S = 4 ⇒
run 0 = ordinals [0,4), run 1 = ordinals [4,8).

Entry classification (§15.3):
- 1 = valid sentinel → transparent to run continuity
- 5 = offset S with length 0 ≠ S → *structural* reject-tile → **transparent**
- 6 = well-formed entry whose stored bytes fail its crc → **not** transparent;
  "its offset and length stand, and the packing relation reads them as it does
  any other stored tile's"

Run 0: first stored = ordinal 0 at 1024; 1024 mod 64 = 0 ✓.
  1024 + 40 = 1064 = ordinal 2's offset ✓; 1064 + 16 = 1080 = ordinal 3's ✓.
Run 1: first stored = ordinal 4 at 2048; 2048 mod 64 = 0 ✓.
  Ordinal 5 transparent. 2048 + 50 = 2098 = ordinal 6's offset ✓.
  Ordinal 6 participates ⇒ ordinal 7's offset must be 2098 + 30 = **2128**.

(a) **2128**
(b) `[R-SLB-03]` — "A verifier MUST check these invariants (violation:
    reject-layer, §15.3)"; rows L41/L42 → **reject-layer**

*Noted caveat (question scope, not document ambiguity).* The stem's uniqueness
claim holds over values of X that leave entry 7 well-formed. Were X in 0–15 the
entry would be *structural* reject-tile under §15.3 and become transparent to
run continuity, so the slab invariants would hold vacuously and the recorded
outcome would be reject-tile, not reject-layer. Entry 7 is presented in parallel
with the other stored entries, so I answer on the well-formed reading; 2128 is
the answer under every reading in which entry 7 is a stored tile.

---

## Q11 — slack total

Claimants of the live committed state (§5.2 `[R-CNT-02]`, §9.7 `[R-LIF-08]`):

| claimant | range | bytes |
|---|---|---|
| front signature block | [0, 16) | 16 |
| stored tile (entry offset 16, length 100) | [16, 116) | 100 |
| user-metadata record extent | [116, 124) | 8 |
| layer record extent = tile-index region | [128, 152) | 24 |
| directory region | [152, 352) | 200 |
| live trailer | [384, 448) | 64 |
| | **total** | **412** |

The two records are *not* claimants of their own headers/payloads — those lie
inside the directory region, "which is the claimant covering them" (§9.7).
Index cross-check: entry_count 1 under index_encoding 1 ⇒ extent_length
1×20 + 1×4 = 24 ✓ matches the declared slot.

Slack = F − claimed = 448 − 412 = **36** — the gap [124,128) = 4 plus the
pre-trailer pad [352,384) = 32. The walk completes and no scope is rejected,
so this is a full total, not a partial one (`[R-CNT-21]`).

**Answer: 36**

---

## Q12 — compactor output trailer

(a) `[R-WRT-06]`: a compactor "MUST mint a fresh file_id for the output …
    and generation 1". → **1**
(b) flags 0x00030000 sets bits 16 and 17 — both in the ignore lane (§6.3), both
    unknown to a compactor implementing no flag bit. `[R-CNT-08]`: "A compactor,
    though its output is a new file, carries the input's unknown ignore-lane
    bits into its output trailer rather than writing flags = 0"; `[R-WRT-06]`
    repeats it as a MUST. Incompat lane is empty and stays empty.
    → **`00030000`**

(version_minor is a separate SHOULD and is not asked.)

---

## Q13 — corrupted front-block reserved bytes

§6.1's table fixes bytes [8,16) as zero and "Writers MUST emit exactly these 16
bytes". Register row F6 covers exactly this: "The 16-byte front signature block
is not byte-identical to the constant", instance "reserved bytes [8,16)".

(a) File conformance is "a pure predicate on bytes" (`[R-CNF-02]`) and this byte
    sequence violates a file-level requirement → **no**.
(b) F6's row: "a verifier holds no such exemption (§2.3)"; §2.3 has a verifier
    check every file-level requirement and forbids certifying a violating file
    → **no**.
(c) `[R-CNT-04]`: "A reader that would have to issue a further range request to
    obtain those bytes MAY defer or omit the check." The window [16,128) leaves
    [0,16) non-resident, so no obligation attaches; §19.2 scopes the open-tier
    duty to "a reader whose open leaves it resident". Appendix A states this
    exact scenario: "112 bytes covering [16, 128) contains the directory … while
    bytes [0, 16) stay non-resident, so §6.1 leaves the front-block check to the
    reader." The file is nonconforming, so no acceptance duty is breached either.
    → **yes**

---

## Q14 — three shrinks

Layer: E = 8, T = 4, G = 2, N = 2, interleaved, one uint8 channel, fill 0x00,
Q = 1, decoded size P·Q = 4. Tile 0 = `01 02 03 04` (coords 0–3),
tile 1 = `05 06 00 00` (coords 4–7). Both stored in the superseded generation.

§20.3: "a shrink is permitted exactly where it alters nothing §14 fixes for any
tile the layer stores in the generation this commit supersedes."

(a) **E = 6.** G = ⌈6/4⌉ = 2, both tiles still addressed. Tile 1's ordinals 2,3
    (coords 6,7) become padding positions; their stored bytes are `00 00`, which
    already equal the fill. The bar's own carve-out: "a new padding position
    whose stored byte already holds the fill `[R-SER-05]` fixes is not one, so a
    shrink producing only those is permitted here exactly as it is there."
    Decoded size, sample offsets, codec and filter are unchanged. → **permitted**

(b) **E = 5.** G = 2, both tiles addressed. Tile 1's ordinals 1,2,3 (coords
    5,6,7) become padding; the stored byte at ordinal 1 is 0x06 ≠ fill 0x00.
    That alters what `[R-SER-05]` fixes for a tile stored in the superseded
    generation. → **barred**

(c) **E = 4.** G = ⌈4/4⌉ = 1, N = 1: tile 1 leaves the addressed set entirely.
    "Dropping a tile out of the addressed set (§11.2's grid count falls) is not
    itself such an alteration — a tile the new state does not address carries no
    §14 obligation and its extent becomes slack." Tile 0 covers coords 0–3, all
    real, byte-identical obligations. `[R-CNT-17]` obliges the smaller
    entry_count and a re-emitted index region, which the stem grants.
    → **permitted**

---

## Q15 — experimental MU = 1 record

Type 0x8123 ≥ 0x8000 ⇒ experimental range (§10.2). MU = 1, PE = 1 — not the
prohibited MU=1/PE=0 combination. Extent slot (0,0) = "no extent", valid.
inline_length 0 is unconstrained for an unassigned type (payload opaque,
`[R-CNT-15]`).

(a) §21.6: "an **experimental-range top-level record type carrying MU = 1**
    (§10.2, §10.3): `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]`
    makes the file conforming all the same." §10.3's publishing prohibition
    "binds the writer's conduct, not the bytes". → **yes**
(b) `[R-CNT-15]`: "An unknown record type at file scope: MU = 1 → reject-file."
    → **reject-file**
(c) `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer, and
    where the file is otherwise conforming a reader MUST NOT reject the file for
    it". §21.6 confirms the qualifier is load-bearing: "the same type as a layer
    sub-record is reject-layer and never a ground to refuse the file".
    → **reject-layer**

---

## Summary

| Q | Answer |
|---|---|
| 01 | `65 1f 3c f3` |
| 02 | (a) `fd` (b) 1 (c) `f7 70 3b 1e` |
| 03 | (a) `11 44 33 66 22 55` (b) `c5 4f eb 38` |
| 04 | (a) 99 (b) 18 (c) 364 |
| 05 | (a) 71250 (b) 1425008 (c) 71249 (d) 1424980 |
| 06 | (a) 165 (b) 13 (c) 146 (d) 2 |
| 07 | (a) reject-layer (b) L2 |
| 08 | (a) barred (b) [R-SER-05] |
| 09 | (a) ignore-record (b) R4 (c) nonconforming |
| 10 | (a) 2128 (b) reject-layer |
| 11 | 36 |
| 12 | (a) 1 (b) `00030000` |
| 13 | (a) no (b) no (c) yes |
| 14 | (a) permitted (b) barred (c) permitted |
| 15 | (a) yes (b) reject-file (c) reject-layer |

No question came out underdetermined. Q10 carries a question-scope caveat
(recorded above), not a gap in the document.
