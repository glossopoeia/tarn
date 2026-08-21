# Round 18 — Writer/updater implementation walk

**Disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in four passes covering all 4,339 lines. I opened no other file — no `docs/`,
no ADRs, no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no `spec/registry.json`,
no git history, no web. I did not list the output directory.

I ran local computation that reads no project file: a Python CRC-32C
implementation (written from §4.5's stated parameters), a file **builder**
(`build.py`), an **appender** (`append.py`), and an independent **reader/
verifier** (`read.py`) which I used to check the builder's output against
§19.1–§19.4 and §9.7. Scratch files live in the session scratchpad
(`demo.tarn`, `demo2.tarn`, `crc.py`, `build.py`, `append.py`, `read.py`) and
were created by me.

---

## 0. Calibrating the tools before trusting them

Before building anything I checked my CRC against every constant the document
publishes, because every later byte depends on it.

- §4.5's check vector: `CRC-32C("123456789")` → `0xE3069283` ✓; CRC of zero
  bytes → `0x00000000` ✓.
- §7.4's worked layer-record example: the 80-byte array of four sentinel
  entries → `0x80A34955` ✓, and the CRC of that 4-byte array →
  `0xC4EE982E` ✓.
- §15.4's sparse constant: CRC over 2¹⁶ sentinel entries → `0xEECB3BB2` ✓.

All four reproduce. This is worth saying because it means the polynomial
statement in §4.5 (Castagnoli `0x1EDC6F41`, reflected in/out, init/final XOR
`0xFFFFFFFF`, stored little-endian) is unambiguous enough that a
from-scratch implementation lands on the published constants first try. That
is not true of every CRC specification I have implemented.

---

## 1. Creation: a file built byte by byte

I did not want a toy. The file exercises: two layers, both layouts, a packed
boolean plane, sentinels, edge padding, a multi-channel interleaved sample
stride, and a file-scope user-metadata extent.

### 1.1 What I chose, and who chose it

| Decision | Value | Fixed by the document, or by me? |
|---|---|---|
| front block | `89 54 41 52 4E 0D 0A 1A` + 8 zero | **document** (§6.1) |
| first structure offset | 16 | **me.** §16 `[R-SLB-05]` makes placement free; the floors are `[R-CNT-13]`/§15.3's `offset ≥ 16`. Appendix G item 3 pins 16 for the profile. |
| layer A name / geometry | `img`, rank 2, dims `y`(E=5,T=4), `x`(E=5,T=4) | me (input) |
| A layout / channels | interleaved; `r` uint8 fill `00`, `v` uint16 fill `AB CD` | me (input) |
| A codec / filter | 1 / 1 | me; `[R-COD-03]`, `[R-COD-09]` bound the value set |
| layer B | `mask`, planar, same geometry, one bool channel `m`, fill `00` | me (input) |
| record order in directory | img, mask, user-metadata | **me.** `[R-CNT-14]`: "Record semantics MUST NOT depend on record order". |
| layer-record flags | `0x0003` (MU=1, PE=1) | **document** (§7.3 table + `[R-CNT-22]`) |
| user-metadata flags | `0x0002` (MU=0, PE=1) | **document** (§7.3) |
| metadata encoding | 1 (none) | me (`[R-MTA-03]` value set) |
| `version_minor` | 0 | **document-advised** (`[R-CNT-26]`, SHOULD) |
| `flags` | 0 | **document** (`[R-CNT-08]`: a creator "MUST write flags = 0") |
| `file_id` | `0x0123456789ABCDEF` | **me**; §9.3 SHOULDs a CSPRNG draw |
| pad content | zero | **document-advised** (`[R-CNT-03]`, SHOULD) |
| pre-trailer pad length | 62 bytes | **document** (`[R-LIF-02]` step 5, to the next 64-byte boundary) |

Everything else fell out of arithmetic.

### 1.2 Grid and serialization arithmetic

Both layers: Gᵢ = ⌈5/4⌉ = 2 for each axis (§11.2's stated form, deliberately
not `(E+T−1)/T`), so N = 4 and P = ∏Tᵢ = 16.

- `img` is interleaved → addressed-tile count = N = 4. Q = ΣBᵢ = 1 + 2 = 3,
  F_r = 0, F_v = 1. Decoded size = P·Q = 48. In-tile ordinal
  u = u₀·T₁ + u₁ = 4u₀ + u₁ (`[R-GEO-06]`, ∏_{j>0} Tⱼ = 4, ∏_{j>1} = 1).
  Value k of the sequence is channel (k mod C) at ordinal k div C
  (`[R-SER-01]`), and offset of value k is (k div C)·Q + F_{k mod C}
  (`[R-SER-02]`) — so channel c at ordinal u sits at u·3 + Fᶜ.
- `mask` is planar with C = 1 → addressed-tile count = C·N = 4, disk ordinal
  = c·N + s = s. Bool channel → §14.3's packed plane, decoded size
  ⌈16/8⌉ = 2 bytes, value k at bit k mod 8 of byte k div 8, LSB-first.

Stored tiles: `img` stores disk ordinals 0 and 3; `mask` stores ordinal 0.
The rest are sentinels (`FF ×16 00 ×4`, §15.2).

Tile 3 of `img` is tile coordinates (1,1), covering y ∈ [4,8), x ∈ [4,8).
Only (4,4) is inside the extents; the other 15 positions are **padding
positions** (§11.3). `[R-SER-05]` fixes their content to fill, per channel.
Verified in the dump below: bytes `2C 14 04` is the real sample
(r = 44, v = 0x0414 = 1044), followed by fifteen copies of `00 CD AB`.

`mask` tile 0 covers y,x ∈ [0,4) — all real, P = 16, so 16 mod 8 = 0 and there
are **no pad bits**. Bits set where (y+x) is even → `A5 A5`, which is what the
dump shows at offset 0x00C4.

### 1.3 The layout

```
[0,16)      front signature block
[16,64)     img tile 0        48 bytes  (codec 1 ⇒ length = decoded size, [R-COD-04])
[64,112)    img tile 3        48 bytes
[112,196)   img index region  84 = 4·20 + ⌈4/2¹⁶⌉·4     ([R-CNT-17])
[196,198)   mask tile 0        2 bytes  (⌈16/8⌉)
[198,282)   mask index region 84 bytes
[282,307)   user-metadata extent 25 = 21-byte JSON + 4-byte terminal CRC
[307,578)   directory         271 = (24+100) + (24+94) + (24+1) + 4
[578,640)   pre-trailer pad   62 bytes — slack
[640,704)   trailer
F = 704, F mod 64 = 0 ✓;  dir_offset + dir_length = 578 ≤ F − 64 = 640 ✓
```

The `img` layer record's inline payload came out at exactly 100 bytes:
name 4 + nine scalars 34 + two dimension entries 36 + two channel entries
(6 + 7) + trailing fixed fields 13. `mask`: 5 + 34 + 36 + 6 + 13 = 94. Both
parse with no residue, so both sub-record sequences are empty — the §7.4
example's arithmetic generalizes cleanly.

I then wrote an independent reader (`read.py`) implementing §19.1's four open
steps, §19.3's layer validation, §19.4's index chain and tile reads, and
§9.7's coverage walk. It accepts the file, decodes both layers, and reports:

```
claimants [(0,16),(16,64),(64,112),(112,196),(196,198),(198,282),
           (282,307),(307,578),(640,704)]
covered 642   F 704   SLACK 62
```

Slack = 62 = exactly the pre-trailer pad. That is the whole of a creation
commit's slack when no alignment is declared.

### 1.4 Places the creation path made me stop and re-read

**(a) "Pad to the next 64-byte boundary" when you are already on one.**
`[R-LIF-02]` step 5 says "append the pad to the next 64-byte boundary". If a
directory happens to end at offset 640, is the pad 0 or 64 bytes? This is a
genuine fork — and §6.2 closes it in the same breath: "a writer that ends its
directory on a 64-byte boundary leaves none". Good. I flag it here only
because it is the shape of thing that usually *isn't* closed.

**(b) Is the directory required to be the last structure?** Yes, twice over:
`[R-LIF-02]` orders step 3 after step 2, and `[R-CNT-05]` says "Writers MUST
place the directory so that no structure lies between its end and the
trailer." I could not have inferred the second from the first (step ordering
is temporal, not spatial), so the explicit rule earns its place.

