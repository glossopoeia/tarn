# Cleanroom round 29 — Diagram auditor transcript

## 0. Access and disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,697 lines by `wc -l`; the brief said 4,698 — the difference is a missing
trailing newline or an off-by-one in the brief, not a missing file, and the file
was where the brief said it was). I read it end to end in five `Read` calls and
then ran `grep`/`awk`/`sed` pipelines against that same file only. I opened no
`docs/`, no `PLAN.md`, no `OPEN-QUESTIONS.md`, no `conformance/`, no
`spec/registry.json`, no git history, no web.

I wrote two files, both under my own scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-round/scratch/diagrams/`:

- `crc_diag.py` — a self-contained CRC-32C implementation plus the Appendix A
  hex dump transcribed by hand from my reading of the document. It reads no
  files; the dump is inlined in the script. This is the only executable I ran.

I wrote this transcript to
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-round/out/transcript-diagrams.md`
and did not read or list that directory.

**Unrequested context.** My runtime placed material in my context before I began:
a project instruction file pointing at an `AGENTS.md`, and an index of the
maintainer's auto-memory naming several memory files (working cadence, decision
style, prior workflow failures, and notes about spec edits and the §21 register).
I did not open any of them, and I have not used anything they suggested as
evidence. I disclose their appearance because the brief requires it. One index
line names §21 and a "vector corpus build list"; I mention only that it appeared,
not its content, and I re-derived every §21 figure below myself from the document.

---

## 1. Method

My charter is figures, diagrams, byte-layout boxes, offset tables, worked
examples, and checklists. I did the enumeration first, then judged.

### 1.1 Enumeration of everything in charter

**Layout / structure tables**

| § | lines | what |
|---|---|---|
| 2.2 | 126–146 | requirement-prefix table (19 rows) |
| 2.4 | 294–300 | outcome-class table (5 rows) |
| 6.1 | 762–765 | front signature block, 16 bytes |
| 6.2 | 805–816 | trailer, 64 bytes |
| 7.2 | 969–975 | record header, 24 bytes |
| 7.3 | 1044–1047 | record types of format major 1 |
| 7.4 | 1073–1090 | layer-record inline payload (packed, no offsets) |
| 8.1 | 1191–1199 | checksum coverage map (7 rows) |
| 10.2 | 1516–1525 | numeric identifier spaces (8 rows) |
| 12.1 | 1734–1748 | sample types (13 rows) |
| 14.2 | 1966–1969 | decoded size / offset of value k (2 rows) |
| 15.1 | 2136–2140 | tile-index entry, 20 bytes |
| 15.3 | 2184–2196 | entry-validity classification (11 rows) |
| 18.2 | 2580–2582 | user-metadata inline payload, 1 byte |
| 18.4 | 2773–2780 | standardized metadata keys (6 rows) |
| 20.4 | 3365–3369 | updater obligations by stored flags (3 rows) |
| 21.2 | 3642–3678 | file-scope register (35 rows) |
| 21.3 | 3691–3741 | layer-scope register (49 rows) |
| 21.4 | 3751–3778 | tile-scope register (26 rows) |
| 21.5 | 3801–3812 | ignore-record register (10 rows) |
| 21.6 | 3819–3834 | conditions that are not violations (14 rows) |
| 21.9 | 3944–3953 | minimum guarantees (8 rows) |
| App A | 4322–4337 | annotation of the 128-byte minimal file (14 rows) |
| App B | 4357–4385 | constants (28 rows) |
| App E | 4455–4457 | changelog (1 row) |

**ASCII figures / boxes**

| § | lines | what |
|---|---|---|
| 5.1 | 652–657 | a file after three commits |
| 9.2 | 1284–1293 | what a crash sees (3 rows) |
| 15.1 | 2131–2132 | tile-index region layout — **an unlabelled blockquote, therefore normative** |
| 20.3 | 3294–3298 | commit shape (a) new layer |
| 20.3 | 3310–3314 | commit shape (b) tiles added |
| 20.3 | 3336–3339 | commit shape (c) directory-only |
| 20.5 | 3504–3510 | what compaction reclaims |
| App A | 4311–4320 | the 128-byte hex dump |
| 7.4 | 1139–1158 | the annotated 81-byte layer-record payload |

**Worked examples**: §4.6 (`température`), §5.1 (smallest file), §7.4 (layer
record payload), §11.2 (grid), §11.4 (ordinals), §12.1 (bfloat16), §12.3
(channel entry), §13.3 (fill tuples), §14.2 (byte layout), §14.3 (packed bool),
§14.5 (padding content), §15.4 (two: 10⁶ entries; planar C=4), §16.2 (slabs),
§17.3 (byte-shuffle), §20.3 (superseding one tile), Appendix A.

**Checklists / numbered procedures**: §9.2 commit protocol (6 steps), §10.1
extension vehicles (4), §19.1 open (4), §19.4 tile read (8), §20.3 append (6),
Appendix G reproducible-writer profile (10 items), Appendix H four class
checklists.

### 1.2 Guarding against false zeros

The brief warns that a hard-wrapped document defeats line-oriented grep. Before
resting anything on a zero I ran the same search normalized:

```
tr '\n' ' ' < spec/tarn.md | tr -s ' ' | grep -c "never arises in a conforming file"   -> 1
tr '\n' ' ' < spec/tarn.md | sed 's/> //g' | tr -s ' ' | grep -c "the two are the same length" -> 1
```

Both are phrases I had read and both span a line break (the second also spans a
`> ` blockquote marker). The pipeline finds them, so a zero from it is
informative. I used this normalized form for every phrase search below.

