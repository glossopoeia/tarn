# Cleanroom round 7 — triage pass: implementer

Distinct defects: **44**. Byte-level: **0**.

**Coverage check.** All 63 input findings appear in exactly one judgement each; none dropped. reader: RD-01→§19-tier-enumerations, RD-02→cnf04-overbroad, RD-03→mta07-unregistered, RD-04→sec2.3-parenthetical, RD-05→§19.1-step1-residency, RD-06→multi-entry-layer-failure, RD-07→oversized-metadata-decline, RD-08→§21.7-not-inventory. writer: WR-01→wrt08-mu1-row, WR-02→commit-reusing-prior-directory, WR-03→compactor-flags0, WR-04→mta07-unregistered, WR-05→extent-growth-metadata-only, WR-06→appender-relocating-index, WR-07→walk-double-claims, WR-08→§21.7-not-inventory, WR-09→sec2.3-parenthetical, WR-10→§7.4-taxonomy, WR-11→catalogue-not-a-defect. verifier: RD-01→mta07-unregistered, RD-02→value-shape-not-violation, RD-03→slab-continuity, RD-04→cnt19-uncovered-extent, RD-05→verdict-priority, RD-06→sec2.3-parenthetical, RD-07→slack-total-vs-early-stop, RD-08→verifier-backward-probe, RD-09→§21.7-not-inventory, RD-10→cod11-trigger, RD-11→appendixA-suffix-window. diagrams: DG-01→cnt19-uncovered-extent, DG-02→§18.2-valid-values, DG-03→§15.4-example, DG-04→§5.1-caption, DG-05→§19-tier-enumerations, DG-06→brace-alignment, DG-07→appendixA-suffix-window, DG-08→F5-L3-no-witness, DG-09→instance-arithmetic. register: RD-01→F31-L50, RD-02→mta07-unregistered, RD-03→sec2.3-parenthetical, RD-04→instance-arithmetic, RD-05→§21.1-scope, RD-06→F5-L3-no-witness, RD-07→T15-T23-reader-clause, RD-08→T13-duplicates-T25, RD-09→§21.7-not-inventory, RD-10→R5-surrogate-escape, RD-11→L2-instances, RD-12→§21.9-composition. adversary: RD-01→lz4-cap-vacuous, RD-02→encoding2-occupancy, RD-03→mta07-unregistered, RD-04→verdict-priority, RD-05→cnt19-uncovered-extent, RD-06→wrt08-mu1-row, RD-07→name-framing-order, RD-08→overlong-pad, RD-09→§21.7-not-inventory, RD-10→deflate-residual-bits, RD-11→generation-saturation, RD-12→vec04-sibling. Merges: 5 agents found the [R-MTA-07] register omission; 4 found the §2.3/§21.6 cross-reference; 5 found §21.7's incompleteness; 3 found the uncovered record extent; 2 each for §19's enumerations, the Appendix A suffix window, the [R-WRT-08] MU=1 row, verdict priority, instance arithmetic, F5. Zero of the 8 self-flagged byte-level findings survive.

## Judgements

### mta07-standardized-key-outside-scope-unregistered — CONFIRMED

- merged: `reader:RD-03`, `writer:WR-04`, `verifier:RD-01`, `register:RD-02`, `adversary:RD-03`
- location: §18.4 [R-MTA-07]; §21.2–§21.6; §21.1 completeness clause; §2.4 [R-CNF-07]
- severity: register-bookkeeping

The omission is real: I read every row of §21.2–§21.5 and none carries the condition, and §21.6 does not list it as a non-violation either. Not byte-level, because the rule is not silent — [R-MTA-07] states both halves in its own text: 'A file carrying a standardized key outside its listed scope is nonconforming, and a verifier detects it' and 'a reader MUST ignore a standardized key found outside its listed scope … rather than rejecting the document'. Two independent implementers therefore build the same verifier (refuse certification for a layer document carrying tarn.created) and the same reader (skip the key, read the rest). verifier:RD-01's reading 1 — no row, so no violation, so certify — is foreclosed by §21.1's own words: an omitted row 'is a defect in this document', a statement about the register, not a licence to certify. What is missing is the row, an [R-CNF-07] outcome class, and the [R-ERR-02]/[R-VEC-02] vector.

### sec2.3-parenthetical-miscounts-21.6-exceptions — CONFIRMED

- merged: `reader:RD-04`, `writer:WR-09`, `verifier:RD-06`, `register:RD-03`
- location: §2.3 [R-CNF-03]; §21.6 closing paragraphs; §21.9 [R-ERR-04]
- severity: editorial

