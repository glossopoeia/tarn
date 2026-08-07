# TARN specification — acceptance review, NAVIGATOR charter (gate G1)

## 0. What I verified mechanically before judging readability

A navigator's verdict is worth little if the document's own arithmetic doesn't hold, so I checked every claim in it that is decidable by computation.

| Claim | Where | Result |
|---|---|---|
| CRC-32C(`"123456789"`) = `0xE3069283` | §4.5 | reproduces exactly |
| CRC-32C(zero bytes) = `0x00000000` | §4.5 | reproduces exactly |
| CRC of a full all-sentinel segment = `0xEECB3BB2` | §15.4 `[R-IDX-05]` | reproduces exactly (2¹⁶ × 20 B = 1,310,720 B = 1.25 MiB, as §15.4's example says) |
| Appendix A trailer CRC = `0xE00938D2`, bytes `D2 38 09 E0` | Appendix A | reproduces exactly |
| Appendix A's 128-byte hex dump | Appendix A | byte-identical to a file I rebuilt from §5.1, §6.1, §6.2, §7.1 alone |
| Register size: 43 / 47 / 26 rows | §21.2, §21.3, §21.4 | 43 / 47 / 26 |
| "126 conditions over 235 named instances" | §21.8 `[R-ERR-02]` | 126 conditions, 235 instances, counting exactly as §21.1 prescribes (semicolon-separated; a cell reading — is one) |
| Requirement-ID inventory | §2.2 | 158 distinct IDs, no dangling reference, no prefix gap; the single retirement (`[R-SER-04]`) is documented in §14.4 |

Worked examples I checked by hand all hold: §11.2's grid (4, 8) / N=32 / P=65,536; §11.4's ordinals 0, 1, 8, s=10, in-tile 11,452, planar disk ordinal 74; §12.3's twelve-byte channel entry; §14.2's Q=3/decoded 18 and Q=5/decoded 30 cases; §14.3's `55 01` / `55 FD`; §14.5's 32-byte edge tile; §15.4's 20,000,064-byte region with segment 15 at [19,660,800, 20,000,000); §17.3's shuffle output `00 00 00 00 00 00 80 00 40 3F 40 40`; §20.3's 644-byte index region; §21.9's 256 KiB-at-2³² and 4 MiB-at-2³⁶ note; and §5.1's 128-byte floor, which is derivable from `[R-CNT-06]`'s gates alone (dir_offset ≥ 16, dir_length ≥ 4, sum ≤ F−64, F mod 64 = 0 ⟹ F ≥ 128).

That is an unusually clean result. The findings below are about *readability and residual under-specification*, not about a document that doesn't add up.

---

## 1. Structure

### The spine

Four parts plus appendices, and the partition is real rather than cosmetic:

- **Part 0 (§1–§4)** — introduction, conformance vocabulary, terminology, encoding conventions.
- **Part I (§5–§10)** — container: anatomy and byte coverage, front block and trailer, directory and records, integrity, lifecycle, extension points.
- **Part II (§11–§18)** — array model: geometry, types, fill, serialization, index, slabs, codecs, metadata.
- **Part III (§19–§24)** — behavior: reading, writing, the error register and limits, security, privacy, vectors.
- **Appendices A–H** — minimal file, constants, registry snapshot, rationale, changelog, references, reproducible-writer profile, checklists.

The declared reading order is §1's closing paragraph: §2 first ("fixes the conformance vocabulary every later section uses"); Part I "can be implemented without decoding a single sample"; Part II is the array model; Part III the algorithms. §1 also warns that "Part I alone yields a container reader… returning sample values needs Part II as well."

The section-opening paragraphs do what the §1 rubric promises. §5.1 opens with anatomy, §7.1 with the directory region, §11.1 with "geometry and its validity floor," §14 with "this section defines the **decoded tile image**," §19 with "this section consolidates the reader's normative path… It introduces no new structures." §3.3's Note explicitly asserts the Part I / Part II independence and says it is "load-bearing for the updater rules of §7 and §20" — a claim I could check, and it holds: no Part I rule requires decoding a payload.

### Does the declared order match the dependency graph?

Mostly. Three places where it does not, in descending severity:

**(a) §7.4 (the layer record) cannot be understood without forward-reading five Part II sections.** Its constraint table resolves layout into §14, linearization into §11.4, codec and filter into §17, index_encoding into §15, channel type into §12, fill length into §12.1's element sizes, and alignment/slab into §16. `[R-CNT-23]` makes validating those value sets a *layer-scope* obligation, and §19.3 confirms that first access to a layer must check "the value sets of §11.4, §12.2, §14.1, §15.1, §17.2, and §17.3." So a Part I-only reader cannot validate a layer record at all — it can only skip past it.

The text does warn, twice: §7.4 says inline "the value sets are §14, §17, §15, and §12's subjects," and §1 says returning samples needs Part II. But §1's framing — Part I "can be implemented without decoding a single sample" — understates it. What Part I yields alone is a reader that can enumerate layer *names* (§19.1 step 4) and nothing more; it cannot even declare a layer well-formed. That is a real gap between the promise and the dependency, though a mild one, and §1's very next sentence about §19.3 resolving into Part II "at every step" is the honest version.

**(b) §5.2 forward-references §7.2 and §16 before either exists.** `[R-CNT-02]`'s coverage classes name "record extent (bytes referenced by a record's extent slot, §7.2)" and define declared padding as "the alignment gaps of aligned or slab-declared layers (§16) and each generation's pre-trailer pad." A linear reader meets both terms cold. Both are section-cited, so it is a lookahead rather than a trap — but §5.2 is also where the document's most easily-missed writer constraint hides (see Finding O2).

