# Cleanroom round 7 — triage pass: skeptic

Distinct defects: **44**. Byte-level: **0**.

**Coverage check.** All 63 input findings appear in exactly one judgement, and none was dropped. Tally by role: reader RD-01…RD-08 (8), writer WR-01…WR-11 (11), verifier RD-01…RD-11 (11), diagrams DG-01…DG-09 (9), register RD-01…RD-12 (12), adversary RD-01…RD-12 (12) = 63. Sum of finding_ids across the 44 judgements = 5+1+4+4+3+1+2+1+1+1+2+1+2+1+1+1+1+1+1+1+1+2+1+1+1+1+1+1+1+2+2+1+1+1+1+1+1+1+1+1+1+1+1+1 = 63. Six multi-report merges: the [R-MTA-07] missing-row defect (5 reports), the §2.3 parenthetical (4), §21.7-is-not-an-inventory (4), the unchecksummed unknown-record extent (3), Appendix A's suffix-window sentence (2), §19's under-inclusive enumerations (2), the §20.4 MU=1 row (2), verdict priority (2), F5/L3 (2), instance arithmetic (2). writer:WR-11 is carried as its own judgement even though its author states it is not a defect claim; it is judged REFUTED as a defect, not dropped.

## Judgements

### mta07-scope-violation-missing-register-row — CONFIRMED

- merged: `reader:RD-03`, `writer:WR-04`, `verifier:RD-01`, `register:RD-02`, `adversary:RD-03`
- location: §18.4 [R-MTA-07]; §21.2–§21.5 (no row); §21.1 completeness clause; §2.4 [R-CNF-07]
- severity: register-bookkeeping

Verified: [R-MTA-07] states flatly that a file carrying a standardized key outside its listed scope 'is nonconforming, and a verifier detects it', and no row of §21.2–§21.5 registers it, nor does §21.6 list it as a non-violation. §21.1 makes that omission 'a defect in this document'. A second real facet: [R-CNF-07] requires every detectable violation to carry exactly one of four reader outcomes, and none of them fits — the reader ignores the *key*, not the record, so ignore-record is wrong. NOT byte-level: verifier:RD-01's reading 1 (register authoritative, so the file is conforming and must be accepted) is unavailable — §21.1's own sentence says a missing row is a defect in the document, which is a statement about the register, not a licence to certify, and [R-MTA-07]'s 'is nonconforming' is unqualified. Both verifiers therefore refuse to certify a layer-scope document carrying `tarn.created`, and both readers ignore the key. The cost is a missing row and a missing [R-ERR-02] vector.

### mta07-value-shape-no-writer-prohibition — PARTIAL

- merged: `verifier:RD-02`
- location: §18.4 table and [R-MTA-07]
- severity: editorial

Narrower than reported. [R-MTA-07] does tell a reader to ignore 'a standardized key ... whose value does not match the shape its row gives', while the sentence that makes a file nonconforming is deliberately restricted to 'outside its listed scope'. The reporter's reading 2 (the table's Value column is normative on writers) is unsupported: §18.4 has no analogue of §7.4's 'Writers MUST NOT emit a field violating a constraint in the table above', its lead calls every key 'OPTIONAL and advisory', and §2.1's phrasing Note requires a requirement to name its actor — the Value cells name none. So `{"tarn.title":42}` is a conforming file under the only supported reading; no verifier fork, no accept/reject fork. The real (small) defect is the inverse of §2.1's discipline: a reader-side clause with no paired writer-side prohibition.

### cnf03-parenthetical-miscount — CONFIRMED

- merged: `reader:RD-04`, `writer:WR-09`, `verifier:RD-06`, `register:RD-03`
- location: §2.3 [R-CNF-03]; §21.6 closing paragraphs; §21.9 [R-ERR-04]
- severity: editorial

