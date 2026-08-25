# TARN cleanroom round 24 — Reader implementer transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,445 lines), in five `Read` calls covering lines 1–4445, plus one `grep` over
that same file for analogy connectives ("exactly as", "the same way", "for the
same reason", "transposed", "likewise", …). I opened no other file in the
repository: no `docs/`, no `conformance/`, no `spec/registry.json`, no
`PLAN.md`/`AGENTS.md`/`README.md`, no git history, no web.

I ran local computation that reads no repository file:

- `scratchpad/crc.py` — a CRC-32C implementation (Castagnoli, reflected, init
  0xFFFFFFFF, final XOR) used to check the document's stated check vector and
  its four stated CRC constants.
- `scratchpad/appa.py` — re-parses Appendix A's hex dump (typed in from the
  document, not read from disk) and recomputes its trailer CRC.
- `scratchpad/build.py` — emits a complete conforming TARN file from the
  document's rules alone.
- `scratchpad/read.py` — an independent reader that walks that file per §19.
- Two throwaway scripts: one that counts §21's register rows and instances
  by parsing the markdown tables of the one file I am permitted to read, and
  one that works the planar mis-mapping case for finding reader-01.

I wrote this transcript and the scratch files above. I did not read the output
directory.

**Context I did not ask for.** My runtime placed material in context before I
began: a project instruction file (`CLAUDE.md`, pointing at `AGENTS.md`) and an
index of the maintainer's memory notes with several titles that name TARN
working practice and prior-round failure shapes. I did not open any file it
named and I have not used any of its content as evidence about the
specification. Disclosing that it appeared, per the brief.

---

## 1. What I set out to do

Write a conforming reader on paper, in the order I would actually write the
code, and stop every time the document failed to tell me what to do. Then walk
the degradation paths, then check every stated constant, offset and checksum I
could check.

I read the four flagged passages (§20.5, §21.2, §21.5, §21.7) first and last,
but the bulk of the walk is the reader itself.

---

## 2. Constants and checksums I could check

Every numeric claim I could decide, I decided.

### 2.1 The checksum function (§4.5)

Implemented CRC-32C with polynomial 0x1EDC6F41 reflected (0x82F63B78), reflected
in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF.

| Claim | Document | Computed |
|---|---|---|
| CRC-32C("123456789") | `0xE3069283` | `0xe3069283` ✓ |
| CRC-32C(zero bytes) | `0x00000000` | `0x0` ✓ |
| CRC of 4 sentinel entries (80 bytes), §7.4 example | `0x80A34955`, stored `55 49 A3 80` | `0x80a34955`, `55 49 a3 80` ✓ |
| crc_of_crc_array over that 4-byte array, §7.4 example | `0xC4EE982E` | `0xc4ee982e` ✓ |
| CRC of a full all-sentinel segment (2¹⁶ entries), §15.4 / App. B | `0xEECB3BB2` | `0xeecb3bb2` ✓ |

All four stated constants are correct. That is a real result: a wrong
`0xEECB3BB2` would have been a silent interoperability trap, since
`[R-IDX-05]` lets a writer emit it without computing it while forbidding a
reader to match against it.

### 2.2 Appendix A's annotated minimal file

I typed the 128-byte hex dump out of the document and parsed it as a trailer.

```
magic            8a 4e 52 41 54 0d 0a 1a   ✓ matches §6.2's constant
version_major    1                          ✓
version_minor    0                          ✓
flags            0                          ✓ both lanes clear
generation       1                          ✓ ≥ 1
dir_offset       16                         ✓ ≥ 16
dir_length       4                          ✓ ≥ 4
committed_file_length 128                   ✓ = file size, ≡ 0 mod 64
file_id          0x0123456789abcdef         ✓ ≠ 0, and the LE byte order in
                                              the dump (EF CD AB 89 …) is right
reserved         00 00 00 00                ✓
stored CRC       0xe00938d2
computed CRC over [0,60)  0xe00938d2        ✓
```

`dir_offset + dir_length = 20 ≤ F − 64 = 64` ✓. The directory region [16,20) is
four zero bytes = CRC-32C of zero bytes over a zero-length record sequence ✓.
Appendix A is internally exact.

Appendix A's closing paragraph also claims "112 bytes covering [16, 128)
contains the directory" — 128 − 16 = 112 ✓, and bytes [0,16) stay non-resident,
so `[R-CNT-04]`'s residency test leaves the front-block check optional there ✓.

### 2.3 The worked examples in Parts I and II

| Where | Claim | Check |
|---|---|---|
| §5.1 | smallest conforming file = 128 bytes | 16 + 4 = 20; next 64-aligned trailer start ≥ 20 is 64; F = 128 ✓ |
| §7.4 | layer-record inline payload = 81 bytes | 4 (name) + 34 (nine scalars: 1+2+2+2+8+8+8+1+2) + 18 (dim) + 12 (chan) + 13 (trailing) = 81 ✓; the offset column 0,4,5,7,9,11,19,27,35,36,38,40,48,56,63,68,69,77(+4)=81 ✓ |
| §7.4 | index extent length 4×20 + ⌈4/2¹⁶⌉×4 = 84 | 80 + 4 = 84 ✓ |
| §11.2 | (1024,2048)/(256,256) → G=(4,8), N=32, P=65536 | ✓ |
| §11.2 | extents (1000,2048): G_y = ⌈1000/256⌉ = 4 | ✓ |
| §11.4 | (300,700) → tile (1,2), s = 10, in-tile (44,188), ordinal 11,452 | 44·256+188 = 11,452 ✓; planar C=4, c=2 → 2·32+10 = 74 ✓ |
| §14.2 | interleaved (2,3), uint8+uint16: Q=3, size 18, ordinal 5 at [15,18) | ✓; planar `b` 12 bytes, ordinal 5 at 10–11 ✓; float32+bool: Q=5, size 30, [25,30) ✓ |
| §14.3 | planar bool (2,5), P=10, alternating → `55 01`; fill true → `55 FD` | bits 0..7 = 1,0,1,0,1,0,1,0 = 0x55 ✓; byte 1 bits 0–1 = 1,0 → 0x01, pad bits 2–7 set → 0xFD ✓ |
| §14.5 | (5,5)/(4,4), edge tile (1,1): 1 real, 15 padding, 32 bytes, `CD AB` ×15 | ✓ |
| §15.4 | entry_count 1,000,000: 16 segments (15 full + 16,960), 64-byte array, region 20,000,064; tile 999,999 at segment-relative 339,180; array [20,000,000, 20,000,064); segment 15 [19,660,800, 20,000,000) | all ✓; 65,536×20 = 1,310,720 = 1.25 MiB ✓ |
| §15.4 | planar C=4, N=32: disk 74, entry bytes [1,480,1,500); channel 3 = entries 96–127 | 74×20 = 1480 ✓ |
| §17.3 | shuffle of 1.0,2.0,3.0 f32 → `00 00 00 00 00 00 80 00 40 3F 40 40` | recomputed byte-for-byte ✓ |
| §20.3 | 32-tile layer index region = 32·20 + 4 = 644 | ✓ |
| §21.9 note | 2³² tiles → 256 KiB CRC array; 2³⁶ → 4 MiB | 2¹⁶×4 = 256 KiB ✓; 2²⁰×4 = 4 MiB ✓ |
| §21.8 | "121 conditions over 277 instances" | parsed the four register tables mechanically: F 36/58, L 49/116, T 26/55, R 10/48 → **121 rows, 277 instances** ✓ exactly |

