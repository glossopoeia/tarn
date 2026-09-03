# Cross-hunk consistency audit — round 29, lane "cross-hunk"

## Access log

Read:
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md (in parts, via offset/limit — file too large for one read)
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-audit3/case/hunk-01.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-audit3/case/hunk-02.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-audit3/case/hunk-03.diff

Did NOT read: full.diff, any docs/, PLAN.md, AGENTS.md, registry.json, git log/diff, the web.

**Disclosure of unsolicited context**: before this task began, the runtime's system
reminders contained a project CLAUDE.md pointer, a user MEMORY.md index (with entries
like "TARN repair prose vs rules" and "TARN lineage gate word list"), and a `gitStatus`
block showing the 5 most recent commit subject lines (e.g. "Cleanroom round 29: zero
byte-level ambiguities, and G3's second half begins", "ADR-0116: §21.7's walk-through is
cut..."). None of this was fetched by me via a tool call; it was injected automatically.
I did not open any memory file, did not treat any commit subject as evidence about which
hunk is defective, and did not use "G3" or "§21.7" mentions in that commit-message text to
steer my search — my conclusions below are derived solely from the three hunk files and my
own greps of spec/tarn.md. Flagging this per the access-rule's disclosure requirement.

Local scratch: none needed beyond this transcript; all checks were done with `grep`/`python3`
one-liners inline (not saved to scratch/cross-hunk), reproduced verbatim below.

## The three hunks, restated

**Hunk 1** — spec/tarn.md lines ~16-20, inside the document's opening blockquote, which
is headed `> **Note.** How to read this document.` Edits the field-taxonomy summary:
"whether the file is accepted" → "whether the file, layer or tile is accepted at all".

**Hunk 2** — spec/tarn.md lines ~3901-3907, inside §21.7 "What no check detects", in the
paragraph defining *unwitnessed*/*detectable* as duals. Rewrites the sentence connecting
that duality to §21.1's register-completeness clause: splits one sentence ("...so an
unwitnessed condition is absent from it by that clause's own terms rather than in breach
of them.") into two ("...violation. An unwitnessed condition is not one, so that clause
requires no row for it and its absence from the register breaches nothing.").

**Hunk 3** — spec/tarn.md lines ~4577-4589, inside Appendix G item 5 (reproducible-writer
profile, "Fixed declared tile extents and a fixed layout"). Old text: "...and item 2 names
both: §11.3 states tile extents are a writer's choice... and §14.1 leaves the layout to the
writer, so two writers agreeing on everything above still emit different numbers of tiles,
of different shapes, without both pinned." New text specifies the mechanism separately for
each of the two freedoms: tile extents fix tile shape/grid count; layout fixes addressed-tile
count (§11.2) and intra-tile byte arrangement (§14.2).

## Step 1 — grouping by rule, not section

These three hunks turn out to touch **three distinct rule families** with no shared
requirement ID and no shared defined term:

- Hunk 1: the **scope taxonomy** of structural/descriptive fields (what "accepted" ranges
  over — file/layer/tile), governed by `[R-ENC-16]` (§4.7) and `[R-CNF-08]` (§2.4).
- Hunk 2: the **detectable/unwitnessed duality** and its role in §21.1's register
  completeness clause, governed by `[R-CNF-07]`, `[R-CNF-13]`.
- Hunk 3: the **reproducible-writer profile**'s enumeration of writer degrees of freedom
  that must be pinned for byte-identical output — a non-normative appendix, governed by
  no requirement ID at all (Appendix G "adds no requirement to any actor").

I looked hard for a shared thread (tile-level scope appears in hunk 1's "tile" and hunk 3's
tile geometry; §21.7 in hunk 2 cites `[R-COD-10]`, which Appendix G's *filter* clause
— untouched by hunk 3 — also cites). None of these amount to two repairs stating the same
rule with different quantifiers. I record the searches below and treat the three as
independent for the remainder of the audit, checking each one internally (checks 1-8) and
against the rest of the document, then re-checking specifically for the two cross-hunk
patterns the charter flags (label-vs-force, and the "one definition / one sentence
reporting it" pattern) even though they did not land inside my three hunks as a colliding
pair.

## Step 2/3 — per-hunk checks against the rest of the document

### Hunk 1

Rule adopted: a field is *structural* if (among other things) its value determines
"whether the file, layer or tile is accepted at all."

**Check 3 (label, not marker).** This text sits inside the document's very first
blockquote, headed `> **Note.**` — explicitly labeled, hence non-normative under
`[R-CNF-01]`. Confirmed no other label word governs this block (read lines 1-25 directly).

**Check 2 (citations).** The edited text has no bracketed identifier itself, but is a
paraphrase of §4.7. Opened §4.7 (lines 585-616):

> "A field is **structural** if its value determines anything a conforming reader or
> verifier does with the bytes it reads — where a byte lies, how it decodes, what a
> decoded value is, or **whether the file, layer or tile is accepted at all**, which is
> the sense `[R-CNT-07]`, `[R-MTA-02]` and `[R-SEC-06]` already use." `[R-ENC-16]`

§4.7 is plain paragraph text (not a blockquote at all) — normative. It already reads
"file, layer or tile," verbatim matching hunk 1's post-image. So: the non-normative Note
and the normative §4.7 definition **agree**, and the actual rule is the one in §4.7 (which
is normative and unedited by this hunk, but not in a labeled block, and not in dispute).

Search run (normalizing `> ` blockquote markers and whitespace so the hard-wrap can't hide
a match):
```
python3 -c "... re.sub(r'^\s*>\s?','',text,flags=re.M) ... 'whether the file, layer or tile is accepted' -> 2 hits"
```
Both hits are exactly the Note (line ~19-20) and §4.7 (line ~592) — no other restatement,
no stale "whether the file is accepted" left anywhere (0 hits for that shorter phrase).

**Check 5 (exhaustiveness).** "file, layer or tile" — checked against §2.4 line 303-304:
"Every structure this specification defines has exactly one **owning scope** — file, layer,
or tile." Exhaustive and exactly matching; not a closed-list overclaim.

**Check 8 (back-reference).** The following clause "**descriptive** (none of those — §4.7)"
— "those" now ranges over the four things listed including the broadened "file, layer or
tile" scope. Since §4.7 itself already states this fuller list, "those" resolves consistently
before and after the edit; no new mismatch.

No defect found in hunk 1, and no dependency of anything normative on this non-normative
restatement (the normative source, §4.7, is untouched and already agreed).

### Hunk 2

Rule adopted: the register (§21.2-§21.5) need not carry a row for an unwitnessed condition,
because unwitnessed is the exact negation of detectable, and completeness (§21.1) only
requires rows for *detectable* violations.

**Check 3 (label).** Confirmed via `grep -n "^>"` over lines 3877-3935: no blockquote
markers in this range. §21.7 is ordinary section prose, normative (not §1, not a labeled
block, not a non-normative appendix). The repair lands in force-carrying text.

**Check 2 (citations).** Opened §21.1 (lines 3557-3596):

> "Its **completeness is normative** — a *detectable* file-conformance violation this
> specification names and the register omits is a defect in this document, detectability
> being the gate `[R-CNF-07]` already applies and §21.7 states the test for..."

This matches hunk 2's "detectable file-conformance violation" quantifier exactly (not
"any violation," not "every named condition" — specifically *detectable*). `[R-CNF-07]`
(§2.4 line 287-289): "Every detectable file-conformance violation named by this
specification is assigned exactly one reader outcome... `[R-CNF-07]`" — consistent usage.

**Check 1 (tense/quantifier).** The paragraph immediately above hunk 2's edit (untouched)
states the duality hunk 2 relies on: "The two are stated over the same subject, and each
quantifier is the other's dual, so each is exactly the negation of the other." Hunk 2's "An
unwitnessed condition is not one [a detectable violation]" is a direct, licensed consequence
of that untouched sentence — same quantifier, same subject (conditions "this specification
names"), not a shift of generation or set.

**Check 4 (contradiction in the passage).** Read the whole of §21.1 and §21.7 (reproduced
above/below). §21.1 explicitly carves the completeness clause down to §21.2-§21.5, excluding
§21.6/§21.7/§21.9 by name — consistent with, not contradicted by, hunk 2's "breaches
nothing" (scoped implicitly to "that clause," i.e., §21.1's completeness clause, not some
broader obligation). No MUST elsewhere in §21.7 is loosened by this rewrite: the paragraph
after (untouched) still requires the requirement itself to bind ("Being unwitnessed bears on
detection and not on permission: the requirement binds its actor as any other does").

**Check 5 (exhaustiveness).** "breaches nothing" — checked whether some other clause imposes
a broader obligation the rewrite ignores. §21.8 (conformance vectors) only concerns existing
rows. §21.9 (limits) is unrelated. No such clause found.

**Check 8 (back-reference).** "That is the whole of the test" (first sentence of the next,
untouched paragraph) — checked what "that"/"the test" resolves to before and after the
edit. Before: the antecedent is the unwitnessed/detectable duality paragraph (two sentences
up), since "test" is first used as a noun there implicitly via "detectability so stated is
the gate... §21.1's completeness clause turns on." After hunk 2's split (one sentence
becoming two, same content, no new competing noun-phrase introduced before "the test"):
resolution is unchanged — still the duality/detectability test, not the (also unchanged)
register-completeness restatement. No anaphor mis-resolution.

No defect found in hunk 2.

### Hunk 3

Rule adopted: within Appendix G item 5, "fixed declared tile extents and a fixed layout"
is required for byte-identical output because (a) tile extent fixes tile shape and grid
count and (b) layout fixes addressed-tile count and intra-tile byte arrangement.

**Check 3 (label).** `grep -n "^>"` over lines 4489-4640: no blockquote markers. But
Appendix G's own heading reads "Appendix G — Reproducible-writer profile
(non-normative)" — the *appendix-identified-as-non-normative* branch of `[R-CNF-01]`,
distinct from the Note/Example/Rationale-labeled-block branch. So this hunk, like hunk 1,
lands in non-normative text — but by the *other* mechanism the rule provides for, and the
appendix says so of itself explicitly ("It adds no requirement to any actor: a writer
ignoring it is fully conforming"). Nothing downstream treats this appendix as binding.

**Check 2 (citations).**
- "§11.2" for addressed-tile count: opened §11.2 (lines 1639-1650): "The layer's
  **addressed-tile count** — the number of its tile-index entries (§15) — is N for an
  interleaved layer and C · N for a planar layer." Matches "the layout fixes how many
  tile-index entries the layer addresses (§11.2)" — PASS.
- "§14.2" for value arrangement: opened §14.2 (lines 1963-1984): its table gives a
  different "Offset of value k" formula for planar vs. interleaved. Matches "how each
  tile's values are arranged (§14.2)" — PASS.
- "§11.3 states that tile extents are a writer's choice" (unedited context, carried over
  from the pre-repair text): opened §11.3 (lines 1664-1680) — the actual sentence
  ("Tile extents are a writer's choice, and this specification imposes none...") sits
  inside a `> **Note.**` block there too, i.e., non-normative-on-non-normative. Since
  Appendix G itself carries no force either way, this is not a force-mismatch — PASS,
  noted but not a defect (see "also considered" below).
- "item 2's closing sentence names both": opened item 2 in full (lines 4509-4530). Its
  literal last sentence: "...this format fixes no canonical serialization of logical
  content, and two files carrying the same arrays can legitimately differ in **tiling,
  layout**, and codec." Confirmed this is indeed item 2's closing sentence, and it does
  name both tiling and layout (plus codec, covered separately by item 1) — PASS.

**Check 1 (tense/quantifier).** Old text conflated tile-extent and layout's effects under
one blanket clause ("two writers... still emit different numbers of tiles, of different
shapes, without both pinned") — which is imprecise: layout (planar/interleaved) does not
change tile *shape* or spatial tile *count* (N), only the *addressed*-tile count (via the
channel multiplier C·N) and intra-tile byte arrangement. The repair separates the two
mechanisms correctly and specifically, matching §11.2/§14.2's actual quantifiers. This
reads as the defect this repair was written to fix, and it does so precisely — no
new quantifier mismatch introduced.

**Check 6 (unconstrained siblings).** Named the structure: the layer record's
geometry/layout fields (§7.4's table: layout, linearization, dimension entries incl. tile
extent, index_encoding, entry_count). Checked every sibling field for whether it is a
free writer choice needing a pin, or already fixed:
- linearization: `[R-GEO-05]` — only value 1 is legal for writers ("writers MUST NOT emit
  any other value"). Not a free choice; nothing to pin.
- index_encoding: only value 1 (raw-segmented) is legal (§7.4 table). Not a free choice.
- entry_count: `[R-CNT-17]`, derived arithmetically from tile extent + layout (= the
  addressed-tile count already covered).
- channel order / channel count / dimension order: content-derived (part of "the same
  input"/"the same arrays" per item 2's own framing), not writer degrees of freedom the
  same way tile extent/layout are.
No sibling quantity found left ungoverned by this specific sub-clause.

**Check 7 (analogy verbs).** "as item 2's closing sentence names both" is a terminology
pointer, not a warrant-by-analogy in the R-COD-10 sense (it doesn't argue "layout behaves
exactly as tiling does"); item 2's governing verb is "can legitimately differ" (an
existence claim about two conforming files) vs. item 5's "fixes" (a determinism claim about
what happens once the choice is pinned) — different roles, not competing quantifiers over
the same set. No mismatch.

**Check 8 (back-reference).** "Without both pinned, two writers agreeing on everything
above still disagree on bytes" — "everything above" is unchanged wording from the
pre-repair text (items 1-4 plus the earlier part of item 5: codec, file_id, emission
order, one generation, no alignment/slab, fixed filter). Checked item 6, immediately
after the insertion ("The sentinel for every all-fill tile... otherwise two writers
agreeing on content still disagree on bytes") — self-contained, no anaphor pointing back
into the newly-inserted material. No resolution change.

No defect found in hunk 3.

## Step 4 — the three scoping mechanisms

Checked whether any passage touched by these hunks falls under two of {rule-reach,
section-preamble, requirement-deciding-applicability} with different answers:
- Hunk 1's "file, layer or tile" is a *rule-reach* statement (what `[R-ENC-16]` ranges
  over) — I found no section preamble or applicability requirement giving a different
  answer for the same three-way scope split; §2.4's owning-scope enumeration (file, layer,
  tile) is the same three, matching exactly.
- Hunk 2's "detectable" is gated by `[R-CNF-07]` (assigns outcomes to detectable
  violations) and scoped by §21.1's own preamble carve-out (§21.6/§21.7/§21.9 excluded).
  Both apply consistently to the same subject; no conflicting second scoping mechanism
  found.
- Hunk 3 carries no requirement ID and is explicitly outside `[R-CNF-05]`'s core-writer-
  conformance requirement ("adds no requirement to any actor") — it is is deliberately
  outside all three scoping mechanisms, by its own header. Nothing else claims it is bound.

## Step 5 — direction of any disagreement

No disagreement found to adjudicate a direction for.

## Byte-level assessment

No finding survived to the byte-level test. For completeness: had hunk 1's Note and §4.7
disagreed, that would not have been byte-level (the Note is explicitly non-normative,
`[R-ENC-16]`/§4.7 is the operative text — conforming implementations are bound by the
latter regardless of the former's wording). Had Appendix G's item 5 misattributed a
mechanism, that too would not have been byte-level on its own, since Appendix G "adds no
requirement to any actor" — a writer's bytes are unaffected by what the appendix claims;
only a claim inside a §11/§14/§21 normative rule could move emittable bytes or reader
verdicts, and none of the three hunks' edits sit in text whose citations turned out wrong.

## Conclusion

I audited all eight checks against each of the three hunks individually, checked each
hunk's citations by opening the cited section, swept the document for every other
restatement of the terms each hunk uses (structural/descriptive scope; detectable/
unwitnessed; tile extent/layout/addressed-tile-count), and specifically looked for the two
patterns the charter names (a definition and its restatement both edited and now
disagreeing; two repairs bounding the same rule differently). I found:
- Hunk 1's non-normative restatement agrees exactly with the normative §4.7 definition it
  restates (both currently read "file, layer or tile... accepted at all").
- Hunk 2's rewrite is a direct, quantifier-preserving consequence of the untouched
  duality sentence immediately above it, and matches §21.1's "detectable" quantifier
  exactly.
- Hunk 3's rewrite corrects a real pre-existing conflation (tile shape/count vs.
  addressed-tile-count/byte-arrangement) with citations that check out against §11.2 and
  §14.2, and leaves no sibling geometry field ungoverned.
- The three hunks touch three disjoint rule families with no shared vocabulary strong
  enough to collide; I found no pair among them that is jointly inconsistent.

This is a clean result for these three hunks specifically — it says nothing about the
other hunks in this commit (which I did not read, by design, so a different auditor's
pair could still collide).
