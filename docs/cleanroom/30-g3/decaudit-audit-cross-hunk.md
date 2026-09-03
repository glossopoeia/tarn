# Cross-hunk consistency audit — round 29

## Access

Read: spec/tarn.md (full, via targeted `sed`/`grep`), and hunk-01.diff through
hunk-06.diff in case/. Did not read full.diff, other hunk files claimed by
other auditors, or any docs/ADR/PLAN/registry material. No contamination from
pre-loaded context was used as evidence (the CLAUDE.md/MEMORY.md material
shown to me at session start names file paths only; I did not act on any of
its content as a conclusion about the spec — it is disclosed here per the
access rule, but nothing in my findings below rests on it).

Working files written under scratch/cross-hunk/: `register_23_25.txt` (a
sed extract of tarn.md lines 3640-3821, i.e. §21.2-§21.5, used only as scratch
input to the Python recomputation below — no other file consumed it).

## The six hunks, one-line rule each states

1. hunk-01 (line 12, before §1): relabels the "How to read this document"
   blockquote from `**How to read this document** *(non-normative).*` to
   `**Note.** How to read this document.` — a normativity-label fix under
   [R-CNF-01].
2. hunk-02 (§9.2, after the commit-protocol paragraph): declares that steps
   4 and 6 of [R-LIF-02] (the two durability barriers) bind writer *conduct*
   on the [R-CNF-02] model, so omitting one does not make the file
   nonconforming.
3. hunk-03 (§21.5, row R8): splits R8's Instances cell from 2 to 4 by
   distinguishing "overflowing magnitude" from "bare token" as two shapes,
   each over both containers.
4. hunk-04 (§21.7): changes "The register carries a row for a condition
   *exactly where* it is a detectable violation" to "...for *every condition
   that is* a detectable violation", and separately changes "no obliged check
   separates from *a conforming one*" to "...from *one that does not exhibit
   the condition*".
5. hunk-05 (§21.8): changes "120 conditions over 275 instances" to "...277
   instances".
6. hunk-06 (Appendix G, item 5): adds "Fixed declared tile extents and a
   fixed layout likewise, and item 2 names both: §11.3 states... and §14.1
   ...", extending the reproducible-writer profile.

## Grouping by rule, not by section

- **Group A — normativity labeling** (hunk-01 alone): tests [R-CNF-01]'s
  three-way exemption (§1 / labeled block / non-normative appendix) against
  a specific passage.
- **Group B — conduct-vs-bytes conformance model** (hunk-02, and
  contextually hunk-04's second clause and hunk-06's appendix, all resting on
  "conformance is a predicate on bytes"): whether an obligation's violation
  can leave the file's bytes untouched.
- **Group C — register completeness/detectability machinery** (hunk-04
  alone, tested against §21.1's completeness clause and §21.7's own earlier
  paragraph): the logical chain from "detectable" to "has a row" to
  "unwitnessed conditions are absent."
