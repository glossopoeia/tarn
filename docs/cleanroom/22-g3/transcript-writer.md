# Round 22 — Writer / updater implementer, working transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in
four passes covering lines 1–4395 (the whole document). I opened no ADR, no
`PLAN.md`, no `AGENTS.md`, no `conformance/`, no `spec/registry.json`, and ran no
`git` command and no web access. I did not list or read the output directory.

I ran local Python that reads no project file except `spec/tarn.md` (one script
counts register instances by parsing the §21 tables; the rest are self-contained
byte builders). Scratch files live in a private subdirectory I created —
**note for the operator**: my first two scratch scripts, written to the
scratchpad *root*, were silently overwritten mid-session by another process
writing files of the same name, and I only noticed because a rebuilt artifact
came back 640 bytes instead of 2240. Concurrent walkers sharing the scratchpad
root is a hazard for this workflow. Everything below was re-derived in
`scratchpad/w22priv/`.

**Context I did not ask for.** Material appeared in my context before I began: a
project-instruction pointer, and an index of the maintainer's memory files with
one-line descriptions naming things like a working cadence, a register/corpus
relationship, and prior workflow failures. I read none of the files it indexed
and used none of it. I disclose it because the rules require disclosure, not
because it moved anything.

I did not build a running implementation. I built files byte by byte with
arithmetic I checked, which is what "on paper but concretely" asks for.

**Calibration of my own tooling first.** Before trusting any of my byte layouts I
reproduced every worked constant in the document with my own CRC-32C:

| Document claim | Where | My computation |
|---|---|---|
| CRC-32C(`"123456789"`) = 0xE3069283 | §4.5 | 0xE3069283 |
| CRC-32C(zero bytes) = 0x00000000 | §4.5 | 0x00000000 |
| segment CRC over four sentinel entries = 0x80A34955, stored `55 49 A3 80` | §7.4 example | 0x80A34955 / `55 49 a3 80` |
| crc_of_crc_array for that layer = 0xC4EE982E | §7.4 example | 0xC4EE982E |
| CRC of a full 2¹⁶-entry all-sentinel segment = 0xEECB3BB2 | §15.4, `[R-IDX-05]` | 0xEECB3BB2 |
| Appendix A trailer CRC = 0xE00938D2 | Appendix A | 0xE00938D2 |
| `temp` channel entry = `04 74 65 6D 70 0C 00 04 00 00 C0 7F` | §12.3 | identical |
| byte-shuffle of 1.0,2.0,3.0 float32 = `00 00 00 00 00 00 80 00 40 3F 40 40` | §17.3 | identical |

All eight reproduce. Nothing in the arithmetic below rests on an unverified
checksum implementation.

I also mechanically counted §21's register: **121 conditions over 273
instances**, which is exactly what `[R-ERR-02]` (§21.8) states. Per family:
F 36 conditions / 58 instances, L 49 / 116, T 26 / 55, R 10 / 44. The register's
own arithmetic is internally consistent, which matters later — it is what
forecloses one candidate finding I had to discard.

---

## 1. Creation: a file built end to end

### 1.1 What I chose to build, and why

Something small enough to lay out by hand and non-trivial enough to exercise the
writer's real decisions: two layers with opposite layouts, both alignment
mechanisms (mutually exclusive per `[R-CNT-16]`, so one layer each), a sentinel
tile, an edge tile with padding positions, a packed boolean plane with pad bits,
and a file-scope user-metadata record.

**Layer `elev`** — rank 2, dims `y`(E=5,T=4) and `x`(E=5,T=4), interleaved,
C = 2: `h` float32 (fill = quiet NaN `0x7FC00000`) and `m` bool (fill `0x00`).
Codec 1, filter 1, alignment A = 512, no slab.

Grid arithmetic (§11.2, `[R-GEO-03]`): Gᵧ = ⌈5/4⌉ = 2, Gₓ = 2, N = 4, P = 16.
Interleaved decoded size (§14.2, `[R-SER-02]`): Q = Bʰ + Bᵐ = 4 + 1 = 5,
decoded size = P·Q = 80. Addressed-tile count = N = 4 (interleaved), so
`entry_count` = 4 and, by `[R-CNT-17]`, extent_length = 4×20 + ⌈4/2¹⁶⌉×4 = 84.

**Layer `mask`** — rank 1, dim `x`(E=10,T=4), **planar**, C = 1: `b` bool,
fill `0x01`. Codec 1, filter 1, no alignment, slab S = 2 with A_slab = 64.

Gₓ = ⌈10/4⌉ = 3, N = 3, P = 4. Planar bool ⇒ §14.3 packing: decoded size =
⌈4/8⌉ = **1 byte**, with pad bits at positions 4–7. Addressed-tile count =
C·N = 3, extent_length = 3×20 + 4 = 64.

**Tile content.** I set `h(y,x) = y·10 + x` and `m(y,x) = (x+y) even`, except
that I forced column x = 4, rows 0–3 to fill so that spatial tile s = 1 would be
entirely fill. Tile s = 1 covers y∈[0,4), x∈[4,8): four real positions (all
forced to fill) and twelve padding positions, which `[R-SER-05]` fixes to fill.
So the whole tile is fill and I emit the **sentinel** for it — permitted rather
than required (a stored all-fill tile is equally conforming; Appendix G item 6
turns it into a rule only for the reproducible profile). Tile s = 3 covers
y,x ∈ [4,8): one real position (4,4) and fifteen padding positions.

For `mask`, values alternate true/false over x = 0…9. Tile 2 covers x = 8…11,
so x = 10 and 11 are padding positions and must carry the fill bit (1), and
because P mod 8 = 4 ≠ 0 the final byte's bits 4–7 are pad bits which
`[R-SER-05]` also fixes to the fill bit. My computed tiles are `F5`, `F5`, `FD`.
Working tile 2 by hand: bit0 = x8 = true = 1; bit1 = x9 = false = 0;
bit2 = x10 = padding = fill = 1; bit3 = x11 = padding = fill = 1 ⇒ low nibble
`0b1101` = 0xD; bits 4–7 pad = 1111 ⇒ 0xFD. My builder agrees.

