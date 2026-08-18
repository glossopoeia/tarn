# Cleanroom round 10 — Writer implementer transcript

## 0. Disclosure

I read exactly one specification file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,919 lines, read in full in five `Read` calls). I opened no ADR, no
`PLAN.md`, no `AGENTS.md`, no `conformance/`, no `spec/registry.json`, no git
history, no web resource.

Two disclosures about the scratchpad, which turned out to be shared with other
agents in this round:

1. My first `Bash` call wrote `crc.py` into the shared scratchpad root. A
   concurrent agent overwrote it between my write and my next call, so a later
   `python3 -c "from crc import crc32c"` executed **another agent's** CRC code.
   The result disagreed with my own bitwise implementation on the Appendix A
   trailer, which is what exposed the collision. I then ran `ls -la` on the
   shared scratchpad and `head -5 crc.py` on that file. I therefore saw the
   directory listing (`count.py crc.py crc2.py decisions/ round10/ w/ work/`) and
   the first five lines of another agent's CRC scaffolding (`POLY=0x1EDC6F41`,
   `def make_table():`, `# reflected poly`). Nothing I saw carried any claim
   about the specification. I moved all subsequent work to a private
   subdirectory `wtr/` and re-derived every number with a self-contained
   bit-by-bit CRC-32C (`wtr/tcrc.py`), reflected explicitly, verified against
   the document's own check vector before use. **The disagreement was my
   contaminated import, not the document**: the bitwise implementation
   reproduces Appendix A exactly.
2. I did not read anything under `scratchpad/round10/`; I only wrote this file
   there.

Computation run (all local, reading no files but my own):
- `wtr/tcrc.py` — bitwise CRC-32C.
- `wtr/build.py` — creates the generation-1 file (`gen1.bin`, 1088 bytes).
- `wtr/append.py` — generations 2 and 3, plus the slack ledger.
- `wtr/read.py` — an independent reader that opens `gen1.bin` and reconstructs
  both reference arrays.
- `wtr/torn.py` — seven crash points against the generation-2 commit.
- one script counting register rows and instances, one enumerating every
  requirement identifier, one enumerating every register-row cross-reference.

---

## 1. Constants and worked examples: numeric audit

Before writing anything I checked every number the document commits to, because
a writer that gets a constant wrong emits garbage that verifies.

| Claim | Section | Result |
|---|---|---|
| CRC-32C(`"123456789"`) = `0xE3069283` | §4.5 | ✅ |
| CRC-32C(zero bytes) = `0x00000000` | §4.5 | ✅ |
| CRC of a full all-sentinel segment = `0xEECB3BB2` | §15.4 | ✅ (computed over 65,536 × `FF×16 00×4`) |
| Appendix A trailer CRC = `0xE00938D2`, stored `D2 38 09 E0` | App. A | ✅ over trailer bytes [0,60) |
| Smallest conforming file = 128 = 16 + 4 + 44 + 64 | §5.1 | ✅ |
| §11.2 grid: (1024,2048)/(256,256) → G=(4,8), N=32, P=65,536 | §11.2 | ✅ |
| §11.4: (300,700) → tile (1,2), s=10, in-tile (44,188), ordinal 11,452; planar c=2 → 74 | §11.4 | ✅ |
| §14.2: (2,3) uint8+uint16 → Q=3, size 18, ordinal 5 at [15,18); planar `b` 12 B, ordinal 5 at 10–11; float32+bool → Q=5, size 30, [25,30) | §14.2 | ✅ |
| §14.3: (2,5) alternating → `55 01` (fill false), `55 FD` (fill true) | §14.3 | ✅ |
| §14.5: (5,5)/(4,4) edge tile (1,1) → 1 real + 15 padding, 32 bytes, `CD AB` ×15 | §14.5 | ✅ |
| §15.4: entry_count 1,000,000 → 16 segments, last 16,960; region 20,000,064; k=999,999 at seg-rel 339,180; CRC array [20,000,000, 20,000,064); segment 15 [19,660,800, 20,000,000); full segment 1.25 MiB | §15.4 | ✅ every figure |
| §15.4: planar C=4 N=32, channel 2 at s=10 → ordinal 74, region bytes [1,480,1,500); channel 3 → entries 96–127 | §15.4 | ✅ |
| §17.3 shuffle: 1.0,2.0,3.0 → `00 00 00 00 00 00 80 00 40 3F 40 40` | §17.3 | ✅ recomputed from `i·n + j` |
| §12.3: `temp`/float32/`0x7FC00000` = 12 bytes `04 74 65 6D 70 0C 00 04 00 00 C0 7F` | §12.3 | ✅ |
| §4.6: `température` NFC 12 bytes, NFD 13 | §4.6 | ✅ |
| §12.1: bfloat16 1.0 = `0x3F80` → `80 3F`; `0x7FC0` qNaN | §12.1 | ✅ |
| §20.3: 32-tile index re-emit = 32·20+4 = 644 | §20.3 | ✅ |
| §21.9 note: 2³² entries → 256 KiB CRC array; 2³⁶ → 4 MiB | §21.9 | ✅ |
| §21.2/3/4/5 headers: 36 / 49 / 26 / 10 conditions | §21 | ✅ (36+49+26+10 = 121) |
| §21.8: "121 conditions over 248 instances" | §21.8 | ✅ mechanical count of the Instances column (`—` = 1, semicolon-separated otherwise) gives F 53, L 106, T 45, R 44 = **248** |
| Appendix B "Reader minimum guarantees" vs §21.9's eight rows | App. B | ✅ all eight agree |

**Requirement identifiers.** Extracted every `` `[R-XXX-NN]` `` in the document:
20 prefixes, no numeric gaps anywhere (`R-ENC-100` is §2.2's illustrative
example; `R-SER-04` is present only in §14.4's withdrawal note, exactly as §2.2
prescribes). No identifier is referenced that is never defined.

**Register cross-references.** The brief warned that §21.2/§21.3 had been
wholesale re-labelled, so every row citation from anywhere in the document is
newly suspect. I extracted all of them mechanically and checked each against the
row it lands on:

| Where | Cites | Lands on | Verdict |
|---|---|---|---|
| §9.6 | F8, F17 | trailer magic at F−64; cfl ≠ transport size | ✅ both are what a torn tail fails |
| §17.2 deflate note | T24 | "decode does not consume the entry's length exactly" | ✅ |
| §21.1 specializations | F1 of F6 and F8 | F1 = byte-reversed constant (2 instances); F6 = front block ≠ constant; F8 = 8 bytes at F−64 ≠ magic | ✅ F1's two instances are exactly specializations of F6 and F8 |
| §21.1 | F35 of F36 | F35 = reserved-range top-level type with MU=1 (reader/open); F36 = reserved-range type whatever the MU bit (verifier/certification) | ✅ strict specialization |
| §21.1 | L24 of L25 | same shape at sub-record scope | ✅ |
| §21.1 | T24's *any codec*; (T15, T25) | T24 one instance; T15 two (zlib, gzip); T25 three (deflate, zstd, lz4) | ✅ illustrates the single-vs-enumerated rule correctly |
| §21.2 F33 | F9/F10, F31/F32, L16/L17, T8/T9 | dir_offset<16 / dir end past F−64; record extent_offset 1–15 / extent past F−64; layer-or-sub-record extent_offset<16 / past F−64; entry offset<16 / entry end past F−64 | ✅ all eight are exactly the front-block and trailer bounds rows at their four tiers |
| §21.4 T2 | T4 | padding position ≠ fill | ✅ partitions `[R-SER-08]`'s byte between real and padding positions |
| §21.4 T13 | T25 | malformed stream fails to decode | ✅ |
| §21.4 T26 | T2, T4 | ✅ |
| §21.5 R4 | R3 | "stored bytes fail to decode" | ✅ the contrast is right |
| §21.6 | F36, L25; F18; F35, F36, L24, L25 | ✅ each resolves to the reserved-range or version_major=0 row named |
| App. H | F7; F36, L25 | F7 = structure between directory end and trailer | ✅ |

