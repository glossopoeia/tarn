# Round 27 — Reader implementer — working transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,549 lines; the brief said 4,550 — the file has 4,549 newline-terminated
lines, which is the same document off by one on how you count the tail). I
opened no other file, listed no directory, ran no `git` command, and did no
web access. The only other things I ran were `wc -l`, `grep`/`sed` against
that one file, and four local Python scripts I wrote myself, which read no
files except one 320-byte TARN file I generated in my own scratchpad. I wrote
this transcript and my scratch scripts into the scratchpad; I did not read the
output directory.

**Context I did not ask for.** My runtime placed material in context before I
began: a project instruction file pointing at an `AGENTS.md`, and an index of
the maintainer's memory notes with several titled entries. I did not read any
of the files it names and I have not used any of its contents as evidence.
Two entries' titles named topics adjacent to this document; I disregarded
them. I also note that the spec was exactly where the brief said it would be,
so no path carried information the brief withheld.

I generated suspicions from general knowledge of array/image container
formats (HDF5, Zarr, TIFF, PNG), but I settled every one of them against this
document's own text, and no conclusion below rests on outside knowledge.

---

## 1. Method

I read the document straight through once, then walked it a second time in the
order I would actually write a reader: transport → trailer → directory →
records → layer record → geometry → index → tile → decode → return. Every time
the text failed to hand me a value, an order, or a verdict, I stopped and wrote
it down. I checked every constant, offset and checksum I could compute, and I
built one non-trivial file from scratch to see whether the document determines
a complete artifact.

I did not treat the thirteen changed sections as suspects and the rest as
clean. Two of my three findings are in text the brief did not list.

---

## 2. Arithmetic and constant verification (done first, so later reasoning
rests on it)

I implemented CRC-32C from §4.5's parameters alone (Castagnoli 0x1EDC6F41,
reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF), verified it against
§4.5's own check vector, and then checked every stated checksum in the
document.

| Claim | Section | Computed | Verdict |
|---|---|---|---|
| CRC-32C(`"123456789"`) = 0xE3069283 | §4.5 | 0xE3069283 | ✅ |
| CRC-32C(zero bytes) = 0x00000000 | §4.5 | 0x00000000 | ✅ |
| CRC of a full 2¹⁶-sentinel segment = 0xEECB3BB2 | §15.4, App. B | 0xEECB3BB2 | ✅ |
| §7.4 example: CRC over four sentinel entries (80 bytes) = 0x80A34955, stored `55 49 A3 80` | §7.4 | 0x80A34955 | ✅ |
| §7.4 example: `crc_of_crc_array` = 0xC4EE982E, stored `2E 98 EE C4` | §7.4 | 0xC4EE982E | ✅ |
| Appendix A: trailer CRC-32C over trailer bytes [0,60) = 0xE00938D2, stored `D2 38 09 E0` | App. A | 0xE00938D2 | ✅ |
| Appendix A: directory region [16,20) = CRC of zero bytes = 0x00000000 | App. A | 0x00000000 | ✅ |

I decoded Appendix A's whole hexdump field by field against §6.2's layout
table: magic `8A 4E 52 41 54 0D 0A 1A`, version_major 1, version_minor 0,
flags 0, generation 1, dir_offset 16, dir_length 4,
committed_file_length 128 = the file's actual length, file_id
0x0123456789ABCDEF, reserved four zero bytes, CRC as above. Every gate of
[R-CNT-06] passes; 128 mod 64 = 0; dir_offset + dir_length = 20 ≤ F − 64 = 64.
**Appendix A is internally correct in every byte.**

Layout arithmetic I re-derived independently and found correct:

- §7.4's worked layer record: 4 + 34 + 18 + 12 + 13 = **81** bytes, and each
  stated field offset (0,4,5,7,9,11,19,27,35,36,38,40,48,56,63,68,69,77)
  matches a packed parse in table order. The extent length
  4 × 20 + ⌈4/2¹⁶⌉ × 4 = **84** is right.
- §11.2: G = (4,8), N = 32, P = 65,536; with E_y = 1000, G_y = 4. ✅
- §11.4: (300,700) → tile (1,2), s = 10, in-tile (44,188), in-tile ordinal
  11,452; planar channel 2 → disk ordinal 74. ✅
- §15.4: entry_count 1,000,000 → 16 segments (15 full + 16,960), CRC array 64
  bytes at [20,000,000, 20,000,064), segment 15 at [19,660,800, 20,000,000),
  entry 999,999 at segment-relative byte 339,180; a full segment is 1,310,720
  bytes = 1.25 MiB. ✅ Second example: disk ordinal 74 → region bytes
  [1,480, 1,500); channel 3 occupies entries 96–127. ✅
- §14.2: Q = 3, decoded 18, ordinal 5 at [15,18); planar `b` 12 bytes, ordinal
  5 at [10,12); float32+bool Q = 5, decoded 30, ordinal 5 at [25,30). ✅
- §14.3: alternating bools, P = 10 → `55 01`; with fill true → `55 FD`. ✅
- §14.5: extents (5,5), tiles (4,4) → grid 2×2, edge tile (1,1) has one real
  position and 15 padding positions, decoded 32 bytes, values 1–15 = `CD AB`. ✅
- §17.3: 1.0/2.0/3.0 float32 shuffled at s=4,n=3 gives
  `00 00 00 00 00 00 80 00 40 3F 40 40`. ✅ (I also verified the inverse
  restores the original.)
