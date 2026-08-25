# Cleanroom round 25 — Adversary transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,477 lines), in eight `sed -n` slices, plus targeted `grep`/`python3` over that
same file. I opened no other file in the repository — no `docs/`, no `PLAN.md`,
no `AGENTS.md`, no `conformance/`, no `spec/registry.json`, no git history, no
network. The file was exactly where the brief said it would be. Every script I
ran is in a scratch directory I created (`scratchpad/work/`) and reads no
repository file; the only file I wrote under the round-25 output directory is
this transcript, and I did not read or list that directory.

**Context I did not ask for, and disregarded.** My runtime placed material in
context before I began: a project-instruction pointer (`CLAUDE.md` → `AGENTS.md`),
an index of the maintainer's private memory files with one-line descriptions, and
a `git status` block carrying the subject lines of the five most recent commits.
Those commit subjects name a round number, name ADR numbers, and characterise
what recent ADRs did — including one that names a specific register row. I did
not open any of those files, and I have deliberately not used any of that
material to settle a question. Where a conclusion of mine happens to touch text
those subject lines mention, I reached it from the discipline stated in §21.1 and
from comparing the row against its sibling rows, and I say so in the finding. I
note the exposure here because a disclosed breach is usable and a silent one is
not.

## 1. What I did

I read the whole document cold, front to back, then:

1. **Reproduced every constant and worked example numerically.** CRC-32C
   implementation from §4.5's parameters, checked against both check vectors,
   then used to reproduce: the 80-byte four-sentinel entry array CRC
   (`0x80A34955`), §7.4's `crc_of_crc_array` (`0xC4EE982E`), §15.4's full
   all-sentinel segment constant (`0xEECB3BB2`), and Appendix A's trailer CRC
   (`0xE00938D2`). All four reproduce exactly. I rebuilt Appendix A's 128-byte
   minimal file byte for byte from §6.1, §7.1 and §6.2 alone and got the
   published hex dump.

2. **Built a real file end to end** from the document alone: a rank-2
   interleaved layer, extents (5, 5), tile extents (4, 4), one `uint16` channel
   with fill `0xABCD`, codec 1, filter 1, four stored tiles, index region,
   directory, pad, trailer. G = (2, 2), N = 4, P = 16, Q = 2, decoded size 32,
   `entry_count` = 4, `extent_length` = 4·20 + ⌈4/2¹⁶⌉·4 = 84, `inline_length`
   = 94, F = 448. The edge tile at tile coordinates (1, 1) came out as
   `2c 00` followed by fifteen copies of `cd ab` — which is §14.5's worked
   example exactly, independently derived. Nothing in the build forced a guess:
   placement is free (`[R-SLB-05]`), record order is free (`[R-CNT-14]`), and
   every field I had to fill was pinned by §7.4's table.

3. **Checked every closed count and every list presented as complete.**

4. **Mechanically recomputed the register's instance arithmetic** and audited
   each Instances cell against §21.1's own stated discipline.

5. **Ran an attack list**: boundary values on every size/count/offset/alignment,
   overlapping and out-of-file structures, zero-length structures, every reserved
   and experimental value in every position, every combination of the record flag
   bits, the reader/verifier seam, feature interactions, and degenerate-but-legal
   files.

## 2. Arithmetic and constant verification (all pass)

```
CRC-32C("123456789")        = 0xE3069283   spec §4.5      ✓
CRC-32C("")                 = 0x00000000   spec §4.5      ✓
CRC-32C(4 × sentinel, 80 B) = 0x80A34955   spec §7.4      ✓
CRC-32C(55 49 A3 80)        = 0xC4EE982E   spec §7.4      ✓
CRC-32C(2^16 × sentinel)    = 0xEECB3BB2   spec §15.4     ✓
Appendix A trailer CRC      = 0xE00938D2   spec App. A    ✓  (whole 128 bytes reproduce)
```

Worked examples re-derived and confirmed:

- §5.1's 128-byte floor: dir at [16, 20) forces dir_offset + dir_length = 20
  ≤ F − 64, so F ≥ 84, and F ≡ 0 (mod 64) gives F ≥ 128. ✓
- §11.2: G = (4, 8), N = 32, P = 65,536; with E_y = 1000, G_y = 4 still. ✓
- §11.4: (300, 700) → tile (1, 2), s = 10, in-tile (44, 188), ordinal
  44·256 + 188 = 11,452; planar channel 2 → 2·32 + 10 = 74. ✓
- §14.2: T = (2, 3), a:uint8 + b:uint16 → Q = 3, size 18, ordinal 5 at [15, 18);
  planar b → 12 bytes, ordinal 5 at [10, 12); t:float32 + m:bool → Q = 5,
  size 30, ordinal 5 at [25, 30) with m at byte 29. ✓
- §14.3: T = (2, 5), P = 10, alternating → `55 01` with fill false, `55 FD`
  with fill true (pad bits 2–7 set). ✓