**Every row citation in the document resolves to the row its surrounding
sentence claims.** That is a meaningful negative result: the re-labelling was
carried through consistently. I found no dangling or misdirected row label.

---

## 2. Creation — the byte layout, emitted in order

I built a file with two layers, both edge-padded, one interleaved with a mixed
sample type, one planar bool with packed bits and a slab declaration, both
kinds of user-metadata record, and one sentinel tile. Every number below came
out of `wtr/build.py`; the whole file is 1,088 bytes.

### 2.1 The layers I declared

**Layer `sst`** — interleaved (layout 1), rank 2, dimensions `y`(E=5, T=4) and
`x`(E=5, T=4); channels `t` (float32, fill `00 00 00 00`) and `m` (bool, fill
`01`). linearization 1, codec 1 (none), filter 1 (none), A=0, S=0, A_slab=0.

Derived, all from `[R-GEO-03]` and `[R-SER-02]`:
G = (⌈5/4⌉, ⌈5/4⌉) = (2,2); N = 4; P = 16; addressed = N = 4 (interleaved);
Q = 4 + 1 = 5; decoded size = P·Q = **80 bytes**; F⁰ = 0, F¹ = 4.
Index region = 4·20 + ⌈4/2¹⁶⌉·4 = 80 + 4 = **84 bytes** (`[R-CNT-17]`).

Every tile is 80 bytes, so codec 1's `[R-COD-04]` equality holds by construction.
Tiles 1 and 2 are edge tiles (12 padding positions each); tile 3 covers
coordinates 4–7 on both axes, so it has one real position (4,4) and 15 padding
ones. I chose the input array so (4,4) equals fill (0.0, true), which makes tile
3 wholly fill and lets me sentinel it. **The document forced this check on me:**
had (4,4) carried 44.0, sentinelling tile 3 would have silently changed the
reference array, because `[R-TYP-08]` makes a sentinel read as fill at *every*
position the tile carries, and §3.2 makes the reference array the conformance
target. Nothing warns a writer about this directly; §13.3's rules make it
derivable, and Appendix G item 6 ("The sentinel for every all-fill tile")
approaches it from the reproducibility side. I did not treat it as a defect.

**Layer `mask`** — planar (layout 2), rank 2, `y`(E=5, T=3), `x`(E=5, T=3);
one bool channel `b`, fill `00`. codec 1, filter 1, A=0, **S=2, A_slab=64**.
G = (2,2); N = 4; P = 9; addressed = C·N = 4; packed plane = ⌈9/8⌉ = **2 bytes**
(`[R-SER-03]`). P mod 8 = 1, so bits 1–7 of byte 1 are pad bits and must carry the
channel's fill bit, which is 0 (`[R-SER-05]`). Index region 84 bytes.

Slab runs, per `[R-SLB-02]`: the single channel block is [0,4); with S=2 the runs
are ordinals [0,2) and [2,4). Each run's first stored tile must satisfy
offset mod 64 = 0, and each run's stored tiles must be packed.

### 2.2 Emission order and offsets

`[R-LIF-02]`'s creation path: front block first, then steps 2–6 beginning at
offset 16, generation 1.

```
[    0,   16)   16  front signature block   89 54 41 52 4E 0D 0A 1A + 8 zero bytes
[   16,   96)   80  sst tile 0   (s=0, all 16 positions real)
[   96,  176)   80  sst tile 1   (s=1, 4 real + 12 padding)
[  176,  256)   80  sst tile 2   (s=2, 4 real + 12 padding)
[  256,  340)   84  sst tile-index region  (4 entries + one 4-byte segment CRC)
[  340,  384)   44  SLACK  — forced by mask's A_slab = 64
[  384,  386)    2  mask tile 0   run 0 first stored tile, 384 mod 64 = 0
[  386,  388)    2  mask tile 1   packed: 384 + 2 = 386
[  388,  448)   60  SLACK  — forced by A_slab on run 1
[  448,  450)    2  mask tile 2   run 1 first stored tile, 448 mod 64 = 0
[  450,  452)    2  mask tile 3   packed
[  452,  536)   84  mask tile-index region
[  536,  637)  101  file-scope user-metadata extent (97-byte JSON + 4-byte CRC)
[  637,  681)   44  sst layer user-metadata extent (40-byte JSON + 4-byte CRC)
[  681,  979)  298  directory region (3 records + 4-byte CRC)
[  979, 1024)   45  pre-trailer pad
[ 1024, 1088)   64  trailer
F = 1088, F mod 64 = 0
```

Bytes, verbatim, of the structures where the document is most load-bearing:

```
front  0000  89 54 41 52 4e 0d 0a 1a 00 00 00 00 00 00 00 00

sst index region [256,340)
 0100  10 00 00 00 00 00 00 00 50 00 00 00 00 00 00 00   entry 0: off 16, len 80
 0110  e9 44 22 61                                        entry 0: crc
       60 00 00 00 00 00 00 00 50 00 00 00 00 00 00 00   entry 1: off 96, len 80
 0120  1e 45 9d 46                                        entry 1: crc
       b0 00 00 00 00 00 00 00 50 00 00 00 00 00 00 00   entry 2: off 176, len 80
 0130  d0 17 f8 3a                                        entry 2: crc
       ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
 0140  00 00 00 00                                        entry 3: the sentinel
       c0 ad 02 9e                                        segment 0 CRC

trailer [1024,1088)
 0400  8a 4e 52 41 54 0d 0a 1a   magic
       01 00                     version_major = 1
       00 00                     version_minor = 0        (R-CNT-26 floor)
       00 00 00 00               flags = 0                (R-CNT-08, MUST)
 0410  01 00 00 00 00 00 00 00   generation = 1
       a9 02 00 00 00 00 00 00   dir_offset  = 681
 0420  2a 01 00 00 00 00 00 00   dir_length  = 298
       40 04 00 00 00 00 00 00   committed_file_length = 1088
 0430  34 12 0d ee ff c0 17 5a   file_id (nonzero, random per §9.3)
       00 00 00 00               reserved
       4c 2c ee 41               CRC-32C over [0,60)
```

