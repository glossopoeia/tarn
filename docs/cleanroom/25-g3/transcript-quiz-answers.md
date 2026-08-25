# Cleanroom round 25 — quiz answerer transcript

## Access disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(found at the path the brief named). Read it whole, in five chunks, via the
Read tool plus one `wc`/`grep -n '^#'` for the section index. No other file in
the repository was read, listed, or grepped. No git history, no web access, no
conformance vectors, no ADRs, no registry.json.

Local computation only: a Python CRC-32C implementation I wrote in the
scratchpad, reading no project files. I validated it against four constants the
specification itself publishes before using it for any answer:

- CRC-32C("123456789") = 0xE3069283 (§4.5 check vector) — reproduced
- CRC-32C(zero bytes) = 0x00000000 (§4.5) — reproduced
- CRC-32C of 80 bytes of four sentinel entries = 0x80A34955 (§7.4 example) — reproduced
- CRC-32C of that 4-byte array = 0xC4EE982E (§7.4 example) — reproduced
- CRC-32C of a full 2^16-sentinel segment = 0xEECB3BB2 (§15.4, `[R-IDX-05]`) — reproduced
- Appendix A trailer CRC = 0xE00938D2 — reproduced

Unrequested context: my runtime placed a project instruction pointer
(CLAUDE.md → AGENTS.md) and an index of maintainer memory files in context
before I began. I did not open any of them and did not use their contents. I
note their appearance here as the brief requires.

---

## Q01 — trailer CRC of a generation-3 layer-less file

Layout forced by the givens:

