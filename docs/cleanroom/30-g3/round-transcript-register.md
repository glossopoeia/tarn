# Round 30 — Register hunter — transcript

## Access and disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` only, in full (4,743 lines, in eight Read calls covering lines 1–4743). No other file was opened. No git, no web, no directory listing. My runtime placed a project-instruction file and an index of the maintainer's memory notes into my context before I began; I did not open any of those files and did not act on anything they said. The brief itself names §21 and nineteen changed passages; I used that only for where to look.

Scratch files written, all under `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-round/scratch/register/`:
- `count_instances.py` — parses the four register tables and counts rows and semicolon-separated instances per §21.1's arithmetic.
- An inline Python sweep (heredoc, not saved) that normalised the document's whitespace and `> ` blockquote markers before pattern matching, plus a line-oriented control.

## Method

1. Read §21 (lines 3573–4052) first, then the rest of the document in order.
2. Counted conditions and instances mechanically from the table cells.
3. For every row, located the governing requirement and compared condition wording, outcome/scope, detector and detection point.
4. Swept every `validity error` / `MUST treat` clause in the document for a row; swept the rows for a rule making the condition a violation.
5. Resolved every row-label citation outside the tables (F/L/T/R labels) to its row and checked the citing claim.
6. Compared §21.9's guarantees and hard limits against every other statement of a limit (Appendix B, §4.6, §7.4, §16, §17.2, §18.2, §2.5, §1).
7. Checked the outcome and detection-tier vocabularies.

Wrap hazard control: the phrase `the record carrying a user-metadata document, as §18.2 assigns` returns **0** with line-oriented grep and **1** after whitespace normalisation; every zero I relied on below came from the normalised search.

## Derived numbers

| Quantity | Derived | Document says | Match |
|---|---|---|---|
| §21.2 conditions | F1–F36 less F11 = 35 | 35 (line 3663) | yes |
| §21.3 conditions | L1–L49 = 49 | 49 (3718) | yes |
| §21.4 conditions | T1–T26 = 26 | 26 (3778) | yes |
| §21.5 conditions | R1–R10 = 10 | 10 (3828) | yes |
| Total conditions | 120 | 120 (3956) | yes |
| Instances F | 56 | — | — |
| Instances L | 116 | — | — |
| Instances T | 55 | — | — |
| Instances R | 50 | — | — |
| Total instances | 277 | 277 (3956) | yes |
| [R-CNT-06] conditions | F8, F9, F10, F12, F13, F14, F15, F16, F17 = 9 | "nine" (§2.3 line 253, §21.7 line 3939) | yes |
| Reaching rows per [R-CNF-13] | F8 (magic), F14 (CRC), F6 (front block), F1 both instances | same (§21.2 line 3665) | yes |
| §10.2 spaces other than record type | layout, linearization, type, codec, filter, index enc, metadata enc = 7 | L36, L33, L34, L43, L45, L31, R1 (§20.5 line 3481) | yes |
| R4 instances | 8 constraints × 2 containers = 16 | 16 cells | yes |
| Segment-CRC array at 2³² entries | 2¹⁶ × 4 B = 256 KiB; at 2³⁶ = 4 MiB | §21.9 Note | yes |
| 65,536 layers at 12.5 MiB | 200 bytes/record | "small layer records" | plausible |
| Minimum file | 16 + 4 = 20 → trailer at 64 → F = 128 | 128 | yes |
| §7.4 example index region | 4×20 + 1×4 = 84 | 84 | yes |
| §15.4 example region | 20,000,064 bytes, 16 segments | same | yes |
| §21.9 guarantees table | 8 rows: 5 declaration rows + 3 per-instance rows | "last three … first five" | yes |

