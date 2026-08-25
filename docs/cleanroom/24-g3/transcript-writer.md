# Round 24 — Writer / updater implementer, verbatim walk

## 0. Disclosure and method

I read exactly one specification file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in six `sed -n` slices covering lines 1–4445, plus targeted `grep`/`awk` over the same file. I
opened no ADR, no PLAN.md, no OPEN-QUESTIONS.md, no AGENTS.md, no conformance corpus, no
registry.json, no git history, no web resource. All computation was local Python over data I
typed myself.

Two things I must disclose because they are breaches of the spirit if not the letter of the
access rule, and a disclosed breach is usable while an undisclosed one poisons the round:

1. **Context I did not ask for.** My runtime placed a project-instruction pointer and an index of
   the maintainer's memory files into my context before I began. It named topics and one
   standing wording rule. I did not open any of the files it named, and I have not used anything
   it said as evidence about the specification. I note only that it appeared.
2. **Another agent's scratch file.** The scratchpad root is shared. I wrote `build.py` there; a
   concurrent agent's file of the same name replaced mine between two of my invocations, and the
   contents of *their* `build.py` were printed into my context when I re-ran it — roughly 20 lines
   of a TARN file-builder for a rank-2 5×5/4×4 single-uint16-channel layer, plus a hex dump of the
   file it produced. It contained no findings, no prose, no conclusions — it was a byte builder.
   I also listed the scratchpad root (not the `round24/` output directory), which showed me other
   agents' filenames. I did not open `round24/` and did not read any other agent's file
   deliberately. I then moved my work to a private subdirectory `wk-writer-r24-priv/` and rebuilt
   from scratch with a different geometry and channel set. I do not believe this contaminated any
   finding below — none of my five findings touches §14.5's padding example, which is what their
   geometry was exercising — but the reader of this transcript should know it happened.

Method: I implemented, on paper and in Python, a creator, an appender and (on paper) a compactor.
I built a real file byte for byte, appended two generations to it, and computed every CRC,
offset and slack total with my own CRC-32C. I checked my checksum against the document's own
check vector before trusting a single byte of it.

---

## 1. Bootstrapping: does my CRC agree with the document?

§4.5 gives a check vector and I ran it first, because every later byte depends on it.

```
CRC-32C("123456789") = 0xE3069283          spec says 0xE3069283      OK
CRC-32C(<zero bytes>) = 0x00000000         spec says 0x00000000      OK
```

Then the three derived constants the document states, so that I am not merely reproducing my own
arithmetic:

```
CRC-32C(4 sentinel entries, 80 bytes)   = 0x80A34955   §7.4 example says 0x80A34955   OK
CRC-32C(that 4-byte array)              = 0xC4EE982E   §7.4 example says 0xC4EE982E   OK
CRC-32C(2^16 sentinel entries)          = 0xEECB3BB2   §15.4 / App B says 0xEECB3BB2  OK
Appendix A trailer CRC over [0,60)      = 0xE00938D2   App A says 0xE00938D2          OK
```

Four independent hits. The checksum definition in §4.5 is unambiguous and my implementation of it
is the document's. Everything below rests on that.

I also reproduced every other piece of worked arithmetic in the document, because a writer
implementer's cheapest sanity check is the spec's own examples:

- §17.3 byte-shuffle of float32 1.0/2.0/3.0 → `00 00 00 00 00 00 80 00 40 3F 40 40`. Matches.
- §14.3 packed bool, T=(2,5), P=10, alternating: fill false → `55 01`, fill true → `55 FD`. Matches.
- §15.4 entry_count = 1,000,000 → 16 segments, last covering 16,960; CRC array 64 bytes; region
  20,000,064 bytes; tile 999,999 at segment-relative byte 339,180; segment 15 at
  [19,660,800, 20,000,000). All match.
- §11.4 coordinate (300,700) → s = 10, in-tile ordinal 11,452; planar channel 2 → disk ordinal 74;
  §15.4's entry at region bytes [1,480, 1,500). All match.
- §7.4 layer-record payload: 4 + 34 + 18 + 12 + 13 = 81; extent length 4·20 + ⌈4/2¹⁶⌉·4 = 84. Match.
- §21.9's note: segment-CRC array at 2³² tiles = 256 KiB; at 2³⁶ = 4 MiB; one full segment = 1.25 MiB.
  All match.
- Appendix G item 10: `température` is 12 bytes NFC, 13 bytes NFD (verified with a real normalizer).
- §21.1's instance arithmetic: I parsed all 121 register rows mechanically and summed the
  Instances cells (a cell reading `—` counting as 1, otherwise semicolon-separated items):
  F 36 rows / 58 instances, L 49/116, T 26/55, R 10/48 → **121 rows over 277 instances**, exactly
  what §21.8 claims. That is a non-trivial check on the two register subsections that changed this
  round (§21.2 and §21.5) and it passes.

This is a document whose numbers are right. Everything I report below is a matter of what a rule
says, never of a miscomputed constant.

---

## 2. Creation: a file built byte for byte

### 2.1 What I chose to build, and why

A file with two layers, both non-trivial in a way that exercises a different part of §14:

- **`grid`** — rank 2, dimensions declared `(y, x)`, extents (5, 5), tile extents (4, 4),
  **interleaved**, two channels: `t` float32 with fill `0x7FC00000` (quiet NaN), `m` bool with
  fill `0x00`. This gets me an edge-padded grid (G = (2,2), so three of four tiles carry padding
  positions), a mixed bool/numeric interleaved sample (§14.4's licensed combination), and a
  sample stride Q that is not a power of two.
- **`mask`** — rank 1, extent 10, tile extent 10, **planar**, one bool channel `v` with fill
  `0x00`. This gets me a packed boolean plane with pad bits (P mod 8 = 2), which is a different
  §14 path from anything `grid` exercises.
- A file-scope user-metadata record, and a layer-scope user-metadata sub-record on `grid`.

Both layers codec 1 (none), filter 1 (none), no alignment, no slab. I deliberately chose codec 1
so that every stored byte in this walk is a byte I can state; §17.2's compressing codecs are
encoder-dependent by construction (Appendix G item 1 says so plainly) and would make the layout
unrepeatable in prose.

### 2.2 Geometry, fixed by the document

`[R-GEO-03]`: Gᵢ = ⌈Eᵢ/Tᵢ⌉, stated as Eᵢ/Tᵢ plus 1 if Eᵢ mod Tᵢ ≠ 0 — the document goes out of its
way (§11.2's Note) to forbid the `(E+T−1)/T` idiom because the intermediate sum can leave the
declared domain. I used the stated form.

```
grid: G = (⌈5/4⌉, ⌈5/4⌉) = (2, 2)      N = 4      P = 4·4 = 16
      C = 2, B_t = 4, B_m = 1  →  Q = 5,  F_t = 0, F_m = 4
      addressed-tile count (interleaved) = N = 4  → entry_count = 4
      decoded size = P·Q = 80
mask: G = (⌈10/10⌉) = (1)              N = 1      P = 10
      addressed-tile count (planar) = C·N = 1·1 = 1 → entry_count = 1
      decoded size = ⌈P/8⌉ = 2                                (§14.3, not §14.2 — bool + planar)
```

Nothing here was a guess. §11.2 fixes the addressed-tile count as N interleaved and C·N planar;
§14.2's table fixes P·Q for interleaved and P·Bᶜ for a planar *numeric* channel; §14.3 carves the
planar bool plane out to ⌈P/8⌉ and §14.4 tells me explicitly that a single-channel bool layer is
*not* layout-invariant, which is exactly why I made `mask` planar.

### 2.3 The decoded tile images

`grid` tile at tile coordinates (ty, tx) has spatial ordinal s = ty·Gx + tx (`[R-GEO-06]`, row-major,
last-declared dimension varying fastest). Interleaved, so disk ordinal = s (§11.4).

The value sequence is `[R-SER-01]`'s interleaved form: value k is channel (k mod C)'s value at
in-tile ordinal k div C, sample-major, channels adjacent in declared order. In bytes
(`[R-SER-02]`): for each in-tile ordinal u = uy·4 + ux, four bytes of `t` little-endian then one
byte of `m`. 16 × 5 = 80 bytes.

Padding positions: `[R-SER-05]` fixes them to the channel's recorded fill — for `t` the four bytes
`00 00 C0 7F`, for `m` the single byte `00`. So:

- tile 0 = (0,0) covers y 0–3, x 0–3: all sixteen positions real.
- tile 1 = (0,1) covers y 0–3, x 4–7: x = 4 real (four positions), x = 5,6,7 padding (twelve).
- tile 2 = (1,0) covers y 4–7, x 0–3: y = 4 real (four), y = 5,6,7 padding (twelve).
- tile 3 = (1,1) covers y 4–7, x 4–7: only (4,4) real; fifteen padding.

I chose the input array so that the sample at (4, 4) equals the fill for both channels. That makes
tile 3's whole decoded image the 80 bytes `(00 00 C0 7F 00) × 16` — an all-fill tile. §3.1 says an
addressed tile is stored iff its entry is not the sentinel, and §13.3 says an unstored tile reads
as fill at every position, so storing it and sentinelling it produce **the same reference array**.
The core document leaves the choice to me (`[R-CNF-05]`: two conforming writers given identical
input MAY produce different conforming files); Appendix G item 6 takes it away for a reproducible
writer ("The sentinel for every all-fill tile"). I sentinelled it, and I flag it here as
**degree of freedom D14** for §7's catalogue.

`mask`'s single tile: ten bool values alternating true/false in in-tile-ordinal order, bit-packed
LSB-first per §14.3. Byte 0 = `0x55` (values 0–7), byte 1 carries values 8–9 in bits 0–1 = `0x01`,
and bits 2–7 are **pad bits**, which `[R-SER-05]` fixes to the plane's channel's fill bit — fill is
false, so zero. Decoded image `55 01`. This is byte-for-byte §14.3's own example, which is how I
know I read §14.3 the way its author did.

§14.3's Note is load-bearing and I want to record that I needed it: **pad bits are not padding
positions.** `mask` has E = T = 10, so it has *no* padding positions at all, and it still has six
pad bits. A writer that conflates the two emits a conforming file here by luck (both are fill) and
a nonconforming one the moment the fill is true.

### 2.4 The tile index

`[R-IDX-01]`: entry k at region byte 20k, entry order is disk-ordinal order, and the region is
`[entries: 20·entry_count][segment CRC array: ⌈entry_count/2¹⁶⌉ × 4]` with no padding anywhere
inside it. `[R-CNT-17]` cross-checks extent_length against
`entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4`.

```
grid index region = 4·20 + 1·4 = 84 bytes.   Formula agrees.
mask index region = 1·20 + 1·4 = 24 bytes.   Formula agrees.
```

Sentinel for tile 3: `[R-IDX-02]` — offset and length both `0xFFFF_FFFF_FFFF_FFFF`, crc 0, i.e. the
twenty bytes `FF ×16 00 ×4`.

**One place I got it wrong on the first pass, and the document caught me.** I initially computed
`crc_of_crc_array` over the *entry array*. §7.4's table says "CRC-32C over the index's
**segment-CRC array**", §8.1's map says the segment CRC array is "itself covered by the layer
record's crc_of_crc_array", and §15.4 says the same. Three statements, all consistent, and the
§7.4 worked example pins the value (0xC4EE982E over a four-byte array) so that a reader who
mis-scopes it discovers the error immediately. This is the document doing its job: the
"every non-obvious encoding is followed by a worked numeric example" discipline of §4.7's Note is
not decoration.

Final values in my file:

```
grid: segment CRC = 0x0F1C0711   crc_of_crc_array = 0xBAFE5BEA
mask: segment CRC = 0x994B1629   crc_of_crc_array = 0xA9AE9771
```

`[R-IDX-05]`'s all-sentinel constant does not apply to either: `grid`'s single segment is partial
(4 entries, not 2¹⁶) and mixed, and the rule is explicit that "a partial segment's CRC MUST be
computed" and that a *full* segment means one covering exactly 2¹⁶ entries, final or not. Clear.

### 2.5 Placement — what the document fixes and what it leaves to me

`[R-SLB-05]` is unusually generous and unusually explicit: a layer declaring neither alignment nor
a slab "makes no layout promise: its stored tiles MAY occupy any non-overlapping byte positions,
in any order". §20.2 repeats it for creation ("placement is otherwise free"). So the only
placement rules binding me are:

| Rule | Constraint |
|---|---|
| `[R-CNT-01]`, §6.1 | front block at [0,16), constant |
| `[R-CNT-13]` | every extent at offset ≥ 16, ending ≤ F − 64, owned exactly once, no overlap |
| `[R-CNT-05]` | no structure between the directory's end and the trailer |
| `[R-LIF-02]` step 5 | pad from the directory's end to the next 64-byte boundary; trailer there |
| §6.2 | F mod 64 = 0 |
| `[R-CNT-09]` | SHOULD keep dir_length + pad + 64 within 65,536 bytes |

Everything else — the order of tiles, the position of an index region relative to its tiles, the
interleaving of one layer's structures with another's, the order of records inside the
directory — is mine. I adopted Appendix G item 3's total order so that this transcript is
checkable: layers by ascending name byte order (`grid` = `67 72 69 64` before `mask` = `6D 61 73 6B`),
each layer's stored tiles in disk-ordinal order, then its index region; then remaining record
extents, top-level first, then per layer record its sub-records; then the directory.

### 2.6 The byte map

```
 [0,   16)  front signature block            89 54 41 52 4E 0D 0A 1A + 8 zero bytes
 [16,  96)  grid stored tile, disk ordinal 0   80 bytes, codec 1, filter 1
 [96, 176)  grid stored tile, disk ordinal 1   80 bytes
 [176,256)  grid stored tile, disk ordinal 2   80 bytes
            (disk ordinal 3 is all-fill -> sentinel entry, no bytes)
 [256,340)  grid tile-index region             84 bytes  = 4x20 entries + 1x4 segment CRC array
 [340,342)  mask stored tile, disk ordinal 0    2 bytes  = 55 01
 [342,366)  mask tile-index region             24 bytes  = 1x20 + 1x4
 [366,402)  file-scope user-metadata extent    36 bytes  = 32-byte document + 4-byte CRC
 [402,427)  grid user-metadata sub-record ext  25 bytes  = 21-byte document + 4-byte CRC
 [427,708)  directory region                  281 bytes  = 277-byte record sequence + 4-byte CRC
 [708,768)  pre-trailer pad                    60 bytes  slack, zeroed by [R-CNT-03]'s advice
 [768,832)  trailer                            64 bytes
                                               F = 832,  F mod 64 = 0
```

Trailer fields, all fixed by §6.2 except the two marked:

```
[0,8)   8A 4E 52 41 54 0D 0A 1A     trailer magic
[8,10)  01 00                        version_major = 1
[10,12) 00 00                        version_minor = 0     <- [R-CNT-26] SHOULD; my choice
[12,16) 00 00 00 00                  flags = 0             ([R-CNT-08] MUST for a creator here)
[16,24) 01 00 ...                    generation = 1
[24,32) AB 01 ...                    dir_offset = 427
[32,40) 19 01 ...                    dir_length = 281
[40,48) 40 03 ...                    committed_file_length = 832
[48,56) 18 07 F6 E5 D4 C3 B2 A1      file_id                <- my choice, nonzero; SHOULD be random
[56,60) 00 00 00 00                  reserved
[60,64) <CRC-32C over [0,60)>
```

The layer records: `[R-CNT-12]` header 24 bytes; `[R-CNT-22]` fixes the flag values from §7.3's
registry, so a layer record carries MU = 1, PE = 1 → flags = `0x0003`, and a user-metadata record
MU = 0, PE = 1 → flags = `0x0002`. `grid`'s inline_length = 128 (its sub-record is inside the
payload, `[R-CNT-18]`); `mask`'s = 76.

### 2.7 What I had to guess during creation

Very little, and I want to be precise about it, because "the document left it to me" and "the
document failed to tell me" are different verdicts and only the second is a finding.

**Left to me, and the document says so:** structure placement and order (`[R-SLB-05]`,
§20.2); record order in the directory (`[R-CNT-14]`: "Record semantics MUST NOT depend on record
order"); whether to store or sentinel an all-fill tile; `file_id` (§9.3 advises randomness as a
SHOULD); `version_minor` (`[R-CNT-26]`, a SHOULD); slack content (`[R-CNT-03]`, a SHOULD to zero);
tile extents (§11.3's Note offers guidance and disclaims a rule).

**Fixed and I found the rule without difficulty:** every field width and order in §6.2, §7.2, §7.4,
§15.1; the value sequence and byte layout in §14.1–§14.3; padding and pad-bit content in §14.5;
the sentinel in §15.2; the checksum coverage map in §8.1; the ordered validation in §6.2; the
commit protocol in §9.2.

**Genuinely fixed but easy to get wrong** — I record these because a fresh implementer will hit
them: (a) `crc_of_crc_array` scopes to the segment-CRC array, not the entries; (b) a planar bool
plane is ⌈P/8⌉ bytes and an interleaved bool value is one byte, and the same layer may carry both
kinds of channel; (c) pad bits ≠ padding positions; (d) the fill *field's* length is the type's
element size and is cross-checked (`[R-CNT-23]`), so a bool fill field is one byte and
`[R-TYP-07]` restricts it to `0x00`/`0x01` while the *numeric* fill field admits every bit pattern
including NaN payloads (`[R-TYP-05]`); (e) `[R-CNT-16]` makes A and S mutually exclusive, and a
nonzero A_slab with S = 0 is a layer-scope error even though nothing reads it.

No creation-path finding. §5, §6, §7, §11–§17 and §20.2 gave me every byte.

---

## 3. The append procedure

### 3.1 Generation 2 — supersede one stored tile

The operation: change one sample of `grid`, at coordinate (0, 4), which lies in tile 1.

`[R-WRT-04]`'s six steps, in order.

**Step 1 — establish F.** Validate the trailer in the final 64 bytes of the *physical* file
(`[R-LIF-04]`). Passing that gate implies physical length = committed_file_length, since
`[R-CNT-06]` compares them (F17). So after step 1, F = 832 and physical = 832; nothing to truncate.

**Step 2 — open.** §19.1's four steps, as a reader. Note what this does *not* do: it consumes the
trailer and the directory only, so it establishes no tile-scope violation, which `[R-WRT-04]`
step 2 states outright. The layer table is built from name fields alone.

**Step 3 — validate what the commit touches.** `[R-WRT-03]`: the trailer and the *full* directory
always ("re-emission relies on every directory byte"), plus §19.3's layer validation for `grid`
(whose record and index I modify), plus the §19.4 index chain for every segment whose entries I
reuse. `mask` I neither modify nor rely on, so I owe it nothing beyond the open. This is exactly
the reliance principle and it is stated cleanly.

**Step 4 — write payloads and indexes.** Writing begins at exactly F = 832.

```
[832,  912)  new stored tile for disk ordinal 1      80 bytes
[912,  996)  grid tile-index region, RE-EMITTED IN FULL   84 bytes
             entry 0: byte-identical, still -> [16,96)
             entry 1: re-pointed -> [832,912), new crc
             entry 2: byte-identical, still -> [176,256)
             entry 3: still the sentinel
             segment CRC recomputed; crc_of_crc_array in the layer record recomputed
```

The whole 84-byte region moves for one changed entry. §20.3's Note quantifies exactly this
("editing one sample of a 10⁶-tile layer appends about 20 MB of index and leaves as much slack"),
and §20.3's figure (b) draws it. The re-emission is *necessarily* at a new placement because
`[R-LIF-01]` freezes [0, F).

`mask`'s record keeps its extent slot pointing at [342, 366) — `[R-WRT-05]`, and §5.1's example
says it in words: "a layer the commit does not touch keeps its extent slot pointing where it
always pointed".

**Step 5 — re-emit the directory** per §20.4, then its CRC. Every record byte-identical except
`grid`'s, whose extent slot and `crc_of_crc_array` changed. `grid`'s user-metadata sub-record is
carried through byte-identically inside the modified layer record's payload, extent slot and all —
the sub-record is itself a record and `[R-WRT-05]` reaches it.

**Step 6 — commit.** `[R-LIF-02]` steps 4–6: barrier; pad; trailer with generation 2, the same
`file_id`, unknown ignore-lane bits copied forward, version_minor per `[R-CNT-26]`; barrier.

```
[996, 1277)  directory 2                        281 bytes (same size: only field values changed)
[1277,1280)  pad                                  3 bytes
[1280,1344)  trailer, generation 2               64 bytes    F2 = 1344
appended: 512 bytes for an 80-byte payload change
```

**Slack after generation 2.** Live state = 16 (front) + 3·80 (grid tiles) + 84 (grid index′)
+ 2 (mask tile) + 24 (mask index) + 36 (file UM extent) + 25 (grid UM extent) + 281 (dir₂) + 64
(trailer₂) = 772. Slack = 1344 − 772 = **572**, and it decomposes exactly:

```
generation-1 grid index region   84
generation-1 directory          281
generation-1 pre-trailer pad     60
generation-1 trailer             64
superseded tile-1 payload        80
generation-2 pre-trailer pad      3
                                ---
                                572
```

That is `[R-CNT-21]`'s total, and my walk completed, so it is exact rather than partial.

### 3.2 Generation 3 — add a layer with no addressed tiles

Add `aux`: rank 1, extent 0, tile extent 64, one float64 channel with all-zero fill. `[R-GEO-02]`
makes this valid: grid count 0, zero addressed tiles, empty index, empty reference array, and
readers MUST accept it. So `entry_count = 0`, extent slot `(0, 0)` (§7.4), `crc_of_crc_array = 0`
(`[R-CNT-23]`; L27 registers the nonzero case), and `[R-CNT-17]`'s formula yields 0. No index
region exists at all — §15.4's closing example says so explicitly: "At entry_count = 0 there is no
region at all — zero segments, a zero-byte CRC array, extent slot (0, 0) and crc_of_crc_array = 0
— so nothing is fetched and nothing is verified."

The commit appends the directory, the pad and the trailer and nothing else. That is §20.3's
figure (a) with the new layer contributing no structures. dir₃ = 387 bytes at [1344, 1731), pad 61,
trailer [1792, 1856), F3 = 1856. Slack rises to 978.

I note in passing that this file is where `[R-COD-07]`'s escape lives: `aux` could declare codec 4
with a tile extent whose decoded size is far past `0x7E000000`, and §17.2's Note says so —
the cap is quantified over the layer's *addressed* tiles, of which there are none. §20.3 step 4
then makes the escape non-durable: the first growth that addresses a tile is measured against the
cap (L44). `[R-ENC-04]`'s 2⁶³ − 1 ceiling carries no such quantifier and is checked in the empty
layer anyway. This is a quantifier the document gets right and says it is getting right, twice.

### 3.3 Appending to a file whose records I do not all understand

The charter asks me to walk every combination of record flags. §7.2 defines two: bit 0
MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2–15 reserved. Four combinations, at two scopes.
§20.4's table plus `[R-CNT-12]`, `[R-CNT-15]`, `[R-CNT-18]` and `[R-CNT-22]` cover all eight cells.

First, the authority question, which §20.4 answers before the table: the stored bits are
authoritative **only for a type the consuming tool does not implement**. For a §7.3-registered
type the registry's fixed flags govern (`[R-CNT-22]`); for a type I implement from some other
definition, that definition's flags govern; only for a type I cannot identify at all do I read the
bits off the record. That ordering matters and it is stated.

| Scope | Stored MU | Stored PE | What my updater may do |
|---|---|---|---|
| top-level | 1 | 1 | Retain byte-identical. MUST NOT modify the scope it governs — and its scope is the *file*, so **no commit is available at all**: my open (§19.1 step 4) applies `[R-CNT-15]`'s MU gate, an unknown top-level MU = 1 type is reject-file, and I am a reader before I am a writer. Compaction barred on the same ground (`[R-WRT-06]`). |
| top-level | 1 | 0 | `[R-CNT-12]`: read as PE = 1. Same as above. The combination is a writer violation whose detector is the verifier (F25); it never changes my behaviour. |
| top-level | 0 | 1 | Retain byte-identical, **extent content unmodified**. An appender may not even relocate the extent — `[R-WRT-05]` requires the extent slot re-emitted byte-identically. Only a compactor relocates it, and only by re-pointing the slot (`[R-WRT-08]`), which §7.2's no-embedded-offsets rule for MU = 0 records is what makes safe. |
| top-level | 0 | 0 | Retain byte-identical, **or drop it** — but only in a commit that *independently* changes the file's layer set, any layer record's content, or another non-layer top-level record. Dropping is not itself such a change, and neither is dropping some other record in the same commit. SHOULD report the loss. A compactor may drop it whenever it rewrites. |
| layer sub-record | 1 | 1 | Retain byte-identical; **that layer** is unmodifiable, every other layer stays editable (`[R-CNT-18]`, and the file is not rejected — the qualifier §21.6 calls load-bearing). |
| layer sub-record | 1 | 0 | Read as PE = 1 (`[R-CNT-12]`); as above. L46 registers the combination for the verifier. |
| layer sub-record | 0 | 1 | Retain byte-identical, extent content unmodified. |
| layer sub-record | 0 | 0 | Retain, or drop only in a commit that independently changes **that layer's** record, the entry set of its index, or which of its tiles are stored. A change to a *different* layer buys nothing. |

Two asymmetries I want on the record because they are exactly the quantifier shape this round is
hunting, and in both cases the document scopes them correctly:

- A top-level MU = 0 / PE = 0 record may be dropped on **any** layer record's content change; a
  layer's sub-record only on **its own** layer's. The text says "that layer's record" for the
  sub-record and "any layer record's content" for the top-level one. Deliberate and unambiguous.
- Superseding a stored tile re-places the layer's index region, which moves its extent slot, which
  modifies that layer's record — and §20.4 spells that chain out rather than leaving me to derive
  it, because it is the difference between "may drop" and "MUST retain".

Write order for a commit that carries unknown records: unchanged. Their extents are already
committed bytes, so they are never rewritten; only their *records* are re-emitted, inside the
directory, at step 5. Nothing about an unknown record changes what must be durable before what.

Durability and the commit point, stated plainly for my implementation:

1. Payloads, index regions and record extents go down first, anywhere at or above F.
2. The complete directory and its CRC follow (step 3). §9.2's Note is emphatic that a new trailer
   may not point at a prior generation's directory region: "A writer that re-points a new trailer
   at a prior generation's directory region has left step 3 unperformed."
3. **Barrier 1** (step 4) — steps 1–3 durable.
4. Pad, then trailer (step 5).
5. **Barrier 2** (step 6) — the trailer durable. **This is the commit point.**

A detail worth recording because the document's narrowness here is load-bearing rather than
sloppy: step 6 says "make the trailer durable" and says nothing about the pad written in the same
step. That is safe precisely because `[R-CNT-05]` leaves pad content unconstrained — a filesystem
hole reading as zeros in the pad is indistinguishable from the zeros `[R-CNT-03]` advises. Had the
pad been checksummed, step 6 would be under-specified. It is not.

---

## 4. Slack, per shape of commit

`[R-CNT-21]`: slack is every byte the live committed state does not claim; its content is
unconstrained; a verifier reports the total, and reports it as *partial* — an upper bound, naming
what stopped it — where its walk did not complete. §9.7 defines the walk: from the live trailer,
through the directory, each record's extent, and each non-sentinel index entry's stored extent,
plus the front block and the live trailer themselves.

| Commit shape | Bytes that become slack | Counted by |
|---|---|---|
| **Append, new layer** | prior directory, prior pad, prior trailer. Nothing of any existing layer moves. Sized by the file's *layer count*, never by any layer's data. | the walk, exactly |
| **Append, tiles added to a layer** | that layer's prior index region, plus prior dir/pad/trailer. Retained payloads do not move. | exactly |
| **Append, tile superseded** | as above plus the superseded payload | exactly |
| **Append, tile unstored** (entry becomes the sentinel) | as above plus the now-unreachable payload; the new entry contributes no stored extent to the walk, so those bytes fall to slack | exactly |
| **"In-place update"** — there is none. `[R-LIF-01]` forbids modifying a committed byte. The nearest thing is §20.3's shape (c), a change confined to the directory | prior dir/pad/trailer only | exactly |
| **Shrink that de-addresses tiles** | the de-addressed tiles' extents, plus the re-emitted index region's prior extent, plus dir/pad/trailer | exactly |
| **Whole-file rewrite** (a new file under a fresh `file_id`) | none carried; the *input* persists entirely, outside this format's reach | n/a |
| **Compaction** | none carried (§20.5). The output still has its own alignment gaps and its own pre-trailer pad, which are slack in the output | exactly, in the output |
| **Abandoned partial write** | *nothing becomes slack*, because there is no live state. The physical tail is not a trailer, §6.2's gates fail, and §5.2 is explicit: "Where §6.2's ordered validation rejects the file before a live trailer is established there is no F and no live state to walk, so the total is not owed at all". Not a partial total — the absence of one. | nobody |

What slack may contain: anything. `[R-CNT-21]` — "Slack has no internal structure this
specification defines, its content is unconstrained, and no conformance requirement applies to it.
A reader MUST NOT interpret it". `[R-CNT-03]` advises zeroing and names the two costs of not
doing so: bytes indistinguishable from stale data, and forfeited byte reproducibility. §22.3 adds
that corruption confined to slack is invisible to reader and verifier alike. §23.1 makes it a
privacy consideration. All four statements agree; none of them is a requirement.

One boundary I checked because it is the kind of thing that goes wrong: **a payload byte string
that mimics a trailer.** §6.2's Note, §9.6's first caution, §21.6's row and §22.3 all cover it, and
they agree: under live-state coverage a mimic is inert because nothing enumerates slack; the
exposure is a *recovery tool* landing on one, which is why `[R-LIF-06]` makes recovery output
re-verified as a whole file. My file's `grid` tile 0 begins `00 00 00 00 …`, so it could not mimic;
but the rule does not depend on luck and I could not construct a case the document does not name.

---

## 5. Torn-write recovery — four crash points

I use generation 2's commit against my file, F₁ = 832, F₂ = 1344.

**Crash A — during step 2 (payload/index appended, directory not yet written).** Physical length,
say, 900. Next reader: takes bytes [836, 900) as the trailer, magic fails, `[R-LIF-05]` forbids
scanning backward, reports the file torn. Next updater: step 1's trailer validation fails, so
**no append** — recovery is "a deliberate, separate operation" and never an implicit step of
opening for append (`[R-LIF-04]`). Recovery (§9.6) probes backward at 64-aligned offsets from the
largest o with o + 64 ≤ 900, requires magic + CRC + committed_file_length = o + 64, and lands on
o = 768 where trailer₁ sits with committed_file_length = 832 = 768 + 64. Truncating to 832 restores
the file exactly. **Is the file conforming in the meantime? No** — F17 (committed_file_length ≠
transport size) is a reject-file row. The append-only design buys *recoverability*, not
readability, and §9.2's figure says so in as many words: "The window is not one in which the old
state is *readable* — it is one in which the old state is *recoverable*."

**Crash B — after barrier 1, before the trailer is written.** Physical length 1277. Identical
diagnosis to A: no trailer at the tail, torn, recover to 832. The difference is invisible from
outside, which is the point: the directory being durable buys nothing until a trailer commits it.
This is why §9.2's Note insists a new trailer must address *this* commit's directory.

**Crash C — mid-trailer.** Physical length 1320, say: the final 64 bytes are [1256, 1320), which
straddles the tail of dir₂ and the first 40 bytes of trailer₂. Magic almost certainly fails; if by
malice it did not, the trailer CRC would, and if that did not, committed_file_length ≠ 1320 would.
Three independent gates, and §6.2 fixes their order. Torn; recover to 832.

**Crash D — trailer written but barrier 2 not taken, and the pad or a payload page not durable.**
This is the case §9.2's second Note is about. If the trailer survived and the directory did not,
the trailer validates and the directory CRC fails: reject-file, loudly, never silently. If the
trailer survived and one *tile payload* did not, the trailer and directory validate, the index
chain validates, and that one tile's crc fails: reject-**tile**, and every other tile of every
layer still reads. Degradation from "torn commits are invisible" to "torn commits are detected",
exactly as stated, with the blast radius scoped by §8.2's outcome map.

**Crash E — the residue case, which is not a crash at all.** A completed commit followed by a
writer that neither truncated nor overwrote past F (`[R-LIF-04]` violated). §9.5's Note is precise:
the reader meets a trailer that fails its gates, cannot tell residue from corruption, and is not
asked to; §21.2 already registers the state it can observe (F8, F17). No new row is owed and none
exists. I checked for a gap here and found the document ahead of me.

One consequence for my updater that I want stated: after any of A–D, the *only* sanctioned path
back is §9.6, and §9.6's output must be re-verified as a whole file before being trusted, and
`[R-WRT-04]` step 1 says that if I resume from re-verified recovery output I take F from that
output and "F, never the physical end, anchors every step below". So my implementation never
appends to a file whose tail it could not validate, full stop.

---

## 6. Compaction, walked as an implementer

This is where I found my byte-level candidate, so I set out the walk in full.

`[R-WRT-06]`, `[R-WRT-07]`, `[R-WRT-09]` and §20.4 give me: output contains only the structures
reachable from the input's live trailer, less any record §20.4 lets me drop; content preserved and
placement not; fresh `file_id` (a new draw, not merely a different value) and generation 1; input's
unknown ignore-lane bits carried forward in place of flags = 0; version_minor at least the input's
where the output carries an unimplemented feature, else `[R-CNT-26]`'s floor; refuse on any
`[R-WRT-09]` check that fails; refuse on any record of an unimplemented MU = 1 type; verification
depth = the open, each retained layer's record and full index chain, and each relocated extent's
checksum including every stored tile's entry crc, **before emitting that structure's bytes**.

I checked §20.5's arithmetic claim about the four extension vehicles, since §20.5 is one of this
round's changed passages. It says the two of §10.1's four vehicles §21.6 makes conforming are a
carried ignore-lane bit and an unrecognized `tarn.` key, and that the other two reach such a file
only as reserved-range violations — "F36 and L25 for a record type, and one row for each of the
other seven spaces §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)". §10.2 tabulates eight
spaces; minus record type leaves seven; the seven rows named are index encoding (L31),
linearization (L33), sample type (L34), channel layout (L36), codec (L43), filter (L45), metadata
encoding (R1). That is exactly right, and each of those rows' condition text does cover its
reserved range. The passage survives the check.

I then walked the regeneration rule and found the trigger it names is not the trigger that
operates — **finding writer-02** below.

Then I walked what §20.5 does *not* say, and found the larger gap — **finding writer-01**.

Two compaction behaviours I checked and found sound, so that the findings are not mistaken for a
general complaint about §20.5:

- **A structurally invalid index entry.** §15.3's six *structural* rows give an entry no usable
  extent. Regenerating a region means classifying every entry, such an entry is neither a sentinel
  nor re-pointable, so the compactor meets it and thereafter has detected the violation;
  `[R-WRT-06]` obliges refusal, and no drop is available because a tile-index entry is no record
  §20.4's table licenses dropping. Airtight, and the contrast with the *appender* — which carries
  such an entry forward byte-identically at its disk-ordinal position (`[R-WRT-04]` step 2) — is
  stated rather than left to be inferred.
- **An entry whose only defect is a failed payload crc.** §15.3 says such an entry is well-formed,
  its extent stands, it keeps its place in the verifier rows, in slab run continuity and in the
  coverage walk. `[R-WRT-09]` obliges the compactor to verify every stored tile's entry crc before
  emitting it, so the compactor detects it and refuses. Consistent across three sections.

---

## 7. Byte-divergence catalogue

Two conforming writers, identical input arrays, identical stated options (schema, tiling, layout,
codec choice, fill values, metadata document content). Every way their bytes may legitimately
differ, and whether Appendix G closes it.

| # | Degree of freedom | Source of the freedom | Closed by |
|---|---|---|---|
| D1 | Encoder output for codecs 2–4 (block/match/table choices) | `[R-CNF-05]`; §17.2 | **G1** (pin implementation + version + settings incl. thread count) |
| D2 | Raw DEFLATE's up-to-seven unused final-byte bits | §17.2 Note: "This specification constrains them nowhere" | **G1**, and §17.2 says so |
| D3 | Whether a zstd frame declares Frame_Content_Size at all | `[R-COD-06]`: "MAY be present" | **G1** |
| D4 | A zstd frame's declared Window_Size, anywhere ≤ decoded size | `[R-COD-06]` | **G1** |
| D5 | `file_id` | §9.3: any nonzero, SHOULD be random | **G2** (hash of emitted bytes, last eight digest bytes LE, 1 substituted if all-zero) |
| D6 | Placement of every structure and the extent of every gap | `[R-SLB-05]`, `[R-LIF-02]` step 2 | **G3** |
| D7 | Content of every gap and of the pre-trailer pad | `[R-CNT-03]` is a SHOULD | **G3** ("every byte of every such gap is zero — `[R-CNT-03]`'s advice, taken as a requirement here") |
| D8 | Order of records in the directory | `[R-CNT-14]` | **G3** (type, then layer-name for 0x0001, else header-with-extent_offset-masked ‖ payload ‖ extent, lexicographic) |
| D9 | Order of a layer record's sub-records | `[R-CNT-14]` via `[R-CNT-18]` | **G3**, same key |
| D10 | Number of commits used to build the same content | §9 constrains nothing | **G4** (one generation) |
| D11 | Whether to declare A, or S/A_slab, and at what value | §16 leaves it to the writer | **G5** |
| D12 | Filter value (1 vs 2) | §17.3 | **G5** |
| D13 | Storing vs sentinelling an all-fill tile | §3.1/§13.3 make them equivalent in the reference array | **G6** |
| D14 | Fill recorded when the caller chooses none | `[R-TYP-10]` is a SHOULD | **G7**, which also notes this reaches D13 |
| D15 | `version_minor` and `flags` | `[R-CNT-26]` SHOULD; `[R-CNT-08]` | **G8**, with the compactor carve-out stated |
| D16 | JSON serialization of the metadata document (number formatting, escaping, whitespace) | `[R-MTA-05]` explicitly does not make two writers identical | **G9** (pin the JSON writer, the storage encoding, and the zstd implementation where encoding is 2) |
| D17 | Unicode normalization of names | `[R-ENC-14]` is a SHOULD; `[R-ENC-13]` makes NFD a different name *and* a different length | **G10** |

Freedoms that are **not** freedoms, which I checked and which the profile therefore needs no item
for: padding-position content and pad-bit content (`[R-SER-05]`, mandatory); interleaved boolean
byte values (`[R-SER-08]`); the recorded fill's presence (`[R-TYP-06]`); the `crc_of_crc_array`,
each segment CRC, each entry crc, the directory CRC and the trailer CRC (all determined);
`entry_count` and the index region's length (`[R-CNT-17]`); `[R-IDX-05]`'s all-sentinel constant
(equal to the computed value, so no divergence); the extent slot of a zero-addressed-tile layer;
in-tile sample order (row-major for every linearization value, permanently, §11.4).

I tried to break Appendix G's own claims and could not:

- **Item 2 is not circular.** Its hash input is [0, F − 64) followed by the trailer's first 60
  bytes with `file_id` zeroed. Every one of those 60 bytes — including `committed_file_length` — is
  determined before `file_id` is chosen, because item 3 fixes placement and item 4 fixes the
  generation. Checked against my own file: at the point I would compute it, `dir_offset`,
  `dir_length` and F were all known.
- **Item 3's ordering key is total where it needs to be.** Two records the key does not separate
  agree in type, flags, `inline_length`, `extent_length`, inline payload and extent contents, and
  differ only in `extent_offset`. Since their extents have equal length and equal content,
  emitting them in either order places the same bytes at the same offsets and produces
  byte-identical headers. The claim "emitting them in either order yields the same file" holds.
  The masking of `extent_offset` is likewise necessary and the profile explains why.
- **Item 3's start position is well defined** even under a declared alignment: the first structure
  goes at 16, or at the least position above 16 the declaration admits — and since A ≥ 512, an
  aligned layer's first stored tile lands at A. If the first layer stores no tile, its index region
  is not alignment-constrained and goes at 16.
- **Item 10's arithmetic is right**: `température` is 12 bytes NFC, 13 NFD (verified).

The one thing I could not classify cleanly is writer-injected metadata content — a writer that
stamps `tarn.created` or `tarn.creator` of its own accord produces a different document from one
that does not, and item 9 pins the *serializer* rather than the content. I did not report it,
because §18.4 makes every standardized key OPTIONAL and the document is entitled to treat the
document's content as caller input rather than writer freedom. It is a note, not a finding.

Appendix G is non-normative and adds no requirement to any actor, so nothing in this section
could have been byte-level even had I falsified something. I found nothing to falsify.

---

## 8. Findings

### writer-01 — §20.5 never binds a compactor to the commit protocol, so neither its durability barriers nor its pre-trailer pad length are fixed

**Kind:** AMBIGUITY. **Byte-level:** yes.

**Location:** §20.5 (`[R-WRT-06]`, `[R-WRT-07]`, `[R-WRT-09]`), against §20.1 (`[R-WRT-01]`),
§20.2 (`[R-WRT-02]`), §20.3 (`[R-WRT-04]` step 6), §9.2 (`[R-LIF-02]`), §6.2 (`[R-CNT-05]`).

**Quotation.** §6.2, `[R-CNT-05]`:

> Those bytes — the **pre-trailer pad** — are slack (§5.2): a writer that ends its directory on a
> 64-byte boundary leaves none, this specification does not constrain their content, and bounds
> their number only through step 5 of the commit protocol, which pads to the next 64-byte boundary
> (`[R-LIF-02]`) — a longer gap is conforming, and no conforming commit produces one.

And §20.1, `[R-WRT-01]`, which is where the tiers are separated:

> - **creator** — emits a complete file in one commit, generation 1: the minimal conforming writer.
> - **appender** — extends an existing file by commits (§9.2) […]
> - **compactor** — rewrites a file whole under a new identity (§20.5), reclaiming slack.

And §20.2, `[R-WRT-02]`, whose binding is on *a creator*:

> A creator MUST follow `[R-LIF-02]`'s creation path: […] then the barrier, the pad, the
> generation-1 trailer with a fresh nonzero file_id (§9.3), and the barrier that makes the trailer
> durable (`[R-LIF-02]` steps 4–6 — both barriers, not one).

**The problem.** `[R-LIF-02]` is invoked by name for a creator (§20.2) and for an appender (§20.3
step 6: "**Commit** (`[R-LIF-02]` steps 4–6): barrier; pad; trailer …; barrier"). I grepped every
occurrence of `[R-LIF-02]`, "barrier" and "durable" in the file: **§20.5 contains none of them.**
A compactor is a third, separately defined tier, `[R-LIF-01]` classifies its output as a
whole-file rewrite rather than a commit, and `[R-WRT-01]` binds it only to "every writer
requirement for the bytes they produce" plus §20.4's preservation obligations.

Two readings are defensible.

*Reading A.* A compactor emits a new file at generation 1, which is precisely what `[R-LIF-02]`'s
creation path describes ("On creation there is no prior trailer: the writer first emits the front
signature block … then performs steps 2–6, writing beginning at offset 16, with generation 1").
So the creation path binds it: both barriers, and a pad of exactly (−dir_end) mod 64 bytes.

*Reading B.* §20.1 makes the tiers disjoint; §20.2's rule binds "a creator"; §20.5 states the
compactor's procedure and its obligations exhaustively — down to which trailer fields it must
write — and never mentions barriers or the pad. Under this reading a compactor owes no durability
ordering at all, and `[R-CNT-05]`'s "bounds their number **only** through step 5 of the commit
protocol" leaves its pre-trailer pad **unbounded**, because it is not performing a commit. The
sentence's own qualifier — "no conforming *commit* produces one", not "no conforming *writer*" —
reads as though it were written with exactly this case in mind, which is what makes reading B
hard to dismiss.

**Which I picked.** Reading A, because the alternative removes the format's central durability
guarantee from one of its three writer tiers for no stated reason. But I picked it on
design-sense, not on text: nothing in §20.5, §20.1 or §9.2 says a compactor performs a commit or a
creation, and `[R-WRT-01]`'s "every writer requirement for the bytes they produce" cannot settle
it, since a barrier is not a requirement about bytes and the pad's *length* is.

**What an implementer does wrong without it.** Two things, one silent and one on disk.

(i) *Durability.* A compactor under reading B may write its trailer before its relocated tile
payloads are durable. It crashes; the output file has a valid trailer, a valid directory, and one
or more tiles whose bytes never reached the medium. Those tiles fail their entry crcs (T1) — the
damage is detected, which is the whole point of §8's chain — but the operator now holds a file
that *looks* committed and is not, at the exact moment they are deciding whether to delete the
input. §9.2's Note earns the guarantee "torn commits are invisible … §8's chain still catches
every inconsistent state loudly" for commits; a compactor under reading B gets neither half.

(ii) *Bytes.* Name the two implementations. Compactor **P** (reading A) pads from the directory's
end to the next 64-byte boundary and emits F = 4,096 for some input. Compactor **Q** (reading B)
aligns its trailer to the storage device's 4 KiB block for its own direct-I/O reasons, pads
3,392 bytes further, and emits F = 8,192 with a 3,452-byte pre-trailer gap. Both output files are
*conforming files* — `[R-CNF-02]` names "§6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's
pad" among the writer obligations whose violation is expressly not a file-conformance
violation — so a reader's verdict cannot separate them and `[R-CNF-05]` cannot settle it. What
differs is whether **Q is a conforming compactor**, which is exactly what the byte-level test
asks: resolving this changes which byte sequences a conforming implementation may emit. Under
reading A, Q's file is a file no conforming compactor may produce; under reading B it is one any
may.

I grade this byte-level and I want to be honest about its shape: the durability half is the
consequential half and is not byte-level, while the byte half is real but reachable only by a
compactor that *wants* a longer pad. I do not think that is contrived — trailer-to-block alignment
is an ordinary reason to want one, and §16.1's own Note ("4096 — the page size and modern physical
sector size") shows the document takes such reasons seriously elsewhere.

**Repair shape** (offered as a locator, not a demand): one clause in §20.5 stating whether a
compactor follows `[R-LIF-02]`'s creation path, in the same register §20.2 uses for a creator.

---

### writer-02 — §20.5 keys index-region regeneration on the region being relocated, when the operative trigger is that the region's tiles were relocated

**Kind:** AMBIGUITY. **Byte-level:** no.

**Location:** §20.5, `[R-WRT-07]`.

**Quotation.**

> A compactor MUST preserve content, and preserves no placement — placement is not among the
> things it carries forward, and it is free to place structures anywhere §5.2 admits and every
> declared layout invariant permits (`[R-SLB-01]`, `[R-SLB-03]`): every stored tile's bytes
> verbatim — each index entry's crc is unchanged — and every retained record per §20.4, except
> that relocation re-points extent slots, regenerates each relocated tile-index region (entry
> offsets new; entry lengths, entry crcs, and sentinel entries unchanged; segment CRCs recomputed
> over the entries as re-emitted), and updates the layer-record fields covering a regenerated
> region (crc_of_crc_array).

**The problem.** What forces an index region to be regenerated is not that the *region* moved — it
is that the *tiles the region addresses* moved. The sentence's grammar attaches "relocated" to
"tile-index region", and the following paragraph ("Regenerating a region means classifying every
entry in it…") restates no trigger of its own, so the whole of the regeneration obligation hangs
on the region having been relocated. The exception clause is closed ("except that …"), so on a
literal reading a region that is *not* relocated must be preserved as a retained record's extent
would be — unchanged — even though its entries no longer describe reality.

**Is the case reachable?** Yes, and by a perfectly ordinary compactor. §20.5 imposes no emission
order (that is Appendix G item 3's job, and Appendix G is non-normative and is a *creator's*
profile). Take an input laid out `[front][index_A at 16][slack][tile_A0][tile_A1][dir][pad][tr]`.
A compactor that emits index regions before payloads packs it as
`[front][index_A at 16][tile_A0][tile_A1][dir][pad][tr]`: index_A is at offset 16 in both, so it
is not relocated, while both tiles move. Under the literal reading nothing obliges regeneration,
and the output's entries point at the input's tile offsets — bytes that are now other structures
or slack.

**Permitted readings.** (a) Regenerate exactly the regions that were relocated. (b) Regenerate
every region any of whose entries' targets moved — which is what the parenthetical "entry offsets
new" describes and what `[R-WRT-06]`'s "Given a conforming input the output is a conforming file"
requires.

**Which I picked, and why this is not byte-level.** (b), because the file predicate settles it: a
region carrying stale offsets violates `[R-CNT-13]` (extents owned exactly once; overlap), or
§15.3's bounds rows, or T1 at minimum, so reading (a)'s output is not a conforming file and
`[R-CNF-05]`/`[R-CNF-06]` bar a conforming compactor from emitting it. The emittable set is
therefore unchanged, and I grade this not byte-level. What it costs is an implementer's afternoon:
§20.5 is the section a compactor is written from, and its regeneration trigger is the one thing
in it a reader would not think to double-check against the file predicate.

---

### writer-03 — §21.7's account of obligations with no single-file witness omits the commit protocol's durability barriers and the whole of §20.4's preservation regime

**Kind:** OBSERVATION. **Byte-level:** no.

**Location:** §21.7, `[R-ERR-01]`, second paragraph; against §9.2 (`[R-LIF-02]` steps 4 and 6),
§20.4 (`[R-WRT-05]`, `[R-WRT-08]`, and the preservation table).

**Quotation.** §21.7:

> A second set of obligations is omitted from the register because a single file exhibits no
> witness of their violation. Committed-prefix immutability and the generation sequence
> (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a file's history, which §9.7 does not
> reconstruct; the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a
> structurally valid tile whatever values it carries […]

**The problem.** The paragraph is an enumeration, and it is the document's only account of which
MUSTs the register deliberately does not cover. At least two families of MUST-level obligation
belong in it and are absent:

1. **`[R-LIF-02]` steps 4 and 6 — the two durability barriers, and the step ordering itself.** A
   commit that skips both barriers, or that writes its trailer before its directory, produces a
   file byte-identical to one that did neither. There is no witness, in one file or in any number.
   These are not "conduct" rules in `[R-CNF-02]`'s sense either: `[R-CNF-02]` names the conduct
   category as §10.3's and §18.3's publication rules plus obligations "whose violation this
   specification expressly declares not to be a file-conformance violation", of which it says
   §6.3's flags and §6.2's pad "are the cases this text states". Barriers are neither. They are a
   third class — an obligation about *how the bytes reached the medium* — that §21.7's two classes
   (wrong content; properties of history) do not name.
2. **§20.4's preservation table, `[R-WRT-05]`'s byte-identical re-emission, and `[R-WRT-08]`'s bar
   on re-encoding an unimplemented record.** These are the most consequential updater MUSTs in
   Part III, and every one of them is a property of the relation between two generations. An
   updater that silently drops a PE = 1 record, or that re-encodes an unknown record's extent,
   leaves a file that is perfectly conforming and carries no trace of what it lost. §21.7's
   "properties of a file's history, which §9.7 does not reconstruct" is precisely the right
   description of them, and names only `[R-LIF-01]` and `[R-LIF-03]`.

§20.4's own Rationale sharpens the point rather than answering it: "byte-identity makes
preservation testable — the records of adjacent generations differ exactly by those modified,
added, or dropped". Testable across *two* files. §24 says "Each vector is one file plus a manifest
entry", so the corpus cannot exhibit it and `[R-ERR-02]`'s coverage obligation has nothing to
reach.

**Which reading I picked, and why this is only an OBSERVATION.** §21.1 disclaims completeness for
this subsection in terms — "neither this completeness clause nor the instance arithmetic below
reaches §21.6's defined non-violations, §21.7's account of what no check detects, or §21.9's
limits" — so an omission here is not a violation of a normative completeness duty the way an
omission from §21.2–§21.5 would be. I therefore read the paragraph as a non-exhaustive account,
and I report it because the document elsewhere treats it as the canonical place to look:
§20.5 ends "Neither obligation has a witness in the output alone (§21.7)", §17.3 ends "undetectable
by construction (§21.7)", §20.3 says "§21.7 records the consequence", and §16.2's Note handles
`[R-SLB-04]` in place with the explicit words "carries no register row of its own". Every other
no-witness obligation in the document is either listed in §21.7 or given an in-place note of that
kind. §20.4's and `[R-LIF-02]`'s are given neither.

**What an implementer does wrong without it.** A writer implementer using §21.7 to decide which of
their obligations any test could ever catch will conclude that preservation and durability are
testable. They are not, from a file. The practical consequence is that these two families need
implementation-level testing (two-generation diffs, crash injection) that nothing in the document
tells the implementer to build — which is exactly what §21.7 exists to tell them.

---

### writer-04 — §23.1 enumerates two ways a commit removes sample data and omits the third, which is the one a user calls "delete"

**Kind:** OBSERVATION. **Byte-level:** no.

**Location:** §23.1, `[R-PRV-01]`; against §20.3 step 4 (`[R-WRT-04]`) and §23.2 (`[R-PRV-03]`).

**Quotation.** §23.1:

> A commit removes sample data two ways — superseding it, and a shrink that de-addresses tiles
> (§20.3 step 4) — and a dropped ancillary record's extent (§20.4) goes the same way; no commit
> removes a layer at all.

Against §20.3 step 4, which names three dispositions for entries in a re-emitted region and treats
the second as distinct from the first:

> with entries for tiles this commit stores or supersedes written to their new state, entries for
> tiles that become unstored written as the sentinel, entries new to this generation (added tiles,
> grown extents) emitted per §15

**The problem.** **Unstoring** a tile — replacing a live entry with the sentinel, so that the tile
reads as fill and its payload becomes slack — is a third way a commit makes sample data
unreachable, and §20.3 step 4 lists it as its own case rather than folding it into "supersedes".
It is also the operation a caller most naturally invokes when they say *delete this data*: it
writes no replacement bytes, it is what a "clear this region" API compiles to, and it is the
single most likely thing to be *reported to a user as an erasure*, which is precisely what
`[R-PRV-01]` exists to forbid.

§23.2 knows about it — "a tile unstored by a later commit leaves its earlier payload in the file as
slack (§23.1)" — and points back at §23.1, where it is not among the two ways.

**Which reading I picked.** That the rule's force is unimpaired: `[R-PRV-01]`'s MUST is quantified
over "any commit that makes sample data unreachable", not over the enumerated two, so an updater
that reports an unstore as erasure violates it regardless. Not byte-level, and not a
contradiction, because the enumeration is a gloss on a rule whose own quantifier is general.

**What an implementer does wrong without it.** A writer implementer building a "delete region"
operation reads §23.1, sees supersede and shrink, does not see the operation they are actually
implementing, and ships a UI that calls it erasure. The section is one paragraph long and its
entire purpose is to stop that.

---

### writer-05 — R8's Instances cell collapses alternatives that §18.2 states separately and that R7 enumerates, leaving the bare-token form of a non-finite number with no vector

**Kind:** OBSERVATION. **Byte-level:** no.

**Location:** §21.5, row R8; against §21.1's instance rules, §18.2 (`[R-MTA-04]`), §21.8
(`[R-ERR-02]`), §24 (`[R-VEC-03]`).

**Quotation.** R8:

> | R8 | A user-metadata document contains a non-finite number, in any form — a magnitude whose
> binary64 interpretation overflows (`1e400`) and the bare tokens `NaN`, `Infinity` and
> `-Infinity` alike | top-level document; layer sub-record document | reader | extent use |
> `[R-MTA-04]` (R-CNT-25) |

Against §18.2's own statement of the rule, which joins the two forms with *or* and flags the second
as the hazardous one:

> A document is unreadable if it contains a number whose binary64 interpretation is not finite —
> which covers a magnitude that overflows on conversion, `1e400` being the ordinary case — or any
> of the bare tokens `NaN`, `Infinity`, or `-Infinity`, which RFC 8259 does not admit and some
> parsers accept regardless.

**The problem.** §21.1 says an instance "names a field the condition ranges over, a container it
can occur in, one of several alternatives the condition text states, or any combination of the
three", and that a row "whose members give the condition materially different shapes enumerates
them (T15, T25)" while one "whose check ranges over a family without the condition changing shape
states that range as a single instance (T24's *any codec*)". R8 takes the T24 route with the word
"alike", giving 2 instances (the two containers). Its sibling **R7**, drawn from the same bullet
list in §18.2, takes the other route: "not well-formed JSON; top-level value not an object;
leading U+FEFF", each × 2 containers = 6.

The two forms R8 collapses are not one shape. `1e400` is a *conversion* failure inside a
syntactically valid JSON number; `NaN` is a *lexical* token RFC 8259 does not define at all. They
sit on opposite sides of the parser, and §18.2 itself separates them and adds the operational
warning that "some parsers accept regardless" — which is true and specific: several widely used
JSON libraries accept the bare tokens by default while correctly failing to represent `1e400` as a
finite double.

**Consequence.** §21.8 obliges "one vector per instance", and §24's `[R-VEC-03]` inherits it. A
corpus built mechanically from R8's cell contains two vectors, and both may legitimately use
`1e400`. An implementation whose JSON parser accepts bare `NaN` — the single most common way to be
wrong about `[R-MTA-04]`'s third bullet — passes the corpus and is nonconforming. R7's cell, by
contrast, forces a vector for each of its three shapes.

**Which reading I picked, and why it is only an OBSERVATION.** §21.1 states only two axes (layout
formulas, and magnitude direction) as "stated rather than judged each time"; every other axis is a
judgement, so R8's judgement is *permitted* by the letter of §21.1 even though it is inconsistent
with R7's on the same bullet list. And the governing rule is not in doubt: `[R-MTA-04]` makes all
four forms unreadable, so no reader's verdict and no writer's bytes are at stake. This is a
corpus-coverage defect, not a rule defect, and I grade it accordingly.

---

## 9. What I checked and did not report

I record these so the transcript shows where effort went, and so that a later round does not spend
it again.

- **§21.2's preamble.** Its claim that exactly four rows reach a foreign-major file, because their
  subjects are fields `[R-CNT-24]` fixes across every major — F8, F1's trailer-magic instance,
  F14, and F6 with F1's front-block instance. I checked every other candidate against
  `[R-CNT-24]`'s three fixed positions (magic at F−64, major/minor at F−56, CRC at F−4, plus the
  constant front block): F13's 64-alignment, F15's reserved bytes at [56,60), F17's
  committed_file_length at [40,48) and F19's flags at [12,16) all sit in the 48 redefinable bytes,
  and F5's 128-byte floor rests on major-1's directory minimums. The preamble is right, including
  its treatment of F18 as "outside the premise" rather than an exception.
- **§21.5's preamble** against §18.2 and `[R-MTA-10]`: the quarantine's three carve-outs
  (experimental encoding; a reader's or verifier's decline on the size bound; the same on the
  frame's declared window) match §18.2 clause for clause, and the insistence that encoding 0 and
  the reserved range stay violations under R1 while `[R-MTA-10]` withdraws only the *content*
  rules is consistent with `[R-MTA-03]` and `[R-EXT-03]`.
- **R4's sixteen instances** against §18.2's carried-over list. Eight frame constraints × two
  containers, with exactly the two the passage says carry no witness (undisclosed dictionary use,
  and the buffer-sizing bar) correctly absent, and no window instance because §18.2 removes the
  window constraint. It agrees with T17–T22's treatment of the same constraints for a tile,
  allowing for the layout axis that a document does not have.
- **§18.2's Single_Segment_Flag paragraph.** A document between 8 MiB and 16 MiB framed
  single-segment has Window_Size = content size > the §21.9 window guarantee while staying inside
  the document guarantee. The passage anticipates exactly this and resolves it ("§21.9's
  user-metadata row bounds a document's decoded size; it does not relieve the frame carrying it of
  the `Window_Size` row"), and tells a writer what to do instead. I looked for the gap and it was
  already closed.
- **§20.3 step 4's declaration-change bar** against every layer declaration a commit could touch.
  The enumerated list omits pad bits, but the rule says the list "names where that effect arises
  rather than standing on its own" and the governing test — anything §14 fixes for a stored tile —
  reaches `[R-SER-05]`'s pad-bit clause; and §20.3's own figure (c) names pad bits explicitly.
  A same-element-size type change (int32 → float32) alters nothing §14 fixes and is permitted,
  which is coherent because `[R-TYP-04]` makes a value its bit pattern; uint8 → bool in an
  interleaved layer *does* engage `[R-SER-08]` and is barred and witnessed by T2; bool ↔ uint8 in
  a planar layer changes the decoded size and is barred and witnessed by T3/T14. The identity-filter
  carve-out ("a filter whose mandated stride makes it the identity") is real — `[R-COD-10]` makes
  filter 2 the identity on a packed bool plane — and correctly stated.
- **`[R-COD-10]`'s divisibility claim** ("The decoded image's length L is divisible by s in every
  case"): planar numeric L = P·Bᶜ with s = Bᶜ; interleaved L = P·Q with s = Q; packed bool s = 1.
  True in all three.
- **The MU/PE matrix** for both scopes, all eight cells, walked in §3.3 above. Complete, with the
  authority-of-flags question answered before the table rather than after it.
- **Torn-write behaviour** at five points, in §5 above. Every state I could reach is already a
  registered row, and §9.5's Note explains why residue past a completed commit needs no row of its
  own.
- **Slab and alignment invariants** for a writer: `[R-SLB-03]`'s packing relation is decidable from
  index entries plus F, sentinels and structurally-invalid entries are transparent to it, an
  entry failing only its payload crc is not, and `[R-SLB-04]` makes re-establish-or-clear the
  updater's obligation with `[R-SLB-03]`'s rows as its detection. §16.2's Note says the stale
  declaration therefore carries no row of its own, which is the in-place treatment I found
  *missing* for `[R-WRT-05]` in finding writer-03.
- **The whole of Appendix G**, item by item, in §7 above. No falsifiable claim; no unclosed
  divergence I could defend as a defect.

## 10. Confidence

Medium-high that an implementation built from this document alone interoperates. Every byte of my
file was determined by a rule I could cite, every constant the document states reproduced, and
every one of its worked examples came out right. The three places I had to reason past the text
are the compactor's commit protocol (writer-01), the compactor's regeneration trigger
(writer-02), and — for testing rather than for bytes — what §21.7 leaves unaccounted (writer-03).
Only the first can move bytes, and only in one of the three writer tiers.


---

*Editorial substitution for the repository vocabulary gate: one ordinary-English
use of a gate word was replaced with an exact synonym at line 457 ("the re-emitted
index region's prior extent"). The walk's reasoning and its byte accounting are
unchanged. Rounds 19, 22 and the round-24 audit each required the same treatment;
the substitution is recorded here rather than made silently.*
