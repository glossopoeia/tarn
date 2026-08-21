# Round 18 — Verifier implementer, working transcript

## Disclosure

I opened exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
read in four `Read` calls covering lines 1–4340 (the whole document). I ran three
local Python scripts of my own authoring, in the scratchpad, that read no project
file: a CRC-32C implementation to reproduce the document's stated constants, a
regex pass over the register tables (reading `spec/tarn.md` only) to count rows and
semicolon-separated instances, and a placement/coverage calculator for the files I
construct below. I ran two `grep`/`sed` passes over `spec/tarn.md`. I opened no ADR,
no `docs/`, no `conformance/`, no `registry.json`, no `PLAN.md`, no `AGENTS.md`, no
git history, and issued no web request. I did not read or list the round18 output
directory.

---

## 0. What I built

A conforming verifier, on paper: the certification procedure as an ordered
algorithm; the coverage walk with worked arithmetic on files I constructed; the
overlap/alignment/slab checks on an adversarial layout; the checksum obligations
with every locally-computable constant reproduced; the decoded-content
obligations; and a four-generation trace with a certification result at each step.

I record the places I had to guess as I reach them, and collect the findings at
the end.

---

## 1. Checksum constants — reproduced

Every constant the document states that I could compute locally, I computed.
CRC-32C implemented from `[R-ENC-09]`'s parameters alone (reflected polynomial
0x82F63B78 derived from the stated 0x1EDC6F41, init 0xFFFFFFFF, final XOR
0xFFFFFFFF):

| Constant | Document | Computed | Where |
|---|---|---|---|
| CRC-32C(`"123456789"`) | 0xE3069283 | **0xE3069283** | §4.5 check vector |
| CRC-32C(zero bytes) | 0x00000000 | **0x00000000** | §4.5, §5.1 example, App. A |
| CRC over 4 sentinel entries (80 bytes) | 0x80A34955, stored `55 49 A3 80` | **0x80A34955** | §7.4 worked example |
| crc_of_crc_array over `55 49 A3 80` | 0xC4EE982E | **0xC4EE982E** | §7.4 worked example |
| CRC of a full all-sentinel segment (2¹⁶ entries) | 0xEECB3BB2 | **0xEECB3BB2** | `[R-IDX-05]`, App. B |
| Appendix A trailer CRC over trailer[0,60) | 0xE00938D2, stored `D2 38 09 E0` | **0xE00938D2** | App. A |

Five distinct constants, all reproduced. The sentinel entry I built from
`[R-IDX-02]`'s prose (`FF ×16 00 ×4`) rather than from any vector, and the
Appendix A trailer I reassembled field by field from §6.2's layout table (60
bytes exactly, as the table's offsets require) — so both computations are
independent checks of the layout tables as well as of the constants.

**Could not reproduce:** nothing in the document. The two external-format
constants — the zstd frame magic `28 B5 2F FD` and the lz4 cap `0x7E000000` —
are pinned to RFC 8878 and to the LZ4 Block Format Description, which I was not
permitted to consult; I verified only that they are internally consistent
(§17.2, App. B, L44's condition text). I did not verify `[R-TYP-02]`'s bfloat16
identification against IEEE 754 for the same reason, though its worked example
(bfloat16 1.0 = 0x3F80 from binary32 0x3F800000) is arithmetically self-consistent.

Other arithmetic I checked and found correct: §15.4's 1,000,000-entry example
(16 segments, 64-byte array, region 20,000,064, entry 999,999 at segment-relative
byte 339,180, segment 15 at [19,660,800, 20,000,000)); §15.4's planar example
(disk ordinal 74 at region bytes [1,480, 1,500)); §11.4's ordinal example
(s = 10, in-tile ordinal 11,452, planar disk ordinal 74); §14.2's stride examples
(Q = 3 → 18 bytes; Q = 5 → 30 bytes, `m` at byte 29); §14.3's packed-plane example
(`55 01` / `55 FD`); §17.3's shuffle example (byte-for-byte); §7.4's 81-byte
inline payload (4 + 34 + 18 + 12 + 13 = 81); §20.3's 32·20 + 4 = 644; §21.9's
note arithmetic (2³² tiles → 256 KiB array; 2³⁶ → 4 MiB); Appendix A's whole
128-byte layout.

I also checked §21.8's own counts mechanically: the register tables hold
**121 rows** (F 36, L 49, T 26, R 10) over **273 instances** under §21.1's counting
rule (semicolon-separated; a cell reading `—` is one). That matches
`[R-ERR-02]` exactly. And I extracted every `[R-XXX-NN]` identifier: 161 distinct,
no cited-but-undefined identifier, `[R-SER-04]` appearing only in its withdrawal
note as §14.4 says it should.

---

## 2. The certification procedure

### 2.1 Verdict vocabulary and what bars certification

From §2.3 (`[R-CNF-11]`), §2.4 (`[R-CNF-12]`), §17.4 (`[R-COD-11]`), §18.2
(`[R-MTA-09]`) and §21.6, I derive:

- **conforming** — available only when the traversal established no violation
  *and* left no requirement unchecked on a capability or resource ground.
  §2.3 makes the second half mandatory rather than optional: "a verifier MUST NOT
  certify a file it reports that way", and both §17.4 and `[R-MTA-09]` say "MUST
  NOT certify the file" of their own grounds.
- **nonconforming** — whenever any violation is established. §2.3's priority rule
  is unconditional: "An established violation takes priority: a verifier that has
  established any violation reports *nonconforming*, however many requirements it
  was unable to check". This covers ignore-record violations too — §21.5's
  preamble: "Every row here is a violation all the same: the outcome bounds a
  reader's blast radius and never makes the file conforming".
- **cannot establish** — no violation established, and at least one requirement
  unchecked on a capability or resource ground. §2.3 enumerates five grounds; I
  find only three of them reachable by a *conforming* verifier:
  1. foreign format major (reachable);
  2. an unimplemented MU = 1 record type (reachable only from the *experimental*
     range — a reserved-range MU = 1 type is F35/L24, an established violation,
     and the priority rule then forces *nonconforming*);
  3. a decode declined on resource grounds under `[R-ERR-04]` (reachable, but
     only above §21.9's minimum guarantees: `[R-ERR-04]`'s last paragraph makes
     declining *within* the table a failure of conforming-reader status, so a
     verifier may not manufacture this ground);
  4. `[R-COD-11]`'s "cannot execute a codec or filter" — **dead** for a conforming
     verifier. Every assigned codec and filter is core (`[R-CNF-03]`), a verifier
     is a reader (§2.3), so the only unexecutable values are reserved/experimental
     ones, which are L43/L45 violations. §17.4 says exactly this itself. I
     implemented it anyway, as a defensive branch that can only fire in a
     non-conforming verifier;
  5. `[R-MTA-09]`'s declined document decode (reachable, above §21.9's 16 MiB).

