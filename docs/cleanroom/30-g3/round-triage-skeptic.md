# Round 30 triage — skeptic lens — working transcript

## What I read

- `spec/tarn.md` (4743 lines): §2 whole; §4 whole; §5 whole; §6 whole; §7 whole; §9 whole; §10 whole; §11–§13 whole; §14 whole; §17 whole; §18 whole; §19 whole; §20 whole; §21 whole; §22 whole; Appendix G and H whole. Plus greps for "designat", "ascending", "lexicograph".
- No walk transcripts. No directory listing of `r30-round/out` or of anything else (I opened nothing by listing; every read was by path or by grep/sed on `spec/tarn.md`). Two of my own `sed` outputs were auto-persisted by the harness to its tool-results directory and I re-read those files; they contain only spec text.
- Not read: docs/, PLAN.md, AGENTS.md, conformance/, registry.json, git history, web, any other triage pass.

## Grouping

| group | members |
|---|---|
| planar-pq-designation | reader-01 |
| cnf02-closed-list-vs-barriers | reader-02, writer-03, verifier-04 |
| retype-makes-tile-nonconforming-wording | reader-03 |
| l23-name-overrun-tier | reader-04, register-02 |
| key-order-proper-prefix-undefined | writer-01 |
| appg-item8-vs-closing-compactor-floor | writer-02, diagrams-01 |
| unassigned-encoding-two-senses | verifier-01 |
| err04-note-denies-record-scope | verifier-02, register-01 |
| partial-total-after-file-scope-rejection | verifier-03 |
| discard-clause-buried-in-parenthetical | quiz-01 |
| s215-cross-reference-to-s216-under-delivers | register-03 |
| ser08-detecting-serving-reader | adversary-01 |
| pe0-drop-on-added-toplevel-record | adversary-02 |
| cod11-ground-unreachable-by-conforming-verifier | adversary-03 |

14 groups, 19 ids. verifier-03 and quiz-01 both live in [R-CNT-21]'s discard clause but name different defects (a gap for file-scope rejections vs. a presentational hazard for the layer case), so they stay apart.

## Judgements

### planar-pq-designation (reader-01) — byte-level flag DOWNGRADED; the group I tried hardest to kill

Reporter's fork: is P·Q a designated [R-ENC-04] quantity of a *planar* layer? Reading (i) yes (every product §14.2 writes is designated for every layer); reading (ii) no (the designated quantity is the layer's decoded size, which is P·Bᶜ under planar).

Construction checked: planar, one dimension E = 0, T = 2^52, C = 4096 uint8, codec 1. P = 2^52, N = 0, C·N = 0, N·P = 0, entry_count = 0, slot (0,0). P·Bᶜ = 2^52 in domain; P·Q = 2^64 out. No §21.9 row is exceeded (no addressed tile). Under (ii) the file is conforming and inside the guarantees so [R-CNF-03] obliges acceptance; under (i) L2 fires. The example holds; the fork is real iff reading (i) is competent.

Text that decides it, in my judgement:

1. [R-ENC-04]: "A designation is express, made by the section that defines the quantity; an expression this specification writes only inside a comparison, and names nowhere, is not a designated quantity and no reader is obliged to form it." §14.2 defines P·Q as one thing: the decoded size of an interleaved tile (table row "interleaved | P · Q"). It defines no planar quantity whose expression is P·Q.
2. [R-SER-07]: "decoded size is a function of the layer's declarations alone — geometry, layout, and channel types ... Every decoded size, and the value count V, is a declaration-derived quantity under [R-ENC-04]." Layout is an input; a planar layer's decoded sizes are P·Bᶜ and ⌈P/8⌉.
3. §19.3 [R-RDR-03] states the reader's layer-access obligation as "the 2⁶³ − 1 ceiling on every quantity that arithmetic derives ([R-ENC-04]) and on the decoded sizes §14 derives from it ([R-SER-02], [R-SER-07])" — it characterises [R-SER-02]'s designation as *the decoded sizes*, which are per-layout.
4. §21.1's convention: "Where the quantity a condition derives varies by layout, the layout formulas are materially different shapes and the cell enumerates them." L2's "P·Q ...; P·Bᶜ" is exactly such an enumeration, and its parenthetical "P·Q (which dominates V = P·C)" pairs P·Q with the *interleaved* value count — under reading (i) a planar layer would be obliged to form V = P·C, which [R-SER-01] says is not a planar layer's V (V = P). Reading (i) makes the cell contradict [R-SER-01]; reading (ii) makes everything consistent.

