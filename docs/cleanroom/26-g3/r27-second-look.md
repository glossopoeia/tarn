# Round-27 audit — second look

*The per-auditor cap of 4 left thirteen of twenty-five findings ungraded. They
were grouped into eight distinct defects and verified; the four downgraded
byte-level flags were attacked separately. Structured returns, verbatim, for
every agent that wrote no transcript of its own.*


## Group G1 — CONFIRMED, byte-level False

### Disclosure

I read only what my charter permits: the finding brief at /private/tmp/claude-501/.../case-r27audit/case/case-G1.md, the hunk file /private/tmp/claude-501/.../case-r27audit/hunk-12.diff, and /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md. Against the spec I ran `sed -n` range reads of Appendix G (lines 4300-4420), §17.3 (2400-2460), §14.1-§14.4 (1840-1990), §11.1-§11.4 (1490-1600), §12.1, and §2.1 (96-112), plus `grep -n` for "R-CNF-01", "R-GEO-01", "R-SER-02", "identity s = 1", and a whitespace-normalised `tr | grep -o "identity[^.]*"` scan of the whole file to defeat hard wrapping. I did not open docs/, PLAN.md, AGENTS.md, conformance/, registry.json, git history, full.diff, or any other hunk file, and did not list the case directory.

Unrequested context did appear in my context before I began: a project-instruction pointer (CLAUDE.md -> AGENTS.md) and an index of the maintainer's auto-memory files naming TARN working practices, a register/corpus relationship, and prior workflow failure patterns. I did not open any of those files and drew no conclusion from their contents; every finding below rests on lines I read in spec/tarn.md itself. The task prompt also narrated a "repair-in-the-preceding-repair" pattern; I treated that as framing, not evidence, and tested the arithmetic independently.

### Reasoning

QUOTATION CHECK. Accurate. The current file at lines ~4392-4398 reads exactly: "**A fixed filter value** likewise: §17.3 leaves the choice to the writer, it changes the stored bytes of any tile whose shuffle stride exceeds 1 — §17.3 makes it the identity where the stride is 1, as for a packed boolean plane — and no content implies it, so two writers agreeing on everything else still disagree on bytes without it pinned." The hunk shows the pre-repair text was "changes the stored bytes of every tile it touches", so the repair did narrow an unconditional universal to a stride-keyed one. Nothing is truncated in a way that changes meaning.

ARITHMETIC CHECK, done myself. [R-COD-10] (§17.3): "Viewing the image as n = L/s consecutive groups of s bytes, the filtered image places byte i of group j at offset i · n + j". Substituting n = 1: the only group is j = 0, and byte i lands at i·1 + 0 = i. That is the identity permutation for every value of s, not only s = 1. The inverse half agrees: "restores byte i · n + j to offset j · s + i" gives i -> 0·s + i = i.

REACHABILITY CHECK. [R-SER-02] (§14.2) gives decoded size P · Bᶜ for a planar numeric channel and P · Q for an interleaved tile. §17.3 sets s = Bᶜ (planar) or s = Q (interleaved). So n = L/s = P in both layouts. §11.2 [R-GEO-03] defines P = ∏ Tᵢ, and §11.1 [R-GEO-01] requires only "a tile extent Tᵢ ≥ 1" — writers are barred from "any tile extent 0", not from 1. A layer with every tile extent 1 therefore has P = 1, hence n = 1, hence filter 2 emits bytes identical to filter 1 on every one of its tiles at any stride. Such a layer is ordinary and conforming: with Eᵢ ≥ 1 and Tᵢ = 1, Gᵢ = Eᵢ and N = ∏Eᵢ tiles are addressed. §11.3's Note even says of tile extents that "Tiles far outside that range remain conforming." A concrete case: a planar float64 channel with all tile extents 1 has s = 8, L = 8, n = 1 — stride 8, identity.

So the repaired sentence's positive universal ("changes the stored bytes of ANY tile whose shuffle stride exceeds 1") is false for a whole class of conforming tiles. The correct condition is stride > 1 AND more than one group.

HUNT FOR THE FORECLOSING SENTENCE — none found. I searched specifically for a qualifier elsewhere that would rescue the claim: (a) §17.3 itself names only one identity case, the packed boolean plane at s = 1, and never mentions the n = 1 case; (b) I scanned every occurrence of "identity" in the whole file with whitespace normalised — the only ones touching the shuffle are §17.3's packed-bool clause, §20's [R-COD-10] cross-reference, §21 row T26, and the Appendix G sentence under audit; none states the single-group case; (c) §21 row T26 restates the stride sources ("planar numeric: channel element size; interleaved: sample stride Q; packed planar bool: identity s = 1") and adds no qualifier that would decide this, and §21.1's rows-versus-rules rule is not engaged because no row contradicts anything here; (d) Appendix G's own preamble scopes the appendix ("It adds no requirement to any actor: a writer ignoring it is fully conforming") but says nothing that softens item 5's factual assertion into a hedge; (e) nothing in §11.3, §14.4, or §14.2 excludes P = 1 layers or excludes them from the profile — item 6 and item 7 concern all-fill tiles, not tile size.

SCOPE CHECK. The cited contradicting text ranges over exactly the same case: [R-COD-10]'s permutation is stated for every filtered tile, with s defined per tile in the very same paragraph, and Appendix G item 5's claim is about the same filter applied to the same tiles. Disjoint scopes do not save it.

SECONDARY POINTS. A-07 is right that §12.1 gives bool, int8 and uint8 element size 1, so stride-1 identity is not limited to the packed boolean plane; I agree with A-07 that "as for" reads as exemplary, so that is a weakness of illustration, not a second defect. X-10's separate observation about the codec value being unpinned is outside this finding's subject; item 1 does pin "a named codec implementation at a named version with fixed encoder settings", which is arguably the pinning X-10 says is missing, so I do not carry that part.

I also note, without needing it, that the claim fails content-wise too: any tile whose decoded image is invariant under the permutation (e.g. all bytes equal) is unchanged by the filter regardless of stride or group count. The structural n = 1 case is the clean one.

The repair therefore exhibits the failure mode it was meant to fix: it corrected one false universal and installed a narrower false universal in the same sentence, in text nobody re-read around.

### Decisive quotes

§17.3 [R-COD-10]: "Viewing the image as n = L/s consecutive groups of s bytes, the filtered image places byte i of group j at offset i · n + j — all first bytes in image order, then all second bytes, and so on; the inverse restores byte i · n + j to offset j · s + i. Length is unchanged."  (At n = 1: j = 0 and byte i goes to i·1 + 0 = i — the identity, at every stride.)

