# Cleanroom round 13 — Reader implementer transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,128 lines), in five `Read` calls covering lines 1–4128 with no gaps. I ran
`wc -l` against that file, one `grep` against that file, and three Python
programs of my own authorship that read no project file: a CRC-32C
implementation used to check the document's stated checksums and constants, a
register-table parser that reads `spec/tarn.md` and counts rows and instance
cells, and a file builder that emits a synthetic TARN file into my scratchpad.

I did not open `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`README.md`, `CONTRIBUTING.md`, `conformance/`, `spec/registry.json`, any ADR,
any prior round's findings, or the output directory. I ran no `git` command, no
web search, no web fetch. I did not list any directory. I did see the harness's
task list (four task titles) in a system reminder; I did not act on it, and
nothing in it told me what any edit was meant to accomplish. Two of those
titles named sections, which I would have read closely anyway because the brief
listed them as changed.

Scratch files I wrote and read: `scratchpad/crc.py`, `scratchpad/build.py`,
`scratchpad/mine.tarn`.

---

## 1. What I set out to build

A conforming reader, written in the order I would actually write the code:

1. `open(transport) -> FileHandle` — trailer, directory, record walk, layer table.
2. `layer(handle, name) -> LayerHandle` — full layer-record validation.
3. `read(layer, request) -> samples` — index chain, entry classification, payload,
   codec, filter inverse, extraction.
4. Everything the degradation walks demand at each of those.

I kept a running list of every point where I had to stop and decide something
the text did not decide for me. That list is §9 below; it is short, and two
entries survived as findings.

---

## 2. The open path, byte by byte

### 2.1 What the reader must have before it fetches anything

Nothing. §19.1 step 1 obtains F from the transport (`[R-CNT-10]`), and for a
remote reader the suffix range of step 2 carries F in its own response, so steps
1 and 2 cost one request between them (§6.4). This is the only place the reader
uses a number it did not get from the file, and `[R-CNT-10]` is emphatic that it
must be transport-authoritative and must never be substituted from
`committed_file_length`. My reader therefore has two constructors — one that
takes a size, one that probes — and refuses to open if neither is available.

### 2.2 Request 1: the suffix

Range: `[F-64, F)`. Bounded before reading by the constant 64. This is the whole
point of tail anchoring: the first range needs no prior knowledge.

Validation order is fixed and I implemented it literally (§6.2, `[R-CNT-06]`):

```
1. trailer magic == 8A 4E 52 41 54 0D 0A 1A          (F8; F1's trailer instance)
2. CRC32C(trailer[0:60]) == u32le(trailer[60:64])    (F14)
3. version gate: version_major != 0, and implemented (F18; §6.3 R-CNT-07)
   -- steps 1..3 touch only fields R-CNT-24 pins across all majors
4. flag gates: no set bit in 0..15 (F19); ignore 16..31   (R-CNT-08)
5. committed_file_length == F and F mod 64 == 0      (F17, F13)
6. dir_offset >= 16                                   (F9)
7. dir_length >= 4                                    (F16)
8. dir_offset + dir_length <= F - 64                  (F10)
9. 1 <= generation <= 2^63-1                          (F11)
10. file_id != 0                                      (F12)
11. trailer[56:60] all zero                           (F15)
```

Plus `[R-ENC-03]`/`[R-ENC-04]` on the u64s (F2, F3) and `[R-CNT-27]`'s
128-byte floor (F5), which in practice I test first, because step 2's
`[F-64, F)` is not computable at F < 64. §19.1 does not say to test the floor
before computing `F-64`; the register does say F5 is reader-detected at open, and
§19's preamble makes the register the complete inventory of what is due at a
tier, so the ordering is mine to choose and no outcome turns on it. Not a
finding.

Note the residency rule, which I found unusually well engineered: §6.1's front
block obligation turns on *residency*, not on transport class, so my remote
reader that speculates a suffix window has one branch — `if window_start == 0:
check_front_block()` — and no need to classify its own network (`[R-CNT-04]`,
F6, F1's front instance).

### 2.3 Request 2: the directory

Range: `[dir_offset, dir_offset + dir_length)`. Bounded before reading by
`dir_offset >= 16` and `dir_offset + dir_length <= F - 64` from the CRC-verified
trailer. This is the chain `[R-ENC-05]` demands and `[R-SEC-02]`'s note
describes: I never issue I/O sized by an integer whose covering checksum has not
verified. The trailer's CRC covers `dir_offset`/`dir_length`; the directory's own
CRC covers everything the record walk then reads.

`CRC32C(region[0 : dir_length-4]) == u32le(region[dir_length-4 : dir_length])`
(F20, `[R-CNT-11]`), verified *before any other use of the region*. My parser is
structured so the CRC check is the constructor of the record-sequence iterator;
it is not possible to call `next()` without having verified.

### 2.4 Byte-exact cold remote open, Appendix A

Appendix A's 128-byte file:

- Request 1: suffix, `[64, 128)`, 64 bytes.
- Request 2: `[16, 20)`, 4 bytes.
- **Total: 2 requests, 68 bytes.**

The front block is *not* fetched and *not* checked; Appendix A's closing
paragraph and `[R-CNT-04]` both say so, and §6.4's accounting excludes it. A
reader that speculates a 112-byte suffix `[16, 128)` gets one request, 112
bytes, and still no front-block check (bytes `[0,16)` non-resident). A reader
that speculates the whole 128 bytes gets one request, 128 bytes, and *must*
check the front block. All three are conforming; §6.4's Note says so explicitly
and I confirm the text leaves no ambiguity about which obligations attach to
which of the three.

I recomputed Appendix A's trailer CRC over `[64, 124)`:

```
computed 0xE00938D2   stored 0xE00938D2   -- matches
```

and the check vectors of §4.5: `CRC32C("123456789") = 0xE3069283`,
`CRC32C(<empty>) = 0x00000000`. Both match. Appendix A's directory at `[16,20)`
holding `00 00 00 00` is the CRC of a zero-byte record sequence, consistent.

### 2.5 Request 3 does not exist

§19.1's closing sentence (`[R-RDR-01]`) is the invariant I coded against: the
open consumes trailer and directory only, at any layer count and file size. My
`open()` returns a layer table of names and record slices; it fetches no extent,
no index, no payload. §19.2's tier list agrees, and §21.5's R2–R10 all sit at
*extent use*, which the open never reaches.

### 2.6 The record walk

Header is fixed 24 bytes (§7.2). Inline payload is `inline_length` bytes. At each
step I check:

- `type != 0` (F24, `[R-CNT-12]`).
- header + inline fit inside the sequence, and no residue at the end (F29).
- reserved flag bits 2–15: **ignore** (readers), verifier rejects (F26).
- MU=1 with PE=0: treat as PE=1; verifier rejects (F25).
- unknown top-level type: MU=1 → reject-file; MU=0 → ignore-record (`[R-CNT-15]`,
  F35 for the reserved-range MU=1 case).
- multiplicity: at most one top-level user-metadata record (F34).
- extent slot validity for non-layer top-level records (F30, F31, F32).
- the extra framing a user-metadata record carries: slot not (0,0) (F21),
  `extent_length >= 5` (F22), `inline_length == 1` (F23).
- for each layer record, parse the name field and build the namespace; duplicates
  are reject-file (F4), decided over raw bytes before any well-formedness test.

One decision I had to reason about rather than read off: **does an ignored
record's extent slot still have to be valid?** §2.4 says ignore-record means "the
record is skipped as though absent", which reads like a licence to skip its slot.
Three passages settle it the other way and I followed them: §19.1 step 4
enumerates "the extent-slot validity rules for non-layer top-level records
(`[R-CNT-13]`)" as part of the record walk with no exemption for ignored
records; `[R-CNT-13]` itself scopes the error to "the scope the record governs"
with no exemption; and §5.2 defines a structure as "a record extent (the bytes
any record's extent slot references, **whatever the record's type**)", which puts
an ignored record's extent inside the live committed state and therefore inside
the partition `[R-CNT-02]` certifies. Decidable; not a finding.

### 2.7 Cold open of a file I built myself

To check that the container really closes, I emitted a file from the spec alone
(scratchpad/build.py): one interleaved rank-1 layer `sst`, dimension `x` with
E=4, T=4, one float32 channel `temp` with fill 0x7FC00000, codec 1, filter 1,
one stored tile holding 1.0f 2.0f 3.0f 4.0f.

```
inline_length 81   dir_length 109   dir end 165   trailer at 192   F 256   pad 27

0000  89 54 41 52 4E 0D 0A 1A 00 00 00 00 00 00 00 00   front block
0010  00 00 80 3F 00 00 00 40 00 00 40 40 00 00 80 40   stored tile [16,32)
0020  10 00 00 00 00 00 00 00 10 00 00 00 00 00 00 00   entry: off 16, len 16
0030  0A 69 BA 9E E3 A1 F9 12 01 00 03 00 51 00 00 00   entry crc | rec hdr
0040  20 00 00 00 00 00 00 00 18 00 00 00 00 00 00 00   extent (32, 24)
0050  03 73 73 74 01 01 00 01 00 01 00 00 00 00 00 00   name sst, layout/lin/codec/filter
...
00C0  8A 4E 52 41 54 0D 0A 1A 01 00 00 00 00 00 00 00   trailer
00F0  EF CD AB 89 67 45 23 01 00 00 00 00 D4 0A 82 C5
```

Cold remote open: request 1 `[192,256)` = 64 bytes; request 2 `[56,165)` = 109
bytes; **2 requests, 173 bytes**. Coverage: 16 + 16 + 24 + 109 + 64 = 229
claimed, F = 256, slack = 27 (the pre-trailer pad, and only that — `[R-CNT-05]`
bounds it through step 5 of `[R-LIF-02]`, and 165 → 192 is exactly the pad to the
next 64-byte boundary). Every claimant lies in `[16, 192)`, disjoint. The file
partitions.

Then the tile read: CRC array at `[52,56)` (4 bytes), segment at `[32,52)`
(20 bytes) — coalescable into one range `[32,56)` — and payload `[16,32)`
(16 bytes). Three ranges cold, two if the index region is fetched whole, which
§15.4's example calls the naive reader for a single-segment layer.

Nothing in this construction required a guess.

---

## 3. Validation timing by tier

I implemented §19.2 as four gates, and the mapping is unusually clean:

| Tier | What my reader checks | Register rows |
|---|---|---|
| open | front block *if resident*; trailer; directory CRC; record walk; layer-name namespace | F1–F6, F8–F24, F29–F32, F34, F35; L3, L5, L6; R1 (top-level) |
| layer access | the whole of §19.3's list, before any use of the layer's declarations other than its name | L1, L2, L4, L7–L17, L19–L36, L39, L43–L45; R1 (sub-record) |
| tile use | index chain, entry classification, payload CRC, decode | L37, L38; T1, T3, T6–T12, T14, T17–T25 |
| extent use | the extent's CRC and the document rules that attach at its encoding | R2–R10 |

I cross-checked §19.3's enumeration against every reader-detected row in §21.3
whose detection point is *layer access*. All 40 of them are reachable from
§19.3's list: the six value sets (§11.4, §12.2, §14.1, §15.1, §17.2, §17.3) cover
L31/L33/L34/L36/L43/L45; `[R-CNT-23]`'s constraint set covers L27–L30, L35, L39;
`[R-CNT-16]` covers L20; `[R-CNT-17]` covers L21/L22; `[R-CNT-18]`/`[R-CNT-12]`
cover L13/L14/L23/L24/L26; `[R-CNT-13]` covers L15–L17; the name rules cover
L4/L7/L8/L9; `[R-GEO-01]`–`[R-GEO-03]` and `[R-ENC-03]`/`[R-ENC-04]` cover
L1/L2/L32; `[R-COD-07]` covers L44; the user-metadata sub-record framing covers
L10–L12; `[R-CNT-14]` covers L19. Nothing is orphaned.

**What a reader is permitted never to check.** The verifier-only set, which I
compiled from the register's Detector column and confirmed against the prose:
F7 (structure in the pre-trailer gap), F25/F26 (record flag bits), F27
(unsorted metadata members), F28 (registered type's stored flags), F33
(cross-scope overlap), F36 (reserved-range type); L18 (intra-layer overlap),
L25, L40–L42 (alignment and slab invariants), L46/L47, L48, L49; T2, T4, T5
(decoded content — bool bytes, padding, pad bits), T26 (mis-strided filter).
§7.2 ("readers are not obligated to detect overlap"), §16.1 ("alignment is
reader-invisible"), §16.2, and §14.5 ("a conforming reader ... is not obligated
to check it") each say so at the site, and Appendix H's verifier checklist
enumerates the same set. That is three independent statements of the same
partition and they agree — this is the part of the document I would least expect
to be wrong, and it is not.

**What becomes a verdict when.** §2.3's three verdicts and §21.1's *certification*
detection point put every verifier row outside the reader tiers entirely. The
one thing I had to hold carefully: `[R-RDR-02]`'s prospectivity. A reject-layer
established at tile use (L37/L38, index-chain CRC failure) bars *further* service
but does not retroactively invalidate what §19.2's timing already let the reader
return (§2.4's reject-layer row, and §19.4 step 8's closing sentence). My reader
returns values as it produces them and marks the layer dead on the failure; it
does not buffer a whole region in order to un-return anything.

---

## 4. Layer access

§19.3 says layer access performs no fetch. I confirmed this holds: every item in
its list is decidable from the directory bytes and F. The `[R-CNT-17]`
cross-check is the interesting case — `extent_length == entry_count*20 +
ceil(entry_count/2^16)*4` and `entry_count == addressed-tile count` — and both
sides come from the record. `[R-SEC-02]`'s note is right that this is what keeps
`entry_count` from being a hostile amplifier: the declared region length is tied
to `entry_count`, and `[R-CNT-13]` ties that length to F.

I verified §7.4's worked example byte for byte, because it is newly authored text
and the brief says newly authored text has had the least review.

```
 0  03 73 73 74                name, 4 bytes
 4  01                         layout       ] 
 5  01 00                      linearization]
 7  01 00                      codec        ]
 9  01 00                      filter       ] nine scalars,
