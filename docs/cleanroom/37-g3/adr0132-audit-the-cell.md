# Audit transcript — Hunk 01, §6.2 trailer flags cell

## 0. Contamination disclosure (read this first)

Before any of my own reading, my runtime context already contained, unsolicited:

- `CLAUDE.md`'s one line pointing to `AGENTS.md` (a file the charter explicitly
  forbids me to read; I did not read it).
- A `MEMORY.md` index of ~18 prior-session note titles about this same TARN
  project (e.g. "TARN repair prose vs rules", "TARN class lines are
  undertakings", "TARN no lowercase keywords"), none of whose linked bodies I
  opened.
- A `gitStatus` block naming the branch, and five recent commit subjects,
  including `ab0c096 ADR-0132: round 37's repair, and G3 declared met` and
  `3ec4b50 Cleanroom round 37: ... six findings, six defects, the refute phase
  stood on the zero`.
- MCP server instructions for a Docs connector and a Chrome browser tool,
  irrelevant to this task.

None of this is the specification and none of it is evidence about the
specification or about this hunk. I have not opened `AGENTS.md`, any
`MEMORY.md`-linked file, `docs/`, git log, or git diff, and I have not let the
commit subjects above (e.g. "six findings, six defects") steer my search for a
target count of defects in *this* hunk — my findings below are derived solely
from the spec text and the hunk file. I disclose this per the charter's
instruction rather than acting on it silently.

## 1. Access and hunk-file check

Read exactly:
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r38-audit/case/hunk-01.diff`

Did not read: `full.diff`, any other hunk file, `docs/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`,
`spec/registry.json`, git history/log/diff, or the web. Did not list the
`case/` directory (only `cat`'d the one named hunk file).

Hunk file contents (`hunk-01.diff`):

```
# hunk 1 of 1
# lands in spec/tarn.md at lines 838-838 (current file)
# this hunk both inserts and deletes
# nearest preceding heading in the current file: line 828, "6.2 Trailer"
@@ -835,7 +835,7 @@ The trailer occupies the final 64 bytes of the file, beginning at a
 | 0 | 8 | bytes | trailer magic | structural | `8A 4E 52 41 54 0D 0A 1A` (`\x8A`, "NRAT", CR, LF, ctrl-Z) |
 | 8 | 2 | u16 | version_major | structural | 1 (0 invalid; others: §6.3) |
 | 10 | 2 | u16 | version_minor | descriptive | any (see §6.3) |
-| 12 | 4 | u32 | flags | structural | bits 0–15 (incompat lane) all zero, a set bit being reject-file (F19); bits 16–31 (ignore lane) 0 from a creator, carried forward unchanged by an updater, appender or rewriter alike, a set bit ignored (§6.3) |
+| 12 | 4 | u32 | flags | structural | bits 0–15 (incompat lane) all zero, a set bit being reject-file (F19); bits 16–31 (ignore lane) 0 from a creator, carried forward unchanged by every updater, appender and rewriter alike, a set bit ignored (§6.3) |
 | 16 | 8 | u64 | dir_offset | structural | ≥ 16 |
 | 24 | 8 | u64 | dir_length | structural | ≥ 4; dir_offset + dir_length ≤ F − 64 |
 | 32 | 8 | u64 | committed_file_length | structural | = F; multiple of 64 |
```

Verified against the current file:

```
$ sed -n '828,844p' spec/tarn.md
```
gives line 828 = `#### 6.2 Trailer` (matches header comment) and line 838 =
the post-image exactly, byte for byte, including the em dash in "0–15"/"16–31"
and the section mark before "6.3". **No header/body discrepancy.** The hunk
file is exactly where the brief says.

## 2. The rule the repair adopts, in my own words

Before repair, the cell said the 16 ignore-lane bits are (a) 0 as emitted by a
creator, and (b) "carried forward unchanged by an updater, appender or
rewriter alike" — worded as if "updater", "appender", and "rewriter" were
three separate, coordinate kinds of actor, each independently in view. §20.1
and §2.3 establish that there is no such third kind: the *only* two tiers of
updater this document defines are appender and rewriter ("An appender and a
rewriter are updaters", §20.1; "Conforming updater ... Its tiers, the
appender and the rewriter, are §20.1's", §2.3). So reading the old cell as
listing three coordinate actors overclaims a class of updater the document
does not have.

The repair does not change the substantive rule (still: 0 from a creator,
unchanged-carry from every appender/rewriter) — it changes the actor phrase
to copy §6.3's own wording, "carried forward unchanged by every updater,
appender and rewriter alike", to match §6.3's "carried forward by every
updater under this text, appender and rewriter alike" (`[R-CNT-08]`).

## 3. Passages read before judging (per charter's list)

Read: §2.3 (lines 152–301), §4.7 (596–628), all of §6.1 (784–827), all of
§6.2 (828–877), all of §6.3 (878–922), §20.1 (3134–3172), §20.2 (3173–3187),
§20.3 step 6 (3379–3388), §20.5's opening through its trailer sentence
(3551–3627), Appendix G item 2 (4726–4740) and item 8 (4816–4831), Appendix H's
writer entry (4915–4924) and updater entry (4926–4948).

Quotes pulled out for direct comparison:

- §2.3 (line 208-214): "**Conforming updater.** A tool that modifies an
  existing file, or as a rewriter writes a new one from it (§20.1), without
  necessarily understanding all of its content. ... Its tiers, the appender
  and the rewriter, are §20.1's."
- §20.1 (line 3150-3151): "An appender and a rewriter are updaters: each
  satisfies every writer requirement for the bytes it produces and the
  preservation obligations of §20.4 ..."
- §20.1 (line 3163-3169): "A writer of a new file from an existing one takes
  one of two positions, and the choice is its own. As a **rewriter** it
  undertakes to preserve its input ... As a **creator** it undertakes nothing
  toward its input, whatever it read: §20.2 binds it, it writes flags = 0..."
- §6.3 [R-CNT-08] (lines 898-915), in full: "Flags: a reader MUST reject-file
  on any set bit it does not implement in the incompat lane (bits 0–15), and
  MUST ignore all bits in the ignore lane (bits 16–31). In this
  specification's text no flag bits are defined: a writer creating a file
  under this text MUST write flags = 0, but a set ignore-lane bit is not a
  file-conformance violation — such bits are defined by later minor versions,
  and files carrying them are conforming files this text's readers ignore. A
  rewriter, though its output is a new file, carries the input's unknown
  ignore-lane bits into its output trailer rather than writing flags = 0, and
  sets no other (§20.5, `[R-WRT-06]`). An updater MUST copy forward unknown
  ignore-lane bits of its input file, MUST NOT clear them, and MUST NOT set
  any other: no writer under this text originates an ignore-lane bit, this
  text defining none for it to mean anything by, so a bit is set only by a
  writer under the later minor version that defines it and carried forward by
  every updater under this text, appender and rewriter alike. An updater
  encountering an unknown incompat-lane bit is a reader first, and therefore
  rejects the file before modifying anything."
- §20.3 step 6 (3381-3388): "**Commit** ... unknown ignore-lane flag bits
  copied forward and no other set (`[R-CNT-08]`) ..."
- §20.5 (3608-3611): "The output trailer MUST copy the input's unknown
  ignore-lane flag bits forward and set no other, in place of the flags = 0
  §6.3 requires of a file created under this text (`[R-CNT-08]`)."
- §21.6 register row (line 4030): "An ignore-lane flag bit (16–31) is set |
  Ignored; the file is conforming — such bits are defined by later minor
  versions | `[R-CNT-08]`".
- Appendix G item 8 (4830-4832): "The `flags` half is a creator's rule, as
  item 2's identifier is: a rewriter adopting the profile carries its input's
  unknown ignore-lane bits forward instead, setting no other (`[R-CNT-08]`)."
- Appendix H writer entry (4919-4921): "writes flags = 0 when it creates a
  file, a rewriter instead carrying its input's unknown ignore-lane bits
  forward and setting no other (`[R-CNT-08]`, §6.3, §20.5)."
- Appendix H updater entry (4926, 4936-4938): "**Conforming updater**, an
  appender or a rewriter (§20.1) ... copies forward the input's unknown
  ignore-lane flag bits, clears none and sets no other (`[R-CNT-08]`, §6.3)."

## 4. Establishing the cell's force (check 3 / NORMATIVE_PLACEMENT)

The flags row sits inside an ordinary Markdown table under `#### 6.2 Trailer`,
not inside a `>`-blockquote of any kind, so the "check the label, not the
marker" question doesn't even present a `>` to second-guess — there is no
label at all attached to this row (no **Note.**, **Example.**, **Rationale.**
heading governs a table row). Per `[R-CNF-01]`, text is normative "except:
§1 ...; any text labeled Note, Example, or Rationale; and appendices
identified as non-normative." §6.2 is none of those, so **the row is
normative text**, full stop.

What is the cell's "Valid values" column *relative to* the rules stated below
the table? §4.7 states the general layout-table convention (offset, size,
type, name, class, valid range) but its one sentence about a value column
being glossed "in the rules below the table" is stated specifically for
§7.2's field cell (line 620-621), not as a universal rule for every layout
table. For §6.2 specifically, the text immediately following the table
settles the question directly: "A reader MUST validate, in order: the
trailer magic; the trailer CRC; the version gate (§6.3) ...; and then ... MUST
validate all of the following ...: the flag gates (§6.3); committed_file_length
..." (lines 861-869). So §6.2 itself names §6.3 as the place the actual flag
gate is validated — the cell is a normative *summary* whose authority for the
flags rule is §6.3, cited in the cell's own parenthetical "(§6.3)". This
matches how the cell is written (it doesn't restate the MUST-level obligations
itself; it points at §6.3).

## 5. Check 2 — citations resolve

The repaired cell carries exactly one citation, `(§6.3)`, covering both the
incompat-lane and ignore-lane sentences (unchanged placement of the citation;
hunk did not move it). §6.3, read in full above, is exactly the site of
`[R-CNT-08]` (ignore-lane copy-forward rule) and of the incompat-lane
reject-file rule ("a reader MUST reject-file on any set bit it does not
implement in the incompat lane"). **Verdict: PASS.** §6.3 says what the cell
claims it says, for both lanes.

No requirement ID appears inside the hunk's changed text itself (the cell
names no `[R-...]` id directly — only the section number). Nothing else to
resolve.

## 6. Check 1 — tense, quantifier, actor (the central question for this hunk)

**Generation:** Not applicable in the "prior state vs new state" sense used
for tile/layer rules — this is about which *actor*, not which file
generation, the sentence ranges over.

**Set the repair ranges over:** "every updater, appender and rewriter alike."
Compare to §6.3's own construction, word for word:

- Cell (after repair): `carried forward unchanged by every updater, appender
  and rewriter alike`
- §6.3 [R-CNT-08]: `carried forward by every updater under this text,
  appender and rewriter alike`

The only textual difference is §6.3's extra `under this text` between
`updater` and the comma. What does `under this text` do there that nothing
does in the cell? In §6.3's sentence, `under this text` is doing real
disambiguating work: the sentence's own immediately preceding clause has just
introduced a *second*, contrasting actor — "a bit is set only by **a writer
under the later minor version** that defines it" — i.e. a writer bound by a
different (future) specification text who *originates* new ignore-lane bits.
`under this text` then marks the *carrying* actor ("every updater under this
text") as the writer bound by *this* document, in contrast to that other
writer bound by the later text. That contrast is what makes `appender and
rewriter alike` parse as a gloss on the single class `updater` rather than a
third, independent list item — the sentence has already spent a full clause
establishing "updater" (singular, definite: "An updater MUST copy forward...")
as its topic before this final clause repeats it.

**Does the cell's quantifier match the normative rule it restates?**
Substantively, yes — "every updater" here correctly ranges over exactly
{appender, rewriter} and nothing else, which is what §20.1/§2.3 establish and
what §6.3 states. I checked this concretely with **check 5**: take a writer
of a new file who read an existing file and takes the *creator* position
under §20.1 — §20.1 line 3168-3169 puts it under "it writes flags = 0",
i.e. the cell's first half ("0 from a creator"). Take the same shape of
writer taking the *rewriter* position — §20.1 line 3164-3167 and §6.3's
rewriter sentence put it under "carries the input's unknown ignore-lane bits
... rather than writing flags = 0", i.e. the cell's second half. An
*appender* (§20.1's third tier) also falls under the second half via
`[R-CNT-08]`'s "An updater MUST copy forward..." Between the two halves,
every one of §20.1's three writer tiers (creator, appender, rewriter) is
covered once, and none twice. **No exhaustive-claim defect: "every updater"
does not overclaim, and nothing is left uncovered.**

**But does the phrase, read as this table cell is read — cold, without first
re-reading §6.3 — still admit the very reading the repair was written to
foreclose?** I think yes, and this is the one substantive finding of this
audit (see §9 below).

## 7. Check 4 — contradiction in the untouched surrounding passage

Re-read the whole §6.2 flags-adjacent text: the pre-trailer-pad paragraph
(846-855), the validation-order paragraph (861-871), the two Notes (857-859,
873-876). None of them mention flags-lane actors again, and none narrows or
widens what the repaired cell says. The row above (version_minor, "any (see
§6.3)") and below (dir_offset, "≥ 16") are untouched and don't interact with
the flags cell's wording.

Checked the incompat-lane half of the same cell (unchanged by the hunk): "bits
0–15 (incompat lane) all zero, a set bit being reject-file (F19)" — no
actor-list wording there to be inconsistent with the repaired ignore-lane
half; no MUST/MAY collision found.

**No local contradiction found**, touched or untouched.

## 8. Check 6 — what else in this structure is left unconstrained

The structure here is the whole `flags` field: a u32, 32 bits, partitioned by
the cell itself into two lanes, bits 0–15 (incompat) and bits 16–31 (ignore).
16 + 16 = 32 — I verified this arithmetic against the field's own declared
size (4 bytes = 32 bits) and it accounts for every bit; the repair did not
touch the incompat-lane clause or the lane boundary, and neither lane is left
unmentioned. Within the ignore lane, the cell states a value for exactly the
two writer-facing situations that exist per §20.1 (creator: 0; appender or
rewriter, i.e. every updater: unchanged) and one reader-facing situation ("a
set bit ignored"), matching `[R-CNT-08]`'s reader clause and the §21.6/F-row
treatment of the incompat lane's own reader clause (F19) for the other lane.
I don't find a fourth writer/reader situation this table's own convention
(offset/size/type/field/class/valid-values) would call for that the cell
omits. **No UNCONSTRAINED_SIBLING finding here** — unlike the historical
"pinned one quantity, left a neighbouring quantity of the same header
unpinned" case the charter warns about, this field has exactly two siblings
(the two lanes) and both are constrained, on both the writer and reader side.

Swept the rest of the table's Valid-values column for any other cell naming
an actor, to compare idiom: `1 (0 invalid; others: §6.3)`,
`any (see §6.3)`, `≥ 16`, `≥ 4; ...`, `= F; multiple of 64`, `≠ 0`, `zero`,
`CRC-32C over trailer bytes [0, 60)` — none of the other eight cells name an
actor at all. The flags cell is the only one in this table describing
per-actor behavior, so there is no sibling-cell idiom to compare it against
for consistency.

## 9. Check 8 / the "idiom copied" concern — the finding

Grepped every occurrence of the word "alike" in the document (normalized
whitespace, to survive the hard wrap):

```
$ python3 -c "import re; t=open('spec/tarn.md').read(); n=re.sub(r'\s+',' ',t); 
  import re as r; [print(m.start()) for m in r.finditer('alike', n)]"
```
gives 5 hits. Located and read each:

1. Line 838 (the cell, under audit): `...every updater, appender and
   rewriter alike...`
2. Line 913 (§6.3, `[R-CNT-08]`): `...carried forward by every updater under
   this text, appender and rewriter alike.`
3. Line 4298 (§22.4): `...is invisible to reader and verifier alike...`
   — a two-item pair.
4. Line 4763 (Appendix G item 3): `Records and a layer record's sub-records
   alike are ordered by type...` — a two-item pair (records, sub-records).
5. Line 4875 (Appendix G, closing paragraph): `...binding creator and
   rewriter alike save §20.5's...` — a two-item pair.
6. Line 4953 (Appendix H, updater entry, closing sentence): `...of an
   appender and a rewriter alike: an updater that drops a record SHOULD
   report the loss...` — a two-item pair.

**Every other use of "alike" in this entire document pairs it with exactly
two coordinate nouns joined by "and" immediately before it** (reader/verifier;
records/sub-records; creator/rewriter; appender/rewriter). Occurrence 1 (the
repaired cell) and occurrence 2 (§6.3, its model) are the *only* two places in
the document where a noun sits *before* an "X and Y alike" pair, separated by
a comma, with no further scaffolding.

This is exactly why §6.3's own version is not itself a problem in its home
paragraph: that paragraph's opening sentence, "An updater MUST copy forward
unknown ignore-lane bits of its input file..." (line 907-908), has already
made "updater" the definite, singular topic of the whole passage two clauses
earlier, and "under this text" further marks it off from the *other* actor
the same sentence just introduced (the later-minor-version writer). By the
time the reader reaches "...carried forward by every updater under this
text, appender and rewriter alike," "appender and rewriter alike" reads as
the document's normal two-item "alike" idiom, glossing the single,
already-established class "updater."

**The cell has none of that scaffolding.** It is a comma-separated list of
clauses inside one table row; the flags cell's own immediately preceding
clause is about a *different* actor ("0 from a creator"), not about
"updater." Nothing in the cell first establishes "updater" as a definite
topic before "every updater, appender and rewriter alike" is reached. Read
cold — the way a table cell is read — "every updater, appender and rewriter
alike" is exactly as compatible with a three-coordinate-actor parse (every
updater / every appender / every rewriter, distributed, on the same pattern
as "every man, woman and child alike") as the *pre-repair* text was ("an
updater, appender or rewriter alike"). Swapping "an"→"every" and "or"→"and"
made the surface tokens match §6.3, but it did not import the discourse
context (the prior sentence establishing "updater" as topic, and the
contrasting later-minor-version writer) that made §6.3's identical
three-noun-before-"alike" string parse unambiguously there. A reader of the
table alone — who, per this cell's own convention, is not required to have
just read §6.3's full paragraph, only to consult it as authority (§4) — can
still read this cell as implying a third kind of updater next to appender and
rewriter, which is precisely the reading `[R-CNT-08]`/§20.1/§2.3 foreclose
and precisely the reading this repair was written to eliminate.

**This is UNDERSHOT, not a fresh, self-standing NEW_AMBIGUITY**: the defect
the repair was aimed at (a wording that can be read as three coordinate
actors, implying a non-existent third updater class) is still available in
the repaired text, for a reader who takes the cell on its own, because the
fix copied §6.3's tokens without also importing the sentence-initial
topic-establishing move ("An updater MUST...") that disambiguates them there.

Contrast with §2.3's own restatement of the same rule (line 174-175): `"an
updater's copy-forward and set-no-other"` — §2.3 sidesteps the whole issue by
never listing the tiers at all, just naming the class. That both proves a
clean phrasing was available and reachable within this document's own
vocabulary, and shows the cell's three-noun-before-"alike" construction was
an avoidable choice, not a forced one.

**Byte-level:** No. Under either reading of the cell (apposition, or
three-coordinate-actor), no other passage in the document defines or permits
a third kind of updater, or a different carry-forward rule for it — `[R-WRT-01]`
is explicit that the only two positions a writer of a new file from an
existing one can take are creator and rewriter, and `[R-CNF-06]`/§20.1 are
explicit that appender and rewriter, and only they, are updaters. So a
misreading of this cell cannot license an implementer to produce, or a
verifier to accept, any byte sequence that `[R-CNT-08]`, §20.3 step 6, and
§20.5 do not already independently permit or forbid. The set of conforming
files, and the set of bytes a conforming updater may emit, does not move
under either reading. This is a documentation-clarity defect, not a
byte-level one.

## 10. Check 5 — exhaustive-claim words

Flagged in the repaired text: "every" (updater), "all" (zero, incompat
lane — unchanged by hunk). Tested "every updater" against §20.1's full writer
taxonomy above (§6 of this transcript) — it is exactly co-extensive with
{appender, rewriter} and does not overclaim. No falsifying case found.

## 11. Check 7 — analogy

The hunk contains no "exactly as", "the same way", "following X", "on the
model of", or similar analogy-by-citation language — the cell's only
justificatory move is the direct citation `(§6.3)`, checked in §5 above as a
citation, not an analogy. **Check 7 does not apply to this hunk**; reporting
that explicitly rather than silently skipping it.

## 12. Check 8 — anaphors and "alike" resolution, formally

The hunk is a same-shape substitution inside one table cell, not an insertion
of new material between two previously-adjacent sentences, so there is no
"the bar above" / "that requirement" back-reference from later text whose
nearest antecedent has moved. I checked anyway, forward from the cell to the
end of the row and into the next row (dir_offset: "≥ 16") — no anaphor there
refers back into the flags cell.

Within the cell: `alike` attaches, both before and after the edit, to the
nearest immediately-preceding pair — `appender {or/and} rewriter` — not to
`updater`. That attachment did not change. What changed is only the relation
between `updater` and that pair (see §9): whether `updater` is a third
coordinate item or the head being glossed by the pair is exactly as
underdetermined after the edit as before it, so no pronoun/`alike` silently
re-resolved to a different antecedent — it was already unresolved, and the
edit didn't resolve it either. I record this as UNDERSHOT (§9), not as a
fresh ANAPHOR-category defect, since nothing *newly* mis-resolves; the same
open question persists.

## 13. BCP 14 casing and NESTED_DASH

The repaired cell text contains no BCP 14 keyword at all — no MUST, MUST NOT,
SHALL, SHOULD, or MAY appears anywhere in either the pre- or post-image of
the hunk. (Confirmed by reading both images character by character above;
the cell states values and defers the modal force to §6.3, which does carry
the MUSTs.) Nothing to case-check.

The cell contains no em dash at all (it uses commas, semicolons, and
parentheses only), so there is no dash pair to nest and no NESTED_DASH
finding.

## 14. Restatement sweep (full list, per charter)

Ran, both as plain `grep -n` (line-oriented) and as a whitespace-normalized
Python count (to catch phrases the hard wrap splits across lines), for every
phrase the charter names:

| phrase | grep -n (lines) | normalized count | control |
|---|---|---|---|
| `ignore lane` | 3 | 3 | — |
| `ignore-lane` | 17 | 17 | — |
| `flags = 0` | 6 | 6 | — |
| `set no other` | 1 | 1 | — |
| `sets no other` | 2 | 2 | — |
| `copy forward` | 1 | 1 | — |
| `copies forward` | 1 | 1 | — |
| `clears none` | 1 | 1 | — |
| `carried forward` | 6 | 6 | — |
| `carries forward` | 8 | **11** | proves normalization needed/works |

The `carries forward` discrepancy (8 line-grep vs 11 normalized) is the
control that proves the normalized search is actually finding wrapped
instances the line-oriented grep misses, per the charter's warning about hard
wrap — I did not rest any zero-result conclusion on the line-oriented numbers
alone anywhere in this audit.

Located every `ignore-lane`/`ignore lane` hit and read its context (§2.3 line
174, §4.2 line 501, the cell line 838, §6.3 lines 900/902/906/908/910/913,
§10.1 line 1572, §10.4 line 2848, §20.1 line 3165, §20.3 step 6 line 3385,
§20.5 line 3609/3613, §21.6 register row line 4030, Appendix A line 4555,
Appendix B line 4633, Appendix G item 8 line 4832, Appendix H writer entry
line 4919, Appendix H updater entry line 4937). Quoted the load-bearing ones
in §3 above. **Every one is consistent with the repaired cell** — same
"0/flags=0 from a creator (or a rewriter adopting the reproducible profile,
per item 8 — a creator's rule)" / "copy-forward, clear none, set no other,
from every updater" shape, no contradicting statement of the ignore-lane rule
survives anywhere in the document.

Specifically swept for the *old*, pre-repair three-actor phrasing to see if
it survives anywhere else that also needed fixing:

```
"an updater, appender" -> 0
"updater, appender or rewriter" -> 0
"an updater, appender or rewriter alike" -> 0
```

All zero, confirmed against the non-zero controls above (`updater, appender
and rewriter` -> 1, i.e. the repaired cell itself; `by every updater` -> 2,
i.e. cell + §6.3) so these are true zeros, not broken-search zeros. **No
UNSWEPT_RESTATEMENT of the old defective phrasing** — it existed in exactly
one place (this cell) and the repair replaced it there.

## 15. Rejected candidates

- *Is "0 from a creator" itself under-cited, since §20.2 never states "flags
  = 0" explicitly?* Checked §20.2 in full (§3 above) — it indeed doesn't say
  it, but the cell doesn't cite §20.2 (only "(§6.3)"), and §6.3 and §20.1 both
  do state it plainly ("it writes flags = 0"). Not a defect in the hunk;
  closed.
- *Does dropping "under this text" from the cell let "every updater" be read
  to include a hypothetical updater bound by a future minor-version's own
  text, with different obligations?* Considered at length in §6. Closed: this
  document only ever states rules for actors "under this text" (it has no
  jurisdiction to describe a future text's updaters), so every normative
  sentence in it, this cell included, is implicitly so scoped already; adding
  the words would be redundant here rather than corrective, since (unlike
  §6.3) the cell never introduces the *other*, later-minor-version writer for
  "under this text" to be contrasted against.
- *Is the incompat-lane half of the same cell affected by the hunk, and does
  it now conflict with the ignore-lane half's new wording?* Checked (§7) —
  the hunk's diff context lines show the incompat-lane clause is byte-for-byte
  unchanged, and it names no actor to conflict with the ignore-lane actor
  list.
- *Does the repair overshoot by widening "an" (existential-flavored) to
  "every" (universal) in a way that newly claims something about a fourth
  actor?* Checked against §20.1's exhaustive three-tier taxonomy (§6/§8
  above) — "every updater" is exactly co-extensive with {appender, rewriter};
  no widening beyond the document's own class structure. Closed, not a
  defect.
- *NESTED_DASH anywhere in the hunk?* The cell has zero em dashes. Closed
  immediately.

## 16. Confidence / what a clean area would have needed

Every one of the eight checks was run and its result recorded above (§5–§12),
including the ones that passed (citation resolution, exhaustive-claim,
contradiction, uncovered-sibling, analogy-not-applicable). The one finding I
am reporting (§9) came specifically from doing the document-wide "alike"
sweep the charter's check 1/check 8 asked for, and from reading §6.3's full
paragraph closely enough to see *why* its identical three-noun string
resolves cleanly there (a topic-establishing lead sentence, and a contrasting
second actor) while the cell's copy of the same string has neither. Had I
stopped at "the cell's tokens now match §6.3's tokens, so the repair is
correct" — the natural, shallow check — I would have reported a clean
verdict and missed it; the thing that caught it was reading §6.3 as a whole
paragraph rather than as a phrase to string-match against, and reading every
other "alike" in the document to establish this document's own idiom
convention before judging whether the copied phrase obeys it.
