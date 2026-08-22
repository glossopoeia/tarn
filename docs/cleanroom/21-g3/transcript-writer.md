# Round 21 — Writer implementer, verbatim working transcript

**Charter:** implement, on paper but concretely, a conforming writer and updater.
**Access:** I read `spec/tarn.md` and nothing else. See "Disclosure" at the end.

Everything below is the actual walk, in the order I did it.

---

## 0. Instrument check before trusting my own arithmetic

Before building anything I implemented CRC-32C to §4.5's parameters (Castagnoli
0x1EDC6F41, reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF, stored
little-endian) and checked it against every constant the document states, because
if my CRC is wrong every byte below is wrong.

| Document's claim | Where | My computation | Agrees |
|---|---|---|---|
| `CRC-32C("123456789") = 0xE3069283` | §4.5 check vector | `0xE3069283` | yes |
| `CRC-32C(zero bytes) = 0x00000000` | §4.5 | `0x00000000` | yes |
| CRC over four sentinel entries = `0x80A34955` | §7.4 example | `0x80A34955` | yes |
| `crc_of_crc_array` of that = `0xC4EE982E` | §7.4 example | `0xC4EE982E` | yes |
| CRC of a full all-sentinel segment (2¹⁶ entries) = `0xEECB3BB2` | §15.4 `[R-IDX-05]`, Appendix B | `0xEECB3BB2` | yes |
| Appendix A trailer CRC = `0xE00938D2` over trailer `[0,60)` | Appendix A | `0xE00938D2` | yes |
| Appendix A directory `[16,20)` = CRC of zero bytes | Appendix A | `00 00 00 00` | yes |

Appendix A's whole 128-byte file re-verifies: 128 bytes, `F mod 64 = 0`,
`dir_offset = 16 ≥ 16`, `dir_length = 4 ≥ 4`, `dir_offset + dir_length = 20 ≤ F − 64 = 64`,
`file_id ≠ 0`, reserved zero. §5.1's "no conforming file is shorter than 128 bytes"
also checks: 16 (front) + 4 (minimum directory at minimum offset) = 20, and the
trailer must begin at a 64-aligned offset, so the first admissible trailer start
is 64 and F = 128. Nothing shorter satisfies `[R-CNT-27]`.