Verified against both passages. §2.3 attaches three qualifiers to the acceptance duty (implemented major; no unimplemented MU = 1 type; no value above §21.9's guarantees) and then says '§21.6's closing paragraph names those two exceptions'. §21.6 names an unimplemented version_major — §2.3's first qualifier, not one of its exceptions — and an *experimental-range* MU = 1 type, narrower than §2.3's second; the resource qualifier appears nowhere in §21.6. Not byte-level: every refusal ground is independently and unambiguously fixed elsewhere ([R-CNT-07]/F21 for the major, [R-CNT-15] and §21.6's second case for MU = 1, [R-ERR-04] for the resource decline), so no reader's accept/reject turns on the pointer. A broken finding aid.

### 21.7-called-the-inventory-but-is-a-sample — CONFIRMED

- merged: `reader:RD-08`, `writer:WR-08`, `verifier:RD-09`, `register:RD-09`, `adversary:RD-09`
- location: §21.1 ('§21.7 the inventory of what fails it'); §21.7 [R-ERR-01] second paragraph
- severity: editorial

§21.7's second paragraph names [R-LIF-01], [R-LIF-03], [R-GEO-06], [R-SER-01] and [R-CNT-13]'s no-embedded-offsets rule. I checked the named omissions: [R-WRT-05]'s byte-identical re-emission, [R-WRT-06]'s fresh file_id, [R-CNT-08]'s updater copy-forward, [R-IDX-01]'s disk-ordinal entry order and [R-PRV-01] are all MUST-level with no single-file witness and appear neither in the register nor in §21.7. §21.1 calls §21.7 'the inventory', which overstates a list that reads as exemplary. Not byte-level: each omitted obligation is either an actor-conduct rule [R-CNF-02] already excludes from file conformance or a multi-generation property no verifier can test, so no file's verdict and no writer's byte choices move. (Note the spec does discharge the same duty inline elsewhere — §16.2's and §7.4's notes each explain why a rule carries no row — which is why 'the inventory' reads as a claim §21.7 does not meet.)

### cnt19-every-structure-checksummed-vs-unknown-record-extent — CONFIRMED

- merged: `verifier:RD-04`, `diagrams:DG-01`, `adversary:RD-05`
- location: §8.1 [R-CNT-19] and its map; §5.2 [R-CNT-02]; §9.7 [R-LIF-08]
- severity: editorial

Confirmed by reading §8.1's map: its six rows cover the front block, trailer, directory, tile-index region, stored tile and user-metadata extent. §5.2 defines a structure to include 'a record extent (the bytes any record's extent slot references, whatever the record's type)', so an experimental-range MU = 0 record with a nonzero extent is a live-state structure with no row, and §9.7's 'each verifies against the checksum covering it' has nothing to apply. Not byte-level: [R-CNT-19] is declarative and names no actor, §21 registers no violation for an uncovered structure, and §21.6 makes the experimental MU = 0 record conforming — so both verifiers certify and no reader fetches the extent at all. The substantive residue is that corruption inside such an extent is invisible to reader and verifier alike, a third residue §22.3's 'Two residues are stated rather than defended' does not name.

### cnf04-overbroad-reader-detection-duty — CONFIRMED

- merged: `reader:RD-02`
- location: §2.3 [R-CNF-04]; against §19.2 [R-RDR-02], §21.1's verifier-row paragraph, §6.2 [R-CNT-05], §14.2 [R-SER-08]
- severity: editorial

[R-CNF-04] as written says flatly that a reader MUST detect the violations enumerated in §21 and apply each outcome, with no reference to the Detector column. Three passages contradict the literal reading in terms: §19.2 ('a violation whose assigned detector is the verifier … imposes no reader obligation'), §21.1 ('For a row whose Detector is verifier, the outcome … [is] not an obligation on any reader'), and §6.2's parenthetical 'readers check neither'. [R-SER-08] settles it decisively — 'a reader that does not detect the violation is not thereby nonconforming'. So only the narrow reading is available and two implementers build the same reader; the defect is that the requirement most implementers will quote states the wrong rule in isolation.

### 19-tier-enumerations-not-coextensive-with-register — CONFIRMED

- merged: `reader:RD-01`, `diagrams:DG-05`
- location: §19.1 step 4 [R-RDR-01]; §19.3 [R-RDR-03]; §21.2 F24/F25/F26; §21.3 L5/L11/L12/L13
- severity: editorial

Verified row by row. §19.1 step 4 names [R-CNT-12], [R-CNT-15], [R-CNT-14], [R-CNT-13] and [R-ENC-12], while F24/F25/F26 ([R-CNT-25], [R-MTA-03]) are reader-detected reject-file rows whose Detected cell reads *open*, and none of them follows from the cited five — extent (0,0) is expressly legal under [R-CNT-13], and inline_length ≠ 1 comes only from [R-MTA-03]. §19.3 likewise omits [R-ENC-11] (L5), [R-CNT-25] (L11/L12) and [R-MTA-03] (L13). Not byte-level: §19's own preamble says it 'consolidates' and 'introduces no new structures', §19.2's first tier bullet already places 'the directory region and its record walk' at open, and §21.1 makes the Detected column the point by which detection is due — so reader:RD-01's reader B, which serves a layer after skipping F26, is nonconforming under rules already written. The lists are under-inclusive restatements, not a licence.

### 19.1-step1-front-block-residency-restatement — PARTIAL

- merged: `reader:RD-05`
- location: §19.1 step 1 [R-RDR-01]; §6.1 [R-CNT-04]
- severity: editorial

Narrower than reported. §19.1 step 1's own text defuses the divergence: 'These steps are ordered by dependency, not by I/O: a remote reader's suffix range for step 2 carries F in its own response, so steps 1 and 2 cost one request between them.' A reader that speculates a window reaching offset 0 therefore does hold [0, 16) 'once this step completes', so §19.1 binds it exactly as §6.1 does, and a reader whose window does not reach offset 0 is released by both. I could construct no case the two formulations decide differently. What survives is a wording defect: 'once this step completes' states as a point-in-time test what §6.1 states as residency across the whole open, and reads the wrong way when §19.1 is read alone.

### appendix-a-any-suffix-window-reaches-offset-0 — CONFIRMED

- merged: `verifier:RD-11`, `diagrams:DG-07`
- location: Appendix A, closing paragraph
- severity: editorial

The sentence 'since this file is 128 bytes and any such window reaches offset 0' is false as written. A 96-byte suffix window covers [32, 128) and reaches nothing; DG-07's sharper case is a 112-byte window covering [16, 128), which contains the directory — so §6.4's containment test makes request 2 unnecessary — while leaving [0, 16) non-resident and the front-block check optional. Not byte-level: Appendix A is identified non-normative and excluded by [R-CNF-01], the rule it illustrates is stated correctly in §6.1, and F8's condition cell already records the same conditionality. A reader that speculates 96 bytes falls under [R-CNT-04]'s MAY-defer branch under every reading.

### oversized-metadata-document-whole-file-decline — PARTIAL

- merged: `reader:RD-07`
- location: §18.2 [R-MTA-09]; §21.9 [R-ERR-04]; §2.3 [R-CNF-03]
- severity: editorial

Narrower than reported, and the divergence is licensed rather than undecided. [R-ERR-04] says in terms 'a reader MAY decline it — at the whole file', and [R-CNF-03]'s acceptance duty is itself expressly conditioned on 'none of whose values exceeds the minimum guarantees', so a 20 MiB document puts the file outside the duty by §2.3's own text. Reading 1's claim that refusal 'is not permitted' has no textual support — [R-MTA-09] assigns the record's outcome, it does not create an acceptance obligation. Two implementers may therefore diverge on that file, but by an explicit MAY, the same way [R-CNF-05] licenses writer divergence; resolving nothing changes the must-accept set. The real editorial defect: [R-ERR-04]'s scope list ('a layer or a tile') and its phrase 'the narrowest scope whose *declarations* exceed what it can serve' are drafted for declaration-derived magnitudes, and a document — which [R-MTA-09] says 'has no declared size' — is the one §21.9 quantity that is not one, leaving whole-file as its only listed scope.

### verifier-verdict-priority-nonconforming-vs-cannot-establish — CONFIRMED

- merged: `verifier:RD-05`, `adversary:RD-04`
- location: §2.3 [R-CNF-11]; §18.2 [R-MTA-09]; §17.4 [R-COD-11]
- severity: editorial

Real gap: §2.3 defines three verdicts and states no priority for a file that both exhibits an established violation and contains a requirement the verifier cannot check. [R-MTA-09]'s 'MUST report that it cannot establish … rather than that the file is nonconforming' is about not mislabelling the decline, not about a file that also carries a real violation, and §2.3's stop-at-first-violation licence makes the verdict a function of traversal order. Not byte-level: neither verdict certifies, [R-CNF-12]'s MAY-reject licence is triggered by the detected violation under either, and no byte sequence's accept/reject status moves. The cost is that an operator is sent to different remedies by two equally conforming verifiers.

### slab-run-continuity-across-a-rejected-entry — CONFIRMED

- merged: `verifier:RD-03`
- location: §15.3 [R-IDX-03]; §16.2 [R-SLB-03]; §21.3 L42
- severity: register-bookkeeping

The ambiguity is real: §15.3 says the verifier rows 'bind over well-formed entries' extents only', which can mean either that the survivors must be adjacent to each other (L42 fires across the removed entry) or that the relation is simply not evaluated where the sequence is broken. §16.2 grants continuity transparency explicitly and only to sentinels, which cuts against extending it to malformed entries, while §21.1's 'Conditions attach to the finest structure they damage' cuts the other way. Not byte-level, and the reporter's own argument fails on the register: L42's Detector is *verifier*, and §16.2 says 'readers are not obligated to' check the invariants, so [R-CNF-09] never bars a reader from returning tile 0's samples under either reading. The condition also requires a malformed entry (T10, length = 0), so the file is nonconforming and no verifier certifies either way. Only the recorded scope and the corpus row differ — the calibration case exactly.

### lz4-cap-vacuous-on-a-zero-addressed-tile-layer — PARTIAL

- merged: `adversary:RD-01`
- location: §17.2 [R-COD-07]; §21.3 L45; §11.1 [R-GEO-02]; §4.2 [R-ENC-04]
- severity: editorial

The vacuity is real and is the best implementer trap in the batch — natural code computes the tile decoded size from P and Q without consulting the addressed-tile count, so one implementer rejects the layer and another accepts. But the rule is not silent: [R-COD-07] quantifies explicitly over 'a layer any of whose addressed tiles' decoded size exceeds', L45 repeats the same quantifier verbatim, and §21.6 records 'A dimension has extent 0' as 'A valid, empty layer'. Three consistent signals make the empty quantification determinate — the layer is conforming — so a rejecting verifier is the nonconforming party and no resolution is owed. The reporter's own reading 3 is correct on the second half: [R-ENC-04] is *not* vacuous, since [R-SER-02] calls P·Q a declaration-derived quantity and L2 lists it as an instance, so the T₀ = 2⁶² / four-float64 variant is reject-layer under both readings. Worth a Note that the lz4 cap and the overflow rule quantify differently; not a fork. The escape is also temporary: any later commit that grows the extent re-imposes the bound.

### encoding-2-document-occupancy-has-no-register-row — PARTIAL

- merged: `adversary:RD-02`
- location: §18.2 [R-MTA-09]; §21.5 R3/R4
- severity: register-bookkeeping

The register gap is real: R4's ten instances are exactly the four carried-over [R-COD-06] frame constraints, R3 is 'stored bytes fail to decode', and neither reaches a valid frame followed by two stray bytes before the terminal CRC. But the rule is not silent — occupancy sits in [R-MTA-09]'s main clause ('exactly one RFC 8878 compressed frame *occupying the extent's bytes before its terminal CRC*'), grammatically parallel to [R-COD-05]'s 'The stored bytes are exactly one DEFLATE compressed data stream', which the register does treat as generating violations (T15, T16, T24). A verifier 'checks every file-level requirement' (§2.3), so both verifiers report nonconforming and neither certifies; reading 2, which treats the participle as scenery, is careless rather than licensed. The residue that survives is genuine but non-byte: no detector is assigned, so whether a streaming decoder that returns `{}` is obliged to take ignore-record is unstated — and metadata can affect no structural byte ([R-MTA-02]).

### commit-pointing-live-trailer-at-a-prior-generation-directory — PARTIAL

- merged: `writer:WR-02`
- location: §9.2 [R-LIF-02] step 3; §5.1 [R-CNT-01]; §3.1; §6.2 [R-CNT-05]
- severity: editorial

I built the reporter's 192-byte file and checked every gate: dir_offset = 16 ≥ 16, dir_length = 4 ≥ 4, 20 ≤ 128, F = 192 mod 64 = 0, generation 2 = 1 + 1, file_id ≠ 0, directory CRC over zero bytes = 0x00000000, live state = front block + [16,20) + [128,192), slack = [20,128) = 108 bytes disjoint. Reading 1 (nonconforming file) is nonetheless foreclosed, and by a sentence the reporter quotes but does not apply: [R-CNT-05] says of the pre-trailer gap 'a longer gap is conforming, and no conforming commit produces one' — precisely this shape. Add [R-CNF-02]'s pure-predicate rule, §21.1's normative completeness (no row), and §9.7's refusal to reconstruct history, and both verifiers certify. Reading 3 is foreclosed too: step 3's 'append the new complete directory' is an unqualified MUST and cannot be discharged by an existing one. So the file is conforming and the writer is not — reading 2, decided. What is genuinely missing is any statement of the cheap byte-testable invariant this implies: for generation ≥ 2 the live dir_offset must be ≥ the prior generation's committed length, hence ≥ 128.

### wrt08-mu1-persistence-row-captures-the-layer-record — CONFIRMED

- merged: `writer:WR-01`, `adversary:RD-06`
- location: §20.4 [R-WRT-08] stored-flags table, MU = 1 row; §7.3 [R-CNT-22]; §20.3 [R-WRT-04] step 4; §2.3 [R-CNF-06]
- severity: editorial

Confirmed by reading the paragraph that introduces the table: 'Persistence governs every record type … For a type §7.3 registers, the registry's fixed flags govern rather than the stored ones' — and §7.3 fixes the layer record at MU = 1. That routes the one record every appender modifies into a row whose first sentence reads 'Retain byte-identical. The updater MUST NOT modify the scope the record governs.' Taken literally, no conforming append could touch a layer, which unmakes §20.3, §9.2 and §20.5. Reading 2 governs — [R-CNF-06] scopes preservation to 'records it does not understand', the cell's own gloss says 'an unknown critical record at layer scope', and Appendix H states it plainly. Not byte-level: the two readings differ only in whether an updater may offer the operation; every file the permissive updater emits is conforming under both, and the restrictive reading yields a tool that refuses to act, not one that emits divergent bytes.

### compactor-flags-zero-vs-ignore-lane-copy-forward — PARTIAL

- merged: `writer:WR-03`
- location: §6.3 [R-CNT-08]; §20.5 [R-WRT-06]; §20.1 [R-WRT-01]
- severity: editorial

'Which governs a compactor is not stated' is too strong — §20.5 states the compactor case specifically, in terms, and cites [R-CNT-08] as its authority: 'The output trailer copies the input's unknown ignore-lane flag bits forward ([R-CNT-08])', with the reason given. What survives is a smaller tension: §20.1's tiers make a compactor distinct from a creator, yet a compactor does create a file, so [R-CNT-08]'s 'a writer creating a file under this text MUST write flags = 0' reads onto it if 'under this text' is taken as a tier test rather than as a feature test. Not byte-level: §6.3 and [R-CNF-02] jointly declare a set ignore-lane bit not to be a file-conformance violation and every reader MUST ignore bits 16–31, so both output trailers are conforming and no verdict differs.

### extent-growth-called-metadata-only — CONFIRMED

- merged: `writer:WR-05`
- location: §11.1 Rationale; §13.3 'Note — sparse writing'; against §20.3 [R-WRT-04] step 4 and [R-GEO-06]
- severity: editorial

The claim is true only when no grid count changes. With T₀ = 256, growing E₀ from 1000 to 1024 leaves G₀ = 4 and is genuinely directory-only (§20.3's shape (c)); growing it to 1100 makes G₀ = 5, changes entry_count, trips [R-CNT-17]'s cross-check, forces the layer's whole tile-index region to be re-emitted, and renumbers disk ordinals for any d ≥ 2. Both offending sentences sit in blocks labelled *Rationale* and *Note*, which [R-CNF-01] makes non-normative, and §20.3's own note prices the true cost ('editing one sample of a 10⁶-tile layer appends about 20 MB of index'). Not byte-level: a writer misled by the rationale emits a file failing [R-CNT-17], which is L22/L23 — already registered and already reject-layer at layer access.

### 5.1-caption-only-dir-pad-trailer-re-emitted — CONFIRMED

- merged: `diagrams:DG-04`
- location: §5.1 'a file after three commits' figure caption; §20.3 [R-WRT-04] step 4
- severity: figure

The caption states without qualification that 'only the directory, the pad and the trailer are re-emitted per commit', while the figure it captions shows layer B arriving in a later commit — which by §20.3 step 4 wrote B's tiles and its whole index. The sentence is scoped by a preceding colon ('Layer A's tiles and index have never moved:') but the clause itself is universal, and §20.3's own note and §1's third design pillar both price the omitted cost. Not byte-level: the figure is an *Example*, non-normative under [R-CNF-01] and self-disclaimed ('Regions, not offsets'), and a writer misled by it emits a well-formed file whose index points at a superseded payload — §21.7's 'incorrectness of content' class, not a divergence about which bytes anyone must accept.

### appender-relocating-an-untouched-layers-index — PARTIAL

- merged: `writer:WR-06`
- location: §20.3 [R-WRT-04] step 4; §20.4 [R-WRT-05]
- severity: editorial

Narrower than reported. Step 4's own trigger list — 'Every layer whose stored-tile set, index content, or *index placement* this commit changes has its tile-index region re-emitted in full' — presupposes that a commit may change index placement; otherwise that third disjunct is dead text. Combined with [R-WRT-05]'s condition 'every record it retains and does not logically modify', relocation is contemplated and permitted, with the superseded region becoming slack the writer pays for ([R-SLB-05]). What is missing is only an imperative statement of the permission. Not byte-level: the relocated region is a live record extent, disjoint and checksum-consistent; no register row distinguishes the two files and no reader or verifier reaches a different verdict.

### coverage-walk-double-claims-a-layer-records-extent — CONFIRMED

- merged: `writer:WR-07`
- location: §9.7 [R-LIF-08]; §21.2 row F36 Instances; §7.4
- severity: editorial

Verified: §9.7 enumerates 'the live directory and its records, each record's extent, and each layer's tile-index region', while §7.4 makes a layer record's extent slot address exactly that index region. Read literally the walk names one byte range twice and the disjointness check fails on every layer with entry_count > 0. F36's instance cell repeats the double count ('tile-index regions; record extents'). Not byte-level: the literal reading is self-refuting — it would make Appendix A's model and §21.6's 'zero layers' baseline the only passing shapes — and L19's instance cell ('stored-tile extents; tile-index region; layer sub-record extents') makes the dedup explicit by pointedly omitting a separate layer-record extent. No implementer sustains it; the defect is an imprecise enumeration in a rule whose whole content is an enumeration.

### slack-total-must-vs-stop-at-first-violation — CONFIRMED

- merged: `verifier:RD-07`
- location: §5.2 [R-CNT-21]; §2.3 [R-CNF-11]
- severity: editorial

Real interaction gap. [R-CNT-21] places an unconditional MUST on a verifier to report the slack total, with a 'partial' escape triggered specifically by 'a scope-level rejection stop[ping] the walk of §9.7'; §2.3 separately and unconditionally licenses a verifier to stop at the first violation and report the rest as *unexamined*. Nothing says whether an early stop discharges the slack-total MUST, or whether *unexamined* and *partial* compose. Not byte-level: §5.2 states in terms that slack's 'content is unconstrained, and no conformance requirement applies to it', so the total is report content; no file's validity and no reader's return behaviour turns on which number is printed.

### verifier-use-of-the-backward-trailer-probe — PARTIAL

- merged: `verifier:RD-08`
- location: §9.6 [R-LIF-06]; §9.7 [R-LIF-08]
- severity: editorial

Partly answered by §9.6 itself, which the finding under-reads: the sentence 'A recovery tool enumerating a file's commit states continues the same probe to offset 0; coverage verification does not (§9.7, [R-LIF-08])' already bounds what a verifier does with the probe, and §9.7's note ('A verifier certifies what a reader can reach … decidable from the live trailer in one pass') fixes the verdict basis. What remains unstated is only whether the probe result carries any diagnostic obligation. Not byte-level: §2.3 makes conformance a pure predicate on the bytes handed over, F10/F19 already decide a file whose physical tail is not a valid trailer, and §9.6's own 'recovery output MUST be re-verified as a whole file' makes the truncated prefix a separate artifact — so reading 2 is unavailable and no implementation certifies what another rejects.

### wrongly-shaped-standardized-metadata-value — PARTIAL

- merged: `verifier:RD-02`
- location: §18.4 [R-MTA-07], [R-MTA-08]; §21.1 completeness clause
- severity: editorial

The silence is real — [R-MTA-07]'s writer prohibition covers only scope ('MUST NOT emit a standardized key outside the scopes its row lists') and its nonconformance sentence is narrowed the same way, while the reader clause covers both scope and shape. But the finding's byte-level claim fails: no MUST binds a writer to the Value column, and §21.1's *normative* completeness settles the rest — a wrongly-shaped value would be a detectable violation, so if it were one the register would carry a row, and it carries none. Both verifiers therefore certify {"tarn.title":42} and both readers ignore the key. Reading 2 would require reading the table's Value cell as a writer constraint against an explicit narrowing one sentence away. Editorial: the contrast is inferable rather than stated.

### f31-l50-scope-collision-for-registered-type-flag-mismatch — CONFIRMED

- merged: `register:RD-01`
- location: §21.2 row F31; §21.3 row L50; §7.3 [R-CNT-22]
- severity: register-bookkeeping

Confirmed: type 0x0001 is a top-level registered type, so a layer record with a flipped stored MU or PE bit satisfies F31's condition (under §21.2's blanket 'Outcome: reject-file') and L50's (reject-layer) at once. [R-CNT-22] resolves it — 'a validity error at the record's governing scope' — and §7.2 fixes that as the layer for a layer record, so F31 must be read as restricted to non-layer top-level records. Not byte-level, and this is the calibration's paradigm case: §21.1's 'where a row and the rule it cites diverge, the rule governs' decides the scope, both rows carry Detector *verifier* and Detected *certification*, the verdict is nonconforming either way, and [R-CNT-22] obliges every reader to apply the type's fixed semantics regardless. Only the table is wrong.

### instance-arithmetic-applied-inconsistently-across-cells — CONFIRMED

- merged: `register:RD-04`, `diagrams:DG-09`
- location: §21.1 Instances paragraph; §21.2 F33; §21.3 L1, L16; §21.5 R5; §21.8
- severity: register-bookkeeping

Confirmed by comparing cells that restate one and the same condition. [R-CNT-13]'s half-zero extent slot is enumerated by *alternatives* at file scope (F33: 'extent_offset; extent_length', one container) and by *containers* at layer scope (L16: 'layer record extent slot; sub-record extent slot', two alternatives collapsed) — the same predicate counted along different axes. L1 lists two fields that each occur in two containers as two instances; R5 lists two containers and drops [R-ENC-11]'s key-versus-string-value alternatives. §21.1's rule ('a condition applying to two alternatives in two containers has four') would give 4, 4 and 8; the cells give 2, 2 and 6. Both reporters recounted independently and both reach 61 + 100 + 45 + 36 = 242, matching §21.8 exactly, so the cells were counted as written and §21.8 is internally consistent — the rule and the cells are not. Not byte-level: this decides only how many corpus files a row builds, and §24 makes the corpus derivative.

### 21.1-scope-over-21.6-and-21.7 — PARTIAL

- merged: `register:RD-05`
- location: §21.1 opening paragraph; §21.6; §21.7
- severity: editorial

The scope question is real — §21.1 governs 'The register below', §21.6 is a non-violation table and §21.7 an undetectability inventory, and whether the completeness clause, the row-versus-rule tiebreak and the instance arithmetic reach them is never stated (though §21.1 does enrol §21.7 by role and §21.5's preamble cross-refers to §21.6). But the reporter's own test is the right one and comes out negative: §21.6's rows each carry a Rule column and every row I checked is independently decided by the rules it cites — the experimental metadata encoding by [R-MTA-03] plus §10.3 plus [R-CNF-02], on the same chain [R-CNT-15] spells out for record types. So no §21.6 row is the sole statement of anything, both scope readings land on identical emit/accept behaviour, and only the derivation path differs.

### f5-l3-width-violation-has-no-isolable-witness — CONFIRMED

- merged: `register:RD-06`, `diagrams:DG-08`
- location: §21.2 row F5; §21.3 row L3; §4.2 [R-ENC-06]; §21.8 [R-ERR-02]
- severity: register-bookkeeping

Both halves check out. F5's condition requires 'total size unchanged', yet its own worked instance — trailer version_major and version_minor as u32 each — adds four bytes to a structure [R-CNT-24] says has 'zero slack: every byte is assigned'; holding 64 bytes means deleting another 4-byte field, which is a different violation, and shifting the remaining fields makes dir_offset, dir_length and committed_file_length read as garbage that F11/F12/F15/F19 catch first. L3 has the same problem in a variable-length payload, where a rewidened rank d shifts the parse into L24. So neither row names a byte pattern a reader can attribute to it alone, yet [R-ERR-02] and [R-VEC-03] require a vector per instance. Not byte-level: a reader parses at the fixed widths and has no other layout available, so a same-size width error yields bytes that are either indistinguishable from conforming or caught by another row's gate.

### t15-t23-cite-rules-with-no-reader-clause — CONFIRMED

- merged: `register:RD-07`
- location: §21.4 T15, T16, T23; §17.2 [R-COD-05], [R-COD-07], [R-COD-06], [R-COD-08]
- severity: editorial

Confirmed against the three codec rules. [R-COD-06] (zstd) states its reader clause explicitly — 'a reader MUST treat a payload whose first four bytes are not that magic … as a validity error at tile scope'. [R-COD-05] (deflate) states only what the bytes are, and [R-COD-07]'s only reader clause is about the declaration cap, not about frame-versus-block. So T15, T16 and T23 assign Detector *reader* at *tile use* on the strength of rules that impose no reader check, in a document whose §2.1 note promises that 'every writer-side prohibition is paired with an explicit reader-side clause'. Detection in fact flows from [R-COD-08]. Not byte-level: T15's condition is 'carr[ying] a wrapper', which for gzip means a full member (magic, CM, FLG, MTIME, XFL, OS, trailing CRC32+ISIZE), not merely two bytes — so a conforming raw stream that happens to begin 1F 8B is not caught, and every file that does exhibit the condition is nonconforming, where [R-CNF-12] licenses both behaviours.

### t13-duplicates-t25-lz4-instance — CONFIRMED

- merged: `register:RD-08`
- location: §21.4 T13 and T25; §17.1 [R-COD-02]; §17.2 [R-COD-08]
- severity: register-bookkeeping

Confirmed: T13's second instance ('lz4 block whose match offset reaches before its own output start') and T25's third ('lz4 match offset 0 or match reaching past produced output') are the same predicate in different words, so one file satisfies both rows. T13's cited rule [R-COD-02] states a property of the format and supplies no detection procedure — a reader meets the condition only as a decode failure, which is [R-COD-08], which is T25. T26 is already drafted as a cause row that borrows T2's and T4's procedures; T13 needs the same treatment, and §21.1's specialization list ('F2 of F8 and of F10, F38 of F39, L25 of L26') should name the pair. Not byte-level: identical outcome, detector and detection point, and the same tile is rejected under either attribution — the cost is duplicate corpus vectors under [R-ERR-02].

### r5-omits-the-unpaired-surrogate-escape — CONFIRMED

- merged: `register:RD-10`
- location: §21.5 row R5; §18.2 [R-MTA-04] fourth bullet
- severity: register-bookkeeping

Confirmed. [R-MTA-04] names two distinct failures — 'a \uXXXX escape denoting an unpaired surrogate has no UTF-8 encoding and makes the document unreadable, as does an ill-formed byte sequence in the source' — and R5's condition and instance cell carry only the second. The escape case falls through no other row either: such a document is well-formed UTF-8 in its source bytes and well-formed JSON under RFC 8259, so R7 ('not well-formed JSON') does not reach it. Not byte-level: [R-MTA-04] states the consequence in the rule text and §7.1's quarantine fixes unreadable as ignore-record with a SHOULD-report, so two implementations handle the bytes identically. The gap is a missing instance and a missing corpus vector.

### l2-instances-that-are-not-distinguishable-files — CONFIRMED

- merged: `register:RD-11`
- location: §21.3 row L2; §21.1 distinguishability rule; §21.8
- severity: register-bookkeeping

I checked the arithmetic and the reporter is right. §21.1 requires one instance to be one *distinguishable* file. Of L2's ten, 'max disk ordinal (C−1)·N + (N−1)' equals C·N − 1, so any file overflowing it also overflows C·N, which is already an instance; and 'V = P·C' is dominated by 'P·Q', since Q = ΣBᵢ ≥ C makes P·Q ≥ P·C, so no file overflows V without overflowing P·Q. Two of the ten build no file that differs from another instance's, which would put the corpus at 240. §21.8's word 'named' is also wrong for the 51 cells reading —. Not byte-level: [R-ENC-04] gives one outcome for every quantity in the cell, so a reader that overflow-checks its products behaves identically at eight instances or ten.

### 21.9-guarantees-have-no-composition-rule — CONFIRMED

- merged: `register:RD-12`
- location: §21.9 [R-ERR-03], [R-ERR-04]; §2.5 [R-CNF-10]
- severity: editorial

Real gap: [R-ERR-03] says 'a conforming reader MUST accept any conforming file whose quantities lie within these bounds' with the rows stated per quantity and no rule for their product, while [R-ERR-04]'s only escape is for a file 'exceeding any of these' — which a file combining in-bounds quantities does not do. 65,536 layers at 2³² addressed tiles each is within every row and runs to petabytes of index. Not byte-level, and not for a merely practical reason: [R-CNT-17] ties extent_length to entry_count and [R-CNT-13] ties that to F, so a file at even the single-row tile-count bound is ≥ 85 GB — §24 says as much, declining to build a vector at that bound — and no composed file can be handed to two implementations at all. Either way [R-ERR-04] requires the refusal to be reported as a resource limit, so no reader mislabels intact bytes as corrupt.

### layer-name-framing-vs-uniqueness-ordering — CONFIRMED

- merged: `adversary:RD-07`
- location: §19.1 step 4 [R-RDR-01]; §7.4 [R-CNT-18]; §21.3 L4/L6/L7 vs L24
- severity: editorial

The ordering gap is real, and sharper than the finding states: §19.1's 'Uniqueness is decided first … over the raw name bytes' is unqualified about framing, and the register makes the tension structural — L4, L6 and L7 (the layer name's UTF-8, emptiness and control-character rules) carry Detected *open*, while L24 (a declared region overrunning inline_length, whose instance cell includes 'leading fixed fields (name … C)') carries Detected *layer access*. A reader obliged to parse each layer's name at open must bound-check the length prefix at open too, which L24's tier says is not yet due. Reading 1 is better supported ([R-CNT-18] states the bound as a hard parse requirement; §19.1's own justification is about well-formedness, not framing). Not byte-level: the crafted file is nonconforming under every order, [R-CNF-12] lets a reader reject it entire, and §24's note says both readers pass the vector.

### overlong-pre-trailer-pad-binds-the-writer-only — PARTIAL

- merged: `adversary:RD-08`
- location: §6.2 [R-CNT-05]; §9.2 [R-LIF-02] step 5; §2.3 [R-CNF-02]
- severity: editorial

Narrower than reported: [R-CNF-02] already establishes the category the finding says is missing. Its second sentence names conduct rules (§10.3, §18.3), but its third generalizes — 'A writer obligation whose violation this specification expressly declares not to be a file-conformance violation — §6.3's flags = 0 against a set ignore-lane bit — binds the actor in the same way' — and [R-CNT-05] makes exactly that express declaration ('a longer gap is conforming, and no conforming commit produces one'). So step 5's pad is a second member of a class §2.3 defines but illustrates with only one example. Not byte-level: both verifiers certify, §21.2 registers only a *structure* in the gap (F9) and not an over-long gap, and what is left open is whether the writer is a conforming writer — which no byte sequence records.

### deflate-final-byte-residual-bits-unconstrained — CONFIRMED

- merged: `adversary:RD-10`
- location: §17.2 [R-COD-05], [R-COD-08]; §22.3 [R-SEC-04]; §21.7
- severity: editorial

Correct on the mechanics: a raw RFC 1951 stream ends on a bit boundary, RFC 1951 fixes no value for the final byte's unused high bits, and [R-COD-08] speaks of 'trailing bytes past the stream', which no partial byte is. So up to seven bits per codec-2 tile sit inside a live, crc-covered extent, consumed by no decoder and constrained by no rule — a third residue neither §22.3's 'Two residues are stated rather than defended' nor §21.7 names. Not byte-level: two files differing only in those bits both decode to the same tile image and both verify, which is writer freedom [R-CNF-05] already grants and Appendix G item 1 already closes by pinning the encoder. A whole extra byte after the one holding the final bit does trail, and is T24.

### generation-counter-saturation-unstated — CONFIRMED

- merged: `adversary:RD-11`
- location: §6.2 trailer table; §9.2 [R-LIF-02] step 5; §9.3 [R-LIF-03]; §4.2 [R-ENC-03]
- severity: editorial

Arithmetically correct and genuinely unstated: generation is capped at 2⁶³ − 1 by [R-ENC-03] and the trailer's valid-values cell, and [R-LIF-03] requires exactly +1 per commit, so a file at the cap admits no further commit and the only conforming path onward is compaction — which §20.5 presents purely as slack reclamation, never as the counter's escape. Not byte-level: a trailer carrying 2⁶³ fails [R-CNT-06]'s '1 ≤ generation ≤ 2⁶³ − 1' gate at open in every reader (F3's neighbourhood), so no implementation could disagree about the bytes. Of negligible practical weight; worth a sentence at most.

### vec04-intact-sibling-disjunct-wrong-for-reject-layer — CONFIRMED

- merged: `adversary:RD-12`
- location: §24 [R-VEC-04]
- severity: editorial

Confirmed: [R-VEC-04] offers one disjunction — 'another layer, or another tile of the same layer' — for two outcome classes, and the second disjunct cannot discharge the stated purpose for a reject-layer vector, since a rejected layer's every tile is unusable and the manifest can record no decoded content from it. The rule's own justification ('Without the sibling a vector cannot distinguish a reader that scopes its refusal from one that rejects the file entire') is exactly what a corpus builder taking the disjunction literally would fail to achieve. Not byte-level: this constrains corpus construction only; no file's verdict and no implementation's behaviour changes.

### 18.2-table-valid-values-vs-experimental-encoding — PARTIAL

- merged: `diagrams:DG-02`
- location: §18.2 [R-MTA-03] layout table; §21.6; §10.3 [R-EXT-03]; §7.1 [R-CNT-25]
- severity: editorial

Weaker than a contradiction. The cell reads '1 or 2; **see below**', and the prose immediately below partitions the space (0 invalid; 1–2 assigned; 3–0x7F reserved; ≥ 0x80 experimental), so the cell defers rather than asserting a closed valid set — unlike the trailer table's cells, which F13/F14/F17 do register. And three rules foreclose the rejecting reading anyway: [R-CNT-25] assigns ignore-record to 'an unimplemented or invalid encoding' notwithstanding [R-CNF-08]'s owning-scope mapping, [R-EXT-03] says 'never a scope-level rejection', and §21.6 states the file is conforming. Not byte-level, as the reporter concludes: a reader that reject-files on encoding 0x80 is the nonconforming party, and the verifier's verdict is fixed at conforming.

### 15.4-example-one-segment-at-entry-count-zero — CONFIRMED

- merged: `diagrams:DG-03`
- location: §15.4 second worked example; [R-CNT-17]; [R-CNT-23]; [R-GEO-02]
- severity: editorial

Confirmed: 'A layer with entry_count ≤ 65,536 has one segment and a 4-byte array' is false at entry_count = 0, an explicitly first-class case ([R-GEO-02]: a dimension with extent 0 is valid, 'its tile index has zero entries'). At 0 the region has ⌈0/2¹⁶⌉ = 0 segments, a zero-byte array, extent slot (0, 0) and crc_of_crc_array = 0 — nothing to fetch and no CRC to verify. Not byte-level: the text is an *Example*, non-normative under [R-CNF-01], and the normative rules compute a unique answer — [R-CNT-17]'s formula gives 0 and [R-CNT-23] fixes crc_of_crc_array at 0, so a file with a 4-byte extent at entry_count = 0 is L23/L28 reject-layer under every reading.

### 5.1-and-20.3-figure-brace-alignment — CONFIRMED

- merged: `diagrams:DG-06`
- location: §5.1 'a file after three commits' figure; §20.3 shape (a) brace label
- severity: figure

Verified by counting columns. In §5.1's box, layer A's cell content spans columns 9–19 with pipes at 8 and 20, but the brace runs └ at 9 to ┘ at 21 — the closing corner lands on the first ▓ column of the adjacent slack run, and the same offset repeats for layer B and for the 're-emitted' brace. In §20.3 shape (a), the brace labelled 'was dir₁' spans a slack run that the example's own prose identifies as 'the old directory, pad and trailer' (and §5.1's caption as 'the directories, pads and trailers'), so the label undercounts what it spans. Not byte-level: the figures carry no offsets, sizes or ordering commitments and disclaim contiguity by citing [R-SLB-05].

### 7.4-layout-table-omits-taxonomy-class — CONFIRMED

- merged: `writer:WR-10`
- location: §7.4 layer-record layout table; §4.7 [R-ENC-16] and its Note
- severity: editorial

Confirmed against every other layout table. §6.2 (trailer), §7.2 (record header), §15.1 (index entry) and §18.2 (metadata encoding) all carry a Class column; §7.4's gives only Field/Type/Constraint. [R-ENC-16] is normative and says 'Every field this specification defines is classified structural, semantic, or informative', so §7.4's fields are unclassified in violation of it — and the byte-offset omission is forced, since the payload is variable-length, which means §4.7's Note ('Layout tables … give, per field: byte offset …') overstates what any table can do. No field anywhere is classified informative, leaving [R-ENC-16]'s only normative consequence without a subject. Not byte-level: every §7.4 field's decoding role is fully fixed by the rules that use it, so writers emit and readers parse identical bytes whatever label is attached.

### layer-scope-failure-part-way-through-a-multi-entry-request — CONFIRMED

- merged: `reader:RD-06`
- location: §19.4 step 8 [R-RDR-04]; §2.4's reject-layer row; §15.4 [R-IDX-04]
- severity: editorial

Real gap. Step 8 fixes what a multi-entry request returns when individual entries are rejected at *tile* scope, but step 3's index-chain failure takes *layer* scope ([R-IDX-04]), and step 8's per-entry bounding does not reach it. §2.4 then makes reject-layer prospective — it 'does not retroactively invalidate content already returned' — which leaves the answer turning on whether earlier tiles were handed to the caller, while §2.4's own note says how failure is reported 'is implementation technique'. Not byte-level: a step-3 failure is a crc_of_crc_array or segment-CRC mismatch, which only a nonconforming file exhibits, and for such a file [R-CNF-12] already lets any reader reject everything. No conforming file can exercise the condition.

### cod11-cannot-establish-trigger-and-tile-resource-decline — CONFIRMED

- merged: `verifier:RD-10`
- location: §2.3 [R-CNF-11]; §17.4 [R-COD-11]; §21.9 [R-ERR-04]; §18.2 [R-MTA-09]
- severity: editorial

Confirmed by reading [R-COD-11] against [R-CNF-03]. §2.3 lists 'it cannot execute a codec or filter' as a cannot-establish trigger, but [R-COD-11] itself says that position 'arises only at a reserved or experimental value' for a conforming reader — and those are reject-layer, i.e. nonconforming, not cannot-establish — while 'software unable to execute an assigned codec or filter is not a conforming reader'. The only live path is a resource decline under [R-ERR-04] (a wide zstd window, an oversized tile), and §17.4 never says a tile-level resource decline yields cannot-establish, though §18.2 spells out exactly that shape for over-bound documents ('the bound is that verifier's capability and not a limit on validity … so it MUST report that it cannot establish'). Not byte-level: §21.9 keeps the file conforming under all three readings, all three bar certification, and [R-ERR-04] forbids reporting the refusal as a validity error. What differs is a report label.

### writer-divergence-catalogue-not-a-defect-claim — REFUTED

- merged: `writer:WR-11`
- location: Whole document; catalogue anchored at §2.3 [R-CNF-05], §5.2, §9.2, §16, §17, §18.2, §20.5, Appendix G
- severity: none

Not a defect and not offered as one — the reporter says so in terms ('This is the requested catalogue of legitimate byte divergence, not a defect claim'). Every entry is a divergence the document deliberately licenses under [R-CNF-05] ('two conforming writers given identical input MAY produce different conforming files'), so both outputs are conforming and every reader and verifier reaches the same verdict on each. The two entries that would move bytes were broken out as WR-02 and WR-06 and are judged there. Recorded here solely to keep coverage complete; it contributes nothing to the defect count and nothing to the byte-level count.
