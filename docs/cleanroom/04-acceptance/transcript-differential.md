# Differential write of one input, two implementers

## 0. Resolving the input into declarations

| Input clause | Declared field | Value | Authority |
|---|---|---|---|
| layer `grid`, planar | layout `u8` | 2 | §7.4, §14.1 `[R-SER-06]` |
| dims z(E=2,T=1), y(E=3,T=2) | rank d, dim entries | d=2 | §7.4, §11.1 `[R-GEO-01]` |
| channels d(float32), m(bool) | C, channel entries | C=2, types 12 and 1 | §12.1 `[R-TYP-01]` |
| fills | fill fields | `00 00 C0 7F`, `01` | §13.1 `[R-TYP-06]`, §13.2 `[R-TYP-07]` |
| codec 1, filter 1 | codec, filter | 1, 1 | §17.2 `[R-COD-03]`, §17.3 `[R-COD-09]` |
| A = 512 | alignment A | 512 | §7.4, §16.1 `[R-SLB-01]` |
| — | slab S, A_slab | 0, 0 | forced by `[R-CNT-16]`, `[R-CNT-23]` |
| layer `tag`, interleaved | layout | 1 | §14.1 |
| dim i(E=1,T=1), channel c(uint8, fill 00) | — | d=1, C=1, type 6 | §12.1 |
| file-scope user metadata, encoding 1 | inline payload | `01` | §18.2 `[R-MTA-03]` |

**Two things the input does not pin, and I pinned them identically in both writers so the differential isolates structural divergence:**

1. **`tag`'s codec and filter.** Codec 0 is invalid (§17.2), so *something* must be chosen, and `[R-CNF-05]` makes the choice a writer freedom ("two conforming writers given identical input MAY produce different conforming files"). Both writers use codec 1 / filter 1.
2. **Every real sample value.** The input pins fills and storedness but no sample data. I take every in-extent sample to equal its channel's fill. This is the only content the input determines; it is not a spec ambiguity.

## 1. Derived geometry and the content the spec forces

Grid counts (§11.2 `[R-GEO-03]`): G_z = ⌈2/1⌉ = 2, G_y = ⌈3/2⌉ = 2, so **N = 4**, **P = T_z·T_y = 2**. Planar ⇒ addressed tiles = C·N = **8** = `entry_count` (`[R-CNT-17]`).

Spatial ordinal s = t_z·G_y + t_y (§11.4 `[R-GEO-06]`); disk ordinal = c·N + s. Channel `d` is index 0, `m` is index 1, so **"m at spatial ordinal 1" is disk ordinal 1·4 + 1 = 5**, the sole sentinel.

Since E_y = 3 and T_y = 2, tiles with t_y = 1 — spatial ordinals **1 and 3** — carry one padding position at in-tile ordinal 1 (y = 3 ≥ E_y). §11.3 `[R-GEO-04]`.

Decoded sizes (§14.2, §14.3 `[R-SER-02]`, `[R-SER-03]`):

| Tile | Rule | Size | Content | Why forced |
|---|---|---|---|---|
| `d` plane (ordinals 0–3) | planar numeric, P·Bᶜ | 8 B | `00 00 C0 7F 00 00 C0 7F` | ordinal-1 slot in tiles s=1,3 is a padding position ⇒ fill (`[R-SER-05]`) |
| `m` plane (4, 6, 7) | packed planar bool, ⌈P/8⌉ | 1 B | `FF` | bit0 = value (fill), bit1 = padding position ⇒ fill bit, bits 2–7 = pad bits ⇒ fill bit (`[R-SER-05]`, `[R-SER-03]`) |
| `tag` (ordinal 0) | interleaved, P·Q | 1 B | `00` | — |

Codec 1 forces entry length = decoded size (`[R-COD-04]`): 8, 1, 1. Entry CRCs: `crc32c(00 00 C0 7F 00 00 C0 7F)` = **0x7BB1B19C**, `crc32c(FF)` = **0xFF000000**, `crc32c(00)` = **0x527D5351**.

Index regions (§15.1 `[R-IDX-01]`, `[R-CNT-17]`): grid = 8×20 + ⌈8/2¹⁶⌉×4 = **164 B**; tag = 1×20 + 4 = **24 B**. One partial segment each, so `[R-IDX-05]`'s constant is unavailable and both CRCs must be computed.