The `[R-COD-06]` note's claim that a Window_Descriptor "cannot express less than
1 KiB" is right (RFC 8878's windowBase = 1 << (10 + Exponent), minimum 1024), so
its conclusion — a sub-1-KiB tile is encodable under codec 3 only as a
single-segment frame — holds, and it is a claim worth having checked, because
without it §14.2's own 18- and 30-byte examples would be unencodable under a
core codec.

**No stated constant, offset, or checksum in this document is wrong.** I looked
for the high-value finding my charter names and did not find one.

---

## 3. The open path, byte-exact

### 3.1 Steps, and what bounds each range

`[R-RDR-01]` fixes four steps. Written as I would code them:

1. **F.** Transport-authoritative size (`[R-CNT-10]`): a full-response content
   length, the complete length of a range response, or a size probe. Explicitly
   *not* the trailer's `committed_file_length` — a reader that cannot obtain a
   real one MUST probe or fail. Nothing bounds this request; it is the anchor.
2. **Trailer.** Fetch `[F−64, F)`. Bounded by the transport alone. Validate in
   §6.2's fixed order:
   - trailer magic `8A 4E 52 41 54 0D 0A 1A` (F8; byte-reversed is F1);
   - trailer CRC over `[0,60)` (F14);
   - version gate (F18 for 0, capability refusal for a foreign major);
   - then, **together**, the flag gates (F19), `cfl == F` (F17), `cfl ≡ 0 mod
     64` (F13), `dir_offset ≥ 16` (F9), `dir_length ≥ 4` (F16),
     `dir_offset + dir_length ≤ F−64` (F10), `1 ≤ generation ≤ 2⁶³−1` (F11),
     `file_id ≠ 0` (F12), reserved bytes zero (F15).
   `[R-VEC-02]` acknowledges that the last group is unordered, so a file failing
   two of them attributes to neither alone. I coded them as a single group.
3. **Directory.** Fetch `[dir_offset, dir_offset + dir_length)`. **What bounds
   it before I read it**: `dir_offset` and `dir_length` are covered by the
   trailer CRC I verified in step 2 (`[R-ENC-05]`, `[R-ENC-10]`), and
   `dir_offset + dir_length ≤ F−64` caps it against a size I got from the
   transport, not from the file. That is the whole of §22.2's amplification
   defense on the open path. Verify the terminal CRC over the preceding
   `dir_length − 4` bytes before any other use (F20).
4. **Record walk.** Parse the `dir_length − 4` byte sequence as 24-byte headers
   plus inline payloads, no residue (F29, F24), MU gate for unknown top-level
   types (F35/§21.6), multiplicity (F34), extent-slot validity for **non-layer**
   top-level records only (F30–F32), the user-metadata framing floor
   (F21/F22/F23), and the layer-name namespace (F4, then L3/L5/L6).

### 3.2 Byte-exact cost of a cold remote open

**Two requests.** Suffix range for the final 64 bytes (64 bytes, and the
response carries F), then `[dir_offset, dir_offset+dir_length)` (`dir_length`
bytes). **Total 64 + dir_length bytes, in 2 round trips, at any file size and
any layer count** — the invariant §6.4's note calls the working set.

The front signature block is **not** in that accounting. `[R-CNT-04]` turns the
obligation on *residency*, not transport: a two-exact-range remote reader never
holds `[0,16)` and MAY omit the check entirely. I coded it that way and my
reader never fetched bytes 0–15. A speculative-suffix reader that reaches offset
0 must check it, before other processing.

On my own worked file (§4 below): **2 requests, 64 + 123 = 187 bytes.**

The alternative §6.4 licenses — one speculative suffix window, using containment
— collapses steps 1–3 into one request; §19.1 says so explicitly. Nothing here
is a conformance property.

---

## 4. A file I built, and my reader walking it

I did not want to grade the document on Appendix A alone (zero layers exercises
almost nothing), so I built a file from the rules and then wrote an independent
reader against it.

### 4.1 The file

Layer `grid`: rank 2, dimensions `y` (E=5, T=4) and `x` (E=5, T=4); one
interleaved `uint16` channel `v` with fill `0xABCD`; linearization 1, codec 1,
filter 1, A = 0, S = 0, A_slab = 0, index_encoding 1.

Derived: G = (2,2), N = 4, P = 16, C = 1, Q = 2, decoded size = P·Q = 32,
addressed-tile count = N = 4 (interleaved), entry_count = 4, segments =
⌈4/2¹⁶⌉ = 1, index extent length = 4·20 + 1·4 = 84.

Only spatial tile 0 stored, holding v(y,x) = 100y + x; entries 1–3 sentinel.

Layout:

```
[0,16)     front signature block
[16,48)    tile 0 payload (32 bytes)
[48,132)   tile-index region (80 entry bytes + 4 CRC bytes)
[132,255)  directory region (one 119-byte layer record + 4-byte CRC)
[255,256)  pre-trailer pad (1 byte)   <- `[R-LIF-02]` step 5 pads to 64
[256,320)  trailer
F = 320
```