### 1.2 Placement — every decision, and who made it

`[R-LIF-02]`'s creation path: front block first, then steps 2–6 "writing
beginning at offset 16", generation 1. Step 2 permits "any order satisfying
§5.2's coverage classes"; `[R-SLB-05]` makes ordering and relative position free
outright. So placement is **mine**, not the document's. To make the walk
reproducible I adopted Appendix G item 3's total order (legitimate but
non-normative): per layer in ascending layer-name byte order, its stored tiles in
disk-ordinal order, then its index region; then remaining record extents; then the
directory. `elev` (`65 6C 65 76`) sorts before `mask` (`6D 61 73 6B`).

One decision Appendix G explicitly anticipates: the first structure would go at
16, but `elev` declares A = 512 and its first structure *is* a stored tile, whose
offset must satisfy `offset mod A = 0` (`[R-SLB-01]`). Item 3 says "where a
declared alignment admits no structure at 16, at the least position above it the
declaration admits" — 512. That leaves [16, 512) as slack in a freshly created
file, which I want to flag as a thing an implementer will not expect: **a
conforming creator's very first 496 bytes after the signature can be waste.**
`[R-LIF-02]`'s "writing beginning at offset 16" does *not* require a structure at
16; §5.1's anatomy ("with slack wherever a commit left a gap") and `[R-SLB-05]`
settle it.

The resulting map (F = 2240):

```
[0,16)        front signature block
[16,512)      slack 496        <- forced by A=512 on the first structure
[512,592)     elev tile 0   (80)
[592,1024)    slack 432        <- alignment gap
[1024,1104)   elev tile 2   (80)
[1104,1536)   slack 432        <- alignment gap
[1536,1616)   elev tile 3   (80)   (edge tile: 1 real position, 15 padding)
[1616,1700)   elev index    (84)   <- NOT alignment-constrained; see below
[1700,1728)   slack 28         <- forced by A_slab=64 on mask run 0
[1728,1729)   mask tile 0   (1)
[1729,1730)   mask tile 1   (1)    <- packed: offset = prev offset + prev length
[1730,1792)   slack 62         <- forced by A_slab=64 on mask run 1
[1792,1793)   mask tile 2   (1)
[1793,1857)   mask index    (64)
[1857,1909)   umd extent    (52)   = 48-byte JSON document + 4-byte terminal CRC
[1909,2165)   directory     (256)  = 252-byte record sequence + 4-byte CRC
[2165,2176)   pre-trailer pad 11
[2176,2240)   trailer       (64)
```

Live claimed = 16 + 64 + 256 + (84+64+52) + (3×80 + 3×1) = 779. Slack = 1461,
**65% of the file**. That is conforming and, per `[R-SLB-05]`, "wastes space
rather than violating a rule".

Decisions the document fixed, and where:

- Front block bytes: fixed exactly (§6.1, `[R-CNT-04]`).
- Index region *not* alignment-constrained: `[R-SLB-01]` binds "every **stored
  tile's** offset", nothing else. So `elev`'s index at 1616 (1616 mod 512 = 80)
  is fine. I had to reread this; a writer that over-applies A here wastes another
  432 bytes for nothing.
- Slab run partition: `[R-SLB-02]` — interleaved layers have one block [0,N);
  planar layers one block per channel. `mask` has C = 1, so one block [0,3),
  S = 2 ⇒ runs [0,2) and [2,3), the final run shorter than S, which
  `[R-SLB-02]` allows. Run r starts at ordinal block_start + r·S.
- Slab invariant: `[R-SLB-03]` — within a run, packed (`offset = prev offset +
  prev length`) and the run's *first stored tile* A_slab-aligned. Runs are "not
  mutually ordered or joined", so the 62-byte gap between run 0's end and run 1's
  start is legal slack, not a violation.
