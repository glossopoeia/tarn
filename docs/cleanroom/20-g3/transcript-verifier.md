# Round 20 — Verifier implementer, working transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in full, in seven sequential chunks. I opened no other file in the repository —
no `docs/`, no `conformance/`, no `PLAN.md`, `AGENTS.md`, `README.md`, no
`spec/registry.json`, no git history, no web. I ran `grep` against that one
file. All other computation was local Python that read no project file: a
CRC-32C implementation of my own, a TARN file builder, and a verifier
implementation, all written into my scratchpad.

Context I did not ask for **did** appear before I began: my runtime placed a
project instruction file and an index of the maintainer's private notes in my
context, and the harness surfaced a task list. Several of those entries name
this project's position and process. I did not open any of the files they
point at, and I have not used their contents as evidence about the
specification. I name their appearance here because the brief requires it. One
consequence worth stating plainly: the index's entries are phrased in ways that
could bias where I looked, and I cannot fully prove to a reader that they did
not. What I can say is that every claim below is traced to a quotation from
`spec/tarn.md` and, where arithmetic is involved, to a computation shown here.

---

## 1. What I built

A conforming verifier, implemented as executable Python (`verify.py`, ~230
lines), driven against TARN files I constructed byte by byte (`build.py`,
`gens.py`, `adv.py`, `adv2.py`). Everything below is the output of actually
running it, not a description of what it would do.

The verifier is structured as the ordered procedure the document dictates. I
give the order first, then the evidence for each step's placement.

### 1.1 The certification procedure, as an ordered algorithm

