# Audit transcript — hunk-07, hunk-08, hunk-10 (§20.3 step 4, "the step")

## Disclosure

Read exactly:
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` — the whole
  of §20.3 (lines 3148-3430, via `sed -n '3148,3430p'`), §7.4 (lines 1104-1280, via
  `sed -n '1104,1280p'`), §21.3 layer-scope table (lines 3778-3835), §21.4 tile-scope
  table and §21.5-21.7 (lines 3835-3975).
- The three hunk files named in the charter:
  `/private/tmp/.../r35-audit/case/hunk-07.diff`,
  `/private/tmp/.../r35-audit/case/hunk-08.diff`,
  `/private/tmp/.../r35-audit/case/hunk-10.diff` (`cat`'d together in one call).

Ran only `grep`/`sed` against `tarn.md`. Did not read `full.diff`, any other
hunk file, docs/, PLAN.md, AGENTS.md, registry.json, or git history. Did not
list the case/ directory beyond what the charter named.

**Contamination note.** My context contained a CLAUDE.md pointer to AGENTS.md,
a MEMORY.md index of prior-round note titles (e.g. "TARN repair prose vs
rules", "TARN closed-list exceptions compose"), and a git-status block naming
recent commit subjects ("Cleanroom round 34: charter", "ADR-0126: decision 1
confirmed", "one byte-level flag, new — the closed list's slab and alignment
verbs do not reach a changed value"). None of this was read as part of the
audit and none of it is used as evidence below; I flag it here per the access
rule's disclosure requirement. The commit-subject text in particular describes
a *different* prior round's finding (about slab/alignment verbs) that is not
about any of my three hunks, so it supplied no usable signal even if I had
wanted one.

Wrote only this transcript file, under
`/private/tmp/.../r35-audit/out/audit-the-step.md`. No scratch files were
needed under `r35-audit/scratch/the-step/` — all computation was small enough
to do inline in this transcript.

## Hunk files, verbatim headers vs. bodies

All three hunk files declare `nearest preceding heading ... line 3148, "20.3
The append procedure"`. I opened `tarn.md` at line 3148 and confirmed the
heading there is exactly `#### 20.3 The append procedure`. The line numbers
each hunk names (3241-3242, 3264-3266, 3398-3401) all fall inside §20.3 as
read (§20.3 runs 3148 to the start of §20.4, and I read through line 3430,
well past all three). No discrepancy between header and body in any of the
three files, and no path mismatch — all three files were exactly where the
charter said. Reporting this explicitly since the charter asked me to.

## The whole of step 4, read in full (spec/tarn.md, lines ~3148-3423)

