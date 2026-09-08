# Audit transcript — lane "the-glosses" — hunks 06, 17, 18, 23

## Disclosure

Read exactly: `spec/tarn.md` (via Read tool, multiple ranges: 1900-2000,
1609-1729, 3121-3461, 3460-3600, 3644-3971 (register section headers +
§21.6), 4130-4230, 4795-4820) and the four charter hunk files
(`hunk-06.diff`, `hunk-17.diff`, `hunk-18.diff`, `hunk-23.diff`) under
`/private/tmp/.../r32-audit/case/`. Did not read `full.diff`, other
hunk files, docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md,
conformance/, spec/registry.json, or git history/log/diff, and did not
list the case/ directory beyond the four named files.

Ran `Bash`/`python3` only for local grep/search computation against
`spec/tarn.md` (no other files read by those scripts) and to write this
transcript plus nothing else, under
`/private/tmp/.../r32-audit/scratch/the-glosses/` — actually no scratch
file was needed; all searches were run inline via `python3 -` heredocs
that read only `spec/tarn.md` and wrote no files. Only output file
written is this transcript itself, at the path the charter specifies.

**Contamination note.** My context included a project CLAUDE.md/AGENTS.md
pointer, a user MEMORY.md index (with entries like "TARN repair prose vs
rules", "TARN repair list vs diff", "TARN harness vs charter" etc.), a
git status block naming recent commit subjects ("Cleanroom round 31:
charter", "ADR-0122...", "ADR-0121...", "ADR-0120..."), and later a
system-reminder that the date advanced mid-session. None of this was
read as part of my two-file access, none of it names any defect or
answer for these four hunks specifically, and I did not use any of it to
reach a conclusion below — every finding here traces to a passage I
quote from `spec/tarn.md` itself or the hunk files. Flagging per the
disclosure requirement.

---

## Hunk 06 — §13.3's "Note — sparse writing" (lines ~1949-1956)

### The hunk

```
-> layer's stored-tile set, or that grows its extents so that
-> entry_count changes, re-emits that layer's whole tile-index region
-> (§11.1, §20.3, `[R-WRT-04]`).
+> layer's stored-tile set or its index content — a growth, a shrink or
+> a channel removal that changes entry_count among them — re-emits
+> that layer's whole tile-index region (§11.1, §20.3, `[R-WRT-04]`).
```

Header claims landing lines 1954-1956, nearest preceding heading "13.3
Unstored tiles read as fill" (line 1911). Confirmed against the body:
read spec lines 1900-1958; the Note sits at 1949-1956, immediately
before "### 14. Tile Serialization" at 1958, and is headed
`> **Note — sparse writing.**` (line 1949) — a labelled Note block.
Header claim matches.

### Label / force (check 3)

`> **Note — sparse writing.**` — labelled Note. Per `[R-CNF-01]`
(§1 exempts, plus Note/Example/Rationale-labelled blocks), this whole
block is **non-normative**. Confirmed the ">" marker is not the test —
this is a labelled block, so the marker is irrelevant either way; the
label itself settles it.

### The rule the repair adopts

Old rule (paraphrase): "a commit that changes the stored-tile set, OR
that grows extents so entry_count changes, re-emits the whole
tile-index region." This is under-inclusive: it omits shrinks and
channel removals as index-content-changing/re-emission triggers, both
of which §20.3's normative text documents.

New rule (paraphrase, as I read it distributively): "a commit that
changes the stored-tile set, or that changes index content — where
'changes index content' is illustrated by: a growth, a shrink, or a
channel removal, in each case *only when* it changes entry_count —
re-emits the whole tile-index region."

### Check 1 (tense/quantifier) — governing citations

Opened §11.1's Rationale (lines 1629-1664, non-normative, labelled
`> **Rationale.**`):

> "Growth that leaves **entry_count** unchanged touches the directory
> alone — a growth raising one grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) while
> another stays 0 among them, the product holding at 0. Growth that
> changes entry_count changes extent_length with it (`[R-CNT-17]`), so
> the layer's whole tile-index region is re-emitted..."

This is an explicit two-way split for growth alone: entry_count
unchanged → directory only; entry_count changed → full re-emission.
A growth that leaves entry_count unchanged is **not** limited to the
"one dimension stays 0" example given — I verified this against
§11.2's grid formula: a layer with extent (900, 2048), tile (256, 256)
has G_y = ⌈900/256⌉ = 4; growing to (1000, 2048) keeps G_y = 4 (since
⌈1000/256⌉ = 4 too), so N and hence entry_count are unchanged even
though no dimension is at extent 0. §20.3's own growth paragraph
confirms growth is generally "free" this way: "a position that becomes
real held that channel's fill... this is an exception §20.3's
permission states" — no requirement that grid count change.

