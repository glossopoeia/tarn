# Round 30 triage — implementer-consequence lens

## What I read

- `spec/tarn.md`: §2 (whole), §4, §5, §6.2–6.4, §7, §9.1–9.7, §11, §12, §14, §17, §18, §19, §20 (whole), §21 (whole), §22.3 [R-SEC-04], Appendix G.
- `r30-round/out/transcript-reader.md` lines 160–215 (reader-01 reasoning), and a grep of `transcript-adversary.md` to locate adversary-02 (lines 405–420; I did not need to read further).
- Nothing else. No directory listing of `r30-round/` was run; the only `ls` was of the two named transcript files. No other triage pass's notes were opened.

## Grouping

| group | members | why one defect |
|---|---|---|
| planar-pq-designation | reader-01 | alone |
| cnf02-closed-list-of-two | reader-02, writer-03, verifier-04 | all three: §2.3's "the cases this text states" (two) vs §9.2's barrier declaration |
| retype-makes-tiles-nonconforming | reader-03 | alone |
| l23-name-instance-tier | reader-04, register-02 | same cell, same sub-case, same rule |
| key-order-unequal-length | writer-01 | alone |
| appendix-g-compactor-minor-floor | writer-02, diagrams-01 | item 8 vs closing paragraph |
| unassigned-encoding-two-senses | verifier-01 | alone |
| mta09-note-vs-err04-scope | verifier-02, register-01 | same Note vs same sentence |
| partial-total-file-scope-rejection | verifier-03 | alone — a gap in the discard clause |
| partial-total-discard-legibility | quiz-01 | separate: reports no gap, only cost of applying a clause it concedes is decided |
| ser08-antecedent-detecting-reader | adversary-01 | alone |
| wrt08-drop-on-added-record | adversary-02 | alone |
| cod11-dead-cannot-establish-ground | adversary-03 | alone |
| sec216-crossref-bound-declines | register-03 | alone |

19 ids, 14 groups, each id once.

## Judgements

### planar-pq-designation (reader-01) — CONFIRMED, byte-level

Checked text. §14.2 table is layout-keyed: `planar, numeric channel c | P · Bᶜ` / `interleaved | P · Q`; then "where Bᶜ is …, Q = Σ Bᵢ over all channels (the **sample stride**), and Fᶜ = … These products and sums are declaration-derived quantities under `[R-ENC-04]`." The designation sentence is collective and untagged. [R-ENC-04]: "A designation is express, made by the section that defines the quantity". L2 Instances: "N·P; C·N (…); P·Q (which dominates V = P·C); P·Bᶜ; entry_count × 20 + …" — untagged, whereas L21 says "interleaved N … planar C·N" and L44/T3/T14/T21/T22 say "interleaved P·Q; planar numeric P·Bᶜ; packed planar bool ⌈P/8⌉". §21.1: "Where the quantity a condition derives varies by layout, the layout formulas are materially different shapes and the cell enumerates them." §19.3: "on the decoded sizes §14 derives from it". [R-SER-07]: "Every decoded size, and the value count V, is a declaration-derived quantity". §17.2 Note: "P·Q and P·Bᶜ are checked in an empty layer even though this cap is not."

Two implementations, both natural:
- A (reading i): at layer access forms every product L2 lists, including P·Q, for every layer; for a planar layer with P·Q > 2⁶³−1 it reject-layers and a verifier reports *nonconforming*.
- B (reading ii): forms the layer's decoded size(s) under its layout — P·Bᶜ per numeric channel, ⌈P/8⌉ per bool plane — plus V, N·P, C·N; never forms P·Q for a planar layer.