Verified: §2.3 attaches three restrictive qualifiers to the acceptance duty (implemented major; no unimplemented MU=1 type; no value above §21's guarantees) and then says '(§21.6's closing paragraph names those two exceptions)' immediately after the third. §21.6's closing names only the unimplemented major and the experimental-range MU=1 type, and never the resource case. So the pointer is both misplaced and §21.6's 'Two distinct cases' is itself under-inclusive — a resource decline under [R-ERR-04] is a third. NOT byte-level: each ground is independently and unambiguously stated ([R-CNT-07] in §6.3, [R-CNT-15] in §7.2, [R-ERR-04] in §21.9), so no reader's accept/reject on any byte sequence turns on repairing the cross-reference.

### sec-21-7-not-the-inventory-it-is-called — CONFIRMED

- merged: `reader:RD-08`, `writer:WR-08`, `verifier:RD-09`, `adversary:RD-09`
- location: §21.1 ('§21.7 the inventory of what fails it'); §21.7 [R-ERR-01] second paragraph
- severity: editorial

Verified: §21.1 enrols §21.7 as 'the inventory' of obligations failing the detectability gate; §21.7's second paragraph names only [R-LIF-01], [R-LIF-03], [R-GEO-06], [R-SER-01] and [R-CNT-13]'s no-embedded-offsets rule. Since [R-LIF-01]/[R-LIF-03] show the class includes actor obligations, the omission of the §20 updater/compactor family ([R-WRT-05]–[R-WRT-09]), [R-CNT-08]'s copy-forward clause, [R-LIF-02]/[R-LIF-04]/[R-LIF-06]/[R-LIF-07] and [R-PRV-01] is a real gap between what §21.1 promises and what §21.7 delivers. (writer:WR-08's [R-IDX-01] example is the weakest member — §15.1 states it definitionally rather than as a MUST — but [R-CNT-08]'s updater clause is squarely in the class.) NOT byte-level: every omitted item is either multi-generation or actor-conduct, so no single byte sequence's status moves under either reading of how exhaustive §21.7 is.

### unknown-record-extent-covered-by-no-checksum — CONFIRMED

- merged: `verifier:RD-04`, `diagrams:DG-01`, `adversary:RD-05`
- location: §8.1 [R-CNT-19] and coverage map; §5.2 [R-CNT-02]; §9.7 [R-LIF-08]
- severity: editorial

Verified: §5.2 makes 'a record extent (the bytes any record's extent slot references, whatever the record's type)' a structure of the live committed state; §8.1's map has rows only for tile-index regions and user-metadata extents. An experimental-range MU=0 record with a nonzero extent therefore has a live-state structure covered by no checksum, contradicting [R-CNT-19]'s 'Every field of every structure ... as this map states' and leaving §9.7's 'each verifies against the checksum covering it' with nothing to perform. NOT byte-level: the strict reading (such a file violates [R-CNT-19]) is refuted by §7.2 (the extent slot is an MU=0 record's sanctioned outside reference precisely so a compactor can relocate it unparsed), §20.4/§20.5 (which describe relocating exactly such an extent), and §21.6's row making an experimental MU=0 type conforming. Both verifiers certify; no reader ever fetches the extent. The residue adversary:RD-05 names — corruption inside such an extent is undetectable and §22.3's 'Two residues' does not count it — is a real but non-byte-level omission.

### f31-l50-scope-collision — CONFIRMED

- merged: `register:RD-01`
- location: §21.2 row F31; §21.3 row L50; §7.3 [R-CNT-22]
- severity: register-bookkeeping

Verified: type 0x0001 (layer) is a registered type and layer records are top-level records, so F31's condition ('A top-level record of a type §7.3 registers carries a stored MU or PE bit differing from the registry') literally claims layer records, which sit under §21.2's blanket 'Outcome: reject-file' — while L50 claims the same file for reject-layer. §21.1's specialization list (F2/F8/F10, F38/F39, L25/L26) does not name this pair. NOT byte-level: [R-CNT-22] fixes the scope ('a validity error at the record's governing scope') and §7.2 makes that the layer for a layer record, so §21.1's 'the rule governs' decides it with no implementation guessing; detector is verifier on both rows, the verdict is nonconforming either way, and [R-CNT-22] obliges every reader to apply the fixed semantics regardless. This is exactly the row-contradicts-rule class the calibration flags as not byte-level.

### sec19-tier-enumerations-under-inclusive — CONFIRMED

- merged: `reader:RD-01`, `diagrams:DG-05`
- location: §19.1 step 4 [R-RDR-01]; §19.3 [R-RDR-03]; §21.2 F24/F25/F26; §21.3 L5/L11/L12/L13
- severity: editorial

Verified: §19 says it 'consolidates the reader's normative path', but §19.1 step 4 cites only [R-CNT-12], [R-CNT-15], [R-CNT-14], [R-CNT-13] and [R-ENC-12], while F24/F25/F26 ([R-CNT-25], [R-MTA-03]) are reject-file rows with Detected = open; and §19.3 lists [R-ENC-12]/[R-ENC-15] for dimension and channel names but omits [R-ENC-11], whose L5 is a layer-access row, as well as L11/L12/L13. NOT byte-level: DG-05 has this right and reader:RD-01 over-claims. §19.1 is silent, not contrary — 'all decidable from the resident bytes and F' describes the listed items, it does not close the list — and §19.2's first tier bullet ('at open: ... the directory region and its record walk') together with each row's own Detected cell and [R-CNF-04] already oblige detection at open. A reader that opens and serves the layer despite an inline_length of 2 on a top-level user-metadata record is nonconforming under rules already written, so no two conforming readers diverge.

### oversized-metadata-document-decline — REFUTED

- merged: `reader:RD-07`
- location: §18.2 [R-MTA-09]; §21.9 [R-ERR-04]; §2.3 [R-CNF-03]
- severity: none

The reporter's reading 1 — that a reader MUST accept a conforming file whose user-metadata document exceeds the reader's bound — is refuted by [R-CNF-03] itself, which they quote: the acceptance duty runs only to a conforming file 'none of whose values exceeds the minimum guarantees of §21's limits table'. §21.9's table lists 'decoded size of one user-metadata document | 16 MiB', so a 20 MiB document puts the file outside the must-accept set before [R-ERR-04] is even reached; [R-ERR-04] then expressly permits declining 'at the whole file'. [R-MTA-09]'s ignore-record assignment fixes what happens to the document for a reader that proceeds; it creates no acceptance obligation. Both behaviours are licensed on purpose, so there is no undecided question and no byte-level divergence.

### cnf04-detect-every-register-row — PARTIAL

- merged: `reader:RD-02`
- location: §2.3 [R-CNF-04]; §19.2 [R-RDR-02]; §21.1; §6.2 [R-CNT-05]
- severity: editorial

Real but narrower than 'roughly twenty rows'. [R-CNF-04]'s bare sentence ('A reader MUST detect the violations enumerated in the error register (§21)') is over-broad as written, and three passages qualify it explicitly: §19.2 ('a violation whose assigned detector is the verifier ... imposes no reader obligation'), §21.1 ('For a row whose Detector is verifier, the outcome names the scope at which the damage is recorded, not an obligation on any reader'), and §6.2 ('readers check neither'). The delegating reading is therefore the only sustainable one and the defect is a missing qualifier in one sentence, not a genuine fork. NOT byte-level, and the reporter agrees: [R-CNF-12] already lets any reader reject any nonconforming file, and [R-SER-08] fixes what a non-detecting reader returns for the one byte where returned content could differ.

