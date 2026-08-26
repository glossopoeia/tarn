# Cleanroom round 27 — Writer implementer transcript

**Access.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,549 lines; the brief said 4,550 — a one-line discrepancy I note and did not chase).
I ran `grep`/`awk` against that file only, and Python that reads no files (CRC-32C,
SHA-256, and byte-layout arithmetic). I opened no ADR, no `PLAN.md`, no
`conformance/`, no registry, no git history, no directory listing.

**Unrequested context.** Material appeared in my context before I began: a project
instruction file pointing at `AGENTS.md`, an index of the maintainer's memory files
with descriptive titles, and a `git status` block carrying recent commit subject
lines. I did not open any of it and I have not used any of it as evidence. I name
that it appeared, per the brief, without repeating its contents. One consequence I
should flag honestly: the commit subjects were visible in that block and named
sections. I did not treat them as a map — I read §2.2's prefix table because the
brief told me a list had become a table, not because of anything in that block —
but a reader auditing this run should know the block was present.

---

## Part 1 — Creation: a byte-layout walk

I built a small but non-trivial file end to end and emitted it in the order a writer
actually writes. Every offset below is a real number from a script I ran; I checked
each against hand arithmetic before running it.

### 1.1 The array I am asked to store

One layer, name `a` (1 byte, `61`). Rank 2. Dimensions declared in order
`y` (E=5, T=4) and `x` (E=5, T=4). Interleaved (§14.1). One channel `v`,
type 7 = uint16 (§12.1), fill `0xABCD` (bytes `CD AB`, little-endian per
`[R-ENC-01]`). Codec 1 = none, filter 1 = none. No alignment, no slab.
Plus one file-scope user-metadata record carrying `{"tarn.title":"a"}` under
encoding 1.

Geometry (§11.2, `[R-GEO-03]`): Gᵢ = ⌈5/4⌉ = 2 for both axes, so N = 4, P = 16.
Addressed-tile count = N = 4 (interleaved), so `entry_count` = 4.
Q = ΣBᵢ = 2, decoded size = P·Q = 32 bytes (§14.2, `[R-SER-02]`).

Padding (§11.3, `[R-GEO-04]`): 5 mod 4 ≠ 0 on both axes, so the tiles at the high
edge carry padding positions. Tile (1,1) covers coordinates 4–7 on both axes and has
exactly one real position, (4,4), and 15 padding positions. `[R-SER-05]` fixes their
content: each must encode the channel's recorded fill, `CD AB`. **Fixed by the
document, not by me.**

### 1.2 What the document fixed and what it left to me

| Decision | Fixed by | My choice |
|---|---|---|
| Bytes [0,16) | `[R-CNT-04]`, §6.1 table | none |
| First structure at 16 | `[R-CNT-13]` (offset ≥ 16), §15.3 | none |
| Order of tiles / index / extents | **left open** — `[R-LIF-02]` step 2 "in any order satisfying §5.2's coverage classes"; `[R-SLB-05]` | I followed Appendix G item 3 |
| Position of each structure | **left open** within [16, F−64), disjoint (`[R-CNT-13]`) | contiguous from 16 |
| Directory last before the pad | `[R-CNT-05]` | none |
| Pad length | `[R-LIF-02]` step 5 — to the next 64-byte boundary | none |
| Pad content | **left open** — `[R-CNT-03]` is a SHOULD | zeroed |
| F | forced: pad end + 64, and F mod 64 = 0 (§6.2) | none |
| `generation` | 1 (`[R-LIF-02]` creation path) | none |
| `file_id` | **left open** — nonzero, SHOULD be random (`[R-LIF-03]`) | Appendix G item 2 derivation |
| `flags` | 0 (`[R-CNT-08]`, creator) | none |
| `version_minor` | **SHOULD** be 0 (`[R-CNT-26]`) | 0 |
| `linearization` | 1 (only value, `[R-GEO-05]`) | none |
| `index_encoding` | 1 (only value, §7.4) | none |
| Record order in the directory | **left open** (`[R-CNT-14]`) | layer, then user-metadata |
| Record flags | fixed by §7.3's registry table | none |

Nothing in creation stopped me. Every field I had to emit had either a fixed value or
an explicitly stated freedom.

### 1.3 The layer record's inline payload — 92 bytes

Packed in §7.4's table order with no padding between fields (`[R-CNT-18]`):

```
  0  01 61                    name: length 1, "a"
  2  01                       layout 1 = interleaved
  3  01 00                    linearization 1 = row-major
  5  01 00                    codec 1 = none
  7  01 00                    filter 1 = none
  9  00 x8                    alignment A = 0
 17  00 x8                    slab S = 0
 25  00 x8                    slab alignment 0, forced by S = 0 ([R-CNT-23])
 33  02                       rank d = 2
 34  01 00                    channel count C = 1
 36  01 79 | 05.. | 04..      dim "y": extent 5, tile extent 4      (18 bytes)
 54  01 78 | 05.. | 04..      dim "x": extent 5, tile extent 4      (18 bytes)
 72  01 76 07 00 02 CD AB     channel "v", type 7 = uint16, fill 0xABCD (7 bytes)
 79  01                       index_encoding 1
 80  04 00 00 00 00 00 00 00  entry_count = 4
 88  CD BE C7 32              crc_of_crc_array = 0x32C7BECD
```

2 + 34 (the nine scalars from layout through channel count) + 18 + 18 + 7 + 13 = 92,
no residue, so the sub-record sequence is empty (`[R-CNT-18]`). I cross-checked this
arithmetic against §7.4's own worked example (rank-1 `sst`, 81 bytes) and reproduced
its 4 + 34 + 18 + 12 + 13 = 81 exactly, and its two CRC constants
(`0x80A34955` over the 80 sentinel bytes, `0xC4EE982E` over the 4-byte array)
byte for byte with my own CRC-32C implementation.

