# Cleanroom round 15 — Verifier implementer transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,227 lines), in five sequential `Read` calls covering lines 1–4227 with no gaps.
I ran `wc -l` on that file, and three Python scripts of my own authorship in the
scratchpad (`crc.py`, `crc2.py`, `build.py`, `adv.py`) plus two inline `python3 -
<<EOF` heredocs. Two of those inline scripts opened `spec/tarn.md` to parse the
§21 register tables mechanically (row counting, instance counting,
detector/detection-point cross-check) — that is the same permitted file. Nothing
else was opened. I did not read `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`,
`AGENTS.md`, `README.md`, `conformance/`, `spec/registry.json`, or the output
directory. I ran no `git` command, no web search, no web fetch. I did not list
any directory.

---

## 0. What I built

A conforming verifier, on paper but concretely: the ordered certification
procedure, the coverage walk with real arithmetic on files I constructed
byte-for-byte, the extent/alignment/slab invariants exercised on adversarial
layouts, the checksum obligations with every locally-computable constant
reproduced, the decode obligations, and a four-generation trace
(create → append → supersede → compact) with a verdict at each step.

I worked from §2.3, §5.2, §6.2, §7.2, §8, §9.7, §15.3, §16, §17.4, §18.2,
§19.1–§19.4, §20.3–§20.5, §21, and Appendix H, and I checked the register
mechanically against its own stated totals.

---

## 1. Checksum constants — every one I could compute, reproduced

I implemented CRC-32C from §4.5's parameters alone (Castagnoli 0x1EDC6F41,
reflected in and out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF, stored
little-endian) — no library, no reference implementation.

| Constant | Where stated | Computed | Match |
|---|---|---|---|
| CRC-32C(`"123456789"`) = `0xE3069283` | §4.5, App. B | `0xe3069283` | ✅ |
| CRC-32C(zero bytes) = `0x00000000` | §4.5, §7.1, App. A | `0x0` | ✅ |
| CRC over 80 bytes of 4 sentinel entries = `0x80A34955` | §7.4 worked example | `0x80a34955` | ✅ |
| crc_of_crc_array over `55 49 A3 80` = `0xC4EE982E` | §7.4 worked example | `0xc4ee982e` | ✅ |
| CRC of a full 2¹⁶-entry all-sentinel segment = `0xEECB3BB2` | §15.4, App. B | `0xeecb3bb2` | ✅ |
| Appendix A trailer CRC = `0xE00938D2` (bytes `D2 38 09 E0`) | App. A | `0xe00938d2` | ✅ |

All six reproduce. The §7.4 pair is the strongest evidence that the layer-record
worked example is internally consistent: I built the 20-byte sentinel
(`FF ×16 00 ×4`, §15.2), concatenated four of them, CRC'd the 80 bytes, stored
the result little-endian, and CRC'd *that* 4-byte array — and got both stated
values without adjusting anything.