### layer-scope-failure-mid-request — PARTIAL

- merged: `reader:RD-06`
- location: §19.4 step 8 [R-RDR-04]; §2.4 reject-layer row; §15.4 [R-IDX-04]
- severity: editorial

Something is there: §19.4 step 8 addresses only entry-bounded (tile-scope) failures inside a multi-entry request, and says nothing about a step-3 index-chain failure, which [R-IDX-04] makes reject-layer. But §2.4's reject-layer row supplies the substantive answer — the outcome 'is prospective: it bars further service from the layer, and does not retroactively invalidate content already returned' — and [R-CNF-09] forbids returning further data from the rejected layer. What is left is only how much a streaming reader had already delivered, which §2.4 deliberately leaves to the reader. NOT byte-level: only a corrupt (hence nonconforming) file exercises the condition, and [R-CNF-12] already lets any reader reject the whole file.

### appendix-a-suffix-window-reaches-offset-zero — CONFIRMED

- merged: `verifier:RD-11`, `diagrams:DG-07`
- location: Appendix A, closing paragraph
- severity: editorial

Verified as a plain factual error: Appendix A says '... whenever it speculates a suffix window, since this file is 128 bytes and any such window reaches offset 0.' Only a window of at least 128 bytes reaches offset 0. DG-07 sharpens it correctly — a 112-byte window over [16, 128) already contains the directory, so §6.4's containment test is satisfied and request 2 is unnecessary, yet bytes [0, 16) stay non-resident and [R-CNT-04]'s check remains optional. NOT byte-level: the appendix is identified as non-normative ([R-CNF-01] excludes it), and §6.1 states the residency test correctly, with F8's condition cell recording the same conditionality.

### front-block-residency-in-19-1-step-1 — REFUTED

- merged: `reader:RD-05`
- location: §19.1 step 1 [R-RDR-01]; §6.1 [R-CNT-04]
- severity: none

The claimed inversion does not exist. §19.1 step 1's own text says 'a remote reader's suffix range for step 2 carries F in its own response, so steps 1 and 2 cost one request between them (§6.4)' — the speculative suffix fetch *is* the fetch that completes step 1. A reader whose window reached offset 0 therefore holds bytes [0, 16) 'once this step completes' and is bound by the MUST, exactly as §6.1 says; and it issues no 'further range request', so the release clause cannot reach it either. §19.1 and §6.1 agree for every reader, so a reader following §19.1 alone reaches the same answer. No fork, no defect.

### wrt08-mu1-row-captures-layer-records — CONFIRMED

- merged: `writer:WR-01`, `adversary:RD-06`
- location: §20.4 [R-WRT-08] persistence table, MU = 1 row; §20.3 [R-WRT-04] step 4; §2.3 [R-CNF-06]
- severity: editorial

Verified drafting collision: §20.4's introducing sentence says 'Persistence governs every record type ... For a type §7.3 registers, the registry's fixed flags govern rather than the stored ones', and §7.3 fixes the layer record at MU = 1, PE = 1 — which routes the one record every appender modifies into a row whose first sentences are 'Retain byte-identical. The updater MUST NOT modify the scope the record governs.' Read literally that forbids every layer edit and makes §20.3, §9.2 and §20.5 unreachable. NOT byte-level: [R-CNF-06] scopes preservation to 'records it does not understand', [R-WRT-05] scopes byte-identical re-emission to records the updater 'does not logically modify', and the cell's own gloss says 'an unknown critical record'. The restrictive reading yields an updater that refuses to act, not one that emits different bytes; any generation g+1 file with a modified layer record and re-emitted index is conforming under both readings, since [R-CNF-02] makes conformance a pure predicate on bytes.

### live-directory-not-pinned-to-live-generation — PARTIAL

- merged: `writer:WR-02`
- location: §9.2 [R-LIF-02] step 3; §3.1 (definition of directory); §5.1 [R-CNT-01]; §5.2
- severity: editorial

The observation is right: no *file-level* requirement obliges the live trailer's dir_offset to point at a directory this generation appended, so the reporter's 192-byte construction satisfies [R-CNT-01], [R-CNT-02], [R-CNT-05], [R-CNT-06], [R-CNT-11], [R-CNT-27] and [R-LIF-08]. But the byte-level claim fails. Reading 1 (nonconforming) needs a file-level requirement to point at: §3.1's 'a file contains one directory per generation' sits in a Terms list, names no actor and states no MUST, and §5.1's enumeration is likewise descriptive — §2.1's Note says every requirement names its actor. And even granting reading 1, §9.7 walks the live state only and expressly does not reconstruct history, so no verifier procedure could detect it; both verifiers certify. The superseded trailer in the gap is not a §5.2 'structure' (§21.6 classes superseded structures as slack and §5.2 says 'no conformance requirement applies to it'), so F9 does not fire either. Meanwhile [R-LIF-02] step 3's 'append the new complete directory' is an unqualified sequenced MUST, so no conforming writer emits it. Conforming bytes plus nonconforming writer is exactly the shape [R-CNT-05] already models ('a longer gap is conforming, and no conforming commit produces one').

### compactor-flags-zero-vs-copy-forward — REFUTED