Reporter's construction verified: rank 1, E = 0, T = 2⁵², 4096 uint8 channels, codec 1, planar. [R-GEO-01]: "A tile extent MAY exceed its dimension's extent … at Eᵢ = 0 the grid count is 0 and the layer addresses no tile". N = 0, N·P = 0, C·N = 0, entry_count = 0, slot (0,0). P·Bᶜ = 2⁵², V = P = 2⁵², both in domain. P·Q = 2⁶⁴, out of domain. §21.9: "A layer addressing no tile therefore has no tile whose decoded size the table bounds"; C = 4096 meets "at least 4096"; rank 1. So under (ii) the file is conforming and within every guarantee and [R-CNF-03] obliges A to accept — A is nonconforming. Under (i) the file is nonconforming, B has missed a reader-detected row, and no conforming writer may emit it. Accept/reject verdict, verifier verdict, and emittable set all move.

Not only the empty layer: a planar layer with an addressed tile, P = 2⁵⁰, float64 channels ×4096 has P·Bᶜ = 2⁵³ (in domain) and P·Q = 2⁶⁵. A refusal on resource grounds is licensed there either way, but the *verifier verdict* still forks (nonconforming under (i); conforming-or-cannot-establish under (ii)), and so does whether a writer may emit it.

The same untagged-cell question sits on C·N (§11.2 designates "N for an interleaved layer and C · N for a planar layer … These products are declaration-derived"; L2 lists "C·N" untagged): an interleaved layer with C·N > 2⁶³−1 forks the same way. The repair should cover both.

Premise my grade rests on: that the §14.2 designation sentence and the L2 cell are each readable as designating P·Q for every layer (the sentence is collective; the cell is untagged where every sibling cell is tagged), while §19.3, [R-SER-07] and §21.1's layout convention read the other way. I could not find a sentence that decides which; the reporter's reading (ii) is well supported and reading (i) is what a reader building L2 from the register writes.

Repair: pick one and say it in the designating section and the row. Cheapest and consistent with §19.3/[R-SER-07]: §14.2 → "The decoded size of each layout, Q, and Fᶜ are declaration-derived quantities under `[R-ENC-04]`: an interleaved layer's P·Q, a planar numeric channel's P·Bᶜ; a planar layer has no P·Q to form." L2 Instances → "interleaved P·Q (which dominates V = P·C); planar numeric P·Bᶜ" and "interleaved N; planar C·N" for the ordinal product, adjusting §21.8's instance count. Or the other way (designate both unconditionally) — either is a one-clause edit; the choice is the maintainer's.

### cnf02-closed-list-of-two (reader-02, writer-03, verifier-04) — CONFIRMED, editorial, not byte-level

§2.3: "§6.3's flags = 0 against a set ignore-lane bit and §6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad are the cases this text states". §9.2: "Steps 4 and 6 bind a writer's **conduct** rather than its output, and are declared so here on the model `[R-CNF-02]` states … A writer that omits a barrier violates this requirement, and the file it produces is not nonconforming on that account." §9.2 uses both of [R-CNF-02]'s categories' phrasings, and the second category's closed count is now short by one whichever it is. writer-03 is right that which category is not stated.

Not byte-level; deciding text, §9.2: "a barrier … leaves no trace in the bytes, so a file committed without one can be byte-identical to a file committed with it." Nothing an implementation emits, accepts or rejects turns on the count. Repair: either add the barriers to §2.3's list, or reword §9.2 to "on the model §10.3 and §18.3 state" (conduct category only) and drop the "not nonconforming on that account" clause, which is what puts it in the second category.

### retype-makes-tiles-nonconforming (reader-03) — CONFIRMED, editorial, not byte-level

§20.3 step 4: "Where a change does reach them it makes each stored tile it reaches nonconforming". [R-CNF-02]: "File conformance is a pure predicate on bytes". [R-TYP-05]: "Every bit pattern of a numeric type's element size is a valid sample value". Reporter's byte-identity argument holds: int8→uint8 with same fill byte and no padding positions leaves every T-row satisfied, and a creator can emit the identical bytes with the old directory/trailer as slack ([R-CNT-21]: "its content is unconstrained"). So the sentence's "nonconforming" is not a statement about the file. The bar (MUST NOT) is clear and stands.