**(c) Is the tile-index region its own coverage class?** §5.1's prose lists
"stored-tile payloads, tile-index regions, record extents" as if the first
two were separate, but §5.2's normative list has only "a stored-tile extent, a
record extent…, the directory, or the trailer", and §9.7 resolves it: "A layer
record's extent slot addresses that layer's tile-index region (§7.4), so the
region enters the walk once, as that record's extent, and is not a second
claimant beside it." My coverage walk counts it once. No divergence, but the
§5.1 phrasing costs a cross-reference.

**(d) `crc_of_crc_array` when there is one segment.** §15.4 says the segment
CRC array is ⌈entry_count/2¹⁶⌉ × 4 bytes and `crc_of_crc_array` covers the
array. With one segment that is a CRC of four bytes — not of the entries.
The §7.4 example confirms it (`0xC4EE982E` over `55 49 A3 80`). Easy to get
wrong, correctly pinned.

---

## 2. The append procedure

### 2.1 Adding a layer to an existing file

I appended a third layer `zed` (rank 1, dim `t` E=3 T=2 → G = 2, N = 2,
interleaved, one int32 channel `q`, fill 0). Tile 1 covers t ∈ [2,4), with
t = 2 real and t = 3 a padding position → fill-encoded.

Walking `[R-WRT-04]`'s six steps against the real file:

1. **Establish F.** Validate the trailer in the final 64 bytes of the
   *physical* file (`[R-LIF-04]`). Physical length 704 = committed_file_length ✓.
2. **Open.** §19.1's four steps. Note what this does *not* do: it does not
   touch a single extent. `[R-RDR-01]`: "It consumes the trailer and directory
   only — no extent slot's content, no tile index, no payload."
3. **Validate what the commit touches** (`[R-WRT-03]`): "the trailer and the
   full directory always — re-emission (§20.4) relies on every directory
   byte". Because I am adding a layer and modifying none, §19.3's layer
   validation is owed for *no* existing layer, and the §19.4 index chain for
   *no* segment. This is a real and useful economy: adding a layer to a file
   with 65,536 layers costs one directory read and no index I/O at all.
4. **Write payloads and indexes**, beginning at exactly F = 704:
   `zed` tile 0 [704,712), tile 1 [712,720), `zed` index region [720,764)
   (2·20 + 4 = 44). `img` and `mask` keep their extent slots pointing where
   they always pointed — `[R-WRT-05]`, and §20.3's step 4 is explicit that
   "relocating a live index region is compaction's operation (§20.5,
   `[R-WRT-07]`), not an appender's."
5. **Re-emit the directory** per §20.4: the three existing records
   byte-identically, plus `zed`'s. New directory [764,1137), 373 bytes.
6. **Commit:** barrier; pad [1137,1152); trailer [1152,1216) with
   generation 2, the same `file_id`, ignore-lane bits copied forward
   (`[R-CNT-08]`), `version_minor` = max(floor 0, prior 0) = 0
   (`[R-CNT-26]`); barrier.