- merged: `writer:WR-03`
- location: §6.3 [R-CNT-08]; §20.5 [R-WRT-06]; §20.1 [R-WRT-01]
- severity: none

'Which governs a compactor is not stated' is false — it is stated twice. [R-WRT-06] says in terms 'The output trailer copies the input's unknown ignore-lane flag bits forward ([R-CNT-08])', and the clause it cites is [R-CNT-08]'s own 'An updater MUST copy forward unknown ignore-lane bits of the file it modifies and MUST NOT clear them'. §20.1 [R-WRT-01] places a compactor under [R-CNF-06], the conforming-updater rule, so the compactor is the actor that clause names. [R-CNT-08]'s 'a writer creating a file under this text' never had a competing claim on a file carrying a bit this text does not define. No conflict, no divergence — and the reporter concedes both trailers would be conforming in any case.

### extent-growth-called-metadata-only — CONFIRMED

- merged: `writer:WR-05`
- location: §11.1 Rationale; §13.3 'Note — sparse writing'; against §20.3 [R-WRT-04] step 4
- severity: editorial

Verified: §11.1's Rationale ('extent growth is a metadata-only operation under this specification's commit model') and §13.3's Note repeat it, while §20.3 step 4 lists 'grown extents' among the things that force a layer's whole tile-index region to be re-emitted, and [R-CNT-17] pins extent_length to entry_count. The claim holds only where growth changes no ⌈Eᵢ/Tᵢ⌉; where it does, entry_count changes, ordinals renumber ([R-GEO-06]) and the index is re-emitted in full. NOT byte-level: both sentences sit in Rationale/Note blocks that [R-CNF-01] makes non-normative, and a writer misled by them emits a file failing [R-CNT-17] — L22/L23, already registered and already reject-layer.

### index-relocation-for-otherwise-untouched-layer — PARTIAL

- merged: `writer:WR-06`
- location: §20.3 [R-WRT-04] step 4; §20.4 [R-WRT-05]
- severity: editorial

Narrower than 'not stated'. §20.3 step 4's trigger list — 'Every layer whose stored-tile set, index content, or index placement this commit changes' — presupposes that a commit may change index placement, and [R-WRT-05] conditions byte-identical re-emission on the record being one the updater 'does not logically modify', which a re-pointed extent slot is not. So relocation is contemplated and its consequence (full re-emission, old region becomes slack) is stated. What is genuinely absent is an affirmative permission sentence. NOT byte-level: both files are conforming — the relocated region is a live record extent, disjoint and checksum-consistent, and the superseded one is slack that [R-CNT-21] leaves unconstrained — so no reader or verifier verdict differs.

### coverage-walk-enumerates-layer-extent-twice — PARTIAL

- merged: `writer:WR-07`
- location: §9.7 [R-LIF-08]; §21.2 row F36; §7.4
- severity: editorial

Real imprecision, not a contradiction. §9.7 enumerates 'each record's extent, and each layer's tile-index region', and §7.4 makes those the same bytes for a layer record. But §5.2 defines a structure as 'a record extent (the bytes any record's extent slot references, whatever the record's type)' — one structure, reached under two names, not two claimants — and §8.1's map lists the tile-index region once, under its structural name. L19's instance cell ('stored-tile extents; tile-index region; layer sub-record extents', with no separate layer-record extent) confirms the dedup. The literal double-claim reading is self-refuting: it would make every file with entry_count > 0 fail [R-CNT-02]. NOT byte-level — no verifier can sustain the failing reading.

### layer-record-table-omits-taxonomy-class — PARTIAL

- merged: `writer:WR-10`
- location: §7.4 layout table; §4.7 [R-ENC-16] and its Note
- severity: editorial

One of three sub-claims survives. [R-ENC-16] is normative and says 'Every field this specification defines is classified structural, semantic, or informative'; §7.4's table gives only Field/Type/Constraint, while §6.1, §6.2, §7.2, §15.1 and §18.2 all carry a Class column — so §7.4's fields are unclassified, a real gap. The byte-offset complaint is refuted twice over: the rubric the finding quotes is §4.7's *Note* (non-normative under [R-CNF-01]), not §1's, and the layer record's inline payload is variable-length, so per-field byte offsets are not expressible. 'No field is classified informative' is an observation, not a defect — a defined class with no format-major-1 instance costs nothing. NOT byte-level: every §7.4 field's decoding role is fixed by the rules that use it.

### licensed-writer-divergence-catalogue — REFUTED

- merged: `writer:WR-11`
- location: whole document (catalogue deliverable)
- severity: none

Not a defect claim, by its author's own statement: every entry is a divergence the document deliberately licenses under [R-CNF-05] ('two conforming writers given identical input MAY produce different conforming files'), so both outputs are conforming and every reader and verifier reaches the same verdict on each. Nothing here is a finding against the specification. Its two byte-moving candidates are broken out and judged separately as writer:WR-02 and writer:WR-06.

### slab-continuity-across-a-rejected-entry — REFUTED

- merged: `verifier:RD-03`
- location: §15.3 [R-IDX-03]; §16.2 [R-SLB-03]; §21.3 L42
- severity: none

§15.3 decides it in the sentence the reporter quotes: an entry these rows classify reject-tile 'contributes no stored extent to the *verifier* rows, which bind over well-formed entries' extents only'. L42's predicate therefore ranges over the well-formed stored extents of the run, so entry 2's 'previous stored tile' is entry 0 and the 500-byte gap breaks packing — reading 1, and only reading 1. Reading 2 has no textual anchor: §16.2's transparency is granted to sentinels for a stated reason that does not transfer ('they occupy no bytes and do not break packing'), whereas a malformed entry nominally addresses bytes, which §15.3 sends to [R-LIF-08]'s slack total rather than to the continuity relation. With one permitted reading there is no fork and no byte-level divergence.