### 1.4 Placement and the emitted file

```
[  0,  16)  front signature block                                    16
[ 16,  48)  stored tile, disk ordinal 0        crc 0x1EAC5229        32
[ 48,  80)  stored tile, disk ordinal 1        crc 0x8AB47D1C        32
[ 80, 112)  stored tile, disk ordinal 2        crc 0x1C1C4D28        32
[112, 144)  stored tile, disk ordinal 3        crc 0x39A5407D        32
[144, 228)  tile-index region: 4x20 entries + one segment CRC        84
[228, 250)  user-metadata extent: 18-byte document + terminal CRC    22
[250, 395)  directory: 116-byte layer record + 25-byte UM record + CRC 145
[395, 448)  pre-trailer pad (slack, zeroed)                          53
[448, 512)  trailer                                                  64
                                                              F  =  512
```

Checks I ran before believing it:

- `[R-CNT-17]`: extent_length must equal 4x20 + ⌈4/2¹⁶⌉x4 = 84. ✓ (matches the
  region I emitted; §15.1's unlabelled blockquote gives the same layout — see §1.7.)
- Segment CRC over the 80 entry bytes = `0xCF68D747`; `crc_of_crc_array` =
  CRC-32C over those 4 bytes = `0x32C7BECD`. ✓
- Under codec 1, `[R-COD-04]` forces each non-sentinel entry's length to equal the
  decoded size, 32. ✓
- dir_offset 250 ≥ 16, dir_length 145 ≥ 4, 250 + 145 = 395 ≤ F − 64 = 448. ✓
- F mod 64 = 0. ✓ File size = committed_file_length. ✓
- Pad = 448 − 395 = 53, exactly "to the next 64-byte boundary" from 395. ✓
- `file_id` under Appendix G item 2: SHA-256 over bytes [0, F−64) followed by the
  trailer's first 60 bytes with the file_id field zeroed; last eight digest bytes
  read little-endian → `0x34E1390D8A478BE9`. Nonzero, so no substitution.
  Note this exceeds 2⁶³ − 1 — legal, because §4.2's domain rule covers "every
  offset, length, extent, and count", and `file_id` is none of those; §6.2's table
  constrains it only to ≠ 0. Appendix G item 2 only works because of that.
- Directory CRC = `0x52EAC13F`; trailer CRC over trailer bytes [0,60) = `0x7CEAD775`.

**Write order actually used** (`[R-LIF-02]` creation path): front block; then steps
2–6 beginning at offset 16 — payloads and index region and the metadata extent (any
order, I chose Appendix G's); directory + CRC; **barrier**; pad + trailer with
generation 1; **barrier**. §20.2 is emphatic that both barriers are owed, not one.

### 1.5 What I would have to guess

Only two things, and both are declared open: the *positions* of structures within
[16, F−64), and the *content* of the pad. `[R-CNT-03]`'s zeroing is a SHOULD, whose
stated consequence is "bytes indistinguishable from stale data" and forfeited byte
reproducibility. Neither is a defect.

### 1.6 The degenerate cases I built to test the rules (shape 8)

- **Zero-extent dimension.** E=(4,0), T=(2,2): G=(2,0), N=0, entry_count=0,
  extent slot (0,0), `crc_of_crc_array`=0, no index region at all. `[R-CNT-17]`'s
  formula gives 0 (⌈0/2¹⁶⌉ = 0). §15.4's closing example says exactly this.
  Consistent.
- **Tile extent exceeding the extent.** E=3, T=4: G=1, one padded tile.
  §11.3's "equivalently, where the grid overhangs the extent" is a genuine
  equivalence including at E=0 (G·T = 0 = E, no overhang, no padding). Consistent.
- **Minimum file.** Appendix A's 128-byte file: I recomputed its trailer CRC over
  bytes [0,60) and got `0xE00938D2`, stored `D2 38 09 E0`. ✓ And I confirmed 128 is
  really the floor: dir at 16 with length 4 ends at 20, the trailer must start at a
  64-aligned offset ≥ 20, so 64, so F = 128.
- **P = 1 (all Tᵢ = 1)** and **stride 1**: byte-shuffle degenerates to the identity.
  This is where Appendix G item 5's claim broke — see finding writer-04.

### 1.7 The convention I checked rather than assumed

`[R-CNF-01]` exempts text *labeled* Note, Example or Rationale, not every `>` block.
I enumerated every top-level blockquote in the file with `awk` and filtered out those
carrying such a label. Exactly one unlabelled, non-diagram, non-continuation
blockquote survives: **§15.1's tile-index region layout**

> [ entry array: entry_count × 20 bytes ] [ segment CRC array:
> ⌈entry_count / 2¹⁶⌉ × 4 bytes ]

That block is normative, and I relied on it: it is where the region's two-part
layout is actually stated. It agrees with `[R-CNT-17]`'s formula. (The other
unlabelled blocks are ASCII figures and continuation paragraphs of labelled
Example/Rationale blocks, and Appendix G is non-normative by its own heading.)

---

## Part 2 — The append procedure

### 2.1 Adding to a file I wrote: superseding one stored tile

Second commit against the 512-byte file above, superseding spatial tile 1.

1. **Establish F** — validate the trailer in the final 64 bytes of the *physical*
   file (`[R-LIF-04]`). F = 512. Physical length = 512, so no truncation is owed.
2. **Open** — §19.1's four steps (`[R-RDR-01]`). The appender is a reader here.
3. **Validate what the commit touches** (`[R-WRT-03]`): trailer and the *full*
   directory always, because re-emission relies on every directory byte; §19.3's
   layer validation for layer `a`; and the §19.4 index chain for the one segment
   whose entries I reuse.
4. **Write payloads and indexes**, beginning at exactly F = 512:

```
[512, 544)  new stored tile, disk ordinal 1                          32
[544, 628)  layer a's WHOLE tile-index region, re-emitted            84
[628, 773)  new directory (UM record byte-identical; layer record's
            extent slot and crc_of_crc_array both changed)          145
[773, 832)  pre-trailer pad                                          59
[832, 896)  trailer, generation 2, same file_id                      64
                                                              F2 =  896
```

384 bytes appended to change 2 bytes of one sample. That is §20.3's note about
index cost, exactly.

5. **Re-emit the directory** per §20.4.
6. **Commit**: barrier; pad; trailer with generation 2, the same file_id, unknown
   ignore-lane bits copied forward, version_minor per `[R-CNT-26]`; barrier.

Three of the four index entries are byte-identical at their disk-ordinal positions;
one is re-pointed. `crc_of_crc_array` changes because the segment CRC changed, and
the layer record's extent slot changes because the region moved — which §20.3 says
is *necessarily* a new placement, since `[R-LIF-01]` freezes [0, F).

### 2.2 Adding to a file whose records I do not all understand

Here is the full flag matrix, with what the document permits my updater to do. All
four combinations of MU (bit 0) and PE (bit 1) are reachable in stored bytes, because
`[R-CNT-12]` makes MU=1/PE=0 a *verifier*-detected violation rather than something a
reader refuses.

**Top-level record, type this updater does not implement**

| Stored MU | Stored PE | Effective PE | Reader outcome | What my updater may do |
|---|---|---|---|---|
| 0 | 0 | 0 | ignore-record (`[R-CNT-15]`) | retain byte-identical, **or** drop it under §20.4's independence test (see writer-03) |
| 0 | 1 | 1 | ignore-record | retain byte-identical, extent content unmodified; may **not** relocate the extent — that is compaction's operation only (`[R-WRT-08]`) |
| 1 | 0 | 1 (`[R-CNT-12]`) | reject-file (`[R-CNT-15]`) | **no commit is available at all** — the updater is a reader first |
| 1 | 1 | 1 | reject-file | no commit available |

**Layer sub-record, type this updater does not implement**

| Stored MU | Stored PE | Effective PE | Reader outcome | What my updater may do |
|---|---|---|---|---|
| 0 | 0 | 0 | ignore-record (`[R-CNT-18]`) | retain, or drop only in a commit that independently changes *that layer's* record, the entry set of its index, or which of its tiles are stored |
| 0 | 1 | 1 | ignore-record | retain byte-identical |
| 1 | 0 | 1 | reject-layer (`[R-CNT-18]`) | may not modify that layer; **other layers stay editable**; the file itself is not refused where it is otherwise conforming |
| 1 | 1 | 1 | reject-layer | as above |

**Types this specification registers** (0x0001 layer, 0x0002 user metadata): §7.3's
registry flags govern, not the stored bits (`[R-CNT-22]`). Both carry PE = 1, so
neither can ever be dropped; no commit removes a layer record or a user-metadata
record at either scope. A stored bit that disagrees with the registry is a
verifier-detected violation (F28, L49) and changes no reader behavior.

**A type the updater implements that this document does not register**: the private
definition supplies the flags and the stored bits never do (§20.4). I checked the
consequence: a tool that does *not* implement that type reads the stored bits
instead, so two conforming updaters can disagree about droppability. Both output
files are conforming, and §10.3 already bars such values from circulating, so I do
not report it.

**Write order, durability, commit point.** Steps 1–3 (payloads, index regions,
record extents, directory + CRC) must be durable before step 5 writes the pad and
trailer; step 6 makes the trailer durable. The pad's durability is not separately
owed and does not matter: the pad is slack and its content is unconstrained, so a
torn or hole-filled pad under an intact trailer is still a conforming file.

The commit point for a *reader* is later than the commit point for the writer: a
reader takes the trailer at the **physical** end of file, so the new generation
becomes visible only when the trailer is at the physical end *and* the physical
length equals committed_file_length. `[R-LIF-04]` puts the truncation "no later than
step 6" for a writer that chose to overwrite rather than truncate first, so the
window between the trailer landing and the truncation is a window in which a
fully-written generation is still unreadable. That is stated, not a gap.

### 2.3 A malformed index entry met while re-emitting

§20.3 step 2 is explicit and I followed it: an entry that §15.3 would classify
reject-tile is **carried forward byte-identically at its disk-ordinal position**, not
repaired to a sentinel. My updater therefore knowingly writes fresh bytes that carry a
violation, and the resulting file is nonconforming — and my updater is still
conforming, because "reproducing a structure's bytes unchanged is not authoring
them". I checked that this does not collide with `[R-WRT-06]`: the compactor's
"MUST NOT emit a file carrying a violation it has detected" is an expressly different
rule for an expressly different actor, and §20.5 spells out that a compactor must
refuse in exactly this case because a structurally-rejected entry gives it no extent
to re-point.

I also checked that my appender need not *detect* it: `[R-WRT-03]`'s verification
depth reaches the index **chain** (`crc_of_crc_array`, segment CRCs) but not §15.3's
per-entry classification. So the carry-forward is not a knowing emission of a
detected violation. Consistent.

---

## Part 3 — Slack, per shape of commit

| Commit shape | Bytes that become slack | Who counts them | Permitted content |
|---|---|---|---|
| **Append, new layer** | the prior directory, its pad, its trailer — sized by the file's layer count, never by any layer's data | a verifier that reaches a live state, as a **total** (`[R-CNT-21]`); readers never | unconstrained; SHOULD be zeroed only for gaps the writer *creates* (`[R-CNT-03]`) |
| **Append, tiles added or superseded** | the prior index region of every touched layer, every superseded payload, plus the prior directory/pad/trailer | same | same |
| **In-place update** | *does not exist*. `[R-LIF-01]`: every conforming mutation is a commit or a whole-file rewrite | — | — |
| **Whole-file rewrite (new file_id)** | nothing in the new file; the old file persists untouched as a separate artifact | — | — |
| **Compaction** | nothing carried; the output's only slack is its own alignment gaps and its own pre-trailer pad | verifier of the output | same |
| **Abandoned partial write** | **no slack total is owed at all.** §5.2: where §6.2's ordered validation rejects before a live trailer is established there is no F and no live state to walk; the verifier reports the trailer failure and nothing about slack | — | — |

Numbers from my own gen-2 commit: superseded structures = old index 84 + old
directory 145 + old pad 53 + old trailer 64 + superseded payload 32 = 378. New
pre-trailer pad = 59. Total slack = 437. I checked this against §9.7's walk
independently: live claimants = front 16 + three retained tiles 96 + new tile 32 +
new index 84 + metadata extent 22 + directory 145 + trailer 64 = 459; F2 − 459 = 437.
The two agree exactly.

One place slack content *is* constrained: `[R-CNT-05]` forbids a **structure** in the
pre-trailer gap (F7). I checked this is not a contradiction with "slack content is
unconstrained": a live structure's bytes are by definition claimed and therefore not
slack, so F7's condition is about a live claimant sitting in that region, and
`[R-CNT-05]` then "counts the rest as slack". Coherent.

A partial total (`[R-CNT-21]`) is F less the bytes claimed by the claimants the walk
did enumerate — an upper bound, never an under-count — and the verifier must say
which scope or violation stopped the walk. I confirmed the discarding rule: where the
walk itself established a layer-scope rejection (L18, L40–L42), the claimants it had
already enumerated for that layer are discarded, which is what keeps the figure an
upper bound rather than an arbitrary one.

---

## Part 4 — Torn-write recovery, five crash points

**(1) Crash during creation, after the front block only.** File is 16 bytes.
Next reader: `[R-CNT-27]` — shorter than 128 — reject-file. Next updater: cannot
establish F (`[R-LIF-04]`), no append. §9.6's probe begins at the largest 64-aligned
o with o + 64 ≤ physical length; there is none, so no candidate. Nothing to recover;
the caller starts over. Not conforming in the meantime.

**(2) Crash mid-step-2 of a commit (payloads partially appended).** Physical tail is
not a trailer. Reader: reject-file, "torn or invalid", and MUST NOT scan backward
(`[R-LIF-05]`). Updater: no append; recovery is the deliberate separate operation of
§9.6, which probes back to trailer *n* and truncates to it, restoring generation *n*
exactly. Not conforming in the meantime. The window is one in which the old state is
*recoverable*, not *readable* — §9.2's example says so in as many words.

**(3) Crash after step 3 (directory durable) but before step 5.** Identical reader
and updater behavior to (2). This is the case `[R-LIF-07]`'s checkpoint-commit SHOULD
exists for: recovery has to scan back across the whole appended run.

**(4) Crash *during* the trailer write in step 5.** Three sub-cases, all reject-file:
magic torn → F8; magic intact, CRC torn → F14; both intact but the physical file is
short of committed_file_length → F17. §9.6's probe requires both the trailer CRC to
verify *and* committed_file_length = o + 64, so a half-written trailer is never
mistaken for a commit state.

**(5) Crash after step 5's trailer write, before step 6's barrier or before
`[R-LIF-04]`'s truncation.** If everything reached stable storage the file is
conforming and the commit stands. If the trailer reached storage but the truncation
did not, the physical file is longer than F_new, residue past the trailer, and a
reader meets it as a trailer that fails its gates — §9.5's Note is explicit that
residue carries no register row of its own and that the observable state is already
named. Recovery here can legitimately land on the *new* trailer: the probe from the
physical end finds o = F_new − 64 with committed_file_length = o + 64, so truncating
to it produces the newer generation. I confirmed the probe cannot be fooled into
preferring the older one — it takes the nearest-to-end valid candidate.

**A payload that mimics a trailer.** §21.6 records this as inert under live-state
coverage (nothing enumerates slack), and §9.6 makes re-verification of recovery output
normative. I checked the mimic can also sit at exact physical end of file and pass
§6.2's gates; §6.2's Note says it is then caught at the directory CRC.

---

## Part 5 — Byte-divergence catalogue

Given identical input arrays and identical stated options (tiling, layout, codec,
channel declarations, metadata content are inputs, per Appendix G item 2's own
framing), here is every way I could find for two conforming writers to differ, and
whether Appendix G closes it.

| # | Degree of freedom | Governing text | Closed by |
|---|---|---|---|
| 1 | Encoder output for codecs 2–4 (block/match/table choices; DEFLATE's up-to-seven unused final-byte bits) | `[R-CNF-05]`; §17.2's Note | item 1 (pin implementation + version + settings, thread count included) |
| 2 | `file_id` | `[R-LIF-03]` (SHOULD random) | item 2 (hash derivation), creator only |
| 3 | Placement of every structure | `[R-LIF-02]` step 2, `[R-SLB-05]` | item 3 (contiguous from 16, in a total order) |
| 4 | Order of records in the directory | `[R-CNT-14]` (order carries no meaning) | item 3 |
| 5 | Order of a layer record's sub-records | `[R-CNT-14]`, §7.4 | item 3 |
| 6 | Order of record *extents* | `[R-LIF-02]` step 2 | item 3 (top-level first, then per-layer sub-records) |
| 7 | Gap **extent** (how much space between structures) | `[R-SLB-05]` | item 3 |
| 8 | Gap **content** | `[R-CNT-03]` (a SHOULD) | item 3 (zero, taken as a requirement) |
| 9 | Number of generations | §9 constrains none | item 4 |
| 10 | Declared alignment A / slab S / A_slab | §16 leaves to the writer | item 5 |
| 11 | Declared filter value | §17.3 leaves to the writer | item 5 |
| 12 | Whether an all-fill tile is stored | no rule requires the sentinel | item 6 |
| 13 | Fill recorded when the caller chooses none | `[R-TYP-10]` (a SHOULD) | item 7 |
| 14 | `version_minor` | `[R-CNT-26]` (a SHOULD) | item 8 |
| 15 | `flags` beyond the mandated 0 | `[R-CNT-08]` | item 8, creator only — **see finding writer-02** |
| 16 | JSON serialization of the metadata document (number formatting, whitespace) | `[R-MTA-05]` closes member *order* only | item 9 (pin the JSON writer; and the zstd implementation at encoding 2) |
| 17 | Unicode normalization of names | `[R-ENC-14]` (a SHOULD) | item 10 |

I then tried to break the catalogue by finding an eighteenth. Things I checked and
found already determined, not free:

- **Stored length under codec 1** — `[R-COD-04]` forces equality with the decoded size.
- **`entry_count`, `extent_length`, `crc_of_crc_array`, the extent slot of an empty
  layer** — all forced by `[R-CNT-17]`/`[R-CNT-23]`.
- **The all-sentinel segment CRC shortcut** (`[R-IDX-05]`) — produces the same four
  bytes whether computed or substituted, so it is not a divergence. I verified the
  constant: CRC-32C of 2¹⁶ sentinel entries is `0xEECB3BB2`. ✓
- **Pre-trailer pad length** — forced by `[R-LIF-02]` step 5; a longer gap is
  conforming but no conforming commit produces one, which `[R-CNF-02]` names
  expressly.
- **F itself** — forced once the directory's end is fixed.
- **Which tiles must be stored** — a tile with any non-fill real sample must be
  stored (an unstored tile reads as *all* fill), and item 6 forces the converse.
- **Item 3's tie-breaking claim** — "Two records this key does not separate are
  byte-identical in type, flags, lengths, payload and extent content; emitting them
  in either order yields the same file". I tested this. Ties are impossible among
  layer records (unique names), impossible among user-metadata records (multiplicity
  is 1 per scope, and different layers' sub-records live in different sequences), so
  ties arise only among records of an unassigned type — and there the claim holds,
  because their extents have equal length and equal content, so swapping them
  permutes nothing observable. The claim survives.
- **Item 2's derivation** — no circularity: the hash input is [0, F−64) plus the
  trailer's first 60 bytes with the file_id field zeroed, and both are fully
  determined before file_id is chosen. The trailer CRC is computed afterwards over
  the real value. Well defined.

**Claims in the reproducible-writer material I tried to falsify.** Item 3's
tie-breaking claim survived. Item 5's identity claim did **not** — see writer-04.
Item 6's "a tile whose samples all equal fill" uses *sample* where a planar tile
carries only one channel's values and no complete sample; I censused the document's
own use of "sample" (§12's "sample type" is per-channel, §21.7's "wrong sample
values", §14.1's "sample-major") and concluded the loose reading is the document's
own practice, so I do not report it.

---

## Findings

### writer-01 — CONTRADICTION — §22.2 `[R-SEC-02]` forbids the allocation §14/§17 require

`[R-SEC-02]`'s closing MUST NOT and its own opening sentence cannot both be obeyed.

The opening sentence:

> Decoded tile size is a function of the layer's declarations alone (§14.2, §14.3),
> so a reader allocates from geometry and never from a length embedded in a payload

The closing sentence of the same requirement:

> A reader MUST NOT size an allocation, fetch, or index walk in proportion to a
> declared magnitude it has not corroborated against the file's actual length: a
> layer can declare 2⁶³ − 1 addressed tiles, and the declaration alone costs nothing
> to state.

A tile's decoded size **is** a declared magnitude, and under codecs 2–4 nothing
corroborates it against the file's actual length. §17.2 says so directly: "For the
compressing codecs (2–4), no bound relates a stored length to its decoded size in
either direction". `[R-SER-07]` makes the allocation mandatory in the other
direction: "readers allocate from those declarations, not from stored data".

The witness is a small conforming file. Rank 1, dimension `x` with E = T =
200,000,000; interleaved; one uint8 channel with fill `0x00`; codec 3. Then P =
2×10⁸, Q = 1, decoded size = 200,000,000 bytes = 190.7 MiB. N = 1, so entry_count = 1
and the index region is 24 bytes. One stored tile, a zstd frame of a couple of
hundred bytes with a declared window of 8 MiB. The whole file is well under 512
bytes. Every quantity lies **within** §21.9's table: rank 1 ≤ 32, C 1 ≤ 4096,
entry_count 1 ≤ 2³², 1 layer ≤ 65,536, dir_length ≪ 16 MiB, decoded tile 190.7 MiB ≤
256 MiB, no user-metadata document, `Window_Size` 8 MiB ≤ 8 MiB. So `[R-CNF-03]`
obliges every conforming reader to accept it, `[R-MDL-02]` obliges it to return the
samples bit-for-bit, and `[R-ERR-04]` says software that declines it *on resource
grounds* "is not a conforming reader". Serving it requires a ~190 MiB allocation
sized in proportion to a declared extent that the 512-byte file corroborates not at
all.

The two readings an implementer can defend:

1. **Narrow.** The MUST NOT is about magnitudes that purport to describe *file
   content* — entry counts, extents, lengths — which the rule's own example and its
   following Note are entirely about ("The index is the cheapest hostile amplifier:
   entry_count is one `u64`, and `[R-CNT-17]`'s cross-check ties it to the region's
   declared length while `[R-CNT-13]` ties that length to the file's actual size").
   Decode buffers are exempt because §14 derives them from geometry by design.
2. **Literal.** "a declared magnitude" means any declared magnitude, decoded tile
   size included, and a reader must refuse to allocate for such a tile.

I pick (1): it is the only reading under which §22.2's own first sentence,
`[R-SER-07]`, and `[R-CNF-03]` all hold. But the text does not say it, and reading
(2) is what the words state. An implementer taking (2) builds a reader that fails a
conforming file it is obliged to serve, and reports the failure as a *validity*
error rather than a resource one, which `[R-ERR-04]` singles out as the mistake that
"invites the deletion of intact data".

The repair I would make: bound the MUST NOT to magnitudes describing bytes the file
claims to contain — offsets, lengths, extents and entry counts — and say expressly
that decoded sizes are exempt because §21.9's per-tile guarantee, not the file
length, is what bounds them.

**Byte-level: yes.** The disputed file is conforming. Reader A (narrow) accepts it
and returns its 2×10⁸ samples; reader B (literal) must refuse the tile because it
may not size the buffer, and cannot reach for `[R-ERR-04]`'s resource decline
because every quantity is inside §21.9's table. Two conforming readers reach opposite
accept/reject verdicts on the same conforming file — which is precisely what the
gate's discriminating question asks about.

### writer-02 — AMBIGUITY — may an appender originate an ignore-lane flag bit?

`[R-CNT-08]` (§6.3):

> In this specification's text no flag bits are defined: a writer creating a file
> under this text MUST write flags = 0, but a set ignore-lane bit is not a
> file-conformance violation — such bits are defined by later minor versions, and
> files carrying them are conforming files this text's readers ignore. A compactor,
> though its output is a new file, carries the input's unknown ignore-lane bits into
> its output trailer rather than writing flags = 0 (§20.5, `[R-WRT-06]`). An updater
> MUST copy forward unknown ignore-lane bits of the file it modifies and MUST NOT
> clear them

The MUST that pins `flags` to 0 is scoped to "a writer **creating a file**". The very
next sentence treats a compactor as needing an express exception *because* "its
output is a new file" — which shows the drafters read "creating a file" as producing a
new file. An appender does not produce a new file. Its only stated flags obligation is
to copy forward unknown ignore-lane bits and not clear them. Nothing I can find says
it must set no *further* ones.

Two defensible readings:

1. **Strict scope.** `flags = 0` binds creators (and, but for the exception,
   compactors). An appender may set an ignore-lane bit of its own; §21.6 makes the
   resulting file conforming ("An ignore-lane flag bit (16–31) is set | Ignored; the
   file is conforming").
2. **Exhaustive step 6.** §20.3's step 6 enumerates the appended trailer —
   "trailer with generation one greater, the same file_id, unknown ignore-lane flag
   bits copied forward (`[R-CNT-08]`), and version_minor per `[R-CNT-26]`" — and that
   enumeration is a complete specification of the flags field, so the appended
   trailer's flags are exactly the input's.

I pick (2), because originating a bit that names a feature no minor version has
defined is incoherent with §6.3's own account of what those bits are for. But (2)
rests on reading an enumerative clause as exhaustive, which the text does not say,
and (1) is what the scoping words state.

What it costs an implementer: an appender written to (1) can emit a trailer with an
ignore-lane bit that means nothing, and `[R-WRT-06]` then obliges every later
compactor to propagate it forever. A verifier cannot flag it, because the file is
conforming under both readings.

**Byte-level: yes, narrowly.** The disputed file — an appended generation whose
trailer carries an ignore-lane bit absent from its input — is conforming. Creators
must write `flags = 0`, and a compactor may only carry bits forward, so under reading
(2) *no* conforming actor can originate such a bit and that trailer is unreachable;
under reading (1) an appender can. Two conforming appenders given the same input and
instruction emit trailers differing in `flags`, at trailer offset 12, and in the
trailer CRC at offset 60.

### writer-03 — AMBIGUITY — §20.4: does *adding* a top-level record license dropping a PE = 0 record?

§20.4's MU = 0, PE = 0 row:

> Retain byte-identical, or drop it — its extent becoming slack. An appender MUST NOT
> drop it except in a commit that *independently* changes the scope the record
> attaches to: for a layer sub-record, that layer's record, the entry set of its
> index, or which of its tiles are stored; for a top-level record, the file's layer
> set, any layer record's content, or another *non-layer* top-level record. A commit
> changes the layer set by adding a layer; an appender never removes one
> (`[R-CNT-22]`, §7.3). ... Dropping the record, or dropping another record in the
> same commit, is not itself such a change, so a commit whose only effect would be
> the drop MUST retain it.

The rule tells me what *adding* does for the first qualifying item ("A commit changes
the layer set by adding a layer") and what *dropping* does for the third ("dropping
another record in the same commit, is not itself such a change"). It is silent on
**adding** a top-level non-layer record — a commit that attaches a file-scope
user-metadata record to a file that previously had none.

1. **Set reading.** The third item is parallel to the first: what qualifies is a
   change to the file's non-layer top-level record population, additions included.
   Adding a metadata record licenses the drop.
2. **Individual reading.** The first item names a *set* ("the file's layer set") and
   the third names an *individual record* ("another non-layer top-level record").
   Changing a record presupposes a record that exists before and after. Adding one
   changes no existing record, so the drop is barred.

I pick (1), on the rule's stated purpose — the drop must not be the commit's only
effect, and adding a record is independent work — but (2) is the better fit to the
words, and the deliberate-looking asymmetry between "layer *set*" and "another
*record*" is evidence for it.

An implementer taking (2) must retain a PE = 0 record whose owner asked to remove it,
in a commit that is doing plenty of other work; one taking (1) drops it. Both files
are conforming; the SHOULD-report is the only thing that keeps the loss visible
either way.

**Byte-level: yes, narrowly.** The disputed file — generation *n+1* of a specific
input, carrying the new metadata record and *not* carrying the dropped one — is a
conforming file. It is producible only by an appender (a creator emits generation 1
with a fresh file_id, and a compactor produces a different byte sequence entirely),
and only reading (1) permits an appender to produce it. Two conforming updaters given
the same file and the same instruction emit different directories and therefore
different `dir_length`, different trailer, different F.

### writer-04 — OBSERVATION — Appendix G item 5's universal is falsified by a legal tile

Item 5:

> The filter is the identity exactly where its permutation is — where the stride is
> 1, as for a packed boolean plane, and equally where the decoded image is a single
> group, n = L/s being 1 (`[R-COD-10]`); elsewhere it changes the stored bytes of
> every tile it touches.

The first half is correct and I verified it: `[R-COD-10]` places byte *i* of group
*j* at offset i·n + j, which equals the original j·s + i for all i, j exactly when
s = 1 or n = 1 (at s ≥ 2, n ≥ 2, take i = 0, j = 1: the shuffled offset is 1 and the
original is s).

The closing universal is false. Take an interleaved layer, one uint16 channel with
fill `0x0000`, tile extents giving P = 2, so Q = 2, L = 4, s = 2, n = 2 — neither
degenerate case. Let the tile hold values `0x0100` and `0x0001`, decoded image
`00 01 01 00`. Neither value is fill, so item 6 stores the tile. Shuffling: group 0 is
(`00`,`01`), group 1 is (`01`,`00`); the outputs land at offsets 0, 1, 2, 3 as `00`,
`01`, `01`, `00` — the input unchanged. Under codec 1 the stored bytes are identical
with and without the filter. Any image whose byte *i* of group *j* already equals byte
*j* of group *i* is such a case, and nothing forbids one.

This is confined to a non-normative appendix and changes no prescription: item 5
requires the filter value to be pinned regardless, and a writer that left it unpinned
would emit a different `filter` field in the layer record anyway, so the file differs
whether or not any tile's bytes do. I report it because Appendix G's claims are what
an adopter reasons from, and this one is refutable in four bytes.

**Byte-level: no.** No conforming file's bytes turn on it, and no accept/reject
verdict moves; the profile's requirement to pin the filter is unaffected.

---

## Things I checked and did not report

Recorded so the reasoning can be audited rather than repeated.

- **§21's counts.** I counted the register mechanically: 36 + 49 + 26 + 10 = 121
  conditions, and — applying §21.1's own rule that instances are semicolon-separated
  and a cell reading `—` is one instance — 277 instances. §21.8 says "121 conditions
  over 277 instances". Exact match.
- **§2.2's list-to-table conversion.** I extracted every `R-XXX-` prefix used
  anywhere in the document: CNF, CNT, COD, ENC, ERR, EXT, GEO, IDX, LIF, MDL, MTA,
  PRV, RDR, SEC, SER, SLB, TYP, VEC, WRT — nineteen, exactly the nineteen rows of the
  new table, no additions and no losses. I also checked identifier numbering for gaps
  and found none (SER-04 appears only in its withdrawal note; ENC-100 only as §2.2's
  own example).
- **Every CRC constant in the document.** `CRC-32C("123456789") = 0xE3069283`;
  `CRC-32C()` of zero bytes `= 0x00000000`; §7.4's `0x80A34955` and `0xC4EE982E`;
  §15.4's `0xEECB3BB2`; Appendix A's `0xE00938D2`. All five reproduce.
- **Every worked numeric example.** §7.4's 81-byte payload; §11.2's grid; §11.4's
  ordinals (s = 10, in-tile 11,452, planar disk ordinal 74); §14.2's three offset
  walks; §14.3's `55 01` / `55 FD`; §14.5's 32-byte edge tile; §15.4's
  1,000,000-entry layout down to the byte; §17.3's shuffle of three float32s;
  §20.3's 644-byte index; §21.9's 256 KiB and 4 MiB CRC-array figures. All correct.
- **`[R-CNF-13]`'s reach derivation.** I counted `[R-CNT-06]`'s conditions and got
  twelve, less the version gate and the flag gates (which §21.2 attributes to
  `[R-CNT-07]` and `[R-CNT-08]`) = ten, matching "`[R-CNT-06]` states ten". I then
  checked which of §21.2's 36 rows assert an invariant `[R-CNT-24]` fixes and derived
  exactly F8, F14, F6 and both F1 instances — matching the preamble's claim, with F13,
  F15, F17 and F19 all falling inside the 48 trailer bytes a future major may
  redefine, and F5 resting on major-1's directory minimums.
- **`[R-SLB-05]`'s scope.** Its antecedent is "A layer that declares neither
  alignment nor a slab", yet §16.2, §19.4 and Appendix G cite it for a *slab-declared*
  layer's inter-run placement. I decided this is citation looseness with no
  consequence: absence of a constraint is freedom, and `[R-SLB-03]` states expressly
  that "The runs themselves are not mutually ordered or joined". Nothing is
  under-determined.
- **§16 has no owning-scope sentence** where §§11–15, §17 and §18 all do, and
  `[R-CNF-08]` says every structure's scope is "stated in the section that defines the
  structure". I traced every alignment/slab condition and found each assigns its
  outcome expressly (L20, L28, L29, L39, L40, L41, L42, all reject-layer via
  `[R-CNT-23]`, `[R-SLB-01]`, `[R-SLB-03]`, `[R-SLB-04]`), so nothing turns on it.
- **§20.3 step 4's bar list versus its general test.** The list names "the byte
  offset of any **sample** within the decoded tile image", but permuting two
  equal-sized interleaved channels moves each channel's in-sample offset Fᶜ while
  leaving the *sample's* offset (k div C)·Q untouched. The change is still barred by
  the general test — §14.1 fixes which channel a tile's values belong to — and the
  rule says outright that "the list names where that effect arises rather than
  standing on its own". Not a defect.
- **Growth versus the bar.** A growth turning padding positions real changes "the
  set of padding positions", an item in the bar's list, yet growth is expressly
  permitted two sentences later. Resolved by the same "not standing on its own"
  clause plus the express MAY. I also checked the grammar of "A layer that stores no
  tile ... MAY be re-declared freely ... **and** an extent MAY grow": the second
  clause has its own subject and is general, which the justification ("a position
  that becomes real held that channel's fill") forces.
- **§13.3's sparse-writing Note** triggers index re-emission on "changes a layer's
  stored-tile set, or ... grows its extents so that entry_count changes", where
  §20.3 normatively says "stored-tile set **or index content**" — which also catches a
  *shrink* and an ordinal renumbering at constant entry_count. The Note is labelled and
  is not offered as exhaustive; §20.3 governs and is correct.
- **§20.5's "regenerates each relocated tile-index region"** keys regeneration to the
  *region's* relocation, but a region whose own placement is unchanged while its
  tiles moved must still be regenerated. `[R-WRT-07]`'s "The output's reference arrays
  MUST equal the live generation's bit for bit" and `[R-CNT-13]`'s ownership rules
  force the correct behavior, so no conforming output diverges.
- **§19.2's "no earlier, since the open fetches no extent"** could be read as
  forbidding early detection, which `[R-RDR-02]`'s own "A reader MAY detect any
  violation earlier" contradicts; the permissive reading is forced by the immediate
  context.
- **`[R-CNF-02]`'s "the cases this text states" (two).** I derived the class —
  writer MUSTs whose violation is expressly not a file-conformance violation — and
  found exactly the two named (§6.3's flags = 0 against a set ignore-lane bit; §6.2's
  over-long pre-trailer gap). §10.3 and §18.3 are the separate *conduct* category the
  preceding sentence names; `[R-COD-10]`'s stride and `[R-COD-06]`'s undisclosed
  dictionary are violations that merely lack a witness (§21.7).
- **`[R-CNT-19]`/§4.5's "exactly one checksum".** I walked every field of every
  structure: trailer, directory region, index entries, segment CRC array,
  `crc_of_crc_array`, stored tiles, user-metadata extents, sub-record headers and
  payloads, and the extents of unassigned types. Three terminal checksums, three
  interior ones, two exceptions. The claim holds.
- **§17.2's "Three frame features are excluded"** admits two plausible partitions
  (dictionary + dictionary ID + content checksum; or dictionary + content checksum +
  oversized window) both totalling three. The sentence carries no normative force of
  its own — the MUSTs that follow do — so I do not report it.
- **`[R-MTA-09]`'s Window_Size arithmetic.** "a frame declaring more than the reader
  admits" implies the frame exceeds 8 MiB, because the reader's bound is "no smaller
  than §21.9's guarantee". Correct. The Single_Segment_Flag argument is also correct:
  under SSF, RFC 8878 makes Window_Size the content size, which §18.2 pins to the
  decoded length, so a >8 MiB document framed that way exceeds the Window_Size row
  and a Window_Descriptor is the writer's escape.
- **`[R-COD-07]`'s empty-layer escape.** A layer addresses no tile iff some Eᵢ = 0
  (Gᵢ ≥ 1 whenever Eᵢ ≥ 1, and C ≥ 1), so §17.2's Note — "which takes every
  dimension's extent nonzero" — is exactly right.
- **`[R-COD-10]`'s "L is divisible by s in every case".** Planar numeric: L = P·Bᶜ,
  s = Bᶜ. Interleaved: L = P·Q, s = Q. Packed bool: s = 1. Holds.
- **§17.2's "Decoded output is never empty".** P ≥ 1 and Q ≥ 1 and Bᶜ ≥ 1 and
  ⌈P/8⌉ ≥ 1, so every decoded size is at least 1 byte. Holds.
- **§22.3's "Four residues"** — I counted four in that paragraph. Holds.
- **`[R-ERR-04]`'s "the two capability refusals §21.6 names"** — §21.6 names exactly
  two *structural* cases, and a resource decline of an over-guarantee file is a third
  kind expressly excluded by the qualifier. Holds.

**Confidence.** An implementation built from this document alone would interoperate.
Everything a creator, appender and compactor must emit is determined; what is left
open is left open on purpose and named as such; and the reproducible-writer profile
closes all seventeen freedoms I could find. The one place I would expect two
independently-built readers to diverge on a conforming file is writer-01.