Not byte-level; §21.7: "A writer that emits well-formed structures carrying wrong sample values … produces a file that every checksum in §8 certifies" — this is the class the retyped tiles fall in, and no verifier row exists to find. Implementer consequence: a verifier author hunting for a row wastes time; no verdict moves. Repair: "Where a change does reach them, the tiles' stored bytes would denote values under a type they were not written under — wrong content of the kind §21.7 leaves unwitnessed — and re-emitting those tiles would strand …".

### l23-name-instance-tier (reader-04, register-02) — CONFIRMED, register-bookkeeping, not byte-level

L23 Detected: "layer access" for the instance "leading fixed fields (name … C)". §19.1 step 4: "a layer record whose name field does not lie entirely within that record's inline_length yields no name field to compare, so it contributes no name to the namespace and is instead a validity error at layer scope (`[R-CNT-18]`)" — at open, where the namespace is built. L3/L5/L6 (other layer-name rows) already say "open".

Not byte-level; §21.1: "where a row and the rule it cites diverge, **the rule governs**", and [R-RDR-02]: "A reader MAY detect any violation earlier". Both tiers give reject-layer; a reader that defers cannot in fact defer, since it must parse every name at open to build the namespace and must notice the overrun to skip the record. Repair: split the cell on R1's model — "open (name); layer access (the remaining fields)".

### key-order-unequal-length (writer-01) — CONFIRMED that it is undefined in letter, editorial, not byte-level

[R-MTA-05]: "in ascending order of their keys' UTF-8 bytes". Appendix G item 3 says "compared lexicographically" for its record key. No sentence states the unequal-length case. Reporter self-graded not byte-level and I agree, on this premise: the sentence names the *bytes* as the sort key and nothing else; a length-first (shortlex) order sorts first on a quantity — the length — the sentence does not name, so it is not "ascending order of their bytes" but a different order that needs extra words (which is exactly how RFC 7049 had to state it, "sorted by length first", before RFC 8949 moved to bytewise lexicographic). That precedent is why this is worth the one-clause repair: implementers coming from CBOR canonical encoding have seen both. Implementer consequence today: every mainstream byte-string sort (memcmp, sort.Strings, BTreeMap, Python bytes ordering) is lexicographic-prefix-first, so two teams do not diverge. Repair: "(lexicographically by byte value, a proper prefix ordering first)" in [R-MTA-05], with the same words in Appendix G item 3's "ascending layer-name byte order".

### appendix-g-compactor-minor-floor (writer-02, diagrams-01) — CONFIRMED, editorial, not byte-level

Item 8: "The version_minor floor binds a compactor too, save where its output carries a feature it does not implement, when §20.5's floor governs instead". Closing paragraph: "`version_minor` at its floor, which `[R-CNT-26]` states as a SHOULD — item 8's creator's rule, not a compactor's (§20.5)". §20.5 [R-WRT-06]: "Otherwise version_minor follows `[R-CNT-26]`'s floor." Item 8 and §20.5 agree; the closing gloss is the stale neighbour. Not byte-level: Appendix G "adds no requirement to any actor"; [R-CNF-12] "Deviation from a SHOULD is not a violation"; [R-CNT-07] "A reader MUST NOT reject a file for its version_minor". Implementer consequence: a profile compactor built from the summary might emit the input's minor rather than the floor, defeating byte-identity across compactors — but item 8 already concedes that ("reproducible only modulo its trailer"). Repair: closing paragraph → "— item 8, which binds a compactor too save §20.5's carried-feature case".

### unassigned-encoding-two-senses (verifier-01) — CONFIRMED, editorial, not byte-level