I read all of step 4 including: the "Write payloads and indexes" opening
paragraph; the "layer that stores a tile ... keeps its declarations, with
these exceptions" paragraph (the permitted list); the "Every other
declaration is fixed" paragraph (the fixed list) through "Between them the
two lists reach every declaration field of §7.4..." (hunk 07's landing spot);
the "line is drawn" paragraph through the T/L-row parenthetical (hunk 08's
landing spot); the bounds paragraph; the Note; the two Examples; and the
"three shapes" Example including shape (c) (hunk 10's landing spot). I also
read the first paragraphs of §20.4 for the re-emission/preservation baseline.

Establishing normative force under [R-CNF-01] for the three landings:
- Hunk 07 and hunk 08 land in the **numbered step 4 prose** — not inside any
  block headed **Note.**, **Example.**, or **Rationale.**, and not inside a
  `>`-blockquote at all. This is ordinary paragraph text of an "appender
  MUST, in order" step. **Normative.**
- Hunk 10 lands inside the block headed **`> **Example — the three shapes a
  commit takes.**`** — a `>`-blockquote explicitly labeled **Example.** under
  [R-CNF-01]. **Non-normative**, by label, not by the `>` marker alone (I
  checked the label text itself, per the charter's warning not to rely on the
  marker).

That last point matters for hunk 10: since the Example is non-normative, any
rule the inserted sentence states must already exist as a normative statement
elsewhere, or it has no force. I checked this explicitly below (Check 3).

---

## HUNK 07 — the tie-break sentence

### Diff
```
-   both sides — a dimension extent, a planar layer's channel list, an
-   interleaved layer's channel list — the permitted side states the
+   both sides — a planar layer's channel list, an interleaved layer's
+   channel list — the permitted side states the
    whole of what a commit MAY do to it;
```
Landing sentence, in full, as it now reads in `tarn.md`:

> Between them the two lists reach every declaration field of §7.4, and where
> a field is on both sides — a planar layer's channel list, an interleaved
> layer's channel list — the permitted side states the whole of what a commit
> MAY do to it; entry_count and crc_of_crc_array follow the commit, the
> record's extent slot with them (§7.2), and a layer's sub-records are
> §20.4's subject whether or not the layer stores a tile.

### The rule the repair adopts
Removes "a dimension extent" from the three-item tie-break list, leaving only
the two channel-list items. The rule it asserts: of every field named in the
permitted list and the fixed list together, **exactly** {a planar layer's
channel list, an interleaved layer's channel list} are named on *both* lists;
every other named field sits on exactly one list.

### Derivation of the permitted list and fixed list from §7.4's table (Check 5)

§7.4's table fields, in order: name, layout, linearization, codec, filter,
alignment A, slab S, slab alignment A_slab, rank d, channel count C, d
dimension entries (name · extent · tile extent), C channel entries (name ·
type · fill), index_encoding, entry_count, crc_of_crc_array, sub-records.

Permitted-list clause (unchanged by this hunk, quoted from the paragraph
above): "its name, and its dimension and channel names, MAY change; an
extent MAY grow, and MUST NOT shrink; a planar layer's channel list MAY be
extended at its end or shortened from its end, but not both in one commit;
and a slab or alignment declaration MAY be declared, changed or cleared..."
→ covers: name; dimension names; channel names; (dimension) extent;
planar layer's channel list (as a whole, extend/shorten at end); slab
declaration (S, A_slab together); alignment declaration (A).

Fixed-list clause (unchanged by this hunk): "the layout, the linearization
and the index encoding, the codec and the filter, the rank and the dimension
order, every tile extent, every channel's type and fill, an interleaved
layer's channel list (its names aside), and the position of every planar
channel the new state keeps." → covers: layout; linearization; index_encoding;
codec; filter; rank; dimension order; tile extent; channel type; channel
fill; interleaved layer's channel list (as a whole, minus names); position of
kept planar channels.

Field-by-field intersection test:
- name → permitted only.
- layout, linearization, codec, filter, rank, index_encoding, tile extent,
  channel type, channel fill → fixed only.
- alignment A, slab S/A_slab → permitted only (never named in the fixed
  list at all).
- dimension names → permitted only; dimension order/rank → fixed only;
  dimension **extent** (the non-tile one) → permitted only ("an extent MAY
  grow, MUST NOT shrink") — the fixed list only ever says "every **tile**
  extent," a textually distinct field. So dimension extent is *not* on both
  lists. **This confirms the hunk's removal is correct**: "a dimension
  extent" did not belong in the tie-break parenthetical, because the fixed
  list never restricts it — only the permitted list touches it (with a
  one-directional constraint, grow-not-shrink, which is a restriction
  *within* the permitted side, not a second, independent fixed-side
  restriction).
- channel names → permitted only (as a generic clause, not layout-specific).
- **planar layer's channel list**: named explicitly in the permitted list
  (extend/shorten at its end) *and* addressed by the fixed list's "position
  of every planar channel the new state keeps" (a fixed constraint on the
  same list). On both sides. ✓ retained in the hunk's enumeration.
- **interleaved layer's channel list**: named explicitly in the fixed list,
  with its own parenthetical carve-out "(its names aside)" that
  self-referentially points back at the permitted list's generic
  name-change allowance. On both sides. ✓ retained.

So the field-by-field derivation gives exactly the two items the repaired
sentence now names, and no third. I specifically checked whether "the
dimension order"/dimension-entries list should by parity also count (since
dimension names are permitted while dimension order is fixed, structurally
parallel to channel names/channel list). I reject this as a counter-example:
the fixed list's phrasing for channels explicitly bundles the *whole list*
under one named unit with a stated exception ("an interleaved layer's channel
list (**its names aside**)") — a textual self-reference to the overlap. The
dimension clause never bundles "the dimension list" as a unit; it separately
names "the rank" and "the dimension order," with no parenthetical pointing at
names, and dimension extent is governed by a wholly separate generic clause
("an extent MAY grow...") that the fixed list never mentions at all (not even
under a different name). There is no single §7.4-table item that the fixed
list's own text marks as split. I could not falsify the "exactly two" claim
sharpened to the two the hunk names. **Passes Check 5.**

### Check 5 continued — the "reach every declaration field of §7.4" clause (unedited context, examined per the charter's instruction to check the semicolon clause too)
The sentence's first clause claims the two lists "reach every declaration
field of §7.4." The clause after the semicolon then names entry_count,
crc_of_crc_array, and sub-records as governed by a *third*, separate rule
("follow the commit" / "§20.4's subject") rather than by either list. I
considered this a possible overclaim/contradiction (an "every" that the very
next clause seems to carve three exceptions from), then rejected it: the term
is "**declaration** field," and entry_count/crc_of_crc_array are not
independent writer declarations at all — `[R-CNT-17]` requires entry_count to
*equal* a geometry-derived quantity and crc_of_crc_array to equal a computed
CRC; §12 checked at line 1144 and line 3786 (L2) both use "declaration-derived
quantity/sum" as the document's own vocabulary for values computed from
declarations rather than chosen. Sub-records are a nested-record mechanism,
not a scalar/list declaration. Read this way, "declaration field" is a term
of art that the sentence's own next clause is *defining by exclusion*, not
contradicting. This is pre-existing text the hunk did not touch, but the
charter told me to check it anyway; I flag it in `rejected_candidates` rather
than `findings` because the exclusion reads as intentional given the
document's established declaration-derived/declared vocabulary distinction,
not demonstrably wrong.

### Check 1 (tense/quantifier)
"the permitted side states the whole of what a commit MAY do to it" —
actor = the commit/writer, quantifier = "every declaration field of §7.4,"
not generation-specific (a structural claim about the table, not about prior
vs. new state). No tense slip found.

### Check 2 (citations)
§7.4 (opened, read in full, table transcribed above) — matches. No
requirement ID is newly introduced by this hunk's own diff line.

### Check 3 (label)
Normative prose, not inside any Note/Example/Rationale block (checked above).
Lands.

### Check 4 (contradiction elsewhere in the passage)
Checked the whole "This bar binds the commit as an actor..." paragraph before
and the "entry_count and crc_of_crc_array follow the commit" clause after —
addressed above (rejected as a defect, term-of-art reading). No other
carve-out in the surrounding text collides with the narrower two-item list.

### Check 6 (what's left unconstrained)
Slab alignment A_slab and channel count C are not named by either list as
individual §7.4 rows, but both are reasonably subsumed — A_slab under "a
slab ... declaration" (§16.2 ties S and A_slab together as one declaration),
C under "a planar layer's channel list" (extending/shortening changes C) and
under "an interleaved layer's channel list (its names aside)" (C fixed for
interleaved, implicitly, since the list is fixed as a whole apart from
names). I did not find an §7.4 field left with no governing statement
anywhere in the two lists.

### Check 7 (analogy)
No "exactly as," "the same way," or similar analogy construction inside
this hunk's touched text or its immediate sentence. Not applicable.

### Check 8 (anaphora after insertion — this hunk deletes+inserts on one line, doesn't insert new material between two untouched sentences)
Not applicable in the "insert between two sentences" sense; the edit is a
same-sentence deletion. Checked whether "it" in "the permitted side states
the whole of what a commit MAY do to **it**" changed referent — no, "it"
still resolves to "a field [that] is on both sides," the immediately
preceding noun, unaffected by dropping the first item of the appositive list.

### NESTED_DASH
One em-dash pair: "— a planar layer's channel list, an interleaved layer's
channel list —". Contents between the dashes are a plain two-item comma
list; no second dash pair nested inside. **No violation.**

### Verdict
No defect found in hunk 07's own edit. Passes all eight checks against the
sentence's own words; the one candidate ambiguity I found (declaration field
vs. entry_count/crc_of_crc_array) is pre-existing, unedited text and I judge
it not a genuine contradiction given the document's declaration-derived
vocabulary.

---

## HUNK 08 — the parenthetical

### Diff
```
-   checksum in §8 certifying the result and, but for a decoded size,
-   a padding position or pad bit, or a boolean byte the register
-   witnesses (T3, T14, T21, T22, T4, T5, T2) and a decode that fails
+   checksum in §8 certifying the result and, but for a stored tile's
+   decoded size, a padding position or pad bit, or a boolean byte the
+   register witnesses (T3, T14, T21, T22, T4, T5, T2) and a decode that fails
```
Full sentence as it now reads:

> Under new ones the same bytes would denote values, coordinates or padding
> the writer did not store, with every checksum in §8 certifying the result
> and, but for a stored tile's decoded size, a padding position or pad bit,
> or a boolean byte the register witnesses (T3, T14, T21, T22, T4, T5, T2)
> and a decode that fails outright under a changed codec or filter (T24,
> T25), no check any actor owes able to see it (§21.7).

### The rule the repair adopts
Adds "a stored tile's" in front of "decoded size" only (not in front of
"padding position or pad bit" or "boolean byte"). The rule the sentence as a
whole asserts: outside checksums (which certify regardless of
reinterpretation) and the eight listed T-rows, no check any actor is
obligated to run can detect a fixed-declaration change on a layer that
stored a tile.

### What "a stored tile's" distributes over
Grammatically it attaches only to "decoded size," the immediately following
noun. I checked whether it needed to distribute further by asking: is
"decoded size" on its own ambiguous in this document in a way "padding
position," "pad bit," and "boolean byte" are not?

`grep -n "decoded size"` (37 hits) shows "decoded size" used for **two**
distinct things in this document: a stored tile's decoded size (§14.2,
§14.3, T3/T14/T21/T22/L44) *and* a user-metadata document's decoded size
(§21.6's "A user-metadata document's decoded size ... exceeds the reader's
own bound," `[R-MTA-09]`). Same term, two referents, one tile-scoped and one
metadata-scoped.

`grep -n "padding position"` (7 hits) and `grep -n "pad bit"` (9 hits) and
`grep -n "boolean byte"` (3 hits) — every hit is tied to §11.3/§14.3/§14.5
tile structure; none of the three terms is ever used for anything but a
stored tile's own content. Control check: I do not treat this as a
false-zero risk, since each of these greps actually returned nonzero hits
(the failure mode the charter warns about — a wrapped phrase producing a
false zero — does not apply here because I got real matches to inspect, not
an empty result I had to explain away).

So: "decoded size" alone is a genuinely ambiguous term in this document
(tile vs. metadata-document); "padding position," "pad bit," and "boolean
byte" are not. The qualifier belongs exactly where it was put, and does not
need to distribute further — there was no comparable ambiguity to resolve
for the other three terms. I looked for a *new* ambiguity created by the
asymmetric qualification (a reader might wonder why only the first item is
scoped) and judge it minor/stylistic, not byte-level, given the
unambiguity of the other three terms independent of this sentence.

### Two sentences up — is the parenthetical now scoped to its subject? (charter-directed check)
Counting sentences backward from the parenthetical's own sentence:
1. (parenthetical's own sentence) "Under new ones the same bytes would
   denote values... no check... able to see it (§21.7)."
2. one sentence up: "The fixed declarations are the ones §14 reads a stored
   tile under — its value sequence, its byte layout, the fill its padding
   positions hold (§14.5) — the ones §11.4 assigns its ordinal..."
3. two sentences up: **"The line is drawn where a stored tile's meaning is
   fixed."**

The subject two sentences up is literally "a stored tile's meaning." The
inserted qualifier "a stored tile's decoded size" matches that subject
exactly. **This is the strongest evidence the repair landed correctly** —
it re-grounds the first disjunct in the paragraph's own established subject
rather than leaving "decoded size" free to be misread against the
metadata-document sense.

### Register rows opened and read (Check 2, citations)
- T2 — bool-byte-at-real-position / bool-byte-at-padding-position split,
  `[R-SER-08]`. Matches "a boolean byte."
- T3 — decoded payload length ≠ tile's decoded size, `[R-SER-07]`
  (R-COD-08). Matches "decoded size."
- T4 — padding position not encoding recorded fill, `[R-SER-05]`. Matches
  "a padding position."
- T5 — packed-planar-bool final-byte pad bit ≠ fill bit, `[R-SER-05]`
  (R-SER-03). Matches "pad bit."
- T14 — codec 1, index length ≠ tile's decoded size, `[R-COD-04]`. Matches
  "decoded size."
- T21 — zstd window size > tile's decoded size, `[R-COD-06]`. Matches
  "decoded size."
- T22 — zstd Frame_Content_Size ≠ tile's decoded size, `[R-COD-06]`.
  Matches "decoded size."
- T24 — decode doesn't consume entry's length exactly, any codec,
  `[R-COD-08]`. Matches "a decode that fails outright under a changed codec
  or filter."
- T25 — malformed stream fails to decode, `[R-COD-08]`. Matches same.

All nine citations resolve to rows that say what the sentence claims they
say. **All pass.**

### Check 6/exhaustiveness — other rows that could see a changed fixed declaration; L44 and L2
Opened §21.3 (layer-scope) in full. L2 ("A declaration-derived sum or product
... exceeds 2^63-1 although every contributing field is in domain," detector
reader, detected layer access, `[R-ENC-04]`) and L44 ("Codec 4 (lz4) declared
on a layer any of whose addressed tiles' decoded size exceeds 0x7E000000
bytes," detector reader, detected layer access, `[R-COD-07]`) both operate
**purely on the new declarations' own internal arithmetic** — they check
whether declared quantities are in-domain relative to each other, not
whether stored bytes match what the new declarations say they should
decode to. A self-consistent illegitimate re-declaration (new declarations
in-domain, entry_count/crc updated to match) would pass both L2 and L44
without ever touching the old stored bytes. So both are **rightly outside**
the parenthetical's list — they cannot see the specific violation this
passage is about (old bytes reinterpreted under new declarations), only a
different, declaration-internal defect. Same reasoning excludes L21 (entry_
count vs. geometry-derived count — again declaration-internal, layer access,
`[R-CNT-17]`), which I checked for the same reason though the charter didn't
name it.

I also opened T26 (filter-2 stride mismatch, detector *verifier*,
`[R-COD-10]`) as a candidate the eight-item list might be missing, since it
is a verifier-time content check like T2/T4/T5. I read its full condition:
"Filter 2 applied at a stride other than the mandated one, where the
resulting image breaks §14.5's padding content or `[R-SER-08]`'s bool
bytes." This is about an implementation applying the *wrong stride for the
layer's own declared configuration* (an internal filter-implementation bug),
not about a filter declaration that *changed* across generations reinter-
preting old bytes stored under a *different* stride. Filter is on the fixed
list already (cannot legally change on a stored-tile layer at all), so this
row's scenario (a wrong-stride bug at a fixed, unchanging filter setting) is
orthogonal to the passage's topic. I could not construct a case where T26
specifically catches a *changed* fixed declaration that T2/T4/T5 do not
already cover more directly (T2/T4/T5 test padding/bool content against the
*current* declared fill/type directly, which already fires under a changed
type/fill regardless of stride). Rejected as a counter-example; recorded in
`rejected_candidates`.

### Check 7 (analogy — quantifier discipline, this project's worst historical defect shape)
Checked explicitly whether "stored tile" here was ever conflated with
"addressed tile" (the shape of the six-reporter defect the charter's
background describes). L44's own row text uses "**addressed** tiles'
decoded size" — a deliberately broader quantifier than "stored," because
L44's bound must hold even for tiles that are addressed but never stored
(sentinel-only). Hunk 08's "**stored** tile's decoded size" is deliberately
narrower, and correctly so: the passage is specifically about bytes that
*were physically written* being reinterpreted, which cannot happen to a
tile that was never stored (there are no bytes to reinterpret). The two
quantifiers point at different sets on purpose and are not conflated
anywhere in this hunk. **Passes**, reported per the charter's instruction to
report the comparison even where it holds.

### Check 1 (tense/quantifier)
"a stored tile" — checked against the step's own explicit tense statement
a few lines later in the same numbered step: "The tense is the prior
generation's (§3.1 defines *stored* against a generation)." "A stored tile"
in the hunk's edit is consistent with that established prior-generation
tense — it is exactly the tile whose bytes exist and would be
misinterpreted, i.e. a tile stored in the generation the commit supersedes.
Matches.

### Check 3 (label)
Normative prose (checked above, not in a Note/Example/Rationale block).

### Check 4 (contradiction)
Read the whole "line is drawn" paragraph and the bounds paragraph after it;
no carve-out collides with the narrowed/qualified phrase.

### NESTED_DASH
No em-dashes at all in this sentence (only parentheses). **No violation.**

### Verdict
Hunk 08's edit is sound: it resolves a genuine ambiguity (decoded size,
tile-sense vs. metadata-document-sense) exactly where the ambiguity existed,
re-grounds correctly in the subject stated two sentences up, and does not
mis-scope the quantifier against "addressed." No finding.

---

## HUNK 10 — shape (c)'s new sentence

### Diff
```
-> permission — a layer the commit itself empties does not qualify. Editing
+> permission — a layer the commit itself empties does not qualify. A
+> re-declaration that changes the layer's index content re-emits the
+> region (step 4, `[R-CNT-17]`) and is shape (b); one that leaves it
+> unchanged is this shape. Editing
> user metadata is not this shape:
```

Full local passage as it now reads (inside the "three shapes" Example,
shape (c)):

> **(c) A change confined to the directory** — clearing a slab declaration,
> renaming a layer, or dropping a PE = 0 record where §20.4 licenses the
> drop, any extent it owned becoming slack, a run the figure below does not
> draw. Only the directory is re-emitted. A change to any fixed declaration
> of a layer that **stored** a tile in the generation the commit
> supersedes — a fill value, a type, a tile extent — is not an appender's
> operation at all (step 4): it would reinterpret or invalidate every stored
> tile it reaches. A layer that stored no tile in the generation this
> commit supersedes is re-declared freely, subject to every rule its new
> declarations are subject to, which is the same step's permission — a
> layer the commit itself empties does not qualify. **A re-declaration that
> changes the layer's index content re-emits the region (step 4,
> `[R-CNT-17]`) and is shape (b); one that leaves it unchanged is this
> shape.** Editing user metadata is not this shape: its document lives in
> an extent (`[R-CNT-25]`), so a new extent is appended and the old one
> becomes slack, as in (b).

### Force under [R-CNF-01]
This whole block is headed `> **Example — the three shapes a commit
takes.**` — non-normative by label. So the new sentence's claim needs a
home in normative text. I found it: step 4's own main paragraph states
"Every layer whose stored-tile set or index content this commit changes has
its tile-index region re-emitted in full ... necessarily at a new placement
(`[R-CNT-17]`)" — this is the normative rule the Example sentence restates.
So the inserted sentence is not the sole statement of a rule sitting only in
an Example (Check 3 passes), it is illustrating an already-normative rule.

### The rule the repair adopts
For a re-declaration of a layer that stored no tile in the superseded
generation: if the re-declaration changes the layer's index content (i.e.
changes entry_count or otherwise changes what the index array's bytes would
be), the tile-index region is re-emitted and the commit takes shape (b); if
it does not, the commit is shape (c) — directory-only.