- **Group D — register instance arithmetic** (hunk-03 + hunk-05): a
  definition (R8's shape count) and the sentence reporting the register's
  total, edited in the same commit, must still agree.
- **Group E — reproducibility profile** (hunk-06 alone): a citation inside
  a non-normative appendix.

## Checks run

### Group A — hunk-01

Rule adopted: the "How to read this document" block is exempt from
[R-CNF-01]'s normative-by-default rule via the *labeled-block* branch, not
the *§1* branch (this block sits at lines 9-19, **before** "## Part 0 —
Preliminaries" (line 20) and before "### 1. Introduction" (line 24), so the
§1 exemption cannot reach it) and not the *non-normative-appendix* branch
(it isn't in an appendix at all).

Check 3 (label, not marker): searched for any other body-text use of the
`*(non-normative)*` parenthetical pattern:

```
grep -n "non-normative" spec/tarn.md
```
→ only hits are `[R-CNF-01]`'s own defining sentence (line 106) and seven
appendix *headings* ("Appendix X — ... (non-normative)"), lines 4314-4641.
So `(non-normative)` in body prose (pre-repair) was not a recognized label
under [R-CNF-01] at all — the old text was arguably unintentionally
normative. The new `**Note.**` lead matches the document's actual
convention:
```
grep -n "^> \*\*Note\.\*\*\|^> \*\*Rationale\.\*\*\|^> \*\*Example" spec/tarn.md
```
→ 9 hits, all `> **Note.**`/`> **Rationale.**`/`> **Example.**`, same form
hunk-01 now uses. Verdict: **repair correctly lands force removal where it
belongs; no defect.**

Check 4 (contradiction / dependency): the block's only substantive claim —
fields are **structural** or **descriptive** — is independently and
normatively restated at §4.7 (unlabeled, plain prose):
```
sed -n '584,598p' → "A field is **structural** if its value determines
anything a reader... **descriptive** if it determines none of those...
version_minor is the only descriptive field, and every other field this
specification defines is structural."
```
So nothing normative depends solely on the now-Note block; §4.7 is the
actual source and is untouched. **No defect** — checked and rejected as a
candidate.

### Group B — hunk-02 vs. the conduct-rule model elsewhere

Rule adopted: "[R-LIF-02] steps 4 and 6 (the two commit barriers) are a
conduct obligation; a writer that omits one violates [R-LIF-02] but the
*file* is not nonconforming on that account, because omission can be
byte-identical to compliance."

Check 2 (citations): `[R-CNF-02]` — read its defining bullet, §2.3:
> "A few obligations this specification places on writers govern their
> *conduct* rather than their output... a file is never nonconforming by
> virtue of one: conduct rules bind the actor, the predicate binds the
> bytes... §6.3's flags = 0 against a set ignore-lane bit and §6.2's
> pre-trailer gap... are the cases this text states, **and each is declared
> where it arises rather than enumerated here**."
The trailing clause explicitly licenses new conduct-rule declarations at
their own site — exactly what hunk-02 does. Citation **verified, passes**.

Check 7 (analogy): hunk-02's governing verb "bind... conduct rather than
its output" is the *same* verb pair R-CNF-02 itself uses ("govern their
conduct rather than their output"). Not a paraphrase-drift; near-identical
language, correctly scoped. **Passes.**

Check 4 (contradiction): does anything nearby assert barrier omission IS
witnessed/detectable, which would contradict "byte-identical... not
nonconforming"? Searched all "barrier" hits:
```
grep -n "barrier|durable|fdatasync" spec/tarn.md
```
→ line 1283's existing (untouched) Note: "Where barriers are weaker than
assumed, safety degrades from 'torn commits are invisible' to 'torn
commits are detected': §8's chain still catches every inconsistent state
loudly." This is compatible, not contradictory: hunk-02 covers the
no-crash case (bytes end up identical, hence conduct-only); the pre-existing
Note covers the case where a crash *does* land mid-write (the resulting
torn file *is* structurally inconsistent and §8 rejects it). Two different
factual scenarios, no collision. Verified against line 848's forward
reference "detection is never silent, per §9.2's barrier note" — that
antecedent is the line-1283 Note, unaffected by hunk-02's insertion, which
sits earlier in §9.2, before all three existing Notes. **No back-reference
drift** (Check 8): traced "the Note above" at line ~1289 (Step-5 Note) —
resolves to the Step-3 Note immediately preceding it, both of which sit
*after* hunk-02's insertion point, so hunk-02 cannot have altered that
resolution.

Byte-level: **no.** File conformance is already defined as "a pure
predicate on bytes" (§2.3); a storage barrier has no on-disk representation
absent an actual crash, so this text states a consequence already implicit
in the existing model rather than creating a new one.

### Group C — hunk-04, the quantifier defect

Rule the *unedited* first half of the paragraph establishes (lines
3894-3899, untouched by this hunk):
> "unwitnessed" and "detectable" are **duals** — each is exactly the
> negation of the other over the same subject (a condition this
> specification names).

§21.1's completeness clause (quoted in full, also untouched):
> "a *detectable* file-conformance violation this specification names and
> the register omits is a defect in this document" — i.e. **detectable(C)
> ⟹ ought-have-row(C)**. One direction only.

Pre-repair sentence (removed by this hunk): "The register carries a row for
a condition **exactly where** it is a detectable file-conformance
violation" — "exactly where" states the **biconditional**: row(C) ⟺
detectable(C). That entails both directions, including the one the very
next clause needs: ¬detectable(C) ⟹ ¬row(C) (i.e. row(C) ⟹ detectable(C)).

Post-repair sentence: "The register carries a row for **every condition
that is** a detectable file-conformance violation" — states only
detectable(C) ⟹ row(C). It does **not** state row(C) ⟹ detectable(C).

The sentence's own conclusion, unchanged by the hunk: "**so** an unwitnessed
condition is absent from it by that clause's own terms rather than in
breach of them." "Absent" is the factual claim ¬row(C) for ¬detectable(C),
i.e. exactly the direction the new premise dropped. Read most charitably,
"by that clause's own terms" says only that such an absence would not
*breach* §21.1's completeness clause (which only obliges the other
direction) — but the sentence's own opening still asserts, as a fact about
the register's construction, that a row exists "for every condition that
is detectable," and a fact stated only in that direction cannot by itself
support "so an unwitnessed condition is absent." The repair swapped a
premise strong enough to carry its own conclusion for one that isn't.

This is checkable independent of any tacit "a row implies a Detector
implies a check implies detectability" argument (which the document
never actually states in so many words) — the sentence used to be
self-contained and is no longer.