---

## 2. Computation: every checksum recomputed

I wrote CRC-32C from the reflected Castagnoli polynomial 0x82F63B78 (the
reflection of the 0x1EDC6F41 §4.5 names), init 0xFFFFFFFF, final XOR
0xFFFFFFFF. I validated the implementation against §4.5's own check vector
before using it on anything else.

```
CRC32C("123456789")            = 0xE3069283   document: 0xE3069283      MATCH
  stored little-endian          = 83 92 06 E3  document: 83 92 06 E3     MATCH
CRC32C(zero bytes)             = 0x00000000   document: 0x00000000      MATCH
```

### 2.1 Appendix A, byte by byte

I transcribed the 8 dump lines by hand into the script and re-derived every
field from §6.2's layout table (offset/width read from the table, bytes cut from
the dump, decoded little-endian), rather than reading the annotation table.

```
file length                    = 128        App A prose: 128            MATCH
trailer = f[64:128], length      64         §6.2: final 64 bytes        MATCH
tr[0:8]  magic  8A 4E 52 41 54 0D 0A 1A     §6.2 table                  MATCH
tr[8:10] version_major  = 1                 App A row [72,74)           MATCH
tr[10:12] version_minor = 0                 App A row [74,76)           MATCH
tr[12:16] flags = 0x00000000                App A row [76,80)           MATCH
tr[16:24] dir_offset = 16                   App A row [80,88); ≥16 ok   MATCH
tr[24:32] dir_length = 4                    App A row [88,96); ≥4 ok    MATCH
tr[32:40] committed_file_length = 128       = file size; 128 mod 64 = 0 MATCH
tr[40:48] file_id = 0x0123456789ABCDEF      App A row [104,112); ≠0     MATCH
tr[48:60] reserved: all zero                App A row [112,124)         MATCH
tr[60:64] stored CRC = 0x402F157E  (7E 15 2F 40)
COMPUTED CRC-32C over tr[0:60] = 0x402F157E                             MATCH
directory [16,20) = 00 00 00 00 = CRC-32C of zero bytes                 MATCH
pad [20,64): 44 bytes, all zero                                         MATCH
```

Column sum of the annotation table's 14 rows: 8+8+4+44+8+2+2+4+8+8+8+8+12+4 =
**128**, contiguous with no gap or overlap. The trailer layout table's own
offsets close likewise: 0+8=8, 8+2=10, 10+2=12, 12+4=16, 16+8=24, 24+8=32,
32+8=40, 40+8=48, 48+12=60, 60+4=64 — which is [R-CNT-24]'s "The format-major-1
trailer has zero slack: every byte is assigned", confirmed arithmetically.

Record header closes at 0+2=2, 2+2=4, 4+4=8, 8+8=16, 16+8=**24**. Index entry
closes at 0+8=8, 8+8=16, 16+4=**20**. Front block 0+8=8, 8+8=**16**.

I also checked Appendix A's remote-open arithmetic: a 112-byte suffix window is
[128−112, 128) = [16, 128), which contains the directory [16, 20) and does not
reach offset 0. Both halves of the claim hold.

### 2.2 §7.4's worked layer-record payload

The document prints `0x80A34955` for the segment CRC over the 80-byte all-sentinel
entry array and `0xC4EE982E` for `crc_of_crc_array`. I recomputed both from the
sentinel definition in §15.2 (`FF ×16 00 ×4`) rather than trusting the printed
values:

```
entry array = 4 × (FF ×16 00 ×4)      length 80        §15.1: 4 × 20 = 80  MATCH
CRC32C(that 80 bytes)  = 0x80A34955   document: 0x80A34955                MATCH
  stored little-endian  = 55 49 A3 80  document: 55 49 A3 80              MATCH
CRC32C(55 49 A3 80)    = 0xC4EE982E   document: 0xC4EE982E                MATCH
  stored little-endian  = 2E 98 EE C4  document: 2E 98 EE C4              MATCH
```

Field-by-field offsets, each width read from §7.4's own Type column, not from
the dump's left margin:

```
 0 name        1 + 3   -> 4     (03 73 73 74 = len 3, "sst")
 4 layout      u8      -> 5
 5 linearize   u16     -> 7
 7 codec       u16     -> 9
 9 filter      u16     -> 11
11 A           u64     -> 19
19 S           u64     -> 27
27 A_slab      u64     -> 35
35 rank d      u8      -> 36
36 C           u16     -> 38
38 dim name    1 + 1   -> 40    (01 78 = len 1, "x")
40 extent      u64     -> 48    (64 00 …  = 100)
48 tile extent u64     -> 56    (20 00 …  =  32)
56 chan name   1 + 4   -> 61
61 chan type   u16     -> 63    (0C 00 = 12 = float32)
63 fill        1 + 4   -> 68    (04 00 00 C0 7F = 0x7FC00000)
68 index_enc   u8      -> 69
69 entry_count u64     -> 77    (04 00 … = 4)
77 crc_of_crc  u32     -> 81
```

Every printed offset in the dump matches. The prose's decomposition also
checks out: name 4; the nine scalars layout…C = 1+2+2+2+8+8+8+1+2 = **34**;
the dimension entry 2+8+8 = **18**; the channel entry 5+2+5 = **12** (byte for
byte identical to §12.3's twelve-byte example `04 74 65 6D 70 0C 00 04 00 00 C0 7F`
— I concatenated dump offsets 56 and 63 and compared); the trailing fixed fields
1+8+4 = **13**. 4+34+18+12+13 = **81**, and inline_length = 81, so the
sub-record sequence is empty with no residue, exactly as claimed.