`inline_length` = 95, so the layer record is 119 bytes; `dir_length` = 123.
`dir_offset + dir_length = 255 ≤ F − 64 = 256` ✓. F ≡ 0 mod 64 ✓.

Computed: tile CRC `0xD7839CC7`; segment CRC `0x7E815880`; crc_of_crc_array
`0xA0D0C8CA`; directory CRC `0xC9C6348F`; trailer CRC `0x7E44E355`.

Full hex dump is in §4.4 below.

### 4.2 The reader's walk

The reader re-derives everything from the bytes:

```
step1 F = 320
step2 trailer ok: gen=1 dir=[132,255) F=320 file_id=0x123456789abcdef
step3 directory CRC ok, record sequence 119 bytes
  record type=0x0001 flags=0b11 inline_length=95 extent=(48,84)
step4 layer names: ['grid']
OPEN COST: requests [(256,320), (132,255)]  bytes 187
```

Layer access (§19.3), no fetch, everything from the resident directory and F:

```
layer 'grid' dims=[('y',5,4),('x',5,4)] G=[2,2] N=4 P=16 C=1 layout=1 Q=2
entry_count=4 segments=1 index extent=(48,84) decoded_size=32
```

Cross-checks that fired at layer access and are `[R-RDR-03]`'s subject:
`entry_count == N` (else L21), `extent_length == 4·20 + 1·4` (else L22), fill
length == element size (else L30), value sets for layout/linearization/codec/
filter/index_encoding/type (L36/L33/L43/L45/L31/L34), geometry floor (L32),
`[R-COD-07]`'s lz4 cap (not applicable, codec 1).

Tile reads (§19.4):

```
read (2,3): stored  s=0 in-tile ordinal=11 disk=0 value=cb 00  -> 203
read (0,0): stored  s=0 in-tile ordinal=0  disk=0 value=00 00  -> 0
read (4,4): fill    s=3 in-tile ordinal=0  disk=3 value=cd ab  -> 0xABCD
read (3,4): fill    s=1 in-tile ordinal=12 disk=1 value=cd ab  -> 0xABCD
```

Each is what §11.4 and §14.2 predict: (2,3) → tile (0,0), s = 0·G_x + 0 = 0,
in-tile (2,3) → ordinal 2·4+3 = 11, byte offset 11·Q = 22, and bytes [22,24) of
the payload are `CB 00` = 203 = 100·2+3 ✓. (3,4) → tile (0,1), s = 0·2+1 = 1,
sentinel → fill, and 0xABCD comes back bit-exact (`[R-TYP-06]`, `[R-TYP-08]`).

**Cold remote cost of one tile read**, on top of the open: the segment CRC array
`[128,132)` = 4 bytes, the segment `[48,128)` = 80 bytes, the payload `[16,48)`
= 32 bytes — **3 requests, 116 bytes**. The array and segment fetches MAY run in
parallel (`[R-IDX-04]`) and both are computable from the layer record alone;
their verification results MAY be cached under `[R-LIF-03]`, which is why my
reader re-fetched them on each of the four reads only because I wrote it naively.
§15.4's example gives the shape at scale: never more than one full segment
(1.25 MiB) plus the CRC array, at any layer size.

### 4.3 Decoded byte layout I ended up with

Interleaved, C = 1, B = 2, Q = 2, P = 16 → decoded tile image = 32 bytes, value
k at byte `(k div C)·Q + F_{k mod C}` = `k·2`:

```
0000  00 00 01 00 02 00 03 00   v(0,0..3) = 0,1,2,3
0008  64 00 65 00 66 00 67 00   v(1,0..3) = 100..103
0010  C8 00 C9 00 CA 00 CB 00   v(2,0..3) = 200..203
0018  2C 01 2D 01 2E 01 2F 01   v(3,0..3) = 300..303
```

Tile 0 covers y,x ∈ [0,4) — entirely inside the extents (5,5), so it carries no
padding position and §14.5 imposes nothing on it. Tiles 1, 2 and 3 *would* carry
padding (x or y ∈ [5,8)), which is exactly why storing them sentinel is the
cheap, legal choice a sparse writer makes.

### 4.4 The file

```
0000  89 54 41 52 4E 0D 0A 1A 00 00 00 00 00 00 00 00
0010  00 00 01 00 02 00 03 00 64 00 65 00 66 00 67 00
0020  C8 00 C9 00 CA 00 CB 00 2C 01 2D 01 2E 01 2F 01
0030  10 00 00 00 00 00 00 00 20 00 00 00 00 00 00 00
0040  C7 9C 83 D7 FF FF FF FF FF FF FF FF FF FF FF FF
0050  FF FF FF FF 00 00 00 00 FF FF FF FF FF FF FF FF
0060  FF FF FF FF FF FF FF FF 00 00 00 00 FF FF FF FF
0070  FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00
0080  80 58 81 7E 01 00 03 00 5F 00 00 00 30 00 00 00
0090  00 00 00 00 54 00 00 00 00 00 00 00 04 67 72 69
00A0  64 01 01 00 01 00 01 00 00 00 00 00 00 00 00 00
00B0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00C0  02 01 00 01 79 05 00 00 00 00 00 00 00 04 00 00
00D0  00 00 00 00 00 01 78 05 00 00 00 00 00 00 00 04
00E0  00 00 00 00 00 00 00 01 76 07 00 02 CD AB 01 04
00F0  00 00 00 00 00 00 00 CA C8 D0 A0 8F 34 C6 C9 00
0100  8A 4E 52 41 54 0D 0A 1A 01 00 00 00 00 00 00 00
0110  01 00 00 00 00 00 00 00 84 00 00 00 00 00 00 00
0120  7B 00 00 00 00 00 00 00 40 01 00 00 00 00 00 00
0130  EF CD AB 89 67 45 23 01 00 00 00 00 55 E3 44 7E
```

### 4.5 Where I had to guess while building this

Nowhere. Every field width, order, prefix width, sentinel pattern, ordinal
formula, CRC scope and layout constant I needed was stated. The specific things
I expected to have to guess and did not:

- fill length prefix width — §4.2 states it (`u8`), and `[R-CNT-23]` ties it to
  the element size so the payload parses without type knowledge;
