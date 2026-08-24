# Round 23 — Writer/updater cleanroom walk

**Charter:** implement, on paper but concretely, a conforming *writer and updater*.
**Access:** `spec/tarn.md` only. See the disclosure at the end.

Everything below is the actual walk. Where I computed something I show the
computation; where I guessed I say so and say what I guessed.

---

## 0. Method and tooling

I read the document end to end (4,426 lines) before writing a byte. I then
built three artifacts with a local Python script that reads no files but my own
scratch:

- `gen1.tarn` — a 448-byte file created from nothing (one layer, two stored
  tiles, two sentinels, one file-scope user-metadata record).
- `gen2.tarn` — the same file after one append that adds a second layer
  (planar, slab-declared, mixed bool/uint8) and supersedes a tile of the first.
- a paper compaction of `gen2.tarn`.

I implemented CRC-32C from the parameters in `[R-ENC-09]` (Castagnoli
0x1EDC6F41, reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) rather
than from any library, and gated it on §4.5's check vector before using it.

---

## 1. Constants and worked examples — an independent check

Before trusting the document's arithmetic I recomputed every constant a writer
has to reproduce. All of them verified:

| Claim | Section | Recomputed | Verdict |
|---|---|---|---|
| CRC-32C(`"123456789"`) = 0xE3069283 | §4.5 | 0xe3069283 | ✅ |
| CRC-32C(zero bytes) = 0x00000000 | §4.5 | 0x0 | ✅ |
| CRC over 4 sentinel entries (80 B) = 0x80A34955, stored `55 49 A3 80` | §7.4 example | 0x80a34955 / `55 49 a3 80` | ✅ |
| crc_of_crc_array over that 4-byte array = 0xC4EE982E | §7.4 example | 0xc4ee982e | ✅ |
| CRC of a full all-sentinel segment (2¹⁶ entries, 1,310,720 B) = 0xEECB3BB2 | §15.4, `[R-IDX-05]` | 0xeecb3bb2 | ✅ |
| Appendix A trailer CRC = 0xE00938D2, bytes `D2 38 09 E0` | Appendix A | 0xe00938d2 | ✅ |
| channel entry `temp`/float32/NaN = `04 74 65 6D 70 0C 00 04 00 00 C0 7F` | §12.3, §7.4 | identical | ✅ |
| byte-shuffle of float32 1,2,3 → `00 00 00 00 00 00 80 00 40 3F 40 40` | §17.3 example | identical | ✅ |
| packed bool P=10 alternating, fill false → `55 01`; fill true → `55 FD` | §14.3 example | identical | ✅ |
| §15.4's 1,000,000-entry example: 16 segments (15 full + 16,960), 64-byte array, region 20,000,064 B, entry 999,999 at segment-relative 339,180, segment 15 at region [19,660,800, 20,000,000) | §15.4 | all reproduce | ✅ |
| §11.4's ordinals: (300,700) → tile (1,2), s=10, in-tile (44,188), ordinal 11,452; planar c=2 → 74; entry at [1480,1500) | §11.4, §15.4 | all reproduce | ✅ |
| §14.2's examples: Q=3 size 18, ordinal 5 at [15,18); planar b 12 B ordinal 5 at 10–11; float32+bool Q=5 size 30, ordinal 5 at [25,30) | §14.2 | all reproduce | ✅ |
| §21.9 note: segment-CRC array at 2³² tiles = 256 KiB; 4 MiB at 2³⁶ | §21.9 | 2³²/2¹⁶·4 = 256 KiB; 2³⁶/2¹⁶·4 = 4 MiB | ✅ |
| §21.8: 121 conditions over 277 instances | §21.8 | see §7 below | ✅ |

The §7.4 worked layer-record payload also adds up exactly as the document says
(4 + 34 + 18 + 12 + 13 = 81), and `[R-CNT-17]`'s extent length for it,
4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84, is right.

I found no arithmetic error anywhere in the document. That is worth saying
plainly, because it is what let the rest of the walk proceed without hedging.

---

## 2. Creation byte layout — building `gen1.tarn`

### 2.1 What I chose and what the document chose for me

Design: one layer `sst`, rank 2, dimensions `y` and `x`, extents (5, 5), tile
extents (4, 4), interleaved, one `uint16` channel `v` with fill `0xABCD`,
codec 1 (none), filter 1 (none), no alignment and no slab. Plus one file-scope
user-metadata record under encoding 1.

Geometry, from §11.2:

```
G = (⌈5/4⌉, ⌈5/4⌉) = (2, 2)      N = ∏Gᵢ = 4       P = ∏Tᵢ = 16
addressed-tile count = N = 4     (interleaved)     entry_count = 4
Q = ΣBᵢ = 2                      decoded size = P·Q = 32 bytes
```

Tile s=0 is (t₀,t₁)=(0,0), all 16 positions real. Tile s=3 is (1,1), covering
y,x ∈ 4..7 — one real position (4,4) and 15 padding positions. I stored
tiles 0 and 3 and left 1 and 2 as sentinels, so the file exercises
`[R-SER-05]`'s padding rule, `[R-IDX-02]`'s sentinel, `[R-COD-04]`'s
length equality and `[R-TYP-08]`'s fill read.

Tile 3's decoded image is therefore `2C 00` followed by fifteen copies of
`CD AB` — exactly the shape §14.5's worked example gives for its (5,5)/(4,4)
uint16 layer. That match is reassuring: the document's own example is the
degenerate edge tile, and my independently derived one agrees byte for byte.

**Ordering and placement.** `[R-SLB-05]` and `[R-LIF-02]` step 2 make placement
and order free for a layer declaring neither alignment nor slab. I chose
tiles → index region → metadata extent → directory. §6.2 forces the directory
last among structures ("no structure lies between its end and the trailer"),
and `[R-CNT-05]`/F7 make a violation a verifier-detected file-scope error.

**Final layout (F = 448):**

```
[0,   16)  front signature block           fixed by §6.1 — no choice
[16,  48)  stored tile, disk ordinal 0     placement mine; content forced
[48,  80)  stored tile, disk ordinal 3     placement mine; content forced
[80, 164)  tile-index region (84 B)        placement mine; content forced
[164,227)  user-metadata extent (63 B)     placement mine; JSON serialization mine
[227,374)  directory region (147 B)        placement mine; record order mine
[374,384)  pre-trailer pad (10 B)          length forced by [R-LIF-02] step 5
[384,448)  trailer (64 B)                  offset forced (64-aligned, final 64)
```