Record sizes are identical in both files: grid layer record inline = **103 B**, tag = **75 B**, metadata record inline = **1 B**; directory = 127 + 99 + 25 + 4 = **255 B**.

## 2. Writer A — Appendix-G emission order

Layers in ascending name order, each layer's tiles in disk-ordinal order then its index region, then record extents, then the directory.

| Range | Len | Class | Contents |
|---|---|---|---|
| [0, 16) | 16 | front block | `89 54 41 52 4E 0D 0A 1A` + 8 × `00` |
| [16, 512) | 496 | declared padding | zero |
| [512, 520) | 8 | structure | grid tile ord 0 |
| [520, 1024) | 504 | declared padding | zero |
| [1024, 1032) | 8 | structure | grid tile ord 1 |
| [1032, 1536) | 504 | declared padding | zero |
| [1536, 1544) | 8 | structure | grid tile ord 2 |
| [1544, 2048) | 504 | declared padding | zero |
| [2048, 2056) | 8 | structure | grid tile ord 3 |
| [2056, 2560) | 504 | declared padding | zero |
| [2560, 2561) | 1 | structure | grid tile ord 4 (`FF`) |
| [2561, 3072) | 511 | declared padding | zero |
| [3072, 3073) | 1 | structure | grid tile ord 6 |
| [3073, 3584) | 511 | declared padding | zero |
| [3584, 3585) | 1 | structure | grid tile ord 7 |
| [3585, 3749) | 164 | structure | grid tile-index region |
| [3749, 3750) | 1 | structure | tag tile (`00`) |
| [3750, 3774) | 24 | structure | tag tile-index region |
| [3774, 3796) | 22 | structure | user-metadata extent |
| [3796, 4051) | 255 | structure | directory (records: grid, tag, meta) |
| [4051, 4096) | 45 | declared padding | pre-trailer pad |
| [4096, 4160) | 64 | structure | trailer |

**F = 4160** (mod 64 = 0 ✓).

```
grid tile-index region @3585
  00 02 00 00 00 00 00 00  08 00 00 00 00 00 00 00  9C B1 B1 7B     ord0  off=512
  00 04 00 00 00 00 00 00  08 00 00 00 00 00 00 00  9C B1 B1 7B     ord1  off=1024
  00 06 00 00 00 00 00 00  08 00 00 00 00 00 00 00  9C B1 B1 7B     ord2  off=1536
  00 08 00 00 00 00 00 00  08 00 00 00 00 00 00 00  9C B1 B1 7B     ord3  off=2048
  00 0A 00 00 00 00 00 00  01 00 00 00 00 00 00 00  00 00 00 FF     ord4  off=2560
  FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF  00 00 00 00     ord5  SENTINEL
  00 0C 00 00 00 00 00 00  01 00 00 00 00 00 00 00  00 00 00 FF     ord6  off=3072
  00 0E 00 00 00 00 00 00  01 00 00 00 00 00 00 00  00 00 00 FF     ord7  off=3584
  01 BF FE 35                                                        segment CRC
  crc_of_crc_array = 0x7611AB57

tag tile-index region @3750
  A5 0E 00 00 00 00 00 00  01 00 00 00 00 00 00 00  51 53 7D 52     off=3749 len=1
  74 31 B9 03                                                        segment CRC
  crc_of_crc_array = 0xB46ED4C4

user-metadata extent @3774 (22 B)
  7B 22 74 61 72 6E 2E 74 69 74 6C 65 22 3A 22 67 22 7D   {"tarn.title":"g"}
  F2 7D D1 65                                              CRC-32C = 0x65D17DF2

trailer @4096
  8A 4E 52 41 54 0D 0A 1A | 01 00 | 00 00 | 00 00 00 00
  gen=1 | dir_off=3796 | dir_len=255 | F=4160 | file_id=0x9E3779B97F4A7C15
  reserved 00000000 | CRC = 0xB56B64B9
```

## 3. Writer B — packed head, descending tile order, reversed record order

B interleaves the unaligned structures into what would otherwise be alignment padding, emits `grid`'s index region *before* its tiles, stores grid tiles in **descending** disk-ordinal order, orders the directory meta/tag/grid, and pretty-prints the JSON with one space after the colon.

