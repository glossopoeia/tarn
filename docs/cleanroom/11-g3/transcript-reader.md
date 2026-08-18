# Cleanroom round 11 — Reader implementer transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,953 lines), via `sed -n` ranges and one `python3` pass over it to count
register rows. I opened no ADR, no `PLAN.md`, no `AGENTS.md`, no
`conformance/` file, no `spec/registry.json`, no prior round's findings. I ran
no `git` command, no web search, no web fetch, and did not list any directory.
I wrote two files, both in my scratchpad: `crc.py` (a self-contained CRC-32C
implementation with no file input) and this transcript.

Local computation performed: CRC-32C of `"123456789"`, of zero bytes, of
Appendix A's trailer bytes [0,60), and of a 2^16-entry all-sentinel index
segment; the instance arithmetic of §21.8; and by hand, every worked numeric
example in §11.2, §11.4, §12.3, §14.2, §14.3, §14.5, §15.4, §16.2, §17.3,
§20.3 and §21.9's note.

I have no prior knowledge of this document from any other source. Where I use
knowledge of other array formats below it is to *generate* a suspicion, never
to settle one.

---

## 0. How I read it

I read the whole document front to back once, then re-read §4.7, §5.2, §6.1,
§6.2, §6.4, §7, §9.7, §14, §15, §17, §19, §20.3, §20.4, §20.5, §21 and
Appendices A, B, G and H while writing the implementation below. I did not
treat the weighted section list as a checklist; I wrote the reader and stopped
where it stopped.

The document is unusually implementable. I want to say that plainly before the
findings, because the findings are few and small and I do not want the count
read as a verdict on the whole. Every constant I could check is right, every
worked example is right, the register's arithmetic is right, and the open path,
the index chain and the decode pipeline are stated to the byte. The places I
had to guess are listed in §7 below and they are all at the edges — the
compactor, and one taxonomy sentence.

---

## 1. The open path, byte-exact

### 1.1 What I actually implement

`open(transport) -> Session`

**Step O1 — obtain F.** §19.1 step 1 requires a *transport-authoritative* size
(`[R-CNT-10]`): "a full-response content length, the complete length of a range
response, or a size probe", and explicitly forbids substituting the trailer's
own `committed_file_length`. For a ranged HTTP transport I get F from the
`Content-Range` total of the suffix response in O2, so O1 costs no request of
its own — §19.1 says exactly that: "a remote reader's suffix range for step 2
carries F in its own response, so steps 1 and 2 cost one request between them".

**Step O2 — request 1: `Range: bytes=-64`.** 64 bytes. Nothing bounds this
range because nothing has been read: it is a constant suffix. Two hazards the
document names and I handle:

- A `200` response instead of `206`. `[R-CNT-10]`: "A remote reader MUST handle
  a 200 response to a range request (abort or accept the full body
  deliberately — never treat the body prefix as the requested range)". I accept
  the full body and take the last 64 bytes of it, and take F as the full
  content length. Note that if I accept the full body of a small file, bytes
  [0,16) are now **resident**, which arms `[R-CNT-04]` — see O3.
- No suffix-range support. `[R-CNT-10]` SHOULDs a size probe plus an absolute
  range; without it "remote open fails outright on such transports". I
  implement the probe: `HEAD` for F, then `Range: bytes=F-64-(F-1)`. That is
  3 requests on such a transport, and §6.4's note is explicit that no request
  count is a conformance property.

**Step O3 — front block, conditionally.** `[R-CNT-04]` turns the obligation on
*residency*, not on transport: "A reader whose open leaves bytes [0, 16)
resident — a local file read whole, a memory mapping, a speculative suffix
window that reached offset 0, or any transport already holding them — and a
content sniffer MUST verify the full block by byte equality before other
processing". My exact-range remote reader never holds [0,16), so it defers the
check and never performs it. My local (mmap) reader holds them and checks them
first. This is a clean rule and I implemented it as a one-line predicate on my
buffer map rather than on a transport class, which is what the text asks for.

**Step O4 — validate the trailer, in §6.2's fixed order.** The order matters
and I coded it as three phases because §6.2 splits it that way:

Phase A — the fields whose positions are fixed across *all* majors
(`[R-CNT-24]`):
1. `trailer_magic == 8A 4E 52 41 54 0D 0A 1A` (bytes [F-64, F-56)). Fail →
   reject-file (F8; a byte-reversed magic is the narrower F1).
2. `u32 at F-4 == CRC32C(bytes[F-64, F-4))`. Fail → reject-file (F14).
3. Version gate: `version_major` at F-56. 0 → reject-file (F18). Not 1 →
   reject-file on *capability* grounds with a distinct diagnostic
   (`[R-CNT-07]`); §21.6 tells me this is not a finding about the bytes, so my
   error type here is `UnsupportedMajor`, not `Corrupt`.

Phase B — the rest, all before acting on any of them:
4. flag gates: any of bits 0–15 set → reject-file (F19). Bits 16–31 ignored
   unconditionally.
5. `committed_file_length == F` (F17) and `F mod 64 == 0` (F13).
6. `dir_offset >= 16` (F9); `dir_length >= 4` (F16);
   `dir_offset + dir_length <= F - 64` (F10, and F3 for the wrapping sum).
7. `1 <= generation <= 2^63-1` (F11, F2).
8. `file_id != 0` (F12).
9. `reserved[56,60) == 00 00 00 00` (F15).
10. Every u64 above `<= 2^63-1` (F2).
11. `F >= 128` (F5, `[R-CNT-27]`).

I put the F5 check here rather than before O2 deliberately: on a 40-byte
physical file the suffix request returns 40 bytes and F=40 from the transport;
the magic check on "the final 64 bytes" is not even well-formed. My
implementation short-circuits: if F < 128, reject-file immediately without
attempting a trailer parse. The document supports this — `[R-CNT-27]` is an
unconditional file-scope rule and F5's instances are "F (physical file size);
committed_file_length" — but it does not *order* it against §6.2's sequence.
That is not a defect: §6.2's order binds "in order" only over the checks it
lists, and `[R-CNF-12]` licenses earlier detection.

