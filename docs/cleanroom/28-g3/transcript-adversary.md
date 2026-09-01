# Round 28 — Adversary transcript

## 0. Disclosure and hygiene

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,648 lines by `wc -l`; the brief says 4,649 — a trailing-newline convention
difference, not a discrepancy worth reporting). It was where the brief said it
would be. I listed no directories, opened no ADR, no PLAN.md, no
OPEN-QUESTIONS.md, no conformance corpus, no registry, no git history, and ran
no web tool.

I ran `grep`/`rg`/`awk` against that one file, and one Python script
(`scratchpad/crc.py`) that reads no files and computes CRC-32C over byte
strings I constructed in the script itself. I wrote two scratch files
(`crc.py`, `flat.txt` — the spec with newlines collapsed, produced by `tr` from
the spec I am permitted to read, so I could grep across line wraps) and this
transcript. I did not read the output directory.

**Context I did not ask for.** My runtime placed a project instruction file in
context before I began: a `CLAUDE.md` whose entire content is a pointer to
`AGENTS.md`. It carried no specification content and no findings, and I
disregarded it; I did not open `AGENTS.md`. A `gitStatus` block with recent
commit subject lines was also present. Those subject lines name the round's
recent history (a generation counter removed, a trailer reordered, a struck row
label, an ADR-0112 audit). **I did not use them to locate anything**: the brief
itself already told me a structural field had been removed from a fixed-size
structure with fields moving after it, that the structure's size was unchanged,
and that a register row was struck and its label retired — so the commit
subjects added nothing my brief had not already given me, and I confirmed each
of those facts against the document's own text before relying on it (trailer
layout table §6.2, `[R-CNT-24]`, §21.2's F11 Note). I disclose their presence
because the rule requires it.

---

## 1. How I worked

I read the document end to end first (five passes over contiguous ranges), then:

1. **Recomputed every checksum and every worked number the document states.**
2. **Mechanically re-derived the register's stated totals** — condition counts
   per subsection and the 275-instance figure — against the tables as written
   and against §21.1's own instance-enumeration rules.
3. **Swept the trailer's field offsets** across every passage that names one,
   because the brief said a field had been removed from a fixed-size structure
   and the fields after it had moved.
4. **Built concrete attack files** in the four families my charter names —
   boundary values, two structures claiming one byte, rules stated twice, and
   degenerate-but-legal files — and for each, tried to find the sentence that
   forecloses it.
5. **Ran the ten shapes** the brief lists over the twenty-five changed passages
   and then over the unchanged ones.

---

## 2. Arithmetic and checksums I computed myself

All computed with a from-scratch CRC-32C (reflected, poly 0x82F63B78, init
0xFFFFFFFF, final XOR 0xFFFFFFFF), validated first against §4.5's own check
vector.

| Quantity | Document says | I computed | Verdict |
|---|---|---|---|
| CRC-32C(`"123456789"`) (§4.5) | `0xE3069283` | `0xe3069283` | ✅ |
| CRC-32C(zero bytes) (§4.5) | `0x00000000` | `0x0` | ✅ |
| Appendix A trailer CRC over [0,60) | `0x402F157E`, stored `7E 15 2F 40` | `0x402f157e`, `7e 15 2f 40` | ✅ |
| §7.4 example: CRC of the 80-byte all-sentinel entry array | `0x80A34955`, stored `55 49 A3 80` | `0x80a34955`, `55 49 a3 80` | ✅ |
| §7.4 example: `crc_of_crc_array` over those 4 bytes | `0xC4EE982E` | `0xc4ee982e` | ✅ |
| §15.4 / Appendix B: CRC of a full 2¹⁶-sentinel segment | `0xEECB3BB2` | `0xeecb3bb2` | ✅ |

I reconstructed the Appendix A trailer field by field from §6.2's layout table
(magic 8 @0, version_major 2 @8, version_minor 2 @10, flags 4 @12, dir_offset 8
@16, dir_length 8 @24, committed_file_length 8 @32, file_id 8 @40, reserved 12
@48, CRC 4 @60 = 64 bytes) and got the stated CRC. That is a real cross-check of
the reordered trailer: had `file_id` still been at 48 or `reserved` still been
4 bytes at 56, the CRC would not have reproduced. **The byte-level worked
example and its annotation table agree with each other and with the structure's
own layout, byte for byte.**

Other numbers I derived and compared:

- **§7.4's layer-record example, offset by offset.** name 4 (0–3), layout 1 (4),
  linearization 2 (5–6), codec 2 (7–8), filter 2 (9–10), A 8 (11–18), S 8
  (19–26), A_slab 8 (27–34), rank 1 (35), C 2 (36–37), dimension entry 18
  (38–55), channel entry 12 (56–67), index_encoding 1 (68), entry_count 8
  (69–76), crc_of_crc_array 4 (77–80) = **81**, matching the stated 81 and the
  stated decomposition "4 + 34 … 18 … 12 … 13". The nine scalars from layout
  through C are 1+2+2+2+8+8+8+1+2 = **34** — nine of them, as stated. ✅
- **§7.4's index extent length**: 4 × 20 + ⌈4/2¹⁶⌉ × 4 = **84** ✅; the region is
  an 80-byte entry array plus one 4-byte segment CRC ✅.
- **The channel entry** `04 74 65 6D 70 0C 00 04 00 00 C0 7F` is byte-identical
  to §12.3's twelve bytes ✅.
- **§15.4's 1,000,000-entry example**: 16 segments (15 full + 16,960) ✅;
  64-byte CRC array ✅; region 20,000,064 ✅; k=999,999 → segment 15,
  segment-relative byte 20 × 16,959 = 339,180 ✅; CRC array
  [20,000,000, 20,000,064) ✅; segment 15 [19,660,800, 20,000,000) ✅ (339,200
  bytes ≈ "~339 KB" ✅); full segment 1,310,720 = 1.25 MiB ✅.
- **§15.1's planar example**: disk ordinal 2·32+10 = 74 ✅, entry at
  [1480, 1500) ✅, channel-3 block entries 96–127 = 32 ✅.