F′ = 1216, a multiple of 64 ✓. My reader accepts the result and reports:

```
covered 804   F 1216   SLACK 412
```

412 = 271 (superseded directory) + 62 (superseded pad) + 64 (superseded
trailer) + 15 (new pad). Every byte accounted for.

**The commit point** is step 6's barrier. Before it the file is torn to every
reader (§2.4 below). §9.2's ordering is the whole design: the barrier of step
4 orders payloads-and-directory ahead of the trailer, so the trailer never
commits a directory that is not durable. §20.2 is explicit that a creator owes
"both barriers, not one" — and this is worth restating because a naive
implementation writes one fsync at the end and is silently wrong under power
loss (though, per §9.2's note, degraded only from "torn commits are invisible"
to "torn commits are detected").

### 2.2 Superseding a tile, and the index-cost cliff

Superseding one stored tile of `img` re-emits `img`'s whole 84-byte index
region at a new placement (`[R-WRT-04]` step 4), which changes the segment
CRC, which changes `crc_of_crc_array`, which changes the layer record, which
changes the directory. The old index region and the old payload become slack.
§20.3's note quantifies the general case (≈20 MB of index for a one-sample
edit on a 10⁶-tile layer). I confirm the mechanism: because the region is
addressed by a single extent slot, a single changed entry costs its whole
length.

### 2.3 Extent growth, and ordinal renumbering

I worked the case where growth renumbers. `img` grows E_x from 5 to 9 with
T_x = 4 → G_x goes 2 → 3, N goes 4 → 6. Old ordinals s = t_y·G_x + t_x under
G_x = 2 map (0,0)→0, (0,1)→1, (1,0)→2, (1,1)→3; under G_x = 3 they become
0, 1, 3, 4. So old entries 2 and 3 must be **moved** to positions 3 and 4, and
new positions 2 and 5 emitted per §15. §20.3 step 4 says exactly this — "every
other entry byte-identical at its disk-ordinal position (a geometry change
renumbers ordinals wherever `[R-GEO-06]` moves them)". Growth along the *first*
dimension does not renumber; only a change to a non-leading Gᵢ does. The
document does not say that out loud but it falls out of `[R-GEO-06]`'s formula
and I did not have to guess.

Crucially, growing E_x turns padding positions of stored tile (1,1) into real
positions. §20.3 step 4 licenses this directly — "an extent MAY **grow**,
since a position that becomes real held that channel's fill and fill is a
legal sample value" — and the invariant holds in my bytes: those positions
already contain `00 CD AB`, so after the growth they read as fill, which is
what an unwritten position should read as. Decoded size is unchanged (P and Q
are functions of T and the channel types, not of E), so `[R-COD-04]`'s
codec-1 equality still holds. This is the single most delicate rule in §20
and it is correct.

### 2.4 A file whose records I do not all understand

Here is the full flag walk for my updater. §7.2 defines bit 0 = MUST_UNDERSTAND,
bit 1 = PRESERVE_ON_EDIT, bits 2–15 reserved. §20.4's preamble tells me where
the *authoritative* flags come from, which is not always the stored bits:

- **type §7.3 registers** (0x0001 layer, 0x0002 user metadata): the registry's
  fixed flags govern (`[R-CNT-22]`), the stored bits do not. Both are PE = 1,
  so neither can ever be dropped.
- **type I implement that this text does not register**: "the definition it
  implements the type from supplies the flags, and the stored bits never do".
- **type I do not implement**: stored flags are authoritative, and
  MU = 1 / PE = 0 reads as PE = 1 (`[R-CNT-12]`).

| Stored flags | Top-level record | Layer sub-record |
|---|---|---|
| **MU=1, PE=1** (unimplemented type) | Reject the file. `[R-CNT-15]` makes an unimplemented top-level MU = 1 record reject-file, and §20.4 says "At file scope no commit is available at all". Compaction likewise barred (`[R-WRT-06]`). **No commit of any kind is available.** | Retain byte-identical; **that layer** may not be modified, other layers stay editable (`[R-CNT-18]`, §20.4). I may still add a new layer, edit a different layer, or edit top-level records. Compaction is nonetheless barred outright by `[R-WRT-06]`'s final sentence ("any record whose type it does not implement with MU = 1"). |
| **MU=1, PE=0** | Same as above — `[R-CNT-12]`: "a reader or updater encountering it MUST treat the record as PE = 1". The file is nonconforming (verifier-detected, F25/L46) but my behavior is unchanged. | Same, via L46. |
| **MU=0, PE=1** | Retain byte-identical, extent content unmodified. I may relocate the extent and re-point the slot **only under §20.5** (`[R-WRT-08]`) — i.e. never as an appender. I must not re-encode it. | Same; re-pointing the slot rewrites the *layer record's* inline payload, which only a compactor is licensed to do here. |
| **MU=0, PE=0** | Retain byte-identical, **or** drop it — but "An appender MUST NOT drop it except in a commit that *independently* changes the scope the record attaches to": for a top-level record, the file's layer set, any layer record's content, or another non-layer top-level record. A compactor MAY drop it whenever it rewrites the file. Dropping SHOULD be reported. | Same, with the trigger set being "that layer's record, the entry set of its index, or which of its tiles are stored". |
| **reserved bits 2–15 set** | Ignore them (`[R-CNT-12]`: "readers MUST ignore them"); re-emit the record byte-identically, which carries the nonconforming bits forward. Detection is a verifier's (F26/L47). | Same. |

I checked the circularity in the MU=0/PE=0 row and it is closed: "Dropping the
record, or dropping another record in the same commit, is not itself such a
change, so a commit whose only effect would be the drop MUST retain it."