Geometry: ⌈100/32⌉ = 4 = entry_count (interleaved, C = 1, so addressed = N).
[R-CNT-17]'s extent_length = 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 80 + 4 = **84**, as printed.

Name bytes decoded: `73 73 74` = "sst"; `78` = "x"; `74 65 6D 70` = "temp".
Type 12 little-endian = `0C 00`. Fill 0x7FC00000 little-endian = `00 00 C0 7F`.
Extent 100 = 0x64; tile extent 32 = 0x20. All correct.

### 2.3 §15.4's all-sentinel segment constant

```
2^16 sentinel entries = 1,310,720 bytes
CRC32C = 0xEECB3BB2      §15.4 and Appendix B: 0xEECB3BB2       MATCH
```

Appendix B's "CRC of a full all-sentinel segment | `0xEECB3BB2`" agrees, and
1,310,720 bytes = 1.25 MiB, which is §15.4's "never more than one full segment
(1.25 MiB)".

### 2.4 Every other numeric example, recomputed

- **§11.2.** (1024, 2048) / (256, 256) → G = (4, 8) ✔, N = 32 ✔, P = 65,536 ✔.
  With E_y = 1000, ⌈1000/256⌉ = 4 ✔ (the last tile row padded).
- **§11.4.** s = t₀·G₁ + t₁: (0,0)→0, (0,1)→1, (1,0)→8 ✔. (300, 700) → tile
  (1, 2), s = 10 ✔; in-tile (44, 188), ordinal 44·256 + 188 = 11,452 ✔;
  planar C = 4, channel 2 → 2·32 + 10 = 74 ✔.
- **§12.1.** bfloat16 1.0: binary32 1.0 = 0x3F800000, high half 0x3F80, stored
  `80 3F` ✔. 0x7FC0 ↔ binary32 0x7FC00000 ✔.
- **§14.2.** (2, 3), P = 6, uint8 + uint16: Q = 3, size 18 ✔; ordinal
  1·3 + 2 = 5, bytes [15, 18) ✔. Planar b: 6·2 = 12 bytes, ordinal 5 at 10–11 ✔.
  float32 + bool: Q = 5, size 30, ordinal 5 at [25, 30), bool byte at 29 ✔.
  I also checked the closing identity "channel c's value at in-tile ordinal u
  sits at byte u·Q + Fᶜ — the table's forms with k = u·C + c": for 0 ≤ c < C,
  k div C = u and k mod C = c, so (k div C)·Q + F_{k mod C} = u·Q + Fᶜ ✔.
- **§14.3.** P = 10, alternating true/false: byte 0 bits 0,2,4,6 set = 0x55 ✔;
  byte 1 bit 0 set = 0x01 ✔; fill true sets pad bits 2–7 → 0x01 | 0xFC = 0xFD ✔.
- **§14.4 Note.** At P = 1 planar is ⌈1/8⌉ = 1 byte and interleaved 1 byte;
  pad bits 1–7 carry fill, so the images coincide iff fill is false ✔
  (fill true gives 0xFE/0xFF planar against 0x00/0x01 interleaved).
- **§14.5.** (5,5)/(4,4) → grid 2×2 ✔; tile (1,1) covers 4–7 on both axes, so
  exactly one position (4,4) is real and 15 are padding ✔; 16 · 2 = 32 bytes ✔;
  fill 0xABCD little-endian = `CD AB` ✔; value 0 is in-tile ordinal 0 = (0,0) =
  coordinate (4,4), the real one ✔.
- **§15.4 first example.** ⌈10⁶/2¹⁶⌉ = 16 segments ✔; 10⁶ − 15·65,536 = 16,960 ✔;
  16·4 = 64-byte CRC array ✔; 20,000,000 + 64 = 20,000,064 ✔; k = 999,999 →
  segment 15, index 16,959, offset 20·16,959 = 339,180 ✔; CRC array at
  [20,000,000, 20,000,064) ✔; segment 15 at [983,040·20, 20,000,000) =
  [19,660,800, 20,000,000), length 339,200 ≈ 339 KB ✔.
- **§15.4 second example.** disk ordinal 74 → [20·74, 20·75) = [1,480, 1,500) ✔;
  channel 3 of C = 4, N = 32 → ordinals 96…127, thirty-two entries ✔.
- **§16.2.** N = 32, S = 8 → runs [0,8), [8,16), [16,24), [24,32) ✔; each is one
  tile row under row-major with G_x = 8 ✔; rows 1–2 = ordinals 8–23 = runs 1 and
  2 ✔.
- **§17.3.** 1.0f/2.0f/3.0f = `00 00 80 3F | 00 00 00 40 | 00 00 40 40`; s = 4,
  n = 3; byte i of group j to offset i·n + j gives
  `00 00 00 00 00 00 80 00 40 3F 40 40` — identical to the printed result ✔.
- **§19.4 Note.** Entries c·N+s and (c+1)·N+s differ by N; if N ≥ 2¹⁶ then
  (a + N) div 2¹⁶ > a div 2¹⁶ always, so they are guaranteed to be in different
  segments ✔.
- **§20.3 example.** 32·20 + ⌈32/2¹⁶⌉·4 = 640 + 4 = **644** ✔.
- **§20.3 Note.** 10⁶ · 20 = 20,000,000 ≈ "about 20 MB of index" ✔.
- **§21.9 Note.** ⌈2³²/2¹⁶⌉·4 = 2¹⁶·4 = 262,144 = **256 KiB** ✔; at 2³⁶ it is
  2²⁰·4 = **4 MiB** ✔; 65,536 layers × 200 bytes = 13,107,200 = **12.5 MiB**
  exactly, and 16 MiB > that ✔.
