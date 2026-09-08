# Cleanroom round 32 — Reader implementer transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,754 lines; `wc -w` = 47,314 words — matching the brief's "about 47,300"). I opened
no ADR, no `docs/`, no `conformance/`, no `spec/registry.json`, no git history, no web
resource. I listed no directory other than creating my own scratch directory.

The file was where the brief said it was.

**Context I did not ask for.** Before I began, my runtime placed in my context a project
`CLAUDE.md` pointer, an `AGENTS.md` reference, and an index of the maintainer's memory
notes (a list of titles about this project's harness, gates, and repair practice). None
of it is specification text and I have treated none of it as evidence. I name that it
appeared; I do not repeat its contents, and no conclusion below traces to it. I did not
open any file it named.

**Files I wrote** (all under
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-round/scratch/reader/`,
a directory I created and that is mine alone):

- `crc_check_rdr.py` — a self-contained CRC-32C implementation plus the arithmetic
  checks in §3 below. Reads no files.
- `norm_rdr.py` — a whitespace-normalising search harness over `spec/tarn.md` that
  strips leading `> ` from blockquote lines and joins hard-wrapped lines into one blob,
  so that a phrase search cannot be defeated by the document's wrapping. I verified the
  harness against a control phrase known to span a line break
  (`keeps its declarations, with these exceptions and no other`, which wraps after
  "no") — 1 hit — before resting any zero on it.

Everything numeric below I derived myself and then compared against the document's
figure. I never took a document figure on trust.

---

## 1. The reader I am building

I am writing, on paper, a conforming reader in the order I would actually write the
code: open → validate → layer table → layer access → tile read → decode → extract. I
stop wherever the text stops telling me what to do.

Part I alone gets me a container reader; §19.3's layer validation resolves into Part II
at every step, so returning samples needs both (§1's own statement, which I checked
against §19.3's citation list and found true — §19.3 cites §11.4, §12.2, §13.2, §14.1,
§15.1, §17.2, §17.3, all Part II).

---

## 2. The open path — every byte, in order

### 2.1 What I fetch, and what bounds each range before I have read it

**Request 1 — suffix, 64 bytes.** §19.1 step 1 tells me to obtain the
transport-authoritative file size F (`[R-CNT-10]`); §19.1 step 2 tells me to fetch
[F − 64, F). §6.4 collapses these into one request: a suffix range whose response
carries the transport-authoritative size. So my first request is
`Range: bytes=-64`.

What bounds this range before I have read anything? The constant 64, fixed permanently
by `[R-CNT-24]` in every format major version. Nothing in the file bounds it. Good —
this is the one range that can be issued cold.

I then validate in §6.2's stated order, and the order is normative and explicit
(`[R-CNT-06]`), which matters because `[R-ENC-10]` otherwise forbids acting on a field
before its checksum verifies:

1. trailer magic == `8A 4E 52 41 54 0D 0A 1A` (byte equality, not "acting on")
2. trailer CRC: CRC-32C over trailer[0,60) == the u32 at trailer[60,64)
3. version gate (§6.3): version_major != 0 and is a major I implement; version_minor
   never gates
4. then, and only then, the remaining field gates: flags incompat lane (bits 0–15) all
   zero; committed_file_length == transport size and ≡ 0 mod 64; dir_offset ≥ 16;
   dir_length ≥ 4; dir_offset + dir_length ≤ F − 64; file_id != 0; reserved[48,60)
   all zero.

Note the first three are exactly the checks that touch fields `[R-CNT-24]` fixes
across majors — which is what makes `[R-CNF-13]`'s reaching-condition machinery
implementable: I can run 1 and 2 before I know whether I implement the major, and 3
is where I find out.

I derived `[R-CNF-13]`'s reaching set myself rather than reading §21.2's answer first.
`[R-CNT-24]` fixes four invariants: trailer magic at F − 64; version_major and
version_minor at F − 56; a CRC-32C at F − 4 over [F − 64, F − 4); and the front
signature block's constancy. Walking §21.2's 35 rows and asking which assert one of
those four: F8 (magic), F14 (trailer CRC), F6 (front block), and both instances of F1
(byte-reversed front block; byte-reversed trailer magic). Every other row reads a field
inside the 48 bytes a future major may redefine, or asserts a floor derived from format
major 1's own structures (F5), or is outside the premise (F18, version_major = 0
declaring no major at all). That is exactly §21.2's stated derivation — "F8, F14, F6
and both of F1's instances … and no other row". I did not find a row it missed. I paid
particular attention to F13 (committed_file_length a multiple of 64): `[R-CNT-24]`
locates its fields *relative to F* and never requires F to be 64-aligned, so F13 does
not reach. The document does not say so explicitly but the derivation is forced.

**Request 2 — the directory.** `Range: bytes=<dir_offset>-<dir_offset+dir_length-1>`.
This range is bounded, before I read it, by dir_offset ≥ 16, dir_length ≥ 4, and
dir_offset + dir_length ≤ F − 64 — all validated in step 4 above, all after the trailer
CRC verified, so `[R-ENC-05]` ("MUST NOT allocate, seek, or issue I/O based on any
integer obtained from a file before the checksum covering it has been verified") is
satisfied. The sum is a designated declaration-derived quantity under `[R-ENC-04]`
(§6.2 says so expressly), so I check it against 2⁶³ − 1 before forming it.

Then: verify the final 4 bytes of the region against CRC-32C over the preceding
dir_length − 4 bytes (`[R-CNT-11]`), mismatch → reject-file. Only then parse.

**Byte-exact cold remote open cost: 2 requests, 64 + dir_length bytes.**
For the Appendix A file: 2 requests, 64 + 4 = **68 bytes**. Appendix A states exactly
this and I agree with it.

I never fetch [0, 16) on this path. `[R-CNT-04]`'s obligation over the front block turns
on *residency*, not transport, and my two-exact-range open leaves it non-resident, so I
MAY defer or omit the check. If I instead speculate a 64 KiB suffix and the file is
smaller than 64 KiB, the window reaches offset 0, [0, 16) is resident, and I MUST verify
it by byte equality before other processing. I like this rule: it is decidable at my own
open path with no transport taxonomy.

### 2.2 The record walk (§19.1 step 4)

Parse the record sequence — zero or more 24-byte headers each followed by inline_length
bytes, no residue. Per record I apply, from resident bytes and F alone:

- type != 0 (F24)
- header + inline payload within the sequence, no trailing residue (F29)
- unknown top-level type: MU = 1 → reject-file; MU = 0 → ignore-record (`[R-CNT-15]`)
- multiplicity: at most one file-scope user-metadata record (F34)
- extent-slot validity, **for non-layer top-level records only** (F30/F31/F32) — a layer
  record's slot is layer-scope and is checked at layer access
- a top-level user-metadata record's framing: slot not (0, 0), extent_length ≥ 5,
  inline_length == 1 (F21/F22/F23)
- each layer record's name field, parsed and checked per §4.6

Then the layer-name namespace. §19.1 spells out two things I would otherwise have had to
invent: uniqueness is decided *first*, over raw bytes, whether or not the names are
themselves well-formed; and a layer record whose name field does not lie within its
inline_length contributes no name and is instead a layer-scope error. That closes the
question "what do I compare when one name is malformed?" cleanly.

One thing that would have tripped me: §19.1 step 4 does **not** mention the user-metadata
encoding byte's *value set*, yet R1's Detected cell says "open (top-level)". I nearly
filed this. It is closed by §19's own preamble, which is a governing clause above every
step: "Those enumerations are not the complete inventory of what a reader detects at
that tier: §21's register is … A row this section does not restate is due at its own
tier all the same." So R1 is due at open even though step 4 is silent. This is the
"read the paragraph above" discipline earning its keep.

---

## 3. Arithmetic and constants I checked myself

All computed with my own CRC-32C (reflected poly 0x82F63B78, init 0xFFFFFFFF, final XOR
0xFFFFFFFF), which I first validated against the document's own check vector.

| Quantity | I computed | Document states | Verdict |
|---|---|---|---|
| CRC-32C("123456789") | `0xE3069283` | `0xE3069283` (§4.5) | match |
| CRC-32C(zero bytes) | `0x00000000` | `0x00000000` (§4.5) | match |
| CRC-32C of 4 sentinel entries (80 B) | `0x80A34955`, stored `55 49 A3 80` | `0x80A34955`, `55 49 A3 80` (§7.4 example) | match |
| CRC-32C of that 4-byte CRC array | `0xC4EE982E` | `0xC4EE982E` (§7.4 example) | match |
| CRC-32C of 2¹⁶ sentinel entries | `0xEECB3BB2` | `0xEECB3BB2` (§15.4, App. B) | match |
| Appendix A trailer CRC over [0,60) | `0x402F157E`, stored `7E 15 2F 40` | `0x402F157E`, `7E 15 2F 40` | match |

Layer-record example (§7.4), field by field, packed with no padding:

```
name 1+3=4  [0,4)      layout 1 [4]        linearization 2 [5,7)
codec 2 [7,9)          filter 2 [9,11)     A 8 [11,19)
S 8 [19,27)            A_slab 8 [27,35)    rank 1 [35]
C 2 [36,38)            dim entry 1+1+8+8=18 [38,56)
chan entry 1+4+2+1+4=12 [56,68)            index_encoding 1 [68]
entry_count 8 [69,77)  crc_of_crc_array 4 [77,81)
```

Total 81 bytes; the document's offset column reads 0/4/5/7/9/11/19/27/35/36/38/40/48/56/63/68/69/77
and every one agrees with mine. Its own summing sentence — "4 + 34 … the dimension entry
18, the channel entry 12, and the trailing fixed fields 13 — 81 exactly" — checks:
1+2+2+2+8+8+8+1+2 = 34; 4+34+18+12+13 = 81. The nine scalars are indeed nine.
Extent length 4·20 + ⌈4/2¹⁶⌉·4 = 84: correct.

Other figures I re-derived and found correct:

- ⌈100/32⌉ = 4 (§7.4); grid (4, 8), N = 32, P = 65,536 (§11.2); ⌈1000/256⌉ = 4 (§11.2).
- §11.4 example: tile (1,2) → s = 1·8 + 2 = 10; in-tile (44,188) → 44·256 + 188 = 11,452;
  planar channel 2 → 2·32 + 10 = 74. All three correct.
- §15.4 example: entry_count 1,000,000 → ⌈/2¹⁶⌉ = 16 segments, last covering
  1,000,000 − 15·65,536 = 16,960 entries; CRC array 64 B; region 20,000,064 B; entry
  999,999 at segment-relative byte 20·16,959 = 339,180; CRC array at
  [20,000,000, 20,000,064); segment 15 at [19,660,800, 20,000,000) = 339,200 B ≈ 339 KB;
  a full segment 65,536·20 = 1,310,720 B = 1.25 MiB. All correct.
- §15.4 second example: disk ordinal 74 → region bytes [1,480, 1,500); channel 3's
  entries 96–127. Correct.
- §14.2 example: interleaved (2,3), P = 6, Q = 3, size 18; ordinal 5 at [15,18); planar
  uint16 plane 12 B with ordinal 5 at [10,12); (float32, bool) Q = 5, size 30, ordinal 5
  at [25,30). All correct. The general form u·Q + Fᶜ reduces from the table's
  (k div C)·Q + F_{k mod C} at k = u·C + c. Correct.
- §14.3 example: P = 10, alternating from true → byte 0 = 0x55, byte 1 = 0x01 with six
  pad bits; fill true → 0xFD. Correct.
- §14.5 example: extents (5,5) tiles (4,4) → grid 2×2; edge tile (1,1) has 1 real and 15
  padding positions; 32-byte tile, values 1–15 each `CD AB`. Correct.
- §17.3 example: 1.0/2.0/3.0 float32, s = 4, n = 3 → shuffled
  `00 00 00 00 00 00 80 00 40 3F 40 40`. I reproduced this byte for byte from
  "byte i of group j at offset i·n + j".
- §20.3 example: 32·20 + 4 = 644. Correct.
- §21.9 note: 2³² tiles → 2¹⁶ segments → 2¹⁸ B = 256 KiB; 2³⁶ → 2²² B = 4 MiB. Correct.
- §21.8's "120 conditions over 277 instances": I extracted every register row
  mechanically and counted instance cells by semicolon (a cell reading "—" counted as
  one, per §21.1). Rows: F 35, L 49, T 26, R 10 = **120** — matching the four
  subsection preambles' own "35 conditions", "49 conditions", "26 conditions",
  "10 conditions". Instances: F 56, L 116, T 55, R 50 = **277**. Both figures match the
  document exactly. I also spot-checked the instance *rules* of §21.1 against a dozen
  cells (L21 = 2 layouts × 2 directions = 4; T3/T14/T22 = 3 layouts × 2 = 6; T21/L44 =
  3 layouts × 1, "exceeds"/"larger than" bounding the direction; L37/F14 = 1, a checksum
  comparison having no magnitude ordering; R4 = 8 alternatives × 2 containers = 16).
  Every one came out as the cell states.

I found **no wrong constant, offset or checksum in this document.**

---

## 4. Validation timing by tier — the reader I would ship

**At open** (`[R-RDR-02]`): front block if resident; trailer; directory region and CRC;
the record walk; the layer-name namespace. Register rows F1–F36 (bar the
verifier-detected ones), plus L3/L5/L6 and L23's name-field instance, plus R1's
top-level instance.

**At first access to a layer** (§19.3): the *whole* of the layer record, and it is a
long list — slot validity (`[R-CNT-13]`), the §7.4 constraint set (`[R-CNT-23]`,
`[R-CNT-16]`), exact parse and sub-record walk and multiplicity (`[R-CNT-18]`,
`[R-CNT-14]`), dimension/channel name rules, the u64 value domain, the value sets of
§11.4/§12.2/§14.1/§15.1/§17.2/§17.3, bool fill (`[R-TYP-07]`), the lz4 declaration cap
(`[R-COD-07]`), the geometry floor and grid arithmetic, every `[R-ENC-04]` ceiling
including §14's decoded sizes, and the index cross-checks computable without I/O
(`[R-CNT-17]`). §19.3 closes with "All are decidable from the resident directory and F:
layer access performs no fetch". I checked that claim item by item and it holds — the
lz4 cap and the decoded sizes are functions of declarations alone, and `[R-CNT-17]`'s
extent_length identity compares two declared numbers.

**At use of a tile** (§19.4): index chain (L37/L38), entry classification (T6–T12),
payload CRC (T1), decode (T3, T13–T25).

**At use of a record's extent**: the extent CRC (R2) and the document content rules
(R3–R10) — "no earlier, since the open fetches no extent".

**What I may never check** (detector = verifier): the live-state coverage partition and
the slack total; extent overlap (F33, L18); a structure in the pre-trailer gap (F7);
record flag bits (F25/F26/F28, L46/L47/L49); a reserved-range record or sub-record type
(F36, L25); alignment and slab invariants (L40–L42); padding content, pad bits, and
interleaved boolean bytes (T2, T4, T5, T26); user-metadata member ordering (F27, L48).
A reader that skips all of these is still conforming; §22.3 says so plainly and tells a
pipeline to verify instead of merely read.

`[R-CNF-12]` lets me detect any of these earlier and reject — divergence is only ever
toward earlier rejection. That is a clean rule to implement against.

---

## 5. Layer access and the tile-read algorithm

From a layer name and a coordinate (x₀ … x_{d−1}):

1. **Domain.** Point request: 0 ≤ xᵢ < Eᵢ for every i, else the *request* fails with no
   verdict on the file. Region request: intersect with the extents; empty intersection
   succeeds and returns nothing. Note the deliberate seam: a single-position *range* is
   a region request, so it returns empty where the same coordinate as a *point* request
   fails. I would have got this wrong without §19.4's sentence saying so.
2. **Ordinals.** tᵢ = xᵢ div Tᵢ, uᵢ = xᵢ mod Tᵢ; in-tile ordinal Σ uᵢ·∏_{j>i} Tⱼ;
   spatial ordinal s = Σ tᵢ·∏_{j>i} Gⱼ (linearization 1, the only legal value); disk
   ordinal s interleaved, c·N + s planar.
3. **Index chain.** Region base = layer record extent_offset. Entry array =
   entry_count·20 bytes; CRC array = ⌈entry_count/2¹⁶⌉·4 bytes at region byte
   entry_count·20. Segment σ = k div 2¹⁶ covers entries [σ·2¹⁶, min((σ+1)·2¹⁶,
   entry_count)) at region bytes [20·σ·2¹⁶, …). Fetch the CRC array and the segment (may
   be parallel), verify crc_of_crc_array over the array, then the σ-th u32 over the
   segment. Both ranges are computable from the layer record alone — I confirmed this;
   nothing here needs a prior fetch. Failure is reject-**layer**, though detected at
   tile use.
4. **Entry.** Classify per §15.3. Sentinel → short-circuit: every requested position of
   that tile reads as that channel's recorded fill (planar) or every carried channel's
   fill in declared order (interleaved), bit-exactly, no I/O. Malformed → reject-tile,
   and fill is never a fallback.
5. **Payload.** Fetch [offset, offset + length); verify the entry's crc.
6. **Decode.** Codec first, then the filter's inverse. Length must be exactly the
   decoded size.
7. **Extract.** §14's offset arithmetic; never return a padding position.
8. **Return.** Bit patterns unaltered, with `[R-SER-08]`'s one resolved case.

### 5.1 The exact decoded byte layout I end up with

- **Interleaved**, any channel mix: P·Q bytes, Q = Σ Bᵢ (bool contributing 1). Channel
  c at in-tile ordinal u sits at byte u·Q + Fᶜ, Fᶜ = Σ_{j<c} Bⱼ.
- **Planar, numeric channel c**: P·Bᶜ bytes, value k at k·Bᶜ.
- **Planar, bool channel**: ⌈P/8⌉ bytes, value k at bit k mod 8 of byte k div 8, LSB
  first; final-byte bits P mod 8 … 7 are pad bits carrying the fill bit.

The filter: stride s = Bᶜ (planar numeric), Q (interleaved), 1 and identity (packed bool
plane). L = s·n divides in every case — I checked all three: P·Bᶜ/Bᶜ = P;
P·Q/Q = P; ⌈P/8⌉/1. Inverse: byte at i·n + j goes to j·s + i.

Everything I needed for this section the document gave me. I had to guess nothing.

### 5.2 Degradation walks, five traced end to end

1. **Unknown top-level record type, MU = 0, experimental range.** Skip it as though
   absent (ignore-record). Decoding unaffected. The file is conforming (§21.6); an
   updater preserves or drops it per its stored PE bit; a compactor may relocate its
   extent without parsing it, because §7.2 forbids an MU = 0 record from encoding
   offsets anywhere. I still serve every layer.
2. **Unknown *sub-record* type, MU = 1.** reject-layer, and — this is the clause I
   would have got wrong — "where the file is otherwise conforming a reader MUST NOT
   reject the file for it" (`[R-CNT-18]`). So I serve every other layer and refuse this
   one. §21.6's closing paragraph is explicit that the top-level/sub-record qualifier is
   load-bearing.
3. **Codec value 0x8123 (experimental).** Layer access fails: `[R-COD-03]` → L43,
   reject-layer. Every other layer still serves. I may still list this layer's name
   (§2.4's reject-layer row). Note the asymmetry against the metadata-encoding space,
   which §17.4's closing sentence and `[R-MTA-10]` handle differently and deliberately:
   an experimental *document* encoding is ignore-record and no violation.
4. **Truncated tail.** The physical file has grown past F, or the tail is a partial
   write. My trailer gates fail — magic (F8), or CRC (F14), or committed_file_length
   against the transport size (F17). reject-file. I MUST NOT scan backward
   (`[R-LIF-05]`). I cannot tell residue from corruption and §9.5's Note says I am not
   asked to. Recovery is a separate, deliberate tool (§9.6). On a shared filesystem I
   MAY retry once for attribute-cache staleness before concluding.
5. **Stored tile CRC mismatch.** T1, reject-tile. That tile's read reports failure; its
   neighbours in the same layer are unaffected; and — `[R-CNF-09]`, `[R-TYP-09]` — I
   MUST NOT quietly return fill for it. In a region read covering several tiles I MAY
   return the good tiles' values with a per-entry report of the failed one, or fail the
   whole request; I MUST NOT stand fill in. The one thing that escalates mid-request is
   a step-3 index-chain failure, which takes layer scope and bars the rest of the
   request and all further service from the layer, prospectively.
6. *(sixth, since it is the one that most changes my code shape)* **Format major 7.**
   `[R-CNF-13]` obliges me to run every *reaching* condition first — the trailer magic,
   the trailer CRC, and, if [0,16) is resident, the front block — and to report a
   failure of one as reject-file on that requirement's ground, not on capability
   grounds. Only if all reaching conditions pass do I emit the distinct "TARN format
   major 7; this reader supports major 1" diagnostic `[R-CNT-07]` asks for. That
   ordering falls straight out of §6.2's validation order, which is why §6.2 states the
   order normatively.
7. **A layer whose decoded tile size is 512 MiB.** Above §21.9's 256 MiB guarantee, so
   the file is conforming and outside `[R-CNF-03]`'s acceptance duty. I MAY decline at
   the tile, or the layer, or any containing scope up to the file — and MUST report the
   refusal as a resource limit, never as corruption.

---

## 6. The worked example: Appendix A, through my reader

```
0000  89 54 41 52 4E 0D 0A 1A  00 00 00 00 00 00 00 00
0010  00 00 00 00 ...
0040  8A 4E 52 41 54 0D 0A 1A  01 00 00 00 00 00 00 00
0050  10 00 ...                04 00 ...
0060  80 00 ...                EF CD AB 89 67 45 23 01
0070  00 00 00 00 00 00 00 00  00 00 00 00 7E 15 2F 40
```

Request 1: `bytes=-64` → 64 bytes, transport size 128.
- magic at [64,72) == `8A 4E 52 41 54 0D 0A 1A` ✓
- CRC-32C over [64,124) — I computed it independently from the field values, not by
  copying the file's bytes: `0x402F157E`, stored little-endian `7E 15 2F 40` ✓
- version_major = 1 ✓, version_minor = 0 (never gates)
- flags = 0 ✓; committed_file_length = 128 == 128 and 128 mod 64 = 0 ✓;
  dir_offset = 16 ≥ 16 ✓; dir_length = 4 ≥ 4 ✓; 16 + 4 = 20 ≤ 128 − 64 = 64 ✓;
  file_id = 0x0123456789ABCDEF ≠ 0 ✓; reserved [112,124) all zero ✓

Request 2: `bytes=16-19` → 4 bytes `00 00 00 00`. Region CRC = final 4 bytes = the
CRC-32C of the preceding dir_length − 4 = 0 bytes = `0x00000000` ✓. Record sequence is
empty, so zero records, no residue. Layer table empty. File opens.

Total: 2 requests, 68 bytes. `[R-CNT-27]`'s 128-byte floor is exactly met: 16 (front) +
4 (minimum directory at minimum offset) + pad to the 64-boundary + 64 (trailer).
20 → next 64-boundary is 64, so 44 bytes of pad, and 64 + 64 = 128. The floor argument
is sound and I reproduced it.

Appendix A's remarks on the front-block check are also right and worth an
implementer's attention: a speculative window of the whole 128 bytes makes [0,16)
resident and the equality check mandatory; a 112-byte suffix covering [16,128) still
contains the directory (so §6.4's containment test spares request 2) while leaving
[0,16) non-resident and the check optional.

---

## 7. Where I pushed hardest, and what I found

I read the nineteen changed passages first, then the whole document. The three findings
below all live in or beside §20.3 step 4 — the closed list of permissions — and they are
all one underlying shape: **the step expressly permits several changes in one commit,
and its surrounding prose reasons about each change as if taken alone.**

### 7.1 Deriving the list's members myself before reading its own census

Before reading the sentence that says "Between them the two lists reach every
declaration field of §7.4", I enumerated §7.4's fields and put each on a side:

| §7.4 field | side |
|---|---|
| name | permitted (may change) |
| layout | fixed |
| linearization | fixed |
| codec | fixed |
| filter | fixed |
| alignment A | permitted (declare / re-establish / clear) |
| slab S | permitted (same) |
| slab alignment A_slab | permitted, as part of "a slab … declaration" (§16.2 declares S *with* A_slab) |
| rank d | fixed |
| channel count C | permitted for planar via the channel list; fixed for interleaved |
| dimension name | permitted |
| dimension extent Eᵢ | permitted to grow; a shrink is named a rewrite |
| dimension tile extent Tᵢ | fixed |
| channel name | permitted |
| channel type | fixed |
| channel fill | fixed |
| index_encoding | fixed |
| entry_count / crc_of_crc_array / extent slot | neither — "follow the commit" |
| sub-records | neither — §20.4's subject |

Every field lands. I also checked the *rewrite* list against the *fixed* list and they
correspond one-for-one: shrink↔extent, fill change↔fill, re-type↔type,
re-tiling↔tile extent, transposition↔dimension order, rank, layout, linearization,
index encoding, codec, filter, interleaved channel list, non-terminal planar channel
position. Nothing on one list is missing from the other. That is a real partition, and
the "field on both sides" claim is right once you notice that the extent's *shrink* half
and the channel list's *interior* half sit in the rewrite list.

I then took each permitted member to its smallest legal instance:

- Shorten a planar channel list from C = 2 to C = 1: legal. From C = 1 to C = 0:
  barred by `[R-GEO-01]`'s floor, which the bounds paragraph names explicitly. Good.
- Extend a planar channel list from C = 1 to C = 2: the new channel's plane can raise
  the largest plane above `[R-COD-07]`'s lz4 cap; the bounds paragraph names L44 and
  says "the largest channel plane governing in a planar layer". Good.
- Grow an extent from Eᵢ to Eᵢ + 1 where Eᵢ mod Tᵢ ≠ 0: converts one padding position
  per edge tile into a real position, which `[R-SER-05]` already fixed to fill. Good.
- Declare an alignment on a layer whose tiles are frozen: only possible if they already
  satisfy it, which the step's own closing clause states ("every one the new state
  keeps, not only those this commit adds").

**Then I took two at once**, which is where the trouble is.

### 7.2 The construction

Planar layer, rank 1, dimension `x` with E = 8, T = 1, so G = 8 and N = 8. C = 4
channels, all uint8, decoded plane size P·Bᶜ = 1 byte. entry_count = C·N = 32;
extent_length = 32·20 + ⌈32/2¹⁶⌉·4 = 644. The layer stores at least one tile — say
channel 0 at s = 0 and channel 1 at s = 0 — so the closed list binds it.

One commit makes two permitted changes at once, as the step expressly allows:

- grow E from 8 to 16 (T unchanged at 1, so G and N go 8 → 16) — permitted, "an extent
  MAY grow";
- shorten the planar channel list from C = 4 to C = 2 — permitted, "shortened from its
  end".

New entry_count = C·N = 2·16 = **32**. Unchanged. New extent_length = **644**.
Unchanged. If channels 2 and 3 held only sentinels, the *stored-tile set* is unchanged
too — the same two tiles are stored.

But the index content changes completely. Under the old declarations, disk ordinal
8 was channel 1 at s = 0 (`[R-GEO-06]`: c·N + s = 1·8 + 0). Under the new ones,
ordinal 8 is channel 0 at s = 8, and channel 1 at s = 0 has moved to ordinal 16.
Every entry from 8 upward means something different.

The governing test at the head of step 4 — "Every layer whose stored-tile set or **index
content** this commit changes has its tile-index region re-emitted in full" — fires
correctly here. The prose around it does not.

### 7.3 Finding reader-01 — §13.3's Note, on what changes index content

> each commit that changes a layer's stored-tile set or its index content — which,
> among the declaration changes §20.3 permits a layer that stores a tile, only a change
> to entry_count does — re-emits that layer's whole tile-index region (§11.1, §20.3,
> `[R-WRT-04]`).

The parenthetical is a closed claim: among the permitted declaration changes, *only* a
change to entry_count changes the stored-tile set or the index content. The construction
above falsifies it. entry_count is unchanged, extent_length is unchanged, the stored-tile
set is unchanged, and the index content changes utterly.

An implementer who takes the parenthetical as its test keeps the extent slot pointing at
the old region. What comes out is a **fully conforming file**: entry_count equals the
geometry-derived C·N (`[R-CNT-17]`), extent_length matches the formula,
crc_of_crc_array and every segment CRC still verify over unmodified bytes, every entry
is well formed and in bounds, no extent overlaps. Not one of §21's 120 rows fires. And
its reference array is wrong: a reader asking for channel 0 at coordinate 8 is handed
the payload the writer stored for channel 1 at coordinate 0.

This is the same *shape* as round 31's survivor — a commit that reinterprets unchanged
stored bytes — reached through a different door.

I graded this **not byte-level**, honestly and with the counter-argument stated: the
block is labelled `> **Note — sparse writing.**`, so `[R-CNF-01]` makes it
non-normative, and the normative test at the head of §20.3 step 4 is unambiguous and
governs. Two *competent* implementations do not diverge. But the block cites
`[R-WRT-04]` as its authority and reads as a gloss on it, and if a triager finds the
head-of-step test less decisive than I do, the disputed file is conforming and the
emittable set moves.

### 7.4 Finding reader-02 — §20.3's "not offered as exhaustive" sentence

> The list is not offered as exhaustive: a change is permitted exactly where the
> declarations it produces satisfy every rule they are subject to.

Two readings, and the antecedent of "The list" is what separates them.

(A) *"The list" is the four-bound list in the sentence immediately before* —
`[R-COD-07]`'s lz4 cap, `[R-ENC-04]`'s ceiling, `[R-GEO-01]`'s floor, and §4.6's name
rules. Then the clause means: among the changes the closed list permits, one holds
exactly where its output declarations satisfy *every* rule, not merely those four. The
closed list stands.

(B) *"The list" is the permitted list or the rewrite list*, both of which are called
lists nearby and one of which is called "this list" three sentences earlier
("deciding which files would is the edge this list exists to remove"). Then "a change
is permitted exactly where the declarations it produces satisfy every rule they are
subject to" is a biconditional over changes at large — and it licenses a fill change, a
re-type, a re-tiling, a shrink, anything whose *resulting* declarations are individually
legal. A smaller extent is a perfectly legal declaration; so is a different fill; so is
a different tile extent. Under (B) the closed list is decorative.

I picked (A): nearest antecedent, and the closed list is stated with "with these
exceptions and **no other**" and enforced with "A commit **MUST NOT** change one of
these". Under §2.1 the capitalised MUST NOT binds, and a lowercase "is permitted"
cannot lift it. That is the same discrimination this project's §21.1 makes for a
register row against its rule.

But the sentence as written switches subject — the sentence before it says "A
**permitted** change holds provided…", this one says "a change is permitted…" — and
"exactly where" is an if-and-only-if. In the step this document has repaired most,
in the paragraph that states the bounds on a closed list, that is not a switch a reader
should have to repair in his head.

Not byte-level, because reading (A) is forced by the MUST NOT and by "and no other" one
paragraph up. I state the case for (B) fully so a triager can weigh it: under (B) the
disputed file — a commit that changes a fill value on a layer storing tiles — is
conforming, and only one reading lets a writer produce it in a commit.

### 7.5 Finding reader-03 — §20.3's account of a channel removal

> A channel removed from the end leaves its stored tiles' extents as slack (§5.2), and
> `[R-CNT-17]` obliges the smaller entry_count and so a re-emitted index region;

This is normative text, not a labelled block. In the construction of §7.2 the shortening
does **not** produce a smaller entry_count — the concurrent growth holds it at 32 — and
`[R-CNT-17]` obliges nothing, since extent_length still equals the formula. The
re-emission is still owed, but by the head-of-step "index content" test, not by this
route. The sentence describes the change as if taken alone, three sentences after the
step said "A commit MAY make several of these changes at once."

Grading: not byte-level. The sentence licenses nothing; it mis-attributes a mechanism,
and the obligation it mis-attributes is independently and unconditionally stated at the
head of the same requirement. But it is normative text making a false claim about a case
the same requirement expressly permits, and it is the second sentence in this surface —
after §13.3's Note — that reasons about one permitted change at a time.

---

## 8. Suspicions I opened and closed

Recorded because a clean lane has to show it looked.

- **`[R-CNF-03]`'s parenthetical** — "in a conforming file such a type is necessarily
  from the experimental range" — holds only if every conforming reader implements both
  *registered* record types, and `[R-CNF-03]`'s own list of non-declinable features
  (codecs, filters, layouts, sample types, metadata encodings) omits record types.
  §20.4 asserts it for updaters ("an updater implements both registered types") but not
  for readers. **Closed** by entailment: `[R-CNF-03]` requires handling every
  user-metadata encoding §18.2 assigns, which requires implementing type 0x0002, and
  requires handling both channel layouts and every core sample type, which cannot be
  done without implementing type 0x0001. Not a defect, but it is reasoning the reader
  must supply.
- **§21.6's closing paragraph** says of an experimental-range top-level MU = 1 type
  that "`[R-CNT-15]` obliges the reader to reject", omitting "that the reader does not
  implement" — `[R-CNT-15]` governs *unknown* types. **Closed** by §21.1's own escape:
  "where such an entry and the rule it cites diverge, the rule governs there too", and
  §2.3 states it correctly.
- **§20.3's principle for a grown extent** — "a grown extent adds positions that held
  their channel's fill (§14.5)" — reaches only the sub-case where the new positions were
  padding positions of an already-stored tile. It does not reach new positions inside
  tiles the growth newly *addresses*, which read as fill via `[R-TYP-08]`, not §14.5.
  **Closed**: the permission is stated unconditionally in the list, and step 4's own
  re-emission clause names "grown extents" as a source of "entries new to this
  generation", so growth beyond the current grid is plainly contemplated. An
  under-inclusive justification, with no operative consequence.
- **§19.4 step 2 speaks of "each requested channel c"** although neither request form
  §19.4 defines mentions channels. **Closed**: the reference array is per (coordinate,
  channel), so a channel subset is a projection of a defined request; nothing in the
  bytes forks.
- **`[R-CNF-05]` against `[R-CNF-06]`** — an appender that extends a file carrying a
  latent violation emits a nonconforming file, which "A writer MUST emit only conforming
  files" would forbid. **Closed**: conforming updater is a separate class, and
  `[R-CNF-06]` scopes the duty to "the bytes it produces", with §20.1 and §20.3 step 2
  spelling out that reproducing bytes unchanged is not authoring them.
- **`[R-MTA-06]`'s "writers MUST NOT emit a `tarn.`-prefixed key…"** against §21.6's
  "A file carrying an unrecognized `tarn.` key is conforming". **Closed**: §2.3 names
  "which registry version a writer targets (§10.3, §18.3)" as a conduct rule that binds
  the actor and never the bytes, and §18.3 is exactly this rule.
- **§6.2's pre-trailer gap longer than step 5's pad** is detectable by a verifier but
  carries no register row. **Closed**: §2.3 expressly declares it not a
  file-conformance violation, and §6.2 says "a longer gap is conforming".
- **§11.1's Rationale** — "Growth that leaves entry_count unchanged touches the
  directory alone". **Closed**: it is scoped to growth *alone*, and for growth alone the
  claim is provable — every Gᵢ is non-decreasing in Eᵢ, so an unchanged positive product
  forces every Gᵢ unchanged, hence unchanged ordinals. It is the one nearby sentence of
  this family that is right, which is why §13.3's is worth flagging.
- **§15.3's overlapping rows** — an entry with offset = length = sentinel and crc ≠ 0
  satisfies both the "crc ≠ 0" row and the ">2⁶³ − 1" row (T6 and T11). **Closed**:
  both are *structural* reject-tile, and §21.1's specialization rule assigns the file to
  the narrower row, with the list of pairs expressly "not offered as closed".
- **§17.1's stage order against §19.4 step 6** — "codec decodes the stored bytes, the
  filter's inverse is applied" versus "Apply the codec, then the filter's inverse".
  **Closed**: identical, and the byte-shuffle preserves length so `[R-SER-07]`'s size
  check is equivalent before or after the inverse.
- **Single_Segment_Flag and §21.9's 8 MiB `Window_Size` row** for a tile — a
  single-segment frame's Window_Size is its content size, which `[R-COD-06]` obliges to
  equal the decoded size, so a tile above 8 MiB cannot satisfy the SHOULD when framed
  that way. **Closed**: a Window_Descriptor frame can declare a smaller window than the
  content, so the SHOULD is satisfiable; and §18.2 makes exactly this point for the
  document case and tells a writer which framing to choose.
- **Register completeness.** I tried to name a detectable file-conformance violation
  with no row: sub-record residue (L14), file-level residue (F29), slot (0,0) with
  entry_count > 0 (L22), a stale slab declaration (§16.2's Note: detected as L41/L42, no
  row of its own by design), nesting beyond two (§7.4's Note: no reader-detectable
  witness), `[R-ENC-06]`'s field widths (§21.7: no condition a file can exhibit), a
  strictly-non-increasing committed_file_length (unwitnessed from one file), an index
  region overlapping the directory (F33's "tile-index regions" instance). Every one is
  either registered or expressly and correctly excluded. I found no omission.

## 9. Where I found little, and what I did that would have found something

The open path, validation timing, the tile-read algorithm and the decoded byte layout
came out clean. That is not an absence of effort: I derived every byte offset in §7.4's
layer-record example independently and compared all eighteen of them; I recomputed all
six CRC constants the document states, including the 1.25 MiB all-sentinel segment; I
re-derived every worked example in §11.2, §11.4, §14.2, §14.3, §14.5, §15.4, §17.3 and
§20.3 and reproduced the shuffle example byte for byte; I extracted all 120 register
rows mechanically and counted 277 instances against §21.8's figure and the four
subsection counts; I traced seven degradation paths end to end; and I derived
`[R-CNF-13]`'s reaching set from `[R-CNT-24]` before reading §21.2's answer. Had a
constant, an offset, a count or a reaching-set membership been wrong, those passes would
have shown it. They did not.

The three findings are all in one place because that is where a two-at-once construction
bites, and I only got there by taking the brief's instruction literally: derive the
list's members, take each to its smallest legal instance, and then take two at once.