`F = 448`, `F mod 64 = 0` ✅ (`[R-CNT-01]`, §6.2).

Index region, 84 bytes = 4 × 20 + ⌈4/2¹⁶⌉ × 4:

```
entry 0  10 00 00 00 00 00 00 00  20 00 00 00 00 00 00 00  88 C8 26 1E   off 16, len 32
entry 1  FF ×16 00 ×4                                                    sentinel
entry 2  FF ×16 00 ×4                                                    sentinel
entry 3  30 00 00 00 00 00 00 00  20 00 00 00 00 00 00 00  8E 1D 9E 8B   off 48, len 32
seg CRC  1B EF 1F E8                                                     over the 80 entry bytes
```

crc_of_crc_array = CRC-32C(`1B EF 1F E8`) = 0x65974DAE, stored `AE 4D 97 65`.

Layer record inline payload, 94 bytes:

```
 0  03 73 73 74                 name  len 3, "sst"
 4  01                          layout 1 = interleaved
 5  01 00                       linearization 1 = row-major
 7  01 00                       codec 1 = none
 9  01 00                       filter 1 = none
11  00 ×8                       A = 0
19  00 ×8                       S = 0
27  00 ×8                       A_slab = 0 (forced by S = 0, [R-CNT-23])
35  02                          rank d = 2
36  01 00                       C = 1
38  01 79  05.. 04..            dim "y", extent 5, tile extent 4      (18 B)
56  01 78  05.. 04..            dim "x", extent 5, tile extent 4      (18 B)
74  01 76  07 00  02 CD AB      chan "v", type 7 = uint16, fill 2 B   (7 B)
81  01                          index_encoding 1
82  04 00 00 00 00 00 00 00     entry_count = 4
90  AE 4D 97 65                 crc_of_crc_array
```