Premise my downgrade rests on (attackable): "These products and sums are declaration-derived quantities" in §14.2 designates, for a given layer, the products the table gives for that layer's layout — not every product the table writes. What supports the reporter's (i): the sentence is layout-unqualified; L2's cell is untagged where L44/T3/T14/T21/T22 are tagged; §17.2's Note says "P·Q and P·Bᶜ are checked in an empty layer" without a layout word. None of those three is a normative statement that P·Q is a planar quantity, and points 1–4 above are.

Grade: PARTIAL (the text decides (ii), but the designating sentence and L2's cell are loose enough that the pin is worth one edit), editorial, not byte-level. Repair: §14.2 "These products and sums are declaration-derived quantities under [R-ENC-04] for the layout the layer declares — P·Q and the interleaved offset in an interleaved layer, P·Bᶜ and k·Bᶜ in a planar one"; tag L2's instances "interleaved P·Q (which dominates V = P·C); planar numeric P·Bᶜ" to match the sibling rows.

### cnf02-closed-list-vs-barriers (reader-02, writer-03, verifier-04)

[R-CNF-02] has two categories. Category 1: "A few obligations this specification places on writers govern their *conduct* rather than their output — where a value is published, or which registry version a writer targets (§10.3, §18.3) — and a file is never nonconforming by virtue of one". Category 2: "A writer obligation whose violation this specification expressly declares not to be a file-conformance violation binds the actor in the same way; §6.3's flags = 0 ... and §6.2's pre-trailer gap ... are the cases this text states". The two category-2 cases are *output* obligations (a byte value; a gap length) whose violation is declared not a file violation. §9.2 puts the barriers in category 1 in so many words: "Steps 4 and 6 bind a writer's **conduct** rather than its output, and are declared so here on the model [R-CNF-02] states". Its last sentence ("the file it produces is not nonconforming on that account") restates category 1's consequence ("a file is never nonconforming by virtue of one"). So the count of two is a count of category 2 and is not falsified. Reporters' form-based reading (any express declaration = category 2) would collapse category 2 into category 1, since §2.3 itself expressly declares every conduct rule harmless to the file.

But the §9.2 sentence does mirror category 2's form closely enough to invite the misreading, and nothing turns on it ("binds the actor in the same way"). Grade: PARTIAL, editorial, not byte-level (all three reporters agree; barriers leave no trace in bytes — §9.2: "a file committed without one can be byte-identical to a file committed with it"). Repair: §9.2 "...and are declared so here as [R-CNF-02] declares of every conduct rule: ..." — or in §2.3 make category 2 say "output obligation".

### retype-makes-tile-nonconforming-wording (reader-03)

§20.3: "Where a change does reach them it makes each stored tile it reaches nonconforming". Checked: re-type int8→uint8 with no padding positions, same element size, fill bytes unchanged. Every stored byte is a valid uint8 ([R-TYP-05]); decoded size unchanged so T3/T14 do not fire; T4 does not fire (fill bytes unchanged). No row applies. [R-CNF-02]: "File conformance is a pure predicate on bytes". §21.7 calls the parallel cases (mis-strided filter, undisclosed dictionary) "a writer violation whose consequence is wrong decoded content" and says such a file is one "that every checksum in §8 certifies" — the document's own practice is to call these writer violations, not nonconforming tiles. The §20.3 sentence overstates: the tile is nonconforming only where the re-type changes the decoded size (T3, T14). The bar itself is unaffected. Grade: CONFIRMED, editorial, not byte-level (reporter's own rationale; §21.7 makes the condition unwitnessed, so no verdict or served value moves). Repair: "...it makes the stored bytes of each tile it reaches denote values the writer did not store — a violation the file witnesses only where the decoded size changes (T3, T14) and otherwise carries unwitnessed (§21.7) — and re-emitting those tiles would strand...".

### l23-name-overrun-tier (reader-04, register-02)