**Inputs.** The byte sequence, and a transport-authoritative size
(`[R-CNT-10]`: "The size a remote reader compares against
committed_file_length MUST be transport-authoritative"). Capability
declarations: which format majors, codecs, filters, record types, and
metadata encodings the tool implements, and its decode bounds.

**Verdict vocabulary.** Three verdicts (`[R-CNF-11]`): *conforming*,
*nonconforming*, *cannot establish*. Two report-only channels that are
neither verdicts nor findings: the per-requirement **unchecked** report
(mandatory whichever verdict is reported) and **unexamined** scopes
(mandatory only for a verifier that exercised the stop-at-first-violation
licence). A fourth channel, **advisory**, for SHOULD deviations
(`[R-CNF-12]`: "a verifier reports a SHOULD deviation as an advisory that
does not bar certification. A verifier owes no search for one").

**Step 0 — size floor.** `[R-CNT-27]`, F5. Physical size < 128 → reject-file.

**Step 1 — front signature block.** `[R-CNT-04]` obliges a resident reader
to "verify the full block by byte equality **before other processing**", and
§19.1 step 1 places it there. A verifier holds no residency exemption: F6's
row says so outright — "a verifier holds no such exemption (§2.3)" — and
Appendix H's verifier checklist repeats it. So for a verifier this check is
unconditional and strictly precedes the trailer. F6, F1's front-block
instance.

**Step 2 — trailer, in §6.2's fixed order.** `[R-CNT-06]`: "A reader MUST
validate, in order: the trailer magic; the trailer CRC; the version gate
(§6.3) — only these touch fields whose positions are fixed across all majors
(`[R-CNT-24]`) — and then, those gates passed, MUST validate all of the
following before acting on the fields involved". F8/F1, F14, F18, then the
version capability gate, then F19 and the field gates F17, F13, F9, F16, F10,
F11, F12, F15, plus F2/F3 on the u64 domain.

If version_major ≠ 0 and is a major the tool does not implement: **cannot
establish**, and stop. §2.3 lists this ground first, and §21.2's preamble
explains why only four rows reach such a file at all: "F8 and F1's
trailer-magic instance, F14's trailer CRC — the two checks §6.2 places before
the gate — and F6 with F1's front-block instance, which `[R-CNT-04]` places
before other processing."

**Step 3 — directory region.** Fetch `[dir_offset, dir_offset+dir_length)`;
`[R-CNT-11]`: "A reader MUST verify that CRC before any other use of the
region (mismatch: reject-file)". F20.

**Step 4 — top-level record walk.** §7.2 framing (F29, F24), multiplicity
(F34), extent slots (F30, F31, F32, F2, F3), user-metadata framing (F21, F22,
F23), and the layer-name namespace (F4) — the last decided, per §19.1 step 4,
"over the raw name bytes whether or not each name is itself well-formed".
Verifier-exclusive here: F25 (MU=1/PE=0), F26 (reserved flag bits), F28
(registered type's stored flags), F36 (reserved-range type). F35 for
reserved-range + MU=1.

An experimental-range top-level type with MU = 1 that the tool does not
implement is **not** a violation — §21.6's closing paragraph is explicit that
"`[R-CNF-02]` makes the file conforming all the same" — but it is a
cannot-establish ground (§2.3).

**Step 5 — per layer, §19.3's full validation.** The §7.4 constraint set,
exact parse, sub-record walk and multiplicity, name rules, value sets,
per-type fill, `[R-COD-07]`'s lz4 cap, the geometry floor and its arithmetic,
`[R-ENC-04]`'s ceiling, and `[R-CNT-17]`'s index cross-checks. §19.3 closes:
"All are decidable from the resident directory and F: layer access performs
no fetch." My implementation confirmed that — `parse_layer` touches no byte
outside the directory. Verifier-exclusive: L46, L47, L49.

**Step 6 — per layer, index chain.** `[R-IDX-04]`: crc_of_crc_array over the
fetched CRC array (L37), then each segment CRC (L38), then §15.3's per-entry
classification (T6–T12, and T1 later at payload).

**Step 7 — layout invariants.** `[R-SLB-01]`: "A verifier MUST check the
invariant (violation: reject-layer, §15.3)" — L40. `[R-SLB-03]`: "A verifier
MUST check these invariants" — L41, L42.

**Step 8 — per stored tile.** Entry crc over stored bytes (T1); then decode.
§9.7: "A verifier decodes every stored tile, whatever content obligations §14
places on the layer: §21.4's codec rows are file-conformance violations, and
a verifier MUST NOT certify past a violation it has not looked for." Then
T14/T24/T25 and the codec-specific rows, T3 on the decoded length, and the
content rows T2, T4, T5 (and T26 by way of T2/T4).

**Step 9 — record extents.** Each user-metadata extent's terminal CRC (R2),
decode (R3, R4), and the decoded document's rules (R5–R10), plus the
verifier-exclusive member-ordering rows F27 and L48.

**Step 10 — coverage walk (§9.7).** Disjointness, bounds, slack total, and
F7 (a structure in the pre-trailer gap).

**Verdict.** Any established violation → *nonconforming*, unconditionally:
"An established violation takes priority: a verifier that has established any
violation reports *nonconforming*, however many requirements it was unable to
check, and *cannot establish* is available only to a traversal that
established no violation." Otherwise, any unchecked requirement on a
capability or resource ground → *cannot establish*. Otherwise *conforming*.

**What bars certification.** Five distinct bars, and I had to collect them
from five places: (1) any established violation (`[R-CNF-12]`: "a verifier
certifies only violation-free files"); (2) a *cannot establish* report
(`[R-CNF-11]`: "a verifier MUST NOT certify a file it reports that way");
(3) not having looked (`[R-LIF-08]`: "MUST NOT certify past a violation it
has not looked for"); (4) `[R-COD-11]`, a codec or filter it cannot execute;
(5) `[R-MTA-09]`, a user-metadata document it declines on its size bound.

**What does *not* bar certification.** SHOULD deviations (`[R-CNF-12]`); a
user-metadata record under an unassigned encoding (`[R-MTA-10]`: "certification
is unaffected"); any quantity of slack; ignore-lane flag bits; a high
version_minor; unrecognized or misplaced `tarn.` keys; experimental-range
MU = 0 record types.

---

## 2. The coverage walk, with arithmetic

### 2.1 The partition

§5.2 names the classes: "the front signature block; or a **structure** — a
stored-tile extent, a record extent ..., the directory, or the trailer."
§9.7 says the walk claims the front block and the live trailer too, and that
"A layer record's extent slot addresses that layer's tile-index region
(§7.4), so the region enters the walk once, as that record's extent, and is
not a second claimant beside it."

**Can a byte be neither claimed nor slack?** No, and the document says why:
"The live committed state is *defined* as the front block plus what a
complete coverage walk reaches, and `[R-LIF-08]` makes every byte that walk
misses slack — so 'belongs to no class' describes nothing, and a register row
for it would be a row no file could exhibit."

**Which claimed bytes are actually certified?** Not all of them. The
certificate covers three grades:

| grade | bytes | integrity | content rules |
|---|---|---|---|
| certified | front block, trailer, directory, index regions, stored tiles, user-metadata extents at an assigned encoding | equality or CRC | yes |
| claimed, uninspected | extent of a record of an unassigned type | **none** (§8.1) | none (§7.2, opaque) |
| claimed, uninspected | user-metadata extent at an unassigned encoding | terminal CRC | none (`[R-MTA-10]`) |
| counted, unconstrained | slack | none | none |

That is my answer to the charter's "which bytes are certified, which are
counted-but-unconstrained". The second row is the subject of finding
verifier-02.

**Is every live structure covered by a checksum?** No — and the document says
so twice, consistently. §4.5: "Every field of every structure is covered by
exactly one checksum, excepting the front signature block ..., the terminal
checksum fields ..., and the extent of a record of a type this specification
has not assigned". §8.1's map's last row: "Extent of a record of a type this
specification has not assigned | none — the bytes are opaque (§7.2) | —".

I checked the map for a *gap* rather than a stated exception, and found none.
The one that could have been a gap is the tail of a tile-index region: if
extent_length exceeded the entry array plus the CRC array, the excess would
be covered by nothing. `[R-CNT-17]` closes it — "extent_length MUST equal
entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4" — combined with §15.1's "with no
padding anywhere inside the region". Every byte of the region is therefore
covered by a segment CRC or by crc_of_crc_array. Likewise the directory (its
CRC covers dir_length − 4, and F29 forbids residue) and the trailer
(`[R-CNT-24]`: "The format-major-1 trailer has zero slack: every byte is
assigned").

### 2.2 A concrete file, and the arithmetic

Layer `sst`: rank 1, dimension `x`, E = 100, T = 32, one interleaved float32
channel `temp` with fill 0x7FC00000; codec 1, filter 1, no alignment or slab.
G = ⌈100/32⌉ = 4, N = 4, P = 32, Q = 4, decoded tile size = 128. entry_count
= 4; index region = 4×20 + ⌈4/2¹⁶⌉×4 = 84. Layer record inline payload = 81
bytes (I reproduced §7.4's worked example exactly: 4 + 34 + 18 + 12 + 13 =
81), record framing 24, directory 24 + 81 + 4 = 109.

Tiles 0 and 3 stored. Tile 3 is the edge tile: it covers x ∈ [96,128), of
which 96–99 are real and 100–127 are 28 padding positions, so it exercises
`[R-SER-05]`.

```
[0,16)      front signature block          16
[16,144)    tile 0 extent                 128
[144,272)   tile 3 extent                 128
[272,356)   layer index region             84   (= the layer record's extent)
[356,465)   directory                     109
[465,512)   pre-trailer pad                47   <- slack
[512,576)   live trailer                   64
F = 576, 576 mod 64 = 0
```

claimed = 16 + 128 + 128 + 84 + 109 + 64 = **529**; slack = 576 − 529 = **47**.

My verifier: `verdict: conforming; slack: 47 (exact)`.

I ran the same computation against Appendix A's 128-byte file as a control:
claimed = 16 + 4 + 64 = 84, slack = **44**, which is exactly what §5.1's
example states ("44 bytes of slack, zeroed by advice"). The verifier
reproduced 44. That confirms both that the front block and the live trailer
are claimants and that the pre-trailer pad is slack.

### 2.3 A walk that does not complete

Two layers. Layer A declares alignment A = 512 and stores one tile at offset
**520**. Layer B is clean.

```
[0,16)        front block                  16
[520,648)     layer A tile 0              128
[1024,1108)   layer A index                84
[1108,1192)   layer B index                84
[2048,2176)   layer B tile 0              128
[2176,2386)   directory                   210
[2432,2496)   trailer                      64
F = 2496
```

520 mod 512 = 8, so L40 fires (`[R-SLB-01]`, verifier, certification).

The trap: the walk had **already enumerated** layer A's index region and its
stored tile before establishing the placement violation. `[R-CNT-21]` is
explicit that they must now be thrown away — "where the rejection is one the
walk itself established, L18's overlap or L40 through L42's placement among
them, the claimants it had already enumerated are discarded with the layer,
since the total is a claim about a live state one of whose layers is not
usable".

- naive (keep everything): claimed 714, slack **1782** — this is what my first
  implementation printed, and it is the *exact* slack, which is precisely why
  it is wrong: a partial total must be "an upper bound on the file's true
  slack, never an under-count".
- correct: discard layer A's 84 + 128 = 212 bytes of claimants. claimed 502,
  **partial** slack **1994**, with the report naming layer A / L40 as what
  stopped the walk (`[R-CNT-21]`: "a verifier reporting one MUST say which
  scope or violation stopped the walk").

After patching, my verifier printed
`nonconforming; slack: 1994 (partial); stopped by: layer 'A' rejected: L40`.

A second trap I hit: the partial total must be computed over the **byte set**,
not as a sum of claimant lengths. `[R-CNT-21]` says "F less the bytes claimed
by the claimants the walk did enumerate". In a file with an overlap, summing
lengths double-counts the shared bytes and yields an under-count — the one
thing the rule forbids. I rewrote the walk as a sweep-line union. The document
does decide this; the word is "bytes", not "lengths".

### 2.4 Cases where the walk stays complete

I checked each candidate against §9.7 and found all four decided:

- **an entry §15.3 classifies reject-tile on a structural ground** — "does not
  make the walk incomplete: the walk passes over it, and the bytes it
  nominally addresses fall to slack (§15.3)". Exact total, nonconforming
  verdict.
- **an entry whose stored bytes alone fail its crc (T1)** — "one whose stored
  bytes alone fail its crc keeps its extent". Claimant stands, exact total.
- **content and decode violations (T2–T5, T24, T25)** — no effect on claimant
  enumeration; neither of `[R-CNT-21]`'s two partial triggers applies, so the
  total is exact.
- **a cross-scope overlap (F33)** with no scope-level enumeration cut — the
  walk did enumerate everything, so exact, and the union computation keeps it
  honest. My case N (a top-level metadata extent at [300,311) overlapping the
  directory at [296,428)) printed `F33 ... slack: 88 (exact)`.

---

## 3. Extent overlap, alignment, and slab, on concrete layouts

`[R-CNT-13]` gives the three-way scope split: "a verifier MUST treat an
intra-layer overlap — including a stored extent overlapping its own layer's
index region or sub-record extents — as reject-layer, any overlap across
layers or touching another scope's structures as reject-file, and any overlap
between two structures neither of which belongs to a layer as reject-file".

| layout I built | rows | outcome my verifier reached |
|---|---|---|
| layer A tile [200,328) vs its own index [272,356) | L18 | reject-layer |
| layer A tile [16,144) vs layer B tile [80,208) | F33 | reject-file |
| layer A index [200,284) vs directory [250,357) | F33 | see below |
| metadata extent [300,311) vs directory [296,428) | F33 | reject-file, exact slack 88 |

The third case is instructive and I want to record it honestly: the directory
physically overwrote the tail of the index region, so crc_of_crc_array failed
(**L37**) before the overlap check ran, the layer was rejected, its claimants
were discarded, and F33 was never established. That is correct behaviour, not
a bug — a violation is established either way and the verdict is
nonconforming — but it means overlap detection is order-dependent and a
verifier's *report* for such a file is implementation-dependent. §24
`[R-VEC-02]` anticipates exactly this: "where a condition cannot be isolated
... the entry records every row the file exercises and says which it was built
for."

**Alignment (`[R-SLB-01]`, L40).** A = 512: tile at 512 certifies; tile at 520
gives L40. Note that the first admissible offset is 512, not 16, so an aligned
layer necessarily leaves [16,512) as slack; nothing forbids that
(`[R-SLB-05]`, and §16.1: "The bytes alignment leaves between structures are
slack (§5.2), which writers SHOULD zero and no conformance requirement
constrains").

**Slabs (`[R-SLB-03]`, L41/L42).** Interleaved, N = 4, S = 3, A_slab = 64.
`[R-SLB-02]` partitions the single block [0,4) into runs [0,3) and [3,4),
"Run r of a block starts at ordinal block_start + r·S". Four layouts:

- tiles 0,1,2 at 64, 192, 320 — packed, first offset 64 mod 64 = 0 → clean.
- tiles at 64, 200, 328 — an 8-byte gap → **L41** ("run at 0: tile 1 offset 200
  != 192").
- tiles at 80, 208, 336 — 80 mod 64 = 16 → **L42**.
- ordinal 1 a sentinel, tiles 0 and 2 at 64 and 192 → clean, because
  "Sentinel tiles are transparent to run continuity: they occupy no bytes and
  do not break packing."

The asymmetry `[R-SLB-03]` draws — structural reject-tile entries transparent,
a crc-failing entry not — is load-bearing for implementation order. My
verifier classifies all entries structurally *first*, runs the slab check over
the surviving extents, and only then verifies payload CRCs; otherwise a
crc-failing tile would drop out of the run and mask an L41. The document
justifies exactly this: "so this invariant stays decidable from the index
entries alone, given the committed file length §15.3 already requires to
classify any entry."

**F7, the pre-trailer gap.** `[R-CNT-05]`: "A verifier MUST treat a structure
in that gap as a validity error at file scope". I placed a stored tile at
[880,1008) with the directory ending at 335 and F − 64 = 1024 — the verifier
returned F7. My first attempt put the tile past F − 64 and tripped T9 instead;
that is the right precedence (T9 is a structural entry classification, so the
entry contributes no extent to the walk at all and F7 never gets a claimant to
find).

---

## 4. Checksum obligations, and which constants I reproduced

Reproduced locally, all matching:

| constant | stated | computed |
|---|---|---|
| CRC-32C("123456789") | 0xE3069283 (§4.5) | 0xE3069283 ✓ |
| CRC-32C(zero bytes) | 0x00000000 (§4.5, Appendix A directory) | 0x00000000 ✓ |
| full all-sentinel segment (2¹⁶ entries, 1,310,720 B) | 0xEECB3BB2 (`[R-IDX-05]`) | 0xEECB3BB2 ✓ |
| §7.4's 80-byte 4-sentinel entry array | 0x80A34955, stored `55 49 A3 80` | 0x80A34955 ✓ |
| §7.4's crc_of_crc_array over `55 49 A3 80` | 0xC4EE982E | 0xC4EE982E ✓ |
| Appendix A trailer CRC over [0,60) | 0xE00938D2, stored `D2 38 09 E0` | 0xE00938D2 ✓ |

I built the CRC from the *reflected* polynomial 0x82F63B78; that it reproduces
the check vector confirms §4.5's parameters (polynomial 0x1EDC6F41, reflected
in and out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) as a set.

Non-CRC constants I could confirm only for internal consistency, not compute:
the zstd frame magic (0xFD2FB528 spells `28 B5 2F FD` little-endian ✓), the
lz4 frame magic T23 names (`04 22 4D 18` = 0x184D2204 ✓), and the lz4 decoded
cap 0x7E000000, all of which are external-format facts this document pins by
reference. bfloat16 1.0 = 0x3F80 and 0x7FC0 as a quiet NaN follow from
`[R-TYP-02]`'s identification and check out.

Every other worked number in the document reproduced too, which is worth
recording because it is the cheapest evidence of internal consistency I have:
§17.3's shuffle (`00 00 00 00 00 00 80 00 40 3F 40 40`, and the inverse round-
trips), §14.3's packed plane (`55 01` at fill false, `55 FD` at fill true),
§14.5's edge tile (32 bytes, value 0 real, values 1–15 all `CD AB`), §14.2's
offsets (18 and 30 byte images; ordinal 5 at [15,18) and [25,30)), §11.4's
ordinals (s = 10, in-tile 11,452, planar disk ordinal 74), §15.4's
1,000,000-entry layer (16 segments, 64-byte array, region 20,000,064, segment
15 at [19,660,800, 20,000,000)), §20.3's 644-byte index region, and §21.9's
note (2³² entries → a 256 KiB CRC array; 2³⁶ → 4 MiB; a full segment 1.25 MiB).

I also counted the register mechanically: 121 rows (F 36, L 49, T 26, R 10)
over **273** instances (F 58, L 116, T 55, R 44), taking a "—" cell as one
instance and otherwise splitting on semicolons, exactly as §21.1 prescribes
("the count is therefore mechanical once the cell is written"). §21.8 states
"121 conditions over 273 instances". It matches on the nose. Of those, 20 rows
/ 42 instances carry detector *verifier*; I checked each against its governing
rule and each has a verifier MUST or is reached through one that does (T2 and
T26 have no verifier MUST of their own — `[R-SER-08]` says only "its assigned
detector is the verifier" and `[R-COD-10]` "a verifier detects it" — but §2.3's
"checks every file-level requirement" and §9.7's "MUST NOT certify past a
violation it has not looked for" supply the force).

---

## 5. Decoded-content obligations

**What a verifier must decode.** Every stored tile of every layer (§9.7), and
every user-metadata document under an assigned encoding. The obliging sentence
has no BCP 14 keyword in its first clause — "A verifier decodes every stored
tile" — and I stopped on that, because a keyword-less clause has no force of
its own. It is nonetheless bound, twice over: the same sentence continues "and
a verifier MUST NOT certify past a violation it has not looked for", and §2.3
defines the class as one that "checks every file-level requirement". I record
the hesitation but do not report it: unlike the shapes this project has been
burned by, the operative MUST NOT sits in the same sentence and reaches the
same result.

**What it compares against.** T3 against the declaration-derived decoded size
(`[R-SER-07]`: "decoded size is a function of the layer's declarations alone
... never of payload content"); T14 for codec 1, checkable before any fetch;
T24/T25 for exact consumption and well-formedness; T17–T22 on the zstd frame
header; T4 padding positions against the recorded fill; T5 pad bits against the
fill bit; T2 interleaved bool bytes at real positions only. The last split is
decided explicitly by T2's own row — "the same byte at a padding position is
T4's, the two rows together covering `[R-SER-08]`" — and since `[R-TYP-07]`
confines a bool fill byte to 0x00/0x01, T2 can never fire at a padding
position in a file whose fill is valid.

I exercised T4 by flipping four bytes of tile 3's padding region from the fill
NaN to zero; the verifier reported
`T4 tile 3 ordinal 4 padding != fill (00000000 vs 0000c07f)`.

**What it may skip.** Only on a capability or resource ground, and each skip
costs certification: a codec or filter it cannot execute (`[R-COD-11]` — nearly
vacuous for a *conforming* verifier, since §2.3 obliges every core codec and
filter, so the only reachable case is a reserved or experimental value, which
is L43/L45 and a violation anyway); a layer's or tile's decode declined on
resource grounds; a user-metadata document declined on the §18.2 bound
(`[R-MTA-09]`, which pins that bound at no smaller than §21.9's 16 MiB).
`[R-ERR-04]` closes the loophole: "Software that declines **on that ground** a
file whose every quantity lies within the table is not a conforming reader",
so a verifier may not decline a 200 MiB tile against a 256 MiB guarantee.

**What is explicitly not a skip.** A user-metadata record under an unassigned
encoding: "A verifier meeting such a record in an otherwise conforming file
has no requirement it is unable to check — the record is not among
`[R-CNF-11]`'s cannot-establish grounds, and certification is unaffected — and
it MUST report each record it ignored on this ground, naming the owning scope,
the encoding value, and the stored extent length" (`[R-MTA-10]`). Its terminal
CRC is still checked; R2 still applies. Encoding 0 and the reserved range stay
violations (R1). I built this case and confirmed the split.

**What no decode can reach.** §21.7 is unusually candid and I checked its
claim: `[R-LIF-01]`, `[R-LIF-03]`, `[R-GEO-06]`/`[R-SER-01]` ordinal mappings,
`[R-CNT-13]`'s no-embedded-offsets prohibition, `[R-CNT-18]`'s nesting
prohibition, §20.3's declaration-change bar, and §20.5's two trailer
obligations have no single-file witness. Crucially the section also settles
what that means for the verdict: "None of these is a requirement a verifier is
*unable to check* within the meaning of `[R-CNF-11]`: no file-level witness
exists to check, so nothing about the file is left undetermined and the verdict
is unaffected." Without that sentence a verifier would have to report *cannot
establish* on every file. It is there.

---

## 6. Multi-generation trace

Same layer as §2.2. All four generations built byte-exactly and verified.

**Gen 1 — creation** (`[R-LIF-02]` creation path, `[R-WRT-02]`). front block;
tiles 0 and 3 at [16,144) and [144,272); index at [272,356); directory at
[356,465); pad [465,512); trailer [512,576). F = 576.
→ **conforming**, slack **47** (exact).

**Gen 2 — append tile 1** (`[R-WRT-04]` step 4). Writing begins at exactly
F = 576. New payload [576,704); the layer's *whole* index region re-emitted at
[704,788) — "necessarily at a new placement (`[R-LIF-01]`)" — new directory
[788,897); pad [897,960); trailer [960,1024). F = 1024. Tiles 0 and 3 do not
move; the old index, the old directory, the old pad and the old trailer become
slack (84 + 109 + 47 + 64 = 304), plus the new 63-byte pad.
→ **conforming**, slack **367** (exact). Claimed 657.

**Gen 3 — supersede tile 0**. New payload [1024,1152), index [1152,1236),
directory [1236,1345), pad, trailer [1408,1472). F = 1472. The superseded
payload joins the slack.
→ **conforming**, slack **815** (exact). Claimed still 657 — the live state's
size is invariant across these two commits, which is the point of the example
in §20.3 ("a commit's cost is dominated by its index, not its data").

**Gen 4 — compaction** (`[R-WRT-06]`, `[R-WRT-07]`). Fresh file_id, generation
1. Tiles re-placed in disk-ordinal order at [16,144), [144,272), [272,400);
index regenerated at [400,484) — entry offsets new, "entry lengths, entry crcs,
and sentinel entries unchanged; segment CRCs recomputed over the entries as
re-emitted" — layer record's crc_of_crc_array and extent slot updated;
directory [484,593); trailer [640,704). F = 704.
→ **conforming**, slack **47** (exact). I verified byte-identity of all three
stored tiles between gen 3 and gen 4, which is `[R-WRT-07]`'s "every stored
tile's bytes verbatim" and what makes "The output's reference arrays MUST equal
the live generation's bit for bit" hold.

Certification result at each generation: conforming, conforming, conforming,
conforming; slack 47 → 367 → 815 → 47. The 815 is the number §20.5's example
calls "what tells an operator when to run this".

Two compaction questions I had to resolve from the text:

*Must the compactor honour a slab or alignment declaration in its new
placement?* `[R-SLB-04]` binds "A writer or updater whose **commit** changes
... the byte placement of any run", and §9.1 makes compaction not a commit
("every conforming mutation of a file is either a commit (§9.2) or a whole-file
rewrite under a new file_id"). So `[R-SLB-04]` does not reach a compactor by
its own terms. §20.5 answers directly: the compactor "is free to place
structures anywhere §5.2 admits and every declared layout invariant permits
(`[R-SLB-01]`, `[R-SLB-03]`)", and independently `[R-CNF-06]`/`[R-CNF-05]` make
L40–L42 bind its output. Resolved; no guess needed.

*May it clear the declaration instead?* No — `[R-WRT-05]` requires
byte-identical re-emission of retained records, and `[R-WRT-07]`'s exception
list is closed: re-pointed extent slots, regenerated index regions, and
crc_of_crc_array. Clearing A or S is not in it.

*What if an entry is structurally malformed?* §20.5 handles it: regeneration
"cannot proceed without meeting it, and the violation is thereafter one the
compactor has detected. `[R-WRT-06]` then obliges refusal". My gen-4 build
never hit this because gen 3 was clean.

---

## 7. Places I had to guess, and what I found

Most of what looked open closed under reading. I record the ones that took
real work, because the charter asks for it:

- **A file-scope rejection after the trailer gates** (F20, directory CRC).
  `[R-CNT-21]`'s relief is scoped to "§6.2's ordered validation", which F20 is
  not. But the general condition — "Where the walk of §9.7 does not enumerate
  every region's claimants" — is satisfied, so the total is **partial**, and it
  comprises the three claimants the walk did reach: the front block (16), the
  live trailer (64), and the directory region itself (§9.7 lists "the directory
  itself" among the claimants). My verifier reports F − 16 − 64 − dir_length,
  partial, naming F20. Determined, not guessed — but it took composing a
  general condition with an illustrative parenthetical.
- **A layer rejected before any claimant was enumerated** (L34, a bad channel
  type at layer access; or L38, a segment CRC). The general clause is "a
  rejected layer's claimants are not enumerated, **whether or not the rejection
  impeded reading them**", so none are counted, and the parenthetical about
  discarding covers only the sub-case where some had already been enumerated.
  Determined.
- **`[R-CNF-11]`'s "report each scope it did not examine"** when the stop
  happens at open. The layer set is not yet known, so "each scope" is literally
  unenumerable; the best a verifier can say is "everything below file scope".
  The clause's stated purpose — "which is not a finding that the scope is
  clean" — is satisfied by that, so I did not treat it as a defect on its own.
  It is the same root as finding verifier-01 and I fold it there.
- **Whether a stop before a live trailer owes a partial total at all.** This
  one did *not* close. It is finding verifier-01.
- **What a certificate must say about bytes it covered without inspecting.**
  Half-closed. Finding verifier-02.

Two things I checked and specifically decided *not* to report:

- The lowercase-keyword trap. I grepped the whole document for lowercase
  `must`/`should`/`may`/`shall`: nine hits, every one inside a `>` block
  (Note/Rationale/Example), which §2.1 makes non-normative anyway. The document
  is clean on this.
- Keyword-less invariants: §16.1's "When declared: every stored tile's offset
  satisfies offset mod A = 0" and §16.2's run-packing sentence. Both are bound
  — §20.2's "A creator MUST follow `[R-LIF-02]`'s creation path: ... in any
  order satisfying §5.2's coverage classes ... and every declared layout
  invariant" is a writer MUST, and L40/L41/L42 are register rows that §21.1
  makes file-conformance violations. I traced the chain and it holds.

---

## 8. Findings

### verifier-01 — AMBIGUITY

**Location.** §5.2, `[R-CNT-21]`; interacting with §6.1 `[R-CNT-04]`, §5.1
`[R-CNT-27]`, §2.3 `[R-CNF-11]`, and §21.2 rows F1, F5, F6.

**Title.** `[R-CNT-21]`'s "total not owed" relief names only §6.2's ordered
validation, leaving a stop at F6 or F5 owing a partial total it has no F to
compute.

**Quotation.**

> "a verifier that reaches a live state MUST report the total number of slack
> bytes, since that number is what tells an operator to compact. Where §6.2's
> ordered validation rejects the file before a live trailer is established
> there is no F and no live state to walk, so the total is not owed at all:
> the verifier reports the trailer failure and nothing about slack, which is
> not a partial total but the absence of one. Where the walk of §9.7 does not
> enumerate every region's claimants — whether because a scope-level rejection
> ends that scope's enumeration ... or because the verifier elected under
> `[R-CNF-11]` to stop at the first violation — the verifier MUST report the
> total as partial."

**Detail.** Two reject-file conditions are decidable *before* any live trailer
exists and are **not** part of §6.2's ordered validation:

1. **F6 / F1's front-block instance**, governed by `[R-CNT-04]` in §6.1. For a
   verifier this is not optional — F6's row says "a verifier holds no such
   exemption (§2.3)" — and `[R-CNT-04]` places it "before other processing",
   which §19.1 step 1 confirms by putting it ahead of the step-2 trailer fetch.
   So a verifier meets F6 with the trailer entirely unvalidated.
2. **F5's physical-size instance**, governed by `[R-CNT-27]` in §5.1. A 40-byte
   file cannot even present 64 bytes for §6.2 to validate.

`[R-CNF-11]` licenses a verifier to stop at the first violation. A verifier
that does so on either condition is squarely inside `[R-CNT-21]`'s second
sentence-group — it "elected under `[R-CNF-11]` to stop at the first
violation", so it "MUST report the total as partial" — while the relief that
would excuse it names only "§6.2's ordered validation". Yet the state it is in
is exactly the one the relief describes: "there is no F and no live state to
walk". A partial total is defined as "F less the bytes claimed", and F is the
live trailer's committed file length (`[R-CNT-01]`), which it has not
validated. The relief's own prose does not even fit the case: it says "the
verifier reports the trailer failure", and at F6 there may be no trailer
failure at all — the trailer can be perfectly valid behind a corrupt front
block.

Permitted readings:

- **(a) The relief is about the *state*, not the citation.** Its stated reason
  — no F, no live state — holds at F6 and F5, so no total is owed, and the
  verifier reports the absence of one. This is what I implemented, and my
  verifier prints, for a magic/CRC failure, `slack total not owed at all`.
- **(b) The relief is about the *citation*, as written.** §6.2's gates are
  enumerated and F6/F5 are not among them, so the partial-total MUST applies.
  A verifier taking this reading must validate the trailer *after* the
  front-block failure purely to obtain F, then report `slack ≥ F − 16
  (partial), stopped by F6` — which also puts it in tension with
  `[R-CNT-04]`'s "before other processing" ordering and with having elected to
  stop.
- **(c) The walk never began.** §9.7's walk starts "From the live trailer", so
  a verifier that never had one performed no walk, and "the walk does not
  enumerate every region's claimants" is vacuous rather than triggering.
  Same result as (a), by a different route.

I picked (a): the relief's reason, not its citation, is what the sentence is
for, and (b) forces a verifier that has elected to stop to keep working. But
(b) is the literal text, and the document is elsewhere scrupulous about
enumerating exactly which rows sit outside which gate — §21.2's preamble names
F8, F1's trailer-magic instance, F14, and "F6 with F1's front-block instance"
individually as the rows that reach a foreign-major file. That the same care
was not taken here is what makes (b) defensible.

**What an implementer does wrong without it.** Emits a certificate for a
short or front-block-corrupt file carrying a slack figure derived from an
unvalidated trailer, or omits a figure another verifier's report contains, so
two certificates for the same file disagree on whether a slack bound exists.
The narrowest repair is one clause: extend the relief from "§6.2's ordered
validation" to any rejection established before a live trailer, naming
`[R-CNT-04]` and `[R-CNT-27]`.

**Byte-level: no.** Both readings yield *nonconforming* and neither certifies.
No writer's output changes and no file is accepted or rejected differently;
what differs is a field of the report. I considered claiming byte-level on the
grounds that a verifier's report is its output, and rejected it: `[R-CNF-11]`'s
own framing is that the per-requirement and unexamined channels "constrain the
report, not the verdict", and the slack total is the same kind of thing.

### verifier-02 — OBSERVATION

**Location.** §22.3 `[R-SEC-04]`; §8.1 `[R-CNT-19]` (final map row); §18.2
`[R-MTA-10]`; §2.3 `[R-CNF-11]`.

**Title.** The naming duty for bytes a certificate covers uninspected attaches
to unassigned metadata encodings but not to unassigned record types, the worse
of the two residues.

**Quotation.**

> "The extent of a record of a type this specification has not assigned is
> covered by no checksum either (§8.1), so corruption inside it is equally
> invisible ... And the extent of a user-metadata record under an unassigned
> encoding is covered by its terminal CRC but constrained by no content rule
> (`[R-MTA-10]`): the CRC detects corruption and authenticates nothing (§4.5),
> so a certificate covers those bytes uninspected — which is why `[R-MTA-10]`
> makes the verifier's report name each such record, and an operator who wants
> no such bytes rejects on that report line, a policy above conformance."

**Detail.** `[R-SEC-04]` sets the two residues side by side and states the
naming remedy for only the second. `[R-MTA-10]` supplies a MUST — "it MUST
report each record it ignored on this ground, naming the owning scope, the
encoding value, and the stored extent length ... bytes a certificate covers
without inspecting are counted and named, never silent." No corresponding duty
exists anywhere for the extent of a record of an unassigned type, which §8.1's
map covers by **no checksum at all** and §7.2 leaves opaque. A verifier can
therefore certify a file whose bytes are, say, 90% an experimental record's
extent, and the certificate is obliged to say nothing about it beyond folding
zero of it into the slack total — because those bytes are *claimed*, not slack.

Readings: (a) the naming duty is `[R-MTA-10]`'s alone and no report line is
owed — correct on the keywords, since §2.3's report duty runs to requirements
the verifier "was unable to check on a capability or resource ground" and here
there is no requirement to be unable to check; (b) `[R-SEC-04]`'s stated
principle governs both classes and the verifier names both. I picked (a): there
is no MUST, and §21.7's reasoning ("no file-level witness exists to check, so
nothing about the file is left undetermined") applies.

I file this as an OBSERVATION rather than an AMBIGUITY because the normative
answer is decidable and cheap — the cost is not in deciding it but in what the
decision leaves the certificate unable to say. The consequence is concrete: the
operator policy §22.3 explicitly endorses ("an operator who wants no such bytes
rejects on that report line") is unavailable for the class with no checksum,
and two verifiers will produce certificates that differ in whether these bytes
are mentioned at all.

**What an implementer does wrong without it.** Nothing, in conformance terms.
But a pipeline built on the §22.3 policy will silently pass files it was
designed to catch, because the report line it filters on exists only for
metadata records.

**Byte-level: no.** No rule attaches to those bytes in either reading, so no
writer's output and no accept/reject verdict changes; the difference is
confined to what a certificate enumerates.

---

## 9. Confidence

**High** that a verifier built from this document alone interoperates on
verdicts and on the register's 121 rows. Every check I needed was locatable,
every worked constant reproduced, the register's own arithmetic (121/273) is
exact, and the two hardest pieces of verifier-only machinery — the
claimant-discard rule and the byte-set semantics of the partial total — are
both decided in the text, in ways a careless implementer would get wrong and a
careful one will find.

Where I would expect two independent verifiers to differ is in the *shape of
the report* on files that stop the walk early, which is the subject of both
findings and of neither's byte-level claim.
