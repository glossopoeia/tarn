# Round 8 — Adversary transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,842 lines), in four `Read` calls covering lines 1–3842, plus two `grep`
invocations against that same file (`version_major`, `cannot establish`,
`undetectable|no witness|witness of`, `predicate on bytes|conduct`,
`violation-free|MUST NOT certify|certifies only`) and one `wc -l`.

I opened no other file. No `docs/`, no ADRs, no `PLAN.md`, no `AGENTS.md`, no
`conformance/`, no `spec/registry.json`, no git history, no web. I did not list
any directory.

I ran four local Python programs that read no project file:

- `scratchpad/round8/crc.py` — a CRC-32C implementation from §4.5's parameters,
  used to check §4.5's check vector, Appendix A's trailer CRC, and §15.4's
  all-sentinel segment constant.
- `scratchpad/round8/reg.py` — this one *does* read `spec/tarn.md`; it parses
  §21.2–§21.5's markdown tables and counts rows and semicolon-separated
  instances, to audit §21.8's "125 conditions over 252 instances".
- `scratchpad/round8/build.py` — a TARN writer built from Part I and Part II,
  emitting three files.
- `scratchpad/round8/verify.py` — a TARN verifier built from §19.1, §19.3,
  §19.4, §7, §8, §15 and §9.7, run against the third file. It reads only
  `f3.bin`, which I wrote.

I also wrote `scratchpad/round8/f3.bin` (the attack file) and this transcript.

---

## 1. What I did, in order

I decided at the outset that "narrating each listed section and finding nothing"
was the failure mode the brief warns about, so I set myself a hard target:
**write a byte-exact TARN writer and a byte-exact verifier from the document
alone, and record every point where I had to guess.** If the document is
implementable cold, the guesses are the findings. If it isn't, the gaps are.

Order of work:

1. Read the whole document.
2. Verify every published constant and every worked example arithmetically.
3. Audit §21.8's instance arithmetic mechanically.
4. Build a conforming empty file, a conforming one-layer-no-tiles file, and a
   conforming one-tile file.
5. Build attack files against each surface the brief names.
6. Write a verifier and run it against the surviving attack.

---

## 2. Constants and worked examples: all correct

I implemented CRC-32C from §4.5's parameters alone (Castagnoli 0x1EDC6F41,
reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF, stored LE). Reflected
table polynomial 0x82F63B78.

```
CRC-32C("123456789") = 0xe3069283   §4.5 says 0xE3069283          ✓
CRC-32C(<empty>)     = 0x00000000   §4.5 says 0x00000000          ✓
```

**Appendix A.** I transcribed the 128-byte hexdump verbatim and recomputed the
trailer CRC over trailer bytes [0, 60):

```
computed 0xe00938d2   stored (bytes D2 38 09 E0, LE) 0xE00938D2   ✓
```

The whole dump is self-consistent: F = 128, F mod 64 = 0, dir_offset = 16 ≥ 16,
dir_length = 4 ≥ 4, 16 + 4 = 20 ≤ F − 64 = 64, generation = 1, file_id ≠ 0,
reserved zero, directory region [16,20) = `00 00 00 00` = CRC-32C of the empty
record sequence. Appendix A is byte-correct.

**§15.4's sentinel-segment constant.** I built 65,536 copies of
`FF ×16 00 ×4` (1,310,720 bytes) and took the CRC:

```
CRC-32C(2^16 sentinel entries) = 0xeecb3bb2   §15.4 says 0xEECB3BB2   ✓
```

**Worked examples**, all re-derived by hand and checked:

| Where | Claim | Check |
|---|---|---|
| §11.2 | E=(1024,2048), T=(256,256) → G=(4,8), N=32, P=65,536 | ✓ |
| §11.2 | E_y=1000, T=256 → G_y = ⌈1000/256⌉ = 4 | ✓ |
| §11.4 | (300,700) → t=(1,2), s = 1·8+2 = 10; u=(44,188); in-tile ordinal 44·256+188 = 11,452 | ✓ |
| §11.4 | planar C=4, channel 2 at s=10 → disk ordinal 2·32+10 = 74 | ✓ |
| §12.3 | `temp`/float32/0x7FC00000 → `04 74 65 6D 70 0C 00 04 00 00 C0 7F` (12 bytes) | ✓ |
| §14.2 | interleaved T=(2,3), a:u8 b:u16 → Q=3, decoded 18, ordinal 5 at [15,18) | ✓ |
| §14.2 | same planar: b's tile 12 bytes, ordinal 5 at bytes 10–11 | ✓ |
| §14.2 | t:f32 + m:bool → Q=5, decoded 30, ordinal 5 at [25,30), m at 29 | ✓ |
| §14.3 | T=(2,5), P=10, alternating T/F → `55 01` (fill false), `55 FD` (fill true) | ✓ (bit 0 = value 0, LSB-first; pad bits 2–7 → 0x01\|0xFC = 0xFD) |
| §14.5 | E=(5,5), T=(4,4) → tile (1,1) has 1 real + 15 padding; 32 bytes, values 1–15 = `CD AB` | ✓ (in-tile ordinal of (4,4) is 0) |
| §15.4 | entry_count 1,000,000 → 16 segments, last 16,960 entries, array 64 B, region 20,000,064 B, tile 999,999 at segment-relative byte 339,180, segment 15 at [19,660,800, 20,000,000) | ✓ all six numbers |
| §15.4 | planar C=4 N=32: ordinal 74 at region bytes [1480,1500); channel 3 = entries 96–127 | ✓ |
| §17.3 | f32 1.0/2.0/3.0, s=4, n=3 → `00 00 00 00 00 00 80 00 40 3F 40 40` | ✓ (recomputed with the i·n+j formula) |
| §12.1 | bfloat16 1.0 = 0x3F80; b=0x0001 ↔ binary32 0x00010000 = 2^-133, matches bfloat16 subnormal 1·2^-7·2^-126 | ✓ |
| §21.9 note | 2^32 tiles → 2^16 segments → 256 KiB array; 2^36 → 4 MiB | ✓ |
| §15.4 | one full segment = 65,536 × 20 = 1,310,720 B = 1.25 MiB | ✓ |
| §5.1 | minimum file: 16 + (dir ≥ 4 at ≥ 16) + 64 with F ≡ 0 mod 64 → F ≥ 128 | ✓ (F=64 impossible: dir_offset+dir_length ≤ 0) |
| §17.2 | lz4 cap 0x7E000000 = 2,113,929,216 > 256 MiB guarantee | ✓ no conflict |

Nothing in this table needed a guess. That is a meaningful result on its own:
every number in the document that I could check is right.

## 3. §21.8's instance arithmetic

I parsed §21.2–§21.5's tables mechanically, counting a cell reading `—` as one
instance and otherwise splitting on `;` (the rule §21.1 states: "Instances
within a cell are separated by semicolons, and a cell reading — is one
instance; the count is therefore mechanical once the cell is written").

```
F rows 39  instances  61
L rows 50  instances 102
T rows 26  instances  45
R rows 10  instances  44
TOTAL     125 rows, 252 instances
```

§21.2 declares 39, §21.3 declares 50, §21.4 declares 26, §21.5 declares 10;
§21.8 declares "125 conditions over 252 instances". Exact. This is where round 6
and 7 reporters found register defects; there is nothing here.

I also checked §21.1's specialization list (F2 of F8 and F10, F38 of F39, L25 of
L26) — all four hold. I noticed unlisted near-specializations (F3's `dir_offset`
instance implies F12; T11's `offset` instance implies T9; L1's extent fields
imply L18), but §24 `[R-VEC-02]` already covers non-isolable conditions
explicitly ("the entry records every row the file exercises and says which it
was built for"), so this is not a defect. I also checked that L29 (S=0 with
A_slab≠0) and L30 (S≠0 with A_slab=0 included) are disjoint — they are; that is
careful drafting of exactly the boundary I went looking to break.

---

## 4. Building conforming files

### 4.1 The layer-record inline payload

