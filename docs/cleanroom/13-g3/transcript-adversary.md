# Cleanroom round 13 — Adversary transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`.
I opened no ADR, no `PLAN.md`, no `AGENTS.md`, no `README.md`, no
`conformance/` artifact, no `spec/registry.json`, no git history. I ran no
web search and no web fetch. I did not list or read the output directory.

I ran `wc`, `rg` and `python3` against that one file, plus Python scripts I
wrote myself into my scratchpad (`work1.py`, `work2.py`, `work3.py`,
`tarn.py`, `b1.py`, `atk.py`). Those scripts read no project file except,
in the case of the register-counting script, `spec/tarn.md` itself.

One caveat I want on the record: the task list surfaced in my environment
(not a file I opened) carried three completed-item titles that named
subject matter — a metadata-encoding verifier decision, a §7.4 worked byte
example, and a §21.1 instance-criterion fix. I did not seek those out and
they told me nothing about *what* the text now says, but they are more
than the brief's section list gave me, and a reader weighing my
independence should know I saw them. I had already picked §7.4's example
and §18.2/§21.5 as targets from the brief's changed-section list before I
noticed them; the F33/F7 instance work I did notice first, and I checked
it anyway (§21.8 arithmetic, below) rather than assuming it was sound.

---

## 1. What I built, and why I built it first

The brief's instruction is to implement rather than narrate, so I started
by writing a container writer and a checker straight out of Part I, then
used it to reproduce every number the document asserts. If the document
stands alone, an implementation built from it alone should land on the
document's own bytes. That is the strongest single test available, and it
is cheap.

### 1.1 CRC-32C

§4.5 fixes CRC-32C: Castagnoli 0x1EDC6F41, reflected in and out, init
0xFFFFFFFF, final XOR 0xFFFFFFFF, stored little-endian. The reflected
polynomial is 0x82F63B78. §4.5's check vector is the test:

```
CRC('123456789') = 0xE3069283   (§4.5: 0xE3069283)   OK
CRC(b'')         = 0x00000000   (§4.5: 0x00000000)   OK
```

This is the one constant in the document I could not have derived from
elsewhere in it, and it is stated with a self-test. Good.

### 1.2 Appendix A, byte for byte

I built the 128-byte minimal file from §5.1, §6.1, §6.2, §7.1 and §9.2
without looking at Appendix A's hex, then diffed:

```
front block         [0,16)   89 54 41 52 4E 0D 0A 1A + 8 zero bytes   (§6.1)
directory           [16,20)  CRC-32C of zero bytes = 00 00 00 00      (§7.1, §4.5)
pre-trailer pad     [20,64)  44 zero bytes                            (§6.2, R-CNT-03)
trailer             [64,128) magic, 1, 0, 0, gen 1, 16, 4, 128, id, 0, CRC
```

Result: **byte-identical to Appendix A**, and the trailer CRC I computed
over bytes [64,124) is 0xE00938D2, exactly the document's value. The
64-byte trailer layout in §6.2 packs as `8s H H I Q Q Q Q Q 4x I` = 64
with no slack, which is what [R-CNT-24]'s closing sentence claims ("The
format-major-1 trailer has zero slack: every byte is assigned").

### 1.3 §7.4's worked layer-record example — the newest text in the document

This is material the brief flags as written from scratch and never read
cold, so I built it from the §7.4 field table alone and only then compared.

Packing the table in order — name (u8 len + bytes), layout u8,
linearization u16, codec u16, filter u16, A u64, S u64, A_slab u64,
rank u8, C u16, d dimension entries, C channel entries, index_encoding u8,
entry_count u64, crc_of_crc_array u32 — for the layer `sst`, rank 1,
dimension `x` extent 100 tile extent 32, one interleaved float32 channel
`temp` with fill 0x7FC00000:

```
inline_length = 81                              (§7.4 example: 81)   OK
byte dump matches the example's 19 annotated lines exactly            OK
grid count ⌈100/32⌉ = 4, entry_count = 4        (§11.2, R-CNT-17)     OK
index region = 4×20 + ⌈4/2^16⌉×4 = 84           (§7.4, R-CNT-17)      OK
CRC-32C over the 80 sentinel bytes = 0x80A34955 (§7.4: 0x80A34955)    OK
  stored little-endian as 55 49 A3 80           (§7.4: 55 49 A3 80)   OK
crc_of_crc_array = CRC over that 4-byte array
                 = 0xC4EE982E                   (§7.4: 0xC4EE982E)    OK
```

The example's own cumulative-width prose — "Name and the nine scalars from
layout through channel count occupy 4 + 34 bytes, the dimension entry 18,
the channel entry 12, and the trailing fixed fields 13 — 81 exactly" —
also checks: 1+2+2+2+8+8+8+1+2 = 34 over nine scalars, 4+34+18+12+13 = 81,
and the field offsets in the dump (0, 4, 5, 7, 9, 11, 19, 27, 35, 36, 38,
40, 48, 56, 63, 68, 69, 77) are the exact cumulative sums.

The channel entry it cites "byte for byte" from §12.3 —
`04 74 65 6D 70 0C 00 04 00 00 C0 7F` — is reproduced identically inside
the layer payload at offsets 56–67. The two places agree.

I found **no defect** in this newly authored material. It is the cleanest
worked example in the document.

### 1.4 The all-sentinel segment constant

[R-IDX-05] pins CRC-32C over 2^16 sentinel entries at 0xEECB3BB2. I built
1,310,720 bytes of `FF×16 00×4` and got **0xEECB3BB2**. Appendix B repeats
the same value. OK.

### 1.5 Every other worked example

I checked all of them arithmetically. All correct:

- §11.2: (1024,2048)/(256,256) → G=(4,8), N=32, P=65,536; (1000,2048) →
  G_y = 4 still.
- §11.4: (300,700) → tile (1,2), s = 1·8+2 = 10, in-tile (44,188),
  ordinal 44·256+188 = 11,452; planar c=2 → 2·32+10 = 74.
- §14.2: (2,3) uint8+uint16 → Q=3, size 18, ordinal 5 at [15,18); planar
  `b` 12 bytes, ordinal 5 at 10–11; float32+bool → Q=5, size 30, ordinal 5
  at [25,30).
- §14.3: (2,5) alternating → byte 0 = 0x55, byte 1 = 0x01, fill true →
  0xFD (pad bits 2–7 set).
- §14.5: (5,5)/(4,4) → grid 2×2, edge tile (1,1) has 1 real + 15 padding,
  32 bytes, values 1–15 each `CD AB`.
- §15.4: entry_count 1,000,000 → 16 segments (15 full + 16,960), 64-byte
  array, region 20,000,064; k=999,999 in segment 15 at relative byte
  339,180; array [20,000,000, 20,000,064); segment 15 [19,660,800,
  20,000,000); full segment 1.25 MiB.
- §15.4: planar C=4 N=32, ordinal 74 at region bytes [1480,1500); channel
  3 = entries 96–127.
