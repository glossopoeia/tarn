# Cleanroom round 9 — Reader implementer transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in full (3,857 lines, in five `Read` calls plus targeted `grep`s against that same
file). I opened no other file in the repository: no `docs/`, no ADRs, no
`PLAN.md`, `AGENTS.md`, `README.md`, no `conformance/`, no `spec/registry.json`,
no git history, no web access, no directory listings.

I ran two local computations that read no repository file:

1. A CRC-32C implementation written from §4.5's parameters alone (reflected
   Castagnoli, poly 0x1EDC6F41 → reflected table constant 0x82F63B78, init
   0xFFFFFFFF, final XOR 0xFFFFFFFF), used to check the document's four stated
   CRC constants.
2. A mechanical count of the §21.2–§21.5 register rows and of the semicolon-
   separated items in their `Instances` cells, to check §21.8's arithmetic. That
   script parsed the spec file itself; it read nothing else.

I wrote this transcript and one scratch script
(`…/97fba2d9-…/scratchpad/crc.py`). I did not read the round9 output directory.

---

## 1. What I built

An implementation walk of a conforming reader, in the order I would actually
write the code:

```
open()            → §19.1 steps 1–4
  layer_table()   → names only, from the directory
access(layer)     → §19.3, full layer-record validation, no I/O
read(layer, coord | region) → §19.4 steps 1–8
```

Below, each stage, then the degradation walks, then a worked example against
Appendix A and against a layer I constructed myself.

---

## 2. The open path, byte by byte

### 2.1 Step 1 — establish F

`[R-CNT-10]` demands a *transport-authoritative* size: "a full-response content
length, the complete length of a range response, or a size probe", and
explicitly forbids substituting the trailer's own `committed_file_length`. That
is the right rule and it is unambiguous: my remote reader takes F from the
`Content-Range` total of the suffix response, and falls back (SHOULD) to a HEAD
probe plus an absolute range where suffix ranges are unsupported. A 200 response
to a range request must be handled deliberately — I abort it.

The front-block obligation (`[R-CNT-04]`) attaches here. See finding
**reader-04**: I had to guess what "resident" means for a local reader that
`pread`s only the tail. I picked the literal reading — residency is about bytes
the reader actually holds — because §6.1 says twice that "The test is residency,
not transport" and that it is "decidable at any reader's own open path". But the
gloss in the same sentence lists "a local file" as a residency case, and a
`pread`-only local open does not leave [0,16) resident. Under the other reading,
my reader is nonconforming for skipping F8.

### 2.2 Step 2 — the trailer