**Constants I could not reproduce, and why.** The zstd frame magic `28 B5 2F FD`
(§17.2) and the LZ4 block format bound `0x7E000000` (§17.2) are external
citations, not derivable here. The lz4 revision pin (App. F, "as published with
lz4 release v1.9.4") is an external artifact. Appendix G item 2's `file_id`
derivation names no hash function ("the hash a named function at a named
version"), so it is deliberately not computable — that is the profile's design,
not a gap.

**Non-CRC constants I did verify arithmetically:**

- §5.1 / `[R-CNT-27]`: minimum conforming file = 128 bytes. From
  `dir_offset ≥ 16`, `dir_length ≥ 4`, `dir_offset + dir_length ≤ F − 64`,
  `F mod 64 = 0`: F ≥ 84, hence F ≥ 128. ✅
- §5.1's smallest-file example: front [0,16), directory [16,20), pad [20,64)
  = 44 bytes, trailer [64,128). ✅ (Coverage walk below confirms 44.)
- §15.4's 1,000,000-entry example: 16 segments (⌈10⁶/2¹⁶⌉ = 16), final segment
  covers 1,000,000 − 983,040 = 16,960 entries; region 10⁶·20 + 16·4 =
  20,000,064; tile 999,999 at segment-relative byte 20·16,959 = 339,180;
  segment 15 at [19,660,800, 20,000,000); CRC array at
  [20,000,000, 20,000,064). All ✅.
- §15.4's second example: planar C=4, N=32, channel 2 at s=10 → disk ordinal
  2·32+10 = 74, entry at [1,480, 1,500); channel 3's entries are ordinals
  96–127. ✅
- §11.4's example: (300,700) with T=(256,256), G=(4,8) → tile (1,2), s = 10,
  in-tile (44,188), in-tile ordinal 44·256+188 = 11,452; planar channel 2 →
  74. ✅
- §14.2's examples: interleaved (2,3) with uint8+uint16 → Q=3, size 18,
  ordinal 5 at [15,18); planar `b` 12 bytes, ordinal 5 at [10,12); float32+bool
  → Q=5, size 30, ordinal 5 at [25,30). All ✅.
- §14.5's example: extents (5,5), tiles (4,4) → grid 2×2, edge tile (1,1)
  covers 4–7 on both axes = 1 real + 15 padding; uint16 fill 0xABCD → 32 bytes,
  value 0 real, values 1–15 = `CD AB`. ✅
- §14.3's example: P=10 alternating → byte 0 = 0x55; byte 1 = 0x01 with fill
  false, 0xFD with fill true (pad bits 2–7 set: 0x01 | 0xFC = 0xFD). ✅
- §17.3's byte-shuffle example: I applied the rule "byte *i* of group *j* at
  offset *i·n + j*" to `00 00 80 3F 00 00 00 40 00 00 40 40` (s=4, n=3) and got
  `00 00 00 00 00 00 80 00 40 3F 40 40`. ✅
- §21.9's note arithmetic: 2³² entries → 2¹⁶ segments × 4 bytes = 256 KiB;
  2³⁶ → 4 MiB; one full segment = 65,536 × 20 = 1.25 MiB. All ✅.
- §7.4's `[R-CNT-17]` formula at the segment boundary: entry_count 65,536 →
  1,310,724; 65,537 → 1,310,748. ✅

---

## 2. The certification procedure, as an ordered algorithm

Verdict vocabulary (§2.3, `[R-CNF-11]`): **conforming**, **nonconforming**,
**cannot establish**. Two report-only channels sit beside them and constrain the
report, not the verdict: *unexamined* (scopes skipped after an early stop) and
the per-requirement "unable to check" report. Plus two more report obligations:
the slack total (`[R-CNT-21]`) and the `[R-MTA-10]` ignored-record report.

Availability, which I had to derive by composing §2.3's paragraph:

- **nonconforming** iff the traversal established ≥ 1 violation. This takes
  priority over everything: *"An established violation takes priority: a
  verifier that has established any violation reports nonconforming, however
  many requirements it was unable to check."*
- **cannot establish** iff no violation established **and** ≥ 1 requirement was
  unable to be checked on a capability or resource ground.
- **conforming** iff no violation established **and** no requirement unable to
  be checked. Note that a §21.6 defined non-violation does not bar this, and
  neither does a SHOULD deviation (`[R-CNF-12]`: *"a verifier reports a SHOULD
  deviation as an advisory that does not bar certification"*).

Because a verifier may only stop early *at a violation* (`[R-CNF-11]`),
*unexamined* implies *nonconforming*. That closes the vocabulary: there is no
state in which a verifier has examined nothing and owes a verdict other than by
a capability/resource ground. I checked this and it holds.

The capability/resource grounds (§2.3, and the rules it cites):

1. format major it does not implement (§6.3, `[R-CNT-07]`);
2. a record with MU = 1 whose type it does not implement (§21.6) — but see
   below;
3. cannot execute a layer's codec or filter (`[R-COD-11]`, §17.4);
4. declines a layer's or a tile's decode on resource grounds (`[R-ERR-04]`,
   `[R-SER-05]`, `[R-SER-08]`);
5. declines to decode a user-metadata document on its own bound
   (`[R-MTA-09]`).

On (2) I initially thought there was a conflict: a *reserved*-range type with
MU = 1 is F35 **and** F36, i.e. two established violations, which under §2.3
would demand *nonconforming*, not *cannot establish*. The priority rule
resolves it, and the "(§21.6)" citation points at the experimental-range case,
which is the one that is genuinely a conforming file a verifier cannot judge.
No finding.

Explicitly **not** a ground: a user-metadata record under an *unassigned*
encoding. `[R-MTA-10]`: *"A verifier meeting such a record in an otherwise
conforming file has no requirement it is unable to check — the record is not
among `[R-CNF-11]`'s cannot-establish grounds, and certification is
unaffected."* It must instead **report** the record: owning scope, encoding
value, stored extent length. Appendix H repeats the same three fields. ✅
consistent.

Also explicitly not a ground: the undetectable-content class of §21.7.
*"None of these is a requirement a verifier is unable to check within the
meaning of `[R-CNF-11]`: no file-level witness exists to check, so nothing about
the file is left undetermined and the verdict is unaffected."* This answered a
question I had queued (does an unwitnessable obligation force *cannot
establish*? No) and I was glad to find it stated.

### The ordered algorithm I implemented

**Tier 0 — physical.**
0.1 Obtain the transport-authoritative size F_phys (`[R-CNT-10]`). A verifier
     that cannot obtain one MUST probe or fail the open; it MUST NOT substitute
     committed_file_length.
0.2 F_phys < 128 → **F5** reject-file (`[R-CNT-27]`).

**Tier 1 — front block.** §19.1 step 1 and `[R-CNT-04]`: verify [0,16) by byte
equality *before other processing*. A verifier holds no residency exemption —
F6's row says so in terms (*"a verifier holds no such exemption (§2.3)"*) and
Appendix H repeats it. Failure → **F6**, and byte-reversal → **F1**. Both
reject-file. *(This tier's placement relative to Tier 2 is the subject of
finding **verifier-02**.)*

**Tier 2 — trailer, in §6.2's fixed order** (`[R-CNT-06]`), the order being
normative because only the first three touch cross-major-fixed positions:
2.1 magic at F−64 → **F8** (and **F1**'s trailer instance);
2.2 CRC-32C at [60,64) over [0,60) → **F14**;
2.3 version gate → **F18** if version_major = 0; an unimplemented major is a
     *capability* refusal → **cannot establish**, not a row (§21.6);
2.4 then, gates passed, all of: flag gates → **F19**; committed_file_length =
     F_phys → **F17**, and mod 64 = 0 → **F13**; dir_offset ≥ 16 → **F9**;
     dir_length ≥ 4 → **F16**; dir_offset + dir_length ≤ F − 64 → **F10**;
     1 ≤ generation → **F11**; file_id ≠ 0 → **F12**; reserved [56,60) zero →
     **F15**. Domain and sum checks **F2**/**F3** ride along
     (`[R-ENC-03]`, `[R-ENC-04]`).

If Tier 2 rejects before a live trailer is established, §5.2 is explicit that
**no slack total is owed at all**: *"there is no F and no live state to walk, so
the total is not owed at all: the verifier reports the trailer failure and
nothing about slack, which is not a partial total but the absence of one."*
That is a clean, well-drawn line and I implemented it exactly.

**Tier 3 — directory.** Fetch [dir_offset, dir_offset+dir_length); verify the
terminal CRC over the preceding dir_length − 4 bytes **before any other use** →
**F20**. If it fails, the record sequence is unparsable; the walk still owes a
*partial* total (see §4 below).

**Tier 4 — record walk (open tier).** Framing with no residue → **F29**; type 0
→ **F24**; multiplicity → **F34**; extent slots → **F30**/**F31**/**F32**;
unknown top-level type MU gate → **F35** (reserved range) / capability refusal
(experimental range); reserved-range type whatever its MU → **F36**; flag
checks → **F25**, **F26**, **F28**; user-metadata framing → **F21**, **F22**,
**F23**; layer-name namespace → **F4**, and layer-record name well-formedness
→ **L3**, **L5**, **L6** (layer scope, detected at *open* — I confirmed
mechanically that L3/L5/L6 are the only L-rows with detection point *open*,
which matches §19.1 step 4 exactly).

I noted §19.1 step 4's careful sequencing: uniqueness is decided *first*, over
raw bytes, *"whether or not each name is itself well-formed"*, and a record
whose name field does not lie within inline_length contributes no name and is
instead `[R-CNT-18]`. That is a genuinely subtle rule and it is stated without
gaps.

**Tier 5 — per layer (layer-access tier).** §19.3's enumeration: slot validity
(`[R-CNT-13]` → **L15**–**L17**), the §7.4 constraint set (`[R-CNT-23]` →
**L27**–**L31**, **L35**), mutual exclusion (`[R-CNT-16]` → **L20**), exact
parse and sub-record walk (`[R-CNT-18]` → **L13**, **L14**, **L23**, **L24**,
**L26**; sub-record multiplicity → **L19**), dimension/channel names
(**L4**, **L7**–**L9**), field widths and u64 domain (**L1**, **L2**), value
sets (**L31**, **L33**, **L34**, **L36**, **L43**, **L45**), fill constraints
(**L35**), the lz4 declaration bound (**L44**), the geometry floor and its
arithmetic (**L32**, and `[R-GEO-03]`'s products under **L2**), the alignment
value set (**L39**, **L29**), and the index cross-checks computable without I/O
(**L21**, **L22**). Plus verifier-only flag rows **L25**, **L46**, **L47**,
**L49**. §19.3 states *"All are decidable from the resident directory and F:
layer access performs no fetch"* — I checked every cited rule against that claim
and it holds; nothing in the list needs a byte outside the directory.

**Tier 6 — index chain (tile-use tier).** Fetch the CRC array and the segments;
verify crc_of_crc_array → **L37**, then each segment CRC → **L38**
(`[R-IDX-04]`, in dependency order). Note `[R-IDX-05]`'s bite: *"Equality with
the constant licenses nothing for readers: verification is byte comparison of
computed CRCs, never constant matching."* So the `0xEECB3BB2` shortcut is a
*writer's*; my verifier recomputes.

Then classify every entry per §15.3 → **T6**–**T12**, and the codec-1 length
cross-check **T14** (checkable before any payload fetch, per `[R-COD-04]`).

**Tier 7 — every stored tile.** §9.7 is unambiguous that a verifier does not
get to skip this: *"A verifier decodes every stored tile, whatever content
obligations §14 places on the layer: §21.4's codec rows are file-conformance
violations, and a verifier MUST NOT certify past a violation it has not looked
for."* So: fetch [offset, offset+length); verify entry crc → **T1**; decode
(codec then filter inverse) → **T15**–**T25**; decoded length exactly the
declaration-derived decoded size → **T3**; then the content obligations
→ **T4** (padding), **T5** (pad bits), **T2** (interleaved bool bytes), with
**T26** recorded as the cause where T2/T4 is the detector.

**Tier 8 — record extents (extent-use tier).** Terminal CRC → **R2**; decode
under the declared assigned encoding → **R3**, **R4**; document rules →
**R5**–**R10**; member ordering → **F27**/**L48**. Under an unassigned
encoding, stop after the CRC and file the `[R-MTA-10]` report. Under an
unassigned *record type*, §8.1 states no checksum at all — the extent is a
claimant of the walk, bounds- and disjointness-checked, and its content is
never inspected (§22.3, `[R-SEC-04]`).

**Tier 9 — the coverage walk (certification tier).** §9.7. Disjointness →
**F33**/**L18**; the pre-trailer gap → **F7**; alignment and slab invariants →
**L40**, **L41**, **L42**; then the slack total.

**Register cross-check.** I parsed all 121 rows out of §21.2–§21.5
mechanically. Row count 36 + 49 + 26 + 10 = **121**, matching each subsection's
stated count and §21.8's *"121 conditions over 273 instances"*. Instance count,
computed by splitting each Instances cell on semicolons and counting a cell of
`—` as one: **273** exactly (F 57, L 115, T 57, R 44). Detector/detection-point
consistency: every `verifier` row is `certification` and no `reader` row is;
20 verifier rows, 101 reader rows. Zero mismatches. I also spot-checked
§21.1's two stated axes against the rows that use them — T3/T14 (3 layouts × 2
magnitude directions = 6 each), T21/L44 (*exceeds*/*larger than* → one
direction × 3 layouts = 3 each), T22 (2 × 3 = 6), L21 (2 × 2 = 4), L30
(2 directions), F17 (2 directions), T24 (*any codec*, one instance as §21.1
names) — all consistent. The instance criterion is applied uniformly across
the register; I found no row that violates it.

I also cross-checked Appendix H's verifier checklist against the 20 verifier
rows: coverage/slack, overlap (F33/L18), flag bits (F25/F26/L46/L47 and
F28/L49), front block (F1/F6, named there because §2.3 removes the exemption),
pre-trailer gap (F7), reserved-range types (F36/L25), alignment and slab
(L40–L42), decoded content (T2/T4/T5, with T26 detected through them), member
ordering (F27/L48). Every verifier row is accounted for. ✅

---

## 3. The coverage walk on a concrete file, with arithmetic

I constructed a file byte-for-byte from the declarations alone.

**Layer `sst`** (§7.4's worked example's geometry, so the record layout is
pinned by the document): rank 1, dimension `x` with E = 100, T = 32; one
interleaved float32 channel `temp` with fill `0x7FC00000` (bytes
`00 00 C0 7F`); linearization 1, codec 1 (none), filter 1 (none), A = 0,
S = 0, A_slab = 0, index_encoding 1.

Derived: G = ⌈100/32⌉ = 4, N = 4, P = 32, Q = 4, decoded size P·Q = **128**,
entry_count = **4**, index region = 4·20 + ⌈4/2¹⁶⌉·4 = **84** bytes,
inline payload = **81** bytes (§7.4's own count), record = 24 + 81 = **105**,
directory region = 105 + 4 = **109**.

Under codec 1 every stored tile's index length MUST equal 128 (`[R-COD-04]`,
T14). Tile 3 is the edge tile: it covers x ∈ [96,128), so positions 96–99 are
real and 100–127 are **28 padding positions**, each of which `[R-SER-05]` fixes
to the recorded fill. I generated it that way and confirmed the T4 check passes,
then flipped one padding byte and confirmed T4 fires.

### Generation 1 — creation

```
[     0,    16)      16  front signature block
[    16,   144)     128  stored tile 0
[   144,   272)     128  stored tile 1
[   272,   356)      84  tile-index region  (layer record's extent)
[   356,   465)     109  directory region
[   465,   512)      47  pre-trailer pad          <- SLACK
[   512,   576)      64  live trailer
F = 576   (576 mod 64 = 0)   dir_offset+dir_length = 465 <= F-64 = 512
```

**Partition.** §5.2: *"Every byte of the live committed state belongs to
exactly one of: the front signature block; or a structure — a stored-tile
extent, a record extent ..., the directory, or the trailer."* Claimants:
16 + 128 + 128 + 84 + 109 + 64 = **529 bytes certified**. Disjointness verified
pairwise. **Slack = 576 − 529 = 47**, exactly the pre-trailer pad.

Note the walk claims the front block and the trailer, per §9.7: *"The front
signature block at [0, 16) and the live trailer at [F − 64, F) are claimed by
the walk as well, being members of the live committed state."* And the layer
record itself is *not* a claimant — §9.7: *"A record is not a claimant of its
own — its header and inline payload lie inside the directory region, which is
the claimant covering them."* Nor is the index region a second claimant beside
the layer record's extent. Both of those would have double-counted if I had
guessed; both are stated.

**Which bytes are certified, which are counted-but-unconstrained, whether any
byte is neither.**

- **Certified**: the 529 live-state bytes — but "certified" needs the three-way
  refinement §8.1 and §22.3 force. Of the 529, every byte is bounds- and
  disjointness-checked; content is checked for all but two classes: (a) the
  extent of a record of a type this specification has not assigned, which §8.1
  covers with *"none — the bytes are opaque (§7.2)"*, and (b) a user-metadata
  extent under an unassigned encoding, which its terminal CRC covers but no
  content rule constrains (`[R-MTA-10]`). §22.3's `[R-SEC-04]` names both:
  *"a certificate covers those bytes uninspected — which is why `[R-MTA-10]`
  makes the verifier's report name each such record."* Neither class appears
  in my file, but a verifier must be built for them.
- **Counted-but-unconstrained**: the 47 slack bytes. §5.2: *"Slack has no
  internal structure this specification defines, its content is unconstrained,
  and no conformance requirement applies to it."*
- **Neither**: impossible, and the document says why rather than leaving me to
  infer it. §5.2's Note: *"The live committed state is defined as the front
  block plus what a complete coverage walk reaches, and `[R-LIF-08]` makes every
  byte that walk misses slack — so 'belongs to no class' describes nothing, and
  a register row for it would be a row no file could exhibit."* That is the
  right answer and it is the reason F33/L18 are the only overlap rows and there
  is no "uncovered byte" row. I checked: there is none.

**Cross-check against Appendix A.** The 128-byte minimal file: claimants
16 (front) + 4 (directory) + 64 (trailer) = 84; slack = 128 − 84 = **44**,
which is exactly §5.1's *"44 bytes of slack, zeroed by advice"*. ✅

**Verdict G1: conforming.** No violation established, nothing unable to be
checked (codec 1 and filter 1 need no external decoder), slack total 47,
complete.

### Generations 2–4: the multi-generation trace

Each commit begins writing at exactly F (§9.4, `[R-LIF-02]` step 1), appends
payloads and the re-emitted whole index region, then the complete directory,
then pad + trailer.

| Gen | Operation | F | Certified | Slack | Verdict |
|---|---|---|---|---|---|
| 1 | create | 576 | 529 | **47** | conforming |
| 2 | append: store tile 2 | 1024 | 657 | **367** | conforming |
| 3 | update: supersede tile 0 | 1472 | 657 | **815** | conforming |
| 4 | compact | 704 | 657 | **47** | conforming |

**G2 layout** — front 16; tile0 [16,144); tile1 [144,272); tile2 [576,704);
index′ [704,788); dir₂ [788,897); pad [897,960); trailer [960,1024).
Claimed 657. Slack 367, which decomposes as the superseded index [272,356) = 84,
dir₁ [356,465) = 109, pad₁ [465,512) = 47, trail₁ [512,576) = 64, and the new
pad = 63. 84+109+47+64+63 = 367 ✅. This is §20.3's note made numeric: *"any
change to a layer's stored-tile set re-emits that layer's whole tile-index
region"*, and the whole prior generation's directory/pad/trailer goes to slack.

**G3** supersedes tile 0: a new 128-byte payload at [1024,1152), a new index at
[1152,1236), dir₃ [1236,1345), pad, trailer [1408,1472). Certified stays 657
(same live structure count); slack climbs to 815. The superseded payload
[16,144) and the G2 index both become slack. This is §20.3's example (b) shape.

Note what G3 is **not** allowed to be: `[R-WRT-05]` obliges byte-identical
re-emission of every retained record, and §20.4's table makes both registered
types PE = 1, so no commit can drop the layer record. My G3 re-emits the layer
record with only crc_of_crc_array and extent_offset changed — which is
permitted because the layer record *is* logically modified (its index moved).

**G4 — compaction.** New file_id (a fresh draw, `[R-WRT-06]`: *"a new draw
under §9.3's randomness advice, not merely a value compared against the
input's"*), generation **1**, every stored tile's bytes verbatim, index region
regenerated (offsets new; lengths, crcs, sentinels unchanged; segment CRCs
recomputed), crc_of_crc_array updated. Output: front 16; tiles at 16/144/272;
index [400,484); dir [484,593); pad [593,640); trailer [640,704). Certified 657,
slack 47 — back to the pre-trailer pad alone, which is §20.5's *"slack is never
carried"*.

A compaction detail I had to compose from three rules rather than read in one
place: my layer declares neither A nor S, so placement was free. Had it declared
a slab, §20.5's exception list is closed — *"every retained record per §20.4,
except that relocation re-points extent slots, regenerates each relocated
tile-index region ..., and updates the layer-record fields covering a
regenerated region (crc_of_crc_array)"* — so clearing the declaration is not
among the compactor's licensed deviations, while `[R-SLB-04]` offers "re-establish
**or** clear". Composition forces re-establish. That is decidable and always
achievable (lay each run out packed with its first stored tile A_slab-aligned),
so I did not file it; but it took three sections to settle.

### A walk that does **not** complete

I built a two-layer adversarial file, F = 896:

```
[  0,  16) front | A.tile0 [16,144) | A.tile1 [144,272) | A.index [200,284)!!
B.tile0 [356,484) | B.index [484,568) | dir [568,782) | pad [782,832) | tr [832,896)
```

Layer A's index region [200,284) overlaps A's own stored tile 1 [144,272) by
**72 bytes**. §15.3's verifier row and `[R-CNT-13]` classify it: *"a verifier
MUST treat an intra-layer overlap — including a stored extent overlapping its
own layer's index region or sub-record extents — as reject-layer"* → **L18**,
reject-layer(A).

§5.2 then governs the total: *"a rejected layer's claimants are not enumerated
... and where the rejection is one the walk itself established, L18's overlap or
L40 through L42's placement among them, the claimants it had already enumerated
are discarded with the layer."* So A's three claimants are discarded.

- Retained claimants: front 16 + B.tile0 128 + B.index 84 + directory 214 +
  trailer 64 = **506**.
- **Partial total = 896 − 506 = 390**, reported as partial, naming layer A and
  L18 as what stopped the walk (`[R-CNT-21]`: *"a verifier reporting one MUST
  say which scope or violation stopped the walk"*).
- Had A been clean, the true slack would be 896 − |union of all claimants| =
  896 − 774 = **122** (the 72-byte hole at [284,356) plus the 50-byte pad).
- 390 ≥ 122 ✅ — the upper-bound property `[R-CNT-21]` claims (*"an upper bound
  on the file's true slack, never an under-count"*) holds, and holds in general:
  enumerated ⊆ all, so F − |union enumerated| ≥ F − |union all|. I checked the
  general argument, not just this instance.

**Verdict: nonconforming** (L18 established), slack total **partial 390**,
stopped by layer A / L18.

**Walk-completeness cases I had to decide and found decided.** These are the
ones I expected to have to guess at and did not:

- A *structural* reject-tile (T6–T12) does **not** make the walk incomplete.
  §9.7: *"the walk passes over it, and the bytes it nominally addresses fall to
  slack (§15.3)."* So the total stays exact and those bytes count as slack.
- An entry whose *only* defect is that its stored bytes fail its crc (T1)
  **keeps its extent** and stays in the walk. §15.3: *"its extent stands and it
  keeps its place in the verifier rows, in run continuity, and in the coverage
  walk."* Total stays exact.
- By the same principle, an entry that is well-formed but whose payload fails to
  decode (T3, T24, T25) or fails a content rule (T2, T4, T5) keeps its extent:
  §15.3's six *structural* rows are a closed list of "an entry whose own 20
  bytes yield no usable extent", and none of those rows is a decode failure.
  I verified the list is exactly six rows and that they map onto seven §21.4
  rows (T6, T7, T8, T9, T10, T11, T12 — §15.3's overflow/bounds row splits into
  T9 and T12).
- A verifier that declines a *decode* on resource grounds still enumerates
  everything (enumeration needs only entries), so the total is exact and the
  verdict is *cannot establish*. **Except** where the decline is of the layer's
  index itself — which is finding **verifier-01**.
- A directory-CRC failure (F20) still owes a total. The trailer is established,
  so F exists; the directory's bounds come from the verified trailer; the walk
  reaches the directory as a claimant even though its checksum failed, because
  §9.7 separates *"reaches the claimants"* from *"checks ... that each verifies
  against the checksum covering it"*. Partial total = F − 16 − dir_length − 64.
  I had to reason this one out but the two clauses are distinct enough that I am
  confident.

---

## 4. Extent overlap, alignment, and slab invariants on adversarial layouts

**Overlap.** Done above (L18). The cross-scope case: had A's tile overlapped
**B's** index region instead, `[R-CNT-13]` gives *"any overlap across layers or
touching another scope's structures as reject-file"* → **F33**, and F33's row
excludes the front block and trailer because the bounds rows F9/F10, F31/F32,
L16/L17, T8/T9 catch a claimant reaching them at their own tiers. I checked that
exclusion is sound: a claimant can only reach [0,16) or [F−64,F) by violating one
of those bounds rows first, since §9.7 requires each claimant to lie within
[16, F − 64).

**Alignment (`[R-SLB-01]`, L40).** Layer declares A = 4096. I laid stored tiles
at 4096 and 8192 (pass), then moved the second to 8200: 8200 mod 4096 = 8 →
**L40**, reject-layer, detector *verifier*.

Two things I checked and found correctly scoped:
- The invariant binds **stored tiles only**. It does not constrain the index
  region, the directory, or record extents. §16.1 says *"every stored tile's
  offset satisfies offset mod A = 0"* and nothing more. My aligned layer's index
  at 8320 is not 4096-aligned and that is fine.
- A structurally-invalid entry is **not** measured against A. §15.3: such an
  entry *"contributes no stored extent to the verifier rows, which bind over
  well-formed entries' extents only"*, and L40 is a verifier row. So a bogus
  offset in a length-0 entry is T10 and not also L40.

**Slab (`[R-SLB-02]`/`[R-SLB-03]`, L41/L42).** Layer with S = 2, A_slab = 512,
interleaved, N = 4 → runs [0,2) and [2,4). This is where §16.2's transparency
rule earns its keep, and I built the pair of cases that separate its two halves:

*Case (a) — ordinal 2's entry has length 0 (T10, structural).* §16.2: *"So are
the entries §15.3 classifies reject-tile on a structural ground: they address no
usable extent, and the run's stored tiles close over them."* Run [2,4)'s stored
tiles are therefore just ordinal 3, at 1024; 1024 mod 512 = 0 → **pass**.

*Case (b) — ordinal 2's entry is well-formed, at offset 768, but its stored
bytes fail its crc (T1).* §16.2: *"An entry whose only defect is that its stored
bytes fail its crc is not transparent — its offset and length stand, and the
packing relation reads them as it does any other stored tile's."* Run [2,4)'s
first stored tile is now ordinal 2 at 768; 768 mod 512 = 256 → **L42 fires**,
reject-layer, on top of the tile-scope T1.

I want to record that this is a well-made rule, because it is the kind of thing
that usually breaks. The claim §16.2 attaches — *"so this invariant stays
decidable from the index entries alone, given the committed file length §15.3
already requires to classify any entry"* — is **true**, and I verified it: case
(a) and case (b) are separated by *structural* classification, which needs only
the entry's 20 bytes and F. Whether the payload's crc actually verifies never
enters the run computation, because a crc-failing entry and a good entry are
treated identically. A verifier can therefore check L41/L42 before fetching a
single payload byte. That is a non-obvious invariant and the text nails it.

Two further slab points I checked:
- Runs never span channel blocks: for planar, block c is [c·N, (c+1)·N) and run
  r of that block starts at c·N + r·S (`[R-SLB-02]`). So growing N in a planar
  layer re-partitions **every** block, which is why §20.3 step 4 requires the
  declaration re-established or cleared. Consistent.
- *"A run with no stored tiles imposes nothing"* — my case (a) run would have
  imposed nothing had ordinal 3 also been a sentinel. Stated, not inferred.

**Mutual exclusion.** `[R-CNT-16]` bars A ≠ 0 with S ≠ 0 (L20); `[R-CNT-23]`
bars A_slab ≠ 0 with S = 0 (L28) and requires A_slab a power of two in [1, 2⁶²]
when S ≠ 0, A_slab = 0 included as a violation (L29). The three rows partition
the declaration space cleanly; I found no gap.

---

## 5. Checksum obligations — is every live structure covered?

§8.1's map, walked against the claimant kinds a live state can contain:

| Live claimant | Covering checksum | Verified how |
|---|---|---|
| front signature block | none | byte equality (§6.1) — the stated exception |
| trailer | its own [60,64) over [0,60) | comparison; terminal, covered by nothing further |
| directory region | final 4 bytes over dir_length − 4 | comparison; terminal |
| tile-index region | per-segment CRC array, itself under crc_of_crc_array, itself inside the directory under the directory CRC | full chain closes |
| stored tile | its index entry's crc field | comparison |
| user-metadata extent | final 4 bytes over the preceding bytes *as stored, before decoding* | comparison; terminal |
| extent of an unassigned-type record | **none** | not checked — stated exception |

So: **every live structure is covered by a checksum except two, both explicitly
excepted** — the front block (equality instead) and the unassigned-type record
extent (opaque by §7.2). §4.5 states the same two exceptions plus the three
terminal fields, and the two statements agree. The chain of trust in §8.2 —
trailer → directory → crc_of_crc_array → segment CRC array → index segment →
index entry → stored tile — is strictly ordered and I implemented it in that
order; `[R-ENC-05]` forbids allocating, seeking or issuing I/O on any integer
before the covering checksum verifies, which is what makes the ordering
mandatory rather than stylistic.

One nicety I checked: the segment CRC array is covered *once*, by
crc_of_crc_array, and not also by any segment CRC (segments cover entry bytes
only). §4.5's claim that interior checksum fields are *"both comparison-verified
and covered by exactly one further checksum"* holds for all three interior kinds
(segment CRC array, entry crc fields, crc_of_crc_array). No double coverage, no
gap.

---

## 6. Decoded-content obligations

**What a verifier must decode.** Every stored tile, unconditionally (§9.7,
quoted above). Plus every user-metadata document under an *assigned* encoding
(§19.2's extent-use tier; `[R-MTA-09]`).

**What it must compare against.**
- decoded length ≡ the declaration-derived decoded size (`[R-SER-07]`, T3) —
  P·Q interleaved, P·Bᶜ planar numeric, ⌈P/8⌉ packed planar bool. Never from
  payload content, never from an embedded frame size (`[R-COD-06]` bars sizing
  a buffer from Frame_Content_Size even when present).
- every padding position ≡ the channel's **recorded** fill bytes, and every pad
  bit ≡ the fill bit (`[R-SER-05]`, T4/T5).
- every interleaved bool byte ∈ {0x00, 0x01} (`[R-SER-08]`, T2).
- exact consumption of the stored extent, no trailing bytes (`[R-COD-08]`, T24).
- codec-specific header checks (T17–T22 for zstd; T14 for codec 1).
- the document rules of §18.2 (R4–R10) and member sort order (F27/L48).

**What it is permitted to skip.**
- Sample *values*. §21.7: *"this format detects corruption of structure, not
  incorrectness of content."* There is nothing to compare them against.
- Slack content entirely (§5.2).
- The content of an unassigned-type record's extent (§8.1).
- The content of a user-metadata document under an unassigned encoding
  (`[R-MTA-10]`) — and this is a *skip without penalty*: certification is
  unaffected, only a report is owed.
- A decode it declines on resource grounds — but that costs the certificate:
  the verdict falls to *cannot establish* (`[R-COD-11]`, `[R-ERR-04]`,
  `[R-MTA-09]`).

I confirmed the asymmetry between the codec space and the metadata-encoding
space is deliberate and stated in three places that agree: §17.4's closing
sentence, `[R-MTA-10]`, and §21.6's table row. An unassigned *codec* is a
layer-scope violation (L43); an unassigned *metadata encoding* splits — 0 and
the reserved range are violations (R1), the experimental range is a defined
non-violation. §21.5's preamble states the split explicitly: *"what
`[R-MTA-10]` withdraws is the document's content rules, never the encoding
byte's own value set."* That is exactly the distinction I needed and it is
drawn.

**One decode subtlety worth recording.** §17.2's Note on zstd Window_Size
resolves a case I would otherwise have had to guess: a tile whose decoded size
is below 1 KiB (§14.2's worked examples give 18 and 30 bytes, §14.3's gives 2)
*"is therefore encodable under codec 3 only as a single-segment frame, and no
conforming file turns on which derivation a reader implements."* T21's check is
therefore well-defined at small sizes. Good.

---

## 7. Findings

Four. Each is quoted, located, and byte-level-tested. I flag none of them as
byte-level, and I say why in each case; I would rather be explicit about a
near-miss than pad the count.

---

### verifier-01 — AMBIGUITY — §5.2 `[R-CNT-21]`, §9.7 `[R-LIF-08]`: the grounds for a *partial* slack total omit the resource decline that §21.9 licenses

**Quotation (§5.2, `[R-CNT-21]`):**

> Where the walk of §9.7 does not enumerate every region's claimants — whether
> because a scope-level rejection ends that scope's enumeration ... or because
> the verifier elected under `[R-CNF-11]` to stop at the first violation — the
> verifier MUST report the total as partial.

**And (§9.7, `[R-LIF-08]`):**

> Where the walk does not complete — a scope-level rejection blocks enumeration,
> or the verifier stops at the first violation (`[R-CNF-11]`) — the sum is
> reported as partial

Both passages give the same closed two-item list of grounds: a scope-level
*rejection*, or an elective stop at the first *violation*. Neither reaches the
third case, which the document elsewhere expressly licenses.

`[R-ERR-04]` lets a conforming reader — and a verifier is one (§2.3) — decline
a file *"at the whole file, or at the narrowest scope whose declarations exceed
what it can serve, a layer or a tile"*, and §21.9's minimum guarantee for
addressed tiles per layer is 2³². A layer declaring entry_count = 2⁴⁰ is
conforming; its index region is 2⁴⁰ · 20 + 2²⁴ · 4 ≈ 22 TB. A verifier that
declines that layer on resource grounds **cannot enumerate its stored extents at
all** — not because the layer was rejected (a resource decline is expressly not
a validity error: *"a refusal on resource grounds MUST be reported as a resource
limit and not as a validity error"*), and not because it elected to stop at a
violation (there is none). Yet §5.2 says flatly that *"a verifier that reaches a
live state MUST report the total number of slack bytes"*.

**Permitted readings.**

1. The general clause *"Where the walk of §9.7 does not enumerate every region's
   claimants"* governs, and the "whether because … or because …" pair is
   illustrative rather than exhaustive. The verifier reports the total as
   **partial**, discarding the declined layer's claimants, and names the layer
   as what stopped the walk. Appendix H's phrasing — *"naming the scope or
   violation that stopped the walk"* — accommodates naming a scope with no
   violation attached, which is weak support for this reading.
2. The pair is exhaustive (the "whether … or …" construction normally is). A
   resource decline is neither ground, so the verifier owes a **complete** total
   — which it cannot compute, and which if reported as complete would be wildly
   wrong: it would count the entire declined layer's stored payloads as slack,
   under-stating nothing but over-stating the file's waste by potentially the
   whole file. That is the one failure mode `[R-CNT-21]`'s *"never an
   under-count"* guarantee was written to exclude, and reading 2 breaks the
   guarantee's usefulness rather than the guarantee itself.

**I picked reading 1**, because reading 2 makes a MUST unsatisfiable and because
`[R-CNT-21]`'s upper-bound property is preserved only under reading 1. But the
choice is mine, not the document's: nothing in §5.2, §9.7, `[R-ERR-04]`,
`[R-CNF-11]` or Appendix H names the resource decline as a partial-total ground,
while §5.2 goes to unusual length to name the *other* boundary case exactly
(*"there is no F and no live state to walk, so the total is not owed at all …
which is not a partial total but the absence of one"*). The care taken over that
case makes the silence over this one read as an omission rather than a
delegation.

**What an implementer does wrong without it.** A verifier following reading 2
reports a complete slack total that treats a declined layer's entire live data
as reclaimable, and §22.3 makes that number load-bearing: *"a verifier reports
the slack total (§9.7), which is the number that distinguishes a working file
from a padded one."* An operator acting on it compacts a file that has nothing
to reclaim, or worse trusts a "complete" figure that is an artifact of the
verifier's own limits. The fix is one clause: add the resource decline to both
grounds lists.

**Byte-level: no.** The disagreement is over a reported number and a
partial/complete label. Both verifiers report *cannot establish* (the decline is
a `[R-CNF-11]` capability/resource ground), so no accept/reject verdict and no
emitted byte turns on it.

---

### verifier-02 — CONTRADICTION — §21.2's preamble vs. §6.1 `[R-CNT-04]`, §19.1 step 1, §2.3, and F6's own row: the front-block check reaches a foreign-major file that the preamble says no row reaches

**Quotation (§21.2, preamble):**

> Every row here presupposes a file this specification judges: one declaring
> format major 1. A file declaring another major is neither conforming nor
> nonconforming under this text (§2.3, `[R-CNF-02]`), and no row below reaches
> it — §6.2's ordered validation puts the version gate ahead of every check but
> the trailer magic and the trailer CRC, so a foreign-major file is refused on
> capability grounds before any geometry row applies.

**Against (§19.1, step 1, `[R-RDR-01]`):**

> A reader whose open leaves bytes [0, 16) resident — a speculative suffix
> window that reached offset 0 included — MUST verify the front signature block
> by byte equality **before other processing** (mismatch: reject-file)

**And (§21.2, row F6's own Condition cell):**

> The 16-byte front signature block is not byte-identical to the constant; the
> obligation binds a reader holding those bytes resident, and a reader that
> would have to fetch them MAY defer or omit the check (`[R-CNT-04]`); **a
> verifier holds no such exemption (§2.3)**

The preamble's exception list is closed and names exactly two checks that
precede the version gate: the trailer magic and the trailer CRC. It omits the
front signature block. But the front block check is ordered *ahead of all of
them* — §19.1 places it in step 1, before step 2's trailer, and `[R-CNT-04]`
says "before other processing" — and §2.3, F6's row, and Appendix H
(*"the 16-byte front signature block by byte equality, which `[R-CNT-04]` lets a
reader not holding it resident defer or omit and §2.3 does not (F1, F6)"*) all
deny the verifier the residency exemption. So a verifier always runs it, always
first.

The consequence is a concrete file on which two verifiers must disagree: a file
whose trailer declares version_major = 2 and whose front block byte 0 is `0x88`
rather than `0x89`.

- Verifier A follows §19.1's step order and F6's row: the front-block equality
  fails at step 1, before the version gate is ever reached, so **F6** is
  established → verdict **nonconforming**.
- Verifier B follows §21.2's preamble: the file declares another major, *"no row
  below reaches it"*, so the refusal is on capability grounds → verdict
  **cannot establish**.

§2.3 makes the difference substantive, not cosmetic: *"Cannot establish is not a
finding that the file is nonconforming"*, and §2.3 says of a foreign-major file
that it *"is neither conforming nor nonconforming under it … and that refusal is
not a finding about its bytes."* One of A and B is reporting a finding about
bytes this document declines to judge; the other is withholding a finding this
document's rows do make. The text does not say which.

The same fault reaches **F1**, whose Instances cell is *"front signature block
bytes [0,8); trailer magic at F-64"*: the preamble accounts for the second
instance and not the first.

**Note that §21.1's tiebreak does not resolve this.** §21.1 says *"where a row
and the rule it cites diverge, the rule governs"*, and extends the same
treatment to §21.6's entries. §21.2's preamble is neither a row nor a §21.6
entry, and it does not cite a governing rule of its own — it makes a claim
*about* the register. So the standing tiebreak is unavailable here, which is
precisely what distinguishes this from the register-row-versus-rule pattern that
prior rounds over-claimed on.

**What an implementer does wrong without it.** A verifier built from §21.2's
preamble suppresses two rows (F6 and F1's front-block instance) on any
foreign-major file, and reports *cannot establish* for a byte sequence that is
not a TARN file of any major — §6.3's `[R-CNT-24]` is explicit that *"the front
signature block (§6.1) is constant"* in every format major version, so its
failure is a cross-major finding of exactly the kind the trailer magic's failure
is. The narrow fix is to extend the preamble's exception list from two items to
three; the cleaner one is to say "the checks §6.3 `[R-CNT-24]` fixes across all
majors", which is a set the document already defines.

**Byte-level: no.** The fork is between two verdicts, *nonconforming* and
*cannot establish*, neither of which certifies the file and neither of which
licenses a reader to accept it — §21.2's own preamble and §2.3 agree that a
foreign-major file carries no acceptance obligation either way. No conforming
writer's output changes, and no reader's accept/reject decision changes: a
reader rejects on the front block under `[R-CNT-04]` and on the major under
`[R-CNT-07]` regardless. What changes is which of the verifier's three verdicts
is correct for a given byte sequence, which is a report-level fork.

---

### verifier-03 — CONTRADICTION — §11.1 `[R-GEO-01]`'s parenthetical asserts a grid of one tile where `[R-GEO-02]` and `[R-GEO-03]` give a grid of zero

**Quotation (§11.1, `[R-GEO-01]`):**

> A tile extent MAY exceed its dimension's extent (the grid is then a single
> padded tile along that axis).

**Against (§11.1, `[R-GEO-02]`, the very next paragraph):**

> A dimension with extent 0 is valid: its grid count is 0, the layer has zero
> addressed tiles, its tile index has zero entries, and its reference array is
> empty.

The parenthetical is normative text (§2.1 exempts only §1, Notes, Examples,
Rationales, and appendices identified as non-normative — a parenthetical inside
a requirement is none of those). Its antecedent condition — a tile extent
exceeding its dimension's extent — is satisfied by **every** layer with
Eᵢ = 0 and Tᵢ ≥ 1, since Tᵢ ≥ 1 is itself required. For those layers its
consequent is false: §11.2's `[R-GEO-03]` gives Gᵢ = ⌈0/Tᵢ⌉ = 0 (and states the
division in the form *"Eᵢ/Tᵢ plus 1 if Eᵢ mod Tᵢ ≠ 0"*, which is 0 + 0), and
`[R-GEO-02]` says so in words.

The gap matters because Gᵢ propagates: N = ∏Gᵢ, entry_count = N or C·N
(`[R-CNT-17]`), extent_length = entry_count · 20 + ⌈entry_count/2¹⁶⌉ · 4, and
crc_of_crc_array = 0 when entry_count = 0 (`[R-CNT-23]`). A rank-1 zero-extent
layer written under the parenthetical would carry entry_count = 1, a 24-byte
index region and a nonzero crc_of_crc_array; written under `[R-GEO-02]` it
carries entry_count = 0, extent slot (0,0), crc_of_crc_array = 0. A verifier
would reject the first at **L21** and **L22**.

**Why I nonetheless judge this non-byte-level.** The two readings are not
equally available. `[R-GEO-02]` is adjacent, specific to exactly this case,
stated in four independent consequences, cross-referenced from §21.6's table
(*"A dimension has extent 0 | A valid, empty layer: zero addressed tiles, an
empty index, reads returning no samples"*), from §17.2's lz4 Note (*"a layer
that addresses none — any dimension extent 0 (`[R-GEO-02]`, §21.6)"*), from
§15.4's example (*"At entry_count = 0 there is no region at all"*), and from
§11.1's own Rationale (*"the first growth of a zero-extent layer included"*).
The parenthetical is a one-clause gloss on a MAY. No competent implementer
reaches E = 0 and computes G = 1. So while I can quote a genuine
contradiction in normative text, I cannot in honesty name two implementations
that would fork on it, and I decline to inflate it.

**What an implementer does wrong without it.** Nothing, if they read the next
paragraph. The defect is that the parenthetical states its consequent
unconditionally where it holds only for Eᵢ ≥ 1 — the repair is to say "where
Eᵢ ≥ 1" or to move the gloss into the Rationale, where §2.1 gives it no force.

---

### verifier-04 — AMBIGUITY — §21.7's account of §20.3's declaration-change bar reads as promising a §21.4 witness that does not always exist

**Quotation (§21.7, `[R-ERR-01]`):**

> §20.3 step 4's bar on a declaration change is witnessed only where the
> affected tiles remain stored — the §21.4 rows then fire — and a commit that
> supersedes every tile it would have damaged leaves the live state clean, so
> the bar is unwitnessed there for the same reason `[R-LIF-01]` is

**Permitted readings.** The sentence supports two:

1. *"witnessed only where"* is a necessary condition alone: witnessed ⟹ the
   affected tiles remain stored. The em-dash clause is a partial gloss, and
   nothing is claimed about the converse.
2. The em-dash clause supplies the converse: the affected tiles remaining stored
   ⟹ the §21.4 rows fire. Read this way the sentence partitions the bar's
   violations exhaustively into "tiles still stored, therefore caught by §21.4"
   and "tiles superseded, therefore unwitnessed".

Reading 2 is false, and I can construct the counterexample from §14's own
arithmetic. Take an interleaved layer with three uint8 channels `r`, `g`, `b`,
all with fill `0x00`, and extents exactly divisible by the tile extents so the
layer has **no padding positions** and (being interleaved, not packed bool) no
pad bits. Commit a change that permutes the channel declarations to `b`, `g`,
`r`, retaining every stored tile. Then:

- decoded size P·Q is unchanged (Q = 3 either way);
- every value's byte offset within the decoded tile image is unchanged
  (F⁰,F¹,F² = 0,1,2 either way);
- the padding-position set is empty, so `[R-SER-05]` has no witness — **T4** and
  **T5** cannot fire;
- there is no bool channel, so **T2** cannot fire;
- codec and filter are untouched, so **T3**, **T14**, **T24**, **T25** cannot
  fire.

No §21.4 row fires. Yet the commit is squarely within §20.3 step 4's bar under
its own general test — *"The test is the effect on such a tile, and the list
names where that effect arises rather than standing on its own"* — because every
retained tile's stored bytes now mean something different: byte 0 of each sample
is read as channel `b` where it was written as channel `r`. The reference array
changed silently, with every tile still stored.

**Which I picked.** Reading 1. *"Only where"* is the operative quantifier and it
is a necessary condition; the case above falls under §21.7's **first** paragraph
instead (*"A writer that emits well-formed structures carrying wrong sample
values … produces a file that every checksum in §8 certifies"*), which owns it
correctly. So the section's *conclusion* — that the bar carries no register row
— survives, and §21.1's normative completeness claim survives with it, since a
file produced this way is conforming as a pure predicate on bytes
(`[R-CNF-02]`): a fresh creator could have emitted exactly those bytes for a
`b,g,r` layer.

**What an implementer does wrong without it.** A verifier author who reads the
second paragraph as reading 2 concludes that running §21.4's tile checks
discharges the whole of §20.3 step 4 whenever tiles remain stored, and reports
accordingly — for instance certifying a file and telling an operator that its
layer declarations were checked against its retained tiles. They were not, and
cannot be, because §9.7 does not reconstruct the prior generation. The repair is
a clause: "the §21.4 rows then fire *where the change reaches a structurally
constrained byte*", which is the qualification §21.7's own first paragraph
already states for the general case (*"The obligations of §14.5 and `[R-SER-08]`
narrow this only where content is structurally constrained: padding positions,
pad bits, and boolean bytes"*).

**Byte-level: no.** Both readings leave the file conforming and leave every
reader's and writer's byte-level behavior identical; the disagreement is about
what a verifier may claim to have checked, not about what it accepts. The
counterexample file is emitted identically by writers under either reading.

---

## 8. Things I checked and found sound (recorded so the absence of a finding is legible)

- **The register's own arithmetic.** 121 rows over 273 instances, matching
  §21.8, computed mechanically. Zero detector/detection-point mismatches.
  §21.1's two stated axes (layout formulas; magnitude direction) are applied
  uniformly — I checked T3, T14, T21, T22, T26, L21, L22, L30, L44, F17, T24
  individually and found no row that departs from the criterion.
- **Twin-row symmetry.** I walked every file-scope/layer-scope twin pair
  (F21/L10, F22/L11, F23/L12, F24/L13, F25/L46, F26/L47, F27/L48, F28/L49,
  F29/L14, F30/L15, F31/L16, F32/L17, F33/L18, F34/L19, F35/L24, F36/L25) and
  found each pair's instance counts explicable by container count. This is the
  place the brief warned an enumeration might be extended on one side only, and
  in the *rows* it is not. (The one asymmetric enumeration I did find is
  verifier-02, and it is in a preamble, not a row.)
- **§16.2's transparency rule.** Exercised on the two-case adversarial slab
  layout above; the "decidable from the index entries alone" claim is true and
  non-obvious.
- **§20.3 step 4's declaration bar.** Exercised on four cases: extent growth
  within a grid count (permitted; a padding position becoming real held fill),
  extent growth across a grid count (permitted; index re-emitted, planar
  ordinals renumber), a shrink turning a real position into a padding position
  (barred unless the stored byte already holds fill), and a filter change whose
  mandated stride is the identity (permitted). All four fall out of the rule's
  general test correctly. The "provided the grown geometry stays within every
  bound the layer's own declarations impose, `[R-COD-07]`'s lz4 decoded-size cap
  being the one such bound" clause checks out: decoded size does not depend on
  Eᵢ, so growth can only trip the cap through the addressed-tile quantifier that
  §17.2's Note describes.
- **§20.4's drop rules.** The MU=0/PE=0 row's *"a commit whose only change is a
  supersede MUST retain the record"* and *"a commit whose only effect would be
  the drop MUST retain it"* are both non-circular and both decidable. No layer
  record or user-metadata record can ever be dropped by a commit.
- **§20.5's closed exception list** against `[R-SLB-04]`'s "re-establish or
  clear" — composes to "re-establish", always achievable.
- **Appendix G.** Item 3's emission order reproduces my G4 compaction layout
  exactly (tiles in disk-ordinal order, then the index region, then record
  extents, then the directory, first structure at 16). Item 2's hash input is
  fully determined once item 3 fixes placement: [0, F−64) plus the trailer's
  first 60 bytes with file_id zeroed, and the trailer CRC at [60,64) is
  correctly excluded (it could not be an input). Item 3's *"which §5.2 counts as
  no structure"* about the front block is exactly right — §5.2 makes it a
  coverage class but not a *structure*. Item 6 (sentinel for every all-fill
  tile) composes correctly with §14.5, since an edge tile whose real samples all
  equal fill has every decoded byte equal to fill.
- **The three-verdict vocabulary's closure.** Verified that *unexamined* can
  only arise after an established violation, so it never competes with *cannot
  establish*.

## 9. Where the document left me guessing, in order of how much it cost me

1. The partial-total ground for a resource decline (finding verifier-01) — I had
   to choose.
2. The verdict for a foreign-major file with a broken front block (finding
   verifier-02) — I had to choose.
3. Whether a file-scope violation established *by* the walk (F33, F7) makes the
   total partial. I settled on no: §5.2's trigger is *"does not enumerate every
   region's claimants"*, and F33/F7 are established only *after* enumeration
   completes, since both need every claimant's position. So the total is exact
   and the verdict is nonconforming. I am confident enough in this not to file
   it, but it took re-reading §5.2 and §9.7 three times each.
4. Whether the directory region remains a claimant when its own CRC fails (F20).
   Settled yes, because §9.7 separates *"reaches the claimants"* from
   *"checks … that each verifies against the checksum covering it"*. Not filed.
5. What a compactor does with an index entry §15.3 classifies structurally
   invalid. Settled: refuse, because §20.5 says *"MUST refuse to compact when
   any check `[R-WRT-09]` obliges fails, and MUST NOT emit a file carrying a
   violation it has detected"*, and it cannot copy the entry byte-identically
   the way §20.3 step 2 licenses an appender to, because it regenerates offsets.
   The asymmetry with the appender is deliberate and stated on the appender's
   side; I did not file it, but a sentence on the compactor's side would have
   saved me the composition.

---

## 10. Confidence

**Medium-high.** I built a conforming file byte-for-byte, ran four generations
through it, computed the coverage partition and slack total at each, reproduced
every checksum constant the document states that is locally computable, and
exercised the overlap, alignment and slab invariants on layouts designed to
separate their edge cases — and the document answered nearly everything without
my having to invent a rule. The certification procedure, the verdict vocabulary,
the checksum coverage map, the decode obligations and the slab transparency rule
are all fully determined. The two places I had to choose (verifier-01,
verifier-02) are both in the verifier's *reporting* surface rather than its
accept/reject surface, which is why I flag neither as byte-level; but both are
real, and verifier-01 in particular is a MUST that a legitimate verifier cannot
satisfy as written.