- §14.5: extents (5, 5), tiles (4, 4), edge tile (1, 1) = 1 real position and
  15 padding; 32 bytes, values 1–15 each `CD AB`. ✓ (reproduced by build)
- §15.4: entry_count 1,000,000 → 16 segments (15 full + 16,960), CRC array 64 B
  at [20,000,000, 20,000,064), segment 15 at [19,660,800, 20,000,000), entry
  999,999 at segment-relative byte 339,180; one full segment = 1,310,720 B =
  1.25 MiB. ✓
- §17.3: three float32s, s = 4, n = 3 → `00 00 00 00 00 00 80 00 40 3F 40 40`. ✓
- §7.4: 4 + 34 + 18 + 12 + 13 = 81 bytes, matching every offset in the hex
  dump. My own two-dimension one-channel layer: 4 + 34 + 36 + 7 + 13 = 94. ✓
- §12.1 bfloat16: 0x3F80 stored `80 3F`; 0x7FC0 = binary32 0x7FC00000. ✓
- §17.2's note on RFC 8878 window derivation: the Window_Descriptor's minimum is
  Window_Log = 10, i.e. 1 KiB, so a sub-1-KiB tile under codec 3 is indeed
  encodable only as a single-segment frame. ✓

I found no arithmetic error anywhere in the document.

## 3. Counts and closed lists (all pass but one, §5)

Mechanically extracted every register row and counted its Instances cell by
§21.1's rule ("Instances within a cell are separated by semicolons, and a cell
reading — is one instance"):

```
F: 36 rows,  58 instances
L: 49 rows, 116 instances
T: 26 rows,  55 instances
R: 10 rows,  48 instances
   121 rows, 277 instances
```

§21.3 says "49 conditions", §21.2 "36", §21.4 "26", §21.5 "10", §21.8
"121 conditions over 277 instances". All four subsection counts and both
§21.8 totals are exactly right. The arithmetic is sound; the question I pursue
in §5 below is whether one *cell* was written per §21.1's discipline.

Other counts I derived independently and confirmed:

| Claim | Location | Derivation | Verdict |
|---|---|---|---|
| "exactly four vehicles" | §10.1 | four numbered items; §10.2's spaces, §6.3's lanes, §7.3's types, §18.4's keys | ✓ |
| "Two spaces carry no experimental range" | §10.2 | channel layout (table) + the flag lanes | ✓ |
| "exactly thirteen sample types" / "the twelve types other than bool" | §12.1 | IDs 1–13 | ✓ |
| "Six rows are marked *structural*" | §15.3 | counted the table: 6 | ✓ |
| "Three frame features are excluded" | §17.2 | dictionary, content-checksum flag, oversized window | ✓ |
| "Four restrictions apply" | §18.2 | four bullets | ✓ |
| "Two axes recur" | §21.1 | layout-varying quantity; magnitude direction | ✓ |
| "Four rows are outside that reasoning" | §21.2 | F8, F1, F14, F6 | ✓ |
| "Two conditions that once sat in this table" | §21.6 | `[R-MTA-05]`, `[R-CNT-22]` | ✓ |
| "Two structural cases are conforming files a reader nevertheless refuses" | §21.6 | foreign major; experimental top-level MU = 1. §21.9 independently confirms exactly these two ("the two capability refusals §21.6 names"), and a resource decline is a MAY, not a refusal | ✓ |
| "Three properties bound what a hostile file can make a reader spend" | §22.2 | declaration-derived sizes; overflow checks; checksum-before-use | ✓ |
| "Four residues are stated rather than defended" | §22.3 | slack; unassigned-type extent; trailer mimic; unassigned-encoding metadata extent | ✓ |
| "§20.5's four obligations on a compacted file's trailer" | §21.7 | fresh file_id, generation, ignore-lane carry-forward, version_minor floor | ✓ |
| "one row for each of the other seven spaces §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)" | §20.5 | 8 spaces − record type = 7; the seven rows map one-to-one onto index encoding, linearization, sample type, layout, codec, filter, metadata encoding | ✓ |
| "Six choices shape everything else" | App. D | six bold items | ✓ |
| Appendix G's numbered list | App. G | the closing paragraph explicitly refuses to give a count ("this paragraph names what they are for, not how many there are"), and its enumeration omits item 5's fixed filter value — but the disclaimer forecloses the complaint | ✓ |

I also derived the register's **row** completeness independently, by walking every
normative rule in Parts 0–II and asking which condition it makes detectable, then
comparing against §21.2–§21.5. I could not find a detectable file-conformance
violation the register omits. In particular:

- Every `[R-CNT-06]` field gate has a row (F8–F17), and the two domain rules
  split correctly by owning scope (F2/F3 file, L1/L2 layer, T11/T12 tile).