I also checked that my three concrete commits classify correctly:

- Adding layer `zed` changes the file's layer set → a top-level MU=0/PE=0
  record could be dropped in that commit.
- Superseding an `img` tile re-places `img`'s index region, moving its extent
  slot, and so modifies `img`'s record → licenses dropping a top-level
  MU=0/PE=0 record, or such a sub-record **of `img`** but not of `mask`.
  §20.4 spells this out.
- A checkpoint commit (§5.1: "a commit that touches no layer re-emits the
  directory, the pad and the trailer alone") licenses no drop at all.

**An index entry I do not understand.** §20.3 step 2 is unusually direct:
"a malformed index entry an appender meets while re-emitting a region is
carried forward byte-identically at its disk-ordinal position under step 4,
not repaired to a sentinel." I nearly got this wrong: my instinct was that
re-emitting a region at a new placement is *authoring* those bytes and
therefore subject to `[R-CNF-05]`. §20.3 rejects that instinct explicitly —
"Reproducing a structure's bytes unchanged is not authoring them" — and
extends it to entries as well as records. Without that sentence I would have
had to guess, and I would have guessed wrong.

Note the asymmetry it creates, which is stated and deliberate: an **appender**
carries a structurally-malformed index entry forward, while a **compactor**
meeting the same entry MUST refuse (§20.5: "regenerating the region cannot
proceed without meeting it… `[R-WRT-06]` then obliges refusal").

### 2.5 Two updater traps the document actually closes

**Slab re-establishment.** Suppose a layer declares S = 8, A_slab = 4096, and
run 0's stored tiles 0…7 are packed contiguously. I want to store ordinal 3,
currently a sentinel. `[R-SLB-03]` requires the run's stored tiles to be
"contiguous and packed in ordinal order" — so tile 3 must sit *between*
tiles 2 and 4, which `[R-LIF-01]` forbids (those are committed bytes). The
document's answer is `[R-SLB-04]`: "MUST either re-establish the invariants
for every such run — or clear the declaration in the new generation". So I
either append fresh copies of the whole run packed in order (stranding the
originals as slack) or clear S and A_slab. §20.3 step 4 restates it. This is
an expensive but fully determined answer, and it is the kind of thing a
specification usually leaves to be discovered in production.

**Alignment on retained tiles.** §20.3 step 4: "an aligned layer's stored
tiles — **every one the new state keeps, not only those this commit adds** —
satisfy its invariant or the declaration is cleared". That closes the obvious
mistake of adding an A declaration to a layer whose existing tiles are not
A-aligned.

---

## 3. Slack, by shape of commit

| Shape | Which bytes become slack | Who counts them | Permitted content |
|---|---|---|---|
| **Creation** | the pre-trailer pad, plus any alignment/slab gaps | a verifier (`[R-CNT-21]`, §9.7); no reader obligation | unconstrained; writers SHOULD zero (`[R-CNT-03]`) |
| **Append** | the superseded directory, its pad and its trailer; every re-emitted index region's prior copy; every superseded stored-tile extent; every superseded record extent; the new pad. Measured on my file: 271 + 62 + 64 + 15 = 412. | verifier | unconstrained |
| **In-place update** | *does not exist.* `[R-LIF-01]`: bytes in [0,F) "are immutable: a writer MUST NOT modify them, and every conforming mutation of a file is either a commit (§9.2) or a whole-file rewrite under a new file_id". The only bytes any writer overwrites are beyond F. | — | — |
| **Rewrite** (new file_id, not compaction) | the new file's own gaps and pad; the *input* file is untouched and persists entire | verifier, on the new file | unconstrained |
| **Compaction** | only the output's alignment gaps and pre-trailer pad — "slack is never carried" (§20.5). My demo2 (F = 1216, slack 412) compacts to F = 832 with slack 28 (the pad alone). | verifier | unconstrained |
| **Abandoned partial write** | **nothing becomes slack.** The residue lies beyond F, so it is outside the live state's range altogether; §9.5's note says "What the residue violates is `[R-LIF-04]`'s writer obligation to truncate or overwrite". The byte sequence is **not a conforming file** until truncated or overwritten (F17, and F8 once the tail is not a trailer). | nobody — a verifier rejects at the trailer gate before any live state exists (§5.2: "there is no F and no live state to walk, so the total is not owed at all") | — |

Two further points I had to work out rather than read:

- A **partial** slack total is not merely "incomplete" — `[R-CNT-21]` makes it
  "an upper bound on the file's true slack, never an under-count", and
  requires the verifier to name what stopped the walk. My reader reports a
  full total because its walk completes.
- Slack from an **abandoned write** *can* re-enter a later committed state.
  See finding **writer-01**.

---

## 4. Torn-write recovery: four crash points

All against the append of §2.1 (commit 2 on the 704-byte file, ending at
F′ = 1216).

**Crash A — mid-payload (physical length 708).**
*Next reader:* fetches [644,708); the 8 bytes at 644 are trailer bytes [4,8)
of trail₁, not the magic → F8, reject-file. `[R-LIF-05]` forbids scanning
backward, so the reader cannot tell torn from corrupt and is not asked to.
*Next updater:* `[R-LIF-04]` — validation fails, "the writer MUST NOT append".
Recovery is §9.6, a deliberate separate operation.
*Conforming?* **No.** The 708-byte sequence fails `[R-CNT-06]`.

**Crash B — after step 4's barrier, before the trailer (length 1137).**
Reader: same verdict. Recovery: probe backward at 64-aligned offsets from
o = 1072 down; magic matches at 640, the trailer CRC verifies, and
committed_file_length = 704 = 640 + 64 ✓. Truncate to 704 → generation 1
restored exactly, because commit 2 modified no committed byte. This is the
whole return on append-only, and §9.2's figure states it plainly: "The window
is not one in which the old state is *readable* — it is one in which the old
state is *recoverable*."

**Crash C — partial trailer (length 1184, or 1216 with a torn trailer).**
At 1184, [1120,1184) is not a trailer → torn. At 1216 with a half-written
trailer, the magic may match at 1152 but the CRC fails → not a candidate;
the probe continues and lands on 640.

**Crash D — the pad written, the trailer durable, the pad's bytes lost.**
This one is interesting: the pad is slack, and slack content is unconstrained
(`[R-CNT-21]`). So a commit whose trailer is durable but whose pad holds stale
bytes yields a **fully conforming file**. The design tolerates a class of
partial write for free.

**Crash E — a crash during `[R-LIF-04]`'s option-2 overwrite.** The appender
was overwriting residue in [F, P) when it died. Physical length is still P
(residue length), the tail is not a trailer, and recovery lands on F. Safe,
but see writer-01 for what happens when this *succeeds*.

One thing I checked and could not decide cheaply, and then decided:
`[R-LIF-06]`'s "whole-file re-verification" — is that §8's checksum chain, or
full verifier certification (§9.7, which decodes every stored tile)? The two
give different truncation points for a candidate that passes the chain but
carries, say, a T4 padding violation or an F27 unsorted metadata document.
I settled on the chain: the citation is "(§8)", the stated purpose is
defeating trailer mimics (which the chain defeats), and `[R-LIF-06]`'s
criterion is "was not a commit state" — a nonconforming file can perfectly
well have been committed. I did not report this; the citation does the work.

---

## 5. Byte-divergence catalogue

Given identical input arrays and identical stated options (tiling, layout,
codec choice, fill choice, metadata content), here is every way I found for
two conforming writers to emit different bytes, and what Appendix G does
about each.

| # | Degree of freedom | Governing rule | Appendix G |
|---|---|---|---|
| 1 | Placement and relative order of every structure | `[R-SLB-05]`, `[R-LIF-02]` step 2 | **closed** — item 3's total emission order |
| 2 | Extent of alignment/slab gaps | `[R-SLB-05]` | **closed** — item 3 ("each later structure begins where the previous one ended, save where alignment forces a gap") |
| 3 | Content of gaps and the pad | `[R-CNT-03]` (SHOULD) | **closed** — item 3 takes the SHOULD as a requirement |
| 4 | Record order in the directory | `[R-CNT-14]` | **closed** — item 3's type/name/lexicographic key |
| 5 | Sub-record order inside a layer record | `[R-CNT-14]` | **closed** — item 3 |
| 6 | `file_id` | §9.3 (SHOULD random) | **closed for creators** — item 2's derived hash; **left open for compactors**, explicitly (`[R-WRT-06]`'s fresh draw) |
| 7 | `version_minor` | `[R-CNT-26]` (SHOULD) | **closed for creators**; **mis-closed for compactors** — finding writer-02 |
| 8 | trailer `flags` | `[R-CNT-08]` (creator MUST = 0; updater MUST copy ignore-lane bits) | item 8 says `flags = 0` without the compactor carve-out — finding writer-02 |
| 9 | Encoder output for codecs 2–4, including DEFLATE's unused final-byte bits (§17.2's note) and zstd's optional `Frame_Content_Size` | `[R-CNF-05]` | **closed** — item 1 pins implementation, version and settings, and concedes cross-implementation identity is unattainable |
| 10 | Filter value (1 vs 2) | `[R-COD-09]` leaves the choice | **closed** — item 5 |
| 11 | Whether alignment/slab are declared, and at what values | §16 | **closed** — item 5 |
| 12 | Sentinel vs. stored for an all-fill tile | nothing requires either | **closed** — item 6 |
| 13 | Recorded fill when the caller chooses none | `[R-TYP-10]` (SHOULD zero) | **closed** — item 7, and item 7 notes it compounds with item 6 |
| 14 | NFC vs. NFD in names | `[R-ENC-14]` (SHOULD) | **closed** — item 10 |
| 15 | JSON serialization of metadata (whitespace, number formatting, escapes) | `[R-MTA-05]` fixes only member order | **closed** — item 9 pins the JSON writer |
| 16 | Metadata storage encoding (1 vs 2), and the zstd producer if 2 | `[R-MTA-03]` | **closed** — item 9 |
| 17 | Number of commits used to reach the same content | §9 constrains none | **closed** — item 4 |
| 18 | Pre-trailer pad *length* — §2.3 names "§6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad" as a writer obligation whose violation is **not** a file-conformance violation, so a longer pad yields a conforming file from a misbehaving writer | `[R-CNT-05]`, §2.3 | **closed** — item 3 folds the pad into alignment-forced gaps |
| 19 | Residue from an abandoned write surviving into a later live state as slack | `[R-LIF-04]` vs. `[R-CNT-21]`/`[R-SLB-05]` | **closed** — item 3 requires every gap byte zero; but the normative text does not close it — finding **writer-01** |
| 20 | Placement/order of the structures a **commit** appends | not stated | **not closed.** Item 3 is anchored at offset 16 and enumerates "its stored tiles", which for an append is the wrong set; item 4 restricts the profile to one generation while asserting "the appended bytes are" reproducible — finding writer-02's second half |

