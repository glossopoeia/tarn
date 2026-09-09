# Cleanroom round 34 — Register hunter — working transcript

Charter: §21, the error-handling register and limits, audited against the rules it
restates and against itself.

## 0. Access and disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`.
The path in the brief was correct; the file was where it said it would be, 4,838 lines.
I did not open `docs/`, `conformance/`, `spec/registry.json`, `PLAN.md`, `AGENTS.md`,
`README.md`, or any ADR; I ran no git command, no web search, no directory listing.
I did not read the output directory.

Context I did not ask for **did** appear before I began: a project-instruction pointer
(`CLAUDE.md` → `AGENTS.md`) and an index of the maintainer's auto-memory listing a
dozen note titles about this project's harness, gates, and repair practice, several of
which name round-specific conclusions. I disregarded all of it — I did not open any of
those notes, and nothing below rests on a title I saw there. I am naming that it
appeared, not repeating its contents, as the brief requires.

Scratch files I wrote, all in
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r34-round/scratch/register/`:
`mk.py` (whitespace-normaliser producing `norm.txt` and `marked.txt`), `count_rows.py`
(row and instance counter), `xref.py` (row-label cross-reference sweep), `gov.py`
(Governing-rule-cell parser), `sweep.py` (normative-phrase counter), `crcchk.py`
(CRC-32C implementation and constant check). Nothing was written outside that directory
except this transcript.

On the wrapping hazard: the document is hard-wrapped and blockquotes carry `> `. I built
`norm.txt` by stripping leading `> ` markers and collapsing all whitespace to single
spaces before any phrase search, so no conclusion below rests on a line-oriented zero.
Where I did use line-oriented `grep`/Python over raw lines, it was on the register tables,
whose rows are each a single physical line — I verified that by parsing 120 six-cell rows
out of them, which a wrapped table could not have produced.

## 1. First pass: the shape of §21

§21 has nine subsections. §21.1 states the register's own rules; §21.2–§21.5 are the four
tables (reject-file, reject-layer, reject-tile, ignore-record); §21.6 is defined
non-violations; §21.7 is the detectability test; §21.8 is corpus coverage; §21.9 is limits.

I read all of §21 first, then read the whole document end to end (§1 through Appendix H)
before doing any row-versus-rule work, because every row cites a rule that lives elsewhere
and I did not want to judge a row against a rule I had only skimmed.

## 2. The counting

§21.1 fixes the arithmetic mechanically: "Instances within a cell are separated by
semicolons, and a cell reading — is one instance; the count is therefore mechanical once
the cell is written."

Before counting I checked the hazard that would break the mechanism: a semicolon nested
inside a parenthetical would split one instance into two. I ran a bracket-depth scan over
all 120 Instances cells. Zero nested semicolons, zero unbalanced brackets. So a naive
split is the rule's own split.

Rows, per subsection:

- §21.2: F1–F10 (10) + F12–F36 (25) = **35**. F11 is struck; §21.2's Note says so and
  §2.2's retirement model backs it. Header states 35. ✔
- §21.3: L1–L49 = **49**. Header states 49. ✔
- §21.4: T1–T26 = **26**. Header states 26. ✔
- §21.5: R1–R10 = **10**. Header states 10. ✔
- Total **120**. §21.8 states 120. ✔

Instances, per subsection (semicolon split, `—` = 1):

- §21.2 = **56**. Working, row by row: F1 2, F2 5, F3 2, F4 1, F5 2, F6 2, F7 4, F8 1,
  F9 1, F10 1, F12 1, F13 1, F14 1, F15 1, F16 1, F17 2, F18 1, F19 1, F20 1, F21 1,
  F22 1, F23 2, F24 1, F25 1, F26 1, F27 1, F28 2, F29 3, F30 2, F31 1, F32 1, F33 5,
  F34 1, F35 1, F36 1.
- §21.3 = **116**. L1 8, L2 9, L3 1, L4 2, L5 1, L6 1, L7 2, L8 2, L9 2, L10 1, L11 1,
  L12 2, L13 1, L14 3, L15 4, L16 2, L17 2, L18 3, L19 1, L20 1, L21 4, L22 4, L23 4,
  L24 1, L25 1, L26 1, L27 1, L28 1, L29 3, L30 2, L31 3, L32 3, L33 4, L34 4, L35 1,
  L36 2, L37 1, L38 1, L39 3, L40 1, L41 3, L42 1, L43 3, L44 3, L45 3, L46 2, L47 2,
  L48 1, L49 4.
- §21.4 = **55**. T1 1, T2 1, T3 6, T4 4, T5 1, T6 1, T7 2, T8 1, T9 1, T10 1, T11 2,
  T12 1, T13 2, T14 6, T15 2, T16 1, T17 1, T18 2, T19 1, T20 1, T21 3, T22 6, T23 1,
  T24 1, T25 3, T26 3.
- §21.5 = **50**. R1 4, R2 2, R3 2, R4 16, R5 8, R6 4, R7 6, R8 4, R9 2, R10 2.
- Total 56 + 116 + 55 + 50 = **277**. §21.8 states 277. ✔

Both totals reproduce exactly. This is the second thing I checked and I expected it to be
where a defect lived, given how recently the surrounding text changed; it is clean.

I then checked the cells against §21.1's two stated axes rather than only the arithmetic.

**Layout axis** — "Where the quantity a condition derives varies by layout, the layout
formulas are materially different shapes and the cell enumerates them." Rows deriving a
layout-varying quantity: T3 (3 layouts × 2 directions = 6), T14 (6), T21 (3 layouts × 1
direction), T22 (6), L44 (3 × 1), L21 (2 layouts × 2 directions = 4), T26 (3), T4 (4 —
interleaved numeric / interleaved bool / planar numeric / packed planar bool, which is the
three-layout split with interleaved further split by channel kind, matching §14.5's own
three-way statement plus the interleaved/planar distinction), L2 (layout-varying quantities
enumerated separately). I found no row that derives a layout-varying quantity and fails to
enumerate the layouts.

**Magnitude axis** — "a *differs from* or *does not equal*" gets two directions; an
*exceeds*/*larger than* gets one; a checksum or constant comparison gets none. I walked
every row whose Condition cell carries a comparison:

- Two directions: F17 (2), L21 (×2 layouts), L22 (2 dirs + 2 alternatives), L30 (2),
  T3/T14/T22 (×3 layouts). All correct.
- One direction: F5 ("below"), F9 ("less than"), F10 ("exceeds"), F16 ("less than"),
  F32 ("exceeds"), T9 ("ends past"), T21 ("larger than"), L44 ("exceeds"). All correct.
- No direction: F1, F6, F8, F14, F15, F20, L37, L38, T1, R2. All correct — these are
  byte-pattern-against-constant or stored-checksum-against-computed comparisons.
- Value tests, not comparisons: L20 (A ≠ 0 with S ≠ 0, 1 instance), L27, L28, F25 (MU/PE
  combination, 1 instance). §21.1 names exactly these shapes and the cells match.

**Single-predicate-over-several-fields** — "the fields it reads are not instances". F3
enumerates the two *sums*, not the four fields (2 instances); F25 and L20 enumerate 1.
Correct.

Instance-granularity calls I inspected and did **not** file:

- L23's four instances gloss the predicate as "(overrun or truncation)" without doubling,
  while L14 does enumerate header-truncation and inline_length-overrun separately. I
  satisfied myself these are different: L14's two are genuinely distinct predicates over
  distinct fields, L23's parenthetical is two viewpoints on one predicate.
- F7 and F33 enumerate "tile-index regions", "record extents" and "sub-record extents"
  side by side, though §5.2 makes a tile-index region and a sub-record extent both
  *record extents* ("the bytes any record's extent slot references, whatever the record's
  type"), and §9.7 says so explicitly ("the region enters the walk once, as that record's
  extent"). §21.1 licenses "a container it can occur in" as an instance axis, so
  enumerating kinds of record extent is permitted, and the counts are what the cells say.
  Not a defect.
- R8 collapses `NaN`, `Infinity` and `-Infinity` into one "bare token" instance while T15
  splits zlib from gzip. §21.1's rule decides this — a family that does not change the
  condition's shape is one instance — and the three bare tokens are the same shape while
  the two wrappers are not. Correct.

## 3. Row-versus-rule agreement, all 120 rows

I parsed every Governing-rule cell mechanically. All 120 name a bracketed requirement
identifier first. Exactly two carry a bracket-free section citation in the parenthetical:
L26 (`§7.3 registry table`) and L31 (`§7.4`). §21.1 claims exactly that — "the section
stating what it reads where no requirement identifier does, a value set (L31) or a
registered type's scope (L26), cited without brackets" — and it reproduces.

Governing-rule frequency, which I used as the spine for the row-versus-rule walk:
R-CNT-06 ×9, R-CNT-12 ×8, R-CNT-13 ×8, R-CNT-25 ×7, R-IDX-03 ×7, R-COD-06 ×6, R-CNT-23 ×5,
R-MTA-04 ×5, R-ENC-12 ×4, R-CNT-15 ×3, R-CNT-18 ×3, and 38 more rules at 1 or 2.

**The nine.** §2.3 and §21.7 both assert that `[R-CNT-06]` states nine conditions. I
derived the nine independently from the register: F8 (magic), F9 (dir_offset < 16),
F10 (dir sum past F−64), F12 (file_id = 0), F13 (committed_file_length not a multiple of
64), F14 (trailer CRC), F15 (reserved bytes nonzero), F16 (dir_length < 4), F17
(committed_file_length ≠ transport size). That is exactly nine, and §2.3's split — "the
trailer magic and the trailer CRC assert invariants `[R-CNT-24]` fixes and the other seven
do not" — is 2 + 7 = 9. Reproduces.

**Outcome-versus-scope, every row.** §21.1: "Conditions attach to the finest structure
they damage, and the outcome follows from that scope … except where a rule assigns one
expressly". I checked each row's subsection (which fixes its outcome) against the scope
its governing rule assigns:

- All 35 §21.2 rows: each governing rule says file scope or reject-file. F21/F22/F23
  reach it through "the record's containing scope" (§7.1, §18.2) with a top-level record,
  F25/F26/F28/F35/F36 through "the record's governing scope" (§7.2's `[R-CNT-13]`
  paragraph: "the file for other top-level records"), F27 through `[R-CNT-25]`'s "where a
  rule outside this quarantine records a document's defect at the file or the layer
  (`[R-MTA-05]`, F27, L48), the verifier records it there". All correct.
- All 49 §21.3 rows: layer scope in every case. L46/L47/L49 land at layer because §7.2
  assigns "the layer for a layer record and for sub-records". Correct.
- All 26 §21.4 rows: tile scope. T13, T15, T16 and T23 have governing rules that state no
  outcome of their own (`[R-COD-02]`, `[R-COD-05]`, `[R-COD-07]`'s block-format half); the
  rows say so — "the check that detects it is T25's" / "T24's" — and the detecting checks
  are `[R-COD-08]`'s, tile scope, which is also the owning scope §17 gives a stored tile's
  payload. Correct.
- All 10 §21.5 rows: ignore-record by express assignment (`[R-CNT-25]`'s quarantine, and
  `[R-MTA-09]` for R4). Correct, and §21.1 flags exactly this exception.

I found **no** scope or outcome divergence between any row and its governing rule. That is
the class the brief warns is the dominant over-claim, so I state it plainly: there is
nothing here to over-claim.

**Detector and detection-point vocabulary.** 100 rows carry Detector *reader*, 20 carry
*verifier*. Detection points, mechanically: open 31, layer access 34, tile use 24, extent
use 9, certification 20, plus two compound cells (L23's "open (the name field, §19.1 step
4); layer access (every other field and entry)" and R1's "open (top-level); layer access
(sub-record)"). §21.1 says "Detection points name §19.2's reader tiers — open, layer
access, tile use, extent use — or *certification* for the rows a verifier detects". Every
value is drawn from that list, and Detector=verifier ⟺ Detected=certification, with no
exception in either direction.

I checked the two compound cells against §19: L23's split matches §19.1 step 4's rule that
"a layer record whose name field does not lie entirely within that record's inline_length
… is instead a validity error at layer scope (`[R-CNT-18]`)", and R1's split matches the
inline payload being read at open for a top-level record and at layer access for a
sub-record.

The 20 verifier rows are F7, F25, F26, F27, F28, F33, F36, L18, L25, L40, L41, L42, L46,
L47, L48, L49, T2, T4, T5, T26. I checked each against a MUST-level obligation, because
§2.4's `[R-CNF-12]` says "§21's register enumerates MUST-level conditions only": F7 ←
`[R-CNT-05]` "A verifier MUST treat a structure in that gap as a validity error at file
scope"; F25/F26/L46/L47 ← `[R-CNT-12]` "a verifier MUST treat a nonzero reserved flag bit
or the MU = 1 with PE = 0 combination as a validity error"; F27/L48 ← `[R-MTA-05]`
"Writers MUST serialize object members … the file is nonconforming, a verifier MUST report
it"; F28/L49 ← `[R-CNT-22]` "writers MUST emit exactly the flag values fixed in the table
above … a verifier MUST treat the mismatch as a validity error"; F33/L18 ← `[R-CNT-13]`;
F36/L25 ← `[R-CNT-15]`; L40/L41/L42 ← `[R-SLB-01]`/`[R-SLB-03]`'s "A verifier MUST check
the invariant(s)"; T2 ← `[R-SER-08]`; T4/T5 ← `[R-SER-05]`; T26 ← `[R-COD-10]`. No row
registers a SHOULD.

I also checked the keyword-free declaratives in the chain, because the brief warns not to
treat them as inert: `[R-SLB-01]`'s "When declared: every stored tile's offset satisfies
offset mod A = 0", `[R-SLB-03]`'s run continuity, `[R-COD-05]`'s "The stored bytes are
exactly one DEFLATE compressed data stream", and `[R-COD-07]`'s "The stored bytes are
exactly one LZ4 block". Each is paired with an explicit verifier or reader MUST elsewhere
in its own rule, so the register's rows for them are properly grounded.

## 4. Completeness, inward: does any row register a non-violation?

Checked all 20 verifier rows above and spot-checked reader rows. Every row traces to a
MUST-level requirement. No row registers something the rules leave conforming.

The two entries §21.6's closing paragraph says moved out of the non-violation table —
unsorted document members and a registered type's stored-flag mismatch — are now F27/L48
and F28/L49, all four Detector *verifier*, exactly as that paragraph says.

## 5. Completeness, outward: is any violation missing a row?

I swept `norm.txt` for the phrases that create file conditions and walked every hit:
`validity error at` (52), `MUST NOT emit` (18), `is a violation` (5), `makes the file
nonconforming` (3), `reject-file` (23), `reject-layer` (21), `reject-tile` (19),
`ignore-record` (20), `MUST treat` (36), `a verifier MUST` (9), `MUST NOT declare` (2),
`MUST equal` (5), `unreadable` (10). Then I walked the requirement identifiers by prefix
and asked, for each, whether it names a condition and whether a row registers it.

Everything I could construct as a file condition has a row. The ones I had to work at:

- **`[R-IDX-03]`'s eleven-row table (§15.3)** maps completely: sentinel-with-crc → T6;
  half-sentinel → T7; length 0 → T10; offset < 16 → T8; over-domain → T11; overflow /
  past F−64 → T12 and T9; stored bytes fail crc → T1; intra-layer overlap → L18;
  cross-scope overlap → F33; alignment/slab invariant → L40/L41/L42. Eleven table rows,
  eleven register destinations.
- **`[R-CNT-06]`'s ordered gates** → the nine above.
- **`[R-CNT-12]`'s flag rules** partition every record: MU = 1/PE = 0 → F25 (non-layer
  top-level) + L46 (layer record, sub-record); reserved bits 2–15 → F26 + L47. No record
  kind falls between them.
- **`[R-CNT-22]`** → F28 (top-level user-metadata, the only non-layer registered top-level
  type) + L49 (layer record, and a registered sub-record type). Complete.
- **`[R-EXT-03]`'s bar on emitting reserved-range values** → F36/L25 for record types plus
  one row per remaining space in §10.2's table: L31 index encoding, L33 linearization, L34
  sample type, L36 channel layout, L43 codec, L45 filter, R1 metadata encoding. Eight
  spaces, eight destinations. §20.5 makes exactly this claim ("one row for each of the
  other seven spaces §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)") and it holds.
- **`[R-MTA-04]`'s four decoded-document restrictions** → R7 (object/BOM/well-formedness),
  R8 (finite numbers), R9 (duplicate keys), R5 + R6 + R10 (UTF-8 and the folded §4.6 name
  rules: well-formedness, non-empty, C0-free, ≤ 255 bytes). Complete.
- **`[R-MTA-09]`'s carried-over frame constraints** → R4's eight alternatives: magic,
  skippable frame, second frame, dictionary ID, content-checksum flag, bytes remaining,
  content-size larger, content-size smaller. §18.2 states which two of the carried
  constraints fall outside the register and why ("dictionary use the header does not
  disclose … an unwitnessed condition … while the bar on sizing a buffer binds a reader
  rather than the document, and so states no condition a file can exhibit at all"), and R4
  registers neither. That is 8 × 2 containers = 16, which is what the cell has.

Absences the document itself accounts for, which I confirmed rather than assumed:

- `[R-SLB-04]`'s stale slab declaration: §16.2's Note says its detection *is*
  `[R-SLB-03]`'s, so no row of its own. I tested it: a carried-forward declaration whose
  invariants happen to hold is not a violation of anything observable, and one whose
  invariants fail is L41 or L42. Sound.
- `[R-CNT-18]`'s nesting prohibition: §7.4's Note says it has no reader-detectable witness
  in format major 1, because a reader parses a sub-record payload as records only for the
  layer record, whose appearance as a sub-record is L26. Sound.
- `[R-CNT-02]`'s "belongs to no class" half: §5.2's Note says a row for it "would be a row
  no file could exhibit", because `[R-LIF-08]` makes every byte the walk misses slack.
  Only disjointness is testable, and that is F33 + L18. Sound.
- `[R-ENC-06]`'s field widths: §21.7 names it as a requirement stating no condition a file
  can exhibit. `[R-ENC-01]`'s byte order is the exactly parallel case and is *not* named
  there — but §21.7 disclaims being a list ("That is the whole of the test, and it decides
  any condition put to it without appeal to a list"), and the one detectable byte-order
  condition, a byte-reversed signature constant, is F1 under `[R-ENC-02]`. Sound.
- Residue past a completed commit: §9.5's Note says it carries no row because a reader
  meets it as F8, F14 or F17. I checked that trio against §9.6's identical citation
  ("§21.2 rows F8, F14 and F17 — the magic, the trailer CRC and the length cross-check").
  Both resolve.
- Undisclosed compression dictionaries and mis-strided filters with no structural
  constraint: §21.7 names both.

I found no unregistered detectable file-conformance violation.

## 6. Every cross-reference to a row

I swept every line of the document for `\b[FLTR]\d{1,2}\b` and separated hits inside the
register tables from hits elsewhere. Forty-nine citations outside the tables, spanning 39
distinct row labels. I resolved each against the row it names:

- §2.3's Note: F14 reaches, F5 does not, F15 does not — checked each against `[R-CNT-24]`'s
  four fixed invariants (magic at F−64, version fields at F−56, CRC at F−4 over
  [F−64, F−4), constant front block). F14's subject is the CRC ✔; F5's floor is derived
  from format-major-1 directory minimums ✔; F15's bytes are inside the redefinable 48 ✔.
- §2.3 and §21.6: F18 for version_major = 0 ✔; F35/F36/L24/L25 for reserved-range types ✔.
- §21.2's reach derivation: "F8, F14, F6 and both of F1's instances … and no other row". I
  derived this independently from `[R-CNT-24]`'s four invariants and got exactly that set.
  Reproduces.
- §5.2: "L18's overlap or L40 through L42's placement" — all four are verifier/reject-layer
  rows a coverage walk can establish ✔.
- §6.2's trailer table: "a set bit being reject-file (F19)" ✔.
- §7.1: "(`[R-MTA-05]`, F27, L48)" ✔.
- §7.4's Note: "whose appearance as a sub-record §21.3 registers" → L26 ✔.
- §9.6: F8, F14, F17 ✔.
- §17.2's Note: "`[R-COD-08]` rejects it (§21.4, T24)" ✔.
- §18.2: R1, R3, R4 ✔ — including "encoding 0 and a reserved value are unassigned too and
  R1 registers both", which matches R1's four instances exactly.
- §20.3: "(L44, the largest channel plane governing in a planar layer)" ✔ — L44's condition
  says exactly that. And "(T3, T14, T21, T22, T4, T5, T2) … (T24, T25)" for what the
  register witnesses about a changed fixed declaration: four decoded-size rows, two
  padding/pad-bit rows, one boolean-byte row, two decode-failure rows. All nine resolve to
  rows whose conditions are what the sentence claims.
- §20.5: "F36 and L25 for a record type, and one row for each of the other seven spaces
  §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)". §10.2 tabulates eight spaces; minus
  record type leaves seven; the seven labels are the seven right rows. Reproduces.
- §21.1's specialization list — F1/F6, F1/F8, F35/F36, L24/L25, F21/F22, L10/L11. I tested
  each for strict containment: a byte-reversed front magic is necessarily not byte-identical
  to the constant ✔; a byte-reversed trailer magic is necessarily not the trailer magic ✔;
  reserved-range-with-MU=1 ⊂ reserved-range-whatever-MU ✔; extent slot (0, 0) forces
  extent_length 0 < 5 ✔ (both for F21/F22 and L10/L11). All six hold, and in each case the
  named narrower row is the one §21.1 says the file is recorded against.
- §21.1's instance examples: T24's "any codec" is one instance ✔; T15 (2) and T25 (3)
  enumerate materially different shapes ✔.
- Appendix F: RFC 1950 and RFC 1952 both cited to T15, whose two instances are exactly
  "zlib RFC 1950 (CMF/FLG header + trailing Adler-32); gzip RFC 1952 member (1F 8B,
  trailing CRC32+ISIZE)" ✔.
- Appendix H: "(F1, F6)" for the front block, "(`[R-CNT-05]`, F7)" for the pre-trailer gap,
  "(`[R-CNT-15]`, F36, L25)" for reserved-range types, "(R1)" for encoding 0 and the
  reserved range. All resolve.

One citation is not cleanly resolvable, and it is **register-01** below: §21.1's
"— F27 and L48" in a parenthetical that also carries `[R-CNT-22]`, whose rows are F28 and
L49.

Every other row citation in the document points at a row that says what the citing text
claims it says.

## 7. Outcome vocabulary

§2.4 `[R-CNF-07]` defines four reader outcomes — reject-file, reject-layer, reject-tile,
ignore-record — and §2.4's table adds preserve-verbatim, expressly "an updater obligation,
orthogonal to reader outcomes". The register's four subsections use exactly the four
reader outcomes, one per subsection, so all four are used and all four are reachable
(35, 49, 26 and 10 rows respectively). preserve-verbatim is not a register outcome and
§2.4 says so; it is reachable through §20.4's table.

I checked the one structural oddity: `[R-CNF-08]` maps owning scopes to only three
outcomes (file → reject-file, layer → reject-layer, tile → reject-tile), so ignore-record
is unreachable from an owning scope. That is not a gap — §21.1 states the express-assignment
exception and names `[R-CNT-25]` and `[R-MTA-09]` as the two rules that use it, and I
confirmed that all ten §21.5 rows and no other row take their outcome that way.

§21.6's Defined-behavior cells use "Ignored", "Ignore-record", "Conforming", "Accepted",
"Defined", "Expected", "Inert", "Slack", "A valid, empty layer". §2.4 licenses this —
"The same vocabulary is used for defined conditions that are not violations (an unknown
ancillary record is *ignored*, not rejected)" — and §21.1 says the subsections after §21.5
carry no rows, so they are not held to the register's column discipline.

## 8. Limits, both directions

**The guarantee table** (rank 32, C 4096, entry_count 2³², layers 65,536, dir_length
16 MiB, decoded tile 256 MiB, metadata document 16 MiB, zstd Window_Size 8 MiB). I checked
it against Appendix B's "Reader minimum guarantees" row: identical, all eight values in the
same order. Against §2.5 `[R-CNF-10]` and §2.3 `[R-CNF-03]`: both say a conforming reader
MUST accept any conforming file within these, and §21.9 says the same. Against §17.2 and
§18.2, which both defer to "§21.9's 8 MiB `Window_Size` guarantee": consistent.

I re-derived the Note's arithmetic. At entry_count = 2³², the segment-CRC array is
⌈2³²/2¹⁶⌉ × 4 = 2¹⁶ × 4 = 262,144 bytes = 256 KiB — the Note says 256 KiB. At 2³⁶ it is
2²⁰ × 4 = 4,194,304 = 4 MiB — the Note says 4 MiB. Both reproduce. The Note is a labelled
Note and therefore non-normative under `[R-CNF-01]`, which I checked before spending time
on its looser claims ("roughly a 12.5 MiB directory", "an order of magnitude above").

I checked the guarantees against the hard limits for consistency: rank 32 < 255 ✔; C 4096
< 65,535 ✔; entry_count 2³² < 2⁶³−1 ✔; 256 MiB decoded tile < 0x7E000000 = 2,113,929,216,
so a codec-4 layer can still meet the tile guarantee ✔; dir_length 16 MiB ≥ 4 ✔.

**The hard limits.** Nine are listed. Each matches its defining section: name ≤ 255 bytes
(§4.6); user-metadata key ≤ 255 bytes (§18.2's folding of §4.6); rank ≤ 255 and C ≤ 65,535
(§7.4's u8 and u16); codec 4's 0x7E000000 (§17.2 `[R-COD-07]`, including "the largest
channel plane governing in a planar layer", which is `[R-COD-07]`'s own wording); the
2⁶³−1 value domain (§4.2 `[R-ENC-03]`); A a power of two 512…2⁶² and A_slab a power of two
1…2⁶² (§7.4's table, §16.1, §16.2); S in 1…2⁶³−1 (§7.4, §16.2); dir_offset ≥ 16 and
dir_length ≥ 4 (§6.2); 128-byte floor (§5.1 `[R-CNT-27]`). **No limit claimed in §21.9 is
stated differently by its defining section.**

In the other direction, hard limits stated elsewhere and absent from §21.9's list:
the user-metadata extent minimum extent_length ≥ 5 (§7.1, and Appendix B lists it as
"User-metadata extent minimum"), the record header size of 24 bytes, the index entry size
of 20 bytes, the 64-byte trailer, and the geometry floors d ≥ 1, C ≥ 1, Tᵢ ≥ 1
(`[R-GEO-01]`). I did **not** file any of these, because §21.9 disclaims inventory-hood in
terms: "The hard limits it restates are a finding aid rather than an inventory — each is
normative where the structure forcing it is defined." The extent_length ≥ 5 omission is the
one that made me look hardest, since §21.9 *does* carry the exactly parallel "directory of
at least 4 bytes" minimum and Appendix B carries both; the disclaimer closes it.

What I did file from §21.9 is **register-03**: the sentence individuating the first five
rows, which a conforming zero-layer file falsifies.

## 9. §21.7, checked as a piece of logic

§21.7 defines *unwitnessed* and *detectable* and claims "each quantifier is the other's
dual, so each is exactly the negation of the other". I checked that rather than taking it.

Detectable: ∃f ∈ C. ∀g ∉ C. ∃check separating f from g.
Unwitnessed: ∀f ∈ C. ∃g ∉ C. no check separates f from g.

¬Detectable = ∀f ∈ C. ¬(∀g ∉ C. ∃check) = ∀f ∈ C. ∃g ∉ C. ¬∃check. That is Unwitnessed
verbatim. The duality claim holds.

§21.1 restates the detectability half — "a condition is detectable exactly where some file
exhibiting it is separated from every file that does not by some check this specification
obliges a reader or a verifier to perform, not necessarily the same check for each such
file" — and it is the same predicate as §21.7's, including the non-uniformity clause
("which need not be the same check for every one of those files"). No divergence.

§21.7's claim that "`[R-CNT-06]` shows by stating nine" reproduces (§3 above).

## 10. Degenerate legal files

Shape 8 of the brief. I built the smallest legal cases I could and ran the register at them.

- **Zero-layer file** (Appendix A's 128 bytes; §21.6 records it valid). dir_length = 4,
  CRC over zero bytes = 0x00000000. I recomputed that CRC and Appendix A's trailer CRC
  (see §11). No register row fires. The one thing that does break is §21.9's sentence about
  the first five limit rows — **register-03**.
- **Layer with a zero-extent dimension.** N = 0, addressed-tile count 0, entry_count = 0,
  extent slot (0, 0), crc_of_crc_array = 0. L22's formula gives 0 ✔; L27 is satisfied ✔;
  L37 compares 0 against CRC-32C of zero bytes = 0 ✔; §17.2's Note and §21.9 both handle
  the lz4 cap's escape ✔. §15.4's Example states the same and matches.
- **entry_count = 65,536 exactly.** One segment, 4-byte array, extent_length =
  65,536 × 20 + 4 = 1,310,724. §15.4's Example says "1 ≤ entry_count ≤ 65,536 has one
  segment and a 4-byte array" ✔.
- **P = 1 packed planar bool plane.** ⌈1/8⌉ = 1 byte, 1 mod 8 = 1 ≠ 0, so pad bits 1–7
  exist and T5 applies. §14.4's Note says exactly this ✔.
- **P ≡ 0 mod 8.** No pad bits; T5's condition is vacuous, correctly, since it says
  "with P mod 8 ≠ 0".
- **A layer with A = 0, S = 0, A_slab = 0.** No declaration, no row fires. I then walked
  the whole (A, S, A_slab) space: A ≠ 0 ∧ S ≠ 0 → L20; S = 0 ∧ A_slab ≠ 0 → L28;
  S ≠ 0 ∧ A_slab invalid (0 included) → L29; A nonzero and out of shape → L39. The space
  is partitioned with no gap and no double-registration.

## 11. Arithmetic and checksums I recomputed

I implemented CRC-32C from §4.5's parameters (polynomial 0x1EDC6F41, reflected in/out,
init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and checked it against the document's own check
vector before using it.

| Quantity | I computed | Document states |
|---|---|---|
| CRC-32C("123456789") | 0xE3069283 | 0xE3069283 (§4.5) |
| CRC-32C(zero bytes) | 0x00000000 | 0x00000000 (§4.5) |
| CRC-32C of 2¹⁶ sentinel entries | 0xEECB3BB2 | 0xEECB3BB2 (§15.4, Appendix B, **L38**) |
| CRC-32C of 4 sentinel entries (80 B) | 0x80A34955 | 0x80A34955 (§7.4 Example) |
| CRC-32C of that 4-byte array | 0xC4EE982E | 0xC4EE982E (§7.4 Example) |
| Appendix A trailer CRC over [0,60) | 0x402F157E | 0x402F157E (Appendix A) |

L38's cell names 0xEECB3BB2 as "the all-sentinel constant … [that] never substitutes for
comparison"; the constant is right and the row's use of it matches `[R-IDX-05]`.

Other numbers I derived and compared:

- Register rows 35 / 49 / 26 / 10, total 120 — matches §21.2, §21.3, §21.4, §21.5 headers
  and §21.8.
- Register instances 56 / 116 / 55 / 50, total 277 — matches §21.8.
- Verifier rows 20, reader rows 100 — no stated figure to compare, derived for §7's checks.
- `[R-CNT-06]` governs 9 rows — matches §2.3 and §21.7's "nine".
- §10.2 tabulates 8 identifier spaces; §20.5 names 1 + 7 — reproduces.
- Segment-CRC array at 2³² entries = 256 KiB; at 2³⁶ = 4 MiB — matches §21.9's Note.
- §7.4's Example payload: 4 + 34 + 18 + 12 + 13 = 81 bytes, extent length
  4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84 — both match.
- §15.4's Example: 16 segments (15 full + 16,960), 64-byte array, region 20,000,064 bytes,
  entry 999,999 at segment-relative byte 339,180, segment 15 at [19,660,800, 20,000,000),
  full segment 1,310,720 B = 1.25 MiB — all match.
- §11.4's Example: s = 10 for tile (1,2); in-tile ordinal 44·256 + 188 = 11,452; planar
  disk ordinal 2·32 + 10 = 74; §15.4 puts entry 74 at [1,480, 1,500) — all match.
- §17.3's byte-shuffle Example: I applied i·n + j by hand to the twelve bytes and got
  `00 00 00 00 00 00 80 00 40 3F 40 40` — matches.
- §14.3's packed-bool Example: byte 0 = 0x55, byte 1 = 0x01 with fill false, 0xFD with fill
  true — matches.
- §20.3's Example: 32 · 20 + 4 = 644 — matches.

Every number the document states in or around §21 reproduces.

## 12. Findings

Five. None is byte-level; I say why for each. I want to be explicit that the register
itself — the 120 rows, their outcomes, scopes, detectors, detection points, governing
rules, instance counts and totals — came through this audit clean. What survived is in the
prose *around* the tables.

---

### register-01 — AMBIGUITY — §21.1, verifier-detector paragraph

**Location.** §21.1, final paragraph, the parenthetical naming `[R-CNT-22]` and
`[R-MTA-05]`. Rows affected: F27, F28, L48, L49.

**Quotation.**

> the governing rule states what a reader does, and for
> several such rows it obliges the reader that serves the structure to
> serve it unchanged (`[R-CNT-22]`, whose registered type keeps its
> fixed semantics; and `[R-MTA-05]`, whose unsorted document readers
> process as they find it — F27 and L48), `[R-CNF-12]`'s licence to
> reject the nonconforming file being untouched in each.

**The problem.** The parenthetical opens on "several such rows" and then lists two *rules*
with a gloss each, closing with a row citation "— F27 and L48". The scope of that citation
is undetermined.

Reading A: "— F27 and L48" attaches to the `[R-MTA-05]` clause alone. Then the sentence is
true — F27 and L48 are exactly `[R-MTA-05]`'s two rows — but asymmetric: `[R-CNT-22]`'s
rows, F28 and L49, go unnamed while its sibling's are named.

Reading B: "— F27 and L48" names "several such rows", i.e. the rows of both rules. Then it
is wrong twice over. The rows are four, not two, and the two named belong to only one of
the two rules: F28's Governing rule cell reads `[R-CNT-22]` (R-CNF-05) and L49's reads the
same, while F27's and L48's read `[R-MTA-05]` (R-CNF-05).

**Which I picked and why.** Reading A. §7.1's `[R-CNT-25]` uses the identical citation
shape and there it is unambiguous — "where a rule outside this quarantine records a
document's defect at the file or the layer (`[R-MTA-05]`, F27, L48), the verifier records
it there" — so the document's own practice pairs F27/L48 with `[R-MTA-05]` and nothing
else. A reader who checks the tables reaches the same place.

**What an implementer does wrong without it.** A corpus builder or a verifier author
reading §21.1 straight through under reading B looks for `[R-CNT-22]`'s rows at F27 and
L48, finds `[R-MTA-05]` conditions there, and either mis-labels vectors — which §24
`[R-VEC-02]` makes load-bearing, since a manifest entry must record "the §21 register row
it exercises together with that row's governing requirement identifier" — or concludes
that only two verifier rows carry a serve-unchanged reader clause when four do.

**Byte-level?** No. Both readings leave every row's condition, outcome, scope and detector
exactly where the tables put them, and §21.1's own tie-break ("where a row and the rule it
cites diverge, **the rule governs**") plus `[R-VEC-01]` ("where a vector's recorded
expectation and this specification disagree, this specification governs") keep the
emittable and acceptable sets fixed. The cost is a mislabelled corpus entry, not a
different file.

---

### register-02 — AMBIGUITY — §21.6, the trailer-mimic entry

**Location.** §21.6, table, the entry governed by `[R-LIF-06]`.

**Quotation.**

> | A payload contains a byte string that mimics a trailer | Inert: nothing enumerates slack, and a recovery tool re-verifies its output whole (§9.6) — which catches any mimic that is not itself a consistent generation; §9.6's second caution covers the rest | `[R-LIF-06]` |

**The problem.** The Condition cell names a **payload**; the first clause of the Defined
behavior cell justifies inertness by a fact about **slack**. The two are different classes
under `[R-CNT-02]`, which makes a stored-tile extent a *structure* of the live committed
state and slack "Every byte the live state does not claim". §9.7 has the coverage walk
reach "the stored extent of each non-sentinel tile-index entry" — so a live payload is
precisely something that *is* enumerated.

The source this entry is condensing keeps the two apart. §22.3 `[R-SEC-04]`:

> And a payload can contain a byte string that mimics
> a trailer; recovery tooling that scans backward can land on one, which
> is why recovery output is re-verified as a whole file before being
> trusted (`[R-LIF-06]`): under live-state coverage a mimic in slack
> is inert — nothing enumerates it — but a recovery tool that
> truncates to one produces a different file.

There, "nothing enumerates it" is said of a mimic *in slack*, and what is said of a mimic
in a *payload* is that a recovery tool can land on one.

**Permitted readings.**

1. The condition covers a mimic in a **live** stored-tile payload — the case §9.6's first
   caution names ("a tile payload can deliberately contain a byte string that mimics a
   valid trailer"). The conclusion "Inert" still holds, but for a different reason than the
   one given: a reader never scans backward (`[R-LIF-05]`) and the coverage walk claims the
   bytes as a stored extent. "Nothing enumerates slack" is not that reason; the payload is
   enumerated.
2. The condition covers a mimic in a **superseded** payload, which is slack. Then the
   reason holds, but the entry no longer covers the case §9.6 and §22.3 actually warn about,
   and the Condition cell's bare "A payload" does not say so.

**Which I picked and why.** Reading 1, because the governing rule `[R-LIF-06]` states the
caution over "a tile payload", not over slack, and because §21.1 makes the rule govern a
§21.6 entry that diverges from it: "§21.6's entries restate their governing rules on the
same terms a row does, and where such an entry and the rule it cites diverge, the rule
governs there too."

**What an implementer does wrong without it.** A verifier author who takes the entry's
reason at face value concludes that a trailer-mimic is a slack phenomenon and that the
live-state walk need not consider it — which is true of the conclusion but reached from a
false premise, and it is the wrong mental model for the one actor that *is* exposed: a
recovery tool, which probes every 64-aligned offset of the physical file, live payloads
included, and is why `[R-LIF-06]` requires whole-file re-verification.

**Byte-level?** No. `[R-LIF-06]`'s obligations on recovery tools are unchanged under either
reading, and §21.6 records a non-violation in both. No file becomes emittable or rejectable
either way.

---

### register-03 — AMBIGUITY — §21.9, individuation of the first five limit rows

**Location.** §21.9, the paragraph after the guarantees table.

**Quotation.**

> Either way a file containing no instance of a kind does not exceed
> that row, whatever its declarations would derive. The first five rows
> range over declarations, which every file and every layer carries.

**The problem.** The paragraph's whole work is to say which of the eight guarantee rows can
be instance-free. It grants that to the last three, explicitly and twice — "A layer
addressing no tile (§11.2) therefore has no tile whose decoded size the table bounds" and
"The other two range over the user-metadata documents and compressed frames a file actually
contains, neither of which exists except as stored bytes" — and then denies it to the first
five, on the ground that their declarations are carried by "every file and every layer".

Three of those five are *per-layer* declarations: "rank d of a layer", "channels per layer,
C", and "addressed tiles per layer (entry_count)". A conforming file with **zero layers**
carries none of them. That file is not a corner the document leaves undecided — it is one
the document blesses in three places. §21.6:

> | The file contains zero layers | A conforming file: a directory carrying no layer record is a conforming generation whether or not it carries other records, an empty directory included | `[R-CNT-14]` (R-CNT-02) |

Appendix A's 128-byte minimal file is one, and §5.1's Example calls it "a valid, empty
file".

**Permitted readings.**

1. Distributive: file-level declarations are carried by every file, layer-level ones by
   every layer. Then the clause is true as stated, but it no longer supports the contrast
   the paragraph is drawing, because a zero-layer file has no layer and so no instance of
   rank, C or entry_count — exactly the situation the paragraph has just reserved for the
   last three rows.
2. Universal: every file carries an instance of each of the first five. Then it is
   falsified by the minimal conforming file of Appendix A.

**Which I picked and why.** Reading 1, because it is the only one a legal file does not
refute, and because the paragraph's own preceding sentence — "Either way a file containing
no instance of a kind does not exceed that row, whatever its declarations would derive" —
states the principle that settles the zero-layer case for the first three rows too. On
reading 1, the sentence's contrast is simply not exhaustive: five rows are declaration-
individuated, three of them still absent from a zero-layer file.

**What an implementer does wrong without it.** A reader author who takes reading 2 has no
account of what "rank ≤ 32" means for a layerless file and may reach for a default. Nothing
in §7.4 or §11.1 supplies one, because there is no layer record to read it from. The right
answer — no instance, therefore no exceedance, therefore `[R-CNF-03]`'s acceptance duty is
undisturbed — is the answer the paragraph gives the last three rows and withholds here.

**Byte-level?** No. Under both readings a conforming zero-layer file lies within every
guarantee (there is nothing to exceed), so `[R-CNF-03]`'s acceptance duty runs to it either
way and no reader may decline it on §21.9's ground. The set of files a conforming reader
must accept does not move.

---

### register-04 — AMBIGUITY — §21.1, "the row is the rule"

**Location.** §21.1, opening of the Instances paragraph.

**Quotation.**

> The **Instances** column enumerates what a conformance corpus builds
> for that row (§21.8): the row is the rule, and each instance is one
> file.

**The problem.** Twenty lines earlier the same subsection has settled the opposite:

> but each row *restates* its governing rule, and where a
> row and the rule it cites diverge, **the rule governs**.

And §24 `[R-VEC-02]` keeps row and rule distinct as two things a manifest entry must both
record: "the §21 register row it exercises together with that row's governing requirement
identifier … recording both ties the vector to the rule as well as to the row."

**Permitted readings.**

1. "The row is the rule" is corpus-building shorthand: for the purpose of §21.8's coverage
   claim, the row is the unit against which vectors are counted, and each instance names
   one file to build. This is consistent with everything around it.
2. "The row is the rule" is a statement of authority: what the row says is what the corpus
   is built to. This contradicts §21.1's own tie-break and `[R-VEC-01]`'s "where a vector's
   recorded expectation and this specification disagree, this specification governs and the
   vector is corrected."

**Which I picked and why.** Reading 1, because the clause sits inside a sentence whose
subject is what a corpus builds, because §21.1 has already ruled against reading 2 in
terms, and because `[R-VEC-01]` rules against it again from the other end.

**What an implementer does wrong without it.** A corpus author under reading 2, meeting a
row whose wording is narrower or broader than its cited requirement, builds the file the
row describes and records an expectation the specification does not support. `[R-VEC-01]`
then makes that vector wrong rather than the document wrong, so the error is recoverable —
but the sentence as written invites it, in the one paragraph a corpus author reads first.

**Byte-level?** No. Two implementations reading this sentence differently still accept and
reject the same files, because both §21.1 and `[R-VEC-01]` put the requirement above both
the row and the vector.

---

### register-05 — AMBIGUITY — §21.8 against §24's `[R-VEC-03]`

**Location.** §21.8 (`[R-ERR-02]`) and §24 (`[R-VEC-03]`).

**Quotations.**

§21.8:

> Every row of §21.2 through §21.5 — 120 conditions over 277
> instances — has at least one conformance vector (§24) whose expected
> outcome is that row's outcome, and one vector per instance.

§24:

> Coverage is the corpus's own obligation, inherited from
> `[R-ERR-02]`: every register row has at least one vector for each
> instance it names, and every sentinel, every boundary value, and every
> hard limit of `[R-ERR-05]` has one at its stated bound.

**The problem.** §21.8's final clause reads "one vector per instance"; §24 reads "at least
one vector for each instance". §24 declares itself to inherit from `[R-ERR-02]`, so the two
are meant to state the same obligation, and one of them carries an "at least" the other
drops.

**Permitted readings of §21.8.**

1. "and [at least] one vector per instance" — the "at least" from the first half of the
   sentence distributes across the "and". Then §21.8 and §24 agree.
2. "and exactly one vector per instance" — a cardinality constraint. Then a corpus carrying
   two vectors for one instance satisfies `[R-VEC-03]` and violates `[R-ERR-02]`, and
   §24's own further demand that "every sentinel, every boundary value, and every hard
   limit of `[R-ERR-05]` has one at its stated bound" becomes hard to satisfy without
   either doubling up on some instance or contriving coincidences.

**Which I picked and why.** Reading 1. §24 states the obligation it says it inherited, in
full and with the quantifier, and a coverage floor is what the surrounding text is about
throughout: "A row without a vector is a gap in the corpus, not a licence to skip the
check" (§21.8), "A missing vector is a gap in the corpus and never a licence to skip the
check it would have exercised" (§24). Nothing anywhere gives a reason to cap the corpus.

**What an implementer does wrong without it.** A corpus maintainer under reading 2 refuses
a second vector for an instance already covered — including the boundary-value and
hard-limit vectors `[R-VEC-03]` separately requires, where those coincide with an instance
already vectored. That subtracts coverage from a corpus whose stated purpose is coverage.

**Byte-level?** No. Both `[R-ERR-02]` and `[R-VEC-03]` bind the conformance corpus, not any
file a writer emits or a reader accepts, and `[R-VEC-01]` makes the corpus derivative:
"where a vector's recorded expectation and this specification disagree, this specification
governs and the vector is corrected."

---

## 13. Candidates I opened and closed

Recorded because a lane that finds little should be able to say what it did that would have
found something.

- **A row whose outcome disagrees with its rule.** The class the brief warns is the dominant
  over-claim. I walked all 120 and found none; §3 above records the walk. This is the single
  thing I most expected to find and it is not there.
- **`[R-ENC-06]` and `[R-ENC-01]` asymmetry in §21.7.** §21.7 names field widths as stating
  no condition a file can exhibit but not byte order, which is the exactly parallel case.
  Closed by §21.7's own disclaimer, "That is the whole of the test, and it decides any
  condition put to it without appeal to a list", and by F1 registering the one detectable
  byte-order condition under `[R-ENC-02]`.
- **§21.6's slack entry omitting the no-live-trailer case.** `[R-CNT-21]` distinguishes three
  cases (exact total, partial total, no total owed) and the entry mentions two. Closed
  because the entry's Condition cell is "Bytes the live state does not claim", which
  presupposes a live state; where §6.2's ordered validation rejects before a live trailer is
  established the entry's subject does not arise.
- **The user-metadata extent minimum (extent_length ≥ 5) missing from §21.9's hard limits.**
  Closed by "The hard limits it restates are a finding aid rather than an inventory — each is
  normative where the structure forcing it is defined."
- **The geometry floors (d ≥ 1, C ≥ 1, Tᵢ ≥ 1) missing from §21.9's hard limits.** Same
  sentence closes it.
- **§21.1's list of what the completeness clause does not reach omits §21.8.** "The
  subsections after §21.5 are not part of the register and carry no rows: neither this
  completeness clause nor the instance arithmetic below reaches §21.6's defined
  non-violations, §21.7's test for what no check detects, or §21.9's limits." §21.8 is after
  §21.5 and is not in the list. Closed: §21.8 carries no entries to reach — it *reports* the
  arithmetic rather than being reached by it — so its absence from the list is correct
  rather than an omission.
- **An experimental-range MU = 1 *sub-record* having no §21.6 table entry.** It is a
  conforming file whose layer a reader must refuse. Closed: §21.6's closing paragraph states
  it in prose ("the same type as a layer sub-record is reject-layer and never a ground to
  refuse the file (`[R-CNT-18]`)"), §21.1 says the subsections after §21.5 carry no rows and
  claims no completeness for them, and `[R-CNT-18]` resolves the apparent tension with
  `[R-CNF-03]`'s acceptance duty directly: "where the file is otherwise conforming a reader
  MUST NOT reject the file for it".
- **F1 and F6 listed under Appendix H's *verifier* checklist though their Detector cell reads
  *reader*.** Closed: `[R-CNT-04]` exempts a reader that would have to fetch the bytes and
  §2.3 exempts no verifier, which is what the checklist says in terms ("which `[R-CNT-04]`
  lets a reader not holding it resident defer or omit and §2.3 does not"), and F6's own
  Condition cell restates the exemption.
- **T14 as an unlisted strict specialization of T3.** Under codec 1 the stored bytes are the
  filtered image verbatim and the filter preserves length, so an entry length ≠ decoded size
  forces a decoded payload length ≠ decoded size. Closed: §21.1 says "the property decides
  any pair and this list is not offered as closed", and both rows are reader/tile use/
  reject-tile, so nothing turns on which is recorded.
- **R3 and R4 overlapping.** Closed by R3's own text — "where the encoding is 2 and what
  fails is one of the frame constraints R4 registers, R4 is the row, whether or not the bytes
  also fail to decode" — which is an express assignment, and by §21.1's "Rows that merely
  overlap, each reachable without the other, do not stand in it".
- **F30 and F32 overlapping** at a slot (0, N) with N > F − 64. Closed the same way: each is
  reachable without the other.
- **§19.1 step 4 citing only `[R-ENC-12]` for the layer-name check while L3's governing rule
  is `[R-ENC-11]`.** Closed by §19's preamble: "Those enumerations are not the complete
  inventory of what a reader detects at that tier: §21's register is … A row this section
  does not restate is due at its own tier all the same."
- **§21.1's "no two files could differ" as the reason a sum's fields are not instances.**
  Two files *can* differ in how a sum splits. Closed as imprecise gloss on a rule whose
  operative content ("One instance is one *distinguishable* file") is right and whose
  application to F3 and F25 is right; not worth a finding.
- **The `[R-CNT-06]` parenthetical asymmetry** — L46/L47 cite "(R-CNT-13)" for the governing-
  scope mapping while F25/F26 cite nothing, though both need the same §7.2 sentence. Closed
  as below the threshold: §21.1 makes parentheticals "the further rules the condition reads",
  which is a permission rather than an obligation to be exhaustive.
- **§18.2's "a document larger than that guarantee" antecedent.** Ambiguous between the
  8 MiB Window_Size row and the 16 MiB document row. Closed because both readings yield true
  statements and the next sentence disambiguates: "§21.9's user-metadata row bounds a
  document's decoded size; it does not relieve the frame carrying it of the `Window_Size`
  row."
- **Whether any register row rests on a SHOULD.** Checked all 49 distinct governing rules;
  none is SHOULD-only, so §2.4's "§21's register enumerates MUST-level conditions only"
  holds.
- **§21.1 carrying no requirement identifier of its own** although it states normative rules
  ("Its **completeness is normative**", "the rule governs"). Closed as consistent with the
  document's practice — §2.2, §3.1, §5.2's Notes and other structural prose likewise carry
  none, and `[R-CNF-01]` makes unlabelled text normative regardless of whether an identifier
  is attached.

## 14. Confidence

High on the tables. The 120 rows, their outcomes, scopes, detectors, detection points,
governing rules, instance cells and both totals were each checked against the rule they
cite and against each other, and I recomputed every number and checksum the document states
in or near §21. The register reproduces exactly and I found no divergence in it.

Medium on the surrounding prose, which is where all five findings sit, and where the density
of recent rewriting is highest. Four of the five are ambiguities a careful reader resolves
correctly by consulting a neighbouring sentence; the fifth (register-03) is a universal a
legal file falsifies. None moves a byte, and I say so for each rather than reaching.

I did not find a byte-level fork in §21. I want to be clear about what that claim rests on:
the strongest byte-level candidate in this charter would have been a register row that
contradicts its rule about a *verdict*, and §21.1 pre-decides that class ("the rule
governs"), so even a found divergence there would have died on §21.1. The place a fork
could still live is a rule whose §21 restatement is the *only* statement of some condition —
and I looked for that by deriving the register's completeness in both directions rather than
by reading the rows against the rules alone. Section 5 above is that work.