| Range | Len | Class | Contents |
|---|---|---|---|
| [0, 16) | 16 | front block | identical to A |
| [16, 17) | 1 | structure | tag tile (`00`) |
| [17, 41) | 24 | structure | tag tile-index region |
| [41, 64) | 23 | structure | user-metadata extent |
| [64, 228) | 164 | structure | grid tile-index region |
| [228, 512) | 284 | declared padding | zero |
| [512, 513) | 1 | structure | grid tile **ord 7** |
| [513, 1024) | 511 | declared padding | zero |
| [1024, 1025) | 1 | structure | grid tile **ord 6** |
| [1025, 1536) | 511 | declared padding | zero |
| [1536, 1537) | 1 | structure | grid tile **ord 4** |
| [1537, 2048) | 511 | declared padding | zero |
| [2048, 2056) | 8 | structure | grid tile **ord 3** |
| [2056, 2560) | 504 | declared padding | zero |
| [2560, 2568) | 8 | structure | grid tile **ord 2** |
| [2568, 3072) | 504 | declared padding | zero |
| [3072, 3080) | 8 | structure | grid tile **ord 1** |
| [3080, 3584) | 504 | declared padding | zero |
| [3584, 3592) | 8 | structure | grid tile **ord 0** |
| [3592, 3847) | 255 | structure | directory (records: meta, tag, grid) |
| [3847, 3904) | 57 | declared padding | pre-trailer pad |
| [3904, 3968) | 64 | structure | trailer |

**F = 3968** (mod 64 = 0 ✓).

```
grid tile-index region @64   (same entry order — disk-ordinal — different offsets)
  ord0 off=3584 | ord1 off=3072 | ord2 off=2560 | ord3 off=2048
  ord4 off=1536 | ord5 SENTINEL | ord6 off=1024 | ord7 off=512
  lengths and entry CRCs byte-identical to A; segment CRC = 0xF8BBDADF
  crc_of_crc_array = 0x9756E537

tag tile-index region @17   off=16 len=1 crc=0x527D5351 ; segCRC=0xFAAA5F3F ; crc_of_crc=0xC4913F42

user-metadata extent @41 (23 B)
  7B 22 74 61 72 6E 2E 74 69 74 6C 65 22 3A 20 22 67 22 7D   {"tarn.title": "g"}
  41 15 4F 28                                                 CRC-32C = 0x284F1541

trailer @3904
  gen=1 | dir_off=3592 | dir_len=255 | F=3968 | file_id=0xC2B2AE3D27D4EB4F | CRC=0xEA3D1742
```

## 4. §5.2 partition and the dead-space total

**Both files partition.** I ran §9.7 `[R-LIF-08]`'s walk explicitly: from the live trailer, enumerate the live directory; from its records, each record's extent (which for a layer record *is* the tile-index region, §7.4); from each index region's non-sentinel entries, each stored-tile extent; plus the declared padding §5.2 constructively defines. Every range is disjoint, every interior range lies in [16, F − 64), and each verifies against the checksum §8.1 assigns it.

Every declared-padding run qualifies under §5.2 bullet 1 or 2:

- Each run preceding a `grid` stored tile is *exactly* the distance from the previous claim to the next multiple of A = 512, and is shorter than 512 (max observed 511). Note this is automatic: the gap is (−end) mod A, always in [0, A).
- The final run is the pre-trailer pad, 45 B (A) and 57 B (B), both < 64 (`[R-CNT-05]`).
- No run precedes a structure that alignment does not constrain — §16.1 constrains **stored-tile offsets only**, so neither the index regions, the metadata extent, nor the directory may be preceded by a gap. Both writers pack them flush.

**Dead space = 0 bytes for both.** Computation: the live-state claims sum to F exactly.

- A: 16 (front) + 36 (stored tiles) + 188 (index regions) + 22 (metadata extent) + 255 (directory) + 64 (trailer) + 3 579 (declared padding) = **4 160 = F**.
- B: 16 + 36 + 188 + 23 + 255 + 64 + 3 386 = **3 968 = F**.

Generation 1, so nothing was superseded; there is no byte outside the live state to count. See Observation 1 for the one wrinkle in *how* the walk is written.

Worth flagging for the operator: A = 512 on tiles of 1 and 8 bytes makes **86.0 % of A and 85.3 % of B declared padding**, and §8.1 assigns declared padding no checksum. That is legal and stated (§22.3, F9 is verifier-only) but here the unchecksummed fraction is the majority of the file, not a residue.

