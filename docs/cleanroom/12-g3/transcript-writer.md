# Cleanroom round 12 — Writer/updater implementer transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 3,982 lines, in five `Read` calls). I opened no other file in the
repository — no `docs/`, no ADRs, no `PLAN.md`, `AGENTS.md`, `README.md`,
no `conformance/`, no `spec/registry.json`, no git history, no network.

I ran `wc -l` and `grep` against that one file, and I ran four Python
programs I wrote myself, which read no repository files:

- a CRC-32C implementation, checked against §4.5's check vector
  (`CRC-32C("123456789") = 0xE3069283`, `CRC-32C("") = 0x00000000`) and
  against §15.4's all-sentinel-segment constant `0xEECB3BB2`;
- a full creation build of a non-trivial file (written to my own
  scratchpad as `demo.tarn`);
- a full append (generation 2) onto that file;
- a mechanical parse of §21.2–§21.5's register tables to recount rows
  and instances.

Everything below is derived from the document text plus that arithmetic.
Where I used prior knowledge of other formats it was only to generate a
suspicion; every conclusion is settled against this document's words.

---

## 0. Order of work

I read the six named sections first (front matter, §4.7, §9.7, §13.1,
§20.3, Appendix G) and found nothing wrong with any of them in
isolation. Then I did what the charter asked and stopped narrating them:
I built a file end to end, appended to it, walked the flag matrix, the
slack shapes and four crash points, and finally worked Appendix G item
by item against the divergence catalogue I had accumulated while
building. Six of my eight findings are outside the six changed sections;
two are inside Appendix G, and they are of the kind the charter
explicitly asked for (a degree of freedom the profile leaves open, and a
claim in the profile I can falsify).

---

## 1. Creation: the byte-layout walk

### 1.1 What I chose, and what the document chose for me

Design of the file I built (`demo.tarn`, generation 1):

| Thing | Value | Fixed by |
|---|---|---|
| layer name | `img` | me (input) |
| layout | 1 = interleaved | me (input); §7.4 / `[R-SER-06]` fixes the value set |
| dims | `y` E=5 T=4, `x` E=5 T=4 | me (input) |
| channels | `r` uint8 fill `00`; `v` uint16 fill `CD AB` (0xABCD) | me (input) |
| linearization | 1 | **document**: `[R-GEO-05]` — writers MUST NOT emit any other value |
| codec / filter | 1 / 1 | me (input); value sets `[R-COD-03]`, `[R-COD-09]` |
| A / S / A_slab | 0 / 0 / 0 | me; §16 + `[R-CNT-16]` (mutually exclusive), `[R-CNT-23]` (A_slab=0 when S=0) |
| index_encoding | 1 | **document**: only value defined (§7.4, §15.1) |
| entry_count | 4 | **document**: `[R-GEO-03]` + `[R-CNT-17]` — N for interleaved |
| layer record flags | `03 00` (MU=1, PE=1) | **document**: §7.3's registry table + `[R-CNT-22]` |
| user-metadata record flags | `02 00` (MU=0, PE=1) | **document**: §7.3 |
| version_major / minor | 1 / 0 | **document**: §6.2 table; `[R-CNT-26]` SHOULD floor |
| flags | 0 | **document**: `[R-CNT-08]` — MUST write 0 under this text |
| generation | 1 | **document**: §9.2 creation path |
| file_id | `0x9E3779B97F4A7C15` | me; only constraint is ≠ 0 (`[R-CNT-06]`), SHOULD be random (`[R-LIF-03]`) |

Geometry, derived and checked: G = (⌈5/4⌉, ⌈5/4⌉) = (2, 2); N = 4; P = 16;
Q = Σ Bᵢ = 1 + 2 = 3; decoded size = P·Q = 48 bytes per tile
(§14.2's table row "interleaved | P · Q"). Addressed-tile count = N = 4
because the layer is interleaved (`[R-GEO-03]`), so entry_count = 4 and
the index region is 4·20 + ⌈4/2¹⁶⌉·4 = **84** bytes (`[R-CNT-17]`).

### 1.2 Placement — how much freedom did I actually have?

Less than I expected, and the document is what narrowed it. Three rules
compose:

1. §9.2 creation path: "the writer first emits the front signature block
   (§6.1) … then performs steps 2–6, writing beginning at offset 16".
   So the first structure starts at 16, not before.
2. `[R-CNT-05]`: "Writers MUST place the directory so that no structure
   lies between its end and the trailer." Combined with `[R-CNT-06]`'s
   `dir_offset + dir_length ≤ F − 64`, this forces *every* non-trailer
   structure into `[16, dir_offset]`. The macro order
   front → structures → directory → pad → trailer is therefore not a
   writer's choice at all.
3. Within `[16, dir_offset)` placement is free: `[R-SLB-05]` — "its
   stored tiles MAY occupy any non-overlapping byte positions, in any
   order".

I adopted Appendix G item 3's total order (tiles in disk-ordinal order,
then the index region, then record extents, then the directory) so the
file would be a profile file, and got zero slack in generation 1.

### 1.3 The emitted bytes

```
[0, 16)     89 54 41 52 4E 0D 0A 1A 00×8      front signature block  (§6.1)
[16, 64)    tile s=0   len 48   crc 0x537ABCC7
[64, 112)   tile s=1   len 48   crc 0xD2C14F26
[112, 160)  tile s=2   len 48   crc 0x08B2F629
            tile s=3   SENTINEL — no bytes
[160, 244)  tile-index region, 84 bytes = 4×20 entries + one 4-byte segment CRC
              segment CRC[0] = 0x8C4A53DC ; crc_of_crc_array = 0x0279C2ED
[244, 295)  user-metadata extent: 47-byte JSON document + 4-byte CRC-32C
[295, 448)  directory region, 153 bytes = rec(img) 124 + rec(meta) 25 + CRC 4
              directory CRC = 0x4236E80C
[448, 448)  pre-trailer pad — ZERO bytes (dir ends 64-aligned)
[448, 512)  trailer; F = 512, F mod 64 = 0; trailer CRC = 0xF7E43053
slack: 0
```

