# Round 18 — Register hunter — working transcript

**Charter:** audit §21, the error-handling register, against the rules it restates
and against itself.

**Access disclosure.** I opened exactly one file:
`/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, read end to end
(lines 1–4339, in five Read calls plus targeted re-reads of §6.4's tail, which my
first two chunk boundaries had skipped). I ran `grep`/`python3` against that file
only, and wrote three scratch scripts of my own (`count.py`, `ids.py`, `crc.py`,
`shuffle.py`) in the scratchpad. I did **not** open `docs/`, `PLAN.md`,
`AGENTS.md`, `README.md`, `OPEN-QUESTIONS.md`, `conformance/`,
`spec/registry.json`, or any git history; I ran no `git` command, no web search,
no web fetch, and did not list any directory to discover what else exists. I did
not read the round-18 output directory.

---

## 0. Method

The register is a table of 121 rows across four subsections, each row restating a
rule stated elsewhere. My plan was, in order:

1. Read §21 first and extract its governing rules (§21.1) mechanically.
2. Read the whole document, so that every "governing rule" cell could be checked
   against the actual rule text rather than against memory.
3. Recount the conditions and instances by script, applying §21.1's own
   arithmetic, and compare against every total stated.
4. Walk every row → rule → row, comparing wording, outcome, scope and detector.
5. Sweep both completeness directions: MUST-level byte conditions without a row,
   and rows registering non-violations.
6. Resolve every cross-reference to a row label from anywhere in the document.
7. Cross-check §21.9's limits against every other statement of a limit.
8. Actually build a file and walk the register over it, noting where I guessed.

I read the five sections the brief flags (§20.4, §20.5, §21.7, §23.1, Appendix G)
first-pass with the rest, and returned to §21.7 in depth because it is inside my
charter. §20.4 and §20.5 I checked only where they touch the register (§2.4's
`preserve-verbatim` row cites §20.4's table; §20.5's regeneration passage rests on
§15.3's structural entries, which are register rows T6–T12).

---

## 1. The counting

§21.1 fixes the arithmetic:

> Instances within a cell are separated by semicolons, and a cell reading — is one
> instance; the count is therefore mechanical once the cell is written.

So I parsed the four tables mechanically: any line matching `^\|\s*[FLTR]\d+\s*\|`,
split on `|`, six cells expected, instance count = number of non-empty
semicolon-separated fragments, with a bare `—` counting 1.

Per-subsection row counts:

| Subsection | Rows found | Stated |
|---|---|---|
| §21.2 file scope | F1–F36 = 36 | "36 conditions" ✓ |
| §21.3 layer scope | L1–L49 = 49 | "49 conditions" ✓ |
| §21.4 tile scope | T1–T26 = 26 | "26 conditions" ✓ |
| §21.5 ignored records | R1–R10 = 10 | "10 conditions" ✓ |
| **Total** | **121** | §21.8: "121 conditions" ✓ |

Per-subsection instance sums: F = 58, L = 116, T = 55, R = 44. Total **273**.
§21.8 states "121 conditions over 273 instances" — reproduces exactly, including
the multi-count cells (R4 = 12, L2 = 9, L1 = 8, R5 = 8, T3/T14/T22 = 6 each,
R7 = 6, F2 = 6, F33 = 5).

No per-subsection instance total is stated anywhere, so there is nothing else to
reconcile. Appendix B's "Reader minimum guarantees" row restates §21.9's eight
table rows and matches all eight.

I then checked the *rules* §21.1 gives for how a cell is written, row by row,
because the count reproducing is not the same as the cells being right.

- **Magnitude comparisons enumerate two directions.** F17 (2), L21 (2 layouts × 2
  directions = 4), L22 (2 directions + 2 stated alternatives = 4), L30 (2),
  T3 (3 layouts × 2 = 6), T14 (6), T22 (6), F23/L12 (`inline_length` is a byte
  count and "is not 1" is a magnitude test → 2 each). All consistent.
- **One-direction comparisons enumerate one.** F5 ("below"), F9 ("less than"),
  F16, F22/L11 ("less than 5"), L44 ("exceeds", × 3 layout formulas), T21
  ("larger than", × 3 layouts). Consistent.
- **No magnitude ordering → no direction.** F8, F14, F15, F20, L37, L38, T1
  (checksum/constant comparisons) all 1. Consistent.
- **Nonzero value tests are not comparisons.** L20, L27, L28, T6 all 1.
  Consistent.
- **Layout-varying derived quantities enumerate the formulas.** L44 (3), T3 (6),
  T14 (6), T21 (3), T22 (6), T26 (3), T4 (4 content forms). Consistent.
- **Enumerator value-set rows enumerate the ranges the defining section names,
  not directions.** L31 (0 / 2–0x7F / ≥0x80 = 3), L33 (0 / 2–3 / 4–0x7FFF /
  ≥0x8000 = 4, matching §11.4's four bands), L34 (0 / 14–19 / 20–0x7FFF /
  ≥0x8000 = 4, matching §12.2), L36 (0 / 3–255 = 2, and channel layout correctly
  has no experimental band per §10.2), L43 (3), L45 (3), R1 (2 bands × 2
  containers = 4, experimental correctly excluded as a non-violation). All match
  their defining sections' band structure exactly.
- **A single predicate over several fields is one instance.** F10, T12 — both `—`.
  Consistent with "no two files could differ".
- **Containers multiply.** F30 (1 container, 2 alternatives = 2) against L15
  (2 containers × 2 alternatives = 4); F31 (1) against L16 (2); F32 (1) against
  L17 (2). Symmetric and correct.

One cell does not obey §21.1's own instance rule: **R7**, whose Instances cell
enumerates "leading U+FEFF" although the row's Condition cell states only two
alternatives. Written up as **register-02** below.

I also checked whether "(overrun or truncation)" in L23 should double the count.
It should not: §21.1 says "One instance is one *distinguishable* file", and a
region that overruns the payload is the same file as one the payload truncates.
L23's 4 = four declared regions. Correct.

---

## 2. Arithmetic and byte layouts I recomputed

Since the register's tile rows all turn on decoded sizes and CRCs, I recomputed
everything the document asserts numerically, from scratch (CRC-32C implemented
from §4.5's parameters — Castagnoli reflected, init/final `0xFFFFFFFF`):

- §4.5 check vector: `CRC32C("123456789")` = `0xE3069283` ✓; `CRC32C(∅)` =
  `0x00000000` ✓.
- Appendix A's trailer: I assembled bytes `[0,60)` from the field table and got
  `0xE00938D2`, stored `D2 38 09 E0` ✓ — matches the hex dump at `[124,128)`.
- §7.4's example: 80 bytes of four sentinel entries → segment CRC `0x80A34955`,
  stored `55 49 A3 80` ✓; `crc_of_crc_array` over that 4-byte array =
  `0xC4EE982E` ✓.
- §15.4's constant: CRC-32C over 2¹⁶ sentinel entries (1,310,720 bytes) =
  `0xEECB3BB2` ✓.
- §7.4's payload layout: name 4 + nine scalars 34 + dimension entry 18 + channel
  entry 12 + trailing 13 = 81 ✓, offsets in the annotated dump all land where the
  field order puts them; extent slot length 4×20 + ⌈4/2¹⁶⌉×4 = 84 ✓ (L22's
  formula).
- §15.4's worked index: entry_count 1,000,000 → 16 segments (15 full + 16,960),
  64-byte CRC array, region 20,000,064 bytes, entry 999,999 at segment-relative
  20×16,959 = 339,180, segment 15 at [19,660,800, 20,000,000) ✓, full segment
  1.25 MiB ✓.
- §11.4's ordinals: (300,700) → tile (1,2) → s = 10, in-tile (44,188) → 11,452;
  planar channel 2 → 2·32 + 10 = 74; entry at [1,480, 1,500) ✓.
- §14.2/§14.3/§14.5/§17.3 worked examples: Q = 3 → 18 bytes, ordinal 5 at [15,18);
  planar `b` 12 bytes, ordinal 5 at 10–11; Q = 5 → 30 bytes; packed plane `55 01`
  and `55 FD`; edge tile 32 bytes with values 1–15 = `CD AB`; the byte-shuffle
  example `00 00 00 00 00 00 80 00 40 3F 40 40`. All reproduce.
- §21.9's Note: segment-CRC array at 2³² entries = 2¹⁶ segments × 4 = 256 KiB ✓,
  at 2³⁶ = 4 MiB ✓; 65,536 layers × ~200 B ≈ 12.5 MiB ✓; 2³² entries × 20 B ≈
  86 GB, so §24's "tens of gigabytes" for the unconstructible vector ✓.

Nothing in the numeric surface is wrong.

---

## 3. Row-versus-rule agreement

I walked all 121 rows against the requirement each cites. Method: for each row,
find the cited requirement's actual text, and compare four things — wording,
outcome class (from the subsection header), scope, and detector.

### 3.1 Detector column

This is the column with the most teeth, because §2.3's `[R-CNF-04]` makes the
**register**, not the rule, the authority for reader obligations:

> A reader MUST detect every violation the error register (§21) assigns to the
> reader as its detector

while §21.1 says the rule governs on divergence. If a row assigned `reader` where
its rule assigns `verifier` (or vice versa), those two clauses would point in
opposite directions and two readers could legitimately differ on whether a file
is refused. So I checked every one.

**Verifier rows** — F7, F25, F26, F27, F28, F33, F36, L18, L25, L40, L41, L42,
L46, L47, L48, L49, T2, T4, T5, T26. Each cited rule explicitly assigns detection
to a verifier and, in almost every case, explicitly relieves the reader:

- `[R-CNT-05]` — "A verifier MUST treat a structure in that gap as a validity
  error at file scope … (readers check neither …)" → F7 ✓
- `[R-CNT-12]` — "their detection is a verifier's: a verifier MUST treat a nonzero
  reserved flag bit or the MU = 1 with PE = 0 combination as a validity error at
  the record's governing scope" → F25, F26, L46, L47 ✓
- `[R-CNT-13]` — "(readers are not obligated to detect overlap …)" → F33, L18 ✓
- `[R-CNT-15]` — "a verifier MUST treat a reserved-range record type as a validity
  error" → F36, L25 ✓
- `[R-CNT-22]` — "a verifier MUST treat the mismatch as a validity error" → F28,
  L49 ✓
- `[R-MTA-05]` — "a verifier MUST report it, and readers process the document
  unchanged" → F27, L48 ✓
- `[R-SLB-01]`/`[R-SLB-03]` — "A verifier MUST check the invariant(s) …; readers
  are not obligated to" → L40, L41, L42 ✓
- `[R-SER-05]` — "a verifier MUST check it" → T4, T5 ✓
- `[R-SER-08]` — "its assigned detector is the verifier" → T2 ✓
- `[R-COD-10]` — "a verifier detects it as a validity error at tile scope" → T26 ✓

**Reader rows** — every one of the remaining 101 traces to an explicit reader
MUST, either in the cited rule itself (`[R-ENC-02/03/04/11/12/15]`,
`[R-CNT-04/06/07/08/11/12/14/15/18/20/23/25/27]`, `[R-GEO-01/05]`, `[R-TYP-03/07]`,
`[R-SER-06/07]`, `[R-IDX-03/04]`, `[R-SLB-01]`, `[R-COD-03/04/06/07/08/09]`,
`[R-MTA-03/04/09]`) or, for the four "cause" rows whose own rules are stated
declaratively without a keyword, in the rule that performs the detection and which
the row itself names:

- T13 (`[R-COD-02]`) — "the check that detects it is T25's" → `[R-COD-08]`'s
  reader MUST ✓
- T15, T16 (`[R-COD-05]`) — "T24's or T25's" / "T24's" ✓
- T23 (`[R-COD-07]`) — "T25's" ✓ (I checked this is decodable: `04 22 4D 18` read
  as a raw LZ4 block is token `0x04` = 0 literals, match length field 4, then a
  2-byte offset `0x4D22` = 19,746, which reaches back past zero produced output —
  exactly T25's third instance, "lz4 match offset 0 or match reaching past
  produced output").

So there is **no** detector divergence anywhere, and the latent tension between
`[R-CNF-04]` and §21.1 is unexercised. I note it here as a hazard for future
edits rather than as a finding: if any row's Detector cell ever came to disagree
with its rule, the document would give two contradictory answers about which one
a reader follows.

### 3.2 Outcome and scope

Each subsection header fixes one outcome. I checked every row's rule assigns that
scope:

- §21.2 → reject-file. All 36 trace to a file-scope assignment. F25/F26/F28 and
  F30–F32 rest on §7.2's governing-scope rule ("the layer for a layer record and
  for sub-records, the file for other top-level records"), and the register
  correctly restricts them to "non-layer top-level record" so that layer records
  and sub-records fall to L46/L47/L49 and L15–L17. F21/F22/F23 rest on §7.1's
  "a validity error at its containing scope" and §18.1's clarification that the
  quarantine "covers the document only". F27 is the only one worth a second look:
  an unsorted metadata document is *not* an unreadability, so `[R-MTA-02]`'s
  "the outcome of every failure to read its document is ignore-record" does not
  reach it, and the record's owning scope (file, when top-level) governs — file
  scope is right.
- §21.3 → reject-layer. All 49 check out, including the three detected at *open*
  (L3, L5, L6): §7.4 puts the owning scope of a layer record's inline payload at
  the layer, and §19.1 step 4 requires the name parse at open, so open/reject-layer
  is the correct pair. L37/L38 are layer scope though detected at tile use —
  §19.2 says so explicitly ("index-chain failures take layer scope … although
  their detection point is tile use").
- §21.4 → reject-tile. All 26. T6–T12 map onto §15.3's table exactly, including
  the split of §15.3's sixth row ("offset + length overflows, or offset + length
  > F − 64") into T12 and T9, which is the right split: T12 covers the case where
  the sum is not computable in domain, T9 the case where it is and exceeds.
- §21.5 → ignore-record. All 10, under `[R-CNT-25]`'s express assignment, which
  §21.1 flags as the one standing exception to the scope-determines-outcome rule.

The outcome vocabulary is complete and every defined value is reachable: all four
reader outcomes of `[R-CNF-07]` head a subsection, and `preserve-verbatim` —
which §2.4 defines as an updater obligation rather than a reader outcome — is
reachable through §20.4's table. I checked §2.4's claim about where:

> §20.4's table states the cases: its MU = 1 and MU = 0 / PE = 1 rows.

§20.4's table has exactly three rows — MU = 1 ("Retain byte-identical"),
MU = 0/PE = 1 ("Retain byte-identical, extent content unmodified"), and
MU = 0/PE = 0 ("Retain byte-identical, or drop it"). The first two are the
preserve-verbatim cases; the citation is exact.

### 3.3 Wording

Every row's Condition wording restates its rule accurately, with these
observations:

- **F21**'s gloss "placing its document inline" is loose — an extent slot of
  (0, 0) means *no extent* (§7.2), so the document is absent, not inline. The
  condition itself (slot = (0,0) on a top-level user-metadata record) is exactly
  §7.1's, so nothing turns on the gloss. Not reported.
- **F5**'s gloss lists the pre-trailer pad among what "cannot all fit", but a
  conforming 128-byte file need not have one (`dir_offset` 16, `dir_length` 48
  ends the directory exactly at F − 64). `[R-CNT-27]`'s own reasoning does not
  mention the pad. Cosmetic; not reported.
- **L41**'s "the previous stored tile's offset plus that tile's length" uses a
  demonstrative where §16.2 uses "its". Both mean the previous tile's length —
  head-to-tail packing — and §16.2's "contiguous and packed in ordinal order"
  settles it. Not reported.
- **R7**'s Condition omits an alternative its own Instances cell carries.
  **Reported as register-02.**
- **T26**'s "the check that detects it is T2's or T4's" contradicts §21.7's
  "T2, T4 or T5, exactly as a mis-strided filter is". **Reported as register-01**
  — and T26 is the one that is right; see §6 below for the proof.

### 3.4 Format conventions

Two rows put a section reference where §21.1 says the parenthetical carries
"further rules … cited without brackets": L26's `` `[R-CNT-18]` (§7.3 registry
table) `` and L31's `` `[R-CNT-23]` (§15.1) ``. The governing identifier — the
one §24's `[R-VEC-02]` makes a vector record — is the first-named one in both
cases, so nothing downstream breaks. Noted, not reported.

---

## 4. Completeness, both directions

### 4.1 Rules without a row

I extracted all 161 requirement identifiers and partitioned them into
governing-in-a-row (37), cited-parenthetically (24), and absent (100), then went
through all 100 absent ones asking whether each names a *detectable
file-conformance violation*.

Every one resolves. The classes:

- **Not file predicates at all** — conformance-class definitions (`[R-CNF-01/02/03/
  06/07/08/09/10/11/12]`), reader algorithms (`[R-RDR-01..04]`), writer/updater
  conduct (`[R-WRT-01..09]`), verifier procedure (`[R-LIF-08]`), tool behavior
  (`[R-LIF-05/06/07]`), security/privacy advice (`[R-SEC-*]`, `[R-PRV-*]`),
  corpus rules (`[R-VEC-*]`), definitions (`[R-MDL-01/02]`, `[R-ENC-08/16]`,
  `[R-TYP-01/02/05]`, `[R-IDX-01]`, `[R-EXT-01/02/04/05]`, `[R-COD-01]`,
  `[R-MTA-01]`).
- **SHOULDs**, which §2.4 explicitly excludes ("§21's register enumerates
  MUST-level conditions only") — `[R-CNT-03]` (zero the gaps), `[R-CNT-09]`
  (65,536-byte discovery window), `[R-CNT-26]` (lowest version_minor),
  `[R-ENC-14]` (NFC), `[R-LIF-07]` (checkpoint commits), `[R-TYP-10]` (zero fill
  default), `[R-MTA-07/08]` (key placement and `tarn.stats`).
- **Defined non-violations already in §21.6** — `[R-GEO-02]`, `[R-IDX-02]`,
  `[R-SER-09]`, `[R-TYP-08]`, `[R-MTA-06]`, `[R-MTA-07]`, `[R-MTA-10]`,
  `[R-CNT-08]`'s ignore lane, `[R-CNT-07]`'s minor.
- **Expressly not-a-violation writer obligations** — §6.3's `flags = 0` against a
  set ignore-lane bit, and §6.2's over-long pre-trailer gap. §2.3's `[R-CNF-02]`
  names exactly these two, and I could find no third: `[R-EXT-03]` and
  `[R-MTA-06]` are handled by the separate *conduct* clause ("where a value is
  published, or which registry version a writer targets (§10.3, §18.3)"), and
  every other writer MUST I could find either has a row or is in §21.7.
- **Accounted for in §21.7** — `[R-LIF-01]`, `[R-LIF-03]`, `[R-GEO-06]`,
  `[R-SER-01]`, `[R-CNT-13]`'s no-embedded-offsets clause, `[R-CNT-18]`'s nesting
  prohibition, §20.3 step 4's declaration bar, `[R-ENC-06]`'s field widths.
- **Detection is another rule's, so no row of its own, and the document says so
  where it arises** — `[R-SLB-04]` (§16.2's Note: "a stale declaration carries no
  register row of its own"), `[R-LIF-04]`'s residue (§9.5's Note: "Residue past a
  completed commit carries no register row of its own"), `[R-CNT-02]`'s
  "belongs to no class" half (§5.2's Note: "a register row for it would be a row
  no file could exhibit").

The two I had to think hardest about:

- **`[R-ENC-01]`/`[R-ENC-02]`'s "writers MUST NOT emit big-endian values."** Only
  the signature case is detectable, and that is F1. A big-endian `dir_offset` is
  just a different `dir_offset`; whether it trips F10 or nothing at all depends on
  the value. §21.7's first paragraph covers this under "or simply wrong data",
  and no separate witness exists. No row is owed.
- **`[R-IDX-01]`'s "entry order is disk-ordinal order."** No witness — an index
  written in the wrong order is structurally valid. §21.7 names `[R-GEO-06]`,
  which is where the disk ordinal is defined ("The **disk tile ordinal**, which
  orders tile-index entries (§15)"), so the class is accounted for.

I also swept all `MUST NOT emit` / `MUST emit` / `MUST equal` / `MUST parse` /
`MUST lie` / `MUST place` / `MUST serialize` occurrences directly (23 sites) and
mapped each to its row(s). No gap.

### 4.2 Rows registering a non-violation

Every row's condition is genuinely a violation under its rule. The ones worth
naming because they are *not* reader-visible:

- F7, F25, F26, F27, F28, F33, F36, L18, L25, L40–L42, L46–L49, T2, T4, T5, T26
  are violations that leave conforming reader behavior unchanged. Each rule says
  so in terms (`[R-CNT-12]`: "Both writer violations make the file nonconforming
  (`[R-CNF-05]`) while leaving conforming behavior unchanged"; `[R-CNT-22]`:
  "A stored-flag mismatch on a registered type makes the file nonconforming";
  `[R-MTA-05]`: "the file is nonconforming"; `[R-SER-08]`: "Any other byte makes
  the file nonconforming").
- R1's registration of encoding 0 and the reserved band as violations, while the
  experimental band is not, is exactly what `[R-EXT-03]`, `[R-MTA-03]` and
  `[R-MTA-10]` say: "what `[R-MTA-10]` withdraws is the document's content rules,
  never the encoding byte's own value set".
- T13, T15, T16, T23, T26 record causes rather than procedures, which §21.1
  contemplates and each row states.

§21.6's fourteen entries all check out against their rules, and the two paragraphs
that follow — the ex-non-violations (`[R-MTA-05]`, `[R-CNT-22]`) and the two
capability refusals — are both accurate and both cross-referenced correctly (see
§5).

---

## 5. Every cross-reference to a row

I extracted every occurrence of a bare row label outside the leading cell of a
register row (a regex that also caught false positives like `0x3F80`, which I
discarded by hand). Twenty-eight citation sites. Each resolves:

| Site | Cites | Verdict |
|---|---|---|
| §5.2 (line 646) | L18, L40–L42 | ✓ all four are verifier-detected layer-scope rows the coverage walk itself establishes |
| §9.6 (1297) | F8, F17 | ✓ trailer magic and transport-size mismatch, the two gates a torn tail fails |
| §17.2 Note (2265) | T24 | ✓ "bytes remain in the stored extent after the stream … ends" |
| §20.3 step 4 (2983) | L44 | ✓ codec-4 decoded-size cap |
| §21.1 (3289–90) | F1⊂F6, F1⊂F8, F35⊂F36, L24⊂L25 | ✓ all four containments hold, and the narrower row's detector/tier is the operative one in each pair |
| §21.1 (3308, 3310) | T24, T15, T25 | ✓ T24's cell is literally "any codec"; T15 (zlib/gzip) and T25 (three malformed-stream shapes) do enumerate materially different family members |
| §21.1 (3338) | F27, L48 | ✓ both are `[R-MTA-05]` rows whose readers "process the document unchanged" |
| §21.2 preamble (3352–55) | F8, F1, F14, F6, F18 | ✓ "Four rows" = F8, F1, F14, F6; and §6.2 does place magic and CRC ahead of the version gate, `[R-CNT-04]` does place the front block "before other processing", and F18 is correctly excluded as outside the premise |
| F33 (3393) | F9/F10, F31/F32, L16/L17, T8/T9 | ✓ all eight are the front-block and trailer bounds rows at their own tiers |
| T2 (3463) | T4 | ✓ T4's instances include "interleaved bool fill byte" |
| T13/T15/T16/T23 | T25, T24 | ✓ |
| T26 (3487) | T2, T4 | ✓ — and this is the correct pair; §21.7's competing claim is register-01 |
| §21.5 preamble (3501), R3 (3513) | R1 | ✓ |
| §21.6 (3533) | F36, L25 | ✓ correct: for an MU = 0 reserved-range type the violation rows are the verifier ones, not F35/L24 |
| §21.6 (3569–71) | F18, F35, F36, L24, L25 | ✓ |
| §21.7 (3597) | T2, T4, T5 | ✓ for a *mis-ordered image*; ✗ for the "exactly as a mis-strided filter is" analogy — register-01 |
| §21.7 (3607–12) | T3, T14, T15, T17, T23, T25 | ✓ each row does test what the sentence says it tests |
| App. H (4323, 4325, 4326, 4335) | F1, F6, F7, F36, L25, R1 | ✓ |

I also checked the citation-by-description sites, where a section names a row's
content without its label: §9.5's Note ("the magic, the CRC, or
committed_file_length against the transport size" = F8, F14, F17 ✓), §16.2's Note
("a run whose tiles are unpacked or whose first stored tile is misaligned, which
§21.3 registers" = L41, L42 ✓), §7.4's closing Note ("whose appearance as a
sub-record §21.3 registers in its own right" = L26 ✓).

One outbound reference I chased down because it looked undefined: `[R-CNT-10]` is
cited three times and I had skipped lines 850–864 between two chunk reads. It is
defined at the end of §6.4 (the transport-authoritative-size rule). It is reader
conduct, so it correctly has no row of its own and appears only as a further-rule
citation in F17.

---

## 6. §21.7 in depth

Two problems, one of which resolves in the register's favour.

### 6.1 The mis-strided filter and T5

§21.7 says:

> a mis-ordered image is then witnessed by T2, T4 or T5, exactly as a mis-strided
> filter is

T26 says:

> the check that detects it is T2's or T4's

I set out to decide which is right, expecting the row to be the loose one, and got
the opposite answer. The byte-shuffle of `[R-COD-10]` places byte *i* of group *j*
at offset *i·n + j*, with *n = L/s*. The last offset *L − 1* forces *i = s − 1*,
*j = n − 1*, whose source position is *j·s + i = (n−1)s + (s−1) = ns − 1 = L − 1*.
**The final byte is a fixed point of the shuffle at every stride that divides L.**
I verified this exhaustively for every (L, s) with L ≤ 400 and s | L: zero
violations of "offset 0 and offset L − 1 are fixed".

Pad bits live in the final byte of a packed planar bool plane and nowhere else
(§14.3: "The final byte's high bits beyond the last value (bit positions P mod 8
through 7, when P mod 8 ≠ 0) are the tile's **pad bits**"). A mis-strided writer's
image passes through the reader's inverse at the *mandated* stride — 1 for a
packed bool plane, i.e. the identity — so the reader's decoded image is the
writer's filtered image, whose last byte is the writer's correct last byte. I
simulated it (P = 204, L = 26, writer stride 2, reader stride 1): interior bytes
scramble, the pad byte survives untouched. So T5 **cannot** witness a mis-strided
filter, and T26's "T2's or T4's" is exact.

T5 *is* reachable for a mis-ordered image, which is what §21.7's clause is
primarily about — swap two channels' planar planes whose fill bits differ and the
plane's pad bits are the other channel's fill bit, violating `[R-SER-05]`'s
"Every pad bit (§14.3) MUST carry the plane's channel's fill bit". The defect is
the "exactly as" analogy, which extends the three-row disjunction to a case where
only two rows can fire. **register-01.**

### 6.2 The "only … and" conjunction

> §20.3 step 4's bar on a declaration change is witnessed only where the affected
> tiles remain stored *and* the change reaches a byte §14 structurally
> constrains — a padding position, a pad bit, or a boolean byte — where §21.4's
> content rows fire; a change that reaches the decoded size instead is witnessed
> by T3 or T14 …

The italicised *and* reads as a second necessary condition, and the clauses that
follow assert witnesses in cases that do not satisfy it — a decoded-size change is
not "a byte §14 structurally constrains", and neither is a codec change. Under
that reading the sentence contradicts itself. Under the alternative reading —
"only where the tiles remain stored", followed by a case analysis of which rows
fire in which sub-case — it is coherent, and that is the reading I take, because
T3, T14, T15, T17, T23 and T25 are real rows a reader MUST apply regardless of
what §21.7 says about them. **register-03.**

I checked §21.7's account of §20.3 step 4 against step 4's actual four-head list
(padding positions and their content; decoded size; sample byte offsets; codec and
filter). §21.7 covers heads 1, 2 and 4-minus-filter explicitly; head 3 (sample
byte offsets) and the filter half of head 4 fall under the content-row clause,
correctly — a filter change alters no length and leaves the stored bytes parsing
as the same codec, so only T2/T4/T5 can see it. And the tense agrees: §20.3's bar
quantifies over tiles stored "in the generation this commit supersedes", while
§21.7 says the bar is unwitnessed where the commit "supersedes every tile it would
have damaged", which is §20.3's own statement ("§21.7 records the consequence —
that this is precisely where the bar has no witness, the live state being clean").

Everything else in §21.7 checks: `[R-ENC-06]`'s "not a state a file can be in" is
right (a structure written at another width simply yields different values at the
fixed widths, caught by the rows for those fields); `[R-CNT-18]`'s nesting
prohibition really is undetectable except through L26, per §7.4's closing Note;
`[R-CNT-13]`'s MU = 0 no-embedded-offsets clause really is opaque.

---

## 7. Limits (§21.9) against every other statement of a limit

**Minimum guarantees, table → rest of document.** All eight rows are restated
identically in Appendix B. Cross-references: §17.2's "§21.9's 8 MiB `Window_Size`
guarantee" ✓; §18.2's Note "The 16 MiB figure is a §21.9 minimum guarantee" ✓;
§2.3's and §2.5's "the minimum guarantees of §21's limits table" ✓; §24's
"§21.9's minimum guarantees are exercised where a vector at the bound is
constructible" ✓; §1's "§21.9's tile-count guarantee" ✓. No divergence.

**Hard limits, §21.9 → defining sections.** Nine restated; each matches its
definition — name ≤ 255 (§4.6), metadata key ≤ 255 (§18.2's fourth bullet),
rank ≤ 255 and C ≤ 65,535 (§7.4's `u8`/`u16`), lz4 cap `0x7E000000` (§17.2),
value domain 2⁶³ − 1 (§4.2), A a power of two in 512…2⁶² (§16.1 and §7.4's table),
A_slab a power of two in 1…2⁶² (§7.4's table; §16.2 states only the "≥ 1" half,
which does not conflict), S in 1…2⁶³ − 1 (§7.4's table), directory ≥ 4 bytes at
offset ≥ 16 (§6.2), file ≥ 128 bytes (§5.1). The closing claim "Two do not
[follow from a field's width, an external format, or the value domain]" is
correct: I checked each of the nine, and only the 512 floor on A and the 255-byte
metadata-key cap are chosen numbers.

**Defining sections → §21.9.** The one hard limit stated elsewhere and absent
here is §7.1's `extent_length ≥ 5` for a user-metadata extent (Appendix B lists
it; §21.9 does not). That is not a defect, because §21.9 disclaims inventory
status in terms: "The hard limits it restates are a finding aid rather than an
inventory — each is normative where the structure forcing it is defined." Same
for the 24-byte record header, the 20-byte index entry, the 2¹⁶-entry segment, and
§6.4's 65,536-byte discovery window (a SHOULD).

**Reverse direction — a limit claimed here that its section states differently.**
None found.

`[R-ERR-04]`'s scoping ("at the whole file, or at the narrowest scope whose
declarations exceed what it can serve, a layer or a tile") composes correctly with
§18.2's Note, which sends a metadata-document decline to the whole file "a
document having no declared size and so no narrower scope whose declarations that
rule can measure", and with §2.3's list of cannot-establish grounds. And
`[R-ERR-04]`'s exclusion — "the two capability refusals §21.6 names, a foreign
format major and an unimplemented MU = 1 type, are not this ground" — matches
§21.6's closing paragraph exactly, which names exactly those two.

All the modal keywords in §21.9 are ALL-CAPS on both halves of every rule
(`[R-ERR-03]`'s "MUST accept … MAY rely"; `[R-ERR-04]`'s "MAY decline … MUST be
reported"), so the casing asymmetry the brief warns about does not arise here. I
checked the same for `[R-SER-08]`, `[R-CNT-04]`, `[R-CNT-05]`, `[R-CNT-08]`,
`[R-MTA-09]` and `[R-COD-06]` — the rules with a permission and a restriction in
one breath — and all are consistently capitalised.

---

## 8. Building the thing

I walked the whole register over two files I laid out by hand.

**File A — one interleaved float32 layer, four addressed tiles, one stored.**
Geometry from §7.4's example (rank 1, E = 100, T = 32, one float32 channel `temp`,
fill quiet NaN, codec 1, filter 1). P = 32, Q = 4, decoded size 128.

```
[0,16)     front signature block
[16,144)   stored tile, disk ordinal 0, length 128 (codec 1 → length = decoded size)
[144,228)  tile-index region: 4 × 20 = 80 entry bytes + 4 CRC bytes = 84
[228,337)  directory: 24-byte record header + 81-byte inline payload + 4-byte CRC
[337,384)  pre-trailer pad, 47 bytes of slack
[384,448)  trailer.  F = 448, 448 mod 64 = 0
```

`dir_offset` 228 ≥ 16 ✓, `dir_length` 109 ≥ 4 ✓, 228 + 109 = 337 ≤ F − 64 = 384 ✓.
Coverage: 16 + 128 + 84 + 109 + 64 = 401 claimed, F = 448, slack = 47 ✓ — which is
the number `[R-CNT-21]` obliges a verifier to report.

Walking §21.2: F1–F36 all pass or are vacuous (F21–F23, F25–F28, F30–F32 and
F34–F36 are vacuous because the only top-level record is a layer record).
§21.3: L21 (entry_count 4 = ⌈100/32⌉ = N ✓), L22 (84 = 4·20 + ⌈4/2¹⁶⌉·4 ✓),
L23 (81 bytes accounted for exactly, no residue → empty sub-record sequence ✓),
L27–L36, L39, L43–L45 all pass; L18, L25, L40–L42, L46–L49 vacuous or pass.
§21.4: entry 0 non-sentinel with length = decoded size (T14 ✓), entries 1–3
sentinel `FF ×16 00 ×4` (T6/T7 ✓). Tile 3 covers coordinates 96–127, of which
100–127 are padding — but it is unstored, so T4 is vacuous for it; had I stored
it, its bytes 16–127 would each have to be `00 00 C0 7F`.

**File B — planar, mixed bool and numeric.** rank 1, E = 20, T = 8, layout 2,
C = 2 (`m` bool fill 0x01, `v` uint16 fill 0xABCD). G = 3, N = 3, P = 8,
entry_count = C·N = 6. Disk ordinals 0–2 carry `m`, 3–5 carry `v`. Decoded sizes
differ per channel: ⌈8/8⌉ = 1 byte for `m`'s planes, 8·2 = 16 for `v`'s. P mod 8 = 0
so there are no pad bits (T5 vacuous), and tile 2/5 cover coordinates 16–23 with
20–23 padding — `m`'s plane 2 must carry fill bit 1 in bits 4–7, `v`'s plane 5 must
carry `CD AB` at bytes 8–15. T3, T14, T21, T22 and L44 all have to be evaluated
per channel, which is exactly why those cells enumerate three layout formulas.

**Where I had to guess: nowhere structural.** The four places I stopped and
re-read, and what settled each:

1. *Does the segment CRC of a 4-entry index cover only 80 bytes?* §15.4: "the
   final partial segment's CRC covers only its actual bytes", and `[R-IDX-05]`:
   "a partial segment's CRC MUST be computed". Settled.
2. *Is the register's Detected cell a deadline or a fixed point?* §19.2 makes it a
   deadline ("no later than the reader's first reliance"; "A reader MAY detect any
   violation earlier"). This matters for L23, whose "leading fixed fields
   (name … C)" instance is forced to open by §19.1 step 4 — a reader that cannot
   obtain a name field within `inline_length` has to decide that at open in order
   to build the namespace, even though L23's cell says layer access. Detecting
   earlier is licensed and the outcome (reject-layer) is the same on both paths,
   so there is no fork; I record it as a place a careful implementer will pause.
3. *Does §19.1's step-4 enumeration bound what a reader checks at open?* No —
   §19's preamble is explicit: "Those enumerations are not the complete inventory
   of what a reader detects at that tier: §21's register is". This is what makes
   R1's "open (top-level)" tier legitimate even though §19.1 step 4 lists the
   user-metadata *framing* checks without the encoding byte's value.
4. *Which of F21/F22/F23 versus R1 governs a malformed user-metadata record?*
   §18.1 draws the line: "The quarantine covers the document only: a malformed
   extent slot on such a record, (0, 0) included, is a validity error at the
   record's containing scope … because that failure precedes the document."
   Framing → scope (F21/F22/F23, L10/L11/L12); encoding byte and beyond →
   ignore-record (R1–R10). Clean.

---

## 9. Findings

### register-01 — CONTRADICTION — §21.7 and §21.4 T26 disagree on whether T5 can witness a mis-strided filter

**Location:** §21.7 `[R-ERR-01]`; §21.4 row T26 (`[R-COD-10]`).

§21.7 says:

> the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a
> structurally valid tile whatever values it carries, except where §14 constrains
> a byte's content — a padding position, a pad bit, or an interleaved boolean —
> and a mis-ordered image is then witnessed by T2, T4 or T5, exactly as a
> mis-strided filter is

T26's Condition cell says:

> Filter 2 applied at a stride other than the mandated one, where the resulting
> image breaks §14.5's padding content or `[R-SER-08]`'s bool bytes (a wrong
> stride with no such structural constraint is undetectable, §21.7); the check
> that detects it is T2's or T4's, and this row records the cause rather than a
> procedure of its own

The "exactly as" analogy extends a three-row disjunction to the mis-strided-filter
case, where only two of the three can fire. T26 is the one that is right, and I
can prove it. §17.3's forward shuffle sends byte *i* of group *j* to offset
*i·n + j* with *n = L/s*; solving *i·n + j = L − 1* over *0 ≤ j < n* gives
*i = s − 1*, *j = n − 1*, whose source offset is *j·s + i = ns − 1 = L − 1*. The
final byte is a fixed point at every stride dividing L (verified exhaustively for
all L ≤ 400). T5's subject — a packed planar bool plane's pad bits — lives only in
that final byte (§14.3), and the reader's inverse for such a plane is the identity
(mandated s = 1), so the reader's decoded image carries the writer's own final
byte and the pad bits survive intact. T5 is unreachable from a stride error.

**Which governs:** §21.1 makes the *rule* govern over a row, and `[R-COD-10]`
names "§14.5's padding, `[R-SER-08]`'s bool bytes", which §21.4 splits between T4
(padding positions and pad bits) and T2 (interleaved bool bytes). Both §21.7 and
T26 are restatements; the mechanics decide, and they decide for T26. §21.7's
analogy is the sentence to repair.

**Byte-level: no.** T5 and T26 carry the same detector (verifier) and the same
outcome (reject-tile); a file exhibiting the packed-planar-bool instance of T26
is nonconforming under T4 for both readings, and a file with no structurally
constrained byte is undetectable under both. Nothing about accept/reject changes.
What changes is what a corpus builder tries to construct: a T5-witnessed
mis-strided-filter vector is not constructible, and §21.7 currently implies it is.

### register-02 — CONTRADICTION — R7's Condition cell omits an alternative its own Instances cell and its governing rule state

**Location:** §21.5 row R7 (`[R-MTA-04]`, R-CNT-25); §18.2 `[R-MTA-04]` bullet 1.

R7's Condition cell:

> A decoded user-metadata document is not well-formed JSON, or its top-level value
> is not an object

R7's Instances cell:

> not well-formed JSON, top-level document; not well-formed JSON, layer sub-record
> document; top-level value not an object, top-level document; top-level value not
> an object, layer sub-record document; leading U+FEFF, top-level document;
> leading U+FEFF, layer sub-record document

§18.2's governing bullet states three restrictions, not two:

> - **A JSON object, unmarked.** The top-level value is an object, and the
>   encoding carries no byte-order mark: a leading U+FEFF makes the document
>   unreadable.

§21.1 licenses an instance to name "a field the condition ranges over, a container
it can occur in, one of several alternatives the condition text states, or any
combination of the three". "leading U+FEFF" is none of the three: not a field, not
a container, and not an alternative *the condition text states* — the Condition
cell stops at "or its top-level value is not an object". The cell is written and
therefore the mechanical count (6) reproduces and §21.8's 273 total stands; what
is defective is the row's restatement, which drops the BOM clause that the rule
carries and the Instances column then reintroduces.

I considered the rescue that a leading U+FEFF is *already* "not well-formed JSON"
under RFC 8259's grammar (`JSON-text = ws value ws`, and U+FEFF is not `ws`), and
it is — but §18.2 deliberately states the BOM prohibition separately, precisely
because parsers differ on it ("some parsers accept regardless" is the neighbouring
bullet's logic for the bare tokens), and R7's own Instances cell treats it as a
distinct shape. Either the Condition should carry the third alternative or the
Instances should not.

**Which governs:** the rule, per §21.1. `[R-MTA-04]` makes a BOM-led document
unreadable, so a reader takes ignore-record and a verifier reports nonconforming,
whichever way the row is read.

**Byte-level: no.** Both readings produce the same verdict on the same bytes,
because the rule is unambiguous and §21.1 makes it govern.

### register-03 — AMBIGUITY — §21.7's "witnessed only where … *and* …" is contradicted by the clauses that follow it

**Location:** §21.7 `[R-ERR-01]`.

> §20.3 step 4's bar on a declaration change is witnessed only where the affected
> tiles remain stored *and* the change reaches a byte §14 structurally
> constrains — a padding position, a pad bit, or a boolean byte — where §21.4's
> content rows fire; a change that reaches the decoded size instead is witnessed
> by T3 or T14, which test a length rather than the decoded image's content

Two readings are available.

*Reading A (conjunctive).* The italicised *and* introduces a second necessary
condition: the bar has a witness only when the tiles remain stored **and** the
change reaches a structurally constrained byte. Under this reading the very next
clause contradicts the sentence, since a change reaching the decoded size reaches
no such byte yet is said to be witnessed by T3 or T14. It also contradicts §21.1's
completeness clause, which would then make T3 and T14 rows for a condition §21.7
declares unwitnessed.

*Reading B (distributive).* "only where the affected tiles remain stored" is the
single necessary condition, and what follows is a case analysis: content-reaching
changes fire §21.4's content rows, size-reaching changes fire T3 or T14,
codec-reaching changes fire the rows for the codec now declared. Under this
reading the sentence is coherent and agrees with every row it names.

**I take Reading B**, because T3 and T14 are register rows with detector *reader*
that `[R-CNF-04]` obliges every reader to apply at tile use regardless of what
§21.7 says about them, and because §20.3 step 4's own text names the decoded size
among the four heads of the bar. An implementer who takes Reading A concludes that
a declaration change reaching only the decoded size of a still-stored tile is one
of the unwitnessed obligations and builds no vector for it; one who takes Reading
B builds a T3/T14 vector. That is a corpus difference, not a reader difference.

**Byte-level: no.** §21.7 is an account of what the register omits; it assigns no
check to any actor. Both readings leave every row of §21.2–§21.5 in force, so the
same files are accepted and rejected either way.

### register-04 — OBSERVATION — §21.1 states normative rules but carries no requirement identifier

**Location:** §21.1 (both paragraphs); §2.2.

§21.1 is where the register's governing rules live, and it says so:

> Its **completeness is normative** — a *detectable* file-conformance violation
> this specification names and the register omits is a defect in this document …
> but each row *restates* its governing rule, and where a row and the rule it
> cites diverge, **the rule governs**.

Neither paragraph terminates in a `[R-…]` identifier. The section cites
`[R-ERR-02]` parenthetically for the register's extent, but `[R-ERR-02]` is
§21.8's vector-coverage requirement, not this text. §2.2 says:

> Normative requirements carry identifiers of the form `[R-<PREFIX>-<NN>]`.
> Identifiers are stable: they are never renumbered or reused …

§21.1 therefore holds the only normative conflict-resolution rule in the document
— "the rule governs" — with no stable handle to cite it by. Everything that needs
it today cites §21.1 by section number (§19's preamble at line 2644, §21.6's
closing paragraph, §24's `[R-VEC-04]`), and §24's `[R-VEC-02]` requires a vector to
record its row's *governing* identifier, which is always the first one in the
Governing rule cell — so nothing is broken now. But §24 gives the reason
identifiers exist: "row labels are positional and renumber when a row is struck,
while §2.2 makes the identifier permanent". The register's own governing rules are
currently addressable only positionally.

**Byte-level: no.** No file's bytes and no verdict turn on whether §21.1 has an
identifier.

---

## 10. Things I checked and did not report

For the record, and so the next round does not re-spend the effort:

- Instance-count rules applied to all 121 rows; only R7 deviates.
- `[R-CNF-04]`'s "the register assigns the detector" versus §21.1's "the rule
  governs": a latent conflict with no exercised instance, because no row's
  Detector disagrees with its rule. Worth watching on future edits.
- L23's name-field instance is due at open by §19.1 step 4 though its cell says
  layer access; §19.2 licenses earlier detection and the outcome is identical, so
  no fork.
- §21.1's specialization list ("F1 of F6 and of F8, F35 of F36, L24 of L25") is
  introduced with "Some", so T12 ⊂ T9 and F3 ⊂ F10 not being listed is not a gap —
  and in both pairs the rows are written to be complementary (overflow versus
  in-domain-but-out-of-bounds) rather than nested.
- §21.1's "The subsections after §21.5 … carry no rows" then lists §21.6, §21.7
  and §21.9, omitting §21.8. §21.8 has no table; harmless.
- L26 and L31 put a section reference in the parenthetical where §21.1 specifies
  "further rules … cited without brackets". Format only; the governing identifier
  is still first.
- F21's gloss "placing its document inline" (an extent slot of (0,0) means no
  extent, not an inline document) and F5's inclusion of the pre-trailer pad among
  what "cannot all fit" (a 128-byte file need not have one). Both cosmetic; the
  conditions themselves are exact.
- §21.9's hard-limit list omits §7.1's `extent_length ≥ 5`, but the section
  disclaims inventory status in terms.
- Every CRC, offset, ordinal and size the document asserts, recomputed
  independently — all reproduce.