- §20.3's example: 32·20 + 4 = 644-byte index region. ✅
- §12.3's channel entry is exactly the twelve bytes given; bfloat16 1.0 is
  `80 3F`. ✅
- §21.9's note: 2³² entries → 2¹⁶ segments × 4 = 256 KiB; 2³⁶ → 4 MiB. ✅

**Register arithmetic.** I extracted every row of §21.2–§21.5 mechanically and
counted instances by §21.1's stated rules (a `—` cell is one instance,
otherwise semicolon-separated items). Result: **121 rows** (36 F + 49 L + 26 T
+ 10 R) over **277 instances** — exactly the figures §21.2/§21.3/§21.4/§21.5
and §21.8 state. I spot-checked the individuation rules against ~20 cells
(both-directions for *does not equal*, one direction for *exceeds*, layout
formulas enumerated, no direction for a checksum comparison, no instance for a
nonzero test) and found no cell that breaks them.

I also derived §21.2's new reach claim independently. [R-CNT-24] fixes four
invariants in every major: trailer magic at F−64; version_major/minor at F−56;
a CRC-32C at F−4 over [F−64, F−4); and the front block constant. The register
conditions asserting one of those are exactly F8 (magic), F14 (trailer CRC),
F6 (front block), and both instances of F1 (byte-reversed constants). Every
other row asserts something inside the 48 bytes [R-CNT-24] lets a future major
redefine, or is derived from format-major-1 structure (F5's 128-byte floor,
F13/F17's 64-alignment and length cross-check, F15's reserved bytes, F19's
flag lanes, F2/F3's field domains). F18 is correctly excused as outside the
premise. **§21.2's "F8, F14, F6 and both of F1's instances — and no other row"
is right**, and the §2.3 Note's three worked cases (F14 reaches, F5 does not,
F15 does not) are each right for the reasons given.

I also checked §2.2's prefix table, which the brief flagged as a presentation
change asserted to preserve content. I grepped every `R-XXX-NN` identifier in
the document: nineteen distinct prefixes are used, and the table lists exactly
those nineteen. Every identifier space is contiguous from 01 with no gaps
except the expressly withdrawn `[R-SER-04]` and the `[R-ENC-100]` that §2.2
itself uses as an example of numbers above 99. **The table is complete and
correct.** (`ERR | error register` slightly undersells §21.9's limits, which
also carry ERR identifiers; I do not think that is a defect worth a row.)

---

## 3. The open path, byte-exact

### 3.1 Cold remote open against a ranged server

Two requests. Nothing in the file bounds either one before I have read it —
the first range is a constant, the second is bounded by fields the trailer CRC
covers.

**Request 1** — `Range: bytes=-64`. 64 bytes. The suffix length is the one
number a reader may use with no prior knowledge: [R-CNT-24] fixes "the final
64 bytes of a file contain the trailer magic at F − 64" *in every format major
version*, so 64 is safe even against a file I cannot otherwise read. The
response also carries the transport-authoritative F (a `Content-Range`
complete length), which [R-CNT-10] requires be transport-authoritative and
never taken from `committed_file_length` — so §19.1's steps 1 and 2 cost one
request between them.

Validation, in §6.2's mandatory order:
1. bytes [0,8) == `8A 4E 52 41 54 0D 0A 1A` — else F8/F1, reject-file.
2. `u32` at 60 == CRC-32C over [0,60) — else F14, reject-file. **Only now may
   I act on any other trailer field** ([R-ENC-05], [R-ENC-10]).