- whether the segment CRC array immediately follows the entry array — §15.1,
  "with no padding anywhere inside the region";
- whether a zero-tile layer has an index region — §7.4 + `[R-CNT-17]` +
  §15.4's example: extent (0,0), crc_of_crc_array 0, nothing fetched;
- the layer record's flags — §7.3's table fixes MU = 1, PE = 1, so `0x0003`;
- whether interleaved value k belongs to channel `k mod C` or `k div P` —
  `[R-SER-01]` says sample-major and §14.2's offset formula agrees;
- reserved record flag bits — writers zero, readers ignore, verifier detects.

---

## 5. Validation timing by tier

Coded as four gates, per `[R-RDR-02]`. The rule fixes the **latest** detection
point; earlier is always licensed, so divergence is only ever toward earlier
rejection.

**At open** — front block *if resident*; trailer; directory region and its CRC;
the record walk; the layer-name namespace. Note two things I had to read twice:

1. The layer-name namespace is built at open, but from "the name fields a
   reader can obtain under §7.4's framing". A layer record whose name field
   overruns `inline_length` contributes **no** name and is instead reject-layer.
   So my open builds the namespace from a partial set.
2. Uniqueness is decided **first**, over raw bytes, "whether or not each name is
   itself well-formed". So F4 (reject-file) can fire on two byte-identical names
   neither of which is a valid name. I ordered my code that way: compare bytes,
   then validate UTF-8 and the name rules (L3/L5/L6), also at open.

**At first access to a layer** — the whole of `[R-RDR-03]`. Crucially "layer
access performs no fetch": every item on its list is decidable from the resident
directory and F. I verified that against the list — extent-slot bounds need F
(resident), the index cross-checks need only `entry_count` and `extent_length`,
`[R-COD-07]`'s cap needs only declarations, `[R-ENC-04]`'s ceiling needs only
declarations. It holds.

**At use of a tile** — the index chain (crc_of_crc_array, then the segment CRC),
the entry classification, the payload CRC, and the decode checks. Note the scope
inversion the rule names explicitly: an index-chain failure is detected at tile
use but takes **layer** scope (`[R-IDX-04]`), and §19.4 step 8 spells out the
consequence — such a failure bars the request's remaining entries and all
further service from the layer, prospectively, so values already returned stand.

**At use of a record's extent** — the extent CRC and the document content rules
§18.2 attaches at its encoding. Never at open, because the open fetches no
extent.

**What a reader is permitted never to check.** Everything whose Detector cell is
*verifier*: live-state coverage and the slack total (§9.7), extent overlap (F33,
L18), the pre-trailer gap (F7), record flag bits (F25/F26/F28, L46/L47/L49),
reserved-range type values whatever the MU bit (F36, L25), alignment and slab
invariants (L40/L41/L42), all decoded-content obligations (T2, T4, T5, T26), and
user-metadata member ordering (F27, L48). Also the front signature block, for a
reader that would have to fetch it (`[R-CNT-04]`) — an exemption §2.3 does not
extend to verifiers. A reader that *does* detect a verifier row MAY reject the
file under `[R-CNF-12]`, but is not obliged to and is not nonconforming for not
looking.

**What becomes a verdict when.** A verifier's verdict is *nonconforming* the
moment it establishes any violation, however much it could not check;
*cannot establish* is reserved for a traversal that established none and was
blocked on a capability or resource ground — a foreign major, an unimplemented
MU = 1 type, an inexecutable codec or filter, a declined decode on resource
grounds, or a declined user-metadata document. An unassigned metadata encoding
is expressly *not* such a ground (`[R-MTA-10]`), because no content rule
attaches there; the verifier certifies and reports the record.

---

## 6. Layer access and the tile-read algorithm

From a layer name and a coordinate:

1. **Name → record.** Built at open. §19.3's full validation runs before any
   declaration other than the name is used.