4 + 1+2+2+2+8+8+8+1+2 = 38; + 18 + 18 = 74; + 7 = 81; + 1+8+4 = 94, no residue,
so the sub-record sequence is empty (`[R-CNT-18]`'s exact-parse rule).

Record framing: type `01 00`, flags `03 00` (MU=1, PE=1 — fixed by §7.3's
registry, not my choice, `[R-CNT-22]`), inline_length 94, extent slot
(80, 84).

The user-metadata record: type `02 00`, flags `02 00` (MU=0, PE=1), inline_length 1,
extent (164, 63), inline payload `01` (encoding 1 = none). Document is
`{"tarn.created":"2026-08-24T00:00:00Z","tarn.title":"demo"}` — 59 bytes —
followed by its terminal CRC-32C, so extent_length = 63 ≥ 5 ✅ (`[R-CNT-25]`).
Key order: `tarn.created` < `tarn.title` because at byte 5, `c` (0x63) < `t`
(0x74) — `[R-MTA-05]`'s ascending-UTF-8-bytes rule at every nesting depth.

Trailer: magic, version_major 1, version_minor 0 (`[R-CNT-26]`'s floor),
flags 0 (`[R-CNT-08]`: a creator under this text MUST write 0), generation 1,
dir_offset 227, dir_length 147, committed_file_length 448, file_id
0x0123456789ABCDEF (any nonzero; §9.3 SHOULDs a CSPRNG draw — I used a fixed
value deliberately so the artifact is reproducible), reserved 0, CRC.

### 2.2 The creation write order and its commit point

`[R-LIF-02]`'s creation path, restated by `[R-WRT-02]`:

1. front signature block at 0
2. payloads, index regions, record extents from offset 16, any order
3. complete directory + its CRC
4. **barrier** — steps 1–3 durable
5. pad to the next 64-byte boundary, then the trailer
6. **barrier** — trailer durable

§20.2 is emphatic: "both barriers, not one". The commit point is step 6.
Between 5 and 6 a concurrent reader on the same filesystem may already see the
new trailer; that is fine, because step 4 has already ordered everything it
addresses. Determined.

### 2.3 What the document fixed vs. what it left to me — creation

| Decision | Fixed by | Free? |
|---|---|---|
| front block bytes | §6.1 | no |
| F mod 64 = 0, trailer at final 64 bytes | §6.2 | no |
| directory last among structures | §6.2, `[R-CNT-05]` | no |
| pre-trailer pad **length** | `[R-LIF-02]` step 5 | no |
| pre-trailer pad **content** | `[R-CNT-03]` SHOULD | **free** (I zeroed) |
| structure order and placement | `[R-SLB-05]`, `[R-LIF-02]` step 2 | **free** |
| gap content between structures | `[R-CNT-03]` SHOULD | **free** (I zeroed) |
| record order in the directory | `[R-CNT-14]` | **free** |
| file_id value | §9.3 SHOULD (random), `[R-CNT-06]` (≠0) | **free** |
| version_minor | `[R-CNT-26]` SHOULD | effectively fixed at 0 |
| flags | `[R-CNT-08]` MUST = 0 for a creator | no |
| entry_count, extent_length, crc_of_crc_array | `[R-CNT-17]`, `[R-CNT-23]` | no |
| sentinel bytes | `[R-IDX-02]` | no |
| padding-position content | `[R-SER-05]` | no |
| whether an all-fill tile is stored or sentinel | nothing normative | **free** |
| codec, filter, layout, tiling | writer's choice (§17.2, §17.3, §14.1, §11.3) | **free** |
| fill when the caller chooses none | `[R-TYP-10]` SHOULD (all-zero) | **free** |
| NFC normalization of names | `[R-ENC-14]` SHOULD | **free** |
| JSON serialization details | `[R-MTA-05]` fixes member order only | **free** |

I did not have to guess anywhere in creation. Every byte I wrote is either
forced or explicitly licensed.

---

## 3. The append procedure — building `gen2.tarn`

Commit 2 does three things at once, to exercise the interesting combinations:
supersede `sst`'s tile 0; add a new layer `mask` (planar, C=2, channels `m`
bool fill `0x00` and `w` uint8 fill `0x07`, slab S=4 with A_slab=64); carry the
user-metadata record forward untouched.

### 3.1 Verification depth first (`[R-WRT-03]`)

- trailer + full directory: **always** ("re-emission relies on every directory byte")
- §19.3 layer validation for `sst` (its index is modified) — but *not* for a
  layer the commit does not touch
- §19.4 index chain (crc_of_crc_array + the segment CRC) for every segment
  whose entries the commit **reuses** — here `sst`'s single segment, because
  entry 3 is copied byte-identically

Note what is *not* owed: the appender does **not** re-verify the stored bytes of
retained tile 3. It copies entry 3's `crc` field verbatim and never relies on
the payload. Contrast `[R-WRT-09]`, which does oblige a compactor to verify
"every stored tile's entry crc", because a compactor relocates the bytes. That
asymmetry is stated and correct, and it is the difference between an append
costing O(index) and O(data).

### 3.2 Placement

`mask` declares S=4, A_slab=64. `[R-SLB-02]` partitions each *channel block*
independently: block 0 = ordinals [0,4) (channel `m`), block 1 = [4,8)
(channel `w`); runs never span blocks; run r of a block starts at
block_start + r·S. With S=4 = N, each block is one run.

`[R-SLB-03]`: for every run, the run's stored tiles are contiguous and packed
in ordinal order, and **the first stored tile's offset** satisfies
offset mod A_slab = 0. I store ordinal 0 (the `m` plane of s=0, ⌈16/8⌉ = 2
bytes) and ordinal 4 (the `w` plane of s=0, 16 bytes). Each is the first stored
tile of its run, so each needs a 64-aligned offset.

```
  448   sst tile 0, superseding (32 B)              F1 = 448, writing begins at exactly F
  480   ▓ 32 B gap forced by mask's A_slab
  512   mask ordinal 0, packed bool plane (2 B)     512 mod 64 = 0 ✅
  514   ▓ 62 B gap forced by A_slab
  576   mask ordinal 4, uint8 plane (16 B)          576 mod 64 = 0 ✅
  592   mask tile-index region (8·20 + 4 = 164 B)
  756   sst tile-index region, re-emitted (84 B)
  840   directory (271 B)
 1111   ▓ 41 B pre-trailer pad
 1152   trailer, generation 2                       F2 = 1216, 1216 mod 64 = 0 ✅
```

`mask` inline_length = 100. `sst`'s record changes **only** in extent_offset
(80 → 756) and crc_of_crc_array; entry_count and extent_length are unchanged
(4 and 84), because the geometry did not change.

The user-metadata record is re-emitted **byte-identically**, header, inline
payload and extent slot alike (`[R-WRT-05]`) — its extent stays at [164, 227)
and does not move. An appender may not relocate it; §20.3 step 4 and
`[R-WRT-08]` reserve relocation for compaction.

### 3.3 Slack accounting after commit 2

Live claimants of the gen-2 state, from §9.7's walk:

```
[0,16)      front block           16
[48,80)     sst tile 3            32   (retained, never moved)
[164,227)   user-metadata extent  63
[448,480)   sst tile 0            32
[512,514)   mask m-plane           2
[576,592)   mask w-plane          16
[592,756)   mask index           164
[756,840)   sst index             84
[840,1111)  directory            271
[1152,1216) trailer               64
                        claimed = 744
```

Disjointness verified programmatically. Slack = 1216 − 744 = **472 bytes**,
which decomposes exactly as the rules predict:

- superseded by this commit: old sst tile 0 (32) + old sst index (84) +
  dir₁ (147) + pad₁ (10) + trail₁ (64) = **337**
- alignment gaps this commit created: 32 + 62 = **94**
- this commit's pre-trailer pad: **41**

337 + 94 + 41 = 472 ✅. That is a verifier's reportable total under
`[R-CNT-21]`, and the walk completes, so it is not partial.

### 3.4 Every record-flag combination an updater can meet

My charter asks for all of them. §7.2 defines exactly two flag bits
(bit 0 MU, bit 1 PE) plus reserved bits 2–15. Four combinations, and the
document answers each:

| Stored flags | Type known to me? | What my updater is permitted to do |
|---|---|---|
| any | **registered type** (0x0001, 0x0002) | Registry flags govern, stored bits are ignored for behavior (`[R-CNT-22]`). Both registered types are PE=1, so **neither can ever be dropped**. A stored-bit mismatch makes the file nonconforming (F28/L49) but changes nothing I do. |
| any | type I implement, **unregistered** | Flags come from the definition I implement the type from; stored bits never do (§20.4). Obligations otherwise as below — §20.4's "Persistence governs every record type; only the authoritative source of the flags differs." |
| MU=1, PE=1 | not implemented, **top level** | **No commit at all.** `[R-CNT-15]` makes it reject-file; I am a reader first (§2.3). Compaction barred too (`[R-WRT-06]`). |
| MU=1, PE=1 | not implemented, **sub-record** | Retain byte-identical; I MUST NOT modify *that layer*; other layers stay editable. The file is not rejected (`[R-CNT-18]`). |
| MU=1, PE=0 | not implemented | Read as PE=1 (`[R-CNT-12]`), i.e. identical to the row above at each scope. Never silently deletable. A verifier records the violation (F25/L46); my behavior is unchanged. |
| MU=0, PE=1 | not implemented | Retain byte-identical, extent content unmodified. As an appender I may not even relocate the extent. |
| MU=0, PE=0 | not implemented | Retain, **or** drop — but only in a commit that *independently* changes the scope the record attaches to. Dropping it, or dropping another record, is not such a change, so a commit whose only effect would be the drop MUST retain it. A compactor may drop it whenever it rewrites. SHOULD report the loss. |
| reserved bits 2–15 set | any | Ignore them as a reader/updater; re-emit byte-identically. Verifier records F26/L47. |

Two things I checked rather than assumed:

- Superseding a stored tile *does* license dropping an MU=0/PE=0 record,
  because it re-places the layer's index region, which moves its extent slot
  and so modifies that layer's record. §20.4 spells this out explicitly. It is
  the one non-obvious entailment in the table and the document supplies it.
- "A commit changes the layer set by adding a layer; an appender never removes
  one." So the drop licence at file scope is reachable by *adding* a layer, and
  never by removing one. Also spelled out.

### 3.5 Write order, durability, and the commit point for an append

`[R-WRT-04]` step by step: establish F (validating the trailer at the physical
end — on failure, **no append**, recovery is a separate deliberate operation,
`[R-LIF-04]`); §19.1 open; validate what the commit touches; write payloads and
indexes starting at exactly F; re-emit the directory; then
`[R-LIF-02]` steps 4–6 — **barrier; pad; trailer; barrier**.

Durability ordering: everything in steps 1–3 must be durable *before* the
trailer is written. The commit point is the trailer becoming durable. This is
fully determined and §9.2's note tells me what degrades if my barriers are
weaker than assumed ("torn commits are detected" rather than "invisible") —
which is the right thing to tell an implementer.

### 3.6 Declaration changes across a commit — the four cases I tested

§20.3 step 4's bar is quantified over "any tile that layer stores **in the
generation this commit supersedes**". I worked four cases against it:

1. **Grow (5,5) → (8,8), tile extents (4,4).** Grid counts stay (2,2); the
   index is untouched; the commit touches the directory alone. Stored tile 3's
   padding positions become real. Permitted, and explicitly so: "a position
   that becomes real held that channel's fill and fill is a legal sample
   value." I verified the claim holds in all three sub-cases — padding of a
   stored tile (fixed to fill by `[R-SER-05]`), a sentinel tile (reads as
   fill), and a wholly new grid cell (a new entry, emitted per §15).
2. **Shrink (5,5) → (4,4).** Grid becomes (1,1); tiles 1–3 de-addressed;
   stored tile 3's 32 bytes become slack; entry_count 4 → 1 forces a re-emitted
   index region. Permitted. Stored tile 0's positions are all still real.
3. **Shrink (5,5) → (3,5).** Stored tile 0's row y=3 turns from real into
   padding, so `[R-SER-05]` would now require fill bytes there and the stored
   bytes hold data. **Barred** — and barred whether or not the commit also
   unstores tile 0, because "the quantifier is the superseded generation's".
4. **Reorder two equal-size channels of an interleaved layer with equal
   fills.** Alters "the byte offset of any sample within the decoded tile
   image" for every stored tile → barred. §21.7 correctly says this is exactly
   where the bar has no witness: no content row fires because the padding bytes
   are unchanged when the fills are equal, and no length row fires because the
   decoded size is unchanged. §21.7's "witnessed **only** where…" phrasing
   covers it.

I also confirmed a **filter** change (none → byte-shuffle) is in the bar's list
and, unlike a codec change, is witnessed only by the content rows (T2/T4/T5),
since shuffle preserves length. §21.7's enumeration names decoded size and
codec explicitly, and the filter case falls under the content-row clause that
opens the sentence. Consistent.

### 3.7 Slab invariants across a commit

`[R-SLB-04]` requires re-establishing the invariants or clearing the
declaration. I tested the nastiest case: a 2-D slab layer whose grid shrinks
from (4,4) to (4,2). Under `[R-GEO-06]` the ordinal of tile (1,0) moves from 4
to 2, so run 0 now spans tiles that are not byte-contiguous. The appender must
either re-emit the run's stored tiles contiguously (appending copies and
stranding the originals as slack, since `[R-LIF-01]` freezes them) or clear the
declaration. Determined, and §20.3 says the same thing in step 4's closing
sentence.