Check 5 (exhaustive claim): "every condition that is a detectable
violation" is itself a completeness-style universal claim (matches
[R-CNF-07]'s and §21.1's genuinely-universal completeness requirement — not
falsified on its own), so the defect is not that this half-clause overclaims;
it's that the *conclusion drawn from it* no longer follows.

Second edit in the same hunk (Check 2/4): "no obliged check separates from
**a conforming one**" → "...from **one that does not exhibit the
condition**." Compared word-for-word against the actual "unwitnessed"
definition two paragraphs up: "some file **that does not exhibit it**
cannot be told apart..." — exact match. This half of the hunk is a correct,
verified fix (the old "a conforming one" was too narrow: the alternate file
need not be fully conforming in every other respect, only not exhibit this
one condition). **This edit is sound.**

Byte-level: **no.** The operative test — the final, untouched paragraph of
§21.7 ("ask whether a breach can be made to leave behind a file no obliged
check separates from one that does not exhibit the condition") — is
unaffected, and §21.1's completeness clause is unaffected. The defective
sentence is explanatory scaffolding connecting the two; fixing it changes
no accept/reject verdict on any byte sequence. It is a soundness gap in
normative prose (this text is in-register connective tissue and carries
[R-CNF-01] force — no blockquote, no §1, no non-normative-appendix
exemption applies to §21.7), not a change in what any implementation must
do.

### Group D — hunk-03 + hunk-05, verified by independent recomputation

hunk-03's new R8 splits 2 instances into 4 ("overflowing magnitude" ×
{top-level, layer sub-record}; "bare token" × {top-level, layer
sub-record}). hunk-05 raises the reported total from 275 to 277 — exactly
+2, matching R8's net change if nothing else moved.

I did not trust the arithmetic on the diff's say-so. I extracted the whole
register (§21.2 through §21.5, i.e. every row up to but excluding §21.6)
from the **current, post-repair** file and recomputed independently:

```python
# scratch/cross-hunk/ — recompute, not the diff's claim
lines = open('spec/tarn.md').read().split('\n')
start, end = 3640, 3822   # §21.2 heading .. just before §21.6 heading
total = 0; rowcount = 0
for i in range(start-1, end-1):
    line = lines[i]
    if line.startswith('| ') and re.match(r'^\|\s*[A-Z]?\d+\s*\|', line):
        cells = line.split('|')
        instances_cell = cells[3].strip()
        n = 1 if instances_cell == '—' else instances_cell.count(';') + 1
        total += n; rowcount += 1
```
Result: **rowcount = 120, total = 277.**

Sanity check on row well-formedness (guards against the hard-wrap trap —
every register row here is one physical line, confirmed by requiring
exactly 8 `|`-split fields per row, 0 exceptions found):
```python
for i in range(start-1,end-1):
    ... if len(cells) != 8: print(...)
# → 0 bad rows
```
Both derived numbers (120 conditions, 277 instances) match §21.8's
post-repair sentence exactly: "Every row of §21.2 through §21.5 — 120
conditions over 277 instances." **hunk-03 and hunk-05 are mutually
consistent, confirmed by direct recount, not by re-reading the diff.**

I additionally checked whether reverting only R8 to its pre-repair 2
instances reproduces the pre-repair total: 277 − 2 = 275, matching hunk-05's
removed text exactly — confirms R8 is the *sole* source of the delta (no
other row's instance count is implicated by either hunk).

Check 1 (quantifier match against the governing rule): R8's Governing rule
is `[R-MTA-04]`. Read `[R-MTA-04]`'s actual "Finite numbers only" bullet
(§18.x, lines ~2693-2700, untouched by any hunk):
> "A document is unreadable if it contains a number whose binary64
> interpretation is not finite — which covers a magnitude that overflows
> on conversion, `1e400` being the ordinary case — or any of the bare
> tokens `NaN`, `Infinity`, or `-Infinity`, which RFC 8259 does not admit
> and some parsers accept regardless."
hunk-03's new R8 condition text: "a magnitude whose binary64 interpretation
overflows (`1e400`), or one of the bare tokens `NaN`, `Infinity` and
`-Infinity`, which RFC 8259 does not admit." This is a faithful, same-shape
restatement of the governing rule (same two-way split, same example, same
RFC citation) — **matches**, and is a strictly *more* faithful restatement
of `[R-MTA-04]` than the pre-repair "in any form" phrasing was.

Cross-check against §21.1's own instance-counting rule: "one whose members
give the condition materially different shapes enumerates them (T15,
T25)." Magnitude overflow and bare-token rejection are different detection
mechanisms (numeric-range check vs. lexical/token check) — materially
different shapes, correctly enumerated. Also checked neighboring rows R6
and R7, both **already** split this way pre-repair (R6: empty-key /
control-code-key × 2 containers = 4; R7: three shapes × 2 containers = 6) —
confirming R8's old 2-instance form was the outlier, and the repair brings
it into line with the register's own established convention. **No defect;
strong positive confirmation.**

Byte-level: **no** for either hunk in isolation (a register instance count
is corpus-coverage bookkeeping under [R-ERR-02], not a file-conformance
predicate) — but the *pairing* had to be checked for mutual consistency,
which it is.

### Group E — hunk-06, broken citation

Rule adopted: item 5 of the (non-normative, per its own heading) Appendix G
reproducible-writer profile now also requires fixed tile extents and a
fixed layout for byte-identical output, "and item 2 names both."

Check 2 (citations): read Appendix G's own numbered list in full (items
1-8, lines 4498-4600). **Item 2** is:
> "`file_id` from a cryptographic hash of the file's own emitted bytes..."
— entirely about the trailer's `file_id` field; it does not mention tile
extents, layout, or anything geometric. Checked §11.3 (cited immediately
after, for tile extents) and §14.1 (cited for layout) for any numbered list
of their own that might be the intended "item 2":
```
sed -n '1663,1700p'  → §11.3 is two paragraphs and one blockquoted Note,
                        no numbered list.
grep -n "^#### 14\." → §14.1 "The value sequence" is prose plus one
                        bullet pair (Planar/Interleaved), no numbered
                        list either.
```
Searched the whole document for any other numbered list that names both
"tile extent" and "layout" as members:
```
grep -n "deliberately leaves open|degrees of freedom|writer's choice"
→ only 3 hits, none a numbered list.
```
The only numbered list in scope at all is Appendix G's own (items 1-8),
and by ordinary anaphoric resolution ("item 2" with no other antecedent in
view) a reader lands on the `file_id`-hash item. **Citation does not
resolve — it points at unrelated content.** This is Check 8's back-reference
failure in miniature: the new sentence *introduces* a bare numeric
reference ("item 2") whose only available antecedent, the enclosing list,
gives the wrong answer, and no other candidate list exists anywhere in the
document.