2. **Domain.** Point request: `0 ≤ xᵢ < Eᵢ`. Outside → the request fails as a
   request, no verdict on the file. Region request: intersect with the extents;
   a disjoint region, or any region of a zero-extent layer, **succeeds and
   returns nothing**. The point/region asymmetry at a single coordinate is
   deliberate and stated ("a range whose every interval holds a single position
   is a region request").
3. **Ordinals.** `tᵢ = xᵢ div Tᵢ`, `uᵢ = xᵢ mod Tᵢ`; in-tile ordinal
   `Σ uᵢ·∏_{j>i} Tⱼ` (row-major, permanently, every linearization); spatial
   ordinal `s = Σ tᵢ·∏_{j>i} Gⱼ` (linearization 1 only, and 1 is the only legal
   value); disk ordinal `s` interleaved, `c·N + s` planar.
4. **Index chain.** Fetch the CRC array at region bytes
   `[entry_count·20, entry_count·20 + ⌈entry_count/2¹⁶⌉·4)` and the segment for
   `s' = disk div 2¹⁶` at `[s'·2¹⁶·20, min((s'+1)·2¹⁶, entry_count)·20)`. Verify
   crc_of_crc_array, then the segment CRC, in that dependency order; both may be
   fetched in parallel and both verifications may be cached.
5. **Entry.** Classify per §15.3. Sentinel (`FF ×16 00 ×4`) short-circuits: fill,
   bit-exact, no I/O. Six *structural* rows reject the tile and yield no extent
   at all — those entries are transparent to slab run continuity and contribute
   nothing to the coverage walk, so the bytes they nominally address fall to
   slack. The seventh failure mode — stored bytes failing the entry's crc — is
   different: the entry is well-formed, its extent stands, and it keeps its place
   in the verifier rows, run continuity and the walk. That distinction is stated
   three times (§15.3, §16.2, §9.7) and each statement agrees.
6. **Payload.** Fetch `[offset, offset+length)`, verify the crc **before**
   decoding.
7. **Decode.** Codec first, then the filter's inverse. Under codec 1 the entry's
   length must already equal the decoded size, checkable before any fetch
   (`[R-COD-04]`, T14). Under 2–4 no bound relates stored length to decoded size
   in either direction; the reader allocates from declarations only.
   `[R-SER-07]` then requires the decoded length to be *exactly* the decoded
   size (T3) — this is the decompression-bomb defense.
8. **Extract.** Interleaved: value at `u·Q + Fᶜ`. Planar numeric: `k·Bᶜ`.
   Planar bool: bit `k mod 8` of byte `k div 8`, LSB-first. Padding positions are
   never returned; pad bits never encode values.
9. **Return.** Bit patterns unaltered. The single exception in the whole format
   is `[R-SER-08]`: a nonconforming interleaved bool byte a reader chooses to
   return rather than reject reports 0x00 as false and every other byte as true.

**Byte-shuffle strides I had to get right.** `s = Bᶜ` for a planar numeric tile,
`s = Q` for an interleaved tile, `s = 1` (identity) for a packed bool plane. `L`
is divisible by `s` in every case — I checked all three: `P·Q / Q`, `P·Bᶜ / Bᶜ`,
`⌈P/8⌉ / 1`.

A useful property I derived while checking §21.7's filter claims: the shuffle
maps position 0 to 0 and position `L−1` to `(s−1)·n + (n−1) = L−1`, so the final
byte of an image is **invariant under any stride**. That means a mis-strided
filter can never disturb a packed plane's pad bits, which is why T26 correctly
names only T2 and T4 as its detectors and not T5 — a distinction I initially
suspected was an error and it is not.

---

## 7. Degradation walks

Traced end to end, seven of them.

**(1) Unknown record type, top level, MU = 0.** Ignore-record. The record is
skipped as though absent; decoding of all stored data is unaffected; every layer
still serves. An updater retains or drops it per its stored PE bit — and here
the stored bits *are* authoritative, because the tool does not implement the
type. If the value is experimental (≥ 0x8000) the file is conforming (§21.6); if
reserved (0x0003–0x7FFF) the file is nonconforming (F36) but the reader behaves
identically. **Serves: everything.**

**(2) Unknown record type, top level, MU = 1.** Reject-file. The reader serves
nothing. If experimental, this is one of exactly two "conforming files a reader
refuses" §21.6 names; the diagnostic ought to say capability, not corruption.
The same type as a **layer sub-record** is a different walk: reject-layer, and
`[R-CNT-18]` forbids rejecting an otherwise-conforming file for it. **Serves:
every other layer.** I note a wording problem about that qualifier in
reader-03.

**(3) Unknown codec.** For a *conforming* reader this can only be an unassigned
value, since all four assigned codecs are core — declining a core codec makes
you a non-conforming reader outright, not a subset one. Value 0, 5–0x7FFF or
≥ 0x8000 → reject-layer at **layer access**, before any I/O (L43). Same shape
for filter (L45), layout (L36), linearization (L33), sample type (L34), index
encoding (L31). **Serves: every other layer, and it MAY still list the rejected
layer's name.** A *verifier* that cannot execute a codec is in a different
position again: not a violation, but *cannot establish* (`[R-COD-11]`).

**(4) Unrecognized flag or enum value.** Trailer ignore-lane bit (16–31):
ignored, file conforming, and an updater MUST carry it forward. Trailer
incompat-lane bit (0–15): reject-file (F19), and this text defines none, so every
set bit is unimplemented. Record flag bits 2–15: readers MUST ignore, verifier
detects (F26/L47). Metadata encoding ≥ 0x80: **ignore-record, and no violation**
— the one enum space where an unassigned value does not reject a scope; encoding
0 and 3–0x7F are ignore-record *and* violations (R1). **Serves: everything but
the ignored record.**

**(5) Truncated tail.** Two shapes. (a) Physical file shorter or longer than
`committed_file_length` → F17, reject-file. (b) A torn commit: the physical tail
is not a valid trailer at all → reject-file, and `[R-LIF-05]` forbids scanning
backward. The reader cannot distinguish a torn commit from corruption and is not
asked to; §9.6's deliberate recovery scan is not a reader behavior. **Serves:
nothing.** The prior generation is *recoverable*, not *readable* — a distinction
the document is careful about and I found genuinely load-bearing when coding
step 1 of the append procedure.

**(6) Checksum mismatch.** Five outcomes by structure, and the chain is strictly
ordered: trailer → reject-file (F14); directory → reject-file (F20);
crc_of_crc_array or a segment CRC → **reject-layer** (L37/L38), even though
detection happens at tile use; a stored tile's crc → reject-tile (T1); a
user-metadata extent's crc → **ignore-record** whatever the containing scope
(R2), with a SHOULD-report. **Serves:** everything outside the failed scope —
and never fill in place of a rejected tile (`[R-TYP-09]`, `[R-CNF-09]`). That
last is the rule that makes sparseness safe: fill is produced by exactly one
condition, a sentinel entry read from a verified chain.

**(7) Limit exceeded.** A file exceeding a §21.9 minimum guarantee stays
conforming; the reader MAY decline it at the whole file or at the narrowest
scope whose *declarations* exceed what it can serve — a layer or a tile — and
MUST report the refusal as a resource limit, never as a validity error. A
user-metadata document is the odd case: it has no declared size, so a
resource-decline has no narrower scope and lands on the whole file, while
ignore-record remains available at the record. Software that declines *on that
ground* a file entirely within the table is not a conforming reader.

**(8) Format major it does not implement.** Reject-file, and the diagnostic
SHOULD be distinct from both "not a TARN file" and "corrupt". The file is
neither conforming nor nonconforming under this text; a verifier reports *cannot
establish*, not *nonconforming*. Only four register rows reach such a file, and
§21.2's preamble names them: F8 and F1's trailer-magic instance, F14, and F6
with F1's front-block instance — the fields `[R-CNT-24]` fixes across every
major. I checked that the four are the right four: F15 (reserved bytes at
[56,60)) and F13 (F ≡ 0 mod 64) correctly do **not** appear, because a future
major may redefine those 48 bytes and the alignment is not among `[R-CNT-24]`'s
permanent guarantees. That preamble is carefully right.

---

## 8. The four flagged passages

### §21.2

I re-derived the preamble's arithmetic and its capability argument (above), and
mechanically counted the table: 36 rows, 58 instances. I checked F33's claim
that "a claimant reaching the front signature block or the live trailer is
instead caught by the bounds rows F9/F10, F31/F32, L16/L17 and T8/T9" against
the four claimant kinds §9.7 enumerates — directory, non-layer top-level record
extents, layer/sub-record extents, stored-tile extents — and the list is
complete, one low-bound row and one high-bound row each. I checked the
specialization claims (F1 of F6 and of F8, F35 of F36) and they hold. I found
nothing wrong in §21.2.

### §21.5

10 rows, 48 instances, counted mechanically. I walked the quarantine boundary,
which is the passage's real content: framing failures (extent slot, extent
length floor, `inline_length ≠ 1`) take the **containing** scope and live in
§21.2/§21.3 (F21/F22/F23, L10/L11/L12); everything from the encoding byte's
value inward takes **ignore-record** and lives here. `[R-CNT-25]` draws the line
at "once its framing has been read", and `[R-MTA-02]` says the same thing from
the other side; the two agree and R1's placement in §21.5 follows.