- `entry_count` and extent_length: `[R-CNT-17]`, exact formula, no freedom.
- `crc_of_crc_array`: derived; 0 iff entry_count = 0 (`[R-CNT-23]`).
- The pre-trailer pad: `[R-LIF-02]` step 5 pads *to the next 64-byte boundary*.
  dir_end = 2165, 2165 mod 64 = 53, pad = 11, F = 2240, F mod 64 = 0. Not free:
  §6.2 says "a longer gap is conforming, and no conforming commit produces one",
  and §2.3 classifies a longer gap as a **conduct** violation that does not make
  the file nonconforming. And the degenerate reading ("dir already 64-aligned:
  pad 0 or pad 64?") is closed by §6.2's "a writer that ends its directory on a
  64-byte boundary leaves none".
- Directory last: `[R-CNT-05]` — no structure between the directory's end and the
  trailer (F7 for a verifier).
- Record flags: `[R-CNT-22]` + §7.3 fix layer = MU 1 / PE 1 (`flags = 0x0003`)
  and user metadata = MU 0 / PE 1 (`0x0002`). With `[R-ENC-08]` bit 0 = LSB.
- Trailer field values: §6.2's table. `file_id` nonzero, my choice; §9.3 makes
  cryptographic randomness a SHOULD. `version_minor` 0 by `[R-CNT-26]`'s SHOULD.
  `flags` = 0 by `[R-CNT-08]`'s MUST for a creator. `reserved` zero.

Decisions the document left to me: placement and order of every structure; which
all-fill tiles to store versus sentinel; codec, filter, tile extents, layout,
alignment/slab declarations and their values; `file_id`; the JSON document's
formatting (subject to `[R-MTA-05]`'s ascending-key ordering — my two keys
`tarn.creator` and `tarn.title` compare `c` < `t` at byte 5, so creator first);
slack content (I zeroed, per `[R-CNT-03]`'s SHOULD).

### 1.3 The `elev` layer record, byte for byte

inline_length = 103. Fields packed in §7.4's table order, no padding
(`[R-CNT-18]`: "packed in table order with no alignment or padding between
them"):

```
off  bytes                               field
  0  04 65 6C 65 76                      name len 4 "elev"
  5  01                                  layout 1 = interleaved
  6  01 00                               linearization 1 = row-major (only legal value)
  8  01 00                               codec 1 = none
 10  01 00                               filter 1 = none
 12  00 02 00 00 00 00 00 00             alignment A = 512
 20  00 ×8                               slab S = 0
 28  00 ×8                               A_slab = 0  (forced by S = 0, [R-CNT-23])
 36  02                                  rank d = 2
 37  02 00                               channel count C = 2
 39  01 79 | 05.. | 04..                 dim "y": extent 5, tile extent 4    (18 bytes)
 57  01 78 | 05.. | 04..                 dim "x": extent 5, tile extent 4    (18 bytes)
 75  01 68 | 0C 00 | 04 | 00 00 C0 7F    channel "h" float32, fill NaN        (9 bytes)
 84  01 6D | 01 00 | 01 | 00             channel "m" bool,    fill false      (6 bytes)
 90  01                                  index_encoding 1
 91  04 00 00 00 00 00 00 00             entry_count = 4
 99  <u32>                               crc_of_crc_array
```
5 + 1 + 6 + 24 + 1 + 2 + 36 + 15 + 1 + 8 + 4 = 103 exactly, so the sub-record
sequence is empty and `[R-CNT-18]`'s "no residue" holds. `mask`'s payload works
out to 76 by the same accounting. Directory record sequence =
(24+103) + (24+76) + (24+1) = 252; dir_length = 256.

Where I had to be careful: the **fill length prefix must equal the type's element
size** (`[R-CNT-23]`, L30) — 4 bytes for float32, 1 for bool — and the bool fill
byte is constrained to `0x00`/`0x01` (`[R-TYP-07]`, L35). Both are checkable
without knowing the type and validated with it, exactly as §7.4's table says.

### 1.4 Order of writes and the commit point

`[R-LIF-02]`, creation path: front block; **step 2** payloads/index regions/record
extents (order free); **step 3** the complete directory and its CRC; **step 4**
barrier; **step 5** pad + trailer with generation 1; **step 6** barrier. §20.2
restates it and insists on "both barriers, not one".

Durability ordering: everything at steps 1–3 must be durable before the trailer
is written; the trailer's own durability is step 6. The **commit point is the
trailer becoming visible at the physical end of the file** — before that, a
reader sees a file whose last 64 bytes are not a trailer, which `[R-LIF-05]` makes
"torn". The document is careful that a weak barrier degrades safety from
"invisible" to "detected" (§9.2's note), never to silent corruption.

Nothing in the creation path was underdetermined.

---

## 2. Append

### 2.1 Adding a layer's tile to the file above

Operation: store `elev` tile s = 1, which was the sentinel. That changes the
layer's stored-tile set, so `[R-WRT-04]` step 4 requires the **whole** index
region re-emitted, "necessarily at a new placement" (because `[R-LIF-01]` freezes
[0, F)).

`[R-WRT-04]`'s ordered steps, as I executed them:

1. **Establish F** — validate the trailer in the final 64 bytes (`[R-LIF-04]`).
   F = 2240. If that fails the file is torn and there is *no append*; recovery is
   the separate deliberate operation of §9.6.
2. **Open** — §19.1's four steps. I am a reader here. The open consumes trailer +
   directory only; it establishes no tile-scope violation, and it does **not**
   walk sub-records (that is §19.3, at layer access).
3. **Validate what the commit touches** — `[R-WRT-03]`: trailer + *full*
   directory always, plus §19.3 layer validation for `elev` (whose record and
   index I modify), plus the §19.4 index chain for every segment whose entries I
   reuse. Since I re-emit the whole region I reuse entries from every segment, so
   I must verify `crc_of_crc_array` and every segment CRC — i.e. fetch the whole
   index region. `mask` and the user-metadata record I neither modify nor rely
   on, so I owe them nothing beyond re-emitting their records byte-identically.
4. **Write payloads and indexes** beginning at exactly F = 2240. A = 512 forces
   the new tile to 2560, so [2240, 2560) is 320 bytes of brand-new slack.
5. **Re-emit the directory** per §20.4.
6. **Commit**: barrier; pad; trailer with generation 2, same `file_id`, unknown
   ignore-lane bits copied forward, `version_minor` per `[R-CNT-26]`; barrier.

Result:

```
[2240,2560)  slack 320          (alignment gap, brand new)
[2560,2640)  elev tile 1     (80)
[2640,2724)  elev index'     (84)   3 entries byte-identical at their ordinal
                                    positions, 1 re-pointed
[2724,2980)  directory'     (256)   mask + umd records byte-identical [R-WRT-05]
[2980,3008)  pre-trailer pad 28
[3008,3072)  trailer gen 2   (64)
```

Live claimed 859; **slack 2213 = 72% of a 3072-byte file.** Itemised, and it
reconciles exactly:

| slack run | bytes |
|---|---|
| gen-1 alignment gap [16,512) | 496 |
| gen-1 alignment gap [592,1024) | 432 |
| gen-1 alignment gap [1104,1536) | 432 |
| gen-1 slab gap [1700,1728) | 28 |
| gen-1 slab gap [1730,1792) | 62 |
| **superseded** elev index [1616,1700) | 84 |
| **superseded** directory₁ | 256 |
| **superseded** pad₁ | 11 |
| **superseded** trailer₁ | 64 |
| new alignment gap [2240,2560) | 320 |
| new pre-trailer pad | 28 |
| total | **2213** = 3072 − 859 ✔ |

Two things a writer must not get wrong, both of which the document does state but
neither of which is obvious:

- **The appender cannot reuse slack.** `[R-LIF-01]` freezes all of [0, F), and
  slack lives inside [0, F). The 496-byte hole at [16,512) is unusable for the new
  tile even though it is 80 bytes' worth of nothing. Only compaction reclaims.
- **A slab-declared layer can essentially never gain a stored tile by append.**
  `[R-SLB-03]` demands `offset = prev stored tile's offset + its length` inside a
  run, and every existing tile is frozen below F while every new byte is at or
  above F. So `[R-SLB-04]`'s second option — "clear the declaration in the new
  generation" — is the only route, unless the new tile is ordinal-last in a run
  whose prior structure happens to end exactly at F. This is stated but I had to
  derive the consequence; it is the single biggest practical constraint the slab
  feature imposes on updaters, and §16.2's note about slabs does not mention it.

Note also that a **geometry change renumbers disk ordinals**: for a planar layer
with disk ordinal c·N + s, growing any extent across a grid boundary changes both
N and the spatial ordinal s = Σ tᵢ·∏_{j>i} Gⱼ, so *every* surviving entry moves
to a different slot. §20.3 step 4 says exactly this ("a geometry change renumbers
ordinals wherever `[R-GEO-06]` moves them"), and §11.1's rationale repeats it. An
implementer who reads "byte-identical" as "in place" will corrupt every index.

### 2.2 Appending to a file whose records I do not all understand

Here is the full flag matrix. Bits: 0 = MUST_UNDERSTAND, 1 = PRESERVE_ON_EDIT,
2–15 reserved (`[R-CNT-12]`: writers emit zero, readers ignore, **verifier**
detects a nonzero one as F26/L47).

`[R-CNT-12]` also fixes that **MU = 1 with PE = 0 is read as PE = 1** by both
readers and updaters, and is itself a verifier-detected violation (F25/L46). So
the matrix has three behavioural rows, not four.

§20.4's key sentence — "Persistence governs every record type; only the
authoritative source of the flags differs" — gives three sources: the §7.3
registry for a registered type; the definition the updater implements the type
from, for a non-registered type it *does* implement; the **stored bits** only for
a type it does not implement.

**Top-level records:**

| Case | What my updater is permitted to do |
|---|---|
| type 0x0001 layer (implemented; registry MU 1/PE 1) | Retain always — never droppable. May modify. Its extent slot addresses the tile-index region and moves whenever the region is re-emitted. |
| type 0x0002 user metadata (implemented; registry MU 0/PE 1) | Retain always. May modify: a new extent is appended and the old becomes slack (§20.3 example (c) — editing user metadata is *not* a directory-only change). |
| unimplemented type, MU = 1 (reserved range **or** experimental range) | **No commit is available at all.** `[R-CNT-15]` makes it reject-file; the updater is a reader first. Note the sharp consequence: §21.6 says an experimental-range top-level MU = 1 record makes a **conforming** file — so a perfectly conforming file can be permanently un-appendable and un-compactable (`[R-WRT-06]` bars compaction on the same ground). |
| unimplemented, MU = 0, PE = 1 | Retain byte-identical, extent content unmodified. An appender may not relocate it; only §20.5 relocation re-points a slot (`[R-WRT-08]`). |
| unimplemented, MU = 0, PE = 0 | Retain byte-identical, or drop (extent → slack) — but only in a commit that *independently* changes the file's layer set, any layer record's content, or another non-layer top-level record. Dropping is never itself such a change, so a commit whose only effect is the drop MUST retain. SHOULD report the loss. |
| reserved flag bits set, any of the above | Ignore them; re-emit byte-identically. `[R-WRT-05]` forces the nonconforming bits forward, and §20.3 step 2 forbids repairing them. |

A narrowing worth stating: for an **appender** in format major 1, the licence
trigger "another *non-layer* top-level record [changes]" is only reachable
through the user-metadata record, because `[R-WRT-08]` forbids an appender to
modify a record whose type it does not implement at all.

**Layer sub-records** (`[R-CNT-18]` scopes them to the layer):

| Case | Permitted |
|---|---|
| type 0x0002 sub-record | Retain always; may modify (new extent, old → slack). At most one per layer (`[R-CNT-14]`). |
| type 0x0001 appearing as a sub-record | L26: reject-layer. The layer is unusable; re-emit its record byte-identically, modify nothing in it. |
| unimplemented, MU = 1 | Blocks modification of *that layer only*; every other layer stays editable. Reject-layer, and where the file is otherwise conforming `[R-CNT-18]` forbids rejecting the *file* for it. |
| unimplemented, MU = 0, PE = 1 | Retain byte-identical. |
| unimplemented, MU = 0, PE = 0 | Retain, or drop only in a commit that independently changes that layer's record, the entry set of its index, or which of its tiles are stored. Superseding a tile counts, because it re-places the index region and so moves the layer record's extent slot — the document says so explicitly. |

Two detection subtleties I had to reason through rather than read off:

- An unimplemented MU = 1 **sub-record** is *not* found by the open. §19.1 step 4
  parses only each layer record's **name**; the sub-record walk is §19.3, at first
  layer access. `[R-WRT-03]` requires §19.3 only for layers the commit touches.
  So an appender that never touches layer L legitimately never learns that L is
  reject-layer, and just re-emits L's record byte-identically. That is coherent —
  §20.3 step 2's "A violation the open establishes bars the commits its outcome
  bars and no others" is precisely calibrated for it — but a naive implementation
  that validates every layer at open will refuse commits it is allowed to make.
- **Malformed index entries are carried forward, never repaired.** §20.3 step 2
  is explicit, and it forecloses what would otherwise be a real conflict with
  `[R-CNF-05]`: "Reproducing a structure's bytes unchanged is not authoring them
  … which is as true of an index entry copied to its disk-ordinal position as of
  a record re-emitted byte-identically." Note the asymmetry with a **compactor**,
  which `[R-WRT-06]` obliges to *refuse* on meeting the same entry, because
  regenerating a region means re-pointing every non-sentinel entry and a
  structurally-rejected entry has no extent to re-point. Both are stated; the
  asymmetry is deliberate and reasoned in the text.

---

## 3. Slack, by commit shape

Definitions I am working from: §5.2 — slack is every byte of the file the *live
committed state* does not claim; content unconstrained; no conformance
requirement applies; a reader MUST NOT interpret it. §9.7 — the walk's claimants
are the directory, each record's extent (a layer record's extent being its
tile-index region, entering once), and each non-sentinel index entry's stored
extent, plus the front block and the live trailer. A record's header and inline
payload are *not* claimants of their own; the directory region covers them.

**(a) Append that adds a layer.** New slack = the prior directory + prior pad +
prior trailer, plus any alignment/slab gap the new bytes force. Nothing of the
existing layers moves; their records carry into the new directory
byte-identically, extent slots and all. Sized by the *layer count*, never by any
layer's data.

**(b) Append that changes a layer's stored-tile set or index content.** As (a),
plus that layer's whole prior index region, plus every superseded tile payload.
This is the expensive shape: §20.3's note prices it at ~20 MB of index for one
sample of a 10⁶-tile layer. Retained payloads do not move.

**(c) Append confined to the directory** (clearing a slab declaration, renaming a
layer, changing a fill on a layer with no padding position and no pad bit).
Slack = prior directory + pad + trailer only. Editing user metadata is *not* this
shape: the document lives in an extent, so it takes shape (b)'s form.

**(d) A commit that touches nothing** (generation bump only). Legal —
`[R-LIF-02]` step 2 may append nothing. Slack = prior directory + pad + trailer.

**(e) Compaction / whole-file rewrite.** The output carries *no* slack from the
input; its only slack is the alignment/slab gaps and pre-trailer pad it creates
itself. The input file is untouched and persists until something outside this
specification deletes it (`[R-PRV-02]`). Fresh `file_id`, generation 1.

**(f) Abandoned partial write.** **No bytes become slack**, and this is the
distinction I most want to record. Bytes past F are not part of a conforming
file at all: §5.1 fixes the file size of a conforming file at F, and a physical
file longer than F fails §6.2's committed_file_length-versus-transport-size gate
(F17). `[R-CNT-21]` then says the slack total "is not owed at all: the verifier
reports the trailer failure and nothing about slack, which is not a partial total
but the absence of one". `[R-LIF-04]` obliges the next writer to truncate to F or
overwrite from F. So the residue is either erased or overwritten — it never
becomes slack of any generation.

With one real exception, which I want on the record because it is a privacy
consequence the document permits without naming: under `[R-LIF-04]`'s
overwrite-from-F option, the new commit writes structures *and leaves alignment
gaps*, and the bytes of those gaps are whatever the abandoned write left there
unless the writer zeroes them. So **residue from a crashed commit can survive
into a later generation's slack.** §5.2 permits any content there; `[R-CNT-03]`
only advises zeroing; §22.3 and §23.1 flag slack generally as a privacy
consideration. Nothing is violated — but the "truncate to F" option and the
"overwrite from F" option are not equivalent in what they leave behind, and the
document presents them as alternatives without noting it.

**Who counts slack.** A verifier, and only one that reaches a live state
(`[R-CNT-21]`). Where a scope-level rejection ends enumeration, or where the
verifier stops at the first violation under `[R-CNF-11]`, the total is reported
as **partial** — F less the bytes claimed by the claimants actually enumerated,
an upper bound, naming what stopped the walk. Readers and updaters owe nothing.
A layer rejected by the walk itself (L18's overlap, L40–L42's placement) has its
already-enumerated claimants *discarded*, which makes the bound looser, not
tighter — a detail easy to implement backwards.

**What slack may contain.** Anything. Explicitly including a byte string that
mimics a trailer (§21.6: "Inert: nothing enumerates slack"), and including
superseded structures with their old checksums intact. Writers SHOULD zero the
gaps they create.

One under-inclusiveness I noticed and decided not to raise as a finding:
`[R-CNT-03]`'s SHOULD reads "Writers SHOULD zero the gaps they create — the run
before an aligned tile or slab run, and the pre-trailer pad", and that apposition
does not reach the gaps a writer creates purely by scattering under
`[R-SLB-05]`'s placement freedom. Since §5.2 states outright that "no
conformance requirement rides on slack content either way", and since
`[R-CNF-12]` puts SHOULD deviation outside the register entirely, resolving it
moves no byte and no verdict. I record it as a walk note, not a defect.

---

## 4. Torn-write recovery — four crash points

Setup: the gen-1 file above (F = 2240) is being extended to F′ = 3072.

**P1 — crash during step 2** (payload/index bytes written, no directory).
*Next reader*: the physical file is 2240 + k bytes. The 8 bytes at
physical_len − 64 are not the trailer magic ⇒ F8 ⇒ reject-file, reported as
torn. `[R-LIF-05]` forbids scanning backward, so the reader cannot tell torn from
corrupt and is not asked to (§9.5's note is explicit).
*Next updater*: `[R-LIF-04]` — validation of the final 64 bytes fails, so **no
append**. Recovery is a separate deliberate operation.
*Recovery* (§9.6): probe backward from the largest 64-aligned o with o + 64 ≤
physical length. Worked example with k = 10: physical = 2250, largest such o =
2176, which is trail₁; its CRC verifies and committed_file_length = 2240 =
o + 64 ✔. Truncate to 2240, re-verify the whole file, done — the gen-1 state is
restored byte-exactly.
*Conforming meanwhile?* No. The file is nonconforming (F8 and F17 both fire).

**P2 — crash after step 3** (directory written and durable, no barrier/trailer).
Identical to P1 from every actor's point of view. The new directory is just bytes
past 2240; nothing points at it. It becomes nothing — not slack, because there is
no live state containing it — and is discarded by the truncation.

**P3 — crash mid-step 5** (pad written, trailer partially written). Same again.
Worth noting that a partially-written trailer cannot accidentally validate: the
magic is the first 8 bytes of the trailer, so a trailer truncated anywhere still
fails either the magic test (if it is not at physical_len − 64) or the CRC.

**P4 — crash after the step-5 trailer write, before the step-6 barrier.** Two
sub-cases, and they differ:
 (i) The trailer bytes reached stable storage: the file is complete, physical
 length 3072 = committed_file_length, and **it is conforming**. The missing
 barrier is a durability guarantee, not a byte; §2.3's conduct/predicate split
 means a file is never nonconforming for it.
 (ii) They did not: back to P3.
 (iii) A third sub-case only under `[R-LIF-04]`'s overwrite option: if the
 physical file was longer than F′ and the writer had not yet truncated, the
 physical tail is residue, F17 fires, and the file reads as torn. But recovery
 now finds **trail₂** first (at 3008, committed_file_length 3072 = o + 64), so
 truncation lands on the *new* state, not the old one. Correct, and it is the
 reason `[R-LIF-06]` requires the probe to start from the physical end and walk
 backward rather than from any remembered offset.

**P5 — crash after step 6.** Complete and conforming.

The one hazard the document names and does not eliminate: a payload can
deliberately contain a byte string that mimics a trailer, and if such a string
happens to sit at the exact physical end it passes every §6.2 gate. §6.2's note
says it is caught at the directory CRC; §9.6 requires recovery output to be
re-verified as a whole file. Both are stated. I could not construct a case where
that is unsound for a non-adversarial writer.

---

## 5. Byte-divergence catalogue

Identical input arrays, identical stated options (geometry, tiling, layout,
channel names/types/fills, codec and filter selection, metadata content). Every
legitimate way two conforming writers may differ, and whether Appendix G closes
it.

| # | Degree of freedom | Where the document grants it | Closed by |
|---|---|---|---|
| 1 | Placement of every structure | `[R-SLB-05]`, `[R-LIF-02]` step 2 | **G item 3** (total order, contiguous) |
| 2 | Order of structures | same | **G item 3** |
| 3 | Extent of gaps between structures | `[R-SLB-05]`, §5.2 | **G item 3** ("each later structure begins where the previous one ended") |
| 4 | Content of gaps and the pre-trailer pad | `[R-CNT-03]` is a SHOULD | **G item 3** ("every byte of every such gap is zero", advice taken as requirement) |
| 5 | Where the first structure sits when an alignment forbids 16 | `[R-SLB-01]` + `[R-SLB-05]` | **G item 3**'s explicit clause |
| 6 | Record order in the directory | `[R-CNT-14]` ("Record semantics MUST NOT depend on record order") | **G item 3**'s sort key |
| 7 | Sub-record order within a layer record | same | **G item 3** ("within each layer record, its sub-records") |
| 8 | `file_id` | §9.3 (nonzero; randomness a SHOULD) | **G item 2** (hash-derived, fully specified: input = [0,F−64) ‖ trailer[0,60) with file_id zeroed; identifier = digest's last 8 bytes in output order, read little-endian; 1 substituted if all zero) |
| 9 | Number of generations for one logical write | §9 constrains nothing | **G item 4** (one generation) |
| 10 | Whether to declare A / S / A_slab, and their values | §16 leaves it to the writer | **G item 5** |
| 11 | Filter value (1 vs 2) | `[R-COD-09]` | **G item 5** (explicitly) |
| 12 | Codec implementation and encoder settings (block/match/table choices) | `[R-CNF-05]`; §17.2 note; Appendix G item 1's own analysis | **G item 1** (pins implementation + version + level + strategy + thread count) |
| 13 | Unused high bits of a raw DEFLATE stream's final byte | §17.2 note: "This specification constrains them nowhere" | **G item 1**, as §17.2's note itself asserts |
| 14 | Whether a zstd frame carries Frame_Content_Size, and what window it declares | `[R-COD-06]` ("MAY be present"); §18.2 (window unconstrained for documents) | **G item 1** *only if* one reads "fixed encoder settings" as reaching the content-size and window-log flags. Both are ordinary encoder API parameters, so I take it as closed — but item 1 does not name them the way item 5 names the filter. |
| 15 | Storing vs sentinelling an all-fill tile | no rule requires either | **G item 6** |
| 16 | The fill a writer records when the caller chooses none | `[R-TYP-10]` is a SHOULD | **G item 7** (and item 7 correctly notes it also determines *which tiles exist*, via item 6) |
| 17 | `version_minor` | `[R-CNT-26]` is a SHOULD | **G item 8** |
| 18 | Trailer `flags` on a compactor's output | `[R-CNT-08]` obliges carrying input bits forward | **G item 8** (creator writes 0; compactor carries forward — item 8 states the split, and concedes a compactor's output is reproducible only modulo its trailer) |
| 19 | JSON serialization of the user-metadata document (number formatting, escaping, whitespace) | `[R-MTA-05]` explicitly disclaims cross-writer identity | **G item 9** (pins the JSON writer, the storage encoding, and — where encoding 2 — the zstd implementation) |
| 20 | Unicode normalization of names | `[R-ENC-14]` is a SHOULD | **G item 10** |
| 21 | Which of two byte-identical records is placed first | `[R-CNT-14]` | **G item 3** explicitly, and correctly: two records the sort key does not separate are identical in type, flags, lengths, payload and extent content, so either placement yields the same file. I checked this claim and it holds — including the (0,0)-extent case. |

**Divergences I found that Appendix G does not close, and why none of them is a
defect:**

- **Updater capability.** Two updaters given the same input file may produce
  different outputs, because §20.4 keys the MU/PE obligations on *which types the
  updater implements*: an updater that implements an experimental type reads its
  flags from that type's definition, one that does not reads the stored bits, and
  the drop licence can be available to one and not the other. This is outside G's
  scope by construction — item 4 restricts the profile to a single generation and
  says "appending is reproducible only in the weaker sense that the appended bytes
  are". Legitimate, and correctly out of scope.
- **Compactor placement and identity.** `[R-WRT-06]` requires a *fresh draw* for
  `file_id`, which is by definition not a function of content; item 2 says so
  ("a compactor adopting the profile takes `[R-WRT-06]`'s fresh draw instead") and
  item 8 says the output is reproducible only modulo its trailer. Legitimate,
  and named.
- **Whether an absent-metadata caller yields no record or a record holding `{}`.**
  Item 9 says "User metadata either absent, or serialized by a named JSON
  writer…", which enumerates the two profile-compliant states rather than
  choosing between them. In practice "identical stated options" decides it, so I
  classify this as legitimate-and-stated-option rather than an open divergence.

I found **no divergence I could not classify** as either legitimate or forbidden,
and **no claim in Appendix G I could falsify**. The two claims I tried hardest to
break — item 3's tie-breaking argument (§21 above) and item 2's non-circularity
(the hash input is [0,F−64) plus the trailer's first 60 bytes with `file_id`
zeroed, and the trailer CRC is computed afterwards over [0,60), so nothing
depends on its own result) — both hold.

---

## 6. Degenerate but legal files I built or checked

Because rounds 18–21 found their survivors this way, I spent budget on files
nobody would write on purpose.

- **The 128-byte file** (Appendix A): reproduced, trailer CRC 0xE00938D2 ✔.
- **A layer with a dimension of extent 0**: grid count 0, N = 0, entry_count 0,
  extent slot (0,0), crc_of_crc_array 0, zero segments, zero-byte CRC array.
  Everything is stated (§11.1, §15.4's closing example, `[R-CNT-23]`).
- **A slab or alignment declaration on a layer with no stored tiles**: vacuous but
  legal; `[R-SLB-03]`'s "A run with no stored tiles imposes nothing".
- **A layer declaring codec 4 with an enormous tile shape but no addressed
  tiles**: conforming, per §17.2's note, and the escape expires the moment a later
  commit grows an extent — which §20.3 step 4 names (L44).
- **A layer whose one addressed tile has a decoded size of 2⁶³ − 1 bytes.** I
  built this one in full, because it is the sharpest witness for my finding.
  Rank 1, dim `x` with E = 1 and **T = 2⁶³ − 1**; interleaved; one bool channel
  (so Q = 1); codec 1, filter 1. Then G = ⌈1/(2⁶³−1)⌉ = 1, N = 1, P = 2⁶³ − 1,
  and the decoded tile size is P·Q = 2⁶³ − 1 = 8 EiB. Every quantity is *at* the
  `[R-ENC-03]` domain edge and none exceeds it, so `[R-ENC-04]` is satisfied:
  N·P = 2⁶³−1, C·N = 1, entry_count×20 + 4 = 24. `entry_count` = 1 and the single
  entry is the sentinel. The resulting file is **256 bytes**:

```
0000  89 54 41 52 4e 0d 0a 1a 00 00 00 00 00 00 00 00
0010  ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff   <- the sentinel entry
0020  00 00 00 00 3d 9d 38 e5 01 00 03 00 4b 00 00 00      + segment CRC array
0030  10 00 00 00 00 00 00 00 18 00 00 00 00 00 00 00
0040  03 62 69 67 01 01 00 01 00 01 00 00 00 00 00 00
0050  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0060  00 00 00 01 01 00 01 78 01 00 00 00 00 00 00 00
0070  ff ff ff ff ff ff ff 7f 01 62 01 00 01 00 01 01      <- tile extent 2^63-1
0080  00 00 00 00 00 00 00 89 79 d5 d5 50 4a 05 c0 00
0090  … pre-trailer pad …
00C0  8a 4e 52 41 54 0d 0a 1a 01 00 00 00 00 00 00 00      <- trailer, gen 1
…
```
  Nothing is stored, so a read of coordinate x = 0 returns the channel's fill bit
  with **no I/O and no allocation** (`[R-RDR-04]` step 4 short-circuits on a valid
  sentinel). Every structural rule I can find is satisfied. This is a conforming
  256-byte file whose layer declares an 8-exabyte tile. What a conforming reader
  owes on it is the subject of my one finding.

---

## 7. Findings

### writer-01 — AMBIGUITY — §21.9, `[R-ERR-03]` / `[R-ERR-04]` (and `[R-CNF-03]`, §2.3)

**Which tiles the "decoded size of one tile" guarantee ranges over — addressed or
stored — is left open, and it decides whether a reader must accept a
fully-sparse layer with a huge declared tile size.**

Quotation (§21.9, the paragraph following the limits table):

> The last three rows are **per-instance**: they range over the tiles,
> user-metadata documents and compressed frames a file actually contains, and a
> file containing none of a kind does not exceed that row, whatever its
> declarations would derive — a layer addressing no tile (§11.2) has no tile
> whose decoded size the table can bound, exactly as `[R-COD-07]`'s cap is
> quantified over a layer's *addressed* tiles.

And the rule the quantifier feeds, §2.3 `[R-CNF-03]`:

> A reader MUST accept every conforming file of a format major version it
> implements, … and none of whose values exceeds the minimum guarantees of §21's
> limits table

and `[R-ERR-04]`:

> A file exceeding any of these remains conforming, and a reader MAY decline
> it — at the whole file, or at the narrowest scope whose declarations exceed
> what it can serve, a layer or a tile. Software that declines **on that ground**
> a file whose every quantity lies within the table is not a conforming reader
> (`[R-CNF-03]`)

**The two permitted readings.**

*Reading A — "contains" means **addresses**.* The em-dash gloss says "a layer
addressing no tile … has no tile", and closes by pinning the analogy to
`[R-COD-07]`, whose cap the document elsewhere describes as "quantified over a
layer's *addressed* tiles". On this reading a layer that addresses tiles but
stores none still has tiles whose decoded size the table bounds.

*Reading B — "contains" means **stores**.* "the tiles … a file **actually
contains**" is the natural way to say "the tiles physically present in it", and
an unstored tile occupies no byte of the file at all: §3.1 says a tile is stored
"if and only if that generation's tile-index entry for it is not the sentinel",
and §5.2's live committed state contains no bytes for it. The whole point of the
paragraph is to separate rows that range over *instances* from rows that range
over *declarations* — and under Reading A the tile row is itself a
declaration-derived row (both the addressed-tile set and the decoded size come
from declarations alone), which collapses the distinction the paragraph is drawing.

The gloss does not discriminate, because a layer that *addresses* no tile also
*stores* none: the example is true under both readings. Only the trailing
"exactly as `[R-COD-07]`'s cap is quantified over a layer's addressed tiles"
leans toward A, and it is offered as an analogy of form ("exactly as"), not as a
definition of "contains". Nothing else in the document decides it: I grepped every
occurrence of "256 MiB", "actually contains", "per-instance", "minimum
guarantee", "guarantees of §21" and "§21.9", and §24's `[R-VEC-03]` singles out
only the *tile-count* guarantee as not constructible, which is neutral here.

The contrast with the document's own care elsewhere is what makes me confident
this is a gap rather than a style choice. §20.3 step 4 distinguishes the two
quantifiers within a single paragraph and depends on the distinction: "A layer
that stores no tile **in the generation this commit supersedes** MAY be
re-declared freely" versus "`[R-COD-07]`'s lz4 decoded-size cap … which an empty
layer escapes only because that cap is quantified over **addressed** tiles". The
document knows the difference matters and says so twice; §21.9 says "actually
contains".

**Which I picked, and why.** I implemented Reading A — a writer that relies on the
guarantees (`[R-CNF-10]`: "writers MAY rely on those minimums") must assume the
stricter of the two, so my writer keeps every *addressed* tile's decoded size
within 256 MiB even in layers it leaves entirely sparse. That is the safe side
for a writer. It is the wrong side for a *reader*, which is where the fork bites.

**What an implementer does wrong without it.** Take the 256-byte file in §6 above:
one layer, one addressed tile, decoded size 2⁶³ − 1, entry the sentinel, nothing
stored. Or a milder one: extents (8192, 8192), tile extents (8192, 8192), one
float64 channel ⇒ decoded size 512 MiB, entry_count 1, sentinel. Both are
conforming files a few hundred bytes long.

- Reader A (Reading A) observes an addressed tile whose decoded size exceeds the
  256 MiB row, concludes the file exceeds a §21.9 guarantee, and under
  `[R-ERR-04]` declines the **layer** as "the narrowest scope whose declarations
  exceed what it can serve", reporting a resource limit. Reads of that layer
  report failure.
- Reader B (Reading B) observes that the file contains no tile, concludes no row
  is exceeded, and is therefore *obliged* by `[R-CNF-03]` to accept — and by
  `[R-TYP-08]` / `[R-RDR-04]` step 4 to return the channel's fill at every
  position, at zero cost.

Under Reading B, reader A "declines on that ground a file whose every quantity
lies within the table" and is by `[R-ERR-04]`'s own sentence **not a conforming
reader**. Under Reading A, reader A is conforming and reader B is merely
permissive. Exactly one of the two implementations is conforming, and the text
does not say which. Note also that Reading A puts `[R-ERR-04]`'s licence to
decline in direct tension with `[R-TYP-08]`'s "MUST return … that channel's fill
value at every such position" for a tile that costs nothing to serve; Reading B
has no such tension, which is a further argument that B was intended and A is
what the words say.

The fix is one word: "the tiles a file actually **stores**" (with the gloss then
reading "a layer storing no tile has no tile whose decoded size the table can
bound"), or "the tiles a layer **addresses**" if A is intended — in which case
the `[R-COD-07]` analogy should be promoted from an aside to the definition.

**Byte-level: yes.** Two competent implementations reading this text disagree
about the accept/reject verdict on a specific conforming file — reader A refuses
to serve a layer that reader B is obliged to serve — and `[R-ERR-04]`'s closing
sentence makes exactly one of them a conforming reader. It does not turn on a
SHOULD, and it is not a register-row-versus-rule dispute: §21.9 is outside the
register (§21.1 says so explicitly), so §21.1's "the rule governs" tie-breaker
has nothing to break.

---

## 8. Things I checked and found determined

Recording these so the next round does not re-spend the budget.

- Every worked constant and example in the document reproduces (§0's table).
- The register's own arithmetic: 121 conditions / 273 instances, matching §21.8.
  This forecloses a candidate I had built — that the newly-pinned metadata
  content-size constraint (§18.2) deserves its own instances under §21.1's
  magnitude rule the way the tile analogue T22 gets six. §21.1's "family" rule
  ("a row whose check ranges over a family without the condition changing shape
  states that range as a single instance") licenses R3's two, and §21.8's stated
  total confirms two is the intended count. Not a defect.
- Alignment A binds stored-tile offsets only, never index regions or record
  extents (`[R-SLB-01]`).
- The pre-trailer pad's length is determined, and a longer gap is a conduct
  violation rather than a file-conformance one (§2.3, §6.2).
- An appender cannot write into slack (`[R-LIF-01]` freezes [0,F)).
- Residue past F never becomes slack, and no slack total is owed for a file whose
  trailer gate fails (`[R-CNT-21]`).
- §20.3 step 4's bar is quantified on the **superseded** generation's stored
  tiles, and both escape hatches (grow → former padding becomes a real fill
  sample; shrink → new padding whose byte already holds fill) are stated. A
  same-element-size type change (int32 → float32) is *permitted* by the stated
  test, since §14 fixes nothing that changes and `[R-TYP-04]` makes a value its
  bit pattern; bool ↔ uint8 is barred, interleaved by `[R-SER-08]` and planar by
  the decoded size. I convinced myself this is deliberate, not a gap.
- The bar's enumeration omits *pad bits* while its example (c) and §21.7 both
  treat them as covered — but the enumeration is explicitly non-exhaustive ("the
  list names where that effect arises rather than standing on its own"), so the
  general test decides it. Not a defect.
- `[R-MTA-09]`'s enumeration of carried-over frame constraints excludes
  `[R-COD-06]`'s undisclosed-dictionary prohibition (it "references a tile"), so a
  metadata writer is not literally told not to use a dictionary. But a
  dictionary-compressed document that does not decode standalone fires R3 and
  makes the file nonconforming, so `[R-CNF-05]` bars it anyway. No fork.
- `[R-ERR-04]`'s scope list ("a layer or a tile") does not name a record, but
  §18.2 assigns ignore-record expressly for the metadata size and window bounds,
  and §21.5's header carves both out. §21.1's "except where a rule assigns one
  expressly" covers it.
- The MU/PE matrix (§2.2 above) is complete and internally consistent, including
  the appender-versus-compactor asymmetry on malformed index entries and the
  un-appendable conforming file created by an experimental-range top-level MU = 1
  record.

---

*Editorial substitution by the maintainer, recorded per the repository's
vocabulary gate: one ordinary-English use of a reserved word was replaced with
"prior structure". No claim, number or citation in this transcript is affected.*
