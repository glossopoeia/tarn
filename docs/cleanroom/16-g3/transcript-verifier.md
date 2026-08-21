# Cleanroom round 16 — Verifier implementer, working transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,282 lines), in five `Read` calls covering lines 1–4282 with no gaps. I ran
`wc -l` and `grep` against that file only. Every other command I ran was local
computation in Python over data I typed myself: a CRC-32C implementation, byte
constructions of TARN files of my own design, and arithmetic. I wrote scratch
files (`crc.py`, `witness.tarn`) into my own scratchpad and read back only
`crc.py`, which I wrote.

I did not open `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`README.md`, `CONTRIBUTING.md`, `conformance/`, `spec/registry.json`, or any
ADR. I ran no `git` command. I did not list the round-16 output directory and
did not read any other agent's transcript. I did not search the web.

I used prior knowledge of other array/image formats only to generate suspicions
(e.g. "does the trailer-first ordering leave a short-file hole?"), never to
settle one; every conclusion below is argued from quoted text in `spec/tarn.md`.

---

## 1. What I built

A conforming verifier, on paper but concretely: the ordered certification
procedure, the coverage walk with worked arithmetic on files of my own
construction, adversarial layouts for overlap/alignment/slab, a checksum audit
in which I recomputed every constant the document states that is computable
without external data, the decode obligations, and a four-generation trace
(create → append → update → compact) with a verdict and a slack figure at each
step.

I will state up front where I came out: **the document determined almost
everything I needed.** I have one finding I believe forks a verdict on a
constructible file, one contradiction between §21.7's account and §21.4's rows
that does not fork anything, and three smaller items. Details in §8.

---

## 2. The certification procedure, as an ordered algorithm

### 2.1 Verdict vocabulary

§2.3 `[R-CNF-11]` gives exactly three verdicts, and I take them as a strict
priority lattice:

| Verdict | When |
|---|---|
| **nonconforming** | Any violation established. Dominates everything: *"An established violation takes priority: a verifier that has established any violation reports nonconforming, however many requirements it was unable to check"* |
| **cannot establish** | No violation established **and** at least one requirement unable to be checked on a capability or resource ground. *"cannot establish is available only to a traversal that established no violation"* |
| **conforming** | No violation established and nothing left unchecked. Only then may it certify. |

Two report channels are **not** verdicts and I kept them structurally separate
in my design, because §2.3 says so twice:

- *per-requirement unchecked report* — mandatory in all three verdicts:
  *"A verifier MUST report each requirement it was unable to check on a
  capability or resource ground, naming the requirement and the ground,
  whichever of the three verdicts it reports; that per-requirement report
  constrains the report and not the verdict"*.
- *unexamined* — owed only by a verifier that elected to stop early:
  *"Unexamined is neither a verdict nor cannot establish — it constrains the
  report, not the verdict."*

A consequence I checked and relied on: **a verifier that certifies has examined
everything.** §2.3 licenses stopping only "at the first violation it finds", and
a violation forces *nonconforming*. So there is no path to *conforming* with
unexamined scopes. Good — that closes what would otherwise be a large hole in a
certificate's meaning.

The five enumerated cannot-establish grounds (§2.3):

1. format major not implemented;
2. a record carrying MU = 1 with a type it does not implement (§21.6);
3. cannot execute a codec or filter (`[R-COD-11]`);
4. declines a layer's or a tile's decode on resource grounds, so cannot check
   §14's decoded-content obligations (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`);
5. declines to decode a user-metadata document (`[R-MTA-09]`).

I checked which are *live for a conforming verifier*:

- (3) is effectively dead. §17.4 says *"For a conforming reader that position
  arises only at a reserved or experimental value, every assigned codec and
  filter being core: it rejects the layer"* — and a reserved/experimental codec
  value is L43/L45, an established violation, so the verdict is *nonconforming*,
  not *cannot establish*. `[R-CNF-03]` makes software that cannot run an
  assigned codec not a conforming reader at all. So (3) only bites for a
  non-conforming verifier. This is internally consistent, just vacuous; I
  recorded it rather than flagging it.
- (1), (2), (4), (5) are all live. (4) and (5) are the ones a real tool hits.

Also load-bearing and explicit: §18.2 `[R-MTA-10]`/§21.6 make an
**experimental-range metadata encoding** *not* a cannot-establish ground —
*"no content rule attaches there, so nothing is left unchecked, and
certification is unaffected"* — while encoding 0 and reserved 3–0x7F stay
violations (R1). §21.5's preamble states the distinction outright: *"what
`[R-MTA-10]` withdraws is the document's content rules, never the encoding
byte's own value set"*. Appendix H repeats it. I found this fully determined; it
reads like a previously repaired seam that now holds.

### 2.2 The algorithm

Each step names its input, the rules it discharges, and what happens when it
cannot run.

**V0 — Physical size.** Obtain transport-authoritative F (`[R-CNT-10]`). Local
verifier: the file length.

**V1 — Minimum length.** F ≥ 128 (`[R-CNT-27]`, F5). *Ordering note:* the
document does not place this in `[R-CNT-06]`'s ordered list, and §21.2's
preamble asserts F5 does **not** reach a file declaring a foreign major, which
implies it sits *after* the version gate. For F < 64 that is physically
impossible (there are no bytes at F−64 to read), so I check F ≥ 64 first for
tractability and F ≥ 128 after the version gate. I then verified this never
matters: F must be a multiple of 64 to pass F13, and the only sub-128 multiple
of 64 is F = 64, where dir_offset ≥ 16 and dir_offset + dir_length ≤ F − 64 = 0
are jointly unsatisfiable, so F10 fires anyway. F5's real bite is on files whose
trailer fails other gates too, and §24 `[R-VEC-02]` already covers
non-isolable conditions (*"§6.2's field gates are validated together, so a file
failing two of them attributes to neither alone"*). Not a finding.

**V2 — Front signature block.** Byte-equality over [0, 16) (F1's front-block
instance, F6). A verifier has **no** residency exemption: §2.3 defines a
verifier as one that checks *"every file-level requirement — including those
ordinary readers are exempted from"*, F6's row says *"a verifier holds no such
exemption (§2.3)"*, and Appendix H repeats it. Failure → reject-file →
nonconforming.

**V3 — Trailer, in §6.2's fixed order** (`[R-CNT-06]`): magic (F8, F1); trailer
CRC (F14); version gate (F18 for major 0; foreign major → *cannot establish*);
then jointly the flag gates (F19), committed_file_length = F and a multiple of
64 (F17, F13), dir_offset ≥ 16 (F9), dir_length ≥ 4 (F16),
dir_offset + dir_length ≤ F − 64 (F10), 1 ≤ generation ≤ 2⁶³−1 (F11), file_id ≠ 0
(F12), reserved zero (F15), and the u64 domain / sum rules (F2, F3).

*Cannot-run case:* foreign major. §5.2 is explicit that no slack figure is owed
here: *"Where §6.2's ordered validation rejects the file before a live trailer
is established there is no F and no live state to walk, so the total is not owed
at all: the verifier reports the trailer failure and nothing about slack, which
is not a partial total but the absence of one."* I implemented exactly that.

**V4 — Directory region.** Fetch [dir_offset, dir_offset + dir_length); verify
the terminal CRC over the preceding dir_length − 4 bytes before any other use
(`[R-CNT-11]`, F20). Failure → reject-file. The region's extent is still a
claimant (it is named by `[R-CNT-02]`), so a partial slack total of
F − 16 − 64 − dir_length is computable and I report it as partial.

**V5 — Top-level record walk** (§7.2, §19.1 step 4): exact parse, no residue
(F29); type ≠ 0 (F24); multiplicity (F34); extent-slot rules for non-layer
records (F30, F31, F32); MU gate for unknown types (F35); reserved-range type,
whatever its MU bit (F36); user-metadata framing (F21, F22, F23);
verifier-only flag checks (F25 reserved-flag, F26 MU=1/PE=0, F28 stored-vs-
registry flags); layer-name namespace over raw bytes (F4).

I noted §19.1's careful rule that a layer record whose name field does not lie
within its inline_length *"contributes no name to the namespace"* and is instead
layer-scope — and that uniqueness is decided over raw bytes *"whether or not
each name is itself well-formed"*. Both are needed to make F4 deterministic and
both are stated. Good.

**V6 — Per layer, full layer-record validation** (§19.3 `[R-RDR-03]`): L1–L17,
L19–L36, L39, L43–L47, L49. All decidable from the resident directory and F;
no fetch.

**V7 — Per layer, index chain** (`[R-IDX-04]`): fetch the tile-index region,
verify crc_of_crc_array over the segment CRC array (L37), then each segment CRC
over exactly entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count)) (L38). Then classify
every entry per §15.3 (T6–T12).