I checked R4's 16 instances against the constraint list §18.2 carries over from
`[R-COD-06]` — magic, no skippable frame, no second frame, no nonzero dictionary
ID, no content-checksum flag, no trailing bytes, content-size in both directions
— and against the two it expressly does *not* register (undisclosed dictionary
use, the buffer-sizing bar). The list closes exactly. I also checked the two
exceptions §18.2 declares against `[R-COD-06]`'s text word for word: the tile's
declared decoded size (replaced by the decoded document's byte length) and the
frame's declared `Window_Size` (left to the reader's own bound). Both
replacements are stated, and the last sentence — "Any violation here is
ignore-record, never the tile-scope outcome §17.2 assigns" — closes the outcome
question the transposition would otherwise leave open. I found nothing wrong in
§21.5.

One thing I noticed and decided *not* to report: R4's own gloss says "a reader
that only tries decoding establishes none of them", which is not quite true of
the content-size instance — a reader that decodes and compares lengths does
establish it, and many zstd decoders will instead error out and route the same
file to R3. But R3 and R4 share outcome, detector and detection point, so no
reader behavior and no verifier verdict turns on the routing; only a vector's
manifest line does, and §24 already tells a corpus author to record every row a
file exercises. Not a defect.

### §20.5

Walked the compactor as an implementer. The rules that actually bind:

- output = live committed state less any record §20.4 licenses dropping;
- refuse if any `[R-WRT-09]` check fails; never emit a file carrying a violation
  it has **detected**; correcting is barred by `[R-WRT-05]`, so dropping (where
  licensed) or refusing are the only disposals;
- fresh `file_id` — a *draw*, not a comparison — and generation 1;
- carry the input's unknown ignore-lane bits into the output trailer;
- preserve content, preserve no placement; regenerate each relocated tile-index
  region (offsets new; lengths, crcs and sentinels unchanged; segment CRCs
  recomputed) and update `crc_of_crc_array`;
- refuse outright on any unimplemented MU = 1 record type.

I checked the passage's row arithmetic: "F36 and L25 for a record type, and one
row for each of the other seven spaces §10.2 tabulates (L31, L33, L34, L36, L43,
L45, R1)". §10.2 tabulates eight spaces; minus record type leaves seven, and the
mapping is exactly channel layout → L36, linearization → L33, sample type →
L34, codec → L43, filter → L45, index encoding → L31, metadata encoding → R1.
Seven rows, correct.

I also checked the passage's claim that on a *conforming* input only two of
§10.1's four vehicles can reach the compactor — and it holds, because every
reserved-range value in the other six enum spaces is a **reader**-detected row
that `[R-WRT-09]`'s obliged §19.3 layer validation (or the open, for R1) forces
the compactor to meet, at which point `[R-WRT-06]` obliges refusal.

The one thing I could not resolve is reader-02 below.

### §21.7

The passage I spent most on, since it is the one whose enumerations are load-
bearing. I walked every requirement identifier in the document and asked
whether it has a register row, and if not, whether §21.7 accounts for it.

Accounted for and correct: `[R-LIF-01]`/`[R-LIF-03]` (history), `[R-CNT-13]`'s
no-embedded-offsets rule, `[R-CNT-18]`'s nesting prohibition, `[R-COD-10]`'s
mis-stride, `[R-COD-06]`'s undisclosed dictionary, `[R-MTA-09]`'s document
analogue, §20.3 step 4's bar, `[R-WRT-06]`'s four trailer obligations,
`[R-ENC-06]`'s field widths. Accounted for **elsewhere**, correctly, with the
document saying so in each place: `[R-SLB-04]`'s stale slab declaration (its own
Note), `[R-LIF-04]`'s untruncated residue (§9.5's Note), `[R-CNT-05]`'s
over-long pre-trailer gap and `[R-CNT-08]`'s flags = 0 against a set ignore-lane
bit (both declared non-violations by `[R-CNF-02]`), `[R-MTA-06]`'s registry-
version targeting (conduct, §2.3).

I verified §21.7's account of §20.3 step 4 item by item against the bar's own
list — padding-position set and content → T4/T5; decoded size → T3/T14; codec →
sometimes; filter and sample offset → T26's terms; supersede-everything →
unwitnessed. It closes.

I verified the first paragraph's claim that the only structurally constrained
decoded content is "padding positions, pad bits, and boolean bytes" against §14
in full — `[R-SER-03]` says every bit pattern of a packed plane's value region
decodes, `[R-TYP-05]` says every bit pattern is a valid sample value — and it
is complete.

Two things did not close: reader-01 and reader-04 below.

---

## 9. Findings

### reader-01 — OBSERVATION
**§21.7, `[R-ERR-01]`; §11.4 `[R-GEO-06]`; §21.4 rows T3, T14**

**Quotation.**

> the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a
> structurally valid tile whatever values it carries, except where §14
> constrains a byte's content — a padding position, a pad bit, or an
> interleaved boolean — and a mis-ordered image is then witnessed by T2, T4 or
> T5, exactly as a mis-strided filter is

§21.7's whole office is to say what has no witness, and §21.1 introduces it as
"the account, by class, of what fails [detectability]". This sentence's
"except" clause names exactly one route by which a violation of the ordinal
mappings can become visible in a file: a byte whose content §14 constrains,
witnessed by T2, T4 or T5 — three **verifier** rows. There is a second route,
and it is a **reader** row.