- §16.2: N=32, S=8 → runs [0,8),[8,16),[16,24),[24,32).
- §17.3: 1.0/2.0/3.0 float32, s=4 n=3 → `00 00 00 00 00 00 80 00 40 3F 40
  40`. I recomputed the permutation offset i·n+j and got the same string.
- §20.3: 32-tile index region = 32·20 + 4 = 644.
- §12.1: bfloat16 1.0 = 0x3F80 from binary32 0x3F800000's high half.
- §4.6: `température` NFC = 12 bytes `74 65 6D 70 C3 A9 72 61 74 75 72 65`.

### 1.6 The register's own arithmetic

§21.8 claims "121 conditions over 264 instances". §21.1 gives the counting
rule mechanically: instances are semicolon-separated, and a cell reading
`—` is one instance. I parsed all four register tables and counted:

```
rows:       121   (F 36, L 49, T 26, R 10)   §21.2/3/4/5 headers: 36/49/26/10   OK
instances:  264   (F 56, L 110, T 54, R 44)  §21.8: 264                          OK
detectors:  reader 101, verifier 20
tiers:      open 32, layer access 35, tile use 24, extent use 9,
            certification 20, and R1's split cell
```

Every count is exact. I also checked the tier assignments against §19.1's
open steps, §19.3's layer-access list and §19.4's tile-read steps: the 20
`certification` rows are exactly the 20 `verifier` rows, and no row is due
at a tier where its information is unavailable. L3/L5/L6 (layer-record
name) sit at `open`, which §19.1 step 4 licenses by obliging the reader to
parse each layer record's name there; L4/L7/L8/L9 (dimension and channel
names) sit at `layer access`; L37/L38 (index CRCs) at `tile use`.

### 1.7 Identifier hygiene

I extracted every `R-XXX-NN` and looked for gaps. Every prefix is
contiguous with no holes (the only apparent gap, `R-ENC` 17–99, is
[R-ENC-100] appearing once as §2.2's own illustration of numbering above
99; [R-SER-04] appears once, as §14.4's explicit withdrawal notice, which
§2.2 licenses). No identifier is cited but never defined, and none is
defined but never cited.

---

## 2. Coverage completeness — the round-12 shape

Round 12's survivor was a rule written down only once. I went looking for
the same shape in reverse: a *detectable file-conformance violation* that
§21's register omits, which §21.1 declares "a defect in this document".

I enumerated every writer-binding MUST in the document
(`rg "[Ww]riters? (MUST|SHALL)"` → 25 hits) and traced each to a row:

| Rule | Row(s) |
|---|---|
| [R-ENC-02] big-endian | F1 |
| [R-ENC-11] ill-formed UTF-8 | L3, L4, R5 |
| [R-ENC-12] name rules | L5, L6, L7, L8, R6, R10 |
| [R-ENC-15] duplicate names | F4, L9 |
| §6.1 front block | F6 (and F1) |
| [R-CNT-05] directory placement | F7 |
| [R-CNT-12] reserved bits / MU=1 PE=0 | F25, F26, L46, L47 |
| [R-CNT-22] registry flags | F28, L49 |
| [R-CNT-23] layer field constraints | L27–L36, L39, L43, L45 |
| [R-EXT-03] reserved/experimental | F35, F36, L24, L25, L31, L33, L34, L36, L43, L45, R1 |
| [R-GEO-01] geometry floor | L32 |
| [R-GEO-05] linearization | L33 |
| [R-TYP-03] sample type | L34 |
| [R-TYP-07] bool fill | L35 |
| [R-SER-06] layout | L36 |
| [R-SER-08] interleaved bool byte | T2 (real positions), T4 (padding) |
| [R-SLB-01] alignment A | L39, L40 |
| [R-COD-03] codec value | L43 |
| [R-COD-05] deflate wrapper/second stream | T15, T16 |
| [R-COD-06] zstd frame constraints | T17–T22 |
| [R-COD-07] lz4 cap | L44 |
| [R-COD-09] filter value | L45 |
| [R-MTA-05] member ordering | F27, L48 |
| [R-MTA-06] `tarn.` keys | §18.3 declares the file conforming (conduct) |
| [R-LIF-01], [R-LIF-04] | §21.7 / F17 |

Then the eight "value 0 is invalid" spaces of §10.2, each of which is a
distinct byte a writer can emit: record type 0 → F24/L13; channel layout 0
→ L36; linearization 0 → L33; sample type 0 → L34; codec 0 → L43;
filter 0 → L45; index encoding 0 → L31; metadata encoding 0 → R1. All
eight covered.

Then the six checksum locations of §8.1: trailer → F14; directory → F20;
crc_of_crc_array → L37; segment CRC → L38; stored tile → T1;
user-metadata extent → R2. All six. The two rows §8.1 marks "none" (front
block, unassigned-type record extent) are exactly the two §4.5 excepts.

