# Cleanroom round 29 — Register hunter — working transcript

## 0. Access, disclosure, paths

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,697 lines). I did not open `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`CLAUDE.md`, `README.md`, `conformance/`, `spec/registry.json`, or any git history, and
I ran no directory listings anywhere except `mkdir -p` on my own scratch and output
directories. No web access.

**Context I did not ask for.** My runtime placed material in context before I began: a
project instruction file pointer and an index of the maintainer's memory notes, naming
things like a working cadence, a naming constraint, and prior workflow failures. I did
not read any of the files it named and I have disregarded its contents; nothing below
rests on it. I note its appearance as required. It also contained a **path
discrepancy**: that material refers to the repository as `.../GitHub/tarn/`, while my
brief and my working directory put the spec under `.../GitHub/tarn-first-draft/`. The
spec file was where the brief said it was, so I read it there and did nothing to
resolve the discrepancy beyond noting it.

**Files I wrote** (all under
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-round/scratch/register/`):

- `count_inst.py` — mechanical instance counter over the four register tables
- `cols.py` — detector / detection-point / governing-rule tallies
- `crcs.py` — a CRC-32C implementation and the four constants the document states
- `trailer.py` — Appendix A's trailer CRC

plus this transcript at the single output path named in the brief. I did not read the
output directory.

---

## 1. How I worked

I read §21 first, then the whole document front to back, because my charter is
row-versus-rule agreement and I cannot check a restatement without the rule. I then ran
mechanical sweeps over a whitespace-normalised, `> `-stripped join of the file (the
brief's hard-wrap warning is real: `grep -n 'validity error'` and a normalised search
returned different hit counts, and every phrase search below was run against the
normalised text with a positive control).

Positive-control discipline: before resting anything on a zero I searched for a phrase I
knew was present in the same passage. Example: `unwitnessed` returned 5 hits (2613,
3886, 3897, 3911, 3917); `§21.7` returned 7. A search for `preserve-verbatim` outside
§2.4 returned 2 (both in §2.4/§20.4), which I confirmed by first searching
`preserve-verbatim` unrestricted (3 hits) — so the zero-outside-§2.4-and-§20.4 result is
a real zero, not a wrap artefact.

---

## 2. The counting — recount by hand and by machine

### 2.1 Conditions per subsection

Extracted every table row matching `^\| ([FLTR]\d+) \|` in lines 3540–3930:

| Subsection | Labels | Count found | Count stated | Notes |
|---|---|---|---|---|
| §21.2 file scope | F1–F36, F11 absent | **35** | 35 | F11 struck; the Note after the table says so, on §2.2's retirement model |
| §21.3 layer scope | L1–L49, contiguous | **49** | 49 | |
| §21.4 tile scope | T1–T26, contiguous | **26** | 26 | |
| §21.5 ignored records | R1–R10, contiguous | **10** | 10 | |
| **Total** | | **120** | 120 (§21.8) | |

No duplicate labels, no gaps other than F11.

### 2.2 Instances

§21.1 makes the count mechanical: "Instances within a cell are separated by semicolons,
and a cell reading — is one instance; the count is therefore mechanical once the cell is
written." Applying exactly that:

F = 56, L = 116, T = 55, R = 48. **Total 275.** §21.8 states 275. Reproduces exactly.

Per-row (the ones above 1): F1 2, F2 5, F3 2, F5 2, F6 2, F7 4, F17 2, F23 2, F28 2,
F29 3, F30 2, F33 5; L1 8, L2 9, L4 2, L7 2, L8 2, L9 2, L12 2, L14 3, L15 4, L16 2,
L17 2, L18 3, L21 4, L22 4, L23 4, L29 3, L30 2, L31 3, L32 3, L33 4, L34 4, L36 2,
L39 3, L41 3, L43 3, L44 3, L45 3, L46 2, L47 2, L49 4; T3 6, T4 4, T7 2, T11 2, T13 2,
T14 6, T15 2, T18 2, T21 3, T22 6, T25 3, T26 3; R1 4, R2 2, R3 2, R4 16, R5 8, R6 4,
R7 6, R8 2, R9 2, R10 2.

I then re-derived a sample of cells from §21.1's *substantive* rules rather than from
the semicolons, to check that the cells were written correctly in the first place:

- **Magnitude rule** ("a *differs from* or *does not equal*" → two directions; an
  "exceeds"/"larger than" → one). L21 (`does not equal` the addressed-tile count) —
  2 layouts × 2 directions = 4 ✓. L30 (`differs from` the element size) = 2 ✓.
  F17 (`does not equal` the transport size) = 2 ✓. T3, T14, T22 (`is not exactly`,
  `differs from`, `does not equal` the decoded size) — 3 layouts × 2 = 6 each ✓.
  T21 (`larger than`) and L44 (`exceeds`) — 3 layouts × 1 = 3 each ✓.
- **No-ordering rule** (checksum against computed, byte pattern against constant).
  F14, F20, L37, L38, T1, R2 = 1 (or 1 per container) ✓. F1's byte-reversal against a
  constant = no direction, 2 containers ✓. T17 (frame magic) = 1 ✓.
- **Nonzero value test** ("an *A ≠ 0*, an *S ≠ 0*"). T6 (`crc ≠ 0`) = 1 ✓. L27, L28 = 1 ✓.
- **Layout rule.** Every decoded-size row enumerates exactly three layout formulas
  (interleaved P·Q, planar numeric P·Bᶜ, packed planar bool ⌈P/8⌉): T3, T14, T21, T22,
  L44 ✓. §14.2/§14.3 define exactly those three ✓.
- **Family rule** (T24's *any codec* = 1) ✓ — §21.1 names T24 itself.
- **R4** — 8 frame constraints × 2 containers = 16 ✓. The 8 are: missing magic,
  skippable frame, second frame, nonzero dictionary ID, content-checksum flag, bytes
  after the frame, content-size larger, content-size smaller. §18.2 carries over exactly
  those from `[R-COD-06]` minus the two it replaces (decoded size, `Window_Size`) and
  minus the two it says fall outside the register (undisclosed dictionary use; the bar
  on sizing a buffer) ✓.

**Verdict on the counting: 120 / 275 both reproduce, and the cells reproduce from
§21.1's own arithmetic, not merely from the semicolons.**

### 2.3 `[R-CNT-06]` states nine

§2.3's `[R-CNF-13]` says "`[R-CNT-06]` states nine", and §21.7 repeats it. Counting from
§6.2's own text and stripping the two it delegates (the version gate → `[R-CNT-07]`, the
flag gates → `[R-CNT-08]`): trailer magic; trailer CRC; committed_file_length = file
size; committed_file_length multiple of 64; dir_offset ≥ 16; dir_length ≥ 4;
dir_offset + dir_length ≤ F − 64; file_id ≠ 0; reserved bytes zero = **9**. The register
rows whose Governing rule cell names `[R-CNT-06]` are F8, F9, F10, F12, F13, F14, F15,
F16, F17 = **9**. Exact match, and the split "the trailer magic and the trailer CRC
assert invariants `[R-CNT-24]` fixes and the other seven do not" is 2 + 7 ✓.

