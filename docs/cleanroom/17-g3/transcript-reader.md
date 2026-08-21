# Cleanroom round 17 — Reader implementer transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in
four `Read` calls covering lines 1–4317 (the whole document). I opened no other file in
the repository. I ran no `git` command, no directory listing, no web fetch, no search.

Everything else I ran was local computation over files I wrote myself, in
`/private/tmp/.../scratchpad/`:

- `crc.py`, `crc2.py` — a CRC-32C implementation written from §4.5's parameters, used to
  check the document's stated check vector and every stated checksum constant.
- `inst.py` — parses §21.2–§21.5's markdown tables out of a copy of the spec text and
  counts rows and semicolon-separated instances mechanically.
- `build.py` — constructs a complete conforming 448-byte TARN file from the declarations
  alone (an extension of §7.4's `sst` example with one stored tile).
- `reader.py` — a conforming reader written from the document, with a transport that
  records every range request so the open and tile-read costs are byte-exact.
- `degrade.py` — mutates the built file fifteen ways and runs the reader over each.

`inst.py` reads `spec/tarn.md` (the one file I am permitted to read) with `open()`; I note
that explicitly in case "read" is meant to cover programmatic reads too. It reads nothing
else. I did not read, list, or otherwise touch the round17 output directory; I only wrote
this file into it.

---

## Part 1 — Constants and arithmetic I could check before writing any code

I did these first because a wrong constant is the cheapest high-value finding available,
and because I wanted a CRC I trusted before building anything.

**§4.5 check vector.** CRC-32C over `"123456789"` → `0xE3069283`. Over zero bytes →
`0x00000000`. Both reproduce. My table-driven implementation uses the reflected polynomial
`0x82F63B78`, init `0xFFFFFFFF`, final XOR `0xFFFFFFFF`, which is what §4.5's prose
(Castagnoli `0x1EDC6F41`, reflected in and out) specifies. Good — the document gives me
enough to build the checksum without consulting RFC 3720.

**Appendix A's 128-byte file.** I transcribed the hex dump and recomputed:

- file length 128 ✓, `F mod 64 = 0` ✓
- trailer at [64,128); CRC-32C over trailer bytes [0,60) = `0xE00938D2`; stored bytes at
  [124,128) are `D2 38 09 E0` ✓
- directory region [16,20) = `00 00 00 00`; `dir_length − 4 = 0` covered bytes; CRC of zero
  bytes is `0x00000000` ✓
- `dir_offset = 16 ≥ 16` ✓, `dir_length = 4 ≥ 4` ✓, `dir_offset + dir_length = 20 ≤ F − 64 = 64` ✓
- `file_id = 0x0123456789ABCDEF ≠ 0` ✓; reserved [120,124) zero ✓

Appendix A is correct byte for byte.

**§7.4's worked layer-record payload.** Recomputed independently:

- grid count `⌈100/32⌉ = 4`, so `entry_count = 4` ✓
- index region = 4 × 20 = 80 entry bytes + `⌈4/2¹⁶⌉ × 4 = 4` CRC bytes = 84, matching the
  extent-slot length the example states ✓
- CRC-32C over 80 bytes of `FF ×16 00 ×4` (four sentinels) = `0x80A34955`, stored
  `55 49 A3 80` ✓
- CRC-32C over that 4-byte array = `0xC4EE982E`, stored `2E 98 EE C4` ✓
- field offsets: name 4 bytes at 0; nine scalars 1+2+2+2+8+8+8+1+2 = 34 at 4; dimension entry
  1+1+8+8 = 18 at 38; channel entry 1+4+2+1+4 = 12 at 56; trailing 1+8+4 = 13 at 68 →
  total 81 ✓, matching every annotated offset in the example
- the channel entry `04 74 65 6D 70 0C 00 04 00 00 C0 7F` is byte-identical to §12.3's ✓

**§15.4's constant.** CRC-32C over 2¹⁶ sentinel entries (1,310,720 bytes) = `0xEECB3BB2` ✓.
Note that §7.4's example segment is *partial* (4 entries), so `[R-IDX-05]`'s licence to emit
the constant does not apply there and the example correctly computes `0x80A34955` instead.
The two rules compose correctly.

**§15.4's million-entry example.** `⌈10⁶/2¹⁶⌉ = 16` segments (15 full + 16,960); CRC array 64
bytes; region 20,000,064 bytes; entry 999,999 in segment 15 at segment-relative byte
`20 × 16,959 = 339,180`; array at [20,000,000, 20,000,064); segment 15 at
[19,660,800, 20,000,000) = 339,200 bytes ≈ "~339 KB" ✓. Full segment 1,310,720 = 1.25 MiB ✓.
Second example: disk ordinal `2·32 + 10 = 74`, entry at [1,480, 1,500) ✓; channel 3's entries
96–127 ✓.

**§11.2/§11.4 examples.** `G = (4,8)`, `N = 32`, `P = 65,536` ✓; `(300,700)` → tile `(1,2)`,
`s = 10`, in-tile `(44,188)`, ordinal `44·256 + 188 = 11,452` ✓; planar channel 2 → 74 ✓.

**§14.2 examples.** `Q = 3`, decoded 18, ordinal 5 at [15,18) ✓; planar `b` 12 bytes, ordinal 5
at [10,12) ✓; `t`+`m` → `Q = 5`, decoded 30, ordinal 5 at [25,30) ✓.

**§14.3 example.** P = 10 alternating: byte 0 = bits 0,2,4,6 set = `0x55` ✓; byte 1 = `0x01`;
with fill true the pad bits 2–7 set → `0xFD` ✓.

**§14.5 example.** Extents (5,5), tiles (4,4): grid 2×2, edge tile (1,1) covers 4–7 on both
axes = 16 positions, 1 real + 15 padding; 16 × 2 = 32 bytes ✓.

**§17.3 shuffle example.** I applied `[R-COD-10]`'s formula (byte *i* of group *j* → offset
`i·n + j`) to `00 00 80 3F | 00 00 00 40 | 00 00 40 40` with s = 4, n = 3 and got
`00 00 00 00 00 00 80 00 40 3F 40 40`, byte for byte what the example prints ✓.