§21.5: "Encoding 0 and a reserved-range value are unassigned too, and R1 registers both as violations". [R-MTA-03]: "An encoding a reader does not implement is therefore one this specification does not assign". §2.3 and §17.4 say of "an encoding this specification does not assign" that "certification is unaffected" / "is not a violation" — true only of the experimental range. §17.4's "in a conforming file" qualifier rescues its sentence circularly; §2.3's has no qualifier. Not byte-level: R1 is a reader-detected register row, "0 is invalid" in [R-MTA-03], and [R-CNF-11] "a verifier that has established any violation reports *nonconforming*" — every verifier implements R1 as a reader and the verdict does not fork. Repair: in §2.3, §17.4 (and §9.7, §22.3 for consistency) say "experimental-range encoding (§21.6)".

### mta09-note-vs-err04-scope (verifier-02, register-01) — CONFIRMED, editorial, not byte-level

[R-ERR-04]: "at the narrowest scope … a layer, a tile, or the record carrying a user-metadata document, as §18.2 assigns". §18.2 body: "a frame declaring more than the reader admits is ignore-record on that ground — the reader's capability … the file exceeds a §21.9 guarantee and so remains conforming while the reader MAY decline it (`[R-ERR-04]`)". §18.2 Note: "a reader that instead declines on resource grounds under `[R-ERR-04]` does so at the whole file, a document having no declared size and so no narrower scope". The Note denies what the rule and the body it glosses assert. Not byte-level: under either text the permitted behaviours are ignore-record or whole-file refusal on a conforming file, and only the report's label ("resource limit" per [R-ERR-04] vs [R-CNT-25]'s SHOULD-report) differs; [R-CNF-01] makes the labelled Note non-normative. Implementer consequence: a reader's diagnostic path files the record-level ignore under the wrong rule; no served byte changes. Repair: rewrite the Note: "A reader that declines the document takes ignore-record for that record, which is `[R-ERR-04]`'s narrowest-scope decline for a document — reported as a resource limit, not as corruption — or MAY decline the whole file."

### partial-total-file-scope-rejection (verifier-03) — PARTIAL, design-decision, not byte-level

§5.2's discard clause is expressly a layer clause: "a rejected layer's claimants are not enumerated … where the rejection is one the walk itself established, L18's overlap or L40 through L42's placement among them, the claimants it had already enumerated are discarded with the layer". For a walk-established file-scope rejection (F33, F7) the general definition applies literally: "A partial total is F less the bytes claimed by the claimants the walk did enumerate". So the letter decides (b), the reporter's implementation; the stated rationale ("a claim about a live state one of whose layers is not usable") invites (a) for a state none of which is usable. Not byte-level: a partial total is a reported figure, "an upper bound on the file's true slack, never an under-count", both readings satisfy that and the file is already nonconforming. Two verifiers report different integers, which nothing tests. Decision for the maintainer: state which; I recommend confirming (b) in one sentence ("A file-scope rejection discards nothing: the total is F less what was enumerated before it") since discarding everything makes the figure F − 80 for every such file and tells the operator nothing.

### partial-total-discard-legibility (quiz-01) — REFUTED as a defect, severity none

The reporter concedes "The rule is fully decidable from the text (I resolved it correctly by rereading)". The clause quoted is the deciding one. No repair needed; if group 9's sentence is added, restating the composition rule as three cases (layer rejection the walk established → discard that layer's claimants; other scope stop → keep what was enumerated; file-scope → as decided) would serve both.

### ser08-antecedent-detecting-reader (adversary-01) — PARTIAL, editorial, not byte-level

[R-SER-08]: "A reader that neither detects the violation nor rejects the tile, and returns the value, MUST report 0x00 as false and every other byte as true." Literal antecedent excludes a reader that detects, does not reject, and serves. But the document decides it elsewhere: §19.4 step 8: "`[R-SER-08]` fixes what a reader returns for the one byte a conforming file cannot"; [R-TYP-04]: "the one case where a reader resolves a byte to a value rather than passing it through arises only in a nonconforming file, and `[R-SER-08]` states it"; §21.1: "it resolves a nonconforming interleaved boolean byte to a value rather than serving it through". Three places attribute an unconditional return rule to [R-SER-08]; only its own antecedent is narrower. Not byte-level: file nonconforming under every reading, no emitted byte, no accept/reject; what is at stake is a served sample value in a nonconforming file, and the three cross-references fix it. Repair: "A reader that does not reject the tile and returns the value MUST report …".

