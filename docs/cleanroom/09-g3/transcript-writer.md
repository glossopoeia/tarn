# Round 9 — Writer implementer, working transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,892 lines), in four `Read` passes covering lines 1–3892 with no gaps. I opened
no ADR, no `PLAN.md`, no `AGENTS.md`, no `README.md`, no `conformance/` file, no
`spec/registry.json`, no git history. I ran no `git` command, no web search, no
web fetch. I did not list any directory.

I ran local Python (no file reads except my own scratch scripts, which I wrote)
in
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/97fba2d9-.../scratchpad/w/`:
a CRC-32C implementation (Castagnoli, reflected, init/final `0xFFFFFFFF`), and
two builders that emit a complete generation-1 TARN file and then a
generation-2 append of it. Those builders wrote `gen1.tarn` and `gen2.tarn` into
my scratch directory and read nothing else.

I grepped the one permitted file four times (`byte-identical|verbatim`,
`pre-trailer pad|next 64-byte|64-aligned`, `delet|drop|remov|shrink|layer set`,
and an earlier structural grep). I wrote this transcript to the single output
path in the brief and did not read that directory.

Prior knowledge of other array/image formats was used only to generate
suspicions; every conclusion below is cited to this document.

---

## 1. Checking my instruments first

Before emitting anything I confirmed that my checksum matches §4.5's check
vector, because every structure I am about to write terminates in one.

```
CRC-32C("123456789")            = 0xE3069283   ✓ §4.5
CRC-32C(zero bytes)             = 0x00000000   ✓ §4.5
CRC-32C(2^16 sentinel entries)  = 0xEECB3BB2   ✓ §15.4 / [R-IDX-05] / Appendix B
```

The all-sentinel-segment constant is a falsifiable claim and it holds: I built
65,536 copies of `FF ×16 00 ×4` (§15.2's sentinel, 20 bytes) and got exactly
`0xEECB3BB2`.

I then reconstructed Appendix A's trailer from its field values and computed the
CRC over bytes [0, 60):

```
computed trailer CRC = 0xE00938D2, stored little-endian as  D2 38 09 E0
Appendix A [124,128) =                                      D2 38 09 E0   ✓
```

Appendix A is byte-correct. I also checked its arithmetic: directory at 16,
length 4, ends at 20; `[R-LIF-02]` step 5 pads to the next 64-byte boundary → 64;
trailer [64,128); F = 128, F mod 64 = 0; `dir_offset + dir_length = 20 ≤ F − 64 =
64`. All of §6.2's gates pass.

I also spot-checked every other worked example in the document that a writer
depends on, because if one of them were wrong my layout would be wrong in the
same place:

- §11.2/§11.4: extents (1024, 2048), tiles (256,256) → G = (4,8), N = 32,
  P = 65,536; (300,700) → tile (1,2), s = 1·8+2 = 10, in-tile (44,188),
  ordinal 44·256+188 = 11,452; planar C = 4, channel 2 → 2·32+10 = 74. ✓
- §15.4: entry 74 at region bytes [1480, 1500) = 74·20. ✓ Channel-3 block
  = [96, 128) → 32 sentinels. ✓
- §15.4 large example: entry_count 1,000,000 → 16 segments (15 full + 16,960);
  CRC array 64 bytes; region 20,000,064; segment 15 at [19,660,800, 20,000,000);
  k = 999,999 at segment byte 20·16,959 = 339,180; one full segment = 65,536·20
  = 1,310,720 = 1.25 MiB. ✓ All exact.
- §14.2: interleaved (2,3), `a` uint8 + `b` uint16 → Q = 3, decoded 18, ordinal
  5 at [15,18). Planar `b` → 12 bytes, ordinal 5 at 10–11. `t` float32 + `m`
  bool → Q = 5, decoded 30, ordinal 5 at [25,30). ✓
- §14.3: P = 10 alternating → `55 01`; with fill true → `55 FD` (pad bits 2–7
  set). ✓
- §14.5: extents (5,5), tiles (4,4), edge tile (1,1) → 1 real + 15 padding,
  32 bytes, values 1–15 each `CD AB`. ✓
- §17.3 shuffle: 1.0/2.0/3.0 float32, s = 4, n = 3 →
  `00 00 00 00 00 00 80 00 40 3F 40 40`. ✓ (I recomputed the permutation
  i·n+j by hand and it matches.)
- §12.3: channel entry `temp`/float32/qNaN → the 12 bytes
  `04 74 65 6D 70 0C 00 04 00 00 C0 7F`. ✓
- §4.6: `température` NFC → 12 bytes, prefix 12. ✓
- §21.9 note: 2³² entries → 2¹⁶ segments × 4 = 256 KiB; 2³⁶ → 4 MiB. ✓
- §20.3 example: 32·20 + 4 = 644. ✓ §20.3 note: 10⁶ tiles ≈ 20 MB index. ✓

None of these are findings. I record them because a writer that cannot reproduce
them has a bug, and because a document whose examples all check out changes where
I should be looking: not at the arithmetic, at the seams between rules.

I also mechanically counted §21's Instances cells against §21.8's claim of
"125 conditions over 253 instances": F rows total 60, L rows 103, T rows 46,
R rows 44 → 253, and 38 + 50 + 27 + 10 = 125. Both match. §15.3's "Six rows are
marked *structural*" also matches (I counted the six). Not findings.

---

## 2. Creation: a byte layout, in emission order

### 2.1 What I chose, and who chose it

Layer `img`, interleaved, rank 2, dimensions `y` and `x`, extents (5, 5), tile
extents (4, 4); channels `v` (uint16, fill `0xABCD`) and `m` (bool, fill `0x01`);
codec 1 (none), filter 1 (none), linearization 1, no alignment, no slab,
index_encoding 1. Plus one file-scope user-metadata record (encoding 1).

Derived, with no writer freedom:

```
G = (⌈5/4⌉, ⌈5/4⌉) = (2, 2)        §11.2 [R-GEO-03]
N = 4 spatial tiles, P = 16 positions/tile
addressed tiles = N = 4 (interleaved)   → entry_count = 4   [R-CNT-17]
Q = B_v + B_m = 2 + 1 = 3            §14.2 [R-SER-02]
decoded size = P · Q = 48 bytes
index region = 4·20 + ⌈4/2¹⁶⌉·4 = 80 + 4 = 84 bytes   [R-CNT-17], §15.1
```

I stored ordinals 0, 1 and 3 and left ordinal 2 (tile coordinates (1,0)) as the
sentinel, so the file exercises §15.2 and `[R-TYP-08]`.

Padding content is *not* my choice: §14.5 `[R-SER-05]` requires each padding
position to carry each channel's recorded fill. Tile 3 (coordinates (1,1)) has
one real position (4,4) and 15 padding positions, so 15 of its 16 samples are the
five bytes `CD AB 01` repeated — visible in the dump at 0x0070 onward. Tile 1
(coordinates (0,1)) covers x = 4..7, so 12 of its 16 positions are padding, and
tile 0 has none.

### 2.2 The emission order I had to use

`[R-LIF-02]`'s creation path is: front signature block, then steps 2–6 "writing
beginning at offset 16, with generation 1". Step 2 is "in any order satisfying
§5.2's coverage classes", so tile/index/extent placement is mine
(`[R-SLB-05]` says so explicitly). Step 3 appends the directory; §6.2
`[R-CNT-05]` forbids any structure between the directory's end and the trailer,
so the directory is necessarily the last structure. Step 5 pads to the next
64-byte boundary and writes the trailer.

There is one dependency the document forces and does not spell out in one place,
which I had to derive: the layer record's `crc_of_crc_array` covers the segment
CRC array (§8.1), the segment CRC covers the entry bytes (§15.4), and the entry
bytes carry the tiles' *offsets* (§15.1). So tile placement must be final before
the index region can be written, and the index region must be final before the
layer record — hence before the directory — can be written. That is why item 3
of Appendix G's total order (tiles, then index region, then extents, then
directory) is the only order in which a single forward pass works. Not a finding;
worth stating because it is the whole shape of a creator.

### 2.3 The resulting file (generation 1)

```
[0, 16)        front signature block   89 54 41 52 4E 0D 0A 1A + 8 zero bytes
[16, 64)       stored tile, disk ordinal 0   (48 bytes, codec 1)
[64, 112)      stored tile, disk ordinal 1   (48 bytes)
[112, 160)     stored tile, disk ordinal 3   (48 bytes)
[160, 223)     user-metadata extent: 59-byte JSON document + 4-byte CRC-32C
[223, 307)     tile-index region: 4 entries (80 B) + 1 segment CRC (4 B)
                 entry 0: off 16   len 48   crc
                 entry 1: off 64   len 48   crc
                 entry 2: FF ×16 00 ×4                (sentinel, §15.2)
                 entry 3: off 112  len 48   crc
                 crc_of_crc_array = 0x0D85E7C7