Instance counts per row (from `count_instances.py`): F1 2, F2 5, F3 2, F4 1, F5 2, F6 2, F7 4, F8–F16 1 each, F17 2, F18–F22 1, F23 2, F24–F27 1, F28 2, F29 3, F30 2, F31 1, F32 1, F33 5, F34–F36 1; L1 8, L2 9, L3 1, L4 2, L5 1, L6 1, L7 2, L8 2, L9 2, L10 1, L11 1, L12 2, L13 1, L14 3, L15 4, L16 2, L17 2, L18 3, L19 1, L20 1, L21 4, L22 4, L23 4, L24–L28 1, L29 3, L30 2, L31 3, L32 3, L33 4, L34 4, L35 1, L36 2, L37 1, L38 1, L39 3, L40 1, L41 3, L42 1, L43 3, L44 3, L45 3, L46 2, L47 2, L48 1, L49 4; T1 1, T2 1, T3 6, T4 4, T5 1, T6 1, T7 2, T8–T10 1, T11 2, T12 1, T13 2, T14 6, T15 2, T16–T17 1, T18 2, T19–T20 1, T21 3, T22 6, T23 1, T24 1, T25 3, T26 3; R1 4, R2 2, R3 2, R4 16, R5 8, R6 4, R7 6, R8 4, R9 2, R10 2.

## Row-versus-rule walk (summary of what I checked, row by row)

§21.2: F1 ↔ [R-ENC-02] (byte-swapped signature → reject-file; residency exemption restated from [R-CNT-04]) agrees. F2/F3 ↔ [R-ENC-03]/[R-ENC-04]; dir_offset+dir_length and extent sums are expressly designated in §6.2 and §7.2. F4 ↔ [R-ENC-15] and §19.1 step 4 agree on raw-byte comparison within inline_length. F5 ↔ [R-CNT-27]. F6 ↔ [R-CNT-04]. F7 ↔ [R-CNT-05] ("A verifier MUST treat a structure in that gap as a validity error at file scope"); the longer-gap non-violation has no row, as §2.3 and §6.2 require. F8–F17 ↔ the nine [R-CNT-06] conditions, all reject-file, all at open; F17's two directions per §21.1. F18 ↔ [R-CNT-07]. F19 ↔ [R-CNT-08]. F20 ↔ [R-CNT-11]. F21/F22 ↔ [R-CNT-25]'s "(0, 0) … or … less than 5 … validity error at its containing scope". F23 ↔ [R-MTA-03]. F24, F25, F26, F29 ↔ [R-CNT-12] (type 0 reader; reserved bits and MU=1/PE=0 verifier; framing reader). F27 ↔ [R-MTA-05] (verifier; readers process unchanged). F28 ↔ [R-CNT-22]. F30–F33 ↔ [R-CNT-13] (half-zero, <16, past F−64 reader; cross-scope overlap verifier/reject-file). F34 ↔ [R-CNT-14]. F35/F36 ↔ [R-CNT-15].

§21.3: L1/L2 ↔ [R-ENC-03]/[R-ENC-04]; every L2 instance is expressly designated (§7.2, §11.2, §14.2, §14.3/[R-SER-07], §7.4) or dominated by one that is (disk ordinal by C·N, V by P·Q, ⌈P/8⌉ by P). L3–L9 ↔ [R-ENC-11]/[R-ENC-12]/[R-ENC-15] with layer-name rows at open and dimension/channel-name rows at layer access, matching §19.1/§19.3. L10–L12 ↔ [R-CNT-25]/[R-MTA-03]. L13, L14, L46, L47 ↔ [R-CNT-12]. L15–L18 ↔ [R-CNT-13] ("the layer for a layer record and for sub-records"; intra-layer overlap reject-layer). L19 ↔ [R-CNT-14]. L20 ↔ [R-CNT-16]. L21/L22 ↔ [R-CNT-17]. L23, L24, L26 ↔ [R-CNT-18]. L25 ↔ [R-CNT-15]. L27–L31, L36, L39 ↔ [R-CNT-23] and the value-set rules. L32 ↔ [R-GEO-01]. L33 ↔ [R-GEO-05]. L34 ↔ [R-TYP-03]. L35 ↔ [R-TYP-07]. L37/L38 ↔ [R-IDX-04] (reject-layer at tile use, exactly as §19.2 says). L40 ↔ [R-SLB-01]; L41/L42 ↔ [R-SLB-03] including the §16.2 transparency wording, which the row restates verbatim in substance. L43 ↔ [R-COD-03]. L44 ↔ [R-COD-07] with the addressed-tile quantifier and planar largest-plane clause. L45 ↔ [R-COD-09]. L48 ↔ [R-MTA-05]. L49 ↔ [R-CNT-22].

