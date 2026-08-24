# Round 23 — quiz answerer working transcript

## Disclosure

Files read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` only, via
`sed -n`/`grep` on that path. No ADRs, no `docs/`, no `conformance/`, no
`registry.json`, no git history, no web.

Local computation run (reads no project files): a Python CRC-32C implementation
(Castagnoli, reflected, init 0xFFFFFFFF, final XOR), self-checked against the
spec's own check vector (`"123456789"` → 0xE3069283, empty → 0x00000000), against
`[R-IDX-05]`'s 0xEECB3BB2 all-sentinel-segment constant, and against §7.4's
worked example (0x80A34955 / 0xC4EE982E). One Python script parsed the §21.5
register table rows out of the spec text to count semicolon-separated instance
cells mechanically.

Unrequested context that appeared before I began: a project-instruction pointer
(CLAUDE.md → AGENTS.md) and an index of the maintainer's memory files with
one-line descriptions. I did not open any of them and did not use their content;
naming that they appeared, not their contents, per the brief.

---

## Q01 — encoding-2 document, content-size 1048576, decodes to 1048570

Record is top-level user metadata, inline payload = 0x02 → encoding 2 (zstd),
`[R-MTA-03]`. Every carried-over `[R-COD-06]` frame constraint is satisfied
(magic, dict ID 0, no content-checksum, one non-skippable frame filling the
extent before the terminal CRC, terminal CRC verifies). The decoded document is
a legal JSON object with sorted members, so `[R-MTA-04]` and `[R-MTA-05]` are
clean.

The one defect: Frame_Content_Size is present and declares 1048576, while the
decoded document is 1048570 bytes. §18.2 `[R-MTA-09]`:

> "The frame's content-size field, unlike the decoded size and the window, is
> *not* left to the reader: it MAY be present, and when present it MUST equal
> the byte length of the decoded document. A mismatch is one of the frame
> constraints R4 registers, not a failure to decode under R3: the bytes decode,
> and what is wrong is what the header said about them."

R4's own cell confirms: "the content-size field breaks its constraint exactly
when it is present and does not equal the decoded document's byte length", with
instances "the content-size field declared larger than the decoded length,
top-level extent" — exactly this file (1048576 > 1048570).

R4 sits in §21.5, whose outcome is **ignore-record**, and whose preamble says
"Every row here is a violation all the same: the outcome bounds a reader's blast
radius and never makes the file conforming (`[R-CNF-12]`)".

(a) R4 · (b) ignore-record · (c) nonconforming.

## Q02 — Single_Segment_Flag, FCS 12582912, decodes to 12582912

Content-size equals the decoded document's length, so R4's content-size
instance does not fire. Every other frame constraint holds. Document rules hold.

Window: §18.2 states the frame's declared `Window_Size` is *not* constrained by
the file —

> "The frame's declared `Window_Size` is unconstrained here for the same reason,
> and takes the same treatment: a reader's window bound is its own, no smaller
> than §21.9's guarantee for that quantity, and a frame declaring more than the
> reader admits is ignore-record on that ground — the reader's capability, not a
> failure to decode within the meaning of R3, and no violation: the file exceeds
> a §21.9 guarantee and so remains conforming while the reader MAY decline it
> (`[R-ERR-04]`)."

So (a) **conforming**.

Which §21.9 minimum-guarantee row does it exceed? With Single_Segment_Flag set
there is no Window_Descriptor and RFC 8878 makes Window_Size the content-size
field — §18.2 spells this out: "a document larger than that guarantee, framed
that way, exceeds a §21.9 row … §21.9's user-metadata row bounds a document's
decoded size; it does not relieve the frame carrying it of the `Window_Size`
row." Window_Size = 12582912 = 12 MiB > 8 MiB guarantee → exceeded.
Document decoded size 12 MiB ≤ 16 MiB guarantee → that row not exceeded.
No tiles, no other frames, so no other per-instance row has an instance.

(b) the row named **zstd frame `Window_Size`**.

## Q03 — declined document + reserved flag bit on an unregistered top-level type

(ii) is a violation the verifier establishes: `[R-CNT-12]` — "a verifier MUST
treat a nonzero reserved flag bit … as a validity error at the record's
governing scope" — registered as **F26** ("Any of a non-layer top-level
record's reserved flag bits 2-15 is set", detector verifier, certification).
Whether the unregistered type is reserved-range (F36, also a violation) or
experimental (§21.6 non-violation) does not matter: F26 fires either way.

§2.3: "An established violation takes priority: a verifier that has established
any violation reports *nonconforming*, however many requirements it was unable
to check, and *cannot establish* is available only to a traversal that
established no violation."

(a) **nonconforming**.

(b) §2.3 again: "A verifier MUST report each requirement it was unable to check
on a capability or resource ground, naming the requirement and the ground,
**whichever of the three verdicts it reports**; that per-requirement report
constrains the report and not the verdict." And `[R-MTA-09]`: "The decline is
one of the unchecked requirements `[R-CNF-11]` obliges the verifier to report".
The window bound (16 MiB frame vs. the verifier's 8 MiB, the stated minimum) is
that actor's capability, and §18.2 gives window and size bounds "the same
treatment". So the report obligation stands despite the nonconforming verdict.

(b) **yes**.

## Q04 — encoding byte 0x00 / 0x7F / 0x80

§10.2's metadata-encoding space: assigned 1, 2; reserved 3–0x7F; experimental
≥ 0x80; "Value 0 is invalid in every space above."

- 0x00 → R1 ("declares a document encoding of 0"). §21.5's preamble and R1's own
  note: "Encoding 0 and a reserved-range value are unassigned too, and R1
  registers both as violations". → nonconforming.
- 0x7F → reserved range 3–0x7F → R1 → nonconforming.
- 0x80 → experimental. §21.6: "A user-metadata record declares an
  experimental-range (≥ 0x80) document encoding | Ignored (ignore-record); **the
  file is conforming** — §10.3's prohibition binds a writer's conduct, not the
  bytes." → conforming.

**nonconforming, nonconforming, conforming**.

## Q05 — instance counting

§21.1: "Instances within a cell are separated by semicolons, and a cell reading
— is one instance; the count is therefore mechanical once the cell is written."
Also: "a row whose check ranges over a family without the condition changing
shape states that range as a single instance (T24's *any codec*)."

Mechanical split on ';' of the Instances cells (script output):

    R1 4 · R2 2 · R3 2 · R4 16 · R5 8 · R6 4 · R7 6 · R8 2 · R9 2 · R10 2

R4 = 16: {missing magic, skippable frame, second frame, nonzero dict ID,
content-checksum flag, bytes remaining after the frame, content-size larger,
content-size smaller} × {top-level extent, layer sub-record extent} = 8 × 2.

Sum R1..R10 = 4+2+2+16+8+4+6+2+2+2 = **48**.

(a) 16 · (b) 48.

## Q06 — zero-extent dimension with an lz4 declaration over a huge tile

Grid: G_y = ⌈0/16384⌉ = 0, G_x = ⌈4096/16384⌉ = 1 (`[R-GEO-03]`). N = 0.
Interleaved ⇒ addressed-tile count = N = 0, so entry_count = 0 ✓
(`[R-CNT-17]`), extent slot (0, 0) ✓, crc_of_crc_array = 0 ✓ (`[R-CNT-23]`).
`[R-GEO-02]`: "A dimension with extent 0 is valid: its grid count is 0, the
layer has zero addressed tiles … Readers MUST accept such a layer".

Codec 4's cap: P = 16384·16384 = 268,435,456; Q = 8 (one float64); P·Q =
2,147,483,648 > 0x7E000000 = 2,113,929,216. But §17.2's note on `[R-COD-07]`:

> "The cap is quantified over the layer's *addressed* tiles, so a layer that
> addresses none — any dimension extent 0 (`[R-GEO-02]`, §21.6) — satisfies it
> whatever its tile shape declares, and codec 4 is conforming there."

`[R-ENC-04]`'s ceiling is unquantified and is still checked: P·Q = 2^31 and
N·P = 0 are both far below 2⁶³ − 1. So (a) **conforming**.

(b) §21.9: "*Decoded size of one tile* ranges over a layer's **addressed** tiles
… A layer addressing no tile (§11.2) therefore has no tile whose decoded size
the table bounds." No user-metadata document, no zstd frame; d = 2 ≤ 32,
C = 1 ≤ 4096, entry_count 0 ≤ 2³², one layer, tiny directory. So every quantity
lies within the table, and `[R-ERR-04]`: "Software that declines **on that
ground** a file whose every quantity lies within the table is not a conforming
reader (`[R-CNF-03]`)". → (b) **no**.

## Q07 — codec 3 → codec 1 declaration change

§21.7 `[R-ERR-01]`: "a change that reaches the codec is witnessed by the rows
for the codec now declared, which test the stored bytes as a stream of it (T15,
T17, T23, T25), **or by T14 where the new declaration is codec 1**".

Answer: **T14**.

## Q08 — planar bool tile, byte-shuffle, codec none

P = T_y·T_x = 2·5 = 10. Planar bool ⇒ packed plane, decoded size ⌈10/8⌉ = 2
(`[R-SER-03]`). Tile (0,0) covers y∈{0,1}, x∈{0..4}; extents are 3 and 3, so
x = 3, 4 are padding positions (`[R-GEO-04]`), whose content is fixed to the
fill bit by `[R-SER-05]` (fill 0x01 = true), as are the pad bits.

In-tile ordinal k = u_y·T_x + u_x = u_y·5 + u_x (`[R-GEO-06]`, row-major,
permanent):

    k0 (0,0) true    k1 (0,1) false   k2 (0,2) true
    k3 (0,3) PAD=1   k4 (0,4) PAD=1
    k5 (1,0) false   k6 (1,1) true    k7 (1,2) false
    k8 (1,3) PAD=1   k9 (1,4) PAD=1

LSB-first packing, bit k mod 8 of byte k div 8:
byte0 bits[0..7] = 1,0,1,1,1,0,1,0 → 1+4+8+16+64 = 93 = 0x5D
byte1 bits[0..1] = 1,1 → 0x03; pad bits 2–7 carry the fill bit 1 → 0xFC;
byte1 = 0xFF.

Filter 2 on a packed bool plane: `[R-COD-10]` — "for a packed boolean plane
s = 1 and the filter is the identity". Codec 1: stored bytes are the filtered
image verbatim, length = decoded size = 2 (`[R-COD-04]`).

Stored bytes: **5d ff**.

## Q09 — interleaved, three channels, ordinal 15 of tile (1,1)

B_m = 1 (bool interleaved is one byte, §14.2), B_v = 8, B_q = 2.
Q = 11. F_m = 0, F_v = 1, F_q = 1+8 = 9. P = 4·4 = 16; decoded size P·Q = 176.

(a) `[R-SER-02]`: channel c's value at in-tile ordinal u sits at u·Q + F_c
= 15·11 + 9 = 165 + 9 = **174**. (Sample 15 occupies [165, 176).)

(b) Ordinal 15 → (u_y, u_x) = (3, 3) → real coordinates (y, x) = (4+3, 4+3) =
(7, 7). Extents are 5 and 5, so both axes are out of extent: this is a padding
position. `[R-SER-05]`: "at every padding position, a writer MUST encode, for
each channel the position carries, that channel's fill value". Sample-major, in
declared channel order:

    m: 01
    v: 00 00 00 00 00 00 f8 3f
    q: cd ab

→ **01 00 00 00 00 00 00 f8 3f cd ab** (11 bytes).

## Q10 — 131072 all-sentinel entries

(a) `[R-CNT-17]`: extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4
= 131072 × 20 + 2 × 4 = 2,621,440 + 8 = **2,621,448**.

(b) Two full segments of exactly 2¹⁶ sentinel entries. `[R-IDX-05]`: "The
CRC-32C of a segment consisting of 2¹⁶ sentinel entries is `0xEECB3BB2`" —
reproduced by my implementation over 65536 × (FF×16 00×4). Segment CRC array =
`b2 3b cb ee b2 3b cb ee` (each u32 little-endian, `[R-ENC-09]`).
crc_of_crc_array = CRC-32C of those 8 bytes = 0xD7926B78, stored little-endian:

**78 6b 92 d7**

(Implementation validated against the spec's own check vector and against
§7.4's worked example, which it reproduces exactly.)

## Q11 — 200-byte transport, trailer sitting at [64, 128)

`[R-CNT-10]`/§19.1 step 1: F is the transport-authoritative size = 200. §6.2:
"The trailer occupies the final 64 bytes of the file" — bytes [136, 200), which
are all 0x00. §19.1 step 2 fetches [F−64, F) and validates in §6.2's fixed
order; `[R-LIF-05]` forbids scanning backward to the trailer at [64, 128).

§6.2: "A reader MUST validate, in order: the trailer magic; the trailer CRC;
the version gate …". The first check is the magic, and 00×8 ≠
`8A 4E 52 41 54 0D 0A 1A`. That is **F8** — "The 8 bytes at F-64 are not exactly
the trailer magic 8A 4E 52 41 54 0D 0A 1A", detector reader, at open, governed
by `[R-CNT-06]`, outcome reject-file. (Not F1: the bytes are zeros, not a
byte-reversed constant. Not F5: 200 ≥ 128. Not F17: it never reaches that gate.)

(a) **reject-file** · (b) **F8**.

## Q12 — slab run continuity across a structural entry and a bad-CRC entry

S = 4, interleaved ⇒ single block [0, 8), runs [0, 4) and [4, 8) (`[R-SLB-02]`).
First run = ordinals 0–3.

- Entry 0: offset 8192, length 300, crc good → first stored tile;
  8192 mod 4096 = 0, so `[R-SLB-03]`'s alignment holds.
- Entry 1: offset = length = 0xFFFF_FFFF_FFFF_FFFF with crc = 5 → §15.3 row
  "offset = S ∧ length = S ∧ crc ≠ 0 | *structural*: reject-tile" (T6).
  `[R-SLB-03]`: "So are the entries §15.3 classifies reject-tile on a
  *structural* ground: they address no usable extent, and the run's stored tiles
  close over them." Transparent.
- Entry 2: length 100, crc mismatching its bytes → `[R-SLB-03]`: "An entry whose
  only defect is that its stored bytes fail its crc is **not** transparent — its
  offset and length stand, and the packing relation reads them as it does any
  other stored tile's." So X = 8192 + 300 = **8492**.
- Entry 3: length 60 → Y = 8492 + 100 = **8592**.

## Q13 — slack total

Claimants of the live committed state (`[R-CNT-02]`, `[R-LIF-08]`):

    front block   [0, 16)        16
    stored tile A [16, 116)     100   (non-sentinel, crc verifies)
    A's index     [128, 152)     24   (1×20 + 4 = 24 ✓ [R-CNT-17])
    B's index     [160, 204)     44   (2×20 + 4 = 44 ✓)
    user-md ext   [256, 320)     64
    directory     [384, 896)    512
    live trailer  [960, 1024)    64
                               ----
                                824

Layer B's entry 1 is the sentinel pattern with crc = 5 → structural reject-tile,
and §15.3/`[R-LIF-08]`: it "contributes … none to `[R-LIF-08]`'s coverage walk,
so any bytes it nominally addressed that no other claimant claims fall to
slack." Entry 0 is a valid sentinel — no extent either.

Slack = F − claimed = 1024 − 824 = **200**.

Partial or complete? §9.7 `[R-LIF-08]`: "An entry `[R-IDX-03]` classifies
reject-tile on a *structural* ground **does not make the walk incomplete**: the
walk passes over it, and the bytes it nominally addresses fall to slack (§15.3)."
No layer-scope rejection blocks enumeration, and the verifier does not stop
early. So the walk completes → **complete**.

(The file is nonconforming — T6 is an established violation — but §5.2 obliges
the slack total from any verifier that reaches a live state, and the
partial/complete distinction turns on walk completeness, not on the verdict.)

## Q14 — layer record sizes

Inline payload (packed, table order, §7.4; method validated against §7.4's
81-byte worked example, which this arithmetic reproduces):

    name          1 + 4                        =  5
    layout u8                                     1
    linearization u16                             2
    codec u16                                     2
    filter u16                                    2
    A u64                                         8
    S u64                                         8
    A_slab u64                                    8
    rank u8                                       1
    C u16                                         2      (subtotal 39)
    dim y   1+1 + 8 + 8                        = 18
    dim x   1+1 + 8 + 8                        = 18      (36)
    chan r  1+1 + 2 + 1+1  (uint8,  size 1)    =  6
    chan g  1+1 + 2 + 1+2  (uint16, size 2)    =  7
    chan b  1+1 + 2 + 1+4  (float32,size 4)    =  9      (22)
    index_encoding u8                             1
    entry_count u64                               8
    crc_of_crc_array u32                          4      (13)

39 + 36 + 22 + 13 = **110**, no sub-records, no residue.

Geometry: G_y = ⌈10/4⌉ = 3, G_x = ⌈10/4⌉ = 3, N = 9. Planar ⇒ addressed-tile
count = C·N = 27 = entry_count (`[R-GEO-03]`, `[R-CNT-17]`).
extent_length = 27 × 20 + ⌈27/2¹⁶⌉ × 4 = 540 + 4 = **544**.

## Q15 — two layer records with identical ill-formed name fields

Both L3 ("A layer record's name bytes are not well-formed UTF-8", reject-layer,
reader, open) and F4 ("Two layer records in the live directory carry
byte-identical name fields, both obtainable within their records'
inline_length", reject-file, reader, open) are exhibited.

§19.1 step 4 fixes the order:

> "Uniqueness is decided first, and over the raw name bytes whether or not each
> name is itself well-formed — `[R-ENC-13]` makes name comparison a byte
> comparison, which needs no valid name — so two layers whose name fields are
> byte-identical are a duplicate even when neither name is valid."

`[R-ENC-15]`: a duplicate layer name is a file-scope error → reject-file.

(a) **reject-file** · (b) **F4**.
