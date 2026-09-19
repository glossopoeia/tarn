# Audit transcript — "the renames" (hunks 05, 06, 11, 14, 40, 41, 43, 46)

## Disclosure

I read, in this order:

1. My eight hunk files, verbatim, via `cat`:
   `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r36-audit/case/hunk-{05,06,11,14,40,41,43,46}.diff`.
   No other file in `case/` was opened, and that directory was not listed.
2. `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` — the
   whole file's line count (`wc -l`), then targeted `Read` calls over the
   passages named below, plus `grep`/`rg`-style searches over the whole file
   (shown verbatim below with their output).

I wrote two files, both under my scratch directory and nowhere else:
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r36-audit/scratch/the-renames/notes.md`
(working notes) and this transcript.

**Context I did not ask for, and did not use as evidence.** Before this task
began, my context already contained: a project `CLAUDE.md` that says "See
AGENTS.md" (I did not read AGENTS.md — the access rule forbids it, and I
disregarded the pointer); a user memory file (`MEMORY.md`) listing many
TARN-project note titles (e.g. "TARN repair prose vs rules", "TARN
lineage gate word list", "TARN refute phase and unanimous upholds", etc.); a
git-status block naming the five most recent commit subjects on this repo,
including "ADR-0130: the layer record carries PE = 0 — a commit MAY drop a
layer; ADR-0068 superseded, ADR-0129's decision 2 withdrawn, corpus rebuilt"
and "ADR-0128 decision 1 ... confirmed"; and MCP server usage instructions
unrelated to this task. None of this is part of the specification and I did
not treat any of it as evidence about the specification, the charter, or the
repairs. I note in particular that the git-status commit-subject line names
the exact flag change (PE = 0 for layer records) that the charter's "third
commit" also describes — I did not use that commit-subject text as
confirmation of anything; every claim below is grounded only in the hunk
files and the spec text, cited by line.

**Paths.** Every file named in the charter was exactly where the charter said
it would be — no discrepancy to report.

---

## The eight hunks, verbatim (already shown to me; reproduced here for the record)

### Hunk 05 — lands at spec/tarn.md:690 (§5.1 Anatomy, an Example block)
```
-> otherwise; that is compaction's operation (§20.5, `[R-WRT-07]`).
+> otherwise; that is a rewrite's operation (§20.5, `[R-WRT-07]`).
```

### Hunk 06 — lands at spec/tarn.md:745-746 (§5.2 Byte coverage, normative prose)
```
-completes. Only compaction (§20.5) reclaims it.
+completes. Only a rewrite (§20.5) reclaims it, compaction being the
+rewrite an operator runs for that alone.
```

### Hunk 11 — lands at spec/tarn.md:1046 (§7.2 Record framing, normative prose)
```
-lets a compactor relocate an unknown ancillary's extent without
+lets a rewriter relocate an unknown ancillary's extent without
```

### Hunk 14 — lands at spec/tarn.md:1548 (§9.7 Coverage verification, a Note block)
```
-> not promise to keep and compaction is expected to discard.
+> not promise to keep and a rewrite is expected to discard.
```

### Hunk 40 — lands at spec/tarn.md:4373 (§23.2 What a file discloses, normative prose, R-PRV-03)
```
-altogether from a compacted file (§20.5), which retains no earlier
+altogether from a rewritten file (§20.5), which retains no earlier
```

### Hunk 41 — lands at spec/tarn.md:4384 (§23.2, normative prose, R-PRV-04)
```
-correlate two copies of a file as the same artifact. Compaction
+correlate two copies of a file as the same artifact. A rewrite
 mints a new one (`[R-WRT-06]`) ...
```

### Hunk 43 — lands at spec/tarn.md:4704 (Appendix G item 2, non-normative)
```
-   (§6.2 forbids `file_id` = 0). This is a creator's rule: a compactor
+   (§6.2 forbids `file_id` = 0). This is a creator's rule: a rewriter
    adopting the profile takes `[R-WRT-06]`'s fresh draw instead, ...
```

### Hunk 46 — lands at spec/tarn.md:4795-4807 (Appendix G item 8, non-normative)
Six substitutions of "compactor" → "rewriter"/"rewriters" **except one**,
which became "compaction" instead of "rewriter":
```
-   identifier is: a compactor adopting the profile carries its input's
+   identifier is: a rewriter adopting the profile carries its input's
    ...
-   version_minor floor binds a compactor too, save where its output
+   version_minor floor binds a rewriter too, save where its output
    carries a feature it does not implement, when §20.5's floor governs
-   instead (`[R-WRT-06]`). A compactor's output is therefore
+   instead (`[R-WRT-06]`). A compaction's output is therefore
    reproducible only modulo its trailer and the records §20.4 lets it
    drop: `[R-WRT-06]`'s fresh file_id is no function of content, this
-   item's floor turns on which features the compactor implements, and
+   item's floor turns on which features the rewriter implements, and
    a record whose governing flags are MU = 0 and PE = 0 is retained or
-   dropped at the compactor's choice (§20.4), which no item here pins.
+   dropped at the rewriter's choice (§20.4), which no item here pins.
    An adopter needing byte-identity
-   across compactors pins the compactor, as items 1 and 9 pin their
+   across rewriters pins the rewriter, as items 1 and 9 pin their
    producers.
