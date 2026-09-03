# Repair audit — "the-prose-repairs" (hunks 01, 02, 05, 06)

## Access disclosure

Read: the four hunk files named in my charter
(case/hunk-01.diff, case/hunk-02.diff, case/hunk-05.diff, case/hunk-06.diff),
and spec/tarn.md (multiple ranges, via offset/limit reads and rg). I did not
read full.diff, other hunk files, docs/, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, README.md, conformance/, spec/registry.json, or git history/log/
diff, and did not list the case/ directory.

**Contamination notice.** Before I did any work, my context already
contained a large amount of material I did not ask for: a full project
CLAUDE.md/AGENTS.md pointer, and — critically — a user memory index
(`MEMORY.md`) listing entries such as "Naming constraint on published
rationale", "TARN working cadence", "Workflow verifier failures", "Spec
edits need propagation checks", and "TARN register is the corpus build
list". I did not open any of the linked memory files and did not act on
their contents; I am naming their titles here only because the access rule
requires me to disclose that this material appeared, not to import it as
evidence. None of my findings below rest on anything from that index — every
claim I make is derived from spec/tarn.md and the hunk files, with a
specific line-quoted citation.

Working file written: scratch/the-prose-repairs/notes.md (arithmetic
scratch notes only, no other file touched).

## Setup: R-CNF-01 and the label rule

`[R-CNF-01]` (spec line 104-106): "All text in this document is normative
except: §1 (Introduction); any text labeled *Note*, *Example*, or
*Rationale*; and appendices identified as non-normative."

Applying this to each hunk's landing site:

- **Hunk 01** lands at spec lines 2607-2616, inside §18.2 "Encoding". I read
  the whole subsection (2576-2660): there is no ">" blockquote anywhere in
  this stretch — it is plain paragraph prose. **Normative.**
- **Hunk 02** lands at spec lines 3168-3173, inside §20.3's numbered step 4
  ("An appender MUST, in order: ... 4. Write payloads and indexes"). No ">"
  marker anywhere in this list item. **Normative.**
- **Hunk 05** and **Hunk 06** both land inside the same block: spec lines
  3925-4001, which opens `> **Rationale.**` (line 3925) and runs
  continuously (every line prefixed ">") through line 4001, immediately
  before "#### 21.8 Conformance vector coverage" at line 4003. I read the
  entire block start to finish. Per R-CNF-01's explicit label list,
  **this is non-normative** — checked by the label ("Rationale."), not by
  the presence of ">", per the charter's instruction. I verified this isn't
  an unlabeled blockquote (which would be normative) by reading the actual
  first word after ">" at line 3925: `**Rationale.**`.

This matters directly for the byte-level test on hunks 05/06 below: nothing
in them can move an accept/reject verdict or an emittable byte set, because
R-CNF-01 already voids their normative force. The text at lines 3925-3930
itself says as much and hunk 05 sharpens that statement (see below).

## Hunk 01

### The rule it adopts

Before: "Two of those carry no witness a file exhibits, and R4 registers
neither: dictionary use the header does not disclose is a writer violation
nothing in the extent shows, exactly as `[R-COD-06]` has it for a tile
(§21.7), and the bar on sizing a buffer binds a reader rather than the
document."

After: "Two of those fall outside the register, on the two distinct grounds
§21.7 separates, and R4 registers neither: dictionary use the header does
not disclose is a writer violation nothing in the extent shows — an
unwitnessed condition, exactly as `[R-COD-06]` has it for a tile (§21.7) —
while the bar on sizing a buffer binds a reader rather than the document,
and so states no condition a file can exhibit at all."

What it makes true of an implementation: nothing new operationally (no
reader/writer/verifier obligation changes) — this is explanatory prose
classifying, for two items in the §18.2 carried-over RFC 8878 constraint
list, *why* each is absent from register row R4. It asserts that these two
items are absent for **two different reasons** — (a) unwitnessed
(undetectable but a real file state) vs (b) not even a condition a file can
exhibit — rather than lumping both under one undifferentiated "carries no
witness" label as the pre-repair text did.

### Check 1 — tense and quantifier

"Two of those" ranges over the carried-over list at lines 2606-2609 (frame
magic; no skippable/second frame; no dictionary use/no nonzero dictionary
ID; no content-checksum flag; the buffer-sizing bar) — same quantifier as
before the repair (unchanged by the hunk). No tense shift: both halves of
the repaired sentence describe the current, in-force prohibition, matching
`[R-COD-06]`'s present-tense "Writers MUST NOT ... MUST NOT" (line 2411-2413,
2419-2422).