**Step O5 — request 2: `Range: bytes=dir_offset-(dir_offset+dir_length-1)`.**
`dir_length` bytes. What bounds this range before I have read it: `dir_offset
>= 16`, `dir_length >= 4`, `dir_offset + dir_length <= F - 64`, and both under
2^63-1 — all checked in O4, all covered by the trailer CRC verified in O4
step 2, which is what `[R-ENC-05]` demands ("MUST NOT allocate, seek, or issue
I/O based on any integer obtained from a file before the checksum covering it
has been verified"). Nothing else bounds it: `dir_length` may legitimately be
16 MiB (§21.9's guarantee) and a file may declare more and stay conforming, in
which case I may decline under `[R-ERR-04]` and must report the decline as a
resource limit, not as corruption.

**Step O6 — directory CRC.** `CRC32C(region[0, dir_length-4)) ==
u32 at region[dir_length-4]`. Mismatch → reject-file (F20, `[R-CNT-11]`).
Before any other use of the region — including before parsing a single record
header. This is also the check §6.2's note relies on to catch a payload that
mimics a trailer at exact end of file.

**Step O7 — record walk.** Over `region[0, dir_length-4)` only. Records are
24-byte headers plus `inline_length` bytes, concatenated, no residue (F29). Per
record:
- `type == 0` → reject-file (F24). Explicitly *not* an unknown type.
- unknown type, MU=1 → reject-file (F35 if reserved-range; a conforming file
  reaching here carries an experimental-range type, and §21.6's closing
  paragraph tells me the file is conforming and my refusal records my own
  capability).
- unknown type, MU=0 → skip (ignore-record). I record its extent slot only so
  I can hand it to an updater; a reader never touches those bytes.
- type 0x0002 at top level: at most one (F34); extent slot not (0,0) (F21);
  `extent_length >= 5` (F22); `inline_length == 1` (F23). Extent slot bounds
  per `[R-CNT-13]` (F30, F31, F32, F2, F3). I do **not** fetch the extent here:
  §19.2 places extent checks at "at use of a record's extent", and §19.1 is
  explicit that "the open fetches no extent".
- type 0x0001: I parse *only* the name field, out of `inline_length`, and
  nothing else. §19.1 is precise about the failure mode: "a layer record whose
  name field does not lie entirely within that record's inline_length yields no
  name field to compare, so it contributes no name to the namespace and is
  instead a validity error at layer scope".

**Step O8 — layer-name namespace.** Two sub-steps in the order §19.1 fixes:
first *uniqueness*, over raw bytes, "whether or not each name is itself
well-formed" — byte-identical names in two layer records → reject-file (F4);
then *validity* of each name per §4.6 — ill-formed UTF-8 (L3), empty (L5), a
code point in U+0000–U+001F (L6), each reject-**layer**, detected here at open.
This ordering is load-bearing and stated, and I would have got it wrong without
that sentence: the naive implementation validates each name as it parses it and
would report reject-layer for a file whose correct verdict is reject-file.

**That is the open.** §19.1: "It consumes the trailer and directory only — no
extent slot's content, no tile index, no payload".

### 1.2 The byte-exact cold remote open

Against a server supporting ranged requests, exact-range strategy:

| # | Range | Bytes | Bounded before reading by |
|---|---|---|---|
| 1 | `bytes=-64` (suffix) | 64 | nothing — a constant suffix; the response carries F |
| 2 | `bytes=dir_offset-(dir_offset+dir_length-1)` | `dir_length` | `dir_offset >= 16`, `dir_length >= 4`, `dir_offset+dir_length <= F-64`, all trailer-CRC-covered and verified |

**Total: 2 requests, 64 + dir_length bytes.** Bytes [0,16) are never fetched.

For Appendix A's 128-byte file that is **2 requests, 68 bytes** — 64 for
[64,128) and 4 for [16,20). Appendix A states exactly this.

The speculative variant: one request for `bytes=-65536`. If the response
contains [dir_offset, dir_offset+dir_length) — the containment test of
`[R-CNT-09]` — request 2 is unnecessary: **1 request, min(65536, F) bytes**.
On a file smaller than the window the response is the whole file, [0,16) is
resident, and `[R-CNT-04]` now *obliges* the front-block equality check. I
implemented containment as `dir_offset >= F - window_len`, evaluated after the
trailer validates, since `dir_offset` is not trustworthy before then.

Appendix A adds a case I would not have thought of and which I checked against
the rule: a 112-byte window covering [16,128) contains the directory, so the
second request is spared, *and* [0,16) stays non-resident so the front-block
check stays optional. That is consistent — residency is per-byte-range, not
per-open.

---

## 2. Validation timing by tier

§19.2 gives the *latest* point; `[R-CNF-12]` licenses earlier. My reader is
lazy, so I implemented the latest points literally.

**At open** (§1.1 above): front block if resident; the whole trailer; the
directory region and its CRC; the full top-level record walk including
multiplicity, framing, non-layer extent-slot bounds and user-metadata framing;
and the layer-name namespace. Register rows due here: F1–F6, F8–F24, F29–F32,
F34, F35, and — outcome reject-layer but detected at open — L3, L5, L6.

**At first access to a layer** (§19.3): everything in the layer record, and
nothing fetched. The list `[R-RDR-03]` gives is long and I coded it as a single
`validate_layer()` that runs once and caches its verdict:

- extent slot: L15 (one half zero), L16 (`offset < 16`), L17 (`> F-64`), L1
  (`> 2^63-1`), L2 (wrapping sum).
- exact parse of the packed inline payload in §7.4's table order, no padding
  between fields: L23 for any overrun of the fixed prefix, the d dimension
  entries, the C channel entries, or the trailing fixed fields.
- remaining bytes parse as zero or more complete sub-records, no residue: L14;
  sub-record type 0 → L13; layer record nested as sub-record → L26; unknown
  sub-record MU=1 → reject-layer; more than one user-metadata sub-record → L19;
  user-metadata sub-record framing → L10, L11, L12.
- names: L4, L7, L8 (dimension and channel entries), L9 (duplicates within
  each of the two separate namespaces — §4.6 is explicit that a dimension and a
  channel may share a name).
- value sets: layout L36, linearization L33, codec L43, filter L45,
  index_encoding L31, channel type L34.
- geometry floor: L32 (rank 0, C 0, any Tᵢ 0). Eᵢ = 0 is **valid**
  (`[R-GEO-02]`) and I coded that as an early return: zero addressed tiles,
  entry_count 0, extent slot (0,0), crc_of_crc_array 0, every read returns no
  samples.
- arithmetic, all under `[R-ENC-04]`: Gᵢ = ceil(Eᵢ/Tᵢ) computed as
  `Eᵢ/Tᵢ + (Eᵢ % Tᵢ != 0)` — §11.2's note tells me *not* to use
  `(Eᵢ + Tᵢ - 1)/Tᵢ` because the intermediate sum can leave the declared
  domain; N = ∏Gᵢ; P = ∏Tᵢ; C·N; N·P; P·Q; P·Bᶜ; and
  `entry_count*20 + ceil(entry_count/2^16)*4`. Any of these exceeding 2^63-1 →
  L2.
- cross-checks: entry_count == addressed-tile count (N interleaved, C·N planar)
  → L21; extent_length against the index formula, including (0,0) with
  entry_count > 0 and a nonzero slot with entry_count = 0 → L22.
- declarations: A and S mutually exclusive → L20; A power of two in
  [512, 2^62] → L39; A_slab power of two in [1, 2^62] and zero iff S = 0 →
  L28, L29; codec 4 against the 0x7E000000 decoded-size cap → L44.
- fill: length prefix equals the type's element size → L30; bool fill byte in
  {0x00, 0x01} → L35.

Every one of these is decidable from bytes already resident plus F, which
`[R-RDR-03]` asserts and which I confirmed field by field. Layer access
performs no I/O. That is a real property and it is worth stating that it
survived the walk.

**At use of a tile** (§19.4): index chain (L37, L38), entry classification
(T6–T12), payload CRC (T1), decode (T3, T14–T25). Note the scope split
§19.2 flags: index-chain failures are detected at tile use but take **layer**
scope.

**At use of a record's extent**: the extent CRC (R2) and the document's own
content rules (R3–R10). Never at open.

**What a reader is permitted never to check.** Every row whose Detector is
*verifier*: F7, F25, F26, F27, F28, F33, F36; L18, L25, L40, L41, L42, L46,
L47, L48, L49; T2, T4, T5, T26. §2.4 and `[R-RDR-02]` say these impose no
reader obligation, and `[R-CNF-12]` lets me reject anyway if I happen to
notice. My reader notices exactly one of them for free — T2, the interleaved
bool byte, because my extractor has to look at the byte — and I chose *not* to
reject, which puts me on `[R-SER-08]`'s charitable path: report 0x00 as false
and every other byte as true. That rule is the difference between two readers
returning different sample values for the same tile, and the document closes it
explicitly.

**What becomes a verdict when.** A verifier's verdict is *nonconforming* the
moment any violation is established; *cannot establish* is reserved for a
traversal that established none and hit a capability or resource wall (an
unimplemented major, an MU=1 type it does not implement, a codec or filter it
cannot execute, a decode it declined on resource grounds, a user-metadata
document it declined). *Unexamined* is a report property, never a verdict.

---

## 3. Layer access and the tile-read algorithm

### 3.1 From layer name to declarations

`layers[name]` is built at open from the record walk. First access runs
`validate_layer()` above. From it I derive and cache:

- `G[i] = ceil(E[i]/T[i])`, `N = prod(G)`, `P = prod(T)`
- `B[c]` from §12.1's element-size column; `Q = sum(B)`; `Fofs[c] = sum(B[j] for j<c)`
- addressed-tile count = `N` (interleaved) or `C*N` (planar)
- decoded size per tile: `P*Q` interleaved; `P*B[c]` planar numeric;
  `ceil(P/8)` planar bool
- index region layout: entries at `[0, entry_count*20)`, segment CRC array at
  `[entry_count*20, entry_count*20 + ceil(entry_count/2^16)*4)`

### 3.2 Coordinate to disk ordinal

Linearization 1 only; any other value is L33 at layer access. From §11.4:

```
t[i] = x[i] div T[i]          u[i] = x[i] mod T[i]
in_tile_ordinal = sum_i u[i] * prod_{j>i} T[j]     # row-major, permanent
s = sum_i t[i] * prod_{j>i} G[j]                   # linearization 1
disk_ordinal = s                     (interleaved)
disk_ordinal = c*N + s               (planar, channel c)   # channel-major
```

I checked this against §11.4's example: extents (1024, 2048), tiles (256, 256),
G = (4, 8). Coordinate (300, 700): t = (1, 2), s = 1*8 + 2 = **10**;
u = (44, 188), in-tile ordinal = 44*256 + 188 = **11,452**; planar C = 4,
channel 2 → 2*32 + 10 = **74**. All three match the document.

### 3.3 The index chain

For disk ordinal k:

1. `seg = k div 2^16`. Segment byte range in the region:
   `[seg*2^16*20, min((seg+1)*2^16, entry_count)*20)`. CRC array byte range:
   `[entry_count*20, entry_count*20 + ceil(entry_count/2^16)*4)`. Both
   computable from the layer record alone — §15.4 says so and I confirmed it.
2. Fetch both (MAY be parallel). Verify `crc_of_crc_array` over the whole CRC
   array (L37), then the `seg`-th u32 over the segment's bytes as stored (L38).
   Mismatch → reject-**layer**, though we are at tile use.
3. `[R-IDX-05]`'s all-sentinel constant 0xEECB3BB2 licenses nothing on the read
   side: "verification is byte comparison of computed CRCs, never constant
   matching". My verifier computes.
4. Entry at region byte `20*k`, 20 bytes: u64 offset, u64 length, u32 crc.

I verified §15.4's worked example arithmetically: entry_count 1,000,000 →
ceil(1e6/65536) = 16 segments, 15 full and the last covering
1,000,000 − 15*65536 = **16,960** entries; CRC array 64 bytes; region
20,000,064 bytes; k = 999,999 → seg 15, segment-relative entry 16,959, byte
offset 339,180; CRC array at [20,000,000, 20,000,064); segment 15 at
[19,660,800, 20,000,000), i.e. 339,200 bytes. All match. A full segment is
65,536*20 = 1,310,720 = 1.25 MiB, as stated.

I also verified the planar example: C = 4, N = 32, channel 2 at s = 10 → disk
ordinal 74 → region bytes [1,480, 1,500); channel 3 unstored → entries 96–127.
Both match.

**Cold single-tile cost.** 3 requests: CRC array
(`ceil(entry_count/2^16)*4` bytes), one segment (≤ 1.25 MiB), the tile payload
(`length` bytes). §1's claim that "the array being the only term that grows
with the layer" is correct: the segment is capped and the payload is a tile.

### 3.4 Entry classification (§15.3), coded as a match

```
S = 0xFFFF_FFFF_FFFF_FFFF
if off==S and len==S and crc==0:  SENTINEL          # reads as fill
if off==S and len==S and crc!=0:  REJECT_TILE (T6)  # structural
if (off==S) != (len==S):          REJECT_TILE (T7)  # structural
if len==0:                        REJECT_TILE (T10) # structural
if off<16:                        REJECT_TILE (T8)  # structural
if off>2^63-1 or len>2^63-1:      REJECT_TILE (T11) # structural
if off+len overflows or > F-64:   REJECT_TILE (T9/T12) # structural
otherwise STORED
```

I checked the table is total. `(0,0)` falls to T10 and T8 — deliberately, since
"absence is spelled sentinel". The six rows §15.3 says are marked *structural*
are exactly the six above; I counted them.

The *structural* / *crc-failure* split matters in three places and the document
states all three: such entries contribute no stored extent to the verifier
overlap rows, are transparent to slab run continuity (`[R-SLB-03]`), and are
passed over by the coverage walk (`[R-LIF-08]`), their nominal bytes falling to
slack. An entry whose *only* defect is that its stored bytes fail its crc is
well-formed and keeps its extent in all three. That is a distinction I would
certainly have got wrong unaided.

### 3.5 Sentinel path

`[R-TYP-08]`: every requested position of that tile reads as fill — the entry's
channel's recorded fill in a planar layer; each carried channel's fill in
declared order in an interleaved layer — bit-exactly, with no payload I/O.
`[R-TYP-09]` is the guard I coded as an assertion: fill is produced by exactly
one condition, a sentinel entry read from a verified chain. Never for a
malformed entry, never for a failed segment or array CRC, never for a failed
payload CRC.

### 3.6 Payload, decode, extract

5. Fetch `[offset, offset+length)`; `CRC32C(bytes) == entry.crc` else T1.
6. Decode: **codec first, then the filter's inverse** (`[R-COD-01]`, §19.4
   step 6). Getting this backwards is the classic bug and the document states
   the order twice, in both directions (writer: filter then codec).
   - codec 1: stored bytes are the filtered image verbatim, and
     `length == decoded_size` is checkable *before the fetch* (T14).
   - codec 2: exactly one raw RFC 1951 stream, no zlib/gzip wrapper (T15), no
     second stream (T16). Up to seven unused high bits in the final byte are
     unconstrained; a whole trailing byte is T24.
   - codec 3: first four bytes `28 B5 2F FD` (T17); exactly one frame, no
     skippable frame anywhere (T18); Dictionary_ID zero (T19); no
     Content_Checksum flag (T20); Window_Size ≤ decoded size (T21);
     Frame_Content_Size, if present, == decoded size (T22) and **never** an
     allocation source.
   - codec 4: exactly one raw LZ4 block, not a frame (T23), decoded with
     `length` as input size and `decoded_size` as output capacity.
   - all codecs: exact consumption, no trailing bytes (T24), no malformed
     stream (T25).
7. `len(decoded) == decoded_size` exactly, else T3 — and `decoded_size` comes
   from declarations, never from the payload. This is the decompression-bomb
   defense §22.2 names.
8. Inverse byte-shuffle if filter 2: stride `s` = element size (planar
   numeric), Q (interleaved), 1/identity (packed bool plane); with n = L/s,
   restore byte at `i*n + j` to offset `j*s + i`.

I checked §17.3's example by hand. 1.0f, 2.0f, 3.0f little-endian are
`00 00 80 3F | 00 00 00 40 | 00 00 40 40`; s = 4, n = 3; the filtered image is
first bytes `00 00 00`, second bytes `00 00 00`, third bytes `80 00 40`, fourth
bytes `3F 40 40` → `00 00 00 00 00 00 80 00 40 3F 40 40`. Matches the document
byte for byte.

### 3.7 The decoded byte layout I end up with

Interleaved (§14.2): sample-major, value k of the sequence is channel
`k mod C`'s value at in-tile ordinal `k div C`. Channel c's value at in-tile
ordinal u sits at byte `u*Q + Fofs[c]`. Decoded size `P*Q`.

Planar numeric: channel c's plane, value k at byte `k*B[c]`, decoded size
`P*B[c]`.

Planar bool (§14.3): bit-packed LSB-first, value k at bit `k mod 8` of byte
`k div 8`, decoded size `ceil(P/8)`; final-byte high bits beyond the last value
are pad bits carrying the channel's fill bit.

Checked against §14.2's example: interleaved, T = (2,3), P = 6, channels
`a`(uint8) + `b`(uint16) → Q = 3, decoded size 18; in-tile (1,2) → ordinal
1*3+2 = 5 → bytes [15,18), `a` at 15, `b` at 16–17. Planar `b`: 12 bytes,
ordinal 5 at bytes 10–11. `t`(float32) + `m`(bool) interleaved → Q = 5,
decoded 30, ordinal 5 → [25,30), `t` at 25–28, `m` at 29. All correct.

Checked §14.3's example: T = (2,5), P = 10, alternating true/false → byte 0 =
`0x55` (bits 0,2,4,6), byte 1 = value 8 true in bit 0, value 9 false in bit 1 =
`0x01`, pad bits 2–7. Fill false → `55 01`; fill true → `55 FD`. Correct —
0x01 | 0xFC = 0xFD.

Checked §14.5's example: extents (5,5), tiles (4,4) → grid 2x2; the (1,1) edge
tile spans 4–7 on both axes; only (4,4) is inside the extents, so 1 real and 15
padding positions; one uint16 channel with fill 0xABCD → 32 bytes, value 0 the
sample, values 1–15 each `CD AB`. Correct.

9. Extract: never return a padding position (`[R-GEO-04]`).
10. Return: bit patterns unaltered — NaN payloads preserved, −0.0 distinct from
    +0.0 (`[R-TYP-04]`, `[R-MDL-02]`). The one byte a reader ever *resolves* is
    `[R-SER-08]`'s malformed interleaved bool, which cannot occur in a
    conforming file.

Partial failure inside one request (§19.4 step 8): a rejected tile bounds its
failure to the positions it carries; I may return the good entries' values with
a per-entry failure report, or fail the whole request — but I must never stand
fill in for a rejected tile. A step-3 index-chain failure instead takes layer
scope, bars the rest of the request and all further service from the layer, and
is *prospective*: values already returned stand.

---

## 4. Degradation walks

Six, end to end.

### 4.1 Unknown record type at file scope, MU = 0, PE = 0, with an extent

Open proceeds normally through O6. At O7 the type is not 0x0001 or 0x0002 and
not 0. MU = 0 → **ignore-record**: skipped as though absent (§2.4). I do not
parse its inline payload, do not fetch its extent, and do not verify anything
over it — §8.1's map gives such an extent *no* checksum, and §22.3 concedes the
consequence plainly: corruption inside it is invisible to reader and verifier
alike. I record `(type, flags, header_bytes, extent_slot)` so an updater can
re-emit it byte-identically.

**What I still serve:** everything. Every layer, every tile, both metadata
documents. The file is conforming if the type is from the experimental range
(§21.6) and nonconforming-but-fully-readable if from the reserved range (F36,
verifier).

**What I must not do:** infer anything from the payload. `[R-CNT-13]` makes the
extent slot its only sanctioned reference to bytes outside the record sequence,
which is exactly what lets a compactor relocate it unread.

### 4.2 Unknown codec value 7 on layer B, file has layers A and B

O1–O8 succeed; the file opens. First access to B runs `validate_layer()`, which
hits §17.2's value set: 7 is reserved → L43 → **reject-layer**.

**What I still serve:** all of layer A, and B's *name* (§2.4 explicitly permits
listing a rejected layer, including its name). Nothing of B's data or
declarations.