## 5. The differential

The two files share only their front block and the interiors of some padding runs — 3 372 of 3 968 overlapping bytes are equal, but only incidentally (both are zero padding). Structurally they overlap nowhere. Classifying every differing range:

| # | A range | B range | What differs | Class | Citation |
|---|---|---|---|---|---|
| 1 | [16,512) padding; payload from 512 | [16,228) tag tile + tag index + meta extent + grid index; padding [228,512) | Which structures occupy the pre-alignment region | **(a) freedom** | `[R-LIF-02]` step 2 "in any order satisfying §5.2's coverage classes"; §20.2 "placement is otherwise free (`[R-SLB-05]`)" |
| 2 | grid tiles ord 0→7 ascending at 512…3584 | grid tiles ord 7→0 descending at 512…3584 | Byte order of stored tiles vs. disk-ordinal order | **(a) freedom** | §16.1 constrains only `offset mod A = 0`; §20.2's "placement is otherwise free (`[R-SLB-05]`)". Entry *order in the region* is fixed (`[R-IDX-01]`); entry *offsets* are not |
| 3 | grid index @3585 | grid index @64 | Index region emitted after vs. before its tiles | **(a) freedom** | `[R-LIF-02]` step 2 |
| 4 | 8 entry-offset u64s in grid index | same slots, different u64s | Consequence of #2 | **(a)** consequence of #2 | — |
| 5 | grid segment CRC `01 BF FE 35`; crc_of_crc `0x7611AB57` | `DF DA BB F8`; `0x9756E537` | Consequence of #4 | **(b) determined** — each writer's value is forced by its own entry bytes | §15.4 `[R-IDX-04]`, §8.1 `[R-CNT-19]` |
| 6 | tag tile @3749, index @3750 | tag tile @16, index @17 | Placement | **(a) freedom** | `[R-SLB-05]`, `[R-LIF-02]` step 2 |
| 7 | metadata doc 18 B `{"tarn.title":"g"}` | 19 B `{"tarn.title": "g"}` | RFC 8259 insignificant whitespace | **(a) freedom** | §18.2 `[R-MTA-05]` fixes member *order* only and says explicitly it "does not make two writers' output identical"; `[R-CNF-05]` |
| 8 | extent_length 22 | extent_length 23 | Consequence of #7 | **(b) determined** by #7 | §7.1 `[R-CNT-25]` (doc + terminal CRC), §8.1 |
| 9 | extent CRC `F2 7D D1 65` | `41 15 4F 28` | Consequence of #7 | **(b) determined** | §8.1 |
| 10 | directory records grid, tag, meta | meta, tag, grid | Record order in the sequence | **(a) freedom** | `[R-CNT-14]` "Record semantics MUST NOT depend on record order" |
| 11 | dir_offset 3796 | dir_offset 3592 | Consequence of #1–#6 | **(b) determined** — the directory may not be preceded by declared padding (§5.2 admits no such class), so dir_offset is forced to the end of the last preceding structure | §5.2 `[R-CNT-02]`, `[R-SLB-05]` |
| 12 | dir CRC `E3 55 DC 1C` | `77 F9 4F 45` | Consequence of #10 | **(b) determined** | §7.1 `[R-CNT-11]` |
| 13 | pad 45 B; trailer @4096 | pad 57 B; trailer @3904 | Consequence of #11 | **(b) determined** — trailer offset = ⌈dir_end/64⌉·64; a 64-or-larger pad is F12 | `[R-CNT-05]`, `[R-CNT-06]` |
| 14 | file_id `15 7C 4A 7F B9 79 37 9E` | `4F EB D4 27 3D AE B2 C2` | Identity | **(a) freedom** | §6.2 (≠ 0 only); §9.3 `[R-LIF-03]` SHOULD-random |
| 15 | F = 4160 | F = 3968 | Consequence of #13 | **(b) determined** | `[R-CNT-06]` |
| 16 | trailer CRC `B9 64 6B B5` | `42 17 3D EA` | Consequence | **(b) determined** | `[R-CNT-06]` |

**No byte fell outside the two classes.** Every difference is either a freedom I can point at a sentence for, or a value one of us would have got wrong.

## 6. Bytes both writers were forced to (the traps that did not fire)