### verdict-priority-nonconforming-vs-cannot-establish — CONFIRMED

- merged: `verifier:RD-05`, `adversary:RD-04`
- location: §2.3 [R-CNF-11]; §18.2 [R-MTA-09]; §17.4 [R-COD-11]
- severity: editorial

Verified gap: [R-CNF-11] defines three verdicts and states no priority, while [R-MTA-09] phrases its obligation as a whole-file report — 'it MUST report that it cannot establish the file's conformance rather than that the file is nonconforming' — so a verifier that both declines an oversized document and finds an established violation (say codec = 0, an L44) has two candidate verdicts and the text picks neither. The 'stop at the first violation' licence makes the verdict a function of traversal order the specification never fixes. NOT byte-level: both verdicts bar certification ('a verifier MUST NOT certify a file it reports that way'), and [R-CNF-12]'s reader licence is triggered by the detected violation itself, present under either verdict. No byte sequence's accept/reject status moves; the divergence is in the operator's diagnostic.

### slack-total-under-early-stop — PARTIAL

- merged: `verifier:RD-07`
- location: §5.2 [R-CNT-21]; §2.3 [R-CNF-11]
- severity: editorial

A thin residue, not the open question reported. [R-CNT-21] states the MUST unconditionally and supplies the escape in the same sentence ('the verifier MUST report the total as partial and name the regions it could not walk'), and [R-CNF-11] supplies *unexamined* for skipped scopes — so a verifier that stops early reports a partial total and names what it skipped. What is genuinely unstated is only whether a *voluntary* stop counts as 'a scope-level rejection stops the walk', which is the clause's stated trigger. NOT byte-level: §5.2 says slack's 'content is unconstrained, and no conformance requirement applies to it', so the total is report content and no file's validity or reader behaviour turns on it.

### recovery-probe-has-no-stated-verifier-consequence — PARTIAL

- merged: `verifier:RD-08`
- location: §9.6 [R-LIF-06]; §9.7 [R-LIF-08]
- severity: editorial

Small loose end, correctly identified but over-stated. §9.6 names verifiers as running the backward probe and never says what a verifier does with the result; §9.7 supplies one negative consequence ('A recovery tool enumerating a file's commit states continues the same probe to offset 0; coverage verification does not') and nothing positive. NOT byte-level, and the reporter concedes it: reading 2 (certify the recovered prefix) is foreclosed by §2.3's pure-predicate-on-bytes rule, by F10/F19 on the bytes actually handed to the verifier, and by §9.6's own requirement that 'recovery output MUST be re-verified as a whole file' — which makes the truncated prefix a different artifact. One permitted reading, so no divergence.

### cannot-establish-for-a-resource-decline-on-tiles — PARTIAL

- merged: `verifier:RD-10`
- location: §2.3 [R-CNF-11]; §17.4 [R-COD-11]; §21.9 [R-ERR-04]; §18.2 [R-MTA-09]
- severity: editorial

The observation checks out: §2.3 lists 'cannot execute a codec or filter' as a cannot-establish trigger, but [R-CNF-03] makes all four codecs and both filters mandatory for a conforming reader and [R-COD-11] routes reserved/experimental values to reject-layer (a nonconforming file, hence the *nonconforming* verdict), leaving the resource decline of [R-ERR-04] as the only live path — which §17.4 never labels, though §18.2 labels the exactly parallel document case. NOT byte-level: §21.9 says a file exceeding a guarantee 'remains conforming', all readings bar certification, and [R-ERR-04] requires the refusal to be reported as a resource limit and not a validity error under every reading. And [R-CNF-11]'s own definition ('where some requirement is one it is unable to check') already reaches a budget-limited verifier, so the gap is a missing cross-reference rather than a missing rule.

### metadata-encoding-valid-values-cell — REFUTED

- merged: `diagrams:DG-02`
- location: §18.2 layout table; §21.6 row; §10.3 [R-EXT-03]; §7.1 [R-CNT-25]
- severity: none

The contradiction dissolves on the cell's own text: §18.2's Valid values cell reads '1 or 2; **see below**', explicitly deferring to the prose that follows ('0 is invalid; 1 = none and 2 = zstd are assigned; 3 through 0x7F are reserved; values ≥ 0x80 are the experimental range'). Reading 1 requires discarding 'see below'. Unlike §7.4, §18.2 carries no 'Writers MUST NOT emit a field violating a constraint in the table above', and the register rows the finding points to for precedent (F13, F14, F17) all derive from §6.2's prose gate list rather than from a table cell. [R-CNT-25], [R-EXT-03] ('never a scope-level rejection') and §21.6 then fix encoding 0x80 as ignore-record on a conforming file. No permitted reading rejects the file; no fork.

### segments-example-fails-at-entry-count-zero — CONFIRMED

- merged: `diagrams:DG-03`
- location: §15.4 second worked Example
- severity: editorial

Verified: the Example says 'A layer with entry_count ≤ 65,536 has one segment and a 4-byte array', and entry_count = 0 is inside that range but has ⌈0/2¹⁶⌉ = 0 segments, a zero-byte array, extent slot (0, 0) per §7.4 and crc_of_crc_array = 0 per [R-CNT-23] — there is no region to fetch and no CRC to verify. §21.6 and [R-GEO-02] make the zero-extent layer a first-class case, so the range genuinely includes it. NOT byte-level: the sentence is inside an Example block ([R-CNF-01] non-normative), and [R-CNT-17]'s formula plus [R-CNT-23]'s 'crc_of_crc_array ... 0 when entry_count = 0' compute a unique answer that L23/L28 already enforce.

### three-commits-caption-commit-cost — PARTIAL

- merged: `diagrams:DG-04`
- location: §5.1 'a file after three commits' Example caption
- severity: editorial

Weaker than reported. The sentence is 'Layer A's tiles and index have never moved: only the directory, the pad and the trailer are re-emitted per commit, and a layer the commit does not touch keeps its extent slot pointing where it always pointed (§20.3, [R-WRT-05])' — bracketed by two clauses that scope it to untouched layers, and 're-emitted' is accurate for the depicted file (layer B's tiles and index were newly *emitted*, not re-emitted). Lifted out of those clauses the middle assertion is over-general against §20.3 step 4, which is the residual defect. NOT byte-level: it is an Example block, and a writer misled by it produces an index still pointing at the superseded payload — a well-formed file with wrong content, §21.7's undetectable class, not a divergence about which bytes must be accepted.