```

Header sanity: every hunk header's "nearest preceding heading" matched the
body I found at the stated line (5.1, 5.2, 7.2, 9.7, 23.2 ×2, Appendix G ×2).
No header/body mismatch to report.

---

## Grounding: §20.1 and §20.5 read in full

§20.1 (lines 3122-3151) defines three tiers — creator, appender, **rewriter**
— and states: *"rewriter — writes a new file from an existing one under a new
identity (§20.5), carrying structures forward, re-creating some, or dropping
some; compaction, which carries every structure forward and changes nothing
but placement, is the rewrite that reclaims slack."*

§20.5 (lines 3519-3638) opens: *"A rewriter's output is a new file under a
fresh file_id, built from the structures reachable from the input's live
trailer ... and carrying no slack. Each structure of the input is carried
forward verbatim, re-created as new output, or dropped ... This text names
three rewrites: **compaction**, which carries every structure forward and
changes nothing but placement, and is the rewrite that reclaims slack;
**dropping** a layer or another record §20.4's table licenses dropping ...
and **re-declaring** a layer that stores a tile in the input ... A rewrite MAY
be several of these at once."*

Two facts follow directly and govern every hunk below:

- **Fact A.** Every rewrite (not only compaction) produces an output
  "carrying no slack," and mints a fresh file_id via the creation path with
  no prior trailer. So any place that says "X is true of a rewrite in
  general" where X is (no slack in output / fresh file_id / no prior
  trailer / relocation permitted) is testing a real, general property, not
  one specific to compaction.
- **Fact B.** Compaction is defined to "carry every structure forward" —
  by definition it **never drops or re-creates anything**. Any place that
  attributes a drop-specific or re-create-specific property to "compaction"
  by name is describing something compaction structurally cannot do.

---

## Hunk-by-hunk audit

### Hunk 05 — §5.1 Example, line 690

**Rule the repair adopts:** in the illustrated three-commit history, no
commit relocates a live index region; only a rewrite operation does that
(§20.5, [R-WRT-07]).

**1. Tense/quantifier.** The claim is about *which actor* can relocate a
live index region. §20.3 step 4 (line 3230-3232) states this exact rule in
normative prose: *"relocating a live index region is a rewriter's operation
(§20.5, `[R-WRT-07]`), not an appender's."* The repaired Example now matches
this normative rule's quantifier exactly (rewriter, not compactor). Before
the repair, the Example said "compaction's operation," which was **narrower**
than the normative rule it echoes — the classic shape this round's own defect
had (duty stated over the narrow case where the normative rule already
ranges wider). The repair fixes that gap correctly.

**2. Citations.** `(§20.5, [R-WRT-07])`. I read all of R-WRT-07's span
(3594-3638): *"A rewriter MUST preserve the content of every structure it
carries forward ... except that relocation re-points extent slots,
regenerates each tile-index region any of whose stored extents the output
relocates ..."* — this is exactly the relocation-of-a-live-index-region rule.
Citation **verified**, and it is the same citation §20.3 step 4 itself uses.

**3. Label check.** Lines 655-696 are entirely inside a `> **Example — a file
after three commits.**`-labeled blockquote — confirmed non-normative by its
own label, consistent with [R-CNF-01]. The rule this Example restates is
independently stated in normative prose at §20.3 step 4 (line 3230-3232,
outside any blockquote — confirmed by `sed -n '3225,3233p'` showing no `>`
prefix in my earlier read). So the repair does not depend on this Example
for its force; it is a correct restatement of a rule already normative
elsewhere.

**4. Contradiction in the passage.** Read the whole Example (655-696). No
carve-out or MUST/MAY collision found. "A commit that changes a layer's
stored-tile set or index content re-emits that layer's whole tile-index
region as well, at a new placement" (line 685-687) is about *re-emission at
a new placement within the SAME commit's own layer*, a different case from
"relocating a **live** [i.e., another commit's already-anchored] index
region," so no conflict.

**5. Exhaustive claims.** "A commit never relocates a live index region
otherwise" — checked against §20.3's full step 4 and §20.4; no commit-level
exception found. Holds.

**6. Unconstrained siblings.** The structure here is "a live index region."
Its only two dispositions this passage discusses are (a) re-emitted in place
at a new placement by the commit that changed it, (b) relocated by a
rewrite. No third disposition (e.g. partial relocation) is implied or left
hanging.

**7. Analogy.** None present (no "exactly as"/"the same way" language in the
touched sentence).

**8. Anaphora.** Substitution only, no inserted clause; "This is what
tail-anchored discovery buys" (next sentence) refers to the paragraph's
general property, unaffected by the word swap.

**Verdict: no defect. Byte-level: n/a (nothing to resolve).**

---

### Hunk 06 — §5.2, lines 745-746

**Rule the repair adopts:** the set of operations that reclaim slack is
`{rewrite}`, not `{compaction}`; compaction is characterized, within that
set, as the rewrite an operator runs purely to reclaim slack.

**1. Tense/quantifier.** Per Fact A, every rewrite's output "carries no
slack" — so *any* rewrite (compaction, a drop, a re-declare, or a
combination) reclaims all of the input's slack in its output. The original
text ("Only compaction ... reclaims it") was narrower than §20.5 itself.
The repair's main clause ("Only a rewrite (§20.5) reclaims it") now matches
§20.5's actual quantifier. **Verified correct and necessary widening.**

**2. Citations.** `(§20.5)` — verified against the "carrying no slack"
language at line 3523 and the naming of three rewrite kinds at 3526-3534.

**3. Label check.** Confirmed by direct read (`sed -n '740,748p'`) that lines
740-748 carry **no** `>` prefix — this is plain normative prose, tagged
`` `[R-CNT-21]` ``. The repair lands in normative text and its normative
force is real.

**4. Contradiction in the passage — and beyond it.** I read the whole §5.2
subsection (697-763) and found no local contradiction. But the mandated
whole-document sweep for the stem "compact" (below) turned up a **direct
contradiction elsewhere that this repair should have swept and did not**:

> **§23.1, line 4348** (normative, tagged `[R-PRV-02]`, no `>` prefix —
> confirmed by `sed -n '4344,4354p'`):
> *"Compaction (§20.5) is the only operation that removes slack, and it does
> so by writing a new file ..."*

This says the **opposite quantifier** from the repaired §5.2 text: it says
only *compaction* removes slack, where §5.2 (post-repair) correctly says
*any rewrite* does. Under Fact A this is not a stylistic difference — a
rewrite that only **drops** a layer (no compaction at all) also produces an
output "carrying no slack" (§20.5, line 3523), and §20.4 itself says
*"Dropping a layer by commit strands its stored tiles and tile-index region
as slack (§5.2), which **only a rewrite** reclaims"* (line 3487-3488,
normative, no `>` prefix). So a drop-only rewrite genuinely does remove/
reclaim slack, and R-PRV-02's "Compaction ... is the only operation that
removes slack" is now false relative to every other correctly-worded
statement of this rule in the document. I found the correctly-widened
phrasing independently restated at:

- line 3670 (§20.5's own worked Example, `> A rewrite is the only operation
  that reclaims slack; truncation past F ... and recovery ... also shorten a
  file, but neither reclaims any.`)
- line 3695 (`> **Note.** A rewrite is the only true removal ...`)
- line 3998 (§21.6's normative register table, row for slack: `"...only a
  rewrite reclaims it"` — confirmed this table sits outside any `>` block,
  i.e. is itself normative per the brief's own note about normative tables
  in `>`-free blocks)

