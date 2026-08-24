# Round 23 — Register hunter — working transcript

**Charter:** audit §21, the error-handling register, against the rules it restates and
against itself.

**Access:** I read exactly one file, `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in four `Read` calls covering lines 1–4426. I ran `grep`/`sed`/`awk` against that file only,
and two `python3 -c` invocations that read no files (one fed from a `grep` pipe over that same
file to count table cells; one pure arithmetic/CRC computation with literal inputs). I opened
no ADR, no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no `spec/registry.json`, no git
history, and I did not list any directory. I wrote this transcript and read nothing back from
its directory.

**Unrequested context.** My runtime placed a project instruction file (`CLAUDE.md`, pointing at
`AGENTS.md`) and an index of the maintainer's memory notes in my context before I began. I did
not open any of the files they name, and I have disregarded their contents in reaching every
conclusion below. Disclosing this as instructed.

---

## 0. Method

The register is a restatement layer. So the walk was:

1. Recount everything §21 states as a number, mechanically, from the cells as written.
2. Verify every arithmetic and CRC constant the document asserts, since a register that
   restates rules resting on bad constants is auditing nothing.
3. Row → rule: for each of the 121 rows, find the cited requirement, and compare wording,
   outcome class, scope, detector and detection point.
4. Rule → row: sweep every requirement identifier in the document, decide whether it names a
   *detectable file-conformance violation*, and if so find its row (or find §21.6/§21.7's
   account of why there is none).
5. Every citation of a row label from outside the tables.
6. Instance arithmetic against §21.1's own stated rules, cell by cell.
7. Limits, both directions.
8. Degenerate-but-legal files, to see what the tables say about them.

---

## 1. The counting

§21.1 fixes the arithmetic: *"Instances within a cell are separated by semicolons, and a cell
reading — is one instance; the count is therefore mechanical once the cell is written."*

I extracted all 121 table rows with `grep -n '^| [FLTR][0-9]'` and split the Instances cell on
`;`. Per-subsection:

| Subsection | Rows | Stated | Instances |
|---|---|---|---|
| §21.2 file | F1–F36 = 36 | "36 conditions" ✓ | 58 |
| §21.3 layer | L1–L49 = 49 | "49 conditions" ✓ | 116 |
| §21.4 tile | T1–T26 = 26 | "26 conditions" ✓ | 55 |
| §21.5 ignored | R1–R10 = 10 | "10 conditions" ✓ | 48 |
| **total** | **121** | §21.8 "121 conditions" ✓ | **277** |

§21.8 states *"121 conditions over 277 instances"*. Both reproduce exactly. The largest cells,
which I re-counted by hand as well: L2 = 9, L1 = 8, R4 = 16, R5 = 8, T3 = T14 = T22 = 6,
F33 = 5.

Detector/detection-point vocabulary: every Detector cell is `reader` or `verifier`; every
Detected cell is one of `open`, `layer access`, `tile use`, `extent use`, `certification`, plus
R1's split cell `open (top-level); layer access (sub-record)`. All 20 verifier rows (F7, F25,
F26, F27, F28, F33, F36; L18, L25, L40, L41, L42, L46, L47, L48, L49; T2, T4, T5, T26) carry
`certification`, and no reader row does. That matches §21.1: *"Detection points name §19.2's
reader tiers … or *certification* for the rows a verifier detects, which §19.2 places outside
the reader tiers entirely."*

**Outcome vocabulary.** §2.4 defines four reader outcomes (reject-file, reject-layer,
reject-tile, ignore-record) plus preserve-verbatim as an updater obligation. §21.2–§21.5 are
one subsection per reader outcome, so all four are reachable; preserve-verbatim is reachable
through §20.4's MU = 1 and MU = 0 / PE = 1 rows, exactly as §2.4 says. No row carries an
outcome outside the vocabulary, and no defined value is unreachable.

## 2. Constants and arithmetic the register rests on

Computed locally (CRC-32C, Castagnoli reflected, init/final 0xFFFFFFFF):

- `CRC32C("123456789")` = **0xE3069283** ✓ (§4.5 check vector)
- `CRC32C("")` = **0x00000000** ✓
- §7.4's worked layer record: 4 sentinel entries = 80 bytes → **0x80A34955**, stored
  `55 49 A3 80` ✓; `crc_of_crc_array` = CRC32C(`55 49 A3 80`) = **0xC4EE982E** ✓
- §15.4's full all-sentinel segment (65,536 × 20 bytes) = **0xEECB3BB2** ✓ (Appendix B ✓)
- Appendix A's trailer: I reassembled trailer bytes [0,60) from the annotation table and got
  CRC32C = **0xE00938D2**, stored `D2 38 09 E0` ✓

Arithmetic spot-checks that the register's derived-quantity rows depend on:

- §7.4 payload = 81 bytes: 4 (name) + 34 (nine scalars) + 18 (dim entry) + 12 (channel entry)
  + 13 (trailing) = 81 ✓; extent length 4·20 + ⌈4/2¹⁶⌉·4 = 84 ✓
- §15.4 example: 1,000,000 entries → 16 segments (15 full + 16,960) ✓; region 20,000,064 ✓;
  entry 999,999 at segment-relative 339,180 ✓; CRC array [20,000,000, 20,000,064) ✓; segment 15
  at [19,660,800, 20,000,000) ✓; full segment 65,536·20 = 1,310,720 = 1.25 MiB ✓
- §11.4: (300,700) → tile (1,2), s = 10, in-tile ordinal 11,452 ✓; planar c = 2 → 74 ✓
- §14.2/§14.3/§14.5/§17.3 worked byte layouts all reproduce (18/30/12-byte images; `55 01`
  vs `55 FD`; 32-byte edge tile with 15 × `CD AB`; the shuffle
  `00 00 00 00 00 00 80 00 40 3F 40 40`) ✓
- §21.9's Note: 2³² tiles → 2¹⁶ segments × 4 B = 256 KiB ✓; 2³⁶ → 4 MiB ✓; 65,536 layers at
  ~200 B/record ≈ 12.5 MiB ✓; 256 MiB ≈ 16× the 16 MiB top of §11.3's ordinary range ✓
- §20.3's example: 32·20 + 4 = 644 ✓

Nothing here diverges. That matters for the register because L2, L21, L22, L44, T3, T14, T21,
T22 and §21.9's rows are all stated over exactly these derived quantities.

## 3. Row → rule

I walked all 121. Rather than reprint agreement, here is the ledger of what I checked and where
the risk was.

**§21.2 against §6.2's ordered gate list.** §6.2 enumerates nine post-gate checks. Mapping:
cfl = transport size → F17; cfl multiple of 64 → F13; dir_offset ≥ 16 → F9; dir_length ≥ 4 →
F16; dir_offset + dir_length ≤ F − 64 → F10; 1 ≤ generation → F11 (and > 2⁶³−1 → F2);
file_id ≠ 0 → F12; reserved zero → F15; plus magic → F8 and CRC → F14 ahead of the gate. Nine
for nine, none spare.

§21.2's preamble claims *"Four rows are outside that reasoning and do reach it"* — F8, F1, F14,
F6. That is four rows, and §6.2's order plus `[R-CNT-04]`'s "before other processing" put
exactly those checks ahead of the version gate. `[R-CNT-24]` fixes the trailer magic, the
version fields, the trailer CRC and the front block across every major — the four rows'
subjects. F18 is separately excused as *"a case outside the premise"*, correctly: version_major
= 0 declares no major.

**§7.2 extent-slot rules.** `[R-CNT-13]` names four failures: either half zero (F30 / L15),
extent_offset < 16 (F31 / L16), extent past F − 64 (F32 / L17), overflowing sum (F3 / L2). The
file/layer split matches `[R-CNT-13]`'s own — *"the layer for a layer record and for
sub-records, the file for other top-level records"* — which is why F30–F32 all say
"non-layer top-level record" and L15–L17 say "layer record's or sub-record's". Correct.

**§15.3's eleven-row table → §21.** Row by row: valid sentinel → §21.6; sentinel with crc ≠ 0 →
T6; half-sentinel → T7; length 0 → T10; offset < 16 → T8; field > 2⁶³−1 → T11; overflow → T12;
extent past F − 64 → T9; stored bytes fail crc → T1; intra-layer overlap → L18; cross-scope
overlap → F33; alignment/slab invariant → L40, L41, L42. Complete in both directions.

**§17.2 `[R-COD-06]`'s six checkable zstd constraints** → T17 (magic), T18 (skippable / second
frame), T19 (dictionary ID), T20 (checksum flag), T21 (window), T22 (content size). The
seventh — undisclosed dictionary use — `[R-COD-06]` itself declares undetectable and §21.7
records it. Complete.

**§18.2's `[R-MTA-04]` four restrictions** → R7 (object/BOM), R8 (finite numbers), R9
(duplicate keys), R5 + R6 + R10 (UTF-8, key name rules, 255-byte cap). Complete — see §6 below
for two problems inside this mapping.

**Verifier rows against their rules.** `[R-CNT-12]` (F25, F26, L46, L47), `[R-CNT-22]` (F28,
L49), `[R-CNT-15]` (F36, L25), `[R-CNT-05]` (F7), `[R-CNT-13]` (F33, L18), `[R-SLB-01]` (L40),
`[R-SLB-03]` (L41, L42), `[R-SER-08]` (T2), `[R-SER-05]` (T4, T5), `[R-COD-10]` (T26),
`[R-MTA-05]` (F27, L48) — each rule does assign detection to the verifier in those words, and
each row's outcome is the record's or structure's governing scope. In particular L49's
reject-layer for a *layer record's* stored flag bits is right: §7.3's table calls the layer
record's scope "file (container for layer scope)", but `[R-CNT-13]` resolves it explicitly —
*"the layer for a layer record"* — and `[R-CNT-22]` says "the record's governing scope".

**Detection points against §19.1/§19.2/§19.3.** L3, L5, L6 at `open` is right: §19.1 step 4
parses and checks each layer record's *name* at the open, and §19.3 defines first access as
*"the first operation using any of the layer's declarations other than its name, whose parse
§19.1 step 4 places at the open"*. L4, L7, L8, L9 (dimension/channel names) at `layer access`
is right for the same reason. L37/L38 at `tile use` with reject-layer is exactly §19.2's
worked case. R1 at `open` for a top-level record is not restated in §19.1 step 4, but §19's
preamble forecloses that objection: *"Those enumerations are not the complete inventory of what
a reader detects at that tier: §21's register is."*

I found no row whose wording, outcome class, scope, detector or detection point diverges from
the requirement it cites. The divergences I did find are in the citations themselves (§6).

## 4. Rule → row (completeness inward)

I listed every `[R-<PREFIX>-<NN>]` in the document (159 distinct, plus `[R-ENC-100]`, which is
§2.2's illustration of numbering above 99, not a requirement). For each requirement not cited
as a Governing rule anywhere in the register, I asked whether it names a detectable
file-conformance violation.

Accounted for, with the document's own reason:

- `[R-CNT-02]` coverage partition — §5.2's Note: only disjointness is testable, and *"a
  register row for it would be a row no file could exhibit"*; disjointness is F33/L18.
- `[R-SLB-04]` stale slab declaration — §16.2's Note: *"a stale declaration carries no register
  row of its own"*, its detection being `[R-SLB-03]`'s (L41/L42).
- `[R-LIF-04]` residue past a completed commit — §9.5's Note: no row of its own, the reader
  meets it as a trailer gate failure.
- `[R-CNT-18]`'s nesting prohibition — §7.4's closing Note: no reader-detectable witness in
  format major 1; the one witness, a layer record as sub-record, is L26.
- `[R-ENC-06]` field widths, `[R-CNT-13]`'s MU = 0 offset prohibition, `[R-GEO-06]`/`[R-SER-01]`
  ordinal mappings, `[R-LIF-01]`/`[R-LIF-03]` history properties, §20.3 step 4's declaration
  bar, §20.5's carried flags and version_minor floor — all §21.7.
- `[R-COD-02]` — has a row (T13). Worth flagging that its operative sentence carries no BCP 14
  keyword; the document's own practice (`[R-CNT-13]`, `[R-CNT-02]`, `[R-SER-01]`, `[R-SER-02]`,
  and §21.7 calling `[R-CNT-13]`'s keyword-free clause a *prohibition*) makes that force
  ordinary, so T13 is correctly registered as a violation.
- SHOULD-level rules (`[R-CNT-03]`, `[R-CNT-09]`, `[R-CNT-26]`, `[R-ENC-14]`, `[R-LIF-07]`,
  `[R-TYP-10]`, `[R-MTA-07]`'s writer half) — §21.1: MUST-level only, and `[R-CNF-12]` puts
  SHOULD deviation outside the register.
- Reader/writer conduct rules with no file witness (`[R-ENC-05]`, `[R-ENC-10]`, `[R-ENC-13]`,
  `[R-CNT-10]`, `[R-GEO-04]`, `[R-TYP-04]`, `[R-TYP-06]`, `[R-TYP-08]`, `[R-TYP-09]`,
  `[R-MDL-02]`, `[R-MTA-02]`, `[R-MTA-08]`, `[R-SEC-*]`, `[R-RDR-*]`, `[R-WRT-*]`).

Structure-by-structure reconstruction. I enumerated every field of every structure the document
defines and asked what fixes each. Trailer: 11 fields → F1, F2, F3, F5, F8–F20, §21.6 (minor,
ignore lane). Record header: type → F24/F34/F35/F36/L13/L24/L25/L26; flags →
F25/F26/F28/L46/L47/L49; inline_length → F23/F29/L12/L14/L23; extent slot →
F2/F3/F30/F31/F32/L1/L2/L15/L16/L17/L22. Layer record inline payload: name (L3, L5, L6, F4,
L23), layout (L36), linearization (L33), codec (L43), filter (L45), A (L20, L39, L40), S (L1,
L20), A_slab (L28, L29, L42), rank (L32), C (L32), dimension entries (L1, L4, L7, L8, L9, L32),
channel entries (L4, L7, L8, L9, L30, L34, L35), index_encoding (L31), entry_count (L1, L21,
L22), crc_of_crc_array (L27, L37), sub-records (L10–L14, L19, L24–L26, L46, L47, L49). Index
region: L22, L37, L38, T1, T6–T12. Stored tile: T1–T5, T13–T26. User metadata: F21–F23, F27,
F34, L10–L12, L19, L48, R1–R10.

I found no field whose failure modes lack a row and no rule making something a violation that
the register omits. Two near-misses I chased and dismissed:

- **`[R-IDX-05]`** licenses writers to stamp `0xEECB3BB2` on any *full* all-sentinel segment and
  requires a partial segment's CRC to be computed. A writer stamping it on a partial segment
  produces a CRC that fails byte comparison → L38, which cites `R-IDX-05` in its parentheticals
  and spells the case out. No row needed.
- **§21.9 bounds a tile's *decoded* size but no row bounds a stored tile's *length*.** I built
  the case that a reader "MUST accept" a file with a 100 GB stored extent decoding to 1 KiB
  and found it collapses: the entry's length is corroborated against F (T9), so such a file
  really is 100 GB, and no row bounds file size either — deliberately, this being a format for
  large files. `[R-SEC-02]`'s allocate-from-declarations rule keeps the decoded side bounded.
  Not a gap.

## 5. Every citation of a row label

Grepped for `F|L|T|R` + digits outside the tables. Fifteen sites. Checked each against the row
it names:

- §5.2 `[R-CNT-21]`: *"L18's overlap or L40 through L42's placement"* — L18 is intra-layer
  overlap (verifier, reject-layer); L40/L41/L42 are the alignment and slab placement rows
  (verifier, reject-layer). Both resolve. ✓
- §9.6: *"(§21.2 rows F8 and F17)"* — F8 is the trailer magic, F17 the transport-size mismatch;
  both are `[R-CNT-06]` gates. §9.5's parallel Note names three grounds ("the magic, the CRC, or
  committed_file_length"), so F14 is unnamed here. I read both as exemplary — §6.2 has nine
  gates and neither passage lists them all — so not a finding.
- §17.2's deflate Note: *"(§21.4, T24)"* — T24 is "bytes remain in the stored extent after the
  stream … ends", governing rule `[R-COD-08]`, which is what the Note says rejects a trailing
  byte. ✓
- §18.2's five R3/R4 references — all resolve, see §6.
- §20.3 step 4: *"`[R-COD-07]`'s lz4 decoded-size cap among them (L44)"* — L44 is exactly that
  cap, quantified over addressed tiles, same as §17.2's Note. ✓
- §20.5: *"(F36, L25, R1)"* — see finding **register-03**.
- §21.1: *"F1 of F6 and of F8, F35 of F36, L24 of L25"* — all four specialization claims hold
  (a byte-reversed front block is a special case of a non-identical front block; a byte-reversed
  trailer magic of a wrong trailer magic; MU = 1 reserved type of any reserved type). I looked
  for unnamed specializations where the detector or point differs, which is what §21.1 says the
  list is for, and found none. T14 ⟹ T3 under codec 1 (the decoded payload *is* the stored
  bytes, so a length mismatch is both), but detector, point and outcome are identical
  (reader / tile use / reject-tile), so nothing turns on it, and §24's non-isolable-condition
  rule already tells a corpus author what to record.
- §21.1: *"(T24's *any codec*)"*, *"(T15, T25)"* — the blessed examples match the cells. ✓
- §21.1: *"F27 and L48"* — the `[R-MTA-05]` rows. The `[R-CNT-22]` rows (F28, L49) are named by
  rule rather than label; the em-dash attaches to the second clause, so this reads correctly. ✓
- §21.6 closing: *"(F18 …)"* and *"(F35, F36, L24, L25)"* — exhaustive and correct for
  version_major = 0 and reserved-range record types respectively. ✓
- §21.7: T2/T4/T5, T3/T14, T15/T17/T23/T25 — each names a row that tests what §21.7 says it
  tests. T14 tests the entry's declared length and T3 the decoded payload's own, as stated. ✓
- Appendix H: *"(F1, F6)"*, *"(`[R-CNT-05]`, F7)"*, *"(`[R-CNT-15]`, F36, L25)"*, *"(R1)"* —
  all resolve to rows saying what the checklist claims. ✓

## 6. Instance arithmetic against §21.1's own rules

§21.1 states four discriminators. I applied each across all 121 cells.

**Layout axis** — *"Where the quantity a condition derives varies by layout, the layout formulas
are materially different shapes and the cell enumerates them."* Three formulas exist
(interleaved P·Q, planar numeric P·Bᶜ, packed planar bool ⌈P/8⌉). Rows deriving a per-tile size
all enumerate three: T3 (×2 directions = 6), T14 (6), T21 (3), T22 (6), L44 (3). T4 enumerates
four carriers because `[R-SER-05]`'s numeric case splits by layout. L21 enumerates the two
addressed-tile formulas. Consistent everywhere.

**Magnitude direction** — *differs from / does not equal* → two; *exceeds / larger than* → one;
checksum or byte-pattern comparison → none. Checked: L21, L22, L30, T3, T14, T22, F17 all take
two; L1, L2, T21, T9, T11, F5, F16, F22, F32, L17, L44 all take one; F14, F20, L37, L38, T1,
L35, T2, F1 all take none. No exception.

**Single predicate over several fields → one instance.** F25 (MU = 1 with PE = 0) = 1; L20
(A ≠ 0 and S ≠ 0) = 1; L27, L28 = 1; T12 (offset + length) = 1. Meanwhile F28/L49 read "MU *or*
PE", a disjunction, and correctly enumerate the bits. Consistent.

**Family without shape change → one instance.** F19 (16 incompat bits) = 1; F26/L47 (14 reserved
bits) = 1 per container; T24 ("any codec") = 1, explicitly blessed by §21.1.

One cell fails these rules: **R8**. See **register-01**.

Cross-check on the §21.5 container axis, which is the cleanest test bed because every row has
exactly two containers (top-level document and layer sub-record document):

| Row | Alternatives in the governing rule | Cell |
|---|---|---|
| R1 | 2 (encoding 0; reserved 3–0x7F) | 2 × 2 = 4 ✓ |
| R2 | 1 | 2 ✓ |
| R3 | 1 | 2 ✓ |
| R4 | 8 | 8 × 2 = 16 ✓ |
| R5 | 4 | 4 × 2 = 8 ✓ |
| R6 | 2 (empty; C0 control) | 2 × 2 = 4 ✓ |
| R7 | 3 (ill-formed JSON; non-object; BOM) | 3 × 2 = 6 ✓ |
| R8 | **2** (overflowing magnitude; bare token) | **2** — containers only |
| R9 | 1 | 2 ✓ |
| R10 | 1 | 2 ✓ |

R8 is the only row in the subsection that does not multiply its stated alternatives by its
containers.

## 7. Limits, both directions

**§21.9's minimum-guarantee table** (rank 32 · C 4096 · entry_count 2³² · 65,536 layers ·
16 MiB dir_length · 256 MiB decoded tile · 16 MiB metadata document · 8 MiB zstd Window_Size)
matches Appendix B's collected line exactly, matches §17.2's *"§21.9's 8 MiB `Window_Size`
guarantee"*, matches §18.2's *"no smaller than §21.9's user-metadata guarantee"* and its
16 MiB Note, matches §1's *"§21.9's tile-count guarantee"*, Appendix D's *"§21.9's entry_count
guarantee"*, §24's tile-count constructibility carve-out, and Appendix H. No divergence.

The three per-instance rows are individuated coherently. *Decoded size of one tile* ranges over
**addressed** tiles, and I checked that against `[R-COD-07]`'s own quantifier and §17.2's Note
(*"a layer that addresses none … satisfies it whatever its tile shape declares"*) and against
§20.3 step 4's *"which an empty layer escapes only because that cap is quantified over addressed
tiles"*. Three passages, one quantifier, no drift. The Window_Size row ranging over *"compressed
frames a file actually contains"* correctly covers both codec-3 tile payloads and encoding-2
metadata frames, which is what §17.2 and §18.2 each need of it.

**§21.9's hard limits.** Ten stated. Against their defining sections: names ≤ 255 (§4.6 u8
prefix) ✓; user-metadata key ≤ 255 (§18.2's fourth `[R-MTA-04]` bullet) ✓; rank ≤ 255 and
C ≤ 65,535 (§7.4 u8/u16) ✓; codec 4 decoded tile size ≤ 0x7E000000 (`[R-COD-07]`) ✓; every
offset/length/extent/count ≤ 2⁶³−1 (`[R-ENC-03]`) ✓; A a power of two 512…2⁶² (§7.4, §16.1) ✓;
A_slab a power of two 1…2⁶² (§7.4, §16.2) ✓; S in 1…2⁶³−1 (§7.4, §16.2) ✓; dir_offset ≥ 16 and
dir_length ≥ 4 (§6.2) ✓; no file shorter than 128 bytes (§5.1) ✓. Not one is stated differently
from its defining section.

Limits stated elsewhere and absent here: the user-metadata `extent_length ≥ 5` floor (§7.1,
Appendix B). This is not a finding — `[R-ERR-03]` says outright *"The hard limits it restates
are a finding aid rather than an inventory."* I checked that no other §21.9 statement claims
exhaustiveness, and none does.

## 8. Degenerate files the document permits

Built these on paper and asked what the tables say:

- **Zero-extent dimension.** E₀ = 0 → G₀ = 0 → N = 0 → entry_count = 0 → extent slot (0,0),
  crc_of_crc_array = 0. §21.6 records it as a non-violation; L21/L22/L27 all agree; §15.4's
  example agrees; §21.9's tile row has no instance to bound. Coherent at four sites.
- **Codec 4 on an empty layer with a 3 GiB declared tile shape.** Conforming (L44 quantified
  over addressed tiles). §20.3 step 4 correctly notes the escape is not durable. Coherent.
- **A = 2⁶².** Legal. Every stored offset must be a multiple of 2⁶² and ≥ 16, so at most one
  stored tile can exist in any file. Degenerate, permitted, and no row says otherwise.
- **A_slab = 1.** A power of two (2⁰), permitted by L29's bound, and §16.2's Note names it as
  the contiguity-only declaration. ✓
- **Slab declared on a layer with zero stored tiles.** `[R-SLB-03]`: *"A run with no stored
  tiles imposes nothing."* L41/L42 correspondingly have no witness. ✓
- **L2's N·P instance in isolation.** I wanted to know whether every L2 instance is
  constructible without dragging in others (since `[R-ERR-02]` demands one vector per instance).
  d = 2, T = (2⁶¹, 2), E = (2⁶², 2): G = (2, 1), N = 2, P = 2⁶², so N·P = 2⁶³ overflows while
  P = 2⁶² and P·Q = 2⁶² and C·N = 2 all stay in domain, and entry_count = 2 means an
  extent_length of 44. A file of a few hundred bytes exhibits N·P alone. Good — the cell is
  not aspirational.
- **Smallest file carrying a layer.** Minimum layer-record inline payload is 72 bytes (name 2,
  nine scalars 34, one dimension entry 18, one uint8 channel entry 5, trailing 13), so
  dir_length = 24 + 72 + 4 = 100, which does not fit [16, F−64) at F = 128. F = 192 is the
  floor. Nothing in §21 claims otherwise; F5's 128-byte row is about the empty file.

## 9. Findings

### register-01 — AMBIGUITY. R8's Instances cell collapses two alternatives its governing rule states disjunctively

**Location:** §21.5, row R8; §18.2, `[R-MTA-04]`; §21.1's instance rules; §21.8's total.

R8 reads:

> | R8 | A user-metadata document contains a non-finite number, in any form | top-level document; layer sub-record document | reader | extent use | `[R-MTA-04]` (R-CNT-25) |

Its governing rule states two alternatives explicitly:

> **Finite numbers only.** A reader interprets every JSON number as an IEEE 754 binary64 value
> and MAY use a wider representation. A document is unreadable if it contains a number whose
> binary64 interpretation is not finite — which covers a magnitude that overflows on conversion,
> `1e400` being the ordinary case — or any of the bare tokens `NaN`, `Infinity`, or
> `-Infinity`, which RFC 8259 does not admit and some parsers accept regardless.

§21.1 licenses collapsing only where the shape is constant: *"a row whose check ranges over a
family without the condition changing shape states that range as a single instance (T24's *any
codec*), and one whose members give the condition materially different shapes enumerates them
(T15, T25)."* The two members here do change shape. `1e400` is a syntactically valid JSON
number requiring a decimal-to-binary64 conversion and an overflow test; `NaN` is a token
RFC 8259 does not admit at all, which a strict parser rejects before any numeric rule runs and
which only a lenient parser ever hands to this check. That is a wider gap than T15's zlib-versus-
gzip wrappers or R7's three, both of which the register enumerates.

**Permitted readings.** (a) Two instances, on the ground that "a non-finite number" is one
predicate and "in any form" states its range the way T24's "any codec" does. (b) Four instances
— two alternatives × two containers — on the ground that §18.2 states the alternatives
disjunctively with materially different detection procedures, and that every other §21.5 row
multiplies its stated alternatives by its containers (R1 4, R4 16, R5 8, R6 4, R7 6). I pick
(b): R8 is the only row in the subsection that does not, and §21.1's collapse licence is
conditioned on shape, which does not hold.

**What an implementer does wrong without it.** `[R-ERR-02]` and `[R-VEC-03]` require one vector
per instance. Under reading (a) the corpus discharges R8 with two files, and the natural pair is
one `NaN` document at each scope — because a bare token is the memorable case and because a
corpus author reads the two instances as *containers*, which is all they name. Nothing then
obliges a `1e400` vector, and `1e400` is the case §18.2 itself calls "the ordinary case". An
implementation whose JSON parser rejects `NaN` for free (every RFC 8259 parser does) but silently
converts `1e400` to `+Infinity` passes R8's coverage while violating `[R-MTA-04]`. Under reading
(b), §21.8's stated total becomes 279, not 277.

**Byte-level:** no. Both forms are already unreadable under `[R-MTA-04]`, whichever way the cell
is counted, so no implementation reading this text may emit or must accept a byte it could not
before. The cost is corpus coverage and a stated total.

### register-02 — AMBIGUITY. R6 names a governing rule that does not define its condition, while R10 — drawn from the same sentence — names the one that does

**Location:** §21.5, rows R5, R6, R10; §21.1's Governing-rule rule; §4.6 `[R-ENC-12]`;
§18.2 `[R-MTA-04]`.

R6 and R10 both come from the fourth bullet of `[R-MTA-04]`:

> **Well-formed UTF-8 throughout** (`[R-ENC-11]`) — including after escape resolution … — and
> every key satisfying §4.6's name rules — non-empty, at most 255 bytes, free of U+0000 through
> U+001F.

The two rows cite differently:

> | R6 | A key of a decoded user-metadata document is empty or contains a code point in U+0000
> through U+001F | … | `[R-CNT-25]` (R-ENC-12) |
>
> | R10 | A user-metadata document key is longer than 255 bytes | … | `[R-MTA-04]` (R-ENC-12) |

§21.1 fixes what the cell is for: *"the requirement that defines it. A Governing rule cell names
that requirement first; any identifiers following it in parentheses are the further rules the
condition reads."* R6's chain is `[R-CNT-25]` → `[R-ENC-12]`, and neither link defines the
condition. `[R-CNT-25]` says only *"content violating the document's own rules"* — it assigns an
outcome, it does not state a key rule. And `[R-ENC-12]` expressly **excludes** document keys
from its own scope:

> a reader MUST treat such a name as a validity error at the owning scope — except for a key
> inside a user-metadata document, where `[R-CNT-25]`'s quarantine governs and the outcome is
> ignore-record.

So the only requirement in the document that makes a user-metadata key non-empty and C0-free is
`[R-MTA-04]`'s fourth bullet — the requirement R6's cell does not cite at all. R5 has the milder
form of the same problem: it names `[R-CNT-25]` first but does at least carry `R-MTA-04` in its
parentheses.

**Permitted readings.** (a) `[R-CNT-25]` governs R6, because the quarantine is what makes the
condition registrable with an ignore-record outcome. (b) `[R-MTA-04]` governs R6, matching R7,
R8, R9 and R10, because §21.1 asks for the requirement that *defines* the condition and
`[R-CNT-25]` defines no key rule. I pick (b).

**What an implementer does wrong without it.** Two things. First, §21.1's tie-break — *"where a
row and the rule it cites diverge, the rule governs"* — sends a reader of R6 to `[R-CNT-25]`,
which is silent on empty keys, so the tie-break resolves to nothing; under (b) it resolves to
`[R-MTA-04]`. Second, `[R-VEC-02]` makes the pair (row label, governing requirement identifier)
the durable identity of a vector precisely because *"row labels are positional and renumber when
a row is struck, while §2.2 makes the identifier permanent"*. As written, two vectors testing
adjacent clauses of one sentence carry permanently different identifiers, and the R6 vector's
identifier does not name the clause it tests.

**Byte-level:** no. `[R-MTA-04]` binds either way; an empty key is ignore-record under both
readings. The cost is the register's tie-break and corpus manifest durability.

### register-03 — OBSERVATION. §20.5's "(F36, L25, R1)" under-enumerates the rows its claim ranges over

**Location:** §20.5, `[R-WRT-06]`; §10.1's four vehicles; §10.2's seven identifier spaces.

> Where the output carries a feature a later minor defines and this compactor does not — on a
> conforming input a carried ignore-lane bit (§6.3) or an unrecognized `tarn.` key in a record
> it never decoded (§18.3), the two of §10.1's four vehicles §21.6 makes conforming, the other
> two reaching such a file only as values this text still registers as reserved-range violations
> (F36, L25, R1) —

The two vehicles §21.6 makes conforming are ignore-lane bits and `tarn.` keys, so "the other
two" are §10.1's vehicle 1 (*"New record types"*) and vehicle 2 (*"New values in the ranges this
specification reserves (§10.2)"*). F36 and L25 discharge vehicle 1. Vehicle 2 ranges over the
seven spaces §10.2 tabulates, and the register carries a reserved-range row for each of them:
L31 (index encoding), L33 (linearization), L34 (sample type), L36 (channel layout), L43 (codec),
L45 (filter), R1 (metadata encoding). The parenthetical names one of the seven.

The omission is not idle. §12.2's Note pins sample-type identifiers 14–19 to specific future
assignments — *"14 and 15 for 8-bit floats … 16, 17, and 18 for int128, uint128, and float128,
and 19 for a fixed-size raw-bytes type"* — which makes a reserved *sample type* the most
concrete instance of "a feature a later minor defines" anywhere in the document, and its row is
L34, not R1. A new codec (L43) is the next most concrete. Neither appears.

I tried and failed to find a reading that makes the three-row list complete. The natural
candidate — that only rows a *compactor* could carry past its own verification survive — does
not separate them: `[R-WRT-09]` puts §19.3's layer validation in a compactor's path, which
catches L31/L33/L34/L36/L43/L45 *and* catches R1 (a reader row due at open for a top-level
record and at layer access for a sub-record), while F36 and L25 are verifier rows a compactor
need not run. Under that filter R1 should drop out too, not the six.

**Byte-level:** no. The sentence is a finding aid inside a compactor rule whose operative
obligations are the ignore-lane carry-forward and the version_minor floor; nothing an actor does
turns on the list. The cost is that a reader of §20.5 can take the parenthetical for the
exhaustive set — §21.6's closing paragraph uses the same construction *exhaustively* four lines
later, *"(F35, F36, L24, L25)"* — and conclude that a reserved-range sample type or codec is not
a registered violation, which L34 and L43 contradict.

## 10. Things I chased and rejected

Recorded so the next round does not re-spend the effort.

1. **§21.5's *"§21.6 lists the ignore-record conditions that are not violations"* against
   §21.6's table**, which has no row for a reader or verifier declining a document on its own
   size bound or on the frame's declared window — both of which §21.5's own preceding sentence
   calls ignore-record and *"not a fact about the file"*. Rejected: §21.6's frame is *"A reader
   that treats any of them as a failure is the nonconforming party"*, and a reader IS licensed
   to treat these as ignore-record, so they cannot be §21.6 rows. §21.5 answers them itself,
   two sentences earlier.

2. **§18.2's *"the bound above"* in the verifier sentence**, which follows both a decoded-size
   bound and a window bound and is singular. Rejected as resolved elsewhere: §2.3 lists the
   cannot-establish ground generically as *"when it declines to decode a user-metadata document
   (`[R-MTA-09]`)"*, and §21.5's preamble reads it as covering *"the size bound or … the frame's
   declared window"*. Two independent sites converge, so a verifier's verdict does not fork.

3. **`[R-CNF-03]`'s MU = 1 carve-out is not qualified to top-level records**, so read alone it
   withdraws the acceptance duty for a conforming file carrying an experimental MU = 1 *layer
   sub-record* — which §21.6 says is *"never a ground to refuse the file"*. Rejected:
   `[R-CNT-18]` closes it with an express prohibition — *"where the file is otherwise conforming
   a reader MUST NOT reject the file for it"* — so behavior is determined.

4. **T14 ⟹ T3 under codec 1** is an unnamed strict specialization. Rejected: §21.1's
   specialization list exists to fix *"whose detector and detection point are the ones that
   apply"*, and T14 and T3 share detector, point and outcome, so the list's purpose is not
   engaged. §24's non-isolable-condition rule handles the corpus side.

5. **§21.7's *"§20.5's two obligations on a compacted file's trailer"*** when `[R-WRT-06]` places
   four (fresh file_id, generation 1, ignore-lane carry-forward, version_minor floor). Rejected:
   the first two are generation-sequence properties, which §21.7's opening item already covers
   under `[R-LIF-03]` — *"properties of a file's history, which §9.7 does not reconstruct"*.

6. **§9.6's *"(§21.2 rows F8 and F17)"*** omitting F14 where §9.5's parallel Note names the CRC.
   Rejected: §6.2 has nine gates and neither passage lists them all; both are exemplary.

7. **§21.7's *"witnessed only where the affected tiles remain stored and the change reaches a
   byte §14 structurally constrains"*** followed immediately by two more witnesses (T3/T14 for a
   decoded-size change, T15/T17/T23/T25/T14 for a codec change). Rejected: the "only" reads as
   governing the appositive *"where §21.4's content rows fire"*, and the subsequent clauses
   disambiguate it in the same sentence.

8. **§21.9 bounding decoded tile size but nothing bounding a stored tile's length.** Rejected:
   see §4 above.

9. **L26 and L31 put section numbers (`§7.3 registry table`, `§15.1`) where §21.1 says the
   parentheses carry *identifiers*.** Cosmetic; both resolve.

10. **§21.1–§21.6 carry no requirement identifier**, though §21.1 states normative rules
    (completeness, row-versus-rule precedence, instance arithmetic). Rejected: §2.1's Note
    characterises a requirement as one that *"names the actor it binds"*, and §21.1's statements
    are interpretive rules about the document rather than obligations on an actor; `[R-CNF-01]`
    makes them normative without one, and `[R-VEC-02]`'s durable pairing uses each *row's*
    governing identifier, which every row has.

## 11. Where I had to guess

- Whether §21.1's *"materially different shapes"* covers the gap between an overflowing JSON
  number and a bare `NaN` token. I argued it from T15 and R7's precedents; the document does not
  define the phrase, and a maintainer could reasonably rule the other way. **register-01** is
  stated as an ambiguity for that reason.
- Whether the parentheticals in §20.5 and in §9.6 are meant exhaustively. §21.6's closing
  paragraph uses the construction exhaustively; §17.2's Note uses it exemplarily. I split them:
  §20.5 reported, §9.6 not, on the ground that §20.5's list is the *complete* answer to a "the
  other two" claim while §9.6's is a sample of nine gates.
- Whether R5's `[R-CNT-25]`-first citation is wrong in the same way R6's is. `[R-CNT-25]` does
  name ill-formed UTF-8 in its own enumeration, so R5 has a footing R6 lacks; I reported the
  clean case and named R5 only as context.

## 12. Verdict

The counting reproduces exactly, in both dimensions and in every subsection. Every constant and
every worked layout the register depends on verifies. Row-versus-rule agreement is clean across
all 121 rows: I found no row whose outcome class, scope, detector or detection point diverges
from the requirement it cites, and no requirement naming a detectable file-conformance violation
that lacks a row or an account in §21.6 or §21.7. The three findings are all in the citation and
instance-enumeration layer, and none of them moves a byte or a verdict.
