# Cleanroom round 17 — Adversary transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,317 lines, read in five contiguous `Read` calls covering lines 1–4317 with no
gaps). I ran one `grep` against that file (`still stores|stores no tile|storing no
tile|re-declar|supersedes`) and one `wc -l`. Everything else I ran was local
computation over files I wrote myself in the scratchpad: a CRC-32C implementation
(`crc.py`), a minimal-file builder (`minfile.py`), a two-layer file builder
(`build.py`, output `probe.tarn`), and one register-table counting script that
parses the register rows out of the spec text. I did not open `docs/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `CONTRIBUTING.md`,
`conformance/`, `spec/registry.json`, or any ADR; I ran no `git` command, no web
search, and no web fetch; I did not list the output directory. I wrote this file
and my scratch files and read back only my own scratch files.

---

## 0. Method

I read the document cold, front to back, then did three things in parallel:

1. **Reproduced every number the document states.** Any spec that gets its own
   worked examples wrong is usually wrong somewhere load-bearing too.
2. **Built files.** A 128-byte minimal file, a 192-byte single-empty-layer file
   (by arithmetic), and an 832-byte two-layer file with real tiles, real index
   regions, real segment CRCs, and a file-scope user-metadata record.
3. **Attacked seams**, in the order the charter lists them, plus the eleven
   sections the brief named.

I did not walk the eleven named sections in order and narrate them. I read them,
then went where the construction forced questions.

---

## 1. Reproducing the document's arithmetic

I implemented CRC-32C (Castagnoli, reflected in/out, init `0xFFFFFFFF`, final XOR
`0xFFFFFFFF`) and checked it against §4.5's check vector before trusting it:

```
CRC32C("123456789") = 0xE3069283   ✓ (§4.5)
CRC32C("")          = 0x00000000   ✓ (§4.5)
```

Then every constant and worked example in the document:

| Claim | Where | Verified |
|---|---|---|
| Appendix A's 128-byte file, trailer CRC `D2 38 09 E0` = 0xE00938D2 over `[0,60)` | App. A | ✓ byte-for-byte; I rebuilt the whole 128 bytes and they matched the hex dump exactly |
| Segment CRC over four sentinel entries = `0x80A34955` | §7.4 example | ✓ |
| `crc_of_crc_array` over that 4-byte array = `0xC4EE982E` | §7.4 example | ✓ |
| CRC of a full 2¹⁶-sentinel segment = `0xEECB3BB2` | §15.4, App. B | ✓ |
| §7.4's layer-record inline payload is 81 bytes, `4 + 34 + 18 + 12 + 13` | §7.4 | ✓ my independent builder emitted 81 |
| §15.4's 1,000,000-entry example: 16 segments (15 full + 16,960), 64-byte array, region 20,000,064 bytes, tile 999,999 at segment-relative byte 339,180, segment 15 at `[19,660,800, 20,000,000)`, full segment = 1.25 MiB | §15.4 | ✓ all |
| §15.4's planar example: C=4, N=32, channel 2 at s=10 → disk ordinal 74, entry bytes `[1,480, 1,500)`; channel 3 = entries 96–127 | §15.4 | ✓ |
| §11.4's example: (300,700) → tile (1,2), s=10, in-tile (44,188), ordinal 11,452; planar channel 2 → 74 | §11.4 | ✓ |
| §14.2's examples: Q=3/size 18/bytes [15,18); planar b 12 bytes/ordinal 5 at 10–11; float32+bool Q=5/size 30/[25,30) | §14.2 | ✓ |
| §14.3's example: `55 01` with fill false, `55 FD` with fill true | §14.3 | ✓ (pad bits 2–7 set gives `0x01 \| 0xFC = 0xFD`) |
| §14.5's example: edge tile (1,1) over extents (5,5)/tiles (4,4) has 1 real and 15 padding positions; 32 bytes, values 1–15 = `CD AB` | §14.5 | ✓ |
| §17.3's shuffle example: `00 00 00 00 00 00 80 00 40 3F 40 40` | §17.3 | ✓ recomputed from `i·n + j` |
| §20.3's example: 32-tile index region = 32·20 + ⌈32/2¹⁶⌉·4 = 644 | §20.3 | ✓ |
| §16.2's slab example: rows 1–2 = ordinals 8–23 = runs 1 and 2 | §16.2 | ✓ |
| §21.9's note: 2³² tiles → 256 KiB CRC array; 2³⁶ → 4 MiB | §21.9 | ✓ |
| `[R-CNT-27]`'s 128-byte floor derivation | §5.1 | ✓ dir_offset ≥ 16 ∧ dir_length ≥ 4 ∧ dir_off+dir_len ≤ F−64 ⇒ F ≥ 84; F mod 64 = 0 ⇒ F ≥ 128 |

Then §21.8's normative count, which is mechanical once §21.1 fixes the counting
rule ("Instances within a cell are separated by semicolons, and a cell reading —
is one instance"). I parsed all 121 register rows out of §21.2–§21.5 and counted:

```
rows 121   instances 273
F: 36   L: 49   T: 26   R: 10
```

§21.2 says 36, §21.3 says 49, §21.4 says 26, §21.5 says 10, §21.8 says "121
conditions over 273 instances". All five agree. I did not pursue the register
further: my standing experience is that register rows produce over-claims, and
§21.1 has already decided that where a row and its rule diverge the rule governs,
so a discrepant row is a table defect and not a verdict fork.

**Every number in the document is right.** That is unusual and it changed how I
spent the rest of the round: I stopped hunting arithmetic and went after the
prose that quantifies obligations.

---

## 2. What I built

### 2.1 The minimal file

Reproduced Appendix A exactly. Nothing to guess.

### 2.2 The minimal file with one layer

By arithmetic, not bytes: a rank-1 layer named `a`, dimension `d` with E=0, T=1,
one bool channel `c`. `[R-GEO-02]` makes E=0 valid; grid count 0, N=0,
addressed-tile count 0, `entry_count = 0`, extent slot (0,0),
`crc_of_crc_array = 0` (`[R-CNT-23]`). Inline payload:

```
name              2      (u8 len 1 + 'a')
layout..C        34      (1 + 2 + 2 + 2 + 8 + 8 + 8 + 1 + 2)
dim entry        18      (2 + 8 + 8)
chan entry        6      (2 + 2 + 1 + 1)   bool element size 1
trailing fixed   13      (1 + 8 + 4)
                 --
                 73