[307, 460)     directory region: layer record (124+? B) + user-metadata
               record (25 B) + 4-byte CRC-32C            dir_length = 153
[460, 512)     pre-trailer pad, 52 bytes, zeroed by [R-CNT-03]'s advice
[512, 576)     trailer, generation 1, file_id 0x9E3779B97F4A7C15
F = 576, F mod 64 = 0
```

Coverage check (§5.2 `[R-CNT-02]`, §9.7 `[R-LIF-08]`): claimed = 16 (front) +
144 (three tiles) + 63 (metadata extent) + 84 (index) + 153 (directory) + 64
(trailer) = 524. F − claimed = **52 bytes of slack**, exactly the pre-trailer
pad. Every claimant lies in [16, F − 64) = [16, 512). Nothing overlaps.

The layer record's inline payload is 100 bytes and I laid it out field by field
against §7.4's table with no padding between fields:

```
03 "img"                       name          (4)
01                             layout = interleaved
01 00                          linearization = 1
01 00                          codec = 1 (none)
01 00                          filter = 1 (none)
00×8                           A = 0 (none declared)
00×8                           S = 0
00×8                           A_slab = 0        (required 0 when S=0, [R-CNT-23])
02                             rank d = 2
02 00                          channel count C = 2
01 "y" 05 00.. 04 00..         dim y: extent 5, tile extent 4   (18)
01 "x" 05 00.. 04 00..         dim x: extent 5, tile extent 4   (18)
01 "v" 07 00 02 CD AB          channel v: uint16, fill length 2 (7)
01 "m" 01 00 01 01             channel m: bool,   fill length 1 (6)
01                             index_encoding = 1
04 00 00 00 00 00 00 00        entry_count = 4
C7 E7 85 0D                    crc_of_crc_array
                               (no sub-records)
                               inline_length = 100
```

The fill *length prefix* is not free: `[R-CNT-23]` cross-checks it against the
type's element size, so `v` gets 2 and `m` gets 1, and `[R-TYP-07]` constrains
the bool fill byte to `0x00` or `0x01`. The record header's flags must be
`0x0003` — §7.3's registry fixes MU = 1, PE = 1 for type 0x0001 and
`[R-CNT-22]` makes a stored-bit mismatch a verifier-detected violation (L50).

### 2.4 What the document fixed, and what it left to me

Fixed, with no writer choice:

| Thing | Rule |
|---|---|
| Front block bytes [0,16) | §6.1, exact 16 bytes |
| Where creation writing begins (offset 16) | §9.2 creation path |
| Directory last among structures | §6.2 `[R-CNT-05]` + `[R-LIF-02]` step 3 |
| Pre-trailer pad *length* (to the next 64-byte boundary; zero if the directory already ends on one) | `[R-LIF-02]` step 5 + §6.2 |
| F multiple of 64; trailer in the final 64 bytes | §6.2, `[R-CNT-01]` |
| generation = 1; flags = 0; version_major = 1 | §9.3, `[R-CNT-08]`, §6.2 |
| Trailer reserved [56,60) zero | §6.2 |
| Every checksum's covered range | §8.1 |
| Index entry order = disk-ordinal order | `[R-IDX-01]`, `[R-GEO-06]` |
| Sentinel encoding for unstored tiles | `[R-IDX-02]` |
| Index region layout: entries then CRC array, no padding | §15.1 |
| entry_count = addressed-tile count; extent_length = 20n + 4⌈n/2¹⁶⌉ | `[R-CNT-17]` |
| Decoded tile image bytes and their order | §14.1–§14.3 |
| Padding-position and pad-bit content = fill | §14.5 `[R-SER-05]` |
| Interleaved bool bytes = 0x00/0x01 only | `[R-SER-08]` |
| Codec 1 ⇒ entry length = decoded size | `[R-COD-04]` |
| Registered record types' MU/PE bits | §7.3, `[R-CNT-22]` |
| Reserved record flag bits 2–15 = 0 | `[R-CNT-12]` |
| Layer record with zero addressed tiles ⇒ extent (0,0), crc_of_crc_array = 0 | §7.4, `[R-CNT-23]` |
| User-metadata document in an extent, never inline; inline payload exactly 1 byte | `[R-CNT-25]`, `[R-MTA-03]` |
| JSON object members sorted by key UTF-8 bytes | `[R-MTA-05]` |
| Both durability barriers | `[R-LIF-02]` steps 4 and 6 |

Left to me:

| Degree of freedom | Where the document says so |
|---|---|
| Order and placement of stored tiles, index regions and record extents | `[R-LIF-02]` step 2, `[R-SLB-05]` |
| Gap *extent* between structures | `[R-SLB-05]` |
| Gap *content*, incl. the pre-trailer pad | `[R-CNT-03]` (SHOULD only), §5.2, §6.2 |
| `file_id` value | §6.2 (≠ 0), §9.3 (SHOULD random) |
| `version_minor` | `[R-CNT-26]` (SHOULD floor) |
| Tile extents, layout, codec, filter, linearization (must be 1), alignment/slab declarations | §11.3 note, §7.4 |
| Which tiles to store vs. sentinel (any all-fill tile may go either way) | §13, Appendix G item 6 |
| Record order in the directory; sub-record order | `[R-CNT-14]` |
| Deflate final-byte unused high bits; all encoder choices for codecs 2–4 | §17.2 note, `[R-CNF-05]` |
| Fill recorded when the caller chooses none | `[R-TYP-10]` (SHOULD) |
| Metadata encoding 1 vs 2, and the zstd settings under 2 | §18.2 |

I found no place in creation where I had to guess. The one thing I had to
*derive* rather than read is the checksum dependency chain of §2.2.

Two writer constraints I want to record because they surprised me and would
surprise an implementer: (a) `[R-CNT-13]`'s "extents are owned exactly once"
forbids content deduplication — two index entries may not point at the same
bytes, within a layer or across layers, so identical tiles must be stored twice;
(b) `[R-SLB-01]`'s alignment invariant binds *stored tiles only*, not index
regions or record extents, so an aligned layer's index region needs no alignment.

---

## 3. The append procedure

### 3.1 A concrete generation 2

Generation 2 supersedes stored tile ordinal 1 of `img` and retains the
file-scope user-metadata record untouched. Establish F = 576 by validating the
trailer at the physical end (`[R-LIF-04]`, `[R-WRT-04]` step 1); perform §19.1's
open (step 2); validate what the commit touches (`[R-WRT-03]`: trailer + the
full directory always, plus §19.3 layer validation for `img`, plus the §19.4
index chain for segment 0 because its entries 0, 2 and 3 are reused).

```
[576, 624)     new stored tile, disk ordinal 1
[624, 708)     index region', all 4 entries re-emitted (entry 1 re-pointed,
               entries 0/2/3 byte-identical), new segment CRC,
               new crc_of_crc_array = 0x5815BFB9