I also mechanically counted §21's register, since §21.8 makes a checkable claim.
Extracting every row `| F#|L#|T#|R# |` and counting instances by §21.1's rule
("instances within a cell are separated by semicolons, and a cell reading — is
one instance"):

```
rows: 121   (F 36, L 49, T 26, R 10)  — matches §21.2/3/4/5's stated counts
instances: 273 (F 58, L 116, T 55, R 44) — matches §21.8's "121 conditions over 273 instances"
```

Exact. That is a strong signal that the register is maintained mechanically, and
it steered me away from hunting there.

---

## 1. Creation: a file built byte by byte

I built a deliberately awkward small file — three layers exercising edge padding,
a sentinel, a packed planar bool plane, a slab declaration with alignment, a
zero-extent layer, a file-scope user-metadata record and a layer-scope
user-metadata sub-record.

### 1.1 What the caller asked for (the "input", so divergence talk later has a referent)

- **Layer `grid`** — rank 2, dims `y` (extent 5, tile extent 4) and `x` (5, 4).
  Interleaved, two channels: `t` float32 with fill `0x7FC00000`, `m` bool with
  fill `0x00`. Sample `t(y,x) = float(10y + x)`, `m(y,x) = 1` iff `x+y` even.
  The band `y = 4, x ∈ [0,4)` is fill in the caller's array.
- **Layer `mask`** — rank 1, dim `x` (extent 20, tile extent 8). Planar, one bool
  channel `b`, fill `0x00`, `b(x) = 1` iff `x mod 3 = 0`.
- **Layer `empty`** — rank 1, dim `z` extent 0, tile extent 2³¹. One uint8 channel
  `v`, fill `0x00`. Schema-first: declared now, grown later (§11.1's rationale).
- File-scope metadata `{"tarn.created":…,"tarn.creator":…}`; layer-scope metadata
  on `grid`, `{"tarn.title":"5x5 demo grid"}`.

### 1.2 Decisions the document fixed for me

| Decision | Fixed by | Value |
|---|---|---|
| Bytes `[0,16)` | §6.1, `[R-CNT-04]` | `89 54 41 52 4E 0D 0A 1A` + 8 zeros |
| Byte order everywhere | `[R-ENC-01]` | little-endian |
| Where creation's first write goes | `[R-LIF-02]` creation path | offset 16 |
| Grid counts | `[R-GEO-03]` | `grid` G=(2,2) N=4 P=16; `mask` G=(3) N=3 P=8; `empty` G=(0) N=0 |
| Addressed-tile count | `[R-GEO-03]` | `grid` N=4 (interleaved); `mask` C·N=3 (planar); `empty` 0 |
| Disk ordinal | `[R-GEO-06]` | `s` interleaved; `c·N+s` planar |
| In-tile ordinal | `[R-GEO-06]` | `Σ uᵢ ∏_{j>i} Tⱼ`, row-major, permanently |
| Interleaved decoded size | `[R-SER-02]` | `P·Q` = 16·5 = **80** bytes |
| Planar bool decoded size | `[R-SER-03]` | `⌈P/8⌉` = ⌈8/8⌉ = **1** byte |
| Padding-position content | `[R-SER-05]` | each channel's recorded fill |
| Pad bits | `[R-SER-05]` | the plane's fill bit (none here: `P mod 8 = 0`) |
| Codec-1 stored length | `[R-COD-04]` | must equal decoded size |
| Index region shape | `[R-IDX-01]`, `[R-CNT-17]` | `entry_count·20 + ⌈entry_count/2¹⁶⌉·4` |
| Sentinel bytes | `[R-IDX-02]` | `FF ×16 00 ×4` |
| `entry_count = 0` layer | §7.4, `[R-CNT-17]`, `[R-CNT-23]` | extent slot (0,0), `crc_of_crc_array = 0` |
| Registered record flags | §7.3, `[R-CNT-22]` | layer MU=1 PE=1; user metadata MU=0 PE=1 |
| User-metadata inline payload | `[R-MTA-03]` | exactly one byte, the encoding |
| User-metadata extent | §7.1, §8.1 | document bytes then a 4-byte CRC over them; length ≥ 5 |
| JSON member order | `[R-MTA-05]` | ascending by keys' UTF-8 bytes at every depth |
| Directory placement | `[R-CNT-05]` | nothing between its end and the trailer |
| Pad | `[R-LIF-02]` step 5 | to the next 64-byte boundary |
| `flags` | `[R-CNT-08]` | 0 (creator) |
| `generation` | `[R-LIF-02]` | 1 |
| Trailer reserved `[56,60)` | §6.2 | zero |

### 1.3 Decisions the document left to me

| Decision | Left open by | What I chose |
|---|---|---|
| Order and position of every structure | `[R-SLB-05]`, `[R-LIF-02]` step 2 | Appendix G item 3's total order |
| Gap content | `[R-CNT-03]` (SHOULD) | zeroed |
| Record order in the directory | `[R-CNT-14]` | by type, layers by name |
| `file_id` | §6.2 (≠0), `[R-LIF-03]` (SHOULD random) | `0x0123456789ABCDEF` (fixed, for a reproducible transcript) |
| `version_minor` | `[R-CNT-26]` (SHOULD) | 0 |
| Codec / filter per layer | `[R-COD-03]`, `[R-COD-09]` | 1 / 1 for `grid` and `mask`; codec 4 for `empty` |
| Alignment vs slab | §16, `[R-CNT-16]` | none on `grid`; S=2, A_slab=64 on `mask` |
| Whether to store an all-fill tile | nothing requires either | sentinel (Appendix G item 6) |
| Metadata storage encoding | `[R-MTA-03]` | 1 (none) |
| Tile extents | §11.3 Note: "a writer's choice" | 4×4 and 8 |
| Channel layout | `[R-SER-06]` | interleaved / planar / interleaved |

### 1.4 The emitted layout

```
[    0,   16)  front signature block            structure? no — §5.2 counts it separately
[   16,   96)  grid stored tile, disk ordinal 0  80 B, codec 1, crc 0x612244E9
[   96,  176)  grid stored tile, disk ordinal 1  80 B, crc 0x00F35A32
[  176,  256)  grid stored tile, disk ordinal 3  80 B, crc 0x51E62F3D
[  256,  340)  grid tile-index region            84 B = 4·20 + 1·4
[  340,  384)  SLACK 44 B                        forced by A_slab = 64 on `mask`
[  384,  385)  mask stored tile, ordinal 0        1 B   run 0 first stored tile, 384 mod 64 = 0
[  385,  386)  mask stored tile, ordinal 1        1 B   packed: 384 + 1
[  386,  448)  SLACK 62 B                        forced by A_slab = 64 for run 1
[  448,  449)  mask stored tile, ordinal 2        1 B   run 1 first stored tile, 448 mod 64 = 0
[  449,  513)  mask tile-index region            64 B = 3·20 + 1·4
[  513,  587)  file-scope user-metadata extent   74 B = 70 doc + 4 CRC
[  587,  621)  grid's user-metadata sub-record extent  34 B = 30 doc + 4 CRC
[  621, 1003)  directory region                 382 B (4 records + 4-byte CRC)
[ 1003, 1024)  SLACK 21 B                        pre-trailer pad
[ 1024, 1088)  live trailer                      64 B
F = 1088, F mod 64 = 0.  Claimed 961 B, slack 127 B, 961 + 127 = 1088. ✔
```

Front signature block and trailer, verbatim:

```
00000  89 54 41 52 4E 0D 0A 1A 00 00 00 00 00 00 00 00
01024  8A 4E 52 41 54 0D 0A 1A 01 00 00 00 00 00 00 00   magic, vmaj 1, vmin 0, flags 0
01040  01 00 00 00 00 00 00 00 6D 02 00 00 00 00 00 00   generation 1, dir_offset 621
01056  7E 01 00 00 00 00 00 00 40 04 00 00 00 00 00 00   dir_length 382, F 1088
01072  EF CD AB 89 67 45 23 01 00 00 00 00 02 27 30 80   file_id, reserved 0, CRC 0x80302702
```

`grid`'s tile-index region, verbatim — the shape §15.1 fixes, entry array then
segment-CRC array with no padding anywhere:

```
00256  10 00 00 00 00 00 00 00 50 00 00 00 00 00 00 00   entry 0: offset 16, length 80
00272  E9 44 22 61 | 60 00 00 00 00 00 00 00 50 00 00 00   crc; entry 1: offset 96, len 80
00288  00 00 00 00 32 5A F3 00 | FF FF FF FF FF FF FF FF   crc; entry 2: SENTINEL
00304  FF FF FF FF FF FF FF FF 00 00 00 00 | B0 00 00 00   …crc 0; entry 3: offset 176
00320  00 00 00 00 50 00 00 00 00 00 00 00 3D 2F E6 51   len 80, crc
00336  D5 BC 82 38                                       segment 0 CRC = 0x3882BCD5
```

`crc_of_crc_array` for `grid` is CRC-32C of those four bytes = `0x24904702`, and
it appears in the layer record at directory offset 845 as `02 47 90 24`.

### 1.5 The `grid` layer record's inline payload, field by field

128 bytes, packed in §7.4's table order with no alignment or padding between
fields (`[R-CNT-18]`: "fields are packed in table order with no alignment or
padding between them"):

```
 0  04 67 72 69 64             name: length 4, "grid"
 4  01                         layout 1 = interleaved
 5  01 00                      linearization 1 = row-major
 7  01 00                      codec 1 = none
 9  01 00                      filter 1 = none
11  00 ×8                      alignment A = 0
19  00 ×8                      slab S = 0
27  00 ×8                      slab alignment 0, forced by S = 0 ([R-CNT-23])
35  02                         rank d = 2
36  02 00                      channel count C = 2
38  01 79 | 05.. | 04..        dim "y", extent 5, tile extent 4
56  01 78 | 05.. | 04..        dim "x", extent 5, tile extent 4
74  01 74 0C 00 04 00 00 C0 7F channel "t", type 12 float32, fill len 4, 0x7FC00000
83  01 6D 01 00 01 00          channel "m", type 1 bool, fill len 1, 0x00
89  01                         index_encoding 1
90  04 00 00 00 00 00 00 00    entry_count 4
98  02 47 90 24                crc_of_crc_array
102 <26-byte sub-record>       user metadata, MU=0 PE=1, inline_length 1, extent (587,34)
```

Cross-checks I ran and the rules they answer to:

- `[R-CNT-17]`: `extent_length = 4·20 + ⌈4/2¹⁶⌉·4 = 84` — matches the slot. And
  `entry_count = 4 = N` for an interleaved layer.
- `[R-CNT-23]`: fill length 4 equals float32's element size; fill length 1 equals
  bool's; the bool fill byte is `0x00`, permitted by `[R-TYP-07]`.
- `[R-CNT-18]`: leading fixed fields + 2 dimension entries + 2 channel entries +
  trailing fixed fields = 102 bytes; the remaining 26 parse as exactly one
  complete sub-record with no residue.
- `[R-COD-04]`: every non-sentinel entry's length is 80 = `P·Q`.

Edge padding, which is where a writer most easily gets `[R-SER-05]` wrong: `grid`'s
tile at tile-coordinates (0,1) covers `x ∈ [4,8)`, so `u_x ∈ {1,2,3}` are padding
positions; the tile at (1,1) covers `y,x ∈ [4,8)` and has one real position, (4,4),
and fifteen padding positions. At each padding position I encoded `t`'s recorded
fill `00 00 C0 7F` and `m`'s recorded fill `00` — not zeros, not uninitialised
memory. §14.5's rationale is exactly right that this is what makes the tile CRC
a function of logical content.

`mask` tile 2 covers `x ∈ [16,24)`; `x ∈ [20,24)` are padding, so bits 4–7 of its
single byte carry the fill bit 0. Value: `0x04`.

### 1.6 The slab arithmetic, checked

`mask` declares S = 2, A_slab = 64, layout planar, C = 1, N = 3. `[R-SLB-02]`:
one block `[0,3)`; run 0 = ordinals `[0,2)`, run 1 = `[2,3)` (the final run of a
block may cover fewer than S ordinals). `[R-SLB-03]` then requires, per run, that
stored tiles be packed in ordinal order and the first stored tile be A_slab-aligned:

- run 0: 384 mod 64 = 0 ✔; tile 1 at 384 + 1 = 385 ✔
- run 1: 448 mod 64 = 0 ✔; single stored tile, nothing to pack ✔

`[R-CNT-16]` forbids A ≠ 0 together with S ≠ 0, so `mask` declares A = 0. `[R-CNT-23]`
requires A_slab = 0 when S = 0, which is why `grid` and `empty` carry three zero u64s.

The two gaps A_slab forces — 44 and 62 bytes — are slack under §5.2 ("alignment and
slab gaps"), unconstrained in content, zeroed by `[R-CNT-03]`'s advice. No index
region is alignment-constrained: `[R-SLB-01]` and `[R-SLB-03]` bind *stored tiles'
offsets* only, which is why `mask`'s index region sits at the unaligned 449.

### 1.7 `empty`, and the one place the creation walk made me guess

`empty` declares extent 0, tile extent 2³¹, one uint8 channel, **codec 4 (lz4)**.
`[R-GEO-02]` makes the layer valid: grid count 0, zero addressed tiles, empty index,
extent slot (0,0), `crc_of_crc_array = 0`. §17.2's Note goes out of its way to bless
exactly this:

> The cap is quantified over the layer's *addressed* tiles, so a layer that
> addresses none — any dimension extent 0 (`[R-GEO-02]`, §21.6) — satisfies it
> whatever its tile shape declares, and codec 4 is conforming there. […]
> `[R-ENC-04]`'s overflow rule carries no such quantifier — it binds any sum or
> product a file yields — so P·Q and P·Bᶜ are checked in an empty layer even
> though this cap is not.

So the document tells me two things about this layer: `[R-COD-07]`'s
`0x7E000000` cap does **not** bite (no addressed tiles), and `P·Q = 2³¹` **is** a
quantity the file yields and is checked against `[R-ENC-04]`'s 2⁶³−1 ceiling
(it passes). §19.3 confirms the second: at layer access a reader validates
"the decoded sizes §14 derives from it (`[R-SER-02]`, `[R-SER-07]`)".

What it does **not** tell me is whether the third rule in the same family bites:
§21.9's minimum guarantee row "decoded size of one tile | 256 MiB". My layer's
derived decoded size is 2³¹ = 2048 MiB, eight times the guarantee, with no tile
in existence. Is that "a quantity of the file" for `[R-ERR-04]`'s purposes?
This is **writer-01** below; it is the one place in the creation walk where I could
not decide from the text, and it decides whether every conforming reader must
open my file.

I resolved it by taking the `[R-COD-07]` precedent — per-tile quantities are
quantified over addressed tiles — and emitting the layer. A writer that resolves
it the other way would refuse to declare a tile shape above 256 MiB even on an
empty layer, and would emit different bytes for the same schema-first request.

### 1.8 The rest of creation

Emission order: front block, then from offset 16, per `[R-LIF-02]`'s creation
paragraph ("the writer first emits the front signature block […] then performs
steps 2–6, writing beginning at offset 16, with generation 1"). Then barrier
(step 4), pad, trailer (step 5), barrier (step 6). `[R-WRT-02]` is emphatic:
"both barriers, not one". A creator that omits the first barrier can produce a
trailer that outlives its own directory on a reordering device — §9.2's Note
prices that as "torn commits are detected" rather than "invisible", which is a
degradation of the recovery guarantee, not of correctness.

Read back through §19.1–§19.4 the file passes every reader check: front block by
equality; trailer magic, CRC (`0x80302702`), version gate, then the field gates;
directory CRC; record walk with no residue; per-layer §19.3 validation; per-tile
index chain, entry classification, payload CRC, codec-1 length equality; and the
verifier's §9.7 coverage walk — 961 claimed bytes, no two claimants overlapping,
127 slack.

---

## 2. The append procedure

### 2.1 Adding a layer (§20.3's shape (a)) — walked, then the harder case

Trivial and fully determined: nothing existing is rewritten, every retained
record is re-emitted byte-identically including its extent slot, so layer `A`'s
record still addresses the index region it always addressed (`[R-WRT-05]`), and
the only new slack is the superseded directory, pad and trailer.

### 2.2 Superseding a tile (shape (b)) — built and verified

Commit 2 supersedes `grid`'s disk ordinal 1. The order I emitted in, and what
each step is answerable to:

1. **Establish F** (`[R-LIF-04]`): validate the trailer in the *physical* file's
   final 64 bytes. It passes, F = 1088. Had it failed, the file is torn and I
   MUST NOT append; recovery (§9.6) is a separate, deliberate operation and never
   an implicit step of opening for append.
2. **Open** (§19.1, `[R-RDR-01]`): the appender is a reader here. Front block
   resident → verify by equality. Trailer, directory, record walk, layer-name
   namespace.
3. **Validate what the commit touches** (`[R-WRT-03]`): the trailer and the *full*
   directory always, because re-emission relies on every directory byte; §19.3
   layer validation for `grid`; and the §19.4 index chain for every segment whose
   entries the commit reuses — `grid` has one segment, so `crc_of_crc_array` and
   segment 0. `mask` and `empty` get neither §19.3 nor an index-chain check: their
   records are copied, not relied on.
4. **Write payloads and indexes**, beginning at exactly F.
5. **Re-emit the directory** complete (§20.4).
6. **Commit**: barrier, pad, trailer at generation 2 with the same `file_id`,
   `flags` unchanged (no ignore-lane bits to copy forward here), barrier.

Result, verified by a full re-read:

```
[1088,1168)  new stored tile, ordinal 1          80 B
[1168,1252)  grid's whole tile-index region       84 B  — necessarily a new placement
[1252,1634)  directory                           382 B  — dir_length unchanged
[1634,1664)  pre-trailer pad                      30 B
[1664,1728)  trailer, generation 2
F = 1728, claimed 961 B (unchanged), slack 767 B.
```

Three entries of `grid`'s index were copied byte-identically at their disk-ordinal
positions; one was re-pointed. 640 bytes of file growth to change 80 bytes of
data, of which 631 is new slack. §20.3's own note quantifies this at scale
("editing one sample of a 10⁶-tile layer appends about 20 MB of index").

The claimed total is *invariant* across the commit — 961 bytes before and after —
which is the cleanest statement I found of what a supersede actually does: it
moves a structure, it does not add one.

### 2.3 The slab layer is where an appender runs out of room

I then tried to grow `mask` from extent 20 to 25. `G` goes 3 → 4, so
`entry_count` goes 3 → 4, `[R-CNT-17]` forces a new `extent_length` of 84, and the
whole index region is re-emitted. `[R-SLB-02]`'s run partition changes: run 0 =
`[0,2)`, run 1 = `[2,4)`. Tile 2 stays at 448 (still run 1's first stored tile,
still 64-aligned), and `[R-SLB-03]` then requires the new tile 3 to sit at
**449** — inside the committed prefix, which `[R-LIF-01]` freezes absolutely
("Bytes in [0, F) […] are immutable"). Slack inside `[0,F)` is no help: it is
still inside `[0,F)`.

So an appender adding a tile to a partially-populated slab run has exactly two
moves, and the document supplies both:

- **clear the declaration** in the new generation — `[R-SLB-04]` states it
  ("MUST either re-establish the invariants for every such run — or clear the
  declaration in the new generation"), and §20.3's shape-(c) example names
  "clearing a slab declaration" as a directory-only change; or
- **supersede the whole run**: rewrite every stored tile of that run after F,
  A_slab-aligned and packed, stranding the originals as slack. §20.3's SHOULD
  ("A writer SHOULD instead produce a new file wherever a commit would strand a
  large share of a layer's stored bytes — and always where it would re-emit every
  one of them") is the guidance on when that is the wrong move.

Adding a slab declaration to a layer that already stores tiles is the same problem
seen from the other end, and is likewise decided: the invariant is a file
predicate (§21.3 rows L41, L42 name `[R-SLB-03]` as governing, so it is a
file-conformance violation), so `[R-CNF-05]` binds the writer whether or not
`[R-SLB-04]`'s "changes the run partition" is read to cover a declaration
appearing where there was none.

I note that `[R-SLB-01]`'s alignment invariant carries no BCP-14 keyword —
"When declared: every stored tile's offset satisfies offset mod A = 0" — and
checked whether that matters, given round 17's and 18's lesson about unkeyworded
clauses. It does not: the sentence states a *file* predicate, §21.3's L40
registers it as a violation governed by `[R-SLB-01]`, and §21.1 makes the register
an inventory of file-conformance violations, so `[R-CNF-05]` binds the writer
transitively. The same reasoning covers `[R-SLB-03]`'s packing and alignment
sentences (L41, L42). No finding.

### 2.4 Every combination of the record flags

The document defines two flag bits (`[R-CNT-12]`: bit 0 MUST_UNDERSTAND, bit 1
PRESERVE_ON_EDIT, bits 2–15 reserved) and three sources of authority for their
values (§20.4). The full matrix, and exactly what my updater may do:

**Authority first** (§20.4: "Persistence governs every record type; only the
authoritative source of the flags differs"):

| Type | Whose flags govern |
|---|---|
| §7.3-registered (0x0001, 0x0002) | the registry's fixed values, never the stored bits (`[R-CNT-22]`) |
| unregistered, updater implements it | the definition the updater implements it from |
| unregistered, updater does not implement it | the stored bits (`[R-CNT-15]`), with MU=1/PE=0 read as PE=1 (`[R-CNT-12]`) |

**Then the obligations**, for a type the updater does not implement:

| Stored MU | Stored PE | Top-level | Layer sub-record |
|---|---|---|---|
| 1 | 1 | **No commit at all.** `[R-CNT-15]` makes an unimplemented top-level MU=1 record reject-file, and the updater is a reader first (§2.3, §19.1 step 4 applies the MU gate at open, mandatorily). Compaction barred on the same ground (`[R-WRT-06]`). | Retain byte-identical; **that layer** may not be modified; every other layer stays editable (`[R-CNT-18]`, reject-layer). |
| 1 | 0 | Read as PE=1 → identical to the row above. Separately, the combination is itself a violation whose detector is the verifier (F25 / L46), which my appender is not obliged to detect and carries forward. | Same. |
| 0 | 1 | Retain byte-identical, **extent content unmodified**. May not be re-encoded (`[R-WRT-08]`); may not be relocated by an appender — relocation is compaction's operation only. | Same, and the layer record containing it is re-emitted byte-identically as a whole. |
| 0 | 0 | Retain, **or drop** — but only in a commit that *independently* changes the file's layer set, any layer record's content, or another non-layer top-level record. Dropping it, or dropping another record in the same commit, is not itself such a change, so "a commit whose only effect would be the drop MUST retain it". Its extent becomes slack. SHOULD report the loss. | Retain, or drop only in a commit that independently changes that layer's record, the entry set of its index, or which of its tiles are stored. |
| reserved bits 2–15 set | — | Readers MUST ignore; the appender re-emits them byte-identically. §20.3 step 2 settles that this is not authoring them: "Reproducing a structure's bytes unchanged is not authoring them." | Same. |

Two consequences I had to reason out rather than read directly, and both came out
determinate:

- **My commit 2 licenses drops.** Superseding a tile re-places `grid`'s index
  region, which moves its extent slot and so modifies `grid`'s record — §20.4
  says so explicitly. So commit 2 could have dropped a top-level MU=0/PE=0
  record, or such a sub-record *of `grid`*, but not one of `mask`.
- **Dropping a sub-record makes the layer record new output.** `[R-WRT-05]`:
  "a record it modifies is new output under its writer obligations
  (`[R-CNF-05]`)". So an updater cannot drop a sub-record from a layer whose
  record carries a latent violation — and it will find out, because
  `[R-WRT-03]` obliges §19.3 layer validation for every layer whose record the
  commit modifies, and §19.3 rejects the layer. The circle closes.

The registered types are the easy half: both carry PE = 1, so no commit removes a
layer record or a user-metadata record at either scope, and "implementing a
record's type confers understanding of it, not permission to drop it". §20.4
prices the alternative correctly: an in-place removal would strand the layer's
tiles and index as slack and leave the file no smaller.

### 2.5 Write order, durability, and the commit point

`[R-LIF-02]`, in order: (1) begin at exactly F; (2) payloads, index regions, record
extents, in any order satisfying §5.2's classes; (3) the complete directory and its
CRC; (4) **barrier**; (5) pad to the next 64-byte boundary, then the trailer;
(6) **barrier**.

- Durable before what: everything in steps 1–3 must be durable before *any* byte
  of step 5. That is the whole safety property — the trailer is the only structure
  that can turn unreferenced bytes into a live state.
- No barrier is required between the pad and the trailer: the pad is slack, whose
  content no requirement constrains.
- **The commit point is step 6.** Before it, the previous generation is the live
  one and remains byte-intact; after it, the new generation is. §9.2's Note is
  precise that step 3 cannot be discharged by an earlier generation's directory:
  "A writer that re-points a new trailer at a prior generation's directory region
  has left step 3 unperformed."
- `[R-LIF-04]` adds a truncation obligation that lands *inside* the commit:
  a writer that overwrote from F over a longer stale physical file must truncate
  to the new `committed_file_length` "no later than step 6", so residue never
  survives into a committed state.

### 2.6 There is no in-place update

The charter lists "in-place update" as a commit shape. The document's answer is
that there is no such shape: `[R-LIF-01]` makes every conforming mutation "either
a commit (§9.2) or a whole-file rewrite under a new file_id (compaction, §20)".
The only writes to existing bytes the document sanctions anywhere are to bytes
**at or beyond F** (`[R-LIF-04]`'s "overwrite from F") and truncation. Even
slack — bytes no live claimant owns — is frozen, because `[R-LIF-01]` freezes
`[0, F)` without reference to reachability. That is what makes §9.3's
(file_id, range) cache contract sound, and I relied on it in §2.3 above.

---

## 3. Slack, per commit shape

Who counts it: a verifier, never a reader (§5.2's second Note: "Coverage is
checked by verifiers, never by readers"). `[R-CNT-21]` makes the total a MUST for a
verifier that reaches a live state, and a *partial* total — an upper bound naming
what stopped the walk — where a scope-level rejection or an early stop under
`[R-CNF-11]` prevented full enumeration.

What it may contain: anything. "Slack has no internal structure this specification
defines, its content is unconstrained, and no conformance requirement applies to
it. A reader MUST NOT interpret it." Writers SHOULD zero it (`[R-CNT-03]`); nothing
rides on whether they do. §22.3 and §23.1 are the honest consequences: corruption
confined to slack is invisible to reader and verifier alike, and superseded sample
data stays readable with a hex editor.

| Commit shape | Bytes that become slack | Notes |
|---|---|---|
| **Create** | alignment and slab gaps; the pre-trailer pad | My file: 44 + 62 + 21 = 127 of 1088. |
| **Append — new layer** (a) | the previous directory, pad and trailer only | Sized by the file's *layer count*, never by any layer's data. |
| **Append — supersede / add tiles** (b) | superseded payloads; the layer's **whole** previous index region; previous directory, pad, trailer | My commit 2: 80 + 84 + 382 + 21 + 64 = 631. |
| **Append — directory-only** (c) | previous directory, pad, trailer. Editing user metadata is *not* this shape: its document lives in an extent, so the old extent becomes slack too | |
| **Append — shrink** | the de-addressed tiles' extents, plus the previous index region and directory triple | §20.3 step 4 and §23.1: "A commit removes sample data two ways — superseding it, and a shrink that de-addresses tiles". |
| **Whole-file rewrite (new file_id)** | none in the new file; the old file persists entirely | `[R-LIF-01]` sanctions it; §20.4 recommends it as the way to produce a file without a layer. |
| **Compaction** | none carried; the output's own alignment gaps and pre-trailer pad remain | §20.5: output contains only live structures. It is "the only operation that reclaims slack" — truncation past F and recovery shorten a file but reclaim nothing. |
| **Abandoned partial write** | **none — the question does not arise.** | See below. |

The abandoned partial write is the interesting one and the document resolves it
cleanly. Slack is defined against the *live committed state*, which is anchored at
F. In a torn file the final 64 bytes are not a valid trailer, so `[R-CNT-06]`
fails, there is no F and no live state, and §5.2 says so in terms:

> Where §6.2's ordered validation rejects the file before a live trailer is
> established there is no F and no live state to walk, so the total is not owed at
> all: the verifier reports the trailer failure and nothing about slack, which is
> not a partial total but the absence of one.

So the bytes of an abandoned write are not slack; they are the reason the file is
nonconforming. Nobody counts them, and `[R-LIF-04]` obliges the next writer to
truncate or overwrite them.

One more accounting subtlety I checked: a *record extent* is a claimant "whatever
the record's type" (§5.2), and a layer's tile-index region enters the walk exactly
once — as that layer record's extent, not a second time as a region (§9.7). A
record is not a claimant of its own header and payload; the directory region covers
those. My walk's arithmetic (961 + 127 = 1088) only balances on both of those
readings, which is a decent check that I read them right.

---

## 4. Torn-write recovery — five crash points

For each: what the next reader sees, what the next updater does, and whether the
file is conforming in the meantime. Baseline: a committed state at F = 1088,
generation 1; commit 2 in progress.

**(A) Crash during step 2 (payload bytes partly written).** Physical length is
somewhere in (1088, 1252). The last 64 bytes are tile or index bytes.
*Reader:* the 8 bytes at physical-end − 64 are not the trailer magic → F8 →
reject-file, and `[R-LIF-05]` forbids scanning backward, so it reports the file
torn or invalid and stops. *Updater:* `[R-LIF-04]` step 1 fails → no append.
Recovery (§9.6) probes backward at 64-aligned offsets from the largest `o` with
`o + 64 ≤` physical length; the first magic it meets is trail₁ at 1024, whose CRC
verifies and whose `committed_file_length` equals `o + 64 = 1088`. Truncate to 1088
and the file is exactly the generation-1 file again. *Conforming meanwhile:* **no** —
F8 and F17 both fire.

**(B) Crash after step 3, before step 5.** Physical end is the new directory's end
(1634). Same reader verdict, same recovery. Worth noting: the last 64 bytes here
end in the directory's own CRC, and §6.2's Note has already priced the case where
some byte-string mimics a trailer at exact end of file — "it is caught at the
directory CRC (§7.1) — detection is never silent". §21.6 records a trailer-mimic in
a payload as *inert*: nothing enumerates slack. *Conforming meanwhile:* no.

**(C) Crash inside step 5, mid-trailer.** Physical length between 1664 and 1728.
The bytes at physical-end − 64 are pad and partial trailer; magic or CRC fails.
Identical handling. *Conforming meanwhile:* no.

**(D) Crash after the trailer's bytes reach the device but before step 6's
barrier, with the step-4 barrier weaker than assumed.** The trailer is intact and
self-consistent (it carries its own CRC over `[0,60)`), `committed_file_length`
matches the physical size — so the file passes every §6.2 gate — but the directory
it points at is not durable. *Reader:* the directory CRC fails → F20 → reject-file.
§9.2's Note is exactly this case: "safety degrades from 'torn commits are
invisible' to 'torn commits are detected': §8's chain still catches every
inconsistent state loudly". *Updater:* the open fails at step 3, reject-file bars
every commit. Recovery's probe finds trail₂ first, whole-file re-verification
fails, so per `[R-LIF-06]` "a candidate whose whole-file re-verification fails was
not a commit state, so the tool continues the probe past it" — landing on trail₁,
and it MUST report which candidate it settled on and how many it rejected.
*Conforming meanwhile:* no.

**(E) Crash after step 6 but before `[R-LIF-04]`'s truncation, with stale residue
past F₂.** The commit *completed*, yet the file does not read: the physical size
exceeds `committed_file_length`, so F17 fires. §9.5's Note names precisely this
state — "Residue past a completed commit carries no register row of its own. A
reader meets it as a trailer that fails its gates […] What the residue violates is
`[R-LIF-04]`'s writer obligation to truncate or overwrite". Recovery's probe starts
above F₂ − 64, walks down, meets trail₂, re-verifies whole, truncates to 1728 and
the *new* generation is recovered. *Conforming meanwhile:* no — which is the
sharpest lesson of the whole exercise for a writer: the truncation is not
housekeeping, it is part of the commit.

Two normative cautions §9.6 attaches, both of which bind my recovery tool: output
MUST be re-verified as a whole file before being trusted, and truncation to an
earlier commit boundary is indistinguishable in-format from that earlier version,
so rollback detection needs out-of-band state.

---

## 5. Byte-divergence catalogue

Given identical input arrays and identical stated options, every way two
**conforming** writers may legitimately produce different bytes, and whether
Appendix G closes it.

| # | Degree of freedom | Licensed by | Appendix G |
|---|---|---|---|
| 1 | Placement of every structure; order of tiles, index regions, extents | `[R-SLB-05]`, `[R-LIF-02]` step 2 | item 3 — closed |
| 2 | Extent of the gaps between structures | `[R-SLB-05]` | item 3 — closed |
| 3 | Content of those gaps and of the pre-trailer pad | `[R-CNT-03]` (SHOULD) | item 3 ("every byte of every such gap is zero") — closed |
| 4 | Record order in the directory | `[R-CNT-14]` | item 3 — closed |
| 5 | Sub-record order inside a layer record | `[R-CNT-14]`, `[R-CNT-18]` | item 3 — closed |
| 6 | `file_id` (any nonzero) | §6.2, `[R-LIF-03]` (SHOULD random) | item 2 — closed, and its "last eight bytes in output order, read little-endian" is well defined |
| 7 | Encoder output for codecs 2–4 | `[R-CNF-05]`, §17.2's Note | item 1 — closed by pinning the producer, correctly noting byte-identity across *implementations* is unattainable |
| 8 | DEFLATE's up-to-seven unused final-byte bits | §17.2's Note, explicitly | item 1 — closed, and the Note says so |
| 9 | zstd `Frame_Content_Size` present or absent | `[R-COD-06]` ("MAY be present") | item 1's "fixed encoder settings" — closed, if a little implicitly |
| 10 | Whether an all-fill tile is stored or sentinelled | nothing requires either | item 6 — closed |
| 11 | The fill recorded when the caller chooses none | `[R-TYP-10]` (SHOULD) | item 7 — closed, and item 7 correctly notes it reaches item 6 |
| 12 | `version_minor` | `[R-CNT-26]` (SHOULD) | item 8 — closed |
| 13 | Whether a declared alignment or slab is present, and its values | §16 | item 5 — closed |
| 14 | Filter 1 vs filter 2 | `[R-COD-09]` | item 5 — closed, explicitly |
| 15 | Number of generations / checkpoint commits | `[R-LIF-07]` (SHOULD) | item 4 — closed |
| 16 | JSON serialization of a metadata document (escaping, number formatting, whitespace) | `[R-MTA-05]` pins order only; §18.2's Note concedes number formatting varies | item 9 — closed by pinning the producer |
| 17 | Metadata storage encoding 1 vs 2, and the zstd producer for 2 | `[R-MTA-03]` | item 9 — closed |
| 18 | NFC vs NFD in names | `[R-ENC-14]` (SHOULD) | item 10 — closed |
| 19 | **Tile extents `Tᵢ`** | §11.3's Note: "Tile extents are a writer's choice, and this specification imposes none"; §11.1 permits `Tᵢ > Eᵢ` | **not closed by any item** |
| 20 | **Channel layout, interleaved vs planar** | `[R-SER-06]`; §14.4's Note observes a single-channel bool layer's tile bytes differ between them | **not closed by any item** |

Items 19 and 20 are **writer-02** below.

Things I checked and found were *not* degrees of freedom, in case that is useful
to a later round:

- Sharing one tile-index region between two layers with identical geometry, or
  one stored extent between two byte-identical tiles: forbidden, `[R-CNT-13]`
  ("no two extent slots and no two structures overlap"), reject-file across
  layers and reject-layer within one.
- Padding-position content, pad-bit content, interleaved bool byte values,
  sentinel bytes, the trailer's reserved bytes, every checksum, `entry_count`,
  `extent_length` under `[R-CNT-17]`, `crc_of_crc_array` when `entry_count = 0`:
  all pinned.
- A pre-trailer gap longer than to the next 64-byte boundary. §6.2 says "a longer
  gap is conforming, and no conforming commit produces one", and §2.3 classes it
  with the conduct rules that bind the actor without touching the byte predicate.
  So it is a divergence between conforming *files* but not between conforming
  *writers* — the conforming-file set is strictly larger than the
  conforming-writer-output set here, deliberately.
- `[R-IDX-05]`'s all-sentinel-segment constant: a permission to skip a
  computation, never a different byte.

Claims in the reproducible-writer material I tried to falsify and could not:
item 3's "the first structure begins at 16 […] which §5.2 counts as no structure"
(true — §5.2 lists the front block *beside* the structure classes, not among them);
item 2's masking rationale (the ordering key genuinely would be self-referential
without it, and every remaining component is content-derived, so the key is one a
reader can derive); item 3's tie-break exhaustiveness (two records the key does
not separate are byte-identical in type, flags, lengths, payload and extent
content, so either order yields the same file — as it says); item 8's split
between a creator's `flags = 0` and a compactor's carry-forward, which matches
`[R-CNT-08]` and `[R-WRT-06]` exactly.

---

## 6. Findings

### writer-01 — AMBIGUITY — §21.9 `[R-ERR-04]`, §17.2 `[R-COD-07]`'s Note, §19.3 `[R-RDR-03]`

**Does §21.9's per-tile minimum guarantee range over a layer that addresses no
tile?**

§21.9's table row:

> | decoded size of one tile | 256 MiB |

and `[R-ERR-04]`:

> A file exceeding any of these remains conforming, and a reader MAY decline
> it — at the whole file, or at the narrowest scope whose declarations exceed what
> it can serve, a layer or a tile. Software that declines **on that ground** a file
> whose every quantity lies within the table is not a conforming reader
> (`[R-CNF-03]`) […] the guarantees are the floor, not a suggestion.

My layer `empty` declares extent 0 and tile extent 2³¹ with one uint8 channel, so
`P·Q = 2³¹ = 2048 MiB`. §19.3 obliges a reader to derive that quantity at layer
access ("the decoded sizes §14 derives from it (`[R-SER-02]`, `[R-SER-07]`)"), and
§17.2's Note confirms it is computed even here: "P·Q and P·Bᶜ are checked in an
empty layer even though this cap is not". But §11.2 gives the layer zero addressed
tiles and §3.1 defines a tile as "the unit a tile-index entry addresses", so the
layer has no tile whose decoded size could exceed anything.

Two defensible readings:

- **(A) quantified over addressed tiles.** No tile exists, so no quantity of the
  file exceeds the table, and a reader that declines the layer on resource grounds
  "declines **on that ground** a file whose every quantity lies within the table"
  and is therefore **not a conforming reader**.
- **(B) a declaration-derived quantity, addressed or not.** The layer's
  declarations do yield 2048 MiB; §21.9's own text speaks of "a file whose
  quantities lie within these bounds", and `[R-ERR-04]` licenses declining "at the
  narrowest scope whose declarations exceed what it can serve". The reader **may**
  decline the layer and must report it as a resource limit.

I picked (A), on the precedent §17.2's Note sets for `[R-COD-07]` — per-tile caps
are quantified over addressed tiles — and on §3.1's definition of *tile*. The
document draws that quantifier explicitly for `[R-COD-07]`, and explicitly denies
it for `[R-ENC-04]`, and then says nothing about the third member of the family.

**What an implementer does wrong without it.** A writer serving schema-first
workflows (which §11.1's rationale invites: "declare layers at creation, grow
extents as data arrives") has to choose a tile shape before it has any data.
Under (A) it may declare whatever tile shape the eventual data wants — including
one above 256 MiB decoded, which §17.2's Note actively blesses for codec 4 — and
expect every conforming reader to open the file. Under (B) it must keep the
declared decoded size at or below 256 MiB from creation onward or forfeit the
acceptance guarantee, which for a large-tile workload means declaring a tile
shape it will have to change later — and changing tile extents is precisely what
§20.3 step 4 bars once any tile is stored, so the choice is not recoverable.
A reader implementer likewise cannot tell whether refusing such a layer makes it
nonconforming.

**Byte-level: yes.** Reader X validates layer records against a 256 MiB decode
budget and, at §19.3 layer access on `empty`, refuses the layer under `[R-ERR-04]`
reporting a resource limit. Reader Y serves the layer, and every read of it
succeeds returning no samples (`[R-GEO-02]`). Both read the same conforming
1088-byte file; they return opposite verdicts for that layer, and `[R-ERR-04]`'s
final sentence makes exactly one of them a conforming reader without saying which.
This is a *must-accept* fork on a specific byte sequence, not merely a difference
of diagnostics.

### writer-02 — OBSERVATION — Appendix G, §11.3, §14.1/`[R-SER-06]`

**The reproducible-writer profile leaves two writer choices unpinned that it pins
their structural twins.**

Appendix G's preamble:

> Applications that need byte-identical output — content-addressed storage,
> reproducible builds — can adopt this profile, which closes the degrees of
> freedom this format deliberately leaves open.

Item 5's justification for pinning the filter:

> **A fixed filter value** likewise: §17.3 leaves the choice to the writer, it
> changes the stored bytes of every tile it touches, and no content implies it, so
> two writers agreeing on everything else still disagree on bytes without it
> pinned.

That reasoning is verbatim true of two choices no item pins:

- **Tile extents.** §11.3's Note: "Tile extents are a writer's choice, and this
  specification imposes none: the workable range in practice runs from roughly 1
  to 16 MiB of decoded tile […] Tiles far outside that range remain conforming."
  `[R-GEO-01]` bounds them only below (`Tᵢ ≥ 1`) and `[R-CNT-23]` above by the u64
  domain. Tile extents change `N`, `P`, `entry_count`, every index entry, every
  stored tile's bytes, and the layer record.
- **Channel layout.** `[R-SER-06]`: "1 = interleaved and 2 = planar are the only
  values this specification defines and the only values a writer MAY emit."
  §14.4's Note even points out where it changes bytes for identical content: "A
  single-channel numeric layer produces byte-identical tile images under either
  layout. A single-channel bool layer does not — ⌈P/8⌉ packed bytes planar versus
  P bytes interleaved — and both forms are valid." And the layout byte itself
  differs in the layer record even where the tile images do not.

Two writers that adopt every one of Appendix G's ten items, given the same
arrays, still emit different files if one tiles at 256×256 and the other at
512×512, or if one writes a mask planar and the other interleaved. The closing
paragraph's inventory of "what is not [already mandatory]" also omits both (and
omits the filter, though item 5 covers it, so the paragraph is admittedly loose:
"Read the numbered items as the list").

The natural defence is that tiling and layout are part of the *input* rather than
writer freedom. I do not think it survives item 5: alignment, slab, filter, fill
default and `version_minor` are all equally describable as caller options, and the
profile pins every one of them. The drafting convention of the profile is to pin
writer-selectable declarations, and these two were missed.

**Byte-level: no.** Appendix G is explicitly non-normative and "adds no requirement
to any actor: a writer ignoring it is fully conforming", so resolving this changes
no emittable set and no accept/reject verdict. The cost is to an adopter of the
profile, who will believe conformance to it implies byte-identity and find it does
not — which is exactly the failure the profile exists to prevent, and which the
profile itself says "can be refuted cheaply but confirmed only by reproducing the
file".

### writer-03 — OBSERVATION — §21.5 preamble vs §21.6

**§21.5 now names an ignore-record non-violation and, in the same paragraph,
points at a table that does not list it.**

§21.5's preamble (the changed clause is the second `except`):

> User metadata is quarantined (`[R-CNT-25]`): every way its document can be
> unreadable takes this outcome, whatever the containing scope — as a violation in
> the rows below, except at an experimental-range encoding, where no document rule
> attaches and §21.6 records the defined non-violation (`[R-MTA-10]`), and except
> where a reader or verifier declines the decode on the size bound or on the
> frame's declared window, which `[R-MTA-09]` makes that actor's capability and
> not a fact about the file.

and, four sentences later in the same paragraph:

> §21.6 lists the ignore-record conditions that are not violations.

§21.6's table carries exactly two ignore-record non-violations — an
experimental-range record type with MU = 0, and an experimental-range document
encoding — and its closing prose covers the two "conforming files a reader
nevertheless refuses" (a foreign format major, and an experimental-range top-level
type with MU = 1). Neither the table nor that prose mentions the decline. The
first `except` in the sentence above says of its case "§21.6 records the defined
non-violation" and §21.6 does; the second `except` introduces a case §21.6 does
not record, while the closing sentence asserts that §21.6 is where such cases are
listed.

The condition itself is documented — `[R-MTA-09]` states it and `[R-ERR-04]`
supplies the general rule ("A file exceeding any of these remains conforming, and
a reader MAY decline it") — so nothing is undefined. What is wrong is the
signpost: an implementer who builds a defined-non-violations table from §21.6, as
that sentence invites, gets an incomplete one and will class a reader's
bound-decline as a violation. §21.1 does exempt §21.6 from the register's
normative completeness ("neither this completeness clause nor the instance
arithmetic below reaches §21.6's defined non-violations"), which is why I grade
this an observation rather than an ambiguity.

**Byte-level: no.** The decline is a `MAY` on the reader's side either way
(`[R-ERR-04]`), the file is conforming under both the correct and the mistaken
reading, and no writer's output changes. The cost is a mis-classified diagnostic:
a reader reporting "metadata document too large" as corruption rather than as a
resource limit, which `[R-ERR-04]` itself warns "invites the deletion of intact
data".

---

## 7. Things I checked in the changed surface and found sound

Because the charter asked me to cover them first, here is what I concluded about
the two changed passages beyond writer-03.

**§18.2 `[R-MTA-09]`'s verifier clause.** The gap it closes is real: `[R-MTA-04]`'s
four document restrictions and `[R-MTA-05]`'s member ordering are §21.5 and §21.2/3
rows whose *Detector* is **reader** (R5–R10) and **verifier** (F27, L48), all of
which require decoding the document. §2.3 obliges a verifier to check "every
file-level requirement — including those ordinary readers are exempted from", and
§18.2 simultaneously lets a reader pick a decode bound. Without the new sentences a
verifier with a 16 MiB bound meeting a 17 MiB document had a duty it could not
discharge and no verdict to report. The clause routes it to *cannot establish*,
which §2.3's own list already anticipated ("or when it declines to decode a
user-metadata document (`[R-MTA-09]`)"), and correctly subordinates it to the
established-violation priority. I could not construct a case where it conflicts
with `[R-CNF-03]`, `[R-CNF-10]` or `[R-CNF-11]`.

Two smaller things I looked at and decided were not defects:

- "the bound above" is singular where §21.5's new clause names two bounds (size
  and declared window). The nearest antecedent is the window bound, but §2.3's
  generic "declines to decode a user-metadata document" and §21.5's explicit "the
  size bound or on the frame's declared window" triangulate to both. Determinate
  by triangulation, so not reported.
- "because a document has no declared size" is false for encoding 1, where the
  document's size is exactly `extent_length − 4`, a structural field corroborated
  against the file's length by `[R-CNT-13]`. It carries no operational weight:
  the premise is used only to justify the *scope* of an `[R-ERR-04]` decline in a
  **Note** (non-normative per §2.1), and `[R-ERR-04]` itself licenses both the
  whole file and the narrowest scope, so no behaviour forks. Not reported.
- `[R-MTA-09]`'s new "the verifier SHOULD report the bound it applied and the
  stored length of the extent it declined" states no consequence of deviation,
  which §2.1's Note says every SHOULD does. I did not report it: `[R-CNF-11]`
  already makes reporting the unchecked requirement a MUST, so the SHOULD only
  adds detail and the consequence of omitting it — a thinner report — is
  self-evident. Recording it here so the omission is on the record without
  inflating the finding count.

**§21.5's other content.** The clause correctly excepts the decline from *both*
the outcome and the violation status, and correctly leaves R1 intact — "Encoding 0
and a reserved-range value are unassigned too, and R1 registers both as
violations: what `[R-MTA-10]` withdraws is the document's content rules, never the
encoding byte's own value set". I checked that R3's exclusion ("not a failure to
decode within the meaning of R3") does not orphan R4, whose frame constraints are
header-checkable and so survive a decline for a verifier that reads the header;
a verifier that declines before reading the header would owe R4 as a further
unchecked requirement under `[R-CNF-11]`, which is a reporting detail the rule
already covers generically.

---

## 8. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`.
I opened no other file — no `docs/`, no ADRs, no `PLAN.md`, `AGENTS.md`,
`README.md`, no `conformance/`, no `spec/registry.json`, no git history, no web.
I did not list or read the output directory.

I ran only local computation reading no project file: a CRC-32C implementation and
three Python scripts of my own authorship (a builder, a reader/verifier, and an
appender) that construct and re-read a TARN file in a scratch directory, plus one
script that reads `spec/tarn.md` itself to count §21's register rows and instances.

**Context I did not ask for.** Material appeared in my context before I began:
a project instruction file pointing at a contributor guide, and an index of the
maintainer's memory notes naming several topics including prior-round workflow and
a register/corpus relationship. I did not open any file it referenced and did not
use its contents to reach any conclusion; naming its existence here as the brief
requires. Nothing in it informed a finding above — writer-01 came out of building
the `empty` layer, writer-02 out of walking Appendix G item by item against the
choices my builder actually made, and writer-03 out of reading §21.5 and §21.6
side by side.
