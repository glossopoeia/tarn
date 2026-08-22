# Round 19 — Register hunter — working transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in full (4,364 lines), in five reads plus targeted `sed`/`grep`/`awk` over that
same file. I ran two local Python computations that read no file: a CRC-32C
implementation used to check four constants the document states, and a script
that re-counted the register's rows and instances from text I had already read
(it opens `spec/tarn.md`, the one permitted file, and nothing else). I created
one directory for this transcript and wrote this file. I read no ADR, no
`docs/`, no `conformance/`, no `registry.json`, no `PLAN.md`, no `AGENTS.md`,
no git history, and I did not list the output directory. I did not consult the
web. Where I used prior knowledge of DEFLATE/zlib/gzip/zstd/LZ4 framing it was
only to generate suspicions about T13–T25; every conclusion below is settled
from this document's own text.

## 1. What I set out to do

Charter: audit §21, the error-handling register, against the rules it restates
and against itself. Six axes: row-versus-rule agreement, completeness in both
directions, every cross-reference to a row, the counting, the outcome
vocabulary, and the limits. Plus the round-wide instruction to cover §20.5,
§21.7, §23.1 and Appendix G first and then keep going.

I did the counting first because it is mechanical and because a total that does
not reproduce would have reframed everything else. It reproduces exactly. Then
I built the verifier §21 describes, on paper, structure by structure, and
recorded every point at which I had to guess.

## 2. The counting — worked in full

§21.1 fixes the arithmetic:

> Instances within a cell are separated by semicolons, and a cell reading — is
> one instance; the count is therefore mechanical once the cell is written.

So the count is a text operation on the Instances column. I did it by hand
first and then re-derived it with a script (splitting each row's third cell on
`;`, treating `—` as 1) to catch transcription slips. Both agree.

### §21.2 — file scope

F1 2, F2 6, F3 2, F4 1, F5 2, F6 2, F7 4, F8 1, F9 1, F10 1, F11 1, F12 1,
F13 1, F14 1, F15 1, F16 1, F17 2, F18 1, F19 1, F20 1, F21 1, F22 1, F23 2,
F24 1, F25 1, F26 1, F27 1, F28 2, F29 3, F30 2, F31 1, F32 1, F33 5, F34 1,
F35 1, F36 1.

Running sum: 2, 8, 10, 11, 13, 15, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30,
31, 32, 33, 34, 35, 37, 38, 39, 40, 41, 43, 46, 48, 49, 50, 55, 56, 57, **58**.

36 rows. §21.2's header says "36 conditions." ✔

### §21.3 — layer scope

L1 8, L2 9, L3 1, L4 2, L5 1, L6 1, L7 2, L8 2, L9 2, L10 1, L11 1, L12 2,
L13 1, L14 3, L15 4, L16 2, L17 2, L18 3, L19 1, L20 1, L21 4, L22 4, L23 4,
L24 1, L25 1, L26 1, L27 1, L28 1, L29 3, L30 2, L31 3, L32 3, L33 4, L34 4,
L35 1, L36 2, L37 1, L38 1, L39 3, L40 1, L41 3, L42 1, L43 3, L44 3, L45 3,
L46 2, L47 2, L48 1, L49 4.

Running sum: 8, 17, 18, 20, 21, 22, 24, 26, 28, 29, 30, 32, 33, 36, 40, 42, 44,
47, 48, 49, 53, 57, 61, 62, 63, 64, 65, 66, 69, 71, 74, 77, 81, 85, 86, 88, 89,
90, 93, 94, 97, 98, 101, 104, 107, 109, 111, 112, **116**.

49 rows. §21.3's header says "49 conditions." ✔

L2's nine is worth spelling out because it is the largest cell and it is where a
miscount would hide: `layer record extent_offset + extent_length` (1),
`sub-record extent_offset + extent_length` (2), `N = ∏⌈Eᵢ/Tᵢ⌉` (3), `P = ∏Tᵢ`
(4), `N·P` (5), `C·N (which dominates the max disk ordinal (C−1)·N + (N−1))`
(6), `P·Q (which dominates V = P·C)` (7), `P·Bᶜ` (8),
`entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4` (9).

I checked the two domination claims because they are the reason the cell is nine
and not eleven. Max disk ordinal = (C−1)·N + (N−1) = C·N − 1 < C·N ✔. And
Q = Σ Bᵢ over all channels, each Bᵢ ≥ 1, so Q ≥ C and P·Q ≥ P·C = V ✔. I also
asked whether the packed-bool decoded size ⌈P/8⌉ needs a tenth instance under
§21.1's layout rule; it does not, since ⌈P/8⌉ ≤ P and P is already instance 4,
so ⌈P/8⌉ can never exceed 2⁶³−1 without P doing so first.

### §21.4 — tile scope

T1 1, T2 1, T3 6, T4 4, T5 1, T6 1, T7 2, T8 1, T9 1, T10 1, T11 2, T12 1,
T13 2, T14 6, T15 2, T16 1, T17 1, T18 2, T19 1, T20 1, T21 3, T22 6, T23 1,
T24 1, T25 3, T26 3.

Running sum: 1, 2, 8, 12, 13, 14, 16, 17, 18, 19, 21, 22, 24, 30, 32, 33, 34,
36, 37, 38, 41, 47, 48, 49, 52, **55**.

26 rows. §21.4's header says "26 conditions." ✔

### §21.5 — ignored records

R1 4, R2 2, R3 2, R4 12, R5 8, R6 4, R7 6, R8 2, R9 2, R10 2 = **44**.
10 rows. §21.5's closing line says "10 conditions." ✔

### Grand total

121 conditions, 58 + 116 + 55 + 44 = **273** instances.

§21.8: "Every row of §21.2 through §21.5 — 121 conditions over 273 instances".
Both numbers reproduce exactly. No finding here.

### Are the cells written the way §21.1 says to write them?

The count is mechanical *once the cell is written*, so I also checked the cells
against §21.1's substantive rules. The three that matter:

- Layout-varying derived quantities enumerate their formulas. T3 and T14 and
  T22 each give three layout formulas × two directions = 6 ✔; T21 and L44 give
  three formulas × one direction ("larger than", "exceeds") = 3 ✔; T4 gives the
  four layout×type combinations ✔; T26 gives the three mandated strides ✔.
- Magnitude comparisons enumerate both directions only where the text does not
  bound them. L30 ("differs from") = 2 ✔; L21 ("does not equal") = 2 layouts ×
  2 directions ✔; L22 = 2 directions plus the two alternatives its own text
  states ✔; T1, L37, L38, F14, F20 (checksum against checksum, no ordering) = 1
  each ✔.
- Nonzero tests and single predicates over several fields are one. L20
  ("declares both A ≠ 0 and S ≠ 0") = 1 ✔; F25 (MU = 1 with PE = 0) = 1 ✔;
  F26 ("any of ... bits 2-15") = 1 ✔.

One pleasing cross-check: L36 (layout value) has two instances, `layout 0` and
`reserved 3-255`, and no experimental instance — which is exactly right,
because §10.2's `[R-EXT-02]` says channel layout is one of the two spaces with
no experimental range. L33 and L34 split their reserved ranges in two because
§11.4 and §12.2 split them in two; L31, L43, L45 do not because §15.1, §17.2
and §17.3 do not. The Instances column tracks the value-set sections faithfully.

## 3. Outcome vocabulary

§2.4 defines four reader outcomes — reject-file, reject-layer, reject-tile,
ignore-record — plus **preserve-verbatim** as an updater obligation orthogonal
to them.

Every row's outcome is the outcome its subsection header states: §21.2
reject-file, §21.3 reject-layer, §21.4 reject-tile, §21.5 ignore-record. All
four defined reader outcomes are therefore reachable, one subsection each.
preserve-verbatim is reachable through §20.4's table, which §2.4 names
("its MU = 1 and MU = 0 / PE = 1 rows"), and correctly carries no register row,
since it binds no reader.

Detector/detection-point vocabulary: §21.1 says detection points name §19.2's
reader tiers — open, layer access, tile use, extent use — "or *certification*
for the rows a verifier detects". I checked all 121 rows: every row whose
Detector is `verifier` has Detected `certification` (F7, F25, F26, F27, F28,
F33, F36; L18, L25, L40, L41, L42, L46, L47, L48, L49; T2, T4, T5, T26 — 21
rows), and every reader row uses one of the four tier names. R1 is the only
cell with two detection points ("open (top-level); layer access (sub-record)"),
which is correct: its four instances split by container and a top-level
record's inline payload is read at the open (§19.1 step 4) while a sub-record's
is read at layer access (§19.3).

