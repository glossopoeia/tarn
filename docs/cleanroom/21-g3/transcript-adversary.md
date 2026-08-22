# Cleanroom round 21 — Adversary transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,377 lines), in five `Read` calls covering lines 1–4377 with no gaps. I ran
`wc -l` and four `grep`/`python3` invocations against that file, plus local
Python that reads no project file (CRC-32C, byte-layout assembly, register
arithmetic). I did not open `docs/`, `PLAN.md`, `AGENTS.md`, `README.md`,
`conformance/`, `spec/registry.json`, or any ADR; I ran no `git` command, no
web search, no web fetch, and did not list any directory to discover what
else exists. I wrote three scratch Python files and one `.tarn` binary I
generated myself, plus this transcript. I did not read the output directory.

**Context I did not ask for.** My runtime placed material in context before I
began: a project instruction file (`CLAUDE.md`, which forwards to `AGENTS.md`)
and an index of the maintainer's memory notes with six entry titles, plus a
stale task list from prior rounds. I name that it appeared; I did not open any
file it referenced and I did not use any of it to reach a conclusion. Nothing
below rests on it. I also received an MCP server instruction block and a skills
listing, neither relevant.

**Method.** I read the document end to end once, cold, taking the four
"changed-surface" passages the brief pointed at (§18.2's `[R-MTA-09]`, §21.5's
preamble clause) in sequence with everything else rather than first, so that I
would meet them the way an implementer does. Then I did four things:

1. **Reproduced every worked number in the document** — CRC constants, the
   Appendix A minimal file byte for byte, the §7.4 layer-record example byte
   for byte, the §11.2/§11.4/§14.2/§14.3/§14.5/§15.4/§17.3 arithmetic.
2. **Built a complete conforming file** with a real layer, a stored tile, an
   index region and a directory, and checked its slack total against
   `[R-CNT-21]`'s definition.
3. **Ran the register's own arithmetic** mechanically against §21.8's claim.
4. **Attacked**, surface by surface, writing each attack down to concrete
   bytes and then asking which sentence forecloses it.

Findings are in §5. Everything I tried and failed to break is in §4, because
an empty result is only worth anything if the attacks were real.

---

## 1. Arithmetic verification — everything the document asserts numerically

I implemented CRC-32C from the parameters in §4.5 alone (polynomial 0x1EDC6F41,
reflected in and out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) — reflected table
constant 0x82F63B78 — and checked it against §4.5's own check vector before
using it for anything.

```
CRC-32C("123456789")            = 0xE3069283   §4.5 says 0xE3069283   OK
CRC-32C(zero bytes)             = 0x00000000   §4.5 says 0x00000000   OK
CRC-32C(4 sentinel entries, 80B)= 0x80A34955   §7.4 says 0x80A34955   OK
CRC-32C(bytes 55 49 A3 80)      = 0xC4EE982E   §7.4 says 0xC4EE982E   OK
CRC-32C(2^16 sentinel entries)  = 0xEECB3BB2   §15.4 says 0xEECB3BB2  OK
```

The last one is 1,310,720 bytes of `FF x16 00 x4` repeated 65,536 times. It
matches. `[R-IDX-05]`'s constant is right, and so is the observation in
§15.2's Rationale that a sentinel's crc field being 0 is what keeps an
all-0xFF region invalid.

Note also that CRC-32C of zero bytes is 0x00000000, which is why
`[R-CNT-23]`'s forced `crc_of_crc_array = 0` at `entry_count = 0` is not an
arbitrary sentinel but the actual CRC of the zero-length segment-CRC array.
Consistent; I checked it because a forced-zero field that disagreed with the
real CRC would be a genuine seam.

### Appendix A, byte for byte

I built the 128-byte minimal file from the rules alone — front block, empty
record sequence (zero bytes) followed by its CRC at [16,20), 44 bytes of pad,
trailer at [64,128) with generation 1, dir_offset 16, dir_length 4,
committed_file_length 128, file_id 0x0123456789ABCDEF, reserved zero, trailer
CRC over [0,60) — and compared against the hex dump in Appendix A.

**Exact match, all 128 bytes.** Trailer CRC computes to 0xE00938D2, which is
what byte [124,128) holds as `D2 38 09 E0`.

I checked the pad length against `[R-LIF-02]` step 5: the directory ends at
20, the next 64-byte boundary is 64, so the pad is 44 bytes and F = 128. So
Appendix A's file is one a conforming commit actually produces, not merely one
that passes the gates. (§6.2 separately says a *longer* gap is conforming and
that no conforming commit produces one, and `[R-CNF-02]` classifies that as a
writer-conduct rule — so a file with, say, F = 192 and the same directory is
also conforming. I confirmed the gates: 20 <= 192-64 = 128, 192 mod 64 = 0.)

### The §7.4 layer-record example

I built the inline payload from the field table alone: name `sst`, layout 1,
linearization 1, codec 1, filter 1, A = 0, S = 0, A_slab = 0, rank 1, C = 1,
dimension `x` extent 100 tile extent 32, channel `temp` type 12 fill
`00 00 C0 7F`, index_encoding 1, entry_count 4, crc_of_crc_array 0xC4EE982E.

**81 bytes, byte-identical to the annotated block.** The stated field
accounting also checks: 4 (name) + 34 (layout..C) + 18 (dimension entry) +
12 (channel entry) + 13 (trailing) = 81. `[R-CNT-17]`'s extent_length is
4 x 20 + ceil(4/2^16) x 4 = 84, and the region I built (80-byte entry array
plus one 4-byte segment CRC) is 84.