I also checked the reverse: a commit that *adds* a slab declaration to a layer
with scattered stored tiles. `[R-SLB-04]`'s trigger list is arguably not
engaged (there was no run partition before), but `[R-SLB-03]` is a file-level
invariant on the new generation, so the output would be nonconforming (L41/L42)
and `[R-CNF-05]` forbids the writer to emit it. No hole.

---

## 4. Slack, by shape of commit

| Commit shape | What becomes slack | Who counts it | Permitted content |
|---|---|---|---|
| **Append (new layer)** | the previous directory, pad and trailer — sized by the file's *layer count*, never by any layer's data — plus any alignment gaps the new structures force | verifier, §9.7, total under `[R-CNT-21]` | unconstrained; writers SHOULD zero (`[R-CNT-03]`) |
| **Append (tiles added / superseded)** | additionally the layer's whole previous tile-index region, and each superseded payload | same | same |
| **In-place update** | does not exist. `[R-LIF-01]` freezes [0, F). Every "in-place" edit is an append; §20.3's shape (c) is the directory-only case | — | — |
| **Rewrite (new file under a fresh file_id)** | nothing in the output; the *input* persists whole until something outside this format deletes it (`[R-PRV-02]`) | — | — |
| **Compaction** | nothing in the output — "so slack is never carried" — except the gaps its own declared layout invariants force and its own pre-trailer pad | verifier on the output | same |
| **Abandoned partial write** | nothing. There is no live state at all: the physical tail is not a valid trailer, so §6.2's gates fail and the file is nonconforming (F8/F17). §5.2 is explicit that where ordered validation rejects before a live trailer is established, "the total is not owed at all" — the verifier reports the trailer failure and nothing about slack. `[R-LIF-04]` obliges the next writer to truncate or overwrite so those bytes never survive into any committed state. | nobody | n/a |

Two sharp edges worth recording:

- **A partial total is an upper bound, never an under-count**, and the verifier
  MUST say which scope or violation stopped the walk. Where a rejected layer's
  rejection was one the walk itself established (L18 overlap, L40–L42
  placement), claimants already enumerated for that layer are **discarded**.
  That is a quantifier I would have got wrong without §5.2 saying it.
- Slack content is a privacy consideration (§23.1), and a shrink that
  de-addresses tiles leaves their bytes readable — writers MUST NOT report it
  as erasure (`[R-PRV-01]`).

---

## 5. Torn-write recovery — four crash points

Taking the gen-2 commit (F₁ = 448 → F₂ = 1216) and crashing at four distinct
points:

**(A) Mid-payload, physical length 700.** The final 64 bytes [636, 700) are
index bytes. Next reader: fetch [F−64, F), magic check fails → reject-file,
"torn", and `[R-LIF-05]` forbids scanning backward. Next updater: `[R-LIF-04]`
fails to establish F → **no append**; recovery is a separate deliberate
operation. Recovery (`[R-LIF-06]`): probe backward at 64-aligned offsets from
the largest o with o+64 ≤ 700, i.e. 636, 576, 512, 448, 384; at o = 384 the
magic matches, the trailer CRC verifies and committed_file_length = 448 = o+64
→ candidate; truncating to 448 restores gen 1 exactly, and the output MUST be
re-verified whole before being trusted. The tool MUST report the candidate it
settled on and how many it rejected. **The file is nonconforming in the
meantime** (F8/F17).