- L2's nine derived quantities are exactly the ones the document defines:
  N, P, N·P, C·N (dominating the max disk ordinal), P·Q (dominating V = P·C),
  P·B^c, the index-region formula, and the two extent sums. ⌈P/8⌉ and the
  in-tile/spatial ordinals are all dominated by quantities already listed, and
  Q = ΣB_i ≤ 65,535 · 8 can never overflow.
- §15.3's six structural rows map one-to-one onto T6–T12 (seven rows, because
  the sixth structural row splits into T9 and T12 by which half fails).
- The flag-bit matrix is closed: for a registered type every deviation lands on
  F28/L49, MU = 1 with PE = 0 on F25/L46, reserved bits on F26/L47.
- Alignment A is *not* an "offset, length, extent, or count" under `[R-ENC-03]`,
  so its absence from L1 is right — an out-of-domain A is a non-power-of-two in
  range, caught by L39 (and A_slab by L29).

## 4. The attack list

Every attack below is a concrete construction. For each I give the two candidate
verdicts and the sentence that forecloses the disagreement, or record it as
surviving.

### 4.1 Boundary values

| Construction | Foreclosed by |
|---|---|
| F = 128 with dir at [16, 20) | conforming; Appendix A, reproduced |
| F = 64 (trailer only) | `[R-CNT-06]`'s `dir_offset + dir_length ≤ F − 64` is unsatisfiable with `dir_offset ≥ 16` → F10; also F5. And [0, 16) is inside the 64-byte suffix, hence resident, so `[R-CNT-04]` forces the front-block check → F6 |
| `dir_offset + dir_length = F − 64` exactly | conforming — the bound is "≤" |
| stored extent ending exactly at F − 64 | conforming — §15.3's row is "`offset + length > F − 64`" |
| `extent_offset = 16` exactly | conforming — the rows are "`< 16`" and "in 1–15" |
| `entry_count = 0` with slot (0, 0) and `crc_of_crc_array = 0` | conforming: §7.4, `[R-CNT-17]` ("and 0 when entry_count is 0"), `[R-CNT-23]`. The formula gives 0·20 + 0·4 = 0, consistent |
| `entry_count = 65,536` (one full segment) vs 65,537 (a 1-entry partial) | §15.4 defines segment s as `[s·2¹⁶, min((s+1)·2¹⁶, entry_count))`; the first is "full … final or not" so `[R-IDX-05]`'s constant is licensed, the second's tail CRC "MUST be computed" |
| `generation = 1` and `= 2⁶³ − 1` | both in range; §9.3's note closes the top ("step 5 of `[R-LIF-02]` has no value left to write") |
| `file_id = 1`; `version_minor = 65,535`; ignore lane `0xFFFF0000` | all conforming (`[R-CNT-06]`, `[R-CNT-07]`, `[R-CNT-08]`, §21.6) |
| `A = 512`, `A = 2⁶²`, `A_slab = 1`, `A_slab = 2⁶²`, `S = 1`, `S = 2⁶³ − 1` | all at the stated bounds, all conforming (§7.4, §16, §21.9) |
| `T_i = 2⁶³ − 1` with `E_i = 0`, rank 1, one uint8 channel | conforming. P = 2⁶³ − 1 is in domain; §17.2's note is explicit that `[R-ENC-04]` still checks P·Q in an empty layer while `[R-COD-07]`'s cap does not apply. §21.9's tile-size row does not reach it either ("A layer addressing no tile … has no tile whose decoded size the table bounds") |
| rank 2 with `T = (2³², 2³²)` | P = 2⁶⁴ → L2 at layer access, no I/O |
| `entry_count = 2⁶³ − 1` | `extent_length = entry_count × 20 + …` overflows → L2, before any allocation. §22.2's note states exactly this defence |
| `E_i = 1`, `T_i = 2⁶²`, tile is the sentinel | conforming and trivially servable (reads as fill, no payload I/O), yet outside `[R-CNF-03]`'s duty because §21.9's tile-size row ranges over addressed tiles "stored or not". Two readers diverge — one serves fill, one declines — but `[R-ERR-04]` licenses exactly that, and the file's status is unchanged |

### 4.2 Two structures claiming the same bytes; structures outside the file; zero length

- **Two stored extents of one layer, identical** — §15.3's *verifier* row and
  `[R-CNT-13]` make it reject-layer (L18). Deduplicating identical tiles is
  therefore not available; "Extents are owned exactly once" is unambiguous.
- **A stored extent of layer A overlapping layer B's index region** — "any
  overlap across layers … as reject-file" → F33. A reader accepts it (readers
  "are not obligated to detect overlap"); both *verifiers* reject.
- **Two layer records whose extent slots address one index region** — same
  bytes claimed twice; F33. Both entry_counts must agree by `[R-CNT-17]`, so
  the file is readable; it is nonconforming all the same.
- **A record extent inside the directory region** — reader-legal (offset ≥ 16,
  end ≤ F − 64), verifier-fatal: §9.7 makes the directory a claimant and the
  extent another, and `[R-CNT-13]` classes two non-layer structures overlapping
  as reject-file (F33). §9.7's "A record is not a claimant of its own" closes
  the obvious counter-argument.