11  00 x8                      A            ] 1+2+2+2+8+8+8+1+2
19  00 x8                      S            ] = 34 bytes
27  00 x8                      A_slab       ]
35  01                         rank d       ]
36  01 00                      C            ]
38  01 78 | 64 00.. | 20 00..  dimension entry, 2+8+8 = 18
56  04 74 65 6D 70 0C 00 | 04 00 00 C0 7F   channel entry, 5+2+5 = 12
68  01 | 04 00.. | 2E 98 EE C4              trailing fixed, 1+8+4 = 13
                                            4+34+18+12+13 = 81  OK
```

Independent recomputation of its two checksums:

```
CRC32C(4 sentinel entries, 80 bytes)  = 0x80A34955   stored 55 49 A3 80   OK
CRC32C(55 49 A3 80)                   = 0xC4EE982E   stored 2E 98 EE C4   OK
```

Grid count `ceil(100/32) = 4`, so `entry_count = 4` (interleaved, N). Extent
length `4*20 + ceil(4/65536)*4 = 84`. The record's flags are MU=1, PE=1 = 0x0003
per §7.3. The channel entry is byte-identical to §12.3's `temp` example, as the
text claims. Every number in this example is correct.

I also recomputed §15.4's all-sentinel constant:

```
CRC32C(2^16 sentinel entries) = 0xEECB3BB2   -- matches Appendix B and §15.4
```

and §17.3's shuffle example (`00 00 80 3F 00 00 00 40 00 00 40 40`, s=4, n=3,
byte i of group j to offset i*3+j) → `00 00 00 00 00 00 80 00 40 3F 40 40`,
which is exactly what the document prints. §14.3's packed-bool example
(P=10, alternating, fill false → `55 01`; fill true → `55 FD`) is correct.
§14.5's (5,5)/(4,4) edge tile has 1 real and 15 padding positions and 32 bytes
at uint16, correct. §15.4's 1,000,000-entry example — 16 segments, 64-byte CRC
array, region 20,000,064 bytes, entry 999,999 at segment 15 offset 339,180,
segment 15 at `[19,660,800, 20,000,000)`, one full segment = 1.25 MiB — is
correct in every figure. §11.4's ordinals (s=10, in-tile 11,452, disk 74) and
§15.4's `[1,480, 1,500)` are correct. §14.2's three worked strides
(Q=3/size 18/bytes [15,18); planar b 12 bytes at 10–11; Q=5/size 30/bytes
[25,30)) are correct.

I could not find an arithmetic error anywhere in this document.

---

## 5. The tile-read algorithm

```
read(layer, request):
  # 1. Domain
  if point:   all i: 0 <= x_i < E_i        else fail-as-request (no file verdict)
  if region:  intersect with extents; empty intersection -> success, no samples

  # 2. Ordinals
  t_i = x_i div T_i ; u_i = x_i mod T_i
  in_tile = sum_i u_i * prod_{j>i} T_j          # row-major, permanently
  s       = sum_i t_i * prod_{j>i} G_j          # linearization 1
  disk    = s                     (interleaved)
          = c*N + s               (planar, per requested channel c)

  for each needed entry:
    # 3. Index chain
    seg = disk div 2^16
    fetch crc_array = region[20*entry_count : 20*entry_count + 4*ceil(entry_count/2^16))
    fetch segment   = region[20*seg*2^16 : 20*min((seg+1)*2^16, entry_count))
    verify crc_of_crc_array over crc_array         -> mismatch: reject-LAYER (L37)
    verify crc_array[seg]   over segment           -> mismatch: reject-LAYER (L38)
    # both ranges computable from the layer record alone; MAY be parallel; MAY be cached

    # 4. Entry
    e = segment[20*(disk - seg*2^16) : +20]
    classify per 15.3's eleven rows
      valid sentinel  -> every requested position of this tile reads FILL, no I/O
      structural rows -> reject-TILE, and fill is never the fallback
    if codec == 1 and e.length != decoded_size: reject-TILE (T14)   # before any fetch

    # 5. Payload
    fetch [e.offset, e.offset + e.length)
    verify CRC32C(bytes) == e.crc                  -> mismatch: reject-TILE (T1)

    # 6. Decode
    image = filter_inverse(codec_decode(bytes))
    assert len(image) == decoded_size              -> else reject-TILE (T3)

    # 7. Extract
    ...

  # 8. Return bit patterns unaltered