§14.2 [R-SER-02] table: "| planar, numeric channel c | P · Bᶜ | k · Bᶜ |" and "| interleaved | P · Q | (k div C) · Q + F_{k mod C} |"  (with §17.3's s = Bᶜ or Q, this makes n = L/s = P in both layouts).

§11.2 [R-GEO-03]: "its **sample-position count per tile** is P = ∏ Tᵢ".

§11.1 [R-GEO-01]: "each of its d dimensions has a name (§4.6), an extent Eᵢ ≥ 0, and a tile extent Tᵢ ≥ 1 ... Writers MUST NOT emit a layer with rank 0, any tile extent 0, or channel count 0"  (Tᵢ = 1 is permitted, so P = 1 is reachable).

§11.3 Note: "Tiles far outside that range remain conforming."

Appendix G item 5, as repaired (spec/tarn.md ~4392-4398): "it changes the stored bytes of any tile whose shuffle stride exceeds 1 — §17.3 makes it the identity where the stride is 1, as for a packed boolean plane —".

For the byte-level answer — heading: "### Appendix G — Reproducible-writer profile (non-normative)"; §2.1 [R-CNF-01]: "All text in this document is normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices identified as non-normative."; Appendix G preamble: "It adds no requirement to any actor: a writer ignoring it is fully conforming".

## Group G2 — REFUTED, byte-level False

### Disclosure

I read only: the finding brief /private/tmp/.../case-r27audit/case/case-G2.md; hunk-03.diff, hunk-09.diff, hunk-11.diff from that directory; and /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md. I did not open full.diff, other hunk files, docs/, conformance/, registry.json, git history, or the web, and I did not list the case directory. Tools used: Read on the four permitted files; Bash running only `sed -n` and `grep -n` against spec/tarn.md (regions read: 160-192, 261-300ish via a sed range on §2.4, 418-460, 1495-1600, 1880-1895, 1960-1975, 2370-2396, 2700-2760, 2770-2832, 2830-2900, 3400-3425, plus grep hit lines in §21). Unrequested context did appear in my context before I began: a project CLAUDE.md pointer, an index of the maintainer's memory files with titles, a user email, and a git status/recent-commit list shown by the harness. I did not open any of those files and drew no conclusion from their contents; the commit subject lines in particular name prior rounds and I disregarded them. Every conclusion below rests on text I read in spec/tarn.md.

### Reasoning

The finding asserts that §19.3 [R-RDR-03] "carries the identical construction" that hunks 9 and 11 swept, and so now over-reaches [R-ENC-04] as repaired. Checked at the location, the construction is not identical and the repair does not change the sentence's extension.

1. The two swept sentences were unrestricted; §19.3's is scoped. §20.3 said "every derived product" and §22.2 said "Every sum and product taken from a file" — neither has an antecedent, so both range over the whole document, which is exactly where the defined-vs-designated narrowing bites. §19.3 reads "the geometry floor and its arithmetic (`[R-GEO-01]`–`[R-GEO-03]`), the 2⁶³ − 1 ceiling on every quantity **that arithmetic** derives (`[R-ENC-04]`)". "That arithmetic" is anaphoric to "its arithmetic", just named and bracketed to [R-GEO-01]–[R-GEO-03]; the following clause ("the decoded sizes §14 derives from **it**") confirms the anaphora. The sentence therefore ranges only over §11.1–§11.2 geometry.

2. Inside that range every sum and product is expressly designated, so the sweep had nothing to sweep. §11.2 defines Gᵢ, N = ∏Gᵢ, P = ∏Tᵢ, the addressed-tile count (N or C·N) and N·P, then states: "These products are declaration-derived quantities under `[R-ENC-04]`: a reader MUST treat one exceeding 2⁶³ − 1 as a validity error at layer scope. `[R-GEO-03]`" That is an express designation by the section that defines the quantities — precisely what hunk 3's new sentence requires ("A designation is express, made by the section that defines the quantity"). The set-difference the brief needs is therefore only {Gᵢ}, and Gᵢ is a ceiling division, not a sum or product: it was outside [R-ENC-04]'s subject matter before the repair ("any quantity this specification defines as a sum or product") just as much as after it. The repair did not narrow anything relative to §19.3, so §19.3 cannot be an unswept restatement of it.

3. The repair's new excusing clause has no instance in the cited range. Hunk 3 added: "an expression this specification writes only inside a comparison, and names nowhere, is not a designated quantity and no reader is obliged to form it." Within [R-GEO-01]–[R-GEO-03] there is no comparison-only, unnamed product — §11.1's only comparison is "0 < Eᵢ < Tᵢ", and the one comparison-form phrasing the document flags ("where the grid overhangs the extent, stated in a form that forms no product (§4.2)") sits in §11.3 under [R-GEO-04], outside the range §19.3 cites. So §19.3 obliges the formation of nothing [R-ENC-04] now excuses — the conflict the finding needs does not exist.

4. B-05's two consequence claims are false at the text.
 (a) "The two undesignated quantities at layer scope are exactly the ones B-03 identifies — the index region size among them." The index region size (entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4) is not derived by the geometry arithmetic of [R-GEO-01]–[R-GEO-03]; §19.3 reaches it, if at all, through the separately cited "index cross-checks computable without I/O (`[R-CNT-17]`)". The complained-of clause cannot pick it up.
 (b) "at a tier [R-ENC-04] does not name." [R-ENC-04] assigns "a validity error at the owning scope"; [R-CNF-08] maps owning scope to outcome; and §11.1 states "The owning scope (§2.4) of a layer's geometry and linearization fields is the layer." [R-GEO-03] says layer scope in terms. §19.2 places full layer-record validation at first access to a layer. The tier is the one the rules name.

5. Foreclosing text I did find. §19's preamble: "It introduces no new structures; each step cites the requirement whose outcome governs its failure." and "Each step names the checks its tier's structures turn on. Those enumerations are not the complete inventory of what a reader detects at that tier: §21's register is". §19.3's phrase is a pointer to the ceiling [R-ENC-04] imposes, not a new ceiling; where [R-ENC-04] imposes none on a quantity there is no "ceiling on" it to validate. Register row L2 confirms the operative inventory and does not list Gᵢ, while it does list the geometry products, P·Q, P·Bᶜ and the index-region formula, each designated at its own defining section (§14.2 "These products and sums are declaration-derived quantities under `[R-ENC-04]`. `[R-SER-02]`"; §14.3 "Every decoded size, and the value count V, is a declaration-derived quantity under `[R-ENC-04]`. `[R-SER-07]`") — and §19.3 cites those two rules separately, so its coverage tracks L2 rather than exceeding it. I could not find any sentence making §19.3 govern over [R-ENC-04], and did not need one: the two do not diverge.

6. Even on the reporters' own arithmetic the residue is inert, and X-06 says so: Gᵢ ≤ Eᵢ ≤ 2⁶³ − 1 by [R-ENC-03] with Tᵢ ≥ 1 by [R-GEO-01], and the ceiling division's "Eᵢ/Tᵢ plus 1" applies only when Eᵢ mod Tᵢ ≠ 0, hence Tᵢ ≥ 2, hence Eᵢ/Tᵢ + 1 ≤ (2⁶³−1)/2 + 1. No file can fail the supposed extra check, and a reader forms Gᵢ regardless in order to form N. The proposed repair also mis-attributes designation to arithmetic rather than to a section ("every quantity that arithmetic designates"), which is the opposite of hunk 3's "made by the section that defines the quantity".

What survives is at most a preference that four places use one phrase. That is not a divergence between a normative checklist and the rule it cites, so I do not grade it PARTIAL: the checklist's extension equals the rule's, before and after the repair.

Byte-level, independently: no. No writer's emittable set changes, no file's accept/reject verdict changes, and no byte of any conforming file is affected — the only quantity in the alleged difference cannot exceed the ceiling under [R-ENC-03] and [R-GEO-01].

### Decisive quotes

§11.2 [R-GEO-03] (spec/tarn.md lines 1550-1556): "The layer's **spatial-tile count** is N = ∏ Gᵢ, and its **sample-position count per tile** is P = ∏ Tᵢ. The layer's **addressed-tile count** ... is N for an interleaved layer and C · N for a planar layer ... and its **total sample-position count** is N · P. These products are declaration-derived quantities under `[R-ENC-04]`: a reader MUST treat one exceeding 2⁶³ − 1 as a validity error at layer scope."

§4.2 [R-ENC-04] as repaired (lines 442-445): "A designation is express, made by the section that defines the quantity; an expression this specification writes only inside a comparison, and names nowhere, is not a designated quantity and no reader is obliged to form it."

§19 preamble (lines 2733-2743): "It introduces no new structures; each step cites the requirement whose outcome governs its failure. / Each step names the checks its tier's structures turn on. Those enumerations are not the complete inventory of what a reader detects at that tier: §21's register is ... A row this section does not restate is due at its own tier all the same, with its governing rule's own outcome."

§19.3 as it actually reads (lines 2858-2862): "the geometry floor and its arithmetic (`[R-GEO-01]`–`[R-GEO-03]`), the 2⁶³ − 1 ceiling on every quantity that arithmetic derives (`[R-ENC-04]`) and on the decoded sizes §14 derives from it (`[R-SER-02]`, `[R-SER-07]`), and the index cross-checks computable without I/O (`[R-CNT-17]`)." — the quantifier is bound by the immediately preceding "its arithmetic (`[R-GEO-01]`–`[R-GEO-03]`)", which the brief's excerpt keeps but its argument ignores.

§11.1 (line 1508): "The owning scope (§2.4) of a layer's geometry and linearization fields is the layer." — against B-05's "a tier [R-ENC-04] does not name".

§21 row L2 (line 3524): "... N = ∏⌈Eᵢ/Tᵢ⌉; P = ∏Tᵢ; N·P; C·N ...; P·Q ...; P·Bᶜ; entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 | reader | layer access | `[R-ENC-04]` (R-GEO-03, R-CNT-13, R-SER-02, R-SER-07)" — Gᵢ is not among the quantities the register makes a reader check, and the index-region formula is cited to rules §19.3 lists separately.

## Group G3 — PARTIAL, byte-level False

### Disclosure

Read: the finding brief /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/95161ceb-f057-4b49-92d8-298403d066a9/scratchpad/case-r27audit/case/case-G3.md; hunk-01.diff, hunk-02.diff, hunk-10.diff from that same directory; and /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (sections read: §2.1-§2.4 lines 95-270, §6.2-§6.3 lines 745-845, §21.1-§21.2 lines 3389-3516, §21.6 lines 3641-3700, §21.9 lines 3795-3830). Ran only grep/sed against spec/tarn.md (searches for "R-CNF-13", "R-CNT-07", "R-CNT-04", "R-CNT-24", "R-CNF-01", "21.6", "Two structural cases", "declines to judge", "Neither is a register row", "records a reader's capability"). I did not read full.diff, other hunk files, docs/, conformance/, registry.json, git history, or anything on the web, and did not list the case directory.

Unrequested context did appear before I began: a project instruction file pointer (CLAUDE.md -> AGENTS.md) and an index of the maintainer's personal memory notes naming TARN working practices, plus a git-status block showing recent commit subject lines that reference ADR numbers and a prior cleanroom round's outcome. I did not open any of those files and did not reason from their contents; I note the appearance here rather than repeating what they said. One caveat for the record: the git-status block visible in my prompt included commit subjects mentioning a prior round's result. I formed my conclusions from the specification text only, but I cannot un-see that those lines were present.

### Reasoning

QUOTATION CHECK — all three quotations in the brief are accurate and in context. §21.6's closing paragraph reads verbatim at lines 3674-3693; §2.3's [R-CNF-13] at lines 226-246 and the repaired [R-CNF-02] at lines 140-148 match the hunks; §21.2's repaired preamble at lines 3468-3475 matches hunk 10. Nothing is truncated in a meaning-changing way.

SWEEP CHECK — the brief's core factual claim holds. `grep -n "R-CNF-13"` returns exactly three hits in the whole document: lines 144, 246 (both §2.3) and 3469 (§21.2's preamble). §21.6 contains no occurrence of "R-CNF-13", no occurrence of "reach", and no occurrence of "R-CNT-24". §21.6 was demonstrably not swept when the repair landed.

WHAT FORECLOSES MOST OF IT — §21.6 states every one of its entries as a condition considered in isolation, and does so uniformly. "An ignore-lane flag bit (16-31) is set | Ignored; **the file is conforming**"; "The file contains zero layers | **A conforming file** with an empty directory"; "A user-metadata record declares an experimental-range document encoding | Ignored; **the file is conforming**". Each of those is equally "false" of a file that also has a bad directory CRC — the idiom plainly means *this condition alone leaves the file conforming*. §21.1 confirms the reading: "§21.6's entries restate their governing rules on the same terms a row does", and a row is one condition. The closing paragraph continues that idiom ("Two structural **cases**", "The first **is** version_major naming a major this reader does not implement"), so "conforming files a reader nevertheless refuses" and "In both the outcome records a reader's capability, not a defect in the bytes" say that *the foreign-major declaration itself* is not a byte defect — which [R-CNF-13] does not deny. [R-CNF-13]'s carve-out concerns a *different, co-present* condition (F1/F6/F8/F14) failing. X-07's headline — "§21.6 still classes every foreign-major file as a conforming file refused on capability" — therefore overstates: it reads a per-condition catalogue as a per-file classification, and if that reading were right, four other §21.6 entries would be defective for the same reason. The clause X-07 concedes survives ("the file **can** be perfectly conforming under that major") is modal and confirms the isolation reading rather than being an isolated survivor. The paragraph's operative conclusion — that neither *condition* is a register row — is untouched, as both reporters concede.

WHAT SURVIVES — one clause is not condition-scoped and is now literally false as written: "a file this document declines to judge is not one" (line 3688). Its subject is a *file*, not a condition, and it asserts a blanket refusal to judge. That is exactly the proposition hunk 1 edited at its source: [R-CNF-02] previously said a foreign-major file "is neither conforming nor nonconforming under it" flat, and now says "...under it **save as to the requirements that reach it** (`[R-CNF-13]`)... while the failure of a reaching requirement **is** [a finding about its bytes]". §21.6 restates the pre-repair wording of the very sentence the repair changed, and it cites [R-CNF-02] elsewhere in the same paragraph. That is an unswept restatement in normative text — §21.6 is not §1, not a blockquote, not a labelled Note/Rationale, so [R-CNF-01] leaves it normative. The companion sentence "What is registered in each case is the neighbouring condition that *is* a violation — version_major = 0..." is now incomplete in the same direction, since §21.2's preamble names four rows that do record such a file.

THE OVERLAP IS NOT EMPTY, so the surviving clause is not merely cosmetic. I tested the strongest ordering refutation: §6.2 ([R-CNT-06], line 809) puts trailer magic and trailer CRC ahead of the version gate, so a reader failing F8/F14/F1-trailer never reaches [R-CNT-07], and [R-CNT-04] (line 753) puts the front-block check "before other processing" for a resident reader. But (a) a reader that would have to fetch bytes [0,16) "MAY defer or omit the check", so it can reach the version gate on a file that violates F6; and (b) F6's row expressly says "a verifier holds no such exemption (§2.3)", and [R-CNF-11] makes an established violation beat *cannot establish*. So a verifier on a major-2 file with a corrupt front block establishes F6 and reports *nonconforming* — a file §21.6's unqualified "declines to judge" clause says this document does not judge.

WHY NOT CONFIRMED — the case as merged asserts three stale statements plus an incomplete enumeration; I can sustain one clause plus the enumeration, and the isolation idiom defeats the other two. B-07's title is accurate; X-07's is not, and B-07's own "Both halves are now stale" and its proposed qualification of "the outcome records a reader's capability" go further than the text supports.

WHY NOT BYTE-LEVEL — I answered this independently and reach the same place both reporters did, for partly different reasons. (1) The paragraph carries no BCP 14 keyword; [R-CNF-13] carries MUST twice and [R-CNF-11] carries the priority rule ("An established violation takes priority: a verifier that has established any violation reports *nonconforming*"), so the verdict on every byte sequence is fixed by keyworded rules elsewhere. (2) §21.1's closing sentence (lines 3419-3421) subordinates §21.6: "where such an entry and the rule it cites diverge, the rule governs there too" — and the paragraph does cite [R-CNF-02], which now carries the qualification. That routing is imperfect (the diverging rule for case 1 is [R-CNF-13], which the paragraph does not cite, and "entries" arguably means table rows rather than closing prose), which is why I do not treat §21.1 as refuting the finding outright — but it is enough that no implementer who follows the register's own reading instructions lands on a wrong verdict. (3) The paragraph's operative output — that these two conditions are not register rows — is unchanged, so no file moves between *conforming*, *nonconforming* and *cannot establish*.

