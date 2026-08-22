# Round 19 — Reader implementer, working transcript

**Disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in five `Read` calls covering lines 1–4365 (the whole document). I opened nothing
in `docs/`, `conformance/`, `spec/registry.json`, `PLAN.md`, `AGENTS.md`,
`README.md`, or any ADR; I ran no `git` command; I issued no web search or fetch;
I listed no directory. I ran local Python that reads only files I wrote myself
(a CRC-32C implementation, a file builder, a reader) plus one `grep`/`python3`
pass over `spec/tarn.md` itself for identifier bookkeeping. Scratch files I
created and read: `crc.py`, `t2.py`, `build.py`, `reader.py`, `test.tarn`, all
under this session's scratchpad. I did not read the round-19 output directory.

---

## 0. Method

I wrote the reader in the order I would actually write the code: CRC primitive →
trailer → directory → record walk → layer record parse → index chain → entry
classification → payload → decode → extract. I built a real 576-byte TARN file
from the document alone, then ran the reader against it and against the
Appendix A file. Where the document told me something I could check
arithmetically, I checked it. Where it did not tell me what to do, I stopped and
wrote it down.

---

## 1. The CRC primitive (§4.5)

`[R-ENC-09]` gives CRC-32C with the Castagnoli polynomial 0x1EDC6F41, reflected
in and out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF, stored little-endian. I
implemented it with the reflected constant 0x82F63B78 and checked §4.5's check
vector:

```
CRC-32C("123456789") = 0xE3069283   ✓ (spec: 0xE3069283, stored 83 92 06 E3)
CRC-32C(<zero bytes>) = 0x00000000  ✓
```

This is the single most load-bearing constant in the document and it is right.
Everything below depends on it.

## 2. The open path, byte by byte

### 2.1 What a cold remote open costs

§19.1 orders the open by dependency, §6.4 prices it. My implementation:

**Request 1 — suffix range `bytes=-64`.** 64 bytes. What bounds this range
before I have read anything: the constant 64 (§6.2's fixed trailer size, made
permanent across every format major by `[R-CNT-24]`: "the final 64 bytes of a
file contain the trailer magic at F − 64 … and a CRC-32C at F − 4"). This is the
only range in the format whose length is knowable a priori. The response also
carries the transport-authoritative F (`[R-CNT-10]`), so §19.1 steps 1 and 2
cost one request between them.

Before the fetch I check `[R-CNT-27]`: if the transport size is below 128, F5,
reject-file, no request at all.

Validation in §6.2's fixed order:

1. trailer magic `8A 4E 52 41 54 0D 0A 1A` (F8)
2. trailer CRC over bytes [0,60) against the u32 at [60,64) (F14)
3. version gate (F18 for 0; `[R-CNT-07]` capability refusal for any other
   unimplemented major; version_minor never gates)
4. then, gates passed: flag gates (F19); committed_file_length == transport size
   (F17) and ≡ 0 mod 64 (F13); dir_offset ≥ 16 (F9); dir_length ≥ 4 (F16);
   dir_offset + dir_length ≤ F − 64 (F10); 1 ≤ generation ≤ 2⁶³−1 (F11, F2);
   file_id ≠ 0 (F12); reserved [56,60) zero (F15). Plus `[R-ENC-03]`/`[R-ENC-04]`
   on the u64 fields and the sum (F2, F3).

The ordering matters and is stated: comparing the magic against a constant is
not "acting on" it (`[R-ENC-10]` says so explicitly, and §6.2 is the "explicit
validation order" that rule defers to), so checking the magic before the CRC is
sanctioned rather than a violation of the verify-before-use chain.

**Request 2 — `bytes=dir_offset..dir_offset+dir_length−1`.** dir_length bytes.
What bounds it: dir_offset ≥ 16 and dir_offset + dir_length ≤ F − 64, both
verified in step 4 above, both under a CRC that has already verified. So the
directory fetch is bounded by F, which is transport-authoritative — this is
exactly `[R-SEC-02]`'s "never in proportion to a declared magnitude it has not
corroborated against the file's actual length".

**Totals.**

| file | requests | ranges | bytes |
|---|---|---|---|
| Appendix A (128 B) | 2 | [64,128), [16,20) | 68 |
| my test file (576 B) | 2 | [512,576), [356,465) | 173 |

No third request is needed at open: §19.1 step 4 is a walk over bytes already
resident, and `[R-RDR-01]` says so ("It consumes the trailer and directory only
— no extent slot's content, no tile index, no payload"). I confirmed my reader
issued exactly two fetches before the layer table was built.

The speculative-window variant: one request for a suffix window; if the buffer
contains [dir_offset, dir_offset+dir_length) the second request is unnecessary
(`[R-CNT-09]`). Appendix A works this through for a 112-byte window covering
[16,128) — the directory is contained, so one request suffices, and bytes [0,16)
stay non-resident, so `[R-CNT-04]`'s front-block obligation does not fire. That
worked example is correct and is the cleanest statement in the document of the
residency-not-transport test.

### 2.2 Appendix A, walked byte-exact

I fed Appendix A's hex dump into my reader:

```
len = 128
magic 8a 4e 52 41 54 0d 0a 1a
version_major 1  version_minor 0  flags 0
generation 1  dir_offset 16  dir_length 4
committed_file_length 128  file_id 0x0123456789ABCDEF
reserved 00000000
computed trailer CRC over [0,60) = 0xE00938D2   stored 0xE00938D2   ✓
directory [16,20) = 00 00 00 00 = CRC-32C of zero bytes = 0x00000000 ✓
```

Every stated value in Appendix A's annotation table is correct, including the
trailer CRC, which is the one value in that appendix that could plausibly have
rotted. F = 128, F mod 64 = 0, dir_offset + dir_length = 20 ≤ F − 64 = 64. The
layer table is empty. §21.6 records zero layers as conforming.

### 2.3 The record walk (§19.1 step 4)

Record sequence is [dir_offset, dir_offset + dir_length − 4) — §7.1 fixes the
terminal 4 bytes as the CRC and F29 spells the bound out. Parse loop: 24-byte
header, then inline_length bytes. Residue or overrun → F29.

Per record: type 0 → F24. Type 0x0002 top-level → the three framing checks
`[R-CNT-25]`/`[R-MTA-03]` place at open (no (0,0) slot F21, extent_length ≥ 5
F22, inline_length exactly 1 F23) plus at-most-one F34. Unknown type with MU=1 →
reject-file; MU=0 → ignore. Type 0x0001 → extract the name and build the
namespace.

The name-extraction rule in step 4 is careful and I needed all of it:
uniqueness is decided **first**, over **raw bytes**, **whether or not each name
is well-formed**, and a record whose name field does not lie inside its
inline_length **contributes no name** and is instead reject-layer. So two layers
with byte-identical ill-formed names are F4 (reject-file), not two L3s. I
implemented exactly that ordering. This is the sort of thing that would
otherwise have been a finding; it is nailed down.

## 3. Validation timing by tier

`[R-RDR-02]` fixes the **latest** point; earlier is always licensed
(`[R-CNF-12]`). What I built:

| tier | checked | register rows |
|---|---|---|
| **open** | front block *if resident*; trailer; directory CRC; record framing; top-level record extent slots (non-layer); top-level user-metadata framing and encoding byte; multiplicity; layer-name namespace | F1–F6, F8–F24, F29–F32, F34, F35; L3, L5, L6; R1 (top-level) |
| **layer access** | the whole §19.3 list — extent slot, §7.4 constraint set, exact parse, sub-record walk and multiplicity, dim/channel names, sub-record user-metadata framing, value domains, six value sets, fill constraints, lz4 cap, geometry floor and arithmetic, `[R-CNT-17]` cross-checks. **No I/O.** | L1, L2, L4, L7–L17, L19–L36, L39, L43–L45; R1 (sub-record) |
| **tile use** | index chain (crc_of_crc_array, segment CRC), entry classification, payload CRC, decode, decoded size | L37, L38; T1, T3, T6–T25 |
| **extent use** | the extent's terminal CRC and the document rules §18.2 attaches at an **assigned** encoding | R2–R10 |
| **never (reader)** | everything whose Detector is *verifier* | F7, F25–F28, F33, F36; L18, L40–L42, L46–L49; T2, T4, T5, T26 |

I confirmed mechanically that every one of the 121 rows carries a
Detector/Detected pair drawn from exactly that vocabulary and that no
verifier row carries a reader tier and vice versa. No anomalies.

I also confirmed the two deliberate cross-tier cases: L3/L5/L6 are layer-scope
rows detected at **open** (the name is parsed at open, so its well-formedness is
too), and L37/L38 are layer-scope rows detected at **tile use** — §19.2 states
that second case explicitly ("index-chain failures take layer scope … although
their detection point is tile use"). Both are consistent; I would have flagged
either as a defect if the register had not been reconciled with §19.2.

§19's preamble is doing real work and I leaned on it twice: the step lists in
§19.1/§19.3/§19.4 are *not* the inventory — §21 is — and `[R-CNF-04]` binds a
reader to every reader-detected row at the tier its *Detected* cell names. Two
examples where the step list alone would have under-specified me: R1's encoding
byte value is not named in §19.1 step 4 but is due at open; T14's codec-1 length
equality is not a numbered step of §19.4 but is due at tile use.

## 4. The layer record parse (§7.4, §19.3)

Packed, no alignment, table order. I wrote the parse as a cursor with a
bounds-checked `take(n)`; every overrun is L23. Fields:

```
name(u8+bytes) layout(u8) linearization(u16) codec(u16) filter(u16)
A(u64) S(u64) A_slab(u64) rank d(u8) C(u16)
d × [ name(u8+bytes) extent(u64) tile_extent(u64) ]
C × [ name(u8+bytes) type(u16) fill(u8 len + bytes) ]
index_encoding(u8) entry_count(u64) crc_of_crc_array(u32)
sub-records to the end of the inline payload
```

I re-derived §7.4's worked example independently:

```
name 4 + nine scalars 34 (1+2+2+2+8+8+8+1+2) + dim entry 18 + channel entry 12
   + trailing fixed 13 (1+8+4) = 81   ✓ matches the stated inline_length
extent_length = 4×20 + ⌈4/2¹⁶⌉×4 = 84 ✓
index region = 4 sentinel entries (80 B); CRC-32C over them = 0x80A34955,
   stored 55 49 A3 80                                          ✓ as stated
crc_of_crc_array = CRC-32C(55 49 A3 80) = 0xC4EE982E            ✓ as stated
```

Both of those CRCs are correct. So is §15.4's all-sentinel constant: I computed
CRC-32C over 2¹⁶ copies of `FF×16 00×4` = **0xEECB3BB2** ✓.

Fill length cross-check (`[R-CNT-23]`): the element-size table §12.1 gives
{1:1, 2:1, 3:2, 4:4, 5:8, 6:1, 7:2, 8:4, 9:8, 10:2, 11:2, 12:4, 13:8}. A fill
whose prefix differs from the element size is L30, in either direction. bool
fill restricted to 0x00/0x01 (L35). This is the one place where a field parses
without type knowledge and validates with it, and it works: the u8 prefix tells
me how far to advance regardless of whether I recognise the type value.

Geometry: Gᵢ = Eᵢ/Tᵢ + (1 if Eᵢ mod Tᵢ else 0) — the document is explicit that
the `(E+T−1)/T` idiom is barred because the intermediate sum can leave the
declared domain. N = ∏Gᵢ, P = ∏Tᵢ, addressed = N (interleaved) or C·N (planar).
`[R-CNT-17]`'s two cross-checks (entry_count vs addressed → L21; extent_length
vs the formula → L22) are both computable with no I/O, which is what makes
§19.3's "layer access performs no fetch" true. My reader asserts it and it held.

I checked §11.2's and §11.4's examples: (1024,2048)/(256,256) → G=(4,8), N=32,
P=65,536 ✓; (1000,2048) → G_y still 4 ✓; coordinate (300,700) → tile (1,2),
s = 1·8+2 = 10, in-tile (44,188), in-tile ordinal 44·256+188 = 11,452 ✓; planar
C=4 channel 2 → disk ordinal 2·32+10 = 74, entry at region bytes [1480,1500) ✓;
channel 3's tiles at ordinals 96–127 ✓. All correct.

## 5. The tile-read algorithm, run for real

I built a file from the document alone:

```
front  [0,16)
tile 0 [16,144)     128 B, 32 float32 values 0.0 … 31.0
tile 1 [144,272)    128 B, 32 float32 values 100.0 … 131.0
index  [272,356)    84 B = 4 entries × 20 + 1 segment CRC × 4
dir    [356,465)    109 B = one layer record (24 + 81) + 4 B CRC
pad    [465,512)    slack, zeroed
trail  [512,576)    F = 576, F mod 64 = 0
```

Layer `sst`: rank 1, dim `x` E=100 T=32, interleaved, one float32 channel `temp`
with fill 0x7FC00000, codec 1, filter 1, A=S=A_slab=0, entry_count 4, entries 0
and 1 stored, 2 and 3 sentinel. G=[4], N=4, P=32, Q=4, decoded size P·Q = 128.

Reads, each with the I/O it actually issued:

```
x =  40 → stored 0x42D80000 (= 108.0)   [352,356) 4 B ; [272,352) 80 B ; [144,272) 128 B
x =  95 → fill   0x7FC00000             [352,356) 4 B ; [272,352) 80 B
x =  96 → fill   0x7FC00000             [352,356) 4 B ; [272,352) 80 B
x =   0 → stored 0x00000000 (= 0.0)     [352,356) 4 B ; [272,352) 80 B ; [16,144) 128 B
x = 100 → request fails as a request, no verdict on the file   (no I/O)
```

x=40 → t₀ = 1, u₀ = 8, s = 1, disk ordinal 1; interleaved with C=1 so value k is
channel 0 at in-tile ordinal k; byte offset u₀·Q + F₀ = 32; bytes [32,36) of the
decoded image = 108.0. The value is right, which means the whole chain —
linearization, in-tile ordinal, sample stride, in-sample offset — is right.

x=96..99 are real positions of tile 3; 100..127 are padding positions of the
same tile. Tile 3 is a sentinel, so all four real positions read as fill and the
padding question never arises. Had tile 3 been stored, `[R-SER-05]` would fix its
padding bytes to `00 00 C0 7F` and `[R-GEO-04]` would forbid me from returning
them; only a verifier checks that content.

x=100 is outside the extents: **the request fails as a request, with no verdict
on the file** (`[R-MDL-01]`, §19.4 step 1). Note the deliberate asymmetry the
document pins down: the same position asked for as a degenerate *region*
request succeeds and returns no samples, because §19.4 defines "a range whose
every interval holds a single position is a region request". That sentence exists
precisely to stop an implementer guessing, and it works.

**Cold open + one tile: 5 requests, 385 bytes** (64 + 109 + 4 + 80 + 128). The
CRC array and the segment could be coalesced into one 84-byte fetch of the whole
region, giving 4 requests / 385 bytes; `[R-IDX-04]` licenses fetching them in
parallel and §15.4's note licenses caching both verifications.

### 5.1 The index chain as I implemented it

Ranges computable from the layer record alone, as `[R-IDX-04]` promises:

```
CRC array : [extent_offset + entry_count·20, extent_offset + extent_length)
segment j : [extent_offset + j·2¹⁶·20, extent_offset + min((j+1)·2¹⁶, entry_count)·20)
entry k   : segment k div 2¹⁶, at segment-relative byte (k mod 2¹⁶)·20
```

Verify crc_of_crc_array over the whole array (L37), then the segment CRC over
the fetched segment (L38) — dependency order, parallel fetch allowed. I checked
§15.4's worked example: entry_count 1,000,000 → 16 segments (15 full,
last = 1,000,000 − 983,040 = 16,960 entries), 64-byte CRC array, region
20,000,064 bytes; k = 999,999 sits in segment 15 at segment-relative byte
20 × 16,959 = 339,180; segment 15 is region bytes [19,660,800, 20,000,000) =
339,200 bytes; a full segment is 65,536 × 20 = 1,310,720 = 1.25 MiB. Every
figure checks.

### 5.2 Entry classification (§15.3)

Six *structural* rows, and I counted six in the table — the preamble's claim is
accurate. My classifier, in order:

```
S = 2⁶⁴−1
off==S ∧ len==S ∧ crc==0     → valid sentinel, reads as fill, no payload I/O
off==S ∧ len==S ∧ crc!=0     → T6  structural reject-tile
(off==S) xor (len==S)        → T7  structural reject-tile
len==0                       → T10 structural reject-tile
off < 16                     → T8  structural reject-tile
off ≥ 2⁶³ ∨ len ≥ 2⁶³        → T11 structural reject-tile
off+len ≥ 2⁶³                → T12 structural reject-tile
off+len > F−64               → T9  structural reject-tile
codec==1 ∧ len != decoded    → T14 reject-tile (no payload fetch needed)
payload crc mismatch         → T1  reject-tile (entry well-formed, extent stands)
```

The sentinel carve-out in `[R-IDX-02]` is essential and stated: `[R-ENC-03]` and
`[R-ENC-04]` apply "to the fields of non-sentinel entries only", so the all-ones
sentinel does not trip the domain check. A zeroed region parses as off=0/len=0 →
T10, loudly invalid rather than silently all-sparse. An all-0xFF region parses as
sentinel-with-crc≠0 → T6. Both failure modes are as the rationale claims.

The structural/well-formed distinction is load-bearing three ways and the
document keeps it straight in all three: a structurally-rejected entry
contributes no extent to the verifier rows, none to `[R-LIF-08]`'s coverage walk
(its bytes fall to slack), and is transparent to `[R-SLB-03]`'s run continuity;
an entry whose only defect is a failed payload crc is none of those things — its
extent stands. I did not have to guess here.

### 5.3 Decode and the decoded byte layout

`[R-COD-01]`: writer does filter then codec; reader does codec then filter⁻¹.
§19.4 step 6 restates it in the same order. `[R-SER-07]`: the decoded payload's
length must be exactly the declaration-derived decoded size — never taken from
payload content, never from a codec's embedded size field (`[R-COD-06]` bars
allocating from Frame_Content_Size explicitly).

The three layouts I implemented:

```
interleaved            size P·Q            value k at (k div C)·Q + F_{k mod C}
planar, numeric ch. c  size P·Bᶜ           value k at k·Bᶜ
planar, bool           size ⌈P/8⌉          value k at bit (k mod 8) of byte (k div 8), LSB-first
```

with Q = ΣBᵢ and Fᶜ = Σ_{j<c} Bⱼ. I checked every worked example in §14.2/§14.3:
(2,3) tile with uint8+uint16 → Q=3, size 18, ordinal 5 at [15,18) ✓; planar `b`
plane 12 bytes, ordinal 5 at [10,12) ✓; float32+bool interleaved → Q=5, size 30,
ordinal 5 at [25,30) with the bool byte at 29 ✓; planar bool P=10 alternating
→ `55 01` with fill false, `55 FD` with fill true ✓ (0xFD = bits 0 set, 1 clear,
2–7 set = the six pad bits carrying fill true). §14.5's (5,5)/(4,4) edge tile:
grid 2×2, corner tile has one real position and 15 padding positions, 32 bytes
of uint16, values 1–15 each `CD AB` ✓.

Byte-shuffle (`[R-COD-10]`): stride s = Bᶜ planar / Q interleaved / 1 for a
packed bool plane (identity). Forward puts byte i of group j at i·n + j with
n = L/s; inverse restores i·n+j to j·s+i. I re-derived §17.3's example — three
float32 1.0/2.0/3.0, s=4, n=3 — and got
`00 00 00 00 00 00 80 00 40 3F 40 40`, byte for byte what the document states ✓.

The two definitions of s for a planar bool plane agree (bool's element size is 1
and the packed-plane rule says 1), so there is no conflict to resolve.

## 6. Degradation walks

Traced end to end. For each: what the reader does, and what it may still serve.

**(a) Unknown top-level record type, MU = 1, experimental range.**
`[R-CNT-15]` → reject-file. Serves **nothing** (§2.4: "A reader MUST NOT rely on
any structure in it"). But the file is **conforming** — §21.6's closing paragraph
and `[R-CNF-02]` make §10.3's prohibition bind the writer's conduct, not the
bytes — so this is a capability refusal, and `[R-CNF-03]`'s acceptance duty is
carved out for exactly it. The diagnostic must not say "corrupt". A verifier
reports *cannot establish*, never *nonconforming*.

**(b) The same type as a layer sub-record.** `[R-CNT-18]` → reject-**layer**,
"never reject-file". Serves every other layer, and may still list the rejected
layer's name (§2.4). File still conforming. I had to assemble this from
`[R-CNT-18]` + `[R-CNF-03]` + `[R-CNF-11]` rather than from §21.6, whose closing
paragraph is phrased around the file-scope case, but no guess was needed.

**(c) Unknown codec value 0x8001 on one layer.** `[R-COD-03]` → validity error at
layer scope, detected at first access (§19.3), **not at open** — so a reader that
never touches that layer serves the file happily and conformingly (§19.2's last
sentence). Other layers unaffected. Note the asymmetry with (a): a codec value is
a layer-scope enum, an MU=1 record type is a file-scope capability.

**(d) Truncated tail / torn commit.** The physical tail is not a trailer → F8 at
the magic check. `[R-LIF-05]`: report torn **and MUST NOT scan backward**. Serves
nothing. The recoverable state is reachable only by §9.6's deliberate probe,
which is explicitly not a reader behaviour and whose output must be re-verified
whole. The subtle sub-case is covered too: if the physical tail happens to be a
payload byte-string that passes every trailer gate, §6.2's note says it dies at
the directory CRC (F20), so detection is never silent.

**(e) Stored-tile checksum mismatch.** T1 → reject-tile. That tile's read reports
failure; **fill is never a fallback** (`[R-CNF-09]`, `[R-TYP-09]`). Neighbours in
the same layer are unaffected. In a region read, §19.4 step 8 lets me return the
validating entries' values with a per-entry report, or fail the request whole —
but never stand fill in for the rejected positions.

**(f) Limit exceeded.** A layer declaring entry_count = 2⁴⁰ (above §21.9's 2³²
guarantee): `[R-ERR-04]` lets me decline — at the whole file, or at the narrowest
scope whose declarations exceed what I can serve. The refusal **MUST be reported
as a resource limit and not as a validity error**. Contrast a layer inside every
guarantee: declining that one on resource grounds makes me a nonconforming
reader.

**(g) Format major 2.** Magic ✓, trailer CRC ✓ (both fixed across majors by
`[R-CNT-24]`), then the version gate → reject-file with a diagnostic distinct
from "not a TARN file" and from "corrupt". Note the ordering consequence §21.2
spells out: only F8, F14, and F1/F6's front-block instance reach such a file;
F19's flag check does not, because the version gate precedes the flag gates.

**(h) Ignore-lane flag bit 20 set.** Ignored; file conforming (§6.3, §21.6). An
updater must copy it forward and must not clear it.

**(i) Incompat-lane bit set.** F19 → reject-file. Serves nothing.

**(j) User-metadata encoding 0x80 (experimental).** ignore-record; the file is
**conforming**; a verifier certifies and reports the record it ignored with owning
scope, encoding value, and stored extent length (`[R-MTA-10]`). Encoding 0 and
the reserved range 3–0x7F are different: R1, violations, still ignore-record.
The document is unusually careful to keep those apart and I did not have to guess.

**(k) Ill-formed UTF-8 in a user-metadata key.** R5 → ignore-record, not
reject-layer — `[R-ENC-11]`'s own carve-out defers to `[R-CNT-25]`'s quarantine.
The whole document decodes to nothing usable; the structural data it annotates is
untouched.

## 7. Checks I ran against the document's own arithmetic

Everything below I recomputed; all agree with the text.

- CRC check vector and CRC of zero bytes (§4.5) ✓
- Appendix A's trailer CRC 0xE00938D2 over [0,60) ✓, and every field in its
  annotation table ✓
- §7.4's 0x80A34955 segment CRC and 0xC4EE982E crc_of_crc_array ✓
- §15.4's 0xEECB3BB2 all-sentinel segment constant ✓
- §7.4's 81-byte inline payload decomposition (4 + 34 + 18 + 12 + 13) ✓ and its
  84-byte extent_length ✓
- §11.2, §11.4, §14.2, §14.3, §14.5, §15.4, §16.2, §17.3, §20.3 worked examples ✓
- §5.1's 128-byte floor derivation ✓ and its 44-byte pad ✓
- §21.8's "121 conditions over 273 instances": I counted rows and
  semicolon-separated instance cells mechanically under §21.1's stated rule
  (a cell reading `—` is one instance) and got **exactly 121 / 273**, split
  F 36/58, L 49/116, T 26/55, R 10/44, matching each subsection's stated count ✓
- §21.9's note arithmetic: 2³² entries → 2¹⁶ segments × 4 B = 256 KiB ✓;
  2³⁶ → 4 MiB ✓; 65,536 layers × 200 B ≈ 12.5 MiB ✓
- `[R-VEC-03]`'s "tens of gigabytes": 2³² × 20 = 85.9 GB ✓
- Requirement identifiers: 17 prefixes, no numbering gaps in any prefix
  (`R-SER-04` is present only in its own withdrawal note, as §14.4 says);
  `R-ENC-100` occurs once, in §2.2's own example of above-99 numbering ✓
- Appendix B's 27 constant rows and Appendix C's registry snapshot each agree
  with the sections that define them ✓
- Every register row's Detector/Detected pair is drawn from §19.2's four reader
  tiers or *verifier*/*certification*, with no crossings ✓

I found **no wrong constant, offset, or checksum** anywhere in the document.

---

# Findings

## reader-01 — AMBIGUITY — §23.1, `[R-PRV-01]`

**The "two ways" enumeration of how a commit removes sample data omits
unstoring a tile in place, which §20.3 and §23.2 both treat as a third thing.**

§23.1 states:

> "A commit removes sample data two ways — superseding it, and a shrink that
> de-addresses tiles (§20.3 step 4) — and a dropped ancillary record's extent
> (§20.4) goes the same way; no commit removes a layer at all."

This is a closed enumeration in normative text (§2.1 makes everything outside
§1, Notes/Examples/Rationales and the non-normative appendices normative), and
the sentence after it — "In each case the bytes remain in the file as slack" —
quantifies over its members.

There is a third operation. §20.3 step 4 distinguishes it from superseding in
one breath:

> "with entries for tiles this commit stores or supersedes written to their new
> state, entries for tiles that become unstored written as the sentinel"

A commit that leaves a layer's extents alone, re-emits its index region, and
writes the sentinel over a previously-stored entry removes that tile's sample
data from reachability. It is not a shrink — the tile is still *addressed*, its
grid count is unchanged — and under §20.3's own usage it is not a supersede
either, because nothing was "written to a new state" in its place. §23.2 names
it as a distinct case and cites §23.1 for it:

> "a tile unstored by a later commit leaves its earlier payload in the file as
> slack (§23.1)"

**Permitted readings.** (a) "superseding it" is broad — any commit that makes
previously-live sample bytes non-live — in which case the enumeration is
complete but the "shrink" clause is redundant, since a de-addressing shrink also
makes live bytes non-live. (b) "superseding it" is narrow, as §20.3 step 4 uses
it, in which case unstoring-in-place is a missing third way and §23.2's
back-reference points at a case §23.1 does not enumerate.

**Which I picked and why.** (b). The specification defines *stored* against a
generation (§3.1) and §20.3 step 4 sets "stores or supersedes" against "become
unstored" as disjoint categories in a single clause; reading (a) would make the
newly added shrink clause do no work.

**What an implementer does wrong without it.** A tool author enumerating the
privacy-relevant operations from §23.1 builds a warning for supersedes and for
shrinks and none for the commonest sparse-layer edit — unstoring a tile — and
then reports "tile deleted" for the one case §23.1's list does not name. The
operative requirement does not have the hole (it is scoped "any commit that
makes sample data unreachable"), so the damage is confined to whoever implements
from the enumeration rather than from the MUST NOT.

**Byte-level: no.** `[R-PRV-01]` constrains how a writer or tool *represents* a
commit to its caller. It fixes no byte and no accept/reject verdict; every file
involved is byte-identical under either reading. What already decides the byte
question is `[R-CNT-21]`: whichever way sample data leaves the live state, the
abandoned extent is slack, whose content is unconstrained and covered by no
checksum.

## reader-02 — AMBIGUITY — §20.5, `[R-WRT-06]`; Appendix G item 8

**The version_minor rule for a compactor turns on an antecedent the compactor
cannot evaluate, and its own worked example of the triggering case is one the
text says the compactor never sees.**

§20.5:

> "Where the output carries a feature a later minor defines and this compactor
> does not — on a conforming input a carried ignore-lane bit (§6.3) or an
> unrecognized `tarn.` key in a record it never decoded (§18.3), the two of
> §10.1's four vehicles §21.6 makes conforming, the other two reaching such a
> file only as values this text still registers as reserved-range violations
> (F36, L25, R1) — the output's version_minor SHOULD be at least the input's …
> Otherwise version_minor follows `[R-CNT-26]`'s floor."

I checked the closure argument and it holds: of §10.1's four vehicles, ignore-lane
bits (§21.6, conforming) and `tarn.` keys (§21.6, conforming) can ride in a
conforming input, while new record types are reserved-range values (F36/L25) and
new values in any reserved range are violations under this text (L31, L33, L34,
L36, L43, L45, R1 — I enumerated §10.2's eight spaces and every reserved range
is a violation row). So the two-item enumeration is genuinely closed.

The problem is the second item. The trigger is *an unrecognized `tarn.` key in a
record the compactor never decoded* — and a compactor's verification depth,
fixed by `[R-WRT-09]`, reaches "the open (§19.1), each retained layer's record
(§19.3) and full index chain (`[R-IDX-04]`), and each relocated extent's
checksum", not the decoding of a user-metadata document. The key sits inside a
possibly-zstd-framed JSON document the compactor carries forward verbatim. So in
the very case the rule offers as its example, the compactor cannot determine
whether the antecedent is true, and therefore cannot determine which of the two
branches — SHOULD be ≥ the input's minor, or SHOULD follow `[R-CNT-26]`'s floor
— applies. The branches pull in opposite directions whenever the input's minor
exceeds the floor. §20.5's own stated reason acknowledges only the weaker
problem ("a compactor cannot know which minor version defined a feature it does
not implement"), not that it cannot know *whether* one is present.

**Permitted readings.** (a) The compactor must assume the antecedent whenever it
carries forward any structure it did not fully interpret — in practice, any
user-metadata extent — and so takes max(floor, input minor), which is
`[R-CNT-26]`'s *appender* rule. (b) The compactor takes the floor unless it has
positive evidence of a later-minor feature, i.e. unless it actually carried an
ignore-lane bit; the `tarn.` key case is then acknowledged as unreachable
guidance.

**Which I picked and why.** (a), because the stated harm is one-sided: §20.5
says a lower minor "understates the file's feature floor to tooling", while
`[R-CNT-26]` says a higher minor than needed "costs readers nothing (minors
never gate)". Under uncertainty the asymmetric cost picks max(floor, input).

**What an implementer does wrong without it.** Two compactors given the same
input emit trailers differing in version_minor and hence in the trailer CRC —
which is exactly the divergence Appendix G item 8 concedes but attributes to
"which features the compactor implements", when in the `tarn.` case it is not a
function of what the compactor implements at all, only of what it chose to
assume.

**Byte-level: no.** Both branches are SHOULDs. `[R-CNF-12]` places SHOULD
deviation outside §21's register entirely — "§21's register enumerates MUST-level
conditions only, and a verifier reports a SHOULD deviation as an advisory that
does not bar certification" — so neither choice can make a file nonconforming,
and `[R-CNF-05]` gates emission on file conformance. Independently,
`[R-ENC-16]` makes version_minor the format's only *descriptive* field and
`[R-CNT-07]` forbids a reader to reject on it, so no accept/reject verdict moves.
Cost to an implementer: a coin-flip on one u16 and the trailer CRC over it, and
a documented inability to reproduce another compactor's output.

## reader-03 — CONTRADICTION — Appendix G item 8 vs §20.4, `[R-WRT-08]` table

**Appendix G's concession says a compactor's output is reproducible except for
its trailer; §20.4 licenses a compactor to drop a record, which changes the
directory.**

Appendix G item 8:

> "A compactor's output is therefore reproducible only modulo its trailer:
> `[R-WRT-06]`'s fresh file_id is no function of content, and this item's floor
> turns on which features the compactor implements."

§20.4's persistence table, row MU = 0 / PE = 0:

> "Retain byte-identical, or drop it — its extent becoming slack. … A compactor
> MAY drop it whenever it rewrites the file."

And §20.5 relies on that licence: "less any record §20.4 lets it drop".

The case is reachable in a profile-conforming input. §7.3 registers only two
types and both carry PE = 1, so an MU = 0 / PE = 0 record must be of an
unassigned type; §21.6 records an experimental-range MU = 0 record as a defined
non-violation, so a **conforming** input can carry one, and nothing in Appendix G
forbids it. Two compactors both adopting the profile, given that input: one
drops the record, the other retains it. Their outputs differ in the record
sequence, in dir_length, in the directory CRC, in every subsequent offset, and
in the dropped extent's bytes — none of which is the trailer. The concession is
therefore too generous by exactly one degree of freedom, and it is the one
degree the appendix's own list (items 2 and 8 carve compactors out explicitly)
shows the author was tracking.

I checked the other items for the same problem and they are clean: for a
compactor, items 1, 5, 6, 7, 9 and 10 are properties inherited from the input
rather than choices — a compactor carries stored tile bytes verbatim and cannot
change a layer record's alignment, slab, filter or fill fields, since
`[R-WRT-07]`'s exception list is closed at "re-points extent slots, regenerates
each relocated tile-index region …, and updates the layer-record fields covering
a regenerated region (crc_of_crc_array)" — so a profile-conforming input yields
those items for free. Item 3's emission order and item 4's single generation the
compactor can satisfy directly. The drop licence is the only leak.

**Byte-level: no.** Appendix G is "non-normative" by its own title and says of
itself "It adds no requirement to any actor: a writer ignoring it is fully
conforming", so §2.1 excludes it from normative text and nothing in it can
enlarge or shrink the emittable set. Both outputs — dropped and retained — are
conforming files, which is what already decides it: §20.4's MAY is the
authority and it is unambiguous. What is wrong is only the appendix's claim
about how far its own profile reaches.

## reader-04 — AMBIGUITY — §20.5, `[R-WRT-07]`

**Regeneration of a tile-index region is conditioned on the *region* moving,
when the thing that forces regeneration is the *tiles* moving.**

§20.5:

> "every retained record per §20.4, except that relocation re-points extent
> slots, regenerates each relocated tile-index region (entry offsets new; entry
> lengths, entry crcs, and sentinel entries unchanged; segment CRCs recomputed
> over the entries as re-emitted), and updates the layer-record fields covering
> a regenerated region (crc_of_crc_array)."

and the Example's gloss:

> "every record extent but a relocated tile-index region — itself a record
> extent (§5.2), and the one kind this operation regenerates rather than copies,
> since its entries carry the offsets that moved"

An index region's *entries* must be rewritten exactly when the tiles they
address move. Whether the *region itself* moves is a separate and independent
fact: a compactor packing a file can perfectly well land a layer's index region
at the same absolute offset it occupied in the input while every tile it
addresses has moved. Under the letter of "each **relocated** tile-index region"
that region is not regenerated, and its entries keep offsets that now point into
slack or into another structure. The parenthetical "entry offsets new" has the
mirror-image slack: a stored tile that happens to land at the same offset keeps
its entry offset, so "new" is not literally true either. The sentence couples two
events that are not the same event.

**Permitted readings.** (a) Literal: regenerate exactly those regions whose own
bytes moved. (b) Intended: regenerate every region any of whose entries must
change — i.e. every region belonging to a layer any of whose stored tiles moved.

**Which I picked and why.** (b). `[R-WRT-07]` closes with a MUST — "The output's
reference arrays MUST equal the live generation's bit for bit (`[R-MDL-02]`)" —
which reading (a) can violate: stale entry offsets either fail the entry crc
(T1, reject-tile) or address the wrong bytes, and either way the output's
reference array is not the input's.

**What an implementer does wrong without it.** A compactor written to the letter
skips regeneration in the corner case and emits a file whose layer is
unreadable, with no check in its own pipeline to catch it: `[R-WRT-09]`'s
verification runs over the *input*'s chain before emitting, not over the output.
Whether the corner case is hit is a function of the compactor's own packing
arithmetic, so it is exactly the class of bug that appears once in production and
never in a test.

**Byte-level: no.** Reading (a) produces a nonconforming output, and
`[R-CNF-05]` gates emission on file conformance — "A writer MUST emit only
conforming files" — so the set of byte sequences a conforming compactor may emit
is the same under both readings. `[R-WRT-07]`'s closing MUST already decides the
verdict; only the procedural sentence is loose.

## reader-05 — AMBIGUITY — §23.1, `[R-PRV-01]`

**The erasure prohibition is scoped to "sample data" while the paragraph it
closes also covers a dropped record's extent.**

§23.1:

> "A commit removes sample data two ways — superseding it, and a shrink that
> de-addresses tiles (§20.3 step 4) — and **a dropped ancillary record's extent
> (§20.4) goes the same way**; no commit removes a layer at all. In each case the
> bytes remain in the file as slack (`[R-CNT-21]`), readable by anyone with the
> bytes and a hex editor … Writers and the tools built on them MUST NOT
> represent any commit that makes **sample data** unreachable as erasure of it"

The paragraph deliberately brings the dropped-extent case inside "In each case
the bytes remain in the file as slack", and §20.4 makes the same point from the
other side — "An updater that drops such a record SHOULD report the loss;
unreported, application state disappears with no diagnostic". The MUST NOT that
closes the paragraph then quantifies only over sample data, so a tool that drops
an MU = 0 / PE = 0 record, or that supersedes a user-metadata document by
appending a new extent (§20.3's shape (c): "a new extent is appended and the old
one becomes slack"), is free under the letter of `[R-PRV-01]` to report the
operation to its user as erasure — while the abandoned bytes sit in the file
exactly as a superseded tile's do.

**Permitted readings.** (a) The scope limit is deliberate: only sample data
attracts the honesty requirement, and metadata or ancillary-record removal may
be described as deletion. (b) The MUST NOT is meant to reach everything the
paragraph enumerates, and "sample data" is a residue of the narrower rule this
one was widened from.

**Which I picked and why.** (a), by the letter — a requirement is read as
written, and §2.1's Note says "every requirement names the actor it binds",
which this one does precisely. I record the reading rather than the intent
because a tool author will do the same.

**What an implementer does wrong without it.** A "delete metadata" or "forget
this record" feature ships with an honest-sounding label and leaves the document
— which §23.2 explicitly warns can carry sensitive material: "Writers handling
sensitive material SHOULD treat names and metadata as published content" —
fully recoverable from slack. The gap is in the one section whose entire subject
is that this misrepresentation is the hazard.

**Byte-level: no.** Like reader-01, `[R-PRV-01]` binds a representation made to
a caller, not a byte. Every file is byte-identical under either reading, and
`[R-CNT-21]` already fixes what happens to the bytes: they become slack, whose
content no conformance requirement constrains.

---

## What I could not determine, and did not report as a defect

- Whether a reader's API returns a byte or a language boolean for a bool sample
  is implementation technique, and `[R-TYP-04]`'s "the one case where a reader
  resolves a byte to a value rather than passing it through" settles the only
  case where it could matter. Not a gap.
- §21.7's "witnessed **only** where the affected tiles remain stored *and* the
  change reaches a byte §14 structurally constrains" reads, on a first pass, as
  contradicted by the clauses that follow it ("a change that reaches the decoded
  size instead is witnessed by T3 or T14"). On a second pass the "only" plainly
  attaches to the stored-tiles conjunct and the rest enumerates sufficient
  witnesses. Wording, no consequence; I am recording it here rather than as a
  finding.
- Record flag bits 2–15 and the trailer's incompat lane are reserved but reachable
  by none of §10.1's four growth vehicles. Per the charter, reserved space is not
  a defect, and both behave as designed tripwires (F26/L47, F19).
- §16.2's "each stored tile's offset equals the previous stored tile's offset
  plus its length" has a dangling "its", but only one referent yields a
  well-defined packing relation.

## Confidence

**High** that a reader built from this document alone interoperates. I built one
and it read a file I built from the same document, returning the right bit
patterns for stored positions and the recorded fill for sentinel ones, with the
request accounting §6.4 predicts. Every constant, offset and checksum I could
check is correct — including all four CRC constants, Appendix A's full trailer,
§7.4's 81-byte payload decomposition, and §21.8's 121/273 register arithmetic.
None of my five findings touches the open path, layer access, the index chain,
the codec/filter pipeline, or the decoded byte layout; four of the five sit in
compaction and privacy prose, and none of them changes a byte or a verdict.