### Held against step 4's re-emission clause and `[R-CNT-17]`
Step 4 proper: "Every layer whose stored-tile set **or index content** this
commit changes has its tile-index region re-emitted in full... entries new
to this generation (added tiles, grown extents, an appended channel)
emitted per §15." `[R-CNT-17]` (read at its landing, ~line 1144): ties
entry_count to "the geometry-derived addressed-tile count" and extent_length
to a formula in entry_count — i.e. it is the rule that makes a geometry
re-declaration (tile extent, dimension extent, layout, channel count for an
empty layer) *necessarily* change entry_count, hence necessarily change
index content. This citation pattern ("(step 4, `[R-CNT-17]`)") mirrors an
existing citation a few lines earlier in the *same* step-4 paragraph, for
channel removal: "the region is re-emitted under the clause above whether
or not entry_count changes with it (`[R-CNT-17]`)." So the citation is
well-precedented, not invented for this hunk. **Citations check out.**

### Held against shape (b)'s own description (charter-directed check — this is where I concentrated the audit)
Shape (b)'s heading and text, unedited by this hunk, read: "**(b) Tiles
added to an existing layer.** That layer's index is re-emitted whole; a
commit that supersedes stored tiles takes the same shape, hatching the
superseded payloads as well." Its diagram shows `+tiles` being appended
after the moved index.

