# Round 24 — quiz keyer transcript

## Access disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(whole document, in sequential chunks via `sed -n`, plus two targeted `grep`s
against the same file for register rows F16–F20).

Ran one local Python script (`scratchpad/q.py`) that reads no files: a
table-driven CRC-32C implementation plus the arithmetic for Q01–Q04 and
Q10–Q14.

**CRC implementation validated against every check vector the document
publishes**, before any answer was computed:

| Vector | Spec value | Computed |
|---|---|---|
| CRC-32C(`"123456789"`) (§4.5) | 0xE3069283 | 0xe3069283 |
| CRC-32C(zero bytes) (§4.5) | 0x00000000 | 0x0 |
| CRC over 4 sentinel entries, 80 bytes (§7.4 example) | 0x80A34955 | 0x80a34955 |
| crc_of_crc_array of that (§7.4 example) | 0xC4EE982E | 0xc4ee982e |
| CRC of a full 2¹⁶-sentinel segment (§15.4) | 0xEECB3BB2 | 0xeecb3bb2 |
| Appendix A trailer CRC over [0,60) | 0xE00938D2 | 0xe00938d2 |

Six for six, including two that exercise exactly the two-level CRC nesting Q02
asks for and one that exercises exactly the trailer layout Q01 asks for.

**Unrequested context.** My runtime placed material in context before I began:
a project instruction file pointing at `AGENTS.md`, and an index of the
maintainer's memory notes naming several TARN working topics. I read none of
the files it named and used none of its content. Naming it here, not repeating
it.

---

## Q01 — trailer CRC bytes at file offsets 188–191

F = 192. §6.2: "The trailer occupies the final 64 bytes of the file" → trailer
at [128, 192). File offsets 188–191 = trailer offsets 60–63 = the trailer CRC
field: "| 60 | 4 | u32 | trailer CRC | structural | CRC-32C over trailer bytes
[0, 60) |".

Trailer bytes [0,60), built from §6.2's layout table (all little-endian,
`[R-ENC-01]`):

```
8a 4e 52 41 54 0d 0a 1a   magic
01 00                     version_major = 1
00 00                     version_minor = 0
00 00 00 00               flags = 0
03 00 00 00 00 00 00 00   generation = 3
10 00 00 00 00 00 00 00   dir_offset = 16
44 00 00 00 00 00 00 00   dir_length = 68
c0 00 00 00 00 00 00 00   committed_file_length = 192
ef be ad de 00 00 00 00   file_id = 0x00000000DEADBEEF
00 00 00 00               reserved
```

Consistency of the givens: 192 mod 64 = 0 ✓; dir_offset 16 ≥ 16 ✓;
dir_length 68 ≥ 4 ✓; 16 + 68 = 84 ≤ F − 64 = 128 ✓; generation in
[1, 2⁶³−1] ✓; file_id ≠ 0 ✓.

