# Round 22 — Reader implementer, working transcript

Access: I read `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` and nothing
else. I ran `wc -l` on it and `grep` against it. Every other command I ran was Python
over files I wrote myself in my own scratch directory (`crc.py`, `build.py`,
`reader.py`, `two.tarn`). I did not open `docs/`, `conformance/`, `PLAN.md`,
`AGENTS.md`, `README.md`, `spec/registry.json`, or any git history, and I did not
list the output directory. Context I did not ask for did appear before I began: a
project-instruction pointer and an index of the maintainer's memory files naming
prior rounds and prior findings. I disregarded it; nothing below is traceable to it,
and I have not repeated its contents.

---

## 0. Method

I wrote the reader in the order I would actually write the code: constants and CRC
first, then the open path, then layer access, then the tile read, then degradation.
I stopped at every point where the text did not tell me what to do, and I built an
actual file and ran an actual reader over it rather than reasoning about one.

---

## 1. Constants and the checksum (§4.5, Appendix B)

The first thing a reader needs is a working CRC-32C. §4.5 pins it completely:
polynomial 0x1EDC6F41 (RFC 3720 §12.1), reflected in and out, init 0xFFFFFFFF, final
XOR 0xFFFFFFFF, stored little-endian. That is the ordinary Castagnoli-reflected
formulation with reflected table constant 0x82F63B78. §4.5's check vector gives me a
self-test before I touch a file:

```
CRC-32C("123456789") = 0xE3069283   -> my implementation: 0xE3069283   OK
CRC-32C(zero bytes)  = 0x00000000   -> my implementation: 0x00000000   OK
```

Both reproduce. Every other stated checksum in the document is then checkable, and I
checked all four I could reach:

| Stated in | Constant | Computed |
|---|---|---|
| §7.4 example | CRC over 80 bytes = four sentinel entries: `0x80A34955`, stored `55 49 A3 80` | `0x80A34955` — matches |
| §7.4 example | crc_of_crc_array over that 4-byte array: `0xC4EE982E` | `0xC4EE982E` — matches |
| §15.4 `[R-IDX-05]` | CRC of a full 2^16-entry all-sentinel segment: `0xEECB3BB2` | `0xEECB3BB2` — matches |
| Appendix A | trailer CRC-32C over trailer bytes [0,60): `0xE00938D2`, stored `D2 38 09 E0` | `0xE00938D2` — matches |

No stated constant, offset or checksum in this document is wrong as far as I can
compute it. That includes the whole of Appendix A: I parsed its hex dump as bytes,
found length exactly 128, trailer at [64,128), version_major 1, version_minor 0,
flags 0, generation 1, dir_offset 16, dir_length 4, committed_file_length 128,
file_id 0x0123456789ABCDEF, reserved zero, and the directory region [16,20) holding
`00 00 00 00` = CRC-32C of zero bytes. Every annotation row in the table is correct
and the file passes every gate of `[R-CNT-06]`.

I also checked the two arithmetic self-statements that a corpus builder would rely
on. §21.2/§21.3/§21.4/§21.5 declare 36 + 49 + 26 + 10 = 121 conditions; the tables
contain exactly 36 F-rows, 49 L-rows, 26 T-rows and 10 R-rows. §21.8 declares "121
conditions over 273 instances"; applying §21.1's mechanical rule (a cell reading
`—` is one instance, otherwise instances are semicolon-separated) I count
58 + 116 + 55 + 44 = **273**. Both figures are exact.

## 2. The open path, byte by byte (§19.1, §6.1–§6.4)

### 2.1 What a cold remote open costs

Two requests. Byte-exactly:

1. **Request 1 — suffix range, 64 bytes.** §19.1 step 1 wants the
   transport-authoritative size F (`[R-CNT-10]`); §6.4 says a suffix range's response
   carries F in its own headers, so steps 1 and 2 cost one request between them. What
   bounds this range before I have read anything: nothing but the constant 64 — that
   is the point of a fixed-size trailer, and it is the only read in the whole reader
   that is not bounded by a checksum-verified field. §21.9's floor of 128 bytes
   (`[R-CNT-27]`, F5) is what stops the range from being ill-formed.