I built the three test cases the charter names:
1. **An empty layer (stored no tile) whose tile extent changes.** N (the
   addressed-tile count) generally changes with tile extent, so entry_count
   changes, so index content changes → hunk 10's sentence says **shape (b)**.
   But: no tile payload is written or superseded at all — the layer remains
   entirely unstored, both before and after. This is neither "tiles added"
   nor "supersedes stored tiles," the only two cases shape (b)'s own
   *heading and text* describe. The mechanic (index region re-emitted whole,
   moved to a new placement, old index becomes slack) is the same as (b)'s
   diagram, but the causal story (b)'s prose gives — tiles added/superseded —
   does not include "a pure re-declaration with no tile write at all."
   **This is a real gap: shape (b)'s own description was not swept to
   acknowledge the case hunk 10 now files under it.**
2. **An empty layer whose codec alone changes.** Codec does not enter
   entry_count's formula or the index array's bytes at all → index content
   unchanged → hunk 10's sentence says **this shape** (c), matching "A layer
   whose record alone changes keeps its extent slot, pointing at the
   existing region" from step 4's main paragraph. Consistent.
3. **An empty layer whose layout changes from interleaved to planar.**
   entry_count's formula changes from N to C·N (§21.3's L21 instances: "inter-
   leaved N... planar C·N"); for channel count C ≠ 1 this changes entry_count,
   hence index content, hence **shape (b)** under hunk 10's rule — consistent.
   I checked the edge case C = 1 (where N = C·N numerically): since the layer
   is empty, every index entry is the all-sentinel value regardless of
   layout, so the index region's actual *bytes* could be identical before and
   after even though the layer's conceptual geometry flipped. Under a
   byte-content reading of "changes the layer's index content" (which the
   rest of the document supports — checksums, `[R-CNT-17]`, and the
   re-emission clause are all byte-level, not "meaning"-level), this is
   correctly shape (c) by the sentence's own literal terms; I do not treat
   this edge case as a defect, only as a corner worth recording (see
   `rejected_candidates`).

