# Cleanroom round 29 — Adversary transcript

## 0. Access, disclosure, and setup

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,697 lines, read in four `Read` calls covering lines 1–700, 700–1400, 1400–2099,
2099–2799, 2799–3498, 3498–4198, 4198–end). I opened no other file, listed no
directory, ran no `git` command, and made no network request. All my other tool calls
were Python scripts that read only that one file (or nothing at all) and wrote only
into my own scratch directory.

Files I wrote, all in
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-round/scratch/adversary/`:

- `adv_crc.py` — an independent CRC-32C (Castagnoli, reflected, init/final 0xFFFFFFFF)
  and every checksum constant the document states.
- `adv_rows.py` — reads the spec, extracts every `| F#/L#/T#/R# |` register row, and
  counts rows and semicolon-separated instances.
- `adv_build_pq.py` — builds the 256-byte attack file of finding adversary-01 and
  prints its full hex dump.

**Unrequested context.** Material appeared in my context before I began: a project
instruction file (`CLAUDE.md`, which points at an `AGENTS.md`), a user-memory index
listing several memory-file names, and a `git status` snapshot naming top-level
repository entries. I did not open any of it and I have not used any of it. I note two
things it revealed that the brief did not, because paths are context:

1. The instruction file's own path is under a directory named `.../GitHub/tarn/`, while
   the spec I was told to read is under `.../GitHub/tarn-first-draft/`. Two directories,
   not one. I read only the path the brief gave.
2. The `git status` snapshot named `docs/`, `spec/`, `PLAN.md`-adjacent files and
   `OPEN-QUESTIONS.md` as untracked. I did not open them.

I disclose these rather than pretending the context was clean. Nothing in my findings
derives from any of it; every finding below is anchored to a quotation from
`spec/tarn.md` and to arithmetic I ran myself.

---

## 1. Warm-up: reproducing the document's own numbers

Before attacking I re-derived everything checkable, so that a later "the document is
wrong here" carries weight.

### 1.1 Checksums (`adv_crc.py`)

| Quantity | Document | Mine |
|---|---|---|
| CRC-32C("123456789") (§4.5) | `0xE3069283` | `0xe3069283` |
| CRC-32C of zero bytes (§4.5) | `0x00000000` | `0x0` |
| CRC over 4 sentinel entries, 80 bytes (§7.4 example) | `0x80A34955` | `0x80a34955` |
| crc_of_crc_array over `55 49 A3 80` (§7.4) | `0xC4EE982E` | `0xc4ee982e` |
| CRC of a full 2¹⁶-sentinel segment (§15.4, App. B) | `0xEECB3BB2` | `0xeecb3bb2` |
| Appendix A minimal-file trailer CRC over [0,60) | `0x402F157E` | `0x402f157e` |

All six reproduce. My CRC implementation is therefore the document's, which matters for
adversary-01's constructed file.

### 1.2 Register counts (`adv_rows.py`)

§21.8 states "120 conditions over 275 instances". Parsing the four register tables and
counting a `—` cell as one instance and otherwise semicolon-separated entries:

- §21.2 file scope: 35 rows / 56 instances (header says "35 conditions" ✓)
- §21.3 layer scope: 49 rows / 116 instances (header says "49 conditions" ✓)
- §21.4 tile scope: 26 rows / 55 instances (header says "26 conditions" ✓)
- §21.5 ignored records: 10 rows / 48 instances (header says "10 conditions" ✓)
- **Total 120 rows / 275 instances — exactly §21.8's figures.**

The F11 gap is deliberate and the note at line 3680 says so; my parser counts labels,
not the numeric span, so the gap does not perturb the total.

### 1.3 Worked examples

I re-derived every numeric example in the document. All reproduce:

- §7.4's layer-record payload: 4 + 34 + 18 + 12 + 13 = 81 bytes; the offsets in the hex
  listing run 0,4,5,7,9,11,19,27,35,36,38,40,48,56,63,68,69,77 and 77 + 4 = 81 ✓.
  extent slot length 4·20 + ⌈4/2¹⁶⌉·4 = 84 ✓.
- §11.2/§11.4: G=(4,8), N=32, P=65,536; (300,700) → tile (1,2), s = 10, in-tile
  (44,188), ordinal 44·256+188 = 11,452; planar C=4 channel 2 → 2·32+10 = 74 ✓.
- §14.2: Q=3, decoded 18, ordinal 5 at [15,18); planar `b` 12 bytes, ordinal 5 at
  10–11; float32+bool Q=5, decoded 30, ordinal 5 at [25,30) ✓.
- §14.3: P=10 alternating → `55 01`; fill true → `55 FD` (0x01 | 0xFC) ✓.
- §14.5: extents (5,5) tiles (4,4), edge tile (1,1) has exactly one real position (4,4)
  and 15 padding; uint16 fill 0xABCD → 32 bytes, values 1–15 each `CD AB` ✓.
- §15.4: entry_count 1,000,000 → 16 segments (15 full + 16,960); array 64 bytes; region
  20,000,064; k=999,999 at segment-relative 20·16,959 = 339,180; segment 15 spans
  [19,660,800, 20,000,000); 339,200 bytes ≈ "~339 KB"; full segment 65,536·20 =
  1,310,720 = 1.25 MiB ✓. Planar example: 74·20 = [1,480,1,500); channel 3 block
  [96,128) ✓.
- §17.3: shuffle of 1.0,2.0,3.0 float32 → `00 00 00 00 00 00 80 00 40 3F 40 40`; I
  recomputed the permutation byte i of group j → offset i·n+j and got the identical
  twelve bytes ✓.
- §9.3's Note: 2⁶³−1 = 9,223,372,036,854,775,807; the largest multiple of 64 at or below
  it is 2⁶³−64 = 64·(2⁵⁷−1) ✓.
- §21.9's Note: 2³² entries → 2¹⁶ segments → 2¹⁸ = 256 KiB array; 2³⁶ → 2²² = 4 MiB ✓.
- §20.3's example: 32·20 + 4 = 644 ✓.
- Appendix A: every field of the 128-byte file, CRC included, reproduces ✓.

Nothing in the document's arithmetic is wrong. That is a real result and I record it.

---

## 2. Attack surface walked, and what closed each attack