**§12.1 bfloat16.** 1+8+7 = 16 bits ✓; binary32 1.0 = `0x3F800000`, high half `0x3F80`, stored
`80 3F` ✓.

**§20.3's example.** 32 · 20 + 4 = 644 ✓. **§20.3's note.** 10⁶ × 20 = 20 MB ✓.

**§21.9's note.** 2³² entries → 2¹⁶ segments → 256 KiB array ✓; 2³⁶ → 4 MiB ✓.

**§21.8's totals.** I parsed §21.2–§21.5's tables mechanically. Rows: 36 + 49 + 26 + 10 = 121,
matching each subsection heading and §21.8's "121 conditions". Instances (a `—` cell counting
as one, otherwise semicolon-separated): **273**, matching §21.8's "273 instances" exactly. I
also spot-checked the §21.1 instance criteria against individual cells — the two-direction
rule for *differs from* / *does not equal* (T3, T14, T22, L21, L22, L30, F17) versus the
one-direction rule for *exceeds* / *larger than* (T21, L44, F5), the "no magnitude ordering"
rule for checksum comparisons (F14, F20, L37, L38, T1), and the "nonzero is a value test"
rule (L20, L27, L28) — and every cell I checked follows the stated criteria.

**Verdict on Part 1: I found no wrong constant, offset or checksum anywhere in the
document.** That is a real result; sixteen rounds' worth of arithmetic is internally
consistent and externally reproducible.

---

## Part 2 — The open path, written as code

I wrote the open in the order the document forces, not the order I would have chosen.

### Step 1 — F

`[R-CNT-10]` fixes this: the size must be transport-authoritative (full-response content
length, complete length of a range response, or a size probe), and I "MUST NOT substitute
the trailer's `committed_file_length` for the transport size". So `F` is an *input* to
validation, never derived from the file. My transport exposes `size()` separately from the
byte-range API for exactly that reason.

The front block: my remote reader's open never holds [0,16), so under `[R-CNT-04]` I omit
the check. The residency test is decidable at my own open path without classifying the
network — which is the point §6.1 makes and it is the right call; my local variant reads
the file whole and *must* check by equality first.

### Step 2 — the trailer, in §6.2's mandated order

One suffix request of 64 bytes. Then, in this order and no other:

1. magic `8A 4E 52 41 54 0D 0A 1A` at trailer offset 0
2. CRC-32C over [0,60) against the u32 at [60,64)
3. version gate: `version_major = 0` → reject-file; a major I do not implement → reject-file
   with a *distinct* diagnostic (`[R-CNT-07]` makes this a SHOULD and it matters — my code
   returns "capability, not corruption")
4. only then the rest: flags gates, `committed_file_length == F` and `≡ 0 (mod 64)`,
   `dir_offset ≥ 16`, `dir_length ≥ 4`, `dir_offset + dir_length ≤ F − 64`,
   `1 ≤ generation ≤ 2⁶³ − 1`, `file_id ≠ 0`, reserved zero.

The ordering is load-bearing and the document explains why: §6.2 puts magic and CRC ahead of
the version gate because `[R-CNT-24]` fixes only those two positions across all majors, and
§21.2's preamble names exactly the four rows (F8, F14, F6, and F1's two instances) that
therefore reach a file of an unimplemented major. I implemented that and it is unambiguous.

I also added `[R-CNT-27]`'s 128-byte floor here. §6.2 does not list it among the ordered
gates but §5.1 makes it a file-scope validity error and F5 puts its detection at open. There
is no conflict: any file below 128 also fails one of §6.2's gates, but the diagnostic is
better if I check it explicitly.

### Step 3 — the directory

One range request, `[dir_offset, dir_offset + dir_length)`. Everything bounding this range
came from the trailer and is covered by the trailer CRC, so `[R-ENC-05]` is satisfied. Verify
the terminal CRC over the preceding `dir_length − 4` bytes before any other use
(`[R-CNT-11]`). The record sequence is `[dir_offset, dir_offset + dir_length − 4)` — F29's
condition states that boundary explicitly, which saved me a guess.

### Step 4 — the record walk

Framing per §7.2: 24-byte header, `inline_length` bytes of payload, repeat, no residue. Type 0
is a validity error, never an unknown type. For unknown types, the MU bit decides
(`[R-CNT-15]`). For user-metadata records I check, at open and from resident bytes only, the
three framing rules §19.1 step 4 enumerates: no (0,0) slot, `extent_length ≥ 5`,
`inline_length` exactly 1.

The layer-name namespace is the one part of the open that took real care, and §19.1 step 4
answers every question I had:

- a layer record whose *name field* does not fit inside its `inline_length` yields no name,
  contributes nothing to the namespace, and is a layer-scope error — not a file-scope one;
