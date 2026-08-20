# Cleanroom round 14 — Adversary transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in full (4,168 lines, in five `Read` calls). I opened no other file in the
repository — no `docs/`, no ADRs, no `PLAN.md`, no `AGENTS.md`, no
`conformance/`, no `spec/registry.json`, no `README.md`. I ran no `git`
command of any kind, no web search, no web fetch, and I did not list any
directory to discover what else exists.

I ran two kinds of local computation, both reading only files I wrote
myself in my own scratch directory:

- `grep`/`awk`/`sed` and a small Python script over `spec/tarn.md` itself,
  to count register rows and instances and to scan for normative keywords
  inside Note/Example/Rationale blocks.
- Python, in `…/scratchpad/work/`: a CRC-32C implementation, three TARN
  file builders, and an independent verifier written from the specification
  text alone. These produced and consumed only `.tarn` files I generated
  (`probe.tarn`, `flat.tarn`, and mutant families `a01`–`a14`, `b01`–`b16`,
  `c01`–`c09`, `d01`–`d05`, `e01`–`e10`).

I did not read the round-14 output directory and did not list it. I wrote
only this one file into it.

I used prior knowledge of RFC 1951, RFC 8878 and the LZ4 block format to
*generate* suspicions about codec edges. Every suspicion was then settled
against this document's own text, never against that outside knowledge, and
I say so explicitly wherever it arises below.

---

## 1. Method

The brief pointed at seventeen sections carrying the previous round's
repairs. I did not walk them in order — a section-by-section narration that
finds nothing is worth little. Instead I did four things:

1. **Verified every constant and every worked example** the document states,
   by computation. This is the cheapest possible test of whether the text is
   self-consistent at the level where bytes actually live.
2. **Counted the register mechanically** against §21.1's own stated instance
   criterion — the criterion being the single most recently repaired passage
   in the document, and the one whose correctness is checkable by machine.
3. **Built files end to end** and wrote an independent verifier from the text
   alone, then ran 54 hand-built mutants through it, aiming at every boundary
   the charter names.
4. **Swept the "unconstrained" surface** — every place the document declares
   something unconstrained — asking in each case whether a verifier might
   nonetheless check it.

Findings are at the end. The bulk of this transcript is attacks that
*failed*, because the charter asks for those explicitly and because a round
that reports only its two hits hides most of its evidence.

---

## 2. Arithmetic and constants — all verified

I implemented CRC-32C from §4.5's parameters (Castagnoli 0x1EDC6F41,
reflected in and out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and checked it
against §4.5's own check vector before using it for anything.

| Claim | Section | Computed | Verdict |
|---|---|---|---|
| CRC-32C(`"123456789"`) = `0xE3069283` | §4.5 | `0xe3069283` | ✓ |
| CRC-32C(zero bytes) = `0x00000000` | §4.5 | `0x0` | ✓ |
| CRC of 4 sentinel entries (80 bytes) = `0x80A34955` | §7.4 example | `0x80a34955` | ✓ |
| crc_of_crc_array over that = `0xC4EE982E` | §7.4 example | `0xc4ee982e` | ✓ |
| CRC of a full 2¹⁶-sentinel segment = `0xEECB3BB2` | §15.4, App. B | `0xeecb3bb2` | ✓ |
| Appendix A trailer CRC = `0xE00938D2` | App. A | `0xe00938d2` | ✓ |

I then parsed Appendix A's hex dump field by field. Every annotation in its
table matches the bytes: magic, version 1.0, flags 0, generation 1,
dir_offset 16, dir_length 4, committed_file_length 128, file_id
`0x0123456789ABCDEF`, reserved zero. The directory region at [16,20) is the
CRC of zero bytes, `00 00 00 00`. The file is 128 bytes and 128 mod 64 = 0.
Appendix A is byte-exact.

I re-derived every worked example:

- **§7.4's layer-record payload.** Name 4 + nine scalars 34 + one dimension
  entry 18 + one channel entry 12 + trailing fixed 13 = 81, matching the
  stated `inline_length = 81` with no residue, so the sub-record sequence is
  empty. The extent length 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84 matches.
- **§11.2/§11.4.** G = (4,8), N = 32, P = 65,536. Coordinate (300,700) → tile
  (1,2) → s = 10; in-tile (44,188) → ordinal 44·256+188 = 11,452. Planar
  channel 2 → 2·32+10 = 74. All correct.