The `sst` layer record: header `01 00 03 00 7f 00 00 00 | 00 01 00 00 00 00 00 00 |
54 00 00 00 00 00 00 00` — type 0x0001, flags 0b11 (MU=1, PE=1, exactly as
§7.3's registry table fixes them), inline_length 127, extent slot (256, 84).
The 127-byte inline payload packs, with no padding between fields
(`[R-CNT-18]`):

```
03 73 73 74            name "sst"
01                     layout = 1 interleaved
01 00                  linearization = 1
01 00                  codec = 1
01 00                  filter = 1
00×8 00×8 00×8         A = 0, S = 0, A_slab = 0
02                     rank d = 2
02 00                  channel count C = 2
01 79 | 05×8 | 04×8    dim "y": E=5, T=4
01 78 | 05×8 | 04×8    dim "x": E=5, T=4
01 74 0c 00 04 00 00 00 00    channel "t": float32, fill len 4, +0.0f
01 6d 01 00 01 01             channel "m": bool,    fill len 1, 0x01
01                     index_encoding = 1
04 00 00 00 00 00 00 00       entry_count = 4
37 2a 59 c1            crc_of_crc_array
02 00 02 00 01 00 00 00 7d 02 ... one user-metadata sub-record (24+1 bytes)
```

Sizes hand-checked against `[R-CNT-18]`: 4+1+2+2+2+8+8+8+1+2 = 38 fixed; two
18-byte dimension entries = 36 → 74; channel entries 9 + 6 = 15 → 89; trailing
1+8+4 = 13 → 102; sub-record 25 → **127**, no residue.

### 2.3 What the document fixed and what it left to me

| Decision | Fixed? | Where |
|---|---|---|
| Front block content and position | **Fixed** | §6.1, MUST emit exactly those 16 bytes |
| First writable offset on creation | **Fixed** at 16 | `[R-LIF-02]` creation path |
| Order: payloads → index regions → record extents → directory → pad → trailer | **Fixed** at that granularity | `[R-LIF-02]` steps 2,3,5 |
| Order *within* step 2 (tiles vs indexes vs extents, and across layers) | **Free** | `[R-LIF-02]` "in any order"; `[R-SLB-05]` |
| Placement of any structure, absent A or S | **Free** | `[R-SLB-05]` |
| Tile extents Tᵢ | **Free** (guidance only) | §11.3 note, 1–16 MiB "guidance" |
| Layout, codec, filter | **Free** (caller's) | §7.4 value sets constrain, not choose |
| Whether to declare A or S at all | **Free** | §16 |
| Aligned/slab placement once declared | **Fixed** | `[R-SLB-01]`, `[R-SLB-03]` |
| Content of alignment/slab gaps | **Free**, SHOULD zero | `[R-CNT-03]` |
| Padding-position content | **Fixed** = fill | `[R-SER-05]` |
| Pad-bit content in a packed plane | **Fixed** = fill bit | `[R-SER-05]` |
| Sentinel vs stored for an all-fill tile | **Free** | §13.3 note; App. G item 6 |
| Fill when the caller chooses none | **Free**, SHOULD all-zero | `[R-TYP-10]` |
| Segment CRC for a full all-sentinel segment | **Fixed** value, computation optional | `[R-IDX-05]` |
| Segment CRC for a *partial* segment | **Fixed**, MUST compute | `[R-IDX-05]` — my 4-entry segment is partial, so the `0xEECB3BB2` shortcut is barred even though 1 of the 4 entries is a sentinel |
| Record order in the directory | **Free** | `[R-CNT-14]` |
| Sub-record order in a layer record | **Free** | `[R-CNT-14]`; App. G names it |
| `flags` | **Fixed** = 0 for a creator | `[R-CNT-08]` |
| `version_minor` | SHOULD = 0 | `[R-CNT-26]` |
| `file_id` | **Free**, nonzero, SHOULD be random | `[R-LIF-03]` |
| `generation` | **Fixed** = 1 | `[R-LIF-02]` |
| Pre-trailer pad **length** | **Fixed**: pad to the next 64-byte boundary | `[R-LIF-02]` step 5 |
| Pre-trailer pad **content** | **Free**, SHOULD zero | §6.2, `[R-CNT-03]` |
| Both barriers | **Fixed** | `[R-LIF-02]` steps 4 and 6; `[R-WRT-02]` insists "both barriers, not one" |
| JSON member order | **Fixed** ascending by keys' UTF-8 bytes | `[R-MTA-05]` |
| JSON whitespace, escaping, number formatting | **Free** | §18.2's note says so explicitly |
| Metadata storage encoding (1 vs 2) | **Free** | §18.2 |

**Places where I had to re-read before I could emit a byte:**

- §6.2's pre-trailer pad. Two sentences bound it from opposite sides: "a longer
  gap is conforming, and no conforming commit produces one." So the *file*
  predicate admits a 128-byte pad while `[R-LIF-02]` step 5 bars my writing one.
  I emitted 45. This is the same shape as §2.3's flags = 0 carve-out (a writer
  obligation that is not a file-conformance violation) but is not named there;
  the em-dash in §2.3 reads as illustrative rather than exhaustive, so I did not
  treat it as a defect. No fork: minimal padding is mandatory for me either way.
- `[R-CNT-17]`'s formula at entry_count = 0. `0·20 + ⌈0/2¹⁶⌉·4 = 0`, so the
  parenthetical "(and 0 when entry_count is 0)" is a restatement, not an
  override. Confirmed arithmetically.
- Whether a *partial* all-sentinel segment may use `0xEECB3BB2`. §15.4 says
  "one covering exactly 2¹⁶ entries, final or not" and "a partial segment's CRC
  MUST be computed". Unambiguous once found.
- `[R-CNT-23]`'s fill-length cross-check: the u8 length prefix lets me *parse*
  the fill without knowing the type and *validate* it with the type. That is
  what makes my layer-record parser a single forward pass. Stated outright.

### 2.4 The file reads back

`wtr/read.py` is a reader written from §19.1/§19.3/§19.4 alone, sharing no code
with the builder. It performs §6.2's validation order, verifies the directory
CRC, builds the layer-name namespace, does §19.3's layer validation, walks the
index chain (`crc_of_crc_array` → segment CRC → entry → payload CRC), and
extracts by §14.2/§14.3's offset arithmetic. Both reference arrays round-trip
exactly, including the sentinel tile reading as (+0.0, true) at (4,4), and the
slab invariants L41/L42 check clean:

```
sst   0.0/1s   1.0/0s   2.0/1s   3.0/0s   4.0/1s
     10.0/0s  11.0/1s  12.0/0s  13.0/1s  14.0/0s
     20.0/1s  21.0/0s  22.0/1s  23.0/0s  24.0/1s
     30.0/0s  31.0/1s  32.0/0s  33.0/1s  34.0/0s
     40.0/1s  41.0/0s  42.0/1s  43.0/0s   0.0/1F     ← F = from the sentinel
mask [1,0,0,1,0] [0,1,0,0,1] [0,0,1,0,0] [1,0,0,1,0] [0,1,0,0,1]
```

**Creation is fully determined by the document.** I did not have to guess once.

---

## 3. The append procedure

### 3.1 Generation 2 — adding a layer (§20.3 shape (a))

Layer `aux`: interleaved, rank 1, `x`(E=3, T=2) → G=2, N=2, P=2; one uint16
channel `v`, fill `00 00`; Q=2, decoded size 4. Tile 1 covers x=2 (real) and
x=3 (padding, encoded as fill per `[R-SER-05]`). entry_count = 2, index region
2·20+4 = 44.

`[R-WRT-04]`'s six steps, run in order:

1. **Establish F.** Validate the trailer at the physical end: F = 1088.
2. **Open** — §19.1, the appender acting as a reader.
3. **Validate what the commit touches** (`[R-WRT-03]`): the trailer and the
   *full directory* always, because re-emission relies on every directory byte;
   plus §19.3's layer validation for layers I modify. I modify none: `sst` and
   `mask` are carried byte-identically. I do not touch either layer's index
   chain, so `[R-IDX-04]`'s verification is not owed for them.
4. **Write payloads and index** starting at exactly F = 1088:
   `aux` tile 0 at 1088 (4 B), tile 1 at 1092 (4 B), `aux` index at 1096 (44 B).
5. **Re-emit the directory** at 1140, length 398: `sst`'s 151 bytes and `mask`'s
   118 bytes copied verbatim out of generation 1's directory, `aux`'s new 100
   bytes, then the file-scope metadata record's 25 bytes verbatim, then the CRC.
6. **Commit**: barrier; pad 62 bytes to 1600; trailer with generation 2, the
   same file_id, flags carried forward (0), version_minor = max(floor, prior) = 0;
   barrier. **F = 1664**, 576 bytes appended.

Nothing in [0,1088) changed. `sst`'s record still addresses its original index
region at 256 — `[R-WRT-05]`: "A layer whose record alone changes keeps its
extent slot"; a layer untouched keeps it a fortiori, and §5.1 adds "A commit
never relocates a live index region otherwise; that is compaction's operation."

### 3.2 Generation 3 — superseding a tile (§20.3 shape (b))

Supersede `sst` tile 1. Appended at F = 1664: the new 80-byte payload at 1664;
**`sst`'s entire index region re-emitted** at 1744 (all four entries — one
re-pointed, two byte-identical, one still the sentinel — plus a recomputed
segment CRC); a new directory at 1828 in which `sst`'s record differs from
generation 2's in exactly two places, its extent slot (1744, 84) and its
`crc_of_crc_array`; 14 bytes of pad; trailer generation 3. F = 2304, 640 bytes
appended to change 80 bytes of data.

