# Cleanroom round 6 — writer

Protocol: ADR-0034. Access rule: `spec/tarn.md` only.

## Walk

## WRITER IMPLEMENTER'S WALK — TARN, spec/tarn.md only

Access disclosure: I read `spec/tarn.md` and nothing else. No docs/, no
conformance/, no registry.json, no git history, no web. Every constant below I
recomputed myself rather than taking on the document's word; the three I could
check independently all agree with the text (see "Constants I verified").

---

### 0. Constants I verified before writing a byte

Implementing §4.5 `[R-ENC-09]` (CRC-32C, reflected, init 0xFFFFFFFF, final XOR
0xFFFFFFFF) I reproduced all three self-checks the document offers:

- CRC-32C("123456789") = 0xE3069283 — §4.5 check vector. Matches.
- CRC-32C(zero bytes) = 0x00000000 — §4.5. Matches (init XOR final).
- CRC-32C of 2^16 sentinel entries (`FF x16 00 x4` repeated 65,536 times) =
  0xEECB3BB2 — §15.4 `[R-IDX-05]`, Appendix B. Matches.
- Appendix A's trailer: CRC-32C over bytes [0,60) of that trailer = 0xE00938D2,
  which is exactly what Appendix A stores at [124,128). Matches.

I also re-derived every worked example in §11.2, §11.4, §12.3, §14.2, §14.3,
§14.5, §15.4, §16.2, §17.3 and §20.3 and found no arithmetic error. And §21.8's
claim — "125 conditions over 244 named instances" — is exactly right: §21.2/3/4/5
carry 39+50+26+10 = 125 rows, and counting semicolon-separated instance cells
(a cell reading "—" counting as one, per §21.1) gives 61+100+45+38 = 244.

That is an unusually clean substrate. The findings below are about the seams,
not the arithmetic.

---

### 1. The minimal file I emit — 128 bytes, field by field

This is the empty file of §5.1 / Appendix A. It is the creator path of §9.2
with zero layers: front block, a directory that is only its own CRC, the
pre-trailer pad, the trailer.

```
off  len  field                          value                       cite
0    8    front signature magic          89 54 41 52 4E 0D 0A 1A     §6.1
8    8    front signature reserved       00 x8                       §6.1
16   0    record sequence (empty)        —                           §7.2
16   4    directory CRC-32C              00 00 00 00 (CRC of 0 bytes)§7.1 [R-CNT-11]
20   44   pre-trailer pad (slack)        00 x44 by advice            §6.2 [R-CNT-05], [R-CNT-03]
64   8    trailer magic                  8A 4E 52 41 54 0D 0A 1A     §6.2
72   2    version_major = 1              01 00                       §6.2
74   2    version_minor = 0              00 00                       §6.3 [R-CNT-26]
76   4    flags = 0                      00 00 00 00                 §6.3 [R-CNT-08]
80   8    generation = 1                 01 00 x7                    §9.3 [R-LIF-03]
88   8    dir_offset = 16                10 00 x7                    §6.2
96   8    dir_length = 4                 04 00 x7                    §6.2
104  8    committed_file_length = 128    80 00 x7                    §6.2, §5.1 [R-CNT-01]
112  8    file_id (nonzero, random)      §9.3 SHOULD cryptographic   §9.3 [R-LIF-03]
120  4    trailer reserved               00 00 00 00                 §6.2, §6.3 [R-CNT-24]
124  4    trailer CRC-32C over [64,124)  computed                    §6.2, §8.1
```

F = 128, a multiple of 64, trailer at the 64-aligned offset 64. dir_offset 16 ≥
16, dir_length 4 ≥ 4, dir_offset+dir_length = 20 ≤ F−64 = 64. All of `[R-CNT-06]`'s
gates pass. `[R-CNT-27]` is met exactly at its floor.

### 2. The minimal file that actually carries data

To exercise every structure I built a one-layer file and emitted it for real.
Layer `a`: interleaved, linearization 1, codec 1 (none), filter 1 (none), no
alignment, no slab, rank 1, dimension `x` with E=4 and T=4, one channel `v` of
type uint8 (id 6) with fill 0x00. Geometry per §11.2 `[R-GEO-03]`: G = ceil(4/4)
= 1, N = 1, P = 4; interleaved so addressed-tile count = N = 1. Sample stride Q
= 1, decoded size = P·Q = 4 (§14.2 `[R-SER-02]`).

Emitted layout:

```
[0,16)     front signature block                                §6.1
[16,20)    stored tile, 4 bytes 01 02 03 04                     §14.2 (codec 1: stored = filtered image verbatim, [R-COD-04])
[20,40)    index entry 0: offset=16, length=4, crc=0x29308CF4   §15.1 [R-IDX-01]
[40,44)    segment CRC array, 1 u32 = 0x8A854EAD                §15.4 [R-IDX-04]
[44,145)   directory region (97-byte layer record + 4-byte CRC) §7.1, §7.2
[145,192)  pre-trailer pad, 47 bytes                            §6.2 [R-CNT-05]
[192,256)  trailer, generation 1, F = 256                       §6.2
```

Index region length check, `[R-CNT-17]`: entry_count × 20 + ceil(entry_count /
2^16) × 4 = 1×20 + 1×4 = 24, which is what the layer record's extent slot
declares (offset 20, length 24). crc_of_crc_array = CRC-32C over the 4-byte
segment CRC array = 0xFCBB36C7.

Layer record, type 0x0001, flags 0x0003 (MU=1, PE=1, fixed by §7.3's registry
table and required of writers by `[R-CNT-22]`):

```
hdr  +0  u16 type            01 00
     +2  u16 flags           03 00
     +4  u32 inline_length   49 00 00 00   (73)
     +8  u64 extent_offset   14 00 ...     (20)  -> tile-index region §7.4
     +16 u64 extent_length   18 00 ...     (24)
inline (§7.4, packed in table order, no padding — [R-CNT-18]):
     +0  name                01 'a'
     +2  layout              01            interleaved §14.1 [R-SER-06]
     +3  linearization       01 00         row-major, the only legal value §11.4 [R-GEO-05]
     +5  codec               01 00         none §17.2 [R-COD-03]
     +7  filter              01 00         none §17.3 [R-COD-09]
     +9  alignment A         00 x8         none §16.1
     +17 slab S              00 x8         none §16.2
     +25 slab alignment      00 x8         must be 0 when S = 0, [R-CNT-23]
     +33 rank d              01
     +34 channel count C     01 00
     +36 dim entry           01 'x' | 04 x8 (E) | 04 x8 (T)
     +54 chan entry          01 'v' | 06 00 (uint8) | 01 (fill len) | 00 (fill)
     +60 index_encoding      01            raw-segmented §15.1
     +61 entry_count         01 00 ...     equals addressed-tile count [R-CNT-17]
     +69 crc_of_crc_array    C7 36 BB FC
     +73 (no sub-records)
```

Every quantity a reader will re-derive at §19.3 layer access is decidable from
these bytes plus F, as `[R-RDR-03]` promises: fill length 1 equals uint8's
element size (§12.1, `[R-CNT-23]`); entry_count 1 equals N; extent_length 24
equals the formula; A=0 and S=0 so `[R-CNT-16]` is satisfied vacuously.

Ordering of the emission itself follows §9.2 `[R-LIF-02]`: front block, then
step 2 (payload and index, in either order — placement is free under
`[R-SLB-05]`), then step 3 (directory + CRC), barrier, step 5 (pad to the next
64 boundary + trailer), barrier.

### 3. The append procedure and its barriers

An appender does, in order (§20.3 `[R-WRT-04]`, resting on §9.2 `[R-LIF-02]`):

1. **Establish F.** Validate the trailer in the *physical* final 64 bytes
   (`[R-LIF-04]`). Not "search for" — validate exactly there. Magic, CRC,
   version gate, then the field gates of `[R-CNT-06]`, including
   committed_file_length equal to the physical size. If any fails the file is
   torn and the appender MUST NOT append; recovery (§9.6) is a separate,
   deliberate operation.
2. **Open** as a reader, §19.1 `[R-RDR-01]`: trailer, directory region, its CRC,
   the record walk, the layer-name namespace check.
3. **Validate what the commit touches**, `[R-WRT-03]`: the full directory always
   (re-emission relies on every directory byte); §19.3 layer validation for each
   layer whose record, index or extents change; the §15.4 index chain for every
   segment whose entries are being reused byte-for-byte.
4. **Write payloads and indexes**, beginning at exactly F. Any layer whose
   stored-tile set, index content, *or index placement* changes has its whole
   tile-index region re-emitted — entry_count entries plus the segment CRC
   array — with unchanged entries byte-identical at their disk-ordinal
   positions.
5. **Re-emit the complete directory** and its CRC. Every retained, unmodified
   record byte-identical, header/inline/extent slot (`[R-WRT-05]`).
6. **Barrier #1** — steps 1–3 of `[R-LIF-02]` durable.
7. **Pad** to the next 64-byte boundary, then the **trailer**: generation + 1,
   same file_id, unknown ignore-lane flag bits copied forward (`[R-CNT-08]`),
   version_minor = max(floor, prior minor) (`[R-CNT-26]`), committed_file_length
   = new end.
8. **Barrier #2** — the trailer durable.