- **§14.2.** Interleaved (2,3), channels uint8+uint16: Q = 3, size 18,
  ordinal 5 at [15,18). Planar `b` 12 bytes, ordinal 5 at [10,12).
  float32+bool: Q = 5, size 30, ordinal 5 at [25,30). All correct.
- **§14.3.** P = 10, alternating true/false from ordinal 0: byte 0 =
  0b01010101 = `0x55`; byte 1 low two bits = `0x01`; with fill true the pad
  bits 2–7 set gives `0xFD`. Correct.
- **§14.5.** Extents (5,5), tiles (4,4): edge tile (1,1) has one real
  position and 15 padding; 32 bytes with values 1–15 each `CD AB`. Correct.
- **§15.4.** entry_count 1,000,000 → 16 segments (15 full + 16,960),
  64-byte CRC array, region 20,000,064 bytes; tile 999,999 at
  segment-relative byte 339,180; segment 15 at [19,660,800, 20,000,000);
  one full segment = 65,536 × 20 = 1,310,720 = 1.25 MiB. All correct.
- **§17.3.** I applied the shuffle transform `byte i of group j → i·n + j`
  to `00 00 80 3F 00 00 00 40 00 00 40 40` with s = 4, n = 3 and got
  `00 00 00 00 00 00 80 00 40 3F 40 40`, exactly the stated result.
- **§21.9's note.** 2³² entries / 2¹⁶ per segment × 4 bytes = 256 KiB; at
  2³⁶ it is 4 MiB. Both correct.

I found no arithmetic error anywhere in the document. That is a real result
and it is unusual.

---

## 3. The register, counted by machine

§21.8 asserts "121 conditions over 268 instances". I extracted every row of
§21.2–§21.5 by regex and applied §21.1's stated counting rule — "Instances
within a cell are separated by semicolons, and a cell reading — is one
instance; the count is therefore mechanical once the cell is written."

```
F rows: 36 instances: 56
L rows: 49 instances: 111
T rows: 26 instances: 57
R rows: 10 instances: 44
TOTAL rows 121  TOTAL instances 268
```

Row counts also match each subsection's own header (36 / 49 / 26 / 10). So
the *stated total* is consistent with the cells *as written*.

That is not the same as the cells being right. §21.1 states a mechanical
criterion for what a cell must contain, and the last commit visible in the
document's own structure is a repair to that criterion. So I tested the
criterion against every row rather than trusting the total. That produced
finding **adversary-01**; see §7.

I also confirmed several consistency properties the register gets *right*,
because they are the kind of thing that usually breaks:

- **The layout axis is applied at three values** wherever a derived quantity
  varies by layout (interleaved P·Q; planar numeric P·Bᶜ; packed planar bool
  ⌈P/8⌉) — T21, T26, L44 give 3; T3, T14, T22 give 3 × 2 directions = 6.
- **L21 correctly gives two, not three**, because the addressed-tile count
  (N interleaved, C·N planar) does not depend on bool packing.
- **L36 gives two, not three**, because §10.2 gives the channel-layout space
  no experimental range. Every other value-set row (L31, L33, L34, L43, L45)
  gives three or four, matching its space's partition exactly.
- **F2 omits `file_id`** from the u64-domain instances. That is correct:
  `[R-ENC-03]` binds "every offset, length, extent, and count", and a file
  identifier is none of those. Getting this right requires noticing that a
  u64 field can be outside the value domain rule.
- **L1 omits A and A_slab**, because L39 and L29 already give them narrower
  range rows. No double-registration.
- **F7 gives four instances and F33 five** — the difference being the
  directory region, which can be an overlap participant but cannot lie in
  its own trailing gap. That asymmetry is correct.
- **F33's closing clause** — "a claimant reaching the front signature block
  or the live trailer is instead caught by the bounds rows F9/F10, F31/F32,
  L16/L17 and T8/T9" — I checked exhaustively. The claimant kinds are the
  directory (F9/F10), top-level record extents (F31/F32), layer-record and
  sub-record extents including the tile-index region (L16/L17), and stored
  tiles (T8/T9). The enumeration is complete.

---

## 4. Building a file end to end

I wrote a builder and an independent verifier, both from the text alone.

### 4.1 `probe.tarn` — 576 bytes, one layer, slab, metadata, ancillary

Layer `sst`: interleaved, rank 2, dims y(E=3,T=2) and x(E=3,T=2) so
G = (2,2), N = 4, P = 4; channels `a` uint8 fill `0x07` and `b` bool fill
`0x01`, so Q = 2 and the decoded tile image is 8 bytes; codec 1, filter 1;
slab S = 2 with A_slab = 64; plus a file-scope user-metadata record
(encoding 1, document `{"tarn.creator":"round14","tarn.title":"probe"}`,
keys in ascending UTF-8 byte order per `[R-MTA-05]`) and an ancillary record
of experimental type 0x8001 with MU = 0, PE = 0 and a 4-byte extent.

