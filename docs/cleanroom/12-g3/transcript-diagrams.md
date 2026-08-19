# Cleanroom round 12 — Diagram auditor transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,982 lines as it stands on disk; the brief said 3,965 — I did not chase the
difference, and it does not affect anything below). I opened no ADR, no
`docs/`, no `conformance/`, no `spec/registry.json`, no `PLAN.md`,
`AGENTS.md`, `README.md`, or `OPEN-QUESTIONS.md`. I listed no directories. I
ran no `git` command. I ran no web search or fetch.

I ran three things, all local computation, all reading no project file:

1. `wc -l` on the spec.
2. `grep -n` against the spec only (three greps: for `renumber|stable|…`, for
   `register row|…`, and `sed -n` range prints for quotation).
3. Two Python scripts I wrote into my own scratchpad
   (`round12/crc.py`, `round12/count.py`). `crc.py` reads no file — it carries
   the Appendix A hex dump as a literal. `count.py` reads the spec, and only
   the spec, to parse the §21 register tables mechanically.

I wrote this transcript and those two scripts. I read no other file in the
scratchpad and did not list it.

---

## Part 1 — Enumeration of every figure, table, box, worked example and
## checklist, with line numbers

Enumerated before judging any of them, so coverage is checkable. `L` = line
number of the first line of the object.

### Byte-layout / structure tables

| L | Object |
|---|---|
| 668 | §6.1 front signature block layout (Offset / Size / Value / Class) |
| 711 | §6.2 trailer layout (Offset / Size / Type / Field / Class / Valid values) |
| 875 | §7.2 record header layout (Offset / Size / Type / Field / Class) |
| 946 | §7.3 record types of format major 1 (Type / Name / Scope / Flags) |
| 975 | §7.4 layer-record inline payload (Field / Type / Constraint) |
| 1049 | §8.1 checksum coverage map (Structure / Checksum location / Covers) |
| 1511 | §12.1 core sample types (ID / Name / Element size / Definition) |
| 1743 | §14.2 byte layout and decoded size (Layout / Decoded size / Offset of value k) |
| 1906 | §15.1 tile-index region schematic box (entry array + segment CRC array) |
| 1911 | §15.1 index entry layout (Offset / Size / Type / Field / Class / Valid values) |
| 1959 | §15.3 entry-validity classification table (Entry state / Outcome) |
| 2345 | §18.2 user-metadata inline payload layout |
| 2469 | §18.4 standardized keys (Key / Scope / Value) |

### Enumeration / restatement tables

| L | Object |
|---|---|
| 227 | §2.4 outcome classes (Outcome / Meaning) |
| 1316 | §10.2 numeric identifier spaces (Space / Width / Assigned / Reserved / Experimental) |
| 2917 | §20.4 preservation obligations (Stored flags / Updater obligation) |
| 3092 | §21.2 file-scope register, F1–F36 |
| 3136 | §21.3 layer-scope register, L1–L49 |
| 3193 | §21.4 tile-scope register, T1–T26 |
| 3234 | §21.5 ignored-record register, R1–R10 |
| 3252 | §21.6 conditions that are not violations |
| 3347 | §21.9 minimum-guarantee limits |
| 3669 | Appendix A byte-by-byte annotation table |
| 3705 | Appendix B constants |
| 3800 | Appendix E changelog |

### ASCII diagrams / boxes

| L | Object |
|---|---|
| 571 | §5.1 "a file after three commits" region box |
| 1128 | §9.2 "what a crash sees" three-row box |
| 1906 | §15.1 region schematic (also listed above) |
| 2855 | §20.3 example (a), a new layer |
| 2871 | §20.3 example (b), tiles added to an existing layer |
| 2891 | §20.3 example (c), a change confined to the directory |
| 2994 | §20.5 "what compaction reclaims" input/output box |
| 3658 | Appendix A hex dump |

### Worked numeric examples

| L | Object |
|---|---|
| 499 | §4.6 `température` NFC vs NFD byte counts |
| 560 | §5.1 the smallest conforming file, region offsets |
| 1428 | §11.2 grid arithmetic, extents (1024,2048) and (1000,2048) |
| 1482 | §11.4 ordinals, grid (4,8), coordinate (300,700), planar C=4 |
| 1545 | §12.1 bfloat16 1.0 and quiet NaN |
| 1594 | §12.3 a channel entry's twelve bytes |
| 1664 | §13.3 interleaved rgb fill, planar mixed storedness |
| 1785 | §14.2 interleaved (2,3) uint8+uint16, and float32+bool |
| 1819 | §14.3 packed bool plane, P=10, fill false/true |
| 1875 | §14.5 edge tile (5,5)/(4,4), uint16 fill 0xABCD |
| 1999 | §15.4 entry_count = 1,000,000 segment arithmetic |
| 2014 | §15.4 planar C=4 N=32, disk ordinal 74 |
| 2111 | §16.2 slab runs, S=8, A_slab=4096 |
| 2292 | §17.3 byte-shuffle of three float32 |
| 2841 | §20.3 superseding one 100,000-byte tile |
| 3368 | §21.9 note on where the guarantee numbers come from |

### Checklists / profiles

| L | Object |
|---|---|
| 1094 | §9.2 commit protocol, numbered steps 1–6 |
| 1293 | §10.1 the four extension vehicles, numbered 1–4 |
| 2531 | §19.1 open algorithm, numbered steps 1–4 |
| 2655 | §19.4 tile-read algorithm, numbered steps 1–8 |
| 2779 | §20.3 append procedure, numbered steps 1–6 |
| 3760 | Appendix D six design choices |
| 3835 | Appendix G reproducible-writer profile, numbered items 1–10 |
| 3925 | Appendix H conformance checklists, five classes |

That is 8 checklists, 16 worked examples, 8 ASCII boxes, 12 enumeration
tables and 13 layout tables — 57 objects. Everything below is a judgement on
one of them.

---