**V8 — Per stored tile:** fetch [offset, offset + length); verify the entry crc
(T1); decode (T15–T25, T3, T14); check padding content (T4), pad bits (T5),
interleaved bool bytes at real positions (T2), and mis-strided filter where it
surfaces (T26).

**V9 — Placement invariants:** alignment (L40), slab run packing (L41), slab run
start alignment (L42) — all from index entries plus F, per §16.2's explicit
*"this invariant stays decidable from the index entries alone, given the
committed file length §15.3 already requires to classify any entry."*

**V10 — Extent use:** each record extent's terminal CRC (R2) and the document
rules its assigned encoding attaches (R3–R10). Under an unassigned encoding, no
document rule attaches (`[R-MTA-10]`) and the verifier **reports** the record:
owning scope, encoding value, stored extent length.

**V11 — Coverage walk, overlap, pre-trailer gap, slack total** (§9.7, §5.2,
§6.2): F7, F33, L18, and the slack figure.

Steps V5–V11 are independent of ordering except that V11 needs V5–V7's outputs.

### 2.3 What bars certification

Exactly three things: an established violation (any §21.2–§21.5 row); any
requirement unable to be checked on a capability or resource ground; and — as a
special case of the second — §17.4's and §18.2's explicit "MUST NOT certify"
clauses. A SHOULD deviation does **not** bar (`[R-CNF-12]`). An
experimental-encoding metadata record does **not** bar (`[R-MTA-10]`).

---

## 3. The coverage walk, with arithmetic

### 3.1 The partition

`[R-CNT-02]` gives a **closed** list of claimant classes: *"the front signature
block; or a **structure** — a stored-tile extent, a record extent (the bytes any
record's extent slot references, whatever the record's type, §7.2), the
directory, or the trailer."*

I leaned on the closedness of that list at one point and want to record it,
because it resolves a hole I initially thought I had found. §7.2 says
*"Records with MU = 1 carry further references only where this specification or
registry review (§10) defines them"* — so an unimplemented MU = 1 record could
in principle reference bytes the verifier cannot discover, which would make the
partition undecidable. It does not, because `[R-CNT-02]`'s list is closed on
*extent slots*: bytes referenced any other way are simply not claimants, and
`[R-LIF-08]` makes them slack. The walk therefore stays complete and the total
stays exact even for a file the verifier cannot fully understand. (It still
cannot certify such a file — that is cannot-establish ground 2.) I mention this
because it is the kind of thing that looks like a defect until the closed list
is noticed.

§9.7 adds three refinements I implemented literally:

- a record is *not* a claimant of its own header/payload — the directory covers
  those;
- a layer record's extent slot *is* the tile-index region, so the region *"enters
  the walk once, as that record's extent, and is not a second claimant beside
  it"*;
- an entry `[R-IDX-03]` classifies reject-tile on a **structural** ground
  contributes no extent (six such rows in §15.3 — I counted them: the four
  sentinel-shape rows, length = 0, offset < 16, the >2⁶³−1 row, and the
  overflow/bound row — exactly the "Six rows are marked *structural*" the text
  claims); an entry whose *only* defect is a failed stored-bytes crc keeps its
  extent.

I checked the gap this leaves: an entry that is reject-tile for a **codec**
reason (T14 length mismatch, T17 bad magic, T24 trailing bytes) is classified by
`[R-COD-04]`/`[R-COD-06]`/`[R-COD-08]`, not by `[R-IDX-03]`, so it is neither
"structural" nor "crc-only". The general rule then applies unmodified — it is a
non-sentinel entry, so its extent is a claimant, and it is not transparent to
run continuity. Determinate. No finding.

### 3.2 Can a byte be neither certified nor counted?

No, and the document says why. §5.2's Note: *"The live committed state is
*defined* as the front block plus what a complete coverage walk reaches, and
`[R-LIF-08]` makes every byte that walk misses slack — so 'belongs to no class'
describes nothing, and a register row for it would be a row no file could
exhibit."* Every byte is claimed or slack. What *is* testable is disjointness
(F33, L18) — the Note says exactly that.

But "claimed" is not "content-certified", and a verifier's certificate has four
tiers, not two. I enumerated them:

| Tier | Bytes | Checksum? | Content rules? |
|---|---|---|---|
| A | front block, trailer, directory, index regions, stored tiles, assigned-encoding metadata extents | yes (§8.1) | yes |
| B | extent of a user-metadata record under an **unassigned** encoding | yes (terminal CRC) | **none** (`[R-MTA-10]`) |
| C | extent of a record of a **type this specification has not assigned** | **none** (§8.1 last row) | none |
| D | slack | none | none, counted only |