- **§11.4's example**: (300,700) → tile (1,2), s = 10, in-tile (44,188),
  in-tile ordinal 44·256+188 = 11,452 ✅; planar disk ordinal 74 ✅.
- **§14.2's examples**: (2,3), Q=3, size 18, ordinal 5 at [15,18) ✅; planar b
  12 bytes, ordinal 5 at 10–11 ✅; float32+bool Q=5, size 30, [25,30) ✅.
- **§14.3's example**: P=10 → `55 01`; fill true → `55 FD` ✅ (bits 2–7 set).
- **§14.5's example**: grid 2×2, edge tile covers 4–7 both axes → 1 real +
  15 padding, 32 bytes ✅.
- **§17.3's shuffle example**: I applied `filtered[i·n+j] = image[j·s+i]` with
  s=4, n=3 and got `00 00 00 00 00 00 80 00 40 3F 40 40` ✅, exactly as printed.
- **§20.3's example**: 32·20 + 4 = **644** ✅.
- **§21.9's Note**: 2³²/2¹⁶ × 4 = 262,144 = 256 KiB ✅; at 2³⁶ → 4 MiB ✅;
  65,536 × 200 B = 13,107,200 = 12.5 MiB ✅; 256 MiB / 16 MiB = 16× ✅.
- **§24**: 2³² × 20 ≈ 80 GiB — "tens of gigabytes" ✅.
- **§9.2's Note derivation**: dir_offset ≥ F, dir_length ≥ 4, sum ≤ F′ − 64 ⇒
  F′ ≥ F + 68; F′ ≡ 0 (mod 64) and F ≡ 0 (mod 64) ⇒ F′ ≥ F + 128 ✅.
- **§9.3's Note ceiling**: largest multiple of 64 that is ≤ 2⁶³ − 1 is
  2⁶³ − 64 ✅ (remainder 63).
- **`[R-CNT-24]`'s 48 redefinable bytes**: fixed = magic 8 + version_major 2 +
  version_minor 2 + CRC 4 = 16; 64 − 16 = **48** ✅, and the redefinable run is
  [12, 60), which contains F15's reserved [48, 60) — exactly as §2.3's Note
  claims when it says F15 does not reach.
- **`[R-CNT-24]`'s "zero slack"**: 8+2+2+4+8+8+8+8+12+4 = **64** ✅.
- **`[R-COD-10]`'s identity condition** (Appendix G item 5): the permutation
  `filtered[i·n+j] = image[j·s+i]` is the identity iff s = 1 or n = 1 — take
  i=0, j=1 to force s=1 when n>1. ✅ as stated.
- I also proved for myself that **the byte-shuffle always fixes offsets 0 and
  L−1**: i=s−1, j=n−1 gives filtered offset (s−1)n + n − 1 = L−1 sourced from
  image offset (n−1)s + s − 1 = L−1. This matters because it means a wrong
  filter stride can **never** disturb a packed plane's pad bits (which live in
  the final byte). T26 and §21.7 both name "T2's or T4's" as the check that
  detects a wrong stride and both omit T5 — and **they are right to**. I opened
  that as a suspicion and closed it by this computation.

### The register's stated totals

Row counts, taken mechanically (`grep -cE '^\| F[0-9]+ \|'` etc.):

| Subsection | Document says | Rows present |
|---|---|---|
| §21.2 file scope | 35 conditions | 35 (F1–F36, F11 struck) ✅ |
| §21.3 layer scope | 49 conditions | 49 (L1–L49) ✅ |
| §21.4 tile scope | 26 conditions | 26 (T1–T26) ✅ |
| §21.5 ignored records | 10 conditions | 10 (R1–R10) ✅ |
| §21.8 total | 120 conditions | 35+49+26+10 = **120** ✅ |

Instances, summed cell by cell by hand:

- §21.2: F1 2, F2 5, F3 2, F4 1, F5 2, F6 2, F7 4, F8 1, F9 1, F10 1 = 21;
  F12–F20: 1,1,1,1,1,2,1,1,1 = 10 (→31); F21–F30: 1,1,2,1,1,1,1,2,3,2 = 15
  (→46); F31–F36: 1,1,5,1,1,1 = 10 → **56**
- §21.3: L1–L10 = 8,9,1,2,1,1,2,2,2,1 = 29; L11–L20 = 1,2,1,3,4,2,2,3,1,1 = 20
  (→49); L21–L30 = 4,4,4,1,1,1,1,1,3,2 = 22 (→71); L31–L40 =
  3,3,4,4,1,2,1,1,3,1 = 23 (→94); L41–L49 = 3,1,3,3,3,2,2,1,4 = 22 → **116**
- §21.4: T1–T10 = 1,1,6,4,1,1,2,1,1,1 = 19; T11–T20 = 2,1,2,6,2,1,1,2,1,1 = 19
  (→38); T21–T26 = 3,6,1,1,3,3 = 17 → **55**
- §21.5: 4,2,2,16,8,4,6,2,2,2 = **48**

**56 + 116 + 55 + 48 = 275**, exactly §21.8's figure. I then re-audited a
sample of individual cells against §21.1's stated instance rules (layout axis;
magnitude direction only where either side can be the greater; no direction for
a checksum or constant comparison; no direction for a nonzero test) and found
them consistent: L21 = 2 layouts × 2 directions = 4; T3/T14/T22 = 3 shapes × 2
directions = 6; T21/L44 = 3 shapes × 1 direction ("larger than", "exceeds") = 3;
T4 = 4 layout/type combinations with no direction; L30 = 2 directions; L29/L39 =
3 alternatives each; L33/L34 = 4 (the document states two reserved sub-ranges in
each of §11.4 and §12.2, and the cells follow); L36 = 2 (channel layout has no
experimental range, §10.2, and the cell correctly omits one); R4 = 8
alternatives × 2 containers = 16.