2. **Request 2 — `[dir_offset, dir_offset + dir_length)`, exactly `dir_length`
   bytes.** Bounded, before I read it, by: dir_offset >= 16, dir_length >= 4,
   dir_offset + dir_length <= F - 64, and the overflow rule `[R-ENC-04]` — all four
   read out of the trailer, all four covered by the trailer CRC I have already
   verified, so `[R-ENC-05]`'s "allocate, seek, or issue I/O only after the covering
   checksum verifies" holds. §21.9 guarantees dir_length up to 16 MiB, which is the
   number a reader sizes its buffer against.

Total: **2 requests, 64 + dir_length bytes**. On Appendix A's file that is
64 + 4 = 68 bytes. On the two-layer file I built below it is 64 + 231 = 295 bytes.
The `[R-RDR-01]` invariant holds in both: the open's working set is the trailer and
the directory, at any file size and layer count. §6.4's speculative-suffix variant
collapses this to one request when the fetched window contains the directory region;
Appendix A's own note that a 112-byte window over [16,128) suffices while leaving
[0,16) non-resident is correct and is the case that makes the residency test of
`[R-CNT-04]` bite differently from the transport test.

The front block is **not** in that accounting. `[R-CNT-04]` makes the obligation turn
on residency, not transport: resident -> MUST verify by byte equality before other
processing (reject-file on mismatch); would need a further range request -> MAY defer
or omit. My local reader reads the whole file, so [0,16) is resident and I check it
first. My remote reader with exact ranges never holds it and skips it. Both
conforming. A verifier holds no such exemption (§2.3; F6's Instances cell says so).

### 2.2 Trailer validation, in §6.2's fixed order

I implemented exactly the stated order, because §6.2 makes it an *ordered*
validation and §21.2's preamble makes the order load-bearing for which rows reach a
foreign-major file:

```
magic at [F-64, F-56)  == 8A 4E 52 41 54 0D 0A 1A          else F8   (F1 byte-reversed)
u32 at trailer[60,64)  == CRC-32C(trailer[0,60))           else F14
version_major != 0                                          else F18
version_major == 1 (a major I implement)                     else capability refusal, not a finding
--- gates passed; now the rest, before acting on any of them ---
flags & 0xFFFF == 0                                          else F19   (ignore lane 16-31: ignored)
committed_file_length == transport size                      else F17
committed_file_length % 64 == 0                              else F13
dir_offset >= 16                                             else F9
dir_length >= 4                                              else F16
dir_offset + dir_length <= F - 64                            else F10
1 <= generation <= 2^63-1                                    else F11 / F2
file_id != 0                                                 else F12
trailer[56,60) all zero                                      else F15
every u64 field <= 2^63-1                                    else F2; sums checked   F3
physical size >= 128                                         else F5
```

One thing worth writing down because it is easy to get wrong and the document gets
it right: **F in step 2 is the transport size, not the trailer's own
committed_file_length.** §19.1 step 1 says so ("Obtain the transport-authoritative
file size F"), and `[R-CNT-10]` forbids substituting the trailer's field for the
transport size. A reader that located the trailer at committed_file_length - 64 would
read a stale trailer out of the middle of a file whose commit is in flight. The
document's own crash figure in §9.2 is the picture of exactly that state, and
`[R-LIF-05]` forbids the backward scan that would rescue it. `file_id` is not an
"offset, length, extent, or count" and so is *not* subject to `[R-ENC-03]`'s
2^63 - 1 ceiling — Appendix G item 2, which derives it from a hash's last eight
bytes read little-endian, confirms that reading, and my reader accepts a file_id with
bit 63 set.

### 2.3 Directory and record walk

Verify the terminal 4 bytes against CRC-32C of the preceding dir_length - 4 bytes
(`[R-CNT-11]`, F20) **before any other use**. The record sequence is the covered
bytes; its end is dir_offset + dir_length - 4, which is exactly what F29 names.

Then the walk. Per record: 24-byte header, then inline_length bytes. type 0 -> F24
(never treated as unknown). Header or payload past the sequence end, or residue after
the last complete record -> F29. Unknown top-level type: MU=1 -> reject-file (F35 for
a reserved-range value; an experimental-range value with MU=1 is a *conforming file a
reader refuses*, §21.6, and is not a register row); MU=0 -> ignore-record. Two
top-level user-metadata records -> F34. Non-layer extent slots checked here: half-zero
-> F30, offset in 1..15 -> F31, past F-64 -> F32, out of domain -> F2/F3. Top-level
user-metadata framing checked here too: (0,0) slot -> F21, extent_length < 5 -> F22,
inline_length != 1 -> F23, encoding byte 0 or reserved -> R1 at *open*.

Then the layer-name namespace. §19.1 step 4 is unusually careful here and I followed
it literally: uniqueness is decided **first**, over **raw name bytes**, whether or not
each name is well-formed, because `[R-ENC-13]` makes name comparison a byte
comparison that needs no valid name. A layer record whose name field does not lie
within its own inline_length yields no name field, contributes nothing to the
namespace, and is reject-layer (`[R-CNT-18]`, L23) rather than a file-scope error.
Duplicate -> F4 reject-file, at open. Ill-formed UTF-8 / empty / C0 control in a layer
*record's* name -> L3/L5/L6, reject-layer, also at open. My reader implements all of
that and it is unambiguous.

**Cross-check I ran on §19.1 and §19.3.** For every reader-detected row in §21.2 I
confirmed there is a step of §19.1 that reaches it, and for every reader-detected
layer-scope row in §21.3 marked *layer access* I confirmed it is decidable without
I/O — because `[R-RDR-03]` claims exactly that ("layer access performs no fetch").
All of L1, L2, L4, L7-L17, L19-L36, L39, L43-L45 are decidable from the resident
directory and F. The only reader-detected L-rows that need I/O are L37 and L38, and
both are marked *tile use*, which is where §19.2 puts index-chain failures while
keeping their scope at the layer (`[R-IDX-04]`). The claim holds.

## 3. Validation timing by tier (§19.2)

What I built, and what a reader is permitted never to do:

- **At open** — front block (only if resident), trailer, directory region and its
  record walk, the layer-name namespace. Nothing else. No extent is fetched, so no
  extent CRC and no document rule is due here.
- **At first access to a layer** — the whole of `[R-RDR-03]`'s list, before any use of
  the layer's declarations other than its name. Failure takes each cited rule's scope.
- **At use of a tile** — the index chain (crc_of_crc_array, then the segment CRC),
  the entry classification, the payload CRC, the decode. Index-chain failure takes
  *layer* scope though it is detected at tile use.
- **At use of a record's extent** — that extent's CRC, and the document content rules
  §18.2 attaches at its encoding.
- **Never** — anything whose assigned detector is the verifier: extent overlap
  (F33, L18), coverage and the slack total (§9.7), the pre-trailer gap (F7),
  alignment and slab invariants (L40-L42), reserved flag bits and MU=1/PE=0 (F25,
  F26, L46, L47), a registered type's stored flag bits (F28, L49), reserved-range
  type values as such (F36, L25), padding content and pad bits and interleaved
  boolean bytes (T2, T4, T5), mis-strided filters (T26), unsorted metadata members
  (F27, L48). A conforming reader that detects any of these MAY reject the file
  (`[R-CNF-12]`) but owes nothing.

Detection may always move *earlier* and never later; divergence is only ever toward
earlier rejection. That is the property that lets me implement a strict reader and a
lazy reader from the same text and have both be conforming.

## 4. A file I built, and my reader run over it

I wrote a builder and a reader and ran them. First I reproduced §7.4's worked layer
record payload from the field table alone, without copying its dump, and compared:

```
03 73 73 74 01 01 00 01 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 01 01 00 01 78 64 00 00 00 00 00 00 00 20 00
00 00 00 00 00 00 04 74 65 6d 70 0c 00 04 00 00 c0 7f 01 04 00 00 00 00 00
00 00 2e 98 ee c4                                                (81 bytes)
```

Byte for byte identical to §7.4's example, including the field arithmetic it states
(4 + 34 for the name and the nine scalars, 18 for the dimension entry, 12 for the
channel entry, 13 for the trailing fixed fields = 81), the entry_count 4 = ceil(100/32),
the extent length 4*20 + ceil(4/2^16)*4 = 84, and both CRCs. I take the example as
verified.

Then I built a **two-layer file** of my own, 448 bytes:

```
[0,16)     front signature block
[16,34)    layer 'm' stored tile, 18 bytes, codec 1, filter 2 (byte-shuffle)
[34,118)   layer 'sst' tile-index region, 84 bytes, four sentinels + one segment CRC
[118,142)  layer 'm' tile-index region, 24 bytes, one entry + one segment CRC
[142,373)  directory: two layer records + terminal CRC, dir_length = 231
[373,384)  pre-trailer pad, 11 bytes (step 5 of [R-LIF-02] pads to the next 64)
[384,448)  trailer, generation 1, committed_file_length 448
```

Layer `m`: interleaved, dims (y,x) extents (2,3) tile extents (2,3), so
G = (1,1), N = 1, P = 6; channels `a` uint8 fill 0x00 and `b` uint16 fill 0xABCD, so
Q = 3 and the decoded size is P*Q = 18. Filter 2 at stride s = Q = 3 with
n = L/s = 6:

```
decoded image : 00 00 10 01 01 10 02 02 10 03 03 10 04 04 10 05 05 10
filtered      : 00 01 02 03 04 05 00 01 02 03 04 05 10 10 10 10 10 10
```

which is `[R-COD-10]`'s "byte i of group j at offset i*n + j" and inverts exactly.
Codec 1, so `[R-COD-04]` obliges entry length == 18, which it is.

My reader, running cold:

```
trailer ok: gen=1 dir=[142,373) F=448 file_id=0x123456789abcdef
open complete: 2 requests, 295 bytes: [(384,448), (142,373)]
layers: ['sst', 'm']
layer sst  layout=1 codec=1 filter=1 G=[4]   N=4 P=32 ec=4 region=[34,118)
layer m    layout=1 codec=1 filter=2 G=[1,1] N=1 P=6  ec=1 region=[118,142)
sst @ x=0   -> [('fill', 00 00 c0 7f)]                     # the recorded quiet NaN, bit-exact
m @ (0,0)   -> [('stored', 00), ('stored', 00 10)]
m @ (1,2)   -> [('stored', 05), ('stored', 05 10)]
m @ (0,2)   -> [('stored', 02), ('stored', 02 10)]
m @ (2,0)   -> out of extents: request fails, no verdict on file
```

Every number in that run is derived from the document with no guessing: the ordinals
from `[R-GEO-06]`, the in-sample offsets from `[R-SER-02]`'s
`(k div C)*Q + F_{k mod C}`, the fill from `[R-TYP-06]`/`[R-TYP-08]`, and the
out-of-extents disposition from `[R-MDL-01]`/§21.6 (the request fails as a request,
with no verdict on the file).

I also confirmed the ordinal arithmetic against §11.4's own example independently:
tile(1,0) -> s = 8; (300,700) -> tile (1,2), s = 10, in-tile (44,188), in-tile
ordinal 44*256 + 188 = 11452; planar C=4 -> disk ordinal 2*32 + 10 = 74, whose entry
sits at region bytes [1480,1500). §15.4's large example is right too: entry_count
1,000,000 gives 16 segments (15 full + 16,960), a 64-byte CRC array, a region of
20,000,064 bytes, segment 15 at [19,660,800, 20,000,000) and entry 999,999 at
segment-relative byte 339,180.

## 5. Layer access and the tile read (§19.3, §19.4)

The parse of the layer record's inline payload is fully determined, and one detail is
worth recording because it is the only place where a field's *length* depends on
another field's *value*: the channel entry's fill is a u8 length prefix followed by
that many bytes, and §7.4 says explicitly "fill parses without type knowledge and
validates with it". So the parser advances on the stored prefix and only afterwards
cross-checks the prefix against the declared type's element size (L30). That ordering
matters, because a layer whose channel type is unassigned (L34) still has to be
*parsed* far enough to report a single well-scoped reject-layer rather than a parse
crash.

The chain of trust I implemented, in §8.2's order, with the range each link bounds:

```
trailer CRC          -> bounds the directory fetch          [dir_offset, +dir_length)
directory CRC        -> bounds each layer record's extent   [extent_offset, +extent_length)
                        and every declaration in it
crc_of_crc_array     -> bounds the segment CRC array        [region + 20*entry_count, +4*nseg)
segment CRC          -> bounds each entry in that segment   [region + 20*k, +20)
entry.crc            -> bounds the stored tile              [offset, +length)
```

Every fetch after the first two is sized from a field that a verified checksum
already covers, which is what `[R-ENC-05]` and `[R-SEC-02]` between them require. The
only field a hostile file can inflate for free is entry_count, and `[R-CNT-17]` ties
it to extent_length while `[R-CNT-13]` ties that to F — so I validate both before I
fetch, and §22.2's note names exactly that path.

Tile read, per needed entry:

1. Domain check (`[R-MDL-01]`); a region request returns the intersection with the
   extents, empty for a zero-extent layer.
2. Ordinals: s interleaved, c*N + s planar (`[R-GEO-06]`).
3. Fetch the whole segment CRC array and the one segment containing the entry, verify
   crc_of_crc_array then the segment CRC (`[R-IDX-04]`); both are reject-**layer**.
4. Classify the entry against §15.3's table. Sentinel (offset = length = 2^64-1,
   crc = 0) short-circuits: fill, no payload I/O. Six *structural* rows reject the
   tile; the seventh (stored bytes fail the crc) also rejects the tile but leaves the
   entry well-formed, which is what keeps it inside slab run continuity and inside
   the coverage walk.
5. Fetch [offset, offset+length), verify against entry.crc.
6. Codec, then the filter's inverse. Length must be exactly the decoded size
   (`[R-SER-07]`), which is a function of declarations alone.
7. Extract by §14's offset arithmetic; padding positions are never returned.
8. Return bit patterns unaltered. On a mixed result the reader MAY return the good
   entries plus a per-entry failure report, or fail the whole request, but MUST NOT
   substitute fill for a rejected tile.

**Decoded byte layout, stated exactly as I implemented it.** Planar numeric channel
c: P * B^c bytes, value k at k * B^c. Planar bool: ceil(P/8) bytes, value k in bit
k mod 8 of byte k div 8, LSB-first, high bits of the last byte being pad bits that
carry the channel's fill bit. Interleaved: P * Q bytes where Q = sum of all channels'
element sizes (bool counting 1), with channel c's value at in-tile ordinal u at byte
u * Q + F^c. §14.2's worked example (Q = 3, size 18, ordinal 5 at [15,18); planar `b`
12 bytes with ordinal 5 at 10-11; float32+bool giving Q = 5, size 30, ordinal 5 at
[25,30)) is arithmetically correct in every part, as is §14.3's `55 01` / `55 FD`
packed example and §14.5's 32-byte edge tile with fifteen `CD AB` padding values.