So the answer to "is every live structure covered by a checksum" is **no** — tier
C. §4.5 and §8.1 both say so, and §22.3 `[R-SEC-04]` states the consequence:
*"corruption inside it is equally invisible"*. Tier B is reported by name
(`[R-MTA-10]`: *"bytes a certificate covers without inspecting are counted and
named, never silent"*). Tier C is **not** given a reporting obligation anywhere
I could find — §22.3 states the residue but assigns no report. I considered
filing that and did not: `[R-SEC-04]` is a security-considerations statement, no
rule is missing, and inventing a reporting duty would be over-reach.

### 3.3 Worked arithmetic — a complete walk

File A, generation 1, entirely of my construction. Layer `a`: rank 1, dimension
`x` with E = 10, T = 4 → G = ⌈10/4⌉ = 3, N = 3; interleaved, one `uint16` channel
`v` with fill `00 00`; codec 1, filter 1, no alignment, no slab. P = ∏Tᵢ = 4,
Q = ΣBᵢ = 2, decoded size = P·Q = 8. All three tiles stored. Tile 2 covers
x ∈ [8, 12): x = 8, 9 real, x = 10, 11 padding, so its last four bytes are the
recorded fill (`[R-SER-05]`) — I encoded them that way.

Index region = entry_count·20 + ⌈entry_count/2¹⁶⌉·4 = 3·20 + 4 = **64** bytes
(`[R-CNT-17]`). Layer-record inline payload = 74 bytes; record = 24 + 74 = 98;
directory = 98 + 4 = **102**.

```
[0,16)      front signature block           16
[16,24)     tile 0                           8
[24,32)     tile 1                           8
[32,40)     tile 2                           8
[40,104)    tile-index region (= layer      64
            record's extent)
[104,206)   directory (dir_offset=104,     102
            dir_length=102)
[206,256)   pre-trailer pad                 50   <- slack
[256,320)   trailer                         64
F = 320, 320 mod 64 = 0
```

Gates: dir_offset + dir_length = 206 ≤ F − 64 = 256 ✓; nothing between 206 and
256 (F7 clear) ✓.

Claimed = 16 + 8 + 8 + 8 + 64 + 102 + 64 = **270**.
Slack = F − claimed = 320 − 270 = **50**, which is exactly the pad. Verdict:
**conforming**, slack 50, no unchecked requirements, nothing unexamined.

### 3.4 Worked arithmetic — a walk that does not complete

Same file with a second layer `b` (rank 1, `y` E = 4 T = 4 → G = 1, one `uint8`
channel, one stored 4-byte tile, index region 1·20 + 4 = 24) added at generation
2, and layer `b`'s **linearization set to 2** — a reserved value, so L33,
reject-layer, reader-detected at layer access.

Generation-2 geometry (computed, not estimated):

```
F = 640;  layer a: tiles [16,40), index [40,104)
          layer b: tile [320,324), index [324,348)
          directory [348,547) = 199 bytes;  pad [547,576) = 29;  trailer [576,640)
```

Complete-walk claimed (if `b` were valid) = 16 + 24 + 64 + 4 + 24 + 199 + 64 =
**395**; true slack = 640 − 395 = **245** (g1's directory 102 + g1 pad 50 +
g1 trailer 64 + g2 pad 29 = 245 ✓).

With `b` rejected, §5.2 governs: *"a rejected layer's claimants are not
enumerated, whether or not the rejection impeded reading them"*. I noted that
this is normatively "not enumerated", not "may be enumerated if readable" — that
matters, because a verifier that *could* read `b`'s index would otherwise
produce a tighter total that is no longer an upper bound. Enumerated claimants =
16 + 24 + 64 + 199 + 64 = 367.

**Partial total = F − enumerated = 640 − 367 = 273.** True slack 245.
273 ≥ 245 ✓ — an upper bound, *"never an under-count"*, as `[R-CNT-21]` requires.
The verifier must *"say which scope or violation stopped the walk"*: **layer `b`,
L33, `[R-GEO-05]`**. Verdict: **nonconforming**.

I also checked the L18/L40–L42 sub-case: when the rejection is one *the walk
itself established*, §5.2 says *"the claimants it had already enumerated are
discarded with the layer"*. Discarding only ever raises the total, so the upper
bound survives there too. And because "the bytes claimed" is a **set**, not a sum
of lengths, an overlapping-claimant file cannot drive the total negative.

### 3.5 Which partial triggers are exhaustive

§5.2 gives two: a scope-level rejection ending that scope's enumeration, or an
elective stop at the first violation. I tested three cases against that list:

- **Tile-scope rejection** (T1, T14): does *not* make the walk partial. §9.7 says
  so for structural entries (*"does not make the walk incomplete"*), and for the
  others the extent stands and is enumerated. ✓
- **A declined decode on resource grounds** (verdict *cannot establish*): neither
  trigger applies; the extent is still enumerated. Total is **complete**. ✓
- **An unimplemented MU = 1 record** (verdict *cannot establish*): §3.1 above —
  the closed claimant list means the walk still completes. Total **complete**. ✓

All three determinate.

---

## 4. Extent overlap, alignment, and slab — on an adversarial layout

Layer `s`: rank 1, `x` E = 40, T = 4 → G = N = 10; interleaved, one `uint8`
channel, fill `00`; P = 4, Q = 1, decoded size 4; codec 1, filter 1; **S = 4,
A_slab = 64**, A = 0 (mutually exclusive per `[R-CNT-16]`/L20).

Runs, per `[R-SLB-02]`: the single block [0, 10) partitions into run 0 = [0, 4),
run 1 = [4, 8), run 2 = [8, 10) — *"the final run of a block can cover fewer
than S ordinals"*. Stored: 0, 1, 3, 4, 5, 6, 7, 8; ordinals 2 and 9 sentinel.

Clean layout:

```
[0,16)   front            [64,76)   run 0: t0@64 t1@68 t3@72
[128,144) run 1: t4@128 t5@132 t6@136 t7@140
[192,196) run 2: t8@192
[256,460) index region (10·20 + 4 = 204)
[460,561) directory (101)   [561,576) pad   [576,640) trailer   F = 640
```

Claimed = 16 + 8·4 + 204 + 101 + 64 = 417; slack = 640 − 417 = **223**, and
enumerating the gaps by hand: [16,64) 48 + [76,128) 52 + [144,192) 48 +
[196,256) 60 + [561,576) 15 = 223 ✓.

Invariants I checked on this layout:

- **A_slab**: offsets 64, 128, 192 are all ≡ 0 mod 64 ✓ (L42).
- **Packing**: within run 0, sentinel ordinal 2 is transparent
  (*"Sentinel tiles are transparent to run continuity: they occupy no bytes and
  do not break packing"*), so the relation is offset(3) = offset(1) + length(1)
  = 68 + 4 = 72 ✓ (L41).
- **Run 2 imposes only alignment** — one stored tile, nothing to pack.

Adversarial mutations and the row each yields:

| Mutation | Row | Outcome |
|---|---|---|
| offset(3) = 73 | L41 (gap) | reject-layer, verifier |
| offset(4) = 130 | L42 | reject-layer, verifier |
| offset(8) = 140 (into t7) | L18 **and** L42 | reject-layer, verifier |
| offset(0) = 460 (into the directory) | **F33** | reject-**file**, verifier |
| tile 8 length = 8 | T14 first (`[R-COD-04]`, *"checkable from the entry and the layer record alone, before any payload fetch"*) | reject-tile, reader |

The last row is the one worth stating: under codec 1, an oversize extent is
caught as a tile-scope reader violation *before* it can present as an overlap,
because `[R-COD-04]`'s equality is a pre-fetch check. Two rows fire in the
overlap-into-t7 case and both are reject-layer, so no verdict forks.

**Scope routing for overlap.** `[R-CNT-13]` partitions it three ways —
intra-layer (including a stored extent against its own layer's index region or
sub-record extents) → reject-layer (L18); across layers or against another
scope's structures → reject-file; two non-layer structures → reject-file (F33).
I checked F33's claim that *"a claimant reaching the front signature block or the
live trailer is instead caught by the bounds rows F9/F10, F31/F32, L16/L17 and
T8/T9, each at its own tier"* against every claimant class:

- directory → F9 (dir_offset < 16), F10 (past F − 64) ✓
- non-layer top-level record extent → F31 (offset 1–15; offset 0 with nonzero
  length is F30), F32 ✓
- layer record and sub-record extents → L16, L17 ✓
- stored-tile extents → T8, T9 ✓

Complete. Consequently every *enumerated* claimant lies in [16, F − 64), which is
what makes the walk's disjointness check and the slack subtraction well-founded.

**Planar slab check.** With C = 2, N = 3, S = 2, A_slab = 16: blocks [0,3) and
[3,6); runs [0,2), [2,3), [3,5), [5,6). `[R-SLB-02]`'s *"runs never span channel
blocks"* means ordinals 2 and 3 need not be contiguous — I confirmed that a
verifier must not join them, and that `[R-SLB-05]` governs the space between.

**Stale slab declarations** (`[R-SLB-04]`) need no separate check: §16.2's Note
is right that every file exhibiting one exhibits L41 or L42.

---

## 5. Checksum obligations

### 5.1 Which structure is covered by which checksum

§8.1's map, and I verified the chain closes: entry bytes ← segment CRC ← segment
CRC array ← crc_of_crc_array (a layer-record field) ← directory CRC ← (nothing;
terminal, comparison-verified). Stored tile ← its entry's crc ← segment CRC.
Trailer ← itself. §4.5's classification of *interior* checksum fields (segment
CRC arrays, entry crc fields, crc_of_crc_array) as *"both comparison-verified and
covered by exactly one further checksum"* checks out against the map in each
case.

**Is every live structure covered?** No — tier C of §3.2: *"Extent of a record of
a type this specification has not assigned | none — the bytes are opaque
(§7.2)"*. For format major 1 the only assigned types are 0x0001 and 0x0002, and
both their extents are covered, so the map is complete for this major.

### 5.2 Constants I reproduced

I implemented CRC-32C from §4.5's parameters alone — polynomial 0x1EDC6F41,
reflected in and out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF — reflecting the
polynomial myself to 0x82F63B78. Reproduced, all bit-exact:

| Constant | Stated | Computed |
|---|---|---|
| CRC-32C(`"123456789"`) §4.5 | 0xE3069283 | **0xE3069283** ✓ |
| CRC-32C(zero bytes) §4.5 | 0x00000000 | **0x00000000** ✓ |
| §7.4 example: CRC over 4 sentinel entries (80 B) | 0x80A34955, stored `55 49 A3 80` | **0x80A34955** ✓ |
| §7.4 example: crc_of_crc_array | 0xC4EE982E, stored `2E 98 EE C4` | **0xC4EE982E** ✓ |
| §15.4 / Appendix B: full all-sentinel segment (2¹⁶ entries) | 0xEECB3BB2 | **0xEECB3BB2** ✓ |
| Appendix A: trailer CRC over [0, 60) | 0xE00938D2, stored `D2 38 09 E0` | **0xE00938D2** ✓ |
| §17.2 / Appendix B: zstd frame magic 0xFD2FB528 → LE bytes | `28 B5 2F FD` | **`28 B5 2F FD`** ✓ |

The fact that my independently-reflected polynomial reproduces the check vector
is itself the confirmation §4.5 asks for: *"An implementation whose checksum
function does not reproduce these values does not implement this
specification's checksum."*

I also rebuilt §7.4's worked layer-record payload from the field table alone and
got 81 bytes, byte-identical to the dump, with every stated offset matching
(name 0, layout 4, linearization 5, codec 7, filter 9, A 11, S 19, A_slab 27,
rank 35, C 36, dimension entry 38, channel entry 56, fill 63, index_encoding 68,
entry_count 69, crc_of_crc_array 77) and `[R-CNT-17]`'s extent length
4·20 + ⌈4/2¹⁶⌉·4 = 84.

And the other worked examples: §14.2's interleaved offsets (Q = 3, decoded 18,
ordinal 5 at bytes 15–17); §14.3's packed bool tile (`55 01` fill-false,
`55 FD` fill-true); §14.5's edge tile (32 bytes, 1 real + 15 padding);
§15.4's 1,000,000-entry layer (16 segments, 64-byte array, region 20,000,064,
segment 15 at [19,660,800, 20,000,000), tile 999,999 at segment-relative
339,180); §15.4's planar example (disk ordinal 74, entry bytes [1,480, 1,500));
§17.3's byte-shuffle (`00 00 00 00 00 00 80 00 40 3F 40 40`); §20.3's 32-tile
index region 32·20 + 4 = 644; §5.1's 128-byte minimum (44 bytes of slack).
**All reproduce.**