- [0,16) front block (§6.1)
- directory at dir_offset = 16, record sequence empty, so dir_length = 4 holding
  CRC-32C(zero bytes) = 0x00000000 (§7.1; Appendix A's [16,20) row).
- `[R-LIF-02]` step 5: "append the pad to the next 64-byte boundary". Directory
  ends at 20; next 64-boundary is 64. Pad = [20,64), 44 bytes.
- trailer [64,128); F = committed_file_length = 128, a multiple of 64 (§6.2).

Trailer bytes [0,60), per §6.2's layout table:

```
 0  8A 4E 52 41 54 0D 0A 1A   magic
 8  01 00                     version_major = 1
10  00 00                     version_minor = 0
12  00 00 00 00               flags = 0
16  03 00 00 00 00 00 00 00   generation = 3
24  10 00 00 00 00 00 00 00   dir_offset = 16
32  04 00 00 00 00 00 00 00   dir_length = 4
40  80 00 00 00 00 00 00 00   committed_file_length = 128
48  88 77 66 55 44 33 22 11   file_id = 0x1122334455667788
56  00 00 00 00               reserved
```

Offset 60 is "trailer CRC | structural | CRC-32C over trailer bytes [0, 60)".
Computed: 0xF33C1F65, stored little-endian (`[R-ENC-09]`).

**Answer: `65 1f 3c f3`.** Confidence high.

---

## Q02 — planar packed bool edge tile

Geometry: G_y = ceil(3/2) = 2, G_x = ceil(3/4) = 1 (§11.2). N = 2. P = T_y·T_x = 2·4 = 8.

Tile (1,0) covers y in [2,4), x in [0,4). In-tile ordinal = u_y·T_x + u_x
(`[R-GEO-06]`, row-major, last-declared dimension fastest).

| ord | (u_y,u_x) | (y,x) | status | value |
|---|---|---|---|---|
| 0 | (0,0) | (2,0) | real | true |
| 1 | (0,1) | (2,1) | real | **false** |
| 2 | (0,2) | (2,2) | real | true |
| 3 | (0,3) | (2,3) | padding (x ≥ 3) | fill = true |
| 4–7 | (1,·) | (3,·) | padding (y ≥ 3) | fill = true |

Planar bool → §14.3: "value k occupies bit k mod 8 of byte k div 8 … decoded
size is ⌈P/8⌉ bytes" = 1 byte. `[R-SER-05]`: padding positions encode the
channel's fill — fill byte 0x01 = true.

bits 0..7 = 1,0,1,1,1,1,1,1 → 0b11111101 = 0xFD. P mod 8 = 0, so no pad bits.

(b) codec 1 + filter 1 → stored bytes are the decoded image verbatim;
`[R-COD-04]`: "The index entry's length therefore MUST equal the tile's decoded
size" → 1.

(c) `[R-IDX-01]`: crc = "CRC-32C of the stored tile's bytes". CRC-32C(FD) =
0x1E3B70F7 → stored `f7 70 3b 1e`.

**Answer: (a) `fd`; (b) 1; (c) `f7 70 3b 1e`.** Confidence high.

---

## Q03 — interleaved tile under byte-shuffle

C = 2, B_a = 1, B_b = 2, Q = 3 (§14.2). P = 2. Decoded size = P·Q = 6.

`[R-SER-01]` interleaved: value k = channel (k mod C) at in-tile ordinal k div C.
k=0 → a@0 = 11; k=1 → b@0 = 0x2233 → `33 22` (LE); k=2 → a@1 = 44;
k=3 → b@1 = 0x5566 → `66 55`.

Decoded image: `11 33 22 44 66 55`.

`[R-COD-10]`: interleaved stride s = Q = 3; n = L/s = 2. "the filtered image
places byte i of group j at offset i · n + j".
Groups: g0 = 11 33 22, g1 = 44 66 55.
offset 0 = g0[0] = 11; 1 = g1[0] = 44; 2 = g0[1] = 33; 3 = g1[1] = 66;
4 = g0[2] = 22; 5 = g1[2] = 55.

(I checked my transform direction against §17.3's own worked example — three
float32s 1.0/2.0/3.0 shuffling to `00 00 00 00 00 00 80 00 40 3F 40 40` — and it
reproduces it exactly.)

Codec 1 → stored bytes = filtered image = `11 44 33 66 22 55`.
CRC-32C of those = 0x38EB4FC5 → `c5 4f eb 38`.

**Answer: (a) `11 44 33 66 22 55`; (b) `c5 4f eb 38`.** Confidence high.

---

## Q04 — layer record sizes

(a) inline_length, packed in §7.4 table order with no padding (`[R-CNT-18]`):

```
name          1 + 2  =  3
layout        1
linearization 2
codec         2
filter        2
A             8
S             8
A_slab        8
rank d        1
C             2         (the nine scalars = 34)
dim y      1+1+8+8 = 18
dim x               = 18
chan p  1+1 + 2 + 1+2 =  7   (int16, element size 2 → fill length 2)
chan q  1+1 + 2 + 1+1 =  6   (bool, element size 1 → fill length 1)
index_encoding 1
entry_count    8
crc_of_crc_array 4       (trailing fixed = 13)
```

3 + 34 + 36 + 13 + 13 = **99**. (Cross-checked against §7.4's own worked
example, which sums 4 + 34 + 18 + 12 + 13 = 81 by the same accounting.)

(b) G_y = G_x = ceil(10/4) = 3, N = 9. Layout 2 = planar, so the addressed-tile
count is C·N (§11.2, `[R-GEO-03]`) = 2·9 = **18**, which `[R-CNT-17]` obliges
entry_count to equal.

(c) `[R-CNT-17]`: extent_length = entry_count × 20 + ⌈entry_count/2^16⌉ × 4 =
360 + 4 = **364**.

(A = 0 with S = 4 is fine — `[R-CNT-16]` bars only A ≠ 0 *and* S ≠ 0.)

**Answer: (a) 99; (b) 18; (c) 364.** Confidence high.

---

## Q05 — planar ordinals at scale

G = (⌈100/4⌉, ⌈200/8⌉, ⌈300/16⌉) = (25, 25, 19). N = 25·25·19 = 11,875.

(a) planar → entry_count = C·N = 6 · 11,875 = **71,250**.

(b) 71,250 × 20 = 1,425,000; ⌈71250/65536⌉ = 2 → + 8 = **1,425,008**.

(c) t = (99 div 4, 199 div 8, 299 div 16) = (24, 24, 18).
s = Σ t_i · ∏_{j>i} G_j = 24·(25·19) + 24·19 + 18 = 11,400 + 456 + 18 = 11,874.
Disk ordinal = c·N + s (`[R-GEO-06]`, channel-major) = 5·11,875 + 11,874 = **71,249**.

(d) `[R-IDX-01]`: "The entry for the tile with disk ordinal k is the k-th entry,
at region byte 20·k" → 20 × 71,249 = **1,424,980**.

**Answer: (a) 71250; (b) 1425008; (c) 71249; (d) 1424980.** Confidence high.

---

## Q06 — interleaved stride arithmetic

P = 3·5 = 15. B = (2, 1, 8) → Q = 11.

(a) §14.2 table, interleaved decoded size = P·Q = **165**.
(b) in-tile ordinal = u_0·T_1 + u_1 = 2·5 + 3 = **13**.
(c) "channel c's value at in-tile ordinal u sits at byte u · Q + F^c";
F_c = B_a + B_b = 3 → 13·11 + 3 = **146**.
(d) planar bool → §14.3 packing, ⌈P/8⌉ = ⌈15/8⌉ = **2**.

**Answer: (a) 165; (b) 13; (c) 146; (d) 2.** Confidence high.

---

## Q07 — zero-extent layer with huge tile extents

E_0 = 0 → G_0 = 0 → N = 0 → interleaved addressed-tile count 0. entry_count 0,
extent (0,0), crc_of_crc_array 0 all consistent (`[R-CNT-17]`, `[R-CNT-23]`).

The lz4 cap does *not* fire: §17.2's Note — "a layer that addresses none — any
dimension extent 0 … — satisfies it whatever its tile shape declares, and codec
4 is conforming there."

But the same Note continues: "`[R-ENC-04]`'s overflow rule carries no such
quantifier — it binds any sum or product a file yields — so P·Q and P·B^c are
checked in an empty layer even though this cap is not."

P = ∏T_i = 2097152^3 = (2^21)^3 = 2^63 = 9,223,372,036,854,775,808, which
exceeds 2^63 − 1 by exactly one. `[R-GEO-03]`: "a reader MUST treat a product
exceeding 2^63 − 1 as a validity error at layer scope." §19.3 places that check
at first access to the layer.

Register: L2, "A declaration-derived sum or product of a layer exceeds 2^63 - 1
although every contributing field is in domain", whose instance list names
"P = ∏Tᵢ" explicitly. Detector reader, detected at layer access, outcome
reject-layer.

**Answer: (a) reject-layer; (b) L2.** Confidence high.

---

## Q08 — fill change on a layer with pad bits

Geometry: G = ⌈10/5⌉ = 2, N = 2, planar C = 1 → 2 addressed tiles, both stored
in generation 3. P = 5. Planar bool → decoded size ⌈5/8⌉ = 1 byte, values in
bits 0–4, and since P mod 8 = 5 ≠ 0 the plane has **pad bits** at positions 5–7
(§14.3).

E = 10 = G·T = 10, so there are no *padding positions*. Pad bits are the
distinct mechanism (§14.3's Note), and `[R-SER-05]` fixes their content:
"Every pad bit (§14.3) MUST carry the plane's channel's fill bit."

Changing fill 0x00 → 0x01 changes what the stored byte of each of the two
stored tiles must contain. §20.3 step 4: "A commit MUST NOT change a layer's
declarations in a way that alters, for any tile that layer stores **in the
generation this commit supersedes**, what §14 fixes for its stored bytes or how
they decode". §20.3's shape-(c) example says exactly this: a fill change is a
directory-only edit only "on a layer with no padding position and no pad bit",
and "A fill change on a layer that **stores** a tile carrying either is not an
appender's operation at all (step 4)".

**Answer: (a) barred; (b) `[R-SER-05]`.** Confidence high.

---

## Q09 — zstd metadata frame declaring the wrong content size

Everything structural passes: extent CRC verifies, encoding 2 is assigned,
inline_length 1, extent slot well-formed. The frame satisfies every carried-over
`[R-COD-06]` constraint the question enumerates. The decoded document satisfies
every `[R-MTA-04]` restriction and `[R-MTA-05]`'s ordering.

The one defect: §18.2 — "The frame's content-size field … MAY be present, and
when present it MUST equal the byte length of the decoded document." Declared
100 against a 120-byte document.

Routing: "A mismatch is one of the frame constraints R4 registers, not a failure
to decode under R3: the bytes decode, and what is wrong is what the header said
about them." R4's instance list carries "the content-size field declared smaller
than the decoded length, top-level extent".

(a) §21.5 header: "Outcome: ignore-record"; `[R-MTA-09]`'s closing sentence —
"Any violation here is ignore-record".
(b) R4.
(c) The verifier implements zstd, so no capability decline arises; it
establishes the violation. §2.3: "An established violation takes priority: a
verifier that has established any violation reports *nonconforming*." §21.5 also
insists "Every row here is a violation all the same: the outcome bounds a
reader's blast radius and never makes the file conforming."

**Answer: (a) ignore-record; (b) R4; (c) nonconforming.** Confidence high.

---

## Q10 — slab packing across a structurally-bad entry

Interleaved → one block [0, 8) (`[R-SLB-02]`). S = 4 → run 0 = ordinals [0,4),
run 1 = [4,8).

Transparency classification (`[R-SLB-03]`, §15.3):
- ordinal 1: sentinel → transparent.
- ordinal 5: offset = S, length = 0 ≠ S → §15.3 row "offset = S ∧ length ≠ S,
  or offset ≠ S ∧ length = S | *structural*: reject-tile" → transparent
  ("So are the entries §15.3 classifies reject-tile on a *structural* ground").
- ordinal 6: only defect is that its stored bytes fail its crc → **not**
  transparent. `[R-SLB-03]`: "An entry whose only defect is that its stored
  bytes fail its crc is not transparent — its offset and length stand, and the
  packing relation reads them as it does any other stored tile's."

Run 0: first stored is ordinal 0 at 1024; 1024 mod 64 = 0 ✓. Then
1024 + 40 = 1064 = ordinal 2's offset ✓; 1064 + 16 = 1080 = ordinal 3's ✓.

Run 1: first stored is ordinal 4 at 2048; 2048 mod 64 = 0 ✓. Ordinal 5 skipped.
Ordinal 6 must sit at 2048 + 50 = 2098 ✓. Ordinal 7 must sit at
2098 + 30 = **2128**.

(b) Any other X breaks "each stored tile's offset equals the previous stored
tile's offset plus its length", which is L41 — detector verifier, outcome
reject-layer (also §15.3's row "alignment or slab invariant violated (§16) |
*verifier*: reject-layer").

**Answer: (a) 2128; (b) reject-layer.** Confidence high.

---

## Q11 — slack total

Claimants of the live committed state (§5.2 `[R-CNT-02]`, walked per §9.7
`[R-LIF-08]`, which claims the front block and the live trailer as members):

| claimant | range | bytes |
|---|---|---|
| front signature block | [0, 16) | 16 |
| stored-tile extent (entry: offset 16, length 100) | [16, 116) | 100 |
| user-metadata record extent | [116, 124) | 8 |
| layer record extent = tile-index region | [128, 152) | 24 |
| directory region | [152, 352) | 200 |
| live trailer | [384, 448) | 64 |

The index region's length checks out: `[R-CNT-17]`, entry_count 1 →
1×20 + 1×4 = 24. The record headers and inline payloads are *not* separate
claimants — "A record is not a claimant of its own — its header and inline
payload lie inside the directory region, which is the claimant covering them".
Nor is the index region a second claimant beside the layer record's extent.

Sum = 412. Unreached bytes = [124, 128) (4) + [352, 384) (32, the pre-trailer
pad) = 36. The walk completes and no scope is rejected, so the total is exact,
not partial (`[R-CNT-21]`).

**Answer: 36.** Confidence high.

---

## Q12 — compactor output trailer

(a) `[R-WRT-06]`: "It MUST mint a fresh file_id for the output … and
generation 1: a compacted file is a whole-file rewrite under a new file_id by
definition". → **1**.

(b) flags 0x00030000 sets bits 16 and 17 — both in the ignore lane (§6.3: bits
16–31). This text defines no flag bits at all, so a compactor implementing
nothing beyond it treats both as unknown. `[R-WRT-06]`: "The output trailer MUST
copy the input's unknown ignore-lane flag bits forward, in place of the flags = 0
§6.3 requires of a file created under this text." `[R-CNT-08]` says the same. No
incompat bit is set, so nothing bars the compaction.

**Answer: (a) 1; (b) `00030000`.** Confidence high.

---

## Q13 — nonzero front-block reserved bytes

(a) §6.1's table fixes bytes [8,16) to "zero" and "Writers MUST emit exactly
these 16 bytes." F6 registers the condition with instance "reserved bytes
[8,16)". A file-conformance violation → **no**.

(b) "a verifier certifies only violation-free files" (`[R-CNF-12]`), and F6's
condition text is explicit that "a verifier holds no such exemption (§2.3)".
Appendix H's verifier checklist repeats it: the front block by byte equality,
"which `[R-CNT-04]` lets a reader not holding it resident defer or omit and §2.3
does not (F1, F6)". → **no**.

(c) `[R-CNT-04]`: "A reader that would have to issue a further range request to
obtain those bytes MAY defer or omit the check … The test is residency, not
transport." A [16,128) window leaves [0,16) non-resident. Appendix A describes
this exact reader: "A shorter window can still spare the second request: 112
bytes covering [16, 128) contains the directory … while bytes [0, 16) stay
non-resident, so §6.1 leaves the front-block check to the reader." → **yes**.

**Answer: (a) no; (b) no; (c) yes.** Confidence high.

---

## Q14 — three shrinks

Layer: interleaved, one uint8 channel, Q = 1, T = 4, P = 4, decoded size 4.
Live: G = ⌈8/4⌉ = 2, tiles 0 and 1 both stored.
Tile 1's image `05 06 00 00` maps byte u to coordinate 4+u.

Governing text, §20.3 step 4 and its shrink paragraph: a shrink "is permitted
exactly where it alters nothing §14 fixes for any tile the layer stores in the
generation this commit supersedes", with the carve-out that "a new padding
position whose stored byte already holds the fill `[R-SER-05]` fixes is not one".

(a) 8 → 6: G = ⌈6/4⌉ = 2, both tiles still addressed. Coordinates 6 and 7 become
padding. Their stored bytes are `00 00`, which is exactly the recorded fill
0x00. Decoded size, sample offsets, codec and filter all unchanged. The
carve-out applies → **permitted**.

(b) 8 → 5: G = ⌈5/4⌉ = 2, both tiles still addressed. Coordinates 5, 6, 7 become
padding. Coordinate 5's stored byte is 0x06 ≠ fill 0x00, so the commit would
falsify `[R-SER-05]` for a tile stored in the superseded generation →
**barred**. (Unstoring it in the same commit would not rescue it: "the
quantifier is the superseded generation's".)

(c) 8 → 4: G = ⌈4/4⌉ = 1, N = 1. Tile 1 leaves the addressed set — "Dropping a
tile out of the addressed set (§11.2's grid count falls) is not itself such an
alteration — a tile the new state does not address carries no §14 obligation and
its extent becomes slack." Tile 0 covers coordinates 0–3, all still real, with no
padding position and no change to size, offsets, codec or filter →
**permitted**. `[R-CNT-17]` obliges the smaller entry_count and a re-emitted
index region, which the question grants.

**Answer: (a) permitted; (b) barred; (c) permitted.** Confidence high.

---

## Q15 — experimental-range MU = 1 record

Type 0x8123 ≥ 0x8000 → experimental range (§10.2's record-type row). MU = 1 with
PE = 1 is a legal combination; inline_length 0 and extent (0,0) are legal.

(a) §21.6: "an **experimental-range top-level record type carrying MU = 1** …
`[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]` makes the file
conforming all the same … since the prohibition on publishing experimental
values binds a writer's conduct and not the bytes." → **yes**.

(b) `[R-CNT-15]`: "An unknown record type at file scope: MU = 1 → reject-file."
→ **reject-file**.

(c) `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer, and
where the file is otherwise conforming a reader MUST NOT reject the file for
it." §21.6 makes the same point: "the same type as a layer sub-record is
reject-layer and never a ground to refuse the file". → **reject-layer**.

**Answer: (a) yes; (b) reject-file; (c) reject-layer.** Confidence high.

---

## Underdetermined count

Zero questions on this slate came out underdetermined. I looked specifically for
ambiguity at Q07 (whether the lz4 cap or the overflow rule fires — §17.2's Note
settles it, and both land on layer scope anyway), Q09(c) (whether *cannot
establish* could apply — §2.3's priority clause settles it), Q10 (the treatment
of the crc-failing entry — `[R-SLB-03]` names it explicitly), and Q14(a) (whether
a new padding position is itself an alteration — §20.3's carve-out names it).
Each had text that decided it outright, so I did not flag any.