`[R-COD-11]` is worth quoting to myself here because it closes what would
otherwise be a profile hole: "For a conforming reader that position arises only
at a reserved or experimental value, every assigned codec and filter being core
... software unable to execute an assigned codec or filter is not a conforming
reader". So there is no such thing as a reader that opens the file but declines
codec 3.

The outcome is *prospective* (§2.4): if I had already returned tiles from B
before something else pushed me to re-validate, those returns stand. In my
implementation validation precedes any access, so this never arises — which is
the point of §19.2 fixing the *latest* detection point.

### 4.3 Truncated tail — a torn commit

Writer crashed after appending payloads and a directory but before the trailer.
Physical size is F_old + 900,000. My suffix request returns the final 64 bytes,
which are payload or directory bytes.

- Magic check fails → **reject-file** (F8), reported as *torn or invalid*.
- `[R-LIF-05]` forbids me to scan backward. I do not. §9.5's note tells me why
  I cannot even distinguish this from corruption: "it cannot tell residue from
  corruption and is not asked to."
- If the tail happens to satisfy magic + CRC by accident, F17 catches it:
  `committed_file_length` will not equal the transport size. §6.2's note points
  out the remaining case — a payload byte-string that mimics a trailer and sits
  at exact end of file passes every trailer check and is caught at the
  directory CRC (F20).