The byte-shuffle stride rule is complete across every case a reader can meet: element
size for a planar numeric plane, Q for an interleaved tile, and identity (s = 1) for
a packed boolean plane — and L is divisible by s in each, so the inverse is total.

## 6. Degradation walks

**(1) Unknown record type, top level, MU = 0.** Ignore-record. The record is skipped
as though absent; decoding of all stored data is unaffected; its extent is covered by
no checksum at all (§8.1's last row) and I never touch it. I still serve every layer.
If the type is from the reserved range the file is nonconforming (F36) but its
detector is the verifier, so I am not obliged to notice — and if I do notice,
`[R-CNF-12]` lets me reject, which is a licensed divergence, not a defect. If MU = 1
and the type is reserved-range, F35: reject-file, at open. If MU = 1 and the type is
experimental-range, the file is *conforming* and I still refuse it — §21.6's second
"conforming file a reader refuses", and the diagnostic must not say "corrupt".

**(2) Unknown codec value.** Layer A declares codec 5. At A's first access, L43:
reject-layer. I may still list A's name (§2.4). Layer B is untouched and I serve every
tile of it. Nothing about this is file-scope, which is the whole point of the
owning-scope mechanism. The same shape covers an unassigned filter (L45), layout
(L36), linearization (L33), index_encoding (L31) and sample type (L34).

**(3) Unrecognized flag / enum value.** A set ignore-lane bit (16-31) in the trailer:
ignored, file conforming, and if I were an updater I would have to copy it forward.
A set incompat-lane bit (0-15): reject-file, F19, because this text defines no flag
bits so every such bit is one I do not implement. An experimental-range user-metadata
encoding byte (>= 0x80): ignore-record, file conforming, no document rule attaches
(`[R-MTA-10]`) — whereas encoding 0 or a reserved value 3..0x7F is the same
ignore-record but *is* a violation (R1). That three-way split is stated cleanly in
§21.5's preamble and I implemented it directly.

**(4) Truncated tail.** I take the transport size, read the final 64 bytes, and the
magic fails (F8) — or, in the unlucky case that the bytes there happen to be a magic,
the trailer CRC fails (F14), or committed_file_length disagrees with the transport
size (F17). Reject-file. I MUST NOT scan backward (`[R-LIF-05]`); recovery is a
deliberate separate operation and not a reader behavior. I serve nothing. §9.5's note
is right that residue past a completed commit carries no register row of its own and
does not need one — I meet it as one of F8/F14/F17 and cannot tell it from
corruption, and am not asked to.

**(5) Checksum mismatch, at each of the four scopes.** Directory CRC -> reject-file
(F20), nothing served. crc_of_crc_array or a segment CRC -> reject-layer (L37/L38),
detected at tile use, other layers served in full, and the bar on the damaged layer is
prospective so samples already returned stand. A stored tile's crc -> reject-tile
(T1), that tile's read reports failure, neighbours in the same layer unaffected, and
critically I MUST NOT return fill for it (`[R-CNF-09]`, `[R-TYP-09]`). A
user-metadata extent's CRC -> ignore-record (R2), SHOULD report the loss, structural
data completely unaffected. Four different blast radii from one mechanism, and the
document is precise about all four.

**(6) Limit exceeded.** A layer declaring rank 40 exceeds §21.9's guarantee of 32. I
may decline it — at the whole file, or at the narrowest scope whose declarations
exceed what I can serve, here the layer — and I MUST report it as a resource limit
and not as a validity error. The file stays conforming. This is where finding
`reader-01` below bites: for the tile-decoded-size row I had to decide *which* tiles
the row ranges over.

**(7) Format major I do not implement.** version_major = 7: reject-file on capability
grounds (`[R-CNT-07]`), with a diagnostic distinct from both "not a TARN file" and
"corrupt". This refusal is not a finding about the bytes, and only four rows —
F8, F14, F6 and F1's two instances — reach such a file at all, because §6.2 puts the
version gate ahead of everything but the magic and the trailer CRC, and `[R-CNT-04]`
puts the front block ahead of all processing. version_major = 0 is different: it
declares no major at all and is permanently invalid, F18.

## 7. Legal-but-degenerate files I pushed through

- **The 128-byte empty file** (Appendix A). Opens in two requests, layer table empty,
  nothing further to read. Verified byte for byte.
- **A layer with a zero-extent dimension.** G_i = 0, N = 0, addressed-tile count 0,
  entry_count 0, extent slot (0,0), crc_of_crc_array 0, no index region, nothing
  fetched and nothing verified. Every read returns no samples. `[R-COD-07]`'s lz4 cap
  is satisfied whatever the tile shape declares, because it is quantified over
  addressed tiles — while `[R-ENC-04]`'s ceiling on P = product of T_i still applies,
  which §17.2's note states explicitly and which I implemented as two separate checks.
- **A layer that addresses tiles but stores none.** Rank 1, E = 1, T = 2^63 - 1, so
  G = 1, N = 1, P = 2^63 - 1, one uint8 channel, Q = 1, decoded size 2^63 - 1 bytes,
  codec 1, one sentinel entry, a 24-byte index region. The whole file fits in a few
  hundred bytes. Reading x = 0 costs one 24-byte fetch, two CRC verifications, and
  returns fill; I never allocate anything proportional to P. This is the file that
  makes `reader-01` concrete: it exceeds §21.9's 256 MiB decoded-tile row under one
  reading of the new per-instance sentence and does not under the other, and the two
  readings differ on whether I am permitted to refuse it.
- **A single-channel bool layer in both layouts.** ceil(P/8) packed bytes planar
  versus P bytes interleaved; both valid and both required of me (`[R-SER-09]`), and
  the filter is the identity in the planar case and stride-1 in the interleaved case.
- **A non-sentinel entry whose crc field is 0.** Legal — the sentinel test reads
  offset and length, never crc, and CRC-32C(x) = 0 is reachable for some payloads.
  My classifier does not treat crc = 0 as a sentinel marker, which §15.2's
  "Sentinel entries are a reserved pattern" and §15.3's first three rows make
  mandatory.
- **A file_id with bit 63 set.** Legal; `[R-ENC-03]` does not reach it.

## 8. Findings

### reader-01 — AMBIGUITY. §21.9, `[R-ERR-03]`; reaches `[R-CNF-03]` and `[R-ERR-04]`

> The last three rows are **per-instance**: they range over the tiles,
> user-metadata documents and compressed frames a file actually contains, and a file
> containing none of a kind does not exceed that row, whatever its declarations would
> derive — a layer addressing no tile (§11.2) has no tile whose decoded size the
> table can bound, exactly as `[R-COD-07]`'s cap is quantified over a layer's
> *addressed* tiles.

One sentence supplies the quantifier for three rows whose instances are individuated
differently, and for the "decoded size of one tile" row the two halves of the sentence
point opposite ways.

*Reading A — addressed tiles.* The em-dash gloss names the quantifier outright:
"exactly as `[R-COD-07]`'s cap is quantified over a layer's *addressed* tiles". A
layer that addresses tiles therefore has tiles whose decoded size the row bounds,
stored or not. Supporting this: `[R-ERR-04]` measures a decline against "the
narrowest scope whose **declarations** exceed what it can serve", and a tile's decoded
size is a declaration-derived quantity (`[R-SER-07]`: "decoded size is a function of
the layer's declarations alone ... never of payload content").

*Reading B — tiles the file physically holds, i.e. stored tiles.* The governing verb
is "a file actually **contains**", and for the other two rows the sentence covers —
user-metadata documents and compressed frames — "contains" can only mean physically
present, since neither exists except as stored bytes. A reader applying one verb
uniformly across the three rows it governs gets "stored tiles". Supporting this: the
table's stated purpose is what a reader must be able to *accept*, and an unstored tile
asks nothing of a reader — §19.4 step 4 short-circuits it with no payload I/O and no
allocation — so a row that bounds it bounds nothing real.

*What I picked and why.* Reading A. The gloss names the quantifier explicitly, and
`[R-ERR-04]`'s "declarations" corroborates it. My reader treats a layer's declared
decoded tile size as bounded by the row whenever entry_count > 0.

*What an implementer does wrong without it.* Take the degenerate file from §7 above:
rank 1, E = 1, T = 2^63 - 1, one uint8 channel, one sentinel entry, a few hundred
bytes on disk, declared decoded tile size 2^63 - 1. Implementation X reads A,
concludes the file exceeds the 256 MiB row, and — since `[R-CNF-03]`'s acceptance
duty runs only to a conforming file "none of whose values exceeds the minimum
guarantees" — declines the layer (or the file) under `[R-ERR-04]`, reporting a
resource limit. Implementation Y reads B, finds no tile the row can bound, and is
obliged to serve: under Y's reading, X's refusal makes X "not a conforming reader"
(`[R-ERR-04]`: "Software that declines **on that ground** a file whose every quantity
lies within the table is not a conforming reader"). So the two readings disagree
about a verdict on a specific file, and about which of the two implementations is
conforming. The fix costs one word — saying "addressed" (or "stored") in the row's
own terms rather than leaving one verb to serve three differently-individuated rows.

I grade this byte-level because it changes what a conforming reader **must accept**,
and I record honestly that the gloss's analogy is the stronger of the two pulls; a
triage that finds Reading A already decisive is a defensible outcome.

### reader-02 — OBSERVATION. §21.5 row R3's Instances cell, against §18.2 `[R-MTA-09]`

§18.2 states, of a user-metadata document under encoding 2:

> The frame's content-size field, unlike the decoded size and the window, is *not*
> left to the reader: it MAY be present, and when present it MUST equal the byte
> length of the decoded document. A mismatch is a failure to decode within the
> meaning of R3, so that R3's condition stays checkable from the bytes alone rather
> than turning on a decoder's tolerance (`[R-CNF-02]`) — the tile rule of
> `[R-COD-06]` transposed to the quantity a document does have, its decoded length,
> in place of the declared size it does not.

R3 as registered:

> | R3 | A user-metadata document's stored bytes fail to decode under its declared
> assigned encoding — under an experimental-range one this specification defines no
> decoding and §21.6 governs (`[R-MTA-10]`); encoding 0 and a reserved value are
> unassigned too and R1 registers both | top-level extent; layer sub-record extent |
> reader | extent use | `[R-CNT-25]` |

R3's Instances cell enumerates containers only: two instances. §21.1 says an instance
names "a field the condition ranges over, a container it can occur in, **one of
several alternatives the condition text states**, or any combination of the three",
and adds that "Where the condition compares two **magnitudes** either of which can be
the greater — a *differs from* or *does not equal* — the two directions are likewise
enumerated". The content-size rule is precisely a *does not equal* between two
magnitudes, and the tile-side analogue the text names — T22, "the frame's
Frame_Content_Size field is present but does not equal the tile's decoded size" —
enumerates six instances on exactly that basis (three layouts x two directions). The
metadata transposition gets none: R3's cell names no content-size alternative and no
direction, so §21.8's "one vector per instance" and `[R-VEC-03]`'s coverage
obligation generate no vector for a normative MUST whose violation is a
distinguishable, easily constructed file (a valid frame decoding to a 50-byte JSON
object while declaring a Frame_Content_Size of 60).

A defence of the cell as written exists and I state it: §18.2 stipulates the mismatch
*is* "a failure to decode within the meaning of R3", so one could argue R3's condition
does not change shape and the family collapses to a single instance the way T24's
"any codec" does. Against that: T25 enumerates three decode-failure shapes across
codecs, and the reader's check here genuinely differs in kind — comparing a header
field against a produced length is not the same procedure as a decoder aborting.

Not byte-level. The rule is clear, its outcome (ignore-record, SHOULD report) is
clear, and no implementation reading this text would treat the file differently. What
it costs is corpus coverage: a MUST with a defined outcome that §21.8's arithmetic
does not oblige anyone to test, and it also means §21.8's stated total of 273
instances is right about the cells and possibly short about the conditions.

## 9. Places I had to guess, and did not report

For completeness, the decisions I made that the document leaves open by design rather
than by defect:

- **Order of checks within layer access.** Unspecified; every failure is reject-layer,
  so no order is observable. Implementation technique.
- **How a caller names a channel subset.** §19.4 step 2 says "per requested channel c"
  and the closing note says "Channel-subset reads verify only the segments they
  touch", but no request form carries a channel selector. Not a defect: §19.2 settles
  the consequence ("Structures a request never relies on impose no detection
  obligation"), and the API shape is technique, not bytes.
- **The output layout of a region read.** Undefined, deliberately; `[R-MDL-02]` fixes
  only that the values equal the reference array bit-for-bit.
- **Whether a metadata reader may size a buffer from the frame's content-size field.**
  §18.2 transposes `[R-COD-06]`'s "MAY be present" and "MUST equal" but not its
  "a reader MUST NOT allocate or size any buffer from it". I concluded the general
  rule covers it: `[R-SEC-02]` forbids sizing an allocation "in proportion to a
  declared magnitude it has not corroborated against the file's actual length", and a
  content-size field in a short extent is exactly that. Clear enough not to report.
- **"the bound above" in `[R-MTA-09]`'s verifier sentence**, where two bounds (decode
  size, window) were just introduced. §2.3's cannot-establish list generalises it
  ("when it declines to decode a user-metadata document (`[R-MTA-09]`)"), so both
  grounds are covered. Verifier-side and decided elsewhere; not reported.

## 10. Verdict on the charter question

The document sufficed to write the reader. I implemented the open path, the tier
model, layer access, the index chain, the entry classifier, the codec-1 and
byte-shuffle pipeline, the extraction arithmetic and the fill path from this text
alone, ran it against a file I built from the same text, and got the values the
document's own examples predict. Every stated constant, offset and checksum I could
compute is correct, and the register's own arithmetic (121 conditions, 273 instances)
is exact. One quantifier in the newly-changed §21.9 text is the single place where I
believe two competent readers could reach different verdicts on the same file.