### Check 2 — citations resolve

- `` `[R-COD-06]` `` (twice, one via the hunk's insertion at line 2602 unchanged,
  one inside the hunk at line 2614): opened at spec lines 2405-2432. Verified
  line 2411-2419: "Writers MUST NOT compress a tile using a dictionary —
  whether or not the header discloses one ... Dictionary use the header does
  not disclose is not detectable by inspection and need not decode to an
  error: it is a writer violation whose consequence is wrong decoded
  content, the same undetectable class as any other writer that emits wrong
  bytes (§21)." This matches the hunk's claim exactly — PASS.
  Also verified line 2426-2427: "a reader MUST NOT allocate or size any
  buffer from it — the decoded size comes from the layer's declarations
  alone" — a rule that binds the **reader**, not a condition of the file.
  Matches the hunk's claim that "the bar on sizing a buffer binds a reader
  rather than the document" — PASS.
- §21.7 (cited twice): opened lines 3868-4001. Verified the "two distinct
  grounds": (1) **unwitnessed** condition, defined lines 3886-3898 ("A
  condition this specification names is unwitnessed where, for every file
  exhibiting it, some file that does not exhibit it cannot be told apart
  from it by any check this specification obliges..."); (2) a requirement
  that "states no condition a file can exhibit" — defined at line 3917-3923
  as an explicit contrast to (1): "Distinguish an unwitnessed condition from
  a requirement that states **no condition a file can exhibit**." Both
  grounds do exist and are "the two ... §21.7 separates" — PASS.

### Check 3 — normative label

Already covered above: hunk 01 sits in plain, unlabeled prose in §18.2 — no
blockquote at all — so it is normative text and the repair lands with force.

### Check 4 — contradiction in the passage

Read the whole surrounding paragraph (2595-2660). No carve-out or MUST
elsewhere in this paragraph is loosened or tightened by the reclassification
— the repair only renames *why* the two items are absent from R4, it does
not change which items are absent, does not touch R4's own definition (line
3806, unchanged, outside this hunk), and does not touch `[R-COD-06]` itself.
No contradiction found.

### Check 5 — exhaustive claims

