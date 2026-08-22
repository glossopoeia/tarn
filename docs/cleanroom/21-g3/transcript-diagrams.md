# Round 21 — Diagram auditor transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,377 lines), in four `Read` calls covering lines 1–4377, plus targeted
`grep`/`sed` over that same file. I opened no other file, ran no `git`
command, listed no directory, and issued no web request. I wrote and ran
scratch Python in
`/private/tmp/.../scratchpad/` (`crc.py`, ad-hoc scripts, and one
constructed binary `mini.tarn` that I wrote myself and hexdumped) — none
of which reads any file of the repository.

Context I did not ask for did appear before I began: a project instruction
file pointing at `AGENTS.md`, and an index of the maintainer's memory notes
naming several TARN working topics. I did not open any of it and did not
act on it. I also received a task list from the harness naming prior
rounds. None of it informed any judgement below; every claim here is traced
to a line of `spec/tarn.md` that I quote.

Method, per charter: enumerate every figure, layout table, worked example,
ASCII box, checklist and numbered list **first**, with line numbers; then
judge each one by doing its arithmetic myself.

---

## 1. Enumeration of every figure, table, box, example and checklist

### 1.1 Fenced ASCII boxes (`grep -n '^\s*>\?\s*```'`)

| Lines | What |
|---|---|
| 587–592 | §5.1 — a file after three commits (region box) |
| 1071–1090 | §7.4 — complete layer record payload, annotated byte offsets |
| 1202–1211 | §9.2 — what a crash sees (three rows) |
| 3059–3063 | §20.3(a) — a new layer |
| 3075–3079 | §20.3(b) — tiles added to an existing layer |
| 3099–3102 | §20.3(c) — a change confined to the directory |
| 3239–3245 | §20.5 — what compaction reclaims |
| 3998–4007 | Appendix A — annotated minimal file, 128-byte hexdump |

### 1.2 Tables (`grep -n '|---'`)

| Line of separator | Table |
|---|---|
| 236 | §2.4 outcome classes (5 rows) |
| 698 | §6.1 front signature block layout (2 rows) |
| 741 | §6.2 trailer layout (11 rows) |
| 905 | §7.2 record header layout (5 rows) |
| 978 | §7.3 record types of format major 1 (2 rows) |
| 1007 | §7.4 layer record inline payload (16 rows) |
| 1124 | §8.1 checksum coverage map (7 rows) |
| 1398 | §10.2 numeric identifier spaces (8 rows) |
| 1602 | §12.1 core sample types (13 rows) |
| 1834 | §14.2 byte layout / decoded size (2 rows) |
| 2002 | §15.1 tile-index entry layout (3 rows) |
| 2050 | §15.3 entry validity (11 rows) |
| 2442 | §18.2 user-metadata encoding byte (1 row) |
| 2598 | §18.4 standardized keys (6 rows) |
| 3129 | §20.4 stored-flags → updater obligation (3 rows) |
| 3377 | §21.2 file-scope register (36 rows) |
| 3421 | §21.3 layer-scope register (49 rows) |
| 3478 | §21.4 tile-scope register (26 rows) |
| 3528 | §21.5 ignored-record register (10 rows) |
| 3546 | §21.6 conditions that are not violations (14 rows) |
| 3668 | §21.9 minimum guarantees (8 rows) |
| 4010 | Appendix A byte annotation (14 rows) |
| 4046 | Appendix B constants (27 rows) |
| 4143 | Appendix E changelog (1 row) |

Plus the inline block quote at §15.1 lines 1996–1997 (the index region
schematic), which is a figure without a fence.

### 1.3 Worked examples (`> **Example`)

513 (§4.6 `température`); 577 (§5.1 smallest file); 584 (§5.1 three
commits); 1060 (§7.4 layer record); 1198 (§9.2 crash); 1518 (§11.2 grid);
1572 (§11.4 ordinals); 1635 (§12.1 bfloat16); 1684 (§12.3 channel entry);
1754 (§13.3 fill tuple); 1875 (§14.2 byte layout); 1909 (§14.3 packed
bool); 1965 (§14.5 padding); 2089 (§15.4 million-entry index); 2104 (§15.4
planar entries); 2203 (§16.2 slabs); 2384 (§17.3 shuffle); 3045 (§20.3
supersede cost); 3054 (§20.3 three shapes); 3236 (§20.5 compaction).

### 1.4 Checklists and numbered/counted lists

- §2.3 "five classes" (5 bullets)
- §4.6 "three further constraints" (3 bullets)
- §9.2 `[R-LIF-02]` steps (1)–(6)
- §10.1 "exactly four vehicles" (1–4)
- §17.2 codec 3 "Three frame features are excluded"
- §18.2 "Four restrictions apply" (4 bullets)
- §19.1 open, steps 1–4
- §19.4 tile read, steps 1–8
- §20.1 writer tiers (3 bullets)
- §20.3 appender, steps 1–6
- §21.2/3/4/5 stated counts (36 / 49 / 26 / 10)
- §21.8 stated totals (121 conditions, 273 instances)
- §22.2 "Three properties"; §22.3 "Four residues"
- Appendix D "Six choices"
- Appendix G items 1–10
- Appendix H five conformance checklists