§21.4: T1 ↔ [R-CNT-20]. T2 ↔ [R-SER-08] (verifier; row splits real vs padding positions to T4). T3 ↔ [R-SER-07]. T4/T5 ↔ [R-SER-05]. T6–T12 ↔ §15.3's six structural rows ([R-IDX-03]); the register splits §15.3's sixth row into T9 (> F−64) and T12 (overflow), which §21.1's condition-individuation permits. T13 ↔ [R-COD-02]. T14 ↔ [R-COD-04]. T15/T16 ↔ [R-COD-05]. T17–T22 ↔ [R-COD-06] (magic; one frame/no skippable; dict ID; checksum flag; window "exceeding" one direction; content size "does not equal" two directions × three layout shapes). T23 ↔ [R-COD-07]. T24/T25 ↔ [R-COD-08]. T26 ↔ [R-COD-10].

§21.5: R1 ↔ [R-CNT-25]'s "an unimplemented or invalid encoding" with §10.3's reserved-range emission bar; R2 ↔ [R-CNT-20]; R3/R4 ↔ [R-CNT-25]/[R-MTA-09], with R4's eight constraints matching §18.2's carried-over list plus the content-size rule and "occupying"; R5–R10 ↔ [R-MTA-04]'s four restrictions and §4.6's name rules folded onto keys. The window-size and decoded-size bounds are correctly absent from R4 (§18.2 makes them reader capability).

§21.6: each entry's cited rule says what the entry says (checked all fourteen). The two "conforming files a reader nevertheless refuses" agree with §2.3's [R-CNF-03] parenthetical and §21.9's "the two capability refusals §21.6 names".

§21.1's specialization list: F1-front ⊂ F6, F1-trailer ⊂ F8, F35 ⊂ F36, L24 ⊂ L25, F21 ⊂ F22, L10 ⊂ L11 — each verified as a genuine subset. Further same-detector subsets exist (F2's dir_offset instance ⊂ F3's; T11 ⊂ T9; T10 ⊂ T14 on a codec-1 layer; T14 ⊂ T3), all harmless and covered by "this list is not offered as closed".

Cross-references to rows: every citation at lines 252, 277–286, 715, 1422, 2421, 2629–2664, 3236, 3479–3481, 3605–3607, 3625–3627, 3655, 3665–3667, 3822, 3854, 3893–3895, 4727–4739, and the intra-table references (T2→T4, T13→T25, T15→T24/T25, T16→T24, T23→T25, T26→T2/T4, F33→F9/F10/F30–F32/L15–L17/T8/T9, R3↔R4) resolve to a row that says what the citing text claims.

Outcome vocabulary: every row's outcome is one of §2.4's four reader outcomes; all four are reached (§21.2–§21.5 each carry one); preserve-verbatim is reached by §20.4's table. Detection tiers: open, layer access, tile use, extent use, certification — all five defined in §21.1, all used, no other value appears.

Limits: §21.9's eight guarantees match Appendix B, §17.2, §18.2, §1, §2.5, Appendix D. The hard-limit list in [R-ERR-05] matches §4.6, §7.4, §16.1, §16.2, §17.2, §6.2, §5.1 figure for figure. The user-metadata extent minimum (extent_length ≥ 5, §7.1, Appendix B) is not in [R-ERR-05]'s list; §21.9 says the list is "a finding aid rather than an inventory", so that is not a defect, but see rejected candidates.

## Findings

### register-01 — CONTRADICTION (not byte-level)

**Location.** §21.9 `[R-ERR-04]` versus §18.2's Note following `[R-MTA-09]`.

**Quotation A (§21.9, normative):** "A file exceeding any of these remains conforming, and a reader MAY decline it — at the whole file, or at the narrowest scope whose stated or derived quantities exceed what it can serve: a layer, a tile, or the record carrying a user-metadata document, as §18.2 assigns."

