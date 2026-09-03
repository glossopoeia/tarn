# Cleanroom round 30 — refute-phase verdicts

The refute phase fired on two split verdicts. Both refuters ran on the fallback model (the recorded remedy for refute-shaped briefs, which the driver refuses); a verdict in the direction that clears the gate is provisional until hand-checked, and both were.


## planar-pq-designation — Whether P·Q is an [R-ENC-04]-designated quantity of a planar layer is not fixed by §14.2, and L2 restates it untagged


**Verdict:** DOWNGRADE_STANDS


### Disclosure

I read only /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md, via Read (offsets 1970-2070, 2440-2514, 2948-2988, 3575-3665, 3715-3745, 3772-3786, 3961-4052, 1600-1690, 1938-1969, 2074-2103, 1071-1183, 447-484) and via `grep -n` over that same file for section headers, "R-ENC-04|R-CNF-03|R-SER-07|R-COD-07|R-RDR-03|R-SER-02|R-CNF-05", and "P·Q". I ran no code and consulted no other file. I created the scratch directory /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-round/scratch/refute-planar-pq-designatio/ but wrote nothing into it — all analysis was arithmetic done in my head from the table values (P=2^52, C=4096, Bᶜ=1, Q=4096, P·Bᶜ=2^52, P·Q=2^64), which I verified: 2^52 × 4096 = 2^52 × 2^12 = 2^64, and I confirmed 2^64 > 2^63−1 while 2^52 < 2^63−1. No project instructions, memory files, or other context material influenced this analysis beyond what the system reminders already placed in context (a TARN-project memory index and CLAUDE.md pointer to AGENTS.md) — I did not open AGENTS.md or any memory file, and none of that material bears on the P·Q question, so I disregarded it. No path substitution was needed; spec/tarn.md was exactly where the brief said.


### Sections opened

§11.1-11.3 (Geometry and its validity floor, Grid arithmetic, Uniform tiles); §14 preamble, §14.1 (The value sequence), §14.2 (Byte layout and decoded size, in full), §14.3 (Packed boolean planes), §14.4 (Layout–type validity); §17.2 Codecs (R-COD-06, R-COD-07 body and both its Notes, R-COD-08); §19.3 (Layer access); §21.1 (How to read the register, in full); §21.3 rows L1-L23 including L2 and L21 in full, plus L44's row via grep; §21.4 preamble and rows T1-T5 plus T3/T14/T21/T22 via grep; §21.9 (Implementation limits); §7.4 (The layer record, field table); §4.2 (Integer types and domains, R-ENC-03 through R-ENC-06).


### Reasoning

The finding's construction is arithmetically sound as far as it goes (planar, rank 1, E=0, T=2^52, C=4096×uint8 gives P·Bᶜ=2^52 in-domain and P·Q=4096·2^52=2^64 out-of-domain, with zero addressed tiles so no §21.9 or T-scope row is reached) — I don't dispute the arithmetic. What I don't accept is the premise that no text decides whether P·Q is an R-ENC-04-designated quantity of a *planar* layer at all.

First, the structural facts of §14.1 and §14.4 already answer the question directly, independent of the designation sentence's wording. §14.1 defines the planar tile as inherently single-channel: 'the tile with disk ordinal c·N+s carries exactly the values of channel c... the sequence has V = P values,' against interleaved's 'V = P·C values.' §14.4 then states 'planar layers carry any mix of channel types, each channel's plane serializing under §14.2 or §14.3 by its type alone' — planar serialization is defined per-channel, through Bᶜ alone; Q (the *sample* stride) has no referent for a structure that never assembles a sample. R-ENC-04 itself gates on this: 'A designation is express, made by the section that defines the quantity' — and the section (§14.2's table) defines P·Q only in the interleaved row and P·Bᶜ only in the planar row. The designation sentence that follows ('These products and sums are declaration-derived quantities under [R-ENC-04]') is naturally read as blessing the quantities the table has just scoped, not as creating a new, layout-blind quantity the table itself never assigns to planar.

Second, §21.1 supplies the register's own rule for exactly this kind of surface inconsistency: 'each row *restates* its governing rule... and where a row and the rule it cites diverge, **the rule governs**,' and separately, 'Where the quantity a condition derives varies by layout, the layout formulas are materially different shapes and the cell enumerates them.' L2's governing rule is R-ENC-04, restating R-GEO-03/R-CNT-13/R-SER-02/R-SER-07 — so even if L2's own Instances cell is imprecisely worded, the governing rules (already shown above to be layout-scoped) win.

Third, and most decisively: every other row in the register that ever lists P·Q ties it to layout, without exception — L44: 'interleaved P·Q; planar numeric P·Bᶜ; packed planar bool ⌈P/8⌉'; T3: 'interleaved P·Q, payload longer; ... planar numeric P·Bᶜ, payload longer; ...'; T14, T21, T22 identically. §17.2's own R-COD-07 body (the rule L44 restates) says outright: 'in a planar layer each channel's plane carries its own decoded size (§14.2, §14.3), and the largest governs' — no P·Q anywhere in a planar layer's accounting. Six rows total touch this quantity (L2, L44, T3, T14, T21, T22); five of six explicitly tag it 'interleaved.' The sixth (L2) is the outlier, and the plain reading is that its list simply omits the layout tags its siblings all carry, not that it silently redefines the quantity's scope.