3. version gate: version_major ≠ 0 (else F18), and a major I implement (else
   [R-CNT-07] capability refusal, with a diagnostic distinct from "not a TARN
   file" and from "corrupt"). version_minor is never a rejection ground.
4. then, all together: flags incompat lane 0–15 all clear (F19); ignore lane
   16–31 ignored; committed_file_length == F and F mod 64 == 0 (F17, F13);
   dir_offset ≥ 16 (F9); dir_length ≥ 4 (F16); dir_offset + dir_length ≤ F − 64,
   forming the sum first and rejecting above 2⁶³−1 (F3, F10); 1 ≤ generation ≤
   2⁶³−1 (F11, F2); file_id ≠ 0 (F12); bytes [56,60) all zero (F15). Plus the
   128-byte floor (F5), which §19.1 does not restate but §19's preamble makes
   due at this tier anyway.

**Request 2** — `Range: bytes=dir_offset-(dir_offset+dir_length-1)`.
`dir_length` bytes. Verify the final 4 bytes against CRC-32C over the
preceding `dir_length − 4` (F20) **before any other use of the region**
([R-CNT-11]). Only then parse the record sequence, whose extent is
[dir_offset, dir_offset + dir_length − 4) — F29's cell states that boundary
explicitly, which is the one place the sequence's end is pinned; §7.1 gets you
there too but only by inference from "those covered bytes are the record
sequence itself".

**Total: 2 requests, 64 + dir_length bytes.** For Appendix A's file that is
64 + 4 = **68 bytes**. For the 320-byte file I built in §7 below it is
64 + 126 = **190 bytes**.

The one-request variant: a speculative suffix window of W bytes. If the window
contains [dir_offset, dir_offset+dir_length), request 2 is unnecessary
(§6.4's containment test). Writers SHOULD keep dir_length + pad + 64 ≤ 65,536
so a 64 KiB window suffices. If the window reaches offset 0, bytes [0,16)
become **resident** and [R-CNT-04] then *obliges* the front-block equality
check before other processing. Appendix A works this through correctly,
including the sharp case: a 112-byte window on a 128-byte file covers
[16,128), contains the directory, and leaves [0,16) non-resident — so the
second request is spared and the front-block check is still optional.

The residency test is decidable at my own open path without classifying the
transport, which is exactly what [R-CNT-04] says it is for. I found no gap
here.

### 3.2 Record walk (§19.1 step 4)

Parse 24-byte headers; type 0 is a validity error, not an unknown type
(F24/L13). Apply the MU gate for unknown top-level types (F35 for a
reserved-range type with MU=1; MU=0 → ignore-record). Apply multiplicity: any
number of layer records including zero, at most one top-level user-metadata
record (F34). Validate extent slots of **non-layer** top-level records only
(F30/F31/F32) — a layer record's slot waits for layer access, which L1/L2/L15–L17
confirm by placing those rows at "layer access". Apply the extra framing a
top-level user-metadata record carries: slot ≠ (0,0) (F21), extent_length ≥ 5
(F22), inline_length == 1 (F23), and — not restated in §19.1 but due at open
by R1's *Detected* cell and §19's preamble — the encoding byte's value set.

Build the layer-name namespace. §19.1 answers the two questions I would
otherwise have had to guess: a layer record whose name field does not fit
inside its own `inline_length` contributes **no** name (so two such records are
not a duplicate), and uniqueness is decided over raw bytes *before* the names
are checked for validity, so two byte-identical invalid names are still F4
(reject-file) rather than two independent reject-layers. That ordering is
load-bearing and it is stated. Good.

---

## 4. Validation timing by tier

I mapped §19.2's tiers against every register row's *Detected* cell.

**At open** — front block (only if resident), trailer, directory region and
its record walk, the layer-name namespace. The L-rows detected at open are
exactly L3, L5, L6 (the layer record's own name: ill-formed UTF-8, empty,
C0 control) — reject-*layer* outcomes established at the *file*'s open, which
is consistent because the name parse is what the open needs and nothing else
about the layer is touched.

**At first access to a layer** — the whole of §19.3: extent slot, the §7.4
constraint set, exact parse and sub-record walk, dimension/channel names,
value sets of §11.4/§12.2/§14.1/§15.1/§17.2/§17.3, per-type fill, the lz4
declaration cap, the geometry floor and its arithmetic, every [R-ENC-04]
ceiling, and the index cross-checks that need no I/O. §19.3 asserts "layer
access performs no fetch"; I checked each cited rule and that holds — the
index cross-check [R-CNT-17] compares `extent_length` against a formula over
`entry_count`, both resident in the directory.

**At use of a tile** — the index chain and everything downstream. The only
reader-detected **layer-scope** rows at this tier are L37 and L38 (the
`crc_of_crc_array` and segment CRC). I verified that by scanning the whole
L-table: no other L row carries *Detected: tile use*. That matters because
§19.4 step 8's closed statement — "A failure inside the same request that
takes layer scope instead — step 3's index-chain failure" — is only correct if
that list is complete. **It is.**

**At use of a record's extent** — R2 through R10.

**Certification only** — F7, F25, F26, F27, F28, F33, F36; L18, L25, L40–L42,
L46–L49; T2, T4, T5, T26. A reader is never obliged to detect any of these,
and [R-CNF-12] lets it reject anyway once it has.

**Never checked by anyone** — §21.7's account. I tested its class-2 list
against my own derivation and found one obligation it does not name:
[R-LIF-02] step 3's "each commit appends its own complete directory". A writer
that appends payloads and then re-points the new trailer at a *prior*
generation's directory region produces bytes indistinguishable from a normal
file (the superseded structures precede the old directory, the newly appended
payloads become slack, and F7 does not fire because nothing *live* sits
between the live directory's end and the trailer). §9.2's own Note names this
as a way to leave step 3 unperformed. §21.7 also does not name the two
storage barriers of steps 4 and 6. I decided **not** to report this: §21.1
describes §21.7 as "the account, **by class**, of what fails" detectability,
and the class ("properties of a file's history, which §9.7 does not
reconstruct") plainly covers all three; §21.1's normative completeness clause
runs to the *register*, and no row is owed for an undetectable condition. No
implementer is misled and no verdict moves.

---

## 5. Layer access and the tile-read algorithm

From a layer name and a coordinate, the document gave me a complete algorithm
with no gaps. Walking it:

1. **Layer record.** Full validation per §19.3 before touching any declaration
   other than the name.
2. **Domain.** Point request: 0 ≤ xᵢ < Eᵢ for every i, else the *request*
   fails with no verdict on the file. Region request: intersect with the
   extents; wholly-outside or zero-extent succeeds empty. Note the deliberate
   asymmetry — §19.4 defines a range whose every interval holds one position as
   a *region* request, so the "same" out-of-range access succeeds-empty as a
   region and fails as a point. That is stated, not accidental, and §21.6's
   row restates it.
3. **Ordinals.** tᵢ = xᵢ div Tᵢ, uᵢ = xᵢ mod Tᵢ; in-tile ordinal
   Σ uᵢ ∏_{j>i} Tⱼ (row-major, for every linearization, permanently);
   s = Σ tᵢ ∏_{j>i} Gⱼ under linearization 1; disk ordinal = s interleaved,
   c·N + s planar.
4. **Index chain.** Fetch the segment-CRC array (region bytes
   [entry_count·20, entry_count·20 + ⌈entry_count/2¹⁶⌉·4)) and the segment
   containing entry k (region bytes [⌊k/2¹⁶⌋·2¹⁶·20,
   min((⌊k/2¹⁶⌋+1)·2¹⁶, entry_count)·20)); both ranges are computable from the
   layer record alone, may run in parallel, and may be cached under
   [R-LIF-03]. Verify `crc_of_crc_array` (L37) then the segment CRC (L38);
   either failure is reject-**layer**.
5. **Entry.** 20 bytes at region offset 20k. Classify by §15.3's eleven-row
   table. Sentinel (`FF ×16 00 ×4`) → fill, no payload I/O. Six *structural*
   rows → reject-tile. Verifier rows → not my problem as a reader.
6. **Payload.** Fetch [offset, offset+length), verify the entry's crc (T1)
   before decoding.
7. **Decode.** Codec first, then the filter's **inverse** — §17.1 states the
   writer's order (filter then codec) and the reader's reversal explicitly, so
   there is nothing to guess. Result length must equal the decoded size
   exactly (T3).
8. **Extract.** §14.2's table for interleaved and planar-numeric; §14.3's
   bit-packing for planar bool. Never return a padding position.
9. **Return.** Bit patterns unaltered. The single exception is a nonconforming
   interleaved boolean byte: 0x00 → false, every other byte → true.

**The exact decoded byte layout I end up with**, restated the way I would code
it:

- planar, numeric channel c: `P·Bᶜ` bytes; value k at `k·Bᶜ`.
- planar, bool channel: `⌈P/8⌉` bytes; value k at bit `k mod 8` of byte
  `k div 8`, LSB-first; the final byte's bits `P mod 8 … 7` are pad bits
  carrying the channel's fill bit.
- interleaved: `P·Q` bytes with `Q = Σ Bᵢ`; channel c at in-tile ordinal u sits
  at `u·Q + Fᶜ`, `Fᶜ = Σ_{j<c} Bⱼ`. Bool contributes one byte, Bᶜ = 1.

I checked the degenerate corners of all three: P ≥ 1 always (every Tᵢ ≥ 1), so
every decoded size is at least 1 byte — which is what §17.2's Note needs for
the "no zero-length non-sentinel entry" rule, and it is true. Q ≥ C ≥ 1.
L is divisible by the mandated shuffle stride in every case (Q | P·Q,
Bᶜ | P·Bᶜ, 1 | ⌈P/8⌉).

**One thing I proved for myself that the document only implies**, and which
turned out to matter for judging a register cell: the byte-shuffle permutation
always fixes the *last* byte of the image. Source offset j·s+i maps to i·n+j;
the last byte has j = n−1, i = s−1, and (s−1)n + (n−1) = sn − 1 = L − 1. So a
mis-strided shuffle can never disturb a packed plane's pad bits, which live in
the final byte. That is why T26's cell can say "the check that detects it is
T2's or T4's" and omit T5 — and why §21.7's parallel sentence about a
*mis-ordered value sequence* correctly says "T2, T4 **or** T5", since a
re-ordered value sequence *can* put a wrong bit in a pad position. I went into
that expecting a defect and came out satisfied the two cells differ correctly.

---

## 6. Degradation walks (seven, traced end to end)

**W1 — unknown record type, top level, MU = 0.** Reader ignores the record as
though absent (§2.4's ignore-record). All layers still served; the reference
array is untouched. §5.2 still classes its extent as a *record extent* of the
live state, so a verifier counts those bytes as claimed, not slack — but §8.1
covers them by no checksum, so corruption inside them is invisible
([R-SEC-04] says so). An updater re-emits the record byte-identically, or may
drop it only if PE = 0 *and* the commit independently changes the scope the
record attaches to. Caller gets: everything.

**W2 — unknown record type, top level, MU = 1 (experimental range).**
Reject-file ([R-CNT-15]). The file is nevertheless **conforming** — §21.6
names this as one of exactly two structural cases of a conforming file a
reader refuses. So my diagnostic must say "this reader cannot understand a
critical record", not "corrupt". Caller gets: nothing. The same type as a
*sub-record* is reject-layer and I must **not** reject the file
([R-CNT-18]); caller gets every other layer. I checked whether §2.3's
acceptance carve-out ("carrying no record of a type it does not implement with
MUST_UNDERSTAND = 1") over-reaches into the sub-record case and licenses
rejecting the file. It does not: the carve-out only lifts a *duty to accept*;
it grants no MAY, and [R-CNT-18]'s MUST NOT stands. In fact the carve-out is
*necessary*, or [R-CNF-03] would forbid the reject-layer that [R-CNT-18]
requires on a conforming file. No finding.

**W3 — unknown codec value.** Cannot happen for a conforming reader at an
*assigned* value: codecs 1–4 and filters 1–2 are core and a reader that
declines one is not a conforming reader. A reserved or experimental value is
reject-**layer** at layer access (L43/L45), from declarations alone, with no
I/O. Caller gets: every other layer, and may still list the rejected layer's
name (§2.4's reject-layer row). A *verifier* that cannot execute a codec is in
a different position — [R-COD-11] gives it *cannot establish*, not
*nonconforming*.

**W4 — unrecognized flag / enum value.** Trailer ignore-lane bit 16–31: ignore
it, the file is conforming, and if I am an updater I MUST copy it forward and
MUST NOT clear it. Incompat-lane bit 0–15: reject-file (F19). Reserved record
flag bits 2–15: readers MUST ignore; only a verifier records F26/L47. A stored
MU/PE bit that disagrees with §7.3's registry: I apply the **registry's**
semantics regardless, and only a verifier records F28/L49. An unassigned
user-metadata encoding ≥ 0x80: ignore-record, **not** a violation, and a
verifier still certifies but must report the record (scope, encoding value,
stored extent length). Encoding 0 or 3–0x7F: ignore-record **and** a violation
(R1).

**W5 — truncated tail.** Three sub-cases and the document distinguishes all
three. (a) Physical file longer than committed_file_length, or shorter: F17,
reject-file. (b) The final 64 bytes are not a valid trailer at all: F8 or F14,
reject-file, and I MUST NOT scan backward ([R-LIF-05]) — I cannot tell a torn
commit from corruption and I am not asked to. (c) A recovery tool *may* probe
backward at 64-aligned offsets, but that is not reader behavior and no verdict
turns on it; the earlier state it finds is a different artifact. Caller gets:
nothing, plus a "file torn or invalid" report. I checked the interaction with
[R-LIF-04]: residue past a completed commit reaches a reader as (a) or (b),
which §9.5's Note states.

**W6 — checksum mismatch, at each scope.** Trailer → reject-file. Directory →
reject-file. `crc_of_crc_array` or a segment CRC → reject-**layer** (even
though I detect it at tile use). Stored tile crc → reject-**tile**, and that
tile's read reports failure — I MUST NOT quietly return fill in its place
([R-CNF-09], [R-TYP-09]). User-metadata extent crc → ignore-record with a
SHOULD-report. On a region read spanning several tiles I may return the good
tiles' values with a per-entry failure report, or fail the whole request — but
never substitute fill. I walked the boundary case: an entry whose *only*
defect is a failing tile crc is still **well-formed**, so its extent still
counts for slab run continuity, for overlap checking, and for the coverage
walk; only the six *structural* rows make an entry contribute no extent. §15.3
and §16.2 agree on this word for word.

**W7 — limit exceeded.** §21.9's guarantees are floors, not caps. A file above
one stays conforming and I MAY decline it — at the whole file, or at the
narrowest scope whose *declarations* exceed what I can serve. The refusal MUST
be reported as a resource limit, never as a validity error. Declining a file
that lies *within* the table on that ground makes me non-conforming. This walk
is where finding **reader-01** below surfaced.

**W8 — format major I do not implement.** Reject-file on capability grounds
with a distinct diagnostic — but first I must still apply every *reaching*
condition ([R-CNF-13]): trailer magic, trailer CRC, and (if the bytes are
resident) the front block. If one of those fails I reject on *that* rule's
ground, and a verifier reports **nonconforming**, not *cannot establish*,
because the invariant broken is one every major shares. §6.2's mandatory order
puts magic and CRC ahead of the version gate precisely so this comes out
right. Caller gets: nothing, plus "TARN format major N; this reader supports
major 1".

---

## 7. A worked example I built myself

Appendix A verified byte-for-byte (§2 above), but it has no layer, so it
exercises none of Part II. I built a second file from the document alone to
see whether a non-trivial artifact is fully determined.

Layer `L`, rank 2, dimensions `y` (E=3, T=2) and `x` (E=5, T=4), interleaved,
channels `a` (uint8, fill 0x00) and `b` (uint16, fill 0x0000), linearization 1,
codec 1 (none), **filter 2 (byte-shuffle)**, no alignment, no slab.

Derived: G = (2,2), N = 4, P = 8, Q = 3, decoded size 24, entry_count = 4,
index region 4·20 + 4 = 84 bytes, layer-record inline_length 98,
dir_length 126.

Stored: only spatial ordinal 0 (tile coords (0,0), covering y∈[0,2), x∈[0,4) —
entirely real positions, so no [R-SER-05] obligation bites). Values
a(y,x) = 10y+x, b(y,x) = 1000+10y+x.

```
decoded image : 00 e8 03 01 e9 03 02 ea 03 03 eb 03 0a f2 03 0b f3 03 0c f4 03 0d f5 03
filtered (s=3, n=8)
              : 00 01 02 03 0a 0b 0c 0d e8 e9 ea eb f2 f3 f4 f5 03 03 03 03 03 03 03 03
stored bytes  = filtered (codec 1), length 24 = decoded size   ✔ [R-COD-04]
entry crc     = 0x7F6F478A
segment CRC   = 0x202613EE      crc_of_crc_array = 0xF8303917
```

Placement: front [0,16); tile [16,40); index [40,124); directory [124,250);
pre-trailer pad [250,256) — six bytes, because [R-LIF-02] step 5 pads to the
*next* 64-byte boundary and §6.2 settles the boundary case ("a writer that
ends its directory on a 64-byte boundary leaves none", so "next" means the
current position when already aligned — a 64-byte ambiguity the document
closes); trailer [256,320); F = 320, 320 mod 64 = 0.

Reading back coordinate (y,x) = (1,2): tile coords (0,0), s = 0, disk ordinal
0, in-tile ordinal 1·4+2 = 6. Entry 0 → offset 16, length 24. CRC verifies.
Codec 1 → filtered image; inverse shuffle → decoded image. `a` at byte
6·3+0 = 18 → `0C` = 12 ✔. `b` at bytes 19–20 = `F4 03` = 1012 ✔.

Reading (2,4): tile coords (1,1), s = 1·2+1 = 3, entry 3 is the sentinel →
a = 0x00, b = 0x0000, no payload I/O ✔. Reading (0,4): tile coords (0,1),
s = 1, sentinel → fill ✔.

**Every byte of this file was determined by the document.** I never had to
choose a value the text left open except where it says the choice is the
writer's (placement, and the file_id). That is a real result for Part II: the
serialization, the index, the filter, the CRC chain and the placement rules
compose without a gap.

---

## 8. Findings

### reader-01 — §22.2 [R-SEC-02] forbids the allocation §14/§17 direct a reader to make

**Kind:** CONTRADICTION. **Location:** §22.2, [R-SEC-02]; against §14.3
[R-SER-07], §17.2 [R-COD-06] and its closing Note, and §21.9 [R-ERR-04].

The whole of [R-SEC-02] is one paragraph. Its second sentence tells me where a
decode buffer's size comes from:

> "Decoded tile size is a function of the layer's declarations alone (§14.2,
> §14.3), so a reader allocates from geometry and never from a length embedded
> in a payload"

Its last sentence forbids exactly that:

> "A reader MUST NOT size an allocation, fetch, or index walk in proportion to
> a declared magnitude it has not corroborated against the file's actual
> length: a layer can declare 2⁶³ − 1 addressed tiles, and the declaration
> alone costs nothing to state."

A tile's decoded size is a declared magnitude — `P·Q`, `P·Bᶜ` or `⌈P/8⌉`,
derived from the layer's tile extents and channel types. Under **codecs 2, 3
and 4 it cannot be corroborated against the file's actual length at all**,
and the document says so in terms: §17.2's Note states "no bound relates a
stored length to its decoded size in either direction — codec 1's equality is
`[R-COD-04]`'s subject", and [R-COD-06] separately bars sizing any buffer from
the frame's own content-size field. So a forty-byte zstd extent may legitimately
declare a 256 MiB decoded size, and nothing in the file corroborates it. Only
codec 1 escapes, because [R-COD-04] pins the entry length to the decoded size
and [R-CNT-13]/§15.3 pin that length inside [16, F−64).

The two readings an implementer can defend:

- **(a) Literal.** The MUST NOT is unqualified, so I may not allocate a decode
  buffer for a compressed tile until something corroborates the decoded size
  against the file's length — which never happens. A reader taking this
  reading must decline every compressed tile whose decoded size it cannot
  corroborate, i.e. all of them.
- **(b) Scoped.** The MUST NOT reaches only magnitudes for which corroboration
  is *available* — entry counts against the index region's declared length
  ([R-CNT-17]) and that length against F ([R-CNT-13]), which is exactly the
  chain §22.2's own following Note walks — and decode buffers are bounded
  instead by §21.9's 256 MiB per-tile guarantee plus [R-ERR-04]'s licence to
  decline above it.

**I picked (b)**, and I think the document forces it, but only by a two-step
argument the implementer has to construct: reading (a) makes conformance
impossible, because §21.9 says "Software that declines **on that ground** a
file whose every quantity lies within the table is not a conforming reader",
so a reader that refuses to allocate 256 MiB for an in-guarantee tile is
non-conforming — while a reader that allocates it is violating [R-SEC-02] on
reading (a). Nothing can satisfy both. Since the document elsewhere insists
four separate times that a reader allocates from declarations, (b) is the only
coherent reading.

**What an implementer does wrong without it:** builds a reader that refuses to
allocate a decode buffer larger than the stored extent — a very natural
anti-bomb heuristic, and precisely what a security-conscious engineer reading
§22 would implement — and thereby fails §21.9's acceptance floor on ordinary
compressed files. Or, worse, sizes the buffer from the stored length and then
fails [R-SER-07]'s exact-size rule.

**Byte-level:** No. Both readings agree on which byte sequences are conforming
and on every accept/reject verdict about a file's validity; they differ only in
whether a particular reader is entitled to issue a *resource* refusal, which
[R-ERR-04] already classes as "not a validity error". §21.9 decides the dispute
even if it makes the implementer work for it.

**Fix that would settle it:** qualify the MUST NOT — e.g. "…in proportion to a
declared magnitude the file's own cross-checks do not bound; a tile's decoded
size is bounded instead by §21.9's per-tile guarantee and [R-ERR-04]" — or say
plainly that decode buffers are the excepted case.

---

### reader-02 — §14.4's Note is false for a legal single-channel bool layer with one sample per tile

**Kind:** OBSERVATION. **Location:** §14.4, the Note following [R-SER-09]
("A single-channel numeric layer produces byte-identical tile images…").

> "A single-channel numeric layer produces byte-identical tile images under
> either layout. A single-channel bool layer does not — ⌈P/8⌉ packed bytes
> planar versus P bytes interleaved — and both forms are valid; writers
> wanting compact masks choose planar."

The stated reason evaporates at **P = 1**, which is legal: [R-GEO-01] requires
only Tᵢ ≥ 1, so a rank-1 layer with T = (1) has P = ∏Tᵢ = 1, and ⌈1/8⌉ = 1 = P.
Both images are then one byte, and with the channel's fill = `0x00` they are
**byte-identical**:

- planar: value 0 in bit 0; pad bits 1–7 must carry the fill bit ([R-SER-05]),
  which is 0 — so the byte is `0x00` or `0x01`.
- interleaved: a single byte, `0x00` or `0x01` (§14.2).

The two agree exactly. (With fill = `0x01` they differ — `0xFE`/`0xFF` versus
`0x00`/`0x01` — so the Note is right for that half of the case and wrong for
the other, which is worse than being wrong throughout: the reader has no way to
see that the claim is fill-dependent.) For every P from 2 to 8 the lengths do
differ, so P = 1 is the sole counterexample, and it is the one the Note's own
formula ⌈P/8⌉ vs P collapses on.

**Which reading I picked:** the normative text is unambiguous — §14.2 and
§14.3 fix both images exactly, and I implemented from them, not from the Note.
The Note is simply a false universal about what those two rules imply.

**What an implementer does wrong without it:** nothing in a reader. The risk is
in a *test suite* or a writer: someone who trusts "a single-channel bool layer
does not [produce byte-identical images]" may build a round-trip test that
asserts the two layouts differ, and it will fail on the degenerate layer, or
assert a layout-detection heuristic that has no ground.

**Byte-level:** No. [R-CNF-01] exempts text labelled *Note*, and §14.2/§14.3
fix every byte of both images regardless. Nothing about which files may be
emitted or accepted moves.

---

### reader-03 — Appendix G item 10's length claim is false for a large class of NFD names

**Kind:** OBSERVATION. **Location:** Appendix G (non-normative), item 10.

> "**Names normalized to Unicode Normalization Form C**, which `[R-ENC-14]`
> states as a SHOULD. A caller-supplied decomposed name is a different name
> under `[R-ENC-13]` and a different length — §4.6's `température` is 12 bytes
> in NFC and 13 in NFD — so a writer that does not normalize emits a different
> layer record, a different `inline_length`, and a different `dir_length`."

"A different name" and "a different layer record" are both true. "**A different
length**", and the two consequences that hang off it — "a different
`inline_length`, and a different `dir_length`" — are false for every name whose
NFD and NFC forms have equal UTF-8 length. Those are not exotic: I enumerated
the BMP and SMP and found **155** single characters whose NFD form is a
different byte string of the *same* UTF-8 length. The first is U+1E00 LATIN
CAPITAL LETTER A WITH RING BELOW:

```
NFD  U+0041 U+0325 = 41 CC A5   (3 bytes)
NFC  U+1E00         = E1 B8 80  (3 bytes)
```

The class is the Latin Extended Additional block — an ASCII base letter (1
byte) plus a combining mark in U+0300–U+036F (2 bytes) composing to a
three-byte precomposed character. Vietnamese and scholarly transliteration
live there, so a name like `Ḁ` or `ḅ` is an entirely ordinary layer name. A
non-normalizing writer emits different *bytes* for such a name but the **same**
`inline_length` and the same `dir_length`.

**Which reading I picked:** the profile item itself is unaffected — pinning
names to NFC still closes the degree of freedom, because the *bytes* differ
even when the lengths do not. Only the justification is wrong. I read item 10
as "normalize, because otherwise the layer record's bytes differ", which is
sound.

**What an implementer does wrong without it:** an adopter of the profile who
believes normalization only ever changes the record's *length* may write a
reproducibility check that compares `inline_length` and `dir_length` and
concludes two files match when their names differ byte-for-byte — exactly the
"visually identical but byte-distinct names" failure §4.6's Example and
[R-ENC-14] exist to warn about, reintroduced by the sentence meant to close it.

**Byte-level:** No. Appendix G is identified as non-normative, "adds no
requirement to any actor", and [R-CNF-01] exempts it; a writer ignoring the
whole profile "is fully conforming". The emittable set is untouched.

---

## 9. Noted, examined, and deliberately **not** reported as findings

I want these visible so the reasoning can be checked, but I judged each below
the bar or already known.

1. **Appendix G item 5's closing clause is a false universal.** "The filter is
   the identity exactly where its permutation is — where the stride is 1 … and
   equally where the decoded image is a single group, n = L/s being 1
   (`[R-COD-10]`); **elsewhere it changes the stored bytes of every tile it
   touches.**" The first half is exactly right — I verified that j·s+i = i·n+j
   for all i,j iff s = 1 or n = 1. The tail is false: a tile whose decoded
   image is byte-constant is a fixed point of *any* stride's permutation, and
   such a tile is legal and need not be sentinelled (item 6 only sentinels
   *all-fill* tiles). Concretely: interleaved, channels `a` (uint8, fill 0x00)
   and `b` (uint8, fill 0x00), T = (2), so P = 2, Q = 2, L = 4, s = 2, n = 2
   (non-identity); a tile whose four decoded bytes are all `0x11` filters to
   itself, so filter 2 changes none of its stored bytes. I am not reporting
   this because the brief states that one sentence in Appendix G has been given
   three different false universals in three cycles and has been sent to the
   maintainer's ledger rather than repaired again; this sentence carries every
   mark of that history (an "exactly where", two separately-patched cases, and
   a trailing universal), and I take it to be the ledgered one. If it is not,
   this paragraph is the report.
2. **§16 states no owning scope.** Every other structure-defining section does
   ([R-CNF-08] promises "stated in the section that defines the structure"),
   and §3.1 defines a *slab* as a structure. No gap results: the alignment,
   slab and slab-alignment fields live in the layer record's inline payload,
   whose owning scope §7.4 states, and every §16 invariant names its outcome
   expressly (reject-layer). Nothing to decide.
3. **[R-ENC-04]'s parenthetical names two kinds nothing designates.** It lists
   "(offsets plus lengths, grid counts, tile counts, sample-position counts,
   **ordinals**)", but "A designation is express, made by the section that
   defines the quantity", and §11.2 designates no grid count while §11.4
   designates no ordinal. Harmless: Gᵢ ≤ Eᵢ and every ordinal is strictly
   dominated by a quantity that *is* designated (in-tile < P, spatial < N, disk
   < C·N), all of which L2 enumerates — the register even says so in the cell
   ("C·N (which dominates the max disk ordinal (C−1)·N + (N−1))"). No reader
   obligation is created or missed.
4. **T24 ("any codec") overlaps T14 for codec 1** without being listed among
   §21.1's specializations. Both are reader/tile-use/reject-tile, so nothing
   diverges, and §21.1's list is introduced with "Some rows are…", not as
   closed. §24 already says a vector records every row a file exercises.
5. **R7 and R8 overlap** on the bare tokens `NaN`/`Infinity`/`-Infinity`, which
   are both "not well-formed JSON" and "a non-finite number". Same outcome
   (ignore-record), same detector, same tier.
6. **§2.1's Note claims "every writer-side prohibition is paired with an
   explicit reader-side clause"**, which is not true of [R-LIF-01] or
   [R-LIF-02] — but those have no single-file witness, so there is no violating
   file for a reader to be told about, and §21.7 accounts for them. Note-level,
   and the exception is structural rather than an oversight.
7. **§2.3's acceptance carve-out** for a file carrying an unimplemented MU = 1
   record reads broadly enough to cover a *sub-record*, where §21.6 says the
   file is "never a ground to refuse". I traced this expecting a fork in the
   accept/reject verdict on a conforming file and concluded there is none: the
   carve-out only lifts a duty to accept, grants no MAY, and [R-CNT-18]'s
   "a reader MUST NOT reject the file for it" is unconditional. The carve-out
   is in fact *required*, or [R-CNF-03] would forbid the reject-layer
   [R-CNT-18] mandates.
8. **§18.2's "the bound above"** in the verifier sentence is ambiguous between
   the document-size bound and the frame's declared-window bound, both of which
   the paragraph introduces. §21.5's preamble treats the two identically
   ("declines the decode on the size bound **or** on the frame's declared
   window"), and both readings land on the same verdict (*cannot establish*),
   so nothing turns on it.
9. **[R-LIF-02] step 3 and the two barriers are absent from §21.7's class-2
   list** — see §4 above. §21.1 calls §21.7 an account "by class", the class
   covers them, and no register row is owed for an undetectable condition.

---

## 10. Things I checked and found sound, in case that is useful

- §8.1's coverage map really does cover every field exactly once, with the
  stated exceptions. I traced each of: trailer CRC → trailer[0,60); directory
  CRC → the record sequence; `crc_of_crc_array` → segment CRC array; segment
  CRC → its entries (including each entry's own `crc` field); entry `crc` →
  the stored tile; user-metadata extent's final 4 bytes → the encoded bytes
  before decoding. The three terminal fields (trailer, directory, metadata
  extent) are covered by nothing, as §4.5 says, and the three interior ones
  are each both comparison-verified and covered exactly once.
- §6.3's arithmetic: 8 (magic) + 4 (major/minor) + 4 (CRC) = 16 fixed, leaving
  **48** redefinable, and format major 1's trailer assigns all 64 bytes
  (8+2+2+4+8+8+8+8+8+4+4 = 64). Both stated figures are right.
- §17.2's zstd Note: with Single_Segment_Flag set, Window_Size *is* the frame
  content size, which [R-COD-06] already pins to the decoded size; without it,
  the Window_Descriptor cannot express below 1 KiB — so a sub-1-KiB tile is
  encodable only as a single-segment frame and no conforming file turns on
  which derivation a reader uses. Correct as stated.
- §17.2's lz4 escape: the addressed-tile count is N or C·N with N = ∏⌈Eᵢ/Tᵢ⌉,
  so it is positive **iff every extent is nonzero** — exactly what the Note
  claims, including the "a growth that leaves any extent at 0 holds the count
  at 0" clause.
- §11.1's rationale, "Growth that leaves entry_count unchanged touches the
  directory alone": true, because grid counts are non-decreasing under growth,
  so a constant positive product forces every factor constant, and the only
  other case is N holding at 0 where there is no index at all.
- §19.4's planar Note: entries at c·N+s are N·20 region bytes apart, and for
  N ≥ 2¹⁶ consecutive channels are guaranteed to land in different segments.
  Verified.
- §20.3 step 4's bar and its carve-outs are consistent with §11.1's rationale,
  §23.1's two exhaustive cases, and §21.7's account of where the bar has no
  witness. I tried to break it with a planar layer that gains or loses a
  channel while storing tiles (permitted — nothing §14 fixes for an existing
  channel's plane moves) and with a shrink that both de-addresses tiles and
  creates padding positions (permitted only where those positions already hold
  the fill). Both come out determinate.
- §21.6's "Two structural cases are conforming files a reader nevertheless
  refuses" survives the obvious third candidate — a resource refusal under
  [R-ERR-04] — because §21.9 explicitly separates that ground ("the two
  capability refusals §21.6 names … are not this ground").

## 11. Confidence

**Medium-high.** I built a complete non-trivial file from the document alone
and read it back, and the only place I had to reason past the text rather than
from it was reader-01's allocation question. Two of my three findings are in
non-normative text and none of them moves a byte.