- uniqueness is decided **first**, over raw bytes, before well-formedness;
- so two layer records with byte-identical ill-formed names are a duplicate (reject-file),
  while one such record alone is reject-layer.

F4's condition cell agrees ("both obtainable within their records' `inline_length`"). This
is fully determined; I implemented it directly.

### Byte-exact cold remote open

Against a server supporting ranged requests, with no speculation:

| # | Range | Bytes | What bounds it before I have read it |
|---|---|---|---|
| 1 | suffix, last 64 | 64 | nothing — a suffix range needs no file integer; the response also carries F (`[R-CNT-10]`) |
| 2 | `[dir_offset, dir_offset+dir_length)` | `dir_length` | `dir_offset ≥ 16`, `dir_length ≥ 4`, `dir_offset+dir_length ≤ F−64`, all read from the CRC-verified trailer |

**Total: 2 requests, `64 + dir_length` bytes.** The front block is *not* fetched; a third
request would be needed for it and `[R-CNT-04]` licenses omitting it.

Measured on Appendix A's file: 2 requests, 68 bytes. Measured on my own built file
(`dir_length = 109`): **2 requests, 173 bytes** — my instrumented transport printed
`[('suffix', 64), ('range', 228, 109)]`.

The speculative variant: one request for a 64 KiB suffix window. If it contains the directory
region, request 2 is unnecessary (§6.4's containment test). If it reaches offset 0 — which on
any file ≤ 65,536 bytes it does — the front block becomes resident and I *must* check it by
equality. Appendix A's closing paragraph walks exactly this and gets it right, including the
112-byte window over [16,128) that spares request 2 while leaving [0,16) non-resident.

---

## Part 3 — Validation timing by tier

§19.2 gives four tiers and §21's *Detected* column gives the per-row deadline. I built the
reader as a state machine over those tiers. What I check when:

**At open** — front block (only if resident), trailer, directory CRC, record framing, unknown
top-level MU gate, multiplicity, non-layer top-level extent slots, user-metadata framing,
the layer-name namespace, and each layer record's *name* well-formedness (L3/L5/L6 carry
`Detected: open`, which is right — the open must parse names to decide uniqueness).

**At first access to a layer** — everything in §19.3's list. I checked §19.3's enumeration
against every §21.3 row whose *Detected* cell reads "layer access": L1, L2, L4, L7–L17,
L19–L24, L26–L36, L39, L43–L45. Every one of them is reached by a rule §19.3 cites. That
enumeration is complete, and I say so explicitly because a gap there would have been the
most expensive kind of defect for an implementer.

**At use of a tile** — L37, L38 (index chain, layer scope though detected at tile use — §19.2
calls this out and it is the one place the tier and the scope come apart), then T1–T25.

**At use of a record's extent** — R2–R10.

**Never** — everything whose *Detector* is `verifier`: F7, F25, F26, F27, F28, F33, F36, L18,
L25, L40, L41, L42, L46, L47, L48, L49, T2, T4, T5, T26. `[R-RDR-02]` says these impose no
reader obligation, and `[R-CNF-12]` lets me reject anyway if I happen to notice. My reader
does not look for them.

**What becomes a verdict when.** A reader has no verdict; it has outcomes. The verdict
vocabulary (*conforming* / *nonconforming* / *cannot establish*) belongs to §2.3's verifier,
and `[R-CNF-11]` orders it: an established violation always wins, *cannot establish* is
reserved for a traversal that established none, and *unexamined* constrains the report and
not the verdict. That is stated cleanly enough that I could implement a verifier's verdict
logic from it without a guess.

---

## Part 4 — A file I built, and my reader walking it

To test the layer-access and tile-read paths I built a complete conforming file from the
declarations alone. It extends §7.4's `sst` layer with one stored tile.

**Declarations.** Layer `sst`; rank 1; dimension `x`, E = 100, T = 32; interleaved; one
float32 channel `temp` with fill `0x7FC00000`; codec 1 (none); filter 1 (none); no alignment,
no slab; `linearization` 1; `index_encoding` 1.

**Derived.** `G = ⌈100/32⌉ = 4`; `N = 4`; `P = 32`; `Q = 4`; addressed-tile count = N = 4
(interleaved); decoded size = `P·Q` = **128 bytes**; index extent length =
`4 × 20 + 1 × 4` = **84**.

**Tile 3** covers x ∈ [96,128): four real positions (96–99) and **28 padding positions**
(100–127). Under `[R-SER-05]` every padding position must encode the channel's recorded fill,
so the decoded image is four real float32s followed by 28 copies of `00 00 C0 7F`. I chose
the real values to exercise `[R-TYP-04]`/`[R-TYP-05]`: 300.5 (`0x43964000`), **−0.0**
(`0x80000000`), 1.0 (`0x3F800000`), **+∞** (`0x7F800000`). Under codec 1 the stored bytes are
that image verbatim, so the index entry's length must equal 128 (`[R-COD-04]`).

**Placement** (a plain streaming writer; `[R-SLB-05]` leaves it free):

| Region | Range | Size |
|---|---|---|
| front signature block | [0, 16) | 16 |
| tile 3 payload | [16, 144) | 128 |
| tile-index region | [144, 228) | 84 |
| directory | [228, 337) | 109 |
| pre-trailer pad (slack) | [337, 384) | 47 |
| trailer | [384, 448) | 64 |