I also checked §21.1's claim that for verifier rows "the governing rule states
what a reader does", against all 21: `[R-CNT-05]` ("readers check neither"),
`[R-CNT-12]` ("readers MUST ignore them" / "MUST treat the record as PE = 1"),
`[R-MTA-05]` ("readers process the document unchanged"), `[R-CNT-22]` ("A
reader MUST apply a known type's specified semantics regardless"), `[R-CNT-13]`
("readers are not obligated to detect overlap"), `[R-CNT-15]` ("Readers of both
apply the MU rule above unchanged"), `[R-SLB-01]` ("readers are not obligated
to"), `[R-SLB-03]` (same), `[R-SER-05]` ("is not obligated to check it"),
`[R-SER-08]` (the resolved byte). All hold. `[R-COD-10]` (T26) is the one that
does not state a reader clause of its own, but T26's own text routes detection
to T2/T4, whose rules do.

## 4. Row-versus-rule, structure by structure

I worked this by building the verifier rather than by reading the table
top-to-bottom, so that a row without a rule and a rule without a row would both
surface. Below is the walk, with only the places I had to stop and think
recorded in detail.

### 4.1 Open — trailer and directory

`[R-CNT-06]` names eleven gates. Mapping: trailer magic → F8; trailer CRC →
F14; version gate → F18 (version_major 0) and, for a major the reader does not
implement, §21.6's capability refusal, correctly no row; flag gates → F19;
committed_file_length = transport size → F17; multiple of 64 → F13;
dir_offset ≥ 16 → F9; dir_length ≥ 4 → F16; dir_offset + dir_length ≤ F − 64 →
F10; 1 ≤ generation → F11, and ≤ 2⁶³−1 → F2's `generation` instance; file_id ≠ 0
→ F12; reserved bytes zero → F15. Every gate registered, nothing registered
that is not a gate. ✔

§21.2's preamble reasoning about a foreign format major checks out against
`[R-CNT-24]`. `[R-CNT-24]` fixes across every major: the trailer magic at
F − 64, version_major/version_minor at F − 56, a CRC at F − 4, and the front
signature block. The preamble names exactly four rows as reaching such a file —
F8, F1's trailer-magic instance, F14, and F6 with F1's front-block instance —
and those are precisely the rows whose subject is one of those fixed fields.
The remaining 48 trailer bytes ([12, 60): flags, generation, dir_offset,
dir_length, committed_file_length, file_id, reserved) are major-1's to define,
so F9–F13, F15–F17 and F19 correctly do not reach it. Arithmetic: 64 − 8 (magic)
− 4 (version pair) − 4 (CRC) = 48 ✔, matching "A future major MAY redefine only
the remaining 48 trailer bytes".

I checked the one claim in that preamble that this document cannot get from
§6.3: "version_major = 0 declares no major at all and is permanently invalid in
every one". §6.3 says only "A reader MUST reject-file when version_major is 0
(invalid)"; the *permanence* across majors is asserted in §21.2 and §21.6 and
nowhere established in §6.3. I decided not to report it: `[R-CNT-07]`'s second
limb ("or is a major it does not implement") reaches version_major = 0 under
every reading, so F18's registration and outcome are right either way, and no
implementation can act differently.

### 4.2 The record walk

`[R-CNT-12]` → F24 (type 0), F29 (framing/residue), F25 and F26 (flag bits,
verifier), L13, L14, L46, L47. `[R-CNT-13]` → F30/F31/F32 and L15/L16/L17 for
slots, F33 and L18 for overlap. `[R-CNT-14]` → F34, L19. `[R-CNT-15]` → F35,
F36, L25. `[R-CNT-22]` → F28, L49. `[R-CNT-18]` → L23, L24, L26.

Coverage of the flag rows across all record placements is complete without
overlap: F25/F26 bind "a non-layer top-level record", L46/L47 bind "a layer
record's or sub-record's". F28 binds "a non-layer top-level record of a type
§7.3 registers" — which in format major 1 is exactly the top-level
user-metadata record — and L49 binds "a layer record, or a sub-record of a type
§7.3 registers". Union = every record; intersection = empty. ✔

F31 says "extent_offset in 1-15" where L16 says "extent_offset < 16"; both are
under the "nonzero extent slot" premise, so both denote 1..15 and the
asymmetry is cosmetic.

Something worth recording because I initially thought it was a hole: a record
the reader *ignores* (unknown type, MU = 0; or a user-metadata record whose
document is ignore-record) still has its extent slot validated as a
scope-level error, and its extent is still a coverage claimant. §2.4 says
ignore-record means "skipped as though absent", which would suggest otherwise.
The document decides it twice and unambiguously: §5.2 classes "a record extent
(the bytes any record's extent slot references, **whatever the record's type**,
§7.2)" as a structure, and §9.7's walk reaches "each record's extent". So the
"as though absent" is about semantics, not coverage. Not a finding — but it is
the single place where an implementer most plausibly builds the wrong verifier
and gets a wrong slack total, and the resolution is only findable in §5.2 and
§9.7 rather than in §2.4 or §21.5.

### 4.3 The layer record

I walked §7.4's table field by field against §21.3. name → L3/L5/L6 and F4
(uniqueness, file scope, correctly not layer scope); layout → L36;
linearization → L33; codec → L43; filter → L45; A → L39; S → L1 (domain) and
L20 (mutual exclusion); A_slab → L28 (S = 0 with A_slab ≠ 0) and L29
(S ≠ 0 with a bad A_slab, A_slab = 0 included); rank d and channel count C →
L32; dimension entries → L1, L4, L7, L8, L9, L32; channel entries → L4, L7, L8,
L9, L30, L34, L35; index_encoding → L31; entry_count → L1, L2, L21; 
crc_of_crc_array → L27 and L37; sub-records → L13, L14, L19, L23, L24, L25, L26.
Every table constraint has a row; every row lands on a table constraint. ✔

`[R-ENC-03]`'s domain rule: I checked that every field it binds has a row. It
binds "every offset, length, extent, and count ... entry counts and slab run
lengths included". F2 covers the file-scope fields, L1 the layer-scope ones,
T11 the index entry's. A and A_slab are not offsets/lengths/extents/counts and
are bounded instead by L39 and L29's "above 2^62" instances, so there is no gap
and no double registration. inline_length is a u32 and cannot exceed 2⁶³−1;
name and fill length prefixes are u8. Complete. ✔

Worked example check (§7.4's annotated payload), because L23's four instances
are the four regions it names and I wanted to be sure the regions partition the
payload: name 4 + nine scalars 34 (layout 1, linearization 2, codec 2, filter 2,
A 8, S 8, A_slab 8, rank 1, C 2 = 34 ✔) + dimension entry 18 (2 + 8 + 8) +
channel entry 12 (5 + 2 + 5) + trailing fixed 13 (1 + 8 + 4) = 81 ✔, matching
the stated inline_length. Grid ⌈100/32⌉ = 4 ✔. Extent length 4×20 + ⌈4/2¹⁶⌉×4 =
84 ✔.

### 4.4 The index

§15.3's classification table has eleven rows. Mapping to the register:
sentinel → §21.6 (non-violation); sentinel with crc ≠ 0 → T6; exactly one field
sentinel → T7; length 0 → T10; offset < 16 → T8; either field > 2⁶³−1 → T11;
sum overflow → T12; sum > F − 64 → T9; stored bytes fail crc → T1; intra-layer
overlap → L18; extra-layer overlap → F33; alignment/slab invariant → L40, L41,
L42. Eleven rows, thirteen register entries, no leftovers in either direction. ✔

§15.3 says "Six rows are marked *structural*"; I counted six ✔, and they are
exactly T6, T7, T8, T10, T11, T12 — the six the compaction text in §20.5 relies
on ("An entry §15.3 classifies reject-tile on a structural ground is neither").
T1 is the well-formed one, and §15.3, §16.2, §9.7 and §20.5 all treat it that
way consistently.

T11's "the value being distinct from the all-ones sentinel" is what keeps T7 and
T11 disjoint; without it a length of 2⁶⁴−1 would satisfy both.

### 4.5 Codecs, filters, serialization

`[R-COD-04]` → T14. `[R-COD-05]` → T15, T16. `[R-COD-06]` → T17 (magic), T18
(skippable/second frame), T19 (dict id), T20 (checksum flag), T21 (window), T22
(content size). `[R-COD-07]` → L44 (declaration) and T23 (frame instead of
block). `[R-COD-08]` → T24 (inexact consumption), T25 (malformed), and T3
through `[R-SER-07]`. `[R-COD-02]` → T13. `[R-COD-10]` → T26 and §21.7.
`[R-SER-05]` → T4, T5. `[R-SER-08]` → T2 (+ T4's interleaved-bool instance).
`[R-SER-06]` → L36. `[R-SER-09]` → §21.6. Nothing left over. ✔

Two rows made me stop. `[R-COD-02]` and `[R-COD-05]` carry no BCP 14 keyword
at all — they are declarative ("Every stored tile is independently decodable
…"; "The stored bytes are exactly one DEFLATE compressed data stream … raw, not
a zlib … wrapper"). T13, T15 and T16 nevertheless carry Detector `reader`,
Detected `tile use`, outcome reject-tile. I concluded this is *not* a defect:
§21.1 says the Governing rule cell names "the requirement that defines it",
while the *detector* is what the register itself assigns and `[R-CNF-04]` binds
readers to ("A reader MUST detect every violation the error register (§21)
assigns to the reader as its detector"), and the *outcome* follows from the
owning scope, which §17's opening fixes at the tile. Each of the three rows then
says in its own Condition cell where the procedure lives ("the check that
detects it is T24's or T25's, and this row records the cause rather than a
procedure of its own"). That is coherent. I checked the routing claim for T15
against the byte patterns: a gzip member begins `1F 8B`, and 0x1F read LSB-first
as a DEFLATE block header gives BFINAL = 1, BTYPE = 0b11 — the reserved block
type, which is T25's own first instance ("deflate block type 3 / invalid
Huffman table"). A zlib member's `78 xx` gives BTYPE = 00, a stored block whose
LEN/NLEN check is drawn from the FLG byte and the first compressed byte, which
fails almost surely; and if it did not, the size check T3 or the residue check
T24 would. So the routing holds.

T13's instance "lz4 block whose match offset reaches back into a previous tile's
output" and T25's "lz4 match offset 0 or match reaching past produced output"
are the same byte-level condition described from two directions — an offset
larger than the bytes produced so far reaches before the output buffer's start.
Consistent.

### 4.6 User metadata

`[R-MTA-04]`'s four restrictions map to R7 (object + no BOM), R8 (finite
numbers), R9 (duplicate keys), and R5/R6/R10 (UTF-8 throughout, and the key
name rules). `[R-CNT-25]`'s four "ways a document can be unreadable" map to R2
(extent CRC), R1 (encoding), R3 (decode failure), R5–R10 (content).
`[R-MTA-09]`'s frame constraints map to R4's six alternatives × two containers.
Nothing left over in either direction. ✔

R4's twelve: the six constraints are the magic, no skippable frame, no second
frame, no nonzero dictionary ID, no content-checksum flag, and the frame
occupying the extent's bytes before the terminal CRC — exactly what
`[R-MTA-09]` states, with "bytes remaining after the frame" answering
"occupying the extent's bytes before its terminal CRC". ✔

§21.5's preamble does the encoding-space bookkeeping correctly and it is worth
recording because it is where I expected to find a defect and did not: encoding
0 and reserved 3–0x7F are violations (R1), the experimental range ≥ 0x80 is a
conforming file (§21.6's row), and the distinction is exactly `[R-MTA-10]`'s —
"what `[R-MTA-10]` withdraws is the document's content rules, never the
encoding byte's own value set". That is the same partition `[R-EXT-03]` makes
between conduct and bytes, applied to one space, and it holds.

### 4.7 Coverage, slack, limits

`[R-CNT-02]` → F33 and L18 for overlap, and §5.2's own Note explains why the
"belongs to no class" half can have no row ("a register row for it would be a
row no file could exhibit"). `[R-CNT-05]` → F7. `[R-CNT-21]` is a verifier
reporting obligation, not a file condition, and correctly has no row; §21.6's
slack entry restates it.

## 5. Every cross-reference to a row

I extracted every `[FLTR]NN` token outside the four tables and resolved each.

| Site | Cites | Resolves? |
|---|---|---|
| §5.2 `[R-CNT-21]` | L18, L40–L42 | ✔ L18 overlap, L40–L42 placement, all verifier/reject-layer |
| §9.6 `[R-LIF-06]` | F8, F17 | ✔ both are `[R-CNT-06]` gates; see note below |
| §17.2 deflate Note | T24 | ✔ trailing byte after the stream |
| §20.3 step 4 | L44 | ✔ the lz4 decoded-size cap |
| §20.5 `[R-WRT-06]` | F36, L25, R1 | partial — **register-06** |
| §21.1 specialization | F1/F6/F8, F35/F36, L24/L25 | ✔ all three relations hold |
| §21.1 instance rules | T24, T15, T25 | ✔ |
| §21.1 verifier-row para | F27, L48 | ✔ (the `[R-MTA-05]` pair) |
| §21.2 preamble | F8, F1, F14, F6, F18 | ✔ |
| F33's cell | F9/F10, F31/F32, L16/L17, T8/T9 | ✔ all eight are the bounds rows |
| T2's cell | T4 | ✔ |
| §21.6 experimental row | F36, L25 | ✔ |
| §21.6 closing | F18, F35, F36, L24, L25 | ✔ |
| §21.7 | T2, T4, T5, T3, T14, T15, T17, T23, T25 | ✔ each row says what is claimed |
| App. H verifier | F1, F6, F7, F36, L25, R1 | ✔ |

Two of these deserve a paragraph.

**§9.6.** "a file whose final 64 bytes are not a valid trailer fails
`[R-CNT-06]`'s gates on the bytes handed over (§21.2 rows F8 and F17)". §9.5's
Note gives the same account with three rows — "the magic, the CRC, or
committed_file_length against the transport size" — i.e. F8, F14, F17. §9.6
names two of the three. I decided not to report it. The two sections are making
slightly different points (§9.5 enumerates what a reader can observe; §9.6 only
needs an existence claim that *some* gate fails), F14 is registered either way,
and no implementation can behave differently on it.

**§20.5.** "the other two reaching such a file only as values this text still
registers as reserved-range violations (F36, L25, R1)". The three rows cited do
say what is claimed. But the "other two" of §10.1's four vehicles are *new
record types* and *new values in the ranges this specification reserves*, and
the second of those covers eight numeric spaces (§10.2's table), not one. A
reserved-range linearization, sample type, codec, filter, channel layout or
index encoding is registered at L33, L34, L43, L45, L36 and L31 respectively —
six rows the parenthesis omits. See **register-06**; I grade it low because the
sentence's *conclusion* survives (all of them are violations, so a conforming
input carries none), and because the three cited rows are exactly the ones a
compactor could carry forward without its own §19.3 layer validation catching
them, which may be the intent.

## 6. Findings

### register-01 — §23.1's closed enumeration of how a commit removes sample data omits unstoring a tile

§23.1, `[R-PRV-01]`:

> A commit removes sample data two ways — superseding it, and a shrink that
> de-addresses tiles (§20.3 step 4) — and a dropped ancillary record's extent
> (§20.4) goes the same way; no commit removes a layer at all.

The closure argument is the last clause: the third conceivable way, removing a
layer, is unavailable, and §20.4 confirms it ("No commit therefore removes a
layer record, or a user-metadata record at either scope"). That much holds.

But §20.3 step 4 names three dispositions an index re-emission gives an entry,
not two:

> with entries for tiles this commit stores or supersedes written to their new
> state, entries for tiles that become unstored written as the sentinel

"become unstored" is listed *beside* "stores or supersedes", not inside it. And
§23.2 names that case explicitly and points back here for its account:

> a tile unstored by a later commit leaves its earlier payload in the file as
> slack (§23.1)

So a commit that writes a sentinel over a stored entry — without shrinking any
extent — removes sample data (those positions now read as fill) by a route
§23.1's two-item enumeration does not name and §23.2 assumes it does.

Two readings I can defend. (a) "superseding it" is narrow — replacing a stored
tile's bytes with new bytes — which is how §20.3 step 4 uses the word beside
"become unstored"; then the enumeration is short by one. (b) "superseding it"
is broad — making bytes unreachable — which is how §5.2 uses it ("everything an
earlier commit superseded" = all slack); then the enumeration is complete but
"a shrink that de-addresses tiles" becomes a redundant sub-case rather than a
coordinate one, which is not how the sentence reads.

I picked (a): §20.3 step 4 is the section §23.1 cites, and it keeps the two
apart. An implementer building a "what did this commit make unrecoverable?"
report from §23.1 alone omits the sentinel case and under-reports.

Not byte-level. `[R-PRV-01]`'s MUST NOT is quantified over "any commit that
makes sample data unreachable", which reaches the sentinel case whatever the
enumeration says, and it constrains how a tool *describes* a commit, not what
it writes.

### register-02 — §21.6's second capability refusal is stated file-wide, but for a layer sub-record `[R-CNT-18]` confines it to the layer

§21.6, closing prose:

> Two structural cases are **conforming files a reader nevertheless refuses**.
> ... The second is an **experimental-range record type carrying MU = 1**
> (§10.2, §10.3): `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]`
> makes the file conforming all the same

§7.4, `[R-CNT-18]`:

> an unknown sub-record type with MU = 1 is reject-layer — never reject-file —
> and with MU = 0 is ignore-record

The case as stated ("an experimental-range record type carrying MU = 1", with
no placement qualifier) reaches a layer sub-record, and it cites §10.3 — the
one section that splits the two placements explicitly:

> for record types, the MU-bit outcome of `[R-CNT-15]` at file scope and
> `[R-CNT-18]` for layer sub-records

§20.4's table splits them the same way ("At layer scope an unknown critical
record blocks modification of that layer, leaving other layers editable
(`[R-CNT-18]`). At file scope no commit is available at all"). §21.6 does not:
it frames the outcome as refusing the file and attributes it to `[R-CNT-15]`
alone.

This matters because §2.3 designates §21.6 as the authority. `[R-CNF-03]`:

> A reader MUST accept every conforming file of a format major version it
> implements, carrying no record of a type it does not implement with
> MUST_UNDERSTAND = 1 ... (§21.9's `[R-ERR-04]` governs a refusal on that last
> ground; §21.6's closing paragraph names the other two)

Concretely: a conforming file with layers X and Y, where Y's layer record
carries a sub-record of experimental type 0x8001 with MU = 1. A reader
following §21.6 refuses the file. A reader following `[R-CNT-18]`, §10.3 and
§20.4 rejects layer Y and serves X.

I picked `[R-CNT-18]`: it is the rule that defines the sub-record case, §10.3
and §20.4 agree with it, and §21.1's tie-break principle ("where such an entry
and the rule it cites diverge, the rule governs") points the same way — though
strictly that clause is written for §21.6's *table entries* and this is prose
after the table, so the tie-break is not formally available here.

Also worth noting inside this finding: the justification the same paragraph
gives for neither case being a register row — "the register enumerates
file-conformance violations (§21.1), and a file this document declines to judge
is not one" — covers only the *first* case. The second case's file is expressly
judged, and judged conforming; the reason it is not a row is that it is not a
violation, not that the document declines to judge it.

Not byte-level, and I want to be explicit about why I am not claiming it,
because I nearly did. `[R-CNF-03]`'s MUST-accept is relieved under *both*
readings — the file carries a record of a type the reader does not implement
with MU = 1, whatever its placement — so a reader that refuses the whole file
violates no MUST. And `[R-CNT-18]`'s "never reject-file" carries no BCP 14
keyword, so under §2.1 it has no force of its own, and `[R-CNF-04]`'s duty to
"apply the outcome class this specification assigns" reaches only register rows,
which this condition (a conforming file) is not. So both behaviours are
licensed and no verdict is forked. What is lost is the *narrowest scope* a
reader should refuse, which is a real cost to an implementer and to §24's
sibling-vector machinery, but not a byte or a verdict two conforming
implementations must disagree about.

### register-03 — §21.7 states a necessary condition for witnessing §20.3 step 4's bar that its own next clause contradicts

§21.7, `[R-ERR-01]`, one sentence, two clauses:

> §20.3 step 4's bar on a declaration change is witnessed only where the
> affected tiles remain stored *and* the change reaches a byte §14 structurally
> constrains — a padding position, a pad bit, or a boolean byte — where §21.4's
> content rows fire;

> a change that reaches the decoded size instead is witnessed by T3 or T14,
> which test a length rather than the decoded image's content

The first clause makes "the change reaches a byte §14 structurally constrains"
a necessary condition for the bar being witnessed, and the em-dash gloss pins
that phrase to three content bytes. The second clause then supplies a witness
for a change that reaches none of those three — and says so in as many words
("which test a length rather than the decoded image's content"). The third
clause does it again for the codec ("witnessed by the rows for the codec now
declared ... (T15, T17, T23, T25), or by T14 where the new declaration is
codec 1").

Two readings. (a) "only where" governs the whole conjunction as written, in
which case the second and third clauses are counter-examples to it. (b) "only
where" governs the first conjunct alone ("the affected tiles remain stored"),
and the em-dash gloss is a slip that narrows "the change reaches [something §14
fixes]" to one of the things §14 fixes. I picked (b) as the intent and (a) as
what the text says; either way one clause is wrong.

An implementer taking the sentence literally concludes that a declaration change
altering only the decoded size is unwitnessed, then finds T3 and T14 in the
register and cannot reconcile them. Not byte-level: §21.7 registers nothing and
obliges nothing; T3 and T14 are in the register regardless, so no
implementation's accept/reject set moves.

### register-04 — §21.7's walk of §20.3 step 4 covers three of the bar's four heads

§20.3 step 4 names four things a declaration change must not alter for a tile
stored in the superseded generation:

> the set of padding positions (§11.3) and the content `[R-SER-05]` fixes
> there, the decoded size, the byte offset of any sample within the decoded
> tile image, or the codec and filter that produced the stored bytes

§21.7's account walks padding/pad-bit/boolean content (T2, T4, T5), the decoded
size (T3, T14) and the codec (T15, T17, T23, T25, T14) — and then closes on the
one unwitnessed case it names:

> and a commit that supersedes every tile it would have damaged leaves the live
> state clean, so the bar is unwitnessed there for the same reason `[R-LIF-01]`
> is

The third head, "the byte offset of any sample within the decoded tile image",
is not walked, and it has a live unwitnessed case of its own. Worked example: an
interleaved layer with channels `a` (uint32) and `b` (uint16), extents exact
multiples of the tile extents so there is no padding position and no bool
channel, codec and filter unchanged. Re-declare `a` as uint16 and `b` as uint32.
Q = 6 either way, so the decoded size P·Q is unchanged and T3/T14 are silent;
`b`'s in-sample offset F_b moves from 4 to 2, so every stored sample now decodes
to a different value. `[R-CNT-23]` forces each channel's fill length to follow
its element size, so the layer record does change — but nothing in the live
state witnesses the damage. The bar is violated and no row fires.

So the sentence's closing "the bar is unwitnessed there" names one unwitnessed
case where there are two, and §21.7 is by §21.1's own framing "the account, by
class, of what fails" detectability. In mitigation, §21.7's first paragraph
covers wrong sample content as a class ("A writer that emits well-formed
structures carrying wrong sample values ... produces a file that every checksum
in §8 certifies"), so the case is arguably covered by class if not by name;
that is why I file it as an observation and not a contradiction.

Not byte-level: it changes nothing about what a file may contain or what a
reader must do with one.

### register-05 — §21.7 lists the compactor's ignore-lane carry-forward as unwitnessed and omits the appender's, which is identical

§21.7:

> §20.5's two obligations on a compacted file's trailer (`[R-WRT-06]`) — the
> unknown ignore-lane bits it MUST carry forward, and the floor its
> version_minor SHOULD take — are unwitnessed for that same reason, the output
> carrying no record of its input's flags or its input's minor

§6.3, `[R-CNT-08]`, states the exactly parallel obligation for an appender:

> An updater MUST copy forward unknown ignore-lane bits of the file it modifies
> and MUST NOT clear them

and §20.3 step 6 restates it ("unknown ignore-lane flag bits copied forward
(`[R-CNT-08]`)"). It is equally unwitnessed: the live state carries one trailer,
§9.7 walks the live state only, and the prior generation's trailer is slack that
"a reader MUST NOT interpret" (§5.2). Yet §21.7's enumeration names only the
compactor half.

This is the sharpest instance of a broader thinness in that paragraph — the same
argument applies to `[R-LIF-02]` step 3 (a new trailer re-pointed at a prior
generation's directory region leaves the live state consistent; §9.7 cannot see
that the directory was not appended by this commit) and to `[R-LIF-04]`'s
truncation obligation, whose account is given in §9.5's Note instead of here. I
name `[R-CNT-08]` because it is the one whose omission is visibly asymmetric
with something the paragraph does list.

Not byte-level: an unwitnessed obligation is unwitnessed under either reading;
nothing about which files are conforming or which verdicts are owed changes.

### register-06 — §20.5's row citation for reserved-range values names one of the seven enum spaces

§20.5, `[R-WRT-06]`:

> the two of §10.1's four vehicles §21.6 makes conforming, the other two
> reaching such a file only as values this text still registers as
> reserved-range violations (F36, L25, R1)

§10.1's four vehicles are new record types, new values in reserved ranges, new
ignore-lane flag bits, and new standardized metadata keys. §21.6 makes the last
two conforming; "the other two" are record types and reserved-range values.
F36 and L25 register the record-type half at both placements. R1 registers one
of the seven remaining spaces §10.2's table lists — metadata encoding. The
other six are registered too, and are not cited: L33 (linearization 2–0x7FFF),
L34 (sample type 14–0x7FFF), L43 (codec 5–0x7FFF), L45 (filter 3–0x7FFF), L36
(channel layout 3–255), L31 (index encoding 2–0x7F).

The claim the parenthesis supports is true — every reserved-range value in every
space is a violation under this text, so a conforming input carries none — so
the argument's conclusion survives. What a reader loses is the register's own
map: taking the parenthesis as the list, one would conclude that a reserved-range
*codec* value is not registered, which is false.

I record the alternative reading: F36, L25 and R1 are precisely the three rows a
compactor could carry forward *without detecting*, since §19.3's layer
validation (which `[R-WRT-09]` obliges) catches every enum-value row, while a
reserved-range record type is verifier-detected and a reserved metadata encoding
is ignore-record. If that is the intent, the parenthesis is right for its
purpose and wrong for its wording.

Not byte-level.

### register-07 — Appendix G's summary paragraph contradicts item 8 on whether the version_minor floor binds a compactor

Appendix G, item 8:

> The `flags` half is a creator's rule, as item 2's identifier is: a compactor
> adopting the profile carries its input's unknown ignore-lane bits forward
> instead (`[R-CNT-08]`). The version_minor floor binds a compactor too, save
> where its output carries a feature it does not implement, when §20.5's floor
> governs instead (`[R-WRT-06]`).

Appendix G, closing paragraph:

> `version_minor` at its floor, which `[R-CNT-26]` states as a SHOULD — item
> 8's creator's rule, not a compactor's (§20.5)

Item 8 divides its two halves precisely: the `flags` = 0 half is the creator's
alone, and the version_minor floor "binds a compactor too" except in one named
case. The closing paragraph attaches "creator's rule, not a compactor's" to the
version_minor half — the half item 8 says does bind a compactor. It reads as if
the two halves had been swapped.

Readings: (a) the gloss means what it says and contradicts item 8; (b) the gloss
is a compressed pointer meaning "item 8 states this for a creator; §20.5 states
a compactor's", which would still be wrong, since item 8 makes §20.5's floor the
*exception* and `[R-CNT-26]`'s floor the rule for a compactor. I picked item 8
as governing: it is the numbered item, the closing paragraph says of itself
"Read the numbered items as the list; this paragraph names what they are for".

Not byte-level. Appendix G is identified non-normative and states of itself that
it "adds no requirement to any actor"; the cost is to an adopter deciding
whether a compactor claiming the profile must put version_minor at
`[R-CNT-26]`'s floor.

### register-08 — §21.5 registers the three key-name constraints under two different governing rules, neither of them the rule that states them

§4.6, `[R-ENC-12]`, states the constraints and names user-metadata keys among
the strings it binds:

> **Names** — the strings that identify layers, dimensions, channels, and
> user-metadata keys — satisfy three further constraints. ... A name is:
> non-empty; at most 255 bytes of UTF-8 ...; free of code points in the range
> U+0000 through U+001F.

§18.2, `[R-MTA-04]`, restates them for keys ("every key satisfying §4.6's name
rules — non-empty, at most 255 bytes, free of U+0000 through U+001F").

The register splits the three constraints across two rows with two different
Governing rule cells:

> | R6 | A key of a decoded user-metadata document is empty or contains a code
> point in U+0000 through U+001F | ... | `[R-CNT-25]` (R-ENC-12) |

> | R10 | A user-metadata document key is longer than 255 bytes | ... |
> `[R-MTA-04]` (R-ENC-12) |

§21.1 fixes what the cell means: "A Governing rule cell names that requirement
first" — "that requirement" being "the requirement that defines it" — "any
identifiers following it in parentheses are the further rules the condition
reads". By that rule, R6's defining requirement is not `[R-CNT-25]`:
`[R-CNT-25]` says only that content "violating the document's own rules" is
ignore-record; it states no key constraint. R10 gets it right in kind
(`[R-MTA-04]` does state the key rules) but then differs from R6 for two clauses
of a single three-clause list. Neither names `[R-ENC-12]`, the rule that
actually states all three, as governing.

The same inversion shows at R5 (`[R-CNT-25]` governing, `[R-MTA-04]`
parenthetical) against R7, R8, R9 (`[R-MTA-04]` governing, `[R-CNT-25]`
parenthetical) — six rows drawn from `[R-MTA-04]`'s four restrictions, split
four-to-two on which identifier goes first. R5 is at least defensible, because
`[R-CNT-25]` does name ill-formed UTF-8 explicitly; R6 is not.

Cost to an implementer: §24's `[R-VEC-02]` requires each vector to record "the
§21 register row it exercises together with that row's governing requirement
identifier", and says the pair is what survives a renumbering. A corpus indexed
by governing identifier shows `[R-ENC-12]`'s three key constraints under
`[R-CNT-25]` and `[R-MTA-04]` and never under `[R-ENC-12]`.

Not byte-level.

### register-09 — §21.1's own governing rules carry no requirement identifier

§21.1 is the section my charter calls "the register's own governing rules", and
it is the only subsection of §21 with no `[R-…]` identifier: §21.7 carries
`[R-ERR-01]`, §21.8 `[R-ERR-02]`, §21.9 `[R-ERR-03]`/`[R-ERR-04]`/`[R-ERR-05]`.
§21.1 cites `[R-ERR-02]` in its first line, but `[R-ERR-02]` as stated in §21.8
is a corpus-coverage requirement ("Every row ... has at least one conformance
vector") and does not state the register's extent, its completeness, or its
tie-break.

The unidentified statements are load-bearing and are cited from elsewhere by
prose position:

> where a row and the rule it cites diverge, **the rule governs**

> §21.6's entries restate their governing rules on the same terms a row does,
> and where such an entry and the rule it cites diverge, the rule governs there
> too.

§19's preamble cites it positionally ("at the tier that row's *Detected* cell
names (§21.1)"), and so does `[R-VEC-04]` ("no reader is obliged to refuse
anything (§21.1)"). §2.2 says "Normative requirements carry identifiers of the
form `[R-<PREFIX>-<NN>]`", and the front matter says "test vectors cite those
identifiers rather than prose positions".

Counter-argument I weighed: the completeness clause binds the *document*, not an
actor, so under §2.1's Note ("every requirement names the actor it binds") it is
arguably not a requirement and needs no identifier. That argument does not
reach the tie-break, which binds every reader, verifier and corpus builder that
meets a divergence, nor the Instances arithmetic, which `[R-ERR-02]` and
`[R-VEC-03]` both depend on for the corpus's shape.

Not byte-level.

## 7. Things I checked and did not report

Recorded so that the next round does not re-derive them.

- **All four CRC constants verify.** CRC-32C("123456789") = 0xE3069283 and
  CRC-32C(∅) = 0x00000000 (§4.5); §7.4's 80-byte four-sentinel array →
  0x80A34955, stored `55 49 A3 80`, whose CRC is 0xC4EE982E = crc_of_crc_array;
  §15.4's full all-sentinel segment (2¹⁶ × 20 bytes) → 0xEECB3BB2; Appendix A's
  trailer bytes [0, 60) → 0xE00938D2, stored `D2 38 09 E0`. I implemented
  CRC-32C from §4.5's parameters alone (poly 0x1EDC6F41 reflected = 0x82F63B78,
  init and final XOR 0xFFFFFFFF) and every one matched first try — which is
  itself evidence that §4.5 is implementable from the text.
- **Every other worked example verifies.** §11.2's grids; §11.4's ordinals
  (1·8+2 = 10, 44·256+188 = 11,452, 2·32+10 = 74); §14.2's offsets (18 and 30
  byte decoded sizes, bytes [15,18) and [25,30)); §14.3's `55 01` / `55 FD`;
  §14.5's 32-byte edge tile; §15.4's 20,000,064-byte region, segment 15 at
  [19,660,800, 20,000,000), 1.25 MiB full segment, entries 96–127; §17.3's
  shuffle `00 00 00 00 00 00 80 00 40 3F 40 40`; §20.3's 644-byte index; §5.1's
  128-byte minimum. Also §21.9's Note: 2³² entries → 2¹⁶ segments × 4 = 256 KiB
  and 2³⁶ → 4 MiB ✔; 65,536 layers ≈ 12.5 MiB at 200-byte records ✔; 2³² × 20 =
  ~86 GB, "tens of gigabytes" as `[R-VEC-03]` says ✔.
- **§21.9's hard limits against their defining sections**, all nine: names ≤ 255
  (§4.6), key ≤ 255 (§18.2), rank ≤ 255 / C ≤ 65,535 (§7.4's u8/u16), lz4
  0x7E000000 (`[R-COD-07]`), 2⁶³−1 domain (`[R-ENC-03]`), A power of two
  512…2⁶² and A_slab power of two 1…2⁶² (§16.1, §16.2, §7.4), S in 1…2⁶³−1
  (§7.4, §16.2), dir_offset ≥ 16 / dir_length ≥ 4 (§6.2), 128-byte file (§5.1).
  Each matches its source exactly. §16.2 states no upper bound on A_slab, but
  §21.9 cites `[R-CNT-23]` alongside it, and §7.4's table supplies the 2⁶².
  Nothing is stated differently here from where it is defined.
- **A limit stated elsewhere and missing from §21.9**: the user-metadata extent
  minimum, extent_length ≥ 5 (§7.1), which Appendix B lists and §21.9 does not.
  Not reported: `[R-ERR-05]` expressly disclaims inventory status — "The hard
  limits it restates are a finding aid rather than an inventory".
- **The minimum-guarantee table against Appendix B's summary row**: all eight
  values agree (rank 32, C 4096, entry_count 2³², 65,536 layers, 16 MiB
  directory, 256 MiB tile, 16 MiB document, 8 MiB zstd window).
- **`[R-ERR-04]` against `[R-CNF-03]`, `[R-CNF-10]` and §18.2's Note.** The
  refusal-scope machinery is consistent: guarantees are floors not caps, a file
  exceeding one stays conforming, refusal is at the whole file or the narrowest
  scope whose declarations exceed capability, and §18.2 correctly says a
  document has no declared size and so no narrower scope. Notably, `[R-ERR-04]`
  states the whole-file option explicitly where §21.6's MU = 1 case does not —
  which is what makes register-02's gap visible by contrast.
- **§21.1's specialization list.** F1 ⊂ F6 and F1 ⊂ F8 (byte-reversed is a
  species of not-byte-identical), F35 ⊂ F36, L24 ⊂ L25 — all three hold, and
  they are the three where the narrower row's detector or detection point
  differs from the wider row's. T13 ⊂ T25, T15 ⊂ T24/T25, T16 ⊂ T24, T23 ⊂ T25
  and T26 ⊂ T2/T4 are also strict specializations and are not listed, but each
  states the relation in its own Condition cell and each shares its detector and
  detection point with the row it routes to, so nothing turns on the omission.
- **`[R-ENC-02]`'s big-endian prohibition** has no register row and no §21.7
  entry beyond F1's byte-reversed signature. I judged it not a defect for the
  same reason §21.7 gives for `[R-ENC-06]`: a big-endian field "is not a state a
  file can be in", since the same bytes are a little-endian value of a different
  magnitude and no fact of the matter distinguishes them.
- **`[R-SLB-04]`'s stale slab declaration** has no row; §16.2's Note gives the
  account ("Because this rule's detection *is* `[R-SLB-03]`'s, a stale
  declaration carries no register row of its own"). Correct, though the account
  lives outside §21.7, as do §5.2's (coverage's untestable half), §7.4's
  (nesting) and §9.5's (residue past a completed commit).
- **`[R-CNT-08]`'s incompat-lane bits.** F19 registers any set incompat bit as a
  violation. I checked whether a later minor could define one, which would make
  F19 wrong: §10.1's vehicle 3 is "New **ignore-lane** flag bits" only, and
  "Nothing else extends this format", so no minor can. F19 is right.
- **§21.6's table entries against their rules**, all fourteen. Each restates its
  rule faithfully. The nearest thing to a slip is "The file contains zero
  layers | A conforming file with an empty directory", which reads as though a
  layer-less file must have an empty directory — but `[R-CNT-14]` says the same
  thing in the same words ("zero is valid: an empty directory is a conforming
  generation") and §21.6 creates no violations, so no reader or writer can act
  differently on it.
- **The instance cells for F27/L48 and R5–R10** are unqualified by encoding,
  although `[R-MTA-10]` withdraws every document rule at an unassigned encoding.
  §21.5's preamble carries the carve-out for its own rows; §21.2 and §21.3 do
  not carry it for F27 and L48. Not reported: at an unassigned encoding there is
  no decoding by which a verifier could evaluate sortedness, so the row is
  self-limiting and no verdict can differ.

## 8. Where an implementation would have had to guess

The honest list, in order of how long it cost me:

1. Whether to refuse the file or the layer on an experimental MU = 1 *sub-record*
   (register-02). This is the one place where I had to pick, and where I think a
   second implementer would plausibly pick the other way.
2. Whether an ignored record's extent is a coverage claimant. Decidable, but
   only from §5.2's "whatever the record's type" and §9.7's "each record's
   extent" — §2.4's "skipped as though absent" points the other way and is where
   an implementer looks first.
3. Which of `[R-CNT-25]`, `[R-MTA-04]` and `[R-ENC-12]` a corpus entry should
   name for a malformed user-metadata key (register-08).
4. Whether §21.7's account of §20.3 step 4 is exhaustive (register-03,
   register-04). I concluded it is not, but the sentence is recoverable and no
   behaviour turns on it.

Nothing on that list moves a byte or a verdict, which is why I am reporting zero
byte-level findings. The document's structural core — trailer, directory, record
framing, layer record, index, codecs, coverage — implemented cleanly from the
text alone, every worked example and every checksum reproduced on the first
attempt, and the register's completeness held in both directions across every
sweep I made.
