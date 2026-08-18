# Round 10 — Register hunter — working transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,919 lines, read in full, in five `Read` calls). I opened no other file, listed
no directory, ran no `git` command, and issued no web request.

Commands run:

- `wc -l spec/tarn.md`
- several `grep -n` / `grep -o` / `awk -F'|'` pipelines over `spec/tarn.md` only
  (row-label extraction, field-count check, instance counting, requirement-ID
  inventory, `§21` back-reference sweep, `verdict` and `descriptive` sweeps)
- three `python3 -c` programs that read **no** files: a CRC-32C implementation
  used to check the document's own constants, and bit arithmetic on DEFLATE /
  zlib / LZ4 headers.

Nothing else. No ADR, no conformance corpus, no registry.json, no PLAN.md, no
prior round's findings.

---

## 1. First pass: what §21 claims about itself

§21.1 is the governing text. The clauses I held the rest of §21 to:

1. **Scope of the register.** "The register — §21.2 through §21.5 (`[R-ERR-02]`)
   — enumerates every detectable file-conformance violation this specification
   names".
2. **Completeness is normative**, gated on *detectability*, with `[R-CNF-07]`
   supplying the gate and §21.7 the account of what fails it.
3. **Precedence.** "each row *restates* its governing rule, and where a row and
   the rule it cites diverge, **the rule governs**."
4. **Scope follows damage**, not severity.
5. **Specialisations** are recorded against the narrower row (F1 of F6 and of
   F8; F35 of F36; L24 of L25).
6. **§21.6–§21.9 are not part of the register** and carry no rows; §21.6's
   entries restate rules on the same terms and the rule governs there too.