- **§24 [R-VEC-03].** 2³² × 20 = 85.9 GB — "tens of gigabytes" ✔.
- **§9.2 Note.** prior F + 4 + 64 = prior F + 68; the next multiple of 64 above
  that is prior F + 128 ✔.
- **§5.1 [R-CNT-27].** Smallest F: dir end ≥ 20, trailer needs F − 64 ≥ 20 →
  F ≥ 84, and F ≡ 0 (mod 64) → F = **128** ✔; pad = 64 − 20 = 44 ✔.
- **§4.6.** `74 65 6D 70 C3 A9 72 61 74 75 72 65` decodes to "température",
  12 bytes ✔; NFD substitutes `65 CC 81` for `C3 A9`, giving 13 ✔.

**Nothing in any worked example, dump, or annotation disagreed with the
normative text or with my own arithmetic.** Every checksum the document prints
reproduces.

---

## 3. The register: counts derived mechanically

§21.8 asserts "120 conditions over 275 instances". §21.1 fixes the counting
rule: "Instances within a cell are separated by semicolons, and a cell reading —
is one instance; the count is therefore mechanical once the cell is written."
So I counted rather than trusted.

First I checked column alignment — every register row splits into exactly 8
fields on `|`, and field 5 is always `reader` or `verifier`, so field 4 really
is the Instances cell:

```
awk -F'|' 'NR>=3644 && NR<=3812 && $2 ~ /^ *[FLTR][0-9]+ *$/ {if (NF!=8) print "BADCOLS"}'  -> no output
```

Then per table, splitting field 4 on `;`:

```
§21.2  F rows: 35   instances:  56    header says "35 conditions"   MATCH
§21.3  L rows: 49   instances: 116    header says "49 conditions"   MATCH
§21.4  T rows: 26   instances:  55    header says "26 conditions"   MATCH
§21.5  R rows: 10   instances:  48    header says "10 conditions"   MATCH
                    ----                ---
       total   120             275    §21.8: "120 conditions over 275 instances"  MATCH
```

Row labels are in ascending order in every table with exactly one gap, F11,
which §21.2's Note declares struck and deliberate. No duplicates.

I then spot-audited the instance cells against §21.1's two stated axes.

- *Layout axis.* T3, T14, T22 each enumerate three decoded-size formulas ×
  two magnitude directions = 6; T21 and L44 enumerate three formulas × one
  direction ("larger than", "exceeds") = 3; L21 two layouts × two directions =
  4. All consistent.