Two report-only channels ride alongside the verdict and never change it:
*unexamined* scopes (§2.3, for a verifier that stops at the first violation) and
the per-requirement "unable to check" report, which §2.3 requires "whichever of
the three verdicts it reports". That last clause is vacuous under *conforming* —
if nothing is unchecked there is nothing to name — but harmless.

SHOULD deviations are advisories that do not bar certification, and `[R-CNF-12]`
relieves me of hunting for them: "a SHOULD deviation is reported where the
verifier observes it and not hunted for". My verifier therefore reports, without
searching: a non-zero slack gap (`[R-CNT-03]`), a discovery window over 65,536
bytes (`[R-CNT-09]`), a version_minor above the floor (`[R-CNT-26]`), a name not
in NFC (`[R-ENC-14]`), and a JSON number binary64 cannot represent exactly
(`[R-MTA-04]`).

### 2.2 The ordered algorithm

Each step names the rows it can establish. Where a check cannot be run, the
verifier names the requirement and the ground and continues if it can.

**Step 0 — size.** Obtain the transport-authoritative file size (`[R-CNT-10]`).
*Guess recorded:* `[R-CNT-10]` says a reader that cannot obtain one "MUST probe
separately or fail the open". "Fail the open" is not one of §2.3's three verdicts.
I treat a transport that cannot supply an authoritative size as a capability
ground and report *cannot establish*, naming `[R-CNT-10]`. Nothing in the document
says so; nothing contradicts it either.

**Step 1 — front signature block.** Fetch [0, 16), compare by equality
(`[R-CNT-04]`). Rows: F6, F1's front-block instance. §2.3 removes
`[R-CNT-04]`'s residency exemption from a verifier; F6's own condition cell and
Appendix H both restate that ("a verifier holds no such exemption (§2.3)"). This
check precedes everything else — `[R-CNT-04]` says "before other processing", and
§21.2's preamble relies on that placement.

*Decision recorded:* §2.4 says of reject-file that "A reader MUST NOT rely on any
structure in it", and §2.3 makes a verifier a reader. Read literally, establishing
F6 would forbid every later step, since walking the directory is relying on a
structure. I read "rely on" as *rely on for the purpose of returning or asserting
data*, not *read at all* — because §2.3 presents stopping as optional ("A verifier
MAY stop at the first violation it finds"), which presupposes continuing is
permitted, and because §21.2 and §21.3 assign a dozen reject-file and
reject-layer rows to detection at *certification*, a tier that only exists for a
verifier that keeps walking. I continue.

**Step 2 — trailer, in §6.2's fixed order.** Fetch [F − 64, F).
2a magic (F8, F1); 2b trailer CRC (F14); 2c version gate — F18 at
version_major = 0, otherwise an unimplemented major is a capability ground;
then, those three gates passed, the remaining gates *as a set* (§6.2 says
"MUST validate all of the following", and §24 confirms they are not separable:
"§6.2's field gates are validated together, so a file failing two of them
attributes to neither alone"): flag gates (F19; ignore-lane bits ignored per
`[R-CNT-08]`), committed_file_length against the transport size and mod 64 (F17,
F13), dir_offset ≥ 16 (F9), dir_length ≥ 4 (F16), dir_offset + dir_length ≤ F − 64
(F10), 1 ≤ generation ≤ 2⁶³ − 1 (F11, and F2 for the domain), file_id ≠ 0 (F12),
reserved zero (F15), plus F5 for the 128-byte floor and F2/F3 for the u64 domain
and sums.

I checked that F5 can never fire alone and does not need to: F ≥ 128 follows from
dir_offset ≥ 16, dir_length ≥ 4, dir_offset + dir_length ≤ F − 64 and F mod 64 = 0,
so any file below 128 also trips F10 or F13. §24 already licenses a vector that
exercises several rows and records which it was built for.

If step 2 rejects before a live trailer exists, §5.2 discharges the slack duty
entirely: "there is no F and no live state to walk, so the total is not owed at
all". I report the trailer failure and nothing about slack.

**Step 3 — directory region.** Fetch [dir_offset, dir_offset + dir_length),
verify the terminal CRC over the preceding dir_length − 4 bytes before any other
use (`[R-CNT-11]`). Row F20.

**Step 4 — top-level record walk.** Parse under §7.2's framing (F29 for a header
or inline payload past dir_offset + dir_length − 4, or residue; F24 for type 0).
Per record: reserved-range type → F36, and with MU = 1 → F35 (§21.1 names F35 a
specialization of F36, so a file exhibiting both is recorded against F35);
experimental-range type with MU = 1 and unimplemented → capability ground;
MU = 0 → ignored, but its extent still enters the walk (see §3.2 below);
registered types → stored MU/PE against §7.3's registry (F28, and L49 for layer
records), MU = 1 with PE = 0 (F25/L46), reserved flag bits 2–15 (F26/L47);
multiplicity (F34 for a second top-level user-metadata record); extent slot
(F30, F31, F32, F2, F3); user-metadata framing (F21 for a (0,0) slot, F22 for
extent_length < 5, F23 for inline_length ≠ 1).

**Step 5 — layer-name namespace.** F4, over raw bytes, decided first and without
requiring the names to be valid (§19.1 step 4 is explicit). L3, L5, L6 also fall
here — §21.3 puts their *Detected* cell at "open", which matches §19.1's parse of
each layer record's name. A layer record whose name field does not lie inside its
inline_length contributes no name and is instead L23/`[R-CNT-18]`.