[708, 861)     directory': new layer record + the generation-1 user-metadata
               record re-emitted BYTE-IDENTICALLY (verified in code: True)
[861, 896)     pre-trailer pad', 35 bytes
[896, 960)     trailer', generation 2, same file_id
F = 960
```

Slack after the commit = 960 − 524 = **436 bytes**, and it decomposes exactly:

```
 48  superseded tile payload (old ordinal 1)
 84  superseded tile-index region
153  superseded directory
 52  superseded pre-trailer pad
 64  superseded trailer
 35  new pre-trailer pad
---
436  ✓ matches F − claimed
```

That is `[R-CNT-21]`'s number, and §5.2 makes the verifier — not the reader —
report it. Note that the retained metadata extent at [160, 223) did **not**
move: `[R-WRT-05]` re-emits the record byte-identically, extent slot and all,
and `[R-WRT-08]` bars relocating it outside compaction. So a single superseded
tile costs 48 bytes of payload but 384 bytes of everything else — the
index-dominated cost §20.3's note quantifies at scale.

### 3.2 Write order, durability, and the commit point

`[R-LIF-02]` fixes it and `[R-WRT-04]` step 6 restates it consistently:

```
1. begin at exactly F (= 576)
2. append payloads, index regions, new record extents (order free)
3. append the complete directory + its CRC
4. BARRIER  ← everything in 1–3 must be durable here
5. append pad, then the trailer (generation+1, same file_id, ignore-lane
   bits copied forward per [R-CNT-08], version_minor per [R-CNT-26])
