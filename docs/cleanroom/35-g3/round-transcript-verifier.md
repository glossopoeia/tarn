# Cleanroom round 35 — Verifier implementer, working transcript

## 0. Access and disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,864 lines). It was where the brief said it would be. I opened no ADR, no
`docs/`, no `conformance/`, no `registry.json`, no git history, no web. I ran no
`git` command of any kind. I listed no directory other than my own scratch
directory (which was empty when I began — no previous attempt's files were
present).

Context I did not ask for **did** appear before I began: the runtime placed a
project instruction file (`CLAUDE.md`, which redirects to `AGENTS.md`) and an
index of the maintainer's memory notes into my context, the latter listing
titles that plainly concern this project's harness, its repair history, and its
gate mechanics. I did not read the files behind those titles and I have not
used any of it. I name its appearance here because the brief requires it; I do
not repeat its contents. Nothing in my findings derives from it — every claim
below is anchored to a quotation from `spec/tarn.md` and to arithmetic I ran
myself.

Files I wrote (all in
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r35-round/scratch/verifier/`):

- `vfy_crc.py` — CRC-32C implementation and the document's stated check vectors
- `vfy_appA.py` — Appendix A's 128-byte file, decoded field by field and re-CRC'd
- `vfy_layouts.py` — coverage-walk arithmetic for every file I construct below

plus this transcript at the single output path named in the brief. I did not
read that output directory.

**Method note on searching.** The document is hard-wrapped and blockquotes carry
`> `. Every phrase search below was run against a whitespace-normalised copy of
the file built in Python (`re.sub(r'\s+',' ', re.sub(r'\n>\s?','\n', text))`), so
a phrase spanning a line break or a `> ` marker is still found. I checked the
instrument before trusting any zero: `'declared, changed, cleared'` returned 0
while `'declared, changed or cleared'` returned 3 in the same passage, which is
the positive control for that sweep.

---

## 1. What I built

A conforming verifier, on paper. The document's verifier is defined by
[R-CNF-11] (§2.3), [R-CNF-12] (§2.4), [R-CNT-21] (§5.2), [R-LIF-08] (§9.7),
and a scatter of `a verifier MUST` clauses that I swept for exhaustively
(§4 below). Appendix H's checklist is a non-normative summary of the same.

### 1.1 The certification procedure, as an ordered algorithm

The verdict vocabulary is fixed by [R-CNF-11]:

> A verifier reports one of three verdicts: *conforming*, *nonconforming*, or
> *cannot establish* — the last where some requirement is one it is unable to
> check on a capability or resource ground

and the priority rule is unambiguous:

> An established violation takes priority: a verifier that has established any
> violation reports *nonconforming*, however many requirements it was unable to
> check, and *cannot establish* is available only to a traversal that
> established no violation.

So the verdict lattice is: **any established violation → nonconforming**;
**no violation but ≥1 unchecked requirement → cannot establish**; **no violation
and nothing unchecked → conforming**. There is no fourth state. *Unexamined* and
the per-requirement unchecked report are explicitly *not* verdicts: "that
per-requirement report constrains the report and not the verdict, as
*unexamined* does below."

The algorithm I would implement, in order, with the input and verdict effect of
each step:

**V0. Physical size.** Obtain the transport-authoritative size (§19.1 step 1,
[R-CNT-10]). Size < 128 → F5, reject-file, *nonconforming*. Note that this is
"decided from F alone and needing no other byte of the file", so it precedes
every other check. No slack total is owed here (§1.3).

**V1. Front signature block, [0,16), by byte equality.** A verifier has no
residency exemption. §21.2's F6 cell says so in terms: "the obligation binds a
reader holding those bytes resident, and a reader that would have to fetch them
MAY defer or omit the check (`[R-CNT-04]`); **a verifier holds no such
exemption (§2.3)**". Appendix H repeats it. Mismatch → F6 (or F1's front-block
instance if byte-reversed) → *nonconforming*.

**V2. Trailer, in §6.2's fixed order.** magic (F8/F1) → trailer CRC (F14) →
version gate (F18, and the unimplemented-major refusal) → then, and only then,
the remaining gates together: flags (F19), committed_file_length == physical
size (F17) and multiple of 64 (F13), dir_offset ≥ 16 (F9), dir_length ≥ 4
(F16), dir_offset + dir_length ≤ F − 64 (F10, the sum being [R-ENC-04]-
designated → F3), file_id ≠ 0 (F12), reserved [48,60) zero (F15), and the
u64 domain on each (F2). Any failure → *nonconforming*.

An unimplemented `version_major` is the one branch that is **not** a violation:
[R-CNF-13] confines the file to the conditions that *reach* it, and the verifier
reports *cannot establish* if every reaching condition passes, *nonconforming*
if one fails. I derived the reaching set myself in §3.4 and it matches §21.2's
claim exactly.

**V3. Directory region.** Fetch [dir_offset, dir_offset + dir_length), verify
the terminal CRC over the preceding dir_length − 4 bytes before any other use
(F20). Then parse the record sequence with no residue (F29).

**V4. Top-level record walk.** Per record: type ≠ 0 (F24); reserved-range type
(F36; with MU = 1, F35 is the narrower row); registered types' stored MU/PE bits
against §7.3 (F28); reserved flag bits 2–15 (F26); MU = 1 with PE = 0 (F25);
extent-slot validity (F30, F31, F32); multiplicity (F34); user-metadata framing
(F21, F22, F23). Layer names → the namespace, duplicates → F4.

An **experimental-range** top-level type with MU = 1 is the second of §21.6's
"conforming files a reader nevertheless refuses": [R-CNT-15] obliges rejection,
[R-CNF-02] leaves the file conforming, and [R-CNF-11] lists it as a
cannot-establish ground. My verifier therefore reports *cannot establish*,
never *nonconforming*, and must say which requirement and on what ground.

**V5. Per layer:** the whole of §19.3's list (extent slot, the §7.4 constraint
set, exact parse, sub-record walk and multiplicity, name rules, u64 domain, the
six value sets, bool fill, the lz4 cap, the geometry floor and its arithmetic,
the [R-ENC-04] ceiling, and the index cross-checks) — L1 … L36, L39, L43 … L47,
L49. Then the index chain: crc_of_crc_array (L37) and every segment CRC (L38).

**V6. Per index entry:** classify under §15.3's eleven rows. Six are marked
*structural* (I counted them: rows 2–7 of the table) and yield no usable extent;
one is the crc failure, which leaves the entry well-formed.

**V7. Whole-file, verifier-only:** the coverage walk (§1.2), extent overlap
(L18 intra-layer, F33 otherwise), no structure in the pre-trailer gap (F7),
alignment (L40) and slab (L41, L42) invariants.

**V8. Decode every stored tile.** §9.7 is categorical: "A verifier that
certifies decodes every stored tile, whatever content obligations §14 places on
the layer: §21.4's codec rows are file-conformance violations, and a verifier
MUST NOT certify past a violation it has not looked for". Checks: exact decoded
size (T3), exact consumption and well-formedness (T24, T25), codec-specific
header rules (T14, T17–T23), padding content (T4), pad bits (T5), interleaved
bool bytes at real positions (T2).

**V9. Decode every user-metadata document under an assigned encoding**
(R2 … R10). Under an **experimental-range** encoding, [R-MTA-10] withdraws every
content rule, so there is nothing to check and certification is unaffected — but
the verifier "MUST report each record it ignored on this ground, naming the
owning scope, the encoding value, and the stored extent length".

**V10. Verdict and report.** Report per §1.4.

#### When a check cannot be run

[R-CNF-11] names the grounds with "as when", so the list is illustrative rather
than closed — I checked that wording specifically, because a closed list here
would have left the "declined a whole layer on resource grounds" case of §5.2
and §9.7 homeless:

> the last where some requirement is one it is unable to check on a capability
> or resource ground, **as when** the file names a format major version it does
> not implement, when a record carries MUST_UNDERSTAND = 1 with a type it does
> not implement (§21.6), when it cannot execute a codec or filter
> (`[R-COD-11]`), when it declines a layer's or a tile's decode on resource
> grounds and so cannot check §14's decoded-content obligations
> (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`), or when it declines to decode a
> user-metadata document (`[R-MTA-09]`).

