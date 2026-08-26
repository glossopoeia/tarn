# Round 27 — Adversary transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,549 lines — the brief said 4,550; the file has 4,549 newline-terminated
lines, which is the same thing counted differently, and I mention it only
because it is the kind of off-by-one this exercise trains me to notice).
I read it end to end in eight `sed -n` slices, then re-read §7.2, §7.4, §11.1–§11.4,
§14, §15.3, §16, §17.2, §18.2, §19.1–§19.4, §20.3–§20.5, §21.1–§21.9 and
Appendix G several times each.

I ran no tool against any other file. I ran `grep` against that one file
(prefix census, "owning scope" census, analogy census). I ran Python that
reads no files: a CRC-32C implementation, an instance-count script that parses
the register tables out of the spec text, and a byte-shuffle model. Scratch
files live under my own scratchpad `work/` directory. I did not read or list
the round27 output directory. No git, no web, no ADRs, no conformance corpus,
no registry.json.

The path in the brief was exactly where the file is. Nothing to report there.

**Context I did not ask for.** Material appeared in my context before I began:
a project instruction file pointing at `AGENTS.md`, and an index of the
maintainer's private memory files with one-line descriptions naming topics such
as a naming constraint, a working cadence, and how §21 relates to a vector
corpus. I did not open any of it and I have not used any of it. I note its
appearance here because the brief requires it; I am not repeating its contents
beyond what is needed to identify that it appeared. Nothing in this transcript
descends from it: every claim below cites a line of `spec/tarn.md`.

The working method was: (a) verify every number the document states about
itself; (b) walk the thirteen changed passages against the nine shapes in the
brief; (c) build concrete degenerate and boundary files and check them against
the register; (d) enumerate reserved/experimental values in every position;
(e) probe the reader/verifier seam for a file two verifiers could split on.

## 1. Arithmetic and constants — everything the document says about itself

I recomputed every constant and every worked example. All of them hold.

CRC-32C (poly 0x1EDC6F41 reflected = 0x82F63B78, init/final 0xFFFFFFFF):

- `CRC32C("123456789")` = `0xE3069283` — §4.5's check vector. ✓
- `CRC32C(<zero bytes>)` = `0x00000000`. ✓
- CRC over 4 sentinel entries (80 bytes of `FF×16 00×4`) = `0x80A34955`,
  stored `55 49 A3 80` — §7.4's example. ✓
- CRC over that 4-byte array = `0xC4EE982E` — §7.4's `crc_of_crc_array`. ✓
- CRC over 65,536 sentinel entries = `0xEECB3BB2` — §15.4 / Appendix B. ✓
- Appendix A's 128-byte file: I decoded every trailer field and recomputed
  the trailer CRC over bytes [0,60): `0xE00938D2`, matching the stored
  `D2 38 09 E0`. dir region [16,20) = `00 00 00 00` = CRC of zero bytes. ✓

Layout arithmetic:

- §7.4's layer-record payload: offsets 0,4,5,7,9,11,19,27,35,36,38,40,48,56,63,
  68,69,77 with a 4-byte tail = 81 bytes; the prose decomposition
  4 + 34 + 18 + 12 + 13 = 81 checks; the extent length 4·20 + ⌈4/2^16⌉·4 = 84
  checks. ✓
- §11.2's example: G=(4,8), N=32, P=65,536; with E_y = 1000, G_y = 4. ✓
- §11.4's example: s(1,2) = 1·8+2 = 10; in-tile ordinal 44·256+188 = 11,452;
  planar disk ordinal 2·32+10 = 74. ✓
- §14.2's examples: Q=3 → 18 bytes, ordinal 5 at [15,18); planar b = 12 bytes,
  ordinal 5 at 10–11; float32+bool → Q=5, 30 bytes, [25,30). ✓
- §14.3's example: alternating from true at ordinal 0 gives byte 0 = 0x55,
  byte 1 = 0x01 with six pad bits; fill true → 0xFD. ✓
- §14.5's example: extents (5,5), tiles (4,4), tile (1,1) has exactly one real
  position (4,4) and 15 padding positions; 32 bytes with values 1–15 = `CD AB`. ✓
- §15.4's example: 1,000,000 entries → 16 segments (15 full + 16,960),
  64-byte array, region 20,000,064 bytes; entry 999,999 at segment-relative
  byte 339,180; array at [20,000,000, 20,000,064); segment 15 at
  [19,660,800, 20,000,000) = 339,200 bytes; one full segment = 1.25 MiB. ✓
- §15.4's second example: disk ordinal 74 at region bytes [1480,1500);
  channel 3's entries are 96–127. ✓