- **A structure claiming bytes past F − 64** — F32/L17/T9 by tier.
- **A zero-length structure** — unreachable: `dir_length ≥ 4`, a non-sentinel
  entry of length 0 is T10, an extent slot with one half zero is F30/L15, and
  (0, 0) means *no* extent rather than an empty one. §17.2's note nails the
  premise ("Decoded output is never empty — §14's decoded sizes are at least 1
  byte"), which I verified: every decoded size is P·Q, P·B^c or ⌈P/8⌉ with
  P ≥ 1 and Q, B^c ≥ 1.
- **A structure in the pre-trailer gap** — a legal reader accepts (its only
  check is `[R-CNT-06]`'s dir bounds); a verifier must reject (F7, `[R-CNT-05]`).
  Designed seam, stated in `[R-CNT-05]` itself ("readers check neither").

### 4.3 Reserved / unknown / experimental values in every position

I walked all eight spaces of §10.2 in every position they occupy.

- **Record type, top level**: 0 → F24; reserved with MU = 1 → F35 (reader,
  reject-file) *and* F36 (verifier); reserved with MU = 0 → F36 only, reader
  ignores; experimental with MU = 0 → conforming and ignored (§21.6);
  experimental with MU = 1 → **conforming file the reader must refuse**
  (§21.6's second structural case).
- **Record type, sub-record**: same values, but `[R-CNT-18]` makes MU = 1
  reject-*layer* and adds "where the file is otherwise conforming a reader MUST
  NOT reject the file for it". L24/L25 register the reserved case.
- **Layout, linearization, sample type, codec, filter, index encoding**: 0,
  reserved and experimental all reject-layer (L36, L33, L34, L43, L45, L31),
  each with the value-set alternatives enumerated.
- **Metadata encoding**: 0 and reserved are R1 (violation, ignore-record);
  experimental is a *defined non-violation* (§21.6, `[R-MTA-10]`) that a
  verifier certifies while naming the record. This is the one space where a
  reserved value and an experimental value part company, and §21.5's preamble
  says so explicitly.
- **Reserved flag bits 2–15**: writers zero, readers ignore, verifiers reject
  (F26/L47). Every one of the four (MU, PE) combinations on both registered
  types lands on a row; I enumerated the matrix and found no gap.

### 4.4 The reader / verifier seam

The document deliberately puts twenty conditions on the verifier's side of the
line (F7, F25–F28, F33, F36, L18, L25, L40–L42, L46–L49, T2, T4, T5, T26, plus
F1/F6's front-block instance for a non-resident reader). I tried to turn each
into a *verifier-versus-verifier* divergence and could not: §21.1 states the
reader's side for every one of them ("the governing rule states what a reader
does, and for several such rows it obliges the reader to serve the structure
unchanged"), and every such file is nonconforming, so both verifiers reject.

The nearest thing to a fork I found is a **verdict-flavour** divergence, not a
certification divergence:

- A file with `version_major = 2`, valid magic and trailer CRC, and a physical
  length of 100 bytes. Verifier A checks `[R-CNT-27]` (nothing in §6.2 orders
  it) and reports *nonconforming* on F5. Verifier B follows §6.2's order —
  magic, CRC, version gate — refuses on capability grounds, and reports *cannot
  establish*, which is what §21.2's preamble prescribes (F5 is not one of the
  four rows whose subject is "a field fixed across every major"). Neither
  certifies, so no accept/reject verdict moves; §2.3's "An established violation
  takes priority" plus §21.2's preamble decide it in B's favour, at the cost of
  a cross-reference.
- A file carrying an experimental top-level MU = 1 record *and* a reserved flag
  bit on a layer record. Verifier A stops (as a reader it must reject-file, and
  "A reader MUST NOT rely on any structure in it") and reports *cannot
  establish*; Verifier B continues, establishes L47, and reports *nonconforming*.
  §2.3 resolves it: *cannot establish* "is available only to a traversal that
  established no violation", and a verifier's licence to stop is granted only
  "at the first violation it finds" — which the experimental record is not.
  Again both refuse certification.
- A 20 MiB verbatim user-metadata document. Verifier A (bound 16 MiB) declines,
  reports *cannot establish*, MUST NOT certify. Verifier B (bound 32 MiB)
  certifies. **One certifies, the other does not** — but this is licensed and
  explained, not a defect: §18.2 says in terms that "the bound is that
  verifier's capability and not a limit on validity (`[R-CNF-10]`)", and §2.3
  lists the decline among the cannot-establish grounds. The same shape recurs
  for `[R-COD-11]` and for an implemented-versus-unimplemented experimental
  type. I record it because it is exactly the charter's target shape and the
  document has already priced it.

### 4.5 Feature interactions

- **Sparse tile under a filter chain**: a sentinel occupies no bytes, so neither
  stage runs (§19.4 step 4 short-circuits 5 and 6). No interaction.
- **Empty layer under a limit**: covered above; §17.2's note and §21.9's
  per-instance paragraph both handle the quantifier explicitly and agree.
- **Compaction over a record the compactor cannot read**: MU = 1 unknown →
  `[R-WRT-06]` refuses ("any record whose type it does not implement with
  MU = 1" — and §7.4 makes sub-records records, so a layer-scope one bars the
  whole compaction too, which §20.4's table does not contradict, since it never
  says compaction is *available* at layer scope). MU = 0 unknown → the extent
  relocates unread, which §7.2's no-embedded-offsets rule makes safe and §8.1
  covers by no checksum.
- **Compaction over a structurally malformed index entry**: §20.5's regeneration
  paragraph is airtight — the entry "is neither" a sentinel nor re-pointable,
  `[R-IDX-03]` gives it no extent to target, so the compactor meets it and
  `[R-WRT-06]` obliges refusal; no drop is available because a tile-index entry
  is not a record §20.4's table licenses dropping.
- **Compaction over an entry that fails only its stored bytes' crc**:
  `[R-WRT-09]` obliges verifying "every stored tile's entry crc", so it is met
  and refusal follows. The asymmetry with an *appender* (§20.3 step 2 carries a
  malformed entry forward byte-identically) is principled: an appender does not
  move tiles and so never has to re-point.
- **Planar bool + slab + shuffle**: the three cohere. Each plane has its own
  decoded size (⌈P/8⌉ for bool, P·B^c for numeric), slab runs partition each
  channel block independently, packing reads the entries' own offsets and
  lengths, and `[R-COD-10]`'s divisibility holds in every case (s = B^c divides
  P·B^c; s = Q divides P·Q; s = 1 for a packed plane).
- **Codec 1 + filter 2**: `[R-COD-04]`'s equality still holds because
  byte-shuffle is length-preserving; the entry's crc covers the *shuffled*
  bytes.
- **Codec 4 and T24**: I note in passing that "bytes remain after the block"
  cannot arise for codec 4 — `[R-COD-07]` decodes "with the stored length as the
  input size", so the block *is* the extent — nor for codec 1, where T14's
  equality forecloses it. T24 is therefore reachable only under codecs 2 and 3.
  §21.1 nevertheless names T24's "any codec" as its own canonical single-instance
  example, so the cell is settled by fiat and a corpus builder has two codecs to
  build it from. Not a defect.

### 4.6 Degenerate-but-legal files

- **The 128-byte empty file.** Built; reproduces Appendix A.
- **A file whose only record is an experimental-type, MU = 0, PE = 0 record with
  `inline_length = 0` and extent (0, 0).** 28-byte directory. Conforming
  (§10.3's prohibition "binds a writer's conduct, not the bytes"). A curiosity:
  in a file with zero layers, §20.4's drop licence ("a commit that
  *independently* changes … the file's layer set, any layer record's content, or
  another *non-layer* top-level record") may be unreachable, so this ancillary
  can be immortal. Both readings of "changes … another non-layer top-level
  record" yield conforming files, so nothing forks.
- **A file with one layer, every dimension extent 0, codec 4, tile extents
  chosen so P·Q would blow the lz4 cap.** Conforming; §17.2's note is explicit
  and correct.
- **A file with every optional thing absent**: no alignment, no slab, no
  sub-records, no user metadata, every tile a sentinel. Verified constructible;
  `[R-IDX-05]`'s constant becomes available at exactly 2¹⁶-entry segments.

## 5. Findings

### adversary-01 — §20.3 step 4's bar names loci that omit the declaration changes with no witness at all

**Kind: AMBIGUITY. Location: §20.3, `[R-WRT-04]` step 4; §21.7, `[R-ERR-01]`.**

The bar reads:

> "A commit MUST NOT change a layer's declarations in a way that alters, for any
> tile that layer stores **in the generation this commit supersedes**, what §14
> fixes for its stored bytes or how they decode — the set of padding positions
> (§11.3) and the content `[R-SER-05]` fixes there, the decoded size, the byte
> offset of any sample within the decoded tile image, or the codec and filter
> that produced the stored bytes."

and then:

> "The test is the effect on such a tile, and the list names where that effect
> arises rather than standing on its own"

There are two defensible readings, and they part company on a concrete commit.

*Reading A (list-as-exhaustive).* The clause after the dash enumerates the loci
at which the effect can arise; a change touching none of them is not barred.
The sentence's own words support this: the list "names **where** that effect
arises", and §21.7's account of what no check detects is written entirely
against this list — it enumerates witnesses for "a change reaching a byte §14
structurally constrains", "a change reaching the decoded size", "a change
reaching the codec", "a change reaching the filter, or moving a sample's byte
offset within the decoded image", and stops. It contemplates no other kind of
declaration change.

*Reading B (test-as-primary).* The governing test is "alters … what §14 fixes
for its stored bytes **or how they decode**", and the list is illustrative. §14.2
fixes a numeric value as "its type's element size, little-endian", and §14.1
fixes value k as "channel (k mod C)'s value at in-tile ordinal k div C" — so a
channel's declared **type** and the channels' declared **order** are both things
§14 fixes decoding by.

I pick Reading B, because "the list names where that effect arises rather than
standing on its own" is an explicit disclaimer of the list's independence. But
Reading B leaves the list, and §21.7 with it, materially short. Three concrete
commits sit in the gap:

1. **A channel's sample type re-declared at unchanged element size.** The
   type groups of §12.1 by element size are `{bool, int8, uint8}`,
   `{int16, uint16, float16, bfloat16}`, `{int32, uint32, float32}` and
   `{int64, uint64, float64}`. Take an interleaved layer, T = (2, 3), channels
   `a` float32 and `b` uint16, so Q = 6 and the decoded size is 36. Commit a
   directory-only change re-declaring `a` as int32, with the fill bytes
   untouched. Q is unchanged, the decoded size is unchanged, every F^c is
   unchanged, the padding-position set is unchanged, the codec and filter are
   unchanged, `entry_count` and `extent_length` are unchanged, so the tile-index
   region is not even re-emitted. Not one item on the list is touched — yet every
   stored sample of the layer now denotes a different number. And because
   `[R-TYP-05]` makes "every bit pattern of a numeric type's element size … a
   valid sample value", the resulting file is perfectly conforming: no register
   row fires, and every verifier certifies it. Within the same element size,
   only the two moves *into* `bool` are ever caught, and only sometimes —
   planar `uint8 → bool` changes the decoded size from P to ⌈P/8⌉ and fires
   T3/T14, and interleaved `uint8 → bool` fires T2 only if some stored byte
   happens to exceed 0x01. Every move inside `{int16, uint16, float16,
   bfloat16}`, `{int32, uint32, float32}` and `{int64, uint64, float64}` is
   silent.

2. **Two channels' declaration order swapped at unchanged stride.** Interleaved,
   channels `a` and `b` both uint16, Q = 4. Swapping the two channel entries
   leaves the sample stride, the decoded size, the padding set and the codec
   untouched, but moves F_a from 0 to 2 and F_b from 2 to 0. Here the list
   *might* bite, on "the byte offset of any sample within the decoded tile
   image" — but only under one of two readings of "sample". §14.2 gives two
   offsets for interleaved data: the sample's, `(k div C) · Q`, and the value's,
   `(k div C) · Q + F_{k mod C}`. §3.1 defines a **sample** as "the tuple of one
   value per channel at one coordinate", and *that* offset does not move. Under
   the §3.1 reading the list does not reach this commit; under a loose reading
   of "sample" as "sample value" it does.

3. **Two dimension entries' declaration order swapped.** Declare E = (4, 6),
   T = (2, 3) instead as E = (6, 4), T = (3, 2). P = 6, G = (2, 2), N = 4 and
   the decoded size are all unchanged, but §11.4's in-tile ordinal
   `Σ u_i · ∏_{j>i} T_j` changes from `u₀·3 + u₁` to `u₀·2 + u₁`, so every stored
   byte now denotes a transposed coordinate. This turns on the same "sample"
   reading as (2).

The document supplies no reasoning that closes any of the three. What an
implementer does wrong without it: an appender built from the list — which is the
only operational form the bar takes — will permit `float32 → int32`, silently
reinterpreting the whole of a layer's stored data as a directory edit, and no
verifier anywhere will report anything, because §21.7's account never
contemplated the case and so no row exists.

**Byte-level: no**, and I want to be explicit about why, because the strongest
framing tempts the other answer. Resolving this changes nothing about which files
are accepted or rejected: file conformance is "a pure predicate on bytes"
(`[R-CNF-02]`), §21's register is normatively complete over *detectable*
violations and has no row here, and §21.7 already classes the unwitnessed part of
this bar with `[R-LIF-01]` and `[R-GEO-06]` as "a property of a file's history,
which §9.7 does not reconstruct". Every conforming verifier certifies the output
under both readings, and no reader's returned bytes differ for a given file. What
moves is only whether a particular *updater run* was conforming conduct, which no
examination of any byte sequence can decide. I grade it AMBIGUITY rather than
byte-level for that reason, and note that the cost to an implementer is
nevertheless high: this is the one place where a conforming-looking file can
carry wholesale wrong data as a result of a rule the document states but does not
enumerate.

### adversary-02 — §21.5's R8 is the only row in its subsection that does not enumerate the alternatives its own condition text states

**Kind: OBSERVATION. Location: §21.5, row R8; §21.8, `[R-ERR-02]`; §21.1.**

R8 reads:

> "| R8 | A user-metadata document contains a non-finite number, in any form — a
> magnitude whose binary64 interpretation overflows (`1e400`) and the bare tokens
> `NaN`, `Infinity` and `-Infinity` alike | top-level document; layer sub-record
> document | reader | extent use | `[R-MTA-04]` (R-CNT-25) |"

Two instances: the two containers, and nothing else. §21.1's discipline is:

> "An instance names a field the condition ranges over, a container it can occur
> in, one of several alternatives the condition text states, or any combination
> of the three … a row whose check ranges over a family without the condition
> changing shape states that range as a single instance (T24's *any codec*), and
> one whose members give the condition materially different shapes enumerates
> them (T15, T25)."

Derived from the rule the row accounts for rather than from the row: §18.2's
bullet states two structurally distinct predicates joined by "or" —

> "A document is unreadable if it contains a number whose binary64
> interpretation is not finite — which covers a magnitude that overflows on
> conversion, `1e400` being the ordinary case — **or** any of the bare tokens
> `NaN`, `Infinity`, or `-Infinity`, which RFC 8259 does not admit and some
> parsers accept regardless."

These are materially different shapes by every measure §21.1 offers. `1e400` is a
*well-formed JSON number* that a conformant RFC 8259 parser accepts and that only
a binary64 conversion rejects; `NaN` is *not JSON at all*, and the rule exists
solely to close a parser-tolerance hole the bullet names in the same breath. A
corpus vector for one exercises a numeric-conversion path; a vector for the other
exercises token acceptance. That is a wider gap than T15's zlib-versus-gzip
wrappers or T25's three malformed-stream shapes, both of which §21.1 cites as
examples that *must* be enumerated.

The internal evidence is stronger than the analogy. Every other §21.5 row whose
condition text states alternatives enumerates them: R7 gives three
("not well-formed JSON; top-level value not an object; leading U+FEFF") × two
containers = 6; R5 gives two failure modes × two positions × two containers = 8;
R6 gives two × two = 4; R1 gives two × two = 4. R8 is the only row in the
subsection that states alternatives in its Condition cell and declines to carry
them into its Instances cell — the word "alike" being the whole of the argument
for collapsing them.

I picked the reading that R8 is short. Under it, R8 is two instances where it
should be four (the three bare tokens are properly one family, like T24's "any
codec"), and §21.8's "121 conditions over **277** instances" — which
`[R-ERR-02]` makes normative, requiring "one vector per instance" — is short by
two, with two corpus vectors unbuilt. Under the other reading the cell is
deliberate and the total right. Nothing in §21.1 decides between them, because
"materially different shapes" is left to judgment and this is the one row where
the judgment was made the other way.

One consequence worth stating: a vector for the bare-token instance necessarily
also exercises R7's "not well-formed JSON", since RFC 8259 does not admit the
token. §24's `[R-VEC-02]` handles that ("where a condition cannot be isolated …
the entry records every row the file exercises and says which it was built for"),
so the overlap is a construction note, not an obstacle. §21.1's list of
specialisation pairs ("F1 of F6 and of F8, F35 of F36, L24 of L25") does not
include R8-of-R7, which is a second, smaller sign that the bare-token alternative
was not carried through the register's own machinery.

**Byte-level: no.** Instance counts govern the conformance corpus (§21.8, §24)
and nothing else; §21.8 says in terms that "A row without a vector is a gap in
the corpus, not a licence to skip the check", so a reader's or verifier's
obligation is identical under both readings and no file's verdict moves. The cost
is two missing vectors and a normative total that does not match its own
discipline.

*Contamination note.* My runtime placed a `git status` block in context whose
commit subjects mention an ADR and the row label "R8". I reached this finding by
counting all 121 Instances cells mechanically, then auditing them against
§21.1's two stated axes and against the other nine rows of §21.5 — R8 is the
residue of that audit, and it is the only cell in the whole register that failed
it. I have not read the ADR and do not know what it decided; if it settled this
question the other way, this finding is answered, and I record the exposure so
that the answer can be checked rather than assumed.

### adversary-03 — §2.3's acceptance duty is lifted by any unknown MU = 1 record, where only a top-level one should lift it

**Kind: OBSERVATION. Location: §2.3, `[R-CNF-03]`.**

§2.3 defines the conforming reader's acceptance duty as:

> "A reader MUST accept every conforming file of a format major version it
> implements, carrying no record of a type it does not implement with
> MUST_UNDERSTAND = 1 — in a conforming file such a type is necessarily from the
> experimental range, since a reserved-range type carrying MU = 1 is itself a
> violation — and none of whose values exceeds the minimum guarantees of §21's
> limits table"

"no record of a type it does not implement with MUST_UNDERSTAND = 1" carries no
*top-level* qualifier, and §7.4 makes sub-records records in terms ("Sub-records
are layer-scope records"). Read literally, a file one of whose layers carries an
experimental-range MU = 1 sub-record falls outside the acceptance duty entirely,
and a reader may refuse the whole file. That is precisely the outcome two other
passages forbid. `[R-CNT-18]`:

> "an unknown sub-record type with MU = 1 is reject-layer, and where the file is
> otherwise conforming a reader MUST NOT reject the file for it"

and §21.6's closing paragraph, which §2.3 itself points at for "the other two"
grounds:

> "The qualifier is load-bearing — the same type as a layer sub-record is
> reject-layer and never a ground to refuse the file (`[R-CNT-18]`), so only the
> top-level case is a file a reader refuses"

So the question *is* decided — by `[R-CNT-18]`'s MUST NOT, which no lifting of a
duty can override — and §21.6 says the qualifier is load-bearing at exactly the
point where §2.3 omits it. But deciding it costs three cross-references from the
one paragraph an implementer reads first, and §2.3 is the definitional passage a
reader's acceptance behaviour is built from. The construction that exposes it:
a two-layer file, layer A clean, layer B carrying an experimental-range
(≥ 0x8000) MU = 1, PE = 1 sub-record, otherwise conforming. The correct
behaviour is to open the file, list both layers, serve A, and reject B; a reader
built from §2.3 alone refuses the file.

**Byte-level: no.** The file's conformance is unchanged under either reading
(§21.6 makes it conforming), and `[R-CNT-18]`'s MUST NOT forecloses the refusal,
so no conforming implementation may actually diverge. What is at stake is only
how expensive it is to discover that.

## 6. Attacks that did not survive — the sentence that closed each

For completeness, the constructions I built or sketched that the document
forecloses outright, with the closing text:

- **A trailer mimic inside a tile payload, at exact end of file.** §6.2's note:
  caught at the directory CRC. §21.6 records the general case as inert
  ("nothing enumerates slack"), and §9.6 requires recovery output to be
  re-verified whole.
- **A zeroed index region read as all-sparse.** §15.2's rationale: offset 0 /
  length 0 is "loudly invalid" (T8, T10), never a sentinel; an all-0xFF region
  is invalid too because a sentinel's crc is 0 (T6).
- **A shrink that hides data inside a still-stored tile's padding.** §20.3 step
  4 permits it "only where those bytes already hold the channel's recorded
  fill", and §23.1 works through both cases and argues their exhaustiveness
  correctly ("the bytes either travel out of the live state or stay in the
  structure that carried them").
- **A commit that escapes the bar by unstoring as it re-declares.** §20.3:
  "the tense is the bar's, so a commit does not earn this permission by emptying
  the layer as it re-declares it", and again for shrink.
- **A commit that grows an extent past a bound the layer's own declarations
  impose.** §20.3: "a growth is permitted exactly where the geometry it produces
  satisfies every rule that geometry is subject to", with L44 and `[R-ENC-04]`
  named and the list expressly not exhaustive.
- **A stale slab declaration carried forward.** `[R-SLB-04]` plus its note: no
  row of its own, because every file exhibiting one exhibits L41 or L42.
- **A compactor reusing the input's file_id.** `[R-WRT-06]`: "a new draw under
  §9.3's randomness advice, not merely a value compared against the input's".
- **A compactor writing flags = 0 over an input's ignore-lane bits.** §6.3 and
  `[R-WRT-06]` both state the carry-forward, and Appendix G item 8 restates it
  for the profile.
- **A record extent slot of (0, N).** F33's own cell resolves the attribution:
  it "reaches the block through its zero offset and is theirs rather than F31's
  or L16's" — i.e. F30/L15, not the offset-range rows.
- **A bool byte of 0x02 at a padding position.** T2 excludes it and hands it to
  T4, "the two rows together covering `[R-SER-08]`"; I checked that T2 and T4
  between them cover every interleaved bool byte in every tile.
- **A reader that returns fill for a damaged tile.** `[R-TYP-09]` and
  `[R-CNF-09]`: "a rejection is never satisfied by returning fill".
- **A partial slack total that under-counts on overlap.** §5.2's "F less the
  bytes claimed by the claimants the walk did enumerate" reads as the *union* of
  claimed bytes, under which the stated guarantee ("an upper bound … never an
  under-count") holds; only a sum-of-lengths reading breaks it, and nothing in
  the text asks for a sum.
- **`[R-MTA-09]`'s "the bound above".** The antecedent is ambiguous between the
  decoded-size bound and the frame's declared window, both of which the
  paragraph discusses — but §21.5's preamble names both explicitly ("declines
  the decode on the size bound **or on the frame's declared window**") and §2.3
  lists the decline generically, so the verdict machinery is the same either
  way and I did not have to guess.

## 7. Confidence

I would rate an implementation built from this text alone as very likely to
interoperate. Every structure I had to lay out was pinned; every arithmetic
identity I checked reproduced; the register's row set is, so far as I can derive
it, complete; and the register's total arithmetic is exactly right. The one place
I would expect two honest implementations to produce materially different
*results* is adversary-01, and even there the divergence is invisible to every
verdict the document defines — which is itself the finding.