One suffix range of exactly 64 bytes. What bounds it *before* I have read
anything: the constant 64, permanently fixed by `[R-CNT-24]` ("the final 64
bytes of a file contain the trailer magic at F − 64, version_major and
version_minor at F − 56, and a CRC-32C at F − 4 … A future major MAY redefine
only the remaining 48 trailer bytes and MUST NOT grow the trailer"). This is the
one range in the whole format whose size is knowable with zero prior
information, and it is what makes the open cost independent of file size.

Validation order (§6.2, `[R-CNT-06]`) is *stated*, which matters because
`[R-ENC-10]` otherwise forbids acting on a field before its checksum verifies,
and the magic is compared before the CRC is computed. §6.2 resolves this
cleanly: "comparing a field against a constant for validation is not acting on
it, and an explicit validation order (§6.2) governs where one is stated." So:

1. magic == `8A 4E 52 41 54 0D 0A 1A`  (else F10, reject-file)
2. CRC-32C(trailer[0,60)) == u32 at [60,64)  (else F16)
3. version gate: version_major ≠ 0 (F20) and is a major I implement
   (`[R-CNT-07]`; a *refusal*, not a finding — §21.6)
4. flag gates: no incompat bit 0–15 set (F21); ignore lane 16–31 ignored
5. committed_file_length == F and F mod 64 == 0 (F19, F15)
6. dir_offset ≥ 16 (F11); dir_length ≥ 4 (F18); dir_offset + dir_length ≤ F − 64
   (F12); 1 ≤ generation ≤ 2⁶³−1 (F13, F3); file_id ≠ 0 (F14); reserved
   [56,60) all zero (F17)
7. F ≥ 128 (F7, `[R-CNT-27]`)

Note that steps 1–3 are the only ones touching fields whose *positions* are
fixed across all majors; the document is explicit about that and it is exactly
what a forward-compatible implementation needs.

### 2.3 Step 3 — the directory

One range: `[dir_offset, dir_offset + dir_length)`. Bounded before reading by
two trailer fields that are now CRC-verified, so `[R-ENC-05]` ("MUST NOT
allocate, seek, or issue I/O based on any integer obtained from a file before
the checksum covering it has been verified") is satisfied. Verify the terminal
CRC over the first `dir_length − 4` bytes before any other use (`[R-CNT-11]`,
F22). The directory is always raw — no codec on the open path (§7.1). Good: the
open path needs no decompressor at all.

### 2.4 Step 4 — the record walk

Parse 24-byte headers + `inline_length` inline payloads, no residue. At this
tier I do:

- type 0 → reject-file (F26)
- header or payload past the sequence end, or residue → reject-file (F31)
- unknown top-level type: MU=1 → reject-file; MU=0 → ignore-record (`[R-CNT-15]`)
- multiplicity: ≤1 top-level user-metadata record (F36)
- extent-slot rules for **non-layer** top-level records only (F32/F33/F34) —
  §19.1 is careful to scope this, because a layer record's slot is layer-scope
  and belongs to the layer-access tier (L16–L18)
- for a top-level user-metadata record: slot ≠ (0,0) (F23), extent_length ≥ 5
  (F24), inline_length == 1 (F25)
- build the layer-name namespace

The namespace rule is the sharpest piece of new-looking text in §19.1 and I
found it fully determinate. Uniqueness is decided **first**, over **raw name
bytes**, "whether or not each name is itself well-formed", and a record whose
name field does not fit inside its `inline_length` "contributes no name to the
namespace and is instead a validity error at layer scope". F6's Instances cell
matches word for word ("both obtainable within their records' inline_length").
Two layers with byte-identical ill-formed names → reject-file (F6), not two
reject-layers. I implemented it exactly that way and had nothing to guess.

Encoding-byte validity for a top-level user-metadata record: §19.1 step 4 does
*not* list it, but §19's preamble defers the inventory to the register, and R1's
Detected cell reads "open (top-level); layer access (sub-record)". So my open
checks the encoding byte and reports ignore-record when it is 0 or 3–0x7F, even
if the caller never asks for metadata. That is a behavioural obligation I would
have missed reading §19.1 alone; §19's preamble is what makes it findable.

### 2.5 Byte-exact cost of a cold remote open

Against a server that honours ranged requests:

| # | Range | Bytes | What bounds it before I read it |
|---|---|---|---|
| 1 | suffix, last 64 | 64 | the constant 64, fixed permanently by `[R-CNT-24]` |
| 2 | `[dir_offset, dir_offset+dir_length)` | `dir_length` | trailer fields, CRC-verified in step 2 |

**Total: 2 requests, 64 + dir_length bytes.** Nothing else is fetched — no
extent, no index, no payload (`[R-RDR-01]`). `dir_length` is guaranteed
acceptable up to 16 MiB (§21.9); writers SHOULD keep trailer + pad + directory
inside 65,536 bytes (`[R-CNT-09]`) so a single 64 KiB suffix speculation
collapses this to **1 request**.

For Appendix A's 128-byte file: **2 requests, 68 bytes** (64 + 4), or 1 request
of 128 bytes speculatively — in which case [0,16) becomes resident and
`[R-CNT-04]` then *requires* the front-block equality check. Appendix A states
exactly this, including the intermediate case of a 112-byte window covering
[16,128) that contains the directory but leaves the front block non-resident. I
checked the arithmetic: 128 − 16 = 112. Correct.

First cold tile read adds up to three more requests: the segment-CRC array
(⌈entry_count/2¹⁶⌉ × 4 bytes), the covering segment (≤ 65,536 × 20 =
1,310,720 = 1.25 MiB), and the payload (`length` from the entry). The array and
segment ranges are computable from the layer record alone and MAY go in
parallel (`[R-IDX-04]`), so the wall-clock cost is 2 round trips, not 3.

---

## 3. Validation timing by tier

`[R-RDR-02]` fixes the *latest* detection point; earlier is always licensed
(`[R-CNF-12]`). My tiers:

| Tier | What I check | Example rows |
|---|---|---|
| open | front block (if resident), trailer, directory CRC, record walk, layer-name namespace, top-level UM framing + encoding byte | F1–F38, L4, L6, L7, R1(top) |
| layer access | the whole layer record: slot, §7.4 constraint set, exact parse, sub-records, dim/channel names, value sets, fill constraints, geometry floor + products, index cross-checks | L1–L37, L40, L44–L46 |
| tile use | crc_of_crc_array, segment CRC, entry classification, payload CRC, codec/filter, decoded size | L38, L39, T1, T3, T6–T25 |
| extent use | user-metadata extent CRC and document content rules | R2–R10 |
| never | every row whose Detector is *verifier* | F9, F27–F30, F35, F38, L19, L26, L41–L43, L47–L50, T2, T4, T5, T26 |

Two things I want to record because they were not obvious:

- **Index-chain failures are detected at tile use but take layer scope.**
  §19.2 says so explicitly ("in particular, index-chain failures take layer
  scope (`[R-IDX-04]`) although their detection point is tile use"), and §19.4
  step 8 says the bar is *prospective*: values already returned stand. That
  combination is unusual and I would have got it wrong without the explicit
  statement.
- **A verifier-detected row imposes no reader obligation at all**, even though
  §21.3's and §21.4's headers say "the named layer is unusable" / "that tile's
  read reports failure". §21.1 resolves it: "For a row whose Detector is
  *verifier*, the outcome names the scope at which the damage is recorded, not
  an obligation on any reader … for several such rows it obliges the reader to
  serve the structure unchanged". So my reader serves a layer with L41's
  alignment violation and a tile with T4's bad padding, unchanged. `[R-CNF-09]`
  is scoped to match ("whose rejection this reader is obliged to detect").
  This is one of the places I re-read three times; it is correct as written.

What a reader is permitted **never** to check: coverage/overlap (§9.7, §7.2),
alignment and slab invariants (§16), decoded-content obligations (§14.5,
`[R-SER-08]`), record flag hygiene (`[R-CNT-12]`, `[R-CNT-22]`), reserved-range
type values (F38/L26), user-metadata member ordering (`[R-MTA-05]`), and the
pre-trailer-gap rule (`[R-CNT-05]`). Appendix H's verifier checklist enumerates
exactly this set; I cross-checked it row by row against every *verifier* row in
§21.2–§21.5 and it is complete.

---

## 4. Layer access

No I/O at all (`[R-RDR-03]`: "All are decidable from the resident directory and
F"). That is a strong and useful property: my `open()` + `access()` never
touches a byte outside the trailer and directory.

The parse of §7.4's inline payload, packed with no alignment:

```
u8 name_len, name[name_len]
u8 layout            1|2
u16 linearization    1
u16 codec            1..4
u16 filter           1|2
u64 A                0 | pow2 in [512, 2^62]
u64 S                0 | [1, 2^63-1]
u64 A_slab           0 iff S==0, else pow2 in [1, 2^62]
u8 d                 >= 1
u16 C                >= 1
d  × { u8 nlen, name, u64 E, u64 T }     T >= 1
C  × { u8 nlen, name, u16 type, u8 flen, fill[flen] }
u8 index_encoding    == 1
u64 entry_count
u32 crc_of_crc_array
records...                                to end of inline payload, no residue
```

Cross-checks I compute here, all pure arithmetic:

- `G_i = ceil(E_i / T_i)` computed as `E/T + (E%T ? 1 : 0)` — §11.2 explicitly
  forbids the `(E+T-1)/T` idiom because the sum can leave the declared 0..2⁶³−1
  domain. I used the stated form.
- `N = ∏G_i`, `P = ∏T_i`, `addressed = N` (interleaved) or `C·N` (planar), each
  product overflow-checked against 2⁶³−1 (`[R-ENC-04]`, L2).
- `entry_count == addressed` (L22).
- `extent_length == entry_count*20 + ceil(entry_count/2^16)*4`, and 0 iff
  entry_count == 0 (L23), with slot (0,0) iff entry_count == 0.
- `crc_of_crc_array == 0` when entry_count == 0 (L28).
- fill length == element size of the declared type (L31); bool fill ∈ {0,1}
  (L36).
- `A ≠ 0 && S ≠ 0` → reject-layer (L21).
- codec 4 cap: max over channels of the per-tile decoded size ≤ 0x7E000000
  (L45) — quantified over *addressed* tiles, so a layer with any `E_i = 0`
  passes vacuously. The §17.2 note spells this out and also warns that
  `[R-ENC-04]` carries no such quantifier, so `P·Q` and `P·B` are still checked
  in an empty layer. I implemented both halves.

Zero-extent layers (`[R-GEO-02]`): `G_i = 0` for that axis → `N = 0` →
entry_count 0 → slot (0,0), crc_of_crc_array 0, no index region, reads return
no samples. Consistent everywhere I looked (§11.1 rationale, §15.4's last
example, §21.6's row).

---

## 5. The tile-read algorithm

### 5.1 Ordinals

For coordinate `(x_0 … x_{d-1})`: `t_i = x_i div T_i`, `u_i = x_i mod T_i`.

- spatial tile ordinal `s = Σ t_i · ∏_{j>i} G_j` (linearization 1 only)
- in-tile sample ordinal `k = Σ u_i · ∏_{j>i} T_j` — row-major "for every
  linearization value, permanently", which is a nice invariant to be able to
  hard-code
- disk ordinal = `s` interleaved, `c·N + s` planar (channel-major)

I re-derived §11.4's example: grid (4,8), coord (300,700) → tile (1,2) → s = 10;
in-tile (44,188) → 44·256+188 = 11,452; planar channel 2 → 2·32+10 = 74. All
three match the document. §15.4's follow-on says entry 74 occupies region bytes
[1480,1500) — 74·20 = 1480 ✓ — and that channel 3's entries are 96..127 —
3·32 = 96 ✓.

### 5.2 Index chain

Entry k is at region byte 20k. Segment `s = k div 2^16` covers
`[s·2^16, min((s+1)·2^16, entry_count))`. Verify `crc_of_crc_array` over the
whole fetched CRC array, then the segment CRC over the fetched segment. Both
ranges computable from the layer record alone; both MAY be cached under
committed-prefix immutability (§15.4's note + `[R-LIF-03]`). Any mismatch →
reject-layer (L38/L39). The all-sentinel constant `0xEECB3BB2` "licenses nothing
for readers" — I compare computed CRCs and never match constants.

I verified §15.4's worked example arithmetically:
entry_count 1,000,000 → 16 segments, 15 full (983,040 entries) + 16,960;
CRC array 64 bytes; region 20,000,064 bytes; tile 999,999 → segment 15,
segment-relative entry 16,959 → byte 339,180; segment 15 spans
[19,660,800, 20,000,000) = 339,200 bytes ("~339 KB" ✓); CRC array at
[20,000,000, 20,000,064) ✓; one full segment = 1,310,720 = 1.25 MiB ✓.
Every number in that example is right.

### 5.3 Entry classification (§15.3)

Six *structural* rows (I counted them: sentinel-with-crc≠0; half-sentinel;
length 0; offset < 16; either field > 2⁶³−1; overflow-or-past-F−64), one
crc-failure row that is explicitly **not** structural ("the defect lies in the
bytes it addresses, not in the entry, so its extent stands"), and three
*verifier* rows. The structural/non-structural split is load-bearing in three
other places and I checked all three agree:

- §9.7's coverage walk: a structural entry "contributes no stored extent to the
  walk", a crc-failing one "keeps its extent";
- `[R-SLB-03]`'s run continuity: structural entries are transparent, a
  crc-failing one is not, "so this invariant stays decidable from index bytes
  alone";
- L42's Instances text repeats the same distinction.

Three independent restatements, all consistent. This is exactly the kind of
cross-section propagation that usually breaks; here it does not.

`[R-IDX-02]` also matters: sentinel fields are a reserved pattern, so
`[R-ENC-03]`/`[R-ENC-04]` "apply to the fields of non-sentinel entries only",
and T11's Instances text adds "the value being distinct from the all-ones
sentinel". So an entry with offset = 2⁶⁴−1 and length = 5 is T7 (half-sentinel),
not T11. Determinate.

### 5.4 Decode

Write path: image → filter → codec. Read path: codec-decode → filter-inverse.
§17.1 states both directions explicitly, which removes the single most common
source of interop failure in filtered formats.

Shuffle stride: element size (planar numeric), Q (interleaved), 1 / identity
(packed bool plane). `L` is divisible by `s` in every case — I verified:
planar numeric `L = P·B`, `s = B`; interleaved `L = P·Q`, `s = Q`; bool plane
`s = 1`. Inverse: byte at `i·n + j` goes to `j·s + i`.

I reproduced §17.3's example by hand: float32 1.0,2.0,3.0 →
`00 00 80 3F | 00 00 00 40 | 00 00 40 40`, s=4, n=3 →
`00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40`. Matches the document exactly.

### 5.5 The decoded byte layout I end up with

| Case | Decoded size | Value k at |
|---|---|---|
| interleaved | `P · Q`, Q = ΣB_i | `(k div C)·Q + F_{k mod C}` |
| planar, numeric channel c | `P · B_c` | `k · B_c` |
| planar, bool channel | `⌈P/8⌉` | bit `k mod 8` of byte `k div 8`, LSB-first |

`[R-SER-07]` makes any other decoded length a tile-scope error, and — crucially
for the allocator — decoded size "is a function of the layer's declarations
alone … never of payload content". So my decoder allocates `P·Q` before it
decompresses anything, and a zstd Frame_Content_Size is never an allocation
source (`[R-COD-06]` says so in terms). That is the decompression-bomb defence
and it is airtight.

I re-derived §14.2's examples: interleaved (2,3) with uint8+uint16 → Q=3,
size 18, ordinal 5 at [15,18); planar `b` plane 12 bytes, ordinal 5 at [10,12);
float32+bool interleaved → Q=5, size 30, ordinal 5 at [25,30) with the bool at
byte 29. And §14.3's packed example: P=10, alternating from true →
byte 0 = 0b01010101 = 0x55, byte 1 = bit0 set, bit1 clear, pad bits 2–7 = fill
→ `55 01` (fill false) / `55 FD` (fill true). Both correct.

And §14.5's: extents (5,5), tiles (4,4), edge tile (1,1) covers 4..7 on both
axes = 16 positions of which exactly one (4,4) is real; uint16 fill 0xABCD →
32 bytes, value 0 the sample, values 1..15 each `CD AB`. Correct.

### 5.6 Extract and return

Padding positions are never returned (`[R-GEO-04]`). Bit patterns returned
unaltered (`[R-MDL-02]`, `[R-TYP-04]`) — NaN payloads preserved, −0.0 ≠ +0.0.
The sole byte a reader ever *resolves* rather than passes through is a
nonconforming interleaved bool ≠ {0x00,0x01}, and `[R-SER-08]` fixes it: 0x00
false, everything else true. Appendix H repeats it as "the sole resolved byte",
and §12.3 carves it out of `[R-TYP-04]` by name. Three places agree.

Multi-entry requests: per-entry failure is bounded to that entry's positions;
I MAY return the good entries with a per-entry failure report, or fail whole,
but I MUST NOT substitute fill (`[R-CNF-09]`). Fill has exactly one producer —
"a sentinel entry read from a verified index chain" (`[R-TYP-09]`) — which also
closes a hole I went looking for: a reader that *declines* a tile on resource
grounds under `[R-ERR-04]` cannot return fill either, because `[R-TYP-09]` is
an exhaustive statement of fill's provenance, not a list of prohibitions.

---

## 6. Degradation walks (seven, end to end)

**(1) Unknown top-level record type, MU = 0, experimental range 0x8000.**
Open: parse header, note unknown type, `[R-CNT-15]` → ignore-record. I never
fetch its extent, never parse its inline payload. Everything else is served
normally. §21.6 confirms the file is *conforming*. If it had been a reserved
type 0x0003 with MU = 0, my reader behaves identically (F38 is a verifier row) —
but the file is nonconforming. Reader behaviour is deliberately blind to the
difference; the register makes that explicit.

**(2) Unknown top-level record type, MU = 1.** reject-file (F37 if reserved,
otherwise §21.6's "conforming file a reader nevertheless refuses"). Nothing
served. Diagnostic must distinguish "I cannot" from "your file is broken" —
§21.6's closing paragraph asks for it and Appendix H does not, but nothing
turns on it.

**(3) Unknown *sub*-record type, MU = 1.** `[R-CNT-18]`: reject-layer, "never
reject-file". Other layers keep working; I may still list the rejected layer's
name (§2.4). This override of `[R-CNT-15]`'s file-scope rule is stated in terms
and I had nothing to guess.

**(4) Unknown codec value 7 on layer B.** Layer access → L44 → reject-layer.
Layer A still serves. Note the asymmetry I had to be careful about: an
*assigned* codec I cannot execute makes me a nonconforming reader
(`[R-CNF-03]`), not a rejecting one. `[R-COD-11]` states exactly that: for a
conforming reader the "cannot execute" position "arises only at a reserved or
experimental value".

**(5) Truncated tail.** Physical file shortened by 3 bytes after commit. F is
now F′ = F−3. Bytes [F′−64, F′) are not a trailer → magic fails → F10 →
reject-file, reported as *torn or invalid*, and `[R-LIF-05]` forbids me to scan
backward for the earlier trailer. §9.5's note is explicit that residue past a
completed commit "carries no register row of its own" and is met as F10/F16/F19.
Recovery (§9.6) is a separate tool, not my open path. Extended-tail is
symmetric: committed_file_length ≠ transport size → F19.

**(6) Checksum mismatch, one per link.** trailer → reject-file (F16); directory
→ reject-file (F22); crc_of_crc_array → reject-layer (L38); segment CRC →
reject-layer (L39); tile crc → reject-tile (T1), neighbours unaffected;
user-metadata extent → ignore-record with a SHOULD-report (R2). §8.2 lists all
six outcomes in one sentence and §21 registers each; I found no divergence.

**(7) Limit exceeded.** A layer declaring entry_count = 2³³ (above §21.9's 2³²
guarantee). The file is still *conforming*. I may decline — "at the whole file,
or at the narrowest scope whose declarations exceed what it can serve, a layer
or a tile" — and I MUST report it as a resource limit, not corruption
(`[R-ERR-04]`). I decline the layer and serve the rest. The parallel case for a
zstd Window_Size above 8 MiB is per-tile and §17.2 names tile-or-layer
explicitly, which matters because a frame window is not a "declaration" in the
layer record and `[R-ERR-04]`'s own wording says "declarations".

**(8) Format major 7.** Version gate → reject-file, with a diagnostic distinct
from both "not a TARN file" and "corrupt" (`[R-CNT-07]` SHOULD). §2.3 says the
file "is neither conforming nor nonconforming under" major 1, and a verifier
reports *cannot establish*. This is where finding **reader-03** lives.

---

## 7. Worked example — Appendix A, byte by byte

I re-derived every value in Appendix A's 128-byte file from §6.1/§6.2/§7.1
alone and then checked the stated CRC with my own CRC-32C.

```
[0,8)    89 54 41 52 4E 0D 0A 1A   front magic          — equality (resident) ✓
[8,16)   00 × 8                    front reserved       — equality ✓
[16,20)  00 00 00 00               directory: 0 record bytes + CRC32C("") = 0 ✓
[20,64)  00 × 44                   pre-trailer pad (slack)
[64,72)  8A 4E 52 41 54 0D 0A 1A   trailer magic ✓
[72,74)  01 00                     version_major 1 ✓
[74,76)  00 00                     version_minor 0
[76,80)  00 00 00 00               flags 0 ✓
[80,88)  01 …                      generation 1, in [1, 2^63-1] ✓
[88,96)  10 …                      dir_offset 16, ≥ 16 ✓
[96,104) 04 …                      dir_length 4, ≥ 4 ✓
[104,112)80 …                      committed_file_length 128 = F, 128 % 64 = 0 ✓
[112,120)EF CD AB 89 67 45 23 01   file_id 0x0123456789ABCDEF ≠ 0 ✓
[120,124)00 00 00 00               reserved zero ✓
[124,128)D2 38 09 E0               trailer CRC
```

Gate checks: `dir_offset + dir_length = 20 ≤ F − 64 = 64` ✓; F ≥ 128 ✓.

Independently computed CRC-32C over the 60 constructed trailer bytes:

```
0xE00938D2   → stored little-endian as  D2 38 09 E0
```

**Matches the document exactly.** The other three stated constants also match my
implementation:

| Constant | Document | Computed |
|---|---|---|
| CRC-32C("123456789") | 0xE3069283 | 0xE3069283 ✓ |
| CRC-32C(zero bytes) | 0x00000000 | 0x00000000 ✓ |
| CRC-32C(2¹⁶ sentinel entries) | 0xEECB3BB2 | 0xEECB3BB2 ✓ |
| Appendix A trailer CRC | 0xE00938D2 / `D2 38 09 E0` | 0xE00938D2 ✓ |

That last one is worth noting: it means the annotated file is *actually*
loadable, not merely plausible. I found no wrong constant, offset or checksum
anywhere in the document.

### 7.1 A layer I built myself

To exercise the parts Appendix A cannot, I constructed a layer on paper:
interleaved, d = 2, dims (y: E=5, T=4), (x: E=5, T=4), channels
`a` (uint8, fill 0x00) and `h` (uint16, fill 0xABCD), codec 1, filter 2.

- G = (2,2), N = 4, P = 16, addressed = 4, Q = 1 + 2 = 3, decoded size = 48.
- index region = 4·20 + 1·4 = 84 bytes; crc_of_crc_array over those 4 bytes.
- Tile (1,1): 16 positions, one real (4,4) at in-tile ordinal 0, 15 padding.
  Under `[R-SER-05]` its decoded image is
  `[a_sample][h_sample_lo][h_sample_hi]` then 15 × `00 CD AB`.
- Filter 2 at s = Q = 3, n = 16: the shuffled image is 16 `a` bytes, then 16
  `h` low bytes, then 16 `h` high bytes. Length unchanged, 48.
- Codec 1 ⇒ the entry's `length` MUST equal 48 (`[R-COD-04]`, T14), checkable
  before any payload fetch. I check it there.
- Reading coordinate (4,4): t = (1,1), s = 1·2 + 1 = 3, disk ordinal 3, entry at
  region byte 60, u = (0,0), k = 0, `a` at byte 0, `h` at bytes 1–2.

Every step was determined by the text. The one place I paused was whether the
filter operates on the whole tile including padding positions — `[R-COD-02]`
("Both stages consume and produce whole tiles") settles it.

---

## 8. Register arithmetic (checked mechanically)

I counted the rows and the semicolon-separated `Instances` items exactly as
§21.1 prescribes ("Instances within a cell are separated by semicolons, and a
cell reading — is one instance; the count is therefore mechanical once the cell
is written"):

| Table | Rows | Header claims | Instances |
|---|---|---|---|
| §21.2 file | 38 | 38 ✓ | 60 |
| §21.3 layer | 50 | 50 ✓ | 103 |
| §21.4 tile | 27 | 27 ✓ | 46 |
| §21.5 ignore | 10 | 10 ✓ | 44 |
| **total** | **125** | §21.8: "125 conditions over 253 instances" ✓ | **253** ✓ |

Exact. I then walked every requirement identifier in the document and asked
whether a detectable file-conformance violation of it appears in the register.
I found no omission: every `[R-CNT-*]`, `[R-ENC-*]`, `[R-GEO-*]`, `[R-IDX-*]`,
`[R-SLB-*]`, `[R-TYP-*]`, `[R-SER-*]`, `[R-COD-*]`, `[R-MTA-*]` condition maps
to at least one row, and the ones that do not (`[R-LIF-01]`, `[R-LIF-03]`,
`[R-GEO-06]`, `[R-SER-01]`, `[R-CNT-13]`'s no-embedded-offsets) are named in
§21.7 as witnessless. §21.1's specialization list (F2 of F8/F10, F37 of F38,
L25 of L26) omits T16-of-T24 and T18-of-T24 — a deflate second stream and a
zstd second frame both also leave bytes after the first stream ends — but the
list is introduced with "Some rows", not "all", and detector, tier and outcome
coincide for all three, so nothing forks. Not reported.

§21.9's derivations also check out: 2³² entries ⇒ 2¹⁶ segments ⇒ 256 KiB CRC
array; 2³⁶ ⇒ 4 MiB; 2³² entries ⇒ an 85.9 GB index region, which is why §24
says that guarantee is not constructible as a vector ("tens of gigabytes"). And
the guarantees compose: opening a 65,536-layer file costs ≤ 16 MiB, reading one
tile of a 2³²-tile layer costs 256 KiB + 1.25 MiB + the payload. The design is
coherent at its own stated bounds.

---

## 9. Findings

### reader-01 — CONTRADICTION — Appendix G, items 1–9 vs the closing paragraph

Appendix G's closing paragraph claims the profile supplies four things the core
does not, and names gap *content* first:

> Four things are not, and the items above are where the profile adds them: gap
> *content*, which `[R-CNT-03]` only advises; gap *extent*, which placement
> freedom (`[R-SLB-05]`) leaves open; sub-record order within a layer record's
> inline payload, which `[R-CNT-14]` leaves free; and the fill a writer records
> when its caller chooses none, which `[R-TYP-10]` states as a SHOULD.

I checked each of the four against the nine items. Gap *extent* is item 3 ("Each
structure begins where the previous one ended"). Sub-record order is item 3.
The fill default is item 7. **Gap content is in no item.** Items 1–9 say nothing
about what bytes occupy a gap.

This is not academic, because the profile cannot avoid gaps. `[R-LIF-02]` step 5
requires "the pad to the next 64-byte boundary" between the directory and the
trailer, and §6.2 leaves its content unconstrained: "this specification does not
constrain their content". A directory ends 64-aligned only by luck — the record
sequence must parse "with no residue", so a writer cannot pad it, and it cannot
insert a filler record without emitting an unassigned type. Appendix A's own
minimal file has a 44-byte pad at [20,64). Two writers that both follow items
1–9 exactly, given the same input, therefore emit different 128-byte files —
which is precisely the failure the profile exists to prevent, and precisely the
degree of freedom the closing paragraph says it closed.

Reading I picked: I implement `[R-CNT-03]`'s SHOULD as a MUST when claiming the
profile, i.e. I treat the closing paragraph as the operative statement and item
3 as silently incomplete. An implementer who reads only the nine items, as the
list's imperative framing invites, will not.

Not byte-level: Appendix G is labelled non-normative and states "It adds no
requirement to any actor: a writer ignoring it is fully conforming", so no file's
conformance and no reader's verdict changes. What changes is whether two
independent implementations of the *profile* agree byte for byte, which is the
profile's entire claim.

### reader-02 — AMBIGUITY — Appendix G, item 2

> **`file_id` from a cryptographic hash of the file's own emitted bytes**,
> computed over [0, F − 64) together with the trailer's other fields with the
> `file_id` field taken as zero, then written in. Deterministic, and
> high-entropy

Three things an implementer must invent:

1. **Which hash.** "a cryptographic hash" names no function. Item 1 and item 9
   both close their degrees of freedom by pinning a named implementation at a
   named version ("a named codec implementation at a named version"; "a named
   JSON writer at a named version"). Item 2 does not, and claims determinism
   anyway.
2. **How a digest becomes a `u64`.** First 8 bytes? Last 8? Big- or
   little-endian interpretation? Unstated.
3. **What "the trailer's other fields" are concatenated as.** The trailer CRC
   at [60,64) cannot be an input (it covers [0,60), which contains `file_id`),
   so presumably the input is trailer[0,60) with bytes [48,56) zeroed — but
   that is my inference, and hashing the 60 bytes as laid out versus hashing
   the fields in some other order gives different answers.

There is also an unhandled edge: `[R-CNT-06]` requires `file_id ≠ 0`, and item 2
offers no rule for a digest whose selected 8 bytes are zero. Astronomically
unlikely, but a profile whose point is determinism should say.

The readings I can defend: (a) item 2 is, like items 1 and 9, a
pin-your-producer item and byte-identity across implementations is not claimed
for it; (b) item 2 is meant to be fully determined and merely under-drafted.
I picked (a) and would document my hash choice. But (a) contradicts the
appendix's own boundary statement — "Byte-identity across *implementations* is
therefore unattainable for codecs 2–4; codec 1 is reproducible by anyone" —
which asserts that under codec 1, *anyone* reproduces the file. With item 2
unpinned (and reader-01's gap content unpinned), they do not.

Not byte-level, for the same reason as reader-01: the appendix is non-normative
and adds no conformance requirement.

### reader-03 — CONTRADICTION — §21.2 row F1 vs §21.6 and §21.1

F1 registers, as a file-scope violation with detector *reader* and outcome
reject-file:

> | F1 | A multi-byte field is stored big-endian rather than little-endian,
> detectable only through that field's own value or range gate | trailer
> version_major; dir_offset; dir_length; committed_file_length; generation |
> reader | open | `[R-ENC-01]` (R-CNT-07) |

Two of those five instances have no file-conformance witness.

**`version_major`.** A big-endian `1` is the bytes `00 01`, read as 256. The
resulting file declares format major 256. §2.3 says of such a file: "a file
declaring another major is neither conforming nor nonconforming under it: a
reader refuses such a file on capability grounds (§6.3, `[R-CNT-07]`), and that
refusal is not a finding about its bytes." §21.6's closing paragraph then says
of that exact case:

> Neither is a register row: the register enumerates file-conformance
> violations (§21.1), and a file this document declines to judge is not one.
> What is registered in each case is the neighbouring condition that *is* a
> violation — version_major = 0, permanently invalid in every format major
> version (F20, `[R-CNT-07]`) …

So §21.6 asserts that the only registered `version_major` condition is F20,
while §21.2 registers `version_major` a second time as an instance of F1.

**`generation`.** A big-endian generation `g` is stored as `g · 2⁵⁶`. For
g ≤ 127 that is at most 127 · 2⁵⁶ = 9,151,314,442,816,847,872, which is below
2⁶³ − 1 = 9,223,372,036,854,775,807 and therefore *inside* `[R-CNT-06]`'s stated
range "1 ≤ generation ≤ 2⁶³ − 1". The file passes every gate. §21.7 already
records that the generation sequence has no single-file witness
("`[R-LIF-01]`, `[R-LIF-03]` are properties of a file's history, which §9.7 does
not reconstruct"). So a file exhibiting F1's `generation` instance is a
**conforming file** — sitting in a table headed "Outcome: reject-file" in a
register whose completeness clause is scoped to "every *detectable*
file-conformance violation this specification names".

The consequence an implementer meets is in the corpus, not the reader.
`[R-ERR-02]` requires "one vector per instance" whose "expected verdict is that
row's outcome" (reject-file), and `[R-VEC-02]` requires each vector's manifest
to record "whether the file is **conforming**". Neither is answerable for these
two instances: the `generation` vector would be a conforming file no reader
rejects, and the `version_major` vector is a file this document expressly
declines to judge.

Note this is *not* the ordinary "register row contradicts the rule it cites"
pattern that §21.1's precedence clause disposes of. F1 restates `[R-ENC-01]`
faithfully; the divergence is between F1's *placement* — in a table of
file-conformance violations — and `[R-CNF-02]` and §21.6, neither of which F1
cites, so §21.1's "the rule governs" does not reach it.

Reading I picked: F1's other three instances (dir_offset, dir_length,
committed_file_length) are real and detectable via `[R-CNT-06]`'s gates; the
`version_major` and `generation` instances are cause-notes with no witness and
my reader implements nothing for them. A verifier meeting version_major = 0x0100
reports *cannot establish* per §2.3, not *nonconforming*, because it cannot
establish byte-reversal from bytes that are equally a legitimate major-256
declaration — and §2.3's "An established violation takes priority" therefore
never fires.

Not byte-level, on that last point: once "establish" is read as requiring a
witness, both a verifier following F1 and one following §2.3 land on the same
verdict (*cannot establish* for version_major, *conforming* for a big-endian
small generation), and reader behaviour is identical either way. What breaks is
the constructibility of two of §21.8's 253 vectors and the internal consistency
of §21.1's completeness claim.

### reader-04 — AMBIGUITY — §6.1, the residency test

> A reader whose open leaves bytes [0, 16) **resident** — a local file, a memory
> mapping, a speculative suffix window that reached offset 0, or any transport
> already holding them — and a content sniffer MUST verify the full block by
> byte equality before other processing, and MUST treat any mismatch as
> reject-file. A reader that would have to issue a further range request to
> obtain those bytes MAY defer or omit the check

My reader on a local filesystem uses `pread` for the trailer and `pread` for the
directory. It never touches [0,16). Is it obliged to check the front block?

- **Reading (a), literal residency.** The obligation binds only a reader that
  actually holds the bytes. Mine does not, so it may omit the check. Support:
  the paragraph above says the obligation "turns on residency instead" of the
  local/remote distinction "because … residency is decidable at any reader's own
  open path", and the closing sentence repeats "The test is residency, not
  transport, so an implementation decides it at its own open path". F8's
  Instances text is the same shape: "the obligation binds a reader holding those
  bytes resident".
- **Reading (b), the gloss.** The dash-list names "a local file" as a residency
  case, alongside "a memory mapping". Under (b) any local open makes [0,16)
  resident *per se* — the bytes are one syscall away at no round trip — and my
  `pread`-only reader is nonconforming for failing to detect F8, which
  `[R-CNF-04]` obliges every reader to detect at open.

The escape clause is written in remote vocabulary — "would have to issue a
further **range request**" — which does not obviously describe a second `pread`,
so it does not settle (a) against (b) either.

I picked (a), and my local reader omits the check unless it has already mapped
or slurped the file. I flag it because the difference is observable: given a
file whose byte 0 is `0x88`, an mmap-based local reader rejects the file and a
`pread`-based one serves every layer in it, and each can point at this sentence.

Not byte-level: the file at issue fails F8 and is nonconforming either way, and
`[R-CNF-12]` ("For a nonconforming file no acceptance obligation exists — a
reader MAY reject it upon detecting any violation") licenses the rejecting
reader under both readings. What forks is whether the *serving* reader is a
conforming reader, not whether the bytes are a conforming file.

### reader-05 — AMBIGUITY — §4.7 and §6.2's class column

> Every field this specification defines is classified **structural**,
> **semantic**, or **informative**. A field classified informative MUST NOT
> affect how any byte is located or decoded, and a reader MUST NOT alter
> decoding based on it; each informative field's definition states what a reader
> does when it contradicts the data it describes. `[R-ENC-16]`

Building the field-metadata table for my parser, I had to assign a class to
every field, and two things did not resolve.

**No field in the document is informative.** I grepped the whole file: the
string "informative" occurs three times, all inside the definitions (§1's rubric
note and §4.7 itself). Every class cell in every layout table reads
`structural`, `structural (reserved)`, or `semantic` (19 / 1 / 2 occurrences).
So `[R-ENC-16]`'s second clause — "each informative field's definition states
what a reader does when it contradicts the data it describes" — has no subject,
and §1's promise that "Every field is classified as structural …, semantic …, or
informative" advertises a class the document never uses.

**Two fields look mis-classed against §4.7's own definitions.** §6.2 classifies
`generation` and `file_id` as *semantic*, where semantic is defined as "affects
what decoded values mean". Neither affects what any decoded value means; both
are pure identity and snapshot metadata, and by §4.7's definitions ("informative
… never affects decoding") they are informative. The same question recurs for
the layer record's inline payload, whose table "omits the offset and class
columns" and whose classes "follow from the definitions above": a layer,
dimension or channel *name* neither locates bytes nor changes what a decoded
value means, which makes it informative — except that a reader does select a
layer by name, so classifying it informative sits badly with `[R-ENC-16]`'s
"MUST NOT affect how any byte is located".

I picked: treat names as structural (a layer name is the handle by which a
caller reaches that layer's bytes) and leave `generation`/`file_id` as §6.2
states. Nothing in my reader's behaviour depends on the choice, because
`[R-ENC-16]` binds only informative fields and there are none.

Not byte-level: the taxonomy has exactly one operative rule, it constrains only
a class no field occupies, and no reader behaviour or writer output turns on any
assignment.

---

## 10. What I could not determine, and what I could

I could not determine: the five items above. Everything else in my charter, I
could.

Specifically, I want to record what did *not* break, because a walk that reports
only defects misrepresents the document. The scope-assignment web is the part I
expected to find holes in, and it held under every probe: `[R-IDX-03]`'s
per-entry outcomes override `[R-ENC-03]`/`[R-ENC-04]`'s owning-scope mapping in
terms; `[R-CNT-18]` overrides `[R-CNT-15]` for sub-records in terms;
`[R-MTA-09]` overrides §17.2's tile-scope frame outcomes in terms; §18.1
separates the quarantined *document* from the un-quarantined extent *slot* in
terms; §21.1 disarms the verifier rows sitting under reject-* headers in terms.
Five overrides, five explicit statements, no inference required.

The structural/non-structural split in §15.3 is restated in three other places
(§9.7, `[R-SLB-03]`, L42) and all four agree. The reader/verifier detector split
is restated in §2.3, §2.4, §19.2, §21.1 and Appendix H and all five agree. Every
numeric example I could recompute — §11.2, §11.4, §14.2 (×3), §14.3, §14.5,
§15.4 (×2), §17.3, §20.3, Appendix A — came out right, including the two
CRC-32C constants that would have been easiest to get wrong (0xEECB3BB2 over
1,310,720 bytes of sentinel, and Appendix A's 0xE00938D2). The register's
125-row / 253-instance arithmetic is exact.

Confidence that two implementations built from this text alone would
interoperate: **high**. None of my five findings changes a byte or a verdict;
two of them are confined to a non-normative appendix.