`F = 448`, `448 mod 64 = 0` ✓; `dir_offset + dir_length = 337 ≤ F − 64 = 384` ✓.

**Index entries** (disk-ordinal order): ordinals 0, 1, 2 are the sentinel `FF ×16 00 ×4`;
ordinal 3 is `offset = 16, length = 128, crc = 0x4801BBE3`. Segment CRC over the 80-byte entry
array = `0x36A47B08`; `crc_of_crc_array` over that 4-byte array = `0xE65F06AE`.

**Directory**: one record, type `0x0001`, flags `0x0003` (MU = 1, PE = 1 — §7.3 fixes them),
`inline_length = 81`, extent slot (144, 84); 24 + 81 = 105 bytes plus a 4-byte CRC = 109.

The full 448-byte hex dump is in my scratchpad. My reader, given only the file and the
document, reproduced every derived quantity and returned:

```
OPEN: F=448 gen=1 doff=228 dlen=109   layers ['sst']
  open requests: [('suffix', 64), ('range', 228, 109)]  bytes: 173
LAYER sst  G=[4] N=4 P=32  decoded sizes [128]
  x=  0  s=0 u= 0 -> temp=0000c07f    (+84 B)     sentinel -> fill, no payload I/O
  x= 31  s=0 u=31 -> temp=0000c07f    (+84 B)
  x= 32  s=1 u= 0 -> temp=0000c07f    (+84 B)
  x= 96  s=3 u= 0 -> temp=00409643    (+212 B)    300.5
  x= 97  s=3 u= 1 -> temp=00000080    (+212 B)    -0.0, preserved bit-exactly
  x= 98  s=3 u= 2 -> temp=0000803f    (+212 B)    1.0
  x= 99  s=3 u= 3 -> temp=0000807f    (+212 B)    +inf
  x=100  -> request-failed: coordinate outside extents
  x=127  -> request-failed: coordinate outside extents
```

Three things worth naming from that trace.

**Sentinel reads cost 84 bytes and no payload request.** The CRC array (4 bytes) and the
single segment (80 bytes) still have to be fetched and verified — `[R-TYP-09]` insists fill is
produced *only* by "a sentinel entry read from a verified index chain", so I cannot skip the
chain — but §19.4 step 4's short-circuit means steps 5 and 6 never run.

**A cold single-tile read costs 3 requests and 212 bytes** here: CRC array (4) + segment (80)
+ payload (128). §19.4's note licenses fetching the array and the segment in parallel. At
scale the array is the only term that grows with the layer, exactly as §1 claims: at
`entry_count = 2³²` the array is 256 KiB and the segment is capped at 1.25 MiB whatever the
layer's size.

**x = 100 and x = 127 are padding positions of a stored tile and are never returned**
(`[R-GEO-04]`). A point request there "fails as a request, with no verdict on the file"
(§19.4 step 1). Note the deliberate asymmetry §19.4 step 1 states: a *region* request whose
single interval names x = 100 succeeds and returns nothing, while a *point* request at x = 100
fails. That reads oddly but it is stated twice (§19.4 step 1 and §21.6's row) and I
implemented it as written.

### The tile-read algorithm as I coded it

From a layer name and a coordinate, in order:

1. domain: `0 ≤ xᵢ < Eᵢ`
2. `tᵢ = xᵢ div Tᵢ`, `uᵢ = xᵢ mod Tᵢ`
3. spatial ordinal `s = Σ tᵢ · ∏_{j>i} Gⱼ`; in-tile ordinal `u = Σ uᵢ · ∏_{j>i} Tⱼ`
4. disk ordinal `k = s` interleaved, `c·N + s` per requested channel c planar
5. CRC array at region byte `entry_count·20`, length `⌈entry_count/2¹⁶⌉·4`; verify against
   `crc_of_crc_array`
6. segment `k div 2¹⁶` at region bytes `[seg·2¹⁶·20, min((seg+1)·2¹⁶, entry_count)·20)`;
   verify against the array's s-th u32
7. entry at segment-relative byte `20·(k − seg·2¹⁶)`; classify per §15.3's table
8. sentinel → fill for every requested position of that tile, bit-exactly from the channel
   entry; malformed → reject-tile, and **never** fill
9. fetch `[offset, offset+length)`; verify the entry's crc
10. codec decode, then the filter's **inverse** (the pipeline is filter-then-codec on write,
    so codec-then-inverse-filter on read — §17.1 states the order explicitly and it is the
    one thing in this area an implementer would otherwise get backwards)
11. length must equal the declaration-derived decoded size exactly (`[R-SER-07]`)
12. extract: interleaved `u·Q + Fᶜ`; planar numeric `u·Bᶜ`; planar bool bit `u mod 8` of byte
    `u div 8`
13. return bit patterns unaltered

The decoded byte layout I end up with, stated exactly, for the three cases:

- **interleaved**: `P·Q` bytes; channel c's value at in-tile ordinal u occupies
  `[u·Q + Fᶜ, u·Q + Fᶜ + Bᶜ)` where `Q = Σ Bᵢ` and `Fᶜ = Σ_{j<c} Bⱼ`; a bool channel is one
  byte, 0x00/0x01
- **planar, numeric channel c**: `P·Bᶜ` bytes; ordinal u at `[u·Bᶜ, (u+1)·Bᶜ)`
- **planar, bool channel**: `⌈P/8⌉` bytes, LSB-first; ordinal u is bit `u mod 8` of byte
  `u div 8`; the final byte's bits `P mod 8 … 7` are pad bits carrying the fill bit

