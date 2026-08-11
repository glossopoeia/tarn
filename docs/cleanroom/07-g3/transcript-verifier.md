# Cleanroom round 7 — verifier walk

**Access disclosure.** spec/tarn.md only — plus one local computation I ran in Python (no files read): CRC-32C of "123456789", of zero bytes, of a 2^16-entry all-sentinel segment, and of Appendix A's trailer bytes [0,60). All four reproduce the document's stated constants exactly (E3069283, 00000000, EECB3BB2, E00938D2).

## Walk summary

I implemented the certification procedure on paper in this order: (1) physical size F ≥ 128 and F mod 64 = 0; (2) front block [0,16) by equality — unconditionally, since §2.3 strips a verifier of `[R-CNT-04]`'s residency exemption; (3) trailer magic, trailer CRC, version gate, then flag lanes, committed_file_length = physical size, dir_offset ≥ 16, dir_length ≥ 4, dir_offset+dir_length ≤ F−64, 1 ≤ generation ≤ 2^63−1, file_id ≠ 0, reserved zero; (4) directory CRC over dir_length−4, then the record walk (framing, no residue, type ≠ 0, reserved flag bits, MU/PE against §7.3, reserved-range types, multiplicity, extent slots); (5) per layer, the whole §19.3 set plus `[R-CNT-16]`/`[R-CNT-17]`; (6) per layer, crc_of_crc_array → segment CRCs → entries, classifying each by §15.3; (7) per stored tile, entry CRC, codec/frame constraints, exact decode to the declared decoded size, then the decoded-content obligations; (8) whole-file predicates: overlap, alignment, slab, the pre-trailer-pad gap, coverage, slack total.

The three verifier-only geometric predicates are decidable as stated. Overlap: build the claimant list (front block, directory, trailer, each record extent, each layer's index region, each well-formed non-sentinel entry's extent), require pairwise disjointness, each claimant inside [16, F−64), and no claimant intersecting [dir_end, F−64) (F9); same-layer collisions record reject-layer, everything else reject-file. Alignment: for every well-formed stored entry, offset mod A = 0. Slab: partition [0,N) (or each [cN,(c+1)N)) into runs of S; within a run the well-formed stored extents must satisfy offset_i = offset_{i−1} + length_{i−1}, and offset_0 mod A_slab = 0.

Coverage walk on Appendix A: claimants are [0,16), [16,20), [64,128); slack = [20,64) = **44 bytes**, matching §5.1's example.

Decoded content: a verifier must decode every stored tile (§14.5 padding and pad bits, §14.2 interleaved bool bytes, `[R-COD-08]` exactness) and every user-metadata document; it may decline only where it cannot execute a codec/filter or exceeds its self-chosen document bound (≥16 MiB), each yielding *cannot establish*.

Requirements a verifier cannot decide from one file: `[R-LIF-01]`, `[R-LIF-02]`, `[R-LIF-03]`, `[R-LIF-04]`, `[R-LIF-06]`, `[R-LIF-07]` (history/protocol); `[R-WRT-03]`–`[R-WRT-09]` (updater/compactor conduct, including the fresh file_id and byte-identical re-emission); `[R-SLB-04]` (only via `[R-SLB-03]`); `[R-GEO-06]`/`[R-SER-01]` ordinal mappings; `[R-CNT-13]`'s no-embedded-offsets rule; `[R-COD-10]` at a stride with no structural witness; `[R-COD-06]`'s undisclosed dictionary; `[R-CNT-08]`'s updater copy-forward; the conduct rules of §10.3, §18.3, `[R-CNT-26]`; and all §23 privacy obligations.

## Could not decide from the text