The charter's category (b) is best demonstrated by what *didn't* diverge. These are places a naive second implementer would plausibly have differed, and the spec determines each:

| Byte | Forced value | Rule |
|---|---|---|
| layer record `flags` | `03 00` (MU=1, PE=1) — not `00 00` | §7.3 table + `[R-CNT-22]` "writers MUST emit exactly the flag values fixed in the table" |
| metadata record `flags` | `02 00` (MU=0, PE=1) | same |
| disk ordinal of the unstored tile | 5, not 1 or 4 | `[R-GEO-06]` c·N + s, channel-major |
| `m` plane pad bits 2–7 | `1` (fill is true) ⇒ byte `FF`, not `03` | `[R-SER-05]`, T5 |
| `d` plane ordinal-1 slot in tiles s=1, 3 | fill `00 00 C0 7F`, not zero or writer memory | `[R-SER-05]`, T4 |
| `m` plane size | 1 B packed, not 2 B | §14.3 `[R-SER-03]` — packing is planar-bool-only |
| `entry_count` | 8 (C·N), not 4 | `[R-CNT-17]`, `[R-GEO-03]` |
| index `extent_length` | 164 / 24 | `[R-CNT-17]`'s formula, including the segment-CRC array |
| segment CRC | computed, not `0xEECB3BB2` | `[R-IDX-05]` — the constant is licensed only for **full** segments |
| all declared padding | zero | `[R-CNT-03]`, F9 |
| trailer `flags`, reserved | `00 00 00 00` | `[R-CNT-08]`, `[R-CNT-06]` |
| `linearization` | 1 | `[R-GEO-05]` |
| `A_slab`, `S` | 0, 0 | `[R-CNT-16]`, `[R-CNT-23]` |

## Findings

### BYTE-LEVEL AMBIGUITY

None. Every byte of both files classified into a spec-granted freedom or a spec-determined value.

### CONTRADICTION

None found. I mechanically checked the claims most likely to drift: §21.8's "121 conditions over 213 named instances" parses out of §21.2–§21.5 as exactly 38 + 47 + 26 + 10 = 121 rows and 69 + 81 + 43 + 20 = 213 instances under §21.1's stated counting rule; §21.3's stated 47 matches its L1–L48-minus-L40 row set; and the four published CRC constants all reproduce.

### OBSERVATION 1 — §9.7's walk does not enumerate the front block or the trailer, so the mandated dead-space total is stated two ways

**Location.** §9.7 `[R-LIF-08]` vs. §5.2 `[R-CNT-02]`/`[R-CNT-21]`.

§9.7: "From the live trailer it enumerates the live directory and its records, each record's extent, each layer's tile-index region and that region's non-sentinel entries, and the declared padding §5.2 defines; it checks that these ... each lies within [16, F − 64) ... **Bytes the walk does not reach are dead space:** the verifier sums them and reports the total." The enumeration omits the front block and the trailer, and the bounds check `[16, F − 64)` excludes them by construction.

§5.2, by contrast, puts both *inside* the live committed state — "the front signature block, and every structure reachable from the live trailer ..., together with the live directory, its declared padding, and the live trailer" — and then defines dead space as "every other byte of the file".

**Divergent outcome.** `[R-CNT-21]` makes reporting the dead total a MUST. On Appendix A's own 128-byte minimal file, verifier 1 reports **0 dead bytes**; verifier 2, following §9.7's sentence literally, reports **80 dead bytes — 62.5 % of the file** — telling an operator to compact a file with nothing to reclaim. On my writer A it is 0 vs. 80 of 4 160.

**Why this is not byte-level.** §9.7's first sentence is "walks **the live state** only", and §5.2 is the section that defines the live state; the enumeration list describes what is reached *from the live trailer* (the trailer and front block are already in hand), and `[16, F − 64)` is a bounds check on interior structures, not a definition. A careful reader gets 0. **Searched:** §5.2 (all three paragraphs), §9.7 including its Note, §22.3's coverage paragraph, `[R-CNT-21]`, and F8/F35 in §21.2 — none states the front block's and trailer's status in the dead total explicitly. Naming them in §9.7's enumeration would close it.

### OBSERVATION 2 — gratuitous dead space is a "writer defect" with no register row and no file-level outcome

**Location.** §16 `[R-SLB-05]`: "a byte the live state neither claims nor accounts for as declared padding is dead space, and a commit that produces dead space it did not supersede is a writer defect (`[R-CNT-02]`, `[R-LIF-02]`)."