---

## 2. Arithmetic and byte checks I performed

### 2.1 CRC-32C constants — all four verified

I implemented CRC-32C from §4.5's parameters alone (reflected Castagnoli,
init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and validated it against §4.5's own
check vector before using it:

```
CRC-32C("123456789") = 0xE3069283   (spec: 0xE3069283)   OK
CRC-32C(zero bytes)  = 0x00000000   (spec: 0x00000000)   OK
```

Then:

| Constant | Where | Spec value | Computed |
|---|---|---|---|
| Appendix A trailer CRC over [0,60) | line 4025 | `0xE00938D2`, stored `D2 38 09 E0` | 0xE00938D2, `d2 38 09 e0` |
| §7.4 example, CRC over 4 sentinel entries (80 B) | line 1069 | `0x80A34955`, stored `55 49 A3 80` | 0x80A34955, `55 49 a3 80` |
| §7.4 example, crc_of_crc_array | line 1070/1089 | `0xC4EE982E`, stored `2E 98 EE C4` | 0xC4EE982E, `2e 98 ee c4` |
| §15.4 full all-sentinel segment (2¹⁶ × 20 B) | line 2081 | `0xEECB3BB2` | 0xEECB3BB2 |

All four exact, including the little-endian storage direction each one states.

### 2.2 Appendix A, byte by byte

Trailer field decode from the hexdump at 3999–4007 against §6.2's layout:

```
[64,72)  8A 4E 52 41 54 0D 0A 1A   magic                    OK
[72,74)  01 00                     version_major = 1        OK (offset 8)
[74,76)  00 00                     version_minor = 0        OK (offset 10)
[76,80)  00 00 00 00               flags = 0                OK (offset 12)
[80,88)  01 …                      generation = 1           OK (offset 16)
[88,96)  10 …                      dir_offset = 16          OK (offset 24)
[96,104) 04 …                      dir_length = 4           OK (offset 32)
[104,112) 80 …                     committed_file_length=128 OK (offset 40)
[112,120) EF CD AB 89 67 45 23 01  file_id = 0x0123456789ABCDEF  OK (offset 48)
[120,124) 00 00 00 00              reserved zero            OK (offset 56)
[124,128) D2 38 09 E0              CRC = 0xE00938D2         OK (offset 60)
```

Offsets close: 8+2+2+4+8+8+8+8+8+4+4 = 64. §6.3's "The format-major-1
trailer has zero slack: every byte is assigned" holds.

Gate check against `[R-CNT-06]`: dir_offset 16 ≥ 16; dir_length 4 ≥ 4;
16 + 4 = 20 ≤ F − 64 = 64; F = 128 ≡ 0 (mod 64); 1 ≤ generation; file_id ≠ 0;
reserved zero. Directory region [16,20) = `00 00 00 00`, which is the
CRC-32C of the preceding dir_length − 4 = 0 bytes. Coverage: front [0,16),
directory [16,20), trailer [64,128), slack [20,64) = 44 bytes — disjoint,
matching §5.1's "44 bytes of slack".

The prose after the table also checks: 128 − 16 = 112 for the shorter
suffix window; a whole-file window on a 128-byte file is exactly what
"reaches offset 0" means.

### 2.3 §7.4's layer record example (line 1060)

Offset walk against §7.4's table order, verifying the packing rule "fields
are packed in table order with no alignment or padding between them":

```
 0 name          4  (u8 len 3 + "sst")
 4 layout        1
 5 linearization 2
 7 codec         2
 9 filter        2
11 alignment A   8
19 slab S        8
27 A_slab        8
35 rank d        1
36 channel C     2
38 dim entry    18  (1+1 name, 8 extent, 8 tile extent)
56 chan entry   12  (1+4 name, 2 type, 1+4 fill)
68 index_enc     1
69 entry_count   8
77 crc_of_crc    4
                --
                81
```

Every stated offset in the figure matches. The prose's own accounting —
"4 + 34 bytes, the dimension entry 18, the channel entry 12, and the
trailing fixed fields 13 — 81 exactly" — is right: the nine scalars from
layout through channel count are 1+2+2+2+8+8+8+1+2 = 34, and they are nine.