Two barriers, not one (§20.2 `[R-WRT-02]` says so explicitly). The invariant
they buy is stated in §9.2's note: if the barriers are weaker than assumed,
safety degrades from "torn commits are invisible" to "torn commits are
detected" — §8's chain still catches every inconsistent state loudly. Note that
the pad and the trailer are both written *after* barrier #1, so up to 127 bytes
(63 pad + 64 trailer) are in flight at the moment of the crash window; that is
fine, because every one of them is at an offset ≥ F_prev and cannot damage the
previous state (§9.1 `[R-LIF-01]`).

One appender consequence worth naming, derived from §11.4 `[R-GEO-06]`: growing
a layer's extents renumbers disk ordinals unless the growth is along
dimension 0. Under row-major, s = Σ tᵢ · ∏_{j>i} Gⱼ, so increasing G₀ leaves
every existing tile's ordinal unchanged and appends new ordinals at the end;
increasing any *other* Gᵢ changes ∏_{j<i} strides and permutes the whole index.
`[R-WRT-04]` step 4 acknowledges this in one parenthesis ("a geometry change
renumbers ordinals") and leaves the writer to work out which growths are cheap.

Slab layers make appends expensive in a second way: `[R-SLB-04]` says a commit
that supersedes a stored tile in, or grows the extents of, a slab-declared layer
MUST either re-establish `[R-SLB-03]`'s invariants for every affected run — i.e.
rewrite *every stored tile of that run* contiguously at a fresh A_slab-aligned
offset — or clear the declaration (S = 0, and A_slab = 0 with it, per
`[R-CNT-23]`). Per-tile alignment is cheaper: only the commit's *new* tiles must
satisfy offset mod A = 0.

### 4. What becomes unreachable, per commit shape

Because `[R-CNT-05]` forbids any structure between the directory's end and the
trailer, the live directory, pad and trailer of a generation always occupy the
single contiguous run [dir_offset, F). So:

**Every commit, whatever its shape, orphans exactly [dir_offset_prev, F_prev).**
That is dir_length_prev + pad_prev + 64 bytes. Nothing else is unconditional.

On top of that:

- **(a) New layer** (§20.3 example a). Nothing else. The prior layers' records
  are re-emitted byte-identically, extent slots and all, so their tiles and
  indexes stay live and never move. Slack = dir+pad+trailer only — sized by the
  file's *layer count*, never by any layer's data.
- **(b) Tiles added to or superseded in an existing layer** (example b). Also:
  the touched layer's entire previous tile-index region (entry_count × 20 +
  ceil(entry_count/2^16) × 4 bytes), plus the previous payload extent of every
  tile whose entry changed — superseded tiles and tiles turned into sentinels.
  Retained tiles' payloads do not move. This is the cost §20.3's note
  quantifies: one edited sample in a 10^6-tile layer orphans ~20 MB of index.
- **(c) Metadata-only change** (example c) — clearing a slab declaration,
  editing user metadata. Also: the previous extent of any user-metadata record
  whose document changed. Nothing else; the layer records keep their extent
  slots.
- **(d) Layer removed** — if permitted at all; see finding 2. Would additionally
  orphan the layer's whole index region and every one of its stored-tile
  extents.

Concretely on my file: generation 1 has F = 256. A shape-(b) commit that
supersedes the single tile appends payload at [256,260), index at [260,284),
directory at [284,385), pad [385,448), trailer [448,512), F₂ = 512. Orphaned:
[16,20) old payload, [20,44) old index, [44,145) old directory, [145,192) old
pad, [192,256) old trailer — the entire run [16,256). The live state of
generation 2 is the front block plus [256,512). A shape-(c) commit on the same
file instead appends only a directory at [256,357), pad [357,384), trailer
[384,448), F = 448, orphaning [44,256) = 212 bytes and leaving the tile and
index at [16,44) live.

None of this is reclaimable except by compaction (§20.5 `[R-WRT-06]`,
`[R-WRT-07]`), which mints a fresh file_id and generation 1 and must refuse the
file outright if it carries an MU = 1 record type it does not implement.

### 5. Torn-write recovery

Three distinct actors, three distinct behaviors, and the document keeps them
apart cleanly:

- **Reader (default path)** — §9.5 `[R-LIF-05]`: trailer-at-end-or-fail. No
  valid trailer in the final 64 bytes ⇒ report torn/invalid and MUST NOT scan
  backward. A reader cannot distinguish a torn commit from residue past a
  completed one (§9.5's note) and is not asked to.
- **Appender** — §9.4 `[R-LIF-04]`: same validation; on failure, do not append.
  Once F is established (directly, or from re-verified recovery output) and the
  physical file is longer than F, either truncate to F before step 1 or
  overwrite from F and truncate no later than step 6, so that after every
  completed commit physical length == committed_file_length.
- **Recovery tool** — §9.6 `[R-LIF-06]`: probe backward at 64-aligned offsets o
  for the trailer magic; a candidate requires the trailer CRC to verify *and*
  committed_file_length == o + 64. The nearest-to-end valid candidate is the
  last committed state; truncate to o + 64. Then re-verify the output as a whole
  file (§8) before trusting it, because a tile payload can deliberately mimic a
  trailer. Rollback is undetectable in-format: truncation to an earlier commit
  boundary is indistinguishable from that earlier version, so detecting it needs
  an out-of-band expected generation or a detached hash.

The self-referential gate (committed_file_length == o + 64) is what makes
mimicry hard: a mimic must know its own file offset. The document nevertheless
raises the mimic case explicitly and then does not say what to do when the
re-verification it mandates fails — see finding 4.

`[R-LIF-07]` is the writer's mitigation: very large single commits SHOULD emit
intermediate checkpoint commits, so that a torn multi-hour append is not
recoverable only by scanning back across its entire length.

### 6. Catalogue of legitimate divergence between two conforming writers

§2.3 `[R-CNF-05]` says outright that two conforming writers given identical
input MAY produce different files. Here is every place I found where the choice
is actually mine, grouped by where it bites. (Appendix G, non-normative, closes
most of these for a reproducible profile — which is itself a useful confirmation
that I enumerated the right set; my list is a superset of its eight items.)

**Container identity and header**
1. `file_id` — any nonzero u64; SHOULD be cryptographically random (§9.3
   `[R-LIF-03]`). Appendix G item 2 offers a deterministic hash construction.
2. `version_minor` — `[R-CNT-26]` is a SHOULD, so a writer may emit a higher
   minor than the floor.
3. `flags` ignore-lane bits — a creator MUST write 0 (`[R-CNT-08]`), but an
   appender copies forward whatever it found.
4. Number of commits used to reach the same live state — one commit vs. many
   produce different files with identical reference arrays (§3.2).

**Placement**
5. Order of stored tiles, index regions and record extents within a commit
   (§9.2 step 2: "in any order"; `[R-SLB-05]`: any non-overlapping positions,
   any order).
6. `dir_offset` — the directory need not abut the last payload; a writer may
   leave arbitrary slack before it.
7. Pre-trailer pad length, subject to finding 3.
8. Whether to declare alignment A, and its value (512 … 2^62, power of two;
   4096 recommended, §16.1).
9. Whether to declare a slab S, its run length, and A_slab (power of two ≥ 1).
   `[R-CNT-16]` forbids only declaring both A and S.
10. Slack content — `[R-CNT-03]` zeroing is a SHOULD; alignment gaps, slab gaps
    and the pad are unconstrained (§5.2 `[R-CNT-21]`).

**Array encoding of the same logical data**
11. Tile extents T — the spec imposes none (§11.3's note offers only guidance).
12. Channel layout — interleaved vs planar. For a single-channel numeric layer
    the tile images are byte-identical; for a single-channel bool layer they are
    not (ceil(P/8) vs P bytes), and §14.4's note says both are valid.
13. Codec 1–4 (§17.2), and within codecs 2–4, the encoder, its version, its
    level, its block/match/table choices and its thread count. Appendix G item 1
    names this the profile's real boundary: byte-identity across *implementations*
    is unattainable for codecs 2–4.
14. Filter 1 vs 2 — byte-shuffle is optional, and applying it changes stored
    bytes for identical logical content (§17.3 `[R-COD-10]`).
15. DEFLATE's final-byte padding bits (codec 2): the stream ends mid-byte and
    RFC 1951 does not fix the residual bits.
16. Zstd frame options that `[R-COD-06]` does not pin — single-segment vs
    window descriptor, presence of Frame_Content_Size (MAY be present), block
    partitioning.
17. Sentinel vs. stored-all-fill tile. Nothing requires a writer to elide a tile
    all of whose samples equal fill; Appendix G item 6 makes it a profile rule
    precisely because the core does not.
18. Fill value when the caller does not choose one — `[R-TYP-10]` is a SHOULD
    (all-zero bytes).

**Directory content**
19. Record order within the directory sequence — order carries no meaning
    (`[R-CNT-14]`).
20. Whether to emit a file-scope or layer-scope user-metadata record at all;
    every standardized key of §18.4 is OPTIONAL.
21. Metadata encoding 1 (none) vs 2 (zstd) (§18.2 `[R-MTA-03]`).
22. JSON serialization within the document: insignificant whitespace, number
    formatting, escape choices (`"a"` vs `"a"` — §18.2 says they are the
    same key, so both are legal spellings of it). Member *order* is not free:
    `[R-MTA-05]` makes ascending UTF-8 key order a MUST.
23. Unicode normalization of names — `[R-ENC-14]` is a SHOULD, and this one has
    a semantic consequence, not merely a byte one: NFC and NFD spellings are
    *different names* under `[R-ENC-13]`.

**Not divergence, though it looks like it:** the all-sentinel segment CRC
constant of `[R-IDX-05]`. A writer MAY emit 0xEECB3BB2 without computing it, but
the bytes are identical either way.

### 7. Places where the document closed a door I expected to be open

Worth recording because they shape a writer's data structures:

- **No deduplication of any kind.** `[R-CNT-13]` says extents are owned exactly
  once — two stored extents of one layer overlapping is reject-layer, and any
  overlap across layers or into another scope's structures is reject-file. So a
  writer cannot point two byte-identical tiles at one payload, and cannot share
  one index region between two identically-shaped layers. `(0,0)` means "no
  extent" and so is not an overlap, which is the one case where two layer
  records may carry the same slot.
- **No partial index update.** Any change to a layer's stored-tile set, index
  content, or index placement re-emits the whole region (`[R-WRT-04]` step 4).
- **The directory is always the last structure.** `[R-CNT-05]` plus the
  no-overlap rule forces every other live structure into [16, dir_offset).
- **Decoded size is never read from the payload.** §14.2/§14.3 `[R-SER-07]`,
  and `[R-COD-06]` explicitly forbids sizing a buffer from zstd's
  Frame_Content_Size. Writers get no freedom here and readers get their
  decompression-bomb defense (§22.2 `[R-SEC-02]`).

### 8. Where I had to guess

Ten findings follow in the structured list. The two that would actually change
my writer's behavior if resolved the other way are #2 (may an appender delete a
layer?) and #3 (may a commit's pre-trailer pad exceed 63 bytes?). The two
contradictions (#1, #5, #6) are document defects rather than implementation
forks — but #5 and #6 both change what a conformance corpus must contain and
what a verifier must certify, so they are not cosmetic.

## Findings

### CONTRADICTION — §21.6 (closing paragraphs, lines 2896–2907) vs §21.2 row F21

Byte-level: False

§21.6 states that a file whose version_major names a major the reader does not implement is one of two cases that are 'conforming files a reader nevertheless refuses', and says of them: 'In both the outcome records a reader's capability, not a defect in the bytes, and the diagnostic ought to distinguish the two — which is why neither is a register row, while a *reserved*-range type, whose emission `[R-CNT-15]` does make a violation, is.' But §21.2 registers exactly that case as a row: 'F21 | Trailer version_major is a nonzero major the reader does not implement (e.g. 2); magic and CRC still validate | version_major | reader | open | `[R-CNT-07]` (R-CNT-24)'. §21.2's header assigns every row in it the outcome reject-file and §21.8 `[R-ERR-02]` requires 'Every row of §21.2 through §21.5 ... has at least one conformance vector (§24) whose expected verdict is that row's outcome' — so F21 obliges a corpus vector for a file §21.6 says can be 'perfectly conforming under that major', while §24 `[R-VEC-02]` requires each vector to record 'whether the file is conforming'. The second of §21.6's two cases (an experimental-range record type with MU = 1) genuinely has no row; the first does. Either F21 must be struck, or §21.6's 'neither is a register row' must become 'the second is not'.

**Readings.** n/a (contradiction, not ambiguity)

### AMBIGUITY — §20.4 `[R-WRT-05]` and its flags table; §2.4's preserve-verbatim definition; §7.3's registry table (layer = MU 1/PE 1, user metadata = MU 0/PE 1)

Byte-level: True

Nothing in the document states whether an appender may emit a new complete directory that omits a record of a type it *does* implement. §20.3's three worked commit shapes are (a) a new layer, (b) tiles added or superseded, (c) a metadata-only change — there is no 'layer removed' shape, and §20.5's compactor is described as emitting 'only the structures reachable from the input's live trailer ... less any record §20.4 lets it drop', where §20.4's drop permission is confined to MU = 0 with PE = 0. Since §7.3 fixes PE = 1 for both registered types, a literal reading makes layer deletion and user-metadata-record deletion impossible in this format. §23.1 `[R-PRV-01]`'s 'a commit that removes data removes only its reachability' can be read either way — it is satisfied by superseding tiles with sentinels.

**Readings.** (a) No record with PE = 1 may ever be dropped: §2.4 defines preserve-verbatim as 'Binds updaters: the bytes are carried forward unmodified', §7.3 fixes PE = 1 for both major-1 types, and §20.4's table grants drop permission only in the MU = 0 / PE = 0 row. Under this reading a layer, once created, is permanent, and a file can only grow. (b) The PE table governs only types the updater cannot parse — its header sentence is 'For record types the updater does not implement, the stored flags govern' — and `[R-WRT-05]` constrains only 'every record it retains and does not logically modify', saying nothing about retention itself; for a type it implements, the updater is simply a writer emitting a new conforming generation, so it may omit a layer record. I picked (b), because reading (a) leaves the format with no defined way to remove a layer at all, which would make §20.5's 'less any record §20.4 lets it drop' the sole deletion mechanism in the whole document and would make compaction unable to shrink a file that no longer needs one of its arrays. But (a) is defensible from the same text, and the two readings emit different directories for the same caller request, so I flag it rather than rely on it.

### AMBIGUITY — §6.2 `[R-CNT-05]` vs §9.2 `[R-LIF-02]` step 5

Byte-level: True

`[R-CNT-05]` says of the pre-trailer pad: 'a writer that ends its directory on a 64-byte boundary leaves none, and this specification bounds neither their number nor their content.' `[R-LIF-02]` step 5 says the writer MUST '(5) append the pad to the next 64-byte boundary — zeroed by advice, `[R-CNT-03]` — and the new trailer'. The first sentence says the pad is unbounded; the second, read as a requirement on a writer performing a commit, fixes it at exactly (−dir_end) mod 64 bytes, i.e. 0 to 63.

**Readings.** (a) `[R-LIF-02]` binds writer conduct and `[R-CNT-05]` describes only what a *file* predicate tolerates (§2.3 `[R-CNF-02]` explicitly separates conduct rules from the byte predicate): a commit's pad is 0–63 bytes, and a file carrying a larger pad is conforming but unreachable by any conforming commit. (b) `[R-CNT-05]`'s 'bounds neither their number' is the operative rule and `[R-LIF-02]` step 5 merely names the pad's purpose, so a writer may pad arbitrarily — e.g. to reserve growth room, or to land the trailer on a 4 KiB boundary. I picked (a) for my writer: minimum pad, always < 64 bytes. My reader and verifier accept (b)'s files, since `[R-CNT-06]`'s gates and `[R-CNT-05]`'s own verifier check (a structure in the gap is reject-file; anything else there is slack) admit them. If (b) were intended for writers too, `[R-LIF-02]` step 5 should say 'to a 64-byte boundary' rather than 'to the next'.

### AMBIGUITY — §9.6 `[R-LIF-06]`

Byte-level: True

`[R-LIF-06]` defines recovery as: 'probe backward at 64-aligned offsets o for the trailer magic; on a match, require the trailer CRC to verify and committed_file_length = o + 64. The nearest-to-end valid candidate is the last committed state; truncating to it recovers the file.' It then makes a caution normative: 'a tile payload can deliberately contain a byte string that mimics a valid trailer, so recovery output MUST be re-verified as a whole file (§8) before being trusted.' The document raises the mimic case and mandates the re-verification, but never says what a recovery tool does when that re-verification fails — which is precisely the mimic case realized. Nor does it say where the backward probe starts (in practice, the largest 64-aligned o with o + 64 ≤ physical size).

**Readings.** (a) Recovery fails and reports the file unrecoverable: 'the nearest-to-end valid candidate is the last committed state' is definitional, so a candidate that fails whole-file verification means the file is beyond repair. (b) The tool continues the backward scan past the failed candidate to the next one, since the re-verification has demonstrated that the candidate was not in fact a commit state. I picked (b): the sentence 'Generation enumeration for coverage verification (§5.2) is the same probe continued to offset 0' shows the probe is designed to be continued, and (a) would let a single crafted 64-byte payload string permanently deny recovery of an otherwise intact file — the exact attack §22.3 `[R-SEC-04]` says the re-verification exists to blunt. The risk of (b) is the mirror image: it will truncate away a genuine last generation whose file fails §8 for an unrelated reason (a corrupt tile in an untouched layer), silently rolling the file back, and §9.6 itself notes rollback is undetectable in-format. A recovery tool should therefore report which candidate it landed on and how many it skipped, but the document does not require that.

### CONTRADICTION — §21.3 section header vs rows L49/L50 (and identically §21.2 header vs F30/F31, §21.4 header vs T2)

Byte-level: False

§21.3 opens: 'Outcome: reject-layer — the named layer is unusable, every other layer unaffected. 50 conditions.' Row L49 in that same table reads: 'A layer sub-record's user-metadata document has object members not in ascending order of their keys' UTF-8 bytes; the document stays readable and readers process it unchanged'. A layer that readers process unchanged is not a layer that is unusable. The same collision occurs in §21.2 (header 'Outcome: reject-file' vs F30/F31, whose text says readers process the record unchanged and 'readers apply the type's fixed semantics regardless') and in §21.4 (header 'Outcome: reject-tile — that tile's read reports failure' vs T2, whose governing rule `[R-SER-08]` says 'A reader that neither detects the violation nor rejects the tile, and returns the value, MUST report 0x00 as false and every other byte as true' — i.e. serves the tile). §2.4 `[R-CNF-07]` forces the issue by requiring that 'Every detectable violation named by this specification is assigned exactly one reader outcome', leaving no class for 'nonconforming, but no reader outcome', and §21.6's own closing paragraph concedes these rows leave 'every reader behavior unchanged'. §21.1's precedence rule ('where a row and the rule it cites diverge, the rule governs') resolves row-vs-rule but not header-vs-row, so I resolved it by the cited rules: `[R-MTA-05]` and `[R-SER-08]` govern, readers serve. This matters beyond editing: §21.8 `[R-ERR-02]` requires a vector 'whose expected verdict is that row's outcome', and §24 `[R-VEC-04]` requires every reject-layer/reject-tile vector to carry an intact sibling — obligations that are incoherent for a row no reader may act on.

**Readings.** n/a (contradiction, not ambiguity)

### CONTRADICTION — §2.3 opening sentence vs §2.3's own bullet list

Byte-level: False

§2.3 states 'Conformance is defined for four classes.' and then defines five: 'Conforming TARN file' `[R-CNF-02]`, 'Conforming reader' `[R-CNF-03]`/`[R-CNF-04]`, 'Conforming writer' `[R-CNF-05]`, 'Conforming updater' `[R-CNF-06]`, and 'Conforming verifier' `[R-CNF-11]`. Appendix H likewise enumerates five checklists ('Conforming file', 'Conforming reader', 'Conforming writer', 'Conforming updater', 'Conforming verifier'). The count is wrong, not the list.

**Readings.** n/a (contradiction, not ambiguity)

### OBSERVATION — §17.2 `[R-COD-06]` (zstd window rule) against Appendix F's normative reference to RFC 8878

Byte-level: True

`[R-COD-06]` says writers 'MUST NOT declare a window size exceeding the tile's decoded size; a reader MUST treat either as a validity error at tile scope' — registered as §21.4 row T21. RFC 8878's frame format cannot express a Window_Size below 1024 bytes through the Window_Descriptor (Window_Log has a floor of 10); the only way a frame declares a smaller window is the Single_Segment_Flag form, in which the window is taken to be the Frame_Content_Size. Consequence for a writer: every tile whose decoded size is under 1024 bytes MUST be compressed as a single-segment frame under codec 3, and — because that form obliges Frame_Content_Size to be present — that field must then equal the decoded size, which `[R-COD-06]` independently requires anyway. The specification never states this. It is fully decidable, but only by cross-reading an external normative reference against a rule that reads as innocuous; a writer that hands small tiles to a stock whole-buffer compress call and does not control the frame header can produce a file every one of whose tiles is reject-tile under T21, with checksums that all verify. Small tiles are not exotic: a rank-1 layer with T = 64 and one uint8 channel has a 64-byte decoded size, and §11.3's note declines to impose any tile-size floor.

**Readings.** n/a

### OBSERVATION — §17.2 `[R-COD-06]` against §21.9's limits table and §2.3 `[R-CNF-03]`

Byte-level: True

§21.9 guarantees a conforming reader accepts a zstd frame Window_Size of at least 8 MiB and a decoded tile size of at least 256 MiB. `[R-COD-06]` permits a writer to declare any window up to the tile's decoded size. So a conforming writer may emit a conforming 64 MiB-window frame on a 256 MiB tile, and a conforming reader may decline it: `[R-CNF-03]` only obliges acceptance of files 'none of whose values exceeds the minimum guarantees', and `[R-ERR-04]` explicitly licenses declining at 'the narrowest scope whose declarations exceed what it can serve, a layer or a tile'. The writer-side advice that follows — cap Window_Size at 8 MiB if you want universal readability, even on large tiles — is derivable but stated nowhere; §21.9's note only observes that '8 MiB is the decoder window support RFC 8878 itself recommends, which stock encoder settings stay within', which describes encoder defaults rather than binding or advising the writer. Cheap to get right once noticed; expensive to notice, since nothing in §17.2 points at §21.9.

**Readings.** n/a

### AMBIGUITY — §18.2 `[R-MTA-05]`, read against §18.2's duplicate-key restriction and register rows F30/L49

Byte-level: True

`[R-MTA-05]` says 'Writers MUST serialize object members in ascending order of their keys' UTF-8 bytes.' A user-metadata document is an arbitrary JSON object and may nest objects to any depth — §18.4's `tarn.stats` is itself 'an object keyed by channel name, each value an object', so nesting is not hypothetical but registered. The requirement does not say whether it binds every object in the document or only the top-level one.

**Readings.** (a) Every object at every nesting depth. Supported by the phrasing 'object members' without qualification, by the duplicate-key restriction two paragraphs earlier which is explicitly per-object ('a document in which any one object carries that key twice is unreadable'), by F30/L49's condition text ('a user-metadata document's object members are not in ascending order'), and by the stated purpose — 'This makes one writer's output reproducible for identical content', which top-level-only sorting would not achieve for a document containing `tarn.stats`. (b) The top-level object only, since that is the object §18.2 has been discussing ('The top-level value is an object'). I picked (a). The cost of guessing wrong is asymmetric but real in both directions: under (b) my sorted-everywhere output is still conforming, but under (a) a writer that sorts only the top level emits a nonconforming file that no reader will ever complain about — the violation's detector is the verifier and readers process the document unchanged.

### OBSERVATION — §17.4 `[R-COD-11]` citing '§9.7(d)'

Byte-level: False

`[R-COD-11]` reads: 'A verifier that cannot execute a layer's codec or filter cannot establish the layer's conformance and MUST NOT certify the file — the rule of §9.7(d) applied to content.' §9.7 is a single unlettered paragraph carrying `[R-LIF-08]`, describing the coverage walk; it has no items (a) through (d), and no other section in the document uses lettered sub-items. §18.2 `[R-MTA-09]` reaches the same conclusion for undecodable metadata documents by citing `[R-COD-11]` rather than §9.7, so the intended rule is recoverable — a verifier certifies only what it can establish, per §2.4 `[R-CNF-12]`'s 'a verifier certifies only violation-free files'. The reference itself is unresolvable as written.

**Readings.** n/a


## Verdict
Implementable as a writer and an appender from this document alone. I built a byte-exact 128-byte empty file and a byte-exact 256-byte one-layer file (front block, one stored tile, a 24-byte index region, a 97-byte layer record, a 101-byte directory, a 47-byte pad, a trailer at 192) without needing a single external decision on structural layout, and independently reproduced all four of the document's self-check constants (CRC-32C of "123456789" and of zero bytes, the all-sentinel segment CRC 0xEECB3BB2, and Appendix A's trailer CRC 0xE00938D2) plus every worked example in §11–§20 and §21.8's own instance count of 125 rows / 244 instances. The container is genuinely self-contained: I never had to infer a field width, an offset, an order, or an outcome. Ten findings. Three are contradictions in the document rather than forks in my implementation: §2.3 says four conformance classes and defines five; §21.6 says the unimplemented-version_major case "is not a register row" while §21.2 registers it as F21; and the scope headings of §21.2/§21.3/§21.4 assert reader outcomes (reject-file / reject-layer / reject-tile) for rows whose own text says readers process the structure unchanged (F30/F31, L49/L50, T2) — a hole §2.4 `[R-CNF-07]` creates by requiring every named violation to carry exactly one reader outcome, with no class for "nonconforming but reader-invisible". The last of those propagates into the corpus obligations of §21.8 and §24 `[R-VEC-04]` and is the one I would fix first. Four are places where I had to guess and my choice changes emitted bytes: whether an appender may drop a PE = 1 record and thereby delete a layer (§20.4 — I chose yes, and the format otherwise has no deletion mechanism at all); whether a commit's pre-trailer pad may exceed 63 bytes (§6.2 `[R-CNT-05]` says unbounded, §9.2 `[R-LIF-02]` step 5 says "to the next 64-byte boundary" — I chose the latter for writing and the former for reading); whether `[R-MTA-05]`'s key sort binds nested objects (I chose yes); and what a recovery tool does when the mandated whole-file re-verification of its output fails, which is exactly the trailer-mimic case §9.6 itself raises and then leaves open (I chose to continue the backward scan). The remaining three are decidable but costly to notice, and two of them are real traps for a first writer: `[R-COD-06]`'s "window size must not exceed the decoded size" silently forces single-segment zstd frames for any tile under 1 KiB, because RFC 8878's Window_Descriptor cannot express a smaller window — a naive writer produces a file whose every tile is reject-tile with all checksums valid; and a writer wanting universal readability must cap the zstd window at §21.9's 8 MiB guarantee even though `[R-COD-06]` permits up to the decoded size. Neither has a home in the document today. The third is a dangling cross-reference, "§9.7(d)", to a section with no lettered items.