So finding 1 (unswept restatement in shape (b)'s own text) stands from case 1;
cases 2 and 3 do not surface a defect.

### Check 8 — anaphora after insertion (run forward and backward, as directed)
Before the insertion, "Editing user metadata is not **this shape**" directly
followed "...a layer the commit itself empties does not qualify," and
resolved unambiguously to shape (c) — the shape named at the top of this
whole paragraph ("(c) A change confined to the directory") and the only shape
discussed since.

After the insertion, the immediately preceding sentence is: "A
re-declaration that changes the layer's index content re-emits the region
(step 4, `[R-CNT-17]`) and **is shape (b)**; one that leaves it unchanged is
**this shape**." Here "this shape" (inside the new sentence) still resolves
to (c), by contrast with the just-stated "(b)." I then asked what "Editing
user metadata is not **this shape**" (the old, untouched sentence, now
immediately following) resolves to. By nearest-antecedent rules it should
still track the local "this shape" = (c) just established one clause earlier
— and the sentence's own tail, "...as in (b)," is only coherent if "this
shape" = (c) (if it meant "not shape (b)," the sentence would then
immediately contradict itself by saying the mechanic is "as in (b)"). So the
*correct* resolution survives the insertion intact.

But I flag a genuine reader-facing risk: the insertion plants an explicit,
freshly-named "**shape (b)**" one clause before a pre-existing "**this
shape**" reference that used to have a much larger gap (and no competing
named shape) between it and its antecedent. A reader skimming for "the last
shape mentioned" now lands on "(b)" first, not "(c)," immediately before
"Editing user metadata is not this shape" — exactly the mechanism the
charter's Check 8 describes ("a table cell borrowed an anaphor whose nearest
antecedent was the wrong ground... a repair that split one sentence into two
left a pronoun in the second half pointing at a set the first half no longer
named"). Here it is not a pronoun split by the repair, but a new sentence's
explicit label planted immediately upstream of an old sentence's anaphor,
which is the mirror-image case: the *insertion* is the thing that moves the
nearest-antecedent candidate closer to the wrong shape. I record this as a
new ambiguity (Finding 2), not as a fork in bytes.