**What I still serve:** nothing. Reject-file is the whole file.

**What recovery does, and I do not:** §9.6's backward probe at 64-aligned
offsets, requiring magic + CRC + `committed_file_length == o + 64`, then
whole-file re-verification of the truncation candidate, then reporting which
candidate it settled on and how many it rejected. Explicitly "not a reader
behavior".

### 4.4 Checksum mismatch on one stored tile of a 32-tile layer

Index chain verifies (L37, L38 pass). Entry k is well-formed and STORED. I
fetch `[offset, offset+length)` and `CRC32C(bytes) != entry.crc` → T1 →
**reject-tile**.

**What I still serve:** every other tile of the same layer, every other layer,
and the layer's metadata. For a region request covering tile k and its
neighbours, §19.4 step 8 lets me return the neighbours' values with a per-entry
report of k's failure.

**What I must not do:** return fill for tile k. `[R-CNF-09]` — "in particular, a
read of a rejected tile MUST NOT silently return fill" — and `[R-TYP-09]`
restate this from both ends. This is the single most tempting wrong behavior in
the whole reader and the document forecloses it twice.

Note the coverage consequence, which I only found by reading §9.7 carefully:
this entry is *not* structurally defective, so its extent still stands, still
counts in the verifier's overlap rows, still participates in slab run
continuity, and is still claimed by the coverage walk. Its bytes do not fall to
slack.

### 4.5 A limit exceeded — a 40 MiB user-metadata document

§21.9 guarantees 16 MiB decoded for a user-metadata document. My reader bounds
its decode at 16 MiB (the minimum `[R-MTA-09]` permits).

- I decode with that bound; the frame exceeds it; I abandon the decode. The
  record is **ignore-record** and I SHOULD report the loss.
- `[R-ERR-04]` gives me a second, whole-file option, and §18.2's note is
  explicit that the narrower scope is unavailable: "a document having no
  declared size and so no narrower scope whose declarations that rule can
  measure". If I take it, I decline the **whole file**, and I MUST report the
  refusal as a resource limit, not as a validity error.
- The file remains **conforming** either way. A verifier that declines the
  decode cannot establish that document's conformance, must not certify, must
  report the requirement it could not check and the ground, and — if it
  established no violation elsewhere — reports *cannot establish*.

I chose ignore-record. The whole-file option seemed to me the wrong default: it
turns an advisory annotation into a file-opening failure. Both are licensed.

### 4.6 Format major 2

The suffix request returns 64 bytes. Magic matches (`[R-CNT-24]` fixes it at
F−64 permanently). Trailer CRC at F−4 over [F−64, F−4) verifies (also
permanent). `version_major` at F−56 reads 2. My reader implements only major 1
→ **reject-file** on capability grounds.

The diagnostic is the whole point: `[R-CNT-07]` SHOULDs it distinct from both
"not a TARN file" and "corrupt", "e.g. 'TARN format major N; this reader
supports major 1'", because "a reader that reports an unimplemented major as
corruption misleads users into discarding files that current software reads".
My error type is `UnsupportedMajor { major: 2 }`.

Critically, I stop here and check *nothing* else. §6.2's ordering exists for
this: only magic, trailer CRC and the version gate touch fields whose positions
are fixed across majors. Checking `dir_offset >= 16` on a major-2 trailer would
be reading a field that major may have redefined. §21.6 confirms the file may
be perfectly conforming and my refusal "records a reader's capability, not a
defect in the bytes".

### 4.7 (extra) Unrecognized flag bits

Trailer flags = 0x0003_0000. Bits 16 and 17 are ignore-lane → I ignore them,
and the **file is conforming** (§21.6, `[R-CNT-08]`). Trailer flags =
0x0000_0001: bit 0 is incompat-lane and I implement no flag bits → reject-file
(F19). An updater must copy unknown ignore-lane bits forward and must not clear
them; a compactor does the same even though its output is a new file.

Record flags with reserved bits 2–15 set: readers MUST ignore them; only a
verifier records the violation (F26, L47). Stored MU/PE on a *registered* type
that disagree with §7.3: readers apply the fixed semantics regardless, verifier
records F28/L49. These are the rows where the register's outcome column names a
scope of damage and imposes nothing on me — §21.1 says so directly.

---

## 5. A worked example — Appendix A's 128-byte file, driven through my reader

I took the hex dump verbatim and ran it.

```
0000  89 54 41 52 4E 0D 0A 1A  00 00 00 00 00 00 00 00
0010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
0020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
0030  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
0040  8A 4E 52 41 54 0D 0A 1A  01 00 00 00 00 00 00 00
0050  01 00 00 00 00 00 00 00  10 00 00 00 00 00 00 00
0060  04 00 00 00 00 00 00 00  80 00 00 00 00 00 00 00
0070  EF CD AB 89 67 45 23 01  00 00 00 00 D2 38 09 E0
```

