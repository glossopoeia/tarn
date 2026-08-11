# Cleanroom round 7 — triage pass: correctness

Distinct defects: **44**. Byte-level: **0**.

**Coverage check.** All 63 input findings appear in exactly one judgement. Counts by role: reader 8 (RD-01..RD-08), writer 11 (WR-01..WR-11), verifier 11 (RD-01..RD-11), diagrams 9 (DG-01..DG-09), register 12 (RD-01..RD-12), adversary 12 (RD-01..RD-12) = 63. Sum of finding_ids across the 44 judgements: 5+4+5+3+2+2+2+1*13+2+1*4+2+2+1*17 = 63. Nothing dropped. Merges performed: [R-MTA-07] missing row (5 findings); §2.3 parenthetical (4); §21.7 inventory (5); §8.1 uncovered extent (3); §20.4 MU=1 row (2); §19 tier enumerations (2); Appendix A suffix window (2); verdict priority (2); instance arithmetic (2); F5/L3 no witness (2). reader:RD-05 was kept separate from the Appendix A pair because its claim is about §19.1 step 1's timing wording, not the appendix's window arithmetic. register:RD-11 was kept separate from register:RD-04/diagrams:DG-09 because it concerns L2's non-constructible instances and the word "named", not the alternatives-times-containers product.

## Judgements

### mta07-standardized-key-no-register-row — CONFIRMED

- merged: `reader:RD-03`, `writer:WR-04`, `verifier:RD-01`, `register:RD-02`, `adversary:RD-03`
- location: §18.4 [R-MTA-07]; §21.1 completeness clause; §21.2–§21.5; §2.4 [R-CNF-07]
- severity: register-bookkeeping

Verified. [R-MTA-07] reads verbatim: 'A file carrying a standardized key outside its listed scope is nonconforming, and a verifier detects it ([R-CNF-11]); no reader's behavior turns on the violation, since a reader ignores the key either way.' I searched §21.2–§21.5 and §21.6: no row for it. §21.1 makes register completeness normative, so the omission is a defect as stated. [R-CNF-07]'s four-outcome vocabulary also has no value that fits 'the reader ignores the key, not the record'. NOT byte-level: verifier:RD-01's reading 1 (register-as-second-authority ⇒ certify) is foreclosed by §21.1's own words — an omitted row 'is a defect in this document', not a licence — and by 'where a row and the rule it cites diverge, the rule governs'. Here the rule is not silent; it states the verdict outright. Both verifiers refuse certification on a layer-scope document carrying `tarn.created`; both readers ignore the key. This is precisely the previous round's over-claim pattern.

### cnf03-parenthetical-vs-21.6-closing — PARTIAL

- merged: `reader:RD-04`, `writer:WR-09`, `verifier:RD-06`, `register:RD-03`
- location: §2.3 [R-CNF-03]; §21.6 closing paragraphs; §21.9 [R-ERR-04]
- severity: editorial