```

### 5.1 Decoded size and offsets — the whole of §14 in four lines

```
Q  = sum over channels of B_i                       # sample stride
F_c= sum over channels j<c of B_j                   # in-sample offset
interleaved:            size = P*Q     value(c,u) at u*Q + F_c
planar, numeric c:      size = P*B_c   value(u)   at u*B_c
planar, bool c:         size = ceil(P/8)           value(u) = bit u mod 8 of byte u div 8
```

Every one of these is fixed by declarations alone, never by payload content
(`[R-SER-07]`), which is the allocation discipline `[R-SEC-02]` rests on. My
decoder allocates `decoded_size` up front and hands the codec a fixed-capacity
output; nothing in the stream can enlarge it.

### 5.2 The filter, correctly ordered

Writer: image → filter → codec → stored. Reader: stored → codec → filter⁻¹ →
image. §17.1 and §19.4 step 6 agree, and §17.3 fixes the stride: element size
planar-numeric, Q interleaved, and s=1 (identity) for a packed bool plane. `L`
is divisible by `s` in all three cases, which I checked: `P*B / B`, `P*Q / Q`,
`ceil(P/8) / 1`. Length is unchanged by the filter, so `[R-SER-07]`'s exact-size
test is the same test before and after the inverse — no ambiguity about which
buffer it measures.

### 5.3 Sparse and fill

Fill is produced by exactly one condition (`[R-TYP-09]`): a valid sentinel read
from a verified chain. Not a malformed entry, not a failed segment CRC, not a
failed tile CRC. My reader has a single call site that emits fill and it is
inside the sentinel branch of step 4. `[R-CNF-09]` is the invariant I asserted
in the failure path: a rejected tile's positions must never be satisfied with
fill, even for a region read where the caller would not notice.

Interleaved sentinel → the whole fill sample, channels in declared order.
Planar sentinel → exactly that entry's channel; the same coordinate can mix
decoded and fill channels (§3.2, §13.3's r/g/b example).

### 5.4 Padding

Never returned (`[R-GEO-04]`). But a *stored* edge tile's padding bytes are
fill-encoded (`[R-SER-05]`), so a reader that forgets to clip observes a defined
value rather than garbage — the property §14.5's Rationale names, and it is real:
my extractor clips by comparing `t_i*T_i + u_i < E_i`, and I verified against
§14.5's example that the unclipped bytes are `CD AB` repeated.

---

## 6. Degradation walks

### 6.1 Unknown record type, top level, MU = 0, experimental range

Open, step 4. `[R-CNT-15]` → ignore-record. The file is **conforming** (§21.6's
row; §10.3's prohibition binds the writer's conduct, not the bytes,
`[R-CNF-02]`). I still validate its extent slot (F30–F32) and still count its
extent as a live-state structure. **What I still serve:** everything. All layers,
all tiles, all metadata. The record's extent is covered by no checksum (§8.1's
last row), so I never read it and never report on it.

### 6.2 Unknown record type, top level, MU = 1

`[R-CNT-15]` → reject-file, at open. **What I still serve:** nothing. §21.6's
closing paragraph tells me this file may be perfectly conforming and that my
refusal records my capability, not a defect — so my diagnostic string is
"unsupported critical record type 0xNNNN", distinct from both "not a TARN file"
and "corrupt". Same treatment §6.3 gives an unknown incompat-lane bit, which is
the parallel §20.4's table draws.

An unknown *sub*-record with MU = 1 is reject-**layer**, never reject-file
(`[R-CNT-18]`). That asymmetry is stated twice and I coded it as two separate
call sites.

### 6.3 Unknown codec value

A conforming reader cannot meet an unimplemented *assigned* codec — all four are
core (`[R-COD-03]`, `[R-CNF-03]`), and software that declines one is not a
conforming reader. So the only reachable case is a reserved (5–0x7FFF) or
experimental (≥0x8000) value, which is a validity error at **layer** scope at
layer access (L43). **What I still serve:** every other layer in the file, in
full; and I may still list the rejected layer's name (§2.4). §17.4 confirms this
is the only position from which a conforming reader ever cannot execute a codec.

### 6.4 Unrecognized flag / enum value

- Trailer ignore-lane bit set (16–31): **ignored**, file conforming, serve
  everything (§21.6's row, `[R-CNT-08]`).
- Trailer incompat-lane bit set (0–15): reject-file at open (F19). This text
  defines no flag bits, so every set incompat bit is unimplemented.
- Record reserved flag bits 2–15 set: **ignored** by me; the verifier records it
  (F26/L47). Serve everything.
- Layer `layout` = 3: reject-layer at layer access (L36). Other layers served.
- `version_minor` higher than this text defines: **accepted**, minors never gate
  (`[R-CNT-07]`, §21.6). This is the document's only descriptive field (§4.7)
  and it correctly determines nothing my reader does.

### 6.5 Truncated tail

Physical file 1000 bytes, last commit torn. F = 1000 (transport-authoritative).
I fetch `[936, 1000)`. Either the magic at 936 fails (F8), or — improbably — it
passes and the CRC fails (F14), or both pass and `committed_file_length != 1000`
(F17). All three are reject-file at open. `[R-LIF-05]` forbids scanning backward,
and §9.5's Note is explicit that I cannot tell residue from corruption and am
not asked to. **What I still serve:** nothing. Recovery (§9.6) is a deliberate,
separate operation belonging to a different tool, and its output must be
re-verified as a whole file before trust (`[R-LIF-06]`).

I traced the crash figure in §9.2 and it holds: mid-commit the physical tail is
not a trailer, `trail_n` is intact but no longer at the end, and truncating to it
restores the file exactly. The window is one in which the old state is
*recoverable*, not *readable*. My reader is on the wrong side of that line by
design.

### 6.6 Checksum mismatch — five scopes, five answers

| Failed | Outcome | What I still serve |
|---|---|---|
| trailer CRC | reject-file | nothing |
| directory CRC | reject-file | nothing |
| `crc_of_crc_array` or a segment CRC | reject-**layer** (L37/L38) | every other layer, in full; already-returned values of this layer stand |
| a stored tile's entry crc | reject-**tile** (T1) | every other tile of the same layer, including neighbours |
| a user-metadata extent's terminal CRC | **ignore-record** (R2), SHOULD report | everything; all structural data is unaffected |

The last row is the quarantine (`[R-CNT-25]`), and it is the one I most wanted to
get wrong: metadata sits inside the directory's trust chain, so it is tempting to
let its failure poison the file. §7.1, §18.1, and §21.5 all say the opposite, and
§18.1 draws the line precisely — the quarantine covers the *document*; a
malformed extent slot or a wrong `inline_length` **precedes** the document and
takes the containing scope (F21, F22, F23 → reject-file at top level).

### 6.7 Limit exceeded

`[R-ERR-04]`: refuse at the whole file, or at the narrowest scope whose
declarations exceed what I can serve — a layer or a tile — and **report it as a
resource limit, never as a validity error**. My error type is a separate class
from the validity errors for exactly this reason; §21.9's closing sentence says a
reader that reports "too large" as "corrupt" invites the deletion of intact data.
A file exceeding a guarantee stays conforming; only a reader that declines a file
*within* every guarantee is nonconforming.

The one narrow case: a user-metadata document has no declared size, so
`[R-ERR-04]` has no sub-file scope to measure and §18.2's Note routes me to the
whole file — or I take ignore-record for that record and proceed. Both are
explicitly licensed. I chose ignore-record, because it is the strictly more
useful behavior and the quarantine's whole purpose.

### 6.8 Format major version I do not implement

Reject-file at open, at the version gate, with a diagnostic distinct from both
"not a TARN file" and "corrupt" (`[R-CNT-07]`). §2.3 and §21.6 both stress that
the file may be conforming under that major and that my refusal is not a finding
about its bytes. If I were a verifier, this is *cannot establish*, not
*nonconforming* — and a verifier that has established any violation elsewhere
reports *nonconforming* regardless, since an established violation takes
priority (`[R-CNF-11]`).

---

## 7. The register, checked mechanically

I parsed §21.2–§21.5 out of the file and counted.

```
rows: 121      F 36 rows / 56 instances
               L 49 rows / 110 instances
               T 26 rows / 54 instances
               R 10 rows / 44 instances