### section-5-1-figure-brace-misalignment — PARTIAL

- merged: `diagrams:DG-06`
- location: §5.1 'a file after three commits' figure; §20.3 shape (a)
- severity: figure

I measured the columns. In §5.1 the box separators sit at string indices 2, 10, 22, 30, 42, 50, 57, 62, 71 and the brace corners at 11, 23 / 31, 43 / 51, 72 — every brace is shifted exactly one column right of a separator-to-separator span, so each closing corner lands on the first ▓ column of the adjacent slack run and the third overruns the box's right border at 71. The misalignment is real, but it is a uniform one-column shift, not the 'two columns right' the finding states, and the opening corners sit correctly on their cells' first content column. The §20.3(a) half is refuted: I measured that figure too — 'untouched' spans 16–32 and 'was dir₁' spans 33–46, both closing exactly on their separators — and the label is a shorthand the very next sentence expands ('The slack is the old directory, pad and trailer'). NOT byte-level: the figure is captioned 'Regions, not offsets' and disclaims contiguity and ordering by citing [R-SLB-05].

### f5-l3-width-condition-has-no-isolable-witness — CONFIRMED

- merged: `diagrams:DG-08`, `register:RD-06`
- location: §21.2 row F5; §21.3 row L3; §4.2 [R-ENC-06]; §21.8 [R-ERR-02]
- severity: register-bookkeeping

Both facets verified. (a) F5's worked instance is unbuildable as written: [R-CNT-24] says 'The format-major-1 trailer has zero slack: every byte is assigned', so writing version_major and version_minor as u32 each adds four bytes and the condition's own 'with total size unchanged' cannot hold unless another field is deleted, which is a different violation. (b) More generally, with total size fixed a reader parses every structure at the widths this specification fixes and has no other layout available, so the bytes are either fully valid or caught by some other row's value gate — F5 and L3 name conditions with no distinguishable witness, contrary to §21.1's 'One instance is one *distinguishable* file' and [R-ERR-02]'s one-vector-per-instance duty. They belong with §21.7's inventory. NOT byte-level: no byte sequence can be classified differently on the strength of these rows.

### instance-arithmetic-applied-inconsistently — CONFIRMED

- merged: `diagrams:DG-09`, `register:RD-04`
- location: §21.1 Instances paragraph; F33; L1; L16; R5; §21.8
- severity: register-bookkeeping

Verified against the cells. §21.1 fixes the arithmetic as multiplicative — 'a condition applying to two alternatives in two containers has four' — and the register does not apply it uniformly: F33 states two alternatives in one container and enumerates the alternatives; L16 states the same [R-CNT-13] half-zero-slot condition with two alternatives in two containers and enumerates only the containers (2, not 4); R5's key-or-string-value alternatives collapse to two containers; L1's parenthetical folds two fields across two containers into two instances. §21.8's 242 matches the cells as written, so the cells were counted and the rule was not applied — which means the rule as stated yields a different corpus than the register does. NOT byte-level: this bears only on how many files a corpus builds; every affected condition has one unambiguous outcome from its governing rule, and §24 makes the corpus derivative.

### scope-of-section-21-1 — PARTIAL

- merged: `register:RD-05`
- location: §21.1 opening paragraph; §21.6; §21.7
- severity: editorial

A real scoping ambiguity with no identified consequence. §21.1 governs 'The register below', §21 contains four violation subsections plus §21.6, §21.7, §21.8 and §21.9, and §21.1 itself enrols §21.7 by role while §21.5's preamble cross-refers to §21.6 — so whether the completeness clause, the row-versus-rule tiebreak and the instance arithmetic reach §21.6 and §21.7 is never stated. NOT byte-level, and the reporter tested the right case: the register is not the sole statement for the experimental-encoding row, since [R-CNF-02] plus §10.3 plus [R-MTA-03] independently yield 'conforming'. Both readings of §21.1's scope land on identical emit/accept behaviour.

### t15-t16-t23-cite-rules-with-no-reader-clause — CONFIRMED

- merged: `register:RD-07`
- location: §21.4 rows T15, T16, T23; §17.2 [R-COD-05], [R-COD-07], [R-COD-08]
- severity: editorial