Two things are expressly **not** grounds. An experimental-range document
encoding: "the record is not among `[R-CNF-11]`'s cannot-establish grounds"
([R-MTA-10]). And §21.7's unwitnessed conditions: "None of these is a
requirement a verifier is *unable to check* within the meaning of `[R-CNF-11]`:
no file-level witness exists to check, so nothing about the file is left
undetermined and the verdict is unaffected."

I note in passing that [R-COD-11]'s ground ("cannot execute a codec or filter")
is dead for a *conforming* verifier, because §2.3 makes a verifier a conforming
reader and [R-CNF-03] makes all four codecs and both filters core — §17.4 says
so itself ("software unable to execute an assigned codec or filter is not a
conforming reader"). I did not file this: the document names the case in the
same paragraph, which is exactly the "read the paragraph above" test.

### 1.2 The coverage walk

[R-CNT-02] partitions the live committed state into: the front signature block;
or a **structure** — a stored-tile extent, a record extent, the directory, or
the trailer. [R-LIF-08] enumerates the claimants:

> the directory itself, each record's extent, and the stored extent of each
> non-sentinel tile-index entry (an entry `[R-IDX-03]` classifies reject-tile on
> a *structural* ground contributes no stored extent to the walk; one whose
> stored bytes alone fail its crc keeps its extent)

plus, explicitly, the front block and the live trailer. Three exclusions matter
and all three are stated in three places consistently (§5.2, §9.7, §15.3):

1. A record is not a claimant of its own header/inline payload — those lie
   inside the directory region, which claims them.
2. A layer record's extent slot addresses the tile-index region, so "the region
   enters the walk once, as that record's extent, and is not a second claimant
   beside it."
3. A structural-ground reject-tile entry contributes nothing; "the bytes of the
   file it nominally addresses fall to slack where no other claimant claims
   them."

**Can a byte be neither claimed nor slack?** No, and the document says why in
§5.2's Note: "The live committed state is *defined* as the front block plus what
a complete coverage walk reaches, and `[R-LIF-08]` makes every byte that walk
misses slack — so 'belongs to no class' describes nothing, and a register row
for it would be a row no file could exhibit." I checked that no claimant can lie
outside [0, F): F17 pins F to the physical size, and every claimant is bounded
into [16, F − 64) by F9/F10, F31/F32, L16/L17, T8/T9.

**Which bytes are certified, and which are counted-but-unconstrained.** Three
states, not two:

- **Certified** — claimed and covered by a checksum in §8.1's map, or (front
  block) by byte equality: front block, trailer, directory, tile-index region,
  every stored tile, every user-metadata extent.
- **Counted but unconstrained** — claimed, but with no checksum and no content
  rule: "the extent of a record of a type this specification has not assigned",
  which §8.1's last row covers "none — the bytes are opaque (§7.2)". §22.3 names
  it as one of its four residues. A second, weaker case: a user-metadata extent
  under an experimental-range encoding *is* CRC-covered but content-
  unconstrained — §22.3 again: "a certificate covers those bytes uninspected".
- **Slack** — unclaimed. Counted, reported, content irrelevant.

#### Worked file A — a complete walk

