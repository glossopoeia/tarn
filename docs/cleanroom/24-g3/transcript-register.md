# Round 24 — Register hunter — working transcript

Charter: audit §21, the error-handling register, against the rules it restates and
against itself.

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in full, in overlapping chunks. I ran `grep`/`wc` against that file only, and one
Python script that reads no files (a CRC-32C implementation plus arithmetic), and one
Python script that re-parses the four register tables out of that same file to count
rows and instances. I listed no directories, read no ADRs, no `docs/`, no
`conformance/`, no `registry.json`, no `PLAN.md`, no `AGENTS.md`, no git history. No
web access.

Context I did not ask for **did** appear before I began: the runtime placed a project
instruction file (`CLAUDE.md` pointing at `AGENTS.md`) and an index of the
maintainer's auto-memory notes in my context, the latter with titles naming things
like a "gate board", a "working cadence", prior "workflow verifier failures", and a
claim about how §21 relates to a vector corpus. I did not open any of the files it
named and I have not used any of it as evidence; I flag its appearance here because
the brief requires it. Nothing below rests on it — every claim cites a line of
`spec/tarn.md`.

## 1. Method

1. Read §21 end to end first (§21.1's governing rules before anything else), then the
   whole document front to back so that every row could be checked against its rule
   in the rule's own words rather than the row's.
2. Re-parsed the four register tables mechanically and recomputed §21.1's instance
   arithmetic per cell, per subsection, and in total.
3. Enumerated every requirement identifier in the document and asked, for each,
   whether it names a condition that makes a file nonconforming and whether the
   register carries it — and in the other direction, whether each row's condition is
   actually a violation under the rule it cites.
4. Chased every citation of a register row label from outside §21 (and from inside),
   and checked that each resolves to a row saying what the citing text claims.
5. Recomputed every worked number in the document that a register claim leans on
   (CRCs, index-region sizes, the §21.9 note's arithmetic, the §7.4 payload layout).
6. Built degenerate-but-legal files in my head and asked what the register said about
   them.

## 2. The counting — worked

### 2.1 Conditions

Row labels, counted off the tables:

| Subsection | Labels | Count | Stated |
|---|---|---|---|
| §21.2 | F1…F36 | 36 | "36 conditions" |
| §21.3 | L1…L49 | 49 | "49 conditions" |
| §21.4 | T1…T26 | 26 | "26 conditions" |
| §21.5 | R1…R10 | 10 | "10 conditions" |
| total | | **121** | §21.8: "121 conditions" |

Reproduces exactly.

### 2.2 Instances

§21.1 fixes the arithmetic mechanically: "Instances within a cell are separated by
semicolons, and a cell reading — is one instance; the count is therefore mechanical
once the cell is written." I applied exactly that (semicolon count + 1; `—` → 1),
after checking by eye that no cell contains a semicolon inside a parenthetical — the
only cells with nested punctuation are L2 (`C·N (which dominates the max disk ordinal
(C−1)·N + (N−1))`), L23 (`trailing fixed fields (index_encoding, entry_count,
crc_of_crc_array)`) and T26, and all of those use commas or colons internally.

Per-subsection totals:

- §21.2 (F): 2,6,2,1,2,2,4,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,2,3,2,1,1,5,1,1,1
  → **58**
- §21.3 (L): 8,9,1,2,1,1,2,2,2,1,1,2,1,3,4,2,2,3,1,1,4,4,4,1,1,1,1,1,3,2,3,3,4,4,1,2,1,1,3,1,3,1,3,3,3,2,2,1,4
  → **116**
- §21.4 (T): 1,1,6,4,1,1,2,1,1,1,2,1,2,6,2,1,1,2,1,1,3,6,1,1,3,3 → **55**
- §21.5 (R): 4,2,2,16,8,4,6,2,2,2 → **48**

Total **58 + 116 + 55 + 48 = 277**, exactly §21.8's "277 instances". Both totals in
§21.8 reproduce. I found no arithmetic discrepancy anywhere in §21.

### 2.3 The arithmetic *rules*, applied cell by cell

Reproducing the total is not the same as the cells being right, so I checked the
cells against §21.1's five stated axes.

*Magnitude, two directions.* Rows whose condition is a "differs from" / "does not
equal" between two quantities either of which can be the greater, and which therefore
owe two directions: L30 (fill prefix vs element size — 2 ✓), L21 (entry_count vs
derived count, ×2 layouts — 4 ✓), L22 (extent_length vs formula — 2 directions plus 2
stated alternatives = 4 ✓), T3 (3 layouts × 2 = 6 ✓), T14 (3 × 2 = 6 ✓), T22 (3 × 2
= 6 ✓), F17 (2 ✓), F23/L12 (`inline_length` not 1 → 0 / ≥2 = 2 ✓). All correct.

*One direction where the text bounds it.* F9 ("less than 16"), F10 ("exceeds"), F16
("less than 4"), L44 ("exceeds 0x7E000000"), T21 ("larger than") — all 1 direction ✓.

*No magnitude ordering.* F14, F20, T1, L37, L38 — checksum-against-computed, 1 each ✓.
F6 (byte pattern against a constant, split by *field* into 2, not by direction) ✓.
F28/L49 (a stored bit against a registry constant, split by field) ✓.

*Nonzero tests are not comparisons.* L20 ("declares both A ≠ 0 and S ≠ 0") = 1 ✓ —
§21.1 cites this case by name. L27, L28 = 1 each ✓. F25 ("a combination of two flag
bits") = 1 ✓ — also cited by name.

*Layout formulas are materially different shapes.* L44, T21 (3 ✓), T3, T14, T22 (3 ×
2 ✓), T4 (4 — the four places a fill value can sit ✓), T26 (3 layout contexts ✓), L2
(P·Q and P·Bᶜ enumerated separately ✓; ⌈P/8⌉ correctly *not* enumerated, since it can
never overflow independently of P).

*Family without shape change is one instance.* T24 "any codec" ✓ (§21.1 cites it),
F19 "flags bits 0-15" ✓, T18 "the constraint reading the same at every placement" → 2
alternatives, not 4 ✓.

*Value-set rows enumerate the space's partitions,* which I checked against §10.2's
table: L31 index encoding 3 (0 / reserved 2–0x7F / experimental ≥0x80) ✓; L33
linearization 4 (0 / 2–3 / 4–0x7FFF / ≥0x8000 — §11.4 does distinguish the two
reserved bands) ✓; L34 sample type 4 ✓ (§12.2's bands); L36 layout 2 ✓ (§10.2: layout
has *no* experimental range); L43 codec 3 ✓; L45 filter 3 ✓; R1 metadata encoding 2
alternatives × 2 containers = 4 ✓, correctly excluding the experimental range, which
§21.6 makes a non-violation.

*Container axis in §21.5.* Every R row is (alternatives × 2 containers): R1 2×2, R2
1×2, R3 1×2, R4 8×2, R5 4×2, R6 2×2, R7 3×2, R8/R9/R10 1×2. Perfectly regular. The
one place the regularity exposes a problem is R7 — see finding register-04.

*R4's eight alternatives* I checked one by one against §18.2. §18.2 carries over from
`[R-COD-06]`: frame magic; no skippable frame; no second frame; no dictionary use,
disclosed or not; no nonzero dictionary ID; no content-checksum flag; the bar on
sizing a buffer from a declared length. It replaces two (the tile's declared decoded
size, and `Window_Size`), and adds "occupying the extent's bytes before its terminal
CRC" and the content-size pin. It expressly withholds two from R4: "Two of those
carry no witness a file exhibits, and R4 registers neither: dictionary use the header
does not disclose is a writer violation nothing in the extent shows … and the bar on
sizing a buffer binds a reader rather than the document." That leaves magic,
skippable, second frame, dictionary ID, checksum flag, bytes remaining, content-size
larger, content-size smaller = 8. R4 enumerates exactly those 8 × 2 = 16. Correct.

## 3. Row-versus-rule agreement

I walked all 121 rows against their governing rules. Rather than reproduce 121
paragraphs, here is what I checked and what came out.

### 3.1 Outcome against scope

Every F row: I traced the governing rule's own scope assignment and confirmed
reject-file. The non-obvious ones: F21/F22 take file scope because `[R-CNT-25]`'s
extent-slot clause says "a validity error at **its containing scope**" and `[R-MTA-02]`
adds "The quarantine covers the document only: a malformed extent slot on such a
record, (0, 0) included, is a validity error at the record's containing scope …
because that failure precedes the document" — so these are correctly *not* in §21.5.
F25/F26/F28 take file scope because §7.2/§7.3 say "the record's governing scope" and
§7.2 fixes that as "the file for other top-level records". F27 takes file scope
because `[R-MTA-05]`'s unsorted document is not a way the document is *unreadable*, so
the quarantine does not reach it and §21.1's scope rule applies — which §21.6's
closing paragraph and §21.1's own "F27 and L48" aside both confirm.

Every L row: reject-layer confirmed. The layer record's flags rows (L46/L47/L49) are
correctly layer-scope, because §7.2 says the scope a *layer* record governs is the
layer, even though §7.3's table calls a layer record's own scope "file (container for
layer scope)". The split of the flags rows between §21.2 ("A **non-layer** top-level
record's flags…") and §21.3 ("A layer record's or sub-record's flags…") is exactly
right, and F24 correctly says "A **top-level record's** type field is 0x0000" without
the non-layer qualifier — a type-0 record cannot be a layer record. That is a
deliberate and correct asymmetry.

Every T row: reject-tile confirmed. §15.3's eleven-row table maps onto the register
without loss: sentinel→§21.6; sentinel with crc≠0→T6; one-half sentinel→T7;
length 0→T10; offset<16→T8; domain→T11; overflow→T12 and >F−64→T9 (the register
splits one rule row into two, which is fine); crc fail→T1; intra-layer overlap→L18;
cross-scope overlap→F33; alignment/slab→L40/L41/L42. §15.3's "Six rows are marked
*structural*" — I counted the italic markers: six. ✓

Every R row: ignore-record, which §21.1 sources to `[R-CNT-25]`'s express assignment
"for every §21.5 row, whatever the containing scope". R4's governing rule is
`[R-MTA-09]`, which supplies its own express assignment: "Any violation here is
ignore-record, never the tile-scope outcome §17.2 assigns."

### 3.2 Detector and detection point

Mechanical count: 101 reader rows, 20 verifier rows; all 20 verifier rows carry
Detected = *certification* and all 20 certification rows carry Detector = *verifier*.
No leakage in either direction.

Reader tiers: open 32, layer access 35, tile use 24, extent use 9, plus R1's split
cell "open (top-level); layer access (sub-record)". 32+35+24+9+1 = 101 ✓.

I checked each verifier assignment against its rule's own words and all twenty hold:
`[R-CNT-05]` ("readers check neither"), `[R-CNT-12]` ("their detection is a
verifier's"), `[R-CNT-13]` ("readers are not obligated to detect overlap"),
`[R-CNT-15]` ("a verifier MUST treat a reserved-range record type as…"), `[R-CNT-22]`,
`[R-MTA-05]`, `[R-SLB-01]` ("readers are not obligated to — offsets are always
explicit"), `[R-SLB-03]`, `[R-SER-05]` ("a verifier MUST check it"), `[R-SER-08]`
("its assigned detector is the verifier"), `[R-COD-10]`.

Two detection points deserved a second look and both are right:

- L37/L38 are reject-**layer** but Detected = **tile use**. §19.2 anticipates exactly
  this: "index-chain failures take layer scope (`[R-IDX-04]`) although their detection
  point is tile use."
- L3/L5/L6 are reject-**layer** but Detected = **open**. §19.1 step 4 puts each layer
  record's name parse at the open ("each layer record's name, parsed and checked per
  §4.6"), and §4.6 is where both `[R-ENC-11]` and `[R-ENC-12]` live. §19's preamble
  also disclaims its own enumerations in favour of the register's Detected cells: "A
  row this section does not restate is due at its own tier all the same." That
  disclaimer is what licenses R1's "open" too, since §19.1 step 4 names only the three
  framing checks (no (0,0) slot, extent_length ≥ 5, inline_length = 1) and not the
  encoding byte's value set.

The one genuinely conditional detector is F1/F6's front-block instance, where
`[R-CNT-04]` lets a non-resident reader "defer or omit the check". The Detector cell
just says "reader", but both Condition cells spell the condition out, §21.2's preamble
repeats it, and Appendix H records the verifier's lack of the exemption. Not a defect.

### 3.3 Divergences found

Only two rows say something materially different from the rule they cite, and both
are recorded below (register-04 for R7, register-05 for F31). Everything else
restates faithfully. A few notes on near-misses I checked and cleared:

- **L41 vs `[R-SLB-03]`.** The rule says "each stored tile's offset equals the previous
  stored tile's offset plus **its** length"; the row says "plus **that tile's**
  length". Both antecedents resolve to the previous stored tile. No divergence.
- **T9 vs §15.3.** "ends past F − 64" against "offset + length > F − 64". Equal, and
  the boundary case offset+length = F−64 is correctly conforming.
- **F31/L16 boundary** — see register-05.
- **T13's governing rule `[R-COD-02]` carries no BCP-14 keyword** ("Every stored tile
  is independently decodable…"). Following the brief's second discriminator, I did not
  treat that as inert: it is the same declarative construction §21.7 calls a
  *prohibition* for `[R-CNT-13]`. T13's outcome comes from tile scope (§17: "the
  owning scope of one stored tile's payload under them is the tile") and its check
  from T25/`[R-COD-08]`, exactly as the row says.
- **R10's Governing cell reads `[R-MTA-04]` (R-ENC-12)** — the only §21.5 row that
  names `[R-CNT-25]` neither as governing nor in parentheses; every other one of the
  ten does. I decided this is citation hygiene and not a defect: §21.1 fixes the
  outcome for every §21.5 row from the quarantine regardless, and `[R-MTA-04]`'s own
  lead-in ("a document violating any of them is unreadable — ignore-record") supplies
  it too. Recording it here rather than as a finding.
- **L26 and L31 put a section reference in the parentheses** ("§7.3 registry table",
  "§15.1") where §21.1 says "any identifiers following it in parentheses are the
  further rules the condition reads". Cosmetic; not reported.

## 4. Completeness, both directions

### 4.1 Rules → rows

I enumerated every `[R-…]` identifier in the document (155 of them, including
`[R-ENC-100]`, which appears only as §2.2's illustration of how numbering extends, and
`[R-SER-04]`, which §14.4 records as withdrawn and permanently retired) and asked of
each whether it names a detectable file-conformance violation and where the register
carries it. The mapping is complete. The ones worth recording:

- `[R-ENC-03]` / `[R-ENC-04]` are carried at all three scopes (F2/F3, L1/L2, T11/T12),
  and §15.2's carve-out — "`[R-ENC-03]`'s value-domain rule and `[R-ENC-04]`'s sum rule
  apply to the fields of non-sentinel entries only" — is honoured: T11 and T12 both
  say "non-sentinel".
- `[R-ENC-12]`'s 255-byte cap has a row only for user-metadata keys (R10), correctly:
  layer/dimension/channel names carry a `u8` prefix, so an over-long one is
  unrepresentable, which is exactly the distinction §21.9's hard-limit paragraph draws
  ("a user-metadata key at most 255 bytes by §18.2's folding of §4.6's name rules onto
  keys, **which carry no such prefix**").
- `[R-IDX-05]`'s "a partial segment's CRC MUST be computed" has no row of its own and
  needs none: a partial segment carrying `0xEECB3BB2` fails L38, and L38's condition
  says so in terms — "a partial segment covers only its actual bytes, and the
  all-sentinel constant 0xEECB3BB2 never substitutes for comparison".
- `[R-SLB-04]` (stale slab declaration) has no row, and §16.2's Note says why.
  `[R-LIF-04]` (truncate/overwrite) has no row, and §9.5's Note says why.
  `[R-CNT-18]`'s nesting bar has no row, and §7.4's closing Note says why *and* §21.7
  repeats it. That is a consistent, well-executed idiom — which is precisely what
  makes its one omission visible (register-03).
- `[R-COD-08]` decomposes into three conditions (output size, input consumption,
  malformedness) and the register carries all three: T3 (governing `[R-SER-07]`, citing
  R-COD-08), T24, T25.
- Every one of §7.2's, §6.2's, §7.4's and §15.3's field-by-field constraint lists has a
  row for each field. I checked the trailer field by field (all eleven fields plus the
  two derived sums), the record header field by field (all five), the layer record's
  inline payload field by field (all sixteen entries of §7.4's table), and the index
  entry field by field (all three). No field is left ungoverned.

### 4.2 Rows → rules

Every row registers something the rules do make a violation. The ones where the
answer is not immediate:

- **F19** (any incompat-lane bit set). `[R-CNT-08]` carves the ignore lane out of
  file conformance — "a set ignore-lane bit is not a file-conformance violation" — and
  carves nothing out for the incompat lane, while requiring "a writer creating a file
  under this text MUST write flags = 0". §10.1's four growth vehicles include "New
  ignore-lane flag bits" and *not* incompat-lane bits, so no minor version can ever
  define one inside major 1. F19's reject-file is therefore right, and §21.6's
  "conforming files a reader nevertheless refuses" is right to name only two cases.
- **R1's reserved-range half.** Is emitting metadata encoding 3–0x7F a violation, when
  emitting an experimental one is not? Yes: `[R-EXT-03]` says "a value from a reserved
  range MUST NOT be emitted at all before this specification assigns it", while
  §10.3's experimental prohibition is conduct (`[R-CNF-02]`, §2.3). §21.5's preamble
  gets this exactly right, including the subtle part: "what `[R-MTA-10]` withdraws is
  the document's content rules, never the encoding byte's own value set".
- **R2 at an experimental encoding.** §21.5's preamble excepts "an experimental-range
  encoding, where no document rule attaches". Does that exempt the extent CRC? No —
  `[R-MTA-10]` names the terminal CRC as one of the three structural checks that
  survive ("the record's framing and extent slot …, the encoding byte's own value set
  …, and the extent's terminal CRC"), and the CRC covers "the encoded bytes exactly as
  stored, before decoding" (§8.1), so it precedes the document. The word doing the
  work is "document rule". Tight, but correct.
- **T2 and T4 jointly covering `[R-SER-08]`.** T2's condition asserts it ("the same
  byte at a padding position is T4's, the two rows together covering `[R-SER-08]`").
  I checked: `[R-SER-08]` binds every interleaved bool value byte; T2 takes the real
  positions and T4 (via its "interleaved bool fill byte" instance) takes the padding
  ones; a bool fill byte is itself constrained to 0x00/0x01 by `[R-TYP-07]`/L35, so
  the union is exact. Correct.

### 4.3 The §21.6 side

§21.1 explicitly removes §21.6 from the completeness clause ("neither this
completeness clause nor the instance arithmetic below reaches §21.6's defined
non-violations"), so I checked §21.6 for correctness rather than completeness. Its
fourteen rows all check out against their cited rules. I spent time on one candidate
gap — §21.5's preamble says "§21.6 lists the ignore-record conditions that are not
violations", and the reader's or verifier's decline on the size bound or the frame
window is ignore-record and is not a violation, yet has no §21.6 row. I decided this
is not a defect: §21.6's table is headed "Condition", its intro is "A reader that
treats any of them as a failure is the nonconforming party", and §21.5's own preamble
already classifies the decline as "that actor's capability and **not a fact about the
file**" — so it is not a condition of the file and does not belong in that table.
Recording the reasoning rather than the finding.

## 5. Every cross-reference to a row

Fifteen citations of row labels from outside the tables. I resolved each.

| Where | Cites | Verdict |
|---|---|---|
| §5.2 `[R-CNT-21]` L646 | L18, L40–L42 | ✓ all four are verifier/reject-layer rows established by the coverage walk itself (overlap; alignment; run continuity; run alignment) |
| §9.6 `[R-LIF-06]` L1299 | F8, F17 | ✓ both reachable: F8 for residue/tear, F17 for a truncation landing on an earlier trailer. Not exhaustive (F14 is also reachable), but §9.5's Note gives the full three |
| §17.2 Note L2267 | T24 | ✓ "bytes remain in the stored extent after the stream … ends" |
| §18.2 `[R-MTA-09]` L2472–2504 | R3, R4 | ✓ R3 = decode failure, R4 = frame constraints; the routing sentence matches R4's condition cell word for word in substance |
| §20.3 L3026 | L44 | ✓ the lz4 decoded-size cap |
| §20.5 `[R-WRT-06]` L3224–3226 | F36, L25 + L31, L33, L34, L36, L43, L45, R1 | ✓ **checked arithmetically**: §10.2 tabulates 8 spaces; minus record type = 7; the seven rows map one-to-one onto layout, linearization, sample type, codec, filter, index encoding, metadata encoding. Exactly one row per space, and I confirmed no space has a second reserved-range row anywhere |
| §21.1 L3342 | F1/F6/F8, F35/F36, L24/L25 | ✓ each is a strict specialization, and in the two pairs whose detectors differ (F35 reader vs F36 verifier; L24 reader vs L25 verifier) the rule "the narrower row's detector and detection point are the ones that apply" does real work |
| §21.1 L3361/L3363 | T24, T15, T25 | ✓ T24's cell literally reads "any codec"; T15 and T25 enumerate members of a family |
| §21.1 L3391 | F27, L48 | ✓ both are the `[R-MTA-05]` pair |
| §21.2 L3405–3407 | F8, F14, F6, F1 | ✓ four rows; and the four are exactly the rows whose subject `[R-CNT-24]` fixes across every major (trailer magic at F−64, the CRC at F−4, the front block). F15 is correctly *not* among them — trailer bytes [56,60) lie inside the 48 a future major may redefine. But see register-01 |
| §21.6 L3628–3630 | F18, F35, F36, L24, L25 | ✓ |
| §21.7 L3658 | T2, T4, T5 | see register-02 |
| §21.7 L3668 | T3, T14 | ✓ "T14 the entry's declared length, T3 the decoded payload's own" is exactly the two rows' subjects |
| §21.7 L3673 | T15, T17, T23, T25 | ✓ as the rows that test stored bytes *as a stream of the declared codec*; T24 and T18–T22 also witness some codec changes, but the sentence is hedged ("*sometimes*") and creates no obligation either way |
| §21.7 L3678–3681 | T26, T2, T4 | ✓ against T26 — but in tension with L3658, see register-02 |
| App. H L4429/4431/4432/4441 | F1, F6, F7, F36, L25, R1 | ✓ all resolve; the F1/F6 line correctly states the verifier's lack of `[R-CNT-04]`'s residency exemption |

## 6. The outcome vocabulary

§2.4 defines five values. Four are reader outcomes and each heads exactly one register
subsection: reject-file (§21.2), reject-layer (§21.3), reject-tile (§21.4),
ignore-record (§21.5). The fifth, **preserve-verbatim**, is not a reader outcome —
`[R-CNF-07]` lists only four, and §2.4 says preserve-verbatim "names an updater
obligation, orthogonal to reader outcomes" — so its absence from the register is
correct, and it is reachable through §20.4's table, which §2.4 names ("its MU = 1 and
MU = 0 / PE = 1 rows"). No row carries a value the document does not define, and every
defined value is reachable. Nothing to report.

## 7. Limits, both directions

### 7.1 §21.9's minimum guarantees

Eight rows. Cross-checked against every other statement:

- Appendix B's "Reader minimum guarantees" line lists the same eight values in the
  same units. ✓
- §2.5 `[R-CNF-10]` and §2.3 `[R-CNF-03]` both point at the table and state the same
  duty; §21.9 `[R-ERR-03]` states it a third time. All three agree. ✓
- §17.2 `[R-COD-06]` and §18.2 `[R-MTA-09]` both cite the 8 MiB `Window_Size` row, and
  §18.2 cites the 16 MiB document row. ✓
- §24 `[R-VEC-03]` and Appendix D both cite the entry_count row. ✓

The §21.9 Note's arithmetic reproduces:
- 2³² entries ⇒ ⌈2³²/2¹⁶⌉ × 4 = 2¹⁶ × 4 = 2¹⁸ = **256 KiB** ✓; at 2³⁶ ⇒ 2²⁰ × 4 =
  **4 MiB** ✓.
- 65,536 layers × 200 bytes = 13,107,200 = **12.5 MiB** ✓, against the 16 MiB
  directory row.
- 256 MiB against §11.3's "roughly 1 to 16 MiB" ordinary tile = 16×, "an order of
  magnitude above" ✓.
- Minimum viable layer record: 24 header + (2 name + 34 scalars + 18 dim + 6 chan + 13
  trailing) = 97 bytes, so 65,536 layers fit in ~6.4 MiB — the two rows are jointly
  satisfiable, which is what the Note's "that same budget over the region itself"
  claims. ✓

The per-instance paragraph's quantifiers are sound. "*Decoded size of one tile* ranges
over a layer's **addressed** tiles, stored or not, exactly as `[R-COD-07]`'s cap is" —
I checked the analogy, since analogies are where this document has bled before:
`[R-COD-07]` reads "for a layer **any of whose addressed tiles'** decoded size exceeds
0x7E000000", and §17.2's Note confirms "The cap is quantified over the layer's
*addressed* tiles, so a layer that addresses none … satisfies it whatever its tile
shape declares". The analogy is about the quantifier only (one is a validity cap, the
other a floor on acceptance), and on the quantifier it holds. ✓

I tested the "one quantity named where two are in play" shape here at length. The
family {layers per file, dir_length} is the case where the document *does* carry both
siblings and explains why. The family {decoded tile size, stored tile length} is the
case where it carries only one — a conforming reader must accept a file whose stored
tile extent is arbitrarily long provided its decoded size is within 256 MiB, because
`[R-CNF-03]`'s condition is "none of whose values exceeds the minimum guarantees" and
a quantity with no row cannot exceed one. I convinced myself this is *decided* rather
than ambiguous (so not a finding): §22.2's three bounding properties are about
amplification, which is unaffected, and the stored length is bounded by the file's own
length, which the attacker pays for. Recording it as a checked-and-cleared line rather
than a finding.

### 7.2 §21.9's hard limits

Nine entries. Each checked against its defining section: §4.6 (names), §18.2 (keys),
§7.4 (rank u8 / C u16, A, A_slab, S), §17.2 (`0x7E000000`), §4.2 (2⁶³−1), §16.1/§16.2
(A, A_slab), §6.2 (dir minimums), §5.1 (128 bytes). **No entry states a bound its
defining section states differently.** The closing claim — "Most follow from a field's
width, an external format, or the value domain, and the rest from arithmetic over
structures a generation cannot omit. Two do not" — holds: the 512 floor on A and the
255-byte key cap are the only two that are neither, and the 2⁶² ceilings on A and
A_slab do follow from the value domain (2⁶² is the largest power of two ≤ 2⁶³−1).

In the other direction: §7.1's `extent_length ≥ 5` is a hard bound stated elsewhere
and *not* in §21.9's list, even though its sibling ("a directory of at least 4 bytes
at an offset of at least 16") is. I did not report this, because §21.9 disclaims
inventory status in terms — "The hard limits it restates are a finding aid rather than
an inventory — each is normative where the structure forcing it is defined." Appendix
B carries it. Same disposition for §6.4's 65,536-byte discovery window (a SHOULD) and
§11.3's 1–16 MiB guidance.

## 8. Building things, and where I had to guess

### 8.1 Every worked number in the document reproduces

I implemented CRC-32C to §4.5's parameters and confirmed:

- `CRC-32C("123456789")` = `0xE3069283`; `CRC-32C(∅)` = `0x00000000` — §4.5's check
  vector.
- Appendix A's trailer: I rebuilt trailer bytes [0,60) from the field table (magic,
  major 1, minor 0, flags 0, generation 1, dir_offset 16, dir_length 4,
  committed_file_length 128, file_id 0x0123456789ABCDEF, reserved 0) and got
  `8a 4e 52 41 54 0d 0a 1a 01 00 00 00 00 00 00 00 01 00 …` — byte-identical to the
  hex dump at [64,124) — and `CRC-32C` = `0xE00938D2`, stored `D2 38 09 E0`. Matches.
- §7.4's example: CRC-32C over four sentinel entries (80 bytes of `FF×16 00×4`) =
  `0x80A34955`; CRC-32C over the 4-byte array `55 49 A3 80` = `0xC4EE982E`. Both
  match.
- §15.4/Appendix B's all-sentinel full-segment constant: CRC-32C over 2¹⁶ sentinel
  entries = `0xEECB3BB2`. Matches.
- §7.4's payload layout: 4 (name) + 34 (nine scalars) + 18 (dim entry) + 12 (channel
  entry) + 13 (trailing) = 81, and the hex dump's offsets (0,4,5,7,9,11,19,27,35,36,
  38,40,48,56,63,68,69,77 + 4) land on 81 exactly. Extent length 4×20 + ⌈4/2¹⁶⌉×4 =
  84. All match.
- §15.4's million-entry example: 16 segments (15 full + 16,960), 64-byte array, region
  20,000,064 bytes, entry 999,999 at segment-relative byte 339,180, array at
  [20,000,000, 20,000,064), segment 15 at [19,660,800, 20,000,000), one full segment =
  1,310,720 = 1.25 MiB. All match.
- §11.4, §14.2, §14.3, §14.5, §17.3 examples all recompute correctly (spatial ordinal
  10, in-tile ordinal 11,452, planar disk ordinal 74; Q=3 decoded 18 and Q=5 decoded
  30; `55 01` / `55 FD`; 32-byte edge tile; the three-float32 shuffle).

Nothing in the document's arithmetic is wrong. That is worth saying plainly, because
it means the findings below are all about *text*, not about numbers.

### 8.2 Degenerate files the document permits

I worked these to see what the register says:

- **Zero layers, 128 bytes.** §21.6 row 4 ✓, Appendix A ✓.
- **A layer with a zero-extent dimension declaring codec 4 and a tile shape whose
  decoded size is 4 GiB.** Conforming: L44's quantifier is "any of whose **addressed**
  tiles", and there are none. §17.2's Note blesses it and warns the escape is not
  durable; §20.3 step 4 repeats the warning ("which an empty layer escapes only because
  that cap is quantified over addressed tiles"); §21.9 repeats it a third time. Three
  statements, one quantifier, all agreeing. Good.
- **The same layer with `[R-ENC-04]`'s overflow rule.** §17.2's Note draws the
  contrast correctly: "`[R-ENC-04]`'s overflow rule carries no such quantifier … so
  P·Q and P·Bᶜ are checked in an empty layer even though this cap is not", and L2 does
  list P·Q and P·Bᶜ.
- **A zero-filled index region.** offset 0 / length 0 / crc 0 is not a sentinel, so it
  fires both T10 (length 0) and T8 (offset < 16). Two rows, one file — which §15.3's
  own table also does, and which `[R-VEC-02]` provides for. §15.2's rationale predicts
  exactly this ("loudly invalid (§15.3)").
- **An all-0xFF index region.** offset=S, length=S, crc=0xFFFFFFFF → T6, exactly as
  §15.2's rationale says.
- **A packed bool plane with P=1.** ⌈1/8⌉ = 1 byte, seven pad bits, T5 constructible.
- **A layer whose slab runs contain no stored tile.** `[R-SLB-03]`: "A run with no
  stored tiles imposes nothing." L41/L42 vacuous. ✓
- **A file whose live trailer points at a *prior* generation's directory.** This is
  the one that produced a finding — see register-03. The bytes between that directory's
  end and the live trailer are superseded structures, which §5.2 makes slack rather
  than structures, so F7 does not fire; `[R-CNT-05]` says a longer-than-a-pad gap "is
  conforming"; §2.3 names that gap as one of the two writer obligations expressly
  outside file conformance. Every check passes.

### 8.3 The one place I had to compute rather than read

§21.7 and T26 disagree (see register-02) about whether a pad-bit check can witness a
mis-strided filter. The document does not answer it in words, so I computed. §17.3
defines the shuffle as: viewing the image as n = L/s groups of s bytes, byte *i* of
group *j* goes to offset i·n + j. Solve for the pre-image of the last offset L−1:
i·n + j = s·n − 1 with 0 ≤ j < n forces j = n−1 and i = s−1, whose source offset is
(n−1)·s + (s−1) = L−1. **The byte-shuffle fixes offset L−1 for every stride s that
divides L** (and offset 0 likewise). §17.3's own worked example confirms it: the
decoded bytes end `40` and the shuffled bytes end `40`. Since a packed plane's pad bits
live in the final byte and their required content is the plane's fill bit — a function
of P and the recorded fill, neither of which a stride error touches — the reader's
decoded image always carries the writer's true final byte, so T5 can never fire on a
stride error. T26's "T2's or T4's" is therefore *correct*, and §21.7's L3658 sentence
is the loose one. I would not have been able to settle this from the text alone; the
document does not state the fixed-point property anywhere.

## 9. Findings

### register-01 — AMBIGUITY

**Location.** §21.2 preamble; §2.3 `[R-CNF-02]`, `[R-CNF-11]`; §21.6 closing
paragraph.

**Quotation.** §21.2: "A file declaring a format major other than 1 is neither
conforming nor nonconforming under this text (§2.3, `[R-CNF-02]`), and the rows below
whose subject is that file's *geometry* do not reach it … Four rows are outside that
reasoning and do reach it, because their subject is a field fixed across every major
(`[R-CNT-24]`)". §2.3: "a file declaring another major is neither conforming nor
nonconforming under it: a reader refuses such a file on capability grounds (§6.3,
`[R-CNT-07]`), and that refusal is not a finding about its bytes."

**The problem.** §21.1 defines a register row as "one malformed condition" among
"every detectable **file-conformance violation** this specification names". So a row
that "reaches" a file is a row that can make that file nonconforming. §21.2 says four
rows reach a file that §2.3 says is neither conforming nor nonconforming. Take the
concrete case the preamble's own reasoning admits: a file with a valid trailer magic,
a verifying trailer CRC, `version_major` = 7, and a front signature block that is not
byte-identical to the constant. The magic and CRC pass, so the file *has* validly
declared major 7; F6 fires on the front block, which `[R-CNT-24]` and §6.1 fix in every
major.

What does a verifier report? §2.3 gives it a *cannot establish* ground in terms — "as
when the file names a format major version it does not implement" — and also gives a
priority rule — "An established violation takes priority: a verifier that has
established any violation reports *nonconforming*". Whether F6 on a major-7 file is an
"established violation" is exactly what §21.2's sentence leaves open.

**Permitted readings.**
(a) "Reach it" carries its register meaning: the row's condition, exhibited by such a
file, is a file-conformance violation, because `[R-CNT-24]` is a requirement this
document states about *every* major's bytes. §2.3's "under it" then means "under
format major 1", and a foreign-major file can still be nonconforming on the four
permanent fields. A verifier reports **nonconforming**.
(b) "Reach it" means only that a reader still performs the check and rejects on it,
with no conformance verdict attaching; §2.3's "neither conforming nor nonconforming"
governs absolutely, and §21.6's "the file **can be perfectly conforming under that
major**" describes the whole class. A verifier reports **cannot establish**.

**I pick (a).** Under (b) the sentence "Four rows are outside that reasoning and do
reach it" has no register content at all — it would be asserting something about
reader behaviour inside a subsection §21.1 defines as an enumeration of conformance
violations — and the justification it gives ("their subject is a field fixed across
every major") is a claim about bytes, not about reader ordering. Reading (a) is also
what makes F1's trailer-magic instance coherent: `[R-ENC-02]`'s byte-reversed
signature must be rejectable without regard to any declared major.

**What an implementer does wrong without it.** A verifier handed a major-7 file whose
front signature block is byte-reversed reports *cannot establish* — telling its
operator that the file might be fine under major 7 — when this document has stated
that its front block is wrong in every major. The mirror error is a verifier that
reports *nonconforming* for a file this document declines to judge.

**Byte-level: no.** Both readings leave every reader at reject-file (either on the
version gate or on F6), and neither verifier certifies. Only the verdict *label*
differs, and the set of files a conforming verifier certifies is identical under both.
No writer can emit a major-7 file under this text, so the emittable set is untouched.

### register-02 — AMBIGUITY

**Location.** §21.7, first sentence of the second paragraph; §21.4 row T26; §21.7,
later in the same paragraph.

**Quotation.** §21.7: "the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are
satisfied by a structurally valid tile whatever values it carries, except where §14
constrains a byte's content — a padding position, a pad bit, or an interleaved boolean
— and a mis-ordered image is then witnessed by T2, T4 or T5, **exactly as a
mis-strided filter is**". Against T26: "Filter 2 applied at a stride other than the
mandated one, where the resulting image breaks §14.5's padding content or
`[R-SER-08]`'s bool bytes … **the check that detects it is T2's or T4's**". And
against §21.7 twenty-two lines later: "the check that detects it is T2's or T4's,
**exactly as T26 has it**".

**The problem.** A mis-ordered image genuinely has three possible witnesses. A writer
that packs a boolean plane MSB-first inside each byte pushes real values into the bit
positions §14.3 designates as pad bits, so with P = 10 the spec-required pad bits 2–7
of byte 1 hold values 8 and 9; if either differs from the fill bit, T5 fires. So "T2,
T4 or T5" is right for a mis-ordering.

A mis-strided filter has only two. §17.3's shuffle sends byte *i* of group *j* to
offset i·n + j with n = L/s; the pre-image of offset L−1 is i = s−1, j = n−1, whose
source offset is (n−1)s + (s−1) = L−1 — the shuffle fixes the last byte for every
stride dividing L, and §17.3's own example ends `40` before and after. A packed
plane's pad bits live in that byte and their required content (the plane's fill bit)
is a function of P and the recorded fill, which no stride error changes. Interleaved
tiles and planar numeric planes have no pad bits at all. So T5 can never witness a
wrong stride, and T26's two-row list is correct — which is exactly what the "exactly
as" then over-claims.

**Permitted readings.**
(a) "exactly as a mis-strided filter is" asserts the same witness set, attaching to
the immediately preceding "T2, T4 or T5". Then it contradicts T26 and §21.7's own
later sentence, and a reader concludes a pad-bit check can catch a stride error.
(b) "exactly as" attaches only to the manner — witnessed *only* where §14 structurally
constrains a byte — and not to the row list. Then the passage is sound.

**I pick (b) as the intended meaning and (a) as the natural one.** The clause sits
immediately after the three-row list with nothing separating them, and §21.7 is the
one section whose purpose is to say precisely which witnesses exist; §21.1 makes the
register's completeness normative and §21.7 "the account, by class, of what fails
it", so an enumeration here is read as a claim.

**What an implementer does wrong without it.** A corpus builder or a verifier author
concludes that a stride error on a packed boolean plane is catchable by the pad-bit
check, and either builds a vector that cannot exist or records a coverage claim the
format cannot honour. T26 already says the honest thing — "a wrong stride with no such
structural constraint is undetectable" — and for a packed bool plane with no padding
position the *only* witness is none at all.

**Byte-level: no.** T5 is a verifier MUST under `[R-SER-05]` regardless of which
sentence one believes, and T2/T4/T5 all carry reject-tile at certification. No
implementation's accept/reject verdict on any byte sequence turns on it; what turns on
it is a coverage claim.

### register-03 — AMBIGUITY

**Location.** §21.7, second paragraph (the closed list of obligations omitted from the
register); §9.2 `[R-LIF-02]` step 3 and its Note.

**Quotation.** §21.7: "A second set of obligations is omitted from the register
because a single file exhibits no witness of their violation. Committed-prefix
immutability and the generation sequence (`[R-LIF-01]`, `[R-LIF-03]`) are properties of
a file's history, which §9.7 does not reconstruct; …" — and the list runs on through
`[R-GEO-06]`/`[R-SER-01]`, `[R-CNT-13]`'s MU = 0 offset prohibition, `[R-CNT-18]`'s
nesting prohibition, §20.3 step 4's bar, `[R-WRT-06]`'s four trailer obligations, and
"`[R-ENC-06]`'s fixed field widths", with no member for `[R-LIF-02]`. Against §9.2's
Note: "Step 3 is not discharged by a directory an earlier generation appended: each
commit appends its own complete directory, and the trailer of step 5 addresses that
one. **A writer that re-points a new trailer at a prior generation's directory region
has left step 3 unperformed.**"

**The problem.** I built that file. Generation *n*+1 writes only a pad and a trailer,
and points `dir_offset` at generation *n*'s directory region. Walk it: the trailer
magic, CRC, version and flag gates pass; `committed_file_length` equals the file size;
`dir_offset ≥ 16`; `dir_length ≥ 4`; `dir_offset + dir_length ≤ F − 64`; the directory
CRC verifies over an intact record sequence; every record's extents are in range and
disjoint. The superseded directory, pad and trailer of generation *n* now lie between
the live directory's end and the live trailer — but §5.2 makes them **slack**, not
structures ("Every byte the live state does not claim is **slack**: … everything an
earlier commit superseded"), so F7 does not fire, and `[R-CNT-05]` says of that gap
"a longer gap is conforming, and no conforming commit produces one", which §2.3 lists
as one of the two writer obligations "this specification expressly declares not to be
a file-conformance violation". The file is conforming and the step-3 violation has no
witness whatever.

That is precisely the class §21.7's second paragraph exists to enumerate, and
`[R-LIF-02]` is not in it. The omission is visible because the document's idiom
elsewhere is unusually disciplined: §7.4's closing Note says the nesting bar "has no
reader-detectable witness, and so no register row"; §9.5's Note says residue past a
completed commit "carries no register row of its own"; §16.2's Note says a stale slab
declaration "carries no register row of its own". §9.2's Note identifies the violable
case and then says nothing about the register.

**Permitted readings.**
(a) The list is closed (its members are semicolon-separated and it terminates with
"and `[R-ENC-06]`'s …"), so §21.7 asserts these *are* the unwitnessed obligations, and
`[R-LIF-02]` step 3 is an omission from a normative account.
(b) "`[R-LIF-01]`, `[R-LIF-03]`" is illustrative of the class named in the same breath
— "properties of a file's history, which §9.7 does not reconstruct" — and step 3 is a
member of that class even though unnamed, so nothing is missing.

**I pick (a).** Every other member of the list is named by identifier, and two of them
(`[R-CNT-13]`'s and `[R-CNT-18]`'s prohibitions) are individual clauses of larger
rules rather than whole requirements — the list's granularity is clause-level, not
class-level, which is what makes it read as an inventory. §21.1 leans on it: it calls
§21.7 "the account, by class, of what fails" the detectability gate, so a reader
checking whether an obligation is owed a row consults this list.

**What an implementer does wrong without it.** A verifier author reads §21.7,
concludes that every obligation not listed there is either registered or detectable,
and goes looking for a way to establish that the live directory was appended by the
commit that wrote the live trailer. There is none — the live state cannot distinguish
it from a conforming no-op commit — and time is spent discovering that the hard way. A
corpus builder makes the mirror error and tries to construct a vector.

**Byte-level: no.** No file exhibits a witness under either reading, so no reader or
verifier can behave differently; both readings leave the file conforming and every
implementation certifying it.

### register-04 — CONTRADICTION

**Location.** §21.5, row R7 (Condition cell versus Instances cell); §21.1's instance
arithmetic; §18.2 `[R-MTA-04]`.

**Quotation.** R7's Condition: "A decoded user-metadata document is not well-formed
JSON, or its top-level value is not an object". R7's Instances: "not well-formed JSON,
top-level document; not well-formed JSON, layer sub-record document; top-level value
not an object, top-level document; top-level value not an object, layer sub-record
document; **leading U+FEFF, top-level document; leading U+FEFF, layer sub-record
document**". §21.1: "An instance names a field the condition ranges over, a container
it can occur in, **one of several alternatives the condition text states**, or any
combination of the three". `[R-MTA-04]`: "**A JSON object, unmarked.** The top-level
value is an object, and the encoding carries no byte-order mark: a leading U+FEFF
makes the document unreadable."

**The problem.** `[R-MTA-04]`'s first restriction has three limbs — well-formed JSON,
object at top level, and no byte-order mark — and the BOM limb exists precisely
because it is *not* redundant in practice: RFC 8259's grammar excludes a leading
U+FEFF, but real parsers routinely skip it, which is why the rule states it
separately. R7's Instances cell counts the BOM as its own alternative, giving three
alternatives × two containers = six. R7's Condition cell states only two of the three.

Under §21.1's own arithmetic an instance may enumerate "one of several alternatives
**the condition text states**", and the condition text as written states two. The row
therefore supports four instances, not six, and §21.8's total of 277 — which I verified
depends on R7 contributing six — does not follow from the cells as written. §21.1's
tie-break ("where a row and the rule it cites diverge, **the rule governs**") rescues
the substance: `[R-MTA-04]` does bar the BOM and does make such a document
ignore-record. What it does not rescue is the register's own claim that "the count is
therefore mechanical once the cell is written".

**Which governs.** The rule. `[R-MTA-04]`'s three-limb restriction is the operative
text; R7's Condition cell is a defective restatement of it, and the six instances the
cell enumerates are the right six.

**What an implementer does wrong without it.** Someone recomputing §21.8's totals from
the Condition cells — the check §21.1 says is mechanical — gets 275 and reports a
counting defect that is not there. More consequentially, a reader who takes R7's
Condition cell as the register's statement of `[R-MTA-04]`'s first restriction ships a
metadata parser that tolerates a leading BOM, since a BOM-skipping parser will report
the document as well-formed JSON with an object at top level and R7's condition, as
written, is then not met.

**Byte-level: no.** `[R-MTA-04]` governs and unambiguously makes a BOM-led document
unreadable, and §21.1 says so; the divergence is inside the register table, so no
competent implementation reading `[R-MTA-04]` reaches a different accept/reject
verdict. The cost is a defective finding aid and a mis-set expectation for anyone who
reads the table without the rule.

### register-05 — OBSERVATION

**Location.** §21.2 rows F30 and F31; §21.3 rows L15 and L16; §7.2 `[R-CNT-13]`.

**Quotation.** F31: "A non-layer top-level record's nonzero extent slot has
extent_offset **in 1-15**, placing the extent inside the front signature block".
L16: "A layer record's or sub-record's nonzero extent slot has extent_offset **< 16**,
pointing into the front signature block". `[R-CNT-13]`: "The **extent slot**
(extent_offset, extent_length): (0, 0) means no extent. Any other combination with
either half zero, an **extent_offset < 16**, an extent extending past F − 64, or an
overflowing sum is a validity error at the scope the record governs".

**The problem.** One rule, two register renderings of the same clause, with different
boundaries. `[R-CNT-13]` says `< 16`, so under the rule the slot (0, 5) violates both
the either-half-zero clause and the offset clause. F30/F31 partition that overlap away
by narrowing F31 to `1-15`, so at file scope the two rows are disjoint. L15/L16 do not
narrow, so at layer scope they overlap on exactly the slots F30/F31 separate.

§21.1 decides which governs: "each row *restates* its governing rule, and where a row
and the rule it cites diverge, **the rule governs**." F31's `1-15` is a divergence from
`[R-CNT-13]`'s `< 16`, so the narrowing F31's text performs has no normative force,
and the file-scope pair overlaps under the rule exactly as the layer-scope pair does.
The register's own text therefore describes a partition the rule does not make, and
describes it inconsistently between two rows that restate the same clause.

Note that §21.1's specialization machinery does not reach this: L15 is not a strict
specialization of L16 (L15 also covers `(5, 0)`, which L16 does not), so "a file
exhibiting a specialization is recorded against the narrower row" gives no answer, and
the case falls instead to `[R-VEC-02]`'s provision for conditions that cannot be
isolated. In practice a corpus can dodge it — a vector at offset 1–15 exercises F31 or
L16 alone — so the whole consequence is attribution for the single slot (0, nonzero).

**Which governs.** The rule: `extent_offset < 16` at both scopes.

**Why OBSERVATION and not a defect claim.** Deciding it costs nothing, but it is
disproportionate to call it wrong: both rows carry reject-file / reject-layer
respectively, both carry Detector *reader*, both are due at the same tier as their
sibling, and no reader or verifier behaves differently under either rendering. What is
worth recording is that the register states a boundary its rule does not state, and
states it in only one of the two places the same clause appears — which is the kind of
asymmetry that has to be looked at once and then can be dismissed.

**Byte-level: no.** Identical outcome, detector and detection point on either reading;
the union of the two rows covers the rule's clause exactly either way.

## 10. Things I checked and cleared, recorded so they are not re-checked

- §21.8's two totals (121, 277) reproduce mechanically. Every worked CRC and every
  worked byte layout in the document reproduces.
- All 20 verifier rows have Detected = certification and vice versa; no leakage.
- All 15 external and internal citations of row labels resolve to rows saying what the
  citing text claims, including §20.5's seven-space enumeration (L31, L33, L34, L36,
  L43, L45, R1), which I verified is one row per space with no space carrying a
  second.
- Every trailer field, record-header field, layer-record payload field and index-entry
  field has a register row. No field is ungoverned.
- All five outcome values are defined and reachable; the register uses only the four
  reader outcomes, correctly.
- §21.9's minimum guarantees agree with Appendix B, §2.3, §2.5, §17.2, §18.2 and §24;
  its hard limits agree with every defining section; its Note's arithmetic reproduces.
- §21.5's carve-outs (experimental encoding, actor decline) do not accidentally exempt
  R2, because `[R-MTA-10]` names the terminal CRC among the surviving structural
  checks.
- F19's reject-file is right, and §21.6's "two capability refusals" are right to be
  two, because §10.1's growth vehicles admit no new incompat-lane bit inside a major.
- T2 ∪ T4 covers `[R-SER-08]` exactly, and T26's two-row witness list is correct (see
  §8.3 for the computation).
- `[R-SLB-04]`, `[R-LIF-04]` and `[R-CNT-18]`'s nesting bar are each accounted for by
  an explicit "no register row" Note where they arise. `[R-LIF-02]` step 3 is the one
  that is not — register-03.
- R10 is the only §21.5 row that cites `[R-CNT-25]` neither as governing nor in
  parentheses; the outcome is still derivable from `[R-MTA-04]`'s lead-in and from
  §21.1's blanket assignment, so I did not raise it as a finding.
