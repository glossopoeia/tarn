# Cleanroom round 31 — Reader implementer transcript

## 0. Disclosure and setup

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,790 lines), in five `Read` calls covering lines 1–4790 with no gaps. I opened no
other file in the repository, ran no `git` command, listed no directory, and made no
network request. I did not read the output directory this transcript is written to.

The brief's path was correct: the spec is where it says it is.

**Context I did not ask for.** My runtime placed several things in context before I
began: a project instruction file (`CLAUDE.md`, which only forwards to `AGENTS.md`),
an index of the maintainer's auto-memory naming several TARN-process notes, a git
status block with the last five commit subject lines, and an MCP server instruction
about which tool to prefer for reading files. The commit subjects in particular name
ADR numbers and describe decisions. **I did not open any of it and I have not used any
of it as evidence.** Where a commit subject appeared to describe a rule, I re-derived
the rule from §6.3, §20.3, §20.4 and §20.5 of the specification and cite only the
specification below. I disclose its appearance because the brief requires it.

Files I wrote, all under my own scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r31-round/scratch/reader/`:

- `crc_checks_rdr.py` — CRC-32C implementation and all the document's stated checksums
- `count_instances_rdr.py` — register row and instance counter
- `s_rdr.py` — whitespace-normalised phrase search (joins hard wraps, strips `> `)
- `norm_rdr.txt` — the normalised document (intermediate)
- `worked_file_rdr.py` — builds a complete TARN file from §7.4's example layer and
  walks §19.1/§19.3/§19.4 over it
- `worked.tarn` — the 448-byte file that script emits

Nothing was written to the parent directory or to the repository.

I ran my searches through `s_rdr.py`, which normalises whitespace before matching, for
exactly the reason the brief gives. I sanity-checked the instrument on phrases I knew
were present and hard-wrapped (`"MUST accept every conforming file"` spans a line
break in the source and my normaliser found it; a naive `grep` for it returns zero).

---

## 1. Constants and arithmetic — everything the document states, checked

Before writing a line of reader code I implemented CRC-32C from §4.5's parameters
(Castagnoli 0x1EDC6F41, reflected in and out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF,
stored little-endian) and checked it against the document's own check vector, then
used it on every stated checksum in the document.

| Quantity | Document | Mine |
|---|---|---|
| §4.5 CRC-32C(`"123456789"`) | `0xE3069283` | `0xE3069283` ✓ |
| §4.5 CRC-32C(zero bytes) | `0x00000000` | `0x00000000` ✓ |
| §15.4 CRC of a full 2¹⁶-sentinel segment | `0xEECB3BB2` | `0xEECB3BB2` ✓ |
| §7.4 example, CRC over 80 bytes of 4 sentinels | `0x80A34955`, stored `55 49 A3 80` | `0x80A34955` ✓ |
| §7.4 example `crc_of_crc_array` | `0xC4EE982E`, stored `2E 98 EE C4` | `0xC4EE982E` ✓ |
| Appendix A trailer CRC over bytes [0,60) | `0x402F157E`, stored `7E 15 2F 40` | `0x402F157E` ✓ |

I rebuilt §7.4's example inline payload byte for byte from the field order in the
table. My reconstruction is byte-identical to the hex dump the Example gives, and its
length is 81, matching both the stated total and the stated breakdown
(4 + 34 + 18 + 12 + 13 = 81). Field offsets land where the Example's left column says:
38 after channel count, 56 after the dimension entry, 63 after the channel name+type,
68 after the fill, 81 total, no residue, so the sub-record sequence is empty. ✓
`[R-CNT-17]`'s arithmetic for that layer, 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84, matches the
Example's stated extent length. ✓

Other examples I re-derived and confirmed:

- §11.2: extents (1024, 2048), tiles (256, 256) → G = (4, 8), N = 32, P = 65,536 ✓;
  extent 1000 still gives G_y = 4 ✓.
- §11.4: tile (1,0) → s = 8; coordinate (300, 700) → tile (1,2), s = 10, in-tile
  (44, 188), in-tile ordinal 44·256 + 188 = 11,452; planar C = 4, channel 2 →
  disk ordinal 2·32 + 10 = 74 ✓.
- §14.2: interleaved T=(2,3), channels uint8+uint16 → Q = 3, decoded size 18, ordinal
  5 at bytes [15,18) ✓; planar `b` plane 12 bytes, ordinal 5 at 10–11 ✓;
  float32+bool → Q = 5, size 30, ordinal 5 at [25,30) ✓.
- §14.3: planar bool T=(2,5), P = 10, alternating → `55 01` with fill false and
  `55 FD` with fill true (pad bits 2–7) ✓.
- §14.5: extents (5,5), tiles (4,4) → grid 2×2, edge tile (1,1) has 1 real position
  and 15 padding; uint16 fill `0xABCD` → 32 bytes, value 0 real, values 1–15 `CD AB` ✓.
  (Coordinate (4,4) has in-tile position (0,0), so ordinal 0 — the Example's "value 0
  is the stored sample" is right.)
- §15.4: entry_count 1,000,000 → 16 segments (15 full, last 16,960 entries), 64-byte
  CRC array, region 20,000,064 bytes; tile 999,999 in segment 15 at segment-relative
  byte 339,180; array at [20,000,000, 20,000,064); segment 15 at
  [19,660,800, 20,000,000) = 339,200 bytes ("~339 KB") ✓; one full segment = 1.25 MiB ✓.
  Second example: disk ordinal 74 → entry bytes [1,480, 1,500) ✓; channel 3's entries
  are 96–127 ✓.
- §17.3: three float32 1.0/2.0/3.0 shuffled at s = 4, n = 3 →
  `00 00 00 00 00 00 80 00 40 3F 40 40` ✓, and the inverse formula
  (byte i·n+j restored to j·s+i) is the exact inverse of the forward one ✓.
- §16.2: grid 4×8, S = 8 → runs [0,8), [8,16), [16,24), [24,32); tile rows 1–2 =
  ordinals 8–23 = runs 1 and 2 ✓.
- §12.3: the `temp` channel entry is the 12 bytes given ✓.
- §12.1: bfloat16 1.0 = `0x3F80` from binary32 `0x3F800000` ✓; `0x7FC0` is a quiet
  NaN ✓.
- §4.6: `température` NFC = 12 bytes, NFD = 13 ✓.
- §21.9's Note: ⌈2³²/2¹⁶⌉ × 4 = 256 KiB ✓; at 2³⁶ it is 4 MiB ✓.
- §17.2's Note on zstd: RFC 8878's Window_Descriptor floor is windowLog 10 = 1 KiB, so
  a sub-1-KiB tile is single-segment-only, exactly as stated ✓.
- Front block `89 54 41 52 4E 0D 0A 1A` decodes as \x89 "TARN" CR LF ctrl-Z ✓; trailer
  magic `8A 4E 52 41 54 0D 0A 1A` as \x8A "NRAT" CR LF ctrl-Z ✓, first byte differing
  from the front block's as §6.2's Note claims ✓.
- lz4 frame magic `04 22 4D 18` (T23) is the little-endian encoding of 0x184D2204 ✓;
  zstd `28 B5 2F FD` of 0xFD2FB528 ✓.

**Register counts.** I parsed the four register tables mechanically and counted rows
and semicolon-separated Instances cells under §21.1's rule that a `—` cell is one
instance:

- §21.2: 35 rows / 56 instances — document says "35 conditions" ✓ (F11 struck, F1–F36)
- §21.3: 49 rows / 116 instances — "49 conditions" ✓
- §21.4: 26 rows / 55 instances — "26 conditions" ✓
- §21.5: 10 rows / 50 instances — "10 conditions" ✓
- Total: **120 rows / 277 instances** — §21.8 says "120 conditions over 277 instances" ✓

I spot-checked the instance arithmetic against §21.1's stated axes: T3, T14 and T22 are
each 3 layout formulas × 2 magnitude directions = 6 ✓; T21 and L44 are 3 layout formulas
with no direction because their comparisons are one-directional ("exceeds", "larger
than") ✓; L21 is 2 layouts × 2 directions = 4 ✓; R4 is 8 alternatives × 2 containers =
16 ✓; T24 is one instance because "any codec" is one shape ✓. L2's nine designated
quantities are exactly the designated ones that can overflow independently — ⌈P/8⌉ is
correctly absent because ⌈P/8⌉ ≤ P and P is itself listed, V = P·C is dominated by P·Q
since Q = ΣBᵢ ≥ C, and (C−1)·N + (N−1) = C·N − 1 is dominated by C·N ✓.

**§20.5's closed count.** The passage claims that of §10.1's four growth vehicles, two
reach a conforming file (a carried ignore-lane bit, an unrecognised `tarn.` key) and the
other two reach one only as reserved-range violations, giving "F36 and L25 for a record
type, and one row for each of the other seven spaces §10.2 tabulates (L31, L33, L34,
L36, L43, L45, R1)". I derived the mapping independently: layout→L36, linearization→L33,
sample type→L34, codec→L43, filter→L45, index encoding→L31, metadata encoding→R1 —
seven spaces, seven rows, one each, and no space has a second row. ✓ Correct.

I found **no wrong constant, offset or checksum anywhere in the document.**

---

## 2. The open path, as I would write it

### 2.1 Cold remote open, byte-exact

Two requests, per §6.4 `[R-CNT-09]`.

**Request 1 — a suffix range of exactly 64 bytes.** What bounds it before I have read
anything: `[R-CNT-24]`, which fixes for *every* format major that the final 64 bytes
carry the trailer magic at F − 64, version_major/minor at F − 56, and a CRC-32C at
F − 4 over [F − 64, F − 4). So the 64 is a constant of the format, not a value read
from the file. The response also carries the transport-authoritative F
(`[R-CNT-10]`), which is why §19.1's steps 1 and 2 cost one request between them.
If the transport cannot give a transport-authoritative size — a `Content-Range` with
`*` as the total — `[R-CNT-10]` obliges a separate probe or a failed open, and
explicitly bars substituting `committed_file_length` for it. Good: that closes the
obvious self-referential hole.

**Validation of request 1**, in §6.2's mandatory order: magic; trailer CRC; version
gate; then, all before acting on the fields, the flag gates, `committed_file_length`
== transport size and ≡ 0 (mod 64), `dir_offset` ≥ 16, `dir_length` ≥ 4,
`dir_offset + dir_length` ≤ F − 64 (a designated `[R-ENC-04]` sum), `file_id` ≠ 0,
reserved 12 bytes zero. §6.2 does not itself list the 2⁶³ − 1 domain check on
dir_offset/dir_length/committed_file_length, but §19's preamble is explicit that the
step enumerations are not the inventory and §21's register is, and F2 puts that check
at the open. I implemented it there.

**Request 2 — `[dir_offset, dir_offset + dir_length)`.** Bounded before reading by the
two gates just validated: ≥ 16 below and ≤ F − 64 above. Verify the terminal CRC-32C
over the preceding `dir_length − 4` bytes before any other use (`[R-CNT-11]`), then
parse.

**Total: 2 requests, 64 + dir_length bytes.** For Appendix A's 128-byte file that is
64 + 4 = 68 bytes. For the file I built in §5 below it is 64 + 109 = 173 bytes. The
count is independent of file size and layer count, which is the invariant §6.4's Note
says the section exists to make legible.

A reader may collapse this to one request by speculating a suffix window and using
containment. Appendix A's arithmetic for that is right: a 112-byte window covers
[16, 128), which contains the directory but not bytes [0, 16), so the front-block check
stays optional; a 128-byte window reaches offset 0 and the check becomes mandatory.

### 2.2 The front block

`[R-CNT-04]` keys the obligation to **residency**, not to transport. My reader reads
local files whole, so [0, 16) is always resident and I verify by byte equality before
anything else; my remote path speculates a 64 KiB suffix and therefore checks the
block only on files ≤ 65,536 bytes, where the window reaches 0. The rule is decidable
at my own open path without classifying the network, which is what §6.1 says it is
for. Mismatch → reject-file, and F1's front-block instance is the byte-reversed
special case.

### 2.3 Record walk (§19.1 step 4)

24-byte header, then `inline_length` bytes; the sequence must consume
`dir_length − 4` exactly with no residue (F29). Type 0 is a validity error, never an
unknown type (F24). Unknown top-level type: MU = 1 → reject-file, MU = 0 →
ignore-record. At most one top-level user-metadata record (F34). Extent-slot rules
(`[R-CNT-13]`) apply here to **non-layer** top-level records only — a layer record's
slot is layer-scope and deferred to §19.3, which is exactly how F30/F31/F32 and
L15/L16/L17 are split. The user-metadata framing checks — no (0,0) slot,
`extent_length` ≥ 5, `inline_length` exactly 1 — are due here for the top-level record
(F21, F22, F23) and at layer access for a sub-record (L10, L11, L12).

Layer-name namespace: built from the name fields obtainable under §7.4's framing.
§19.1 is unusually careful here and I needed all of it — a layer record whose name
field does not fit inside its `inline_length` contributes *no* name (so it cannot be
half of a duplicate) and is instead an L23 layer-scope error; uniqueness is decided
over raw bytes first, before well-formedness, so two byte-identical invalid names are
still F4. Without that paragraph I would have had to guess the order.

---

## 3. Validation timing by tier

`[R-RDR-02]` fixes the *latest* detection point; earlier is always licensed
(`[R-CNF-12]`). My four tiers:

- **Open:** front block (if resident), trailer, directory region and record walk,
  layer-name namespace. A layer record's own name rules (L3, L5, L6) land here too,
  even though their scope is the layer — a layer-scope rejection established at open.
- **First access to a layer:** the whole of §19.3 — extent slot, the §7.4 constraint
  set, exact parse and sub-record walk, sub-record multiplicity, dimension and channel
  name rules, the u64 value domain, the six value sets, bool fill constraint, the lz4
  declaration bound, the geometry floor and its arithmetic, the 2⁶³ − 1 ceiling on
  every designated derived quantity including the decoded sizes, and the two index
  cross-checks that need no I/O. §19.3 states that all of it is decidable from the
  resident directory and F, so **layer access performs no fetch**. I confirmed that on
  my worked file: every one of those checks ran against bytes already in hand.
- **Use of a tile:** index chain, entry classification, payload CRC, decode. Note the
  scope inversion §19.2 calls out explicitly: an index-chain failure is detected at
  tile use but takes *layer* scope (`[R-IDX-04]`).
- **Use of a record's extent:** the extent CRC and whichever document content rules
  §18.2 attaches at that record's encoding. Nothing here is due at open, because the
  open fetches no extent.

**Never checked by a conforming reader**, per §21's Detector column: live-state
coverage and the slack total, extent overlap (F33, L18), record flag bits (F25, F26,
F28, L46, L47, L49), a structure in the pre-trailer gap (F7), reserved-range type
values as such (F36, L25), alignment and slab invariants (L40–L42), decoded-content
obligations (T2, T4, T5, T26), and user-metadata member ordering (F27, L48). I counted
20 verifier rows and checked them against Appendix H's verifier checklist: every one is
there, with T26 covered because its own row says "the check that detects it is T2's or
T4's". The checklist is complete.

---

## 4. Layer access and the tile-read algorithm

Geometry: Gᵢ = ⌈Eᵢ/Tᵢ⌉ stated as Eᵢ/Tᵢ plus 1 when Eᵢ mod Tᵢ ≠ 0, deliberately avoiding
the (E + T − 1)/T idiom that can overflow the declared domain. N = ∏Gᵢ, P = ∏Tᵢ,
addressed-tile count N (interleaved) or C·N (planar), all designated and all checked
against 2⁶³ − 1 at layer access.

Ordinals: tᵢ = xᵢ div Tᵢ, uᵢ = xᵢ mod Tᵢ; in-tile ordinal Σ uᵢ ∏_{j>i} Tⱼ, row-major for
every linearization value permanently; spatial ordinal s = Σ tᵢ ∏_{j>i} Gⱼ under
linearization 1; disk ordinal s interleaved, c·N + s planar.

Index: region = entry_count × 20 bytes of entries, then ⌈entry_count/2¹⁶⌉ × 4 bytes of
segment CRCs, contiguous, no padding. Entry k at region byte 20k. To use entry k:
verify `crc_of_crc_array` over the fetched array and the segment CRC over the fetched
segment — both ranges computable from the layer record alone, so they may be fetched in
parallel, and both verifications may be cached under committed-prefix immutability.

Entry classification (§15.3): I implemented the eight reader rows as an ordered
cascade. The two "reserved pattern" rows and the domain rows can both fire on the same
entry, but they agree on the outcome, and T11's own text excludes the all-ones value
so T6 and T11 are actually disjoint. The *structural* marking matters downstream: such
an entry contributes no extent to the verifier rows, to slab run continuity, or to the
coverage walk, while an entry that merely fails its payload CRC keeps its extent
everywhere. That distinction is stated three times (§15.3, §16.2, §9.7) and is
consistent in all three.

Decode: codec first, then the filter's inverse (§17.1, §19.4 step 6 — the reverse of
the writer's filter-then-codec). Decoded length must be exactly the declared decoded
size (`[R-SER-07]`), which comes from declarations only, never from the payload or any
embedded size field. Under codec 1 the *stored* length must equal the decoded size too
(`[R-COD-04]`), checkable from the entry and the layer record before any payload fetch —
I placed that between steps 4 and 5.

Byte-shuffle: stride is the channel element size for a planar tile, Q for an
interleaved tile, 1 (identity) for a packed bool plane. L is divisible by s in every
one of those cases — P·Bᶜ by Bᶜ, P·Q by Q, ⌈P/8⌉ by 1 — which I checked exhaustively
over the layouts, so the "in every case" is true and there is no fourth case.

Decoded byte layout I end up with:

- planar numeric channel c: P · Bᶜ bytes, value k at k·Bᶜ, little-endian
- planar bool: ⌈P/8⌉ bytes, value k at bit k mod 8 of byte k div 8, LSB-first, with
  final-byte pad bits carrying the fill bit
- interleaved: P · Q bytes, channel c's value at in-tile ordinal u at u·Q + Fᶜ

Fill: produced by exactly one condition — a valid sentinel entry read from a verified
chain. Never as a fallback for a rejected tile, a failed CRC, or a resource decline;
`[R-TYP-09]` closes that door and `[R-CNF-09]` restates it, and Appendix H's reader
checklist restates it again. All three agree.

---

## 5. Worked example — a complete file built and read

§7.4's Example gives a layer record but no file around it, so I built one, using its
layer verbatim except that I store tile 0 (the Example stores none, which changes the
segment CRC and `crc_of_crc_array`). Layer `sst`: rank 1, dimension `x` extent 100 tile
extent 32, interleaved, one float32 channel `temp` with fill `0x7FC00000`, codec 1,
filter 1, no alignment or slab. G = 4, N = 4, P = 32, Q = 4, decoded size 128,
entry_count 4.

```
[0, 16)      front signature block
[16, 144)    tile 0 payload, 128 bytes (float32 values 0.0 … 31.0)
[144, 228)   tile-index region, 84 bytes:
               entry 0  offset 16, length 128, crc 0xF8118D31
               entries 1-3  FF x16 00 x4  (sentinel)
               segment CRC array (1 u32)  0xB76F7866