The four decoded tile images, with §14.5's fill-encoded padding:

```
tile 0  00 00 01 01 0a 01 0b 00     (all four positions real)
tile 1  02 00 07 01 0c 01 07 01     (x = 3 padding → a=07 b=01)
tile 2  14 00 15 01 07 01 07 01     (y = 3 padding)
tile 3  16 00 07 01 07 01 07 01     (only (2,2) real)
```

Placement with S = 2, A_slab = 64: run 0 = ordinals [0,2), run 1 = [2,4).
Each run's first stored tile must satisfy `offset mod 64 = 0`, so tiles land
at 64, 72, 128, 136. Index region at 144, length 4 × 20 + 4 = 84 (matching
`[R-CNT-17]`). Metadata extent at 228, ancillary at 278, directory at
[283, 459), pad [459, 512), trailer [512, 576). Claimed 427 bytes,
slack 149.

My verifier certifies it: `CONFORMING; layers=['sst'] slack=149`.

### 4.2 Where I had to guess while building

Almost nowhere, which is the point of reporting it. The places I paused:

- **`[R-SLB-03]`'s packing relation** reads "each stored tile's offset equals
  the previous stored tile's offset plus **its** length". "its" could in
  principle attach to either tile. It attaches to "the previous stored
  tile", the nearest antecedent, and L41 disambiguates in the register by
  saying "the previous stored tile's offset plus **that** tile's length" —
  "that tile" being a deliberate pointer back at the previous one. I checked
  whether the wrong reading (`offset_k = offset_{k−1} + len_k`) could fork a
  verdict: it can, whenever two consecutive stored tiles differ in length.
  But the register row is *clearer* than the rule here, not in conflict with
  it, so there is nothing to resolve. **No finding.**
- **The registry-fixed flag values.** §7.3 fixes layer = MU 1/PE 1 and user
  metadata = MU 0/PE 1, and `[R-CNT-22]` makes a stored mismatch a verifier
  violation. I emitted `flags = 0b11` and `0b10`. Unambiguous.
- **The ancillary record's flags.** MU = 0, PE = 0, flags = 0. §10.3 forbids
  publishing experimental values *as conduct*, and §21.6 makes the file
  conforming. Explicit.
- **What checksum covers the ancillary's extent.** §8.1's last row: none,
  the bytes are opaque. Explicit, and confirmed by §22.3.

That is the whole list. Nothing about the container or the array model
required me to invent behaviour.

### 4.3 `flat.tarn` — the padding-free control

Because `probe.tarn` has padding positions in three of its four tiles, some
mutations trip §14.5's padding check before reaching the structural check I
wanted to exercise. I built a second file with E = (4,4), T = (2,2) — grid
2 × 2, no padding positions anywhere, one uint8 channel, no slab — so that
tile images are interchangeable and pure overlap/coverage attacks are
isolable. 384 bytes; certifies.

---

## 5. The attack battery

54 mutants. Every one landed on the register row the document predicts.

### 5.1 Value sets (`a01`–`a14`) — all reject at layer scope

layout 0 / 3 / 255 → L36; linearization 0 / ≥0x8000 → L33; codec 0 / 5 →
L43; filter 0 → L45; A ≠ 0 with S ≠ 0 → L20; A_slab 0 / 3 / 2⁶³ with S ≠ 0 →
L29; rank 0 → L32; channel count 0 → L32.

Note `a03` and `a12`: layout 255 is the top of a `u8` space with *no*
experimental range (§10.2), and A_slab = 2⁶³ is a power of two that lies
outside the value domain. Both are correctly rejected, and both required me
to read §10.2's "Two spaces carry no experimental range" and `[R-ENC-03]`'s
domain rather than the field's own table cell.

### 5.2 Index entries (`b04`–`b11`) — all reject at tile scope

offset + length one past F − 64 → T9; offset 15 → T8; length 0 → T10;
sentinel with crc ≠ 0 → T6; half-sentinel → T7; bit 63 set → T11; codec 1
length mismatch → T14; stored bytes failing crc → T1.