- Whether a verifier that declines a stored tile on resource grounds (decoded size or zstd window above its budget) reports *cannot establish*, a bare resource-limit refusal, or must decode regardless — §18.2 answers this for user-metadata documents and §17.4 answers nothing for tiles (see RD-10).
- Whether a standardized user-metadata key whose value does not match §18.4's stated shape is a file-conformance violation at all; the document states the scope rule's consequence and is silent on the shape rule's (see RD-02).
- Which of *nonconforming* and *cannot establish* a verifier reports when both apply to the same file (see RD-05).
- What checksum, if any, a verifier is to apply to an unknown or experimental record type's extent during §9.7's walk; §8.1's map has no row for that structure class (see RD-04).
- What a verifier is to do with the result of §9.6's backward probe, which §9.6 expressly authorises verifiers to run without stating any consequence for the verdict (see RD-08).

## Findings (11)

### RD-01 — CONTRADICTION  · reporter flags BYTE-LEVEL

**Location.** §18.4 `[R-MTA-07]`; §2.4 `[R-CNF-07]`; §21.1; §21.2–§21.5; Appendix H

`[R-MTA-07]` declares a file carrying a standardized key outside its listed scope to be nonconforming and expressly assigns detection to the verifier, but §21's register contains no row for that condition and §2.4's four-value outcome vocabulary has no value that fits it (the reader ignores only the key, not the record), so the document simultaneously names a detectable violation and declares its own register complete.

> A writer MUST NOT emit a standardized key outside the scopes its row lists, and a reader MUST ignore a standardized key found outside its listed scope, or whose value does not match the shape its row gives, rather than rejecting the document. A file carrying a standardized key outside its listed scope is nonconforming, and a verifier detects it (`[R-CNF-11]`); no reader's behavior turns on the violation, since a reader ignores the key either way. `[R-MTA-07]`

> Every detectable violation named by this specification is assigned exactly one **reader outcome**: reject-file, reject-layer, reject-tile, or ignore-record. `[R-CNF-07]`

> Its **completeness is normative** — a *detectable* violation this specification names and the register omits is a defect in this document, detectability being the gate `[R-CNF-07]` already applies and §21.7 the inventory of what fails it

**Permitted readings.**

1. The register is authoritative for what counts as a violation; with no row and no assigned outcome class, the condition is not a violation and the file is conforming — a verifier certifies it.
2. `[R-MTA-07]`'s explicit sentence governs; the missing row is the document defect §21.1 anticipates. The file is nonconforming, a verifier must refuse certification, and `[R-CNF-12]` then licenses any reader to reject the file entirely.

**Picked.** Reading 2. §21.1 does not make the register a second authority — it says a missing row *is a defect in this document*, which is a statement about the register, not a licence to certify. `[R-MTA-07]`'s 'is nonconforming' is unqualified and names its detector.

**Rationale.** Under the picked reading the outcome-class hole remains: §2.4 offers only reject-file/reject-layer/reject-tile/ignore-record, and 'ignore the key but read the rest of the document' is none of them, so `[R-CNF-07]`'s 'exactly one' is false for this violation. Appendix H's verifier checklist also omits the check, which corroborates that the omission is unintentional rather than a deliberate silence. The same gap covers `tarn.title`/`tarn.description` (file+layer), `tarn.created`/`tarn.creator` (file only) and `tarn.axes`/`tarn.stats` (layer only).

**Byte-level?** yes — Concrete file: a 128+N byte file whose single layer record carries a user-metadata sub-record whose document decodes to {"tarn.created":"2026-01-01T00:00:00Z"} — a file-only key in a layer-scope document, everything else conforming. Under reading 1 the file is conforming and `[R-CNF-03]`/`[R-CNF-12]` oblige every conforming reader to accept it and serve the layer. Under reading 2 it is nonconforming and `[R-CNF-12]`'s 'a reader MAY reject it upon detecting any violation, including violations whose assigned detector is the verifier' lets a reader reject the whole file. Two implementations therefore disagree about whether these exact bytes must be accepted, and two verifiers return opposite verdicts.

### RD-02 — AMBIGUITY  · reporter flags BYTE-LEVEL

**Location.** §18.4 `[R-MTA-07]`, `[R-MTA-08]`; §2.1 `[R-CNF-01]`