## Part 2 — What I actually built and computed

### 2.1 Appendix A, byte by byte

I transcribed the hex dump at line 3659 into a literal in `crc.py` and
rebuilt every field from it rather than reading the annotation table, then
compared.

```
file length              = 128                      §5.1 minimum ✓, F mod 64 = 0 ✓
front magic  [0,8)       = 89 54 41 52 4E 0D 0A 1A  §6.1 ✓
front resv   [8,16)      = 8 zero bytes             §6.1 ✓
dir region   [16,20)     = 00 00 00 00
  CRC-32C(zero bytes)    = 0x00000000               §4.5, §7.1 ✓
pre-trailer pad [20,64)  = 44 bytes zero            (annotation says 44)  ✓
trailer      [64,128)
  magic      [0,8)       = 8A 4E 52 41 54 0D 0A 1A  §6.2 ✓
  version_major          = 1                        ✓
  version_minor          = 0                        `[R-CNT-26]` floor ✓
  flags                  = 0x00000000               §6.3 ✓
  generation             = 1                        ✓
  dir_offset             = 16                       ≥ 16 ✓
  dir_length             = 4                        ≥ 4 ✓
  committed_file_length  = 128                      = F, mult of 64 ✓
  file_id                = 0x0123456789ABCDEF       ≠ 0 ✓, LE bytes EF CD AB 89 67 45 23 01 ✓
  reserved   [56,60)     = 00 00 00 00              ✓
  stored CRC [60,64)     = 0xE00938D2
  computed CRC-32C[0,60) = 0xE00938D2               MATCH
  stored bytes           = D2 38 09 E0              = LE of computed ✓
```

Also checked the trailer-bound arithmetic against `[R-CNT-06]`:
dir_offset + dir_length = 20 ≤ F − 64 = 64 ✓.

And the offsets in the annotation table itself: [0,8), [8,16), [16,20),
[20,64), [64,72), [72,74), [74,76), [76,80), [80,88), [88,96), [96,104),
[104,112), [112,120), [120,124), [124,128). Contiguous, non-overlapping,
covering exactly [0,128). No gap, no duplicate. Every "Meaning" cell matches
the field the offset lands on in §6.2's layout table.

Appendix A is byte-perfect. That is the strongest single result of this walk
and I want it on the record.

### 2.2 The other two fixed constants

- CRC-32C(`"123456789"`) computed = `0xE3069283`. §4.5 says `0xE3069283`. ✓
  Byte order `83 92 06 E3` ✓.
- CRC-32C of 2¹⁶ sentinel entries (65,536 × `FF ×16 00 ×4` = 1,310,720
  bytes) computed = `0xEECB3BB2`. §15.4 and Appendix B say `0xEECB3BB2`. ✓

I computed the CRC with a bit-at-a-time reflected implementation using
0x82F63B78 (the reflection of 0x1EDC6F41), init 0xFFFFFFFF, final XOR
0xFFFFFFFF — i.e. built from §4.5's parameters, not from a library
constant — so the check vector is doing real work here.

### 2.3 Every worked example's arithmetic, redone

I did not eyeball any of these.

- **§4.6 `température`.** `74 65 6D 70 C3 A9 72 61 74 75 72 65` decodes to
  t,e,m,p,é,r,a,t,u,r,e = "température", 11 code points, 12 bytes, prefix 12 ✓.
  NFD replaces `C3 A9` with `65 CC 81`: 13 bytes ✓.
- **§5.1 smallest file.** [0,16)+[16,20)+[20,64)+[64,128) = 128, and 64−20 = 44 ✓.
- **§11.2.** ⌈1024/256⌉=4, ⌈2048/256⌉=8, N=32, P=256·256=65,536 ✓.
  ⌈1000/256⌉=4 ✓ (3.906…).
- **§11.4.** s = Σ tᵢ·∏_{j>i}Gⱼ; d=2 gives s = t_y·8 + t_x. (0,0)→0,
  (0,1)→1, (1,0)→8 ✓. (300,700): tile (1,2), s=10 ✓; in-tile (44,188),
  ordinal 44·256+188 = 11,452 ✓. Planar C=4: 2·32+10 = 74 ✓.
- **§12.1 bfloat16.** binary32 1.0 = 0x3F800000; high 16 bits 0x3F80;
  LE bytes `80 3F` ✓. 0x7FC0 ↔ 0x7FC00000 quiet NaN ✓.
- **§12.3 channel entry.** 1+4+2+1+4 = 12 bytes; `04` `74 65 6D 70`
  `0C 00` `04` `00 00 C0 7F` ✓ — type 12 LE, fill LE of 0x7FC00000 ✓.
- **§13.3.** fills FF/00/00 → (255,0,0) ✓.
- **§14.2.** Q = 1+2 = 3; decoded 6·3 = 18 ✓; ordinal 1·3+2 = 5;
  5·3 = 15 so [15,18) ✓. Planar `b`: 6·2 = 12 bytes, ordinal 5 at
  [10,12) ✓. float32+bool: Q = 4+1 = 5, 6·5 = 30 ✓, ordinal 5 at [25,30),
  `t` 25–28, `m` 29 ✓. The generalisation "channel c at ordinal u sits at
  u·Q + Fᶜ — the table's forms with k = u·C + c" checks: k div C = u,
  k mod C = c ✓.
- **§14.3.** alternating from true: bits 0,2,4,6 set → byte 0 = 0x55 ✓;
  values 8,9 = true,false → byte 1 bit0 = 1 → 0x01 ✓; P mod 8 = 2 so pad
  bits 2–7, six of them ✓; fill true sets bits 2–7 → 0xFC | 0x01 = 0xFD ✓.
  ⌈10/8⌉ = 2 ✓.
- **§14.5.** grid ⌈5/4⌉ = 2 each axis ✓; tile (1,1) covers 4–7 ×
  4–7; only (4,4) is inside extents → 1 real + 15 padding ✓; P = 16,
  decoded 16·2 = 32 ✓; ordinal of in-tile (0,0) is 0 ✓; fill 0xABCD LE =
  `CD AB` ✓.