- §17.3's example: `00 00 80 3F 00 00 00 40 00 00 40 40` with s=4, n=3
  shuffles to `00 00 00 00 00 00 80 00 40 3F 40 40`. ✓
- §21.9's note: 2^32 tiles → 2^16 segments → 256 KiB CRC array; 2^36 → 4 MiB;
  65,536 layers at ~200 bytes/record ≈ 12.5 MiB. ✓
- §5.1's 128-byte floor: dir_offset ≥ 16 and dir_length ≥ 4 force
  F − 64 ≥ 20, so F ≥ 84, and F ≡ 0 (mod 64) forces F ≥ 128. ✓

Register counts. I parsed the four register tables mechanically and counted
instance cells (a cell reading `—` counts 1; otherwise semicolon-separated):

- §21.2: 36 rows (F1–F36) — matches "36 conditions". ✓
- §21.3: 49 rows (L1–L49) — matches. ✓
- §21.4: 26 rows (T1–T26) — matches. ✓
- §21.5: 10 rows (R1–R10) — matches. ✓
- Total 121 rows, **277 instances** — matches §21.8's "121 conditions over
  277 instances" exactly. ✓

I then spot-audited ~30 instance cells against §21.1's stated axes (layout
variation; two directions for *differs from* / *does not equal*, one for
*exceeds*; no direction for a checksum or constant comparison; a homogeneous
family as one instance). Every one I checked is consistent: T21 = 1 direction ×
3 layouts = 3; T22/T14/T3 = 2 × 3 = 6; L44 = 1 × 3 = 3; L21 = 2 layouts × 2
directions = 4; L30 = 2; F17 = 2; F13 = 1; F26 = 1 (bits 2–15 as a family)
against F28 = 2 (MU and PE are materially different); L33 = 4 and L34 = 4
because §11.4 and §12.2 each state *two* reserved sub-ranges, while L31/L43/L45
= 3 because those spaces state one; L36 = 2 because channel layout has no
experimental range; R4 = 8 frame constraints × 2 containers = 16. I could not
find a miscount.

§2.2's prefix table. I grepped every `R-XXX-NN` identifier in the document:
19 distinct prefixes are used (CNF CNT COD ENC ERR EXT GEO IDX LIF MDL MTA PRV
RDR SEC SER SLB TYP VEC WRT). §2.2's table lists exactly those 19, and each
expansion matches the title of the section that owns the identifiers. The
"presentation change alone" claim holds: no prefix is added, dropped, or
re-expanded, and `[R-ENC-100]` still appears as the numbering example.

## 2. The thirteen changed passages, against the nine shapes

### §2.3 — [R-CNF-13] reach, and §21.2's derivation

[R-CNF-13] defines *reach* per condition and claims "`[R-CNT-06]` states ten, of
which the trailer magic and the trailer CRC assert invariants `[R-CNT-24]`
fixes and the other eight do not." I counted the §21.2 rows whose **Governing
rule** cell names `[R-CNT-06]` first: F8, F9, F10, F11, F12, F13, F14, F15,
F16, F17 — exactly ten, of which F8 and F14 are the magic and the CRC. 2+8=10. ✓

§21.2's preamble then claims the reaching rows are "F8, F14, F6 and both of
F1's instances … and no other row." I derived it independently from
[R-CNT-24]'s four permanent invariants (magic at F−64; version_major and
version_minor at F−56; CRC-32C at F−4 over [F−64, F−4); the front block
constant):

- F6 (front block ≠ constant) — reaches; the block is constant in every major.
- F1 (front block byte-reversed; trailer magic byte-reversed) — both reach.
- F8 (magic), F14 (trailer CRC) — reach.
- F13 (F not a multiple of 64) — does **not** reach: [R-CNT-24] fixes the
  trailer's *position relative to F* and its *size*, not F's alignment.
- F17 (committed_file_length vs transport size) and F15 (reserved bytes zero)
  — do not reach; both fields lie inside the 48 bytes a future major may
  redefine. The §2.3 Note says exactly this for F15.
- F19 (incompat lane) — does not reach; flags are inside the 48.
- F5 — does not reach, and the Note explains why (the 128 floor is derived
  from major-1 minimums).
- F18 — outside the premise (version_major = 0 declares no major).

I could not construct a row that reaches and is not on the list, nor one on
the list that does not reach. **Foreclosed.**

