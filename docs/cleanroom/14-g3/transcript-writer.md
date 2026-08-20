# Cleanroom round 14 — Writer implementer transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in full (4,168 lines), in four `Read` calls. I opened no other file in the
repository — no `docs/`, no ADRs, no `PLAN.md`, `AGENTS.md`, `README.md`,
`OPEN-QUESTIONS.md`, no `conformance/`, no `spec/registry.json`, no git
history, no web. I did not list any directory in the repository.

I ran `grep` against that one file three times (to re-locate §21.1's instance
criterion, the four register rows I cite, and the detector/detection-point
columns).

I wrote and ran five Python files of my own in a scratch directory
(`crc.py`, `check_examples.py`, `build.py`, `build2.py`, `verify.py`,
`reg.py`). `crc.py`, `check_examples.py`, `build.py`, `build2.py` and
`verify.py` read no repository file at all; they build and re-read
`gen1.tarn` / `gen2.tarn`, which are files I created myself in the
scratchpad. `reg.py` and one inline `python3 -c` opened
`spec/tarn.md` — the one file I am permitted to read — to count §21's
register rows and instance cells mechanically rather than by eye.

I did not read the round-14 output directory.

One consequence worth stating plainly: everything below is derived from the
document. Where I say "the document does not say", I mean I searched for it
and did not find it; I have no ADR, no vector, and no prior round's finding
to fall back on, and I have not tried to reconstruct any.

---

## 1. Warm-up: does my CRC agree with the document's?

Before laying out a byte I implemented CRC-32C from §4.5's parameters
(Castagnoli 0x1EDC6F41, reflected in and out, init 0xFFFFFFFF, final XOR
0xFFFFFFFF, stored little-endian) and checked it against §4.5's check
vector and Appendix B's constants.

```
CRC-32C("123456789")            = 0xE3069283   § 4.5 says 0xE3069283   OK
CRC-32C(zero bytes)             = 0x00000000   § 4.5 says 0x00000000   OK
CRC-32C(2^16 sentinel entries)  = 0xEECB3BB2   §15.4 says 0xEECB3BB2   OK
```

Then I reproduced §7.4's newly-added worked layer-record example from its
prose alone — rank-1 `sst`, dim `x` extent 100 tile extent 32, one
interleaved float32 channel `temp` with fill 0x7FC00000, codec 1, filter 1,
no alignment or slab, no tile stored:

```
grid count  ceil(100/32) = 4                       -> entry_count = 4
index region 4*20 + ceil(4/65536)*4 = 84 bytes
segment CRC over the 80 sentinel bytes = 0x80A34955   §7.4 says 0x80A34955  OK
crc_of_crc_array = CRC(55 49 A3 80)    = 0xC4EE982E   §7.4 says 0xC4EE982E  OK
inline payload length                  = 81          §7.4 says 81          OK
my reconstructed bytes are identical to the hexdump in §7.4, offset for offset
accounting: name 4 + nine scalars 34 + dim 18 + chan 12 + trailing 13 = 81   OK
```

And Appendix A's trailer:

```
CRC-32C over trailer bytes [0,60) = 0xE00938D2       App. A says 0xE00938D2 OK
```

