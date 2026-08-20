# Cleanroom round 15 — Adversary transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in five `Read` calls covering lines 1–4227 (the whole document). I ran `wc -l` on
that file and one `grep`-equivalent Python pass over its text to extract the §21
register tables mechanically. Everything else I ran was local computation in a
scratch directory I created: a CRC-32C implementation, a TARN file builder, and a
partial verifier. I opened no ADR, no `docs/`, no `conformance/`, no
`spec/registry.json`, no `PLAN.md`, no `AGENTS.md`, no git history. I did not list
or read the round15 output directory. I ran no web search or fetch.

Scratch files I wrote and read back (all mine):
`scratchpad/tarn.py`, `build.py`, `chk.py`, `mk.py`, `attack.py`,
`probe1.tarn`, `empty_layer.tarn`, `pq_overflow.tarn`.

---

## 1. Calibrating the checksum and the document's own byte claims

Before attacking anything I wanted to know whether I could reproduce the
document's arithmetic, because a defect I find is worthless if my CRC is wrong.

CRC-32C per `[R-ENC-09]` — reflected Castagnoli, init `0xFFFFFFFF`, final XOR
`0xFFFFFFFF`. §4.5's check vector:

```
CRC-32C("123456789") = 0xE3069283   -> my implementation: 0xe3069283  ✓
CRC-32C(<zero bytes>) = 0x00000000  -> my implementation: 0x0         ✓
```

Then I reproduced every worked byte claim in the document. I list them because
several were the place a defect would have to hide, and none did:

| Claim | Section | Result |
|---|---|---|
| Appendix A's 128-byte file, all 128 bytes | App. A | reproduced byte-for-byte |
| trailer CRC `0xE00938D2` over trailer `[0,60)` | App. A | ✓ |
| 4-sentinel entry array CRC `0x80A34955`, stored `55 49 A3 80` | §7.4 example | ✓ |
| `crc_of_crc_array = 0xC4EE982E` over that 4-byte array | §7.4 example | ✓ |
| full all-sentinel segment CRC `0xEECB3BB2` (2¹⁶ entries) | §15.4, App. B | ✓ |
| §7.4's 81-byte layer payload field-by-field, 4+34+18+12+13 = 81 | §7.4 | ✓ |
| shuffle of `1.0,2.0,3.0` → `00 00 00 00 00 00 80 00 40 3F 40 40` | §17.3 | ✓ |
| packed bool `55 01` (fill false) / `55 FD` (fill true), P=10 | §14.3 | ✓ |
| interleaved (a:uint8, b:uint16) Q=3, size 18, ordinal 5 at `[15,18)` | §14.2 | ✓ |
| (t:float32, m:bool) Q=5, size 30, ordinal 5 at `[25,30)` | §14.2 | ✓ |
| edge tile (1,1) of (5,5)/(4,4): 1 real + 15 padding, 32 bytes | §14.5 | ✓ |
| (300,700) → s=10, in-tile ordinal 11,452; planar c=2 → 74 | §11.4 | ✓ |
| entry_count 1,000,000 → 16 segments, region 20,000,064 B, seg 15 at `[19,660,800, 20,000,000)` | §15.4 | ✓ |
| planar C=4 N=32: ordinal 74 at region `[1480,1500)`; channel 3 = entries 96–127 | §15.4 | ✓ |
| 32·20 + 4 = 644 | §20.3 | ✓ |
| 2³² entries → 256 KiB CRC array; 2³⁶ → 4 MiB | §21.9 note | ✓ |
| 4·20 + ⌈4/2¹⁶⌉·4 = 84 | §7.4 | ✓ |