**O1/O2.** `bytes=-64` → 64 bytes, F = 128 from the transport.

**O3.** Not resident (exact-range remote). Skipped. A local reader checks
`89 54 41 52 4E 0D 0A 1A` + 8 zeros at [0,16) — present.

**O4 phase A.** [64,72) = `8A 4E 52 41 54 0D 0A 1A` ✓. Trailer CRC: I computed
CRC-32C over the 60 bytes

```
8a 4e 52 41 54 0d 0a 1a 01 00 00 00 00 00 00 00
01 00 00 00 00 00 00 00 10 00 00 00 00 00 00 00
04 00 00 00 00 00 00 00 80 00 00 00 00 00 00 00
ef cd ab 89 67 45 23 01 00 00 00 00
```

and got **0xE00938D2**, stored little-endian as `D2 38 09 E0` at [124,128).
**Matches the document exactly.** `version_major` = 1 ✓.

**O4 phase B.** flags 0 ✓; `committed_file_length` = 128 = F ✓ and 128 mod 64 =
0 ✓; `dir_offset` = 16 ≥ 16 ✓; `dir_length` = 4 ≥ 4 ✓; 16 + 4 = 20 ≤ 128 − 64 =
64 ✓; generation = 1 ✓; `file_id` = 0x0123456789ABCDEF ≠ 0 ✓; reserved [120,124)
zero ✓; F = 128 ≥ 128 ✓.

**O5.** `bytes=16-19` → 4 bytes `00 00 00 00`.

**O6.** Record sequence is `dir_length − 4` = 0 bytes. CRC-32C of zero bytes =
0x00000000 (I computed it; §4.5 states it) = the stored `00 00 00 00` ✓.

**O7/O8.** Zero records, zero layers, empty namespace. §21.6 records "The file
contains zero layers" as a conforming, defined condition.

**Total cost: 2 requests, 68 bytes.** Nothing further to read.

**The pre-trailer pad** at [20,64) is 44 bytes, slack. §5.1's derivation of the
128-byte floor checks out: the trailer must start at a 64-aligned offset and
the directory must end at or before it, so `F − 64 >= dir_offset + dir_length
>= 20`, giving `F >= 84`, and F must be a multiple of 64, so F = 128.

### 5.1 Other constants I could check, and did

- CRC-32C(`"123456789"`) = **0xE3069283**, stored `83 92 06 E3`. ✓ (§4.5)
- CRC-32C of zero bytes = **0x00000000**. ✓ (§4.5)
- CRC-32C of a full all-sentinel segment — 65,536 copies of
  `FF ×16 00 ×4`, 1,310,720 bytes — = **0xEECB3BB2**. ✓ (§15.4, Appendix B)
- §21.9's note: 2^32 addressed tiles → 2^16 segments × 4 bytes = 262,144 =
  **256 KiB** ✓; 2^36 → 2^20 × 4 = **4 MiB** ✓.
- §20.3's example: a 32-tile interleaved layer's re-emitted index region =
  32*20 + ceil(32/65536)*4 = 640 + 4 = **644 bytes** ✓.
- §12.3's channel entry `temp`/float32/0x7FC00000 =
  `04 74 65 6D 70 0C 00 04 00 00 C0 7F`, 12 bytes ✓ (1 + 4 + 2 + 1 + 4).
- §4.6's `température` in NFC = 12 bytes
  `74 65 6D 70 C3 A9 72 61 74 75 72 65` ✓; NFD 13 ✓.
- §11.2: extents (1000, 2048), tiles (256,256) → G_y = ceil(1000/256) = 4 ✓.
- §16.2: N = 32, S = 8 → runs [0,8), [8,16), [16,24), [24,32) ✓; tile rows 1–2
  under row-major with G_x = 8 are ordinals 8–23 = runs 1 and 2 exactly ✓.