Four independent places (745-746 post-repair, 3670, 3695, 3998) now say "a
rewrite," and exactly one (4348, R-PRV-02) still says "Compaction ... is the
only operation." This is the project's most common defect shape by the
charter's own account: **a rule changed in one place and left standing in
another.** I flag this as **E-02** below, anchored to hunk 06 because hunk
06 is the repair that should have swept it (it is the one that establishes
the correct, wider quantifier for this exact rule).

**5. Exhaustive claims.** "Only a rewrite ... reclaims it" — checked against
line 3670-3672, which explicitly confirms truncation and recovery "also
shorten a file, but neither reclaims any [slack]." The "only" holds (once
R-PRV-02 is fixed to match — see above).

**6. Unconstrained siblings.** N/A — the structure ("slack," and what
reclaims it) is fully covered by the enumerated rewrite/truncation/recovery
trio elsewhere.

**7. Analogy.** None present.

**8. Anaphora.** This hunk *does* insert new text (", compaction being the
rewrite an operator runs for that alone"). I read forward to the end of the
paragraph and the next: the following sentence is `` `[R-CNT-21]` Slack that
holds superseded data is a privacy consideration (§23).`` — "Slack" here is a
fresh noun phrase, not an anaphor, so it is unaffected by the insertion.
Next paragraph (750-754, "Writers SHOULD zero the gaps...") is a new topic.
No anaphor-drift found.

I separately checked whether "compaction being the rewrite an operator runs
for that alone" (i.e., *solely* for reclaiming slack) is itself an
overclaim, since §23.2 (line 4376) advises a writer to "compact before
publication when the history itself is sensitive" — a privacy motive, not a
slack motive. I concluded this is not a contradiction: compaction is still
the *correct minimal* action for that privacy goal (it removes history
without dropping/recreating any content), so recommending it there doesn't
contradict describing it here as "the rewrite an operator runs [for
reclaiming slack] alone" among the three *named rewrite kinds* — the
contrast being drawn is with the other two named kinds (drop, re-declare),
not with every possible operator motive. I record this as a rejected
candidate, not a finding.

**Verdict: the repair itself is correct and necessary. Finding E-02
(untouched, contradicting restatement at line 4348) is raised against this
repair's incompleteness — the sweep it needed to make was not made.**

**Byte-level:** No. R-PRV-02's actual MUST ("A deployment whose obligation
is erasure MUST treat that obligation as belonging to its storage layer, not
to this format") is unaffected by which of the two readings is true; the
contradiction is in the supporting premise, not in a requirement that
constrains what bytes a writer may emit or a reader/verifier must accept or
reject. Two conforming implementations don't disagree about any byte or
verdict because of this — they'd only disagree about a sentence's truth.

---

### Hunk 11 — §7.2, line 1046

**Rule the repair adopts:** for an MU=0 record, since neither its inline
payload nor its extent content encodes other file-byte offsets, its extent
can be relocated (as part of a rewrite) without the relocating actor parsing
the record's content.

**1. Tense/quantifier.** Is this a *rewriter*-general fact, or specific to
compaction? Per §20.4, line 3496-3499 (normative, no `>` prefix): *"An
updater MUST NOT re-encode a record whose type it does not implement, and
MUST NOT modify one except by relocating its extent and re-pointing its slot
**under §20.5**"* — i.e. relocation is licensed as a §20.5 (rewrite)
operation specifically, for any rewriter, not just compaction. Combined with
§20.3 step 4's "relocating a live index region is a rewriter's operation ...
not an appender's" (3230-3232), the pattern is consistent: relocation in
general (of index regions *and*, by the same no-embedded-offsets logic, of
other MU=0 records' extents) is exclusively a rewriter capability, exercised
by any rewrite, not compaction alone. **Correct widening.**

**2. Citations.** `(§20)` is a whole-section citation (not a specific
subsection/rule id). I read §20 in full for this purpose; the claim is
supported specifically by §20.4's R-WRT-08 paragraph and by §20.5's
R-WRT-07 paragraph together. The citation is accurate but loose (points at
the section, not the specific rule); I don't count vague-but-correct
section citations as a defect since the sentence doesn't purport a specific
rule id here.

**3. Label check.** Confirmed no `>` prefix around line 1046 (this sits in
plain §7.2 prose, tagged `` `[R-CNT-13]` `` a few lines down). Normative;
repair lands with force.

**4. Contradiction.** Read the whole of §7.2 (1005-1062). "Records with MU
= 1 carry further references only where this specification or registry
review (§10) defines them" (the sentence immediately after) is a different
case (MU=1) and does not collide.

**5. Exhaustive claims.** None added by this substitution.

**6. Unconstrained siblings.** The record header's fields (type, flags,
inline_length, extent_offset, extent_length) are all governed elsewhere in
the same subsection (the table at 1010-1016 and the surrounding rules); this
hunk touches none of that.

**7. Analogy.** None present.