Then the register's own arithmetic. §21.1 makes the instance count mechanical
("Instances within a cell are separated by semicolons, and a cell reading — is one
instance; the count is therefore mechanical once the cell is written"), so I
extracted all four tables and counted:

```
rows: 121   instances: 273
F 36 rows / 57 instances
L 49 rows / 115 instances
T 26 rows / 57 instances
R 10 rows / 44 instances
```

§21.2 says 36, §21.3 says 49, §21.4 says 26, §21.5 says 10, §21.8 says "121
conditions over 273 instances". All four subsection counts and both §21.8 figures
are exactly right. I also checked detector/detection-point consistency: every
`verifier` row carries `certification` and no `reader` row does. 20 verifier rows,
101 reader rows.

Conclusion of this pass: the document's own numbers are sound. Whatever is wrong
here is not arithmetic.

---

## 2. Building the thing

My charter is constructive, so I built. First a non-trivial file end to end
(`probe1.tarn`, 640 bytes), because guesses only surface when you have to emit a
byte.

**Layer `a`** — interleaved, rank 2, dims `y`(E=5,T=4) and `x`(E=5,T=4), so
G=(2,2), N=4, P=16. Channels `u`:uint16 fill `0xABCD`, `v`:uint8 fill `0x07`;
Q=3, decoded size 48. Codec 1, filter 1. Tiles 0 and 3 stored, 1 and 2 sentinel.

Tile 3 is the edge tile at tile coordinates (1,1). It covers y∈[4,8), x∈[4,8);
only in-tile ordinal 0 (the coordinate (4,4)) is real, ordinals 1–15 are padding
positions. `[R-SER-05]` fixes their content to fill, so:

```
A tile3 = ae 08 09 | cd ab 07 | cd ab 07 | ... (15 fill samples)
```

Index region: 4 × 20 = 80 entry bytes + one 4-byte segment CRC = 84, matching
`[R-CNT-17]`'s `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4`.

**Layer `b`** — planar, rank 1, dim `i`(E=10,T=10), one bool channel `m` with
fill true. P=10, `[R-SER-03]` decoded size ⌈10/8⌉ = 2, pad bits 2–7 of byte 1 must
carry the fill bit. Filter 2 (byte-shuffle): §17.3 says "for a packed boolean
plane s = 1 and the filter is the identity", so the stored bytes are the decoded
bytes `55 FD`. Codec 1, so `[R-COD-04]` requires entry length = 2. ✓

Plus one top-level user-metadata record, encoding 1, extent = document + terminal
CRC.

Placement (free, `[R-SLB-05]`):

```
A.t0    [16,64)   48
A.t3    [64,112)  48
A.index [112,196) 84
B.t0    [196,198) 2
B.index [198,222) 24
um      [222,273) 51
dir     [273,521) 248
pad     [521,576) 55
trailer [576,640) 64      F = 640
```

Coverage check per §9.7: claimants are front(16) + trailer(64) + directory(248) +
48+48+84+2+24+51 = 585. Slack = 640 − 585 = 55 = exactly the pre-trailer pad. The
partition holds and the slack total is what `[R-CNT-21]` says it is.

**Where I had to guess while building this: nowhere.** Every field's width,
order, domain and cross-check is pinned. That is a genuinely good result for a
container this size, and it is why the findings below are all at the edges rather
than in the middle.

I then built the two degenerate files. `empty_layer.tarn` (192 bytes) carries one
layer with dim `x` at E=0, T=1, one uint8 channel — N=0, entry_count=0, extent
slot (0,0), crc_of_crc_array 0. Conforming, and every rule I could apply agreed.

---

## 3. Attacks tried, and what forecloses them

I will be explicit about the ones that died, because an empty result is only
worth something if the attacks were good.

### 3.1 Two structures claiming the same bytes

- Record extent overlapping the directory region → `[R-CNT-13]` "any overlap
  between two structures neither of which belongs to a layer as reject-file",
  registered F33 whose Instances cell explicitly lists "directory region".
  **Foreclosed.**
- A layer sub-record's extent overlapping the directory → `[R-CNT-13]`'s "touching
  another scope's structures as reject-file", F33's "a layer structure against
  another scope's structure". **Foreclosed.**
- A layer's index region overlapping its own sub-record extent — note that
  `[R-CNT-13]`'s *enumeration* only names "a stored extent overlapping its own
  layer's index region or sub-record extents", which does not cover
  index-vs-sub-record. But the sentence opens with the general "an intra-layer
  overlap — including …", and L18's condition is stated generally ("Two structures
  of one and the same layer claim overlapping bytes"). **Foreclosed**, by the
  general clause rather than the enumeration.
- Two layer records sharing one extent slot (one index region) → cross-layer
  overlap, F33. **Foreclosed.**
- A stored extent reaching the front block or the trailer → T8/T9, and F33's
  Condition cell explicitly routes those to the bounds rows at their own tier.
  **Foreclosed.**

### 3.2 Zero-length and degenerate structures

- Extent (0,0) is "no extent" (`[R-CNT-13]`) and is therefore not a claimant; it
  cannot overlap. A half-zero slot is F30/L15. **Foreclosed.**
- Zero-length stored tile → T10, and §17.2's Note plus `[R-COD-08]` justify it
  ("Decoded output is never empty — §14's decoded sizes are at least 1 byte").
- The smallest conforming file: 128 bytes, reproduced from Appendix A exactly.
  I also confirmed it is not unique — dir_offset = 60, dir_length = 4 gives
  another 128-byte conforming file with a zero-length pre-trailer pad, since
  `[R-CNT-06]` permits `dir_offset + dir_length ≤ F − 64` with equality. Nothing
  in the document claims uniqueness, so this is not a defect.
- A layer with every dimension extent 0: N=0, entry_count=0, extent (0,0),
  crc_of_crc_array = 0. Note the pleasing coincidence that CRC-32C of zero bytes
  *is* 0, so `[R-CNT-23]`'s mandated 0 equals the correct CRC of the empty array.
  §15.4's closing example says so.
- A tile with zero real positions: **unconstructible.** For every addressed tile,
  tᵢ < Gᵢ = ⌈Eᵢ/Tᵢ⌉ implies tᵢ·Tᵢ < Eᵢ, so the all-zero in-tile position is always
  real. Good: there is no degenerate all-padding stored tile.

### 3.3 Arithmetic overflow

I looked for a formula whose *intermediate* value can exceed 2⁶³ − 1 even when
its result cannot, since §11.2's Note shows the document is alert to exactly that
("The stated form of the ceiling division avoids the idiom (Eᵢ + Tᵢ − 1)/Tᵢ").

- `F − 64` is a **difference**, and `[R-ENC-04]` names only "a sum or product". If
  committed_file_length were 0 this underflows. But §6.2's field gates include
  "committed_file_length equals the file size", and a reader that has read a
  trailer has a physical size ≥ 64; a mismatched committed length is F17 →
  reject-file on the same pass. The verdict is the same whichever order a verifier
  evaluates the gate set in. **Foreclosed.**
- §15.4's `min((s+1)·2¹⁶, entry_count)`: the intermediate `(s+1)·2¹⁶` exceeds
  2⁶³ − 1 only for entry_count near 2⁶³. But `[R-CNT-17]` ties extent_length to
  `entry_count × 20 + …`, and L2 registers that product's overflow at layer
  access, capping entry_count at about 4.6 × 10¹⁷ ≈ 2⁵⁸·⁷. At that ceiling
  `(s+1)·2¹⁶ ≤ entry_count + 2¹⁶ − 1`, comfortably in domain. And layer access
  precedes tile use. **Foreclosed**, though only by the chain.
- `offset + length` in an index entry: both fields can be 2⁶³ − 1, and T12
  registers the overflowing sum separately from T9's bound against F − 64, so the
  wrap is caught before the comparison. **Foreclosed.**
- Interleaved value offset `(k div C)·Q + F_{k mod C}` maxes at `P·Q − B_{C−1}`,
  which is in domain whenever P·Q is. Disk ordinal maxes at `C·N − 1`, and L2's
  cell says exactly that ("C·N (which dominates the max disk ordinal
  (C−1)·N + (N−1))"). I verified both dominations algebraically. **Foreclosed.**
- `P·Q` and `P·Bᶜ` in a layer with **zero addressed tiles**: **this one survived.**
  It is finding `adversary-01` and §4 works it in full.

### 3.4 The slab machinery (§16.2 — a changed section)

The paragraph I spent most time on:

> Sentinel tiles are transparent to run continuity: they occupy no bytes and do
> not break packing. So are the entries §15.3 classifies reject-tile on a
> *structural* ground: they address no usable extent, and the run's stored tiles
> close over them. An entry whose only defect is that its stored bytes fail its
> crc is not transparent — its offset and length stand, and the packing relation
> reads them as it does any other stored tile's — so this invariant stays
> decidable from the index entries alone, given the committed file length §15.3
> already requires to classify any entry.

I tried to fork a verdict on it and could not, and the reason is structural: the
transparency question only ever arises for an entry that *itself* carries a
violation. A structurally-rejected entry is T6/T7/T8/T9/T10/T11/T12; a
crc-failing entry is T1. Either way the file is already nonconforming, so the
transparency rule changes only *which rows fire*, never the verdict. Concretely,
with S=4, A_slab=1, tiles at 4096(len 10), 4106(len 10, crc wrong), 4116(len 10),
ordinal 3 sentinel: packing holds, T1 fires. Swap the middle entry for one with
offset 5: it is transparent, so the run must close (tile 2 at 4106), and T8 fires
either way.

So §16.2's repair is **verdict-neutral by construction**. It matters for corpus
vectors (whether L41 also fires) and not for certification. I record that as a
positive result: I could not turn it into an attack.

I also checked the boundaries: `A_slab = 1` is a power of two (2⁰) and §16.2's
closing Note confirms it is intended ("With A_slab = 1 a slab is
contiguity-only"); runs never span channel blocks (`[R-SLB-02]`); a run with no
stored tiles imposes nothing; S may exceed N, giving a single short run. All
consistent.

`[R-SLB-04]` says "A writer or updater whose **commit** changes … MUST either
re-establish the invariants … or clear the declaration." A compaction is not a
commit (§9.1 makes it the other branch), so `[R-SLB-04]` does not bind a
compactor by its own terms. I chased this: §20.5's "Given a conforming input the
output is a conforming file" plus `[R-SLB-03]`'s status as a file-level invariant
close it, and `[R-WRT-05]`/`[R-WRT-07]` forbid the compactor from *clearing* the
declaration, since the only permitted layer-record edits are the extent slot and
crc_of_crc_array. So a compactor must lay out slab runs to satisfy the invariant,
which it always can. **Foreclosed**, by a four-step chain rather than a sentence.

### 3.5 Reserved / experimental / unknown values in every position

- Reserved-range record type at file scope: F35 (MU=1, reader) and F36 (any MU,
  verifier), and §21.1 declares F35 a specialization of F36. At layer scope:
  L24/L25 the same way. **Foreclosed.**
- Experimental-range record type, MU=0: §21.6 non-violation, ignored, PE governs
  preservation. MU=1: §21.6's second "conforming file a reader nevertheless
  refuses", and §2.3 gives the verifier *cannot establish*. **Foreclosed and
  deliberate.**
- Reserved/experimental values in linearization, layout, sample type, codec,
  filter, index encoding: all reject-layer, all registered (L31/L33/L34/L36/L43/
  L45), each cell enumerating the ranges. **Foreclosed.**
- Metadata encoding: 0 and reserved 3–0x7F are R1 violations (ignore-record);
  experimental ≥0x80 is a §21.6 non-violation with a mandated verifier report
  (`[R-MTA-10]`). §21.5's preamble states the split explicitly and correctly:
  "what `[R-MTA-10]` withdraws is the document's content rules, never the
  encoding byte's own value set". **Foreclosed** — and this is the tightest
  reserved/experimental seam in the document.
- A user-metadata extent of exactly 5 bytes (`[R-CNT-25]`'s floor): under
  encoding 1 the document is 1 byte, which cannot be a JSON object → R7,
  nonconforming. Under an experimental encoding it is **conforming**, because no
  content rule attaches. I like this file; both verifiers certify it, and it is
  the sharpest legal use of the quarantine. Not a defect.
- Reserved trailer flag bits: incompat lane → F19; ignore lane → §21.6
  non-violation, copied forward by updaters and compactors. **Foreclosed.**
- Reserved record flag bits 2–15 → F26/L47, verifier. MU=1/PE=0 → F25/L46,
  verifier, read as PE=1. **Foreclosed.**

### 3.6 The reader/verifier seam

`[R-CNF-12]` licenses a reader to reject any nonconforming file, including on
verifier-detected grounds, so the seam cannot produce a *conformance* fork — it
produces a licensed behavioural difference. A file whose only defect is F26 (a
reserved flag bit) is read completely by a conforming reader and rejected by a
verifier, and both are conforming. That is the design.

The one place the seam bites *certification* is resource capability: §21.9's
guarantees are a floor, `[R-ERR-04]` lets a reader decline above them, and §2.3
turns a verifier's decline into *cannot establish*. So a 512 MiB tile, or a
20 MiB metadata document, is certified by a large verifier and not by a small
one. **This is stated, deliberate, and repeated three times** (`[R-COD-11]`,
`[R-MTA-09]`, `[R-ERR-04]`). Not a defect, but it is the answer to "can two
conforming verifiers judge a file differently": yes, on capability, by design.

### 3.7 §20.3's declaration-change bar (a changed section)

I read step 4's bar closely and tried to break it:

> A commit MUST NOT change a layer's declarations in a way that alters, for any
> tile that layer stores **in the generation this commit supersedes**, what §14
> fixes for its stored bytes or how they decode

I checked what it does and does not bar. Adding a channel to a **planar** layer
is not barred: existing planes' decoded sizes are unchanged (P·Bᶜ), disk ordinals
c·N+s are unchanged because N is unchanged, and padding positions are unchanged.
Removing the *last* planar channel is likewise not barred. Shrinking an extent
across a grid boundary removes tiles from the address space rather than altering
what §14 fixes for a tile that survives, so its status is genuinely unclear from
step 4's text — but §21.7 declares the whole bar unwitnessed in a single file
("witnessed only where the affected tiles remain stored — the §21.4 rows then
fire"), so no verifier can fork on it. **Foreclosed for verdict purposes**, and
this is the right disposition: the bar is a writer-conduct rule with no
single-file witness.

Two smaller things in step 4 did survive as findings: `adversary-05` (the "one
such bound" claim) and, adjacent to it, `adversary-06` in §21.7.

### 3.8 The appender carrying a malformed entry forward

> a malformed index entry an appender meets while re-emitting a region is carried
> forward byte-identically at its disk-ordinal position under step 4, not repaired
> to a sentinel … Reproducing a structure's bytes unchanged is not authoring them

This is a nice repair and it holds. The appender re-emits the whole region at a
new placement, so it literally produces the malformed entry's bytes; the carve-out
is what keeps `[R-CNF-05]` from making the appender nonconforming. The output file
is nonconforming either way (T8 or whichever row), so both verifiers reject it and
there is no fork. **Foreclosed.**

Note the ambiguity of "stored" that this exposes and that the document handles:
§3.1 defines *stored* as "its index entry is not the sentinel", so a malformed
non-sentinel entry names a *stored* tile; §9.7 says such an entry "contributes no
stored extent to the walk"; §16.2 says its run's "stored tiles close over" it.
Three usages, each carved out where it differs. I checked each site and found no
place where the wrong reading is reachable — in particular `[R-WRT-09]`'s "every
stored tile's entry crc" uses §3.1's sense, so a compactor meeting a malformed
entry fails a check it is obliged to make and must refuse. That is what stops a
compactor from having to invent an offset for an entry that addresses nothing, a
question §20.5 otherwise never answers.

### 3.9 Register completeness

§21.1 makes completeness normative, so I walked every requirement identifier
looking for a detectable file-conformance violation with no row. I checked all of
`CNF`, `MDL`, `ENC`, `CNT`, `LIF`, `EXT`, `GEO`, `IDX`, `SLB`, `TYP`, `SER`,
`COD`, `MTA`, `RDR`, `WRT`, `ERR`, `SEC`, `PRV`, `VEC`. Every MUST is either
registered, a reader/writer procedure with no file witness, expressly declared a
conduct rule (`[R-CNF-02]`, §10.3, §18.3), or accounted for in §21.7. I found no
missing row. I also verified the twin rows F↔L pairwise for enumeration drift
(F21/L10, F22/L11, F23/L12, F24/L13, F25/L46, F26/L47, F28/L49, F27/L48, F29/L14,
F30/L15, F31/L16, F32/L17, F33/L18, F34/L19, F35/L24, F36/L25, F4/L9). Every pair
scales correctly by container count — one container at file scope, two at layer
scope — with **one exception**, F23/L12, which is `adversary-07`.

---

## 4. Findings

### adversary-01 — AMBIGUITY — the decoded-size overflow check in a layer that addresses no tiles

**Location:** §14.2 `[R-SER-02]`, §14.3 `[R-SER-07]`, §4.2 `[R-ENC-04]`, §17.2's
Note after `[R-COD-07]`, §21.3 row L2.

**Quotation** (§17.2, the Note following `[R-COD-07]`):

> The cap is quantified over the layer's *addressed* tiles, so a layer that
> addresses none — any dimension extent 0 (`[R-GEO-02]`, §21.6) — satisfies it
> whatever its tile shape declares, and codec 4 is conforming there. … `[R-ENC-04]`'s
> overflow rule carries no such quantifier — it binds any sum or product a file
> yields — so P·Q and P·Bᶜ are checked in an empty layer even though this cap is not.

**The construction.** `pq_overflow.tarn`, 192 bytes, built and re-parsed:

```
89 54 41 52 4e 0d 0a 1a 00 00 00 00 00 00 00 00   front block
01 00 03 00 50 00 00 00 00 00 00 00 00 00 00 00   record hdr: type 0x0001, MU=1 PE=1,
00 00 00 00 00 00 00 00                            inline_length 80, extent (0,0)
01 71                                              name len 1, "q"
01                                                 layout 1 = interleaved
01 00  01 00  01 00                                linearization 1, codec 1, filter 1
00 x8  00 x8  00 x8                                A = 0, S = 0, A_slab = 0
01                                                 rank d = 1
01 00                                              channel count C = 1
01 78                                              dim name "x"
00 00 00 00 00 00 00 00                            extent E = 0
00 00 00 00 00 00 00 40                            tile extent T = 2^62
01 63  0d 00  08 00 00 00 00 00 00 00 00           channel "c", type 13 = float64, fill 8 zero bytes
01                                                 index_encoding 1
00 x8                                              entry_count = 0
00 00 00 00                                        crc_of_crc_array = 0
4c 9a 4e 5d                                        directory CRC
00 00 00 00                                        4-byte pre-trailer pad
8a 4e 52 41 54 0d 0a 1a … 8f 20 e4 c0              trailer, F = 192
```

I re-parsed the emitted bytes and confirmed the file is clean on **every other
axis**: front block exact; trailer magic, CRC, version 1, flags 0, generation 1,
dir_offset 16, dir_length 108, dir_offset+dir_length = 124 ≤ F−64 = 128, F = 192 ≡ 0
(mod 64), file_id ≠ 0, reserved zero; directory CRC verifies; the record parses
with zero residue; the layer payload parses with zero residue; name/dim/channel
names valid; layout, linearization, codec, filter, index_encoding all assigned
values; A=0 so A_slab=0 (`[R-CNT-23]`); fill length 8 = float64's element size;
G = ⌈0/2⁶²⌉ = 0, N = 0, addressed-tile count 0 = entry_count, extent slot (0,0)
per `[R-CNT-17]`, crc_of_crc_array 0; coverage partitions with 4 bytes of slack.
Codec is 1, not 4, so `[R-COD-07]`'s lz4 cap — the one empty-layer quantifier the
document settles normatively — is not in play.

The single arithmetic fact at issue: P = ∏Tᵢ = 2⁶² (in domain), Q = ΣBᵢ = 8, so
the layer's declared interleaved **decoded size** P·Q = 2⁶⁵ = 36,893,488,147,419,103,232,
against the ceiling 2⁶³ − 1 = 9,223,372,036,854,775,807. Every *other* derived
quantity is in domain: N = 0, N·P = 0, C·N = 0, V = P·C = 2⁶², entry_count×20 = 0.
A planar variant with the same declarations gives P·Bᶜ = 2⁶⁵ identically.

**Permitted readings.**

*Reading A — the check applies; the layer is rejected; the file is nonconforming.*
`[R-SER-02]` closes with "These products and sums are declaration-derived
quantities under `[R-ENC-04]`", and `[R-SER-07]` with "Every decoded size, and the
value count V, is a declaration-derived quantity under `[R-ENC-04]`." Neither
sentence is qualified by the existence of a tile, and `[R-SER-07]` says in the same
breath that "decoded size is a function of the layer's declarations alone …
never of payload content". L2's Instances cell names "P·Q (which dominates
V = P·C); P·Bᶜ" at detection point *layer access* with no qualifier. §17.2's Note
states this outcome in terms.

*Reading B — there is no decoded size to check, and the file is conforming.*
§14 opens "This section defines the **decoded tile image**: the byte sequence a
**stored tile's** payload decodes to under §17's codec pipeline". `[R-SER-07]`'s
operative sentence is about "a decoded payload whose byte length is not exactly
that decoded size" — it presupposes a payload. `[R-ENC-04]` binds "any quantity
this specification defines as a sum or product of integers **obtained from a
file**", and its parenthetical inventory — "offsets plus lengths, grid counts,
tile counts, sample-position counts, ordinals" — does not name a decoded byte
size. §19.3's layer-access checklist, which is where L2 places detection, lists
"the geometry floor and its arithmetic (`[R-GEO-01]`–`[R-GEO-03]`)" and does not
cite `[R-SER-02]` or `[R-SER-07]`. A layer with zero addressed tiles has no tile,
hence no tile image, hence no decoded size to overflow — the same reasoning
`[R-COD-07]`'s quantifier makes explicit one paragraph earlier.

**Which I picked, and why.** Reading A. `[R-SER-02]` and `[R-SER-07]` are
unqualified normative sentences and they are directly on point; L2 corroborates.
But I want to be precise about what decides it and what does not. The *only*
sentence in the document that addresses the empty-layer case for `[R-ENC-04]` is
in a **Note**, and §2.1 removes its force: "All text in this document is normative
except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*".
The document evidently regards the empty-layer quantifier question as one needing
an explicit answer — it gives `[R-COD-07]`'s half of the answer twice in normative
text (§17.2's rule, and §20.3 step 4's "which an empty layer escapes only because
that cap is quantified over addressed tiles") — and gives `[R-ENC-04]`'s half only
in a Note.

**What an implementer does wrong without it.** A writer that reasons "no tiles, no
tile image, so no decoded size" declares an enormous tile shape on a schema-first
empty layer and later discovers, at the first commit that grows the extent, that
its layer was never legal. A verifier that reasons the same way certifies
`pq_overflow.tarn`; one that follows `[R-SER-02]` rejects the layer and reports
the file nonconforming. There is no third structure in the file to break the tie.

**Byte-level: yes.** Verifier A rejects the layer, so the file is nonconforming
and is not certified. Verifier B finds no violation and certifies. The two
disagree about the accept/reject verdict on the 192 bytes above, and each can cite
normative text. Naming them: A cites `[R-SER-07]`'s "Every decoded size … is a
declaration-derived quantity under `[R-ENC-04]`" and L2's P·Q instance; B cites
§14's scoping to "a stored tile's payload", `[R-ENC-04]`'s "obtained from a file",
and §19.3's checklist. The disambiguating text exists but sits where §2.1 gives it
no force.

**Suggested repair** (one sentence, normative): move §17.2's Note sentence into
`[R-SER-02]` or `[R-SER-07]` — e.g. "A layer's decoded sizes are declaration-derived
and subject to `[R-ENC-04]` whether or not the layer addresses any tile."

---

### adversary-02 — CONTRADICTION — §11.1's parenthetical is false at Eᵢ = 0

**Location:** §11.1, `[R-GEO-01]` versus `[R-GEO-02]` and §11.2 `[R-GEO-03]`.

**Quotation** (§11.1, `[R-GEO-01]`):

> A tile extent MAY exceed its dimension's extent (the grid is then a single
> padded tile along that axis).

**Against it** (§11.1, the very next paragraph, `[R-GEO-02]`):

> A dimension with extent 0 is valid: its grid count is 0, the layer has zero
> addressed tiles, its tile index has zero entries, and its reference array is
> empty.

**The construction.** Eᵢ = 0, Tᵢ = 4. Tᵢ exceeds Eᵢ, so the parenthetical says the
grid along that axis is "a single padded tile". `[R-GEO-02]` says the grid count is
0, and `[R-GEO-03]`'s ceiling division gives ⌈0/4⌉ = 0 ("equal to Eᵢ/Tᵢ plus 1 if
Eᵢ mod Tᵢ ≠ 0"; 0 mod 4 = 0). The two adjacent sentences give 0 and 1 for the same
layer.

**Detail.** The consequence, taken literally, is byte-visible: a writer that
computed Gᵢ = 1 for a zero-extent axis would emit entry_count = ∏Gⱼ instead of 0,
a nonzero extent slot instead of (0,0), a 24-byte index region holding one
sentinel, and a nonzero crc_of_crc_array — a file three rows of §21.3 reject
(L21, L22, L27). But I do not think any implementation lands there, because
`[R-GEO-02]` states "its grid count is 0" in the next breath and `[R-GEO-03]`'s
formula is explicit and unambiguous, and both are the sentences an implementer
actually computes from. The parenthetical is describing the ordinary case
(0 < E < T) and is simply not guarded for E = 0. §11.1 is one of this round's
changed sections and this is the "collides with a neighbouring sentence nobody
re-read" shape.

**Byte-level: no.** `[R-GEO-02]` and `[R-GEO-03]` each state Gᵢ = 0 for Eᵢ = 0
directly and unambiguously, so no competent implementation reaches the other side;
the defect is a false statement in normative text rather than an open question.

**Suggested repair:** "(where 0 < Eᵢ < Tᵢ the grid is then a single padded tile
along that axis)".

---

### adversary-03 — CONTRADICTION — §21.2's preamble excludes rows that do reach a foreign-major file

**Location:** §21.2's opening paragraph, versus rows F1, F6, F8, F14 and §6.2's
`[R-CNT-06]`, §6.1's `[R-CNT-04]`, §6.3's `[R-CNT-24]`.

**Quotation** (§21.2):

> Every row here presupposes a file this specification judges: one declaring
> format major 1. A file declaring another major is neither conforming nor
> nonconforming under this text (§2.3, `[R-CNF-02]`), and no row below reaches it —
> §6.2's ordered validation puts the version gate ahead of every check but the
> trailer magic and the trailer CRC, so a foreign-major file is refused on
> capability grounds before any geometry row applies.

**Against it** — the sentence's own justification clause concedes two checks
precede the version gate, and each is a registered row: F8 ("The 8 bytes at F-64
are not exactly the trailer magic"), F14 ("The u32 at trailer offset 60 does not
equal the CRC-32C of trailer bytes [0,60)"), and F1's trailer-magic instance. A
third row is outside §6.2's ordering entirely: `[R-CNT-04]` places the front-block
check "before other processing", and `[R-CNT-24]` makes the front block "constant"
in *every* format major version, so F6 reaches a file declaring any major. And
F18 registers version_major = 0 — a file that declares no major at all, so the
presupposition "one declaring format major 1" excludes the very row §21.6 points
back to ("version_major = 0, permanently invalid in every format major version
(F18, `[R-CNT-07]`)").

**Detail.** Two readings of what a verifier reports for a file declaring
version_major = 3 whose front signature block is corrupt. (i) F6 is established, so
`[R-CNF-11]`'s "An established violation takes priority" applies and the verdict is
*nonconforming*. (ii) §21.2's "no row below reaches it" applies, so the verifier
reports *cannot establish* on capability grounds. I picked (i): §6.1's check runs
before any trailer field is read, and `[R-CNT-24]` makes the front block's
constancy a permanent cross-major invariant, so F6 is genuinely a finding about
the bytes and not about the reader's capability. For the trailer-magic and
trailer-CRC rows, reading (ii) is untenable for a different reason — `[R-ENC-10]`
forbids acting on version_major before the trailer CRC verifies, so a verifier
with a failed CRC cannot even establish that the file declares a foreign major.

**What an implementer does wrong without it.** It writes the wrong diagnostic:
"TARN format major 3; this reader supports major 1" (which §6.3 asks for) instead
of "corrupt signature", or the reverse — and §6.3 says precisely why that matters,
"a reader that reports an unimplemented major as corruption misleads users into
discarding files that current software reads".

**Byte-level: no.** Under both readings the verifier declines to certify —
*cannot establish* and *nonconforming* both bar certification (`[R-CNF-11]`: "a
verifier MUST NOT certify a file it reports that way"). The fork is in the
reported verdict and the diagnostic, not in accept/reject.

**Suggested repair:** narrow the claim to what the justification supports — "no
row below other than F1, F6, F8 and F14 reaches it", or "no row below that depends
on a field this text defines reaches it".

---

### adversary-04 — AMBIGUITY — §21.7's second class lacks the `[R-CNF-11]` disclaimer its first class carries

**Location:** §21.7, `[R-ERR-01]`, paragraph 1 versus paragraph 2; §2.3
`[R-CNF-11]`.

**Quotation** (§21.7, end of paragraph 1):

> None of these is a requirement a verifier is *unable to check* within the
> meaning of `[R-CNF-11]`: no file-level witness exists to check, so nothing about
> the file is left undetermined and the verdict is unaffected.

Paragraph 2 opens "A second set of obligations is omitted from the register
because a single file exhibits no witness of their violation" and enumerates
`[R-LIF-01]`, `[R-LIF-03]`, `[R-GEO-06]`, `[R-SER-01]`, `[R-CNT-13]`'s offset
prohibition, `[R-CNT-18]`'s nesting prohibition, §20.3 step 4's bar, and
`[R-ENC-06]` — and ends, at `[R-ENC-06]`, with **no** corresponding sentence.

**Detail.** The two paragraphs share their reason for omission (no single-file
witness) but only the first says what that means for the verdict. Permitted
readings: (i) the disclaimer is general and covers both classes, so a verifier's
verdict is unaffected by these; (ii) the disclaimer's placement is deliberate and
paragraph 2's obligations *are* things a verifier "is unable to check", in which
case `[R-CNF-11]` obliges the verifier to report them as unchecked and — because
"*cannot establish* is available only to a traversal that established no
violation" and the verifier has established none — to report *cannot establish*
for **every** file, including Appendix A's. I picked (i): `[R-CNF-11]` qualifies
its ground twice as "a capability or resource ground", and the absence of a
witness is neither. The 16 uses of *cannot establish* in §2.3, §17.4, §18.2 and
§21.9 all instantiate capability or resource, never absence-of-witness.

**What an implementer does wrong without it.** Reading (ii) is catastrophic — no
file is ever certifiable — which is why I rate it unreachable in practice. But the
asymmetry is exactly the "enumeration extended in one place and not its twin"
shape, in a changed section, and it costs one sentence to close.

**Byte-level: no.** `[R-CNF-11]`'s "on a capability or resource ground" qualifier
excludes absence-of-witness on its face, so no competent verifier lands on reading
(ii); nothing about the certified/rejected boundary is genuinely open.

---

### adversary-05 — CONTRADICTION — §20.3 step 4 names the lz4 cap as the only bound a grown geometry can breach

**Location:** §20.3, `[R-WRT-04]` step 4; versus §4.2 `[R-ENC-04]`, §11.2
`[R-GEO-03]`, §7.4 `[R-CNT-17]`, §21.3 row L2.

**Quotation** (§20.3 step 4):

> and an extent MAY **grow**, since a position that becomes real held that
> channel's fill and fill is a legal sample value — provided the grown geometry
> stays within every bound the layer's own declarations impose, `[R-COD-07]`'s lz4
> decoded-size cap being the one such bound in format major 1 (L44), which an
> empty layer escapes only because that cap is quantified over addressed tiles.

**Against it** (§11.2, `[R-GEO-03]`):

> These products, like all geometry arithmetic, are subject to `[R-ENC-04]`: a
> reader MUST treat a product exceeding 2⁶³ − 1 as a validity error at layer scope.

**The construction.** A layer with d = 1, T = 1, C = 1, currently E = 100 (so
N = 100, entry_count = 100, index region 2004 bytes — every quantity in domain).
A commit grows E to 2⁶². Now G = N = entry_count = 2⁶², which is in domain, but
`[R-CNT-17]`'s region length `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4` ≈ 20 · 2⁶²
= 2·2⁶⁶, far past 2⁶³ − 1 — a bound L2's Instances cell registers by name
("entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4"). The layer's codec is 1, so
`[R-COD-07]`'s cap is not in play at all. Growth also reaches N·P and C·N by the
same route.

**Detail.** Two readings of "every bound the layer's own declarations impose".
(i) It means every bound, in which case "the one such bound in format major 1
(L44)" is false, since `[R-ENC-04]`'s domain bounds on N, N·P, C·N and the index
region length are equally imposed by the layer's declarations and equally breached
by a grow. (ii) It means only bounds *quantified over the layer's addressed tiles*
— the distinction §17.2's Note draws ("`[R-ENC-04]`'s overflow rule carries no such
quantifier") — in which case the sentence is true but says much less than it
appears to, and the writer guidance it gives is incomplete. I picked (ii) as the
intent and (i) as what the words say; the sentence needs to say which.

**What an implementer does wrong without it.** An appender that treats L44 as its
only pre-flight check on a grow emits a commit whose new layer record is rejected
at layer access by L2. It costs a wasted commit, and since `[R-LIF-01]` freezes the
committed prefix, the damage cannot be undone in place.

**Byte-level: no.** The emitted file is nonconforming under both readings — L2
fires on the bytes regardless of what the appender believed — so no two verifiers
disagree about it. The defect is in writer guidance.

---

### adversary-06 — CONTRADICTION — §21.7 over-claims that the ordinal mappings have no witness

**Location:** §21.7 `[R-ERR-01]`, paragraph 2; versus §14.5 `[R-SER-05]` and
§21.4 row T4.

**Quotation** (§21.7):

> the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a
> structurally valid tile whatever values it carries

**Against it** (§14.5, `[R-SER-05]`):

> at every padding position, a writer MUST encode, for each channel the position
> carries, that channel's fill value … a verifier MUST check it, and a violation
> is a validity error at tile scope.

**The construction.** Interleaved layer, d = 1, dim `x` with E = 5, T = 4, one
uint8 channel with fill `0x5A`. G = 2, N = 2, P = 4, decoded size 4. Tile at tile
coordinate 1 covers x ∈ [4,8): in-tile ordinal 0 is real (x = 4), ordinals 1–3 are
padding, so `[R-SER-05]` fixes the decoded tile to `v 5A 5A 5A` for the stored
sample v. A writer that implements `[R-SER-01]`'s value sequence in the reverse
in-tile order emits `5A 5A 5A v`. A verifier applying the correct mapping reads
ordinal 3 — a padding position — and finds `v`, not the fill byte. T4 fires
whenever v ≠ `0x5A`. So the mapping violation *is* witnessed, in exactly the
places §21.7's own first paragraph identifies for `[R-COD-10]`: "The obligations of
§14.5 and `[R-SER-08]` narrow this only where content is structurally
constrained: padding positions, pad bits, and boolean bytes."

**Detail.** The parallel is exact: a wrong shuffle stride (`[R-COD-10]`) and a
wrong in-tile ordinal (`[R-SER-01]`) both produce a decoded image whose bytes are
individually legal but misplaced, and both are caught precisely where §14.5 or
`[R-SER-08]` constrains a byte's content. §21.7 gives the first case an honest,
qualified treatment in paragraph 1 and registers it as T26; it gives the second an
unqualified "whatever values it carries" in paragraph 2 and registers nothing. The
correct statement is that the mappings are unwitnessed *in a tile with no padding
position, no pad bit and no bool channel*, and witnessed by T4 or T2 otherwise.

**Byte-level: no.** The file exhibiting the mis-ordering is nonconforming via T4,
and every verifier that discharges its `[R-SER-05]` obligation finds it. The
defect is that §21.7's account — which §21.1 calls "the account, by class, of what
fails" the detectability gate — mis-classifies one class.

---

### adversary-07 — OBSERVATION — §21.1's magnitude criterion is applied to L30 but not to F23/L12

**Location:** §21.1's instance criterion; rows F23 and L12 versus row L30.

**Quotation** (§21.1):

> Where the condition compares two **magnitudes** either of which can be the
> greater — a *differs from* or *does not equal* — the two directions are likewise
> enumerated; where its own text bounds the comparison in one direction — an
> *exceeds*, a *larger than* — there is one. A comparison with no magnitude
> ordering enumerates no direction: a stored checksum against a computed one, or a
> byte pattern against a constant, is equal or it is not, and *greater* names
> nothing.

**The two rows.**

> F23 | A top-level user-metadata record's inline_length is not 1; the encoding
> field is a fixed structure, not a growable one | — | reader | open |
> `[R-MTA-03]` (R-ENC-07)

(one instance; L12 is its layer-scope twin, also one) against

> L30 | A channel entry's fill length prefix differs from the element size of the
> channel's declared type | prefix longer than the element size; prefix shorter
> than the element size | reader | layer access | `[R-CNT-23]` (R-TYP-06)

(two instances).

**Detail.** Both rows compare a length field against a required value, and in both
the field can be greater or lesser: inline_length can be 0 (the encoding byte
absent) or ≥ 2 (extra bytes), materially different files. §21.1's carve-out covers
"a byte pattern against a constant", and inline_length is a magnitude rather than a
byte pattern — the very distinction the criterion draws. So by the criterion's own
terms F23 and L12 should each enumerate two directions, making §21.8's totals 275
instances rather than 273 and adding two vectors to the corpus under
`[R-ERR-02]`/`[R-VEC-03]`'s "one vector per instance". The counter-reading is that
the row's explanatory clause "not a growable one" bounds the comparison in the
*larger* direction; but §21.1 says "where its own text bounds the comparison", and
the *condition* text is the unbounded "is not 1".

I checked every other row against the criterion and found no second instance of
this. The near-misses are all defensible: L41's three alternatives are stated in
its own condition text ("gap, overlap, or out-of-ordinal placement") and so qualify
under "one of several alternatives the condition text states"; L23's "overrun or
truncation" are one direction described from two sides; L29's "A_slab = 0" is a
below-the-floor case where L39 has no counterpart because A = 0 is legal.

**Byte-level: no.** This changes the size of the conformance corpus, not any
file's verdict. Both verifiers reject an inline_length of 0 and of 2 alike, under
the same rule.

---

## 5. What I could not determine

- Whether a **shrink** of a dimension extent that removes stored tiles from the
  address space is barred by §20.3 step 4. The clause quantifies over "any tile
  that layer stores in the generation this commit supersedes" and asks whether the
  change "alters … what §14 fixes for its stored bytes or how they decode" —
  removing the tile from the addressed set does neither, on a literal reading.
  §11.1's Rationale says a shrink "is barred wherever it alters what §14 fixes for
  a tile the layer already stores (§20.3, which states the tense normatively and
  governs)", which defers to §20.3 rather than answering. I did not report this
  because §21.7 makes the whole bar unwitnessed in a single file, so no verifier
  verdict turns on it — but an appender author has to guess.
- Whether a compactor may relocate the extent of an **MU = 1 record type it
  implements** whose registration defines offsets *inside the extent* while
  Appendix G's item 3 sort key uses "the contents of its extent". The key would
  then depend on placement, which depends on the key. Format major 1 registers no
  such type, and Appendix G is non-normative, so I did not report it.
- Whether `[R-WRT-06]`'s "fresh file_id … and generation 1" belongs in §21.7's
  second class. It is a history property with no single-file witness, and
  §21.7 ¶2's "the generation sequence (`[R-LIF-01]`, `[R-LIF-03]`)" arguably
  already covers it. Too marginal to file.

## 6. Honest ranking of the surviving attack

Only `adversary-01` reaches concrete bytes with two defensible verdicts. My
estimate of how plausibly a real implementation lands on each side: reading A
(reject) is what I would expect from an implementation that derives its layer
validation from §21's register, since L2 names P·Q at layer access without a
qualifier — call it the likely majority. Reading B (certify) is what I would expect
from an implementation that derives its validation from §19.3's checklist, which
does not cite `[R-SER-02]` or `[R-SER-07]`, and which computes decoded sizes lazily
at tile use — a perfectly ordinary architecture, and one for which a layer with
zero entries never triggers the computation at all. I would put it at roughly 70/30
and I would not want to bet a certificate on it.

Findings in this transcript: **7**.
