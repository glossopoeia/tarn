# Round 8 — Reader implementer, working transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 3,842 lines, in four `Read` calls). I opened no ADR, no `docs/` file, no
`conformance/` artifact, no `registry.json`, no `PLAN.md`, no `AGENTS.md`, no
`README.md`. I ran no `git` command of any kind and did no web access. I ran
`grep` twice against that same file (to pull the §21 register rows and to
confirm four Detected cells). I ran three Python scripts that read no file
except `spec/tarn.md` (a `count.py` that re-parses the register tables) and
their own siblings in the scratchpad: a CRC-32C implementation, a TARN file
builder, and a reader. I wrote four files into the scratchpad
(`crc.py`, `count.py`, `build.py`, `reader.py`, `reader2.py`, `worked.tarn`)
and this transcript. I did not list or read the scratchpad directory.

Prior knowledge of other array/image formats was used only to generate
suspicions (e.g. "does the zstd window rule interact badly with tiny tiles?");
every suspicion was settled against this document's own text or against
arithmetic, never against outside knowledge.

---

## 1. Ground truth first: does the document's own arithmetic hold?

Before writing a line of reader code I checked every constant and checksum the
document states that I could actually compute. This is cheap and it is where a
spec most often lies to you.

CRC-32C per `[R-ENC-09]`: Castagnoli, reflected in/out, init `0xFFFFFFFF`,
final XOR `0xFFFFFFFF`. Implemented as the reflected table with polynomial
`0x82F63B78`.

| Claim | Section | Computed | Verdict |
|---|---|---|---|
| CRC-32C("123456789") = `0xE3069283` | §4.5 | `0xE3069283` | ✅ |
| CRC-32C(∅) = `0x00000000` | §4.5 | `0x00000000` | ✅ |
| Appendix A trailer CRC = `0xE00938D2`, stored `D2 38 09 E0` | App. A | `0xE00938D2` → `d2 38 09 e0` | ✅ |
| CRC-32C of 2¹⁶ sentinel entries = `0xEECB3BB2` | §15.4, App. B | `0xEECB3BB2` | ✅ |

The sentinel-segment constant is the one I most expected to be wrong (it is
1,310,720 bytes of `FF×16 00×4` and nobody recomputes it by hand). It is
right.

Hand-checked arithmetic, all of which holds:

- **§11.2 example.** E=(1024,2048), T=(256,256) → G=(4,8), N=32, P=65,536. With
  E_y=1000, G_y = ⌈1000/256⌉ = 4. ✅
- **§11.4 example.** (300,700) → t=(1,2), s = 1·8+2 = 10; u=(44,188), in-tile
  ordinal 44·256+188 = 11,452; planar C=4 channel 2 → disk ordinal 2·32+10 = 74. ✅
- **§14.2 example.** Interleaved T=(2,3), P=6, `a` uint8 + `b` uint16 → Q=3,
  decoded 18; ordinal 5 at bytes [15,18). Planar `b` plane = 12 bytes, ordinal
  5 at [10,12). `t` float32 + `m` bool → Q=5, decoded 30, ordinal 5 at [25,30),
  `m` at byte 29. ✅
- **§14.3 example.** Planar bool T=(2,5), P=10, alternating from true: byte 0 =
  bits 0,2,4,6 set = `0x55`; byte 1 = bit 0 set = `0x01`; with fill true the
  pad bits 2–7 set → `0x01 | 0xFC = 0xFD`. So `55 01` / `55 FD`. ✅
- **§14.5 example.** E=(5,5), T=(4,4) → grid 2×2; edge tile (1,1) spans 4–7 on
  both axes = 16 positions, 1 real ((4,4)) and 15 padding; uint16 → 32 decoded
  bytes, values 1–15 each `CD AB`. ✅
- **§17.3 example.** float32 1.0/2.0/3.0 = `00 00 80 3F 00 00 00 40 00 00 40 40`,
  s=4, n=3. Applying "byte i of group j goes to offset i·n+j" I get
  `00 00 00 00 00 00 80 00 40 3F 40 40`. ✅ (I checked this by executing the
  permutation, not by eye.)
- **§15.4 example.** entry_count 1,000,000 → 16 segments (15 full + 16,960);
  CRC array 64 bytes; region 20,000,064 bytes; k=999,999 in segment 15 at
  segment-relative byte 20·16,959 = 339,180; CRC array at [20,000,000,
  20,000,064); segment 15 at [19,660,800, 20,000,000) = 339,200 bytes ≈ 339 KB;
  full segment = 65,536·20 = 1,310,720 = 1.25 MiB. ✅ every figure.
- **§15.4 second example.** C=4, N=32, channel 2 at s=10 → ordinal 74, entry at
  region bytes [1,480, 1,500); channel 3 = ordinals 96–127, 32 sentinels. ✅