The *substance* either side of the bad citation is independently correct:
"§11.3 states that tile extents are a writer's choice and that this
specification imposes none" matches §11.3's Note verbatim in substance
("Tile extents are a writer's choice, and this specification imposes
none..."); "§14.1 leaves the layout to the writer" matches §14.1's "1 =
interleaved and 2 = planar are the only values... a writer MAY emit."
Only the "item 2 names both" clause is wrong.

Check 7 (analogy): the surrounding "likewise" chain — "A fixed filter value
**likewise**... Fixed declared tile extents and a fixed layout
**likewise**" — analogizes three same-shaped freedoms (filter, tile
extents, layout: each a writer's-choice-with-no-content-implication that
still changes stored bytes). The analogy's own logic is sound; only the
appended citation is broken.

Byte-level: **no.** Appendix G is explicitly non-normative ("It adds no
requirement to any actor: a writer ignoring it is fully conforming"), so no
conforming/nonconforming verdict on any byte sequence turns on this
citation being right or wrong. Still reported per the charter ("a citation
that points at a rule which almost says the claimed thing is the most
expensive kind of defect here, because it reads as verified").

## Rejected candidates

- Hunk-01 reclassifying a body blockquote as `**Note.**`: considered
  whether this strips force from something load-bearing. Rejected —
  §4.7 independently and normatively restates the only substantive claim
  in the block (structural/descriptive field classification), unlabeled,
  so nothing normative depends solely on the now-exempt block.
- Hunk-02 vs. the pre-existing "barriers weaker than assumed" Note (line
  1283): considered as a possible contradiction (one says omission is
  invisible, the other says weak barriers are still caught). Rejected —
  they describe different scenarios (no crash vs. an actual crash) and
  are jointly consistent.
- Hunk-03/hunk-05 pairing: considered as the most likely site of a
  "changed-together, silently diverged" defect per the charter's explicit
  hint. Rejected after independent recomputation of the register's row
  and instance counts from the current file (120 rows, 277 instances,
  matching both the R8 row as currently written and §21.8's stated total
  exactly), and after confirming R8's new split matches its governing
  rule `[R-MTA-04]` and the register's own established convention (seen
  already in sibling rows R6/R7).

## Confidence on the empty parts

I did not come back with an empty finding set, but for completeness: the
main techniques that would have caught a defect I didn't find and didn't —
(a) independent recomputation of every derivable number the hunks touch
(120/277, cross-checked two ways), (b) grepping every citation's target and
reading it rather than trusting the citing sentence, (c) tracing every
"the Note above" / "that clause" / "item N" back-reference to its actual
nearest antecedent by line position rather than by the repair's evident
intent, (d) reading the full untouched paragraphs on both sides of every
insertion. I did not exhaustively re-derive every other cross-reference in
the document outside the six hunks' immediate neighborhoods (e.g. I did not
re-verify every one of [R-CNF-02]'s or [R-CNF-07]'s other citation sites
throughout the whole spec beyond what each hunk's own text cites) — that is
outside a cross-hunk audit's scope, since those sites are untouched by this
commit.
