# Cleanroom round 13 — Writer implementer transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in
full, in four `Read` calls. I opened no other file in the repository — no ADR, no
`PLAN.md`, no `AGENTS.md`, no `conformance/`, no `spec/registry.json`, no git
history, no web. I did not list any directory. Everything else I ran was local
computation over strings I typed myself or over files I created in my own
scratchpad:

- a CRC-32C implementation written from §4.5's parameters (polynomial 0x1EDC6F41
  reflected → 0x82F63B78, reflected in/out, init/final 0xFFFFFFFF), checked
  against §4.5's own check vector;
- `build.py` / `append.py`, which emit `gen1.tarn`, `gen2.tarn`, `gen3.tarn` in my
  scratchpad — files I wrote, then read back with my own code;
- three short `python3 - <<EOF` scripts that parse §21's register tables **out of
  the spec file** to count rows/instances and check the Detector/Detected columns.

I wrote this transcript to the single output path named in the brief. I did not
read that directory.

---

## 0. How I worked

I read the document end to end first, then built a small file byte by byte,
then appended to it twice, then walked the flag matrix, the slack ledger, the
crash points, and the divergence catalogue on paper. Everywhere I had to make a
decision I recorded whether the document made it for me or left it to me. I
verified every worked numeric example the document contains, because three
previous rounds found defects in text nobody had touched recently and a worked
example is the cheapest place for one to hide.

**Every worked example in the document checks out.** I list the verifications in
§8 below. That is a real (negative) result and I want it stated plainly rather
than buried: I found no arithmetic error anywhere in §§4.5, 7.4, 11.2, 11.4,
12.1, 12.3, 14.2, 14.3, 14.5, 15.4, 16.2, 17.3, 20.3, 21.8, 21.9 or Appendix A.

---

## 1. Creation: a file built byte by byte

### 1.1 What I chose to build, and why

I wanted a file that is small enough to dump and non-trivial enough to exercise
the corners a writer actually trips on: an interleaved layer with a mixed-width
channel set (so the sample stride Q ≠ any single element size), an **edge tile**
(so `[R-SER-05]`'s padding content is live), **sentinel** entries (so §15.2 is
live), and a **file-scope user-metadata record** (so the extent-with-terminal-CRC
shape is live).

Layer `grid`:

| Declaration | Value | Fixed by |
|---|---|---|
| name | `grid` | me (input) |
| layout | 1 = interleaved | me |
| linearization | 1 = row-major | **document** — `[R-GEO-05]` permits no other value |
| codec | 1 = none | me |
| filter | 1 = none | me |
| alignment A | 0 | me |
| slab S, A_slab | 0, 0 | me; A_slab = 0 **forced** by S = 0 (`[R-CNT-23]`) |
| rank d | 2 | me |
| channel count C | 2 | me |
| dim `y` | E = 5, T = 4 | me |
| dim `x` | E = 5, T = 4 | me |
| chan `v` | uint16 (7), fill `CD AB` = 0xABCD | me; fill **length** forced to 2 by §12.1's element size (`[R-CNT-23]`) |
| chan `m` | bool (1), fill `01` | me; fill byte constrained to 0x00/0x01 by `[R-TYP-07]` |
| index_encoding | 1 | **document** — `[R-CNT-23]`, only value defined |
| entry_count | 4 | **document** — `[R-CNT-17]` ties it to the geometry |
| crc_of_crc_array | 0x3ED5708B | **document** — §15.4 |

Derived, all forced: G = (⌈5/4⌉, ⌈5/4⌉) = (2, 2); N = 4; P = 16; Q = 2 + 1 = 3;
decoded size = P·Q = 48 (`[R-SER-02]`); addressed-tile count = N = 4 (interleaved,
`[R-GEO-03]`); index extent_length = 4·20 + ⌈4/2¹⁶⌉·4 = **84** (`[R-CNT-17]`).

I store the tiles at spatial ordinals 0 and 3 and leave 1 and 2 unstored.
Ordinal 3 is tile coordinates (1, 1), covering y ∈ [4,8), x ∈ [4,8) — **one real
position (4,4) and fifteen padding positions**, exactly the shape §14.5 governs.

### 1.2 Emission order, and what fixed it

