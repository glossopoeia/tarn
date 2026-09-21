# Audit transcript — "the positions" (hunks 01, 02, 04, 10, 11, 16, 25)

## 0. Disclosure of unrequested context

Before this task's charter was presented, my runtime context already contained: the
project's CLAUDE.md pointer ("See AGENTS.md"), the contents of a user memory file
listing titles of prior-round memory notes (e.g. "TARN harness spec path", "TARN
repair prose vs rules", "TARN closed-list exceptions compose", "TARN permissions,
not carve-outs", "TARN ADR status change gates quotes", etc. — titles only, I did not
open any of the linked files), and a git-status block naming this repo's five most
recent commit subjects (round 36 charter/re-cut, ADR-0129 erratum E3, ADR-0130
erratum E2/E1). None of this is part of the specification or the hunks, and I did not
read AGENTS.md, docs/, PLAN.md, OPEN-QUESTIONS.md, README.md, conformance/,
spec/registry.json, or any git log/diff during this audit, and did not use the memory
titles or commit subjects to steer any conclusion below. Every finding below is
derived solely from spec/tarn.md (read directly) and the seven assigned hunk files.
Flagging this per the charter's instruction to disclose rather than silently act on
unrequested context.

**Paths**: both directories named in the charter existed exactly where stated; no
path discrepancy to report.

## 1. What I read

- All seven hunk files in full (`hunk-01.diff`, `hunk-02.diff`, `hunk-04.diff`,
  `hunk-10.diff`, `hunk-11.diff`, `hunk-16.diff`, `hunk-25.diff`), each header and
  body.
- spec/tarn.md: §2.3 (all five conformance-class definitions, lines 152–251) in full;
  §2.4 (296–341); §5.2 Byte coverage (698–781); §6.2 Trailer (828–877); §6.3 Version
  and flag gates (878–922); §6.4 opening; §9.6 Recovery scan (1460–1505); §20 opening
  through §20.5 and its closing R-WRT-09 paragraph and Notes (3126–3733); Appendix G
  item 1–2 (4707–4748); Appendix H's Conforming-file/-reader/-writer/-updater entries
  (4882–4951).
- I did not read §7.2, §7.4, §9.3, §23.1, or Appendix C in full — they are not where
  any of my seven hunks land and the charter's per-hunk instructions for this set
  point at §2.3/§20.1/§20.2/§20.5/§5.2/§6.2/§6.3/§9.6/Appendix G/Appendix H
  specifically, all of which I did read.

## 2. Scripts run

No script was needed beyond `grep`/`python3 -c` one-liners run directly in Bash
against `spec/tarn.md` (read-only) and the hunk files (read-only). Nothing was
written to disk except this transcript, at
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r36-audit2/scratch/the-positions/`
— in fact nothing else was needed, so that directory holds no other file.

## 3. Sweeps run, verbatim, with hit counts and controls

```
grep -n "decod" tarn.md | grep -iE "creator|rewriter|updater|appender"
```
→ 2 hits: line 3161 ("...is an appender and an updater, whatever it decodes: the file
it leaves holds every byte of its input." — hunk 11's own text, a *correct* use, not
a class-by-decode assignment) and line 3644 ("...content the rewriter decoded (§19.3,
§19.4), and nothing of the input's copy of that layer is carried forward." — describes
what a *re-created* layer is written from, not a class test). **Control**: the old
defective sentence this replaced ("one that decodes everything it writes is a
creator, whatever it read") is gone; confirmed by:
```
grep -n "decoded everything\|decodes everything\|decode every byte\|decoded every byte" tarn.md
```
→ 0 hits (clean zero, and the search terms are short/unwrappable so the zero is
trustworthy).

```
grep -noE ".{60}is (a creator|a rewriter|an appender|an updater).{60}" tarn.md
```
→ 0 hits. **Control for wrap-blindness**: this is a single-line-anchored grep, so I
do not trust a bare zero from it alone. Re-ran with whitespace normalization:
```python
norm = re.sub(r'\s+', ' ', text)
norm.count("whatever it decodes")            -> 1
norm.count("the choice is its own")          -> 1
norm.count("undertakes to preserve its input") -> 1
norm.count("undertakes nothing toward its input") -> 1
```
Each phrase is present exactly once, matching hunk 11's own inserted text and
nothing else — confirms the zero above is real (no stray class-by-decode sentence
survives elsewhere), not a wrap miss, because these control phrases (which *are*
present) were found by the same method.

```
grep -n "writes a new file\|new file from\|a new one from\|writes a new one" tarn.md
```
→ 3 hits: line 209 (hunk 02, §2.3), line 3141 (hunk 10 bullet, unmodified half), line
3162 (hunk 11). No stray fourth restatement elsewhere in the document.

```
grep -n "modifies an existing file\|Conforming updater\|conforming updater" tarn.md
```
→ 2 hits: line 208 (§2.3, hunk 02) and line 4923 (Appendix H, hunk 25's paragraph).
No third restatement of the updater-class definition exists to sweep.

```
grep -n "input file\b" tarn.md
```
→ 1 hit (hunk 04's own line). **Control for wrap**: normalized-whitespace search for
`input file` found 2 hits — hunk 04's line and hunk 11's "A writer that extends an
input file is an appender..." — confirming the term is shared coherently between the
two hunks and not orphaned.

```python
norm.count("table for every record")            -> 1   (hunk 11)
norm.count("for what it carries forward")        -> 2   (both in §20.1: the pre-existing
                                                           R-CNF-06 sentence, and hunk 11's
                                                           own accountability clause)