Opened §20.3 step 4 (lines 3166-3179, normative, not in a blockquote):

> "Every layer whose stored-tile set or index content this commit
> changes has its tile-index region re-emitted in full..."

This is the actual normative trigger, phrased as "index content...
changes," not "entry_count changes" — a growth that changes neither
the stored-tile set nor index content (because grid count, hence every
entry, is unchanged) correctly falls outside this normative rule too.

**Now the ambiguity.** The repaired Note's appositive — "a growth, a
shrink or a channel removal that changes entry_count among them" — is
genuinely parseable two ways:

- **(a) Distributive** (correct, matches §11.1's Rationale and §20.3
  step 4): "among {growth, shrink, channel removal}, the ones that
  change entry_count [trigger this]." Growth that doesn't change
  entry_count is excluded, matching the Rationale exactly.
- **(b) Proximity-bound** (the ordinary English default for "A, B, or C
  that VERBs" without a comma before "that"): "that changes
  entry_count" modifies only "a channel removal," leaving "a growth"
  and "a shrink" as **unconditional** members of the list. Under this
  reading the Note claims *every* growth re-emits the tile-index
  region — directly false, and it directly contradicts the §11.1
  Rationale it cites two words later ("§11.1") and the §20.3 step-4
  rule the same citation names.

I ran a control to confirm §11.1's own text uses this exact
"...that changes entry_count" fragment specifically for **growth**
(sweep below), which supports (a) as intended but does not resolve the
sentence's own grammar — the sentence as written still supports (b) on
a plain reading, and "among them" (an unusual phrase to append to a
three-item list) does not disambiguate; if anything "among them" reads
naturally as "among {growth, shrink, channel removal}, [the type that]
changes entry_count" — restating the same ambiguity, not resolving it.

**Verdict:** genuine ambiguity, introduced by this repair (the old
text's "or that grows... so entry_count changes" had no such
ambiguity — it unambiguously restricted itself to growth-with-
entry_count-change). Because this Note is non-normative (label: Note),
this does not fork conforming bytes — the governing rule remains
correctly stated, if separately, in §20.3 step 4 (normative) and in
§11.1's own Rationale. **Not byte-level.** But it is precisely the
shape of defect this project has been losing rounds to: a repair that
fixes the reported omission (shrink, channel removal not mentioned)
and, in the same edit, introduces a new ambiguity a reader could act on
incorrectly if they treat this Note as authoritative without checking
§11.1 and §20.3 directly.

### Check 5 / check 6 — is the "among them" list exhaustive, and what's left unconstrained

Re-read the whole of §20.3's declarations-change discussion (lines
3210-3304) for every operation that changes "index content" without
necessarily changing entry_count. Found (line 3251):

> "...what it disturbs is instead the re-emission rule above, whose
> stated occasions for a renumbering are **a geometry change and a
> permitted change to a planar layer's channel declarations**."

and (lines 3253-3264):

> "For a **planar** layer, a commit MUST NOT change the channel
> declarations in a way that alters the disk ordinal `[R-GEO-06]`
> assigns any tile the layer stores in the generation this commit
> supersedes. A channel's tiles move exactly when its index does:
> reordering moves those channels the reorder re-indexes, and
> inserting or removing one moves every channel after the affected
> position... Appending a channel, or removing the last, re-indexes
> nothing and moves no ordinal at all..."

So there are at least two more index-content-changing, permitted
commit shapes that this passage names and the Note's list does not:

1. **Reordering** existing planar channels (permitted only where the
   layer stores no tile for the moved channels) — moves ordinals
   (changes index-entry *order*, hence index content) **without**
   changing C, hence without changing entry_count at all. This case is
   invisible to *either* reading of the Note's qualifier: even the
   correct distributive reading ("...that changes entry_count") would
   wrongly exclude it, because it is a real, permitted, full-
   re-emission-triggering commit shape that does *not* change
   entry_count.
2. **Inserting** a channel not at the end (as opposed to appending,
   which "re-indexes nothing") — moves every subsequent channel's
   ordinal, and (unlike reordering) does change C and hence
   entry_count, but it is not itself "growth," "shrink," or "channel
   removal" — it's a channel *addition*, a fourth, unnamed shape.