Two rows I looked at hardest and did not report as defects: **F2** correctly
omits `file_id` (a `u64` identifier, not "an offset, length, extent, or count",
so `[R-ENC-03]`'s domain rule does not reach it), and **L2** correctly omits
`Q` and `Fᶜ` (designated as sums by §14.2 but bounded above by 65,535 × 8, so
no instance is constructible) and correctly folds `V = P·C` and the maximum
disk ordinal `(C−1)·N + (N−1)` into `P·Q` and `C·N`, which dominate them — I
verified both dominations arithmetically.

### The trailer sweep

`grep -n 'trailer offset\|F − 56\|offset 48\|offset 60\|\[0, 60)\|\[60, 64)'`
returns eight sites; every one is consistent with the layout table:
`version_major`/`version_minor` at F−56 (`[R-CNT-24]`), CRC at F−4 over
[F−64, F−4) (§2.3's Note and `[R-CNT-24]`), CRC field at trailer offset 60 over
[0,60) (§6.2 table, §8.1's map, F14, Appendix A), 12 reserved bytes at trailer
offset 48 (F15, Appendix A). **No stale offset survives anywhere.** Searching
for the removed quantity turns up seven sites, each of which now says the same
thing correctly and none of which names a counter field: §3.1 ("No field
numbers generations"), §9.3's Note ("no field records it"), §20.4's Rationale,
§20.5 ("no field counts commits"), §21.7 ("no field of a file records how many
commits"), §23.2 ("No field carries a count of the commits"), Appendix G item 4.
Appendix D's "no counter in the trailer numbering the commits" is the eighth.

I also re-derived **§2.3's "`[R-CNT-06]` states nine"**: magic, CRC,
committed_file_length = file size, committed_file_length multiple of 64,
dir_offset ≥ 16, dir_length ≥ 4, dir_offset + dir_length ≤ F − 64, file_id ≠ 0,
reserved zero — nine, excluding the version gate (`[R-CNT-07]`) and the flag
gates (`[R-CNT-08]`), which the sentence's own "the other seven" arithmetic
(2 + 7 = 9) confirms. The register agrees: exactly nine rows name `[R-CNT-06]`
first — F8, F9, F10, F12, F13, F14, F15, F16, F17. And §21.2's reaching set —
F8, F14, F6, both of F1's instances — falls out of that: only magic and CRC
among the nine assert `[R-CNT-24]` invariants, and F6/F1's front-block instance
ride on `[R-CNT-24]`'s "the front signature block (§6.1) is constant". **The
closed count survived the field removal.**

### The `[R-CNF-01]` blockquote convention

The brief told me to check the label rather than the marker. I extracted every
blockquote in the file with `awk` and filtered out those whose first line
carries `**Note`, `**Example` or `**Rationale`. Exactly two survive: the
"How to read this document" block at line 12, which labels itself
*(non-normative)*, and **§15.1's index-region layout block at line 2124** —

> `[ entry array: entry_count × 20 bytes ] [ segment CRC array: ⌈entry_count / 2¹⁶⌉ × 4 bytes ]`

which is normative and which I checked against `[R-CNT-17]`'s
`entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4`. They agree. I also swept for
BCP 14 keywords inside blockquotes (five hits, lines 112, 1296, 2205, 3015,
3215) and read each; none of them contradicts the normative text it glosses.

---

## 3. Attacks I built, and what forecloses each

This is the constructive half of my charter. Each entry is a concrete file, the
two verdicts I hoped to get, and the sentence that closed it.

### 3.1 Degenerate-but-legal files

**A1. The 128-byte file.** Front block [0,16); directory [16,20) holding
`00 00 00 00`; 44 bytes of pad; trailer [64,128). I reconstructed the whole
thing from §6.2's table and reproduced Appendix A's trailer CRC. Live-state
claimants: front block 16 + directory 4 + trailer 64 = 84; slack = 44. Both
verifiers must report 44 and certify. **Foreclosed** and correct.

**A2. Moving the directory in a 128-byte file.** dir_offset = 60, dir_length = 4
puts the directory at [60,64) — still ≥ 16, still ≤ F − 64 = 64, still inside
§9.7's [16, F−64) claimant window. Zero pre-trailer pad, 44 bytes of slack
before the directory. Conforming; the slack total moves but is deterministic.
No fork.

**A3. dir_length = 48 at dir_offset = 16.** Directory fills [16,64) exactly:
zero pad, zero slack. 44 bytes of record sequence must parse with no residue,
which forces exactly one record with `inline_length` = 20 (24 + 20 = 44). A
layer record cannot fit (its minimum inline payload is well over 20 bytes), so
this must be an experimental-type record. Conforming. No fork.

**A4. The minimal file with a layer.** rank 1, C = 1, one dimension with
E = 0, T = 1, one `int8` channel with a 1-byte fill, `index_encoding` = 1,
`entry_count` = 0, extent slot (0,0), `crc_of_crc_array` = 0. Inline payload
2 + 34 + 18 + 6 + 13 = 73; record 97; directory 101; dir end 117; F = 192.
`[R-GEO-02]` blesses the zero extent, `[R-CNT-17]`'s "(and 0 when entry_count is
0)" blesses the empty slot, `[R-CNT-23]` blesses `crc_of_crc_array` = 0.
Conforming. No fork.

**A5. Two layers, both with extent slot (0,0).** Neither claims a byte, so no
overlap. Legal.

**A6. The all-optional-absent file.** No layers, no records, no metadata. That
is A1.

### 3.2 Boundary values

**B1. `offset + length = F − 64` exactly on a stored tile.** §15.3 and T9 both
say "> F − 64", so equality passes the entry check. But such an extent lies
between the live directory's end and the trailer unless the directory sits
above it, and `[R-CNT-05]` forbids any structure there; and if the directory
ends at F − 64 too, the two overlap. So **every** such file is nonconforming,
via F7 or via F33/L18 — not via T9. Two rules jointly close a boundary neither
closes alone, and they close it consistently: reader sees nothing at tile scope,
verifier rejects the file. That is the designed reader/verifier seam, not a
fork. **Foreclosed.**

**B2. Sentinel-shaped entry with a nonzero crc.** `FF ×16` + crc 5. Rows T6, and
arguably T9/T11/T12 depending on whether "non-sentinel" means "not the sentinel
*entry*" or "not carrying sentinel *values*". I chased this because it looked
like a scope ambiguity, and closed it: T11 has the qualifier "the value being
distinct from the all-ones sentinel" and T12 has "although each field alone is
in domain", both of which exclude the entry; and **every** §15.3 row that could
match gives the same outcome (*structural*: reject-tile). No observable
difference under either reading. **Foreclosed.**

**B3. `entry_count` = 2¹⁶ and 2¹⁶+1.** At 2¹⁶ there is exactly one full segment
and `[R-IDX-05]`'s constant is licensed; at 2¹⁶+1 the second segment covers one
entry and its CRC "MUST be computed". I verified the constant.
**Foreclosed.**

**B4. `2⁶³` in a `u64` field** → F2/L1/T11; **`2⁶⁴−1` in both halves of an entry
with crc 0** → the sentinel, expressly exempted from `[R-ENC-03]`/`[R-ENC-04]`
by `[R-IDX-02]`; **`2⁶⁴−1` in a layer record's extent slot** → no sentinel
exists for extent slots, so L1. **Foreclosed.**

**B5. F = 2⁶³ − 64.** The largest legal committed file length. §9.3's Note
derives it and I confirmed the arithmetic. **Foreclosed.**

**B6. A 64-byte file whose bytes are a valid trailer declaring version_major 2.**
Magic, CRC and the version gate all pass; `[R-CNF-13]` says the reaching
conditions apply whatever the declared major, and F6 reaches. Bytes [0,16) are
the trailer's own first 16, which are not the front-block constant, and any
reader that fetched the whole 64-byte file holds them resident, so
`[R-CNT-04]`'s residency exemption does not save it. Reject-file, nonconforming,
"whatever major the file declares". **Foreclosed** — and a nice demonstration
that `[R-CNF-13]`'s machinery bites.

**B7. Zero-extent layer with codec 4 and a colossal tile shape.** rank 1,
E = 0, T = 2⁶², `codec` = 4. Decoded size 2⁶² ≫ `0x7E000000`, but §17.2's Note
is explicit that the cap "is quantified over the layer's *addressed* tiles, so a
layer that addresses none … satisfies it whatever its tile shape declares", and
§21.9 says the same for the tile-size guarantee. The file is conforming and a
conforming reader **must** accept it. **Foreclosed** — expressly, and this
reads like a defect a previous round already found and repaired.

**B8. The same layer with two `int64` channels interleaved and T = 2⁶³−1.**
P·Q = 16·(2⁶³−1) overflows. §17.2's Note anticipates exactly this:
"`[R-ENC-04]`'s overflow rule carries no such quantifier … so P·Q and P·Bᶜ are
checked in an empty layer even though this cap is not." L2. **Foreclosed.**

**B9. A zero-extent layer whose *partial* grid product overflows.** This one is
**not** foreclosed by an express sentence. See finding `adversary-01`.

### 3.3 Two structures claiming the same bytes

I enumerated the overlap trichotomy and checked it is exhaustive and
unambiguous. `[R-CNT-13]`: intra-layer overlap (including a stored extent
against its own layer's index region or sub-record extents) → reject-layer
(L18); overlap across layers or touching another scope's structures →
reject-file; overlap between two structures neither of which belongs to a layer
→ reject-file (both F33). Concrete cases I ran: two layer records pointing at
one index region (F33); layer A's tile over layer A's sub-record extent (L18);
layer A's tile over layer B's tile (F33); a stored tile inside the directory
region (F33); two top-level unknown-record extents overlapping (F33); a
three-way overlap that fires L18 and F33 at once (nonconforming either way).
The trichotomy has no gap and no double-assignment. **Foreclosed.**

I also checked F33's own tie-breaking sentence — that a slot of (0, N) with N
nonzero "reaches the block through its zero offset and is theirs rather than
F31's or L16's" — against F30/L15 and F31/L16, and it is right: offset 0 is not
in 1–15.

### 3.4 Rules stated in two places

**D1. `[R-CNT-25]`'s "containing scope" vs `[R-CNT-13]`'s "scope the record
governs".** For a top-level user-metadata record both resolve to file; for a
sub-record both resolve to layer. No divergence.

**D2. §7.3's Scope column ("file (container for layer scope)") vs
`[R-CNT-12]`/`[R-CNT-22]`'s "the record's governing scope".** Read alone this is
a genuine tension for a layer record. `[R-CNT-13]` resolves it expressly — "the
layer for a layer record and for sub-records, the file for other top-level
records" — and the register follows it exactly: F25/F26/F28 all say
"non-layer top-level record", and L46/L47/L49 carry the layer-record cases at
layer scope. **Foreclosed**, and carefully.

**D3. `[R-CNF-03]`'s acceptance carve-out vs `[R-CNT-18]`.** `[R-CNF-03]`
removes from the acceptance duty any conforming file "carrying no record of a
type it does not implement with MUST_UNDERSTAND = 1", without qualifying
*top-level*, while §21.6 says only the top-level case is a file a reader
refuses and `[R-CNT-18]` says a reader "MUST NOT reject the file" for the
sub-record case. I opened this as a candidate contradiction and closed it: the
broad carve-out is *necessary*, because otherwise `[R-CNF-03]` would oblige a
reader to serve a layer `[R-CNT-18]` forbids it to serve, and the MUST NOT
independently bars rejecting the file. Coherent. **Foreclosed.**

**D4. F5's cell ("front block, directory, pre-trailer pad and trailer cannot
all fit") vs `[R-CNT-27]`'s derivation, which does not use the pad.** The pad is
a consequence of the 64-alignment, not a premise. §21.1's "where a row and the
rule it cites diverge, the rule governs" settles it and §2.3's Note states the
derivation correctly. Restatement colour, not a defect; I am not reporting it.

### 3.5 Reserved / unknown / experimental values in every position

I walked §10.2's eight spaces against §20.5's claim that this text registers
"one row for each of the other seven spaces §10.2 tabulates (L31, L33, L34,
L36, L43, L45, R1)" and confirmed each row does register the reserved range for
its space, with record type separately at F36/L25 — seven plus one, matching.
I also confirmed §20.5's "the two of §10.1's four vehicles §21.6 makes
conforming" against §21.6's table: ignore-lane bits and unrecognized `tarn.`
keys. Correct.

Concrete files built and closed:
- Top-level experimental record type, MU = 0, PE = 0, `inline_length` = 0,
  extent (0,0) → conforming, ignored, droppable under §20.4's conditions.
- Top-level experimental record type, MU = 1 → conforming file, reader must
  reject-file, verifier reports *cannot establish* unless it implements the
  type. Two verifiers can differ (*conforming* vs *cannot establish*) — but
  §2.3 licenses exactly that, and *cannot establish* "is not a finding that the
  file is nonconforming". **Not a fork about the bytes.**
- The same type as a layer sub-record → reject-layer, file conforming,
  `[R-CNT-18]` forbids refusing the file.
- Reserved-range record type with MU = 0 → conforming behaviour for readers,
  but a violation: F36 (verifier). With MU = 1 → F35 as well, and §21.1 names
  F35 as a strict specialization of F36. I checked that specialization claim and
  the other four (F1's front-block instance of F6; F1's trailer-magic instance
  of F8; F21 of F22; L10 of L11) and all five hold: a (0,0) slot necessarily has
  `extent_length` 0 < 5, a byte-reversed constant is necessarily not the
  constant, and a reserved type with MU = 1 is necessarily a reserved type.
- User-metadata record at an experimental encoding (0x80), extent 5 bytes with
  a correct terminal CRC → conforming; the verifier certifies and must name the
  record. With a *wrong* terminal CRC → R2, nonconforming: `[R-MTA-10]` is
  explicit that the extent's terminal CRC still decides.
- Encoding 0 or a reserved encoding → R1, violation, ignore-record. §21.5's
  preamble states this against `[R-MTA-10]` expressly.

### 3.6 The reader/verifier seam

I hunted specifically for a condition one actor must detect and the other need
not, with a file sitting exactly on it. Every one I found is explicitly
two-sided:

- F6/F1's front-block instance: a remote reader that never fetches [0,16) MAY
  omit the check, so it serves a file a local reader rejects. Both readers
  conform; the file is nonconforming; **the verifier holds no such exemption**
  (F6's own cell says so, §2.3 says so, Appendix H repeats it). Not a verifier
  fork.
- F7, F25–F28, F33, L18, L40–L42, L46–L49, T2, T4, T5, T26: verifier-only. A
  reader that serves such a file is conforming. `[R-CNF-12]` licenses rejection
  and §21.1 explains the outcome column for verifier rows. Not a fork.
- `[R-MTA-09]`'s decode bound and `[R-ERR-04]`'s resource decline: two readers
  can serve or refuse the same conforming file with a 20 MiB metadata document,
  and two verifiers can report *conforming* and *cannot establish*. Explicitly
  designed, and §18.2's Note even fixes the *scope* of the `[R-ERR-04]` decline
  (whole file, "a document having no declared size and so no narrower scope").
  Not a fork.

### 3.7 Feature interactions

- **Sparse tile under a filter chain**: a sentinel entry has no payload, so no
  filter runs. `[R-TYP-09]` forbids returning fill for anything but a verified
  sentinel.
- **Empty layer under a limit**: covered at B7/B8 and by §21.9's per-instance
  paragraph.
- **Compaction over a record the compactor cannot read**: MU = 1 unimplemented
  → MUST refuse (§20.4's table and `[R-WRT-06]`, both). MU = 0 unimplemented →
  relocate the extent unread; §8.1 covers it by no checksum and §22.3 says so.
- **Compaction over a structurally malformed index entry**: §20.5 walks this
  through — the entry has no stored extent to re-point at, so regeneration
  cannot proceed, the violation is thereafter detected, and refusal follows.
  Carefully done.
- **Slab run continuity across sentinels and structurally-bad entries**: both
  transparent; an entry failing only its stored bytes' crc is not. §16.2 and
  §15.3 agree word for word, and L41's cell restates it. I checked the S = 1 and
  A_slab = 1 degenerate cases (vacuous, legal) and the S = 2⁶³−1 case (one run
  per block, legal).
- **Planar bool plane under filter 2**: `[R-COD-10]` makes it the identity at
  s = 1, and §14.4's "at P = 1 … the images coincide exactly when that fill is
  false" checks out both for a real and for a padding position.

---

## 4. Findings

Six. **None of them is a byte-level fork.** I could not construct a file two
conforming verifiers could defensibly judge differently; every candidate above
is closed by a sentence I have quoted. What follows is what I found instead:
places where the document decides the question but decides it expensively, or
where a restatement, an inventory or a universal claim does not hold up. I have
ranked them by how likely a real implementation is to land on the wrong side.

---

### adversary-01 — OBSERVATION

**A grid product with a zero factor: the normative text bounds the product but
never the partial product, and only a Rationale says the partial one may
overflow**

*Location:* §4.2 `[R-ENC-04]`; §11.2 `[R-GEO-03]`; §11.1's Rationale; §22.2
`[R-SEC-02]`.

*Quotation* (`[R-ENC-04]`, §4.2):

> A reader — including any updater or verifier, which are readers of the files
> they process — MUST treat any quantity this specification **designates** a
> declaration-derived sum or product of integers obtained from a file (offsets
> plus lengths, grid counts, tile counts, sample-position counts, ordinals)
> whose mathematical value would exceed 2⁶³ − 1 as a validity error at the
> owning scope, and MUST NOT act on a wrapped or truncated value.

*The file.* A layer, interleaved, C = 1, one `uint8` channel, rank 3, in
declared order:

| dim | name | Eᵢ | Tᵢ | Gᵢ |
|---|---|---|---|---|
| 0 | `a` | 2⁶² | 1 | 2⁶² |
| 1 | `b` | 3 | 1 | 3 |
| 2 | `c` | 0 | 1 | 0 |

`entry_count` = 0, extent slot (0,0), `crc_of_crc_array` = 0, `codec` = 1,
`filter` = 1, `linearization` = 1, A = S = A_slab = 0. Inline payload
2 + 34 + 3×18 + 6 + 13 = 109 bytes; record 133; directory 137 at offset 16;
F = 256.

Every field is in domain (2⁶² ≤ 2⁶³ − 1). Every **designated** quantity is
tiny: N = ∏Gᵢ = **0**, P = ∏Tᵢ = 1, N·P = 0, C·N = 0, P·Q = 1, and
`entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4` = 0. §11.2's cross-check holds
(`entry_count` = addressed-tile count = 0). **The file is conforming.**

But **G₀ · G₁ = 3 · 2⁶² = 13,835,058,055,282,163,712 > 2⁶³ − 1**. A verifier
that forms ∏Gᵢ left to right in checked 64-bit arithmetic — the natural
implementation, and the one `[R-SEC-02]`'s "Every declaration-derived sum and
product `[R-ENC-04]` designates is overflow-checked before use" invites — trips
on the partial product before it ever reaches the zero, and reports L2 /
reject-layer / *nonconforming*.

*The two readings.*

- **(i) The mathematical value governs.** N's value is 0. A partial product is
  not a designated quantity: "an expression this specification writes only
  inside a comparison, and names nowhere, is not a designated quantity and no
  reader is obliged to form it." §11.2 designates N, P, N·P and C·N and nothing
  smaller. Conforming.
- **(ii) The computation governs.** The reader must form ∏Gᵢ, and the way it is
  written in §11.2 is a product over the declared dimensions; a step of that
  product exceeds the domain, and `[R-ENC-04]` bars acting on a wrapped or
  truncated value. Reject-layer.

*Which I picked, and why.* **(i).** "Whose **mathematical value** would exceed"
is decisive about the quantity, and the non-designation clause is decisive about
the partial product. So the document does decide this, and a verifier taking
(ii) is wrong.

*Why it is still worth reporting.* The only place the document discusses this
case is **non-normative**. §11.1's Rationale says:

> Growth that leaves **entry_count** unchanged touches the directory alone — a
> growth raising one grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) while another stays 0 among
> them, **the product holding at 0**.

That is exactly the state my file is in, and it is a Rationale — exempt under
`[R-CNF-01]`. Nothing normative says a partial product may exceed the bound
while the designated product does not; §11.2's own Note anticipates the
*additive* overflow idiom (`(Eᵢ + Tᵢ − 1)/Tᵢ`) and warns against it, but says
nothing about the multiplicative one, which invites the reading that the
multiplicative case was thought about and is safe. And §20.3 step 4 explicitly
licenses growth "provided the grown geometry stays within every bound the
layer's own declarations impose, … `[R-ENC-04]`'s 2⁶³ − 1 ceiling on every
quantity it designates" — so a schema-first workflow can grow a layer's extents
into this state one commit at a time and each commit is legal.

*What an implementer does wrong without it.* Rejects a conforming file, at layer
scope, on a file that `[R-CNF-03]` obliges it to accept (nothing here exceeds a
§21.9 guarantee). Zero-extent layers are the schema-first workflow §11.1 exists
to serve, so this is not an exotic corner.

*Byte-level:* **no.** "Mathematical value" plus the non-designation clause
decides it, so a competent implementation reading the text lands on (i); the
emittable set does not move and no verdict is genuinely open. Grading it
byte-level would be exactly the over-claim the brief warns against.

---

### adversary-02 — OBSERVATION

**§21.7's inventory of unwitnessed obligations names the compactor's
carry-forward duty and omits the appender's, and omits §20.4's preservation
duties entirely**

*Location:* §21.7 `[R-ERR-01]`; §6.3 `[R-CNT-08]`; §20.4 `[R-WRT-05]` and its
table; §21.1.

*Quotation* (§21.7):

> §20.5's three obligations on a compacted file's trailer (`[R-WRT-06]`) — its
> fresh `file_id` draw, the unknown ignore-lane bits it MUST carry forward, and
> the floor its version_minor SHOULD take — are unwitnessed for a reason all
> three share: the output carries no record that it is a compaction output at
> all, so no check can know that any of the three was owed.

*The parallel the paragraph omits* (`[R-CNT-08]`, §6.3):

> An updater MUST copy forward unknown ignore-lane bits of the file it modifies
> and MUST NOT clear them

*The permitted readings.* §21.7 opens its second paragraph with "A second set of
obligations is omitted from the register because a single file exhibits no
witness of their violation" and then enumerates. §21.1 calls §21.7 "the account,
by class, of what fails" the detectability gate. Either that enumeration is
meant to be complete for the classes it names — in which case it is short — or
"by class" licenses naming exemplars, in which case it is fine but the reader
cannot tell which obligations are covered.

*What is missing, concretely.*

1. **`[R-CNT-08]`'s appender/updater carry-forward.** An appender that clears an
   unknown ignore-lane bit emits a *conforming* file. The input's flags survive
   only in the superseded trailer, which is slack — content unconstrained
   (`[R-CNT-21]`), a reader "MUST NOT interpret it", and §9.7's walk does not
   enumerate it. So the violation is unwitnessed for exactly the reason
   §21.7 gives for the compactor's identical duty. §21.7 names the compactor's
   and not this one.
2. **`[R-WRT-05]` and §20.4's table.** "an updater MUST re-emit byte-identically
   … every record it retains and does not logically modify" and "An appender
   MUST NOT drop it except in a commit that *independently* changes the scope
   the record attaches to". A commit that re-encodes a retained record, or drops
   a PE = 0 record in a commit whose only effect is the drop, produces a
   conforming file. §20.4's own **Rationale** — non-normative — says why no
   check can see it ("nothing in either says how many commits separate them.
   Adjacency is a fact about a file's history, which §9.7 does not
   reconstruct"). §21.7, which is normative and is where that account belongs,
   does not mention it.

Note the asymmetry is not merely stylistic: §21.7 *does* reach for the
neighbouring cases. It names `[R-LIF-01]`, `[R-LIF-02]`, `[R-GEO-06]`,
`[R-SER-01]`, `[R-CNT-13]`'s embedded-offset bar, `[R-CNT-18]`'s nesting bar,
§20.3 step 4's declaration bar, `[R-WRT-06]`'s three, and `[R-ENC-06]` — a list
carefully assembled from every part of the document except §20.4 and §6.3's
updater clause.

*What an implementer does wrong without it.* Reads §21.7 as the inventory it
presents itself as, concludes that §20.4's preservation obligations must
therefore be witnessed somewhere, and goes looking for a register row that does
not exist — or, worse, builds a verifier that tries to enforce byte-identical
re-emission from a single file, which is not decidable from one.

*Byte-level:* **no.** It changes no requirement and no emittable byte; it is a
completeness gap in a non-register subsection.

---

### adversary-03 — OBSERVATION

**§20.5 keys index-region regeneration to relocation of the *region*, when what
forces it is relocation of the *tiles* the entries address**

*Location:* §20.5 `[R-WRT-07]`.

*Quotation:*

> A compactor MUST preserve content, and preserves no placement — placement is
> not among the things it carries forward, and it is free to place structures
> anywhere §5.2 admits and every declared layout invariant permits
> (`[R-SLB-01]`, `[R-SLB-03]`): every stored tile's bytes verbatim — each index
> entry's crc is unchanged — and every retained record per §20.4, except that
> relocation re-points extent slots, **regenerates each relocated tile-index
> region** (entry offsets new; entry lengths, entry crcs, and sentinel entries
> unchanged; segment CRCs recomputed over the entries as re-emitted), and
> updates the layer-record fields covering a regenerated region
> (`crc_of_crc_array`).

*The file.* An input with one layer whose stored tiles are scattered with slack
between them and whose tile-index region sits at offset X. The compactor packs
the tiles — every tile moves — and, exercising the freedom the same sentence
grants it ("free to place structures anywhere §5.2 admits"), happens to place
the index region back at **X**. The region is not relocated. Its entries'
targets all are.

*The permitted readings.*

- **(i) Literal.** The exception to §20.4's byte-identical preservation is
  triggered by "each **relocated** tile-index region". This region is not
  relocated, so the exception does not reach it and §20.4's byte-identical rule
  stands: the compactor re-emits the region unchanged, with entry offsets
  pointing where the tiles used to be.
- **(ii) Purposive.** What the exception exists for is that "its entries carry
  the offsets that moved" (§20.5's own example says exactly this). Regeneration
  is owed whenever any entry's target moved, whatever happens to the region's
  own address.

*Which I picked, and why.* **(ii).** Reading (i) produces an output whose
entries address bytes that in the output hold something else or nothing —
violating `[R-WRT-07]`'s own closing sentence, "The output's reference arrays
MUST equal the live generation's bit for bit (`[R-MDL-02]`)", and §20.5's
"Given a conforming input the output is a conforming file", and almost
certainly F33 or T9 on the output. So (i) is barred by the surrounding text
even though the trigger clause, read alone, states it.

*What an implementer does wrong without it.* A compactor written to the literal
trigger, on a layout where a region happens to land where it started, emits a
file with stale entry offsets.

*Byte-level:* **no**, and this is the case the brief's fourth discriminator was
written for. The output of reading (i) is nonconforming, so `[R-CNF-05]` bars a
conforming writer from emitting it under *both* readings and the emittable set
does not move. The defect is that the trigger clause names the wrong condition,
not that the bytes are open.

---

### adversary-04 — OBSERVATION

**L23's detection point disagrees with §19.1 step 4 and §19.2 for the one
instance §19.1 places at the open**

*Location:* §21.3 row L23; §19.1 step 4 `[R-RDR-01]`; §19.2 `[R-RDR-02]`.

*Quotation* (§19.1 step 4):

> The layer-name namespace is built from the name fields a reader can obtain
> under §7.4's framing: a layer record whose name field does not lie entirely
> within that record's inline_length yields no name field to compare, so it
> contributes no name to the namespace and is instead a validity error at layer
> scope (`[R-CNT-18]`).

*And* (§21.3, L23, Detected column):

> | L23 | A declared region of the layer record's inline payload does not lie
> entirely within inline_length (overrun or truncation) | leading fixed fields
> (name … C); d dimension entries; C channel entries; trailing fixed fields
> (index_encoding, entry_count, crc_of_crc_array) | reader | **layer access** |
> `[R-CNT-18]` |

The condition "the name field does not lie entirely within `inline_length`" is
L23's *leading fixed fields* instance. §19.1 step 4 obliges a reader to decide
it **at the open**, because the layer-name namespace cannot be built without it,
and §19.2's first bullet confirms: "at open: … the layer-name namespace (§19.1's
steps)". L23's Detected cell says layer access.

*The permitted readings.* Either the row governs (detection due at first access
to the layer) or §19.1/§19.2 govern (due at open, for the name portion). §21.1
resolves it — "where a row and the rule it cites diverge, **the rule governs**"
— and §19's preamble points the same way. So the row is what is wrong; the
Instances column cannot express a tier that varies across instances of one row.

*What an implementer does wrong without it.* Little, which is why I grade it
low: under both readings the same layer is rejected, the same other layers are
served, and the namespace is built the same way. What is lost is a reader that
defers the check and therefore builds a *different* namespace at open than the
one §19.1 specifies — it cannot, because it needs the answer to build the
namespace at all, which is the circularity that makes the row's cell wrong
rather than merely early.

*Byte-level:* **no.** No returned byte and no verdict differs.

---

### adversary-05 — OBSERVATION

**§2.1's Note states a universal about SHOULDs that the document does not meet**

*Location:* §2.1's Note; §18.2 `[R-MTA-09]`; §16.2 `[R-SLB-03]`.

*Quotation* (§2.1's Note):

> Requirements in this document follow a fixed phrasing discipline: every
> requirement names the actor it binds (writer, reader, updater, verifier, or
> file); every writer-side prohibition is paired with an explicit reader-side
> clause stating what a reader does with a violating file; **every SHOULD states
> the consequence of deviation**; and requirements constrain bytes and
> observable behavior, never implementation technique.

I extracted every line containing `SHOULD` (44 hits) and read each with four
lines of context. The clearest counterexample is `[R-MTA-09]`, §18.2:

> the verifier SHOULD report the bound it applied and the stored length of the
> extent it declined.

No consequence of deviation is stated there or anywhere else for that
obligation. A second is `[R-SLB-03]`, §16.2:

> between runs, placement freedom (`[R-SLB-05]`) governs, and the bytes left
> between them are slack (§5.2), which writers SHOULD zero.

— which restates `[R-CNT-03]`'s SHOULD without its consequence clause, as does
`[R-SLB-01]` ("which writers SHOULD zero and no conformance requirement
constrains"). `[R-PRV-03]`'s two SHOULDs ("SHOULD treat names and metadata as
published content, and SHOULD compact before publication") likewise state none
locally, though the section around them supplies the reasoning.

*The permitted readings.* Either the Note is a claim about every SHOULD in the
document (false), or it is a claim about the *requirement-defining* SHOULDs and
tolerates cross-referenced or contextually-obvious consequences (true, but the
Note does not say so).

*Which I picked.* The second, because it is the only one under which the
sentence is true — but the sentence does not carry the qualifier.

*What an implementer does wrong without it.* Nothing about bytes. What is lost
is a drafting-discipline guarantee an implementer might rely on when deciding
whether a bare SHOULD they cannot find a consequence for is a SHOULD they have
misread.

*Byte-level:* **no.** The Note is labelled *Note* and is therefore non-normative
under `[R-CNF-01]`; and it makes a claim about the document, not about bytes.
This is the weakest of my six and I report it because it is a closed universal
that a five-minute census falsifies, which is precisely the shape the brief
asked me to test.

---

### adversary-06 — OBSERVATION

**Appendix G item 5 asserts a universal about the filter that a legal tile
falsifies**

*Location:* Appendix G, item 5.

*Quotation:*

> The filter is the identity exactly where its permutation is — where the stride
> is 1, as for a packed boolean plane, and equally where the decoded image is a
> single group, n = L/s being 1 (`[R-COD-10]`); **elsewhere it changes the
> stored bytes of every tile it touches.**

*The counterexample.* Take an interleaved layer, C = 2, channels `x` and `y`
both `uint8`, so Q = 2; tile extents giving P = 8, decoded size L = 16; s = Q =
2, n = 8 — neither 1, so the permutation is not the identity. Now take a stored
tile all of whose 16 decoded bytes are `0x00` — e.g. every sample (0, 0) — and
whose channel fills are the quiet NaN pattern's low byte, or any nonzero byte,
so that item 6's "sentinel for every all-fill tile" does not apply and the tile
must be stored. Every byte permutation of a constant image is that image. The
filtered bytes equal the unfiltered bytes; filter 1 and filter 2 produce
byte-identical stored tiles for this tile. More generally any image fixed by the
permutation — and offsets 0 and L−1 are fixed for *every* stride, which I proved
above — falsifies "every tile it touches".

*The permitted readings.* Either "changes the stored bytes of every tile" is
literal (false), or it means "is capable of changing the stored bytes of a tile"
(true, and what item 5 actually needs: "no content implies it, so two writers
agreeing on everything else still disagree on bytes without it pinned").

*Which I picked.* The second. The item's operative requirement — pin the filter
value — is unaffected either way.

*What an implementer does wrong without it.* Nothing directly; the risk is an
adopter of the reproducible-writer profile concluding that a filter mismatch is
always detectable by comparing tile bytes, which it is not.

*Byte-level:* **no.** Appendix G identifies itself as non-normative and the
sentence is a rationale for an item whose requirement is unchanged. It does not
disagree with the normative text it glosses; it overstates a consequence of it.

---

## 5. What I looked for and did not find

Stated for the record, because a reporter that finds no fork should be able to
say what it did that would have found one.

- **I could not find a stale offset, width, count or checksum anywhere.** Every
  number the document states that I could recompute, I recomputed, and all
  fifteen matched. That includes the four CRC-32C constants, the reordered
  trailer's own CRC over its reordered fields, the 81-byte layer-record example
  laid out field by field, all four register condition counts, and the
  275-instance total summed cell by cell. If the trailer change had left
  anything behind, this is where it would have shown.
- **I could not construct a file two conforming verifiers could defensibly
  judge differently.** Every candidate I built (§3) is closed by a sentence I
  quoted. The near misses — an experimental MU = 1 record, a metadata document
  above a verifier's bound, an unimplemented format major — all produce
  *conforming* against *cannot establish*, which §2.3 defines precisely so that
  the divergence is not a finding about the bytes.
- **The overlap trichotomy, the entry-classification table, the reach analysis
  of `[R-CNF-13]`, and the instance-enumeration rules of §21.1 all survived
  direct attack.** In each case I built the case that should have fallen through
  the gap and found the gap closed, usually by a sentence written for exactly
  that case.
- **The quantifier shapes the brief flagged are, so far as I can tell,
  discharged.** The lz4 cap's quantification over addressed tiles, the
  `[R-ENC-04]` ceiling's lack of that quantifier, §20.3 step 4's "in the
  generation this commit supersedes" tense on both the bar and the permission,
  and T26/§21.7's exclusion of T5 from the wrong-stride witnesses (which I
  verified by proving the shuffle fixes the final byte) are all correct as
  written. The one quantifier question I could not close from normative text is
  `adversary-01`.