Boundary confirmed: an extent ending *exactly* at F − 64 is legal by §15.3
("offset + length > F − 64" is the error), by §7.2 ("extending past F − 64"),
and by §9.7's half-open "[16, F − 64)". Three statements of the same bound in
three sections, and they coincide exactly. I checked the same for the ≥ 16
floor: §6.2, §7.2, §15.3 and §9.7 all agree.

### 5.3 Coverage and overlap (`d01`–`d04`)

- Tile 3 aliased onto tile 2's extent (same layer) → intra-layer overlap →
  **reject-layer** (L18), per `[R-CNT-13]` and §15.3's row.
- Tile 3 pointed at the directory region → **reject-file** (F33).
- Tile 3 pointed at its own layer's index region → §15.3 says intra-layer,
  **reject-layer** (L18). My verifier reported it through the shared overlap
  path; the scope distinction is stated and unambiguous.
- Tile 3 placed between the directory's end and the trailer → **F7**,
  reject-file, per `[R-CNT-05]`. Note this is reject-*file* even though the
  damage is confined to one tile: `[R-CNT-05]` says "a validity error at
  file scope" and there is no competing text. Determinate.

Deduplication attack: two entries in *different* layers pointing at the same
byte range is exactly the optimisation an implementer might reach for. §7.2
forecloses it — "Extents are owned exactly once" — and F33 registers it as
reject-file. No ambiguity.

### 5.4 Decoded content (`c04`–`c06`)

The interesting structural fact I learned by building these: **to exercise
T2 or T4 at all you must recompute the entry's crc.** Flipping a padding
byte in place is caught as T1 (crc mismatch) at step 5 of §19.4, before any
decode. Only a *writer* that computes the checksum over its own wrong bytes
produces a T2/T4 witness. That is precisely §21.7's claim — "Checksums are
computed over what the writer wrote" — and the document is right about its
own detection model. With the crc recomputed:

- padding byte `0x07 → 0x09` on a uint8 channel → **T4**
- padding byte `0x01 → 0x00` on an interleaved bool channel → **T4**
  (not T2 — T2's own condition text excludes padding positions and hands
  them to T4, and the two rows together cover `[R-SER-08]`)
- real-position bool byte `0x01 → 0x02` → **T2**

The T2/T4 split is clean and I could not construct a byte that falls in
neither or both.

### 5.5 Slab invariants (`b12`, `c07`, `c09`)

- Gap inside run 0 → **L41**.
- Run 1's first stored tile off A_slab → **L42**.
- **`c09` is the one worth naming.** I turned ordinal 2 into a sentinel.
  §16.2: "Sentinel tiles are transparent to run continuity". So ordinal 3
  becomes run 1's *first stored tile*, and must therefore be A_slab-aligned
  — which it is not, because it was placed as run 1's *second* tile. The
  file goes from conforming to **L42** by a change that touches no offset.
  This is a real hazard for writers, and the document anticipates it exactly:
  `[R-SLB-04]` requires a commit that changes the stored-tile set to
  "re-establish the invariants for every such run — or clear the
  declaration", and its Note explains that this rule is what makes L41/L42
  reachable after a commit at all. Fully determinate. **No finding**, and a
  good piece of drafting.

### 5.6 Degenerate-but-legal files (`e01`–`e10`)

- **`e01`** — a layer with dimension extent 0: G = 0, N = 0, entry_count 0,
  extent slot (0,0), crc_of_crc_array 0. Certifies. §21.6 records it.
- **`e04`** — the extreme legal file. Rank 1, E = T = 2⁶³ − 1, one
  interleaved bool channel, entry_count 1, that one entry a sentinel. The
  layer declares a tile whose decoded size is 2⁶³ − 1 bytes. No product
  overflows (`[R-ENC-04]`), codec 1's length equality (`[R-COD-04]`) binds
  only non-sentinel entries, and nothing is stored. **A 192-byte file
  declaring a nine-exabyte tile certifies.** I checked hard for a rule that
  would catch it and there is none — nor should there be: §21.9's guarantees
  are floors, not caps, and a reader may decline on resource grounds under
  `[R-ERR-04]` while reporting it as a limit. The document is deliberate
  here and self-consistent.
- **`e05`** — a top-level record of experimental type 0x8000 with MU = 0 and
  no extent. Certifies, ignored. §21.6.
- **`e06`** — a user-metadata record at experimental encoding 0x80.
  Certifies, and the verifier emits the report line `[R-MTA-10]` demands
  (owning scope, encoding value, stored extent length). The round-13
  metadata-encoding repair holds under construction.
