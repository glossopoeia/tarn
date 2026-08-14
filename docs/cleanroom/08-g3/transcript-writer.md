# Round 8 — Writer implementer transcript

## 0. Access disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in four `Read` calls covering lines 1–3843 (the whole document). I ran six
`grep` invocations against that same file, all of them to confirm that
passages I intended to quote were verbatim and to locate wrapped sentences
my earlier reads had split across lines.

I ran three Python scripts. None of them read any file: each embeds its own
CRC-32C table and constructs the byte images inline from literals I typed.
I opened no ADR, no `docs/` file, no `conformance/` directory, no
`registry.json`, no `PLAN.md`, no `AGENTS.md`, no git history, and did no web
access. I did not list any directory. The one path I wrote to is this
transcript.

Where I mention behaviour of DEFLATE, zstd, LZ4, JSON or IEEE-754 I am using
outside knowledge to *generate suspicion*; every conclusion below about what
TARN requires is cited to a section of the document.

---

## 1. Method and instrument checks

Before trusting any arithmetic I validated my CRC-32C against every constant
the document publishes, because a writer that gets the checksum wrong
produces a file that is wrong everywhere at once and I would have found
nothing.

```
CRC-32C("123456789")                = 0xE3069283   §4.5 check vector      OK
CRC-32C(zero bytes)                 = 0x00000000   §4.5 check vector      OK
CRC-32C(2^16 sentinel entries)      = 0xEECB3BB2   §15.4 [R-IDX-05]       OK
```

Then I reconstructed Appendix A's 128-byte minimal file from the field table
alone — not from the hex dump — and computed its trailer CRC:

```
trailer[0,60) = 8a 4e 52 41 54 0d 0a 1a 01 00 00 00 00 00 00 00
                01 00 00 00 00 00 00 00 10 00 00 00 00 00 00 00
                04 00 00 00 00 00 00 00 80 00 00 00 00 00 00 00
                ef cd ab 89 67 45 23 01 00 00 00 00
CRC-32C        = 0xE00938D2, stored little-endian as D2 38 09 E0
```

which is byte-identical to Appendix A's line `0070`. So §6.2's field table,
§4.5's checksum definition, and Appendix A agree with each other and with an
independent implementation. That is a good sign about the document and it is
also the only reason I trust the numbers below.

I also re-derived every worked example the document gives that bears on
writing, because they are the cheapest cross-check available on the rules I
was about to depend on:

- §11.4's ordinal example: coordinate (300,700) with tile extents (256,256)
  → tile (1,2), s = 1·8+2 = 10, in-tile position (44,188), in-tile ordinal
  44·256+188 = 11,452; planar channel 2 → 2·32+10 = 74. Reproduces.
- §14.2's stride example: interleaved (uint8, uint16), Q = 3, P = 6, decoded
  size 18, ordinal 5 at bytes [15,18). Reproduces. The `t`(float32)+`m`(bool)
  variant, Q = 5, size 30, ordinal 5 at [25,30). Reproduces.
- §14.3's packed-bool example: P = 10 alternating from true → `55 01` with
  fill false, `55 FD` with fill true (pad bits 2–7 carrying the fill bit).
  Reproduces bit for bit.
- §17.3's shuffle example: 1.0f, 2.0f, 3.0f, s = 4, n = 3 →
  `00 00 00 00 00 00 80 00 40 3F 40 40`. Reproduces.
- §15.4's segmentation example: entry_count 1,000,000 → 16 segments (15 full
  + 16,960), region 20,000,064 bytes, entry 999,999 at segment-relative
  339,180, segment 15 at region [19,660,800 , 20,000,000). Reproduces.
- §20.3's cost example: 32-tile index = 32·20 + 4 = 644. Reproduces.

Nothing in that set is wrong. I mention it because it means the arithmetic
spine of the writer path — grid counts, ordinals, strides, segment layout,
CRC — is unambiguous, and the findings at the end are all somewhere else.

---

## 2. Creating a file: the byte-layout walk

### 2.1 What I chose to build

A two-layer file, chosen so that every writer-side mechanism I could reach
without a compressed codec is exercised at least once:

- **`elev`** — interleaved, rank 2, dims `y`(E=5,T=4) and `x`(E=5,T=4), one
  channel `h` of type uint16 with fill `0xABCD`. Grid (2,2), N = 4, P = 16,
  Q = 2, decoded tile size 32. Codec 1, filter 1, no alignment, no slab.
  Three tiles stored, the corner tile a **sentinel** — so the layer is
  sparse, has **edge padding** on two sides, and has a tile whose only real
  sample position reads as fill.
- **`mask`** — planar, same geometry, two channels: `m` (bool, fill `0x00`)
  and `w` (float32, fill `+0.0`). C·N = 8 addressed tiles. Codec 1, filter 1,
  **slab S = 4 with A_slab = 64**. This gives me a packed boolean plane
  (⌈16/8⌉ = 2 bytes), a numeric plane (16·4 = 64 bytes), two slab runs, and
  channel-major disk ordinals.
- One **file-scope user-metadata record** with its document in an extent.

### 2.2 The order in which I actually emitted bytes

`[R-LIF-02]`'s creation path is explicit: *"On creation there is no prior
trailer: the writer first emits the front signature block (§6.1) … then
performs steps 2–6 beginning at offset 16, with generation 1."* So:

1. front signature block
2. payloads and index regions and record extents, in any order satisfying
   §5.2's coverage classes
3. the complete directory + its CRC
4. **barrier**
5. pad to the next 64-byte boundary, then the trailer
6. **barrier**

§20.2 restates it and adds *"both barriers, not one"*, which is the one thing
I would otherwise have got wrong: my instinct was a single fsync before the
trailer. The document is unambiguous that the trailer needs its own.

