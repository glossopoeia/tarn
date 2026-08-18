# Round 11 — Writer implementer, working transcript

**Disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in five passes covering lines 1–3953 (the whole document). I ran `grep`/`sed` against
that same file only, to pull the verbatim quotations below. I ran three Python scripts
I wrote myself in the scratchpad (`crc.py`, `build.py`, `append.py`); they read no files
and produced one scratch artifact, `demo.tarn`. I opened no ADR, no `PLAN.md`, no
`AGENTS.md`, no `conformance/`, no `spec/registry.json`, no git history, and did no web
access. I did not list any project directory. I did not read the round-11 output
directory; I only wrote this file into it.

---

## 0. Method

I built a conforming writer on paper by emitting bytes in the order a real writer would,
stopping every time the document failed to fix a decision. I then appended a generation
to that file, then walked the updater's flag matrix against records I stipulate I do not
understand, then the slack ledger, then four crash points, then the divergence
catalogue against Appendix G.

First, three sanity checks on my own arithmetic, so that later numbers mean something:

| check | computed | document |
|---|---|---|
| CRC-32C(`"123456789"`) | `0xE3069283` | §4.5 — `0xE3069283` ✓ |
| CRC-32C(zero bytes) | `0x00000000` | §4.5 ✓ |
| Appendix A trailer CRC over [0,60) | `0xE00938D2` | Appendix A — `D2 38 09 E0` ✓ |
| CRC-32C of 2¹⁶ sentinel entries | `0xEECB3BB2` | §15.4 / Appendix B ✓ |

All four reproduce. §4.5's parameters (Castagnoli, reflected in/out, init `0xFFFFFFFF`,
final XOR, stored little-endian) are enough to implement the checksum with no external
reference, which is the point of the check vector. No guess here.