### wrt08-drop-on-added-record (adversary-02) — PARTIAL, editorial, not byte-level (downgrade of the reporter's flag)

Cell: "An appender MUST NOT drop it except in a commit that *independently* changes the scope the record attaches to: … for a top-level record, the file's layer set, any layer record's content, or another *non-layer* top-level record. A commit changes the layer set by adding a layer; an appender never removes one … Dropping the record, or dropping another record in the same commit, is not itself such a change, so a commit whose only effect would be the drop MUST retain it."

Premise of the downgrade, stated so it can be attacked: the colon introduces a closed definition of "changes the scope", and "changes … another non-layer top-level record" describes modifying a record that exists in the superseded generation, not bringing one into existence. The same cell, where adding was meant, said so in terms of the *set* ("changes the layer set by adding a layer"); for non-layer records it named the record, not the set. Adding M therefore satisfies none of the three, and P's drop is barred by the letter. I tested the reporter's construction: both outputs are conforming files (X's extent falls to slack, no row); the fork is in the appender's licence, and both P and Q are readers who can defend nothing from the bytes alone. Implementer consequence if (ii) were competent: P's directory lacks X's 24-byte header, Q's carries it — a real byte difference from identical input. I judge (ii) requires reading "changes a record" as "creates a record", which the cell's own contrast with the layer-set sentence does not support; the reporter also picks (i) and rates the fork low. Because the contrast is the only thing deciding it, the repair is one clause: "Adding a non-layer top-level record is not a change to another such record and licenses no drop." This is the group I would most want a second reading on after group 1.

### cod11-dead-cannot-establish-ground (adversary-03) — PARTIAL, editorial, not byte-level

[R-COD-11]'s own last sentence already says it: "For a conforming reader that position arises only at a reserved or experimental value, every assigned codec and filter being core: it rejects the layer (`[R-COD-03]`, `[R-COD-09]`)". L43/L45 are reader-detected rows, and [R-CNF-11]: "a verifier that has established any violation reports *nonconforming*, however many requirements it was unable to check". So the verdict word is decided: nonconforming. What is true in the finding is that §2.3's ground list carries an item a conforming verifier never uses. Not byte-level: neither verdict certifies, the file is nonconforming under every reading, and the register row does not move. Repair: in §2.3, qualify the ground — "when it cannot execute a codec or filter (`[R-COD-11]`, a position a conforming verifier reaches only at a value `[R-COD-03]` already rejects)" — or drop it.

### sec216-crossref-bound-declines (register-03) — CONFIRMED, register-bookkeeping, not byte-level

§21.5 closes with "§21.6 lists the ignore-record conditions that are not violations", two sentences after naming the bound/window declines as ignore-record and "not a fact about the file". §21.6 has two ignore-record non-violations (experimental record type MU = 0; experimental encoding) and no row for the over-bound document or over-bound window. §21.1 exempts §21.6 from completeness, so it is an under-delivering cross-reference. Not byte-level: §18.2 states the behaviour ("ignore-record like any other it cannot read"; "no violation") and §21.9 the licence, so an implementer who looks in §21.6 and finds nothing still has the rule. Repair: add a §21.6 row — "A user-metadata document's decoded size, or its frame's declared Window_Size, exceeds the reader's bound (no smaller than §21.9's) | ignore-record on capability grounds, or an `[R-ERR-04]` decline; the file is conforming | `[R-MTA-09]`, `[R-ERR-04]`".

## Byte-level count: 1 (planar-pq-designation).