MINOR: both reports' line citations are a couple of lines off (§21.6's paragraph begins at 3674, the complained-of sentence at 3687-3690); immaterial.

### Decisive quotes

SURVIVING DEFECT — §21.6 line 3687-3690 (normative prose, not a blockquote): "Neither is a register row: the register enumerates file-conformance violations (§21.1), and a file this document declines to judge is not one."

THE SOURCE SENTENCE THE REPAIR CHANGED AND §21.6 STILL RESTATES — §2.3 [R-CNF-02] lines 143-148: "a file declaring another major is neither conforming nor nonconforming under it save as to the requirements that reach it (`[R-CNF-13]`): a reader refuses such a file on capability grounds (§6.3, `[R-CNT-07]`), and that refusal is not a finding about its bytes, while the failure of a reaching requirement is."

WHAT REFUTES THE BROADER LIMB — §21.6's uniform condition-in-isolation idiom, stated identically for four other entries: "An ignore-lane flag bit (16-31) is set | Ignored; the file is conforming"; "The file contains zero layers | A conforming file with an empty directory"; "A user-metadata record declares an experimental-range (>= 0x80) document encoding | Ignored (ignore-record); the file is conforming". Under this idiom "Two structural cases are **conforming files a reader nevertheless refuses**" (line 3674) predicates of the condition, not of every file carrying it, and the hedge in the same sentence confirms it: "the file **can** be perfectly conforming under that major."

WHY NO VERDICT FORKS — §21.1 lines 3419-3421: "§21.6's entries restate their governing rules on the same terms a row does, and where such an entry and the rule it cites diverge, the rule governs there too." And §2.3 [R-CNF-11]: "An established violation takes priority: a verifier that has established any violation reports *nonconforming*, however many requirements it was unable to check."

WHY THE OVERLAP IS REAL — §21.2 F6's row: "the obligation binds a reader holding those bytes resident, and a reader that would have to fetch them MAY defer or omit the check (`[R-CNT-04]`); a verifier holds no such exemption (§2.3)."

SWEEP EVIDENCE — `grep -n "R-CNF-13" spec/tarn.md` returns only lines 144, 246, 3469; a grep for "reach", "R-CNF-13" and "R-CNT-24" over lines 3641-3695 (all of §21.6) returns nothing.

## Group G4 — PARTIAL, byte-level False

### Disclosure