**Quotation B (§18.2, labelled Note):** "A reader that proceeds takes ignore-record for that record; a reader that instead declines on resource grounds under `[R-ERR-04]` does so at the whole file, a document having no declared size and so no narrower scope whose stated or derived quantities that rule can measure, its decoded size being neither."

**Detail.** The normative sentence names the record carrying a user-metadata document as a scope at which a reader may *decline* under [R-ERR-04]. The Note glossing the same case says a decline under [R-ERR-04] is at the whole file, because the record is *not* a scope "whose stated or derived quantities" that rule can measure, and re-labels the record-level response (ignore-record) as "proceeding" rather than declining. Two readings: (i) R-ERR-04's "as §18.2 assigns" means the record-level decline takes the form §18.2 assigns — ignore-record — so a record-level ignore-record *is* an R-ERR-04 decline and must be "reported as a resource limit and not as a validity error"; (ii) the Note's reading, under which the record-level ignore-record is not a decline, is reported under [R-CNT-25]'s SHOULD-report like any unreadable document, and the only R-ERR-04 decline is whole-file. I picked (i) because the Note is labelled and [R-CNF-01] makes it non-normative, so [R-ERR-04] governs — but the Note tells an implementer the opposite of the sentence it glosses. What an implementer gets wrong without a fix: how to classify and report the record-level response for an over-guarantee document (resource-limit report vs. unreadable-metadata report). The file is conforming under both readings, the record is ignored under both, and no verdict or emitted byte changes, so this is not byte-level.

### register-02 — OBSERVATION

**Location.** §21.3 row L23 (Detected cell) versus §19.1 step 4 and §19.2 `[R-RDR-02]`.

**Quotation (L23):** "A declared region of the layer record's inline payload does not lie entirely within inline_length (overrun or truncation) | leading fixed fields (name … C); d dimension entries; C channel entries; trailing fixed fields (index_encoding, entry_count, crc_of_crc_array) | reader | layer access | `[R-CNT-18]`"

**Quotation (§19.1 step 4):** "a layer record whose name field does not lie entirely within that record's inline_length yields no name field to compare, so it contributes no name to the namespace and is instead a validity error at layer scope (`[R-CNT-18]`)."

**Quotation (§19.2):** "at open: … the directory region and its record walk, and the layer-name namespace (§19.1's steps)".

**Detail.** L23's first instance groups the name with the other leading fixed fields and states "layer access" as the point by which detection is due. But §19.1 step 4 has the reader parse every layer record's name at open to build the namespace, and says a name that overruns "is instead a validity error at layer scope" — i.e. the reader has necessarily established that L23 condition at open, and §19.2 lists the namespace among the open-tier checks. For the name sub-case, the register states a later deadline than the rule. §21.1 says the rule governs, so the outcome (reject-layer) and the actual point (open) are settled; the only cost is a reader implementing from the table alone believing it may defer a check §19.1 already forces it to make. Not byte-level: same bytes, same verdict, same scope; timing only, and R-RDR-02 already permits earlier detection.

### register-03 — OBSERVATION

**Location.** §21.5 introductory paragraph, last sentence, versus §21.6's table.

**Quotation (§21.5):** "… and except where a reader or verifier declines the decode on the size bound or on the frame's declared window, which `[R-MTA-09]` makes that actor's capability and not a fact about the file. … Every row here is a violation all the same: the outcome bounds a reader's blast radius and never makes the file conforming (`[R-CNF-12]`); §21.6 lists the ignore-record conditions that are not violations."

**Quotation (§18.2, normative):** "a document exceeding that bound is ignore-record like any other it cannot read" and "a frame declaring more than the reader admits is ignore-record on that ground — the reader's capability, not a failure to decode within the meaning of R3, and no violation".

**Detail.** §21.6's table carries two ignore-record non-violations (an experimental-range record type with MU = 0; an experimental-range document encoding). The two ignore-record non-violations the §21.5 paragraph itself names two sentences earlier — a document over the reader's decode bound, and a frame declaring a window above the reader's bound — appear in §18.2 and §21.9 but not in §21.6. The definite article ("the ignore-record conditions that are not violations") sends a reader to a table that does not contain them. §21.1 exempts §21.6 from the completeness clause, so this is a cross-reference that under-delivers rather than a completeness defect; it is decidable from the text once §18.2 is read, hence an observation. Not byte-level.

