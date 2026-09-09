# Cleanroom round 35 — Writer implementer transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
in full, in seven `Read` calls covering lines 1–4864. I opened no other file in the
repository, ran no `git` command, issued no web request, and listed no directory of the
repository. I did not read the output directory.

I ran shell text-processing (`grep`, `awk`, and one `python3` heredoc) **against that one
file only**, and one `python3` script that reads no files (a CRC-32C implementation plus a
file builder). My scratch directory
`/private/tmp/.../r35-round/scratch/writer/` was **empty when I began**; I created it
myself. The files I wrote into it are:

- `wr_crc.py` — CRC-32C (reflected 0x82F63B78) plus the document's own check constants.
- `wr_build.py` — an end-to-end two-layer file builder.
- `demo.tarn` — the 576-byte file that builder emits.

I wrote this transcript to the single output path named in my brief and nothing else.

**Context I did not ask for.** Material was placed in my context before I began: a project
instruction file pointer (`CLAUDE.md` → `AGENTS.md`), an index of maintainer memory notes
with titles referring to this project's harness and to prior rounds' findings, a git status
snapshot with recent commit subject lines, and an MCP server instruction block. I did not
open any of it, and I have not used any of it as evidence. I name that it appeared, as
required. The git-status commit subjects in particular assert things about rounds 33 and 34;
I treated them as absent. Nothing below rests on them, and nothing below was suggested by
them — every finding is anchored to a quotation I pulled out of `spec/tarn.md` myself.

**Path check.** The specification was where the brief said it was.

**Wrapping.** The document is hard-wrapped and blockquotes carry `> `. Every search I report
below was run over a whitespace-normalised, `> `-stripped copy of the text held in memory,
not line-by-line, precisely because a line-oriented `grep` would return spurious zeros. I
control-tested the normalisation by searching for phrases I knew were present (see §7).

---

## 1. What I built: a creation byte layout, end to end

I picked a small but non-trivial file: two layers exercising both layouts, an edge-padded
interleaved tile, a packed planar boolean plane with pad bits, one sentinel entry, and a
file-scope user-metadata record.

### 1.1 The declarations

**Layer A — `sst`**, interleaved, rank 2.

| Field | Value | Fixed by the document, or my choice? |
|---|---|---|
| name | `sst` (3 bytes) | input |
| layout | 1 = interleaved | **my choice** ([R-SER-06] admits 1 or 2) |
| linearization | 1 = row-major | **fixed** — [R-GEO-05] admits no other value for writers |
| codec | 1 = none | **my choice** ([R-COD-03], 1–4) |
| filter | 1 = none | **my choice** ([R-COD-09], 1 or 2) |
| alignment A | 0 | **my choice** ([R-SLB-01]) |
| slab S / A_slab | 0 / 0 | **my choice**; A_slab = 0 then **forced** by [R-CNT-23] |
| rank d | 2 | input |
| C | 1 | input |
| dims | `y` E=5 T=4; `x` E=5 T=4 | E input; **T is my choice** — §11.3's Note says the document imposes none |
| channel | `v`, type 7 = uint16, fill `CD AB` (0xABCD) | type input; fill is the caller's, defaulting to all-zero by [R-TYP-10]'s SHOULD |
| index_encoding | 1 | **fixed** — [R-CNT-23]'s table admits nothing else |
| entry_count | 4 | **derived**: G = (⌈5/4⌉, ⌈5/4⌉) = (2,2), N = 4, interleaved ⇒ entry_count = N ([R-GEO-03]) |
| crc_of_crc_array | derived | **derived** |

P = ∏Tᵢ = 16, Q = ΣBᵢ = 2, decoded size = P·Q = 32 bytes per tile ([R-SER-02]).

**Layer B — `mask`**, planar, rank 1, dim `i` E=10 T=10, one bool channel `m` fill `0x00`.
G = 1, N = 1, planar ⇒ entry_count = C·N = 1. P = 10, planar bool ⇒ decoded size =
⌈P/8⌉ = 2 bytes ([R-SER-03]).

### 1.2 Tile content, including the two content obligations a writer owes

Layer A's four addressed tiles. I set the real sample at (y,x) to `10y + x`.

- tile (0,0), s = 0: covers y 0–3, x 0–3 — **every position real**, 16 values.
- tile (0,1), s = 1: covers y 0–3, x 4–7 — x = 4 real, x = 5,6,7 **padding**.
- tile (1,0), s = 2: covers y 4–7, x 0–3 — y = 4 real, y = 5,6,7 **padding**.
- tile (1,1), s = 3: covers y 4–7, x 4–7 — one real position (4,4). I left it **unstored**,
  so (4,4) reads fill ([R-TYP-08]). This is the sentinel entry.