Geometry: ⌈100/32⌉ = 4, so entry_count = 4 for an interleaved rank-1 layer
(§11.2's N). Index extent length 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 80 + 4 = 84,
matching both the figure's "84" and §15.1's region shape.

Channel bytes at 56–67 are `04 74 65 6D 70 0C 00 04 00 00 C0 7F` — byte for
byte the twelve bytes §12.3's example gives, as the figure claims. Fill
`00 00 C0 7F` little-endian is 0x7FC00000, length prefix 4 = float32's
element size (`[R-CNT-23]`).

The segment is partial (4 entries, not 2¹⁶), so `[R-IDX-05]`'s "a partial
segment's CRC MUST be computed" applies — and the figure computes rather
than substituting 0xEECB3BB2. Correct.

### 2.4 §11.2 / §11.4 ordinals

(1024, 2048) with tiles (256, 256): G = (4, 8), N = 32, P = 65,536. With
extents (1000, 2048), G_y = ⌈1000/256⌉ = 4. Both as stated.

Spatial ordinals under s = Σ tᵢ ∏_{j>i} Gⱼ: (0,0)→0, (0,1)→1, (1,0)→8.
(300,700) → t = (1,2) → s = 10; u = (44,188) → 44·256 + 188 = 11,452.
Planar C = 4, channel 2 at s = 10 → 2·32 + 10 = 74. All as printed.

I also checked the formulas' ranges: max in-tile ordinal is P − 1, max
spatial ordinal N − 1, and at d = 1 the empty product convention reduces
both to u₀ and t₀ as §11.4 says.

### 2.5 §14.2, §14.3, §14.5 examples — computed

```
interleaved a(uint8)+b(uint16), T=(2,3): P=6, Q=3, decoded 18
  ordinal of (1,2) = 1*3+2 = 5; sample [15,18); a at 15, b at 16-17     OK
planar b: 6*2 = 12 bytes; ordinal 5 at byte 10-11                        OK
interleaved t(float32)+m(bool): Q=5, decoded 30; ordinal 5 [25,30);
  t at 25-28, m at 29                                                    OK
packed bool T=(2,5), P=10, alternating T,F,...:
  fill false -> 55 01 ; fill true -> 55 FD                               OK
padding, E=(5,5), T=(4,4): grid 2x2; edge tile (1,1) has 1 real
  position and 15 padding; decoded 16*2 = 32 bytes; fill 0xABCD -> CD AB OK
```

I also checked the table's own consistency claim "the table's forms with
k = u·C + c": with k = uC + c, k div C = u and k mod C = c, so
(k div C)·Q + F_{k mod C} = u·Q + F_c. Holds.

### 2.6 §17.3 shuffle example — computed

1.0f/2.0f/3.0f encode as `00 00 80 3F 00 00 00 40 00 00 40 40`; with s = 4,
n = 3 the map "byte i of group j at offset i·n + j" produces
`00 00 00 00 00 00 80 00 40 3F 40 40`, exactly the figure. The stated
inverse "restores byte i·n + j to offset j·s + i" round-trips.

A useful side result I derived while checking T26: under this permutation
the final byte at index L − 1 always maps to (s−1)n + (n−1) = L − 1, i.e.
the last byte never moves. So a mis-strided filter on a **packed bool
plane** can never disturb its pad bits, and T26's "the check that detects
it is T2's or T4's" — omitting T5 — is correct rather than an oversight.
I had suspected a missing row here and the arithmetic refuted me.

### 2.7 §15.4's million-entry example — computed

entry_count = 1,000,000 → ⌈1e6/65536⌉ = 16 segments, 15 full, last covering
1,000,000 − 983,040 = 16,960. CRC array 64 bytes; region
1,000,000×20 + 64 = 20,000,064. Tile 999,999 is in segment 15 at
segment-relative byte 20 × 16,959 = 339,180; array at
[20,000,000, 20,000,064); segment 15 at [19,660,800, 20,000,000). Full
segment = 65,536 × 20 = 1,310,720 = exactly 1.25 MiB. Every number as
printed.

Planar example: C = 4, N = 32, disk ordinal 74 → entry at [1,480, 1,500);
channel 3's entries 96–127, thirty-two of them.

### 2.8 §21.9's derivation Note — computed

2³² entries → 2¹⁶ segments → 2¹⁶ × 4 = 262,144 = 256 KiB; at 2³⁶ →
2²⁰ × 4 = 4 MiB. 12.5 MiB / 65,536 layers = 200 bytes per record. 256 MiB
is 16× the top of §11.3's "roughly 1 to 16 MiB". All hold.

### 2.9 §20.3's cost figures

32·20 + 4 = 644 for a 32-tile layer's re-emitted index ("one entry
re-pointed, 31 byte-identical"). 10⁶ tiles → 20,000,064 ≈ "about 20 MB".
Both hold.

### 2.10 §21 register — mechanical count

I parsed all 121 register rows and counted instances by §21.1's stated
rule ("Instances within a cell are separated by semicolons, and a cell
reading — is one instance"):

```
F: 36 rows, 58 instances
L: 49 rows, 116 instances
T: 26 rows, 55 instances
R: 10 rows, 44 instances
     121 rows, 273 instances
```

§21.2 says 36, §21.3 says 49, §21.4 says 26, §21.5 says 10; §21.8 says
"121 conditions over 273 instances". All four subsection counts and both
totals are exact.

I then re-derived a sample of cells from §21.1's enumeration rules rather
than trusting them:

- Magnitude rule ("*differs from*/*does not equal*" → two directions;
  "*exceeds*/*larger than*" → one): T3 = 3 layouts × 2 = 6; T14 = 6;
  T22 = 6; T21 = 3 (one direction, "larger than"); L44 = 3 ("exceeds");
  L21 = 2 layouts × 2 = 4; L30 = 2; F17 = 2; F23/L12 = 2. All consistent.
- "A comparison with no magnitude ordering enumerates no direction":
  F14, F20, L37, L38, T1 are all 1. Consistent.
- "a combination of two flag bits" → 1: F25 = 1, L46 = 2 (one per
  container). F19/F26 (any bit of a lane set) = 1. Consistent.
- Field-ranging: L1's eight u64 fields. I checked the omissions: **A** and
  **A_slab** are absent from L1, and correctly so — `[R-ENC-03]` binds
  "every offset, length, extent, and count", and an alignment is none of
  those; its 2⁶² ceiling comes from `[R-SLB-01]`/`[R-CNT-23]` and is
  registered at L39/L29. F2's six fields correctly exclude `file_id`,
  which is an identifier and is covered by F12 for its own zero case.
- L2's nine derived quantities: I checked the two dominance parentheticals.
  Q = Σ Bᵢ ≥ C so P·Q ≥ P·C = V; and (C−1)N + (N−1) = CN − 1 < CN. Both
  claims hold, so the omitted quantities really are dominated.
- R4 = 6 constraints × 2 containers = 12; the six are exactly §18.2's
  carried-over frame constraints plus "bytes remaining after the frame".
  R5 = 2 defects × 2 locations × 2 containers = 8. R7 = 3 alternatives × 2.
  All consistent with the bulleted restrictions they come from.

### 2.11 §15.3's own counts

"Six rows are marked *structural*" — I counted the table: rows 2–7 are the
six. Three rows are marked *verifier* (intra-layer overlap, cross-scope
overlap, alignment/slab). Each of the eleven rows maps onto exactly one
§21.4 or §21.3 register row, and §15.3's row 7 splits into T12 (overflow)
and T9 (> F − 64) — both present.

### 2.12 F33's cross-reference to the bounds rows

F33 says a claimant reaching the front block or the live trailer "is
instead caught by the bounds rows F9/F10, F31/F32, L16/L17 and T8/T9, each
at its own tier". I checked the four claimant kinds against those pairs:
directory → F9/F10; non-layer top-level record extent → F31/F32; layer
record and sub-record extents (which includes the tile-index region, since
§9.7 makes it the layer record's extent) → L16/L17; stored tile → T8/T9.
Complete, and no claimant kind is left without a pair.

### 2.13 Numbered lists

§10.1 vehicles 1–4 and §4.3's prose list of four agree item for item.
§9.2 steps 1–6 with every back-reference in §20.2/§20.3 ("steps 1–3",
"steps 4 and 6", "step 5", "steps 1–2", "steps 4–6") in range.
§19.1 1–4, §19.4 1–8 (with "Steps 3 through 6 run once per needed entry"
consistent), §20.3 1–6, Appendix G 1–10 — none out of order, duplicated or
missing. §17.2's "Three frame features are excluded" resolves to
dictionary, content-checksum flag, oversized window — three, with the
magic and the one-frame rules stated ahead of the sentence rather than
inside its count. §22.2's three properties and §22.3's four residues both
count out. Appendix D's six choices count out. §18.2's four restrictions
count out. §2.3's five classes match Appendix H's five checklists.

### 2.14 Requirement identifier space

161 distinct identifiers; every prefix contiguous from 1 with no holes
(`[R-ENC-100]` is §2.2's own illustration of the >99 rule, and
`[R-SER-04]` appears only in §14.4's withdrawal note, exactly as §2.2
prescribes). Every identifier cited in a register Governing-rule cell
exists.

### 2.15 Field taxonomy

`grep 'descriptive'` shows exactly one table cell so marked —
§6.2's `version_minor` — matching §4.7's "In format major 1 `version_minor`
is the only descriptive field". §4.7 also requires "each descriptive
field's definition states what a reader does when the field contradicts the
data it describes"; `[R-CNT-07]`'s "A reader MUST NOT reject a file for its
version_minor: minor releases are additive-only, and all feature gating is
structural" discharges that.

---

## 3. Building the thing end to end

Beyond auditing, I constructed a complete conforming one-layer file from
the document alone, to find out where I would have to guess.

Layer: rank 1, dimension `x` extent 4 tile extent 4 (so G = 1, N = 1,
P = 4), interleaved, one uint8 channel `v` with fill 0x00, codec 1,
filter 1, no alignment, no slab. entry_count = N = 1. Decoded tile size
P·Q = 4. Index region 1×20 + 1×4 = 24 bytes.

Placement I chose: tile at 16, index at 20, directory at 44
(24-byte header + 73-byte inline payload + 4-byte CRC = 101 bytes, ending
at 145), pad 145→192, trailer [192, 256), F = 256.

```
0000  89 54 41 52 4E 0D 0A 1A 00 00 00 00 00 00 00 00
0010  0A 0B 0C 0D 10 00 00 00 00 00 00 00 04 00 00 00
0020  00 00 00 00 5E E4 72 40 CD D7 8A 66 01 00 03 00
0030  49 00 00 00 14 00 00 00 00 00 00 00 18 00 00 00
0040  00 00 00 00 01 4C 01 01 00 01 00 01 00 00 00 00
...
00C0  8A 4E 52 41 54 0D 0A 1A 01 00 00 00 00 00 00 00
00D0  01 00 00 00 00 00 00 00 2C 00 00 00 00 00 00 00
00E0  65 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00
00F0  EF CD AB 89 67 45 23 01 00 00 00 00 9D CF 41 C5
```

Every field was determined by the document. The places I paused:

1. **"the pad to the next 64-byte boundary"** (`[R-LIF-02]` step 5) when
   the directory already ends on one — resolved by §6.2's "a writer that
   ends its directory on a 64-byte boundary leaves none". No guess.
2. **Layer record flags** — §7.3 fixes MU = 1, PE = 1, so the u16 is
   0x0003. `[R-CNT-22]` makes the stored bits non-authoritative but a
   writer must still emit them exactly. No guess.
3. **Codec 1's length equality** — `[R-COD-04]` ties the entry's length to
   the decoded size, checkable before any fetch. No guess.
4. **Whether the front block counts as a structure for placement** —
   §5.2 lists it as its own coverage class, so the first structure may sit
   at 16. Appendix G item 3 says the same. No guess.

I then re-walked the file as a reader per §19.1 steps 1–4 and §19.3 and it
passes every cited check. I could not find a place in the happy path where
the document left me to invent anything.

---

## 4. Findings

### diagrams-01 — Appendix H's reader checklist restates the acceptance duty without the carve-out the rule it cites carries (OBSERVATION)

**Location.** Appendix H, "Conforming reader" (lines 4319–4330); against
§2.3 `[R-CNF-03]` (lines 186–171), §21.6's closing paragraph (3573–3585),
and §21.9 `[R-ERR-04]` (3678–3688).

**Quotation.** Appendix H:

> **Conforming reader** — … accepts every conforming
> file within §21.9's minimum guarantees and reports any resource refusal
> as a limit rather than as corruption (`[R-ERR-04]`)

**Detail.** §2.3 states the duty with three qualifications, not one:

> A reader MUST accept every conforming file of
> a format major version it implements, carrying no record of a type
> it does not implement with MUST_UNDERSTAND = 1 … and
> none of whose values exceeds the minimum guarantees of §21's
> limits table

The first qualification is harmless in the checklist, because §2.3 also
says a file of another major is "neither conforming nor nonconforming under
it", so it is not a *conforming file* in this document's vocabulary. The
second is not harmless. §21.6's closing paragraph:

> The second is an **experimental-range top-level record type carrying
> MU = 1** (§10.2, §10.3): `[R-CNT-15]` obliges the reader to reject, and
> `[R-CNF-02]` makes the file conforming all the same.

So there exists a **conforming** file, every quantity inside §21.9's
guarantees, that a conforming reader MUST reject — and the checklist line
says the reader accepts it. The rule the line cites, `[R-ERR-04]`, names
the exception itself ("the two capability refusals §21.6 names, a foreign
format major and an unimplemented MU = 1 type, are not this ground"), which
makes the omission visible only if you follow the citation.

Readings I can defend: (a) the checklist means the duty exactly as §2.3
states it, with the MU = 1 carve-out implied; (b) the checklist means what
it says. I pick (a), because Appendix H is headed "(non-normative)" and
opens "each entry's authority is the requirement or section cited, never
this summary", and because `[R-CNT-15]`'s reject-file is an unqualified
MUST that no summary can displace. An implementer auditing only against the
checklist — which is what Appendix H is for — builds a reader that serves a
file it is obliged to refuse.

**Byte-level: no.** The normative text decides the case in three places
(§2.3, §21.6, `[R-CNT-15]`); a summary explicitly disclaiming authority
cannot fork it. Cost to an implementer is one missed rejection path found
late, not a divergence two careful implementations could both defend.

---

### diagrams-02 — `[R-CNT-27]`'s 128-byte reader check has no ordering, and only §21.2's preamble places it behind the version gate (AMBIGUITY)

**Location.** §5.1 `[R-CNT-27]` (lines 571–575); §21.2's preamble
(3362–3374); §6.2 `[R-CNT-06]` (769–778); F5 (line 3382).

**Quotation.** §5.1:

> No conforming file is shorter than 128 bytes: the front signature
> block, a directory of at least 4 bytes at an offset of at least 16,
> and the 64-byte trailer at a 64-aligned offset cannot be satisfied in
> fewer. A reader MUST treat a shorter file as a validity error at file
> scope. `[R-CNT-27]`

and §21.2's preamble:

> §6.2 puts the version gate ahead of every check but the trailer magic
> and the trailer CRC, so such a file is refused on capability grounds
> first. Four rows are outside that reasoning and do reach it

**Detail.** `[R-CNT-24]` fixes, permanently and across every major, only
the front block, the trailer magic at F − 64, the version fields at F − 56
and the CRC at F − 4, and forbids the trailer to grow. A future major may
therefore define a conforming 80-byte file: front block [0,16) and trailer
[16,80). Its magic and CRC verify; §6.2's version gate then refuses it on
capability grounds, and `[R-CNF-02]` says that refusal "is not a finding
about its bytes".

But `[R-CNT-27]`'s reader obligation is unconditional and carries no
ordering clause, and §6.2's own ordered list — "the trailer magic; the
trailer CRC; the version gate … and then, those gates passed, MUST validate
all of the following before acting on the fields involved" — orders the
*trailer's fields*, not a comparison of the physical file size against 128.
F5's two instances are "F (physical file size); committed_file_length": the
second is plainly post-gate (it is a trailer field), the first is not
ordered anywhere in §5, §6 or §19.1.

Permitted readings: (a) the 128-byte floor is a check a reader may make as
soon as it knows F, i.e. before the version gate — the plain reading of the
unconditional MUST in §5.1, and the natural implementation, since a reader
needs *some* size floor before it can even read the final 64 bytes;
(b) it is due after the version gate, as §21.2's preamble asserts.

I pick (b), on two grounds. `[R-CNF-02]` makes every file-level requirement
of this document a requirement about a stated major, so `[R-CNT-27]`'s
premise (dir_offset ≥ 16, dir_length ≥ 4, a 64-aligned trailer) is major-1
reasoning that cannot bind a major-2 file. And §21.2's preamble is
normative text (`[R-CNF-01]` exempts only Notes, Examples, Rationales and
appendices) that says so. But (b) is reached only by a reader who consults
§21.2's preamble — a place an implementer working through §5 and §6 has no
reason to be — and the preamble reaches it by attributing to §6.2 an
ordering §6.2's own text confines to trailer fields.

Without the resolution: a reader takes a conforming future-major file
shorter than 128 bytes and reports it *corrupt*, which is precisely what
`[R-CNT-07]` asks readers not to do ("a reader that reports an
unimplemented major as corruption misleads users into discarding files that
current software reads"); and a verifier reports *nonconforming* where §2.3
requires *cannot establish*.

**Byte-level: no.** Both readings reject the file; only the diagnostic
class and the verifier's verdict label differ, and `[R-CNT-07]`'s
diagnostic clause is a SHOULD. The verdict divergence is real but is
foreclosed by `[R-CNF-02]`'s "neither conforming nor nonconforming",
so no competent implementation could defend reporting *nonconforming*.
Nothing here moves the emittable set or an accept/reject verdict.

---

### diagrams-03 — §4.7's Note promises §7.2 folds *each* field's range into its Field cell; three of the five carry no range there (OBSERVATION)

**Location.** §4.7's presentation Note (lines 536–549); §7.2's record
header table (lines 904–910).

**Quotation.** §4.7:

> **Note.** Layout tables for fixed-layout structures give, per field:
> byte offset within the structure, size, type, name, taxonomy class,
> and valid range, each table giving the columns its structure needs.
> … §6.1's block is a 16-byte
> constant, where a Value column replaces type and range, and §7.2
> folds each field's range into its Field cell.

**Detail.** §7.2's table:

> | 0 | 2 | u16 | type (0 invalid) | structural |
> | 2 | 2 | u16 | flags: bit 0 MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2–15 reserved | structural |
> | 4 | 4 | u32 | inline_length | structural |
> | 8 | 8 | u64 | extent_offset | structural |
> | 16 | 8 | u64 | extent_length | structural |

`type` and `flags` do fold a range into the Field cell. `inline_length`,
`extent_offset` and `extent_length` fold nothing: their Field cells are
bare names. Their ranges are real and stated — `inline_length` is bounded
by the containing sequence (`[R-CNT-12]`, `[R-CNT-18]`), the extent slot by
`[R-CNT-13]`'s (0,0)/one-half-zero/< 16/past F − 64 rules and `[R-ENC-03]`'s
2⁶³ − 1 domain — but none of that is in the cell the Note says holds it.

The §6.1 half of the same sentence is delivered exactly (a Value column
replaces type and range), and §7.4's half is delivered exactly (offset and
class columns omitted for a packed payload), which is why this half reads
as an unmet promise rather than a loose paraphrase. The escape clause
"each table giving the columns its structure needs" licenses omitting a
*column*; it does not license a stated folding that three of five fields
do not receive.

Readings: (a) "each field's range" means "the ranges §7.2 chooses to give";
(b) it means every field's. I pick (b) — "each" is not "some" — and record
the mismatch. An implementer looking for the record header's field domains
in the layout table finds two of five and must go hunting.

**Byte-level: no.** Every one of the three ranges is stated normatively
elsewhere and is cited from §19.1 step 4 and §19.3; nothing about the
emittable set turns on where they are printed.

---

### diagrams-04 — §18.2's layout table gives "Valid values | 1 or 2" for the one enum whose out-of-set values leave the file conforming (OBSERVATION)

**Location.** §18.2's encoding table (lines 2441–2443); against
`[R-MTA-03]` (2445–2454), `[R-EXT-03]` (1426–1430), §21.6 (line 3556) and
`[R-MTA-10]` (2546–2566).

**Quotation.** §18.2:

> | Offset | Size | Type | Field | Class | Valid values |
> |---|---|---|---|---|---|
> | 0 | 1 | u8 | encoding | structural | 1 or 2; see below |

against §21.6:

> | A user-metadata record declares an experimental-range (≥ 0x80)
> document encoding | Ignored (ignore-record); the file is conforming —
> §10.3's prohibition binds a writer's conduct, not the bytes.

**Detail.** §4.7 defines the last column of a fixed-layout table as the
field's "valid range". For every other enum in the document that column
tells the truth about validity: §7.4's layout cell ("0 invalid; others
reserved"), its index_encoding cell ("any other value … is a validity error
at layer scope"), §6.2's version_major cell. The metadata-encoding byte is
the single field in the format where a value outside the assigned set does
**not** make the file invalid: 0 and 3–0x7F are violations (R1), while
≥ 0x80 leaves the file conforming and the record merely ignored. The cell
collapses that three-way partition to "1 or 2".

Readings: (a) "valid" here means "assigned", with "see below" carrying the
rest; (b) "valid" means the conforming set, and the cell is narrower than
the rule. I pick (a) — "see below" is an explicit deferral, and the prose
immediately under the table gives the full partition, as do §10.2's table,
§10.3, §17.4, §21.6 and `[R-MTA-10]`. But (a) makes this the one place in
the document where the "valid range" column means something different from
what it means everywhere else, and an implementer transcribing layout
tables into a validator writes a rejection for encoding 0x85 — a rejection
of a conforming file, which §21.6 says makes the *reader* the nonconforming
party.

**Byte-level: no.** Five separate normative passages say the experimental
encoding is conforming and ignore-record; the table cell defers explicitly
rather than contradicting. No implementation reading the section could
defend the strict reading.

---

### diagrams-05 — §21.6's sentinel row states the fill rule wider than `[R-TYP-08]` in two ways (OBSERVATION)

**Location.** §21.6's first table row (line 3547); against `[R-TYP-08]`
(§13.3, lines 1744–1752), `[R-GEO-04]` (§11.3) and §19.4 step 4
(2804–2812).

**Quotation.** §21.6:

> | An index entry is the sentinel | The tile is addressed but not stored;
> every sample position it carries reads as the channel's fill |
> `[R-IDX-02]`, `[R-TYP-08]` |

against `[R-TYP-08]`:

> a reader that returns any of
> the tile's sample positions inside the layer's extents MUST
> return, for each channel the tile carries, that channel's fill value
> at every such position.

**Detail.** Two divergences, both in the widening direction.

First, "every sample position it carries" — an edge tile carries padding
positions as well, and those lie outside the layer's extents. `[R-GEO-04]`
says "a reader MUST NOT return padding positions as samples", and §13.3's
own Note is explicit that the two mechanisms are different: "Fill governs
unstored tiles. The padding positions of stored edge tiles (§11.3) are a
different mechanism … and a reader never returns padding positions in any
case". The rule's qualifier "inside the layer's extents" is exactly what
the row drops.

Second, "the channel's fill" is singular. In an interleaved layer the
sentinel tile carries every channel, and the rule says "for each channel
the tile carries". §19.4 step 4 states both correctly — "every **requested**
sample position of its tile reads as fill — the entry's channel's recorded
fill in a planar layer; each carried channel's, in declared order, in an
interleaved layer".

Readings: (a) the row is shorthand for `[R-TYP-08]`; (b) it means what it
says. I pick (a). §21.1 pre-resolves it — "§21.6's entries restate their
governing rules on the same terms a row does, and where such an entry and
the rule it cites diverge, the rule governs there too" — which is why I
grade this low rather than dropping it: the divergence is real, and the
document's own device for handling it is what keeps it harmless.

**Byte-level: no.** `[R-GEO-04]`, `[R-TYP-08]` and §19.4 step 4 all decide
the case, and §21.1 subordinates the row to them by name.

---

## 5. Things I checked and did not report

For a triager's benefit, the checks that came back clean or that I talked
myself out of:

- **All four CRC constants and the entire Appendix A hexdump** — exact.
- **§7.4's layer record example** — every offset, every length, the 81-byte
  total, the 84-byte extent, the 12 bytes shared with §12.3 — exact.
- **T26 omitting T5.** I suspected a missing witness row for a mis-strided
  filter on a packed bool plane. The byte permutation fixes index L − 1, so
  the pad-bit byte can never move; T5 is genuinely unreachable there, and
  §21.7's separate list naming "T2, T4 or T5" for a *mis-ordered image* is
  right for a different reason (mis-ordering acts at bit granularity).
- **R6 versus R10 citing different governing rules** for two clauses of the
  same §18.2 bullet. This looked like a register inconsistency until I
  traced it: R6's empty/C0 clauses come straight from `[R-ENC-12]` with
  `[R-CNT-25]`'s quarantine redirect, while §21.9 says the 255-byte cap on
  keys is "this specification folding §4.6's name rules onto keys, which
  carry no length prefix to force it" — i.e. `[R-MTA-04]`'s own. The split
  is principled.
- **§2.3's MU = 1 carve-out lacking a "top-level" qualifier.** Not a
  contradiction: `[R-CNT-18]`'s "where the file is otherwise conforming a
  reader MUST NOT reject the file for it" is a positive prohibition, and
  "no acceptance duty" is not a licence to reject.
- **§20.5's "(F36, L25, R1)"** as a partial list of reserved-range rows.
  On a *conforming* input those three are the only reserved-range rows a
  compactor could carry forward without refusing under `[R-WRT-09]`, so
  the list fits its context.
- **§21.2's "Four rows"** — F1, F6, F8, F14, and F18 correctly excluded as
  "outside the premise". Verified against `[R-CNT-24]`'s permanently-fixed
  field list.
- **§8.1's coverage map against §4.5's three terminal and three interior
  checksum fields** — every byte of a live state falls under exactly one,
  including the segment CRC array (crc_of_crc_array), crc_of_crc_array
  itself (directory CRC), and each entry's crc field (segment CRC).
- **§10.2's eight spaces against their defining sections** — assigned,
  reserved and experimental bands agree everywhere; the finer splits in
  §11.4 and §12.2 are sub-partitions of one reserved band, not divergences,
  and `[R-EXT-05]` governs anyway.
- **§12.1's thirteen types against Appendix C**, including the pinned
  reservations 14–19 — identical.
- **§21.9's table against Appendix B's "Reader minimum guarantees" row** —
  all eight quantities, same values.
- **Appendix B's 27 constants against their defining sections** — no stale
  value found.
- **Appendix H's verifier checklist against the complete set of
  verifier-detected rows** (F7, F25–F28, F33, F36, L18, L25, L40–L42,
  L46–L49, T2, T4, T5, T26) — every row has a checklist line.
- **Appendix G's ten items against its own closing paragraph** — every item
  accounted for, and the paragraph disclaims its own count ("Read the
  numbered items as the list; this paragraph names what they are for, not
  how many there are"), which forecloses the count mismatch I went looking
  for.
- **Appendix H's writer checklist omitting `[R-CNT-08]`'s "MUST write
  flags = 0"** and four of the five writer-side SHOULDs. Considered and
  dropped: the appendix says "A summary", which promises no exhaustiveness,
  and singling out `[R-CNT-03]` is presented as an example of an advisory
  rather than as the only one.
- **§5.1's three-commit box** — the region order is exactly what three
  commits (create A; add B; touch nothing) produce, and the underbrace
  label "re-emitted" spanning the pad is clarified two lines later by "the
  pad and the ▓ runs are slack".
- **§20.3(c)'s three directory-only operations** — clearing a slab
  declaration, renaming a layer and changing fill on a layer with no
  padding position and no pad bit all leave §14's fixed quantities alone,
  so step 4's bar does not reach them.
- **§21.6's "The file contains zero layers | A conforming file with an
  empty directory"** — the behavior cell is narrower than the condition (a
  file with zero layers can still carry a file-scope user-metadata record),
  but §21.1's precedence clause covers it and `[R-CNT-14]` itself uses the
  same shorthand. Judged noise.
