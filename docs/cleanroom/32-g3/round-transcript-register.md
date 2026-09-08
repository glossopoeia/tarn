# Round 32 — Register hunter — working transcript

Charter: §21, the error-handling register, audited against the rules it restates
and against itself.

Access: I opened exactly one file, `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
reading it whole in four `Read` calls (lines 1–700, 700–1400, 1400–2100,
2100–2800, 2800–3500, 3500–4200, 4200–4754). I opened no other file, ran no
`git` command, listed no directory, and fetched nothing. Working files, all in
my own scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-round/scratch/register/`:
`norm.py` (whitespace-normaliser producing `flat.txt`), `flat.txt` (the
hard-wrap-flattened document, so phrase searches cannot fail on a line break or
a `> ` continuation), `count_reg.py` (mechanical row/instance counter),
`crc32c_check.py` (CRC-32C implementation and constant checks). Context I did
not ask for: a project instruction file (`CLAUDE.md` pointing at `AGENTS.md`)
and an index of the maintainer's memory notes about this project's harness
appeared in my context before I began. I read neither for content beyond
noticing what they were, and nothing below rests on either. The spec was where
the brief said it was.

---

## 1. Method

The document is hard-wrapped and blockquotes wrap with `> ` inserted, so I built
`flat.txt` first: every line stripped of a leading `> ` marker, then joined with
single spaces and whitespace-collapsed. Every phrase search below ran against
`flat.txt`, not against the raw lines. I checked the instrument on phrases I knew
were present before trusting any zero — e.g. `validity error` returned 52 hits
and `reject-file` 23, so a zero from the same tool is a real zero rather than a
wrap artefact.

I took the register's own rules (§21.1) as the yardstick, in this order:

1. recount conditions and instances mechanically and compare against every total
   the document states;
2. check every row against the requirement its Governing rule cell names —
   wording, outcome class, scope, detector, detection point;
3. sweep the document for conditions that make a file nonconforming and check
   each has a row (rules → rows);
4. check no row registers a non-violation (rows → rules);
5. resolve every citation of a register row from anywhere in the document;
6. check §21.9's limit material against every other statement of a limit, both ways;
7. check the outcome vocabulary is closed and every value reachable.

---

## 2. The counting

`count_reg.py` parses every table line matching `^\|\s*([FLTR]\d+)\s*\|`, splits
on `|`, and counts semicolon-separated entries in the Instances cell — which is
exactly §21.1's stated arithmetic:

> Instances within a cell are separated by semicolons, and a cell reading — is
> one instance; the count is therefore mechanical once the cell is written.

Result:

```
F: 35 conditions,  56 instances
L: 49 conditions, 116 instances
T: 26 conditions,  55 instances
R: 10 conditions,  50 instances
TOTAL: 120 conditions, 277 instances
```

Against the document's own figures:

- §21.2 "35 conditions" — reproduces (F1–F10, F12–F36; F11 struck, and the Note
  after the table says so).
- §21.3 "49 conditions" — reproduces (L1–L49).
- §21.4 "26 conditions" — reproduces (T1–T26).
- §21.5 "10 conditions" — reproduces (R1–R10).
- §21.8 "120 conditions over 277 instances" — reproduces exactly, both halves.

Every table row has exactly six cells (the parser reports none odd), every
verifier row's Detected cell reads `certification`, and every reader row's names
one of §19.2's four tiers (`open`, `layer access`, `tile use`, `extent use`), two
rows carrying a legitimate compound: L23 (`open (the name field, §19.1 step 4);
layer access (every other field and entry)`) and R1 (`open (top-level); layer
access (sub-record)`). That matches §21.1: "Detection points name §19.2's reader
tiers — open, layer access, tile use, extent use — or *certification* for the
rows a verifier detects".

I then hand-audited the instance cells against §21.1's two stated axes.

**Layout axis.** "Where the quantity a condition derives varies by layout, the
layout formulas are materially different shapes and the cell enumerates them."
Every row whose derived quantity is a *decoded size* enumerates three shapes
(interleaved P·Q; planar numeric P·Bᶜ; packed planar bool ⌈P/8⌉): T3, T14, T21,
T22, L44 — five rows, all three-shaped. Every row whose derived quantity is an
*addressed-tile count* enumerates two (interleaved N; planar C·N): L21. Rows
whose quantity does not vary by layout enumerate no layout (L22's index-region
formula). This is internally consistent across all seven rows.

**Magnitude axis.** "Where the condition compares two **magnitudes** either of
which can be the greater — a *differs from* or *does not equal* — the two
directions are likewise enumerated; where its own text bounds the comparison in
one direction — an *exceeds*, a *larger than* — there is one." Checked: F17 (2),
F23 (2), L12 (2), L21 (4 = 2×2), L22 (2 directions + 2 special cases), L30 (2),
T3 (6 = 3×2), T14 (6), T22 (6), R4's content-size pair (2 directions × 2
containers) — all two-directional. T21 ("larger than", 3×1), L44 ("exceeds",
3×1), F5/F9/F16/F22/F10/F32/L17/T9 (one-directional bounds) — all one. Checksum
comparisons and constant comparisons carry no direction: F14, F20, L37, L38, T1,
R2 — confirmed, each one per container. And "Nor does a field tested only for
being nonzero — an *A ≠ 0*, an *S ≠ 0*": L20 is one instance, L27 and L28 one
each. All consistent.