Every padding position carries the recorded fill bytes `CD AB` — [R-SER-05], whose worked
example in §14.5 is this exact geometry ("extents (5, 5), tile extents (4, 4) … values 1–15
are each the bytes `CD AB`"). I checked my construction against it.

Layer B's single tile: ten bool values alternating true/false from k = 0. Bit k of byte
k div 8, LSB-first ([R-SER-03]).

- byte 0 = values 0–7 = `0x55`
- byte 1 = value 8 in bit 0, value 9 in bit 1, **pad bits 2–7 = the channel's fill bit = 0**
  ⇒ `0x01`

Stored bytes `55 01`, length 2. Under codec 1 the entry's length MUST equal the decoded
size ([R-COD-04]) — 2 = 2. ✓

### 1.3 Placement — what the document fixes and what it leaves me

The only placement rules that bind a creator are: the front block at [0,16) ([R-CNT-04],
§6.1); `[R-LIF-02]`'s creation path, "writing beginning at offset 16"; `[R-CNT-05]`'s "no
structure lies between [the directory's] end and the trailer"; step 5's pad to the next
64-byte boundary; F ≡ 0 mod 64; every stored-tile extent at offset ≥ 16 and ending ≤ F − 64
(§15.3); every record extent likewise ([R-CNT-13]); and non-overlap ([R-CNT-02],
[R-CNT-13]). Everything else is free: `[R-SLB-05]` — "its stored tiles MAY occupy any
non-overlapping byte positions, in any order".

I packed contiguously from 16:

```
offset   len  what
0x0000    16  front signature block  89 54 41 52 4E 0D 0A 1A + 8 zero bytes
0x0010    32  layer A tile s=0
0x0030    32  layer A tile s=1   (12 padding positions, each CD AB)
0x0050    32  layer A tile s=2   (12 padding positions, each CD AB)
0x0070    84  layer A tile-index region  (4 entries x 20 = 80, + 1 segment CRC x 4)
0x00C4     2  layer B tile (planar bool plane, 55 01)
0x00C6    24  layer B tile-index region  (1 entry x 20 = 20, + 1 segment CRC x 4)
0x00DE    25  file-scope user-metadata extent: 21 document bytes + 4-byte CRC
0x00F7   247  directory region: recA(118) + recB(100) + recM(25) + 4-byte CRC
0x01EE    18  pre-trailer pad -- slack, zeroed by [R-CNT-03]'s advice
0x0200    64  trailer
                                         F = 0x0240 = 576, and 576 mod 64 = 0. OK
```

The index-region length is `[R-CNT-17]`'s expression: for layer A,
4 × 20 + ⌈4/2¹⁶⌉ × 4 = 80 + 4 = 84; for layer B, 1 × 20 + 1 × 4 = 24. Both agree with the
extent slots I emitted, which is the cross-check `[R-CNT-17]` makes a layer-scope error to
get wrong (L22).

Computed CRC-32C values (my own implementation, check-vectored in §7 below):

- tile s=0 `0x1E26C888`, s=1 `0xAC3CBAA4`, s=2 `0x4CEF0D9D`; layer B's tile `0x9EF03AFF`
- directory region CRC `0x61D10179`; trailer CRC over bytes [0,60) `0x1D249A18`

**Slack in the created file: 18 bytes**, the pre-trailer pad and nothing else. F (576) minus
the claimed bytes (16 + 98 tiles + 108 index + 25 extent + 247 directory + 64 trailer = 558)
= 18. That arithmetic is the verifier's obligation under [R-CNT-21]/[R-LIF-08], and it
completes here, so the total is exact rather than partial.

### 1.4 Ordering decisions the document did *not* fix, and how I resolved them

1. **Whether to store tile (1,1).** Its one real position holds fill, so storing it or
   sentinelling it are both conforming and denote the same reference array. I sentinelled
   it. Appendix G item 6 pins this for reproducibility; the core does not.
2. **Where the index regions go relative to the tiles.** Free ([R-SLB-05]). I put each
   layer's index immediately after its tiles; §5.1's Example warns that the grouping "is
   illustrative: a layer's structures need not be contiguous or ordered".
3. **Record order in the directory.** Free — [R-CNT-14]: "Record semantics MUST NOT depend
   on record order". I emitted A, B, metadata.
4. **file_id.** Any nonzero u64; [R-LIF-03] states a SHOULD for a cryptographically random
   draw. I used a constant, which is conforming and, per §9.3's own text, courts
   (file_id, range) cache collisions.
5. **version_minor = 0**, [R-CNT-26]'s floor.
6. **flags = 0** — this one is *not* free for a creator: §6.3, "a writer creating a file
   under this text MUST write flags = 0".

Everything a creator needs is forward-computable in one pass: tile offsets → tile CRCs →
index entries → segment CRC → crc_of_crc_array → layer record → record offsets → directory
→ dir_offset/dir_length → F → trailer CRC. No field in this format refers to a quantity
that depends on itself. I checked that explicitly, because a circular dependency would have
forced two-pass emission and the document never says a writer may not need one.

---

## 2. The append procedure

### 2.1 Second commit: supersede one tile

Take the file above and supersede layer A's tile s=0 with new content. Following
[R-WRT-04]:

1. **Establish F** — validate the trailer at the physical end ([R-LIF-04]). F = 576, and
   the physical length is 576, so no truncation is owed.
2. **Open** — §19.1's four steps. The appender is a reader here.
3. **Validate what the commit touches** — [R-WRT-03]: trailer and full directory always;
   §19.3's layer validation for layer A; the §19.4 index chain for every segment whose
   entries the commit reuses, which for layer A is segment 0 (all four entries).
   Layer B is neither modified nor relied on, so nothing further is owed for it.
4. **Write payloads and indexes** beginning at exactly F = 576.

```
0x0240    32  layer A tile s=0, new content
0x0260    84  layer A index region, re-emitted IN FULL
                entry 0 re-pointed to 0x0240 with its new crc
                entries 1, 2 byte-identical at their disk-ordinal positions
                entry 3 still the sentinel FF x16 00 x4
                segment CRC recomputed over all 80 entry bytes
0x02B4   247  directory: recA modified (extent slot -> 0x0260), recB and recM
                byte-identical ([R-WRT-05])
0x03AB    21  pad to the next 64-byte boundary
0x03C0    64  trailer, same file_id, committed_file_length = 0x0400 = 1024
```

F₂ = 1024, which is F₁ + 448 — comfortably above [R-LIF-02]'s "at least 128".

**Slack after commit 2: 466 bytes.** 1024 − 558 (the live state is the same size as before)
= 466, made of: the old tile s=0 (32), the old index region (84), the old directory (247),
the old pad (18), the old trailer (64), and the new pad (21). This is exactly §20.3's Note
("A commit's cost is dominated by its index, not its data") made concrete: superseding 32
bytes of payload cost 84 bytes of index plus 247 bytes of re-emitted directory.

### 2.2 A file whose records I do not all understand — the full flag walk

§20.4 fixes the authority for the flags before the table is read: "For a type §7.3
registers, the registry's fixed flags govern rather than the stored ones (`[R-CNT-22]`) …
For a type the updater implements that this specification does not register, the definition
it implements the type from supplies the flags, and the stored bits never do … For a type
the updater does not implement, the stored flags are authoritative".

| Case | Governing flags | What my updater may do |
|---|---|---|
| type 0x0001 layer (implemented) | MU=1, PE=1 from the registry | Modify per §20.3 step 4; may never drop it. The MU=1 *row* does not bite: "Its MU = 1 row reaches only a type the updater does not implement". |
| type 0x0002 user metadata (implemented) | MU=0, PE=1 | Retain byte-identical, extent content unmodified; or modify it (a new extent is appended and the old one strands, §20.3 shape (b)). May never drop it. |
| unregistered type I implement, its definition says MU=0/PE=1 | from that definition | Retain byte-identical, extent unmodified; modify as that definition provides. |
| unregistered type I implement, definition says MU=0/PE=0 | from that definition | Retain, **or drop** — "in any commit it is otherwise free to make — one whose only effect is the drop included". SHOULD report the loss. |
| unknown type, stored MU=0/PE=0 | stored | Retain, or drop; extent becomes slack. |
| unknown type, stored MU=0/PE=1 | stored | Retain byte-identical, extent content unmodified. May relocate the extent and re-point the slot, but only under §20.5 ([R-WRT-08]). |
| unknown type, stored MU=1/PE=1, **top level** | stored | **No commit at all.** [R-CNT-15] makes it reject-file; my updater is a reader first. A compactor must refuse. |
| unknown type, stored MU=1/PE=0, **top level** | read as MU=1/PE=1 ([R-CNT-12]) | As above. |
| unknown type, stored MU=1, **layer sub-record** | stored | Reject-layer ([R-CNT-18]); that layer is not modifiable; **other layers stay editable**. A compactor must still refuse the whole file ([R-WRT-06]). |
| any record, reserved flag bits 2–15 set | — | Readers ignore them; a verifier records F26/L47. My updater re-emits the record byte-identically, reserved bits and all, and MUST NOT "repair" them (§20.3 step 2). |

Two consequences I want on the record because they are easy to get backwards:

- **Implementing a type confers no permission to drop it.** §20.4: "implementing a record's
  type confers understanding of it, not permission to drop it."
- **No commit removes a layer record or a user-metadata record at either scope.** §20.4
  states it flatly, and gives the reason: an in-place removal would strand the layer's tiles
  and index as slack "leaving the file no smaller than before".

### 2.3 Write order, durability, and the commit point

[R-LIF-02] is explicit and I found no gap in it. Steps 1–3 (payloads, index regions, record
extents, then the complete directory and its CRC) must be durable at step 4's barrier;
step 5 appends the pad and the trailer; step 6's barrier makes the trailer durable. **The
commit point is step 6.** Both barriers are owed, not one — §20.2 and §20.5 both say so in
those words.

Two details worth naming because a careless implementer loses them:

- On creation the front block is written *before* step 1 and is therefore covered by neither
  step's nominal range. The document closes this by hand: "the writer first emits the front
  signature block (§6.1) — **whose durability the barriers of steps 4 and 6 cover**".
- The **pad** is covered by neither barrier. That turns out not to matter, and the document
  is right not to say anything: the pad is slack, and [R-CNT-21] makes its content
  unconstrained with "no conformance requirement" on it. A commit whose pad bytes are lost
  to a torn write still produces a conforming file.

Steps 4 and 6 bind conduct, not bytes — §9.2 says so and [R-CNF-02] generalises it. So a
file committed without a barrier is never nonconforming *by virtue of that*. My updater
cannot detect a missing barrier in an input file and is not asked to.

---

## 3. Slack, by commit shape

| Shape | What becomes slack | Who counts it | What it may contain |
|---|---|---|---|
| **Creation** | the pre-trailer pad only, and any gap a declared A or A_slab forced | verifier ([R-CNT-21], §9.7) | anything; writers SHOULD zero ([R-CNT-03]) |
| **Append — new layer (shape (a))** | the previous directory, pad and trailer. Sized by the file's *layer count*, never by any layer's data | verifier | anything |
| **Append — tiles added or superseded (shape (b))** | the previous directory/pad/trailer, plus that layer's whole previous index region, plus every superseded payload | verifier | anything |
| **Append — directory-only (shape (c))** | the previous directory, pad and trailer; plus the extent of any PE=0 record dropped | verifier | anything |
| **Planar channel shortened** | every removed channel's stored-tile extents (§20.3 step 4, §23.1) | verifier | anything |
| **User-metadata edit** | the old extent — explicitly *not* shape (c): "its document lives in an extent … so a new extent is appended and the old one becomes slack, as in (b)" | verifier | anything |
| **Whole-file rewrite / compaction** | **none is carried**; the output's only slack is its own pad and its own alignment gaps | verifier on the output | anything |
| **Abandoned partial write** | **none — there is no slack, because there is no live state.** The physical tail past F makes the file's final 64 bytes not a trailer, so [R-CNT-06]'s gates fail and no F is established. §5.2 says the total "is not owed at all" in that case, "which is not a partial total but the absence of one" | nobody | n/a |

The last row is the one an implementer is most likely to get wrong, and I want to record
that the document handles it precisely. Residue past a completed commit "carries no register
row of its own" (§9.5's Note) — a reader meets it as a failing trailer gate (F8, F14 or
F17). What it violates is [R-LIF-04]'s writer obligation to truncate or overwrite.

**In-place update does not exist in this format.** [R-LIF-01] freezes [0, F) absolutely;
every mutation is a commit or a whole-file rewrite. What an application calls an in-place
update is shape (b), and the old bytes stay in the file.

---

## 4. Torn-write recovery — six crash points

Throughout: F is the *prior* committed file length; "physical" is the file's actual length.

**(1) Crash during step 2 (payloads/indexes appended, no directory).**
Next reader: the final 64 bytes are payload bytes; the trailer magic check at
physical − 64 fails ⇒ **F8, reject-file**, reported as torn ([R-LIF-05], and the reader
MUST NOT scan backward). Next updater: [R-LIF-04] — "the writer MUST NOT append; …
recovery (§9.6) is a deliberate, separate operation". Conforming in the meantime?
**No** — the byte sequence on disk is not a conforming file. The prior generation is intact
and recoverable by truncation to F.

**(2) Crash during step 3 (directory partially written).** Identical to (1).

**(3) Crash inside step 5, trailer partially landed.** If the physical length is F_new − k
for k > 0, the magic is not at physical − 64 ⇒ **F8**. If all 64 bytes' worth of extent
exists but the last 4 read as zeros, the magic passes and the CRC at offset 60 fails ⇒
**F14**. Either way loud, either way reject-file. This is §9.2's Note in practice: "§8's
chain still catches every inconsistent state loudly".

**(4) Crash after the trailer bytes land but before step 6's barrier.** If the trailer
reached durable storage the commit is complete and the file is the new generation,
conforming. If it did not, this is case (3). There is no state in between that a reader
accepts as a wrong generation.

**(5) A weak barrier reorders: the new trailer lands, the directory does not.** The trailer
passes every §6.2 gate — its magic, its own CRC, and committed_file_length equals the
physical size. The directory region CRC then fails ⇒ **F20, reject-file**. §9.6's probe
finds the new trailer as a *candidate* (magic, CRC, and committed_file_length = o + 64 all
hold) and the whole-file re-verification rejects it: "a candidate whose whole-file
re-verification fails was not a commit state, so the tool continues the probe past it". The
prior generation is then found. I checked this path specifically because it is the one where
a naïve recovery tool truncates to a wrong candidate.

**(6) Crash during [R-LIF-04]'s "overwrite from F" branch.** The physical file may legally
be longer than the new committed_file_length for the duration of the commit; the truncate is
owed "no later than step 6". A crash between writing the new trailer at F_new − 64 and
truncating leaves the new trailer *buried*, with stale residue after it. The next reader
sees residue at physical − 64 ⇒ **F8**. §9.6's backward probe finds the buried trailer,
whose committed_file_length = o + 64 holds, and whole-file re-verification succeeds —
recovery lands on the *new* generation, which is correct. I could not construct a case where
this branch produces a candidate that re-verifies but is the wrong state, because the only
64-aligned trailer-shaped bytes below the buried one belong to genuine earlier generations.

One residual the document names and does not defend: a payload can carry a byte string that
mimics a trailer, and a mimic that is itself a consistent whole file survives re-verification.
[R-LIF-06]'s second caution and §21.6's "payload contains a byte string that mimics a
trailer" row both say so. Rollback needs out-of-band state, and "A signed committed file
length is not among them — the value is exactly what the re-append reproduces."

---

## 5. Byte-divergence catalogue, checked item by item against Appendix G

Given identical input arrays and identical stated options, here is every legitimate way two
conforming writers may differ, and which Appendix G item closes it.

| # | Degree of freedom | Rule that leaves it open | Closed by |
|---|---|---|---|
| 1 | tile extents Tᵢ | §11.3's Note | item 5 |
| 2 | layout (interleaved / planar) | [R-SER-06] | item 5 |
| 3 | codec 1–4 | [R-COD-03] | item 1 |
| 4 | encoder freedom *within* a codec (block/match/table choices, threads) | [R-COD-05]/[R-COD-06]/[R-COD-07] constrain decoders, not encoders | item 1, by pinning the producer |
| 4a | a raw DEFLATE stream's unused final-byte high bits | §17.2's Note: "This specification constrains them nowhere" | item 1 |
| 5 | filter 1 or 2 | [R-COD-09] | item 5 |
| 6 | declared alignment A / slab (S, A_slab) | [R-SLB-01], [R-SLB-02] | item 5 |
| 7 | placement and ordering of every structure | [R-SLB-05] | item 3 |
| 8 | gap *content* | [R-CNT-03] is a SHOULD | item 3 ("every byte of every such gap is zero") |
| 9 | gap *extent* | [R-SLB-05] | item 3 |
| 10 | record order, and sub-record order | [R-CNT-14] | item 3 |
| 11 | file_id | [R-LIF-03] states only advice | item 2 |
| 12 | version_minor above the floor; ignore-lane flags | [R-CNT-26] is a SHOULD | item 8 |
| 13 | the fill recorded when the caller chooses none | [R-TYP-10] is a SHOULD | item 7 |
| 14 | storing vs sentinelling an all-fill tile | nothing requires either | item 6 |
| 15 | number of generations | §9 nowhere constrains it | item 4 |
| 16 | user-metadata JSON text (number formatting, whitespace, escapes) | [R-MTA-05]: sorting "does not make two writers' output identical" | item 9 |
| 17 | user-metadata storage encoding 1 vs 2, and the zstd encoder | [R-MTA-03] | item 9 |
| 18 | name normalisation (NFC vs NFD) | [R-ENC-14] is a SHOULD | item 10 |
| 19 | a compactor's fresh file_id | [R-WRT-06] requires a *draw* | **left open, and item 8 says so** |
| 20 | a compactor's choice to drop an MU=0/PE=0 record | §20.4 | **left open, and item 8 says so** |
| 21 | a compactor's version_minor where it carries an unimplemented feature | §20.5 | **left open, and item 8 says so** |

Items 19–21 are acknowledged in terms: "A compactor's output is therefore reproducible only
modulo its trailer and the records §20.4 lets it drop … An adopter needing byte-identity
across compactors pins the compactor". That is an honest closure of an open item, not a gap.

**What is *not* a divergence, and I checked each:**

- Linearization and index_encoding — only value 1 is emittable in format major 1.
- The segment CRC of a full all-sentinel segment — [R-IDX-05] lets a writer emit the
  constant `0xEECB3BB2` without computing it, but the constant **is** the computed value. I
  verified: CRC-32C of 65,536 sentinel entries = `0xEECB3BB2`. No divergence.
- Padding-position content, pad-bit content, and interleaved bool byte values — fixed by
  [R-SER-05] and [R-SER-08].
- Trailer reserved bytes, record reserved flag bits, registered types' MU/PE bits — all
  fixed.
- The pre-trailer pad's *length* — [R-LIF-02] step 5 forces the minimum, and §6.2 confirms:
  "a longer gap is conforming, and no conforming commit produces one."
- Declared dimension order and channel order — these change what the layer *denotes*
  (§11.4's Note on column-major ecosystems, §3.1 on channel index), so two writers given
  the same input array are not free in them.
- An appender relocating a stored payload byte-for-byte (superseding it at a new offset) is
  permitted and wasteful; item 4's "one generation" removes it from the profile's scope.

**Falsifiable claims in Appendix G that I checked and that hold:**

- Item 5's identity claim: "The filter is the identity exactly where its permutation is —
  where the stride is 1 … and equally where the decoded image is a single group, n = L/s
  being 1". I checked the permutation p = j·s + i ↦ i·n + j. Identity requires
  j·s + i = i·n + j for all i < s, j < n; setting i = 0 gives j(s−1) = 0 for all j < n, so
  either n = 1 or s = 1. **Exactly** those two cases. The claim is correct.
- Item 2's hash input is well defined and non-circular: [0, F − 64) followed by the
  trailer's first 60 bytes with file_id zeroed excludes the trailer CRC, which is the only
  field that depends on file_id. F is known before the hash is taken. Correct.
- Item 3's tie-break key ("the record's header with **extent_offset masked to zero**") is
  content-derived and non-circular, and the claim that two records the key does not separate
  yield the same file under either order is right: they are byte-identical apart from
  extent_offset, and swapping them swaps the two offsets back into the same positions.
- Item 4's refutation route: nothing in the file *records* a commit count (§9.3's Note, §23.2),
  so only §9.6's backward probe refutes it. Correct.

**Two claims in Appendix G that I can falsify** are findings W-01 and W-02 below.

---

## 6. Findings

### W-01 — AMBIGUITY. Appendix G item 3 says "a declared alignment" where the same sentence elsewhere says "a declared A or A_slab", and neither constrains a non-tile structure

**Location.** Appendix G, item 3 (non-normative).

**Quotation.**

> The first structure begins at 16, directly
> after the front signature block, which §5.2 counts as no
> structure — or, where a declared alignment admits no structure at
> 16, at the least position above it the declaration admits; each
> later structure begins where the previous one
> ended, save where alignment forces a gap — a
> declared A or A_slab, or §6.2's 64-byte trailer alignment, the
> pre-trailer pad included — and every byte of every such gap is zero

Two readings of "a declared alignment", and a third gap on top of them.

**Reading 1 — A only.** The very next clause of the same sentence names "a declared A or
A_slab" explicitly, so the bare "a declared alignment" three clauses earlier reads
naturally as the per-tile alignment A alone. Under this reading, a profile adopter whose
first layer by name declares a slab with A_slab = 4096 places that layer's first stored
tile at offset 16, because no *A* is declared. That tile is the first stored tile of run 0,
and [R-SLB-03] requires "the first stored tile's offset satisfies offset mod A_slab = 0".
16 mod 4096 ≠ 0, so the emitted file exhibits **L42** and is nonconforming.

**Reading 2 — A or A_slab.** "Alignment" is generic, and the first structure goes at the
least admissible position above 16 under whichever declaration governs the structure being
placed.

**Which I picked, and why.** Reading 2. Reading 1 makes item 3 instruct a writer to emit a
nonconforming file, and Appendix G opens by saying "It adds no requirement to any actor: a
writer ignoring it is fully conforming" — a profile that produced nonconforming output would
be worse than useless. But the sentence supplies that reasoning nowhere; I had to supply it.

**A separate gap the same clause carries.** Neither A nor A_slab constrains a structure that
is not a stored tile. [R-SLB-01] binds "every stored tile's offset"; [R-SLB-03] binds "the
run's stored tiles" and "the first stored tile's offset". So when the first structure under
item 3's order is *not* a stored tile — which happens whenever the first layer by name
addresses tiles but stores none, so that its tile-index region leads — "a declared alignment
admits no structure at 16" is simply false: the region may sit at 16, whatever the layer
declares. Two adopters can read this either way and place that region at 16 or at A,
producing two different but equally conforming files from identical input. That defeats
exactly the property item 3 exists to give.

**What an implementer does wrong without it.** Under reading 1 they emit an L42 file. Under
the non-tile-structure gap they emit a file that is conforming but not reproducible against
another adopter's — which is the profile's whole purpose.

**Byte-level:** no. Appendix G is a non-normative appendix and explicitly adds no
requirement to any actor. Reading 1's output is barred by [R-CNF-05] under both readings
because it carries L42, so the emittable set does not move; the divergence in the non-tile
case is between two conforming files that the core rules already both permit.

---

### W-02 — CONTRADICTION. Appendix G item 5's stated reason for pinning the layout is falsified by §14.4's own Note for a single-channel numeric layer

**Location.** Appendix G, item 5 (non-normative), against §14.4's Note.

**Quotation, Appendix G item 5:**

> Without both pinned, two writers agreeing on everything
> above still disagree on bytes: the tile extents fix every tile's
> shape and with it the grid count, while the layout fixes how many
> tile-index entries the layer addresses (§11.2) and how each tile's
> values are arranged (§14.2).

**Quotation, §14.4's Note:**

> **Note.** A single-channel numeric layer produces byte-identical
> tile images under either layout.

**The falsification.** Take a layer with C = 1 and a numeric channel.

- *"how many tile-index entries the layer addresses"*: [R-GEO-03] gives N for an interleaved
  layer and C·N for a planar one. At C = 1 these are equal. The layout changes nothing.
- *"how each tile's values are arranged"*: §14.4's Note states outright that they are
  byte-identical. The layout changes nothing.

Both stated mechanisms are inoperative, yet the item is still needed, because the layer
record's own `layout` field holds `01` under one choice and `02` under the other — one byte
that differs and that no other item pins. The reason the item gives is not the reason it is
needed.

**What an implementer does wrong without it.** A profile adopter whose layers are
single-channel float32 arrays — the commonest scientific case there is — reads item 5's
justification, observes that neither mechanism applies to their data, concludes that pinning
the layout is unnecessary for them, and ships a writer that leaves the layout to a caller
default. Two such writers then emit files differing in one byte of every layer record,
breaking byte-identity, which is the only thing the profile exists to deliver.

**Byte-level:** no. Appendix G is non-normative and adds no requirement to any actor; both
layouts are conforming and already permitted by [R-SER-06], so the emittable set does not
move.

---

### W-03 — AMBIGUITY. §20.3 step 4's enumeration of "entries new to this generation" names a cause that produces no new entry

**Location.** §20.3, step 4, `[R-WRT-04]`.

**Quotation.**

> with entries for tiles this commit stores or supersedes written to their new state,
> entries for tiles that become unstored written as the sentinel, entries new to this
> generation (added tiles, grown extents, an appended channel) emitted per §15, and every
> other entry byte-identical at its disk-ordinal position

**Reading 1 — "added tiles" means tiles this commit newly stores.** This is what the phrase
says on its face, and it is wrong: an addressed tile has an entry in *every* generation
(§15.1, "the entry for the tile with disk ordinal k is the k-th entry"). A tile that goes
from unstored to stored occupies an entry that already existed as a sentinel. Its entry is
not "new to this generation"; it is the *first* clause's subject — "tiles this commit stores
… written to their new state". Under this reading the clause's parenthetical contradicts its
own head.

**Reading 2 — "added tiles" means tiles added to the *addressed* set**, with "grown extents,
an appended channel" as the two ways that happens, the comma standing in for a colon. This
reading is coherent: the addressed-tile count is N (interleaved) or C·N (planar)
([R-GEO-03]), and among the changes step 4 permits, only a grown extent that raises a grid
count and an appended planar channel raise it. The document does use "tile" for an addressed
tile elsewhere in this very step ("a tile the new state does not address carries no
obligation").

**Which I picked, and why.** Reading 2, because reading 1 makes the parenthetical name a
member of the wrong clause, and because §3.1's "addressed tile / stored tile" distinction is
the document's own vocabulary.

**What an implementer does wrong without it.** Nothing at byte level: the four classes are a
partition of the re-emitted region's entries, and a newly stored tile lands in class 1 under
reading 2 and class 3 under reading 1, with the same twenty bytes emitted either way. What
it costs is confidence in the partition itself — an implementer verifying that the four
classes cover every entry exactly once will find "added tiles" straddling classes 1 and 3
and will not know whether the list is meant to be exhaustive.

**Byte-level:** no. Both readings emit the same index region.

---

### W-04 — OBSERVATION. §22.3 says every reachable byte belongs to a structure; [R-CNT-02] expressly makes the front signature block not a structure

**Location.** §22.3, `[R-SEC-03]`, against §5.2, `[R-CNT-02]`.

**Quotation, §22.3:**

> Byte coverage (`[R-CNT-02]`) partitions the *live* state
> exactly: every byte a reader can reach belongs to one named structure.

**Quotation, §5.2:**

> Every
> byte of the live committed state belongs to exactly one of: the front signature block; or a **structure** — a
> stored-tile extent, a record extent (the bytes any record's extent
> slot references, whatever the record's type, §7.2), the directory, or
> the trailer.

Bytes [0, 16) are in the live committed state and are reachable by any local reader — indeed
[R-CNT-04] *obliges* a reader holding them resident to verify them. They belong to no
structure in [R-CNT-02]'s sense, because [R-CNT-02] puts the front block on the other side
of its "or".

The document is not consistent with itself on this word. §8.1's coverage-map table heads its
first column **Structure** and its first row is "Front signature block". §9.7 avoids the
question by naming the block directly: "The front signature block at [0, 16) and the live
trailer at [F − 64, F) are claimed by the walk as well, being members of the live committed
state". And Appendix G item 3 hedges it explicitly — "the front signature block, which §5.2
counts as no structure" — which is the only place in the document that acknowledges the two
senses.

**What an implementer does wrong without it.** Almost nothing: a verifier that builds its
coverage walk from §9.7 gets it right, and §9.7 is where the walk is specified. The cost is
that §22.3 is the section a security reviewer reads, and it states a partition claim that is
literally false at the one place the partition has a special case.

**Byte-level:** no. No reader, writer, updater or verifier behaviour turns on the word; §9.7
states the walk's claimants by name.

---

## 7. Evidence: what I ran, what I derived, what I closed

### 7.1 Control test on the search method

Before resting on any zero, I searched the normalised text for phrases I knew were present.
`'slab or alignment'` returned **4**, `'declared, changed'` returned **4**,
`'extended at its end'` returned **2**. All four "slab or alignment" hits and all four
"declared, changed" hits span hard-wrapped line breaks in the source and would have returned
**0** under a line-oriented `grep`. That is the control: the normalisation works, and the
zeros I report below are real zeros.

### 7.2 Derived numbers, against the document's own figures

Every CRC below is from my own reflected-CRC-32C implementation, itself check-vectored
first.

| I computed | Value | Document states | Match |
|---|---|---|---|
| CRC-32C(`"123456789"`) | 0xE3069283 | §4.5: 0xE3069283 | yes |
| CRC-32C(zero bytes) | 0x00000000 | §4.5: 0x00000000 | yes |
| CRC-32C of 4 sentinel entries (80 bytes) | 0x80A34955 | §7.4 Example: 0x80A34955 | yes |
| crc_of_crc_array over that 4-byte array | 0xC4EE982E | §7.4 Example: 0xC4EE982E | yes |
| CRC-32C of 2¹⁶ sentinel entries | 0xEECB3BB2 | §15.4, Appendix B: 0xEECB3BB2 | yes |
| Appendix A trailer CRC over bytes [0,60) | 0x402F157E | Appendix A: 0x402F157E | yes |
| §7.4's example inline payload: 4 + 34 + 18 + 12 + 13 | 81 | §7.4: "81 bytes … 81 exactly" | yes |
| §7.4's extent length 4×20 + ⌈4/2¹⁶⌉×4 | 84 | §7.4: 84 | yes |
| register rows: F 35 (F11 struck), L 49, T 26, R 10 | **120** | §21.2/3/4/5 headers: 35, 49, 26, 10; §21.8: "120 conditions" | yes |
| register instances, counted mechanically by semicolons (a `—` cell = 1) | **277** (F 56, L 116, T 55, R 50) | §21.8: "277 instances" | yes |
| row-number gaps | only F11 | §21.2's Note: "Row label F11 is struck" | yes |
| §15.4 example: ⌈10⁶/2¹⁶⌉ | 16 segments, last covering 16,960 | §15.4: "16 segments (15 full, the last covering 16,960)" | yes |
| §15.4 example: region 10⁶×20 + 64 | 20,000,064 | §15.4: 20,000,064 | yes |
| §15.4 example: 20×(999,999 − 983,040) | 339,180 | §15.4: 339,180 | yes |
| §15.4: one full segment 65,536×20 | 1,310,720 = 1.25 MiB | §15.4: "1.25 MiB" | yes |
| §15.4 example: disk ordinal 2·32+10 = 74, entry at 74×20 | [1480, 1500) | §15.4: [1,480, 1,500) | yes |
| §11.4 example: 300 div 256 = 1, 700 div 256 = 2, s = 1·8+2 | 10; in-tile 44·256+188 | §11.4: 10; 11,452 | yes |
| §14.2 example: P=6, Q=3, ordinal 5 at 5·3 | 15, sample [15,18) | §14.2: [15, 18) | yes |
| §14.3 example: fill true ⇒ byte1 = 0x01 \| 0xFC | 0xFD | §14.3: `55 FD` | yes |
| §17.3 example: shuffle of 1.0/2.0/3.0 at s=4, n=3 | `00 00 00 00 00 00 80 00 40 3F 40 40` | §17.3: identical | yes |
| §20.3 example: 32·20 + 4 | 644 | §20.3: 644 | yes |
| §21.9 Note: 2³²/2¹⁶ × 4 | 256 KiB; at 2³⁶, 4 MiB | §21.9 Note: 256 KiB, 4 MiB | yes |
| §9.3 Note: largest multiple of 64 ≤ 2⁶³−1 | 2⁶³ − 64 | §9.3 Note: 2⁶³ − 64 | yes |
| §4.6 example: `température` NFC / NFD | 12 / 13 bytes | §4.6, Appendix G item 10: 12 and 13 | yes |
| **my own file:** F, live-state bytes, slack | 576, 558, 18 | — (my construction) | internally consistent |
| **my own file, commit 2:** F₂, slack | 1024, 466 | — | internally consistent |

Not one of the document's stated numbers came out wrong. This is the cleanest arithmetic
surface I have walked.

### 7.3 Sweeps run, with hit counts

Over the normalised, `> `-stripped text:

- `'slab or alignment'` — **4** (§11.1 Rationale; §20.3 step 4's exception list; §20.3's
  "governs placement" clause; Appendix H's updater entry). I read all four in full context.
- `'declared, changed'` — **4**: three reading "declared, changed or cleared" (§11.1,
  §20.3's list, Appendix H) and one reading "declared, changed or kept" (§20.3's delegated
  clause).
- `'changed or cleared'` — **3**; `'changed or kept'` — **1**; `'or is cleared'` — **1**.
- `'extended at its end'` — **2**; `'shortened from its end'` — **1**;
  `'shortened from it'` — **2**; `'MAY be extended'` — **1**; `'channel list may be'` — **1**.
- `'alignment declaration'` — **4**; `'slab declaration'` — **9**; `'aligned layer'` — **1**.
- Register-row extraction: `^\| (F|L|T|R)[0-9]+ \|` — **120** rows, from which I counted the
  Instances column mechanically.
- Row-number enumeration per prefix — F 1–36 minus 11, L 1–49, T 1–26, R 1–10, no other gaps.

### 7.4 Suspicions I opened and the sentence that closed each

1. **The closed list's fifth member lost a verb: is a transition now unnamed?** I enumerated
   every transition a slab or alignment declaration can make — none→some, some→another,
   some→same, some→none, and the exclusive switch in one commit. "declared" covers the
   first, "changed" the second, "cleared" the fourth, and the switch is two of "these
   changes" made at once. The third — some→same — needs no verb, because it is not an
   exception at all: the head of the list is "A layer that stores a tile … **keeps its
   declarations**, with these exceptions". *Closed by:* "A layer that stores a tile **in the
   generation this commit supersedes** keeps its declarations, with these exceptions and no
   other".

2. **The delegated clause names "kept", which the member does not — is that a divergence?**
   The member permits three dispositions; the delegated clause states an *invariant
   obligation* over four. "Kept" is not a permission the member owes, and the clause's four
   dispositions are exactly the four states a slab declaration can be in after a commit, so
   the sets agree. *Closed by:* "on a layer this commit modifies, a slab declaration
   declared, changed or kept has its invariants satisfied over every run of the new state,
   the runs this commit adds included, or is cleared".

3. **Does the §20.3 restatement's quantifier match [R-SLB-04]'s?** I put them side by side.
   §20.3 ranges over "a layer this commit modifies"; [R-SLB-04] over "a layer slab-declared
   in either the superseded or the new generation" whose commit changes one of five listed
   things. Every case in [R-SLB-04]'s domain is a layer the commit modifies, and every case
   in §20.3's domain is either satisfied trivially (nothing moved, so [R-SLB-03] already
   held) or in [R-SLB-04]'s domain. The alignment half needs no [R-SLB-04] analogue because
   [R-SLB-01] is a file invariant and [R-CNF-05] bridges to the writer. *Closed by:*
   [R-SLB-01]'s "When declared: every stored tile's offset satisfies offset mod A = 0", read
   against "an aligned layer's stored tiles, every one the new state holds and those this
   commit adds included, satisfy its invariant or the declaration is cleared".

4. **Do the two non-normative restatements of the closed list drop §20.3's "of one channel
   list" qualifier?** §11.1 says "one or the other in a commit" and Appendix H says "(not
   both in one commit)", neither carrying "of one channel list". If read globally, both would
   bar a commit that extends layer X's list and shortens layer Y's, which §20.3 permits.
   *Closed by:* the grammatical subject in each case is singular — §11.1's is "a planar
   layer's channel list", Appendix H's is "a layer that stores a tile in the generation its
   commit supersedes" — so the qualifier is already scoped by the subject. No divergence.

5. **Can a layer that stores a tile ever reach entry_count = 0, making §20.3's "(0, 0)"
   clause reachable for it?** Extents may grow and not shrink, tile extents are fixed, and
   [R-GEO-01] floors C at 1, so N and C·N can only rise from ≥ 1. *Closed by:* "a dimension
   extent MAY grow, and MUST NOT shrink" plus "`[R-GEO-01]`'s floor of one channel".

6. **Does "nothing else this step permits moves [an ordinal]" hold?** Disk ordinal is
   c·N + s ([R-GEO-06]). A name change, a channel appended at the end, and a channel removed
   from the end all leave N and every retained c unchanged; only a grown extent that raises a
   grid count moves one. *Closed by:* "a growth renumbers ordinals wherever `[R-GEO-06]`
   moves them, and nothing else this step permits moves one" — verified against every member
   of the exceptions list.

7. **Can entry_count stay unchanged across a channel shortening, making §20.3's hedge
   vacuous?** Yes, when a growth is composed with it: C=4, N=10 → C'=2, N'=20 gives 40 both
   times. *Closed by:* the hedge is exactly right — "whether or not entry_count changes with
   it (`[R-CNT-17]`) and whether or not a retained ordinal moves".

8. **Is a structurally-rejected index entry checked against the alignment invariant?**
   §16.1 says "every stored tile's offset", and §3.1 makes any non-sentinel entry's tile
   "stored", which would reach it. *Closed by the paragraph above the table:* "Such an entry
   contributes no stored extent to the *verifier* rows, which bind over well-formed entries'
   extents only". §16.2 says the same for run continuity.

9. **Is the slab invariant really "decidable from the index entries alone", given that one
   row turns on a stored tile's CRC?** It is: transparency is decided by *structural*
   well-formedness, which needs only the entry's 20 bytes and F. A well-formed entry is never
   transparent, whether or not its CRC passes. *Closed by:* "An entry whose only defect is
   that its stored bytes fail its crc is not transparent — its offset and length stand".

10. **Does [R-IDX-02]'s "non-sentinel entries only" leave an entry with offset = length = S
    and crc ≠ 0 exposed to [R-ENC-03] at layer scope?** No: an index entry's owning scope is
    the tile (§15.1), so [R-ENC-03] would give reject-tile anyway, and §15.3's preamble
    settles it regardless. *Closed by:* "The per-entry outcomes below govern notwithstanding
    the general owning-scope mapping of `[R-ENC-03]`/`[R-ENC-04]`".

11. **Is §15.3's "Six rows are marked *structural*" the right count?** I counted: rows 2–7 of
    the eleven-row table. Six. *Closed by* the count itself.

12. **Does the commit protocol leave the pre-trailer pad's durability unspecified?** It does,
    and it does not matter: the pad is slack. *Closed by:* "Slack has no internal structure
    this specification defines, its content is unconstrained, and no conformance requirement
    applies to it."

13. **Does [R-WRT-09] oblige a compactor to verify a checksum that does not exist, for an
    unassigned-type record's extent?** Its "each relocated extent's checksum" lacks §9.7's
    guard "where §8.1's map states one". *Closed by:* §22.3's flat statement that such an
    extent is carried "forward unread" and that "nothing an updater does would surface the
    damage", plus §4.5's express carve-out and §8.1's "none — the bytes are opaque" row.
    The document decides this three times over.

14. **Does §20.3's alignment clause contradict [R-WRT-01]'s "a violation latent in a
    structure they carry forward unmodified travels with it" on a nonconforming input?** I
    built the case: an input with A = 4096 and a retained unaligned tile (L40, a verifier row
    an appender need not detect), then a commit that adds an aligned tile. *Closed by:*
    [R-WRT-03]'s depth already reaches every entry of a re-emitted region ("the §19.4 index
    chain for every segment whose entries the commit reuses"), so the appender does read
    every offset and can discharge the clause; and in any case the disputed output carries
    L40 under both readings, so [R-CNF-05] bars it either way and the emittable set does not
    move.

15. **Does a slab with S = 1 defeat §16.1's 512-byte floor on A?** It does exactly reproduce
    per-tile alignment at any power of two down to 1, since each run is one ordinal and
    contiguity is vacuous. But both declarations are conforming and denote the same
    placements, so nothing is contradictory. *Closed by:* [R-SLB-03]'s "the first stored
    tile's offset satisfies offset mod A_slab = 0" — with S = 1 every stored tile is a run's
    first, which is a redundancy, not a defect.

16. **Does §20.3's "(T3, T14, T21, T22, T4, T5, T2) … (T24, T25)" omit witnesses, making
    "no check any actor owes able to see it" false?** A changed codec declaration would also
    trip T17 (missing zstd magic), T23 and others. *Closed by:* those are all instances of
    "a decode that fails outright under a changed codec or filter", which the sentence
    already names; extra witnesses only strengthen the "but for" clause rather than falsify
    it.

17. **Does §21.9's "the layout fixes how many tile-index entries the layer addresses" hold at
    C = 1?** It does not — and this became finding W-02, since the same claim is load-bearing
    in Appendix G item 5. (§21.9 itself does not make the claim; only item 5 does.)

18. **Does Appendix G leave writer-injected `tarn.created` open?** *Closed by:* §18.1's "Its
    content is application data: this specification defines its encoding, not its meaning" —
    the document's content is input, and item 9 pins the serialisation of it.

19. **Is Appendix F missing a normative reference my walk needed?** I listed everything the
    writer path depends on externally — BCP 14, RFC 3720 §12.1, IEEE 754-2019 (including the
    decimal→binary64 conversion §18.2 needs), RFC 1950/1951/1952, RFC 8878, the pinned LZ4
    Block Format revision, RFC 8259, RFC 3339, RFC 9110, Unicode — and found every one
    present. bfloat16 needs no external reference because §12.1 defines it by identification
    with binary32. Appendix F carries no "(non-normative)" marker and is therefore normative
    under [R-CNF-01], which is correct for a normative-references appendix.

20. **Does §21.2's reach derivation hold?** "Deriving it there yields F8, F14, F6 and both of
    F1's instances … and no other row." I re-derived it against [R-CNT-24]'s permanent list —
    trailer magic at F − 64, version fields at F − 56, CRC at F − 4 over [F − 64, F − 4), and
    the constant front block. F8 (magic), F14 (trailer CRC), F6 and F1's two instances
    (magic bytes and the front block) all assert one of those. F13's 64-alignment, F17's size
    cross-check, F12's file_id, F15's reserved bytes and F5's 128-byte floor assert nothing
    on that list. The derivation is right.

### 7.5 Where I found little, and what would have found something

**Torn-write recovery.** I found nothing. What would have found something: I ran six distinct
crash points, including the two hardest — a reordered barrier where the trailer lands and the
directory does not, and a crash inside [R-LIF-04]'s "overwrite from F" branch that buries a
valid new trailer under stale residue. In each I traced which §21.2 row a reader hits, whether
§9.6's probe produces a candidate, and whether whole-file re-verification accepts it. The
buried-trailer case is the one that would break a naïve recovery tool, and the document
handles it: the probe walks 64-aligned offsets over the *physical* file, and every candidate
is re-verified whole. I am confident this area is clean.

**Creation byte layout.** I found nothing. What would have found something: I emitted a real
576-byte file with two layouts, edge padding, pad bits, a sentinel, and a metadata extent,
and cross-checked every derived quantity — index-region length against [R-CNT-17]'s formula,
decoded sizes against §14.2/§14.3, padding content against §14.5's worked example (whose
geometry I deliberately matched), and the slack total against F. A missing or contradictory
rule would have shown up as a byte I could not decide. There was none. I am confident.

**The record-flag walk.** I found nothing. What would have found something: I enumerated all
ten combinations of {registered / implemented-unregistered / unimplemented} × {MU, PE},
including the MU = 1 / PE = 0 combination readers must re-read as PE = 1, and traced each to
its §20.4 row, its scope, and its effect on a compactor. §20.4 fixes the flag authority
*before* the table, which is what makes the walk decidable; every cell resolved. Confident.

**Slack accounting.** I found nothing. What would have found something: the abandoned-partial-
write row, where a careless document would have said "the residue is slack" and this one says
the total "is not owed at all … which is not a partial total but the absence of one". I
checked the partial-total machinery too ([R-CNT-21] against §9.7's list of what makes a walk
incomplete) and the two lists agree item for item. Confident.

**The byte-divergence catalogue.** I found two falsifiable claims (W-01, W-02) and I am
*less* confident here than elsewhere, because Appendix G is long, dense, and non-normative,
and because "every legitimate way two writers may differ" is an open-ended enumeration
rather than a closed one. I built my list of twenty-one degrees of freedom from the rules
that leave each open rather than from the appendix's items, precisely so the appendix could
not seed the list — and then matched item to freedom in both directions. Three freedoms
(19–21) are left open and the appendix says so in terms. If something is missing from my
catalogue it is a freedom that arises from a rule I did not think to read as permissive.

**A byte-level fork.** I did not find one, and I want to be plain about that rather than
reach. Every candidate I opened either produced a nonconforming file under both readings
(items 14 above), or lived in text that adds no requirement to any actor (W-01, W-02), or
emitted the same bytes under both readings (W-03), or was settled by a governing sentence
above the one I was reading (items 2, 3, 8, 10, 13). The changed surface in my lane — the
closed list, its delegated clause, and its three restatements — is the most carefully
composed passage in the document, and I checked its transitions, its partition, its
composition of changes, and its quantifiers against [R-SLB-01], [R-SLB-03] and [R-SLB-04]
one at a time. I could not break it.

**Finding count in this transcript: 4** (W-01, W-02, W-03, W-04).
