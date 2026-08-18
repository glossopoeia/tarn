# Cleanroom round 10 — Verifier implementer transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,919 lines). I opened no other file in the repository — no `docs/`, no ADRs, no
`PLAN.md`, `AGENTS.md`, `README.md`, no `conformance/`, no `spec/registry.json`,
no git history, no web access. I did not list any directory to discover what else
exists.

I ran three kinds of local computation, all of which read no repository file
except the spec:

1. A pure-Python CRC-32C implementation (Castagnoli reflected polynomial
   `0x82F63B78`, init `0xFFFFFFFF`, final XOR `0xFFFFFFFF`), used to reproduce
   every checksum constant the document states, and to re-check the hex dump in
   Appendix A. Script written to my own scratchpad.
2. A parser over `spec/tarn.md` that extracts the §21.2–§21.5 register rows and
   counts rows, instances (semicolon-separated, a cell reading `—` counting as
   one), and checks the Detector/Detected columns for internal consistency.
3. `grep` over the same file to enumerate every cross-reference to a register row
   label, and to enumerate the taxonomy-class cells.

Everything below is derived from that file plus arithmetic.

---

## 1. What I built

A conforming verifier, on paper. I worked in this order, because that is the
order the document forces:

- fix the checksum primitive and reproduce every stated constant, since nothing
  else can be checked before the CRC is right;
- write the certification procedure as an ordered algorithm with the three-verdict
  vocabulary of `[R-CNF-11]`;
- construct a concrete conforming file and run the coverage walk on it, then run
  it again on a walk that is blocked;
- construct an adversarial layout that exercises overlap, alignment and slab
  invariants simultaneously;
- enumerate the checksum obligations and ask whether every live structure is
  covered;
- enumerate the decoded-content obligations and ask what a verifier may skip;
- run a four-generation trace (create, append, update, compact) and state the
  verdict at each generation.

---

## 2. The checksum primitive, and which constants I reproduced

§4.5 `[R-ENC-09]`:

> The checksum used throughout this specification is CRC-32C: the 32-bit cyclic
> redundancy check with the Castagnoli polynomial 0x1EDC6F41 (RFC 3720 §12.1),
> reflected input and output, initial value 0xFFFFFFFF, and final XOR
> 0xFFFFFFFF, stored as a little-endian `u32`.

That is enough to implement without ambiguity. The reflected form of `0x1EDC6F41`
is `0x82F63B78`; I built the table-driven right-shifting variant.

**Constants I reproduced (all four exact):**

| Constant | Document | Computed | Where |
|---|---|---|---|
| CRC-32C(`"123456789"`) | `0xE3069283` | `0xE3069283` | §4.5, App. B |
| CRC-32C(zero bytes) | `0x00000000` | `0x00000000` | §4.5, §7.1, App. A |
| CRC-32C of a full all-sentinel segment (2¹⁶ × `FF ×16 00 ×4`) | `0xEECB3BB2` | `0xEECB3BB2` | §15.4 `[R-IDX-05]`, App. B |
| Appendix A trailer CRC over bytes [0,60) | `0xE00938D2` (stored `D2 38 09 E0`) | `0xE00938D2` | App. A |

The Appendix A hex dump is 128 bytes exactly, the directory at [16,20) is
`00 00 00 00` which is CRC-32C of zero bytes, and every annotated field in the
table under the dump matches the bytes. `committed_file_length = 0x80 = 128 =`
the file length, `128 mod 64 = 0`, `dir_offset = 16 ≥ 16`, `dir_length = 4 ≥ 4`,
`16 + 4 = 20 ≤ 128 − 64 = 64`, `generation = 1`, `file_id ≠ 0`, reserved zero.
Appendix A is a conforming file and my verifier certifies it. Slack = 128 − (16 +
4 + 64) = 44 bytes, exactly the pre-trailer pad [20,64) the annotation names.

**Constants I could not reproduce locally**, and why:

- `0xFD2FB528` / bytes `28 B5 2F FD` (zstd frame magic, §17.2): an external
  format's constant. I can only confirm the byte order is the little-endian
  spelling the document claims, which it is.
- `0x7E000000` (lz4 decoded-tile cap, §17.2 `[R-COD-07]`): an external
  interoperability bound, not derivable.
- The front signature block and trailer magic: arbitrary chosen constants. I
  confirmed the property §6.2's note claims — `0x89` vs `0x8A` in the first byte
  — so a backward recovery scan for the trailer magic can never match the front
  block. That is a real check and it holds.
- bfloat16 `0x3F80` for 1.0: verified by hand against binary32 `0x3F800000`
  under `[R-TYP-02]`'s "high 16 bits" identification. Correct.

I also re-derived every worked numeric example that bears on a verifier's
arithmetic, all correct:

- §11.2/§11.4: grid (4,8), N=32, P=65,536; (300,700) → tile (1,2), s = 1·8+2 = 10;
  in-tile (44,188) → 44·256+188 = 11,452; planar channel 2 → 2·32+10 = 74.
- §14.2: interleaved, T=(2,3), P=6, channels uint8+uint16 → Q=3, decoded size 18,
  ordinal 5 at [15,18). Planar `b` → 12 bytes, ordinal 5 at [10,12).
  float32+bool → Q=5, decoded 30, ordinal 5 at [25,30).
- §14.3: planar bool, P=10, alternating → `55 01`; with fill true, `55 FD`
  (pad bits 2–7 set). Correct under LSB-first packing.
- §14.5: extents (5,5), tiles (4,4), edge tile (1,1) → 16 positions, 1 real, 15
  padding; one uint16 channel → 32 bytes, values 1–15 each `CD AB`.
- §15.4: entry_count = 1,000,000 → 16 segments (15 full + 16,960), 64-byte CRC
  array, region 20,000,064 bytes; entry 999,999 at segment-relative 339,180;
  CRC array at [20,000,000, 20,000,064); segment 15 at [19,660,800, 20,000,000).
- §15.4 second example: planar C=4, N=32, channel 2 at s=10 → ordinal 74, entry
  bytes [1,480, 1,500); channel 3 entries 96–127.
- §17.3 shuffle: 1.0/2.0/3.0 float32, s=4, n=3 → `00 00 00 00 00 00 80 00 40 3F
  40 40`. Correct under "byte i of group j at offset i·n + j".
- §20.3: 32-tile index re-emission = 32·20 + 4 = 644 bytes.
- §21.9's note: 2³² entries → 2¹⁶ segments × 4 = 256 KiB; 2³⁶ → 4 MiB. Correct.

Everything a verifier needs to compute, this document lets me compute.

---

## 3. The certification procedure

### 3.1 Verdict vocabulary

§2.3 `[R-CNF-11]` gives me three verdicts and two report-only annotations. I
transcribed the rules into a decision function before writing any check, because
the priority order is what makes the procedure deterministic:

> A verifier reports one of three verdicts: *conforming*, *nonconforming*, or
> *cannot establish* — the last where some requirement is one it is unable to
> check on a capability or resource ground […] An established violation takes
> priority: a verifier that has established any violation reports *nonconforming*,
> however many requirements it was unable to check, and *cannot establish* is
> available only to a traversal that established no violation.

So, with `V` = set of established violations and `U` = set of requirements it was
unable to check on a capability or resource ground:

```
if V ≠ ∅            → nonconforming
else if U ≠ ∅       → cannot establish        (MUST NOT certify)
else                → conforming              (certify)
```

Two report-only annotations, neither of which moves the verdict:

- **per-requirement unchecked report.** MUST be emitted "whichever of the three
  verdicts it reports", naming the requirement and the ground. Note this is
  vacuous in the *conforming* branch, since `U = ∅` there; it bites only for
  *nonconforming* and *cannot establish*.
- **unexamined scopes.** Only for a verifier that exercised the stop-at-first-
  violation licence. "*Unexamined* is neither a verdict nor *cannot establish* —
  it constrains the report, not the verdict."

SHOULD deviations are advisories and do not bar certification, per `[R-CNF-12]`:
"§21's register enumerates MUST-level conditions only, and a verifier reports a
SHOULD deviation as an advisory that does not bar certification." So my verifier
carries a fourth output channel, `advisories`, for `[R-CNT-03]` (unzeroed gaps),
`[R-CNT-09]` (discovery window), `[R-CNT-26]` (version_minor floor),
`[R-TYP-10]` (fill default), `[R-ENC-14]` (NFC names), `[R-LIF-07]`
(checkpoint commits), `[R-COD-06]`'s window-size SHOULD, `[R-MTA-04]`'s
number-exactness SHOULD, `[R-MTA-06]`/`[R-MTA-07]`'s key guidance, and
`[R-CNT-10]`'s transport fallback. None of these bars certification.

**Where `cannot establish` is available.** §2.3 enumerates five grounds. I
checked each for reachability by a verifier that is itself a *conforming reader*
(which §2.3 requires: "Verifiers and updaters are readers of the files they
process and inherit every reader obligation"):

| Ground | Reachable by a conforming verifier? |
|---|---|
| unimplemented format major | Yes. `[R-CNT-07]` + §21.6's first structural case. |
| record with MU = 1 and an unimplemented type | Yes, but only for an **experimental**-range type — §2.3 says so itself ("in a conforming file such a type is necessarily from the experimental range, since a reserved-range type carrying MU = 1 is itself a violation"). A reserved-range MU = 1 type is F35/L24, i.e. *nonconforming*. |
| cannot execute a codec or filter (`[R-COD-11]`) | **No.** All four codecs and both filters are core (`[R-COD-03]`, `[R-COD-09]`, `[R-CNF-03]`), so a conforming verifier can run every assigned value, and an unassigned value is L43/L45 — a violation, not a capability gap. `[R-COD-11]` says exactly this: "software unable to execute an assigned codec or filter is not a conforming reader". |
| declines a layer's or tile's decode on resource grounds | Yes, via `[R-ERR-04]`, when a declaration exceeds §21.9's guarantee. |
| declines to decode a user-metadata document (`[R-MTA-09]`) | Yes, via the size bound. **Whether it also covers an unassigned encoding is finding verifier-02.** |

That table is the useful shape of `cannot establish`: for a verifier that is a
conforming reader, only three of the five grounds are live, and two of those three
are resource declines. That was worth working out, because it means a verifier
that (a) implements major 1, (b) implements no record type beyond 0x0001/0x0002,
and (c) sets its resource bounds at or above §21.9's guarantees, reaches
`cannot establish` for exactly one reason: an experimental-range record type
carrying MU = 1.

### 3.2 The ordered algorithm

Each step names its input, the rows it can establish, and what it does when the
step cannot be run. Rows in **bold** are verifier-only (`Detector = verifier`).

**Step 0 — physical size.** Obtain the transport-authoritative size (`[R-CNT-10]`).
Cannot be obtained → the open fails; this is not a verdict about the file, it is
a failure to read it. If size < 128 → **F5**, `[R-CNT-27]`.

**Step 1 — front block.** Fetch [0,16) and compare by equality. §2.3 obliges the
verifier to check "every file-level requirement — including those ordinary
readers are exempted from", so the conditional exemption `[R-CNT-04]` grants a
remote reader does not reach a verifier: it fetches. Rows: F1 (byte-reversed
front constant), F6.

**Step 2 — trailer, in §6.2's fixed order.** Magic (F8, F1's trailer instance);
trailer CRC over [0,60) (F14); version gate (F18 for major 0, *cannot establish*
for an unimplemented major). Then, gates passed, all of: flags incompat lane
(F19); `committed_file_length` = physical size (F17) and multiple of 64 (F13);
`dir_offset ≥ 16` (F9); `dir_length ≥ 4` (F16); `dir_offset + dir_length ≤ F − 64`
(F10); `1 ≤ generation ≤ 2⁶³ − 1` (F11, and F2's generation instance); `file_id ≠ 0`
(F12); reserved [56,60) zero (F15). Domain and overflow: F2, F3.

Note the ordering constraint is real and I honoured it: `[R-CNT-06]` says only
magic, CRC and version gate "touch fields whose positions are fixed across all
majors (`[R-CNT-24]`)". A verifier that read `dir_offset` before the version gate
would be reading a field whose position a future major may redefine.

**Step 3 — directory region.** Fetch [dir_offset, dir_offset + dir_length),
verify the terminal CRC over the preceding `dir_length − 4` bytes before any
other use (F20). Failure is reject-file and stops everything downstream: nothing
in the record sequence may be acted on.

**Step 4 — record walk (top level).** Parse §7.2 framing with no residue (F29);
type 0 (F24); multiplicity (F34); extent slots of non-layer top-level records
(F30, F31, F32); user-metadata framing (F21, F22, F23); MU gate for unknown
types (F35); **F25** (MU=1/PE=0), **F26** (reserved flag bits 2–15), **F28**
(registered type's stored flags vs §7.3), **F36** (reserved-range type whatever
its MU bit). Build the layer-name namespace over raw name bytes; F4 for
duplicates. §19.1's rule that a layer record whose name field does not lie within
its `inline_length` "contributes no name to the namespace" is load-bearing and I
implemented it literally: such a record is excluded from the duplicate test and
raised as L23 at layer scope instead.

**Step 5 — per layer, full record validation** (§19.3 `[R-RDR-03]`): L1–L36,
L39, L43, L44, L45, plus **L46**, **L47**, **L49**, **L18**'s inputs. All
decidable from the resident directory and F, with no fetch. `[R-CNT-16]`'s
mutual exclusion (L20) and `[R-CNT-17]`'s two cross-checks (L21, L22) live here.

**Step 6 — per layer, index chain.** Fetch the tile-index region; verify
`crc_of_crc_array` over the segment CRC array (L37), then every segment CRC
(L38). A verifier verifies *every* segment, not only the segments covering
entries it wants — it has no "wants". Failure is reject-layer and blocks step 7
for that layer.

**Step 7 — per entry, classification** (§15.3 `[R-IDX-03]`): T6, T7, T8, T9, T10,
T11, T12. Six of these rows are the *structural* rows §15.3 marks; an entry
caught by one "contributes no stored extent" downstream.

**Step 8 — per stored tile, payload.** Fetch [offset, offset+length), verify the
entry's crc (T1). Codec-1 length equality (T14) is checkable *before* the fetch
and I do it there.

**Step 9 — per stored tile, decode.** Codec then inverse filter: T15, T16, T17,
T18, T19, T20, T21, T22, T23, T24, T25, then T3 (decoded length exactly the
declaration-derived decoded size). T13 is recorded here but, as the row itself
says, "the check that detects it is T25's".

**Step 10 — per stored tile, decoded content.** **T2** (interleaved bool byte at
a real position), **T4** (padding positions carry fill), **T5** (packed-plane pad
bits carry the fill bit). **T26** is recorded here, its check being T2's or T4's.

**Step 11 — per user-metadata extent.** Terminal CRC (R2); decode under the
declared encoding (R1 for encoding 0 or reserved 3–0x7F; R3 for decode failure;
R4 for the frame constraints); document content (R5–R10); and **F27**/**L48**
for member ordering.

**Step 12 — whole-file structural checks.** These need the whole directory and
cannot be done incrementally: **F33** (cross-scope overlap), **L18** (intra-layer
overlap), **F7** (a structure in the pre-trailer gap), **L40** (alignment),
**L41**/**L42** (slab), and the `[R-LIF-08]` coverage walk with the slack total.

**Step 13 — verdict.** Apply §3.1's decision function.

Two things about ordering that the document does settle and that I would
otherwise have got wrong:

- Step 12's checks are all verifier-only, and every one of them requires the
  outputs of steps 5–7 for *every* layer. So a verifier that exercises
  `[R-CNF-11]`'s stop-at-first-violation licence forfeits the coverage walk
  entirely, and `[R-CNT-21]` requires it to say so. The licence and the slack
  total are in tension by design; §22.3 says so plainly: "the distinguishing
  figure comes from a walk that completes."
- `[R-ENC-05]` bars acting on any integer before the checksum covering it
  verifies. So step 7 cannot classify an entry before step 6 verified its
  segment, and step 8 cannot fetch before step 7 classified. This is the chain
  of §8.2 and it is strictly ordered.

---

## 4. The coverage walk on a concrete file

### 4.1 Construction

I built the smallest file that exercises every claimant class. Layer `a`:
interleaved, rank 1, dimension `x` with E = 4, T = 2, one channel `v` of uint8
with fill `0x00`, linearization 1, codec 1 (none), filter 1 (none), A = 0, S = 0,
A_slab = 0.

Geometry: G = ⌈4/2⌉ = 2, N = 2, P = ∏Tᵢ = 2, addressed-tile count = N = 2
(interleaved). Q = ΣBᵢ = 1. Decoded size = P · Q = 2 bytes. Under codec 1
`[R-COD-04]` forces stored length = 2.

Layer-record inline payload, packed in §7.4's table order with no padding:

```
name         u8 len + 1 byte              2
layout       u8                           1
linearization u16                         2
codec        u16                          2
filter       u16                          2
alignment A  u64                          8
slab S       u64                          8
A_slab       u64                          8
rank d       u8                           1
channels C   u16                          2
1 dim entry  (1+1) + 8 + 8               18
1 chan entry (1+1) + 2 + (1+1)            6
index_encoding u8                         1
entry_count  u64                          8
crc_of_crc_array u32                      4
sub-records                               0
                                        ----
                                          73
```

Record = 24-byte header + 73 = 97 bytes. Directory = 97 + 4 (terminal CRC) = 101.
Index region under `[R-CNT-17]`: 2 × 20 + ⌈2/2¹⁶⌉ × 4 = 44 bytes.

**Generation 1 layout (F = 256):**

| Range | Bytes | Claimant |
|---|---|---|
| [0,16) | 16 | front signature block |
| [16,18) | 2 | layer `a` tile 0, stored extent |
| [18,20) | 2 | layer `a` tile 1, stored extent |
| [20,64) | 44 | layer `a` record extent = tile-index region |
| [64,165) | 101 | directory |
| [165,192) | 27 | — (pre-trailer pad) |
| [192,256) | 64 | trailer |

Gates: `dir_offset = 64 ≥ 16` ✓; `dir_length = 101 ≥ 4` ✓; `64 + 101 = 165 ≤
256 − 64 = 192` ✓; `F = 256`, `256 mod 64 = 0` ✓; `F ≥ 128` ✓.

### 4.2 The partition, and the slack total

`[R-LIF-08]` tells me exactly what enters the walk:

> From the live trailer it enumerates the live directory and its records and
> their sub-records, each record's extent, and the non-sentinel entries of each
> layer's tile-index region […] The front signature block at [0, 16) and the live
> trailer at [F − 64, F) are claimed by the walk as well.

One parse I had to settle: "the live directory and its records and their
sub-records, each record's extent". Read as making the *records themselves*
claimants, every conforming file would immediately fail, since a record's bytes
lie inside the directory region and would overlap it. So the claimant list is:
the directory (one claimant covering the whole region), each record's and
sub-record's extent, each non-sentinel entry's stored extent, the front block,
and the trailer. Records and sub-records are what the walk traverses, not what it
claims. §5.2's class list confirms it — the classes are "the front signature
block; or a **structure** — a stored-tile extent, a record extent […], the
directory, or the trailer", and a record is not among them. Cheap to decide, so
not a finding, but it is the first thing an implementer meets.

Also settled by the text and worth stating: "A layer record's extent slot
addresses that layer's tile-index region (§7.4), so the region enters the walk
once, as that record's extent, and is not a second claimant beside it." Without
that sentence I would have double-claimed every index region and reported every
file as overlapping.

**Claimed** = 16 + 2 + 2 + 44 + 101 + 64 = **229 bytes**.
**F** = 256. **Slack total = 256 − 229 = 27 bytes**, exactly [165,192), the
pre-trailer pad.

**Can a byte be neither?** No, and the document proves it rather than asserting
it. §5.2's Note:

> The live committed state is *defined* as the front block plus what a complete
> coverage walk reaches, and `[R-LIF-08]` makes every byte that walk misses
> slack — so "belongs to no class" describes nothing, and a register row for it
> would be a row no file could exhibit.

So the partition of [0, F) is total by construction, and the only testable half
of `[R-CNT-02]` is disjointness. That is right, and the reasoning is sound: the
walk's reach *defines* the live state, so unreached ⟹ slack.

**But "certified" and "claimed" are not the same set**, and this is the one place
where the answer to my charter's question is genuinely interesting. Partition the
claimed bytes by whether any checksum covers them (§8.1):

| Claimed bytes | Covered by | Certified? |
|---|---|---|
| front block [0,16) | nothing — byte equality | Yes, by equality |
| trailer [F−64, F−4) | trailer CRC | Yes |
| trailer CRC field [F−4, F) | nothing (terminal) | By comparison only |
| directory [dir_offset, end−4) | directory terminal CRC | Yes |
| directory CRC field (final 4) | nothing (terminal) | By comparison only |
| tile-index entry array | its segment CRC | Yes |
| segment CRC array | `crc_of_crc_array` | Yes |
| stored-tile extent | that entry's `crc` | Yes |
| user-metadata extent, less final 4 | that extent's terminal CRC | Yes |
| user-metadata extent final 4 | nothing (terminal) | By comparison only |
| **extent of a record of an unassigned type** | **nothing** | **No** |

So the honest answer is: a byte can be **claimed but uncertified**. The extent of
a record of a type this specification has not assigned is inside the live
committed state — it is claimed, so it is *not* counted in the slack total — and
§8.1's map covers it by no checksum at all, and §7.2 leaves its content opaque.
It is subject only to bounds (`[R-CNT-13]`) and disjointness (F33/L18). §22.3
`[R-SEC-04]` says this out loud and I read it as confirming rather than as
correcting me:

> The extent of a record of a type this specification has not assigned is covered
> by no checksum either (§8.1), so corruption inside it is equally invisible.

So the tri-partition my charter asked for is really a four-way one:

1. **certified** — checked against a checksum §8.1 maps, or against a constant;
2. **claimed but uncertified** — unassigned-type record extents; bounded and
   disjoint, content unconstrained, *not* in the slack total;
3. **counted but unconstrained** — slack;
4. **neither** — empty, by §5.2's Note.

A verifier that reports only "slack = N" therefore understates the unexamined
surface, because class 2 is invisible in that number. The document does not
require reporting class 2 separately. I chose to report it anyway, since
`[R-CNF-11]` obliges me to report requirements I was unable to check and there is
no requirement here to be unable to check — so it is an advisory, not a
`cannot establish` ground. §21.7's principle governs: "no file-level witness
exists to check, so nothing about the file is left undetermined and the verdict
is unaffected."

### 4.3 A walk that does not complete

Same trace, at generation 3 (see §7 below, F = 896, complete-walk slack = 522).
Now posit that layer `b`'s `crc_of_crc_array` does not match the stored segment
CRC array — row **L37**, reader-detected, reject-layer.

The walk is now blocked exactly where `[R-LIF-08]` says it can be: "a scope-level
rejection blocks enumeration". `b`'s entries cannot be trusted, so `b`'s two
stored-tile extents are not enumerated and are not claimants.

Complete-walk claimants at generation 3 totalled 374 bytes; without `b`'s two
2-byte tiles that drops to 370, so the naive unclaimed count rises from 522 to
**526**.

Here is where I had to guess, and it is finding **verifier-01**. `[R-CNT-21]`:

> A partial total counts only the bytes no claimant claims within the regions the
> verifier did walk, and a verifier reporting one MUST also name the regions it
> did not walk and report their byte extent.

Nothing defines "region". Three readings I can defend:

(i) **Region = the structure whose claimants could not be enumerated.** Here that
is `b`'s tile-index region, [260,304), 44 bytes. "Regions walked" is then
everything else, so the partial total is 526 and the named unwalked region is
[260,304) with byte extent 44. This over-counts by 4: `b`'s live tiles at
[256,260) are reported as slack although they are live.

(ii) **Region = the byte ranges whose claimancy the verifier actually resolved.**
Then `b`'s tiles sit in an unwalked region — but the verifier cannot name that
region, because its extent is precisely what the untrusted index would have told
it. The obligation to "report their byte extent" is unsatisfiable.

(iii) **Region = the whole footprint of the rejected scope.** Same problem as
(ii), and worse: layer `b`'s footprint is not a contiguous range in general.

I implemented (i), because it is the only reading under which the two obligations
in the sentence — report a number, and name unwalked regions with a byte extent —
are both dischargeable. I record the 4-byte over-count in the report. §5.2's Note
licenses that: "A partial total (`[R-CNT-21]`) reports what one verifier's
incomplete walk left unclaimed, which is a fact about that run and not about the
file's live state."

The stop-at-first-violation case is sharper still. Suppose the verifier stops at
**F26** (a reserved flag bit set on the third top-level record). At that point it
has claimed only the front block [0,16), the directory [622,820) and the trailer
[832,896) — 278 bytes — so the partial total is 896 − 278 = **618**. What are
"the regions it did not walk", and what byte extent do they have? It never read
the remaining records' extent slots, so it cannot name a single byte range. Under
reading (i) the answer is "the record sequence from record 3 onward", whose byte
extent within the directory it *can* give — but the regions those records
*address* are exactly what it cannot name. I report the un-walked record range's
extent and note that the extents it addresses are unnameable. That discharges the
letter of the sentence and not its evident intent.

None of this moves a verdict: a partial total is a report field, and
certification is barred by violations alone (`[R-CNF-12]`). So finding
verifier-01 is not byte-level. But two conforming verifiers handed the same file
will print different slack numbers, and §22.3 makes that number operationally
load-bearing — "the number that distinguishes a working file from a padded one".

---

## 5. Extent overlap, alignment and slab, on one adversarial layout

Abstract statements of these three invariants are easy to nod at. I built one
file that violates all of them at once and checked that the register partitions
the damage the way the rules say.

**File W**, F = 6,592 (= 103 × 64). Five layers, all interleaved, all codec 1,
filter 1, linearization 1.

| Structure | Extent | Intended defect |
|---|---|---|
| front block | [0,16) | — |
| A tile 0 | [512,516) | A declares alignment A = 512; 512 mod 512 = 0 ✓ |
| A tile 1 | [1024,1028) | 1024 mod 512 = 0 ✓ |
| A tile 2 | [1500,1504) | 1500 mod 512 = 476 → **L40** |
| A index | [2048,2112) | 3 entries → 3·20 + 4 = 64 ✓ |
| B tile 0 | [3072,3074) | B declares S = 2, A_slab = 256; 3072 mod 256 = 0 ✓ |
| B tile 1 | [3074,3076) | packed: 3072 + 2 = 3074 ✓ |
| B tile 2 | [3300,3302) | run 1's first stored tile; 3300 mod 256 = 228 → **L42** |
| B tile 3 | [3400,3402) | 3300 + 2 = 3302 ≠ 3400 → **L41** |
| B index | [3500,3584) | 4 entries → 4·20 + 4 = 84 ✓ |
| C tile 0 | [1026,1028) | overlaps A tile 1 [1024,1028) → **F33** |
| C tile 1 | [4096,4098) | — |
| C index | [4200,4244) | 2 entries → 44 ✓ |
| D tile 0 | [4300,4308) | overlaps D's own index → **L18** |
| D index | [4304,4348) | 2 entries (entry 1 sentinel) → 44 |
| E tile 0 | [6510,6514) | lies wholly in the pre-trailer gap → **F7** |
| E index | [4400,4444) | 2 entries → 44 |
| directory | [6000,6500) | dir_offset 6000 ≥ 16; 6500 ≤ 6592 − 64 = 6528 ✓ |
| pre-trailer gap | [6500,6528) | 28 bytes |
| trailer | [6528,6592) | 6592 mod 64 = 0 ✓ |

What I confirmed by working it:

- **Alignment.** L40 fires per *entry*, but its outcome is reject-layer, not
  reject-tile. `[R-SLB-01]` puts it there ("violation: reject-layer, §15.3") and
  §15.3's last three rows agree. So one misaligned tile condemns layer A, not
  just that tile. That is not obvious from §16.1's prose alone and it matters:
  a verifier must not report L40 at tile scope.
- **Slab run partition.** `[R-SLB-02]`: runs are `[block_start + r·S, …)`, and for
  an interleaved layer the single block is [0, N). B has N = 4, S = 2, so runs are
  ordinals [0,2) and [2,4). L42 checks only the *first stored* tile of each run;
  L41 checks packing between consecutive stored tiles *within* a run. Between
  runs, `[R-SLB-05]` governs and nothing is checked — so B tile 2 at 3300 is not
  compared against B tile 1's end at 3076. I got this wrong on my first pass and
  had to re-read §16.2's "The runs themselves are not mutually ordered or joined".
- **Transparency.** §15.3 and `[R-SLB-03]` agree exactly on which entries a run's
  packing relation skips: sentinels, and entries §15.3 classifies reject-tile "on
  a *structural* ground". An entry whose only defect is a failed stored-bytes crc
  is **not** transparent — "its offset and length stand, and the packing relation
  reads them as it does any other stored tile's — so this invariant stays
  decidable from index bytes alone". I tested this: if I make B tile 2 a
  length-0 entry (T10, structural), run 1's first stored tile becomes B tile 3 at
  3400, 3400 mod 256 = 72, so L42 fires there instead — the row moves but does
  not vanish. If instead B tile 2 merely fails its crc (T1), it stays in the run
  and L42/L41 read its offsets. Both behaviours are exactly what the text says,
  and the distinction is load-bearing: it is what keeps the slab check decidable
  without fetching payload.
- **Overlap scope.** The split between L18 and F33 is a scope test, not a severity
  test. C tile 0 overlapping A tile 1 is cross-layer → **reject-file**. D tile 0
  overlapping D's own index is intra-layer → **reject-layer**. `[R-CNT-13]` says
  it and §15.3's last three rows restate it consistently. F33's parenthetical
  correctly routes bounds violations elsewhere: "a claimant reaching the front
  signature block or the live trailer is instead caught by the bounds rows F9/F10,
  F31/F32, L16/L17 and T8/T9, each at its own tier" — I checked all eight labels
  against the rows they name and every one lands correctly.
- **The pre-trailer gap.** E tile 0 at [6510,6514) is inside [6500,6528). It
  overlaps nothing. It satisfies T8 (offset ≥ 16) and T9 (6514 ≤ 6528). It is
  caught by **F7 alone**, `[R-CNT-05]`. This is the one check a verifier will
  forget, because it is the only structural rule that is not a bounds test or an
  overlap test. I would not have implemented it from §5.2 or §9.7; it exists only
  in §6.2's paragraph and in F7.

**Verdict on file W: nonconforming.** Established violations: F7, F33, L18, L40,
L41, L42. Unable-to-check: none. Slack total is computable but irrelevant to the
verdict; I still report it, since `[R-CNT-21]`'s obligation is unconditional and
the walk here does complete (every rejection is at a scope whose enumeration
already succeeded — none of these six blocks the index chain).

That last point is worth stating: an overlap or alignment violation does **not**
make the walk incomplete. `[R-LIF-08]` blocks only on "a scope-level rejection
[that] blocks enumeration" — and L18/L40/L41/L42 are *discovered by* enumeration,
so they cannot block it. Only L37/L38 (index chain), F20 (directory CRC), and the
trailer gates actually stop the walk.

---

## 6. Checksum and decoded-content obligations

### 6.1 Which structures are covered

§8.1's map is complete and I found no live structure it fails to place. §4.5's
statement of the exceptions is exact and matches the map:

> Every field of every structure is covered by exactly one checksum, excepting the
> front signature block (a constant whose check is equality, §6), the terminal
> checksum fields of §8.1's map — the trailer, directory-region, and
> user-metadata checksum fields — which are verified by comparison and covered by
> no further checksum, and the extent of a record of a type this specification
> has not assigned, which §8.1's map covers by no checksum at all.

Three terminal fields, one equality-checked constant, one uncovered class. The
three "interior" checksum fields — segment CRC array, each entry's `crc`, each
layer record's `crc_of_crc_array` — are each both compared and covered:
`crc_of_crc_array` by the directory CRC (it lives in the layer record's inline
payload), the segment CRC array by `crc_of_crc_array`, each entry's `crc` by its
segment CRC. I traced the whole chain on my concrete file and it closes.

So the answer to "is every live structure covered by a checksum" is **no, and
deliberately**: unassigned-type record extents are not, which is class 2 of §4.2
above.

### 6.2 What a verifier must decode

`[R-COD-11]` frames this as being about §14's content obligations:

> The decoded-content obligations of §14 (`[R-SER-05]`, `[R-SER-08]`) require
> decoding. A verifier that cannot execute a layer's codec or filter cannot
> establish that layer's conformance and MUST NOT certify the file.

But that understates it. Three *reader*-assigned rows also require a decode —
T3 (`[R-SER-07]`, decoded length ≠ decoded size), T24 and T25 (`[R-COD-08]`) —
and §2.3 makes a verifier a reader. So a verifier must decode **every stored tile
of every layer**, not only tiles in layers with padding positions or bool
channels. I checked whether any layer shape escapes: a layer with every Eᵢ a
multiple of Tᵢ has no padding positions, and with no bool channel it has no pad
bits and no T2 witness — but it still has T3, T24 and T25. Even codec 1 with
filter 1 needs the bytes read, since T14's pre-fetch equality does not establish
T3 for a filtered image.

**What it compares against.** Everything is declaration-derived, never
payload-derived. `[R-SER-07]`: "decoded size is a function of the layer's
declarations alone — geometry, layout, and channel types — never of payload
content". For each stored tile the verifier computes:

- interleaved: P · Q, with Q = Σ Bᵢ;
- planar numeric channel c: P · Bᶜ;
- planar bool: ⌈P/8⌉;

and compares the decode's output length to it. Padding positions are computed
from Gᵢ · Tᵢ > Eᵢ; for each such position and each channel it carries, the
verifier compares the encoded bytes to the recorded fill (T4), and for a packed
plane the fill bit; pad bits are bit positions P mod 8 .. 7 of the final byte
(T5). Interleaved bool bytes at real positions must be 0x00 or 0x01 (T2).

**What it is permitted to skip.** Only two things, and both cost it the
certificate:

- a decode declined on resource grounds (`[R-ERR-04]`) → the requirement goes to
  `U`, verdict *cannot establish* if `V = ∅`;
- a user-metadata document declined against its own bound (`[R-MTA-09]`) →
  likewise, and `[R-MTA-09]` adds a SHOULD to report the bound applied and the
  stored length declined.

It is permitted to skip nothing else. In particular §21.7 is explicit that
content-correctness failures are *not* skipped requirements: "None of these is a
requirement a verifier is *unable to check* within the meaning of `[R-CNF-11]`:
no file-level witness exists to check, so nothing about the file is left
undetermined and the verdict is unaffected." So a mis-strided filter that happens
to break no padding and no bool byte leaves the file *conforming*, not
*cannot establish*. That is a strong and correct statement and I implemented it
directly.

---

## 7. Multi-generation trace

One file, four steps, verified after each. Layer `a` as in §4.1; layer `b`
identical in shape (name `b`, dimension `y`, channel `w`), so each layer record is
97 bytes and a two-record directory is 198 bytes.

### Generation 1 — creation (`[R-WRT-02]`)

Layout as in §4.1. F = 256. Claimed 229, **slack 27**.
Trailer: generation 1, fresh nonzero `file_id = X`, `flags = 0`, `version_minor = 0`.
Both barriers of `[R-LIF-02]` steps 4 and 6 performed (unobservable to a verifier;
§21.7's history class).

**Verdict: conforming.** `U = ∅`, `V = ∅`. Slack total 27, walk complete.

### Generation 2 — append a new layer (`[R-WRT-04]`, shape (a) of §20.3)

Writing begins at exactly F = 256.

| Range | Bytes | Claimant |
|---|---|---|
| [0,16) | 16 | front block |
| [16,18) | 2 | `a` tile 0 |
| [18,20) | 2 | `a` tile 1 |
| [20,64) | 44 | `a` index (unmoved — `[R-WRT-05]`, extent slot carried byte-identically) |
| [64,192) | 128 | superseded gen-1 directory, pad, trailer |
| [256,258) | 2 | `b` tile 0 |
| [258,260) | 2 | `b` tile 1 |
| [260,304) | 44 | `b` index |
| [304,502) | 198 | directory (two records) |
| [502,512) | 10 | pad |
| [512,576) | 64 | trailer |

F = 576 (= 9 × 64). `304 + 198 = 502 ≤ 576 − 64 = 512` ✓.
Claimed = 16+2+2+44+2+2+44+198+64 = 374. **Slack = 576 − 374 = 202.**
Cross-check by naming the superseded runs: gen-1 dir 101 + gen-1 pad 27 + gen-1
trailer 64 + gen-2 pad 10 = 202 ✓.

`a`'s record is re-emitted byte-identically including its extent slot, so `a`'s
tiles and index never move — §5.2's figure and `[R-WRT-05]` both say so, and the
arithmetic confirms it: the whole cost of adding a layer is the new layer plus one
directory, never anything proportional to `a`'s data.

**Verdict: conforming.** Slack total 202.

### Generation 3 — update: supersede `a` tile 1 (shape (b))

| Range | Bytes | Claimant |
|---|---|---|
| [0,16) | 16 | front block |
| [16,18) | 2 | `a` tile 0 |
| [18,20) | 2 | *slack* — superseded `a` tile 1 |
| [20,64) | 44 | *slack* — superseded `a` index |
| [64,192) | 128 | *slack* — gen-1 dir/pad/trailer |
| [256,260) | 4 | `b` tiles |
| [260,304) | 44 | `b` index |
| [304,502) | 198 | *slack* — gen-2 directory |
| [502,512) | 10 | *slack* — gen-2 pad |
| [512,576) | 64 | *slack* — gen-2 trailer |
| [576,578) | 2 | `a` tile 1′ |
| [578,622) | 44 | `a` index′ (whole region re-emitted) |
| [622,820) | 198 | directory |
| [820,832) | 12 | *slack* — pad |
| [832,896) | 64 | trailer |

F = 896 (= 14 × 64). `622 + 198 = 820 ≤ 832` ✓.
Claimed = 16+2+4+44+2+44+198+64 = 374 — unchanged, as it must be: the live state
has the same shape.
**Slack = 896 − 374 = 522.** Itemised: 2 + 44 + 101 + 27 + 64 + 198 + 10 + 64 + 12
= 522 ✓.

Note `a`'s *whole* index region is re-emitted for a one-entry change — 44 bytes
here, 20 MB in §20.3's note's million-tile example — and the old one becomes
slack. Slack has now grown from 27 to 522 across two commits while the live state
stayed at 374 bytes. That is exactly the signal §22.3 says the slack total exists
to give an operator.

**Verdict: conforming.** Slack total 522. This is the generation on which §4.3's
partial-walk exercise is run.

### Generation 4 — compaction (`[R-WRT-06]`, `[R-WRT-07]`)

A new file, not a commit. Fresh `file_id = Y ≠ X`, generation 1. Placement is free
(`[R-WRT-07]`: "A compactor preserves content but not placement"); I use
Appendix G item 3's contiguous order.

| Range | Bytes | Claimant |
|---|---|---|
| [0,16) | 16 | front block |
| [16,18) | 2 | `a` tile 0 (bytes verbatim, entry crc unchanged) |
| [18,20) | 2 | `a` tile 1′ (bytes verbatim) |
| [20,64) | 44 | `a` index, **regenerated** — offsets new, lengths and crcs unchanged, segment CRC recomputed, `crc_of_crc_array` updated |
| [64,66) | 2 | `b` tile 0 |
| [66,68) | 2 | `b` tile 1 |
| [68,112) | 44 | `b` index, regenerated |
| [112,310) | 198 | directory (extent slots re-pointed) |
| [310,320) | 10 | pad |
| [320,384) | 64 | trailer |

F = 384 (= 6 × 64). `112 + 198 = 310 ≤ 320` ✓.
Claimed = 374. **Slack = 384 − 374 = 10** — the pre-trailer pad alone.

Reclaimed: 896 − 384 = 512 bytes. The reference arrays are bit-identical
(`[R-MDL-02]` via `[R-WRT-07]`), every stored tile's bytes and every entry's crc
survive unchanged, and only the offsets, the segment CRCs, the two
`crc_of_crc_array` fields and the two extent slots differ. `flags` copies the
input's unknown ignore-lane bits forward (there are none); `version_minor` is the
greater of `[R-CNT-26]`'s floor and the input's, i.e. 0.

**Verdict: conforming.** Slack total 10.

**Verification depth of the compactor itself.** `[R-WRT-09]` obliges it to verify
the open, each retained layer's record and full index chain, and every relocated
extent's checksum including every stored tile's entry crc — and §20.5 says its
depth "reaches no decoded content". So a compactor is a strictly weaker checker
than a verifier: T2, T3, T4, T5, T24, T25, T26 and the whole of §21.5 travel
through it untouched. I confirmed this is stated rather than inferred: "a
violation latent in a structure it carries forward verbatim travels into its
output (`[R-WRT-01]`)". A pipeline that compacts is therefore not a pipeline that
certifies, and §22.3's advice ("a pipeline accepting files from untrusted sources
SHOULD verify rather than merely read") extends to it.

**Certification results, all four generations:**

| Step | F | Live | Slack | Verdict |
|---|---|---|---|---|
| gen 1 (create) | 256 | 229 | 27 | conforming |
| gen 2 (append layer) | 576 | 374 | 202 | conforming |
| gen 3 (update tile) | 896 | 374 | 522 | conforming |
| gen 4 (compact) | 384 | 374 | 10 | conforming |

---

## 8. Mechanical audit of the register

The brief warned that §21.2 and §21.3 carry a wholesale re-labelling, so I
audited the tables mechanically rather than by eye.

**Row counts.** Parsed 121 rows: F1–F36 (36), L1–L49 (49), T1–T26 (26), R1–R10
(10). All four sequences are contiguous from 1 with no gaps and no duplicates.
The stated counts — §21.2 "36 conditions", §21.3 "49 conditions", §21.4 "26
conditions", §21.5 "10 conditions" — all match.

**Instance count.** Counting semicolon-separated entries, with a cell reading `—`
counting as one, per §21.1's mechanical rule: **248**. §21.8 states "121
conditions over 248 instances". Exact match. I spot-checked §21.1's own examples
against the cells: T24's cell reads "any codec" (one instance, a family without a
change of shape) ✓; T15 has two and T25 three (materially different shapes) ✓;
F25 and T12 read `—` because each is "a single predicate over several fields" ✓.

**Column consistency.** Every Detector cell is `reader` or `verifier`; every
Detected cell draws from {open, layer access, tile use, extent use,
certification}; every `verifier` row is detected at `certification` and no
`reader` row is. Zero anomalies. The twenty verifier rows are F7, F25, F26, F27,
F28, F33, F36, L18, L25, L40, L41, L42, L46, L47, L48, L49, T2, T4, T5, T26 —
which is exactly the set my step-12 and step-10 checks implement, plus F27/L48 in
step 11.

**Every cross-reference to a row label.** I enumerated all of them and checked
each against the row it lands on:

| Cited at | Labels | Lands correctly? |
|---|---|---|
| §9.6 `[R-LIF-06]` | F8, F17 | Yes — magic mismatch and size mismatch are exactly the two gates a torn tail fails |
| §17.2 note | T24 | Yes — trailing byte after a DEFLATE stream |
| §21.1 specialisations | F1 of F6 and F8; F35 of F36; L24 of L25 | Yes, all three; F1's two instances specialise F6 and F8 respectively |
| §21.1 instances | T24, T15, T25 | Yes |
| F33's cell | F9, F10, F31, F32, L16, L17, T8, T9 | Yes — all eight are the bounds rows for directory, top-level extents, layer/sub-record extents, and index entries |
| T2's cell | T4 | Yes — the padding-position case of the same byte |
| T13's cell | T25 | Yes |
| T26's cell | T2, T4 | Yes |
| §21.6 experimental-type row | F36, L25 | Yes |
| §21.6 closing | F18; F35, F36, L24, L25 | Yes |
| Appendix H verifier checklist | F7; F36, L25 | Yes |

No mis-landed citation. The re-labelling is clean.

**Governing-rule spot checks.** I compared roughly twenty rows against the text
of their governing requirement, concentrating on the ones a verifier acts on. All
agreed. Two that I expected to diverge and did not:

- L46/L47 place `[R-CNT-12]`'s flag violations at **layer** scope for a layer
  record, while §7.3's table gives a layer record's Scope as "file (container for
  layer scope)". §7.2 settles it explicitly — "the layer for a layer record and
  for sub-records, the file for other top-level records" — and F25/F26 are
  correspondingly restricted to "a **non-layer** top-level record". Consistent.
