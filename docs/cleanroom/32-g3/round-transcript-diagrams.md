# Round 32 — Diagram auditor — working transcript

Lane: figures, diagrams, byte-layout boxes, offset tables, worked examples,
checklists. Cleanroom.

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
4,754 lines, in four `Read` calls plus `grep`/`awk`/`python3` passes over that
same path. I opened no ADR, no `docs/`, no `conformance/`, no `registry.json`,
no `PLAN.md`, no `AGENTS.md`, no git history. I listed no directory other than
creating my own scratch directory. No web access.

The file was where the brief said it would be.

**Context I did not ask for.** Material was placed in my context before I began:
a project instruction file pointing at an `AGENTS.md`, and an index of the
maintainer's memory notes with titles about this project's harness, its round
mechanics, and its repair history. I did not open any of it and I have not used
any of it. I record its appearance here because the brief requires it; I am not
repeating its contents. Nothing below rests on it.

Scratch files I wrote, all under
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-round/scratch/diagrams/`:

- `crc32c_diag.py` — my own CRC-32C, table-driven, built from the reflected
  polynomial; used to check every printed checksum.
- `count_inst.py` — parses the four register tables out of the document and
  counts rows and semicolon-separated instances.
- `tablecheck.py` — finds every markdown table and checks each row's cell count
  against its header.
- `appa.py` — reassembles Appendix A's hex dump and decodes each trailer field.
- `layerrec.py` — reassembles §7.4's layer-record dump and re-parses it against
  §7.4's field table.

I wrote nothing else anywhere, and read nothing in the output directory.

---

## 1. Enumeration — every figure, table, example and checklist, with line numbers

I enumerated before judging, so coverage is checkable.

### 1.1 Markdown tables (25, all well-formed — every row's cell count matches its header)

| line | cols | rows | table |
|---|---|---|---|
| 127 | 2 | 19 | §2.2 requirement prefixes |
| 301 | 2 | 5 | §2.4 outcome classes |
| 773 | 4 | 2 | §6.1 front signature block layout |
| 816 | 6 | 10 | §6.2 trailer layout |
| 984 | 5 | 5 | §7.2 record header layout |
| 1060 | 4 | 2 | §7.3 record types of format major 1 |
| 1089 | 3 | 16 | §7.4 layer record inline payload |
| 1207 | 3 | 7 | §8.1 checksum coverage map |
| 1550 | 5 | 8 | §10.2 numeric identifier spaces |
| 1762 | 4 | 13 | §12.1 core sample types |
| 1995 | 3 | 2 | §14.2 byte layout / decoded size |
| 2168 | 6 | 3 | §15.1 tile-index entry layout |
| 2216 | 2 | 11 | §15.3 entry validity classification |
| 2615 | 6 | 1 | §18.2 user-metadata encoding byte |
| 2812 | 3 | 6 | §18.4 standardized keys |
| 3378 | 2 | 3 | §20.4 updater preservation obligations |
| 3658 | 6 | 35 | §21.2 file-scope register |
| 3707 | 6 | 49 | §21.3 layer-scope register |
| 3767 | 6 | 26 | §21.4 tile-scope register |
| 3817 | 6 | 10 | §21.5 ignored-record register |
| 3837 | 3 | 15 | §21.6 conditions that are not violations |
| 3963 | 2 | 8 | §21.9 minimum guarantees |
| 4350 | 3 | 14 | Appendix A annotated byte table |
| 4385 | 3 | 27 | Appendix B constants |
| 4483 | 3 | 1 | Appendix E changelog |

### 1.2 ASCII figures / box diagrams (6)

- L659–664 §5.1 — a file after three commits (8-cell box + under-box annotation)
- L1155–1174 §7.4 — layer record inline payload, 81-byte annotated dump
- L1309–1318 §9.2 — what a crash sees (three rows, two arrows)
- L2163–2164 §15.1 — index region layout (**unlabelled blockquote — normative**)
- L3300–3346 §20.3 — the three shapes a commit takes, (a)/(b)/(c)
- L3517–3523 §20.5 — what compaction reclaims (input/output)
- L4339–4348 Appendix A — the 128-byte hex dump

### 1.3 Worked examples (labelled `Example`, 24)

L585 (`température`), L649 (smallest file), L656 (three commits), L1144 (layer
record payload), L1305 (crash), L1677 (grid arithmetic), L1733 (linearization),
L1796 (bfloat16), L1845 (channel entry), L1915 (fill tuples), L2040 (interleaved
byte layout), L2074 (packed bool plane), L2132 (edge padding), L2256 (segments at
10^6 entries), L2271 (planar entry placement), L2373 (slabs), L2558
(byte-shuffle), L3286 (superseding one tile), L3295 (three commit shapes), L3514
(compaction).

### 1.4 Checklists / list-shaped material

- §10.1 four extension vehicles (4 numbered items)
- §19.1 open algorithm (4 steps), §19.4 tile read (8 steps), §9.2 commit (6 steps)
- §20.3 append procedure (6 steps)
- Appendix D six design choices
- Appendix G reproducible-writer profile (10 numbered items)
- **Appendix H conformance checklists (5 entries — file, reader, writer, updater,
  verifier)**

### 1.5 The blockquote-label check

`awk` over every blockquote block, taking each block's first line and removing
those beginning `> **Note`, `> **Example`, `> **Rationale`: **exactly one**
survives — line 2163, §15.1's index-region layout box. It is therefore normative
under `[R-CNF-01]`. Its content —
`[ entry array: entry_count × 20 bytes ] [ segment CRC array: ⌈entry_count / 2¹⁶⌉ × 4 bytes ]`
— agrees with `[R-CNT-17]`'s `entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4`
exactly. No defect there. I note the label rule cuts the other way for the rest
of my surface: §5.1's, §20.3's and §20.5's figures are all inside blocks labelled
*Example*, and Appendix H is headed "(non-normative)". That is why none of my
findings is graded byte-level, and I say so per finding.

---

## 2. The standing charge — every checksum recomputed, every dump re-parsed

I wrote CRC-32C myself from §4.5's parameters (Castagnoli, reflected in/out,
init 0xFFFFFFFF, final XOR 0xFFFFFFFF) rather than reading a library, and ran it
over bytes I reassembled from the document's own dumps.

| what | document says | I computed | verdict |
|---|---|---|---|
| CRC-32C("123456789") (§4.5, App. B) | 0xE3069283, bytes `83 92 06 E3` | 0xE3069283, `83 92 06 E3` | match |
| CRC-32C(zero bytes) (§4.5, §5.1, App. A) | 0x00000000 | 0x00000000 | match |
| Appendix A trailer CRC over [0,60) | 0x402F157E, bytes `7E 15 2F 40` | 0x402F157E, `7E 15 2F 40` | match |
| §7.4 index CRC over 4 sentinel entries (80 B) | 0x80A34955, bytes `55 49 A3 80` | 0x80A34955, `55 49 A3 80` | match |
| §7.4 `crc_of_crc_array` over `55 49 A3 80` | 0xC4EE982E, bytes `2E 98 EE C4` | 0xC4EE982E, `2E 98 EE C4` | match |
| §15.4 / App. B all-sentinel full segment (2¹⁶ entries) | 0xEECB3BB2 | 0xEECB3BB2 | match |

Every printed checksum in the document is correct. The all-sentinel segment
constant in particular is a 1,310,720-byte input and it is right.

### 2.1 Appendix A, byte by byte

I reassembled the hex dump (`appa.py`), asserting each row's printed offset
against the running length. It is exactly 128 bytes and the rows are contiguous.
Then I cut each field out at the offset and width §6.2's *layout table* gives —
not at the offsets Appendix A's annotation table gives — and compared:

```
[0,8)     89 54 41 52 4E 0D 0A 1A   front magic (§6.1 constant: match)
[8,16)    00 ×8                     front reserved (zero: match)
[16,20)   00 00 00 00               directory region = CRC-32C of zero bytes
[20,64)   00 ×44                    pre-trailer pad (all zero)
[64,72)   8A 4E 52 41 54 0D 0A 1A   trailer magic (§6.2 constant: match)
[72,74)   version_major = 1
[74,76)   version_minor = 0
[76,80)   flags = 0
[80,88)   dir_offset = 16           (§6.2: ≥ 16 ✓)
[88,96)   dir_length = 4            (§6.2: ≥ 4 ✓)
[96,104)  committed_file_length = 128  (= file size ✓, 128 mod 64 = 0 ✓)
[104,112) file_id = 0x0123456789ABCDEF  (≠ 0 ✓)
[112,124) 00 ×12                    trailer reserved (zero ✓)
[124,128) 7E 15 2F 40 = 0x402F157E  (recomputed: match)
```

Cross-checks: `dir_offset + dir_length = 20 ≤ F − 64 = 64` ✓. The annotation
table's 14 rows tile [0,128) with no gap and no overlap. §5.1's Example gives the
identical decomposition (front [0,16), directory [16,20), 44 bytes of slack,
trailer [64,128)) and §6.2's `[R-CNT-05]` predicts the pad exactly: the directory
ends at 20, `[R-LIF-02]` step 5 pads to the next 64-boundary, 64 − 20 = 44. All
three agree.

### 2.2 §7.4's layer-record dump, re-parsed against §7.4's own field table

`layerrec.py` reassembles the 18 annotated rows, asserting each printed offset
against the running length (no drift), then re-parses the 81 bytes strictly in
§7.4's table order:

```
name len 3 "sst" | layout 1 | lin 1 | codec 1 | filter 1 | A 0 | S 0 | A_slab 0
rank 1 | C 1 | dim "x" extent 100 tile extent 32 (entry ends at 56)
channel "temp" type 12 fill len 4 fill 00 00 C0 7F = 0x7FC00000 (ends at 68)
index_encoding 1 | entry_count 4 | crc_of_crc_array 0xC4EE982E
consumed 81, residue 0
```

- The printed running offsets 0/4/5/7/9/11/19/27/35/36/38/40/48/56/63/68/69/77
  are exactly what the field widths force. No off-by-one anywhere.
- The prose's arithmetic: "4 + 34 bytes, the dimension entry 18, the channel
  entry 12, and the trailing fixed fields 13 — 81 exactly" → 4+34+18+12+13 = 81.
  Confirmed. The "nine scalars from layout through channel count" are layout(1)
  + linearization(2) + codec(2) + filter(2) + A(8) + S(8) + A_slab(8) + rank(1)
  + C(2) = 34, and there are exactly nine of them.
- Geometry: G = ⌈100/32⌉ = 4, interleaved so addressed-tile count = N = 4 =
  entry_count. `[R-CNT-17]`: 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84, which is the extent
  length the example states.
- The channel entry `04 74 65 6D 70 0C 00 04 00 00 C0 7F` split across the dump's
  rows 56 and 63 is byte-for-byte §12.3's example, as the text claims.
- Sentinel bytes `FF ×16 00 ×4` (§15.2) × 4 = the 80 bytes whose CRC I recomputed.

Nothing wrong in it.

### 2.3 Every other worked example, arithmetic redone by hand

- §4.6 `température`: NFC `74 65 6D 70 C3 A9 72 61 74 75 72 65` = 12 bytes,
  length prefix 12 ✓; NFD with `65 CC 81` = 13 ✓. Appendix G item 10 restates
  both figures identically.
- §11.2: extents (1024,2048) / tiles (256,256) → G = (4,8), N = 32, P = 65,536 ✓;
  extents (1000,2048) → G_y = ⌈1000/256⌉ = 4 ✓.
- §11.4: tile (1,0) → 1·8+0 = 8 ✓; coordinate (300,700) → tile (1,2), s = 10 ✓;
  in-tile (44,188) → 44·256+188 = 11,452 ✓; planar C=4 channel 2 → 2·32+10 = 74 ✓.
- §12.1 bfloat16: 1.0 = high 16 bits of 0x3F800000 = 0x3F80, stored `80 3F` ✓;
  0x7FC0 ↔ 0x7FC00000 ✓.
- §14.2: (2,3) P=6, uint8+uint16 → Q=3, size 18 ✓; ordinal 5 at bytes [15,18),
  `a` at 15, `b` at 16–17 ✓; planar `b` = 12 bytes, ordinal 5 at 10–11 ✓;
  float32+bool → Q=5, size 30, ordinal 5 at [25,30), `t` 25–28, `m` at 29 ✓.
  The closing identity "channel c's value at ordinal u sits at u·Q + Fᶜ — the
  table's forms with k = u·C + c" is exact: k div C = u, k mod C = c.
- §14.3: P=10 alternating from true → byte 0 = 0b01010101 = 0x55 ✓; byte 1 bit 0
  set = 0x01 ✓; pad bits are 2..7, six of them ✓; fill true → 0x01|0xFC = 0xFD ✓;
  decoded size ⌈10/8⌉ = 2 ✓.
- §14.4's note: ⌈P/8⌉ = P only at P = 1, and there the planar image equals the
  interleaved one exactly when fill is false (planar byte = value bit | 0xFE·fill).
  Correct as stated.
- §14.5: extents (5,5) tiles (4,4) → grid 2×2; edge tile (1,1) covers 4–7 on both
  axes; only (4,4) is real, 15 padding ✓; P=16, one uint16 → 32 bytes; ordinal 0
  is the sample, 1–15 are `CD AB` ✓ (0xABCD little-endian).
- §15.4 first example: 10⁶ entries → ⌈10⁶/65536⌉ = 16 segments, 15 full and a
  last of 1,000,000 − 983,040 = 16,960 ✓; CRC array 64 bytes ✓; region
  20,000,064 ✓; k = 999,999 is segment-relative 16,959, byte 339,180 ✓; CRC array
  at [20,000,000, 20,000,064) ✓; segment 15 at [19,660,800, 20,000,000) ✓;
  16,960 × 20 = 339,200 ≈ "339 KB" ✓; one full segment = 65,536 × 20 = 1,310,720
  = 1.25 MiB exactly ✓; entry_count 0 → zero segments, zero-byte array ✓.
- §15.4 second example: disk ordinal 74 → region bytes [1,480, 1,500) ✓; channel
  3's ordinals are 96–127, 32 entries ✓.
- §16.2: N=32, S=8 → four runs [0,8) [8,16) [16,24) [24,32) ✓, each a tile row
  under row-major with G_x = 8 ✓; rows 1–2 = ordinals 8–23 = runs 1 and 2 ✓.
- §17.3 byte-shuffle: I did the permutation myself. 1.0/2.0/3.0 float32 LE =
  `00 00 80 3F 00 00 00 40 00 00 40 40`; s=4, n=3; byte i of group j → i·3+j
  gives `00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40`. The document prints exactly
  that.
- §20.3: 32 · 20 + 4 = 644 ✓; "editing one sample of a 10⁶-tile layer appends
  about 20 MB of index" — 10⁶ × 20 = 20,000,000 ✓.
- §21.9's note: at entry_count 2³², the segment-CRC array is (2³²/2¹⁶)·4 = 2¹⁸ =
  256 KiB ✓, and at 2³⁶ it is 2²² = 4 MiB ✓; 65,536 layers × 200 B = 13,107,200 =
  12.5 MiB exactly ✓.
- Appendix A's open accounting: a 112-byte window covering [16,128) does contain
  [16,20) ✓ and leaves [0,16) non-resident ✓.

### 2.4 Cross-document constant agreement

I grepped each constant and counted occurrences, then read every occurrence:
front block bytes (4 sites), trailer magic (5), 0xEECB3BB2 (3), 0xE3069283 (2),
`28 B5 2F FD` / 0xFD2FB528 (3+2), 0x7E000000 (4), 0x1EDC6F41 (2), 0x7FC00000 (3),
`FF ×16` (3), 20-byte entry / 24-byte header / 2¹⁶ segment, 255 / 65,535, 512 ≤ A
≤ 2⁶², 1 ≤ A_slab ≤ 2⁶², 1 ≤ S ≤ 2⁶³−1, extent_length ≥ 5, dir_offset ≥ 16 /
dir_length ≥ 4, the 128-byte floor, the 65,536-byte discovery window, and all
eight §21.9 guarantees. **Every restatement agrees with every other and with the
defining section.** Appendix B's 27 rows all check out against their cited
sections; the one asymmetry I looked at — the zstd frame magic is in Appendix B
and the LZ4 frame magic (T23) is not — is right, because `[R-COD-06]` *requires*
the zstd magic while the LZ4 frame magic is only named as a thing that must not
appear, so this specification does not fix it.

---

## 3. The register tables as figures

### 3.1 Row and instance counts, derived mechanically

`count_inst.py` parses the four register tables, takes the third pipe-delimited
cell (Instances), and applies §21.1's own counting rule — semicolon-separated
items, a cell reading `—` counting as one:

```
rows: 120   total instances: 277
by prefix rows:      F 35   L 49   T 26   R 10
by prefix instances: F 56   L 116  T 55   R 50
```

§21.2 says "35 conditions" (F1–F36 with F11 struck — 10 + 25 = 35 ✓), §21.3 "49",
§21.4 "26", §21.5 "10". §21.8 says "120 conditions over 277 instances".
**Both totals match to the unit.** I take this as the strongest single piece of
evidence that the register has been maintained mechanically since the last round.

### 3.2 §21.1's stated instance axes, checked row by row

- Two-directional magnitude comparisons: L21 (2 layouts × 2 directions = 4) ✓,
  L22 (4) ✓, L30 (2) ✓, T3 (3 layouts × 2 = 6) ✓, T14 (6) ✓, T22 (6) ✓, F17 (2) ✓,
  F23/L12 (2 each) ✓.
- One-directional (*exceeds*, *larger than*): T21 (3 layouts × 1) ✓, L44 (3) ✓,
  L2 (one direction, 9 named quantities) ✓.
- No magnitude ordering (checksum vs. computed, byte pattern vs. constant):
  F14, F20, L37, L38, T1 all 1 ✓.
- Nonzero value tests (*A ≠ 0*, *S ≠ 0*): L20, L27, L28 all 1 ✓.
- Single predicate over several fields: F25 (MU/PE combination) 1 ✓, F10, F32,
  T12 all 1 ✓.
- Layout-varying quantities enumerated: L44/T21 give 3 (interleaved P·Q, planar
  numeric P·Bᶜ, packed planar bool ⌈P/8⌉) matching §14.2's two rows plus §14.3 ✓.

L2's parenthetical dominance claims are true: P·Q ≥ P·C because each Bᵢ ≥ 1 so
Q = ΣBᵢ ≥ C; and C·N > (C−1)·N + (N−1) = C·N − 1.

### 3.3 §21.3's L1 instance list

Eight fields. I checked whether A or A_slab belong: they do not, because L39 and
L29 already register out-of-range A and A_slab (including "above 2^62"), which
is stricter than 2⁶³−1. Correct as written.

### 3.4 §15.3's counts

"Six rows are marked *structural*" — I counted the table: sentinel-with-crc≠0,
half-sentinel, length 0, offset < 16, field > 2⁶³−1, sum overflow / past F−64 =
six ✓. Three rows are marked *verifier* ✓. The eleven rows map onto §21.4
exactly: T6, T7(×2), T10, T8, T11(×2), then the sum row splits into T12 and T9,
the crc row is T1, and the three verifier rows are L18, F33 and L40/L41/L42.
Nothing in §15.3 is unregistered and nothing in §21.4 is unsourced.

### 3.5 §21.2's reach derivation

"Deriving it there yields F8, F14, F6 and both of F1's instances … and no other
row." `[R-CNT-24]` fixes only: the magic at F−64 (trailer bytes 0–7),
version_major/minor at F−56 (bytes 8–11), the CRC at F−4 (bytes 60–63), and the
front block. That leaves trailer bytes 12–59 — 48 bytes — redefinable, which is
exactly `[R-CNT-24]`'s own "only the remaining 48 trailer bytes". So flags (12),
dir_offset (16), dir_length (24), committed_file_length (32), file_id (40) and
reserved (48) are all redefinable, and F9/F10/F12/F13/F15/F16/F17/F19 correctly
do not reach. F6 and F1 reach through the front block. Derivation confirmed.

I also checked `[R-CNF-13]`'s claim that `[R-CNT-06]` "states nine": the register
rows citing `[R-CNT-06]` as governing rule are F8, F9, F10, F12, F13, F14, F15,
F16, F17 — nine, of which two (magic, CRC) reach. Confirmed; the version gate
and flag gates named in §6.2's ordering are `[R-CNT-07]`/`[R-CNT-08]`, not
`[R-CNT-06]`, so they are not among the nine.

### 3.6 §21.1's specialization pairs

F21⇒F22 (slot (0,0) forces extent_length 0 < 5) ✓; L10⇒L11 ✓; F35⇒F36 ✓;
L24⇒L25 ✓; F1's front-block instance ⇒ F6 ✓; F1's magic instance ⇒ F8 ✓. I looked
for a pair the list misses and that matters: F5's committed_file_length instance
implies *one of* F9/F10/F16 but no single one of them, so it is overlap rather
than specialization, which §21.1 already distinguishes. The one pair I did find
uncomfortable is F2⇒F3, discussed as a finding below.

### 3.7 §21.6's fifteen rows

Every row read against its cited rule; all fifteen agree. The two closing
paragraphs' counts ("Two conditions that once sat in this table"; "Two structural
cases are conforming files a reader nevertheless refuses") are both exactly two
and both enumerate their members.

### 3.8 Other closed counts

§22.2 "Three properties" — three ✓. §22.3 "Four residues" — four ✓. Appendix D
"Six choices" — six ✓. §10.1 "exactly four vehicles" — four ✓, and §4.3's list of
the same four is in the same order with the same members ✓. §17.2 "Three frame
features are excluded" — dictionary/dictionary-ID, content-checksum flag,
oversized window: three ✓, and §18.2's "save two" carve-out from `[R-COD-06]`
names exactly the decoded-size and Window_Size constraints, consistent.
§12.1 "exactly thirteen sample types" — the table has 13 rows, IDs 1–13 with no
gap or repeat, and Appendix C's snapshot lists the same 13 in the same
assignment. §2.2's 19 prefixes: I grepped every `[R-XXX-` prefix actually used
and got 19, the same 19 (`[R-ENC-100]` at line 122 is §2.2's own illustration of
three-digit numbering, not a requirement).

### 3.9 §4.7's promise about layout-table columns

"Layout tables … give, per field: byte offset within the structure, size, type,
name, taxonomy class, and valid range, each table giving the columns its
structure needs. A packed variable-length payload … omits the offset and class
columns … §6.1's block is a 16-byte constant, where a Value column replaces type
and range, and §7.2 folds each field's range into its Field cell."

Checked against all six structure-layout tables: §6.1 is Offset/Size/**Value**/
Class ✓; §6.2, §15.1 and §18.2 are the full six ✓; §7.2 is five with ranges folded
into Field ("type (0 invalid)", "flags: bit 0 MUST_UNDERSTAND …") ✓; §7.4 is
Field/Type/Constraint, offset and class dropped ✓. The promise is kept in every
case. Offsets in §6.2 (0,8,10,12,16,24,32,40,48,60 summing to 64), §7.2
(0,2,4,8,16 summing to 24) and §15.1 (0,8,16 summing to 20) all close exactly,
and "The format-major-1 trailer has zero slack: every byte is assigned" is true.

### 3.10 §8.1's coverage map against §4.5's exception list

§4.5 names three exception classes; §8.1's seven rows realise them. I walked
every field of every structure looking for one covered twice or not at all:
`crc_of_crc_array` sits in the layer record's inline payload, hence inside the
directory region, hence under the directory CRC (one further checksum, as §4.5
says); the segment CRC array is under `crc_of_crc_array`; an entry's `crc` is
under its segment CRC; the tile-index region's two parts are jointly covered
with nothing left over. The three terminal fields (trailer [60,64), directory
final 4, user-metadata extent final 4) are covered by nothing, as stated. No
gap, no double cover.

---

## 4. Findings

Seven. None is byte-level, and I say why for each. The four figure/checklist
restatements (01–04) are the substantive ones; 05 is a genuine ambiguity in a
diagram's notation; 06 and 07 are register-cell defects that §21.1 already
decides but that leave the table wrong.

### diagrams-01 — §5.1's three-commits Example asserts that a commit touching no layer appends nothing but directory, pad and trailer; `[R-LIF-02]` step 2 and §20.3's own figure say otherwise (CONTRADICTION)

§5.1, the Example at L656–688, closes its account of commit 3 with:

> "Layer A's tiles and index have never moved: a layer the commit does not touch
> keeps its extent slot pointing where it always pointed (§20.3, `[R-WRT-05]`),
> so a commit that touches no layer re-emits the directory, the pad and the
> trailer alone."

The inference is from a fact about layers to a claim about *everything a commit
appends*, and it drops the whole file-scope record class. `[R-LIF-02]` step 2 is
explicit that a commit appends "new stored-tile payloads and tile-index regions
for the layers it changes, **and any new record extents (file-scope or
layer-scope)**". A commit that adds or replaces the file's top-level
user-metadata record touches no layer at all — the record is top-level, not a
sub-record — and `[R-CNT-25]` forces its document into an extent ("Each
user-metadata record carries its document in its extent — never inline"), so
such a commit must append that extent. The same is true of a commit that adds a
top-level record of an unknown or experimental type carrying an extent.

§20.3's own three-shapes Example says so in as many words, at L3338–3341, about
the very case:

> "Editing user metadata is not this shape: its document lives in an extent
> (`[R-CNT-25]`), so a new extent is appended and the old one becomes slack, as
> in (b)."

So the document holds both propositions. §20.3's is right and §5.1's is wrong as
written; the repair is presumably "a commit that touches no layer and adds no
record extent", or scoping the claim to the figure's commit 3.

*Byte level: no.* Both passages are inside blocks labelled *Example* and so are
non-normative under `[R-CNF-01]`; `[R-LIF-02]` step 2 governs and is unambiguous.
A writer misled by §5.1 could only fail to append an extent it needed, and a
record whose slot pointed at an extent the writer never wrote would be a
`[R-CNT-13]`/`[R-CNT-02]` violation barred by `[R-CNF-05]` under either reading.
The emittable set does not move. It still tells an implementer what to build,
which is why it is reported.

### diagrams-02 — Appendix H's reader checklist states an acceptance duty §21.6 explicitly denies (CONTRADICTION)

Appendix H, **Conforming reader**, L4690–4692:

> "accepts every conforming file within §21.9's minimum guarantees and reports
> any resource refusal as a limit rather than as corruption (`[R-ERR-04]`)"

`[R-CNF-03]` (§2.3) states the duty with three qualifiers, not one:

> "A reader MUST accept every conforming file of a format major version it
> implements, carrying no top-level record of a type it does not implement with
> MUST_UNDERSTAND = 1 … and none of whose values exceeds the minimum guarantees
> of §21's limits table"

The checklist keeps only the third. §21.6's closing paragraph is the passage that
makes the omission bite, because it names a file that is conforming, whose every
value lies within §21.9's guarantees, and that a conforming reader must
nevertheless refuse:

> "Two structural cases are **conforming files a reader nevertheless refuses**. …
> The second is an **experimental-range top-level record type carrying MU = 1**
> (§10.2, §10.3): `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]`
> makes the file conforming all the same."

An implementer auditing against the checklist, which is exactly what Appendix H
is for ("for implementers auditing their own work"), would mark that reader
non-conforming for rejecting, or would build a reader that accepts. The document
knows this question and answers it twice — in `[R-CNF-03]` and again in
`[R-ERR-04]`, which goes out of its way to say "the two capability refusals
§21.6's closing paragraph names, a foreign format major and an unimplemented
top-level MU = 1 type, are not this ground". The checklist is the one place that
compresses it away.

(The first of §21.6's two cases is partly self-defusing: §2.3 says a file
declaring another major "is neither conforming nor nonconforming under" this
document, so "every conforming file" arguably never reached it. The MU = 1 case
has no such escape — §21.6 calls that file conforming outright.)

*Byte level: no.* Appendix H is headed "(non-normative)" and disclaims its own
authority in its first sentence — "each entry's authority is the requirement or
section cited, never this summary" — and `[R-CNF-03]`, `[R-CNT-15]` and §21.6 all
decide the case in the same direction. A competent implementer resolves to the
rule. The verdict on the disputed file therefore does not fork between two
implementations that read the whole document.

### diagrams-03 — Appendix H's updater checklist drops the five words that make re-emission compatible with editing, and contradicts its own preceding clause (CONTRADICTION)

Appendix H, **Conforming updater**, L4719–4720:

> "re-emits every retained record byte-identically (§20.4)"

`[R-WRT-05]` (§20.4) states:

> "In the new complete directory, an updater MUST re-emit byte-identically —
> header, inline payload, and extent slot — every record it retains **and does
> not logically modify**; a record it modifies is new output under its writer
> obligations (`[R-CNF-05]`)."

"Retains" and "does not logically modify" are two conditions in §20.4, and the
section works to keep them apart: its table preamble says "The table states what
an updater owes a record it does not logically modify", and the whole treatment
of the MU = 1 row turns on the distinction. The checklist collapses them, and the
result contradicts the clause three lines above it in the same entry, which
permits an updater to change a layer's names, grow an extent, and declare or
clear a slab — every one of which is a logical modification of a retained layer
record, and none of which can be re-emitted byte-identically.

The direction of the error is toward over-strictness (an auditor would think
renaming a layer is barred), but it also loses the second half of `[R-WRT-05]`:
that a modified record is *new output under writer obligations* and so must be
validated as such rather than merely copied.

*Byte level: no.* Same grounds as diagrams-02 — non-normative appendix,
self-subordinating, and `[R-WRT-05]` is unambiguous.

### diagrams-04 — §20.3's shape-(c) figure narrows the empty-layer permission from "declarations" to "geometry" while claiming to restate it verbatim (CONTRADICTION)

§20.3's Example, shape (c), L3334–3338:

> "A layer that stored no tile in the generation the commit supersedes is
> re-declared freely, subject to every rule its **new geometry** is subject to,
> which is the same step's permission — a layer the commit itself empties does
> not qualify."

Step 4 itself, L3204–3207, says:

> "A layer that stores no tile in the generation this commit supersedes MAY be
> re-declared freely, subject to every rule its **new declarations** are subject
> to, which is what schema-first creation needs (§11.1)."

The figure asserts identity — "which is the same step's permission" — while
substituting a strictly narrower subject. This document uses *geometry* narrowly
and deliberately: §11.1 is headed "Geometry and its validity floor" and covers
rank, extents, tile extents and channel count; §11.1's own opening separates
"a layer's geometry **and** linearization fields"; §10.4 lists "sample types,
geometry, channel sets and layout, codecs, filters, linearization, fill, and
index location or encoding" as distinct things; §19.3 speaks of "the geometry
floor and its arithmetic (`[R-GEO-01]`–`[R-GEO-03]`)" as one item among a dozen.
So "every rule its new geometry is subject to" leaves out the codec bound
(`[R-COD-07]`), the fill constraints (`[R-TYP-07]`), the A/S exclusivity
(`[R-CNT-16]`), the alignment and slab domains, the value sets of §11.4, §12.2,
§14.1, §15.1, §17.2 and §17.3, and the name rules — all of which step 4's
"declarations" does reach.

A reader of the figure alone could conclude that an emptied-and-re-declared
layer's non-geometry declarations are not rechecked at re-declaration.

I note the third restatement of the same permission drops the qualifier
altogether. §11.1's Rationale, L1646–1648: "A layer that stored no tile in the
generation the commit supersedes may be re-declared freely; a layer the commit
itself empties does not qualify." Three statements of one permission, with three
different qualifiers — none, geometry, declarations — of which only the last is
step 4's.

*Byte level: no.* Both restatements are in labelled blocks (*Example*,
*Rationale*), non-normative under `[R-CNF-01]`. And the substantive consequence
is nil in the emittable-set sense: `[R-CNT-23]`, `[R-TYP-07]`, `[R-COD-07]` and
the rest bind a layer record in any generation independently of §20.3, so a file
written on the narrow reading that broke one of them would carry a register-row
violation and `[R-CNF-05]` bars every conforming writer from emitting it under
both readings.

### diagrams-05 — §20.5's compaction figure marks both index regions with ′ but does not say what ′ means, and on the reading the surrounding prose supplies, one of the two marks is wrong (AMBIGUITY)

§20.5's Example, L3517–3531:

> ```
> input  │front│ A │▓▓▓▓│ B │▓▓│ A: index │▓▓│ B: index │▓▓▓│ dir │pad│ tr │
> output │front│ A │ B │ A: index′ │ B: index′ │ dir │pad│ tr │
> ```
> "… extent slots are re-pointed and each index region any of whose stored
> extents moved is regenerated — the ′ marks (`[R-WRT-07]`)."

Two readings of "the ′ marks":

(a) **′ marks regeneration.** Then `A: index′` asserts that A's index region was
regenerated, which `[R-WRT-07]` licenses only where "the output relocates" one
of that region's stored extents. In the figure, A's tiles are drawn immediately
after `front` in both rows, with no slack between; on the natural reading of the
drawing A's stored extents did not move, so A's index region should have been
**copied** as an ordinary record extent with its slot re-pointed, not
regenerated. Under this reading the figure over-generalises the rule.

(b) **′ marks "re-pointed and/or regenerated"** — the sentence is a compound and
"the ′ marks" attaches to both halves. Then both marks are correct, but the mark
carries no information about which regions were regenerated, which is the one
distinction the surrounding paragraph exists to draw ("the one kind this
operation regenerates rather than copies").

I pick (a), because the sentence the figure's caption points at is specifically
about regeneration and because "Regions, not offsets" disclaims offsets, not the
left-to-right identity of the regions it draws. On (a) the figure is wrong about
A. The distinction is not cosmetic: §20.5 makes regeneration the step at which a
compactor necessarily meets a structurally malformed entry — "regenerating the
region cannot proceed without meeting it, and the violation is thereafter one the
compactor has detected. `[R-WRT-06]` then obliges refusal" — so whether an
unmoved region is regenerated or copied decides whether a compactor is put in
front of a defect it would otherwise not be obliged to look for
(`[R-WRT-09]` "bounds how far a compactor goes looking").

*Byte level: no.* `[R-WRT-07]`'s normative text is unambiguous, and where nothing
moved, a regenerated region is byte-identical to a copied one (same offsets,
lengths, crcs; segment CRCs recomputed over identical entries). The only
divergence is refuse-versus-emit on an input that already carries a
`[R-IDX-03]`-structural violation — a nonconforming input, whose compacted
output would carry the violation and be barred by `[R-CNF-05]` and `[R-WRT-06]`
either way.

### diagrams-06 — §21.3's L14 Condition cell states two of the three alternatives its own Instances cell and `[R-CNT-18]` carry (OBSERVATION)

§21.3, L3722:

> "| L14 | A sub-record does not fit in the layer record's inline payload: its
> 24-byte header is truncated at the payload end, or its inline_length runs past
> that end | sub-record header; sub-record inline_length; **trailing residue** |
> reader | layer access | `[R-CNT-12]` (R-CNT-18, R-ENC-07) |"

`[R-CNT-18]` names three failure modes, not two: "the remaining bytes MUST parse
as zero or more complete sub-records under §7.2's framing with no residue; any
**overrun, truncation, or residue** is a validity error at layer scope." The
Instances cell keeps all three; the Condition cell keeps only overrun and
truncation. The parallel file-scope row states all three: F29 reads "…extends
past the end of the directory's record sequence …, **or bytes remain after the
last complete record**".

Consequences are small but real. §21.1 makes the instance count mechanical from
the cell, so the 277 total is unaffected (I re-derived it: 277). But `[R-VEC-03]`
obliges "at least one vector for each instance it names", and a corpus builder
constructing L14's third vector has to go to `[R-CNT-18]` to learn what condition
it is meant to exhibit, because L14's own condition text does not name it. Under
§21.1's precedence — "where a row and the rule it cites diverge, the rule
governs" — the rule wins and the row is simply incomplete.

*Byte level: no.* §21.1 already decides which of the two governs; only the table
cell is wrong, which changes no verdict.

### diagrams-07 — §21.2's F3 lacks the in-domain qualifier its two sibling rows carry, and adds a "wraps" clause that admits a narrower condition than `[R-ENC-04]` states (OBSERVATION)

§21.2, L3662:

> "| F3 | A sum of a u64 offset and length taken from the file exceeds 2^63 - 1,
> **so the sum wraps** | dir_offset + dir_length; non-layer top-level record
> extent_offset + extent_length | reader | open | `[R-ENC-04]` (R-CNT-06,
> R-CNT-13) |"

Its two siblings — the same condition at the other two scopes — both carry a
qualifier F3 does not:

> "| L2 | A declaration-derived sum or product of a layer exceeds 2^63 - 1
> **although every contributing field is in domain** | … |"
> "| T12 | A non-sentinel tile-index entry's offset + length exceeds 2⁶³ − 1
> **although each field alone is in domain** | … |"

Two things follow. First, without the qualifier F3 is entailed by F2 (a
dir_offset above 2⁶³ − 1 makes dir_offset + dir_length exceed it too), so every
F2 file for that field is also an F3 file; §21.1's specialization rule then
records it against F2, which is presumably the intent, but the row does not say
so where its siblings do. Second, "so the sum wraps" reads two ways: as a gloss
on the consequence in signed 64-bit arithmetic (`[R-ENC-04]`'s "MUST NOT act on a
wrapped or truncated value"), or as part of the condition, in which case a sum of
2⁶³ + 100 — above the domain, but nowhere near wrapping a u64 — would not be F3.
`[R-ENC-04]` states the condition as exceeding 2⁶³ − 1 with no wrap requirement,
so the first reading is the one to take, and I take it.

*Byte level: no.* §21.1's "where a row and the rule it cites diverge, the rule
governs" settles both points; `[R-ENC-04]` is the operative text and the verifier
verdict is not open. Only the row is wrong.

---

## 5. Suspicions I opened and closed

Recorded so a reader can see the lane looked rather than merely reported.

- **Appendix B's "Every named constant this specification fixes, collected."**
  A completeness promise. I walked its 27 rows and then hunted for constants it
  omits: the 128-byte minimum commit growth (§9.2 — a floor, and the 128-byte
  file floor is present), the LZ4 frame magic (T23 — not a value this
  specification fixes, only one it excludes), the 12 reserved trailer bytes and
  the 48 redefinable ones (structure, not named constants), the 255-byte
  user-metadata key cap (covered: §4.6 defines *names* to include user-metadata
  keys, and the row cites §4.6). Nothing missing. Closed.
- **Appendix H's "each class's obligations" — five classes?** §2.3 defines five;
  Appendix H has exactly five entries, in §2.3's order. Closed.
- **Appendix H's conforming-file entry: "no violation row of §21.2–§21.5
  applies."** Read as a sufficient condition this would be wrong, because §21.7's
  unwitnessed violations carry no row. But the entry's first clause is "every
  requirement at every scope holds (§2.4)", which is the definition, and the
  clauses are a conjunction of necessary conditions. Closed as not a defect.
- **Appendix H's verifier entry against the verifier-detected rows.** I listed
  every row with Detector = verifier (F7, F25–F28, F33, F36; L18, L25, L40–L42,
  L46–L49; T2, T4, T5, T26) and found each represented: coverage/slack, overlap,
  record flag bits, front block, pre-trailer gap, reserved-range types, alignment
  and slab, decoded content, member ordering. Closed.
- **Appendix H's updater entry narrowing "extended at its end, or shortened from
  its end" to "a planar channel added or removed at the end" (singular).**
  Too thin to file: the singular reads as a category, not a count, and no rule
  turns on it.
- **§20.1's appender gloss — "adding layers or records, superseding tiles,
  growing extents, amending metadata".** This is the shape the round warns about:
  a gloss written under an older rule. I checked every item against §20.3 step
  4's closed list and every one is still permitted; the list is illustrative
  (introduced by a colon, no exhaustiveness claim) and omits only further
  permitted operations, never a forbidden one. Closed.
- **§13.3's sparse-writing Note: "among the declaration changes §20.3 permits a
  layer that stores a tile, only a change to entry_count does" [change the index
  content].** I tested each permitted change: names touch no entry; an extent
  growth that leaves entry_count unchanged touches no entry (and §11.1 gives the
  only way that happens — a zero grid count holding the product at 0, in which
  case there are no entries at all); a planar channel added or removed changes
  entry_count; declaring or re-establishing an alignment or slab either finds the
  existing offsets already satisfying the invariant, or is not available without
  re-storing tiles, which is a stored-tile-set change in its own right. The claim
  holds. Closed.
- **§23.1's "That is every case: no commit turns a real position of a stored tile
  into padding."** A real position becomes padding only by an extent shrink or a
  tile-extent change, both of which §20.3 step 4 sends to a rewrite; growth only
  adds real positions; a planar channel removal takes tiles out of the addressed
  set rather than making positions padding. Closed.
- **§20.3 step 4's claim that "Between them the two lists reach every declaration
  field of §7.4."** I walked §7.4's sixteen table rows and placed each: name,
  A, S, A_slab, dimension names, dimension extents, channel names on the
  permitted side; layout, linearization, codec, filter, rank, dimension order,
  tile extents, channel types, fills, index_encoding on the fixed side;
  channel count on both, resolved by the stated both-sides rule; entry_count,
  crc_of_crc_array and the extent slot as consequences; sub-records to §20.4.
  Complete. Closed.
- **§20.4's three-row table as a partition of (MU, PE).** All four combinations
  land: MU=1/PE=1 and MU=1/PE=0 (read as PE=1 by `[R-CNT-12]`) on row 1,
  MU=0/PE=1 on row 2, MU=0/PE=0 on row 3; and the preamble's restriction of row 1
  to unimplemented types keeps a layer record editable. §2.4's preserve-verbatim
  row names exactly rows 1 and 2. Closed.
- **§17.2's Note "§14.2's worked examples give 18 and 30 bytes".** §14.2's example
  also names a 12-byte planar tile, but the two figures the Note quotes are the
  two the example labels *decoded size*, and every one of the three is under
  1 KiB so the Note's conclusion is unaffected. Closed.
- **§21.9's "The last three rows are per-instance … The first five rows range over
  declarations."** Three plus five is the table's eight rows, and the split falls
  where the prose says. Closed.
- **`[R-VEC-03]`'s "every hard limit of `[R-ERR-05]`" against §21.9's "The hard
  limits it restates are a finding aid rather than an inventory."** A coverage
  obligation keyed to a list that disclaims being a list. I enumerated the hard
  limits I could find that `[R-ERR-05]` does not print — the ≥ 5 user-metadata
  extent, inline_length exactly 1, F a multiple of 64, the entry_count
  cross-check — and every one carries a register row (F22/L11, F23/L12, F13, L21)
  whose instances `[R-VEC-03]`'s first clause already covers. Harmless. Closed.
- **The §5.1 and §9.2 box-drawing alignment.** I counted columns by hand for
  §5.1: the under-box annotation's `└`/`┘` land on divider columns 8/20, 28/40 and
  48/69, spanning layer A, layer B, and dir₃+pad+trail₃ exactly. §20.3(a)'s
  annotation spans columns 14–30 and 31–44, which align with both the *before* and
  *after* rows (" dir₁│pad│tr₁│" is 14 columns, exactly the ▓ run plus its
  divider). §9.2's `↑ F` sits one column past the closing `│`, which is correct —
  F is one past the last byte. Nothing misaligned. Closed.
- **The three-shapes figure's shape (c) list of directory-only changes.** Clearing
  a slab declaration, renaming a layer and dropping a PE = 0 record are all
  directory-only; §11.1's "Growth that leaves entry_count unchanged touches the
  directory alone" adds a fourth the list does not name, but the list is
  introduced without an exhaustiveness claim. Closed (the (c) defect I do file is
  the "new geometry" one).
- **§19.1/§19.3's enumerations against the register's Detected column.** I mapped
  every F-row detected at *open* and every L-row detected at *layer access* onto
  §19.1 step 4's and §19.3's cited rules, and each is reachable. §19's preamble
  disclaims exhaustiveness explicitly ("Those enumerations are not the complete
  inventory … §21's register is"), so the gaps I found (e.g. §19.3 cites
  `[R-CNT-18]` rather than `[R-CNT-12]` for a type-0 sub-record) are licensed.
  Closed.
- **A missing register row.** I went through the requirement list looking for a
  detectable file-conformance violation with no row: `[R-SLB-04]`'s stale slab
  declaration (§16.2's Note explains its absence and points at L41/L42),
  `[R-CNT-18]`'s nesting prohibition (§7.4's Note explains its absence and points
  at L26), `[R-ENC-06]`'s field widths (§21.7 explains it states no condition a
  file can exhibit), `[R-MTA-06]`'s unregistered `tarn.` key (a conduct rule
  `[R-CNF-02]` names by section), `[R-LIF-01]`/`[R-LIF-02]` (no single-file
  witness). Every absence is accounted for in the text. Closed.
- **Table cell-count integrity.** `tablecheck.py` found no row in any of the 25
  tables whose cell count differs from its header. Closed.

## 6. Where I found little, and what I did that would have found something

The worked examples and the byte layouts are the part of my charter where I found
nothing at all, and I want to be precise about what that rests on. I did not
eyeball any of them. I rebuilt both hex dumps byte by byte from the document's own
printed rows, asserting each row's printed offset against the running length so a
one-byte drift anywhere would have thrown; I re-parsed the layer-record payload
strictly in §7.4's declared field order and confirmed it consumes exactly 81
bytes with zero residue; I decoded every trailer field at the offset and width
§6.2's layout table gives rather than at the offsets Appendix A's annotation
claims, so a disagreement between dump and annotation would have surfaced as a
decode mismatch rather than being read past; and I wrote CRC-32C from §4.5's
stated parameters and ran it over the reassembled bytes for all six printed
checksums, including the 1.31 MB all-sentinel segment. Any wrong constant, wrong
offset, wrong width or wrong checksum in either dump would have shown up as a
concrete numeric disagreement, and none did. Likewise the register: I derived
120 rows and 277 instances mechanically from the cells and compared them against
§21.2–§21.5's four stated counts and §21.8's stated pair; a single added,
dropped or re-punctuated cell would have broken one of the five numbers.

My confidence that the *arithmetic* surface is clean is high. My confidence that
the *restatement* surface is clean is lower, and that is where all seven findings
sit: figures and checklists that paraphrase a rule stated elsewhere. Those are
judgement calls about English, not arithmetic, and a different reader would
plausibly grade some of 05–07 as non-defects. I have said for each what closes it.