- **§15.4 first example.** ⌈1,000,000/65,536⌉ = 16 ✓; 15 full = 983,040;
  remainder 16,960 ✓; CRC array 64 bytes ✓; region 20,000,000 + 64 =
  20,000,064 ✓; 999,999 − 983,040 = 16,959, ×20 = 339,180 ✓; array at
  [20,000,000, 20,000,064) ✓; segment 15 at [983,040·20, 20,000,000) =
  [19,660,800, 20,000,000), length 339,200 ≈ 339 KB ✓; one full segment =
  65,536·20 = 1,310,720 = 1.25 MiB ✓.
- **§15.4 second example.** 74·20 = 1,480, so [1,480, 1,500) ✓; channel 3's
  block is [96,128), i.e. entries 96–127, 32 of them ✓.
- **§16.2 example.** N = 32, S = 8 → runs [0,8),[8,16),[16,24),[24,32) ✓;
  under row-major each is one tile row ✓; rows 1–2 = ordinals 8–23 = runs 1
  and 2 ✓; A_slab = 4096 is a power of two in [1,2⁶²] ✓.
- **§17.3 byte-shuffle.** 1.0f/2.0f/3.0f LE = `00 00 80 3F 00 00 00 40
  00 00 40 40` ✓. s = 4, n = 3, output[i·n + j] = group j byte i gives
  `00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40` ✓ — exactly the printed
  `00 00 00 00 00 00 80 00 40 3F 40 40`, and the prose gloss matches.
- **§20.3 supersede example.** 32·20 + ⌈32/65,536⌉·4 = 640 + 4 = 644 ✓;
  "one entry re-pointed, 31 byte-identical" ✓.
- **§21.9 note.** 2³²/2¹⁶ = 2¹⁶ segments × 4 = 2¹⁸ = 256 KiB ✓;
  2³⁶/2¹⁶ = 2²⁰ × 4 = 4 MiB ✓; 65,536 × 200 B = 13,107,200 = 12.5 MiB ✓.
- **§20.3 note.** 10⁶ × 20 ≈ 20 MB ✓.
- **§24 `[R-VEC-03]`.** 2³² × 20 = 85.9 GB — "tens of gigabytes" ✓.
- **§17.2 note.** §14.2's examples give 18 and 30 (also 12, uncited but
  harmless); §14.3's gives 2 ✓. All below 1 KiB, so the single-segment
  argument holds.

Every number in every worked example is correct. I found no arithmetic
error anywhere in the document.

### 2.4 The §21 register, counted mechanically

`count.py` parses the four register tables as markdown, checks the row-ID
sequence, and counts instances by §21.1's own stated rule ("Instances within
a cell are separated by semicolons, and a cell reading — is one instance").

```
§21.2  F1…F36   36 rows,  53 instances   (header claims 36 conditions) ✓
§21.3  L1…L49   49 rows, 106 instances   (header claims 49 conditions) ✓
§21.4  T1…T26   26 rows,  45 instances   (header claims 26 conditions) ✓
§21.5  R1…R10   10 rows,  44 instances   (header claims 10 conditions) ✓
                121 rows, 248 instances
§21.8 claims:   121 conditions over 248 instances                      ✓
```

No gaps, no duplicates, no out-of-order IDs in any of the four sequences.
Both of §21.8's numbers are exactly right. Given that §21.1 makes the count
"mechanical once the cell is written", this is a checkable claim and it
checks.

I also audited the instance cells against §21.1's own discipline —
"where a condition is a single predicate over several fields … the fields it
reads are not instances". F25 (MU=1 with PE=0) is one instance; F10
(dir_offset + dir_length vs F−64) is one; T12 (offset + length overflow) is
one; F30 and T7 (exactly one half of a pair) are two apiece because two
distinguishable files exist. F28 has two instances (one container, two
alternatives) while L49 has four (two containers, two alternatives), and F26
has one while L47 has two, on the same container logic. Consistent
throughout.

Detection points: every §21.5 row is "extent use" except R1, which is
"open (top-level); layer access (sub-record)" — correct, since R1 reads the
inline encoding byte and not the extent. L3/L5/L6 are "open" while
L4/L7/L8 are "layer access" — correct, because §19.1 step 4 parses the layer
record's *name* at open to build the namespace, and dimension/channel names
are only reached at §19.3. L37/L38 are "tile use" with layer-scope outcome —
matching `[R-RDR-02]`'s explicit carve-out ("index-chain failures take layer
scope although their detection point is tile use").

Specialisation claim in §21.1 (F1 of F6 and F8, F35 of F36, L24 of L25):
verified. F1's two instances are byte-reversed constants, which are strict
subsets of "not byte-identical" (F6) and "not exactly the magic" (F8). F35
is F36 restricted to MU = 1. L24 is L25 restricted to MU = 1. And T11 says
"the value being distinct from the all-ones sentinel", which keeps T11
disjoint from T6/T7 rather than overlapping them.

### 2.5 Building a file with a layer, to find where I would have to guess

Appendix A's annotated file has no layers, so I built one on paper to
exercise §7.4, §11, §14, §15 and §9.2 end to end.

Layer `a`: interleaved (layout 1), linearization 1, codec 1, filter 1,
A = 0, S = 0, A_slab = 0, d = 1, C = 1, dimension `x` E=4 T=2, channel `v`
type 6 (uint8) fill `00`.