§18.4's table states a value shape for every standardized key and `[R-MTA-07]` obliges a reader to ignore a key 'whose value does not match the shape its row gives', but only the *scope* violation is declared to make the file nonconforming. Whether a wrongly-shaped standardized value is itself a file-conformance violation is never stated.

> A writer MUST NOT emit a standardized key outside the scopes its row lists, and a reader MUST ignore a standardized key found outside its listed scope, or whose value does not match the shape its row gives, rather than rejecting the document. A file carrying a standardized key outside its listed scope is nonconforming, and a verifier detects it (`[R-CNF-11]`)

> All text in this document is normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices identified as non-normative. `[R-CNF-01]`

> Each is OPTIONAL and advisory — being metadata, none can affect decoding (`[R-MTA-02]`) — and a reader that finds one malformed MUST ignore that key rather than the document.

**Permitted readings.**

1. The value shapes are advisory descriptions of intent; only the scope rule is normative on writers, so a wrongly-shaped standardized value leaves the file conforming and a verifier certifies it.
2. §18.4's table is normative text under `[R-CNF-01]`, so a `tarn.title` whose value is not a string violates the table; the file is nonconforming and a verifier must refuse certification.
3. A middle reading: the shape is normative but its violation carries the same non-outcome as RD-01's scope violation, leaving both the register row and the outcome class undefined.

**Picked.** Reading 1 — the sentence that makes a file nonconforming is deliberately narrowed to 'outside its listed scope', and the section's lead calls every key 'OPTIONAL and advisory'. But nothing in the document says this, and the contrast is only inferable from what `[R-MTA-07]` chose not to say.

**Rationale.** A verifier must decide, for every standardized key it decodes, whether shape conformance bars certification. `[R-MTA-08]` further muddies it by declaring `tarn.stats` may be *stale* — a content-accuracy exemption — without saying anything about its shape. There is no register row for either case (see RD-01), so the register offers no tiebreak.

**Byte-level?** yes — Concrete file: a top-level user-metadata document decoding to {"tarn.title":42}. Under reading 1 the file is conforming and every conforming reader must accept it. Under reading 2 it is nonconforming, a verifier must refuse to certify it, and `[R-CNF-12]` licenses a reader to reject the file on detecting the violation. Same bytes, opposite accept/reject obligations.

### RD-03 — AMBIGUITY  · reporter flags BYTE-LEVEL

**Location.** §15.3 `[R-IDX-03]`; §16.2 `[R-SLB-03]`; §21.3 L42

When a reject-tile entry sits in the middle of a slab run, §15.3 removes its extent from the verifier rows, but the document never says whether run continuity is then evaluated *across* the removed entry (making its neighbours non-adjacent and escalating the damage from reject-tile to reject-layer) or is simply not evaluated where the stored sequence is broken.

> an entry these rows classify reject-tile contributes no stored extent to the *verifier* rows, which bind over well-formed entries' extents only, and none to `[R-LIF-08]`'s coverage walk, whose slack total therefore includes whatever bytes such an entry nominally addresses. `[R-IDX-03]`

> When declared, for every run: the run's stored tiles are contiguous and packed in ordinal order — each stored tile's offset equals the previous stored tile's offset plus its length — and the first stored tile's offset satisfies offset mod A_slab = 0.

> Sentinel tiles are transparent to run continuity: they occupy no bytes and do not break packing. A run with no stored tiles imposes nothing.

**Permitted readings.**

1. Build the list of well-formed stored extents in the run and require adjacency over that list. A malformed mid-run entry whose payload bytes physically sit between its neighbours therefore breaks packing, L42 fires, and the whole layer is rejected in addition to the tile.
2. Treat a malformed entry the way §16.2 treats a sentinel — transparent — and skip the continuity relation across it, so only the tile is rejected and the run's remaining pairs are checked among themselves where they are ordinal-adjacent.
3. Treat the entry as still nominally occupying [offset, offset+length) for continuity purposes only — impossible for the length=0 and offset>2^63−1 cases, so not generally available.

