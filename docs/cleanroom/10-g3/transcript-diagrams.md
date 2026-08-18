# Round 10 — Diagram auditor working transcript

**Access disclosure.** I opened exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,919 lines), read end to end in five `Read` calls. I ran `wc -l` and `grep`/`python3`
against that file only, plus three self-contained Python scripts I wrote into my own
scratchpad (`crc.py`, `appa.py`, and inline heredocs) that read nothing but the spec text
and literals I typed. I did not open `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`README.md`, `CONTRIBUTING.md`, `conformance/`, or `spec/registry.json`. I ran no git
command, no web search, no web fetch, and did not list any directory. Where prior knowledge
of zstd/deflate/LZ4/CRC-32C generated a suspicion, I settled it against the document's own
text or against arithmetic I performed here, never against outside authority — the two
places I leaned on external formats (RFC 8878's 1 KiB minimum window, the LZ4 frame magic)
I have flagged in-line as suspicion-only and did not turn into findings.

---

## Phase 1 — Enumeration

I enumerated every figure, byte-layout box, ASCII diagram, worked example, table that
restates a rule, checklist, and numbered list before judging any of them. Line numbers are
the first line of the object.

### Fixed-layout / byte-layout tables
| line | object |
|---|---|
| 659 | §6.1 front signature block layout (Offset/Size/Value/Class) |
| 702 | §6.2 trailer layout (Offset/Size/Type/Field/Class/Valid values) |
| 866 | §7.2 record header (Offset/Size/Type/Field/Class) |
| 966 | §7.4 layer-record inline payload (Field/Type/Constraint) |
| 1890 | §15.1 tile-index region layout box (blockquote ASCII) |
| 1895 | §15.1 index entry (Offset/Size/Type/Field/Class/Valid values) |
| 2329 | §18.2 user-metadata inline payload (Offset/Size/Type/Field/Class/Valid values) |

### Tables that restate rules stated in prose elsewhere
| line | object |
|---|---|
| 227 | §2.4 outcome-class table (5 rows incl. preserve-verbatim) |
| 937 | §7.3 record types of format major 1 |
| 1040 | §8.1 checksum coverage map (7 rows) |
| 1302 | §10.2 numeric identifier spaces (8 rows) |
| 1497 | §12.1 sample types (13 rows) |
| 1727 | §14.2 decoded size / offset-of-value-k |
| 1943 | §15.3 entry validity (11 rows) |
| 2453 | §18.4 standardized keys (6 rows) |
| 2886 | §20.4 updater preservation obligations (3 rows) |
| 3062 | §21.2 file-scope register (F1–F36) |
| 3106 | §21.3 layer-scope register (L1–L49) |
| 3163 | §21.4 tile-scope register (T1–T26) |
| 3204 | §21.5 ignored records (R1–R10) |
| 3222 | §21.6 conditions that are not violations (14 rows) |
| 3309 | §21.9 minimum-guarantee limits (8 rows) |
| 3662 | Appendix B constants (24 rows) |
| 3690 | Appendix C registry snapshot |
| 3757 | Appendix E changelog |

### ASCII diagrams
| line | object |
|---|---|
| 563 | §5.1 "a file after three commits" |
| 1119 | §9.2 "what a crash sees" (3 rows) |
| 2824 | §20.3 commit shape (a) new layer |
| 2840 | §20.3 commit shape (b) tiles added |
| 2860 | §20.3 commit shape (c) directory-only |
| 2964 | §20.5 "what compaction reclaims" |
| 3615 | Appendix A hex dump (8 lines, 128 bytes) + annotation table at 3626 |

### Worked numeric examples
| line | object |
|---|---|
| 499 | §4.6 `température` NFC/NFD byte counts |
| 553 | §5.1 smallest conforming file |
| 1414 | §11.2 grid arithmetic |
| 1468 | §11.4 spatial / in-tile / disk ordinals |
| 1531 | §12.1 bfloat16 1.0 and quiet NaN |
| 1580 | §12.3 channel entry, 12 bytes |
| 1648 | §13.3 rgb fill tuple |
| 1769 | §14.2 interleaved / planar byte offsets |
| 1803 | §14.3 packed bool tile, fill false / true |
| 1859 | §14.5 edge tile, 32 bytes |
| 1983 | §15.4 entry_count = 1,000,000 |
| 1998 | §15.4 planar disk ordinal 74 |
| 2095 | §16.2 slab runs |
| 2276 | §17.3 byte-shuffle of three float32 |
| 2810 | §20.3 superseding one tile |

### Checklists / numbered lists that promise completeness
| line | object |
|---|---|
| 41 | §1 design pillars (5, no count claimed) |
| 1279 | §10.1 four growth vehicles |
| 1085 | §9.2 commit protocol steps 1–6 |
| 2514 | §19.1 open, steps 1–4 |
| 2638 | §19.4 tile read, steps 1–8 |
| 2762 | §20.3 append procedure, steps 1–6 |
| 2378 | §18.2 "Four restrictions apply" |
| 470 | §4.6 "three further constraints" |
| 2167 | §17.2 "Three frame features are excluded" |
| 3381 | §22.2 "Three properties" |
| 3422 | §22.3 "Three residues" |
| 3717 | Appendix D "Six choices" |
| 3792 | Appendix G reproducible-writer profile, items 1–9 + closing count |
| 3862 | Appendix H conformance checklists (5 classes) |

---

## Phase 2 — Arithmetic and byte verification

Everything below I computed rather than eyeballed. Scripts in the scratchpad.

### Appendix A, byte by byte (line 3615)
I parsed the hex dump, checked offsets are contiguous, decoded every trailer field, and
recomputed the CRC-32C over trailer bytes [0,60).

```
file length 128
magic 8a 4e 52 41 54 0d 0a 1a       -> matches §6.2's constant
version_major 1  version_minor 0  flags 0
generation 1  dir_offset 16  dir_length 4
committed_file_length 128            (= file size, multiple of 64)
file_id 0x0123456789abcdef           (LE bytes EF CD AB 89 67 45 23 01)
reserved 00 00 00 00
computed trailer CRC = E00938D2  stored = E00938D2  MATCH
dir region [16,20) = 00 00 00 00 ; CRC-32C(zero bytes) = 00000000  MATCH
pad [20,64) all zero, 44 bytes       (annotation says "44 bytes")  MATCH
```
Every one of the 13 annotation rows is correct, the hex dump is internally consistent, and
`F mod 64 = 0`, `dir_offset >= 16`, `dir_length >= 4`, `dir_offset + dir_length <= F - 64`
(20 <= 64) all hold. Appendix A is clean.

I also checked the prose after the dump. "112 bytes covering [16, 128) contains the
directory" — 128 - 16 = 112, correct, and [0,16) stays non-resident so `[R-CNT-04]`'s
residency test correctly leaves the front-block check optional. "§19.1's four-step open" —
§19.1 does have exactly four steps.

### §4.5's check vector and §15.4's sentinel-segment constant
```
CRC-32C("123456789") = 0xe3069283   (spec: 0xE3069283)  MATCH
CRC-32C(b"")         = 0x0          (spec: 0x00000000)  MATCH
CRC-32C(65536 x "FF*16 00*4"), 1,310,720 bytes = 0xeecb3bb2
                                    (spec §15.4 and Appendix B: 0xEECB3BB2)  MATCH