**Single-predicate rule.** "where a condition is a single predicate over several
fields — a sum against a bound, a combination of two flag bits — the fields it
reads are not instances". Checked against F10 (1), F32 (1), T12 (1), L20 (1),
L27 (1), L28 (1), F25 (1), L46 (2 = containers only, not the two bits) — all
consistent. F28 and L49 do enumerate the two flag bits, correctly, because their
condition is a disjunction ("a stored MU **or** PE bit differing"), not a
combination.

**Verdict on the counting: the register's arithmetic reproduces exactly, per
subsection and in total.** No finding here.

## 3. Other numbers I derived myself

`crc32c_check.py` implements CRC-32C (reflected, poly 0x82F63B78, init/final
0xFFFFFFFF) and reproduces §4.5's check vector first:

```
CRC-32C("123456789")            = 0xE3069283   spec: 0xE3069283  ✓
CRC-32C(zero bytes)             = 0x00000000   spec: 0x00000000  ✓
```

Then the constants the register and its neighbours restate:

```
full all-sentinel segment (65536 × "FF×16 00×4") = 0xEECB3BB2
   §15.4 and Appendix B: 0xEECB3BB2  ✓   (L38 quotes this constant)
§7.4's 4-sentinel 80-byte array                  = 0x80A34955  (stored 55 49 A3 80) ✓
§7.4's crc_of_crc_array over those 4 bytes       = 0xC4EE982E  ✓
Appendix A's trailer CRC over trailer [0,60)     = 0x402F157E  ✓
```

§21.9's Note: "2³² addressed tiles is the point where the segment-CRC array …
is still 256 KiB — it reaches 4 MiB at 2³⁶".
⌈2³²/2¹⁶⌉ × 4 = 2¹⁶ × 4 = 262 144 = 256 KiB ✓; ⌈2³⁶/2¹⁶⌉ × 4 = 2²⁰ × 4 =
4 194 304 = 4 MiB ✓.
Full segment = 2¹⁶ × 20 = 1 310 720 = 1.25 MiB, matching §15.4's example ✓.
"65,536 layers is roughly a 12.5 MiB directory" → 13 107 200 / 65 536 = 200 bytes
per layer record; §7.4's worked minimal layer record is 24 + 81 = 105 bytes, so
200 is a plausible "small layer record" and the figure is not falsifiable ✓.
16 MiB > 12.5 MiB, so the directory row does state "that same budget" with headroom ✓.

§15.4's worked example (adjacent to L37/L38, which restate it):
entry_count 1 000 000 → ⌈1e6/65536⌉ = 16 segments, 15 full covering 983 040
entries and a last covering 16 960 ✓; CRC array 64 bytes ✓; region
1 000 000×20 + 64 = 20 000 064 ✓; entry 999 999 at segment-relative byte
20 × 16 959 = 339 180 ✓; array at [20 000 000, 20 000 064) ✓; segment 15 at
[19 660 800, 20 000 000) ✓. All reproduce.

## 4. §21.2's reach derivation — re-derived by hand

§21.2's preamble makes a closed claim I could check:

> Deriving it there yields F8, F14, F6 and both of F1's instances — each
> asserting an invariant `[R-CNT-24]` fixes in every major — and no other row.

[R-CNT-24] fixes exactly four things in every major: (i) the trailer magic at
F − 64; (ii) version_major and version_minor at F − 56; (iii) a CRC-32C at F − 4
covering [F − 64, F − 4); (iv) the front signature block constant. Everything
else in the trailer — offsets 12 through 59, 48 bytes — is redefinable.

Walking all 120 rows: (i) is asserted by F8 and by F1's trailer-magic instance;
(iii) by F14 (its Condition cell reads "The u32 at trailer offset 60 does not
equal the CRC-32C of trailer bytes [0,60)", and trailer offset 60 is F − 4 while
trailer [0,60) is [F − 64, F − 4) — the same assertion, byte for byte); (iv) by
F6 and by F1's front-block instance. (ii) fixes position only, not a value
constraint, so F18 asserts nothing [R-CNT-24] fixes — and §21.2 does not claim
it does, treating F18 as a case outside [R-CNF-13]'s premise because
version_major = 0 declares no major. Every other F row turns on a field at
trailer offsets 12–59 (F2's dir_offset/dir_length/committed_file_length, F9,
F10, F12, F13, F15, F16, F17, F19) or on a structure this text defines for major
1 only (F5, F7, F20–F36); every L, T and R row likewise. **The derivation
reproduces exactly, with no row over- or under-claimed.** §2.3's Note's three
worked cases (F14 reaches, F5 does not, F15 does not although its Governing rule
cell cites `[R-CNT-24]`) each check out; I confirmed F15's Governing rule cell
really does read "`[R-CNT-06]` (R-CNT-24)".

I also checked §2.3's arithmetic that "`[R-CNT-06]` states nine". Rows whose
Governing rule cell names [R-CNT-06] *first* are F8, F9, F10, F12, F13, F14,
F15, F16, F17 — nine exactly, and two of them (magic, CRC) reach while the other
seven do not, which is precisely what §2.3 says. Rows citing [R-CNT-06] only
parenthetically (F2, F3, F5) are governed elsewhere and correctly excluded.

## 5. Row-versus-rule, row by row

I read every row's Condition, Instances, Detector, Detected and Governing rule
cells against the requirement named, in the source section. Rather than
reproduce 120 paragraphs, here is what I checked and where it landed.