record           97      (24-byte header + 73)
directory       101      (97 + 4-byte CRC)
dir end         117      (16 + 101)
F               192      (117 + 64 rounded up to a multiple of 64)
pre-trailer pad  11
```

Nothing to guess here either. Note the pad is 11, not 0, and §6.2 explicitly
tells me that is fine: "a writer that ends its directory on a 64-byte boundary
leaves none". §9.2 step 5 pads to the next 64-byte boundary, so 11 is exactly
what a conforming commit produces.

### 2.3 The two-layer working file (`probe.tarn`, 832 bytes)

- **Layer A** `sst`: rank 1, E=100, T=32, interleaved, one float32 channel `temp`
  with fill qNaN `0x7FC00000`, codec 1, filter 1. G=4, N=4, entry_count=4,
  P=32, Q=4, decoded size 128. Tile 0 stored (values 0.0…31.0); tiles 1 and 2
  sentinel; tile 3 stored — it covers positions 96–127, of which 96–99 are real
  and 100–127 are padding, so its last 28 values are the recorded fill
  (`[R-SER-05]`).
- **Layer B** `mask`: rank 2, E=(5,5), T=(4,4), **planar**, one bool channel `m`
  with fill `0x00`. G=(2,2), N=4, C=1, entry_count=4, P=16, packed decoded size
  ⌈16/8⌉ = 2 bytes (`[R-SER-03]`). Tile at spatial ordinal 0 stored as `55 55`
  (alternating); tile at spatial ordinal 3 — tile coordinates (1,1), covering
  y∈[4,8), x∈[4,8), with exactly one real position (4,4) at in-tile ordinal 0 —
  stored as `01 00`: value true at bit 0 of byte 0, and the other fifteen
  positions are padding carrying the fill bit 0. P mod 8 = 0 so there are no pad
  bits, which is precisely §14.3's note ("A plane can have many padding positions
  and no pad bits").
- A file-scope user-metadata record, encoding 1, holding a sorted-key JSON object
  with a terminal CRC-32C over the document bytes.

Layout: front `[0,16)`; tiles; the metadata extent; layer A's index region;
layer B's index region; the directory at 507 for 252 bytes; a 9-byte pad; the
trailer at 768. F = 832.

Coverage check by hand: 16 + 128 + 128 + 2 + 2 + 63 + 84 + 84 + 252 + 64 = 823,
so the slack total a verifier owes (`[R-CNT-21]`) is 832 − 823 = 9 — the pad, and
nothing else. `[R-CNT-05]`/F7: no structure sits between 759 and 768. ✓

**Places I had to make a decision while building this, and what decided them:**

- *Must every structure precede the directory?* Not stated as such; it follows
  from `[R-CNT-05]` ("no structure lies between its end and the trailer") plus
  F7. Decided by the text.
- *Is a layer's tile-index region a "record extent"?* Yes — §9.7 says the region
  "enters the walk once, as that record's extent", and §20.5 calls it "itself a
  record extent (§5.2)". Decided.
- *Layer B's disk ordinals.* Planar with C=1 gives c·N+s = s, and row-major
  s = t_y·G_x + t_x. §11.4. Decided.
- *What does `[R-COD-04]` require of a packed bool plane under codec 1?* The
  entry's length must equal ⌈P/8⌉ = 2. Decided.
- *Does the layer-B edge tile need pad bits set to fill?* No — P mod 8 = 0.
  §14.3 is explicit. Decided.

I did not have to guess anything to build a conforming file. That is a real
result and I want it on the record before the findings.

---

## 3. Attacks that the document forecloses

I record these because "empty is a real result, but only if the attacks were
good", and several of these are the shapes that have historically produced
findings.

**A longer-than-necessary pre-trailer gap.** File with the directory ending at
100 and the trailer at F−64 = 1024, leaving 924 bytes of slack. Foreclosed
twice: §6.2 says "a longer gap is conforming, and no conforming commit produces
one", and §2.3 names it as one of exactly two writer obligations whose violation
is expressly not a file-conformance violation. Both verifiers certify.

**A byte string in the pre-trailer gap that parses as a record / a trailer.**
`[R-CNT-05]`: "A verifier MUST treat a structure in that gap as a validity error
at file scope." I wanted "structure" to be pattern-based so that planted bytes
would fork the verdict. It isn't: §5.2 defines a structure as "a stored-tile
extent, a record extent …, the directory, or the trailer" — i.e. something a
live claimant claims — and F7's Instances cell confirms it ("stored-tile extents;
tile-index regions; record extents; sub-record extents"). Planted bytes are
slack, and §21.6 registers the trailer-mimic as inert. Foreclosed.

**An ignored record's malformed extent slot.** Top-level record, type `0x8001`
(experimental), MU=0, PE=0, `extent_offset = 100`, `extent_length = 0`. Reading
A: F30 fires (reject-file). Reading B: `[R-CNT-15]` makes it ignore-record, §2.4
says an ignored record "is skipped as though absent", so its slot is never
examined and the file certifies. Foreclosed by three separate sentences:
`[R-CNT-15]`'s own "This governs a reader's treatment, not the file's validity";
§21.5's "the outcome bounds a reader's blast radius and never makes the file
conforming"; and §19.1 step 4, which puts "the extent-slot validity rules for
non-layer top-level records (`[R-CNT-13]`)" in the open with no carve-out for
ignored types. Reading B dies.

**Front-block divergence between a local and a remote reader.** File whose bytes
`[0,16)` are corrupt. A local reader must reject (`[R-CNT-04]`); a remote reader
issuing two exact ranges may never fetch them and may serve the file. This is a
real behavioural fork and it is entirely deliberate — §6.1 spends a paragraph on
why the test is residency rather than transport, and F6's Condition cell restates
the exemption. Crucially it is **not** a verifier fork: §2.3 gives verifiers no
such exemption, F6 says so ("a verifier holds no such exemption (§2.3)"), and
Appendix H repeats it. Both verifiers reject. Foreclosed.

**Overlap taxonomy.** I tried every overlap pairing: two stored extents of one
layer; a stored extent over its own index region; a stored extent over a
*different* layer's index region; a sub-record extent over the directory; two
non-layer record extents; a claimant reaching `[0,16)` or `[F−64, F)`.
`[R-CNT-13]` partitions these into reject-layer / reject-file exhaustively, and
F33's Condition cell explicitly routes the front-block and trailer cases to the
bounds rows "each at its own tier". No gap.

**Every §15.3 boundary.** `offset = S ∧ length = S ∧ crc ≠ 0` (T6);
exactly one half sentinel (T7); `length = 0` (T10); `offset = 15` (T8);
`offset = 2⁶³` with `length = S` (T7 and T11 both, which §24 handles by recording
every row a file exercises); `offset = 2⁶³−1, length = 1` (T12 and T9). All
classified. I could not construct an entry §15.3 leaves unclassified.

**Degenerate geometry.** d=1 with E=0; d=2 with E=(0,5); planar C=4 with N=0;
`T_i > E_i` (single padded tile); slab declared on a layer with zero addressed
tiles. All defined: `[R-GEO-01]`, `[R-GEO-02]`, §11.1's parenthetical, §16.2's
empty block. The lz4 cap's escape at N=0 is not only defined but has a Note
explaining that `[R-ENC-04]` carries no such quantifier — I checked that P·Q and
P·B^c really are still computable and checkable in an empty layer, and they are.

**Zstd at a sub-1-KiB tile.** Decoded size 2 (§14.3's example). The
Window_Descriptor cannot express under 1 KiB, so the only legal encoding is a
single-segment frame, whose Window_Size is the frame content size, which
`[R-COD-06]` already forces to equal the decoded size. §17.2's Note works this
out and it is correct: "no conforming file turns on which derivation a reader
implements."

**Byte-shuffle divisibility.** §17.3 asserts "The decoded image's length L is
divisible by s in every case (§14)". Checked all three: planar numeric
L = P·B^c, s = B^c; interleaved L = P·Q, s = Q; packed bool L = ⌈P/8⌉, s = 1.
True.

**The oversized-anything acceptance seam.** rank 33, a 20 MiB directory, a 512
MiB tile, a 20 MiB metadata document, a 16 MiB zstd window. Every one is a
§21.9 minimum guarantee, every one leaves the file conforming, every refusal is
`[R-ERR-04]`'s resource-limit report. Two readers diverge; no verifier certifies
a nonconforming file on that ground. Foreclosed — with one wrinkle I do report
below (finding 04).

**Duplicate layer names where the names are themselves invalid.** Two layer
records whose name fields are both `00` (empty). §19.1 step 4 is explicit:
"Uniqueness is decided first, and over the raw name bytes whether or not each
name is itself well-formed … so two layers whose name fields are byte-identical
are a duplicate even when neither name is valid." F4 and its "both obtainable
within their records' inline_length" qualifier close the truncated-name variant.
Foreclosed, and impressively so.

**The §8.1 coverage map's "exactly one checksum" claim.** I traced every field:
entry `crc` → its segment CRC → `crc_of_crc_array` → directory CRC → (terminal).
Stored tile bytes → entry `crc`. Trailer, directory-region and user-metadata
terminal CRCs → nothing, as §4.5 states. Front block → equality. Unassigned
record type's extent → nothing, as stated. Slack → nothing, and it is not a
structure. The map is complete and consistent.

---

## 4. Findings

### adversary-01 — CONTRADICTION — §20.5, `[R-WRT-06]` vs `[R-WRT-07]`

**A compactor is told both that it MUST refuse to emit a file carrying a
violation it has detected, and that it reproduces a structurally invalid index
entry into its output.**

`[R-WRT-06]` (§20.5):

> A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges fails,
> and MUST NOT emit a file carrying a violation it has detected: it can neither
> re-emit the structure corrected (`[R-WRT-05]`), nor keep it and call the output
> clean. Dropping is the one disposal that answers, and only where §20.4's table
> licenses it: a record dropped is not in the output, so the output carries no
> violation and the prohibition — which bites on what the output carries — is
> satisfied. Where the table does not license a drop the compactor MUST refuse.

`[R-WRT-07]` (§20.5), the same subsection:

> an entry §15.3 classifies reject-tile on a structural ground is reproduced with
> its offset and length exactly as they stand, there being no live extent for a
> re-pointing to target — `[R-IDX-03]` gives such an entry no stored extent and
> no claimant in the coverage walk — and the violation travels with it into the
> output (`[R-WRT-01]`); `[R-WRT-09]`'s checks reach the index chain and each
> stored tile's entry crc, not an entry's own value domain, so such an entry is
> not one `[R-WRT-06]` obliges a compactor to refuse

**The construction.** Take my `probe.tarn` and change layer A's index entry for
disk ordinal 1 from the sentinel to `offset = 0xFFFF_FFFF_FFFF_FFFF,
length = 0x0000_0000_0000_0080, crc = 0` — §15.3's third row, "offset = S ∧
length ≠ S", *structural*: reject-tile, register row T7, detector **reader**,
detected at **tile use**. Recompute the segment CRC and `crc_of_crc_array` so the
index chain verifies. The file is nonconforming (T7) but every checksum passes
and layer A's other three entries are fine.

Feed it to two compactors.

- **Compactor A** classifies each entry per §15.3 before regenerating the index
  region. It must: `[R-WRT-09]` obliges it to verify "each relocated extent's
  checksum, including **every stored tile's entry crc**", and the only definition
  of which entries address stored tiles is §15.3's classification — and
  `[R-WRT-07]` itself instructs it to treat "an entry §15.3 classifies
  reject-tile on a structural ground" differently from a sentinel and from a
  well-formed entry, which is not a distinction one can act on without making it.
  Having classified, it has **detected** a T7 violation. §15.3 is addressed to
  readers ("a reader MUST classify as follows"), §2.3 makes updaters "readers of
  the files they process [who] inherit every reader obligation", `[R-CNF-04]`
  makes a reader detect every register row whose detector is the reader, and T7's
  detector is the reader. So the detection is not optional. `[R-WRT-06]` then
  bites: dropping is not licensed (an index entry is not a droppable record), so
  "Where the table does not license a drop the compactor MUST refuse."
  **Compactor A emits nothing.**
- **Compactor B** follows `[R-WRT-07]` literally: it reproduces the entry with
  its offset and length exactly as they stand, recomputes the segment CRCs over
  the entries as re-emitted, updates `crc_of_crc_array`, mints a fresh `file_id`,
  writes generation 1. **Compactor B emits a specific 832-ish-byte file** in which
  the T7 violation survives — which is exactly what `[R-WRT-07]` says happens
  ("the violation travels with it into the output").

Both defend from §20.5. They differ on whether any output bytes exist at all.

**The permitted readings.** `[R-WRT-07]`'s carve-out — "such an entry is not one
`[R-WRT-06]` obliges a compactor to refuse" — can be read (i) narrowly, as
disposing only of `[R-WRT-06]`'s *first* clause, since the reason it gives is
clause-1-shaped ("`[R-WRT-09]`'s checks reach … not an entry's own value domain,
**so**…"), leaving the second clause and its closing "Where the table does not
license a drop the compactor MUST refuse" fully in force; or (ii) broadly, as
disposing of `[R-WRT-06]` entirely for such entries. I pick (i), because the
carve-out's stated reason supports only (i): clause 2's trigger is *detection*,
not `[R-WRT-09]`'s check list, so an argument about what `[R-WRT-09]` checks
cannot license an exception to it. Under (i) the two rules are inconsistent and
`[R-WRT-07]`'s reproduction provision is text no conforming compactor can ever
exercise.

**What sharpens this.** §20.3 step 2 gives the *appender* the mirror-image case
and resolves it the other way, in so many words: "a malformed index entry an
appender meets while re-emitting a region is carried forward byte-identically at
its disk-ordinal position under step 4, not repaired to a sentinel." The appender
has no clause like `[R-WRT-06]`'s second, so for the appender the carry-forward
is clean. The compactor was given a prohibition the appender was not, and
`[R-WRT-07]` then describes the compactor doing what the appender does.

**A second instance of the same clause.** `[R-WRT-06]`'s clause 2 makes a
compactor's output depend on its own thoroughness in a second place. A top-level
record with a **reserved-range** type value (0x0003–0x7FFF) and MU = 0 is an F36
violation ("emitting one is a violation whatever its MU bit"), detector
*verifier*. A compactor must read that type field to decide the record's §20.4
disposition. A compactor that recognises 0x0003–0x7FFF as reserved has detected
an F36 violation; the record is PE = 1 by its stored flags in the ordinary case,
so no drop is licensed, so it MUST refuse. A compactor that does not check the
range carries it forward. Same input, two outcomes. I mention this rather than
file it separately because the governing sentence is the same one.

**What an implementer does wrong without this.** Either they ship a compactor
that refuses inputs the document says it can compact, or they ship one that
emits an output the document says it MUST NOT emit. There is no way to satisfy
both sentences on this input.

**Byte-level: yes.** Compactor A produces no file; Compactor B produces a
specific file. That is a disagreement about actual bytes on disk from the same
input, between two implementations each of which can quote §20.5 for its
behaviour. I note honestly that it is not a *verifier verdict* fork on a single
file — no verifier certifies either the input or B's output, both being
nonconforming — so if the gate's bar is "two verifiers, one certificate", this
sits just outside it. Under the byte-level test as stated ("which byte sequences
a conforming implementation may **emit**"), it is inside.

---

### adversary-02 — AMBIGUITY — §20.4, the MU = 0 / PE = 0 drop licence

**"Modifying any layer's record" does not say whether a re-pointed extent slot
counts, and the carve-out that would settle it is stated for one named operation
only.**

§20.4's table, MU = 0 / PE = 0 row:

> An appender may drop it only in a commit that *independently* changes the scope
> the record attaches to: for a layer sub-record, that layer's record, the entry
> set of its index, or which of its tiles are stored; for a top-level record, the
> file's layer set — which a commit changes by adding or removing a layer and
> equally by modifying any layer's record — or another *non-layer* top-level
> record. Superseding a stored tile's bytes is not such a change for either kind
> — it re-places that layer's index region (§20.3, `[R-WRT-04]`) without altering
> the scope any record attaches to — so a commit whose only change is a supersede
> MUST retain the record.

**The construction.** Start from `probe.tarn`. It carries a top-level record of
type `0x8000` (experimental), MU = 0, PE = 0, `inline_length = 0`, extent slot
(0, 0) — conforming per §21.6's experimental-MU=0 row. Instruct an appender:
*store layer A's tile at disk ordinal 1* (currently the sentinel), leaving
geometry, `entry_count`, and every declaration untouched.

Per §20.3 step 4, layer A's tile-index region is re-emitted in full "necessarily
at a new placement (`[R-LIF-01]`)", so layer A's record's **extent slot** changes
value in the new directory. Its inline payload does not change: `entry_count`
is still 4, `crc_of_crc_array` changes because the segment CRC changed — so in
fact both the slot and the payload differ from the input's bytes.

- **Appender X** reads "the file's layer set — which a commit changes by … and
  equally by modifying any layer's record". Layer A's record in the new directory
  is not byte-identical to the input's; §20.4's own opening paragraph defines
  retention as re-emitting "byte-identically — header, inline payload, and extent
  slot", so a record that is not byte-identical was modified. Therefore the file's
  layer set changed, the licence applies, and X **drops the `0x8000` record**. Its
  output directory is 24 bytes shorter and its extents differ throughout.
- **Appender Y** reads the carve-out: superseding a tile's bytes "re-places that
  layer's index region … **without altering the scope any record attaches to**".
  Storing a previously-unstored tile re-places the index region in exactly the
  same way, so by parity it too alters no record's scope, and Y **retains** the
  record.

Both outputs are conforming files; a verifier certifies both, because no single
file witnesses a preservation violation (§21.7: the preservation obligations "are
properties of a file's history, which §9.7 does not reconstruct"). The two output
byte sequences differ.

**The permitted readings.** (a) "Modifying any layer's record" means any byte
change to the record, including the extent-slot re-point that an index
re-emission forces. (b) It means a *logical* modification of the record's
declarations — a rename, a fill change, a slab clear, a geometry change — with
extent-slot re-points and `crc_of_crc_array` refreshes excluded as bookkeeping.

**Which I picked, and why.** (b). Three things push that way, none of them
stated: the supersede carve-out would be self-contradictory under (a), since a
supersede also re-points the slot; §20.4's opening says "retains and does not
**logically** modify"; and §20.3 step 4 uses "a layer whose record alone changes"
as a category distinct from "a layer whose stored-tile set or index content this
commit changes", implying the latter is not a record change. But (b) requires an
implementer to generalise a carve-out the document states for one named operation
("Superseding a stored tile's bytes"), and to notice that §20.4's "logically"
is load-bearing. Reading (a) is the literal one and is what a careful implementer
who has not made the parity argument will land on.

**What an implementer does wrong without this.** They silently discard a
third-party tool's ancillary state on a commit that only added a tile — the exact
failure §20.4's "An updater that drops such a record SHOULD report the loss;
unreported, application state disappears with no diagnostic" is written to
prevent. Note also that under reading (b) the boundary is razor-thin and
unstated: growing an extent *within* the same grid counts (it changes
`entry_count`? no — it changes the dimension extent field, so it is a logical
record change and the licence applies), while storing a tile does not. Two
operations that look identical to a caller land on opposite sides.

**Byte-level: yes.** Appender X and Appender Y, given the same input file and the
same instruction, emit different byte sequences — X's output omits 24 bytes of
record and every subsequent structure lies at a different offset. I note the
limitation honestly: no verifier can adjudicate between them from either output
alone, so this forks emission, not acceptance.

---

### adversary-03 — CONTRADICTION — §11.1 Rationale vs §20.3 step 4

**The shrink bar is quantified over the wrong generation's stored-tile set in
§11.1.**

§11.1, Rationale:

> §20.3 states normatively, and governs, what a commit may do to a layer that
> already stores tiles: a shrink is barred wherever it alters what §14 fixes for
> a tile the new state still stores, and permitted where it drops tiles out of
> the addressed set, whose extents then become slack.

§20.3 step 4:

> An extent MAY also **shrink**, and the bar above is the whole of the test, **in
> the bar's own tense**: a shrink is permitted exactly where it alters nothing
> §14 fixes for any tile the layer stores in the generation this commit
> supersedes. … Unstoring that tile in the same commit does not rescue it either,
> and for the same reason: the quantifier is the superseded generation's, so a
> shrink that turns real positions into padding of a tile stored there is barred
> whether or not the new state still stores it.

The two range over different sets. §11.1 says the bar reaches tiles **the new
state still stores**; §20.3 says it reaches tiles **the superseded generation
stores**, and names the exact case where they differ ("whether or not the new
state still stores it") to rule §11.1's version out.

**The construction that separates them.** Layer with E=100, T=32, G=4, all four
tiles stored, one uint16 channel with fill `0xABCD`. Generation g. Commit to
g+1: shrink E to 90 — G is still ⌈90/32⌉ = 3… no: G falls from 4 to 3, and tile 2
(covering 64–95) now has positions 90–95 as padding, which under `[R-SER-05]`
must hold `CD AB` and do not, since they were real data in g. In the same commit,
write tile 2's index entry as the sentinel and de-address tile 3.

- Under §20.3 the commit is **barred**: tile 2 is stored in the generation this
  commit supersedes, and the shrink alters what §14 fixes for its stored bytes.
  The writer must produce a new layer or a whole-file rewrite.
- Under §11.1 the commit is **permitted**: the new state stores no tile at all,
  so there is no "tile the new state still stores" for the bar to reach.

**Which I picked.** §20.3, without hesitation: §11.1's own sentence concedes it
("§20.3 states normatively, and **governs**"), §11.1's passage is labelled
*Rationale* and §2.1 makes all Rationale text non-normative, and §21.7 records
the consequence of §20.3's quantifier ("a commit that supersedes every tile it
would have damaged leaves the live state clean, so the bar is unwitnessed
there"), which only makes sense under §20.3's reading.

**What an implementer does wrong without this.** An appender author who reads
§11.1 first — a natural path, since §11.1 is where empty layers and re-declaration
are introduced — implements the new-state quantifier, permits the commit above,
and ships a writer that produces nonconforming stored tiles which no verifier will
ever catch. §21.7 says so in as many words. The damage is real; only the
detection is absent.

**Byte-level: no.** The passage is non-normative and defers explicitly, and in
every case where the two quantifiers differ, §21.7 establishes that the live state
carries no witness, so no verifier's verdict and no reader's output changes. What
changes is which files a writer following the wrong sentence emits — but the
document has already decided which sentence governs, so an implementation that
gets it wrong is wrong, not licensed. I grepped for other occurrences of the old
quantifier: line 1485 is the only one. §20.3's Example (c) and §21.7 both use the
untensed "stores", which §3.1's default ("unqualified *stored* means stored in the
live generation") resolves correctly to the superseded generation at commit time.

---

### adversary-04 — OBSERVATION — §21.5's preamble over-claims completeness for ignore-record

**A user-metadata document a reader declines on resource grounds is a third way
the document can be unreadable, and the preamble's two-way split does not admit
it.**

§21.5:

> User metadata is quarantined (`[R-CNT-25]`): every way its document can be
> unreadable takes this outcome, whatever the containing scope — as a violation
> in the rows below, except at an experimental-range encoding, where no document
> rule attaches and §21.6 records the defined non-violation (`[R-MTA-10]`).

The appositive offers exactly two dispositions for an unreadable document: a
violation registered in R1–R10, or the experimental-encoding non-violation of
§21.6. §18.2 defines a third:

> a reader instead decodes with a bound of its own choosing, no smaller than
> §21.9's user-metadata guarantee, and a document exceeding that bound is
> ignore-record like any other it cannot read.

**The construction.** A conforming file carrying a top-level user-metadata record,
encoding 2, whose zstd frame decodes to 20 MiB of well-formed, sorted-key,
duplicate-free JSON with no non-finite numbers and no oversized keys. §21.9's
guarantee is 16 MiB and "A file exceeding any of these remains conforming". The
document is unreadable to a verifier holding a 16 MiB bound. It matches no R-row:
R3 requires a *decode failure* (the bytes decode fine), R4 a broken frame
constraint, R5–R10 rules over a decoded document the verifier declined to
produce. It is not an experimental encoding, so §21.6's row does not reach it.

- **Verifier P** applies §21.5's preamble literally: the document is unreadable,
  it is not at an experimental encoding, therefore it is "a violation in the rows
  below" — and reports *nonconforming*.
- **Verifier Q** applies `[R-MTA-09]` and reports *cannot establish*, or, with a
  64 MiB bound, decodes it and reports *conforming*.

**Which I picked, and why this is an OBSERVATION and not a defect that forks
bytes.** Q. `[R-MTA-09]` forecloses P in terms: "the bound is that verifier's
capability and not a limit on validity (`[R-CNF-10]`), so the decline is not a
finding that the file is nonconforming and **a verifier MUST NOT report it as
one**." §21.9 independently makes the file conforming, and §21.1's principle —
"where a row and the rule it cites diverge, the rule governs" — applies a fortiori
to a subsection preamble. There is also a rescuing reading of the preamble itself:
"every way its **document** can be unreadable" may be meant file-relative rather
than reader-relative, and a resource decline is a fact about the reader, not the
document — in which case the sentence is simply not about this case.

So the verdict is decided; deciding it costs a reader a trip from §21.5 to §18.2
to §21.9 and back, past a sentence that looks like a completeness claim and reads
as one. That is what makes it an OBSERVATION rather than an ambiguity: it is
decidable, and disproportionately expensive to decide relative to how confident
the preamble sounds.

**Byte-level: no.** `[R-MTA-09]`'s "MUST NOT report it as one" already settles
every verdict, and no reader's returned bytes turn on it.

---

## 5. Ranking of the surviving attacks

By how plausible it is that a real implementation lands on the wrong side:

1. **adversary-01** — high. A compactor author implementing `[R-WRT-09]`'s
   verification depth and `[R-WRT-06]`'s prohibition in the same function has no
   way to also implement `[R-WRT-07]`'s reproduction clause. Whichever they write
   first wins, and both are defensible. This is the one I would fix first.
2. **adversary-02** — medium. The literal reading of "modifying any layer's
   record" is the one an implementer reaches without the parity argument, and
   the failure mode is silent data loss in a third party's records.
3. **adversary-03** — medium-low as a shipping risk, high as a document defect.
   The wrong quantifier is in a Rationale that says §20.3 governs, so a careful
   reader is safe; a reader who meets §11.1 first and never returns is not.
4. **adversary-04** — low. Foreclosed by an explicit MUST NOT two sections away.

## 6. What I could not determine

Nothing that blocked construction. The two places I had to reason rather than
read were both in §20 and both are filed above: whether a compactor that has
classified an index entry may still emit (adversary-01), and whether an index
re-emission counts as modifying a layer's record (adversary-02). Every geometry,
serialization, index, codec, checksum and trailer question I put to the document
came back answered, and every number it states is correct.