Read: the finding brief /private/tmp/.../case-r27audit/case/case-G4.md, hunk-02.diff and hunk-10.diff, and /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (via sed ranges over §2.1–2.4 lines 95–265, §5.1 lines 600–620, §6.2–6.3 lines 780–850, §21.1 lines 3389–3466, §21.2 lines 3466–3516, §21.6 lines 3641–3700, §21.9 lines 3845–3860) plus grep/rg over the spec only (searches for "R-CNT-24", "R-CNT-06]", "R-CNF-13", "R-CNF-01]", "version_major", "R-CNT-27]", "reach", and whitespace-normalised `tr`-pipeline greps for the [R-CNT-06] ordering sentence, the §21.2 preamble deferral clause, and [R-CNF-02]'s pure-predicate sentence). I read nothing under docs/, conformance/, no PLAN.md/OPEN-QUESTIONS.md/AGENTS.md/README.md, no registry.json, no git history, no full.diff, no other hunk file, and did not list the case directory. Unsolicited context did appear before I began: a project instruction file pointer and an index of the maintainer's memory notes (naming prior-round themes and working cadence). I did not open any of it and drew no conclusion from it; every claim below is sourced to spec/tarn.md line ranges I read myself.

### Reasoning

The core observation is real and I could not find the sentence that forecloses it; two of the brief's three supporting limbs do not survive checking, so PARTIAL.

WHAT HOLDS. [R-CNF-13] (lines 227–246) fixes reach at the granularity of a *requirement*: "A requirement of this specification **reaches** a file … when, and only when, the invariant its condition violates is one `[R-CNT-24]` fixes …", "A reader MUST apply every reaching requirement …", "Every other requirement of this specification governs a structure this text defines for format major 1 alone". The definite "its condition" presupposes one condition per requirement. §2.2 (lines 115–121) ties a requirement to an identifier, and §21.1 (lines 3391–3398) makes a row "one malformed condition" plus "the requirement that defines it" — so identifier and condition are explicitly different units. [R-CNT-06] is a single identifier whose text (lines 811–818) is one ordered list of checks, and it is the Governing rule cell of ten §21.2 rows: F8, F9, F10, F11, F12, F13, F14, F15, F16, F17 (lines 3486–3495). I checked the split the brief asserts and it is correct: F8 (trailer magic) and F14 (trailer CRC) assert invariants [R-CNT-24] fixes; F9, F10, F11, F12, F13, F15, F16, F17 assert dir_offset ≥ 16, dir_offset+dir_length ≤ F−64, generation ≥ 1, file_id ≠ 0, committed_file_length 64-aligned, reserved bytes zero, dir_length ≥ 4, committed_file_length = F — none of which [R-CNT-24] (lines 836–843) fixes; it fixes only the magic at F−64, version fields at F−56, the CRC at F−4, the constant front block, and the no-growth cap, expressly licensing a future major to redefine "the remaining 48 trailer bytes" — which is where F15's [56,60) sits.

So the rule, taken at its own unit, yields either too much (existential reading: [R-CNT-06] reaches, therefore is not one of the "other requirements", therefore its reserved-bytes-zero and directory-bounds conditions are asserted against a foreign-major file and F15 records it — flatly contrary to [R-CNT-24]'s 48-byte licence and to [R-CNF-13]'s own justification "the invariant broken is one that major shares") or too little (universal reading: [R-CNT-06] does not reach, so F8 and F14 do not — contrary to §6.2's own ordering, which puts magic and CRC before the version gate precisely because "only these touch fields whose positions are fixed across all majors"). Neither branch produces the set §21.2's preamble states. I searched for a deciding sentence and found none: "reach" in this technical sense appears only at lines 144, 227–246, the Note at 248–260, and the §21.2 preamble at 3468 — nowhere else in the document, and no passage says "requirement" distributes over the conditions a register row individuates. §21.1's "the row is the rule" (line 3423) is about corpus instance-counting, not requirement identity. Line 144's amendment to [R-CNF-02] repeats the same unit ("save as to the requirements that reach it"), so the under-determination propagates rather than being cured.

WHAT DOES NOT HOLD. (1) The brief's check label and its "There is no reading on which both survive" are wrong. The §21.2 preamble subordinates itself in the same breath: "where this restatement and that rule diverge, the rule governs (§21.1)" (hunk 10, line 3472). And the Note at 248–260 is inside a blockquote, hence non-normative under [R-CNF-01] (line 106). A non-normative Note and a self-deferring restatement cannot stand in unresolved contradiction with a normative rule — the document already decides which text wins. The defect is that the winning rule then gives an answer its own worked examples and the register's enumeration deny, not that two normative statements collide.

(2) The brief's headline consequence — that a reader is obliged to apply reserved-bytes-zero to a major-7 file — is blunted by [R-CNT-06]'s own internal ordering, which the brief never quotes: the tail checks are owed only "those gates passed", and the version gate is one of the three gates. For every reader that does not implement the declared major the gate fails ([R-CNT-07], line 827) and the tail checks are never owed. The defect survives only at the predicate/register level, where the ordering gives no cover, because [R-CNF-02] makes file conformance "a pure predicate on bytes: it does not depend on any reader" — so whether F15 records a foreign-major file is settled by which requirements reach, not by a reader's traversal order. That is the ground the finding actually stands on, and the brief did not identify it.

(3) The F5 limb fails. F5's Governing rule is [R-CNT-27] (line 3483), a single-condition requirement (lines 611–615) asserting one invariant, a 128-byte floor. [R-CNT-24] does not fix that floor, so F5 does not reach under a plain application of the test; the several major-1 facts the brief calls a "conjunction" are the floor's derivation, not conjuncts of the asserted invariant. No decomposition rule is needed and its absence is not a defect.

ACTUAL DEFECT: [R-CNF-13] states reach over requirements while the invariants it tests are condition-granular, and [R-CNT-06] — one identifier, ten §21.2 rows, two of whose conditions assert [R-CNT-24] invariants and eight of which assert format major 1's — has no reading under which the rule reproduces the reaching set §21.2's preamble and the Note state. The brief's suggested repair (make the unit the condition as §21.1's rows individuate them, naming [R-CNT-06]'s split explicitly) addresses it; the added conjunction-decomposition clause is unnecessary.

BYTE-LEVEL: no. §6.2's trailer table fixes version_major = 1 (line 783) and [R-CNF-05] binds writers to conforming files, so no conforming writer emits a foreign major. For any major-1 reader a foreign-major file is reject-file on both readings — on [R-CNT-06]'s own ground or on [R-CNT-07]'s capability ground — so no accept/reject verdict and no byte on disk forks. What forks is a verifier's verdict word (nonconforming vs. cannot establish), a reader's diagnostic, and whether F15/F9–F17 record such a file. The one place an accept/reject could fork is a reader implementing the foreign major, which [R-CNF-13] expressly contemplates ("whether or not it implements that major") — but this text defines no such major and no vector can exercise it.

### Decisive quotes

[R-CNF-13], spec/tarn.md lines 227–246: "A requirement of this specification **reaches** a file declaring a format major other than 1 when, and only when, the invariant its condition violates is one `[R-CNT-24]` fixes in every format major version. … A reader MUST apply every reaching requirement to a file whatever major it declares … Every other requirement of this specification governs a structure this text defines for format major 1 alone; it is not assessed against a file declaring another major, no violation of it is established there, and no §21 row restating it records such a file."

[R-CNT-06], lines 811–818 (one identifier, many conditions, with the ordering the brief omits): "A reader MUST validate, in order: the trailer magic; the trailer CRC; the version gate (§6.3) — only these touch fields whose positions are fixed across all majors (`[R-CNT-24]`) — and then, those gates passed, MUST validate all of the following …: the flag gates (§6.3); committed_file_length equals the file size … and is a multiple of 64; dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64; 1 ≤ generation ≤ 2⁶³ − 1; file_id ≠ 0; reserved bytes zero."

[R-CNT-24], lines 836–843: "A future major MAY redefine only the remaining 48 trailer bytes and MUST NOT grow the trailer" — F15's bytes [56,60) are inside those 48, yet F15's Governing rule cell is `[R-CNT-06]` (line 3493), the same identifier as F8 and F14.

§21.1, lines 3391–3398 (row and requirement are different units): "each row is one malformed condition, with the outcome class its scope determines … and the requirement that defines it."

§21.2 preamble, line 3472 (the self-deferral that defeats the LOCAL_CONTRADICTION framing): "where this restatement and that rule diverge, the rule governs (§21.1)."

[R-CNF-02], lines 139–141 (why the reader-ordering does not rescue the rule): "File conformance is a pure predicate on bytes: it does not depend on any reader, writer, or environment."

[R-CNF-01], line 106 (the Note at 248–260 is a blockquote): "All text in this document is normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale* …"

## Group G5 — REFUTED, byte-level False

### Disclosure

I read exactly: the finding brief /private/tmp/.../case-r27audit/case/case-G5.md; the two hunk files hunk-02.diff and hunk-10.diff; and /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (via sed/awk/grep only). I ran: sed -n on spec/tarn.md line ranges 130-270, 735-850, 2745-2815, 3400-3500, 4165-4185, 4495-4520; `tr '\n' ' ' < spec/tarn.md | tr -s ' ' > /tmp/flat.txt` to build a whitespace-normalised single-line copy of the spec in the system temp dir, and grep -o -b over that copy for the fragments "own terms", "exempted from", "exemption", "subject to", "MUST apply", "apply every", "on its own terms", "more specific", "MUST apply a known type", "when, and only when", "is owed where"; grep -n for "R-CNF-13|R-CNT-04", for "^#{1,6} " (heading index), and for "non-normative"; and awk to print the first 3 characters of lines in four ranges to confirm blockquote status. I did NOT read full.diff, other hunk files, docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, spec/registry.json, git history, or the web, and I did not list the case directory. Unrequested context DID appear in my context before I began: a project CLAUDE.md pointer, an index of the maintainer's persistent memory notes with descriptive filenames, and an environment block containing git status with recent commit subject lines (which name ADR numbers and a cleanroom round position). I disregarded all of it; no conclusion below rests on it, and every claim is sourced to a line of spec/tarn.md that I quote.

### Reasoning

The brief's quotations are accurate and in context — I checked every one. But the finding rests on reading "MUST apply every reaching requirement" as "MUST perform every reaching check regardless of residency," and four things foreclose that reading.

1. The sentence's only contrastive axis is the declared major, not residency. "A reader MUST apply every reaching requirement to a file whatever major it declares" (line 233-234). The document uses this exact construction elsewhere with exactly the meaning "the named circumstance does not disturb the requirement's own terms": §7.3, "A reader MUST apply a known type's specified semantics regardless of its stored MU and PE bits." Applying [R-CNT-04] means applying [R-CNT-04] as written — resident: MUST verify; non-resident: MAY defer or omit. [R-CNF-13] never mentions residency and cannot silently override it. The continuation reinforces this: the failure is treated "on that requirement's own ground."

2. Read structurally, [R-CNF-13] adds no check at all, so it cannot add a fetch. The reaching set is exactly the checks §6.1/§6.2 already place before the version gate: [R-CNT-06] orders "the trailer magic; the trailer CRC; the version gate (§6.3) — only these touch fields whose positions are fixed across all majors ([R-CNT-24])," and [R-CNT-04] places the front block "before other processing" for a resident reader. A reader performs precisely these on any file, foreign major or not. What [R-CNF-13] changes is the *ground* of refusal and the *verdict* — not what is read. X-09's own conclusion ("a competent implementer does not actually acquire a new fetch duty") is right, and it is right for a textual reason, not by reconstruction.

3. The exemption did not survive only in the register. Both reporters treat F6's Condition cell as the last normative-ish trace, and X-09 argues §21.1 makes the rule beat the row. That misapplies §21.1, which says "where a row and the rule it cites diverge, the rule governs" — F6's Governing rule cell is `[R-CNT-04]`, not [R-CNF-13], so the rule §21.1 prefers over F6's cell is the one carrying the MAY. More decisively, the exemption is restated in two further NORMATIVE passages neither reporter cites and neither hunk touches: §19.1 step 1 under [R-RDR-01] (lines 2755-2760), "one that would have to issue a further range request for them MAY defer or omit the check (`[R-CNT-04]`)", and §19.2's at-open bullet under [R-RDR-02] (lines 2807-2809), "the front signature block, for a reader whose open leaves it resident (`[R-CNT-04]`)". I verified by column inspection that neither is inside a blockquote. Three normative statements of the residency test stand; the §21.2 preamble that hunk 10 shortened was a restatement that now expressly defers ("where this restatement and that rule diverge, the rule governs (§21.1)").

4. The [R-CNT-07] limb is a sufficient condition, not an exclusive one, and the two clauses can never both be engaged. [R-CNF-13] says the distinct diagnostic "is owed where every reaching requirement is satisfied…" — "where", not "only where". The drafter demonstrably knows how to write exclusivity: the same requirement, two sentences earlier, says a requirement reaches "when, and only when". A-06 converts a non-statement into a prohibition. And operationally there is no gap: every reaching failure is detected before the version gate (§6.2's fixed order; [R-CNT-04]'s "before other processing"), so a reader that establishes one never reaches [R-CNT-07]'s diagnostic clause at all; a reader that lawfully omits the front-block check reaches the gate and gives the distinct diagnostic [R-CNT-07] still asks for unconditionally. Nothing is undecidable and nothing collides.

I searched specifically for a sentence that would support the strengthening reading — an interpretive rule that a later requirement overrides an earlier one, a statement that reaching requirements are applied without their internal conditions, any "notwithstanding"/"more specific"/"subject to" precedence clause — and found none; what I found instead was consistent language in the opposite direction, including [R-CNF-11]'s definition of a verifier as one that checks "every file-level requirement — including those ordinary readers are exempted from", which presupposes that ordinary-reader exemptions remain live.

If anything survives here it is editorial: the shortened §21.2 preamble no longer spells out the F6/front-block interaction in situ. That is a loss of a gloss whose content is stated normatively in three other places and in the row itself, in a passage that explicitly subordinates itself to the rule. That is not a contradiction, not an overshoot, and not a defect.

### Decisive quotes

§7.3 (house meaning of "MUST apply … regardless of X"): "A reader MUST apply a known type's specified semantics regardless of its stored MU and PE bits — a flipped stored bit never changes conforming behavior".

§2.3 [R-CNF-13], line 233-236 (the contrastive axis is the major, and the ground is the requirement's own): "A reader MUST apply every reaching requirement to a file whatever major it declares, and MUST treat its failure as reject-file on that requirement's own ground rather than on capability grounds".

§2.3 [R-CNF-13], line 231-233 vs line 236-238 (the drafter's own exclusivity marker, present in one clause and absent in the other): "reaches** a file declaring a format major other than 1 when, and only when, the invariant its condition violates is one `[R-CNT-24]` fixes in every format major version" — against — "is owed where every reaching requirement is satisfied and the declared major is one the reader does not implement".

§19.1 [R-RDR-01], step 1, lines 2755-2760 (normative, untouched, no major qualification): "A reader whose open leaves bytes [0, 16) resident — a speculative suffix window that reached offset 0 included — MUST verify the front signature block by byte equality before other processing (mismatch: reject-file); one that would have to issue a further range request for them MAY defer or omit the check (`[R-CNT-04]`)."

§19.2 [R-RDR-02], lines 2807-2809 (normative, untouched): "at open: the front signature block, for a reader whose open leaves it resident (`[R-CNT-04]`), the trailer, the directory region and its record walk, and the layer-name namespace".

§21.1, lines ~3406-3407 (what §21.1 actually prefers, refuting X-09's use of it): "each row *restates* its governing rule, and where a row and the rule it cites diverge, **the rule governs**." — and F6's Governing rule cell, line 3484, is "`[R-CNT-04]`", the rule that states the exemption.

§6.2 [R-CNT-06] (why the reaching set is exactly the pre-gate checks, so no new fetch arises): "A reader MUST validate, in order: the trailer magic; the trailer CRC; the version gate (§6.3) — only these touch fields whose positions are fixed across all majors (`[R-CNT-24]`)".

§2.3 [R-CNF-11] (exemptions remain a live category): "A reader that additionally checks every file-level requirement — including those ordinary readers are exempted from — and certifies conformance."

## Group G6 — REFUTED, byte-level False

### Disclosure

Read exactly three files: the finding brief /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/95161ceb-f057-4b49-92d8-298403d066a9/scratchpad/case-r27audit/case/case-G6.md, the hunk /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/95161ceb-f057-4b49-92d8-298403d066a9/scratchpad/case-r27audit/hunk-03.diff, and /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md. Against the spec I ran `sed -n` on lines 400-460, 790-830, 862-882, 955-985, 1065-1095, 1130-1145, 1545-1615, 1875-1900, 1955-1980, 2036-2048, 2050-2115, 2375-2400, 2755-2775, 3070-3095, 3389-3430, 3865-3900, and `grep -n` for: "designat", "R-ENC-04", "dir_offset", "entry_count × 20", "× 20", "mathematical|forms no product|form the |forming |to form|compute|computed|evaluat", "^#### 21.1", "^### 21", "^#### 11.3". I did not read full.diff, other hunk files, docs/, conformance/, registry.json, git history, or anything else, and did not list the case directory.

Unrequested context appeared before I began: a project instruction file pointer (CLAUDE.md -> AGENTS.md), an index of the maintainer's memory notes naming several TARN working documents, a current-date/user-email block, a list of installed skills, and MCP server usage instructions. I did not open any file it named and drew no conclusion from it; the reasoning below rests only on spec/tarn.md, the brief, and hunk-03.diff. I note that the index named things that could hint at round position and prior findings; I disregarded them.

### Reasoning

The brief's quotations of the hunk, [R-CNT-06] and [R-CNT-17] are accurate. The finding nevertheless fails, because three of its four "contradicting" passages do not satisfy the exemption clause's own two conditions ("writes only inside a comparison" AND "names nowhere"), and the fourth is not contradicted by the clause at all.

1. dir_offset + dir_length — the brief's centrepiece — is NOT written only inside a comparison. §6.4 [R-CNT-09] (line 873, normative prose, not blockquoted) says "fetch / [dir_offset, dir_offset + dir_length); verify and decode per §7.1", and §19.1 step 3 (line 2766, normative numbered list) says "Fetch [dir_offset, dir_offset + dir_length) and / verify the directory CRC before any other use of the region". Both write the sum as a range endpoint a reader must actually form to issue the request. The clause's condition is conjunctive and "only"-quantified, so it never reaches this sum, and the brief's narrative — "A reader taking hunk 3's clause at face value concludes it need not form dir_offset + dir_length, then discovers [R-CNT-06]" — cannot arise.

2. [R-CNT-13] (§7.3, lines 968-971) does not write its sum only inside a comparison either: it lists "an extent extending past F − 64, or an overflowing sum is a validity error at the scope the record governs". "An overflowing sum" is a standalone predicate on the sum, not a comparison. Outside the exemption.

3. §15.3's table row likewise states "offset + length overflows" as a standalone condition, and — decisively — §15.2 [R-IDX-02] contains the express designation the clause demands: "`[R-ENC-03]`'s value-domain rule and `[R-ENC-04]`'s sum rule apply to the fields of non-sentinel entries only." That is a designation "made by the section that defines the quantity", exactly what the new clause requires. Outside the exemption. (§15.3 additionally says the per-entry outcomes "govern notwithstanding the general owning-scope mapping of `[R-ENC-03]`/`[R-ENC-04]`", so it was never dependent on [R-ENC-04] for its verdicts.)

4. Only [R-CNT-17]'s "entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4" is genuinely written only inside comparisons in normative text (line 1079; line 1138 is a blockquote Example, and the "entry_count × 20 bytes" region diagram at line 2044 is inside a blockquote, so non-normative under [R-CNF-01]). But there is no collision: [R-CNT-17] obliges an equality to hold, not the formation of an expression. Deciding a comparison and forming its operand are different acts — the overflow-safe way to check that equality is precisely to rearrange it. The clause's "form" is bounded by its immediate subject ("is not a designated quantity AND no reader is obliged to form it"), and a whole-document grep for form/forming/compute/evaluate turns up no other obligation anywhere in the spec phrased as forming a quantity: "to form" appears at line 445 only, and "forms no product" at line 1574 only. There is no rule for the clause to be a "general licence" against.

The brief's supporting claim that the clause "is doing no remaining work at that site" is also false. §11.3 line 1573-1574 now reads "Where Eᵢ mod Tᵢ ≠ 0 — equivalently, where the grid overhangs the / extent, stated in a form that forms no product (§4.2)", an explicit cross-reference into §4.2 that lands on this very clause. The repair's vocabulary is corroborated by untouched text: §22.2 [R-SEC-02] line 3881-3882 already reads "Every declaration-derived sum and product `[R-ENC-04]` designates is overflow-checked before use", and §20 line 3083-3084 "`[R-ENC-04]`'s 2⁶³ − 1 ceiling on every quantity / it designates".

Residue, not sufficient for PARTIAL and not raised by the brief: §21 rows F3 and L2 name [R-ENC-04] as governing rule for "dir_offset + dir_length" and for "entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4". For dir_offset + dir_length the designation survives via the non-comparison uses above; for the entry_count formula the row now cites a rule that no longer designates it. §21.1 forecloses that: "each row *restates* its governing rule, and where a / row and the rule it cites diverge, **the rule governs**." The condition remains caught by [R-CNT-17] (and register row L22, governing rule [R-CNT-17]) at the same layer scope with the same outcome, so no verdict moves and nothing is left undetected.

Byte-level, independently assessed: no. Even granting the brief's reading in full, [R-CNT-06] rejects a directory whose sum exceeds F − 64 (and F ≤ 2⁶³ − 1 by [R-ENC-03], so any sum above 2⁶³ − 1 necessarily exceeds F − 64) — reject-file either way. [R-CNT-17]'s equality fails against an extent_length that is itself capped at 2⁶³ − 1 whenever the formula's mathematical value exceeds that cap — layer-scope validity error either way, the same scope [R-ENC-04] would have assigned. No file changes verdict and no writer gains latitude.

### Decisive quotes

Hunk 3, spec lines 442-445: "A designation is express, made by the / section that defines the quantity; an expression this specification / writes only inside a comparison, and names nowhere, is not a designated / quantity and no reader is obliged to form it."

§6.4 [R-CNT-09], lines 872-873 (normative, not blockquoted): "(2) fetch / [dir_offset, dir_offset + dir_length); verify and decode per §7.1."

§19.1 step 3, line 2766 (normative numbered list): "3. **Directory.** Fetch [dir_offset, dir_offset + dir_length) and / verify the directory CRC before any other use of the region / (`[R-CNT-11]`)."

§7.3 [R-CNT-13], lines 969-971: "Any other combination with either half zero, an / extent_offset < 16, an extent extending past F − 64, or an / overflowing sum is a validity error at the scope the record governs" — the sum's overflow is stated standalone, not inside a comparison.

§15.2 [R-IDX-02], lines 2065-2067: "Sentinel entries are a reserved pattern, / not offsets or lengths: `[R-ENC-03]`'s value-domain rule and / `[R-ENC-04]`'s sum rule apply to the fields of non-sentinel entries / only." — the express designation for the §15.3 row.

§15.3, lines 2084-2086: "The per-entry outcomes below / govern notwithstanding the general owning-scope mapping of / `[R-ENC-03]`/`[R-ENC-04]`."

§11.3 [R-GEO-04], lines 1573-1574: "Where Eᵢ mod Tᵢ ≠ 0 — equivalently, where the grid overhangs the / extent, stated in a form that forms no product (§4.2)" — the clause still has a live referrer.

§21.1, lines 3403-3405: "each row *restates* its governing rule, and where a / row and the rule it cites diverge, **the rule governs**."

§22.2 [R-SEC-02], lines 3881-3882: "Every declaration-derived sum and product / `[R-ENC-04]` designates is overflow-checked before use."

## Group G7 — REFUTED, byte-level False

### Disclosure

Read in full: the finding brief /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/95161ceb-f057-4b49-92d8-298403d066a9/scratchpad/case-r27audit/case/case-G7.md and the hunk /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/95161ceb-f057-4b49-92d8-298403d066a9/scratchpad/case-r27audit/hunk-02.diff. Read the specification /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md via sed on line ranges 95-135, 130-275, 275-340, 735-765, 760-805, 800-860, 2745-2775, 3430-3460, 3455-3500, 3670-3700, 826-834, and via grep/rg for: "R-CNF-01", "R-CNT-24", "R-CNF-13", "R-CNT-07", "distinct diagnostic", "capability ground(s)", "before other processing", "in order: the trailer", "version gate", "diverge", "restat", "the rule governs", "cross-refer". Ran one `tr`/`fold` whitespace-normalisation on lines 826-834 to defeat the hard wrap when checking the brief's quotation. Read nothing else — no docs/, no full.diff, no other hunk file, no conformance/, no registry.json, no git history, no web, and I did not list the case directory.

Context I did not ask for and did not act on: before I began, my runtime placed in context (a) the project CLAUDE.md pointer to AGENTS.md, and (b) an index of the maintainer's auto-memory files, whose entry titles reference this project's cadence, its gate board, its register, and prior workflow failures. I did not open AGENTS.md or any memory file, and no conclusion below derives from those titles; every claim is sourced to a line of spec/tarn.md I quote.

### Reasoning

Both halves of the finding fail, each to a sentence the brief did not consult.

SCOPE HALF — refuted by the mandated validation order. The brief's whole case rests on reading [R-CNT-07] "on its own", and its counterexample is "a major-7 file with a corrupt trailer magic". But [R-CNT-07]'s unimplemented-major clause is not a free-floating test; it is the third gate of an ordered sequence, and two separate places say so. §6.2 [R-CNT-06] (line 809): "A reader MUST validate, in order: the trailer magic; the trailer CRC; the version gate (§6.3) — only these touch fields whose positions are fixed across all majors ([R-CNT-24])". §19.1 step 2 (line 2761) names the same order and attaches the identifiers: "validate them in §6.2's fixed order — magic, trailer CRC, version gate, then the remaining field gates ([R-CNT-06], [R-CNT-07], [R-CNT-08])". So on the brief's own example the reader validates the trailer magic FIRST, rejects there on F8's ground, and never arrives at the version gate. [R-CNT-07] never fires. There is no file for which the two texts give conflicting instructions.

That is not a coincidence of one example; it holds across the whole reaching set. §21.2's derivation (line 3471) fixes that set as "F8, F14, F6 and both of F1's instances — each asserting an invariant [R-CNT-24] fixes in every major — and no other row". F8 (trailer magic), F14 (trailer CRC) and F1's trailer-magic instance are gates 1 and 2 of [R-CNT-06]'s order, ahead of the version gate. F6 and F1's front-block instance are governed by [R-CNT-04] (line 756), which puts them earlier still: a reader holding [0,16) resident "MUST verify the full block by byte equality before other processing, and MUST treat any mismatch as reject-file" — §19.1 step 1 repeats this ahead of step 2's trailer entirely. A reader that would have to fetch those bytes "MAY defer or omit the check", so it establishes no failure there either. Every reaching requirement is therefore disposed of before [R-CNT-07]'s version gate is reached.

Read against that, [R-CNF-13]'s "is owed where every reaching requirement is satisfied" is not a silent narrowing of another section's rule. It describes the state the ordered open guarantees at the exact moment [R-CNT-07] fires. The parenthetical inside [R-CNT-06] even states the reason the ordering exists — those gates "touch fields whose positions are fixed across all majors ([R-CNT-24])" — which is the same [R-CNT-24] test [R-CNF-13] uses to define reaching. The repair and the untouched rule are built on one mechanism, not two.

STRENGTH HALF — refuted by §2.1 and by the document's existing register text. The brief reads "is owed" as a duty replacing a SHOULD. §2.1 [R-CNF-01] (line 99) forecloses it: the BCP 14 keywords are to be interpreted as such "when, and only when, they appear in all capitals, as shown here". "is owed" is not one of the eleven listed words and is not capitalised, so it creates no MUST. Internal evidence in the very same sentence confirms deliberateness: the drafter wrote "A reader MUST apply every reaching requirement" and "MUST treat its failure as reject-file" in caps two clauses earlier, then declined caps here. And the grammatical object is "the distinct diagnostic [R-CNT-07] asks for" — the strength of what is owed is set by reference to [R-CNT-07], which asks for it at SHOULD. Corroborating, the document was already speaking of this same diagnostic in non-caps advisory terms in text this repair did not touch: §21.6, line 3686, "the diagnostic ought to distinguish the two". Non-caps advisory phrasing about this diagnostic is house style here, not an upgrade introduced by the repair.

The brief's supporting quotation from §2.4 is accurate ([R-CNF-12], line 295, "Deviation from a SHOULD is not a violation for this purpose") but does no work: it governs file conformance and certification, and a diagnostic string is reader behaviour, not a property of the bytes. Nothing in §2.3's or §2.4's conformance-class definitions makes a SHOULD deviation a reader-conformance failure either.

QUOTATION ACCURACY. The brief's [R-CNT-07] quotation is verbatim as far as it goes but stops mid-sentence at the em dash, dropping "— a reader that reports an unimplemented major as corruption misleads users into discarding files that current software reads." That clause is the SHOULD's stated consequence of deviation, which §2.1's Note requires of every SHOULD, and it is precisely the material a reader would weigh when judging whether the obligation had been restated at the wrong strength.

WHAT I SEARCHED FOR AND DID NOT FIND, in fairness to the finding: there is no general prose-versus-prose precedence rule in this document (§21.1's "where a row and the rule it cites diverge, the rule governs" is scoped to register rows, and §21.2 line 3472 invokes it only for its own restatement). So had a genuine divergence existed, nothing would have adjudicated it. It does not exist, for the ordering reason above.

ONE ADJACENT ISSUE I NOTED AND AM NOT GRADING, since it is not the finding briefed and the brief does not raise it: [R-CNF-13]'s "A reader MUST apply every reaching requirement to a file whatever major it declares" sits alongside [R-CNT-04]'s express permission for a non-resident reader to "defer or omit" the front-block check, which is a reaching requirement (F6, F1-front). Whether the new MUST is meant to override that residency exemption is not stated. I flag it only so it is visible; it is a different clause pairing than case G7 alleges and I did not test it to a verdict.

### Decisive quotes

Deciding sentence, §6.2 [R-CNT-06], line 809 (untouched by this repair): "A reader MUST validate, in order: the trailer magic; the trailer CRC; the version gate (§6.3) — only these touch fields whose positions are fixed across all majors (`[R-CNT-24]`)". This places the brief's counterexample — corrupt trailer magic — at gate 1, two gates before [R-CNT-07] can fire.

Corroborating, §19.1 step 2, line 2761: "validate them in §6.2's fixed order — magic, trailer CRC, version gate, then the remaining field gates (`[R-CNT-06]`, `[R-CNT-07]`, `[R-CNT-08]`)". Names [R-CNT-07] explicitly as the ordered third gate.

Closing the front-block half of the reaching set, §6.1 [R-CNT-04], line 756: a reader holding [0,16) resident "MUST verify the full block by byte equality before other processing, and MUST treat any mismatch as reject-file. A reader that would have to issue a further range request to obtain those bytes MAY defer or omit the check".

Fixing the reaching set, §21.2, line 3471: "deriving it there yields F8, F14, F6 and both of F1's instances — each asserting an invariant `[R-CNT-24]` fixes in every major — and no other row".

On the strength half, §2.1 [R-CNF-01], line 99: the keywords apply "when, and only when, they appear in all capitals, as shown here". And §21.6, line 3686, untouched: "the diagnostic ought to distinguish the two" — the document's pre-existing non-caps phrasing for this same diagnostic.

## Group G8 — CONFIRMED, byte-level False

### Disclosure

I read exactly three files: the finding brief /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/95161ceb-f057-4b49-92d8-298403d066a9/scratchpad/case-r27audit/case/case-G8.md, the hunk /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/95161ceb-f057-4b49-92d8-298403d066a9/scratchpad/case-r27audit/hunk-10.diff, and the specification /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md. I ran only sed/grep against the specification (regions 90-112, 130-260, 3380-3500, 3516-3522, 3573-3580, 3607-3616, 3684-3694, 3773-3790, 4090-4102, 4218-4232; greps for "rule governs", "restate", "governs", "§21.1", "21.1)", "R-CNF-13", "R-CNF-02", "R-CNF-01", and the §21 heading list). I did not read full.diff, other hunk files, docs/, conformance/, registry.json, git history, or the web, and I did not list the case directory.

Context I did not ask for did appear before I began: a project instruction file pointer (CLAUDE.md redirecting to AGENTS.md), an index of the maintainer's auto-memory notes with titles that name TARN working practice and register conventions, an MCP server instruction block, and a skills listing. I did not open any of the files those referenced and I drew no conclusion from them; every claim below rests on text I read in spec/tarn.md itself.

Note on hard wrapping: `grep -n "rule governs"` returns only lines 2028, 3407 and 3421 — it does NOT return the hunk's own occurrence, because that phrase wraps across lines 3472/3473 ("...diverge, the rule" / "governs (§21.1)"). I therefore verified the hunk text by reading lines 3460-3480 directly rather than relying on that grep.

### Reasoning

**The brief's quotations check out, in context.**

The hunk landed at spec/tarn.md lines 3468-3475, under "#### 21.2 File-scope violations" (line 3466) — the header the hunk file predicted, so no mismatch. The text now reads, verbatim: "Which rows reach a file declaring a format major other than 1 is decided by `[R-CNF-13]` (§2.3), and deriving it there yields F8, F14, F6 and both of F1's instances — each asserting an invariant `[R-CNT-24]` fixes in every major — and no other row; where this restatement and that rule diverge, the rule governs (§21.1)."

I read §21.1 in full (lines 3389-3465). It grants rule-over-restatement precedence exactly twice, and both times the object is something the §21.2 preamble is not:
- line 3406-3407: "but each row *restates* its governing rule, and where a row and the rule it cites diverge, **the rule governs**" — quantified over *rows*, and §21.1 defines a row two sentences earlier as "each row is one malformed condition". A preamble paragraph is not one.
- line 3419-3421: "§21.6's entries restate their governing rules on the same terms a row does, and where such an entry and the rule it cites diverge, the rule governs there too."

The brief's line numbers are off by one on the first citation (3406-3407, not 3405-3406) and it gives 3417-3421 in one place and 3419-3421 in another. Immaterial: the quoted strings are exact and complete, and nothing truncated changes their sense.

**I hunted for the sentence that would forecloseit and did not find one.**

Places I checked that could have decided it the other way:
1. `[R-CNF-01]` (line 106): "All text in this document is normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices identified as non-normative." The §21.2 preamble is plain prose, not a blockquote — so this repair did *not* land in a Rationale, and the failure mode the charter warns about is absent here. But [R-CNF-01] also does nothing to extend §21.1's precedence.
2. A general "summary versus requirement" precedence rule elsewhere. `grep -n "governs"` over the whole file returns 30 hits; the only two precedence-of-that-shape statements are §21.1's (rows, §21.6 entries) and `[R-EXT-05]` at line 1491, which is scoped to the registry/§10.2 table/Appendix C. `grep -i "restate"` returns six hits — 2743, 3406, 3419, 3472, 3778, 4224 — and none of 2743 (§19's step enumerations), 3778 (§21.9 limits, "a finding aid rather than an inventory — each is normative where the structure forcing it is defined") or 4224 (Appendix C, deferring to `[R-EXT-05]`) reaches a §21.2 preamble.
3. Whether "part of the register" might carry the precedence implicitly. §21.1 does say "The register — §21.2 through §21.5 (`[R-ERR-02]`) —", so the preamble sits inside the register. But §21.1's precedence sentence is quantified over *rows*, not over the register, so membership in the register does not deliver it.

**Two things push this from nit to real.**

First, the document demonstrably knows how to extend this precedence when it wants to. §21.1 says "The subsections after §21.5 are not part of the register and carry no rows", and then adds an express extension for §21.6 entries. That express extension is only necessary because the row-quantified sentence does not reach non-row structures on its own — which is precisely the reading that leaves the §21.2 preamble uncovered.

Second, the document has a distinct idiom for citing an *analogous* principle rather than a governing one. At line 1491-1492: "the registry is machine-readable convenience, never a second authority (§21.1 applies the same principle to the error register)." Where §21.1 supplies the warrant directly, the document uses a bare pointer, and I verified all three other bare "(§21.1)" pointers resolve exactly: line 2742 ("at the tier that row's *Detected* cell names") matches §21.1's Detected-column definition; line 3688 ("the register enumerates file-conformance violations") matches §21.1's opening sentence; line 4097 ("no reader is obliged to refuse anything") matches §21.1's verifier-detector paragraph. Hunk 10's is the one bare "(§21.1)" that does not.

**Why this is not a downgrade to a stylistic quibble, and not an upgrade past what it is.** The preamble's clause "where this restatement and that rule diverge, the rule governs" is normative on its own force under [R-CNF-01], so the precedence obtains regardless of the pointer. `[R-CNF-13]` at line 246 is real, does live in §2.3, and its closing sentence — "no §21 row restating it records such a file" — independently decides which rows reach. So no reader reaches a different verdict about any byte. The defect is confined to what the check names it: a citation that does not resolve to the proposition it is attached to, in text a reader is specifically invited to go check. Grading it PARTIAL would require the brief to have mis-described it, and it has not — its title, its detail and its own byte-level rationale all state exactly this.

I searched for, and could not find, any sentence anywhere in spec/tarn.md that grants rule-over-restatement precedence to register prose that is neither a row nor a §21.6 entry. That absence is the finding.

### Decisive quotes

§21.1, lines 3406-3407 (the precedence, quantified over rows): "but each row *restates* its governing rule, and where a row and the rule it cites diverge, **the rule governs**."

§21.1, line 3391 (what a row is): "each row is one malformed condition, with the outcome class its scope determines (§2.4)"

§21.1, lines 3417-3421 (the express extension, which is only needed because the row-sentence does not reach non-rows): "The subsections after §21.5 are not part of the register and carry no rows: neither this completeness clause nor the instance arithmetic below reaches §21.6's defined non-violations, §21.7's account of what no check detects, or §21.9's limits. §21.6's entries restate their governing rules on the same terms a row does, and where such an entry and the rule it cites diverge, the rule governs there too."

§21.2 preamble as repaired, lines 3468-3473: "Which rows reach a file declaring a format major other than 1 is decided by `[R-CNF-13]` (§2.3), and deriving it there yields F8, F14, F6 and both of F1's instances — each asserting an invariant `[R-CNT-24]` fixes in every major — and no other row; where this restatement and that rule diverge, the rule governs (§21.1)."

§10.2 / `[R-EXT-05]`, lines 1489-1492 — the document's own idiom for pointing at §21.1 as an *analogy* rather than a warrant: "the registry is machine-readable convenience, never a second authority (§21.1 applies the same principle to the error register)."

§2.3 / `[R-CNF-13]`, lines 242-246 — the rule that does independently decide the preamble's substance, which is why nothing byte-level turns on the bad pointer: "Every other requirement of this specification governs a structure this text defines for format major 1 alone; it is not assessed against a file declaring another major, no violation of it is established there, and no §21 row restating it records such a file."

§2.1 / `[R-CNF-01]`, lines 104-106 — the preamble is plain prose, so its precedence clause has force on its own: "All text in this document is normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices identified as non-normative."

## Refute A-02 (lens: overclaim scope) — DOWNGRADE_REFUTED

### Disclosure

I read only: /private/tmp/.../case-r27audit/case/case-A-02.md, hunk-06.diff, hunk-07.diff, and /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (via sed on lines 165-232, 230-330, 1020-1080, 1425-1496, 2255-2500, 3380-3424, 3555-3575, 3790-3820, 4212-4240). I ran: `grep -n "ranges over" spec/tarn.md` (4 hits: 2265, 3425, 3430, 3797); `grep -n "R-CNF-11\|R-CNF-03\|R-CNF-05\|R-CNF-08" spec/tarn.md`; `grep -n "the rule governs\|governs when\|diverge" spec/tarn.md`; and a python3 whitespace-normalising regex scan of spec/tarn.md for "whatever it stores" (0 hits), "whatever the layer stores" (0), "stores no tile" (2, neither in §17), "no stored tile" (1, §16), "declarations alone" (5), "stored or not" (1, §21.9), "vacuous"/"vacuously" (1 each, only the repaired sentence), "ranges over" (4). I read no docs/, no conformance/, no git history, no full.diff, no other hunk files, and did not list the case directory. CONTEXT I DID NOT ASK FOR: my runtime injected a CLAUDE.md pointer and an index of the maintainer's private memory files (titles referencing project cadence, gate boards, register/corpus relationships, and prior workflow-failure shapes), plus environment/git-status preamble showing recent commit subject lines that mention ADR numbers, a round number, and phrases about the register and an overflow ceiling. I disregarded all of it; no conclusion below derives from it, and every claim is anchored to a quoted line of spec/tarn.md. I also could not write the requested transcript file — the harness blocked the write with "Subagents should return findings as text" — so the full working transcript is folded into `reasoning` and `constructions_tried` below.

### Reasoning

SPLIT RESULT, stated precisely so it is not over-read: the REFUTED grade is overturned; the byte-level:False half of the grade should stand.

Q1 — real as text? YES, and the downgrader conceded it. §17 contains R-COD-01..11. Three range over no tile at all: [R-COD-03] constrains the layer record's codec field, [R-COD-09] its filter field, [R-COD-11] a verifier's certification. "Every rule in this section ranges over stored tiles" is false of each. The verifier's own words: "the first clause, read in isolation, is literally an overclaim: [R-COD-03], [R-COD-09] and [R-COD-11] do not range over tiles at all, stored or otherwise". It then graded REFUTED on the ground that the falsehood has no reachable consequence. My charter's test is exactly this: it established that reading (b) is not grammatically forced, not that the repaired text is correct. Those are different claims and only the first is a refutation of an OVERCLAIM finding.

Independent of the auditor and of the verifier, the document itself contradicts the repaired clause in normative prose. §21.9 (line 3797ff, no blockquote marker): "*Decoded size of one tile* ranges over a layer's **addressed** tiles, stored or not, exactly as `[R-COD-07]`'s cap is". That asserts a §17 rule ranges over tiles stored or not. The repair asserts every §17 rule ranges over stored tiles. Two normative sentences, flatly contrary. The verifier called this "corroborating rather than deciding"; understating a normative self-contradiction as "prose looseness" is itself the scope overclaim my lens was aimed at. (Its byte-level reach is A-01's subject; I do not lean on it for Q2.)

A-02 is also not absorbed by A-01. A-01's repair (stored -> addressed) leaves "Every rule in this section ranges over **addressed** tiles", still false for R-COD-03, R-COD-09, R-COD-11. A-02 names precisely the residue A-01's fix does not reach, so refuting it would leave a known-false universal quantifier standing after the sibling repair lands.

Q2 — byte-level? NO. I attacked the refutation's scope premise and found it genuinely overclaimed, but the overclaim does not flip the outcome.

The refutation's premise is "the deciders live outside §17". Both alleged deciders in fact route through §17: §7.4's table cell is literally `| codec | u16 | §17 (0 invalid) |` and `| filter | u16 | 1 = none, 2 = byte-shuffle (0 invalid; others per §17) |`, and [R-CNT-23]'s writer bar is "Writers MUST NOT emit a field violating a constraint in the table above" — for codec that constraint IS "§17". [R-EXT-03] says "A reader encountering either treats it as its space's rules require", delegating back to §17.2. And [R-EXT-05] subordinates §10.2 outright: "Where the registry, §10.2's table, and Appendix C diverge, the section that defines the space governs — the registry is machine-readable convenience, never a second authority" (Appendix C repeats it at line 4225). So the verifier's parenthetical calling [R-EXT-02] the table "which fixes the value sets independently of any §17 obligation" is wrong: §10.2 is a restatement and §17.2 is the authority.

Two textual facts nevertheless save the outcome. (1) Reading (b) can at most vacate an obligation; [R-COD-03]'s first sentence states a partition ("values 5 through 0x7FFF are reserved ... values ≥ 0x8000 are the experimental range"), and a definition is not the kind of thing "satisfied vacuously" — so 0x8000 stays an unassigned codec value under both readings. (2) [R-CNT-23] stipulates by apposition that such a value IS a table-constraint violation — "including a reserved or unassigned layout, codec, filter, index_encoding, or channel-type value" — with no tile quantifier anywhere in it, and §7.3 fixes that "unassigned" covers the experimental range. [R-EXT-03]'s colon clause names the outcome itself for "the value sets of ... §17.2, and §17.3". So under both readings the writer is barred and the reader rejects the layer; the disputed file is non-conforming either way and, per the charter's discriminator, the emittable set does not move.

I closed the one crack: [R-EXT-03]'s writer bar for experimental values is qualified ("in released software or published data") while [R-COD-03]'s is unconditional, so for an unreleased writer [R-EXT-03] alone would not bar codec 0x8000 — but [R-CNT-23] does, unqualified.

On [R-COD-11]: its MUST NOT is unconditional, so (a) and (b) do diverge on whether a verifier may certify a file with an all-sentinel layer whose codec it cannot execute. But not between conforming implementations: [R-CNF-03] says software declining a core codec "is not a conforming reader", and a verifier is a reader ([R-CNF-11]), so a conforming verifier can only fail to execute at a reserved/experimental value — where [R-CNT-23]/[R-EXT-03] already establish a violation and [R-CNF-11]'s priority clause ("a verifier that has established any violation reports *nonconforming*") fixes the same verdict under both readings. [R-CNF-11] also frames "cannot establish" as arising "where some requirement is one it is unable to check", which for a layer with no stored tile leans toward the refuter's reading.

Net: restore A-02 as a real textual defect (a false universal quantifier that a normative sentence in §21.9 directly contradicts, and that A-01's repair will not fix); leave byte-level at False.

### Constructions tried

A. All-sentinel layer, codec = 0x8000 (experimental) / codec = 5 (reserved) / codec = 0. FAILS as byte-level: [R-CNT-23]'s "reserved or unassigned ... codec ... value" apposition and [R-EXT-03]'s colon clause both bar the writer and force reject-layer under reading (b) too. File non-conforming under both readings; emittable set unmoved.

B. Same with filter = 3 (reserved) / filter = 0. FAILS identically; §10.2 fixes filter reserved = 3–0x7FFF outside §17, and [R-CNT-23] names "filter" in the same apposition.

C. Parasitism attack (my lens, the strongest one available): argue [R-CNT-23] is not independent because §7.4's codec cell is literally "§17" and the filter cell says "others per §17", so vacating §17's rule vacates the table constraint the writer bar consults; reinforced with [R-EXT-05] making §10.2 a mere restatement of §17.2. REAL as a criticism of the refutation's premise, but does NOT flip the verdict: reading (b) vacates an obligation, not [R-COD-03]'s partition sentence, and [R-CNT-23]'s apposition stipulates the instance directly without consulting any quantifier.

D. Unreleased-writer crack in [R-EXT-03] ("Writers MUST NOT emit files carrying an experimental value in released software or published data" — conditional for experimental, unconditional only for reserved). Real gap in that rule, but [R-CNT-23]'s writer bar has no such qualifier, so codec 0x8000 stays barred.

E. [R-COD-11] certification divergence: all-sentinel layer declaring an assigned-but-unimplemented codec (zstd), verifier that cannot execute it. Under (a) MUST NOT certify; under (b) may. FAILS the "two conforming implementations" gate: [R-CNF-03] makes such software not a conforming reader at all, and a verifier is a reader ([R-CNF-11]). Restricting to a conforming verifier forces a reserved/experimental value, where [R-CNF-11]'s established-violation priority yields "nonconforming" under both readings.

F. Actor enumeration per the charter: reader, writer, updater ([R-CNF-06]), creator/appender (§20), verifier. All reach the codec/filter field only through the §7.4 layer-record inline payload, so all hit [R-CNT-23]. No other declaration site for a codec or filter value exists in the document (checked).

G. "Leave the damaged structure out of the live state" move: superseded/slack layer record carrying the bad codec. Then no register row fires under EITHER reading, so no divergence — the move helps A-01-style constructions, not this one.

H. Deliberately NOT used: [R-COD-07]/L44, the lz4 decoded-size cap. It IS free of any external decider (codec 4 is assigned, so [R-CNT-23], [R-EXT-02] and [R-EXT-03] never reach it; §21.9's limits are explicitly non-invalidating — "A file exceeding any of these remains conforming"), and vacating it would move the emittable set. But it ranges over addressed tiles, is A-01's subject, is expressly excluded by A-02's reporter, and was expressly not evaluated by the downgrader. Refuting A-02 with it would be borrowing a sibling's construction, so I left it out of the Q2 answer and record it here only to show the boundary I respected.

### Decisive quotes

1. The repair, spec/tarn.md 2264-2267 (not in a blockquote): "The owning scope of a layer's codec and filter declarations is the layer; the owning scope of one stored tile's payload under them is the tile (§2.4). Every rule in this section ranges over **stored** tiles — a tile whose index entry is the sentinel is not stored (§3.1, `[R-IDX-02]`), carries no payload under any codec, and satisfies these rules vacuously."

2. DECIDES Q1 — spec/tarn.md §21.9, line 3797ff, normative prose, no ">" prefix: "*Decoded size of one tile* ranges over a layer's **addressed** tiles, stored or not, exactly as `[R-COD-07]`'s cap is: a tile's decoded size is a function of the layer's declarations alone (`[R-SER-07]`), so an addressed tile has one whether or not its index entry is the sentinel." [R-COD-07] is a rule in §17; this sentence says it ranges over tiles stored or not. Directly contrary to the repair's first clause.

3. Q1 conceded by the downgrader itself (case-A-02.md, verdict section): "The first clause, read in isolation, is literally an overclaim: [R-COD-03], [R-COD-09] and [R-COD-11] do not range over tiles at all, stored or otherwise, so 'Every rule in this section ranges over stored tiles' is not true of them."

4. The refutation's scope premise is overclaimed — spec/tarn.md 1489-1493, [R-EXT-05]: "Where the registry, §10.2's table, and Appendix C diverge, the section that defines the space governs — the registry is machine-readable convenience, never a second authority (§21.1 applies the same principle to the error register)." So §10.2's partition table is a restatement subordinate to §17.2, not the independent authority the refutation called it. Appendix C, line 4225: "where any of the three diverge the section defining the space governs".

5. And spec/tarn.md §7.4 table: "| codec | u16 | §17 (0 invalid) |" and "| filter | u16 | 1 = none, 2 = byte-shuffle (0 invalid; others per §17) |" — [R-CNT-23]'s bar is "Writers MUST NOT emit a field violating a constraint in the table above", and for codec that constraint is "§17" itself.

6. WHY Q2 STILL FAILS — spec/tarn.md 1064-1074, [R-CNT-23]: "a reader MUST treat any such violation — including a reserved or unassigned layout, codec, filter, index_encoding, or channel-type value (the value sets are §14, §17, §15, and §12's subjects) ... — as a validity error at layer scope". The apposition names the instance directly and carries no tile quantifier; §7.3 (line 1021-1022) fixes the term: "All other type values are unassigned (registry and experimental ranges: §10)."

7. WHY Q2 STILL FAILS — spec/tarn.md 1462-1471, [R-EXT-03]: "A reader encountering either treats it as its space's rules require: a validity error at the owning scope for the value sets of §11.4, §12.2, §14.1, §15.1, §17.2, and §17.3".

8. WHY THE [R-COD-11] LEG FAILS — spec/tarn.md 167-173, [R-CNF-03]: "MUST handle every codec and filter that §17 designates as core ... software that declines to support a core codec, a core filter, either channel layout, a core sample type, or an assigned user-metadata encoding is not a conforming reader"; and [R-CNF-11]: "a verifier that has established any violation reports *nonconforming*, however many requirements it was unable to check".

### Missing sentence

The document has no sentence saying that §17's declaration-ranging rules bind whatever the layer stores — I searched "whatever it stores", "whatever the layer stores", "stores no tile", "declarations alone", and "vacuous"/"vacuously" over the whitespace-normalised file; the only occurrence of "vacuously" in the entire specification is the repaired sentence itself. §17 needs, in place of "Every rule in this section ranges over stored tiles": "The payload rules of §17.1 through §17.3 ([R-COD-01], [R-COD-02], [R-COD-04] through [R-COD-06], [R-COD-08], [R-COD-10]) range over stored tiles, and a tile whose index entry is the sentinel is not stored (§3.1, [R-IDX-02]), carries no payload under any codec, and satisfies those rules vacuously. The codec and filter value-set rules ([R-COD-03], [R-COD-09]) and the certification rule ([R-COD-11]) bind the layer's declarations whatever the layer stores, and [R-COD-07]'s cap ranges over the layer's addressed tiles, stored or not (§21.9)." Without the second sentence, the repair's "these rules" is anaphoric to a universal quantifier the document elsewhere (§21.9) states to be false, and only reasoning found nowhere in spec/tarn.md — that the vacuity clause's grammatical subject is a tile and so cannot be re-predicated of a layer's declaration field — keeps the permissive reading off the table.

## Refute X-03 (lens: vacuous satisfaction) — DOWNGRADE_STANDS

### Disclosure

Read: /private/tmp/.../case-r27audit/case/case-X-03.md, hunk-06.diff, hunk-07.diff, and spec/tarn.md only. Nothing else was read — no docs/, no full.diff, no other hunk files, no registry.json, no git, no web, no directory listing.

Commands run (all against spec/tarn.md alone): sed -n on 2255-2480 (all of §17), 1400-1490 (§10), 1030-1080 (§7.4 table + [R-CNT-23]), 165-235 ([R-CNF-03]/[R-CNF-04]/[R-CNF-05]/[R-CNF-11]), 275-300 (§2.4/[R-CNF-08]/file-conformance), 3380-3440 (§21.1), 3555-3575 (L33-L49), 3592-3602 (T13-T23), 3790-3820 (§21.9), 2495-2515 ([R-MTA-03]), 2555-2575; grep -n for "sentinel", "R-CNF-05|R-CNF-11|R-CNF-03", "R-COD-03|R-COD-09|R-COD-11|R-COD-04|R-COD-07", "validity error"; awk first-3-characters probes at 2261-2270 and 3788-3806 to test for blockquote prefixes.

CONTEXT I DID NOT ASK FOR: my runtime injected a project instruction file (CLAUDE.md pointing to AGENTS.md) and an index of the maintainer's memory files naming several TARN working notes. I did not open any of them and drew no conclusion from their titles; I am naming their appearance, not their contents.

I attempted to write the working transcript to case/analysis-X-03-vacuous-satisfaction.md as instructed; my harness blocked writing analysis .md files, so the full transcript is reproduced in the fields below rather than on disk.

### Reasoning

BLOCKQUOTE CHECK FIRST. awk first-3-chars at 2263-2268 returns The/lay/the/til/`[R/rul — no ">" — so the disputed sentence is normative prose, not a Note. awk at 3796-3805 returns The/dif/**a/a t/(`[/ent/has/ove/act/Eit — §21.9's counter-sentence is normative too. Both sides of any conflict I find carry force.

QUESTION 1 — REAL AS TEXT: YES, and the downgrader conceded it. Its own closing paragraph says "'Every rule in this section ranges over stored tiles' is literally inaccurate as to [R-COD-03], [R-COD-09] and [R-COD-11], whose subject is a layer declaration." So the refutation never established that the repaired sentence is correct; it established that an incorrect sentence is harmless. Those are the two different claims my charter names, and only the first is a refutation of the text. A normative universal that is false about four of its own section's eleven rules is an OVERCLAIM by the check's own definition. The grade REFUTED ("there is no defect, only an imprecise sentence") overstates what the argument earned.

QUESTION 2 — BYTE-LEVEL: NO, for X-03's distinct targets. I built every construction the vacuous-satisfaction lens offers and each one is closed by rules the §17 preamble cannot reach.

C1. Fully sparse layer, codec 0x8000. [R-CNT-23] sits in §7.4, outside §17, with no tile quantifier, and names the case itself: a reader MUST treat "a reserved or unassigned ... codec ... value" as a validity error at layer scope. The value set is fixed outside §17 by [R-EXT-02]'s table row "codec (§17.2) | u16 | 1–4 | 5–0x7FFF | ≥ 0x8000", and [R-EXT-03] states the outcome by section number for "the value sets of §11.4, §12.2, §14.1, §15.1, §17.2, and §17.3". Owning scope is the layer, from the preamble sentence hunk 6 left standing. I then closed the writer half, which the downgrader asserted rather than traced: [R-CNF-08] converts "validity error at layer scope" to reject-layer; §2.3 states "A file is conforming only if it satisfies every requirement at every scope"; therefore the file is nonconforming and [R-CNF-05] bars every conforming writer under BOTH readings. The emittable set does not move. The register route survives too: even granting §21.1's "where a row and the rule it cites diverge, the rule governs" so that row L43 narrows with [R-COD-03], [R-CNT-23]'s own prose is unnarrowed and still obliges rejection.

C2. Fully sparse layer, filter 3 or ≥0x8000. Closed harder than C1 — the §7.4 table states the assigned set inline ("filter | u16 | 1 = none, 2 = byte-shuffle (0 invalid; others per §17)"), so [R-CNT-23] does not even consult §17 for it.

C3. codec 0 / filter 0. [R-EXT-02]: "Value 0 is invalid in every space above"; §7.4 cell "§17 (0 invalid)".

C4. [R-COD-11] as a verdict divergence — the angle I judged most promising, since [R-CNF-11] lists "when it cannot execute a codec or filter ([R-COD-11])" as a cannot-establish ground. Construction: fully sparse layer declaring codec 3, verifier that cannot execute zstd; strict reading MUST NOT certify, vacuous reading may certify. It fails because no conforming verifier can occupy that position: [R-CNF-03] requires every core codec, §17.4 itself says "For a conforming reader that position arises only at a reserved or experimental value", and at such a value C1 already makes the file nonconforming, whereupon [R-CNF-11]'s "An established violation takes priority" fixes the verdict as nonconforming under both readings. Independently, [R-CNF-11]'s own gate — cannot-establish applies "where some requirement is one it is unable to check" — is not met when nothing is stored to decode, so the vacuity is substantively right. Two conforming verifiers cannot differ.

C5. Downstream chain. [R-MTA-03] leans on [R-COD-11] for the zstd decoder but states the duty itself ("Both assigned encodings are core: a conforming reader MUST be able to decode encoding 2"), so narrowing [R-COD-11] does not unpin it.

C6. Actor sweep, per the charter's second move. Creator, appender, updater, reader, verifier. An updater that unstores every tile of a layer (§20's "unstoring a tile so its entry becomes the sentinel") manufactures the vacuity antecedent inside a live commit, but [R-CNF-06] binds it to every writer requirement and C1–C3 close the only declarations it could then change. No actor, scope or commit shape reaches a different structure.

C7. The [R-COD-04] half of the finding. Hunk 7 as landed reads "A **non-sentinel** index entry's length therefore MUST equal the tile's decoded size", and row T14 independently says "a non-sentinel index entry's length". The auditor concedes §15.2 makes stored and non-sentinel coextensive, so the hunks agree; the residue is an argument about what hunk 7's author "did not trust", which is inference about drafting process, not about the document.

C8 — the one place the blanket does move bytes, and why it is not X-03's. A layer with one addressed tile whose decoded size exceeds 0x7E000000, codec 4, entry the sentinel: strict [R-COD-07] bars the declaration ("any of whose **addressed** tiles"), the blanket vacates it, and no §7.4/§10 backstop exists because this is not a value-set rule. §21.9 says the opposite of the blanket in normative prose, and row L44 says "addressed tiles". That is byte-level — but X-03's own Detail assigns it to X-02 ("[R-COD-07]: quantified over addressed tiles (see X-02)"), so it is not this framing's distinct contribution. It does falsify the downgrader's summary claim that the imprecision "is fully absorbed by §7.4 and §10" — §7.4 and §10 say nothing whatever about the lz4 cap — but the claim it falsifies is a claim about a rule X-03 handed to another finding.

So: the downgrade's byte-level half was actually established, not merely asserted, and my independent trace of the writer chain strengthens it rather than breaking it. The grade half is overstated by the downgrader's own concession — this is a true overclaim in normative text, correctly identified, just without force on its own targets. Byte-level downgrade stands.

### Constructions tried

C1 — fully sparse layer (every index entry the sentinel), codec = 0x8000 experimental. CLOSED by [R-CNT-23] + [R-EXT-02] + [R-EXT-03] on the reader side, and by [R-CNF-08] → §2.3 → [R-CNF-05] on the writer side. Nonconforming under both readings; emittable set static.

C2 — same layer, filter = 3 (reserved) and filter = 0x8000. CLOSED more strongly: the §7.4 table states filter's assigned set inline, so the backstop does not consult §17 at all.

C3 — codec = 0, filter = 0. CLOSED by [R-EXT-02]'s "Value 0 is invalid in every space above" and the §7.4 cells.

C4 — [R-COD-11] verdict divergence: fully sparse layer, codec 3, verifier lacking zstd. Strict = MUST NOT certify, vacuous = may certify. FAILED as byte-level: [R-CNF-03] makes all four codecs core so no conforming verifier lacks one; §17.4 confines the position to reserved/experimental values, where C1 already makes the file nonconforming and [R-CNF-11]'s violation-takes-priority rule fixes the same verdict under both readings; and [R-CNF-11]'s own "unable to check" gate is unmet where nothing is stored.

C5 — chain through [R-MTA-03], which cites [R-COD-11] for the zstd decoder duty. CLOSED: [R-MTA-03] states the duty itself.

C6 — actor sweep (creator, appender, updater, reader, verifier), including an updater that unstores every tile of a live layer so the vacuity antecedent is created inside a commit rather than at file creation. CLOSED: [R-CNF-06] binds the updater to every writer requirement; C1–C3 close the declarations reachable that way.

C7 — [R-COD-04] warrant mismatch. NOT A DEFECT: hunk 7's "non-sentinel" is in place at 2300-2304 and row T14 carries it independently; the auditor concedes the two hunks are consistent.

C8 — [R-COD-07] lz4 cap on a layer with an addressed-but-unstored oversized tile. GENUINELY BYTE-LEVEL and unbackstopped, with §21.9 contradicting the blanket in normative prose — but X-03's own text assigns it to X-02, so it is not this framing's distinct defect. Importing it would be manufacturing a refutation.

C9 — register-route attack: assume §21.1's "where a row and the rule it cites diverge, the rule governs" narrows rows L43/L45 along with [R-COD-03]/[R-COD-09], so [R-CNF-04]'s register-driven detection duty lapses. FAILED: [R-CNT-23]'s reader clause is prose in §7.4 and binds independently of any row.

### Decisive quotes

1. The downgrader's own concession, which is why REFUTED is the wrong label even though not-byte-level is the right call: "'Every rule in this section ranges over stored tiles' is literally inaccurate as to [R-COD-03], [R-COD-09] and [R-COD-11], whose subject is a layer declaration."

2. spec/tarn.md §7.4, [R-CNT-23], lines 1071-1078 — outside §17, no tile quantifier, names the case: "a reader MUST treat any such violation — including a reserved or unassigned layout, codec, filter, index_encoding, or channel-type value (the value sets are §14, §17, §15, and §12's subjects) ... — as a validity error at layer scope".

3. spec/tarn.md §10.2, [R-EXT-02], table row and closing line — the value set exists outside §17: "| codec (§17.2) | u16 | 1–4 | 5–0x7FFF | ≥ 0x8000 |" and "Value 0 is invalid in every space above."

4. spec/tarn.md §10.3, [R-EXT-03] — states the outcome by section number rather than deferring to §17: "A reader encountering either treats it as its space's rules require: a validity error at the owning scope for the value sets of §11.4, §12.2, §14.1, §15.1, §17.2, and §17.3".

5. The writer half the downgrader asserted and I traced — spec/tarn.md §2.4, [R-CNF-08], lines 281-284: "The phrase 'a validity error at the owning scope' means the reader outcome for that scope: file → reject-file, layer → reject-layer, tile → reject-tile." And §2.3, lines ~290-292: "A file is conforming only if it satisfies every requirement at every scope". With [R-CNF-05] "A writer MUST emit only conforming files", the disputed file is unemittable under BOTH readings. This is the decisive text: the disputed file is not conforming, so the emittable set does not move.

6. Closing C4 — spec/tarn.md §17.4, lines 2460-2464: "For a conforming reader that position arises only at a reserved or experimental value, every assigned codec and filter being core: it rejects the layer (`[R-COD-03]`, `[R-COD-09]`); software unable to execute an assigned codec or filter is not a conforming reader (`[R-CNF-03]`)." Plus [R-CNF-11], line ~211: "An established violation takes priority: a verifier that has established any violation reports *nonconforming*".

7. Blockquote probes proving both the repair and its §21.9 counter-sentence are normative: awk first-3-chars, lines 2263-2268 → "The","lay","the","til","`[R","rul"; lines 3796-3805 → "The","dif","**a","a t","(`[","ent","has","ove","act","Eit". No ">" in either range.

8. The sentence that falsifies "fully absorbed by §7.4 and §10", though for a rule X-03 defers — spec/tarn.md §21.9, lines 3797-3801: "*Decoded size of one tile* ranges over a layer's **addressed** tiles, stored or not, exactly as `[R-COD-07]`'s cap is: a tile's decoded size is a function of the layer's declarations alone (`[R-SER-07]`), so an addressed tile has one whether or not its index entry is the sentinel."

### Missing sentence

The document states precedence for a register row against its governing rule (§21.1, "where a row and the rule it cites diverge, the rule governs") and for the registry against §10.2 and Appendix C (§10.4), but nowhere for one normative sentence of this specification against another. §17's new preamble and §21.9 now assert opposite quantifiers for the same rule, and the preamble and [R-COD-03]/[R-COD-09]/[R-COD-11]'s unquantified MUSTs disagree about their own subjects, with no tiebreak anywhere. The missing sentence, which belongs in §2.1 or §2.2: "Where a scoping statement in a section's preamble and an individual requirement in that section disagree about the structures the requirement ranges over, the requirement's own stated subject governs." Absent that, resolving X-03 depends on reasoning — the downgrader's "the vacuity clause's operative subject is a tile, not a layer" — that appears nowhere in spec/tarn.md.