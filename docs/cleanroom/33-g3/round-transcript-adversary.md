# Cleanroom round 33 — Adversary transcript

## 0. Access, disclosure, and working files

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,805 lines, 47,853 words, 290,982 bytes). It was where the brief said it would be. I
read it end to end in eight `sed`/`awk` slices, then re-read §2.3, §5.1–§5.2, §6.2–§6.3,
§7.1–§7.4, §9.6–§9.7, §11.1, §13.3, §14.2–§14.5, §15.3–§15.4, §17.2, §18.2, §19.1–§19.4,
§20.3–§20.5, §21.1–§21.9 and Appendices F/G/H repeatedly.

I opened no other file. No ADRs, no `docs/`, no `PLAN.md`, no `conformance/`, no
`registry.json`, no git history, no web. I did not list any directory except my own
scratch directory (which I created) and I did not read the output directory.

Working files, all under
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r33-round/scratch/adversary/`,
all written by me and named so as not to collide:
- `adv_crc.py` — a from-scratch CRC-32C (reflected Castagnoli 0x82F63B78) plus the
  document's own check vectors and three of its stated checksums.
- `count_inst.py` — a mechanical count of §21's register rows and Instances cells.
- `flat.py` / `flat.txt` — a whitespace-normalised, `> `-stripped flattening of the
  document, so that phrase searches survive the hard wrap and blockquote prefixes.
- `srch.py` — phrase search over `flat.txt` with approximate line-number back-mapping.
- `bq.py` — enumerates every blockquote block and reports which carry no
  *Note*/*Example*/*Rationale* label.
- `mustnote.py` — finds BCP-14 keywords inside labelled (non-normative) blocks.

**Context I did not ask for.** My runtime placed a project instruction file (CLAUDE.md,
pointing at AGENTS.md) and an index of the maintainer's memory notes into my context
before I began. The memory index carries entries naming this project's harness, its
lineage gate, its repair habits and its subagent model. I disregarded all of it; I did
not open any file it names, and no conclusion below rests on it. Disclosing that it
appeared, per the brief.

## 1. Method

I treated the document as a byte-format specification and tried to build files that two
conforming verifiers would judge differently. Where I could not, I recorded the sentence
that forecloses the attack. In parallel I re-derived every number the document states
that I could compute without external data, because a specification that gets its own
arithmetic wrong is usually wrong about more than the arithmetic.

The hard wrap and the `> ` blockquote prefix both break line-oriented `grep`, so every
phrase search below ran against `flat.txt` (whitespace normalised, `> ` stripped). I
sanity-checked the flattener by searching for phrases I knew spanned a wrap — e.g.
`"and no other"`, which straddles a line break at §20.3 step 4 and returns 0 hits under
plain `grep` on the raw file and 5 hits under the flattened search. That is the check the
brief asks for before resting anything on a zero.

## 2. Derived numbers, against the document's own figures

### 2.1 Checksums

I implemented CRC-32C from the parameters in §4.5 (polynomial 0x1EDC6F41, reflected
in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) as the reflected table constant
0x82F63B78, and checked it against §4.5's own check vector first.

| Quantity | Computed | Document |
|---|---|---|
| CRC-32C("123456789") | `0xE3069283` | `0xE3069283` (§4.5) |
| CRC-32C(zero bytes) | `0x00000000` | `0x00000000` (§4.5) |
| Appendix A trailer CRC over trailer[0,60) | `0x402F157E`, stored `7E 15 2F 40` | `0x402F157E`, `7E 15 2F 40` (Appendix A) |
| §7.4 example: CRC over 4 sentinel entries (80 bytes) | `0x80A34955`, stored `55 49 A3 80` | same (§7.4) |
| §7.4 example: crc_of_crc_array over those 4 bytes | `0xC4EE982E`, stored `2E 98 EE C4` | same (§7.4) |
| §15.4: CRC of a full 2^16-sentinel segment | `0xEECB3BB2` | `0xEECB3BB2` (§15.4, Appendix B) |

I rebuilt Appendix A's trailer field by field from §6.2's layout table (magic;
version_major=1; version_minor=0; flags=0; dir_offset=16; dir_length=4;
committed_file_length=128; file_id=0x0123456789ABCDEF; 12 zero bytes) and got
`8a4e5241540d0a1a01000000000000001000000000000000040000000000000080000000000000
00efcdab8967452301000000000000000000000000`, which is byte-for-byte the hex dump at
Appendix A offsets [64, 124). Every stated checksum in the document that I could compute
is correct.

### 2.2 The register's own arithmetic

`count_inst.py` parses every `| Fnn |`, `| Lnn |`, `| Tnn |`, `| Rnn |` row of §21.2–§21.5
and counts semicolon-separated instances, treating a cell reading `—` as one instance
(§21.1: "a cell reading — is one instance").

- Rows: F 35, L 49, T 26, R 10 = **120**. §21.2 says 35, §21.3 says 49, §21.4 says 26,
  §21.5 says 10; §21.8 says 120.
- Instances: F 56, L 116, T 55, R 50 = **277**. §21.8 says "120 conditions over 277
  instances".

Exact on both. I also spot-checked §21.1's two stated instance axes against individual
rows: T21 ("larger than", one direction) has 3 instances = the three layout formulas;
T22 ("does not equal", two directions) has 6 = 3 layouts × 2 directions; T14 and T3
likewise 6; L21 4 = 2 layouts × 2 directions; L37/L38 (checksum comparisons, "no
magnitude ordering") 1 each; F17 2 (shorter/longer). R4's 16 instances decompose as
seven frame constraints × two containers, with the content-size constraint contributing
two directions rather than one: 6×2 + 2×2 = 16. All consistent with §21.1's rules.

### 2.3 Other numbers I re-derived

- §7.4's worked layer record: 4 (name) + 34 (nine scalars) + 18 (dimension entry) + 12
  (channel entry) + 13 (trailing fixed) = **81** bytes, matching the stated 81 and the
  offsets in the hex listing (0, 4, 5, 7, 9, 11, 19, 27, 35, 36, 38, 40, 48, 56, 63, 68,
  69, 77). Extent length 4×20 + ⌈4/2^16⌉×4 = **84** ✓.
- §11.2: extents (1024, 2048), tiles (256, 256) → G=(4,8), N=32, P=65,536 ✓. With extent
  1000, G_y = ⌈1000/256⌉ = 4 ✓.
- §11.4: (300, 700) → tile (1,2), s = 1·8+2 = 10 ✓; in-tile (44,188) → 44·256+188 =
  **11,452** ✓; planar C=4, channel 2 → 2·32+10 = **74** ✓.
- §15.4: entry_count 1,000,000 → 16 segments (15 full + 16,960), CRC array 64 bytes,
  region 20,000,064 bytes, entry 999,999 at segment-relative byte 20×16,959 = **339,180**,
  CRC array at [20,000,000, 20,000,064), segment 15 at [19,660,800, 20,000,000) =
  **339,200 bytes** ("~339 KB") ✓; a full segment 65,536×20 = 1,310,720 = **1.25 MiB** ✓.
- §15.4's second example: ordinal 74 → region bytes [1,480, 1,500) ✓; channel 3 of
  C=4, N=32 → entries **96–127** ✓.
- §14.2: tiles (2,3), P=6, uint8+uint16 → Q=3, size 18, ordinal 5 at [15,18) ✓; planar
  uint16 plane 12 bytes, ordinal 5 at 10–11 ✓; float32+bool → Q=5, size 30, ordinal 5 at
  [25,30) ✓.
- §14.3: tiles (2,5), P=10, alternating from true → byte0 = 0x55, byte1 = 0x01, fill-true
  pad → 0xFD ✓.
- §14.5: extents (5,5), tiles (4,4) → grid 2×2, edge tile (1,1) has 1 real + 15 padding
  positions, 32 bytes, values 1–15 = `CD AB` ✓.
- §17.3: shuffle of 1.0f, 2.0f, 3.0f (s=4, n=3) → `00 00 00 00 00 00 80 00 40 3F 40 40` ✓.
- §9.2's Note: dir_offset ≥ prior F, dir_length ≥ 4, dir_offset+dir_length ≤ new F − 64 →
  new F ≥ prior F + 68; both multiples of 64 → new F ≥ prior F + **128** ✓ (the smallest
  multiple of 64 at or above prior F + 68 is prior F + 128, since prior F + 64 < prior F + 68).
- §9.3's Note: largest multiple of 64 at or below 2^63 − 1 is **2^63 − 64** ✓.
- §21.9's Note: segment CRC array at entry_count 2^32 is 2^16 × 4 = 2^18 = **256 KiB** ✓;
  at 2^36 it is 2^20 × 4 = **4 MiB** ✓. 2^32 entries × 20 bytes = 85.9 GB = "tens of
  gigabytes" ✓.
- §5.1 / [R-CNT-27]: front block 16, directory ≥ 4 at offset ≥ 16 (ends ≥ 20), trailer 64
  at a 64-aligned offset → smallest F = **128** ✓; Appendix A's 44-byte pad closes
  20 + 44 = 64 ✓.
- §14.4's Note, at P = 1: planar packed bool is ⌈1/8⌉ = 1 byte, interleaved bool is 1 byte;
  with [R-SER-05] fixing pad bits 1–7 to the fill bit, the images coincide for both values
  exactly when fill is false (fill false: 0x00/0x00 and 0x01/0x01; fill true: 0xFE/0x00 and
  0xFF/0x01) ✓ — the Note's claim is exactly right.
- §17.2's Note on zstd window derivations: RFC 8878's Window_Descriptor cannot express
  below 1 KiB (windowLog floor 10), and with Single_Segment_Flag Window_Size is the frame
  content size, which [R-COD-06] pins to the decoded size. A sub-1-KiB tile is therefore
  encodable under codec 3 only as a single-segment frame, and both derivations agree ✓.
- [R-COD-10]'s divisibility claim: L is divisible by s in every case — planar numeric
  L = P·B^c with s = B^c; interleaved L = P·Q with s = Q; packed bool L = ⌈P/8⌉ with
  s = 1 ✓.
- L2's dominance claims: C·N ≥ (C−1)·N + (N−1) = C·N − 1 ✓; P·Q ≥ P·C because
  Q = ΣB_i ≥ C (every element size ≥ 1) ✓.
- §20.5's "one row for each of the other seven spaces §10.2 tabulates (L31, L33, L34,
  L36, L43, L45, R1)": §10.2 tabulates eight spaces; excluding record type leaves seven —
  index encoding→L31, linearization→L33, sample type→L34, channel layout→L36, codec→L43,
  filter→L45, metadata encoding→R1 ✓. The trailer flag lanes are called a space in §10.2's
  prose but are not tabulated, which is why "tabulates" is the right word ✓.
- §18.2's finiteness test now names roundTiesToEven, which makes the overflow boundary
  exact: under roundTiesToEven a decimal magnitude converts to infinity iff it is at least
  2^1024 − 2^970 (the midpoint between DBL_MAX = 2^1024 − 2^971 and 2^1024; at the midpoint
  ties-to-even selects 2^1024, i.e. overflow). Two conforming readers cannot disagree about
  any decimal literal. This repair works.

Nothing in the arithmetic is wrong. That matters for calibration: the parts of this
document that can be checked mechanically all check.

## 3. Blockquote-label sweep

`bq.py` finds **62** blockquote blocks. Exactly **one** carries no *Note*/*Example*/
*Rationale* label and is therefore normative under [R-CNF-01]: §15.1's tile-index region
layout,

> `[ entry array: entry_count × 20 bytes ] [ segment CRC array: ⌈entry_count / 2^16⌉ × 4 bytes ]`

which is load-bearing (it is the only statement of the region's internal order) and is
consistent with [R-CNT-17]'s length formula and §15.4's segmentation. The brief's warning
("at least one exists") is satisfied by this one and I found no second.

`mustnote.py` finds six labelled blocks carrying BCP-14 keywords. Five are restatements
whose normative anchor I located: §9.2's crash Example restates [R-LIF-05]'s MUST NOT
scan backward; §15.4's Note's "MAY verify each range once and cache" is anchored by
§19.4 step 3's normative "their verifications MAY be cached per §15.4's note"; §18.2's
Note's "MAY instead decline any scope containing the record" is anchored by [R-ERR-04]'s
"It MAY also decline at any scope that contains the narrowest one"; §19.4's Note's
"Readers MAY coalesce" grants nothing not already free; §20.3's Note's "Writers ... SHOULD
batch" is advice with no normative counterpart, but as advice in a Note it binds nothing.
The sixth is §2.1's own discipline Note, which is the subject of finding adversary-03.

## 4. Attacks attempted, and what forecloses each

I list these as constructions, not as descriptions, because the brief is right that a
described attack is not an attack.

### 4.1 Degenerate-but-legal files

**A-1. The 128-byte empty file.** Rebuilt from Appendix A byte for byte; the trailer CRC
is `0x402F157E` as stated and the directory's 4 bytes are the CRC of zero bytes,
`00 00 00 00`. Conforming. Both verifiers certify. No fork.

**A-2. The smallest file carrying a layer.** Layer `a`, rank 1, one uint8 channel,
E=(0), T=(1), interleaved, codec 1, filter 1, A=S=A_slab=0, index_encoding 1,
entry_count 0, crc_of_crc_array 0, extent slot (0,0). Inline payload 73 bytes; record
24+73 = 97; directory 101 bytes at [16,117); pad to 128; trailer [128,192); F=192.
Conforming under [R-GEO-02] and §21.6's "A dimension has extent 0" row, and
[R-CNT-17]/[R-CNT-23] force exactly the (0,0) slot and zero crc_of_crc_array I used. No
fork.

**A-3. A-2 with codec 4 and a huge tile extent.** T = 2^62, uint8, interleaved:
P = 2^62, decoded size P·Q = 2^62 > 0x7E000000. [R-COD-07] is quantified over *addressed*
tiles and the layer addresses none, so the lz4 cap is vacuous and the file is conforming —
§17.2's Note says exactly this, and L44's condition text ("any of whose addressed tiles'
decoded size exceeds") restates the quantifier faithfully. **Foreclosed.**

**A-4. A-3 pushed past 2^63 − 1.** T = 2^62, four uint8 channels, interleaved: Q = 4,
P·Q = 2^64. Now the file is *rejected at layer scope* even though no tile is addressed,
because [R-ENC-04] carries no addressed-tile quantifier, [R-SER-02] and [R-SER-07]
expressly designate every decoded size, and §19.3 requires the ceiling to be checked at
layer access "on the decoded sizes §14 derives from it". §17.2's Note states the
asymmetry between the cap and the ceiling explicitly. Two verifiers must agree.
**Foreclosed.**

**A-5. Sentinel-adjacent boundary entries.** offset = length = 2^64−1 with crc ≠ 0 (T6);
exactly one half sentinel (T7); offset = 2^64−2 (T11, "distinct from the all-ones
sentinel"); length 0 non-sentinel (T10); offset 15 (T8); offset+length = F−63 (T9). §15.3's
table is ordered and its first three rows dispose of the sentinel patterns before
[R-ENC-03]/[R-ENC-04] can bite, and [R-IDX-02] says so ("[R-ENC-03]'s value-domain rule and
[R-ENC-04]'s sum rule apply to the fields of non-sentinel entries only"). Every case lands
on exactly one row with the same outcome, reject-tile. **Foreclosed.**

**A-6. A non-sentinel entry whose stored bytes have CRC-32C = 0.** Legal: the sentinel is
identified by offset *and* length being all-ones, not by crc = 0, and §15.2 uses the crc
field only to say a sentinel's is 0. A verifier that treated crc = 0 as a sentinel marker
would be wrong under §15.3's first row. **Foreclosed**, and cleanly.

### 4.2 Two structures claiming the same bytes

**A-7. Two layer records whose extent slots address the same index region.** Each region
is that layer's structure, so this is an overlap "across layers" → reject-file, F33.
§9.7's "the region enters the walk once, as that record's extent, and is not a second
claimant beside it" keeps a *single* layer's region from being double-counted, and does
not blunt the cross-layer case. **Foreclosed.**

**A-8. Two index entries of one layer with identical offset and length.** Two stored
extents of the same layer overlap → intra-layer → reject-layer, L18. §22.3 names this
case ("two index entries pointing at one payload") as removed by construction.
**Foreclosed.**

**A-9. A stored-tile extent inside its own layer's index region** → reject-layer;
**inside another layer's index region** → reject-file; **inside the directory** →
"touching another scope's structures" → reject-file. [R-CNT-13]'s three-way split and
F33/L18 agree on all three. **Foreclosed.**

**A-10. A claimant reaching the front block or the trailer.** F33's condition text
pre-empts this and routes each to its own bounds row, including the awkward case: a record
extent slot of (0, N) with N nonzero "reaches the block through its zero offset and is
theirs [F30/L15's] rather than F31's or L16's". I could not construct a claimant that
falls between two rows. **Foreclosed.**

### 4.3 The pre-trailer gap

**A-11. A conforming file with a 10 KiB pre-trailer gap.** [R-CNT-05] says in terms that
"a longer gap is conforming, and no conforming commit produces one", and [R-CNF-02] lists
"§6.2's pre-trailer gap longer than [R-LIF-02] step 5's pad" among the writer obligations
whose violation is expressly not a file-conformance violation. Both verifiers certify.
**Foreclosed** — and this is the shape the document handles best.

**A-12. A live stored-tile extent in that gap.** F7, verifier, reject-file. A plain reader
never notices, which is licensed. Both verifiers agree. **Foreclosed.**

**A-13. A *superseded* region in that gap.** This is the one that produced a finding; see
adversary-01. The live-state walk does not reach it, so under [R-CNT-02]'s definition of
"structure" it is slack and the file is conforming; under [R-CNT-01]'s use of the same
word it is one of "the structures the file's commits appended".

### 4.4 The seam between reader and verifier

**A-14. An interleaved bool byte of 0x02 at a real position.** T2, detector *verifier*.
Reader A returns "true" encoded 0x01 per [R-SER-08]; Reader B rejects the tile under
[R-CNF-12]'s licence on a nonconforming file. Both conforming readers; the file is
nonconforming under both. Not a certification fork, and [R-SER-08]'s Rationale says this
is deliberate. **Foreclosed.**

**A-15. Coverage overlap that only a verifier sees.** [R-CNT-13]'s parenthetical
("readers are not obligated to detect overlap") makes reader/verifier divergence expected
here. Verifiers still agree with each other. **Foreclosed.**

### 4.5 Capability-relative verdicts (the most promising family, and it is closed)

I made four separate attempts to turn a capability difference into a certify/reject fork,
and the document routes every one of them into *cannot establish*, which is neither
certification nor a finding of nonconformance:

**A-16.** A 12 MiB user-metadata document framed with Single_Segment_Flag: Window_Size =
content size = 12 MiB, above §21.9's 8 MiB guarantee but below the 16 MiB document
guarantee. Verifier A (16 MiB window bound) decodes and certifies; Verifier B (8 MiB
bound) declines. [R-MTA-09] makes B's verdict *cannot establish* and forbids it to report
nonconforming; §21.6's row makes the file conforming. B does not reject; A does not
certify a file B rejects. **Foreclosed.**

**A-17.** A 200 MiB tile with a 16 MiB zstd window. [R-COD-06]: "a wider window is
conforming and merely permits a conforming reader to decline the tile or the layer on
resource grounds". §9.7 makes a declining verifier unable to certify. Same shape.
**Foreclosed.**

**A-18.** A top-level record of an experimental type with MU = 1. §21.6's closing
paragraph makes the file conforming and the reader's refusal a capability fact;
[R-CNF-11] gives the verifier *cannot establish*. A verifier that implements the private
type certifies. **Foreclosed** — and §21.9's "the two capability refusals §21.6's closing
paragraph names ... are not this ground" keeps it out of [R-ERR-04].

**A-19.** The same type as a *layer sub-record* with MU = 1. [R-CNT-18] makes it
reject-layer and adds "where the file is otherwise conforming a reader MUST NOT reject
the file for it"; §21.6's closing paragraph calls the qualifier load-bearing. The
verifier's route is again [R-CNF-11]'s cannot-establish ground. **Foreclosed.**

The document has, systematically, made certification capability-relative in one direction
only: a verifier that cannot check something must not certify and must not condemn. I
tried and failed to find a case where two verifiers land on *opposite* sides of the
conforming/nonconforming line for capability reasons.

### 4.6 The closed list of §20.3 step 4 — the surface the brief points hardest at

I derived the members from the structure the list governs (§7.4's declaration fields)
rather than from the sentence, and put each on exactly one side:

| §7.4 field | Side |
|---|---|
| layer name | permitted (names) |
| layout | fixed |
| linearization | fixed |
| codec | fixed |
| filter | fixed |
| alignment A | permitted (declared / re-established / cleared) |
| slab S | permitted (same) |
| slab alignment A_slab | permitted (part of "a slab declaration") |
| rank d | fixed |
| channel count C | permitted for planar (via the channel list); fixed for interleaved |
| dimension name | permitted |
| dimension extent E_i | permitted (grow only) |
| tile extent T_i | fixed |
| channel name | permitted |
| channel type | fixed |
| channel fill | fixed |
| index_encoding | fixed |
| entry_count, crc_of_crc_array, extent slot | derived, "follow the commit" |
| sub-records | §20.4's subject, expressly carved out |

The claim "Between them the two lists reach every declaration field of §7.4" is true. The
tie-break clause — "where a field is on both sides ... the permitted side states the whole
of what a commit MAY do to it" — resolves the three fields that appear twice, including
the one that would otherwise be genuinely open: the fixed side's "the position of every
planar channel but the last" would, read alone, forbid removing a *run* of trailing
channels, while the permitted side allows "shortened from its end ... whatever the counts".
The tie-break clause makes the permitted side govern. That is a real repair and it holds.

Then I took the four permitted members in pairs, since the brief asks for exactly that:

- **(names, names).** "a commit MAY change several names at once, two swapped included,
  the dimension order and the channel order being positional and fixed." Correct: names
  enter no map, and a swap changes no position.
- **(names, extent growth).** Independent. Growth adds positions that held their
  channel's fill (§14.5), so no stored byte is reinterpreted.
- **(names, channel-list change).** A rename that collides with an appended channel's name
  is caught by "each subject to every rule the declarations it produces are under" plus
  [R-ENC-15]. Sound.
- **(names, slab/alignment).** Independent.
- **(extent growth, channel-list extension).** The justification is "an appended planar
  channel adds tiles at ordinals after every existing one, a disk ordinal being c·N + s".
  With N growing to N′ in the same commit, the appended channel occupies [C·N′, (C+1)·N′)
  and the existing tiles [0, C·N′), so the claim survives the pair. I checked this
  explicitly because it is exactly the shape the brief warns about — a justification true
  of a member alone and false of the pair — and it does not fail here.
- **(extent growth, channel-list shortening).** The interesting one. C: 3→2 with N: 4→6
  leaves entry_count unchanged at 12 while every entry's meaning changes (old ordinal 6 =
  channel 1, s = 2 becomes new ordinal 8). The step's re-emission clause covers it
  ("the region is re-emitted under the clause above **whether or not entry_count changes
  with it** ... and whether or not a retained ordinal moves"). That qualifier is doing
  real work and it is correct.
- **(extent growth, slab/alignment).** Growth changes N and therefore the run partition,
  which triggers [R-SLB-04]; §20.3's below-clause requires re-establishment or clearing,
  and the failure is verifier-detectable as L41/L42. Sound, and detectable — which is more
  than most of this step is.
- **(channel-list, slab/alignment).** Same route.
- **(extension, shortening) of one channel list.** The stated exception. "of one channel
  list" correctly leaves a commit free to extend layer A's list and shorten layer B's.
- **(slab, alignment).** Clearing S and declaring A in one commit is within the member and
  produces a record [R-CNT-16] permits; declaring both is L20. Sound.

I also checked the closure claim "a growth renumbers ordinals wherever [R-GEO-06] moves
them, and nothing else this step permits moves one" against each member: names no, growth
yes (both through G_i in s and through N in c·N + s), extension no (existing c·N + s
unchanged), shortening no, slab/alignment no. True.

And I checked §11.1's Rationale and §13.3's Note against §20.3, since both restate it:
"a growth that changes no grid count moves no entry and adds none, as does one that raises
a grid count while another stays 0". The three-way partition {no grid count changes} ∪
{a grid count rises while another stays 0} ∪ {everything else} is exhaustive and each
branch is correct, because N = ∏G_i holds at 0 whenever any G_i is 0, and rises whenever
one G_i rises and none is 0. §11.1's "the growth that raises a zero-extent layer's **only
remaining** zero grid count included" is the boundary case and it is right.

The one place I could not close the list cleanly is the gloss "so replacing the last
channel, or any run of channels at the end, is two commits or a rewrite", which is
finding adversary-04.

I also asked the prior question the brief implies: **can any actor detect a §20.3 breach
at all?** No. §9.7's walk reaches the live state only; the superseded generation survives
as slack; §9.6 offers the backward probe to verifiers but says "no verdict turns on the
probe" and "For a verifier the probe is diagnosis ... not a finding about the file it was
given". So a §20.3 breach is *unwitnessed* in §21.7's exact sense, which is why the
register carries no row and §21.1's completeness clause is not violated. The prohibition
still binds the actor — §21.7: "Being unwitnessed bears on detection and not on
permission" — so an ambiguity in the list still moves the set of byte sequences a
conforming updater may emit, even though no verifier can see it. That is why I treated
this surface as byte-level-capable and ground through it. What the document never says is
whether the *file* such a commit produces is conforming; see finding adversary-03.

### 4.7 Compaction (§20.5)

**A-20.** A layer declaring A = 2^62 with one stored tile. The only legal offset at or
above 16 is 2^62, so the input is ≥ 4 exabytes, and the compactor — bound by "every
declared layout invariant permits ([R-SLB-01], [R-SLB-03])" — must reproduce that. It
cannot clear the declaration ([R-WRT-05]/[R-WRT-07] let it change only extent slots and
regenerated-region fields). So compaction cannot shrink the file. Absurd but consistent;
"so slack is never carried" means the input's slack is not copied, not that the output has
none. **Foreclosed.**

**A-21.** An entry that §15.3 classifies reject-tile on a structural ground, inside a
region the compactor must regenerate. §20.5's regeneration paragraph is explicit: the
entry is neither a sentinel nor re-pointable, so meeting it makes the violation one the
compactor has detected, [R-WRT-06] obliges refusal, and no drop is available because a
tile-index entry is no record §20.4 licenses dropping. **Foreclosed**, and unusually
carefully.

**A-22.** An entry whose stored bytes fail their crc, in a compaction. [R-WRT-09] reaches
"each relocated extent's checksum, **including every stored tile's entry crc**", and
§20.5's next paragraph reads that as unqualified ("[R-WRT-09]'s checks reach the index
chain and each stored tile's entry crc"). So the compactor detects it and must refuse.
I considered the narrower reading — that only *relocated* extents' crcs are owed — and
the second sentence closes it. **Foreclosed.**

**A-23.** Whether a compactor may drop its way out of a [R-WRT-09] failure. The text
separates the two: "MUST refuse to compact when any check [R-WRT-09] obliges fails, **and**
MUST NOT emit a file carrying a violation it has detected"; dropping answers only the
second, and only where §20.4's table licenses it. Since both registered types carry PE = 1,
the droppable case is an unregistered MU = 0 / PE = 0 record — which is precisely where a
[R-WRT-09] check does not reach (§8.1 covers such an extent by no checksum). The two
clauses do not overlap. **Foreclosed.**

### 4.8 User metadata (§18.2 / §21.5 / §21.6)

**A-24.** A document containing the decimal midpoint 2^1024 − 2^970. Under roundTiesToEven
this converts to infinity, so R8 fires; the newly named rounding attribute makes this
decidable rather than parser-dependent. **Foreclosed by the repair.**

**A-25.** `NaN` as a bare token: exhibits both R8 (bare token) and R7 (not well-formed
JSON). §21.1's specialization rule records it against the narrower row, R8. Both outcomes
are ignore-record and both are violations, so no verdict moves. **Foreclosed.**

**A-26.** An encoding-2 document whose Frame_Content_Size disagrees with the decoded
length. Routed to R4 rather than R3 by R3's own text; R4's instance cell enumerates both
directions. Checkable only by decoding, which R4's condition text concedes ("broken by
what the frame declares while the bytes decode"). Consistent.

**A-27.** A user-metadata record at an experimental-range encoding whose extent's terminal
CRC fails. This is finding adversary-02 and the closest thing to a certify/reject fork I
found.

**A-28.** extent_length exactly 5 (a one-byte document). Structurally legal, and the
document is then unreadable under R7 (a one-byte JSON text cannot be an object) or R4
(one byte cannot carry the zstd magic). Nonconforming but for a document reason, not a
framing one. Both verifiers agree. **Foreclosed.**

### 4.9 Reach across format majors ([R-CNF-13], §2.3, §21.2)

I re-derived §21.2's claim that the reaching rows are "F8, F14, F6 and both of F1's
instances — and no other row" from [R-CNT-24]'s four permanent invariants (magic at
F−64; version_major/minor at F−56, i.e. trailer bytes [8,12); a CRC-32C at F−4 over
[F−64, F−4); the front block constant). The redefinable 48 bytes are trailer [12,60),
which contains flags, dir_offset, dir_length, committed_file_length, file_id and the
reserved bytes — so F9, F10, F12, F13, F15, F16, F17, F19 and every F2/F3 instance are
correctly excluded. F5's exclusion is argued in §2.3's Note from the fact that its
128-byte floor is derived from format-major-1 minimums. F18 is outside the premise because
version_major = 0 declares no major. I could not find a fifth reaching row.

## 5. Findings

### adversary-01 (AMBIGUITY) — §5.1 uses "structure" for bytes §5.2 defines as slack, and §6.2 makes a structure in the pre-trailer gap a file-scope error

**Location.** §5.1 [R-CNT-01]; §5.2 [R-CNT-02]; §6.2 [R-CNT-05]; §21.2 F7.

**Quotation** (§5.1, [R-CNT-01]):

> "Between them lie the structures the file's commits appended — stored-tile payloads,
> tile-index regions, record extents (§5.2), the directory each commit appended, and each
> prior generation's trailer — with slack (§5.2) wherever a commit left a gap"

against §5.2 [R-CNT-02]:

> "Every byte of the live committed state belongs to exactly one of: the front signature
> block; or a **structure** — a stored-tile extent, a record extent (the bytes any
> record's extent slot references, whatever the record's type, §7.2), the directory, or
> the trailer."

and §6.2 [R-CNT-05]:

> "A verifier MUST treat a structure in that gap as a validity error at file scope"

**The construction.** F = 448. Front block [0,16). A layer's tile-index region at
[16,100). The live directory at [100,201) (dir_offset 100, dir_length 101). A byte-exact
copy of a superseded tile-index region — 84 bytes for four sentinel entries plus their
segment CRC — at [201,285). Zeroes to [384). Trailer at [384,448). Everything the live
trailer reaches is well-formed; the bytes at [201,285) are reachable from nothing.

**The two verdicts.** Verifier A reads "structure" as [R-CNT-02] defines it — a member of
the live committed state's partition — finds no claimant in [201,384), counts 183 bytes of
slack, and **certifies**. Verifier B reads "structure" as [R-CNT-01] uses it, where "each
prior generation's trailer" and "the directory each commit appended" are structures the
commits appended, concludes that a superseded region lying between the live directory's
end and the trailer is a structure in the gap, and reports **nonconforming** on F7.

**Which reading I picked, and why.** A. [R-CNT-02] is the only place the word "structure"
is *defined*, and it defines it as a class of the live-state partition; [R-CNT-05] cites
§5.2 for the pad's status, so it is drawing on that definition; §9.7 walks the live state
only; and F7's Instances cell enumerates live-state claimant kinds ("stored-tile extents;
tile-index regions; record extents; sub-record extents") with no trailer or superseded
directory among them. Reading B is also unimplementable: nothing an actor is obliged to do
identifies a run of opaque bytes as a superseded region, and §9.6 forecloses the one
mechanism that could ("no verdict turns on the probe").

**What an implementer does wrong without it.** A verifier author who takes §5.1's sentence
as the operative sense of "structure" will implement F7 as a backward scan of the
pre-trailer gap for trailer magic and directory-shaped bytes, and will reject files that
§21.6's "A payload contains a byte string that mimics a trailer | Inert" row declares
conforming.

**Byte-level: no.** The competing reading dies on [R-CNT-02]'s express definition, on
§9.7's live-state-only walk, and on §9.6's "no verdict turns on the probe" — three
governing clauses above the sentence. §5.1's first sentence is also descriptive anatomy;
[R-CNT-01]'s operative clause is the last one ("The file size of a conforming file equals
the live trailer's committed file length F"). The emittable set does not move.

### adversary-02 (AMBIGUITY) — §21.5's experimental-encoding exception is stated over "the rows below" and names only R1 as surviving, leaving R2's extent CRC in doubt

**Location.** §21.5 preamble; §21.5 R2; §21.6's experimental-encoding row; §18.2
[R-MTA-10].

**Quotation** (§21.5 preamble):

> "User metadata is quarantined (`[R-CNT-25]`): every way its document can be unreadable
> takes this outcome, whatever the containing scope — as a violation in the rows below,
> except at an experimental-range encoding, where no document rule attaches and §21.6
> records the defined non-violation (`[R-MTA-10]`) ... Encoding 0 and a reserved-range
> value are unassigned too, and R1 registers both as violations: what `[R-MTA-10]`
> withdraws is the document's content rules, never the encoding byte's own value set
> (`[R-MTA-03]`)."

and §21.6:

> "A user-metadata record declares an experimental-range (≥ 0x80) document encoding |
> Ignored (ignore-record); the file is conforming — §10.3's prohibition binds a writer's
> conduct, not the bytes. No document rule attaches at such an encoding, so a verifier
> certifies, reporting the record it ignored"

**The construction.** A 320-byte-plus file, otherwise conforming, carrying one top-level
user-metadata record: inline_length 1, encoding byte `0x80`, extent slot (X, 40) with the
extent's final four bytes deliberately *not* equal to the CRC-32C of the preceding 36. No
other defect anywhere.

**The two verdicts.** Verifier A applies R2 ("A user-metadata extent's final 4 bytes do not
equal the CRC-32C of the preceding bytes"), whose row carries no encoding qualifier, and
reports **nonconforming**. Verifier B reads the preamble's exception as reaching "the rows
below" wholesale at an experimental-range encoding — noting that the preamble takes the
trouble to name R1 as surviving and says nothing about R2 — and reads §21.6's row as
instructing it that "a verifier certifies". It **certifies**.

**Which reading I picked, and why.** A. [R-MTA-10] states the surviving checks as a closed
three-item list and the extent CRC is in it: "file conformance — a pure predicate on bytes
(`[R-CNF-02]`) — is decided by the structural checks that precede the document alone: the
record's framing and extent slot (`[R-CNT-13]`), the encoding byte's own value set
(`[R-MTA-03]`), and the extent's terminal CRC (`[R-CNT-20]`)." §22.3 says the same in
other words ("covered by its terminal CRC but constrained by no content rule ... the CRC
detects corruption"), §8.1's map states the UM extent's checksum with no encoding
qualifier, and the preamble's own next sentence supplies the limiting principle ("what
[R-MTA-10] withdraws is the document's content rules") — a CRC over stored bytes is not a
document content rule. §21.1 seals it twice: "where a row and the rule it cites diverge,
**the rule governs**", and "§21.6's entries restate their governing rules on the same
terms a row does, and where such an entry and the rule it cites diverge, the rule governs
there too."

**What an implementer does wrong without it.** A verifier that takes reading B certifies
a file with a corrupt user-metadata extent, which is the one thing §22.3 says that
extent's CRC is still there to catch, and the one certificate §8's chain of trust would
be silently short of.

**Byte-level: no** — but it is the nearest miss in this walk. Reading B is a certify /
reject fork on identical bytes, and it is textual rather than invented: the preamble
carves at the level of "the rows below" and its enumeration of survivors names R1 alone,
which invites *expressio unius*. It dies because [R-MTA-10] names the terminal CRC
outright and §21.1 makes the rule govern the row and the §21.6 entry. Under the brief's
fifth discriminator this is a finding that dies on a governing clause above the sentence,
so I grade it not byte-level and say so.

### adversary-03 (OBSERVATION) — §2.1's Note states two phrasing invariants the document does not satisfy, and the shortfall lands on §20.3's closed list

**Location.** §2.1 (the Note after [R-CNF-01]); §20.3 step 4; §18.2 [R-MTA-09];
[R-WRT-08]; [R-LIF-01].

**Quotation** (§2.1):

> "**Note.** Requirements in this document follow a fixed phrasing discipline: every
> requirement names the actor it binds (writer, reader, updater, verifier, or file); every
> writer-side prohibition is paired with an explicit reader-side clause stating what a
> reader does with a violating file; every SHOULD states the consequence of deviation; and
> requirements constrain bytes and observable behavior, never implementation technique."

**Limb 1 — the pairing claim.** I swept every writer-, updater- and commit-side MUST NOT
in the document (24 matches over the flattened text). Twenty carry an explicit reader-side
clause, usually in the same sentence ("a reader MUST treat ... as a validity error at
layer scope"). Four do not:

- §20.3 step 4: "A commit MUST NOT change one of these; the change is a new layer, or a
  whole-file rewrite under a fresh file_id" — no reader-side clause, no §21 row, and no
  statement anywhere of what a reader or verifier does with a file a violating commit
  produced.
- [R-WRT-08]: "An updater MUST NOT re-encode a record whose type it does not implement,
  and MUST NOT modify one except by relocating its extent and re-pointing its slot".
- [R-LIF-01]: "a writer MUST NOT modify them".
- [R-LIF-04]: "the writer MUST NOT append" (on a torn file).

**Limb 2 — the SHOULD claim.** I swept all 44 SHOULD/SHOULD NOT occurrences. Every
normative one states a consequence of deviation except [R-MTA-09]'s, in §18.2, which is on
this round's changed surface:

> "the verifier SHOULD report the bound it applied and the stored length of the extent it
> declined."

No consequence is stated. (Two others — [R-SLB-01]'s and [R-SLB-03]'s "which writers
SHOULD zero" — state theirs only by cross-reference to [R-CNT-03] via "(§5.2)", which I
count as satisfying the claim.)

**Why this is worth a line rather than a shrug.** The pairing claim is what tells an
implementer that any writer prohibition it finds has a detectable consequence it can build
against. §20.3's closed list is the document's most consequential writer prohibition — an
entire round's byte-level survivor lived in it — and it is precisely the one with no
reader-side clause. The document does establish, elsewhere and correctly, that a §20.3
breach is *unwitnessed* in §21.7's sense (§9.7 walks the live state only; §9.6 says "no
verdict turns on the probe"), so the register's completeness clause is not violated. But
nothing says whether the *file* a violating commit produces is a conforming file.
[R-CNF-02] enumerates the two kinds of writer obligation that do not touch file
conformance — conduct rules (§10.3, §18.3) and obligations "whose violation this
specification expressly declares not to be a file-conformance violation" (§6.3's flags
rules, §6.2's long pre-trailer gap) — and §20.3's list is in neither. §21.7 then says
that being unwitnessed "bears on detection and not on permission", which leaves the file
nonconforming-but-invisible; and [R-CNF-12]'s "a verifier certifies only violation-free
files" is then satisfied only because no verifier can look. That is a coherent position,
but the document never states it, and §2.1's Note points the reader at a reader-side
clause that does not exist.

**Byte-level: no.** The block is labelled *Note* and is therefore non-normative under
[R-CNF-01], so it cannot itself move the emittable set; and the §20.3 status question has
no behavioural consequence I could construct — an updater that breaches §20.3 is
nonconforming under §20.3 whether or not its output is also a nonconforming file, and no
verifier can reach either question. Reported because a non-normative block that misstates
the document's own practice still tells an implementer what to build.

### adversary-04 (AMBIGUITY) — §20.3's gloss "replacing the last channel ... is two commits or a rewrite" is stated over a result that a permitted rename also produces

**Location.** §20.3 step 4, the paragraph beginning "A commit MAY make several of these
changes at once".

**Quotation:**

> "A commit MAY make several of these changes at once, an extension and a shortening of one
> channel list excepted: a commit that shortens a planar layer's channel list appends no
> channel to it and one that extends it removes none, whatever the counts, so replacing the
> last channel, or any run of channels at the end, is two commits or a rewrite."

against, in the same step:

> "its name, and its dimension and channel names, MAY change"

**The construction.** A planar layer L that stores tiles, with channels
[a: uint8 fill 0x00, b: uint8 fill 0x00, c: uint8 fill 0x00]. One commit emits a new
directory in which L's channel list is [a, b, d], where d has type uint8 and fill 0x00 —
byte-identical to c in every field but the name — and every index entry is carried forward
byte-identically at its disk-ordinal position.

**The two readings.**
1. This is a rename of channel 2, permitted outright by the first member of the closed
   list and by the justification paragraph's "a name enters no map this specification
   defines, and a commit MAY change several names at once". The commit is legal; d's tiles
   are c's tiles and no byte is reinterpreted.
2. This is "replacing the last channel", which the quoted sentence says "is two commits or
   a rewrite". The commit is illegal, and the in-place route — commit 1 shortens, commit 2
   extends — strands c's stored tiles as slack and gives d a fresh set of entries.

The two readings differ on whether a conforming updater may emit that directory as one
commit, and they differ on whether the channel's data survives the operation at all.

**Which reading I picked, and why.** 1. The sentence's antecedent is "an extension and a
shortening of one channel list", and the "so" ties the gloss to that composition; a rename
is neither. The justification paragraph two paragraphs down states the rename permission
without qualification and gives its ground. And reading 2 is against the step's own stated
principle — "The line is drawn where a stored tile's meaning is fixed" — since a rename
fixes nothing and moves nothing.

**Where the gloss is nonetheless loose.** "Replacing the last channel" is stated over a
*result* (the last channel differs), while the ban it is glossing is over an *operation*
(extend and shorten in one commit). Between two generations those are distinguishable only
by type and fill — and a replacement that changes type or fill is already forbidden
outright by the fixed side ("every channel's type and fill"), for which "two commits" is
the correct remedy, while a replacement that changes neither is a rename, for which it is
not. So the gloss is exactly right in the case it was written for and over-broad in the
only other case the result admits.

**What an implementer does wrong without it.** An updater library author who reads the
gloss as a result-level ban will refuse `rename_channel(layer, C−1, name)` on any planar
layer that stores tiles, and will offer instead a shorten-then-extend path that silently
discards that channel's stored data — the outcome §20.3 elsewhere warns writers about
("a writer SHOULD instead produce a new file wherever a commit would strand a large share
of a layer's stored bytes").

**Byte-level: no.** The competing reading dies on the unqualified permission in the closed
list's first member and on the justification paragraph's "a name enters no map this
specification defines, and a commit MAY change several names at once, two swapped
included" — both above the sentence complained of, and both in the same step.

## 6. Where I found little, and what I did there that would have found something

**A certify/reject fork.** I did not find one. What I did: I enumerated every place the
document makes a verdict depend on something other than the bytes — capability (§2.3's
cannot-establish grounds, [R-COD-11], [R-MTA-09], [R-ERR-04]), detector assignment
(reader vs verifier across all 120 rows), and detection tier (§19.2) — and built a file
for each of the four capability families (A-16 to A-19). Every one is routed into *cannot
establish*, which the document explicitly separates from both certification and a finding
of nonconformance, and [R-CNF-11] forbids certifying past it. I then walked the register
for pairs of rows that could attach different outcomes to one file, using §21.1's
specialization rule as the filter, and found the six named pairs plus no unnamed pair with
divergent outcomes. The one construction that came closest is adversary-02, and it dies on
[R-MTA-10]'s three-item list.

**Overlap and coverage.** I built six overlap constructions (A-7 to A-10 plus the
intra-layer and cross-scope variants) against [R-CNT-13]'s three-way split and could not
find a pairing that falls outside it or that F33/L18's condition texts route differently
from the rule. F33's own text pre-empts the hardest case (a claimant reaching the front
block through a zero offset) explicitly.

**Boundary values.** I exercised zero, one, the stated maximum and one past it on: file
size (64/128), dir_length (0/4/5/28), dir_offset (0/15/16), entry_count (0/1/65,536/
65,537/2^32/2^63−1), rank (0/1/255), channel count (0/1/65,535), extent (0), tile extent
(0/1/2^62/2^63−1), A (0/3/512/2^62/2^62+1), A_slab (0/1/2^62), S (0/1/2^63−1), P (1),
decoded size (1/0x7E000000/2^62/2^64), index entry offset and length (0/15/16/2^63−1/
2^63/2^64−2/2^64−1), extent_length on a user-metadata record (0/4/5). Each landed on
exactly one register row or was explicitly conforming. The two that surprised me — a
non-sentinel entry whose crc is legitimately 0, and an empty layer declaring an lz4 tile
size above the cap — are both handled in terms.

**§20.3's closed list.** This is where I spent the most time, because the brief pointed
there and because the emittable-set half of the byte-level test reaches it even though no
verifier can. I derived the members from §7.4's field list rather than the sentence,
partitioned all nineteen fields, took the four permitted members in all ten pairs, checked
each pair against the fixed side and against the justification sentence written for the
member alone, and checked the two closure claims ("Between them the two lists reach every
declaration field", "nothing else this step permits moves one"). All hold. The tie-break
clause "the permitted side states the whole of what a commit MAY do to it" closes the one
field where the two sides genuinely conflict. adversary-04 is the only residue, and it is
a gloss rather than a rule.

**Non-normative text.** I enumerated all 62 blockquotes, confirmed exactly one is
unlabelled and normative, and checked every labelled block that carries a BCP-14 keyword
for a normative anchor; five of six have one. I checked Appendix G's ten items for
internal consistency, including the non-obvious claim that two records tied by its
ordering key yield the same file in either order (they do, because the same total order
fixes both extent placement and directory order, so the record placed first gets the lower
extent_offset under either choice), and Appendix H's four checklists against the rules
they summarise. I found no contradiction in either appendix.

**Confidence.** High that the arithmetic, the checksums, the register's counts and the
cross-major reach derivation are correct — I recomputed all of them. Medium-high that no
certify/reject fork survives in the areas I walked. Lower for two areas I could exercise
only by reading: the RFC 8878 frame constraints as they apply to a *document* rather than
a tile (I checked the Window_Size and content-size logic by hand but ran no zstd encoder),
and the interaction of §20.3 with a slab declaration across a growth that changes the run
partition, where the invariant is verifier-checkable but I could not construct a file large
enough to exercise it.