Confirmed by direct citation that channel reordering/insertion is a
real "renumbering" trigger, distinct from geometry growth/shrink and
distinct from channel *removal*. The repaired Note presents its list
with "among them," which reads as a closed enumeration (three named
shapes), when in fact §20.3's own text names at least one further shape
(permitted channel reordering) that changes index content while never
touching entry_count, and one more (mid-list channel insertion) that
isn't covered by "growth" (which in §20.3 is used exclusively for
*extent* growth, never channel-count growth — verified: every use of
"grow"/"growth" in §20.3 attaches to "an extent," never to a channel
count).

**Verdict:** the pre-repair text was open-ended ("changes... stored-
tile set, OR grows... entry_count") and so, while incomplete, did not
claim closure. The repair's "among them" list reads as closed and is
still incomplete — an UNDERSHOT that, in fixing part of the omission
(shrink, channel removal), introduced a new false impression of
completeness. Non-normative block, so **not byte-level**; the true
condition ("index content... changes") is correctly and completely
stated in normative §20.3 step 4, which this Note is merely
illustrating.

### Checks 2, 4, 7, 8 — citations, contradiction, analogy, back-reference

- **Citations** (§11.1, §20.3, `[R-WRT-04]`): opened all three.
  §11.1 exists and its Rationale (non-normative) states the
  growth/entry_count split used above — matches. §20.3 exists and step
  4 (tagged `[R-WRT-04]` at the end of the numbered list, line 3364)
  states the normative "index content... changes" → full re-emission
  rule — matches, modulo the completeness gap noted above (a citation
  problem only in the sense that the cited rule reaches further than
  the citing sentence admits — not a wrong-pointer problem). All three
  citations resolve to real, on-topic text. PASS on resolution, with
  the completeness caveat filed as G-02.
- **Contradiction (check 4):** the reading-(b) contradiction with
  §11.1's Rationale is filed as G-01 above.
- **Analogy (check 7):** no "exactly as / the same way / on the model"
  language in this hunk. N/A.
- **Back-reference (check 8):** this hunk replaces a clause in place;
  nothing after it in §13.3 refers back with "it/that/such" to "grows
  its extents" or similar, and the section ends two lines later at
  "### 14." Checked forward to the start of §14 — no anaphor crosses
  the boundary. No back-reference defect found.

### NESTED_DASH

One em-dash pair in the repaired sentence ("— a growth, a shrink or a
channel removal that changes entry_count among them —"), not nested
inside another dash-delimited clause. Not a violation.

---

## Hunk 17 — §20.3 Example (c) (lines ~3415-3420)

### The hunk

```
 > **(c) A change confined to the directory** — clearing a slab
-> declaration, renaming a layer, or changing a channel's fill value
+> declaration, renaming a layer, changing a channel's fill value
 > where that channel carries no padding position and no pad bit in any
-> tile the layer stores in the generation the commit supersedes. Only
+> tile the layer stores in the generation the commit supersedes, or
+> dropping a PE = 0 record where §20.4 licenses the drop, any extent
+> it owned becoming slack. Only
 > the directory is re-emitted. ...
```

Header claims landing 3416-3420, nearest heading "20.3 The append
procedure" (3121). Confirmed: this is inside the blockquote
`> **Example — the three shapes a commit takes.**` (opens at line
3383), sub-case (c), which is itself inside the `>`-blockquoted
Example. Labelled **Example** → non-normative per `[R-CNF-01]`.

### Check 2 — citations

"§20.4 licenses the drop": opened §20.4's table (lines 3462-3466).
Row: `| MU = 0, PE = 0 | Retain byte-identical, or drop it — its
extent becoming slack. The licence is the bit's own... an updater MAY
drop the record in any commit it is otherwise free to make — one whose
only effect is the drop included... |`. This is exactly the licence
cited, and "one whose only effect is the drop included" is exactly the
scenario Example (c) illustrates (a commit whose only effect is
confined to the directory). Citation resolves and supports the claim.
PASS.

### Check 4/1 — is "a PE = 0 record" the right quantifier (MU implicit)?

The new clause says "a PE = 0 record," not "an MU = 0, PE = 0 record."
Checked whether this is under-specified. Opened `[R-CNT-12]` (lines
995-1003): "Writers MUST NOT emit the combination MU = 1 with PE = 0;
a reader or updater encountering it MUST treat the record as PE = 1."
So a stored MU = 1 record is *never* genuinely PE = 0 in the governing
sense — it is read as PE = 1 regardless of the stored bit. Combined
with hunk 18's own table (§20.4), the only row offering a drop is
"MU = 0, PE = 0" — the "MU = 1" row's obligation is "Retain
byte-identical" outright, drop not offered, for *either* stored value
of its PE bit. So "a PE = 0 record" (governing PE = 0) is, by
construction of this document's own rules, always an MU = 0 record —
the omission of "MU = 0" is not an ambiguity given `[R-CNT-12]` and the
table's own MU = 1 row (which doesn't discriminate by PE at all).
Checked every other use of "PE = 0" in the document (sweep below) for
a counter-example where "PE = 0" is used loosely to include an MU = 1
record — found none. **No defect** — considered and rejected.

### Check 4 — figure vs. prose (the charter's specific ask)

Read the figure immediately below shape (c) (lines 3432-3435):

```
> before │front│ A: tiles+index │ dir₁│pad│tr₁│
> after  │front│ A: tiles+index │▓▓▓▓▓▓▓▓▓▓▓▓▓│ dir₂│pad│tr₂│
```

The figure shows region "A: tiles+index" **unmarked** (not ▓) in both
"before" and "after" — i.e., the figure's own visual claim for shape
(c) is that *nothing* besides the old directory/pad/trailer becomes
slack. The new prose sentence added by this hunk says the opposite for
its own sub-case: "dropping a PE = 0 record where §20.4 licenses the
drop, **any extent it owned becoming slack**." Per the figure's own
legend two paragraphs later ("▓ marks what the commit turned to
slack"), the record's now-orphaned extent should register as new slack
in the "after" row — and it does not. The other three sub-cases
(clearing a slab declaration, renaming a layer, an in-place fill-value
change) genuinely create *no* new slack at all, so the figure was
accurate for them; the newly added fourth sub-case breaks that
uniformity but the figure was not updated to show it.

**Verdict:** LOCAL_CONTRADICTION between the repaired prose and the
figure immediately beneath it, within the same non-normative Example
block. **Not byte-level** — the figure and its surrounding prose are
inside a block labelled "Example," so per `[R-CNF-01]` neither carries
normative force; the actual obligation (drop licensed, extent becomes
slack) is independently and correctly stated in §20.4's table, which
*is* normative body text (no blockquote). This is a documentation/
illustration defect, not a conformance fork.

### Check 4 continued — the user-metadata exclusion

Read the paragraph after the figure (lines 3427-3430): "Editing user
metadata is not this shape: its document lives in an extent
(`[R-CNT-25]`), so a new extent is appended and the old one becomes
slack, as in (b)." Checked whether a *dropped* PE = 0 record could
collide with this exclusion. §20.4 (line 3450-3452): "For a type §7.3
registers, the registry's fixed flags govern... both registered types
carry PE = 1, so neither can be dropped." User metadata is a registered
type (line 1059: `0x0002 | user metadata | ... | MU = 0, PE = 1`), so
it is never PE = 0 and never in scope for the new clause. No collision.
PASS.

### Checks 5, 6, 7, 8

- **Exhaustive claims:** "Only the directory is re-emitted" (pre-
  existing, unchanged) still holds for the new sub-case — dropping
  licenses no re-emission of the extent, only its abandonment.
  Verified against §20.4's row text ("drop it — its extent becoming
  slack," no mention of moving or rewriting it). PASS.
- **Unconstrained siblings (check 6):** the other two rows of §20.4's
  table (`MU = 1`, `MU = 0, PE = 1`) offer no drop at all, so there is
  no missing "drop" case among the three obligation rows that Example
  (c) should have picked up and didn't. PASS.
- **Analogy (check 7):** no analogy language in the inserted clause.
  N/A.
- **Back-reference (check 8):** the insertion is the last item before
  "Only the directory is re-emitted," which (both before and after the
  hunk) summarizes the whole list of sub-cases — its referent set
  correctly grows to include the new sub-case; verified this doesn't
  break because "Only the directory is re-emitted" makes no claim that
  depends on the *number* of sub-cases, only that each one is
  directory-confined, which I verified above holds for the new one
  too.

### NESTED_DASH

No dashes in the inserted text.

---

## Hunk 18 — §20.4 flag-source paragraph and table heading (lines ~3459-3462)

### The hunk

```
 stored flags are authoritative (§7.3, `[R-CNT-15]`; MU = 1 with
-PE = 0 is read as PE = 1, `[R-CNT-12]`), and carry these obligations:
+PE = 0 is read as PE = 1, `[R-CNT-12]`). Whichever source governs,
+its flags carry these obligations:
 
-| Stored flags | Updater obligation |
+| Governing flags | Updater obligation |
```

Header claims 3459-3462, nearest heading "20.4 Re-emission and
preservation" (3441). Confirmed: sits in the plain paragraph
introducing the obligations table (lines 3449-3460), **not** inside a
blockquote — this is ordinary normative body text. Check 3 applies:
this is normative, and the repair, by editing normative text directly,
lands.

### The rule the repair adopts

Old text bound "and carry these obligations" grammatically only to the
third of three enumerated flag-sources ("For a type the updater does
not implement, the stored flags are authoritative..."), even though the
table plainly needs to apply across all three sources (registry-fixed,
externally-defined, and stored). New text adds a closing sentence
("Whichever source governs, its flags carry these obligations")
functioning as an explicit umbrella over all three, and renames the
column header from "Stored flags" to "Governing flags" to match.

### Check 1/6 — does the parenthetical's reinterpretation reach the other two sources?

Read the full three-source paragraph (3449-3459):

1. Registered (§7.3): "the registry's fixed flags govern rather than
   the stored ones (`[R-CNT-22]`) — both registered types carry
   PE = 1..." — MU and PE are *both* fixed by the registry; no
   MU = 1/PE = 0 combination currently exists among registered types
   (checked the registry table at line 1058-1059: layer is MU=1,PE=1;
   user metadata is MU=0,PE=1). `[R-CNT-12]`'s reinterpretation is moot
   here: there is no stored-bit ambiguity to resolve because the
   registry supplies a full, fixed (MU, PE) pair directly.
2. Updater-implemented, unregistered ("the definition it implements
   the type from supplies the flags, and the stored bits never do"):
   same structure — the external definition supplies a full (MU, PE)
   pair; stored bits are declared irrelevant ("never"). `[R-CNT-12]`'s
   text (`[R-CNT-12]` at lines 995-1003) is phrased as "Writers MUST
   NOT emit the combination... a reader or updater **encountering**
   it" — about the literal stored flags byte — so it has no
   independent bite here either, though its *practical* effect (see
   next) is moot regardless.
3. Unimplemented (stored flags authoritative): this is the sentence
   the parenthetical is textually attached to, and where
   `[R-CNT-12]`'s reinterpretation is squarely on-topic (stored bits
   *are* what's being consulted).

**Does it matter whether the reinterpretation formally reaches sources
1-2?** Checked the table itself: the `MU = 1` row's obligation
("Retain byte-identical...") does **not** branch on PE at all — there
is no separate `MU = 1, PE = 0` row. So whether a governing pair of
(MU = 1, PE = 0) is read literally or reinterpreted to (MU = 1, PE = 1),
the applicable table row and the resulting obligation are identical
either way. **The new umbrella sentence does not, in practice, extend
`[R-CNT-12]`'s reinterpretation anywhere it would change an
obligation** — I checked this specifically because the charter flagged
it as a risk, and it resolves clean. No defect here.

### Check 4 — the MU = 0, PE = 0 row's own text vs. the new "Governing flags" framing

The hunk renamed the heading from "Stored flags" to "Governing flags"
— a real, needed generalization, since two of the three sources supply
flags that are explicitly *not* what's stored. But the row text for
`MU = 0, PE = 0` (untouched by this hunk, line 3466) says:

> "The licence is the bit's own: **the writer that stored PE = 0**
> declined preservation across edits, so an updater MAY drop the
> record..."

This presumes the governing PE = 0 came from what "the writer... stored"
— true for source 3 (stored flags authoritative), but by the
paragraph's own words, **false** for source 2: "the definition it
implements the type from supplies the flags, **and the stored bits
never do**." A type reaching the `MU = 0, PE = 0` row via source 2 (an
externally-defined, updater-implemented, unregistered type whose
definition specifies MU = 0, PE = 0) did *not* get there because any
writer "stored PE = 0" in this file — the governing value came from the
external definition, independent of whatever bits are physically
present. (Source 1 cannot reach this row at all — both current
registered types are fixed PE = 1 — so the live counter-example is
specifically source 2.)

Practical obligation is unaffected (still "MAY drop... its extent
becoming slack" either way), so this is a rationale/attribution
staleness, not an obligation change. But it is a real inconsistency the
repair should have swept: broadening the header to "Governing flags"
while leaving a row's own explanatory sentence keyed to "the writer
that stored" is exactly the pattern of "a restatement elsewhere ... the
repair should have swept and did not," here in the very same table the
repair edited. Filed as G-04. **Not byte-level.**

Swept the rest of the document for this phrase (sweep below) — only
one occurrence, confirming this is not also duplicated (and therefore
inconsistently fixed) elsewhere.

### Checks 2, 5, 7, 8

- **Citations:** `[R-CNT-15]` (§7.3, unimplemented-type file/layer
  handling) and `[R-CNT-12]` (checked above) both resolve to on-topic
  text. PASS.
- **Exhaustive claims:** "Whichever source governs" ranges over exactly
  the three sources enumerated in the same paragraph — verified the
  three are exhaustive by construction (registered / implemented-
  unregistered / unimplemented is a full trichotomy over "does the
  updater implement this type and is it registered"). No fourth case
  found. PASS.
- **Analogy (check 7):** none in this hunk.
- **Back-reference (check 8):** "its flags" in the new sentence refers
  to "whichever source" in the same sentence — self-contained, no
  drift. Checked forward: the paragraph after the table ("No commit
  therefore removes a layer record...") depends on the table's MU = 1
  and PE = 1 rows, unaffected by the rename. PASS.

### NESTED_DASH

No dashes in the inserted text.

---

## Hunk 23 — §22.3 Structural attacks, mimic-trailer residue (lines ~4196-4201)

### The hunk

```
 trusted (`[R-LIF-06]`) before any use. Under live-state coverage a
-mimic in slack is inert — nothing enumerates it — but a recovery
-tool that truncates to one produces a different file, which is why
-its output is re-verified whole. And the extent of a user-metadata
+trusted (`[R-LIF-06]`): under live-state coverage a mimic in slack
+is inert — nothing enumerates it — but a recovery tool that
+truncates to one produces a different file. And the extent of a user-metadata
```

Header claims 4199-4201, nearest heading "22.3 Structural attacks"
(4167). Confirmed: plain body text (not a blockquote) inside §22.3's
"Four residues are stated rather than defended" paragraph — normative
per `[R-CNF-01]` (§22 is not an exempted appendix and this text carries
no Note/Example/Rationale label).

### The rule the repair adopts

Removes a redundant trailing justification clause and merges two
sentences at a colon. Before: two separate "which is why X is
re-verified" statements (once with the `[R-LIF-06]` citation, once
without, at the very end). After: one "which is why... (`[R-LIF-06]`)"
statement, followed by a colon-introduced elaboration that states two
supporting facts (mimic-in-slack is inert under live-state coverage;
truncating to one produces a different file) without repeating the
"which is why" framing a second time. Also drops the redundant
"before any use" (redundant with "before being trusted").

### Check 8 — "its output" and "one" (charter's specific ask)

**"its output":** this phrase is **deleted entirely** by the hunk — it
does not appear anywhere in the repaired text. Confirmed by search
(sweep below: 0 occurrences after the hunk). So there is no dangling
"its output" reference left to resolve; the concern the charter raises
is moot by deletion, not by a bad resolution.

**"one":** traced both occurrences.
- First "one" ("recovery tooling that scans backward can land on
  one") — refers to "a byte string that mimics a trailer" (same
  sentence, unaffected by the hunk).
- Second "one" ("a recovery tool that truncates to one") — nearest
  antecedent, both before and after the hunk, is "a mimic in slack"
  (the noun phrase immediately preceding, in the clause "under
  live-state coverage a mimic in slack is inert — nothing enumerates
  it — but a recovery tool that truncates to one"). The hunk changes
  the punctuation before this clause (period → colon after
  `[R-LIF-06]`) but does not move this clause relative to "a mimic in
  slack," so the antecedent is **unchanged** by the repair — verified
  this is not a case of check 8's failure mode (inserting text between
  a pronoun and its antecedent), since nothing was inserted here; the
  material between "mimic in slack" and "truncates to one" is
  identical before and after ("is inert — nothing enumerates it —
  but a recovery"). Read as intended: recovery's backward scan can
  truncate specifically to a mimic that sits in slack (the case that
  is inert for ordinary live-state-covering readers but dangerous for
  a tool that scans raw bytes). Coherent, unaffected by the repair.

**Considered and rejected:** whether "a mimic in slack" is itself too
narrow — a mimic byte string could in principle occur inside a
currently-*live* tile's payload too (not only in superseded/slack
bytes), and the residue's own opening clause ("a payload can contain a
byte string that mimics a trailer") does not restrict itself to slack.
Checked whether the hunk introduced this narrowing: it did not — "a
mimic in slack is inert" is present verbatim in the pre-hunk ("-")
lines too, unchanged by this repair. Since my charter is to audit what
*this* repair did to the text, and this phrase's scope was neither
touched nor made worse by the hunk, I am not filing it as a finding
against hunk 23; noted here as a rejected candidate.

### Check 4 — "which is why" still has its reason; colon clause explains rather than restates

"recovery tooling that scans backward can land on one, which is why
recovery output is re-verified as a whole file before being trusted
(`[R-LIF-06]`)" — the reason ("tooling can land on a mimic") for the
consequence ("re-verified before trusted") is intact and adjacent;
unaffected by the hunk's colon/period change. PASS.

Colon clause ("under live-state coverage a mimic in slack is inert...
but a recovery tool that truncates to one produces a different file")
adds two facts not previously stated before this point in the sentence
(the live-state/inert contrast, and the truncation mechanism) — this is
elaboration, not restatement of "which is why... re-verified." PASS —
matches the charter's framing that the colon should explain rather than
restate.

### Check 2 — citation

`[R-LIF-06]` opened at §9.6 (lines 1418-1457). Confirmed §9.6's own
text: "a tile payload can deliberately contain a byte string that
mimics a valid trailer, so recovery output MUST be re-verified as a
whole file (§8) before being trusted." This matches the §22.3
sentence's claim precisely (same trigger, same consequence, same
citation). PASS.

Cross-checked §21.6's mimic row (line 3936): "A payload contains a
byte string that mimics a trailer | Inert: nothing enumerates slack,
and a recovery tool re-verifies its output whole (§9.6) — which catches
any mimic that is not itself a consistent generation; §9.6's second
caution covers the rest | `[R-LIF-06]`." This is a *more* nuanced
statement (re-verification does not catch a mimic that also happens to
form a self-consistent generation; that residual risk is left to
§9.6's second, rollback caution) than §22.3's residue text, but §22.3's
repaired text makes no completeness claim ("catches every mimic") that
this would contradict — it only says truncating "produces a different
file," which is true regardless of whether re-verification catches it.
No contradiction with §21.6. PASS.

### Checks 1, 5, 6, 7

- **Tense/quantifier:** "a payload can contain," "recovery tooling
  that scans backward can land," "a mimic in slack is inert," "a
  recovery tool that truncates" — all present-tense, generic-actor
  statements, unchanged in scope by the hunk (only punctuation/
  sentence-boundary and the one redundant clause were touched). PASS.
- **Exhaustive claims:** none introduced ("Four residues," pre-existing,
  unaffected).
- **Unconstrained siblings:** the other three residues in this same
  list (slack corruption, unassigned-type-record corruption,
  user-metadata-under-experimental-encoding) are untouched by this
  hunk and were not re-examined for new gaps, since the hunk does not
  touch them.
- **Analogy:** none in this hunk.

### NESTED_DASH

One em-dash pair ("— nothing enumerates it —") in the post-colon
clause, not nested inside a second dash-delimited clause. Not a
violation.

---

## Sweeps run (verbatim, with hit counts and controls)

All sweeps below strip leading `> ` blockquote continuation markers per
line, then collapse remaining whitespace runs to a single space, before
substring search — this is necessary because a naive `\s+`-only
normalization leaves the literal `"> "` markers in place at wrapped
line-breaks inside blockquotes and produces false zero-counts (see
"methodology check" below, which is exactly this failure caught on my
own first pass).

**Methodology check (control proving the naive approach is unsafe):**
first pass, normalizing only `\s+` without stripping `"> "`, returned
**0** hits for `"a growth, a shrink or a channel removal"` and **0**
hits for `"any extent it owned becoming slack"` — both of which are
verbatim substrings of the *current* file (confirmed by direct
`Read`). Re-running with blockquote markers stripped first found both
(1 hit each). This is reported per the brief's explicit instruction:
"before you rest any conclusion on a zero, run the same search for a
phrase you know is present" — the first pass's zeros were exactly this
failure mode, caught before drawing any conclusion from them.

Sweeps (post-fix methodology), with hit counts:

| Search | Hits |
|---|---|
| `that changes entry_count` | 2 (§11.1 Rationale: "Growth that changes entry_count..."; hunk 06's own Note) |
| `a growth, a shrink or a channel removal` | 1 (hunk 06 only) |
| `any extent it owned becoming slack` | 1 (hunk 17 only) |
| `dropping a PE = 0 record where` | 1 (hunk 17 only) |
| `Governing flags` | 1 (hunk 18's table heading only — not referenced elsewhere by name) |
| `Whichever source governs` | 1 (hunk 18 only) |
| `a mimic in slack is inert` | 1 (hunk 23 only) |
| `its output is re-verified whole` | 0 (confirms hunk 23's deletion took; this exact phrase is gone) |
| `before any use` | 1 — but at an unrelated location (§19-ish, "before any use of the layer's declarations," a different sentence entirely; not the deleted §22.3 occurrence) |
| `declined preservation` / `bit's own` / `the writer that stored` | 1 (only in §20.4's MU=0,PE=0 row — confirms G-04 is not duplicated/inconsistently-fixed elsewhere) |
| `Stored flags` (old table heading, as a standalone phrase) | 0 (fully replaced, no stale duplicate of the old heading text elsewhere) |
| PE = 0 (raw, all occurrences via line-oriented grep, then checked each in context) | lines 997, 1002, 3419 (hunk 17), 3459 (hunk 18), 4811 — all reviewed above; no case where "PE = 0" is used to denote a governing value for an MU = 1 record |

## Derived numbers

- Recomputed grid counts for the §11.1 growth-without-entry_count-change
  example by hand: extent 900, tile 256 → ⌈900/256⌉ = ⌈3.515625⌉ = 4;
  extent 1000, tile 256 → ⌈1000/256⌉ = ⌈3.90625⌉ = 4. Equal — confirms a
  growth exists that changes Eᵢ but not Gᵢ (hence not N, hence not
  entry_count) outside the "one dimension stays 0" example §11.1 gives,
  supporting that the Rationale's stated principle is broader than its
  own illustrative example (used in the check-1 analysis for hunk 06).
- No CRC, checksum, count, or offset arithmetic was required by any of
  the other three hunks' own claims (hunk 17/18/23 turn on citation and
  cross-reference checks, not on independently derivable numbers), so
  no further derived numbers were computed.

## Rejected candidates

1. **Hunk 17 — "a PE = 0 record" omitting "MU = 0."** Considered as a
   possible under-specification; closed by `[R-CNT-12]` (MU=1/PE=0 is
   always read as PE=1) plus §20.4's `MU = 1` row not branching on PE —
   a governing PE = 0 is, by the document's own construction, always an
   MU = 0 record, so the shorthand is accurate. Not filed.
2. **Hunk 18 — does `[R-CNT-12]`'s reinterpretation formally extend to
   sources 1 and 2 given the new umbrella sentence?** Considered at
   length; closed because the table's `MU = 1` row doesn't discriminate
   by PE at all, so the question is moot in every case that could
   arise. Not filed as a defect (documented in the hunk-18 section as
   a checked-and-passed item, not silently dropped).
3. **Hunk 23 — "a mimic in slack" narrower than "a payload... contains
   a byte string that mimics a trailer."** Considered; the phrase
   predates this hunk verbatim (present in the "-" lines too), so any
   defect here belongs to a different round's repair, not this one.
   Not filed against hunk 23.
4. **Hunk 06 — could "among them" be read as deliberately signalling
   "these are only *some* examples, not a closed list"?** Considered;
   rejected as the natural reading, because the list is bounded ("a
   growth, a shrink or a channel removal") with no hedge like "such as"
   or "for instance," and because the very passage it summarizes
   (§20.3) names a further shape (channel reordering) that isn't
   covered by any reading of the sentence as written. Filed as G-02.

## Confidence / where little was found

Hunk 23 returned no filed findings. What I did that would have caught
one: read the full residue paragraph and its neighbors on both sides
(not just the diff's context lines), opened both citations it touches
(`[R-LIF-06]` at §9.6 in full, and cross-checked against §21.6's more
nuanced mimic row), traced both back-references the charter named
("its output," "one") to their actual antecedents pre- and post-repair,
confirmed the deleted clause's phrase is fully gone (not orphaned) by
direct search, and checked for nested em-dashes. The one substantive
alternate reading I found (mimic could occur in live payload, not only
slack) is pre-existing text this hunk did not touch, so it's reported
as a rejected candidate rather than a finding against this repair.