**Outcome vocabulary.** §2.4/[R-CNF-07] defines four reader outcomes —
reject-file, reject-layer, reject-tile, ignore-record — plus preserve-verbatim as
an updater obligation explicitly "orthogonal to reader outcomes". §21.2–§21.5 are
titled by those four, one apiece, so every defined reader-outcome value is
reachable and no row carries a value the document does not define.
preserve-verbatim correctly has no subsection: it is not a reader outcome.
Clean.

**Scope agreement.** For each row I checked the subsection's outcome against the
scope its governing rule assigns.
- Every F row: [R-ENC-02] "reject-file"; [R-ENC-03]/[R-ENC-04] at the owning
  scope, which for the trailer is the file ([R-CNT-06]: "The owning scope of the
  front signature block and the trailer is the file") and for a non-layer
  top-level record is the file ([R-CNT-13]: "the file for other top-level
  records"); [R-ENC-15] "a duplicate layer name is a file-scope error
  (reject-file)"; [R-CNT-27] "at file scope"; [R-CNT-04] "reject-file";
  [R-CNT-05] "at file scope"; [R-CNT-06] "Any failure is reject-file";
  [R-CNT-07] "reject-file"; [R-CNT-08] "reject-file"; [R-CNT-11] "reject-file";
  [R-CNT-25]/[R-MTA-03] "containing scope" = file for a top-level record;
  [R-CNT-12] "reject-file for the directory's top-level sequence"; [R-CNT-14]
  "the directory's scope (reject-file)"; [R-CNT-15] "MU = 1 → reject-file" and
  "the record's governing scope"; [R-CNT-22] "the record's governing scope";
  [R-MTA-05] "the file is nonconforming". All agree.
- Every L row: layer scope in each cited rule. [R-CNT-13] "the layer for a layer
  record and for sub-records", [R-CNT-18] "at layer scope", [R-CNT-23] "at layer
  scope", [R-GEO-01]/[R-GEO-05]/[R-TYP-03]/[R-TYP-07]/[R-SER-06]/[R-COD-03]/
  [R-COD-07]/[R-COD-09] "at layer scope", [R-IDX-04] "is reject-layer",
  [R-SLB-01]/[R-SLB-03] "violation: reject-layer", [R-ENC-11]/[R-ENC-12]/
  [R-ENC-15] at the owning scope, which §7.4 fixes as the layer for the layer
  record's inline payload. All agree.
- Every T row: [R-CNT-20] "a stored tile's CRC → reject-tile"; [R-IDX-03]'s
  eleven-row table; [R-SER-05]/[R-SER-07]/[R-SER-08]/[R-COD-04]/[R-COD-06]/
  [R-COD-08]/[R-COD-10] "at tile scope"; [R-COD-02] via T25's check. All agree.
- Every R row: ignore-record, assigned expressly by [R-CNT-25]'s quarantine and,
  for R4, by [R-MTA-09] ("Any violation here is ignore-record"). All agree.

**Detector agreement.** For each of the twenty verifier rows (F7, F25, F26, F27,
F28, F33, F36, L18, L25, L40, L41, L42, L46, L47, L48, L49, T2, T4, T5, T26) the
governing rule says a verifier detects and a reader is not obliged: [R-CNT-05]
"A verifier MUST treat a structure in that gap…(readers check neither)";
[R-CNT-12] "their detection is a verifier's"; [R-MTA-05] "a verifier MUST report
it"; [R-CNT-22] "a verifier MUST treat the mismatch"; [R-CNT-13] "(readers are
not obligated to detect overlap…)"; [R-CNT-15] "a verifier MUST treat a
reserved-range record type as a validity error"; [R-SLB-01]/[R-SLB-03] "A
verifier MUST check…readers are not obligated to"; [R-SER-08] "its assigned
detector is the verifier"; [R-SER-05] "a verifier MUST check it"; [R-COD-10] "a
verifier detects it". Every one agrees. No row assigns to a reader what its rule
assigns to a verifier, or the reverse. This is the failure mode §21.1 warns
about most and I found none of it.

**§15.3's table against §21.4.** §15.3 states eleven entry states. Mapping:
sentinel (no row, §21.6's first entry); crc ≠ 0 sentinel → T6; half-sentinel →
T7 (2); length 0 → T10; offset < 16 → T8; offset or length > 2⁶³−1 → T11 (2);
overflow → T12 and > F−64 → T9; stored bytes fail crc → T1; intra-layer overlap
→ L18; extra-layer overlap → F33; alignment/slab → L40, L41, L42. Every row
accounted for, both ways, and §15.3's own count "Six rows are marked
*structural*" is right (rows 2–7 of its table).

**§8.2's chain against the register.** [R-CNT-20]: "trailer or directory →
reject-file" (F14, F20); "any of a layer's index cross-checks (`[R-CNT-17]`), CRC
array, or segments → reject-layer" (L21, L22, L37, L38); "a stored tile's CRC →
reject-tile" (T1); "a user-metadata extent's CRC → ignore-record" (R2). Complete
in both directions.

**§18.2's four document restrictions against §21.5.** "A JSON object, unmarked" →
R7; "Finite numbers only" → R8; "No duplicate keys" → R9; "Well-formed UTF-8
throughout … and every key satisfying §4.6's name rules — non-empty, at most 255
bytes, free of U+0000 through U+001F" → R5, R6, R10. Complete.

**R4 against §18.2's carried-over frame constraints.** §18.2 carries over "the
frame magic; no skippable frame and no second frame; no dictionary use, disclosed
or not, and no nonzero dictionary ID; no content-checksum flag; and the bar on
sizing any buffer from a length the frame itself declares", replaces the
decoded-size and Window_Size constraints, adds "exactly one … frame occupying the
extent's bytes before its terminal CRC" and a content-size rule keyed to the
decoded document's byte length, and explicitly excludes two from the register
("R4 registers neither"): the undisclosed dictionary and the buffer-sizing bar.
That leaves exactly eight registrable conditions — magic, skippable frame, second
frame, dictionary ID, content-checksum flag, trailing bytes, content-size larger,
content-size smaller — and R4 enumerates all eight in two containers, 16
instances. Reproduces exactly.

## 6. Completeness, rules → rows

I enumerated every `validity error` statement (52 hits), every `reject-file` (23),
`reject-layer` (21), `reject-tile` (18) and `ignore-record` (21) statement, and
every `Writers MUST NOT` / `writers MUST` (16 + 9) outside the register tables,
and traced each to a row or to an explicit exemption. The traceback:

- [R-ENC-02] → F1. [R-ENC-03] → F2, L1, T11. [R-ENC-04] → F3, L2, T12.
  [R-ENC-06] → §21.7 states no condition exists. [R-ENC-07] → F16, F22, F23,
  F29, L11, L12, L14, L22. [R-ENC-11] → L3, L4 (and R5 inside a document).
  [R-ENC-12] → L5–L8 (and R6, R10). [R-ENC-13]/[R-ENC-14] state no condition.
  [R-ENC-15] → F4, L9.
- [R-CNT-02] → F33, L18 (§5.2's Note: "only disjointness is testable … a register
  row for it would be a row no file could exhibit"). [R-CNT-03] SHOULD.
  [R-CNT-04] → F6. [R-CNT-05] → F7. [R-CNT-06] → F8–F17. [R-CNT-07] → F18.
  [R-CNT-08] → F19. [R-CNT-09] SHOULD. [R-CNT-11] → F20. [R-CNT-12] → F24, F25,
  F26, F29, L13, L14, L46, L47. [R-CNT-13] → F30–F33, L15–L18. [R-CNT-14] → F34,
  L19. [R-CNT-15] → F35, F36, L24, L25. [R-CNT-16] → L20. [R-CNT-17] → L21, L22.
  [R-CNT-18] → L23, L26; its nesting prohibition is exempted in terms by §7.4's
  Note ("in format major 1 it has no reader-detectable witness, and so no
  register row"); its unknown-sub-record-MU=1 case is a conforming file, recorded
  in §21.6's closing paragraph. [R-CNT-21] verifier reporting, no condition.
  [R-CNT-22] → F28, L49. [R-CNT-23] → L27–L31, L35 and the whole §7.4 constraint
  set. [R-CNT-24] no condition of its own. [R-CNT-25] → F21, F22, L10, L11, R1,
  R3, R5. [R-CNT-26] SHOULD. [R-CNT-27] → F5.
- [R-LIF-01]…[R-LIF-08]: no live-state witness for the commit-protocol and
  immutability rules (a verifier "walks the live state only", §9.7), and §9.5's
  Note says so in terms for residue past a completed commit ("carries no register
  row of its own"). [R-LIF-04]'s truncation obligation surfaces as F17.
  [R-LIF-08]'s three walk checks map to the bounds rows, the overlap rows, and
  the checksum rows.
- [R-EXT-03] → L31, L33, L34, L36, L43, L45, R1, F35/F36, L24/L25.
- [R-GEO-01] → L32. [R-GEO-02] → §21.6. [R-GEO-03] → L2. [R-GEO-04] → T4 via
  [R-SER-05]. [R-GEO-05] → L33. [R-GEO-06] no condition.
- [R-TYP-03] → L34. [R-TYP-06] → L30. [R-TYP-07] → L35. [R-TYP-10] SHOULD.
- [R-SER-02]/[R-SER-07] → T3, L2. [R-SER-03] → T5. [R-SER-05] → T4, T5.
  [R-SER-06] → L36. [R-SER-08] → T2 (+ T4 for the padding-position byte).
  [R-SER-09] → §21.6.
- [R-SLB-01] → L39, L40. [R-SLB-02] → L28, L29. [R-SLB-03] → L41, L42.
  [R-SLB-04] exempted in terms by §16.2's Note ("a stale declaration carries no
  register row of its own"). [R-SLB-05] no condition.
- [R-COD-02] → T13. [R-COD-03] → L43. [R-COD-04] → T14. [R-COD-05] → T15, T16.
  [R-COD-06] → T17–T22 (undisclosed dictionary explicitly unwitnessed, §21.7).
  [R-COD-07] → L44, T23. [R-COD-08] → T24, T25. [R-COD-09] → L45. [R-COD-10] →
  T26.
- [R-MTA-03] → F23, L12, R1. [R-MTA-04] → R5–R10. [R-MTA-05] → F27, L48.
  [R-MTA-06]/[R-MTA-07] → §21.6, both non-violations by their own rules.
  [R-MTA-09] → R4. [R-MTA-10] → §21.6.
- [R-WRT-05]/[R-WRT-06]/[R-WRT-07]: no live-state witness (the format records no
  commit count and §9.7 reconstructs no history), and §20.4's Rationale says so.

**I found no rule stating a detectable file-conformance violation that the
register omits.** The one place a rule's reach is narrower than its wording
(names longer than 255 bytes) is unrepresentable — the length prefix is a `u8`,
which [R-ERR-05] itself gives as the reason — and R10 correctly registers the
*key* case, keys carrying no prefix.

## 7. Completeness, rows → rules

Every row I could plausibly have called an over-registration turned out to be
backed:

- T13, T15, T16, T23, T26 each say in terms that they record a *cause* whose
  detecting check belongs to another row ("the check that detects it is T25's",
  "T24's or T25's", "T2's or T4's"). Each cause is a genuine violation of its
  governing rule ([R-COD-02], [R-COD-05], [R-COD-07], [R-COD-10]) and each is
  detectable through the row it names, so each satisfies §21.7's detectability
  test. Consistent, and the detectors line up: T13/T15/T16/T23 are reader rows
  whose detecting rows are reader rows, T26 is a verifier row whose detecting
  rows (T2, T4) are verifier rows.
- F25/F26/L46/L47 (flag violations), F27/L48 (unsorted document), F28/L49
  (stored-flag mismatch) are all violations by explicit statement in [R-CNT-12],
  [R-MTA-05] and [R-CNT-22] respectively ("make the file nonconforming").
- F35/L24 are not redundant with F36/L25: F35/L24 carry detector *reader*, which
  is the whole point of §21.1's strict-specialization rule ("whose detector and
  detection point are the ones that apply").
- The experimental-range values registered as violations in L31, L33, L34, L36,
  L43, L45 are violations because their *reader* rules make them validity errors
  at layer scope ([R-GEO-05], [R-TYP-03], [R-SER-06], [R-COD-03], [R-COD-09],
  §7.4/§15.1), which is exactly the distinction [R-EXT-03] draws between those
  spaces and the record-type and metadata-encoding spaces, where the
  experimental range is conforming (§21.6).

**No row registers a condition its rules do not make a violation.**

## 8. Every citation of a register row, resolved

I extracted every `F<n>`/`L<n>`/`T<n>`/`R<n>` token occurring outside the four
register tables and read each in context. Twenty-eight distinct labels are cited
from outside; each resolved as follows.

- §2.3 [R-CNF-13] "(§21.2, F18)" — F18 is version_major = 0 ✓.
- §2.3 [R-CNF-11] "(§21.5, R1)" — R1 registers encoding 0 and the reserved range ✓.
- §2.3's Note: F14 reaches, F5 does not, F15 does not "although its Governing rule
  cell cites `[R-CNT-24]`" — F15's cell reads "`[R-CNT-06]` (R-CNT-24)" ✓.
- §6.2's trailer table "(F19)" — F19 is the incompat-lane bit ✓.
- §9.6 "(§21.2 rows F8, F14 and F17 — the magic, the trailer CRC and the length
  cross-check)" — each row is what the gloss says ✓.
- §5.2 [R-CNT-21] "L18's overlap or L40 through L42's placement" — L18 is
  intra-layer overlap, L40/L41/L42 are alignment and slab placement, all verifier
  reject-layer, all establishable by the coverage walk ✓.
- §17.2's deflate Note "(§21.4, T24)" — T24 is trailing bytes after the stream ✓.
- §18.2 "R4 registers neither", "not a failure to decode under R3", "Routing it to
  R4" — all consistent with R3's and R4's Condition cells, which themselves
  cross-refer correctly ✓.
- §20.3 "`[R-COD-07]`'s lz4 decoded-size cap (L44 …)" ✓.
- §20.5 [R-WRT-06] "F36 and L25 for a record type, and one row for each of the
  other seven spaces §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)" — I
  counted §10.2's table: eight spaces, so "the other seven" after record type are
  channel layout, linearization, sample type, codec, filter, index encoding,
  metadata encoding; the seven rows named cover exactly those, each registering
  its reserved range ✓. Naming F36/L25 rather than F35/L24 is right, because
  [R-WRT-06] makes a compactor refuse any unimplemented MU = 1 record, so only the
  MU = 0 case can reach a compactor's output ✓.
- §21.1's specialization list "F1's front-block instance of F6 and its
  trailer-magic instance of F8, F35 of F36, L24 of L25, F21 of F22 and L10 of
  L11" — I checked each containment. A byte-reversed front block is necessarily
  not byte-identical to the constant (F6) ✓; a byte-reversed trailer magic is
  necessarily not the magic (F8) ✓; a reserved-range type with MU = 1 is
  necessarily a reserved-range type (F36/L25) ✓; an extent slot of (0, 0) has
  extent_length 0 < 5 (F22/L11) ✓. All five hold, and the list is expressly not
  closed.
- §21.1's instance examples "(T24's *any codec*)" and "(T15, T25)" — T24's cell
  reads `any codec`, one instance ✓; T15 (2) and T25 (3) enumerate materially
  different shapes ✓.
- §21.1 "(… `[R-MTA-05]`, whose unsorted document readers process as they find it
  — F27 and L48)" — F27 and L48 are the [R-MTA-05] rows ✓. The parenthetical
  names no rows for the [R-CNT-22] half of the same sentence (F28, L49), which is
  asymmetric but not false, the em-dash falling inside the second semicolon
  clause. I decided not to file this: the sentence says "several such rows", not
  "these rows", and nothing turns on it.
- §21.2's reach paragraph "F8, F14, F6 and both of F1's instances … F18" ✓
  (re-derived in §4 above).
- §21.6's table "(F36, L25)" ✓; §21.6's closing "(F18, `[R-CNT-07]`)" and
  "(F35, F36, L24, L25)" ✓.
- Appendix H "(F1, F6)", "(`[R-CNT-05]`, F7)", "(`[R-CNT-15]`, F36, L25)", "(R1)"
  — each resolves to a row saying what the checklist claims ✓.
- §20.3 "(T3, T14, T2)" — **this one does not resolve.** See finding
  register-01 below.

## 9. Limits, both directions

§21.9's minimum-guarantee table has eight rows: rank 32, C 4096, entry_count 2³²,
65 536 layers, 16 MiB dir_length, 256 MiB decoded tile, 16 MiB metadata document,
8 MiB zstd Window_Size. Appendix B's collected line restates all eight
identically ("rank 32 · C 4096 · entry_count 2³² · 65,536 layers · 16 MiB
directory region · 256 MiB decoded tile · 16 MiB metadata document · 8 MiB zstd
window"). §18.2's Note ("The 16 MiB figure is a §21.9 minimum guarantee"),
§17.2's [R-COD-06] and §18.2 ("§21.9's 8 MiB `Window_Size` guarantee") each cite
a figure matching its row. §1's pillar and Appendix D both cite the entry_count
guarantee consistently. §24 cites the tile-count guarantee as the one not
constructible at the bound. No divergence anywhere.

Consistency against the hard limits: rank 32 ≤ 255 (§7.4's `u8`), C 4096 ≤ 65 535
(`u16`), entry_count 2³² ≤ 2⁶³−1, decoded tile 256 MiB < 0x7E000000 so the lz4
cap never contradicts the guarantee. All clear.

[R-ERR-05]'s hard-limit list: I checked each of its nine items against its
defining section — name ≤ 255 (§4.6), user-metadata key ≤ 255 (§18.2 folding
§4.6), rank ≤ 255 and C ≤ 65 535 (§7.4), lz4 cap 0x7E000000 (§17.2), value domain
2⁶³−1 (§4.2), A a power of two 512…2⁶² (§7.4, §16.1), A_slab a power of two
1…2⁶² (§7.4), S 1…2⁶³−1 (§7.4), dir_offset ≥ 16 and dir_length ≥ 4 (§6.2), 128-byte
floor (§5.1). Every one matches its defining section, and Appendix B's constants
table matches all of them again.

Two candidates for "a limit stated elsewhere and missing here" I opened and
closed:

1. **The user-metadata extent minimum of 5 bytes** (§7.1, Appendix B) is absent
   from [R-ERR-05]'s hard-limit list. Closed by §21.9's own opening: "The hard
   limits it restates are a finding aid rather than an inventory". The list
   disclaims completeness in terms, so an omission from it is not a defect.
   F22 and L11 register the condition regardless.
2. **§16.2 states A_slab as "a power of two ≥ 1" with no ceiling**, while §7.4's
   table and [R-ERR-05] both give 1 ≤ A_slab ≤ 2⁶². §16.2 opens by referring the
   field constraints to §7.4 ("§7.4; mutually exclusive with per-tile alignment"),
   so this is a partial restatement rather than a divergence: a floor stated
   without a ceiling is consistent with a bounded range, and L29 registers the
   ceiling with [R-CNT-23] governing, which is exactly what §21.1 prescribes.

## 10. Findings

### register-01 — CONTRADICTION — §20.3 step 4, citing §21.4's rows

§20.3's closed-list paragraph justifies which declaration changes a commit may
make by claiming that changing a *fixed* declaration is invisible to every check
the specification obliges, save two:

> Under new ones the same bytes would denote values, coordinates or padding the
> writer did not store, with every checksum in §8 certifying the result and, but
> for a decoded size or a boolean byte the register witnesses (T3, T14, T2), no
> check any actor owes able to see it (§21.7).

The same sentence lists, three clauses earlier, what the fixed declarations are:
"the ones §14 reads a stored tile under — its value sequence, its byte layout,
**the fill its padding positions hold (§14.5)**". A channel's fill is on §20.3's
fixed list ("every channel's type and fill"), and §14.5 constrains stored padding
content to it:

> at every padding position, a writer MUST encode, for each channel the position
> carries, that channel's fill value … Every pad bit (§14.3) MUST carry the
> plane's channel's fill bit. A conforming reader never returns this content
> (`[R-GEO-04]`) and is not obligated to check it; **a verifier MUST check it**,
> and a violation is a validity error at tile scope. `[R-SER-05]`

§21.4 registers exactly that check as **T4** ("A padding position does not
encode, for each channel it carries, that channel's recorded fill value",
detector *verifier*, detected *certification*) and **T5** (a packed plane's pad
bits). And §21.7 — the section §20.3 cites for the proposition — states the
narrowing as *three* things, not two:

> The obligations of §14.5 and `[R-SER-08]` narrow this only where content is
> structurally constrained: padding positions, pad bits, and boolean bytes.

Worked witness. Take an interleaved layer, one `uint8` channel with fill `0x00`,
extents (5), tile extent (4). Grid = 2. Tile 1 covers positions 4–7: position 4
is real, 5–7 are padding, so its stored decoded image is `v 00 00 00` with the
three padding bytes at the recorded fill. A commit that changes only the fill to
`0xFF` — a change §20.3 forbids, and forbids on the strength of this sentence —
produces a file in which the layer declares fill `0xFF` while tile 1's padding
bytes are `0x00`. That is T4's condition on its "interleaved numeric fill bytes"
instance: a verifier MUST see it. The parallel case for a packed planar bool
plane with P = 10 and fill flipped false → true is T5's. Neither is a decoded
size and neither is a boolean byte, so neither is on §20.3's "but for" list.

The register (T4, T5), [R-SER-05], and §21.7's own three-item narrowing all say
one thing; §20.3's two-item list says another. Since §20.3's sentence is a
justification and its own closed list bars the change under either reading, and
since [R-SER-05] is unambiguous about the verifier's duty, no byte sequence and
no verdict moves. What moves is the document's account of why the line is drawn
where it is — and this is precisely the passage the last three cycles have
rewritten most.

### register-02 — CONTRADICTION — §21.6's closing paragraph vs [R-CNF-12]

§21.6's closing paragraph records the recent reclassification of two conditions
out of the defined-non-violations table and into the register, and then makes a
claim about what did not change:

> Both make the file nonconforming while leaving every reader behavior unchanged
> — readers process the document and apply the type's fixed semantics — so both
> carry detector *verifier*, on the precedent `[R-CNT-12]`'s reserved-flag rows
> already set. What belongs here is the reader's side of them, and it is
> unchanged: **neither is a reason for a reader to reject anything.**

§2.4's [R-CNF-12] says the opposite for exactly this class of condition:

> For a nonconforming file no acceptance obligation exists — a reader MAY reject
> it upon detecting any violation, **including violations whose assigned detector
> is the verifier**.

The reader's side is precisely what the reclassification changed. While an
unsorted user-metadata document sat in §21.6's table, the file carrying it was
conforming, [R-CNF-12] attached nothing, and §21.6's opening rule bit: "A reader
that treats any of them as a validity failure is the nonconforming party." Now
that the condition is a registered violation (F27, L48), the file is
nonconforming and [R-CNF-12]'s licence attaches, so a reader that detects an
unsorted document MAY refuse the file. The same holds for F28/L49.

The document makes exactly this qualification elsewhere, in [R-CNT-18], for the
structurally identical case:

> where the file is otherwise conforming a reader MUST NOT reject the file for it
> — on a nonconforming file `[R-CNF-12]`'s licence to reject on any detected
> violation is untouched

§21.6's closing sentence omits the qualification [R-CNT-18] supplies. Two
readings survive: (a) "no rule here obliges or specifically licenses rejection,
and [R-CNF-12]'s general licence is untouched", which is true; (b) "a reader may
not reject for these", which would make a reader relying on [R-CNF-12] the
nonconforming party. I pick (a): §21.6's opening rule is scoped to "These" — the
table's entries — and these two conditions are expressly not among them; and
§2.1 binds BCP 14 keywords only in all capitals, so a lowercase "is a reason"
does not bound an all-capitals "MAY reject". Under (b) two readers would return
different verdicts on the same bytes — one refusing the file, one obliged to
serve it — but the file is nonconforming under both readings, so [R-CNF-05] bars
every conforming writer from emitting it either way and the emittable set does
not move; and reading (b) requires importing a rule §21.6 scopes to its own
table. I therefore grade this below byte-level while noting what (b) would cost.

### register-03 — AMBIGUITY — [R-CNT-25] (§7.1) against F27 and L48

[R-CNT-25] closes its quarantine paragraph with an unqualified sentence:

> User metadata is quarantined: each way a user-metadata record's document can be
> unreadable once its framing has been read — a failed extent CRC, an
> unimplemented or invalid encoding, a decode failure, or content violating the
> document's own rules (ill-formed UTF-8 included, `[R-ENC-11]`) — is
> ignore-record with a SHOULD-report, notwithstanding the owning-scope mapping of
> `[R-CNF-08]`. **Application metadata never invalidates the structural data it
> annotates.**

§21.2's F27 records an unsorted file-scope user-metadata document at **file**
scope (reject-file) and §21.3's L48 records the layer sub-record case at **layer**
scope (reject-layer). They escape the quarantine because [R-MTA-05] says
"unsorted members do not make a document unreadable", so the quarantine's premise
fails and §21.1's owning-scope mapping applies. But [R-MTA-05] also says "the
file is nonconforming, a verifier MUST report it", and §2.4 says "a verifier
certifies only violation-free files". So a file whose every structure is intact
and whose only defect is the key order of an application-metadata document cannot
be certified: the metadata has decided the structural verdict for the whole file,
and L48 records the damage against the very layer the metadata annotates.

Two readings of "invalidates":
(a) *causes a reader to treat the annotated structural data as unusable* — true,
since §21.1 makes a verifier row's outcome "the scope at which the damage is
recorded, not an obligation on any reader", and no reader obligation attaches;
(b) *bears on the conformance of the annotated structure* — false, per
[R-MTA-05] and F27/L48.

I pick (a): the sentence sits in a paragraph whose whole subject is outcome
assignment ("is ignore-record … notwithstanding the owning-scope mapping"), and
§21.6's closing paragraph makes the narrow sense explicit for these two
conditions. But nothing at §7.1 says so, and a verifier author who reads §7.1 and
takes reading (b) will certify a file §21 says is nonconforming. That is a
verdict divergence, and I would not call it byte-level only because the more
specific and later rule ([R-MTA-05], with its explicit "the file is
nonconforming") plainly governs over an unscoped gloss, and §21.1's "where a row
and the rule it cites diverge, the rule governs" points at [R-MTA-05], which F27
and L48 cite.

## 11. Suspicions I opened and closed

- **§21.9's hard-limit list omits the ≥ 5-byte user-metadata extent minimum.**
  Closed by "The hard limits it restates are a finding aid rather than an
  inventory."
- **§21.9's guarantee table bounds no stored tile's *stored* length**, while
  §17.2's Note says "Resource limits are §21's subject", so a reader that caps a
  stored extent's size has a limit "living only in an implementation"
  ([R-CNF-10]) and, per [R-ERR-04], "is not a conforming reader". I built the
  witness (a deflate stream of ~2×10¹¹ empty stored blocks decoding to a 1 KB
  tile is legal under RFC 1951 and satisfies [R-COD-08]'s exact-consumption
  rule). Closed, not filed: the stored length is bounded by F through T9, so
  there is no amplification — the attacker must supply the bytes — and the
  guarantees are stated over what a reader must *hold*, not what it must stream;
  the decoded tile, directory, CRC array and segment all have rows and are the
  quantities a reader allocates. This is a design remark, not a divergence
  between two statements in the document, and my charter's limits bullet asks for
  divergences.
- **F6/F1's front-block instance carry Detector *reader* though [R-CNT-04] lets a
  non-resident reader omit the check, while Appendix H lists the same check as
  one "readers are exempt from".** Closed: both rows carry the residency
  qualifier in their own Condition cells, and Appendix H states the same
  qualifier correctly ("which `[R-CNT-04]` lets a reader not holding it resident
  defer or omit and §2.3 does not"). No implementer is misled and §21.1's
  rule-governs clause settles it.
- **L46 (layer record MU = 1 / PE = 0) is a strict specialization of L49 (stored
  flag differs from the registry), and T14 of T3, and F5 of F9/F10/F16**, none of
  them in §21.1's list. Closed: "the property decides any pair and this list is
  not offered as closed."
- **F7 and F33 both enumerate "tile-index regions" and "record extents" as
  separate instances, though a tile-index region *is* a record extent** (§9.7:
  "the region enters the walk once, as that record's extent"). Closed: §21.1 makes
  the count "mechanical once the cell is written", the instance counts reproduce
  the stated totals either way, and the enumeration is a list of claimant kinds
  rather than a partition claim.
- **§21.1's parenthetical "F27 and L48" names rows for [R-MTA-05] but none for
  [R-CNT-22]** in a sentence that covers both. Closed: the sentence says "several
  such rows", the em-dash falls inside the [R-MTA-05] clause, and F28/L49 are
  registered and correct regardless.
- **§21.6's entry for an experimental-range MU = 0 record cites `[R-WRT-08]` for
  "preserved or dropped per its PE bit", but [R-WRT-08] states only the
  no-re-encode rule; the PE-drop rule lives in §20.4's unlabelled table.** Closed:
  the document consistently cites that table by section ([R-CNF-06], §2.4's
  preserve-verbatim row, Appendix H all do), [R-WRT-08] is the nearest identifier
  and is about the right subject, and nothing turns on the choice.
- **R4's content-size, dictionary-ID and content-checksum instances are not ways a
  document is "unreadable", yet sit in §21.5 whose preamble is framed around
  unreadability.** Closed: §21.5's preamble states unreadability as a sufficient
  ground for the outcome, not a necessary one, and [R-MTA-09] assigns
  ignore-record expressly ("Any violation here is ignore-record"), which §21.1
  permits ("except where a rule assigns one expressly").
- **§21.6's table records a resource decline for a user-metadata document's size
  and window but not for a tile's or a layer's.** Closed: §21.1 states that
  neither the completeness clause nor the instance arithmetic reaches §21.6, and
  [R-ERR-04] states the general rule for every scope.
- **F5's Condition cell names a "pre-trailer pad" among the components that
  "cannot all fit", though [R-CNT-27]'s derivation names only the front block,
  the directory and the trailer.** Closed: a zero-length pad fits trivially (a
  directory at [16, 64) leaves none, per [R-CNT-05]), so the sentence is not
  false and the 128-byte bound is identical either way.
- **§21.1's "An instance names a field …, a container …, one of several
  alternatives …, or any combination of the three" reads as a closed list of
  three axes, then two more axes are stated two sentences later.** Closed: the
  operative test given immediately after is "materially different shapes", and
  both later axes are applications of it, stated "rather than judged each time".
- **Whether an unknown (experimental) sub-record type with MU = 1 — reject-layer
  on a conforming file — needs a §21.6 table row.** Closed: §21.6's closing
  paragraph addresses it in terms ("the same type as a layer sub-record is
  reject-layer and never a ground to refuse the file"), and §21.1 exempts §21.6
  from the completeness clause.

## 12. What I would have caught

For the parts of the charter where I found nothing, here is what I did that
would have surfaced a defect had one been there. The counting: a mechanical
recount from the table source, per subsection and in total, against four stated
condition counts and one stated instance total — a discrepancy of one anywhere
would have shown. The row-versus-rule sweep: I read all 120 Governing rule cells
and opened each cited requirement, comparing outcome, scope, detector and
detection point; a row assigning to a reader what its rule assigns to a verifier
(the failure mode §21.1 exists to arbitrate) would have shown, and none did. The
completeness sweep: 52 `validity error` statements, 23 `reject-file`, 21
`reject-layer`, 18 `reject-tile`, 21 `ignore-record`, 16 `Writers MUST NOT` and 9
`writers MUST`, each traced to a row or to an explicit textual exemption. The
citation sweep: a regex over the flattened document for every `[FLTR]\d+` token
outside the tables, 28 distinct labels, each read in context — which is how
register-01 surfaced. The limits sweep: all eight guarantee rows and all nine
hard limits compared against their defining sections and against Appendix B. The
arithmetic: four CRC constants recomputed from a CRC-32C implementation
independently validated against §4.5's own check vector, plus the segment-array
sizes at 2³² and 2³⁶, the §15.4 worked example end to end, and the §21.2 reach
derivation re-run from [R-CNT-24]'s four invariants over all 120 rows. Where a
figure could be reproduced, it was, and all of them reproduced.