total instances: 264
```

§21.2 declares 36, §21.3 declares 49, §21.4 declares 26, §21.5 declares 10 —
sum 121. §21.8 declares "121 conditions over 264 instances". Both figures are
exactly right under §21.1's counting rule (semicolon-separated items; a cell
reading `—` is one instance). That is a pleasant result: the derived count and
the cells agree.

I also extracted every `[R-XXX-NN]` in the document (161 distinct identifiers,
including `[R-ENC-100]` as §2.2's illustration and `[R-SER-04]` as the withdrawn
one) and checked each register row's Governing-rule citation against the text of
the rule it names. All 121 check out. I specifically re-derived the ones most
likely to drift:

- L26 → `[R-CNT-18]`, which does say a layer record nested as a sub-record is a
  layer-scope error.
- §21.7's "`[R-CNT-13]`'s prohibition on an MU = 0 record encoding file offsets
  in its own payload" — the paragraph carrying that prohibition in §7.2 does
  terminate in `[R-CNT-13]`. Correct.
- §21.6's experimental-MU=0 row citing `[R-WRT-08]` for the PE-bit drop rule —
  §20.4's preserve/drop table sits inside the block that terminates in
  `[R-WRT-08]`. Correct.
- L2's arithmetic claims: `C*N` does dominate the maximum disk ordinal
  `(C-1)*N + (N-1) = C*N - 1`; and `P*Q` does dominate `V = P*C`, since
  `Q = sum B_i >= C`. Both correct.
- §19.4's note that for `N >= 2^16` the per-channel entries of one spatial
  ordinal fall in different segments: if `N >= 65536` then
  `floor((o+N)/65536) >= floor(o/65536) + 1`. Correct.
- §21.9's note arithmetic: `ceil(2^32/2^16)*4 = 256 KiB`, and
  `ceil(2^36/2^16)*4 = 4 MiB`. Correct.
- §21.1's specialization list (F1 of F6 and F8, F35 of F36, L24 of L25) — all
  three are genuine strict specializations.

The counting criterion of §21.1 is where I found the one asymmetry that
survived: see finding **reader-02**.

---

## 8. Findings

### reader-01 — CONTRADICTION — §21.5's preamble exempts every unassigned metadata encoding from violation, but R1 in the same table registers two of the three unassigned ranges as violations

**Location.** §21.5 (preamble), against row R1 of the same table; §18.2
(`[R-MTA-03]`), §10.3 (`[R-EXT-03]`), §21.6.

**Quotation** — §21.5's preamble:

> User metadata is quarantined (`[R-CNT-25]`): every way its document can be
> unreadable takes this outcome, whatever the containing scope — as a violation
> in the rows below, except at an unassigned encoding, where no document rule
> attaches and §21.6 records the defined non-violation (`[R-MTA-10]`).

**Quotation** — row R1, four lines below it in the same subsection:

> | R1 | A user-metadata record declares a document encoding of 0, or a
> reserved-range value (3-0x7F) | encoding 0, top-level record; encoding 0,
> layer sub-record; reserved 3–0x7F, top-level record; reserved 3–0x7F, layer
> sub-record | reader | open (top-level); layer access (sub-record) |
> `[R-CNT-25]` (R-MTA-03, R-EXT-03) |

**The problem.** §18.2's value set assigns exactly 1 and 2. Three ranges are
therefore *unassigned*: 0, reserved 3–0x7F, and experimental ≥0x80. The preamble
says that at "an unassigned encoding" §21.6 records a defined non-violation.
§21.6's table has exactly one row on this subject, and it is scoped to the
experimental range alone:

> | A user-metadata record declares an experimental-range (≥ 0x80) document
> encoding | Ignored (ignore-record); the file is conforming …

So for encoding 0 and for reserved 3–0x7F — both unassigned — the preamble's
"except" clause asserts something the register flatly denies four lines later.
§17.4 states the same idea correctly, with the qualifier the preamble is missing:
"an unassigned document encoding **in a conforming file** is not a violation
(§21.6)".

**Permitted readings.** (a) "Unassigned" means every value other than 1 and 2, so
a file whose user-metadata record declares encoding 5 is conforming and a
verifier certifies it. (b) "Unassigned" is being used loosely for
"experimental", so encoding 0 and 3–0x7F remain violations under R1 and a
verifier reports *nonconforming*.

**Which I picked and why.** (b). `[R-MTA-03]` says "0 is invalid"; `[R-EXT-03]`
says "a value from a reserved range MUST NOT be emitted at all before this
specification assigns it"; R1 names both ranges explicitly and assigns them a
detector and a detection point; and the preamble's own clause "as a violation in
the rows below" points at R1. Reading (a) requires ignoring three normative
statements to honour one subordinate clause.

**What an implementer does wrong without it.** A verifier author who takes the
preamble at its word certifies a file whose user-metadata record carries
encoding 0x05, and reports it under `[R-MTA-10]`'s "records I ignored" line
rather than as a violation. A reader is unaffected — ignore-record either way.

**Byte-level: no.** Two verifiers could disagree on a verdict for a file
declaring encoding 5, but the disagreement is not licensed: `[R-MTA-03]`,
`[R-EXT-03]` and R1 all decide it against the preamble, and §21.1 has already
established that a row restates its governing rule. What is wrong is the
preamble sentence, not the outcome.

---

### reader-02 — OBSERVATION — §21.1's instance criterion is applied three different ways to "differs from a derived size" conditions (T3/T14 vs T22 vs L22), so the corpus obligation of §21.8 and `[R-VEC-03]` is not derivable from the criterion

**Location.** §21.1 (the Instances criterion), rows T3, T14, T21, T22 of §21.4,
row L22 of §21.3, and the total in §21.8 / `[R-ERR-02]`.

**Quotation** — §21.1:

> What a cell enumerates is the condition's own alternatives and containers: a
> row whose check ranges over a family without the condition changing shape
> states that range as a single instance (T24's *any codec*), and one whose
> members give the condition materially different shapes enumerates them (T15,
> T25). Instances within a cell are separated by semicolons, and a cell reading
> — is one instance; the count is therefore mechanical once the cell is written.

**Quotation** — T14 (a pure integer comparison of a stored length against a
declaration-derived size), which enumerates direction:

> | T14 | Codec 1 (none) declared and a non-sentinel index entry's length differs
> from the tile's decoded size | interleaved P·Q, length longer; interleaved P·Q,
> length shorter; planar numeric P·Bᶜ, length longer; planar numeric P·Bᶜ, length
> shorter; packed planar bool ⌈P/8⌉, length longer; packed planar bool ⌈P/8⌉,
> length shorter | reader | tile use | `[R-COD-04]` |

**Quotation** — T22, the same shape of condition (a header field compared
against the same declaration-derived size), which does not:

> | T22 | Codec 3 (zstd) and the frame's Frame_Content_Size field is present but
> does not equal the tile's decoded size | interleaved P·Q; planar numeric P·Bᶜ;
> packed planar bool ⌈P/8⌉ | reader | tile use | `[R-COD-06]` |

**Quotation** — L22, a third treatment, where the plain "≠ the formula" case
counts as a single instance:

> | L22 | Under index_encoding 1, extent_length ≠ entry_count × 20 +
> ⌈entry_count/2¹⁶⌉ × 4 — including slot (0,0) with entry_count > 0, or a
> nonzero slot with entry_count = 0 | extent_length against the formula; slot
> (0,0) with entry_count > 0; a nonzero slot with entry_count = 0 | reader |
> layer access | `[R-CNT-17]` (R-ENC-07, R-CNT-20) |

**The problem.** All three rows are the same condition shape: an integer taken
from the file is compared for equality against a quantity derived from the
layer's declarations, and the row fires on inequality. T3 and T14 treat "longer"
and "shorter" as materially different shapes and enumerate both, giving 6
instances each. T22 treats them as one, giving 3. L22 treats them as one, giving
1 for the equality clause. T21, whose condition is genuinely one-directional
("declares a window size **larger than** the tile's decoded size"), also gives 3
— which is right, and which shows the register does distinguish directionality
where it matters, making the T22/T14 divergence harder to read as deliberate.

The criterion does not resolve this by itself. "Materially different shapes" is
the test, and the register answers it inconsistently for conditions that are
structurally identical. The escape hatch — "the count is therefore mechanical
once the cell is written" — makes the *count* well defined but makes the
*criterion* unfalsifiable, which is a problem because §21.8 asserts the total as
a fact ("121 conditions over 264 instances") and `[R-VEC-03]` turns that total
into a corpus obligation ("every register row has at least one vector for each
instance it names").

**Which I picked and why.** As a reader implementer this changes nothing I do —
T3, T14, T21, T22 and L22 all reject exactly the same tiles and layers whichever
way their cells are counted. I flag it because the counts are load-bearing
elsewhere: I verified §21.8's 264 mechanically and it matches the cells as
written, so a later correction of T22 or L22 to match T14 silently invalidates
§21.8's stated total and the corpus's completeness claim.

**What an implementer does wrong without it.** A corpus builder produces 264
vectors and believes it has one per distinguishable file; it does not — it has
two directions of the codec-1 length mismatch and one direction of the
Frame_Content_Size mismatch, for no stated reason. Nobody's reader diverges.

**Byte-level: no.** No conforming implementation emits, accepts or rejects a
different byte sequence under either reading. It changes only how many files the
conformance corpus is obliged to contain.

---

## 9. Where I had to guess, and did not report

For completeness, the decisions I made that the text did not spell out but that
carry no divergence in outcome:

1. **Order of the codec-1 length check.** `[R-COD-04]` says it is "checkable from
   the entry and the layer record alone, before any payload fetch" but does not
   place it in §19.4's numbered steps. I check it between steps 4 and 5. Same
   outcome (reject-tile, T14) wherever it goes.
2. **The 128-byte floor before computing `F-64`.** §19.1 step 2 presupposes
   F ≥ 64. I test `[R-CNT-27]` first. Same outcome (reject-file, F5).
3. **The shape of the buffer I hand back for a multi-channel or multi-tile read.**
   §3.2 fixes the *values*; §2.4's Note makes reporting implementation
   technique. Not a format question.
4. **Whether to check an ignored record's extent slot.** Resolved by §19.1 step 4
   plus §5.2's "whatever the record's type" — yes. Reasoned above in §2.6.
5. **The decode bound for a user-metadata document.** An explicit MAY, floored at
   §21.9's 16 MiB (`[R-MTA-09]`).
6. **Whether an oversized document is ignore-record or a whole-file resource
   decline.** Both explicitly licensed (§18.2's Note). I chose ignore-record.

None of these is a defect. Every one of them is a place the document deliberately
left room and said so.

---

## 10. Verdict on the document, from the reader's chair

I was able to build the reader end to end. The open is exactly two ranges and
they are bounded before they are read; the trust chain never asks me to act on an
unverified integer; the tile-read algorithm resolves from a name and a coordinate
to a byte offset with no step missing; every degradation I could construct had a
stated answer and a stated blast radius; and every constant, checksum, offset,
ordinal and worked example I could recompute was correct — including the newly
authored §7.4 layer-record example, which I checked byte by byte and found
exact.

The two findings above are both in §21's register apparatus, neither reaches a
byte on disk, and neither would stop an implementation. If the gate this feeds
requires zero byte-level findings, I did not produce one, and I did look: I
walked the whole tile path, the whole open path, both metadata paths, and all
eight degradation classes, and I could not construct two conforming readers that
disagree about any byte or any verdict.