I could classify every divergence I found as legitimate (both files conforming)
rather than forbidden. Items 19 and 20 are the two where the reproducible-writer
material's claim outruns what the normative text or the item itself supports.

**Claims in Appendix G I tried to falsify and could not:**

- Item 3's tie-breaking claim — "Two records this key does not separate are
  byte-identical in type, flags, lengths, payload and extent content;
  emitting them in either order yields the same file." I checked this. Two
  key-equal records differ only in `extent_offset`; the order itself assigns
  those offsets; so record A at position 1 and record B at position 1 emit
  identical header bytes, and their extents hold identical content at
  identical lengths. Both the directory and the extent region come out
  byte-identical. **True.**
- Item 2's derivation is well-founded: the hash input is [0, F−64) followed
  by the trailer's first 60 bytes with `file_id` zeroed, and every one of
  those bytes — including F itself, the pad, `dir_offset` and `dir_length` —
  is known before the trailer is written. No circularity. **True.**
- Item 3's `extent_offset`-masking rationale ("a key containing it would
  depend on its own result") is correct.

---

## 6. Findings

### writer-01 — `[R-LIF-04]`'s consequence clause is false under its own second option (§9.4)

`[R-LIF-04]` states:

> Once F is established (directly, or by recovery whose output has been
> re-verified), a writer whose physical file is longer than F MUST either
> truncate to F before step 1 of `[R-LIF-02]`, or overwrite from F and
> truncate the physical file to the new committed_file_length no later than
> step 6 — so that after any commit completes, the physical file length
> equals committed_file_length, and **bytes beyond a committed length never
> survive into any committed state**.