**Step 6 — per-layer record validation** (§19.3's list, all decidable from the
resident directory and F, no fetch): L1, L2, L4, L7–L17, L19–L36, L39, L43–L45.

**Step 7 — per-layer index chain.** Fetch the region named by the layer record's
extent slot; verify crc_of_crc_array over the segment-CRC array (L37), then each
segment CRC over exactly entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count)) (L38). I
noted that `[R-IDX-05]`'s constant is never a substitute here — "verification is
byte comparison of computed CRCs, never constant matching" — and that a *partial*
all-sentinel segment must not carry it.

**Step 8 — per-entry classification** (§15.3): T6, T7, T8, T9, T10, T11, T12.
I confirmed the six *structural* rows are exactly the six §15.3 says they are, and
that the sentinel exclusion is watertight: an entry with offset = length = all-ones
and crc ≠ 0 is T6, not T11, because T11's condition says "the value being distinct
from the all-ones sentinel"; an entry with offset = all-ones and length = 5 is T7
for the same reason.

**Step 9 — per-tile decode.** §9.7 is unconditional: "A verifier decodes every
stored tile, whatever content obligations §14 places on the layer". Fetch
[offset, offset + length), verify the entry crc (T1), run codec then inverse
filter, check length against the declaration (T3), exactness of consumption (T24),
malformation (T25), and the codec-specific header rows (T14 for codec 1, T17–T22
for codec 3, T13/T15/T16/T23 as causes recorded against T24/T25). Then the content
rows: T4 (every padding position carries its channel's recorded fill), T5 (every
pad bit carries the plane's fill bit), T2 (every interleaved bool byte at a *real*
position is 0x00 or 0x01). T26 has no procedure of its own; it is recorded when
T2 or T4 fires and the layer declares filter 2.

**Step 10 — coverage.** Build the claimant set, check disjointness (F33, L18) and
containment in [16, F − 64), check `[R-CNT-05]`'s gap (F7), check alignment (L40)
and the slab invariants (L41, L42).

**Step 11 — slack total** (§5.2, §9.7), exact or partial.

**Step 12 — user-metadata extents.** Terminal CRC (R2), encoding value (R1),
decode (R3), encoding-2 frame constraints (R4), document content (R5–R10), and
member ordering (F27/L48). Report each record ignored at an unassigned encoding —
owning scope, encoding value, stored extent length (`[R-MTA-10]`).

**Step 13 — verdict**, per §2.1 above.

---

## 3. The coverage walk

### 3.1 What partitions, and into what