### 2.4 Detector / detection-point consistency

Machine tally of (Detector, Detected) pairs:

- reader / layer access 35, reader / open 31, reader / tile use 24,
  reader / extent use 9, reader / "open (top-level); layer access (sub-record)" 1 (R1),
  verifier / certification 20.

Every `verifier` row has Detected = `certification` and no `reader` row does — the
biconditional holds across all 120. The 20 verifier rows are F7, F25, F26, F27, F28,
F33, F36; L18, L25, L40, L41, L42, L46, L47, L48, L49; T2, T4, T5, T26. I checked each
against its rule: every one of the twelve governing rules says "a verifier MUST …" or
"its assigned detector is the verifier" in its own text. **No row's detector diverges
from its rule.** That matters, because it means the latent circularity I report in
finding register-02 is not actualised by any current row.

### 2.5 Every cited requirement identifier resolves

162 distinct `[R-XXX-NN]` identifiers are defined in the document. Every identifier
appearing in a Governing rule cell (governing or parenthetical) is one of them: zero
dangling citations.

---

## 3. Arithmetic and constants I re-derived

I implemented CRC-32C from §4.5's parameters (Castagnoli 0x1EDC6F41, reflected in/out,
init and final XOR 0xFFFFFFFF) and reproduced:

| Quantity | I computed | Document states |
|---|---|---|
| CRC-32C("123456789") | 0xE3069283 | 0xE3069283 (§4.5) ✓ |
| CRC-32C(zero bytes) | 0x00000000 | 0x00000000 (§4.5) ✓ |
| CRC over 4 sentinel entries (80 bytes `FF×16 00×4` ×4) | 0x80A34955 | 0x80A34955 (§7.4 example) ✓ |
| CRC over that 4-byte CRC array | 0xC4EE982E | 0xC4EE982E (§7.4 example) ✓ |
| CRC over 2¹⁶ sentinel entries | 0xEECB3BB2 | 0xEECB3BB2 (§15.4, `[R-IDX-05]`, App. B) ✓ |
| Appendix A trailer CRC over trailer bytes [0,60) | 0x402F157E | 0x402F157E ✓ |

Layer-record layout (§7.4 example): name 4 + nine scalars 34 (1+2+2+2+8+8+8+1+2) +
one dimension entry 18 (2+8+8) + one channel entry 12 (5+2+5) + trailing 13 (1+8+4) =
**81** ✓, and the byte offsets in the hex listing (0,4,5,7,9,11,19,27,35,36,38,40,48,
56,63,68,69,77) are consistent with those widths ✓. Index extent
4×20 + ⌈4/2¹⁶⌉×4 = **84** ✓.

Other figures I checked by hand and which reproduce: §15.4's 1,000,000-entry example
(16 segments, last covering 16,960; array at [20,000,000, 20,000,064); segment 15 at
[19,660,800, 20,000,000); entry byte 339,180; one full segment = 1.25 MiB);
§11.4's ordinals (s = 10, in-tile 11,452, planar disk ordinal 74, region bytes
[1,480, 1,500), channel-3 entries 96–127); §14.2's strides (Q = 3, size 18; Q = 5,
size 30; bytes [15,18) and [25,30)); §14.3's `55 01` / `55 FD`; §14.5's 32-byte edge
tile; §17.3's shuffle output; §20.3's 32·20+4 = 644; §16.2's four runs;
§5.1's 128-byte file (16 + 4 + 44 + 64).

**§21.9's Note.** Segment-CRC array at entry_count 2³² = 2³²/2¹⁶ × 4 = 2¹⁸ = **256 KiB**
✓; at 2³⁶ = 2²⁰ × 4 = **4 MiB** ✓. 65,536 layers × 200 bytes = 13,107,200 =
**12.5 MiB** ✓. §24's "tens of gigabytes" for a 2³² index region: 2³² × 20 ≈ 85.9 GB ✓.

---

## 4. Row-versus-rule sweep

I walked all 120 rows against their governing rules. I record the outcome compactly,
then the residue.