**Picked.** Reading 1, because §15.3's sentence says the verifier rows 'bind over well-formed entries' extents only', which most directly describes filtering the list and checking the survivors. But §16.2 grants transparency explicitly and only to sentinels, and §21.1's 'Conditions attach to the finest structure they damage' argues the other way.

**Rationale.** This is the one place where a tile-scope defect can silently promote itself to a layer-scope one, and the promotion is an artifact of a filtering sentence written for the overlap rows rather than a stated design choice. A conformance vector built under `[R-VEC-04]` for T10 inside a slab-declared layer would record a different expected outcome under each reading.

**Byte-level?** yes — Concrete file: a slab-declared layer (S=8, A_slab=1), run 0 covering ordinals 0–7; entries 0 and 2 are well-formed stored tiles, entry 1 is non-sentinel with length = 0 (T10, reject-tile), and entry 2's offset equals entry 0's offset plus entry 0's length plus 500 — i.e. the writer left room where entry 1's payload would have been. Under reading 1 the layer is rejected (L42) and `[R-CNF-09]` forbids a detector-obliged implementation to return tile 0's decoded samples at all. Under reading 2 only entry 1's tile is rejected and tile 0's samples may be returned. The same input bytes therefore yield permitted output under one reading and forbidden output under the other.

### RD-04 — CONTRADICTION

**Location.** §5.2 `[R-CNT-02]`; §8.1 `[R-CNT-19]`; §9.7 `[R-LIF-08]`; §7.2 `[R-CNT-13]`

§5.2 makes 'a record extent … whatever the record's type' a live-state structure and §9.7 obliges the coverage walk to check that every claimant verifies against the checksum covering it, but §8.1's map assigns a checksum only to tile-index regions and user-metadata extents. An unknown or experimental-type record's extent is a structure with no checksum, contradicting `[R-CNT-19]`'s 'every field of every structure'.

> Every byte of the live committed state belongs to exactly one of: the front signature block; or a **structure** — a stored-tile extent, a record extent (the bytes any record's extent slot references, whatever the record's type, §7.2), the directory, or the trailer.

> Every field of every structure is covered by exactly one checksum — excepting the equality-checked front signature block and this map's terminal checksum fields, per §4.5 — as this map states. All checksums are CRC-32C over bytes exactly as stored. `[R-CNT-19]`

> It checks that these occupy disjoint byte ranges, that each lies within [16, F − 64), and that each verifies against the checksum covering it (§8.1).

**Picked.** That the walk performs its disjointness and bounds checks on such an extent and simply has no checksum step to perform for it, leaving the extent's content uncovered by the integrity chain.