Take the second option. Physical length is 900; F = 704; residue from an
abandoned commit occupies [704,900). The appender begins writing at exactly
F (`[R-LIF-02]` step 1) and places its first structure at [704,750). Placement
is otherwise free — `[R-SLB-05]`: "its stored tiles MAY occupy any
non-overlapping byte positions, in any order" — and an alignment declaration
positively forces gaps. Say the next structure is 4096-aligned. The new
commit ends at F′ = 8192, so no truncation is owed. Bytes [750,900) still hold
the abandoned commit's data, they lie inside [0,F′), no claimant reaches them,
and they are therefore **slack in the new live committed state** — bytes
beyond a committed length that survived into a committed state.

The two readings are:

- **(a)** "overwrite from F" means overwrite *all* of [F, old physical length).
  Then a writer that leaves residue showing through a gap violates a MUST.
- **(b)** "overwrite from F" means begin writing at F — which is step 1's
  requirement anyway — and unclaimed residue simply becomes slack.

I picked **(b)**, because (a) would make the *content* of certain slack bytes
a conformance obligation, which `[R-CNT-21]` forbids — "Slack has no internal
structure this specification defines, its content is unconstrained, and no
conformance requirement applies to it" — and which §5.2's Rationale says is
not even decidable: "Certifying its content would mean deciding which slack
bytes *this* commit wrote, which is not decidable from the live state — the
only thing a reader ever walks."

Under (b) the trailing clause of `[R-LIF-04]` is simply false: it holds when
the writer truncates first, and when the new commit's structures happen to
cover the residue, and not otherwise. What an implementer does wrong without
this: writes an appender that takes the overwrite option (the fast path — no
truncate syscall, no risk of a truncate racing a reader), and unknowingly
republishes an abandoned commit's bytes inside the live file, which §23.1
then does not describe and no verifier check surfaces. The privacy story in
§23.1 covers "superseded" bytes; these were never committed at all.

**Byte-level: no.** Both readings yield conforming files, because slack
content is unconstrained either way, and §5.2's Rationale concedes the
question is undecidable from the live state. What resolving it changes is a
writer's conduct obligation and §23's disclosure story, not any accept/reject
verdict.

### writer-02 — Appendix G item 8 lacks the compactor carve-out item 2 carries

Appendix G item 8, in full:

> 8. **`version_minor` at the floor** `[R-CNT-26]` states, and `flags` = 0.

The profile explicitly contemplates compactors — item 2 says "This is a
creator's rule: a compactor adopting the profile takes `[R-WRT-06]`'s fresh
draw instead" — and item 4's "One generation" is satisfied by a compacted
file, which carries generation 1 by definition. So a compactor may adopt the
profile, and item 8 then says two things §20 contradicts.

On `version_minor`, `[R-WRT-06]` says:

> The output trailer copies the input's unknown ignore-lane flag bits forward
> (`[R-CNT-08]`) and carries the greater of `[R-CNT-26]`'s floor and the
> input's version_minor — a compactor cannot know which minor version defined
> an ignore-lane bit it does not implement, so it does not lower the floor
> beneath one.

Item 8 says "at the floor `[R-CNT-26]` states"; §20.5 distinguishes that floor
from the value a compactor writes, which is the *greater* of the floor and the
input's minor. Compacting a file whose trailer carries `version_minor = 3`
while the output's features need only 0: a compactor following §20.5 writes 3,
one following item 8 writes 0. Trailer bytes [74,76) differ, and so does the
trailer CRC. Both files are conforming (minors never gate, `[R-CNT-07]`), and
`[R-CNT-26]` is a SHOULD, so both writers are conforming too — which means
the *only* thing in the document that fixes this byte is the profile, and the
profile fixes it to the value §20.5 says a compactor does not write.

On `flags`, §6.3 says the opposite of item 8 in as many words:

> A compactor, though its output is a new file, carries the input's unknown
> ignore-lane bits into its output trailer rather than writing flags = 0
> (§20.5, `[R-WRT-06]`).

Here the normative text does resolve it — `[R-CNT-08]`'s "An updater MUST copy
forward unknown ignore-lane bits of the file it modifies and MUST NOT clear
them" reaches compactors, since §9.1 makes a whole-file rewrite one of the two
"conforming mutation[s] of a file" — and Appendix G's preamble disclaims
adding requirements. But the reader who needs item 8 is precisely the reader
building a reproducible compactor, and item 8 tells that reader to clear the
bits.