`[R-GEO-06]`'s disk tile ordinal is `s` interleaved and `c·N + s` planar. In a
**planar** layer, a tile's decoded size is a function of *which channel's block*
its disk ordinal falls in: `P·Bᶜ` for a numeric channel, `⌈P/8⌉` for a bool
channel (§14.2, §14.3). Where two channels have unequal decoded sizes, a writer
that mis-maps a plane across channel blocks produces a tile whose decoded
payload length is not the decoded size the reader derives from the layer's
declarations — which is T3, or under codec 1 T14, both reader-detected at tile
use, both reject-tile.

Worked instance. Planar layer, `d = 1`, dimension `x` with `E = 4`, `T = 4`, so
`G = 1`, `N = 1`, `P = 4`. Channels `a` (uint8, `B = 1`) and `b` (uint32,
`B = 4`); `C·N = 2` addressed tiles. Disk ordinal 0 is channel 0's plane,
decoded size `P·B⁰ = 4`; disk ordinal 1 is channel 1's plane, decoded size
`P·B¹ = 16`. A writer that swaps them emits entry 0 addressing 16 bytes and
entry 1 addressing 4. Under codec 1 the reader compares the entry's length
against 4 and 16 respectively and rejects both tiles under T14, before any
payload fetch; under codecs 2–4 it rejects them under T3 after decoding.
`E == T`, so there is **no padding position**; there is no bool channel, so no
pad bit and no interleaved boolean. Not one byte's content is constrained by
§14 anywhere in this layer, and yet the violation is witnessed — by the reader,
not the verifier.

The document knows this witness class and applies it correctly one paragraph
later, for a different rule: "A change reaching the decoded size is witnessed by
T3 or T14, which test a length rather than the decoded image's content". The
account of `[R-GEO-06]` does not carry it over.

**What I picked, and what an implementer does wrong without it.** I treated
§21.7 as descriptively wrong here and implemented T3/T14 as mandatory reader
checks regardless, which the register requires anyway. The cost of the omission
falls on someone reasoning *from* §21.7: a verifier author or a corpus author
who takes the passage at its word will conclude that a mis-mapped disk ordinal
has no witness outside the three content rows, and will not realise that in a
planar layer with heterogeneous channel types the mapping is partially
enforced — that a `[R-GEO-06]` violation there is not merely detectable but
detectable by an *ordinary reader*, at tile use, with no decode of content at
all. That is the opposite conclusion from the one the passage supports, and it
is the failure mode a register's negative-space section exists to prevent.

**Byte-level: no.** T3 and T14 are already register rows with reader detectors
and reject-tile outcomes; a conforming reader rejects these tiles whichever way
§21.7 is written, and no writer's emittable set moves. What changes is the
document's account of its own coverage.

---

### reader-02 — AMBIGUITY
**§20.5, `[R-WRT-06]`**

**Quotation.**

> Where the output carries a feature a later minor defines and this compactor
> does not — on a conforming input a carried ignore-lane bit (§6.3) or an
> unrecognized `tarn.` key in a record it never decoded (§18.3), the two of
> §10.1's four vehicles §21.6 makes conforming […] — the output's
> version_minor SHOULD be at least the input's

The rule's antecedent is a fact about the input. For the first of its two named
cases the compactor can establish that fact: it reads the trailer, and a set
ignore-lane bit is right there. For the second it cannot — the clause says so in
the same breath: *"an unrecognized `tarn.` key in a record it never decoded"*. A
compactor's verification depth is `[R-WRT-09]`'s, which reaches "each relocated
extent's checksum" and no further; §20.5 relies on that elsewhere ("No other
record payload carries a file offset"). So the compactor carries a
user-metadata extent forward as opaque bytes and has no way to know whether the
document inside carries a `tarn.` key later minors register.

Permitted readings:

- **(a) Conservative.** Because the antecedent may hold undetectably, a
  compactor SHOULD always emit `max(`[R-CNT-26]`'s floor, the input's minor)`
  whenever the input carries any user-metadata record it did not decode. This
  makes the rule discharge-able but silently converts it into "never lower the
  minor", which is a materially stronger rule than the text states and which
  the "Otherwise version_minor follows `[R-CNT-26]`'s floor" sentence appears
  to contradict.
- **(b) Literal.** The SHOULD binds only where the compactor has in fact
  established the antecedent. Since it never decodes documents, the `tarn.` key
  case never triggers, and the clause naming it is inert — which cannot be the
  intent, since the clause is there precisely to name it.
- **(c) Decode-to-check.** The compactor decodes each user-metadata document to
  look for unrecognized `tarn.` keys. Nothing licenses this: `[R-WRT-09]` bounds
  verification depth, and `[R-MTA-02]` quarantines the document from
  structural interpretation.

I picked (a) and made my compactor take the input's minor whenever the input
carried any user-metadata record, floor otherwise — but I want to record that I
guessed. The parallel obligation for ignore-lane bits is a **MUST** and is
evaluable; this one is a SHOULD whose antecedent is, for half its stated scope,
not.

**What an implementer does wrong without it.** Two conforming compactors given
the same input emit different `version_minor` values in the output trailer, and
each can defend itself from this paragraph. Downstream tooling reading the minor
as a feature floor — the exact use §20.5 and `[R-CNT-26]` both name — gets
different answers for the same content.

**Byte-level: no.** The clause is a SHOULD. `[R-CNF-12]` places SHOULD deviation
outside §21's register entirely and makes it not a violation, so both outputs are
conforming files and `[R-CNF-05]` gates emission on file conformance only. The
bytes at trailer offset [10,12) differ between the two readings, but neither
reading makes a file a conforming writer may not emit.

---

### reader-03 — OBSERVATION
**§2.3 `[R-CNF-03]`; §21.6 closing paragraphs; §7.4 `[R-CNT-18]`**

**Quotation.**

> A reader MUST accept every conforming file of a format major version it
> implements, carrying no record of a type it does not implement with
> MUST_UNDERSTAND = 1

against §21.6:

> The qualifier is load-bearing — the same type as a layer sub-record is
> reject-layer and never a ground to refuse the file (`[R-CNT-18]`), so only
> the top-level case is a file a reader refuses