```
Note the sentinel segment is 1,310,720 bytes = 1.25 MiB exactly, which is the figure
§15.4's example quotes for "one full segment (1.25 MiB)".

### §5.1's 128-byte floor
Minimum `F` with `F mod 64 = 0` and `16 + 4 <= F - 64` is `F = 128`. `[R-CNT-27]`'s
justification is arithmetically sound.

### §11.2 / §11.4 (lines 1414, 1468)
extents (1024,2048), tiles (256,256): G = (4,8), N = 32, P = 65,536 — all match.
`ceil(1000/256) = 4` — matches. Coordinate (300,700): t = (1,2), u = (44,188),
s = 1*8 + 2 = 10, in-tile ordinal 44*256 + 188 = 11,452, planar c=2 disk ordinal
2*32 + 10 = 74. Every number in the example matches.

### §14.2 (line 1769)
P = 6; a:uint8, b:uint16 -> Q = 3, decoded 18, ordinal 5 at byte 15, `b` at 16–17. Planar
`b`: 12 bytes, ordinal 5 at bytes 10–11. t:float32 + m:bool -> Q = 5, decoded 30, ordinal 5
at [25,30), `m` at 29. All match. The general form `u*Q + F^c` with `k = u*C + c` reduces
correctly to the table's `(k div C)*Q + F_{k mod C}`.

### §14.3 (line 1803)
P = 10, alternating true/false from ordinal 0: bit k of byte k div 8. Computed `55 01`
with fill false and `55 fd` with fill true (pad bits are positions P mod 8 = 2 through 7).
Both match. `ceil(10/8) = 2` bytes.

### §14.5 (line 1859)
extents (5,5), tiles (4,4) -> grid 2x2; tile (1,1) covers 4..7 on both axes; exactly one
real position (4,4) and 15 padding; P*B = 16*2 = 32 bytes; fill 0xABCD little-endian is
`CD AB`. All match.

### §15.4 (lines 1983, 1998)
entry_count 1,000,000 -> 16 segments, last covering 16,960 entries, CRC array 64 bytes,
region 20,000,064 bytes. k = 999,999 is in segment 15 at segment-relative byte 339,180;
CRC array at [20,000,000, 20,000,064); segment 15 at [19,660,800, 20,000,000). All match.
Second example: disk ordinal 74 -> region bytes [1480,1500); channel 3's block is entries
96..127, 32 entries. Both match.

### §16.2 (line 2095), §17.3 (line 2276), §20.3 (line 2810)
Slab runs [0,8),[8,16),[16,24),[24,32) for N = 32, S = 8; tile rows 1–2 = ordinals 8–23 =
runs 1 and 2. Correct.
Shuffle: 1.0/2.0/3.0 float32 LE = `00 00 80 3F 00 00 00 40 00 00 40 40`; applying
`byte i of group j -> offset i*n + j` with s = 4, n = 3 gives
`00 00 00 00 00 00 80 00 40 3F 40 40`, byte-identical to the example.
Index region for 32 tiles: 32*20 + ceil(32/65536)*4 = 644. Matches.

### §12.3 (line 1580), §4.6 (line 499), §12.1 (line 1531)
Channel entry `temp`/float32/0x7FC00000 encodes as
`04 74 65 6d 70 0c 00 04 00 00 c0 7f`, 12 bytes — byte-identical to the example.
`température` NFC = 12 bytes with the quoted byte string; NFD = 13 bytes. Both correct.
bfloat16 1.0 = 0x3F80 stored `80 3F`; 0x7FC0 <-> binary32 0x7FC00000. Correct.

### §21.9's note (line 3330)
Segment-CRC array at entry_count 2^32 is (2^32/2^16)*4 = 262,144 B = 256 KiB; at 2^36 it is
4 MiB. Both figures check out.

---

## Phase 3 — The register (§21.2–§21.5) under the re-labelling

The brief warned that rows were removed and the remainder renumbered, so every citation of a
row label is newly suspect. I did two mechanical checks.

### 3a. Row counts and instance counts

I parsed the four register tables and counted rows, and counted instances by the rule §21.1
states ("Instances within a cell are separated by semicolons, and a cell reading — is one
instance").

```
§21.2  rows: 36  instances: 53   ids F1..F36   (header claims "36 conditions")   OK
§21.3  rows: 49  instances: 106  ids L1..L49   (header claims "49 conditions")   OK
§21.4  rows: 26  instances: 45   ids T1..T26   (header claims "26 conditions")   OK
§21.5  rows: 10  instances: 44   ids R1..R10   (header claims "10 conditions")   OK
TOTAL  121 conditions, 248 instances
```
§21.8 claims "121 conditions over 248 instances". Both numbers are exactly right, and the
ids are contiguous with no gap or duplicate in any of the four tables. This is the single
strongest evidence I found that the re-labelling was done consistently.

### 3b. Every row-label citation, resolved against the row it lands on

I grepped every `F<n>` / `L<n>` / `T<n>` reference outside the tables and checked each
against the row it names:

- L1216 §9.6: "fails `[R-CNT-06]`'s gates on the bytes handed over (§21.2 rows F8 and F17)".
  F8 = trailer magic not exactly `8A 4E 52 41 54 0D 0A 1A`; F17 = committed_file_length not
  equal to the transport-authoritative size. Both are exactly the two gates a residue-past-a-
  commit file trips. **Correct.**
- L2159 §17.2: "`[R-COD-08]` rejects it (§21.4, T24)". T24 = "The decode does not consume the
  entry's length exactly — bytes remain in the stored extent after the stream, frame, or
  block ends", governed by `[R-COD-08]`. **Correct.**
- L3021 §21.1: "F1 of F6 and of F8, F35 of F36, L24 of L25". F1 (byte-reversed signature
  constant, instances front block + trailer magic) is strictly narrower than F6 (front block
  not byte-identical) and F8 (the 8 bytes at F-64 are not the magic). F35 (reserved-range
  top-level type with MU = 1, reader/open) is strictly narrower than F36 (reserved-range
  top-level type whatever its MU bit, verifier/certification). L24/L25 are the same pair at
  layer scope. **All three specialization claims correct.**
- L3040/3042 §21.1: "(T24's *any codec*)" and "(T15, T25)". T24's Instances cell is literally
  `any codec` (one instance); T15 enumerates zlib vs gzip (2), T25 enumerates deflate/zstd/lz4
  malformations (3). **Correct.**
- L3096 F33: "caught by the bounds rows F9/F10, F31/F32, L16/L17 and T8/T9, each at its own
  tier". F9 = dir_offset < 16, F10 = dir_offset+dir_length > F-64; F31 = non-layer top-level
  extent_offset in 1..15, F32 = that extent past F-64; L16 = layer/sub-record extent_offset
  < 16, L17 = that extent past F-64; T8 = entry offset < 16, T9 = entry extent past F-64.
  **All eight correct, and they do partition into (front block, trailer) x (directory,
  top-level record extent, layer/sub-record extent, tile extent).**
- L3177 T13: "the check that detects it is T25's" — T25 is the malformed-stream row. Correct.
- L3190 T26: "the check that detects it is T2's or T4's". I stress-tested this one: could a
  mis-strided *packed bool plane* be detectable only by T5 (pad bits), which T26 does not
  name? Working it out: the shuffle maps original byte p = j*s + i to i*n + j, so the last
  byte (i = s-1, j = n-1 -> p = n*s - 1 = L-1) is a fixed point of the permutation for every
  s. Pad bits therefore always survive a wrong stride, so T5 can *never* detect one, and
  T26's "T2's or T4's" is exactly right. **Correct — my suspicion was wrong.**
- L3228 §21.6: "emitting one is a violation (F36, L25)". Correct pair.
- L3264–3266 §21.6: "(F18, `[R-CNT-07]`)" for version_major = 0 and "(F35, F36, L24, L25)"
  for reserved-range types. **All four correct.**
- L3910–3911 Appendix H: "(`[R-CNT-05]`, F7)" — F7 is the pre-trailer-gap structure row,
  verifier/certification, governed by `[R-CNT-05]`. "(`[R-CNT-15]`, F36, L25)" — correct.

**Verdict on the re-labelling: I found no citation that lands on the wrong row.** That is the
thing the brief pointed me at hardest, and it comes back clean.

### 3c. Governing rules and scope placement

I extracted the Governing-rule cell of all 121 rows and checked the scope split. The
partition is disciplined and I could not break it:

- Every `[R-CNT-13]` extent-slot condition appears twice — once for non-layer top-level
  records at file scope (F30/F31/F32) and once for layer records and sub-records at layer
  scope (L15/L16/L17) — matching §7.2's "the layer for a layer record and for sub-records,
  the file for other top-level records".
- `[R-CNT-12]`'s flag conditions likewise split F25/F26 (non-layer top-level) against
  L46/L47 (layer record or sub-record), and `[R-CNT-22]`'s stored-flag mismatch splits
  F28 against L49. No record can fall in both or neither.
- F29 correctly places a *layer* record whose header overruns the directory sequence at
  **file** scope, because `[R-CNT-12]` scopes the sequence, not the record.
- L3/L5/L6 (layer-record name) carry Detected = **open** while L4/L7/L8 (dimension/channel
  names) carry **layer access** — exactly matching §19.1 step 4 versus §19.3.
- L37/L38 carry Detected = **tile use** with outcome reject-layer, matching §19.2's
  "index-chain failures take layer scope although their detection point is tile use".
- §15.3's table says "Six rows are marked *structural*"; I counted the table: 6 structural,
  1 valid sentinel, 1 crc-failure, 3 verifier = 11 rows. The six structural rows map onto
  T6, T7, T10, T8, T11, and T12+T9 (the last row splits into overflow and bound). Complete.

### 3d. Value-set rows against §10.2 and the defining sections

L31 (index_encoding), L33 (linearization), L34 (sample type), L36 (layout), L43 (codec),
L45 (filter) each enumerate 0 / the reserved sub-ranges / the experimental range. I checked
every sub-range against both §10.2's table and the owning section:

| row | instances | §10.2 | owning section |
|---|---|---|---|
| L31 | 0; 2–0x7F; >= 0x80 | u8, assigned 1, res 2–0x7F, exp >= 0x80 | §7.4 table cell verbatim |
| L33 | 0; 2–3; 4–0x7FFF; >= 0x8000 | u16, assigned 1, res 2–0x7FFF | §11.4 splits 2–3 / 4–0x7FFF |
| L34 | 0; 14–19; 20–0x7FFF; >= 0x8000 | u16, assigned 1–13, res 14–0x7FFF | §12.2 splits 14–19 / 20–0x7FFF |
| L36 | 0; 3–255 | u8, assigned 1,2, res 3–255, exp none | §14.1 |
| L43 | 0; 5–0x7FFF; >= 0x8000 | u16, assigned 1–4 | §17.2 |
| L45 | 0; 3–0x7FFF; >= 0x8000 | u16, assigned 1,2 | §17.3 |

All consistent. §10.2's collapsing of §11.4's and §12.2's two reserved sub-ranges into one is
harmless because §10.2's row is the union.

Note the deliberate asymmetry I checked rather than assumed: an *experimental* value in these
six spaces IS a violation (reject-layer), while an experimental *record type* or *metadata
encoding* is not. `[R-EXT-03]` states exactly that split, §21.6 carries the two
non-violation rows, and R1 correctly covers only encoding 0 and reserved 3–0x7F. Consistent.

### 3e. §21.6 and the two paragraphs after it

"Two conditions that once sat in this table are violations and are registered above" —
unsorted members and registered-type stored-flag mismatch: these are F27/L48 and F28/L49,
all four present, all detector *verifier*, on the stated precedent of `[R-CNT-12]`'s
reserved-flag rows (F26/L47, also verifier). Consistent.

"§21.6's closing paragraph names the other two" (cited from `[R-CNF-03]` at §2.3): the two
conforming-files-a-reader-refuses are version_major and experimental MU = 1, and they are
indeed named in the last paragraph of §21.6, with the resource ground handled separately by
`[R-ERR-04]`. Correct.

---

## Phase 4 — Cross-checks that came back clean (recorded so coverage is checkable)

- **§8.1's coverage map** against §4.5's three exception classes. Terminal (comparison-only)
  checksums = trailer, directory region, user-metadata extent — exactly the three §4.5 names.
  Interior (comparison-verified AND covered) = each segment CRC array, each entry crc field,
  each crc_of_crc_array — I traced each: entry crc is inside the segment the segment CRC
  covers; the segment CRC array is covered by crc_of_crc_array; crc_of_crc_array sits in the
  layer record's inline payload inside the directory region. Chain closes. For format major
  1 the map's seven rows cover every byte of every structure: layer-record and sub-record
  headers and payloads fall under the directory row, user-metadata extents under row 6,
  unassigned-type extents under row 7 (uncovered by design).
- **§2.4's outcome table** row for preserve-verbatim says "§20.4's table states the cases: its
  MU = 1 and MU = 0 / PE = 1 rows" — §20.4's table has exactly those two rows plus MU = 0 /
  PE = 0. Correct.
- **§7.3's record-type table** against §10.2 (assigned 0x0001, 0x0002) and Appendix C. All
  three agree, and `[R-EXT-05]`'s precedence rule covers any future divergence.
- **§12.1's sample-type table**: 13 rows, element sizes 1/1/2/4/8/1/2/4/8/2/2/4/8, "the twelve
  types other than bool" = 13 - 1. Appendix C's shorthand `2–5 int8/16/32/64 · 6–9
  uint8/16/32/64` maps exactly onto rows 2–9. §12.2's pinned reservations 14,15 (OFP8 E4M3,
  E5M2), 16,17,18 (int128, uint128, float128), 19 (raw bytes) match Appendix C's "19 opaque".
- **§18.4's six standardized keys** against Appendix C's six. Match, scopes included.
- **§21.9's limits table** against Appendix B's "Reader minimum guarantees" row: all eight
  quantities and values identical (rank 32, C 4096, entry_count 2^32, 65,536 layers,
  16 MiB directory, 256 MiB tile, 16 MiB metadata document, 8 MiB zstd window).
- **Appendix B's other 23 rows** each traced to their defining section; every constant I
  could compute (CRC parameters, check vector, sentinel bytes, all-sentinel segment CRC,
  128-byte minimum, 24-byte header, 20-byte entry, 2^16-entry segment, `0x7E000000`,
  `28 B5 2F FD`, discovery window 65,536) is correct.
- **Numbered lists**: §9.2 (1–6), §19.1 (1–4), §19.4 (1–8), §20.3 (1–6), §10.1 (1–4),
  Appendix G (1–9) — all sequential, none duplicated, none missing. Every cross-reference to
  a step number resolves ( `[R-LIF-02]` "steps 3 and 5" from §5.1 = directory and pad+trailer;
  "steps 1–2", "step 3", "steps 4–6" from §20.3; "steps 4–6 — both barriers, not one" from
  §20.2; §19.4 step 3's "Steps 3 through 6 run once per needed entry").
- **Counted claims**: "five classes" (§2.3) = 5; "four vehicles" (§4.3, §10.1) = 4 and the two
  lists agree item for item; "three further constraints" (§4.6) = 3; "Four restrictions"
  (§18.2) = 4; "Three frame features are excluded" (§17.2) = dictionary ID, content-checksum
  flag, window size = 3; "Three properties" (§22.2) = 3; "Three residues" (§22.3) = 3;
  "Six choices" (Appendix D) = 6; "exactly thirteen sample types" = 13. All hold.
- **ASCII diagrams**: §5.1's three-commit figure has two slack runs and describes them as
  "the directories, pads and trailers of commits 1 and 2" — consistent with a creation commit
  for layer A, a second commit adding layer B, and a third touching no layer. §9.2's crash
  figure marks the right bytes in each of its three rows. §20.3's three shapes (a)/(b)/(c) are
  each consistent with `[R-WRT-04]`/`[R-WRT-05]`; I specifically checked shape (c)'s
  fill-change case and it is correctly fenced ("on a layer with no padding position and no pad
  bit"), because `[R-SER-05]` would otherwise force stored tiles to be re-emitted. §20.5's
  compaction figure agrees with `[R-WRT-06]`/`[R-WRT-07]` including the fresh file_id and
  generation 1.
- **Identifier hygiene**: 160 distinct `[R-*]` identifiers; every prefix is gapless
  (`R-ENC-100` is §2.2's own illustration of numbers above 99; `R-SER-04` appears only in
  §14.4's withdrawal note, as §2.2's retirement rule requires). `[R-VEC-04]` precedes
  `[R-VEC-03]` in document order, which §2.2 expressly licenses ("Identifier order carries no
  meaning").

---

## Phase 5 — Findings

### diagrams-01 (CONTRADICTION) — Appendix G's closing count of what the profile adds is wrong

Appendix G, after nine numbered items, says:

> "Everything else the profile needs is already mandatory — fill-encoded edge padding
> (`[R-SER-05]`) and explicitly recorded fill (`[R-TYP-06]`) among them. Four things are not,
> and the items above are where the profile adds them: gap *content*, which `[R-CNT-03]` only
> advises; gap *extent*, which placement freedom (`[R-SLB-05]`) leaves open; sub-record order
> within a layer record's inline payload, which `[R-CNT-14]` leaves free; and the fill a
> writer records when its caller chooses none, which `[R-TYP-10]` states as a SHOULD."

At least five of the nine items add something that is neither already mandatory nor among
those four:

- **Item 6** — "**The sentinel for every all-fill tile**, so that a tile whose samples all
  equal fill is never stored". Nothing in §13, §15 or §20 requires a writer to leave an
  all-fill tile unstored; `[R-IDX-02]` defines the sentinel and `[R-TYP-08]` defines what an
  unstored tile reads as, but storing an all-fill tile is fully conforming. Item 7's own text
  concedes this: "item 6 stores no tile whose samples all equal fill, so two writers that
  default fill differently disagree about *which tiles exist*". Which tiles exist is not gap
  content, gap extent, sub-record order, or default fill.
- **Item 3** fixes *top-level record* order ("Records are ordered by type, and within type
  0x0001 by layer name") and the layer/structure emission order. The closing names only
  "sub-record order within a layer record's inline payload"; `[R-CNT-14]` leaves top-level
  record order equally free, and item 3 says so itself ("record order carries no meaning
  (`[R-CNT-14]`), so it is otherwise free to vary").
- **Item 2** replaces §9.3's SHOULD-random `file_id` with a deterministic hash.
- **Item 4** requires "One generation"; nothing in §9 constrains a file to one commit.
- **Items 1 and 9** pin an encoder implementation/version/settings and a JSON writer; §17 and
  §18 constrain neither.

An implementer using the closing paragraph as the delta between core conformance and the
profile — which is what it is written to be — will under-implement the profile, and two
"profile-conforming" writers will still not produce byte-identical files.

Byte-level: **no.** Appendix G is labelled non-normative and states "It adds no requirement to
any actor", so nothing here changes what a conforming implementation may emit or must accept.

### diagrams-02 (AMBIGUITY) — Appendix G item 2's `file_id` hash input is not determined

> "2. **`file_id` from a cryptographic hash of the file's own emitted bytes**, computed over
> [0, F − 64) together with the trailer's other fields with the `file_id` field taken as zero,
> then written in."

Three readings are defensible and they yield different `file_id` bytes:

(a) The hash covers [0, F−64) plus trailer bytes [0,48) and [56,64) with [48,56) zeroed —
i.e. "other fields" includes the trailer CRC at [60,64). Since the CRC covers trailer bytes
[0,60), which include `file_id`, this is circular and unimplementable unless one also fixes an
order: build the trailer with `file_id` = 0, compute the CRC over that, hash, write `file_id`,
then *recompute* the CRC. The text says only "then written in" and never mentions recomputing.

(b) "the trailer's other fields" means the trailer's *content* fields — magic, versions,
flags, generation, dir_offset, dir_length, committed_file_length, reserved — excluding both
`file_id` and the CRC, on the ground that the CRC is a checksum rather than a field. §6.2's
layout table works against this reading: it lists "trailer CRC" as a Field, on the same
footing as the rest.

(c) The hash covers only [0, F−64) and the trailer fields are decorative in the sentence.

I picked **(b)**, because it is the only reading that is implementable without an unstated
recompute step and because item 2's stated purpose ("Hashing the bytes rather than an abstract
notion of 'content' is what makes the identifier well defined") is defeated if the derivation
needs an order the text does not give. But the profile's entire point is cross-implementation
byte identity, and this item does not deliver it: two profile implementations picking (a) and
(b) emit different bytes at trailer offset [48,56) and, consequently, a different CRC.

Byte-level: **no.** Appendix G is non-normative and "adds no requirement to any actor"; any
nonzero `file_id` is conforming under `[R-CNT-06]`, so both implementations emit conforming
files. The divergence is confined to the profile.

### diagrams-03 (AMBIGUITY) — §4.7's field taxonomy does not derive the Class column that §6.2 prints, and §7.4 asks implementers to derive it anyway

§4.7 defines the trichotomy as a residual chain:

> "A field is **structural** if its value determines how any byte is located or decoded;
> **semantic** if not, but its value determines what decoded values mean; and **descriptive**
> if neither — its value determines nothing a conforming reader does, and a reader MUST NOT
> alter decoding based on it. Each descriptive field's definition states what a reader does
> when the field contradicts the data it describes. `[R-ENC-16]`"

§6.2's layout table then prints, among others:

> `| 16 | 8 | u64 | generation | semantic | 1 ≤ generation ≤ 2⁶³ − 1 |`
> `| 48 | 8 | u64 | file_id | semantic | ≠ 0 |`
> `| 56 | 4 | bytes | reserved | structural | zero |`

None of the three is derivable from §4.7's words:

- `generation` and `file_id` do not determine how any byte is located or decoded, and they do
  not determine what any decoded value *means* — two files differing only in these fields
  decode identically. By the residual chain they are descriptive; but the descriptive gloss
  ("determines nothing a conforming reader does") is false of them, because `[R-LIF-03]`
  makes concrete reader behaviour turn on both: "different file_id or lower generation, treat
  as a different file".
- `reserved` is labelled structural although its value locates and decodes nothing. It is
  matched against a constant, and §4.5 says explicitly that "comparing a field against a
  constant for validation is not acting on it". §6.1's front-block table has the same shape
  ("8 | 8 | zero | structural (reserved)").

This would be inert if the document always supplied the class. It does not. §4.7's own note
says of §7.4's layer-record payload: "its table omits the offset and class columns, and each
field's class follows from the definitions above." Deriving them, the name fields resist all
three: a layer/dimension/channel name locates and decodes no byte (not structural), determines
no decoded value's meaning (not semantic), and does not "determine nothing a conforming reader
does" (a duplicate is a validity error a reader must detect at open, `[R-ENC-15]`, F4/L9) — and
if it were descriptive, `[R-ENC-16]`'s closing sentence would require §4.6 to state what a
reader does when the name "contradicts the data it describes", which §4.6 does not, there being
no such data.

I picked the reading that "determines nothing a conforming reader does" means *nothing about
how the reader locates, decodes, or interprets stored sample data* — under which names,
alignment `A`, slab `S` and `A_slab` are descriptive (and §16.1/§16.2 do supply their
contradiction rules, which is a point in the reading's favour), and `generation`/`file_id`
would also be descriptive, contradicting §6.2's table. The alternative reading — anything
gating acceptance is structural — makes `generation`, `file_id` and names all structural,
which contradicts the table in the other direction.

Byte-level: **no.** `[R-ENC-16]`'s operative consequence is "a reader MUST NOT alter decoding
based on [a descriptive field]", and no reader alters decoding on any of these fields under any
of the readings, so no byte sequence and no accept/reject verdict moves.

### diagrams-04 (CONTRADICTION) — the front matter says checklists never cite prose positions; Appendix H says the opposite and does the opposite

Front matter, "How to read this document":

> "Normative requirements carry stable identifiers like `[R-IDX-03]`; test vectors and
> conformance checklists cite identifiers, never prose positions."

Appendix H, "Conformance checklists":

> "§2.3 defines the classes; each entry's authority is the requirement or section cited, never
> this summary."

and its entries cite prose positions throughout, in many cases with no identifier at all:
"every requirement at every scope holds (§2.4)"; "every structure's checksum verifies where
§8.1's map states one (§8.1)"; "validates the trailer in §6.2's order"; "detects every
reader-assigned violation no later than its tier (§19.2)"; "never returns padding positions
(§11.3)"; "returns sample bit patterns unaltered (§3.2)"; "follows the commit protocol
including both barriers (§9.2)"; "honors any alignment or slab it declares (§16)"; "validates
the trailer and full directory, and every layer it modifies (§20.3)"; "re-emits every retained
record byte-identically (§20.4)"; "the live-state coverage partition and the slack total
(§9.7)"; "extent overlap (§7.2)"; "certifies only files with no violation at any scope (§2.4)".

Each of these has an identifier available (`[R-CNF-12]`, `[R-CNT-19]`, `[R-CNT-06]`,
`[R-RDR-02]`, `[R-GEO-04]`, `[R-MDL-02]`, `[R-LIF-02]`, `[R-SLB-01]`/`[R-SLB-03]`,
`[R-WRT-03]`, `[R-WRT-05]`, `[R-LIF-08]`, `[R-CNT-13]`, `[R-CNF-11]`), so this is not a case of
a rule that has no identifier to cite — except for the one §20.4 case, which is
diagrams-05. An alternative reading is that "conformance checklists" in the front matter means
only the manifest-side checklists of the corpus and not this appendix; I reject it because
Appendix H is literally titled "Conformance checklists" and the front matter's sentence sits in
the same breath as the statement about `[R-IDX-03]`-style identifiers that Appendix H is
supposed to exemplify.

Byte-level: **no.** Both texts are non-normative (the front-matter block is labelled
*(non-normative)*, Appendix H is "A summary ... never this summary" as authority).

### diagrams-05 (CONTRADICTION) — §20.4's preservation table states MUST-level obligations with no requirement identifier, and §21.6 cites a rule for it that does not state it

§2.2 states the convention as fact:

> "Normative requirements carry identifiers of the form `[R-<PREFIX>-<NN>]`."

§20.4's preservation table carries MUST-level updater obligations and no identifier. Its
introducing sentence ends "and carry these obligations:" with no `[R-...]`, the table's MU = 1
cell reads "Retain byte-identical. The updater MUST NOT modify the scope the record governs.",
and the next identifier in the section, `[R-WRT-08]`, attaches to a later and different
paragraph ("An updater MUST NOT re-encode a record whose type it does not implement..."). The
table is the sole statement of the preserve/drop rules: `[R-CNF-06]` reaches it only by prose
position ("MUST honor the preservation obligations of §20.4"), and §2.4's outcome table
likewise ("§20.4's table states the cases: its MU = 1 and MU = 0 / PE = 1 rows").

The consequence shows up in §21.6's table, which cites the wrong rules for the behaviour it
describes:

> "| A record type this specification has not assigned, from the experimental range
> (≥ 0x8000, §10.2), carries MU = 0 | Ignored, and **preserved or dropped per its PE bit**;
> ... | `[R-CNT-15]`, `[R-WRT-08]` |"

`[R-CNT-15]` governs the MU-bit reader outcome and says nothing about PE; `[R-WRT-08]` bars
re-encoding and modification and says nothing about dropping. The rule that licenses dropping a
PE = 0 record — and fences it with "An appender may drop it only in a commit that
*independently* changes the scope the record attaches to" — is the unlabelled table. §21.1
says "where a row and the rule it cites diverge, **the rule governs**", which here points a
reader at two rules that do not contain the behaviour the row states.

A second, milder instance of the same hygiene gap: §6.1's "Writers MUST emit exactly these 16
bytes." (immediately after the front-block table) also carries no identifier; there it is
recoverable, because `[R-CNT-04]`'s reader rule plus `[R-CNF-05]` make a wrong front block
nonconforming.

Byte-level: **no.** The obligations are stated in prose whether or not they are labelled, and
they bind an updater's conduct across generations rather than the bytes of any single file.

### diagrams-06 (OBSERVATION) — §21.9 claims every limit lives there; `[R-ERR-05]`'s hard-limit enumeration omits several

§21.9 opens:

> "Every limit affecting which files are valid, or which files a conforming reader accepts,
> lives here (`[R-CNF-10]`)."

(`[R-CNF-10]` itself says something weaker and different: "lives in this specification, never
only in an implementation.")

`[R-ERR-05]` then enumerates the hard limits: names at most 255 bytes; user-metadata keys at
most 255 bytes; "rank at most 255 and channel count at most 65,535"; codec 4's `0x7E000000`;
"every offset, length, extent, and count at most 2⁶³ − 1"; `A` a power of two in 512..2⁶²;
`A_slab` a power of two in 1..2⁶²; "a slab run length S with 1 ≤ S ≤ 2⁶³ − 1"; "a directory of
at least 4 bytes at an offset of at least 16"; "no conforming file shorter than 128 bytes".

The list includes floors of the same kind it omits — it states `S ≥ 1`, `A_slab ≥ 1`,
`dir_length ≥ 4`, `dir_offset ≥ 16` and `F ≥ 128` — so floors are plainly in scope. Missing:

- **rank d ≥ 1, channel count C ≥ 1, tile extent Tᵢ ≥ 1** (`[R-GEO-01]`, register row L32).
  The entry gives only the *ceilings* for rank and C, and Appendix B repeats the same
  half-limit: "| Rank d, channel count C | at most 255 and 65,535 — the widths of their fields |".
- **generation ≥ 1** (`[R-CNT-06]`, register row F11). The 2⁶³ − 1 ceiling is covered by the
  value-domain clause; the floor is not.
- **a user-metadata record's extent_length ≥ 5** (`[R-CNT-25]`, rows F22/L11) — the exact
  analogue of the "directory of at least 4 bytes" entry that *is* listed.
- **a user-metadata record's inline_length exactly 1** (`[R-MTA-03]`, rows F23/L12).

An implementer treating §21.9 as the inventory of limits, which its opening sentence invites,
would build a limits table missing four validity floors, all four of which have register rows.

Byte-level: **no.** Each omitted limit is stated normatively where its structure is defined and
is carried by a register row, so no implementation can reach a different verdict from the
omission.

### diagrams-07 (OBSERVATION) — `[R-ENC-06]` is assigned to readers by §19.3 but has no register row and no §21.7 accounting

§4.2 states a file-level requirement:

> "No field's width is ever a writer choice: every field's width is fixed by this
> specification, and a structure whose fields appear at any other width is invalid at its
> owning scope. `[R-ENC-06]`"

§19.3 puts it in the reader's layer-access validation set:

> "the fixed field widths and u64 value domain of §4 (`[R-ENC-06]`, `[R-ENC-03]`)"

I extracted the Governing-rule cell of all 121 register rows: `[R-ENC-06]` is the governing
rule of none of them, and appears in no row's secondary citation either. §21.1 makes that a
reportable state:

> "Its **completeness is normative** — a *detectable* file-conformance violation this
> specification names and the register omits is a defect in this document, detectability being
> the gate `[R-CNF-07]` already applies and §21.7 the account, by class, of what fails it"

So either `[R-ENC-06]` is detectable, in which case a row is owed, or it is undetectable, in
which case §21.7 owes an account. §21.7 gives two accounts — content incorrectness
(`[R-COD-10]`, `[R-COD-06]`'s undisclosed dictionary, wrong data) and a closed list of
witness-free obligations (`[R-LIF-01]`, `[R-LIF-03]`, `[R-GEO-06]`, `[R-SER-01]`,
`[R-CNT-13]`'s no-embedded-offsets) — and `[R-ENC-06]` is in neither. Every other rule I
checked that lacks a row is either a SHOULD, a reader/updater conduct rule, or has an explicit
"no register row" note attached to it (`[R-SLB-04]` at §16.2, the nesting prohibition at §7.4,
`[R-CNT-02]`'s second half at §5.2, `[R-LIF-04]`'s residue at §9.5). `[R-ENC-06]` alone is
silent.

My own analysis is that it is genuinely undetectable — a field emitted at the wrong width is
indistinguishable from correct fields carrying different values, and every instance surfaces as
some other row (a parse overrun L23/L14/F29, an out-of-range value, or a cross-check failure
L21/L22) — which means what is owed is a sentence in §21.7, not a row. But the document does
not say that, and §19.3 tells a reader to perform a check it cannot perform.

Byte-level: **no.** No reader can act on the check either way, so no accept/reject verdict
moves.

### diagrams-08 (OBSERVATION) — no worked byte example exists for a record header or a layer record, and Appendix A's annotated file contains neither

§4.7's presentation note promises:

> "Every non-obvious encoding is followed by a worked numeric example, and every sentinel or
> overloaded encoding additionally has a paired conformance vector."

Inventorying the worked examples (Phase 1 above), every encoding in the document has one
*except* the two most intricate: §7.2's 24-byte record header and §7.4's packed
variable-length layer-record inline payload. Neither appears anywhere in the document as
bytes. Appendix A, the only annotated file, is the 128-byte minimum — "It contains no layers"
— so its directory is four bytes of CRC and it exhibits no record at all. §12.3's twelve-byte
channel entry is the closest thing, and it covers one of §7.4's fifteen field groups; a
dimension entry (`name · extent u64 · tile extent u64`) is never shown.

This is the one place in my walk where I had to construct the encoding myself with no
cross-check available. The construction is determinate — §7.4's table gives the order and
`[R-CNT-18]` says "fields are packed in table order with no alignment or padding between
them", `d` and `C` precede the entries they size, and the trailing fixed fields precede the
sub-records — so I do not think two implementations would disagree. But the promise in §4.7 is
not kept for the structure where an error would be most expensive, and a second annotated file
carrying one layer would let a reader check the layer record, an index region, a sentinel entry
and a stored tile against real bytes, which nothing in the document currently permits.

Byte-level: **no.** The layout is determined by §7.4's table and `[R-CNT-18]`; the missing
example is a verification aid, not a fork.

---

## Things I checked hard and did **not** report

- Every worked example's arithmetic (Phase 2) — all correct.
- Appendix A byte for byte, including the CRC — correct.
- The 121/248 counts and every row-label citation (Phase 3) — correct.
- T26's "detected by T2's or T4's" — I suspected T5 was wrongly omitted, proved the last byte
  of a shuffled image is a fixed point of the permutation for every stride, and withdrew it.
- §21.2/§21.3/§21.4 section headers state a blanket reader outcome ("that tile's read reports
  failure") that is false for the verifier-detected rows (T2, T4, T5, T26, F7, F25–F28, F33,
  F36, L18, L25, L40–L42, L46–L49). §21.1 decides this explicitly — "For a row whose Detector
  is *verifier*, the outcome names the scope at which the damage is recorded, not an obligation
  on any reader" — so it is resolved text, not a defect.
- §21.6's "The file contains zero layers | A conforming file with an empty directory" is looser
  than its condition (a zero-layer file may carry a top-level user-metadata record and so a
  non-empty directory), but the row faithfully restates `[R-CNT-14]`'s own wording, so the row
  is not the divergence.
- §21.8's "at least one conformance vector whose expected **verdict** is that row's **outcome**"
  conflates §2.3's verdicts with §2.4's outcomes, but `[R-VEC-02]` separates them cleanly in
  the manifest and `[R-VEC-03]` restates the coverage obligation without the conflation.
- T24's instance cell "any codec" nominally includes codec 1, where the condition cannot arise
  (identity decode always consumes exactly `length`, and a length mismatch is T14). §21.1
  licenses a family-wide single instance, and the over-reach costs the corpus nothing.
- §17.2's note "§14.2's worked examples give 18 and 30 bytes" omits the 12-byte planar case
  from the same example; it is illustrative and claims no completeness.
- §6.1's and §7.2's layout tables omit columns §4.7's note lists (§6.1 has no Type, Field or
  Valid-values column; §7.2 has no Valid-values column, its constraints living inside the Field
  cells). The note is non-normative and both tables are unambiguous as written; I judged this
  below the reporting bar rather than padding the list with it.