I also replayed §21.8's arithmetic by hand before trusting the register: §21.2 declares
36 rows, §21.3 declares 49, §21.4 declares 26, §21.5 declares 10 — 121, matching §21.8's
"121 conditions". Counting instance cells mechanically per §21.1 ("Instances within a
cell are separated by semicolons, and a cell reading — is one instance") gives
F=53, L=106, T=45, R=44 → **248**, matching §21.8's "248 instances" exactly. That is the
one claim in §21 I could falsify cheaply, and it holds. No finding.

---

## 1. Creation: a byte layout, end to end

### 1.1 The file I chose to build

Small, but arranged so that every part of Part I and the awkward corners of Part II are
exercised: two layers of different layout, one edge-padded interleaved layer mixing a
numeric and a bool channel, one packed planar bool layer with both padding positions and
pad bits, one sentinel entry, a declared per-tile alignment on one layer and a slab
declaration on the other, and a file-scope user-metadata record.

**Layer A** — name `A`, interleaved (layout 1), linearization 1, codec 1 (none),
filter 1 (none), alignment A = 512, S = 0, A_slab = 0, rank d = 2, C = 2.
Dimensions in declared order: `y` (E=5, T=4), `x` (E=5, T=4).
Channels: `v` uint16 fill `0xABCD`, `m` bool fill `0x01`.

Geometry per §11.2: Gᵢ = ⌈5/4⌉ = 2 both axes, N = 4, P = 16.
Interleaved → addressed-tile count = N = 4, so `entry_count` = 4.
Sample stride Q = Bᵥ + B_m = 2 + 1 = 3 (§14.2; bool counts as element size 1 in an
interleaved tile, §12.1). Decoded size = P·Q = **48 bytes**.
In-sample offsets Fᵥ = 0, F_m = 2.

**Layer B** — name `B`, planar (layout 2), codec 1, filter 1, A = 0, S = 2, A_slab = 1,
d = 1, C = 1. Dimension `t` (E=10, T=6). Channel `flag` bool fill `0x01`.
G = ⌈10/6⌉ = 2, N = 2, P = 6. Planar → addressed-tile count = C·N = 2.
Planar bool plane → §14.3: decoded size = ⌈6/8⌉ = **1 byte**.

**User metadata** — one top-level record, encoding 1 (none), document
`{"tarn.creator":"walk 1.0","tarn.title":"demo"}` (47 bytes), extent = 47 + 4 CRC = 51.
Members sorted ascending by their keys' UTF-8 bytes per `[R-MTA-05]`:
`tarn.creator` before `tarn.title` because `0x63 < 0x74` at the sixth byte.

### 1.2 Emission order — what the document fixed and what it left to me

`[R-LIF-02]`'s creation path: front block, then steps 2–6 "writing beginning at offset
16, with generation 1". Step 2 is "append new stored-tile payloads and tile-index
regions … **in any order** satisfying §5.2's coverage classes"; `[R-SLB-05]` says the
same from the layer's side. So the order of every payload and index region is **mine**.
The order of the last three things is **the document's**: directory (step 3), then the
barrier, then pad and trailer (step 5). `[R-CNT-05]` independently forbids any structure
between the directory's end and the trailer, so the directory cannot be anywhere but
last among structures. The pad's *length* is also not mine — step 5 says "pad to the next
64-byte boundary", and §6.2 confirms "a writer that ends its directory on a 64-byte
boundary leaves none" and that "a longer gap is conforming, and no conforming commit
produces one". That last clause is the conduct/predicate split of `[R-CNF-02]` applied to
a pad; I read it as binding me while leaving the resulting file conforming either way, on
the model §6.3 uses for `flags = 0`. No guess.

Two placement constraints then bind me:

- `[R-SLB-01]`: every stored tile of layer A satisfies `offset mod 512 = 0`. It binds
  *stored tiles only* — the tile-index region is not a stored tile, so it needs no
  alignment. That is clear from the text and I did not have to guess.
- `[R-SLB-03]`: layer B's slab. §16.2 partitions "each contiguous block of disk
  ordinals independently: … for a planar layer each channel block [c·N, (c+1)·N)". With
  C = 1, N = 2, S = 2, there is one block [0,2) and one run [0,2). Its two stored tiles
  must be contiguous and packed in ordinal order, and the first must satisfy
  `offset mod 1 = 0` (vacuous).

I chose: A's three stored tiles, A's index, B's two tiles, B's index, the metadata
extent, the directory, the pad, the trailer.

### 1.3 The bytes

```
[0,16)        front signature block   89 54 41 52 4E 0D 0A 1A  00 ×8      (§6.1, fixed)
[16,512)      SLACK 496 bytes         forced by A = 512 on the first stored tile
[512,560)     layer A tile ordinal 0  48 bytes, codec 1
[560,1024)    SLACK 464
[1024,1072)   layer A tile ordinal 1  48 bytes
[1072,1536)   SLACK 464
[1536,1584)   layer A tile ordinal 2  48 bytes
[1584,1668)   layer A tile-index region, 84 bytes
[1668,1669)   layer B tile ordinal 0  1 byte
[1669,1670)   layer B tile ordinal 1  1 byte      (packed, run-contiguous)
[1670,1714)   layer B tile-index region, 44 bytes
[1714,1765)   user-metadata extent, 51 bytes (47 doc + 4 CRC)
[1765,2016)   directory region, dir_length = 251
[2016,2048)   SLACK 32 — the pre-trailer pad
[2048,2112)   trailer
F = 2112
```

`[R-CNT-17]`'s index-region length under index_encoding 1 is
`entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4`: layer A → 4·20 + 1·4 = **84** ✓;
layer B → 2·20 + 1·4 = **44** ✓. Both match what I placed.

### 1.4 Tile content — where §14.5 does the real work

Layer A's grid is 2×2 over extents (5,5) with tile extents (4,4), so three of the four
tiles carry padding positions:

| disk ordinal | tile coords | covers | real positions | padding positions |
|---|---|---|---|---|
| 0 | (0,0) | y 0–3, x 0–3 | 16 | 0 |
| 1 | (0,1) | y 0–3, x 4–7 | 4 (x = 4) | 12 |
| 2 | (1,0) | y 4–7, x 0–3 | 4 (y = 4) | 12 |
| 3 | (1,1) | y 4–7, x 4–7 | 1 ((4,4)) | 15 |

Disk ordinal = spatial ordinal s = Σ tᵢ·∏_{j>i} Gⱼ for an interleaved layer
(`[R-GEO-06]`), so ordinal 1 is (0,1) and ordinal 2 is (1,0). Fully determined.

I made ordinal 3 the **sentinel** — 20 bytes `FF ×16 00 ×4` (§15.2). Note that (4,4) is a
real position of the reference array, so it reads as the full fill sample
(v = 0xABCD, m = true) per `[R-TYP-08]` and §19.4 step 4. That is legal: nothing obliges a
writer to store a tile merely because it contains real positions. Appendix G item 6 would
*require* the sentinel here only if every sample equalled fill; it does not, so the choice
is mine even under the profile — no, correction, under the profile it is mine only because
the tile is not all-fill; had it been all-fill the profile would force the sentinel.

Padding content is **not** mine. `[R-SER-05]`:

> "at every padding position, a writer MUST encode, for each channel the position
> carries, that channel's fill value — the recorded fill bytes for a numeric channel, the
> recorded fill byte for an interleaved bool channel, the fill bit in a packed plane.
> Every pad bit (§14.3) MUST carry the plane's channel's fill bit."

So in ordinal 1, the twelve padding samples are each the three bytes `CD AB 01`, laid out
by §14.2's arithmetic: sample at in-tile ordinal u occupies `[3u, 3u+3)`, `v` at `3u`
little-endian, `m` at `3u+2`. I verified my emitter against §14.2's own worked example
(channels `a` uint8 + `b` uint16, tile extents (2,3): Q = 3, decoded size 18, ordinal 5's
sample at bytes [15,18)) — same arithmetic, same answer.

Layer B is where the packed rules bite. P = 6, so `⌈P/8⌉ = 1` byte per plane, and
`P mod 8 = 6 ≠ 0`, so **bits 6 and 7 of that single byte are pad bits** and must carry the
fill bit (= 1). Tile ordinal 1 additionally covers global coordinates t = 6…11, of which
t = 10 and t = 11 are **padding positions** (outside E = 10) and must carry the fill bit
too. With my chosen values:

- ordinal 0 (t = 0…5, values T,F,T,F,T,F): bits 0–5 = `010101`, pad bits 6–7 set
  → byte `0xD5`.
- ordinal 1 (t = 6…9 = F,F,T,T; t = 10,11 padding = fill 1; pad bits 6,7 = fill 1)
  → bits `0,0,1,1,1,1,1,1` LSB-first → byte `0xFC`.

Both computed by my emitter. I cross-checked the mechanism against §14.3's own example
(P = 10, alternating, fill false → `55 01`; fill true → `55 FD`) and got the same rule.
The distinction §14.3's note draws — pad bits are not padding positions, and a plane can
have many padding positions and no pad bits — is exactly the distinction I needed here,
and it is stated. No guess.

### 1.5 Index regions

Entry layout (§15.1): `offset` u64, `length` u64, `crc` u32 = 20 bytes, entry k at region
byte 20k in disk-ordinal order. Layer A's four entries:

```
ord 0: offset 512  len 48  crc 0x254BEE46
ord 1: offset 1024 len 48  crc 0x280558E8
ord 2: offset 1536 len 48  crc 0x66059462
ord 3: FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF  00 00 00 00
```

Under codec 1, `[R-COD-04]` forces `length` = decoded size = 48 for every stored tile. So
the entry `length` field is not a writer choice for this layer at all. Layer B's entries
are `(1668, 1)` and `(1669, 1)`, `length` = ⌈P/8⌉ = 1, again forced.

Segments (§15.4): entry_count 4 → one segment covering entries [0,4), CRC over exactly
those 80 bytes → `0x5F7C2DE7`; the segment CRC array is that single u32; then
`crc_of_crc_array` = CRC over the 4-byte array = `0xFE3F12FF`. Layer B:
segment CRC `0xA17AD5AD`, `crc_of_crc_array` `0xCF96C3DE`.

Note the ordering dependency I had to resolve: `crc_of_crc_array` lives in the layer
record, whose size is fixed regardless of the value, so there is **no circularity** —
place structures, compute entries, compute segment CRCs, compute `crc_of_crc_array`,
then serialize the directory, then the trailer. The document does not spell this out but
the field widths make it forced.

`[R-IDX-05]`'s all-sentinel shortcut does not apply here (my segments are partial, and
"a partial segment's CRC MUST be computed"). I computed them.

### 1.6 Layer record inline payloads