Verified: [R-COD-05] states only what the stored bytes are ('exactly one DEFLATE compressed data stream ... raw, not a zlib or gzip wrapper') with no reader clause, and [R-COD-07]'s only reader clause is about the *declaration* bound at layer scope, not about frame-versus-block. Yet T15, T16 and T23 assign detector 'reader' at 'tile use' and cite exactly those rules — so under §21.1's 'the rule governs' the cited rules impose no magic-based check, and the only reader path is [R-COD-08]. This breaks §2.1's stated discipline that every writer-side prohibition is paired with an explicit reader-side clause; contrast [R-COD-06], which spells the zstd magic check out. NOT byte-level: I checked the divergence is unreachable — an LZ4 block beginning `04 22 4D 18` has token 0x04 (zero literals) followed by match offset 0x4D22 at output position 0, which is malformed, so no conforming codec-4 payload starts with the frame magic; and any deflate file the disagreement could touch is nonconforming, where [R-CNF-12] licenses both behaviours.

### t13-duplicates-t25 — CONFIRMED

- merged: `register:RD-08`
- location: §21.4 rows T13 and T25; §17.1 [R-COD-02]; §17.2 [R-COD-08]
- severity: register-bookkeeping

Verified: T13's second instance ('lz4 block whose match offset reaches before its own output start') and T25's third ('lz4 match offset 0 or match reaching past produced output') name the same malformation, and T13's first instance (a deflate stream relying on a previous tile's history window) is likewise met by a reader only as a decode failure. [R-COD-02] states an independence property and supplies no detection procedure, so T13 has none of its own; both rows carry the same outcome, detector and detection point, and §21.1's specialization list does not name the pair. NOT byte-level: whichever row an implementation attributes the file to, it rejects the same tile under [R-COD-08]. The consequence is duplicate [R-ERR-02] vectors.

### r5-omits-unpaired-surrogate-escape — PARTIAL

- merged: `register:RD-10`
- location: §21.5 row R5; §18.2 [R-MTA-04] fourth bullet
- severity: register-bookkeeping

Real but narrower. [R-MTA-04] names two ways the UTF-8 requirement fails — 'a \uXXXX escape denoting an unpaired surrogate has no UTF-8 encoding ... as does an ill-formed byte sequence in the source' — and R5's condition text mentions only 'ill-formed UTF-8'. R5's wording arguably subsumes the escape case (the rule says 'including after escape resolution'), so the condition is covered; what is missing is the *alternative* in the Instances cell, so §21.8's one-vector-per-instance duty builds no escape vector — and the escape case falls under no other row, since such a document is well-formed JSON per RFC 8259 and so escapes R7. NOT byte-level: [R-MTA-04] states the consequence in the rule text and §7.1's quarantine fixes ignore-record with a SHOULD-report, so two implementations handle the bytes identically.

### l2-instances-not-distinguishable-files — CONFIRMED

- merged: `register:RD-11`
- location: §21.3 row L2; §21.1 distinguishability rule; §21.8
- severity: register-bookkeeping

I checked the arithmetic and two of L2's ten instances cannot be isolated, contrary to §21.1's 'One instance is one *distinguishable* file'. V = P·C cannot overflow without P·Q overflowing, because Q = ΣBᵢ over C channels with every Bᶜ ≥ 1, so Q ≥ C and P·Q ≥ P·C. And 'max disk ordinal (C−1)·N + (N−1)' equals C·N − 1, so it exceeds 2⁶³ − 1 only where C·N already does. Both are separately listed alongside the quantities that dominate them, so no file exercises either alone; the corpus gets two duplicates. NOT byte-level: [R-ENC-04] gives one outcome — a validity error at the owning scope — for every quantity in the cell, so a reader that overflow-checks its products behaves identically at eight instances or ten.

### limits-table-has-no-composition-rule — CONFIRMED

- merged: `register:RD-12`
- location: §21.9 [R-ERR-03], [R-ERR-04]; §2.5 [R-CNF-10]
- severity: editorial

Verified as stated: [R-ERR-03] says 'a conforming reader MUST accept any conforming file whose quantities lie within these bounds' and [R-CNF-10] repeats it, while [R-ERR-04]'s only escape is for a file 'exceeding any of these' — which a file combining 65,536 layers at 2³² addressed tiles each does not do, though its index regions alone run to petabytes. No composition rule exists. NOT byte-level, and the reporter tested the right thing: no such byte sequence can be produced or served, §24 already declines to build a vector even at the single-row tile-count bound ('the tile-count guarantee is not [constructible]'), and under either reading [R-ERR-04] requires any refusal to be 'reported as a resource limit and not as a validity error'. The two readings can never be distinguished by a file two implementations could both be handed.

### lz4-cap-vacuous-on-a-zero-tile-layer — REFUTED

- merged: `adversary:RD-01`
- location: §17.2 [R-COD-07]; §11.1 [R-GEO-02]; §21.3 L45; §21.6
- severity: none

Reading 2 is not available: [R-COD-07] and L45 quantify explicitly over 'a layer any of whose addressed tiles' decoded size exceeds 0x7E000000 bytes', and the reporter concedes that wording is unambiguous. §21.6 and [R-GEO-02] affirm the zero-addressed-tile layer as 'A valid, empty layer', and §19.3's inclusion of [R-COD-07] among layer-access checks obliges performing the check, not rewriting its quantifier. So verifier B's verdict requires ignoring the rule's own words, and there is no fork on the 128+N byte file. The offered second instance refutes itself: [R-ENC-04] carries no addressed-tile quantifier — it binds 'any quantity this specification defines as a sum or product of integers obtained from a file' — and [R-GEO-03] and [R-SER-02] declare P, P·Q and P·Bᶜ declaration-derived, so the T₀ = 2⁶² construction is reject-layer under both readings, not vacuous.