`[R-LIF-02]`'s creation path is explicit: *"the writer first emits the front
signature block (§6.1) … then performs steps 2–6, writing beginning at offset 16,
with generation 1."* So byte 0 is fixed and byte 16 is where I start. Within
step 2 the order is mine: *"append new stored-tile payloads and tile-index
regions … in any order satisfying §5.2's coverage classes"*, and `[R-SLB-05]`
confirms *"its stored tiles MAY occupy any non-overlapping byte positions, in any
order"*. I chose tiles, then index, then the metadata extent, then the directory
(`[R-CNT-05]` forces the directory last: *"Writers MUST place the directory so
that no structure lies between its end and the trailer"*).

### 1.3 The map

```
[0,   16)   16   front signature block          89 54 41 52 4E 0D 0A 1A + 8 zero
[16,  64)   48   grid tile s=0  (all real)      codec 1 ⇒ length = decoded size (R-COD-04)
[64, 112)   48   grid tile s=3  (edge tile)
[112,196)   84   grid tile-index region         4×20 entries + 1×4 segment CRC
[196,253)   57   file-scope user-metadata extent 53-byte JSON + 4-byte terminal CRC
[253,407)  154   directory region               2 records (125 + 25) + 4-byte CRC
[407,448)   41   pre-trailer pad                slack, zeroed by R-CNT-03's advice
[448,512)   64   trailer                        generation 1
                 F = 512, F mod 64 = 0
```

Selected bytes, from my dump:

```
0000  89 54 41 52 4E 0D 0A 1A  00 00 00 00 00 00 00 00   front block
0010  E8 03 00 E9 03 01 EA 03  00 EB 03 01 ...           tile 0: v,m,v,m,... stride Q=3
0040  E8 03 00 CD AB 01 CD AB  01 CD AB 01 ...           tile 3: one real sample,
                                                          then 15 × (CD AB | 01) = fill
0070  10 00 00 00 00 00 00 00  30 00 00 00 00 00 00 00   entry 0: offset 16, length 48
0080  04 B6 A2 31 FF FF FF FF  FF FF FF FF FF FF FF FF   entry 0 crc; entry 1 = sentinel
0090  FF FF FF FF 00 00 00 00  FF ...                    …FF×16 00×4
00A8  ...          00 00 00 00  40 00 00 00 00 00 00 00  entry 3: offset 64,
00B0  00 00 00 00 30 00 ...    9C 0E 77 65                length 48, crc 0x65770E9C
00C0  A4 6E 41 D9                                        segment CRC 0xD9416EA4
```

Tile 3 is the interesting one. Position 0 (in-tile ordinal 0, coordinate (4,4))
is the only real sample; ordinals 1–15 are padding. `[R-SER-05]` fixes their
content exactly: *"at every padding position, a writer MUST encode, for each
channel the position carries, that channel's fill value — the recorded fill bytes
for a numeric channel, the recorded fill byte for an interleaved bool channel"*.
So each padding sample is `CD AB` `01`, and the dump shows fifteen of them. I had
no choice here; that is the point of `[R-SER-05]`, and it is what makes the
tile's CRC a function of the logical content rather than of my buffer.

The layer record's inline payload came out at **101 bytes**:

```
 0  04 67 72 69 64             name: length 4, "grid"
 5  01                         layout 1 = interleaved
 6  01 00                      linearization 1
 8  01 00                      codec 1
10  01 00                      filter 1
12  00×8 / 00×8 / 00×8         A = 0, S = 0, A_slab = 0
36  02                         rank d = 2
37  02 00                      channel count C = 2
39  01 79 | 05 00…| 04 00…     dim "y": extent 5, tile extent 4      (18 bytes)
57  01 78 | 05 00…| 04 00…     dim "x": extent 5, tile extent 4      (18 bytes)
75  01 76 07 00 02 CD AB       chan "v": uint16, fill length 2       (7 bytes)
82  01 6D 01 00 01 01          chan "m": bool,   fill length 1       (6 bytes)
88  01                         index_encoding 1
89  04 00 00 00 00 00 00 00    entry_count = 4
97  8B 70 D5 3E                crc_of_crc_array = 0x3ED5708B
```

5 + 34 + 36 + 13 + 13 = 101, no residue, so the sub-record sequence is empty —
`[R-CNT-18]`'s *"MUST parse exactly"* discharged. Record framing: type 0x0001,
flags 0x0003 (MU = 1, PE = 1, **fixed by §7.3's registry table**, not by me),
inline_length 101, extent slot (112, 84).

User-metadata record: type 0x0002, flags 0x0002 (MU = 0, PE = 1, registry-fixed),
inline_length **1** (`[R-MTA-03]`: *"A record whose inline_length is not 1 is a
validity error"*), inline payload `01` (encoding 1 = none), extent (196, 57). The
extent is the 53-byte document `{"tarn.creator":"tarnw 0.1","tarn.title":"demo
grid"}` followed by its 4-byte terminal CRC (§8.1's map row). Members are in
ascending UTF-8 key order — `tarn.creator` < `tarn.title` on byte 6 (0x63 < 0x74)
— which `[R-MTA-05]` makes a **MUST**, not advice.

Trailer, all forced except `file_id`:

```
[448,456) 8A 4E 52 41 54 0D 0A 1A   magic
[456,458) 01 00                     version_major = 1
[458,460) 00 00                     version_minor = 0    (R-CNT-26's floor)
[460,464) 00 00 00 00               flags = 0            (R-CNT-08 MUST)
[464,472) 01 00 …                   generation = 1
[472,480) FD 00 …                   dir_offset = 253
[480,488) 9A 00 …                   dir_length = 154
[488,496) 00 02 …                   committed_file_length = 512
[496,504) 15 7C 4A 7F B9 79 37 9E   file_id (my draw; SHOULD be CSPRNG, §9.3)
[504,508) 00 00 00 00               reserved, zero
[508,512) 42 42 F6 A2               trailer CRC over [448,508)
```

`[R-CNT-09]`'s SHOULD: dir_length + pad + 64 = 154 + 41 + 64 = 259 ≪ 65,536. Met.

### 1.4 Creation decisions the document left to me

Placement and ordering of every structure; which tiles to store; tile extents;
layout; codec and filter; alignment and slab (declared or not); fill values;
record order in the directory; `file_id`; the JSON serialization; whether to
carry user metadata at all. Everything else in the 512 bytes is forced.

**I did not have to guess anywhere in the creation path.** Every byte is either
pinned by a requirement I can cite or explicitly labelled a writer's choice.

---

## 2. The append procedure

### 2.1 Generation 2 — add a layer

Layer `mask`: **planar**, one bool channel `m2` with fill `01`, dims y(E=5, T=3),
x(E=5, T=3). I picked T = 3 deliberately so that P = 9 and the packed plane has
**pad bits** — the one construct §14.3 and §14.5 govern jointly.

Forced arithmetic: G = (2, 2), N = 4, C = 1 → entry_count = C·N = **4**
(`[R-GEO-03]`); decoded size = ⌈P/8⌉ = ⌈9/8⌉ = **2** bytes (`[R-SER-03]`);
extent_length = 4·20 + 4 = 84.

Tile at disk ordinal 0 (c = 0, s = 0) covers y,x ∈ [0,3) — all real. Byte 0 holds
values 0–7, byte 1 holds value 8 in bit 0 and **seven pad bits** in bits 1–7.
`[R-SER-05]`: *"Every pad bit (§14.3) MUST carry the plane's channel's fill bit."*
Fill is true, so bits 1–7 are all 1 and the tile is `55 FF`.

Tile at disk ordinal 3 (c = 0, s = 3) is tile coordinates (1,1), covering
y,x ∈ [3,6): four real positions and **five padding positions** (k = 2,5,6,7,8),
each of which must carry the fill bit 1, plus seven pad bits also 1. Result
`F5 FF`. Both mechanisms in one tile, and §14.3's Note is right that they are
different mechanisms: k = 2,5,6,7 are padding *positions* inside the value region;
bits 1–7 of byte 1 are pad *bits* past the last value.

The layer record's inline payload is 95 bytes (5 name + 34 scalars + 36 dims +
7 channel + 13 trailing). Placement:

```
[512, 514)   mask tile ordinal 0            writing begins at exactly F = 512 (R-LIF-02 step 1)
[514, 516)   mask tile ordinal 3
[516, 600)   mask tile-index region  (84)
[600, 873)   directory (273)                grid record byte-identical, mask record new,
                                            user-metadata record byte-identical
[873, 896)   pad (23)
[896, 960)   trailer, generation 2, same file_id, flags copied forward
             F₂ = 960
```

The two carried-forward records are copied **byte for byte** — header, inline
payload and extent slot — under `[R-WRT-05]`. The `grid` record's extent slot
still reads (112, 84): §20.3 is explicit that *"A layer whose record alone changes
keeps its extent slot, pointing at the existing region, as does a layer the commit
leaves untouched"*, and my commit does not touch `grid` at all.

Verification depth for this commit, per `[R-WRT-03]`: trailer and **full**
directory always (*"re-emission (§20.4) relies on every directory byte"*), plus
§19.3's layer validation only for layers the commit modifies — none here. So I
never parsed `grid`'s dimension entries, never touched its index region, and
never fetched a tile. That is the whole point of the Part I / Part II
independence §3.3 advertises, and it holds.

### 2.2 Generation 3 — supersede a tile

Supersede `grid`'s tile at ordinal 0 with new content (48 bytes, all-zero
samples — note this is *not* all-fill, since fill is 0xABCD/0x01, so §13's
sentinel option is unavailable and the tile must be stored).

```
[960, 1008)  new grid tile ordinal 0 (48)
[1008,1092)  new grid tile-index region (84)   — the WHOLE region, R-WRT-04
[1092,1365)  directory (273)
[1365,1408)  pad (43)
[1408,1472)  trailer, generation 3
             F₃ = 1472
```

Inside the new index region: entry 0 re-pointed to (960, 48) with a fresh crc,
entries 1 and 2 written as sentinels again, and **entry 3 copied byte-identically
at its disk-ordinal position** — `[R-WRT-04]`'s *"every other entry
byte-identical at its disk-ordinal position"*. The layer record is modified
(extent_offset 112 → 1008, crc_of_crc_array recomputed), so it is *"new output
under its writer obligations"* (§20.4); `mask`'s record and the user-metadata
record are byte-identical carries.

Note the cost shape §20.3's Note quantifies: I changed 48 bytes of payload and
paid 84 bytes of index plus 273 bytes of directory plus 64 of trailer for it, and
stranded 132 bytes (old tile + old index) as slack. On a 10⁶-tile layer the
index term is ~20 MB. That is a real property of the format and the document
states it.

### 2.3 Write order, durability, commit point

`[R-LIF-02]` is unambiguous and I followed it literally:

1. begin writing at exactly F (never at the physical end, when they differ —
   `[R-LIF-04]`);
2. payloads, index regions, record extents, in any order;
3. the complete directory, then its CRC;
4. **barrier** — everything in 1–3 durable;
5. pad to the next 64-byte boundary, then the 64-byte trailer;
6. **barrier** — the trailer durable.

`[R-WRT-02]` insists on *"both barriers, not one"*, and the reason is visible in
step 5: the trailer is the only structure that makes anything reachable, so if it
lands before the bytes it points at, a reader validates a trailer over a garbage
directory. §9.2's Note owns that case: *"§8's chain still catches every
inconsistent state loudly."*

**The commit point is step 6**: the instant the new trailer is durable at the
physical end with `committed_file_length` equal to the new F. Before that instant
the file is not the old generation either — §9.2's figure says so directly
(*"trailₙ intact, but no longer at the file's end"*). The window is one in which
the old state is *recoverable*, not *readable*.

One question the document answered better than I expected: **what does "pad to the
next 64-byte boundary" mean when the directory already ends on one?** §6.2
resolves it — *"a writer that ends its directory on a 64-byte boundary leaves
none"* — so zero, not sixty-four. Without that sentence I would have had a
genuine byte-level fork on every file whose directory happens to end aligned.

### 2.4 Appending to a file whose records I do not all understand

The document defines exactly two record flag bits (§7.2: bit 0 MUST_UNDERSTAND,
bit 1 PRESERVE_ON_EDIT) plus reserved bits 2–15. §20.4 splits the flag *source*
three ways before it applies any obligation: registry-fixed for a type §7.3
registers; the implementer's own definition for a type it implements that this
specification does not register; the **stored** bits for a type it does not
implement. Here is my updater's complete decision table.

| Type | Stored flags | Top-level | Layer sub-record |
|---|---|---|---|
| 0x0001 layer | any | Registry governs (MU=1,PE=1). Retain byte-identical, or modify as new output emitting flags 0x0003. Never droppable. | Illegal position — L26, reject-layer (`[R-CNT-18]`) |
| 0x0002 user metadata | any | Registry governs (MU=0,PE=1). Retain byte-identical, extent unmodified. Never droppable. | same |
| implemented, unregistered | ignored | My definition's MU/PE supply the obligation; stored bits *never* do | same |
| unknown | MU=1, PE=1 | **No commit at all.** `[R-CNT-15]` makes it reject-file; my updater is a reader first (§2.3) | Blocks modification **of that layer only**; other layers stay editable (`[R-CNT-18]`) |
| unknown | MU=1, PE=0 | Read as PE=1 (`[R-CNT-12]`), so identical to the row above. Also F25/L46 for a verifier | same |
| unknown | MU=0, PE=1 | Retain byte-identical, **extent content unmodified**. May not relocate the extent — `[R-WRT-08]` allows that only *"under §20.5"*, i.e. compaction | same |
| unknown | MU=0, PE=0 | Retain byte-identical, **or** drop it (extent → slack) — but only in a commit that *independently* changes the file's layer set or another non-layer top-level record | Drop only in a commit that independently changes that layer's record, the entry set of its index, or which of its tiles are stored |
| any | reserved bits 2–15 set | Ignore the bits (`[R-CNT-12]`); re-emit byte-identically; F26/L47 for a verifier; SHOULD report (§20.3 step 2) | same |

Two things I checked and found correctly closed:

- **Superseding a tile does not license a drop.** §20.4 says so explicitly:
  *"Superseding a stored tile's bytes is not such a change for either kind — it
  re-places that layer's index region (§20.3, `[R-WRT-04]`) without altering the
  scope any record attaches to — so a commit whose only change is a supersede
  MUST retain the record."* My generation 3 is exactly that commit, and it
  retains everything.
- **A drop cannot bootstrap itself.** *"Dropping the record, or dropping another
  record in the same commit, is not itself such a change either."* Without that
  sentence every commit would license every drop.

And one place where I had to reason rather than read: an unknown MU = 1
**sub-record** is a layer-access-tier condition, but my open (§19.1) never walks
sub-records and `[R-WRT-03]` only obliges §19.3 validation for layers the commit
modifies. So an appender adding an unrelated layer will *never discover* the
critical sub-record — and that is fine, because it never modifies that layer and
`[R-WRT-05]` carries the record forward unread. The document does not say this in
one place, but §20.3 step 2's *"A violation the open establishes bars the commits
its outcome bars and no others"* plus `[R-WRT-03]`'s reliance principle compose
to it without residue.

---

## 3. Slack, per commit shape

The ledger for my three generations, computed by partitioning F₃ = 1472 against
the live claimants §9.7 names (front block, each record's extent, each
non-sentinel entry's stored extent, the directory, the trailer):

| Live claimant | Range | Bytes |
|---|---|---|
| front signature block | [0,16) | 16 |
| grid tile ordinal 3 | [64,112) | 48 |
| user-metadata extent | [196,253) | 57 |
| mask tile ordinal 0 | [512,514) | 2 |
| mask tile ordinal 3 | [514,516) | 2 |
| mask index region | [516,600) | 84 |
| grid tile ordinal 0 (gen 3) | [960,1008) | 48 |
| grid index region (gen 3) | [1008,1092) | 84 |
| directory (gen 3) | [1092,1365) | 273 |
| trailer (gen 3) | [1408,1472) | 64 |
| **total claimed** | | **678** |

Slack = 1472 − 678 = **794**, and it partitions exactly into nine runs:
superseded grid tile 0 (48), gen-1 grid index (84), dir₁ (154), pad₁ (41),
trail₁ (64), dir₂ (273), pad₂ (23), trail₂ (64), pad₃ (43). No byte is
double-claimed and none is unaccounted; `[R-CNT-02]`'s partition holds.

Now the charter's question, shape by shape.

**Append that adds a layer (gen 2).** Slack created: the previous generation's
directory, pre-trailer pad, and trailer — 154 + 41 + 64 = 259 — plus this
commit's own pad (23). Nothing else. §5.1's figure says exactly this: *"The ▓ runs
are the directories, pads and trailers of commits 1 and 2, superseded when commit
3 wrote its own."* Crucially the cost is *"sized by the file's layer count, never
by any layer's data"* (§20.3's example (a)), which my numbers confirm: adding
`mask` cost 273 bytes of re-emitted directory for 4 bytes of new payload.

**Append that adds tiles to an existing layer.** Adds the old index region of that
layer to the above. §20.3 example (b).

**Append that supersedes (gen 3).** Adds the old index region *and* the superseded
payloads: 84 + 48 = 132 here. Retained tiles do not move.

**Directory-only commit** (§20.3 example (c) — clearing a slab declaration,
renaming a layer, changing a fill on a layer with no padding position and no pad
bit). Slack = old directory + old pad + old trailer, and nothing else.

**In-place update.** *There is no such shape.* `[R-LIF-01]` freezes [0, F)
absolutely: *"a writer MUST NOT modify them, and every conforming mutation of a
file is either a commit (§9.2) or a whole-file rewrite under a new file_id."* The
only bytes a writer ever overwrites are bytes **≥ F**, which are outside every
committed state and are therefore not slack either (slack is defined against the
live state, and `[R-CNT-21]`'s partial total is *"F less the bytes claimed"*, so
the accounting universe is [0, F)).

**Rewrite / compaction.** The output carries **no** input slack: §20.5, *"A
compactor's output contains only the structures reachable from the input's live
trailer … so slack is never carried."* The output still *has* slack — its own
pre-trailer pad, and any alignment gaps its A or A_slab declarations force — but
that is new, not carried. Compaction is *"the only operation that reclaims
slack"*; truncation past F and recovery to an earlier boundary shorten the file
without reclaiming any.

**Abandoned partial write.** Produces bytes past the live F. These are neither
claimed nor slack — the file is nonconforming (F17: committed_file_length ≠
transport size; usually F8 as well), so no live state exists to measure them
against. `[R-LIF-04]` requires the next writer to truncate to F before step 1 or
overwrite from F and truncate no later than step 6, so they never survive into a
committed state.

**Who counts.** A verifier, not a reader: §5.2, *"a verifier MUST report the total
number of slack bytes"*, and §9.7's walk is the mechanism. A reader is never
obliged to walk anything but the live state, and `[R-CNT-21]` forbids
interpreting slack at all. Where the walk does not complete — a scope-level
rejection or a `[R-CNF-11]` stop-at-first-violation — the total is reported as
**partial**, is an upper bound, and the verifier must name what stopped it.

**What slack may contain.** Anything. *"Slack has no internal structure this
specification defines, its content is unconstrained, and no conformance
requirement applies to it."* `[R-CNT-03]` advises zeroing gaps and the pad; my
writer does, and Appendix G item 3 turns that advice into a requirement for the
reproducible profile. §21.6 registers slack as a defined non-violation, and
§23.1/§22.3 record the privacy and integrity consequences (superseded bytes are
readable with a hex editor; corruption confined to slack is invisible to reader
and verifier alike).

---

## 4. Torn-write recovery — five crash points

All against the generation-3 commit above, starting from a committed generation 2
at F₂ = 960 and ending at F₃ = 1472.

**P1 — crash after the new payload lands, before the index.** Physical length
1008. The final 64 bytes are [944, 1008): the tail of trail₂ followed by payload.
Magic check at 944 fails → reject-file (F8), and F17 is also unsatisfiable.
*Next reader:* reports the file torn and **MUST NOT scan backward**
(`[R-LIF-05]`). *Next updater:* `[R-LIF-04]` — trailer validation at the physical
end fails, so *"the writer MUST NOT append"*; recovery is a deliberate separate
operation. *Conforming in the meantime:* **no**. *Recovery:* §9.6 probes backward
at 64-aligned offsets; the largest o with o + 64 ≤ 1008 is 960 (magic absent —
that is my new payload), then 896, where trail₂'s magic sits, its CRC verifies,
and committed_file_length = 960 = 896 + 64. Truncate to 960 → generation 2
restored exactly, then re-verified whole per `[R-LIF-06]`.

**P2 — crash after the directory lands, before the pad/trailer.** Physical 1365.
Same analysis; the probe walks down from 1280 through my directory bytes (no
magic) to 896. Same recovery.

**P3 — crash mid-trailer.** Physical anywhere in (1408, 1472). Either the last 64
bytes are not magic-aligned (reject at F8), or, if the physical length landed on
1472 with the trailer's tail unwritten, the trailer CRC over [0,60) fails (F14).
Either way reject-file, and recovery lands on 896.

**P4 — the trailer lands but steps 1–3 were not durable** (a weaker barrier than
step 4 assumes). The trailer validates: magic, CRC, F = 1472 = physical size,
dir_offset 1092, dir_length 273 within bounds. The reader then fetches
[1092, 1365) and the directory CRC fails → reject-file (F20). This is the case
§9.2's Note names: *"safety degrades from 'torn commits are invisible' to 'torn
commits are detected'."* Recovery is the interesting part: §9.6 finds the
generation-3 trailer first, whole-file re-verification **fails**, so *"the tool
continues the probe past it, and MUST report the candidate it settled on and how
many it rejected"* — it settles on 896 and reports one rejection. That clause is
load-bearing and I am glad it is there; without it a recovery tool would truncate
to a candidate that is not a commit state.

**P5 — residue: the commit fully lands but the physical file is longer than F.**
Reached by taking `[R-LIF-04]`'s second option (overwrite from F, truncate no
later than step 6) against a physically longer file and crashing between the
trailer write and the truncate. The final 64 bytes are stale, so a reader rejects
(F8/F17) even though a complete, valid trailer sits inside the file. §9.5's Note
owns this state precisely: *"Residue past a completed commit carries no register
row of its own. A reader meets it as a trailer that fails its gates … What the
residue violates is `[R-LIF-04]`'s writer obligation to truncate or overwrite."*
Recovery finds the buried trailer at F′ − 64 (committed_file_length = F′ =
o + 64) and truncates to it, so the commit is not lost.

I looked for a crash point at which the file is *conforming* but denotes neither
generation, and there is none: the trailer's CRC covers all 60 preceding bytes, so
a partial trailer is never valid; and a valid trailer at the physical end whose
chain verifies **is** a committed state by construction. The append-only design
earns its keep here. The one asymmetry worth stating for implementers: option 1 of
`[R-LIF-04]` (truncate to F first) has no window in which a landed commit is
invisible; option 2 does, though it is recoverable. The document does not claim
the options are equally safe, so this is an observation about deployment, not a
defect.

---

## 5. Byte-divergence catalogue

Given identical input arrays and identical stated options, here is every way two
conforming writers may legitimately produce different bytes, checked item by item
against Appendix G.

| # | Degree of freedom | Licensed by | Closed by Appendix G? |
|---|---|---|---|
| 1 | Placement and order of tiles, index regions, record extents | `[R-SLB-05]`, `[R-LIF-02]` step 2 | **Yes** — item 3's total emission order |
| 2 | Content of alignment gaps and the pre-trailer pad | `[R-CNT-03]` (SHOULD only) | **Yes** — item 3, *"every byte of every such gap is zero"* |
| 3 | Extent of gaps (a writer may leave arbitrary space) | `[R-SLB-05]` | **Yes** — item 3, *"Each structure begins where the previous one ended"* |
| 4 | `file_id` | §9.3 (advice only) | **Yes** — item 2's hash derivation |
| 5 | Encoder output for codecs 2–4 (block/match/table choices, deflate's unused final-byte bits, zstd's optional Frame_Content_Size) | `[R-CNF-05]`; §17.2's Note | **Yes** — item 1 pins implementation + version + settings, and says byte-identity *across* implementations is unattainable |
| 6 | Record and sub-record order in the directory | `[R-CNT-14]` | **Partly** — item 3 fixes an order, but see finding writer-04 |
| 7 | Whether an all-fill tile is stored or sentinelled | nothing requires either | **Yes** — item 6 |
| 8 | The fill recorded when the caller chooses none | `[R-TYP-10]` (SHOULD) | **Yes** — item 7, and item 7 correctly notes it reaches item 6 too |
| 9 | Number of generations | §9 constrains none | **Yes** — item 4 |
| 10 | Declaring A / S / A_slab | §16 leaves to the writer | **Yes** — item 5 |
| 11 | `version_minor`, `flags` | `[R-CNT-26]` (SHOULD) | **Yes** — item 8 |
| 12 | JSON serialization of user metadata (number formatting, whitespace, escaping), and its storage encoding | `[R-MTA-05]` explicitly disclaims cross-writer identity | **Yes** — item 9 |
| 13 | Unicode normalization of names | `[R-ENC-14]` (SHOULD) | **Yes** — item 10, with the right consequence (a different `inline_length` and `dir_length`) |
| 14 | Emitting `[R-IDX-05]`'s all-sentinel constant vs computing it | `[R-IDX-05]` | **N/A** — the constant *is* the computed value; no divergence |
| 15 | Tiling, layout, codec/filter selection | — | **Not closed, and correctly so** — item 2's rationale names these as inputs: *"two files carrying the same arrays can legitimately differ in tiling, layout, and codec"* |
| 16 | Deduplicating two identical tiles onto one extent | — | **Forbidden**, not a freedom: `[R-CNT-13]` — *"no two extent slots and no two structures overlap"* |
| 17 | Pre-trailer pad length | — | **Forbidden**: `[R-LIF-02]` step 5 pins it to the next 64-byte boundary. A longer pad is a *conforming file* (`[R-CNT-05]`) that no conforming writer emits — `[R-CNF-02]`'s third sentence assigns this cleanly to actor conduct |

I could classify every divergence I found as either legitimate-and-closed,
legitimate-and-deliberately-open (item 15), or forbidden. Item 6 is the one where
the profile's own machinery does not do what it claims; that is finding
writer-04.

I also checked Appendix G's closing inventory against the numbered list and it is
honest: gap content, gap extent, record order, default fill, the all-fill
sentinel, single generation, alignment/slab, `version_minor`, derived `file_id`,
producer pinning. Nothing in that paragraph is claimed that the items do not
attempt.

---

## 6. Findings

### writer-01 (CONTRADICTION) — "an unassigned encoding is no violation" over-reaches to the reserved range

**Location:** §21.5 preamble; Appendix H (verifier checklist); against §21.5 row
R1 and `[R-EXT-03]`.

**Quoted, Appendix H:**

> a user-metadata record at an unassigned encoding is no violation and no bar, and
> is instead reported: owning scope, encoding value, stored extent length
> (`[R-MTA-10]`)

**Quoted, §21.5 preamble:**

> every way its document can be unreadable takes this outcome, whatever the
> containing scope — as a violation in the rows below, except at an unassigned
> encoding, where no document rule attaches and §21.6 records the defined
> non-violation (`[R-MTA-10]`)

**Quoted, §21.5 row R1:**

> A user-metadata record declares a document encoding of 0, or a reserved-range
> value (3-0x7F)

**The problem.** §10.2 partitions the metadata-encoding space into assigned (1, 2),
reserved (3–0x7F) and experimental (≥ 0x80). "Unassigned" therefore covers both
the reserved *and* the experimental range, and `[R-MTA-10]` uses the word in
exactly that broad sense (*"Under an unassigned encoding this specification defines
no decoding, and for an experimental value §10.3 lets…"*). But §21.6's
non-violation table records only the **experimental** case (*"A user-metadata
record declares an experimental-range (≥ 0x80) document encoding"*), while R1
registers the **reserved** case as a violation, on `[R-EXT-03]`'s ground that *"a
value from a reserved range MUST NOT be emitted at all before this specification
assigns it"*. So a reserved-range encoding is simultaneously "an unassigned
encoding" (hence, per the two quotes above, no violation and no bar to
certification) and register row R1 (hence a violation that makes the file
nonconforming).

**Permitted readings.** (a) Take the two quotes at face value: a verifier meeting
encoding 0x40 certifies the file, reporting the ignored record. (b) Read the
"unassigned encoding" carve-out as scoped to the *document's content* — at an
unassigned encoding there is no document rule to violate — leaving the *encoding
byte's own value* to be judged by `[R-MTA-03]`/`[R-EXT-03]`, which makes a
reserved value a violation.

**Which I picked, and why.** (b). Three things decide it. §21.5's very next
sentence is *"Every row here is a violation all the same"*, which covers R1
without qualification. `[R-MTA-10]` itself is carefully hedged — it says
conformance *"is decided by the structural checks that precede the document alone:
… the encoding byte's own value set (`[R-MTA-03]`)"*, and its certification clause
is guarded by *"in an otherwise conforming file"*. And §17.4's parallel sentence
carries the same guard: *"an unassigned document encoding **in a conforming file**
is not a violation"*. Appendix H is non-normative and disclaims itself
(*"each entry's authority is the requirement or section cited, never this
summary"*).

**What an implementer does wrong without it.** A verifier written from §21.5's
preamble or Appendix H certifies a file carrying metadata encoding 3–0x7F, which
R1, `[R-EXT-03]` and §10.3 make nonconforming. That is a wrong *verdict*, not a
wrong byte.

**Related, same family, folded in here rather than reported separately:** rows F27
and L48 (`[R-MTA-05]` member ordering) carry no "under an assigned encoding"
qualifier, though R3 and R4 both carry one. `[R-MTA-10]` supplies it globally, and
§21.1's *"where a row and the rule it cites diverge, the rule governs"* resolves
it, so it is not independently reportable — but it is the same propagation seam.

**Byte-level: no.** The normative apparatus decides it twice over — §21.5's own
next sentence and `[R-MTA-10]`'s guarded wording — and the over-reaching statement
in Appendix H sits in text the appendix declares non-authoritative. Two competent
verifiers reading the whole document agree.

---

### writer-02 (AMBIGUITY) — §20.3's declaration-freeze rests on a claim I can falsify

**Location:** §20.3 step 4, `[R-WRT-04]`.

**Quoted:**

> A commit MUST NOT change a layer's declarations in a way that alters, for any
> tile that layer stores, what §14 fixes for its stored bytes or how they decode —
> the set of padding positions (§11.3) and the content `[R-SER-05]` fixes there,
> the decoded size, the byte offset of any sample within the decoded tile image, or
> the codec and filter that produced the stored bytes. **Every such change makes
> each stored tile it reaches nonconforming**, and re-emitting those tiles would
> strand the originals as slack

**The problem.** The bolded justification is what tells an implementer how to read
the prohibition, and it is false in at least three ways.

*Witness 1 — filter at stride 1.* `[R-COD-10]`: *"The shuffle stride s is the
channel's element size for a planar tile and the sample stride Q for an
interleaved tile … for a packed boolean plane s = 1 and the filter is the
identity."* For an interleaved layer with a single uint8 channel, Q = 1, so
n = L/1 = L and byte i of group j lands at i·n + j = j — the identity. Changing
that layer's declared filter from 1 to 2 alters *"the codec and filter that
produced the stored bytes"* by the prohibition's letter, yet makes no stored tile
nonconforming: every tile still decodes to precisely the image it decoded to
before, with the same padding content, the same bool bytes and the same decoded
size. The same holds for any planar plane of a 1-byte type and for every packed
bool plane.

*Witness 2 — a shrink whose new padding already holds fill.* A layer with one
uint8 channel, fill 0x00, dimension E = 4, T = 4: one tile, no padding positions,
stored bytes `0A 0B 0C 00`. Shrink E to 3. In-tile ordinal 3 becomes a padding
position and must carry fill — it already carries 0x00. The change alters *"the
set of padding positions"*, so it is prohibited; but no stored tile becomes
nonconforming, and the resulting file is conforming.

*Witness 3 — the paragraph's own exception.* Two sentences later it says *"an
extent MAY always **grow**"* — and growing an extent alters the set of padding
positions of every stored edge tile. So the enumeration already has one stated
exception, which is direct evidence it is not meant as a literal list of
prohibited alterations.

**Permitted readings.** (a) *Literal:* the four enumerated declaration properties
must not change at all for a layer that stores tiles, growth excepted. (b)
*Effect-based:* the operative test is the preamble — *"in a way that alters … what
§14 fixes for its stored bytes or how they decode"* — so a change whose effect on
every stored tile is nil (filter 1 ↔ 2 at stride 1) is permitted, and the
enumeration is a list of the *ways* a change can have that effect.

**Which I picked, and why.** (b), because the preamble is the sentence that carries
"MUST NOT" and the enumeration is attached to it by an em-dash as elaboration, and
because reading (a) would also forbid growth, which the same paragraph explicitly
allows. But (a) is defensible on the plain text and I would not be confident
telling another implementer they were wrong to take it.

**What an implementer does wrong without it.** Under (b) my updater emits a
directory-only commit flipping `filter` 1 → 2 on a stride-1 layer; under (a) it
refuses and forces a new layer or a whole-file rewrite. It also matters for §21.7's
completeness accounting: §21.7 omits obligations from the register *"because a
single file exhibits no witness of their violation"* and lists five of them
(`[R-LIF-01]`, `[R-LIF-03]`, `[R-GEO-06]`, `[R-SER-01]`, `[R-CNT-13]`'s embedded
offsets, `[R-ENC-06]`). `[R-WRT-04]`'s prohibition is not on that list precisely
because the bolded claim asserts it always has a single-file witness — and where
the claim fails, it has none, and it is accounted for nowhere.

**Byte-level: no.** Both readings leave the file the permissive updater emits
**conforming**: the layer declares filter 2, the stored bytes shuffle-at-stride-1
to the correct image, and no register row fires. So no verifier's accept/reject
verdict forks, and the set of conforming byte sequences a writer may emit is
identical under either reading (a creator could always emit that file from
scratch). What forks is one updater's permission to reach it by a commit.

---

### writer-03 (OBSERVATION) — `[R-SLB-04]`'s trigger under-covers a geometry growth that re-partitions slab runs

**Location:** §16.2, `[R-SLB-04]`; with §16.2's `[R-SLB-02]` and §20.3 step 4.

**Quoted:**

> A writer or updater whose commit changes the stored-tile set or the byte
> placement of any run of a slab-declared layer MUST either re-establish the
> invariants for every such run — or clear the declaration in the new generation;
> carrying a stale declaration forward is a validity error at layer scope

**The problem.** A commit can break `[R-SLB-03]`'s invariants without changing the
stored-tile set and without moving a single byte, by changing the **run
partition**. `[R-SLB-02]` defines runs positionally — *"Run r of a block starts at
ordinal block_start + r·S"* — and `[R-GEO-06]` makes disk ordinals a function of
the grid counts, so growing a dimension extent across a grid boundary renumbers
every tile and re-partitions every run.

**Worked witness.** Interleaved layer, one uint8 channel (P = 1, decoded size 1),
codec 1, dims y(E = 2, T = 1) and x(E = 2, T = 1) → G = (2, 2), N = 4,
entry_count = 4. Declare S = 2, A_slab = 4096. All four tiles stored, packed:

```
ordinal 0 = tile(0,0) @ 4096   run [0,2): first stored 4096, 4096 mod 4096 = 0  ✓ packed ✓
ordinal 1 = tile(0,1) @ 4097
ordinal 2 = tile(1,0) @ 8192   run [2,4): first stored 8192, 8192 mod 4096 = 0  ✓ packed ✓
ordinal 3 = tile(1,1) @ 8193
```

Conforming. Now commit a growth of x's extent from 2 to 3. G_x = 3, N = 6,
entry_count = 6, and s = t_y·G_x + t_x renumbers:

```
ordinal 0 = tile(0,0) @ 4096   run [0,2): first stored 4096  ✓
ordinal 1 = tile(0,1) @ 4097
ordinal 2 = tile(0,2)  sentinel (new)      run [2,4): first stored 8192 ✓ (sentinel transparent)
ordinal 3 = tile(1,0) @ 8192
ordinal 4 = tile(1,1) @ 8193               run [4,6): first stored 8193
ordinal 5 = tile(1,2)  sentinel (new)                 8193 mod 4096 = 1   ✗  L42
```

The commit changed the layer record and re-emitted the index region. It changed
**no tile's storedness and no tile's offset**. Whether `[R-SLB-04]`'s trigger fires
depends on what *"the byte placement of any run"* denotes: the offsets of the
tiles in a run (unchanged — trigger silent), or the byte range a run covers
(changed for run [2,4), which lost tile(1,1) — trigger fires).

**Why this is an OBSERVATION and not an ambiguity with teeth.** It is decidable,
just expensively: `[R-SLB-03]` binds *"when declared, for every run"*
unconditionally, L42 registers the failure, and `[R-CNF-05]`/`[R-CNF-06]` require
an updater to emit only conforming files. So a conforming updater must clear the
declaration or re-emit tile(1,1) at an aligned offset regardless of which reading
of `[R-SLB-04]` it takes. The cost of the under-coverage is that an implementer
who reads `[R-SLB-04]` as its own trigger-and-obligation pair — which is how it is
written, and which §20.3 step 4 reinforces with *"a slab declaration is
re-established or cleared (`[R-SLB-04]`)"* attached to a step about tile writes —
will ship an updater that emits a nonconforming file on a pure extent growth. The
same trap exists for planar layers and is worse there, since `block_start = c·N`
moves every channel block's runs when N changes.

**Byte-level: no.** The updater that keeps the declaration emits a file that a
verifier must report nonconforming (L42) under either reading, and the updater
that clears it emits a conforming one under either reading. No verdict forks, and
the set of byte sequences a *conforming* updater may emit is unchanged, because
`[R-CNF-05]` backstops the narrow reading.

---

### writer-04 (OBSERVATION) — Appendix G item 3's tie-break is circular for the only records that can exercise it

**Location:** Appendix G, item 3 (and item 2's all-zero-digest clause).

**Quoted:**

> then any record extents in ascending record order … Records and a layer record's
> sub-records alike are ordered by type, and within a type by their encoded bytes
> compared lexicographically, save that type 0x0001 ties by layer name — an order a
> reader can derive, which a creation order is not.

**The problem.** A record's "encoded bytes" are its 24-byte header — type, flags,
`inline_length`, `extent_offset`, `extent_length` (§7.2) — followed by its inline
payload. `extent_offset` is fixed by the placement order, and the placement order
is *"ascending record order"*, which is what this comparison defines. Where two
records of one type agree on flags and `inline_length`, the lexicographic
comparison reaches `extent_offset` first and the rule closes on itself.

Concretely: two top-level records of type 0x8001, flags 0x0000, `inline_length` 0,
each with a 10-byte extent. Their encoded bytes differ **only** in `extent_offset`.
Place R's extent first and R sorts before S — self-consistent. Place S's first and
S sorts before R — also self-consistent. Two fixed points, two different files,
both satisfying the profile from identical input. Item 3's claim to be *"A total
emission order"* fails, and so does the parenthetical *"an order a reader can
derive"*: a reader can derive the order from the finished file under either fixed
point, which is exactly the problem — derivability does not imply uniqueness.

The `save that type 0x0001 ties by layer name` clause shows the author saw the
circularity for layer records (whose `extent_offset` addresses the index region)
and patched it there. The unpatched cases are the only ones that reach the general
clause: `[R-CNT-14]` caps type 0x0002 at one per top-level sequence and one per
layer record, and L26 keeps type 0x0001 out of sub-record sequences, so
`within a type by their encoded bytes` is *never* exercised for a registered type.
It is exercised only by unassigned types — which §10.3 forbids a writer to publish
as a matter of conduct, but which `[R-CNF-02]` and §21.6 make conforming as bytes.

**Also falsifiable in the same appendix, item 2:** *"with any other fixed nonzero
value substituted in the measure-zero case that they are all zero"*. "Any other
fixed nonzero value" is a per-writer choice, so two profile-following writers
diverge on that input. Measure 2⁻⁶⁴, but the profile's whole purpose is to leave
nothing to the writer, and this leaves something.

**What an implementer does wrong without it.** Two implementations of the profile
disagree on the bytes of a file carrying two same-type ancillary records, and the
disagreement is invisible until they compare digests — the one failure mode a
reproducible-writer profile exists to eliminate.

**Byte-level: no.** Appendix G is non-normative and says so of itself: *"It adds no
requirement to any actor: a writer ignoring it is fully conforming."* Both fixed
points produce conforming files, and no reader or verifier verdict turns on which
one a writer picked.

---

## 7. Things I checked that turned out to be sound

Recording these so a later round need not re-derive them, and because a walk that
only lists complaints misreports what it found.

- **§9.7's coverage walk vs `[R-CNT-02]`'s claimant list.** The walk now claims
  the front block and the trailer explicitly and notes that the [16, F − 64) bound
  on every other claimant keeps them disjoint. My generation-3 file partitions
  exactly (678 claimed + 794 slack = 1472) with no double claim and no orphan.
- **`[R-IDX-03]`'s structural/non-structural split.** An entry rejected on a
  structural ground contributes no extent to the coverage walk, to the overlap
  rows, or to slab run continuity; an entry whose *only* defect is a failing tile
  CRC keeps its extent everywhere. §15.3's preamble, §16.2's `[R-SLB-03]`, §9.7 and
  L41's parenthetical all say the same thing in the same words. I looked for a
  fourth restatement that had drifted and did not find one.
- **§7.4's new worked byte example.** Every offset in the 81-byte payload is
  consistent (0/4/5/7/9/11/19/27/35/36/38/40/48/56/63/68/69/77), the totals
  reconcile (4 + 34 + 18 + 12 + 13 = 81), the channel entry is byte-for-byte
  §12.3's, and both CRCs are correct: CRC-32C over four sentinel entries is
  0x80A34955 and CRC-32C over `55 49 A3 80` is 0xC4EE982E. I computed both.
- **§4.5's check vector** (0xE3069283 / 0x00000000), **§15.4's all-sentinel
  segment constant** (0xEECB3BB2), and **Appendix A's trailer CRC** (0xE00938D2
  over the 60 bytes shown) all reproduce.
- **§21.8's arithmetic.** I parsed the four register tables out of the document:
  36 + 49 + 26 + 10 = **121 rows**, and counting each cell as one instance when it
  reads `—` and as its semicolon-separated members otherwise gives 56 + 110 + 54 +
  44 = **264 instances**. §21.8 states *"121 conditions over 264 instances"*. Exact.
  T3 and T14 both enumerate six instances (three decoded-size shapes × longer /
  shorter), and F33 carries five claimant kinds to F7's four — F7's gap cannot
  contain the directory region, which bounds it. Consistent.
- **Detector/Detected consistency.** Every one of the 121 rows has Detector ∈
  {reader, verifier}, and Detector = verifier holds if and only if Detected =
  certification. §21.1's tier vocabulary (open / layer access / tile use / extent
  use / certification) matches §19.2's four bullets exactly.
- **Requirement identifier space.** Nineteen prefixes, contiguous numbering in
  every one, with exactly two apparent gaps, both explained in place: `[R-SER-04]`
  is withdrawn and §14.4 says so, and `[R-ENC-100]` appears only as §2.2's
  illustration of numbers above 99.
- **§21.7's citation of `[R-CNT-13]`** for the MU = 0 embedded-offsets prohibition
  is correct — that prohibition really does live in `[R-CNT-13]`'s paragraph in
  §7.2, not in `[R-CNT-15]` where a reader might expect it.
- **Every other worked example**: §11.2 (G = (4,8), N = 32, P = 65,536), §11.4
  (ordinals 8, 10, 11,452, 74), §12.1 (bfloat16 1.0 = 0x3F80), §14.2 (Q = 3,
  decoded 18, bytes [15,18); Q = 5, decoded 30, bytes [25,30)), §14.3 (`55 01` /
  `55 FD`), §14.5 (32-byte edge tile, values 1–15 = `CD AB`), §15.4 (16 segments,
  339,180, [19,660,800 … 20,000,064)), §16.2 (four runs of eight), §17.3 (the
  twelve shuffled bytes), §20.3 (32·20 + 4 = 644), §21.9's note (256 KiB at 2³²,
  4 MiB at 2³⁶), Appendix A (all 128 bytes). All correct.
- **No undetermined byte in the creation path.** I enumerated all 512 bytes of my
  generation-1 file and every one is either pinned by a citable requirement or
  explicitly a writer's choice. That is the strongest positive statement I can
  make from this charter, and I make it deliberately.

## 8. Confidence

**Medium-high.** I built a conforming file, appended twice, and never had to
invent a rule. The four findings are all off the byte path: one is a
propagation slip in a restatement that the governing rule corrects, one is a
false justification attached to a real prohibition, one is a writer trap in a
trigger that a general rule backstops, and one is a hole in a non-normative
profile. I flagged **none** of them byte-level, and I want that to read as a
considered verdict rather than timidity: I went looking specifically for a place
where two competent writers put different bytes on disk unlicensed, and for a
place where two verifiers disagree on accept/reject, and in the core container and
array model I could not construct either.