The finding's own textual anchor for reading (i) — 'L2's cell lists P·Q... P·Bᶜ untagged beside N, P, N·P and C·N, which are computed for every layer' — does not hold up. C·N is not computed for every layer: L21 states the addressed-tile-count condition as '(N interleaved, C·N planar)' and enumerates its instances as 'interleaved N, entry_count larger... planar C·N, entry_count larger...' C·N is exactly as layout-exclusive (planar-only) as P·Q is (interleaved-only) and P·Bᶜ is (planar-only); only N, P, and N·P are genuinely layout-independent (§11.2 defines them with no layout branch at all). Once C·N is recognized as planar-only despite appearing untagged in the same list, the untagged-ness of L2's cell stops supporting a layout-blind reading of P·Q — it is simply L2's terser style for the same layout-partitioned set its five sibling rows spell out explicitly.

Fourth, §19.3 already points the same way — 'the 2⁶³−1 ceiling on... the decoded sizes §14 derives from it' names 'the decoded sizes §14 derives,' i.e., whichever one formula §14 actually produces for the layer's declared layout, not the union of both rows' formulas — and the finding itself cites this as reading-(ii) support without finding a way past it.

Putting these together: the disputed construction is conforming under the single reading the text actually supports (reading ii). A planar layer's L2-checked quantities are N, P, C·N, P·Bᶜ, and the entry_count formula; P·Q is not among them because §14.1/§14.4 never produce it for a planar tile and no governing rule (as opposed to a terse register cell) ever designates it there. There is no second, equally supported reading under which a conforming writer's obligations or a conforming reader's accept/reject verdict differs — so nothing here moves the emittable set. I looked for, and could not construct, any file where the two readings actually diverge in outcome once the governing sections are read together; the apparent fork lives only in L2's compressed phrasing, not in the rules it restates.


### Decisive quotations

§14.1: "Planar — the tile with disk ordinal c · N + s (§11.4) carries exactly the values of channel c at the tile's P positions... the sequence has V = P values." / "Interleaved — the tile at spatial ordinal s carries all C channels at the tile's P positions, sample-major... the sequence has V = P · C values."

§14.4 (`[R-SER-09]`): "planar layers carry any mix of channel types, each channel's plane serializing under §14.2 or §14.3 by its type alone... A reader MUST NOT reject a layer for its combination of layout and channel types."

§17.2, R-COD-07 body: "Writers MUST NOT declare this codec for a layer any of whose addressed tiles' decoded size exceeds 0x7E000000 bytes... in a planar layer each channel's plane carries its own decoded size (§14.2, §14.3), and the largest governs."

§21.1: "each row *restates* its governing rule... and where a row and the rule it cites diverge, **the rule governs**." / "Where the quantity a condition derives varies by layout, the layout formulas are materially different shapes and the cell enumerates them."

L21 row (§21.3): "entry_count does not equal the geometry-derived addressed-tile count (N interleaved, C·N planar) | interleaved N, entry_count larger; interleaved N, entry_count smaller; planar C·N, entry_count larger; planar C·N, entry_count smaller"

L44 row (§21.3): "Instances: interleaved P·Q; planar numeric P·Bᶜ; packed planar bool ⌈P/8⌉"

T3 row (§21.4): "The decoded payload's byte length is not exactly the tile's decoded size derived from the layer's declarations | interleaved P·Q, payload longer; interleaved P·Q, payload shorter; planar numeric P·Bᶜ, payload longer; planar numeric P·Bᶜ, payload shorter; ..."

§4.2, R-ENC-04: "A designation is express, made by the section that defines the quantity; an expression this specification writes only inside a comparison, and names nowhere, is not a designated quantity and no reader is obliged to form it."


## pe0-drop-on-record-add — §20.4's PE = 0 cell addresses adding a layer and dropping a record but not adding a non-layer record; the letter reads as not licensing the drop


**Verdict:** DOWNGRADE_STANDS


### Disclosure