- *Magnitude axis.* "differs from" / "does not equal" rows give two directions
  (T14, T3, T22, L21, L22, L30, F17); "exceeds" / "larger than" rows give one
  (T21, L44). Rows with no magnitude ordering give none (T1, L37, L38, F14 —
  checksum comparisons; F8 — a byte pattern). Rows testing only for nonzero
  give none (L20's *A ≠ 0 with S ≠ 0*). All consistent.
- *Single predicate over several fields.* F25 (MU = 1 with PE = 0) is one
  instance; F26/L47 ("any reserved bit set") one per container; F28/L49 (MU or
  PE differing) two per container. Consistent with §21.1's explicit ruling that
  "the fields it reads are not instances, because no two files could differ".
- *Containers.* L15 = 2 alternatives × 2 containers = 4 against F30's 2 × 1 = 2;
  L16/L17 = 1 × 2 = 2 against F31/F32 = 1. Consistent.
- *Value-space rows.* L31 (3), L33 (4), L34 (4), L36 (2), L43 (3), L45 (3),
  R1 (2 × 2 = 4) each reproduce exactly the partition their defining section
  states, and each matches §10.2's row for that space. I checked all eight rows
  of §10.2 against §7.3, §14.1, §11.4, §12.2, §17.2, §17.3, §15.1 and §18.2 —
  all agree.
- *Omission that is correct.* L2 lists `P·Q` and `P·Bᶜ` but not `⌈P/8⌉`.
  ⌈P/8⌉ ≤ P and P is itself listed, so no file exists in which ⌈P/8⌉ overflows
  and P does not — §21.1's "one instance is one *distinguishable* file" makes
  the omission right, not an oversight.

**One cell does not follow the pattern its neighbours follow — R8.** Written up
as finding `diagrams-01`.

### 3.1 Cross-checks that passed

- **§21.2's reach claim.** "Deriving it there yields F8, F14, F6 and both of
  F1's instances … and no other row." [R-CNT-24] fixes exactly: trailer magic at
  F−64, version_major/minor at F−56, a CRC-32C at F−4 over [F−64, F−4), and the
  front block. F8 = magic, F14 = trailer CRC, F6 = front block, F1 = both of
  those byte-reversed. F13 (64-alignment) and F17 (length cross-check) assert
  invariants [R-CNT-24] does *not* fix, so they correctly do not reach. F5 and
  F15 are explained in §2.3's Note. Derivation reproduces.
- **§2.3's "nine".** [R-CNT-06] states: magic, trailer CRC, length = file size,
  length multiple of 64, dir_offset ≥ 16, dir_length ≥ 4, dir_offset+dir_length
  ≤ F−64, file_id ≠ 0, reserved zero = **nine** ✔, of which two ([R-CNT-24]'s
  magic and CRC) reach and **seven** do not ✔. Nine register rows cite
  [R-CNT-06] as governing (F8, F14, F17, F13, F9, F16, F10, F12, F15) ✔.
- **§21.1's specialization pairs.** F21 ⊂ F22: a (0,0) slot has extent_length 0
  < 5 ✔. L10 ⊂ L11 ✔. F35 ⊂ F36, L24 ⊂ L25 ✔. F1's front-block instance ⊂ F6:
  the reversed constant `1A 0A 0D 4E 52 41 54 89` ≠ `89 54 41 52 4E 0D 0A 1A` ✔.
  F1's trailer instance ⊂ F8 likewise ✔.
- **§20.5's "seven spaces".** §10.2 tabulates 8 spaces; minus record type leaves
  7; the cited rows L31 (index encoding), L33 (linearization), L34 (sample
  type), L36 (channel layout), L43 (codec), L45 (filter), R1 (metadata
  encoding) are exactly those 7, in ascending label order ✔.
- **§15.3's "Six rows are marked *structural*".** I counted the table: crc ≠ 0
  sentinel; one-of-two sentinel; length 0; offset < 16; offset/length > 2⁶³−1;
  overflow-or-past-F−64 = **six** ✔.
- **§15.3 → §21 mapping.** Each of its eleven rows has a home: T6, T7, T10, T8,
  T11, T12/T9, T1, L18, F33, L40/L41/L42 ✔, plus the sentinel row which is a
  §21.6 non-violation ✔.
- **§8.1's coverage map vs §4.5.** §4.5 names three terminal checksum fields
  (trailer, directory, user-metadata extent) and three interior ones (segment
  CRC array, entry crc, crc_of_crc_array) plus two uncovered classes (front
  block, unassigned-type extent). §8.1's seven rows realize exactly that
  partition, and every byte of the tile-index region is covered — entries by
  their segment CRC, the array by crc_of_crc_array, and crc_of_crc_array by the
  directory CRC, since it lies inside the layer record's inline payload ✔.
- **§4.7's Note on table columns.** It names three exceptions to the six-column
  form: §6.1 (Value replaces type and range), §7.2 (range folded into the Field
  cell), §7.4 (offset and class omitted). I checked every layout table in the
  document; those are the only three that deviate, and each deviates exactly as
  described ✔.
- **§4.7's "version_minor is the only descriptive field".** A whole-document
  search for `descriptive` returns 5 hits, exactly one of which is a table cell
  (§6.2, version_minor) ✔.
- **§2.2's prefix table.** I extracted every `R-XXX-` prefix used in the
  document (19 distinct) and compared with the table's 19 rows: identical sets ✔.
  I also enumerated every identifier: CNF 01–13, CNT 01–27, COD 01–11, ENC
  01–16, ERR 01–05, EXT 01–05, GEO 01–06, IDX 01–05, LIF 01–08, MDL 01–02, MTA
  01–10, PRV 01–05, RDR 01–04, SEC 01–07, SER 01–09, SLB 01–05, TYP 01–10, VEC
  01–04, WRT 01–09 — **no gaps and no duplicates**. R-SER-04 appears only in
  §14.4's withdrawal Note ✔; R-ENC-100 only as §2.2's own illustration ✔.
- **Numbered lists.** §9.2 1–6; §10.1 1–4; §19.1 1–4; §19.4 1–8; §20.3 1–6;
  Appendix G 1–10 — all present, in order, none duplicated.
- **Appendix B.** I checked all 28 rows against their cited sections. Every
  constant matches, including the two I recomputed (the check vector and the
  all-sentinel segment CRC), the widths (`u8` → 255 rank, `u16` → 65,535
  channels), and the §21.9 digest row (8 items against 8 table rows).
- **Appendix C.** Record types, 13 sample types with their pinned reservations,
  4 codecs, 2 filters, 2 layouts, 1 linearization, 1 index encoding, 2 metadata
  encodings, flag lanes, 6 standardized keys — all match their defining sections.
- **Appendix F.** Nine normative references, each cited from a section that
  needs it; correctly *not* marked "(non-normative)" while A, B, C, D, E, G, H
  all are.
- **Appendix H.** I checked the reader checklist's "all four codecs, both
  filters, both layouts, all thirteen sample types, and both user-metadata
  encodings" against [R-CNF-03] and each defining section — exact. I checked the
  verifier checklist against the register: the twenty rows carrying Detector
  *verifier* are F7, F25, F26, F27, F28, F33, F36, L18, L25, L40, L41, L42, L46,
  L47, L48, L49, T2, T4, T5, T26, and every one of them has a bullet
  (T26 via "decoded-content obligations", which its own row says is T2's or
  T4's check). The updater and writer checklists likewise trace to §20.4,
  §9.2, §16, [R-TYP-06], [R-SER-05], [R-SER-08], [R-MTA-05].
- **Figures against the prose.** §5.1's three-commit box: I reconstructed the
  file state after each of the three commits from [R-LIF-02] and got exactly
  `front | A | (dir₁ pad tr₁) | B | (dir₂ pad tr₂) | dir₃ pad tr₃` — the two ▓
  runs sit precisely where the figure puts them, and the caption's identification
  of them is right. §9.2's crash figure: row 3's ▓ replaces exactly `dirₙ pad
  trailₙ`, which is what commit n+1 supersedes ✔. §20.3's three shapes and
  §20.5's compaction box are each consistent with [R-WRT-04]/[R-WRT-05]/
  [R-WRT-07] and with §5.2's classes. §15.1's region blockquote reproduces
  [R-CNT-17]'s formula exactly.

---

## 4. Findings

### diagrams-01 — R8's Instances cell enumerates containers but not the two alternatives its own condition text states (OBSERVATION)

§21.5, row R8; the counting rule is §21.1.

R8 reads, verbatim:

> | R8 | A user-metadata document contains a non-finite number, in any form — a magnitude whose binary64 interpretation overflows (`1e400`) and the bare tokens `NaN`, `Infinity` and `-Infinity` alike | top-level document; layer sub-record document | reader | extent use | `[R-MTA-04]` (R-CNT-25) |

§21.1 fixes what a cell must carry:

> An instance names a field the condition ranges over, a container it can occur in, one of several alternatives the condition text states, or any combination of the three — a condition applying to two alternatives in two containers has four.

R8's condition text states two alternatives — an overflowing magnitude, and a
bare token — and [R-MTA-04] states them as a disjunction:

> A document is unreadable if it contains a number whose binary64 interpretation is not finite — which covers a magnitude that overflows on conversion, `1e400` being the ordinary case — or any of the bare tokens `NaN`, `Infinity`, or `-Infinity`, which RFC 8259 does not admit and some parsers accept regardless.

The cell enumerates only the two containers. Its neighbours in the same table
enumerate alternatives *and* containers: R5 gives 2 alternatives × 2 loci × 2
containers = 8, R6 gives 2 × 2 = 4, R7 gives 3 × 2 = 6. The escape §21.1 offers
— "a row whose check ranges over a family without the condition changing shape
states that range as a single instance (T24's *any codec*)" — does not obviously
apply, because the two alternatives give the check materially different shapes,
which is the criterion §21.1 uses to *enumerate* T15's zlib and gzip wrappers
and T25's three malformed streams: `1e400` is a syntactically valid RFC 8259
number that fails a binary64 finiteness test after conversion, while `NaN` is a
token RFC 8259 does not admit at all and only a lenient parser ever produces.

The consequence is a corpus gap that the register's own arithmetic hides. A
bare-`NaN` document also satisfies R7's "not well-formed JSON" instance, so by
§21.1's specialization rule ("the file is recorded against the narrower row")
it is recorded against R8, not R7. But R8 names no bare-token instance, and
[R-VEC-03] requires "at least one vector for each instance it names" — so a
corpus that builds R8's two instances with `1e400` in each container, and R7's
"not well-formed JSON" instances with a syntax error, contains **no vector at
all** for the bare tokens, which is exactly the case [R-MTA-04] singles out as
the one "some parsers accept regardless".

Permitted readings: (a) the two alternatives are one family and 2 instances is
right, so 275 stands; (b) they are materially different shapes and the cell
should read 4, making §21.8's total 277. I pick (b): §21.1's own criterion is
"materially different shapes", and the document applies it to enumerate pairs
less different than this one (T15's two wrapper formats share a check —
"is there a wrapper" — far more closely than a numeric conversion shares one
with a lexical token test). But the document leaves "materially different" to
judgement rather than defining it, so I report this as an OBSERVATION rather
than a contradiction.

Not byte-level: both alternatives are already violations under [R-MTA-04]
whichever way the cell is written, with the same ignore-record outcome. What
moves is what a conformance corpus must contain.

### diagrams-02 — the front-matter gloss narrows [R-ENC-16]'s structural test by dropping layer and tile acceptance (CONTRADICTION)

The document's opening blockquote glosses the field taxonomy:

> Every field is classified as **structural** (its value affects where a byte lies, how it decodes, what a decoded value is, or whether the file is accepted) or **descriptive** (none of those — §4.7).

[R-ENC-16] in §4.7 states the test the gloss is glossing:

> A field is **structural** if its value determines anything a conforming reader or verifier does with the bytes it reads — where a byte lies, how it decodes, what a decoded value is, or whether the file, layer or tile is accepted at all

Two differences, both narrowing. The gloss drops the head clause "determines
anything a conforming reader **or verifier** does", and it drops "**layer or
tile**" from the acceptance limb, leaving only "whether the file is accepted".

The narrowing bites on real fields. Take the tile-index entry's `crc` field.
§15.1's own layout table classifies it:

> | 16 | 4 | u32 | crc | structural | CRC-32C of the stored tile's bytes (§8.1); 0 in a sentinel entry |

Its value does not affect where any byte lies, how anything decodes, or what any
decoded value is; a mismatch is reject-**tile** (T1, [R-CNT-20]), never
reject-file. So under the gloss's four-limb test it "affects none of those" and
is **descriptive** — contradicting §15.1's table cell, and contradicting
[R-ENC-16]'s closing sentence "In format major 1 `version_minor` is the only
descriptive field". `crc_of_crc_array` is the same shape one scope up: its only
effect is reject-layer (L37). And the record header's reserved flag bits 2–15,
which [R-CNT-12] tells readers to ignore and assigns to a *verifier*, fall
outside the gloss's test for a second reason, the dropped "or verifier".

The classification is not decorative. [R-ENC-16] attaches a consequence to the
descriptive class: "its value determines nothing a conforming reader does, and a
reader MUST NOT alter decoding based on it". A reader that took the gloss's test
at face value and classified an entry's `crc` as descriptive would conclude its
value determines nothing it does — which is precisely the verification
[R-CNT-20] and T1 require.

I take the resolution to be that [R-ENC-16] governs: it says in terms that
version_minor is the only descriptive field, §15.1's table marks `crc`
structural, and §8.2's chain of trust is unambiguous. So no competent
implementation reading the whole document forks, and I grade this not
byte-level. But the gloss is a restatement that drifted from the rule it
restates, in the first blockquote a reader meets, and it is what an implementer
skimming the front matter will carry into §4.7.

(Whether the gloss is normative is `diagrams-03`; the drift is a defect either
way, since a non-normative block disagreeing with the text it glosses still
tells an implementer what to build.)

### diagrams-03 — the front-matter blockquote claims non-normativity by a device [R-CNF-01]'s closed exception list does not recognize (AMBIGUITY)

[R-CNF-01] states a closed exception list:

> All text in this document is normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices identified as non-normative.

The document's opening blockquote is:

> **How to read this document** *(non-normative).* Sections follow a fixed rubric where applicable: purpose, byte-layout table, writer rules, reader rules, error handling, worked examples.

It sits at lines 12–22, above the `---` at line 24 and above `### 1.
Introduction` at line 28, so it is not in §1. It is not labeled *Note*,
*Example*, or *Rationale*. It is not an appendix. By [R-CNF-01]'s literal terms
it is therefore normative, while announcing that it is not.

Permitted readings: (a) [R-CNF-01]'s list is closed as written, the block is
normative, and its self-label has no effect — this is the reading the text
supports, since the list is introduced by "except:" and enumerates three
exceptions exhaustively; (b) the "(non-normative)" parenthetical is the same
device [R-CNF-01] already honours for appendices ("appendices identified as
non-normative"), so it should be honoured here too — but [R-CNF-01] confines
that device to appendices, and this block is not one.

I pick (a), which is what makes `diagrams-02` bite: under (a) the document
carries two normative definitions of *structural* that disagree about layer and
tile acceptance. Under (b) the block is merely a non-normative gloss that
disagrees with the rule — still a defect, one degree less sharp.

This is also the only place in the document where the two devices collide.
I checked every appendix heading: A, B, C, D, E, G and H all carry
"(non-normative)" and are appendices, so [R-CNF-01] reaches them; F carries no
such marking and is correctly normative. And I confirmed by sweep that §15.1's
region-layout blockquote carries no *Note*/*Example*/*Rationale* label either
and is therefore normative — correctly so, since it is a byte-layout figure that
[R-CNT-17] depends on, and its content reproduces [R-CNT-17]'s formula exactly.
So the document does contain unlabelled normative blockquotes by design; the
front-matter block is the one that contradicts its own status.

Not byte-level. The block's other claims (the section rubric, the layout-table
convention, requirement identifiers, vectors citing identifiers rather than
prose positions) either restate §2.2, §4.7 and [R-VEC-02] faithfully or say
nothing a file can violate. Only the structural gloss diverges, and
`diagrams-02` explains why the specific rules still settle it.

### diagrams-04 — Appendix G item 5's universal is falsified by a legal degenerate tile (OBSERVATION)

Appendix G, item 5:

> The filter is the identity exactly where its permutation is — where the stride is 1, as for a packed boolean plane, and equally where the decoded image is a single group, n = L/s being 1 (`[R-COD-10]`); elsewhere it changes the stored bytes of every tile it touches.

The final clause is a claim about *every* tile. Build the smallest legal
counterexample: an interleaved layer, one `uint16` channel, fill 0x0000, tile
extents giving P = 4, filter 2, codec 1. Then s = Q = 2, L = 8, n = 4, so the
permutation is not the identity. Store a tile all of whose samples are 0x0101 —
a legal sample value under [R-TYP-05], and not an all-fill tile, so item 6 does
not exclude it. The decoded image is `01 01 01 01 01 01 01 01`; the byte-shuffle
sends byte i of group j to i·n + j, which permutes eight equal bytes into eight
equal bytes. The stored bytes are unchanged, and the filter has "touched" the
tile.

The same holds for any decoded image whose bytes are all equal — an all-zero
tile of any type, a `uint8` interleaved tile of a repeated value, a packed bool
plane of all-true bytes.

What the item is actually for survives: the profile still has to pin the filter
value, because a *general* tile's bytes do change and two writers disagreeing on
the filter disagree on the file. So this costs an implementer nothing that
follows the profile. It is reported because the sentence as written is a
universal a conforming file can falsify, and because Appendix G's items are what
an adopter checks its writer against.

Not byte-level: Appendix G is identified as non-normative, and by its own words
"It adds no requirement to any actor: a writer ignoring it is fully conforming".

---

## 5. Candidates I opened and closed

- **§18.2's layout table cell "Valid values: 1 or 2; see below" against §21.6's
  ruling that an experimental-range (≥ 0x80) metadata encoding leaves the file
  conforming.** I spent the longest on this one, because a "Valid values" column
  states a conformance constraint in §6.2 (`dir_offset ≥ 16`, `file_id ≠ 0`,
  `reserved | zero`) and reading it that way here would make encoding 0x80 a
  violation, contradicting §21.6, [R-MTA-10] ("certification is unaffected"),
  [R-EXT-03] and §21.5's header. What closed it: **the same table's own
  neighbour uses the column the same loose way** — §6.2 gives
  `version_major | 1 (0 invalid; others: §6.3)`, and a file declaring
  version_major 2 is expressly neither conforming nor nonconforming
  ([R-CNF-02]). So the column's established practice in this document is "the
  value(s) this text uses, with a pointer", and "see below" is that pointer.
  §7.1 states the same set the same terse way ("u8: 0 invalid, 1 = none, 2 =
  zstd; §18"). Not a defect.
- **§21.1's "which is why §14.2 calls it the sole resolved byte in this
  format".** A normalized whole-document search for `sole resolved byte` returns
  two hits, neither in §14.2 (lines 3630 and 4649); the uniqueness claim lives
  in §12.3's [R-TYP-04] ("the one case where a reader resolves a byte to a
  value"). What closed it: a case-insensitive sweep of §14.2 found its Note
  saying "Only the in-tile byte, whose detector is the verifier, could be met by
  a reader with no obligation to act on it" — a defensible antecedent for the
  paraphrase. Attribution is loose, not wrong.
- **F33's Instances cell enumerating five claimant kinds while its condition
  text states three overlap alternatives.** Closed by §21.1's "One instance is
  one *distinguishable* file": the three alternatives are a classification of
  which claimant pairs count, not independently realizable across all five
  claimant kinds (two structures "neither of which belongs to a layer" excludes
  stored-tile extents and index regions outright), so the cross product §21.1
  describes is not available here.
- **§20.5's compaction figure showing `pad` in the output while its caption says
  "▓ marks slack", though §5.2 makes the pre-trailer pad slack.** Closed by
  §5.1's figure, which establishes the same convention and says in prose "the
  pad and the ▓ runs are slack" — the pad is drawn as a labelled cell in both
  figures, so no reader is invited to conclude the compacted output has no slack.
- **§21.6's "The file contains zero layers | A conforming file with an empty
  directory", which conflates zero layer records with an empty directory (a file
  with zero layers and one user-metadata record has a non-empty directory).**
  Closed because [R-CNT-14] itself makes the same elision in the same words —
  "zero is valid: an empty directory is a conforming generation" — so the §21.6
  entry restates its governing rule faithfully, which is the test §21.1 sets
  for §21.6's entries.
- **F5's condition naming the pre-trailer pad among the four things that "cannot
  all fit" below 128 bytes, where [R-CNT-27]'s derivation does not use the pad.**
  Closed because in the minimal file the pad is 44 bytes and is forced by the
  64-alignment [R-CNT-27] does use; §2.3's Note states the derivation without it,
  so the register row is a gloss over an already-stated derivation.
- **§21.6's trailer-mimic row justifying inertness by "nothing enumerates
  slack" while its condition is stated over "a payload", which is live state.**
  Closed by the rest of the cell — "a recovery tool re-verifies its output whole
  (§9.6) … §9.6's second caution covers the rest" — which is the correct and
  complete justification for a mimic wherever it sits, and which I checked
  against §9.6's two cautions (re-verify; rollback needs out-of-band state).
- **RFC 1950 and RFC 1952 named in [R-COD-05] and T15's instances but absent
  from Appendix F.** Closed because [R-COD-05]'s normative content is "exactly
  one DEFLATE compressed data stream as defined by RFC 1951", decidable from RFC
  1951 alone; the wrapper names are explanatory, and T15's own row says "the
  check that detects it is T24's or T25's".
- **§19.1 step 4 citing only [R-ENC-12] for name checking while L3's governing
  rule is [R-ENC-11].** Closed because step 4 says "parsed and checked per §4.6",
  and §4.6 is where [R-ENC-11] lives; §19.3's parallel list cites both.
- **§14 bar vs §11.1's Rationale on growth and shrink.** I wrote out the
  quantifiers for both bars ("any tile that layer stores **in the generation
  this commit supersedes**") and tested them against a growth from E = 100 to
  E = 128 at T = 32 (the set of padding positions changes for a stored tile).
  §20.3 answers it in terms — "a position that becomes real held … that
  channel's fill (§14.5), and fill is a legal sample value" — and the Rationale's
  "among them" marks its zero-grid-count case as an example rather than the
  class. No divergence.
- **Whether "the growth that raises a zero-extent layer's **last** zero grid
  count" reads *last-declared dimension* or *last remaining zero*.** The
  preceding clause supplies the sense ("while another stays 0 … the product
  holding at 0"), so *last remaining zero*. Non-normative Rationale; not
  reported.
- **Appendix H's reader checklist omitting [R-CNF-03]'s MU = 1 caveat from
  "accepts every conforming file within §21.9's minimum guarantees", and its
  updater checklist omitting §20.4's third flag-authority case (a type the
  updater implements that this specification does not register).** Closed by the
  appendix's own opening: "each entry's authority is the requirement or section
  cited, never this summary."

---

## 6. Where I found little, and what would have found something

**Worked examples and checksums.** This was my highest-effort area and it is
clean. What would have found something: I recomputed all four printed CRC-32C
values from a reimplementation validated against the document's own check
vector, cut every field of the Appendix A trailer out of the dump using
offsets and widths read from §6.2's layout table rather than from the annotation
beside them, and re-derived every arithmetic figure in fifteen examples
independently before comparing. A single wrong constant, offset, width or
checksum would have shown as a mismatch line in §2 above. None did.

**Register arithmetic.** I derived 35/49/26/10 = 120 rows and 56/116/55/48 = 275
instances by machine from the tables themselves, after verifying that the column
split was sound. Had any subsection header or §21.8's total been stale, the
comparison would have shown it. A stale count is exactly the defect this method
finds, and there is none.

**Figures.** For each ASCII box I reconstructed the file state independently from
the commit protocol and compared region for region, rather than reading the
caption. §5.1's two ▓ runs land exactly where [R-LIF-02] puts commit 1's and
commit 2's superseded directory/pad/trailer.

**What I could not settle.** Whether R8's two alternatives count as "materially
different shapes" turns on a phrase §21.1 does not define; I argued it and
graded it OBSERVATION rather than claiming the register's total is wrong.
Whether the front-matter blockquote is normative turns on whether [R-CNF-01]'s
exception list is closed; I read it as closed because it is written as one, and
said so.