Tile 3 (tile coordinates (1,1)) covers y 4..7 × x 4..7: one real position
(4,4) and fifteen padding positions. I set sample (4,4) equal to fill, so
under `[R-SER-05]` the whole decoded tile image is 16 copies of
`00 CD AB` — i.e. an all-fill tile — and Appendix G item 6 ("the sentinel
for every all-fill tile") makes it a sentinel. I verified in code that the
constructed tile image is byte-identical to the all-fill image before
discarding it. That is the one place where a *non*-profile writer has a
real choice: it may store the tile instead, and both files are conforming
(`[R-CNF-05]`). Catalogued below as divergence D10.

Entry bytes actually emitted (region byte 60 onward):

```
000224  FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00
```

which is §15.2's `FF ×16 00 ×4` exactly.

Tiles 1 and 2 are the interesting content check. Tile 1 covers x 4..7 with
only x=4 real, so twelve of its sixteen positions are padding and
`[R-SER-05]` fixes each to `00 CD AB` — "at every padding position, a
writer MUST encode, for each channel the position carries, that channel's
fill value". I emitted them that way. Note the consequence for byte
reproducibility: padding content is *not* a writer's choice, so it is one
of the things Appendix G correctly does not have to list.

Layer record inline payload, 100 bytes, packed in §7.4 table order with no
padding (`[R-CNT-18]`: "fields are packed in table order with no alignment
or padding between them"):

```
03 69 6D 67                     name "img" (u8 len 3)
01                              layout = interleaved
01 00                           linearization = 1
01 00                           codec = 1 (none)
01 00                           filter = 1 (none)
00×8 00×8 00×8                  A = 0, S = 0, A_slab = 0
02                              rank d = 2
02 00                           channel count C = 2
01 79 | 05 00×7 | 04 00×7       dim "y": E=5, T=4
01 78 | 05 00×7 | 04 00×7       dim "x": E=5, T=4
01 72 | 06 00 | 01 00           channel "r": uint8, fill len 1, fill 0x00
01 76 | 07 00 | 02 CD AB        channel "v": uint16, fill len 2, fill 0xABCD
01                              index_encoding = 1
04 00×7                         entry_count = 4
ED C2 79 02                     crc_of_crc_array = 0x0279C2ED
                                (no sub-records)
```

The channel-entry encoding matches §12.3's worked example form exactly
(`04 74 65 6D 70 0C 00 04 00 00 C0 7F`), which was a useful cross-check
that I had the fill length prefix in the right place: `[R-CNT-23]` — "fill
length equals the type's element size … so fill parses without type
knowledge and validates with it".

**Cross-check against Appendix A.** I rebuilt Appendix A's 128-byte
minimal file's trailer independently and computed its CRC: I get
`0xE00938D2`, exactly the value the appendix states at `[124, 128)`. The
minimal-file example is arithmetically correct.

### 1.4 Where creation left me guessing

Nowhere, in the end. Every field I had to fill was either input, fixed by
a rule, or explicitly free with the freedom named. The only judgement call
was whether the pre-trailer pad may be zero bytes long, and §6.2 answers
it directly: "a writer that ends its directory on a 64-byte boundary
leaves none".

---

## 2. The append procedure

### 2.1 Adding a layer to the existing file

Generation 2 adds layer `msk`: **planar**, one **bool** channel `m` with
fill `0x00`, same geometry (5,5)/(4,4). This exercises the packed-plane
path and the slab path at once.

- Planar addressed-tile count = C·N = 1·4 = 4 (`[R-GEO-03]`).
- Packed bool plane decoded size = ⌈P/8⌉ = ⌈16/8⌉ = **2 bytes**
  (`[R-SER-03]`). P mod 8 = 0, so there are **no pad bits** — §14.3's
  distinction between pad bits and padding positions mattered here: this
  plane has twelve padding *positions* in tile 1 and zero pad *bits*.
- Codec 1, so `[R-COD-04]` forces stored length = 2 for every stored tile.
- Slab declared: S = 2, A_slab = 64. `[R-SLB-02]` partitions the single
  interleaved-style block — here a planar layer with C = 1, so one channel
  block [0, 4) — into runs [0,2) and [2,4).

Emitted:

```
[512, 514)  msk tile s=0   a5 a5   (run 0 first stored tile: 512 mod 64 = 0 ✓)
[514, 516)  msk tile s=1   01 01   (packed: 512 + 2 = 514 ✓)
[516, 576)  SLACK — 60 bytes forced by A_slab on run 1
[576, 578)  msk tile s=2   05 00   (run 1 first stored tile: 576 mod 64 = 0 ✓)
[578, 580)  msk tile s=3   01 00   (packed: 576 + 2 = 578 ✓)
[580, 664)  msk tile-index region, 84 bytes
[664, 934)  directory, 270 bytes = rec(img) 124 + rec(msk) 117 + rec(meta) 25 + CRC 4
[934, 960)  pre-trailer pad, 26 bytes
[960, 1024) trailer, generation = 2, same file_id, F = 1024
```

Live claimants sum to 721 bytes; **slack = 303 bytes**, which decomposes
exactly as 153 (generation 1's directory) + 0 (generation 1's pad) + 64
(generation 1's trailer) + 60 (the slab gap) + 26 (generation 2's pad).
That is §9.7's walk done by hand and it closes.

Write order and durability, from `[R-LIF-02]` and `[R-WRT-04]`:

1. Establish F = 512 by validating the trailer at the physical end
   (`[R-LIF-04]`). Physical length equals F, so no truncate.
2. Perform §19.1's open — the appender is a reader here (`[R-WRT-03]`:
   "the trailer and the full directory always — re-emission (§20.4)
   relies on every directory byte").
3. Validate what the commit touches. `msk` is new, so no existing layer
   is modified; I did *not* have to run §19.3 on `img`, nor `[R-IDX-04]`
   on `img`'s index chain, because I neither modify nor rely on it —
   `[R-WRT-03]`: "Structures the commit neither modifies nor relies on
   impose no further obligation."
4. Write payloads and the new index region, beginning at exactly F = 512.
5. Re-emit the complete directory: `img`'s record byte-identically
   (header, inline payload **and extent slot** — so it still points at
   [160, 244), which the commit does not relocate), the user-metadata
   record byte-identically, plus the new `msk` record. Then the CRC.
6. **Barrier.** Then pad + trailer. **Barrier.**

The **commit point is the completion of step 6's barrier**. Everything
before it is invisible to a conforming reader, because a reader takes the
final 64 physical bytes as its snapshot (`[R-LIF-05]`) and those are not a
valid trailer until the trailer lands. What must be durable before what:
payloads, index regions, record extents and the *entire directory
including its CRC* must be durable before a single byte of the trailer
is. That is the only ordering constraint the format needs, and §9.2's note
states the degradation honestly — with weaker barriers "safety degrades
from 'torn commits are invisible' to 'torn commits are detected'".

One thing the document decides that I would otherwise have guessed wrong:
a commit may **not** re-point its new trailer at the previous
generation's directory even when the directory content is unchanged.
§9.2's note: "A writer that re-points a new trailer at a prior
generation's directory region has left step 3 unperformed." So a no-op
commit still costs a full directory + pad + trailer of slack.

A second: an appender may **not** relocate a live index region it is not
changing. §20.3: "A layer whose record alone changes keeps its extent
slot, pointing at the existing region, as does a layer the commit leaves
untouched (`[R-WRT-05]`); relocating a live index region is compaction's
operation." So renaming a layer cannot be used to tidy its index.

### 2.2 The slab, one commit later

I then worked out what generation 3 would have to do to supersede
`msk` tile s=1. Run 0's invariant (`[R-SLB-03]`) is
`offset(s=0) + length(s=0) = offset(s=1)`. Tile 0 sits at 512 in the
committed prefix and cannot move (`[R-LIF-01]`); the new tile 1 must be
written at ≥ 1024. So re-establishing the run means **appending a fresh
copy of tile 0 as well**, 64-aligned, with the new tile 1 packed behind
it — and tile 0's original two bytes become slack even though tile 0 did
not change. `[R-SLB-04]` states exactly this choice ("re-establish the
invariants for every affected run … or clear the declaration in the new
generation"), and it is a real and non-obvious cost of declaring a slab.
The document told me; I did not have to guess. See finding **writer-06**
for the one hole in that rule's trigger.

### 2.3 Appending to a file whose records I do not all understand

The full matrix. Rows are the record's stored flags; columns are what my
updater is permitted to do. "Registered" means a type §7.3's table lists
(0x0001, 0x0002); "unknown" means any other type value the updater does
not implement.

**Top-level records.**

| Type class | Stored MU | Stored PE | What my updater may do | Authority |
|---|---|---|---|---|
| registered 0x0001 (layer) | — | — | Re-emit byte-identical if retained and unmodified; modify freely if it is the layer I am changing; **never drop**. Registry flags MU=1/PE=1 govern, stored bits are ignored for behaviour. | `[R-WRT-05]`, `[R-CNT-22]`, §20.4 ("No commit therefore removes a layer record") |
| registered 0x0002 (user metadata) | — | — | Re-emit byte-identical, or modify (which means appending a *new* extent and letting the old become slack); **never drop**. | §20.4, §20.3 shape (c) note |
| unknown | 1 | 1 | Retain byte-identical. **No commit is available at all** — as a reader I must reject-file first. | §20.4 MU=1 row; `[R-CNT-15]` |
| unknown | 1 | 0 | Identical to the row above: `[R-CNT-12]` — "a reader or updater encountering it MUST treat the record as PE = 1". Also a verifier-detected violation (F25), but that changes nothing I do. | `[R-CNT-12]`, §20.4 |
| unknown | 0 | 1 | Retain byte-identical, **extent content unmodified**. I may commit anything else. I may not re-encode it (`[R-WRT-08]`) and, as an *appender*, may not relocate its extent — relocation is compaction's alone. | §20.4 MU=0/PE=1 row; `[R-WRT-08]` |
| unknown | 0 | 0 | Retain byte-identical, **or** drop it (extent → slack) — but only in a commit that independently changes the file's layer set or another non-layer top-level record. Adding `msk` qualifies. Superseding a tile does **not**. SHOULD report the loss. | §20.4 MU=0/PE=0 row |

**Layer sub-records** — same four flag combinations, different blast radius:

| Stored MU | Stored PE | Permitted | Authority |
|---|---|---|---|
| 1 | either (PE read as 1) | Retain byte-identical; **that layer** is unmodifiable, every other layer stays editable. I can still add `msk`, and I must still re-emit the blocked layer's record byte-identically into the new directory. | §20.4 MU=1 row; `[R-CNT-18]` (unknown sub-record MU=1 → reject-layer, "never reject-file") |
| 0 | 1 | Retain byte-identical, extent untouched. | §20.4 |
| 0 | 0 | Retain, or drop — only in a commit that independently changes that layer's record, the entry set of its index, or which of its tiles are stored. Superseding a stored tile's *bytes* is explicitly not such a change. | §20.4 |

Two things this matrix taught me that I would have got wrong from
intuition:

- **Implementing a type is not permission to drop it.** §20.4: "both
  registered types carry PE = 1, so neither can be dropped, and
  implementing a record's type confers understanding of it, not
  permission to drop it."
- **Superseding tile bytes is deliberately excluded** from the
  MU=0/PE=0 drop licence, on the reasoning that a supersede "re-places
  that layer's index region … without altering the scope any record
  attaches to". That is a fine distinction and the document draws it
  explicitly rather than leaving it to me.

Two holes I did find in the matrix: findings **writer-05** (mutual
drops) and **writer-07** (a type the updater implements that §7.3 does
not register).

---

## 3. Slack, by commit shape

| Commit shape | Bytes that become slack | Who counts them | Permitted content |
|---|---|---|---|
| **Append (new layer)** | the previous generation's directory, its pad and its trailer; plus any alignment or slab gap the new structures force. Sized by the file's *layer count*, never by any layer's data (§20.3 example (a)). | verifier only (§5.2: "a verifier MUST report the total number of slack bytes"); readers never walk it (`[R-CNT-21]`) | unconstrained. `[R-CNT-03]` advises zeroing and nothing rides on it: "no conformance requirement rides on slack content either way" |
| **In-place update (supersede a tile)** | the superseded payload extent, the layer's whole previous index region, plus the previous directory/pad/trailer. §20.3's worked example: superseding one 100,000-byte tile of a 32-tile layer appends 100,000 + 644 + directory + pad + 64. | same | same |
| **Directory-only change** | only the previous directory, pad and trailer (§20.3 example (c)). | same | same |
| **Rewrite / compaction** | none is *carried*: "A compactor's output contains only the structures reachable from the input's live trailer … so slack is never carried". The output still has its own alignment gaps and pre-trailer pad, which are slack. The *input file* is untouched and persists (`[R-PRV-02]`). | same | same |
| **Abandoned partial write** | **none — these bytes never become slack.** They lie beyond F, so they are not part of any committed state. `[R-LIF-04]` obliges the next writer either to truncate to F before step 1 or to overwrite from F and truncate by step 6, "so that … bytes beyond a committed length never survive into any committed state". | nobody: while they exist the file is *not conforming* (F17), so there is no live state to count against | unconstrained, but they must not survive |

That last row is the one I would have got wrong without §9.5's note,
which is explicit that residue past a completed commit "carries no
register row of its own" and is met by a reader as a trailer that fails
its gates.

The verifier's slack total for my generation-2 file: **303 bytes out of
1024**, and because my walk completed it is an exact total, not a partial
one (`[R-CNT-21]`).

---

## 4. Torn-write recovery — five crash points

I take the generation-2 commit as the one being interrupted (F_1 = 512,
F_2 = 1024).

**Crash A — during step 2 (payloads written, directory not).**
Physical length is, say, 600. Next reader: takes bytes [536, 600) as the
candidate trailer; the trailer magic fails → reject-file, "report the
file torn or invalid and MUST NOT scan backward" (`[R-LIF-05]`).
Next updater: §9.4 — validation of the physical-end trailer fails, "the
file is torn: the writer MUST NOT append", and recovery is a separate
deliberate operation. §9.6's probe starts at the largest 64-aligned o
with o+64 ≤ 600, i.e. o = 536, and walks down; it stops at o = 448, where
the magic verifies, the CRC verifies and committed_file_length = 512 =
o + 64. Truncate to 512, re-verify whole (§9.6), and the file is
generation 1 again, bit-identical to what I built in §1.
**Conforming in the meantime? No** — `[R-CNT-01]` requires the file size
to equal the live trailer's F, and here the final 64 bytes are not a
trailer at all, so there is no live trailer.

**Crash B — after step 4's barrier, before the trailer.** Directory is
durable at [664, 934); physical length 934. Identical analysis: the tail
is directory bytes, magic fails, recovery lands on 448. The complete
generation-2 directory is durable and *unreachable*, which is correct —
nothing addresses it.

**Crash C — mid-trailer.** Suppose 32 of the trailer's 64 bytes are
durable and the physical length is 1024. Two sub-cases, both safe: if
the magic bytes [960, 968) did not land, `[R-CNT-06]`'s first gate fails;
if they did but the interior did not, the trailer CRC fails. Either way
reject-file, and §9.6 recovers to 448. Note the ordering §6.2 fixes —
magic, then CRC, then version gate — means a half-written trailer is
never mistaken for an unimplemented major.

**Crash D — barrier inversion (the trailer lands before the directory).**
This is the case worth spelling out, because the reader's answer and the
recovery tool's answer differ. The physical file is 1024 bytes, the
trailer at [960, 1024) is complete and valid: magic ✓, CRC ✓,
committed_file_length = 1024 = physical size ✓, generation 2 ✓,
file_id ≠ 0 ✓, reserved zero ✓. Every gate in `[R-CNT-06]` passes. The
reader then fetches [664, 934) and the directory CRC fails →
**reject-file** (`[R-CNT-11]`). It cannot fall back to generation 1
because `[R-LIF-05]` forbids scanning backward.
The recovery tool does better. §9.6's probe finds o = 960 first; the
trailer is a valid *candidate*, but "a candidate whose whole-file
re-verification fails was not a commit state, so the tool continues the
probe past it, and MUST report the candidate it settled on and how many
it rejected". It continues down and settles on o = 448.
This is the one place where the format's behaviour is only as good as
its barriers, and §9.2's note says so in as many words. The file is not
conforming in the meantime.

**Crash E — trailer durable, truncate not.** Reachable only when the
physical file was already longer than F_2 (residue from an earlier torn
write that the writer chose to overwrite rather than truncate).
`[R-LIF-04]` puts the truncate "no later than step 6", i.e. inside the
same barrier as the trailer, so on recovery either both or neither are
lost. If the trailer landed and the truncate did not, the physical tail
is stale bytes: reject-file (F8 or F17), and §9.6's probe finds
generation 2 at o = 960 and re-verifies it whole successfully →
truncate to 1024. Generation 2 is recovered, not lost. Correct and
determined.

Across all five, the answers to the charter's three questions are
uniform and the document supplies every one of them: the next reader
sees reject-file; the next updater must not append and must run §9.6
deliberately; and the file is not conforming for as long as the state
lasts.

---

## 5. Byte-divergence catalogue

Two conforming writers, identical input arrays, identical stated options
(tiling, layout, codec, filter, channel and dimension declaration order,
metadata content). Every legitimate way their bytes may differ, and
whether Appendix G closes it.

| # | Degree of freedom | Where the document licenses it | Appendix G |
|---|---|---|---|
| D1 | `file_id` — any nonzero value | §6.2, `[R-LIF-03]` | item 2 — **closes only partially**, see writer-04 |
| D2 | Placement of structures within [16, dir_offset) | `[R-SLB-05]` | item 3 — closed (total order) |
| D3 | Extent of gaps between structures | `[R-SLB-05]`, `[R-CNT-03]` | item 3 — closed ("Each structure begins where the previous one ended") |
| D4 | Content of gaps and of the pre-trailer pad | `[R-CNT-03]` (SHOULD only), §5.2 ("its content is unconstrained") | item 3 — closed (zero, "taken as a requirement here") |
| D5 | Record order in the directory | `[R-CNT-14]` ("Record semantics MUST NOT depend on record order") | item 3 — **partially**, see writer-03 |
| D6 | Sub-record order | `[R-CNT-14]` | item 3 — closed (type, then encoded bytes lexicographic) |
| D7 | Encoder output for codecs 2–4 | `[R-CNF-05]`; §17.2's note on DEFLATE's unused final-byte bits | item 1 — closed by pinning implementation + version + settings; item 1 states plainly that cross-implementation identity is unattainable here |
| D8 | zstd frame options: Frame_Content_Size present or absent (`[R-COD-06]`: "MAY be present"), single-segment vs Window_Descriptor | §17.2 | item 1 (encoder settings) |
| D9 | Number of generations used to reach the same content | §9 nowhere constrains it | item 4 — closed (one generation) |
| D10 | Storing an all-fill tile vs emitting the sentinel | no rule requires either | item 6 — closed |
| D11 | Fill recorded when the caller chooses none | `[R-TYP-10]` (SHOULD) | item 7 — closed, and item 7 correctly notes it feeds back into D10 |
| D12 | `version_minor` above the floor | `[R-CNT-26]` (SHOULD) | item 8 — closed |
| D13 | Declaring A, or S/A_slab, or neither | §16 leaves it to the writer | item 5 — closed |
| D14 | Unicode normalization of names | `[R-ENC-14]` (SHOULD NFC) | item 10 — closed, with the byte arithmetic (12 vs 13) worked |
| D15 | JSON serialization of user metadata: whitespace, escaping, number formatting | `[R-MTA-05]` fixes key order only and says so: "it does not make two writers' output identical" | item 9 — closed by pinning the JSON writer |
| D16 | User-metadata storage encoding 1 vs 2 | §18.2 | item 9 — closed ("a fixed storage encoding") |
| D17 | Emitting `0xEECB3BB2` for a full all-sentinel segment vs computing it | `[R-IDX-05]` | no divergence — I verified the constant equals the computed CRC |
| D18 | Length of the pre-trailer pad | **not free**: `[R-LIF-02]` step 5 pads to the next 64-byte boundary, and §6.2 says "a longer gap is conforming, and no conforming commit produces one" | item 3 mentions it; already closed by the commit protocol |
| D19 | `flags` ignore-lane bits at creation | **not free**: `[R-CNT-08]` — "a writer creating a file under this text MUST write flags = 0" | item 8 restates it |
| D20 | Padding-position and pad-bit content | **not free**: `[R-SER-05]` | correctly absent from Appendix G |
| D21 | Whether a tile is stored at all, beyond D10 | determined by content + D10 | — |

Everything in D1–D16 that Appendix G claims to close, it does close,
with two exceptions (D1 and D5) that are findings **writer-04** and
**writer-03**. D17–D21 are freedoms one might expect and the document
has already removed; Appendix G is right not to list D20 and right to
list D18/D19 only as restatements.

I could not find a divergence I was unable to classify as either
legitimate or forbidden. The catalogue's closing paragraph in Appendix G
("gap *content* … gap *extent* … record and sub-record order … the fill a
writer records when its caller chooses none … the sentinel for every
all-fill tile … a single generation … the absence or fixing of a declared
alignment and slab … `version_minor` at its floor … a derived `file_id`
… and the producer pinning of items 1 and 9") is an accurate inventory of
D2–D16 and I could not falsify it. The two claims I *can* falsify are
inside items 2 and 3, below.

---

## 6. Findings

### writer-01 — CONTRADICTION — §20.3 `[R-WRT-04]` step 2 vs §2.3 `[R-CNF-05]`/`[R-CNF-06]`; and `[R-LIF-01]` cited for a rule it cannot support

**Location:** §20.3, `[R-WRT-04]` step 2; §2.3, `[R-CNF-05]`, `[R-CNF-06]`.

**Quotation (§20.3, step 2):**

> The open establishes no tile-scope violation — it consumes the trailer
> and directory only (`[R-RDR-01]`) — and a malformed index entry an
> appender meets while re-emitting a region is carried forward
> byte-identically at its disk-ordinal position under step 4, not
> repaired to a sentinel. Against any other structure the appender
> carries forward, it MUST NOT repair the defect — `[R-LIF-01]` freezes
> the committed prefix — and MUST NOT drop the record (§20.4);
> re-emitting it byte-identically is not authorship, since `[R-WRT-05]`
> makes only *a record it modifies* new output under `[R-CNF-05]`.

**Quotation (§2.3):**

> A writer MUST emit only conforming files. `[R-CNF-05]`

> An updater MUST satisfy every writer requirement for the bytes it
> produces, and additionally MUST honor the preservation obligations of
> §20.4 … `[R-CNF-06]`

**Why it bites.** Take my `img` layer and suppose its committed index
entry for s=2 carries offset 8 (a T8 violation: "a non-sentinel
tile-index entry has offset < 16"). Now commit a change that stores a
new tile at s=3. §20.3 step 4 requires the *whole* index region to be
re-emitted "necessarily at a new placement", with "every other entry
byte-identical at its disk-ordinal position". So the appender physically
writes, into bytes it appends after F, an entry it can see is malformed,
and the resulting file is nonconforming. §20.3 tells it to. `[R-CNF-05]`
and `[R-CNF-06]` tell it not to.

The escape clause does not reach. It says re-emission "is not
authorship" *because* `[R-WRT-05]` makes only a modified record new
output — but a tile-index region is not a record, and the layer record
that owns it *is* being modified (its extent slot moves), so
`[R-WRT-05]` classifies it as new output rather than exempting it.

And the reason offered for the prohibition on repair — "`[R-LIF-01]`
freezes the committed prefix" — is a non-sequitur here. `[R-LIF-01]`
freezes bytes in [0, F). The re-emitted index region and the re-emitted
directory are written *at and after F*. Nothing in `[R-LIF-01]` prevents
an appender from writing a corrected entry into the new region; whatever
the right answer is, this is not the rule that gives it.

**Permitted readings.** (i) The appender commits and emits a
nonconforming file; §20.3's carry-forward is a stated exception to
`[R-CNF-05]`. (ii) `[R-CNF-05]`/`[R-CNF-06]` govern the file the updater
emits, so an appender that has detected the malformed entry must refuse
the commit (it may not repair, per §20.3, and may not emit a violating
file, per `[R-CNF-05]`). I implemented (i), because §20.3 is the more
specific text and states the behaviour imperatively — but I recorded it
as a guess, and I would want the exemption written into `[R-CNF-06]`
rather than left to a parenthetical whose cited authority does not fit.

**Byte level: yes.** Updater A (reading (i)) emits a file whose new index
region contains `offset = 8` at entry 2. Updater B (reading (ii)) emits
nothing. The question at issue is precisely whether that byte sequence is
one a conforming updater may emit.

---

### writer-02 — AMBIGUITY — a commit that shrinks a dimension extent silently turns real positions into padding positions, and §20.3 does not say whether the affected stored tiles must be re-emitted

**Location:** §20.3 `[R-WRT-04]` step 4 and its "three shapes a commit
takes" example, shape (c); §14.5 `[R-SER-05]`; §21.4 row T4.

**Quotation (§20.3, example shape (c)):**

> **(c) A change confined to the directory** — clearing a slab
> declaration, renaming a layer, or changing a channel's fill value on a
> layer with no padding position and no pad bit. Only the directory is
> re-emitted. A fill change on a layer carrying either additionally
> requires re-emitting the affected stored tiles, whose content
> `[R-SER-05]` fixes — which makes it shape (b).

**Quotation (§14.5, `[R-SER-05]`):**

> at every padding position, a writer MUST encode, for each channel the
> position carries, that channel's fill value

**Why it bites.** Take a layer with extents (8, 8) and tile extents
(4, 4): G = (2, 2), no padding positions anywhere, four stored tiles.
Now commit a change of E_x from 8 to 7. G_x = ⌈7/4⌉ = 2, unchanged;
entry_count is unchanged; the stored-tile set is unchanged; the index
content is unchanged. Under §20.3 step 4 nothing forces the index region
to be re-emitted, and under the shape taxonomy this is squarely shape
(c) — "a change confined to the directory".

But the column x = 7 has just become a padding column. The two edge
tiles' stored bytes hold real sample values there, and `[R-SER-05]` now
requires those positions to hold fill. The file the commit produces has
two T4 violations in tiles the commit never touched.

The document states the *analogous* obligation for the analogous
operation — a fill change is called out as promoting shape (c) to shape
(b) — and simply never states it for an extent change. Nor does it
prohibit shrinking: I grepped, and the strings "shrink"/"shrunk" do not
occur anywhere in the document. Every discussion of extent change is of
*growth* — §20.1's appender description ("growing extents"), §20.3 step
4 ("added tiles, grown extents"), §11.1's rationale, `[R-SLB-04]`'s
trigger. Growth is the safe direction: a position that was padding held
fill, and fill is a legal sample value, so growth never breaks
`[R-SER-05]`. Shrinkage is the unsafe one and is unaddressed.

The same gap reaches two neighbouring operations that are also absent
from the taxonomy: changing a channel's type, or adding/removing a
channel from an interleaved layer, changes Q and therefore the decoded
size, so every stored tile becomes a T3 (`[R-SER-07]`) violation. That
one at least is reader-detected and loud; the padding one is
verifier-only and silent.

**Permitted readings.** (i) `[R-CNF-05]` governs the whole emitted file,
so the commit must additionally re-emit every edge tile whose padding
set grew, exactly as it must for a fill change — shape (b). (ii) §20.3's
shape taxonomy is the operative enumeration, the affected tiles are
carried forward under the same carry-forward doctrine as writer-01, and
the commit is shape (c). I implemented (i), because it is the only
reading that yields a conforming file — but reading (ii) is defensible,
and §20.3's own step-2 language ("re-emitting it byte-identically is not
authorship") is what makes it defensible.

**Byte level: yes.** Updater A emits a file containing two re-emitted
edge tiles with fill-encoded column 7, a re-emitted index region and a
new directory. Updater B emits a file containing only a new directory.
The two files differ over hundreds of bytes, both writers claim
conformance, and a verifier certifies A's output and rejects B's at tile
scope (T4).

---

### writer-03 — AMBIGUITY — Appendix G item 3 fixes no order between two top-level records of the same type other than 0x0001

**Location:** Appendix G, item 3.

**Quotation:**

> Records are ordered by type, and within type 0x0001 by layer name; a
> layer record's sub-records are ordered by type, and within a type by
> their encoded bytes compared lexicographically — an order a reader can
> derive, which a creation order is not

**Why it bites.** §7.2 makes multiplicity a per-type matter and caps only
two types: "in format major 1: any number of layer records …; at most one
file-scope user-metadata record …; and at most one user-metadata
sub-record per layer record". Nothing limits the number of top-level
records of an unassigned type. A conforming file may therefore carry two
top-level MU=0 records of the same type — §21.6 records exactly that as a
non-violation — each with its own extent.

Item 3 orders records by type, tie-breaks type 0x0001 by layer name, and
gives a general within-type tie-break **only for sub-records**. Two
top-level records of type 0x8000 are untied, both in the directory's
record sequence and in the "record extents in ascending record order"
placement pass. Two profile writers given identical input emit different
directory bytes and different extent placement — in a profile whose
stated purpose is that they do not.

**Permitted readings.** (i) The lexicographic tie-break is scoped to
sub-records exactly as written, and top-level same-type records are
unordered — the profile has a hole. (ii) The lexicographic tie-break is
meant generally and the sentence merely introduces it in the sub-record
clause. I implemented (ii), because it is the only reading under which
item 3 does what item 3 says it does, and because the parenthetical
justification — "an order a reader can derive, which a creation order is
not" — is a general argument, not a sub-record-specific one. Under
reading (i) a profile writer has to invent a tie-break and two of them
will not agree.

This also matters forward: §10.1's first extension vehicle is new record
types, and a future minor version registering a repeatable top-level type
walks straight into it.

**Byte level: no.** Appendix G is explicitly non-normative and
"adds no requirement to any actor: a writer ignoring it is fully
conforming". Both writers emit conforming files under either reading, and
no reader's accept/reject verdict moves. What is at stake is whether the
profile achieves byte-identity, which is the profile's own claim rather
than a conformance property.

---

### writer-04 — AMBIGUITY — Appendix G item 2's derived `file_id` is not well defined, though item 2 claims it is

**Location:** Appendix G, item 2.

**Quotation:**

> **`file_id` from a cryptographic hash of the file's own emitted
> bytes**, computed over [0, F − 64) together with the trailer's other
> fields with the `file_id` field taken as zero, then written in.
> Deterministic, and high-entropy — satisfying §9.3's advice rather than
> contradicting it, which a counter would not. Hashing the bytes rather
> than an abstract notion of "content" is what makes the identifier well
> defined

**Why it bites.** I tried to implement this item and could not, without
inventing four things the profile does not state:

1. **Which hash.** "a cryptographic hash" names none. Items 1 and 9 —
   the profile's own model for closing a producer-dependent
   choice — insist on "a named codec implementation at a named version"
   and "a named JSON writer at a named version". Item 2 names nothing.
2. **Whether the trailer CRC is one of "the trailer's other fields".**
   The trailer has eleven fields; "other" than `file_id` leaves ten,
   including the CRC at [60, 64), which is itself a function of
   `file_id`. Including it (computed over the zeroed-`file_id` trailer)
   is well defined but a different input from excluding it, and yields a
   different digest.
3. **The serialization of "the trailer's other fields" into the hash
   input.** Concatenated in trailer-layout order as a 60-byte block with
   bytes [48, 56) zeroed? As a 64-byte block? Field-by-field with
   separators? Each gives a different digest.
4. **The reduction of a digest to a nonzero `u64`.** Low eight bytes or
   high eight? Little- or big-endian? And what if the reduction yields
   zero, which `[R-CNT-06]` forbids?

Any two of those choices made differently produce a different `file_id`,
hence eight different trailer bytes and a different trailer CRC. So the
sentence "Hashing the bytes rather than an abstract notion of 'content'
is what makes the identifier well defined" is falsifiable as stated:
hashing the bytes removes one source of indeterminacy (what counts as
content) and leaves four.

**Permitted readings, and what I picked.** I implemented item 2 as
SHA-256 over the 60 bytes [F−64, F−4) with [48, 56) zeroed, prefixed by
the file's bytes [0, F−64), taking the first eight digest bytes
little-endian and substituting 1 if the result is zero. That is a guess
in four places. For the file I actually built I fell back on a fixed
literal `file_id` and noted it as a non-profile choice rather than
pretend the derivation was determined.

**Byte level: no.** Same reasoning as writer-03: Appendix G is
non-normative, every candidate `file_id` is nonzero and therefore
conforming, and no reader's verdict changes. This is a defect in the
profile's claim, which is what the charter asked me to test, not in the
format.

---

### writer-05 — AMBIGUITY — §20.4's MU=0/PE=0 drop licence can be bootstrapped by a second drop, or cannot, and the text supports both

**Location:** §20.4, the MU = 0, PE = 0 row of the updater-obligation table.

**Quotation:**

> Retain byte-identical, or drop it — its extent becoming slack. An
> appender may drop it only in a commit that *independently* changes the
> scope the record attaches to: for a layer sub-record, that layer's
> record, the entry set of its index, or which of its tiles are stored;
> for a top-level record, the file's layer set or another *non-layer*
> top-level record. Superseding a stored tile's bytes is not such a
> change for either kind … Dropping the record is not itself such a
> change either, so a commit whose only effect would be the drop MUST
> retain it.

**Why it bites.** A metadata-stripping updater is handed a file carrying
two top-level MU=0/PE=0 ancillary records R1 and R2, and is asked to drop
both and change nothing else. For R1, has the commit "independently"
changed "another *non-layer* top-level record"? R2 has been dropped. The
exclusion clause denies that a record's *own* drop counts ("Dropping the
record is not itself such a change"), and says nothing about another
record's drop. Symmetrically for R2.

So: dropping one such record in an otherwise-empty commit is forbidden,
and dropping two may be permitted or may not be. Which answer holds
decides the directory bytes of a perfectly ordinary tool.

**Permitted readings.** (i) "changes … another non-layer top-level
record" includes dropping it, so the two drops license each other and
the commit is permitted. (ii) The word *independently*, italicised in
the text, requires the qualifying change to be independent of the drops
under consideration; two mutually-justifying drops are not, and a drop is
in any case a removal rather than a change *to* a record, so neither may
be dropped. I implemented (ii), because *independently* is doing visible
work in the sentence and because reading (i) makes the final sentence's
prohibition trivially evadable by pairing any forbidden drop with a
second one.

**Byte level: yes, though narrowly.** Updater A (reading (i)) emits a
directory containing neither R1 nor R2; updater B (reading (ii)) emits a
directory containing both, and B's file is larger by two record headers,
two inline payloads and two live extents. Both files are conforming;
what differs is which of the two a conforming updater is permitted to
emit. I flag this as the weakest of my three byte-level claims: it needs
a tool that drops several ancillaries and changes nothing else.

---

### writer-06 — OBSERVATION — `[R-SLB-04]`'s trigger is narrower than its own definition of an affected run

**Location:** §16.2, `[R-SLB-04]`.

**Quotation:**

> A writer or updater whose commit supersedes a stored tile in, or grows
> the extents of, a slab-declared layer MUST either re-establish the
> invariants for every affected run — a run whose stored-tile set or
> byte placement the commit changes — or clear the declaration in the
> new generation; carrying a stale declaration forward is a validity
> error at layer scope

**Why it bites.** The trigger is "supersedes a stored tile in, or grows
the extents of". The scope, in the same sentence, is "a run whose
stored-tile set or byte placement the commit changes". Those do not
match. The two commonest slab-disturbing operations fall outside the
trigger and inside the scope:

- **Storing a tile that was a sentinel.** §3.1 is explicit that a
  supersede is about a tile already stored ("Superseded payload bytes
  from earlier generations do not make a tile stored"), so newly storing
  is not superseding. But it changes the run's stored-tile set, and the
  new tile must be packed against tiles that `[R-LIF-01]` has frozen in
  the committed prefix — usually impossible without relocating the whole
  run.
- **Unstoring a tile (writing the sentinel over a stored entry).** Same:
  §15.3 and `[R-SLB-03]` make sentinels transparent to run continuity,
  so unstoring the *first* stored tile of a run promotes the next one to
  first, and that one's offset must now satisfy `mod A_slab = 0` — which
  it generally does not.

In my generation-2 file this is concrete: `msk` run 1 holds stored tiles
at ordinals 2 and 3, at 576 and 578. Unstore ordinal 2, and ordinal 3 at
578 becomes the run's first stored tile; 578 mod 64 = 2, so L42 fires.
`[R-SLB-04]` never triggered, because the commit neither superseded a
stored tile nor grew an extent.

**Why this is an OBSERVATION and not an ambiguity.** The file's validity
is decided regardless: `[R-SLB-03]`'s invariants bind the file, L41/L42
register them, and `[R-CNF-05]` obliges the writer to emit a conforming
file — so a writer that reasons from `[R-SLB-03]` forward reaches the
right answer. Reaching it costs a reader of §16.2 an extra inference
that the section's own note discourages, since the note tells you the
obligation "is what makes those two rows reachable at all after a
commit" — implying the trigger list is meant to be the complete set of
commits that can reach them, which it is not.

**Byte level: no.** `[R-SLB-03]` plus `[R-CNF-05]` already decide what a
conforming writer may emit in every case the trigger omits. Only the
route to the answer is defective.

---

### writer-07 — AMBIGUITY — no authoritative flag source for a record type the updater implements but §7.3 does not register

**Location:** §20.4 ("Persistence governs every record type…"); §7.3, `[R-CNT-22]`.

**Quotation (§20.4):**

> Persistence governs every record type; only the authoritative source
> of the flags differs. For a type §7.3 registers, the registry's fixed
> flags govern rather than the stored ones (`[R-CNT-22]`) … For a type
> the updater does not implement, the stored flags are authoritative
> (§7.3, `[R-CNT-15]`; MU = 1 with PE = 0 is read as PE = 1,
> `[R-CNT-12]`), and carry these obligations:

**Quotation (§7.3, `[R-CNT-22]`):**

> Stored flag bits are authoritative only for record types the consuming
> tool does not implement (`[R-CNT-15]`).

**Why it bites.** The two-way split is drawn as *registered* vs *not
implemented*, and those are not complements. A tool that implements a
private experimental type — §10.3's whole purpose, "Experimental values
are private use" — is in neither branch: §7.3 does not register the
type, so there are no registry flags; and `[R-CNT-22]` says the stored
bits are *not* authoritative for a type it implements. The updater has
no stated source for the PE bit, and PE is what decides whether it may
drop the record. So an updater handed a conforming file carrying an
experimental MU=0/PE=0 record it happens to implement has no rule
telling it whether §20.4's drop licence is available.

The same seam opens forward, not only sideways: a later minor version
registering type 0x0003 (§10.1's first extension vehicle) is registered
by *the registry*, not by *§7.3's table*, and §20.4's branch is written
against §7.3 specifically.

**Permitted readings.** (i) A tool that implements a type knows that
type's semantics, including its persistence, from wherever it got the
type — for private use that is the private definition, which this
document deliberately does not reach. (ii) Falling back to the stored
bits is the only thing the file offers, so they govern by default. I
implemented (i) for experimental types and (ii) for a hypothetical
registry-assigned type, and noted both as guesses.

**Byte level: no.** For the experimental branch, §10.3 hands private-use
semantics to the private user with "no collision protection" and nothing
in this document distinguishes two experiments, so the persistence of a
private type is by construction not something this document was ever
going to decide — the silence is the design. For the registry branch, no
file expressible under this text can exhibit the case, since format major
1 assigns exactly 0x0001 and 0x0002. Both branches leave the byte
sequences a *this-text* conforming updater may emit unchanged.

---

### writer-08 — OBSERVATION — Appendix G item 2 and `[R-WRT-06]` collide when an already-compact profile file is compacted

**Location:** Appendix G item 2; §20.5, `[R-WRT-06]`.

**Quotation (`[R-WRT-06]`):**

> It MUST mint a fresh file_id for the output — a new draw under §9.3's
> randomness advice, not merely a value compared against the input's —
> and generation 1

**Why it bites.** Appendix G item 4 fixes the profile at "One
generation", and a compactor's output is generation 1 by rule, so a
compactor can be a profile writer. Item 2 makes `file_id` a pure function
of the output's other bytes. Now compact a profile file that is already
compact — generation 1, item-3 placement, no reclaimable slack. The
compactor carries every stored tile's bytes verbatim, every record per
§20.4, and re-derives placement under item 3, which reproduces the input's
placement exactly. Every byte of [0, F−64) and every other trailer field
is therefore identical to the input's, so item 2 derives the *input's*
`file_id` — which is precisely what `[R-WRT-06]` forbids ("not merely a
value compared against the input's"). The output is byte-identical to the
input, which is also the one thing compaction's `file_id` rule exists to
prevent, since §20.5's example explains that "a cache keyed (file_id,
range) is sound precisely because ranges never change beneath a file_id".

**Why this is an OBSERVATION.** It is decidable: Appendix G is
non-normative and `[R-WRT-06]` is a MUST, so `[R-WRT-06]` governs and a
profile compactor must break item 2 in this case. Deciding it requires
noticing that items 2 and 4 together make a compactor a profile writer,
which is several hops from either text.

**Byte level: no.** `[R-WRT-06]` decides it; the normative rule governs
over the non-normative appendix, so no conforming compactor's permitted
output changes.

---

## 7. What I could not determine, and what I could

Determined without guessing, in case it is useful to know where the
document is doing its job: the whole creation layout; every field width,
value set and cross-check; the commit protocol's step order, both
barriers and the commit point; the recovery behaviour at all five crash
points I constructed; the slack accounting for all five commit shapes;
the entire record-flag matrix except the seam in writer-07; the slab
invariants and their cost on re-commit; the sentinel encoding, the
segment-CRC constant, the packed-plane arithmetic, the padding-content
rule, and Appendix A's stated trailer CRC — all of which reproduced
numerically.

Guessed, and flagged above: whether an updater may emit a file carrying a
violation it did not author (writer-01); what a commit owes to stored
edge tiles when it shrinks an extent (writer-02); how to order two
same-type top-level records under the profile (writer-03); four
under-specified components of the profile's derived `file_id`
(writer-04); whether two drops license each other (writer-05); the flag
authority for an implemented unregistered type (writer-07).

**Confidence:** medium. A writer and appender built from this document
alone would interoperate on every file I could construct; the two places
I would expect two independent implementations to actually diverge on
bytes are writer-01 and writer-02, and writer-02 is the one I would fix
first, because it turns a conforming file into a nonconforming one
through an operation the document's own taxonomy calls "a change confined
to the directory".