**§21.2 (35).** F1↔`[R-ENC-02]` (byte-swapped signature, reject-file, both §6
constants) ✓. F2/F3↔`[R-ENC-03]`/`[R-ENC-04]` — F2's instance list correctly omits
`file_id`, which is a u64 but not an "offset, length, extent, or count" and is bounded
only by `≠ 0` ✓. F4↔`[R-ENC-15]` + §19.1 step 4's "both obtainable within their records'
inline_length" ✓. F5↔`[R-CNT-27]` ✓. F6↔`[R-CNT-04]` including the residency exemption
and §2.3's denial of it to a verifier ✓. F7↔`[R-CNT-05]` ✓. F8–F17 are exactly
`[R-CNT-06]`'s nine, one row each, wording matching (F10's "exceeds F − 64" against
"≤ F − 64"; F32/L17 use the same boundary; an extent ending exactly at F − 64 is
conforming under all three) ✓. F18↔`[R-CNT-07]` ✓ (but see register-05).
F19↔`[R-CNT-08]` ✓ — and the row's gloss "this text defines no flag bits, so every such
bit is unimplemented" is sound, because §4.3's four growth vehicles admit new
*ignore*-lane bits only, so no minor can define an incompat bit. F20↔`[R-CNT-11]` ✓.
F21/F22↔`[R-CNT-25]`'s two clauses ✓. F23↔`[R-MTA-03]` ✓. F24/F25/F26/F29↔`[R-CNT-12]`
✓. F27↔`[R-MTA-05]` ✓. F28↔`[R-CNT-22]` ✓ (the only registered non-layer type is
0x0002, fixed MU=0/PE=1, so the row's two instances are the two bits). F30/F31/F32/F33↔
`[R-CNT-13]` ✓, and F33's parenthesis about (0, N) belonging to F30/L15 rather than
F31/L16 is right: a zero offset is the half-zero case, not the "1–15" case.
F34↔`[R-CNT-14]` ✓. F35/F36↔`[R-CNT-15]`'s reader MU gate and verifier reserved-range
duty ✓.

**§21.3 (49).** L1/L2↔`[R-ENC-03]`/`[R-ENC-04]`. L2's nine designated quantities check
out against the express designations: extent sums (`[R-CNT-13]`), N, P, N·P, C·N
(`[R-GEO-03]`), ordinals (`[R-ENC-04]`'s own list), P·Q and P·Bᶜ (`[R-SER-02]`), V
(`[R-SER-07]`), and the index-length formula (`[R-CNT-17]`) ✓. The parenthetical
dominance claims hold: C·N ≥ (C−1)·N + (N−1) for N ≥ 1, and P·Q ≥ P·C because Q = ΣBᵢ
and every Bᵢ ≥ 1 ✓. L3–L9↔`[R-ENC-11]`/`[R-ENC-12]`/`[R-ENC-15]`, with the open /
layer-access split matching §19.1 step 4 against §19.3 ✓; no "name too long" row exists
for layer/dimension/channel names, correctly, because a u8 prefix makes 255 unviolable —
and R10 does exist for metadata keys, which carry no prefix ✓. L10–L14, L19,
L23–L26↔`[R-CNT-25]`/`[R-MTA-03]`/`[R-CNT-12]`/`[R-CNT-14]`/`[R-CNT-18]`/`[R-CNT-15]` ✓.
L15–L18↔`[R-CNT-13]` ✓. L20↔`[R-CNT-16]` ✓. L21/L22↔`[R-CNT-17]` ✓ (at entry_count 0 the
formula yields 0, matching §7.4's "(0, 0)" and §15.4's "no region at all"). L27–L36 are
`[R-CNT-23]`'s enumerated constraint set plus the value-set rules it defers to
(`[R-GEO-01]`, `[R-GEO-05]`, `[R-TYP-03]`, `[R-TYP-07]`, `[R-SER-06]`) ✓.
L37/L38↔`[R-IDX-04]`, including L38's refusal to let 0xEECB3BB2 substitute for
comparison, which is `[R-IDX-05]`'s last sentence ✓. L39–L42↔`[R-SLB-01]`/`[R-SLB-03]`
✓, with L41's transparency carve-outs matching §16.2 word for word (sentinels
transparent; §15.3-*structural* entries transparent; an entry failing only its stored
bytes' crc **not** transparent). L43–L45↔`[R-COD-03]`/`[R-COD-07]`/`[R-COD-09]` ✓.
L46–L49↔`[R-CNT-12]`/`[R-MTA-05]`/`[R-CNT-22]` ✓.

**§21.4 (26).** T6–T12 map one-to-one onto §15.3's classification table, and §15.3's
"Six rows are marked *structural*" is exactly six (the sentinel-crc row, the half-
sentinel row, length = 0, offset < 16, the 2⁶³−1 row, the overflow/bounds row) ✓; the
remaining §15.3 rows map to T1 (stored bytes fail crc), L18, F33, and L40/L41/L42 ✓.
T2/T4/T5 partition `[R-SER-08]` and `[R-SER-05]` between real and padding positions
exactly as T2's own text claims ✓. T3↔`[R-SER-07]`, T13↔`[R-COD-02]`,
T14↔`[R-COD-04]` (note the row preserves the rule's "**non-sentinel**" qualifier ✓),
T15/T16↔`[R-COD-05]`, T17–T22↔`[R-COD-06]`, T23↔`[R-COD-07]`, T24/T25↔`[R-COD-08]`,
T26↔`[R-COD-10]` ✓.

**§21.5 (10).** R1↔`[R-CNT-25]`+`[R-MTA-03]`+`[R-EXT-03]` ✓; R2↔`[R-CNT-20]` ✓;
R3↔`[R-CNT-25]` ✓; R4↔`[R-MTA-09]` ✓; R5–R10↔`[R-MTA-04]`'s four restrictions plus
`[R-ENC-11]`/`[R-ENC-12]` ✓. §4.6's three name constraints on keys are covered as
R6 (empty; C0) and R10 (>255) ✓.

**Divergences found: none of the kind §21.1 anticipates.** I did not find a single row
whose condition, outcome class, scope or detector contradicts the requirement it cites.
That is worth stating plainly, because the brief warns that this is the class reporters
most often over-claim, and I looked hard for one.

---

## 5. Completeness in both directions

### 5.1 Nothing registered that is not a violation

Every row's condition is a MUST-level breach in its governing rule. The three that
looked like candidates for "registered but not actually a violation":

- **F19** (any incompat-lane bit set). `[R-CNT-08]` marks the *ignore*-lane bit as
  explicitly not a file-conformance violation and `[R-CNF-02]` names that as one of two
  stated conduct-only cases; by contrast the incompat bit is a violation. Closed.
- **F27 / L48** (unsorted metadata members) carry reject-file / reject-layer while
  `[R-MTA-05]` says readers process the document unchanged. §21.1 closes this in terms:
  "For a row whose Detector is *verifier*, the outcome names the scope at which the
  damage is recorded, not an obligation on any reader … `[R-MTA-05]`, whose unsorted
  document readers process as they find it — F27 and L48". Closed.
- **F36 / L25** (reserved-range type whatever the MU bit) carry reject-file /
  reject-layer while a reader takes ignore-record on the MU = 0 case. Same clause
  closes it. Closed.

### 5.2 Nothing omitted that is a detectable violation

I enumerated every "validity error" clause outside §21 (51 hits over the normalised
text), every "MUST NOT emit" (18), and every "makes the file nonconforming" (2), and
mapped each to a row or to a stated reason for having none. The rules with no row all
have one of four stated grounds, and I checked each ground against §21.7's test rather
than accepting the document's word:

- **Unwitnessed.** `[R-COD-10]`'s mis-strided filter where no structural constraint
  breaks; `[R-COD-06]`'s undisclosed dictionary; `[R-CNT-18]`'s nesting-depth
  prohibition (detecting it means parsing an opaque payload as records, which nothing
  obliges); `[R-SLB-04]`'s stale slab declaration (two byte-identical files, one written
  by a creator and one by an updater, differ only in history); `[R-WRT-05]`'s
  byte-identical re-emission and `[R-LIF-02]` step 3's own-directory rule (the live
  state names one generation, and §20.4's Rationale says the pairing "cannot, from the
  format"); `[R-WRT-06]`'s minor-floor and ignore-lane carry-forward (§20.5 says so);
  §20.3's §14 bar **in the case where the commit unstores the damaged tile**. I worked
  that last one carefully, because the §14 bar is *not* unwitnessed in general — a
  re-typed channel leaves stored tiles whose decoded size no longer matches, which T3 or
  T14 catches, and a shrink that creates a non-fill padding position is caught by T4.
  §20.3's sentence "This is precisely where the §14 bar has no witness, the live state
  being clean" reads, in context, as the *unstore-in-the-same-commit* case, and there it
  is right. The test decides all of these correctly.
- **SHOULD.** `[R-CNT-03]`, `[R-CNT-09]`, `[R-CNT-26]`, `[R-ENC-14]`, `[R-TYP-10]`,
  `[R-LIF-03]`'s randomness advice, `[R-LIF-07]`, `[R-MTA-06]`'s prefix advice,
  `[R-MTA-07]`'s placement advice. `[R-CNF-12]` places these outside the register ✓.
- **Conduct, not bytes.** `[R-EXT-03]`'s experimental prohibition; `[R-CNT-08]`'s
  flags = 0; `[R-CNT-05]`'s over-long pre-trailer gap. `[R-CNF-02]` names the last two
  expressly ✓.
- **No condition a file can exhibit.** `[R-ENC-06]` (see register-03), plus every
  purely reader-side rule (`[R-ENC-05]`, `[R-MDL-02]`, `[R-TYP-08]`, `[R-TYP-09]`,
  `[R-SEC-02]`, `[R-SEC-05]`, `[R-SEC-06]`, `[R-RDR-*]`).

`[R-ENC-07]` (fixed structure sizes) is never a governing rule but is fully subsumed:
the front block by F6, the record header by F29/L14, the entry array and CRC array by
L22, the user-metadata inline payload by F23/L12. That is correct under §21.1, whose
subject is the condition, not the requirement.

I also checked the *reverse* completeness of §21.6 against the rules that name defined
non-violations. All fourteen entries restate their rules faithfully. One shape is not in
the table but is stated in §21.6's closing prose: an **experimental**-range *sub-record*
type carrying MU = 1 is a conforming file whose layer a reader must nonetheless reject
(`[R-CNT-18]`). §21.6's table row is written for MU = 0 only, and the closing paragraph
covers the sub-record case in a parenthesis while counting only "Two structural cases …
conforming files a reader nevertheless refuses" — a count over *file* refusals, which the
sub-record case is not. So the count is right and the case is stated. I opened this and
closed it.

---

## 6. Cross-references to rows

Row labels are cited from outside the tables at eleven places. I resolved each:

| Where | Cites | Resolves? |
|---|---|---|
| §2.3 Note (l.273–280) | F14 reaches; F5 does not; F15 does not | ✓ F14 = trailer CRC; F5 = 128-byte floor derived from format-major-1 minimums; F15's cell does cite `[R-CNT-24]`, and its bytes are inside the redefinable 48 |
| §5.2 `[R-CNT-21]` (l.711) | L18, L40–L42 as rejections "the walk itself established" | ✓ all four are verifier/certification, reject-layer, and all four are decidable from the coverage walk plus index entries |
| §9.6 `[R-LIF-06]` (l.1408) | "F8, F14 and F17 — the magic, the trailer CRC and the length cross-check" | ✓ exactly those three rows |
| §17.2 deflate Note (l.2403) | T24 for a trailing whole byte | ✓ T24 is `[R-COD-08]`'s "bytes remain … after the stream" |
| §18.2 (l.2611–2646) | R3, R4 | ✓ R4 is the frame-constraint row and does register a nonzero dictionary ID, the content-size mismatch, etc.; R3 is the decode-failure row; §18.2's routing of a content-size mismatch to R4 rather than R3 matches R3's own text |
| §20.3 (l.3211) | L44 for the lz4 cap | ✓ |
| §20.5 `[R-WRT-06]` (l.3453–3455) | F36, L25 for record types, "one row for each of the other seven spaces §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)" | ✓ §10.2 tabulates eight spaces; record type is one, the other seven are channel layout (L36), linearization (L33), sample type (L34), codec (L43), filter (L45), index encoding (L31), metadata encoding (R1) — seven rows, one each, all correctly the *reserved*-range rows |
| §21.1 (l.3577–3579) | specialization pairs F1/F6, F1/F8, F35/F36, L24/L25, F21/F22, L10/L11 | Each pair holds as strict containment ✓ — but see **register-01** |
| §21.1 (l.3627) | F27 and L48 for `[R-MTA-05]` | ✓ |
| §21.6 (l.3863–3865) | F18; F35, F36, L24, L25 | ✓ as row references; see **register-05** on the gloss attached to F18 |
| App. H (l.4681–4693) | F1, F6; F7; F36, L25; R1 | ✓ all four resolve to rows saying what the citing text claims |

**No citation points at the wrong row.**

---

## 7. The limits material

### 7.1 §21.9's minimum-guarantee table against the rest of the document

Eight rows: rank 32, C 4096, entry_count 2³², layers 65,536, dir_length 16 MiB, decoded
tile 256 MiB, metadata document 16 MiB, zstd `Window_Size` 8 MiB. Appendix B's one-line
summary reproduces all eight verbatim ✓. §17.2 and §18.2 both cite "8 MiB" for
`Window_Size` ✓. §18.2 cites "16 MiB" for the document ✓. §2.5 `[R-CNF-10]` points at
"§21's limits table; … the table is §21.9" ✓. §1 and Appendix D both refer to the
entry_count guarantee being sized against the segment-CRC array, which the Note
substantiates and I re-derived ✓.

The per-instance paragraph partitions the table 5 + 3 and the table has 8 rows ✓; the
three per-instance rows are the last three ✓; the quantification of the tile row over
*addressed* tiles matches `[R-COD-07]`'s cap and §17.2's Note about an empty layer ✓.

### 7.2 §21.9's hard limits against their defining sections

All nine restated hard limits match their defining sections exactly (name ≤ 255 §4.6;
key ≤ 255 §18.2; rank ≤ 255 and C ≤ 65,535 §7.4; lz4 cap 0x7E000000 §17.2; 2⁶³−1 §4.2;
A power of two 512…2⁶² §16.1; A_slab power of two 1…2⁶² §16.2; S 1…2⁶³−1 §16.2;
dir_length ≥ 4 at dir_offset ≥ 16 §6.2; file ≥ 128 bytes §5.1). **A limit stated here
differently from its defining section: none.**

**A limit stated elsewhere and missing here:** the 5-byte minimum on a user-metadata
extent (§7.1, Appendix B); the 24-byte record header and 20-byte entry; the 64-byte
trailer and its 64-alignment; `inline_length`'s u32 ceiling. None of these is a defect,
because `[R-ERR-03]` disclaims inventory status in terms: "The hard limits it restates
are a finding aid rather than an inventory — each is normative where the structure
forcing it is defined." I checked that sentence specifically before closing the
question.

What that disclaimer does *not* cover is `[R-ERR-05]`'s **closed count** — "Two do not"
— which is a claim about the list as written, not about its completeness. That is
finding **register-04**.

---

## 8. Findings

### register-01 — §21.7's "exactly where" makes F1 a row the register may not carry

**Kind:** CONTRADICTION. **Location:** §21.7, `[R-ERR-01]`; §21.1, `[R-ERR-01]`'s
completeness clause and specialization clause; §21.2 row F1.

§21.7 states the test twice and, the second time, as a biconditional over the register:

> "The register carries a row for a condition exactly where it is a detectable
> file-conformance violation, so an unwitnessed condition is absent from it by that
> clause's own terms rather than in breach of them."

with detectability defined as

> "It is **detectable** in the contrary case: where some file exhibiting it is separated
> by such a check from every file that does not."

and unwitnessedness as

> "A condition this specification names is **unwitnessed** where, for every file
> exhibiting it, some file that does not exhibit it cannot be told apart from it by any
> check this specification obliges a reader or a verifier to perform."

I wrote the quantifiers out, as the brief asks. Let U be the files exhibiting condition
c and Sep_k(f,g) "obliged check k tells f from g".

- Unwitnessed(c) ≡ ∀f∈U ∃g∉U ∀k ¬Sep_k(f,g)
- Its negation ≡ ∃f∈U ∀g∉U ∃k Sep_k(f,g)

§21.7's claim that "each quantifier is the other's dual, so each is exactly the negation
of the other" is **true only under the distributive reading** of the *detectable* clause
— ∃f ∀g ∃k. The English ("separated **by such a check** from every file that does not")
also permits ∃f ∃k ∀g, one check separating f from everything else, which is strictly
stronger and is *not* the dual. I adopt the distributive reading, because §21.7 asserts
duality and because the stronger reading would also strip F35 of its row (a
reserved-range MU = 1 record needs the reader's MU gate to separate it from a
reserved-range MU = 0 record and the verifier's reserved-range check to separate it from
an experimental MU = 1 record — two different checks for two different siblings).

Now apply the adopted reading to **F1**:

> "F1 | A signature constant is stored byte-reversed — never to be adapted as a
> foreign-endian TARN file; the front-block instance binds only a reader holding bytes
> [0, 16) resident (`[R-CNT-04]`), the trailer-magic instance every reader
> (`[R-CNT-06]`) | front signature block bytes [0,8); trailer magic at F-64 | reader |
> open | `[R-ENC-02]` (R-CNT-04, R-CNT-06)"

Take f = a file whose front-block magic is the byte-reversal of the constant, everything
else conforming. Take g = a file identical to f except that bytes [0,8) are eight zero
bytes. g does not exhibit F1 (zeros are not a reversal). The only obliged check over
those bytes is `[R-CNT-04]`'s: "MUST verify the full block by byte equality … and MUST
treat any mismatch as reject-file". Its predicate is false on both f and g and its
outcome is reject-file on both. `[R-ENC-02]` obliges no evaluation: its content is
"a reader encountering what appears to be a byte-swapped signature (§6) MUST treat the
file as invalid (reject-file), **never as a foreign-endian file to be adapted**" — a
prohibition on a *response*, which a reader that never recognises the swap satisfies
vacuously. So no obliged check tells f from g, and by §21.7's own definition F1's
front-block instance is **unwitnessed**. The identical argument runs against F8 for F1's
trailer-magic instance.

This is not an accident of F1; it is what §21.1's specialization clause is *for*:

> "Some rows are strict specializations of others: where every file exhibiting one row's
> condition — at a given instance of it, where the row enumerates several — necessarily
> exhibits another's, the file is recorded against the narrower row, whose detector and
> detection point are the ones that apply. F1's front-block instance of F6 and its
> trailer-magic instance of F8 … stand in that relation"

A strict specialization is precisely a condition whose exhibiting files cannot be
separated from the generalization's by the generalization's check. Some specializations
survive anyway because a *second* obliged check separates them from the sibling cases
(F35/F36, L24/L25 via the MU gate; F21/F22 and L10/L11 because `[R-CNT-25]` states the
(0,0) case and the length-below-5 case as two separate checks). **F1 has no second
check.** So §21.1 deliberately creates a row that §21.7's biconditional forbids.

**Permitted readings.** (a) §21.7's "exactly where" is a genuine biconditional, and F1
is a defect in the register — the byte-reversal condition should be a gloss on F6/F8,
not a row. (b) "Exactly where" is loose and only the ⇒ direction ("detectable ⇒
registered", which is all §21.1's completeness clause actually claims) is normative; the
register may additionally carry narrower rows for attribution. (c) "A check separates f
from g" means merely that some rule names a predicate distinguishing them, whether or
not any actor is obliged to evaluate it — under which `[R-ENC-02]`'s "appears to be a
byte-swapped signature" is a check and F1 survives.

**I pick (b).** §21.1's completeness clause is stated one-directionally ("a *detectable*
… violation … the register omits is a defect"); §24's `[R-VEC-02]` already accepts
rows a vector cannot isolate ("where a condition cannot be isolated … the entry records
every row the file exercises and says which it was built for"); and reading (a) would
require striking a row, which §21.2's own Note treats as a heavier act than the document
contemplates. Reading (c) is available but makes the test's "instrument" the document's
prose rather than its obligations, which §21.7 elsewhere denies.

**What an implementer gets wrong without this.** A corpus builder or an auditor applying
§21.7's test literally to audit the register's completeness will conclude that F1 (and
any future strict specialization with no second check) must be struck; a builder
applying §21.1 will conclude the opposite, and the two disagree about which row a
byte-reversed-signature vector records under `[R-VEC-02]`. Neither disagrees about the
file's verdict.

**Byte-level: no.** Both readings reject a byte-reversed signature at file scope, by F6
or F8 if not by F1, and both readings leave every conforming file conforming. The
divergence is confined to row attribution in the corpus manifest.

---

### register-02 — `[R-CNF-12]` keys the verifier's duty to the register, which §21.7 says the test deliberately does not do

**Kind:** AMBIGUITY. **Location:** §2.4, `[R-CNF-12]`; §21.7, `[R-ERR-01]`; §21.1's
completeness clause.

§21.7 is explicit that the instrument must not be the rows:

> "The instrument is the checks this specification obliges an actor to perform, and
> deliberately not the register's own rows — a test keyed to the rows would make §21.1's
> completeness clause vacuous, every omitted condition being undetectable by
> construction."

But §2.4 scopes the verifier's checking duty by the register:

> "A verifier owes no search for one: §2.3's duty to check every file-level requirement
> runs to the MUST-level conditions §21 inventories, and a SHOULD deviation is reported
> where the verifier observes it and not hunted for."

If a verifier's duty "runs to the MUST-level conditions §21 inventories" in the
restrictive sense, then "the checks this specification obliges … a verifier to perform"
are, at the margin, exactly the register's rows — the keying §21.7 disclaims — and
§21.1's completeness clause becomes self-satisfying: any condition the register omits is
one no verifier is obliged to check, hence undetectable, hence rightly omitted.

**Permitted readings.** (a) Restrictive: the duty is bounded by §21's inventory. (b)
Appositive: the duty runs to MUST-level conditions, of which §21 happens to be the
inventory; the clause is there to exclude SHOULDs (which is the sentence's evident
purpose) and does not bound the duty by the table.

**I pick (b)**, on three grounds: the sentence's subject is SHOULD deviations
throughout; §2.3 states the duty as "checks every file-level requirement — including
those ordinary readers are exempted from", with no reference to §21; and §21.7's
disclaimer would otherwise be false of the document that contains it.

**What an implementer gets wrong without this.** Under (a) a verifier that meets a
MUST-level file-conformance violation the register omits certifies the file
*conforming*; under (b) it reports *nonconforming*. That is a verdict fork on identical
bytes — but only on a file exercising an actual omission, which §21.1 declares a defect
in the document rather than a state of affairs. I could not construct such a file: my
sweep in §5.2 above found no omitted detectable condition. I therefore grade this
**not byte-level**, honestly, rather than reaching for the hypothetical fork. The cost
is real but it is a cost in auditability: the register's completeness clause cannot be
audited by a reader who takes reading (a), and the document nowhere says which reading
governs.

The circularity is at present **latent, not actualised**: I checked all twenty
verifier-detected rows and every one of their governing rules states the verifier's
obligation in its own text ("a verifier MUST treat …", "A verifier MUST check …", "its
assigned detector is the verifier"). Not one row depends on `[R-CNF-11]`'s blanket duty
alone. That is what keeps the defect a documentation defect today.

---

### register-03 — §19.3 obliges a reader to validate what §21.7 says is not a state a file can be in

**Kind:** CONTRADICTION. **Location:** §21.7's closing paragraph, `[R-ERR-01]`; §19.3,
`[R-RDR-03]`.

§21.7:

> "Distinguish an unwitnessed condition from a requirement that states **no condition a
> file can exhibit**. `[R-ENC-06]`'s fixed field widths are not a state a file can be in
> — the parse is always at the widths this specification fixes, and a structure written
> at any other yields different values at them, caught by the rows for the fields that
> hold them. Nothing is omitted from the register on its account, there being no
> condition to omit."

§19.3 lists `[R-ENC-06]` among the things a reader MUST validate before first access to
a layer:

> "A reader's **first access** to a layer … MUST be preceded by full validation of the
> layer record — extent slot and inline payload both: … the fixed field widths and u64
> value domain of §4 (`[R-ENC-06]`, `[R-ENC-03]`), the value sets of §11.4, §12.2,
> §14.1, §15.1, §17.2, and §17.3 …"

These cannot both be right as written. If `[R-ENC-06]` states no condition a file can
exhibit, "validation of … the fixed field widths" names no act; if §19.3's list item is
a real validation obligation, then there is a condition, and the register omits it in
breach of §21.1's completeness clause. §19's own preamble sharpens the collision by
telling the reader that "§21's register is" the complete inventory of what a reader
detects at a tier — so an item on §19.3's list with no row is exactly the mismatch that
preamble tells a reader not to expect.

**Permitted readings.** (a) §19.3's item is a *parsing* convention — "parse at the fixed
widths" — not a check; §21.7 is right and §19.3 is loosely worded. (b) §19.3's item is a
check, and §21.7's disposal of `[R-ENC-06]` is wrong.

**I pick (a).** §21.7's argument is sound on its own terms: a file is bytes, a reader's
parse is fixed by this document, and a writer that "used the wrong width" has simply
produced different bytes, which the rows for the fields at the fixed widths then judge.
Reading (b) would require a register row for a condition nobody can state.

I note in passing that §21.7's supporting clause overstates: a structure written at some
other width "yields different values at them, **caught by the rows for the fields that
hold them**" is not guaranteed — a shifted parse can coincidentally satisfy every value
set and every length check and simply return wrong samples, which is §21.7's own
undetectable-content class. The overstatement is harmless because nothing is omitted on
its account, but it is the sentence a careful implementer will stop on.

**What an implementer gets wrong without this.** A conformance-checker author reading
§19.3 will look for a field-width check to implement at layer access, find none
statable, and either invent one (rejecting files no rule rejects) or conclude the
register is incomplete.

**Byte-level: no** — under reading (a) there is nothing to check and under (b) there is
nothing statable to check, so no two conforming readers can be made to disagree about a
file. It becomes byte-level only if someone resolves it by inventing a width heuristic,
which `[R-CNF-04]`'s "MUST NOT heuristically repair … or infer values this specification
does not define" already forbids.

---

### register-04 — is a declared alignment inside `[R-ENC-03]`'s value domain? L1's instances and `[R-ERR-05]`'s "Two do not" answer differently

**Kind:** AMBIGUITY. **Location:** §21.3 row L1; §21.9, `[R-ERR-05]`; §4.2,
`[R-ENC-03]`; §7.4.

`[R-ERR-05]` closes its hard-limit list with a closed count:

> "Most follow from a field's width, an external format, or the value domain, and the
> rest from arithmetic over structures a generation cannot omit. Two do not: the 512
> floor on A is a number chosen here, fixed at the legacy sector size (§16.1) so that a
> declared alignment is worth declaring, and the 255-byte cap on a user-metadata key is
> this specification folding §4.6's name rules onto keys, which carry no length prefix
> to force it."

I derived the members. The listed limits are: name ≤ 255 (field width); key ≤ 255
(chosen — named); rank ≤ 255 and C ≤ 65,535 (field widths); lz4 cap (external format);
2⁶³−1 (value domain); A a power of two, 512 ≤ A ≤ 2⁶² (floor chosen — named); A_slab a
power of two, 1 ≤ A_slab ≤ 2⁶²; S 1 ≤ S ≤ 2⁶³−1 (value domain); dir minimums and the
128-byte floor (arithmetic).

The **2⁶² ceilings on A and A_slab** follow from "the value domain" only if A and A_slab
are *in* it. `[R-ENC-03]` reads:

> "The valid range of every offset, length, extent, and count this specification
> defines — entry counts and slab run lengths included — is 0 to 2⁶³ − 1 inclusive"

It goes out of its way to name the two marginal members (entry counts, slab run lengths)
and does not name alignments. And **L1's instance cell excludes them**:

> "L1 | A u64 offset, length, extent, or count field of a layer record holds a value
> above 2^63 - 1 | layer record extent_offset; layer record extent_length; sub-record
> extent_offset; sub-record extent_length; dimension extent Eᵢ; tile extent Tᵢ;
> entry_count; slab run length S | reader | layer access | `[R-ENC-03]` (R-CNT-13,
> R-CNT-23)"

**Permitted readings.** (a) A and A_slab are outside `[R-ENC-03]`. Then L1's eight
instances are right, but `[R-ERR-05]`'s "Two do not" undercounts: the 2⁶² ceilings are
numbers chosen here too, as is the power-of-two shape constraint (no field width,
external format, value domain, or structural arithmetic forces an alignment to be a
power of two — u64 alone would admit 2⁶³). (b) A and A_slab are lengths inside
`[R-ENC-03]`. Then `[R-ERR-05]` is right, but L1's condition ranges over them and its
cell omits two instances — and §21.1's specialization clause would then record a file
with A = 2⁶³ against L1 rather than L39, since L1-at-A is strictly narrower than L39's
"A above 2^62" instance.

**I pick (a).** `[R-ENC-03]`'s own enumeration of its marginal members is the strongest
evidence in the document, and L1 was written to it. Under (a) the defect is confined to
`[R-ERR-05]`'s closed count, which is the smaller repair.

**What an implementer gets wrong without this.** A corpus builder counting instances
under reading (b) builds 277 vectors, not the 275 §21.8 states, and files two of them
against L1 rather than L39. An implementer reasoning about which fields the 2⁶³−1 domain
reaches gets a different answer for `A` than for `S`, with nothing in §4.2 to
distinguish them beyond the enumeration's silence.

**Byte-level: no.** A power-of-two alignment above 2⁶³−1 can only be 2⁶³, which L39
rejects at layer scope under both readings; a non-power-of-two above 2⁶³−1 is likewise
L39's. Same outcome, same scope, same detector. The divergence is in instance
attribution and in a stated count, not in any verdict.

---

### register-05 — F18 asserts a cross-major invariant no requirement establishes

**Kind:** AMBIGUITY. **Location:** §21.2 row F18 and its preamble; §21.6's closing
paragraph; §6.3, `[R-CNT-24]` and `[R-CNT-07]`.

F18's row and the two passages that gloss it all assert the same thing:

> "F18 | Trailer version_major is 0, a permanently invalid major in every format major
> version | version_major | reader | open | `[R-CNT-07]`"

> "F18 is not an exception but a case outside the premise: version_major = 0 declares no
> major at all and is permanently invalid in every one (§21.6)."

> "version_major = 0, permanently invalid in every format major version (F18,
> `[R-CNT-07]`)"

The cited rule says only:

> "A reader MUST reject-file when version_major is 0 (invalid) or is a major it does not
> implement" — `[R-CNT-07]`

and the document's sole instrument for binding future majors says:

> "In every format major version, permanently: the final 64 bytes of a file contain the
> trailer magic at F − 64, version_major and version_minor at F − 56, and a CRC-32C at
> F − 4 covering bytes [F − 64, F − 4); and the front signature block (§6.1) is
> constant." — `[R-CNT-24]`

`[R-CNT-24]` fixes the *position* of version_major in every major. It fixes no
constraint on its *value*. So "permanently invalid in every format major version" is a
claim about other majors' documents that this document nowhere establishes, and §21.1's
rule-governs clause makes `[R-CNT-07]` — a format-major-1 rule — the operative text.

**Permitted readings.** (a) The gloss is decorative: version_major = 0 declares no
major, so `[R-CNF-13]`'s premise ("a file declaring a format major other than 1") is not
met, the file falls to format major 1's rules, and `[R-CNT-07]` rejects it. That much is
sound and is what §21.2's "outside the premise" sentence actually needs. (b) The gloss is
normative and this document is asserting an invariant over every future major, in which
case `[R-CNT-24]` should carry it and does not.

**I pick (a).** The argument §21.2 needs — that F18 is outside `[R-CNF-13]`'s premise —
does not require the cross-major claim at all, and §21.1 makes the rule govern where a
row diverges from it.

**What an implementer gets wrong without this.** A verifier implementing majors 1 and 2
(once major 2 exists) has to decide whether a version_major = 0 file is a major-1
finding or is unjudgeable; under (a) it is a major-1 finding, under (b) it is a finding
under whichever major the verifier is applying. Nothing in this document decides it,
and `[R-CNT-24]`'s enumeration is where it would have to be decided.

**Byte-level: no.** Every reader of format major 1 rejects version_major = 0 at file
scope under both readings, and no conforming file carries it.

---

### register-06 — §21.1 attributes "the sole resolved byte" to §14.2, which does not say it

**Kind:** OBSERVATION. **Location:** §21.1, closing sentence; §14.2, `[R-SER-08]`;
§12.3, `[R-TYP-04]`.

> "`[R-SER-08]` is the one rule that goes the other way: it resolves a nonconforming
> interleaved boolean byte to a value rather than serving it through, which is why §14.2
> calls it the sole resolved byte in this format."

§14.2 says no such thing. The rule that calls it the one resolved case is `[R-TYP-04]` in
§12.3: "In a conforming file this rule admits no exception; the one case where a reader
resolves a byte to a value rather than passing it through arises only in a nonconforming
file, and `[R-SER-08]` states it." Appendix H (non-normative) uses the phrase "the sole
resolved byte". §14.2's own text and Rationale never characterise it that way.

The substance §21.1 asserts is correct — `[R-SER-08]` does resolve rather than serve
through, and it is the only such rule. Only the attribution is wrong, and it sends a
reader to the wrong section to check the claim. I report it because my charter is
cross-references and because §21.1 is the section that tells a reader how to read every
row; a wrong pointer there costs more than it would elsewhere.

**Byte-level: no.** No rule changes.

---

## 9. Suspicions I opened and closed

Recorded so that the clean parts of this lane can be seen to have been looked at.

1. **Does R2 (extent CRC) survive an experimental-range encoding?** §21.5's preamble
   excepts "an experimental-range encoding, where no document rule attaches" from being
   a violation. Closed by `[R-MTA-10]`: "file conformance … is decided by the structural
   checks that precede the document alone: the record's framing and extent slot
   (`[R-CNT-13]`), the encoding byte's own value set (`[R-MTA-03]`), and the extent's
   terminal CRC (`[R-CNT-20]`)." The extent CRC is not a document rule; R2's row carries
   no encoding qualifier; the exception's own ground ("where no document rule attaches")
   does not reach it.
2. **Does `[R-ERR-04]`'s enumeration of narrower scopes ("a layer or a tile") omit the
   record scope §18.2 uses for a metadata frame's window?** Closed: §18.2 assigns
   ignore-record on `[R-MTA-09]`'s own authority and cites `[R-ERR-04]` only for "the
   file … remains conforming while the reader MAY decline it". Both routes are
   permissions, neither is an obligation, and a reader taking either is conforming under
   `[R-CNF-03]`, whose acceptance duty does not run to a file exceeding a §21.9 row.
   No fork.
3. **Is `[R-CNF-07]`'s "reader outcome" wrong for the twenty verifier rows?** Closed by
   §21.1: "For a row whose Detector is *verifier*, the outcome names the scope at which
   the damage is recorded, not an obligation on any reader."
4. **Does §21.6's table omit the experimental MU = 1 *sub-record* case?** Closed: the
   closing prose states it, and its count of "two structural cases" is over files a
   reader refuses, which the sub-record case (reject-layer) is not.
5. **Is `[R-SLB-04]`'s stale slab declaration wrongly denied a row?** Closed by
   construction: two byte-identical files, one written by a creator and one by an
   updater carrying the declaration forward, differ only in history, so nothing
   separates them — unwitnessed under §21.7, and §16.2's Note reaches the same answer by
   a different route.
6. **Is the §14 bar of §20.3 step 4 wrongly denied a row?** Closed after working three
   cases: a re-typed channel *is* witnessed (T3/T14 fire on the surviving stored tiles),
   a shrink creating a non-fill padding position *is* witnessed (T4), and the
   unstore-in-the-same-commit case is not — which is the case §20.3's "the live state
   being clean" sentence is about, read in its paragraph.
7. **Does the sub-record nesting prohibition need a row?** Closed by §7.4's Note plus
   `[R-CNT-15]`: an unknown sub-record's payload is opaque and a user-metadata payload
   is one byte, so nothing obliges anyone to parse a payload as records; the one
   detectable case (a layer record as a sub-record) is L26.
8. **Is `file_id` missing from F2's instances?** Closed: `file_id` is neither an offset,
   a length, an extent nor a count, and §6.2 bounds it only by `≠ 0` (F12).
9. **Is a "name too long" row missing?** Closed: layer/dimension/channel names carry a
   u8 prefix, so 255 is unviolable; metadata keys carry none, and R10 exists.
10. **Does `[R-ENC-07]` (fixed structure sizes) need a governing row?** Closed: its
    conditions are registered under the rules for the structures that carry them (F6,
    F23, F29, L12, L14, L22), which is what §21.1's condition-not-requirement
    individuation requires.
11. **Do L3/L5/L6 belong at `open` rather than `layer access`?** Closed by §19.1 step 4,
    which parses and checks each layer record's name at the open and decides uniqueness
    "over the raw name bytes whether or not each name is itself well-formed".
12. **Is §21.6's "a conforming file with an empty directory" too strong for a
    zero-layer file carrying a user-metadata record?** Closed: `[R-CNT-14]` couples them
    the same way, so the entry restates its rule faithfully, which is all §21.1 asks of
    §21.6.

---

## 10. What I could not determine

- Whether "a check separates f from g" in §21.7 means the check's *predicate* differs or
  the actor's *obliged response* differs. I adopted the response reading (which is what
  makes the mis-strided filter and the undisclosed dictionary come out unwitnessed, as
  the document intends) and flagged the consequence for F1 as register-01. Under the
  predicate reading F1 survives, and I could find nothing in the document that chooses.
- Whether `[R-ENC-03]`'s domain reaches a declared alignment. I gave both readings and
  the reason I picked one; the document's only evidence is the enumeration's silence.

## 11. Byte-level assessment

**None of the six findings is byte-level.** I state that plainly rather than reaching.
Every one of them is confined to attribution (which row a condition records against),
to a stated count, to a cross-reference, or to a claim about a future major — and in each
case both permitted readings leave the same files conforming and produce the same
outcome, scope and detector for every violating file I could construct. The two places
where a fork was structurally available — register-02's verifier duty, and register-04's
value domain — I chased to a concrete file and could not reach one: register-02 needs an
actual omission from the register, and my completeness sweep found none; register-04's
only reachable value (A = 2⁶³) is rejected at layer scope by L39 under both readings.

The register itself is in unusually good order. Row-versus-rule agreement is exact across
all 120 rows; the detector/detection-point biconditional holds; both totals reproduce;
every row cross-reference resolves; and the limits material agrees with every defining
section. Where I found defects they are in the *frame* around the register — the test
§21.7 now states, the duty §2.4 scopes, and the counts §21.9 closes — which is what a
section that changed category would be expected to disturb.