I checked shape 9 against [R-CNF-13] specifically, since it defines its object
tightly ("one malformed state, as §21.1 individuates them, and not the
requirement that defines it"). The obvious severance — [R-CNT-04]'s residency
exemption sitting on the other side of that definition — is closed in the same
paragraph: "an exemption the condition's governing requirement grants on a
ground other than the declared major applies unchanged, `[R-CNT-04]`'s
residency exemption among them". **Foreclosed.**

### §4.2 — the value domain and [R-ENC-04]'s designation rule

I enumerated every field of every structure and asked what fixes each width and
each domain.

- Every byte-length field is `u64` except the three the sentence names as
  exceptions (`inline_length` u32; name and fill length prefixes u8). I found
  no fourth.
- The sentence deliberately does **not** claim every *count* is u64, which is
  correct: rank d is u8 and channel count C is u16. If it had said "count" in
  that first sentence it would be false; it says "byte length".
- The 0…2^63−1 domain reaches "every offset, length, extent, and count".
  `file_id` is correctly excluded (it is an identifier; §6.2 constrains it only
  as ≠ 0, and Appendix G item 2 derives it from a hash, which can set bit 63).
  `A` and `A_slab` are excluded and separately bounded at 2^62 by §7.4's table.
  The sentinel is exempted by [R-IDX-02]. Consistent.
- [R-ENC-04]'s parenthetical names "ordinals" as a designated kind, but no
  section expressly designates an ordinal. This is harmless: L2's instance
  cell says "C·N (which dominates the max disk ordinal (C−1)·N + (N−1))", and
  (C−1)·N + (N−1) = C·N − 1, so the designated product dominates every ordinal.
  Same for in-tile ordinals ≤ P−1 and spatial ordinals ≤ N−1. I checked
  ⌈P/8⌉ ≤ P and Q = Σ Bᵢ ≤ 65,535·8, neither of which can overflow. So the
  designated set is complete by domination. **No obligation gap.**

### §6.2 — the pre-trailer gap

The new text says "a longer gap is conforming, and no conforming commit
produces one", and §2.3 names it as one of two writer obligations expressly
declared not to be file-conformance violations. I built the attack: a file
whose directory ends at 100 and whose trailer sits at 1024 (F = 1088), leaving
a 924-byte pre-trailer gap. Verifier A certifies (the gap is slack, no
structure in it, [R-CNT-05] satisfied); verifier B has no rule to reject on.
Both agree. §21.2 correctly carries no row for it, and §21.7 correctly does not
list it among unwitnessed obligations (it is not a violation at all).
**Foreclosed, and stated twice.**

I also confirmed the ordered validation of [R-CNT-06] covers all eleven trailer
fields with no field left unchecked, and that the order (magic, CRC, version
gate, then the eight remaining gates) is a MUST rather than an asserted fact —
shape 4's test. It is: "A reader MUST validate, in order".

### §7.2 / §7.4 — record framing, extent slots, ownership

I enumerated every overlap topology and matched each to a row:

| overlap | outcome | row |
|---|---|---|
| two stored extents, same layer | reject-layer | L18 |
| stored extent × its own layer's index region | reject-layer | L18 |
| stored extent × its own layer's sub-record extent | reject-layer | L18 |
| any structure × a structure of another layer | reject-file | F33 |
| layer structure × directory / trailer / top-level extent | reject-file | F33 |
| two non-layer structures | reject-file | F33 |
| claimant reaching [0,16) or [F−64,F) | bounds rows | F9/F10/F30/F31/F32/L15–L17/T8/T9 |

F33's cell handles the one case I expected to fall through — a slot of (0, N)
with N nonzero, which reaches the front block through a *zero offset* rather
than an out-of-range one — by routing it to the half-zero rows F30/L15 rather
than F31/L16. That is exactly the seam I was hunting; it is closed in the row
text. I also constructed a top-level user-metadata record whose extent slot
*equals* the directory region: its terminal CRC then verifies (it is the
directory CRC), the "document" is the raw record sequence, and R7 makes it
ignore-record — while F33 makes the file nonconforming. No reader/verifier
divergence beyond the one the document declares (readers are not obliged to
detect overlap).

Zero-length structures: dir_length ≥ 4; a record extent with one half zero is
an error; a non-sentinel entry with length 0 is T10. There is no conforming
zero-length structure, so the partition in §5.2 has no degenerate member.

### §11.2 / §11.3 — grid arithmetic and padding

Shape 8, applied to [R-GEO-04]: "Where Eᵢ mod Tᵢ ≠ 0 … the tiles at the high
edge of dimension i contain padding positions". I tested Eᵢ = 0 (no padding,
G = 0, no addressed tiles — consistent with §11.1 and §11.2), Eᵢ = 0 with
Tᵢ large (same), 0 < Eᵢ < Tᵢ (Gᵢ = 1, single padded tile), Eᵢ = Tᵢ (no
padding), Eᵢ = 5 / Tᵢ = 4 (three padding positions in the last tile). The
stated equivalence "Eᵢ mod Tᵢ ≠ 0 ⟺ the grid overhangs the extent" is exact
including at Eᵢ = 0, where Gᵢ·Tᵢ = 0 = Eᵢ. **Foreclosed.**