The same under-scoping affects item 3, which is anchored at "The first
structure begins at 16" and orders "its stored tiles" per layer — the set an
append does not re-emit. Item 4's aside, "Appending is reproducible only in
the weaker sense that the appended bytes are", is therefore unsupported by
any item: nothing in the profile fixes the placement or order of the
structures a commit appends.

What an implementer does wrong without this: builds a content-addressed
compactor that clears ignore-lane bits (losing a later minor's feature
declaration) and writes a lower `version_minor` than §20.5 prescribes; or
believes appends are covered and finds two profile-conformant appenders
disagreeing.

**Byte-level: no.** Both trailers are conforming files and both writers remain
conforming under either resolution, since `[R-CNT-26]` is SHOULD-level and
`flags = 0` is a conduct obligation §2.3 already declares not to be a
file-conformance violation. Resolving it changes what the non-normative
profile prescribes, not which byte sequences a conforming implementation may
emit.

### writer-03 — one failed extent checksum permanently forecloses compaction (§20.5)

`[R-WRT-09]` fixes the compactor's verification depth:

> it relies structurally on every structure it copies, so it MUST verify each
> link of the chain — the open (§19.1), each retained layer's record (§19.3)
> and full index chain (`[R-IDX-04]`), and each relocated extent's checksum,
> including every stored tile's entry crc — before emitting that structure's
> bytes.

and `[R-WRT-06]` turns any such failure into refusal:

> A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges
> fails, and MUST NOT emit a file carrying a violation it has detected

