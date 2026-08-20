# Cleanroom round 15 — Writer implementer transcript

**Disclosure.** I read exactly one file: `spec/tarn.md`. I opened no ADR, no
`PLAN.md`, no `AGENTS.md`, no `conformance/`, no `spec/registry.json`, no git
history, no prior round's findings, and no other transcript. I did not list the
output directory. I ran `grep`/`sed` against `spec/tarn.md` only, and Python
scripts I wrote myself in the scratchpad (`crc.py`, `build.py`, `append.py`),
which read no project file. Everything below is derived from the document plus
that arithmetic.

I noticed that the session's environment banner happens to carry a list of
recent commit subjects. I did not run `git log` and I have not used those
subjects as evidence for anything; where one of them touches a section I
verified the section against the document's own text and against arithmetic I
performed myself. Nothing in my findings rests on them.

---

## 0. Method

I built a conforming writer on paper, then actually emitted the bytes it would
emit, then appended to that file twice, then walked crash points and the slack
ledger. Wherever the document failed to tell me what to do I stopped and wrote
it down. Before trusting my own reading of the arithmetic I reproduced every
numeric constant the document states, so that a disagreement later would be
about the text and not about my CRC.

### 0.1 Calibrating my implementation against the document's own numbers

```
CRC32C('123456789')                  = 0xE3069283   spec §4.5: 0xE3069283   OK
CRC32C(b'')                          = 0x00000000   spec §4.5: 0x00000000   OK
CRC32C(4 sentinel entries, 80 bytes) = 0x80A34955   spec §7.4: 0x80A34955   OK
crc_of_crc_array over `55 49 A3 80`  = 0xC4EE982E   spec §7.4: 0xC4EE982E   OK
CRC32C(2^16 sentinel entries)        = 0xEECB3BB2   spec §15.4/App B        OK
Appendix A trailer CRC over [0,60)   = 0xE00938D2   spec App A: 0xE00938D2  OK
```

I also re-derived, by hand, every worked example that bears on byte layout:

* §7.4's layer-record payload: `4 + 34 + 18 + 12 + 13 = 81` bytes, and every
  offset in its hex block lands where the packed field order puts it. The
  "nine scalars from layout through channel count" are
  `1+2+2+2+8+8+8+1+2 = 34`. Confirmed.
* §11.2 / §11.4: `G=(4,8)`, `N=32`, `P=65536`; `(300,700) → s=10`, in-tile
  ordinal `44·256+188 = 11452`; planar channel 2 → disk ordinal `2·32+10=74`.
  Confirmed.
* §14.2: interleaved `(2,3)` with uint8+uint16 → `Q=3`, decoded size 18,
  ordinal 5 at `[15,18)`; planar `b` 12 bytes, ordinal 5 at bytes 10–11;
  float32+bool → `Q=5`, size 30, ordinal 5 at `[25,30)`. Confirmed.
* §14.3: `P=10` alternating from true → `55 01`; with fill true, `55 FD`.
  Confirmed (pad bits are bits 2–7 of byte 1).
* §14.5: extents (5,5) tile (4,4) → edge tile (1,1) has 1 real and 15 padding
  positions, 32 bytes at uint16. Confirmed.
* §15.4: `entry_count = 1,000,000` → 16 segments, region 20,000,064 bytes,
  tile 999,999 at segment-relative byte 339,180, segment 15 at
  `[19,660,800, 20,000,000)`, CRC array at `[20,000,000, 20,000,064)`.
  Confirmed. Planar example: ordinal 74 → region bytes `[1480,1500)`;
  channel 3 → entries 96–127. Confirmed.
* §17.3: shuffle of `1.0, 2.0, 3.0` float32 →
  `00 00 00 00 00 00 80 00 40 3F 40 40`. Confirmed.
* §16.2: `S=8`, `N=32` → runs `[0,8) [8,16) [16,24) [24,32)`; tile rows 1–2 =
  ordinals 8–23 = runs 1 and 2. Confirmed.
* §21.8's instance count. I counted every Instances cell in §21.2–§21.5 under
  §21.1's stated mechanical rule (semicolon-separated; a cell reading `—` is
  one). I get **57 + 115 + 57 + 44 = 273** over 36+49+26+10 = **121**
  conditions, exactly the figures §21.8 states. I also spot-checked the two
  axes §21.1 states rather than leaves to judgement — layout formulas and
  magnitude direction — against T3/T14 (6 each: 3 layouts × 2 directions),
  T21/L44 (3 each: 3 layouts × one direction, "exceeds"/"larger than"),
  T22 (6), L21/L22 (4), L30 (2), and the no-direction rows L37/L38/F14 (1
  each). They are consistent. This is the cleanest part of the document I
  touched.

Nothing in the document's stated numbers is wrong. Everything below is about
prose.

---

## 1. Creation byte layout

### 1.1 What I chose to build, and why

A file with two layers that between them exercise both layouts, both bool
representations, edge padding in both, a sparse tile, a declared per-tile
alignment, and a file-scope user-metadata record.

* **`mask`** — planar, rank 1, dimension `x` with `E=10`, `T=8`. One bool
  channel `b`, fill `0x00`. `G = ⌈10/8⌉ = 2`, `N = 2`, `P = 8`, `C = 1`.
  Addressed-tile count is `C·N = 2` (`[R-GEO-03]`). Packed bool plane
  (§14.3): decoded size `⌈8/8⌉ = 1` byte. Tile 1 covers x=8..15, so x=10..15
  (in-tile ordinals 2..7) are padding positions and `[R-SER-05]` fixes their
  bits to the channel's fill bit, 0. `P mod 8 = 0`, so there are **no pad
  bits** — a good case, because §14.3's Note says exactly that a plane can
  have many padding positions and no pad bits, and this is one.
  Codec 1, filter 1, `A = 0`, `S = 0`.