7. **Instance arithmetic.** An instance names a field the condition ranges over,
   a container it can occur in, one of several alternatives the condition text
   states, or any combination. A family without a change of shape is one
   instance (T24's *any codec*); members with materially different shapes are
   enumerated (T15, T25). Semicolon-separated; a cell reading `—` is one.
   Crucially: "where a condition is a single predicate over several fields — a
   sum against a bound, a combination of two flag bits — the fields it reads are
   not instances, because no two files could differ."
8. **Detection points** are §19.2's reader tiers or *certification*.
9. **Verifier rows**: the outcome names the scope at which damage is recorded,
   not a reader obligation; for several such rows the governing rule obliges the
   reader to serve the structure unchanged (`[R-SER-08]`, `[R-CNT-22]`).

Note for later: §21.1 carries no requirement identifier of its own. I looked for
this to be a defect and decided it is not — §2.2 (the section that *defines* the
identifier discipline) likewise carries none, so the document's settled
convention is that meta-normative sections are unlabelled. Dropped.

---

## 2. The counting

### 2.1 Rows present, in order, with no gaps

`grep -n '^| [FLTR][0-9]' spec/tarn.md | awk -F'|' '{print $2}'` yields exactly
F1…F36, L1…L49, T1…T26, R1…R10 — 121 rows, in order, no duplicates, no holes.
A field-count check (`awk -F'|' '{print NF}' | sort | uniq -c`) returns `121 8`
for every row, so no Condition or Instances cell contains a stray pipe and the
column split is trustworthy.

### 2.2 Condition counts against the subsection headers

| Subsection | Header claims | Rows counted |
|---|---|---|
| §21.2 file scope | 36 conditions | 36 (F1–F36) ✓ |
| §21.3 layer scope | 49 conditions | 49 (L1–L49) ✓ |
| §21.4 tile scope | 26 conditions | 26 (T1–T26) ✓ |
| §21.5 ignored records | 10 conditions | 10 (R1–R10) ✓ |
| total | — | 121 |

§21.8 states "121 conditions". ✓

### 2.3 Instance counts, per row, by §21.1's own arithmetic

Counted mechanically as `1 + (number of semicolons in the Instances cell)`, which
is exactly the rule §21.1 states ("the count is therefore mechanical once the
cell is written"). Per-row:

```
F1 2  F2 6  F3 2  F4 1  F5 2  F6 2  F7 1  F8 1  F9 1  F10 1
F11 1 F12 1 F13 1 F14 1 F15 1 F16 1 F17 1 F18 1 F19 1 F20 1
F21 1 F22 1 F23 1 F24 1 F25 1 F26 1 F27 1 F28 2 F29 3 F30 2
F31 1 F32 1 F33 5 F34 1 F35 1 F36 1
L1 8  L2 9  L3 1  L4 2  L5 1  L6 1  L7 2  L8 2  L9 2  L10 1
L11 1 L12 1 L13 1 L14 3 L15 4 L16 2 L17 2 L18 3 L19 1 L20 1
L21 1 L22 3 L23 4 L24 1 L25 1 L26 1 L27 1 L28 1 L29 3 L30 1
L31 3 L32 3 L33 4 L34 4 L35 1 L36 2 L37 1 L38 1 L39 3 L40 1
L41 1 L42 1 L43 3 L44 1 L45 3 L46 2 L47 2 L48 1 L49 4
T1 1  T2 1  T3 6  T4 4  T5 1  T6 1  T7 2  T8 1  T9 1  T10 1
T11 2 T12 1 T13 2 T14 1 T15 2 T16 1 T17 1 T18 4 T19 1 T20 1
T21 1 T22 1 T23 1 T24 1 T25 3 T26 3
R1 4  R2 2  R3 2  R4 12 R5 8  R6 4  R7 6  R8 2  R9 2  R10 2
```

Subsection sums, added by hand and re-added:

- §21.2: 2+6+2+1+2+2+1+1+1+1 = 19; +10 (F11–F20) = 29; +7 (F21–F27) = 36;
  +2+3+2+1+1+5+1+1+1 = **53**
- §21.3: 8+9 = 17; +1+2+1+1+2+2+2+1 = 29; +1+1+1+3+4+2+2+3+1+1 = 48;
  +1+3+4+1+1+1+1+1+3+1 = 65; +3+3+4+4+1+2+1+1+3+1 = 88; +1+1+3+1+3+2+2+1+4 = **106**
- §21.4: 1+1+6+4+1+1+2+1+1+1 = 19; +2+1+2+1+2+1+1+4+1+1 = 35; +1+1+1+1+3+3 = **45**
- §21.5: 4+2+2+12+8+4+6+2+2+2 = **44**

**53 + 106 + 45 + 44 = 248.** §21.8 states "248 instances". ✓

Both stated totals reproduce exactly. I re-derived the R4 count independently as
six frame constraints × two containers = 12 (§18.2 names: frame magic; no
skippable frame; no second frame; no nonzero dictionary ID; no content-checksum
flag; and — from R-MTA-09's "the single frame occupying the extent's bytes before
its terminal CRC" — no bytes remaining after the frame), and R5 as two defects
(ill-formed source bytes, unpaired-surrogate escape) × two locations (key, string
value) × two containers = 8. Both match.

Where the cells are *labelled* rather than merely counted, one row does not
survive inspection — L22, see finding register-04.

---

## 3. The document's own constants (arithmetic I actually did)

Not strictly in charter, but L38 and Appendix B both hang off two CRC constants
and Appendix A hangs off a third, so I checked them with a from-scratch CRC-32C
(reflected, poly 0x82F63B78, init/final 0xFFFFFFFF):

- CRC-32C("123456789") = **0xE3069283** ✓ (§4.5 check vector)
- CRC-32C(zero bytes) = **0x00000000** ✓
- CRC-32C of 2¹⁶ sentinel entries (65,536 × `FF×16 00×4` = 1,310,720 bytes) =
  **0xEECB3BB2** ✓ (§15.4, Appendix B, and L38's "the all-sentinel constant
  0xEECB3BB2")
- CRC-32C over Appendix A's trailer bytes [0,60) = **0xE00938D2**, stored little-
  endian as `D2 38 09 E0` ✓ (matches the hex dump's [124,128))

All four reproduce. No finding.

§21.9's note arithmetic also reproduces: 2³² entries ÷ 2¹⁶ per segment × 4 bytes
= 2¹⁸ = 256 KiB ✓; at 2³⁶ that is 2²⁰ × 4 = 4 MiB ✓; 65,536 layers × ~200 bytes
= 13,107,200 = 12.5 MiB ✓; §24's "tens of gigabytes" for a 2³² index region is
2³² × 20 = 85.9 GB ✓.

---

## 4. Row-versus-rule agreement, row by row

I worked the register against the rules rather than narrating it. What follows
records the checks that had a chance of failing.

### 4.1 §6.2's twelve trailer gates against §21.2

`[R-CNT-06]` names, in order: trailer magic → **F8**; trailer CRC → **F14**;
version gate → **F18** (major 0) with an unimplemented major correctly left
un-registered (§21.6's closing paragraph, second structural case); flag gates →
**F19** (incompat lane), with the ignore lane correctly a §21.6 non-violation;
committed_file_length = file size → **F17**; multiple of 64 → **F13**;
dir_offset ≥ 16 → **F9**; dir_length ≥ 4 → **F16**; dir_offset + dir_length ≤
F − 64 → **F10**; 1 ≤ generation → **F11**, ≤ 2⁶³−1 → **F2**'s `generation`
instance; file_id ≠ 0 → **F12**; reserved bytes zero → **F15**. Twelve gates,
twelve rows, no orphan. F3 separately registers the *wrapping* sum, which F10's
comparison cannot see; that split is correct and mirrors L2 at layer scope.

F19 needed a check: is a set incompat bit a *file-conformance* violation at all,
or only a reader-capability refusal like an unimplemented major? §6.3 answers by
contrast — "a set ignore-lane bit is not a file-conformance violation" — and
§4.3/§10.1 confine growth to *ignore*-lane bits, so under format major 1 a set
incompat bit is always a violation and F19 belongs. ✓

### 4.2 §15.3's classification table against §21.4

§15.3 has eleven rows; six are marked *structural*, and I counted the marks: rows
2–7 exactly. The mapping:

| §15.3 row | register |
|---|---|
| valid sentinel | §21.6 non-violation ✓ |
| S/S with crc ≠ 0 | T6 |
| exactly one of offset/length = S | T7 |
| length = 0 (non-sentinel) | T10 |
| offset < 16 (non-sentinel) | T8 |
| offset or length > 2⁶³−1 | T11 |
| sum overflows, or > F−64 | T12 and T9 (one §15.3 row, two register conditions) |
| stored bytes fail crc | T1 |
| intra-layer overlap | L18 (reject-layer) |
| overlap outside own layer | F33 (reject-file) |
| alignment / slab invariant | L40, L41, L42 |

T11's qualifier — "the value being distinct from the all-ones sentinel" — is what
keeps T11 disjoint from T6/T7, and it agrees with `[R-IDX-02]`'s "`[R-ENC-03]`'s
value-domain rule and `[R-ENC-04]`'s sum rule apply to the fields of non-sentinel
entries only". Good.

The structural/well-formed distinction propagates correctly in three places that
must agree, and does: §15.3 ("its extent stands and it keeps its place in the
*verifier* rows, in run continuity, and in the coverage walk"), §16.2's
`[R-SLB-03]` ("An entry whose only defect is that its stored bytes fail its crc
is not transparent"), §9.7's `[R-LIF-08]`, and L41's parenthetical ("sentinels
and entries §15.3 classifies reject-tile on a structural ground are transparent,
an entry failing only its stored bytes' crc is not"). Four statements, one
meaning. No finding.

I also checked that no *cross-check* row is mistakenly treated as structural.
T14 (codec 1, entry length ≠ decoded size) leaves the entry well-formed — its own
20 bytes yield a usable extent — so its extent must stand in the coverage walk
and in run continuity. §15.3's table does not list T14's condition, which is
exactly right. ✓

### 4.3 §7.4's constraint table against §21.3

Every constraint in §7.4's inline-payload table has a row: name (L3/L5/L6 for the
layer name at file-open, L4/L7/L8/L9 for dimension and channel names at layer
access, F4 for layer-name uniqueness at file scope), layout L36, linearization
L33, codec L43, filter L45, alignment L39, slab S domain L1, A_slab L28/L29,
rank/C/T floors L32, extents and tile extents L1, channel type L34, fill length
L30, bool fill L35, index_encoding L31, entry_count L21/L1, extent_length formula
L22, crc_of_crc_array L27/L37, sub-records L10–L14/L19/L24–L26/L46/L47/L49, and
the mutual exclusion L20. `[R-CNT-23]`'s own "including" list is a subset of
these; its omission of *linearization* is harmless because `[R-GEO-05]` states
its own reader rule and L33 cites it.

The scope split between the F-rows and the L-rows is consistent throughout: every
F-row that could collide with a layer record says "non-layer top-level" (F2, F3,
F25, F26, F28, F30, F31, F32) and the layer-scope twin exists (L1, L2, L46, L47,
L49, L15, L16, L17). The one row that deliberately does *not* say "non-layer" is
F29, and that is right: `[R-CNT-12]` puts a framing failure of the directory's
top-level sequence at the sequence's owning scope — file — even for a layer
record. L14 is the sub-record twin.

### 4.4 The twenty verifier rows

F7, F25, F26, F27, F28, F33, F36 (7); L18, L25, L40, L41, L42, L46, L47, L48,
L49 (9); T2, T4, T5, T26 (4). I checked each against a *verifier* MUST in the
cited rule:

- `[R-CNT-05]` "A verifier MUST treat a structure in that gap as a validity error
  at file scope" → F7 ✓
- `[R-CNT-12]` "a verifier MUST treat a nonzero reserved flag bit or the MU = 1
  with PE = 0 combination as a validity error at the record's governing scope" →
  F25, F26, L46, L47 ✓ (governing scope: file for other top-level records, layer
  for a layer record and for sub-records, per `[R-CNT-13]` — which is why L46/L47
  cite R-CNT-13 as the secondary)
- `[R-CNT-13]` "a verifier MUST treat an intra-layer overlap … as reject-layer,
  and any overlap across layers or touching another scope's structures as
  reject-file" → L18, F33 ✓
- `[R-CNT-15]` "a verifier MUST treat a reserved-range record type as a validity
  error at the record's governing scope" → F36, L25 ✓
- `[R-CNT-22]` "a verifier MUST treat the mismatch as a validity error" → F28,
  L49 ✓
- `[R-MTA-05]` "the file is nonconforming, a verifier MUST report it, and readers
  process the document unchanged" → F27, L48 ✓
- `[R-SLB-01]` / `[R-SLB-03]` "A verifier MUST check the invariant (violation:
  reject-layer, §15.3)" → L40, L41, L42 ✓
- `[R-SER-08]` "its assigned detector is the verifier, for which it is a validity
  error at tile scope" → T2 ✓
- `[R-SER-05]` "a verifier MUST check it, and a violation is a validity error at
  tile scope" → T4, T5 ✓
- `[R-COD-10]` "a verifier detects it as a validity error at tile scope" → T26 ✓

All twenty agree with their rule on detector *and* scope. §21.1's remark that
"for several such rows [the rule] obliges the reader to serve the structure
unchanged (`[R-SER-08]`, `[R-CNT-22]`)" is accurate: R-SER-08 fixes what a
non-detecting reader returns for the bad bool byte, and R-CNT-22 obliges a reader
to apply the type's fixed semantics regardless of the stored bits.

§21.5 contains no verifier row, which is right — the two verifier-detected
user-metadata violations are the *sorted-members* ones, and those do not make the
document unreadable, so they sit in §21.2/§21.3 instead. §21.6's closing
paragraph documents that move explicitly and it is coherent.

### 4.5 Detection tiers against §19.2

The tiers that could have been wrong, and were not:

- **L37/L38 at "tile use" with outcome reject-layer.** §19.2 anticipates exactly
  this: "index-chain failures take layer scope (`[R-IDX-04]`) although their
  detection point is tile use". ✓
- **L3/L5/L6 at "open" with outcome reject-layer.** §19.1 step 4 puts layer-name
  parsing and §4.6 checking in the open, and §19.3's layer-access list pointedly
  omits the layer record's own name while listing dimension and channel names.
  The two sections agree. ✓
- **R1 at "open (top-level); layer access (sub-record)".** The encoding byte lives
  in the record's inline payload, which the open's record walk holds. §19.1 step
  4's enumeration does not name the encoding *value*, but §19's preamble
  forecloses the objection: "Those enumerations are not the complete inventory of
  what a reader detects at that tier: §21's register is". ✓
- **R2–R10 at "extent use"**, matching §19.2's fourth tier "no earlier, since the
  open fetches no extent". ✓

One tier I probed hard and cleared: **L23 vs §19.1**. §19.1 makes a reader
determine at *open* whether a layer record's name field "lie[s] entirely within
that record's inline_length", which is an L23 instance, while L23's Detected cell
says "layer access". I constructed the discriminating case — a file with layer A
whose name field overruns and a valid layer B — and both readings serve B and
serve nothing of A, and a verifier reports nonconforming either way. §19.2 makes
Detected the *latest* point and licenses earlier detection, so nothing forks. No
finding.

I also cleared the ordering question between **F4 and L3/L5/L6**: a file whose
two layer records carry byte-identical *ill-formed* name bytes exhibits both a
file-scope and a layer-scope condition. §19.1 settles the precedence explicitly —
"Uniqueness is decided first, and over the raw name bytes whether or not each
name is itself well-formed" — so the verdict is reject-file, deterministically.
§21 does not restate the precedence, but §21.1 says rows restate rules and rules
govern, so the silence is licensed. No finding.

---

## 5. Completeness, both directions

### 5.1 Rules → rows

I inventoried every `[R-…]` identifier (150 of them, one of which — `R-ENC-100` —
is §2.2's illustrative example, not a requirement) and walked the ones that could
generate a file-level witness. Every MUST-level, file-affecting rule resolves to
at least one row. The interesting negatives, i.e. rules with no row, all have an
explicit account somewhere:

- **`[R-CNT-02]`'s "belongs to no class" half** — §5.2's Note: "a register row
  for it would be a row no file could exhibit". Only disjointness is testable,
  and that is F33/L18. ✓
- **`[R-LIF-04]` residue past a completed commit** — §9.5's Note: the observable
  state is already F8/F14/F17 and `[R-LIF-05]` forbids scanning backward. ✓
- **`[R-SLB-04]` stale slab declaration** — §16.2's Note: "every file exhibiting
  one exhibits a run whose tiles are unpacked or whose first stored tile is
  misaligned, which §21.3 registers", i.e. L41/L42. I tested the note's claim
  against the vacuous case (a commit that makes every tile of a run a sentinel):
  R-SLB-03 says "A run with no stored tiles imposes nothing", so the writer has
  vacuously re-established the invariants and there is no violation to register.
  The note holds. ✓
- **`[R-CNT-18]`'s nesting prohibition** — §7.4's Note: no reader-detectable
  witness in major 1; the one detectable neighbour, a layer record appearing as a
  sub-record, is L26. ✓
- **`[R-LIF-01]`, `[R-LIF-03]`, `[R-GEO-06]`, `[R-SER-01]`, `[R-CNT-13]`'s
  embedded-offset prohibition** — §21.7's second class. ✓
- **`[R-COD-10]` mis-stride and `[R-COD-06]` undisclosed dictionary** — §21.7's
  first class, narrowed by T26/T2/T4 where content is structurally constrained. ✓
- **`[R-MTA-06]`'s unregistered `tarn.` key** — expressly conforming (§18.3), and
  §2.3's `[R-CNF-02]` names §18.3 as a conduct rule. §21.6 has the row. ✓
- Every SHOULD (`[R-CNT-03]`, `[R-CNT-09]`, `[R-CNT-26]`, `[R-ENC-14]`,
  `[R-LIF-07]`, `[R-TYP-10]`, `[R-MTA-07]`, R-COD-06's window advice, R-MTA-04's
  binary64 advice) has no row, as `[R-CNF-12]` requires: "§21's register
  enumerates MUST-level conditions only". I checked every register row for a
  SHOULD-level governing clause and found none. ✓

One rule I could not find accounted for anywhere: `[R-LIF-02]` step 3's
"each commit appends its own complete directory", whose violation §9.2's Note
describes ("A writer that re-points a new trailer at a prior generation's
directory region has left step 3 unperformed") and which has no single-file
witness. §21.7's second paragraph names a *class* ("properties of a file's
history, which §9.7 does not reconstruct") rather than an exhaustive list, and
this falls inside that class, so I did not raise it.

### 5.2 Rows → rules (does any row register a non-violation?)

Checked individually for F6, F7, F19, F27, F28, F35, F36, L44, L48, L49, T2, T13,
T26, R1. All are MUST-level violations under their cited rules. The one that took
work was **R1**: encoding 0 is "0 is invalid" (§18.2) and reserved 3–0x7F is
"a value from a reserved range MUST NOT be emitted at all" (§10.3) — both
violations — while the *experimental* range ≥ 0x80 is correctly parked in §21.6
as a non-violation, since §10.3's prohibition binds conduct rather than bytes
(`[R-CNF-02]`). The split is exactly right and matches `[R-EXT-03]`'s closing
clause.

### 5.3 Outcome vocabulary

§2.4 defines four reader outcomes plus **preserve-verbatim** as an updater
obligation. §21.2/§21.3/§21.4/§21.5 use exactly reject-file / reject-layer /
reject-tile / ignore-record, one per subsection, no row states an outcome of its
own, and all four defined reader outcomes are reachable. preserve-verbatim
correctly has no register subsection — it is not a reader outcome, and §2.4
points at §20.4's table for its two cases, which exist there. ✓

---

## 6. Every cross-reference to a row

I swept the whole document for row labels and resolved each against the row it
lands on.

| Citation | Site | Lands on | Verdict |
|---|---|---|---|
| "§21.2 rows F8 and F17" | §9.6 (`[R-LIF-06]`) | trailer magic; committed_file_length vs transport size | ✓ exactly the two gates a torn tail fails |
| "(§21.4, T24)" | §17.2 deflate Note | "bytes remain in the stored extent after the stream … ends" | ✓ |
| "F1 of F6 and of F8, F35 of F36, L24 of L25" | §21.1 | see below | ✓ |
| "T24's *any codec*" | §21.1 | T24's Instances cell reads `any codec` | ✓ |
| "(T15, T25)" | §21.1 | T15 has 2 enumerated shapes, T25 has 3 | ✓ |
| "F9/F10, F31/F32, L16/L17 and T8/T9" | F33 | dir bounds; top-level extent bounds; layer/sub-record extent bounds; tile extent bounds — all four tiers | ✓ |
| "the two rows together covering `[R-SER-08]`" (T2→T4) | T2 | T4 covers the padding-position bool byte | ✓ |
| "the check that detects it is T25's" | T13 | T25 = malformed stream fails to decode | ✓ |
| "the check that detects it is T2's or T4's" | T26 | ✓ |
| "(F36, L25)" | §21.6 experimental-type row | reserved-range emission, verifier, both scopes | ✓ |
| "(F18, `[R-CNT-07]`)" | §21.6 closing | version_major = 0 | ✓ |
| "(F35, F36, L24, L25)" | §21.6 closing | reserved-range type at both scopes, both detectors | ✓ |
| "(`[R-CNT-05]`, F7)" | Appendix H verifier | structure in the pre-trailer gap | ✓ |
| "(`[R-CNT-15]`, F36, L25)" | Appendix H verifier | ✓ |
| "which §21.3 registers" | §16.2 Note | L41, L42 — both in §21.3 | ✓ |
| "§21.3 registers in its own right" | §7.4 Note | L26 — in §21.3 | ✓ |
| "each of which §21.2 already registers" | §9.5 Note | magic F8, CRC F14, size F17 — all in §21.2 | ✓ |
| "(`[R-GEO-02]`, §21.6)" | §17.2 lz4 Note | §21.6's zero-extent row | ✓ |
| "§21.6" for the unrecognised-key case | §18.4 | §21.6's `tarn.`-key row | ✓ |

Verifying the three specialisations claimed in §21.1:

- **F1 of F6.** F1's front-block instance is bytes [0,8) stored byte-reversed:
  `1A 0A 0D 4E 52 41 54 89`, which is by construction not byte-identical to the
  constant, so F6 fires too and F1 is the narrower row. ✓
- **F1 of F8.** The reversed trailer magic is not `8A 4E 52 41 54 0D 0A 1A`. ✓
- **F35 of F36.** A reserved-range type with MU = 1 is a reserved-range type. ✓
  (and the narrowing matters: F35's detector is *reader* at open, F36's is
  *verifier* at certification, which is what §21.1's "whose detector and
  detection point are the ones that apply" is for)
- **L24 of L25.** Same shape at layer scope. ✓

Every row citation in the document resolves to a row that says what the citing
text claims. **Zero cross-reference defects.** Given the brief's warning that
§21.2/§21.3 had been wholesale re-labelled, this is the result I most expected to
break, and it did not.

---

## 7. Limits, both directions

### 7.1 §21.9's minimum-guarantee table against every other statement

| §21.9 row | restated elsewhere | agreement |
|---|---|---|
| rank 32 | Appendix B | ✓ |
| C 4096 | Appendix B | ✓ |
| entry_count 2³² | Appendix B; §1 pillar; Appendix D; §24's `[R-VEC-03]` | ✓ |
| 65,536 layers | Appendix B | ✓ |
| dir_length 16 MiB | Appendix B | ✓ |
| decoded tile 256 MiB | Appendix B | ✓ |
| metadata document 16 MiB | Appendix B; §18.2's `[R-MTA-09]` and its Note ("The 16 MiB figure is a §21.9 minimum guarantee") | ✓ |
| zstd Window_Size 8 MiB | Appendix B; §17.2's `[R-COD-06]` ("§21.9's 8 MiB `Window_Size` guarantee") | ✓ |

No divergence in either direction, and `[R-ERR-04]`'s "at the whole file, or at
the narrowest scope whose declarations exceed what it can serve, a layer or a
tile" is used consistently by §2.3 (reader and verifier clauses), §17.2, and
§18.2's Note — including §18.2's careful observation that a document has no
declared size and so no narrower scope, which forces a whole-file decline.

### 7.2 Hard limits: `[R-ERR-05]`'s list against the defining sections

Checked each of the ten collected hard limits against its defining section: name
≤ 255 (§4.6) ✓; user-metadata key ≤ 255 (§18.2's `[R-MTA-04]`) ✓; rank ≤ 255 and
C ≤ 65,535 (§7.4's u8/u16) ✓; codec 4 at ≤ 0x7E000000 (§17.2) ✓; value domain
2⁶³−1 (§4.2) ✓; A a power of two 512…2⁶² (§16.1) ✓; A_slab a power of two 1…2⁶²
(§7.4, §16.2) ✓; S in 1…2⁶³−1 — §16.2 states only "S ≥ 1" and the upper bound
comes from §7.4's table, so the "(§16.2, `[R-CNT-23]`)" citation is carried by
`[R-CNT-23]`, which is right; directory ≥ 4 bytes at offset ≥ 16 (§6.2) ✓; file
≥ 128 bytes (§5.1) ✓. Appendix B restates all of them consistently.

I also checked the taxonomy claim that follows the list — "Most follow from a
field's width, an external format, or the value domain, and the rest from
arithmetic over structures a generation cannot omit. One does not: the 512 floor
on A". The 2⁶² ceilings do follow from the value domain (2⁶² is the largest
power of two ≤ 2⁶³−1), so the "one chosen number" claim holds. ✓

**But the collection is not complete.** See finding register-03: §7.1 forces a
user-metadata extent to be at least 5 bytes, a validity-affecting minimum of
exactly the same species as "a directory of at least 4 bytes", and it is not
collected here, against `[R-ERR-03]`/`[R-CNF-10]`'s "Every limit affecting which
files are valid … lives here".

---

## 8. Where I had to guess, and what I found there

### 8.1 T15: a reader detector with no procedure — the finding I care about

This is the one place where I could not implement §21 without inventing something
the document does not state, and where the invention changes accept/reject on a
*conforming* file.

T15 reads:

> | T15 | Codec 2 (deflate) and the stored bytes carry a wrapper rather than a raw
> RFC 1951 DEFLATE stream | zlib RFC 1950 (CMF/FLG header + trailing Adler-32);
> gzip RFC 1952 member (1F 8B, trailing CRC32+ISIZE) | reader | tile use |
> `[R-COD-05]` |

Its governing rule, in full, is:

> **Codec 2 — deflate.** The stored bytes are exactly one DEFLATE compressed data
> stream as defined by RFC 1951 — raw, not a zlib (RFC 1950) or gzip (RFC 1952)
> wrapper. `[R-COD-05]`

That is the whole of `[R-COD-05]`. It binds the file and states **no reader-side
clause and no detection procedure** — which is itself against the phrasing
discipline §2.1's Note announces ("every writer-side prohibition is paired with
an explicit reader-side clause stating what a reader does with a violating
file"). The register nonetheless assigns Detector = *reader*, and `[R-CNF-04]`
makes that assignment binding: "A reader MUST detect every violation the error
register (§21) assigns to the reader as its detector."

So a reader must detect "carries a wrapper". How? The document offers two
readings and picks neither:

**Reading A — T15 records a cause, and the check is T3's/T24's/T25's.** A
wrapper is caught because the raw-DEFLATE decode fails, or does not consume the
extent exactly, or produces the wrong length. This is what the document does for
T13 ("the check that detects it is T25's, and this row records the cause rather
than a procedure of its own") and for T26 ("the check that detects it is T2's or
T4's"). T15 carries no such annotation.

**Reading B — T15 is a check of its own, on the wrapper's header.** T15's
Instances cell all but says so: it names *headers* — "zlib RFC 1950 (CMF/FLG
header …)" and "gzip RFC 1952 member (1F 8B …)" — and a header is the only thing
about a wrapper that is inspectable before decoding.

Under Reading B the implementer writes the standard zlib-header test: CM = 8,
FDICT clear, and `(CMF<<8 | FLG) mod 31 == 0`. I checked that this test has
**conforming false positives**:

- `0x78 0x9C` passes the zlib test: CM = 8, CINFO = 7, FDICT = 0, and
  0x789C = 30,876 = 31 × 996, so the mod-31 check passes. (Computed.)
- The same two bytes are a legal opening of a **raw** RFC 1951 stream. 0x78 =
  0b0111_1000, so bit 0 (BFINAL) = 0 and bits 1–2 (BTYPE) = 0b00 = *stored
  block*. RFC 1951 then says to skip the remaining bits of the current byte —
  and fixes no value for them — after which LEN and NLEN follow at bytes 1–4.
  With LEN = 0x009C = 156 and NLEN = 0xFF63 = ~156, the byte string
  `78 9C 00 63 FF <156 literal bytes> 01 00 00 FF FF` is exactly one raw RFC 1951
  DEFLATE stream decoding to 156 bytes and consuming its extent exactly. (I
  verified the bit decomposition and the complement.)

So a tile payload beginning `78 9C` can be fully conforming under `[R-COD-05]`,
`[R-COD-08]` and `[R-SER-07]`.

The fork: **Implementation A** (Reading A) decodes the tile and returns its
samples. **Implementation B** (Reading B) sees a valid zlib header, fires T15,
and reports reject-tile. Same bytes, opposite verdicts, on a file that is
conforming. This is not a nonconforming-file case where `[R-CNF-12]` licenses
either behaviour; `[R-CNF-03]` obliges acceptance, so exactly one of them is
right — and the document never says which, because it never says how a reader
detects a wrapper.

I tested whether the same trap exists for T15's gzip instance and for T23, and it
does not, which is worth recording because it shows the defect is specific:

- gzip's `1F 8B`: 0x1F = 0b0001_1111 → BFINAL = 1, BTYPE = 0b11, which RFC 1951
  reserves as invalid. No conforming raw stream can begin `1F 8B`, so a
  magic test on gzip has no false positives.
- T23's LZ4 frame magic `04 22 4D 18`: as a raw LZ4 block the token 0x04 means
  zero literals and a match of length 8 at offset 0x4D22 = 19,746, with zero
  bytes of output produced — always invalid. No conforming block can begin with
  those four bytes, so T23's magic test is sound.

Only the zlib instance of T15 admits a conforming prefix collision, and it is the
one the Instances cell names by its header.

T16 is the same shape without the teeth: "Codec 2 (deflate) and the stored extent
holds more than one DEFLATE stream — a second stream begins after the BFINAL
block" is, operationally, T24 ("bytes remain in the stored extent after the
stream, frame, or block ends") specialised to codec 2, and both are reader /
tile use / reject-tile, so nothing forks. I mention it only because it is a
second unannotated row whose rule (`[R-COD-05]`) states no reader clause.

### 8.2 §21.8's "verdict"

§21.8 reads:

> Every row of §21.2 through §21.5 — 121 conditions over 248 instances — has at
> least one conformance vector (§24) whose **expected verdict is that row's
> outcome**, and one vector per instance.

"Verdict" is a defined term with a closed three-valued range. §2.3: "A verifier
reports one of three verdicts: *conforming*, *nonconforming*, or *cannot
establish*". A row's *outcome* is reject-file / reject-layer / reject-tile /
ignore-record (§2.4, `[R-CNF-07]`) — none of which is a verdict. And §24 states
the opposite of §21.8's identification: "every vector built from §21's register is
nonconforming" (`[R-VEC-04]`), i.e. every such vector's *verdict* is
`nonconforming`, uniformly, and never its row's outcome. §24's own manifest
requirement uses the right word — "the outcome class (§2.4), the scope, and the
§21 register row it exercises" (`[R-VEC-02]`).

I swept every occurrence of "verdict" in the document: nine of the ten uses are
the verifier's three-valued report; line 3298 (§21.8) is the sole misuse. This is
a genuine contradiction between §21.8 and §2.3/§24, though it changes no bytes —
a corpus builder following §24's explicit manifest schema is unaffected.

### 8.3 L22's instance labels

L22:

> | L22 | Under index_encoding 1, extent_length ≠ entry_count × 20 +
> ⌈entry_count/2¹⁶⌉ × 4 — including slot (0,0) with entry_count > 0, or a nonzero
> slot with entry_count = 0 | extent_offset; extent_length; entry_count | reader |
> layer access | `[R-CNT-17]` (R-ENC-07, R-CNT-20) |

The count (3) reproduces mechanically, and three distinguishable files do exist:
(a) entry_count = 5 with extent_length ≠ 104; (b) entry_count = 5 with slot
(0,0); (c) entry_count = 0 with a nonzero slot. But the cell names *fields*, and
the equality it registers is a single predicate over `extent_length` and
`entry_count` only — `extent_offset` is not read by it at all. §21.1 is explicit
that this is not how instances are named: "where a condition is a single
predicate over several fields — a sum against a bound, a combination of two flag
bits — the fields it reads are not instances, because no two files could differ."

Contrast the rows that get this right. F30 names `extent_offset; extent_length`
but its condition text spells the two alternatives out ("offset 0 with length !=
0, or offset != 0 with length 0"), so the field names are shorthand for
alternatives. F10, whose condition is likewise a single predicate over two
trailer fields, correctly reads `—`, one instance. L22 has three genuine
alternatives in its condition text and names three fields that do not line up
with them, so a corpus builder obliged by `[R-ERR-02]` to produce "one vector per
instance" cannot tell which three files are wanted.

I considered and rejected a parallel complaint about R8 ("A user-metadata
document contains a non-finite number, in any form", two instances = two
containers). Its condition text collapses an overflowing literal such as `1e400`
and the bare tokens `NaN`/`Infinity` into one family, which is the pattern §21.1
blesses for T24's *any codec*; and the bare-token case also lands on R7, which
`[R-VEC-02]` handles ("the entry records every row the file exercises and says
which it was built for"). Not a defect.

### 8.4 Things I looked at and cleared

Recorded so a checker knows they were examined rather than missed:

- **§21.5's header** — "every way its document can be unreadable lands here" is
  loose (an experimental-range encoding and an over-bound `[R-MTA-09]` decline are
  ways a document can be unreadable that land in §21.6 and nowhere), but the very
  next clause corrects it: "§21.6 lists the ignore-record conditions that are not
  violations". Not a defect.
- **§21.6's zero-layer row** — "A conforming file with an empty directory"
  conflates "no layer records" with "empty directory" (a zero-layer file may
  carry a file-scope user-metadata record). `[R-CNT-14]` governs and is clear;
  §21.1's precedence clause covers the looseness. Not raised.
- **§21.6's trailer-mimic row** — justified as "nothing enumerates slack", though
  the stated condition is a mimic *in a payload*, which is live state, not slack.
  §6.2's Note and `[R-SEC-04]` between them say the operative thing (nothing
  enumerates the file for trailer magic at all). Not raised.
- **§21.1's lack of a requirement identifier** — dropped, because §2.2, the
  section that defines the identifier discipline, likewise carries none; the
  document's convention is that meta-normative sections are unlabelled.
- **Appendix H's verifier checklist** names "padding samples" where the writer
  checklist names "edge padding and pad bits", so T5's pad-bit obligation is
  implicit there. Appendix H is non-normative and cites §14.5, which carries the
  pad-bit rule. Not raised.
- **T13, T15, T16, T23's governing rules being file-binding rather than
  reader-binding** — cleared for T13 (annotated), T16 and T23 (no conforming
  false positives), raised only for T15.

---

## 9. Findings

### register-01 — AMBIGUITY — §21.4 T15, §17.2 `[R-COD-05]`, §2.3 `[R-CNF-04]`

**T15 obliges a reader to detect a DEFLATE wrapper but states no procedure, and
the header test its Instances cell points at rejects conforming bytes.**

Quotation (T15's Condition and Instances cells, §21.4):

> Codec 2 (deflate) and the stored bytes carry a wrapper rather than a raw RFC
> 1951 DEFLATE stream | zlib RFC 1950 (CMF/FLG header + trailing Adler-32); gzip
> RFC 1952 member (1F 8B, trailing CRC32+ISIZE) | reader | tile use | `[R-COD-05]`

and its governing rule in full (§17.2):

> **Codec 2 — deflate.** The stored bytes are exactly one DEFLATE compressed data
> stream as defined by RFC 1951 — raw, not a zlib (RFC 1950) or gzip (RFC 1952)
> wrapper. `[R-COD-05]`

Permitted readings, and the fork, are set out in §8.1 above. Reading A (T15
records a cause; the check is T3/T24/T25's, as T13 and T26 say of themselves)
accepts `78 9C …`; Reading B (T15 is a header check, as its Instances cell
implies) rejects it. I pick **Reading A**, because `[R-CNF-03]`'s acceptance duty
plus `[R-COD-05]`'s own definition make the `78 9C` stream conforming, so any
detector with conforming false positives must be wrong. But the text never says
so, and the row's own instance labels point the other way. The repair is one
clause of the kind T13 already carries.

**Byte-level: yes.** Implementation A returns the 156 samples of a tile whose
stored bytes are `78 9C 00 63 FF <156 bytes> 01 00 00 FF FF`; Implementation B
reports reject-tile for it. The file is conforming, so this is not
`[R-CNF-12]`'s licence to reject a nonconforming file — it is two readers
disagreeing about a conforming file's tile.

### register-02 — CONTRADICTION — §21.8 `[R-ERR-02]` vs §2.3 `[R-CNF-11]` and §24 `[R-VEC-04]`

Quotations in §8.2 above. §21.8 says a vector's "expected verdict is that row's
outcome"; §2.3 closes the verdict vocabulary to three values, none of which is an
outcome; §24 says every vector built from the register is *nonconforming*, i.e.
the verdict is constant across all 121 rows and is never the row's outcome.

**Byte-level: no.** §24's `[R-VEC-02]` states the manifest schema in the correct
vocabulary, so a corpus built to §24 is unaffected.

### register-03 — CONTRADICTION — §21.9 `[R-ERR-03]`/`[R-ERR-05]` vs §7.1 `[R-CNT-25]`

`[R-ERR-03]`: "Every limit affecting which files are valid, or which files a
conforming reader accepts, lives here (`[R-CNF-10]`)." `[R-ERR-05]` then collects
the hard limits, and the collection includes the closely parallel "a directory of
at least 4 bytes at an offset of at least 16 (§6.2, `[R-CNT-06]`)".

§7.1 states a hard limit the collection omits: "An extent of (0, 0) on a
user-metadata record, or one whose extent_length is less than 5 — too short to
hold both a document and the terminal CRC-32C §8.1 places in its final 4 bytes —
is a validity error at its containing scope." It is arithmetic over a structure's
own terminal CRC, exactly as dir_length ≥ 4 is, it affects which files are valid,
and it is registered twice (F22 at file scope, L11 at layer scope) — so the
register treats it as a limit while §21.9 does not collect it.

A second, weaker omission of the same kind: `[R-CNT-18]`'s "nesting depth beyond
two is a validity error at layer scope" is a structural bound on validity and is
not collected either, though §7.4's Note explains it has no reader-detectable
witness in format major 1.

**Byte-level: no.** §7.1 states the rule normatively and F22/L11 register it, so
every implementation rejects a 4-byte user-metadata extent regardless.

### register-04 — AMBIGUITY — §21.3 L22 vs §21.1's instance rule

Quotations and analysis in §8.3 above. L22's Instances cell reads
`extent_offset; extent_length; entry_count`; its condition is a single equality
over `extent_length` and `entry_count`, and §21.1 says the fields a single
predicate reads are not instances. The three readings a corpus builder can defend
are: (i) the three named fields, which cannot each be a distinguishable file
because the equality does not read `extent_offset`; (ii) the three alternatives
the condition text actually states — a plain length mismatch, slot (0,0) with
entry_count > 0, and a nonzero slot with entry_count = 0; (iii) a single instance,
by the F10 precedent for a single predicate over two fields, which would make the
subsection total 104 and the document total 246. I pick **(ii)**: it is the only
reading under which all three named files are distinguishable and the stated 248
still reproduces. The cell should name those alternatives rather than fields.

**Byte-level: no.** It bears on corpus construction under `[R-ERR-02]`, not on
any implementation's bytes or verdicts.

---

## 10. What reproduced, and confidence

- 121 conditions and 248 instances both reproduce exactly, per subsection and in
  total, under §21.1's own arithmetic.
- Every one of the 19 row citations in the document resolves to a row that says
  what the citing text claims — no mis-landed label survives the re-labelling.
- All 20 verifier rows agree with their rule on detector and on scope.
- All 12 of `[R-CNT-06]`'s gates, all 11 of §15.3's classification rows, and
  every constraint in §7.4's table have rows; the five rules with no row each
  have an explicit account in the text.
- All four defined reader outcomes are reachable and no row uses an undefined
  one.
- §21.9's eight minimum guarantees agree with every restatement; its ten hard
  limits agree with their defining sections; one hard limit is missing from the
  collection.
- Four of the document's own constants (two CRC check vectors, the all-sentinel
  segment CRC, Appendix A's trailer CRC) recompute correctly.

I would rate confidence in interoperating from this text **high**, with the one
reservation that a reader implementing T15 literally will reject a class of
conforming tiles.

**Transcript finding count: 4.**