**(c) §8 (Integrity) is a consolidation that depends on §15, which is 7 sections later.** §8.1's coverage map has a row for the tile-index region ("the per-segment CRC array, itself covered by the layer record's crc_of_crc_array") whose structure is not defined until §15.1/§15.4. §8 is short and clearly a summary table, so this reads as intended forward-reference, and §8.2's chain of trust is exactly the thing a reader wants early.

No section is *unreadable* without forward-reading. Every forward dependency I found carries a section citation.

One omission in the reading advice: §1 recommends §2 first, but §3 (terminology) and §4 (encoding conventions) are equally universal prerequisites — §4.5's checksum, §4.6's name rules, and §4.2's value domain are cited from every later part. A reader who takes §1's advice literally ("§2 … is worth reading first," then Part I) will hit `[R-ENC-09]`, `[R-ENC-12]`, and `[R-ENC-03]` as undefined terms in §6.1's first page.

---

## 2. Density — the three hardest passages

**(1) §7.4, the layer record (`[R-CNT-23]`, `[R-CNT-16]`, `[R-CNT-17]`, `[R-CNT-18]`).** The densest page in the document. To parse one layer record a reader must simultaneously hold: sixteen fields in fixed order with a `u8`/`u16`/`u64` mix and no padding; that two *variable-length arrays* (d dimension entries, C channel entries) sit between the leading fixed fields and a trailing fixed group (index_encoding, entry_count, crc_of_crc_array), so the tail's offset is content-dependent; that a channel entry's fill carries its own `u8` length prefix which must equal an element size defined in §12.1 ("fill parses without type knowledge and validates with it" — an elegant sentence carrying a lot of weight); that whatever remains is a sub-record sequence under §7.2 framing *with no residue*; that six enum fields each have their own assigned/reserved/experimental partition defined elsewhere; and that `[R-CNT-16]` (A and S mutually exclusive) and `[R-CNT-17]` (extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4) attach immediately. That is roughly twelve cross-references and one variable-offset parse in a single table.

**(2) §9.7, coverage verification (`[R-LIF-08]`).** The single hardest paragraph. Four labeled steps, each with an exception. To follow (a) you must hold §9.6's backward 64-aligned probe, then apply `[R-CNT-06]`'s field validity "against its own committed length F_k (taking the file size as F_k)" — a substitution that means something different from what `[R-CNT-06]` originally said and that I had to read three times — then the chain-selection rule (exactly one candidate per generation from g down to 1, strictly increasing committed lengths, each equal to its own offset + 64, accepted "whenever at least one such set exists," with everything outside the chain discarded as payload mimics). Step (b) needs F₀ = 16. Step (c) needs the *in-range restriction* on transitive references, whose justification appears only in the Note that follows the requirement ("a generation's directory may reference structures appended by earlier commits… but those bytes are claimed by the generation that appended them"). That Note is load-bearing, not decorative: without it step (c) reads as circular.