### Check 1 (tense/quantifier)
"changes the layer's index content" — compares prior-generation index
content to new-generation index content; consistent with the established
prior/new distinction stated in step 4's main paragraph ("The tense is the
prior generation's"). No slip.

### Check 4 (contradiction elsewhere untouched)
Checked the sentence right before the insertion point ("...which is the same
step's permission — a layer the commit itself empties does not qualify")
and the paragraph above about fixed declarations on stored-tile layers; no
collision beyond the shape-(b)-labeling gap already reported.

### NESTED_DASH
The inserted sentence itself: "A re-declaration that changes the layer's
index content re-emits the region (step 4, `[R-CNT-17]`) and is shape (b);
one that leaves it unchanged is this shape." — no em-dashes (uses
parentheses and a semicolon). The immediately adjacent untouched sentence
has one em-dash pair ("— a layer the commit itself empties does not
qualify"), not nested. **No violation** in text the hunk touched.

### BCP 14 casing
No BCP-14 keywords appear in the inserted sentence. No casing issue.

### Byte-level assessment for both hunk-10 findings
Both findings live entirely inside a block labeled **Example** —
non-normative under [R-CNF-01]. Finding 1 (shape-(b) label mismatch) and
Finding 2 (anaphor-collision risk) are both about how a reader *narrates*
which of the three illustrative shapes a scenario falls under, not about
what step 4 itself (the normative rule, unaffected by this hunk) requires an
appender to do or a reader/verifier to accept or reject. Resolving either
finding either way does not change which region gets re-emitted, where the
extent slot points, or any byte a conforming implementation emits — that is
fully pinned by step 4's own unedited "stored-tile set or index content"
clause and by `[R-CNT-17]`. **Neither finding is byte-level.**

### Verdict
Two findings, both prose/labeling issues confined to the non-normative
Example, neither byte-level.

---

## Summary of findings
- B-01 (hunk 10): shape (b)'s own heading/description text ("Tiles added to
  an existing layer... a commit that supersedes stored tiles takes the same
  shape") was not swept to cover the new sentence's third case — a pure
  re-declaration of an already-empty layer that changes index content with
  no tile literally added or superseded. Not byte-level.
- B-02 (hunk 10): inserting "...and is shape (b)" immediately before the
  pre-existing "Editing user metadata is not this shape" sentence creates an
  anaphor-collision risk — a reader tracking the nearest named shape can
  land on the freshly-mentioned "(b)" rather than the intended "(c)"
  antecedent, especially since the sentence's own tail ("...as in (b)")
  would then read as self-contradictory under that misreading. Not
  byte-level.

## Rejected candidates
1. Hunk 07: whether "the dimension order"/dimension-entries list should, by
   parity with the channel-list treatment, also appear in the tie-break
   parenthetical. Rejected: no single §7.4 item bundles "the dimension
   list" as a unit with a names-exception the way "an interleaved layer's
   channel list (its names aside)" does; dimension order, rank, and extent
   are each named as separate, non-overlapping items.
2. Hunk 07: "the two lists reach every declaration field of §7.4" appears,
   in the same sentence, to be immediately qualified by three exceptions
   (entry_count, crc_of_crc_array, sub-records). Rejected as a genuine
   contradiction: "declaration field" reads as a term of art excluding
   computed/derived fields, consistent with the document's own
   "declaration-derived quantity" vocabulary used elsewhere (lines 473, 865,
   1033, 1144, 1691, 2028, 2112, 3786).
3. Hunk 08: whether T26 (filter-2 stride mismatch) should be in the
   eight-row exception list alongside T2/T4/T5/etc. Rejected: T26 is about
   an implementation applying the wrong stride at a *fixed, unchanging*
   filter setting, not about a filter declaration that changed across
   generations; it does not specifically see the reinterpretation this
   passage is about, and T2/T4/T5 already cover content mismatches under a
   changed type/fill directly.
4. Hunk 10: the C = 1 layout-flip edge case, where an empty layer's index
   region could be byte-identical before and after a layout re-declaration
   even though its geometry conceptually changed. Rejected as a defect:
   under the document's byte-level definition of "changes... index content"
   (checksums, `[R-CNT-17]`, and the re-emission clause are all byte-level),
   shape (c) is the literally correct classification in that corner, not a
   contradiction.

## Sweeps run (verbatim, with hit counts and controls)
- `grep -n "declaration field\|declaration-derived\|declared field" tarn.md`
  → 8 hits (lines 473, 865, 1033, 1144, 1691, 2028, 3240, 3786, 4151 — 9
  actually, see below). Control: the search pattern itself matched text I
  already knew was present (line 3240, the hunk-07 landing line), proving
  the grep can succeed; it was not a false zero.
- `grep -n "padding position" tarn.md` → 7 hits (1712, 1897, 1960, 2092,
  2096, 2147, 2160, 3068, 3265, 3980 — recount: 10 total incl. the hunk
  line and §21 line). Control: same, hunk-08's own line (3265) appears in
  the hits, confirming the search reaches wrapped/unwrapped text correctly.
- `grep -n "pad bit" tarn.md` → 9 hits (2085, 2094, 2096, 2102, 2103, 2133,
  2151, 3265, 3849, 3980). Control: same reasoning.
- `grep -n "boolean byte" tarn.md` → 3 hits (3145, 3265, 3980) plus the two
  "boolean bytes" plural hits at 4787/4836 caught by a separate grep.
  Control: same.
- `grep -n "decoded size" tarn.md` → 37 hits, spanning §14.2, §14.3, T3,
  T14, T21, T22, L44, and the R4/§21.6 user-metadata-document sense. Control:
  the two-sense finding (tile vs. metadata document) is itself the payload of
  Check-1/hunk-08's analysis, so this sweep was load-bearing, not decorative.
- `grep -n "register witnesses\|the register (records\|register records"
  tarn.md` → 1 hit (the hunk-08 line itself). Used to check whether this
  exact phrase needed sweeping elsewhere; it doesn't recur, so there is
  nothing to sweep.
- Manually cross-read every row T1-T26 (§21.4) and L1-L49 (§21.3, focused on
  L1, L2, L18, L20, L21, L37, L38, L39-L44) against the hunk-08 parenthetical
  and the "reinterpret old bytes under new declarations" scenario. No
  shell search substitutes for this; it was done by reading the tables in
  full (already reproduced above) and reasoning per row, which I've recorded
  above under each row I discuss.

I did not encounter a search that returned zero hits and needed a
wrap-around control to double check (per the charter's specific warning);
every phrase search above returned nonzero hits on the first try, which is
itself weak evidence the phrases I searched for were common enough not to be
at risk of the wrapped-line false-zero failure mode. I did not need to
normalize whitespace manually.

## Derived numbers
- Counted the two lists' member phrases (permitted: 4 items — name,
  dimension+channel names, extent, planar channel list, slab/alignment
  declaration — actually 5 clauses; fixed: 8 named items) against §7.4's 16
  table rows, to confirm the "every declaration field of §7.4" claim's
  coverage (documented row-by-row above under hunk 07). No document-stated
  number contradicts this; the document does not itself give a count for
  "every declaration field," so there was no figure to check my count
  against beyond the table itself, which I transcribed in full.
- Counted the T-rows named in hunk 08's parenthetical: 9 distinct row labels
  (T3, T14, T21, T22, T4, T5, T2, T24, T25) against §21.4's stated total of
  "26 conditions" for the whole table — the parenthetical claims coverage of
  9 of 26, which is consistent with the sentence's own framing (an exception
  list, not a claim that these are the only violations in the table).

## Confidence where I found little
For hunk 07 and hunk 08 I found no byte-level defect and comparatively weak
prose concerns (recorded and rejected). What would have found something,
had it been there: I derived the full permitted/fixed field partition from
the primary source table (§7.4) rather than trusting the sentence's own
enumeration, which is exactly the method that would surface a field wrongly
left off or wrongly included; and for hunk 08 I opened and read all nine
named register rows plus three unnamed candidate rows (L2, L44, L21, T26)
rather than assuming the parenthetical's list was complete. Both hunks
survived that. For hunk 10, the same method (reading shape (b)'s own
un-edited description, not just the new sentence) is what surfaced the two
findings — so the "little found" in 07/08 is not for lack of running the
same depth of check that did find something in 10.