I worked the charter's surfaces in order. Where an attack failed I name the sentence
that killed it; those are collected in `rejected_candidates` as well.

### 2.1 The degenerate-but-legal file

Built mentally: the 128-byte file of Appendix A; a file with one layer, one dimension of
extent 0, one channel, entry_count 0, extent slot (0,0), crc_of_crc_array 0. Both are
foreclosed as conforming by `[R-GEO-02]`, `[R-CNT-17]`'s "(and 0 when entry_count is 0)",
`[R-CNT-23]`'s "a nonzero crc_of_crc_array with entry_count = 0", and §21.6's "A
dimension has extent 0" row. No fork.

Degenerate slab: S = 5, A_slab = 1 on a layer with entry_count 0. `[R-SLB-02]`'s blocks
are empty, `[R-SLB-03]`'s "A run with no stored tiles imposes nothing" applies. Legal and
vacuous. No fork.

Degenerate packed bool: P = 1 planar. §14.4's Note already works the case — "At P = 1 the
two are the same length and `[R-SER-05]` fixes the planar pad bits to the channel's fill,
so the images coincide exactly when that fill is false." I verified: planar byte is
`0x01 | (fill? 0xFE : 0x00)`, interleaved byte is `0x01`. Correct.

### 2.2 Boundary values on every offset, count and alignment