### 5.3 Constants I could not reproduce

- **0x7E000000**, the lz4 decoded-size cap (§17.2, `[R-COD-07]`). It is a pinned
  external-format interoperability bound; verifying it would require the LZ4
  Block Format document, which I may not consult. I confirmed only that
  0x7E000000 = 2,113,929,216 and that it is representable and comparable
  against `P·Q`, `P·Bᶜ`, and `⌈P/8⌉` as L44 requires.
- **§21.9's minimum guarantees** (rank 32, C 4096, 2³² entries, 65,536 layers,
  16 MiB directory, 256 MiB tile, 16 MiB document, 8 MiB zstd window). These are
  chosen numbers, not derived ones; §21.9's Note explains the derivation of each
  and I checked the internal one that is checkable — 2³² entries × 4 bytes of
  segment CRC per 2¹⁶ entries = 2¹⁶ × 4 = 256 KiB ✓, and 2³⁶ entries → 4 MiB ✓,
  exactly as the Note claims.
- **RFC 1951 / RFC 8878 / RFC 8259 / RFC 3339 conformance** of my decode paths.
  Out of reach and out of charter.

### 5.4 Register arithmetic

I extracted every register row mechanically and counted its Instances cell by
semicolons, with `—` counting as one:

| Subsection | Rows stated | Rows counted | Instances |
|---|---|---|---|
| §21.2 | 36 | **36** | 58 |
| §21.3 | 49 | **49** | 116 |
| §21.4 | 26 | **26** | 57 |
| §21.5 | 10 | **10** | 44 |
| §21.8 | 121 / 275 | **121** | **275** |

Exact. I then re-derived a sample of cells from §21.1's criterion rather than
trusting them, since the brief warned that this is a rule that has been rewritten
before:

- one-directional comparisons → no direction axis: T21 (*"larger than"*) = 3
  layouts; L44 (*"exceeds"*) = 3; F5 (*"below"*) = 2 fields, not 2 directions ✓
- two-magnitude comparisons → two directions: T3, T14, T22 (*"is not exactly"*,
  *"differs from"*, *"does not equal"*) = 2 × 3 layouts = 6 each; L21 = 2 × 2
  layouts = 4; L30, F17 = 2 each ✓
- checksum/constant comparisons → no direction: F14, L37, L38, T1 = 1 each ✓
- nonzero tests → not comparisons: L20, L27, L28 = 1 each ✓
- single predicate over several fields → 1: F10, F32, T12 ✓
- container axes: L15 (2 halves × 2 containers) = 4 against F30 (2 halves × 1) =
  2; L16/L17 = 2 each against F31/F32 = 1 each; L49 (2 bits × 2 containers) = 4
  against F28 = 2; R4 (6 constraints × 2) = 12; R7 (3 × 2) = 6; R5 (2 × 2 × 2) = 8 ✓

Every cell I re-derived matched. I also confirmed mechanically that Detector =
*verifier* ⟺ Detected = *certification* across all 121 rows (20 verifier rows:
F7 F25 F26 F27 F28 F33 F36 L18 L25 L40 L41 L42 L46 L47 L48 L49 T2 T4 T5 T26) —
zero mismatches. §21.1's claim that detection points *"name §19.2's reader tiers
— open, layer access, tile use, extent use — or *certification*"* holds with one
row using a compound cell (R1: "open (top-level); layer access (sub-record)"),
which is correct for a rule that fires at two scopes.

I make no finding on the register arithmetic. It is clean.

---

## 6. Decoded-content obligations

**What must be decoded.** §9.7 is unambiguous: *"A verifier decodes every stored
tile, whatever content obligations §14 places on the layer: §21.4's codec rows
are file-conformance violations, and a verifier MUST NOT certify past a
violation it has not looked for."* So a layer with no padding positions, no pad
bits and no bool channel — where T2/T4/T5 cannot fire — must still have every
tile decoded, because T3, T15–T25 can.

**What it compares against.**

| Check | Compared against | Row |
|---|---|---|
| decoded length | P·Q / P·Bᶜ / ⌈P/8⌉, from declarations alone | T3 |
| codec-1 stored length | same, pre-fetch | T14 |
| every padding position | that channel's recorded fill bytes | T4 |
| every pad bit (P mod 8 ≠ 0) | the plane's channel's fill bit | T5 |
| every interleaved bool byte at a **real** position | {0x00, 0x01} | T2 |
| filter stride | element size / Q / identity | T26 |
| frame/stream/block shape | §17.2's per-codec rules | T15–T25 |

I checked the T2/T4 partition, since both cover interleaved bool bytes. T2's row
says *"the same byte at a padding position is T4's, the two rows together
covering `[R-SER-08]`"*. That is exact: a bool fill byte is constrained to
0x00/0x01 by `[R-TYP-07]` (and L35 catches any other at layer scope, reader-
detected, before any tile is reached), so a padding position's bool byte outside
{0x00, 0x01} necessarily differs from fill and is T4. No byte falls between the
two rows and none is double-counted in a way that forks a scope — both are
verifier/tile-scope.

**What it is permitted to skip.**

1. **Slack content** — §9.7: *"their content is not its concern."*
2. **Tier C bytes** — an unassigned record type's extent (§8.1, §7.2).
3. **Tier B bytes** — a user-metadata document under an unassigned encoding;
   `[R-MTA-10]` says explicitly *"A verifier meeting such a record in an
   otherwise conforming file has no requirement it is unable to check"* — so it
   is a skip that does **not** cost certification, unlike every other skip.
4. **§21.7's undetectables** — wrong sample data, an undisclosed zstd
   dictionary, a mis-strided filter with no structurally-constrained byte:
   *"no file-level witness exists to check, so nothing about the file is left
   undetermined and the verdict is unaffected."* This is the right disposition
   and I want to record that I checked it, because it is the one place where
   "cannot check" must **not** become *cannot establish*.
5. **A tile whose entry crc failed** — §8.2's chain bars acting on unverified
   bytes, so the verifier does not decode it. The verdict is *nonconforming*
   from T1 regardless, and the unchecked codec rows are **not** reportable as
   cannot-establish grounds, because a CRC failure is neither a capability nor a
   resource ground. Determinate, and I relied on it.

**What forces cannot-establish.** Only a *declined* decode: `[R-ERR-04]` lets a
verifier decline *"at the whole file, or at the narrowest scope whose
declarations exceed what it can serve, a layer or a tile"*, and §2.3 turns that
into cannot-establish, with `[R-ERR-04]`'s further requirement that the refusal
*"MUST be reported as a resource limit and not as a validity error."* Same for a
metadata document over the verifier's bound (`[R-MTA-09]`), which additionally
SHOULD report *"the bound it applied and the stored length of the extent it
declined."*

I note without filing it that this makes the verdict **verifier-relative**: a
verifier with a 16 MiB document bound reports *cannot establish* on a file that
a verifier with a 64 MiB bound certifies. `[R-MTA-09]` says this in terms —
*"the bound is that verifier's capability and not a limit on validity"* — and
cannot-establish is by construction not a claim about the bytes. Designed, not
defective.

---

## 7. The multi-generation trace

All four generations built byte-exactly and verified with my own CRC
implementation. Layer `a` as in §3.3; layer `b` as in §3.4 but with a **valid**
linearization this time.