The byte-shuffle inverse: `s = Bᶜ` (planar numeric), `s = Q` (interleaved), `s = 1` and
identity (planar bool). `n = L/s`; restore byte `i·n + j` to offset `j·s + i`. I verified the
divisibility claim holds in all three cases: `P·Bᶜ / Bᶜ`, `P·Q / Q`, and anything / 1.

---

## Part 5 — Degradation walks

Fifteen mutations of the built file, each run through the reader. All fifteen behaved as the
document prescribes; the seven I traced end to end:

**1. `version_major = 2`.** Trailer magic passes, trailer CRC passes (recomputed), version
gate fires → reject-file, reported as a capability refusal with a diagnostic distinct from
"not a TARN file" and from "corrupt" (`[R-CNT-07]`). Nothing is served. §21.6's closing
paragraph is explicit that the file may be perfectly conforming under major 2 and that this
is not a finding about its bytes — so my verifier variant reports *cannot establish*, not
*nonconforming*.

**2. Incompat-lane bit 0 set.** Reject-file (`[R-CNT-08]`). **3. Ignore-lane bit 16 set.**
Ignored; the file reads normally and stays conforming (§21.6). My updater variant copies the
bit forward and must not clear it; my compactor variant carries it into a *new* file rather
than writing `flags = 0` (`[R-WRT-06]`). That is a genuinely easy thing to get wrong and the
document flags it in three places.

**4. Truncated tail** (64 bytes removed) and **5. residue appended** (64 zero bytes). Both
present as "the 8 bytes at F−64 are not the trailer magic" → reject-file, and `[R-LIF-05]`
forbids me to scan backward. §9.5's note is right that a reader cannot tell residue from
corruption and is not asked to; recovery is §9.6's deliberate, separate operation, and my
reader does not implement it.

**6. Unknown top-level record type `0x8001`, MU = 0.** Ignored as though absent; the layer
still reads, both the sentinel and the stored tile. **7. Same with MU = 1.** Reject-file
(`[R-CNT-15]`). Note that the MU = 0 file is *conforming* (§21.6) while the MU = 1 file is
also conforming and I refuse it anyway — §21.6's "conforming files a reader nevertheless
refuses". My diagnostic distinguishes the two, as §21.6 asks.

**8. Codec `0x8000` (experimental) and 9. codec 5 (reserved).** Both reject-**layer** at layer
access (`[R-COD-03]`). Every other layer and the file-scope records stay readable, and §2.4
lets me still list the rejected layer's name. `[R-EXT-03]` is explicit that both ranges take
the same reader treatment in this space, and that the metadata-encoding space is the sole
exception. My reader treats them identically.

**10. One byte of tile 3's payload flipped.** The entry's crc fails → reject-**tile**. x = 96
reports failure; x = 0, a sentinel in the same layer, still returns fill. This is the case
`[R-CNF-09]` and `[R-TYP-09]` exist for: a rejected tile must **not** silently return fill,
and my code returns a failure object rather than the fill bytes. The distinction is invisible
in a naive implementation and is the single most important reader behavior in the document.

**11. Segment-CRC-array byte flipped and 12. `crc_of_crc_array` corrupted.** Both surface as
`crc_of_crc_array` mismatch → reject-**layer**, detected at *tile use* but taking *layer*
scope (`[R-IDX-04]`, and §19.2 calls the tier/scope split out by name). Prospective under
§2.4: anything I had already returned from that layer stands.

**13. `entry_count = 5` against a geometry that derives 4.** Reject-layer at layer access
(`[R-CNT-17]`), before any I/O. **14. Directory byte flipped.** Directory CRC → reject-file.

**15. Entry 3's offset set to 8** (inside the front block), with the segment CRC and
`crc_of_crc_array` recomputed so the chain verifies. §15.3 classifies this *structural*:
reject-tile. x = 96 reports failure; the sentinel tiles still read. The bytes the entry
nominally addressed contribute no claimant to §9.7's coverage walk and fall to slack. This
row is where compaction gets interesting — see finding reader-02.

**Limit exceeded.** Not constructible at realistic size, but the rule is unambiguous:
`[R-ERR-04]` lets me decline "at the whole file, or at the narrowest scope whose declarations
exceed what it can serve, a layer or a tile", and the refusal MUST be reported as a resource
limit and not as a validity error. §18.2's Note handles the one case where the narrowest
scope is the whole file — a user-metadata document has no declared size, so there is no
narrower scope whose declarations the rule can measure.

---

## Findings

### reader-01 — CONTRADICTION — §11.1's Rationale states the shrink bar over the wrong generation

**Location:** §11.1 (the Rationale under `[R-GEO-02]`), against §20.3 step 4 (`[R-WRT-04]`).

**Quotation (§11.1):**

> §20.3 states normatively, and governs, what a commit may do to a layer that already stores
> tiles: a shrink is barred wherever it alters what §14 fixes for a tile the new state still
> stores, and permitted where it drops tiles out of the addressed set, whose extents then
> become slack.

**Quotation (§20.3 step 4):**