- extent ending exactly at F−64: permitted (`[R-CNT-13]`, T9, and §9.7's "[16, F − 64)").
- dir_offset = 16, dir_length = 4: the minimum, Appendix A.
- dir_length = 5: record sequence of 1 byte, cannot hold a 24-byte header → F29.
- extent_length = 4 on a user-metadata record: F22 / L11.
- entry_count = 2⁶³−1 with a 44-byte file: `[R-CNT-17]`'s formula ties extent_length to
  entry_count and `[R-CNT-13]` ties extent_length to F; §22.2's Note says exactly this.
  No fork.
- offset = 0xFFFF_FFFF_FFFF_FFFE in an index entry: non-sentinel, bit 63 set → T11, whose
  cell says "the value being distinct from the all-ones sentinel". Clean.
- A = 256 (below the 512 floor): L39. A = 2⁶³: L39 ("above 2^62").
- The one boundary that did fork is §2.3's designated-quantity ceiling — see §3.1 below.

### 2.3 Two structures claiming the same bytes

I worked every pairing: stored-tile × own layer's index region (reject-layer, L18);
stored-tile × another layer's structure (reject-file, F33); record extent × directory
region (F33, whose cell names "directory region" explicitly); index region × directory
(F33); sub-record extent × sub-record extent of the same layer (`[R-CNT-13]`'s
"intra-layer overlap", L18). `[R-CNT-13]`'s three-way split and §15.3's three overlap
rows agree at every boundary I could construct. F33's parenthetical even resolves the
one case where a bounds row pre-empts overlap: "a record extent slot of (0, N) with N
nonzero reaches the block through its zero offset and is theirs rather than F31's or
L16's." No fork.

### 2.4 Structures outside the file, and the pre-trailer gap

`[R-CNT-05]` says "A verifier MUST treat a structure in that gap as a validity error at
file scope" (F7). I tried placing a layer's tile-index region between the directory's end
and the trailer: F7 fires, both verifiers reject. I tried a *superseded* trailer there —
the state a commit that re-points at a prior generation's directory would leave. That is
**not** a structure: §5.2 defines a structure as a member of the live committed state,
and §5.2 makes "everything an earlier commit superseded" slack. So F7 does not fire, and
the resulting file is conforming. This is the construction I used in §4 below to confirm
that `[R-LIF-02]` step 3 is unwitnessed — a "the test works" result, not a defect.

A gap longer than step 5's pad: `[R-CNF-02]` names it explicitly as a writer obligation
"whose violation this specification expressly declares not to be a file-conformance
violation". Foreclosed.

### 2.5 Reserved / unknown / experimental values in every position

I enumerated the eight spaces of §10.2 against their defining sections. Every partition
matches: linearization (§11.4 splits 2–3 and 4–0x7FFF, table shows 2–0x7FFF), sample type
(§12.2 splits 14–19 and 20–0x7FFF, table shows 14–0x7FFF), codec, filter, index encoding,
metadata encoding, record type, channel layout (no experimental range, u8 too narrow).
Register rows L31/L33/L34/L36/L43/L45/R1/F35/F36/L24/L25 cover them; §21.6 records the
two conforming refusals (foreign major, experimental top-level MU = 1).

All sixteen record-flag combinations: MU/PE = 11 legal; 01 legal for unregistered types;
10 → F25/L46 (verifier); 00 legal for unregistered types, F28/L49 for registered ones;
any of bits 2–15 → F26/L47. `[R-CNT-22]` fixes reader behavior ("A reader MUST apply a
known type's specified semantics regardless of its stored MU and PE bits"), so no two
readers diverge. No fork.

### 2.6 The reader/verifier seam

The seam is real and repeatedly exercised, but every instance I could build is licensed
rather than ambiguous:

- **Front block residency.** `[R-CNT-04]` lets a non-resident reader "defer or omit" the
  check; §2.3 and Appendix H say a verifier holds no such exemption. So a local reader
  rejects and a remote reader serves — but both verifiers must check, so verifiers agree.
- **`[R-SER-08]`'s resolved boolean byte.** Reader A rejects the tile under `[R-CNF-12]`,
  reader B returns "true". Both conforming, on a nonconforming file. Licensed.
- **A verifier's resource decline.** A file whose user-metadata document decodes to
  20 MiB: verifier A (32 MiB bound) certifies, verifier B (16 MiB bound, the §21.9 floor)
  reports *cannot establish* and MUST NOT certify. Different outputs, but `[R-MTA-09]`
  says in terms that "the bound is that verifier's capability and not a limit on validity
  (`[R-CNF-10]`), so the decline is not a finding that the file is nonconforming". So
  neither says *nonconforming*, and the divergence is designed. Same for a top-level
  experimental MU = 1 record: `[R-CNT-15]` obliges rejection, §2.3 routes an
  unimplemented MU = 1 type to *cannot establish*, and §21.6 records the file as
  conforming.

These are all foreclosed. The one place the seam did fork is `[R-SER-02]`, below.

---

## 3. The surviving attack

### 3.1 A 256-byte file two conforming verifiers judge differently — is P·Q a designated quantity in a *planar* layer?

**The text at issue.** §14.2, `[R-SER-02]`:

> The image's byte length — the **decoded size** — and each value's byte offset follow:
>
> | Layout | Decoded size | Offset of value k |
> |---|---|---|
> | planar, numeric channel c | P · Bᶜ | k · Bᶜ |
> | interleaved | P · Q | (k div C) · Q + F_{k mod C} |
>
> where Bᶜ is channel c's element size (§12.1; 1 for bool), Q = Σ Bᵢ over all channels
> (the **sample stride**), and Fᶜ = Σ Bⱼ over channels j < c (channel c's in-sample
> offset). **These products and sums are declaration-derived quantities under
> `[R-ENC-04]`.**

and `[R-ENC-04]`:

> A reader — including any updater or verifier, which are readers of the files they
> process — MUST treat any quantity this specification **designates** a
> declaration-derived sum or product of integers obtained from a file … whose
> mathematical value would exceed 2⁶³ − 1 as a validity error at the owning scope …

**The construction.** A planar layer with two float64 channels and a single enormous tile
extent, in which every derived quantity is inside the domain *except* P·Q, and P·Q
exceeds 2⁶³ − 1 by exactly one.

- rank d = 1; dimension `x`, extent E₀ = 1, tile extent T₀ = 2⁵⁹ = 576,460,752,303,423,488
- layout = 2 (planar); linearization = 1; codec = 1 (none); filter = 1 (none)
- A = 0, S = 0, A_slab = 0
- C = 2 channels `a`, `b`, both type 13 (float64, Bᶜ = 8), fill eight zero bytes each
- index_encoding = 1, entry_count = 2, both entries the sentinel

Derived (`adv_build_pq.py`, printed):

| Quantity | Value | ≤ 2⁶³ − 1? |
|---|---|---|
| G₀ = ⌈1 / 2⁵⁹⌉ | 1 | ✓ |
| N = ∏Gᵢ | 1 | ✓ |
| P = ∏Tᵢ | 2⁵⁹ = 576,460,752,303,423,488 | ✓ |
| addressed tiles C·N | 2 | ✓ |
| N·P | 2⁵⁹ | ✓ |
| P·Bᶜ (each plane's decoded size) | 2⁶² = 4,611,686,018,427,387,904 | ✓ |
| Q = ΣBᵢ | 16 | ✓ |
| Fᶜ | 0, 8 | ✓ |
| entry_count·20 + ⌈entry_count/2¹⁶⌉·4 | 44 | ✓ |
| max interleaved value offset (k div C)·Q + F | 9,223,372,036,854,775,800 | ✓ |
| **P·Q** | **9,223,372,036,854,775,808 = 2⁶³** | **✗ by 1** |

Everything else is inside the domain; only P·Q trips, and it trips by one. That isolation
is what makes this a usable vector rather than a muddle.

**The file.** 256 bytes, produced by `adv_build_pq.py`:

```
0000  89 54 41 52 4E 0D 0A 1A 00 00 00 00 00 00 00 00
0010  FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
0020  00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF
0030  FF FF FF FF 00 00 00 00 12 1C 83 DE 01 00 03 00
0040  5D 00 00 00 10 00 00 00 00 00 00 00 2C 00 00 00
0050  00 00 00 00 01 70 02 01 00 01 00 01 00 00 00 00
0060  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0070  00 00 00 00 00 01 02 00 01 78 01 00 00 00 00 00
0080  00 00 00 00 00 00 00 00 00 08 01 61 0D 00 08 00
0090  00 00 00 00 00 00 00 01 62 0D 00 08 00 00 00 00
00a0  00 00 00 00 01 02 00 00 00 00 00 00 00 C2 32 C6
00b0  78 9A 7A FE A4 00 00 00 00 00 00 00 00 00 00 00
00c0  8A 4E 52 41 54 0D 0A 1A 01 00 00 00 00 00 00 00
00d0  3C 00 00 00 00 00 00 00 79 00 00 00 00 00 00 00
00e0  00 01 00 00 00 00 00 00 EF CD AB 89 67 45 23 01
00f0  00 00 00 00 00 00 00 00 00 00 00 00 A0 65 67 70
```

Map: front block [0,16); tile-index region [16,60) — two sentinel entries plus one
segment CRC `12 1C 83 DE` = 0xDE831C12, which I computed over the 40 entry bytes;
directory [60,181) holding one layer record (type 0x0001, flags 0x0003, inline_length
0x5D = 93, extent slot (16, 44)) followed by its CRC `9A 7A FE A4`; slack [181,192),
11 bytes; trailer [192,256) with dir_offset 60, dir_length 121, committed_file_length
256, file_id 0x0123456789ABCDEF, reserved zero, CRC 0x706765A0.

I hand-checked the file against every gate that could pre-empt the dispute:
`[R-CNT-27]` (256 ≥ 128), `[R-CNT-06]` (dir_offset 60 ≥ 16; dir_length 121 ≥ 4;
60 + 121 = 181 ≤ 192; F mod 64 = 0; file_id ≠ 0; reserved zero), `[R-CNT-05]` (nothing
between 181 and 192), `[R-CNT-02]`/§9.7 (front, index, directory, trailer disjoint, each
non-terminal claimant inside [16, 192)), `[R-CNT-17]` (44 = 2·20 + ⌈2/2¹⁶⌉·4, and
entry_count 2 = C·N = 2·1), `[R-CNT-23]` (every field in range; fill length 8 = float64
element size; A_slab 0 with S 0; crc_of_crc_array nonzero with entry_count > 0),
`[R-GEO-01]` (d ≥ 1, Tᵢ ≥ 1, C ≥ 1), `[R-ENC-15]` (names distinct in their namespaces),
`[R-IDX-04]` (segment CRC and crc_of_crc_array both computed), `[R-COD-04]` (no
non-sentinel entry, so codec 1's length equality has no subject), `[R-SER-05]` (no stored
tile, so no padding-content obligation), `[R-COD-07]` (codec is 1, not 4).

**Verifier A — reports *nonconforming*.** `[R-SER-02]` says "These products and sums are
declaration-derived quantities under `[R-ENC-04]`" without qualification; P·Q is one of
them; §19.3 obliges the check at layer access; P·Q = 2⁶³ exceeds 2⁶³ − 1; the outcome is
"a validity error at the owning scope", which for a layer's serialization declarations is
the layer (§14's opening). Row L2's cell lists "P·Q" among the sums and products it
registers. Verdict: reject-layer, file nonconforming.

**Verifier B — certifies.** P·Q is the *interleaved* decoded size: the table row that
gives it is labelled "interleaved", and Q is defined as "the **sample stride**", which
§17.3 uses only "for an interleaved tile". This layer is planar; §14.1 gives it V = P
values, §14.2 gives it decoded size P·Bᶜ, and `[R-SER-07]` designates "Every decoded size,
and the value count V". §19.3 states the obligation as "the 2⁶³ − 1 ceiling on every
quantity that arithmetic derives (`[R-ENC-04]`) and on **the decoded sizes** §14 derives
from it (`[R-SER-02]`, `[R-SER-07]`)" — and a planar layer has no decoded size P·Q.
`[R-ENC-04]` itself warns that "an expression this specification writes only inside a
comparison, and names nowhere, is not a designated quantity and no reader is obliged to
form it", and L2's own instance cell separates "P·Q (which dominates V = P·C)" from
"P·Bᶜ", pairing each with its layout — §21.1 says instance enumeration is by layout
precisely where "the quantity a condition derives varies by layout". Verdict: no
violation, certify.

**Which I picked.** I would build Verifier A. §21.1 says "where a row and the rule it
cites diverge, **the rule governs**", and the rule is `[R-SER-02]`'s unqualified sentence.
But I would not expect a second implementer to reach it: both §19.3's gloss and L2's
instance split point the other way, and an implementer writing planar decoded-size
arithmetic has no occasion to form Q at all.

**Why an implementer gets this wrong.** A planar reader never needs Q. It computes
P·Bᶜ per plane and is done. A validator written from §19.3's checklist will form
"the decoded sizes §14 derives" and stop. The strict reading demands that a planar
validator compute a quantity that appears nowhere in its own decode path solely to
overflow-check it.

**Byte-level.** Yes. Two conforming verifiers hand down opposite verdicts on the 256
bytes above: one *nonconforming*, one *conforming*. And the emittable set moves with it —
under Verifier A's reading no conforming writer may emit this file (`[R-CNF-05]`), under
Verifier B's reading a writer may. This is not a dispute about a SHOULD and it is not a
register row contradicting its rule: it is the rule itself admitting two scopes.

**Variant.** The same fork is reachable with an all-bool planar layer: C = 2 bool
channels, T₀ = 2⁶², P = 2⁶². Then each plane's decoded size is ⌈P/8⌉ = 2⁵⁹, Q = 2, and
P·Q = 2⁶³. Here Q is doubly foreign to the layer — §14.2 says a bool value is
"interleaved layers only, since §14.3 governs planar bool planes — as a single byte …
with element size 1 **in the arithmetic below**", so Bᶜ = 1 is defined only for the
interleaved arithmetic, and §17.3 makes the shuffle stride 1 rather than Q for a packed
plane. A verifier that forms Q there is forming a quantity the document defines only for a
layout this layer does not use.

---

## 4. Putting §21.7's test to requirements

The brief asked for this and it is where the second and third findings came from. I
first wrote the definitions out formally.

§21.7:

> A condition this specification names is **unwitnessed** where, for every file
> exhibiting it, some file that does not exhibit it cannot be told apart from it by any
> check this specification obliges a reader or a verifier to perform. It is **detectable**
> in the contrary case: where some file exhibiting it is separated by such a check from
> every file that does not. The two are stated over the same subject, and each quantifier
> is the other's dual, so each is exactly the negation of the other …

Let `C` be the set of files exhibiting the condition, `K` the set of obliged checks, and
write `f ~ g` for "no check in K gives different results on f and g".

- **Unwitnessed(C)** = ∀f ∈ C. ∃g ∉ C. f ~ g
- **Detectable(C)**, read as the dual = ∃f ∈ C. ∀g ∉ C. ¬(f ~ g)

Those two *are* exact negations, so the duality claim survives — **on that reading**. But
the English of the detectable half is "some file exhibiting it is separated, **by a
check**…, from **every** file that does not", and the singular indefinite most naturally
scopes outside the universal: ∃f ∈ C. ∃k ∈ K. ∀g ∉ C. k separates f from g. That is
strictly stronger than the dual and is *not* the negation of unwitnessed. §21.1 repeats
the same wording. This is finding adversary-03.

Then the operational gloss, three sentences later:

> That is the whole of the test, and it decides any condition put to it without appeal to
> a list: ask whether a breach can be made to leave behind a file no obliged check
> separates from **a conforming one**.

The formal definition quantifies over "every file that does not [exhibit it]" — which
includes nonconforming files exhibiting *other* conditions. The gloss quantifies over
conforming files. These are different tests, and they disagree on conditions the document
has already classified. That is finding adversary-02.

### 4.1 The twelve-plus requirements, worked

I put both readings to each. "Formal" is the ∀f∃g reading; "gloss" is the
breach-vs-conforming-file reading. "Register" is what the document actually does.

| # | Condition | Formal | Gloss | Register | Agree? |
|---|---|---|---|---|---|
| 1 | `[R-CNT-06]` trailer CRC mismatch | detectable | detectable | F14 | ✓ |
| 2 | `[R-ENC-15]` two byte-identical layer names | detectable | detectable | F4 | ✓ |
| 3 | `[R-CNT-13]` two claimants overlap | detectable | detectable | F33/L18 | ✓ |
| 4 | `[R-SLB-01]` stored tile not A-aligned | detectable | detectable | L40 | ✓ |
| 5 | `[R-MTA-05]` unsorted document members | detectable | detectable | F27/L48 | ✓ |
| 6 | `[R-CNT-22]` registered type's stored flag differs | detectable | detectable | F28/L49 | ✓ |
| 7 | `[R-COD-06]` undisclosed dictionary | **unwitnessed** | **detectable** | absent | ✗ gloss |
| 8 | `[R-COD-10]` mis-strided filter, no structural constraint | unwitnessed | unwitnessed | absent | ✓ |
| 9 | `[R-ENC-06]` fixed field widths | no exhibitable condition | same | absent | ✓ |
| 10 | `[R-CNT-18]` sub-record nesting depth > 2 | unwitnessed | unwitnessed | absent (note says so) | ✓ |
| 11 | `[R-SLB-04]` stale slab declaration carried forward | **unwitnessed** | detectable | absent (note says so) | ✗ gloss |
| 12 | `[R-LIF-02]` step 3 (trailer re-pointed at a prior directory) | unwitnessed | unwitnessed | absent | ✓ |
| 13 | `[R-WRT-06]` compactor's fresh file_id / carried flag bits | unwitnessed | unwitnessed | absent (§20.5 says so) | ✓ |
| 14 | §20.3's §14 bar (declaration change reaching a superseded stored tile) | unwitnessed | unwitnessed | absent (§20.3 says so) | ✓ |
| 15 | §20.3's planar disk-ordinal bar | unwitnessed | unwitnessed | absent | ✓ |
| 16 | `[R-CNT-04]` front block not byte-identical | detectable | detectable | F6 | ✓ |
| 17 | `[R-MTA-09]` content-size ≠ decoded document length | detectable | detectable | R4 | ✓ |
| 18 | `[R-COD-02]` tile not independently decodable | **unwitnessed** | detectable | **T13 present** | ✗ formal |
| 19 | `[R-COD-05]` deflate carried in a zlib/gzip wrapper | **unwitnessed** | detectable | **T15 present** | ✗ formal |
| 20 | `[R-COD-05]` a second DEFLATE stream in the extent | **unwitnessed** | detectable | **T16 present** | ✗ formal |
| 21 | `[R-COD-07]` lz4 *frame* instead of a raw block | **unwitnessed** | detectable | **T23 present** | ✗ formal |
| 22 | `[R-COD-10]` mis-stride that breaks padding or bool bytes | **unwitnessed** | detectable | **T26 present** | ✗ formal |

Twenty-two conditions. Fifteen are decided identically by both readings and agree with
the register — that is the account of where the test works, and it is why I trust the
seven disagreements.

### 4.2 Working the disagreements

**Rows 18–22, the "cause" rows.** Each of these five rows says of itself, in the
register's own Condition cell, that it has no check of its own:

> T13 … the decode needs state or side data outside the extent; **the check that detects
> it is T25's, and this row records the cause rather than a procedure of its own**

Take T13 and the formal test. Let f be a file whose stored deflate stream carries a
back-reference into a previous tile's history window; it fails `[R-COD-08]`'s decode.
Now let g be a file identical to f except that the same tile's stored bytes are a
differently-malformed deflate stream — an invalid Huffman table, say — with the entry's
crc recomputed and the length unchanged. g does **not** exhibit T13 (nothing outside the
extent is needed; the stream is simply broken). Every obliged check gives the same result
on f and on g: the trailer, directory, layer, index chain and entry crc all pass on both,
and the decode fails on both. So f ~ g, and g ∉ C. This construction works for every
f ∈ T13. Therefore T13 is **unwitnessed** under the formal test — and §21.7 says "The
register carries a row for a condition **exactly where** it is a detectable
file-conformance violation, so an unwitnessed condition is absent from it". T13 is
present. The same argument, verbatim, kills T15 (pair it with a corrupt raw stream), T16
(pair it with trailing garbage that is not a second stream), T23 (pair it with a corrupt
block) and T26 (pair a mis-strided filter that spoils padding with a correctly-strided
tile whose padding bytes were simply written wrong — both fail T4's check).

Under the gloss all five are detectable: each breach fails a check that every conforming
file passes. So the gloss agrees with the register on rows 18–22, and the formal
definition does not. That is one half of adversary-02, and adversary-04 states the
consequence for §21.1's completeness clause.

**Row 7, the undisclosed dictionary.** Now the disagreement runs the other way. §21.7
names this as its paradigm unwitnessed condition, and `[R-COD-06]` says "Dictionary use
the header does not disclose is not detectable by inspection and need not decode to an
error". Under the formal test that is right: for any f compressed against an undisclosed
dictionary, either f decodes cleanly (pair it with a conforming file carrying different
content) or it fails the decode (pair it with an ordinarily corrupt frame). Either way
some g ∉ C is indistinguishable. Under the **gloss**, though, the question is whether the
breach *can be made* to leave a file no check separates from a conforming one, and a
great many dictionary-compressed frames fail T25's check outright — so under the gloss
some f ∈ C is separated from every conforming file, and the condition is detectable and
owes a register row it does not have. The gloss therefore mis-classifies the one
condition §21.7 uses as its worked example.

**Row 11, the stale slab declaration.** This is the sharpest of the seven, because the
document handles the identical structural situation two ways in two places. §16.2's Note:

> Because this rule's detection *is* `[R-SLB-03]`'s, a stale declaration carries no
> register row of its own: every file exhibiting one exhibits a run whose tiles are
> unpacked or whose first stored tile is misaligned, which §21.3 registers.

That is exactly T13's situation — a condition whose detection *is* another row's — and
here it yields **no row**, while there it yields a row. §7.4's nesting Note takes the
§16.2 side too ("it has no reader-detectable witness, and so no register row"), and
§9.5's residue Note takes it a third time ("Residue past a completed commit carries no
register row of its own"). Three passages decline a row on the ground that another row's
check is what detects the condition; five rows in §21.4 take a row on that same ground.
Both cannot follow from one test.

### 4.3 A condition the test does not decide at all

The instrument is "the checks this specification obliges a reader or a verifier to
perform", and §21.7 is careful to say it is "deliberately not the register's own rows".
But §2.3 defines a verifier as "A reader that additionally checks **every file-level
requirement**". So the obliged-check set for a verifier is "every file-level requirement",
and a violation of a file-level requirement is therefore checked by definition — which
would collapse the unwitnessed class entirely. The document blocks the collapse in one
sentence, §21.7's "no file-level witness exists to check, so nothing about the file is
left undetermined" — i.e., a requirement can be file-level and yet present nothing to
check. That is coherent, but it means the test's instrument is not "the obliged checks"
simpliciter; it is "the obliged checks that have a witness", and *that* is the notion
being defined. I could apply the test only by supplying that reading myself. I record it
as an observation on the test's applicability rather than as a separate finding, since
§21.7's sentence does close it once the reader supplies the step.

---

## 5. The other changed sections

### 5.1 §20.3's §14 bar — the list versus the test

The bar:

> A commit MUST NOT change a layer's declarations in a way that alters, for any tile that
> layer stores **in the generation this commit supersedes**, what §14 fixes for its stored
> bytes or how they decode — the set of padding positions (§11.3) and the content
> `[R-SER-05]` fixes there, the decoded size, the byte offset of any sample within the
> decoded tile image, the sample type each value in the image is read under, or the codec
> and filter that produced the stored bytes. Call this the **§14 bar**.

I put a permutation to it. Interleaved layer, two channels `a` and `b`, both uint8, both
with fill `0x00`, extents an exact multiple of the tile extents so there are no padding
positions, one stored tile. A commit swaps the two channel entries.

Against the list, item by item:

- set of padding positions — none, unchanged;
- content `[R-SER-05]` fixes there — no padding positions, and the fills are equal anyway;
- decoded size — P·Q with Q = 1 + 1 = 2, unchanged;
- **byte offset of any sample** — §3.1 defines a sample as "the tuple of one value per
  channel at one coordinate", and §14.2's example says "its sample occupies bytes
  [15, 18)", so a sample's offset is (k div C)·Q. A permutation does not move it. What
  moves is Fᶜ, the offset of a *value*, and the list does not name values here;
- sample type each value is read under — value 0 was uint8 and is uint8. Unchanged;
- codec and filter — unchanged.

So nothing in the list changes, and the ordinal bar beside it is explicit that "An
interleaved layer is unaffected, its disk ordinal being s, which no channel declaration
enters." Yet the stored tile now denotes a different array: byte 0 of each sample was
written as the channel named `a` and is now read as the channel named `b`.

The bar survives because the general test does the work the list does not: §14.1 fixes
that "value k of the sequence is channel (k mod C)'s value", so a permutation alters what
§14 fixes, and §20.3 says in terms that "the list names where that effect arises rather
than standing on its own". I checked that the same subordination is load-bearing in the
other direction too — a growth *does* change "the set of padding positions" of a stored
edge tile, and §20.3 permits growth anyway — so the list is genuinely illustrative at
both ends.

What is left is a reporting-grade point, not a fork: the list reads as an apposition, the
document names the whole thing "the §14 bar" and then refers to it a dozen times as a
test, and the one list item that would catch a permutation names the wrong quantity
(sample, not value). An implementer who codes the list gets a wrong answer on a legal
input. I file it as adversary-05, OBSERVATION, not byte-level, because the general test
forecloses the permissive reading.

### 5.2 §11.1's Rationale, checked against §20.3

§11.1's Rationale is labelled *Rationale* and so is non-normative under `[R-CNF-01]`, but
it restates §20.3 and I checked every clause:

- "a growth raising one grid count ⌈Eᵢ / Tᵢ⌉ while another stays 0 among them, the product
  holding at 0" — correct: N = ∏Gᵢ and any Gᵢ = 0 zeroes the product.
- "the growth that raises a zero-extent layer's **last** zero grid count included" — I
  censused "last" elsewhere in the document; §11.4 uses "the last-declared dimension" for
  linearization, which is a different sense. Here it can only mean the final surviving
  zero grid count, and on that reading it is correct: entry_count goes 0 → N.
- "The other bar reaches neither a shrink nor a growth: it bars a change to a planar
  layer's channel declarations that moves a stored tile's disk ordinal" — matches §20.3
  word for word in scope. A geometry growth *does* renumber ordinals (I checked: with
  G = (2,2) a tile at grid (1,0) has s = 2, and after G = (2,3) it has s = 3), but that is
  a geometry change, not a channel-declaration change, and §20.3 step 4 handles it: "a
  geometry change renumbers ordinals wherever `[R-GEO-06]` moves them".
- "A layer that stored no tile in the generation the commit supersedes may be re-declared
  freely; a layer the commit itself empties does not qualify" — matches §20.3's "the tense
  is both bars', so a commit does not earn this permission by emptying the layer as it
  re-declares it".

No divergence. I looked hard here because a non-normative gloss that disagrees with the
normative text is itself reportable, and this one does not disagree.

### 5.3 §18.2's carry-over from `[R-COD-06]`

I enumerated `[R-COD-06]`'s seven frame constraints and matched each against §18.2's
"save two" and against R4's sixteen instances:

| `[R-COD-06]` constraint | §18.2 | R4 |
|---|---|---|
| frame magic | carried | 2 instances |
| no skippable frame | carried | 2 |
| no second frame | carried | 2 |
| no dictionary use, undisclosed | carried, but unwitnessed | none — §18.2 says so |
| no nonzero Dictionary_ID | carried | 2 |
| no content-checksum flag | carried | 2 |
| declared window ≤ tile decoded size | **replaced** (reader's own bound) | none |
| content size = tile decoded size | **replaced** (= decoded document length) | 4 |
| no sizing a buffer from a declared length | carried, binds a reader | none — §18.2 says so |
| no bytes after the frame (from `[R-COD-08]`) | carried via "occupying the extent's bytes before its terminal CRC" | 2 |

2+2+2+2+2+4+2 = 16, which is exactly R4's instance count and matches my mechanical count
in §1.2. The two exclusions §18.2 names — undisclosed dictionary and the buffer-sizing
bar — are the two it says "fall outside the register, on the two distinct grounds §21.7
separates", and both classifications are right under §21.7's *formal* reading (the first
is unwitnessed, the second states no condition a file can exhibit). Under the gloss the
first is wrong, which is more evidence for adversary-02, but §18.2 itself is internally
consistent. No fork here.

I also checked the Single_Segment_Flag paragraph: with the flag set there is no
Window_Descriptor and RFC 8878 makes Window_Size the content-size field, which §18.2 pins
to the decoded document's byte length — so a >8 MiB document framed that way exceeds
§21.9's Window_Size row and falls outside `[R-CNF-03]`'s acceptance duty. That is what
§18.2 says, and it is arithmetically consistent. The mirror note in §17.2 for tiles
("the Window_Descriptor cannot express less than 1 KiB", so a sub-1-KiB tile is
encodable only as a single-segment frame) is also correct against §14's worked decoded
sizes of 18, 30 and 2 bytes.

### 5.4 §21.1's specialization list

I checked each named pair for strict containment: F1's front-block instance ⊂ F6 ✓;
F1's trailer-magic instance ⊂ F8 ✓; F35 ⊂ F36 ✓; L24 ⊂ L25 ✓; F21 ((0,0), so
extent_length 0) ⊂ F22 (extent_length < 5) ✓; L10 ⊂ L11 ✓. All six hold. I then looked
for unlisted pairs that would matter: L46's layer-record instance (MU = 1, PE = 0) ⊂
L49's "layer record flags bit 1" instance, since a layer record's registry-fixed PE is 1;
that is a strict specialization the list omits, but the list is expressly "not offered as
closed" and both rows carry the same detector, tier and outcome, so nothing turns on it.
F25 and F28 merely overlap (an unregistered type with MU = 1, PE = 0 exhibits F25 and not
F28), and §21.1's "Rows that merely overlap, each reachable without the other, do not
stand in it" is the right verdict.

I also checked §21.2's reach derivation. `[R-CNT-24]` fixes three invariants: the trailer
magic at F−64, version_major/minor at F−56, and a CRC-32C at F−4 over [F−64, F−4), plus
the constancy of the front block. Rows asserting exactly those: F8, F1-trailer, F14, F6,
F1-front. §21.2 names "F8, F14, F6 and both of F1's instances … and no other row" —
correct. I confirmed F13 (committed_file_length not a multiple of 64) does **not** reach,
since 64-alignment of F is nowhere in `[R-CNT-24]`, and confirmed that F8 and F14 remain
checkable in a foreign major because F is the transport-authoritative physical size
(§19.1 step 1), not the redefinable committed_file_length field.

---

## 6. Findings

### adversary-01 — AMBIGUITY, byte-level

**Location.** §14.2, `[R-SER-02]`; read against §4.2 `[R-ENC-04]`, §19.3 `[R-RDR-03]`,
§14.1 `[R-SER-01]`, §14.3 `[R-SER-07]`, §17.3 `[R-COD-10]`, and §21.3 row L2.

**Quotation.** "where Bᶜ is channel c's element size (§12.1; 1 for bool), Q = Σ Bᵢ over
all channels (the **sample stride**), and Fᶜ = Σ Bⱼ over channels j < c (channel c's
in-sample offset). These products and sums are declaration-derived quantities under
`[R-ENC-04]`."

**Permitted readings.** (a) Every product and sum in §14.2 — P·Bᶜ, k·Bᶜ, P·Q, the
interleaved offset expression, Q and Fᶜ — is designated for every layer, so a verifier
must form P·Q and overflow-check it in a planar layer. (b) The designation follows the
table's layout keying, so P·Q and the interleaved offset expression are designated only
for an interleaved layer, and a planar layer's designated quantities are P·Bᶜ (or ⌈P/8⌉)
and V = P.

**Which I picked, and why.** (a), because §21.1 says the rule governs over the row and
`[R-SER-02]`'s sentence carries no layout qualifier. But (b) is defensible from §19.3's
gloss ("the 2⁶³ − 1 ceiling … on **the decoded sizes** §14 derives"), from L2's
layout-keyed instance split, and from `[R-ENC-04]`'s own warning against forming
quantities the specification does not name for the case at hand.

**What an implementer does wrong.** A planar validator never forms Q — it has no use for
the sample stride — and so ships without the check. Against Verifier A that validator
certifies a file Verifier A calls nonconforming.

**Byte-level rationale.** Verifier A and Verifier B return opposite verdicts on the
concrete 256-byte file dumped in §3.1 above: A reports *nonconforming* (L2, reject-layer,
P·Q = 2⁶³ against a ceiling of 2⁶³ − 1), B certifies. The emittable set moves with the
verdict: under A no conforming writer may emit those bytes (`[R-CNF-05]`), under B a
writer may.

### adversary-02 — CONTRADICTION, not byte-level

**Location.** §21.7 `[R-ERR-01]`; the same wording is restated in §21.1.

**Quotations.** Formal definition: "It is **detectable** in the contrary case: where some
file exhibiting it is separated by such a check from every file that does not."
Operational gloss, three sentences later: "That is the whole of the test, and it decides
any condition put to it without appeal to a list: ask whether a breach can be made to
leave behind a file no obliged check separates from a conforming one."

**The defect.** The formal definition quantifies over *every file that does not exhibit
the condition* — a class that includes nonconforming files exhibiting other conditions.
The gloss quantifies over *conforming* files. These are different tests, they are
presented as the same test ("That is the whole of the test"), and they return opposite
answers on conditions the document has already classified. §4.1's table works
twenty-two conditions; they disagree on seven. Under the gloss, `[R-COD-06]`'s
undisclosed dictionary — §21.7's own worked example of an unwitnessed condition — is
detectable and owes a register row it does not have. Under the formal definition,
T13, T15, T16, T23 and T26 are unwitnessed and owe the absence of the rows they have.
Neither reading is consistent with the register as it stands.

**What an implementer or editor does wrong.** The test is the instrument §21.1's normative
completeness clause turns on and the gate `[R-CNF-07]` applies. Applied by the gloss, a
reviewer adds rows for undisclosed-dictionary use and for stale slab declarations that
the document deliberately excludes; applied by the formal definition, a reviewer deletes
five rows in §21.4 and the corpus counts in §21.8 and `[R-VEC-03]` change with them.

**Byte-level rationale.** No. Whichever way the test is resolved, the register's presence
or absence of a row does not change an actor's obligation: §21.1 says "each row *restates*
its governing rule, and where a row and the rule it cites diverge, **the rule governs**",
and every one of the five disputed rows routes detection to a check another rule already
obliges (T25's, T24's, T2's, T4's). No accept/reject verdict and no emitted byte moves.

### adversary-03 — AMBIGUITY, not byte-level

**Location.** §21.7 `[R-ERR-01]`, and the restatement in §21.1.

**Quotation.** "It is **detectable** in the contrary case: where some file exhibiting it
is separated by such a check from every file that does not. The two are stated over the
same subject, and each quantifier is the other's dual, so each is exactly the negation of
the other …"

**Permitted readings.** (a) ∃f ∈ C. ∀g ∉ C. ∃k ∈ K. k separates f from g — the reading
under which the duality claim is true. (b) ∃f ∈ C. ∃k ∈ K. ∀g ∉ C. k separates f from g —
a single check separating one file from the whole complement, which the English
"separated, by a check …, from every file that does not" invites, and under which the
duality claim in the very next sentence is false, since ¬(∀f ∃g. f ~ g) is ∃f ∀g ∃k, not
∃f ∃k ∀g.

**Which I picked.** (a), because the document asserts the duality and (a) is the reading
that makes it true. But a reader who trusts the definition's grammar over its following
claim gets (b), and (b) is strictly stronger — it classifies as unwitnessed some
conditions (a) calls detectable.

**What an implementer does wrong.** An editor auditing §21's completeness with reading
(b) drops rows that reading (a) requires. The reading matters because §21.1's completeness
clause is normative and is stated in the same words.

**Byte-level rationale.** No, for the same reason as adversary-02: the reading changes
which conditions the register must carry, not what any actor must do with a file.

### adversary-04 — CONTRADICTION, not byte-level

**Location.** §21.1 (completeness clause) and §21.7, against §21.4 rows T13, T15, T16,
T23, T26; and against §16.2's Note on `[R-SLB-04]`, §7.4's Note on `[R-CNT-18]`, and
§9.5's Note on `[R-LIF-04]`.

**Quotations.** §21.7: "The register carries a row for a condition exactly where it is a
detectable file-conformance violation, so an unwitnessed condition is absent from it by
that clause's own terms rather than in breach of them." §21.4, T13: "the check that
detects it is T25's, and this row records the cause rather than a procedure of its own".
§16.2: "Because this rule's detection *is* `[R-SLB-03]`'s, a stale declaration carries no
register row of its own".

**The defect.** Two passages state opposite policies for the identical structural
situation — a condition whose detection is another row's check. §16.2 declines a row on
that ground; §7.4 declines a row on the neighbouring ground that a prohibition "has no
reader-detectable witness"; §9.5 declines a row for residue past a completed commit on
the ground that "A reader meets it as a trailer that fails its gates … each of which
§21.2 already registers". §21.4 grants a row on that same ground five times over. Under
§21.7's formal test all five of those rows are unwitnessed (§4.2 gives the pairing
construction for each), so the register both carries rows the test says it must not and
declines rows for conditions no different in kind.

**What an implementer does wrong.** §21.8 and `[R-VEC-03]` oblige a corpus vector per
instance — nine instances across the five rows. A corpus author building them cannot
construct a file that exercises T13 rather than T25, or T16 rather than T24, because no
obliged check distinguishes the pair; §24's `[R-VEC-02]` anticipates exactly this
("where a condition cannot be isolated … the entry records every row the file exercises
and says which it was built for"), which is the admission that these rows have no
isolating vector.

**Byte-level rationale.** No. Every one of the five rows routes detection to a check
another rule obliges, and both readings leave that check and its outcome untouched, so no
verdict and no emitted byte changes.

### adversary-05 — OBSERVATION, not byte-level

**Location.** §20.3 `[R-WRT-04]` step 4, the §14 bar's enumerated list; read against
§14.1 `[R-SER-01]`, §14.2 `[R-SER-02]` and §3.1's definition of *sample*.

**Quotation.** "A commit MUST NOT change a layer's declarations in a way that alters, for
any tile that layer stores **in the generation this commit supersedes**, what §14 fixes
for its stored bytes or how they decode — the set of padding positions (§11.3) and the
content `[R-SER-05]` fixes there, the decoded size, the byte offset of any sample within
the decoded tile image, the sample type each value in the image is read under, or the
codec and filter that produced the stored bytes."

**The defect.** The list's third item names the byte offset of a *sample*, and §3.1 makes
a sample "the tuple of one value per channel at one coordinate" — an interleaved sample's
offset is (k div C)·Q, which no channel permutation moves. What a permutation moves is
Fᶜ, the offset of a *value*, and no list item names it. Permuting two interleaved
channels of the same sample type with identical fill bytes therefore changes no item on
the list, and the ordinal bar beside it exempts interleaved layers outright ("An
interleaved layer is unaffected, its disk ordinal being s, which no channel declaration
enters") — while silently reassigning every stored byte to a different channel, so the
layer denotes a different reference array.

**Which reading I picked, and why it is only an observation.** The bar is saved by its
general test, which §20.3 states immediately after: "the list names where that effect
arises rather than standing on its own". §14.1 fixes that "value k of the sequence is
channel (k mod C)'s value", so a permutation does alter what §14 fixes and the bar bites.
The list-only reading is therefore not defensible against the surrounding text — but the
list reads as an apposition, the document then names the construct "the §14 bar" and
refers to it as a test a dozen times, and the one item that would catch a permutation
names the wrong one of the document's own two carefully distinguished quantities.

**What an implementer does wrong.** An updater that codes the enumerated list — the
natural thing to do with a list of five effects introduced by an em-dash — permits a
commit that reinterprets every stored tile of an interleaved layer.

**Byte-level rationale.** No. The general test forecloses the permissive reading, so both
readings converge on "barred", and the resulting file would in any case be conforming in
isolation (the §14 bar is unwitnessed, per §4.1 row 14), so no verifier's verdict moves.

---

## 7. Ranking of surviving attacks

1. **adversary-01.** A real fork on 256 concrete bytes, with both verdicts defensible from
   the document and each backed by a different sentence of it. Most likely of the five to
   be landed on by real implementations, because a planar decode path has no reason to
   form Q at all and §19.3's checklist does not ask it to.
2. **adversary-02** and **adversary-04**, which are one problem seen from two sides: the
   new test in §21.7 does not decide the register the document actually has, and the
   document's own practice on "conditions detected by another row's check" runs both ways.
   No bytes move, but §21.1's completeness clause is normative and the corpus counts in
   §21.8 depend on the answer.
3. **adversary-03.** A quantifier-scope defect in one sentence, self-refuted by the next
   sentence, so an attentive reader recovers the intended reading.
4. **adversary-05.** Reporting-grade: the list is under-inclusive and the surrounding
   prose rescues it.