| Gen | Operation | F | Live state | Slack | Verdict |
|---|---|---|---|---|---|
| 1 | create (layer `a`, 3 tiles) | 320 | 270 | **50** | conforming |
| 2 | append (add layer `b`) | 640 | 395 | **245** | conforming |
| 3 | update (supersede `a`'s tile 1) | 1024 | 395 | **629** | conforming |
| 4 | **compact** | 448 | 395 | **53** | conforming |

Each step, checked rather than asserted:

**g1 → g2.** Writing begins at exactly F = 320 (`[R-LIF-02]` step 1). New
payload and index for `b`; complete new directory re-emitting `a`'s record
**byte-identically, extent slot and all** (`[R-WRT-05]`) — so `a`'s index region
still sits at [40, 104) and never moved, which is §5.1's *"a layer the commit
does not touch keeps its extent slot pointing where it always pointed"*. Slack
added = g1's directory 102 + g1 pad 50 + g1 trailer 64 + g2 pad 29 = 245 ✓
(matches the walk exactly). Generation 2, same file_id.

**g2 → g3.** A supersede. `[R-WRT-04]` step 4 forces `a`'s **whole** index region
to be re-emitted *"necessarily at a new placement (`[R-LIF-01]`)"* — 64 bytes for
one changed entry, with 2 of 3 entries byte-identical at their disk-ordinal
positions. New slack = old tile 1 (8) + old index (64) + g2 directory (199) +
g2 pad (29) + g2 trailer (64) + g3 pad (49) = 413; 245 + 413 = 658... which is
**not** 629, so I recomputed by hand and found my error: g2's pad is 29 and g3's
is 49, and 245 + 8 + 64 + 199 + 29 + 64 + 49 = 658 double-counts g2's pad, which
was already inside the 245. The correct decomposition is
245 (carried) + 8 + 64 + 199 + 64 + 49 = **629** ✓, matching the walk. Recording
the slip because the transcript is meant to be checkable: the pre-trailer pad of
generation *n* becomes slack at generation *n*, not at generation *n*+1.

At this point slack is 629/1024 = 61% of the file. §20.3's Note and §22.3 both
name this as the number that tells an operator to compact.

**g3 → g4, compaction.** Per `[R-WRT-07]`: every stored tile's bytes verbatim;
every index entry's **crc unchanged** (I verified: 0x3230878B, 0x314AB23F,
0x3CA573AB for `a`; 0x8B303ACA for `b` — identical across g3 and g4); entry
offsets new; segment CRCs recomputed over the entries as re-emitted;
crc_of_crc_array updated in each layer record. Fresh file_id, generation 1
(`[R-WRT-06]`: *"a new draw under §9.3's randomness advice, not merely a value
compared against the input's"*). Unknown ignore-lane bits carried forward;
version_minor = max(floor, input's).

The invariant that made the trace worth doing: **live state is 395 bytes at
generations 2, 3 and 4.** Compaction changed placement and nothing else, and
`[R-WRT-07]`'s *"The output's reference arrays MUST equal the live generation's
bit for bit"* is satisfied by construction because every tile's bytes and every
entry's crc are preserved. Slack falls 629 → 53, and 53 is exactly the new
pre-trailer pad — the irreducible floor.

I also confirmed the output satisfies `[R-CNT-05]`: directory ends at 331,
trailer begins at 384, and nothing occupies [331, 384) (F7 clear).

**A wrinkle I checked at g3.** §20.4's MU = 0 / PE = 0 row says an appender may
drop such a record only in a commit that *independently* changes the scope the
record attaches to, and that *"Superseding a stored tile's bytes is not such a
change for either kind"*. My g3 is precisely a supersede-only commit, so had
layer `a` carried an MU = 0 / PE = 0 sub-record it would have had to be retained.
Determinate and stated.

---

## 8. Findings

### verifier-01 — AMBIGUITY — whether `[R-ENC-04]`'s 2⁶³−1 ceiling reaches P·Q and P·Bᶜ in a layer that addresses no tile

**Location:** §14.2 `[R-SER-02]`, §14.3 `[R-SER-07]`, §4.2 `[R-ENC-04]`,
§11.1 `[R-GEO-02]`, §21.3 L2; the only explicit resolution is §17.2's **Note**.

**Quotation** (§17.2, inside a `> **Note.**` block, therefore non-normative
under `[R-CNF-01]`):

> `[R-ENC-04]`'s overflow rule carries no such quantifier — it binds any sum or
> product a file yields — so P·Q and P·Bᶜ are checked in an empty layer even
> though this cap is not.

**The two readings.**

*Reading A (checked).* `[R-ENC-04]` binds *"any quantity this specification
defines as a sum or product of integers obtained from a file"*. §14.2 closes
with *"These products and sums are declaration-derived quantities under
`[R-ENC-04]`"* and §14.3 with *"Every decoded size, and the value count V, is a
declaration-derived quantity under `[R-ENC-04]`"*. A layer with a zero extent
still declares every input — P = ∏Tᵢ (§11.2, unconditional), Q = ΣBᵢ (§14.2,
unconditional) — so P·Q is declaration-derived and is checked. L2's condition
reads *"A declaration-derived sum or product **of a layer**"* and lists P·Q and
P·Bᶜ among its instances.

*Reading B (not checked).* §14.2's table defines P·Q as *"the decoded tile
image's byte length"* — a property of **a tile**. §11.1 says *"at Eᵢ = 0 the grid
count is 0 and the layer addresses no tile"* and `[R-GEO-02]` that such a layer
has *"zero addressed tiles, its tile index has zero entries, and its reference
array is empty"*. No tile exists, so no decoded size is defined, so there is no
"quantity this specification defines" to overflow. "Declaration-derived" is then
read as contrasting with *payload*-derived — which is what §14.2 and §22.2 use it
for (*"readers allocate from those declarations, not from stored data"*) — not as
asserting that the quantity exists absent tiles. §19.3's enumeration of what
layer access validates cites `[R-GEO-01]`–`[R-GEO-03]` for *"the geometry floor
and its arithmetic"* and cites neither `[R-ENC-04]` nor `[R-SER-02]`/`[R-SER-07]`;
`[R-GEO-03]` covers N, P, C·N and N·P — all of which are 0 or in domain here —
and not P·Q.

**Which I picked and why.** Reading A. The §17.2 Note settles the author's
intent beyond doubt, L2 says *"of a layer"*, and the contrast the Note draws
against `[R-COD-07]`'s addressed-tile quantifier is a real and deliberate
distinction — §20.3 step 4 restates half of it normatively (*"which an empty
layer escapes only because that cap is quantified over addressed tiles"*). But
the half that decides *this* question is stated in exactly one place and that
place is a Note.

**Witness file (constructed and built).** One layer, rank 1, one channel:

- name `z`, layout 1 (interleaved), linearization 1, codec 1, filter 1,
  A = S = A_slab = 0, rank 1, C = 1
- dimension `t`: E = 0, T = 2⁶² = 4,611,686,018,427,387,904
- channel `w`: type 13 (float64, Bᶜ = 8), fill 8 zero bytes
- index_encoding 1, entry_count 0, crc_of_crc_array 0, no sub-records
- inline_length 80, record 104 bytes, dir_length 108, dir_offset 16,
  pad [124, 128) = 4, trailer [128, 192), **F = 192**

Every other derived quantity is in domain, which is what makes the witness
clean: G = ⌈0/2⁶²⌉ = 0, N = 0, C·N = 0, N·P = 0, entry_count = 0 (so extent slot
(0,0) and crc_of_crc_array 0 are both correct per `[R-CNT-23]`), P = 2⁶² ≤ 2⁶³−1,
V = P·C = 2⁶² ≤ 2⁶³−1. The **only** overflowing quantity is
**P·Q = 2⁶² × 8 = 2⁶⁵ = 36,893,488,147,419,103,232 > 2⁶³ − 1**.

Coverage walk: claimed = 16 + 108 + 64 = 188, slack = 192 − 188 = 4.

**What an implementer does wrong without it.** Verifier A reports
**nonconforming** (L2, reject-layer, `[R-ENC-04]`). Verifier B **certifies**,
reporting slack 4. Same 192 bytes, opposite certificates. A writer targeting
Reading B may publish this file as conforming; a downstream verifier under
Reading A refuses it. §21.9 offers no escape: the "decoded size of one tile"
row is a *minimum guarantee*, and `[R-ERR-04]` says *"A file exceeding any of
these remains conforming"*, so a large decoded size is not by itself a defect —
the 2⁶³−1 ceiling is the only thing that could make it one. A third verifier may
decline the layer on resource grounds and report *cannot establish*, but that is
a licensed capability outcome and not what the fork is about.

**Byte-level: yes.** Two competent verifiers reading only the normative text
disagree about accept/reject on the 192 bytes above.

---

### verifier-02 — CONTRADICTION — §21.7's account of where §20.3 step 4's bar is witnessed is refuted by §21.4's own rows

**Location:** §21.7 `[R-ERR-01]`; §20.3 step 4 `[R-WRT-04]`; §21.4 rows T14, T17,
T3, T24, T25.

**Quotation** (§21.7, normative — not in a Note/Example/Rationale block):

> §20.3 step 4's bar on a declaration change is witnessed only where the
> affected tiles remain stored *and* the change reaches a byte §14
> structurally constrains — a padding position, a pad bit, or a boolean
> byte — the §21.4 rows firing there and nowhere else

**The rule it describes** (§20.3 step 4, normative):

> A commit MUST NOT change a layer's declarations in a way that alters, for any
> tile that layer stores **in the generation this commit supersedes**, what §14
> fixes for its stored bytes or how they decode — the set of padding positions
> (§11.3) and the content `[R-SER-05]` fixes there, the decoded size, the byte
> offset of any sample within the decoded tile image, or the codec and filter
> that produced the stored bytes.

**Why the "only … and nowhere else" is false.** The bar's list has five limbs.
For limbs 1, 2 and 4 (padding-position set, padding content, in-sample byte
offset) §21.7 is right: the witnesses are T4, T5, T2. For limbs 3 and 5 they are
not, and the change does not reach any byte §14 structurally constrains — the
stored bytes are untouched; only the declarations move.

*Limb 5 (codec/filter).* Layer with codec 1, every tile stored raw. A commit
changes codec to 3. The live state now declares zstd over raw stored bytes, and
**T17** fires — *"Codec 3 (zstd) and the stored bytes do not begin with the
compressed-frame magic 28 B5 2F FD"* — reject-tile, detector **reader**, at tile
use. Not a padding position, not a pad bit, not a boolean byte. T24 and T25 fire
for the same class of change in the other direction.

*Limb 3 (decoded size).* Constructed: rank 1, E = 4, T = 4, one `uint8` channel,
interleaved, codec 1 → G = ⌈4/4⌉ = 1, entry_count = 1, P = 4, Q = 1, decoded
size 4; one 4-byte tile stored. A commit changes T to 5: G = ⌈4/5⌉ = 1 still, so
entry_count is unchanged and `[R-CNT-17]` is satisfied without even re-emitting
the index. But P becomes 5 and the decoded size becomes 5, while the stored
entry's length is 4. **T14** fires — *"Codec 1 (none) declared and a
non-sentinel index entry's length differs from the tile's decoded size"* —
checkable, per `[R-COD-04]`, *"before any payload fetch"*, so T4 is never even
reached. Under a compressing codec the same change is witnessed by **T3**.

So the conjunctive necessary condition §21.7 states ("*and* the change reaches a
byte §14 structurally constrains") is false, and so is "the §21.4 rows firing
there and nowhere else".

**What an implementer does wrong without it.** Nothing, in the accept/reject
sense — which is why I do not claim this is byte-level. The verifier's
obligations for T14, T17, T3, T24 and T25 come from §21.4 and their governing
rules directly, and §21.1 says the register's rows carry the obligations while
*"§21.7's account of what no check detects"* carries none. What goes wrong is
the reader's model: §21.7 is the section an implementer consults to learn what a
certificate does *not* prove, and it currently tells them that a codec swap over
retained tiles produces no witness, when in fact it produces a loud one. It also
weakens §21.1's normative completeness argument, which turns on knowing exactly
which obligations have no witness.

**Byte-level: no.**

---

### verifier-03 — OBSERVATION — §20.5 asserts a compactor was already obliged to refuse on a structurally-invalid index entry, by a citation chain that does not contain the check

**Location:** §20.5 `[R-WRT-07]`, citing `[R-WRT-06]`, which triggers on
`[R-WRT-09]`.

**Quotation** (§20.5, `[R-WRT-07]`):

> an entry §15.3 classifies reject-tile on a structural ground never reaches
> this step, `[R-WRT-06]` having obliged the compactor to refuse

**Why the chain does not close.** `[R-WRT-06]`'s trigger is *"A compactor MUST
refuse to compact when any check `[R-WRT-09]` obliges fails"*. `[R-WRT-09]`
enumerates: *"the open (§19.1), each retained layer's record (§19.3) and full
index chain (`[R-IDX-04]`), and each relocated extent's checksum, including
every stored tile's entry crc"*. Take T6 — a sentinel-shaped entry with crc ≠ 0.
Trace it:

- §19.1's open touches trailer and directory only (`[R-RDR-01]`) — miss.
- §19.3's layer validation reaches *"the index cross-checks computable without
  I/O (`[R-CNT-17]`)"*, i.e. entry_count against geometry and extent_length
  against the formula — miss.
- `[R-IDX-04]` is crc_of_crc_array and the segment CRCs, both of which **pass**
  (the entry's bytes are exactly as stored) — miss.
- *"each relocated extent's checksum"*: a T6 entry addresses **no usable
  extent** (§15.3 says structural rows *"classify an entry whose own 20 bytes
  yield no usable extent"*), so there is no extent to relocate and no crc to
  verify — miss.

Entry classification is `[R-IDX-03]`, and `[R-IDX-03]` is not among
`[R-WRT-09]`'s citations. §19.4 does classify, at step 4 — but `[R-WRT-03]`
imports only *"the §19.4 index chain for every segment whose entries the commit
reuses"*, and §19.4's step 3 is the one labelled "Index chain"; step 4 is
"Entry", separately.

**Why the conclusion nonetheless holds, and why it took work.** §20.5's second
sentence of `[R-WRT-06]` is the operative one: *"MUST NOT emit a file carrying a
violation it has detected"*. A compactor regenerating an index region must
compute a new offset for every stored entry, and a T6 entry has no offset to
renew — it necessarily meets the anomaly and, having met it, may not emit it. So
the answer is refuse, as `[R-WRT-07]` says.

I record this as expensive-to-decide rather than undecided, and I want to note
why it is not a `[R-CNF-05]` argument: §20.3 step 2 explicitly forecloses that
route for appenders — *"Reproducing a structure's bytes unchanged is not
authoring them"* — and §20.5 explicitly admits that *"a violation latent in a
structure it carries forward verbatim travels into its output (`[R-WRT-01]`)"*.
So the "the output must be conforming, therefore refuse" argument is not
available, and the whole weight falls on "detected". Naming `[R-IDX-03]` in
`[R-WRT-09]`'s list would close it in one word.

**Byte-level: no.** Both readings end in a refusal, and the input file is
nonconforming either way, so no verifier verdict and no emitted byte sequence
differs.

---

### verifier-04 — OBSERVATION — a duplicated conjunct in `[R-WRT-06]`

**Location:** §20.5 `[R-WRT-06]`.

**Quotation:**

> it can neither re-emit the structure corrected (`[R-WRT-05]`), nor keep it and
> call the output clean — and a record §20.4 does let it drop is no exception,
> dropping being available only where that table licenses it — nor re-emit it
> corrected (`[R-WRT-05]`).

The first and third conjuncts of the `neither … nor … nor` are the same
proposition with the same citation: "re-emit the structure corrected
(`[R-WRT-05]`)" and "re-emit it corrected (`[R-WRT-05]`)". The sentence reads as
a three-item exhaustion of a compactor's options and is in fact a two-item one
with the first item repeated after the em-dash aside.

I report it because it is a repair artifact in normative text in a section this
round was asked to read, and because a reader counting the options a compactor
has will look for a third that is not there. It changes no obligation.

**Byte-level: no.**

---

### verifier-05 — AMBIGUITY — whether a verifier must detect and report SHOULD deviations, or merely classify the ones it happens to notice

**Location:** §2.4 `[R-CNF-12]`, against §2.3 `[R-CNF-11]`'s definition of the
class.

**Quotation** (§2.4, `[R-CNF-12]`):

> Deviation from a SHOULD is not a violation for this purpose: §21's register
> enumerates MUST-level conditions only, and a verifier reports a SHOULD
> deviation as an advisory that does not bar certification.

**The two readings.**

*Reading A (obligation).* §2.3 defines a conforming verifier as *"A reader that
additionally checks **every file-level requirement** — including those ordinary
readers are exempted from"*, and under BCP 14 (§2.1) a SHOULD is a requirement.
So a verifier must check every file-level SHOULD and emit an advisory for each
deviation. Checkable ones I enumerated: `[R-ENC-14]` (names in NFC — requires
running Unicode normalization over every layer, dimension and channel name and
comparing), `[R-CNT-26]` (version_minor at the floor), `[R-CNT-09]`
(dir_length + pad + 64 within 65,536), `[R-COD-06]` (declared zstd window within
8 MiB), `[R-MTA-04]` (no JSON number binary64 cannot represent exactly).

*Reading B (classification).* The sentence's subject and purpose are the
"does not bar certification" clause; "reports … as an advisory" says what
category such a report falls in, not that the report is owed. A verifier that
checks no SHOULD is still conforming, since §21's register — the thing §2.3's
"checks every file-level requirement" is operationalised by throughout §19 and
§21.1 — *"enumerates MUST-level conditions only"*.

**Which I picked and why.** Reading B, and I emit advisories only for the SHOULDs
I check incidentally. The register is the document's own operationalisation of a
verifier's check list (§19's preamble: *"§21's register is"* the complete
inventory; §21.1: its *"completeness is normative"*), and it deliberately
excludes SHOULDs. Reading A would also put a verifier to work on Unicode
normalization, which nothing else in the document contemplates.

**One instance that resolves itself, and is worth recording**, because I first
took it for a contradiction: `[R-CNT-03]`'s *"Writers SHOULD zero the gaps they
create"* cannot be an advisory a verifier owes, because §9.7 says of slack
*"their content is not its concern"* and §5.2 that *"A reader MUST NOT interpret
it"*. So the document does close that case — it just closes it somewhere other
than `[R-CNF-12]`. The general question stands for the five checkable SHOULDs
above.

**What an implementer does wrong without it.** Two verifiers certify the same
file and hand back different advisory sets — one silent, one reporting a
decomposed name and an over-floor version_minor. Both certify. A pipeline that
gates on "no advisories" gets different answers from different tools while both
report *conforming*.

**Byte-level: no.** No verdict and no emitted byte sequence turns on it;
`[R-CNF-12]` says outright that a SHOULD deviation *"does not bar
certification"*.

---

## 9. Things I checked and did not file

Recording these so the next round does not re-walk them.

- **F5's position in the validation order** (§21.2 preamble vs `[R-CNT-27]`).
  Decidable, and unreachable in isolation: F must be a multiple of 64 to pass
  F13, and F = 64 is barred by F10 (dir_offset ≥ 16 and
  dir_offset + dir_length ≤ 0 are unsatisfiable). §24 `[R-VEC-02]` already
  covers non-isolable conditions.
- **Whether a verifier owes the slack total when the verdict is *cannot
  establish***. Yes if a live state was reached, and **complete** (not partial),
  because §5.2's two partial triggers — scope-level rejection, elective stop at
  a violation — are exhaustive and neither is a declined decode.
- **Whether an unimplemented MU = 1 record makes the walk partial.** No.
  `[R-CNT-02]`'s claimant list is closed on extent slots; anything else such a
  type references is slack by definition. §3.1 above.
- **Whether a codec-reason reject-tile entry (T14/T17/T24) is transparent to
  slab run continuity or drops out of the walk.** Neither — it is not among
  §15.3's six *structural* rows, so the general rules apply: its extent is a
  claimant and its offset/length stand in the packing relation.
- **F33's claim that every claimant reaching the front block or trailer is
  caught by a bounds row.** Verified against all four claimant classes (§4).
- **§21.1's "`[R-SER-08]` is the one rule that goes the other way".** True among
  the 20 verifier rows: it is the only one that resolves a byte to a value
  rather than serving it through or ignoring it. The neighbouring *"for several
  such rows"* does not name `[R-CNT-12]`'s reserved-flag rows, which also oblige
  the reader to serve the record unchanged — but "several" is not an enumeration
  claim, so I did not file it.
- **The whole `[R-MTA-10]` / R1 / §21.6 seam** (unassigned vs experimental vs
  reserved vs 0 metadata encodings). Fully determined, stated three times
  consistently (§18.2, §21.5 preamble, Appendix H), including the non-obvious
  part — that `[R-MTA-10]` withdraws content rules but not the encoding byte's
  own value set.
- **Register arithmetic** — 121 rows, 275 instances, detector/tier consistency,
  and a sampled re-derivation of the instance criterion. Clean (§5.4).
- **All seven computable constants and all nine worked examples.** Reproduced
  bit-exactly (§5.2).
- **Appendix G.** Non-normative and out of my charter, but I read it for
  contradictions against §5.2/§9.7 and found none: item 3's "first structure
  begins at 16" is consistent with `[R-CNT-02]` counting the front block as no
  structure, and item 3's contiguous emission automatically satisfies
  `[R-SLB-03]`'s packing while leaving only run-start alignment gaps.

## 10. Confidence

**Medium-high.** I built the verifier end to end and the document carried me
through every step but one. The certification procedure, the verdict lattice,
the coverage walk (including both the complete and the partial arithmetic), the
overlap scope routing, the slab and alignment invariants, the checksum map, the
decode obligations, and the four-generation trace are all fully determined by
normative text, and the arithmetic and constants all reproduce. The single place
where I believe two conforming verifiers would hand back opposite certificates
on the same bytes is verifier-01.
