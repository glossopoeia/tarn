# Round 25 — Register hunter — working transcript

Charter: audit §21, the error-handling register, against the rules it restates
and against itself.

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in full, in six `sed` ranges. I ran `grep` against that file only, and one
`python3` script that reads no files (a CRC-32C implementation, to check the
document's stated checksum constants), plus two `python3` scripts that parse the
register tables out of that same file to count rows and instances mechanically.
I opened no ADR, no `docs/`, no `conformance/`, no `spec/registry.json`, no
`PLAN.md`, no `AGENTS.md`, no git history. I listed no directories. I wrote this
transcript and read nothing from its directory.

**Context I did not ask for.** My runtime placed material in context before I
began: a project instruction file pointing at `AGENTS.md`, and an index of the
maintainer's memory files with one-line descriptions naming things like a working
cadence, a gate board, and a register/corpus relationship. I did not open any of
it and I have not used any of it as evidence. It is disclosed here because it
appeared, not because I acted on it. The spec was where the brief said it would
be (`spec/tarn.md`); no path surprise.

One further contamination hazard I want to name because I noticed it and had to
discount it deliberately: the session's opening `gitStatus` block printed recent
commit *subject lines*, and one of them names a requirement identifier that falls
inside my charter. I did not open the commit, and I re-derived my conclusion about
that row from §18.2 and §21.1 alone; the conclusion I reached was that the row is
**not** defective, which is the opposite of what the subject line would have
nudged me toward, so I am reasonably confident the nudge did no work. It is
disclosed because it appeared.

Method: read the whole document cold first (§1 through Appendix H), then §21 four
more times, then mechanical extraction of the register tables.

---

## 1. Arithmetic first, because it is the only mechanical check

### 1.1 The document's CRC constants

I implemented CRC-32C (Castagnoli, reflected, init 0xFFFFFFFF, final XOR
0xFFFFFFFF) from §4.5's parameters alone and checked every constant the document
states:

| Stated where | Constant | Reproduced |
|---|---|---|
| §4.5 check vector | CRC-32C("123456789") = 0xE3069283 | yes |
| §4.5 check vector | CRC-32C(zero bytes) = 0x00000000 | yes |
| §7.4 example | segment CRC over 80 sentinel bytes = 0x80A34955 | yes |
| §7.4 example | crc_of_crc_array = 0xC4EE982E | yes |
| §15.4, Appendix B | full all-sentinel segment = 0xEECB3BB2 | yes |
| Appendix A | trailer CRC over [0,60) = 0xE00938D2 | yes |

For Appendix A I rebuilt the 60 trailer bytes from the table's field values
(magic, version_major 1, version_minor 0, flags 0, generation 1, dir_offset 16,
dir_length 4, committed_file_length 128, file_id 0x0123456789ABCDEF, reserved 0)
and got `d2 38 09 e0`, matching the hex dump at [124,128). Every stated constant
reproduces. No finding.

### 1.2 Row counts

Extracted every table line matching `^\| [FLTR]\d+ \|`:

- §21.2 — 36 rows (F1…F36). Header states "36 conditions". ✓
- §21.3 — 49 rows (L1…L49). Header states "49 conditions". ✓
- §21.4 — 26 rows (T1…T26). Header states "26 conditions". ✓
- §21.5 — 10 rows (R1…R10). Header states "10 conditions". ✓
- Sum 121. §21.8 states "121 conditions". ✓

### 1.3 Instance counts

§21.1 fixes the arithmetic: "Instances within a cell are separated by semicolons,
and a cell reading — is one instance; the count is therefore mechanical once the
cell is written." Applying exactly that:

- §21.2: 58 instances
- §21.3: 116
- §21.4: 55
- §21.5: 48
- **Total 277.** §21.8 states "277 instances". ✓

Per-row counts (mine, for anyone who wants to check the split):

```
F1 2  F2 6  F3 2  F4 1  F5 2  F6 2  F7 4  F8 1  F9 1  F10 1
F11 1 F12 1 F13 1 F14 1 F15 1 F16 1 F17 2 F18 1 F19 1 F20 1
F21 1 F22 1 F23 2 F24 1 F25 1 F26 1 F27 1 F28 2 F29 3 F30 2
F31 1 F32 1 F33 5 F34 1 F35 1 F36 1                        = 58
L1 8  L2 9  L3 1  L4 2  L5 1  L6 1  L7 2  L8 2  L9 2  L10 1
L11 1 L12 2 L13 1 L14 3 L15 4 L16 2 L17 2 L18 3 L19 1 L20 1
L21 4 L22 4 L23 4 L24 1 L25 1 L26 1 L27 1 L28 1 L29 3 L30 2
L31 3 L32 3 L33 4 L34 4 L35 1 L36 2 L37 1 L38 1 L39 3 L40 1
L41 3 L42 1 L43 3 L44 3 L45 3 L46 2 L47 2 L48 1 L49 4       = 116
T1 1  T2 1  T3 6  T4 4  T5 1  T6 1  T7 2  T8 1  T9 1  T10 1
T11 2 T12 1 T13 2 T14 6 T15 2 T16 1 T17 1 T18 2 T19 1 T20 1
T21 3 T22 6 T23 1 T24 1 T25 3 T26 3                         = 55
R1 4  R2 2  R3 2  R4 16 R5 8  R6 4  R7 6  R8 2  R9 2  R10 2 = 48
```

No cell contains a semicolon inside a parenthetical (I checked the long ones:
L2's `C·N (which dominates the max disk ordinal (C−1)·N + (N−1))`, L23's
`leading fixed fields (name … C)`, L41's parenthetical which is in the
*Condition* column, not the *Instances* column). The mechanical count is
unambiguous. **Every stated total reproduces.**

### 1.4 Do the cells obey §21.1's *rules* for what a cell should enumerate?

The counts reproducing is not the same as the cells being right. §21.1 states two
axes "rather than judged each time", so I checked both exhaustively.

**Axis 1 — layout.** "Where the quantity a condition derives varies by layout, the
layout formulas are materially different shapes and the cell enumerates them."
Every row deriving a decoded size enumerates three layout formulas
(interleaved P·Q; planar numeric P·Bᶜ; packed planar bool ⌈P/8⌉): T3, T14, T21,
T22, L44, and T26's stride analogue. T4 enumerates the four
{interleaved,planar}×{numeric,bool} combinations. L21 enumerates the two
addressed-count formulas (N interleaved, C·N planar). T5 has only one layout in
which pad bits exist, and states one. T2 is interleaved-only and states one. No
layout-varying row omits the split; no layout-invariant row invents one. Clean.

**Axis 2 — direction.** "Where the condition compares two magnitudes either of
which can be the greater — a *differs from* or *does not equal* — the two
directions are likewise enumerated; where its own text bounds the comparison in
one direction — an *exceeds*, a *larger than* — there is one." I walked every row
with a magnitude comparison:

- one-directional (`below`, `less than`, `exceeds`, `above`, `larger than`,
  `longer than`, `> F−64`): F2, F3, F5, F9, F10, F16, F22, F32, L1, L2, L11,
  L17, L44, T9, T11, T12, T21, R10 — all one direction. ✓
- two-directional (`does not equal`, `differs from`, `is not 1`, `≠`,
  `not exactly`): F17, F23, L12, L21, L22, L30, T3, T14, T22 — all two. ✓
- no magnitude ordering (checksum against checksum, byte pattern against
  constant, multiple-of test, range test, nonzero test): F6, F8, F13, F14, F15,
  F20, F31, L20, L27, L28, L29, L37, L38, L39, T1 — none enumerates a direction. ✓

That is the axis on which a mis-written cell would be easiest to spot, and I
found no exception. The register's instance arithmetic is internally consistent
to a degree I did not expect.

**Reserved-range splits.** Rows over an enum's value set enumerate exactly the
sub-ranges their defining section states: L33 (linearization) gives four because
§11.4 states two distinct reserved sub-ranges (2–3 "without semantics", 4–0x7FFF
"for future assignment"); L34 (sample type) four for the same reason (14–19,
20–0x7FFF); L43, L45, L31 three because their sections state one reserved
sub-range each; L36 (layout) two because §10.2 gives channel layout no
experimental range at all. R1 gives 2 alternatives × 2 containers. All check out
against §10.2's table and the owning sections.

**The one cell I argued with: R8.** Its condition names two forms —
"a magnitude whose binary64 interpretation overflows (`1e400`) and the bare
tokens `NaN`, `Infinity` and `-Infinity` alike" — but its cell enumerates only
the two containers, giving 2 rather than 4. Every neighbouring §21.5 row does
enumerate its stated alternatives (R5 gives 2 forms × 2 loci × 2 containers = 8;
R6 gives 2 × 2; R7 gives 3 × 2). I first read this as under-enumeration, then
talked myself out of it, and I want the reasoning on the record because the call
is close:

- Against a finding: §18.2's underlying restriction is a *single* predicate —
  "A document is unreadable if it contains a number whose binary64
  interpretation is not finite" — and a lenient parser that accepts `NaN` as a
  number produces a binary64 NaN, which the same finiteness test catches. The
  two forms are then one check, and §21.1's rule "a row whose check ranges over a
  family without the condition changing shape states that range as a single
  instance" applies. The row's own words, "in any form … alike", assert exactly
  that, and §21.1 says only the two axes above are "stated rather than judged" —
  the rest is judged, and the document has judged.
- For a finding: a *strict* RFC 8259 parser never reaches the finiteness test for
  `NaN`; it rejects the token, which is R7's condition, not R8's. So the two
  forms are caught by different checks in different implementations.

I resolved it against a finding. The consequence of being wrong is a corpus that
may carry only `1e400` vectors — and since a `NaN` document is caught by R7 in a
strict parser and by R8 in a lenient one, and both outcomes are ignore-record at
the same tier with the same detector, no reader behaviour and no byte differs
either way. Not reportable.

---

## 2. Row-versus-rule agreement, row by row

I resolved every Governing rule cell to its requirement and compared wording,
outcome class, scope and detector. What follows records the checks that could
have gone wrong, not the ones that trivially did not.

### 2.1 Scope: `[R-CNT-12]` carries *two* different scope rules and §21 tracks both

`[R-CNT-12]` says a record of type 0 is "a validity error at the **same scope**"
(the containing *sequence's* owning scope) but says a reserved flag bit or the
MU=1/PE=0 combination is "a validity error at the **record's governing scope**"
(§7.2: layer for a layer record and for sub-records, file for other top-level
records). These are different for a layer record: type 0 at top level is a
file-scope error because the record cannot be identified as a layer record at
all, while a layer record's reserved flag bit is a layer-scope error.

The register gets this exactly right: F24 (type 0, top level) → reject-file;
L13 (type 0, sub-record) → reject-layer; F25/F26 (non-layer top-level flags) →
reject-file; L46/L47 (layer record *and* sub-record flags) → reject-layer, with
`(R-CNT-13)` in the parenthetical supplying the scope. F29/L14 likewise split the
framing-overrun rule at the sequence boundary, matching `[R-CNT-12]`'s explicit
"reject-file for the directory's top-level sequence, reject-layer for a layer
record's sub-record sequence". No divergence.

### 2.2 Detectors

Ten rules name the verifier as detector: `[R-CNT-05]`, `[R-CNT-12]` (flag
clauses), `[R-CNT-13]` (overlap), `[R-CNT-15]` (reserved-range emission),
`[R-CNT-22]`, `[R-SLB-01]`, `[R-SLB-03]`, `[R-SER-05]`, `[R-SER-08]`,
`[R-COD-10]`, `[R-MTA-05]`. These map onto exactly 20 rows — F7, F25, F26, F27,
F28, F33, F36; L18, L25, L40, L41, L42, L46, L47, L48, L49; T2, T4, T5, T26 —
and the table carries exactly 20 verifier rows. No row is assigned to the reader
whose rule assigns the verifier, or the reverse. Every verifier row's *Detected*
cell reads `certification`; every reader row's reads one of §19.2's four tiers.
Machine-checked.

The one place worth a note: F1 and F6 carry detector *reader* while the row text
says "a verifier holds no such exemption (§2.3)" and Appendix H lists the
front-block check among "the checks readers are exempt from". That is not a
divergence — §2.3 makes verifiers readers, so *reader* is the wider assignment,
and the exemption `[R-CNT-04]` gives a non-resident reader is carried in the row's
own condition text. Consistent.

### 2.3 The outcome column for verifier rows

This is the trap the brief warned about, and §21.1 has already sprung it: "For a
row whose Detector is *verifier*, the outcome names the scope at which the damage
is recorded, not an obligation on any reader: the governing rule states what a
reader does, and for several such rows it obliges the reader to serve the
structure unchanged (`[R-CNT-22]` … and `[R-MTA-05]` … — F27 and L48)."

I tested this against §2.4's definition of reject-file — "The file is not usable;
failure is reported for the whole file. A reader MUST NOT rely on any structure
in it" — which read literally contradicts `[R-MTA-05]`'s "readers process the
document unchanged". §21.1's gloss resolves it, and §21.1 also states which of the
two governs when they diverge ("the rule governs"). A reader that nevertheless
rejects the file is exercising `[R-CNF-12]`'s licence over a nonconforming file,
not violating `[R-MTA-05]`. I could not turn this into a fork.

F27's and L48's *scope* (file / layer) is not stated by `[R-MTA-05]`, which says
only that a verifier MUST report it. The scope comes from `[R-MTA-02]`'s owning
scope for a user-metadata record, correctly, because unsorted members are not a
"failure to read the document" and so the `[R-CNT-25]` quarantine — which routes
every *unreadable* document to ignore-record — does not reach them. Checked
against §7.1, §18.1 and §21.5's preamble. Correct.

### 2.4 The quarantine boundary

§21.5's preamble states the quarantine and three carve-outs. I checked each
against §7.1, §18.1 and §18.2:

- experimental-range encoding → no document rule attaches (`[R-MTA-10]`), §21.6
  records the non-violation. ✓
- a reader's or verifier's decline on the size bound or the frame's declared
  window → capability, not a fact about the file (`[R-MTA-09]`). ✓
- encoding 0 and reserved values → still violations, because "what `[R-MTA-10]`
  withdraws is the document's content rules, never the encoding byte's own value
  set". Checked against `[R-MTA-10]`'s own enumeration of what still decides
  conformance under an unassigned encoding: "the record's framing and extent slot
  (`[R-CNT-13]`), the encoding byte's own value set (`[R-MTA-03]`), and the
  extent's terminal CRC (`[R-CNT-20]`)". Three items, and the register has all
  three: F21/F22/L10/L11 and F23/L12 for framing, R1 for the value set, R2 for
  the CRC. R2's instances are not split by encoding, correctly, because the
  terminal CRC binds under an unassigned encoding too. ✓

R4 is the most intricate cell in the document and I derived its members from
`[R-COD-06]` rather than from R4's own text, per the brief. `[R-COD-06]`'s frame
constraints are: (a) begin with the magic; (b) no skippable frame anywhere and no
second frame; (c) no dictionary use, disclosed or not; (d) no nonzero
Dictionary_ID; (e) no content-checksum flag; (f) no window exceeding the tile's
decoded size; (g) content-size, when present, equals the decoded size; (h) a
reader must not size a buffer from it; (i) a SHOULD on keeping the window within
8 MiB. §18.2 excepts (f) and (g) and replaces both, and says (c)'s undisclosed
half and (h) carry no witness. §18.2 adds "exactly one … frame **occupying the
extent's bytes before its terminal CRC**", giving a trailing-bytes constraint.
Derived members: magic, skippable, second frame, dictionary ID,
content-checksum, trailing bytes, content-size-larger, content-size-smaller —
**eight**, × two containers = 16. R4 states exactly 16. The count derives from
the rule, not from the cell. No finding.

### 2.5 Completeness, register → rules (does any row register a non-violation?)

I could not find one. The rows that look like candidates are the "cause" rows —
T13, T15, T16, T23, T26 — each of which says explicitly that "the check that
detects it is T24's / T25's / T2's or T4's, and this row records the cause rather
than a procedure of its own". Each cause is genuinely a MUST-level prohibition:
`[R-COD-02]`'s independent-decodability sentence (keyword-free, but §21.7 treats
the parallel `[R-CNT-13]` sentence as a prohibition and the brief's discriminator
warns against reading keyword-free clauses as inert), `[R-COD-05]`'s "raw, not a
zlib … or gzip … wrapper", `[R-COD-07]`'s "The LZ4 frame format is not used",
`[R-COD-10]`'s stride. T13's two instances are exactly the two detectable ones —
a deflate history window and an lz4 back-reference — with zstd correctly absent
because zstd's only mechanism for it is an undisclosed dictionary, which §17.2
and §21.7 both classify as witnessless. That is careful work.

### 2.6 Completeness, rules → register

I swept every requirement identifier in the document and asked where its
detectable violations land. Working notes:

- `[R-ENC-02]` → F1 (the detectable half; a byte-swapped u64 elsewhere is just a
  different value and §21.7's content class covers it).
- `[R-ENC-03]` → F2, L1, T11. `file_id` is correctly absent from F2: it is an
  identifier, not an offset/length/extent/count, and §6.2 bounds it only by ≠ 0
  (F12).
- `[R-ENC-04]` → F3, L2, T12. L2's nine instances derive correctly: I checked
  that Q = ΣBᵢ (≤ 65535·8) and Fᶜ cannot overflow, that ⌈P/8⌉ is dominated by P,
  that V = P·C is dominated by P·Q since every Bᵢ ≥ 1, and that the max disk
  ordinal (C−1)·N + (N−1) is dominated by C·N. The nine listed are the nine that
  can overflow independently.
- `[R-ENC-06]`, `[R-ENC-13]`, `[R-ENC-14]` → no witness / reader rule / SHOULD.
  §21.7 accounts for `[R-ENC-06]`.
- `[R-ENC-07]` → the structures whose size can be wrong all have rows: directory
  (F16), record header (F29/L14), index entry array (L22), user-metadata inline
  payload (F23/L12), user-metadata extent (F22/L11), front block (F6), layer
  record payload (L23). The trailer's 64 bytes are definitionally the final 64,
  so unexhibitable.
- `[R-ENC-11]`, `[R-ENC-12]`, `[R-ENC-15]` → L3–L9, F4, R5, R6, R10. The 255-byte
  name cap is unexhibitable for layer/dimension/channel names (u8 prefix) and is
  exhibitable only for user-metadata keys, which carry no prefix — R10 exists and
  is the only length row. §21.9 says the same. ✓
- `[R-CNT-01]` → F13, F17. `[R-CNT-02]` → F33, L18 (disjointness); the
  "belongs to no class" half is declared untestable in §5.2's Note, with a
  reasoned account, and correctly carries no row.
- `[R-CNT-06]` → its eleven gates map onto F8, F9, F10, F11, F12, F13, F14, F15,
  F16, F17, F18, F19 plus F2's generation instance. All present.
- `[R-CNT-13]` → F3, F30–F33, L15–L18. `[R-CNT-23]`'s enumerated constraint set
  → L27–L36, L39, L43, L45, L1, L21, L22, L37, plus the name rows. I walked
  §7.4's table field by field; every constraint has a row.
- `[R-IDX-03]`'s eleven §15.3 rows → T1, T6–T12, L18, F33, L40/L41/L42. §15.3
  says "Six rows are marked *structural*" and there are exactly six.
- `[R-COD-*]` → L43, L44, L45, T13–T26. `[R-COD-06]` says "Three frame features
  are excluded" and names three (dictionary, content-checksum, window) → T19,
  T20, T21. Count reproduces.
- `[R-MTA-04]`'s four restrictions → R7 (object/BOM/JSON), R8 (finite numbers),
  R9 (duplicate keys), R5/R6/R10 (UTF-8 and name rules). All four covered.
- `[R-SLB-04]` → §16.2's Note explains why it carries no row of its own (its
  detection *is* `[R-SLB-03]`'s), and the explanation holds: every file
  exhibiting a stale declaration exhibits L41 or L42.
- `[R-LIF-04]`'s residue → §9.5's Note explains why it carries no row, and the
  explanation holds.
- Everything else is actor conduct, a SHOULD, or accounted for by §21.7.

I found no MUST-level, detectable, file-conformance condition without a row.

---

## 3. Cross-references to rows

Every citation of a register row by label, anywhere in the document, and what I
found:

| Where | Cites | Verdict |
|---|---|---|
| §5.2 `[R-CNT-21]` | "L18's overlap or L40 through L42's placement among them" | resolves; all four are verifier/reject-layer rows a coverage walk can establish; "among them" is explicitly non-exhaustive |
| §9.6 `[R-LIF-06]` | "(§21.2 rows F8 and F17)" | resolves, but see finding **register-02** |
| §17.2 Note | "(§21.4, T24)" | T24 is the trailing-bytes row; correct |
| §20.3 step 4 | "(L44)" | L44 is the lz4 decoded-size cap; correct |
| §20.5 `[R-WRT-06]` | "F36 and L25 for a record type, and one row for each of the other seven spaces §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)" | I re-derived this from §10.2's table: eight spaces, record type gets F36/L25, and the other seven are channel layout (L36), linearization (L33), sample type (L34), codec (L43), filter (L45), index encoding (L31), metadata encoding (R1). Seven cited, seven derived, each row is that space's reserved-range row. Correct. |
| §21.1 | "F1 of F6 and of F8, F35 of F36, L24 of L25" | each is a genuine strict specialization; see §5 below on the ones not listed |
| §21.1 | "T24's *any codec*", "(T15, T25)" | correct exemplars |
| §21.1 | "F27 and L48" | correct |
| §21.4 T2 | "the same byte at a padding position is T4's, the two rows together covering `[R-SER-08]`" | I checked the join: an interleaved bool byte at a padding position that is neither 0x00 nor 0x01 necessarily differs from the recorded fill byte, because `[R-TYP-07]` constrains that byte to 0x00 or 0x01 and L35 registers the alternative. So T4 does cover it and the two rows do partition `[R-SER-08]`. Correct. |
| §21.6 | "(F36, L25)", "(F18 …)", "(F35, F36, L24, L25)" | correct |
| §21.7 | T2, T3, T4, T5, T14, T15, T17, T23, T25, T26 | each resolves to a row that says what §21.7 claims; I checked the codec claim in particular ("sometimes witnessed … but neither is assured") and it holds |
| Appendix H | F1, F6, F7, F36, L25, R1 | correct |

One near-miss I checked and cleared: §21.1 says "`[R-SER-08]` … is why §14.2 calls
it the sole resolved byte in this format". The phrase "the one case where a reader
resolves a byte to a value rather than passing it through" is actually
`[R-TYP-04]`'s, in §12.3; §14.2 is where `[R-SER-08]` itself lives. The
attribution is loose by one section. Not worth a finding: the claim is true and
the rule it names is the right one.

---

## 4. Outcome vocabulary

§2.4 defines five values. Four are reader outcomes (`[R-CNF-07]`): reject-file,
reject-layer, reject-tile, ignore-record — one per register subsection, all
reachable, all used. The fifth, preserve-verbatim, "names an updater obligation,
orthogonal to reader outcomes" and is therefore correctly absent from the
register; it is reachable through §20.4's table (its MU = 1 and MU = 0 / PE = 1
rows), exactly as §2.4's own table says. Every row's outcome is one of the four.
No row uses a value the document does not define; no defined value is unreachable.
Nothing to report.

---

## 5. Things I chased and rejected

Recorded so the next round does not re-spend the effort.

**The specialization list is not closed.** §21.1 names three specialization pairs.
I found four more: T14 ⊂ T3 restricted to codec 1 (under codec 1 the stored bytes
*are* the decoded image, so a wrong entry length is also a wrong decoded length);
T12 ⊂ T9 (a sum exceeding 2⁶³−1 necessarily exceeds F−64, since F ≤ 2⁶³−1);
L46 ⊂ L49 for a *layer record* (the registry fixes PE = 1, so PE = 0 is also a
stored-flag mismatch); F25 ⊂ F28 for a type-0x0002 record. In every one of the
four the two rows share detector, detection point and outcome, so §21.1's stated
consequence — "recorded against the narrower row, whose detector and detection
point are the ones that apply" — is a distinction without a difference. The three
listed pairs are the ones where attribution matters (F35/F36 and L24/L25 differ
in detector and detection point; F1 differs in governing rule). Not a defect.

**T11 narrows §15.3.** §15.3's row 6 reads "offset > 2⁶³ − 1 or length > 2⁶³ − 1
(non-sentinel)", which as written catches an entry with offset = all-ones and
length = 5; T11 excludes it ("the value being distinct from the all-ones
sentinel"), routing it to T7 instead. §21.1 says the rule governs on a divergence,
but both rows are reader / tile use / reject-tile, so nothing observable turns on
it. Not a defect.

**A conforming reader has no licence to decline an arbitrarily large *stored*
tile.** §21.9's table bounds decoded sizes, never stored lengths, and §17.2's Note
says "no bound relates a stored length to its decoded size in either direction …
Resource limits are §21's subject" — deferring to a section with no such row.
`[R-ERR-04]` then makes declining a within-table file on resource grounds
nonconforming. I thought this was a gap for a while. It is not: every structure a
reader must hold *whole* has a table row (directory 16 MiB, decoded tile 256 MiB,
document 16 MiB, zstd window 8 MiB) or a fixed bound (one index segment is
2¹⁶ × 20 = 1.25 MiB, the segment CRC array 256 KiB at the 2³² entry_count
guarantee). A large stored extent is verified by streaming CRC and streamed into a
bounded decode, so "MUST accept" costs bounded memory. The table is exactly
complete for its purpose. Not a defect.

**`[R-CNF-03]`'s exemption versus `[R-CNT-18]`.** `[R-CNF-03]` lifts the
acceptance duty for a file "carrying no record of a type it does not implement
with MUST_UNDERSTAND = 1", without a scope qualifier, while §21.6 insists "the
same type as a layer sub-record is reject-layer and never a ground to refuse the
file". A lifted duty is not a permission, and `[R-CNT-18]` states an explicit
"where the file is otherwise conforming a reader MUST NOT reject the file for it".
The prohibition wins. Not a defect, though the §21.6 paragraph is doing real work
here and is worth keeping.

**§21.9's table versus every other limit statement.** I checked all ten hard
limits against their defining sections and Appendix B: name ≤ 255 (§4.6);
user-metadata key ≤ 255 (§18.2); rank ≤ 255 and C ≤ 65,535 (§7.4's u8/u16);
codec 4 at ≤ 0x7E000000 (§17.2); every offset/length/extent/count ≤ 2⁶³−1 (§4.2);
A a power of two 512…2⁶² and A_slab a power of two 1…2⁶² (§7.4, §16.1, §16.2);
S 1…2⁶³−1 (§7.4, §16.2); dir_offset ≥ 16 and dir_length ≥ 4 (§6.2); 128-byte
minimum (§5.1). Every one matches its defining section exactly, and matches
Appendix B. Nothing stated here is stated differently there. §7.1's
extent_length ≥ 5 is a hard limit §21.9 omits, but §21.9 expressly disclaims being
an inventory ("The hard limits it restates are a finding aid rather than an
inventory"), and Appendix B carries it. The minimum-guarantee row derivations in
the Note also reproduce: 2³² entries / 2¹⁶ per segment × 4 bytes = 256 KiB, and
2³⁶ gives 4 MiB, as stated. One provenance count in that paragraph does not
reproduce — finding **register-03**.

**F5's second instance.** "committed_file_length" below 128 with a physical file
at or above 128 also exhibits F17. Both rows fire; both are reader/open/
reject-file. Fine.

**§9.7's coverage walk versus §21.** Every claimant §9.7 names has a bounds row
and a checksum row, and the one class §8.1 leaves unchecksummed — the extent of a
record of an unassigned type — correctly has no CRC row. §22.3's four "residues"
match. Consistent.

---

## 6. Findings

### register-01 — AMBIGUITY — §21.2 preamble; F5; `[R-CNT-27]` (§5.1) against `[R-CNT-06]` (§6.2)

§21.2's preamble excludes the geometry rows from reaching a file that declares a
format major other than 1, and states a closed count of the exceptions:

> "the rows below whose subject is that file's *geometry* do not reach it: §6.2
> puts the version gate ahead of every check but the trailer magic and the
> trailer CRC, so such a file is refused on capability grounds first. Four rows
> are outside that reasoning and do reach it, because their subject is a field
> fixed across every major (`[R-CNT-24]`): F8 and F1's trailer-magic instance,
> F14's trailer CRC — the two checks §6.2 places before the gate — and F6 with
> F1's front-block instance"

The warrant is §6.2's ordering rule. But §6.2's ordering rule governs only the
checks §6.2 itself lists:

> "A reader MUST validate, in order: the trailer magic; the trailer CRC; the
> version gate (§6.3) … and then, those gates passed, MUST validate all of the
> following before acting on the fields involved: the flag gates (§6.3);
> committed_file_length equals the file size … dir_offset ≥ 16; dir_length ≥ 4;
> dir_offset + dir_length ≤ F − 64; 1 ≤ generation ≤ 2⁶³ − 1; file_id ≠ 0;
> reserved bytes zero."

F5's governing rule is `[R-CNT-27]`, stated in §5.1 and absent from that list:

> "No conforming file is shorter than 128 bytes … A reader MUST treat a shorter
> file as a validity error at file scope."

F5 is the **only** register condition whose check §6.2 does not order. Its first
instance is "F (physical file size)", a quantity §19.1 obtains at step 1 — before
the trailer is fetched at step 2 — and neither §19.1 nor §19.2 nor §21.1 orders a
check *within* the "open" tier.

Construct the witness. A file of F = 80 bytes: bytes [0,16) the exact front
signature block, bytes [16,80) a trailer whose magic is `8A 4E 52 41 54 0D 0A 1A`
at offset 16, whose version_major at offset 24 is 7, and whose CRC at [76,80)
verifies over [16,76). `[R-CNT-24]` fixes those three positions in every major, so
all three checks pass, and F6/F1 do not fire because the front block is intact.

- **Reading (a).** The reader guards on file length before touching the trailer —
  the natural implementation, since it must know F ≥ 64 to fetch a trailer at
  all — applies `[R-CNT-27]`, and reports reject-file. As a verifier this is an
  established violation, so §2.3 obliges the verdict *nonconforming*.
- **Reading (b).** The reader follows §6.2's order, reaches the version gate, and
  refuses on capability grounds. §2.3: such a file "is neither conforming nor
  nonconforming under it", and the verifier verdict is *cannot establish*.

I pick **(b)**: §21.2's preamble's *conclusion* covers F5 (its subject is the
file's geometry), and §2.3 forbids a finding about the bytes of a file declaring
another major, which is what (a) produces. But the preamble's conclusion rests on
a premise that does not reach F5, so an implementer who reasons from §5.1 and
§6.2 directly — rather than from a preamble sentence in §21.2 — lands on (a). What
an implementer does wrong without this fixed: a verifier reports *nonconforming*
for a file this document declines to judge, which §2.3 prohibits, and its
diagnostic sends the user to "your file is corrupt" instead of "this reader does
not implement format major 7" — precisely the confusion `[R-CNT-07]`'s SHOULD
about distinct diagnostics exists to prevent.

Note the boundary: below F = 64 there is no trailer to validate and `[R-CNT-27]`
applies unconditionally, so the ambiguity is confined to 64 ≤ F < 128. F5 stays
reachable for major-1 files, so its conformance vector remains constructible.

**Byte-level: no.** Both readings refuse the file; nothing is accepted under one
reading and rejected under the other, and no emittable byte sequence changes. The
fork is in the diagnostic and in which of §2.3's three verifier verdicts is
reported — real, and worth fixing, but not the emittable or accept/reject set.

### register-02 — OBSERVATION — §9.6 `[R-LIF-06]`, citing §21.2

> "a file whose final 64 bytes are not a valid trailer fails `[R-CNT-06]`'s gates
> on the bytes handed over (§21.2 rows F8 and F17)"

The same failure mode is described one subsection earlier, in §9.5's Note, with
three grounds rather than two:

> "A reader meets it as a trailer that fails its gates — the magic, the CRC, or
> committed_file_length against the transport size, each of which §21.2 already
> registers"

Those three are F8, F14 and F17. §9.6's parenthetical names F8 and F17 and omits
F14. The omission is reachable: residue past a completed commit, or a torn tail,
whose final 64 bytes happen to carry the trailer magic — §9.6 itself warns that
"a tile payload can deliberately contain a byte string that mimics a valid
trailer" — is recorded against F14 when its CRC does not verify, a row the
citation does not reach. Deciding whether the list is meant as the set or as
examples costs a reader a cross-check against §9.5 and §21.2; the two passages
being adjacent and differing is what makes it worth naming.

No behavioural consequence: F8, F14 and F17 are all reader / open / reject-file.

**Byte-level: no.** All three rows carry the same detector, detection point and
outcome, so no verdict and no byte turns on which is cited.

### register-03 — OBSERVATION — §21.9 `[R-ERR-05]`

The hard-limits paragraph closes with a provenance account and a closed count:

> "Most follow from a field's width, an external format, or the value domain, and
> the rest from arithmetic over structures a generation cannot omit. Two do not:
> the 512 floor on A is a number chosen here, fixed at the legacy sector size
> (§16.1) so that a declared alignment is worth declaring, and the 255-byte cap on
> a user-metadata key is this specification folding §4.6's name rules onto keys,
> which carry no length prefix to force it."

I derived the members from the list the sentence is about rather than from the
sentence, per the brief. The same paragraph lists among the hard limits:

> "a declared alignment A a power of two with 512 ≤ A ≤ 2⁶², and a declared slab
> alignment A_slab a power of two with 1 ≤ A_slab ≤ 2⁶²"

The **power-of-two form** of A and of A_slab falls in none of the four stated
categories. It follows from no field width (both are `u64`); from no external
format; from no value domain, since `[R-ENC-03]` bounds magnitude and says nothing
about form; and from no arithmetic over an unomittable structure. It is a
constraint chosen here, exactly as the 512 floor is — and unlike the 512 floor it
is chosen twice, once for each field, and for A_slab it is the *only* substantive
constraint (its 1 floor is 2⁰, implied by power-of-two-ness, and its 2⁶² ceiling
is the largest power of two inside the value domain). So the count "Two" is short
by at least one, arguably two.

The rest of the taxonomy does reproduce: dir_offset ≥ 16 and dir_length ≥ 4 and
the 128-byte minimum are arithmetic over structures a generation cannot omit;
rank ≤ 255 and C ≤ 65,535 and the 255-byte name cap are field widths;
0x7E000000 is the external LZ4 block format; 2⁶³−1 and A's and A_slab's ceilings
are the value domain; S ≥ 1 follows from 0 being the field's own no-declaration
sentinel.

What an implementer does wrong without this: nothing to the bytes. No limit is
misstated, every limit is normative where its structure is defined, and §21.9
disclaims being an inventory. The cost is to a reader who trusts the taxonomy to
tell them which numbers are arbitrary and which are forced, and therefore which a
future major could move — and who concludes that A's power-of-two-ness is forced
by something when it is not.

**Byte-level: no.** This is a claim about the provenance of limits the document
states correctly elsewhere; no limit's value, and therefore no file's validity,
changes under either reading.

---

## 7. Confidence

Medium-high on the register itself. The row/rule agreement, the detector
assignments, the outcome vocabulary, the instance arithmetic, the completeness
sweep in both directions, and every stated total all check out, and the two
subsections whose totals a reporter could most easily break (§21.3 at 49 rows /
116 instances, §21.5 at 10 rows / 48 instances) reproduce exactly. The cross-
reference sweep found one under-naming and no misdirection. My one substantive
finding is an ordering question that §21.2's preamble answers with a warrant that
does not cover the row it excludes; I would expect a repair to be one clause in
§5.1 or §6.2 placing `[R-CNT-27]`'s check relative to the version gate, plus a
recount of "Four rows" if the answer goes the other way.

I could not build a case that any of the three forks bytes.