```
G₀ = ⌈4/2⌉ = 2 ; N = 2 ; P = 2 ; addressed tiles = N = 2 (interleaved)
entry_count = 2
index region length = 2·20 + ⌈2/65536⌉·4 = 44                  (`[R-CNT-17]`)
Q = 1 ; decoded size per tile = P·Q = 2                        (§14.2)
codec 1 ⇒ each entry's length must equal 2                     (`[R-COD-04]`)

layer-record inline payload, packed in §7.4 table order:
  name          01 61                                    2
  layout        01                                       1
  linearization 01 00                                    2
  codec         01 00                                    2
  filter        01 00                                    2
  A             00×8                                     8
  S             00×8                                     8
  A_slab        00×8                                     8
  rank d        01                                       1
  C             01 00                                    2
  dim entry     01 78 | E=4 (u64) | T=2 (u64)           18
  chan entry    01 76 | 06 00 | 01 00                    6
  index_encoding 01                                      1
  entry_count   02 00 …                                  8
  crc_of_crc_array (u32)                                 4
                                                    total 73
record header 24 B: type 0x0001, flags 0x0003 (MU bit0 | PE bit1),
  inline_length 73, extent slot → index region, extent_length 44
directory = 24 + 73 + 4 (CRC) = 101 bytes

placement: front [0,16); tile0 [16,18); tile1 [18,20); index [20,64);
dir [64,165); pad [165,192); trailer [192,256); F = 256, F mod 64 = 0 ✓
dir_offset + dir_length = 165 ≤ F − 64 = 192 ✓
```

Guesses I had to make: **none.** Every width, order, and derived length is
pinned. In particular:

- flags = 0x0003 is forced by §7.3's fixed MU/PE, §7.2's bit assignment, and
  §4.4's bit-0-is-LSB rule. Three sections, no gap between them.