Then the bounds of every structure that can carry an offset:
directory F9/F10; non-layer top-level extent F31/F32; layer record and
sub-record extent L16/L17; stored tile T8/T9. Complete, and — importantly
— non-overlapping: F31/F32 say "non-layer top-level record", L16/L17 say
"a layer record's or sub-record's". A layer record is a top-level record,
and the split is clean because §7.2 assigns a layer record's governing
scope to the layer ("the layer for a layer record and for sub-records,
the file for other top-level records"). The same split governs F25/F26
against L46/L47 and F28 against L49.

**I found no omitted row.** The register is complete against every
byte-level MUST I could locate.

---

## 3. Attacks

Each attack below is a concrete construction. Where the document
forecloses it, I name the sentence, as the charter asks.

### 3.1 The degenerate-but-legal files

**Attack.** Find a conforming file the document's own minimum claim
excludes, or a legal file with a shape that breaks the coverage
accounting.

*(a) The 128-byte floor.* §5.1's justification: "the front signature
block, a directory of at least 4 bytes at an offset of at least 16, and
the 64-byte trailer at a 64-aligned offset cannot be satisfied in fewer."
Checked: the directory ends at ≥ 20, [R-CNT-06] forces
dir_offset + dir_length ≤ F − 64, so F − 64 ≥ 20, and F − 64 is
64-aligned, so F − 64 ≥ 64 and F ≥ 128. **Correct.**

*(b) A 128-byte conforming file with zero slack.* Appendix A's file has
44 bytes of slack. I built a different 128-byte file:

```
0000  89 54 41 52 4E 0D 0A 1A 00 00 00 00 00 00 00 00
0010  00 80 00 00 14 00 00 00 00 00 00 00 00 00 00 00
0020  00 00 00 00 00 00 00 00 5A 5A 5A 5A 5A 5A 5A 5A
0030  5A 5A 5A 5A 5A 5A 5A 5A 5A 5A 5A 5A 06 A5 7A FF
0040  8A 4E 52 41 54 0D 0A 1A 01 00 00 00 00 00 00 00
0050  01 00 00 00 00 00 00 00 10 00 00 00 00 00 00 00
0060  30 00 00 00 00 00 00 00 80 00 00 00 00 00 00 00
0070  EF CD AB 89 67 45 23 01 00 00 00 00 9E C2 A3 6D
```

dir_offset 16, dir_length 48, directory [16,64) ending exactly at F−64 so
the pre-trailer pad is empty; the record sequence is one 44-byte record of
experimental type 0x8000, flags 0 (MU=0, PE=0), inline_length 20, extent
slot (0,0). Coverage: 16 + 48 + 64 = 128, **slack = 0**. §21.6 makes it
conforming ("A record type this specification has not assigned, from the
experimental range … carries MU = 0 | Ignored, and preserved or dropped
per its PE bit"); §10.3's prohibition is conduct, not bytes, per
[R-CNF-02]. Both verifiers certify and both report slack 0.
**Not a fork.** It does show the slack figure §5.2 calls "what tells an
operator to compact" bottoms out correctly.

*(c) The smallest file carrying a layer.* Minimal layer record: 1-byte
name, 1 dimension with a 1-byte name, 1 channel with a 1-byte name and a
1-byte type. Inline payload = 73 bytes, record = 97, directory = 101,
directory [16,117), pad [117,128), trailer [128,192), **F = 192**, slack
11. Conforming with entry_count 0 and extent slot (0,0) because E = 0
gives G = 0, N = 0 ([R-GEO-02], [R-CNT-17]'s "(and 0 when entry_count is
0)", [R-CNT-23]'s crc_of_crc_array = 0). I verified `⌈0/2^16⌉ = 0` makes
[R-CNT-17]'s formula give 0 without needing its parenthetical.

### 3.2 A structure that can end exactly at F − 64

**Attack.** §15.3 permits a non-sentinel entry with
`offset + length = F − 64` (its row rejects only `> F − 64`). Place a
stored tile there, abutting the live trailer, and see whether the two
rules that govern that byte agree.

**Result: the boundary is unreachable, and the document closes it
twice.** [R-CNT-05] says "Writers MUST place the directory so that no
structure lies between its end and the trailer" and "A verifier MUST treat
a structure in that gap as a validity error at file scope". A tile ending
at F−64 either lies wholly in that gap (→ F7) or straddles the directory's
end (→ F7 *and* F33 overlap) or requires the directory itself to end at
F−64, in which case the two overlap. So in a conforming file **the
directory is necessarily the last structure**, and every other structure
lies in [16, dir_offset). §5.1's three-commit figure draws exactly that
shape. This is a strong, non-obvious invariant and I could not break it.

### 3.3 The reader/verifier seam — the front signature block

**Attack (concrete bytes).** Take Appendix A's file and change bytes
[8,16) from zero to `01 01 01 01 01 01 01 01`:

```
0000  89 54 41 52 4E 0D 0A 1A 01 01 01 01 01 01 01 01
0010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
…     (bytes [16,128) identical to Appendix A)
```

The trailer CRC still verifies (it covers trailer bytes [0,60) only) and
the directory CRC still verifies (CRC of zero bytes). I confirmed both.
§4.5 excepts the front signature block from checksum coverage, so **no
checksum in the file covers those eight bytes** — the corruption is silent
to the entire chain of trust.

§6.1's table classes bytes [8,16) as `zero`, structural, and §6.1 says
"Writers MUST emit exactly these 16 bytes." F6 registers the violation at
file scope. So the file is nonconforming.

The reader side is deliberately split, and I accept it: a reader whose
open leaves [0,16) resident MUST reject; one that would have to fetch them
MAY omit ([R-CNT-04]). Two conforming readers therefore disagree about
this file, by design, and §6.1 gives the reason ("The test is residency,
not transport, so an implementation decides it at its own open path
without having to classify the network underneath it").

The interesting question is the **verifier**. Six passages restate the
residency exemption without qualifying it for verifiers:

- [R-CNT-04] itself — "A reader that would have to issue a further range
  request to obtain those bytes MAY defer or omit the check";
- F1's condition — "the front-block instance binds only a reader holding
  bytes [0, 16) resident";
- F6's condition — "the obligation binds a reader holding those bytes
  resident, and a reader that would have to fetch them MAY defer or omit
  the check (`[R-CNT-04]`)" — and F6's Detector cell reads *reader*, not
  *verifier*;
- §19.1 step 1 — "one that would have to issue a further range request for
  them MAY defer or omit the check";
- §19.2's first bullet — "the front signature block, for a reader whose
  open leaves it resident";
- §9.7's walk claims [0,16) but checks only "each verifies against the
  checksum covering it, where §8.1's map states one", and §8.1 states none
  for the front block.

And **Appendix H's verifier checklist — the one place an implementer looks
for "the checks readers are exempt from" — does not name the front block**
among its ten items.

A remote verifier assembled from those six passages fetches the trailer,
the directory, each index region and each tile payload, never [0,16), and
certifies this file. A verifier that fetches [0,16) reports nonconforming.

**Foreclosed by one sentence,** §2.3: "**Conforming verifier.** A reader
that additionally checks every file-level requirement — including those
ordinary readers are exempted from — and certifies conformance." §6.1's
sixteen bytes are a file-level requirement, so the verifier checks them.
[R-CNF-11] reinforces it: *cannot establish* is available only where a
requirement is one the verifier "is unable to check on a capability or
resource ground", and a 16-byte range request is neither, so a verifier
that omits the check has no verdict available to it but *conforming*,
which §2.4 forbids for a file carrying a violation.

I judge this **decided but expensively decided** — six restatements of the
exemption against one governing clause, with the summary that exists to
list verifier-only checks silent on it. Reported as **adversary-01**
(OBSERVATION), not byte-level.

### 3.4 The metadata-encoding value space

**Attack (concrete bytes).** A 128-byte file whose only unusual feature is
a top-level user-metadata record declaring encoding `0x05` — a value in
§18.2's reserved range 3–0x7F:

```
0000  89 54 41 52 4E 0D 0A 1A 00 00 00 00 00 00 00 00
0010  7B 22 61 22 3A 31 7D 6A D5 F7 CF 02 00 02 00 01
0020  00 00 00 10 00 00 00 00 00 00 00 0B 00 00 00 00
0030  00 00 00 05 40 37 48 DF 00 00 00 00 00 00 00 00
```

Extent [16,27) holds `{"a":1}` followed by its terminal CRC-32C, which
verifies. The record is type 0x0002, flags MU=0/PE=1 (the registry
values), inline_length 1, encoding byte 0x05 at directory offset +24.

Verifier A: R1 registers "A user-metadata record declares a document
encoding of 0, or a reserved-range value (3-0x7F)" as an ignore-record
**violation**; §21.5's own closing preamble sentence says "Every row here
is a violation all the same"; [R-EXT-03] says "a value from a reserved
range MUST NOT be emitted at all before this specification assigns it".
→ **nonconforming**.

Verifier B: §21.5's opening preamble says the outcome applies "as a
violation in the rows below, **except at an unassigned encoding**, where
no document rule attaches and §21.6 records the defined non-violation
(`[R-MTA-10]`)". 0x05 is an unassigned encoding by [R-MTA-03]'s own
partition. → **certify**.

**Foreclosed, but by three converging pointers rather than one sentence.**
(i) The exception's own cross-reference lands on §21.6, whose row names
only "an experimental-range (≥ 0x80) document encoding". (ii) [R-MTA-10]
expressly preserves "the encoding byte's own value set (`[R-MTA-03]`)"
among the checks that still decide conformance, and [R-MTA-03] says "0 is
invalid … 3 through 0x7F are reserved". (iii) §21.1: "where a row and the
rule it cites diverge, the rule governs", and R1's cited rules are
[R-CNT-25], [R-MTA-03] and [R-EXT-03], all of which support A. The word
"unassigned" in that one preamble sentence is doing the work of
"experimental", and it is the only place in the document where the two are
conflated. Reported as **adversary-02** (AMBIGUITY), not byte-level.

I also checked the adjacent surface and found it tight: R3 explicitly
carries the same carve-out correctly — "under its declared **assigned**
encoding — under an unassigned one this specification defines no decoding,
and §21.6 governs" — which is the phrasing the preamble should have used.
§2.3, §17.4 and §22.3's fourth residue all say "unassigned" too, but each
is confined to the *cannot-establish* axis or to what a certificate
covers, not to violation status, so none of them forks a verdict.

### 3.5 Two structures claiming the same bytes, neither belonging to a layer

**Attack (concrete bytes).** Two top-level records of experimental type
0x8001, flags 0, extent slots (16, 32) and (24, 32) — overlapping on
[24,48). Directory at 64, F = 192. Everything else conforming.

[R-CNT-13] gives three cross-scope overlap cases: "a verifier MUST treat
an intra-layer overlap … as reject-layer, **any overlap across layers or
touching another scope's structures as reject-file, and any overlap
between two structures neither of which belongs to a layer as
reject-file**". My file is the third case.

F33's condition reads: "A byte of the live committed state is claimed by
two structures that do not belong to the same layer — **across two layers,
or a layer structure against another scope's structure**". The em-dash
gloss enumerates the first two of [R-CNT-13]'s three cases and omits the
third. The head clause ("do not belong to the same layer") arguably covers
it vacuously, and F33's Instances cell does list "record extents … ;
directory region", which are precisely non-layer claimants — so the
instance list already anticipates the case the gloss drops.

**Foreclosed** by §21.1's "where a row and the rule it cites diverge, the
rule governs", and by F33's head clause and instance list. Both verifiers
reach *nonconforming*; only the row label a corpus entry would cite under
[R-VEC-02] is at issue. Reported as **adversary-03** (OBSERVATION), not
byte-level. I flag it because §21.1's completeness is normative and this
is a freshly edited row.

### 3.6 Overflow with a zero factor, and the empty layer under a limit

**Attack.** [R-ENC-04] binds "any quantity this specification defines as a
sum or product … whose **mathematical value** would exceed 2^63 − 1". A
layer with E = (2^62, 2^62, 0) and T = (1,1,1) has G = (2^62, 2^62, 0), so
N = 0 mathematically, but a reader multiplying left to right overflows on
the first two factors. Two readers disagree: one accepts, one rejects.

**Foreclosed** by [R-ENC-04]'s own words "whose *mathematical* value would
exceed". N is 0. The rejecting reader is nonconforming, and §11.2's Note
already warns about the neighbouring trap (the `(E+T−1)/T` idiom). I could
not turn this into a defensible fork; it is an implementation hazard the
document names in the abstract but not in this instance.

**Attack.** The complementary case: does an *empty* layer's declarations
still get overflow-checked? E = (0,), T = (2^62,), one float64 channel.
N = 0, entry_count = 0, extent slot (0,0) — the layer addresses no tile at
all. But P = 2^62 and Q = 8, so P·Q = 2^65 > 2^63 − 1. A reader that
short-circuits on N = 0 certifies; one that computes the decoded size
rejects the layer.

**Foreclosed, but I had to work for it.** The passage that decides it
directly is a **Note** in §17.2 — "`[R-ENC-04]`'s overflow rule carries no
such quantifier — it binds any sum or product a file yields — so P·Q and
P·B^c are checked in an empty layer even though this cap is not" — and
§2.1 makes Notes non-normative. The *normative* chain that reaches the
same answer is [R-SER-02]'s "These products and sums are
declaration-derived quantities under `[R-ENC-04]`", [R-SER-07]'s "Every
decoded size, and the value count V, is a declaration-derived quantity
under `[R-ENC-04]`", and register row L2, which lists "P·Q (which
dominates V = P·C); P·B^c" as instances detected by the **reader** at
**layer access** — a tier an empty layer reaches. "Declaration-derived"
is the load-bearing word: it ties the quantity to the declarations, which
exist, rather than to tiles, which do not. I picked *checked*, and I think
that is right, but I want it recorded that the plainest statement of it is
in text §2.1 declares non-normative.

The contrasting half is decided normatively without help: [R-COD-07] and
L44 both quantify over "a layer **any of whose addressed tiles'** decoded
size exceeds 0x7E000000", which an empty layer satisfies vacuously.

### 3.7 Every enum in every reserved and experimental range, in every position

I enumerated the full matrix rather than sampling it.

**Record types, top level:** 0 → F24 (reader, reject-file); 0x0001 layer;
0x0002 user metadata, second copy → F34; reserved 0x0003–0x7FFF with MU=1
→ F35 (reader) and F36 (verifier), §21.1 recording it against the narrower
F35; reserved with MU=0 → F36 only, so a **reader serves the file and a
verifier rejects it** — by design, F36's detector being *verifier*;
experimental ≥ 0x8000 with MU=1 → reader MUST reject a **conforming** file
(§21.6's closing paragraph, second structural case); experimental with
MU=0 → ignored, conforming (§21.6's table).

**Record types, sub-record:** 0 → L13; 0x0001 nested → L26 ("A *known*
type appearing where §7.3's table does not scope it … is a validity error
at layer scope, not an unknown type", [R-CNT-18]); 0x0002 second copy →
L19; reserved MU=1 → L24 and L25; reserved MU=0 → L25; experimental MU=1 →
reject-**layer**, never reject-file, on a conforming file; experimental
MU=0 → ignored.

**Flag bits, all four combinations, both positions:** MU=1/PE=0 → F25
(non-layer top level) or L46 (layer record or sub-record); reserved bits
2–15 set → F26 or L47; a registered type carrying a stored bit that
differs from §7.3's registry → F28 (type 0x0002 at top level) or L49
(layer record, or a registered sub-record). No gap and no double-coverage:
the split turns on §7.2's assignment of a layer record's governing scope
to the *layer*, which is why F25/F26/F28 all say "non-layer top-level".

**All eight numeric spaces at value 0** → covered (see §2 above).

**The one asymmetry worth naming, and it is deliberate:** for record types
the reserved range is a *bytes* violation while the experimental range is
a *conduct* violation only. [R-CNT-15] states it —"a record type from the
experimental range is conforming (§10.3's prohibition binds the writer's
conduct, not the bytes, `[R-CNF-02]`), while one from the reserved range
is a value this specification has not assigned — emitting it is a
violation". The same asymmetry holds in the metadata-encoding space
(§21.6's row vs R1) and does *not* hold in the value-set spaces of §11.4,
§12.2, §14.1, §15.1, §17.2 and §17.3, where [R-EXT-03] makes both ranges a
validity error at the owning scope. I checked each: L31, L33, L34, L36,
L43 and L45 each carry both the reserved and the experimental sub-range as
separate instances. Consistent.

### 3.8 Interactions between individually well-specified features

*Sparse tile under a filter chain.* A sentinel entry short-circuits steps
5 and 6 of §19.4 — "A valid sentinel short-circuits steps 5 and 6 for that
entry" — so no codec or filter runs. [R-IDX-05]'s all-sentinel constant is
a writer convenience only: "Equality with the constant licenses nothing
for readers: verification is byte comparison of computed CRCs, never
constant matching." Closed.

*Byte-shuffle over a packed boolean plane.* §17.3 sets s = 1 and the
filter is the identity, and asserts "The decoded image's length L is
divisible by s in every case". I verified all four cases: interleaved
L = P·Q with s = Q; planar numeric L = P·B^c with s = B^c; packed bool
L = ⌈P/8⌉ with s = 1; and planar bool read through §12.1's element size
1 gives s = 1 as well. Divisible in every case. Closed.

*T26's third instance — a mis-strided shuffle on a packed bool plane —
is it even constructible?* It needs L composite (so a proper divisor
exists) **and** P mod 8 ≠ 0 (so pad bits exist to catch it) **and** the
permutation to actually move a byte carrying constrained content. P = 25
works: L = 4, s = 2 gives the permutation [b0,b2,b1,b3], leaving byte 3
(which holds the pad bits) in place but moving byte 2, where padding
positions live if E < 24. So T4 fires and T5 does not. Constructible.
Closed.

*Empty layer under a limit.* §3.6 above.

*Compaction over a record the compactor cannot read.* [R-WRT-06]: "A
compactor MUST refuse to compact a file carrying any record whose type it
does not implement with MU = 1". §20.4's MU=1 row separately lets an
*appender* commit against such a file when the record is a layer
sub-record ("At layer scope an unknown critical record blocks modification
of that layer, leaving other layers editable"). The two are consistent
because [R-WRT-06] says *any* record and §20.4's carve-out is about which
scopes an appender may modify. Closed.

*Codec 1 on a planar bool plane.* [R-COD-04] requires the entry length to
equal the decoded size, which §14.3 makes ⌈P/8⌉ rather than P. T14's
instance list carries "packed planar bool ⌈P/8⌉" for both the longer and
shorter cases. Closed.

*A zstd tile smaller than 1 KiB.* §17.2's Note works this out: the
Window_Descriptor cannot express less than 1 KiB, so such a tile is
encodable only as a single-segment frame, where Window_Size is the frame
content size, which [R-COD-06] already ties to the decoded size. I
confirmed the arithmetic against RFC 8878's windowBase = 1 << (10 +
Exponent). The three worked decoded sizes the document offers (18, 30, 2)
are all below 1 KiB, so the note is not hypothetical. Closed.

### 3.9 The point-request / region-request seam

**Attack.** A coordinate outside a layer's extents. As a **point request**,
§19.4 step 1 says it "fails as a request, with no verdict on the file". As
a **region request** whose every interval holds a single position, the same
coordinate "succeeds and returns no samples". Two readers exposing only
one of the two API shapes give opposite answers to what a caller thinks is
the same question.

**Foreclosed** by the definition sentence in §19.4 that exists precisely
to draw the line: "a range whose every interval holds a single position is
a region request." The document makes the two request kinds distinct
rather than leaving the overlap open. This is the sharpest example I found
of the document anticipating an attack.

### 3.10 Partial slack totals, and whether they can under-count

**Attack.** §5.2 claims "A partial total is F less the bytes claimed by
the claimants the walk did enumerate — an upper bound on the file's true
slack, **never an under-count**". If a verifier summed claimant *lengths*
in a file with overlapping claimants, double-counting would make the total
an under-count, falsifying the claim exactly where it matters (a
verifier's walk is most likely to stop early on an overlap).

**Foreclosed** by the word "bytes": "F less the **bytes** claimed" is set
language, not a sum of lengths, so the quantity is F − |union|, which is
monotone in the claimant set. I confirmed the complete case against
Appendix A: 128 − 16 − 4 − 64 = 44, the document's own figure.

### 3.11 Rejected tiles, run continuity, and the coverage walk

**Attack.** §15.3 splits reject-tile entries into six *structural* rows and
one non-structural row (crc failure). Three separate mechanisms then have
to agree about which entries "count": [R-LIF-08]'s coverage walk,
[R-SLB-03]'s run continuity, and §15.3's own *verifier* rows. Build a slab
layer where a structurally bad entry sits between two stored tiles and see
whether the three disagree.

**Foreclosed, and consistently, in all three places:**
- §15.3 — "Such an entry contributes no stored extent to the *verifier*
  rows … and none to `[R-LIF-08]`'s coverage walk … An entry whose only
  defect is that its stored bytes fail its crc is well-formed … its extent
  stands".
- §9.7 — "an entry `[R-IDX-03]` classifies reject-tile on a *structural*
  ground contributes no stored extent to the walk; one whose stored bytes
  alone fail its crc keeps its extent", and "does not make the walk
  incomplete".
- §16.2 — "So are the entries §15.3 classifies reject-tile on a
  *structural* ground … An entry whose only defect is that its stored
  bytes fail its crc is not transparent … so this invariant stays decidable
  from index bytes alone."

I checked the last claim independently: the only entries removed from the
packing relation are those decidable from the entry's own 20 bytes, so a
verifier never needs a payload fetch to decide L41/L42. The claim holds.

### 3.12 The two conforming-file refusals, and a third the closing
paragraph does not name

§21.6's closing paragraph names two "conforming files a reader
nevertheless refuses": an unimplemented version_major, and an
experimental-range record type carrying MU = 1. There is a third shape:
an experimental-range **sub-record** carrying MU = 1, which [R-CNT-18]
makes reject-**layer** on a file that is conforming. §21.6's paragraph
cites §10.2/§10.3 and [R-CNT-15] (the top-level rule) and does not mention
[R-CNT-18]'s layer-scope variant.

**Foreclosed** by §2.3's carve-out to [R-CNF-03], which is written to cover
records at either position: a reader must accept every conforming file
"carrying no record of a type it does not implement with MUST_UNDERSTAND =
1" — a sub-record is a record. The refusal is partial rather than total,
which is why the closing paragraph's framing ("refuses") does not quite
fit it, but no verdict turns on it. Not reported.

### 3.13 Verifier-versus-verifier divergence on capability grounds

I built four of these and all four are sanctioned rather than defective:

1. A tile whose declared decoded size is 1 GiB (above §21.9's 256 MiB
   guarantee). Verifier A decodes → certifies. Verifier B declines →
   *cannot establish*, "not a finding that the file is nonconforming"
   ([R-ERR-04], §2.3).
2. A user-metadata document decoding to 32 MiB (above the 16 MiB
   guarantee). Same split, explicitly licensed by [R-MTA-09] — "the bound
   is that verifier's capability and not a limit on validity
   (`[R-CNF-10]`)".
3. An experimental MU=1 record: a verifier that privately implements the
   type certifies; one that does not reports *cannot establish*.
4. An **empty** layer declaring a 1 GiB tile shape but zero addressed
   tiles. Does a verifier that declines the layer on resource grounds owe
   *cannot establish*? **No** — §2.3's ground is "declines a layer's or a
   tile's decode on resource grounds **and so** cannot check §14's
   decoded-content obligations", and with no stored tile nothing is left
   unchecked. The conjunctive "and so" closes it, the same way
   [R-MTA-10]'s "nothing is left unchecked" closes the unassigned-encoding
   case. I went looking for a fork here and the "and so" is what defeats
   it.

None of these is a *certify versus reject* fork: *cannot establish* is a
withheld certificate, not a rejection, and §2.3 makes the difference
explicit ("*Cannot establish* is not a finding that the file is
nonconforming").

### 3.14 Ordering of the duplicate-name check against layer-scope name errors

**Attack.** Two layer records both carrying an empty name (length prefix
0). Each is an L5 violation (reject-layer, detected at open); the pair is
an F4 violation (reject-file, detected at open). Reader A, validating each
record as it walks, rejects both layers and serves the rest of the file.
Reader B, building the namespace first, rejects the whole file. That is a
genuine observable divergence — a served file versus a refused one.

**Foreclosed** by §19.1 step 4's ordering sentence: "**Uniqueness is
decided first**, and over the raw name bytes whether or not each name is
itself well-formed — `[R-ENC-13]` makes name comparison a byte comparison,
which needs no valid name — so two layers whose name fields are
byte-identical are a duplicate even when neither name is valid." The
companion sentence handles the other half: a record whose name field
overruns its inline_length "yields no name field to compare, so it
contributes no name to the namespace". This is the second-sharpest
anticipation I found.

### 3.15 A structure in the pre-trailer pad

Base file: layer record, directory [16,117), pad [117,128), trailer
[128,192). Place an 8-byte record extent at [120,128). Reader: serves the
file — coverage and the pre-trailer rule are both verifier-only. Verifier:
F7, reject-file. Sanctioned split; F7's detector is *verifier* and §21.1
says "For a row whose Detector is *verifier*, the outcome names the scope
at which the damage is recorded, not an obligation on any reader."

### 3.16 Appendix G's emission order

**Attack.** Appendix G item 3 fixes a total emission order so that two
profile-adopting writers produce identical bytes. Records are ordered "by
type, and within a type by their encoded bytes compared lexicographically,
save that type 0x0001 ties by layer name". A record's encoded bytes are
its 24-byte header plus inline payload (§7.2), and the header carries
extent_offset. Item 3 assigns record extents "in ascending record order".
So for two records of the same type that both carry extents, the ordering
key contains a value the ordering itself determines.

The carve-out for 0x0001 shows the author saw the shape of this: layer
records' extent offsets are pinned first, by layer-name order, before
record order is consulted. Type 0x0002 is safe by multiplicity (F34, L19
allow at most one per scope). What is left is **unknown types, whose
multiplicity nothing constrains** — two experimental MU=0 records each
carrying an extent have no determined order under item 3, whether "encoded
bytes" is read as the whole record (circular) or as the inline payload
alone (tied, when payloads match).

Reachability is limited: §10.3 bars a released writer from emitting
experimental values at all, and item 4 pins the profile to one generation,
so the case arises only for an updater. Appendix G is non-normative and
"adds no requirement to any actor", so no conformance verdict turns on it —
but two writers could each claim profile conformance and disagree on
bytes, which is the one thing the profile exists to prevent. Reported as
**adversary-04** (AMBIGUITY), not byte-level.

### 3.17 "Extents grow; they do not shrink"

§11.1's Rationale asserts flatly: "Extents grow; they do not shrink, and no
declaration a stored tile depends on changes once that tile exists (§20.3)".

The normative rule in §20.3 step 4 is narrower: "A commit MUST NOT change a
layer's declarations in a way that alters, for any tile that layer stores,
what §14 fixes for its stored bytes or how they decode". A shrink that
touches no stored tile's stored bytes is not barred by it. Concretely:
d = 1, E = (5,), T = (4,), G = 2, tile 0 stored (covering coordinates 0–3,
all real, no padding), tile 1 the sentinel. Shrink E to 4: G becomes 1,
entry_count 2 → 1, the index region is re-emitted per [R-CNT-17] /
[R-WRT-04], and stored tile 0's decoded size, sample offsets, padding set
(empty before and after) and codec are all unchanged. The normative rule
permits it; the Rationale says it does not happen.

The converse case shows why the rule is written the way it is: shrinking
E from 8 to 5 with T = 4 turns in-tile positions 5–7 of a stored tile into
padding positions, which [R-SER-05] requires to hold fill, so unless the
stored bytes already do, the shrink makes the tile nonconforming (T4). The
rule catches exactly that; the Rationale over-generalises it.

Non-byte-level twice over: §2.1 makes Rationale text non-normative, and
§21.7 confirms that a declaration change across generations has no
single-file witness. Reported as **adversary-05** (OBSERVATION).

### 3.18 Attacks that produced nothing at all

For completeness, surfaces I worked and abandoned without a finding:

- **Checksum coverage.** §4.5's "every field covered by exactly one
  checksum" against §8.1's seven-row map. I traced every field of every
  structure — trailer, front block, directory records, layer record inline
  payload, index entries, segment CRC array, crc_of_crc_array, stored tile
  bytes, user-metadata extent — and found exactly one covering checksum
  for each, with the three terminal fields and the two "none" rows exactly
  as §4.5 excepts them. The interior/terminal distinction §4.5 draws
  ("each segment CRC array, each tile-index entry's crc field, and each
  layer record's crc_of_crc_array — are both comparison-verified and
  covered by exactly one further checksum") is exactly right.
- **crc_of_crc_array = 0 at entry_count = 0.** L27 makes a nonzero value a
  violation. I checked that the mandated 0 also equals the *computed*
  value: the segment CRC array is zero bytes, and CRC-32C of zero bytes is
  0x00000000 (§4.5). The rule and the computation agree; they did not have
  to.
- **Segment boundaries.** entry_count 65,536 → 1 full segment, array 4
  bytes, extent_length 1,310,724. entry_count 65,537 → 2 segments (the
  second covering 1 entry, so a *partial* segment whose CRC [R-IDX-05]
  requires to be computed rather than taken from the constant), array 8
  bytes, extent_length 1,310,748. Both match [R-CNT-17]'s formula.
- **§21.9's derivations.** 2^32 tiles → segment CRC array 2^16 × 4 = 256
  KiB, and 2^36 → 4 MiB, both as the Note claims. 65,536 layers at "small
  layer records" ≈ 12.5 MiB, consistent with the 16 MiB directory row.
- **Appendix B against the body.** All 27 rows checked against their cited
  sections. Every value agrees, including the four that have bitten
  formats before: name length 255 (forced by the u8 prefix), rank 255 and
  C 65,535 (forced by the u8/u16 fields), A in [512, 2^62] and A_slab in
  [1, 2^62], S in [1, 2^63−1].
- **Why A and A_slab are absent from L1's instance list.** [R-ENC-03]'s
  domain covers "every offset, length, extent, and count … entry counts
  and slab run lengths included". An alignment is none of those, so
  [R-ENC-03] does not reach it and L39/L29's power-of-two-in-range rows
  carry the whole burden. S *is* a length and *is* in L1's list. This
  looked like an omission and is not one.
- **Appendix H against §2.3.** Every reader obligation in the checklist
  traces to a requirement; the "all four codecs, both filters, both
  layouts, all thirteen sample types, and both user-metadata encodings"
  line matches §2.3's own enumeration.
- **The incompat flag lane.** I tried to make a set incompat-lane bit a
  "conforming file a reader refuses", by analogy to version_major. It is
  not: §4.3 and §10.1 restrict growth to four vehicles, of which the flag
  vehicle is "**new ignore-lane** flag bits" only, so no minor version ever
  assigns an incompat bit and F19 is unconditional.
- **§19.2's "no earlier".** The fourth bullet reads "before anything the
  extent holds is returned — no earlier, since the open fetches no extent".
  Read as a prohibition it would contradict [R-RDR-02]'s own next sentence
  ("A reader MAY detect any violation earlier"); read as fixing the tier,
  which is what the whole rule does ("no later than the reader's first
  reliance"), it is consistent. I picked the second reading.
- **§19.1 and §19.3 not listing every check.** Neither step list mentions
  the metadata encoding byte's value set (R1), and §19.3 does not cite
  [R-ENC-04] although L2 is due at layer access. §19's preamble forecloses
  both: "Those enumerations are not the complete inventory of what a
  reader detects at that tier: §21's register is … A row this section does
  not restate is due at its own tier all the same."
- **§22.3's editorial slip.** "recovery output is re-verified as a whole
  file before being trusted (`[R-LIF-06]`) before any use" — a doubled
  clause in changed text. No conformance consequence; noted, not filed.
- **L41's referent.** "a stored tile's offset ≠ the previous stored tile's
  offset plus **that tile's** length" restates [R-SLB-03]'s "the previous
  stored tile's offset plus **its** length" with an ambiguous "that tile".
  Read as the current tile the relation is wrong. §21.1's "the rule
  governs" closes it and no competent implementer reads "packed" any other
  way; noted, not filed.

---

## 4. Findings

Five, all ranked below by how plausible it is that a real implementation
would land on the wrong side. None survives as byte-level, and I say why
in each.

| id | kind | location | byte-level | plausibility of divergence |
|---|---|---|---|---|
| adversary-01 | OBSERVATION | §21.2 F1/F6, [R-CNT-04], §9.7, App. H | no | moderate — six restatements vs one clause |
| adversary-02 | AMBIGUITY | §21.5 preamble vs R1 | no | low — three pointers converge |
| adversary-03 | OBSERVATION | §21.2 F33 vs [R-CNT-13] | no | low — same verdict either way |
| adversary-04 | AMBIGUITY | Appendix G item 3 | no | low — non-normative, narrow reach |
| adversary-05 | OBSERVATION | §11.1 Rationale vs §20.3 | no | low — non-normative, no file witness |

### adversary-01 — the front-block check is exempted in six places and
required in one, and the verifier checklist does not carry it

**Kind:** OBSERVATION. **Location:** §21.2 rows F1 and F6; [R-CNT-04]
(§6.1); §9.7 ([R-LIF-08]); §19.1 step 1; §19.2; Appendix H; decided by
§2.3 ([R-CNF-11]).

**Quotation** (F6's condition cell, §21.2): "The 16-byte front signature
block is not byte-identical to the constant; the obligation binds a reader
holding those bytes resident, and a reader that would have to fetch them
MAY defer or omit the check (`[R-CNT-04]`)" — Detector cell: `reader`.

**Detail.** See §3.3 above for the concrete 128-byte file (Appendix A with
bytes [8,16) set to `01`×8, both CRCs still verifying, no checksum
covering the damaged bytes). Six passages state the residency exemption
without qualifying it for verifiers, F6's Detector cell reads *reader*,
§9.7's walk claims [0,16) without checking it, §8.1 assigns it no
checksum, and Appendix H's verifier checklist — the document's own
enumeration of "the checks readers are exempt from" — omits it entirely.
A remote verifier assembled from those passages certifies a nonconforming
file. The single clause that decides it is §2.3's "A reader that
additionally checks every file-level requirement — including those
ordinary readers are exempted from — and certifies conformance", reinforced
by [R-CNF-11]'s restriction of *cannot establish* to "a capability or
resource ground", which a 16-byte range request is not. I picked: the
verifier must fetch and check. An implementer who works from the register
and the checklist rather than §2.3 will ship a verifier that certifies
files with a corrupt front block — the one structure in the format that no
checksum protects.

**Byte-level: no.** §2.3's clause is unambiguous and directly on point;
two competent implementations reading it cannot disagree. What makes this
worth reporting is the ratio, not a genuine fork.

### adversary-02 — §21.5's preamble excepts "an unassigned encoding" from
being a violation, which by §18.2's own partition includes the two ranges
R1 registers as violations

**Kind:** AMBIGUITY. **Location:** §21.5 preamble; row R1; §21.6's
metadata-encoding row; [R-MTA-03], [R-MTA-10], [R-EXT-03].

**Quotation** (§21.5 preamble): "User metadata is quarantined
(`[R-CNT-25]`): every way its document can be unreadable takes this
outcome, whatever the containing scope — as a violation in the rows below,
except at an unassigned encoding, where no document rule attaches and
§21.6 records the defined non-violation (`[R-MTA-10]`)."

**Detail.** [R-MTA-03] partitions the space as: 0 invalid; 1–2 assigned;
3–0x7F reserved; ≥ 0x80 experimental. "Unassigned" therefore denotes 0,
3–0x7F **and** ≥ 0x80. R1, three paragraphs later in the same subsection,
registers "A user-metadata record declares a document encoding of 0, or a
reserved-range value (3-0x7F)" as a violation. §21.6's table registers
only "an experimental-range (≥ 0x80) document encoding" as the defined
non-violation. So the preamble's exception, read literally, excepts from
violation status two of the three ranges the register calls violations.
Permitted readings: (a) "unassigned" means "experimental", so R1 stands;
(b) "unassigned" means what [R-MTA-03] says, so a record with encoding
0x05 is not a violation and a verifier certifies. I picked (a), on three
grounds: the exception's own cross-reference lands on §21.6, whose row
names the experimental range only; [R-MTA-10] expressly keeps "the
encoding byte's own value set (`[R-MTA-03]`)" among the checks that decide
conformance under an unassigned encoding; and [R-EXT-03] makes emitting a
reserved value a byte-level prohibition rather than a conduct one, unlike
the experimental range. Note that R3, in the same table, gets the
distinction right — "under its declared **assigned** encoding" — which is
the phrasing the preamble wants. An implementer taking (b) certifies the
128-byte file in §3.4.

**Byte-level: no.** Reading (b) does not survive [R-MTA-10]'s explicit
preservation of the encoding byte's value set together with §21.6's
experimental-only row; §21.1's "the rule governs" then decides it against
the preamble.

### adversary-03 — F33's gloss enumerates two of [R-CNT-13]'s three
cross-scope overlap cases

**Kind:** OBSERVATION. **Location:** §21.2 row F33; [R-CNT-13] (§7.2).

**Quotation** (F33's condition cell): "A byte of the live committed state
is claimed by two structures that do not belong to the same layer — across
two layers, or a layer structure against another scope's structure".

**Detail.** [R-CNT-13] names three cross-scope cases: "any overlap across
layers or touching another scope's structures as reject-file, and any
overlap between two structures neither of which belongs to a layer as
reject-file". F33's em-dash gloss carries the first two and drops the
third, which is reachable: the two overlapping experimental-type record
extents of §3.5, or a top-level record extent overlapping the directory
region. F33's head clause ("do not belong to the same layer") covers the
dropped case only vacuously, and its Instances cell already lists the
non-layer claimants ("record extents; sub-record extents; directory
region"), so the row is internally inconsistent with its own gloss rather
than wrong. I picked: the head clause and [R-CNT-13] govern, so such a
file is reject-file. The exposure is to §21.1's normative completeness
clause and to [R-VEC-02]'s requirement that a vector name the row it
exercises.

**Byte-level: no.** Both readings reach *nonconforming* for the same file;
only the row label a corpus entry cites differs.

### adversary-04 — Appendix G's record order is circular for two records of
the same type that both carry extents

**Kind:** AMBIGUITY. **Location:** Appendix G, item 3.

**Quotation:** "Records and a layer record's sub-records alike are ordered
by type, and within a type by their encoded bytes compared
lexicographically, save that type 0x0001 ties by layer name — an order a
reader can derive, which a creation order is not."

**Detail.** A record's encoded bytes include its 24-byte header (§7.2),
whose bytes 8–23 are the extent slot; item 3 assigns record extents "in
ascending record order". For two records of one type that both carry
extents, the ordering key therefore contains a value the ordering
determines. The 0x0001 carve-out avoids this for layer records (their
extent offsets are pinned first, by layer-name order) and multiplicity
avoids it for 0x0002 (F34 and L19 permit at most one per scope), leaving
unknown types, whose multiplicity nothing constrains. Permitted readings:
(a) "encoded bytes" is the whole record → the order is circular and
undefined; (b) "encoded bytes" excludes the extent slot → the order is
undefined when two same-type records share type, flags and inline payload.
I picked (b) plus an added extent-length tiebreak, and had to invent the
tiebreak. Reachability is narrow — §10.3 bars a released writer from
emitting experimental types, and item 4 pins the profile to one generation
— so this bites an updater rather than a creator.

**Byte-level: no.** Appendix G is non-normative and "adds no requirement
to any actor", so no conformance verdict turns on it; what diverges is two
writers' claims of *profile* conformance.

### adversary-05 — §11.1's Rationale forbids extent shrinking flatly; §20.3
forbids only shrinks that break a stored tile

**Kind:** OBSERVATION. **Location:** §11.1 Rationale; §20.3 step 4
([R-WRT-04]).

**Quotation** (§11.1): "Extents grow; they do not shrink, and no
declaration a stored tile depends on changes once that tile exists (§20.3)
— a layer that stores nothing may still be re-declared freely."

**Detail.** The governing rule is narrower: "A commit MUST NOT change a
layer's declarations in a way that alters, for any tile that layer stores,
what §14 fixes for its stored bytes or how they decode — the set of
padding positions (§11.3) and the content `[R-SER-05]` fixes there, the
decoded size, the byte offset of any sample within the decoded tile image,
or the codec and filter that produced the stored bytes." The worked case
in §3.17 — E = (5,) → (4,) with T = (4,), tile 0 stored and fully real,
tile 1 the sentinel — alters none of those and is therefore permitted,
while the Rationale says shrinking does not happen. The same rule
correctly bars the shrink that *does* break a tile (E = 8 → 5 with T = 4,
turning stored positions into padding that [R-SER-05] requires to hold
fill). I picked the rule. Without it, an updater implementer rejects a
legal commit and reports a conformance error for it.

**Byte-level: no.** §2.1 makes Rationale text non-normative, and §21.7
confirms a cross-generation declaration change has no single-file witness,
so no verifier verdict can turn on it.

---

## 5. Where I had to guess, and honest limits

Three places where I resolved something the text left me to work out
rather than told me:

1. **Whether P·Q is overflow-checked in a layer with zero addressed
   tiles.** The plainest statement is a §17.2 **Note**, which §2.1 makes
   non-normative. I reconstructed the normative answer from [R-SER-02] and
   [R-SER-07]'s "declaration-derived quantities under `[R-ENC-04]`" plus
   L2's instance list and layer-access tier. I am confident, but the
   normative chain is three hops and the direct statement is not normative.
2. **What "encoded bytes" means in Appendix G item 3** — adversary-04.
3. **Whether §19.2's "no earlier" is a prohibition or a tier statement.**
   I took the tier reading, on the strength of [R-RDR-02]'s own "A reader
   MAY detect any violation earlier".

What I did **not** exercise: I built no real deflate, zstd or lz4 payloads,
so the T13–T25 codec rows are checked only by reading against RFC 1951,
RFC 8878 and the LZ4 block format from memory, not by decoding bytes.
The window-size reasoning in §3.8 is the one place that matters, and I
flag it as a memory-based check rather than an executed one. I also did
not attempt to construct a file at any of §21.9's minimum guarantees —
[R-VEC-03] already concedes the tile-count one is not constructible, and
the others would have consumed the session for no adversarial return.

## 6. Verdict on the charter

**I could not construct a file two conforming verifiers would judge
differently.** Every divergence I built either (a) is a reader-versus-
reader split the document draws deliberately and explains (the front-block
residency rule, F36 and every other verifier-only row, [R-CNF-12]'s
licence to reject any nonconforming file early), or (b) is a
verifier-capability split producing *cannot establish* rather than
rejection, which §2.3 defines as a withheld certificate and not a finding
about the bytes, or (c) is closed by a sentence I have quoted above.

The document's density of anticipation is the story of this walk. Five
places closed an attack I had already built: §19.4's "a range whose every
interval holds a single position is a region request"; §19.1's "Uniqueness
is decided first"; §2.3's "and so cannot check §14's decoded-content
obligations"; §5.2's "F less the **bytes** claimed"; and §9.7's "does not
make the walk incomplete". The newly authored §7.4 example is byte-exact
and the register's 121 rows and 264 instances count out exactly. What I
have left is five imprecisions, none of which forks a byte.