`[R-CNF-03]` defines the acceptance duty by carving out conforming files that
carry an unimplemented MU = 1 record — with no scope qualifier. §21.6, which
`[R-CNF-03]` itself points at ("§21.6's closing paragraph names the other two"),
says the qualifier "top-level" is load-bearing and that the sub-record case is
"never a ground to refuse the file". So the carve-out is written one scope wider
than the condition it exists to accommodate: a conforming file whose *only*
unimplemented MU = 1 record is an experimental-range **layer sub-record** falls
outside `[R-CNF-03]`'s acceptance duty on the literal text, while §21.6 and
`[R-CNT-18]` say a reader must serve it.

Readings and the one I picked:

- **(a)** The carve-out is scoped as written, so a reader has no duty to accept
  such a file and may refuse it whole.
- **(b)** The carve-out silently inherits the top-level qualifier from
  `[R-CNT-15]`, whose MU rule it is describing, and `[R-CNT-18]` governs the
  sub-record case.

I picked (b), because `[R-CNT-18]` is not merely a permission but an explicit
prohibition — "where the file is otherwise conforming a reader MUST NOT reject
the file for it" — and a carve-out from a duty is not a licence to do a thing
another rule forbids. §21.1's "where a row and the rule it cites diverge, the
rule governs" points the same way, and §21.6's own text is unambiguous.

**What an implementer does wrong without it.** A reader author who implements
from §2.3's conformance-class definitions alone — which is where an implementer
naturally starts, and which §1 recommends reading first — will build the
acceptance predicate from `[R-CNF-03]`'s sentence and will not learn until §7.4
that a whole class of files it excludes must in fact be served, minus one layer.
The cost is a reader that refuses files it must accept, in the one direction
`[R-RDR-02]`'s rationale says divergence must never go.

**Byte-level: no.** `[R-CNT-18]`'s MUST NOT settles the verdict; the two
readings do not both survive contact with it, so two competent implementations
have no defensible disagreement about accept/reject once they have read §7.4.

---

### reader-04 — OBSERVATION
**§21.7 `[R-ERR-01]`; §6.3 `[R-CNT-08]`**

**Quotation.**

> §20.5's four obligations on a compacted file's trailer (`[R-WRT-06]`) — its
> fresh `file_id` draw, its generation, the unknown ignore-lane bits it MUST
> carry forward, and the floor its version_minor SHOULD take — are unwitnessed
> for a reason all four share: the output carries no record that it is a
> compaction output at all, so no check can know that any of the four was owed.

§21.7 goes to the trouble of enumerating the compactor's ignore-lane
carry-forward obligation among the unwitnessed ones, and gives a reason specific
to compaction. `[R-CNT-08]` places the **identical** obligation on an ordinary
updater — "An updater MUST copy forward unknown ignore-lane bits of the file it
modifies and MUST NOT clear them" — and §20.3 step 6 repeats it as part of the
append procedure. That obligation is nowhere accounted for: not in §21.7, not by
a local Note the way `[R-SLB-04]`'s and `[R-LIF-04]`'s are, and it has no
register row.

It is genuinely unwitnessed, for a reason §21.7 does not supply and which its
stated reason positively obstructs. The compactor's case rests on "the output
carries no record that it is a compaction output at all". An append output
*does* carry a record that it is an append output: `generation > 1`. The reason
it is still unwitnessed is different — the prior generation's trailer is slack,
and §9.7's coverage walk reaches only the live state, so the value the new
trailer's flags were supposed to be copied *from* is not reachable from the file
a verifier is given. That is the argument, and the document never makes it here.

The same gap covers `[R-LIF-02]`'s ordering and barriers, `[R-WRT-05]`'s
byte-identical re-emission, `[R-WRT-07]`'s reference-array preservation, and
`[R-WRT-08]`'s bar on re-encoding — all obligations on an output file's bytes,
all unwitnessed, none accounted for. I list `[R-CNT-08]` as the finding because
it is the one whose omission is conspicuous: the same obligation, one actor
over, on the same four bytes of the same structure, named for the compactor and
not for the appender.

**What I picked, and what an implementer does wrong without it.** I concluded
the appender's obligation is unwitnessed and carried the bits forward anyway. A
verifier author reasoning by analogy from §21.7's stated reason will conclude the
opposite: that because a generation counter *does* record the append, an
ignore-lane bit cleared by an appender is something a verifier could look for.
It cannot, and it would waste a check discovering that. That is precisely
concluding "a witness exists where none does".

I record honestly that §21.1 does **not** make §21.7 complete — "neither this
completeness clause nor the instance arithmetic below reaches §21.6's defined
non-violations, §21.7's account of what no check detects, or §21.9's limits" —
so this is an incompleteness in a passage whose completeness is not normative,
and I grade it accordingly. It is reportable because §21.7's chosen granularity
(four sub-obligations of one rule, each with its reason) sets an expectation its
own text then breaks.

**Byte-level: no.** `[R-CNT-08]` states the updater's obligation plainly; §21.7's
silence licenses nothing and changes no accept/reject verdict, since neither
reading gives a verifier anything to check.

---

## 10. What I could not determine, and what I am confident about

**Confident.** An implementation built from this document alone would
interoperate on the reader path. I built a real file and read it back without
guessing once, and every constant, offset and checksum I could check was right —
including the two that would have been silent traps (`0xEECB3BB2` and Appendix
A's trailer CRC). The register's own arithmetic is exact to the instance. The
capability/violation boundary — foreign major, unimplemented MU = 1 type,
resource decline, unassigned metadata encoding — is drawn consistently in §2.3,
§21.6, §21.9 and Appendix H, and I could route every degradation walk without
ambiguity.

**Not determined.** Only reader-02: whether a compactor is expected to take the
input's `version_minor` whenever it carries user-metadata it did not read. I
guessed conservative.

**Things I suspected and cleared.** T26's omission of T5 (correct — the shuffle
fixes the final byte, so pad bits are stride-invariant); R8's two instances
(defensible under §21.1's "alike"); §21.2's four-row capability list (exactly
right, and F13/F15 correctly excluded); `[R-COD-06]`'s Window_Size derivation
note (correct against RFC 8878's 1 KiB Window_Descriptor floor); §20.5's seven
enum-space rows (L31, L33, L34, L36, L43, L45, R1 — exactly the seven non-
record-type spaces §10.2 tabulates); F33's bounds-row list (complete over all
four claimant kinds).