- Whether `dir_length` includes its own CRC: §7.1 settles it ("Its final 4
  bytes are a CRC-32C over the preceding dir_length − 4 bytes").
- Whether `extent_length` of the index includes the segment CRC array:
  `[R-CNT-17]`'s formula settles it.
- Whether the pad is 0 or 64 bytes when the directory already ends aligned:
  §6.2 settles it ("a writer that ends its directory on a 64-byte boundary
  leaves none").
- d = 1 ordinals: §11.4's empty-product convention settles it explicitly.

That is the result the gate asks for and I want it stated plainly: the
normative container-plus-layer path is buildable from this document alone,
with no guessing. Everything I report below is at the periphery.

### 2.6 Cross-table consistency sweeps that passed

I checked these and found nothing, and record them so the coverage is
visible rather than implied.

- **§10.2's eight identifier spaces** against §7.3, §14.1, §11.4, §12.2,
  §17.2, §17.3, §7.4/§15.1, §18.2. Every Assigned/Reserved/Experimental
  triple matches the owning section, including the two spaces with no
  experimental range. Appendix C's snapshot matches all eight.
- **§12.1's thirteen types** against §12.2's value set, Appendix C's list,
  Appendix C's pinned reservations (14/15 OFP8, 16/17/18 int128/uint128/
  float128, 19 opaque) against §12.2's note. All match; "exactly thirteen"
  is thirteen rows.
- **§8.1's coverage map** against §4.5's prose. Three terminal checksum
  fields (trailer, directory, user-metadata extent) and three interior ones
  (segment CRC array, entry crc, crc_of_crc_array) — exactly as §4.5
  enumerates, and each interior one is in fact covered by exactly one
  further checksum in the map.
- **§15.3's classification table.** Eleven rows: six marked *structural*
  (the prose says six), three marked *verifier*, plus the valid sentinel
  and the crc-failure row. Count and marking both correct. Mapped
  one-to-one onto T6, T7, T10, T8, T11, T9+T12, T1, and onto L18/F33 and
  L40/L41/L42.
- **§2.4's five outcome rows** against §21.2–§21.5's four headers and the
  preserve-verbatim/§20.4 table cross-reference.
- **§21.9's eight guarantees** against Appendix B's "Reader minimum
  guarantees" row: rank 32, C 4096, entry_count 2³², 65,536 layers,
  16 MiB directory, 256 MiB tile, 16 MiB metadata document, 8 MiB zstd
  window. Identical, in the same order.
- **§21.9's hard-limit list** against §4.6, §7.4, §16.1, §16.2, §17.2,
  §5.1, §6.2. Every bound restated correctly.
- **Appendix B's other 24 rows** against their cited sections. All correct,
  including the two CRC constants I recomputed.
- **§18.4's six keys** against Appendix C's six.
- **Numbered lists** — §9.2 (6 steps), §10.1 (4 vehicles, matching §4.3's
  four in the same order), §19.1 (4 steps, matching Appendix A's "§19.1's
  four-step open"), §19.4 (8 steps, with step 3's "steps 3 through 6 run
  once per needed entry" consistent with §8.2's chain order), §20.3 (6
  steps, each mapped to the right `[R-LIF-02]` step: 4→steps 1–2, 5→step 3,
  6→steps 4–6), Appendix D (six choices, six bold items), Appendix G (items
  1–10 present), Appendix H (five classes, matching §2.3's five). No item
  out of order, duplicated, or missing.
- **Appendix H's verifier checklist** against every verifier-detected
  register row: F7, F25, F26, F27, F28, F33, F36, L18, L25, L40, L41, L42,
  L46, L47, L48, L49, T2, T4, T5, T26. All twenty are covered by one of its
  clauses; none is claimed that the register does not assign to a verifier.
- **§20.3's three shapes** against the rules: (c)'s three cases (clearing a
  slab declaration, renaming a layer, changing fill on a layer with no
  padding position and no pad bit) are each genuinely directory-only under
  `[R-SLB-04]`, `[R-WRT-05]` and `[R-SER-05]`, and (c)'s carve-out for user
  metadata ("its document lives in an extent, so a new extent is appended")
  is right.
- **§9.2's crash box and §20.5's compaction box** — both consistent with the
  prose around them; §20.5's box correctly shows file_id changing X→Y and
  generation 7→1, matching `[R-WRT-06]`.
- **`[R-ENC-16]`'s claim that version_minor is the only descriptive field**
  against every Class cell in every layout table (§6.1, §6.2, §7.2, §15.1,
  §18.2). Holds — and holds only because §4.7 says "conforming reader **or
  verifier**", which is what keeps the trailer's reserved bytes and the
  record reserved flag bits on the structural side. That is a careful piece
  of drafting and it survives.

---

## Part 3 — Findings

Ten findings. None of them forks the bytes; I say why in each. I looked hard
for one that did — §2.5 above is the search — and did not find one.

---

### diagrams-01 — CONTRADICTION — the front matter and §4.7's note give
### different column sets for layout tables, and two of the tables give a third

**Location:** front matter (lines 14–18), §4.7's presentation note (lines
522–532), §6.1 (line 668), §7.2 (line 875).

**Quotation (front matter):**

> On-disk structures are presented as offset/size/type/name/valid-range
> tables. Every field is classified as **structural** (its value affects
> where a byte lies, how it decodes, what a decoded value is, or whether the
> file is accepted) or **descriptive** (none of those — §4.7).

**Quotation (§4.7's note):**

> **Note.** Layout tables for fixed-layout structures give, per field: byte
> offset within the structure, size, type, name, taxonomy class, and valid
> range.

The front matter names five columns and omits taxonomy class; §4.7's note
names six and includes it. They are describing the same tables.

Then neither description is delivered by two of the tables. §6.1's front
signature block table has columns `Offset | Size | Value | Class` — no type
column and no name/field column. §7.2's record header table has `Offset |
Size | Type | Field | Class` — no valid-range column; its ranges are folded
into the Field cells ("type (0 invalid)", "bits 2–15 reserved"). Only §6.2,
§15.1 and §18.2 deliver all six. §7.4's table is legitimately exempt — the
note calls it out by name and its `Field | Type | Constraint` columns are
exactly the promised set minus offset and class.

A second, smaller divergence sits in the same passage pair: the front
matter's definition of *structural* says "whether the file is accepted",
while §4.7's normative text says "whether the file, layer or tile is
accepted at all". The front matter's version is narrower than the rule and
would misclassify, for instance, a layer-record `linearization` value —
which decides only whether a *layer* is accepted.

**Which reading I take:** §4.7's, on `[R-CNF-01]` grounds — the front matter
block is expressly labelled non-normative, §4.7 carries `[R-ENC-16]`, and
§4.7's six-column list is the one the majority of the tables satisfy.

**What an implementer does wrong without it:** nothing to the bytes. The
cost is to a reader building a mental model of the document: a reader who
takes the front matter at its word will not expect a Class column, will not
find it in §6.1 under any of the five promised names, and will not learn
from the front matter that layer- and tile-scope acceptance are structural
grounds too.

**Byte-level:** No. Neither passage constrains a field's value; both describe
how tables are drawn. §6.1's and §7.2's actual field semantics are fully
given in the tables and the prose around them, so no implementation's output
or verdict turns on which column list is right.

---

### diagrams-02 — OBSERVATION — the front matter says vectors cite requirement
### identifiers; §24 has them cite register rows, which nothing makes stable

**Location:** front matter (lines 19–20), §2.2 (lines 116–120), §24
`[R-VEC-02]` (lines 3583–3589), §21.1.

**Quotation (front matter):**

> Normative requirements carry stable identifiers like `[R-IDX-03]`, and
> test vectors cite those identifiers rather than prose positions.

**Quotation (§24):**

> Each vector is one file plus a manifest entry recording, at minimum: its
> identifier; whether the file is **conforming**; the decoded content a
> reader is to return from every scope it can read … and, for each structure
> the file damages, the outcome class (§2.4), the scope, and the §21
> register row it exercises.

§24 requires the manifest to name the **register row** — `F14`, `L22`, `T3`,
`R7` — not the requirement identifier. Row identifiers are a different
namespace from §2.2's `[R-<PREFIX>-<NN>]`, and §2.2's stability guarantee
covers only the latter: "Identifiers are stable: they are never renumbered
or reused, a withdrawn requirement leaves its identifier permanently
retired". I grepped the whole document for `renumber`, `stable`, and
`retired`; the only stability promise is §2.2's, and the only other uses of
"renumber" are about disk ordinals (§11.1, §20.3). §21.1 makes no
corresponding promise about F/L/T/R numbering, and §21.2–§21.5 are dense
enough that an inserted row would renumber every row after it.

So the manifest key that `[R-VEC-02]` and `[R-VEC-03]` actually require is
one the document nowhere pins, while the front matter advertises the one it
does pin. The transitive route back to a stable identifier exists — each
row's Governing rule column names one — but §24 does not require the
manifest to record it.

**Which reading I take:** §24's. It carries `[R-VEC-02]`; the front matter is
non-normative. So a manifest entry that records the row and not the rule is
conforming to §24 and does not do what the front matter says vectors do.

**What an implementer does wrong without it:** an implementer building the
corpus writes `L23` into 248 manifest entries and, on the next round that
inserts a layer-scope row, silently mis-attributes every entry after the
insertion point. `[R-ERR-02]`'s coverage claim would then be unfalsifiable
by inspection.

**Byte-level:** No. This is about the corpus manifest's key, not about any
file's bytes. §24 already says the corpus is derivative and that the
specification governs where they disagree, so no verdict on any file moves.

---

### diagrams-03 — CONTRADICTION — §20.4's own summary sentence is narrower
### than the rule it summarizes, and than Appendix H

**Location:** §20.4 (lines 2923–2924), §20.4's preservation table (lines
2909–2921), §7.3's registry table (line 949), Appendix H (lines 3960–3961).

**Quotation (§20.4):**

> No commit therefore removes a layer record or a file-scope
> user-metadata record.

**Quotation (Appendix H):**

> never removes a layer record, or a
> user-metadata record at either scope (§20.4)

The rule the sentence is summarizing is two paragraphs above it:

> For a type §7.3 registers, the registry's fixed flags govern rather than
> the stored ones (`[R-CNT-22]`) — both registered types carry PE = 1, so
> neither can be dropped, and implementing a record's type confers
> understanding of it, not permission to drop it.

§7.3 fixes type 0x0002 at MU = 0, PE = 1 with scope "file when top-level;
layer as sub-record" — one row, one flag assignment, both placements. So a
layer-scope user-metadata sub-record is as undroppable as a top-level one,
and Appendix H states it correctly. §20.4's "therefore" sentence, which
reads as the complete conclusion of the paragraph above it, names only the
file-scope case. Its supporting rationale reinforces the narrowing — "an
in-place removal would strand *that layer's* stored tiles and index region
as slack" is a layer-record argument, and no argument is offered for the
metadata half.

**Which reading I take:** the wider one. `[R-CNT-22]` plus §7.3's table
decide it unambiguously, §21.1's principle (the rule governs over a
restatement) applies by analogy, and Appendix H agrees.

**What an implementer does wrong without it:** an updater author reading
§20.4 top-down and stopping at its summary sentence concludes that a layer's
user-metadata sub-record may be dropped in any commit, and drops application
metadata that PE = 1 forbids dropping. That is exactly the loss the MU = 0 /
PE = 0 row's SHOULD-report exists to make visible, occurring on a record
where no drop is permitted at all.

**Byte-level:** No. Two competent implementations do not fork here, because
the governing text is explicit and unhedged: "both registered types carry
PE = 1, so neither can be dropped". The summary sentence omits a case; it
does not license the opposite of the rule. This is the register-row pattern
the brief warns about — a restatement that contradicts nothing, only
under-covers — so I flag it as a documentation defect and not as a fork.

---

### diagrams-04 — AMBIGUITY — Appendix G item 2's `file_id` recipe does not
### determine the identifier it promises to make deterministic

**Location:** Appendix G, item 2 (lines 3844–3852).

**Quotation:**

> 2. **`file_id` from a cryptographic hash of the file's own emitted
>    bytes**, computed over [0, F − 64) together with the trailer's
>    other fields with the `file_id` field taken as zero, then written
>    in. Deterministic, and high-entropy

Three things this leaves open, in a profile whose stated job is that "two
conforming writers given the same input" produce identical bytes:

1. **Does "the trailer's other fields" include the trailer CRC?** The CRC at
   trailer bytes [60,64) is a trailer field, and it is not `file_id`, so on
   the plain reading it is included. But the CRC covers [0,60), which
   contains `file_id`, so the value hashed cannot be the final CRC — it can
   only be the CRC of the trailer with `file_id` zeroed. Reading (a): hash
   the 60 pre-CRC bytes with `file_id` zeroed, plus the CRC computed over
   those same bytes. Reading (b): hash only the non-checksum fields, on the
   ground that a CRC is not independent data. The two readings produce
   different digests and therefore different `file_id` values and different
   final trailer bytes.
2. **Which hash?** "a cryptographic hash" names none. Item 1 requires "a
   named codec implementation at a named version", and item 9 requires "a
   named JSON writer at a named version" and "a named zstd implementation at
   a named version" — the profile clearly knows it has to name producers.
   Item 2 does not.
3. **How is a 64-bit `file_id` derived from a digest, and what happens if it
   comes out zero?** Truncate which end, in which byte order? `[R-CNT-06]`
   requires `file_id ≠ 0`, and item 2 offers no fallback.

**Which reading I take:** (b) plus SHA-256 truncated to the low 8 bytes
little-endian, because (b) is the only one where the hashed input is a
function of content alone and does not smuggle in a checksum of a
placeholder — but that is a choice I am making, not one the text makes for
me, and the other reading is equally defensible from the words.

**What an implementer does wrong without it:** two implementations both
claiming Appendix G conformance, on the same input, with codec 1 and every
other item honoured, emit files that differ in trailer bytes [48,56) and
[60,64). The profile's own test — "conformance to the profile can be refuted
cheaply but confirmed only by reproducing the file" — then refutes both.

**Byte-level:** No. Appendix G is labelled non-normative and says outright
"It adds no requirement to any actor: a writer ignoring it is fully
conforming". A conforming writer may emit any nonzero `file_id`, so both
readings emit conforming files and no reader's accept/reject verdict moves.
The divergence is entirely inside the profile's own claim.

---

### diagrams-05 — OBSERVATION — Appendix G item 3 calls itself a total order
### and gives no tiebreak for top-level records sharing an unassigned type

**Location:** Appendix G, item 3 (lines 3853–3870).

**Quotation:**

> 3. **A total emission order, contiguously.** … Records are ordered by
>    type, and within type 0x0001 by layer name; a layer record's
>    sub-records are ordered by type, and within a type by their encoded
>    bytes compared lexicographically — an order a reader can derive,
>    which a creation order is not

At top level the order is: by type, then within type 0x0001 by layer name.
That is total for type 0x0001 (layer names are unique, `[R-ENC-15]`) and
vacuously total for type 0x0002 (at most one, `[R-CNT-14]`). It is **not**
total for any unassigned type. §7.2's multiplicity rules are per type and
constrain only layer and user-metadata records — "in format major 1: any
number of layer records …; at most one file-scope user-metadata record …;
and at most one user-metadata sub-record per layer record" — so a file may
carry three top-level records of experimental type 0x8001, and item 3 orders
neither them nor their extents, which it emits "in ascending record order".

The tiebreak that fixes this is already written six words later, for
sub-records: "within a type by their encoded bytes compared
lexicographically". It simply is not applied at top level.

**What an implementer does wrong without it:** a profile-conforming writer
carrying two unknown ancillary records emits them in whichever order its
record table happens to hold, and a second implementation of the same
profile emits the other order — different `dir_length` layout, different
directory CRC, different `file_id` under item 2, different file. The
profile's headline claim ("closes the degrees of freedom this format
deliberately leaves open") is not met for the one degree of freedom
`[R-CNT-14]` most obviously leaves open.

**Byte-level:** No, for the same reason as diagrams-04: the profile is
non-normative and `[R-CNT-14]` makes both orders conforming. No reader
distinguishes them; §20.4's rationale even relies on that ("as a multiset:
record order carries no meaning").

---

### diagrams-06 — OBSERVATION — §23.2 says a sentinel marks a tile that was
### "never stored"; §3.1 and §20.3 say it marks a tile not stored *now*

**Location:** §23.2 (lines 3530–3535), against §3.1 (lines 302–306) and
§20.3 step 4 (lines 2805–2816).

**Quotation (§23.2):**

> the write footprint
> of every layer at tile granularity, since a sentinel entry (§15.2)
> marks each addressed tile that was never stored, so the index
> publishes which regions were written without disclosing what is in
> them

**Quotation (§3.1):**

> A tile is *stored in a generation* if and only if that
> generation's tile-index entry for it is not the sentinel (§15);
> unqualified *stored* means stored in the live generation.

A live sentinel entry does not mean "never stored". §20.3 step 4 makes the
transition explicit and normative: a commit writes "entries for tiles that
become unstored written as the sentinel". A tile stored in generation 3 and
unstored in generation 7 carries the sentinel in the live index while its
superseded payload sits in the file as slack. Conversely §23.1 is emphatic
that superseding "removes only that data's *reachability*". So the live
index publishes the **live** write footprint, not the historical one — and
§23.2's own closing clause already names history separately ("and the shape
of its own history — generation count, per-commit sizes, and the slack each
commit left behind"), which is where the never-stored question actually
lives.

The restatement is narrower than the fact in a direction that matters for
the section's own subject: read literally, it tells a writer of sensitive
material that a tile it later unstores disappears from the disclosure
surface, when in fact the tile's bytes remain in slack and its earlier
storedness is recoverable by §9.6's probe.

**What an implementer does wrong without it:** a tool that renders "write
footprint" from the live index, and labels the sentinels "never written",
mislabels every tile the file ever unstored. A privacy reviewer using §23.2
as the disclosure inventory under-counts what the file gives away.

**Byte-level:** No. §23.2's sentence is descriptive; the sentinel's
definition, the reject/fill behaviour, and the coverage walk are all
governed elsewhere (§15.2, `[R-TYP-08]`, `[R-LIF-08]`) and are correct
there. Nothing an implementation emits or accepts changes.

---

### diagrams-07 — OBSERVATION — §21.9's "One does not" undercounts its own
### chosen-here hard limits, and the paragraph names the counter-example itself

**Location:** §21.9, `[R-ERR-05]` (lines 3385–3404).

**Quotation:**

> … a user-metadata key at most
> 255 bytes by §18.2's folding of §4.6's name rules onto keys, which
> carry no such prefix; … Most
> follow from a field's width, an external format, or the value
> domain, and the rest from arithmetic over structures a generation
> cannot omit. One does not: the 512 floor on A is a number chosen
> here, fixed at the legacy sector size (§16.1) so that a declared
> alignment is worth declaring.

The 255-byte bound on a user-metadata key is a hard limit — R10 registers
"A user-metadata document key is longer than 255 bytes" as an
ignore-record violation, and §18.2 states it ("every key satisfying §4.6's
name rules — non-empty, at most 255 bytes"). It follows from no field width:
the paragraph itself says keys "carry no such prefix". It follows from no
external format — RFC 8259 bounds no key length. It follows from no value
domain and from no arithmetic over structures. It is a number chosen here,
by §18.2's decision to fold a length rule designed around a `u8` prefix onto
a namespace that has none. So at least two of the listed hard limits are
chosen here, not one.

**The reading that rescues it, stated honestly:** one can say the *number*
255 traces to a field width — §4.6's `u8` prefix — even though the structure
it binds has no such field, and that "follow from a field's width" is
transitive through §18.2's folding. I do not think that survives the
paragraph's own parenthetical flagging the disanalogy, but it is available.

**What an implementer does wrong without it:** nothing directly. The cost is
that a reader auditing which limits are contestable design choices — the
audience §21.9's closing sentence is written for — is told there is exactly
one and stops looking.

**Byte-level:** No. Both limits are stated normatively where their
structures are defined (`[R-SLB-01]`/`[R-CNT-23]` for A, §18.2/`[R-MTA-04]`
and R10 for the key), and §21.9 opens by disclaiming inventory status ("a
finding aid rather than an inventory"). No file's validity moves.

---

### diagrams-08 — OBSERVATION — §5.1's three-commit figure cites the layer-B
### commit as index re-emission at a new placement; §20.3's shape (a) denies it

**Location:** §5.1 figure and caption (lines 571–593), against §20.3 example
(a) (lines 2853–2865).

**Quotation (§5.1):**

> A commit that changes a layer's stored-tile set or index
> content re-emits that layer's whole tile-index region as well, at a
> new placement (§20.3, `[R-WRT-04]`) — the commit that added layer B
> here did exactly that.

**Quotation (§20.3):**

> **(a) A new layer.** Nothing existing is rewritten.

The commit that added layer B is §20.3's shape (a). It emitted B's tiles and
index region for the first time; it re-emitted nothing and relocated
nothing. §5.1's own figure bears this out: its two ▓ runs are identified in
the same caption as "the directories, pads and trailers of commits 1 and 2",
so the figure contains no superseded index region at all — there is no
instance of the rule the caption cites it as an instance of. The rule the
figure does illustrate at that point is the one in the sentence before
("a commit that touches no layer re-emits the directory, the pad and the
trailer alone"), which is commit 3.

`[R-WRT-04]` distinguishes the two cases explicitly — "entries new to this
generation (added tiles, grown extents) emitted per §15" is the addition
path, and "necessarily at a new placement (`[R-LIF-01]`)" is the
re-emission path — so the figure's caption blurs a distinction its own
governing rule keeps.

**What an implementer does wrong without it:** an appender author reading
§5.1 alone may conclude that adding a layer obliges some existing structure
to move, and either relocate an untouched layer's index region — which
`[R-WRT-05]` forbids, "A layer whose record alone changes keeps its extent
slot, pointing at the existing region" and which §5.1 itself calls
compaction's operation two sentences later — or conclude the two figures
describe different operations.

**Byte-level:** No. `[R-WRT-04]` and `[R-WRT-05]` decide what moves and what
does not, in normative text, and both readings of the caption produce
conforming files (placement is free, `[R-SLB-05]`). The defect is that one
figure's caption and another figure's caption classify the same commit
differently.

---

### diagrams-09 — OBSERVATION — §4.7 promises a worked numeric example for
### every non-obvious encoding; the layer record has none anywhere

**Location:** §4.7's note (lines 529–532), §7.4 (lines 969–1025), Appendix A
(lines 3652–3698).

**Quotation (§4.7):**

> Every non-obvious encoding is followed by a worked numeric
> example, and every sentinel or overloaded encoding additionally has a
> paired conformance vector.

The layer record's inline payload is the document's most intricate encoding
and the only one whose parse is driven by counts read out of itself: a
length-prefixed name, nine fixed scalars of four different widths, then `d`
dimension entries and `C` channel entries whose sizes depend on names and
types read as you go, then three more fixed fields, then a nested record
sequence that must consume the remainder exactly. §7.4 gives it a table and
a paragraph of parse rules, and no worked bytes.

Nothing else supplies them either. §12.3's example gives one **channel
entry** — twelve bytes, verified correct in §2.3 above — and that is the
only byte-level example of any part of a layer record in the document.
Appendix A, the one annotated file, "contains no layers". So the document
never shows an implementer a complete layer record, never shows a tile-index
region's bytes in situ, and never shows a directory containing a record.

I verified the parse *is* fully determined — §2.5 above builds a 73-byte
layer-record payload with no guesses — so this is a delivery gap against an
explicit promise, not an ambiguity. But it is the promise most worth
delivering: an implementer who miscomputes `inline_length` by one, or emits
`index_encoding` before the channel entries, gets no check anywhere in this
document.

The second half of the same sentence does hold up: "every sentinel or
overloaded encoding additionally has a paired conformance vector" is
delivered by `[R-VEC-03]`'s "every sentinel, every boundary value, and every
hard limit of `[R-ERR-05]` has one at its stated bound", and the sentinel
and the (0,0) extent slot both get worked bytes in §15.4's examples.

**What an implementer does wrong without it:** builds a layer record and has
nothing to check it against. Every other structure in the format can be
checked byte-for-byte against something in this document; this one cannot.

**Byte-level:** No. §7.4's table order plus "fields are packed in table
order with no alignment or padding between them" fixes the encoding
completely, as §2.5 demonstrates by construction. Two competent
implementations do not fork; they just both work without a net.

---

### diagrams-10 — OBSERVATION — Appendix B and §4.7 claim every named constant
### is collected there, and at least two fixed constants are in neither appendix

**Location:** §4.7's note (line 532), Appendix B (lines 3700–3731),
against §7.1 (lines 852–856) and §13.2/§14.2.

**Quotation (§4.7):**

> All named constants appear once in Appendix B.

**Quotation (Appendix B):**

> Every named constant this specification fixes, collected. Each is
> normative where it is defined; this table is a finding aid.

Two fixed numbers are absent:

1. **The minimum user-metadata extent length, 5.** §7.1 fixes it — "one
   whose extent_length is less than 5 — too short to hold both a document
   and the terminal CRC-32C §8.1 places in its final 4 bytes — is a validity
   error at its containing scope" — and it is cited twice more, by F22 and
   L11. Appendix B lists the exactly analogous bounds for the directory
   ("Directory minimums | dir_offset ≥ 16, dir_length ≥ 4"), so the
   appendix's own precedent is that unnamed numeric floors are in scope.
2. **The boolean byte encodings `0x00` = false and `0x01` = true.** Fixed
   twice — by `[R-TYP-07]` for the fill field ("`0x00` (false) or `0x01`
   (true). Writers MUST NOT emit any other byte") and by `[R-SER-02]` for an
   interleaved in-tile value — and reachable from `[R-SER-08]`, T2, L35 and
   §14.3's bit values. Appendix C does not carry them either: it lists
   identifier-space assignments, and this is not an identifier space.

Both are "named constants this specification fixes" on any reading that
admits the rows Appendix B already has.

**What an implementer does wrong without it:** an implementer using
Appendix B as the constants sheet — which is what §4.7 tells them it is —
has to go back to §7.1 and §13.2 for two values, and an implementer
generating a constants header from Appendix B mechanically will omit them.

**Byte-level:** No. Both constants are stated normatively where their
structures are defined and are enforced by register rows (F22/L11, L35/T2).
Appendix B is explicitly non-normative and explicitly a finding aid.

---

## Part 4 — Confidence

**High**, for the container and array model. I built a two-tile single-layer
file end to end from §7.4, §11, §14, §15, §9.2 and §6.2 without a single
guess, and rebuilt Appendix A byte for byte with an independently
constructed CRC-32C. Both CRC constants and the sentinel-segment constant
reproduce exactly. Every worked example's arithmetic is right — sixteen of
them, all redone by hand or by script. The register's own counts (121 rows,
248 instances) are exactly what its tables mechanically yield, with no gap
or duplicate in any of the four ID sequences.

All ten findings sit in restatements, summaries, captions and the two
non-normative appendices. Not one of them changes which bytes a conforming
implementation may emit or must accept or reject, and I say so in each
rather than hedge — the brief's calibration warns against over-claiming and
I have nothing here that clears the bar. The one place I would most want a
second pair of eyes is Appendix G item 2, because it is the only finding
where two good-faith implementations of a written recipe demonstrably
produce different bytes; it fails the byte-level test only because Appendix G
disclaims normativity in its first paragraph.

**Transcript finding count: 10.**
