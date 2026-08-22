# Round 19 — Writer/updater implementer, verbatim working transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in four `Read` calls covering lines 1–4365 (the whole document). I ran
`grep`/`sed` against that file only, and local Python that reads no project
file (CRC-32C, byte layout, register arithmetic). I did not open `docs/`,
`conformance/`, `PLAN.md`, `AGENTS.md`, `README.md`, `spec/registry.json`, or
git history, and I did not list the round-19 output directory.

**One breach to disclose, unintentional.** My scratch files went into the
*shared* scratchpad root, not an isolated subdirectory. A concurrently running
agent overwrote my `build.py` between my run of it and a later
`exec(open('build.py').read())`. That exec therefore ran another agent's script
and I saw four lines of its stdout:

```
          g1: F=  704 slack=   47    6.7%
          g2: F= 1152 slack=  367   31.9%
          g3: F= 1600 slack=  815   50.9%
   compacted: F=  832 slack=   47    5.6%
```

That is another agent's own byte arithmetic on a different toy file. It
contains no specification text, no finding, and no verdict, and nothing in my
walk below derives from it — every number below is recomputed from scratch in
an isolated directory (`scratchpad/wr-iso/w.py`). I report it because a
disclosed breach is usable and an undisclosed one is not. I did not
deliberately read any other agent's file and I did not list the round-19
transcript directory.

**Cross-checks I ran against the document before trusting my own code.** All
passed, so my CRC and my parse of the layout tables are the document's:

| Constant | Document | Computed |
|---|---|---|
| CRC-32C(`"123456789"`) §4.5 | `0xE3069283` | `0xE3069283` |
| CRC-32C(zero bytes) §4.5 | `0x00000000` | `0x00000000` |
| CRC of 4 sentinel entries §7.4 | `0x80A34955` | `0x80A34955` |
| crc_of_crc_array of that §7.4 | `0xC4EE982E` | `0xC4EE982E` |
| CRC of 2¹⁶ sentinels §15.4 | `0xEECB3BB2` | `0xEECB3BB2` |
| Appendix A trailer CRC | `0xE00938D2` | `0xE00938D2` |
| §7.4's 81-byte layer payload | listed byte for byte | reproduced byte for byte |
| §21.8's "121 conditions over 273 instances" | 121 / 273 | 121 / 273 (36+49+26+10; 58+116+55+44) |

The §7.4 reproduction is the important one: it means my reading of the layer
record's field order, widths and packing is exactly the document's, so the file
I build below is not built on a private guess about the central structure.

---

## 1. Creation: a byte layout, in emission order

I built a two-layer file with a file-scope metadata record, a layer-scope
metadata sub-record, a slab-declared layer, a sparse tile, edge padding in both
layouts, and a packed boolean plane — enough to exercise most of Part I and
Part II at once.

**Layer `sst`** — interleaved, rank 2, dims `y`(E=5,T=4) `x`(E=5,T=4), so
G=(2,2), N=4, P=16 (§11.2). Channels `temp` float32 fill `0x7FC00000`, `ok`
bool fill `0x01`. Q = 4+1 = 5 (§14.2), decoded size P·Q = 80. codec 1, filter
1, A=0, S=0. Ordinals 0,1,2 stored; ordinal 3 the sentinel (§15.2), so
coordinate (4,4) reads fill.

**Layer `mask`** — planar, rank 1, dim `x`(E=20,T=8), G=3, N=3, C=1 channel `m`
bool fill `0x01`. Packed boolean plane (§14.3): decoded size ⌈8/8⌉ = 1 byte per
tile. Slab S=2, A_slab=64. entry_count = C·N = 3 (§11.2). All three stored.

Every decision below is tagged **[fixed]** where the document determined it and
**[free]** where it left the choice to me.

### 1.1 Ordering decisions

* Front signature block at [0,16) — **[fixed]** §6.1, and `[R-LIF-02]`'s
  creation path puts it first.
* Everything else at ≥ 16 — **[fixed]**: `[R-CNT-06]` dir_offset ≥ 16,
  `[R-CNT-13]` extent_offset ≥ 16, §15.3 row `offset < 16`.