§7.4 fixes the field order and `[R-CNT-18]` fixes the packing ("fields are packed in
table order with no alignment or padding between them"), so the inline payload is
completely determined once the declarations are:

```
layer A: 01 'A' | 01 | 01 00 | 01 00 | 01 00 | 00 02 00 00 00 00 00 00 |
         00×8 | 00×8 | 02 | 02 00 |
         01 'y' <5:u64> <4:u64> | 01 'x' <5:u64> <4:u64> |
         01 'v' 07 00 02 CD AB | 01 'm' 01 00 01 01 |
         01 | <4:u64> | FF 12 3F FE
inline_length = 98
```

Fixed head = 2+1+2+2+2+8+8+8+1+2 = 36; two dimension entries at 18 each = 36;
channel `v` = 7, channel `m` = 6 = 13; tail = 1+8+4 = 13. 36+36+13+13 = **98** ✓.
Layer B by the same arithmetic = **76**.

Fill length is not mine: "fill length equals the type's element size (`[R-CNT-23]`)".
uint16 → 2 bytes `CD AB`; bool → 1 byte, and `[R-TYP-07]` restricts it to `0x00`/`0x01`.
I checked my channel-entry encoding against §12.3's worked example
(`04 74 65 6D 70 0C 00 04 00 00 C0 7F`) — same field order, same prefix widths.

Record headers (§7.2): 24 bytes, `type`/`flags`/`inline_length`/`extent_offset`/
`extent_length`. §7.3 fixes the flags: layer → MU=1, PE=1 → `flags = 0x0003`;
user metadata → MU=0, PE=1 → `flags = 0x0002`. "writers MUST emit exactly the flag values
fixed in the table above" — so `flags` is not a writer choice either. Reserved bits 2–15
zero.

Record sizes: 24+98 = 122, 24+76 = 100, 24+1 = 25 → sequence 247 bytes, plus the
region's terminal CRC-32C → **dir_length = 251**, `dir_offset = 1765`.
`dir_offset + dir_length = 2016 ≤ F − 64 = 2048` ✓; `dir_offset ≥ 16` ✓;
`dir_length ≥ 4` ✓.

Record **order** inside the sequence is free (`[R-CNT-14]`: "Record semantics MUST NOT
depend on record order"). I emitted A, B, metadata; any permutation is equally
conforming. That is divergence item D7 below.

### 1.7 Pad and trailer

Directory ends at 2016, already 64-aligned → pad = 32 to 2048? No: 2016 mod 64 = 32, so
the next 64-byte boundary is 2048 and the pad is **32 bytes**. Trailer at [2048, 2112),
F = 2112, F mod 64 = 0 ✓.

Trailer fields (§6.2), every one of which is fixed by the document except `file_id`:

```
magic 8A 4E 52 41 54 0D 0A 1A
version_major = 1        (§6.2 valid values: 1)
version_minor = 0        ([R-CNT-26]: lowest minor defining every feature present → 0)
flags = 0                ([R-CNT-08]: "a writer creating a file under this text MUST
                          write flags = 0")
generation = 1           (creation)
dir_offset = 1765
dir_length = 251
committed_file_length = 2112
file_id = 0x9E3779B97F4A7C15   ← the ONE free field; §9.3 SHOULD draw it randomly
reserved = 00 00 00 00
crc = CRC-32C over [0,60) = 0x3094904D
```

That is the whole creation. **Everything except `file_id`, the choice of which tiles to
store, the placement/ordering of structures, and the record order was fixed by the
document.** I did not have to guess once during creation.

### 1.8 Coverage and slack at generation 1

Live claimants per §5.2 (front block; stored-tile extents; record extents — which
includes each layer's tile-index region, since §9.7 says "A layer record's extent slot
addresses that layer's tile-index region (§7.4), so the region enters the walk once, as
that record's extent"; the directory; the trailer):

16 + 3·48 + 84 + 2·1 + 44 + 51 + 251 + 64 = **656 bytes** live, of F = 2112.
**Slack = 1456 bytes**, in four runs: [16,512) = 496, [560,1024) = 464,
[1072,1536) = 464, [2016,2048) = 32.

Every one of those bytes except the 32-byte pad is forced by my own `A = 512`
declaration — a good illustration of §16.1's "The bytes alignment leaves between
structures are slack (§5.2), which writers SHOULD zero and no conformance requirement
constrains". I zeroed them per `[R-CNT-03]`. 69% of this file is slack the moment it is
created, and a verifier must report that number (`[R-CNT-21]`: "a verifier MUST report
the total number of slack bytes, since that number is what tells an operator to
compact"). That is a correct but slightly alarming signal on a freshly created file, and
the document does not distinguish "slack from alignment I asked for" from "slack from
superseded data". `[R-CNT-21]` reports one number. I note this as a design consequence,
not a defect — §5.2's rationale explicitly declines to attribute slack.

---

## 2. Append: generation 2

Instruction: supersede layer A's tile ordinal 1, and store ordinal 3 (currently the
sentinel). Nothing else changes.

### 2.1 The procedure, step by step

**Step 1 — Establish F** (`[R-LIF-04]`). Validate the trailer in the final 64 bytes of
the *physical* file. It validates → F = 2112, and because `[R-CNT-06]` includes
"committed_file_length equals the file size", passing this check also proves there is no
residue. §9.4's second sentence ("a writer whose physical file is longer than F MUST
either truncate to F … or overwrite from F") therefore only ever applies on the recovery
path, which is consistent but reads as if it could apply on the direct path. Not a
defect; I re-read it twice.

**Step 2 — Open** (§19.1). Four steps: F; trailer; directory fetch + CRC; record walk.
Note what the open does **not** touch: "It consumes the trailer and directory only — no
extent slot's content, no tile index, no payload" (`[R-RDR-01]`). This matters below.

**Step 3 — Validate what the commit touches** (`[R-WRT-03]`): trailer and full directory
always ("re-emission (§20.4) relies on every directory byte"), plus §19.3's layer
validation for layer A, plus the §19.4 index chain — `crc_of_crc_array` and the segment
CRC — "for every segment whose entries the commit reuses". Layer A has one segment and
I reuse entries 0 and 2 from it, so I verify `0xFE3F12FF` over the 4-byte array and
`0x5F7C2DE7` over the 80 entry bytes. Layer B I neither modify nor rely on: **no
obligation at all**, not even its index chain. I do not verify any stored tile's payload
CRC — that is a compactor's job (`[R-WRT-09]`), not an appender's.

**Step 4 — Write payloads and indexes.** Writing begins at exactly F = 2112.
`A = 512` still binds: next multiple of 512 ≥ 2112 is **2560**.

```
[2112,2560)   SLACK 448   alignment gap
[2560,2608)   layer A tile ordinal 1, new bytes
[2608,3072)   SLACK 464   alignment gap
[3072,3120)   layer A tile ordinal 3, new bytes
[3120,3204)   layer A tile-index region, re-emitted whole (84 bytes)
[3204,3455)   directory, 251 bytes
[3455,3456)   SLACK 1     pre-trailer pad
[3456,3520)   trailer, generation 2
F₂ = 3520
```

The whole index region moves even though only two of four entries changed — §20.3 step 4
and §20.3's example (b) are explicit, and §5.1's figure says the same. Entries 0 and 2
are copied byte-identically at their disk-ordinal positions; entry 1 gets its new
offset/length/crc; entry 3 stops being the sentinel. `entry_count` is unchanged (geometry
unchanged), so no ordinal renumbering (`[R-GEO-06]`).

The old index region at [1584,1668) is *not* reused and *not* relocated — "A commit never
relocates a live index region otherwise; that is compaction's operation" (§5.1). It
becomes slack.

**Step 5 — Re-emit the directory.** Layer A's record changes in exactly two fields:
`extent_offset` 1584 → 3120 and `crc_of_crc_array`. Layer B's record and the metadata
record are re-emitted **byte-identically**, extent slots and all (`[R-WRT-05]`). The
metadata extent at [1714,1765) is untouched and stays live.

**Step 6 — Commit**: barrier; pad; trailer with `generation = 2`, the **same** `file_id`,
`committed_file_length = 3520`, unknown ignore-lane bits copied forward (none here),
`version_minor` = max(floor, prior) = 0 (`[R-CNT-26]`); barrier.

### 2.2 Slack ledger for this commit

| becomes slack | range | bytes |
|---|---|---|
| superseded layer A tile ordinal 1 | [1024,1072) | 48 |
| superseded layer A index region | [1584,1668) | 84 |
| superseded directory | [1765,2016) | 251 |
| superseded trailer | [2048,2112) | 64 |
| new alignment gap | [2112,2560) | 448 |
| new alignment gap | [2608,3072) | 464 |
| new pre-trailer pad | [3455,3456) | 1 |
| (the old pre-trailer pad [2016,2048) was already slack — not double counted) | | 0 |

Added: 1360. Prior: 1456. Total at generation 2: **2816** = F₂ (3520) − live (704) ✓ —
the two computations agree, which is the check that my class assignment is right.

Live at generation 2 = 16 + 4·48 + 84 + 2 + 44 + 51 + 251 + 64 = 704.

Note what did **not** become slack: layer B's tiles, index and record; the metadata
extent; layer A's tiles 0 and 2. A commit's slack is bounded by what it re-emits, and
§20.3's note quantifies the dominant term correctly ("editing one sample of a 10⁶-tile
layer appends about 20 MB of index and leaves as much slack").

### 2.3 Slack by commit shape — the full answer

| shape | bytes that become slack | who counts them | permitted content |
|---|---|---|---|
| **append (new layer)** | the previous directory, its pad, its trailer; plus any new alignment/slab gaps | verifier only (`[R-CNT-21]`, §9.7); readers never walk it | unconstrained (§5.2: "its content is unconstrained, and no conformance requirement applies to it"); writers SHOULD zero (`[R-CNT-03]`) |
| **append (tiles added / superseded)** | above, plus that layer's whole prior index region, plus every superseded payload | same | same |
| **in-place update** | *does not exist.* `[R-LIF-01]` freezes [0,F); the only in-place writing the format permits is over bytes beyond F (`[R-LIF-04]`), which are not committed | — | — |
| **directory-only change** (rename, clear a slab, fill change on a layer with no padding position and no pad bit) | prior directory + pad + trailer only, "sized by the file's *layer count*, never by any layer's data" (§20.3 example (a)) | same | same |
| **whole-file rewrite under a new file_id** (§20.4's "producer that wants a file without a layer") | none in the new file beyond alignment gaps and the pad; the *old* file persists untouched | verifier of the new file | same |
| **compaction** | none carried from the input; the output still carries every gap its layers' own alignment/slab declarations force, plus the pre-trailer pad | verifier of the output | same |
| **abandoned partial write** | *none* — those bytes never enter any committed state. They are either truncated away or overwritten (`[R-LIF-04]`), and until then the file is nonconforming, not slack-bearing | nobody; §9.5's note: "Residue past a completed commit carries no register row of its own" | — |

The compaction row deserves the concrete number. Compacting my generation-2 file:
layer A still declares `A = 512` and a compactor may not change it — `[R-WRT-07]` lets it
re-point extent slots, regenerate relocated index regions and update `crc_of_crc_array`,
and nothing else. So the four stored tiles must land at 512, 1024, 1536, 2048; the index
can follow immediately at 2096 (not a stored tile); B's tiles pack; the directory ends at
2528; pad 32; trailer [2560,2624); F = 2624.

Live = 704. **Slack in the compacted output = 1920 bytes (73%)**, of which 1888 is
alignment gap and 32 is the pad. §20.5's "so slack is never carried" is about *carrying*,
and is true; it does not promise a slack-free output, and the example figure — which shows
an output with no ▓ — is drawn for a layer with no alignment declaration. I checked
whether a compactor may drop the declaration to reclaim: it may not, because the layer
record is retained and `[R-WRT-05]` requires byte-identical re-emission except for
`[R-WRT-07]`'s enumerated exceptions. Determined; no guess.

---

## 3. Appending to a file whose records I do not all understand

Stipulate my updater implements types `0x0001` and `0x0002` and nothing else. I walk
every flag combination the document defines: bit 0 = MUST_UNDERSTAND, bit 1 =
PRESERVE_ON_EDIT, bits 2–15 reserved (§7.2), bit 0 being the LSB (§4.4).

| # | where | type | stored MU | stored PE | what my updater is permitted to do |
|---|---|---|---|---|---|
| 1 | top level | `0x0001` layer (implemented) | — | — | §7.3's registry flags govern, not the stored bits (`[R-CNT-22]`, §20.4). MU=1/PE=1 fixed. May **modify** the record (it becomes new output under `[R-CNF-05]`); may **not drop** it — §20.4: "No commit therefore removes a layer record". |
| 2 | top level | `0x0002` user metadata (implemented) | — | — | Registry MU=0/PE=1. May modify (new extent appended, old becomes slack — §20.3 example (c)); may not drop. |
| 3 | top level | unimplemented | 1 | 1 | **No commit at all.** `[R-CNT-15]` makes an unimplemented top-level MU=1 record reject-file; §20.3 step 2 says reject-file "bars every commit"; §20.4's MU=1 row says the same and adds that compaction is barred (`[R-WRT-06]`). |
| 4 | top level | unimplemented | 1 | 0 | Identical to #3: `[R-CNT-12]` — "a reader or updater encountering it MUST treat the record as PE = 1". The stored PE=0 is a writer violation whose detector is the verifier; I neither repair nor act on it. |
| 5 | top level | unimplemented | 0 | 1 | Retain byte-identical, **extent content unmodified**. I may not relocate the extent: `[R-WRT-08]` permits relocation "only … under §20.5", i.e. compaction. |
| 6 | top level | unimplemented | 0 | 0 | Retain byte-identical, **or** drop it (extent → slack) — but only in a commit that *independently* changes "the file's layer set or another *non-layer* top-level record". My commit supersedes a tile, which §20.4 explicitly excludes ("a commit whose only change is a supersede MUST retain the record"). So here: **retain**. Adding a layer would license the drop. |
| 7 | top level | any | any | any | reserved bits 2–15 nonzero: readers MUST ignore them, the verifier owns detection (F26). I re-emit them byte-identically — §20.3 step 2 forbids repair. |
| 8 | layer sub-record | unimplemented | 1 | 1 or 0 | reject-**layer**, never reject-file (`[R-CNT-18]`). That layer becomes unmodifiable; every other layer stays editable, and I still re-emit the layer's record byte-identically into the new directory. |
| 9 | layer sub-record | `0x0002` (implemented) | — | — | Registry MU=0/PE=1; may modify, may not drop (Appendix H: "never removes a layer record, or a user-metadata record at either scope"). §20.4's body sentence names only the *file-scope* metadata record, but the governing clause — "both registered types carry PE = 1, so neither can be dropped" — covers the sub-record too. |
| 10 | layer sub-record | unimplemented | 0 | 1 | Retain byte-identical, extent unmodified. |
| 11 | layer sub-record | unimplemented | 0 | 0 | Droppable only if the commit independently changes "that layer's record, the entry set of its index, or which of its tiles are stored". My commit changes which of layer A's tiles are stored (ordinal 3 becomes stored) — so for a sub-record of **layer A** the drop is licensed; for a sub-record of layer B it is not. |

Two places where I had to reason rather than read:

- **Case 6, "the file's layer set".** Does renaming a layer change the layer set? Layers
  are identified by name (`[R-ENC-15]`), so a rename changes the set of names. I picked
  **no**: §20.4 lists "that layer's record" as a licensing change for a *sub-record*
  drop but not for a top-level drop, so the asymmetry is deliberate and "layer set"
  means membership, not record content. Adding a layer licenses; renaming one does not.
- **Case 6, mutual bootstrapping.** Two top-level MU=0/PE=0 records X and Y: dropping Y
  is literally "a change to another non-layer top-level record", which would license
  dropping X, and vice versa, so a commit whose only effect is both drops would
  self-license. The word *independently* is what forecloses it — neither change is
  independent of the other — and §20.4's "a commit whose only effect would be the drop
  MUST retain it" points the same way. I picked: **not licensed.** I did not raise this
  as a finding because the adverb decides it.

### 3.1 Write order, durability, commit point

`[R-LIF-02]`, unambiguous and I did not have to guess anywhere:

1. begin at exactly F;
2. payloads and index regions and record extents, any order;
3. the complete directory + its CRC;
4. **barrier** — steps 1–3 durable;
5. pad to the next 64-byte boundary + the trailer;
6. **barrier** — trailer durable.

Two barriers, not one (§20.2 says so in as many words: "`[R-LIF-02]` steps 4–6 — both
barriers, not one"). The **commit point** is step 6: the moment the trailer's 64 bytes
are durable at the physical end of a file whose length equals the trailer's
`committed_file_length`. There is no atomicity primitive for the 64-byte write; the
trailer CRC over [0,60) is what converts a torn trailer into a loud failure rather than a
silent one. Where a truncation is owed (`[R-LIF-04]`, the overwrite-from-F path), the
commit point moves to the truncation, which must happen "no later than step 6".

---

## 4. Torn-write recovery — four crash points

Throughout: `[R-LIF-05]` is the reader's whole story — "a reader that finds no valid
trailer in the final 64 bytes MUST report the file torn or invalid and MUST NOT scan
backward."

**Crash 1 — after the front block only (creation).** File is 16 bytes.
*Next reader:* F = 16 < 128 → `[R-CNT-27]` / F5, reject-file; also no trailer (F8).
*Next updater:* `[R-LIF-04]` step 1 fails → torn → MUST NOT append.
*Recovery (§9.6):* "The probe begins at the largest 64-aligned offset o with
o + 64 ≤ the physical file length" — for a 16-byte file no such o exists, so the probe
enumerates nothing and there is no commit state. The document does not say in words what
a recovery tool reports when there is no candidate; it does say the tool "MUST report the
candidate it settled on and how many it rejected", which reduces to "none, zero". I did
not treat this as a defect.
*Conforming?* No.

**Crash 2 — mid step 2, after two of the three new payloads.** Physical length is
2560+48 = 2608, say.
*Next reader:* final 64 bytes are payload bytes → magic mismatch (F8) → reject-file,
and it must not scan backward.
*Next updater:* torn → no append.
*Recovery:* probe backward from the largest 64-aligned o with o+64 ≤ 2608 → o = 2544
fails, … → lands on o = 2048, the generation-1 trailer, whose CRC verifies and whose
`committed_file_length = 2112 = o + 64` ✓. Truncate to 2112 → the file is exactly
generation 1, bit for bit, because no committed byte was modified. Then re-verify whole
(§9.6's first normative caution) before trusting it.
*Conforming in the meantime?* No — F8, and also F17 if the tail happened to look like a
trailer.

**Crash 3 — after step 4's barrier, before the trailer.** The directory is durable at
[3204,3455) but there is no trailer.
*Next reader:* identical to crash 2 — the physical tail is directory bytes. F8.
*Recovery:* same, truncate to 2112. Everything commit 2 wrote is discarded, including a
fully durable directory. This is the price §9.2's figure names: "Mid-commit the physical
tail is not a trailer, so a reader on the default path reports the file torn".
*Conforming?* No.

**Crash 4 — during the trailer write.** Two sub-cases and they behave differently, which
is worth stating because a writer has to know:
 (a) the file grew to F₂ = 3520 but only part of the 64 trailer bytes landed. If the
 magic landed, the reader gets past F8 and fails the trailer CRC (F14). If it did not,
 F8. Either way reject-file.
 (b) the file grew to less than 3520 — final 64 bytes straddle pad and partial trailer →
 F8.
There is no sub-case in which a partially written trailer is accepted, because the CRC
covers every one of bytes [0,60). *Recovery:* probe finds o = 3456 only if the full
trailer is there; otherwise it walks back to 2048.
*Conforming?* No.

**Crash 5 (bonus, the one that matters) — weak barriers.** Trailer durable, directory
not. The physical tail *is* a valid trailer, `committed_file_length` matches, every §6.2
gate passes — and then the directory CRC fails (F20, reject-file). The prior state looks
lost, but §9.6 recovers it: the probe settles on the nearest-to-end valid candidate,
"a candidate whose whole-file re-verification fails was not a commit state, so the tool
continues the probe past it" — landing on trailer₁ at 2048. This is the case that
justifies §9.6's re-verification requirement, and the document handles it correctly.

**Crash 6 — after the trailer, before the owed truncation.** Only reachable on the
`[R-LIF-04]` overwrite-from-F path when the pre-existing physical file was longer than
the new `committed_file_length`. Reader: F17 (size ≠ committed_file_length) → reject-file.
Recovery: probe finds the new trailer, `committed_file_length = o + 64` ✓, truncate → the
new generation, intact. So the crash costs nothing but a recovery run.

Across all six: **the file is never conforming during a torn commit**, and the previous
state is always byte-recoverable. That is exactly the claim §1 and §9.2's figure make,
and I could not construct a counterexample.

---

## 5. Byte-divergence catalogue

Two conforming writers, identical input arrays, identical stated options (same layers,
names, dimensions, tile extents, channel types, fills, layout, codec, filter, alignment
and slab declarations, same metadata document as a decoded JSON value). Every way their
bytes may legitimately differ, and whether Appendix G closes it.

| # | degree of freedom | rule that licenses it | Appendix G |
|---|---|---|---|
| D1 | Order of structures within step 2 | `[R-LIF-02]` step 2 "in any order"; `[R-SLB-05]` | **closed** — item 3's total emission order |
| D2 | Gap *extent* between structures | `[R-SLB-05]` placement freedom | **closed** — item 3, "Each structure begins where the previous one ended" |
| D3 | Gap *content* (slack bytes) | `[R-CNT-03]` is a SHOULD; §5.2 "content is unconstrained" | **closed** — item 3, "every byte of every such gap is zero" |
| D4 | `file_id` | §9.3, any nonzero value | **closed** — item 2 |
| D5 | `version_minor` | `[R-CNT-26]` is a SHOULD; §21.6 accepts any higher minor | **closed** — item 8 |
| D6 | Ignore-lane `flags` bits | `[R-CNT-08]` makes a set ignore-lane bit not a file-conformance violation | **closed** — item 8, `flags` = 0 |
| D7 | Record order in the directory | `[R-CNT-14]` | **closed** — item 3 |
| D8 | Sub-record order in a layer record's inline payload | `[R-CNT-14]` | **closed** — item 3 |
| D9 | Codec 2/3/4 encoder output for identical input (block/match/table choices; DEFLATE's up-to-7 unconstrained final-byte bits, §17.2's note; zstd's optional Frame_Content_Size) | `[R-CNF-05]` | **closed only by pinning the producer** — item 1, which admits byte-identity across implementations is unattainable |
| D10 | Which all-fill tiles are stored vs. sentinel | nothing requires an all-fill tile to be unstored | **closed** — item 6 |
| D11 | Fill recorded when the caller chooses none | `[R-TYP-10]` is a SHOULD | **closed** — item 7 |
| D12 | Number of generations | nothing requires one commit | **closed** — item 4 |
| D13 | Whether A / S / A_slab are declared at all | §16 | **closed** — item 5 (and it is a stated option here anyway) |
| D14 | JSON serialization of a fixed decoded document (whitespace, escapes, number formatting) | `[R-MTA-05]` fixes member *order* only | **closed** — item 9, by pinning the JSON writer |
| D15 | User-metadata **encoding** (1 = none vs 2 = zstd) and, under 2, the zstd encoder's byte output | §18.2 assigns both; nothing prefers one | **open** — see finding writer-04 |
| D16 | Unicode normalization form of a caller-supplied name | `[R-ENC-14]` is a SHOULD ("Writers SHOULD emit names in Unicode Normalization Form C"), and §4.6's example shows the two forms are 12 vs 13 different bytes | **open** — see finding writer-04 |
| D17 | Placement phase of a layer sub-record's user-metadata extent under the profile | item 3's own wording | **ambiguous within the profile** — see finding writer-05 |

D1–D14 are legitimate divergences and the profile closes each (D9 only in the weak sense
it admits). D15 and D16 are legitimate divergences the profile leaves open despite its
preamble's claim to close "the degrees of freedom this format deliberately leaves open".
D17 is not a divergence in the format at all — it is an underdetermination *inside* the
profile.

I also checked the profile's closing summary against its own items, and it does not hold
up (finding writer-03).

One divergence I looked for and did **not** find: the segment-CRC shortcut of
`[R-IDX-05]` cannot produce a divergence, because the licensed constant `0xEECB3BB2` is by
construction equal to the computed value (I verified it above), and the licence is
restricted to full segments.

---

## 6. Findings

Six findings. Each quotes the text it complains about.

---

### writer-01 — CONTRADICTION — §4.7 `[R-ENC-16]` vs §14.5 `[R-SER-05]` and §13.1

§4.7 defines the taxonomy and then makes a closed claim about the document's own
contents:

> "A field is **structural** if its value determines anything a conforming reader or
> verifier does with the file's bytes — where a byte lies, how it decodes, or whether the
> file, layer or tile is accepted at all … In format major 1 `fill` is the
> only semantic field and `version_minor` the only descriptive one: every other field
> this specification defines is structural. `[R-ENC-16]`"

§14.5 makes a verifier's acceptance of a *tile* turn on the value of the `fill` field:

> "at every padding position, a writer MUST encode, for each channel the position
> carries, that channel's fill value … a verifier MUST check it, and a violation is a
> validity error at tile scope. `[R-SER-05]`"

These cannot both stand. In the file I built, layer A's channel `v` records fill
`0xABCD`, and tile ordinal 1 carries twelve padding positions whose stored bytes are
`CD AB`. Change **only** the two fill bytes in the layer record — leaving every payload
byte, every index entry and every checksum-covered region otherwise as it was and
recomputing only the covering CRCs — and the twelve padding samples no longer encode the
recorded fill, so a verifier must record a tile-scope violation (§21.4 row T4). The value
of `fill` therefore "determines … whether the … tile is accepted at all", which is
§4.7's own criterion for **structural**. `fill` is not semantic under §4.7's definition,
so the claim that it is "the only semantic field" is false, and §4.7's stronger claim
that format major 1 has exactly one semantic field is false with it.

§13.1 restates the misclassification with a gloss that quietly omits the failing leg:

> "The fill value is semantic (§4.7): it affects what unstored samples read as, never how
> any byte is located or decoded"

— true as far as it goes, and it is precisely the acceptance leg that §4.7 added to the
definition which §13.1 does not address.

A second, smaller consequence: because `fill`'s acceptance effect exists only in a layer
that has padding positions or pad bits, §4.7's criterion classifies the *same field* as
structural in one file and semantic in another, which a taxonomy of fields cannot express.

**Reading I picked as an implementer:** I treated `fill` as structural in practice —
I recompute padding content whenever a fill changes, which is what §20.3's example (c)
already tells me to do ("A fill change on a layer carrying either additionally requires
re-emitting the affected stored tiles, whose content `[R-SER-05]` fixes"). Nothing in my
writer branched on the taxonomy label.

**Byte-level: no.** No normative requirement branches on the structural/semantic
distinction. §4.7 attaches a MUST only to the *descriptive* class ("a reader MUST NOT
alter decoding based on it"), and the other uses of "structural" (`[R-CNT-07]`,
`[R-MTA-02]`, `[R-SEC-06]`) are about user metadata never being structural, not about
`fill`. Classifying `fill` either way yields identical reader, writer and verifier
behaviour and identical bytes. What is wrong is the document's claim about itself.

---

### writer-02 — CONTRADICTION — §20.3 `[R-WRT-04]` step 2 against step 4 (and `[R-WRT-03]`)

Step 2 of the append procedure:

> "A violation the open establishes bars the commits its outcome bars and no others:
> reject-file bars every commit, reject-layer bars a commit that modifies that layer,
> reject-tile bars reuse of that entry."

Step 4 of the same requirement:

> "Every layer whose stored-tile set or index content this commit changes has its
> tile-index region re-emitted in full … with entries for tiles this commit stores or
> supersedes written to their new state, entries for tiles that become unstored written
> as the sentinel, entries new to this generation (added tiles, grown extents) emitted
> per §15, and **every other entry byte-identical at its disk-ordinal position**"

And `[R-WRT-03]` fixes what "reuse" means in this section:

> "and the §19.4 index chain for every segment whose entries the commit **reuses**
> (`[R-IDX-04]`)"

There, "reuses" can only mean "copies forward into the new index region", because that is
the only thing a commit does with entries it does not change. Apply the same sense in
step 2 and the two steps are irreconcilable for a concrete file.

**Concrete case.** Layer A of my file, but with entry ordinal 2 malformed: non-sentinel
`offset = 1536`, `length = 0`. §15.3 classifies that *structural*: reject-tile
(§21.4 row T10, detector reader). Now issue my generation-2 commit, which stores a new
tile at ordinal 3 and therefore must re-emit the whole index region. Step 4 obliges me to
write entry 2 byte-identically at its disk-ordinal position. Step 2 bars me from reusing
it. There is no third value I may write: the sentinel would be a repair, and step 2's
next sentence forbids repair ("it MUST NOT repair the defect"), while §20.3 step 4's own
text names the sentinel only for "tiles that become unstored", which this tile is not.

**The permitted readings.**
(a) *"Reuse" means copy-forward* (the sense `[R-WRT-03]` uses). Then no commit that
touches layer A's index is ever possible again, and since a compactor must also refuse
(`[R-WRT-06]`: "MUST refuse to compact when any check `[R-WRT-09]` obliges fails"), the
layer is permanently frozen by one bad entry.
(b) *"Reuse" means relying on the entry to read its tile.* Then step 4 governs, I copy
the 20 bytes verbatim, the commit succeeds, and I "SHOULD report it" as step 2's closing
sentence contemplates — which is the only reading under which that sentence has work to
do.
(c) *The clause is dead text.* Step 2 conditions the bar on "a violation **the open**
establishes", and §19.1's open provably cannot establish a reject-tile: `[R-RDR-01]` says
the open "consumes the trailer and directory only — no extent slot's content, no tile
index, no payload." No reject-tile row in §21.4 is detectable from those bytes. Under
this reading the reject-tile clause names an outcome its own trigger can never produce,
step 4 governs unopposed — and nothing at all governs the appender that *does* classify
the entry, which `[R-CNF-12]` expressly licenses it to do.

**Which I picked:** (b), because it is the only reading under which step 2's final
sentence ("An appender that carries a violation forward SHOULD report it, and a caller
that is not told cannot know the file it extended was already damaged") is not dead
letter. But I had to guess, and reading (a) is the one `[R-WRT-03]`'s vocabulary
supports.

**Byte-level: yes.** Implementation P classifies each entry per §15.3 as it copies the
segment forward — licensed by `[R-CNF-12]`'s "A reader MAY detect any violation earlier"
— finds entry 2 reject-tile, applies step 2, and emits **nothing**. Implementation Q
applies step 4, and emits a complete generation 2: the new stored tile at 3072, the
84-byte index region at 3120 containing entry 2's original 20 bytes verbatim, the
251-byte directory at 3204, the pad, and the 64-byte trailer at 3456. Those are ~700
bytes that either are or are not a byte sequence a conforming updater may emit, and the
document does not decide which. The divergence is not covered by `[R-CNF-05]`'s licence
for writers to differ, because the question is not *which* conforming file to produce but
whether producing one at all is permitted.

---

### writer-03 — CONTRADICTION — Appendix G's closing paragraph against Appendix G items 6 and 8

The profile's closing paragraph enumerates, exhaustively, what the profile adds beyond
what is already mandatory:

> "Everything else the profile needs is already mandatory — fill-encoded edge padding
> (`[R-SER-05]`) and explicitly recorded fill (`[R-TYP-06]`) among them. **Four things are
> not**, and the items above are where the profile adds them: gap *content*, which
> `[R-CNT-03]` only advises; gap *extent*, which placement freedom (`[R-SLB-05]`) leaves
> open; sub-record order within a layer record's inline payload, which `[R-CNT-14]`
> leaves free; and the fill a writer records when its caller chooses none, which
> `[R-TYP-10]` states as a SHOULD."

Two of the profile's own numbered items add things that are not already mandatory and are
not among those four.

Item 8:

> "**`version_minor` at the floor** `[R-CNT-26]` states, and `flags` = 0."

`[R-CNT-26]` is a SHOULD — "A writer SHOULD emit the lowest version_minor that defines
every feature present in the file" — and §21.6 confirms a higher minor is accepted
("version_minor is higher than this text defines | Accepted; minors never gate"). So item
8 takes a SHOULD as a requirement, in exactly the way item 7 does for `[R-TYP-10]` and
item 3 does for `[R-CNT-03]` — both of which the closing paragraph lists. Item 8's
`flags = 0` half *is* already mandatory (`[R-CNT-08]`); its `version_minor` half is not.
That is a fifth thing.

Item 6:

> "**The sentinel for every all-fill tile**, so that a tile whose samples all equal fill
> is never stored; otherwise two writers agreeing on content still disagree on bytes."

Nothing in the document requires an all-fill tile to be unstored. §3.1 makes storedness
purely a property of the entry, and §13's note treats sentinel emission as a writer's
choice. Item 6 therefore adds a sixth non-mandatory constraint, and one with a direct
byte consequence far larger than the fill field's — as item 7 itself observes ("item 6
stores no tile whose samples all equal fill, so two writers that default fill differently
disagree about which tiles exist"). Items 2 (a derived `file_id`, where §9.3 states only
a SHOULD), 4 (one generation) and 5 (fixed alignment declarations) are three more.

The count "Four" is wrong on the paragraph's own criterion.

**Byte-level: no.** Appendix G is marked non-normative and is opt-in ("It adds no
requirement to any actor: a writer ignoring it is fully conforming"), so no conforming
file, reader, writer, updater or verifier changes behaviour on it. The defect is that a
reader of the appendix cannot use the closing paragraph as the audit checklist it is
written to be.

---

### writer-04 — AMBIGUITY — Appendix G leaves at least two writer freedoms open despite its preamble

The preamble states what the profile is for:

> "Applications that need byte-identical output — content-addressed storage, reproducible
> builds — can adopt this profile, **which closes the degrees of freedom this format
> deliberately leaves open.**"

Two degrees of freedom I found while building the file survive adoption of all nine
items.

**(i) The user-metadata encoding, and the zstd encoder under it.** §18.2 assigns two
encodings — "1 = none and 2 = zstd are assigned" — and nothing prefers one. Item 9 closes
only the JSON layer:

> "**User metadata either absent, or serialized by a named JSON writer at a named
> version.**"

Item 1 closes the compressor, but names it as a *codec*:

> "**Codec 1 (none), or a named codec implementation at a named version with fixed
> encoder settings** …"

The permitted readings are (a) "codec" means the §17.2 codec field, an identifier space
§10.2 lists separately from "metadata encoding (§18.2)", in which case a profile-adopting
writer that selects encoding 2 has an entirely unpinned zstd encoder producing the extent
bytes; or (b) "codec" is generic and reaches §18.2's encoder too, in which case item 1
still does not decide *which* encoding a writer selects for identical input, since that
is a per-record field with no default. I picked (a), because §10.2 tabulates the two
spaces as distinct and §18.2 consistently calls its field "encoding", never "codec". On
either reading two profile-conforming writers can emit different metadata extents for
the same decoded document — and the extent length feeds through into every subsequent
offset in the file.

**(ii) Unicode normalization of names.** `[R-ENC-14]`:

> "Writers SHOULD emit names in Unicode Normalization Form C; a writer that does not risks
> visually identical but byte-distinct names coexisting, which conforming readers will
> treat as distinct."

§4.6's example gives the byte cost: `température` is 12 bytes in NFC and 13 in NFD, and
they "are a *different name* under `[R-ENC-13]`". A caller supplying a decomposed name
therefore gets a 12-byte or a 13-byte name field depending on whether its writer honours
the SHOULD — different layer records, different `inline_length`, different `dir_length`,
different everything downstream. Appendix G nowhere mentions normalization, and its
closing paragraph does not list it among the things the profile adds.

I read `[R-ENC-14]` as licensing (indeed advising) a creator to normalize a
caller-supplied name, on the strength of the word "emit"; the contrary reading — that a
name arrives as bytes and is never transformed — is supported by §20.4's rationale
warning that "a re-serializer that renormalized a name would change the name's identity",
though that sentence is about *updaters* re-emitting, not creators.

**Byte-level: no.** Both writers in each case emit conforming files, and `[R-CNF-05]`
already licenses conforming writers to differ ("two conforming writers given identical
input MAY produce different conforming files"). Resolving this changes nothing about
which bytes are accepted or rejected; it changes only whether the profile delivers what
it advertises.

---

### writer-05 — AMBIGUITY — Appendix G item 3 does not fix where a layer sub-record's extent goes

Item 3 is the profile's total emission order, and it is the item that makes byte-identity
possible at all:

> "**A total emission order, contiguously.** For each layer in ascending layer-name byte
> order: its stored tiles in disk-ordinal order, then its tile-index region; then any
> record extents in ascending record order; then the directory."

Two things are undetermined for a file whose layers carry user-metadata sub-records —
which is the ordinary case, since §18.1 gives every layer one.

**(i) Is "then any record extents" inside the per-layer loop or after it?** The clause has
no possessive ("its stored tiles … its tile-index region; then **any** record extents"),
and the semicolon separates it from the loop body, which reads as a later phase. But the
colon that opens the loop governs everything to the sentence's end on the competing
reading. Writer P emits `[A's tiles][A's index][A's metadata extent][B's tiles][B's
index][B's metadata extent][file metadata extent][dir]`; writer Q emits `[A's tiles][A's
index][B's tiles][B's index][A's metadata extent][B's metadata extent][file metadata
extent][dir]`. Both claim item 3. Every extent offset after the first divergence differs.

**(ii) What is "ascending record order" for a sub-record extent?** The next sentence
defines an order over top-level records ("Records are ordered by type, and within type
0x0001 by layer name") and, separately, an order over one layer record's sub-records
("ordered by type, and within a type by their encoded bytes compared lexicographically").
It defines no single order over the union. A file-scope metadata record (type 0x0002) and
a layer's metadata sub-record (also type 0x0002) are not comparable under either rule.

I picked the later-phase reading with a flattened order — traverse top-level records in
item-3 order, and within a layer record its sub-records in item-3 order — because it is
the only construction that makes "ascending record order" total. That is a guess.

**Byte-level: no.** The profile is non-normative and both writers emit conforming files;
this affects only whether two independent implementations of the same profile agree,
which is the profile's entire purpose.

---

### writer-06 — AMBIGUITY — §9.7's disjointness check literally includes the records inside the directory

`[R-LIF-08]`:

> "From the live trailer it enumerates the live directory and its records and their
> sub-records, each record's extent, and the non-sentinel entries of each layer's
> tile-index region … **It checks that these occupy disjoint byte ranges**, that each lies
> within [16, F − 64), and that each verifies against the checksum covering it, where
> §8.1's map states one (§8.1)."

Read literally, "these" is the list just enumerated, which includes "its records and
their sub-records". Every record lies **inside** the directory region — §7.1: "The
directory region is dir_length bytes at dir_offset. Its final 4 bytes are a CRC-32C over
the preceding dir_length − 4 bytes; those covered bytes are the record sequence itself" —
so on that reading every file containing at least one record has two claimants covering
the same bytes, and a verifier must report reject-file (§21.2 row F33) on my file, on
Appendix A's 128-byte file the moment it grows a record, and on every conforming file
that has ever existed.

The competing reading is that the enumeration is the *traversal* (records are walked in
order to reach their extents) and the disjointness check runs over `[R-CNT-02]`'s
partition classes, which are named exhaustively and contain no "record" class:

> "Every byte of the live committed state belongs to exactly one of: the front signature
> block; or a **structure** — a stored-tile extent, a record extent (the bytes any
> record's extent slot references, whatever the record's type, §7.2), the directory, or
> the trailer."

I picked the second reading, on the strength of `[R-LIF-08]`'s own opening ("A verifier
checking `[R-CNT-02]`'s partition …") and of the parenthetical two sentences later that
treats front block and trailer as "claimed by the walk as well, being members of the live
committed state (`[R-CNT-02]`)" — i.e. claimancy is defined by `[R-CNT-02]`, not by the
enumeration.

**Byte-level: no.** `[R-CNT-02]`'s enumerated class list decides it: it names five
classes and "record" is not one of them, so the object of the disjointness check is
determined even though §9.7's sentence is loose. I report it because a verifier
implemented from §9.7 alone — which is the section that tells a verifier how to perform
the check — rejects every conforming file, and §9.7 is the only place the check is
operationalised.

---

## 7. What I could not determine, and did not raise as findings

Recorded for the transcript, deliberately not counted as findings because each is
decidable from the text at reasonable cost:

- **Shrinking an extent.** §11.1's rationale addresses only growth ("Growth that leaves
  every grid count … unchanged touches the directory alone"), and §20.3's shape (c) lists
  directory-only changes without mentioning that a *shrink* can convert real positions
  into padding positions, which `[R-SER-05]` then requires to encode fill — forcing the
  affected tiles to be re-emitted. Determined by `[R-SER-05]` being a property of the
  file's state rather than of the commit; my updater re-emits.
- **`[R-SLB-04]`'s trigger list** names only a commit that "supersedes a stored tile in,
  or grows the extents of" a slab-declared layer. My generation-2 commit *stores a
  previously unstored tile*, which is neither. Harmless: `[R-SLB-03]`'s invariant is a
  file property a verifier checks regardless, so the output must satisfy it or be
  nonconforming, and clearing the declaration is always available (§20.3's example (c)
  lists "clearing a slab declaration" as a directory-only change).
- **A compactor barred by one bad tile.** `[R-WRT-09]` obliges verifying "every stored
  tile's entry crc" and `[R-WRT-06]` says "A compactor MUST refuse to compact when any
  check `[R-WRT-09]` obliges fails". So a single T1 tile makes a file permanently
  uncompactable, even though a reader may serve every other tile. Sharp, but stated.
- **Extents are owned exactly once**, so two byte-identical layers cannot share one
  index region (`[R-CNT-13]`: "no two extent slots and no two structures overlap").
  Determined; costs a duplicate region.
- **Recovery with no candidate** (crash 1) is unstated but obvious.
- **`[R-LIF-07]`'s checkpoint SHOULD conflicts with Appendix G item 4** ("One
  generation"). The profile wins for profile adopters because `[R-LIF-07]` is a SHOULD;
  a writer producing a very large reproducible file simply accepts the recovery cost.

---

## 8. Verdict on the charter question

The document sufficed to write a conforming creator with **one** free field (`file_id`),
three free choices (structure placement, record order, which tiles to store) and no
guesses. It sufficed for the append procedure, the durability ordering, the commit point,
the slack ledger and all six crash points without a guess. It failed me in one place that
matters — writer-02, where two steps of the same requirement give opposite instructions
about an index entry I have to write — and in five places that are documentation defects
rather than implementation blockers: one false claim about the document's own field
taxonomy, three defects in the reproducible-writer profile, and one verifier procedure
that rejects every file if read as written.
