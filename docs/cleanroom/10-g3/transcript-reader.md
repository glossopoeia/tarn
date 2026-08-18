# Cleanroom round 10 — Reader implementer transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,919 lines), in five `Read` calls covering the whole document, plus targeted
`grep`/`python3` passes over that same file. I opened no other file: no `docs/`,
no ADRs, no `PLAN.md`, `AGENTS.md`, `README.md`, `OPEN-QUESTIONS.md`, no
`conformance/`, no `spec/registry.json`, no git history, no web access. I did not
list any directory.

Computation I ran, all of it local and reading no file other than the spec:

- A from-scratch CRC-32C implementation (reflected table built from polynomial
  0x1EDC6F41), used to check the document's three stated CRC constants.
- A Python pass over the §21 register tables to count rows and instances
  mechanically, and to check that every row's Detector/Detected pair is one of
  the pairs §21.1 licenses.
- A Python pass collecting every `[R-XXX-NN]` identifier to check for numbering
  gaps.

Scratch files written: `crc.py`, `crc2.py` in my scratchpad. Output written:
this transcript.

---

## 0. How I worked

I wrote the reader in the order I would actually write the code: cold open →
validation tiers → layer access → tile read → degradation → worked example.
Where the document told me what to do I recorded the rule and moved on; where I
had to stop and decide, I recorded the decision and why. The findings at the end
are only the places where I had to guess, or where two passages I needed both
could not both be true.

I checked the document's arithmetic wherever it stated a number I could
reproduce. That is the cheapest way to find a real defect and it is where the
last few rounds' survivors came from, so I did it first.

---

## 1. Arithmetic and constants I verified independently

### 1.1 CRC-32C

I built CRC-32C from §4.5's parameters alone — "the Castagnoli polynomial
0x1EDC6F41 (RFC 3720 §12.1), reflected input and output, initial value
0xFFFFFFFF, and final XOR 0xFFFFFFFF, stored as a little-endian `u32`" — without
consulting any implementation. Reflecting 0x1EDC6F41 gives 0x82F63B78, which is
what a reflected table-driven implementation needs.

| Constant | Document | Computed | Verdict |
|---|---|---|---|
| CRC-32C(`"123456789"`) (§4.5, App B) | `0xE3069283` | `0xE3069283` | ✅ |
| CRC-32C(zero bytes) (§4.5, §7.1, App A) | `0x00000000` | `0x00000000` | ✅ |
| CRC of a full all-sentinel segment (§15.4, App B) | `0xEECB3BB2` | `0xEECB3BB2` | ✅ |
| Appendix A trailer CRC over trailer bytes [0, 60) | `0xE00938D2` (stored `D2 38 09 E0`) | `0xE00938D2` | ✅ |

The all-sentinel constant was computed over 65,536 copies of the 20 bytes
`FF ×16 00 ×4` — §15.2's sentinel and §15.4's "full segment — one covering
exactly 2¹⁶ entries". It matches. That constant is the one place in the document
where a writer is licensed to emit a checksum without computing it
(`[R-IDX-05]`), so a wrong value there would have been a live byte-level defect.
It is right.

### 1.2 Appendix A, walked field by field

I decoded the hex dump against §6.2's trailer layout rather than against the
annotation table, then compared.

```
0040  8A 4E 52 41 54 0D 0A 1A  01 00 00 00 00 00 00 00
0050  01 00 00 00 00 00 00 00  10 00 00 00 00 00 00 00
0060  04 00 00 00 00 00 00 00  80 00 00 00 00 00 00 00
0070  EF CD AB 89 67 45 23 01  00 00 00 00 D2 38 09 E0
```

Trailer begins at file offset 64 (= F − 64 = 128 − 64), 64-aligned ✅.

| Trailer offset | Field | Bytes | Value | §6.2 valid range | ✓ |
|---|---|---|---|---|---|
| 0 | magic | `8A 4E 52 41 54 0D 0A 1A` | — | exact constant | ✅ |
| 8 | version_major | `01 00` | 1 | 1 | ✅ |
| 10 | version_minor | `00 00` | 0 | any | ✅ |
| 12 | flags | `00 00 00 00` | 0 | no incompat bit | ✅ |
| 16 | generation | `01 00 …` | 1 | 1 ≤ g ≤ 2⁶³−1 | ✅ |
| 24 | dir_offset | `10 00 …` | 16 | ≥ 16 | ✅ |
| 32 | dir_length | `04 00 …` | 4 | ≥ 4 | ✅ |
| 40 | committed_file_length | `80 00 …` | 128 | = F, mult of 64 | ✅ |
| 48 | file_id | `EF CD AB 89 67 45 23 01` | 0x0123456789ABCDEF | ≠ 0 | ✅ |
| 56 | reserved | `00 00 00 00` | 0 | zero | ✅ |
| 60 | CRC | `D2 38 09 E0` | 0xE00938D2 | CRC over [0,60) | ✅ computed |

Cross-checks: dir_offset + dir_length = 20 ≤ F − 64 = 64 ✅. Directory region
[16, 20) is four bytes = CRC-32C of a zero-byte record sequence = 0x00000000 ✅.
Pre-trailer pad [20, 64) = 44 bytes, and the annotation says 44 ✅. The 128-byte
floor of `[R-CNT-27]` is forced exactly as §5.1 claims: 16 + 4 = 20, the trailer
must start at a multiple of 64 with F a multiple of 64, so F − 64 ≥ 20 forces
F ≥ 128.

Appendix A's closing paragraph is also arithmetically right: a 112-byte window
covering [16, 128) contains the directory (containment test, §6.4) while leaving
[0, 16) non-resident — 128 − 16 = 112 ✅.

**Appendix A is clean.** I found no wrong constant, offset, or checksum anywhere
in the document.

### 1.3 Every worked example in Part II

I recomputed each rather than reading past it.

- §11.2/§11.4: extents (1024, 2048), tiles (256, 256) → G = (4, 8), N = 32,
  P = 65,536 ✅. Coordinate (300, 700) → tile (1, 2), s = 1·8 + 2 = 10 ✅;
  in-tile (44, 188) → 44·256 + 188 = 11,452 ✅; planar C = 4, channel 2 →
  2·32 + 10 = 74 ✅. With extents (1000, 2048), G_y = ⌈1000/256⌉ = 4 ✅.