Within step 2 the order is mine (`[R-SLB-05]`: *"its stored tiles MAY occupy
any non-overlapping byte positions, in any order"*). I emitted `elev`'s tiles
in disk-ordinal order, then its index, then `mask`'s two runs, then its index,
then the metadata extent.

### 2.3 Tile content — the two places content is fixed, not chosen

**Edge padding.** `elev` tile 1 (tile coords (0,1)) covers x = 4..7 of a
5-wide axis: one real column and three padding columns. `[R-SER-05]` fixes
their content: *"at every padding position, a writer MUST encode, for each
channel the position carries, that channel's fill value."* So tile 1 is:

```
04 00 cd ab cd ab cd ab   68 00 cd ab cd ab cd ab
cc 00 cd ab cd ab cd ab   30 01 cd ab cd ab cd ab
```

— the four real samples (x=4 at y=0..3: 4, 104, 204, 304) each followed by
three copies of the fill `CD AB`. In-tile ordinal is u_y·T_x + u_x = u_y·4 + u_x
(§11.4), and §14.2's planar/interleaved table puts value k at k·B, so this
layout is forced, not chosen.

This matters for a writer in a way the document states only in a Rationale:
padding is inside the tile's CRC and inside the codec's input, so getting it
wrong is a silent content divergence between two writers with identical
inputs. §14.5's rationale says exactly that (*"padding participates in
compression and in the stored tile's checksum"*), and §21.4 T4 registers it
as a verifier-detected tile-scope violation.

**Padding bits in a packed plane.** `mask`'s bool planes have P = 16, so
P mod 8 = 0 and there are no pad bits — but there *are* padding positions,
and `[R-SER-05]` says the fill bit goes in them just the same. Plane 1 (tile
(0,1)) has real positions only at x = 4, i.e. in-tile ordinals 0, 4, 8, 12;
with my content rule (true where (y+x) is even) that gives bits {0, 8} set
and everything else — including all twelve padding positions — carrying the
fill bit 0. Stored: `01 01`. Plane 0 is `a5 a5`, plane 2 `05 00`, plane 3
`01 00`.

The distinction between *padding positions* and *pad bits* (§14.3's note) is
one I had to read twice; it is correct and it is load-bearing for a writer,
because a plane can have many of the first and none of the second, which is
exactly my case.

### 2.4 The index regions

Under index_encoding 1 the region is entry array then segment-CRC array with
*"no padding anywhere inside the region"* (§15.1). `elev` has 4 entries, so
one segment: 4·20 + ⌈4/65536⌉·4 = 84 bytes, matching `[R-CNT-17]`'s
extent_length formula. Entries in disk-ordinal order:

```
ordinal 0  offset 16  len 32  crc D7839CC7
ordinal 1  offset 48  len 32  crc 6BE090F8
ordinal 2  offset 80  len 32  crc 82CA39C9
ordinal 3  FF×16 00×4                        <- sentinel, [R-IDX-02]
segment-CRC array (4 bytes) = 3D70539B
crc_of_crc_array (into the layer record)     = 0ABE35DF
```

`mask` has 8 entries in channel-major order (`[R-GEO-06]`: disk ordinal
c·N + s), one segment, 164 bytes: bool planes at ordinals 0–3, float32 planes
at 4–7.

Two things a writer must not get backwards here, and the document fixes both:
the segment CRC covers *the entry bytes as stored* (§15.4), and
`crc_of_crc_array` covers *the segment-CRC array*, not the entries. §8.1's
map states the chain and §8.2 orders it. I verified my chain end to end by
recomputing it from the emitted image rather than from the values I had
computed while building.

### 2.5 The slab, and what it forced

`mask` declares S = 4, A_slab = 64. `[R-SLB-02]` partitions ordinals by
channel block — `[0,4)` for `m`, `[4,8)` for `w` — and runs never span
blocks, so with S = 4 I get exactly two runs, one per channel. `[R-SLB-03]`
then forces, per run, that the stored tiles be *packed in ordinal order* and
that the run's first stored tile be A_slab-aligned:

```
run 0 (bool)   256 258 260 262   lengths 2 2 2 2   256 mod 64 = 0   packed
run 1 (float)  320 384 448 512   lengths 64 ×4     320 mod 64 = 0   packed
```

The 64-byte alignment forced two gaps that are pure slack: `[196,256)` = 60
bytes (from the end of `elev`'s index to run 0's aligned start) and
`[264,320)` = 56 bytes (from the end of run 0 to run 1's aligned start).
§16.1 and §16.2 both say these are slack and that writers SHOULD zero them
(`[R-CNT-03]`), which I did.

Note that A_slab constrains only the *first* stored tile of each run. Run 1
starting at 320 rather than 264 is my choice of the next aligned offset; a
writer could equally start it at 384 and waste more. That is legitimate
divergence, catalogued in §8 below.

### 2.6 The records

Layer record inline payload, packed in §7.4's table order with *"no alignment
or padding between them"*:

```
elev:  name(5) layout(1) linearization(2) codec(2) filter(2)
       A(8) S(8) A_slab(8) rank(1) C(2)
       dims 2 × [len+name(2) + E(8) + T(8)] = 36
       chans 1 × [len+name(2) + type(2) + filllen+fill(3)] = 7
       index_encoding(1) entry_count(8) crc_of_crc_array(4)
       = 95 bytes inline; record = 24 + 95 = 119

mask:  … C = 2 → chans 6 + 9 = 15 … = 103 inline; record = 127
meta:  header 24 + inline 1 (the encoding byte) = 25
```

Flags are not a writer choice: §7.3 fixes MU = 1, PE = 1 for type 0x0001 and
MU = 0, PE = 1 for 0x0002, and `[R-CNT-22]` makes a mismatch a verifier-detected
violation (F31/L50). So the layer records carry flags `03 00` and the metadata
record `02 00`.

The metadata document is 68 bytes of JSON plus the terminal CRC-32C §8.1
places in *"the final 4 bytes of the extent"* — extent_length 72, comfortably
above `[R-CNT-25]`'s floor of 5. Its two keys are `tarn.created` then
`tarn.creator`, which is ascending UTF-8 byte order at the `e` < `o` in
position 11, as `[R-MTA-05]` requires. That is a MUST and a real trap: the
obvious authoring order (`creator`, then `created`) is nonconforming, and
§21.2 F30 registers it — though as a verifier row, so no reader would ever
tell me.

### 2.7 Directory, pad, trailer

Record sequence 119 + 127 + 25 = 271, plus the region CRC = dir_length 275 at
dir_offset 812. §6.2 requires that *"no structure lies between its end and the
trailer"*, so the directory is necessarily last. Directory ends at 1087;
`[R-LIF-02]` step 5 pads to the next 64-byte boundary → **1 byte** of pad;
trailer at [1088,1152); **F = 1152**, a multiple of 64.

```
1088  8A 4E 52 41 54 0D 0A 1A   trailer magic
1096  01 00 / 00 00             version_major 1 / version_minor 0  [R-CNT-26] floor
1100  00 00 00 00               flags = 0 (creating writer, §6.3)
1104  01 …                      generation 1
1112  2C 03 …                   dir_offset 812
1120  13 01 …                   dir_length 275
1128  80 04 …                   committed_file_length 1152
1136  41 0B D2 55 7E 1A 3C 9F   file_id (random, nonzero, §9.3)
1144  00 00 00 00               reserved
1148  89 24 CE 81               trailer CRC over [0,60) = 0x81CE2489
```

### 2.8 Coverage check — the thing a verifier will do to me

I ran `[R-CNT-02]`'s partition and `[R-LIF-08]`'s walk over my own image:

```
front           [0,16)        16
elev/t0         [16,48)       32
elev/t1         [48,80)       32
elev/t2         [80,112)      32
elev/index      [112,196)     84
mask m planes   [256,264)      8
mask w planes   [320,576)    256
mask/index      [576,740)    164
meta extent     [740,812)     72
directory       [812,1087)   275
trailer         [1088,1152)   64
                            ----
claimed                     1035
slack   [196,256) 60 + [264,320) 56 + [1087,1088) 1 = 117
total                       1152 = F
```

Disjoint, every non-front/non-trailer claimant inside `[16, F−64)`, sum = F.
The verifier's slack total for this file is **117**.

### 2.9 Decision ledger for creation

| Decision | Fixed by the document? |
|---|---|
| front block bytes, trailer magic, field widths and order | fixed (§6.1, §6.2, §7.4, §15.1) |
| F multiple of 64; pad to next 64-byte boundary | fixed (§6.2, `[R-LIF-02]` step 5) |
| directory last, nothing between it and the trailer | fixed (`[R-CNT-05]`) |
| generation = 1, version_major = 1, flags = 0, reserved = 0 | fixed (§9.2, §6.2, §6.3) |
| in-tile ordinal, disk ordinal, decoded size, value offsets | fixed (§11.4, §14.2, §14.3) |
| padding-position and pad-bit content = fill | fixed (`[R-SER-05]`) |
| index entry layout, sentinel pattern, segmentation, CRC chain | fixed (§15, §8.1) |
| codec 1 ⇒ stored length = decoded size | fixed (`[R-COD-04]`) |
| slab packing and A_slab alignment of each run's first stored tile | fixed (`[R-SLB-03]`) |
| metadata key sort order | fixed (`[R-MTA-05]`) |
| version_minor = 0 | SHOULD (`[R-CNT-26]`) — mine in principle |
| file_id value | mine; SHOULD be random (`[R-LIF-03]`) |
| tile extents, layout, codec, filter, which tiles stored | mine (§11.3, `[R-SLB-05]`, Appendix G item 6) |
| placement and order of every structure inside step 2 | mine (`[R-SLB-05]`) |
| size of the alignment gaps | mine |
| whether gaps are zeroed | SHOULD (`[R-CNT-03]`) — mine |
| record order in the directory | mine (`[R-CNT-14]`) |
| **whether my first structure must start at exactly offset 16** | **not decided — finding writer-03** |

---

## 3. The append: commit 2

Task: correct the data in `elev`'s x-edge tile, and add a new layer `grad`
(rank 1, `t` with E = 0, T = 8, one float64 channel — a zero-extent layer, so
zero addressed tiles, extent slot (0,0), crc_of_crc_array 0, and **no payload
bytes at all**; `[R-GEO-02]`, `[R-CNT-17]`, `[R-CNT-23]`).

`[R-WRT-04]`'s six steps, with what each actually cost me:

**1. Establish F.** Validate the trailer in the final 64 bytes of the
*physical* file (`[R-LIF-04]`). It validates: F = 1152. If it had not, §9.4 is
categorical — *"the writer MUST NOT append, and locating the last committed
state is the deliberate recovery operation of §9.6 — never an implicit step
of opening for append."* That is the single most important sentence in the
updater path and I am glad it is stated as a prohibition rather than as
advice.

**2. Open.** §19.1's four steps. The appender is a reader here.

**3. Validate what the commit touches** (`[R-WRT-03]`): the trailer and the
**full** directory always — because re-emission relies on every directory
byte — plus §19.3's layer validation for `elev` (whose record and index I
modify), plus the §19.4 index chain *"for every segment whose entries the
commit reuses"*. `elev` has one segment and I reuse entries 0, 2 and 3, so I
verify `crc_of_crc_array` (0ABE35DF) and segment 0's CRC (3D70539B) before
copying those 60 bytes forward. I do **not** have to validate `mask`'s layer
record beyond the open, and I do **not** re-verify any retained tile's CRC —
*"Structures the commit neither modifies nor relies on impose no further
obligation."* That is a genuinely cheap append and the rule says so.

**4. Write payloads and indexes**, beginning at exactly F:

```
1152  new elev tile 1'          32 bytes
1184  elev index region', full   84 bytes
```

The index is re-emitted **whole** — `[R-WRT-04]`: *"Every layer whose
stored-tile set or index content this commit changes has its tile-index region
re-emitted in full … necessarily at a new placement"*. Entry 1 is re-pointed
to 1184 with a new crc; entries 0, 2 and the sentinel at 3 are byte-identical
at their disk-ordinal positions. `mask` is untouched, so its record keeps
extent slot (576,164) — pointing at bytes written in generation 1. This is
the thing that makes the format work and it is worth saying out loud: the live
committed state of generation 2 spans two generations' worth of physical
bytes, and §7.2 says so (*"whichever generation's commit appended them"*).

**5. Re-emit the directory.** Four records now: `elev` (modified — extent
slot and crc_of_crc_array both change), `mask` (byte-identical), the metadata
record (byte-identical), `grad` (new, 107 bytes). Record sequence 378 +
CRC = **dir_length 382 at dir_offset 1268**, ending at 1650.

**6. Commit.** Barrier; pad (−1650 mod 64 = **14** bytes) to 1664; trailer at
[1664,1728) with generation **2**, the **same file_id**, flags carried
forward, version_minor per `[R-CNT-26]`; barrier. **F₂ = 1728.**

The commit point is step 6. Between step 5 and step 6 the bytes on disk are
already the new generation — a concurrent reader that opens there sees
generation 2 and is correct to (§9.5: the trailer at the current end of file
is its snapshot). Step 6 is about surviving power loss, not about visibility.
Step 4's barrier is the one that carries the safety property: it guarantees
that if the trailer is durable, everything it reaches is.

Verified: claimed bytes in generation 2 = 1142; **slack = 586**; 1142 + 586 =
1728. The itemisation matches to the byte (see §5 below).

---

## 4. Appending to a file whose records I do not all understand

This is where I stopped twice.

### 4.1 The case that works

Suppose the file additionally carries a **layer sub-record on `mask`** of an
experimental type 0x8002 with MU = 1, PE = 1, which my updater does not
implement. `[R-CNT-18]`: *"an unknown sub-record type with MU = 1 is
reject-layer — never reject-file"*. So `mask` is unusable to a reader, the
rest of the file is fine, and §20.4's MU = 1 row says the record *"blocks
modification of that layer, leaving other layers editable"*.

I can therefore still do commit 2's `elev` work. I re-emit `mask`'s whole
layer record byte-identically — header, inline payload (including the
sub-record I cannot parse), extent slot — which I can do from the top-level
record walk alone, without ever parsing the sub-record sequence. `[R-WRT-05]`
requires exactly that, and `[R-WRT-08]` bars me from re-encoding it. `mask`'s
index and tiles are untouched, so its extent slot stays valid across the
growth of F. Clean, and I never had to understand anything.

An MU = 0 / PE = 1 unknown record, top-level or sub-record, is the same story
with a weaker gate: retain byte-identical, extent content unmodified, extent
stays where it is, covered by no checksum (§8.1) and therefore carried
forward unread — which §22.3 names as one of its three stated residues.

### 4.2 The case that does not — finding writer-01

Now suppose the unknown MU = 1 record is **top-level** instead. §20.4 tells
me what to do:

> at file scope it blocks any modification of file-scope structure — adding,
> removing, or reordering top-level records — while a commit that only changes
> a layer's own tiles, index, or record remains permitted.

So: carry it forward, do not touch the top-level record set, and go ahead
with `elev`'s tile. I wrote the commit out. Then I went back to §7.2 to check
the framing of the record I was copying and read:

> An unknown record type at file scope: MU = 1 → reject-file; MU = 0 →
> ignore-record.

and §2.3:

> Verifiers and updaters are readers of the files they process and inherit
> every reader obligation.

and §2.4's definition of the outcome I have just inherited:

> **reject-file** | The file is not usable; failure is reported for the whole
> file. A reader MUST NOT rely on any structure in it.

I cannot both "not rely on any structure in it" and re-emit its directory.
These do not compose. §20.4's file-scope clause describes a commit that
`[R-CNT-15]` forbids me to begin. Details and the two readings are in the
findings section; I picked "refuse", and the file stays at generation 1.

What convinced me the tension is real rather than my misreading is
`[R-WRT-06]`: *"A compactor MUST refuse to compact a file carrying any record
whose type it does not implement with MU = 1."* If `[R-CNT-15]`'s reject-file
already stopped every reader — and a compactor is a reader of everything it
copies (`[R-WRT-09]`) — that sentence would have nothing to do. Its existence
says the authors expected updaters to be able to *hold* such a file, and to
be stopped only at relocation. §20.4's file-scope clause is written on the
same expectation.

### 4.3 The other thing I stopped on — finding writer-02

Suppose the file carries a top-level ancillary with **MU = 0, PE = 0**, and my
commit is exactly commit 2 (supersede a tile in `elev`, add layer `grad`).
May I drop the ancillary? §20.4:

> An appender may drop it only in a commit that *independently* changes the
> scope the record attaches to: … for a top-level record, the file's layer set
> or another top-level record.

A layer record **is** a top-level record — §7.3 scopes type 0x0001 to "file",
and §21.2's rows are careful to say "a *non-layer* top-level record" whenever
they mean to exclude them (F28, F29, F31, F33, F34, F35). So "another
top-level record" reads either as *any other top-level record, layer records
included* — in which case superseding one tile of `elev`, which changes
`elev`'s record, licenses the drop — or as *another non-layer top-level
record*, layer records being separately covered by "the file's layer set".
The two readings give different directories, and I could not settle it from
this sentence. Details in the findings.

---

## 5. Slack, by commit shape

Who counts it: a **verifier**, never a reader. §5.2: *"A reader MUST NOT
interpret it (§9.5); a verifier MUST report the total number of slack bytes,
since that number is what tells an operator to compact."* §9.7 says how: walk
the live state, and *"Bytes the walk does not reach are slack."* What it may
contain: anything. *"Slack has no internal structure this specification
defines, its content is unconstrained, and no conformance requirement applies
to it."* Writers SHOULD zero it (`[R-CNT-03]`) and forfeit byte
reproducibility if they do not.

**Creation.** Slack is only the gaps the writer chose plus the pre-trailer
pad. My file: 60 + 56 (both A_slab-forced) + 1 (pad) = **117**. A creator
that declares neither alignment nor a slab and packs can get this down to the
pad alone, 0–63 bytes.

**Append (commit 2).** New slack is exactly: the superseded tile (32), the
superseded index region (84), the previous directory (275), the previous pad
(1), the previous trailer (64), and the new pad (14) = 470, on top of the 117
carried forward = **586**. Independently confirmed against F₂ − claimed =
1728 − 1142 = 586. Every one of those categories is named in the document:
§20.3 (*"Extents this commit supersedes become slack"*), §5.1's three-commit
figure (*"the directories, pads and trailers of commits 1 and 2"*), §20.5's
example (*"Slack accumulates a directory, a pad and a trailer per commit, plus
a whole index region for each layer a commit touched"*).

**In-place update.** There is no such shape. `[R-LIF-01]` admits only a commit
or a whole-file rewrite; a "change confined to the directory" (§20.3 example
(c) — renaming a layer, changing a fill, clearing a slab) is still an append,
and its slack is the old directory + pad + trailer. Editing user metadata is
*not* that shape: the document is explicit that the document lives in an
extent, so a new extent is appended and the old one becomes slack.

**Rewrite / compaction.** Slack in the output is only the pre-trailer pad plus
whatever gaps the compactor's own placement leaves; the input's slack is not
carried (`[R-WRT-06]`: *"containing only the structures reachable from the
input's live trailer … so slack is never carried"*). The input file is not
modified and persists (`[R-PRV-02]`).

**Abandoned partial write.** The bytes past F are *not* slack of a conforming
file, because there is no conforming file: §5.1 fixes the file size of a
conforming file at F, so a physical file longer than its live trailer's
committed_file_length fails `[R-CNT-06]` (register F19) and, if the residue
does not begin with the magic at physical-end − 64, F10 as well. §9.5's note
says this in as many words: the reader *"cannot tell residue from corruption
and is not asked to"*, and what the residue violates is `[R-LIF-04]`'s writer
obligation to truncate or overwrite. So: an abandoned partial write produces a
**nonconforming file**, not a conforming file with extra slack, and the next
writer must truncate to F or overwrite from it (`[R-LIF-04]`).

One consequence I want on the record because it surprised me: `[R-CNT-21]`
lets a verifier report a **partial** slack total when its walk did not
complete, and requires it to *"name the regions it did not walk and report
their byte extent"*. So the number an operator uses to decide about compaction
is only trustworthy from a walk that completed — §22.3 makes the same point.
A verifier that stops at the first violation under `[R-CNF-11]` produces a
figure that is not comparable with a full one.

---

## 6. Torn-write recovery — five crash points in commit 2

Commit 2's geometry, for reference: F₁ = 1152; payload at [1152,1184);
index′ at [1184,1268); directory at [1268,1650); pad [1650,1664); trailer
[1664,1728); F₂ = 1728.

Throughout: `[R-LIF-05]` fixes the default read path as
*trailer-at-end-or-fail*, and forbids a reader to scan backward. §9.6's probe
is the recovery tool's, and it starts *"at the largest 64-aligned offset o
with o + 64 ≤ the physical file length"*, stepping down, requiring magic +
CRC + committed_file_length = o + 64.

**(A) Crash mid-payload, physical length 1180.** Next reader: the last 64
bytes are [1116,1180), inside generation 1's directory and pad — no magic at
1116 → F10, reject-file, "torn". Next updater: §9.4 forbids it to append.
Recovery: probe from o = 1088 → magic, CRC verifies, committed_file_length =
1152 = 1088 + 64 → truncate to 1152, generation 1 restored **exactly**.
Conforming in the meantime: **no**.

**(B) Crash mid-directory, physical length 1368.** Probe starts at o = 1280
(inside the new directory), steps 1280 → 1216 → 1152 → 1088, four probes, and
lands on trailer₁. Same outcome.

**(C) Crash after the directory is complete and step 4's barrier has been
taken, before any of the trailer, physical length 1650.** This is the
interesting one: everything the new trailer would point at is on stable
storage, and the file is still unreadable, because nothing commits it. Probe
starts at 1536 and walks down eight steps to 1088. Truncate to 1152. The
generation-2 work is lost, which is correct — no trailer, no generation.
§9.2's figure calls this the window in which the old state is *recoverable*
rather than *readable*, and that is the right description.

**(D) Crash mid-trailer, physical length 1708.** Magic is present at 1664 but
the file's last 64 bytes are [1644,1708) — a slice of pad and half a trailer.
Reader: no magic at 1644 → F10. Probe from 1600 down to 1088, nine steps.
Note that the probe *passes over* the real, complete-looking magic at 1664
only because 1664 + 64 = 1728 > 1708, so 1664 is never a candidate — the
"o + 64 ≤ physical length" clause is doing real work here. Truncate to 1152.
A variant where the whole 64 bytes land but the CRC bytes are stale gives
F16 instead of F10 and the same recovery.

**(E) Crash after step 6 but before truncation, on the `[R-LIF-04]` overwrite
path.** This is the only shape in which the *new* generation is the recovery
target. Precondition: the writer was resuming from re-verified recovery output
whose physical length exceeded F, chose to overwrite from F rather than
truncate first, and crashed after the new trailer was durable but before it
truncated to committed_file_length. Physical length > F₂; the last 64 bytes
are stale residue → reader rejects (F10/F19). Probe steps down to 1664, finds
trailer₂, CRC verifies, committed_file_length = 1728 = 1664 + 64 → truncate to
1728. Generation 2 survives. This is the case that makes `[R-LIF-04]`'s
"no later than step 6" wording matter, and it is the only way I could
construct a state in which a writer legitimately holds a physical file longer
than a validated F: an ordinary abandoned write leaves no valid trailer at the
end at all, so §9.4 sends the writer to recovery rather than to the
truncate-or-overwrite branch.

In every case the answer to "is the file conforming in the meantime" is **no**,
and the document says so directly rather than by inference: §9.6's note,
*"a file whose final 64 bytes are not a valid trailer fails `[R-CNT-06]`'s
gates on the bytes handed over (§21.2 rows F10 and F19), and the earlier state
the probe finds is a different artifact"*. I could not find a crash point that
produces a conforming file in an unintended state.

The one residual risk the document names and does not remove: a tile payload
can mimic a trailer, so a probe can land on a false candidate. `[R-LIF-06]`
requires whole-file re-verification of recovery output and requires the tool
to *"report the candidate it settled on and how many it rejected"*. For my
file the mimic risk is nil (all payloads are uint16 grids and float32 planes),
but a writer storing arbitrary uint8 data has no way to prevent it and is not
asked to.

---

## 7. Compaction — one place I had to re-read

`[R-WRT-07]` says a compactor *"is free to place structures anywhere §5.2
admits"*. §5.2 admits any disjoint partition. My `mask` layer carries S = 4
and A_slab = 64, and the compactor re-emits that declaration verbatim
(content is preserved). Read alone, §20.5 licenses the compactor to scatter
`mask`'s planes and produce a file that fails `[R-SLB-03]` at L42/L43.

It is decided, but one section earlier: `[R-WRT-01]` says *"An appender and a
compactor satisfy every writer requirement for the bytes they produce"*, and
`[R-SLB-01]`/`[R-SLB-03]` are writer requirements. So the compactor must
re-establish the runs. I record it here rather than as a finding because the
resolution is unambiguous once found; §20.5's sentence is loose, not wrong.
Note also that `[R-SLB-04]` does not reach the compactor at all — it binds "a
commit", and compaction is a whole-file rewrite, not a commit (`[R-LIF-01]`).

The rest of §20.5 is fully determined for a writer: fresh file_id (a new draw,
not merely a different value), generation 1, ignore-lane bits copied forward,
version_minor = max(floor, input's), entry lengths and crcs and sentinels
unchanged, entry offsets new, segment CRCs recomputed, crc_of_crc_array
updated, every relocated extent's checksum verified before emission
(`[R-WRT-09]`).

---

## 8. Byte-divergence catalogue

Two conforming writers, identical input arrays, identical stated options.
Every way their bytes may legitimately differ, and whether Appendix G closes
it.

| # | Divergence | Status | Closed by |
|---|---|---|---|
| 1 | Tile extents | legitimate — §11.3 imposes none | not a profile matter (input) |
| 2 | Channel layout, interleaved vs planar | legitimate (§14.4's note: single-channel numeric tiles are byte-identical either way, but the layout byte differs) | input |
| 3 | Codec choice | legitimate (`[R-COD-03]`) | G item 1 |
| 4 | Filter choice | legitimate (`[R-COD-09]`) | G item 1 (by pinning the producer) |
| 5 | Encoder output for codecs 2–4 at the same input | legitimate — `[R-CNF-05]`; G item 1 is explicit that byte-identity across *implementations* is unattainable here | G item 1, only by naming implementation + version + settings |
| 6 | DEFLATE's up to seven unused final-byte bits | legitimate; §17.2's note says *"This specification constrains them nowhere"* | G item 1 |
| 7 | zstd Frame_Content_Size present or absent (`[R-COD-06]`: *"MAY be present"*) | legitimate | G item 1 if "encoder settings" is read to include the content-size flag; the profile does not say so |
| 8 | zstd declared window, any value ≤ decoded size | legitimate | G item 1 |
| 9 | Whether an all-fill tile is stored or sentinelled | legitimate | **G item 6** (closed) |
| 10 | Which tiles are stored at all (a writer may store nothing) | legitimate | partly item 6; otherwise input |
| 11 | Placement and order of structures within a commit | legitimate (`[R-SLB-05]`) | **G item 3** (order only — see writer-05) |
| 12 | Size of alignment/slab gaps, and gaps generally | legitimate (§16.1, §16.2, §5.2) | **not closed** — see writer-05 |
| 13 | Slack content (zeroed or not) | legitimate — `[R-CNT-03]` is SHOULD | G's closing paragraph (requires zeroing) |
| 14 | `file_id` | legitimate (`[R-LIF-03]` is SHOULD-random) | **G item 2** (closed, deterministically) |
| 15 | `version_minor` | legitimate (`[R-CNT-26]` is SHOULD) | **G item 7** (closed) |
| 16 | Declared alignment / slab values | legitimate | **G item 5** (closed) |
| 17 | Record order in the directory | legitimate (`[R-CNT-14]`) | **G item 3** (type, then layer name) |
| 18 | Sub-record order inside a layer record | legitimate (same rule) | **not closed** — item 3 orders top-level records only |
| 19 | Number of commits used to reach the same content | legitimate | **G item 4** (closed) |
| 20 | JSON serialisation of the metadata document (spacing, number formatting, escapes) | legitimate — `[R-MTA-05]` sorts members but explicitly *"does not make two writers' output identical"* | **G item 8** (closed by pinning the JSON writer) |
| 21 | Fill value when the caller states none | legitimate — `[R-TYP-10]` is SHOULD-zero | **not closed** — and unlike the rest, this one changes the *reference array*, not just the bytes |
| 22 | Pre-trailer pad length | **not free**: `[R-LIF-02]` step 5 fixes it at pad-to-next-64 — though §6.2 says a longer gap is conforming (writer-04) | fixed |
| 23 | Segment CRC of a full all-sentinel segment, computed vs. the `[R-IDX-05]` constant | **not a divergence** — the constant *is* the computed value; I verified 0xEECB3BB2 | n/a |
| 24 | Relocating an untouched layer's live index region during an append | **forbidden** — §5.1 *"A commit never relocates a live index region otherwise"*, §20.3 *"not an appender's"*. The output would still be a conforming file, so nothing downstream catches it | fixed by prohibition |
| 25 | Whether the first structure starts at offset 16 | **cannot classify** — writer-03 |
| 26 | Whether a PE = 0 top-level ancillary is dropped in a layer-local commit | **cannot classify** — writer-02 |
| 27 | Whether an updater may commit at all against a file carrying an unknown MU = 1 top-level record | **cannot classify** — writer-01 |

Items 25, 26 and 27 are the three I could not classify as either legitimate or
forbidden, and they are findings for that reason. Items 12, 18 and 21 are
legitimate divergences that Appendix G's material does not close although it
claims to close "the degrees of freedom this format deliberately leaves open";
that is finding writer-05.

Worth stating plainly for the record: divergences 5 and 20 mean that
cross-implementation byte-identity is *unattainable* for any file using a
compressing codec or carrying user metadata, and Appendix G says so honestly
in item 1 and item 8. A writer that needs content-addressing must use codec 1
and no metadata, or pin its producers.

---

## 9. Findings

### writer-01 — CONTRADICTION — §20.4 tells an updater to commit against a file §7.2 tells it to reject

**Location.** §20.4, `[R-WRT-08]`'s table, MU = 1 row (line 2869); against
§7.2 `[R-CNT-15]`, §2.3 `[R-CNF-11]`, §2.4's reject-file definition.

§20.4:

> at file scope it blocks any modification of file-scope structure — adding,
> removing, or reordering top-level records — while a commit that only changes
> a layer's own tiles, index, or record remains permitted.

§7.2 `[R-CNT-15]`:

> An unknown record type at file scope: MU = 1 → reject-file; MU = 0 →
> ignore-record.

§2.4:

> **reject-file** | The file is not usable; failure is reported for the whole
> file. A reader MUST NOT rely on any structure in it.

§2.3:

> Verifiers and updaters are readers of the files they process and inherit
> every reader obligation.

**Readings.** (i) The updater rejects the file and emits nothing: `[R-CNT-15]`
is unqualified, §2.3 makes it bind updaters, §2.4 forbids relying on any
structure, and an append relies on the trailer, the directory, and the
records it re-emits. §21.6 confirms the reader side in its own words —
*"`[R-CNT-15]` obliges the reader to reject"* — and `[R-CNF-03]`'s acceptance
duty is explicitly written to exclude such files. (ii) §20.4 carves the
updater out: an updater may hold the file, must carry the record forward
byte-identically, and may commit layer-local changes. `[R-WRT-06]`'s separate,
narrower refusal for compactors — *"such a type can define references this
specification does not (§7.2), so its bytes cannot be safely relocated"* —
reads as written on reading (ii), because on reading (i) it would be
redundant.

**I picked (i)** and refused the commit, because `[R-CNT-15]` and §2.3 are
categorical and §20.4 nowhere claims an exemption from them. But the cost of
(i) is that the entire file-scope half of §20.4's MU = 1 row becomes
unreachable text, and `[R-WRT-06]`'s existence becomes hard to explain.

**What an implementer does wrong without this.** An updater built from §20
appends to files an updater built from Part I refuses to open. In a pipeline
where one tool writes and another audits, the audit tool declares a file
unusable that the writer has been extending for months.

**Byte-level: yes.** Two updaters, the same generation-1 file carrying a
top-level experimental-type record with MU = 1, the same instruction
"supersede tile 1 of layer `elev`". Updater A (reading ii) emits bytes
[1152, 1728): a new payload, a full re-emitted index region, a four-record
directory, a pad and a generation-2 trailer. Updater B (reading i) emits
nothing and leaves the file at 1152 bytes and generation 1. Both resulting
files are conforming files, so no verifier verdict distinguishes them and
nothing downstream corrects the fork; the divergence is entirely in what a
conforming updater may write.

---

### writer-02 — AMBIGUITY — "another top-level record" may or may not mean a layer record, deciding whether a PE = 0 ancillary survives

**Location.** §20.4, `[R-WRT-08]`'s table, MU = 0 / PE = 0 row (line 2871).

> An appender may drop it only in a commit that *independently* changes the
> scope the record attaches to: for a layer sub-record, that layer's record,
> index, or stored tiles; for a top-level record, the file's layer set or
> another top-level record.

**Readings.** (i) *Any* other top-level record, layer records included. §7.3
scopes type 0x0001 to "file", and §21.2 is careful to write "a *non-layer*
top-level record" (F28, F29, F31, F33–F35) whenever it means to exclude them —
so "top-level record" unqualified includes layer records. Under (i), every
commit that re-points a layer's extent slot (i.e. every commit that touches
any layer's index) licenses dropping any PE = 0 ancillary, and the
"the file's layer set" alternative is redundant, since changing the layer set
necessarily changes the set of top-level records. (ii) "Another top-level
record" means another *non-layer* one; layer changes are covered by "the
file's layer set", which then means adding or removing a layer, and a commit
that merely supersedes a tile does not license the drop.

**I picked (ii)**, on the strength of the same table's MU = 1 row, which
glosses "modification of file-scope structure" as *"adding, removing, or
reordering top-level records"* and explicitly contrasts it with *"a commit
that only changes a layer's own tiles, index, or record"*. That gloss treats a
change to a layer's own record as **not** a file-scope change, and reading (ii)
is the only one consistent with it. But the resolution is an inference across
rows about a different obligation, not a statement about this one, and the
literal text of this row supports (i).

**What an implementer does wrong without this.** Application state disappears.
Under (i) a routine tile update silently drops an ancillary record an
application was relying on; §20.4 asks the updater to SHOULD-report the loss,
but the record is gone either way, and its extent becomes slack that only
compaction reclaims.

**Byte-level: yes.** Two updaters, the same generation-1 file carrying a
top-level MU = 0 / PE = 0 ancillary, the same instruction "supersede tile 1 of
`elev`". Updater A (reading i) emits a directory with three records and the
ancillary's extent demoted to slack; updater B (reading ii) emits a directory
with four records, 24 + inline bytes longer, a different dir_length, a
different pad, and a different F in the trailer. Both files are conforming, so
nothing downstream resolves the fork.

---

### writer-03 — AMBIGUITY — §9.2's creation path may or may not require the first structure at exactly offset 16

**Location.** §9.2, `[R-LIF-02]`'s creation paragraph (line 1084–1087),
against step (1) of the same requirement and §5.2/§16.1.

> On creation there is no prior trailer: the writer first emits the front
> signature block (§6.1) — whose durability the barriers of steps 4 and 6
> cover — then performs steps 2–6 beginning at offset 16, with generation 1.

The general protocol's step (1) is *"begin writing at exactly F"*, and the
creation sentence names steps **2–6**, omitting step 1 and substituting
"beginning at offset 16" for it.

**Readings.** (i) "Beginning at offset 16" is the creation analogue of
"begin writing at exactly F", so the creator's first emitted byte after the
front block is at exactly 16 and no gap may precede the first structure.
(ii) It states only where the region available to the commit starts;
placement inside step 2 is free (`[R-SLB-05]`: *"its stored tiles MAY occupy
any non-overlapping byte positions, in any order"*), and a gap before the
first structure is ordinary slack — §5.2 lists *"alignment and slab gaps"*
among slack, and §16.1 says *"The bytes alignment leaves between structures
are slack"*.

**I picked (i)** — the sentence is doing step 1's job — and placed `elev`'s
tile 0 at exactly 16. But nothing in the file witnesses the difference: there
is no register row for a gap after the front block, a verifier's walk
(`[R-LIF-08]`) simply counts those bytes as slack, and §5.2 says *"no
conformance requirement applies to it"*. So both files are conforming and the
question is purely about which one a conforming creator may produce.

**What an implementer does wrong without this.** Under (i), a streaming
creator whose only layer declares alignment A = 4096 cannot simply start
writing tiles at the first aligned offset: it must place something at 16, which
in practice means reserving the tile-index region there and backfilling it
after the tiles are written — a design constraint the document never mentions
and that a writer discovers only after choosing an architecture. Under (ii) it
just leaves `[16, 4096)` as slack. I checked and reading (i) is always
satisfiable — an index region, a record extent, or the directory itself can
always take offset 16 — but only at that cost.

**Byte-level: yes.** Two creators, the same input, one layer declaring
A = 4096, streaming tile acquisition. Creator A (reading ii) emits its first
tile at 4096 with `[16, 4096)` slack and its index after the tiles. Creator B
(reading i) reserves `[16, 16+len)` for the index, emits the first tile at
4096, and backfills. The two files differ across their whole prefix and both
are conforming; nothing in the format distinguishes them, so the fork is in
what a conforming creator may emit and is never corrected downstream.

---

### writer-04 — CONTRADICTION — an over-long pre-trailer pad is a detectable violation of a named MUST that the register is normatively required to carry and does not

**Location.** §6.2 `[R-CNT-05]` (line 706) against §9.2 `[R-LIF-02]` step 5,
§2.4 `[R-CNF-07]`, and §21.1's completeness clause (line 2974).

§6.2:

> bounds their number only through step 5 of the commit protocol, which pads
> to the next 64-byte boundary (`[R-LIF-02]`) — a longer gap is conforming,
> and no conforming commit produces one.

§9.2 `[R-LIF-02]`:

> A writer performing a commit MUST, in order: … (5) append the pad to the
> next 64-byte boundary

§2.4 `[R-CNF-07]`:

> Every detectable violation named by this specification is assigned exactly
> one **reader outcome**: reject-file, reject-layer, reject-tile, or
> ignore-record.

§21.1:

> Its **completeness is normative** — a *detectable* violation this
> specification names and the register omits is a defect in this document

Producing a longer pad violates a MUST. It is detectable from a single file
with no history: the expected pad is (−dir_end) mod 64 and both dir_end and
F are in the trailer, so a verifier computes it in constant time — my own
file's pad is 1 byte and a 65-byte pad would be visible immediately. Yet it
has no register row, no reader outcome, and it is not among §21.7's account
of what escapes detection: §21.7's second class is explicitly *"obligations …
omitted from the register because a single file exhibits no witness of their
violation"*, and it names `[R-LIF-01]`, `[R-LIF-03]`, `[R-GEO-06]`,
`[R-SER-01]` and `[R-CNT-13]`'s no-embedded-offsets rule — not this.

**Reading I picked.** §6.2 governs the file's status directly and
unambiguously — the file is conforming — so `[R-CNF-07]`'s "every detectable
violation" must be read as "every detectable *file-conformance* violation",
and `[R-LIF-02]` step 5 joins the conduct class §2.3 `[R-CNF-02]` describes
(*"A writer obligation whose violation this specification expressly declares
not to be a file-conformance violation … binds the actor in the same way"*).
That reading works, but §2.3 enumerates the conduct class as §10.3, §18.3 and
§6.3's flags = 0, and this is a fourth member it does not name.

**What an implementer does wrong without this.** A verifier author reading
§21.1's completeness clause as normative builds a check for the pad and
reports nonconforming on a file §6.2 calls conforming. A conformance-corpus
author looks for the vector and finds no row to cite.

**Byte-level: no.** §6.2's *"a longer gap is conforming"* decides the
accept/reject verdict outright, so no two conforming readers or verifiers can
differ about a file with an over-long pad, and `[R-LIF-02]` step 5 decides the
writer's obligation outright. What is left open is only whether §21.1's and
`[R-CNF-07]`'s completeness claims are true as written.

---

### writer-05 — AMBIGUITY — Appendix G's total emission order fixes order but not gaps, and leaves sub-record order and the fill default open

**Location.** Appendix G items 3 and 5, and the profile's closing paragraph
(lines 3758–3785).

> 3. **A total emission order.** For each layer in ascending layer-name byte
> order: its stored tiles in disk-ordinal order, then its tile-index region;
> then any record extents in ascending record order; then the directory.
> Records are ordered by type, and within type 0x0001 by layer name — record
> order carries no meaning (`[R-CNT-14]`), so it is otherwise free to vary, as
> is structure placement (`[R-LIF-02]` step 2).

> Everything else the profile needs is already mandatory except gap content,
> which `[R-CNT-03]` only advises and this profile requires

**Readings.** (i) "Emission order" implies sequential emission with no
deliberate gaps, so offsets are determined once the order is: each structure
begins where the previous one ended, subject only to the declared alignment
item 5 pins. (ii) It fixes only the *sequence*, leaving each writer free to
insert padding between structures — which §16 expressly permits (*"A writer
that scatters structures wastes space rather than violating a rule"*) and which
the closing paragraph does not list among the things the profile adds.

**I picked (i)**, because a profile whose stated purpose is byte-identity is
useless under (ii). But (ii) is the literal reading, and the closing paragraph
is written as an exhaustive account of the gap between "already mandatory" and
"what the profile adds" — naming only gap *content*, never gap *extent*.

Two further degrees of freedom the profile does not reach:

- **Sub-record order.** Item 3 orders top-level records by type and layer
  records by name. A layer record's sub-record sequence has no stated order,
  and `[R-CNT-14]` makes record order meaningless there too, so two
  profile-conforming writers emitting the same layer with a user-metadata
  sub-record and one application sub-record can order them differently.
- **The fill default.** `[R-TYP-10]` — *"a writer whose caller does not
  choose a fill SHOULD record all-zero bytes. A writer that defaults
  differently still emits a conforming file"* — is a SHOULD the profile never
  promotes, and the closing paragraph cites `[R-TYP-06]` (fill is *recorded*)
  rather than `[R-TYP-10]` (what it is). Unlike every other item here, this
  one changes the reference array and not merely the bytes: two
  profile-conforming writers given the same input and no stated fill produce
  files whose unstored tiles read back differently.

**What an implementer does wrong without this.** A content-addressing pipeline
adopts the profile, gets stable hashes from one writer, and finds them
unstable across writers or across a refactor that changes alignment padding —
after having been told the profile *"closes the degrees of freedom this format
deliberately leaves open"*.

**Byte-level: no.** Appendix G is labelled non-normative and says of itself
*"It adds no requirement to any actor: a writer ignoring it is fully
conforming"*. Every file produced under either reading is conforming and every
reader accepts all of them, so no conforming implementation's emit-set or
accept/reject verdict changes. What changes is whether the profile delivers
what it claims.

---

## 10. What I could not determine, summarised

Everything in the creation path is determined except the offset of the first
structure (writer-03). Everything in the append path is determined except two
questions about updating in the presence of records I do not implement
(writer-01, writer-02). Slack accounting, torn-write recovery at every crash
point I could construct, and compaction are fully determined — in the last
case only after cross-reading `[R-WRT-01]` against §20.5's looser prose. The
byte-divergence catalogue is complete and every entry is classified except the
three findings above; the reproducible-writer profile closes most of it and
leaves gap extent, sub-record order and the fill default open (writer-05).

I built a 1152-byte two-layer file, a 1728-byte generation-2 append, and five
crash images, and verified each against the document's own arithmetic. The
document sufficed for all of it.