* **`temp`** — interleaved, rank 2, `y(E=5,T=4)`, `x(E=5,T=4)`. `G=(2,2)`,
  `N=4`, `P=16`. Channels `t` float32 (fill `00 00 00 00`) and `m` bool
  (fill `01`). `Q = 4+1 = 5`, decoded size `16·5 = 80`. Tiles 0, 1, 3 stored;
  ordinal 2 (tile coords (1,0)) is the sentinel. `A = 512` declared, `S = 0`.
* One top-level user-metadata record, encoding 1, document
  `{"tarn.title":"demo"}` (21 bytes) + terminal CRC-32C = 25-byte extent.

Padding content: at every padding position of a `temp` edge tile I encoded the
channels' fill in declared order — `00 00 00 00 01` — which is `[R-SER-05]`
read literally ("the recorded fill bytes for a numeric channel, the recorded
fill byte for an interleaved bool channel"). Tile 1 has 12 padding positions,
tile 3 has 15.

### 1.2 Emission order — what the document fixed and what it left to me

`[R-LIF-02]` step 2 is explicit: payloads and index regions "in any order
satisfying §5.2's coverage classes". §20.2 adds "every declared layout
invariant (`[R-SLB-01]`, `[R-SLB-03]`) — placement is otherwise free
(`[R-SLB-05]`)". So order and placement were *mine*, and the document says so.
To make the walk checkable I adopted Appendix G item 3's total order:
layers in ascending layer-name byte order (`mask` < `temp`, `6D` < `74`), each
layer's stored tiles in disk-ordinal order, then its index region, then record
extents, then the directory.

Decisions I had to make, with the document's answer:

| Decision | Fixed by | My choice |
|---|---|---|
| First structure offset | `dir_offset ≥ 16`, front block is [0,16) | 16 |
| Does `A` bind the index region? | `[R-SLB-01]`: "every **stored tile's** offset" — a region is not a stored tile | no |
| Sentinel entry bytes | `[R-IDX-02]`: `FF ×16 00 ×4` | as stated |
| Index region shape | `[R-IDX-01]`: entries then CRC array, "no padding anywhere inside the region" | as stated |
| `extent_length` of the index | `[R-CNT-17]`: `n·20 + ⌈n/2¹⁶⌉·4` | 44 and 84 |
| `crc_of_crc_array` | §7.4, §15.4: CRC over the segment-CRC array | computed |
| Record flags | §7.3 registry: layer MU=1 PE=1 (`0x0003`), metadata MU=0 PE=1 (`0x0002`) | as fixed |
| Pre-trailer pad length | `[R-LIF-02]` step 5: to the next 64-byte boundary | 3 bytes |
| Gap content | `[R-CNT-03]` SHOULD zero | zeroed |
| `file_id` | §9.3: nonzero, SHOULD be random | arbitrary nonzero |
| `version_minor` | `[R-CNT-26]` SHOULD floor | 0 |
| `flags` | `[R-CNT-08]`: creator MUST write 0 | 0 |

### 1.3 The emitted file

```
  [     0,    16)      16  front signature block        front block
  [    16,    17)       1  mask stored tile 0           stored-tile extent
  [    17,    18)       1  mask stored tile 1           stored-tile extent
  [    18,    62)      44  mask tile-index region       record extent (layer record's slot)
  [    62,   512)     450  ---- SLACK (A=512 forces it) ----
  [   512,   592)      80  temp stored tile 0           stored-tile extent
  [   592,  1024)     432  ---- SLACK ----
  [  1024,  1104)      80  temp stored tile 1           stored-tile extent
  [  1104,  1536)     432  ---- SLACK ----
  [  1536,  1616)      80  temp stored tile 3           stored-tile extent
  [  1616,  1700)      84  temp tile-index region       record extent
  [  1700,  1725)      25  user-metadata extent         record extent
  [  1725,  1981)     256  directory region             the directory
  [  1981,  1984)       3  pre-trailer pad              SLACK
  [  1984,  2048)      64  trailer                      the trailer
F = 2048 (mod 64 = 0);  dir_offset = 1725, dir_length = 256, dir_end = 1981 ≤ F-64 = 1984
live-claimed = 731 bytes;  slack = 1317 bytes (64% of the file — all of it alignment)
```

`temp` index entries as emitted:

```
 ordinal 0: 00 02 00 00 00 00 00 00 | 50 00 00 00 00 00 00 00 | fe 6f 93 de
 ordinal 1: 00 04 00 00 00 00 00 00 | 50 00 00 00 00 00 00 00 | 01 64 2a f7
 ordinal 2: ff ff ff ff ff ff ff ff | ff ff ff ff ff ff ff ff | 00 00 00 00
 ordinal 3: 00 06 00 00 00 00 00 00 | 50 00 00 00 00 00 00 00 | cd 68 f1 60
 segment CRC array: 43 e3 20 62   crc_of_crc_array = 0x39BD5173
```

Trailer, at file offset 1984, field by field (offsets are within the trailer):

```
 [ 0, 8)  8a 4e 52 41 54 0d 0a 1a   trailer magic
 [ 8,10)  01 00                     version_major = 1
 [10,12)  00 00                     version_minor = 0
 [12,16)  00 00 00 00               flags = 0
 [16,24)  01 00 00 00 00 00 00 00   generation = 1
 [24,32)  bd 06 00 00 00 00 00 00   dir_offset = 0x6BD = 1725
 [32,40)  00 01 00 00 00 00 00 00   dir_length = 0x100 = 256
 [40,48)  00 08 00 00 00 00 00 00   committed_file_length = 0x800 = 2048
 [48,56)  18 07 f6 e5 d4 c3 b2 a1   file_id = 0xA1B2C3D4E5F60718
 [56,60)  00 00 00 00               reserved
 [60,64)  75 d1 ed 8c               CRC-32C over [0,60) = 0x8CEDD175
```

**Everything in the creation walk was determined by the document** except the
free choices the document names as free. I did not have to guess once to emit
a conforming file. That is a genuinely good result and I want to say it plainly
before the findings.

Two things worth recording as *consequences* rather than defects:

* The alignment declaration cost me 1314 bytes of slack on a 731-byte payload.
  §16.1's Note recommends 4096, which on this file would have cost ~12 KB. The
  document nowhere warns that `A` on a small-tile layer is pathological; §16
  says only that a scattering writer "wastes space rather than violating a
  rule". Not a defect — a design consequence I would want a writer's docs to
  state.
* A layer whose *addressed* tile count is zero has extent slot `(0,0)` and
  `crc_of_crc_array = 0` (§7.4, `[R-CNT-23]`), which is a different state from
  a layer with `entry_count > 0` whose entries are all sentinels — that one has
  a real region and a real CRC. The document distinguishes these cleanly and
  §15.4's closing Example says so explicitly.

---

## 2. The append procedure

### 2.1 Commit 2 — supersede one stored tile of `temp` (§20.3 shape (b))

Order, per `[R-WRT-04]`:

1. **Establish F.** Validate the trailer at the physical end (`[R-LIF-04]`).
   F = 2048.
2. **Open.** §19.1's four steps. The appender is a reader here.
3. **Validate what the commit touches** (`[R-WRT-03]`): trailer + *full*
   directory always, because re-emission relies on every directory byte; plus
   §19.3's layer validation for `temp`; plus the §19.4 index chain for every
   segment whose entries this commit reuses — here `temp`'s one segment.
   `mask` is neither modified nor relied on, so it imposes nothing beyond the
   directory bytes I re-emit.
4. **Write payloads and indexes.** Writing begins at *exactly* F = 2048.
   2048 mod 512 = 0, so the new payload can start there.

```
  new  [ 2048, 2128)   80  temp tile 1 (new payload)
  new  [ 2128, 2212)   84  temp index region, re-emitted IN FULL
  new  [ 2212, 2468)  256  directory 2
  pad  [ 2468, 2496)   28  slack
  new  [ 2496, 2560)   64  trailer 2       F2 = 2560
```

Three entries of the new index region are byte-identical to the old at their
disk-ordinal positions (ordinals 0, 2, 3); one is re-pointed. The whole region
moves because one extent slot addresses it — `[R-WRT-04]` and §20.3's shape (b)
figure say exactly this.

5. **Re-emit the directory** per §20.4: `mask`'s record byte-identical,
   `temp`'s record modified (new extent slot, new `crc_of_crc_array`), the
   user-metadata record byte-identical.
6. **Commit**: barrier (after step 5's CRC); pad; trailer with generation 2,
   the *same* file_id, ignore-lane bits copied forward, version_minor per
   `[R-CNT-26]`; barrier.

**Durability order and commit point.** `[R-LIF-02]` is unambiguous: steps 1–3
(payloads, index regions, record extents, the complete directory and its CRC)
must be durable *before* the pad and trailer are written, and the trailer must
then be made durable itself. Two barriers, not one — §20.2 says so in as many
words for creation ("both barriers, not one") and `[R-LIF-02]` steps 4 and 6
say it for every commit. **The commit point is the moment the new trailer's 64
bytes are the physical tail and durable**; before that, a reader on the default
path sees a torn file (`[R-LIF-05]`).

**Bytes below F are unreachable to an appender.** Step 1 says "begin writing at
exactly F". So slack inside `[0, F)` — 1317 bytes in my file, most of it
alignment gaps big enough to hold the new 80-byte tile — can *never* be reused
by an append. §5.2's "Only compaction (§20.5) reclaims it" is therefore
literally true and not merely a policy: the commit protocol forbids the
alternative. I checked for a permission to write into a gap below F and there
is none.

### 2.2 Commit 3 — add a layer (§20.3 shape (a))

```
  alt tile  [2560,2564)   alt index [2564,2588)   dir [2588,2943)   F3 = 3008
```

Nothing existing moves; `mask`'s and `temp`'s records go into dir₃
byte-identically, extent slots and all. The slack this commit creates is sized
by the file's *layer count* (the old directory) and not by any layer's data —
§20.3's shape (a) note, confirmed by arithmetic.

### 2.3 Appending to a file whose records I do not all understand

The full flag matrix. "Implements" means the updater has a definition for the
type; §20.4 splits the authority of the flags on exactly that line.

| Record | Flags source | What my updater is permitted to do |
|---|---|---|
| type 0x0001 layer | §7.3 registry: MU=1, PE=1 — **stored bits ignored** (`[R-CNT-22]`) | May modify. **May never drop** (PE=1). If retained unmodified, re-emit byte-identically *including a wrong stored flag bit*; if modified, it is new output and MUST carry `MU=1, PE=1`. |
| type 0x0002 user metadata | registry: MU=0, PE=1 | Same: may modify (new extent appended, old becomes slack), may never drop. A *stored* MU=1 on this type does not bar the commit — the reader applies the type's fixed semantics (`[R-CNT-22]`). |
| unknown type the updater implements | the definition it implements the type from; **stored bits never** | That definition's PE governs droppability; understanding the type does not confer permission to drop it (§20.4). |
| unknown, unimplemented, **MU=1** (top-level) | stored | **No commit at all.** The updater is a reader first; `[R-CNT-15]` makes it reject-file. Compaction barred on the same ground (`[R-WRT-06]`). |
| unknown, unimplemented, **MU=1** (sub-record) | stored | Retain byte-identical; **MUST NOT modify that layer**. Other layers stay editable (`[R-CNT-18]`, reject-layer never reject-file). |
| unknown, unimplemented, **MU=1 with PE=0** | stored, but read as PE=1 (`[R-CNT-12]`) | Identical to the MU=1 row. Never silently deletable. |
| unknown, unimplemented, **MU=0, PE=1** | stored | Retain byte-identical, **extent content unmodified**. An appender cannot relocate it in any case: `[R-WRT-05]` freezes the extent slot and `[R-LIF-01]` freezes the bytes. Relocation is a compactor's operation only (`[R-WRT-08]`). |
| unknown, unimplemented, **MU=0, PE=0** | stored | Retain, or drop (extent → slack) **only** in a commit that independently changes the scope it attaches to. |
| any record with **reserved bits 2–15 set** | — | Readers ignore them; the verifier records F26/L47. My updater re-emits byte-identically and the nonzero bits survive — §20.3 step 2's "Reproducing a structure's bytes unchanged is not authoring them". |

The MU=0/PE=0 drop condition, applied to my three commits:

* Commit 2 (supersede a tile): **must retain** any such record — §20.4 says so
  expressly ("Superseding a stored tile's bytes is not such a change for either
  kind ... so a commit whose only change is a supersede MUST retain the
  record"). This is the trap I expected to find open and it is closed. Note
  what it costs to close: superseding *does* change `temp`'s layer record bytes
  (slot + `crc_of_crc_array`), so "changes ... that layer's record" has to be
  read as a *logical* change, and the carve-out is what says so.
* Commit 3 (add a layer): changes "the file's layer set", so a top-level
  MU=0/PE=0 record **may** be dropped, and so may a sub-record of any layer
  whose own record changed.
* A commit whose only effect would be the drop: **must retain** (stated).

**A malformed index entry met while re-emitting.** §20.3 step 2 is explicit and
I would not have guessed it: the entry "is carried forward byte-identically at
its disk-ordinal position under step 4, not repaired to a sentinel", and the
appender "MUST NOT repair the defect". It SHOULD report it. So my updater
propagates a latent tile-scope violation into a new generation on purpose.
Determined; unusual; correct per the text.

---

## 3. Slack — which bytes, who counts them, what they may contain

Per commit shape, against my file:

| Shape | Bytes that become slack |
|---|---|
| **append (add layer)** | the superseded directory, its pre-trailer pad, and the superseded trailer. Sized by layer count. In commit 3: 256 + 28 + 64. |
| **append (supersede a tile)** | the above, **plus** every superseded stored-tile extent, **plus** the whole prior tile-index region of every layer whose stored-tile set or index content changed. Commit 2: 80 + 84 + 256 + 64 (+ the 28-byte new pad, which is slack from birth). |
| **in-place update** | does not exist. `[R-LIF-01]` — every mutation is a commit or a whole-file rewrite. A "directory-only" edit (§20.3 shape (c)) is still an append: old directory + pad + trailer become slack. |
| **rewrite under a fresh file_id** | the *input file* is not slack at all — it is a separate artifact that persists until something outside this format deletes it (`[R-PRV-02]`). The output carries no slack from the input. |
| **compaction** | the output carries only live claimants, so its only slack is what alignment and the 64-byte trailer boundary force. The input is untouched. |
| **abandoned partial write** | **none, at the file level.** The bytes past F are not slack: slack is defined against the *live* state (§5.2), and the torn file has no valid live trailer, so there is no live state to define it against. The residue is what `[R-LIF-04]` obliges the next writer to truncate or overwrite, and §9.5's Note says a reader meets it only as a trailer that fails its gates. §5.2 handles the reporting side: where §6.2's ordered validation rejects the file before a live trailer is established, "the total is not owed at all". |

An arithmetic detail I got wrong on the first pass and want recorded, because
it is a real trap for a slack accountant: **generation g's pre-trailer pad is
already slack in generation g.** The commit that supersedes it does not "turn
it to slack" a second time. My ledger only balanced once I stopped
double-counting it: gen-2 slack 1829 = gen-1 slack 1317 + (80 + 84 + 256 + 64
newly unclaimed + 28 new pad). The document is right; my first ledger was not.

**Who counts.** Verifiers, never readers (§5.2's second Note; §9.7). A verifier
that reaches a live state MUST report the total; where its walk did not
enumerate every claimant it MUST report the total as **partial**, say which
scope or violation stopped it, and the partial is `F` less the bytes claimed by
what it did enumerate — an upper bound, never an under-count. I checked that
this is monotone: dropping claimants only raises the number. I also checked the
one way it could under-count — two enumerated claimants overlapping, so that a
naive sum-of-lengths exceeds the union — and the text says "the bytes claimed",
which reads as a set of bytes and therefore a union. §9.7's formulation ("Bytes
the walk does not reach are slack") is union-based and unambiguous. No defect.

**What slack may contain.** Anything. "Slack has no internal structure this
specification defines, its content is unconstrained, and no conformance
requirement applies to it. A reader MUST NOT interpret it" (`[R-CNT-21]`).
Writers SHOULD zero it (`[R-CNT-03]`); a writer that does not "forfeits byte
reproducibility (Appendix G)". Superseded payloads, prior trailers, and prior
directories all sit there, which §23.1 names as the privacy consequence.

---

## 4. Torn-write recovery — six crash points

All against commit 2 (F₁ = 2048, F₂ = 2560, trail₁ at [1984,2048), trail₂ at
[2496,2560)). "Recovers" is §9.6's probe: backward at 64-aligned offsets `o`
from the largest with `o + 64 ≤` physical length, requiring the magic, a
verifying trailer CRC, and `committed_file_length = o + 64`.

| # | Crash point | physical | Next reader sees | Next updater does | Conforming meanwhile? |
|---|---|---|---|---|---|
| 1 | mid new payload | 2088 | tail 64 bytes are payload → trailer magic fails, F8, **reject-file**, "torn or invalid", MUST NOT scan backward (`[R-LIF-05]`) | §20.3 step 1 fails → **no append**; recovery is a separate, deliberate operation | **No.** The whole physical byte sequence is the artifact; `[0,2048)` is a conforming file but that is not what was handed over. |
| 2 | after payload+index, before the directory | 2212 | same: F8 reject-file | probe finds trail₁ at 1984, `cfl = 2048` ✓ → truncate to 2048 → re-verify whole (`[R-LIF-06]`) → append afresh | No |
| 3 | after step 4's barrier, before pad+trailer | 2468 | same: F8 reject-file. Note the directory *is* durable and complete here, and the reader still refuses — which is the point of anchoring at the tail | same recovery to 2048; the durable dir₂ is discarded | No |
| 4 | mid-trailer (trailer bytes partly written) | 2544 | 64 bytes at [2480,2544) are index/dir/trailer fragments → magic fails at the tail (and if by accident it did not, the trailer CRC or `cfl ≠ 2544` would) → reject-file | recovery to 2048 | No |
| 5 | trailer written, barrier not yet honoured | 2560 or 2048 depending on what survived | either generation 2 (valid) or case 4 | either appends from 2560, or recovers to 2048 | Whichever state survives is well-defined; no third state exists |
| 6 | commit complete, then residue appended (`[R-LIF-04]` violated) | 2860 | tail is not a trailer → F8; or if the residue's tail happened to be a valid-looking trailer, `committed_file_length ≠` transport size → **F17**. §9.5's Note: "Residue past a completed commit carries no register row of its own" | probe finds trail₂ at 2496, `cfl = 2560` ✓ → truncate to 2560 | No, and the violation is the *writer's* |

Two things the document gets right that I would have expected to be gaps:

* The mimic problem. A tile payload can contain something that looks like a
  trailer. `[R-LIF-06]` makes re-verification of recovery output normative, and
  §21.6 records the mimic as *inert* under live-state coverage because nothing
  enumerates slack. My crash-4 case is exactly where a mimic would bite and
  the probe's `committed_file_length = o + 64` condition kills most of them.
* On creation there is no earlier trailer, so a crash at any point before the
  gen-1 trailer leaves nothing recoverable. `[R-LIF-06]` says a tool "MUST
  report the candidate it settled on and how many it rejected" — it does not
  spell out the zero-candidate report, but the obligation reads naturally onto
  it. I did not treat this as a finding.

---

## 5. Byte-divergence catalogue

Two conforming writers, identical input arrays, identical stated options
(names, geometry, tiling, layout, codec, filter, fill, metadata content).
Column 3 is Appendix G's item, or "OPEN".

| # | Degree of freedom | Licensed by | Closed by |
|---|---|---|---|
| 1 | `file_id` | §9.3 (nonzero, SHOULD random) | item 2 — but see finding writer-05 |
| 2 | `version_minor` | `[R-CNT-26]` (SHOULD) | item 8 |
| 3 | `flags` ignore-lane bit set | `[R-CNT-08]` makes it a **conduct** rule; the file stays conforming (§2.3) | item 8 |
| 4 | Structure order and placement | `[R-SLB-05]`, `[R-LIF-02]` step 2 | item 3 |
| 5 | Gap extent | `[R-SLB-05]` | item 3 |
| 6 | Gap content | `[R-CNT-03]` (SHOULD zero) | item 3 |
| 7 | Record order in the directory | `[R-CNT-14]` | item 3 |
| 8 | Sub-record order | `[R-CNT-14]`, §7.4 | item 3 |
| 9 | Storing vs. sentinelling an all-fill tile | nothing requires either | item 6 |
| 10 | Fill recorded when the caller chooses none | `[R-TYP-10]` (SHOULD) | item 7 |
| 11 | Encoder output for codecs 2–4 | `[R-CNF-05]` | item 1 (and item 1 concedes cross-implementation identity is unattainable) |
| 12 | DEFLATE final-byte unused high bits | §17.2's Note, expressly unconstrained | item 1 |
| 13 | zstd `Frame_Content_Size` present or absent | `[R-COD-06]` "MAY be present" | item 1 ("fixed encoder settings") |
| 14 | zstd declared window size (≤ decoded size) | `[R-COD-06]` | item 1 |
| 15 | JSON serialization: whitespace, number formatting, escapes | §18.2's Note; `[R-MTA-05]` fixes only key order | item 9 |
| 16 | Metadata storage encoding 1 vs 2 | `[R-MTA-03]` | item 9 |
| 17 | Name normalization | `[R-ENC-14]` (SHOULD NFC) | item 10 |
| 18 | Declaring `A` / `S` / `A_slab` at all | §16 | item 5 |
| 19 | Number of commits | §9 constrains none | item 4 |
| 20 | Pre-trailer pad length | a longer pad is conforming (§6.2, §2.3) | item 3 |
| 21 | Which tiles are stored, beyond #9 | content-determined: any tile with a non-fill sample must be stored | — (no freedom) |
| 22 | Segment CRC of a full all-sentinel segment | `[R-IDX-05]`'s constant *is* the computed value | — (no freedom) |
| 23 | Compactor's discretion to drop MU=0/PE=0 records | §20.4: "A compactor may drop it whenever it rewrites the file" | **OPEN** — finding writer-05 |
| 24 | The `file_id` fallback when the digest's last eight bytes are all zero | item 2: "Any other fixed nonzero value" | **OPEN by design**, disclosed |

Not free, and I checked each: front-block reserved bytes (MUST be zero),
trailer `reserved` (zero), registered record flags (§7.3), reserved flag bits
(zero), sentinel `crc` (0), `crc_of_crc_array` when `entry_count = 0` (0),
linearization (1), index_encoding (1), padding content (§14.5), pad bits
(§14.5), interleaved bool bytes (§14.2), in-tile sample order (row-major, "for
every linearization value, permanently").

**Claims in Appendix G I tried to falsify.** Item 3's ordering key is
well-founded: it masks `extent_offset` (the one component that would depend on
its own result), and every remaining component — type, flags, `inline_length`,
`extent_length`, inline payload, extent contents — is a function of content.
Layer records tie by name, so the key never has to read a layer record's
`crc_of_crc_array`, which would otherwise be circular through tile placement.
I could not break it. Item 6 plus item 7 compose correctly: the note that item
7 "reaches further than the fill field" because item 6 makes storedness depend
on fill is exactly right. Item 2's compactor carve-out is right for the reason
it gives. What I *could* falsify is the appendix's opening claim and one
sentence of item 3 — findings writer-04 and writer-05.

---

## 6. Findings

### writer-01 — CONTRADICTION — §20.5, `[R-WRT-07]` vs `[R-SLB-01]`/`[R-SLB-03]`

**Location.** §20.5, `[R-WRT-07]`; against §16.1 `[R-SLB-01]`, §16.2
`[R-SLB-03]`, and §20.2 `[R-WRT-02]`.

**Quotation.** §20.5:

> A compactor preserves content but not placement — placement is not among the
> things it carries forward, and it is free to place structures anywhere §5.2
> admits

against §16.1:

> When declared: every stored tile's offset satisfies offset mod A = 0.

and §20.2, which states the carve-out its sibling omits:

> any record extents, in any order satisfying §5.2's coverage classes
> (`[R-CNT-02]`, `[R-CNT-03]`) and every declared layout invariant
> (`[R-SLB-01]`, `[R-SLB-03]`) — placement is otherwise free (`[R-SLB-05]`)

**Detail.** §5.2 admits any placement that partitions and does not overlap. It
knows nothing of `A`, `S` or `A_slab`. A compactor whose input carries a layer
declaring `A = 4096` cannot in fact place that layer's tiles "anywhere §5.2
admits": `[R-SLB-01]` binds every stored tile in the output generation, and
L40 records the violation as reject-layer. Nor can the compactor escape by
clearing the declaration, because `[R-WRT-07]`'s own exception list is closed —
"except that relocation re-points extent slots, regenerates each relocated
tile-index region ..., and updates the layer-record fields covering a
regenerated region (`crc_of_crc_array`)" — and clearing `A` is not on it. So
the sentence is false exactly where a compactor most needs guidance, and the
parallel creation procedure two subsections earlier states the correct rule in
the same breath as the same freedom.

There is a second edge under the same sentence. `[R-SLB-04]` expressly offers
a writer that changes "the byte placement of any run of a slab-declared layer"
the alternative of clearing the declaration — which every compaction does to
every run — while `[R-WRT-07]`'s closed exception list forbids the clearing.
An implementer reading §16.2 concludes clearing is available; one reading
§20.5 concludes it is not.

**What I picked and why.** I honour `A` and `S` in compaction output and never
clear a declaration, because §20.5's own `[R-WRT-06]` says "Given a conforming
input the output is a conforming file" and `[R-CNF-06]` binds an updater to
every writer requirement for the bytes it produces. Those two decide it; the
quoted sentence is simply wrong.

**What an implementer does wrong without it.** Packs a slab- or
alignment-declared layer's tiles contiguously from offset 16 and emits a file
that a verifier rejects at layer scope (L40/L41/L42) — having followed the
compaction procedure literally.

**Byte-level?** No. `[R-CNF-06]` and §20.5's own "Given a conforming input the
output is a conforming file" already decide which output is permitted; only
§20.5's sentence is wrong. No verifier verdict is in doubt: the unaligned
output is nonconforming under L40 either way.

### writer-02 — AMBIGUITY — §20.3 step 4 states the alignment obligation over *new* tiles only

**Location.** §20.3 step 4, `[R-WRT-04]`; against §16.1 `[R-SLB-01]` and
§21.3 row L40.

**Quotation.** §20.3 step 4:

> Extents this commit supersedes become slack (`[R-CNT-21]`); a slab
> declaration is re-established or cleared (`[R-SLB-04]`), and an aligned
> layer's new tiles satisfy its invariant or the declaration is cleared
> (`[R-SLB-01]`, `[R-CNF-05]`).

**Detail.** The two halves of this sentence are not parallel and the difference
is load-bearing. The slab half delegates to `[R-SLB-04]`, which reaches every
retained tile: "MUST either re-establish the invariants for every such run — or
clear the declaration". The alignment half is quantified over *new tiles*.
`[R-SLB-01]`'s invariant is not so quantified — "every stored tile's offset
satisfies offset mod A = 0", over every tile stored in the generation, whether
this commit wrote it or carried it forward. So a commit that newly declares
`A = 4096` on a layer whose retained stored tiles sit at arbitrary offsets
satisfies §20.3 step 4 as written and violates `[R-SLB-01]` (L40).

Permitted readings: (a) §20.3 states the whole alignment obligation, so only
new tiles must be aligned — which contradicts `[R-SLB-01]`; (b) §20.3 is a
summary that under-states, and `[R-SLB-01]` governs. I picked (b): `[R-SLB-01]`
is the rule §20.3 cites, and L40's register row restates the unquantified form.

**What an implementer does wrong without it.** Adds an alignment declaration in
a commit, aligns only the tiles it writes, and ships a layer that any verifier
rejects. The reading also matters for the ordinary case where an already-`A`-
declared layer gains tiles: the writer must check that the retained tiles still
satisfy the invariant (they do, since nothing moved) — harmless there, but the
sentence gives no reason to look.

**Byte-level?** No. `[R-SLB-01]` and L40 already decide which offsets a
conforming file may carry; the resulting file's verdict is not in doubt.

### writer-03 — AMBIGUITY — no rule reaches a declaration change that de-addresses a stored tile

**Location.** §20.3 step 4, `[R-WRT-04]`; §11.1's Rationale; §21.7
`[R-ERR-01]`.

**Quotation.** §20.3 step 4:

> A commit MUST NOT change a layer's declarations in a way that alters, for any
> tile that layer stores **in the generation this commit supersedes**, what §14
> fixes for its stored bytes or how they decode — the set of padding positions
> (§11.3) and the content `[R-SER-05]` fixes there, the decoded size, the byte
> offset of any sample within the decoded tile image, or the codec and filter
> that produced the stored bytes. ... The test is the effect on such a tile

and §11.1, the *only* place in the document where the word "shrink" occurs
(I checked: `grep -c shrink` = 1, and it is inside a Rationale):

> Extents grow; a shrink is barred wherever it alters what §14 fixes for a tile
> the layer already stores (§20.3, which states the tense normatively and
> governs), which is the ordinary case

**Detail.** §20.3 expressly permits growth ("an extent MAY **grow**") and
expressly forecloses the escape route of unstoring — "a commit does not escape
this by unstoring in the same breath: superseding every tile of a layer and
re-declaring it are one operation, and this bars it". Unstoring keeps the tile
*addressed*: it gets a sentinel entry, and the bar's quantifier still reaches
it. Shrinking a dimension extent across a grid boundary does something the
document never names: it removes tiles from the address space entirely, so
they have no entry in the new generation at all.

Concretely, on my `temp` layer: extents (5,5), T=(4,4), G=(2,2), N=4, tiles
0, 1, 3 stored. A commit shrinking `E_y` from 5 to 4 gives G=(1,2), N=2. Tiles
0 and 1 survive with their ordinals and their padding sets unchanged — nothing
§14 fixes for them moves. Tile 3's 80 stored bytes simply stop being addressed
and fall to slack, exactly as a superseded payload does. `entry_count` goes
4 → 2, `extent_length` 84 → 44, and the resulting file passes every check I can
apply: coverage partitions, `[R-CNT-17]` holds, every CRC verifies.

Permitted readings of the bar:

* **(A) barred.** The quantifier ranges over tiles stored in the superseded
  generation, tile 3 is one of them, and what §14 fixed for it — an 80-byte
  image with 15 fill-encoded padding positions — is now nothing at all, which
  is an alteration. §11.1's "which is the ordinary case" is consistent with
  shrinks being almost always barred.
* **(B) permitted.** The test is "the effect on such a tile", and the
  elaboration says a change "that leaves every one of those tiles' stored bytes
  meaning exactly what they meant ... is not what this bars". A *superseded*
  tile's old bytes also stop meaning anything, and superseding is the core
  append operation — so "meaning what they meant" cannot be about continued
  reachability. Under that reading the test is about how still-stored bytes
  decode under the new declarations, and a de-addressed tile is outside its
  domain. The four items in the list all presuppose a tile that still has a
  decoded image.

I picked **(A)**, because §20.3's tense clause shows the drafters intend the
prior-generation quantifier to bite hard, and because (B) makes a two-commit
sequence (unstore everything; then re-declare) equivalent to a one-commit
sequence that §20.3 expressly bars — which would make the bar decorative. But
I record that I am guessing: the sentence that would decide it lives in a
Rationale (§11.1) that §2.1 gives no force, and that Rationale in any case
defers back to §20.3, which never mentions shrinking.

**What an implementer does wrong without it.** Under (B) my updater offers
"shrink an extent" as an ordinary append and produces a smaller-domain layer at
the cost of orphaned payloads; under (A) it must refuse and tell the caller to
write a new layer or rewrite the file. §20.3 step 4's enumeration of what the
re-emitted index region contains — "tiles this commit stores or supersedes ...
tiles that become unstored ... entries new to this generation (added tiles,
grown extents) ... every other entry byte-identical" — names only growth among
geometry changes, which is what first made me look.

**Byte-level?** No, though it is the closest call in this set. Two conforming
updaters given the same instruction produce different bytes on disk — one
emits generation 2, the other refuses — but §21.7 places this bar in the class
that leaves no file-level witness ("a commit that supersedes every tile it
would have damaged leaves the live state clean, so the bar is unwitnessed
there"), so no reader's or verifier's verdict on the emitted file differs under
either reading. It forks a tool's conduct, not any file's accept/reject
verdict.

### writer-04 — OBSERVATION — Appendix G item 3's "first structure begins at 16" is unsatisfiable under item 5

**Location.** Appendix G, item 3 (non-normative).

**Quotation.**

> The first structure begins at 16, directly after the front signature block,
> which §5.2 counts as no structure; each later structure begins where the
> previous one ended, save where alignment forces a gap — a declared A or
> A_slab, or §6.2's 64-byte trailer alignment, the pre-trailer pad included —
> and every byte of every such gap is zero

**Detail.** The "save where alignment forces a gap" proviso is attached
grammatically to the *later*-structures clause. Under item 3's own total order
the first structure is the first stored tile of the alphabetically-first layer,
and item 5 expressly contemplates "fixed declared values" of `A` and `A_slab`.
If that layer declares `A ≥ 512` its first stored tile cannot begin at 16 —
`[R-SLB-01]` forbids it — so the profile as literally worded is unsatisfiable
for exactly the configuration item 5 licenses. My own file hits this the
moment I reorder the layers: `mask` sorts first and declares no alignment, so I
escaped it by luck of the alphabet; had `temp` been named `alt`, item 3 would
have required its `A = 512` first tile at offset 16.

The charitable reading — the proviso is a general one on the placement rule —
is the only one that yields a file at all, and it is fully determinate (the gap
`[16, A)` is forced and zeroed). I record it as an OBSERVATION because deciding
it costs a reader more than it should for a passage whose whole purpose is to
leave nothing to the writer.

**Byte-level?** No. The appendix is non-normative and "adds no requirement to
any actor"; `[R-SLB-01]` forces the aligned offset regardless of which reading
one takes, so no conforming file's bytes or verdict turn on it.

### writer-05 — OBSERVATION — Appendix G's opening claim is falsified by a freedom the items do not close

**Location.** Appendix G, opening paragraph, against §20.4's compactor
sentence and Appendix G item 2.

**Quotation.** Appendix G:

> Applications that need byte-identical output — content-addressed storage,
> reproducible builds — can adopt this profile, which closes the degrees of
> freedom this format deliberately leaves open.

against §20.4's MU = 0 / PE = 0 row:

> A compactor may drop it whenever it rewrites the file.

**Detail.** The profile is written to be adoptable by compactors — item 2 says
so in terms ("a compactor adopting the profile takes `[R-WRT-06]`'s fresh draw
instead"), and item 4's "one generation" is satisfied by a compaction output at
generation 1. But §20.4 gives a compactor unconditional discretion over every
MU = 0 / PE = 0 record, and no item of the profile pins that discretion. Two
profile-conforming compactors given the same input therefore emit different
record sets, different directories, different `dir_length`, and — because item
2 derives `file_id` from the emitted bytes — different `file_id`s. The opening
claim is false for that case.

Item 2 leaves a second, smaller freedom open on its face: "Any other fixed
nonzero value is substituted in the measure-zero case that they are all zero."
That one is disclosed and deliberate, and I classify it as *legitimate and
knowingly left open* rather than as a defect; I mention it only because the
opening sentence claims otherwise about both.

**What an implementer does wrong without it.** Ships a content-addressed store
that treats "compacted under the profile" as reproducible, then finds two
compactors disagreeing on a file's digest because one dropped an ancillary
record the other kept. The fix is a profile item: a compactor adopting the
profile retains every record §20.4 permits it to drop (or drops every one).

**Byte-level?** No. The appendix adds no requirement to any actor and both
compactors' outputs are conforming files; `[R-CNF-05]` already licenses two
writers to differ.

---

## 7. Things I checked and did not report

Recorded so a triager can see the negative space.

* **§16.2's transparency rule** (structurally-bad entries transparent to slab
  run continuity; crc-failing entries not). I stressed it against §15.3's six
  *structural* rows (I counted them: exactly six), against §9.7's coverage
  walk, and against L41's parenthetical. All three agree, and the claim that
  the invariant "stays decidable from the index entries alone, given the
  committed file length" is true: transparency is decided by the entry's own
  20 bytes plus F, and every well-formed non-sentinel entry is opaque whether
  or not its payload's crc verifies. This is the most carefully-joined text in
  the changed set.
* **§5.2's partial-total rule.** Monotone, an upper bound, and union-based.
  The pre-live-trailer exemption is stated. The L18 / L40–L42 discard rule
  raises the bound rather than lowering it. No defect.
* **§21.1's instance criterion.** Totals to 273 exactly, and the two stated
  axes (layout formulas; magnitude direction) are applied consistently across
  T3/T14/T21/T22/L21/L22/L30/L44 and the no-direction checksum rows. No
  defect.
* **§20.3 step 4's list of what a declaration change may not alter.** I tried
  to break it with: interleaved channel reorder at equal element sizes (caught
  — byte offsets), tile-extent permutation preserving P (caught — byte
  offsets), int32 → float32 (permitted, and correctly so: §12.3 makes values
  bit patterns, so nothing a reader returns changes), int8 → bool interleaved
  (caught, but only by the lead-in and not by the four-item list — which the
  text expressly anticipates: "the list names where that effect arises rather
  than standing on its own"), fill change on a layer with pad bits but no
  padding positions (caught by the lead-in and by shape (c)'s example, not by
  the list). The lead-in carries the rule and says so. Good.
* **§20.3 step 4's "`[R-COD-07]`'s lz4 decoded-size cap being the one such
  bound in format major 1".** Growth can also newly breach `[R-ENC-04]` (N,
  N·P, C·N, and the `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4` term all grow
  with extents; L2 registers them). But `[R-ENC-04]`'s bound is imposed by
  §4.2 on every derived quantity, not by "the layer's own declarations", and
  §17.2's Note already says `[R-ENC-04]` "carries no such quantifier — it
  binds any sum or product a file yields". The gloss is defensible and the
  operative clause ("every bound the layer's own declarations impose") is
  complete. Not filed.
* **Appendix G item 3's "ordered by type"** does not say *ascending*. The
  preceding sentence says "ascending record order" and this sentence defines
  that order, so ascending carries over. Not filed.
* **`[R-LIF-06]`'s zero-candidate case** on a torn creation. Not filed.
* **The two-commit circumvention of §20.3's bar** (commit 1 unstores every
  tile; commit 2 re-declares freely under the same step's own permission).
  This is a consequence of the rule, not a defect in it, and §20.3 states both
  halves plainly.
* **Appendix A**, §7.4's example, §15.4's examples, §14.2/§14.3/§14.5's
  examples, §17.3's example, §16.2's example — all recomputed, all correct.

## 8. Confidence

**High** that a writer and updater built from this document alone would
interoperate. I emitted a conforming file without guessing once, appended to it
twice, walked six crash points, and balanced the slack ledger — the one error
in that ledger was mine, not the document's. The five findings are all in
writer *procedure* prose (§20.3, §20.5, Appendix G) rather than in the byte
formats, and none of them changes which bytes a reader must accept or reject.
The place I would most want a second opinion is writer-03: it is the one
question where two competent updaters would take different actions and I had to
pick a reading from a Rationale that disclaims force.