6. BARRIER  ← the commit point
```

**The commit point is the moment the 64 trailer bytes are durable at the
physical end of file.** Nothing before step 5 is observable: a reader takes the
trailer at the current end of file as its snapshot (`[R-LIF-05]`), and until
step 5 lands, the physical tail is payload/directory/pad bytes that fail §6.2's
gates. The two barriers are not optional and are not one barrier — §20.2
`[R-WRT-02]` says so in terms ("both barriers, not one").

One asymmetry a writer must respect: if the physical file is longer than F
(residue from an abandoned commit), `[R-LIF-04]` gives two options — truncate to
F *before* step 1, or overwrite from F and truncate to the new
committed_file_length *no later than step 6*. The second option means the
truncation is inside the commit's atomicity window, and a crash between the
trailer write and the truncation leaves the *new* generation reachable only by
recovery. That is analysed in §4 below.

### 3.3 Every record-flag combination, and what my updater may do

The document defines exactly two flag bits (§7.2: bit 0 MUST_UNDERSTAND, bit 1
PRESERVE_ON_EDIT) plus reserved bits 2–15. Walking all of them:

**For a record type my updater does not implement** — §20.4's table, with
`[R-CNT-12]` normalising (1,0):

| Stored (MU, PE) | What my updater may do |
|---|---|
| (1, 1) top-level | **No commit at all.** `[R-CNT-15]` makes an unimplemented top-level MU = 1 record reject-file, and §2.3 makes the updater a reader first. I abort the open. Compaction is barred on the same ground (`[R-WRT-06]`). |
| (1, 1) sub-record | Retain the containing layer record byte-identically; the layer is frozen (`[R-CNT-18]` gives reject-layer). Other layers stay editable. I may still supersede tiles in *other* layers and re-emit the directory. |
| (1, 0) | Read as (1, 1) — `[R-CNT-12]`: "a reader or updater encountering it MUST treat the record as PE = 1 (never silently deletable)". Behaviour identical to the row above. The stored bits survive re-emission, so the file stays nonconforming (F27/L47) and a verifier reports it; my updater has no obligation to detect it. |
| (0, 1) | Retain byte-identical, extent content unmodified. A compactor may relocate the extent and re-point the slot (§20.5) — safe because `[R-CNT-13]` forbids an MU = 0 record from encoding offsets in its own payload. |
| (0, 0) | Retain byte-identical, **or** drop it — but only in a commit that *independently* changes the scope it attaches to. Concretely, for my generation-2 commit (superseding a tile of `img`): I may drop `img`'s own MU = 0/PE = 0 sub-records, because that layer's index and stored tiles change; I may **not** drop a top-level MU = 0/PE = 0 record, because §20.4 explicitly says "a commit that only supersedes a layer's tiles is not such a change". And a commit whose only effect would be the drop MUST retain it. |
| reserved bits 2–15 set | I ignore them (`[R-CNT-12]`) and carry them forward verbatim under `[R-WRT-05]`. The file stays nonconforming (F28/L48) and the violation travels with the structure, which `[R-WRT-01]` expressly licenses ("a violation latent in a structure they neither modify nor rely on travels with it"). I checked whether `[R-CNF-06]`'s "MUST satisfy every writer requirement for the bytes it produces" forces me to zero the bit instead; I concluded it does not, because §20.4 reserves "new output under its writer obligations" for a record it *modifies*. Determinate; not reported. |

**For a record type my updater does implement** (0x0001, 0x0002), §20.4 switches
the authority to §7.3's registry: I emit MU/PE = the fixed values and ignore the
stored bits. That much is clean. What is *not* clean is what §20.4 then infers
from it — "both registered types carry PE = 1, so neither can be dropped" — which
is finding **writer-01** below and is the one place in the whole append walk where
I could not decide what my updater is permitted to do.

### 3.4 Things I checked in the append path that turned out determinate

- **Ordinal renumbering.** A commit that grows E_x from 5 to 9 with T_x = 4
  raises G_x from 2 to 3 and N from 4 to 6, so old ordinal 2 (tile (1,0)) becomes
  new ordinal 3 (s = 1·3 + 0). §20.3 step 4 says retained entries are
  "byte-identical at its disk-ordinal position (a geometry change renumbers
  ordinals, `[R-GEO-06]`)" — i.e. at the *new* position. Determinate.
- **Slab repacking.** Adding a tile into the middle of a packed run forces me to
  rewrite the run's later stored tiles at new contiguous offsets (their old bytes
  become slack), because `[R-SLB-03]`'s packing relation is "each stored tile's
  offset equals the previous stored tile's offset plus its length". §20.3's
  example prose "retained ones do not move" is illustrative, not a prohibition.
  Determinate — but see writer-09 for the enumeration gap in `[R-SLB-04]`.
- **`[R-WRT-03]` does not require me to verify reused tiles' payload CRCs**, only
  the index chain of segments whose entries I reuse. So a corrupt payload
  survives my commit undetected and the new generation is nonconforming (T1).
  I decided this is sanctioned by `[R-WRT-01]`'s "violation … travels with it",
  since I neither modify nor rely on those payload bytes. Determinate.
- **The no-op commit.** §5.1 says "a commit that touches no layer re-emits the
  directory, the pad and the trailer alone", so a generation bump with no logical
  change is a conforming commit. Determinate.
- **Version_minor on append**: max(floor, prior minor), a SHOULD (`[R-CNT-26]`),
  restated identically in §20.3 step 6 and §20.5. Consistent.

---

## 4. Slack, per commit shape

| Shape | Bytes that become slack | Who counts them | Permitted content |
|---|---|---|---|
| **Append (new layer)** | The prior generation's directory, pre-trailer pad and trailer. Sized by the file's layer count, never by any layer's data (§20.3 example (a)). Plus the new commit's own pre-trailer pad and any alignment gaps it leaves. | Verifier only; `[R-CNT-21]` MUSTs the total. Readers MUST NOT interpret it. | Unconstrained. Writers SHOULD zero (`[R-CNT-03]`); §5.2 says "no conformance requirement applies to it". |
| **Append (tiles superseded)** | Above, plus the layer's entire prior tile-index region, plus every superseded stored-tile payload. In my worked case: 48 + 84 + 153 + 52 + 64 + 35 = 436. | Same. | Same. Superseded payloads remain readable in a hex dump — §23.1 `[R-PRV-01]` forbids representing the commit as erasure. |
| **In-place update** | Does not exist. `[R-LIF-01]`: bytes in [0, F) are immutable and "every conforming mutation of a file is either a commit (§9.2) or a whole-file rewrite under a new file_id". The only in-place writing permitted is into [F, physical end) under `[R-LIF-04]`, which is not a committed byte. | — | — |
| **Rewrite / compaction** | *Input* slack is not carried (§20.5). The *output* has only its own alignment gaps and pre-trailer pad, and can have zero slack if the directory ends on a 64-byte boundary. The input file itself persists untouched (`[R-PRV-02]`). | Verifier, on the output. | Same. |
| **Abandoned partial write** | **Not slack.** Slack is defined relative to the live committed state, which is reached "from the live trailer" (§9.7). A torn file has no valid trailer in its final 64 bytes, so there is no live state and no slack total to compute — `[R-CNT-21]`'s partial-total machinery applies with the whole file named as unwalked. The residue is not a register row of its own; §9.5's note says so directly and points at F10/F16/F19 as the observable states. | Nobody, until the file is recovered. | Unconstrained, and `[R-LIF-04]` requires the next successful commit to truncate or overwrite it so that "bytes beyond a committed length never survive into any committed state". |

The one place this got subtle: `[R-CNT-05]` says a pre-trailer gap *longer* than
step 5's pad "is conforming, and no conforming commit produces one". I checked
that both halves hold. A longer gap breaks no file-level rule (F must still be
64-aligned, `dir_offset + dir_length ≤ F − 64`, and no *structure* may sit in the
gap — F9). And no conforming path produces one: step 5 is a MUST, `[R-LIF-04]`'s
truncation is to the new committed_file_length, and recovery truncates to an
earlier trailer whose own pad was ≤ 63. Consistent. Not a finding.

---

## 5. Torn-write recovery — six crash points

Numbers refer to my generation-2 append (F_old = 576, F_new = 960).

**Crash A — mid step 2** (say 20 bytes of the new tile written; physical length
596).
*Next reader:* takes the final 64 bytes as the trailer. They are the tail of the
old trailer plus new payload — magic mismatch at F−64 (F10), and even if the
magic matched, committed_file_length ≠ 596 (F19). Reports the file torn,
reject-file, and MUST NOT scan backward (`[R-LIF-05]`).
*Next updater:* `[R-WRT-04]` step 1 fails ⇒ "no append; recovery (§9.6) is a
deliberate, separate operation". It stops.
*Conforming in the meantime?* No — F10/F19.
*Recovery:* probes 64-aligned offsets from the largest o with o+64 ≤ 596, i.e.
o = 512; finds trail₁'s magic, CRC verifies, committed_file_length = 576 = 512+64
✓; truncates to 576 and re-verifies the whole file (§9.6's first normative
caution). Generation 1 is restored *exactly* — the return on never modifying a
committed byte.

**Crash B — after step 3, before step 5** (payloads + index + directory written;
physical length 861).
Externally identical to A: the tail is directory bytes, not a trailer. Same
reader verdict, same updater refusal, same recovery to 576. The generation-2
directory sits complete on disk and is unreachable, which is exactly what
§9.2's note means by "step 3 is not discharged by a directory an earlier
generation appended" read in reverse: the trailer is what commits, not the
directory.

**Crash C — mid step 5, torn trailer** (pad written, 30 of 64 trailer bytes
landed; physical length 926 or, if the sector write is partial, 960 with
garbage in the tail).
If the physical length is 926: `F mod 64` fails and the tail is not a trailer.
If it is 960 with a partially-written trailer: the magic may be intact but the
CRC over [0,60) fails (F16), or a partially-updated field fails its gate. Either
way reject-file. Recovery lands on 576 again. §9.2's note is exactly right that
the degradation under weak barriers is from "invisible" to "detected", never to
silent corruption — because the trailer's own CRC covers all 60 preceding bytes.

**Crash D — after step 5's bytes are durable, before step 6's barrier, with
physical length = 960.** The file *is* generation 2 and *is* conforming. A reader
opening now sees generation 2 and everything it reaches is durable because step
4's barrier already covered steps 1–3. This is the true commit point; step 6's
barrier makes the commit survive, it does not create it. Nothing to recover.

**Crash E — the `[R-LIF-04]` overwrite path.** Suppose the physical file was
1,200 bytes of residue from an earlier abandoned commit, and I chose "overwrite
from F and truncate no later than step 6". I write [576, 960), including the
trailer at 896, and crash before truncating. Physical length is still 1,200; the
final 64 bytes are stale residue.
*Next reader:* reject-file (the tail is not a trailer, or fails its gates).
*Next updater:* torn, refuses.
*Recovery:* probes from o = 1,136 downward; the first candidate whose CRC
verifies **and** whose committed_file_length equals o+64 is o = 896
(committed_file_length 960 = 896+64 ✓). It truncates to 960 — recovering
**generation 2**, not generation 1. So a crash in this window loses nothing but
requires a deliberate recovery run. The document handles this correctly; I want
to record that a writer choosing the truncate-first option instead of the
overwrite option never enters this state, and that the difference is a real
operational choice `[R-LIF-04]` leaves open.

**Crash F — during creation, before any trailer exists.** Recovery's probe
"continues the same probe to offset 0" (§9.6) and finds no candidate. §9.6
requires the tool to "report the candidate it settled on and how many it
rejected"; with zero candidates there is nothing to settle on. The document does
not say what a recovery tool reports for a file that has never committed. I
judged this not worth a finding — reporting "no commit state found" is the only
reading — but I flag it here as something a tool author has to invent.

A separate hazard the document does name and I verified against my own bytes:
a stored tile payload can contain a byte string that mimics a trailer. §6.2's
note says such a mimic "is caught at the directory CRC", §9.6 requires recovery
output to be re-verified as a whole file, and §21.6 records the condition as
inert because nothing enumerates slack. In my file no 8-byte window of any tile
payload equals `8A 4E 52 41 54 0D 0A 1A`, but the guarantee is structural, not
statistical, and it holds.

---

## 6. Byte-divergence catalogue

### 6.1 Every legitimate way two conforming writers diverge on identical input and identical stated options

| # | Degree of freedom | Licensed by |
|---|---|---|
| D1 | Relative order of stored tiles, index regions and record extents within a commit | `[R-LIF-02]` step 2, `[R-SLB-05]` |
| D2 | Absolute placement / gap *extent* between structures | `[R-SLB-05]`, `[R-CNT-13]` (only disjointness is required) |
| D3 | Content of every gap, including the mandatory pre-trailer pad | `[R-CNT-03]` is a SHOULD; §5.2 "content is unconstrained" |
| D4 | `file_id` | §6.2 (any nonzero), §9.3 (SHOULD random) |
| D5 | `version_minor` | `[R-CNT-26]` (SHOULD) |
| D6 | Which all-fill tiles are stored vs. sentinel | §13; no rule requires a sentinel |
| D7 | Record order in the directory; sub-record order in a layer record | `[R-CNT-14]` |
| D8 | Codec 2/3/4 encoder output for identical input (block splits, tables, levels, thread count); and DEFLATE's up-to-seven unused final-byte bits | §17.2 note, `[R-CNF-05]` |
| D9 | Fill bytes recorded when the caller chooses none | `[R-TYP-10]` (SHOULD) |
| D10 | Whether an alignment or slab is declared, and its value | §7.4, §16 |
| D11 | Tile extents, layout, channel order — i.e. anything the "identical stated options" do not pin | §11.3 note; §17.2's own item-2 note admits "two files carrying the same arrays can legitimately differ in tiling, layout, and codec" |
| D12 | Metadata encoding 1 vs 2; under 2, the zstd encoder's output | §18.2 |
| D13 | JSON number formatting and escaping inside the metadata document | `[R-MTA-05]` and §18.2's note say so explicitly |
| D14 | Which generation boundaries a large write is split at (checkpoint commits) | `[R-LIF-07]` (SHOULD) |

Nothing else. In particular these are **not** divergences: decoded tile bytes
(§14 fixes them value by value), padding and pad-bit content (`[R-SER-05]`),
interleaved bool bytes (`[R-SER-08]`), index entry order and encoding
(`[R-IDX-01]`), sentinel bytes (`[R-IDX-02]`), any checksum, the pad *length*,
the front block, and the trailer's structural fields.

### 6.2 Appendix G, item by item, against that list

| Item | Closes | Verdict |
|---|---|---|
| 1. Codec 1, or a pinned encoder at a pinned version with fixed settings | D8 | **Closes it**, and honestly: item 1 states outright that cross-implementation byte-identity is unattainable for codecs 2–4. This is the profile's most careful item. |
| 2. `file_id` from a cryptographic hash of the file's own emitted bytes | D4 | **Does not close it** — see writer-04. No hash function is named, no truncation to 64 bits is specified, the exact byte string is under-described, and there is no fallback if the result is 0 (which §6.2 forbids). Unlike items 1 and 9, item 2 claims to be "Deterministic" with no "pin the producer" caveat. |
| 3. Total emission order, contiguously | D1, D2, D7 | **Partially.** It closes tile order, index placement, layer order, top-level record order, and inter-structure gaps for structures it lists. It does **not** unambiguously place a top-level user-metadata record's extent, and it does not order two layers' sub-record extents against each other — see writer-03. Its sub-record rule ("by their order of creation") is not a function of the input at all, so it is vacuous in major 1 and unreproducible in general. |
| 4. One generation | D14, and the whole append surface | Closes it. |
| 5. No declared alignment and no slab, or fixed declared values | D10 | Closes it. |
| 6. The sentinel for every all-fill tile | D6 | Closes it. I checked the edge case: an edge tile is all-fill iff its real samples are all fill, since `[R-SER-05]` already makes its padding fill, so the criterion is well defined for every tile of every layout. |
| 7. The all-zero fill default | D9 | Closes it, and item 7's own note correctly identifies that it reaches through item 6 into *which tiles exist*. |
| 8. `version_minor` at the floor, `flags` = 0 | D5 | Closes it. |
| 9. User metadata absent, or a named JSON writer at a named version | D13 | Closes D13. Does **not** close D12 (encoding 1 vs 2, and the zstd encoder under 2) — "serialized by a named JSON writer" pins the JSON text, not the extent's encoding. |
| — | D3 (gap content) | **Nothing closes it**, although the closing paragraph asserts that the items do. See writer-02. This is the profile's clearest hole: the pre-trailer pad is 0–63 bytes that every commit produces and no item constrains. |
| — | D11 | Out of scope by construction (item 2's note says so). |

So of fourteen degrees of freedom, Appendix G closes eight cleanly (D1, D5, D6,
D7 partially, D8, D9, D10, D14), leaves D2/D7 with a residue (writer-03), fails
to close D3 while claiming to (writer-02), fails to close D4 while claiming to
(writer-04), and fails to close D12 while the closing paragraph asserts
"Everything else the profile needs is already mandatory".

Every divergence in §6.1 is *legitimate* — I could classify all fourteen as
licensed, none as forbidden-but-unpoliced, and none as unclassifiable. The
profile's gaps are gaps in the profile, not in the format.

---

## 7. Findings

### writer-01 — CONTRADICTION — may an updater ever drop a layer record?

**§2.3 `[R-CNF-06]` vs. §20.4 `[R-WRT-05]`; also Appendix H's updater checklist
and §20.5 `[R-WRT-06]`.**

§2.3, defining the conforming updater:

> "An updater MUST satisfy every writer requirement for the bytes it produces,
> and additionally MUST honor the preservation obligations of Part I for records
> it does not understand. `[R-CNF-06]`"

§20.4:

> "Persistence governs every record type; only the authoritative source of the
> flags differs. For a type §7.3 registers, the registry's fixed flags govern
> rather than the stored ones (`[R-CNT-22]`) — both registered types carry
> PE = 1, so neither can be dropped, and implementing a record's type confers
> understanding of it, not permission to drop it."

The first scopes preservation to records the updater **does not understand**; the
second says persistence "governs every record type" and that understanding a type
is "not permission to drop it". A layer record (type 0x0001) is a type every
updater understands and carries PE = 1.

Consequence, which is the concrete question I could not answer: **can a
conforming updater emit a generation whose directory omits a layer record the
previous generation carried — i.e., can a layer ever be deleted from a TARN
file?** Under §2.3, yes: preservation binds only unknown records, so a
caller-directed deletion is an ordinary logical modification and the new
directory simply omits the record. Under §20.4, no, and §20.5 closes the escape
too — "less any record §20.4 lets it drop", and §20.4 lets a compactor drop only
its MU = 0/PE = 0 row. The same question applies to a file-scope user-metadata
record: §20.3's example (c) shows how to *edit* one (a new extent, the old one
slack), but under §20.4's reading a caller who wants no metadata at all can only
write `{}`.

The document's other restatements split. Appendix H's updater checklist takes
§2.3's side: "respects **unknown** records' MU and PE bits (§20.4)". §20.5 takes
§20.4's side. Appendix H is non-normative, so it cannot settle it; §2.3 and §20.4
are both normative and both directly on point. (§2.3 also mislocates the rule —
it cites "the preservation obligations of **Part I**", while §20.4, which states
them, is in Part III.)

I picked §20.4's reading for my updater, because §20.4 is the section that
defines the obligation and because its second clause is written to defeat exactly
the argument §2.3 licenses. That leaves my updater unable to satisfy a
delete-layer request; the closest expressible operation is to modify the layer
record to declare a zero extent on one dimension (`[R-GEO-02]`), which drops
entry_count to 0, sets the extent slot to (0, 0) and `crc_of_crc_array` to 0, and
leaves the layer present but empty. I could not find any text sanctioning that as
a deletion idiom, and a reader still lists the layer (§2.4's reject-layer row
shows layer names survive even rejection).

*Byte-level:* yes. Updater X, implementing `[R-CNF-06]`, honours preservation only
for records it does not understand and, asked to delete layer `old`, emits a
generation-(n+1) directory containing only the remaining layer records — a
different record sequence, a different `dir_length`, a different directory CRC,
and a different trailer. Updater Y, implementing `[R-WRT-05]`, refuses and emits
nothing, or emits a directory that still carries `old`'s layer record. Both files
are conforming *files*, so this forks which byte sequences a conforming updater
may emit rather than which files a reader must reject; it is nevertheless a fork
about actual bytes on disk that two competent implementers reading this text
would produce from the same input and the same request.

---

### writer-02 — CONTRADICTION — Appendix G claims to fix gap content; no item does

**Appendix G, closing paragraph, against items 1–9 and §6.2/`[R-LIF-02]` step 5.**

The closing paragraph:

> "Everything else the profile needs is already mandatory — fill-encoded edge
> padding (`[R-SER-05]`) and explicitly recorded fill (`[R-TYP-06]`) among them.
> Four things are not, and the items above are where the profile adds them: gap
> *content*, which `[R-CNT-03]` only advises; gap *extent*, which placement
> freedom (`[R-SLB-05]`) leaves open; sub-record order within a layer record's
> inline payload, which `[R-CNT-14]` leaves free; and the fill a writer records
> when its caller chooses none, which `[R-TYP-10]` states as a SHOULD."

I read all nine items looking for the one that adds gap content. None does. Item
3 addresses gap *extent* and explicitly declines the content question — "order
alone does not fix bytes while the space between structures is free" — and item
5 addresses whether an alignment is declared. Items 1, 2, 4, 6, 7, 8, 9 are about
codecs, `file_id`, generation count, sentinels, fill, `version_minor`/`flags`, and
JSON.

This is not academic, because under items 3 and 5 there are no alignment gaps at
all, yet one gap survives and is unavoidable: the **pre-trailer pad**.
`[R-LIF-02]` step 5 requires "the pad to the next 64-byte boundary", §6.2 makes
those bytes slack and says "this specification does not constrain their content",
and §5.2 says "Slack has no internal structure this specification defines, its
content is unconstrained". In my generation-1 file the pad is 52 bytes; in
generation 2, 35. So two writers implementing every one of Appendix G's nine items
to the letter — one zeroing the pad, one leaving heap residue — emit files
differing in up to 63 bytes, and, via item 2 (whose hash is taken over
[0, F − 64), which includes the pad), differing in the `file_id` and the trailer
CRC as well. The profile's whole purpose is defeated on files whose directory does
not happen to end on a 64-byte boundary.

The same closing sentence is falsified a second way: "Everything else the profile
needs is already mandatory" is untrue of the user-metadata **encoding** field
(§18.2: 1 = none, 2 = zstd). Item 9 pins the JSON serializer, not the encoding
choice or the zstd encoder under encoding 2, and encoding is not one of the four
named exceptions.

I picked "the profile intends `[R-CNT-03]`'s SHOULD taken as a requirement, by
analogy with item 7's treatment of `[R-TYP-10]`" for my own reproducible writer,
and zeroed the pad — but that is me repairing the profile, not reading it.

*Byte-level:* no. Appendix G is non-normative and "adds no requirement to any
actor: a writer ignoring it is fully conforming". Both pad contents are
conforming, so no verifier verdict and no reader obligation moves. The finding is
that a document-supplied recipe for byte-identity does not produce byte-identity.

---

### writer-03 — AMBIGUITY — Appendix G item 3 does not place every record extent

**Appendix G item 3.**

> "For each layer in ascending layer-name byte order: its stored tiles in
> disk-ordinal order, then its tile-index region; then any record extents in
> ascending record order; then the directory. Records are ordered by type, and
> within type 0x0001 by layer name; a layer record's sub-records are ordered by
> type, and within a type by their order of creation"

Two readings, both defensible:

**(a) The per-layer loop ends at the semicolon after "tile-index region".** Then
"any record extents in ascending record order" is a single pass after all layers,
and it must cover both the top-level user-metadata extent and every layer's
sub-record extent. But "ascending record order" is defined only as "by type, and
within type 0x0001 by layer name" — which does not order two layers' type-0x0002
*sub-record* extents against each other, since sub-record order is defined only
*within* one layer record. Two profile writers with layers `a` and `b`, each
carrying a metadata sub-record, may emit those two extents in either order.

**(b) "then any record extents" is inside the per-layer loop.** Then each layer's
sub-record extents follow its index region, which resolves (a)'s cross-layer
question — but leaves the *top-level* user-metadata record's extent with no
position at all, since it belongs to no layer, and "then the directory" would be
inside the loop too, which is impossible.

I picked (a) and broke the residual tie by ordering sub-record extents by their
owning layer's name, which is the criterion item 3 uses everywhere else. Nothing
in the text supports that choice over the opposite one.

A related soft spot in the same sentence: sub-records ordered "within a type by
their order of creation" is not a function of the input at all — it is a property
of the producing application's history. In format major 1 it is vacuous
(`[R-CNT-14]` allows at most one user-metadata sub-record per layer and there is
no other sub-record type), but it cannot close the degree of freedom the closing
paragraph credits it with closing.

*Byte-level:* no — same reason as writer-02: the appendix is non-normative and
both placements yield conforming files.

---

### writer-04 — OBSERVATION — Appendix G item 2's `file_id` recipe is not reproducible across implementations

**Appendix G item 2.**

> "**`file_id` from a cryptographic hash of the file's own emitted bytes**,
> computed over [0, F − 64) together with the trailer's other fields with the
> `file_id` field taken as zero, then written in. Deterministic, and
> high-entropy"

Four things are missing, and I had to invent all four:

1. **Which hash.** "a cryptographic hash" names no algorithm. SHA-256 and
   BLAKE3 give different results.
2. **How to reduce it to 64 bits.** `file_id` is a `u64` (§6.2). First eight
   bytes? Last eight? Big- or little-endian interpretation? Unstated.
3. **The exact byte string.** "[0, F − 64) together with the trailer's other
   fields" — which fields, in which order, and in which encoding? The trailer CRC
   at [60, 64) is a field, and including it is circular, so it must be excluded;
   the document does not say so. I chose `bytes[0, F−64) || trailer[0,48) ||
   00×8 || trailer[56,60)`, which is a guess.
4. **What to do if the result is zero.** §6.2 requires `file_id ≠ 0`, so a
   hash landing on zero produces a nonconforming file. Item 2 gives no fallback.

Items 1 and 9 both handle exactly this class of problem honestly, by conceding
that byte-identity across implementations requires pinning the producer ("two
conforming encoders emit different, equally valid streams"; "number formatting
varies by runtime"). Item 2 makes no such concession and asserts
"Deterministic" flatly, which is true only per-implementation.

*Byte-level:* no. Non-normative appendix; every choice yields a conforming
trailer (except the zero case, which would yield a nonconforming one but is
unreachable in practice).

---

### writer-05 — OBSERVATION — §21.9's 256 MiB tile guarantee and 8 MiB window guarantee are jointly unusable under codec 3 for a single-segment frame

**§21.9's table with `[R-ERR-03]`/`[R-ERR-04]`, against §17.2 `[R-COD-06]` and
its note.**

§21.9 states, as minimum guarantees a writer "MAY rely on":

> | decoded size of one tile | 256 MiB |
> | zstd frame `Window_Size` | 8 MiB |

and `[R-ERR-03]`: "a conforming reader MUST accept any conforming file whose
quantities lie within these bounds, and a writer MAY rely on that."

§17.2's note observes that with `Single_Segment_Flag` set, "Window_Size is the
frame content size, which this requirement already obliges to equal the decoded
size". So a 64 MiB tile encoded as a single-segment zstd frame has a
`Window_Size` of 64 MiB. Its *tile* quantity (64 MiB) is inside the 256 MiB
guarantee; its *window* quantity (64 MiB) is outside the 8 MiB one. The
acceptance duty is conjunctive over quantities, so it is not engaged, and
`[R-ERR-04]` lets every conforming reader decline that tile, that layer, or the
whole file on resource grounds. A writer that took the 256 MiB row at face value
has produced a file no reader is obliged to read.

The escape exists and the document states it — §17.2's "Writers SHOULD keep the
declared window within §21.9's 8 MiB `Window_Size` guarantee even for a larger
tile" — but it is a SHOULD, it is stated in §17.2 rather than beside the
guarantee it conditions, and satisfying it forces the writer to *not* use a
single-segment frame for any tile above 8 MiB. So the 256 MiB tile guarantee is
freely usable under codecs 1, 2 and 4, and usable under codec 3 only by a writer
that also reads §17.2's note and rejects the encoder's default single-segment
path.

This is decidable from the text; it just costs a three-section join to decide,
and a writer that does not make the join emits interoperable-looking files that
are not.

*Byte-level:* no. `[R-ERR-04]` makes declining a MAY in both directions, so no
two conforming readers are obliged to differ, and no writer emits different bytes
because of the ambiguity — the writer is simply misled about acceptance.

---

### writer-06 — OBSERVATION — §21.7's account of witnessless obligations omits the writer's

**§21.7 second paragraph, against §21.1's characterisation of it.**

§21.1 bills §21.7 as the account of what fails the register's detectability gate:

> "detectability being the gate `[R-CNF-07]` already applies and §21.7 the
> account, by class, of what fails it"

§21.7's second paragraph then enumerates, in a closed list of three:

> "A second set of obligations is omitted from the register because a single file
> exhibits no witness of their violation. Committed-prefix immutability and the
> generation sequence (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a file's
> history, which §9.7 does not reconstruct; the ordinal mappings of
> `[R-GEO-06]` and `[R-SER-01]` are satisfied by a structurally valid tile
> whatever values it carries; and `[R-CNT-13]`'s prohibition on an MU = 0 record
> encoding file offsets in its own payload is opaque by construction."

Every obligation in my charter that has no file-level witness is missing from
that list:

- `[R-LIF-02]` steps 4 and 6 — the two durability barriers. No byte of any file
  records whether `fdatasync` was called, yet Appendix H lists "follows the
  commit protocol including both barriers" under **conforming writer**, i.e. as
  something an implementer is meant to audit.
- `[R-WRT-05]`'s byte-identical re-emission and `[R-WRT-08]`'s no-re-encode rule
  — comparisons between adjacent generations, which §9.7 does not reconstruct.
- `[R-WRT-06]`'s "MUST mint a fresh `file_id`" and `[R-WRT-07]`'s "the output's
  reference arrays MUST equal the live generation's bit for bit" — both require
  the compactor's *input* to check.
- `[R-WRT-09]`'s verification-before-emission ordering — pure conduct.
- The appender's prohibition on relocating a live index region (writer-10).

Two of the document's witnessless writer rules are handled by local notes instead
— §16.2's note for `[R-SLB-04]` ("a stale declaration carries no register row of
its own") and §7.4's note for `[R-CNT-18]`'s nesting prohibition — which shows
the document knows the class exists and treats it case by case rather than in
§21.7. The effect on me as an implementer is that I cannot use §21.7 to answer
"which of my writer MUSTs would a conformance corpus ever catch?", which is the
question §21.7 appears to exist to answer. §21.1's own hedge ("by class") is what
keeps this from being a flat contradiction.

*Byte-level:* no. Nothing about any file's bytes or verdict changes; the register
is unaffected, since none of these obligations is detectable and §21.1's
completeness clause reaches detectable violations only.

---

### writer-07 — AMBIGUITY — `[R-WRT-07]` keys index regeneration on the region moving, not on the tiles moving

**§20.5 `[R-WRT-07]`.**

> "A compactor preserves content but not placement — placement is not among the
> things it carries forward, and it is free to place structures anywhere §5.2
> admits: every stored tile's bytes verbatim — each index entry's crc is
> unchanged — and every retained record per §20.4, except that relocation
> re-points extent slots, regenerates each relocated tile-index region (entry
> offsets new; entry lengths, entry crcs, and sentinel entries unchanged; segment
> CRCs recomputed over the entries as re-emitted), and updates the layer-record
> fields covering a regenerated region (crc_of_crc_array)."

The trigger for regeneration is "each **relocated** tile-index region". But an
index region's entries carry the *tiles'* offsets, not its own. A compactor that
is "free to place structures anywhere" may legitimately leave layer A's index
region at its input offset while moving A's stored tiles to close a slack run
before them. Under the literal rule, that region is not relocated and so is not
regenerated — and its entries then address the tiles' old positions, which the
output no longer contains.

Two readings: (i) "relocated" means "whose entries' targets relocated", so the
region is regenerated whenever any of its tiles moves; (ii) literal, keyed on the
region's own offset. I picked (i), forced by the same requirement's closing
sentence — "The output's reference arrays MUST equal the live generation's bit
for bit (`[R-MDL-02]`)" — and by `[R-CNF-05]`, since a file whose entries point
at the wrong bytes is nonconforming on its face (T1, and probably T9 or F35). An
implementer who reads (ii) and writes the obvious loop ("if region_offset changed
then regenerate") ships a compactor that corrupts any layer whose region happens
to land back at its input offset.

*Byte-level:* no. Reading (ii) produces a file that fails `[R-MDL-02]` and the
tile-scope rows, so the file-conformance predicate already decides which output
is correct; only the compactor's control flow is at risk, and no two *conforming*
outputs differ.

---

### writer-08 — OBSERVATION — §4.7's taxonomy is undetermined for the layer record's names and vacuous for its third class

**§4.7 `[R-ENC-16]` and its note.**

> "Every field this specification defines is classified **structural**,
> **semantic**, or **informative**. A field classified informative MUST NOT
> affect how any byte is located or decoded, and a reader MUST NOT alter decoding
> based on it; each informative field's definition states what a reader does when
> it contradicts the data it describes. `[R-ENC-16]`"

and the note:

> "A packed variable-length payload — the layer record's inline payload (§7.4) —
> has no fixed offsets to give; its table omits the offset and class columns, and
> each field's class follows from the definitions above."

Two problems, both discovered while classifying my own layer record field by
field, which the document's front matter says every field carries:

1. **The class does not follow for the name fields.** The layer name, dimension
   names, and channel names locate no byte and decode no byte, so they are not
   structural under §4.7's definition ("affects how bytes are located or
   decoded"). They do not affect "what decoded values mean" either, so they are
   not obviously semantic. That leaves informative — but then `[R-ENC-16]`'s
   second clause applies ("each informative field's definition states what a
   reader does when it contradicts the data it describes"), and §4.6 states no
   such thing, because a name cannot contradict data. The other inline-payload
   fields do follow: `layout`, `linearization`, `codec`, `filter`, `A`, `S`,
   `A_slab`, `d`, `C`, the extents and tile extents, channel `type`,
   `index_encoding`, `entry_count`, `crc_of_crc_array` are all structural, and
   §13.1 declares `fill` semantic explicitly.

2. **No field in format major 1 is classified informative.** I went through every
   layout table — §6.1, §6.2, §7.2, §7.4, §15.1, §18.2 — and every field is
   structural or semantic. So the second half of `[R-ENC-16]` constrains nothing
   in this major version, and the class it introduces has no member.

I resolved (1) by classifying names as semantic, on the ground that a layer name
is how a caller selects a layer and therefore does affect what a returned value
means. Nothing turns on the choice — `[R-ENC-16]` only binds informative fields —
which is exactly why it is safe to leave undetermined, and exactly why an
implementer who takes the front matter's "Every field is classified" at face
value stalls here.

*Byte-level:* no. No rule keys off a field's class except `[R-ENC-16]`, and it
binds only the empty informative class, so no byte and no verdict moves.

---

### writer-09 — OBSERVATION — `[R-SLB-04]`'s trigger list omits the commit that stores a previously-sentinel tile

**§16.2 `[R-SLB-04]`.**

> "A writer or updater whose commit supersedes a stored tile in, or grows the
> extents of, a slab-declared layer MUST either re-establish the invariants for
> every affected run — a run whose stored-tile set or byte placement the commit
> changes — or clear the declaration in the new generation"

The trigger is "supersedes a stored tile in, or grows the extents of". The
declare-then-fill workflow the document promotes elsewhere does neither: §13's
"Note — sparse writing" describes writers that "append tiles as data arrives,
generation by generation", and §11.1's rationale describes schema-first layers
grown from empty. A commit that turns a sentinel entry into a stored tile
supersedes no stored tile and grows no extent, yet it plainly changes the run's
stored-tile set and, unless the writer repacks, breaks `[R-SLB-03]`'s packing
relation and possibly its `A_slab` alignment (a run whose first stored tile is
new).

The obligation is not actually lost, because `[R-SLB-03]` is a standing invariant
on the live state and a verifier checks it on every generation (L42, L43). So the
file's validity is decided either way and I did not have to guess what to emit —
I repack. But `[R-SLB-04]` is the rule a writer reads to learn *when* it must act,
its own following note says it "is what makes those two rows reachable at all
after a commit", and its enumeration misses the commit shape §13 spends a note
recommending.

*Byte-level:* no. `[R-SLB-03]` already decides which files are conforming, so no
two implementations can disagree about a given file's verdict; only a writer's
prompting is incomplete.

---

### writer-10 — AMBIGUITY — the bar on an appender relocating a live index region carries no requirement keyword

**§20.3 `[R-WRT-04]` step 4, and §5.1's example.**

§20.3:

> "A layer whose record alone changes keeps its extent slot, pointing at the
> existing region, as does a layer the commit leaves untouched (`[R-WRT-05]`);
> relocating a live index region is compaction's operation (§20.5,
> `[R-WRT-07]`), not an appender's."

§5.1:

> "A commit never relocates a live index region otherwise; that is compaction's
> operation (§20.5, `[R-WRT-07]`)."

Both are declarative. §2.1 restricts BCP 14 force to the all-caps keywords, and
neither sentence carries one, while the surrounding text of `[R-WRT-04]` is
otherwise written in MUSTs. So: is an appender that re-emits a layer's index
region at a new offset — for defragmentation, or to satisfy `[R-SLB-03]` after a
repack, or simply because it re-emits everything — violating a requirement, or
merely doing something the document declines to describe?

Readings: (i) the sentences state a prohibition and an appender that relocates is
nonconforming; (ii) they describe the ordinary case and the operation is
permitted, since the output file is conforming under every rule I can find
(§5.2's coverage classes are satisfied, `[R-CNT-13]`'s disjointness holds, the old
region becomes slack like any other superseded structure, and `[R-CNT-17]`'s
cross-check still holds).

I picked (i), because §20.3 phrases it as a contrast between actors ("not an
appender's") which reads as allocating a capability rather than describing a
habit, and because §20.5's fresh-`file_id` rule exists precisely so that
relocation is visible to caches — relocating under the same `file_id` would move
live bytes without the cache-invalidation signal `[R-LIF-03]` is built on. That
last argument is mine, not the document's; the document never says why an
appender may not relocate.

Note that under reading (i) there is a case the document may not have costed: a
slab-declared layer whose repack (writer-09) requires moving stored tiles also
requires re-emitting the index region — which is permitted, since the commit
changes the layer's stored-tile set, so `[R-WRT-04]`'s own rule already re-emits
it "necessarily at a new placement". So (i) is not in tension with slabs. The
ambiguity bites only for a commit that changes nothing about a layer except where
its index sits.

*Byte-level:* no. Under both readings the emitted file is a conforming file, so
no verifier verdict and no reader obligation differs; what differs is whether the
*appender* is conforming, and no file-level check can distinguish the two, which
is the same shape §2.3's `[R-CNF-02]` already treats as binding the actor and not
the bytes. I flag it because it is a MUST-shaped rule an implementer must obey
and cannot recognise as one.

---

## 8. What I could not determine

Only writer-01. Everything else in the creation, append, slack, recovery and
divergence walks resolved from the text, sometimes after joining three sections.
For writer-01 I made a choice (§20.4 governs; layers cannot be deleted) and my
updater is built on it, but I have no way to check that choice against the
document, and §2.3 and Appendix H both point the other way.

Things I looked at and decided were **not** defects, recorded so the next round
does not spend the effort again:

- §21.8's "125 conditions over 253 instances" — I counted every Instances cell:
  60 + 103 + 46 + 44 = 253, and 38 + 50 + 27 + 10 = 125. Exact.
- §15.3's "Six rows are marked *structural*" — exactly six.
- The interaction of `[R-WRT-05]` (byte-identical re-emission) with
  `[R-CNT-12]` (writers MUST emit zero reserved flag bits) for a retained record
  carrying a set reserved bit. `[R-WRT-01]`'s "a violation latent in a structure
  they neither modify nor rely on travels with it" decides it: re-emit verbatim.
  A record the updater *modifies* is "new output under its writer obligations",
  so it is normalised. Determinate.
- `[R-CNT-05]`'s "a longer gap is conforming, and no conforming commit produces
  one" — both halves check out against §6.2, F9 and `[R-LIF-02]` step 5.
- Whether "pad to the next 64-byte boundary" means 0 or 64 bytes when the
  directory already ends on one — §6.2 answers it ("a writer that ends its
  directory on a 64-byte boundary leaves none").
- Whether `[R-WRT-03]` should require verifying reused tiles' payload CRCs —
  `[R-WRT-01]` says latent violations travel.
- §2.4's preserve-verbatim row naming only §20.4's MU = 1 and MU = 0/PE = 1 rows
  while `[R-WRT-05]` makes *all* retained records byte-identical — the class name
  is about non-droppability, the byte-identity rule is `[R-WRT-05]`'s, and they
  do not conflict.
- §9.6's silence on what a recovery tool reports for a file with zero candidate
  trailers — only one reading is available.
- The 512-byte floor on alignment A, the 2⁶² ceilings, `[R-COD-07]`'s
  `0x7E000000` cap and its zero-addressed-tile escape, `[R-CNT-16]`'s
  alignment/slab exclusivity, and `[R-COD-10]`'s divisibility claim
  ("L is divisible by s in every case") — I verified the last by case analysis
  over planar-numeric (L = P·Bᶜ, s = Bᶜ), interleaved (L = P·Q, s = Q) and
  packed-bool (L = ⌈P/8⌉, s = 1). All hold.