- §21.8's arithmetic: I parsed every register row mechanically. **121 rows**
  (36 F + 49 L + 26 T + 10 R — matching each subsection's stated count) over
  **248 instances**, counting a `—` cell as one and otherwise splitting on
  semicolons per §21.1's rule. Both figures match §21.8 exactly.

I found no wrong constant, offset, or checksum anywhere in the document.

---

## 6. Register completeness — the check I ran because §21.1 invites it

§21.1 now makes a confident claim: "Its **completeness is normative** — a
*detectable* file-conformance violation this specification names and the
register omits is a defect in this document, detectability being the gate
`[R-CNF-07]` already applies and §21.7 the account, by class, of what fails
it". So I walked every `[R-...]` identifier in the document and asked, for
each: does it name a file-conformance violation, is it detectable from one
file, and does a row cover it?

Result: I could not find a missing row. Every MUST-level condition I traced
lands somewhere — the ones I expected to be gaps are handled explicitly:

- Nesting beyond two levels (`[R-CNT-18]`) has no reader-detectable witness in
  major 1, and §7.4's note says so and declines a row.
- A stale slab declaration (`[R-SLB-04]`) has no row of its own because every
  file exhibiting one exhibits L41 or L42; §16.2's note says so.
- Residue past a completed commit (`[R-LIF-04]`) has no row because a reader
  meets it only as an already-registered trailer-gate failure; §9.5's note says
  so.
- "A byte belongs to no coverage class" has no row because it describes
  nothing; §5.2's note derives that from `[R-LIF-08]`.

That is four separate places where the document anticipates the exact question
and answers it. The register held up.

The one gap I did find is in §21.7's *account*, not in the register — see
finding reader-05.

---

## 7. Findings

Seven. Two I flag byte-level; both sit in §20.5, and I make the case for each
rather than asserting it.

---

### reader-01 — CONTRADICTION — §4.7 / §13.1 / §14.5

**Location:** §4.7 `[R-ENC-16]`; §13.1 (unnumbered paragraph after
`[R-TYP-06]`); §14.5 `[R-SER-05]`.

**Title:** §4.7's structural test catches `fill`, contradicting its own closing
claim that `fill` is the only semantic field.

**Quotation (§4.7, `[R-ENC-16]`):**

> "A field is **structural** if its value determines anything a conforming
> reader or verifier does with the file's bytes — where a byte lies, how it
> decodes, or whether the file, layer or tile is accepted at all, which is the
> sense `[R-CNT-07]`, `[R-MTA-02]` and `[R-SEC-06]` already use. It is
> **semantic** if not, but its value determines what decoded values are. ... In
> format major 1 `fill` is the only semantic field and `version_minor` the only
> descriptive one: every other field this specification defines is structural."

**Quotation (§14.5, `[R-SER-05]`):**

> "at every padding position, a writer MUST encode, for each channel the
> position carries, that channel's fill value — the recorded fill bytes for a
> numeric channel, the recorded fill byte for an interleaved bool channel, the
> fill bit in a packed plane. Every pad bit (§14.3) MUST carry the plane's
> channel's fill bit. A conforming reader never returns this content
> (`[R-GEO-04]`) and is not obligated to check it; a verifier MUST check it,
> and a violation is a validity error at tile scope."

**Quotation (§13.1):**

> "The fill value is semantic (§4.7): it affects what unstored samples read as,
> never how any byte is located or decoded"

**Detail.** §4.7's definition of *structural* is now stated over "a conforming
reader **or verifier**", and its third disjunct is "whether the file, layer or
tile is accepted at all". The recorded fill bytes satisfy that disjunct
directly: under §14.5 a verifier compares every padding position and every pad
bit against the channel's recorded fill, and a mismatch is a validity error at
**tile** scope (register rows T4 and T5). Change the fill field in a layer
record carrying edge padding and you change which tiles a verifier accepts. So
by §4.7's own test `fill` is structural, and §4.7 says a field is semantic only
"if not" structural — leaving no field in the semantic class and falsifying the
sentence that asserts one.

§13.1 propagates the error and shows how it happened: it glosses "semantic" as
"never how any byte is located or decoded", which is §4.7's *first two*
disjuncts. The third — acceptance — was added when the definition was restated
over readers and verifiers, and the fill classification was not re-derived
against it.

Permitted readings I can defend: (a) the definition governs and `fill` is
structural, so §4.7's closing sentence and §13.1's parenthetical are wrong; (b)
the closing sentence governs and the definition's third disjunct is to be read
as reader-only despite the words "or verifier", so `fill` stays semantic. I
picked (a): §4.7's own text says "which is the sense `[R-CNT-07]`, `[R-MTA-02]`
and `[R-SEC-06]` already use", and `[R-MTA-02]` and `[R-SEC-06]` are both
reader-facing while `[R-CNT-07]` is an acceptance gate — the definition is
plainly meant to cover acceptance, and the "or verifier" is deliberate.

**What an implementer does wrong without it.** Not much on the read path, which
is why I do not flag it byte-level. But an implementer building a *verifier*
from §13.1 alone — "never how any byte is located or decoded" — has been told
the fill field is inert, and the one thing a verifier must do with it (§14.5's
padding and pad-bit check, T4/T5, four instances and one instance respectively
in §21.8's corpus) is exactly the check that reads it. The taxonomy is also the
document's own instrument for saying which fields need conformance vectors and
which an updater may reason about opaquely; a class with no members in it is a
worse defect in a taxonomy than a miscategorised member.

**Byte-level: NO.** Whatever §4.7 calls the field, §14.5 states the verifier
obligation unconditionally and T4/T5 register it. No verdict on any byte
sequence turns on the classification: two competent implementations reading
§14.5 check padding against fill regardless of which noun §4.7 attaches to the
field. The defect is in a definition and in a claim about the document's own
contents, not in an operative rule.

---

### reader-02 — CONTRADICTION — §20.5 `[R-WRT-06]` vs `[R-WRT-07]`

**Location:** §20.5, `[R-WRT-06]` and `[R-WRT-07]`; against §16.1
`[R-SLB-01]`, §16.2 `[R-SLB-03]`, and register rows L40, L41, L42.

**Title:** §20.5 grants a compactor unrestricted placement while requiring its
output to be conforming, and a carried-forward alignment or slab declaration
makes the two incompatible.

**Quotation (§20.5, `[R-WRT-07]`):**

> "A compactor preserves content but not placement — placement is not among the
> things it carries forward, and it is free to place structures anywhere §5.2
> admits: every stored tile's bytes verbatim — each index entry's crc is
> unchanged — and every retained record per §20.4, except that relocation
> re-points extent slots, regenerates each relocated tile-index region (entry
> offsets new; entry lengths, entry crcs, and sentinel entries unchanged;
> segment CRCs recomputed over the entries as re-emitted), and updates the
> layer-record fields covering a regenerated region (crc_of_crc_array)."

**Quotation (§20.5, `[R-WRT-06]`):**

> "A compactor's output contains only the structures reachable from the input's
> live trailer — the live committed state (§7.2), less any record §20.4 lets it
> drop — so slack is never carried. Given a conforming input the output is a
> conforming file."

**Quotation (§16.2, `[R-SLB-03]`):**

> "When declared, for every run: the run's stored tiles are contiguous and
> packed in ordinal order — each stored tile's offset equals the previous
> stored tile's offset plus its length — and the first stored tile's offset
> satisfies offset mod A_slab = 0."

**Detail.** Take a conforming input whose layer L declares S = 8 and
A_slab = 4096 (§16.2's own worked example). The compactor re-emits L's layer
record; `[R-WRT-05]` requires byte-identical re-emission and `[R-WRT-07]`'s
enumerated exceptions are only the extent slot, the regenerated index region
and `crc_of_crc_array` — so S and A_slab survive verbatim, and there is no
mechanism by which a compactor could clear them. It then places L's stored
tiles. `[R-WRT-07]` says it "is free to place structures anywhere §5.2 admits",
and §5.2 admits any non-overlapping partition; §16 is not mentioned anywhere in
§20.5. But if it exercises that freedom — say by packing every layer's tiles
densely in disk-ordinal order across run boundaries, or by starting a run at an
offset not divisible by 4096 — its output violates `[R-SLB-03]` and is
therefore **not** a conforming file, contradicting `[R-WRT-06]`'s flat
statement that it is.

Nothing else closes this. `[R-SLB-04]` binds "A writer or updater whose commit
supersedes a stored tile in, or grows the extents of, a slab-declared layer" —
a compactor does neither; it performs a whole-file rewrite, not a commit.
§20.2's creation rule does name "every declared layout invariant
(`[R-SLB-01]`, `[R-SLB-03]`)" — but §20.1 makes creator, appender and compactor
three distinct tiers, and §20.2 binds only the creator. §20.5's own
verification-depth rule `[R-WRT-09]` lists what a compactor must *verify* on
input and reaches nothing about what it must satisfy on output. The omission is
conspicuous precisely because §20.2 states it for the neighbouring tier.

Permitted readings: (a) the general guarantee governs — the compactor must
re-establish every declared alignment and slab invariant in its output; (b) the
specific permission governs — placement is bounded only by §5.2, and §16's
invariants are among the things the compactor is expressly told it does not
carry forward, since a slab declaration *is* a statement about placement and
"placement is not among the things it carries forward". I picked (a), because
`[R-CNF-06]` makes a compactor satisfy "every writer requirement for the bytes
it produces" and the tile offsets are bytes it produces. But (b) is a
straightforward reading of the sentence as written, and it is reinforced by the
declaration being described as a *placement* property in exactly the clause
that disclaims placement.

**What an implementer does wrong without it.** Reading (b) produces a compactor
whose output is nonconforming for every slab-declared or alignment-declared
input, and — because `[R-SLB-01]`/`[R-SLB-03]` are verifier-detected — nothing
in the read path ever complains. The damage surfaces only when someone
certifies the output, at which point L40/L41/L42 fire and the file cannot be
repaired without another rewrite.

**Byte-level: YES.** Compactor A (reading (a)) emits layer L's stored tiles at
run starts satisfying `offset mod 4096 == 0` with each run packed; compactor B
(reading (b)) emits them densely from the first available offset. The two
outputs differ in every tile offset in the layer, in every index entry's offset
field, in every segment CRC and in `crc_of_crc_array`. And a verifier handed
B's output must reject layer L (L41, L42) while accepting A's — so the fork is
in both halves of the test: which bytes may be emitted, and which are accepted.
The two implementations are named, the differing bytes are the 8-byte offset
field of every non-sentinel index entry in L, and the differing verdict is
reject-layer versus conforming.

---

### reader-03 — AMBIGUITY — §20.5 `[R-WRT-06]`/`[R-WRT-09]` vs §7.1 `[R-CNT-25]`

**Location:** §20.5 `[R-WRT-06]`, `[R-WRT-09]`; §7.1 `[R-CNT-25]`; §21.5 row
R2; §2.4's ignore-record row.

**Title:** Whether one corrupt user-metadata extent permanently bars compaction
of an otherwise sound file.

**Quotation (§20.5, `[R-WRT-09]`):**

> "it relies structurally on every structure it copies, so it MUST verify each
> link of the chain — the open (§19.1), each retained layer's record (§19.3)
> and full index chain (`[R-IDX-04]`), and each relocated extent's checksum,
> including every stored tile's entry crc — before emitting that structure's
> bytes."

**Quotation (§20.5, `[R-WRT-06]`):**

> "A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges
> fails, and MUST NOT emit a file carrying a violation it has detected: it can
> neither drop the structure (§20.4, `[R-WRT-07]`), nor re-emit it corrected
> (`[R-WRT-05]`)."

**Quotation (§7.1, `[R-CNT-25]`):**

> "User metadata is quarantined: each way a user-metadata record's document can
> be unreadable once its framing has been read — a failed extent CRC, an
> unimplemented or invalid encoding, a decode failure, or content violating the
> document's own rules (ill-formed UTF-8 included, `[R-ENC-11]`) — is
> ignore-record with a SHOULD-report, notwithstanding the owning-scope mapping
> of `[R-CNF-08]`. Application metadata never invalidates the structural data
> it annotates."

**Detail.** A user-metadata extent is a relocated extent and it has a checksum
(§8.1's map: "User-metadata extent | final 4 bytes of the extent | the
preceding bytes"). So `[R-WRT-09]` obliges the compactor to verify it, and if
the CRC fails — register row R2, a genuine violation whose outcome is
ignore-record — `[R-WRT-06]`'s first clause fires unqualified: refuse to
compact. The second clause bars the escape, since the record carries PE = 1 by
registry (§7.3) and so cannot be dropped, and `[R-WRT-05]` bars re-emitting it
corrected.

The consequence is severe and I do not think it is obviously intended: a file
with one corrupt metadata blob becomes permanently uncompactable. §20.5 says
compaction "is the only operation that reclaims slack", and §23.1 says it is
"the only operation that removes slack", so such a file can never be shrunk and
its superseded bytes can never be removed — over a corruption that §7.1 says
"never invalidates the structural data it annotates" and that every reader is
told to skip and carry on from.

Permitted readings: (a) refuse — `[R-WRT-06]`'s clauses are unqualified and
doubly stated, and R2 is a violation the compactor has detected; (b) proceed —
the quarantine governs "notwithstanding" the ordinary scope mapping, the record
is "skipped as though absent" (§2.4), its extent bytes are relocated verbatim
without ever being interpreted, and the compactor reports the loss under
`[R-CNT-20]`'s SHOULD; (c) a narrower version of (b): `[R-WRT-09]`'s "each
relocated extent's checksum" was written with tile and index extents in mind
and does not reach a quarantined document at all, so no check fails.

I picked (a), because `[R-WRT-06]` is the rule written specifically for
compactors and states the refusal twice, and because "MUST NOT emit a file
carrying a violation it has detected" is hard to read around once R2 is
established. But I record it as an ambiguity rather than a settled point: the
quarantine's own "notwithstanding" clause is exactly the shape of language that
overrides a general rule, and §7.1's closing sentence — "Application metadata
never invalidates the structural data it annotates" — reads as a direct
statement that this outcome should not happen.

**What an implementer does wrong without it.** Under (a) a compaction tool
returns "refuse" on files that operators expect it to fix, with a diagnostic
about metadata; under (b) it produces output that carries a known violation,
which `[R-WRT-06]` on its face forbids. The two are opposite operational
behaviours on the same input.

**Byte-level: YES.** Compactor A refuses and emits nothing; compactor B emits a
complete compacted file — a fresh file_id, generation 1, every structure
relocated. That is not a difference of degree: one byte sequence exists and the
other does not, from the same input, under two defensible readings of the same
document. The test asks whether resolving this changes which byte sequences a
conforming implementation may emit; it does, for every file that carries a
user-metadata record with a damaged extent.

I am less confident in this one than in reader-02, and I say so: the strongest
counter is that `[R-WRT-06]` really does decide it, and the quarantine language
is about *reader* outcomes rather than about updater conduct. If a triager
downgrades it to OBSERVATION on that ground I would not argue hard. But I would
rather report it than have the reading go unrecorded, and the operational
consequence — permanently uncompactable files — is the kind of thing worth
someone deciding on purpose.

---

### reader-04 — OBSERVATION — §20.4 vs Appendix H

**Location:** §20.4, the paragraph after `[R-WRT-05]`'s table; Appendix H,
"Conforming updater".

**Title:** §20.4's summary of what no commit removes names only the *file-scope*
user-metadata record; Appendix H states it at both scopes, and the governing
paragraph reaches both.

**Quotation (§20.4):**

> "No commit therefore removes a layer record or a file-scope user-metadata
> record. Both registered types carry PE = 1, and an in-place removal would
> strand that layer's stored tiles and index region as slack (§5.2) which only
> compaction reclaims, leaving the file no smaller than before — so the
> operation would cost what it appears to save."

**Quotation (Appendix H, "Conforming updater"):**

> "never removes a layer record, or a user-metadata record at either scope
> (§20.4)"

**Detail.** The preceding paragraph in §20.4 is unambiguous and reaches both
scopes: "For a type §7.3 registers, the registry's fixed flags govern rather
than the stored ones (`[R-CNT-22]`) — both registered types carry PE = 1, so
neither can be dropped, and implementing a record's type confers understanding
of it, not permission to drop it." A layer's user-metadata **sub-record** is
type 0x0002, a registered type, PE = 1 by registry — so it cannot be dropped
either. The summary sentence then restates the consequence at a narrower scope
than the rule that produced it, and its stated *reason* (stranded tiles and
index region) applies only to the layer-record half, which is presumably how
the sub-record case fell out.

Appendix H — which is non-normative and explicitly says "each entry's authority
is the requirement or section cited, never this summary" — states it correctly.
So the reader who takes the summary at face value is contradicted by the
appendix that summarises it, which is the wrong way round.

Permitted readings: (a) the enumerating paragraph governs, both scopes are
protected, and the summary sentence is merely incomplete; (b) the summary
sentence is exhaustive and a layer's user-metadata sub-record may be dropped. I
picked (a) without much hesitation — (b) requires §20.4's own table row
("MU = 0, PE = 1 | Retain byte-identical, extent content unmodified") to have
an unstated exception, and requires "neither can be dropped" to mean something
narrower than it says.

**What an implementer does wrong without it.** An updater that reads only the
summary sentence drops a layer's `tarn.title`/`tarn.axes` document on the next
commit that touches the layer, silently losing application state — the exact
failure §20.4's own SHOULD-report clause exists to make visible. But it would
have to ignore the table row directly above to do it.

**Byte-level: NO.** The table row and the "neither can be dropped" sentence
already decide it; a competent updater reading §20.4 in full does not fork.
And the emitted file is conforming either way — dropping the sub-record
produces a valid file, so no verifier verdict on any byte sequence turns on
this. It is a conduct rule stated at two widths in two places.

---

### reader-05 — OBSERVATION — §21.7 `[R-ERR-01]`

**Location:** §21.7, second paragraph; against §21.1's designation of §21.7 as
"the account, by class, of what fails" the detectability gate.

**Title:** §21.7's closed list of witness-less obligations omits `[R-LIF-02]`
and `[R-IDX-01]`.

**Quotation (§21.7):**

> "A second set of obligations is omitted from the register because a single
> file exhibits no witness of their violation. Committed-prefix immutability
> and the generation sequence (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a
> file's history, which §9.7 does not reconstruct; the ordinal mappings of
> `[R-GEO-06]` and `[R-SER-01]` are satisfied by a structurally valid tile
> whatever values it carries; `[R-CNT-13]`'s prohibition on an MU = 0 record
> encoding file offsets in its own payload is opaque by construction; and
> `[R-ENC-06]`'s fixed field widths are not a state a file can be in, since the
> parse is always at the widths this specification fixes and a structure
> written at any other yields different values at them, caught by the rows for
> the fields that hold them."

**Quotation (§21.1):**

> "Its **completeness is normative** — a *detectable* file-conformance
> violation this specification names and the register omits is a defect in this
> document, detectability being the gate `[R-CNF-07]` already applies and §21.7
> the account, by class, of what fails it"

**Detail.** §21.1 now leans on §21.7 as *the* account of which named
MUST-level conditions escape the register on detectability grounds. The list is
written as closed — four items joined by semicolons with a terminal "and" — and
two MUST-level obligations that belong in it are missing:

1. **`[R-LIF-02]` step 3.** Its own Note establishes the violation: "Step 3 is
   not discharged by a directory an earlier generation appended: each commit
   appends its own complete directory, and the trailer of step 5 addresses that
   one. A writer that re-points a new trailer at a prior generation's directory
   region has left step 3 unperformed." A file whose trailer points at an
   earlier generation's directory region is byte-indistinguishable from one
   whose commit appended that directory — there is no field recording which
   commit wrote which bytes, and §9.7 explicitly does not reconstruct history.
   So the violation is real, MUST-level, named, and witness-less, and it is
   neither registered nor accounted for. The same holds for step 5's
   pad-to-64-boundary obligation, which `[R-CNT-05]` expressly declares
   non-violating ("a longer gap is conforming, and no conforming commit
   produces one") — that one is at least covered in substance by §21.6's slack
   row.
2. **`[R-IDX-01]`.** "The entry for the tile with disk ordinal k (§11.4) is the
   k-th entry, at region byte 20·k; entry order is disk-ordinal order" is an
   ordinal mapping in exactly the sense §21.7 already names for `[R-GEO-06]`
   and `[R-SER-01]`: a structurally valid index satisfies the parse whatever
   order its entries are in, and no file-level witness distinguishes a
   correctly ordered index from a permuted one. It belongs in the same clause
   and is not there.

Permitted readings: (a) the list is illustrative and the omissions are
harmless; (b) the list is the account §21.1 designates and is therefore
incomplete. I picked (b) because §21.1 calls it "the account, by class, of what
fails it" — a definite article and a completeness word — and because the list's
own grammar closes with "and".

**What an implementer does wrong without it.** Nothing on the read path. The
cost falls on anyone auditing the register for completeness — the exercise
§21.1 now invites — who has to derive from scratch that `[R-LIF-02]` and
`[R-IDX-01]` are witness-less rather than missing rows, and who might instead
conclude the register has two gaps.

**Byte-level: NO.** No byte sequence's acceptance turns on where these two
obligations are accounted for; they are witness-less either way, which is
precisely the finding. Adding them to §21.7 changes no row, no outcome and no
vector.

---

### reader-06 — OBSERVATION — §20.3 `[R-WRT-04]`

**Location:** §20.3, `[R-WRT-04]` step 4 and the "three shapes a commit takes"
example, shape (c); against §14.5 `[R-SER-05]` and §11.1's rationale.

**Title:** §20.3 states the re-emission consequence of a fill change but not the
symmetric consequence of a geometry change that creates padding positions.

**Quotation (§20.3, shape (c)):**

> "**(c) A change confined to the directory** — clearing a slab declaration,
> renaming a layer, or changing a channel's fill value on a layer with no
> padding position and no pad bit. Only the directory is re-emitted. A fill
> change on a layer carrying either additionally requires re-emitting the
> affected stored tiles, whose content `[R-SER-05]` fixes — which makes it
> shape (b)."

**Quotation (§11.1, rationale):**

> "Growth that leaves every grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) unchanged touches the
> directory alone"

**Detail.** §14.5 makes padding content a *file* predicate, not merely a writer
instruction: "a verifier MUST check it, and a violation is a validity error at
tile scope" (rows T4, T5). Which positions of an edge tile are padding is a
function of Eᵢ and Tᵢ. A commit that **narrows** a dimension extent — nothing in
the document forbids it; §11.1 discusses only growth — turns real sample
positions into padding positions, and unless those positions happened already
to hold the channel's fill bytes, the layer's edge tiles now violate `[R-SER-05]`
and the committed file is nonconforming at tile scope. §20.3's step 4 lists
what a commit must re-emit and never mentions this; its shape-(c) example
states the exactly analogous rule for the *other* input to §14.5 (a fill
change) and stops there. §11.1's rationale reinforces the wrong instinct by
telling an implementer that a grid-count-preserving extent change "touches the
directory alone".

The same gap covers a tile-extent change, which alters P and every tile's
decoded size and would invalidate every stored tile, and which §20.3 likewise
does not address; there `[R-SER-07]`'s exact-size rule catches it at the reader,
so it is at least loud.

Permitted readings: (a) the file predicate governs — a commit that narrows an
extent must re-emit every affected edge tile with fill-encoded padding, or not
narrow it; (b) §20.3's step 4 is the complete procedure and no such re-emission
is required. I picked (a): `[R-CNF-05]` and `[R-CNF-06]` bind the updater to
emit only conforming files, and T4 is a file-conformance violation regardless of
which commit's bytes are at fault. (b) is not really defensible once §14.5 is
read as a predicate, which is why this is an observation about §20.3's
completeness rather than a contradiction.

**What an implementer does wrong without it.** An appender implementing an
"update layer extents" operation from §20.3's checklist emits a nonconforming
file on every shrink, with no reader-side symptom — T4 and T5 are
verifier-detected, so the damage is invisible until certification.

**Byte-level: NO.** The file predicate already decides which byte sequences are
conforming: an edge tile with non-fill at a padding position is nonconforming
whether §20.3 mentions it or not, and two competent implementations that read
§14.5 reach the same verdict. What is missing is a step in a procedure, not a
rule.

---

### reader-07 — OBSERVATION — §2.4 vs §21.3 rows L3/L5/L6

**Location:** §2.4's reject-layer row; §19.1 step 4; §21.3 rows L3, L5, L6;
§22.4 `[R-SEC-05]`.

**Title:** §2.4 licenses a reader to list a rejected layer's name in the one
case where the name is what was rejected, and does not say what it hands the
caller.

**Quotation (§2.4):**

> "**reject-layer** | The affected layer's data and metadata are not usable; all
> other layers are unaffected. A reader MAY still list the file's layers,
> including the rejected one's name."

**Quotation (§21.3, row L3):**

> "A layer record's name bytes are not well-formed UTF-8 | — | reader | open |
> `[R-ENC-11]`"

**Detail.** Three of the register's layer rows — L3 (ill-formed UTF-8), L5
(empty name), L6 (a code point in U+0000–U+001F) — reject a layer *because* its
name is unusable, and all three are detected at **open**, so a reader holds
them before any caller has asked for a layer. §2.4 then permits it to "list the
file's layers, including the rejected one's name", which in these three cases
means handing a caller either ill-formed UTF-8, an empty string, or a string
carrying C0 controls. §22.4's screening rationale — "Names are length-prefixed
and screened for C0 controls (`[R-ENC-12]`), which removes ESC-introduced escape
sequences and CR/LF injection from the identifiers a tool is most likely to
print" — is precisely the screening that has *failed* here, and §22.4 does not
carve out the rejected-name case.

Permitted readings: (a) the permission is a MAY and a careful reader simply
declines to list a layer whose name did not validate, listing it as unnamed or
by ordinal; (b) the permission covers these cases and the reader hands the raw
bytes onward with a caveat. I picked (a) for my implementation — I list such a
layer as `<invalid name, record #n>` — but the document does not say, and (b)
is what a literal reading gives.

**What an implementer does wrong without it.** Prints attacker-chosen C0 bytes
into a terminal, or hands ill-formed UTF-8 to a caller whose string type cannot
hold it, from a code path whose whole purpose was to be the graceful one.

**Byte-level: NO.** This is entirely about what a reader surfaces to a caller.
The file's verdict is fixed — reject-layer at open — and no byte sequence's
acceptance or emission changes with the answer.

---

## 8. Where I had to guess, and did not report

Recorded for honesty; none of these seemed to me to rise to a finding.

- **Region-request interval convention.** §19.4 says a region request "names a
  rectangular range of coordinates, one interval per dimension" without saying
  whether intervals are half-open or closed. It is an API surface, not a
  format property, and step 1's result ("the region's intersection with the
  extents") is well defined either way. I chose half-open.
- **Point vs region for a single coordinate outside the extents.** A point
  request *fails as a request*; the same coordinate expressed as a
  single-position region *succeeds and returns no samples*. §19.4 states both
  and explicitly notes that a single-position range is a region request, so
  this is deliberate, not a gap. I implemented both behaviours.
- **Whether a commit may narrow a dimension extent at all.** Nothing forbids
  it; §11.1 discusses only growth. I assumed it is permitted, which is what
  makes reader-06 reachable. If it is not permitted, reader-06 dissolves and a
  prohibition is missing instead.
- **Appendix G item 3's ordering of two top-level records of the same
  unassigned type.** The profile orders records "by type, and within type
  0x0001 by layer name", leaving same-type unassigned records unordered. I
  convinced myself this is unreachable rather than a gap: §10.3 forbids a
  conforming writer to emit reserved-range values at all and to emit
  experimental values "in released software or published data", and item 4
  pins the profile to a single generation, so a profile-following creator
  emits no such record. Not reported.
- **Whether a local reader that preads only two ranges must check the front
  block.** It must not — `[R-CNT-04]`'s test is residency, and the text says so
  three times in three sections. I checked this because it looked like a
  local/remote asymmetry and it is not one.

## 9. Confidence

**High.** I would ship a reader from this document without consulting anything
else, and the two byte-level findings are both in the *compactor*, which is the
one actor whose obligations are stated by reference to three other sections
rather than in one place. The read path — open, layer access, index chain,
decode, extract — is closed, ordered, and arithmetically correct everywhere I
could check it, and the register's completeness claim survived a
requirement-by-requirement audit.