norm.count("every record type, not only")        -> 1   (§2.3, R-CNF-06, hunk 02's paragraph)
norm.count("preserving what it does not understand") -> 1  (hunk 10)
norm.count("govern every record type")           -> 1   (same R-CNF-06 sentence)
```
These four counts are the evidentiary core of findings B-01 and B-03 below; see
§4 for the quotations and reasoning.

NESTED_DASH sweep — counted em-dashes (`—`) in the **added** (`+`) lines of all
seven hunks only:
```
for f in hunk-01 ... hunk-25; do grep "^+" $f.diff | grep -o '—' | wc -l; done
```
→ 0, 0, 0, 0, 0, 0, 0. No em-dash appears in any inserted text in this batch, so
NESTED_DASH cannot fire here (a defect needs at least a dash pair to nest).

ANALOGY-language sweep (check 7) over the same added lines, for "exactly as", "the
same way", "as X is,", "following", "the model is", "transposed from", "for the same
reason", "likewise", "on the model": 0 hits in all seven hunks. Check 7 is therefore
reported as **not applicable** to this batch — none of these seven repairs argues by
citing another rule's quantifier as its warrant; they either restate a rule
(check 1 territory) or add scoping words.

## 4. Per-hunk analysis

### Hunk 01 — §2.3, R-CNF-02's flags-gloss citation (line 176)

**The rule it adopts**: this sentence lists the writer-conduct-only obligations whose
violation is *not* a file-conformance violation. The edit adds a second citation,
"§20.3 step 6", alongside the existing "§20.5", for where "a creator's flags = 0, and
an updater's copy-forward and set-no-other" is actually stated.

**Check 2, citations**: opened §20.3 step 4's numbered step 6 ("`[R-WRT-04]`... unknown
ignore-lane flag bits copied forward and no other set (`[R-CNT-08]`)... barrier.") —
this is exactly the appender half of "copy-forward and set-no-other". Opened §20.5's
flags paragraph ("`[R-WRT-06]`... The output trailer MUST copy the input's unknown
ignore-lane flag bits forward and set no other...") — the rewriter half. **Both
citations verified**; before the edit, only the rewriter half was cited and the
appender-specific instantiation (step 6) was uncited from this sentence, even though
the sentence's own parenthetical names "an updater" (both tiers) as the actor. This
is a citation-completeness fix, not a rule change.

**Checks 1/3/4/5/6/7/8**: no quantifier, label, contradiction, overclaim, sibling-gap,
analogy, or anaphora issue found. The sentence's other two citations (§6.2 pad,
§20.3 step 4's declaration bar) are untouched by this hunk. **Byte-level: no** — the
edit only adds a pointer to text that already existed and already governed; no MUST
changed.

### Hunk 02 — §2.3, Conforming updater clause (lines 208–209)

**The rule it adopts**: "conforming updater" now includes not only "a tool that
modifies an existing file" (an appender) but also "[a tool that] writes a new one
that preserves it (§20.1)" (a rewriter) — replacing what was previously silent on
rewriters at this definition (the class list's own later sentence, unchanged,
already said "Its tiers, the appender and the rewriter, are §20.1's", so the class
already covered rewriters in substance; this hunk makes the *opening* clause name
them too).

**Check 1, quantifier / check 4, contradiction**: the charter asks directly: does a
rewrite that drops a layer, or re-declares one, "preserve" the input it is writing
from? I read §20.4's table (line 3504–3508) and §20.5's opening (3554–3568) in full.
§20.4's PE = 0 row: "Retain byte-identical, **or drop it** — its extent becoming
slack... a rewriter MAY drop it in any rewrite." §20.5's opening names three rewrites
— compaction, **dropping**, and re-declaring — and (via hunk 16) explicitly allows "A
rewrite [to] do several of these at once, dropping one layer, re-declaring another
and carrying the rest forward." A rewrite that drops a whole layer removes that
layer's stored tiles, its tile-index region, and its sub-records from the output
entirely ("a dropped layer's sub-records and their extents go with it whatever their
PE bits", §20.4 line 3512). Read in the plainest sense, "preserves it [the input
file]" is a claim about keeping the input's content, and a drop is the one operation
that does not keep content — it discards a whole layer. So the literal reading of
"preserves it" **excludes** exactly the class of rewrite (drop-performing) that
§20.1/§20.4/§20.5 explicitly enfranchise as a legitimate rewriter operation, and that
the unmodified sentence two lines below ("Its tiers, the appender and the rewriter,
are §20.1's") unconditionally calls an updater regardless of what kind of rewrite it
performs.

The charitable reading — "preserves it" is shorthand for "takes the §20.1 rewriter
position", which is itself defined to *include* the licensed drop — is defensible
given the explicit "(§20.1)" pointer, and I think it is what was intended. But the
word chosen ("preserves") does not by itself carry that meaning, and a reader who
does not chase the citation is left with a class boundary that appears to exclude a
tool the rest of the section plainly wants inside it. This is a **NEW_AMBIGUITY**:
the clause and the "rewriter" position (hunk 10/11/16's construction) do not
obviously pick out the same set of tools, even though I believe they are meant to.

**Byte-level**: no. "Conforming updater" is a class label that gates which
*additional* obligations (§20.4's table) bind an actor; it is not itself a
file-conformance predicate, and every specific MUST that actually constrains output
bytes (§20.4's table, §20.5's rules, R-WRT-05/06/07/08/09) is untouched and
unambiguous regardless of how this one summary noun is read. I flag this as a
documentation-clarity defect, not a bytes-forking one.

**Checks 3/5/6/7/8**: §2.3 is normative text, not a Note/Example/Rationale block, so
check 3's label test is moot here (the repair *does* land in normative text; I note
this explicitly since the charter warns not to assume from the ">" marker — this
bullet-list entry carries no ">" at all and is squarely normative by its position in
§2.3, outside any blockquote). No new exhaustive-claim word was introduced ("preserves
it" is not itself a completeness word, though see B-02 above for the tools-picked-out
issue). No sibling gap noted beyond B-02. No analogy language. No anaphor: "it" in
"preserves it" refers, within the same clause, to "an existing file" stated moments
before — clean, unaffected by anything before or after.

### Hunk 04 — §6.3, R-CNT-08 (line 908)

**The rule it adopts**: "An updater MUST copy forward unknown ignore-lane bits of
**its input file**" (was: "of the file it modifies"), generalizing the object from
"the file it modifies" (true of an appender, false of a rewriter, whose output is a
*new* file — it does not modify the old one) to "its input file" (true of both).

**Check 1, quantifier/actor**: confirmed this is exactly the right fix. An appender's
"input file" = the file it opens and extends; a rewriter's "input file" = the source
it rewrites from and mints a fresh identity against. "modifies" only fits the
appender. Checked the sentence immediately above (unmodified): "A rewriter, though
its output is a new file, carries the input's unknown ignore-lane bits into its
output trailer rather than writing flags = 0, and sets no other (§20.5, `[R-WRT-06]`)."
— this already special-cased the rewriter; hunk 04's sentence now generalizes
correctly to "An updater" for both tiers without contradicting that lead-in.

**Check 2, citations**: checked §6.2's trailer field table, flags row (line 838):
"bits 16–31 (ignore lane) ... carried forward unchanged by an updater, appender or
rewriter alike" — matches, confirms both tiers are meant here. Checked `[R-WRT-06]`
(§20.5, already quoted above) — matches the rewriter half. Checked Appendix G item 2
(non-normative, lines 4727–4748): "This is a creator's rule: a rewriter adopting the
profile takes `[R-WRT-06]`'s fresh draw instead" — confirms file_id (not flags, a
different field) is handled by a distinct rule per position; no conflict with hunk
04's flags-only claim. A creator that reads/copies bytes from another file is *not*
an "updater" under §2.3/§20.1, so it is not bound by this sentence at all, and
separately must still write flags = 0 per §6.3's creator sentence — checked, no
tension.

**Checks 3–8**: no label issue (normative running text, no blockquote). No
contradiction found in the surrounding paragraph — the "no writer under this text
originates an ignore-lane bit... a bit is set only by a writer under the later minor
version... and carried forward by every updater under this text, appender and
rewriter alike" sentence right after (unmodified) reinforces exactly the same
"appender and rewriter alike" scope hunk 04 now states. No overclaim; "of its input
file" does not add an exhaustive-claim word. No sibling gap: the incompat lane (bits
0–15) is separately and adequately handled in the same paragraph's last sentence
(unmodified). No analogy language. No anaphor issue.

**Byte-level**: no — the corrected object noun points at text ("§20.5", "the
sentence above") that already fully and separately specified the rewriter's identical
obligation; this hunk consolidates wording, it does not create or remove a permission.

### Hunk 10 — §20.1, rewriter bullet (lines 3141–3146)

**The rule it adopts**: adds "preserving what it does not understand as §20.4
provides, and" before "carrying structures forward, re-creating some, or dropping
some" in the rewriter tier's one-line definition.

**Check 2/4 — this is the strongest finding in this batch.** The charter's own
instruction points straight at it: "Hold 'what it does not understand' to
`[R-CNF-06]`, which says §20.4 governs 'every record type, not only those it does not
understand'." I opened §2.3's updater paragraph (hunk 02's own paragraph, lines
210–213): "...and additionally MUST honor the preservation obligations of §20.4 —
which govern **every record type, not only those it does not understand**." That is
the actual, explicit, unambiguous scope of §20.4's preservation duty: it is *not*
limited to unimplemented/not-understood types.

Hunk 10's added clause says the opposite emphasis: "preserving **what it does not
understand** as §20.4 provides" — phrasing that names the not-understood subset as
the *object* of what §20.4 governs, precisely the narrower reading R-CNF-06 exists to
rule out. This is check 2's most expensive shape: a citation ("§20.4") that points at
a real, correctly-numbered section, attached to a sentence that states something the
section "almost" but does not actually say — §20.4 governs preservation for *every*
record type (subject to the PE bit), not specifically or only for types the rewriter
fails to understand.

It also collides with hunk 11, twenty lines below in the same subsection: hunk 11's
own new sentence says a rewriter "undertakes to preserve its input: **§20.4's table
for every record**" — a *broader* quantifier than hunk 10's "what it does not
understand." Two hunks in the same audited batch, landing four sentences apart in the
same subsection, both purporting to gloss §20.4's scope for a rewriter, and stating
different scopes (one narrow-by-understanding, one broad-by-record) neither of which
matches R-CNF-06's actual, correctly-stated formula ("every record type, not only
those it does not understand" — a *type*-level universal with an explicit
not-only-exception clause, which is neither hunk's phrasing).

Checked §20.4's own text again for the underlying truth: "for an implemented type
only the PE bit bites" (line 3502) — i.e., for a type the rewriter *does* understand
and implement, preservation is still governed (by PE), it is simply governed by a
different bit than the MU-row governs unimplemented types. So "preserving what it
does not understand" as a gloss for "what §20.4 provides" undercounts: §20.4 also
constrains what the rewriter *does* understand (via PE), and hunk 10's clause gives
no hint of that.

**Byte-level**: no. This is a bullet-point summary in §20.1's tier list; the actual
binding text (§20.4's table, R-WRT-05, R-CNT-22, and R-CNF-06's own unambiguous
"every record type" sentence) is untouched and unambiguous, and none of those citations were edited by this hunk. A rewriter that read only this bullet and concluded it
could freely modify a PE = 1 record it understands would still be caught by
R-WRT-05/§20.4's table directly; the actual MUST is not weakened anywhere it is
stated with force. I classify this as a genuine internal contradiction in normative
prose (§20.1 carries no Note/Example/Rationale label and is not a non-normative
appendix, so it is squarely normative text under R-CNF-01 — checked: no ">" quote
block anywhere near this bullet list), but not one that forks emittable bytes.

**Checks 1/3/5/6/7/8**: quantifier mismatch is the finding itself (see above). Label
check: normative, confirmed (plain bulleted list, §20.1, no blockquote). No new
exhaustive-claim word beyond the "what it does not understand" scoping already
discussed. No sibling-structure gap distinct from the above. No analogy language
(checked, 0 hits). Anaphor: none introduced — "it" in the added clause refers to "a
rewriter" (the bullet's own subject two words earlier), unaffected before/after.

### Hunk 11 — §20.1, the two-positions paragraph (lines 3160–3171)

This is the hunk the charter calls hardest, and I gave it the most time.

**The rule it adopts**: a writer that *extends* an input file is always an appender
and an updater "whatever it decodes" (correcting the old decode-based test). A writer
that instead writes a *new* file from an existing one "takes one of two positions,
and the choice is its own": **rewriter** (undertakes to preserve its input — §20.4's
table for every record, the ignore-lane bits, §20.5 whole — and in exchange answers
for what it carries forward only to R-WRT-09's reduced depth) or **creator**
(undertakes nothing toward its input, is bound by §20.2, writes flags = 0, and
answers in full for every byte of its output, copied bytes included).

**Check 6, run over the WRITERS list**:

- *A creator with no input* — unambiguously creator; the "two positions" clause does
  not even apply to it (it applies only to "a writer of a new file **from an existing
  one**"). Owes: §20.2, flags = 0, fresh file_id, full R-CNF-05 accountability.
  Unambiguous.
- *An appender* — unambiguously appender/updater "whatever it decodes" per the new
  first sentence. Owes: §20.3's procedure, R-WRT-03's touched-structures verification
  depth, R-WRT-04 (step 6 flags), §20.4 for what it carries forward. Unambiguous.
- *A compaction* — necessarily the rewriter position: §20.5's own definition
  ("carries every structure forward and changes nothing but placement") and hunk 16's
  added clause ("is compaction only where it does nothing but carry") both use
  *carrying*, which is the rewriter's defining verb, not the creator's (a creator
  "undertakes nothing toward its input" — it does not "carry" anything by
  definition). Unambiguous.
- **A rewrite that drops a layer** — this is where the paragraph's own words
  conflict. See the quantifier finding below. The position the text visibly wants to
  put it in (rewriter — §20.1's bullet list (hunk 10) and §20.5's opening both name
  "dropping" as a rewrite operation, and hunk 16 explicitly reaffirms "dropping one
  layer" as something "a rewrite MAY do") is not the position its own defining clause
  in this hunk literally describes ("undertakes to preserve its input: §20.4's table
  **for every record**" — a drop is not preserving that record).
- *A rewrite that re-creates every layer of an input holding no record it does not
  implement* — this is exactly the scenario the *old*, defective rule (told creator
  from rewriter "by whether the writer decoded every byte it wrote") would have
  misclassified as a creator. Under the *new* rule, "the choice is its own" — this
  writer may still choose the rewriter position (get a fresh file_id via §20.5, owe
  the ignore-lane-bit carry-forward, the MU = 1 refusal, etc.) even though it decoded
  everything. Checked and confirmed this is a genuine improvement over the prior
  (pre-audited) defect the charter describes; no residual problem found for this
  case specifically.
- *A tool that reads a file whole and writes a new one from decoded content* — same
  analysis as above; either position is available and the choice is not tied to
  decode behavior. Clean.
- *A tool that copies some structures undecoded into a new file and leaves out a
  PE = 1 record it does not implement* — checked §20.4's table: the PE = 1 row
  ("Retain byte-identical, extent content unmodified") carries **no drop option**,
  unlike the PE = 0 row. So this tool cannot validly take the rewriter position (it
  would violate §20.4's table outright, a genuine R-WRT-05/R-CNT-22 violation,
  independent of anything these seven hunks changed). It *can* validly be a creator
  — a creator "undertakes nothing toward its input, whatever it read" and owes
  nothing toward a record it chooses not to include. So a valid classification
  exists (creator), even though rewriter is foreclosed by an unrelated, unedited
  rule. Not a defect in this hunk.
- *A recovery tool writing a new file from an earlier commit state (§9.6)* — I read
  §9.6 in full: recovery as specified there is **truncation** of the existing file to
  an earlier commit boundary, not the writing of a *new* file. For a hypothetical
  tool that instead copies the recovered (earlier, non-live) bytes into a genuinely
  new file: §20.5's rewriter definition requires building "from the structures
  reachable from the input's **live** trailer — the live committed state" (line
  3554–3556). An earlier, superseded commit state is by definition not the live
  state, so such a tool cannot satisfy §20.5's own construction requirement and
  cannot validly occupy the rewriter position — only the creator position is
  actually open to it, "the choice is its own" notwithstanding. I considered this an
  overclaim candidate (the phrase reads as unconstrained free choice) but concluded
  the creator position remains fully coherent and available, so I am not filing this
  as a finding — noted here and in rejected_candidates for the record.

**Check 1, quantifier — the primary finding (B-01).** Quote the two clauses side by
side, both inside the same paragraph, separated by one clause:

> "...and the preservation obligations of §20.4 **for what it carries forward**
> (`[R-CNF-06]`)..." *(unmodified sentence, immediately above the hunk's insertion
> point)*

> "As a rewriter it undertakes to preserve its input: **§20.4's table for every
> record**, the unknown ignore-lane bits (`[R-CNT-08]`), and §20.5 whole; in return
> it answers for **what it carries forward** unmodified only to `[R-WRT-09]`'s
> depth..." *(hunk 11's own new text)*

The paragraph uses two different quantifiers for what should be the same underlying
scope, one sentence apart: "for what it carries forward" (an instance-level
quantifier, ranging only over the records actually retained — correctly excludes
dropped and re-created records) versus "for every record" (unqualified — reads,
absent a "type" qualifier, as ranging over every record instance of the input). The
"every record" phrasing is, verbatim, one word short of R-CNF-06's own correctly
scoped formula two sections earlier ("every record **type**, not only those it does
not understand") — dropping "type" changes the quantifier's domain from types to
instances.

**Check 4, contradiction**: §20.4's own table is explicit that preservation is *not*
unconditional over every record instance — the PE = 0 row: "Retain byte-identical,
**or drop it**... a rewriter MAY drop it in any rewrite." §20.5's opening names
dropping as one of three legitimate rewrite operations, and hunk 16 (audited
alongside this one) explicitly reaffirms "dropping one layer" as something "a
rewrite MAY do." So a rewrite that legitimately drops a PE = 0 layer, fully licensed
three separate places in this same section, does not satisfy a literal reading of
"undertakes to preserve its input: §20.4's table for every record" — the "for every
record" phrase overclaims completeness the table itself withholds for droppable
records.

**Byte-level determination**: I considered a genuine fork — if an implementer takes
"for every record" literally and concludes a drop disqualifies the rewriter position,
it would have to fall back to the creator position for that same output, which
requires writing flags = 0 instead of carrying the input's ignore-lane bits forward
(§6.3/R-CNT-08 vs. §20.2/§6.3's creator rule) — genuinely different trailer bytes
for the same logical operation. I traced this all the way through and conclude it is
**not byte-level**, for two independent reasons: (1) §2.3's own R-CNF-02 explicitly
carves ignore-lane-bit disposal out of file-conformance ("a writer obligation whose
violation this specification expressly declares not to be a file-conformance
violation... §6.3's flags rules against a set ignore-lane bit... are the cases this
text states") — both the flags = 0 file and the bit-carried-forward file are
conforming files under either reading, so the file-conformance byte set does not
move; and (2) the operative permission for the drop itself (§20.4's table, §20.5's
named operations, unedited and unambiguous) remains fully in force regardless of how
this one summary sentence is read, so a careful implementation reading the whole
section — not just this compressed gloss — resolves to the same emittable set either
way. I report this transparently rather than suppressing it, since the mechanism is
real even though I conclude against byte-level.

**Check 5, exhaustive claims** — every completeness word checked:
- "whatever it decodes" (appender) — verified true, no counterexample found; this is
  exactly the corrected rule.
- "the file it leaves holds every byte of its input" — checked against the open-step
  1 language ("F, never the physical end, anchors every step below") and
  `[R-LIF-01]`'s "freezes the committed prefix." Considered the recovery-truncation
  edge case (an appender resuming from re-verified recovery output may truncate torn
  bytes before appending) as a potential counterexample, but concluded "its input" in
  this sentence means the *established* commit state (post-recovery if needed), not
  raw pre-recovery physical bytes, which is consistent with how "F" is used
  throughout §20.3 step 1. Rejected as a finding; noted in rejected_candidates.
- "§20.4's table for every record" — filed as B-01, above.
- "the choice is its own" — checked against the recovery-tool-from-earlier-state
  case; rejected as a finding (creator position remains genuinely open).
- "it answers for every byte of its output" (creator) / "whatever it read" / "bytes
  it copied from another file included" — checked against `[R-CNF-05]` ("A writer
  MUST emit only conforming files") and Appendix G item 2 ("a rewriter adopting the
  profile takes `[R-WRT-06]`'s fresh draw instead" — confirms the creator/rewriter
  file_id split is real and consistent with this clause). No overclaim found.

**Check 2, citations** — resolved all four: `[R-CNT-08]` (ignore-lane bits, §6.3,
matches); §20.5 "whole" (read in full, matches: fresh file_id, flags carry-forward,
MU = 1 refusal, R-WRT-09 depth); `[R-WRT-09]` (§20.5's closing paragraph — "MUST
verify each link of the chain... before emitting", "reaches no decoded content" —
matches "only to R-WRT-09's depth" precisely, including the word "only": R-WRT-09's
depth is structural (checksums, index chains, records) but explicitly excludes
decoded-content verification, so "only" correctly marks that exclusion, not an
understatement of the rewriter's actual structural duty, which is in fact *broader*
than an appender's R-WRT-03 depth — see B-04 below for where that broader-than-R-WRT-03
fact gets lost); §20.2 (creation path, matches "§20.2 binds it"); `[R-CNF-05]`
(matches "answers for every byte of its output").

**Check 3, label**: normative running prose in §20.1, no blockquote nearby, no
Note/Example/Rationale label — squarely normative, confirmed by direct inspection of
the surrounding lines (3148–3172), no ">" character present.

**Check 8, anaphora**: traced every "it"/"its" in the new text (nine instances) — all
resolve unambiguously to their own sentence's stated subject ("a writer" /
"a rewriter" / "a creator", each named explicitly at the top of its own clause via
"As a rewriter" / "As a creator"), including "travelling with it" at the end of the
rewriter clause, which resolves the same way the unmodified sentence three lines
above it does ("a violation latent in a structure it carries forward unmodified
travels with it, seen or unseen" — same referent pattern, structure→it). No
re-resolution problem found; this hunk substantially replaces rather than inserts
between untouched sentences, so the classic "insertion re-routes a later pronoun"
shape does not apply here — the sentence immediately following (§20.2's "A creator
MUST follow...") restates its subject by name, not by pronoun, so nothing downstream
depends on how this paragraph's pronouns resolve.

### Hunk 16 — §20.5 opening (lines 3567–3569)

**The rule it adopts**: "A rewrite MAY do several of these at once, dropping one
layer, re-declaring another and carrying the rest forward, and is compaction only
where it does nothing but carry" (was: "A rewrite MAY be several of these at once.").

**Check 5, "only"**: verified against §20.5's own opening definition of compaction
("carries every structure forward and changes nothing but placement") and hunk 10's
matching bullet ("compaction... is the rewrite that reclaims slack") — "is compaction
only where it does nothing but carry" is the accurate converse: any rewrite that
drops, re-declares, or re-creates anything is, by the section's own definition, not
compaction. No counterexample found. Also checked against §5.2's purpose-framed
mention ("compaction being the rewrite an operator runs for that alone") — that
sentence describes *why* an operator runs a rewrite (to reclaim slack, and for that
purpose alone), a different axis from hunk 16's *structural* test (does it carry
only); the two do not conflict, they describe the same operation from different
angles (motive vs. mechanism).

**Check 4, contradiction**: none found. The example illustration ("dropping one
layer, re-declaring another") uses "layer" for both, which is accurate: re-declaring
is defined (§20.5, unmodified: "re-declaring a layer that stores a tile in the
input") as a layer-only operation (only layers carry the "fixed declarations" that
§20.3 step 4 defines), while dropping can also apply to non-layer PE = 0 records
(per §20.4's table) — the example's use of "layer" for both is not a claim that only
layers can be dropped; it is an illustration, not an exhaustive-set claim, and I do
not read "only" as attaching to "layer" anywhere in this sentence.

**Check 2, citations**: no bracketed requirement ID is added by this hunk; the
citation-bearing sentence that follows it (`[R-CNF-06]`, `[R-WRT-01]`) is unmodified
and was not re-verified here beyond confirming it still reads coherently after the
insertion (it does — "A rewriter satisfies every writer requirement for the bytes it
produces (`[R-CNF-06]`)" follows naturally from either the old or new lead sentence).

**Checks 3/6/7/8**: normative (§20.5, plain paragraph, not a blockquote). No
sibling gap found — the same paragraph's later sentences (verification depth,
refusal on detected violations, MU = 1 handling) are unaffected by and consistent
with the added enumeration. No analogy language. Anaphora: the new sentence's own
"it" ("where it does nothing but carry") resolves to "A rewrite" in the same
sentence; the following sentence's subject is restated by name ("A rewriter
satisfies..."), so nothing re-routes.

**Byte-level**: no — this hunk states a converse of an existing definition and adds
an enumeration; no MUST/MAY changes force or permission anywhere.

### Hunk 25 — Appendix H, Conforming-updater entry (line 4925)

**The rule it adopts**: scopes one clause of the non-normative "Conforming updater"
checklist — "changes a layer that stores a tile in the generation its commit
supersedes only as §20.3 step 4 permits" — to "as an appender," explicitly.

**Check 2, citations**: opened §20.3 step 4 in full (lines 3255–3390) and confirmed
the permitted-changes list this clause paraphrases ("its names, a grown dimension
extent, a planar channel list extended at its end or shortened from it (not both in
one commit), a slab or alignment declaration declared, changed or cleared") matches
step 4's text exactly. Confirmed the reason the scoping is *necessary*: step 4 itself
says a change beyond this list "is a new layer, or **a rewrite that re-declares it**
under a fresh file_id" — i.e., a rewrite's re-declaration is explicitly *not* bound
by the "only as step 4 permits" ceiling; re-declaring is precisely how a rewrite goes
*beyond* that ceiling. So before this hunk, an unscoped "Conforming updater... changes
a layer... only as §20.3 step 4 permits" incorrectly implied the same ceiling bound a
rewriter's re-declaration, when §20.3 step 4 and §20.5 both say the opposite. The fix
is correct and necessary.

**Check 6/UNSWEPT_RESTATEMENT — finding B-04.** Reading the whole entry as a
checklist for an appender and then for a rewriter, as the charter directs: the
clause immediately before the fixed one, unmodified by this hunk, has the identical
defect shape. Quoted in full: "**Conforming updater**... — everything a writer does
for the bytes it produces, plus: **validates the trailer and full directory, and
every layer it modifies (§20.3)**; as an appender, changes a layer..." The first
clause cites "(§20.3)" — the append-procedure section — exactly the same citation
whose ambiguity motivated adding "as an appender" to the very next clause. I checked
whether "every layer it modifies" is also true of a rewriter and found it is not:
R-WRT-03 (§20.3, cited here) scopes an *appender's* verification to layers "whose
record, index, or extents **the commit modifies**" — an appender validates only what
it touches. A rewriter's actual verification duty is R-WRT-09 (§20.5, not cited
here), which requires verifying "each retained layer's record... and full index
chain... before emitting that structure's bytes" for **every structure it carries**,
modified or not — confirmed by cross-checking against a pure compaction, which by
definition "changes nothing but placement" (modifies nothing) yet still must, per
R-WRT-09, "verify each link of the chain... the checksum §8.1 states over each
extent it copies, every stored tile's entry crc among them." So if clause 1 is read
(as its unscoped wording invites) to cover a rewriter too, it understates a
compacting rewriter's validation duty to zero, which is false. This is the same
defect shape hunk 25 fixed three words later in the same entry, left unswept.

**Byte-level**: no, on two independent grounds. First, Appendix H's own header reads
"Appendix H — Conformance checklists **(non-normative)**", and R-CNF-01 explicitly
exempts "appendices identified as non-normative" from normative force — checked this
against R-CNF-01's text directly (§2.2, line ~ near the top of the doc, quoted in the
charter and confirmed present) and against Appendix H's own disclaimer ("A summary of
each class's obligations... each entry's authority is the requirement or section
cited, never this summary.") Second, even setting non-normativity aside, the actual
authorities cited elsewhere (R-WRT-03 for the appender, R-WRT-09 for the rewriter)
are both unedited and unambiguous, so no conforming implementation's bytes are at
stake either way.

**Checks 1/3/5/7/8**: no quantifier issue in the edited clause itself (it now
correctly matches R-WRT-03/step 4's scope). Label: confirmed non-normative by
Appendix H's own header — this is check 3's cleanest possible case, an explicit
"(non-normative)" tag rather than an inferred one. No new exhaustive-claim word. No
analogy language. Checked whether inserting "as an appender," re-routes any pronoun
in clauses 3–7 (which all continue the entry's implicit list-subject, "Conforming
updater"): clause 3 contains an explicit "it" ("record it does not logically
modify"). Considered whether a reader might now resolve this "it" to the nearer
noun "an appender" rather than the entry's stated overall subject; concluded this
is weak — English parallel-list structure (semicolon-joined verb phrases sharing one
declared subject, stated once at the top: "Conforming updater... — everything...,
plus: [validates...]; [as an appender, changes...]; [re-emits...]...") does not
typically re-route on a single scoped item, and clauses 3–7's content is independently
confirmed general-updater scope by their own citations (R-WRT-05, R-CNT-08, R-CNT-22,
all cited as "updater" rules, not appender rules, in the normative sections
themselves). Not filed as a finding; noted in rejected_candidates as a considered,
low-confidence candidate.

## 5. Cross-hunk observations

- Hunks 10 and 11 both land in §20.1 and both gloss §20.4's scope for a rewriter with
  different, non-matching quantifiers ("what it does not understand" vs. "every
  record"), and neither matches R-CNF-06's own correct formula two sections earlier
  ("every record type, not only those it does not understand"). Reported as B-03 and
  B-01 respectively, cross-referenced.
- Hunks 02, 10, 11, and 16 together are clearly one coordinated repair (the "two
  positions" model), and the sweep in §3 confirms the old defective decode-based
  classification rule is fully gone with no orphaned restatement — that part of the
  repair succeeded cleanly. The residual defects are all in how precisely the new
  model's boundary conditions (what "preserve" covers, what "§20.4... for every
  record" covers) are phrased, not in whether the model itself is present and
  internally reachable.
- Hunk 25 is the one hunk in a non-normative appendix; every finding under it is
  therefore reported byte_level: false by construction (R-CNF-01), which the charter
  anticipates ("Read the whole entry as a checklist... quote any clause one of them
  cannot perform").

## 6. Summary of checks that passed cleanly, per hunk

- Hunk 01: checks 1, 3, 4, 5, 6, 7, 8 — no findings. Check 2 — both citations verified
  correct.
- Hunk 02: checks 3, 5, 6, 7, 8 — no findings. Check 2 — citation (§20.1) resolves to
  real, relevant content. Checks 1/4 — see B-02.
- Hunk 04: checks 1, 3, 4, 5, 6, 7, 8 — no findings; this hunk is a clean, correctly
  scoped fix. Check 2 — all four citations (§6.2, R-WRT-06, Appendix G item 2, the
  preceding sentence) verified consistent.
- Hunk 10: checks 3, 5, 6, 7, 8 — no additional findings beyond B-03. Check 2/4/1 —
  see B-03.
- Hunk 11: checks 3, 5 (mostly), 7, 8 — no findings beyond what's noted; check 6 —
  worked the full WRITERS list, one finding (B-01, restated) plus several
  rejected/confirmed-clean cases documented above; check 2 — all citations verified.
  Check 1/4 — see B-01.
- Hunk 16: checks 1, 2, 3, 5, 6, 7, 8 — no findings; clean.
- Hunk 25: checks 1, 3, 5, 7 — no findings beyond B-04. Check 2 — citation verified
  and the scoping fix confirmed correct and necessary. Check 6/UNSWEPT — B-04.

## 7. Findings filed

- **B-01** (hunk 11, §20.1): "§20.4's table for every record" — quantifier mismatch
  against the same paragraph's "for what it carries forward" and against §20.4's own
  drop license; non-byte-level.
- **B-02** (hunk 02, §2.3): "preserves it (§20.1)" does not obviously cover a
  drop/re-declare rewrite, creating ambiguity about which tools the "conforming
  updater" clause and the §20.1 rewriter position both pick out; non-byte-level.
- **B-03** (hunk 10, §20.1): "preserving what it does not understand as §20.4
  provides" contradicts R-CNF-06's explicit "every record type, not only those it
  does not understand", and contradicts hunk 11's own broader quantifier four
  sentences later; non-byte-level.
- **B-04** (hunk 25, Appendix H): clause 1 ("validates the trailer and full
  directory, and every layer it modifies (§20.3)") left unscoped, the same defect
  shape hunk 25 fixed in the very next clause, understating a rewriter's actual
  (broader, R-WRT-09) validation duty; non-byte-level (non-normative appendix).