### The rest of the worked numbers

- §11.2: extents (1024,2048), tiles (256,256) -> G = (4,8), N = 32, P = 65,536. OK.
  With extents (1000,2048), G_y = ceil(1000/256) = 4. OK.
- §11.4: coordinate (300,700) -> tile (1,2), s = 1*8+2 = 10, in-tile (44,188),
  in-tile ordinal 44*256+188 = 11,452. Planar C=4 channel 2 -> 2*32+10 = 74. OK.
- §14.2: interleaved a(uint8)+b(uint16), Q = 3, P = 6, decoded 18; ordinal 5's
  sample at [15,18), b at 16-17. Via the table's own formula with k = 5*2+1 = 11:
  (11 div 2)*3 + F_1 = 5*3+1 = 16. OK. Planar b: 12 bytes, ordinal 5 at 10-11. OK.
  t(float32)+m(bool): Q = 5, decoded 30, ordinal 5 at [25,30), m at 29. OK.
- §14.3: planar bool P = 10 alternating -> byte0 0x55, byte1 0x01 with six pad
  bits; fill true -> 0x01 | 0xFC = 0xFD. OK.
- §14.5: extents (5,5) tiles (4,4) -> grid 2x2, edge tile (1,1) has one real
  position and 15 padding; uint16 fill 0xABCD -> 32 bytes, values 1-15 = CD AB. OK.
- §15.4: entry_count 1,000,000 -> 16 segments (15 full + 16,960), 64-byte CRC
  array, region 20,000,064 bytes; tile 999,999 in segment 15 at segment-relative
  byte 20 x 16,959 = 339,180; CRC array at [20,000,000, 20,000,064); segment 15
  at [19,660,800, 20,000,000) = 339,200 bytes. One full segment = 65,536 x 20 =
  1,310,720 = 1.25 MiB. All OK.
- §15.4 second example: disk ordinal 74 -> region bytes [1,480, 1,500) = 20x74. OK.
  Channel 3 of C=4, N=32 -> entries 96..127. OK.
- §17.3 byte-shuffle: I applied `filtered[i*n + j] = image[j*s + i]` to
  `00 00 80 3F 00 00 00 40 00 00 40 40` with s=4, n=3 and got
  `00 00 00 00 00 00 80 00 40 3F 40 40`. Matches the example exactly.
- §21.1's parenthetical "C·N (which dominates the max disk ordinal
  (C-1)·N + (N-1))": (C-1)N + N-1 = CN - 1 < CN. OK.
  "P·Q (which dominates V = P·C)": Q = sum of B_i >= C since every B_i >= 1. OK.
- §21.9's note "2^32 addressed tiles is the point where the segment-CRC array
  ... is still 256 KiB": ceil(2^32/2^16) x 4 = 2^16 x 4 = 262,144. OK.
  "it reaches 4 MiB at 2^36": 2^20 x 4 = 4,194,304. OK.

**Every numeric assertion in the document reproduces.** I found no arithmetic
error. That is itself worth recording: twenty rounds have not left one.

---

## 2. A complete file, built from the document alone

To make sure I was attacking real bytes rather than a mental model, I built a
one-layer file end to end. Layer `sst`, rank 1, E = 100, T = 32 (G = N = 4),
interleaved, one float32 channel, codec 1, filter 1, tile 0 stored (128 bytes
= P x Q = 32 x 4), tiles 1-3 sentinel.

```
front   [0, 16)
tile 0  [16, 144)      128 bytes, codec 1 so length == decoded size (R-COD-04)
index   [144, 228)     84 bytes = 4x20 entries + one 4-byte segment CRC
dir     [228, 337)     24-byte record header + 81-byte payload + 4-byte CRC
pad     [337, 384)     47 bytes of slack
trailer [384, 448)     F = 448, 448 mod 64 = 0, dir end 337 <= 448-64 = 384
```

Coverage check per `[R-CNT-02]` and `[R-LIF-08]`: claimants are the front block
(16), the stored-tile extent (128), the layer record's extent = the index region
(84), the directory (109) and the trailer (64) = 401 bytes. F - 401 = **47**,
which is exactly the pad. `[R-CNT-21]`'s slack total is well-defined and I can
compute it. I did the same for Appendix A: 16 + 4 + 64 = 84, slack 44, which is
the 44-byte pad the annotation names. Both agree.

I also confirmed that `[R-CNT-05]` forces the directory to be the *last*
structure: if I had placed the directory at 16 and the tile after it, the tile
would sit between the directory's end and the trailer and F7 would fire. The
commit protocol's step order (§9.2 steps 2, 3, 5) produces the required layout
by construction.

This file is my mutation base for §3.

---

## 3. The register's own arithmetic

§21.8 claims "121 conditions over 273 instances". §21.1 makes the count
mechanical: instances are semicolon-separated within a cell, and "a cell
reading — is one instance". I parsed all four register tables:

```
rows:      F 36   L 49   T 26   R 10   = 121   (§21.2 says 36, §21.3 49,
                                                §21.4 26, §21.5 10)
instances: F 58   L 116  T 55   R 44   = 273
```

Exact on both. I then hand-checked a dozen cells against §21.1's two stated
axes — layout formulas enumerate, magnitude comparisons enumerate both
directions where the text does not bound the direction, an *exceeds* gives one:

- T3 ("is not exactly") — 2 directions x 3 layouts = 6. Cell has 6.
- T14 ("differs from") — 2 x 3 = 6. Cell has 6.
- T21 ("larger than") — one direction x 3 layouts = 3. Cell has 3.
- T22 ("does not equal") — 2 x 3 = 6. Cell has 6.
- L44 ("exceeds") — one direction x 3 layouts = 3. Cell has 3.
- L21 ("does not equal") — 2 layouts x 2 directions = 4. Cell has 4.
- L30 ("differs from") — 2. Cell has 2.
- L2 — nine derived quantities. Cell has 9.
- F17 ("does not equal") — physical shorter / longer = 2. Cell has 2.
- F5 ("is below") — one direction over two fields = 2. Cell has 2.
- R4 — 6 alternatives x 2 containers = 12. Cell has 12.
- R5 — 4 alternatives x 2 containers = 8. Cell has 8.
- L29 — A_slab = 0; not a power of two; above 2^62 = 3. Cell has 3.

I found no cell whose count disagrees with §21.1's rules.

I then tested §21.1's **completeness** clause ("a detectable file-conformance
violation this specification names and the register omits is a defect in this
document") by walking every writer-binding MUST/MUST NOT and every declarative
file-level constraint in the document and looking for its row. I list the walk
in §4.1. I found no omission.

---

## 4. Attacks, and the sentence that forecloses each

### 4.1 Register-completeness sweep

I grepped every `Writers MUST`, `MUST NOT emit`, `writers MUST`, `MUST equal`
and every field-table constraint, and located each one's register row:

| Constraint | Row(s) |
|---|---|
| §6.1 front block byte-identity | F6 (F1 for the reversed instance) |
| §6.2 trailer magic / CRC / field gates | F8, F14, F9, F10, F11, F12, F13, F15, F16, F17, F2, F3 |
| §6.3 version_major 0 / incompat bit | F18, F19 |
| §7.1 directory CRC | F20 |
| §7.1 UM extent (0,0) / < 5 | F21, F22 / L10, L11 |
| §7.2 framing, residue, type 0 | F29, F24 / L14, L13, L23 |
| §7.2 reserved flag bits, MU=1/PE=0 | F26, F25 / L47, L46 |
| §7.2 extent slot half-zero / <16 / past F-64 | F30, F31, F32 / L15, L16, L17 |
| §7.2 extents owned exactly once | F33 / L18 |
| §7.2 reserved-range type, with and without MU | F35, F36 / L24, L25 |
| §7.3 registered type stored-flag mismatch | F28 / L49 |
| §7.4 every field constraint | L36, L33, L43, L45, L39, L28, L29, L32, L34, L30, L35, L31, L21, L27, L22, L20, L23 |
| §7.4 nested layer record as sub-record | L26 |
| §7.4 multiplicity | F34, L19 |
| §4.6 UTF-8, empty, C0, duplicate names | L3, L4, L5, L6, L7, L8, L9, F4 |
| §5.1 minimum file size | F5 |
| §6.2 structure in the pre-trailer gap | F7 |
| §11.1 rank/tile-extent/channel-count floors | L32 |
| §11.2 geometry overflow | L2 |
| §14 decoded size, padding, pad bits, bool byte | T3, T4, T5, T2 |
| §15.3 all entry states | T6-T12, T1 |
| §16 alignment and slab invariants | L40, L41, L42 |
| §17 all codec and filter conditions | T13-T25, L43, L44, L45 |
| §17.3 wrong shuffle stride | T26 |
| §18 encoding value set, frame constraints, document rules | R1-R10, F23, L12, F27, L48 |

The residue — `[R-ENC-06]` field widths, `[R-LIF-01]`/`[R-LIF-03]` history,
`[R-GEO-06]`/`[R-SER-01]` ordinal mappings, `[R-CNT-13]`'s no-embedded-offsets,
`[R-CNT-18]`'s nesting prohibition, §20.3 step 4's declaration bar, `[R-WRT-06]`'s
two trailer obligations — is exactly what §21.7 accounts for, with a reason per
class. I checked each reason and each is right: none has a single-file witness.
(§21.7 does not name `[R-WRT-05]`, `[R-WRT-07]`, `[R-WRT-09]`, `[R-LIF-02]`'s
barriers, `[R-LIF-04]` or `[R-CNT-10]`, but §21.1 calls §21.7 "the account, **by
class**, of what fails it", and each of those falls inside a class §21.7 does
name — properties of a file's history or of a relation between two files. Not a
defect. I record it so the next reader does not have to redo it.)

### 4.2 Boundary values

- **128-byte floor.** Built. Every gate passes. 127 bytes -> F5.
- **dir_length = 4** (empty record sequence). Conforming; Appendix A. **3** -> F16.
- **dir_offset = 16.** Conforming. **15** -> F9.
- **dir end == F-64 exactly** (zero pad). §6.2: "a writer that ends its
  directory on a 64-byte boundary leaves none." Conforming.
- **generation = 1** OK; **0** -> F11; **2^63 - 1** OK and §9.3's Note says the
  file admits no further commit; **2^63** -> F2.
- **file_id.** I checked deliberately whether the u64 domain rule bites here.
  `[R-ENC-03]` bounds "every offset, length, extent, and count"; file_id is none
  of those, §6.2's table constrains it only as `!= 0`, and F2's instance list
  omits it. So a random 64-bit draw (§9.3) is legal above 2^63 - 1, which it must
  be, and Appendix G item 2's "digest's last eight bytes read little-endian" is
  consistent. **Closed, and closed correctly** — this is a place a naive
  implementation would wrongly reject half of all conforming files.