## Rejected candidates (opened and closed)

- **F29 / L14 third instance "trailing residue".** Every byte sequence after the last complete record is either a truncated 24-byte header or a complete header whose inline_length overruns, so the third alternative names no file class the first two do not. Closed by §21.1: the cell enumerates "the condition's own alternatives" and "the count is therefore mechanical once the cell is written"; the condition text states three alternatives, so the cell follows the rule. A wording redundancy, not a count defect; the 277 reproduces.
- **F23's two directions for "inline_length is not 1".** §21.1 says a comparison against a constant enumerates no direction; but the cell's two instances (0: byte absent; ≥ 2: growable) are materially different shapes, which §21.1 also licenses, and the count is mechanical from the cell. Closed.
- **F2 ⊂ F3, T11 ⊂ T9, L1 ⊂ L17 (literal wording, no "although in domain" clause on F3 unlike L2/T12).** Same detector, tier and outcome in every pair; §21.1's "this list is not offered as closed" covers it. Closed.
- **F5's second instance (committed_file_length < 128).** A file with physical size ≥ 128 and committed_file_length < 128 is F17; one with both < 128 exhibits both instances of F5. Distinguishable files exist for each instance; R-CNT-27's "shorter file" is read through either quantity. Closed as acceptable.
- **R1 detected at open for a top-level record although the reader relies on the encoding byte only at extent use.** §19.1 states the register's Detected cell binds under [R-CNF-04], §21.5 says the encoding byte's value set is not a document content rule (so not the extent-use bullet), and R-RDR-02 permits earlier detection; ignore-record at open changes no verdict. Closed.
- **§21.6 "conforming files a reader nevertheless refuses": "a file this document declines to judge is not one".** The experimental MU = 1 top-level case is judged conforming, not declined; the sentence's reason fits only the foreign-major case. Wording; the paragraph's other sentences state the conforming verdict explicitly. Closed.
- **§21.6 "since the prohibition on publishing experimental values binds a writer's conduct" attached to "only the top-level case is a file a reader refuses".** Misattached causal clause; both facts are stated correctly elsewhere in the paragraph ([R-CNT-18]; [R-CNF-02]). Closed as wording.
- **User-metadata extent_length ≥ 5 absent from [R-ERR-05]'s hard-limit list** (present in §7.1 and Appendix B). Closed by §21.9: "The hard limits it restates are a finding aid rather than an inventory"; F22 carries the vector obligation via [R-ERR-02].
- **§21.4 header "the governing rule states what a reader does" for T26 ([R-COD-10]).** R-COD-10 does not state a reader behaviour in terms, but the row routes detection to T2/T4 whose rules do, and a reader applies the inverse at the mandated stride. Closed.
- **§2.4 calling every outcome a "reader outcome" while §21.1 says a verifier row's outcome is not a reader obligation.** Reconciled by [R-CNF-09]'s qualifier "whose rejection this reader is obliged to detect" and [R-CNF-04]'s verifier-row exemption. Closed.
- **The §21.9 limits table and a stored (compressed) user-metadata extent that exceeds 16 MiB while decoding to less.** No row bounds extent length; §18.2 makes the decode bound the reader's own, no smaller than the guarantee. No text contradicts. Closed.
- **L44's addressed-tile quantifier versus [R-ENC-04] in an empty layer.** §17.2's Note and §21.9's per-instance paragraph state the difference expressly. Closed.
- **F7 versus F33.** A structure in the pre-trailer gap overlaps nothing (the gap is slack), so F7 is reachable without F33 and the two merely overlap elsewhere. Closed.

## Confidence

The register's row texts, outcomes, detectors and detection points agree with their governing rules in every row I compared; the counts reproduce exactly; every row citation resolves; the limits agree in both directions. The three findings are a Note contradicting the normative sentence it glosses (reporting only), a detection-point cell later than §19 for one sub-case, and an over-claiming cross-reference. None changes which bytes a conforming implementation may emit or must accept or reject. I found no byte-level fork in §21.