- §12.3: `temp`/float32/NaN 0x7FC00000 → `04 74 65 6D 70 0C 00 04 00 00 C0 7F`,
  12 bytes ✅ (1 + 4 + 2 + 1 + 4).
- §4.6: `température` NFC = 12 bytes, prefix 12 ✅; NFD = 13 ✅.
- §14.2: interleaved (2,3), a:uint8 + b:uint16 → Q = 3, size 18, ordinal 5 at
  [15, 18) ✅. Planar b → 12 bytes, ordinal 5 at [10, 12) ✅. t:float32 +
  m:bool → Q = 5, size 30, ordinal 5 at [25, 30), m at byte 29 ✅. The
  generalisation `u·Q + Fᶜ` is the table's form with k = u·C + c ✅.
- §14.3: planar bool (2,5), P = 10, alternating → `55 01` with fill false,
  `55 FD` with fill true (pad bits 2–7 set = 0xFC | 0x01) ✅.
- §14.5: extents (5,5), tiles (4,4) → grid 2×2; edge tile (1,1) covers 4–7 on
  both axes = 16 positions, 1 real ((4,4)) and 15 padding ✅; uint16 fill
  0xABCD → 32-byte tile, values 1–15 each `CD AB` ✅.
- §15.4: entry_count = 1,000,000 → 16 segments (15 full + 16,960), 64-byte CRC
  array, region 20,000,064 bytes ✅. k = 999,999 → segment 15, segment-relative
  byte 20 × 16,959 = 339,180 ✅; CRC array at [20,000,000, 20,000,064) ✅;
  segment 15 at [19,660,800, 20,000,000) ✅ (983,040 × 20). Full segment
  = 65,536 × 20 = 1,310,720 = 1.25 MiB ✅.
- §15.4 second example: planar C = 4, N = 32, channel 2 at s = 10 → ordinal 74,
  entry at [1,480, 1,500) ✅; channel 3 unstored → entries 96–127 ✅.
- §16.2: N = 32, S = 8 → four runs [0,8) [8,16) [16,24) [24,32) ✅; tile rows
  1–2 under row-major = ordinals 8–23 = runs 1 and 2 ✅.
- §17.3: 1.0/2.0/3.0 float32, s = 4, n = 3, byte i of group j → offset i·n + j
  gives `00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40` ✅ — matches the document.
- §20.3: 32-tile layer index = 32·20 + 4 = 644 ✅; 10⁶-tile layer ≈ 20 MB ✅.
- §19.4 note: entries for one spatial ordinal are N·20 bytes apart, and for
  N ≥ 2¹⁶ the ordinal gap N ≥ 2¹⁶ guarantees different segments ✅.
- §21.9 note: 2³² entries / 2¹⁶ per segment = 2¹⁶ segments × 4 = 256 KiB ✅;
  at 2³⁶ it is 4 MiB ✅; 12.5 MiB / 65,536 ≈ 200 bytes per layer record,
  consistent with "small layer records" ✅.

Every one checks. This document's numbers are in better shape than any I would
expect at this stage.

### 1.4 The register's own arithmetic

§21.8 claims "121 conditions over 248 instances", and §21.1 makes the count
mechanical: "Instances within a cell are separated by semicolons, and a cell
reading — is one instance."

I extracted every register row and counted:

| Section | Header claim | Rows counted | Instances counted |
|---|---|---|---|
| §21.2 | 36 conditions | 36 | 53 |
| §21.3 | 49 conditions | 49 | 106 |
| §21.4 | 26 conditions | 26 | 45 |
| §21.5 | 10 conditions | 10 | 44 |
| **§21.8** | **121 / 248** | **121** | **248** |

Exact on both axes. I also checked every row's Detector/Detected pair against
§21.1's rule that reader rows name one of §19.2's four tiers and verifier rows
name *certification*: zero anomalies across all 121 rows.

### 1.5 Identifier numbering

No gaps in any prefix except `ENC`, where 17–99 are absent because `[R-ENC-100]`
appears only as §2.2's illustration of how numbering extends. `[R-SER-04]`
appears exactly once, in §14.4's withdrawal note, consistent with §2.2's
"a withdrawn requirement leaves its identifier permanently retired".

---

## 2. The open path — byte-exact

This is the first thing I wrote, and the document determines it completely.

### 2.1 Cold remote open against a ranged server

**Request 1.** `Range: bytes=-64`. Cost: 64 bytes of body.