### encoding-2-occupancy-has-no-register-row — PARTIAL

- merged: `adversary:RD-02`
- location: §18.2 [R-MTA-09]; §21.5 rows R3, R4
- severity: register-bookkeeping

The ambiguity is refuted; a narrower defect is confirmed. Occupancy is in [R-MTA-09]'s operative main clause — 'Encoding 2 stores it as exactly one RFC 8878 compressed frame **occupying the extent's bytes before its terminal CRC**' — and the subordinate 'under the frame constraints of [R-COD-06] that do not reference a tile: ...' enumerates *additional* carried-over constraints, not a replacement for the main clause. Reading 2 requires demoting the main clause to scenery. So the extent `[zstd frame for {}][00 00][CRC]` violates a stated file-level requirement and [R-MTA-09]'s catch-all 'Any violation here is ignore-record' assigns the outcome — both verifiers report nonconforming, both readers ignore the record, no fork. What is confirmed is that §21.5 has no row for it: R3 is a decode failure and R4's ten instances are exactly the four enumerated frame constraints across two containers, none of them occupancy. Under §21.1 that omission is a defect in the document — the same shape as the [R-MTA-07] gap.

### layer-name-parse-tier-versus-framing-tier — PARTIAL

- merged: `adversary:RD-07`
- location: §19.1 step 4 [R-RDR-01]; §7.4 [R-CNT-18]; §21.3 L4/L6/L7 versus L24
- severity: editorial

The constructed fork fails, but a real tier seam remains. Reading 2 requires a reader to obtain five declared name bytes from a three-byte payload, i.e. to read past inline_length into the next record's header — an operation §7.2's framing and [R-CNT-18]'s 'MUST lie entirely within the inline payload' do not define, and §19.1 step 4 parses names inside records already parsed 'under §7.2's framing'. So order 1 governs and no reader legitimately reports F6. What is genuinely unstated is the seam the register itself exposes: L4/L6/L7 (layer-name validity) carry Detected = open while L24 (inline-payload framing) carries Detected = layer access, so a reader must parse a name at open from a structure whose framing check is nominally due later. §19.2's 'A reader MAY detect any violation earlier' supplies the answer. NOT byte-level: the file is nonconforming under either order and [R-CNF-12] licenses whole-file rejection regardless.

### pretrailer-pad-length-conduct-carve-out — REFUTED

- merged: `adversary:RD-08`
- location: §6.2 [R-CNT-05]; §9.2 [R-LIF-02] step 5; §2.3 [R-CNF-02]
- severity: none

§2.3 does cover it. [R-CNF-02]'s second sentence defines a general class — 'A writer obligation whose violation this specification expressly declares not to be a file-conformance violation' — and the em-dashed '§6.3's flags = 0 against a set ignore-lane bit' is an illustration of that class, not a closed list (the earlier conduct-rule clause is the one that cites §10.3 and §18.3 exhaustively). [R-CNT-05]'s 'a longer gap is conforming, and no conforming commit produces one' is precisely such an express declaration, so [R-LIF-02] step 5 binds the actor in exactly the way [R-CNF-02] describes. Nothing is left open, and both verifiers certify the 128-byte-pad file.

### deflate-final-byte-residual-bits — REFUTED

- merged: `adversary:RD-10`
- location: §17.2 [R-COD-05], [R-COD-08]; §22.3 [R-SEC-04]
- severity: none

Factually correct and not a defect. [R-COD-08]'s exactness rule speaks of 'trailing bytes past the stream, frame, or block', and no whole byte trails a stream ending within its last byte, so both decoders produce the same tile image and both verifiers accept. Two files differing only in those bits are both conforming with identical reference arrays — which is ordinary encoder freedom that [R-CNF-05] licenses in terms ('two conforming writers given identical input MAY produce different conforming files') and Appendix G closes for reproducibility by pinning the encoder. Every compressing codec carries the same latitude in its coding choices; §21.7 already states the general principle that this format detects corruption of structure, not incorrectness of content. Nothing about §22.3's residues needs to change.

### generation-counter-saturation — REFUTED

- merged: `adversary:RD-11`
- location: §6.2 trailer table; §9.2 [R-LIF-02] step 5; §9.3 [R-LIF-03]
- severity: none

Nothing is underdetermined — the reporter says so themselves ('Fully decided, just unstated'). A trailer carrying generation 2⁶³ fails [R-CNT-06]'s '1 ≤ generation ≤ 2⁶³ − 1' gate at open in every reader, [R-LIF-02] step 5 forbids a commit that does not increment, and §20.5 supplies the only conforming continuation (a fresh file_id at generation 1). Every actor's behaviour at the bound is fixed by rules already written; a specification is not defective for declining to narrate a state 2⁶³ commits away. No implementation could disagree about any byte.

### vec04-intact-sibling-disjunct — CONFIRMED

- merged: `adversary:RD-12`
- location: §24 [R-VEC-04]
- severity: editorial

Verified: [R-VEC-04] states one disjunction for two outcome classes — 'an intact sibling — another layer, or another tile of the same layer' — and gives the reason it exists ('Without the sibling a vector cannot distinguish a reader that scopes its refusal from one that rejects the file entire'). For a reject-layer vector the second disjunct cannot serve that reason, since every tile of the rejected layer is unusable, so a corpus builder taking the disjunction literally produces a vector that fails the very discrimination the rule was written to guarantee. NOT byte-level: this constrains corpus construction only; no file's verdict and no implementation's accept/reject behaviour changes.