**Rationale.** §7.2 and §20.5 plainly contemplate MU = 0 unknown records carrying relocatable extents ('the extent slot is its only sanctioned reference to bytes outside the record sequence… this is what lets a compactor relocate an unknown ancillary's extent without parsing it'), and §21.6 declares an experimental MU = 0 record conforming, so such files must exist and must be certifiable. The defect is that `[R-CNT-19]`'s universal claim and §9.7's per-claimant checksum step are both written as if §8.1's map were exhaustive over §5.2's structure classes, which it is not. A verifier following §9.7 literally has a step it cannot execute for one claimant class; a security consequence follows too, since §22.3's 'every byte a reader can reach belongs to one named structure' is offered as a defense and these bytes are reachable, live, and unchecksummed.

**Byte-level?** no — No byte sequence changes classification. §21 registers no violation for an uncovered structure, and §7.2/§20.5/§21.6 jointly establish that an MU = 0 unknown record with an extent is a conforming file, so no implementation is licensed to reject it. The only divergence is whether a literal-reading verifier reports *cannot establish* (it cannot perform §9.7's checksum step for that claimant) rather than *conforming* — and §2.3 expressly says 'Cannot establish is not a finding that the file is nonconforming', so no reader may reject the bytes on that basis. Nothing about what may be emitted or must be accepted moves.

### RD-05 — AMBIGUITY

**Location.** §2.3 `[R-CNF-11]`; §2.4 `[R-CNF-12]`

The three verdicts are defined but their priority is not: when a verifier both finds a violation and meets a requirement it cannot check (an unimplemented MU = 1 record type in one layer, or a user-metadata document over its decode bound), the document does not say whether it reports *nonconforming* or *cannot establish*.

> A verifier reports one of three verdicts: *conforming*, *nonconforming*, or *cannot establish* — the last where some requirement is one it is unable to check, as when the file names a format major version it does not implement, when a record carries MUST_UNDERSTAND = 1 with a type it does not implement (§21.6), when it cannot execute a codec or filter (`[R-COD-11]`), or when it declines to decode a user-metadata document (`[R-MTA-09]`).

> *Cannot establish* is not a finding that the file is nonconforming, and a verifier MUST NOT certify a file it reports that way. A verifier MAY stop at the first violation it finds; one that does MUST report each scope it did not examine as *unexamined*, which is not a finding that the scope is clean.

**Permitted readings.**

1. *Nonconforming* wins: a positive finding of a violation is dispositive, and *cannot establish* is the residual verdict for the case where no violation was found but some requirement went unchecked.
2. *Cannot establish* wins: the verifier cannot establish the file's status as a whole, and the found violation is reported as a finding within that verdict.
3. Either is permitted; the verdict is an implementation choice as long as certification is withheld.

**Picked.** Reading 1. §2.3 already models 'violation found, most scopes unexamined' as a legitimate *nonconforming* verdict via the stop-at-first-violation licence, so an unchecked residue does not by itself displace a positive finding.

**Rationale.** Both verdicts withhold certification, so no file is wrongly certified either way; but the two send an operator to opposite remedies — fix the file versus obtain a more capable verifier — which is exactly the distinction `[R-ERR-04]` insists on elsewhere. The reader-facing consequence is nil.

**Byte-level?** no — Both verdicts bar certification and neither licenses accepting or rejecting bytes a reader would otherwise treat differently: `[R-CNF-12]`'s MAY-reject licence is triggered by the detected violation itself, which is present under either verdict. No byte sequence's accept/reject status moves.

### RD-06 — CONTRADICTION

**Location.** §2.3 `[R-CNF-03]`; §21.6 closing paragraphs

§2.3's parenthetical claims §21.6's closing paragraph names 'those two exceptions' to a conforming reader's acceptance duty, but the qualifiers §2.3 lists and the two cases §21.6 names are different sets: §21.6 names an unimplemented major version and an experimental-range MU = 1 record type, while §2.3's nearest two qualifiers are an unimplemented MU = 1 record type and values exceeding §21.9's minimum guarantees.

> A reader MUST accept every conforming file of a format major version it implements, carrying no record of a type it does not implement with MUST_UNDERSTAND = 1, and none of whose values exceeds the minimum guarantees of §21's limits table (§21.6's closing paragraph names those two exceptions),

> Two distinct cases are **conforming files a reader nevertheless refuses**. The first is **version_major naming a major this reader does not implement**: the reader rejects the file (`[R-CNT-07]`), but the file can be perfectly conforming under that major. The second is an **experimental-range record type carrying MU = 1** (§10.2, §10.3)

**Permitted readings.**

1. 'Those two' = the second and third qualifiers (unimplemented MU = 1 type; exceeding the minimum guarantees). §21.6 then names neither pair correctly — it omits the resource-limit case entirely and adds the major-version case.
2. 'Those two' = the first and second qualifiers (major version implemented; no unimplemented MU = 1 record). §21.6 then matches, except that §21.6 narrows its second case to the *experimental* range while §2.3 states it for any unimplemented type, and the third qualifier is left with no cross-reference at all.

**Picked.** Reading 2, because it is the only reading under which §21.6's closing paragraph actually names two matching cases. The resource-limit qualifier is then licensed by `[R-ERR-04]` in §21.9 rather than by §21.6.

**Rationale.** Substantively the acceptance duty is unaffected: §21.6's two cases are both covered by §2.3's qualifiers, and §21.9 independently licenses the resource decline. What is wrong is only the cross-reference's arithmetic, in a sentence that a reader implementer will use to enumerate exactly when it is allowed to refuse a conforming file — which is precisely the enumeration that should not require guessing.

**Byte-level?** no — Every case in either list is independently licensed by a rule of its own — `[R-CNT-07]` for the major version, `[R-CNT-15]` for the MU = 1 type, `[R-ERR-04]` for resource limits — so no reader's accept/reject behavior turns on which two the parenthetical points at. The defect is a broken pointer, not a substantive divergence.

### RD-07 — AMBIGUITY

**Location.** §5.2 `[R-CNT-21]`; §2.3 `[R-CNF-11]`; §9.7 `[R-LIF-08]`

§5.2 places an unconditional MUST on a verifier to report the slack total, with a 'partial' escape triggered only by a scope-level rejection stopping the walk; §2.3 separately licenses a verifier to stop at the first violation and report unexamined scopes. The document does not say whether a verifier that stops early is still bound by the slack-total MUST, nor whether a rejected layer's index region may nevertheless be walked to produce a complete total.

> A reader MUST NOT interpret it (§9.5); a verifier MUST report the total number of slack bytes, since that number is what tells an operator to compact; where a scope-level rejection stops the walk of §9.7 from enumerating a region's claimants, the verifier MUST report the total as partial and name the regions it could not walk. `[R-CNT-21]`

> A verifier MAY stop at the first violation it finds; one that does MUST report each scope it did not examine as *unexamined*, which is not a finding that the scope is clean. *Unexamined* is neither a verdict nor *cannot establish* — it constrains the report, not the verdict.

**Permitted readings.**

1. The slack-total MUST is unconditional; a verifier that stops early must still complete enough of the walk to report a total, marking it partial and naming the regions it skipped — reading the 'partial' clause as covering any incomplete walk, not only scope-level rejection.
2. Stopping at the first violation discharges the obligation via *unexamined*: the slack total is owed only by a verifier that completes the walk, since §2.3's licence is stated without qualification.
3. A rejected layer's structures are still enumerable (the index region's bytes are addressed by an extent slot whose validity may be independent of the rejection cause), so 'partial' is required only when the rejection actually prevents enumeration — leaving each verifier to decide when that is.