Narrower than three of the four reporters state. §2.3 attaches three qualifiers; §21.6 names 'version_major naming a major this reader does not implement' and 'an experimental-range record type carrying MU = 1'. Restricted to *conforming* files — which is §2.3's subject — the second §21.6 case IS §2.3's second qualifier: a reserved-range MU=1 type is a violation (F38/F39), so the only unimplemented MU=1 type a conforming file can carry is experimental. So 'those two exceptions' = qualifiers 1 and 2, and §21.6 matches (verifier:RD-06's reading 2, the only reading under which the pointer works). What is genuinely defective: §2.3's third qualifier (§21.9 guarantees) gets no cross-reference at all, and §21.6's flat claim 'Two distinct cases are conforming files a reader nevertheless refuses' under-enumerates — [R-ERR-04]'s resource decline is a third. Not byte-level: [R-CNT-07], [R-CNT-15] and [R-ERR-04] each state their ground independently.

### err01-inventory-not-exhaustive — CONFIRMED

- merged: `reader:RD-08`, `writer:WR-08`, `verifier:RD-09`, `register:RD-09`, `adversary:RD-09`
- location: §21.1 ('§21.7 the inventory of what fails it'); §21.7 [R-ERR-01] second paragraph
- severity: register-bookkeeping

Verified. §21.1 says 'detectability being the gate [R-CNF-07] already applies and §21.7 the inventory of what fails it'. §21.7's second paragraph names exactly [R-LIF-01], [R-LIF-03], [R-GEO-06], [R-SER-01], and [R-CNT-13]'s no-embedded-offsets rule. Omitted MUST-level obligations with no single-file witness, of exactly the same kind: [R-LIF-02]'s commit ordering and barriers, [R-LIF-04]'s truncate-or-overwrite, [R-LIF-06]'s recovery reporting, [R-WRT-05]–[R-WRT-09] (byte-identical re-emission, fresh file_id, verification depth), [R-CNT-08]'s updater copy-forward, [R-CNT-26]'s minor floor, [R-IDX-01]'s disk-ordinal entry order (the index analogue of the already-listed [R-GEO-06]/[R-SER-01] mappings), and [R-PRV-01]. Since §21.7 already lists actor/history obligations, the omitted ones cannot be excluded on kind. Not byte-level: every omitted item is either actor conduct or a multi-generation property; no verifier can reject on any of them.

### cnt19-unknown-record-extent-uncovered — CONFIRMED

- merged: `verifier:RD-04`, `diagrams:DG-01`, `adversary:RD-05`
- location: §8.1 [R-CNT-19] map; §5.2 [R-CNT-02]; §9.7 [R-LIF-08]
- severity: editorial

Verified. §5.2 defines a structure to include 'a record extent (the bytes any record's extent slot references, whatever the record's type, §7.2)'. §8.1's map has six rows and only two of them are record extents (tile-index region, user-metadata extent). §21.6 registers an experimental-range MU=0 record as conforming, and §7.2 licenses it to carry an extent. So a conforming file can carry a live-state structure covered by no checksum, and §9.7's clause 'each verifies against the checksum covering it (§8.1)' is vacuous for it — a real hole in the integrity claim, and a third residue §22.3's 'Two residues are stated rather than defended' does not name. Not byte-level: no register row exists for an uncovered structure, §21.6 fixes the file as conforming, and readers ignore-record such a type without fetching its extent, so both verifiers certify and both readers behave identically.

### wrt08-mu1-row-forbids-layer-edit — CONFIRMED

- merged: `writer:WR-01`, `adversary:RD-06`
- location: §20.4 [R-WRT-08] persistence table, MU = 1 row; §20.3 [R-WRT-04] step 4; §7.3
- severity: editorial

Verified. §20.4's introducing sentence is 'Persistence governs every record type; only the authoritative source of the flags differs. For a type §7.3 registers, the registry's fixed flags govern rather than the stored ones ([R-CNT-22])'. §7.3 fixes the layer record at MU = 1, PE = 1. The table's MU = 1 cell begins 'Retain byte-identical. The updater MUST NOT modify the scope the record governs' — which, applied to a layer record, forbids every append §20.3 defines. Real drafting contradiction. Resolved by the cell's own gloss ('an unknown critical record at layer scope'), [R-CNF-06]'s scoping to 'records it does not understand', Appendix H's 'never modifies a scope governed by an unknown critical record', and [R-WRT-05]'s 'retains and does not logically modify'. Not byte-level: any file the permissive updater emits is conforming under both readings ([R-CNF-02] is a pure predicate on bytes); the restrictive reading yields an updater that refuses to act, not divergent bytes.

### s19-tier-enumerations-under-inclusive — PARTIAL

- merged: `reader:RD-01`, `diagrams:DG-05`
- location: §19.1 step 4 [R-RDR-01]; §19.3 [R-RDR-03]; §21.2 F24/F25/F26; §21.3 L1/L3/L5/L11/L12/L13
- severity: editorial

The under-enumeration is real. §19.1 step 4 cites only [R-CNT-12], [R-CNT-15], [R-CNT-14], [R-CNT-13] and [R-ENC-12], yet F24/F25/F26 are reject-file rows with Detected = open governed by [R-CNT-25] and [R-MTA-03] — and [R-CNT-13] does not reach them, since it says '(0, 0) means no extent' while §7.1/[R-CNT-25] is what forbids (0,0) on a user-metadata record. §19.3 likewise omits [R-ENC-11] (L5), [R-ENC-06] (L3), [R-ENC-03] (L1) and the sub-record quarantine rules (L11/L12/L13). Since §19 opens 'This section consolidates the reader's normative path', that is a defect. But reader:RD-01's byte-level claim fails: §19.1 is silent, not contrary — 'all decidable from the resident bytes and F' qualifies the listed items and closes nothing — and §19's own preamble says each step 'cites the requirement whose outcome governs its failure'. [R-CNF-04] plus the register's Detected column oblige the check, so reader B is nonconforming under a rule already written. diagrams:DG-05 judged this correctly.

### appendix-a-suffix-window-reaches-zero — CONFIRMED

- merged: `verifier:RD-11`, `diagrams:DG-07`
- location: Appendix A, closing paragraph
- severity: editorial

Verified. Appendix A says '...as a remote reader does too whenever it speculates a suffix window, since this file is 128 bytes and any such window reaches offset 0.' False as written: a 64-byte suffix window reaches offset 64, and per §6.4's containment rule a reader needs only to reach dir_offset = 16, so a 112-byte window covering [16, 128) makes request 2 unnecessary while leaving [0, 16) non-resident. Both reporters are right; DG-07's containment point is the sharper of the two. Not byte-level: the appendix is non-normative under [R-CNF-01], §6.1 states the residency test correctly, and F8's condition cell already records the conditionality.

### s19.1-front-block-residency-timing — CONFIRMED

- merged: `reader:RD-05`
- location: §19.1 step 1 [R-RDR-01]; §6.1 [R-CNT-04]
- severity: editorial

Verified. §19.1 step 1 conditions the obligation on 'A reader holding bytes [0, 16) once this step completes', releasing 'one that would have to fetch them'. §6.1 states the test over the whole open — 'A reader whose open leaves bytes [0, 16) resident — a local file, a memory mapping, a speculative suffix window that reached offset 0, or any transport already holding them' — and releases only a reader needing 'a further range request'. Step 1 is 'Obtain the transport-authoritative file size F', which for a remote reader is fused with the step-2 suffix fetch by §19.1's own text, so 'once this step completes' inverts the answer for a speculating reader when read alone. Not byte-level: §19.1 introduces no new rule (its preamble says each step cites the governing requirement) and §6.1 names the speculative case explicitly, so only one reading is permitted. The reporter judged this correctly.

### cnf04-overbroad-reader-detection-duty — CONFIRMED

- merged: `reader:RD-02`
- location: §2.3 [R-CNF-04]; §19.2 [R-RDR-02]; §21.1; §6.2 [R-CNT-05]
- severity: editorial

Verified. [R-CNF-04] says flatly 'A reader MUST detect the violations enumerated in the error register (§21) and apply the outcome class this specification assigns to each.' Roughly twenty rows carry Detector = verifier, and three passages contradict the literal reading: §19.2 ('a violation whose assigned detector is the verifier ... imposes no reader obligation'), §21.1 ('For a row whose Detector is verifier, the outcome names the scope at which the damage is recorded, not an obligation on any reader'), and §6.2 ('readers check neither, their check being the dir-bounds rule of [R-CNT-06]'). [R-CNF-04] is simply overbroad as drafted. Not byte-level: every file exhibiting a verifier row is nonconforming, [R-CNF-12] already lets any reader reject it, and [R-SER-08] fixes the single returned-byte case with an explicit conditional.

### mta09-ignore-record-vs-err04-file-decline — PARTIAL

- merged: `reader:RD-07`
- location: §18.2 [R-MTA-09]; §21.9 [R-ERR-04]; §2.3 [R-CNF-03]
- severity: editorial

The tension in wording is real — [R-MTA-09] assigns ignore-record to an over-bound document, while [R-ERR-04] permits declining 'at the whole file' any file exceeding a §21.9 guarantee and lists only 'a layer or a tile' as narrower scopes. But the reporter's byte-level argument rests on reading 1 obliging acceptance, and that is refuted by the very rule it invokes: [R-CNF-03] reads 'A reader MUST accept every conforming file ... and none of whose values exceeds the minimum guarantees of §21's limits table'. A file carrying a 20 MiB document exceeds the 16 MiB guarantee, so no reader ever MUST accept it. Both readings therefore leave the same set of files must-accepted, and [R-ERR-04]'s licence to decline over-guarantee files is a divergence the document deliberately grants throughout. What survives is only the drafting question of whether [R-MTA-09] narrows [R-ERR-04] for documents.

### layer-scope-failure-mid-request — PARTIAL

- merged: `reader:RD-06`
- location: §19.4 step 8 [R-RDR-04]; §2.4 reject-layer row; §15.4 [R-IDX-04]
- severity: editorial

Verified that §19.4 step 8's 'MAY return the validating entries' values ... or fail the request as a whole' is stated only for entry-bounded (tile-scope) rejections, while step 3's index-chain failure takes layer scope ([R-IDX-04], and §19.2 says so expressly). §2.4's reject-layer row does answer it, though: the outcome 'bars further service from the layer' and 'does not retroactively invalidate content already returned' — samples not yet delivered are further service. So the corner is under-drawn rather than undecided. Not byte-level: only a corrupt, hence nonconforming, file exhibits a segment-CRC or crc_of_crc_array mismatch, and [R-CNF-12] already permits rejecting it entire.

### commit-pointing-at-prior-generation-directory — PARTIAL

- merged: `writer:WR-02`
- location: §9.2 [R-LIF-02] step 3; §5.1 [R-CNT-01]; §3.1; §21.2 (no row)
- severity: editorial

The observation is right: no byte-testable rule forbids a generation-2 trailer from addressing generation 1's directory. I verified the 192-byte construction — dir_offset 16, dir_length 4, 20 ≤ 192−64, live state front + [16,20) + [128,192), slack [20,128) which holds the superseded trailer (slack, not a live structure, so F9 does not fire), all CRCs verifying, §9.7's walk passing. I also note the condition IS detectable, contra the usual assumption: generation ≥ 2 implies the commit began at a prior F ≥ 128 ([R-LIF-01], [R-CNT-27]), so a live directory at offset 16 provably was not appended by this commit. That makes it a candidate for §21.1's completeness clause. But it is not byte-level, because no rule declares the resulting file nonconforming — unlike [R-MTA-07], which says 'is nonconforming' outright. [R-LIF-02] step 3 is an unqualified MUST on the writer; the register has no row; §9.7 fixes what a verifier walks and this is not in it. A verifier reporting nonconforming would be reporting a condition the document never assigns. Conforming file, nonconforming writer — the reporter's own picked reading. This was the closest call in the set.

### compactor-flags-zero-vs-copy-forward — PARTIAL

- merged: `writer:WR-03`
- location: §6.3 [R-CNT-08]; §20.5 [R-WRT-06]; §20.1 [R-WRT-01]
- severity: editorial

The textual friction is real: [R-CNT-08] says 'a writer creating a file under this text MUST write flags = 0' and scopes copy-forward to 'An updater ... of the file it modifies', while a compactor emits a new file at generation 1 under a fresh file_id and [R-WRT-06] directs it to copy the input's ignore-lane bits forward. But [R-WRT-06] names the compactor case specifically, cites [R-CNT-08], and gives the reason ('a compactor cannot know which minor version defined an ignore-lane bit it does not implement'), so specificity settles it — this is thinner than an undecided rule. Not byte-level: [R-CNT-08] and [R-CNF-02] jointly declare a set ignore-lane bit not to be a file-conformance violation, and every reader ignores bits 16–31, so both outputs are conforming and no verdict changes.

### extent-growth-metadata-only-misstatement — CONFIRMED

- merged: `writer:WR-05`
- location: §11.1 Rationale; §13.3 'Note — sparse writing'; §20.3 [R-WRT-04] step 4
- severity: editorial

Verified both statements verbatim: §11.1's Rationale, 'extent growth is a metadata-only operation under this specification's commit model', and §13.3's Note, 'Extent growth is a metadata-only operation (§11.1)'. It is false whenever growth changes a grid count: §20.3 step 4 requires the whole tile-index region re-emitted and notes '(a geometry change renumbers ordinals, [R-GEO-06])', and [R-CNT-17] ties extent_length to entry_count. The schema-first case the Rationale is selling — E = 0 growing to E > 0 — is the worst case, since the layer goes from extent (0,0) and a zero-byte index to a full index region. Not byte-level: both sit in Rationale/Note blocks, non-normative under [R-CNF-01], and a writer that believed them emits a file failing [R-CNT-17], already registered as L22/L23.

### index-relocation-for-untouched-layer — PARTIAL

- merged: `writer:WR-06`
- location: §20.3 [R-WRT-04] step 4; §20.4 [R-WRT-05]
- severity: editorial

Narrower than reported. §20.3 step 4's own trigger list — 'Every layer whose stored-tile set, index content, or index placement this commit changes' — presupposes that index placement can change, and [R-WRT-05]'s byte-identity obligation is expressly conditioned on records the updater 'retains and does not logically modify'. So relocation is evidently contemplated; what is unstated is only whether an appender may elect it for a layer it otherwise leaves alone, against 'A layer whose record alone changes keeps its extent slot, pointing at the existing region'. Not byte-level: the relocated file is conforming under either reading (live extent, disjoint, checksum-consistent, old region becomes slack that [R-CNT-21] leaves unconstrained), no register row distinguishes them, and [R-CNF-05] already licenses two writers to emit different bytes.

### s9.7-walk-double-claims-layer-index — CONFIRMED

- merged: `writer:WR-07`
- location: §9.7 [R-LIF-08]; §21.2 row F36; §7.4
- severity: editorial

Verified. §9.7 reads 'it enumerates the live directory and its records, each record's extent, and each layer's tile-index region together with that region's non-sentinel entries', then 'checks that these occupy disjoint byte ranges'. §7.4: 'A layer record's extent slot addresses the layer's tile-index region (§15)'. So for every layer with a non-empty index the same bytes are enumerated twice, under 'each record's extent' and under 'each layer's tile-index region', and the disjointness check fails on every layered file. Real imprecision in the enumeration. Not byte-level: the literal reading is self-refuting — it would make Appendix H's own 'Conforming file' checklist and §21.6's normal cases unsatisfiable — and §21.3's L19 instance cell ('stored-tile extents; tile-index region; layer sub-record extents', pointedly no separate layer-record extent) makes the dedup explicit. The reporter's L19 evidence is the right one.

### s7.4-table-missing-taxonomy-class — PARTIAL

- merged: `writer:WR-10`
- location: §7.4 layer-record layout table; §4.7 Note and [R-ENC-16]
- severity: editorial

Half confirmed. §4.7's Note says layout tables give 'byte offset within the structure, size, type, name, taxonomy class, and valid range', and [R-ENC-16] is normative that 'Every field this specification defines is classified structural, semantic, or informative.' §7.4's table gives only Field / Type / Constraint — no class column, unlike §6.2, §7.2, §15.1 and §18.2 — and while some of its fields are classified in their defining sections (linearization §11.4, sample type §12, fill §13.1), layout, codec, filter, A, S, A_slab, d, C, index_encoding, entry_count and crc_of_crc_array are classified nowhere. The byte-offset half of the complaint is not a defect: the inline payload is variable-length, so no field has a fixed offset. The 'informative' class being uninstantiated is confirmed and is fairly characterized as a cost to a future minor version. Not byte-level: [R-ENC-16]'s only normative consequence has no subject in major 1.

### writer-divergence-catalogue — REFUTED

- merged: `writer:WR-11`
- location: whole document (catalogue deliverable)
- severity: none

Not a defect claim and does not assert one: the reporter states it is the requested catalogue of divergence the document deliberately licenses, with its two live items broken out as WR-02 and WR-06 (both judged separately above). Nothing here to confirm or refute against the text; no location is alleged to be wrong. Counted for coverage only.

### mta07-value-shape-status-unstated — PARTIAL

- merged: `verifier:RD-02`
- location: §18.4 [R-MTA-07], [R-MTA-08]; §2.1 [R-CNF-01]
- severity: editorial

The silence is real and correctly identified: [R-MTA-07]'s reader clause covers a key 'whose value does not match the shape its row gives', but its nonconformance sentence is narrowed to 'outside its listed scope', and the writer prohibition is likewise only 'MUST NOT emit a standardized key outside the scopes its row lists'. So the document never says whether a wrongly-shaped standardized value makes the file nonconforming. Not byte-level, and the reporter's own picked reading is the right one: no requirement anywhere binds a writer to the Value column, §18.4's lead calls every key 'OPTIONAL and advisory', and §21's register — whose completeness is normative — carries no row, which for a detectable condition means it is not a violation. {"tarn.title":42} is a conforming file under the only supported reading, so no two verifiers diverge.

### slab-continuity-across-rejected-entry — PARTIAL

- merged: `verifier:RD-03`
- location: §15.3 [R-IDX-03]; §16.2 [R-SLB-03]; §21.3 L42
- severity: editorial

The gap is real: [R-IDX-03] removes a reject-tile entry's extent from 'the verifier rows, which bind over well-formed entries' extents only', and §16.2 grants transparency explicitly and only to sentinels ('Sentinel tiles are transparent to run continuity'), so whether L42 is evaluated across a removed mid-run entry is unstated. The byte-level argument fails on two independent grounds I checked in the text. First, [R-CNF-09] reads 'A reader MUST NOT return data as valid from a scope this specification rejects *and whose rejection this reader is obliged to detect*' — L42's Detector is verifier, and [R-SLB-03] says 'readers are not obligated to' check the invariant, so no reader is barred from returning tile 0's samples under either reading. Second, the reporter's own construction puts a non-sentinel entry with length = 0 in the run, which is T10 reject-tile, so the file is nonconforming under both readings and no verifier certifies either way. What differs is only which additional row a verifier records.

### verdict-priority-nonconforming-vs-cannot-establish — CONFIRMED

- merged: `verifier:RD-05`, `adversary:RD-04`
- location: §2.3 [R-CNF-11]; §18.2 [R-MTA-09]; §17.4 [R-COD-11]
- severity: editorial

Verified. [R-CNF-11] defines three verdicts and says cannot-establish is 'the last where some requirement is one it is unable to check', but states no priority for a file that simultaneously exhibits an established violation and an uncheckable requirement. [R-MTA-09] sharpens the conflict: the declining verifier 'MUST report that it cannot establish the file's conformance rather than that the file is nonconforming', which reads as an obligation over the whole-file report. So two verifiers with identical capabilities can report differently on one file. Not byte-level: neither verdict certifies, and [R-CNF-12]'s reader licence is triggered by the detected violation itself, present under either verdict. The consequence is a misdirected operator, not a byte.

### slack-total-must-vs-stop-at-first-violation — PARTIAL

- merged: `verifier:RD-07`
- location: §5.2 [R-CNT-21]; §2.3 [R-CNF-11]
- severity: editorial

The tension is real but the document is closer to answering it than reported. [R-CNT-21] places an unconditional MUST on reporting the slack total, with the escape 'where a scope-level rejection stops the walk of §9.7 from enumerating a region's claimants, the verifier MUST report the total as partial and name the regions it could not walk'; [R-CNF-11] separately licenses stopping at the first violation. A verifier that stops early has had its walk stopped by a rejection, so the partial mechanism plainly fits, and the reporter's picked reading 1 follows. The residue is that 'a scope-level rejection stops the walk' is not obviously the same event as an elective early stop. Not byte-level: §5.2 says slack's 'content is unconstrained, and no conformance requirement applies to it', so this is report content only.

### s9.6-probe-has-no-stated-verifier-consequence — CONFIRMED

- merged: `verifier:RD-08`
- location: §9.6 [R-LIF-06]; §9.7 [R-LIF-08]
- severity: editorial

Verified. §9.6 opens 'Recovery tools and verifiers — never conforming readers on the default path — locate commit states as follows', and nothing in §9.6, §9.7 or §2.3 states what a verifier does with the result. §9.7's Note ('Nothing here enumerates prior commits') and 'coverage verification does not' point the other way, leaving the mention of verifiers with no assigned consequence. Not byte-level, and the reporter's own analysis is correct: F19 and F10 already fix the whole-file verdict on a file whose tail is not a valid trailer, §2.3 makes conformance a pure predicate on the bytes handed over, and §9.6's own 'recovery output MUST be re-verified as a whole file' makes the truncated prefix a separate artifact. Reading 2 is therefore not available to any implementation reading the whole document.

### cod11-cannot-execute-trigger-near-dead — CONFIRMED

- merged: `verifier:RD-10`
- location: §2.3 [R-CNF-11]; §17.4 [R-COD-11]; §21.9 [R-ERR-04]
- severity: editorial

Verified. §2.3 lists 'when it cannot execute a codec or filter ([R-COD-11])' as a cannot-establish trigger, but [R-COD-11] itself says 'software unable to execute an assigned codec or filter is not a conforming reader ([R-CNF-03])' and that a conforming reader meets the position 'only at a reserved or experimental value', where it rejects the layer — i.e. the file is nonconforming and the verdict is nonconforming, not cannot-establish. So the trigger has no live path for a conforming verifier except a resource decline under [R-ERR-04], and the document never routes a tile-level resource decline to cannot-establish the way [R-MTA-09] explicitly does for documents. Not byte-level: §21.9 fixes the file as conforming under all readings, and all bar certification while forbidding a validity-error report.

### f31-l50-scope-collision-for-layer-records — CONFIRMED

- merged: `register:RD-01`
- location: §21.2 F31; §21.3 L50; §7.3 [R-CNT-22]; §7.2 [R-CNT-13]
- severity: register-bookkeeping

Verified. F31's condition is 'A top-level record of a type §7.3 registers carries a stored MU or PE bit differing from the value the registry fixes'; type 0x0001 (layer) is a top-level registered type, so F31 claims layer records, and it sits under §21.2's 'Outcome: reject-file'. L50 claims the same files for reject-layer. [R-CNT-22] plus §7.2's mapping ('the layer for a layer record and for sub-records, the file for other top-level records') decide it: layer scope, so L50 governs and F31 must be read as restricted to non-layer top-level records. Not byte-level, and this is the exact pattern the round-6 calibration names: §21.1's 'where a row and the rule it cites diverge, the rule governs' already decides it, only the table is wrong, and [R-CNT-22] obliges every reader to apply the fixed semantics regardless.

### instance-arithmetic-applied-inconsistently — CONFIRMED

- merged: `register:RD-04`, `diagrams:DG-09`
- location: §21.1 Instances paragraph; F33; L1; L16; R5; §21.8
- severity: register-bookkeeping

Verified against the cells. §21.1 states the product rule — 'a condition applying to two alternatives in two containers has four' — and in the same paragraph the counting rule, 'Instances within a cell are separated by semicolons ... the count is therefore mechanical once the cell is written.' The two are applied inconsistently to one and the same [R-CNT-13] condition: F33 ('exactly one half zero', one container) enumerates the two alternatives 'extent_offset; extent_length', while L16 (the identical condition over two containers) enumerates only 'layer record extent slot; sub-record extent slot' and drops the alternatives, giving 2 where the product rule gives 4. R5 likewise lists containers only, and L1 lists two fields that each occur in two containers as two instances. The 'mechanical once the cell is written' clause makes §21.8's 242 self-consistent, so the corpus size is not in doubt; the defect is the inconsistent application, and DG-09's reading 1 is right about which authority controls. Not byte-level: §24 makes the corpus derivative, and every affected condition has an unambiguous outcome from its governing rule.

### f5-l3-width-error-no-isolable-witness — CONFIRMED

- merged: `register:RD-06`, `diagrams:DG-08`
- location: §21.2 F5; §21.3 L3; §4.2 [R-ENC-06]; §21.8 [R-ERR-02]
- severity: register-bookkeeping

Both halves verified and they are one defect. F5's condition requires 'total size unchanged', but its own worked instance — 'trailer (e.g. version_major/version_minor written as u32 each)' — adds four bytes to a structure §6.3 fixes at 64 with 'zero slack: every byte is assigned', so the instance cannot be built under the condition (DG-08). That is a symptom of the general point (register:RD-06): with total size held fixed, a reader parses at the widths this specification fixes and has no other layout available, so the resulting bytes are either wholly valid or caught by some other row's value gate. F5 and L3 name writer intent, which is not a property of a file, and [R-ERR-02]/[R-VEC-03] nevertheless demand a vector per instance. They belong with §21.7's inventory. Not byte-level: no byte sequence's classification turns on either row.

### scope-of-the-word-register-in-21.1 — PARTIAL

- merged: `register:RD-05`
- location: §21.1 opening; §21.6; §21.7; §21.8
- severity: editorial

Mostly answered by text the reporter did not weigh. §21.8 [R-ERR-02] fixes the register's extent explicitly — 'Every row of §21.2 through §21.5 — 125 conditions over 242 named instances' — and §21.5's preamble treats §21.6 as a separate list ('§21.6 lists the ignore-record conditions that are not violations'), while §21.1 enrols §21.7 by role. So 'the register below' = §21.2–§21.5, and the completeness clause and instance arithmetic have a determinate scope. What is genuinely unstated is only whether §21.1's row-versus-rule tiebreak extends to §21.6's table, whose rows carry the same Rule column. Not byte-level, and the reporter tested the right thing: [R-CNF-02] plus §10.3 plus [R-MTA-03] already yield 'conforming' for an experimental metadata encoding without §21.6 being sole authority.

### cod05-cod07-lack-reader-side-clause — CONFIRMED

- merged: `register:RD-07`
- location: §21.4 T15, T16, T23; §17.2 [R-COD-05], [R-COD-07], [R-COD-08]
- severity: register-bookkeeping

Verified. [R-COD-05] is one sentence — 'The stored bytes are exactly one DEFLATE compressed data stream as defined by RFC 1951 — raw, not a zlib (RFC 1950) or gzip (RFC 1952) wrapper.' — with no reader clause, and [R-COD-07]'s only reader clause is about the decoded-size cap ('a reader MUST treat such a declaration as a validity error at layer scope'), not about frame-versus-block. Compare [R-COD-06], which spells the check out: 'a reader MUST treat a payload whose first four bytes are not that magic ... as a validity error at tile scope'. Yet T15, T16 and T23 assign Detector = reader at tile use citing [R-COD-05]/[R-COD-07]. This also breaks §2.1's stated phrasing discipline that 'every writer-side prohibition is paired with an explicit reader-side clause'. Not byte-level: detection flows from [R-COD-08], any such file is nonconforming, and the reporter's LZ4/zlib analysis showing the divergence is unreachable checks out.

### t13-duplicates-t25 — CONFIRMED

- merged: `register:RD-08`
- location: §21.4 T13, T25; §17.1 [R-COD-02]; §17.2 [R-COD-08]
- severity: register-bookkeeping

Verified. T13's instances are 'deflate stream carrying a previous tile's history window; lz4 block whose match offset reaches before its own output start'; T25's include 'lz4 match offset 0 or match reaching past produced output'. The lz4 instances are one condition stated from two sides, and a deflate stream referencing a prior tile's window is likewise a back-reference before the start of output — a decode failure, T25's procedure. T13 has no detection procedure of its own, and unlike T26 it carries no gloss saying it 'records the cause rather than a procedure of its own'; §21.1's specialization list (F2/F8/F10, F38/F39, L25/L26) omits the pair. Not byte-level: identical outcome, detector and detection point, so the same tile is rejected either way; the cost is duplicate corpus vectors under [R-ERR-02].

### r5-omits-unpaired-surrogate-escape — CONFIRMED

- merged: `register:RD-10`
- location: §21.5 R5; §18.2 [R-MTA-04] fourth bullet
- severity: register-bookkeeping

Verified. [R-MTA-04]'s fourth bullet names two failure modes — 'including after escape resolution: a \uXXXX escape denoting an unpaired surrogate has no UTF-8 encoding and makes the document unreadable, as does an ill-formed byte sequence in the source' — and R5's condition and instances carry only the second ('a key or string value containing ill-formed UTF-8'). I checked the neighbouring rows: R7 covers 'not well-formed JSON', which an unpaired-surrogate escape is not (RFC 8259 admits any \uXXXX), so no row anywhere reaches it. Given §21.1's normative completeness, that is a genuine omission. Not byte-level: [R-MTA-04] states the consequence ('makes the document unreadable') and §7.1's quarantine fixes unreadable as ignore-record with a SHOULD-report, so both implementations behave identically; the loss is a corpus vector.

### named-instances-wording-and-l2-cell — PARTIAL

- merged: `register:RD-11`
- location: §21.8 [R-ERR-02]; §21.1; §21.3 L2
- severity: register-bookkeeping

Split verdict. The wording point is confirmed: [R-ERR-02] says '125 conditions over 242 named instances', but §21.1 provides that 'a cell reading — is one instance', and a large share of rows carry exactly that, naming nothing — so 'named' is the wrong word. I independently confirmed the row counts (F1–F39 = 39, L1–L50 = 50, T1–T26 = 26, R1–R10 = 10, total 125, matching each subsection's stated count). The second claim — that two of L2's ten instances are files that cannot exist on their own — is asserted without identifying which two, and I could not reproduce it: with C = 1 the products N·P, C·N, V = P·C and max disk ordinal come apart, and P·Q versus P·Bᶜ are distinguished by layout. Unverified, so not confirmed. Not byte-level: [R-ENC-04] gives one outcome for every quantity in the cell.

### limits-table-no-composition-rule — CONFIRMED

- merged: `register:RD-12`
- location: §21.9 [R-ERR-03], [R-ERR-04]; §2.5 [R-CNF-10]
- severity: editorial

Verified. [R-ERR-03] reads 'a conforming reader MUST accept any conforming file whose quantities lie within these bounds', per quantity and with no composition rule, and [R-ERR-04]'s escape is stated for 'A file exceeding any of these' — which a file combining in-bounds quantities does not do. So the literal reading obliges acceptance of a 65,536-layer × 2³²-tile file whose index regions alone are petabytes, and 'Software that declines a file whose every quantity lies within the table is not a conforming reader' reinforces it. Not byte-level: no such byte sequence can be produced or served, §24 already declines to build a vector even at the single-row tile-count bound, and either way [R-ERR-04] requires a refusal to be reported as a resource limit rather than a validity error, so no intact data is mislabelled corrupt.

### lz4-cap-quantified-over-addressed-tiles — PARTIAL

- merged: `adversary:RD-01`
- location: §17.2 [R-COD-07]; §21.3 L45; §11.1 [R-GEO-02]; §4.2 [R-ENC-04]
- severity: editorial

The asymmetry the reporter identifies in their own reading 3 is real and is the finding: [R-COD-07] and L45 are quantified over addressed tiles ('a layer any of whose addressed tiles' decoded size exceeds 0x7E000000'), while [R-ENC-04] is not ('any quantity this specification defines as a sum or product'), and [R-SER-02]/[R-SER-07] make P·Q, P·Bᶜ and V declaration-derived quantities that exist as soon as the declarations do. But the claimed ambiguity is not one. An empty universal quantification is vacuously satisfied; that is not a gap, and nothing in §11.1, §19.3 or §21.6 converts an explicit quantifier into a declaration-level bound. Rule and register row agree word for word, so no verifier fork survives: the reporter's E₀ = 0 / decoded size 0x7E000001 file is conforming, and their second construction (P·Q = 2⁶⁷) is reject-layer under [R-ENC-04] and L2 regardless of tile count. Not byte-level. Worth an editorial note only because extent growth can later make a conforming lz4 declaration invalid.

### mta09-encoding2-occupancy-unregistered — PARTIAL

- merged: `adversary:RD-02`
- location: §18.2 [R-MTA-09]; §21.5 R3, R4
- severity: register-bookkeeping

The register omission is confirmed; the ambiguity is not. [R-MTA-09]'s main clause states the requirement — 'Encoding 2 stores it as exactly one RFC 8878 compressed frame *occupying the extent's bytes before its terminal CRC*' — in the same declarative style [R-COD-05] uses for deflate, whose violations §21.4 registers as T15/T16/T24. The following clause, 'under the frame constraints of [R-COD-06] that do not reference a tile: ...', adds constraints; it does not limit the main clause, so the reporter's reading 2 requires striking the sentence's own subject. Trailing bytes therefore make the file nonconforming, and 'Any violation here is ignore-record' supplies the reader outcome. What is genuinely defective: R4's ten instances are exactly the four enumerated carried-over constraints and R3 is decode failure, so occupancy has no register row, hence no assigned detector and no vector — the same family as the [R-MTA-07] omission. Not byte-level: with the main clause governing, no conforming verifier certifies the reporter's extent.

### name-uniqueness-vs-inline-framing-order — PARTIAL

- merged: `adversary:RD-07`
- location: §19.1 step 4 [R-RDR-01]; §7.4 [R-CNT-18]; §21.3 L24
- severity: editorial

A real ordering question, narrower than stated. §19.1 step 4 has the open parse every layer record's name and decide duplicates at file scope, while [R-CNT-18]'s requirement that the name field 'lie entirely within the inline payload' is layer-scope and §19.3 places it at layer access — so a name whose length prefix overruns its inline payload is met at open by a rule that has not yet been applied. But §19.1's 'Uniqueness is decided first' is qualified by its own justification in the same sentence — 'over the raw name bytes whether or not each name is itself well-formed — [R-ENC-12] makes name comparison a byte comparison, which needs no valid name' — which is about §4.6 well-formedness, not framing. So reading 1 (framing first, L24 reject-layer) is the supported one. Not byte-level: the file is nonconforming under both orders and [R-CNF-12] lets any reader reject it entire, so no reader is obliged to serve layer X under either.

### overlong-pre-trailer-pad-conduct-class — PARTIAL

- merged: `adversary:RD-08`
- location: §6.2 [R-CNT-05]; §9.2 [R-LIF-02] step 5; §2.3 [R-CNF-02]
- severity: editorial

Verified that [R-CNT-05] says exactly what is quoted — 'a longer gap is conforming, and no conforming commit produces one' — so a 128-byte pre-trailer pad is a conforming file emitted by a writer violating [R-LIF-02] step 5. But this is not the unaccounted case the reporter takes it for: [R-CNF-02]'s second half defines the category — 'A writer obligation whose violation this specification expressly declares not to be a file-conformance violation ... binds the actor in the same way' — and [R-CNT-05] makes exactly that express declaration. The defect is only that §2.3 illustrates the category with §6.3's flags = 0 alone, leaving this second member unlisted. Not byte-level, as the reporter says: F9 registers a *structure* in the gap, not an over-long gap, and both verifiers certify.

### deflate-final-byte-residual-bits — PARTIAL

- merged: `adversary:RD-10`
- location: §17.2 [R-COD-05], [R-COD-08]; §22.3 [R-SEC-04]
- severity: editorial

The observation is factually right — a raw RFC 1951 stream ends on a bit boundary, [R-COD-08] speaks of 'no trailing bytes past the stream, frame, or block', and up to seven high bits of the final byte sit inside a checksummed live structure constrained by nothing. As a security note it has some force: unlike slack, these bits ride inside a structure the coverage walk claims and a checksum covers, so §22.3's 'Two residues are stated rather than defended' arguably undercounts. But it is not a specification defect in the ordinary sense: it is encoder freedom of exactly the kind [R-CNF-05] licenses and Appendix G closes by pinning the encoder at a named version. Not byte-level: only one reading exists, both files decode identically to the same reference array, and both are conforming.

### generation-counter-saturation — CONFIRMED

- merged: `adversary:RD-11`
- location: §6.2 trailer table; §9.2 [R-LIF-02] step 5; §9.3 [R-LIF-03]
- severity: editorial

Verified as stated and unstated. The trailer table gives '1 ≤ generation ≤ 2⁶³ − 1 ([R-ENC-03])' and [R-LIF-03] requires generation 'increasing by exactly 1 per commit', so a file at 2⁶³ − 1 admits no further commit; the document nowhere names this terminal condition or directs a writer to compact (§20.5 presents compaction purely as slack reclamation). Not byte-level, and fully decided in behavior: a trailer carrying 2⁶³ fails [R-CNT-06]'s generation gate at open in every reader. Unreachable in practice, so editorial at most.

### vec04-sibling-disjunct-wrong-for-reject-layer — CONFIRMED

- merged: `adversary:RD-12`
- location: §24 [R-VEC-04]
- severity: register-bookkeeping

Verified. [R-VEC-04] requires 'an intact sibling — another layer, or another tile of the same layer — whose decoded content the manifest records', and gives the reason: 'Without the sibling a vector cannot distinguish a reader that scopes its refusal from one that rejects the file entire.' For a reject-layer vector the second disjunct is inside the rejected layer and is therefore unserveable, so it cannot discharge the stated purpose — a corpus builder taking the disjunction literally produces exactly the vector [R-VEC-04] exists to prevent. The disjunct is correct only for reject-tile. Not byte-level: this constrains corpus construction, not any file's verdict.

### metadata-encoding-table-cell-valid-values — REFUTED

- merged: `diagrams:DG-02`
- location: §18.2 layout table; §21.6; §7.1 [R-CNT-25]; §10.3 [R-EXT-03]
- severity: none

The reporter missed the cell's own text. §18.2's Valid values cell does not read '1 or 2' — it reads '1 or 2; see below', and the prose immediately below assigns the full space: '0 is invalid; 1 = none and 2 = zstd are assigned; 3 through 0x7F are reserved; values ≥ 0x80 are the experimental range'. The cell is expressly non-exhaustive by its own terms, so there is no contradiction with §21.6's row for an experimental-range encoding, and the reporter's reading 1 (cell-as-normative-value-set) is not available. Their own analysis then correctly notes that [R-CNT-25] ('an unimplemented or invalid encoding' → ignore-record 'notwithstanding the owning-scope mapping of [R-CNF-08]') and [R-EXT-03] ('never a scope-level rejection') would foreclose it anyway. Not byte-level and not a defect.

### s15.4-example-fails-at-entry-count-zero — CONFIRMED

- merged: `diagrams:DG-03`
- location: §15.4 second worked example; [R-CNT-17]; [R-CNT-23]; [R-GEO-02]
- severity: editorial

Verified. §15.4's example asserts 'A layer with entry_count ≤ 65,536 has one segment and a 4-byte array', which is false at entry_count = 0: ⌈0/2¹⁶⌉ = 0 segments and a zero-byte array, [R-CNT-17] makes extent_length 0 ('and 0 when entry_count is 0'), §7.4 gives extent slot (0, 0), [R-CNT-23] forces crc_of_crc_array = 0, and there is no region to fetch and no CRC to verify. Since [R-GEO-02] makes the zero-extent layer a first-class case that 'Readers MUST accept', the example's range claim is wrong at its own boundary. Not byte-level: the example sits in an Example block (non-normative under [R-CNF-01]) and the normative formulas compute a unique answer; the alternative file the reporter names is L23/L28 reject-layer.

### s5.1-caption-re-emission-claim — PARTIAL

- merged: `diagrams:DG-04`
- location: §5.1 'a file after three commits' example; §20.3 [R-WRT-04] step 4
- severity: figure

Half confirmed. The sentence does read 'only the directory, the pad and the trailer are re-emitted per commit', which as a general claim is false — §20.3 step 4 requires 'Every layer whose stored-tile set, index content, or index placement this commit changes has its tile-index region re-emitted in full', and §20.3's own note prices it at ~20 MB for a 10⁶-tile layer. But the sentence is scoped by its own subject in the preceding clause, 'Layer A's tiles and index have never moved', and by the trailing 'a layer the commit does not touch keeps its extent slot pointing where it always pointed', so read in place it describes this figure rather than commits generally. It also sits inside an Example block, non-normative under [R-CNF-01]. Not byte-level: a writer misled by it produces a well-formed file whose new payload is unreferenced slack — §21.7's 'incorrectness of content' class.

### s5.1-figure-brace-alignment — CONFIRMED

- merged: `diagrams:DG-06`
- location: §5.1 box figure brace line; §20.3 shape (a) brace label
- severity: figure

Verified by counting columns in the source. In §5.1 the cell '  layer A  ' spans columns 9–19 with its separator at 20, while '└tiles+index┘' runs 9–21 — the closing corner lands at 21, the first ▓ column of the adjacent slack run. The second brace repeats it exactly (cell 29–39, brace 29–41). The '└──── re-emitted ────┘' brace closes at column 70 while the box's right border is at 69. All three overhang. §20.3(a)'s braces, by contrast, close on the separator bars and are fine; there the defect is only the label, since the run the '└ was dir₁ ──┘' brace spans is dir₁ *plus* the pad and tr₁. Not byte-level: the figure is captioned 'Regions, not offsets' and disclaims contiguity and ordering by citing [R-SLB-05].