- **§20.3 example.** 32-tile layer index = 32·20 + ⌈32/2¹⁶⌉·4 = 644. ✅
- **§21.9 note.** 2³² tiles → 2¹⁶ segments × 4 = 256 KiB; 2³⁶ → 4 MiB. ✅
- **§6.3 `[R-CNT-24]`.** magic at F−64, version at F−56 (trailer offset 8 ✅),
  CRC at F−4 over [F−64, F−4) = trailer [0,60) ✅; 64 − 8 − 4 − 4 = 48
  redefinable bytes ✅; major-1 trailer fields sum to
  8+2+2+4+8+8+8+8+8+4+4 = 64, "zero slack" ✅.
- **§5.1 128-byte floor.** 16 (front) + 4 (minimum directory) = 20; next
  64-aligned trailer start is 64; F = 128. ✅
- **§19.4 note (planar all-channel).** Entries at c·N+s spaced N apart; for
  N ≥ 2¹⁶ any two differ by ≥ 2¹⁶ so they cannot share a 2¹⁶-ordinal segment. ✅

**Register self-consistency.** I re-parsed §21.2–§21.5 mechanically and counted
instances by §21.1's stated rule (semicolon-separated; a `—` cell is one
instance):

```
F: 39 rows,  61 instances
L: 50 rows, 102 instances
T: 26 rows,  45 instances
R: 10 rows,  44 instances
   125 rows, 252 instances
```

§21.2 says "39 conditions", §21.3 "50", §21.4 "26", §21.5 "10", and §21.8 says
"125 conditions over 252 instances". Every number matches, and the identifiers
are contiguous F1–F39, L1–L50, T1–T26, R1–R10 with no gaps. That is a stronger
result than it looks: it means the instance-counting rule in §21.1 is
mechanically applicable and someone applied it.

Appendix B and Appendix C were checked row by row against their defining
sections. No divergence.

Conclusion of this pass: **every stated constant, offset, and checksum in the
document that I can compute is correct.** The high-value failure the charter
invited me to look for is not there.

---

## 2. The open path, byte by byte

I wrote a reader in the order I would actually write the code, with a
`Transport` object that models a ranged-request server and counts requests
and bytes. Notes below record where I had to make a call.

### Step 1 — F

`[R-CNT-10]` requires a *transport-authoritative* size and forbids
substituting `committed_file_length`. §6.4 and §19.1 step 1 fold this into the
suffix request: an HTTP `Range: bytes=-64` returns 206 with
`Content-Range: bytes X-Y/F`, so F arrives with the trailer. **One request for
steps 1 and 2 between them.** If the server answers 200 with the whole body,
`[R-CNT-10]` says handle it deliberately — and note the consequence: the whole
body means bytes [0,16) are now *resident*, so `[R-CNT-04]` flips from "MAY
omit" to "MUST verify". That interlock is clean and I did not have to guess it.

**What bounds the range before I have read anything:** nothing in the file —
the 64-byte trailer size at a 64-aligned end is fixed *permanently across every
format major version* by `[R-CNT-24]`. That is what makes the first request
safe against a file whose major I do not implement.

### Step 2 — trailer, in §6.2's mandated order

`magic → trailer CRC → version gate → everything else`. §4.5 pre-empts the
obvious objection (checking the magic before the CRC looks like "acting on"
unverified bytes): "comparing a field against a constant for validation is not
acting on it". Good.

My gate list, each mapped to its register row:

```
trailer[0:8]  != 8A 4E 52 41 54 0D 0A 1A     -> F10  reject-file
u32@60        != CRC32C(trailer[0:60))       -> F16  reject-file
version_major == 0                            -> F20
version_major != 1 (unimplemented)            -> F21  (diagnostic MUST be distinct)
flags & 0xFFFF                                -> F22
flags >> 16                                   -> ignored (§21.6, conforming)
committed_file_length != F                    -> F19
committed_file_length % 64                    -> F15
F < 128                                       -> F7   (R-CNT-27)
dir_offset < 16                               -> F11
dir_length < 4                                -> F18
dir_offset|dir_length|generation > 2^63-1     -> F3
dir_offset + dir_length > 2^63-1              -> F4
dir_offset + dir_length > F - 64              -> F12
generation == 0                               -> F13
file_id == 0                                  -> F14
trailer[56:60] != 00 00 00 00                 -> F17
```

**Guess made:** where to put the `F < 128` check. §6.2 gives an ordered list
that does not include it, and `[R-CNT-27]` states no ordering. For a 40-byte
file you cannot even perform §6.2's steps. I check the size first. No fork
follows — every path here is reject-file — so this is an implementation-order
question, not a spec gap.

### Step 3 — directory

Fetch `[dir_offset, dir_offset + dir_length)`; verify the terminal CRC over
`dir_length − 4` bytes before any other use (`[R-CNT-11]`, F23). The bound on
this second range comes entirely from fields the trailer CRC has already
covered — `[R-ENC-05]` is satisfied by construction.

### Step 4 — record walk

Framing per §7.2: 24-byte header + `inline_length`. Type 0 → F27. Header or
payload past the sequence end, or residue → F32. Then:

- multiplicity (`[R-CNT-14]`): ≥2 top-level type 0x0002 → F37 (**reject-file**,
  not ignore-record — the quarantine of §7.1 covers the *document*, and §7.1
  is explicit that it starts "once its framing has been read"; multiplicity is
  framing).
- unknown type MU=1 → reject-file (F38 for reserved-range; for experimental
  range §21.6 explains it is deliberately not a row, because the *file* is
  conforming and only the reader's capability is recorded).
- unknown type MU=0 → ignore-record; its extent is still a coverage claimant
  (§9.7) and still opaque to every checksum (§8.1's last row).
- for each type 0x0002: `(0,0)` → F24, `extent_length < 5` → F25,
  `inline_length != 1` → F26. §19.1 step 4 lists exactly these three, which is
  the only place in the document where the *open-tier* framing duties of a
  user-metadata record are collected. I did not have to guess.
- extent-slot rules **only for non-layer** top-level records (F33/F34/F35).
  Layer-record slots defer to layer access (L16/L17/L18). §19.1 step 4 and
  §19.3 make this split explicit and the register's Detected cells agree.
- layer-name namespace. §19.1 is unusually careful here and I want to record
  that it answered three questions I would otherwise have had to invent
  answers to: (a) uniqueness is decided *before* validity; (b) uniqueness is
  over raw bytes even when neither name is well-formed; (c) a layer record
  whose name field does not fit its `inline_length` contributes **no** name and
  is reject-layer, not reject-file. Without (c) two truncated records would
  either both be "the empty name" (a spurious duplicate → reject-file) or
  neither, and the two readings differ on a whole-file verdict. It is decided.

The open **completes** even when a layer record fails: L4/L6/L7 are detected at
open with outcome *reject-layer*, so the file opens and that one layer is
unusable. §2.4 lets me still list its name.

### Cold remote open, byte-exact

Against Appendix A's 128-byte file:

```
req 1  suffix -64   [64,128)    64 bytes   (carries F=128)
req 2  directory    [16,20)      4 bytes
       2 requests, 68 bytes
```

Against the file I built in §4 below:

```
req 1  suffix -64   [256,320)   64 bytes   (carries F=320)
req 2  directory    [112,231)  119 bytes
       2 requests, 183 bytes
```

The invariant §6.4 exists to state — the open's working set is *the trailer and
the directory and nothing else*, at any file size and layer count — held in my
implementation without special effort. Speculation is a strict superset: a
64 KiB suffix window on either file captures everything and reaches offset 0,
which then obliges the front-block equality check.

---

## 3. Validation timing by tier — what I check, when, and what I may never check

`[R-RDR-02]` fixes the *latest* detection point; earlier is always licensed.

**At open** — front block (only if resident), trailer, directory region + CRC,
top-level record framing/multiplicity/MU gate, non-layer extent slots, the
layer-name namespace including each layer name's UTF-8/emptiness/C0 screening.

**At first access to a layer** (no I/O at all — §19.3 is emphatic and I
confirmed it: every cited check reads only the directory bytes and F) —
the layer record's extent slot, the whole `[R-CNT-23]` constraint set, exact
parse + sub-record walk + sub-record multiplicity, dimension/channel name
rules, the value sets of §11.4/§12.2/§14.1/§15.1/§17.2/§17.3, bool fill,
`[R-COD-07]`'s lz4 declaration cap, the geometry floor and its overflow
arithmetic, and `[R-CNT-17]`'s two cross-checks.

**At use of a tile** — `crc_of_crc_array`, the segment CRC, §15.3's entry
classification, `[R-COD-04]`'s pre-fetch length equality, the tile CRC, the
codec/frame constraints, and `[R-SER-07]`'s exact decoded size.

**At use of a record's extent** — the extent CRC and the document's own content
rules. Never earlier: the open fetches no extent.

**What I may never check** (assigned detector = verifier, `[R-CNF-12]` merely
*permits* me to reject if I notice): live-state coverage and the slack total;
every extent overlap; reserved record flag bits; MU=1/PE=0; a registered type's
stored flags against §7.3; alignment and slab invariants; padding-position and
pad-bit content; interleaved bool byte values; user-metadata member ordering;
reserved-range record types with MU=0; a structure in the pre-trailer pad.

**What becomes a verdict when.** As a plain reader I emit no verdict — I emit
outcomes. As a verifier: an *established* violation forces *nonconforming*
however many other requirements went unchecked; *cannot establish* is available
only to a traversal that established nothing; and the per-requirement
"unable to check" report and the per-scope "unexamined" report constrain the
report, never the verdict. §2.3 states all three separations explicitly, which
is more than most specs manage.

---

## 4. A worked file, built and read

Appendix A is correct but has no layers, so it exercises none of Part II. I
built my own and ran the reader over it.

Layer `L`: interleaved, linearization 1, codec 1 (none), filter 1 (none),
A=0, S=0, A_slab=0, rank 2, dims `y`(E=4,T=2) and `x`(E=4,T=2), one channel
`v` uint8 with fill `0x00`. So G=(2,2), N=4, P=4, C=1, Q=1, decoded size
P·Q = 4, addressed-tile count = N = 4 (interleaved), one segment, index region
4·20 + 4 = 84 bytes. Reference array is `10y + x`. **Tile at spatial ordinal 3
(tile coords (1,1)) is deliberately unstored** — its entry is the sentinel — so
coordinates (2,2), (2,3), (3,2), (3,3) must read as fill.

Layout arithmetic I had to do by hand and then verified by construction:

- layer-record inline payload = 36 (fixed prefix incl. 1-byte name)
  + 2×18 (dimension entries) + 6 (channel entry) + 13 (trailing fixed) = **91**
- record = 24 + 91 = 115; directory = 115 + 4 = **119**
- placement: front [0,16); tiles at 16, 20, 24 (ordinal 3 absent);
  index region [28,112); directory [112,231); pad [231,256) = 25 bytes;
  trailer [256,320). **F = 320**, a multiple of 64. `dir_offset + dir_length
  = 231 ≤ F − 64 = 256` ✅.

Full hex dump of the 320-byte file:

```
0000  89 54 41 52 4E 0D 0A 1A 00 00 00 00 00 00 00 00
0010  00 01 0A 0B 02 03 0C 0D 14 15 1E 1F 10 00 00 00
0020  00 00 00 00 04 00 00 00 00 00 00 00 D4 81 FE CE
0030  14 00 00 00 00 00 00 00 04 00 00 00 00 00 00 00
0040  82 46 98 71 18 00 00 00 00 00 00 00 04 00 00 00
0050  00 00 00 00 A7 18 4F 14 FF FF FF FF FF FF FF FF
0060  FF FF FF FF FF FF FF FF 00 00 00 00 FB 83 6C BE
0070  01 00 03 00 5B 00 00 00 1C 00 00 00 00 00 00 00
0080  54 00 00 00 00 00 00 00 01 4C 01 01 00 01 00 01
0090  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00A0  00 00 00 00 00 00 00 00 00 02 01 00 01 79 04 00
00B0  00 00 00 00 00 00 02 00 00 00 00 00 00 00 01 78
00C0  04 00 00 00 00 00 00 00 02 00 00 00 00 00 00 00
00D0  01 76 06 00 01 00 01 04 00 00 00 00 00 00 00 CA
00E0  6F 20 37 50 DF 83 33 00 00 00 00 00 00 00 00 00
00F0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0100  8A 4E 52 41 54 0D 0A 1A 01 00 00 00 00 00 00 00
0110  01 00 00 00 00 00 00 00 70 00 00 00 00 00 00 00
0120  77 00 00 00 00 00 00 00 40 01 00 00 00 00 00 00
0130  EF CD AB 89 67 45 23 01 00 00 00 00 52 AA E1 3E
```

Reading it back through the reader (log verbatim):

```
step1/2  F = 320 (transport-authoritative)
step1    bytes [0,16) not resident -> front block check omitted per R-CNT-04
step2    magic ok; trailer CRC 0x3EE1AA52 verified over [0,60)
step2    version gate: major=1 minor=0 (minor never gates)
step2    gen=1 dir=[112,231) F=320 file_id=0x0123456789ABCDEF reserved=0 -> all gates pass
step3    directory CRC 0x3383DF50 verified over 115 bytes
step4    1 record(s), no residue
step4    layer table: ['L']

layer access: name=L layout=1 G=(2,2) N=4 P=4 Q=1 entry_count=4 nseg=1 decoded_size=4

point (0,0): tile [0,0] in-tile [0,0] s=0 ordinal=0 -> stored 00
point (1,3): tile [0,1] in-tile [1,1] s=1 ordinal=3 -> stored 0d      (= 10*1+3 = 13) ✅
ordinal 3: SENTINEL -> fill, no payload I/O
point (2,2): tile [1,1] in-tile [0,0] s=3 ordinal=0 -> fill 00        ✅
point (3,3): -> fill 00 ;  point (3,2): -> fill 00 ;  point (2,3): -> fill 00
point (4,0): outside extents -> request fails, no verdict on file (R-MDL-01)
```

Per-tile cold I/O for one stored tile: CRC array (4 bytes) + segment 0
(80 bytes) + payload (4 bytes) = **3 requests, 88 bytes**, of which the first
two may run in parallel (§15.4). The sentinel tile costs **0 bytes** beyond the
index chain, exactly as §19.4 step 4 and the §19.4 region note promise.

Nothing in building or reading this file required me to invent a rule. The one
thing I noticed writing the *writer* side: §9.2 step 5 says "pad to the next
64-byte boundary", and I briefly wondered whether a directory that already ends
on a boundary gets 0 or 64 bytes of pad. §6.2 answers it in one clause —
"a writer that ends its directory on a 64-byte boundary leaves none" — and
also tells me a longer gap is conforming but no conforming commit produces one.
Answered.

---

## 5. Layer access and the tile-read algorithm

`parse_layer` walks §7.4's inline payload in table order with no padding. Two
design decisions in the format make this parse total rather than partial, and
both are worth naming because a format that got them wrong would be
unimplementable here:

1. **The fill field carries its own length prefix** (§7.4: "so fill parses
   without type knowledge and validates with it"). This means an unassigned
   `type` value does not derail the parse — I read the fill, keep parsing, and
   then fail with L35 (reject-layer). Without it, an unknown type would make
   the *rest* of the record unparseable and the failure scope would be
   arguable.
2. **`entry_count` is cross-checked against geometry** (`[R-CNT-17]`) *and*
   against `extent_length` — before any I/O. §22.2's note is right that this is
   the cheapest hostile amplifier and that the two cross-checks close it.

Decoded-size derivation, which the whole allocation story rests on:

- interleaved: `P · Q`, Q = Σ Bᵢ over channels (bool contributes 1)
- planar numeric channel c: `P · Bᶜ`
- planar bool channel: `⌈P/8⌉` (§14.3 — *not* §14.2's table, which does not
  cover it; §14.3's closing sentence "Whichever of §14.2 or §14.3 defines a
  tile's decoded size" is what makes the disjunction total)

For a planar layer the channel is recovered from the disk ordinal as
`c = k div N`, `s = k mod N` — the inverse of `[R-GEO-06]`'s `c·N + s`. The
document never states the inverse explicitly but the mapping is a bijection on
`[0, C·N)` and `s < N`, so it is forced.

Tile read, in the order §19.4 gives:

1. **Domain.** Point request outside extents → the *request* fails, no verdict
   on the file. Region request → intersect with extents; disjoint or
   zero-extent layer → succeed, return nothing. Note the deliberate asymmetry:
   a one-position *region* request outside the extents succeeds empty while a
   *point* request at the same coordinate fails. §19.4's opening sentence
   ("a range whose every interval holds a single position is a region request")
   makes this a property of the API form, not of the geometry, and says so.
2. **Ordinals.** `tᵢ = xᵢ div Tᵢ`, `uᵢ = xᵢ mod Tᵢ`, `s = Σ tᵢ·∏_{j>i} Gⱼ`,
   in-tile ordinal `= Σ uᵢ·∏_{j>i} Tⱼ`, disk ordinal `s` or `c·N + s`.
3. **Index chain.** Fetch the whole segment-CRC array
   (`[entry_count·20, entry_count·20 + ⌈entry_count/2¹⁶⌉·4)` relative to the
   region) and verify it against `crc_of_crc_array`; fetch segment
   `k div 2¹⁶` at `[s·2¹⁶·20, min((s+1)·2¹⁶, entry_count)·20)` and verify it
   against the s-th u32. Both ranges are computable from the layer record
   alone, and §15.4 licenses caching. Failure of either is **layer** scope even
   though I discovered it at tile use — §19.2 flags exactly this and I would
   have gotten it wrong otherwise.
4. **Entry.** §15.3's classification. All-ones/all-ones/crc=0 → sentinel →
   fill, short-circuiting steps 5–6 with no payload I/O. Anything else
   malformed → reject-tile, and `[R-CNF-09]`/`[R-TYP-09]` forbid substituting
   fill. I probed §15.3's row order for a precedence hazard (e.g. `offset=S,
   length=5`: does row 3 or row 6 fire?) and found none — every non-sentinel
   row yields reject-tile with the same structural marking, so evaluation order
   cannot fork.
5. **Payload.** Fetch `[offset, offset+length)`, verify the entry crc *before*
   decoding. Under codec 1 I check `length == decoded size` *before* the fetch
   (`[R-COD-04]` says so explicitly).
6. **Decode.** Codec inverse, then filter inverse (§17.1 and §19.4 step 6
   agree), then `[R-SER-07]`'s exact-size check. The byte-shuffle inverse
   restores byte `i·n + j` to `j·s + i` with `s` = channel element size
   (planar) / Q (interleaved) / 1 (packed bool), and `L` is divisible by `s`
   in all three cases — I verified that: `P·Bᶜ / Bᶜ = P`, `P·Q / Q = P`,
   `⌈P/8⌉ / 1`.
7. **Extract.** Interleaved: channel c at in-tile ordinal u sits at
   `u·Q + Fᶜ`. Planar numeric: `u·Bᶜ`. Planar bool: bit `u mod 8` of byte
   `u div 8`. Padding positions are never returned.
8. **Return.** Bit patterns unaltered. For a multi-entry request each rejected
   tile's failure is bounded to its own positions and I may return the rest
   with a per-entry report — *unless* the failure was step 3's, which is layer
   scope and bars the rest of the request prospectively.

---

## 6. Degradation walks (six, traced end to end)

**(a) Unknown record type, top level, experimental range 0x8001, MU=0, PE=1,
extent (200, 50).** Open, step 4. `[R-CNT-15]` → ignore-record. I skip the
record; every layer still reads; the extent stays a coverage claimant (§9.7)
and is covered by no checksum at all (§8.1's last row), so silent corruption
inside it is stated-not-defended (§22.3). An updater must re-emit the record
byte-identically and may not re-encode it (`[R-WRT-08]`); a compactor may
relocate the extent and re-point the slot, safe because §7.2 bars an MU=0
record from encoding offsets in its own payload. **Served: everything.**

**(b) The same type with MU=1.** `[R-CNT-15]` → **reject-file**, at open. Note
the strangeness the document owns up to in §21.6: the *file is conforming*
(§10.3's publication ban binds the writer's conduct, not the bytes,
`[R-CNF-02]`), so this is a conforming file I must refuse, and the diagnostic
must not say "corrupt". Deliberately not a register row. If the type had come
from the *reserved* range it would be F38 (reader/open) and the file would also
be nonconforming (F39, verifier). **Served: nothing.**

**(c) Unknown codec value 0x8000 on layer B, in a two-layer file.** Nothing
fires at open — codec is not an open-tier check. At first access to layer B,
`[R-COD-03]` → **reject-layer** (L44). Layer A is untouched and fully
readable; §2.4 still lets me list B's name. `[R-COD-11]` confirms this is the
only way a *conforming* reader meets an executable-codec problem, since all
four assigned codecs are core. A *verifier* in the same position reports
nonconforming (a reserved/experimental value is a violation), not "cannot
establish" — "cannot establish" is for a codec it cannot *execute*.
**Served: layer A entirely.**

**(d) Truncated tail — a torn commit.** Physical file = F_old + 3 MB of a
partial commit. The final 64 bytes are payload, not a trailer. Magic fails →
F10 → reject-file, reported as *torn or invalid*, and `[R-LIF-05]` forbids me
to scan backward. §9.5's note makes the crucial point that I would otherwise
have had to reason out: residue past a *completed* commit is indistinguishable
from this and carries no row of its own, because the observable states (magic,
CRC, or `committed_file_length` vs transport size) are already F10/F16/F19.
Recovery is somebody else's deliberate operation. **Served: nothing** — and
that is correct, because trailer_n is intact and *recoverable*, not readable.

**(e) Checksum mismatch, three depths.**
 - Directory CRC → F23 → reject-file. Served: nothing.
 - Segment CRC (or `crc_of_crc_array`) → L39/L38 → **reject-layer**, discovered
   at tile use, prospective: values already returned under §19.2's timing
   stand (§2.4). Served: other layers, plus whatever this layer already
   returned.
 - Tile CRC → T1 → **reject-tile**. That tile's read reports failure; fill is
   never the fallback (`[R-CNF-09]`); neighbours in the same layer are
   unaffected. Served: everything else. Note that §9.7 keeps this entry's
   extent in the coverage walk — the defect is in the bytes, not the entry.
 - User-metadata extent CRC → R2 → **ignore-record**, SHOULD report. Served:
   all structural data, unchanged. This is the quarantine doing its job.

**(f) Limit exceeded.** A layer declares `entry_count = 2⁴⁰` (index region
≈ 21 TB) and my reader caps at 2³². `[R-ERR-04]`: I MAY decline, at the
narrowest scope whose declarations exceed what I can serve — here the layer —
and I MUST report it as a *resource limit*, not as a validity error. Every
other layer stays served. The paired obligation bites the other way too: if the
same file had `entry_count = 2³²` I would be non-conforming to decline it,
because 2³² is the §21.9 floor. §18.2's note works through the analogous case
for a metadata document above 16 MiB and explicitly allows either
ignore-record or an `[R-ERR-04]` decline at the whole file, a document having
no declared size and hence no narrower scope. That is latitude the document
grants on purpose, over a file that is outside the acceptance duty anyway.

---

## 7. Findings

Four. Two are cross-reference defects in text I had to rely on, one is an
overridden rule whose override lives three sections away, and one is an
enumeration I had to complete by inference. **None of them forks bytes**, and I
say so under each. I looked hard for one that does — see §8 — and did not find
it.

### reader-01 — CONTRADICTION — §21.2 F36 vs the Detected cells of L17, L18, T8, T9

F36's parenthetical says a claimant that reaches the front block or the live
trailer is caught *at open* by, among others, L17/L18 and T8/T9. Those four
rows are not detected at open. Quoting F36 verbatim:

> a claimant reaching the front signature block or the live trailer is instead
> caught at open by the bounds rows F11/F12, F34/F35, L17/L18 and T8/T9

and the four rows it names:

> | L17 | A layer record's or sub-record's nonzero extent slot has extent_offset
> < 16, pointing into the front signature block | … | reader | **layer access** |
>
> | T8 | A non-sentinel tile-index entry has offset < 16, addressing bytes of
> the front signature block | — | reader | **tile use** |

(L18 is likewise *layer access*, T9 likewise *tile use*.) F11/F12/F34/F35 are
genuinely open-tier; the other four are not, and §19.2's tier list places them
where their own cells do. The substantive claim F36 is making — that such a
claimant is caught by a *bounds* row rather than by the overlap row — survives;
only "at open" is wrong, for half the rows cited. An implementer who takes the
parenthetical at face value pulls layer-record extent-slot bounds and
tile-index entry bounds forward into the open, which §19.1 says performs no
extent I/O and builds no index, and then discovers the checks cannot be sited
there.

**Not byte-level.** Both readings produce identical outcomes (reject-layer /
reject-tile) and `[R-RDR-02]` licenses earlier detection anyway, so a reader
that believed the parenthetical would still be conforming. What decides it: the
four rows' own Detected cells, plus §19.2's tier definition, plus §19.1's
statement that the open "consumes the trailer and directory only".

### reader-02 — AMBIGUITY — §9.7's closing sentence drops the "structural ground" qualifier

§9.7's paragraph opens by drawing a distinction that decides whether a byte
range counts as slack:

> an entry `[R-IDX-03]` classifies reject-tile on a *structural* ground
> contributes no stored extent to the walk; one whose stored bytes alone fail
> its crc keeps its extent

and closes, five sentences later, without the qualifier:

> An entry `[R-IDX-03]` classifies reject-tile does not make the walk
> incomplete: the walk passes over it, and the bytes it nominally addresses
> fall to slack (§15.3).

Two readings. (A) The closing sentence inherits "on a structural ground" from
the opening one, so a crc-failing tile's extent is still a claimant and its
bytes are not slack. (B) The closing sentence means what it says — *any*
reject-tile entry's bytes fall to slack — which would put a crc-failing tile's
extent into the slack total. I picked (A), because §15.3 states it in terms
that leave no room:

> An entry whose only defect is that its stored bytes fail its crc is
> well-formed: the defect lies in the bytes it addresses, not in the entry, so
> its extent stands and it keeps its place in the *verifier* rows, in run
> continuity, and in the coverage walk.

Under (B) a verifier reports a different slack total for the same file, and
`[R-SLB-03]`'s run-continuity relation loses a tile it is explicitly told to
keep ("An entry whose only defect is that its stored bytes fail its crc is not
transparent"), which would in turn change whether L42 fires. That second
consequence is the one that worries me — it reaches a *verdict*, not just a
count — but only if an implementer reads §9.7's last sentence in isolation and
never reads §15.3 or §16.2, both of which are unambiguous the other way.

**Not byte-level.** Reading (B) is refuted by §15.3's sentence quoted above and
by §9.7's own opening sentence, in the same paragraph. Nothing a *reader*
does is affected at all — coverage is verifier-only.

### reader-03 — AMBIGUITY — `[R-ENC-12]` governs user-metadata keys but lacks `[R-ENC-11]`'s quarantine carve-out

§4.6's two adjacent requirements treat the same case differently.
`[R-ENC-11]` carries an explicit exception:

> a reader MUST treat ill-formed UTF-8 in any string as a validity error at the
> owning scope — except inside a user-metadata document, where `[R-CNT-25]`'s
> quarantine governs and the outcome is ignore-record. `[R-ENC-11]`

`[R-ENC-12]`, which opens by naming user-metadata keys as one of the four
things it governs, carries none:

> **Names** — the strings that identify layers, dimensions, channels, and
> user-metadata keys — satisfy three further constraints. Writers MUST NOT emit
> a name that violates any of them; a reader MUST treat such a name as a
> validity error at the owning scope. `[R-ENC-12]`

Two readings for a file-scope user-metadata document containing a 300-byte key,
or a key holding U+0007. (A) `[R-ENC-12]` applies as written: validity error at
the owning scope = **reject-file**. (B) The quarantine governs:
**ignore-record**, the file reads normally. I picked (B). What decides it,
and why it took three sections to be sure: `[R-CNT-25]` says every way a
document can be unreadable "once its framing has been read", including
"content violating the document's own rules", is ignore-record "notwithstanding
the owning-scope mapping of `[R-CNF-08]`" — and `[R-ENC-12]`'s phrase *is* a
`[R-CNF-08]` mapping; `[R-MTA-02]` says "the outcome of every failure to read
its **document** is ignore-record whatever the scope"; §18.2's fourth
restriction folds §4.6's name rules into the document's own rules; and R6 and
R10 register both cases as ignore-record. The difference between the two
readings is a whole-file rejection versus a fully served file, which is why I
am reporting an omission that is, on its face, purely editorial: the drafters
plainly knew the carve-out needed saying, since they said it one paragraph
earlier for the sibling rule.

**Not byte-level.** Four passages (`[R-CNT-25]`, `[R-MTA-02]`, `[R-MTA-04]`,
and register rows R6/R10) decide it for ignore-record, and no competent
implementation that reads §7.1, §18, or §21.5 can land on reading (A). The
fork exists only for an implementer who stops at §4.6.

### reader-04 — OBSERVATION — §9.7's walk enumeration does not reach layer sub-record extents

§9.7 enumerates the coverage walk's claimants as:

> From the live trailer it enumerates the live directory and its records, each
> record's extent, and the non-sentinel entries of each layer's tile-index
> region

A layer record's sub-records live inside its inline payload, not in the
directory's top-level record sequence, so "the live directory and its records"
admits a narrow reading under which sub-record extents are not walked. That
reading is wrong, but establishing it costs three cross-references: §7.4 says
"Sub-records are layer-scope records"; §7.2's ownership rule names "a stored
extent overlapping its own layer's index region or **sub-record extents**"; and
the register lists "sub-record extents" among F36's instances and "layer
sub-record extents" among L19's. So a verifier must walk them, and a verifier
that did not would both under-detect L19 and over-count slack. §9.7's own
demonstration — "A layer record's extent slot addresses that layer's tile-index
region …, so the region enters the walk once, as that record's extent" — shows
the enumeration is meant to be over records generally, which is the reading I
took. Naming sub-records once in the enumeration would remove the inference.

**Not byte-level.** Verifier-only, and the register rows plus §7.2 decide it
already; a reader never walks coverage at all.

---

## 8. Things I suspected and cleared, recorded so the reasoning can be checked

These are the places I expected to find a fork and did not. Listing them is the
point of an acceptance round.

- **`[R-CNT-04]`'s residency test forks accept/reject.** A file with a corrupt
  front block but a valid trailer and directory is rejected by a local reader
  and served by a remote reader with a small suffix window. This is real, and
  it is deliberate: §6.1 spends a paragraph explaining why the test is
  residency rather than transport, F8 and F2 record the condition, and the file
  is nonconforming either way so `[R-CNF-12]` covers the divergence. Not a
  defect.
- **`[R-CNF-12]` lets one reader reject where another serves.** Any
  verifier-detected violation (a reserved-range MU=0 record, say) may be
  ignored by one conforming reader and rejected by another. Explicitly
  licensed, and confined to nonconforming files.
- **§18.2's metadata size bound.** Three licensed behaviors for a >16 MiB
  document (ignore-record; decode with a larger bound; decline the whole file
  under `[R-ERR-04]`). All three are named in the text, the file is outside
  `[R-CNF-03]`'s acceptance duty by construction, and a ≤16 MiB document is
  fully determined. Not a defect.
- **zstd Window_Size and tiny tiles.** I worked this through because it looked
  like a trap: without Single_Segment_Flag the Window_Descriptor cannot express
  under 1 KiB, so a sub-1-KiB tile under codec 3 would always trip
  `[R-COD-06]`'s window rule. §17.2's note reaches exactly that conclusion and
  states the consequence (such tiles are encodable only as single-segment
  frames), and confirms the two RFC 8878 derivations agree for a conforming
  tile. Fully determined.
- **Deflate's trailing bits.** Unused high bits of the final byte are
  unconstrained (encoder freedom, covered by the tile crc); a whole trailing
  *byte* is T24. The line is drawn precisely.
- **§15.3 row precedence.** No evaluation order can change an outcome — every
  non-sentinel row is reject-tile and six are jointly marked *structural*. I
  counted the *structural* rows: exactly six, as §15.3 says.
- **Unassigned channel type breaking the parse.** Prevented by the fill field's
  own length prefix, and §7.4 says so in the same table cell.
- **A minor version defining an incompat-lane bit.** Would produce a third
  "conforming file a reader nevertheless refuses" beyond §21.6's stated two.
  But under *this* text no flag bits are defined and F22 registers a set
  incompat bit as a violation, and §21.1 explicitly withholds the completeness
  clause from §21.6. Not a defect.
- **F4 lacks the "although each field alone is in domain" qualifier** that its
  analogues L2 and T12 carry, so F3's `dir_offset` instance entails F4's
  condition. Corpus-construction bookkeeping only; both rows are reject-file;
  §24's `[R-VEC-02]` already handles conditions that cannot be isolated.
  Below the reporting bar.
- **Appendix H's conforming-reader checklist** lists four capability classes
  ("all four codecs, both filters, both layouts, and all thirteen sample
  types") where §2.3 lists five, omitting assigned user-metadata encodings.
  Substantively harmless — encoding 2 is zstd, which codec 3 already requires,
  and encoding 1 is verbatim — and the appendix is non-normative and says its
  authority is the cited requirement. Below the bar.
- **§22.3 has a doubled prepositional phrase**: "recovery output is re-verified
  as a whole file before being trusted (`[R-LIF-06]`) before any use." Purely
  editorial; no normative content differs between the two phrasings. Recorded
  here rather than as a finding.

## 9. Verdict on the charter question

I implemented an open path, a layer-access path, a tile-read path with sparse
and stored cases, and six degradation walks, from this document alone, and
built and read a real file end to end. The places I had to guess are the four
above, none of which changes a byte or a verdict for a reader who reads the
whole document. Every constant, offset, and checksum I could compute is
correct, including the two nobody recomputes (Appendix A's trailer CRC and the
all-sentinel segment constant), and the §21 register's own arithmetic —
125 rows, 252 instances — reproduces mechanically from §21.1's counting rule.