**(B) Directory written, before step 4's barrier.** Indistinguishable from (A)
to any reader: the physical tail still is not a trailer. The barrier's absence
means the directory bytes may not even be on disk; it makes no difference,
because nothing points at them.

**(C) Pad written, trailer torn at k < 64 bytes.** Physical length 1216−k, or
1216 if the filesystem zero-fills. Either the magic is absent (→ (A)) or the
magic is present and the trailer CRC fails → reject-file. Detection is never
silent — this is exactly the case §6.2's note is about.

**(D) Trailer written, step 6's barrier not completed.** Either the trailer
reached durable storage — the commit stands, gen 2 — or it did not, and we are
at (C). The one state that cannot occur is "trailer durable, payloads not",
because step 4's barrier ordered them. This is the whole return on the two
barriers, and §20.2's "both barriers, not one" is the sentence that makes it
implementable.

**A payload that mimics a trailer.** §9.6's first caution. Under live-state
coverage a mimic in slack is inert (nothing enumerates slack), and a recovery
tool that lands on one produces a file that fails whole-file re-verification,
so the probe continues past it. §21.6 records the condition as a defined
non-violation. I confirmed the front-block/trailer magics differ in their first
byte (`89` vs `8A`), so a backward scan can never match the front block.

**Rollback is undetectable in-format.** §9.6 says so and says the remedy is
out-of-band state. Correct and honest.

---

## 6. Byte-divergence catalogue

Two conforming writers, identical input arrays, identical stated options
(tiling, layout, codec, fills, metadata content). Every way their bytes may
legitimately differ, and what the reproducible-writer material (Appendix G)
does about each:

| # | Degree of freedom | Licensed by | Closed by |
|---|---|---|---|
| 1 | Order and placement of structures; size of the gaps between them | `[R-SLB-05]`, `[R-LIF-02]` step 2 | **G item 3** (total emission order, contiguous, first structure at 16) |
| 2 | Content of every gap and of the pre-trailer pad | `[R-CNT-03]` (SHOULD only) | **G item 3** (every gap byte zero, taken as a requirement) |
| 3 | `file_id` | §9.3 (SHOULD random, MUST ≠ 0) | **G item 2** (hash of [0, F−64) ‖ trailer[0,60) with file_id zeroed; last eight digest bytes, LE; 1 substituted if all zero) |
| 4 | Record order within the directory | `[R-CNT-14]` | **G item 3** (by type; 0x0001 by layer name; else header with extent_offset masked, then payload, then extent contents) |
| 5 | Sub-record order within a layer record | `[R-CNT-14]` | **G item 3** (same key, and placement pinned together with order) |
| 6 | Encoder output for codecs 2–4 (incl. DEFLATE's unused final-byte bits) | `[R-CNF-05]`; §17.2's note | **G item 1** (named implementation, named version, fixed settings, thread count included) |
| 7 | Filter value | §17.3 leaves the choice free | **G item 5** |
| 8 | Codec value | §17.2 leaves the choice free | **G item 1** (read through item 5's "likewise") |
| 9 | Declared alignment / slab | §16 leaves it to the writer | **G item 5** |
| 10 | Number of generations | §9 nowhere constrains | **G item 4** |
| 11 | Whether an all-fill tile is stored or sentinelled | no rule at all | **G item 6** |
| 12 | Recorded fill when the caller chooses none | `[R-TYP-10]` (SHOULD) | **G item 7** |
| 13 | `version_minor`; `flags` | `[R-CNT-26]` (SHOULD); `[R-CNT-08]` | **G item 8** (creator's rule for flags) |
| 14 | JSON serialization of user metadata; storage encoding 1 vs 2; zstd settings for encoding 2 | `[R-MTA-05]` fixes member order only | **G item 9** |
| 15 | Unicode normalization of names | `[R-ENC-14]` (SHOULD) | **G item 10** |
| 16 | Segment CRC of a full all-sentinel segment: computed vs. the constant | `[R-IDX-05]` | not a divergence — same bytes either way |
| 17 | Pre-trailer pad **length** in an *appended or created* file | `[R-LIF-02]` step 5 forces the minimum; §2.3 makes a longer gap a conduct violation, not a file one | closed by `[R-LIF-02]` itself |
| 18 | Pre-trailer pad **length** in a **compacted** file | — | **see finding writer-01: I cannot classify this one** |

Claims in the reproducible-writer material I tried to falsify and could not:

- Item 2's derivation is well-founded: every input to the hash (F,
  dir_offset, dir_length, generation, version fields, flags, reserved) is fixed
  before `file_id` is chosen, and the trailer CRC is computed after. No cycle.
- Item 3's tie-breaking claim — "Two records this key does not separate are
  byte-identical … emitting them in either order yields the same file" — holds.
  Masking extent_offset is what makes the key derivable, and two records
  agreeing on everything else produce identical directory bytes under either
  placement, because the *slots* are assigned by position in the emission
  order.
- Item 6 (sentinel for every all-fill tile) is sufficient given item 7: fills
  are pinned, so which tiles are all-fill is pinned, so the stored-tile set is
  pinned.
- Item 8's honesty about a compactor being "reproducible only modulo its
  trailer" is right for the file_id and the minor floor.
- Item 4's weaker claim, that "the appended bytes are" reproducible, survives:
  item 3's order applied to the appended structures with F as the start is
  determinate. I note in passing that item 3 literally says "The first
  structure begins at 16", which an appender has to read as "at F"; that is a
  trivial adaptation and I do not raise it as a finding.

The one thing on that list I could not classify as either legitimate or
forbidden is row 18, which is finding writer-01.

---

## 7. Register instance arithmetic (independent recount)

§21.8's stated total is a changed passage, so I recomputed it mechanically
under §21.1's stated counting rules (semicolon-separated items per Instances
cell; a cell reading `—` is one instance):

```
F rows 36  instances  58
L rows 49  instances 116
T rows 26  instances  55
R rows 10  instances  48
TOTAL     121        277
```

§21.8 says "121 conditions over 277 instances". **Exact match.**

I also spot-audited the individuation rules against the cells, and they hold:
`does not equal` between two magnitudes gives two directions (T14, T22, T3,
L21, L22, F17, F23, L12, L30); `exceeds`/`larger than` gives one (T21, L44,
R10); a checksum or constant comparison gives none (T1, L37, L38, F14, F20,
T17, R2); a nonzero test gives none (T19, L28); layout formulas are enumerated
where the derived quantity varies by layout (T3, T14, T21, T22, L44).

R4's 16 instances decompose exactly as 8 conditions × 2 containers, where the
8 are: magic; skippable frame; second frame; nonzero dictionary ID;
content-checksum flag; trailing bytes; content-size declared larger;
content-size declared smaller. That matches §18.2's carried-over list plus the
two exceptions it replaces, minus the two §18.2 itself says have no witness
(undisclosed dictionary use; the reader-side buffer-sizing bar). Consistent.

---

## 8. §18.2 read as one passage (the encoding-2 rules)

Because the brief flags this as the most-repaired passage, I read it as a whole
rather than rule by rule and wrote out what a writer must actually do.

**What the passage says, assembled:**

1. Encoding 1 stores the document verbatim; encoding 2 stores exactly one
   RFC 8878 frame occupying the extent's bytes *before its terminal CRC*.
2. Encoding 2 inherits **every** `[R-COD-06]` frame constraint, "named here or
   not", **save two**: what `[R-COD-06]` states against a *tile's declared
   decoded size*, and what it states about the frame's *declared Window_Size*.
3. Both exceptions are replaced here:
   - decoded size: there is none, so the bound is the **reader's own**, no
     smaller than §21.9's 16 MiB user-metadata guarantee;
   - Window_Size: unconstrained by any MUST; the reader's window bound is its
     own, no smaller than §21.9's 8 MiB row; writers SHOULD stay within 8 MiB.
   - the **content-size field** is *not* left to the reader: MAY be present,
     and when present MUST equal the decoded document's byte length.
4. Under Single_Segment_Flag, RFC 8878 makes Window_Size the content-size
   field, which is pinned to the decoded length — so a document over 8 MiB
   framed that way exceeds §21.9's Window_Size row and falls outside
   `[R-CNF-03]`'s acceptance duty; a writer that needs one uses a
   Window_Descriptor instead.
5. Everything wrong here is **ignore-record**, never §17.2's tile scope.

**Checks I ran on it:**

- The carry-over list is complete against `[R-COD-06]`. I enumerated
  `[R-COD-06]`'s ten distinct clauses and each is either carried, excepted and
  replaced, or (the "exactly one frame … as defined by RFC 8878" clause)
  restated by §18.2's own opening sentence. Nothing falls through.
- `[R-COD-08]`'s "no trailing bytes" is not a `[R-COD-06]` constraint, so it is
  not carried by the "every frame constraint `[R-COD-06]` places" clause — but
  §18.2's own "occupying the extent's bytes before its terminal CRC" supplies
  it, and R4 registers "bytes remaining after the frame". Closed.
- The **analogy check** the brief asks for. §18.2 justifies the content-size
  rule as "the tile rule of `[R-COD-06]` transposed to the quantity a document
  does have, its decoded length, in place of the declared size it does not."
  Putting the verbs side by side: the tile rule compares FCS against a
  *declaration-derived* quantity known before decoding (header-only check); the
  document rule compares FCS against a quantity known only *after* decoding.
  So the transposition changes when the check is affordable — but not what it
  decides, and R4's row text anticipates this exactly ("a reader that only
  tries decoding establishes none of them"). Both R3 and R4 carry the same
  outcome, the same detector and the same detection point, so nothing byte-
  visible turns on the routing. §24's `[R-VEC-02]` already handles the corpus
  attribution question ("the entry records every row the file exercises and
  says which it was built for"). Not a defect.
- The "same reason"/"same treatment" chain for Window_Size holds: the exception
  exists because there is no declared decoded size to compare against, which is
  the same reason the decode-size bound is the reader's own.
- A large-document writer has a determinate path: encoding 1 for anything up to
  16 MiB (no frame, so no Window_Size instance at all — §18.2 explicitly says
  §21.9's row is over the *decoded* size, "which a verbatim document has as
  surely as a compressed one"), or encoding 2 with an explicit
  Window_Descriptor ≤ 8 MiB. Determined.
- A verifier that declines the decode on either bound reports *cannot
  establish*, must not report the file nonconforming, and SHOULD report the
  bound and the stored extent length. §2.3's cannot-establish list already
  names `[R-MTA-09]`. §21.5's preamble covers both bounds symmetrically where
  §18.2's verifier sentence says only "the bound above"; read together they
  agree, so I did not raise it.

I could not break this passage. Reading the sentences together, it says one
coherent thing.

---

## 9. Compaction — the walk that produced the finding

I worked compaction of `gen2.tarn` end to end. Everything about the **output's
content** is determined:

- only live-state structures, less any record §20.4 licenses dropping
- fresh `file_id`, a **new draw**, not merely a value compared against the
  input's; generation 1
- input's unknown ignore-lane bits copied forward *in place of* the flags = 0
  §6.3 would require of a file created under this text — §6.3 says this
  explicitly, "though its output is a new file"
- `version_minor` ≥ the input's where the output carries a feature the
  compactor does not implement, else `[R-CNT-26]`'s floor
- every stored tile's bytes verbatim; every index entry's `crc` unchanged;
  entry offsets new; sentinels unchanged; segment CRCs recomputed;
  `crc_of_crc_array` updated; extent slots re-pointed
- refuse on any `[R-WRT-09]` check failure, on any unimplemented MU=1 record,
  and on any index entry §15.3 classifies reject-tile on a structural ground
  (`[R-IDX-03]` gives it no extent to re-point, and no drop is available since
  an index entry is no record §20.4's table licenses dropping)

Placing my output under Appendix G item 3's order:

```
[0,16)     front            [16,64)   ▓ 48 B, forced by mask's A_slab
[64,66)    mask ordinal 0   [66,128)  ▓ 62 B, forced by A_slab
[128,144)  mask ordinal 4
[144,308)  mask index
[308,340)  sst ordinal 0    [340,372) sst ordinal 3
[372,456)  sst index
[456,519)  user-metadata extent (relocated; slot re-pointed)
[519,790)  directory (mask record, sst record, metadata record)
[790,832)  ▓ 42 B pre-trailer pad
[832,896)  trailer, file_id = fresh, generation 1
```

F = 896; slack = 896 − 744 = 152 = 48 + 62 + 42 ✅. Reference arrays identical
to gen 2's, bit for bit (`[R-WRT-07]`).

**Where I had to guess.** §20.2 binds the creator to `[R-LIF-02]`'s creation
path by name, including "both barriers, not one". §20.3 binds the appender to
`[R-LIF-02]` steps 1–2, step 3 and steps 4–6 by name. §20.5 binds the compactor
to **no write procedure at all** — I grepped every `[R-LIF-02]` citation in the
document and §20.5 is not among them. So when I wrote the compactor I had to
decide for myself (a) whether I owe the two barriers and (b) how long my
pre-trailer pad may be. See finding writer-01.

---

## 10. Degenerate files I built on paper and checked against the tables

Following round 21's method — legal-but-degenerate files, and what the tables
say about them.

| File | Verdict | Where the document says so |
|---|---|---|
| Zero layers, empty directory, 128 bytes | conforming | §21.6 row; Appendix A |
| Layer with a zero-extent dimension: G contains 0, N=0, entry_count 0, slot (0,0), crc_of_crc_array 0 | conforming; reads return no samples | `[R-GEO-02]`, `[R-CNT-17]`, `[R-CNT-23]`, L22 |
| The same layer declaring **codec 4** with a tile shape whose decoded size exceeds 0x7E000000 | conforming — the cap is quantified over *addressed* tiles, and it addresses none | §17.2's note, L44, and §21.9's matching quantifier |
| …but P·Q and P·Bᶜ are still overflow-checked in that empty layer | yes | §17.2's note; `[R-ENC-04]` "carries no such quantifier" |
| E=(1,), T=(2⁶³−1,), one uint8 channel, single sentinel entry: decoded size 2⁶³−1 bytes in a ~200-byte file | conforming; exceeds §21.9's 256 MiB tile row, so a reader MAY decline **and must report it as a resource limit, not corruption** | `[R-ERR-04]`; §21.9's "ranges over addressed tiles, stored or not" |
| Slab-declared layer that addresses no tile | conforming; blocks are empty, no runs, "a run with no stored tiles imposes nothing" | `[R-SLB-02]`, `[R-SLB-03]` |
| Two layer records whose extent slots address the same index region | reject-file (F33): extents are owned exactly once | `[R-CNT-13]` |
| A stored tile whose extent lies inside the directory region | reject-file, but **verifier-detected only** — a reader passes every `[R-IDX-03]` check and happily decodes directory bytes as samples | `[R-CNT-13]` ("readers are not obligated to detect overlap"), F33 |
| A stored tile between the directory's end and the trailer | reject-file, verifier-only; a reader serves it | `[R-CNT-05]`, F7 |
| entry_count exactly 65,536 | one **full** segment, so `[R-IDX-05]`'s all-sentinel constant applies ("final or not") | §15.4, §15.4's example |
| A minimal file *with* a layer | 192 bytes, not 128: the smallest layer record is 24+73 = 97 bytes, which does not fit [16,64) | derived; §5.1 only claims 128 for the empty file, correctly |
| file_id ≥ 2⁶³ | conforming — `[R-ENC-03]`'s domain covers "every offset, length, extent, and count", and file_id is none of those. F2's instance list correctly omits it | §4.2, §6.2, F2 |

That last one is a deliberate piece of precision I checked because I expected
to find a defect there and did not.

---

## 11. Places where the document had to supply reasoning, and did

Recording these because "obviously X" was my failure mode to guard against.

- The segment CRC array is **not** covered by any segment CRC — it is covered
  by `crc_of_crc_array` alone. §8.1's map says so; I would otherwise have had
  to guess.
- The final partial segment's CRC covers only its actual bytes (§15.4).
- `[R-SLB-03]`'s packing relation reads the **index entry's `length` field**
  (the stored, possibly compressed length), not the decoded size — which is
  what makes the invariant "decidable from the index entries alone".
- Entries §15.3 classifies reject-tile on a *structural* ground are transparent
  to run continuity, and contribute no extent to the coverage walk; an entry
  whose only defect is a failed payload CRC is **not** transparent. That
  distinction appears three times (§15.3, §16.2, §9.7) and is consistent each
  time.
- A record is not a claimant of its own bytes; the directory region is
  (§9.7). A layer record's extent slot addresses the index region, so the
  region enters the walk once (§9.7).
- Whether an appender may drop an MU=0/PE=0 record turns on an *independent*
  scope change, and superseding a tile counts because it moves the layer
  record's extent slot (§20.4). Non-obvious; supplied.
- A verifier's slack total is *not owed at all* when §6.2's ordered validation
  rejects before a live trailer is established (§5.2). I would have reported a
  zero.
- The bar of §20.3 step 4 is quantified over the **superseded** generation, so
  unstoring in the same commit does not escape it (§20.3, twice, once for
  growth and once for shrink).

---

## 12. Findings

### writer-01 — §20.5 binds a compactor to no write procedure, while §20.2 and §20.3 bind the creator and appender to `[R-LIF-02]` by name

**Kind:** AMBIGUITY
**Location:** §20.5 (`[R-WRT-06]`, `[R-WRT-07]`), against §20.2 (`[R-WRT-02]`), §20.3 (`[R-WRT-04]`), §9.1 (`[R-LIF-01]`), §9.2 (`[R-LIF-02]`), §6.2 (`[R-CNT-05]`), §2.3 (`[R-CNF-02]`)

**Quotation.** §20.2:

> A creator MUST follow `[R-LIF-02]`'s creation path: the front signature
> block; … then the complete directory and its CRC; then the barrier, the pad,
> the generation-1 trailer with a fresh nonzero file_id (§9.3), and the barrier
> that makes the trailer durable (`[R-LIF-02]` steps 4–6 — both barriers, not
> one).

§20.3 step 6:

> **Commit** (`[R-LIF-02]` steps 4–6): barrier; pad; trailer with generation
> one greater, the same file_id, unknown ignore-lane flag bits copied forward
> (`[R-CNT-08]`), and version_minor per `[R-CNT-26]`; barrier.

§9.1:

> every conforming mutation of a file is either a commit (§9.2) or a whole-file
> rewrite under a new file_id (compaction, §20). `[R-LIF-01]`

§20.5, in full, mentions no barrier, no pad, and no step order; its only
procedural obligations are refusals and content preservation. §9.2's own
procedure is scoped: "A writer performing a commit MUST, in order: …".

**The two permitted readings.**

*Reading A — `[R-LIF-02]` binds a compactor.* Its output is a generation-1 file
with no prior trailer, which is exactly §9.2's creation path; §20.1 lists the
compactor as a writer tier and `[R-WRT-01]` says it "satisfies every writer
requirement for the bytes it produces". Under A the compactor owes both
barriers and its pre-trailer pad is the minimum to the next 64-byte boundary.

*Reading B — it does not.* `[R-LIF-01]` explicitly contrasts a commit with "a
whole-file rewrite under a new file_id (compaction, §20)", and §9.2's procedure
binds "a writer performing a commit". §20.1 lists *creator* and *compactor* as
distinct tiers, and §20.2's obligation is placed on "A creator". The document
elsewhere goes out of its way to say which creator-facing rules a compactor
inherits and which it does not — §6.3 does this for `flags` ("A compactor,
though its output is a new file, carries the input's unknown ignore-lane bits
into its output trailer rather than writing flags = 0"), and §20.5 does it for
`file_id`, `generation` and `version_minor` — which makes the silence on the
commit protocol read as deliberate rather than as an unstated inheritance.
Under B the compactor owes no barrier, and its pre-trailer pad is bounded by
nothing at all, since §6.2 bounds that gap "only through step 5 of the commit
protocol … a longer gap is conforming, and no conforming **commit** produces
one" — and under B compaction is not a commit.

**Which I picked and why.** Reading A. `[R-WRT-01]`'s "every writer
requirement for the bytes it produces" is the closest thing to a general
clause, and a compactor that omits the first barrier can produce an output
whose trailer is durable while its payloads are not — a silently wrong file
that would then be swapped in over a good input. I emitted both barriers and a
41-byte-equivalent minimal pad.

**What an implementer does wrong without it.** Two things. (i) Durability: a
compactor built on Reading B may write the whole output with a single fsync at
the end, or none, and on a crash-and-swap produce a file whose trailer commits
payload bytes that never landed. Nothing in §20.5 warns against it, and §9.2's
note about weak barriers is attached to the commit protocol the compactor was
never told it follows. (ii) Bytes: under Reading B the pre-trailer pad in a
compacted output has no upper bound at all, so two conforming compactors given
byte-identical input may emit outputs of different lengths differing in nothing
but pad, and there is no rule to appeal to. That is the one row of my
divergence catalogue (§6, row 18) that I could classify as neither legitimate
nor forbidden. Appendix G item 3 closes it for profile adopters — "§6.2's
64-byte trailer alignment, the pre-trailer pad included" — but Appendix G is
non-normative and adds no requirement to any actor.

**Byte-level?** No. Under both readings every resulting file is conforming and
every conforming reader accepts it identically: §6.2 states outright that a
longer pre-trailer gap "is conforming", and §2.3 lists it among the writer
obligations whose violation "this specification expressly declares not to be a
file-conformance violation". So the set of conforming files is unchanged and no
reader's accept/reject verdict moves. What changes is whether a given
*compactor* is a conforming writer, which §2.3 has already classified as
conduct rather than bytes. I grade it honestly rather than reaching: the cost
to an implementer is a durability decision made without guidance and an
unconstrained field in the output, not a fork in the emittable set.

**Suggested repair (not my call):** one clause in §20.5 saying either that a
compactor follows `[R-LIF-02]`'s creation path for its output, or that it does
not and what it owes instead — the same sentence §6.3 already writes for
`flags`.

---

## 13. What I could not break

For the record, because an acceptance round needs the negative result stated as
plainly as the positive one:

- §18.2's compressed-document passage is coherent read as a whole. The
  carry-over list is complete against `[R-COD-06]`, the two exceptions are each
  replaced, the analogy to the tile rule survives being read word for word, and
  a writer has a determinate path for a document of any size up to the
  guarantee.
- §21.8's "121 conditions over 277 instances" is exactly right under §21.1's
  own counting rules.
- §21.9's quantifiers are consistent with the rules they cite: the tile row
  ranges over addressed tiles exactly as `[R-COD-07]`'s cap does; the other two
  per-instance rows range over stored bytes; the first five over declarations.
  I found no quantity of the trailer, the record header, the layer-record
  payload, the index entry or the user-metadata record that is governed by
  nothing.
- §21.7's account of what no check detects is correct on every case I
  constructed against it, including the channel-reorder-with-equal-fills case
  its "witnessed only where…" clause has to cover.
- §21.5's preamble routes encoding 0, the reserved range, the experimental
  range, and the two capability declines to four different places, and each
  destination agrees.
- Every stated constant, offset, and worked example recomputes.

---

## 14. Disclosure

I read exactly one file from the repository: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in four `Read` calls covering lines 1–4,426. I ran `grep` against that same
file three times (for `[R-LIF-02]` citations, for analogy connectives, and to
extract §21's Instances cells). I created and ran four Python scripts of my own
in my scratch directory (`crc.py`, `build.py`, `gen2.py`, `count.py`,
`consts.py`) and wrote two binary artifacts (`gen1.tarn`, `gen2.tarn`) there.
The `count.py` script reads `spec/tarn.md` — the permitted file — and nothing
else. I did not read `docs/`, `conformance/`, `spec/registry.json`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, or any git history, and I ran no
web search or fetch. I did not read or list the round-23 output directory.

Context I did not ask for **did** appear before I began: the runtime placed a
project instruction file (`CLAUDE.md`, which forwards to `AGENTS.md`) and an
index of the maintainer's memory files in my context, the latter listing titles
of notes about this project's working cadence, its register, and prior workflow
failures. I did not open any of those files and I have not used their contents;
I am naming their appearance rather than repeating them, as the brief requires.
No conclusion in this transcript derives from them.