§11.2's ceiling-division form E/T + [E mod T ≠ 0] is correct at E = 0 and
avoids the overflowing idiom the Note names.

### §17.2 — the two designations

[R-COD-04] now says "A **non-sentinel** index entry's length therefore MUST
equal the tile's decoded size". This is the fix for exactly the degenerate case
shape 8 asks for: without it, every sentinel entry (length 2^64−1) would
falsify the rule in every codec-1 sparse layer. I looked for the same defect in
its siblings and found each already qualified: §15.3's rows all carry
"(non-sentinel)" where needed; [R-SLB-01]'s "every stored tile" and
[R-SLB-03]'s packing relation are qualified by §15.3's general sentence that
structurally-bad entries "contribute no stored extent to the *verifier* rows";
§9.7 repeats it for the coverage walk; [R-WRT-07] repeats it for regeneration.

[R-COD-07]'s cap is quantified over **addressed** tiles, and the Note derives
the escape condition correctly: addressed-tile count = N or C·N with C ≥ 1, so
it is 0 iff some Gᵢ = 0 iff some Eᵢ = 0. "any dimension extent 0" is exactly
the escape, not a superset. I built the attack file — a zero-extent layer
declaring codec 4 with T = (2^40, 2^20), decoded size 2^60, far past
0x7E000000 — and it is conforming, deliberately, and the Note says so, and
§20.3 closes the growth path ("provided the grown geometry stays within every
bound … `[R-COD-07]`'s lz4 decoded-size cap among them (L44)"). The Note also
correctly says [R-ENC-04] carries no such quantifier, so P·Q and P·Bᶜ are
still checked in the empty layer. **Foreclosed.**

### §20.3 — the grow/shrink bar

This is the passage I attacked hardest, because it is where the quantifier
question of shape 1 lives ("permission and consequence quantified over
different generations").

Attack 1 — *a single commit that grows one axis and shrinks another.* Layer
with G = (2,3), N = 6. Commit grows E₀ so G₀ = 3 and shrinks E₁ so G₁ = 2.
entry_count is unchanged at 6, but disk ordinals renumber: tile (1,0) moves
from s = 3 to s = 2. Does anything oblige the index to be re-emitted? Yes —
step 4 keys the obligation to "stored-tile set **or index content**", not to
entry_count, and index content changes. The rule is keyed to the quantity that
decides it. **Foreclosed** (this was my best candidate for shape 6 and it
failed).

Attack 2 — *the §11.1 Rationale's claim that "Growth that leaves entry_count
unchanged touches the directory alone".* Under growth only, each Gᵢ is
non-decreasing, so ∏Gᵢ fixed forces every Gᵢ fixed **unless** the product is 0,
and the Rationale names that case explicitly ("a growth raising one grid count
⌈Eᵢ / Tᵢ⌉ while another stays 0 among them, the product holding at 0"). With
all Gᵢ fixed, ordinals do not move and the stored bytes do not change — the
newly-real positions already held fill, which §20.3 licenses. Correct.

Attack 3 — *a channel-type change that alters nothing on the enumerated list.*
int8 → bool on an interleaved layer: element size 1 either way, so decoded
size, byte offsets, padding set, padding content (fill byte 0x00 stays 0x00),
codec and filter are all unchanged — none of the four named items moves. But
[R-SER-08] now fixes every one of that channel's stored value bytes to
{0x00, 0x01}, which it did not before. Does the bar catch it? Only through the
general clause, and the rule says the general clause governs: "the list names
where that effect arises rather than standing on its own". So it is barred.
And even under the narrow reading the resulting file is nonconforming (T2), so
[R-CNF-05] bars emission under both readings and the emittable set does not
move. **Foreclosed, and not byte-level even if it were not.**

Attack 4 — *adding or inserting a channel on a planar layer that stores tiles.*
Permitted by the bar (each plane's decoded size, offsets and padding are
untouched); entry_count changes; ordinals renumber where insertion is not at
the end; step 4 obliges full index re-emission with entries at their new
disk-ordinal positions. Coherent.

Attack 5 — *de-addressing versus damaging.* The two sentences
"Dropping a tile out of the addressed set … is not itself such an alteration"
and "a shrink that alters what §14 fixes for a tile stored there is barred
whether or not the new state still stores it" look like they pull apart. They
do not: de-addressing is stipulated not to be an alteration, so it cannot be
the thing the second sentence bars; the second sentence bars a shrink that
*also* changes padding content for a tile stored in the superseded generation,
and denies the rescue of unstoring it in the same breath. A tile that is
de-addressed has no positions in the new geometry, so it cannot acquire new
padding positions. The two are consistent. **Foreclosed.**

Attack 6 — *changing a declared alignment.* Permitted by the bar, and caught by
the sentence "an aligned layer's stored tiles — every one the new state keeps,
not only those this commit adds — satisfy its invariant or the declaration is
cleared". The parenthetical is the quantifier that makes it correct; without it
a writer could raise A from 512 to 4096 and claim only the new tiles must obey.

### §21.2, §22.2

§21.2's preamble is audited above. §22.2's "Three properties" is a closed count
and there are exactly three (declaration-derived decode size; overflow-checked
designated quantities; nothing acted on before its checksum), followed by a
separate MUST. Its supporting claim "no codec's embedded size field is ever an
allocation source" holds across all four codecs (deflate has none; zstd's FCS
is barred as an allocation source by [R-COD-06]; lz4 takes the decoded size as
output capacity by [R-COD-07]; codec 1 has no field). Its example "a layer can
declare 2^63 − 1 addressed tiles" is about a hostile, nonconforming file — such
a layer is rejected at layer access by L2, since entry_count × 20 overflows —
and the sentence's point (do not walk in proportion to it) is exactly right.

## 3. Systematic enumerations that found nothing

**Reserved and experimental values, in every position, in every MU/PE
combination.** I walked all eight spaces of §10.2 in both containers:

- top-level record: experimental + MU=0 → conforming, ignored (§21.6);
  experimental + MU=1 → conforming, reader rejects the file (§21.6 names it as
  one of the two "conforming files a reader nevertheless refuses");
  reserved + MU=0 → F36 (verifier); reserved + MU=1 → F35, specialization of
  F36 per §21.1.
- layer sub-record: experimental + MU=1 → reject-layer, file conforming, and
  §21.6's prose says exactly that ("the same type as a layer sub-record is
  reject-layer and never a ground to refuse the file"); reserved → L24/L25.
- layout 3–255 → L36 (no experimental range exists, matching §10.2).
- linearization, sample type, codec, filter, index encoding → L33, L34, L43,
  L45, L31, each covering 0, reserved and experimental.
- metadata encoding: 0 and 3–0x7F → R1 (violation, ignore-record);
  ≥ 0x80 → §21.6 non-violation, ignore-record, verifier certifies and reports.

§10.3's routing list ("§11.4, §12.2, §14.1, §15.1, §17.2, and §17.3", plus
record types, plus §18.2) covers all eight spaces with no gap and no double
assignment.

I then checked §20.5's closed count: "the two of §10.1's four vehicles §21.6
makes conforming, the other two reaching such a file only as values this text
still registers as reserved-range violations — F36 and L25 for a record type,
and one row for each of the other seven spaces §10.2 tabulates (L31, L33, L34,
L36, L43, L45, R1)". Seven non-record-type spaces, seven rows, bijective. And
the citation of F36/L25 rather than F35/L24 is *right*, not sloppy: [R-WRT-06]
makes a compactor refuse any record of an unimplemented type with MU = 1, so
the MU-gated specializations cannot arise in a compactor's output. That is the
kind of care that told me this passage had been worked over.

**The degenerate-but-legal file.** I built, byte by byte:

- Appendix A's 128-byte empty file — verified field by field and by CRC.
- The smallest file carrying a layer: front [0,16); a layer record with name
  "a", one dimension "x" with E = 0, T = 1, one uint8 channel "c",
  entry_count = 0, extent slot (0,0), crc_of_crc_array = 0. Inline payload is
  2+1+2+2+2+8+8+8+1+2 + 18 + 6 + 1+8+4 = 73 bytes; record = 97;
  directory = 101 at dir_offset 16, ending at 117; trailer at 128; F = 192,
  pre-trailer pad 11 bytes. Conforming.
- The smallest file with one *stored* tile: tile at [16,17) (uint8, E=T=1,
  P=1, Q=1, codec 1 → length must be exactly 1); index region at [17,41)
  (1·20 + 1·4); directory at [41,142); trailer at 192; F = 256. Conforming.
  Note the tile must precede the directory or [R-CNT-05]/F7 fires.
- A file whose directory ends exactly at F−64 (zero pre-trailer pad) —
  conforming, and §6.2 says so.

None of these produced a split verdict.

**The reader/verifier seam.** I looked for a file two *verifiers* could split
on, which is the charter. The candidates all collapsed:

- Slack total. Deterministic where the walk completes. Where it does not,
  §5.2 and §9.7 between them fix which claimants are discarded (a rejected
  layer's, including ones the walk itself had already enumerated when the walk
  established the rejection) and oblige the verifier to say what stopped it.
  A tile-crc failure does *not* make the total partial (§15.3: the entry
  "keeps its place … in the coverage walk"); a structurally-bad entry does
  not either (§9.7 says so in terms). Two verifiers agree.
- *cannot establish* vs *nonconforming*. §2.3 fixes priority ("An established
  violation takes priority"). [R-COD-11]'s codec-inability ground turns out to
  be vacuous for a *conforming* verifier — every assigned codec is core, and
  an unassigned value is itself a violation — and §17.4 says so. The live
  ground is the resource decline of [R-ERR-04] / [R-MTA-09], and both are
  explicitly the actor's capability rather than a fact about the file.
- The metadata content-size mismatch (R4) versus decode failure (R3): a strict
  RFC 8878 decoder given a single-segment frame with a wrong FCS errors out,
  which looks like R3 while §18.2 routes it to R4. Both are ignore-record and
  both make the file nonconforming, so no verdict splits — only the row cited
  in a report.
- Duplicate layer names whose names are also individually invalid: §19.1 step 4
  fixes the order ("Uniqueness is decided first"), so F4/reject-file wins over
  L5/L6/reject-layer rather than being a race.

## 4. Findings

I found nothing that forks the bytes. Three defects survive, all in text that
cannot move the emittable set; I grade them as they are.

---

### adversary-01 — CONTRADICTION — Appendix G item 5

**Location.** Appendix G, item 5 (Reproducible-writer profile, non-normative);
the rule it glosses is §17.3 `[R-COD-10]`.

**Quotation (the text complained about).**

> The filter is the identity exactly where its permutation is — where the
> stride is 1, as for a packed boolean plane, and equally where the decoded
> image is a single group, n = L/s being 1 (`[R-COD-10]`); elsewhere it changes
> the stored bytes of every tile it touches.

**Counter-citation.** §17.3 `[R-COD-10]`:

> Viewing the image as n = L/s consecutive groups of s bytes, the filtered
> image places byte i of group j at offset i · n + j … Length is unchanged.

**The defect.** The first half of the sentence is exactly right, and I verified
it: the map i·n + j ↦ j·s + i is the identity iff s = 1 or n = 1 (take i = 0,
j = 1: the image byte moves from offset 1 to offset s, so any s ≥ 2 with n ≥ 2
is a non-identity permutation). The trailing universal is false. A permutation
of bytes is the identity *on an image* whenever that image is invariant under
it — in particular whenever every byte of the decoded image is equal. Such a
tile is legal and stored.

Worked counterexample. An interleaved layer, one `uint16` channel `v`, fill
`0x0001`, tile extents chosen so the layer has no padding position (Eᵢ a
multiple of Tᵢ), T = (2) so P = 2, Q = 2, decoded size 4. A tile whose two
samples are both `0x0000`:

```
decoded image : 00 00 00 00      (s = Q = 2, n = L/s = 2)
filtered (s=2): 00 00 00 00      identical
```

The samples are `0x0000`, the fill is `0x0001`, so item 6 of the profile does
*not* replace the tile with a sentinel — it is genuinely stored. Filter 1 and
filter 2 produce byte-identical stored bytes for it, with s = 2 and n = 2,
which is squarely inside the "elsewhere". I confirmed the same for P = 8
(n = 8). Nothing about this is contrived: an all-zero tile in a layer whose
fill is not zero is the ordinary case, and `[R-TYP-10]` explicitly contemplates
a writer whose caller chooses a non-zero fill.

**Permitted readings and which I picked.** There is only one reading of
"changes the stored bytes of every tile it touches", and it is false. I read
the sentence as making a claim about bytes because that is what the profile is
about; a reading on which it means "changes the rule for the stored bytes" is
not available, since the rule changes for every tile including the s = 1 ones.

**What an implementer does wrong without it.** Nothing structural — the
profile's conclusion (pin the filter value) stands regardless, since the choice
does matter for tiles with non-uniform images. What it costs is a reader of
Appendix G who takes the sentence as licence to *detect* the filter value from
stored bytes, or who builds a profile-conformance checker that flags "filter 2
declared but tile bytes unchanged" as a profile violation. That checker would
reject reproducible files.

**Byte-level: no.** Appendix G is labelled non-normative in its heading and
says of itself "It adds no requirement to any actor: a writer ignoring it is
fully conforming". No conforming file's status changes on either reading, and
`[R-CNF-05]` already licenses both filter values for the same input.

---

### adversary-02 — AMBIGUITY — Appendix G item 3

**Location.** Appendix G, item 3 (non-normative), the placement sentence.

**Quotation.**

> The first structure begins at 16, directly after the front signature block,
> which §5.2 counts as no structure — or, where a declared alignment admits no
> structure at 16, at the least position above it the declaration admits; each
> later structure begins where the previous one ended, save where alignment
> forces a gap — a declared A or A_slab, or §6.2's 64-byte trailer alignment,
> the pre-trailer pad included — and every byte of every such gap is zero —
> `[R-CNT-03]`'s advice, taken as a requirement here: order alone does not fix
> bytes while the space between structures is free in either extent or content.

**The two readings.** The sentence has two clauses that create gaps: the
*leading* gap, from offset 16 to wherever a declared alignment first admits a
structure, and the *interior* gaps forced by alignment between consecutive
structures. "every byte of every such gap is zero" then reads either:

(a) over both kinds of gap — the intended reading, I believe; or
(b) over only the interior gaps, because the nearest antecedent of "such gap"
is "a gap [that] alignment forces" in the *later*-structure clause, and the
closing gloss says "the space **between structures** is free", which the
leading run is not — the front signature block is stipulated in the same
sentence to be no structure, so [16, first_offset) lies between a non-structure
and a structure.

**Which I picked and why.** (a), because the item's purpose is to close every
degree of freedom and (b) would leave one open. But (b) is defensible on the
words, and the sentence itself supplies the argument for it by insisting the
front block is not a structure.

**Reachability.** The leading gap is nonempty whenever the first layer in
ascending name order has a stored tile and declares A ≥ 512, or declares
A_slab > 16. With A_slab = 4096 the leading gap is bytes [16, 4096) — 4,080
bytes. Under reading (b) two writers both claiming the profile emit different
files, which is the one thing the profile exists to prevent.

**What an implementer does wrong without it.** A profile adopter that leaves
the leading run uninitialised produces a file byte-different from another
adopter's, and — worse — one whose difference is invisible to every check in
the document, since slack content is constrained by nothing (`[R-CNT-03]`,
`[R-SEC-04]`).

**Byte-level: no.** Non-normative appendix; both readings produce conforming
files, and the disputed bytes are slack, which `[R-CNT-21]` puts outside every
conformance requirement.

---

### adversary-03 — AMBIGUITY — §18.2 [R-MTA-10] vs §21.6 / §22.3 [R-SEC-04]

**Location.** §18.2 `[R-MTA-10]`; §21.6's table row for an experimental-range
document encoding; §22.3 `[R-SEC-04]`; Appendix H's verifier checklist.

**Quotation.** §18.2 `[R-MTA-10]`:

> A verifier meeting such a record in an otherwise conforming file has no
> requirement it is unable to check — the record is not among `[R-CNF-11]`'s
> cannot-establish grounds, and certification is unaffected — and it MUST
> report each record it ignored on this ground, naming the owning scope, the
> encoding value, and the stored extent length, as it reports the slack total
> (`[R-CNT-21]`): bytes a certificate covers without inspecting are counted and
> named, never silent.

**The two readings.** "such a record" and "on this ground" are anchored two
sentences earlier to "an encoding this specification does not assign", which
by §10.2 and §18.2 means encoding 0, the reserved range 3–0x7F, **and** the
experimental range ≥ 0x80.

(a) The MUST ranges over every unassigned encoding. §22.3 `[R-SEC-04]` reads it
that way in terms: "the extent of a user-metadata record **under an unassigned
encoding** is covered by its terminal CRC but constrained by no content rule
(`[R-MTA-10]`) … which is why `[R-MTA-10]` makes the verifier's report name
each such record".

(b) The MUST ranges only over the experimental range, because the sentence's
subject is qualified "in an **otherwise conforming** file", and encoding 0 or a
reserved value is itself a violation (R1, `[R-MTA-03]`), so such a file is
never otherwise conforming. §21.6's table states the duty only for the
experimental row ("No document rule attaches at such an encoding, so a verifier
certifies, reporting the record it ignored"), and Appendix H states it only for
the experimental case, adding "encoding 0 and the reserved range stay
violations (R1)".

**Which I picked and why.** (b), on the strength of the "otherwise conforming"
qualifier, which is doing grammatical work in the very sentence that carries
the MUST. But (a) is what §22.3 says, and §22.3's rationale — a certificate
covering bytes it never inspected — is a reason that applies to a reserved
encoding as much as to an experimental one, since neither is decoded.

**What an implementer does wrong without it.** A verifier built on (b) omits
the scope/encoding/extent-length report line for an encoding-0 or reserved-
encoding record. It still reports *nonconforming* and still names R1, so an
operator who filters on the "record ignored, extent length N" line — the
policy §22.3 recommends ("an operator who wants no such bytes rejects on that
report line") — misses those records. Two conformance-checking harnesses would
disagree about whether a report is complete.

**Byte-level: no.** This governs a verifier's *report*, not its verdict and not
what a writer may emit. Under both readings the file's conformance and the
verdict are identical.

---

## 5. What I could not determine

- I could not tell from the document alone which sentence was deleted from a
  section preamble. §16 (Slabs and Alignment) is the only structure-defining
  section whose preamble carries no owning-scope statement; if that is where
  the deletion landed, nothing is lost, because `[R-CNT-23]` puts the alignment
  and slab *declarations* at layer scope through the layer record's inline
  payload, and `[R-SLB-01]`/`[R-SLB-03]` each assign reject-layer expressly for
  the *invariant*. I checked every other structure against `[R-CNF-08]`'s
  claim that each has exactly one owning scope stated where it is defined, and
  the only marginal case is the extent of a record of a type this
  specification has not assigned — which `[R-CNT-13]` scopes by the record's
  governing scope rather than by a definition of its own, which is the only
  thing available for a structure this document does not define.
- I could not tell which register preamble lost a precedence claim. I audited
  precedence coverage instead, by enumerating the cases where two rows of
  different scopes bear on one file (duplicate-and-invalid layer names;
  malformed slot versus overlap; a (0,0) extent on a user-metadata record;
  quarantine versus owning scope; the tile-crc row versus the layer's index
  chain). Every one is decided somewhere — §19.1 step 4, `[R-CNT-23]`'s
  "except where another rule assigns a different scope", §15.3's
  "notwithstanding", §21.1's "where a row and the rule it cites diverge, the
  rule governs", and §21.1's specialization list. I found no case left open.
- §21.9's "The first five rows range over declarations, which every file and
  every layer carries" is loose for a zero-layer file, which carries no rank,
  no channel count and no entry_count. I judged this to be distributive
  phrasing rather than a defect — the per-file rows range over every file and
  the per-layer rows over every layer — and the paragraph's own conclusion
  ("a file containing no instance of a kind does not exceed that row") settles
  the degenerate case anyway. I am recording the judgement rather than the
  finding, because I could not make it bite.

## 6. Honest summary of the attack surface I covered and what forecloses it

Boundary values: entry_count 0 / 1 / 2^16 / 2^16+1 / 2^32 / 2^63−1 (the last
rejected at L2 through the region-length product); E = 0 and E < T and E = T;
P = 1 and P mod 8 ≠ 0; dir_length 4 / 5 / 27; extent_length 0 / 4 / 5;
offsets 0 / 15 / 16 / F−64 / F−63; A = 0 / 256 / 512 / 2^62 / 2^63;
A_slab = 0 / 1 / 2^62; S = 0 / 1 / N / 2^63−1; rank 0 / 1 / 255;
C 0 / 1 / 65,535. Every one lands on a stated row or a stated permission.

Two structures claiming the same bytes: exhausted above, all seven topologies.
A structure outside the file: T9, L17, F32, F10 by tier. A zero-length
structure: unrepresentable.

Records, codecs, flags and enums from every reserved, unknown and experimental
range, in both containers, across all four MU/PE combinations: exhausted above.

The reader/verifier seam: the document declares it (a reader is never obliged
to detect overlap, coverage, flag bits, padding content, boolean bytes, or
member ordering) and `[R-CNF-12]` licenses a reader to reject anyway, so the
seam is a permission rather than a fork.

Feature interactions: sparse tile under a filter chain (a sentinel has no bytes
to filter; `[R-COD-04]`'s new "non-sentinel" makes the codec-1 case exact);
empty layer under the lz4 cap and under `[R-ENC-04]` (the Note distinguishes
them explicitly); compaction over a record the compactor cannot read
(`[R-WRT-06]` refuses for MU = 1, and `[R-WRT-07]` refuses for a structurally
bad index entry it must regenerate rather than copy); slab continuity across a
structurally-bad entry versus a crc-failing entry (§15.3 and §16.2 both state
the distinction, in the same words).