Both round-13 additions (§7.4's example) and the long-standing Appendix A
check out byte-for-byte. I also hand-checked every other worked example in
the document — §11.2, §11.4, §12.3, §14.2, §14.3, §14.5, §15.4 (both),
§16.2, §17.3, §4.6 — and found no arithmetic error in any of them. §17.3's
shuffle example in particular: three float32 (1.0, 2.0, 3.0), s=4, n=3, the
filtered image `00 00 00 00 00 00 80 00 40 3F 40 40` is exactly what
`filtered[i*n+j] = image[j*s+i]` produces.

That is a good sign about the document's arithmetic discipline, and it is
why the findings below are all about prose rather than numbers.

---

## 2. Creation: a file built end to end

I refused to build the 128-byte minimal file, because it exercises nothing.
I built a two-layer file that forces every decision I could think of:
planar *and* interleaved, a packed boolean plane with pad bits, a numeric
plane, an edge tile that is almost all padding, a byte-shuffle filter, a
slab declaration whose alignment forces a real gap, sentinel entries, a
file-scope user-metadata record and a layer-scope user-metadata
sub-record.

### 2.1 Declarations, and who fixed them

**Layer `mask`** — planar (layout 2), rank 1, dim `i` E=10 T=10, C=2:
channel `m` bool fill `0x01` (true), channel `v` float32 fill
`0x7FC00000`. codec 1 (none), filter 1 (none), A=0, S=2, A_slab=8.

- grid count G₀ = ceil(10/10) = 1, so N = 1, P = ∏Tᵢ = 10. **Fixed** by
  §11.2 `[R-GEO-03]`.
- addressed-tile count = C·N = 2 for a planar layer. **Fixed** by
  §11.2, and it is what `entry_count` must equal (`[R-CNT-17]`, L21).
- disk ordinal of channel c at spatial ordinal s is c·N + s, so ordinal 0
  is `m`'s plane and ordinal 1 is `v`'s. **Fixed** by §11.4 `[R-GEO-06]`.
- `m`'s decoded tile image is P bits packed LSB-first, ceil(10/8) = 2
  bytes; `v`'s is P·4 = 40 bytes. **Fixed** by §14.3 `[R-SER-03]` and
  §14.2 `[R-SER-02]`. Note §12.1's carve-out: element size governs
  everything "except that a planar bool plane is sized by packing".
- `m`'s values alternate true/false from ordinal 0, so byte 0 = 0x55; byte 1
  carries values 8–9 in bits 0–1 (0x01) and six pad bits which
  `[R-SER-05]` forces to the channel's fill bit — fill is true, so bits 2–7
  are set and byte 1 is **0xFD**. Stored plane = `55 FD`. **Fixed**; and
  §14.3's example gives exactly this pair for exactly this reason, which
  is how I checked myself.
- E = G·T = 10, so there are **no padding positions** in this layer. Pad
  bits are not padding positions (§14.3's Note is explicit and I needed
  it).

**Layer `sst`** — interleaved (layout 1), rank 2, dims `y` E=5 T=4 and
`x` E=5 T=4, C=1: channel `t` uint16 fill `0xABCD`. codec 1 (none),
**filter 2 (byte-shuffle)**, A=0, S=0, A_slab=0. One user-metadata
sub-record.

- G = (2, 2), N = 4, P = 16, Q = Σ Bᵢ = 2. Decoded size = P·Q = 32.
- addressed = N = 4 for interleaved. entry_count = 4.
- Every tile has real positions: for tᵢ = Gᵢ−1, (Gᵢ−1)Tᵢ < Eᵢ by the
  definition of the ceiling, so no addressed tile is all-padding. I checked
  this because Appendix G item 6 ("sentinel for every all-fill tile") would
  otherwise interact oddly with it. Nothing in the document states it; it
  falls out of §11.2 and I was content to derive it.
- I stored ordinal 0 (tile (0,0), all 16 positions real) and ordinal 3
  (tile (1,1), covering y∈[4,8) x∈[4,8): exactly one real position (4,4)
  and 15 padding positions, each of which `[R-SER-05]` forces to the fill
  bytes `CD AB`). Ordinals 1 and 2 are sentinels.
- The shuffle stride for an interleaved tile is Q = 2 (`[R-COD-10]`), so
  the stored bytes are all sixteen low bytes followed by all sixteen high
  bytes. Tile 3's stored bytes are `E7 CD*15 03 AB*15` — visibly the
  fill-encoded padding, which is the point.

**Everything in this paragraph was fixed by the document.** The only
declarations I chose freely were the ones the charter calls "stated
options": tile extents (§11.3 imposes none), layout, codec, filter, the
slab, channel and dimension order, names, and the fill values.

### 2.2 Placement, and what fixed it

`[R-SLB-05]` gives total freedom over ordering and relative position, so
placement is mine. To make the walk reproducible I adopted **Appendix G
item 3's** total order — layers in ascending layer-name byte order
(`mask` < `sst`), each layer's stored tiles in disk-ordinal order then its
index region, then record extents, then the directory. The
A_slab = 8 declaration on `mask` forces one real gap.

```
[     0,    16)    16  front signature block         §6.1, constant
[    16,    18)     2  mask tile ord0 (packed bool)  55 FD
[    18,    24)     6  SLACK  (A_slab=8 forces ord1 to 24)   zeroed
[    24,    64)    40  mask tile ord1 (float32 plane)
[    64,   108)    44  mask tile-index region        2*20 + 4
[   108,   140)    32  sst tile ord0 (shuffled)
[   140,   172)    32  sst tile ord3 (shuffled)
[   172,   256)    84  sst tile-index region         4*20 + 4
[   256,   358)   102  file-scope user-metadata extent (98 doc + 4 CRC)
[   358,   431)    73  sst sub-record user-metadata extent (69 doc + 4 CRC)
[   431,   712)   281  directory region (3 records + 4-byte CRC)
[   712,   768)    56  SLACK  pre-trailer pad         zeroed
[   768,   832)    64  trailer, generation 1
F = 832, F mod 64 = 0
```

Decisions and their authority:

- **First structure at 16.** `[R-IDX-03]`/`[R-CNT-13]` bar an offset below
  16. Whether the *first* structure must begin at exactly 16 under
  Appendix G's profile is the subject of **writer-05** below.
- **Directory last among structures.** `[R-CNT-05]`: "Writers MUST place
  the directory so that no structure lies between its end and the
  trailer." Fixed.
- **Pre-trailer pad to the next 64-byte boundary.** `[R-LIF-02]` step 5.
  712 → 768, 56 bytes. Fixed.
- **F a multiple of 64, trailer in the final 64 bytes.** §6.2. Fixed.
- **Slab runs.** `mask` is planar with N = 1, so §16.2 `[R-SLB-02]` gives
  two channel blocks [0,1) and [1,2); runs never span them, so with S = 2
  each block holds one run of one ordinal. Each run's first stored tile
  must satisfy offset mod A_slab = 0: 16 mod 8 = 0 and 24 mod 8 = 0. Fixed.
  I had to read `[R-SLB-02]`'s "Run r of a block starts at ordinal
  block_start + r·S" carefully to get this; it is unambiguous.
- **The index region is not itself aligned.** `[R-SLB-01]` and
  `[R-SLB-03]` constrain *stored tiles* only. Fixed, and stated.
- **Record order in the directory.** `[R-CNT-14]`: order carries no
  meaning. Free; I used Appendix G's key.
- **Gap content zeroed.** `[R-CNT-03]` SHOULD. Free, with a stated
  consequence (forfeits byte reproducibility).

### 2.3 Field values I had to derive

- `mask`'s crc_of_crc_array = CRC-32C over the 4-byte segment CRC array =
  0x0529F7F3; segment CRC = 0x5757A5A5.
- `sst`'s crc_of_crc_array = 0x27BA7934; segment CRC = 0x952023F4.
- directory CRC = 0xAEE88BF2 over the 277-byte record sequence.
- layer record flags = 0x0003 (MU=1, PE=1), user-metadata record flags =
  0x0002 (MU=0, PE=1) — **fixed by §7.3's registry table**, and
  `[R-CNT-22]` makes a mismatch a verifier-detected violation (F28/L49).
  I did not have to guess.
- `mask` inline_length = 85, record 109 bytes; `sst` inline_length = 119
  (including its 25-byte sub-record), record 143 bytes; user-metadata
  record 25 bytes.
- `file_id`: Appendix G item 2 says to derive it. See **writer-02**.
- `version_minor` = 0, `flags` = 0, `generation` = 1, `reserved` = 0.

### 2.4 Commit order

Per `[R-LIF-02]`'s creation path: front signature block; then steps 2–6
writing from offset 16. Payloads and index regions and record extents in
step 2 (any order satisfying §5.2's coverage classes); the complete
directory and its CRC in step 3; **barrier**; pad and the
generation-1 trailer in step 5; **barrier**. Two barriers, not one —
§20.2 `[R-WRT-02]` says so explicitly ("both barriers, not one"), which is
the sort of thing that is easy to get wrong and the document called out.

### 2.5 Reading it back

I then wrote an independent verifier (`verify.py`) that knows nothing about
the builder, walking §19.1's four open steps, §19.3's layer validation,
§19.4's tile read, §15.4's index chain, §16's slab invariants, §14's
byte layout and offsets, `[R-COD-10]`'s inverse shuffle, and §9.7's
coverage walk. It reproduces every decoded tile image, confirms the
partition of `[R-CNT-02]`, finds no overlap, and reports:

```
COVERAGE: 11 claimants, no overlap.  SLACK TOTAL = 62 bytes
   (6 alignment gap + 56 pre-trailer pad)
```

The round trip is clean. Nothing in the creation path defeated me.

---

## 3. The append procedure

### 3.1 Generation 2, concretely

Commit: supersede `sst` tile 0, newly store `sst` tile 1 (was sentinel),
add a zero-extent layer `dem`, and replace the file-scope user-metadata
document.

Step 1 — **establish F**. `[R-LIF-04]`: validate the trailer in the final
64 bytes of the *physical* file. F = 832, generation = 1, file_id =
0xD44980B7CE79C479. Physical length is 832, so no truncation is needed.

Step 2 — **open** (§19.1). The appender is a reader here (`[R-WRT-01]`,
§20.3 step 2).

Step 3 — **validate what the commit touches** (`[R-WRT-03]`): the trailer
and the *full* directory always, because re-emission relies on every
directory byte; plus §19.3 layer validation for `sst` (modified) and
`dem` (new); plus §19.4's index chain for every segment whose entries the
commit reuses — `sst`'s single segment, since entries 2 and 3 are carried
forward. Notably **not** §19.3 for `mask`: the commit neither modifies nor
relies on it. This is stated and I relied on it.

Step 4 — **write payloads and indexes**, beginning at exactly F = 832:

```
[   832,   864)    32  sst tile 0' (supersedes the tile at 108)
[   864,   896)    32  sst tile 1  (was a sentinel)
[   896,   980)    84  sst tile-index region, re-emitted IN FULL
[   980,  1087)   107  new file-scope user-metadata extent
[  1087,  1468)   381  complete directory (4 records)
[  1468,  1472)     4  pre-trailer pad
[  1472,  1536)    64  trailer, generation 2, same file_id
F2 = 1536
```

The index region is re-emitted whole — entry 0 re-pointed, entry 1 written
to its new stored state, entry 2 the sentinel byte-identical, entry 3
byte-identical at its disk-ordinal position — because §20.3 step 4 requires
it of "every layer whose stored-tile set or index content this commit
changes", "necessarily at a new placement" since `[R-LIF-01]` freezes the
old bytes. `mask` is untouched and **keeps its extent slot pointing at
[64,108)**; `dem` has entry_count 0 and so extent slot (0,0) with
crc_of_crc_array 0 (`[R-CNT-17]`, `[R-CNT-23]`, and L22's "a nonzero slot
with entry_count = 0" is the row that would fire if I got it wrong).

`sst`'s layer record is new output (its extent slot and crc_of_crc_array
both change) but its user-metadata **sub-record is re-emitted
byte-identically inside it**, extent slot and all, still pointing at
[358,431). `mask`'s whole record is copied byte for byte out of
generation 1's directory. That is `[R-WRT-05]`.

I asserted mechanically that bytes [0, 832) are byte-identical before and
after. They are.

Step 5/6 — barrier; pad; trailer with generation 2, the same file_id,
unknown ignore-lane bits copied forward (there are none), version_minor =
max(floor, prior) = 0 (`[R-CNT-26]`); barrier.

The verifier re-reads generation 2 clean: 12 claimants, no overlap, slack
total 629 bytes.

### 3.2 What the append cost, and what became slack

```
new slack from this commit:
   superseded sst tile 0    [ 108, 140)     32
   superseded sst index     [ 172, 256)     84
   superseded usermeta ext  [ 256, 358)    102
   gen-1 dir + pad + trailer[ 431, 832)    401
   new pre-trailer pad      [1468,1472)      4
   (carried) alignment gap  [  18,  24)      6
                                 total     629
```

Two things I want on the record because they are easy to get wrong and the
document gets them right:

1. `sst`'s **untouched** tile 3 at [140,172) is still a live claimant even
   though everything around it became slack. The index region moved; the
   payload did not.
2. `sst`'s sub-record user-metadata extent at [358,431) is still live and
   sits *inside* a run of superseded bytes. Slack is not contiguous and
   is not a suffix.

### 3.3 The record-flag walk

The charter asks me to walk every combination the document defines and say
what my updater may do. §20.4's table is keyed on **stored** flags, but only
"For a type the updater does not implement"; the sentence before it —
"Persistence governs every record type; only the authoritative source of
the flags differs" — is what tells me the obligations are the same in all
cases and only the flag source moves. I relied on that sentence; without it
the table would be silent about types I do implement.

| Type | Flag source | MU | PE | What my updater may do |
|---|---|---|---|---|
| 0x0001 layer | §7.3 registry (fixed MU=1 PE=1); stored bits ignored | 1 | 1 | Retain byte-identical if unmodified; may modify it (that is the whole point of an append). **Never drop it** — §20.4's closing paragraph. If stored bits differ from 0x0003, I still apply the fixed semantics and the file is nonconforming (L49, verifier). |
| 0x0002 user metadata | §7.3 registry (fixed MU=0 PE=1) | 0 | 1 | Retain byte-identical, extent content unmodified, or modify it (new extent, old becomes slack — §20.3's shape (c)). **Never drop it** at either scope. |
| Unregistered, implemented | the outside definition it implements the type from; stored bits never | per that definition | per that definition | Same obligations as the corresponding row below, with flags from the definition. See **writer-04** for the MU=1 sub-case. |
| Unknown, top-level | stored | 1 | 1 | `[R-CNT-15]` makes it reject-file for me. **No commit is available at all**, and compaction is barred (`[R-WRT-06]`). |
| Unknown, top-level | stored (read as PE=1, `[R-CNT-12]`) | 1 | 0 | Identical to the row above. The writer that emitted it made the file nonconforming (F25, verifier). |
| Unknown, top-level | stored | 0 | 1 | Retain byte-identical, extent content unmodified. I may commit anything else. |
| Unknown, top-level | stored | 0 | 0 | Retain byte-identical, **or** drop it (extent becomes slack) — but only in a commit that *independently* changes the file's layer set or another *non-layer* top-level record. Superseding a tile does not license it; dropping it (or another record) does not license itself. |
| Unknown, layer sub-record | stored | 1 | any | reject-layer (`[R-CNT-18]`) — never reject-file. That layer is unmodifiable; **other layers stay editable**. If I do not modify that layer I never perform §19.3 on it and never learn the record is there; I copy the layer record forward byte-identically and commit. |
| Unknown, layer sub-record | stored | 0 | 1 | Retain byte-identical, extent content unmodified. |
| Unknown, layer sub-record | stored | 0 | 0 | Retain, or drop only in a commit that independently changes that layer's record, the entry set of its index, or which of its tiles are stored. |
| Any type | stored | — | — | Reserved flag bits 2–15 nonzero: I ignore them, re-emit byte-identically, and the file is nonconforming (F26/L47, verifier). I MUST NOT clear them — that would not be byte-identical re-emission. |

Everything in that table is decided by the document. The one place I had to
stop and think was the MU=0/PE=0 drop licence, and the paragraph closes the
self-licensing loop explicitly ("Dropping the record, or dropping another
record in the same commit, is not itself such a change either"). That is a
well-made rule.

A latent violation I carry forward stays a violation and travels with the
structure (§20.1 `[R-WRT-01]`, §20.3 step 2). I may not repair it —
`[R-LIF-01]` freezes the committed prefix — including a malformed index
entry, which §20.3 step 2 says goes forward "byte-identically at its
disk-ordinal position, not repaired to a sentinel". I SHOULD report it.

### 3.4 Two consequences of the append rules worth recording

**(a) Superseding one tile of a slab-declared layer forces re-emission of
that run's whole stored set.** `[R-SLB-04]` says a commit that changes the
stored-tile set, run partition, or byte placement of any run must
re-establish the invariants *for every such run* or clear the declaration.
The invariant is "each stored tile's offset equals the previous stored
tile's offset plus its length", and the earlier tiles' offsets are frozen
by `[R-LIF-01]`. So the only ways to re-establish are (i) re-emit every
stored tile of the affected run at new offsets — the old ones becoming
slack — or (ii) clear the declaration. The document determines this; it
does not spell out the cost, and §20.3's cost note ("dominated by its
index") does not mention it. That is an observation about emphasis, not a
defect: I file nothing.

**(b) The bar in §20.3 step 4 is a test on stored tiles, not a list.** I
worked several cases against it:

- Changing a channel's *type* between two types of the same element size
  (uint16 → int16, float32 → int32), keeping the fill bytes: reaches none
  of padding-position set, padding content, decoded size, sample byte
  offset, codec, filter. **Permitted** — and coherent, because §12.3
  `[R-TYP-04]` makes a sample value a bit pattern, so the reference array
  is literally unchanged.
- Flipping layout between interleaved and planar on a **single-channel
  numeric** layer: §14.4's Note says the tile images are byte-identical;
  entry_count is N either way (C·N with C=1) and the disk ordinal c·N+s
  reduces to s. **Permitted**, and it is not even an index change, so the
  extent slot is kept. On a single-channel **bool** layer the decoded size
  changes (P vs ceil(P/8)) so it is **barred** unless the layer stores
  nothing.
- Adding a channel to a **planar** layer: entry_count grows from C·N to
  (C+1)·N, existing ordinals c·N+s are unchanged for c < C, existing plane
  sizes and padding are unchanged. **Permitted**, with a full index
  re-emission. Adding a channel to an **interleaved** layer changes Q and
  so the decoded size: **barred** if any tile is stored.
- Changing a channel's fill on a layer with no padding position and no pad
  bit: **permitted** (§20.3's shape (c) says so). On my `mask` layer,
  which has pad bits, changing `m`'s fill from true to false would leave
  every stored pad bit violating `[R-SER-05]`: **barred**.
- Growing an extent: always permitted, and the document says why (a
  position that becomes real held that channel's fill, and fill is a legal
  sample value). Growth that raises a grid count renumbers disk ordinals
  via `[R-GEO-06]`; §20.3 step 4 says so parenthetically and that is the
  only place it is said normatively.

All of these are decided. I flag none.

---

## 4. Slack, by shape of commit

| Shape | What becomes slack | Who counts it | What it may contain |
|---|---|---|---|
| **Append (new layer)** | the prior generation's directory, pre-trailer pad and trailer, plus any alignment or slab gap the new payloads force. Sized by the file's *layer count*, never by any layer's data (§20.3's figure (a)). | verifier, via §9.7's walk of the live state; the number is `[R-CNT-21]`'s obligation | unconstrained. `[R-CNT-03]` advises zeroing the gaps *the writer creates*; superseded bytes cannot be zeroed, `[R-LIF-01]` forbids touching them. |
| **Append (tiles added / superseded)** | the above, plus the layer's whole prior index region, plus every superseded payload | same | same |
| **Append (directory only)** | the prior directory, pad and trailer alone | same | same |
| **"In-place update"** | does not exist. `[R-LIF-01]` makes every conforming mutation a commit or a whole-file rewrite. Every "update" is an append. | — | — |
| **Whole-file rewrite (new file_id)** | nothing carried; the input file persists untouched until something outside this specification deletes it (`[R-PRV-02]`) | — | — |
| **Compaction** | none *carried* — §20.5's output holds only what the input's live trailer reaches. The output still has its own alignment gaps and pre-trailer pad, which are slack. | verifier of the output | unconstrained |
| **Abandoned partial write** | **none — the bytes past F are not slack at all.** §5.2's coverage is a property of the live committed state, and §5.1 requires a conforming file's size to equal F. A file with residue is nonconforming, not a conforming file with extra slack. A reader meets it as F8/F14/F17 (§9.5's Note is explicit). What it violates is `[R-LIF-04]`'s writer obligation to truncate or overwrite. | see **writer-03** | — |

The verifier's slack total is `F` less the bytes the walk claims (front
block + trailer + directory + each record's extent + each non-sentinel
entry's stored extent, with structurally-malformed entries contributing
nothing). My verifier computes 62 for generation 1 and 629 for generation 2
and both are exact totals from a complete walk.

Partial totals: `[R-CNT-21]` makes a partial total an *upper* bound, which
is arithmetically right — dropping claimants can only increase F minus the
claimed set — and requires the verifier to name what stopped the walk. That
holds for a rejected layer and for a stop-at-first-violation verifier. It
does not hold when the walk cannot start; see **writer-03**.

---

## 5. Torn-write recovery: four crash points

Throughout: F = 832 is generation 1's committed length; the generation-2
commit runs 832 → 1536.

**Crash A — after step 2 (payloads and the new index region written),
before step 3.** Physical length ≈ 980. The final 64 bytes are index/extent
bytes.
*Next reader*: takes the final 64 bytes as the trailer; the magic fails →
**reject-file** (F8), reported as torn or invalid, and `[R-LIF-05]` forbids
scanning backward. *Next updater*: `[R-LIF-04]` — trailer validation
fails, "the file is torn: the writer MUST NOT append". It must run §9.6's
recovery as a deliberate, separate operation. *Conforming in the meantime?*
**No.** The byte sequence has no valid trailer at its end. The old state is
recoverable, not readable — §9.2's crash figure says exactly this.

**Crash B — after step 3 (directory written) and its barrier, before the
trailer.** Physical ≈ 1468. Identical from a reader's point of view: the
tail is directory bytes, F8 fires. The complete generation-2 directory is
sitting in the file and is unreachable, which is precisely the property
step 5's trailer is there to switch on.

**Crash C — mid-trailer.** The trailer begins at 1472, a 64-aligned
offset. Suppose 32 of its 64 bytes landed. Physical = 1504.
*Next reader*: final 64 bytes are [1440,1504) — pad tail plus half a
trailer. No magic at [1440,1448) → F8, reject-file.
*Recovery* (§9.6): the probe begins at the largest 64-aligned o with
o+64 ≤ 1504, which is o = 1440. No magic. o = 1376, 1312, ... down to
1472? — no: the probe walks *backward* from 1440, so it never sees 1472,
and 1472+64 = 1536 > 1504 anyway. It reaches o = 768, finds the
generation-1 magic, the trailer CRC verifies, and committed_file_length =
832 = 768+64. Truncate to 832: generation 1 restored exactly.
The dangerous sub-case — the magic landed at 1472 but the CRC bytes did
not — cannot arise here because 1472+64 exceeds the physical length and
the probe never offers it as a candidate. Had the file been longer, the
candidate would have failed its CRC and the probe would continue past it,
which §9.6 states.

**Crash D — trailer written, step 6's barrier not reached.** After
reboot the trailer is either durable (the commit took, F = 1536, reader
opens generation 2) or not (crash C's analysis). Both states are handled
and neither is silently wrong: §9.2's Note is right that weaker barriers
degrade "torn commits are invisible" to "torn commits are detected".

**Crash E — the overwrite path.** `[R-LIF-04]` lets a writer overwrite
from F rather than truncating first, provided the physical file is
truncated to the new committed_file_length "no later than step 6". Suppose
crash A left residue to 980 and the next attempt overwrites from 832 to a
new F' = 1536, crashing after writing the trailer at 1472 but before
truncating (physical still, say, 1600 from an even earlier attempt).
Final 64 bytes = [1536,1600), garbage → reader says torn. Recovery probes
from o = 1536 (1536+64 = 1600 ≤ 1600): garbage. Then o = 1472: magic,
CRC verifies, committed_file_length = 1536 = 1472+64. **Candidate
accepted, truncate to 1536 — the new commit is recovered, not the old
one.** That is correct and it is what `[R-LIF-04]`'s "no later than step 6"
buys. §9.6's mandatory whole-file re-verification of the recovery output
catches the residual case where a payload byte string mimics a trailer.

I could answer every one of these from the document. The recovery
machinery is the most carefully specified part of the document I touched.

---

## 6. Byte-divergence catalogue, item by item against Appendix G

Given identical input arrays and identical stated options, here is every
legitimate way two conforming writers may produce different bytes that I
could find, and whether Appendix G closes it.

| # | Degree of freedom | Licensed by | Appendix G |
|---|---|---|---|
| 1 | Order and relative position of every structure in the file | `[R-SLB-05]`, `[R-LIF-02]` step 2 | **closed** by item 3 (total emission order) |
| 2 | Size of the gap between structures | `[R-SLB-05]`; §5.2 makes any unclaimed byte slack | **closed** by item 3, *except* the offset of the first structure — **writer-05** |
| 3 | Content of every gap and of the pre-trailer pad | `[R-CNT-03]` (SHOULD only) | **closed** by item 3 (zeroed, "taken as a requirement here") |
| 4 | Record order within the directory | `[R-CNT-14]` | **closed** by item 3's ordering key |
| 5 | Sub-record order within a layer record | `[R-CNT-14]` via `[R-CNT-18]` | **closed** by item 3 ("Records and a layer record's sub-records alike") |
| 6 | `file_id` (any nonzero value) | §6.2, §9.3 (SHOULD random) | **partly closed** by item 2 — but see **writer-02** |
| 7 | Compressed-stream bytes for codecs 2–4 | `[R-CNF-05]`; RFC 1951/8878 constrain decoders, not encoders | **closed** by item 1, by pinning the encoder — and item 1 is honest that byte-identity *across* implementations is unattainable here |
| 8 | DEFLATE's up to seven unused high bits in its final byte | §17.2's Note, explicitly unconstrained | **closed** by item 1, and the Note says so |
| 9 | zstd `Frame_Content_Size` present or absent | `[R-COD-06]`: "MAY be present" | **closed** by item 1 (fixed encoder settings) |
| 10 | Whether an all-fill tile is stored or left sentinel | nothing requires storing any tile; §13 makes both denote the same reference array | **closed** by item 6 |
| 11 | The fill recorded when the caller chooses none | `[R-TYP-10]` (SHOULD all-zero) | **closed** by item 7 — and item 7 correctly notes this reaches further than eight bytes, because item 6 makes the tile set depend on it |
| 12 | `version_minor` | `[R-CNT-26]` (SHOULD floor) | **closed** by item 8 |
| 13 | `flags` | `[R-CNT-08]` already forces 0 for a writer under this text | closed (and item 8 restates it) |
| 14 | Whether to declare an alignment or a slab, and at what value | §16 leaves it entirely to the writer | **closed** by item 5 |
| 15 | JSON serialization of user metadata: whitespace, number formatting, escaping | `[R-MTA-05]` sorts members but explicitly does not make two writers agree | **closed** by item 9, by pinning the producer |
| 16 | Unicode normalization of names | `[R-ENC-14]` (SHOULD NFC) | **closed** by item 10, which correctly observes that this moves `inline_length` and `dir_length` too |
| 17 | How many commits the work is split into | §9 nowhere constrains it | **closed** by item 4 |
| 18 | The segment CRC of a full all-sentinel segment | `[R-IDX-05]` lets a writer emit the constant without computing it | **not a divergence** — the constant equals the computed value; I verified 0xEECB3BB2 |
| 19 | Whether the tile-index region exists for entry_count = 0 | `[R-CNT-17]` forces extent (0,0) | **not free** |

I could not classify anything else as free. Every remaining choice I made
while building was either forced by a rule or was one of the charter's
"stated options" (tiling, layout, codec, filter, names, fill, channel and
dimension order).

**Claims in Appendix G I tried to falsify and could not:**

- Item 3's ordering key is genuinely a function of content. I specifically
  checked the circularity it was clearly written to avoid: a **layer**
  record's inline payload contains `crc_of_crc_array`, which depends on the
  entry offsets, which depend on placement — so a key over the inline
  payload would be circular for type 0x0001. The text ties type 0x0001 by
  **layer name** instead, and layer names are unique by `[R-ENC-15]`. That
  is correct, and it is not obvious.
- Masking `extent_offset` to zero: correct, and the stated reason (the key
  would depend on its own result) is right.
- "Two records this key does not separate are byte-identical ... emitting
  them in either order yields the same file": I checked this. Two tied
  records have equal `extent_length` and identical extent contents, so
  swapping which gets the lower offset produces the same byte sequence.
  True. And ties can only occur among unknown types, since two file-scope
  user-metadata records are barred by `[R-CNT-14]` and two layer records
  cannot share a name.
- Item 2's claim that re-deriving `file_id` on an already-compact input
  would reproduce the input's own `file_id`: true, since the hash input is
  [0, F−64) plus the trailer's first 60 bytes with `file_id` zeroed, and a
  compacted input is already at generation 1.
- Item 6 plus item 7 interacting: correct and non-obvious, and the appendix
  says so.

---

## 7. Findings

### writer-01 — CONTRADICTION — §21.1's instance criterion is not applied to L21, L22, L30 or F17

**Location:** §21.1 (the instance criterion); §21.3 rows L21, L22, L30;
§21.2 row F17. Requirement identifiers `[R-ERR-02]`, `[R-CNT-17]`,
`[R-CNT-23]`, `[R-CNT-06]`.

**Quotation (the criterion, §21.1):**

> Two axes recur often enough to be stated rather than judged each
> time. Where the quantity a condition derives varies by layout, the
> layout formulas are materially different shapes and the cell
> enumerates them. Where the condition compares two quantities and
> either can be the greater — a *differs from* or *does not equal* —
> the two directions are likewise enumerated; where its own text
> bounds the comparison in one direction — an *exceeds*, a *larger
> than* — there is one.

**Quotation (a row that applies it, T14):**

> | T14 | Codec 1 (none) declared and a non-sentinel index entry's length differs from the tile's decoded size | interleaved P·Q, length longer; interleaved P·Q, length shorter; planar numeric P·Bᶜ, length longer; planar numeric P·Bᶜ, length shorter; packed planar bool ⌈P/8⌉, length longer; packed planar bool ⌈P/8⌉, length shorter | reader | tile use | `[R-COD-04]` |

**Quotations (the rows that do not):**

> | L21 | entry_count does not equal the geometry-derived addressed-tile count (N interleaved, C·N planar) | interleaved N; planar C·N | reader | layer access | `[R-CNT-17]` (R-CNT-20) |

> | L30 | A channel entry's fill length prefix differs from the element size of the channel's declared type | — | reader | layer access | `[R-CNT-23]` (R-TYP-06) |

> | F17 | Trailer committed_file_length does not equal the transport-authoritative file size (physical file not truncated or extended to it) | committed_file_length | reader | open | `[R-CNT-06]` (R-LIF-04, R-CNT-10) |

> | L22 | Under index_encoding 1, extent_length ≠ entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 — including slot (0,0) with entry_count > 0, or a nonzero slot with entry_count = 0 | extent_length against the formula; slot (0,0) with entry_count > 0; a nonzero slot with entry_count = 0 | reader | layer access | `[R-CNT-17]` (R-ENC-07, R-CNT-20) |

**Why this is a contradiction and not a judgement call.** §21.1 states the
two axes as rules — "stated rather than judged each time" — and says "the
count is therefore mechanical once the cell is written". T3, T14 and T22
apply both axes (3 layouts × 2 directions = 6 instances each). L21 applies
the layout axis and not the direction axis. L22, L30 and F17 apply neither,
and L30 and F17 use the criterion's own trigger words verbatim ("differs
from", "does not equal"). L21 is wrong under *either* reading of the
criterion — whether the direction axis is independent (as "Two axes"
implies) or coupled to the layout axis — because it enumerates the layout
formulas and stops.

Each of the four omitted directions is a distinguishable file:

- **L21** — interleaved entry_count = N+1 vs N−1; planar C·N+1 vs C·N−1.
  Four files, not two.
- **L22** — extent_length above the formula vs below it, plus the two named
  alternatives. Four, not three.
- **L30** — a fill length prefix of 4 on a uint16 channel pushes the
  remaining parse forward two bytes; a prefix of 1 pulls it back one. Two
  files with materially different downstream damage, not one.
- **F17** — committed_file_length below the transport size is *residue past
  a completed commit*, which §9.5's Note discusses at length; above it is a
  *truncated* file. The row's own parenthetical names both ("physical file
  not truncated or extended to it") and then enumerates one.

**Which reading I picked and what I did.** I took §21.1's criterion as
governing, on the strength of §21.1's own "where a row and the rule it cites
diverge, the rule governs" and of the criterion being stated as a rule
rather than a description. Under that reading the register's instance count
is **274, not 268**, and §21.8's sentence

> Every row of §21.2 through §21.5 — 121 conditions over 268
> instances — has at least one conformance vector (§24) whose expected
> outcome is that row's outcome, and one vector per instance.

is short by six vectors. I verified mechanically that 268 is exactly what
the cells as written sum to (F 56, L 111, T 57, R 44), so the document is
internally consistent with itself and inconsistent with its own criterion.

**What an implementer does wrong without it.** A corpus builder working
from the cells ships 268 vectors and believes coverage is complete;
`[R-ERR-02]` says "A row without a vector is a gap in the corpus, not a
licence to skip the check", and `[R-VEC-03]` says "every register row has at
least one vector for each instance it names". Six checks — including
"residue past a completed commit", the one torn-write state a reader can
actually observe — go untested while the corpus reports full coverage.

**Byte-level: no.** Both directions of every one of these four conditions
are already rejected by the same rule with the same outcome and at the same
tier, so no two conforming implementations can disagree about any byte or
any accept/reject verdict. What changes is the size of the conformance
corpus, which `[R-VEC-01]` makes derivative of the specification rather than
constitutive of it.

---

### writer-02 — AMBIGUITY — Appendix G item 2: "low eight digest bytes" is not decidable

**Location:** Appendix G, item 2.

**Quotation:**

> **`file_id` from a cryptographic hash of the file's own emitted
> bytes**, computed over [0, F − 64) together with the trailer's
> other fields with the `file_id` field taken as zero, then written
> in — the hash a named function at a named version, its input the
> bytes [0, F − 64) followed by the trailer's first 60 bytes with the
> `file_id` field zeroed, and the identifier its low eight digest
> bytes read little-endian

**The permitted readings.** A digest is a byte string with no intrinsic
numeric orientation. "Low eight digest bytes" can mean:

(a) the **last** eight bytes, if the digest is read as a big-endian
integer — the universal convention for printing and comparing hashes; or

(b) the **first** eight bytes, if the digest is read as an array and "low"
means lowest-indexed.

"read little-endian" does not disambiguate: it says how to turn the chosen
eight bytes into a `u64`, which is orthogonal to which eight.

**Which I picked and why.** I picked (a), on the ground that hashes are
conventionally spoken of as numbers and "low" is a numeric word; I noted
the choice in `build.py` and computed both. For my generation-1 file the two
readings give:

```
sha256 digest = 788c9cdede88a1c0166ece83ebe684b62dffde6077ef345b79c479ceb78049d4
reading (a), last 8 bytes  -> file_id = 0xD44980B7CE79C479
reading (b), first 8 bytes -> file_id = 0xC0A188DEDE9C8C78
```

**What an implementer does wrong without it.** Two writers that have agreed
on everything the profile asks them to agree on — the same named hash
function at the same named version, the same emission order, the same
encoder — emit files differing in trailer bytes [48,56) and, consequently,
in the trailer CRC at [60,64). The profile's stated purpose is that
"Applications that need byte-identical output — content-addressed storage,
reproducible builds — can adopt this profile, which closes the degrees of
freedom this format deliberately leaves open", and this is a degree of
freedom it does not close. It is also the one item in the profile whose
failure is silent: the two files are both conforming, both profile-shaped,
and differ only in the identifier a content-addressed store would key on.

The fix is one word: "trailing eight" or "leading eight".

**Byte-level: no.** Appendix G is non-normative and, in its own words, "adds
no requirement to any actor: a writer ignoring it is fully conforming". Both
`file_id` values satisfy §6.2 (nonzero) and §9.3, so no conforming
implementation's emit set or accept/reject verdicts change. The divergence
is between two *profile* adopters, not two conforming writers.

---

### writer-03 — AMBIGUITY — `[R-CNT-21]`'s slack-total MUST cannot be discharged when there is no live trailer

**Location:** §5.2 `[R-CNT-21]`, with §9.7 `[R-LIF-08]`, §6.2 `[R-CNT-06]`
and §21.2 rows F8/F14/F17. Appendix H's verifier checklist restates it.

**Quotation (§5.2):**

> A reader MUST NOT interpret it (§9.5); a verifier MUST
> report the total number of slack bytes, since that number is what
> tells an operator to compact. Where the walk of §9.7 does not
> enumerate every region's claimants — whether because a scope-level
> rejection ends that scope's enumeration (a rejected layer's claimants
> are not enumerated, whether or not the rejection impeded reading
> them), or because the verifier elected under `[R-CNF-11]` to stop at
> the first violation — the verifier MUST report the total
> as partial. A partial total is F less the bytes claimed by the
> claimants the walk did enumerate

**The problem, hit while implementing crash cases A–C above.** My verifier
is handed the mid-commit file of §5's crash A. Its final 64 bytes are not a
trailer, so F8 fires: a **file-scope** rejection, which is "a scope-level
rejection [that] ends that scope's enumeration". `[R-CNT-21]` therefore
requires a partial total, defined as "F less the bytes claimed by the
claimants the walk did enumerate". But `F` is defined nowhere except as the
live trailer's `committed_file_length` — §5.1: "The file size of a
conforming file equals the live trailer's committed file length F"; §6.2's
table: "committed_file_length | structural | = F". With no valid trailer
there is no F, and §9.7's walk — "From the live trailer it reads the live
directory" — has no starting point. The quantity the MUST demands does not
exist.

The same hole opens at F14 (trailer CRC fails, so `[R-ENC-10]` bars acting
on `committed_file_length`) and at F17 (the trailer's F is known but is not
the file's size, so "F less the bytes claimed" is a number about a file the
verifier was not given).

**The permitted readings.**

(a) The MUST is unconditional and the specification is asking for something
undefined in exactly the cases where a torn file is most likely to be
handed to a verifier.

(b) The obligation presupposes a live trailer, because it is expressed over
"the walk of §9.7", and §9.7's walk is defined to start from the live
trailer. When the trailer gate fails there is no walk, therefore no total,
partial or otherwise.

(c) `F` in this one sentence means the physical file length. This is
excluded: §5.1, §6.2 and every register row use F for
`committed_file_length`, and F5's instance cell even distinguishes "F
(physical file size); committed_file_length" as two things.

**Which I picked.** (b). My verifier reports *nonconforming* with the row
that fired, and "slack total: not computable — no live trailer", naming the
gate that stopped the walk as `[R-CNT-21]`'s last clause requires. I am
confident this is what was intended; I am reporting it because the MUST is
written without the precondition, the verdict machinery of §2.3 makes
*cannot establish* unavailable here (an established violation takes
priority), and Appendix H repeats the obligation without the precondition
either.

**Byte-level: no.** The verdict is *nonconforming* under every reading; only
the shape of the verifier's report changes. No byte a writer emits and no
accept/reject decision turns on it.

---

### writer-04 — OBSERVATION — `[R-WRT-07]`'s "No other record payload carries a file offset" has a case §7.2 expressly permits

**Location:** §20.5 `[R-WRT-07]`, against §7.2 `[R-CNT-13]` and §20.5
`[R-WRT-06]`.

**Quotation (§20.5):**

> No other record payload
> carries a file offset: MU = 0 records by rule (§7.2), and an
> MU = 1 type the compactor does not implement never reaches this
> step (`[R-WRT-06]`).

**Quotation (§7.2):**

> Records with MU = 1 carry further references only where this
> specification or registry review (§10) defines them; the
> layer record's tile index (§15), whose entries reference stored-tile
> extents, is such a case.

**The gap.** The justification enumerates two cases and there are three.
A record of a type this specification has not assigned, carrying MU = 1,
registered by a later minor version (§10.1 vehicle 1, §10.4), **and
implemented by the compactor**, is barred by neither clause: §7.2's
prohibition on embedded offsets binds MU = 0 records only, and
`[R-WRT-06]` refuses compaction only for "any record whose type it does not
implement with MU = 1". §7.2 expressly contemplates such a type carrying
further references. For that record, `[R-WRT-07]` gives no instruction, and
`[R-WRT-05]`'s byte-identical re-emission — from which §20.5 carves out
only extent slots, regenerated index regions and `crc_of_crc_array` — would
require carrying stale offsets forward into a relocated file.

**Why I am filing it as an observation rather than an ambiguity.** It is
decidable that the text does not cover the case; it is not decidable from
the text what a compactor should do, but no implementation of *this* text
can reach the case, since the only MU = 1 type this text assigns is the
layer record and `[R-WRT-06]` bars everything else. It is the kind of
unresolvable forward reference the brief calls expected — except that
`[R-WRT-07]` states it as a completed enumeration rather than as a
condition on this text's type set, and §10.4's registration requirements
(semantics, security review, MU/PE assignment) do not require a new type to
say how a compactor relocates it. A one-clause fix ("and an MU = 1 type
this specification does not assign is relocated only under the rules its
registration states") would close it.

**Byte-level: no.** No implementation of format major 1 as this text defines
it can encounter the case: the compactor either implements no unassigned
MU = 1 type (and `[R-WRT-06]` refuses) or is implementing a specification
this document has not yet written.

---

### writer-05 — OBSERVATION — Appendix G item 3 pins the gap between structures but not the offset of the first one

**Location:** Appendix G item 3, against §5.2 `[R-CNT-02]`.

**Quotation (Appendix G item 3):**

> Each structure begins where the previous one
> ended, save where alignment forces a gap — a
> declared A or A_slab, or §6.2's 64-byte trailer alignment, the
> pre-trailer pad included — and every byte of every such gap is zero

**Quotation (§5.2 `[R-CNT-02]`, defining the term):**

> Every byte of the live committed state belongs to exactly one of: the front signature block; or a **structure** — a
> stored-tile extent, a record extent (the bytes any record's extent
> slot references, whatever the record's type, §7.2), the directory, or
> the trailer.

**The gap.** §5.2 makes "structure" a defined term that **excludes** the
front signature block — the block is its own coverage class, listed
alongside "or a structure" rather than as one. Appendix G uses "structure"
in that defined sense elsewhere in the same item ("the space between
structures is free in either extent or content"). So item 3's rule has no
"previous one" for the very first structure, and nothing in the item fixes
its offset. A profile adopter that begins its first stored tile at 16 and
one that begins it at 512 both satisfy every sentence of item 3, and emit
files that differ from byte 16 onward.

**Which reading I picked.** I placed the first structure at 16, reading the
item's title — "A total emission order, **contiguously**" — as governing,
and treating the front block as the implicit antecedent. That is plainly
the intent. I report it because the appendix's closing paragraph claims
precisely this as one of the freedoms item 3 supplies:

> the list is not short: gap *content*, which `[R-CNT-03]` only advises;
> gap *extent*, which placement freedom (`[R-SLB-05]`) leaves open

Gap extent at the head of the file is exactly the one instance the rule's
own wording does not reach, and it is the one place where a leading gap is
most tempting (a writer aligning its first payload, or reserving room).
Naming the front signature block, or saying "the first structure begins at
offset 16", closes it in five words.

**Byte-level: no.** Appendix G "adds no requirement to any actor"; both
placements are conforming files under §5.2 and `[R-SLB-05]`, so no
conforming implementation's emit set or verdicts change. The divergence is
between two profile adopters.

---

## 8. Things I checked and did not file

Recorded so that a later round does not have to redo them, and so the size
of this list is visible next to the size of the one above.

- **§21's counts.** 36 + 49 + 26 + 10 = 121 conditions; the instance cells
  sum to 268 exactly as §21.8 claims. Every verifier-detected row carries
  detection point *certification* and every reader-detected row carries one
  of §19.2's four tiers, as §21.1 requires. No anomalies.
- **§21.1's specialization list** ("F1 of F6 and of F8, F35 of F36, L24 of
  L25") is not exhaustive — T11 (offset or length above 2⁶³−1) is a strict
  specialization of T9 (extent ends past F−64), and F2 of F10 likewise —
  but detector and detection point coincide in both pairs, so nothing turns
  on it, and §24's rule for conditions that cannot be isolated already
  covers a vector that exercises two rows.
- **§2.3's conduct-rule list.** I looked for a MUST on writers whose
  violation this text declares not to be a file-conformance violation and
  which is *not* one of the two named. §10.3 and §18.3 are named
  separately; `[R-MTA-07]`, `[R-CNT-26]`, `[R-CNT-03]`, `[R-ENC-14]`,
  `[R-TYP-10]` and `[R-LIF-07]` are all SHOULDs, which `[R-CNF-12]` already
  excludes. `[R-MTA-05]`, `[R-CNT-12]`, `[R-CNT-22]`, `[R-SLB-04]` are all
  expressly file-conformance violations with register rows. The list holds.
- **A pre-trailer gap longer than 63 bytes** is indeed conforming (nothing
  bounds the pad's length; `[R-CNT-05]` bars only *structures* there) and
  is indeed produced by no conforming commit (`[R-LIF-02]` step 5). §2.3's
  new sentence is right, and it is right that this is a witness-bearing
  writer violation that is nonetheless not a file-conformance violation.
- **§4.7's "version_minor is the only descriptive field".** I tested it
  against the trailer's reserved bytes, `file_id`, the record flag bits of
  registered types, `crc_of_crc_array` at entry_count 0, and the
  user-metadata encoding byte. All are structural, and the registered
  types' MU/PE bits are structural only because §4.7 says "a conforming
  reader **or verifier**" — that phrase is load-bearing and correct.
  §18.4's standardized keys are not fields (they have no layout table), so
  they do not falsify the claim.
- **§4.7's Note on which columns each table omits** says §7.4's table
  "omits the offset and class columns"; it also omits *size*, which is
  folded into its Type column. The general clause "each table giving the
  columns its structure needs" covers it. Not filed.
- **§15.3's "Six rows are marked structural"** — I counted six. Correct.
- **The structural-entry transparency repair** is consistent across four
  places: §15.3 (contributes no stored extent), §16.2 (transparent to run
  continuity, and a crc-failing entry is *not*), §9.7 (contributes nothing
  to the coverage walk), and L41's parenthetical. §16.2's claim that "this
  invariant stays decidable from index bytes alone" is true: whether an
  entry participates is decided by its own 20 bytes, and the crc-failing
  case is decided *into* participation, not out of it.
- **§20.4's MU=0/PE=0 drop licence** is closed against self-licensing and
  against supersede-only commits. I could not construct a commit where the
  licence is undetermined, except for the thin question of whether *adding*
  a non-layer top-level record counts as changing "another *non-layer*
  top-level record"; both answers leave the resulting file conforming and
  the obligation has no single-file witness, so I did not file it.
- **§21.7's second paragraph** does not enumerate `[R-LIF-02]`'s barriers
  and step ordering, `[R-WRT-04]`'s bar on gratuitously relocating a live
  index region, `[R-WRT-05]`'s byte-identity, or `[R-WRT-08]`'s no-re-encode
  — all no-single-file-witness obligations. §21.1 calls §21.7 "the account,
  **by class**, of what fails" detectability, and the class is named. Not
  filed.
- **`[R-CNT-13]`'s "neither its inline payload nor its extent contents
  encode offsets or lengths of other file bytes"** read literally would make
  a user-metadata document carrying an application byte offset
  nonconforming, which collides with `[R-MTA-01]`'s "this specification
  defines its encoding, not its meaning". I read it as forbidding a
  *sanctioned reference*, not any numeral. §21.7's justification for
  omitting it ("opaque by construction") is false for type 0x0002, whose
  extent a verifier fully decodes — the conclusion is right for a different
  reason. Too thin to file.
- **§24's "a conforming file can carry a record a reader ignores (§21.5,
  §21.6)"** sits oddly beside §21.5's "Every row here is a violation all the
  same ... never makes the file conforming". The charitable reading — the
  citation serves the sentence's pair of clauses, not its first alone — is
  available, and `[R-VEC-01]` self-heals a mislabelled vector. Not filed.
- **`[R-IDX-05]`'s "a partial segment's CRC MUST be computed"** is a
  technique requirement, mildly at odds with §2.1's Note that requirements
  "constrain bytes and observable behavior, never implementation
  technique". No byte consequence. Not filed.
- **`[R-LIF-02]` step 1's "begin writing at exactly F"** against a declared
  alignment: the writer writes the alignment gap (which `[R-CNT-03]`
  explicitly contemplates it creating) and then the aligned structure, so
  there is no conflict, and a writer that seeks past the gap produces
  identical bytes. Not filed.
- **Every worked example in the document** (§4.6, §7.4, §11.2, §11.4,
  §12.3, §14.2, §14.3, §14.5, §15.4 ×2, §16.2, §17.3, Appendix A). All
  correct.
- **Appendix B** against the sections it collects, and **Appendix C**
  against §10.2 and §7.3. All consistent.
- **Appendix H**'s five checklists against §2.3, §21.5, §21.6, §21.9,
  §20.4, `[R-CNF-03]`, `[R-SER-08]`. All consistent; I specifically checked
  the reader row's "the sole resolved byte being a nonconforming
  interleaved boolean" against `[R-TYP-04]`'s "In a conforming file this
  rule admits no exception", and they agree.
- **§21.9's arithmetic notes.** 2³² entries / 2¹⁶ per segment × 4 bytes =
  256 KiB; 2³⁶ gives 4 MiB; 65,536 × 20 = 1.25 MiB per full segment. All
  correct. The "tens of gigabytes" for a 2³² index region is 85.9 GB —
  loose but not false.

---

## 9. Confidence

I would ship a writer, an appender and a verifier from this document
without asking a question that changes a byte. The four crash points, the
whole flag matrix, the slack accounting and the byte layout were all
determined; the only place I had to guess about actual bytes was
Appendix G's `file_id` derivation, and Appendix G binds nobody. The one
substantive defect I found — writer-01 — is in the corpus build list rather
than in the format.

Transcript finding count: **5**.

---
*Editorial note: one ordinary-English word meaning "the thing that came before" was substituted throughout this verbatim transcript (to "antecedent"), per the repository's vocabulary gate. No other change was made.*