* Payloads, index regions and record extents before the directory — **[fixed]**
  by `[R-LIF-02]` steps 2–3 plus `[R-CNT-05]` ("no structure lies between its
  end and the trailer"): the two together force every non-directory structure
  into `[16, dir_offset)`.
* Directory, then pad to the next 64-byte boundary, then trailer — **[fixed]**
  `[R-LIF-02]` step 5. Where the directory already ends 64-aligned the pad is
  zero-length (§6.2, "a writer that ends its directory on a 64-byte boundary
  leaves none"). My generation 2 below hits that case exactly.
* *Which* structure goes where inside `[16, dir_offset)`, and in what order —
  **[free]**, `[R-SLB-05]`. I adopted Appendix G item 3's total order so the
  same file could serve the divergence audit in §5: layers in ascending
  layer-name byte order (`mask` < `sst`), each layer's stored tiles in
  disk-ordinal order then its index region, then the remaining record extents
  (top-level first, then each layer record's sub-records), then the directory.
* Record order inside the directory — **[free]**, `[R-CNT-14]` ("Record
  semantics MUST NOT depend on record order"). I used type-ascending, layer
  records tied by name.

### 1.2 The generation-1 layout

```
  structure       byte range        len    why it is where it is
  GAP             [    16,    64)    48    A_slab=64 admits no stored tile at 16
  mask.tile0      [    64,    65)     1    run 0 first stored tile, 64 | 64   [R-SLB-03]
  mask.tile1      [    65,    66)     1    packed onto tile0                  [R-SLB-03]
  GAP             [    66,   128)    62    run 1 must start 64-aligned
  mask.tile2      [   128,   129)     1    run 1 first stored tile
  mask.index      [   129,   193)    64    3*20 + ceil(3/2^16)*4              [R-CNT-17]
  sst.tile0       [   193,   273)    80    decoded size P*Q, codec 1          [R-COD-04]
  sst.tile1       [   273,   353)    80
  sst.tile2       [   353,   433)    80
  sst.index       [   433,   517)    84    4*20 + 4                           [R-CNT-17]
  meta.file       [   517,   581)    64    JSON doc + terminal CRC-32C        §8.1
  meta.sst        [   581,   669)    88    JSON doc + terminal CRC-32C
  directory       [   669,   953)   284    3 records + CRC-32C                §7.1
  PAD             [   953,   960)     7    to the next 64-byte boundary       [R-LIF-02]#5
  trailer         [   960,  1024)    64
F = 1024   F mod 64 = 0   dir_offset = 669   dir_length = 284
inline_length(mask) = 76   inline_length(sst) = 131
```

Field values I had to fix and the rule that fixed each:

| Field | Value | Source |
|---|---|---|
| front block | `89 54 41 52 4E 0D 0A 1A` + 8 zero | §6.1 **[fixed]** |
| trailer magic | `8A 4E 52 41 54 0D 0A 1A` | §6.2 **[fixed]** |
| version_major | 1 | §6.2 **[fixed]** |
| version_minor | 0 | `[R-CNT-26]` floor, a SHOULD **[fixed-by-advice]** |
| flags | 0 | `[R-CNT-08]`, creator under this text **[fixed]** |
| generation | 1 | `[R-LIF-02]` creation path **[fixed]** |
| file_id | any nonzero | `[R-CNT-06]`; source SHOULD be a CSPRNG (`[R-LIF-03]`) **[free]** |
| reserved [56,60) | zero | §6.2, `[R-CNT-24]` **[fixed]** |
| trailer CRC | over [0,60) | §6.2 **[fixed]** |
| layer record flags | `0x0003` (MU=1,PE=1) | §7.3 registry table **[fixed]** |
| user-metadata record flags | `0x0002` (MU=0,PE=1) | §7.3 **[fixed]** |
| layer extent slot | (index region offset, formula length) | `[R-CNT-17]` **[fixed]** |
| index_encoding | 1 | §7.4 / §10.2 **[fixed]** |
| linearization | 1 | `[R-GEO-05]` — "writers MUST NOT emit any other value" **[fixed]** |
| metadata inline payload | one byte, encoding = 1 | `[R-MTA-03]` **[fixed]** |
| gap content | zero | `[R-CNT-03]` SHOULD **[free]** |

Two content obligations bit at creation, and both were fully determined:

* **§14.5 padding.** `sst` tile 1 covers x = 4..7, of which x = 5,6,7 are
  padding, and tile 2 covers y = 4..7 with y = 5,6,7 padding. Each such
  position carries `00 00 C0 7F 01` — `temp`'s recorded fill bytes followed by
  `ok`'s recorded fill byte (`[R-SER-05]`, "the recorded fill bytes for a
  numeric channel, the recorded fill byte for an interleaved bool channel").
* **§14.3 packed plane.** `mask` tile 2 covers x = 16..23; x = 20..23 are
  padding positions, taking the plane's fill *bit* (1). With the four real
  positions false, the byte is `F0`. P mod 8 = 0, so this tile has **no pad
  bits** — §14.3's Note is exactly right that a plane can have many padding
  positions and no pad bits, and I needed both halves of `[R-SER-05]` to be
  stated separately to get this byte. Tiles 0 and 1 are `55` and `00`.

Nothing in §14, §15 or §16 left me guessing at creation. The one place the
document had to be re-read twice was §14.2 versus §14.3 for a bool channel: the
same type serialises as one byte interleaved and as one bit planar, and the
element size of 1 governs the *fill field* in both cases (§12.1's closing
sentence, "a bool's element size of 1 governs its fill field (§13.2) and its
interleaved byte (§14.2)"). That sentence is load-bearing and it is there.

### 1.3 Durability and the commit point

`[R-LIF-02]` fixes the whole schedule and it is unambiguous: front block, then
steps 2–3 (payloads/index/extents, then the complete directory and its CRC),
then **barrier**, then pad + trailer, then **barrier**. §20.2 restates it with
the emphasis that matters — "both barriers, not one".

The commit point is the moment the trailer's 64 bytes become visible at the
physical end of file: from that instant a reader taking the final 64 bytes
(§9.5) sees generation 1. Durability of that point is step 6. Note a
consequence the document gets right by construction: **the pad need not be
durable before the trailer**, because the pad is slack and §5.2 puts no
requirement on slack content. A crash that lands the trailer but leaves the pad
as filesystem zeros still yields a conforming file.

---

## 2. The append procedure

### 2.1 Generation 2, worked

Operation: supersede `sst` ordinal 1, and add a layer `grad` (rank 1, E=4, T=4,
interleaved, one uint8 channel, one stored tile).

Step order per `[R-WRT-04]`:

1. **Establish F** — validate the trailer in the final 64 bytes (`[R-LIF-04]`).
   F = 1024.
2. **Open** — §19.1's four steps (`[R-RDR-01]`).
3. **Validate what the commit touches** — `[R-WRT-03]`: trailer and full
   directory always; §19.3 layer validation for `sst` (modified) and not for
   `mask`; §19.4's index chain for every `sst` segment whose entries I reuse.
   `mask`'s index chain is neither modified nor relied on, so it imposes
   nothing. I read `[R-WRT-03]`'s "the trailer and the full directory always —
   re-emission (§20.4) relies on every directory byte" as open-depth over the
   whole directory, **not** §19.3 depth on every layer, because the very next
   clause adds §19.3 "for every layer whose record, index, or extents the
   commit modifies" — which would be redundant under the other reading. That is
   an inference, but the structure forces it.
4. **Write payloads and indexes**, beginning at exactly F.
5. **Re-emit the directory** per §20.4.
6. **Commit** — barrier, pad, trailer at generation 2 with the same file_id and
   the ignore-lane bits copied forward, barrier.

```
=== GENERATION 2 (appended at F = 1024) ===
  sst.tile1'    [  1024,  1104)     80    new payload
  grad.tile0    [  1104,  1108)      4
  grad.index    [  1108,  1132)     24    1*20 + 4
  sst.index'    [  1132,  1216)     84    re-emitted in full  [R-WRT-04] step 4
  directory2    [  1216,  1600)    384    4 records + CRC
  (no PAD: 1600 mod 64 = 0)
  trailer2      [  1600,  1664)     64
F2 = 1664   dir_offset = 1216   dir_length = 384
```

`mask`'s record is carried into directory2 byte-identically, extent slot and
all, so it still addresses `mask.index` at 129 — `[R-WRT-05]`, and §5.1's
three-commit example says the same thing in pictures. `sst`'s record is *new
output*: its extent_offset moves to 1132 and its crc_of_crc_array is recomputed
over the new segment-CRC array. Its `inline_length` is unchanged (131), which I
asserted in code — a useful invariant, since crc_of_crc_array is a fixed-width
field.

Inside `sst.index'`, entries 0 and 2 are byte-identical to the old region's,
entry 1 is re-pointed with a new crc, and entry 3 is still the sentinel. That
is `[R-WRT-04]` step 4 verbatim, and it is the whole 84-byte region that moves
because one extent slot addresses it.

### 2.2 Appending to a file whose records I do not all understand

The record flag space is bit 0 MU, bit 1 PE, bits 2–15 reserved (§7.2). Walking
every combination, at each of the two scopes a record can occupy, for a type
the updater does not implement (§20.4's table is explicitly the
does-not-implement case):

| Stored flags | Top-level record | Layer sub-record |
|---|---|---|
| **MU=1, PE=1** | `[R-CNT-15]`: unknown top-level MU=1 is **reject-file**. §20.4: "At file scope no commit is available at all". The updater is a reader first (§2.3), so it refuses before modifying anything. Compaction is barred too (`[R-WRT-06]`). | `[R-CNT-18]`: **reject-layer**. §20.3 step 2: "reject-layer bars a commit that modifies that layer" — every *other* layer stays editable, and I may add a new layer to such a file. The record is retained byte-identical. |
| **MU=1, PE=0** | `[R-CNT-12]`: "a reader or updater encountering it MUST treat the record as PE = 1". Behaves as MU=1/PE=1 above. Separately a violation whose detector is the verifier (F25). | Same, via L46. |
| **MU=0, PE=1** | Retain byte-identical, extent content unmodified. Ignored for reading (`[R-CNT-15]`). Its extent stays where it is: `[R-WRT-05]` re-emits the slot byte-identically and `[R-LIF-01]` freezes the bytes it points at. | Same, at layer scope (`[R-CNT-18]`). |
| **MU=0, PE=0** | Retain, **or** drop — but only "in a commit that *independently* changes the scope the record attaches to": the file's layer set, any layer record's content, or another non-layer top-level record. My generation 2 qualifies twice over (a new layer; `sst`'s record content changed). Dropping SHOULD be reported. | Retain, or drop where the commit independently changes that layer's record, its index entry set, or which of its tiles are stored. |
| **reserved bits 2–15 set** | Readers MUST ignore them; writers MUST emit zero; the verifier records F26/L47. As an updater I neither clear nor honour them — `[R-WRT-05]` carries the whole header forward byte-identically, reserved bits included. | Same. |

For a type the updater *does* implement but this document does not register,
§20.4 says the flags come from "the definition it implements the type from" and
"the stored bits never do". So an updater implementing experimental type
`0x8001` as MU=0/PE=0 may drop it even where the file stores MU=1/PE=1 — a
sharp rule, clearly stated, and one I would have got wrong from §7.2 alone.

Two asymmetries an implementer must not smooth over, both stated:

* An unknown **MU=1 sub-record on layer A** bars only commits that modify layer
  A, but bars **compaction of the whole file** — `[R-WRT-06]` says "any record
  whose type it does not implement with MU = 1", with no scope qualifier.
* An appender may **never** remove a layer record or a user-metadata record at
  either scope (§20.4, both registered types carry PE=1), so "delete a layer"
  is not an append at all; it is a whole-file rewrite under a fresh file_id.

### 2.3 A consequence of slabs that only shows up when you write

`mask` declares S=2, A_slab=64. Suppose a later commit supersedes `mask` ordinal
1. Run 0 is ordinals [0,2). `[R-SLB-03]` requires the run's stored tiles to be
"contiguous and packed in ordinal order — each stored tile's offset equals the
previous stored tile's offset plus its length". Ordinal 0 sits at 64 and its
bytes are frozen (`[R-LIF-01]`), so the new ordinal-1 payload cannot be placed
at 65. **The commit must therefore re-emit ordinal 0 as well**, at a fresh
64-aligned pair of offsets, stranding both old payloads — or clear the slab
declaration, which `[R-SLB-04]` explicitly offers ("or clear the declaration in
the new generation; carrying a stale declaration forward is a validity error at
layer scope"). Both branches are determined; nothing here needed a guess. It is
worth saying out loud that a slab declaration converts any single-tile
supersede into a whole-run rewrite, which §20.3's cost note does not mention
(it quantifies only the index cost).

---

## 3. Slack, by commit shape

`[R-CNT-21]`: slack is every byte the live committed state does not claim; its
content is unconstrained; a verifier that reaches a live state MUST report the
total, and readers never count it. Only compaction reclaims it (§20.5).

Measured on my file:

```
generation 1: F = 1024, claimants 907  ->  slack 117 (11.4%)
              = 48 (A_slab gap) + 62 (A_slab gap) + 7 (pre-trailer pad)

generation 2: F = 1664, claimants 1035 ->  slack 629 (37.8%)
              new slack this commit = 512
              = 80 superseded sst tile
              + 84 old sst index region
              + 284 old directory
              + 64 old trailer
              (+ 0 new pad: directory2 ended 64-aligned)
              (the old 7-byte pad was already slack)
```

Claimants counted per §9.7: front block, each record's extent (which is where
each tile-index region enters, once, as its layer record's extent), the stored
extent of each non-sentinel index entry, the directory, the live trailer.

| Commit shape | Which bytes become slack | Counted by | Permitted content |
|---|---|---|---|
| **append, new layer only** | old directory + old pad + old trailer, plus any alignment gap the new placement opens | verifier (§9.7) | anything; writers SHOULD zero (`[R-CNT-03]`) |
| **append, tiles added to an existing layer** | the above **plus** that layer's whole prior index region | same | same |
| **append, tiles superseded** | the above **plus** every superseded payload; on a slab layer, plus every other stored payload of each touched run (§2.3) | same | same |
| **append, extent shrink** | the above **plus** every de-addressed tile's extent (§20.3 step 4: "the de-addressed tiles' extents become slack") | same | same |
| **append, MU=0/PE=0 record dropped** | that record's extent (§20.4) | same | same |
| **in-place update** | *does not exist.* `[R-LIF-01]` freezes [0,F). The only writes below the new F are `[R-LIF-04]`'s "overwrite from F", which touches bytes that were never in any committed state | — | — |
| **whole-file rewrite (fresh file_id)** | none in the output; the input file is untouched and persists as a separate artifact (`[R-PRV-02]`) | verifier, on each file separately | — |
| **compaction** | only the output's own alignment gaps and pre-trailer pad; "slack is never carried" (§20.5) | verifier | as above |
| **abandoned partial write** | *no slack at all, because there is no live state.* §5.2: "Where §6.2's ordered validation rejects the file before a live trailer is established there is no F and no live state to walk, so the total is not owed at all". The bytes past the last good F are residue, not slack | nobody | unconstrained, but the file is nonconforming |

That last row is the one I expected the document to fumble and it does not:
`[R-CNT-21]` distinguishes "not a partial total but the absence of one", and
§20.5's example separately notes that truncating residue and recovering to an
earlier boundary "also shorten a file, but neither reclaims any [slack]" —
correct, because in both cases the removed bytes were never claimed *or* slack
under any live state.

---

## 4. Torn-write recovery, six points

All offsets are my generation-2 commit: gen 1 ends at F = 1024; gen 2 occupies
[1024, 1664).

**P1 — crash after step 2 wrote `sst.tile1'` (physical length 1104).**
Next reader: takes the final 64 bytes, [1040,1104). 1104 mod 64 = 16, so even a
lucky trailer-magic match inside my payload dies at F13/F17
(committed_file_length must be a multiple of 64 and equal the transport size).
Verdict **reject-file**; `[R-LIF-05]` forbids scanning backward.
File conforming? **No** — `[R-CNT-01]` requires the file size to equal the live
trailer's F and there is no valid live trailer.
Next updater: §9.4 — validation fails, the file is torn, "the writer MUST NOT
append". §9.6's deliberate probe walks 64-aligned offsets downward from
o = 1040 and lands on o = 960: magic matches, CRC verifies,
committed_file_length = 1024 = o + 64. Truncate to 1024, re-verify the whole
file (§8, `[R-LIF-06]`'s first caution), then append.

**P2 — crash after step 3 wrote `directory2` (physical 1600).**
1600 mod 64 = 0 so the alignment gate passes, but the eight bytes at 1536 are
directory bytes, so F8 fires. Identical recovery to P1. Note that the *whole*
new payload set and directory are on disk and byte-intact and are simply
unreachable — which is the property §9.2's example is drawing.

**P3 — crash midway through step 5's trailer write (physical 1632).**
The probe's own bound saves it: §9.6 begins "at the largest 64-aligned offset o
with o + 64 ≤ the physical file length", i.e. 1568, so the half-written trailer
at 1600 is never even a candidate (1600 + 64 = 1664 > 1632). Recovery reaches
960 again.

**P4 — crash after step 5 but before step 6's barrier.**
Two possible on-disk states. (a) The trailer bytes survived: the file is a
complete, conforming generation 2 and a reader sees it. (b) They did not:
identical to P2. A third sub-case matters only if the writer skipped step 4's
barrier and the storage reordered — trailer durable, directory not — and then
§9.2's note holds: the directory CRC fails (F20), reject-file, loudly, and
recovery to 960 still works. "Torn commits are detected", never silently
accepted.

**P5 — crash after step 6.** Nothing torn. F = 1664, generation 2, conforming.

**P6 — a completed commit that is nevertheless unreadable.** `[R-LIF-04]` lets
a writer "overwrite from F and truncate the physical file to the new
committed_file_length **no later than step 6**". Take an earlier abandoned
write that left the physical file at 2000 bytes, then this commit overwriting
from 1024 and crashing after the trailer is durable at [1600,1664) but before
the truncate. Physical length 2000, 2000 mod 64 = 16: the reader takes
[1936,2000), fails, and reports the file torn — a *completed* commit that no
conforming reader can open. Recovery probes down from 1936 and finds gen 2's
trailer at 1600 (CRC valid, committed_file_length 1664 = 1600 + 64), truncates
to 1664, and generation 2 is restored. §9.5's Note names exactly this state and
correctly declines to give it a register row of its own, since the reader meets
it as an ordinary trailer-gate failure.

**Concurrent readers.** Throughout P1–P4 a reader that opened *before* the
commit holds generation 1's trailer as its snapshot and every byte it reaches
is immutable, so its session stays consistent (§9.5, `[R-LIF-05]`). Only a
reader *opening* inside the window fails. §9.5's second Note says so and gives
the deployment answers.

---

## 5. Byte-divergence catalogue

Two conforming writers, identical input arrays, identical stated options
(tiling, layout, channel types, fill values, codec, filter). Every way their
bytes may legitimately differ, and whether Appendix G closes it.

| # | Degree of freedom | Rule that leaves it open | Closed by |
|---|---|---|---|
| 1 | `file_id` | `[R-LIF-03]` (nonzero; random is a SHOULD) | **G item 2** — derived from a named hash over [0, F−64) ++ trailer[0,60) with file_id zeroed; last eight digest bytes; `1` substituted if all zero. No circularity: the trailer CRC is computed after. Closed. |
| 2 | Placement of structures inside [16, dir_offset) | `[R-SLB-05]` | **G item 3**. Closed. |
| 3 | Order of structures | `[R-SLB-05]` | **G item 3** (layers by name; tiles by disk ordinal; index after tiles; remaining extents after all layers; directory last). Closed. |
| 4 | Size of gaps between structures | `[R-SLB-05]` | **G item 3** ("each later structure begins where the previous one ended, save where alignment forces a gap"). Closed. |
| 5 | Content of gaps and of the pre-trailer pad | `[R-CNT-03]` (SHOULD) | **G item 3** ("every byte of every such gap is zero — `[R-CNT-03]`'s advice, taken as a requirement here"). Closed. |
| 6 | Record order in the directory | `[R-CNT-14]` | **G item 3** (type, then layer name / masked-header key). Closed. |
| 7 | Sub-record order inside a layer record | `[R-CNT-14]`, `[R-CNT-18]` | **G item 3** (same key, applied within each layer record). Closed. |
| 8 | Compressed stream bytes for codecs 2–4 | `[R-CNF-05]`; §17.2's Note on DEFLATE's unused final-byte bits | **G item 1**, by pinning implementation, version and settings — and item 1 concedes byte-identity *across* implementations is unattainable for 2–4. Closed as far as it can be, and honestly labelled. |
| 9 | Filter value | `[R-COD-09]` leaves 1 or 2 to the writer | **G item 5**. Closed. |
| 10 | Declared alignment / slab | §16 leaves them to the writer | **G item 5**. Closed. |
| 11 | Whether an all-fill tile is stored or sentinel | nothing requires the sentinel | **G item 6**. Closed. |
| 12 | Fill recorded when the caller chooses none | `[R-TYP-10]` (SHOULD all-zero) | **G item 7**, which correctly notes this reaches further than eight bytes, because item 6 makes the fill decide *which tiles exist*. Closed. |
| 13 | `version_minor`, `flags` | `[R-CNT-26]` (SHOULD), `[R-CNT-08]` | **G item 8**, for a creator. For a compactor, see finding writer-02. |
| 14 | JSON serialisation of user metadata (whitespace, escaping, number formatting) | `[R-MTA-05]` sorts members and explicitly promises nothing else | **G item 9**, by pinning the JSON writer, plus the storage encoding and the zstd producer where encoding 2 is used. Closed. |
| 15 | Unicode normalisation of names | `[R-ENC-14]` (SHOULD NFC) | **G item 10**, which correctly observes this changes `inline_length` and `dir_length`, not just the name. Closed. |
| 16 | Number of generations | §9 nowhere constrains it | **G item 4**. Closed. |
| 17 | Segment-CRC shortcut for a full all-sentinel segment | `[R-IDX-05]` (a MAY) | **Not a divergence at all** — the constant *is* the CRC, so both paths emit the same four bytes. I checked: CRC-32C over 2¹⁶ sentinels is `0xEECB3BB2`. No item needed. |
| 18 | Where the first structure begins under a declared alignment | G item 3's own carve-out | **G item 3** ("at the least position above it the declaration admits"). In my file that is 64, leaving a 48-byte zero gap, which the profile then fixes as zeros. Closed. |

I could not construct a divergence in this list that Appendix G leaves open,
and I could not falsify its central claim about the ordering key. I did try:
the key for a non-layer record is "the record's header with extent_offset
masked to zero, then its inline payload, then the contents of its extent", and
the worry is that some component is placement-dependent, which would restore
the circularity the mask exists to remove. In format major 1 it is not:
`extent_length` and `inline_length` are content lengths; §7.2 guarantees an
MU=0 record's inline payload and extent contents "encode offsets or lengths of
other file bytes" nowhere; and the one MU=1 type that *does* carry offsets —
the layer record, whose inline payload holds `crc_of_crc_array` and whose
extent is the offset-bearing index region — never reaches those components,
because type 0x0001 ties by layer name first. That is a real load-bearing
detail and it holds. (It would stop holding the moment a later minor registers
an MU=1 type carrying references, which §7.2 permits; the profile is scoped to
this document, so I record it as an observation rather than a finding.)

I also verified item 3's claim that two records the key does not separate can
be emitted in either order for the same file: such records are byte-identical
in every field but `extent_offset`, and their extents are byte-identical and
equal-length, so swapping both the records and their extents reproduces the
same directory bytes. The claim is correct.

Two claims in the profile that I checked and found true rather than
falsifiable: item 2's "re-deriving it on an already-compact input would
reproduce the input's own `file_id`" (it would — the body and every other
trailer field would be identical), and item 8's concession that a compactor's
output is "reproducible only modulo its trailer" (file_id and version_minor are
the only non-derived trailer fields, and neither appears anywhere else in the
file).

---

## 6. Findings

### writer-01 — §23.1's closed enumeration of how a commit removes sample data omits unstoring, which §23.2 names and refers back to §23.1 for

**Kind:** AMBIGUITY. **Location:** §23.1, `[R-PRV-01]`; cross-read with §23.2
`[R-PRV-03]` and §20.3 step 4 `[R-WRT-04]`.

Quoted, §23.1:

> "A commit removes sample data two ways — superseding it, and a shrink that
> de-addresses tiles (§20.3 step 4) — and a dropped ancillary record's extent
> (§20.4) goes the same way; no commit removes a layer at all."

The enumeration is closed ("two ways") and carries its own closure argument
("no commit removes a layer at all"), which forecloses the layer-removal route.
But §20.3 step 4 — the very passage cited — uses a **three-way** vocabulary:

> "entries for tiles this commit stores or supersedes written to their new
> state, entries for tiles that become unstored written as the sentinel"

*Superseded* and *becomes unstored* are distinguished there. Unstoring a tile
that remains addressed (writing the sentinel over a live entry) is neither a
supersede nor a shrink: the grid count is unchanged, no tile leaves the
addressed set, and the old payload becomes slack. §23.2 names exactly this
route and points the reader back at §23.1 for it:

> "a tile unstored by a later commit leaves its earlier payload in the file as
> slack (§23.1)"

A second route is also outside a narrow reading: reducing a **planar** layer's
channel count. The bar of §20.3 step 4 quantifies over what §14 fixes for
prior-generation stored tiles, and dropping a channel alters nothing §14 fixes
for the surviving planes (each plane's decoded size is P·Bᶜ, independent of C;
`[R-GEO-06]`'s c·N + s renumbers entries without changing any plane's content),
so the commit is permitted and the dropped plane's extents become slack. That
is not an extent shrink, and §20.3 step 4's "shrink" is stated of an extent
("An extent MAY also **shrink**").

Permitted readings: (a) "superseding it" is §5.2's broad sense — any commit
that supersedes *bytes* — in which case the list is complete but collides with
§20.3 step 4's narrower usage, which §23.1 cites; (b) "superseding it" is
§20.3 step 4's narrow sense, in which case the closed list is short by one
route that §23.2 names and by arguably a second. I picked (b), because §23.1
cites the passage that draws the distinction and because §23.2 treats the
unstore as a separate thing needing its own mention.

What an implementer does wrong without it: `[R-PRV-01]`'s prohibition is
scope-widened to "any commit that makes sample data unreachable", so a careful
implementer is still bound; but a writer building the erasure-warning path from
the enumeration — the natural way to read a closed two-item list — omits the
warning for a sentinel-overwrite commit, which is precisely the operation a
user is most likely to *call* "delete this tile".

**Byte-level: no.** `[R-PRV-01]` binds how a tool represents an operation, not
what it emits. No byte and no verdict moves.

### writer-02 — §20.5 conditions a compactor's version_minor on a fact the compactor cannot establish, and the rule itself says so

**Kind:** AMBIGUITY. **Location:** §20.5, `[R-WRT-06]`.

Quoted:

> "Where the output carries a feature a later minor defines and this compactor
> does not — on a conforming input a carried ignore-lane bit (§6.3) or an
> unrecognized `tarn.` key in a record it never decoded (§18.3), the two of
> §10.1's four vehicles §21.6 makes conforming, the other two reaching such a
> file only as values this text still registers as reserved-range violations
> (F36, L25, R1) — the output's version_minor SHOULD be at least the input's
> ... Otherwise version_minor follows `[R-CNT-26]`'s floor."

I checked the closure argument and it holds: of §10.1's four vehicles, only new
ignore-lane bits and new `tarn.` keys can sit in a *conforming* file under this
text (§21.6's rows for each), while new record types and new reserved-range
values are violations here (F36/L25 for record types, R1 for metadata
encodings — and, uncited but equally, L31/L33/L34/L36/L43/L45 for the other
reserved-range spaces). The enumeration is sound.

The problem is the antecedent, not the enumeration. The rule's own text says
the second case arises "in a record it never decoded". A compactor's
verification depth is `[R-WRT-09]`'s, which reaches each relocated extent's
checksum and no document content, and `[R-MTA-02]` forbids metadata from
influencing anything structural — so the ordinary compactor genuinely has no
way to decide whether the output carries an unrecognized `tarn.` key. Faced
with a conforming input at version_minor = 3, no ignore-lane bit set, and one
user-metadata extent it has verified but not decoded, the two branches give
different bytes:

* **Reading A** — the compactor observes no carried feature, so "Otherwise"
  applies and it writes `[R-CNT-26]`'s floor, 0.
* **Reading B** — it cannot rule the antecedent out, so it takes the
  conservative branch and writes max(floor, 3) = 3.

I picked B for my implementation, on the ground that B satisfies the SHOULD in
every case and A satisfies it in only some, and because §20.5's stated harm ("a
lower minor understates the file's feature floor to tooling") is one-directional
while the mirror harm is already priced by `[R-CNT-26]` as costing readers
nothing. But the document does not say to; and a compactor could equally decode
the document, which nothing forbids and `[R-WRT-09]` merely does not require,
and then decide the antecedent properly. The document does not say whether
adopting that extra depth is expected.

What an implementer does wrong without it: writes a trailer whose version_minor
misstates the feature floor of every compacted file carrying later-minor
metadata keys, and cannot tell from the text that it did.

**Byte-level: no.** The two readings emit different `version_minor` bytes and
hence different trailer CRCs, but both files are conforming: `version_minor` is
the single **descriptive** field of format major 1 (`[R-ENC-16]`) and
`[R-CNT-07]` says "A reader MUST NOT reject a file for its version_minor". The
governing modal is SHOULD, which `[R-CNF-12]` places outside the register
entirely, so no accept/reject verdict moves and `[R-CNF-05]` already licenses
two conforming writers to differ here.

### writer-03 — §21.7 says §20.5 places two obligations on a compacted file's trailer; `[R-WRT-06]` places four, and the two it omits are equally unwitnessed and accounted for nowhere

**Kind:** OBSERVATION. **Location:** §21.7 `[R-ERR-01]`, against §20.5
`[R-WRT-06]`; bears on §21.1's completeness contract and §2.3 `[R-CNF-02]`.

Quoted, §21.7:

> "§20.5's two obligations on a compacted file's trailer (`[R-WRT-06]`) — the
> unknown ignore-lane bits it MUST carry forward, and the floor its
> version_minor SHOULD take — are unwitnessed for that same reason, the output
> carrying no record of its input's flags or its input's minor"

`[R-WRT-06]` states four obligations on the output trailer, not two. Quoted,
§20.5:

> "It MUST mint a fresh file_id for the output — a new draw under §9.3's
> randomness advice, not merely a value compared against the input's — and
> generation 1"

plus the two §21.7 names. The fresh-`file_id` MUST and the generation-1 MUST
are unwitnessed on exactly §21.7's own stated ground: the output carries no
record of its input's `file_id`, and no record that it is a compaction output
at all, so neither can be checked from the output alone.

This matters because §21.1 makes §21.7 the load-bearing account rather than
prose colour:

> "a *detectable* file-conformance violation this specification names and the
> register omits is a defect in this document, detectability being the gate
> `[R-CNF-07]` already applies and §21.7 the account, by class, of what fails
> it"

and because §2.3 closes the other escape hatch by enumeration:

> "§6.3's flags = 0 against a set ignore-lane bit and §6.2's pre-trailer gap
> longer than `[R-LIF-02]` step 5's pad are the cases this text states"

so `[R-WRT-06]`'s fresh-`file_id` and generation-1 MUSTs are not declared
conduct rules either. They fall between the register (which does not carry
them), §21.7's account (which counts them out), and §2.3's conduct list (which
does not name them).

There is a defensible repair reading — that §21.7's earlier clause,
"Committed-prefix immutability and the generation sequence (`[R-LIF-01]`,
`[R-LIF-03]`) are properties of a file's history, which §9.7 does not
reconstruct", already swallows them, leaving "two" to mean the two *remaining*.
I do not think a reader gets there unaided: §21.7 cites rule identifiers
precisely everywhere else, `[R-WRT-06]` is not `[R-LIF-01]` or `[R-LIF-03]`,
and a compacted output's relation to its input is not that output's *history*
in this format's sense — it is a different file_id at generation 1, and §9.3's
own caching rule treats a different file_id as "a different file".

What an implementer does wrong without it: a verifier author reading §21.7 as
the complete account of §20.5's unwitnessed trailer obligations concludes the
fresh-`file_id` MUST is witnessed and looks for a check that cannot exist. The
cost is small; the reason I report it is that §21.1 makes the account's
completeness a contract, and this is a countable claim in text rewritten this
cycle.

**Byte-level: no.** Every reading leaves a compactor with the same four MUST/
SHOULD obligations and leaves a verifier with the same set of checkable rows.
Nothing about which bytes may be emitted or which files must be rejected turns
on it.

### writer-04 — §21.7 places a SHOULD deviation in a set of "violations" omitted from the register for want of a witness, where `[R-CNF-12]` already excludes every SHOULD from the register regardless of witness

**Kind:** OBSERVATION. **Location:** §21.7 `[R-ERR-01]`, against §2.4
`[R-CNF-12]` and §21.1.

Quoted, §21.7's opening of the paragraph in question:

> "A second set of obligations is omitted from the register because a single
> file exhibits no witness of their violation."

and, in the same paragraph, listed as a member of that set:

> "the floor its version_minor SHOULD take"

Against §2.4:

> "Deviation from a SHOULD is not a violation for this purpose: §21's register
> enumerates MUST-level conditions only, and a verifier reports a SHOULD
> deviation as an advisory that does not bar certification."

"For this purpose" is exactly the purpose §21.7's paragraph is about — register
membership. So the version_minor floor is omitted from the register because it
is a SHOULD, and would be omitted even if a perfect witness existed; the reason
§21.7 gives for it is true but inoperative, and it describes a SHOULD deviation
as a "violation", which `[R-CNF-12]` says it is not.

Permitted readings: (a) "their violation" is loose shorthand covering both
MUST-level conditions and SHOULD deviations, and the sentence is merely
imprecise; (b) §21.7 is asserting that this SHOULD would be registrable but for
the missing witness, which contradicts `[R-CNF-12]`. I take (a) as intended and
(b) as what the words say. I implemented (a).

What an implementer does wrong without it: a verifier author reads §21.7 as
licence to treat the version_minor floor as a register-adjacent condition —
either hunting for it, which `[R-CNF-12]` says a verifier owes no search for
("A verifier owes no search for one"), or reporting it as a finding rather than
an advisory, which `[R-CNF-12]` forbids ("does not bar certification").

**Byte-level: no.** It changes no emittable byte and no verdict — at most it
changes an advisory line in a verifier's report.

### writer-05 — §20.4's licence to drop an MU=0/PE=0 top-level record does not say whether *adding* a non-layer top-level record counts as changing one

**Kind:** AMBIGUITY. **Location:** §20.4, the MU = 0 / PE = 0 row of the
updater-obligations table (bound by `[R-CNF-06]`, which requires an updater to
"honor the preservation obligations of §20.4").

Quoted:

> "An appender MUST NOT drop it except in a commit that *independently* changes
> the scope the record attaches to: for a layer sub-record, that layer's
> record, the entry set of its index, or which of its tiles are stored; for a
> top-level record, the file's layer set, any layer record's content, or
> another *non-layer* top-level record. A commit changes the layer set by
> adding a layer; an appender never removes one."

For the layer-set limb the row says explicitly that **adding** counts. For the
top-level-record limb it does not. The row does close the neighbouring hole —

> "Dropping the record, or dropping another record in the same commit, is not
> itself such a change, so a commit whose only effect would be the drop MUST
> retain it."

— but that clause is about drops, not adds.

The case is reachable in format major 1: a file carrying an experimental-range
MU=0/PE=0 top-level record and no file-scope user-metadata record, and a commit
whose only effects are to add the user-metadata record and to drop the
experimental one. Permitted readings: (a) adding a non-layer top-level record
changes the file's top-level record set and therefore counts, by parallel with
the layer-set sentence and with the row's evident test (does the commit do
something to the scope besides the drop?); (b) "changes ... another *non-layer*
top-level record" governs an existing record being modified, and a record that
did not exist before is not "another" one, so the drop is barred and the
appender MUST retain the record. I implemented (a), because the row's own
gloss of the parallel limb ("A commit changes the layer set by adding a layer")
shows the test is meant to be satisfied by additions, and because reading (b)
makes the licence turn on whether the file already happened to carry a
user-metadata record, which is not a distinction anything else in §20.4 draws.

What an implementer does wrong without it: an updater under reading (a) emits a
directory from which the record is absent and lets its extent fall to slack; an
updater under reading (b) is obliged to re-emit the record byte-identically
(`[R-WRT-05]`). The resulting files differ in `dir_length`, in every offset
after the directory, in F, and in the verifier's slack total.

**Byte-level: no, on the rubric I was given, and I want to be explicit about
why I am not reaching for it.** Both outputs are *conforming files*: the drop
licence binds an updater's conduct across two files and has no witness in
either one, exactly as `[R-LIF-01]` and `[R-WRT-06]`'s fresh `file_id` do (and
§21.7 does not list it among the unwitnessed obligations either, though its
list is not offered as exhaustive). `[R-CNF-05]` gates emission on file
conformance, and neither file is nonconforming, so no verdict moves and no
byte sequence leaves or enters the emittable set. What forks is whether a
given tool is a conforming *updater*, which is a real cost to an implementer
and not the same thing.

---

## 7. What I could not determine, summarised

Only the five items above. Everything else in the charter — the creation byte
layout, the append write order and commit point, the durability schedule, the
per-shape slack accounting, the six torn-write states, and the divergence
catalogue against Appendix G — came out of the document without a guess, and
the document's own worked examples (§7.4's layer payload, §11.2, §11.4, §14.2,
§14.3, §14.5, §15.4, §16.2, §17.3, Appendix A) all reproduce exactly. I
deliberately do **not** report as defects: §20.5's citation of §7.2 rather than
§5.2 for "the live committed state" (checked: §7.2's narrower gloss is the one
that makes the sentence true, so the citation is deliberate); the slab-forces-
whole-run-rewrite cost of §2.3 (determined, merely unremarked in §20.3's cost
note); and the fact that a profile-adopting *compactor* cannot enforce items 6,
7, 9 or 10 on content it must carry forward verbatim (checked: this costs no
reproducibility, since every compactor carries the same input the same way, so
item 8's concession stays true as written).