> An extent MAY also **shrink**, and the bar above is the whole of the test, **in the bar's
> own tense**: a shrink is permitted exactly where it alters nothing §14 fixes for any tile
> the layer stores in the generation this commit supersedes. Dropping a tile out of the
> addressed set (§11.2's grid count falls) is not itself such an alteration — a tile the new
> state does not address carries no §14 obligation and its extent becomes slack — but neither
> does it rescue a commit that damages a prior-generation stored tile. Unstoring that tile in
> the same commit does not rescue it either, and for the same reason: the quantifier is the
> superseded generation's, so a shrink that turns real positions into padding of a tile stored
> there is barred whether or not the new state still stores it.

**The defect.** These range over different sets of tiles, and §11.1 names the one §20.3 goes
out of its way to foreclose. §20.3's bar quantifies over *tiles stored in the generation the
commit supersedes*; §11.1 quantifies over *tiles the new state still stores*. §11.1 also
states as a flat permission ("permitted where it drops tiles out of the addressed set") the
very thing §20.3 says is no rescue.

**Construction.** Layer L at generation 5 stores the tile at disk ordinal 0, an interior tile
with no padding positions. Commit 6 shrinks E₀ so that positions the tile carried at ordinal 0
become padding, and in the same commit writes ordinal 0's entry as the sentinel. Under §20.3
this commit is **barred** — "a shrink that turns real positions into padding of a tile stored
there is barred whether or not the new state still stores it", and "Unstoring that tile in the
same commit does not rescue it either". Under §11.1's sentence it is **permitted**, because
the new state does not store that tile. §11.1's set is, in effect, strictly smaller than
§20.3's — a newly stored tile is written under the new declarations and cannot be damaged — so
§11.1's rule is strictly more permissive, and the extra permission covers exactly the case
§20.3 spends three sentences closing.

The same paragraph continues "A layer that stores nothing may be re-declared freely," which
is untensed and therefore correct: §3.1 makes unqualified *stored* mean the live generation,
which for an appender mid-commit is the generation being superseded, and §20.3 says the same
thing with the tense written out. Only the shrink sentence names the wrong generation, which
is what makes this look like a propagation miss rather than a disagreement.

**What an implementer does wrong without it.** A writer implementer who reads §11.1 first —
and §11.1 is where the shrink question naturally arises, since it is the section on geometry
and its validity floor — implements "damage is fine as long as you unstore it in the same
commit". They then emit commits §20.3 forbids. Nothing catches them: §21.7 says this is
precisely the sub-case where the bar has no live-state witness, so no verifier will ever tell
them.

**Byte-level: no.** §11.1's passage is a Rationale and therefore non-normative under
`[R-CNF-01]`, and it explicitly says §20.3 "states normatively, and governs". More decisively,
the operation the two readings disagree about produces the *same conforming bytes* either way:
§21.7 records that "a commit that supersedes every tile it would have damaged leaves the live
state clean, so the bar is unwitnessed there for the same reason `[R-LIF-01]` is". So no reader
outcome and no verifier verdict differs on any byte sequence. What differs is which commits a
conforming writer may perform, which is exactly the class §2.3 calls conduct.

---

### reader-02 — CONTRADICTION — a compactor is told both to refuse and to reproduce a structurally invalid index entry

**Location:** §20.5, `[R-WRT-06]` against `[R-WRT-07]`, reading with `[R-WRT-09]`, §2.3 and
§19.2.

**Quotation (`[R-WRT-06]`, §20.5):**

> A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges fails, and MUST NOT
> emit a file carrying a violation it has detected: it can neither re-emit the structure
> corrected (`[R-WRT-05]`), nor keep it and call the output clean. Dropping is the one
> disposal that answers, and only where §20.4's table licenses it … Where the table does not
> license a drop the compactor MUST refuse.

**Quotation (`[R-WRT-07]`, §20.5):**

> an entry §15.3 classifies reject-tile on a structural ground is reproduced with its offset
> and length exactly as they stand, there being no live extent for a re-pointing to target —
> `[R-IDX-03]` gives such an entry no stored extent and no claimant in the coverage walk — and
> the violation travels with it into the output (`[R-WRT-01]`); `[R-WRT-09]`'s checks reach the
> index chain and each stored tile's entry crc, not an entry's own value domain, so such an
> entry is not one `[R-WRT-06]` obliges a compactor to refuse

**Quotation (`[R-WRT-09]`, §20.5):**

> A compactor's verification depth follows reliance over everything it carries
> (`[R-WRT-03]`): it **relies structurally on every structure it copies**, so it MUST verify
> each link of the chain …

**The defect.** The carve-out's stated reason is refuted by the neighbouring requirement. To
regenerate a relocated index region, a compactor must decide, per entry, whether to re-point
its offset (well-formed stored tile), leave it alone (sentinel), or "reproduce it with its
offset and length exactly as they stand" (structural). That third branch *is* §15.3's
classification — the compactor cannot take it without having classified the entry, i.e.
without having detected T6/T7/T8/T9/T10/T11/T12. And §2.3 makes an updater "a reader of the
files they process", inheriting "every reader obligation"; `[R-CNF-04]` obliges a reader to
detect every register row whose detector is the reader, which all six structural rows are;
§19.2 ties the deadline to "first reliance on the structure that carries it", and `[R-WRT-09]`
says in terms that a compactor relies structurally on every structure it copies.

So the compactor has, necessarily, detected a violation. `[R-WRT-06]` then says it MUST NOT
emit a file carrying it, and dropping is not available — an index entry is not a record, so
§20.4's table licenses nothing — which leaves refusal. `[R-WRT-07]` says the opposite.

**Construction.** My degradation walk 15 is the input: a file whose layer `sst` carries a
tile-index entry with `offset = 8`, `length = 128`, a correct segment CRC and a correct
`crc_of_crc_array`. `[R-WRT-09]`'s enumerated checks — the open, §19.3's layer validation,
`[R-IDX-04]`'s index chain, each relocated extent's checksum — all pass, because none of them
inspects an entry's value domain. Compactor A classifies entries per §15.3 (as any reader
must) and, having detected T8, refuses under `[R-WRT-06]`. Compactor B follows `[R-WRT-07]`
literally and emits an output file that contains the entry verbatim at its disk-ordinal
position, with `crc_of_crc_array` and the segment CRC recomputed over the re-emitted entries.

