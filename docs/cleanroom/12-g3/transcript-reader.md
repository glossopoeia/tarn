# Cleanroom round 12 — Reader implementer transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,982 lines, read in five contiguous chunks covering lines 1–3983). I opened no
other file in the repository — no `docs/`, no ADRs, no `PLAN.md`, `AGENTS.md`,
`README.md`, no `conformance/`, no `spec/registry.json`, no git history, no web
access. I did not list any directory to discover what else exists.

I ran local computation only, in Python, over data I typed in myself or
generated: a CRC-32C implementation (reflected Castagnoli, poly 0x82F63B78),
arithmetic checks on the document's worked examples, a byte-level file builder
that constructs a TARN file from the document's rules, and an independent reader
that opens and reads it. I also ran three `grep`/`python` scans over the spec
file itself: an identifier census, an instance-count of the §21 register tables,
and a `structural`/`descriptive` occurrence scan. Scratch files I wrote and read:
`build.py`, `reader.py`, `file.tarn` in my own scratchpad. Nothing else.

---

## 1. Method

The charter says: implement, on paper but concretely, a conforming reader, in the
order the code would actually be written, and stop every time the text fails to
tell me what to do. I did that, and then I did something stronger: I built the
reader for real, in Python, from the document alone, together with a writer good
enough to feed it a non-trivial file (two channels, mixed element sizes,
interleaved, edge padding, two stored tiles and two sentinels). That converts
"the text is clear" from an impression into a test — if I had had to guess about
an offset, the file would not have read back.

I covered the six sections the brief named (Appendix G, §4.7, §9.7, §20.3, §13.1,
front matter) first, but the bulk of the walk below is §6–§8, §11–§19, and §21,
because that is what a reader is made of.

---

## 2. The open path, byte by byte

### 2.1 Step 1 — end of file

`[R-RDR-01]` step 1: obtain the transport-authoritative file size. `[R-CNT-10]`
fixes what counts: "a full-response content length, the complete length of a
range response, or a size probe", and forbids substituting
`committed_file_length` for it. For HTTP a suffix range `bytes=-64` returns
`Content-Range: bytes <a>-<b>/<total>`; the `/total` is the authoritative size,
so steps 1 and 2 cost one request between them, exactly as §6.4 claims.

A note on the symbol `F`. §9.1 and §15.3 define `F` as the live trailer's
committed file length; §19.1 step 1 and §21.2's F5 instance cell use `F` for the
*physical* file size. In a conforming file they are equal, and `[R-CNT-06]`'s
gate batch makes the inequality reject-file, so a reader never acts on a
divergent pair. I resolved it as: physical size in steps 1–2, `committed_file_length`
everywhere after, and nothing forked. Not a finding.

Before anything else: if the physical size is below 128 the file is rejected
(`[R-CNT-27]`, F5). I verified §5.1's arithmetic for the floor — a directory of
≥4 bytes at offset ≥16 ends no earlier than byte 20, and the trailer must begin
at a 64-aligned offset, so the earliest trailer start is 64 and the smallest file
is 128. A 64-byte file is impossible because [0,16) is the front block.

### 2.2 Step 2 — the trailer, in §6.2's fixed order

Fetch `[F-64, F)`. 64 bytes. The order is normatively fixed and I implemented it
literally:

1. `trailer magic == 8A 4E 52 41 54 0D 0A 1A` (F8; a byte-reversed magic is F1,
   the specialization).