Read only /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md (4743 lines total). Ran grep against that single file for: "20.4" (to locate the section), "R-CNF-05|R-WRT-08|R-CNT-22" (to check cross-references), and "changes the\|change the\|modified, added\|modifies\b" (to survey how the document uses "changes"/"modifies" elsewhere, to test whether the disputed clause's verb choice is idiosyncratic or consistent with the rest of the document). Read §20.4 in full (lines 3371-3570, "Re-emission and preservation" through the start of §20.5/compaction and its rationale/examples) and the R-SLB-04 paragraph at lines 2318-2332. No other files were read; no git history, no ADRs, no conformance vectors. I did notice project context (CLAUDE.md pointer to AGENTS.md, a MEMORY.md index naming prior TARN-round issues like "lineage gate word list" and "repair prose vs rules") appear in my system context before I began — I did not open AGENTS.md or any memory-linked file, and none of it entered my reasoning about the spec text; I disregarded it per the brief's instruction and am naming it here only because it appeared. Wrote one scratch file, notes.md, in /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-round/scratch/refute-pe0-drop-on-record-a/, containing my analysis (no code/CRC needed for this finding — it turns on textual construction, not byte arithmetic). Did not read the shared round output directory.


### Sections opened

§20.4 "Re-emission and preservation" in full, including the MU/PE table (all three flag rows), the paragraph following the table ("No commit therefore removes a layer record..."), the R-WRT-08 sentence, and the Rationale block immediately after it (lines 3371-3429); the start of §20.5 "Compaction" through its rationale and worked example (lines 3430-3570), to confirm the compactor's unrestricted drop license is a separate, unambiguous case not implicated by this dispute; and the R-SLB-04 paragraph (lines 2318-2332) for cross-document usage of "changes the [X] set" as a membership-change idiom.


### Reasoning

The disputed clause (§20.4, MU=0/PE=0 row) licenses an appender's drop of an unimplemented top-level PE=0 record only in a commit that "independently changes the scope the record attaches to: ... for a top-level record, the file's layer set, any layer record's content, or another non-layer top-level record." The finding's premise is that "changes ... another non-layer top-level record" requires modifying an existing record's content, not merely adding a brand-new one — so a commit that adds a new non-layer top-level record (without touching the layer set or any layer's content) would not license dropping some other PE=0 top-level record, under the letter.

To refute the downgrade I needed a conforming input file and a commit construction where reading (i) [letter: "changes" = content-modification of an existing record] and reading (ii) [loose: "changes" includes "adds a new record"] disagree on whether the resulting output is conforming — i.e., whether a conforming appender may emit it. I tried exactly the construction the finding turns on: input has a required layer L1 (PE=1, untouched) and an unimplemented top-level record R (MU=0, PE=0); commit adds a new non-layer top-level record R2 and drops R, touching neither the layer set nor L1's content. Under reading (i) this output is barred (R's drop isn't independently licensed); under reading (ii) it would be licensed. This is the shape of a byte-level fork if, and only if, reading (ii) is a genuinely plausible reading of the text.

I could not sustain reading (ii) as plausible. Three independent pieces of the same document's own usage close it off:

1. The Rationale to this same rule (line 3416) states the directory a commit emits "differs from the one it supersedes exactly by the records modified, added, or dropped" — the drafters' own vocabulary treats "modified" and "added" as distinct, mutually exclusive categories. The disputed clause's verb is "changes," which parallels "modified," not "added." If "changes" were meant to include "added," this trichotomy phrase would be redundant or misleading.

2. Wherever the document intends that adding to a collection counts as a licensing change, it uses explicit set/membership language and (for the one case in this very row) an explicit gloss: "the file's layer set" is followed immediately by "A commit changes the layer set by adding a layer." The other two top-level alternatives — "any layer record's content" and "another non-layer top-level record" — are phrased as a record's content/a record, not a set, and get no such addition-gloss. The same pattern holds for the layer-sub-record list ("the entry set of its index," "which of its tiles are stored" vs. "that layer's record"), and recurs elsewhere in the document (line 2324, §R-SLB-04: "commit changes the stored-tile set"). This is a consistent drafting convention, not an isolated phrasing.

3. The layer-sub-record analogue "that layer's record" cannot mean "a newly added layer's record" at all — a layer's record cannot be added independently of adding the layer itself (that event is already covered by the layer-set alternative). So the parallel "record" item in the top-level list is naturally read the same way: an existing record's content changing, not a new record appearing.

I also checked whether any other construction produces a genuine fork: modifying an existing other top-level record's content, adding a layer, or superseding a tile are all explicitly and identically licensed under both readings — no ambiguity there. Dropping a second record cannot serve as the license either; the text explicitly forecloses that ("Dropping the record, or dropping another record in the same commit, is not itself such a change").

Given this, the "reading (ii)" needed to make the fork real is not a plausible reading of the text — it is, as the original finding's own recommended repair concedes, "a design change to the letter," not a disambiguation of existing ambiguity. That concession from the finding itself undercuts its own byte-level claim: if admitting reading (ii) requires amending the text rather than merely reading it correctly, then under the text as it stands there is only one reading, and no fork exists. This matches the passes' downgrade rationale exactly ("Under the letter a conforming appender may not emit the drop, so the emittable set does not fork; the fork exists only if (ii) is admitted, and I do not admit it").

I was unable to construct a conforming file/commit pair where the two readings genuinely diverge on which byte sequences a conforming appender may emit, so the downgrade stands.


### Decisive quotations

"An appender MUST NOT drop it except in a commit that *independently* changes the scope the record attaches to: for a layer sub-record, that layer's record, the entry set of its index, or which of its tiles are stored; for a top-level record, the file's layer set, any layer record's content, or another *non-layer* top-level record. A commit changes the layer set by adding a layer; an appender never removes one." / "Dropping the record, or dropping another record in the same commit, is not itself such a change, so a commit whose only effect would be the drop MUST retain it." / "the directory a commit emits differs from the one it supersedes exactly by the records modified, added, or dropped" / "A writer or updater whose commit changes the stored-tile set, the run partition, the byte placement of any run..."