**Discriminator.** Take my writer A and move the `tag` stored tile from 3 749 to 4 000, leaving [3 749, 4 000) unclaimed; recompute downstream. Generation 1, so nothing was superseded. Verifier 1 certifies and reports 251 dead bytes. Verifier 2 refuses to certify, citing `[R-SLB-05]` plus `[R-CNF-12]`'s "a verifier certifies only violation-free files".

**Why this is not byte-level.** Three independent statements resolve it toward *conforming*: (i) `[R-CNT-21]` — "no conformance requirement applies to it"; (ii) §21.1's normatively-complete register has no row for it (F8 covers only bytes of the **live** state left unclaimed); (iii) `[R-CNF-02]` carves out exactly this shape of rule — "conduct rules bind the actor, the predicate binds the bytes" — and "a *commit* that produces dead space it did not supersede" is undecidable from bytes above generation 1, so it cannot be a byte predicate. The friction is that `[R-SLB-05]` cites `[R-CNT-02]`, a file-conformance requirement, for a conduct rule; and §5.2's "Conforming writers produce partitioned files by construction — the commit protocol appends nothing it does not declare" points the other way but is labeled **Note**, hence non-normative under `[R-CNF-01]`. **Searched:** §5.2, §16, §9.2, §9.7, §20.2–§20.4, §21.2 rows F8/F9/F11/F12, `[R-CNF-02]`, `[R-CNF-12]`. This was the closest call in the exercise; a one-line register row (or an explicit "not a file-conformance condition") would settle it.

### OBSERVATION 3 — the placement-freedom grant is textually scoped to unaligned layers

`[R-SLB-05]`'s sentence granting free ordering opens "A layer that declares **neither** alignment nor a slab makes no layout promise: its stored tiles MAY occupy any non-overlapping byte positions, **in any order**". §16.1 `[R-SLB-01]` then adds only `offset mod A = 0` for an aligned layer and never restates the ordering freedom. My writer B stores `grid`'s tiles in descending disk-ordinal order, which rests on §20.2's generalizing clause — "every declared layout invariant (`[R-SLB-01]`, `[R-SLB-03]`) — placement is otherwise free (`[R-SLB-05]`)" — rather than on §16 itself. Resolvable, but §16.1 is where an implementer looks.

### OBSERVATION 4 — `dir_offset` and the trailer offset are fully forced, which §5.2 says only by exclusion

Because §5.2 admits declared padding *only* before an alignment/slab-constrained structure or as the pre-trailer pad, no gap may precede the directory: `dir_offset` is forced to the end of the last preceding structure, and the trailer offset to ⌈dir_end/64⌉·64. A writer wanting a page-aligned directory for mmap has no conforming way to get one, and learns this only by noticing that no coverage class would accept the gap. Both my writers comply; the constraint is derivable but never stated affirmatively.

### OBSERVATION 5 — this input makes the majority of the file checksum-free

A = 512 with 1- and 8-byte tiles yields 3 579 / 4 160 (86.0 %) declared padding in writer A and 3 386 / 3 968 (85.3 %) in B, against 36 bytes of stored-tile payload. §8.1 assigns declared padding no checksum and F9 is verifier-only, so a reader validates ~14 % of the file. §22.3 states the residue ("corruption confined to padding is invisible to a reader") but frames it as marginal; nothing bounds the ratio. Not a defect — `[R-SLB-01]` explicitly permits 512 — but the security note's sizing does not match what a small-tile aligned layer produces.

### OBSERVATION 6 — the input as given underspecifies two things a determinism harness must pin

`tag`'s codec and filter, and every real sample value. Codec choice is a genuine `[R-CNF-05]` writer freedom, so an unpinned harness would see codec-1-vs-codec-3 divergence and misattribute it to ambiguity. Stated here so the result is reproducible.

## Verdict

IMPLEMENTABLE: yes
BYTE-LEVEL AMBIGUITIES: 0
CONFIDENCE: high

Working files (both complete and self-consistent, dead space 0): `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/fd7f7832-d335-4b62-b238-e3c853283d84/scratchpad/A.tarn` (4 160 B) and `.../B.tarn` (3 968 B); generator `.../build.py`; constant and register-count checks `.../check.py`.