2. `u32 @ 60 == CRC32C(trailer[0:60])` (F14).
3. version gate: `version_major == 0` → F18; `!= 1` → refuse on capability
   grounds (`[R-CNT-07]`, not a register row, §21.6's closing paragraph).

§6.2 explains why only these three come first: they are the only fields
`[R-CNT-24]` pins across all format majors. I checked that claim against
`[R-CNT-24]`: magic at F−64 (trailer 0–7), major/minor at F−56 (trailer 8–11),
CRC at F−4 (trailer 60–63) — 16 bytes fixed, 48 free, which matches
"A future major MAY redefine only the remaining 48 trailer bytes". `flags` sits
at trailer offset 12, inside the redefinable 48, which is why the flag gate is in
the *second* batch and not the first. That is a subtle piece of engineering and
it is correct.

Then, as one unordered batch, before acting on any of them: incompat-lane flags
zero (F19); `committed_file_length == transport size` (F17) and `% 64 == 0`
(F13); `dir_offset >= 16` (F9); `dir_length >= 4` (F16); `dir_offset + dir_length
<= F - 64` (F10, with `[R-ENC-04]`'s wrap check as F3); `1 <= generation <= 2^63-1`
(F11); `file_id != 0` (F12); reserved bytes [56,60) zero (F15).

Batch-not-sequence matters and the document knows it: `[R-VEC-02]` says
"§6.2's field gates are validated together, so a file failing two of them
attributes to neither alone". Since every failure is reject-file, order is
unobservable. No guess needed.

### 2.3 Step 3 — the directory

Fetch `[dir_offset, dir_offset + dir_length)`. `dir_length` bytes. What bounds
this range *before* I have read it: `dir_length >= 4` and `dir_offset +
dir_length <= F - 64`, both validated in step 2 from bytes the trailer CRC
covers. `[R-ENC-05]` is the rule that makes this ordering mandatory rather than
prudent — "A reader MUST NOT allocate, seek, or issue I/O based on any integer
obtained from a file before the checksum covering it has been verified".

Verify `u32 @ (dir_offset + dir_length - 4) == CRC32C` of the preceding
`dir_length - 4` bytes (F20). The record sequence is exactly those covered bytes:
`[dir_offset, dir_offset + dir_length - 4)`. §7.1's "the directory is always raw,
with no codec involvement on the open path" removes the last possible ambiguity
here.

### 2.4 Step 4 — the record walk

24-byte header, then `inline_length` bytes. Loop until the sequence is consumed;
any header or payload crossing the end, or any residue, is F29. Type 0 is F24 and
is explicitly *not* an unknown type.

Per-record at open: multiplicity (`[R-CNT-14]`, F34 for a second top-level
user-metadata record); the unknown-type MU gate (`[R-CNT-15]`, F35/F36); extent
slot rules for non-layer top-level records (`[R-CNT-13]`, F30/F31/F32); and, for
a top-level user-metadata record, the three framing checks — slot not (0,0)
(F21), `extent_length >= 5` (F22), `inline_length == 1` (F23).

The layer-name namespace is built here and this is where I looked hardest for a
gap, because §19.1 step 4 is doing three things at once. It resolves cleanly:

- A layer record whose *name field* does not fit inside its `inline_length`
  yields no name to compare; it contributes nothing to the namespace and is
  reject-layer under `[R-CNT-18]` (L23).
- Uniqueness is decided *first* and over raw bytes, "whether or not each name is
  itself well-formed". So two layer records both carrying a zero-length name are
  a duplicate (F4, reject-file) *and* each is L5 (reject-layer). Both rows fire;
  §24 already contemplates multi-row files.
- L3/L5/L6 (layer-record name UTF-8 / empty / C0 control) carry Detected = open
  with outcome reject-layer, so a reader must mark a layer dead at open without
  having touched anything else about it. That is unusual but stated, and it is
  the only reject-layer condition due at open.

### 2.5 Cold remote open — byte-exact cost

Two requests.

| # | Range | Bytes | What bounds it before I read it |
|---|---|---|---|
| 1 | suffix `bytes=-64` | 64 | the constant 64 (§6.2's fixed trailer size, `[R-CNT-24]`) |
| 2 | `[dir_offset, dir_offset+dir_length)` | `dir_length` | `dir_length >= 4`, `dir_offset >= 16`, `dir_offset+dir_length <= F-64` — all from the CRC-verified trailer |

Total = **64 + dir_length** bytes.

- Appendix A's minimal file: 64 + 4 = **68 bytes**, and the front block is not
  fetched. Appendix A states this and its arithmetic is right: a 112-byte
  speculative window over [16,128) captures the directory (containment satisfied,
  request 2 dropped) while leaving [0,16) non-resident, so `[R-CNT-04]`'s front
  check stays optional.
- My hand-built file (below): 64 + 126 = **190 bytes**, confirmed by
  instrumenting the transport: `[(256, 320), (124, 250)]`.

`[R-CNT-09]`'s writer SHOULD — `dir_length + pad + 64 <= 65,536` — is exactly the
condition under which a single 64 KiB suffix window covers `[dir_offset, F)`,
since `F - dir_offset = dir_length + pad + 64`. Checked; correct.

The working-set invariant is the real content of §6.4, and §19.1 restates it: the
open consumes the trailer and the directory and *nothing else*, at any file size
and layer count. No extent, no index, no payload. I implemented it and it holds.

---

## 3. Validation timing by tier

`[R-RDR-02]` fixes the *latest* detection point; `[R-CNF-12]` licenses earlier.
Divergence is therefore only ever toward earlier rejection. The four tiers, and
what I put in each:

**At open** — front block if resident (`[R-CNT-04]`; a reader that would need a
further range request MAY omit it entirely, and the two-request accounting
excludes it); the whole trailer; the directory CRC; the entire record walk
including framing, multiplicity, unknown-type MU gates, non-layer extent slots,
user-metadata framing and *encoding-byte value* (R1 is Detected = open for a
top-level record); and the layer-name namespace with each layer record's name
checked per §4.6.

**At first access to a layer** — everything `[R-RDR-03]` lists. I implemented all
of it: extent slot (`[R-CNT-13]`), the §7.4 constraint set (`[R-CNT-23]`),
alignment/slab exclusivity (`[R-CNT-16]`), exact parse and sub-record walk
(`[R-CNT-18]`), sub-record multiplicity (`[R-CNT-14]`), dimension and channel
name rules, the six value sets (§11.4 linearization, §12.2 sample type, §14.1
layout, §15.1/§7.4 index encoding, §17.2 codec, §17.3 filter), bool fill
(`[R-TYP-07]`), the lz4 declaration cap (`[R-COD-07]`), the geometry floor and
its arithmetic (`[R-GEO-01]`–`[R-GEO-03]` plus `[R-ENC-04]` over the derived
products), and the two index cross-checks (`[R-CNT-17]`: `entry_count` against
geometry, and `extent_length` against `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4`).
`[R-RDR-03]`'s closing claim — "layer access performs no fetch" — is true; I
verified it by construction, every check reads only the resident directory and F.

**At use of a tile** — the index chain (L37 `crc_of_crc_array`, L38 segment CRC,
both reject-*layer* though detected at tile use), the per-entry classification of
§15.3, the payload CRC, and the decode checks.

**At use of a record's extent** — the extent CRC and the document content rules
(R2–R10). "No earlier, since the open fetches no extent."

**What a reader is permitted never to check.** Every register row whose Detector
cell reads *verifier*: F7, F25, F26, F27, F28, F33, F36; L18, L25, L40, L41, L42,
L46, L47, L48, L49; T2, T4, T5, T26. Substantively that is: the live-state
coverage partition and slack total (§9.7), all extent overlap (§7.2), the
pre-trailer-pad emptiness rule (§6.2), reserved record flag bits and the
MU=1/PE=0 combination, a registered type's stored bits against §7.3, reserved-range
type values, alignment and slab invariants (§16), user-metadata member ordering
(`[R-MTA-05]`), and every decoded-*content* obligation — padding-position fill
(§14.5), pad bits, and interleaved boolean bytes (`[R-SER-08]`). A reader that
skips all of those is fully conforming; §22.3 says so plainly and draws the right
operational conclusion ("a pipeline accepting files from untrusted sources SHOULD
verify rather than merely read").

**What becomes a verdict when.** *Cannot establish* is reserved for a verifier
that established no violation and could not check something on a capability or
resource ground: unimplemented format major, an unimplemented MU=1 type, a codec
or filter it cannot execute (`[R-COD-11]`), a decode declined on resource grounds
(`[R-ERR-04]`), or a user-metadata document declined on its own bound
(`[R-MTA-09]`). An established violation always wins. *Unexamined* constrains the
report and not the verdict. This is one of the tightest parts of the document and
I found nothing to complain about in it.

---

## 4. Layer access and the tile-read algorithm — implemented

### 4.1 The layer record parse

Packed, no padding, in table order. Fixed prefix is `1 + len(name)` then
`layout u8`, `linearization u16`, `codec u16`, `filter u16`, `A u64`, `S u64`,
`A_slab u64`, `d u8`, `C u16` — i.e. `len(name) + 35` bytes. Then `d` dimension
entries (`1 + len(name) + 8 + 8`), then `C` channel entries
(`1 + len(name) + 2 + 1 + fill_len`), then `index_encoding u8`, `entry_count u64`,
`crc_of_crc_array u32`, then sub-records to the end.

The one place I expected trouble and did not find it: the fill field. §7.4 says
"fill length equals the type's element size (`[R-CNT-23]`), so fill parses without
type knowledge and validates with it". That is exactly right and it is what makes
the parse total — I can advance past a channel entry whose *type* is 0x8000 and
still reject the layer for L34 rather than losing framing. A fill prefix that
disagrees with the element size is L30; a prefix that runs past `inline_length` is
L23. Both reject-layer, so the order I check them in is unobservable.

`entry_count = 0` falls out of the generic path without a special case, which is
a small piece of design elegance worth recording: the CRC array is 0 segments =
0 bytes, `CRC32C(empty) = 0x00000000` (§4.5's second check vector), and §7.4
forces `crc_of_crc_array = 0`. So `CRC32C(fetched array) == crc_of_crc_array`
holds with no branch. L27 registers the nonzero case.

### 4.2 Grid and ordinal arithmetic

`G_i = ⌈E_i/T_i⌉` stated as `E/T + (1 if E mod T else 0)` — the document
explicitly refuses the `(E + T - 1)/T` idiom because the intermediate sum can
leave the declared 0..2⁶³−1 domain. `N = ∏G_i`, `P = ∏T_i`, addressed-tile count
`N` interleaved / `C·N` planar, total sample positions `N·P`. All subject to
`[R-ENC-04]` (L2).

In-tile ordinal `Σ u_i · ∏_{j>i} T_j`; spatial ordinal `s = Σ t_i · ∏_{j>i} G_j`;
disk ordinal `s` interleaved, `c·N + s` planar. I verified §11.4's example
independently: extents (1024,2048), tiles (256,256) → G=(4,8), N=32, P=65,536;
coordinate (300,700) → tile (1,2) → s=10, in-tile (44,188) → ordinal
44·256+188 = 11,452; planar channel 2 → disk ordinal 2·32+10 = 74. All correct.
§15.4's follow-on (entry at region bytes [1,480, 1,500); channel 3's tiles are
ordinals 96–127) is correct too.

### 4.3 Index region and the segment chain

Region = `entry_count × 20` bytes of entries, then `⌈entry_count/2¹⁶⌉ × 4` bytes
of segment CRCs, contiguous, no padding. Entry `k` at region byte `20k`. Segment
`s` covers `[s·2¹⁶, min((s+1)·2¹⁶, entry_count))`; a partial final segment's CRC
covers only its actual bytes.

To use entry `k`: fetch the CRC array at
`[extent_offset + entry_count·20, +nseg·4)` and verify against
`crc_of_crc_array`; fetch segment `k div 2¹⁶` and verify against the `s`-th u32.
Both ranges are computable from the layer record alone, so they may go in
parallel. Either failure is reject-**layer** even though it is detected at tile
use — that asymmetry is stated three times (§8.2, `[R-IDX-04]`, `[R-RDR-02]`) and
I got it right only because it is stated three times.

I reproduced §15.4's worked example exactly: `entry_count = 1,000,000` → 16
segments (15 full, last covering 16,960), 64-byte CRC array, region 20,000,064
bytes; tile 999,999 in segment 15 at segment-relative byte 339,180; CRC array at
[20,000,000, 20,000,064) and segment 15 at [19,660,800, 20,000,000). Also checked
§21.9's note: at 2³² tiles the CRC array is exactly 256 KiB, at 2³⁶ exactly 4 MiB,
and a full segment is exactly 1.25 MiB.

**Verified constant.** I computed `CRC32C` of 2¹⁶ concatenated sentinel entries
(`FF ×16 00 ×4`) and got **0xEECB3BB2**, matching `[R-IDX-05]` and Appendix B.
I also confirmed `CRC32C("123456789") = 0xE3069283` and `CRC32C(∅) = 0x00000000`.

### 4.4 Entry classification (§15.3)

Six rows are marked *structural*; I counted the table and there are exactly six,
matching the prose. They map to register rows T6, T7, T8, T10, T11, T9/T12.

The one thing worth recording: T11 ("offset or length exceeds 2⁶³−1 … the value
being distinct from the all-ones sentinel") is drafted so as *not* to swallow T6
and T7. Without that qualifier every one-field sentinel would also be a T11 and
the corpus row attribution would be ambiguous. It is there. Good.

The sentinel rationale is load-bearing and correct: a zeroed region parses as
offset 0 / length 0 → structural reject-tile, not as a silently all-sparse index;
an all-0xFF region fails because a sentinel's crc field must be 0.

### 4.5 Decode pipeline

Reader order: verify entry crc over the stored bytes → codec decode → filter
inverse → the result is the decoded tile image, length exactly the decoded size
(`[R-SER-07]`). Both stages consume and produce whole tiles and carry no state
between tiles (`[R-COD-02]`).

Decoded size and offsets:

| Layout | Decoded size | Offset of value k |
|---|---|---|
| planar numeric channel c | `P · B_c` | `k · B_c` |
| planar bool channel | `⌈P/8⌉`, bit `k mod 8` of byte `k div 8`, LSB-first | — |
| interleaved | `P · Q`, `Q = Σ B_i` | `(k div C)·Q + F_{k mod C}` |

Equivalently, channel `c` at in-tile ordinal `u` sits at `u·Q + F_c`
interleaved, `u·B_c` planar. I verified §14.2's worked example (tiles (2,3), P=6,
uint8+uint16 → Q=3, size 18, ordinal 5 at bytes [15,18); planar `b` plane 12
bytes with ordinal 5 at [10,12); float32+bool → Q=5, size 30, ordinal 5 at
[25,30) with the bool at byte 29) and §14.3's (P=10 alternating → `55 01` with
fill false, `55 FD` with fill true).

Byte-shuffle: stride `s` = channel element size (planar), `Q` (interleaved), 1
and identity (packed bool plane). Forward puts byte `i` of group `j` at `i·n + j`
with `n = L/s`; the inverse restores `i·n + j` to `j·s + i`. I implemented both
and round-tripped §17.3's example — forward produced
`00 00 00 00 00 00 80 00 40 3F 40 40`, byte-identical to the document, and the
inverse recovered 1.0, 2.0, 3.0. `L` is divisible by `s` in all three cases
(`P·B_c`/`B_c`, `P·Q`/`Q`, `⌈P/8⌉`/1), as §17.3 asserts.

Codec 1's length equality (`[R-COD-04]`, T14) is checkable from the entry and
layer record alone, before any payload fetch. My reader does it there, which
saves a wasted range request on a corrupt entry.

### 4.6 The worked example I built

Not Appendix A's — that file has no layer. I built one that exercises the parts a
reader actually gets wrong: two channels of different element sizes, an edge tile
with padding positions, and a mix of stored and sentinel entries.

Declarations: layer `L`, interleaved, linearization 1, codec 1, filter 1, no
alignment, no slab, rank 2, C=2. Dimensions `y` E=3 T=2, `x` E=4 T=2. Channels
`a` uint8 fill `00`, `b` uint16 fill `CD AB` (0xABCD).

Derived: `G = (2,2)`, `N = 4`, `P = 4`, `Q = 3`, decoded size `12`,
`entry_count = 4`, index region `4·20 + 1·4 = 84`.

Layout:

```
[0,16)      front signature block
[16,28)     tile 0 payload      12 bytes
[28,40)     tile 3 payload      12 bytes
[40,124)    tile-index region   84 bytes  (4 entries + 1 segment CRC)
[124,250)   directory region   126 bytes  (24 hdr + 98 inline + 4 CRC)
[250,256)   pre-trailer pad      6 bytes  (slack, zeroed)
[256,320)   trailer             64 bytes  F = 320, 320 mod 64 = 0
```

Layer-record inline payload length worked by hand: `2 + 1 + 2 + 2 + 2 + 8 + 8 + 8
+ 1 + 2 + 18 + 18 + 6 + 7 + 1 + 8 + 4 = 98`. The builder agreed. Directory
`24 + 98 + 4 = 126`. `dir_offset + dir_length = 250 <= F - 64 = 256`. ✔

Tile 3 is the edge tile (t = (1,1)), covering y∈{2,3}, x∈{2,3}. y=3 is outside
`E_y = 3`, so in-tile ordinals 2 and 3 are padding positions and `[R-SER-05]`
fixes their content to fill: `00 CD AB` each. Its 12 bytes are
`14 55 55 | 15 66 66 | 00 CD AB | 00 CD AB`.

Reads (each read's ranges instrumented):

| coordinate | result | ranges fetched |
|---|---|---|
| (0,0) | a=0x0A, b=0x1111 (stored) | CRC array [120,124), segment [40,120), payload [16,28) |
| (2,2) | a=0x14, b=0x5555 (stored) | [120,124), [40,120), [28,40) |
| (2,3) | a=0x15, b=0x6666 (stored) | same, payload [28,40) |
| (2,0), (2,1) | a=0x00, b=0xABCD (**fill**) | [120,124), [40,120) — *no payload I/O* |
| (3,0) | request fails — outside extents, no verdict on the file | none |
| (0,4) | request fails — outside extents | none |

Cold remote open of this file: 2 requests, 190 bytes. One cold tile read: 3
requests, 4 + 80 + 12 = 96 bytes (and the first two are cacheable per §15.4's
note and `[R-LIF-03]`).

Nothing in this construction required a guess. Every offset, every length, every
returned bit pattern came out of the document.

### 4.7 Appendix A and the checkable constants

I recomputed the trailer CRC of Appendix A's file from its documented field
values and got **0xE00938D2**, stored `D2 38 09 E0` — matching both the table and
byte offset [124,128) of the hex dump. I cross-checked every row of the
annotation against the dump: magic, `01 00` / `00 00` at [72,76), flags zero,
generation 1 at [80,88), dir_offset 16, dir_length 4, committed length 128,
file_id `EF CD AB 89 67 45 23 01`, reserved zero. All consistent. The empty
directory's CRC is `00 00 00 00` because CRC-32C of zero bytes is zero, which
§4.5 states and I confirmed.

**Every stated constant, offset and checksum in this document that I could check,
checks.** That includes: 0xE3069283, 0x00000000, 0xE00938D2, 0xEECB3BB2, the
bfloat16 identification (0x3F80 = binary32 1.0's high half; 0x7FC0 = qNaN), the
`température` NFC/NFD lengths (12 vs 13 bytes) and its exact UTF-8, the twelve-byte
channel-entry example `04 74 65 6D 70 0C 00 04 00 00 C0 7F`, the §14.5 padding
example (32-byte edge tile, values 1–15 each `CD AB`), the §20.3 example
(32·20+4 = 644), the §15.4 examples, the §21.9 note's 256 KiB / 4 MiB / 1.25 MiB,
and the zstd/lz4/gzip magics.

I also mechanically counted the §21 register: 36 + 49 + 26 + 10 = **121 rows**,
and summing the Instances cells by the rule §21.1 states (semicolon-separated,
a `—` cell counting as one) gives **248 instances**. Both match §21.8's
"121 conditions over 248 instances" exactly. I checked the identifier census too:
no gaps in any prefix's numbering except `[R-SER-04]`, which §14.4 declares
withdrawn and permanently retired.

---

## 5. Degradation walks

**(1) Unknown top-level record type 0x8123 (experimental), MU = 0, PE = 0.**
Open parses the header; the type is unknown; MU = 0 → ignore-record
(`[R-CNT-15]`). The file is *conforming* — §10.3's prohibition on publishing
experimental values binds the writer's conduct, not the bytes (`[R-CNF-02]`,
§21.6). The reader still validates the record's extent slot at open (F30/F31/F32)
even though it will never read the extent, because `[R-CNT-13]` scopes a
malformed slot on a non-layer top-level record to the file. Its extent is covered
by no checksum at all (§8.1's last row), so corruption inside it is invisible —
§22.3 states this as a residue rather than defending it. Served to the caller:
everything. Same record with MU = 1 → reject-file, and §21.6's closing paragraph
records this as a *conforming file a reader nevertheless refuses*, which the
diagnostic ought to distinguish from corruption.

**(2) Unknown codec value 7 on layer B, in a file with layers A and B.**
Open succeeds; the layer table has both. First access to B hits `[R-COD-03]` →
reject-layer (L43). Served: all of layer A, plus B's *name* — §2.4 explicitly
permits listing a rejected layer. Not served: any sample, any declaration-derived
answer about B. The outcome is prospective, so anything already returned stands.
A verifier reports nonconforming (a reserved codec value is a violation). Contrast
with a reader that cannot execute an *assigned* codec: that reader is simply not
conforming (`[R-CNF-03]`), and a *verifier* in that position reports
cannot-establish (`[R-COD-11]`).

**(3) Truncated tail.** Physical size 1,000,000 against a trailer claiming
1,000,064. The reader takes the final 64 physical bytes, which are payload or
index, so the magic check fails → F8 → reject-file, reported as torn or invalid
(`[R-LIF-05]`), and the reader MUST NOT scan backward. Served: nothing. What
makes this recoverable rather than fatal is that trailer *n* and everything it
reaches are byte-intact; §9.6's deliberate probe finds it, and recovery output
must be re-verified as a whole file before use. If the truncation lands exactly on
an earlier commit boundary the file simply *is* that earlier generation, and §9.6
says so — rollback detection needs out-of-band state.

**(4) Segment CRC mismatch while reading tile 5 of layer L.** §19.4 step 3 →
`[R-IDX-04]` → reject-**layer**, not reject-tile, even though detection happened
at tile use. Per step 8 the failure "bars the request's remaining entries and all
further service from the layer"; values already returned under §19.2's timing
stand. Served: other layers, in full; nothing further from L. Fill is *never* a
fallback here — `[R-TYP-09]` and `[R-CNF-09]` both forbid it, and the rationale
under §13.3 explains why (otherwise corruption could silently convert "stored"
into "absent, reads as fill").

**(5) Tile CRC mismatch (T1).** reject-tile. The entry is well-formed, so its
extent still stands for the coverage walk and for slab run continuity — §15.3 and
§9.7 both say this explicitly, and it is the distinction that makes L41's slab
check decidable from index bytes alone. Served: every other tile of the same
layer, and for a region request the reader MAY return the validating entries'
values with a per-entry report of the failures, or fail the whole request — but
MUST NOT substitute fill for the rejected tile's positions.

**(6) Limit exceeded.** A layer declaring a 512 MiB decoded tile is *conforming*
(§21.9's table is minimum guarantees, not caps), and a reader MAY decline it "at
the whole file, or at the narrowest scope whose declarations exceed what it can
serve, a layer or a tile". The refusal MUST be reported as a resource limit and
not as a validity error — §21.9's reasoning ("a reader that reports 'too large'
as 'corrupt' invites the deletion of intact data") is the right one. A verifier
that declines a decode on this ground reports cannot-establish for the affected
requirements. The one asymmetric case: an oversized *user-metadata document* has
no declared size, so `[R-MTA-09]` gives a reader two exits — ignore-record for
that record, or an `[R-ERR-04]` decline at the whole file. Both are licensed;
neither is a defect.

**(7) Format major 2.** Magic and CRC verify (their positions are permanent),
then the version gate refuses on capability grounds. `[R-CNT-07]` asks for a
diagnostic distinct from both "not a TARN file" and "corrupt". The file is
neither conforming nor nonconforming under this document; a verifier reports
cannot-establish. Not a register row, deliberately.

**(8) Ignore-lane flag bit 20 set.** Ignored; file conforming; an updater MUST
copy it forward and MUST NOT clear it, and a compactor carries it into its output
trailer rather than writing flags = 0. Incompat-lane bit 3 set → F19,
reject-file.

**(9) Unrecognized enum: layout = 3.** reject-layer (L36). Same shape for
linearization ≠ 1 (L33), sample type outside 1–13 (L34), index_encoding ≠ 1
(L31), filter outside 1–2 (L45). All at layer access, all decidable with no I/O.

**(10) Unreadable user-metadata document.** Every path — bad extent CRC (R2),
encoding 0 or reserved (R1), decode failure (R3), a broken zstd frame constraint
(R4), ill-formed UTF-8 or an unpaired-surrogate escape (R5), a bad key (R6, R10),
non-object or malformed JSON (R7), a non-finite number (R8), a duplicate key (R9)
— lands on ignore-record with a SHOULD-report, *whatever the containing scope*.
That is the quarantine, and it is what makes application metadata safe to carry.
The quarantine stops at the framing: a (0,0) slot, `extent_length < 5`, or
`inline_length != 1` are scope-level errors (F21/F22/F23, L10/L11/L12) "because
that failure precedes the document". Served in the ignore-record case: all sample
data, all geometry, everything except that one record.

---

## 6. Findings

Three. One I believe forks what a conforming implementation may emit; two are
places where I had to choose a reading and the document did not choose for me.

---

### reader-01 — CONTRADICTION — §20.3 `[R-WRT-04]` step 2 vs §2.3 `[R-CNF-05]`/`[R-CNF-06]` and §20.5 `[R-WRT-06]`

**Location.** §20.3 (`[R-WRT-04]`, step 2 and step 4); §2.3 (`[R-CNF-05]`,
`[R-CNF-06]`); §20.1 (`[R-WRT-01]`); §20.5 (`[R-WRT-06]`).

**Quotation.** §20.3, step 2 of the append procedure:

> "The open establishes no tile-scope violation — it consumes the trailer and
> directory only (`[R-RDR-01]`) — and a malformed index entry an appender meets
> while re-emitting a region is carried forward byte-identically at its
> disk-ordinal position under step 4, not repaired to a sentinel. Against any
> other structure the appender carries forward, it MUST NOT repair the defect —
> `[R-LIF-01]` freezes the committed prefix — and MUST NOT drop the record
> (§20.4); re-emitting it byte-identically is not authorship, since `[R-WRT-05]`
> makes only *a record it modifies* new output under `[R-CNF-05]`."

Against §2.3:

> "A writer MUST emit only conforming files. `[R-CNF-05]`"

and

> "An updater MUST satisfy every writer requirement for the bytes it produces,
> and additionally MUST honor the preservation obligations of §20.4 … `[R-CNF-06]`"

and, for the exactly analogous case one tier up, §20.5:

> "A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges fails,
> and MUST NOT emit a file carrying a violation it has detected: it can neither
> drop the structure (§20.4, `[R-WRT-07]`), nor re-emit it corrected
> (`[R-WRT-05]`)."

**The problem.** Step 4 of the same append procedure says the affected layer's
"tile-index region [is] re-emitted in full — entry_count entries plus the segment
CRC array — necessarily at a new placement (`[R-LIF-01]`)". So the appender is
*authoring* those bytes: a new region, at a new offset, with recomputed segment
CRCs, addressed by a re-pointed extent slot. Step 2 then directs it to write a
structurally malformed entry (say `offset = 5`, a T8) into those freshly authored
bytes. The output file therefore carries a register-row violation that the
appender itself created bytes for.

The document supplies a reconciliation for every neighbouring case and withholds
it here:

- For *records*, §20.3 says byte-identical re-emission "is not authorship, since
  `[R-WRT-05]` makes only a record it modifies new output under `[R-CNF-05]`".
  That clause is expressly scoped to "any **other** structure" — i.e. not the
  index entry — and `[R-WRT-05]` governs records in the directory, not entries in
  a re-emitted extent.
- §20.1's carve-out is "a violation latent in a structure they neither modify nor
  rely on travels with it". The tile-index region is a structure whose owning
  scope §15.1 fixes at the layer, and the appender both modifies it (new
  placement, changed entries, recomputed CRCs) and relies on it (`[R-WRT-03]`
  obliges the index chain "for every segment whose entries the commit reuses").
  So the carve-out does not reach it.
- §20.5 shows the document knows how to say "refuse", and says it for a compactor
  meeting the same defect class.

**Permitted readings.** (a) §20.3 is the specific rule and governs: the appender
commits, and emits a file carrying the T-row. (b) `[R-CNF-05]`/`[R-CNF-06]`
govern the bytes the appender produces, and since it cannot repair (step 2),
cannot drop, and cannot leave the region unchanged (step 4 forces re-emission),
its only lawful move is to refuse the commit, as a compactor must.

**Which I picked and why.** I implemented (a) — §20.3 is later, more specific,
and phrased as a direct instruction about this exact situation, and §21.7's
philosophy ("this format detects corruption of structure, not incorrectness of
content" and a verifier's office is certification) leans that way. But I recorded
it as a guess, because reading (b) is what §20.5 does with the identical defect.

**What an implementer does wrong without it.** Under (a) a repair tool that
appends a checkpoint commit to a damaged file silently propagates a tile-scope
defect into a brand-new index region and reports at most a SHOULD-level warning.
Under (b) the same tool refuses and the operator is sent to recovery. Those are
opposite operational outcomes for the same input.

**Byte-level: yes.** Updater A (reading (a)) writes a new index region whose
20 bytes at region offset `20·7` are `05 00 00 00 00 00 00 00 | 0C 00 00 00 00 00
00 00 | <crc>` — an entry with `offset = 5 < 16` — and commits, producing a file
on disk. Updater B (reading (b)) emits nothing. The question "may a conforming
updater emit that byte sequence?" has two defensible answers in this text, which
is exactly the emission fork the test names. The honest counter, which I state
because it may sink the finding at triage: the resulting *file* is nonconforming
under either reading, so no reader and no verifier disagrees about how to treat
it once it exists — the fork is over whether a conforming updater may bring it
into existence, not over any reader's verdict.

---

### reader-02 — AMBIGUITY — Appendix G item 3 gives no tie-break for two top-level records sharing an unassigned type

**Location.** Appendix G, item 3.

**Quotation.**

> "Records are ordered by type, and within type 0x0001 by layer name; a layer
> record's sub-records are ordered by type, and within a type by their encoded
> bytes compared lexicographically — an order a reader can derive, which a
> creation order is not — record order carries no meaning (`[R-CNT-14]`), so it
> is otherwise free to vary, as is structure placement (`[R-LIF-02]` step 2)."

**The problem.** The profile's purpose is to close every degree of freedom that
keeps two writers from emitting identical bytes, and item 3 is the emission-order
item. It supplies a total order for sub-records (by type, then by encoded bytes
lexicographically) and for type 0x0001 (by layer name, unique by `[R-ENC-15]`).
At top level it stops at "ordered by type". Type 0x0002 is bounded to one
occurrence by `[R-CNT-14]`, so the only ambiguity is among top-level records
sharing an *unassigned* type — and `[R-CNT-14]`'s multiplicity rules bound nothing
there: "multiplicity rules are per type — in format major 1: any number of layer
records …; at most one file-scope user-metadata record …; and at most one
user-metadata sub-record per layer record." A file may carry two top-level records
of experimental type 0x8000. Their order in the directory, and the order of their
extents in the emission pass, are undetermined.

**Permitted readings.** (a) The sub-record tie-break — encoded bytes compared
lexicographically — is meant to apply at both levels and was simply written once.
(b) Top-level records of the same unassigned type may be emitted in any order,
and the profile does not fix the file's bytes for such a file.

**Which I picked and why.** (a). It is the only order "a reader can derive", which
is the criterion item 3 states for choosing it, and it makes the rule uniform.
But the text says "a layer record's sub-records", and that qualifier is doing
work everywhere else in the sentence, so I could not treat (a) as the text's
meaning rather than my repair of it.

**What an implementer does wrong without it.** Two implementations both claiming
profile conformance emit different files for the same input, which defeats the
profile's whole reason to exist — and, per the appendix's own note, profile
conformance "can be refuted cheaply but confirmed only by reproducing the file",
so the divergence surfaces as a false refutation.

**Byte-level: no.** Appendix G is non-normative and "adds no requirement to any
actor: a writer ignoring it is fully conforming". Both orders produce conforming
TARN files that every conforming reader accepts identically; `[R-CNT-14]` makes
record order carry no meaning. Nothing about accept/reject changes, and the set
of emittable conforming byte sequences is unchanged — only the profile's claim to
determine a single one within that set.

---

### reader-03 — AMBIGUITY — §19.3's definition of "first access" makes every layer's first access fall at open

**Location.** §19.3 (`[R-RDR-03]`), against §19.1 step 4 (`[R-RDR-01]`) and
§19.2's tiering and rationale (`[R-RDR-02]`).

**Quotation.** §19.3:

> "A reader's **first access** to a layer — the first operation using any of the
> layer's declarations — MUST be preceded by full validation of the layer record
> — extent slot and inline payload both …"

§19.1 step 4, which every open performs for every layer record:

> "build the layer table: each layer record's name, parsed and checked per §4.6
> (`[R-ENC-12]`)."

§19.2's rationale:

> "The open's I/O stays two requests regardless of layer count; its one
> namespace-wide obligation — parsing each record's name — runs over bytes
> already fetched and CRC-verified."

**The problem.** A layer's name is one of its declarations — it is a field of the
layer record's inline payload, §4.7 classifies it structural, and §19.3's own
list includes the name rules among what full validation covers. The open uses it
for every layer, unconditionally. Read literally, then, every layer's "first
operation using any of the layer's declarations" happens during step 4 of the
open, and §19.3 requires full validation of *every* layer record to precede it —
which collapses the two-tier scheme §19.2 builds and contradicts the rationale's
claim that the open's only namespace-wide obligation is name parsing.

**Permitted readings.** (a) "The layer's declarations" excludes the name, because
§19.2 places the name at the open tier and the rest at the layer-access tier; the
tiers are the definition and §19.3's phrase is shorthand. (b) Literal: any use of
any declaration, name included, triggers full validation, so an open validates
every layer record. (c) A middle reading: the name is a declaration but the open's
use of it is exempted by §19.2's explicit tier assignment, while a *caller-visible*
operation that surfaces the name (a `list_layers()` call) is a first access.

**Which I picked and why.** (a). §19.2's bullets are the operative statement of
timing — they name the front block, trailer, directory, record walk and
layer-name namespace at open, and "the full validation of that layer's record" at
first access — and its rationale states the intended cost. Reading (b) would make
`[R-RDR-01]`'s claim that the open's working set is "the trailer and the
directory, and nothing else, at any file size and layer count" true of I/O but
false of work, at 65,536 layers.

**What an implementer does wrong without it.** Under (b) or (c), opening a
65,536-layer file fully parses and validates every layer record — every dimension
entry, every channel entry, every fill length, every enum — before the caller has
named a layer. That is the cost §19.2's rationale exists to disclaim. Under (a)
the open parses one name per record. The two differ by orders of magnitude in
open latency for exactly the file shape §21.9's layer-count guarantee is sized
for.

**Byte-level: no.** Both readings reject the same layers and serve the same
bytes; they differ only in *when* the rejection is computed, and `[R-CNF-12]`
already licenses any reader to detect earlier. §2.4 independently permits listing
a rejected layer's name, so even the caller-visible behaviour of `list_layers()`
is the same under all three readings.

---

## 7. What I could not determine, and what I am confident about

I found no defect in any constant, offset, checksum or worked example — I checked
every one I could compute, and they all reproduce, including the two that require
a CRC engine (0xE00938D2 and 0xEECB3BB2). The register's own arithmetic (121 rows,
248 instances) is self-consistent under the counting rule §21.1 states. The
identifier space has no gaps and no wrongly-cited governing rule that I could
find; in particular `[R-CNF-04]` really is the identifier terminating the
paragraph that obliges a reader to detect every reader-assigned register row, so
§19's preamble and §21.1 cite it correctly.

The reader path is implementable end to end from this document alone. I wrote it,
fed it a file with padding positions, sentinels, mixed element sizes and an edge
tile, and it returned the right bit patterns and the right fills without my ever
having to invent a rule. The three findings above are the only places where I
chose a reading rather than read one, and only the first of them touches bytes.

Confidence that two independent implementations built from this text alone would
interoperate: **high** for readers; the one place I would expect them to differ is
updater behaviour on a pre-existing malformed index entry (reader-01), which is
outside a reader's path.