§19.1 step 4: "a layer record whose name field does not lie entirely within that record's inline_length yields no name field to compare, so it contributes no name to the namespace and is instead a validity error at layer scope ([R-CNT-18])" — established at open. §19.2: "at open: ... the directory region and its record walk, and the layer-name namespace (§19.1's steps)". L23's first instance "leading fixed fields (name … C)" says Detected = layer access. Note the register already places every other layer-name check at open (L3, L5, L6 Detected = open); L23's name sub-case is the outlier. §21.1: "where a row and the rule it cites diverge, the rule governs" — decided; the cost is a reader building from the table. Grade: CONFIRMED, register-bookkeeping, not byte-level ([R-RDR-02]: "A reader MAY detect any violation earlier"; same outcome either way). Repair: split L23's first instance — "name (open, §19.1 step 4); layout … C (layer access)".

### key-order-proper-prefix-undefined (writer-01)

Searched: "ascending order of their keys' UTF-8 bytes" (§18.2, F27, L48), "ascending layer-name byte order" (App. G item 3), "compared lexicographically" (App. G item 3, another key). No sentence defines the order of a proper prefix against its extension. Confirmed absent. Not byte-level: the phrase "ascending order of ... bytes" has one standard meaning for byte strings (lexicographic, proper prefix first — memcmp/strcmp order, which is also code-point order for UTF-8); shortlex is a distinct named order nobody derives from that phrase. Premise (attackable): no competent implementer reads length-first from "ascending order of their keys' UTF-8 bytes". Grade: CONFIRMED (undefined), editorial. Repair: §18.2 "in ascending order of their keys' UTF-8 bytes, compared lexicographically with a proper prefix ordering first"; same clause in App. G item 3.

### appg-item8-vs-closing-compactor-floor (writer-02, diagrams-01)

Item 8: "The version_minor floor binds a compactor too, save where its output carries a feature it does not implement, when §20.5's floor governs instead ([R-WRT-06])." Closing paragraph: "version_minor at its floor, which [R-CNT-26] states as a SHOULD — item 8's creator's rule, not a compactor's (§20.5)". These contradict. Normative text sides with item 8: §20.5 "Otherwise version_minor follows [R-CNT-26]'s floor"; [R-CNT-26] binds "A writer". Non-normative appendix ([R-CNF-01]); version_minor is descriptive ([R-ENC-16]); readers never gate ([R-CNT-07]); SHOULD deviation is outside the register ([R-CNF-12]). Grade: CONFIRMED, editorial, not byte-level. Repair: closing paragraph → "version_minor at its floor, which [R-CNT-26] states as a SHOULD — binding a compactor too, save §20.5's carried-feature case (item 8)".

### unassigned-encoding-two-senses (verifier-01)

[R-MTA-03]: "1 = none and 2 = zstd are assigned; 3 through 0x7F are reserved; values ≥ 0x80 are the experimental range" and "An encoding a reader does not implement is therefore one this specification does not assign". §21.5: "Encoding 0 and a reserved-range value are unassigned too, and R1 registers both as violations". §2.3's "certification is unaffected" and §17.4's "not a violation" are, read at their widest, false for 0 and reserved. But the rule they cite decides it: [R-MTA-10] — "file conformance ... is decided by the structural checks that precede the document alone: the record's framing and extent slot ([R-CNT-13]), the encoding byte's own value set ([R-MTA-03]), and the extent's terminal CRC" and "A verifier meeting such a record in an otherwise conforming file has no requirement it is unable to check" — a file carrying encoding 0 is not otherwise conforming (R1). §17.4 also says "in a conforming file". Every verifier applies R1 as a reader obligation ([R-CNF-11]: verifiers "inherit every reader obligation"). Grade: PARTIAL (loose word, decided by the cited rule), editorial, not byte-level. Repair: in §2.3 and §17.4 write "an experimental-range encoding" or append "(the encoding byte's own value set is checked as any structural field, [R-MTA-03], R1)".

### err04-note-denies-record-scope (verifier-02, register-01)