- **`e07`/`e08`** — encodings 3 (reserved) and 0. §21.5's preamble
  ("Encoding 0 and a reserved-range value are unassigned too, and R1
  registers both as violations: what `[R-MTA-10]` withdraws is the
  document's content rules, never the encoding byte's own value set")
  settles these against R1 → nonconforming. My verifier was lax and only
  noted them; the *specification* is not lax. The three-way split
  (0/reserved = violation, experimental = conforming, 1/2 = assigned) is
  stated in five places and I could not make them disagree.
- **`e10`** — user-metadata extent_length exactly 5, the §7.1 floor. The
  structure is legal; the 1-byte document then fails §18.2's JSON rules and
  is R7, ignore-record but still a violation. The floor is placed exactly
  where a 1-byte document plus a 4-byte CRC needs it. Correct.

### 5.7 The pre-trailer gap (`d05`) — the repair holds

I built a file whose pre-trailer gap is 98 bytes where `[R-LIF-02]` step 5
would have produced 34. §6.2: "a longer gap is conforming, and no conforming
commit produces one." §2.3's `[R-CNF-02]` names this as one of exactly two
conduct-rule cases. My verifier certifies it, which is what the text
requires.

I then tried to break the conduct-rule enumeration. §2.3 says "§6.3's
flags = 0 against a set ignore-lane bit and §6.2's pre-trailer gap longer
than `[R-LIF-02]` step 5's pad are the cases this text states". I looked for
a third: a writer MUST/MUST NOT whose violation the document expressly
declares not to be a file-conformance violation. The candidate is
`[R-MTA-06]` — "writers MUST NOT emit a `tarn.`-prefixed key this
specification's registry does not define at the version they target … A file
carrying an unrecognized `tarn.` key is **conforming**." That looks like a
third case. It is not: §2.3's *first* category already covers it by name —
"which registry version a writer targets (§10.3, **§18.3**)". §18.3 is
`[R-MTA-06]`'s own section. The enumeration is complete. **No finding.**

---

## 6. Attacks that the text forecloses

Recorded because the charter asks for them by name, with the sentence that
closes each.

**A. The metadata-encoding layout table.** §18.2's table cell reads
`| encoding | structural | 1 or 2; see below |`, which taken alone would
make an experimental-range encoding an out-of-range structural field and so
nonconforming — contradicting §21.6, `[R-MTA-10]`, §17.4 and Appendix H,
which all say such a file is conforming. **Closed by the words "see
below"**: the cell explicitly defers to the prose two lines down, which
partitions the space into assigned / invalid / reserved / experimental with
different consequences. This is the closest I came to a certify-versus-reject
fork, and the two-word deferral is what closes it.

**B. Zero-extent layer under codec 4.** `[R-COD-07]` quantifies over "a layer
any of whose *addressed* tiles' decoded size exceeds 0x7E000000". A layer
with a zero extent addresses none, so the quantification is vacuous and the
declaration is legal however large its tile shape. A verifier reading the
cap as a property of the declared tile shape would reject. **Closed by the
word "addressed"**, which is empty-quantifier-explicit, and by L44's
identical phrasing. My `e02` certifies. (§17.2's Note says the same thing,
but the Note is non-normative and is not what closes it.)

**C. Is P checked in a layer with no addressed tiles?** A layer with E = 0
and tile extents whose product overflows 2⁶³ − 1. A reader that
short-circuits on N = 0 would certify what another rejects. **Closed by
`[R-ENC-04]` itself**, which binds "any quantity this specification defines
as a sum or product of integers obtained from a file … sample-position
counts", unconditionally, and by `[R-GEO-03]`'s "These products, like all
geometry arithmetic, are subject to `[R-ENC-04]`". L2 lists `P = ∏Tᵢ` as an
instance. The resolution is normative, not merely noted.

**D. DEFLATE's unused final-byte bits.** A raw RFC 1951 stream ends on a bit
boundary, leaving up to seven bits in the last byte that RFC 1951 does not
fix. A verifier could argue those bits are "past the stream" and reject under
`[R-COD-08]`. **Closed by the word "bytes"**: `[R-COD-08]` says "no trailing
**bytes** past the stream, frame, or block", and T24's condition says
"**bytes** remain in the stored extent after the stream … ends". A partial
byte is not a byte. Two files differing only in those bits are both
conforming and Appendix G item 1 closes the reproducibility gap by pinning
the encoder. (I used outside knowledge of RFC 1951 to *find* this; the
resolution is entirely from this document.)

**E. zstd window on a sub-1-KiB tile.** `[R-COD-06]` bars a declared window
exceeding the decoded size; the smallest window a Window_Descriptor can
express is 1 KiB. So a tile of decoded size 18 or 30 bytes (§14.2's
examples) or 2 bytes (§14.3's) is encodable under codec 3 only as a
single-segment frame. **Closed by §17.2's Note**, which reaches the same
conclusion — and, more importantly, by `[R-COD-06]`'s own text, under which
both RFC 8878 derivations of Window_Size agree for a conforming tile
(single-segment ⇒ Window_Size = FCS = decoded size, which the rule already
pins). No conforming file turns on which derivation a reader implements.

**F. Ignoring an unknown record vs. validating its extent slot.** A top-level
record of an unknown MU = 0 type is "skipped as though absent" (§2.4), yet
`[R-CNT-13]` makes its malformed extent slot a file-scope validity error
(F30–F32). Reader A rejects the file; reader B skips the record entirely.
**Closed by §19.1 step 4**, which names "the extent-slot validity rules for
**non-layer top-level records** (`[R-CNT-13]`)" as an obligation of the open
walk. Unknown types are non-layer top-level records. Both verifiers report
nonconforming.

**G. Ill-formed layer names and duplicate detection.** Two layer records with
byte-identical but ill-formed name fields: does F4 (reject-file) or L3
(reject-layer, twice) govern? **Closed by §19.1 step 4**: "Uniqueness is
decided first, and over the raw name bytes whether or not each name is
itself well-formed". And a layer record whose name field does not fit its
`inline_length` "contributes no name to the namespace" and is instead L23.
Both edges are stated; neither needed guessing.

**H. Zero-length structures.** The charter names this. There are none
possible: dir_length ≥ 4, trailer 64, front block 16, a stored tile of
length 0 is T10, and a record extent of (0,0) is "no extent" and not a
claimant at all. So §9.7's disjointness walk never has to decide whether two
empty ranges at the same offset overlap. Closed by construction.

**I. Verifier resource limits.** Verifier A with a 256 MiB tile budget
declines a 512 MiB tile; verifier B does not. They report different things —
but *cannot establish* versus *conforming*, not certify versus reject.
`[R-CNF-11]`: "*Cannot establish* is not a finding that the file is
nonconforming". By design, and the same shape covers `[R-MTA-09]`'s document
bound and `[R-COD-11]`'s unexecutable codec. Not a fork within the charter's
meaning.

**J. `[R-CNF-07]`'s "reader outcome" on verifier-detected rows.** §2.4
assigns every violation a *reader* outcome, yet rows like F25, F27, F28, L46
and T4 oblige no reader to reject anything. **Closed by §21.1**: "For a row
whose Detector is *verifier*, the outcome names the scope at which the damage
is recorded, not an obligation on any reader … for several such rows it
obliges the reader to serve the structure unchanged". Explicitly reconciled.

**K. §16.2 omits A_slab's upper bound**, giving only "a power of two ≥ 1"
where §7.4, L29 and Appendix B all say ≤ 2⁶². Inert: `[R-ENC-03]` caps the
field at 2⁶³ − 1, and the largest power of two below that is 2⁶². The two
statements cannot disagree on any value. Not a defect.

**L. A file shorter than 64 bytes.** §19.1 step 2 says "Fetch bytes
[F − 64, F)", which is undefined for F < 64, and §19.1 never names
`[R-CNT-27]`. **Closed by §19's preamble**: "Those enumerations are not the
complete inventory of what a reader detects at that tier: §21's register
is" — and F5 is registered at detection point *open*. Every path reaches
reject-file anyway.

**M. Normative force stranded in a Note.** I scanned every Note, Example and
Rationale block for MUST/SHALL/SHOULD/MAY. Five hits, all of them restating
a rule that is stated normatively elsewhere and cited in place
(`[R-LIF-05]`, `[R-LIF-03]`, and two bare permissions). The one SHOULD that
exists *only* in a Note — §20.3's "Writers doing many small updates SHOULD
batch them into one commit" — carries no conformance consequence, since
`[R-CNF-12]` puts SHOULD deviation outside the register entirely. **No
repair from the previous round landed in a Note.** That was the failure mode
the brief flagged hardest and it did not occur.

**N. The slack partial-total arithmetic.** `[R-CNT-21]`: "A partial total is
F less the bytes claimed by the claimants the walk did enumerate — an upper
bound on the file's true slack, never an under-count". Checked: the
enumerated claimants are a subset of all claimants, so the un-enumerated
union is smaller, so F minus it is larger. The bound direction is correct,
and it "tightens to the exact total when the walk completes" as stated. The
interaction with §15.3's structural entries is also right — such an entry
contributes no claimant, so its nominal bytes really are slack in the *true*
total too, and §9.7 correctly says it "does not make the walk incomplete".

---

## 7. Findings

### adversary-01 — CONTRADICTION

**Location:** §21.1 (the instance criterion); §21.2 row F17; §21.3 rows L21,
L22, L30; §21.8's total. `[R-ERR-02]`, `[R-VEC-03]`.

**The text complained about**, §21.1:

> Where the condition compares two quantities and either can be the greater
> — a *differs from* or *does not equal* — the two directions are likewise
> enumerated; where its own text bounds the comparison in one direction — an
> *exceeds*, a *larger than* — there is one. Instances within a cell are
> separated by semicolons, and a cell reading — is one instance; the count is
> therefore mechanical once the cell is written.

Four rows use the exact trigger phrases this criterion names, compare two
quantities either of which can be the greater, and do not enumerate the two
directions:

> | L30 | A channel entry's fill length prefix **differs from** the element size of the channel's declared type | — | reader | layer access | `[R-CNT-23]` (R-TYP-06) |

One instance. Both directions are concretely constructible and
distinguishable: a `float32` channel (element size 4) whose fill length
prefix is 1, and an `int8` channel (element size 1) whose fill length prefix
is 4. Compare T14, which uses the *identical* phrase — "a non-sentinel index
entry's length **differs from** the tile's decoded size" — and enumerates
"length longer; length shorter" for each of its three layout formulas.

> | F17 | Trailer committed_file_length **does not equal** the transport-authoritative file size (physical file not truncated or extended to it) | committed_file_length | reader | open | `[R-CNT-06]` (R-LIF-04, R-CNT-10) |

One instance, although the condition's own parenthetical names both
alternatives — "not truncated **or** extended" — and §21.1 also counts "one
of several alternatives the condition text states" as an instance. The two
directions are materially different files with different diagnoses: physical
length greater than committed is residue past a completed commit, which
§9.5's Note discusses in its own right; physical length less than committed
is a truncated file.

> | L21 | entry_count **does not equal** the geometry-derived addressed-tile count (N interleaved, C·N planar) | interleaved N; planar C·N | reader | layer access |

Two instances — the layout axis applied, the direction axis not. By the
criterion this is 2 × 2 = 4, exactly as T14 and T22 give 3 × 2 = 6.

> | L22 | Under index_encoding 1, extent_length **≠** entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 — including slot (0,0) with entry_count > 0, or a nonzero slot with entry_count = 0 | extent_length against the formula; slot (0,0) with entry_count > 0; a nonzero slot with entry_count = 0 | … |

Three instances; the first ("extent_length against the formula") is a
does-not-equal comparison in which either side can be the greater, so by the
criterion it is two, giving four.

**Permitted readings.** (i) The criterion in §21.1 governs and these four
cells are under-enumerated by 1, 1, 2 and 1 respectively — total 273, not
268, with five corpus files owed that are not currently owed. (ii) The cells
govern and the criterion is narrower than its wording — perhaps intended to
apply only where the compared quantity also varies by layout, which is true
of T3, T14 and T22 and of no other row in the register.

**Which I picked, and why.** (i). §21.1 states the criterion as a general
rule about conditions ("Where the condition compares two quantities"), gives
the trigger phrases in italic as though quoting condition text, and
explicitly says the count "is therefore mechanical once the cell is
written". Reading (ii) would require the criterion to carry an unstated
layout precondition, which nothing in the text supplies — and L30's cell
would still be wrong under (ii)'s own logic, since T14 shows the same phrase
producing two directions. Note also that reading (ii) cannot be rescued by
§21.1's own tie-breaker "where a row and the rule it cites diverge, the rule
governs": that clause resolves a row's *Condition* against its governing
requirement, and the Instances column is not a restatement of any
requirement — it is the corpus build list, whose only authority is §21.1
itself.

**What an implementer does wrong without it.** A corpus builder working from
§21.1 mechanically builds 273 files; one working from the cells builds 268.
`[R-ERR-02]` makes coverage normative — "one vector per instance" — and
`[R-VEC-03]` repeats it, so the two builders disagree about whether the
corpus is complete, and §21.8's stated total certifies the smaller one. The
five missing vectors are the "too short" direction of a fill-length
mismatch, the "physical file extended past committed" direction of F17 (the
residue case §9.5 treats as its own phenomenon), and both under-count
directions of L21/L22.

**Byte-level: no.** Every file on either side of every one of these four
comparisons is rejected at the same scope, by the same rule, under both
readings. A `float32` channel with a 1-byte fill and one with a 4-byte fill
are both L30 / reject-layer. What changes is how many files a conforming
corpus owes, not which bytes a conforming implementation may emit or must
accept or reject.

---

### adversary-02 — OBSERVATION

**Location:** §20.3 `[R-WRT-04]` step 4; against §17.2 `[R-COD-07]` and
§21.3 row L44.

**The text complained about**, §20.3 step 4:

> A layer that stores no tile MAY be re-declared freely, which is what
> schema-first creation needs (§11.1); and an extent MAY always **grow**,
> since a position that becomes real held that channel's fill and fill is a
> legal sample value.

**The construction.** `e02_lz4_escape.tarn`: one layer, rank 1, dimension
`x` with extent 0 and tile extent 2³¹, one `uint8` channel, layout
interleaved, **codec 4 (lz4)**. G = ⌈0/2³¹⌉ = 0, so N = 0 and the layer
addresses no tiles; entry_count 0, extent slot (0,0). `[R-COD-07]`'s cap is
quantified over *addressed* tiles, so it is vacuous. My verifier certifies
this file, and correctly.

`e03_lz4_after_growth.tarn`: the same file after one commit that grows the
extent from 0 to 1 — the *only* change, with the single new index entry
written as a sentinel so that nothing is stored. Now the layer addresses one
tile whose decoded size is P · Q = 2³¹ = 2,147,483,648 > 0x7E000000 =
2,113,929,216. `[R-COD-07]`: "a reader MUST treat such a declaration as a
validity error at layer scope, checkable from declarations alone." My
verifier rejects it: **L44**.

So a commit that §20.3 says a writer "MAY always" perform turns a conforming
file into a nonconforming one, and it does so without storing a single byte
of tile data.

**Why this is decidable, and why it is still expensive.** `[R-COD-07]` is
unconditional and its reader clause is unconditional, and §20.4 makes a
modified record "new output under its writer obligations (`[R-CNF-05]`)", so
the grown layer record must satisfy every §7.4 constraint afresh. The
correct reading of §20.3's sentence is that the MAY is an exception carved
out of the *immediately preceding* prohibition — the one about altering what
§14 fixes for a tile the layer stores — and not a licence against the rest
of the document; the justification the sentence gives ("since a position that
becomes real held that channel's fill") is entirely about stored-tile
content, which signals that scope. The neighbouring clause "A layer that
stores no tile MAY be re-declared **freely**" carries the same implicit
scoping, and is over-broad in the same way (a re-declaration to codec 0 is
obviously not permitted).

The cost is that the only place the document flags this interaction is
§17.2's Note — "The escape is not durable: a later commit that grows an
extent addresses tiles, and the same declarations are then measured against
the cap" — and §2.1 makes Notes non-normative. A writer implementing §20
from §20 will not find it. Deciding the question requires holding
`[R-COD-07]`'s quantifier, §20.4's re-emission rule and §20.3's MAY together
across three parts of the document.

**Byte-level: no.** Both readings agree on both files. `e02` is conforming
under either; `e03` is nonconforming under either, because `[R-COD-07]`'s
reader clause is not in dispute. Resolving the wording changes what a
*careless* writer emits, not what a *conforming* implementation may emit or
must accept or reject — `[R-CNF-05]` already bars the bad output on the
strength of `[R-COD-07]` alone. This is a drafting hazard in repaired text,
not a fork.

---

## 8. Honest summary of what I could not determine

Nothing material. I did not execute a real DEFLATE, zstd or LZ4 encoder, so
the codec rows T15–T25 were reasoned about rather than built; but the
questions those rows raise (wrapper detection, frame counting, trailing
bytes, window size, frame content size) are all settled by `[R-COD-05]`
through `[R-COD-08]` in terms I could check against the external format
definitions I already know, and in every case the document's text was the
tighter of the two. I did not attempt a multi-generation file, since
`[R-LIF-01]`, `[R-LIF-03]`, `[R-WRT-04]` and `[R-WRT-05]` are all properties
of history that §9.7 explicitly does not reconstruct and §21.7 explicitly
omits from the register — a single-file adversary has no witness to build.

I could not construct a file that two conforming verifiers would judge
differently. The nearest miss is attack A (§18.2's table cell), and it is
closed by two words. On the evidence of this walk the document determines
its own byte-level questions.

**Findings in this transcript: 2.**