[228, 337)   directory region, 109 bytes = one 105-byte layer record + CRC
               record header: type 0x0001, flags 0b11, inline_length 81,
                              extent (144, 84)
               inline payload: the 81 bytes of §7.4's Example with
                              crc_of_crc_array = 0x9F491382
[337, 384)   pre-trailer pad, 47 bytes (step 5 pads to the next 64 boundary)
[384, 448)   trailer, F = 448, 448 mod 64 = 0
```

`dir_offset + dir_length = 337 ≤ F − 64 = 384` ✓. The reader walk over these bytes
succeeds at every step: front block equal; trailer magic, CRC, version 1, flags 0, all
seven remaining gates pass; directory CRC verifies; one layer record parses with zero
residue so its sub-record sequence is empty; derived G = [4] equals the declared
entry_count 4 (`[R-CNT-17]`); declared extent_length 84 equals 4 × 20 + 1 × 4
(`[R-CNT-17]`); `crc_of_crc_array` verifies over the 4-byte array;
segment 0's CRC verifies over the 80 entry bytes; entry 0 classifies non-sentinel with
length 128 = decoded size (`[R-COD-04]`); the payload CRC verifies; a point request for
x = 5 lands in tile 0 at in-tile ordinal 5, byte offset 20, and returns bit pattern
`0x40A00000` = 5.0f unaltered; a request in tile 3 short-circuits to the recorded fill
`0x7FC00000` with no payload I/O.

The document sufficed to build and read this file without a single guess. Everything I
needed — field order, widths, the exact bytes each checksum covers, the region layout,
the ordinal formulas, the pad rule — was stated where I looked for it.

---

## 6. Degradation walks

**(1) Unknown record type.** Top-level, MU = 0 → ignore-record; I still serve every
layer, and if I am an updater I preserve or drop it per its PE bit. Top-level, MU = 1 →
reject-file, and if the type is from the reserved range the file is additionally
nonconforming (F35/F36) while if it is experimental the file is *conforming* and my
refusal records my capability, not a defect (§21.6). Sub-record, MU = 1 → reject-layer;
`[R-CNT-18]` explicitly forbids rejecting an otherwise-conforming file for it, so I
serve every other layer. Sub-record, MU = 0 → ignore-record. **Determined at every
branch except one** — see finding reader-01, which is about what I still owe the file's
*other* layers in the sub-record case.

**(2) Unknown codec.** Unreachable for me: codecs 1–4 are all core and `[R-CNF-03]`
makes software that declines one a non-reader. A declared value of 0, 5–0x7FFF or
≥ 0x8000 is L43, reject-layer at layer access, detected from declarations with no I/O.
Same shape for filters (L45). I serve every other layer and may still list the rejected
layer's name (§2.4). Determined.

**(3) Unrecognised flag or enum value.** Incompat-lane bit set (bits 0–15) → F19,
reject-file, and since this text defines no bits every such bit is unimplemented.
Ignore-lane bit set (bits 16–31) → ignore it; the file is conforming (§21.6). Enum
values outside the assigned sets in layout, linearization, sample type, codec, filter
and index_encoding → reject-layer (L36, L33, L34, L43, L45, L31). Metadata encoding: 0
or reserved 3–0x7F → ignore-record *and* a violation (R1); experimental ≥ 0x80 →
ignore-record and *not* a violation (§21.6), with a verifier obliged to report the
record it ignored rather than treat it as a bar to certification (`[R-MTA-10]`).
Determined; the asymmetry between the codec space and the metadata-encoding space is
stated four times (§10.3, §17.4, §18.2, §21.6) and reads the same in all four.

**(4) Truncated tail / torn commit.** I read [size − 64, size). If the magic fails
(F8), the CRC fails (F14), or `committed_file_length` ≠ the transport size (F17), I
report the file torn or invalid and **must not scan backward** (`[R-LIF-05]`). §9.5's
Note licenses a retry against attribute-cache staleness before concluding. Recovery is
a deliberate separate operation (§9.6) and never an implicit step of my open. §9.2's
crash figure and §9.5's Note together told me that residue past a *completed* commit
carries no register row of its own: I meet it as one of those three trailer gates and
am not asked to tell residue from corruption. Determined.

**(5) Checksum mismatch, by link.** Trailer CRC → reject-file. Directory CRC →
reject-file. `crc_of_crc_array` (L37) or a segment CRC (L38) → reject-layer, detected
at tile use. A stored tile's crc (T1) → reject-tile, and I must not return fill in its
place. A user-metadata extent's CRC (R2) → ignore-record with a SHOULD-report, because
the document is quarantined and application metadata never invalidates the structural
data it annotates. Determined at every link; §8.2's chain is strictly ordered and
§8.1's map assigns exactly one checksum to every field, which I verified is genuinely
exhaustive (front block by equality; three terminal fields covered by nothing; segment
CRC array, entry crcs and `crc_of_crc_array` each interior and each covered once; an
unassigned type's extent covered by nothing).

**(6) Limit exceeded.** §21.9's eight rows are minimum guarantees, not caps. A file
exceeding one stays conforming; I may decline it at the whole file or at the narrowest
scope whose quantities exceed what I can serve — layer, tile, or the record carrying a
user-metadata document. The refusal **must be reported as a resource limit and not as a
validity error**, and I must not return fill for a declined tile (`[R-TYP-09]` again).
Software that declines *on that ground* a file entirely within the table is not a
conforming reader. Determined, and §21.9's individuation of the last three rows
(per-instance, over addressed tiles / actual documents / actual frames) answers the one
question I had, which was whether a layer addressing no tile has a tile whose decoded
size the table bounds. It does not.

**(7) Format major I do not implement.** Reject-file with a diagnostic distinct from
"not a TARN file" and from "corrupt". But not *only* that: `[R-CNF-13]` obliges me to
apply every **reaching** condition first, and to report a reaching failure on its own
requirement's ground rather than on capability grounds. I derived the reaching set
independently from `[R-CNT-24]`'s four fixed invariants and got exactly the five
instances §21.2 names — F8 and F1's trailer-magic instance (magic), F14 (trailer CRC),
F6 and F1's front-block instance (front block) — and no others. F13 (64-alignment),
F15 (reserved bytes), F17 (length cross-check) and F19 (flags) all read fields inside
the 48 bytes a future major may redefine, or assert invariants `[R-CNT-24]` does not
fix, so none reaches; F5 does not reach because its 128-byte floor is derived from
format major 1's directory minimums; F18 is outside the premise because
version_major = 0 declares no major at all. Every one of those exclusions is stated,
three of them in §2.3's Note. Determined.

**(8) Region read spanning a rejected tile.** Bounded to that tile's positions: I may
return the validating entries' values with a per-entry report, or fail the request
whole, but never substitute fill. A step-3 index-chain failure inside the same request
takes layer scope instead and bars the request's remaining entries and all further
service from the layer, prospectively — values already returned stand. Determined.

---

## 7. Where I pressed hardest, and what I found

I gave the seventeen named passages a line-by-line reading and then went looking for
the sentences that would have been written under a rule that has since moved.

### 7.1 The flags prohibition, checked word for word in five places

The new prohibition appears at §2.3 `[R-CNF-02]`, §6.3 `[R-CNT-08]` (twice — once for
the compactor, once for the updater), §20.3 step 6 `[R-WRT-04]`, §20.5 `[R-WRT-06]`,
and Appendix G item 8. The operative formulas:

- §6.3 compactor: "carries the input's unknown ignore-lane bits into its output trailer
  rather than writing flags = 0, and **sets no other**"
- §6.3 updater: "MUST copy forward unknown ignore-lane bits of the file it modifies,
  MUST NOT clear them, and **MUST NOT set any other**"
- §20.3 step 6: "unknown ignore-lane flag bits copied forward and **no other set**"
- §20.5: "MUST copy the input's unknown ignore-lane flag bits forward and **set no
  other**"
- Appendix G item 8: "carries its input's unknown ignore-lane bits forward instead,
  **setting no other**"

These are substantively identical. I looked for the joint-unsatisfiability shape the
brief warns about, on the theory that §6.3's creator rule ("a writer creating a file
under this text MUST write flags = 0") could collide with the compactor's copy-forward
duty, since §20.5 obliges a compactor to follow the *creation* path. §6.3 carves the
compactor out by name in the sentence immediately before, and §2.3, §20.5 and
Appendix G item 8 all repeat the carve-out. No collision.

I also checked the qualifier in §2.3 — "§6.3's flags rules **against a set ignore-lane
bit**". That qualifier is doing real work and is right: the creator's flags = 0 rule and
the updater's "set no other" both also bar setting an *incompat*-lane bit, and that
violation *is* a file-conformance violation (F19, reject-file). Restricting the
conduct-rule declaration to the ignore-lane half keeps F19 reachable. I then tested
§2.3's claim that these plus §6.2's over-long pre-trailer gap "are the cases this text
states" by enumerating every writer MUST in the document whose violation leaves the
file conforming: `[R-MTA-05]`, `[R-CNT-12]`, `[R-CNT-22]`, `[R-LIF-04]` and `[R-SLB-04]`
all expressly make the file nonconforming; `[R-COD-06]`'s undisclosed dictionary and
`[R-COD-10]`'s wrong stride are *unwitnessed* violations, which §21.7 says still bind
the actor and still make the file nonconforming; `[R-CNT-03]`, `[R-TYP-10]`,
`[R-CNT-26]`, `[R-ENC-14]` and `[R-MTA-07]` are SHOULDs. The closed list survives.

### 7.2 The widened drop licence

"an updater MAY drop the record in any commit it is otherwise free to make — one whose
only effect is the drop included". I traced every sentence that could have assumed a
drop needs another edit alongside it: §2.4's preserve-verbatim row (names the MU = 1 and
MU = 0/PE = 1 rows only, so it is correct under the new licence), §20.3 step 2 ("MUST
NOT drop the record save where §20.4 licenses the drop"), §20.5 ("less any record §20.4
lets it drop", and "Dropping is the one disposal that answers"), §22.3 (an unassigned
extent carried forward unread), and §23.1 (a record's extent becomes slack "whether a
commit drops the record or supersedes it"). All read correctly under the widened
licence. I also checked the mechanics of a drop-only commit against `[R-LIF-02]`: step 2
appends nothing, steps 3 and 5 append the directory, pad and trailer, F rises by at
least 128 by §9.2's second Note (whose derivation — prior F + 4 + 64 = +68, rounded up
to a multiple of 64 = +128 — I re-derived and confirmed), and dropping the file's only
record leaves an empty directory, which `[R-CNT-14]` says is a conforming generation.
Nothing breaks.

### 7.3 The two-mechanism carve-out in §20.3 step 4

"a change that leaves every one of those tiles' stored bytes meaning exactly what they
meant — a filter whose mandated stride makes it the identity (`[R-COD-10]`), or a new
padding position whose stored byte already holds the fill `[R-SER-05]` fixes — is not
what this bars."

I checked the filter half against `[R-COD-10]` and Appendix G item 5. `[R-COD-10]` gives
the identity at s = 1 (a packed bool plane, and equally any layer whose relevant stride
is 1). Appendix G item 5 names a *second* identity case that the carve-out's phrasing
does not obviously reach — "where the decoded image is a single group, n = L/s being 1"
— and a third case, a tile whose decoded image happens to be a fixed point of the
permutation. I do not report these, because §20.3 states in the same sentence that
"the list names where that effect arises rather than standing on its own" and that the
governing test is the general one, which covers all three. The list is expressly
illustrative, so a narrower list is not a narrower rule.

I checked the padding half against the shrink paragraph and the growth permission, and
against §11.1's Rationale and §23.1, and the three agree: a new padding position whose
stored byte already holds fill is inside the carve-out; a *grown* position that ceases
to be padding is not, and is instead an exception the growth permission states in its
own right, which §20.3 says in as many words.

I then stress-tested the two bars with the "what may one commit do at once" question.
For a **pure growth**, every Gᵢ is non-decreasing, so N unchanged implies every Gᵢ
unchanged or N = 0 throughout — which is exactly the two cases §11.1's Rationale names,
and means a growth that leaves entry_count unchanged really does leave every disk
ordinal and every index entry unchanged. For a **mixed** grow-and-shrink, entry_count
can hold still while ordinals move (G = (2,3) → (3,2) leaves N = 6 but re-maps
s = 3t₀ + t₁ to s = 2t₀ + t₁); §20.3's re-emission trigger is "stored-tile set **or
index content**", not entry_count, so it fires correctly, and its renumbering
parenthetical is licensed for "a geometry change", which this is. The planar
channel-ordinal bar exists precisely because a *channel* reorder would renumber without
a geometry change, leaving the re-emission rule with no stated occasion — and §20.3
says so explicitly. This is the tightest reasoning in the document and I could not
break it.

### 7.4 §18.2's replacement of `[R-COD-06]`'s frame rules

Two exceptions are named (the tile-decoded-size comparison and the declared
`Window_Size`), and both are replaced below. I checked what is carried over against
`[R-COD-06]`'s actual text: frame magic, no skippable and no second frame, no
dictionary use disclosed or not, no nonzero dictionary ID, no content-checksum flag, no
buffer sized from a declared length, and — from `[R-COD-08]` via "occupying the extent's
bytes before its terminal CRC" — no trailing bytes. R4's sixteen instances enumerate
exactly the eight checkable ones across two containers, and §18.2 accounts for the two
that fall outside the register on §21.7's two distinct grounds. The single-segment
corner is handled: RFC 8878 makes a single-segment frame's Window_Size its content size,
which §18.2 pins to the decoded document's length, so a >8 MiB document framed that way
exceeds §21.9's Window_Size row even while staying inside the 16 MiB document row — and
§18.2 says that in terms, with the writer's remedy (use a Window_Descriptor). I could
not find a gap.

---

## 8. Findings

### reader-01 — AMBIGUITY

**Location:** §2.3, `[R-CNF-03]`; read against §21.6's closing paragraph and §7.4
`[R-CNT-18]`.

**Quotation** (§2.3, `[R-CNF-03]`):

> A reader MUST accept every conforming file of a format major version it implements,
> carrying no record of a type it does not implement with MUST_UNDERSTAND = 1 — in a
> conforming file such a type is necessarily from the experimental range, since a
> reserved-range type carrying MU = 1 is itself a violation — and none of whose values
> exceeds the minimum guarantees of §21's limits table

**The problem.** The exemption from the acceptance duty is stated over "record", with
no scope qualifier. §7.2 frames sub-records as records and §7.4 calls them records, and
`[R-CNF-03]`'s own parenthetical confirms the clause ranges over both scopes: it argues
that in a conforming file such a type is necessarily experimental "since a
reserved-range type carrying MU = 1 is itself a violation", and that is true at both
scopes (F35 top-level, L24 sub-record). So a conforming file whose only unimplemented
MU = 1 record is a *layer sub-record* falls, on the literal text, outside the
acceptance duty entirely.

§21.6's closing paragraph says the opposite about that file, and calls the distinction
load-bearing:

> The qualifier is load-bearing — the same type as a layer sub-record is reject-layer
> and never a ground to refuse the file (`[R-CNT-18]`), so only the top-level case is a
> file a reader refuses

and `[R-CNT-18]` states it as a prohibition:

> an unknown sub-record type with MU = 1 is reject-layer, and where the file is
> otherwise conforming a reader MUST NOT reject the file for it

**Permitted readings.** (a) `[R-CNF-03]`'s clause means what it says, and I owe no
acceptance duty for such a file; `[R-CNT-18]` still bars me from *rejecting* it, so I
must open it, but nothing obliges me to serve its undamaged layers, and I may decline
them one by one. (b) `[R-CNF-03]`'s clause is meant to carry §21.6's top-level
qualifier, so the duty runs and I must serve every layer but the one carrying the
sub-record.

**Which I picked and why.** (b). §21.6 calls the qualifier load-bearing and
`[R-CNT-18]` supplies an unconditional MUST NOT for the file-level move, which settles
the only question that could produce a visible accept/reject divergence. Reading (a)
would leave a conforming reader free to open a conforming file and serve nothing from
it, which no other sentence in the document contemplates and which §21.6's "never a
ground to refuse the file" plainly means to exclude.

**What an implementer does wrong without it.** Builds a reader that treats an
experimental MU = 1 *sub-record* the way it treats an experimental MU = 1 *top-level*
record — refusing the file — because `[R-CNF-03]` is the rule that tells a reader what
it must accept, and `[R-CNF-03]`'s exemption reads as covering both. The cross-reference
that would correct this ("§21.6's closing paragraph names the other two") is attached in
§2.3 to the *refusal grounds*, not to the acceptance-duty exemption, so a reader working
from `[R-CNF-03]` outward does not necessarily follow it.

**Byte-level: no.** Two implementations reading only `[R-CNF-03]` would differ on
whether to reject such a file, but `[R-CNT-18]`'s "a reader MUST NOT reject the file for
it" and §21.6's "never a ground to refuse the file" are unconditional and decide the
verdict against the permissive reading. The residue — whether a reader that opens the
file owes service on its *other* layers — is a behavioural gap rather than an
accept/reject fork on a byte sequence, and no register row records it. I flag it as an
AMBIGUITY in `[R-CNF-03]`'s wording, not as a fork.

**Does the document already know the question?** It knows the top-level/sub-record
distinction and says it is load-bearing. It does not appear to know that
`[R-CNF-03]`'s own exemption omits the qualifier that makes it so.

---

## 9. Suspicions I opened and closed

- **`[R-COD-11]`'s cannot-establish ground looked unreachable.** A conforming verifier
  is a conforming reader (§2.3) and therefore implements all four codecs and both
  filters, so it can never fail to execute an *assigned* one; at a reserved or
  experimental value the layer is already a violation (L43/L45) and §2.3's "An
  established violation takes priority" fixes the verdict as *nonconforming*, not
  *cannot establish*. Closed by §17.4's own sentence — "For a conforming reader that
  position arises only at a reserved or experimental value, every assigned codec and
  filter being core: it rejects the layer" — and by §18.2, which uses `[R-COD-11]` as
  the *model* for the metadata-encoding decline, which is reachable. Not dead text.

- **§5.2's partial slack total looked as though it could under-count.** "A partial
  total is F less the bytes claimed by the claimants the walk did enumerate — an upper
  bound on the file's true slack, never an under-count." If claimants overlap (F33,
  L18) and one summed their lengths, the total would be an under-count. Closed by the
  wording itself — "the bytes claimed by", the union, not the sum — reinforced by the
  "never an under-count" clause and by the explicit rule that a rejected layer's
  already-enumerated claimants are discarded with the layer.

- **§23.1's enumeration of unreachability-producing operations omits the removal of a
  planar channel**, which §20.3 says de-addresses N tiles and turns their extents into
  slack, and which §20.3 says expressly "is not one" (a shrink). Closed by §23.1's own
  sentence "the list of operations above is not offered as closed", and by its
  two-case classification, which a channel removal satisfies (the structure carrying
  the bytes leaves the live state).

- **§20.2's creation procedure never states flags = 0**, although §20.3 step 6 and
  §20.5 both state the flags rule for their tiers. Closed as not a defect: §6.3 states
  the creator's rule, §20.2 does not purport to be exhaustive (it gives an explicit
  partial list of content obligations), and a violation is expressly not a
  file-conformance violation (§2.3), so nothing about the bytes turns on it.

- **§20.3 step 4's re-emission clause does not name de-addressed entries**, listing only
  tiles stored/superseded, tiles becoming unstored, entries new to this generation, and
  every other entry. Closed: the region is re-emitted with entry_count entries, and the
  shrink paragraph states that `[R-CNT-17]` obliges the smaller entry_count and a
  re-emitted region, so a de-addressed tile simply has no entry.

- **`[R-SER-08]` permits two readers to disagree** on a nonconforming interleaved bool
  byte — one rejects the tile under `[R-CNF-12]`, one returns true. Closed: both are
  expressly licensed, the Rationale claims only that they will not disagree about the
  *sample value*, and §21.1 and Appendix H both restate the resolved-byte rule
  identically.

- **T2's scope to "a real (non-padding) sample position"** looked as if it could leave a
  padding bool byte outside every row. Closed by deriving the coverage: a bool fill is
  constrained to 0x00/0x01 by `[R-TYP-07]`, so any other byte at a padding position
  necessarily differs from the fill and fires T4. T2 ∪ T4 covers `[R-SER-08]`
  exhaustively, exactly as T2's own text claims.

- **§16.2's "MAY instead detect contiguity arithmetically from any index segment"**
  cannot be right for a run spanning a segment boundary (S may exceed 2¹⁶). Closed as
  non-normative in effect: it is a MAY describing an optional reader convenience, the
  obligation being the verifier's.

- **Whether the §14 bar can be a property of bytes at all**, given `[R-CNF-02]`'s "pure
  predicate on bytes". Closed: `[R-LIF-01]` freezes the superseded generation's
  directory and trailer in the file as slack, so §9.6's backward probe can in principle
  witness the prior declarations; the condition is a property of the bytes and is
  merely *unwitnessed* in §21.7's precise sense, because no check the document obliges
  performs that probe. Consistent.

- **§2.3's "cannot establish" ground for an unimplemented MU = 1 type** omits the
  top-level qualifier too. Closed as correct: at *both* scopes such a record leaves a
  verifier unable to establish something, so the unqualified statement is the right one
  there. Only `[R-CNF-03]`'s acceptance clause is wrong to omit it — that is
  reader-01.

---

## 10. Confidence

High that the open path, the validation tiers, layer access, the tile-read algorithm,
the index chain, the decoded byte layouts and the seven degradation walks are fully
determined by this document: I implemented all of them on paper and executed the
critical ones against a file I built from the document alone, and every stated constant,
offset, formula and checksum I could check was correct.

I found one wording defect and no byte-level fork. I looked for a fork specifically in
the three decided rules — I diffed the flags prohibition across all five of its
statements word for word, traced the drop licence to every sentence that could have
assumed the old gate, and stress-tested the two-mechanism carve-out against the growth
permission, the shrink paragraph, §11.1's Rationale and §23.1 — and each held. The
document's most-repaired step, §20.3 step 4, is now internally consistent under the
"what can one commit do at once" test, including the mixed grow-and-shrink case that
holds entry_count still while moving disk ordinals.