The index cost dominates exactly as §20.3's note predicts. What became slack:
the old payload [96,176) = 80 B, the old index region [256,340) = 84 B, and
generation 2's directory + pad + trailer [1140,1664) = 524 B.

### 3.3 Adding to a file whose records I do not all understand

The flag field is `u16`: bit 0 MU, bit 1 PE, bits 2–15 reserved. The complete
matrix my updater must handle, with the rule that decides each cell:

| Position | Type | Stored (MU,PE) | What my updater is permitted to do |
|---|---|---|---|
| top-level | 0x0001 / 0x0002 (registered) | any | The **registry's** flags govern, not the stored ones (`[R-CNT-22]`, §20.4). Both are PE=1, so **retain, byte-identical** (`[R-WRT-05]`). A stored mismatch is F28/L49 — nonconforming, verifier-detected, and I re-emit the wrong bits unchanged; §20.5's "nor re-emit it corrected (`[R-WRT-05]`)" confirms correction is barred. |
| top-level | unknown | (1,·) | **Refuse the whole file.** `[R-CNT-15]` makes an unimplemented top-level MU=1 record reject-file; §20.4: "At file scope no commit is available at all." I am a reader before I am a writer. |
| top-level | unknown | (0,1) | **Retain byte-identical, extent content unmodified.** I may not relocate the extent: `[R-WRT-08]` allows relocation "only … under §20.5", i.e. compaction. |
| top-level | unknown | (0,0) | Retain, **or drop** — but only in a commit that independently changes "the file's layer set or another *non-layer* top-level record". Adding `aux` (gen 2) qualifies; superseding `sst` tile 1 (gen 3) does not. Dropping is never itself the qualifying change. SHOULD report the loss. |
| sub-record | 0x0002 (registered) | any | PE=1 by registry → **retain**. (§20.4's summary sentence names only "a layer record or a file-scope user-metadata record", but the general rule two sentences earlier — "both registered types carry PE = 1, so neither can be dropped" — forecloses dropping a layer's metadata sub-record too.) |
| sub-record | unknown | (1,·) | **Retain byte-identical and do not modify that layer at all.** Other layers stay editable (`[R-CNT-18]`). Note the layer is also reject-layer for me *as a reader*, so I cannot validate or re-index it; retaining the whole layer record verbatim is the only move. |
| sub-record | unknown | (0,1) | Retain byte-identical, extent unmodified. |
| sub-record | unknown | (0,0) | Retain, **or drop** — under the same "independently changes" test, which is where the text forks (finding **writer-01**). |
| either | any | reserved bits 2–15 nonzero | Readers MUST ignore; a verifier records F26/L47. I re-emit them byte-identically, because `[R-WRT-05]` is unconditional and §20.4 says nothing about normalising them. |
| either | MU=1 with PE=0 | — | Read as PE=1, never silently deletable (`[R-CNT-12]`). Verifier records F25/L46. |