**Picked.** Reading 1. §5.2 gives the slack total a stated purpose ('what tells an operator to compact') that an early stop does not discharge, and its 'partial' mechanism is exactly the right shape for an incomplete walk.

**Rationale.** The slack total is one of only two things §22.3 identifies as verifier-detected security-relevant output ('the number that distinguishes a working file from a padded one'), so whether it survives an early stop matters operationally. Two verifiers can report different totals for the same nonconforming file — one complete, one absent, one partial — with no rule distinguishing them.

**Byte-level?** no — The slack total is report content, not a conformance predicate: §5.2 states slack's 'content is unconstrained, and no conformance requirement applies to it'. No byte sequence's validity, and no reader's accept/reject or return behavior, turns on which total is reported.

### RD-08 — AMBIGUITY

**Location.** §9.6 `[R-LIF-06]`; §9.7 `[R-LIF-08]`; §9.5 `[R-LIF-05]`; §21.2 F10/F19

§9.6 expressly names verifiers — not just recovery tools — as running the backward trailer probe, but nothing states what a verifier does with the result. A file whose physical tail is not a valid trailer is nonconforming (F10/F16/F19), so the probe has no stated bearing on any verdict.

> Recovery tools and verifiers — never conforming readers on the default path — locate commit states as follows: probe backward at 64-aligned offsets o for the trailer magic; on a match, require the trailer CRC to verify and committed_file_length = o + 64.

> A recovery tool enumerating a file's commit states continues the same probe to offset 0; coverage verification does not (§9.7, `[R-LIF-08]`).

> **Note.** Nothing here enumerates prior commits. A verifier certifies what a reader can reach and counts what it cannot, which is decidable from the live trailer in one pass and does not depend on reconstructing the file's history

**Permitted readings.**