[R-ERR-04]: "a reader MAY decline it — at the whole file, or at the narrowest scope whose stated or derived quantities exceed what it can serve: a layer, a tile, or the record carrying a user-metadata document, as §18.2 assigns." §18.2 body (window bound): "ignore-record on that ground — the reader's capability ... the file exceeds a §21.9 guarantee and so remains conforming while the reader MAY decline it ([R-ERR-04])" — the record-level ignore-record *is* the [R-ERR-04] decline. §18.2 Note (size bound): "a reader that instead declines on resource grounds under [R-ERR-04] does so at the whole file, a document having no declared size and so no narrower scope whose stated or derived quantities that rule can measure". The Note denies the record scope the rule names. Direct divergence; the Note is non-normative ([R-CNF-01]) and the rule governs. Behaviours coincide under both texts (ignore the record, or refuse the file); only the report label ([R-ERR-04]'s "MUST be reported as a resource limit") differs. Grade: CONFIRMED, editorial, not byte-level. Repair: rewrite the Note's sentence — "A reader that declines the record on resource grounds takes ignore-record for that record — the narrowest scope [R-ERR-04] names for a document, as this section assigns — and reports it as a resource limit; it MAY instead decline the whole file."

### partial-total-after-file-scope-rejection (verifier-03)

[R-CNT-21] owes a total whenever a live trailer is established ("Where §6.2's ordered validation rejects the file before a live trailer is established there is no F and no live state to walk, so the total is not owed at all" — the only exemption). The discard clause is expressly layer-scoped: "the claimants it had already enumerated are discarded with the layer". The composition rule is literal: "A partial total is F less the bytes claimed by the claimants the walk did enumerate". For F33/F7 (walk-established reject-file) the literal text gives reading (b): keep every enumerated claimant. So the text decides (b); the reporter's (a) is an extrapolation from the rationale clause. But the rationale ("the total is a claim about a live state one of whose layers is not usable") applies a fortiori to a live state none of which is usable, and the text says nothing for that case, so two verifiers can defensibly differ on a reported integer. Grade: PARTIAL, editorial, not byte-level (reporting figure on an already-nonconforming file; [R-CNF-12] "a verifier certifies only violation-free files"). Repair: add after the discard clause: "where the walk itself establishes a file-scope rejection (F7, F33), every enumerated claimant but the front block and the live trailer is discarded on the same ground and the partial total is F − 80" — or state expressly that the literal composition stands. Maintainer's choice; either sentence closes it.

### discard-clause-buried-in-parenthetical (quiz-01)

The discard sub-rule sits inside a parenthetical inside an em-dash clause of one long sentence. Fully decidable (reporter and I agree). Grade: CONFIRMED as a presentational hazard, editorial, not byte-level. Repair: lift the discard clause into its own sentence following the composition rule.

### s215-cross-reference-to-s216-under-delivers (register-03)

§21.5: "§21.6 lists the ignore-record conditions that are not violations." §21.6's table has the experimental record type (MU = 0) and the experimental document encoding; it has no row for a document over the reader's decode bound or a frame over its window bound, both of which §18.2 makes "ignore-record ... and no violation" and §21.5 itself names two sentences earlier. §21.1 exempts §21.6 from the completeness clause, and §2.3 routes the guarantee-excess family to [R-ERR-04] ("§21.9's [R-ERR-04] governs a refusal on that last ground; §21.6's closing paragraph names the other two"), so behaviour is fully stated — the cross-reference over-promises. Grade: CONFIRMED, editorial, not byte-level. Repair: either soften §21.5 ("§21.6 lists the ignore-record conditions that are not violations; the two declines above are §21.9's subject") or add a §21.6 row: "A user-metadata document's decoded size, or its frame's Window_Size, exceeds the reader's bound (each ≥ §21.9's guarantee) | Ignore-record on the reader's capability; the file is conforming; [R-ERR-04] governs a resource decline and its report | [R-MTA-09], [R-ERR-04]".

### ser08-detecting-serving-reader (adversary-01)

[R-SER-08]'s antecedent is "A reader that neither detects the violation nor rejects the tile, and returns the value" — R3 (detects, does not reject, serves) is outside it. Deciding text: [R-TYP-04]: "Writers and readers MUST NOT alter a value's encoded bytes in storing, decoding, or returning it ... the one case where a reader resolves a byte to a value rather than passing it through arises only in a nonconforming file, and [R-SER-08] states it." A reader returning 0x02 as *false* alters the bytes in a way [R-SER-08] does not state and so breaks [R-TYP-04]; the only resolution [R-TYP-04] admits is [R-SER-08]'s (0x00 false, else true). §21.1 states the same unconditionally: "it resolves a nonconforming interleaved boolean byte to a value rather than serving it through". So R3's return is fixed at true. Grade: PARTIAL (antecedent narrower than intent; closed by [R-TYP-04]), editorial, not byte-level (file nonconforming under every reading; no emit/accept/reject verdict moves). Repair: "A reader that returns the value — whether or not it detected the violation, and having not rejected the tile — MUST report 0x00 as false and every other byte as true."

### pe0-drop-on-added-toplevel-record (adversary-02) — byte-level flag UPHELD

§20.4 MU = 0 / PE = 0 row: "An appender MUST NOT drop it except in a commit that *independently* changes the scope the record attaches to: ... for a top-level record, the file's layer set, any layer record's content, or another *non-layer* top-level record. A commit changes the layer set by adding a layer; an appender never removes one ... Dropping the record, or dropping another record in the same commit, is not itself such a change, so a commit whose only effect would be the drop MUST retain it."

Construction checked: gen 1 = layer A + top-level experimental record X (0x8001, MU = 0, PE = 0; conforming per §21.6). Commit 2 adds the file's first user-metadata record M and re-emits the directory. Nothing else changes. Is "adding M" a change to "another non-layer top-level record"?

Hunted for the deciding sentence and did not find one:
- "A commit changes the layer set by adding a layer" states that additions count *for the layer-set item*; there is no parallel sentence for records, and the record item is phrased "another non-layer top-level record", not "the set of non-layer top-level records". Expressio unius → reading (i), adding is not listed.
- Against that: the layer item says "any layer record's *content*" while the record item says "another non-layer top-level record" without "content" — the asymmetry in *this* pair suggests the record item is broader than content, and a record that goes from absent to present is a changed record in that broader sense → reading (ii). The stated principle ("independently changes the scope the record attaches to") is satisfied by adding M as much as by modifying one, and no reason for the layer/record asymmetry is offered.
- "Dropping ... another record in the same commit, is not itself such a change" addresses dropping only; its rationale (a drop needs its own licence) does not transfer to adding.
- §20.4's Rationale distinguishes "modified, added, or dropped" as three verbs, and the document uses "logically modify" for changes to existing records — but the table says "changes", not "modifies".

Byte-level test: under (ii) a conforming appender may emit the directory without X's header (X's extent to slack); under (i) it may not ([R-CNF-06]: an updater "MUST honor the preservation obligations of §20.4"). Both outputs are conforming files, so no reader/verifier verdict moves — but the *emittable set of a conforming updater* from identical input and identical requested edit differs, which is the first prong of the test, and the divergence is observable to X's owner. Retaining is always licensed, so real forks need an appender that wants to drop and reads (ii); the reporter's low-plausibility caveat is fair, but the text does not decide it. Grade: CONFIRMED, byte-level, byte_level = true. Repair is a maintainer decision: either (ii) "for a top-level record, the file's layer set, any layer record's content, or the file's set of non-layer top-level records or any such record's content — adding or replacing a record changes that set" or (i) "...or the content or extent of another existing non-layer top-level record; adding a record is not such a change". I would recommend (ii), which is what the stated principle supports and is symmetric with the layer clause.