**(3) §15.3 + §15.4, taken with §14.2/§14.3.** To read one tile a reader holds: the disk-ordinal formula (§11.4's `c · N + s`), the 20-byte entry stride, the segment index `k div 2¹⁶`, a two-level CRC chain (crc_of_crc_array over the array, segment CRC over the segment), the sentinel's *exemption* from `[R-ENC-03]`/`[R-ENC-04]` (`[R-IDX-02]`), an eleven-row classification table whose last three rows bind verifiers only, `[R-IDX-03]`'s "notwithstanding" clause that overrides the general owning-scope mapping so per-entry failures are tile-scope rather than layer-scope, and finally the decoded-size formula selected by the layout × type cross-product. §15.4's worked example (entry_count = 1,000,000) is the thing that makes this tractable, and it is correct.

Honourable mention: **§17.2's codec 3** compresses six independent, separately-outcome-bearing zstd header constraints into one requirement `[R-COD-06]`. They only become tractable when §21.4 splits them into T17–T22. A reader implementing from §17.2 alone will miss one.

---

## 3. Redundancy and drift

The document restates deliberately and, with one exception, accurately.

**Value-set partitions — stated three times, all agreeing.** Each space is defined in its owning section, tabulated in §10.2, and snapshotted in Appendix C. I compared all eight rows against their owning sections: record type, channel layout, linearization, sample type, codec, filter, index encoding, metadata encoding. All agree. §10.2 flattens one distinction §11.4 makes (linearization 2–3 "reserved without semantics" vs 4–0x7FFF "reserved for future assignment") but both are invalid under `[R-GEO-05]`, so the flattening is lossless for implementers. Drift is guarded by an explicit precedence rule, `[R-EXT-05]`: "Where the registry, §10.2's table, and Appendix C diverge, the section that defines the space governs." This is the right design and it works.

**Constants — §4.7 claims "All named constants appear once in Appendix B," and Appendix B checks out.** All 23 rows agree with their defining sections, and the appendix labels itself a finding aid with normativity resting at the definition site. Helpful, low drift risk.

**Reader/verifier division of labour — stated five times** (§5.2's Note, §15.3's *verifier* rows, §16.1 and §16.2, §21's Detector column, Appendix H) and consistent every time. This is the most-repeated idea in the document and the repetition is earned: it is the thing most likely to be got wrong.

**Checksum-before-use — stated three times with subtly different scope.** `[R-ENC-05]` bans allocating/seeking/fetching on an unverified integer; `[R-ENC-10]` defines "acting on" and carves out "comparing a field against a constant for validation is not acting on it"; §8.2 `[R-CNT-20]` orders the chain. They cohere, but the carve-out exists in exactly one place. A reader who finds `[R-ENC-05]` first will conclude that §6.2's mandated order (magic **then** CRC) violates it, and must find `[R-ENC-10]`'s clause to be un-confused. This is redundancy that mildly increases misreading risk rather than reducing it.

**The metadata quarantine — stated four times** (`[R-CNT-25]`, `[R-MTA-02]`, `[R-MTA-09]`, §21.5's preamble), all agreeing. But the essential *carve-out* — that a malformed extent slot escapes the quarantine because "that failure precedes the document" — appears only in §18.1. A reader who implements from §7.1 alone will route a (0,0) slot to ignore-record instead of reject-file. §7.1 does name the (0,0) case explicitly, which saves it; the general principle is still single-sited.

**The one real drift: `[R-MTA-06]`.** §18.3 says "A file carrying an unrecognized `tarn.` key is **conforming**." §21.6's row for the same condition, citing the same rule, says "**The file is nonconforming**, but a reader ignores that key." These are restatements of one rule that have diverged into opposite verdicts. Detailed under Findings C2.

**Incomplete restatement: §16.1 gives A's floor but not its ceiling.** "a power of two ≥ 512. Writers MUST NOT emit any other nonzero value" — a reader implementing from §16.1 accepts A = 2⁶³. The ceiling (2⁶²) lives in §7.4's table, Appendix B, and register row L38. Decidable via `[R-CNT-23]`, which binds §7.4's table, but the §16.1 restatement is a subset of the rule rather than a copy of it.

---

## 4. Navigation

**"What happens when X is malformed?"** — §21 is purpose-built for this and largely succeeds. Four tables partitioned by outcome, each row carrying Condition / Instances / Detector / Detected / Governing rule, plus a fifth table (§21.6) of non-violations and a §21.7 statement of what nothing detects. §21.1's precedence rule ("where a row and the rule it cites diverge, the rule governs") is exactly right.

The limitation is that the register is **symptom-ordered, not field-ordered**. Answering "what happens if `entry_count` is wrong" means scanning §21.3 for the five rows that mention it (L1, L2, L20, L21, L26). The Instances column functions as a de facto field index if you can search the text, but there is no field→row index for a reader working on paper. For 126 rows across four tables that is tolerable; it would not be at twice the size.

**"How big is this structure?"** — Fixed sizes are excellent: Appendix B collects trailer 64, record header 24, index entry 20, front block 16, segment 2¹⁶ entries, sentinel 20 bytes. Variable sizes are findable but scattered: tile-index region in §15.1 + `[R-CNT-17]` + §15.4's example; decoded tile size in §14.2's table and §14.3; user-metadata extent only by joining §8.1's map with §18.2.

The layer record's inline payload size is computable from §7.4's table and **nowhere demonstrated**. This is the document's largest navigational gap and I flag it as O1: *Appendix A is a zero-layer file*, so the specification never once shows the bytes of a layer record, a dimension entry, a tile-index region, a segment CRC array, or a stored tile. §12.3 gives a single channel entry (12 bytes, correct). Everything else the implementer must synthesize with no cross-check. For a format whose entire value proposition is byte-exactness, and whose §24 corpus is explicitly "derivative" and non-authoritative, one annotated single-layer file would be worth more than any other addition to this document.

**"What does this enum value mean?"** — Best-navigated question in the document. §10.2's table plus Appendix C answer it in one lookup, both pointing back to the owning section, with `[R-EXT-05]` settling precedence. Nothing to improve.

**Findable only if you know where to look:**

- That a layer declaring neither alignment nor a slab may leave **no unclaimed gaps at all** — reachable only by joining §5.2's *enumerative* definition of declared padding with §16's grants. §16 never says it. (Finding O2.)
- `[R-IDX-02]`'s exemption of the sentinel from §4.2's value-domain rule. A reader who implements `[R-ENC-03]` generically will reject every sparse file until they find §15.2. §15.2's Rationale does flag this ("A reader that forgets the sentinel test still fails safely"), which is good, but the exemption is invisible from §4.2.
- `[R-ENC-10]`'s constant-comparison carve-out, needed to reconcile §6.2's validation order with `[R-ENC-05]`.
- §18.1's "the malformed slot precedes the document" carve-out from the quarantine.

**Well-signposted, worth naming as good practice:** §14.4's Note that "`[R-SER-04]` … is withdrawn; per §2.2 it is permanently retired and never reassigned." That is exactly what a reader hunting a missing identifier needs. The contrast with the register's unexplained numbering gaps (F6, F39, L40 — see O5) is instructive.

---

## 5. Honest verdict on G1

**A final G1 judgment belongs to a human who actually sits and reads this.** I cannot simulate the fatigue, the wandering attention, or the moment where a reader gives up. What I can report is the evidence that decides whether they *can*.

**Length and shape.** 3,171 lines, ~183 KB, roughly 28,000 words, of which §21's register is ~260 lines of table designed to be skimmed on a first pass and used as a lookup thereafter. At technical-reading pace with re-reads on layout tables, that is 2.5–3 hours. "One sitting" is a stretch — it is a long sitting — but the material is not padded, and §19/§20's consolidation means a reader who wants the algorithms can get them from two sections plus lookups.

**Evidence for G1:**
- The spine is coherent and the declared reading order is broadly honest.
- The §1 rubric (purpose → layout table → writer rules → reader rules → error handling → examples) is genuinely applied, so sections are predictable in shape.
- Every enum has a partition, a collected table, and a snapshot, all agreeing, with an explicit precedence rule.
- Every named constant appears in one place and every one I could compute is correct.
- 158 requirement IDs, no dangling reference, one retirement, documented in place.
- The register's own counts (43/47/26, 126, 235) are exactly reproducible by the counting convention §21.1 states — which means the completeness discipline is real and not aspirational.
- §21.6 (non-violations) and §21.7 (what nothing detects) are the two sections most specifications lack and most implementers need.
- Appendix H gives a per-class audit checklist that correctly disclaims its own authority.

**Evidence against G1:**
- §7.4 forces a five-section forward read to validate one structure, and §1's reading advice understates that.
- §9.7 is a genuine three-reads paragraph whose comprehension depends on the Note that follows it.
- No worked byte example of any layer-bearing structure anywhere in the document (O1).
- §21.6's taxonomy has drifted such that three of its rows contradict its own header (C3), and one contradicts its governing rule outright (C2).
- §2.3's "four classes" followed by five classes is the sort of error a fresh reader hits in the first ten minutes, and it costs the document trust it then has to re-earn.

**My assessment:** a competent engineer can read this in one long sitting and come away able to use it — for the container and the read path with confidence, and for the write path with confidence *except* for the byte-coverage/padding interaction (O2), which I expect most first-time readers to get wrong. The document's failure mode is not confusion; it is a small number of specific traps in an otherwise navigable text. Every one of them is a one-or-two-sentence fix.

---

## Findings

### AMBIGUITY

**A1 — `generation`'s upper bound. §6.2 `[R-CNT-06]` / §4.2 `[R-ENC-03]` / §21.2 rows F1 and F3. ⚠ BYTE-LEVEL.**
§6.2's trailer table gives `generation` valid values "≥ 1" with no ceiling and classes it *semantic*. §4.2 `[R-ENC-03]` says "The valid range of every offset, length, extent, and **count** this specification defines — entry counts and slab run lengths included — is 0 to 2⁶³ − 1," and §3.1 defines generation as "the **counter** … that numbers it."

Two readings the text permits: **(a)** generation is a count, capped at 2⁶³ − 1, so a trailer carrying 2⁶³ is reject-file; **(b)** generation is an identifier/ordinal outside `[R-ENC-03]`'s four enumerated categories, so any nonzero value is valid. The register pulls both ways: **F3** ("A u64 offset or length field holds a value above 2^63 - 1") lists dir_offset, dir_length, committed_file_length, and record extent fields but pointedly **omits** generation — evidence for (b) — while **F1** lists generation among the fields where a big-endian store "is detectable only through that field's own value **or range gate**," which presupposes generation *has* a range gate — evidence for (a).

I picked **(b)**: `[R-ENC-03]`'s categories are offsets, lengths, extents, counts, and generation is none of these in the sense the sentence uses them (its clarifier names "entry counts and slab run lengths"), and F3's omission is a deliberate-looking editorial choice given how carefully that column is constructed elsewhere. But this is a guess, and it is byte-level: the two readings accept different trailers.

This is not academic. `[R-VEC-03]` obliges the corpus to carry a vector for "every boundary value … at its stated bound." Generation has no stated bound, so the vector's expected verdict is undefined. One clause in §6.2's table row ("≥ 1; ≤ 2⁶³ − 1" or "≥ 1; no upper bound") closes it.

**A2 — A user-metadata extent shorter than its own terminal CRC. §8.1 `[R-CNT-19]` / §7.1 `[R-CNT-25]` / §18.1 `[R-MTA-02]` / §7.2 `[R-CNT-13]`. ⚠ BYTE-LEVEL.**
§8.1's map says a user-metadata extent's checksum is "final 4 bytes of the extent" covering "the preceding bytes." `[R-CNT-13]` validates the *slot* — both halves nonzero, offset ≥ 16, within F − 64, no overflowing sum — and imposes no minimum length. So a slot of (1024, 2) passes every stated slot test while making §8.1's decomposition impossible: there are no "final 4 bytes" and no "preceding bytes."

Two readings: **(a)** this is a way the document "can be unreadable," so the quarantine applies (`[R-CNT-25]`: "*every* way a user-metadata record's document can be unreadable … is ignore-record") and the file otherwise reads normally; **(b)** it is a malformed extent, and §18.1's carve-out governs — "a malformed extent slot on such a record, (0, 0) included, is a validity error at the record's containing scope … because that failure precedes the document" — giving reject-file for a top-level record and reject-layer for a sub-record.

I picked **(a)**, because §18.1's carve-out is worded against the *slot* and this slot is well-formed by every test `[R-CNT-13]` enumerates; the defect is in the extent's *content length*, which is downstream. But (b) is defensible — the failure genuinely does precede the document — and the two readings accept different files. Compare `[R-CNT-06]`'s explicit `dir_length ≥ 4` for the structurally identical directory region: that floor is stated, this one is not.

No register row covers either reading (see C4). One clause — "extent_length MUST be at least 4" in `[R-MTA-03]`, or an explicit routing sentence in §18.2 — closes it.

*Byte-level ambiguities: 2 (A1, A2).*

### CONTRADICTION

**C1 — §2.3 says "four classes" and then defines five.**
§2.3, opening sentence: "Conformance is defined for four classes." The bullets that follow define **Conforming TARN file** `[R-CNF-02]`, **Conforming reader** `[R-CNF-03]`/`[R-CNF-04]`, **Conforming writer** `[R-CNF-05]`, **Conforming updater** `[R-CNF-06]`, and **Conforming verifier** `[R-CNF-11]` — five. Appendix H independently confirms five, giving a checklist for each of file, reader, writer, updater, verifier.

These cannot both hold. The count is wrong, not the list; `[R-CNF-11]`'s verifier is referenced as a class throughout (§2.4, §5.2, §9.7, §21's Detector column, Appendix H). Low severity, high visibility — it is on the second page of normative text and it is the first thing that makes a careful reader stop and count.

**C2 — `[R-MTA-06]`: §18.3 says such a file is conforming; §21.6 says it is nonconforming.**
§18.3: "writers MUST NOT emit a `tarn.`-prefixed key this specification's registry does not define at the version they target … **A file carrying an unrecognized `tarn.` key is conforming** — later minor versions register keys, exactly as they define ignore-lane flag bits (§6.3), and this text's readers skip both harmlessly."

§21.6, row citing `[R-MTA-06]`: "A user-metadata document carries a `tarn.`-prefixed key this specification does not define | **The file is nonconforming**, but a reader ignores that key and reads the rest of the document."

Both cite `[R-MTA-06]`; they assign opposite conformance verdicts to the same bytes. Reader behavior is unaffected (both say ignore the key and read on), but a **verifier's certification** and a §24 manifest entry are not: `[R-VEC-02]` requires every vector to record "whether the file is **conforming**," and a corpus author reading §18.3 and one reading §21.6 will record opposite values for the same file.

The intended resolution is presumably version-relative — a file written by a *later minor's* writer carrying `tarn.newkey` is conforming, while a file from a *this-text* writer carrying an invented `tarn.` key violates §18.3's MUST NOT — but neither sentence says so, and since a reader cannot tell which writer produced the file, the predicate is not decidable on bytes, which sits badly against §2.3's "File conformance is a pure predicate on bytes." §21.1's precedence rule would settle it in §18.3's favour, except that §21.1 says "The register below enumerates every **violation**," and §21.6 is by its own heading *not* part of that enumeration — so it is unclear whether the precedence rule even reaches this row.

**C3 — §21.6's heading contradicts three of its own rows.**
§21.6 is titled "Conditions that are **not violations**" and its preamble states: "These are defined behaviors, not errors. A reader that treats any of them as a failure is the nonconforming party." Three of its thirteen rows say the opposite in their own text:

- unsorted user-metadata object members (`[R-MTA-05]`): "**The file is nonconforming**, but the document is readable: a verifier reports it and readers process it unchanged";
- unrecognized `tarn.` key (`[R-MTA-06]`): "**The file is nonconforming**…";
- a registered record type's stored MU/PE bit differing from §7.3's fixed values (`[R-CNT-22]`): "**The file is nonconforming**, but readers apply the type's fixed semantics regardless."

A condition that renders a file nonconforming is by §2.4's own words a violation ("A file is conforming only if it satisfies every requirement at every scope"). These three rows are not "not violations" — they are violations whose *reader outcome* is "process normally, verifier reports." The table conflates "imposes no reader failure" with "is not a violation," and there is no outcome class in §2.4's vocabulary (reject-file / reject-layer / reject-tile / ignore-record / preserve-verbatim) for "nonconforming but fully processed," which is why they ended up here. Consequence: a verifier implementer reading §21.6 concludes these files certify; reading the row text, concludes they do not.

**C4 — §21.1's normative completeness claim vs. violations the register omits.**
§21.1: "The register below enumerates every violation this specification names … Its **completeness is normative** — a violation this specification names and the register omits is a defect in this document."

At least one named violation has no row in §21.2–§21.5, and I verified this by scanning every row of all four tables:

- **`[R-MTA-03]`**: "A record whose `inline_length` is not 1 is a validity error at the record's containing scope — the payload is a fixed structure (`[R-ENC-07]`), not a growable one." A user-metadata record with `inline_length` = 0 or 2, sitting entirely within its containing sequence, violates this. The only rows mentioning `inline_length` are **F32** (record extends past the end of the directory sequence), **L13** (sub-record doesn't fit), and **L22** (layer-record payload regions) — none of which covers it. Outcome would be reject-file top-level, reject-layer as a sub-record.

Three further named violations appear **only** in §21.6, which §21.8's coverage obligation does not reach ("Every row of §21.2 **through §21.5**"): `[R-MTA-05]` unsorted members, `[R-CNT-22]` stored MU/PE mismatch, and `[R-MTA-06]`'s writer-side prohibition. Under `[R-ERR-02]` and `[R-VEC-03]`, the corpus is therefore obliged to carry no vector for any of them, though each is a MUST-level writer prohibition with an assigned verifier detection.

§21.1's completeness claim and the existence of these conditions cannot both hold. The document names the consequence itself: "a defect in this document."

*(C4 also perturbs §21.8's arithmetic: adding the missing `[R-MTA-03]` row would make it 127 conditions / 237 instances, since the condition ranges over top-level record and layer sub-record.)*

### OBSERVATION

**O1 — The specification never shows the bytes of any layer-bearing structure.** Appendix A is a 128-byte, zero-layer file — correct, well annotated, and byte-verifiable (I rebuilt it exactly). But it contains no layer record, no dimension entry, no tile-index region, no segment CRC array, and no stored tile. §12.3 shows one 12-byte channel entry; that is the only real byte string for anything in Part II. An implementer must therefore synthesize their first layer record — a variable-length structure with a content-dependent tail offset, six enum cross-checks, and an embedded sub-record sequence — with no worked example to check against, and their first index region likewise. For a format whose §24 corpus is explicitly derivative ("Passing the corpus is evidence of conformance, never its definition"), and which is meant to be "implementable from this document alone" (§1), a second annotated file — one layer, two dimensions, two channels, one stored tile and one sentinel, with every byte labeled — would repay its length several times over. This is the single highest-value addition I can name.

**O2 — Gaps between structures are legal only for layers that declare alignment or a slab, and nothing says so where a writer will look.** `[R-CNT-02]` partitions every byte into: front block; a structure of exactly one generation; or **declared padding** of exactly one generation — and defines declared padding *by exhaustive enumeration*: "the alignment gaps of aligned or slab-declared layers (§16) and each generation's pre-trailer pad." It then closes: "A file containing bytes claimed by no class is not a conforming file."

Therefore a layer with A = 0 and S = 0 has **no** padding class available, and its structures must be packed with no unclaimed bytes — as must the run-up to the directory, since no padding class covers "space before dir_offset" either. Meanwhile `[R-SLB-05]` reads, in isolation, as a blanket grant: "A layer that declares neither alignment nor a slab makes no layout promise: its stored tiles MAY occupy **any non-overlapping byte positions, in any order** — a streaming writer places tiles in acquisition order at no cost to conformance."

This is *decidable* — `[R-SLB-05]` grants placement freedom, not a padding class, and §5.2's enumeration is closed — which is why I file it as an observation rather than an ambiguity. But it is decidable only by joining two sections eleven apart, and the sentence a writer-implementer will actually read says "any byte positions." A writer that leaves a 7-byte gap between two tiles of an undeclared layer emits a file that fails F9 at certification while satisfying every rule in §15 and §16. One clause in `[R-SLB-05]` — "…subject to `[R-CNT-02]`: without a declaration a layer has no padding class, so its structures leave no unclaimed bytes" — removes the trap entirely.

**O3 — §1's reading-order advice understates §7.4's forward dependency.** §1 says Part I "can be implemented without decoding a single sample." True for the *read path*, but `[R-CNT-23]` makes validating a layer record's six enum fields a Part I obligation resolved entirely in Part II, and §19.3 confirms it. What Part I alone actually yields is a reader that lists layer names (§19.1 step 4). §1's following sentence about §19.3 "resolv[ing] into Part II's value sets and geometry rules at every step" is the accurate version; the two sentences would be better merged.

**O4 — §9.7 `[R-LIF-08]` is the document's comprehension bottleneck, and its explanatory Note is normative in effect.** Step (c)'s in-range restriction is only *justified* in the Note that follows ("those bytes are claimed by the generation that appended them, not by the generation that retains them"); without it, step (c) reads as circular. Since §2.1 makes text "labeled *Note*" non-normative, a rule whose comprehensibility depends on a Note is structurally fragile. Consider folding that sentence into `[R-LIF-08]` step (c).

**O5 — Unexplained numbering gaps in the register: F6, F39, L40.** Row numbers run F1–F45 minus {6, 39} and L1–L48 minus {40}; T and R are contiguous. The counts are internally consistent (43, 47) and I verified them, so nothing is *missing* relative to the stated totals — but a reader who notices the gap has no way to tell whether a row was withdrawn or whether they are looking at a truncated table. §14.4's treatment of `[R-SER-04]` shows the document already knows how to handle this: one line saying these row numbers are retired would match that practice.

**O6 — `[R-EXT-03]` states a MUST NOT that is not a predicate on bytes.** "Writers MUST NOT emit files carrying an experimental value **in released software or published data**." Whether software is "released" is not observable in the file, so no verifier can check this and no register row can exist for it. It sits against §2.3's "File conformance is a pure predicate on bytes: it does not depend on any reader, writer, or environment." The requirement is good practice and worth keeping, but it may belong as a SHOULD-with-consequence or as explicitly non-file-level guidance.

**O7 — `[R-MTA-09]` makes user-metadata readability reader-dependent, which §24's manifest format cannot express.** "a reader instead decodes with a bound of its own choosing, no smaller than §21.9's user-metadata guarantee, and a document exceeding that bound is ignore-record like any other it cannot read." So for a document between 16 MiB and any larger reader-chosen bound, two conforming readers legitimately disagree about whether the document is readable. `[R-VEC-02]` requires each vector to record "the decoded content a reader is to return from every scope it can read" — for such a file there is no single answer. The design choice is sound (the alternative is a declared size field the quarantine forbids); the interaction with §24 just needs a sentence.

**O8 — The `[R-ENC-05]` / §6.2 apparent conflict is resolved in a third place.** `[R-ENC-05]` says a reader "MUST NOT allocate, seek, or issue I/O based on any integer obtained from a file before the checksum covering it has been verified," while §6.2 `[R-CNT-06]` mandates checking the trailer *magic* before the trailer *CRC*. The reconciliation lives inside `[R-ENC-10]`: "comparing a field against a constant for validation is not acting on it, and an explicit validation order (§6.2) governs where one is stated." Correct, but a reader who reaches `[R-ENC-05]` and stops has an apparent contradiction; a forward pointer from `[R-ENC-05]` to `[R-ENC-10]`'s carve-out would cost one clause.

**O9 — The sentinel's exemption from the value domain is invisible from §4.2.** `[R-ENC-03]` caps every offset and length at 2⁶³ − 1; the sentinel is 2⁶⁴ − 1. The exemption is stated only in `[R-IDX-02]` ("Sentinel entries are a reserved pattern, not offsets or lengths: `[R-ENC-03]`'s value-domain rule and `[R-ENC-04]`'s sum rule apply to the fields of non-sentinel entries only"). An implementer who writes a generic domain check while reading §4 will reject every sparse file. §15.2's Rationale anticipates the failure mode gracefully ("A reader that forgets the sentinel test still fails safely"), and §15.3's table is ordered so the sentinel rows come first — both good. A cross-reference from §4.2 would complete it.

**O10 — Detection-tier wrinkle: a layer record whose *name* field overruns its inline payload.** §19.1 step 4 obliges the open to parse every layer record's name ("build the layer table: each layer record's name, parsed and checked per §4.6"), and §19.2 places the layer-name namespace "at open." But **L22** — "A declared region of the layer record's inline payload does not lie entirely within `inline_length` … leading fixed fields (name … C)" — assigns detection to "layer access." So a truncated name is due at layer access yet unavoidably encountered at open, for a layer that may never be accessed.

The outcome is reject-layer either way (L22), and §19.2 licenses earlier detection, so the file still opens with that layer poisoned — I am confident in that resolution, which is why this is an observation and not an ambiguity. But it leaves §2.4's reject-layer promise unachievable in this case: "A reader MAY still list the file's layers, including the rejected one's name" — there is no parseable name to list. Also worth noting that `[R-ENC-15]`'s file-scope duplicate-name check then runs over a name set with holes in it.

**O11 — §16.1 restates alignment A's constraint incompletely.** "a power of two ≥ 512. Writers MUST NOT emit any other nonzero value" omits the 2⁶² ceiling that §7.4's table, Appendix B, and register row L38 all state. Decidable via `[R-CNT-23]` (which binds §7.4's table) and via §16.1's own "(§7.4)" citation, but an implementer working from §16 will accept A = 2⁶³.

---

## Verdict

IMPLEMENTABLE: qualified — I could build a conforming reader, writer, and verifier from this text alone, but I would have to decide A1 and A2 myself, derive O2's no-gaps rule by joining §5.2 to §16, choose a side in C2/C3 for the verifier's certification verdict, and synthesize my first layer record and tile-index region with no worked example to check against (O1).
BYTE-LEVEL AMBIGUITIES: 2
CONFIDENCE: high