1. The probe is diagnostic only: a verifier may run it to tell an operator where the last good commit lies, but the verdict on the bytes it was handed is nonconforming regardless, since the file's physical size does not equal any valid trailer's committed_file_length.
2. A verifier may treat the recovered prefix as the file under test and certify it, on the theory that §9.6 says 'truncating to it recovers the file' and requires the recovery output to be re-verified whole.
3. §9.6's mention of verifiers exists solely to exempt them from `[R-LIF-05]`'s prohibition on scanning backward, with no further consequence.

**Picked.** Reading 1 (with reading 3 as its mechanism). §2.3 makes file conformance 'a pure predicate on bytes', and the bytes handed to the verifier include the residue; F19 registers committed_file_length ≠ the transport-authoritative size as reject-file. §9.6's own 'recovery output MUST be re-verified as a whole file' treats the truncated result as a *different* artifact to be verified afresh.

**Rationale.** Reading 2 is textually available — §9.6 grants verifiers the probe and immediately talks about recovering the file — and an implementer who takes it would certify byte sequences that F10/F19 reject. The compulsion against it comes from three places outside §9.6, none of which §9.6 cites.

**Byte-level?** no — Under reading 2 a verifier would certify a 200-byte file whose last 64 bytes are residue but which carries a valid trailer at offset 64 with committed_file_length = 128 — bytes that F10 and F19 make reject-file. That divergence is real but foreclosed: §2.3's pure-predicate-on-bytes rule and F19 already decide the 200-byte sequence, and §9.6's own re-verification clause makes the 128-byte prefix a separate artifact. No implementation reading the whole document is licensed to accept what another rejects.

### RD-09 — OBSERVATION

**Location.** §21.1; §21.7 `[R-ERR-01]`

§21.1 characterises §21.7 as 'the inventory of what fails' the detectability gate, but §21.7 enumerates only five items and omits the whole Part III actor-obligation family — `[R-WRT-05]`–`[R-WRT-09]`, `[R-LIF-02]`, `[R-LIF-04]`, `[R-LIF-06]`, `[R-LIF-07]`, `[R-CNT-08]`'s updater copy-forward clause, and the conduct rules of §10.3, §18.3 and `[R-CNT-26]` — none of which a single file witnesses either.

> detectability being the gate `[R-CNF-07]` already applies and §21.7 the inventory of what fails it