- **entry_count = 0.** Extent slot (0,0), crc_of_crc_array 0, zero segments,
  zero-byte CRC array whose CRC is 0. Self-consistent (§15.4's third example
  states it). **entry_count > 0 with slot (0,0)** -> L22.
- **entry_count = 2^63 - 1** with T = 1, d = 1: N is in domain, but
  `entry_count x 20 + ceil(entry_count/2^16) x 4` overflows -> L2 via
  `[R-ENC-04]`. The Note in §11.2 about avoiding `(E+T-1)/T` is also correct:
  E = 2^63 - 1, T = 2 would overflow the idiom's numerator but not the stated
  form.
- **A = 512** (floor) and **A = 2^62** (ceiling) legal; 256 or 2^63 -> L39.
  I worked out that A = 2^62 admits exactly **one** legal offset (2^62 itself;
  0 is barred by T8, 2^63 is out of domain by T11), so such a layer can store at
  most one tile. That is a consequence, not a defect — both verifiers agree —
  and the file is ~4 EiB so it is not constructible. Recorded as colour.
- **A_slab = 1** legal (§16.2's Note names it: "contiguity-only"). **0 with
  S != 0** -> L29. **Nonzero with S = 0** -> L28.
- **S = 1** legal (every run is one ordinal, so packing is vacuous and only
  alignment binds). **S > N** legal ("the final run of a block can cover fewer
  than S ordinals").
- **Zero-extent dimension.** G = 0, N = 0, addressed-tile count 0 (interleaved)
  or C x 0 = 0 (planar); index empty; reads return no samples. `[R-GEO-02]`,
  §21.6. I checked that P = prod T_i >= 1 always, so no zero-P degeneracy.
- **Tile entirely padding.** Not constructible: E_i > (G_i - 1) x T_i by the
  definition of ceiling division, so every addressed tile holds at least one
  real position along every axis. Good — §14.5 never has to define an all-fill
  tile that must nonetheless be stored.
- **Decoded size 1 byte.** Planar bool with P <= 8. Under codec 3 this forces a
  single-segment frame (the Window_Descriptor cannot express below 1 KiB) and
  §17.2's Note says exactly that, naming 18, 30 and 2 as the worked cases.
- **lz4 cap.** Decoded size exactly 0x7E000000 legal ("exceeds"); one more ->
  L44. Quantified over *addressed* tiles, so an empty layer escapes it (§17.2's
  Note), but `[R-ENC-04]` is not so quantified and P·Q is still checked there.
  The Note says this in terms. I could not find daylight between them.

### 4.3 Two structures claiming the same bytes

I enumerated every pair of claimant kinds and found the partition total:

- two stored extents of one layer, or a stored extent against its own layer's
  index region or sub-record extents -> **L18**, reject-layer;
- anything else — across two layers, a layer structure against the directory or
  a non-layer record's extent, or two non-layer structures -> **F33**,
  reject-file;
- a claimant reaching [0,16) or [F-64,F) -> caught earlier by the bounds rows,
  and F33's own condition text says so and names them (F9/F10, F31/F32,
  L16/L17, T8/T9).

I specifically checked the case I expected to be missed: **a stored extent
overlapping its own layer's record header or inline payload.** Those bytes lie
inside the directory region, and §9.7 says "A record is not a claimant of its
own — its header and inline payload lie inside the directory region, which is
the claimant covering them". So the overlap is against the *directory*, a
file-scope structure, and it is reject-file, not reject-layer. Explicitly
handled. I also checked **two unknown MU=0 records with the same extent slot**
(multiplicity is unconstrained for unknown types) — two claimants, neither
belonging to a layer -> F33.

**Zero-length structures.** None exist: a stored extent with length 0 is T10, a
record extent slot with one half zero is F30/L15, (0,0) is "no extent" and
claims nothing, and dir_length >= 4. So the partition has no degenerate member.

### 4.4 Every reserved / unknown / experimental value in every position

I walked §10.2's table against the eight defining sections and found no
divergence in any range boundary. Then, per position:

- **Record type, top level.** Reserved 0x0003-0x7FFF: F36 (verifier) always,
  F35 (reader, reject-file) additionally when MU=1; §21.1 names F35 as a
  specialization of F36. Experimental >= 0x8000 with MU=0: conforming, ignored,
  preserved per PE (§21.6). Experimental with MU=1: **conforming file that a
  reader is obliged to refuse** — §21.6's closing paragraph names it as one of
  exactly two such cases, and a verifier that does not implement the type
  reports *cannot establish* per `[R-CNF-11]`. Type 0: F24, never "unknown".
- **Record type, sub-record.** Same values, but reject-*layer*, and
  `[R-CNT-18]` adds "where the file is otherwise conforming a reader MUST NOT
  reject the file for it". §21.6 calls the qualifier load-bearing. L24/L25.
- **Layout 0 and 3-255** -> L36. No experimental range (u8 too narrow) —
  §10.2 states it.
- **Linearization 0, 2-3, 4-0x7FFF, >= 0x8000** -> L33, four instances.
- **Sample type 0, 14-19, 20-0x7FFF, >= 0x8000** -> L34, four instances.
- **Codec 0, 5-0x7FFF, >= 0x8000** -> L43. **Filter 0, 3-0x7FFF, >= 0x8000** -> L45.
- **index_encoding 0, 2-0x7F, >= 0x80** -> L31.
- **Metadata encoding 0 and 3-0x7F** -> R1, ignore-record, *a violation*.
  **>= 0x80** -> §21.6, ignore-record, **not** a violation, certification
  unaffected. That asymmetry is stated three times (§21.5's preamble,
  `[R-MTA-10]`, §21.6's row) and is consistent in all three.
- **Record flag bits.** All sixteen combinations of bits 0-1 on both registered
  types, and any of bits 2-15: MU=1/PE=0 -> F25/L46; reserved bit set ->
  F26/L47; stored bits differing from §7.3's registry -> F28/L49. A layer record
  with flags 0x0001 exhibits L46 and L49 together; both are verifier,
  reject-layer, certification, so no fork. Readers apply the fixed semantics
  regardless (`[R-CNT-22]`), which I checked against §20.4's flag-authority
  table: registry flags for registered types, the implementer's definition for
  an implemented unregistered type, stored flags only for an unimplemented type.
- **Trailer flags.** Any incompat bit -> F19. Any ignore-lane bit -> conforming,
  ignored, copied forward by updaters and compactors (§6.3, `[R-WRT-06]`).

### 4.5 The reader/verifier seam

I built the sharpest version of this I could: take my base file and move the
stored tile into the pre-trailer pad, at offset 340 with length 20 inside
[337,384). Then:

- T8 does not fire (340 >= 16), T9 does not fire (360 <= F-64 = 384), the
  entry's crc still matches, the decoded length is still right. **No
  reader-detected violation exists.**
- F7 fires (a structure between the directory's end and the trailer), verifier,
  reject-file.

So a conforming reader serves the tile and a conforming verifier rejects the
file. That is the seam — and §6.2 states it in terms: "readers check neither,
their check being the dir-bounds rule of `[R-CNT-06]`". `[R-RDR-02]` and
`[R-CNF-12]` between them make the reader's behaviour correct and the
verifier's verdict correct. **Not a fork**: the two actors have different
obligations by design, and the document says so where the case arises.

I ran the same test on every verifier-only row (F7, F25-F28, F33, F36, L18,
L25, L40-L42, L46-L49, T2, T4, T5, T26) and in each case found the reader-side
clause: §14.5 for T4/T5, `[R-SER-08]` for T2, §16.1/§16.2 for L40-L42,
`[R-CNT-22]` for F28/L49, `[R-MTA-05]` for F27/L48, `[R-CNT-13]`'s parenthetical
for F33/L18, `[R-CNT-12]` for the flag rows, `[R-CNT-15]` for F36/L25. §21.1's
closing paragraph enumerates the ones where the reader is obliged to *serve the
structure unchanged* and names `[R-SER-08]` as the one rule that goes the other
way. I could not find a verifier-only row without a stated reader side.

### 4.6 Two verifiers, same file, different verdict

This is the charter, so I pushed hardest here.

Every divergence I could build reduced to one of three **designed** ones:

1. **capability** — a verifier that cannot execute a codec or filter
   (`[R-COD-11]`), does not implement a format major, or does not implement an
   MU=1 record type reports *cannot establish*. `[R-CNF-11]` lists these.
2. **resource** — a verifier that declines a tile's or layer's decode, or a
   user-metadata document's decode, on a bound of its own, reports *cannot
   establish*. Crucially the bounds are floored: `[R-ERR-04]` says a reader that
   declines a within-guarantee file "on that ground" is not conforming, and
   `[R-MTA-09]` says the document bound is "no smaller than §21.9's
   user-metadata guarantee" and the window bound "no smaller than §21.9's
   guarantee for that quantity". **So for any file within §21.9's table, every
   conforming verifier must actually look, and their verdicts must agree.** That
   floor is what closes the whole class, and it is the thing the changed passage
   in §18.2 supplies for metadata documents.
3. **early stop** — `[R-CNF-11]` lets a verifier stop at the first violation,
   which changes the *report* (unexamined scopes, a partial slack total) but
   never the verdict, because "An established violation takes priority".

And in no case can a decline produce a *certificate*: "a verifier MUST NOT
certify a file it reports that way", and §9.7 adds "a verifier MUST NOT certify
past a violation it has not looked for". I tried to find a decline that
*licenses* certification and found exactly one — `[R-MTA-10]`'s unassigned
metadata encoding — and there the document is explicit that nothing is left
unchecked because no rule attaches. That is a real answer, not a dodge.

The one place where I could not close the loop from this document alone is the
Frame_Content_Size of an encoding-2 metadata document. That is finding
adversary-01.

I also checked the arithmetic of the one report-level divergence:
`[R-CNT-21]`'s partial slack total. partial = F - bytes(enumerated claimants);
true = F - bytes(all claimants); enumerated is a subset, so partial >= true.
The document's claim "an upper bound on the file's true slack, never an
under-count" is correct. And the front block and live trailer are claimed by
the walk (`[R-LIF-08]`), so partial <= F - 80. Both hold on my base file.

### 4.7 Interactions between individually well-specified features

- **Sparse tile under a filter chain.** A sentinel entry short-circuits steps 5
  and 6 of §19.4 — no payload, no decode, so no filter runs. `[R-TYP-09]` bars
  fill for any non-sentinel failure. Closed.
- **Empty layer under a limit.** `[R-COD-07]`'s lz4 cap is quantified over
  addressed tiles and an empty layer has none; `[R-ENC-04]` is not so quantified
  and still binds P·Q. §17.2's Note states both halves. Closed, and this is
  exactly the sort of quantifier seam I expected to find open.
- **Empty layer with a slab or alignment declaration.** No runs, no stored
  tiles, invariants vacuous. Conforming.
- **Compaction over a record the compactor cannot read.** `[R-WRT-06]` bars
  compaction on *any* unimplemented MU=1 record, at either scope. §20.4's table
  row says "Compaction is barred on the same ground" in a sentence about file
  scope, which reads narrower — but I checked that it makes no difference:
  compaction regenerates every layer's index region and re-points its extent
  slot, which *is* modification of that layer, and §20.4's layer-scope sentence
  bars modifying a layer governed by an unknown critical record. Both readings
  refuse. Closed by accident rather than by design, but closed.
- **Compaction of a slab- or alignment-declared layer.** A compactor may not
  clear the declaration (`[R-WRT-05]` byte-identity; `[R-WRT-07]` licenses only
  extent slots, regenerated index regions and crc_of_crc_array), so it must
  honour the invariant — and §20.5's first sentence says exactly that: "free to
  place structures anywhere §5.2 admits and **every declared layout invariant
  permits** (`[R-SLB-01]`, `[R-SLB-03]`)". I checked the pathological
  consequence (a layer with A = 2^30 and five stored tiles forces a >= 5 GiB
  output, so compaction can reclaim nothing) — conforming, and both verifiers
  agree.
- **Compaction meeting a structurally-bad index entry.** §20.5 spends a
  paragraph on this: the entry has no stored extent to re-point, so regeneration
  cannot proceed, and `[R-WRT-06]` obliges refusal because no drop is available
  for an index entry. Closed in terms.
- **A commit that re-declares a channel's type at the same element size.** I
  worked this one carefully. §20.3 step 4's bar names padding set, padding
  content, decoded size, sample byte offsets, codec and filter — and says "the
  list names where that effect arises rather than standing on its own". Test
  cases: planar uint8 -> bool changes the decoded size from P to ceil(P/8), so
  the list catches it. **Interleaved uint8 -> bool** changes nothing on the
  list, but §14.2/`[R-SER-08]` fixes an interleaved bool byte to 0x00/0x01, so
  a stored 0x42 becomes nonconforming — and the non-exhaustive phrasing ("what
  §14 fixes for its stored bytes") catches it, with T2 as the witness. §21.7
  names "a boolean byte" as exactly one of the three places the bar is
  witnessed. Closed, and this is the tightest interaction in the document.
  int32 -> float32 at the same width reaches no byte §14 constrains and is
  permitted and unwitnessed, which is consistent with `[R-TYP-04]`'s "a sample
  value is its bit pattern".
- **Filter 2 on a packed bool plane.** s = 1, identity; L divisible by s
  trivially. On an interleaved single-byte layer, Q = 1, identity. On a planar
  int8 plane, B = 1, identity. `[R-COD-10]`'s "L is divisible by s in every
  case" holds for all three of §14's decoded-size formulas: P·B_c / B_c,
  P·Q / Q, ceil(P/8) / 1.
- **A point request vs a 1-wide region request** at a coordinate outside the
  extents: the first fails as a request, the second succeeds returning no
  samples. §19.4 step 1 defines the distinction explicitly ("a range whose every
  interval holds a single position is a region request"), so this is deliberate,
  not a seam.

### 4.8 Modal-keyword sweep (the round-17 and round-18 shapes)

I grepped every lowercase `must`, `shall`, `should`, `may not`, `required to`,
`ought to` in the document. Five hits:

- lines 614, 1285, 1871, 2313 — all inside `>` blocks labelled Example, Note or
  Note, hence non-normative under §2.1's carve-out. No normative work done.
- line 3585 — "the diagnostic ought to distinguish the two", in §21.6's prose.
  Normative text, no BCP 14 keyword, so no force — but the sentence only
  concerns diagnostics, which §2.4's Note already declares implementation
  technique. Harmless.

**No lowercase modal is carrying normative weight.** I then looked for the
converse shape — a rule stated declaratively with no keyword at all — and found
the interesting cases to be `[R-COD-05]` (codec 2) and `[R-COD-07]`'s first two
sentences (codec 4), both of which state a format requirement with no MUST for
either actor. I chased both:

- **[R-COD-05]**, "The stored bytes are exactly one DEFLATE compressed data
  stream ... raw, not a zlib (RFC 1950) or gzip (RFC 1952) wrapper." T15
  addresses this head-on: "the check that detects it is T24's or T25's, and this
  row records the cause rather than a procedure of its own". I checked the
  detection by hand. A gzip member begins `1F 8B`; 0x1F is 0001 1111, so
  BFINAL=1 and BTYPE = bits 1-2 = 11 = reserved -> T25 fires. A zlib stream
  usually begins `78 9C`; 0x78 is 0111 1000, so BFINAL=0 and BTYPE=00 = stored
  block, whose LEN/NLEN complement check then reads the FLG byte and fails ->
  T25, and the trailing Adler-32 would trip T24 in any case. In the residual
  case where a byte string parses as one raw DEFLATE stream consuming the extent
  exactly and producing the decoded size, those bytes simply **are** one raw
  DEFLATE stream, and file conformance is a pure predicate on bytes
  (`[R-CNF-02]`) — the "not a zlib wrapper" clause is descriptive of the same
  fact, not an independent test. No fork.
- **[R-COD-07]**, "The LZ4 frame format is not used." T23 delegates to T25. I
  checked: the frame magic `04 22 4D 18` read as an LZ4 block gives token 0x04
  (literal length 0, match length 8), then match offset `22 4D` = 19,746 with
  zero bytes produced -> invalid match -> T25 fires. Detected.

Both closed. Recording the negative because the shape is the one this project
has been burned by twice.

### 4.9 Things I confirmed are deliberately free, and are pairwise identical

Files one bit apart that are both conforming and behaviourally identical:
version_minor (`[R-ENC-16]` makes it the only descriptive field; §21.6 accepts
any value); any ignore-lane flag bit; any slack byte, including the pre-trailer
pad; a raw DEFLATE stream's unused final-byte high bits (§17.2's Note is
explicit that "two files differing only in those bits ... are both conforming");
zstd Frame_Content_Size present or absent on a tile; file_id above 2^63 - 1;
record order and sub-record order (`[R-CNT-14]`); structure placement absent a
declaration (`[R-SLB-05]`). Appendix G's list of what the reproducible profile
must pin matches this set item for item, which is a good cross-check on it.

Files one bit apart with **different** verdicts, where the boundary is exactly
where the document says it is: a sentinel's crc field (0 vs anything -> T6); a
bool fill byte (0x01 vs 0x02 -> L35); an interleaved bool value byte at a real
position (0x01 vs 0x02 -> T2); a trailer reserved byte (F15); a record reserved
flag bit (F26/L47); the front block's bytes [8,16) (F6).

---

## 5. Findings

### adversary-01 — AMBIGUITY

**Location.** §18.2, `[R-MTA-09]`; §21.5 rows R3 and R4; against §17.2's
`[R-COD-06]` and §21.4 row T22.

**Quotation** (§18.2, `[R-MTA-09]`):

> Encoding 2 stores it as exactly one RFC 8878 compressed frame occupying the
> extent's bytes before its terminal CRC, under the frame constraints of
> `[R-COD-06]` that do not reference a tile: the frame magic; no skippable
> frame and no second frame; no nonzero dictionary ID; no content-checksum
> flag. The constraints §17.2 states against a tile's declared decoded size do
> not apply, because a document has no declared size

and, for the tile case it is withdrawing (§17.2, `[R-COD-06]`):

> The frame content-size field MAY be present; when present it MUST equal the
> tile's decoded size, a reader MUST treat a mismatch as a validity error at
> tile scope

**The problem.** For a tile, TARN does not rely on the zstd decoder to police
a lying Frame_Content_Size: `[R-COD-06]` makes an FCS that disagrees with the
declared decoded size a TARN-level violation (T22), so every conforming reader
reaches the same verdict whatever its decoder does. For a user-metadata
document, `[R-MTA-09]` withdraws that constraint — correctly, since there is no
declared size to compare against — and puts nothing in its place. The
carried-over list is closed and enumerated ("the frame magic; no skippable
frame and no second frame; no nonzero dictionary ID; no content-checksum
flag"), and R4's Instances cell enumerates exactly those six alternatives plus
"bytes remaining after the frame". FCS is in neither.

So for an encoding-2 document whose frame declares FCS = 999 but whose decode
produces 100 bytes, the only rule left is R3: "A user-metadata document's
stored bytes fail to decode under its declared assigned encoding". Whether
those bytes "fail to decode" is now a property of the decoder, not of the
bytes — and `[R-CNF-02]` says file conformance "is a pure predicate on bytes:
it does not depend on any reader".

I checked whether anything else closes it and found the opposite:
`[R-SEC-02]` **forces** readers into the position where it bites — "A reader
MUST NOT size an allocation, fetch, or index walk in proportion to a declared
magnitude it has not corroborated against the file's actual length" — so a
reader may not decline on the strength of FCS and must actually decode. I also
checked whether the window rule catches it: it catches only the single-segment
case, where RFC 8878 makes Window_Size equal FCS, so an inflated FCS becomes an
inflated window and `[R-MTA-09]`'s window decline applies. For a frame carrying
a Window_Descriptor, FCS and Window_Size are independent and nothing catches it.

**Permitted readings.** (a) The frame is not "exactly one RFC 8878 compressed
frame" because its FCS is inconsistent with its content, so the stored bytes
fail to decode -> R3 -> ignore-record and the file is **nonconforming**.
(b) TARN imposes no FCS constraint on a document, the bytes decode, no rule is
broken, and the file is **conforming**.

**Which I picked.** (b), on the strength of "The constraints §17.2 states
against a tile's declared decoded size do not apply" plus R4's closed list —
TARN visibly considered which `[R-COD-06]` constraints to carry over and did
not carry this one. But I picked it with low confidence, because reading (a) is
what a strict zstd binding will produce by default without the implementer ever
making a choice.

**What an implementer does wrong without it.** Writes a verifier around a
strict zstd binding and reports *nonconforming* on a file another verifier
certifies, or writes one around a lenient binding and certifies a file another
rejects — with no diagnostic pointing at the disagreement, because both are
reporting the outcome their decoder handed them.

**Byte-level.** Yes, with a named contingency. Verifier A uses a zstd binding
that errors on an FCS/content-length mismatch (the reference implementation's
behaviour is the ordinary case): it reports R3, ignore-record, verdict
**nonconforming**. Verifier B uses a binding that streams to end-of-frame and
does not compare against FCS: it decodes a valid JSON object, finds no
violation, and **certifies**. The differing byte is the Frame_Content_Size
field in the metadata extent's frame header. The fork closes if and only if
RFC 8878 itself makes an inconsistent FCS a malformed frame — which this
document does not tell an implementer, and which for tiles it deliberately did
not rely on. I could not consult RFC 8878 under this round's access rule, and
I am reporting what this document alone decides, which is: nothing.

**Suggested shape of a fix** (offered, not required): say in §18.2 either that
a present Frame_Content_Size MUST equal the document's actual decoded length,
with a row beside R4, or that it is unconstrained and a mismatch is not a
failure to decode within the meaning of R3 — the same move §18.2 already makes
one sentence later for the window ("not a failure to decode within the meaning
of R3").

---

### adversary-02 — OBSERVATION

**Location.** §16.1, `[R-SLB-01]`; against §3.1's definition of *stored* and
§15.3's `[R-IDX-03]`; register row L40.

**Quotation** (§16.1, `[R-SLB-01]`):

> When declared: every stored tile's offset satisfies offset mod A = 0.

**The problem.** §3.1 defines the term the invariant quantifies over: "A tile
is *stored in a generation* if and only if that generation's tile-index entry
for it is not the sentinel (§15)." An entry with offset 5 and length 10 is not
the sentinel, so by that definition its tile is *stored*, and §16.1 read on its
own makes offset 5 fail the alignment invariant -> L40, reject-**layer**.

That is the wrong answer. §15.3's `[R-IDX-03]` says of the six structural rows:

> Such an entry contributes no stored extent to the *verifier* rows, which bind
> over well-formed entries' extents only — `[R-SLB-03]`'s run continuity closes
> over it as it does over a sentinel

and one of §15.3's three *verifier*-marked rows is "alignment or slab invariant
violated (§16)". So a structurally-bad entry is transparent to the alignment
check too, and the damage stays at reject-**tile**.

**Why it is expensive to decide rather than ambiguous.** The answer is in the
document, but reaching it costs three hops from §16.1: follow the parenthetical
"(violation: reject-layer, §15.3)" into §15.3, read `[R-IDX-03]`'s prose above
the table rather than the table, and generalise from a sentence whose only
worked example is `[R-SLB-03]`'s run continuity. Meanwhile §16.2, facing the
identical question one subsection later, answers it in the open and at length —
"So are the entries §15.3 classifies reject-tile on a *structural* ground: they
address no usable extent, and the run's stored tiles close over them" — and
L41's own Condition cell restates it a third time ("sentinels and entries §15.3
classifies reject-tile on a structural ground are transparent, an entry failing
only its stored bytes' crc is not"). L40's Condition cell says none of this; the
transparency is reachable only through the `(R-IDX-03)` citation in its
Governing rule cell. A reader who notices the care §16.2 takes will read §16.1's
silence as meaning the opposite.

**The concrete file.** Layer declares A = 4096. Entry 0: offset 4096, length
100, crc correct. Entry 1: offset 5, length 10 (T8: offset < 16, structural).
Entry 2: sentinel. Verifier A applies `[R-IDX-03]`: entry 1 contributes no
extent, L40 does not fire, the finding is T8 at tile scope and tiles 0 and 2
remain servable. Verifier B reads §16.1 with §3.1: L40 fires, reject-layer, the
whole layer is condemned.

**Byte-level.** No, and I want to be precise about why rather than reach for
it. Both verifiers report **nonconforming** — entry 1 is a T8 violation either
way, so the verdict cannot differ. What differs is the *scope* the verifier
records, and no reader's obligation changes at all, because L40's detector is
the verifier and §16.1 says in terms that "readers are not obligated to —
offsets are always explicit, so alignment is reader-invisible". The cost is
real but bounded: a corpus vector built for L40 under `[R-VEC-02]` and
`[R-VEC-04]` records a scope and an intact sibling, and two implementations
would build and expect different pairs. It does not move the emittable set and
it does not move any accept/reject verdict.

**Suggested shape of a fix**: one clause in §16.1 mirroring §16.2's — "entries
§15.3 classifies reject-tile on a structural ground address no usable extent
and are transparent to this invariant, as sentinels are" — or the same clause
in L40's Condition cell, which is where L41 already carries it.

---

## 6. What I could not determine

- Whether RFC 8878 makes a frame with an inconsistent Frame_Content_Size
  malformed. That is the hinge of adversary-01 and the access rule bars me from
  checking it. I have stated the finding so that it is still useful either way:
  if RFC 8878 closes it, the finding reduces to an asymmetry worth a sentence;
  if RFC 8878 does not, it is a verdict fork.
- Whether a byte string exists that is simultaneously a well-formed zlib stream
  and a raw DEFLATE stream consuming the same extent exactly and producing the
  right decoded size. I argued in §4.8 that it does not matter — such bytes are
  a conforming codec-2 payload either way — but I did not search for one.
- The 2^32-entry and 2^62-alignment cases in §4.2 are arithmetically checked but
  not constructed; the files are 86 GB and ~4 EiB respectively. §24's
  `[R-VEC-03]` already says the tile-count guarantee is exercised by a scaled
  vector with the bound checked arithmetically, which is what I did.

## 7. Overall assessment

I built the minimal file, a one-layer file with a stored tile and a sparse
index, and the arithmetic for a dozen boundary layers, entirely from this
document, and every worked number in it reproduced exactly. The register is
mechanically consistent with its own stated instance rules (121 rows, 273
instances, both matching §21.8). I could not find a detectable file-conformance
violation the register omits. The reader/verifier seam is stated at every row I
tested. The capability/resource seam that the changed passages address is
closed by a floor — every conforming verifier's bound is at least §21.9's
guarantee — which means verifiers cannot disagree about any file within the
table, and that floor is the load-bearing thing the §18.2 edit supplies.

One gap survives, and it is a gap the tile path does not have because §17.2
plugged it there deliberately.