I derived the field sequence from §7.4's table and confirmed it parses without
type knowledge (§7.4's claim: "fill parses without type knowledge and validates
with it"). Fixed prefix:

```
name        1 + L_name
layout      1
lineariz.   2
codec       2
filter      2
alignment A 8
slab S      8
A_slab      8
rank d      1
channels C  2                       → 35 + L_name
d × dim     1 + L + 8 + 8
C × chan    1 + L + 2 + 1 + elemsize
index_enc   1
entry_count 8
crc_of_crc  4                       → +13
sub-records to end of inline payload
```

No guess required: §7.4 gives every width and §14/§12 give every element size.

### 4.2 File 1 — one empty layer, 192 bytes

Layer `a`, interleaved, linearization 1, codec 1, filter 1, A=S=A_slab=0, d=1,
C=1, dimension `x` with E=0 T=1, channel `v` uint8 fill `00`, index_encoding 1,
entry_count 0, crc_of_crc_array 0, extent slot (0,0).

Inline = 73 bytes; record = 24 + 73 = 97; directory = 97 + 4 = 101 at
dir_offset 16, ending at 117; pad to 128; trailer [128,192); F = 192.
`dir_offset + dir_length = 117 ≤ F − 64 = 128` ✓, F mod 64 = 0 ✓.

Every constraint checked: `[R-GEO-02]` makes E=0 valid, N = ⌈0/1⌉ = 0, addressed
tiles 0, so `[R-CNT-17]`'s formula gives extent_length 0 and `[R-CNT-23]`
requires crc_of_crc_array 0. Determined, no guesses.

### 4.3 File 2 — one stored tile, 256 bytes

d=1, E=1, T=1, C=1 uint8, interleaved, codec 1, filter 1. N=1, entry_count=1,
P=1, Q=1, decoded size 1. Layout:

```
[0,16)    front block
[16,17)   tile payload (one byte 0x2A)
[17,41)   tile-index region: 1 entry (20) + 1 segment CRC (4) = 24
[41,142)  directory (97-byte layer record + 4-byte CRC)
[142,192) pre-trailer pad (50 bytes of slack)
[192,256) trailer
```

`[R-CNT-17]`: extent_length = 1×20 + ⌈1/2^16⌉×4 = 24 ✓. `[R-COD-04]`: entry
length 1 = decoded size 1 ✓. Note the *layer's structures come before the
directory* — forced by `[R-CNT-05]`'s "no structure lies between its end and the
trailer", which I initially had to re-read to realise makes the directory
necessarily the last structure in any conforming file. That is a real constraint
the layout tables do not state directly, and I record it as a place I had to
work rather than read.

---

## 5. Attacks

I organised attacks by the brief's surfaces. For each I state the construction,
the two candidate verdicts, and the sentence that decides it.

### 5.1 Boundary values

| Attack | Verdict | Foreclosed by |
|---|---|---|
| F = 0 (empty file) — trailer would be at [−64, 0) | reject-file, unambiguously | §5.1 `[R-CNT-27]`: "No conforming file is shorter than 128 bytes … A reader MUST treat a shorter file as a validity error at file scope." Decided *before* §6.2's trailer fetch, so the negative offset never arises. |
| F = 64 | reject-file | dir_offset ≥ 16 and dir_offset+dir_length ≤ F−64 = 0 are jointly unsatisfiable (`[R-CNT-06]`), and `[R-CNT-27]` fires independently. |
| F = 128, dir_length = 4 (empty record sequence) | conforming | Appendix A. CRC of zero bytes is 0x00000000 (§4.5), so `00 00 00 00` is a valid empty directory. |
| dir_length = 5 (1-byte record sequence) | reject-file | §7.2: "The sequence MUST parse as zero or more complete records with no residue" — a record header is 24 bytes. F32. |
| structure ending exactly at F−64 | never legal in a conforming file | `[R-CNT-13]`'s bound (`> F − 64` is the error) admits it, but `[R-CNT-05]` forbids any structure between the directory's end and the trailer, and the directory must therefore be last. The two bounds do not coincide — but the stricter one is verifier-checked (F9) and the looser reader-checked, which is exactly how the document splits the two detectors elsewhere. Not a fork. |
| A = 2^62 (the stated maximum) | conforming, but only satisfiable at F > 2^62 | §16.1 admits it; the only in-domain multiples of 2^62 are 0 (barred by offset ≥ 16) and 2^62. Absurd, legal, and stated. |
| A_slab = 1 with S ≥ 1 | conforming | §7.4 "1 ≤ A_slab ≤ 2^62"; 1 = 2^0 is a power of two. §16.2's note names it: "With A_slab = 1 a slab is contiguity-only". |
| entry_count = 65,536 vs 65,537 | 1 segment / 2 segments | §15.4's `⌈entry_count / 2^16⌉`. 65536×20+4 = 1,310,724; 65537×20+8 = 1,310,748. Both determined. |
| entry_count such that entry_count×20 overflows 2^63−1 | reject-layer | L2 lists the expression as an instance; `[R-ENC-04]`. |
| P = ∏Tᵢ overflowing in a layer with **zero addressed tiles** | reject-layer | This is the sharpest boundary I found. `[R-COD-07]`'s lz4 cap is quantified over *addressed* tiles, so it is vacuous when E=0; is `P·Q` also vacuous? The §17.2 Note says no — but that Note is non-normative under §2.1. What decides it normatively is L2, which lists "P·Q (which dominates V = P·C); P·Bᶜ" as layer-access instances with no addressed-tile qualifier, plus §14.3 `[R-SER-07]`: "Every decoded size … is a declaration-derived quantity under `[R-ENC-04]`" — decoded size is defined from declarations, not from the existence of a tile. **Foreclosed, but only by reading a register cell.** I flag this in the transcript rather than as a finding because the register is normative (§21.1) and the answer is stated twice. |
| Decoded size exactly 0x7E000000 under codec 4 | conforming | §17.2 says "exceeds"; equality passes. |
| Tile decoded size below 1 KiB under codec 3 | must be single-segment | §17.2's Note derives it (Window_Descriptor cannot express < 1 KiB), and `[R-COD-06]`'s window rule makes a non-single-segment sub-1-KiB tile a T21 reject-tile. Concrete: §14.2's 18- and 30-byte tiles and §14.3's 2-byte tile are named. Determined. |

### 5.2 Two structures claiming the same bytes

I tried eight overlap constructions:

1. Two index entries of one layer pointing at identical bytes → L19 reject-layer;
   §22.3 names it: "two index entries pointing at one payload".
2. A stored extent overlapping its own layer's index region → §15.3 row,
   reject-layer.
3. A stored extent overlapping another layer's tile → F36 reject-file.
4. A stored extent overlapping the directory region → F36 (instance "directory
   region").
5. Two layer records with **identical extent slots** (two layers sharing one
   index region) → F36, and the *reader* accepts the file happily, since
   `[R-CNT-13]` says "readers are not obligated to detect overlap". Designed
   split, registered.
6. A record extent placed inside the pre-trailer pad → F9 (verifier), reader
   accepts. Registered.
7. A record extent placed at [F−64, F) → barred by extent_offset+extent_length
   ≤ F−64.
8. A stored extent at [0,16) → §15.3 structural row "offset < 16 … the front
   block is never payload".

**Sub-record extents.** §9.7's walk sentence reads "it enumerates the live
directory and its records, each record's extent" — I tried reading "its records"
as *top-level* records only, which would let a user-metadata sub-record's extent
overlap another layer's tile undetected (verifier A: reject-file; verifier B:
certifies). That reading dies on two normative register cells: L19's instance
list includes "layer sub-record extents" and F36's includes "sub-record
extents", and §5.2 defines a coverage class as "the bytes **any** record's
extent slot references, whatever the record's type". Foreclosed.

**Zero-length structures.** There are none: extent (0,0) means *no extent*
(§7.2), a layer with zero addressed tiles has extent (0,0) (§7.4), a
non-sentinel entry with length 0 is a structural reject-tile (§15.3), and
§17.2's note pins the reason ("Decoded output is never empty — §14's decoded
sizes are at least 1 byte"). I checked that claim: interleaved P·Q with P≥1 and
Q≥1; planar numeric P·Bᶜ; packed bool ⌈P/8⌉ with P≥1. All ≥ 1. Correct.

### 5.3 Reserved / unknown / experimental values in every position

I enumerated every numeric space in §10.2 and each position it can occupy:

| Space | reserved | experimental | Decided? |
|---|---|---|---|
| record type, top-level, MU=1 | F38 reader reject-file | conforming file, reader rejects (§21.6's second structural case), verifier *cannot establish* | yes |
| record type, top-level, MU=0 | F39 verifier reject-file; reader ignores | §21.6: conforming, ignored | yes |
| record type, sub-record | L25/L26 | reject-layer via `[R-CNT-18]`; §21.6's second case is written for the file-scope form only, but `[R-EXT-03]` states the sub-record mapping explicitly | yes |
| layout | L37 (3–255; no experimental range, §10.2 explains the u8 is too narrow) | — | yes |
| linearization / sample type / codec / filter / index encoding | L34 / L35 / L44 / L46 / L32 | same rows | yes |
| metadata encoding | R1 ignore-record (violation) | §21.6: ignore-record, **conforming** | yes |
| trailer flags, incompat lane | F22 reject-file, and a violation, since §6.3 exempts only the ignore lane | — | yes |
| trailer flags, ignore lane | §21.6: conforming | — | yes |

I specifically tried to build a fork out of the ignore-lane exemption: a
major-1 file with bit 16 set and version_minor 0 arguably misstates its feature
floor under `[R-CNT-26]`. But `[R-CNT-26]` is a SHOULD, and `[R-CNF-12]` closes
it: "a verifier reports a SHOULD deviation as an advisory that does not bar
certification." Foreclosed by one sentence.

### 5.4 Feature interactions

- **Sparse tile under a filter chain.** A sentinel entry short-circuits the
  payload path entirely (§19.4 step 4), so the filter never runs. `[R-TYP-09]`
  is emphatic that fill comes from exactly one condition.
- **Empty layer under a limit.** Covered above (P·Q); also `[R-COD-07]`'s
  vacuous quantifier, which the rule text itself carries ("any of whose
  addressed tiles"), not only the Note.
- **Compaction over a record the compactor cannot read.** `[R-WRT-06]` refuses
  for MU=1; for MU=0 the extent relocates unread, protected by §7.2's
  no-embedded-offsets rule. I checked the apparent conflict between
  `[R-WRT-05]`'s byte-identical re-emission and `[R-WRT-07]`'s slot re-pointing:
  §20.5 carves it out explicitly ("except that relocation re-points extent
  slots"). I also checked `[R-WRT-09]`'s "each relocated extent's checksum"
  against §8.1's row for an unassigned type's extent ("none — the bytes are
  opaque") — there is no checksum to verify, and §22.3 says so directly. Loose
  but not contradictory.
- **Compaction of an aligned or slab-declared layer.** `[R-WRT-07]` says the
  compactor "is free to place structures anywhere §5.2 admits" — and §5.2 admits
  any non-overlapping partition, including one that breaks a declared alignment.
  I tried to make that a fork (compactor C1 honours A, C2 scatters and emits a
  file a verifier rejects at L41). It dies on `[R-WRT-06]`'s opening clause:
  "A compactor emits a new conforming file". Foreclosed, though "anywhere §5.2
  admits" is wider than intended.
- **Slab run continuity across a structurally-rejected entry.** §16.2 spells out
  three cases (sentinel transparent; structural reject-tile transparent; crc-only
  failure *not* transparent, "so this invariant stays decidable from index bytes
  alone"). I could not find a fourth case. The six *structural* rows in §15.3 are
  countable and match the text's "Six rows are marked *structural*".
- **Region read spanning a layer-scope failure.** Two readers legitimately
  return different data (`[R-RDR-04]` step 8: the bar "is prospective, so values
  the reader has already returned … stand"). This is licensed nondeterminism on
  a *nonconforming* file only, and §2.4 states it in the reject-layer row. Not a
  fork.

### 5.5 The degenerate-but-legal files

Built and checked: the 128-byte empty file (Appendix A, verified); the 192-byte
one-empty-layer file (§4.2 above); a zero-extent layer under codec 4 with a tile
shape that would blow the lz4 cap (conforming — the cap's quantifier is
vacuous); a layer with every optional thing absent (A=0, S=0, no sub-records, no
user metadata, extent slot (0,0)). All determined.

---

## 6. The attack that survives

### 6.1 Construction

Interleaved layer, d=1, dimension `x` with E=2, T=2 (so G=1 and there are **no
padding positions**), C=2 channels `u` and `v`, both uint16 (so **no boolean
bytes**). P = 2, Q = 4, decoded size P·Q = 8. Codec 1 (none), **filter 2
(byte-shuffle)**.

The writer's intended decoded tile image, sample-major per `[R-SER-01]`:

```
u0=0x0102 v0=0x0304 u1=0x0506 v1=0x0708
decoded = 02 01 04 03 06 05 08 07
```

`[R-COD-10]` mandates shuffle stride s = Q = 4 for an interleaved tile, giving
n = L/s = 2:

```
correct   = 02 06 01 05 04 08 03 07
```

My writer instead uses s = 2, n = 4 — a stride `[R-COD-10]` forbids
("A writer that filters with any other stride violates this rule"):

```
emitted   = 02 04 06 08 01 03 05 07
```

A conforming reader applies the mandated inverse (`restores byte i·n+j to offset
j·s+i`, with s = 4) and obtains:

```
reader sees = 02 06 01 05 04 08 03 07
            → u0=0x0602 v0=0x0501 u1=0x0804 v1=0x0703
```

— four perfectly valid uint16 bit patterns, none of which the writer meant.

The complete 256-byte file (`f3.bin`):

```
0000  89 54 41 52 4e 0d 0a 1a 00 00 00 00 00 00 00 00
0010  02 04 06 08 01 03 05 07 10 00 00 00 00 00 00 00
0020  08 00 00 00 00 00 00 00 bb e6 27 a9 6e 59 83 13
0030  01 00 03 00 51 00 00 00 18 00 00 00 00 00 00 00
0040  18 00 00 00 00 00 00 00 01 61 01 01 00 01 00 02
0050  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0060  00 00 00 00 00 00 00 00 00 01 02 00 01 78 02 00
0070  00 00 00 00 00 00 02 00 00 00 00 00 00 00 01 75
0080  07 00 02 00 00 01 76 07 00 02 00 00 01 01 00 00
0090  00 00 00 00 00 2c 46 18 e0 e6 2a 8a dc 00 00 00
00a0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00b0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00c0  8a 4e 52 41 54 0d 0a 1a 01 00 00 00 00 00 00 00
00d0  01 00 00 00 00 00 00 00 30 00 00 00 00 00 00 00
00e0  6d 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00
00f0  ef cd ab 89 67 45 23 01 00 00 00 00 c5 a1 0b 5e
```

Layout: front [0,16); stored tile [16,24); index region [24,48) (one 20-byte
entry + one 4-byte segment CRC); directory [48,157); pad [157,192); trailer
[192,256).

### 6.2 What my verifier says

I wrote a verifier from §19.1, §19.3, §19.4, §7, §8, §15 and §9.7 and ran it:

```
OK  R-CNT-04 front block
OK  R-CNT-27 / F mod 64
OK  R-CNT-06 magic
OK  R-CNT-06 trailer CRC
OK  R-CNT-07/08 version+flag gates
OK  R-CNT-06 field gates (dir_offset=48 dir_length=109 gen=1)
OK  R-CNT-11 directory CRC
OK  R-CNT-12 record sequence parses with no residue (1 record)
OK  R-CNT-18 layer 'a' inline parses exactly, no sub-records
OK  R-CNT-17 entry_count=1 addressed=1 extent_length=24
OK  R-ENC-04 products in domain (N=1 P=2 Q=4)
OK  R-IDX-04 crc_of_crc_array
OK  R-IDX-04 all 1 segment CRC(s)
OK  tile 0: crc ok, codec-1 length == decoded size (8)
OK  R-CNT-02 claimants disjoint [(0,16),(16,24),(24,48),(48,157),(192,256)]; slack 35 bytes
```

Every reader-detected and every verifier-detected row in §21.2–§21.5 passes.
T26 — the row for a mis-strided filter — cannot fire, because its own condition
text limits it: "*where the resulting image breaks §14.5's padding content or
`[R-SER-08]`'s bool bytes* (a wrong stride with no such structural constraint is
undetectable, §21.7)". My layer has neither padding positions nor bool channels,
by construction.

### 6.3 The fork

Now: **is `f3.bin` a conforming file, and may a verifier certify it?**

Reading A — *certify*. §2.3: "File conformance is a pure predicate on bytes: it
does not depend on any reader, writer, or environment." These eight stored bytes
are, considered as bytes, exactly what a *correct* writer would emit for the
array (0x0602, 0x0501, 0x0804, 0x0703). Nothing distinguishes them. So the file
is conforming; `[R-COD-10]`'s stride prohibition is a rule about the producer's
process, not about output, and a verifier — which "checks every **file-level**
requirement" (§2.3) — has nothing to check. Verdict: *conforming*, certified.

Reading B — *cannot establish*. §2.4: "A file is conforming only if it satisfies
every requirement at every scope"; §2.4 again: a verifier "certifies only
violation-free files". `[R-COD-10]` is a MUST-level rule and this file violates
it. §2.3 then says the verifier "reports one of three verdicts … *cannot
establish* — the last where some requirement is one it is unable to check", and
separately "A verifier MUST report each requirement it was unable to check,
naming the requirement and the ground, whichever of the three verdicts it
reports." A verifier cannot check `[R-COD-10]` for *any* filter-2 tile without
padding positions or bools — nor `[R-COD-06]`'s "Writers MUST NOT compress a
tile using a dictionary — whether or not the header discloses one" for *any*
codec-3 tile. Verdict: *cannot establish*; and §2.3 then forbids certification
("a verifier MUST NOT certify a file it reports that way").

Both are defensible from the text. The consequence of Reading B is severe and is
what makes this worth reporting rather than shrugging at: under it, **no file
that uses filter 2, or codec 2/3/4, can ever be certified by any verifier**,
because the unchecked-requirement list is never empty for such files. *Conforming*
becomes reachable only for codec-1, filter-1 files.

What tips me toward Reading A, and why it is still not decided:

- All five of §2.3's illustrative grounds for *cannot establish* are
  **capability** grounds — an unimplemented major, an unimplemented MU=1 type, an
  unexecutable codec, a resource decline, a declined metadata decode. The
  pattern says "unable **because of something about the verifier**".
  `[R-COD-10]` is unable because of something about the format. But the list is
  introduced with "as when", i.e. illustratively, and the governing clause
  ("some requirement is one it is unable to check") carries no such scoping.
- §21.7 exists to say the format "detects *corruption of structure*, not
  *incorrectness of content*", and §21.1 calls §21.7 "the account, by class, of
  what fails [detectability]". But §21.7's first paragraph says only that such a
  file is one "that every checksum in §8 certifies" — it never says the
  *verifier* certifies it, and it never says the file is conforming.
- §21.7's *second* paragraph does enumerate obligations "omitted from the
  register because a single file exhibits no witness of their violation", and
  lists `[R-LIF-01]`, `[R-LIF-03]`, `[R-GEO-06]`, `[R-SER-01]`, and
  `[R-CNT-13]`'s no-offsets rule. `[R-COD-10]` and `[R-COD-06]`'s dictionary
  clause are **not** in that list — they sit in the first paragraph instead,
  which is about content incorrectness rather than about register omission. So
  the one place that could have said "these are not file-level requirements"
  does not say it about these two.
- §2.3 does contain a carve-out for exactly this shape of rule — but it is
  drawn narrowly, and by enumeration:

  > "A few obligations this specification places on writers govern their
  > *conduct* rather than their output — where a value is published, or which
  > registry version a writer targets (§10.3, §18.3) — and a file is never
  > nonconforming by virtue of one: conduct rules bind the actor, the predicate
  > binds the bytes."

  §10.3 and §18.3 are named; §17.2's dictionary clause and §17.3's stride clause
  are not, though they are witness-free writer prohibitions of exactly the same
  kind. Adding them to that sentence would close the whole question.

I record honestly that I think most implementers land on Reading A, and that
this is therefore a *low-probability, high-blast-radius* fork rather than a
likely one. But it is the only construction I found where two competent
verifiers, reading only this document, arrive at different normative verdicts on
identical bytes with nothing in the text to adjudicate.

---

## 7. Two further defects found while attacking

### 7.1 F21 is a non-violation sitting in the violations register

§21.1: "The register — §21.2 through §21.5 — enumerates every detectable
violation this specification names: each row is one malformed condition".
§21.2's heading: "File-scope violations. Outcome: reject-file. 39 conditions."

F21 is: "Trailer version_major is a nonzero major the reader does not implement
(e.g. 2); magic and CRC still validate | version_major | reader | open |
`[R-CNT-07]` (R-CNT-24)".

But §21.6 says, of exactly that row:

> "the first is registered as F21, whose condition records only the reader's
> outcome and not a defect in the bytes"

and §2.3 lists "when the file names a format major version it does not
implement" as a ground for *cannot establish* — a verdict §2.3 makes available
"only to a traversal that established no violation". If F21 is an established
violation, §2.3's own first illustrative ground for *cannot establish* is
self-defeating: the condition that triggers it would itself be a violation, and
"An established violation takes priority" would force *nonconforming* every
time.

The fork this could open: for a byte sequence with version_major = 2 and an
otherwise-valid major-1 trailer, verifier V1 (reading §21.2) reports
*nonconforming*; verifier V2 (reading §2.3 and §21.6) reports *cannot establish*.
I judge it **closed**, three-to-one: `[R-CNT-07]`'s own text says only that a
reader "MUST reject-file … a major it does not implement" and reserves the word
"invalid" for version_major = 0; §21.1 says "where a row and the rule it cites
diverge, **the rule governs**"; and §21.6 and §2.3 both side against the row.
Neither verdict certifies, so no byte sequence changes hands. It is a real
mislabelling in the register, not a fork.

One downstream consequence is worth naming: §21.8 requires a conformance vector
for every register row, and §24 `[R-VEC-02]` requires each vector's manifest to
record "whether the file is **conforming**". For F21's vector — a file naming
major 2 — this document does not decide that boolean. §6.2's table gives
version_major's valid values as "1 (0 invalid; others: §6.3)", and §6.3 makes an
unimplemented major a reader-capability matter without calling the file invalid,
while §21.6 says the file "can be perfectly conforming under that major" (i.e.
under a *different* specification). Whichever way that is resolved, §24's own
test applies: "A vector whose expectation cannot be stated in those terms is
testing something this specification has not defined, which makes it a finding
against this document rather than a vector."

### 7.2 Appendix H's writer checklist promotes a SHOULD

Appendix H's conforming-writer entry reads:

> "**Conforming writer** — emits only conforming files (§2.3); records fill for
> every channel (`[R-TYP-06]`, §13.1); fill-encodes edge padding and pad bits
> (`[R-SER-05]`, §14.5); emits interleaved boolean values as only 0x00 or 0x01
> (`[R-SER-08]`, §14.2); sorts user-metadata object members by their keys' UTF-8
> bytes (`[R-MTA-05]`, §18.2); zeroes the gaps it creates (`[R-CNT-03]`, §5.2);
> follows the commit protocol including both barriers (§9.2); honors any
> alignment or slab it declares (§16)."

Seven of the eight are MUSTs. "Zeroes the gaps it creates" is not: `[R-CNT-03]`
says "Writers SHOULD zero the gaps they create … no conformance requirement
rides on slack content either way", and §5.2 says slack's "content is
unconstrained, and no conformance requirement applies to it". Appendix G is
explicit that this is the profile's one addition beyond the mandatory:
"Everything else the profile needs is already mandatory except gap content,
which `[R-CNT-03]` only advises and this profile requires."

Appendix H is labelled non-normative and disclaims itself ("each entry's
authority is the requirement or section cited, never this summary"), so nothing
turns on it — no byte changes, no verdict changes, since slack content is
unconstrained by construction. But the appendix's stated purpose is "for
implementers auditing their own work", and an auditor working the checklist
would mark a fully conforming writer as failing.

In the same checklist I noticed a second, smaller slip: the conforming-reader
entry reads "implements all four codecs, both filters, both layouts, and all
thirteen sample types (`[R-CNF-03]`, §2.3)" — enumerating four of `[R-CNF-03]`'s
five clauses and dropping "every user-metadata encoding §18.2 assigns", which
§2.3 states explicitly and backs with "software that declines to support … an
assigned user-metadata encoding is not a conforming reader". Harmless in
practice (encoding 2's decoder is already required for codec 3, as §18.2 notes),
but the checklist is the audit surface.

---

## 8. Attacks I tried that the document simply forecloses

Listing these because an empty result is only worth something if the attacks
were real. Each of these I actually constructed or laid out in bytes before
finding the sentence that kills it.

1. **Two layers with byte-identical empty names.** Would F6 (reject-file) or L6
   (reject-layer, per-layer) govern? §19.1 step 4 decides in one clause:
   "Uniqueness is decided first, and over the raw name bytes whether or not each
   name is itself well-formed". F6.
2. **A layer record whose name field overruns inline_length, alongside a layer
   named the same as nothing.** §19.1: such a record "yields no name field to
   compare, so it contributes no name to the namespace". No spurious duplicate.
3. **A remote reader that never fetches [0,16) versus a local one that does**,
   over a file with a corrupt front block. §6.1 `[R-CNT-04]` splits on
   *residency*, not transport, and F8's condition restates it; a verifier is
   exempt from nothing (§2.3), so it must fetch them. No verifier fork.
4. **A trailer-mimic byte string inside a stored tile.** A stored extent cannot
   reach [F−64, F) (extent_offset+extent_length ≤ F−64), so the live trailer's
   bytes are never inside a live structure. §21.6 registers the mimic as inert
   and §9.6 makes recovery re-verify whole.
5. **Residue past a completed commit** (physical file longer than
   committed_file_length). §9.5's Note handles it explicitly and declines to give
   it a register row, correctly: the observable state is already F19.
6. **A metadata document that decodes to 17 MiB.** Verifier A (16 MiB bound)
   *cannot establish*; verifier B (64 MiB bound) certifies. Explicitly licensed:
   `[R-MTA-09]` says "the bound is that verifier's capability and not a limit on
   validity … so the decline is not a finding that the file is nonconforming".
   Same shape for `[R-ERR-04]` resource declines. Designed, not a defect.
7. **A conforming file with an experimental record type carrying MU = 1.** No
   reader may accept it; §21.6 names it as one of "two structural cases:
   conforming files a reader nevertheless refuses". Stated.
8. **An MU = 0 unknown record whose extent a compactor relocates.** §7.2's
   no-embedded-offsets rule is precisely what makes it safe, and §7.2 says so.
9. **A codec-3 tile with Single_Segment_Flag and a 256 MiB decoded size**,
   forcing Window_Size = 256 MiB past §21.9's 8 MiB guarantee. Not a trap: zstd
   permits a Window_Descriptor smaller than the content size, so a writer can
   always stay inside the guarantee, and `[R-COD-06]`'s SHOULD says so
   ("Writers SHOULD keep the declared window within §21.9's 8 MiB `Window_Size`
   guarantee even for a larger tile").
10. **A layer with a stale slab declaration after a commit.** §16.2's Note
    explains why it has no register row of its own — every file exhibiting one
    exhibits an L42 or L43 — and I could not construct a counterexample: a
    stale declaration that happens to still satisfy the invariants is not a
    detectable defect and is also harmless.
11. **`tarn.title` carrying a number, or `tarn.axes` on a file-scope
    document.** §18.4 and §21.6 both say: ignore the key, the file stays
    conforming. Twice-stated.
12. **A file whose only violation is unsorted metadata members.** F30/L49,
    verifier, and readers "process the document unchanged". Reader accepts,
    verifier rejects — the designed split, registered.

---

## 9. Confidence

I built a writer and a verifier from this document with no external reference,
and every constant, every worked example and every piece of register arithmetic
I could check was correct. The places I had to work rather than read were: that
`[R-CNT-05]` makes the directory necessarily the last structure (derivable but
not stated as such in a layout table); that `P·Q` is checked in a layer with no
addressed tiles (stated only in a Note and a register cell); and the boundary of
"a requirement it is unable to check" in §2.3, which is the one place I could
not resolve.