**What an implementer does wrong without it.** Either they ship a compactor that refuses every
file with one damaged entry — a bad outcome, since compaction is the only operation that
reclaims slack and the damaged entry is exactly the kind of thing an operator is trying to
compact around — or they ship one that knowingly propagates a violation into a file it also
represents as its output. The document does not let them reason to a single answer from
`[R-WRT-06]` alone.

**Byte-level: no**, though I want to be precise about why, because the case is close.
`[R-WRT-07]` does state a conclusion, flatly: "such an entry is not one `[R-WRT-06]` obliges a
compactor to refuse". That sentence decides the question in favour of compactor B, and an
implementer who reads all of §20.5 lands there. What is broken is the *reasoning* offered for
it, which contradicts `[R-WRT-09]`'s own reliance clause and §2.3's reader inheritance. The
divergence I can construct is between a compactor that emits a file and one that emits
nothing — not between two files' bytes, and not between two readers' verdicts on the same
bytes. No conforming *reader* behaves differently on either input, and no verifier's verdict
turns on it (both inputs are nonconforming and stay so). I would rather state that honestly
than inflate it.

---

### reader-03 — AMBIGUITY — §21.5's preamble does not delimit which failures the experimental-encoding exception covers

**Location:** §21.5's introductory paragraph, against `[R-MTA-10]` (§18.2), `[R-SEC-04]`
(§22.3), and R2's own row.

**Quotation (§21.5):**

> User metadata is quarantined (`[R-CNT-25]`): every way its document can be unreadable takes
> this outcome, whatever the containing scope — as a violation in the rows below, except at an
> experimental-range encoding, where no document rule attaches and §21.6 records the defined
> non-violation (`[R-MTA-10]`).

**The problem.** The subject of that sentence is "every way its document can be unreadable",
and `[R-CNT-25]` defines that set explicitly: "a failed extent CRC, an unimplemented or
invalid encoding, a decode failure, or content violating the document's own rules". A failed
extent CRC is a member. The exception clause — "except at an experimental-range encoding" —
is attached to the *encoding*, not to a subset of the failure modes, so read on its face it
withdraws violation status from **every** row in §21.5 whenever the encoding byte is ≥ 0x80,
R2 included.

**Permitted readings.**

*(a) The exception is over the whole failure set.* Under an experimental encoding, a failed
extent CRC (R2) is not a violation. A verifier meeting such a record in an otherwise clean
file **certifies**.

*(b) The exception is over the encoding-value ground only* — i.e. it says only that the
record's being unreadable *because its encoding is unassigned* is not a violation at ≥ 0x80,
which is what §21.6's row records. R2 stays a violation at every encoding value, and a
verifier reports **nonconforming**.

**Which I picked: (b), and why.** Three things outside §21.5 decide it. First, `[R-MTA-10]`
names the surviving checks exhaustively: "file conformance — a pure predicate on bytes
(`[R-CNF-02]`) — is decided by the structural checks that precede the document alone: the
record's framing and extent slot (`[R-CNT-13]`), the encoding byte's own value set
(`[R-MTA-03]`), and **the extent's terminal CRC** (`[R-CNT-20]`)." Second, `[R-SEC-04]` says
the same from the other side: "the extent of a user-metadata record under an unassigned
encoding is covered by its terminal CRC but constrained by no content rule (`[R-MTA-10]`)".
Third, R2's own row carries no encoding qualifier and its instances are containers only
("top-level extent; layer sub-record extent"). The preamble's very next sentence is also
entirely about the encoding-value axis — "Encoding 0 and a reserved-range value are unassigned
too, and R1 registers both as violations: what `[R-MTA-10]` withdraws is the document's
content rules, never the encoding byte's own value set" — which supports reading the exception
as belonging to that axis. So reading (b) is the intended one; it just is not what the
sentence says.

**Construction.** A file with one top-level user-metadata record, `encoding = 0x80`,
`extent_length = 64`, whose terminal 4 bytes do not equal the CRC-32C of the preceding 60, and
which is otherwise conforming. Verifier under (a): *conforming*. Verifier under (b):
*nonconforming*. Reader behavior is identical either way — ignore-record with a SHOULD-report.

**What an implementer does wrong without it.** A verifier author who works from §21.5's
preamble (the natural place to work from, since it is the paragraph that governs the whole
ignore-record table) short-circuits R2 whenever the encoding byte is ≥ 0x80 and certifies a
file with a corrupt metadata extent. That is precisely the outcome §22.3 warns about when it
says a certificate covers those bytes uninspected and that this is why `[R-MTA-10]` makes the
report name each such record.