Chaining these with §20.4 ("both registered types carry PE = 1, so neither can
be dropped") and §20.5's "Where the table does not license a drop the
compactor MUST refuse", the consequence is that **a single bit flip in one
stored tile (T1) or in one user-metadata extent (R2) makes the whole file
permanently uncompactable** — compaction being, per §20.5's own example, "the
only operation that reclaims slack". The reader outcomes are bounded to
reject-tile and ignore-record respectively; §7.1 promises that "Application
metadata never invalidates the structural data it annotates"; and yet the
metadata CRC failure blocks the one operation an operator runs when slack
grows. The escape §20.4 names — "A producer that wants a file without a layer
writes one: a whole-file rewrite under a fresh file_id" — is available but is
expressly *not* compaction, and no rule tells the operator this is where they
have landed.

I state this as decidable-but-expensive rather than as an ambiguity: it takes
four hops (`[R-WRT-09]` → `[R-WRT-06]` → §20.4's table → §7.3's PE fixing) to
reach a conclusion that runs against the intuition §7.1 and §2.4 set up, and
nothing in §20.5, §21.7 or Appendix H says it out loud.

**Byte-level: no.** Both a refusing compactor and (hypothetically) a
tolerant one would leave conforming artifacts; what changes is whether the
tool emits anything at all. No file's accept/reject verdict moves.

### writer-04 — §20.5 conditions index regeneration on the wrong event

§20.5 says:

> except that relocation re-points extent slots, **regenerates each relocated
> tile-index region** (entry offsets new; entry lengths, entry crcs, and
> sentinel entries unchanged; segment CRCs recomputed over the entries as
> re-emitted), and updates the layer-record fields covering a regenerated
> region (crc_of_crc_array).

The condition is that the *region* is relocated. The operative event is that
the region's *entries' targets* moved — as the section's own example says:
"the one kind this operation regenerates rather than copies, since its
entries carry the offsets that moved". Compaction writes a new file and
chooses every offset fresh, so a region can perfectly well land at the offset
it occupied in the input while that layer's stored tiles all move. A
compactor implementing the sentence literally then copies the region verbatim
and emits entries pointing at slack.

Conversely, a region whose entries are all sentinels needs no regeneration
however far it moves — regeneration is a no-op there, since "a sentinel is
re-emitted unchanged" and the segment CRCs recompute to the same values.

The document does decide the outcome: `[R-WRT-07]`'s "The output's reference
arrays MUST equal the live generation's bit for bit" forbids the broken
output, and `[R-CNF-05]` makes the writer nonconforming. So this is an
under-inclusive condition rather than a fork. But the sentence is the one an
implementer follows to build the operation, and it names the wrong trigger.

**Byte-level: no.** `[R-WRT-07]` and `[R-CNF-05]` already forbid the output
the literal reading produces, so no conforming implementation may emit it.

### writer-05 — §23.1's enumeration of what a commit removes omits the extent shrink

§23.1 opens:

> The append-only model (§9.1) means a commit that supersedes data — **the
> only removal of sample data a commit performs**, no commit removing a layer
> at all, and an unknown ancillary record's drop (§20.4) the one other
> removal available to it — removes only that data's *reachability*

§20.3 step 4 describes a second removal, and distinguishes it from
superseding *in the same paragraph*, using both words:

> Where a shrink is permitted the **de-addressed** tiles' extents become slack
> (`[R-CNT-21]`), `[R-CNT-17]` obliges the smaller entry_count and so a
> re-emitted index region, and every surviving stored tile is untouched.
> Discarding data is the caller's operation and this specification does not
> bar it. … Extents this commit **supersedes** become slack (`[R-CNT-21]`)

So an extent shrink removes sample data without superseding it, and §23.1's
"only" is false. The consequence is not cosmetic, because `[R-PRV-01]`'s
prohibition is scoped by that same word:

> Writers and the tools built on them MUST NOT represent a commit that
> supersedes data as erasure of it.

A tool that shrinks an extent and reports "rows 900–1000 deleted" is
representing a removal as erasure, and on the narrow reading of "supersedes"
that §20.3 itself supports, `[R-PRV-01]` does not reach it — even though the
de-addressed tiles' bytes remain in the file exactly as superseded ones do,
readable with a hex editor and recoverable by §9.6's probe. Shrink-as-delete
is also the more natural user-facing operation, so this is the case the rule
most needs to cover.

The narrower point in the same clause: "an unknown ancillary record's drop"
understates §20.4, which lets an updater drop an MU=0/PE=0 record of a type
it *does* implement ("For a type the updater implements that this
specification does not register, the definition it implements the type from
supplies the flags").

I resolved this by reading `[R-PRV-01]` broadly — any commit that makes sample
data unreachable — because that is plainly the section's purpose, and I wrote
my updater to report shrinks and unstores as non-erasure too.

**Byte-level: no.** `[R-PRV-01]` binds how a tool describes an operation; no
byte of any file changes, and no accept/reject verdict moves.

### writer-06 — §20.4's table is attached to one case and extended to all, and its MU=1 row does not survive the extension

§20.4 attaches its table to a single case:

> For a type the updater does not implement, the stored flags are
> authoritative (§7.3, `[R-CNT-15]`; MU = 1 with PE = 0 is read as PE = 1,
> `[R-CNT-12]`), and carry these obligations:

but two other rules extend it to every type. `[R-CNF-06]`:

> MUST honor the preservation obligations of §20.4 — which govern every
> record type, not only those it does not understand.

and §2.4's outcome table: "**preserve-verbatim** | Binds updaters… §20.4's
table states the cases: its MU = 1 and MU = 0 / PE = 1 rows."

Under that extension the MU = 1 row's second sentence — "The updater MUST NOT
modify the scope the record governs." — is selected for **every layer record
in every file**, because §7.3 fixes MU = 1 for type 0x0001 and §20.4's own
preamble says "For a type §7.3 registers, the registry's fixed flags govern
rather than the stored ones (`[R-CNT-22]`)". Read that way, no updater may
ever modify any layer, and the entire append procedure of §20.3 is
unavailable.

The permitted readings are:

- **(a)** Only the rows' *first* sentences ("Retain byte-identical") are the
  "preservation obligations" that generalize; the modification bar is
  particular to a record the updater does not implement.
- **(b)** The whole row generalizes, and layer modification is barred.

I picked **(a)**, on three grounds: §2.4 defines preserve-verbatim narrowly as
"the bytes are carried forward unmodified"; the row's own third sentence
speaks of "an unknown critical record"; and §20.3 is an elaborate, explicit
permission to modify layers, so (b) cannot survive contact with it. What an
implementer does wrong without working that out: builds an updater that
refuses every commit touching a layer, or — more likely — spends the
afternoon I spent deciding that §20.3 governs.

**Byte-level: no.** §20.3's step-by-step permission decides it, so a competent
implementation reading the whole document reaches (a); the two readings do not
survive side by side, and no file's conformance depends on the answer.

---

## 7. What I checked and did not report

- **§21's arithmetic.** I counted the register mechanically: 36 + 49 + 26 + 10
  = 121 rows over 273 instances, which is exactly what §21.8 claims. No drift.
- **Requirement-identifier hygiene.** Every prefix's numbering is dense with no
  gaps except `ENC-100` (§2.2's illustration) and the withdrawn `SER-04`,
  which §14.4 records as retired. No identifier is cited without being
  defined.
- **Lowercase modals.** After last round's finding I grepped for lowercase
  `must`/`shall`/`should`/`may not` outside quoted material: there are none.
  The lowercase permissions that remain ("is free to place structures
  anywhere §5.2 admits", §20.5) are bounded by ALL-CAPS restrictions
  (`[R-CNT-05]`, `[R-SLB-01]`, `[R-SLB-03]`), which is the safe direction of
  the asymmetry.
- **§21.7's "witnessed only where … *and* …"** followed two clauses later by
  "a change that reaches the decoded size instead is witnessed by T3 or T14".
  Read as "only where the affected tiles remain stored", with the following
  clauses enumerating how the witness arises, the passage is coherent — and
  the closing clause ("a commit that supersedes every tile it would have
  damaged leaves the live state clean") confirms that is the intended scope
  of the "only". No register row changes under either reading, and §21.7
  imposes no obligation on any actor, so I did not report it.
- **`[R-LIF-06]`'s "whole-file re-verification"** — see §4 above; the "(§8)"
  citation and the stated anti-mimic purpose settle it.
- **The compactor and `[R-SLB-04]`.** I thought there was a gap — may a
  compactor clear a slab declaration instead of re-establishing it? §20.5
  closes it: the compactor "is free to place structures anywhere §5.2 admits
  and **every declared layout invariant permits** (`[R-SLB-01]`,
  `[R-SLB-03]`)", so it packs the runs and keeps the declaration. Its
  licensed layer-record modifications are enumerated (extent slot,
  `crc_of_crc_array`), and clearing S is not among them.
- **The compactor silently repairing L40/L41/L42 and F33/L18.** A compactor
  that places tiles per the declared invariants produces an output satisfying
  them even from an input that violated them, and copying two overlapping
  extents into disjoint output regions preserves both tiles' decoded content.
  This is not "heuristic repair" under `[R-CNF-04]` (which binds readers and
  concerns inferring values), and §20.5 nowhere forbids it. I concluded it is
  permitted and harmless.
- **Concurrent readers during a commit.** §9.5 promises "any number of
  concurrent readers" but a commit in flight leaves a non-trailer at the
  physical end, so every open fails until step 6. The normative text does not
  actually promise otherwise, and §9.5's note names the mitigation. Not a
  defect.

---

*Editorial substitution by the maintainer, recorded per the repository's
vocabulary gate: one ordinary-English use of a reserved word was replaced with
"prior copy". No claim, number or citation in this transcript is affected.*