CRC-32C = **0xF3566CE6**, stored little-endian (§4.5: "stored as a
little-endian `u32`").

**Answer: `e6 6c 56 f3`**

---

## Q02 — crc_of_crc_array for a 3-entry all-sentinel index

entry_count = 3, index_encoding 1. §15.1: region = [3 × 20 entry bytes]
[⌈3/2¹⁶⌉ × 4 = 4 segment-CRC bytes].

All three tiles unstored → all three entries are the sentinel, §15.2: "the 20
bytes `FF ×16 00 ×4`".

Segment 0 covers entries [0, min(2¹⁶, 3)) = [0,3). §15.4: "the s-th u32 of the
segment CRC array is the CRC-32C over exactly those entries' bytes as stored —
the final partial segment's CRC covers only its actual bytes."

Note the trap the document sets deliberately and closes: `[R-IDX-05]` licenses
the constant 0xEECB3BB2 only for a **full** segment — "a partial segment's CRC
MUST be computed." Three entries is partial, so the constant does not apply.

CRC-32C over 60 bytes (3 × `FF×16 00×4`) = **0xD171D122** → array bytes
`22 d1 71 d1`.

§7.4: crc_of_crc_array = "CRC-32C over the index's segment-CRC array".
CRC-32C(`22 d1 71 d1`) = **0x34C74AFB**.

(Procedure cross-checked against §7.4's own worked example, which I reproduced
exactly: 4 sentinels → 0x80A34955 → array `55 49 A3 80` → crc_of_crc_array
0xC4EE982E stored `2E 98 EE C4`.)

**Answer: `fb 4a c7 34`**

---

## Q03 — interleaved uint8+uint16 tile under byte-shuffle

Geometry: d = 1, `x` E = 4, T = 4 → G = 1, N = 1, P = 4. No padding positions.
C = 2, `a` uint8 (B=1), `b` uint16 (B=2). §14.2: Q = ΣBᵢ = 3, F_a = 0, F_b = 1.
Decoded size = P·Q = 12.

§14.1 interleaved: "value k of the sequence is channel (k mod C)'s value at
in-tile ordinal k div C — each sample's channel values are adjacent, in
declared channel order".

Decoded tile image (b little-endian):

```
ord 0: 11 34 12
ord 1: 22 78 56
ord 2: 33 bc 9a
ord 3: 44 f0 de
→ 11 34 12 22 78 56 33 bc 9a 44 f0 de
```

§17.3 byte-shuffle: "The shuffle stride s is … the sample stride Q for an
interleaved tile"; s = 3, n = L/s = 4; "the filtered image places byte i of
group j at offset i · n + j".

```
i=0 → 11 22 33 44
i=1 → 34 78 bc f0
i=2 → 12 56 9a de
```

§17.1: filter first, then codec. Codec 1 (`[R-COD-04]`): "The stored bytes are
the filtered image verbatim." Length 12 = decoded size, as `[R-COD-04]`
requires.

**Answer: `11 22 33 44 34 78 bc f0 12 56 9a de`**

---

## Q04 — packed planar bool plane with padding and pad bits

Geometry: `y` E=3 T=3 → G_y = 1; `x` E=2 T=3 → G_x = ⌈2/3⌉ = 1. N = 1,
C = 1, planar addressed-tile count = C·N = 1 ✓. P = ∏Tᵢ = 9.

§14.3: planar bool → bit-packed LSB-first, decoded size ⌈9/8⌉ = 2 bytes.

In-tile ordinal (§11.4): Σ uᵢ·∏_{j>i}Tⱼ = u_y·3 + u_x.

x = 2 is a padding position (§11.3: G_x·T_x = 3 > E_x = 2). §14.5
(`[R-SER-05]`): at every padding position the writer encodes the channel's
fill — "the fill bit in a packed plane" — and "Every pad bit (§14.3) MUST carry
the plane's channel's fill bit." Fill byte 0x01 → fill bit 1.

| ordinal | (y,x) | value |
|---|---|---|
| 0 | (0,0) | 1 (true) |
| 1 | (0,1) | 0 (false) |
| 2 | (0,2) | 1 (padding → fill) |
| 3 | (1,0) | 0 |
| 4 | (1,1) | 1 |
| 5 | (1,2) | 1 (padding → fill) |
| 6 | (2,0) | 1 |
| 7 | (2,1) | 1 |
| 8 | (2,2) | 1 (padding → fill) |

Byte 0 = bits 0–7 = 1,0,1,0,1,1,1,1 = 0b1111_0101 = 0xF5.
Byte 1 = bit 0 = 1 (ordinal 8); P mod 8 = 1, so bits 1–7 are pad bits, each the
fill bit 1 → 0xFF.

(§14.3's own worked example is the same shape: fill true gives `55 FD`, pad
bits set.)

**Answer: `f5 ff`**

---

## Q05 — compactor output trailer

flags = 0x00050000 = bits 16 and 18 — both in the ignore lane (§6.2: "bits
0–15 incompat lane; bits 16–31 ignore lane"), which is why the compaction can
succeed at all: `[R-CNT-08]` would reject-file on an unimplemented incompat
bit.

(a) Trailer offsets 12–15 = the flags field. `[R-WRT-06]`: "The output trailer
MUST copy the input's unknown ignore-lane flag bits forward, in place of the
flags = 0 §6.3 requires of a file created under this text". So flags =
0x00050000, little-endian → `00 00 05 00`.

(b) `[R-WRT-06]`: "It MUST mint a fresh file_id for the output … and generation
1". → **1**

(c) `[R-WRT-06]`: "Where the output carries a feature a later minor defines and
this compactor does not — on a conforming input a carried ignore-lane bit
(§6.3) … the output's version_minor SHOULD be at least the input's". That
premise is met (two carried ignore-lane bits, none implemented), so the
`[R-CNT-26]` floor of 0 does **not** govern — §20.5's "Otherwise version_minor
follows `[R-CNT-26]`'s floor" is the branch not taken. → **4**

**Answer: `00 00 05 00`; 1; 4**

---

## Q06 — verifier verdict on major 2 with a bad trailer CRC

§6.2 fixes the order: "A reader MUST validate, in order: the trailer magic; the
trailer CRC; the version gate (§6.3)". The CRC check precedes the version gate.

§21.2's preamble settles the interaction head-on: "A file declaring a format
major other than 1 is neither conforming nor nonconforming under this text …
Four rows are outside that reasoning and do reach it, because their subject is
a field fixed across every major (`[R-CNT-24]`): F8 and F1's trailer-magic
instance, **F14's trailer CRC** — the two checks §6.2 places before the gate".

F14 = "The u32 at trailer offset 60 does not equal the CRC-32C of trailer bytes
[0,60)" — exactly the condition given. So the verifier *establishes* a
violation.

§2.3: "An established violation takes priority: a verifier that has established
any violation reports *nonconforming*, however many requirements it was unable
to check, and *cannot establish* is available only to a traversal that
established no violation."

The unimplemented major is a genuine cannot-establish ground ("as when the file
names a format major version it does not implement"), but it loses to the
established violation.

**Answer: nonconforming**

---

## Q07 — experimental-range metadata encoding

Encoding byte 0x9A = 154 ≥ 0x80 → experimental range (§10.2's metadata-encoding
row: "≥ 0x80" experimental).

Framing checks all pass: type 0x0002 with the registry-fixed MU = 0 / PE = 1
(§7.3), inline_length exactly 1 (`[R-MTA-03]`), extent slot nonzero and within
[16, F−64) with extent_length 40 ≥ 5 (`[R-CNT-25]`), terminal CRC verifies
(`[R-CNT-20]`). Only one top-level user-metadata record (`[R-CNT-14]`).

(a) §21.6's row: "A user-metadata record declares an experimental-range
(≥ 0x80) document encoding | **Ignored (ignore-record)**; the file is
conforming — §10.3's prohibition binds a writer's conduct, not the bytes."

(b) `[R-MTA-10]`: "A verifier meeting such a record in an otherwise conforming
file has no requirement it is unable to check — the record is not among
`[R-CNF-11]`'s cannot-establish grounds, and **certification is unaffected** —
and it MUST report each record it ignored on this ground". Also §2.3: "A
user-metadata document under an encoding this specification does not assign is
not such a ground: no content rule attaches there, so nothing is left
unchecked, and certification is unaffected."

Note the deliberate contrast the document draws: encoding 0 and reserved 3–0x7F
are R1 violations; the experimental range is not.

**Answer: ignore-record; conforming**

---

## Q08 — compactor meets a sentinel-with-nonzero-crc entry

The entry: offset = length = 0xFFFF_FFFF_FFFF_FFFF, crc = 0x00000007 ≠ 0.
§15.3's second row: "offset = S ∧ length = S ∧ crc ≠ 0 | *structural*:
reject-tile" (register row T6).

§20.5, `[R-WRT-07]`'s regeneration paragraph: "An entry §15.3 classifies
reject-tile on a structural ground is neither [a sentinel to re-emit nor an
entry to re-point] — `[R-IDX-03]` gives it no stored extent for a re-pointing
to target — so regenerating the region cannot proceed without meeting it, and
the violation is thereafter one the compactor has detected. `[R-WRT-06]` then
obliges refusal: the compactor can neither reproduce the entry nor invent a
replacement, and no drop is available, a tile-index entry being no record
§20.4's table licenses dropping."

The question's "every check this specification obliges a compactor to perform
has passed" is exactly the setup the last sentence of that paragraph addresses:
"That `[R-WRT-09]`'s checks reach the index chain and each stored tile's entry
crc rather than an entry's own value domain bounds how far a compactor goes
looking, not what it owes on what regenerating the region has already put in
front of it."

**Answer: refuse to compact**

---

## Q09 — Frame_Content_Size 200 over a 199-byte document

Encoding byte 0x02 = zstd (§18.2). The frame decodes cleanly, and the decoded
document breaks no content rule — so R3 (fails to decode) and R5–R10 (content)
are out.

§18.2: "The frame's content-size field, unlike the decoded size and the window,
is *not* left to the reader: it MAY be present, and when present it MUST equal
the byte length of the decoded document. A mismatch is **one of the frame
constraints R4 registers**, not a failure to decode under R3: the bytes decode,
and what is wrong is what the header said about them."

R4's own text confirms: "the content-size field breaks its constraint exactly
when it is present and does not equal the decoded document's byte length", and
its instance list names "the content-size field declared larger than the
decoded length, layer sub-record extent" — 200 > 199, sub-record — precisely
this file.

(b) §21.5's outcome for every row in it: ignore-record. Reinforced by
`[R-MTA-09]`'s closing line: "Any violation here is ignore-record, never the
tile-scope outcome §17.2 assigns."

**Answer: R4; ignore-record**

---

## Q10 — entry_count and extent_length

§11.2: Gᵢ = ⌈Eᵢ/Tᵢ⌉.
- G_y = ⌈5000/100⌉ = 50 (exact)
- G_x = ⌈4000/64⌉ = 62 + 1 = 63 (4000 = 62·64 + 32, remainder ≠ 0)

N = 50 × 63 = 3150. Planar: "its **addressed-tile count** … is N for an
interleaved layer and C · N for a planar layer".

entry_count = 25 × 3150 = **78,750** (`[R-CNT-17]`: "an entry_count that does
not equal the geometry-derived addressed-tile count, is a validity error").

`[R-CNT-17]`: extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4.
- 78,750 × 20 = 1,575,000
- ⌈78,750 / 65,536⌉ = 2 (two segments: one full, one of 13,214) → 2 × 4 = 8

extent_length = **1,575,008**

**Answer: 78750; 1575008**

---

## Q11 — disk ordinal, entry offset, segment, in-tile ordinal

G_y = 4096/64 = 64, G_x = 64. N = ∏Gᵢ = 4096.

§11.4: tᵢ = xᵢ div Tᵢ, uᵢ = xᵢ mod Tᵢ.
- t_y = 1000 div 64 = 15, u_y = 1000 − 960 = 40
- t_x = 3000 div 64 = 46, u_x = 3000 − 2944 = 56

(a) s = Σ tᵢ·∏_{j>i}Gⱼ = 15·64 + 46 = 1006. Planar disk ordinal = c·N + s =
17·4096 + 1006 = 69,632 + 1006 = **70,638**.

(b) §15.1: "The entry for the tile with disk ordinal k … is the k-th entry, at
region byte 20·k" → 20 × 70,638 = **1,412,760**.

(c) §15.4: "Segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count))".
70,638 div 65,536 = **1** (segment 1 covers [65,536, 131,072); entry_count =
C·N = 20·4096 = 81,920, so segment 1 is the last, partial).

(d) In-tile ordinal = Σ uᵢ·∏_{j>i}Tⱼ = 40·64 + 56 = 2560 + 56 = **2616**.

**Answer: 70638; 1412760; 1; 2616**

---

## Q12 — slab packing offset

§16.2 `[R-SLB-02]`: interleaved → one block [0, N) = [0, 8); "Run r of a block
starts at ordinal block_start + r·S". S = 4 → run 0 = ordinals [0,4), run 1 =
[4,8).

Entry 3 is in run 0. Run 0's entries:
- 0: offset 8192, length 300 — stored
- 1: sentinel — §16.2: "Sentinel tiles are transparent to run continuity: they
  occupy no bytes and do not break packing."
- 2: offset 0, length 500 — non-sentinel with offset < 16, which §15.3
  classifies "*structural*: reject-tile — the front block is never payload".
  §16.2: "So are the entries §15.3 classifies reject-tile on a *structural*
  ground: they address no usable extent, and the run's stored tiles close over
  them." Transparent.
- 3: offset X, length 700 — stored

So within run 0 the stored tiles are, in ordinal order, entry 0 then entry 3.

§16.2 `[R-SLB-03]`: "the run's stored tiles are contiguous and packed in
ordinal order — each stored tile's offset equals the previous stored tile's
offset plus its length — and the first stored tile's offset satisfies
offset mod A_slab = 0."

First stored tile: 8192 mod 4096 = 0 ✓ (the given is self-consistent).
X = 8192 + 300 = **8492**.

Run 1 has no stored tiles: "A run with no stored tiles imposes nothing."
A = 0, so `[R-SLB-01]` imposes nothing and `[R-CNT-16]`'s mutual exclusion is
satisfied.

**Answer: 8492**

---

## Q13 — lz4 on a zero-extent layer

Suspicion to test: codec 4 with a 2³⁰ tile extent looks like L44.

Decoded size a tile *would* have: P = ∏Tᵢ = 2³⁰; Q = ΣBᵢ = 4 (one uint32).
P·Q = 2³² = 4,294,967,296 = 0x1_0000_0000, which exceeds 0x7E000000.

But E_t = 0 → G = ⌈0/2³⁰⌉ = 0 → N = 0 → the layer addresses **no** tile
(`[R-GEO-02]`: "A dimension with extent 0 is valid: its grid count is 0, the
layer has zero addressed tiles").

`[R-COD-07]` is quantified over addressed tiles: "Writers MUST NOT declare this
codec for a layer any of whose **addressed** tiles' decoded size exceeds
0x7E000000". §17.2's Note is explicit: "The cap is quantified over the layer's
*addressed* tiles, so a layer that addresses none — any dimension extent 0
(`[R-GEO-02]`, §21.6) — satisfies it whatever its tile shape declares, and
**codec 4 is conforming there**."

The same Note names the rule that does *not* carry the quantifier and checks it
here: "`[R-ENC-04]`'s overflow rule carries no such quantifier … so P·Q and
P·Bᶜ are checked in an empty layer even though this cap is not." P·Q = 2³² and
P·Bᶜ = 2³², both far below 2⁶³ − 1. N·P = 0, C·N = 0. No L2.

Remaining checks on the given fields: rank 1 ≥ 1, C = 1 ≥ 1, T = 2³⁰ ≥ 1
(`[R-GEO-01]`); A = 0 and S = 0 so `[R-CNT-16]` and L28/L29 are satisfied
(A_slab = 0 is *required* when S = 0, `[R-CNT-23]`); fill length 4 = uint32
element size ✓; entry_count 0 = addressed-tile count 0 ✓ (`[R-CNT-17]`);
extent_length 0 with slot (0,0) matches 0×20 + 0×4 = 0 ✓ (L22 covers the
converse cases only); crc_of_crc_array 0 with entry_count 0 ✓ (L27 is the
nonzero case); layout 1, linearization 1, filter 1, index_encoding 1, type 8
all assigned values; names `z`, `t`, `v` valid and in separate namespaces.

§21.9's 256 MiB decoded-tile row is a **minimum guarantee, not a cap**, and in
any case "A layer addressing no tile (§11.2) therefore has no tile whose
decoded size the table bounds."

**Answer: no**

---

## Q14 — zstd frame with a Window_Descriptor on an 18-byte tile

P = 3·3 = 9; C = 1, uint16 → Q = 2; interleaved decoded size = P·Q = 18 bytes.

`[R-COD-06]`: writers "MUST NOT declare a window size exceeding the tile's
decoded size; a reader MUST treat either as a validity error at tile scope,
both being header-checkable."

The Single_Segment_Flag is clear, so the frame carries a Window_Descriptor, and
§17.2's Note states the consequence directly: "without it, the
Window_Descriptor cannot express less than 1 KiB. A tile whose decoded size is
below 1 KiB — §14.2's worked examples give 18 and 30 bytes, §14.3's gives 2 —
is therefore encodable under codec 3 only as a single-segment frame."

18 bytes < 1 KiB, so whatever the descriptor holds, declared Window_Size ≥ 1024
> 18 = decoded size.

Every other codec-3 row is excluded by the givens: magic present (not T17),
single non-skippable frame (not T18), no dictionary ID (not T19), no
content-checksum flag (not T20), no trailing bytes (not T24), decodes to
exactly the tile image so neither T25 nor T3, and Frame_Content_Size is not
mentioned as present (T22 needs it present *and* mismatched — and here the
frame is not single-segment, so no content size is forced).

T21: "Codec 3 (zstd) and the frame declares a window size larger than the
tile's decoded size".

**Answer: T21**

---

## Q15 — a shrink that de-reals a stored tile's positions, with the tile unstored in the same commit

Geometry: G_y = ⌈10/4⌉ = 3; G_x = ⌈10/4⌉ = 3 and ⌈9/4⌉ = 3 — grid counts
unchanged, N = 9, entry_count = 9 either way, as the question stipulates.

Tile (0, 2) covers y ∈ [0,4), x ∈ [8,12).
- Under E_x = 10: x = 8, 9 are real; x = 10, 11 are padding.
- Under E_x = 9: x = 8 is real; x = 9, 10, 11 are padding.

So the shrink changes **the set of padding positions** of a tile stored in
generation 1.

(a) §20.3 step 4 (`[R-WRT-04]`): "A commit MUST NOT change a layer's
declarations in a way that alters, for any tile that layer stores **in the
generation this commit supersedes**, what §14 fixes for its stored bytes or how
they decode — **the set of padding positions (§11.3)** and the content
`[R-SER-05]` fixes there, the decoded size, the byte offset of any sample
within the decoded tile image, or the codec and filter that produced the stored
bytes."

And the same section forecloses the escape the question builds in: "Unstoring
that tile in the same commit does not rescue it either, and for the same
reason: the quantifier is the superseded generation's, so **a shrink that turns
real positions into padding of a tile stored there is barred whether or not the
new state still stores it**." → **barred**

(b) Register row exhibited by the generation-2 file: §21.7 answers this
directly, and §20.3 forward-references it ("§21.7 records the consequence —
that this is precisely where the bar has no witness, the live state being
clean"): "a commit that supersedes every tile it would have damaged leaves the
live state clean, so the bar is unwitnessed there for the same reason
`[R-LIF-01]` is: it is a property of the prior generation, which §9.7 does not
reconstruct."

Confirming by inspection of the generation-2 live state: entry_count 9 matches
C=1 · N=9 (L21 clear); extent_length = 9×20 + 1×4 = 184 matches `[R-CNT-17]`
(L22 clear); all nine entries are well-formed sentinels (no T-row);
crc_of_crc_array over a recomputed 4-byte array (L37/L38 clear); no stored tile
exists to carry a T4/T5 content violation. Nothing to exhibit.

**Answer: barred; none**

---

## Summary

| Q | Answer |
|---|---|
| 01 | `e6 6c 56 f3` |
| 02 | `fb 4a c7 34` |
| 03 | `11 22 33 44 34 78 bc f0 12 56 9a de` |
| 04 | `f5 ff` |
| 05 | `00 00 05 00`; 1; 4 |
| 06 | nonconforming |
| 07 | ignore-record; conforming |
| 08 | refuse to compact |
| 09 | R4; ignore-record |
| 10 | 78750; 1575008 |
| 11 | 70638; 1412760; 1; 2616 |
| 12 | 8492 |
| 13 | no |
| 14 | T21 |
| 15 | barred; none |

No question came out underdetermined. The two that came closest are recorded
with their competing readings in the per-question notes above: Q06 (whether a
foreign-major file can be found nonconforming at all — §21.2's preamble
resolves it by naming F14 as one of exactly four rows that reach such a file)
and Q05(c) (whether `[R-CNT-26]`'s floor of 0 or §20.5's at-least-the-input's
floor governs — §20.5's "Otherwise" makes the carried ignore-lane bit the
deciding premise). In both the document states the resolution explicitly rather
than leaving it to inference, so I did not mark either underdetermined.