> A second set of obligations is omitted from the register because a single file exhibits no witness of their violation. Committed-prefix immutability and the generation sequence (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a file's history, which §9.7 does not reconstruct; the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a structurally valid tile whatever values it carries; and `[R-CNT-13]`'s prohibition on an MU = 0 record encoding file offsets in its own payload is opaque by construction. `[R-ERR-01]`

**Picked.** That §21.7 is an illustrative sample rather than a closed inventory, and §21.1's 'the inventory' overstates it.

**Rationale.** Deciding this cheaply is impossible only in the sense that it takes a full sweep of every MUST in §9, §18 and §20 to confirm the omissions; the sweep is straightforward but tedious. It matters to a verifier because §21.1 invites the reading that anything not in §21.7 and not in the register is therefore checkable — which is how RD-01's gap becomes invisible. A one-line hedge ('a non-exhaustive inventory') or an explicit line for the actor-conduct family would close it.

**Byte-level?** no — Every requirement omitted from §21.7's list is an actor obligation whose violation `[R-CNF-02]` already declares not to be a file-conformance violation, or a multi-generation property. No byte sequence's validity changes under either reading of how exhaustive §21.7 is.

### RD-10 — AMBIGUITY

**Location.** §2.3 `[R-CNF-11]`; §17.4 `[R-COD-11]`; §21.9 `[R-ERR-04]`; §17.2 `[R-COD-06]`

§2.3 lists 'cannot execute a codec or filter' as a *cannot establish* trigger, but `[R-CNF-03]` makes every assigned codec and filter mandatory for a conforming reader — which a verifier is — while reserved and experimental values are reject-layer, i.e. nonconforming. The only live path to the trigger is a resource decline under `[R-ERR-04]` (a zstd window above 8 MiB, or a tile above the verifier's decode budget), and the document never says a resource decline yields *cannot establish* for tiles the way §18.2 says it does for documents.

> A verifier that cannot execute a layer's codec or filter cannot establish the layer's conformance and MUST NOT certify the file. For a conforming reader that position arises only at a reserved or experimental value, every assigned codec and filter being core: it rejects the layer (`[R-COD-03]`, `[R-COD-09]`); software unable to execute an assigned codec or filter is not a conforming reader (`[R-CNF-03]`). `[R-COD-11]`

> a wider window is conforming and merely permits a conforming reader to decline the tile or the layer on resource grounds (`[R-ERR-04]`)

> a refusal on resource grounds MUST be reported as a resource limit and not as a validity error: the two send a user to opposite remedies, and a reader that reports "too large" as "corrupt" invites the deletion of intact data. `[R-ERR-04]`

**Permitted readings.**

1. 'Cannot execute' includes 'declines to execute on resource grounds', so a verifier meeting a 64 MiB zstd window or a 1 GiB tile reports *cannot establish* and additionally reports the refusal as a resource limit — the reading §18.2 makes explicit for over-bound user-metadata documents.
2. 'Cannot execute' means capability only, so a resource decline is neither *cannot establish* nor *nonconforming* but a fourth report shape outside §2.3's three verdicts.
3. A verifier has no resource discretion over tiles at all: §17.4's 'MUST check' obligations for `[R-SER-05]` and `[R-SER-08]` are unqualified, so a verifier must decode every stored tile whatever its size, and the trigger really is dead for codecs.

**Picked.** Reading 1, by direct analogy with `[R-MTA-09]`, which spells out exactly this shape for documents: 'the bound is that verifier's capability and not a limit on validity (`[R-CNF-10]`), so it MUST report that it cannot establish the file's conformance rather than that the file is nonconforming'.

**Rationale.** §18.2 states the analogous rule for user-metadata documents in full — self-chosen bound, cannot-establish, SHOULD-report the bound and the declined length — and §17.4 states nothing equivalent for tiles even though the decode budget for a 256 MiB-guaranteed tile is the far larger cost. Every §21.9 quantity above its guarantee raises the same question and only one of the seven has a stated answer.

**Byte-level?** no — All three readings leave the file conforming (§21.9: 'A file exceeding any of these remains conforming') and all three bar certification while forbidding a validity-error report (`[R-ERR-04]`). What differs is the label on a verifier's report, not whether any byte sequence is accepted, rejected, or emitted.

### RD-11 — OBSERVATION

**Location.** Appendix A, closing paragraph

Appendix A asserts that a remote reader speculating a suffix window on this 128-byte file necessarily reaches offset 0 and therefore incurs `[R-CNT-04]`'s front-block equality check. That is false for speculative windows between 65 and 127 bytes, which land inside the file without reaching offset 0.

> A local reader additionally verifies bytes [0, 16) by equality first, which `[R-CNT-04]` requires of any reader holding them — as a remote reader does too whenever it speculates a suffix window, since this file is 128 bytes and any such window reaches offset 0.

**Picked.** That 'any such window' is meant informally as 'any window a real reader would speculate' (§6.4 suggests 64 KiB), not as a claim over all window sizes.

**Rationale.** Appendix A is non-normative, so nothing turns on it for conformance; but the appendix is the one worked example an implementer will trace, and `[R-CNT-04]`'s residency test is exactly the rule the sentence is illustrating. A window of, say, 96 bytes on this file yields [32, 128) — trailer and directory both resident, front block not — which is the interesting case the sentence claims cannot arise. Deciding it costs nothing; noticing it costs a careful reading of §6.4 against a 128-byte file.

**Byte-level?** no — The text is in an appendix identified as non-normative (`[R-CNF-01]` excludes it), and the normative rule it illustrates — `[R-CNT-04]`'s residency test — is stated correctly in §6.1 and §19.1 step 1. A reader that speculates a 96-byte window simply falls under the MAY-defer branch. No byte sequence is accepted or rejected differently.