**Byte-level: no.** It would be — a verifier's verdict on a specific byte sequence is exactly
an accept/reject verdict — except that the register row itself (R2) and the governing rule
(`[R-MTA-10]`) agree with each other and against the preamble, two-to-one, and §21.1's
principle that a row restates its rule and the rule governs points the same way. The fork is
closed by text I can cite; what remains is that the closing costs a cross-section trip from
the paragraph most likely to be read first. I am recording it as an ambiguity in the prose
rather than an open question about bytes.

---

### reader-04 — CONTRADICTION — §20.4 licenses a drop on an operation §20.4 says no commit performs

**Location:** §20.4, the MU = 0 / PE = 0 row of the preservation table, against the paragraph
immediately following the table.

**Quotation (table row):**

> An appender may drop it only in a commit that *independently* changes the scope the record
> attaches to: … for a top-level record, the file's layer set — which a commit changes by
> **adding or removing a layer** and equally by modifying any layer's record — or another
> *non-layer* top-level record.

**Quotation (next paragraph):**

> No commit therefore removes a layer record, or a user-metadata record at either scope.

**The defect.** The table's licence names three ways a commit changes the file's layer set,
one of which the following paragraph declares impossible for any commit. Compaction does not
rescue it either — §20.4's closing sentence says compaction "carries every layer of its input
forward (§20.5)" — and a whole-file rewrite under a fresh `file_id` is not a commit
(`[R-LIF-01]`). So "removing a layer" names no operation this specification defines.

**What an implementer does wrong without it.** Nothing, in practice, which is why I rank this
last: the branch is dead and an appender that implements it will never take it. The cost is to
a reader of §20.4 who is trying to work out what an appender may do and is told, in the same
subsection, both that removing a layer is a thing a commit does and that no commit does it.
That is the sort of thing that makes an implementer distrust the surrounding text, which in
§20.4 is text they need to trust.

**Byte-level: no.** The licence is unreachable; no file's bytes and no verdict turn on it.

---

## Where I had to guess, and what I guessed (beyond the findings)

These did not rise to findings — the document either decides them or licenses the divergence
— but they are the points where I stopped and had to think, and they are worth recording.

**Partial results when a layer-scope failure interrupts a multi-entry request.** §19.4 step 8
says a layer-scope failure "bars the request's remaining entries and all further service from
the layer; the bar is prospective, so values the reader has already returned under §19.2's
timing stand". Within a *single* request it is not stated whether entries already decoded but
not yet handed to the caller may be delivered. I chose to deliver nothing from a request that
hit a layer-scope failure, on the grounds that "already returned" most naturally means
returned to the caller and nothing has been. Either choice is defensible and `[R-CNF-12]`
licenses the stricter one anyway, so nothing forks.

**The front-block residency asymmetry is deliberate divergence, not a defect.** A file with a
corrupt front block but a clean trailer and directory is rejected by a local reader and served
by a remote one fetching exact ranges. `[R-CNT-04]` says so in terms, F6's condition cell
repeats it, and `[R-CNF-12]` makes both readers conforming because the file is nonconforming.
I implemented both and did not file it.

**§6.1's "and nothing else".** §6.1 says the local/remote distinction "governs the request
accounting of §6.4 and nothing else", while §6.2 uses it ("for a remote reader, the size
reported by its transport") and `[R-CNT-10]` places obligations on "a remote reader" that a
local one does not carry. Since `[R-CNT-10]` sits inside §6.4, "the request accounting of
§6.4" fairly covers it, and I read the sentence as true. Recorded because it cost me a
re-read.

**§21.7's "only where … and".** The sentence reads "witnessed only where the affected tiles
remain stored *and* the change reaches a byte §14 structurally constrains … ; a change that
reaches the decoded size or the codec **instead** is witnessed by T3 or T14". The "only … and"
is false as a claim about the bar in general, but "instead" scopes the first clause to
content-row witnessing and the sentence recovers. Note that §21.7 gets the *quantifier* right
where §11.1 gets it wrong: the witness condition correctly ranges over the live state ("the
affected tiles remain stored") while the bar ranges over the superseded generation. Not filed.

**§20.5's "slack is never carried".** A compactor's output still has a pre-trailer pad and,
where an alignment is declared, alignment gaps — both slack. "Carried" means carried from the
input, and §5.2 makes the pad slack in every file. Not a defect; recorded because the phrase
reads absolutely on first pass.

**Codec-1 length check placement.** `[R-COD-04]` says the equality is "checkable from the entry
and the layer record alone, before any payload fetch", but §19.4 lists no step for it and T14's
deadline is "tile use". I check it between steps 4 and 5, which saves the payload fetch. §19's
preamble ("A row this section does not restate is due at its own tier all the same") licenses
this explicitly and it was the right call.

## What I could not exercise

I did not build files under codecs 2–4 or filter 2, because doing so would need encoders I
would have to pull in, and the rules for them (`[R-COD-05]` through `[R-COD-10]`) are stated
precisely enough — raw RFC 1951 stream with no wrapper and nothing trailing; exactly one RFC
8878 frame with the magic, no skippable frame, no second frame, zero dictionary ID, no
content-checksum flag, window ≤ decoded size, FCS equal to decoded size when present and never
an allocation source; exactly one raw LZ4 block with the decoded size as output capacity —
that I am confident I could implement them without a further guess. I did implement the
byte-shuffle inverse and verified it against §17.3's worked example.

I did not exercise a planar layer or a packed boolean plane with real bytes; I verified their
arithmetic on paper against §14.2's and §14.3's examples instead, and coded both extraction
paths.