### cod11-ground-unreachable-by-conforming-verifier (adversary-03)

[R-COD-11]'s own next sentence says what the reporter derives: "For a conforming reader that position arises only at a reserved or experimental value, every assigned codec and filter being core: it rejects the layer ([R-COD-03], [R-COD-09])", and [R-CNF-11] fixes the verdict: "a verifier that has established any violation reports *nonconforming* ... *cannot establish* is available only to a traversal that established no violation". Decided in the same paragraph. The residue is that §2.3's "as when" list of cannot-establish grounds names one no conforming verifier can reach, and [R-COD-11]'s "no violation *elsewhere*" could be read as excluding the L43 violation at the same layer, which [R-CNF-11]'s wording (no "elsewhere") does not. Grade: PARTIAL, editorial, not byte-level. Repair: drop "elsewhere" in [R-COD-11] (and in [R-MTA-09]'s parallel sentence), and in §2.3 qualify the codec ground "— reachable only by software that is not a conforming reader ([R-COD-11])".

## Byte-level count: 1 (pe0-drop-on-added-toplevel-record)

## Coverage count

reader-01, reader-02, reader-03, reader-04, writer-01, writer-02, writer-03, verifier-01, verifier-02, verifier-03, verifier-04, diagrams-01, register-01, register-02, register-03, adversary-01, adversary-02, adversary-03, quiz-01 — 19 ids; group member counts 1+3+1+2+1+2+1+2+1+1+1+1+1+1 = 19.
