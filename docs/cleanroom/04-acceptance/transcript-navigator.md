# TARN Specification — Navigator Review (G1 evidence)

**Scope of this review.** `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, read in full (3,235 lines, 30,669 words). No other file, no repository history, no external source. Every conclusion below cites section numbers and requirement IDs from that text. Where I made a mechanical check, I state the check and its result.

---

## 1. What I verified mechanically

Before reporting anything, I tried to refute the document by recomputing what it asserts.

**Every stated constant reproduces exactly.** I implemented CRC-32C to §4.5's parameters (polynomial 0x1EDC6F41, reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF):

| Claim | Where | Computed | Verdict |
|---|---|---|---|
| CRC-32C(`"123456789"`) = `0xE3069283` | §4.5 check vector | `0xe3069283` | ✅ |
| CRC-32C(zero bytes) = `0x00000000` | §4.5, Appendix B | `0x0` | ✅ |
| CRC of a full all-sentinel segment (2¹⁶ × `FF×16 00×4`) = `0xEECB3BB2` | `[R-IDX-05]`, Appendix B | `0xeecb3bb2` | ✅ |
| Appendix A trailer CRC `0xE00938D2` over trailer bytes [0,60) | Appendix A | `0xe00938d2` | ✅ |
| Appendix A directory region [16,20) = CRC of a zero-byte record sequence | Appendix A | `0x0` | ✅ |

Appendix A's hexdump is internally consistent end to end: 128 bytes, `committed_file_length` = 0x80 = the dump's length, `dir_offset` = 16, `dir_length` = 4, pre-trailer pad [20,64) all zero, trailer at the 64-aligned offset 64. `[R-IDX-05]`'s constant being correct matters more than it looks: `[R-IDX-05]` licenses writers to *emit* it without computing it, so a wrong constant would have made every sparse writer's output rejected by every reader. It is right.

**§21.8's arithmetic claim reproduces exactly.** §21.1 states the counting rule ("Instances within a cell are separated by semicolons, and a cell reading — is one instance; the count is therefore mechanical"). Applying it literally to §21.2–§21.5:

| Section | Rows | Instances |
|---|---|---|
| §21.2 file scope | 38 (stated: 38) | 69 |
| §21.3 layer scope | 47 (stated: 47) | 81 |
| §21.4 tile scope | 26 (stated: 26) | 43 |
| §21.5 ignored records | 10 | 20 |
| **Total** | **121** (stated: 121) | **213** (stated: 213) |

Both totals match. This is unusual and worth saying plainly: a normative corpus-coverage obligation (`[R-ERR-02]`, `[R-VEC-03]`) is stated as a number, and the number is right.

**Every worked example I recomputed is correct.** §11.2's grid (G=(4,8), N=32, P=65,536); §11.4's ordinals (spatial s=10, in-tile 11,452, planar disk ordinal 74); §14.2's interleaved and planar byte offsets (Q=3 → sample 5 at [15,18); Q=5 → [25,30)); §14.3's packed plane (`55 01` with fill false, `55 FD` with fill true); §14.5's edge tile (32 bytes, values 1–15 each `CD AB`); §15.4's segment arithmetic (16 segments, segment 15 at [19,660,800, 20,000,000), entry at region byte 339,180, region 20,000,064 bytes); §17.3's shuffle (`00 00 00 00 00 00 80 00 40 3F 40 40`); §20.3's index size 32·20+4 = 644.

**The chain of trust closes with no bootstrap paradox.** I traced every fetch a reader issues against `[R-ENC-05]` ("MUST NOT allocate, seek, or issue I/O based on any integer obtained from a file before the checksum covering it has been verified"). The trailer range comes from the transport size, not from the file; `dir_offset`/`dir_length` are covered by the trailer CRC, verified first; the layer record is covered by the directory CRC; the segment and CRC-array ranges are computed from `entry_count` and the extent slot, both directory-CRC-covered; the payload range comes from an entry the segment CRC covers. The one apparent circularity — reading the trailer magic and CRC before the CRC verifies — is closed explicitly by `[R-ENC-10]`'s "comparing a field against a constant for validation is not acting on it, and an explicit validation order (§6.2) governs where one is stated." No gap.

**§10.2's seven numeric spaces agree with their defining sections and with Appendix C.** Where a section subdivides a reserved range (linearization "2 and 3 reserved without semantics; 4 through 0x7FFF reserved for future assignment" vs. the table's flat 2–0x7FFF; sample types 14–19 vs. 20–0x7FFF), the subdivision is a refinement, not a conflict.

**Geometry has no degenerate corner.** Since tᵢ < Gᵢ = ⌈Eᵢ/Tᵢ⌉ implies tᵢ·Tᵢ < Eᵢ, every addressed tile contains at least one real sample position — there is no all-padding tile to argue about. Zero-extent dimensions collapse to N = 0 and zero addressed tiles under both layouts, consistent with `[R-GEO-02]` and `[R-CNT-17]`.

---

## 2. Charter item 1 — Structural spine and declared reading order

§1's "Reading this document" declares: §2 first, then Part I (§5–§10, container), Part II (§11–§18, array model), Part III (§19–§24, behavior), then §21's register and the appendices.

The order mostly matches dependency, and §1 is honest about the one place it doesn't: "Part I alone yields a container reader … returning sample values needs Part II as well, since §19.3's layer validation resolves into Part II's value sets and geometry rules at every step."

Two dependency inversions are real:

1. **§7.4 (Part I) is a hub of forward references into Part II.** The layer-record table has 16 field slots and defers *eight* of them — layout (§14), linearization (§11.4), codec (§17), filter (§17), alignment/slab (§16), channel type (§12), fill (§13), index_encoding (§15). `[R-CNT-23]` states this openly ("the value sets are §14, §17, §15, and §12's subjects"). A first-pass reader can parse the layer record after Part I but cannot validate it. §1 discloses this.

2. **§5.2 (Part I) forward-references §16 (Part II) for the moduli that *define* declared padding.** Declared padding is defined constructively as a run "less than that declaration's modulus — A for per-tile alignment, A_slab for a slab run". You cannot compute the coverage partition — the thing `[R-CNT-02]` makes the file-conformance predicate turn on — until you have read §16. §1 does **not** disclose this one, and it is the more surprising of the two, because §5.2 reads like a self-contained definition.

Otherwise the spine is sound. §2 (conformance vocabulary), §3 (terms + the reference array as the conformance target), §4 (encoding conventions) are genuine prerequisites and are placed first. §8's coverage map and §8.2's ordered chain of trust arrive exactly when they are needed. Part III consolidates rather than introduces, and says so.

**Length.** ~30,700 words; ~22,700 outside §21's register and the appendices; §21 alone is 5,506 words and 23% of the document overall is table. A careful engineer reading the normative core linearly is looking at roughly 2.5–3 hours; treating §21 as the lookup table it is (§21.1 calls each row a restatement of a rule that governs) brings a first pass to around two hours. "One sitting" is achievable, at the long end of it.

## 3. Charter item 2 — The three densest passages

**(a) §7.4 + `[R-CNT-23]`/`[R-CNT-16]`/`[R-CNT-17]`/`[R-CNT-18]` — the layer record.** The densest thing in the document. A reader must simultaneously hold: the exact field order of a variable-length packed payload; that `d` dimension entries and `C` channel entries are themselves variable-length (name prefixes) so nothing after them is at a fixed offset; three interlocking cross-checks (`entry_count` ↔ geometry-derived tile count; `extent_length` ↔ `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4`; A ≠ 0 XOR S ≠ 0, with A_slab = 0 forced when S = 0); that the fill field's *length* is framing but its *validity* needs the type; that the trailing bytes are a nested record sequence that must parse with no residue and may not nest further; and that every failure is layer scope *except* a duplicate layer name, which is file scope. That last exception is stated in three places (`[R-ENC-15]`, `[R-CNT-23]`'s closing clause, §19.1 step 4) — appropriate, given how easy it is to miss.

**(b) §5.2 + §9.7 + §16's `[R-SLB-05]` — the coverage partition.** The concept is split across three sections in two different Parts. To answer "is this file conforming?" a verifier must hold: three coverage classes; two and only two forms of declared padding, each with a modulus test; the live-state reachability walk; and the fact that dead space is defined as the *complement* rather than enumerated. §5.2's own Rationale is what makes this land ("this specification certifies the live state exactly, and counts the rest") — but the rule itself is spread thin, and this is where my two closest near-misses live (O4, O5 below).

**(c) §15.3 + §15.4 + §8.2 + `[R-ENC-05]`/`[R-ENC-10]` — the index chain.** Ten classification rows, split between reader-detected and verifier-detected, over a 20-byte entry whose sentinel value is *deliberately exempt* from the value-domain rules that govern every other offset and length (`[R-IDX-02]`). Layered on top: a strict verification order, per-segment CRCs with a special rule for the final partial segment, and `[R-TYP-09]`'s prohibition on ever substituting fill for a rejected tile. The load here is real, but the document carries it well — §15.2's Rationale explains *why* all-ones rather than zero/zero, and the answer ("a reader that forgets the sentinel test still fails safely: all-ones offsets trip the overflow and bounds checks") is the kind of thing that makes a rule stick.

## 4. Charter item 3 — Duplication and drift

The document duplicates deliberately and heavily: §21's register restates all 121 violation conditions; Appendix B collects every constant; Appendix C snapshots the registry; §10.2's table restates seven value spaces; Appendix H summarizes each conformance class.

**The precedence rules are explicit and consistent.** §21.1: "where a row and the rule it cites diverge, **the rule governs**." `[R-EXT-05]`: "Where the registry, §10.2's table, and Appendix C diverge, the section that defines the space governs." Appendix H: "each entry's authority is the requirement or section cited, never this summary." Appendix B: "Each is normative where it is defined; this table is a finding aid." That is four separate duplications, each with a stated tiebreaker. This is the right design, and it is why the drift I found is survivable.

**Drift actually found is citational, not semantic** — with one exception. I checked §10.2 against all seven defining sections (agree), Appendix B against its cited sections (agree), Appendix C against §7.3/§12.1/§17.2/§17.3/§14.1/§11.4/§15.1/§18.2/§6.3 (agree), and Appendix H against the requirements it summarizes (agree). What did not survive: F7's governing-rule citation (O2), §17.4's dangling §9.7(d) (O3), and the §21.6 placement problem (Contradiction 2), which *is* semantic.

## 5. Charter item 4 — Random-access answerability

| Question | Answerable without linear reading? |
|---|---|
| "What happens when X is malformed?" | **Yes, very well.** §21.2–§21.5 index by outcome scope, and each row carries condition, instances, detector, detection point, and governing rule. The Instances column makes the corpus obligation mechanical. Caveat: five conditions have no row (O1). |
| "How big is this structure?" | **Yes.** Every fixed structure has an offset/size/type/class/valid-range table at its definition, and Appendix B collects every constant with its defining section. Derived sizes (decoded tile size, index region size) have closed-form expressions in `[R-SER-02]`/`[R-SER-03]` and `[R-CNT-17]`. |
| "What does this enum value mean?" | **Yes.** §10.2's table gives all seven spaces with assigned/reserved/experimental partitions in one place; Appendix C restates them as a flat list. |
| "Where is `[R-XXX-NN]` defined?" | **No.** There is no table of contents and no requirement-ID index. With ~130 identifiers, 121 register rows citing them, and §24 requiring vectors to cite identifiers rather than prose positions, ID → location is the most frequent lookup an implementer will perform, and it is unsupported. This is the single highest-value addition to the document's navigability. |

---

# Findings

## BYTE-LEVEL AMBIGUITY

**None found.** I pursued eight candidates to the point of constructing a discriminator, and each was refuted by an explicit sentence. Recording the near-misses and what refuted them, because a null result is only worth as much as the search behind it:

1. *Is a stored tile's CRC over stored or decoded bytes?* — Refuted twice: §8.1's map ("Stored tile | the crc field of its index entry | **the tile's stored bytes**") and §19.4 step 5 ("verify the entry's crc over the stored bytes **before decoding**").
2. *Does a final partial index segment's CRC cover the whole 2¹⁶-entry span or only its actual entries?* — Refuted by §15.4: "the final partial segment's CRC covers only its actual bytes," reinforced by `[R-IDX-05]`'s "a partial segment's CRC MUST be computed" and register row L37.
3. *Filter-then-codec or codec-then-filter?* — Refuted by `[R-COD-01]`, which states both directions explicitly.
4. *Does the "less than the modulus" test for declared padding agree with "exactly the distance to the next legal offset"?* — Not an ambiguity: for a maximal run ending at an aligned structure, the two conditions are mathematically equivalent. Verified algebraically.
5. *`[R-COD-07]`'s lz4 cap over a mixed-type planar layer* — see O8; the two candidate readings ("any channel's plane" and "the maximum") produce identical verdicts, so no discriminator exists.
6. *Dead-space classification of an over-modulus alignment gap in a generation-1 file* — see O5; refuted by §5.2's leading clause plus `[R-SLB-05]`'s explicit complement statement.
7. *Whether the front block and trailer count toward a verifier's dead-byte total* — see O4; refuted by §5.2's definition of the live committed state.
8. *Whether a user-metadata record with `inline_length` ≠ 1 or `extent_length` < 5 is ignore-record (quarantine) or a containing-scope rejection* — refuted by §7.1 and `[R-MTA-03]` stating the outcome in place, and by §18.1's principle: "The quarantine covers the document only … because that failure precedes the document."

**BYTE-LEVEL AMBIGUITIES: 0**

## CONTRADICTION

**C1 — §2.3 declares four conformance classes and then defines five.**
- §2.3, line 132: "Conformance is defined for **four** classes."
- §2.3, lines 134–169: five bulleted classes follow — Conforming TARN file, Conforming reader (`[R-CNF-03]`), Conforming writer (`[R-CNF-05]`), Conforming updater (`[R-CNF-06]`), Conforming verifier (`[R-CNF-11]`).
- Corroborating: Appendix H gives **five** checklists, one per class. `[R-CNF-11]`'s high identifier number is consistent with the verifier class having been added after the sentence was written. §2.1 makes §2.3 normative text, so the count is a normative statement that is false. No byte consequence; a reader who counts wins.

**C2 — §21.6 is headed "Conditions that are **not** violations" but contains two conditions its own rows call violations.**
- §21.6 lead: "These are defined behaviors, **not errors**. A reader that treats any of them as a failure is the nonconforming party."
- §21.6 row (`[R-MTA-05]`): "A user-metadata document's object members are not sorted … | **The file is nonconforming**, but the document is readable: a verifier reports it and readers process it unchanged."
- §21.6 row (`[R-CNT-22]`): "A registered record type's stored MU or PE bit differs from the value §7.3's registry fixes | **The file is nonconforming**, but readers apply the type's fixed semantics."
- The cited rules confirm the rows, not the heading. §18.2: "unsorted members do not make a document unreadable: **the file is nonconforming, a verifier MUST report it**, and readers process the document unchanged." §7.3: "A stored-flag mismatch on a registered type **makes the file nonconforming** (`[R-CNF-05]`)."
- Why it matters beyond editorial: §21.1 makes the register's **completeness normative** ("a violation this specification names and the register omits is a defect in this document"), and §21.8/`[R-VEC-03]` attach the corpus-vector obligation to rows of §21.2–§21.5 only. These two violations therefore get no enumerated row and no required vector. The precedent cuts the other way in the same document — F29/F30/L47/L48 place writer-only, behavior-neutral violations (MU=1 with PE=0; reserved flag bits set) in §21.2/§21.3 as verifier-detected rows. The treatment is inconsistent, not principled.
- A careful reader still resolves the *behavior*: the row text and the governing rule agree that the file is nonconforming and that readers proceed unchanged. What is left undetermined is the **verifier's certify/refuse decision**, since `[R-CNF-12]` says "a verifier certifies only violation-free files."

## OBSERVATION

**O1 — Register-completeness gaps (§21.1 makes completeness normative).** Mechanically confirmed absent from §21.2–§21.5:
- `[R-CNT-25]`'s "an extent … whose `extent_length` is less than 5 … is a validity error at its containing scope" — no row. (Grepped the register for "less than 5": no hit. F27 covers only extent (0,0); L11 the sub-record case.)
- `[R-MTA-03]`'s "A record whose `inline_length` is not 1 is a validity error at the record's containing scope" — no row. (The three `inline_length` hits are F31, L13, L22, all different conditions.)
- `[R-MTA-07]`'s "A writer MUST NOT emit a standardized key outside the scopes its row lists" — no row, no outcome, no detector. Reader behavior *is* defined ("a reader MUST ignore … rather than rejecting the document"); file conformance is not.
- Plus the two from C2.

Reader behavior is determinate for all five, because each rule states its outcome where it lives. The undetermined party is the verifier.

**O2 — F7 cites the wrong governing rule.** The 128-byte minimum is `[R-CNT-27]` (§5.1: "No conforming file is shorter than 128 bytes … A reader MUST treat a shorter file as a validity error at file scope. `[R-CNT-27]`"). F7's Governing-rule cell reads `[R-CNT-01]` (R-ENC-07, R-CNT-06). I grepped the whole document: **`R-CNT-27` occurs exactly once, at its own definition** — it is cited nowhere else, including by the register row that exists to enumerate it. §21.1 says each row cites "the requirement that defines it"; this one does not. Harmless to behavior (both rules yield reject-file at open), but it breaks the ID-to-row traceability §24 depends on.

**O3 — §17.4 cites a subsection that does not exist.** `[R-COD-11]`: "A verifier that cannot execute a layer's codec or filter … MUST NOT certify the file — the rule of **§9.7(d)** applied to content." §9.7 is four sentences of prose plus a Note; it has no lettered or numbered items.

**O4 — §9.7's walk omits the front block and trailer, inflating a mandated output by exactly 80 bytes if read literally.** `[R-CNT-21]` obliges a verifier to "report the total number of dead bytes," and §9.7 defines that total as "Bytes the walk does not reach." The walk it enumerates is "the live directory and its records, each record's extent, each layer's tile-index region and that region's non-sentinel entries, and the declared padding §5.2 defines" — and it checks "that each lies within [16, F − 64)", a bound that structurally excludes the front signature block [0,16) and the trailer [F−64, F). §5.2 puts both squarely in the live committed state. Read literally, §9.7 makes the dead total 16 + 64 = 80 bytes too high on every file. **Refuted** by §5.2's definition (dead space is "every other byte" once the live state — which explicitly includes the front block and the trailer — is subtracted), so a careful implementer gets the right number. Worth a clause in §9.7 nonetheless, because the output is normatively required to be a specific number.

**O5 — §5.2's dead-space gloss is narrower than its own leading clause.** "Every other byte of the file is **dead space**: bytes **an earlier commit wrote** that the live state no longer reaches." In a generation-1 file there is no earlier commit, so an over-modulus alignment gap (a maximal unclaimed run of length ≥ A before an aligned tile, which the constructive rule excludes from declared padding) satisfies the leading clause but not the gloss. **Refuted** by the leading clause itself and, decisively, by `[R-SLB-05]`: "a byte the live state neither claims nor accounts for as declared padding **is dead space**" — and by §9.7's purely complement-based phrasing. Three statements, two unambiguous; a careful reader resolves it. Recommend making the gloss non-defining ("typically: superseded payloads and index regions, …").

**O6 — `[R-SLB-05]` names a "writer defect" with no requirement, outcome, detector, or register row.** "a commit that produces dead space it did not supersede is a writer defect (`[R-CNT-02]`, `[R-LIF-02]`)." Neither cited rule prohibits it: `[R-CNT-02]` constrains only the live-state partition, which such a file satisfies, and §5.2 says outright that "**no conformance requirement applies to** [dead space]." So the sentence either names nothing enforceable or names a violation the register omits. Given §5.2's Rationale, the former is clearly intended; the wording invites the latter.

**O7 — §21.3 skips L40 with no note.** Rows run L1…L39, L41…L48. The section's stated count of 47 is correct, and §21.8's total of 121 depends on the skip, so the arithmetic is deliberate. But §2.2's retirement discipline is stated for `[R-…]` identifiers only, and §14.4 shows the document knows how to announce a retirement ("Identifier `[R-SER-04]` … is withdrawn; per §2.2 it is permanently retired"). A one-line note at L40 would close the question a reader auditing the register will ask.

**O8 — `[R-COD-07]` does not quantify over channels.** "Writers MUST NOT declare this codec for a layer whose **tiles' decoded size** exceeds 0x7E000000 bytes … a reader MUST treat such a declaration as a validity error at layer scope, checkable from declarations alone." In a *planar* layer with mixed element sizes there is no single per-tile decoded size — a `uint8` plane is P bytes and a `float64` plane 8P. The natural readings ("any channel's plane exceeds" and "the maximum exceeds") are equivalent, so no verdict diverges and this is not byte-level; but the text should say which, since it explicitly demands a layer-scope check.

**O9 — a zstd writer trap that nothing warns about.** `[R-COD-06]`: writers "MUST NOT declare a window size exceeding the tile's decoded size; a reader MUST treat either as a validity error at tile scope" (register row T21). Under RFC 8878, when `Single_Segment_flag` is 0 the `Window_Descriptor`'s floor is 1 KiB. A writer that streams a sub-1-KiB tile through a stock zstd encoder without supplying the content size therefore emits `Window_Size` = 1024 > decoded size and produces a file **every conforming reader rejects at tile scope** — while believing it used the codec correctly. The fix (set `Single_Segment_flag`, i.e. supply the content size, for small tiles) is one sentence and belongs next to §17.2's existing Note about exactly-one-frame enforcement, which addresses the symmetric reader-side trap.

**O10 — the window guarantee and the tile guarantee are not connected.** §21.9 guarantees a reader accepts a 256 MiB decoded tile but only an 8 MiB zstd `Window_Size`. A writer relying on the minimums (`[R-CNF-10]`: "writers MAY rely on those minimums") must therefore cap its encoder window at 8 MiB even on a 256 MiB tile, or its file is one a conforming reader may decline on resource grounds. This follows from `[R-CNF-10]` and `[R-ERR-04]` but is never stated as writer guidance, and it is the one place where two of §21.9's rows interact.

**O11 — three phrases for one concept.** "Owning scope" (§2.4, `[R-CNF-08]`), "the scope the record governs" (§7.2, `[R-CNT-13]`, `[R-CNT-15]`), and "its containing scope" (§7.1, §18.1, §18.2, `[R-MTA-03]`) all appear to denote the same thing. §2.4 defines only the first. Since §2.4's owning-scope mapping is the mechanism by which "a validity error at the owning scope" becomes a concrete outcome, the two undefined synonyms cost more than usual.

**O12 — `[R-CNT-25]`'s opening sentence is structurally broken.** §7.1: "each user-metadata record carries its document in its extent — never inline; an extent of (0, 0) …, or one whose extent_length is less than 5 — too short to hold both a document and the terminal CRC-32C §8.1 places in its final 4 bytes — is a validity error at its containing scope — **and declares the document's encoding in its own inline payload**." The subject ("each user-metadata record") is separated from its second predicate ("and declares…") by three interposed clauses and four em-dashes. Both rules are recoverable, but this is the one sentence in the document where I had to re-read to determine what was being predicated of what — and it carries two distinct normative requirements.

**O13 — no table of contents and no requirement-ID index.** See §5 above. §24 (`[R-VEC-02]`) makes vectors cite register rows and identifiers rather than prose positions, which is the right call — and it makes the missing reverse index (identifier → defining section, identifier → register rows) the document's most-felt navigational gap.

---

# G1 verdict (gate evidence)

**PASS, with reservations — and the final judgment belongs to a human reader who actually sits down with it.** I cannot read for two hours; what I can report is that every property that decides whether a human can, holds.

**What supports a pass.** The spine matches the dependency graph, with the two inversions noted and one of them disclosed in §1. The rubric §1 promises (purpose, layout table, writer rules, reader rules, error handling, worked examples) is genuinely followed, and the worked examples are numerically correct — I recomputed nine of them and all nine hold, which means a reader can calibrate their understanding against the document instead of against an implementation. Duplication is heavy but every instance of it carries an explicit precedence rule, so a reader who finds two statements knows which wins without guessing. The three questions the charter names as the random-access test — what happens when X is malformed, how big is this, what does this enum value mean — are all answerable in one lookup. And the two hardest things to hold in the head, the coverage partition and the index chain, are both accompanied by Rationale blocks that explain the *mechanism* rather than restating the rule; §15.2's "a reader that forgets the sentinel test still fails safely" is the kind of sentence that makes a rule survive a reader's memory.

**What qualifies it.** Three things a human reader will hit.

First, **§7.4 is a wall**. It is the one place where the promised structure breaks down: a 16-slot table where half the entries defer their meaning to sections 4–10 chapters away, wrapped in four interlocking requirements (`[R-CNT-16]`, `[R-CNT-17]`, `[R-CNT-18]`, `[R-CNT-23]`) that must be held simultaneously. A reader who is going to lose the thread will lose it here. It would survive being split — framing and parse rules in Part I, the value-set cross-reference table restated compactly at the head of §19.3 where validation actually happens.

Second, **the coverage partition is assembled from three separated sections** (§5.2, §9.7, §16's `[R-SLB-05]`), and it is exactly where my two closest near-misses live (O4, O5). Both are resolvable, but both cost a reader a re-read and a cross-section comparison, and one of them (O4) would produce a wrong number in a normatively mandated verifier output for a reader who *doesn't* re-read. This material wants to be in one place.

Third, **§21 is 5,506 words that no one will read linearly**, nor should they — §21.1 says as much by making each row a restatement whose rule governs. It functions as a lookup table, which is correct, but the lookup it best supports is by outcome scope, and the lookup an implementer most needs is by requirement identifier. Without a TOC or an ID index (O13), the register is a table you can browse but not query.

None of the three is a defect in the *content*. They are load and layout problems, and all three have cheap fixes. Against them: I found zero byte-level ambiguities in a 30,000-word binary-format specification, all five stated constants reproduce, and the register's own arithmetic claim — 121 conditions over 213 instances — is exactly right. That combination is not what an unimplementable document looks like.

---

# Verdict

**IMPLEMENTABLE: qualified**

The reader, writer, and file conformance classes are implementable from this text alone. I traced the full open → directory → layer → index → tile path and found no point where two competent implementers would produce different bytes or reach opposite verdicts. The qualification is narrow and specific: the **verifier** class has undetermined certify/refuse behavior on five conditions — the two in C2 and the three in O1 — because §21.1 makes register completeness normative while `[R-CNF-12]` makes certification turn on violation-freedom, and those five conditions are named as violations in the body but omitted from the enumerated register. That affects no returned sample byte and no reader verdict; it affects what a conforming verifier is obliged to certify. Closing it needs five register rows and one heading fix, not a design change.

**BYTE-LEVEL AMBIGUITIES: 0**

**CONFIDENCE: high**

High for the container and array model (Parts I–II), where I recomputed every constant and worked example, traced the verification chain end to end, and mechanically checked the register's counts, its rule citations, and the seven value spaces against their defining sections. Somewhat lower for the prose-heavy behavioral sections (§20, §22–§24), which I read carefully but could not subject to the same mechanical cross-checking — a second reader targeting §20's updater obligations specifically would be worth the cost.