`[R-CNT-02]`'s classes are closed: front signature block; stored-tile extent;
record extent ("the bytes any record's extent slot references, whatever the
record's type"); the directory; the trailer. §9.7 tells the walk exactly what to
reach and resolves the three questions I would otherwise have had to guess:

- a record is not a claimant of its own — its header and inline payload lie inside
  the directory region;
- a layer record's extent *is* its tile-index region, so the region enters once,
  as that record's extent, not as a second claimant;
- the front block and the trailer are claimed, and the [16, F − 64) bound on every
  other claimant keeps them disjoint by construction.

One consequence worth stating because it is load-bearing and easy to get wrong:
an experimental MU = 1 record type may, under §7.2, "carry further references
where this specification or registry review defines them". Bytes so referenced are
in none of `[R-CNT-02]`'s five classes, so they are *not* part of the live
committed state and the walk counts them as slack. The closed class list is what
makes this decidable rather than an unbounded traversal.

### 3.2 Certified, counted, and neither — concrete file W1

Layer `sst` exactly as §7.4's worked example declares it: rank 1, dimension `x`
E = 100, T = 32, so G = 4 and N = 4; interleaved; one float32 channel `temp`,
fill 0x7FC00000; codec 1, filter 1; A = 0, S = 0. entry_count = 4, so
extent_length = 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84 (`[R-CNT-17]`). Decoded size per tile is
P · Q = 32 · 4 = 128, and under codec 1 the entry's length must equal it
(`[R-COD-04]`). Tiles 0 and 1 stored, tiles 2 and 3 sentinel.

```
[0,16)      front signature block
[16,144)    stored tile 0        128 bytes
[144,272)   stored tile 1        128 bytes
[272,356)   sst tile-index region 84 bytes   (entry array 80 + segment CRC array 4)
[356,465)   directory            109 bytes   (record 24+81=105, + terminal CRC 4)
[465,512)   pre-trailer pad       47 bytes   slack
[512,576)   trailer               64 bytes
F = 576, 576 mod 64 = 0, dir_offset + dir_length = 465 ≤ F − 64 = 512
```

Live-state partition, summed by the walk:

    16 + 128 + 128 + 84 + 109 + 64 = 529 claimed
    576 − 529 = 47 slack

and the 47 is exactly the pre-trailer pad, so this file has no other waste.

Now the charter's three-way question. Which bytes are **certified**?

| Claimant | Bytes | Covered by | Certified? |
|---|---|---|---|
| front block [0,16) | 16 | nothing — byte equality (§6.1, §8.1) | yes, by equality |
| tile 0 [16,144) | 128 | entry 0's crc field | yes |
| tile 1 [144,272) | 128 | entry 1's crc field | yes |
| index entries [272,352) | 80 | segment CRC array | yes |
| segment CRC array [352,356) | 4 | layer record's crc_of_crc_array | yes |
| directory records [356,461) | 105 | directory terminal CRC | yes |
| directory CRC field [461,465) | 4 | nothing — terminal, comparison-verified | yes, by comparison |
| trailer [512,572) | 60 | trailer CRC field | yes |
| trailer CRC field [572,576) | 4 | nothing — terminal, comparison-verified | yes, by comparison |

529 of 529 live bytes certified; 47 counted-but-unconstrained. The chain closes:
crc_of_crc_array is a field of the layer record's inline payload, which sits inside
the directory region and is covered by the directory CRC, which is covered by
comparison against the trailer-anchored region bounds. §8.2's ordering —
trailer → directory → crc_of_crc_array → segment CRC array → segment → entry →
stored tile — is exactly the order I verify in.

**Can a byte be neither?** No. §5.2's Note settles it: "`[R-LIF-08]` makes every
byte that walk misses slack — so 'belongs to no class' describes nothing, and a
register row for it would be a row no file could exhibit". So the partition is
total by construction and only disjointness is testable — which is why F33 and
L18 exist and no third row does.

**Is every live structure covered by a checksum?** *No*, and the document says so
twice. §8.1's last row: "Extent of a record of a type this specification has not
assigned | none — the bytes are opaque (§7.2) | —". §22.3 restates it: "The extent
of a record of a type this specification has not assigned is covered by no
checksum either (§8.1), so corruption inside it is equally invisible". So a
complete walk yields *four* categories, not two: certified by a checksum;
certified by equality or comparison (front block, terminal CRC fields); claimed and
counted but covered by nothing (an unassigned-type record's extent); and slack.
There is a fifth flavour that is not a category but is worth naming in a report:
a user-metadata extent under an *unassigned* encoding is CRC-covered but
content-unconstrained (`[R-MTA-10]`, §22.3) — its bytes are integrity-checked and
never inspected, which is precisely why `[R-MTA-10]` makes the verifier name each
one.

*Observation I did not raise to a finding, because it does not fit the taxonomy:*
`[R-MTA-10]` states the governing principle as "bytes a certificate covers without
inspecting are counted and named, never silent", and imposes a MUST-report for its
own case. The one live structure covered by **no** checksum at all — the unassigned
record type's extent — carries no such reporting duty anywhere in the document.
§22.3 names it as a residue "stated rather than defended" and stops. The document
decides this (no duty exists because none is stated), so it is not an ambiguity,
and nothing contradicts it, so it is not a contradiction; but it is the sharpest
asymmetry I found in §8.1's map, and I mention it here rather than pad the finding
list with it. My verifier reports such extents anyway, by analogy.

### 3.3 A walk that does not complete — concrete file W1b

W1 plus a second layer `aux`: rank 1, dimension `y`, E = 16, T = 8, so G = N = 2;
interleaved; one uint8 channel `v`, fill 0x00; codec 1, filter 1. entry_count = 2,
extent_length = 2 × 20 + 4 = 44, decoded size P · Q = 8. Both tiles stored, and
placed so that they overlap:

```
[0,16)      front block                       16
[16,144)    sst tile 0                       128
[144,272)   sst tile 1                       128
[272,356)   sst index                         84
[356,364)   aux tile 0                         8   ┐ overlap on [360,364)
[360,368)   aux tile 1                         8   ┘
[368,412)   aux index                         44
[412,620)   directory (105 + 99 + 4)         208
[620,640)   pre-trailer pad                   20   slack
[640,704)   trailer                           64
F = 704, 704 mod 64 = 0, 620 ≤ 640
```

(`aux`'s inline payload is 75 bytes: name 4, the nine scalars 34, one dimension
entry 18, one channel entry 6, trailing fixed fields 13. Record = 99.)

The overlap is two stored extents of one and the same layer — L18, reject-layer,
detector *verifier*, governed by `[R-CNT-13]` and §15.3's row "two stored extents
of the same layer overlap … *verifier*: reject-layer". §5.2 then governs the
accounting, and it is the one place in the document that tells a verifier to throw
work away: "where the rejection is one the walk itself established, L18's overlap
or L40 through L42's placement among them, the claimants it had already enumerated
are discarded with the layer".

So `aux` contributes nothing — not its two tiles, not its index region:

    enumerated and retained: 16 + 128 + 128 + 84 + 208 + 64 = 628
    partial total: 704 − 628 = 76

and the verifier MUST say what stopped it: **layer `aux`, L18 (`[R-CNT-13]`)**.

Checking §5.2's guarantee that a partial total is "an upper bound on the file's
true slack, never an under-count": the bytes actually unclaimed by any live
structure are the 20-byte pad. The reported 76 = 12 (the union of the two
overlapping aux tiles — note *union*, not sum; §5.2 says "the bytes claimed",
which is set-valued, and the sum reading would make the total an *under*-count
whenever two enumerated claimants overlap) + 44 (aux index) + 20 (pad). 76 ≥ 20 ✓,
and it tightens to 20 exactly when the walk completes. Verdict: **nonconforming**,
slack reported as partial.

I also worked the case where a *structural* reject-tile entry appears, because it
is the one exception §9.7 carves: such an entry "does not make the walk incomplete:
the walk passes over it, and the bytes it nominally addresses fall to slack". So a
file can be nonconforming (say T8, offset < 16) and still have an **exact** slack
total. My verifier keeps the two facts separate: the verdict and the exactness of
the total are independent.

*Guess recorded (and raised to finding verifier-03):* the case §5.2 does not
resolve is a **file-scope** rejection after the trailer. Corrupt one byte of W1's
directory so its terminal CRC fails (F20). The trailer is valid, so a live state is
reached and the total is owed; `[R-ENC-10]` forbids acting on any field the failed
CRC covers, so nothing beyond the directory can be enumerated. Is the directory
region itself "a claimant the walk did enumerate"? Its bounds come from the
verified trailer, and §9.7 has the walk read it first, so I say yes and report
576 − 16 − 64 − 109 = **387**. A verifier that treats a claimant whose checksum
failed as not enumerated reports 576 − 16 − 64 = **496**. Both satisfy every
property §5.2 states (upper bound, never an under-count, says what stopped the
walk), and the document mandates the number.

---

## 4. Extent overlap, alignment, slab — on an adversarial layout

I built one layer that exercises all three at once rather than reasoning in the
abstract. Layer `adv`: rank 1, dimension `x`, E = 40, T = 8, so G = N = 5;
interleaved; one uint8 channel, fill 0x00; codec 1, filter 1; decoded size
P · Q = 8. Slab S = 2, A_slab = 16, alignment A = 0 (they are mutually exclusive,
`[R-CNT-16]`/L20). entry_count = 5, extent_length = 5 × 20 + 4 = 104.

`[R-SLB-02]` partitions the single interleaved block [0, 5) into runs starting at
block_start + r·S: run 0 = ordinals {0,1}, run 1 = {2,3}, run 2 = {4} — "the final
run of a block can cover fewer than S ordinals".

| ordinal | entry | run | verdict |
|---|---|---|---|
| 0 | offset 1024, length 8 | 0 | first stored tile of run 0; 1024 mod 16 = 0 ✓ |
| 1 | offset 1034, length 8 | 0 | packing requires 1024 + 8 = 1032; got 1034 → **L41 (gap)** |
| 2 | sentinel | 1 | transparent — "Sentinel tiles are transparent to run continuity" |
| 3 | offset 1040, length 8 | 1 | first *stored* tile of run 1; 1040 mod 16 = 0 ✓ |
| 4 | offset 1044, length 8 | 2 | first stored tile of run 2; 1044 mod 16 = 4 → **L42** |

and entry 3's extent [1040, 1048) against entry 4's [1044, 1052) overlap → **L18**,
reject-layer. Put the index region at [1048, 1152) and entry 4 also overlaps its
own layer's index region — §15.3's row names that case explicitly, and it is L18
again, not F33, because the index region belongs to the same layer.

Three things this layout forced me to settle, all of which the document settles:

1. **Which entries are transparent to the run.** `[R-SLB-03]`: sentinels, and
   "the entries §15.3 classifies reject-tile on a *structural* ground". An entry
   whose only defect is a failing stored-bytes crc is **not** transparent — "its
   offset and length stand, and the packing relation reads them as it does any
   other stored tile's". L41's condition cell restates both halves. I checked the
   third case the text does not name: an entry that is well-formed, whose crc
   verifies, and whose *tile* is reject-tile for a codec reason (T14, T25). It is
   in neither named category, so it is not transparent — transparency is granted
   only to §15.3's structural rows — and it counts for packing, alignment and the
   coverage walk. Decidable, and I did not have to guess.
2. **Decidability from entries alone.** `[R-SLB-03]` claims the invariant "stays
   decidable from the index entries alone, given the committed file length §15.3
   already requires to classify any entry". I confirmed that: classifying an entry
   as structural needs offset, length, crc and F, all of which I have; the packing
   relation needs only offsets and lengths; A_slab comes from the layer record.
   No decode, no payload fetch.
3. **Alignment applies to stored tiles, not to regions.** `[R-SLB-01]`: "every
   stored tile's offset satisfies offset mod A = 0". The tile-index region is not
   constrained. I built a second layer `aln` with A = 4096 and a stored tile at
   8200 (8200 mod 4096 = 8) to fire L40, and confirmed it fires against the entry's
   *offset*, not against any region boundary.

I also confirmed L39's bound (A a power of two in 512 … 2⁶²) and L29's
(A_slab a power of two in 1 … 2⁶², A_slab = 0 included when S ≠ 0), and L28
(A_slab ≠ 0 with S = 0). A_slab = 1 is legal and makes the alignment half vacuous —
the "contiguity-only" declaration §16.2's closing Note describes.

**Cross-scope overlap.** Moving `adv`'s tile 4 to overlap `sst`'s index region
changes nothing about the check and everything about the outcome: §7.2 gives
reject-file, F33, because it touches another scope's structures. F33's condition
also disposes of the boundary cases I would otherwise have had to reason about —
"a claimant reaching the front signature block or the live trailer is instead
caught by the bounds rows F9/F10, F31/F32, L16/L17 and T8/T9, each at its own
tier". A stored extent cannot reach [0,16) without tripping T8, and cannot reach
[F−64, F) without tripping T9, so F33 never needs to consider them.

**`[R-CNT-05]`'s gap (F7).** Placing any structure in [dir_offset + dir_length,
F − 64) is a file-scope validity error. In W1 that gap is [465, 512); a stored tile
at [465, 500) would be F7. I noted that the *converse* is not a violation: §6.2
says "a longer gap is conforming, and no conforming commit produces one", and §2.3
declares this one of exactly two conduct-not-bytes cases. So my verifier reports a
long pad as a `[R-LIF-02]` step-5 conduct note and does not bar certification.

---

## 5. Decoded-content obligations

**What the verifier must decode.** Every stored tile, unconditionally (§9.7: "A
verifier decodes every stored tile, whatever content obligations §14 places on the
layer: §21.4's codec rows are file-conformance violations, and a verifier MUST NOT
certify past a violation it has not looked for"). And every user-metadata document
under an encoding this specification assigns — not because §9.7 says so, but
because F27/L48 (`[R-MTA-05]`'s member ordering) carry detector *verifier*, and
§2.3 obliges the verifier to check "every file-level requirement".

**What it compares against.** Nothing in the payload; everything in the
declarations. T3 tests the decoded length against a decoded size that "is a
function of the layer's declarations alone — geometry, layout, and channel types —
never of payload content" (`[R-SER-07]`). T4 tests each padding position against
the channel's *recorded* fill (`[R-TYP-06]` makes the recorded fill authoritative,
and §13.1 notes that "a verifier's acceptance of a tile turns on it"). T5 tests
pad bits against the fill bit. T2 tests interleaved bool bytes at real positions
against {0x00, 0x01}.

I checked that T2 and T4 together exhaust `[R-SER-08]`, as T2's condition claims:
a bool byte at a padding position is T4's, and the fill it must equal is itself
constrained to 0x00 or 0x01 by `[R-TYP-07]`, so no interleaved bool byte in a
conforming file can be anything else. And I checked that the check runs on the
*decoded* image, after the inverse filter: §17.1 puts the filter between the
decoded image and the codec, so §14.5's constraint is a constraint on the decoded
image and a mis-strided filter shows up there — which is exactly what T26 records
("the check that detects it is T2's or T4's").

The padding set is derivable: for a tile at tile coordinates tᵢ, in-tile position
uᵢ is a padding position iff tᵢ·Tᵢ + uᵢ ≥ Eᵢ for some i (§11.3). Worked against
§14.5's example — extents (5,5), tile extents (4,4), edge tile (1,1), one uint16
channel with fill 0xABCD: 32 decoded bytes, value 0 real, values 1–15 each `CD AB`.
I reproduced that by construction.

**What it is permitted to skip.**
- Sample values at real, non-boolean positions. §21.7: "this format detects
  *corruption of structure*, not *incorrectness of content*", and — critically for
  the verdict — "None of these is a requirement a verifier is *unable to check*
  within the meaning of `[R-CNF-11]`: no file-level witness exists to check, so
  nothing about the file is left undetermined and the verdict is unaffected." That
  sentence is what keeps *conforming* reachable at all. If unwitnessable
  obligations counted as unchecked requirements, every verifier would report
  *cannot establish* for every file, since no verifier can check `[R-LIF-01]`.
  §2.3's restriction of cannot-establish to a "capability or resource ground"
  makes the same point from the other side.
- Slack content (§5.2, unconstrained by rule).
- An unassigned record type's extent content (§7.2, §8.1).
- A user-metadata document under an unassigned encoding — and §2.3 is emphatic
  that this is *not* a cannot-establish ground: "no content rule attaches there,
  so nothing is left unchecked, and certification is unaffected". This is the
  narrow case I had to be careful with: encoding 0 and reserved 3–0x7F are
  *also* unassigned but R1 registers them as violations, because what
  `[R-MTA-10]` withdraws is the document's content rules, "never the encoding
  byte's own value set". Only the experimental range ≥ 0x80 gives a conforming
  file with an uninspected document.
- Prior generations (§9.7's Note; and §9.6 forecloses the temptation: "no verdict
  turns on the probe … For a verifier the probe is diagnosis … not a finding about
  the file it was given").

---

## 6. Multi-generation trace

Each generation's file is the previous one plus appended bytes, except G4.
Every F is a multiple of 64 and every dir_offset + dir_length ≤ F − 64.

### G1 — creation (`[R-LIF-02]`'s creation path, `[R-WRT-02]`)

W1 from §3.2. F = 576. Live claimed 529, **slack 47** (the pad alone).
Verdict: **conforming**. Nothing unchecked; walk complete; no advisory except that
the writer zeroed its pad, satisfying `[R-CNT-03]`.

### G2 — append: supersede sst tile 1 (`[R-WRT-04]`)

Writing begins at exactly F = 576 (`[R-LIF-02]` step 1).

```
[576,704)   new stored tile 1                128
[704,788)   sst index region, re-emitted whole 84   (entry 1 re-pointed and re-crc'd,
                                                      entries 0/2/3 byte-identical)
[788,897)   directory (sst record, new extent slot + new crc_of_crc_array)  109
[897,960)   pad                                63   slack
[960,1024)  trailer, generation 2, same file_id     64
F = 1024
```

Live claimed: 16 + 128 + 128 + 84 + 109 + 64 = 529. **Slack 495.**
Cross-check against what the commit superseded: old tile 1 (128) + old index (84) +
dir₁ (109) + pad₁ (47) + trail₁ (64) + pad₂ (63) = 495 ✓.

This is §20.3's Note in miniature — one changed entry cost the whole 84-byte index
region — and it is the number `[R-CNT-21]` says "tells an operator to compact".
Verdict: **conforming**, slack total exact.

### G3 — append: add a file-scope user-metadata record and an experimental ancillary

The metadata document is 20 bytes of JSON under encoding 1, so the extent is 24
(document + terminal CRC-32C, ≥ 5 per `[R-CNT-25]`, inline payload exactly 1 byte
per `[R-MTA-03]`). The ancillary is an experimental-range type (≥ 0x8000) with
MU = 0, PE = 1, inline_length 0 and a 32-byte extent.

```
[1024,1048) user-metadata extent               24
[1048,1080) experimental record extent         32
[1080,1238) directory (105 + 25 + 24 + 4)     158
[1238,1280) pad                                42   slack
[1280,1344) trailer, generation 3              64
F = 1344
```

Live claimed 634, **slack 710** (= 495 + dir₂ 109 + trail₂ 64 + pad₃ 42 ✓).

Coverage broken down the way the charter asks:

    certified (checksum, equality, or terminal comparison)   602
    claimed and counted, covered by no checksum               32   ← the experimental extent
    counted-but-unconstrained (slack)                        710
                                                            ----
                                                            1344 = F ✓

Verdict: **conforming**. The experimental MU = 0 record is a defined non-violation
(§21.6, `[R-CNT-15]`, `[R-CNF-02]` — §10.3's prohibition binds conduct, not bytes),
its extent is a claimant "whatever the record's type", and no rule attaches to its
content. Had it carried MU = 1 the verdict would instead be **cannot establish**,
naming `[R-CNT-15]` and the record's type as the capability ground — the file
remaining conforming all the same (§21.6's second structural case).

### G4 — compaction (`[R-WRT-06]`, `[R-WRT-07]`, `[R-WRT-09]`)

Fresh file_id, generation 1, ignore-lane bits copied forward, version_minor the
greater of `[R-CNT-26]`'s floor and the input's. Placement is the compactor's
(§20.5: "free to place structures anywhere §5.2 admits and every declared layout
invariant permits"); `sst` declares neither A nor S, so I pack:

```
[0,16)     front block                     16
[16,144)   tile 0 (bytes verbatim, crc unchanged)   128
[144,272)  tile 1 (bytes verbatim, crc unchanged)   128
[272,356)  index region, regenerated: entry 0 offset 16, entry 1 re-pointed to 144,
           lengths and crcs unchanged, segment CRC recomputed                84
[356,380)  user-metadata extent, relocated verbatim, slot re-pointed         24
[380,412)  experimental extent, relocated verbatim, slot re-pointed          32
[412,570)  directory (same three records; layer record's crc_of_crc_array
           updated, all three extent slots re-pointed)                      158
[570,576)  pad                                                                6
[576,640)  trailer, file_id Y, generation 1                                  64
F = 640
```

Live claimed 634, **slack 6.** From 710 to 6 — the whole point of the operation.
Verdict: **conforming**.

The exceptions to byte-identical re-emission I relied on are stated, not assumed:
§20.5 says "every retained record per §20.4, except that relocation re-points
extent slots, regenerates each relocated tile-index region (entry offsets new;
entry lengths, entry crcs, and sentinel entries unchanged; segment CRCs recomputed
over the entries as re-emitted), and updates the layer-record fields covering a
regenerated region (crc_of_crc_array)". Record sizes are unchanged by all of that
— extent_offset is a fixed u64, crc_of_crc_array a fixed u32 — so dir_length is
still 158 and my arithmetic holds.

Two compactor behaviours I checked rather than assumed:
- The experimental MU = 0 / PE = 1 record must be retained and relocated, not
  dropped: §20.4's drop licence is the MU = 0 / PE = 0 row alone, and `[R-WRT-08]`
  bars re-encoding it. Relocation is safe precisely because §7.2 forbids an
  MU = 0 record's payload or extent from encoding file offsets.
- Regenerating the index region cannot proceed past a structurally bad entry:
  "`[R-IDX-03]` gives it no stored extent for a re-pointing to target … `[R-WRT-06]`
  then obliges refusal … no drop is available, a tile-index entry being no record
  §20.4's table licenses dropping". I confirmed `[R-WRT-06]` really is the
  requirement that carries the MUST — it closes the paragraph containing "MUST NOT
  emit a file carrying a violation it has detected" — so the citation is sound.

*Guess recorded:* §9.1 makes compaction a "whole-file rewrite", not a commit, and
§20.5 never cites `[R-LIF-02]`. I nonetheless applied `[R-LIF-02]` step 5's
pad-to-the-next-64 to the output, on §20.1's "An appender and a compactor satisfy
every writer requirement for the bytes it produces". Nothing turns on it — §6.2
says a longer gap is conforming — so either reading certifies.

---

## 7. Things I checked and found sound

Listed because a null result is evidence too, and because the brief asked me to
spend the bulk of my effort outside the recently changed text.

- The chain of trust closes with no orphan: every live structure's checksum has a
  covering checksum, terminating at the trailer CRC and the directory CRC, both
  comparison-verified. §4.5's three-way split (equality-checked front block,
  terminal fields, interior fields) matches §8.1's map row for row.
- `[R-CNT-19]`'s "exactly one checksum" is a property of the map, not a state a
  file can be in, so its absence from §21.7's account of undetectables is correct.
- §15.3's sentinel exclusions are airtight against `[R-ENC-03]`/`[R-ENC-04]`
  (§15.2: "`[R-ENC-03]`'s value-domain rule and `[R-ENC-04]`'s sum rule apply to
  the fields of non-sentinel entries only"), and T6/T7/T11 do not double-count.
- §21.1's specialization list (F1 of F6 and F8, F35 of F36, L24 of L25) is
  correct as far as it goes; T12 is arguably a specialization of T9 and F3 of F10
  and neither is listed, but §21.1 says "Some rows are", not "these are all".
- §5.2's Note correctly identifies that only disjointness is testable, and there
  is indeed no register row for "belongs to no class".
- An *ignore-record* record's extent is still a claimant. §2.4's "skipped as
  though absent" tempted me the other way, but §8.1's dedicated row for an
  unassigned type's extent — a record class that is *always* ignore-record —
  settles that ignore-record does not remove a claimant.
- The §6.1 residency rule and §6.4's request accounting are consistent with
  Appendix A's 112-byte-window walkthrough.
- No lowercase BCP-14 modal appears anywhere in normative text. Every occurrence
  of a lowercase "must", "may", "should" or "shall" sits inside a `>`-quoted Note,
  Rationale or Example — non-normative by §2.1. The one place a permission is
  written in lowercase prose against an ALL-CAPS restriction (§20.5's "it is free
  to place structures anywhere §5.2 admits", which omits `[R-CNT-05]`'s pre-trailer
  gap) resolves the safe way round: the capitalised writer MUST governs and the
  lowercase permission is not a BCP-14 permission at all.
- §20.4's table is internally consistent, and its interaction with §20.5's
  relocation exception does not contradict "Retain byte-identical" — `[R-WRT-08]`
  carves the relocation explicitly.
- The document's own counts are right: 121 rows, 273 instances, 36/49/26/10 per
  subsection.

A hygiene note, not a finding: the paragraph and table at §20.4 lines beginning
"Persistence governs every record type" carry MUST-level obligations
("The updater MUST NOT modify the scope the record governs", "An appender MUST NOT
drop it except…", "a commit whose only effect would be the drop MUST retain it")
under **no** requirement identifier. §2.2 says normative requirements carry stable
identifiers and §24 says vectors cite identifiers rather than prose positions.
Nothing rides on it here — these obligations are multi-generation and have no
register row or vector — but `[R-CNF-06]` binds them by section reference alone.

---

## 8. Findings

### verifier-01 — CONTRADICTION — §21.7, `[R-ERR-01]`

A single sentence in §21.7 states that §20.3 step 4's bar is witnessed *only* where
the change reaches a byte §14 structurally constrains, and then, in its next
clause, that a change reaching the decoded size instead *is* witnessed.

> "§20.3 step 4's bar on a declaration change is witnessed only where the affected
> tiles remain stored *and* the change reaches a byte §14 structurally constrains —
> a padding position, a pad bit, or a boolean byte — where §21.4's content rows
> fire; a change that reaches the decoded size instead is witnessed by T3 or T14,
> which test a length rather than the decoded image's content"

The conjunction is emphasised in the source (`*and*`), so it is not a stray "and":
the "only" clause requires both conditions. The continuation then supplies two
further witness classes for changes that satisfy neither the padding/pad-bit/bool
condition (decoded size → T3/T14; codec → T15/T17/T23/T25, or T14 at codec 1).
Both readings of the sentence cannot hold. The intended reading is almost certainly
that "only where the affected tiles remain stored" is the operative restriction and
the three witness classes are alternatives, in which case "*and*" should be the
start of an enumeration rather than a second necessary condition.

Consequence for an implementer: §21.7 is the document's account of what no check
detects, and §21.1 relies on it — "detectability being the gate `[R-CNF-07]`
already applies and §21.7 the account, by class, of what fails it". A reader
building either a verifier or a corpus from this paragraph can come away believing
that a declaration change reaching a tile's decoded size has no witness, when T3
and T14 are exactly that witness and both carry detector *reader*. It does not
change what my verifier does — the register rows are what I implement, and §21.7
creates no obligation — which is why I do not call it byte-level.

**Byte-level: no.** Neither reading changes any byte a writer may emit or any
accept/reject verdict: T3 and T14 are reader-detected rows a conforming reader
implements regardless of what §21.7 says about them, and §21.7's own subject —
`[R-LIF-01]`-class history properties — is outside what any single file witnesses.

### verifier-02 — AMBIGUITY — §2.3 (`[R-CNF-02]`) against §21.2's preamble

What verdict does a verifier report for a file whose version_major names a major
it does not implement *and* whose front signature block or trailer magic is
corrupt?

§2.3 says such a file is outside the dichotomy altogether:

> "This document defines format major 1, and a file declaring another major is
> neither conforming nor nonconforming under it: a reader refuses such a file on
> capability grounds (§6.3, `[R-CNT-07]`), and that refusal is not a finding about
> its bytes."

§21.2's preamble restates that and then carves four rows out of it:

> "Four rows are outside that reasoning and do reach it, because their subject is a
> field fixed across every major (`[R-CNT-24]`): F8 and F1's trailer-magic
> instance, F14's trailer CRC — the two checks §6.2 places before the gate — and F6
> with F1's front-block instance, which `[R-CNT-04]` places before other
> processing."

Two defensible readings:

**(A)** "Do reach it" means the row applies: §21.1 defines a row as one detectable
file-conformance violation, so a foreign-major file with a byte-reversed front
block *exhibits* F6/F1 and is nonconforming. §2.3's priority rule then decides the
verdict: "An established violation takes priority: a verifier that has established
any violation reports *nonconforming*, however many requirements it was unable to
check". Verdict **nonconforming**.

**(B)** "Do reach it" means only that the *check* still runs — a reader holding
[0,16) resident still rejects the file — while §2.3's "neither conforming nor
nonconforming" continues to govern the verdict, since the sentence is stated
without exception and §21.2 opens by repeating it. The file is unimplementable
either way, so the verdict is **cannot establish**, naming `[R-CNT-07]`.

I picked **(A)**, on the specific-governs-general principle and because §21.1
declares the register's completeness normative over *detectable* violations, which
F6 plainly is on a field `[R-CNT-24]` fixes across every major. But (B) is a
straight reading of §2.3 and of §21.2's own first sentence.

An implementer choosing wrong reports the wrong verdict for a whole class of files,
and the corpus feels it: §24 requires each vector's manifest entry to record
"whether the file is **conforming**" — a boolean with no third state — so under (B)
a foreign-major vector exercising F6 cannot be recorded at all, while under (A) it
records `conforming: false`.

**Byte-level: no.** Both readings bar certification, and reader behaviour is
identical under both: `[R-CNT-04]` obliges a reader holding [0,16) resident to
reject-file on the mismatch, and `[R-CNT-07]` obliges rejection on the
unimplemented major, whichever verdict a verifier prints. No conforming writer may
emit either file, and no reader's accept/reject decision moves. The fork is in the
verdict label and in the corpus manifest, not on disk.

### verifier-03 — AMBIGUITY — §5.2, `[R-CNT-21]`

When a violation at **file** scope stops the walk after the trailer has been
established, `[R-CNT-21]` mandates a number that it does not determine.

> "A partial total is F less the bytes claimed by the claimants the walk did
> enumerate — an upper bound on the file's true slack, never an under-count — and a
> verifier reporting one MUST say which scope or violation stopped the walk."

§5.2's two triggers for a partial total are "a scope-level rejection ends that
scope's enumeration" and the `[R-CNF-11]` stop-at-first-violation election. The
worked illustration is a *layer* only: "a rejected layer's claimants are not
enumerated". Nothing says which claimants count as enumerated when the rejected
scope is the file itself.

Concretely, on my file W1 (F = 576, directory at [356, 465), pad [465, 512),
trailer [512, 576)), corrupt one byte inside the directory so its terminal CRC
fails (F20, `[R-CNT-11]`). The trailer is valid, so §5.2's "no F and no live state"
exemption does not apply and a total is owed. `[R-ENC-10]` then forbids acting on
any field the failed CRC covers, so no record, no extent slot and no index entry
can be enumerated. The permitted readings:

- **Directory enumerated** — its bounds came from the verified trailer and §9.7
  has the walk read it first ("From the live trailer it reads the live directory"),
  so it is a claimant the walk did enumerate even though its checksum failed.
  Total = 576 − 16 − 64 − 109 = **387**.
- **Directory not enumerated** — a claimant whose checksum failed has not been
  established as a claimant at all, so only the front block and trailer count.
  Total = 576 − 16 − 64 = **496**.

Both satisfy every property `[R-CNT-21]` states: both are upper bounds on the true
unclaimed count (47 for the file as laid out), neither under-counts, and both can
name F20 as what stopped the walk. I picked the first, because §9.7 lists the
directory among the claimants unconditionally and separates *reaching* a claimant
from *verifying* it ("It checks that these occupy disjoint byte ranges … and that
each verifies against the checksum covering it"). An implementer picking the second
reports a total 109 bytes larger for the same file.

The same underdetermination reappears for a *capability* stop rather than a
violation stop — an unimplemented top-level MU = 1 experimental record makes the
file reject-file for a reader (`[R-CNT-15]`) while the verdict is *cannot
establish*; §5.2's trigger list speaks of "a scope-level rejection", which fits,
and `[R-CNT-21]`'s "which scope or violation stopped the walk" accommodates a
scope that is not a violation, so that half is answerable — but the same question
about which claimants were enumerated recurs.

**Byte-level: no.** A slack total is a reported figure, not a byte a writer emits
and not an accept/reject decision. `[R-CNT-21]` explicitly says the number "is not
the file's slack total but a bound on it", both readings are valid bounds, and no
file changes conformance status under either. Its cost is to an operator comparing
totals across tools, and to any corpus that ever records one.