**Write order and durability, from `[R-LIF-02]`:** everything at step 2 and the
directory at step 3 must be durable *before* the pad and trailer of step 5 are
written (step 4's barrier), and the trailer must itself be durable (step 6). The
**commit point is the trailer's durability** — until step 6, a reader that
happens to see the new trailer without the directory behind it is looking at a
file that fails the directory CRC (F20), which is loud, not silent.

Two writer obligations I nearly missed:
- `[R-SLB-04]`: a commit that supersedes a stored tile in, or grows the extents
  of, a slab-declared layer must re-establish the run invariants **or clear the
  declaration**. If gen 3 had superseded a `mask` tile, my new payload appended
  at F would break run packing, and I would have had to either re-pack the whole
  affected run at the append point or write S = A_slab = 0 into the new layer
  record.
- §20.3's example (c): changing a channel's fill on a layer that has any padding
  position or pad bit forces re-emission of the affected stored tiles, because
  `[R-SER-05]` fixes their content in terms of the fill. My `sst` has 39 padding
  positions, so a fill change there is a shape-(b) commit, not a shape-(c) one.

---

## 4. Slack — who owns which bytes, per commit shape

Coverage is a property of the **live committed state** only (`[R-CNT-02]`,
`[R-LIF-08]`): the front block, plus everything reachable from the live trailer
through the live directory's records, extent slots and non-sentinel index
entries, plus the directory and the live trailer. Everything else is slack, its
content unconstrained, counted but never certified.

| Commit shape | Bytes that become slack | Counted by | Permitted content |
|---|---|---|---|
| **Creation** | alignment/slab gaps; the pre-trailer pad | verifier (§9.7 walk) | anything; SHOULD be zero (`[R-CNT-03]`) |
| **Append, new layer** (gen 2) | the prior generation's directory, pad and trailer — 407 B here, sized by the file's *layer count*, never by any layer's data — plus the new pad | verifier | anything |
| **Append, superseding tiles** (gen 3) | the superseded payloads (80 B), the layer's *whole* prior index region (84 B), the prior directory+pad+trailer (524 B), the new pad | verifier | anything |
| **In-place update** | does not exist. `[R-LIF-01]`: bytes in [0,F) are immutable; every mutation is a commit or a whole-file rewrite | — | — |
| **Directory-only change** (shape (c)) | the prior directory, pad and trailer only | verifier | anything |
| **Rewrite / compaction** | nothing carried; the *output's* own slack is its alignment gaps and its pre-trailer pad. The input file persists untouched (`[R-PRV-02]`) | verifier, on the output | anything |
| **Abandoned partial write** | **none, by definition.** The partial bytes lie at or past F and are not part of any live committed state; the file's live state is still generation n. `[R-LIF-04]` obliges the next writer to truncate them or overwrite them. §9.5's note is explicit that residue carries no register row of its own — a reader meets it as F8/F14/F17 | nobody: a verifier's walk is of the *live* state of the file as handed over, and a file with residue fails `[R-CNT-06]` before any walk begins | anything |

Live-state walk of my generation-3 file (`[R-LIF-08]`), verifier's view:

```
[    0,   16)   16  front signature block
[   16,   96)   80  sst tile 0
[   96,  176)   80  SLACK   (superseded payload)
[  176,  256)   80  sst tile 2
[  256,  384)  128  SLACK   (superseded index region 84 + alignment gap 44)
[  384,  388)    4  mask tiles 0,1
[  388,  448)   60  SLACK   (A_slab gap)
[  448,  452)    4  mask tiles 2,3
[  452,  536)   84  mask index region
[  536,  637)  101  file-scope metadata extent
[  637,  681)   44  sst metadata extent
[  681, 1088)  407  SLACK   (gen-1 directory + pad + trailer)
[ 1088, 1096)    8  aux tiles 0,1
[ 1096, 1140)   44  aux index region
[ 1140, 1664)  524  SLACK   (gen-2 directory + pad + trailer)
[ 1664, 1744)   80  sst tile 1 (new)
[ 1744, 1828)   84  sst index region (new)
[ 1828, 2226)  398  directory
[ 2226, 2240)   14  SLACK   (pre-trailer pad)
[ 2240, 2304)   64  trailer
                    slack total = 1,213 of 2,304 = 52.6%
```

Three generations on a toy file and the majority of it is already slack. §20.3's
note and §20.5's example both say exactly this, and the verifier's slack total
is the number that tells an operator to compact.

Two things I checked because they decide who counts what:
- **A prior generation's trailer is slack**, even though §5.1's prose lists
  "each prior generation's trailer" alongside the structures commits appended.
  §5.2 scopes coverage to what the *live* trailer reaches, and §20.5's figure
  hatches `dir₁…tr₁` as slack. Determined.
- **An index entry §15.3 classifies reject-tile on a *structural* ground
  contributes no extent to the walk**, so the bytes it nominally addressed fall
  to slack — but an entry whose only defect is that its stored bytes fail its crc
  *keeps* its extent, in the walk, in overlap checks, and in slab run continuity.
  §9.7 and §15.3 state this three times over. This is the sharpest edge in the
  whole coverage story and the document nails it.

---

## 5. Torn-write recovery

Seven crash points against the generation-2 commit, run through my reader and a
§9.6 probe (`wtr/torn.py`). In every case the last committed state is generation
1 at F = 1088 unless noted.

| Crash point | Physical size | What the next reader sees | What the next updater does | Conforming meanwhile? |
|---|---|---|---|---|
| **C1** mid-payload (2 of 8 `aux` payload bytes) | 1090 | reject-file, **F8** — the 8 bytes at F−64 are not the trailer magic; `[R-LIF-05]` forbids scanning back | `[R-LIF-04]`/§20.3 step 1: file is torn, **MUST NOT append**. Recovery (§9.6) is a separate deliberate operation. Probe settles on o=1024, generation 1, 0 candidates rejected | **No.** Physical size ≠ any trailer's committed_file_length |
| **C2** payloads and index written, no directory | 1140 | reject-file, F8 | same; probe → o=1024, gen 1 | No |
| **C3** directory written and barriered, no pad/trailer | 1538 | reject-file, F8 | same; probe → o=1024, gen 1. This is the window §9.2's figure draws: trail₁ intact but no longer at the file's end | No |
| **C4** pad written, trailer half written | 1632 | reject-file, F8 (bytes at 1568 are pad zeros) | same; probe begins at the largest 64-aligned o with o+64 ≤ 1632, i.e. o=1568, walks down, settles on o=1024 | No |
| **C5** trailer fully written, final barrier not yet issued | 1664 | **OPEN OK, generation 2** | Nothing to recover: if every byte landed, the commit is complete. Step 6's barrier orders against *later* power loss, it is not the commit point for bytes already on the medium | **Yes** |
| **C6** weak barrier: the trailer landed but the directory did not | 1664 | trailer passes every §6.2 gate, then **F20** — the directory CRC fails. Detection is loud, exactly as §9.2's note promises | Torn. Probe finds o=1600 (magic ✓, CRC ✓, cfl = o+64 ✓), whole-file re-verification **fails**, so it "continues the probe past it" and settles on o=1024, **reporting 1 candidate rejected** (`[R-LIF-06]`) | No |
| **C7** completed commit plus 128 bytes of residue | 1792 | reject-file, F8 | `[R-LIF-04]`: truncate to F or overwrite from F and truncate by step 6. Probe settles on o=1600, generation 2 | No — §9.5's note: what the residue violates is `[R-LIF-04]`, and the observable state is already named by F8/F14/F17 |

Every case behaved as the document predicts. The chain of trust catches C6
without any special machinery, and the "recoverable, not readable" framing in
§9.2's example turned out to be exactly right: in C1–C4 generation 1 is
byte-intact and unreachable by a conforming reader, and one truncation restores
it.

One chain I had to assemble across three rules: an appender resuming from
recovery output that was *not* truncated. §20.3 step 1 says it "takes F from
that output, then truncates to F or overwrites from it per `[R-LIF-04]` — in
which case F, never the physical end, anchors every step below." That last
clause is what stops §19.1 step 1's "transport-authoritative file size" from
being used, which would otherwise trip `[R-CNT-06]`'s cfl-equals-size gate on a
file the appender is about to shorten. `[R-CNT-10]`'s prohibition on
substituting committed_file_length for the transport size binds a *remote
reader*, not this case. Determined, but only after reading three rules together.

---

## 6. Byte-divergence catalogue

Given identical input arrays and identical stated options, here is every way I
found for two conforming writers to differ, and whether Appendix G closes it.

| # | Degree of freedom | Governing text | Closed by App. G? |
|---|---|---|---|
| 1 | Placement of every structure (absent A/S) | `[R-SLB-05]`, `[R-LIF-02]` step 2 | **Yes** — item 3's total order, contiguously |
| 2 | Order of tiles/indexes/extents within step 2 | `[R-LIF-02]` "in any order" | **Yes** — item 3 |
| 3 | Order of records in the directory | `[R-CNT-14]` | **Yes** — item 3 (by type; type 0x0001 by layer name; at most one 0x0002 top-level so no tie) |
| 4 | Order of sub-records in a layer record | `[R-CNT-14]` | **Yes** — item 3, "by type, and within a type by their encoded bytes compared lexicographically". Named in the closing paragraph |
| 5 | Content of alignment/slab gaps | `[R-CNT-03]` SHOULD | **Yes** for alignment-forced gaps — item 3 |
| 6 | **Content of the pre-trailer pad** | §6.2, `[R-CNT-03]` | **Ambiguous** → finding **writer-02** |
| 7 | **Where record extents sit relative to the per-layer loop, and where a sub-record extent sits relative to a top-level one** | — | **Ambiguous** → finding **writer-07** |
| 8 | Extent of gaps (how much space between structures) | `[R-SLB-05]` | **Yes** — item 3 + item 5 |
| 9 | Whether A or S is declared, and their values | §16 | **Yes** — item 5 |
| 10 | `file_id` | `[R-LIF-03]` (nonzero, SHOULD random) | **Yes** — item 2, hash of [0,F−64) plus the trailer's other fields with `file_id` zeroed |
| 11 | `generation` / number of commits | `[R-LIF-02]` | **Yes** — item 4, one generation |
| 12 | `version_minor`, `flags` | `[R-CNT-26]`, `[R-CNT-08]` | **Yes** — item 8 |
| 13 | Codec choice | §17.2 | Stipulated as a caller option (item 2's rationale: "two files carrying the same arrays can legitimately differ in tiling, layout, and codec") |
| 14 | Encoder output for codecs 2–4 at a fixed choice | `[R-CNF-05]` | **Yes** — item 1, named implementation, version, settings, thread count |
| 15 | DEFLATE's up-to-seven unused final-bit values | §17.2's note | **Yes** — item 1, and §17.2 says so itself |
| 16 | Tiling and layout | §11.3 note, §14.1 | Stipulated as caller options (item 2's rationale) |
| 17 | Sentinel vs. stored for an all-fill tile | §13.3 | **Yes** — item 6 |
| 18 | Fill recorded when the caller chooses none | `[R-TYP-10]` SHOULD | **Yes** — item 7, which correctly notes it reaches further than eight bytes, because item 6 makes the fill decide *which tiles exist* |
| 19 | JSON whitespace / escaping / number formatting | §18.2's note | **Yes** — item 9, named JSON writer at a named version |
| 20 | **Metadata storage encoding (1 = none vs 2 = zstd), and the zstd producer if 2** | §18.2 | **No** → finding **writer-03** |
| 21 | Segment CRC for a full all-sentinel segment | `[R-IDX-05]` | No freedom: the licence is to skip the computation, and the constant *is* the computed value |
| 22 | Pre-trailer pad **length** | `[R-LIF-02]` step 5 | No freedom: mandatory minimum pad |
| 23 | Padding-position and pad-bit content | `[R-SER-05]` | No freedom, already mandatory; the closing paragraph correctly lists it among "everything else … already mandatory" |
| 24 | Trailer `reserved`, `crc_of_crc_array` at entry_count 0, extent slot at entry_count 0 | `[R-CNT-06]`, `[R-CNT-23]`, L22 | No freedom |

**The profile's own summary claim.** Its closing paragraph names four things the
items add: gap *content*, gap *extent*, sub-record order, and the default fill.
Rows 4, 5, 8 and 18 confirm three of those and half of the first. Row 6 shows
the "gap content" claim does not reach the pre-trailer pad under item 3's literal
wording, and row 20 shows the profile's coverage of user metadata stops one step
short of bytes. Neither changes any conformance verdict — Appendix G "adds no
requirement to any actor" — but both falsify the appendix's opening claim to
close "the degrees of freedom this format deliberately leaves open" for a writer
that follows it literally.

I could not classify no divergence: everything in the table above is either
legitimate-and-closed, legitimate-and-open (writer-02, -03, -07), or forbidden.

---

## 7. Findings

### writer-01 — AMBIGUITY — §20.4, `[R-WRT-08]`'s preservation table, MU=0/PE=0 row

> An appender may drop it only in a commit that *independently* changes the
> scope the record attaches to: for a layer sub-record, that layer's record,
> index, or stored tiles; for a top-level record, the file's layer set or
> another *non-layer* top-level record — a commit that only supersedes a
> layer's tiles is not such a change, though it re-places that layer's index
> region (§20.3, `[R-WRT-04]`).

The trailing clause after the second semicolon can attach to the top-level
branch alone or to the whole list, and the two attachments give different bytes.

**Reading A (clause qualifies the top-level branch only).** Superseding a
layer's tiles is not a change to "the file's layer set", so it does not license
dropping a *top-level* MU=0/PE=0 record; the "though it re-places that layer's
index region" concession heads off the argument that a large byte movement is a
structural change to the file. Under A, the *sub-record* branch is untouched:
superseding tiles changes "that layer's … index, or stored tiles", so an
appender **may** drop that layer's unknown MU=0/PE=0 sub-record.

**Reading B (clause qualifies the whole list).** Superseding tiles is never
"such a change". The sub-record branch survives only if "index" and "stored
tiles" are read as changes to the *set* of stored tiles — adding tiles, growing
extents, unstoring tiles — and not as superseding an existing tile's bytes.
§20.3 step 4 does distinguish these ("tiles this commit stores or supersedes",
"tiles that become unstored", "entries new to this generation"), so B is not
dead text. Under B an appender **must** retain that sub-record.

Each reading is bought at a price. A must place a dash-clause with a branch that
does not contain the word "index", when the clause's whole subject is the index
region — and the word "index" appears only in the sub-record branch, which is
what makes B's reading of the clause feel like the intended one. B must read
"stored tiles" as set-membership rather than content, which no other sentence in
§20 does.

**I picked A**, because the concession's phrasing — "is not such a change,
though it re-places that layer's index region" — is a concession about
*consequences* ("a lot of bytes moved") rather than about the criterion, and
because B requires re-reading two terms of the first branch against their plain
meaning while A requires only choosing an antecedent. I am not confident, and an
implementer who picks B is not being careless.

**Byte-level: yes.** Take a conforming file with layer `sst` carrying an unknown
experimental-range sub-record of type 0x8001, MU=0, PE=0, inline_length 0,
extent (E, n) — conforming per §21.6's experimental-MU=0 row. Instruct two
conforming appenders to supersede `sst` tile 1. Appender A emits generation 3
with `sst`'s layer record 24 bytes shorter (the sub-record dropped, its extent
falling to slack); appender B emits it with the sub-record intact. The directory
region differs in length by 24 bytes and in content from the first byte of the
sub-record onward; `dir_length` in the trailer differs; the trailer CRC differs;
the two files' slack totals differ by 24 + n. Both are conforming *files*, so no
reader's verdict forks — but exactly one of the two appenders is a conforming
updater, and which one is undetermined. The input is conforming and the
operation is the format's most routine commit, which is why I rate this
byte-level despite the fork living in updater conduct.

### writer-02 — AMBIGUITY — Appendix G item 3 vs. `[R-CNT-03]` and §6.2

> Each structure begins where the previous one ended, save where a declared
> alignment forces a gap, and every byte of such a gap is zero — `[R-CNT-03]`'s
> advice, taken as a requirement here

`[R-CNT-03]` names two gaps: "the run before an aligned tile or slab run, **and
the pre-trailer pad**." The profile's closing paragraph claims the items add
"gap *content*, which `[R-CNT-03]` only advises". But item 3's requirement is
scoped to "such a gap", whose antecedent is a gap "a **declared** alignment
forces" — and a declared alignment in this format is the layer record's A or
A_slab (§7.4, §16). The pre-trailer pad is forced by §6.2's 64-alignment of the
trailer and by `[R-LIF-02]` step 5, neither of which is a declared alignment.

Two readings. **Literal:** "declared alignment" = §7.4's A / A_slab, so the pad
is neither made contiguous nor zeroed by item 3, and its content stays free.
**Loose:** "declared alignment" covers any alignment this format states, so the
pad is such a gap and MUST be zero.

**I picked the loose reading**, because the literal one makes item 3's
contiguity sentence self-defeating: it demands "each structure begins where the
previous one ended", and the trailer never does, so under the literal reading
every profile file with a non-64-aligned directory end already violates item 3.
But the loose reading is a repair, not what the text says.

The exposure is concrete and worst under the profile's own recommended
configuration. Item 5's first branch is "No declared alignment and no slab" —
under which there are *zero* alignment-forced gaps, so the literal reading leaves
item 3's zeroing clause with no referent at all, while the pre-trailer pad is
still 0–63 bytes long. My generation-1 file has no declared alignment on `sst`
and a **45-byte pre-trailer pad** at [979,1024). Two writers following every one
of the nine items produce files differing in those 45 bytes; §5.2 makes both
conforming ("Slack has no internal structure this specification defines, its
content is unconstrained"), and byte-identity — the profile's entire purpose —
fails.

**Byte-level: no.** Appendix G is non-normative and states that it "adds no
requirement to any actor: a writer ignoring it is fully conforming". Both writers
are conforming with or without the repair, and no reader or verifier verdict on
either file changes. What is falsified is a claim in the reproducible-writer
material, not a conformance boundary.

### writer-03 — OBSERVATION — Appendix G item 9

> **User metadata either absent, or serialized by a named JSON writer at a
> named version.** `[R-MTA-05]`'s sorted keys make one writer's output
> reproducible but explicitly do not make two writers' output identical —
> number formatting varies by runtime — so this degree of freedom closes the
> same way item 1 does, by pinning the producer.

Item 9 pins the JSON *serializer* and stops there. §18.2 gives a user-metadata
record two assigned storage encodings — `1 = none` and `2 = zstd` — and the
choice between them is a writer's. Item 1's producer-pinning covers "a named
codec implementation": §10.2's table makes "codec (§17.2)" and "metadata
encoding (§18.2)" separate identifier spaces, so item 1 does not reach §18.2.

Consequently two writers that follow every item of the profile, hold the same
JSON document, and use the same named JSON writer still diverge in two ways:
one may store the document verbatim under encoding 1 while the other compresses
it under encoding 2 (different extent length, different extent bytes, different
extent CRC, different `extent_length` in the record, and a different
`inline` encoding byte); and if both choose encoding 2, nothing pins the zstd
producer, so item 1's own argument — "two conforming encoders emit different,
equally valid streams for the same input" — applies unclosed.

I classify this OBSERVATION rather than AMBIGUITY because the text is not
ambiguous: it simply does not address the encoding, and the omission is decidable
by reading §18.2 and §10.2 together. It is reportable because item 9's own
sentence claims to close "this degree of freedom … the same way item 1 does",
and item 1's way is to pin *every* producer of the bytes.

**Byte-level: no**, for the same reason as writer-02: the appendix imposes no
requirement, and no conformance verdict moves.

### writer-04 — AMBIGUITY — §4.7 `[R-ENC-16]` vs. §6.2's trailer table

§4.7 defines a total trichotomy, "each class being what the one before it is not":

> A field is **structural** if its value determines how any byte is located or
> decoded; **semantic** if not, but its value determines what decoded values
> mean; and **descriptive** if neither — its value determines nothing a
> conforming reader does, and a reader MUST NOT alter decoding based on it.
> Each descriptive field's definition states what a reader does when the field
> contradicts the data it describes.

§6.2's trailer table classifies:

> | 48 | 8 | u64 | file_id | semantic | ≠ 0 |

and, on the row above it, `generation` as semantic. Neither field's value
determines what any decoded value means. Changing `file_id` from X to Y, or
`generation` from 3 to 47, alters no sample a reader returns from any layer:
§3.2's reference array is fixed by the trailer's `dir_offset`, the directory,
the indexes and the payloads, and `[R-TYP-04]` makes values bit patterns. §23.2
describes `file_id` only as "a stable 64-bit identifier". `version_minor` is the
document's sole field labelled *descriptive*, which is what made me check the
other two.

Three readings, none comfortable. **Descriptive:** the natural fit for
`file_id` — it determines nothing a reader is *obliged* to do — but then
`[R-ENC-16]`'s last sentence obliges §9.3 to state what a reader does when the
field contradicts the data it describes, and §9.3 states only the *consequence*
of a reused identifier ("lets two distinct files collide in the (file_id,
range)-keyed caches"), never a reader's behaviour; and for `generation` nothing
could be stated, since §21.7 records that `[R-LIF-03]` has no single-file
witness. **Structural:** arguable, because `[R-LIF-03]` lets a reader serve
bytes from a (file_id, range)-keyed cache, so the value decides which bytes a
reader ends up decoding — but that is cross-file cache identity, not location
within this file. **Semantic:** the table's label, which the definition does not
support.

**I picked descriptive** for both, and treated §9.3 and `[R-CNT-06]`'s gates as
discharging `[R-ENC-16]`'s last sentence as far as it can be discharged. This
changed nothing I emitted: I wrote generation 1 and a random nonzero `file_id`
either way.

**Byte-level: no.** The three classes carry exactly one operative consequence
between them — "a reader MUST NOT alter decoding based on it" for descriptive
fields — and that holds for `generation` and `file_id` under every reading, since
no rule anywhere lets decoding turn on either. The front matter's promise that
"Every field is classified as structural…, semantic…, or descriptive" is what is
at stake, not any byte.

### writer-05 — AMBIGUITY — §20.4, the flags-authority split

> Persistence governs every record type; only the authoritative source of the
> flags differs. For a type §7.3 registers, the registry's fixed flags govern
> rather than the stored ones (`[R-CNT-22]`) … For a type the updater does not
> implement, the stored flags are authoritative

The split is exhaustive over {registered} ∪ {not implemented} but the universe
is {registered} ∪ {implemented-but-unregistered} ∪ {not implemented}. The
uncovered cell is reachable: §21.6 records that an experimental-range record type
(≥ 0x8000) carrying MU=0 makes a **conforming** file, and an updater may perfectly
well implement its own experiment's type. §7.3's `[R-CNT-22]` closes one door —
"Stored flag bits are authoritative **only** for record types the consuming tool
does not implement" — without opening another, since §7.3's registry assigns
nothing in the experimental range and §10.2 gives that range no registry at all.

Readings. **(a)** The stored PE bit governs anyway, by analogy with the
not-implemented row: an updater may drop a stored-PE=0 experimental record it
implements. **(b)** No rule grants permission to drop it, and permissions in this
document are granted rather than assumed; `[R-WRT-05]`'s byte-identical
re-emission is the unconditional default and §20.4 says outright that
"implementing a record's type confers understanding of it, not permission to
drop it". So retain.

**I picked (b).** The quoted clause is the document's own general principle and
it points one way; and retention is never wrong, whereas an incorrect drop
destroys application state with, at best, a SHOULD-level report.

**Byte-level: no.** Reading (b) is available and is the one the document's stated
principle selects, so I do not think two competent implementations genuinely
fork here; and in the experimental case the updater is also the party that
defined the type's flags, so it has an out-of-band answer. I report it because
the charter asked me to walk *every* combination of record flags, and this is the
one combination the table's own preamble does not reach.

### writer-06 — AMBIGUITY — §20.5 `[R-WRT-06]` vs. §20.3, on carrying a detected violation

§20.5 tells a compactor exactly what to do:

> A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges fails,
> and MUST NOT emit a file carrying a violation it has detected: it can neither
> drop the structure (§20.4, `[R-WRT-07]`), nor re-emit it corrected
> (`[R-WRT-05]`), nor author bytes it knows to be nonconforming (`[R-CNF-05]`).

§20.3 tells an appender nothing of the kind, and the general clause that would
cover it is conditioned in a way that fails for directory records. `[R-WRT-01]`:

> a violation latent in a structure they neither modify **nor rely on** travels
> with it

but `[R-WRT-03]` states that an appender's verification depth includes

> the trailer and the full directory always — re-emission (§20.4) relies on
> every directory byte

So every record an appender re-emits is a structure it *relies on*, and
`[R-WRT-01]`'s escape does not reach it — while `[R-CNF-06]` still binds the
appender to "every writer requirement for the bytes it produces", including
`[R-CNF-05]`'s "emit only conforming files".

The case arises concretely. My appender is licensed by `[R-CNF-12]` to detect
more than it must; suppose while re-emitting it notices L49 on the `mask` layer
record (a stored PE bit differing from §7.3's registry — a verifier-detected,
reader-invisible violation) and the commit it was asked to perform only adds a
new layer. **Reading (x):** refuse, on the compactor's precedent and
`[R-CNF-05]`. **Reading (y):** proceed; the latent violation travels; "certifying
the whole file is a verifier's office (§9.7)", and an appender's obligations are
scoped to what it modifies.

**I picked (y)**, because §20.5's refusal is justified by `[R-WRT-09]`'s
compaction-specific verification depth — a compactor "relies structurally on
every structure it copies" and must verify each link — whereas `[R-WRT-03]` ties
an appender's depth to reliance and never obliges verifier-level checks. On that
reading the compactor refuses because it was obliged to look, and the appender
proceeds because it was not. But the text never says an appender proceeds, and
`[R-CNF-05]` is unconditional.

**Byte-level: no.** The fork is refuse-versus-proceed, and the proceeding
appender's output bytes are fully determined once it proceeds. The input is
already nonconforming, both candidate outputs' verdicts are already fixed by §21,
and §2.3 has already separated actor conduct from the byte predicate. I flag it
because an implementer must choose and the document gives the answer for one
writer tier and not the other.

### writer-07 — AMBIGUITY — Appendix G item 3, the emission order's loop scope

> **A total emission order, contiguously.** For each layer in ascending
> layer-name byte order: its stored tiles in disk-ordinal order, then its
> tile-index region; then any record extents in ascending record order; then
> the directory.

Two questions the sentence leaves open, both of which move bytes.

**(i) Is "then any record extents" inside or outside the per-layer loop?**
Reading *inside* puts each layer's sub-record extents immediately after that
layer's index region and leaves the file-scope user-metadata extent with no
stated position at all. Reading *outside* emits every record extent after every
layer's tiles and indexes. "then the directory" is plainly outside the loop
(there is one directory), which is the argument for reading the whole
semicolon-list as outside; but "For each layer …:" governs the colon, which is
the argument for inside.

**(ii) What is "ascending record order" for a sub-record?** Item 3 orders
top-level records by type and gives sub-records an order *within their layer
record*, but never places a sub-record relative to a top-level record in one
total sequence. A pre-order traversal (layer `sst`, then its sub-records, then
layer `mask`, then the top-level type-0x0002 record) puts `sst`'s metadata extent
before the file-scope one; a "top-level records first, sub-records after" reading
reverses them.

**I picked *outside* the loop, and a pre-order total record order** — outside,
because otherwise the profile places no top-level extent at all, which cannot be
what a "total emission order" means; pre-order, because item 3 introduces
sub-record ordering as a refinement of record ordering rather than as a separate
sequence. My generation-1 file happens to contradict my own second choice: I
emitted the file-scope metadata extent at [536,637) before `sst`'s at [637,681),
which is the reverse of pre-order. Under reading *inside*, `sst`'s metadata
extent would instead sit at [340,384) — the alignment gap I currently leave to
slack. Three profile-following writers, three different files.

**Byte-level: no**, for the same reason as writer-02 and writer-03: Appendix G
is non-normative and adds no requirement to any actor.

---

## 8. What I checked and did not report

Recorded so the negative results are usable, and so that nothing below is
mistaken for an unexamined area.

- **Every register-row cross-reference in the document resolves correctly** (§1's
  table above). The re-labelling of §21.2/§21.3 was carried through consistently
  into §9.6, §17.2, §21.1, §21.6, F33's own cell, T2/T13/T26, R4, and Appendix H.
- **The four "this rule carries no register row" justifications all hold.**
  §5.2's note (a byte belonging to no coverage class is undefinable, since
  `[R-LIF-08]` makes every unreached byte slack, leaving only overlap — F33/L18);
  §9.5's note (post-commit residue is met as F8/F14/F17); §7.4's note (nesting
  has no reader-detectable witness beyond L26, because the only payload a reader
  parses as records is a layer record's); §16.2's note (a stale slab declaration
  is, by `[R-SLB-04]`'s own definition, an invariant failure, hence L41 or L42).
  I attacked the last one hardest — with extent growth that renumbers ordinals,
  with A_slab = 1, with all-new tiles sentinelled — and could not construct a
  stale declaration that exhibits neither L41 nor L42.
- **§21's completeness against what a writer can get wrong.** I walked every
  MUST-level writer obligation I exercised and found a row for each: geometry
  floor (L32), value sets (L31/L33/L34/L36/L43/L45), alignment/slab (L20, L28,
  L29, L39, L40, L41, L42), fill length and bool fill (L30, L35), index
  cross-checks (L21, L22, L27), padding and pad bits (T4, T5), codec-1 length
  equality (T14), trailer gates (F8–F19), directory framing (F29, F24),
  user-metadata framing (F21–F23, L10–L12), multiplicity (F34, L19). I found no
  reachable MUST whose violation has a distinguishable single-file witness and no
  row.
- **Instance counts.** 121 rows, 248 instances, matching §21.8 exactly under
  §21.1's stated counting rule. Granularity across cells is uneven (L21 states
  interleaved and planar as one instance where L22 enumerates three fields), but
  §21.1 makes the count follow the cell rather than the cell follow a canon, so
  this is not a defect.
- **§4.7's note claims** that fixed-layout tables give "byte offset …, size,
  type, name, taxonomy class, and valid range" and that "All named constants
  appear once in Appendix B". §6.1's table has four columns and §7.2's five, and
  §10.2's range boundaries and `[R-CNT-25]`'s 5-byte minimum extent are not in
  Appendix B. Both statements sit inside a *Note*, which §2.1 makes
  non-normative, and neither reaches a byte. Not reported.
- **The §20.4 preservation table carries no requirement identifier of its own**,
  sitting between `[R-WRT-05]` and `[R-WRT-08]`; §21.6 cites `[R-WRT-08]` for its
  content, which settles which identifier owns it. Not reported.
- **§20.4's "No commit therefore removes a layer record or a file-scope
  user-metadata record"** names two cases where the general rule (both registered
  types are PE=1) covers three, the third being a layer's user-metadata
  sub-record. Appendix H repeats the same two-case phrasing. The preceding
  sentence forecloses the permissive misreading, so I did not report it.
- **§21.6's "A payload contains a byte string that mimics a trailer"** is
  justified by "nothing enumerates slack", though a live payload is not slack;
  the conclusion holds regardless via `[R-LIF-05]`'s no-backward-scan and §6.2's
  note. Not reported.
- **§23.1's "the only removal a commit performs"** coexists with §20.4's licence
  to drop an MU=0/PE=0 record, but a dropped record's extent also merely becomes
  unreachable slack, which is precisely §23.1's point. Not reported.
- **Whether an experimental-range *sub-record* carrying MU=1 belongs in §21.6's
  "conforming files a reader nevertheless refuses"** — the prose paragraph
  addresses the top-level case and cites `[R-CNT-15]`; the sub-record case is
  reject-layer under `[R-CNT-18]` and is not separately named. A reader's verdict
  is fully determined by `[R-CNT-18]` either way. Not reported.

## 9. Verdict

I implemented a creator, an appender and a compactor's rules on paper, emitted
1,088 bytes of generation 1 and two further generations, and read every one of
them back with an independently written reader. **Creation, the commit
protocol, slack accounting and torn-write recovery are fully determined by this
document — I did not guess once in §§5–17, and the document's own arithmetic is
correct everywhere I checked it.** The places where I had to guess are all in
§20.4's updater rules and in Appendix G, and only one of them — writer-01 —
changes the bytes a conforming implementation emits.