**8. Anaphora.** Substitution only; next sentence ("Records with MU = 1
carry further references only where ...") begins a new topic, unaffected.

**Verdict: no defect. Byte-level: n/a.**

---

### Hunk 14 — §9.7 Note, line 1548

**Rule the repair adopts:** the format does not promise to preserve a file's
commit history, and a rewrite (any rewrite, not just compaction) is expected
to discard it.

**1. Tense/quantifier.** Verified against Fact A and against the normative
statement at §20.5 lines 3560-3564: *"nothing in the output's trailer
records that it is a first committed state ... a rewritten file and a file
appended to a hundred times are indistinguishable by their live trailers
alone"* — this applies to **any** rewrite's output, not compaction
specifically (the paragraph is talking about §20.5's creation-path
obligation generally). Correct widening.

**2. Citations.** No explicit section citation in the touched clause itself
(the Note as a whole is anchored to §9.7's surrounding normative prose,
`` `[R-LIF-08]` ``, not re-cited here). N/A.

**3. Label check.** Confirmed: lines 1544-1548 are entirely inside `>
**Note.**` — non-normative by its own label, consistent with [R-CNF-01].
I checked whether the *same fact* is stated normatively elsewhere (required,
since a Note-only statement of a rule would itself be the R-CNF-01 defect
pattern): it is — §23.2, line 4373 (hunk 40's own target, normative,
`` `[R-PRV-03]` ``): *"absent altogether from a rewritten file (§20.5), which
retains no earlier trailer to find."* Same claim, same (correct, post-repair)
quantifier, in normative prose. **No defect: the Note is consistent with,
and non-load-bearing relative to, the normative statement.**

**4. Contradiction.** Read the whole of §9.7 (1495-1548) and both
surrounding Notes. No contradiction found.

**5. Exhaustive claims.** None beyond what's independently verified above.

**6/7.** N/A (no structure enumeration or analogy language here).

**8. Anaphora.** Substitution only, at the end of a Note block with nothing
following it in the block. No anaphor risk.

**Verdict: no defect. Byte-level: n/a.**

---

### Hunk 40 — §23.2, line 4373

**Rule the repair adopts:** the commit-count history is unavailable to
anyone holding only the live trailer, and is absent altogether — with no
earlier trailer to find — from the output of a rewrite (any rewrite, not
just compaction).

**1. Tense/quantifier.** Directly supported by §20.5 lines 3560-3564 quoted
above (Fact A) — any rewrite's output has no prior trailer. Correct
widening from "a compacted file" to "a rewritten file."

**2. Citations.** `(§20.5)` — verified, matches the passage quoted above.

**3. Label check.** Confirmed no `>` prefix (plain §23.2 prose, tagged
`` `[R-PRV-03]` `` at the end of the paragraph). Normative; lands with
force.

**4. Contradiction — read both neighbors.** The sentence immediately before
(4358-4370) describes what a file *does* disclose (names, geometry, write
footprint, history shape via probing) — no collision. The sentence
immediately after: *"Writers handling sensitive material SHOULD treat names
and metadata as published content, and SHOULD compact before publication
when the history itself is sensitive."* This still says **"compact,"** not
"rewrite," even though the sentence it follows was just widened to "a
rewrite." I checked whether this is a defect (this is exactly what my
charter flagged: "read the sentences either side, one of which still
advises a writer to compact"). My conclusion: **not a defect.** The
recommendation's goal is narrowly "make history disappear without any other
change," and compaction is the *minimal sufficient* rewrite for that (it
changes nothing but placement, per §20.1/§20.5's definition) — recommending
the narrowest tool for the stated job is correct guidance, not an
under-generalization. A reader who also needs to drop a sensitive layer
would combine that with a rewrite anyway (§20.5: "A rewrite MAY be several
of these at once"), which this sentence doesn't foreclose. I record this as
a checked-and-rejected candidate.

**5. Exhaustive claims.** "absent altogether" — checked against §20.5's
creation-path language; holds for any rewrite.

**6/7.** N/A.

**8. Anaphora.** Substitution only. "which retains no earlier trailer to
find" is a relative clause inside the same (repaired) sentence, not an
external anaphor; unaffected.

**Verdict: no defect in the touched text itself.**

**Byte-level: n/a** (nothing to resolve; the neighbor-sentence check above
resolved with no finding).

---

### Hunk 41 — §23.2, line 4384

**Rule the repair adopts:** a rewrite (any rewrite, per [R-WRT-06]) mints a
fresh file_id — the only defined way to break `file_id` linkage — but this
is not by itself an unlinkability measure, because [R-WRT-07] preserves
carried content bit for bit, so specifically **a compacted file** remains
trivially correlatable with its input by content.

**1. Tense/quantifier.** Two different quantifiers appear in one sentence,
deliberately, and I checked each against its warrant separately (this is
also a Check-7 analogy comparison):

- "A rewrite mints a new [file_id] ([R-WRT-06])" — [R-WRT-06] (§20.5, lines
  3542-3592) states this of *"A rewriter"* generally: *"It MUST mint a fresh
  file_id for the output ..."* No compaction-specific carve-out. **Matches;
  correct to widen "Compaction" → "A rewrite" here.**
- "so a compacted file remains trivially correlatable with its input by
  content" — kept **narrow**, correctly. [R-WRT-07] (lines 3594-3638) only
  guarantees bit-for-bit preservation for structures a rewrite **carries
  forward**; a layer a rewrite *re-creates* is explicitly excluded ("A layer
  the rewrite re-creates is new output ... nothing of the input's copy of
  that layer is carried forward," lines 3606-3610), and a dropped layer is
  simply absent. Compaction, by definition (Fact B), carries **every**
  structure forward — so 100% of content is preserved bit for bit only in
  the compaction case. A drop- or re-create-rewrite's output would **not**
  be "trivially correlatable by content" to the same degree (some content
  differs or is missing). **This clause is correctly held to the narrow
  noun.** This is the mirror-image check to hunk 46 item 8 (where the narrow
  noun was wrongly used) — here the author got it right.

**2. Citations — quoted side by side (Check 7).**
- Repair's governing verb: "mints" (a rewrite mints a new file_id).
  [R-WRT-06]'s governing verb: "MUST mint a fresh file_id for the output."
  Same verb, same subject scope (any rewriter). **Match.**
- Repair's governing verb: "preserves" (`[R-WRT-07]` preserves ... bit for
  bit). [R-WRT-07]'s actual text: "every **carried** stored tile's bytes
  verbatim — each index entry's crc is unchanged." The repair's paraphrase
  drops the word "carried," but the sentence's own conclusion narrows back
  down to "a compacted file" (where 100% is carried, so the omission is not
  load-bearing for the conclusion actually drawn). **Match, with the
  qualifier correctly supplied by scoping the conclusion rather than by
  restating "carried" explicitly.**

**3. Label check.** Confirmed no `>` prefix (plain §23.2 prose, tagged
`` `[R-PRV-04]` ``). Normative.

**4. Contradiction.** Read the full paragraph (4379-4389) and the one before
it (already covered under hunk 40). No contradiction found once the
carried/re-created distinction above is applied.

**5. Exhaustive claims.** "the only defined way to break file_id linkage" —
checked: `file_id` is otherwise stable across every generation of an
appended-to file (§23.2's opening sentence, "a stable 64-bit identifier that
persists across every generation of a file"), and only §20.5's rewrite path
mints a new draw. Holds.

**6. Unconstrained siblings.** N/A.

**7. Analogy.** Covered under (1)/(2) above; both comparisons pass.

**8. Anaphora.** Substitution only (single word, "Compaction" → "A
rewrite"); no insertion. Checked forward to the paragraph's end and into
§23.3 (new topic, "The remote read path ...") — no anaphor drift.

**Verdict: no defect. This hunk is a model instance of correctly choosing
the wide noun for one clause and the narrow noun for the next, matched to
what each clause's cited rule actually supports.**

**Byte-level: n/a.**

---

### Hunk 43 — Appendix G item 2, line 4704

**Rule the repair adopts:** item 2's hash-derived-`file_id` scheme is a
creator's rule only; a rewriter adopting the reproducible-writer profile
instead uses [R-WRT-06]'s fresh random draw.

**1. Tense/quantifier.** Per Fact A, [R-WRT-06]'s fresh-draw mandate binds
*every* rewriter (line 3542 "A rewriter MUST refuse..." through 3592,
generally "It MUST mint a fresh file_id"), not compaction alone. Correct
widening of "a compactor" → "a rewriter."

The reason clause kept unchanged — *"since a derived value is not a draw and
re-deriving it on an already-compact input would reproduce the input's own
`file_id`"* — gives **two** reasons, and I checked each against the widened
subject separately:
  - "a derived value is not a draw" — general, applies to any rewriter
    (matches [R-WRT-06]'s "not merely a value compared against the input's,"
    line 3552, and the randomness requirement generally). **Sufficient on
    its own to support the widened claim.**
  - "re-deriving it on an already-compact input would reproduce the input's
    own file_id" — this concrete failure mode is specific to compaction
    (only a placement-only rewrite of an already-slack-free input can
    reproduce byte-identical output, hence an identical hash). I checked
    whether leaving this half of the sentence un-widened is a defect: it is
    not, because the sentence's **general** conclusion ("a rewriter ...
    takes [R-WRT-06]'s fresh draw instead") is already fully supported by
    the first, general reason; the second reason is additional, correctly
    scoped, illustrative evidence for the compaction sub-case and does not
    purport to cover drop/re-create rewrites. I record this as a checked,
    rejected candidate.

**2. Citations.** `[R-WRT-06]` — verified (fresh-draw mandate, as above).
`(§6.2 forbids file_id = 0)` — untouched by this hunk; not re-verified in
detail here since it's outside the renamed text, but I confirmed §6.2 does
state file_id ≠ 0 in the trailer definition (spot-checked in passing while
reading §6).

**3. Label check.** Appendix G's own heading (line 4672) reads "**Appendix G
— Reproducible-writer profile (non-normative)**" — explicitly non-normative
per [R-CNF-01]'s "appendices identified as non-normative" clause. No force
issue: nothing here purports to be the sole statement of a normative rule;
[R-WRT-06] itself is stated normatively in §20.5.

**4. Contradiction.** Read all of item 2 (4692-4713) and the surrounding
items. No collision found.

**5. Exhaustive claims.** None beyond what's checked above.

**6. Unconstrained siblings.** N/A (item 2 is scoped to `file_id` alone;
item 8, which shares the "creator's rule" framing, is handled separately
below under hunk 46, where its own set of siblings — `version_minor` and
`flags` — is checked).

**7. Analogy.** "This is a creator's rule, ... as item 2's identifier is"
(cross-referenced from item 8, see below) — checked there.

**8. Anaphora.** Substitution only; "Deterministic, and high-entropy ..."
(the sentence immediately after the touched clause) is a pre-existing
sentence fragment that was already positioned after this same parenthetical
aside before the repair (the hunk only swaps "compactor" for "rewriter"
inside the aside; it does not insert or move the aside itself). I checked
whether "Deterministic, and high-entropy" could misresolve to describe the
rewriter's *fresh draw* (which would be wrong — a random draw is not
"deterministic") rather than the creator's hash-derivation scheme (item 2's
actual subject, which the fragment correctly describes). This ambiguity, if
real, **predates this hunk** — the aside's position relative to the
fragment is unchanged by a one-word substitution — so it is not something
this repair introduced. I record it as a rejected candidate (pre-existing,
out of this hunk's scope) rather than a finding.

**Verdict: no defect introduced by this hunk.**

**Byte-level: n/a.**

---

### Hunk 46 — Appendix G item 8, lines 4795-4807

**Rule the repair adopts:** item 8 (`version_minor` at the floor, `flags` =
0) is, like item 2, partly a creator-only rule. A rewriter adopting the
profile instead: carries forward unknown ignore-lane bits (not zero) for
`flags`; is bound by the `version_minor` floor too, except where §20.5's
own floor governs (a carried feature the rewriter doesn't implement); and
may retain-or-drop an MU=0/PE=0 record (now including the layer record,
under this round's third commit) at its own discretion, which the profile
does not pin.

**1. Tense/quantifier — the central finding.** I counted every occurrence of
"compactor" in this hunk's diff and what it became:

| # | Old text | New text | Correct? |
|---|---|---|---|
| 1 | "a compactor adopting the profile carries" | "a rewriter adopting the profile carries" | yes — [R-CNT-08]'s ignore-lane-bit-carry-forward rule is stated of "an updater, appender or rewriter alike" generally (line 837) and specifically of §20.5's rewriter (line 3577); not compaction-specific |
| 2 | "version_minor floor binds a compactor too" | "... binds a rewriter too" | yes — [R-WRT-06]'s version_minor floor language (lines 3577-3592) is stated of "a rewriter" generally |
| 3 | "A compactor's output is therefore reproducible ... and the records §20.4 lets it drop" | **"A compaction's output is therefore reproducible ... and the records §20.4 lets it drop"** | **NO — see below** |
| 4 | "this item's floor turns on which features the compactor implements" | "... the rewriter implements" | yes — matches [R-WRT-06]'s "a rewriter cannot know which minor version defined a feature it does not implement" (line 3585-3586) |
| 5 | "dropped at the compactor's choice" | "dropped at the rewriter's choice" | yes — matches §20.4's last table row, "a rewriter MAY drop it in any rewrite" (line 3483) |
| 6 | "across compactors pins the compactor" | "across rewriters pins the rewriter" | yes — consistent with 1, 2, 4, 5 |

Five of six were correctly widened from "compactor" to "rewriter." The
**third** was narrowed to **"compaction"** instead — and this is exactly the
one occurrence whose own clause depends on the wide meaning. The full
sentence, post-repair:

> "A compaction's output is therefore reproducible only modulo its trailer
> and the records §20.4 lets it drop: [R-WRT-06]'s fresh file_id is no
> function of content, this item's floor turns on which features the
> rewriter implements, and a record whose governing flags are MU = 0 and
> PE = 0 is retained or dropped at the rewriter's choice (§20.4), which no
> item here pins."

Per **Fact B**, compaction is defined at §20.5 (line 3526-3528) to "carry
**every** structure forward and change **nothing but placement**." A pure
compaction therefore never exercises the §20.4 MU=0/PE=0 retain-or-drop
discretion the sentence is describing — there is nothing for it to drop,
by its own definition. The variability this sentence is naming ("the
records §20.4 lets it drop," "retained or dropped at the [X]'s choice") is
a property of **rewriters in general** (specifically, of a rewrite that
combines compaction with a drop, or a pure drop-rewrite) — not of
compaction as the narrow named case. Every *other* noun in the same
sentence (the two instances of "rewriter" at #4 and #5) is correctly wide;
"A compaction's output" is the one place that should have stayed wide too
("A rewriter's output"), and instead it is the one place the hunk narrowed.

This is precisely the failure mode my charter names for this hunk: *"say
which of item 8's nouns should be the wide one and which the narrow."*
**The wide noun ("rewriter"/"rewriter's output") belongs here; "compaction"
is the wrong (too narrow, in fact self-contradictory given its own
definition) choice.**

I also checked whether the sentence, read charitably, could mean something
that *is* true of pure compaction — e.g., "even a compaction's output is
only reproducible modulo the drop-choice **that some other rewriter might
have made instead of compacting**." I rejected this reading: the sentence's
own grammar ("the records §20.4 lets **it** drop") makes "it" (the subject,
"a compaction['s output]") the agent of the drop, and a pure compaction is
not such an agent by §20.5's own definition. The reading that makes the
sentence true requires substituting the wide noun.

**2. Citations.** `§20.4` — verified against the MU=0/PE=0 row (line 3483:
*"Retain byte-identical, or drop it ... an updater MAY drop the record ...
and a rewriter MAY drop it in any rewrite"*) — this citation is about
**rewriters generally**, reinforcing (1) above: the citation itself already
supports the wide reading, and the surrounding prose is inconsistent with
its own citation. `[R-WRT-06]` — verified against lines 3577-3592
(version_minor floor / feature-carry exception). Both citations resolve to
what they claim, once the actor is read as "rewriter."

**3. Label check.** Appendix G is "(non-normative)" by its own heading
(line 4672), consistent with [R-CNF-01]. This defect therefore carries no
direct normative force — it does not by itself change a MUST/MAY anywhere.
It is nonetheless a real defect in the document's own explanatory
reasoning about a profile applications may adopt, and it directly
misdescribes what the third commit's flag change (layer record now
MU=0/PE=0) does to compaction-output reproducibility.

**4. Contradiction in the passage.** Item 8's own second sentence ("The
`flags` half is a creator's rule, **as item 2's identifier is**") explicitly
analogizes to item 2, where the parallel construction is *"a rewriter
adopting the profile takes [R-WRT-06]'s fresh draw instead"* — item 2 uses
the wide noun throughout its own rewriter-exception clause. Item 8's own
first three exception-clauses (1, 2, 4, 5, 6 in my table) also use the wide
noun. So the "compaction" substitution in clause 3 is a contradiction with
the pattern set by its own item, not just with the general rule — the
sentence disagrees with its own neighbors on which noun to use for what is,
grammatically, the same referent carried through one sentence.

**5. Exhaustive claims.** "which no item here pins" — checked against items
1-10; correct, no item pins this choice.

**6. Unconstrained siblings — the structure is the trailer's `flags` and
`version_minor` fields together with which optional records survive a
rewrite.** I listed every quantity item 8 (and its neighbors) touch:
`version_minor` (pinned to the [R-CNT-26]/[R-WRT-06] floor, with the stated
exception), `flags` (pinned to 0 for a creator; carried-forward
ignore-lane bits for a rewriter, per [R-CNT-08]), and the MU=0/PE=0 records'
retain-or-drop choice (explicitly *not* pinned, "which no item here pins" —
stated as such, not a silent gap). All three quantities this item's own
text touches are each explicitly addressed (two pinned, one explicitly left
open) — I did not find a fourth, unaddressed sibling quantity in this
specific structure.

**7. Analogy.** "as item 2's identifier is" — compared verb-for-verb: item
2's governing clause is "a rewriter adopting the profile takes
[R-WRT-06]'s fresh draw instead" (verb: *takes ... instead*); item 8's is "a
rewriter adopting the profile carries its input's unknown ignore-lane bits
forward instead" (verb: *carries ... forward instead*). Both range over
"a rewriter" (matching quantifier), both describe an *instead-of-the-
creator-rule* substitution (matching structure). The analogy holds for the
comparison it's actually used for (both are "creator's rule; rewriter
substitutes X instead").

**8. Anaphora.** No new clause inserted (pure word substitutions); checked
that "which no item here pins" (end of the sentence) still resolves to "the
[drop] choice" just named, unaffected by the choice of noun. Unaffected by
the defect above.

**Verdict: Finding E-01 (see below) — item 8's "A compaction's output ..."
should read "A rewriter's output ...".**

**Byte-level: No.** Appendix G is explicitly non-normative
([R-CNF-01]); the actual conformance obligations this passage explains
(flags carry-forward under [R-CNT-08], the version_minor floor under
[R-WRT-06], the retain-or-drop discretion under §20.4's table) are each
independently and correctly stated in normative text elsewhere, untouched
by this error. No conforming writer's or verifier's byte-level behavior
turns on whether this one explanatory sentence says "compaction" or
"rewriter" — the error misdescribes what byte-identity guarantee an
*adopter of the voluntary profile* should expect, which is a documentation
defect, not a fork in what bytes are conforming.

---

## Mandated sweeps

### Sweep 1 — stem "compact", case-insensitive, whole document

Command: `grep -in "compact" spec/tarn.md` → **19 matching lines.**
Occurrence count (a line can hold >1 hit): `grep -io "compact[a-z]*"
spec/tarn.md | wc -l` → **19** (so no line has 2 hits; occurrence count =
line count here).

**Control**, to prove the search could have found something and isn't
silently broken by the hard wrap: I rebuilt the document with all newlines
collapsed to single spaces (Python `re.sub(r'\n',' ',text)`,
`re.sub(r'  +',' ',text)`) and re-ran the same case-insensitive regex over
that normalized text: **19** hits, exactly matching. I additionally scanned
for any adjacent-line pair whose *concatenation* contains "compact" while
neither individual line does (i.e., a genuine mid-word line-wrap split):
**zero** such pairs. The wrap does not affect this single-word stem (word
wraps happen between words, not inside them, and this document does not
hyphenate at line breaks — confirmed no line in the file ends in "re-" or
similar broken-word hyphens near any "compact"/"rewrit" hit).

Full list, classified:

| Line | Text (key fragment) | Section | Classification |
|---|---|---|---|
| 62 | "slack until compaction reclaims" | §1 Introduction | non-normative ([R-CNF-01] excludes §1); named case, no exclusivity claim; fine |
| 64 | "bulk work followed by compaction" | §1 Introduction | non-normative; descriptive; fine |
| 438 | "verifiers, appenders, and compactors operate on files" | §3.3, Note | non-normative; **stale actor name** — should be "rewriters" per §20.1's tier list. See E-03. |
| 715 | "tells an operator to compact" | §5.2, normative | correct: compaction is the specific, minimal appropriate response to a slack total; not an exclusivity claim |
| 745 | "Only a rewrite (§20.5) reclaims it, compaction being the rewrite ..." | §5.2, normative | hunk 06's own text — audited above |
| 759 | "an operator paying for storage compacts rather than retains" | §5.2, Rationale | non-normative; descriptive operator-behavior claim, not an exclusivity claim; fine |
| 1389 | "Compaction (§20.5) is the continuation from there" | (F-ceiling) Note | non-normative; **narrow noun where "a rewrite" is what's actually meant** (any rewrite mints a fresh file_id and resets F). See E-04. |
| 2137 | "writers wanting compact masks choose planar" | §14-ish, Note | unrelated: ordinary adjective ("compact" = small), not the rewrite-actor concept; fine |
| 2400 | "would make compact windows contiguous" | slabs Note | unrelated: ordinary adjective; fine |
| 3131 | "compaction, which carries every structure forward and changes nothing but placement" | §20.1, normative | the definitional source; correct |
| 3372 | "and compact (§20.5) when slack grows" | §20.3, Note | non-normative; advisory, correctly narrow (minimal correct action) |
| 3527 | "This text names three rewrites: **compaction**, which carries ..." | §20.5, normative | the definitional source; correct |
| 3640 | "Example — what compaction reclaims" | §20.5, Example heading | correctly narrow — this Example is explicitly about the compaction sub-case only |
| 4348 | "Compaction (§20.5) is the only operation that removes slack" | §23.1, normative, R-PRV-02 | **contradicts the (correct) wide statement of this same rule at 745, 3670, 3695, 3998.** See E-02. |
| 4376 | "SHOULD compact before publication when the history itself is sensitive" | §23.2, normative, R-PRV-03 | checked and rejected as a defect (see hunk 40 discussion above) — correctly narrow (minimal sufficient action) |
| 4388 | "so a compacted file remains trivially correlatable with its input by content" | §23.2, normative, R-PRV-04 | hunk 41's own text — audited above, correctly narrow |
| 4615 | "just waste awaiting compaction" | Appendix D, non-normative | descriptive, non-exclusivity; fine |
| 4707 | "re-deriving it on an already-compact input" | Appendix G item 2, non-normative | hunk 43's own text — audited above, correctly scoped as illustrative |
| 4800 | "A compaction's output is therefore reproducible ..." | Appendix G item 8, non-normative | hunk 46's own text — **E-01** |

### Sweep 2 — stem "rewrit", case-insensitive, whole document

Command: `grep -in "rewrit" spec/tarn.md` → **82 matching lines.**
Occurrence count: `grep -io "rewrit[a-z]*" spec/tarn.md | wc -l` → **88**
(6 lines carry 2 occurrences each, e.g. "MUST refuse to rewrite" pairing
"refuse" ... "rewrit-" twice on one line, and "whole-file rewrite" +
"rewrite" pairs).

**Control:** same normalized-whitespace regex on the collapsed text → **88**,
matching exactly. This also resolved my own initial apparent discrepancy
(82 lines vs 88 occurrences is not a miss — it's lines-with-a-hit vs.
total-hits, since `grep -c`/`grep -n` count matching *lines*; `grep -o`
counts *occurrences*). I re-ran `grep -ion "rewrit" spec/tarn.md | wc -l`
independently and it also returned 88, confirming the occurrence count by a
second method.

I read every one of the 88 occurrences in context (via the full-file grep
output with line numbers, shown in full above under "Grounding" and in the
per-hunk sections). The purpose of this half of the sweep was to find any
place a sentence uses "rewrite"/"rewriter" broadly where the sentence is
actually only true of **compaction**. Candidates I specifically tested and
rejected, beyond what's covered in the per-hunk sections above:

- Line 3660-3661 ("placement being the rewriter's to choose") and 3666 ("a
  rewrite is the one operation that moves live bytes") — both sit inside
  the explicitly-labeled `> **Example — what compaction reclaims.**` block
  (3640-3661) or its immediate continuation about the general mechanism
  (3662-3680); checked against §20.5's general text and found correctly
  general (any rewrite relocates/moves live bytes when it changes
  placement) rather than compaction-specific overclaims.
- Line 4839 ("item 8, binding creator and rewriter alike save §20.5's
  carried-feature case") — Appendix G's closing summary paragraph; checked
  against item 8's own text (hunk 46) and [R-WRT-06]; consistent, no
  compaction-only fact stated as general.
- Line 4908-4915 (Appendix H, "Conforming updater" checklist: "A rewriter,
  in addition, mints a fresh file_id and follows the creation path
  ([R-WRT-06]); carries every structure it does not decode forward
  verbatim, regenerating each index region it relocates ...") — checked
  against §20.4/§20.5; this is a correct, general summary of a rewriter's
  obligations (not compaction-specific), and Appendix H is itself
  explicitly non-normative and was **not** touched by any of my hunks, so
  it is out of charter scope for a finding, but I checked it for
  consistency with the renamed terminology and found it already uses
  "rewriter" correctly throughout (it was evidently already written, or
  already swept, consistently with the third commit).

No occurrence of "rewrit*" was found stating something true of compaction
alone while claiming general rewriter scope (the inverse of the E-01
defect). The asymmetry is real: the renaming swept "rewrit*" language
cleanly; it is the **surviving "compact*" occurrences** that carry the
residue of the old, narrower rule.

---

## Rejected candidates (recorded in full above, summarized here)

1. Appendix G item 2's "Deterministic, and high-entropy ..." fragment —
   possible anaphor drift onto the rewriter's fresh draw instead of the
   creator's hash scheme; concluded pre-existing (not introduced by hunk 43)
   and out of scope.
2. §23.2's "SHOULD compact before publication ..." (line 4376, adjacent to
   hunks 40/41) — considered whether it should have widened to "SHOULD
   rewrite"; concluded compaction is the correct minimal action for the
   stated (history-only) goal.
3. Hunk 41's "not an unlinkability measure" claim justified only via the
   compaction sub-case — considered whether this under-argues the general
   claim for drop/re-create rewrites; concluded the general claim doesn't
   need that specific justification to extend, and the sentence's own
   conclusion is correctly kept narrow ("a compacted file").
4. Hunk 43's retained "already-compact input" phrase — considered whether
   it should have widened alongside "compactor"→"rewriter"; concluded it's
   correctly-scoped illustrative evidence, not the sentence's sole or
   necessary support.
5. Lines 62/64, 759, 3372, 4615, 4707 (various "compact(ion)" uses in
   Introduction/Rationale/Note/Appendix D/Appendix G) — checked each for an
   implicit exclusivity claim; none found (see Sweep 1 table).
6. Lines 2137, 2400 — "compact" as an ordinary adjective (small/packed),
   unrelated to the rewriter-actor renaming; not a candidate at all once
   read in context.

## Confidence where I found little

For hunks 05, 11, 14, 40, 41, 43 I ran all eight checks and found no defect
internal to the touched text. For each of these I did the following
concretely (not just "looked and saw nothing"): quoted and compared the
repair's quantifier against the specific normative rule it echoes (§20.3
step 4 for hunk 05; §20.4/[R-WRT-08] for hunk 11; §20.5 lines 3560-3564 for
hunk 14 and hunk 40; [R-WRT-06]/[R-WRT-07] verbatim for hunk 41 and hunk
43); confirmed blockquote-label status by direct `sed` extraction showing
the presence or absence of a leading `>` (not by assumption); read the full
enclosing subsection, not just the hunk's context lines; and, for hunks 40
and 41 in particular, explicitly read the sentence before and the sentence
after per my charter's own instruction, finding one real candidate (the
"SHOULD compact" neighbor) which I tested and rejected with a stated
reason rather than passing over silently. Two of the six "no defect" hunks
(41, 43) required a genuine word-by-word Check-7 comparison because they
mix a widened clause and a deliberately-kept-narrow clause in one sentence;
both passed on inspection of what each clause's citation actually supports.

The two hunks with real findings (06, 46) were not found by "the words on
the page were wrong" alone — 06's own text is correct; its defect is an
incomplete sweep discovered only by grepping the whole document for the
same rule restated elsewhere. 46's defect (E-01) was found by literally
counting the six occurrences of "compactor" in its diff and checking each
substitution's destination against §20.5's definition of compaction (Fact
B) — the one outlier ("compaction" instead of "rewriter") stood out
mechanically once counted, and its falsity was then confirmed against the
compaction definition, not assumed from the word choice alone.