"Two of those" — verified by direct count against the carried-over list's
constituent constraints and against R4's Instances column (line 3806):
magic ✓ registered ("missing frame magic"), skippable frame ✓ registered,
second frame ✓ registered, checksum flag ✓ registered ("the content-checksum
flag set"), nonzero dictionary ID ✓ registered ("a nonzero dictionary ID").
Not registered: dictionary-use-undisclosed, and the buffer-sizing bar — an
exact count of **two**. The claim "Two of those fall outside the register"
is exactly right, not an overclaim. PASS.

### Check 6 — what else is left unconstrained

The structure here is the carried-over constraint list (5 semicolon-joined
items, one of which bundles two related dictionary constraints). I checked
every constituent against R4's Instances column (above) and found all
non-flagged constituents are in fact registered. Nothing is left dangling.

### Check 7 — analogy comparison

"exactly as `[R-COD-06]` has it for a tile (§21.7)" — repair's governing verb:
"is a writer violation nothing in the extent shows — an unwitnessed
condition." Cited rule's governing language (line 2415-2418): "is not
detectable by inspection and need not decode to an error: it is a writer
violation whose consequence is wrong decoded content, the same undetectable
class..." Both range over the same subject (undisclosed-dictionary-use) at
the same granularity (one instance: a document extent vs a tile extent,
both governed by the same underlying RFC 8878-derived rule, applied via
§18.2's "under every frame constraint `[R-COD-06]` places on a frame ...
carried over"). The verbs align: "unwitnessed" (§21.7's term) vs
"not detectable ... undetectable class" (R-COD-06's term) — synonymous as
used in this document. PASS, analogy sound.

### Check 8 — back-references

- "Two of those": antecedent = the carried-over list at 2606-2609, unaffected
  by the hunk (same wording before and after).
- "R4": antecedent = register row R4, defined at line 3806, well outside this
  hunk and unaffected.
- "The first exception" (line 2617, immediately following the hunk, NOT part
  of the hunk's changed lines): I checked whether the hunk's insertion could
  have shifted this back-reference's target. The word "exception" is
  introduced earlier at lines 2603-2605: "under every frame constraint
  `[R-COD-06]` places on a frame, named here or not, save two: what it
  states against a tile's declared decoded size, and what it states about
  the frame's declared `Window_Size`. This section replaces both, below."
  This is the only place before "The first exception" that the word
  "exception" (or its concept, "save two") occurs. The hunk's own sentence
  never uses "exception" — it uses "fall outside the register" / "grounds" —
  distinct vocabulary. So "the first exception" still resolves to "what it
  states against a tile's declared decoded size" (confirmed also by the
  next sentence, "The frame's declared `Window_Size` is unconstrained here
  for the same reason" = the *second* exception). This ambiguity risk
  (two different "two"s in close proximity) pre-dates the repair — the old
  text also read "Two of those carry no witness..." right before "The first
  exception" — so the hunk did not introduce or worsen it. **Unaffected.**

### Verdict — Hunk 01

Correct, well-targeted repair. It replaces a vague, partly-inaccurate
label ("carries no witness a file exhibits" — literally a category error for
the buffer-sizing bar, since that rule isn't about a file exhibiting
anything) with the two precise §21.7 grounds, cites them correctly, and
every checked citation and back-reference holds. No findings.

**Byte-level:** N/A (no defect found).

---

## Hunk 02

### The rule it adopts

Before: "...re-emitting those tiles would strand the originals as slack —
the whole layer's worth, since `[R-LIF-01]` freezes them where they lie —
leaving the file larger..."

After: "...would strand the originals as slack — every tile the change
reaches, and for a change reaching every channel the whole layer's worth,
since `[R-LIF-01]` freezes them where they lie — leaving the file larger..."

Rule adopted: the amount of slack a barred re-typing produces is, in
general, exactly the set of tiles the change reaches (not, as the old text
unconditionally claimed, always "the whole layer's worth"), with "the whole
layer's worth" singled out as the amount specifically **when the change
reaches every channel**.

### Check 1 — tense/quantifier

Tense: "originals" = the prior generation's stored tiles (superseded
generation), consistent with the governing §14 bar's own tense ("in the
generation this commit supersedes", line 3137, 3204). "every tile the
change reaches" ranges over the same set the governing rule's own test uses
("wherever the layer stores a tile that carries that channel", line
3156-3157). No tense or quantifier drift versus the governing rule.

### Check 2 — citations

`` `[R-LIF-01]` ``: opened at spec lines 1224-1232, §9.1 Committed-prefix
immutability: "Bytes in [0, F) ... are immutable: a writer MUST NOT modify
them..." Matches "freezes them where they lie" — PASS.

### Check 3 — normative label

Plain prose inside step 4 of "An appender MUST, in order:" (§20.3) — no
blockquote. **Normative.**

### Check 4 — contradiction with the paragraph

The instructed check: "does the sentence still agree with the paragraph
that precedes it, which it did not before this repair." I read the whole
paragraph (lines 3156-3176). It explicitly allows a **partial** effect:
"Where the superseded generation stored no tile carrying that channel there
is nothing to reinterpret, and this bars nothing: re-typing a channel of a
layer that stores nothing, **or a planar channel none of whose own tiles
are stored**, is a declaration edit like any other." This sentence
presupposes that a single planar channel's tiles are a distinguishable
subset of the layer's tiles — i.e., that a change CAN reach less than the
whole layer. The pre-repair text's unconditional "the whole layer's worth"
directly contradicted this: a re-typing of one populated planar channel
(out of several) would, per the old wording, strand "the whole layer's
worth" even though the preceding sentence's own framework treats a single
channel's tiles as a distinguishable, narrower set. The repair resolves
this — confirmed disagreement existed before, confirmed it's gone now for
the general clause.

### Check 5 — exhaustive claims / Check 6 — what's left unconstrained

I derived the arithmetic for the four layer shapes below, using: line 1637
("[addressed-tile count] is N for an interleaved layer and C · N for a
planar layer"); line 3156-3157 ("changing it is such a change wherever the
layer stores a tile that carries that channel"); and the passage's own
established planar/interleaved distinction (line 3166-3168: "re-typing a
channel of a layer that stores nothing, or **a planar channel** none of
whose own tiles are stored").

1. **Change reaches every channel** (retypes every channel of the layer,
   any layout): every tile of the layer carries some changed channel, so
   "every tile the change reaches" = every addressed tile = "the whole
   layer's worth." Repair's specific clause: TRUE.
2. **Change reaches a single planar channel**: for a planar layer, each
   channel's N tiles are a disjoint block (disk ordinal c·N+s, line
   3191-3193) — a single channel's tiles are only that channel's own N
   tiles, not C·N. General clause ("every tile the change reaches") =
   correctly just that channel's N tiles; the specific "every channel"
   clause does NOT fire (correctly, since not every channel was reached).
   No false claim.
3. **Change reaches nothing** (no tile of the superseded generation carries
   the changed channel): the whole sentence is gated by "Where a change does
   reach them" (line 3168) — this case is excluded from the sentence
   entirely (covered instead by "this bars nothing" two sentences earlier).
   Vacuous, no claim made, consistent.
4. **Change reaches a single channel of an INTERLEAVED layer** (a shape the
   charter's three examples don't explicitly list, but the paragraph's own
   framework requires considering it, since it explicitly discusses both
   layouts): for an interleaved layer, addressed-tile count is **N**, not
   C·N (line 1637), because every interleaved tile packs every channel's
   samples into one blob per spatial position — there is no "single
   channel's own tiles" the way there is for planar (this is exactly why
   the preceding paragraph's disjunction singles out "**a planar** channel"
   specifically, line 3167, and not "a channel" generically). So retyping
   even ONE channel of an interleaved layer already makes "the layer stores
   a tile that carries that channel" true for **every** one of the layer's N
   tiles — i.e. "every tile the change reaches" already equals "the whole
   layer's worth", without any need to retype "every channel."

Case 4 shows the added specific clause ("and for a change reaching every
channel the whole layer's worth") is **true but incomplete**: it presents
"a change reaching every channel" as the (implicitly sole) named route to
"the whole layer's worth," and omits the interleaved single-channel route
that the same paragraph's own planar/interleaved framework makes available
just two sentences earlier. A reader relying on the specific clause alone
(rather than working the general clause through for interleaved layouts
themselves) could conclude that a single-channel re-typing of an
interleaved layer strands less than the whole layer — which is false. The
general clause ("every tile the change reaches") is fully correct on its
own and does cover case 4 correctly if worked through; the specific clause
is additive commentary, not a logical error, but it creates exactly the
kind of new ambiguity the charter's check on Hunk 02 was fishing for.

I flag this as B-01 below.

### Check 7 — analogy

No "exactly as" / "the same way" / "transposed from" language appears in
the changed text of this hunk. Nothing to check here.

### Check 8 — back-references

No new sentence was inserted between two existing sentences; the hunk
extends the same sentence (adds a semicolon-joined clause before the
existing "since `[R-LIF-01]` freezes them where they lie" continuation).
The following sentence ("leaving the file larger for a change that reads
like a directory edit") and the one after ("Such a change is a new layer,
or a whole-file rewrite under a fresh file_id") both use "such a change" /
implicit "this" pointing at the same referent (a §14-bar-violating
re-typing) as before the repair — unaffected, since no sentence boundary
was added before them.

I also checked "the whole layer's worth" and "strand[ed]"/"stranding" for a
restatement elsewhere that the repair should have swept: `grep -n "whole
layer" spec/tarn.md` → exactly one hit (this hunk's own line 3172). `grep -n
"strand\|stranded"` → hits at 3171 (this hunk), 3223, 3252 (both about a
shrink stranding "a large share of a layer's stored bytes" — a different,
vaguer quantity, not "the whole layer's worth", not affected by this
repair), 3373, 4218, 4220 (unrelated appender/updater contexts). No
restatement of the specific "whole layer's worth" claim exists elsewhere
that needed sweeping.

### Verdict — Hunk 02

The repair correctly fixes the pre-existing overclaim (unconditional "whole
layer's worth") and is true for every case the charter's three named shapes
cover. It leaves a real but narrower gap: the added specific clause singles
out "a change reaching every channel" as *the* named route to "the whole
layer's worth" without acknowledging that an interleaved layer reaches that
same amount from a single-channel change, given the paragraph's own
established layout framework two sentences earlier. Reportable as
NEW_AMBIGUITY, not as a false statement (the general clause remains
correct and sufficient on its own).

**Byte-level:** No. This whole passage is descriptive commentary explaining
a consequence (file growth from stranded slack) of the actual normative
rule, which is the unconditional §14-bar MUST NOT stated earlier (line
3135-3143) and is untouched by this hunk. Fixing or not fixing the
"whole layer's worth" clause changes no reader/writer/verifier accept-reject
behavior and no emittable byte set.

---

## Hunk 05

### The rule it adopts

Before: "The obligations this test places outside the register, as the
document stands. This walk-through illustrates the test and does not
extend it; where an item here and the test above disagree, the test
governs, and an item found stale is a defect in this block and not in the
register."

After: "Obligations this test places outside the register, as the document
stands. This walk-through illustrates the test and does not extend it, and
its list is not offered as closed; where an item here and the test above
disagree, the test governs, and an item found stale — or an obligation the
list omits — is a defect in this block and not in the register."

Rule adopted: the walk-through's list of illustrative omitted-obligation
examples is explicitly **not** offered as closed/complete, and an omission
from that list (not just a stale item already in it) is likewise "a defect
in this block and not in the register."

### Check 3 — normative label

This whole block is `> **Rationale.**` (line 3925) — **non-normative** per
R-CNF-01. So by definition this hunk cannot itself create or remove a
requirement; its only possible defect class is editorial/self-consistency
within the walkthrough, or a failure to align with the actual (normative)
test defined at lines 3886-3923 just above the blockquote.

### Check 4/6 — does anything else rely on this list being complete?

I opened §21.1 (lines 3548-3625) — the register's own completeness clause.
Line 3581-3584: "The subsections after §21.5 are not part of the register
and carry no rows: neither this completeness clause nor the instance
arithmetic below reaches §21.6's defined non-violations, **§21.7's test for
what no check detects**, or §21.9's limits." This explicitly excludes
§21.7 (the whole section, walkthrough included) from §21.1's completeness
clause. So nothing elsewhere in the document treats this Rationale
walkthrough's list as authoritative or complete — the hunk's added
disclaimer is consistent with, and simply makes explicit, what §21.1
already establishes structurally. No conflict.

I also checked the established idiom "list is not offered as closed" /
"not offered as exhaustive" for consistency: `grep -n "not offered as
closed"` → 3 hits: line 3580 (§21.1, about the strict-specialization
pairs list), line 3927 (this hunk), line 4232 (§20-adjacent, about a list
of operations). `grep -n "list is not offered as"` → adds line 3214 ("the
list is not offered as exhaustive", §20.3). The hunk's phrasing matches
this document's own established idiom for flagging a non-exhaustive
illustrative list — stylistically and substantively consistent.

### Check 8 — back-references

Checked "these obligations" (plural), the opening noun phrase of the next
paragraph (line 3932: "Beyond the content-wrongness this section opens
with, these obligations are omitted from the register because..."). The
hunk inserted a singular "an obligation the list omits" clause just before
this. Since "these obligations" is plural, and the nearest plural
antecedent is the opening "Obligations this test places outside the
register" (the very first words of the Rationale block, also plural), the
inserted singular clause does not compete grammatically for this
antecedent. Checked and unaffected.

### Verdict — Hunk 05

Sits in a labeled non-normative block, correctly. It removes an implicit
completeness claim from a list whose completeness §21.1 already explicitly
disclaims for this whole section, so it does not conflict with anything and
matches the document's established idiom. No findings.

**Byte-level:** N/A (non-normative block; no defect found).

---

## Hunk 06

### The rule it adopts

Before: "...a permutation among channels whose planes are the same length
and whose recorded fills agree disturbs nothing a row can see, while one
that leaves a plane of one length at an ordinal the new declarations size
differently is caught by T3, or by T14 under codec 1. Where the fills
differ, §14.5's padding positions and §14.3's pad bits carry the wrong
channel's fill and T4 or T5 sees it. Where the change does touch something
§14 fixes, the register's rows reach it on the terms they state there and
no better."

After: "...Where the fills differ **and the layer has a padding position or
a pad bit**, §14.5's padding positions and §14.3's pad bits carry the wrong
channel's fill and T4 or T5 sees it; **where it has neither, the
permutation is unwitnessed whether the fills agree or not.** Where the
change does touch something §14 fixes..."

Rule adopted: a disk-ordinal permutation among same-length, differing-fill
channels is witnessed by T4/T5 only **conditionally** — specifically, "where
the layer has a padding position or a pad bit" — and is unconditionally
unwitnessed otherwise, regardless of whether the fills agree or differ.

### Check 3 — normative label

Same Rationale block as hunk 05 (lines 3925-4001). **Non-normative.**

### Deriving the condition from the rules that create T4 and T5

I opened both witnesses' register rows (lines 3756-3757):
- T4: "A padding position does not encode, for each channel it carries,
  that channel's recorded fill value" — reader-tier certification, governed
  by `[R-SER-05]`.
- T5: "In a packed planar bool plane with P mod 8 ≠ 0, a final-byte pad bit
  ... is not the channel's fill bit" — governed by `[R-SER-05]` (R-SER-03).

I then derived, from first principles in the spec, what determines whether
"the layer has a padding position or a pad bit" **for the specific channels
being permuted**, versus for the layer as a whole:

- **Padding positions** are geometric, not per-channel: §11.1 (line
  1589-1591) declares a layer's dimensions — extent Eᵢ and tile extent Tᵢ —
  **once per layer**, not per channel; §11.3 (line 1655-1665) derives
  padding positions from "Eᵢ mod Tᵢ ≠ 0", i.e. from that single shared grid.
  So if a layer has padding positions at all, **every** channel's tiles at
  the grid's high edge have them, at the same spatial positions — this
  disjunct is genuinely layer-wide-equals-channel-wide, no gap here.
- **Pad bits** are not geometric in the same sense — they exist only for a
  channel declared **bool**, stored **planar**, **packed**, with P mod 8 ≠
  0 (§14.3, line 2020-2028, and T5's own row text above). §14.4 (line
  2060-2065) states explicitly: "planar layers carry any mix of channel
  types, each channel's plane serializing under §14.2 or §14.3 **by its
  type alone**" — confirming a single planar layer can freely mix bool and
  non-bool channels, and each channel's own type alone decides whether it
  gets pad bits.

**Counterexample.** Take a planar layer with channels `r` (uint8), `g`
(uint8), and `mask` (bool), grid geometry with no overhang (Eᵢ mod Tᵢ = 0 for
every dimension, so **zero** padding positions anywhere in the layer for any
channel), and P mod 8 ≠ 0 so `mask` has pad bits. A commit permutes `r` and
`g` (same plane length P·1 byte each, differing recorded fills). Per T4/T5's
own definitions: `r` and `g` have no padding positions (no grid overhang)
and no pad bits (not bool) — the permutation is unwitnessed for them. But
"the layer has ... a pad bit" is **true**, purely because of `mask`, which is
not involved in the permutation and whose own ordinal did not move. Read
literally, the hunk's sentence — "Where the fills differ and the layer has
a padding position or a pad bit, §14.5's padding positions and §14.3's pad
bits carry the wrong channel's fill and T4 or T5 sees it" — asserts
detection here, but T4/T5 do not in fact see this permutation: the
condition as stated (layer-wide "has... a pad bit") is not the right
quantifier. The correct condition is "the *permuted channels themselves*
have a padding position or a pad bit" for the pad-bit disjunct (the
padding-position disjunct is safe, since it is genuinely layer-uniform, as
derived above).

I checked this reading of "the layer has..." against the document's own
established idiom for the identical phrase: line 3324 (§20.4(c)) uses "a
layer with no padding position and no pad bit" in an explicitly **global**
sense (a layer where structurally *no* channel anywhere has either) to
license an appender's directory-only edit. That precedent supports reading
hunk 06's "the layer has a padding position or a pad bit" the same way —
layer-wide, not channel-specific — which is exactly the reading that
produces the gap above.

I flag this as B-02 below.

### Check 4 — consistency with the item's other limbs

Re-checked the two limbs the hunk did not touch:
- "fills agree" limb: unconditioned on padding/pad-bit existence at all —
  correctly so, since if the two channels' recorded fills are equal, any
  padding/pad-bit bytes match the (shared) fill regardless of which channel
  nominally owns the ordinal post-permutation. No interaction with the gap
  above; consistent.
- "different plane length" limb (caught by T3/T14): governed by declared vs.
  stored length per channel, independent of padding/pad-bit existence;
  unaffected by and consistent with the hunk.

Only the "fills differ" limb, which the hunk edited, carries the gap
identified above.

### Check 2 — citations

§14.5 → opened, "Padding content" (line 2087+), matches "padding positions."
§14.3 → opened, "Packed boolean planes" (line 2020+), matches "pad bits."
Both citations resolve correctly to the sections they claim — PASS
(the mapping itself is right; the gap found is in the *condition*
gating them, not in the citations).

### Check 8 — back-references

The insertion ("where it has neither, the permutation is unwitnessed
whether the fills agree or not") is joined by a semicolon into the *same*
sentence as the "Where the fills differ..." clause — it does not insert a
new sentence between that clause and the following one ("Where the change
does touch something §14 fixes, the register's rows reach it on the terms
they state there and no better."). I checked "the change" in that following
sentence: before the hunk its nearest antecedent was the fills-differ
clause (part of the same permutation discussion); after the hunk, the
nearest antecedent is still the (extended) same clause, since no sentence
boundary was added ahead of it. **Unaffected.**

### Verdict — Hunk 06

Correctly adds a genuinely-needed condition (the old unconditional "Where
the fills differ ... T4 or T5 sees it" was itself an overclaim, since a
layer entirely free of padding positions and pad bits exists and is
explicitly discussed elsewhere in the document, line 3324) and correctly
adds the "otherwise unwitnessed" residue clause. But the condition it
supplies — "the layer has a padding position or a pad bit" — is
under-specified for the pad-bit disjunct: it should be scoped to the
permuted channels themselves rather than the layer as a whole, because pad
bits (unlike padding positions) are not layer-uniform in a mixed-type
planar layer, which §14.4 explicitly permits. This is the same shape the
charter warns about under check 6: one member of the disjunction (padding
position) is correctly layer-uniform, but its sibling (pad bit) is not, and
the repair states one quantifier for both.

**Byte-level:** No. This whole passage is inside the R-CNF-01-labeled
`Rationale.` block, so per R-CNF-01 it carries no normative force — no
accept/reject verdict or emittable byte set turns on it. §21.7's own text
just above the blockquote (lines 3925-3930, as sharpened by hunk 05) already
says an error found here is "a defect in this block and not in the
register." The genuinely normative rule this walkthrough illustrates — the
planar-disk-ordinal "companion bar" MUST NOT at lines 3182-3189 — is
untouched and unambiguous regardless of this gap.

---

## Sweeps run (verbatim, with hit counts)

- `grep -n "R-CNF-01"` → 1 hit (line 106; definition).
- `grep -n "^#### 21.7\|^### 21\b\|^## 21\b"` → 2 hits (3546, 3868).
- `grep -n "R-COD-06"` → 9 hits (2432, 2602, 2614, 2629, 2647, 3765, 3769-3774 rows, 3806, 3874, 4118) — enumerated and checked the relevant ones above.
- `grep -n '\bR4\b'` → 3 hits (2611, 2643, 2645) plus the R4 row itself at 3805-3806 found via context read.
- `grep -n "R-LIF-01"` → 10 hits; opened definition (1224-1232) and the hunk-02 usage (3173).
- `grep -n "sizing.*buffer\|buffer.*siz"` → 3 hits (2427, 2609, 2615).
- `grep -n "interleaved layer\|planar layer\|storage layout"` (plus manual reads of §11.1-§11.4, §14.3-§14.5) → used to derive addressed-tile-count formulas and mixed-type-layer permission.
- `grep -n "whole layer"` → 1 hit (3172, the hunk itself) — no restatement elsewhere to sweep.
- `grep -n "strand\|stranded"` → 5 hits (3171, 3223, 3252, 3373, 4218/4220) — checked each, none restate "whole layer's worth."
- `grep -n "not offered as closed"` → 3 hits (3580, 3927, 4232) — confirms hunk 05's phrase matches established document idiom.
- `grep -n "list is not offered as"` → 4 hits (adds 3214) — same idiom family.
- `grep -n "padding position or a pad bit"` → 1 hit (3961, the hunk itself).
- `grep -c "unwitnessed"` → 9; `grep -n "unwitnessed"` → listed and spot-checked each occurrence for consistency with the definition at 3886-3898.
- `grep -n "21\.7"` → 8 hits, all opened/checked for any place that might treat the §21.7 walkthrough as authoritative elsewhere (none do, besides §21.1's explicit exclusion at 3581-3584).
- `grep -n "d dimension entries\|d dimension\|tile extent\|extent Eᵢ"` and manual read of §11.1 (1589-1594) and §11.3 (1655-1665) → confirmed grid geometry (hence padding positions) is declared once per layer, shared by all channels.
- `grep -n "C channel entries\|channel entry\|heterogene..."` and manual read of §7.4 (line 1086) and §14.4 (2058-2085) → confirmed each channel has its own independently-declared type, and planar layers may freely mix bool and non-bool channels.
- `wc -l spec/tarn.md` → 4775 (document length, for orientation).

## Derived numbers

- R4's Instances column (line 3806): enumerated 16 semicolon-separated
  instances, confirmed the two omitted concepts (dictionary-use-undisclosed;
  buffer-sizing bar) are not among them, while all five other carried-over
  constraints are — matches hunk 01's "Two of those" exactly (2 of 7
  constituent sub-items, counting the bundled dictionary clause as two).
- Addressed-tile-count formulas (line 1637): N (interleaved) vs C·N
  (planar) — used to derive hunk 02's case 4 (interleaved single-channel
  change reaches all N tiles).
- No numeric miscount found in hunk 05 or hunk 06 beyond the pad-bit
  quantifier scoping issue in hunk 06 (which is a scope/quantifier gap, not
  an arithmetic miscount as such).

## Rejected candidates

1. Whether hunk 01's forward citation to §21.7 (defined later in the
   document than §18.2) is itself a defect — rejected: forward references to
   later sections are used throughout this document (e.g. hunk 01's own
   context already cites §21.7 at line 2521, well before §21 itself), so
   this is normal, established style, not a defect.
2. Whether hunk 01's "the first exception" could have been pulled toward the
   hunk's own "two ... grounds" language by proximity (check 8) — rejected
   after confirming the word "exception" appears nowhere in the hunk's
   vocabulary and the pre-repair text had the identical proximity risk
   (unaffected by this repair specifically).
3. Whether hunk 02's phrase "a change reaching every channel" might already
   (by an alternate reading, where "reach" means "affect the storage of"
   rather than "retype the declaration of") correctly and elegantly cover
   the interleaved case too — considered seriously, but rejected as the less
   natural reading given the paragraph's established usage: "changing it is
   such a change" (line 3156-3157) ties "reaching a channel" to the act of
   retyping that channel's declaration, not to the downstream effect on
   tiles (which is what "every tile the change reaches" already covers,
   using "reach" with tiles, not channels, as its object). Kept as B-01
   under the more natural reading, but noted the alternate reading in the
   writeup for balance.
4. Whether hunk 05's plural/singular shift ("these obligations" vs. the
   hunk's inserted singular "an obligation the list omits") created a
   back-reference collision — rejected after confirming number agreement
   (plural "these obligations" cannot naturally bind to the singular
   inserted phrase; it binds to the paragraph-opening plural "Obligations").
5. Whether hunk 06's "the layer has ... a pad bit" gap could be closed by
   the padding-position disjunct alone in every realistic case (i.e.,
   whether a layer can really have a pad bit-bearing channel but zero
   overhang) — checked directly: overhang (Eᵢ mod Tᵢ ≠ 0) and pad bits
   (P mod 8 ≠ 0, itself derived from tile extents alone, no relation to
   extent-vs-tile-extent divisibility) are governed by unrelated
   quantities, so a layer with zero overhang and P mod 8 ≠ 0 is a normal,
   unremarkable geometry — not rejected, this became the basis for B-02.
6. Whether hunk 06's counterexample requires an unusual/prohibited layer
   shape (mixed bool/non-bool channels in one planar layer) — checked
   directly against §14.4 (line 2060-2065), which explicitly permits and
   names this ("planar layers carry any mix of channel types") — not
   rejected, confirms the counterexample is a normal conforming layer.

## Confidence / where little was found

Hunks 01 and 05 passed all eight checks with no findings; for both I traced
every citation to its source, re-derived the classification claims from
the sections they cite (§21.7's two grounds for hunk 01; §21.1's explicit
exclusion of §21.7 from the completeness clause for hunk 05), checked
established-idiom consistency via grep, and specifically hunted for the
back-reference and contradiction failure modes the charter warns about
(same technique that produced findings for hunks 02 and 06) — they simply
did not turn anything up. What would have found something, had it been
there: a citation that didn't say what's claimed (none did); a restatement
elsewhere in the document that disagreed (none found, via targeted greps);
a plural/singular or nearest-antecedent shift on a back-reference (checked
explicitly, none shifted).