Layer `sst`: rank 1, dimension `x` with E = 100, T = 32 → G = ⌈100/32⌉ = 4,
N = 4, interleaved, one float32 channel `temp`, fill 0x7FC00000, codec 1,
filter 1, **alignment A = 512**, entry_count = 4. Decoded size per tile is
P · Q = 32 · 4 = **128 bytes**, and codec 1 forces every non-sentinel entry's
length to equal it ([R-COD-04]). Tiles 0–2 stored, tile 3 sentinel. Index region
is 4 × 20 + ⌈4/2¹⁶⌉ × 4 = **84 bytes** ([R-CNT-17]). One file-scope user-metadata
record, encoding 1, document `{"tarn.title":"demo"}` (21 bytes) + 4-byte terminal
CRC = 25-byte extent. Layer record inline payload is 81 bytes (I re-derived
§7.4's example byte budget: 4 + 34 + 18 + 12 + 13 = 81), so the layer record is
105 bytes and the user-metadata record 25; dir_length = 105 + 25 + 4 = **134**.

```
[0,16)        front signature block          16
[512,640)     tile 0                        128     512 mod 512 = 0
[1024,1152)   tile 1                        128    1024 mod 512 = 0
[1536,1664)   tile 2                        128    1536 mod 512 = 0
[1664,1748)   tile-index region              84
[1748,1773)   user-metadata extent           25
[1773,1907)   directory                     134
[1907,1920)   pre-trailer pad                     (slack)
[1920,1984)   trailer                        64
F = 1984
```

dir_offset + dir_length = 1907 ≤ F − 64 = 1920 ✓. F mod 64 = 0 ✓.

Claimed = 16 + 128 + 128 + 128 + 84 + 25 + 134 + 64 = **707**.
Slack total = 1984 − 707 = **1277**.

Cross-check by enumerating the unclaimed runs: [16,512) = 496, [640,1024) = 384,
[1152,1536) = 384, [1907,1920) = 13 → 496 + 384 + 384 + 13 = **1277**. The two
agree, which is the arithmetic identity the walk rests on.

Verdict: **conforming**, with the slack total 1277 reported. Note that the
sentinel entry for tile 3 contributes no claimant, and that the 84 bytes it
"would" occupy do not exist at all — a sentinel names no extent.

#### Worked file A′ — a walk that does not complete

Same bytes, but change entry_count from 4 to 5. That is L21 ("entry_count does
not equal the geometry-derived addressed-tile count"), reader-detected at layer
access, reject-layer. §5.2:

> A rejected layer's claimants are not enumerated, whether or not the rejection
> impeded reading them

so the enumerated claimants are the front block (16), the user-metadata extent
(25), the directory (134) and the trailer (64) = **239**. Partial total =
1984 − 239 = **1745**, reported as partial, naming layer `sst` and row L21.
1745 ≥ 1277, so the "upper bound on the file's true slack, never an under-count"
property holds. Verdict: **nonconforming**.

(An aside worth recording: with entry_count = 5 the region length formula also
fails — 5 × 20 + 4 = 104 ≠ 84 — so L22 fires too. The two rows overlap without
either being a strict specialization of the other, which §21.1 permits: "Rows
that merely overlap, each reachable without the other, do not stand in it.")

#### A walk that does not complete without any violation

A layer whose entry_count is 2³³ exceeds §21.9's 2³² guarantee. The file stays
conforming ([R-ERR-04]: "A file exceeding any of these remains conforming"), the
verifier declines the layer on resource grounds, never enumerates its claimants,
reports a **partial** total, and — having established no violation — reports
**cannot establish**. This is the case where the two axes come apart: a partial
slack total with a clean file.

Contrast: a verifier that declines only a *tile's* decode leaves the walk
complete. §5.2 is explicit — "a tile's or a document's decode declined leaves
the walk complete, that claimant being enumerated from its index entry or extent
slot." So a 512 MiB tile (above §21.9's 256 MiB guarantee) yields **cannot
establish with an exact slack total**. I checked both §5.2 and §9.7 list the
same three incompleteness triggers, and they do, verbatim in substance.

#### The floor case: slack can be zero

I built a conforming file with **zero** slack, which I record because it refutes
the natural assumption that the pre-trailer pad guarantees a positive total.
Front block [0,16); a directory of 112 bytes at [16,128) holding one layer record
(24-byte header + 84-byte inline payload); trailer at [128,192); F = 192.
dir_offset + dir_length = 128 = F − 64 exactly, so the pad is empty — §6.2
allows this: "a writer that ends its directory on a 64-byte boundary leaves
none." The layer declares a 12-byte name, rank 1, C = 1, a dimension with
extent 0 and tile extent 1, one bool channel, index_encoding 1, entry_count 0,
crc_of_crc_array 0, extent slot (0,0). Inline budget: 13 + 34 + 18 + 6 + 13 = 84.
Claimed = 16 + 112 + 64 = 192 = F. **Slack = 0.**

The layer is valid by [R-GEO-02] ("A dimension with extent 0 is valid: its grid
count is 0, the layer has zero addressed tiles, its tile index has zero
entries"), it escapes [R-COD-07]'s lz4 cap by §17.2's Note, and both slab and
alignment invariants are vacuous over an empty stored-tile set.

### 1.3 When no total is owed at all

§5.2 carves out exactly one case:

> Where §6.2's ordered validation rejects the file before a live trailer is
> established there is no F and no live state to walk, so the total is not owed
> at all: the verifier reports the trailer failure and nothing about slack,
> which is not a partial total but the absence of one.

I worked through which register rows land in that carve-out: F8, F14, F18, F19,
F13, F17, F9, F10, F12, F15, F16, and F2/F3 at their trailer instances — all of
them inside §6.2's ordered validation. F5 lands there too, not by the carve-out
but because a file below 128 bytes admits no trailer that could pass the gates
(F must be a multiple of 64; at F = 64 the only candidate, dir_offset ≥ 16 and
dir_offset + dir_length ≤ 0 cannot both hold).

F6 and F1's front-block instance are the interesting boundary: they are
reject-file at open, detected outside §6.2's order. I opened this as a candidate
defect and closed it. The obligation in [R-CNT-21] is conditional — "a verifier
that reaches a live state MUST report the total" — and [R-CNF-11] licenses both
paths: a verifier may stop at the first violation (and then "MUST report each
scope it did not examine as *unexamined*"), or continue and walk. Both are
conforming; the verdict (*nonconforming*) is the same either way; and §5.2's Note
already licenses run-dependence in the total: "A partial total (`[R-CNT-21]`)
reports what one verifier's incomplete walk left unclaimed, which is a fact
about that run and not about the file's live state." Not a defect.

### 1.4 The report

Assembled from every reporting obligation I could find (sweep in §4):

| Item | Obligation | Rule |
|---|---|---|
| Verdict | one of three | [R-CNF-11] |
| Each requirement unchecked on a capability/resource ground, with the ground | MUST, whichever verdict | [R-CNF-11] |
| Each scope not examined, as *unexamined* | MUST, if it stopped early | [R-CNF-11] |
| Slack total | MUST, if it reached a live state | [R-CNT-21] |
| — as partial, naming what stopped the walk | MUST, if the walk is incomplete | [R-CNT-21] |
| Each experimental-encoding user-metadata record: owning scope, encoding value, stored extent length | MUST | [R-MTA-10] |
| A declined document's bound and stored extent length | SHOULD | [R-MTA-09] |
| Any resource refusal, as a limit and never as a validity error | MUST | [R-ERR-04] |
| A SHOULD deviation, as an advisory | reported where observed, never hunted for | [R-CNF-12] |
| Loss of a user-metadata record | SHOULD | [R-CNT-20], §21.5 |

The SHOULD line is worth stating precisely because it is easy to over-implement:
"A verifier owes no search for one: §2.3's duty to check every file-level
requirement runs to MUST-level conditions, and a SHOULD deviation is reported
where the verifier observes it and not hunted for" ([R-CNF-12]).

---

## 2. Extent overlap, alignment and slab, on an adversarial layout

### 2.1 The layout

Layer `p`: rank 1, dimension `x` with E = 8, T = 2 → G = 4, N = 4. **Planar**,
C = 2: `a` uint8 (fill 0x00) and `b` bool (fill 0x00). Addressed-tile count =
C · N = 8; disk ordinals 0–3 are channel `a`'s block, 4–7 channel `b`'s
([R-GEO-06]: "**c · N + s** for a planar layer"). P = ∏Tᵢ = 2, so channel `a`'s
plane is P · Bᶜ = 2 bytes and channel `b`'s packed plane is ⌈P/8⌉ = **1 byte**
(§14.3). Codec 1, so those are also the stored lengths. Slab **S = 2,
A_slab = 16**.

[R-SLB-02] partitions each channel block independently: runs are ordinals
[0,2), [2,4) for channel `a` and [4,6), [6,8) for channel `b` — "runs never span
channel blocks". entry_count = 8 → index region = 8 × 20 + 4 = **164 bytes**.

```
[0,16)     front                     16
[16,18)    o0  a-tile               2   run 0 first stored: 16 mod 16 = 0  ✓
[18,20)    o1  a-tile               2   16 + 2 = 18                        ✓ packed
           o2  SENTINEL                 transparent to run continuity
[32,34)    o3  a-tile               2   run 1 first stored: 32 mod 16 = 0  ✓
[48,49)    o4  b-tile               1   run 2 first stored: 48 mod 16 = 0  ✓
[49,50)    o5  b-tile               1   48 + 1 = 49                        ✓ packed
[64,65)    o6  b-tile               1   run 3 first stored: 64 mod 16 = 0  ✓
[65,66)    o7  b-tile               1   64 + 1 = 65                        ✓ packed
[128,292)  tile-index region      164
[292,399)  directory              107   (one layer record, 24 + 79 inline, + 4 CRC)
[399,448)  pre-trailer pad              (slack)
[448,512)  trailer                 64
F = 512
```

Claimed = 16 + 10 + 164 + 107 + 64 = **361**; slack = 512 − 361 = **151**, which
I cross-checked against the unclaimed runs [20,32), [34,48), [50,64), [66,128),
[399,448) = 12 + 14 + 14 + 62 + 49 = 151.

Run 1's first *stored* tile is o3, because o2 is a sentinel and "Sentinel tiles
are transparent to run continuity: they occupy no bytes and do not break
packing" ([R-SLB-03]). This is the case §16.2's own example draws ("If ordinal
10 is a sentinel, run 1's stored tiles are 8, 9, 11…15, packed with no gap where
10 would have been"), so the layout exercises the invariant rather than dodging
it. Verdict: **conforming**.

### 2.2 B′ — slab gap (L41)

Move o7 to offset 66. Now 64 + 1 = 65 ≠ 66 → the run-3 packing relation fails:
L41, instance *gap*, detector verifier, reject-layer. §5.2 then discards the
layer's claimants, including the ones the walk had already enumerated —

> where the rejection is one the walk itself established, L18's overlap or L40
> through L42's placement among them, the claimants it had already enumerated
> are discarded with the layer

— leaving the front block (16), the directory (107) and the trailer (64) = 187.
Partial total = 512 − 187 = **325**, an upper bound on the 151 the file actually
carries. Verdict: **nonconforming**, partial total 325, stopped by layer `p` /
L41.

### 2.3 B″ — slab alignment (L42) and per-tile alignment (L40)

Move o6 to 68 and o7 to 69: run 3 is packed (68 + 1 = 69) but 68 mod 16 = 4, so
the run's first stored tile is misaligned → L42. Separately, in file A, moving
tile 1 from 1024 to 1000 gives 1000 mod 512 = 488 ≠ 0 → L40. Both are
verifier-only: [R-SLB-01] says "readers are not obligated to — offsets are
always explicit, so alignment is reader-invisible", and [R-SLB-03] says readers
"MAY instead detect contiguity arithmetically from any index segment."

### 2.4 B‴ — overlap (L18 and F33)

Place the index region at [60, 224) instead of [128, 292). It now overlaps o6
[64,65) and o7 [65,66). Both structures belong to layer `p`, so [R-CNT-13]
gives reject-layer:

> a verifier MUST treat an intra-layer overlap — including a stored extent
> overlapping its own layer's index region or sub-record extents — as
> reject-layer, any overlap across layers or touching another scope's structures
> as reject-file, and any overlap between two structures neither of which
> belongs to a layer as reject-file

I checked that this trichotomy is exhaustive over pairs of claimants: (X, X) →
L18; (X, Y≠X) and (X, non-layer) → F33; (non-layer, non-layer) → F33. If instead
a *second* layer's tile is placed at [64,65), the pair spans two layers → F33,
reject-file, and the whole enumeration ends.

I also checked F33's bounds parenthetical, which routes any claimant that
reaches the front block or the trailer away from F33 and to its own tier row
(F9/F10, F30/F31/F32, L15/L16/L17, T8/T9), including the subtle half-zero case:
"a record extent slot of (0, N) with N nonzero reaches the block through its
zero offset and is theirs rather than F31's or L16's". Every one of those eight
rows exists and covers exactly the claimant class named. No gap.

### 2.5 The structural-entry exclusion, checked against all three sites

An entry with offset = 8 (below 16) is §15.3's fifth *structural* row — T8. It
"contributes no stored extent to the *verifier* rows, which bind over
well-formed entries' extents only" — so its nominal extent [8, 8+len) is
excluded from the overlap rows **and** from the alignment/slab rows, and
contributes no claimant to the walk; its bytes fall to slack. I verified all
three statements of this exclusion agree: §15.3's preamble, §9.7's parenthetical,
and §5.2's "it contributes no claimant, the walk passes over it".

This matters because §3.1 defines *stored* as "that generation's tile-index entry
for it is not the sentinel" — so a malformed non-sentinel entry **is** a stored
tile by that definition, and [R-SLB-01]'s "every stored tile's offset satisfies
offset mod A = 0" would otherwise catch it at offset 8. §15.3 resolves it, and
L40's Governing rule cell cites `[R-SLB-01] (R-IDX-03)` — the register knows.
Opened and closed.

The converse case is stated just as carefully: "An entry whose only defect is
that its stored bytes fail its crc is well-formed ... so its extent stands and it
keeps its place in the *verifier* rows, in run continuity, and in the coverage
walk." So a T1 tile is a claimant, is checked for overlap and alignment, and
leaves the walk complete. I confirmed §15.3, §9.7 and [R-SLB-03] all say this.

---

## 3. Checksums, decoded content, and the numbers

### 3.1 Every constant I could compute locally

I implemented CRC-32C from the parameters in [R-ENC-09] (reflected polynomial
0x82F63B78, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and reproduced **every**
checksum constant the document states:

| Constant | Document | Computed | ✓ |
|---|---|---|---|
| CRC-32C(`"123456789"`) | 0xE3069283 | 0xE3069283 | ✓ |
| CRC-32C(zero bytes) | 0x00000000 | 0x00000000 | ✓ |
| §7.4: CRC over 80 bytes of 4 sentinel entries | 0x80A34955, stored `55 49 A3 80` | 0x80A34955, `55 49 A3 80` | ✓ |
| §7.4: crc_of_crc_array over that 4-byte array | 0xC4EE982E, stored `2E 98 EE C4` | 0xC4EE982E, `2E 98 EE C4` | ✓ |
| §15.4: CRC of a full all-sentinel segment (2¹⁶ entries) | 0xEECB3BB2 | 0xEECB3BB2 | ✓ |
| Appendix A: trailer CRC over trailer [0,60) | 0x402F157E | 0x402F157E | ✓ |
| Appendix A: directory CRC (zero-byte record sequence) | 0x00000000 | 0x00000000 | ✓ |

Nothing was left unreproduced. The only checksum-adjacent constant I could not
compute is Appendix G item 2's derived `file_id`, which is deliberately
parameterised ("the hash a named function at a named version") and so has no
value to check.

I also decoded Appendix A's full 128-byte hex dump field by field and confirmed
every annotation: magic, version_major = 1, version_minor = 0, flags = 0,
dir_offset = 16, dir_length = 4, committed_file_length = 128, file_id =
0x0123456789ABCDEF, twelve zero reserved bytes, F mod 64 = 0, dir_offset +
dir_length = 20 ≤ 64 = F − 64, and a slack total of **44** — matching the
document's "[20, 64) zero — pre-trailer pad, 44 bytes".

For the degenerate index case I computed two figures the document does not
state, so a corpus builder has them: the CRC of a one-entry all-sentinel
*partial* segment is **0xE5389D3D** (and its crc_of_crc_array **0xD5D57989**).
These are not 0xEECB3BB2 and must not be, because [R-IDX-05] restricts the
constant to a **full** segment: "one covering exactly 2¹⁶ entries, final or not
— whose entries are all sentinels ... a partial segment's CRC MUST be computed."

### 3.2 Which structures are covered by which checksum

§8.1's map, read against §4.5's exception list, and checked against every
claimant class:

| Claimant | Covered by | Certified? |
|---|---|---|
| Front signature block | none — byte equality | yes (by equality) |
| Trailer | trailer bytes [60,64) over [0,60) | yes |
| Directory region | final 4 bytes over dir_length − 4 | yes |
| Tile-index region | entries → segment CRC array → crc_of_crc_array → (in the layer record, inside the directory) → directory CRC | yes, all bytes |
| Stored tile | its index entry's crc | yes |
| User-metadata extent | final 4 bytes over the preceding bytes | yes (bytes); content only under an assigned encoding |
| Extent of a record of an unassigned type | **none** | no — counted, uncovered |

**So: not every live structure is covered by a checksum.** The single uncovered
class is the unassigned-type record extent, and the document is explicit about
the consequence in §22.3: "corruption inside it is equally invisible: §20.4's
byte-identical re-emission (`[R-WRT-05]`) carries such an extent forward unread,
and `[R-WRT-08]` bars re-encoding it, so nothing an updater does would surface
the damage."

I verified the chain closes at both ends. The interior checksum fields — segment
CRC arrays, entry crc fields, crc_of_crc_array — are "both comparison-verified
and covered by exactly one further checksum" (§4.5); the terminal ones — trailer,
directory, user-metadata — are comparison-verified and covered by nothing
further. That accounts for every byte.

I also checked the index region's byte accounting at the boundaries: at
entry_count = 0 the formula gives 0 × 20 + 0 × 4 = 0, the extent slot is (0,0)
and crc_of_crc_array is 0 (L22, L27 otherwise); at 65,536 it gives 1,310,724 with
one full segment; at 65,537, 1,310,748 with two, the second covering one entry.
§15.4's worked example at entry_count = 1,000,000 reproduces exactly: 16 segments
(15 full plus 16,960), a 64-byte array, a 20,000,064-byte region, entry 999,999
at segment-relative byte 20 × 16,959 = 339,180, the array at
[20,000,000, 20,000,064) and segment 15 at [19,660,800, 20,000,000) — 339,264
bytes fetched, the document's "~339 KB", and a full segment is 65,536 × 20 =
1,310,720 = 1.25 MiB as stated.

### 3.3 Decoded-content obligations

**What a verifier must decode:** every stored tile, unconditionally (§9.7), and
every user-metadata document under an assigned encoding ([R-MTA-09] makes the
decline a cannot-establish ground, so a certifying verifier decoded it).

**What it compares against:** decoded size from the layer's declarations alone —
[R-SER-07] is emphatic that "decoded size is a function of the layer's
declarations alone — geometry, layout, and channel types — never of payload
content"; exact stream consumption ([R-COD-08]); each codec's header rules; the
recorded fill at every padding position and every pad bit ([R-SER-05]: "a
verifier MUST check it"); and 0x00/0x01 for interleaved bool values at real
positions ([R-SER-08]).

I worked the padding case concretely. Take file B but with E = 7 instead of 8:
G = ⌈7/2⌉ = 4 still, and tile 3 covers positions 6 and 7, of which 7 lies outside
the extents and is a padding position. Channel `a`'s plane for o3 is then
`<sample at 6> 00` — the second byte is the recorded fill. Channel `b`'s packed
plane for o3 is one byte whose bit 0 is the sample at 6, whose bit 1 is the
*fill bit* (a padding position), and whose bits 2–7 are pad bits, also the fill
bit. With fill false the whole byte above bit 0 is zero. I verified §14.3's
worked example independently: P = 10, alternating true/false from ordinal 0
gives byte 0 = bits 0,2,4,6 set = 0x55 and byte 1 = bit 0 set = 0x01, with six
pad bits; with fill true, byte 1 becomes 0x01 | 0xFC = **0xFD**, exactly as the
document says.

I also verified §14.4's P = 1 claim: the planar packed byte is (value in bit 0,
fill bit in bits 1–7) and the interleaved byte is the value, so "the images
coincide exactly when that fill is false" — correct.

And §17.3's shuffle example, byte for byte. Three float32 values 1.0, 2.0, 3.0
give `00 00 80 3F 00 00 00 40 00 00 40 40`; with s = 4, n = 3, byte i of group j
goes to offset i·n + j, producing `00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40`,
which is the document's `00 00 00 00 00 00 80 00 40 3F 40 40`. ✓

**What a verifier may skip:** slack content; the content of an unassigned-type
record's extent; the content of a user-metadata document under an
experimental-range encoding ([R-MTA-10]: "there is no violation there to look
for"); §21.7's unwitnessed conditions (wrong sample values, an undisclosed
dictionary, a mis-strided filter with no structural witness); and any SHOULD
deviation it did not happen to observe ([R-CNF-12]).

### 3.4 Register arithmetic I re-derived

**Rows and instances.** §21.8 states "120 conditions over 277 instances". I
parsed the four register tables mechanically (six-column rows whose first cell
matches `[FLTR]\d+`), applying §21.1's own counting rule ("Instances within a
cell are separated by semicolons, and a cell reading — is one instance"):

- rows: F 35, L 49, T 26, R 10 → **120** (matching each subsection's own header
  count of 35 / 49 / 26 / 10; F11 is struck and its label retired)
- instances: F 56, L 116, T 55, R 50 → **277**

Both figures reproduce exactly.

I then spot-checked the instance doctrine on the changed §21.4. "Where the
condition compares two **magnitudes** either of which can be the greater — a
*differs from* or *does not equal* — the two directions are likewise enumerated;
where its own text bounds the comparison in one direction — an *exceeds*, a
*larger than* — there is one." T3 (*is not exactly*) → 3 layouts × 2 directions =
6 ✓. T14 (*differs from*) → 6 ✓. T22 (*does not equal*) → 6 ✓. T21 (*larger
than*) → 3 layouts × 1 = 3 ✓. T1 (a checksum comparison, "equal or it is not")
→ 1 ✓. T6 (crc ≠ 0, "a field tested only for being nonzero") → 1 ✓. T12 (a sum
against a bound, "a single predicate over several fields") → 1 ✓. Every cell in
§21.4 obeys the doctrine. R4's sixteen instances are 8 frame-constraint
alternatives × 2 containers, and I checked those eight against §18.2's own
carried-over list; they match.

**Which rows reach a foreign format major.** §21.2 asserts: "Deriving it there
yields F8, F14, F6 and both of F1's instances ... and no other row." I derived
it independently from [R-CNT-24]'s four permanent invariants (trailer magic at
F − 64; version_major/minor at F − 56; a CRC-32C at F − 4 over [F − 64, F − 4);
a constant front block) and got exactly that set. The near misses are
instructive and the document handles each: F15's reserved bytes sit at trailer
offset 48, inside the 48 bytes a future major may redefine, so it does not reach;
F5's 128-byte floor "is derived from a directory of at least 4 bytes at an offset
of at least 16 and a 64-aligned F ... and those are format major 1's"; F13, F17,
F19, F9, F10, F12, F16 all read fields inside those same 48 bytes; and F18 is
"outside the premise" because version_major = 0 declares no major. Confirmed.

**Strict specializations.** §21.1 names six pairs; I checked all six by
constructing the implication. F1's front-block instance ⊂ F6 (a byte-reversed
`89 54 41 52 4E 0D 0A 1A` is not byte-identical to it); F1's trailer-magic
instance ⊂ F8; F35 ⊂ F36 (MU = 1 is a case of "whatever its MU bit"); L24 ⊂ L25;
F21 ⊂ F22 (extent_length 0 < 5); L10 ⊂ L11. All six hold. I also found a seventh
the list does not name — L46's *layer record* instance is necessarily L49, since
a layer record is type 0x0001, a registered type whose registry PE is 1 — but
§21.1 says "the property decides any pair and this list is not offered as
closed", and both rows carry the same detector and detection point, so nothing
turns on it.

**Other arithmetic.** §21.9's Note: 2³² entries → ⌈2³²/2¹⁶⌉ = 2¹⁶ segments →
2¹⁸ = 256 KiB array ✓; at 2³⁶, 2²² = 4 MiB ✓. §9.2's Note: dir_length ≥ 4 plus
the 64-byte trailer forces new F ≥ prior F + 68, and both being multiples of 64
forces ≥ prior F + 128 ✓. §9.3's Note: the largest multiple of 64 at or below
2⁶³ − 1 is 2⁶³ − 64 ✓. §20.3's example: 32 · 20 + 4 = 644 ✓. §11.4's example:
in-tile ordinal 44 · 256 + 188 = 11,452 ✓, spatial ordinal 1 · 8 + 2 = 10 ✓,
planar disk ordinal 2 · 32 + 10 = 74 ✓, entry at region bytes [1,480, 1,500) ✓,
channel 3's entries 96–127 ✓. §14.2's examples: Q = 3 and decoded size 18, sample
5 at [15,18); planar `b` 12 bytes with ordinal 5 at [10,12); Q = 5 and decoded
size 30 with sample 5 at [25,30) ✓. §14.5's example: grid 2 × 2, edge tile (1,1)
carries one real position and 15 padding positions, 32 bytes of uint16 ✓.
§4.6: `température` in NFC is the 12 bytes given, NFD is 13 ✓. §12.3's channel
entry `04 74 65 6D 70 0C 00 04 00 00 C0 7F` ✓. §12.1's bfloat16 1.0 = high 16
bits of 0x3F800000 = 0x3F80, stored `80 3F` ✓.

I found no arithmetic error anywhere in the document.

---

## 4. Sweeps run

All against the whitespace-normalised copy, with hit counts:

| Pattern | Hits | What it was for |
|---|---|---|
| `verifier MUST` | 14 | the full inventory of verifier obligations; I read every one |
| `verifier MUST NOT` | 3 | certify-past, certify-a-cannot-establish, report-a-decline-as-nonconforming |
| `A verifier` / `a verifier` | 13 / 35 | conditional obligations the two patterns above miss (e.g. "a verifier that reaches a live state MUST report") |
| `verifier's` / `verifiers` | 8 / 4 | verification depth in §20.1, §20.3, §20.5 |
| `cannot establish` | 8 | the verdict's every occurrence |
| `unexamined` | 3 | [R-CNF-11]'s report item |
| `certif` | 44 | every certification statement |
| `declared, changed or cleared` | 3 | the three sites of §20.3's fifth closed-list member (§11.1 Rationale, §20.3 step 4, Appendix H) |
| `declared, changed or kept` | 1 | the delegated clause in §20.3's closing paragraph |
| `declared, changed, cleared` | 0 | **negative control**, paired with the 3 above |
| `a slab or alignment declaration` | 4 | every restatement of the member |
| `slab declaration declared` / `kept has its invariants` / `or is cleared` | 1 / 1 / 1 | the restatement grounded in [R-SLB-01]/[R-SLB-03]/[R-SLB-04] |
| `T24, T25` / `T3, T14, T21, T22` / `T4, T5, T2` | 1 / 1 / 1 | the row lists in §20.3 step 4 |
| `no check any actor owes` | 1 | the completeness claim of finding verifier-01 |
| `The fixed declarations are` | 1 | the characterization of finding verifier-03 |
| `fails outright` | 2 | one in §6.4 (unrelated), one the clause at issue |
| `decoded size` inside §21.4 | 4 rows | T3, T14, T21, T22 — confirming the first parenthetical is exhaustive |
| register table rows matching `\|\s*[FLTR]\d+\s*\|` | 120 | the row and instance counts |

---

## 5. The closed list and the grounded restatement, read as the brief asks

### 5.1 The fifth member's transitions

§20.3 step 4:

> A layer that stores a tile **in the generation this commit supersedes** keeps
> its declarations, with these exceptions and no other: its name, and its
> dimension and channel names, MAY change; a dimension extent MAY grow, and MUST
> NOT shrink; a planar layer's channel list MAY be extended at its end or
> shortened from its end, but not both in one commit; and a slab or alignment
> declaration MAY be declared, changed or cleared as this step provides below.

I enumerated the transitions a slab-or-alignment declaration can make and looked
for the verb naming each:

| Transition | Named by |
|---|---|
| none → some | *declared* |
| some → another value | *changed* |
| some → the same value | the head clause — "keeps its declarations"; keeping is not an exception and needs no verb |
| some → none | *cleared* |
| alignment ↔ slab in one commit | *cleared* + *declared*, licensed by "A commit MAY make several of these changes at once" |

No transition is unnamed. The one verb the member does **not** carry — the
default, *kept* — is correctly absent, because the head clause already supplies
it: the list enumerates exceptions to keeping, so "kept" would be a category
error there. And the delegated clause that *does* carry it — "a slab declaration
declared, changed or kept has its invariants satisfied over every run of the new
state ... or is cleared" — carries it for a different purpose: it states the
*obligation* on a kept declaration, which is exactly what [R-SLB-04] needs
(a kept declaration on a layer whose stored-tile set changed must have its
invariants re-established). So the member and the clause it delegates to differ
in vocabulary without diverging in content. I checked both restatements (§11.1's
Rationale and Appendix H's checklist) and both say "declared, changed or
cleared", matching the member. No site carries a stale verb.

### 5.2 The restatement grounded in its rules

> on a layer this commit modifies, a slab declaration declared, changed or kept
> has its invariants satisfied over every run of the new state, the runs this
> commit adds included, or is cleared (`[R-SLB-03]`, `[R-SLB-04]`,
> `[R-CNF-05]`), and an aligned layer's stored tiles, every one the new state
> holds and those this commit adds included, satisfy its invariant or the
> declaration is cleared (`[R-SLB-01]`, `[R-CNF-05]`).

Put each cited rule's quantifier beside the sentence's:

- **[R-SLB-03]** — "When declared, for every run: the run's stored tiles are
  contiguous and packed in ordinal order ... and the first stored tile's offset
  satisfies offset mod A_slab = 0." Quantifier: every run of the layer, in the
  live state. The sentence: "over every run of the new state, the runs this
  commit adds included." Same set; the sentence is a live-state result, matching.
- **[R-SLB-01]** — "When declared: every stored tile's offset satisfies
  offset mod A = 0." Quantifier: every stored tile of the layer in the live
  state. The sentence: "every one the new state holds and those this commit adds
  included." Same set; the second half is redundant emphasis, not an extension.
- **[R-SLB-04]** — binds "A writer or updater whose commit changes the
  stored-tile set, the run partition, the byte placement of any run, the disk
  ordinal of any tile the new state stores, or the slab declaration itself, of a
  layer slab-declared in either the superseded or the new generation". This is
  an *actor* rule over a *pair* of generations. The sentence's "on a layer this
  commit modifies" is broader (it reaches a layer whose record alone changed) and
  the sentence is a state result rather than an actor duty.

The asymmetry I looked hardest at: the slab half cites three rules and the
alignment half two, with no [R-SLB-04] analogue for alignment. I satisfied myself
this is correct rather than an omission. [R-SLB-01]'s invariant is a plain
live-state predicate over the new generation's stored tiles, so a stale alignment
declaration carried forward is caught directly by L40; slabs need [R-SLB-04] only
because §16.2's Note says so — "The obligation here is the writer's, and it is
what makes those two rows reachable at all after a commit."

I opened one ambiguity in [R-SLB-04] and closed it: "MUST either re-establish the
invariants for **every such run**" admits both "every run of the layer" and
"every run the listed changes touched". §20.3's restatement picks the first
("every run of the new state"), and it does not matter which is right, because
[R-SLB-03] is a file-level invariant over every run and L41/L42 are verifier rows
against any file that breaks it. The emittable set is the same under both
readings. Not filed.

### 5.3 The two lists' completeness claim, derived independently

> Between them the two lists reach every declaration field of §7.4

I enumerated §7.4's inline-payload fields and mapped each side:

| §7.4 field | Side |
|---|---|
| name | permitted (names MAY change) |
| layout | fixed |
| linearization | fixed |
| codec | fixed |
| filter | fixed |
| alignment A | permitted (declared / changed / cleared) |
| slab S | permitted |
| slab alignment A_slab | permitted (part of the slab declaration, §16.2) |
| rank d | fixed |
| channel count C | both — planar via the channel list, interleaved fixed |
| dimension entries: name | permitted |
| dimension entries: extent | permitted (grow only) |
| dimension entries: tile extent | fixed |
| channel entries: name | permitted |
| channel entries: type | fixed |
| channel entries: fill | fixed |
| index_encoding | fixed |
| entry_count | "follow the commit" |
| crc_of_crc_array | "follow the commit" |
| sub-records | §20.4's subject |

Every field is reached, and the two fields on both sides are exactly the two the
sentence names ("a planar layer's channel list, an interleaved layer's channel
list"). The claim holds.

---

## 6. Multi-generation trace

Four generations of file A. Certification result at each: **conforming**.

**Gen 1 — creation.** As laid out in §1.2. F₁ = 1984, claimed 707, slack 1277.
Creation path per [R-LIF-02] and §20.2: front block, then payloads and index,
then the directory and its CRC, then the barrier, then pad and trailer, then the
barrier. Both barriers are conduct rules — "a file committed without one can be
byte-identical to a file committed with it" — so the verifier sees nothing of
them and cannot report on them.

**Gen 2 — append tile 3.** Writing begins at exactly F₁ = 1984. The layer
declares A = 512, so the new tile goes at 2048 (2048 mod 512 = 0), not at 1984.
Because the stored-tile set changed, the layer's *whole* index region is
re-emitted at a new placement (§20.3 step 4, [R-WRT-04]) — 84 bytes for one
changed entry. The user-metadata record is re-emitted byte-identically with its
extent slot untouched, so its old extent stays live ([R-WRT-05]).

```
new tile 3   [2048,2176)  128
new index    [2176,2260)   84
new directory[2260,2394)  134
pad          [2394,2432)
trailer      [2432,2496)   64      F₂ = 2496
```

F₂ − F₁ = 512 ≥ 128 ✓ ([R-LIF-02]'s forced minimum). Claimed = 16 + 384 (tiles
0–2) + 128 + 84 + 25 + 134 + 64 = **835**; slack = 2496 − 835 = **1661**. Newly
slack: the old index region (84), the old directory (134), the old pad (13) and
the old trailer (64), plus the 64-byte alignment gap [1984,2048) and the new
38-byte pad.

**Gen 3 — edit the user-metadata document.** §20.3's shape-(c) discussion is
explicit that this is *not* shape (c): "Editing user metadata is not shape (c):
its document lives in an extent (`[R-CNT-25]`), so a new extent is appended and
the old one becomes slack, as in (b)." New 26-byte extent at [2496,2522), new
directory at [2522,2656), trailer at [2688,2752), F₃ = 2752. Claimed = **836**;
slack = **1916**. I cross-checked incrementally: 1661 + (25 + 134 + 64 newly
superseded) + 32 new pad = 1916 ✓. (My first pass got 1954 by double-counting
gen 2's pad, which was already slack; the identity claimed + slack = F caught it.)

**Gen 4 — compaction.** [R-WRT-06] and [R-WRT-07]: a fresh file_id, only live
structures, every stored tile's bytes verbatim with its entry crc unchanged, the
index region regenerated because the stored extents moved, crc_of_crc_array
updated, and the output's reference arrays equal to the input's bit for bit.
Placement is the compactor's to choose but **must still honour A = 512**
("every declared layout invariant permits (`[R-SLB-01]`, `[R-SLB-03]`)"):

```
[0,16) front | 512 t0 | 1024 t1 | 1536 t2 | 2048 t3 | 2176 index | 2260 umd | 2286 dir | 2432 trailer, F₄ = 2496
```

Claimed = **836**; slack = **1660**.

The result worth recording: **compaction reclaimed only 256 of 1916 slack bytes**
here, because the declared 512-byte alignment forces a 384-byte gap before every
128-byte tile and a 496-byte gap before the first. An alignment declaration puts
a hard floor under the slack any compaction can reach, and the verifier's slack
total — which §22.3 calls "the number that distinguishes a working file from a
padded one" — reads no differently for alignment waste than for superseded
generations. Nothing in the document says otherwise; it is a consequence an
operator reading only the total would miss, and [R-SLB-05] arguably anticipates
it ("A writer that scatters structures wastes space rather than violating a
rule, and the verifier's slack total, where its walk completes, is what surfaces
the waste"). I did not file it: it is a true reading of the rules, not a defect
in them.

**Gen 2′ — a generation that fails certification.** Suppose gen 2 had placed
tile 3 at 1984 instead of 2048. 1984 mod 512 = 448 ≠ 0 → L40, verifier-detected,
reject-layer. Verdict *nonconforming*; the layer's claimants are discarded, so
the partial total is 2496 − (16 + 25 + 134 + 64) = 2257, an upper bound on the
1661 the file carries; and the report names layer `sst` / L40 as what stopped the
walk.

---

## 7. Findings

Three. None is byte-level, and I say so for each rather than reaching.

### verifier-01 — AMBIGUITY

**§20.3 step 4** ([R-WRT-04]).

> Under new ones the same bytes would denote values, coordinates or padding the
> writer did not store, with every checksum in §8 certifying the result and, but
> for a stored tile's decoded size, a padding position or pad bit, or a boolean
> byte the register witnesses (T3, T14, T21, T22, T4, T5, T2) and a decode that
> fails outright under a changed codec or filter (T24, T25), no check any actor
> owes able to see it (§21.7).

The sentence is a completeness claim: *apart from the listed rows, no obligatory
check sees a barred re-declaration*. The first parenthetical is demonstrably
exhaustive — I grepped §21.4 for `decoded size` and got exactly T3, T14, T21 and
T22, and T4/T5/T2 are exactly the padding-position, pad-bit and interleaved-bool
rows. That exactness invites reading the second parenthetical the same way, and
read that way the claim is false.

Concretely: a layer stores tiles under codec 1 (none), so each stored extent
holds the raw decoded image. A commit changes the codec declaration to 3 (zstd) —
a change the step bars, but one whose file the step says is "judged on its own
terms". Every stored tile's first four bytes are now measured against the zstd
frame magic and fail, which is **T17** ("Codec 3 (zstd) and the stored bytes do
not begin with the compressed-frame magic 28 B5 2F FD"), a reader-detected
tile-use check, not T24 and not T25. T17 is not in the list. The same change from
codec 2 or codec 4 gives the same result. Under codec 1 → 2 or 1 → 4, T24/T25 do
cover it; it is the change *to* codec 3 that escapes, because [R-COD-06] screens
the magic before any decode is attempted.

Two readings: (a) "(T24, T25)" closes the second exception, in which case the
sentence understates the witnesses by at least T17; (b) "(T24, T25)" illustrates
the category "a decode that fails outright", which stretches to cover a magic
check that precedes decoding. I picked (b), because it keeps the sentence true
and because §21.4's own T17 governing rule is [R-COD-06], the same requirement
whose window and content-size clauses supply T21 and T22, both of which *are*
listed. But (a) is the natural reading given the first parenthetical's evident
exhaustiveness, and the sentence sits in normative text, not in a Note.

An implementer building a verifier does nothing differently either way — it
checks every register row regardless — which is why I grade this low. What it
costs is a reader's confidence in the passage's argument, in the one place the
document argues *for* the shape of its closed list.

### verifier-02 — AMBIGUITY

**§20.5** ([R-WRT-09]).

> A compactor's verification depth follows reliance over everything it carries
> (`[R-WRT-03]`): it relies structurally on every structure it copies, so it
> MUST verify each link of the chain — the open (§19.1), each retained layer's
> record (§19.3) and full index chain (`[R-IDX-04]`), and **each relocated
> extent's checksum**, including every stored tile's entry crc — before emitting
> that structure's bytes.

The premise is quantified over "every structure it copies"; the third enumerated
item is quantified over *relocated* extents. Those are different sets, and §20.5
itself says so in the very next figure's commentary: "In this placement A's
stored extents happen not to move, so A's index is copied and only its slot
re-pointed; under a placement that moved them it would be regenerated too,
placement being the compactor's to choose."

So take a compactor whose chosen placement leaves layer A's stored extents where
they were. Is it obliged to verify those tiles' entry crcs?

- Reading (a): "including every stored tile's entry crc" is an unqualified
  addition, so every stored tile is verified whether or not it moved, and only
  non-relocated *record* extents (a user-metadata extent left in place, say)
  escape the enumeration.
- Reading (b): "relocated" governs the whole item, so a compactor may copy an
  unmoved extent without checking the checksum that covers it — contradicting
  the sentence's own premise and leaving §20.5's "MUST refuse to compact when
  any check `[R-WRT-09]` obliges fails" with nothing to bite on for that extent.

I picked (a), on the strength of the premise clause and of "before emitting that
structure's bytes", which is per-structure and reaches everything the compactor
emits. But (b) is available on the plain words, and the two readings differ in
how much I/O a compactor owes on an already-near-compact input.

Not byte-level, and the reason is [R-CNF-05]'s first sentence rather than its
second. Under reading (b) a compactor could emit an output carrying an unverified
corrupt tile — but that output is nonconforming (T1), and "A writer MUST emit
only conforming files" bars every conforming writer from emitting it under both
readings. The disputed file is not itself conforming, so the emittable set does
not move; what moves is only how much work a compactor must do before finding
out.

### verifier-03 — OBSERVATION

**§20.3 step 4** ([R-WRT-04]), the sentence immediately before verifier-01's.

> The line is drawn where a stored tile's meaning is fixed. The fixed
> declarations are the ones §14 reads a stored tile under — its value sequence,
> its byte layout, the fill its padding positions hold (§14.5) — the ones §11.4
> assigns its ordinal and its values' coordinates by, as a rule rather than as
> the numbers the rule yields, and the one §15 gives the layer's index region
> its shape by.

This is a three-way characterization of "the fixed declarations", and it does not
reach the codec or the filter. §14 gives the value sequence (layout, C, P), the
byte layout (channel types, layout) and the padding fill; §11.4 gives the
ordinal rule (linearization, rank, dimension order, tile extents); §15 gives the
index region's shape (index encoding). Codec and filter belong to §17, and §17.1
places them *between* the decoded tile image and the stored bytes rather than
inside §14.

The operative list two paragraphs earlier does include them —

> Every other declaration is fixed for as long as the layer stores a tile: the
> layout, the linearization and the index encoding, **the codec and the filter**,
> the rank and the dimension order, every tile extent, every channel's type and
> fill, an interleaved layer's channel list (its names aside), and the position
> of every planar channel the new state keeps.

— and the clause immediately after names them too ("a changed codec or filter").
So the characterization is a gloss that is narrower than the rule it glosses, in
normative text, between two sentences that both get it right.

It is decidable — I decided it above by mapping §7.4's fields against §14, §11.4,
§15 and §17 — but deciding it costs a reader a four-section cross-walk that the
operative list makes unnecessary. The risk is that a reader who takes the
characterization as the definition concludes the codec is not a fixed
declaration, and lets an updater re-declare it on a layer that stores tiles.
Not byte-level: the bar "binds the commit as an actor: no file is nonconforming
by virtue of its violation", so the resulting file is judged by §21's rows either
way and the emittable set is unchanged.

---

## 8. Suspicions I opened and closed

Each of these was a real candidate I spent time on. I record the sentence that
closed it, because a lane that finds little should be able to show what it did
that would have found something.

1. **§21.6's "so a verifier certifies"** at the experimental-encoding row reads
   as an unconditional certification licence, which would contradict [R-CNF-11]
   in a file carrying another violation. Closed by §21.1: "§21.6's entries
   restate their governing rules on the same terms a row does, and where such an
   entry and the rule it cites diverge, the rule governs there too" — and the
   entry cites [R-MTA-10], which says only "certification is unaffected".

2. **[R-CNF-11]'s cannot-establish grounds look like a closed list** that omits
   "declined a whole layer on resource grounds", which §5.2 and §9.7 both rely
   on. Closed by the words "**as when**" introducing the list, which makes it
   illustrative under a general clause ("some requirement is one it is unable to
   check on a capability or resource ground").

3. **[R-SLB-01]'s "every stored tile" versus a malformed non-sentinel entry**,
   which §3.1's definition of *stored* would drag into the alignment check at an
   offset of 8. Closed by §15.3: "Such an entry contributes no stored extent to
   the *verifier* rows, which bind over well-formed entries' extents only", and
   by L40's Governing rule cell citing `[R-SLB-01] (R-IDX-03)`.

4. **[R-SLB-04]'s "every such run"** is ambiguous between the layer's runs and
   the runs the commit touched. Closed because [R-SLB-03] is a live-state
   invariant over every run and L41/L42 are verifier rows against any file that
   breaks it, so the two readings admit the same files.

5. **§15.2's "the fields of non-sentinel entries only"** would let [R-ENC-03]
   reach an entry with offset = length = 2⁶⁴ − 1 and crc ≠ 0, since that entry
   is not *the* sentinel entry. Closed by §15.3's preamble — "The per-entry
   outcomes below govern notwithstanding the general owning-scope mapping of
   `[R-ENC-03]`/`[R-ENC-04]`" — and by T11's condition text excluding it
   ("neither field being the all-ones sentinel") while T6 registers it.

6. **F6 sits outside §5.2's carve-out** for when no slack total is owed, so a
   file with a corrupt front block and a valid trailer looked underdetermined.
   Closed because [R-CNT-21]'s obligation is conditional ("a verifier that
   reaches a live state") and [R-CNF-11] licenses both stopping and continuing,
   with "one that does MUST report each scope it did not examine as
   *unexamined*" covering the stopping path.

7. **The partial total for a file-scope rejection the walk itself established**
   (F7, or F33 between two non-layer structures) has no discard rule matching the
   layer case's. Closed by §5.2's Note: "A partial total (`[R-CNT-21]`) reports
   what one verifier's incomplete walk left unclaimed, which is a fact about that
   run and not about the file's live state" — run-dependence is licensed, and the
   total constrains the report and not the verdict.

8. **[R-COD-11]'s cannot-establish ground appears dead** for a conforming
   verifier, since [R-CNF-03] makes every codec and filter core. Closed by §17.4
   naming exactly that: "For a conforming reader that position arises only at a
   reserved or experimental value ... software unable to execute an assigned
   codec or filter is not a conforming reader."

9. **§22.3's "Four residues"** is a closed count. Counted them: slack; the
   extent of an unassigned record type; a payload mimicking a trailer; a
   user-metadata extent under an experimental-range encoding. Four. I looked for
   a fifth — an experimental record type's *inline* payload — and closed it: that
   payload lies inside the directory region and is covered by the directory CRC,
   so corruption there is visible, which is the property the four share.

10. **[R-SER-08] at a padding position** looked like a condition with no row of
    its own. Closed by T2's condition text: "the same byte at a padding position
    is T4's, the two rows together covering `[R-SER-08]`", together with the fact
    that a bool fill byte is 0x00 or 0x01 ([R-TYP-07]), so a byte that is neither
    necessarily fails T4 as well.

11. **§4.7's "each descriptive field's definition states what a reader does when
    the field contradicts the data it describes"** — I checked whether §6.3 does
    this for version_minor, the only descriptive field. Closed by [R-CNT-07]: "A
    reader MUST NOT reject a file for its version_minor: minor releases are
    additive-only, and all feature gating is structural (records, enums, flags)."

12. **§11.1's Rationale arithmetic** about which growths touch the index. I
    derived it: a growth that changes no ⌈Eᵢ/Tᵢ⌉ leaves N and every ordinal
    fixed; one that raises a grid count while another stays 0 leaves the product
    at 0; any other growth raises some Gᵢ with no Gⱼ at 0, and since extents only
    grow, N strictly increases and entry_count with it. Correct as stated,
    including "the growth that raises a zero-extent layer's **only remaining**
    zero grid count".

13. **§21.1's specialization list** — I checked all six named pairs and looked
    for unnamed ones. Found L46's layer-record instance ⊂ L49; closed by "the
    property decides any pair and this list is not offered as closed", and
    because both rows share a detector and detection point.

14. **The §15.3 classification's exhaustiveness.** I enumerated (offset, length,
    crc) space and confirmed every entry falls into at least one row, with the
    overlaps all agreeing on reject-tile. No gap.

---

## 9. Confidence, and where I found little

**Certification procedure, coverage walk, checksums, decoded content:** I am
confident these are clean, and I can say what I did that would have found
something. I built four files and walked each; I derived the slack total twice
by independent methods (claimed-sum and unclaimed-run-sum) for six layouts and
they agreed every time; I reproduced every stated checksum constant and computed
two the document does not state; I re-derived the register's row count, its
instance count, its foreign-major reach set and its specialization pairs and all
four matched; and I swept the whole document for `verifier MUST` and its
conditional cousins and read every hit. Had a claimant class been missing from
§9.7, or a checksum unmapped in §8.1, or the register's counts wrong, those
methods would have surfaced it.

**Extent overlap, alignment, slab:** confident. The trichotomy in [R-CNT-13] is
exhaustive over claimant pairs; the eight bounds rows F33 routes to all exist and
cover exactly the claimant classes named; and the two structural-entry
exclusions (from the verifier rows and from the walk) are stated identically in
three places. My adversarial layout put a gap, a misalignment and an overlap into
one file and each landed on exactly one row.

**Multi-generation:** confident on the arithmetic, less so on the appender's
conduct rules, which are by design invisible to a verifier and so outside what I
could test from the bytes.

**Where I found little relative to effort:** §18.2's user-metadata frame rules.
I read the whole passage, checked that its carried-over list matches
[R-COD-06]'s constraint set item for item, that the two exceptions it names are
exactly the two it replaces, that the two constraints it routes outside the
register fall on §21.7's two distinct grounds, and that R4's sixteen instances
are the remaining eight alternatives across two containers. It is dense and it
is consistent. If something is wrong there, it is not in the enumeration.

**Overall confidence that an implementation built from this text alone would
interoperate: high**, for the verifier. The three verdicts, their priority
ordering, the claimant list, the slack-total obligation and its partial form, the
checksum map, and the decode obligations are all pinned. My three findings would
cost a careful implementer nothing at run time; they cost a reader confidence in
two enumerations and one gloss.