What bounds it before I have read anything: the constant 64. `[R-CNT-24]` makes
that constant permanent across every format major version ("the final 64 bytes
of a file contain the trailer magic at F − 64, version_major and version_minor
at F − 56, and a CRC-32C at F − 4"), so I can issue this request before knowing
anything about the file, including its major version. The response also carries
F: §6.4 and `[R-CNT-10]` require the size I compare against
committed_file_length to be transport-authoritative — "a full-response content
length, the complete length of a range response, or a size probe" — and a 206's
`Content-Range: bytes 64-127/128` supplies it. So §19.1's steps 1 and 2 cost one
request between them. `[R-CNT-10]` also tells me what to do on a 200 (abort, or
accept the full body deliberately — never treat a prefix as the range) and to
fall back to size-probe-plus-absolute-range where suffix ranges are unsupported.

**Validation of request 1's bytes,** in §6.2's mandated order:

1. magic == `8A 4E 52 41 54 0D 0A 1A` (else F8/F1, reject-file)
2. CRC-32C over [0, 60) == the u32 at [60, 64) (else F14)
3. version gate: version_major ≠ 0 and implemented (else F18, or a capability
   refusal that §6.3 requires be diagnosed distinctly from "not TARN" and
   "corrupt")

Only these three touch fields at positions `[R-CNT-24]` fixes across majors —
which is exactly why they come first. Then, gates passed, before acting on any
other field:

4. flags: no set bit in [0, 15] (F19); ignore all bits in [16, 31]
5. committed_file_length == F (F17) and F mod 64 == 0 (F13)
6. dir_offset ≥ 16 (F9); dir_length ≥ 4 (F16); dir_offset + dir_length ≤ F − 64
   (F10)
7. 1 ≤ generation ≤ 2⁶³ − 1 (F11); file_id ≠ 0 (F12); reserved [56, 60) zero
   (F15)
8. F ≥ 128 (F5, `[R-CNT-27]`)

I noted that `[R-CNT-06]`'s enumerated list does not separately state the
2⁶³ − 1 domain check for dir_offset/dir_length/committed_file_length that F2
registers. It does not need to: `[R-ENC-03]` is general ("a reader MUST treat a
value above 2⁶³ − 1 in any such field as a validity error at the owning scope"),
and §19's preamble closes the gap explicitly — "Those enumerations are not the
complete inventory of what a reader detects at that tier: §21's register is."
That preamble is load-bearing and I relied on it several times.

**Request 2.** `Range: bytes=<dir_offset>-<dir_offset+dir_length-1>`. Cost:
dir_length bytes.

What bounds it: dir_offset and dir_length, which I may act on only after the
trailer CRC verified (`[R-ENC-05]`, `[R-ENC-10]`) and after gate 6 bounded them
against F. So the second range can never exceed the file.

**Total: 2 requests, 64 + dir_length bytes.** The front signature block is not
fetched — §6.4 says so outright ("the two-request accounting of §6.4 does not
include the front block"), and §19.1 step 1 lets a reader that would have to
issue a further range request for [0, 16) defer or omit the check. For Appendix
A's file: **2 requests, 68 bytes.**

The speculative variant: one request for a suffix window (§6.4 recommends
writers keep trailer + pad + directory within 65,536 bytes so a 64 KiB suffix
captures both). If the window contains [dir_offset, dir_offset + dir_length),
request 2 is unnecessary — §6.4's containment test. On a file smaller than the
window the response is the whole file, [0, 16) becomes resident, and the
front-block check becomes mandatory. **This is where I hit my one byte-level
finding; see reader-01.**

### 2.2 Directory and record walk (steps 3–4)

Verify the final 4 bytes of the region against CRC-32C over the preceding
dir_length − 4 (`[R-CNT-11]`, F20) **before any other use** — including before
parsing a single record header. Then walk the record sequence, which is exactly
the covered bytes: dir_offset .. dir_offset + dir_length − 4.

Per record (24-byte header, then inline_length bytes):

- header or inline payload past the sequence end, or residue after the last
  complete record → F29, reject-file
- type == 0 → F24, reject-file (explicitly *not* an unknown type)
- unknown type, MU = 1 → reject-file; MU = 0 → ignore (`[R-CNT-15]`).
  Reserved-range type with MU = 1 → F35 (reader); reserved-range type at all →
  F36 (verifier)
- multiplicity: at most one top-level user-metadata record (F34)
- for **non-layer** top-level records, the extent slot rules (F30/F31/F32) —
  and note carefully that a *layer* record's slot is **not** checked here,
  because `[R-CNT-13]` scopes it to the layer and §19.3 defers it
- for a top-level user-metadata record, three framing checks on top: slot ≠
  (0,0) (F21), extent_length ≥ 5 (F22), inline_length == 1 (F23). §7.1 and
  §18.1 draw the quarantine boundary precisely here: framing failures precede
  the document and take the containing scope; everything from the encoding byte
  inward is ignore-record. That boundary matters and the document states it
  twice, consistently.
- build the layer table from each layer record's name — the first field of §7.4's
  inline payload, so no full parse is needed

The name handling in §19.1 step 4 is the most carefully written paragraph in the
document and I want to record that I checked it rather than skimmed it.
Uniqueness is decided **first**, over raw bytes, "whether or not each name is
itself well-formed" — which is coherent because `[R-ENC-13]` makes comparison a
byte comparison. A layer record whose name field does not lie within its
inline_length contributes no name and is instead reject-layer. So:

- two byte-identical name fields → F4, reject-**file**, even if neither name is
  valid UTF-8
- one ill-formed name, no duplicate → L3/L5/L6, reject-**layer**, detected at
  open

I implemented it in that order and it is unambiguous.

**The open's working set is the trailer and the directory, nothing else**
(`[R-RDR-01]`), at any file size and layer count. No extent slot's content, no
index, no payload.

---

## 3. Validation timing by tier

`[R-RDR-02]` fixes the *latest* detection point; earlier is always licensed
(`[R-CNF-12]`). My tier table, built from §19.2 plus the register's Detected
column:

**At open** — front block (if resident), trailer, directory region + record
walk, layer-name namespace. Register rows: F1–F6, F8–F24, F29–F32, F34, F35;
L3, L5, L6; R1 for a top-level record.

**At first access to a layer** — the whole of §19.3, and it performs **no I/O**:
"All are decidable from the resident directory and F." Slot validity
(`[R-CNT-13]`), the §7.4 constraint set (`[R-CNT-23]`, `[R-CNT-16]`), exact
parse and sub-record walk (`[R-CNT-18]`), sub-record multiplicity, dimension and
channel name rules, fixed widths and u64 domain, the value sets of §11.4, §12.2,
§14.1, §15.1, §17.2, §17.3, bool fill (`[R-TYP-07]`), the lz4 declaration bound
(`[R-COD-07]`), the geometry floor and its overflow-checked arithmetic, and the
index cross-checks computable without I/O (`[R-CNT-17]`). Register rows: L1, L2,
L4, L7–L17, L19–L36, L39, L43–L45; R1 for a sub-record.

**At use of a tile** — L37, L38 (index chain, outcome **layer** scope though
detected at tile use — §19.2 calls this out), then T1, T3, T6–T25.

**At use of a record's extent** — R2–R10. "no earlier, since the open fetches no
extent."

**Never obliged** — every row whose Detector is *verifier*: F7, F25–F28, F33,
F36; L18, L25, L40–L42, L46–L49; T2, T4, T5, T26. `[R-CNF-12]` lets me reject
anyway; `[R-CNF-04]` does not oblige me to look.

The one thing I had to reason about rather than read: §19.2's tier bullets do
not mention the encoding-byte check (R1) or the register rows generally, but
§19's preamble says outright that the register is the inventory and "A row this
section does not restate is due at its own tier all the same." So R1 at open for
a top-level record is right, and my reader ignores such a record at open without
ever fetching its extent.

---

## 4. Layer access and the tile-read algorithm

### 4.1 From a layer name to declarations

Look the name up in the table built at open (raw-byte comparison, no
normalisation — `[R-ENC-13]`). Run §19.3's full validation. Everything I need
after that is a pure function of the layer record:

```
G_i = ceil(E_i / T_i)               # stated as E_i/T_i + (E_i mod T_i != 0)
N   = prod G_i                      # spatial tiles
P   = prod T_i                      # sample positions per tile
addressed = N (interleaved) or C*N (planar)
Q   = sum B_i                       # interleaved sample stride
F_c = sum_{j<c} B_j                 # channel c's in-sample offset
decoded_size = P*Q                        (interleaved)
             = P*B_c                      (planar, numeric c)
             = ceil(P/8)                  (planar, bool c)
```

Every product is subject to `[R-ENC-04]`; L2 enumerates the nine I must check,
and I checked that its dominance claims are true: (C−1)·N + (N−1) = C·N − 1 < C·N ✅,
and V = P·C ≤ P·Q since every Bᵢ ≥ 1 so Q ≥ C ✅. The document deliberately
avoids `(E+T−1)/T` because the intermediate can leave the declared domain — a
detail I would otherwise have got wrong.

Index region layout, from `[R-IDX-01]` and `[R-CNT-17]`:

```
entries    : region bytes [0, entry_count*20)
CRC array  : region bytes [entry_count*20, entry_count*20 + ceil(entry_count/2^16)*4)
extent_length MUST equal entry_count*20 + ceil(entry_count/2^16)*4   (0 iff entry_count == 0)
segment s covers entries [s*2^16, min((s+1)*2^16, entry_count))
segment s bytes: [s*2^16*20, min((s+1)*2^16, entry_count)*20)
```

Because `[R-CNT-17]` ties extent_length to entry_count and `[R-CNT-13]` ties the
extent to F, both fetch ranges are bounded before I issue them. §22.2's note
says exactly this and it is true.

### 4.2 The read, step by step

1. **Domain.** Point request: 0 ≤ xᵢ < Eᵢ, else the request fails as a request
   with no verdict on the file. Region request: intersect with the extents;
   disjoint or zero-extent layer returns no samples, successfully.
2. **Ordinals.** tᵢ = xᵢ div Tᵢ, uᵢ = xᵢ mod Tᵢ; s = Σ tᵢ·∏_{j>i} Gⱼ; in-tile
   ordinal Σ uᵢ·∏_{j>i} Tⱼ (row-major, permanently, for every linearization
   value); disk ordinal = s interleaved, c·N + s planar.
3. **Index chain.** Fetch the CRC array and the segment containing the entry
   (both ranges computable from the layer record alone, parallelisable), verify
   crc_of_crc_array over the array, then the segment CRC over the segment. Any
   mismatch → **reject-layer** (L37/L38), even though I am at tile use.
   Verification results may be cached under `[R-LIF-03]`'s (file_id, range) key.
4. **Entry.** Classify by §15.3's table. I traced the whole table:
   - `(S, S, 0)` → valid sentinel, reads as fill
   - `(S, S, ≠0)` → structural reject-tile (T6)
   - exactly one of offset/length == S → structural reject-tile (T7)
   - length == 0 non-sentinel → structural reject-tile (T10). This catches a
     zeroed index region, which §15.2's rationale says is the point of choosing
     all-ones over zero/zero — a zeroed region is loudly invalid rather than
     silently all-sparse. I confirmed `(0, 0, 0)` lands on this row and not on
     the sentinel row.
   - offset < 16 → T8; offset or length > 2⁶³−1 → T11; sum overflow or
     offset + length > F − 64 → T9/T12
   - stored bytes fail the crc → T1 reject-tile, **entry still well-formed** —
     its extent stands, it stays in the coverage walk, in run continuity, and in
     the verifier overlap rows. The six *structural* rows behave the opposite
     way. That distinction is stated three times (§15.3, §9.7, §16.2) and is
     consistent in all three.
5. **Payload.** Fetch [offset, offset + length), verify the crc **before**
   decoding.
6. **Decode.** Codec first, then the filter's inverse. (Writer order is filter
   then codec; `[R-COD-01]` states both directions, so I could not get this
   backwards.) Then `[R-SER-07]`: decoded length must be *exactly* the
   declaration-derived decoded size, else T3 reject-tile. I allocate from the
   declarations, never from the payload, and never from a codec's embedded size
   field (`[R-COD-06]` forbids it explicitly for zstd's content size).

   Byte-shuffle inverse: stride s = Bᶜ for a planar numeric tile, Q for an
   interleaved tile, 1 (identity) for a packed bool plane; n = L/s; restore byte
   i·n + j to offset j·s + i. L is divisible by s in every case, which I
   verified holds for all three decoded-size formulas.
7. **Extract.** planar numeric: value k at k·Bᶜ. planar bool: value k at bit
   k mod 8 of byte k div 8, LSB-first. interleaved: value k at
   (k div C)·Q + F_{k mod C}, i.e. channel c at in-tile ordinal u sits at
   u·Q + Fᶜ. Padding positions are never returned.
8. **Return.** Bit patterns unaltered. NaN payloads preserved, −0.0 ≠ +0.0. The
   single exception is `[R-SER-08]`: an interleaved bool byte that is neither
   0x00 nor 0x01 cannot occur in a conforming file, and if I meet one and choose
   to return it rather than reject, I report 0x00 as false and every other byte
   as true. §12.3 and Appendix H both name this as the sole resolved byte, and
   they agree.

   For a multi-entry request, `[R-CNF-09]` bars standing fill in for a rejected
   tile; I may return the good entries plus a per-entry failure report, or fail
   the whole request. A layer-scope failure (step 3) instead bars the rest of the
   request and all further service from that layer, prospectively — values
   already returned stand.

### 4.3 Sparse and fill

A sentinel short-circuits steps 5–6 with **no payload I/O**. Interleaved: every
carried channel's fill, in declared channel order. Planar: exactly that entry's
channel reads fill, so one sample can mix decoded and fill channels. Fill comes
from the channel entry, bit-exactly, never from a type-derived default.

`[R-TYP-09]` is the rule I would have got wrong without reading it: fill is
produced by **exactly one** condition — a sentinel from a verified chain. A
malformed entry, a failed segment CRC, or a failed tile crc must never yield
fill. I wired that as a hard assertion in my design.

---

## 5. Degradation walks

Five traced end to end, plus three more in brief.

**(1) Unknown top-level record type 0x9001, MU = 1.** Open reaches step 4,
`[R-CNT-15]` → reject-file. Nothing is served. But §21.6's closing paragraph
tells me the file may be perfectly **conforming** — an experimental-range type
with MU = 1 is conforming bytes that a reader must nevertheless refuse — so my
diagnostic says "unsupported critical record type", not "corrupt". If the type
were in the reserved range 0x0003–0x7FFF instead, same reader behaviour, but the
file is nonconforming (F35 reader, F36 verifier).

**(2) Unknown top-level record type 0x9001, MU = 0.** Ignored, skipped as though
absent. Every layer serves normally. As an updater I would preserve it
byte-identically if PE = 1, and could drop it only in a commit that
independently changes the file's layer set or another non-layer top-level record
if PE = 0. As a compactor I may relocate its extent and re-point its slot — safe
because `[R-CNT-13]` forbids an MU = 0 record from encoding file offsets in its
own payload or extent.

**(3) Unknown codec value 0x8000 on layer B of a three-layer file.** Nothing at
open. First access to B → `[R-COD-03]`, L43, reject-layer. Layers A and C serve
completely. I may still list B's name (§2.4's reject-layer row). If instead the
value were an unknown **sub-record type with MU = 1** inside B's record, the
outcome is the same scope — `[R-CNT-18]` says "reject-layer — never
reject-file". That asymmetry against the file-scope rule is deliberate and
stated.

**(4) Truncated tail.** Two sub-cases, and the document distinguishes them:
- Physical file longer than committed_file_length (a torn append, or residue a
  writer failed to truncate): the trailer I read at physical-end − 64 is not a
  trailer → F8, reject-file. `[R-LIF-05]` forbids me to scan backward. §9.5's
  note is explicit that residue carries no register row of its own because the
  state I can observe is already named by F8/F14/F17.
- File truncated to an earlier commit boundary: a *valid* earlier trailer sits
  at the physical end, committed_file_length matches, everything validates. I
  open generation n − 1 and cannot tell. §9.6 states this: "truncation of a file
  to an earlier commit boundary is indistinguishable in-format from that earlier
  version — rollback detection requires out-of-band state." That is a stated
  property, not a gap.

**(5) Checksum mismatch, one per scope.** Directory CRC → reject-file. Segment
CRC → reject-**layer** (the whole layer, not the segment). Tile crc →
reject-tile, neighbours unaffected, and **not** fill. User-metadata extent CRC →
ignore-record with a SHOULD-report; the layer's samples are untouched, because
"Application metadata never invalidates the structural data it annotates."

**(6) Limit exceeded.** A layer declaring entry_count = 2⁴⁰ against my 2³² floor:
`[R-ERR-04]` lets me decline at the whole file or at the narrowest scope whose
declarations exceed what I can serve — here the layer. I MUST report it as a
resource limit and not as a validity error. A user-metadata document decoding
past my bound is different: §18.2's note says a document has no declared size and
so no narrower scope, so a resource decline there is at the whole file, while
simply ignoring the record is the other licensed path.

**(7) version_major = 2.** Reject-file, with a diagnostic distinct from both
"not a TARN file" and "corrupt" (§6.3 gives the wording). The file is neither
conforming nor nonconforming under this document (`[R-CNF-02]`).

**(8) Set incompat-lane flag bit.** Reject-file (F19). A set ignore-lane bit:
ignored, file conforming, and as an updater I copy it forward and MUST NOT clear
it.

---

## 6. Where the document made me guess

Everything above I could implement without guessing. The following are the
places I stopped.

---

### reader-01 — CONTRADICTION — §6.1 `[R-CNT-04]`, §19.1 step 1, §21.2 F6

**A local reader that reads only the trailer and the directory: must it verify
the front signature block?** The document gives two answers that decide
accept/reject differently on the same bytes.

§6.1 sets up the test as *not* transport-based:

> "That distinction governs the request accounting of §6.4 and nothing else; the
> obligation over the front block turns on residency instead, because a
> transport can be classified either way at the margin while residency is
> decidable at any reader's own open path."

and then the next paragraph glosses residency with a transport as its first
item:

> "A reader whose open leaves bytes [0, 16) **resident** — a local file, a
> memory mapping, a speculative suffix window that reached offset 0, or any
> transport already holding them — and a content sniffer MUST verify the full
> block by byte equality before other processing, and MUST treat any mismatch as
> reject-file. A reader that would have to issue a further range request to
> obtain those bytes MAY defer or omit the check"

"a local file" is a transport, not a residency condition. A memory mapping does
leave [0, 16) resident; a `pread`-only local open does not. Under the gloss,
every local reader is resident and MUST check. Under the second sentence, a
`pread`-only local reader "would have to issue a further range request" — §6.1
itself uses "range" generically for local transports, defining a local reader as
"one whose transport serves any byte range at no per-range round trip" — and MAY
omit.

The two restatements split the same way. §19.1 step 1 drops "a local file" from
the gloss entirely:

> "A reader whose open leaves bytes [0, 16) resident — a speculative suffix
> window that reached offset 0 included — MUST verify the front signature block
> by byte equality before other processing (mismatch: reject-file); one that
> would have to issue a further range request for them MAY defer or omit the
> check (`[R-CNT-04]`)."

while §21.2 F6 uses the weaker verb "fetch":

> "the obligation binds a reader holding those bytes resident, and a reader that
> would have to fetch them MAY defer or omit the check (`[R-CNT-04]`)"

and Appendix A asserts the strong reading as fact:

> "A local reader additionally verifies bytes [0, 16) by equality first, which
> `[R-CNT-04]` requires of any reader holding them"

**Readings I can defend.** (a) *Transport-inclusive*: "a local file" is
enumerated, so any reader on a local file has the bytes resident by definition
and MUST verify. Appendix A assumes this. (b) *Literal residency*: residency
means bytes the open actually left in hand; "a local file" is shorthand for the
ordinary local case where a reader slurps or maps, and a `pread`-only reader is
exempt under the same escape §19.1 and F6 both restate. §19.1 — the section an
implementer builds the open path from — omits the item that forces (a), and its
own framing sentence ("The test is residency, not transport") disowns it.

**What I picked.** (a), because the gloss is normative text inside
`[R-CNT-04]` and Appendix A confirms it; my reader checks [0, 16) on any local
open. But I picked it on the balance of three sentences that do not agree, not
because the document decided it.

**What an implementer does wrong without it.** Ships a local reader that accepts
a file whose front signature block is damaged and whose trailer, directory and
tiles are intact — and fails the F6 conformance vectors, which §24 requires to
exist at both instances (magic bytes [0,8); reserved bytes [8,16)) with expected
verdict reject-file.

**Byte-level: yes.** Reader A (local, `pread`-only, reading §6.1's gloss) and
Reader B (local, `pread`-only, reading §19.1 and F6) are handed a file whose
byte 0 is `0x88` instead of `0x89` and which is otherwise a conforming file.
A returns reject-file. B opens the file, walks the directory, and serves every
sample. Opposite verdicts on one byte, and both implementations can point at
normative text. §21.1's "where a row and the rule it cites diverge, the rule
governs" does not settle it, because the divergence is *inside* the rule: its
first sentence and its second sentence classify the same reader differently.

---

### reader-02 — OBSERVATION — §20.5 `[R-WRT-06]`, `[R-WRT-07]` vs §16

**Must a compactor honour a declared alignment or slab it carries forward?**
§20.2 and §20.3 both say so for their tiers. §20.5 does not, and instead grants
placement freedom bounded only by §5.2:

> "A compactor preserves content but not placement — placement is not among the
> things it carries forward, and it is free to place structures anywhere §5.2
> admits"

§5.2 is byte coverage: its content is disjointness and the partition into
classes. It admits placements that violate `[R-SLB-01]`'s "every stored tile's
offset satisfies offset mod A = 0" and `[R-SLB-03]`'s run packing. §20.5 never
cites §16, while its two sibling subsections do — §20.2: "every declared layout
invariant (`[R-SLB-01]`, `[R-SLB-03]`)"; §20.3 step 4: "a slab declaration is
re-established or cleared (`[R-SLB-04]`), and an aligned layer's new tiles
satisfy its invariant or the declaration is cleared".

**The text does decide it**, which is why this is an OBSERVATION rather than an
ambiguity — but deciding it costs four separate passages. `[R-WRT-06]`: "Given a
conforming input the output is a conforming file." `[R-WRT-01]`: a compactor
"satisf[ies] every writer requirement for the bytes [it] produce[s]". A file
declaring A with a misaligned stored tile exhibits L40 (verifier, reject-layer),
so it is not conforming. Therefore the compactor must re-establish the
invariants. And it cannot take `[R-SLB-04]`'s escape of clearing the
declaration: that rule binds "a writer or updater whose commit supersedes a
stored tile in, or grows the extents of, a slab-declared layer", and a compactor
performs a whole-file rewrite rather than a commit; more decisively,
`[R-WRT-07]` enumerates exhaustively what may differ from `[R-WRT-05]`'s
byte-identical re-emission — "relocation re-points extent slots, regenerates
each relocated tile-index region ..., and updates the layer-record fields
covering a regenerated region (crc_of_crc_array)" — and A, S and A_slab are not
in that list.

**What an implementer does wrong without it.** Writes a compactor that packs the
output densely, emits a file whose layer still declares A = 4096 with tiles at
arbitrary offsets, and produces a nonconforming file from a conforming input —
the exact thing `[R-WRT-06]` forbids. One added clause in §20.5 ("and honours
every alignment and slab declaration it carries forward") would close it.

**Byte-level: no.** `[R-WRT-06]`'s "Given a conforming input the output is a
conforming file" is unconditional and sits two sentences earlier in the same
requirement, and L40/L41/L42 make the consequence explicit. A competent
implementation reaches the right answer; it just has to assemble it.

---

### reader-03 — AMBIGUITY — Appendix G, item 3

The reproducible-writer profile's whole claim is that it "closes the degrees of
freedom this format deliberately leaves open". Item 3 does not close the one it
names.

> "**A total emission order, contiguously.** For each layer in ascending
> layer-name byte order: its stored tiles in disk-ordinal order, then its
> tile-index region; then any record extents in ascending record order; then the
> directory. Records are ordered by type, and within type 0x0001 by layer name;
> a layer record's sub-records are ordered by type, and within a type by their
> encoded bytes compared lexicographically"

Two things are open.

**(i) The loop's extent.** The colon opens a per-layer list, but "then the
directory" is plainly not per-layer (there is one directory). So either the loop
body is {tiles, index} and record extents come after all layers, or it is
{tiles, index, that layer's record extents} — in which case the file-scope
user-metadata extent has no stated position at all.

**(ii) "ascending record order" for type-0x0002 extents.** The tie-break given
is "within type 0x0001 by layer name". Type 0x0002 has no tie-break, and a file
can carry several type-0x0002 *extents* at once: at most one at file scope
(`[R-CNT-14]`) plus at most one per layer record. Nothing orders the file-scope
document's extent against the layers' sub-record documents' extents. The
sub-record ordering rule given ("by their encoded bytes compared
lexicographically") governs sub-record placement *within a layer record's inline
payload*, not the placement of their extents in the file.

**Readings.** (a) loop = {tiles, index}; all record extents follow, ordered
file-scope-first then by layer name. (b) loop = {tiles, index, that layer's
sub-record extents}; the file-scope extent goes last, before the directory. (c)
as (b) with the file-scope extent first. Each is consistent with the sentence.

**What I picked.** (a) with file-scope first, because "then any record extents"
reads most naturally as a phase after the per-layer phase, and because item 3's
own justification — "an order a reader can derive, which a creation order is
not" — favours a rule stated over the whole file.

**What an implementer does wrong without it.** Two writers both claiming profile
conformance emit different byte sequences for the same logical content on any
file carrying both a file-scope and a layer-scope user-metadata document, which
is precisely the failure the profile exists to prevent. Appendix G's closing
paragraph lists the four freedoms it adds and does not list this one, so it does
not know it is open.

**Byte-level: no.** Appendix G is explicitly non-normative and "adds no
requirement to any actor: a writer ignoring it is fully conforming." Every
output under every reading is a conforming file.

---

### reader-04 — AMBIGUITY — Appendix G, item 2

> "**`file_id` from a cryptographic hash of the file's own emitted bytes**,
> computed over [0, F − 64) together with the trailer's other fields with the
> `file_id` field taken as zero, then written in. Deterministic, and
> high-entropy"

Three things a second implementer cannot reconstruct:

1. **Which hash.** None is named. Items 1 and 9 of the same list close their
   freedoms precisely by naming the producer — "a named codec implementation at
   a named version with fixed encoder settings", "a named JSON writer at a named
   version" — and item 2 conspicuously does not.
2. **How 64 bits are taken from it.** Every cryptographic hash is wider than the
   `u64` file_id field. Leading eight bytes, trailing eight, big- or
   little-endian folding — all unstated.
3. **The exact byte string hashed.** "[0, F − 64) together with the trailer's
   other fields with the `file_id` field taken as zero" leaves open whether the
   trailer contribution is bytes [0, 48) ∪ [56, 60) concatenated, or the whole
   64-byte trailer with [48, 56) zeroed and [60, 64) excluded (the CRC cannot be
   an input, since it depends on file_id), and in which order the two parts are
   concatenated.

A fourth, minor: §6.2 requires file_id ≠ 0, and the item states no fallback for
the 2⁻⁶⁴ case.

**What I picked.** SHA-256 over [0, F − 64) ‖ trailer[0, 48) ‖ trailer[56, 60),
first eight bytes read little-endian, incremented on a zero result. That is a
guess; nothing in the text prefers it.

**What an implementer does wrong without it.** Believes it has implemented the
profile and produces a file that differs from another profile implementation's
in eight bytes of the trailer and four of the CRC — the profile's exact failure
mode, and the one it can only refute rather than confirm ("conformance to the
profile can be refuted cheaply but confirmed only by reproducing the file").

**Byte-level: no.** Non-normative; every choice yields a conforming file.

---

### reader-05 — CONTRADICTION — §18.4 `[R-MTA-07]` vs §21.3 L48 / §21.2 F27 / Appendix H

§18.4 justifies leaving standardized-key placement and shape advisory by
asserting that verifiers do no work on metadata content, and cites §21.7 for it:

> "No reader's behavior turns on either, since a reader ignores such a key and
> reads the rest of the document — and enforcing them would put a verifier to
> work on the content of metadata, which §21.7 excludes by design."

But the register assigns a verifier exactly that work, twice:

> "| L48 | A layer sub-record's user-metadata document has object members not in
> ascending order of their keys' UTF-8 bytes; the document stays readable and
> readers process it unchanged | — | verifier | certification | `[R-MTA-05]`
> (R-CNF-05) |"

with F27 the file-scope twin, and Appendix H's verifier checklist lists
"user-metadata member ordering (`[R-MTA-05]`, §18.2)" among "the checks readers
are exempt from". Establishing L48 requires decoding the extent, decompressing
it under encoding 2, parsing the JSON, and comparing decoded keys' UTF-8 bytes
at every nesting depth — the deepest excursion into metadata content anywhere in
the document.

The citation is wrong on its own terms as well. §21.7 says nothing about
metadata. Its subject is sample content — "A writer that emits well-formed
structures carrying wrong sample values — a mis-strided filter (`[R-COD-10]`),
an undisclosed compression dictionary (`[R-COD-06]`), or simply wrong data" —
and its stated ground for omission is that "no file-level witness exists to
check". A standardized key in the wrong scope *has* a file-level witness; it is
omitted from the register because §21.6 declares it a non-violation, not because
it is undetectable.

**Readings.** (a) "the content of metadata" means the *semantic* content (values
and their shapes) as distinct from serialization order, so member ordering is
not a counterexample. (b) It means what it says, and the sentence is simply
false as written. I lean (a) as the intent and (b) as the text.

**What I picked.** The normative half of `[R-MTA-07]` is unambiguous — "Neither
placement nor value shape bears on validity: the file stays conforming" — and
§21.6 registers it as a defined non-violation. My reader ignores an out-of-scope
or wrong-shaped standardized key and reads the rest of the document, and my
verifier does not check placement or shape but does check member ordering.

**What an implementer does wrong without it.** Writes a verifier that skips
`[R-MTA-05]`'s ordering check on the strength of §18.4's sentence, and certifies
files F27/L48 make nonconforming.

**Byte-level: no.** The reader-side and file-validity consequences are both
stated flatly elsewhere and agree; only the rationale sentence and its citation
are wrong.

---

### reader-06 — OBSERVATION — §20.4 and Appendix H's updater checklist

Both places summarise the preservation rule more narrowly than the rule itself.
§20.4:

> "No commit therefore removes a layer record or a file-scope user-metadata
> record."

Appendix H:

> "never removes a layer record or a file-scope user-metadata record (§20.4)"

The governing sentence two paragraphs above is broader:

> "For a type §7.3 registers, the registry's fixed flags govern rather than the
> stored ones (`[R-CNT-22]`) — both registered types carry PE = 1, so neither
> can be dropped, and implementing a record's type confers understanding of it,
> not permission to drop it."

Type 0x0002 is one type whether it appears top-level or as a layer sub-record,
so a **layer's** user-metadata sub-record is equally undroppable. Neither
summary says so, and §20.4's supporting argument for the narrow sentence — "an
in-place removal would strand that layer's stored tiles and index region as
slack" — is an argument about layer records only, so it does not extend the
statement by implication either. The one place that gets it right is §20.4's
MU = 0/PE = 0 table row, which is about types the updater does *not* implement
and so does not reach registered type 0x0002 at all.

**What an implementer does wrong without it.** Builds an updater from Appendix
H's checklist — which is where an implementer auditing its own work goes — and
drops a layer's user-metadata sub-record in a commit that touches that layer,
silently losing application state that `[R-CNT-22]` and `[R-WRT-05]` oblige it
to carry forward. The loss produces a perfectly conforming *file*, so nothing
downstream catches it.

**Byte-level: no.** The governing sentence decides it, and both summaries are
true statements that are merely incomplete rather than contradictory.

---

### reader-07 — OBSERVATION — §20.5 `[R-WRT-07]`

`[R-WRT-07]` conditions index regeneration on the *region* having moved:

> "except that relocation re-points extent slots, regenerates each relocated
> tile-index region (entry offsets new; entry lengths, entry crcs, and sentinel
> entries unchanged; segment CRCs recomputed over the entries as re-emitted),
> and updates the layer-record fields covering a regenerated region
> (crc_of_crc_array)"

The condition that actually forces regeneration is that the *entries' offsets*
change, which happens whenever the layer's stored tiles move — regardless of
where the region itself lands. A compactor that repacks a layer's tiles but
happens to place that layer's index region at the same byte offset it occupied
in the input is, on the literal text, not required to regenerate it, and would
emit a region whose entries address the input's tile offsets.

That output is caught by the closing sentence of the same requirement — "The
output's reference arrays MUST equal the live generation's bit for bit
(`[R-MDL-02]`): compaction changes where bytes live, never what a layer
denotes" — and in practice a compactor emitting from offset 0 relocates
everything. So no competent implementation gets this wrong. But the trigger is
stated on the wrong quantity, and a reader building a state machine from this
sentence has to notice that for itself.

**Byte-level: no.** `[R-MDL-02]` and the closing sentence decide it.

---

## 7. What I checked and found sound

Recording these because a walk that reports only defects hides how much of the
document held up.

- **Every register row cross-reference resolves to the row its sentence claims.**
  I checked all of them: §9.6's "F8 and F17"; §17.2's "(§21.4, T24)"; §21.1's
  "F1 of F6 and of F8, F35 of F36, L24 of L25" and "T24's *any codec*", "(T15,
  T25)"; F33's "F9/F10, F31/F32, L16/L17 and T8/T9"; §21.6's "(F36, L25)" and
  "(F35, F36, L24, L25)" and "(F18)"; Appendix H's "(§21.5)... F7" and "F36,
  L25"; §16.2's note pointing at §21.3 (L41, L42); §7.4's note pointing at §21.3
  (L26); T13's "the check that detects it is T25's"; T26's "T2's or T4's". Given
  the brief's warning about a wholesale re-labelling, this was where I expected
  to find something. Nothing is stale.
- **The chain of trust is airtight against `[R-ENC-05]`.** entry_count and the
  layer record's extent_offset are covered by the directory CRC, verified at
  open, so computing the CRC-array and segment ranges from them is legal;
  crc_of_crc_array is likewise directory-covered; it certifies the array; the
  array certifies the segment; the segment certifies the entry; the entry's crc
  certifies the tile. Every I/O I issue is sized from a field whose covering
  checksum has already verified. I could not find a link where I would have to
  act on unverified bytes.
- **The quarantine boundary is drawn identically in all three places** it
  appears (§7.1 `[R-CNT-25]`, §18.1 `[R-MTA-02]`, §19.1/§19.3's framing lists):
  slot, extent_length ≥ 5 and inline_length == 1 precede the document and take
  the containing scope; everything from the encoding byte inward is
  ignore-record. R1–R10 and F21–F23 / L10–L12 partition exactly along that line.
- **§18.2's encoding-2 constraint carry-over is exact.** Six constraints survive
  ("the frame magic; no skippable frame and no second frame; no nonzero
  dictionary ID; no content-checksum flag", plus occupying the extent's bytes
  before the terminal CRC), the two that reference a tile's declared decoded
  size are explicitly dropped, and R4's instance cell enumerates exactly
  6 × 2 containers = 12.
- **The deflate trailing-bits question is closed.** "two files differing only in
  those bits decode to the same tile image and are both conforming ... A whole
  byte after the one holding the final bit does trail the stream, and
  `[R-COD-08]` rejects it (§21.4, T24)." That is the exact boundary I would have
  had to guess at, and it is stated.
- **The zstd window derivation question is closed** by the note after
  `[R-COD-06]`: with Single_Segment_Flag the Window_Size is the content size,
  which must equal the decoded size; without it the Window_Descriptor cannot go
  below 1 KiB, so a sub-1-KiB tile is single-segment-only. I confirmed the
  consequence: §14.2's 18- and 30-byte and §14.3's 2-byte examples are all
  below 1 KiB.
- **§8.1's coverage map is complete** for format major 1: the only record types
  are layer (extent = index region, covered by the segment/crc_of_crc_array
  chain) and user metadata (extent covered by its own terminal CRC), plus the
  unassigned-type extent the map deliberately covers by nothing. §4.5's
  three-way split of checksum fields — terminal, interior, none — matches the
  map row for row.
- **The register's completeness claim survives a sweep.** I walked every
  `[R-...]` identifier looking for a MUST-level, file-witnessed, detectable
  condition with no row, and found none. Every omission I could name is
  accounted for: `[R-SLB-04]` (§16.2's note), nesting depth (§7.4's note),
  post-commit residue (§9.5's note), "belongs to no class" (§5.2's note), and
  the seven in §21.7. `[R-MTA-06]` and `[R-MTA-07]` are declared non-violations
  in §21.6 rather than omitted.
- **§21.6's non-violation table is consistent with every rule it restates**, and
  its closing paragraphs correctly identify the two conforming-file-refused
  cases that §2.3 calls "the other two".
- **The instance-counting discipline is coherent.** §21.1's rule that a single
  predicate over several fields is one instance is honoured: F10, F25, F32 read
  "—", while F3 and L2 enumerate genuinely different sums, and L46 enumerates
  containers rather than the two flag bits.

## 8. Confidence

An implementation built from this document alone would interoperate on every
path I walked, with one exception: whether a `pread`-only local reader rejects a
file with a damaged front signature block (reader-01). That single question can
put two conforming-looking readers on opposite sides of an accept/reject verdict
for a file whose only defect is in bytes [0, 16). Everything else I had to
decide, I could decide from the text — sometimes by assembling three or four
passages, which is what reader-02, reader-06 and reader-07 record.