- T6 vs T11: an entry with offset = length = 2⁶⁴−1 and crc ≠ 0 is not a sentinel
  (§15.2 requires crc = 0) but must not also be caught as an out-of-domain value.
  T11's cell says "the value being distinct from the all-ones sentinel", and
  §15.2 says `[R-ENC-03]` and `[R-ENC-04]` "apply to the fields of non-sentinel
  entries only". The two rows partition cleanly. Same for T7 against T11.

---

## 9. Findings

### verifier-01 — AMBIGUITY — "region" is undefined, so a partial slack total is not a determined number

**Location.** §5.2, `[R-CNT-21]`; §9.7, `[R-LIF-08]`.

**Quotation** (§5.2, `[R-CNT-21]`):

> Where the walk of §9.7 does not enumerate every region's claimants — whether
> because a scope-level rejection stops it, or because the verifier elected under
> `[R-CNF-11]` to stop at the first violation — the verifier MUST report the
> total as partial. A partial total counts only the bytes no claimant claims
> within the regions the verifier did walk, and a verifier reporting one MUST
> also name the regions it did not walk and report their byte extent.

**Permitted readings.** "Region" is used nowhere else in a defined sense.
(i) region = the structure whose claimants could not be enumerated (here, a
layer's tile-index region); (ii) region = the byte ranges whose claimancy the
verifier actually resolved; (iii) region = the whole byte footprint of the
rejected scope. Worked on the generation-3 file (F = 896, complete-walk slack
522) with layer `b`'s `crc_of_crc_array` failing (L37): reading (i) gives a
partial total of **526** and names [260,304) (44 bytes) as unwalked, over-counting
`b`'s two live 2-byte tiles as slack; readings (ii) and (iii) cannot name a byte
extent at all, because the extent is exactly what the untrusted index would have
supplied. In the stop-at-first-violation case the gap is worse: after stopping at
F26 the verifier has claimed 278 bytes and reports 618, but it has no byte range
whatever to name for the extents it never read.

**Which I picked and why.** Reading (i), because it is the only one under which
both obligations in the sentence are dischargeable. I report the over-count
explicitly. §5.2's Note licenses this: a partial total "is a fact about that run
and not about the file's live state".

**What an implementer does wrong without it.** Two verifiers report different
slack totals for the same file and neither is wrong. §22.3 makes that number the
operator's signal — "the number that distinguishes a working file from a padded
one" — and §20.3 says "compact (§20.5) when slack grows". A verifier under
reading (ii) will simply omit the mandated byte extent, silently violating
`[R-CNT-21]`'s second clause.

**Byte-level: no.** The slack total is a report field, never a verdict input.
Certification is barred by established violations alone (`[R-CNF-12]`), and every
file that triggers a partial total has, by construction, already established one
or has stopped early under an explicit licence. No byte a writer may emit and no
accept/reject verdict changes.

---

### verifier-02 — AMBIGUITY — an experimental-range user-metadata encoding leaves the verifier's verdict open between *conforming* and *cannot establish*

**Location.** §2.3 `[R-CNF-11]`; §18.2 `[R-MTA-09]`; §21.6's non-violations table;
§10.3 `[R-EXT-03]`.

**Quotations.** §2.3, listing the grounds for the third verdict:

> […] or when it declines to decode a user-metadata document (`[R-MTA-09]`).
> *Cannot establish* is not a finding that the file is nonconforming, and a
> verifier MUST NOT certify a file it reports that way.

§18.2 `[R-MTA-09]`:

> A **verifier** that declines to decode a document cannot establish that
> document's conformance and MUST NOT certify the file, exactly as `[R-COD-11]`
> requires of a codec it cannot execute […]

§21.6's table, for the same file:

> | A user-metadata record declares an experimental-range (≥ 0x80) document
> encoding | Ignored (ignore-record); the file is conforming — §10.3's
> prohibition binds a writer's conduct, not the bytes | `[R-MTA-03]`,
> `[R-EXT-03]`, `[R-CNF-02]` |

**The file.** Take my generation-1 file and add one top-level user-metadata
record: extent slot valid, `extent_length ≥ 5`, `inline_length = 1`, encoding byte
`0x80`, terminal extent CRC correct. Every framing rule (F21, F22, F23), the
extent CRC (R2), bounds and disjointness all pass. §10.2 puts `0x80` in the
experimental range of the metadata-encoding space; §21.6 states the file is
conforming. No register row applies. The verifier cannot decode the document —
this specification assigns `0x80` no meaning.

**Permitted readings.**

*Reading A — certify.* `[R-MTA-04]` and `[R-MTA-05]` bind "the decoded document".
Under an unassigned encoding this specification defines no decoding, so there is
no decoded document, so those requirements have no witness and are not
"requirements the verifier was unable to check". §21.7's principle applies: "no
file-level witness exists to check, so nothing about the file is left
undetermined and the verdict is unaffected." The parallel with record types is
strong: §8.1 explicitly places the extent of a record of an unassigned type under
"none — the bytes are opaque", and no one suggests such a record forces *cannot
establish*. And `[R-COD-11]`'s parallel is stronger still: for the *codec* space,
an unassigned value is not a capability gap at all — the verifier "rejects the
layer". Verdict: **conforming**, certificate issued.

*Reading B — cannot establish.* §2.3's own enumeration names "declines to decode
a user-metadata document", and `[R-MTA-09]`'s sentence is unconditional on its
face: a verifier that does not decode a document "cannot establish that document's
conformance and MUST NOT certify the file". This verifier does not decode this
document. Therefore it must not certify. Verdict: **cannot establish**,
certificate withheld, with `[R-MTA-09]`'s SHOULD-report of the declined extent's
stored length. §21.6's "the file is conforming" is a statement about the bytes,
not about what a verifier may report — the document already has two cases where a
conforming file draws *cannot establish* (§21.6's closing two structural cases),
so "the file is conforming" does not by itself entail "the verifier certifies".

**Which I picked and why.** Reading A. Three things push me there: (1)
`[R-MTA-09]`'s whole paragraph is about the size bound, and "declines" reads as a
choice, which an unassigned encoding is not; (2) `[R-MTA-03]`'s derivation — "Both
assigned encodings are core […] An encoding a reader does not implement is
therefore one this specification does not assign, and is ignore-record" — closes
the capability gap for every assigned encoding, so no *capability* ground remains;
(3) §8.1 closes the exactly-parallel case for unassigned record-type extents
explicitly. But I had to assemble those three passages to get there, and no single
sentence says it.

**What an implementer does wrong without it.** It issues, or withholds, a
certificate on a file the document calls conforming.

**Byte-level: yes.** Two conforming verifiers, both conforming readers, both
implementing major 1 and nothing beyond §7.3's two record types, handed the same
byte sequence. Verifier A prints *conforming* and certifies. Verifier B prints
*cannot establish* and MUST NOT certify. The verdict is the verifier's entire
output and the two differ on it, on bytes the document elsewhere calls conforming.
This is not a register row disagreeing with its rule — §21.1's tie-breaker
("where a row and the rule it cites diverge, the rule governs") does not reach it,
because §21.6's row cites `[R-MTA-03]`/`[R-EXT-03]`/`[R-CNF-02]`, none of which
speaks to certification, while the competing text is §2.3's own enumeration of
when the third verdict is available. There is no rule that decides between them.

*If triage prefers to treat a certification verdict as not "accept/reject", note
that the underlying gap is the same either way: §2.3's cannot-establish grounds
and §21.6's conforming-file rows overlap in exactly one place and the document
does not say which wins there. The smallest fix is one clause in §21.6's row, or
one clause in `[R-MTA-09]` scoping "declines" to the resource bound.*

---

### verifier-03 — OBSERVATION — `[R-ENC-06]` names an invalidity that appears in neither the register nor §21.7's account of what escapes it

**Location.** §4.2 `[R-ENC-06]`; §21.1's completeness clause; §21.7 `[R-ERR-01]`.

**Quotation** (§4.2):

> No field's width is ever a writer choice: every field's width is fixed by this
> specification, and a structure whose fields appear at any other width is
> invalid at its owning scope. `[R-ENC-06]`

**Detail.** §21.1 makes the register's completeness normative and names §21.7 as
the account of the exceptions:

> Its **completeness is normative** — a *detectable* file-conformance violation
> this specification names and the register omits is a defect in this document,
> detectability being the gate `[R-CNF-07]` already applies and §21.7 the
> account, by class, of what fails it

§21.7's second paragraph is a closed list of four: `[R-LIF-01]`, `[R-LIF-03]`,
the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]`, and `[R-CNT-13]`'s
no-embedded-offsets prohibition. `[R-ENC-06]` is not among them, and I found no
register row citing it as a governing rule — I checked all 121 Governing-rule
cells. §19.3 nonetheless cites it as one of the checks a reader performs at layer
access: "the fixed field widths and u64 value domain of §4 (`[R-ENC-06]`,
`[R-ENC-03]`)".

I worked out why no row exists, and I believe the register is right and the
account is what is short: a byte string is a byte string, and a writer that emitted
`rank d` as a `u16` produces bytes a conforming reader parses at the specified
widths, yielding either an ordinary violation of some other row (L23, L32, L21…)
or a perfectly conforming file that means something else. The writer's intent is
not recoverable, so there is no witness. That places `[R-ENC-06]` squarely in
§21.7's second class, where it is not listed. The alternative reading — that
`[R-ENC-06]` names no independent condition at all, being a restatement of every
layout table — is also defensible, and would mean nothing is missing.

**What an implementer does wrong without it.** Nothing at the byte level; but an
implementer auditing the register for completeness (which §21.1 invites, and which
§24's corpus obligation rests on) finds a MUST-level "is invalid at its owning
scope" with no row and no exemption, and must reconstruct the witness argument
from scratch. I did.

**Byte-level: no.** No file exhibits a witness of the violation, so no
implementation can accept or reject differently on account of it. §21.7's own
words settle the verdict consequence for exactly this class: "no file-level
witness exists to check, so nothing about the file is left undetermined and the
verdict is unaffected."

---

### verifier-04 — AMBIGUITY — Appendix G's zeroing requirement may not reach the pre-trailer pad, which would leave the reproducible profile unable to fix the file's bytes

**Location.** Appendix G, item 3 and its closing paragraph; §5.2 `[R-CNT-03]`;
§6.2 `[R-CNT-05]`.

**Quotation** (Appendix G item 3):

> Each structure begins where the previous one ended, save where a declared
> alignment forces a gap, and every byte of such a gap is zero — `[R-CNT-03]`'s
> advice, taken as a requirement here: order alone does not fix bytes while the
> space between structures is free in either extent or content.

**Permitted readings.** "such a gap" is anaphoric to "a gap [a] declared
alignment forces".

*Reading A (narrow).* Only alignment-forced gaps are zeroed. The pre-trailer pad
is not alignment-forced — it is forced by the trailer's 64-byte placement, and
under item 5 the profile may declare no alignment at all — so its content is
unconstrained. On my generation-1 file that leaves 27 bytes free, and on the
compacted file 10 bytes free, so two writers following the profile emit
byte-different files for identical input. The profile fails its own stated purpose
("Applications that need byte-identical output"), and item 2's `file_id`-as-hash
becomes non-deterministic too, since the hash is "computed over [0, F − 64)",
which contains the pad.

*Reading B (broad).* "such a gap" means every gap the emission leaves, the
pre-trailer pad included. This is what the appendix's closing paragraph implies:
"Four things are not, and the items above are where the profile adds them: gap
*content*, which `[R-CNT-03]` only advises" — and `[R-CNT-03]`'s scope is "the run
before an aligned tile or slab run, **and the pre-trailer pad**". If the profile
adds gap content as `[R-CNT-03]` scopes it, the pad is in.

**Which I picked and why.** Reading B. It is the only one under which item 3
achieves what the appendix says it achieves, and the closing paragraph's appeal to
`[R-CNT-03]` supplies the wider scope. Item 3's own phrasing does not.

Note the pad's *extent* is not at issue: `[R-LIF-02]` step 5 pads to the next
64-byte boundary, and although §6.2 says "a longer gap is conforming, and no
conforming commit produces one", a profile writer is a conforming committer, so
the extent is determined. Only the content is.

**What an implementer does wrong without it.** Two adopters of the profile
produce different bytes for the same logical input and different `file_id`s,
which is precisely the failure the profile exists to prevent. A verifier is
unaffected — I raise it because a verifier is the tool asked to confirm profile
conformance, and Appendix G says such conformance "can be refuted cheaply but
confirmed only by reproducing the file"; under reading A it cannot be refuted
either, since the differing bytes are permitted.

**Byte-level: no.** Appendix G is labelled non-normative and states "It adds no
requirement to any actor: a writer ignoring it is fully conforming." Both files
are conforming TARN files under either reading, and no reader's accept/reject
verdict changes. The fork is in *profile* conformance only.

---

## 10. Where the document was sufficient, and where I guessed

Sufficient, and I want to record it because it is the larger part of the walk:

- Every checksum I could compute reproduced exactly, including the all-sentinel
  segment constant, which is the one that would silently break a sparse-layer
  verifier.
- The three-verdict priority order is stated unambiguously and needed no
  interpretation.
- The transparency rule for structurally-invalid entries (§15.3, `[R-SLB-03]`,
  `[R-LIF-08]`) is stated three times, in three sections, with the same content
  each time — including the harder half, that a crc-failing entry is *not*
  transparent. That is the single most easily botched invariant in the document
  and it is nailed down.
- The scope split between L18 and F33 is decided by rule, restated by table, and
  its interaction with the bounds rows is spelled out in F33's own cell.
- The coverage walk's definition is circular in exactly the right way — live
  state is what the walk reaches, unreached is slack — and §5.2's Note proves the
  "belongs to no class" case is empty rather than asserting it.
- The register is arithmetically clean: 121 rows, 248 instances, contiguous
  numbering, consistent Detector/Detected columns, and every one of the twenty-odd
  cross-references to a row label lands on the row its sentence claims.

I guessed four times, and all four are above: the meaning of "region" in a partial
slack total (verifier-01); whether an unassigned metadata encoding forces
*cannot establish* (verifier-02); whether `[R-ENC-06]`'s absence from both the
register and §21.7 is intended (verifier-03); and the scope of Appendix G's
zeroing requirement (verifier-04). I also had to resolve, more cheaply, whether
records themselves are coverage-walk claimants (they are not — §4.2 above), and
whether a layer name is semantic or descriptive under §4.7 (I classified names
semantic; nothing observable turns on it, since the only operative clause for
descriptive fields is "a reader MUST NOT alter decoding based on it", which is
true of names under either classification).

Confidence that an implementation built from this text alone would interoperate
with another: **high**, with the single reservation of verifier-02.
