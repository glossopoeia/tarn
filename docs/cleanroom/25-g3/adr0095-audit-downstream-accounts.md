# Round 26 audit — downstream-accounts role (auditor B)

Charter: hunk-01.diff (§11.1 shrink Rationale) and hunk-02.diff (§23.1
deletion-is-not-erasure). My question is not whether the rewritten passages are
right; it is what elsewhere in the document depended on what they used to say.

## 0. Disclosure

Read, in full or in the ranges named below:

- `/private/tmp/.../r26audit-b/hunk-01.diff` (whole file, 33 lines)
- `/private/tmp/.../r26audit-b/hunk-02.diff` (whole file, ~50 lines)
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — ranges
  45–75, 96–112, 215–235, 553–625, 625–690, 1170–1215, 1288–1325, 1335–1370,
  1440–1520, 1520–1620, 1702–1730, 1745–1800, 1955–1990, 1990–2032, 2030–2060,
  2110–2200, 2895–2937, 2937–3150, 3150–3200, 3200–3300, 3300–3335, 3471–3535,
  3528–3565, 3596–3650, 3650–3730, 3840–3870, 3869–3895, 3890–3975, 4199–4250,
  4263–4405, 4403–4430.

Ran (all against spec/tarn.md only):
- `wc -l spec/tarn.md` → 4474
- `grep -n "^#### 20\.\|^#### 21\.\|^### 20\.\|^### 21\."`
- `grep -n "20\.3"`, `grep -n "11\.1\b\|§11\.1"`, `grep -n "23\.1\|R-PRV-01\|R-PRV-02\|R-PRV-03"`
- `grep -n "shrink\|shrunk\|de-address\|deaddress"`
- `grep -n "slack"`, `grep -n "supersed"`, `grep -n "ancillary"`, `grep -n "R-SER-05"`
- `grep -n "unreachab\|reachability\|erasure\|erase\|logical deletion\|deletion"`
- `grep -n "three way\|three ways\|two ways\|three shapes\|two cases\|three cases\|the other\b"`
- `grep -n "§14 fixes\|what §14\|declarations in a way\|geometry change\|grid count"`
- `grep -n "step 4\|re-declar\|redeclar"`, `grep -n "R-CNF-01"`
- `grep -n "^## \|^### Appendix\|^## Appendix"`
- whitespace-normalised searches (`tr '\n' ' ' | tr -s ' ' | grep -o ...`) for
  "touches the directory", "Where a shrink is permitted…", "A layer whose record
  alone changes…", because the document is hard-wrapped and a line-oriented grep
  for those phrases returns nothing. (`grep -n "directory alone"` returned zero
  hits; the normalised search found it at §11.1 wrapped as "touches the
  directory\n> alone". Any conclusion I drew from a line-grep miss was re-run
  normalised.)

Did NOT read: full.diff, other auditors' hunk files, docs/, PLAN.md,
OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, spec/registry.json, git
history, the web. Did not list the hunk directory (I `cat`'d the two files my
charter names by path, and `mkdir -p`'d the directory before writing this file).

**Unrequested context.** Before I began, my runtime placed in context: a
project-instruction file pointer (CLAUDE.md → AGENTS.md), an index of the
maintainer's private memory notes with several file names and one-line
descriptions, the user's email address, and the current date. None of it is the
specification and none of it is evidence about the specification. I read none of
the files it names and drew no conclusion from it. Disclosed here, not repeated.

## 1. What each repair makes true

**Hunk 1 (§11.1 Rationale, non-normative under [R-CNF-01]).** Rule adopted: a
shrink is barred exactly where it alters what §14 fixes for a tile the layer
stored in the generation the commit supersedes — quantified over that
generation, not the new one — and permitted otherwise; three independent grounds
on which a shrink alters nothing are named (a tile dropped out of the addressed
set; a tile the superseded generation did not store; a new padding position whose
stored byte already holds the fill), and a single shrink may rest on any
combination of them ("One shrink can do several of these at once"). The old text
named two grounds and closed the enumeration ("is the ordinary case, and … is the
other").

**Hunk 2 (§23.1, normative, [R-PRV-01]).** Rule adopted: no commit erases sample
data; it only makes it unreachable. Four tile-level operations do this
(superseding a stored tile's payload, unstoring a tile to the sentinel, a shrink
that de-addresses tiles, a shrink that turns real positions into padding), a
dropped ancillary record's extent goes the same way, and the list is explicitly
open. Disclosure splits two ways, not by operation but by whether the structure
carrying the bytes leaves the live state: if it does, the bytes are slack; if it
does not (the padding case), they sit in a live stored tile and are fill. The old
text said "three ways" and keyed the disclosure split to "the first two" / "the
third".

**The third passage stating the same rule normatively: §20.3 step 4** ([R-WRT-04]),
lines 2996–3070. It is the source, and both hunks defer to it explicitly
("§20.3 states normatively, and governs"; "§20.3 step 4 permits that shrink only
where…"). Its shrink paragraph:

> "An extent MAY also **shrink**, and the bar above is the whole of the test,
> **in the bar's own tense**: a shrink is permitted exactly where it alters
> nothing §14 fixes for any tile the layer stores in the generation this commit
> supersedes."

All three agree on the test and on its tense. §20.3 names two of hunk 1's three
grounds (de-addressing; the fill-padding carve-out); the third — a tile the
superseded generation did not store — is entailed by the bar's quantifier
("the quantifier is the superseded generation's") rather than named. That is an
entailment, not a new rule, and I do not report it. §23.1's "only where those
bytes already hold the channel's recorded fill" is a correct necessary condition
for a carried-forward tile; for a tile this commit stores fresh the constraint
comes from [R-SER-05] rather than from §20.3 step 4, but no sample data is
removed in that sub-case, so the sentence's conclusion stands.

## 2. Citations opened, with verdicts

Both hunks' own citations, and every citation *into* the two passages.

| Citation | Where | Verdict |
|---|---|---|
| §20.3 (hunk 1: "states normatively, and governs") | line 2937 ff. | PASS — §20.3 step 4 carries the bar and its tense. |
| §14 (hunk 1: "what §14 fixes") | §14, line 1798 ff.; enumerated at §20.3 line 3000–3003 | PASS — padding-position set, padding content, decoded size, sample byte offset, codec, filter. |
| "the fill" (hunk 1, case c) | §14.5 [R-SER-05], line 1955; §13.1 [R-TYP-06] | PASS. |
| §11.2 (hunk 1, growth sentence, untouched) | line 1502 | PASS — grid count ⌈Eᵢ/Tᵢ⌉. |
| [R-CNT-17] (hunk 1, untouched) | L21/L22, lines 3494–3495 | PASS. |
| §15.2 (hunk 2: "unstoring a tile so its entry becomes the sentinel") | line 2014, [R-IDX-02] | PASS — "An addressed tile that is not stored has the **sentinel entry**". |
| §20.3 step 4 (hunk 2, twice) | line 2996 ff. | PASS for the disclosure claim; see §1 for the fresh-store nuance. |
| §20.4 (hunk 2: dropped ancillary record's extent) | line 3150; MU=0/PE=0 row line 3174 | PASS — "Retain byte-identical, or drop it — its extent becoming slack." |
| [R-CNT-21] (hunk 2: "remain in the file as slack") | line 630–657 | PASS — "Every byte the live state does not claim is **slack**." The illustrative list after that colon says "everything an earlier commit superseded", which does not literally name de-addressed extents or dropped record extents; the operative clause covers them and §20.3 line 3056 already cites [R-CNT-21] for de-addressed extents. Checked, not a finding. |
| §9.6 (hunk 2: "scans backward for an earlier trailer") | line 1288, [R-LIF-06] | PASS — "probe backward at 64-aligned offsets o for the trailer magic". |
| "which the layer record publishes" (hunk 2) | §13.1 [R-TYP-06], line 1702 | PASS — fill is recorded in the channel entry of the layer record. |
| "no commit removes a layer at all" (hunk 2) | §20.4 line 3179; [R-CNT-22] | PASS — "No commit therefore removes a layer record…". |
| §23.1 cited by §22.3 ("slack is unconstrained and can hold anything") | line 3858 | PASS. |
| §23.1 cited by §23.2 ("a tile unstored by a later commit leaves its earlier payload in the file as slack") | line 3967 | **PASS, and this is the citation the repair fixed.** Under the old three-way list, unstoring was absent from §23.1 and this neighbouring subsection cited it for a case it did not contain. It now lands. |
| §11.1 cited by §7.4's field table | line 1018 | PASS. |
| §11.1 cited by §20.3 ("which is what schema-first creation needs") | line 3023 | PASS — §11.1 still says "A layer that stored nothing may be re-declared freely." |
| §11.1 cited by §13.3's "Note — sparse writing" | line 1789 | **FAIL (incomplete)** — see B-04. |
| §23 cited by §5.2 [R-CNT-21] and by §20.5's closing Note | lines 657, 3333 | PASS. |

## 3. The seven checks, applied outward

**1. Tense and quantifier.** Both repairs speak in the superseded generation's
tense and both say so. §20.3's is the same. §23.2, §21.7, §20.3's Example (c) and
§20.1 are the four downstream passages that speak about the same generations; three
of them are findings below (B-03, B-05, B-02). §23.2 passes.

**2. Citations.** Table above. One downstream failure (B-04).

**3. Normative placement.** Hunk 1 is a Rationale and therefore carries no force —
but the rule it states is stated normatively at §20.3 step 4, which I opened and
quoted, so this is a Rationale tracking a live normative rule, not a rule stranded
in a blockquote. Hunk 2 is normative prose closed by [R-PRV-01]; its MUST NOT is
outside any ">" block. I grepped the distinctive words of both rules — "shrink",
"de-address", "padding position", "sentinel", "supersed" — and placed every hit.
Passes.

**4. Contradiction in the same structure, including untouched text.** This is where
the real finding is: **B-01**. §20.3 step 4 contains two clauses that give opposite
answers for the one shrink case both repairs now certify as standing alone.

**5. Exhaustive claims.** Hunk 2's "Those two cases are exhaustive" — I tried to
falsify it by walking every claimant class of [R-CNT-02] (stored-tile extent,
record extent, directory, trailer) and every commit operation §20.3/§20.4 permit.
Every route puts the bytes either into slack or into a live stored tile's padding.
I could not falsify it. Hunk 2 also explicitly de-closes the operation list ("not
offered as closed"), which is the right hedge and matches §20.3's own "the list is
not offered as exhaustive" for growth. Hunk 1 carries no such hedge and its
three-item list reads as closed; I tried to find a fourth ground and could not — a
shrink changes only Eᵢ, hence only grid counts and the padding-position set; P=∏Tᵢ,
sample byte offsets, codec, filter and filter 2's mandated stride (T26: element
size / sample stride Q / identity) are all independent of Eᵢ, so §20.3's other
carve-out (an identity-stride filter, [R-COD-10]) cannot be reached by a shrink.
Hunk 1's closure is therefore sound for shrink. Not a finding.

**6. What the structure leaves unconstrained.** The structure hunk 1 governs is a
permitted shrink of a layer. Its quantities: (i) the addressed-tile set and with it
entry_count, extent_length and the tile-index region; (ii) the padding-position set
of surviving stored tiles and the content [R-SER-05] fixes there; (iii) the
de-addressed tiles' bytes; (iv) the layer record's own extent fields; (v) the slab
run partition / alignment invariant. (iii) is pinned ([R-CNT-21], §20.3 line 3056).
(v) is pinned ([R-SLB-04] "changes the stored-tile set, the run partition, or the
byte placement"; [R-SLB-01]; cited at §20.3 line 3067). (ii) is pinned by the
carve-out. **(i) is pinned only for the de-addressing kind of shrink.** That gap is
B-01, and it is the sibling-quantity shape the charter names: the repair certified
the padding ground and left that ground's index consequence unstated, while its
de-addressing sibling three lines away is fully stated and its growth sibling three
sentences up in §11.1 has an explicit dichotomy.

**7. Argument by analogy.** Hunk 1: "permitted here exactly as it is there" does not
appear in the hunk — that phrase is §20.3's, untouched. Hunk 1's only warrant clause
is "§20.3 states normatively, and governs". Compared word for word: hunk 1's
governing verb is "**stored** tiles in the generation a commit supersedes" / "a tile
the superseded generation did not **store**"; §20.3's is "any tile the layer
**stores** in the generation this commit supersedes". Same verb, same generation,
same per-tile individuation. Passes. Hunk 2's analogy is "a shrink reported as
erasure misleads **exactly as** a supersede so reported does" — governing verbs:
"makes sample data unreachable" (the MUST NOT's subject) against "removes only from
*reachability*" (the paragraph's opening). Both range over commits, not over tiles,
so the analogy carries one relation over one set. Passes. Hunk 2's second analogy,
"goes the same way" for a dropped ancillary record's extent, ranges over record
extents rather than stored-tile extents; the shared predicate is "becomes slack",
which §20.4's MU=0/PE=0 row states in those exact words ("its extent becoming
slack"). Passes.

## 4. Downstream passages examined, one by one

Verdicts: **still correct**, **now false**, **now incomplete**.

1. **§23.2** (line 3960 ff.), the neighbouring subsection. "a tile unstored by a
   later commit leaves its earlier payload in the file as slack (§23.1)".
   **Still correct — and repaired by hunk 2.** This was the passage citing §23.1
   for a case the old list did not contain.
2. **§20.1 writer tiers** (line 2905). "appender — extends an existing file by
   commits (§9.2): adding layers or records, superseding tiles, growing extents,
   amending metadata." **Now incomplete** → B-02.
3. **§21.7** (line 3703). "a commit that supersedes every tile it would have
   damaged leaves the live state clean". **Now incomplete** → B-03.
4. **§13.3 "Note — sparse writing"** (line 1786). **Now incomplete** → B-04.
5. **§20.3 Example (c)** (line 3131). "A fill change on a layer that **stores** a
   tile carrying either…"; "A layer **storing** no tile is re-declared freely".
   **Now incomplete / tense-unswept** → B-05.
6. **§20.3 step 4, lines 2993 and 3056.** **Contradiction** → B-01.
7. **§20.3 "Example — the three shapes a commit takes"** (line 3096). Checked
   whether the repaired §23.1's unstoring and de-addressing operations are placed
   by one of the three shapes. Shape (b)'s prose is "That layer's index is
   re-emitted whole; a commit that supersedes stored tiles takes the same shape,
   hatching the superseded payloads as well" — an unstoring commit and a
   de-addressing shrink both re-emit the index whole and hatch the payload, so
   (b) accommodates them even though its heading names only "tiles added". The
   closing claim "In every shape the file grows and no committed byte changes"
   holds for both. **Still correct.** Not reported; the one genuine gap here (the
   padding-only shrink, which is directory-confined and absent from (c)'s three
   examples) is B-01's subject and I do not double-count it.
8. **§5.1's "Example — a file after three commits"** (line 585). "A commit that
   changes a layer's stored-tile set **or index content** re-emits that layer's
   whole tile-index region as well" — the full trigger, matching §20.3.
   **Still correct.** This is what makes §13.3's shorter trigger (B-04) an outlier
   rather than the document's settled phrasing.
9. **§20.5 and its Note** (lines 3200, 3331). "Compaction is the only true removal:
   logical deletion supersedes bytes but leaves them in the file as slack" and "This
   is the only operation that reclaims slack". Checked against §23.1's second
   paragraph ("Compaction (§20.5) is the only operation that removes slack").
   **Still correct.** Also checked that compaction preserves hunk 2's case-2 bytes:
   [R-WRT-07] carries "every stored tile's bytes verbatim", so the padding content
   survives compaction — consistent with §23.1 not claiming compaction reaches it.
10. **§22.3 [R-SEC-03]** (line 3855). "every byte a reader can reach belongs to one
    named structure… slack is unconstrained and can hold anything (§23.1)". Checked
    against hunk 2's case 2, where the bytes sit inside a live stored tile rather
    than in slack: those bytes are inside a named structure and are never returned
    ([R-GEO-04]), and hold fill, so nothing here is disturbed. **Still correct.**
11. **§22.3's "Four residues are stated rather than defended"** (line 3869). A count.
    Enumerated: slack under no checksum; an unassigned record type's extent; a
    trailer-mimicking payload; a user-metadata extent under an unassigned encoding.
    Four. Neither hunk touches this set. **Still correct.**
12. **§21.6's rows** (line 3601 ff.). The sentinel row and the [R-CNT-21] slack row
    are the two that bear on hunk 2. Both read the same under the repaired text.
    **Still correct.**
13. **§21.4 T4/T5** (lines 3538–3539) and **§21.3 L21/L22** (3494–3495). These are
    the witnesses for the two quantities B-01 turns on, and I used them for the
    byte-level test. T4: "A padding position does not encode… that channel's
    recorded fill value" — verifier, certification. L21: "entry_count does not equal
    the geometry-derived addressed-tile count". **Still correct.**
14. **Appendix H's updater and verifier checklists** (lines 4418–4474). No count of
    removal operations; nothing keyed to §23.1's old "three". **Still correct.**
15. **Appendix D's "Six choices"** and **Appendix G's ten items**. Counted; unrelated
    to either hunk. Appendix G item 6 ("the sentinel for every all-fill tile")
    checked against hunk 2's case 2 — a profile writer would not store an all-fill
    tile at all, which does not disturb the case. **Still correct.**
16. **[R-SLB-04]** (line 2183). "changes the stored-tile set, the run partition, or
    the byte placement of any run" — a shrink changes the run partition, so a
    shrink is covered. **Still correct**; §20.3 line 3067 cites it.
17. **§9.6 [R-LIF-06]** and **§9.7 [R-LIF-08]**. Backward probe and coverage walk.
    **Still correct.**

## 5. Findings

### B-01 — §20.3 step 4 contradicts itself for the one shrink case both repairs certify as standing alone (BYTE-LEVEL)

§20.3 step 4 contains, in the same numbered step, both:

> "A layer whose record alone changes keeps its extent slot, pointing at the
> existing region, as does a layer the commit leaves untouched (`[R-WRT-05]`);
> relocating a live index region is compaction's operation (§20.5,
> `[R-WRT-07]`), not an appender's." (line 2993)

and

> "Where a shrink is permitted the de-addressed tiles' extents become slack
> (`[R-CNT-21]`), `[R-CNT-17]` obliges the smaller entry_count and so a
> re-emitted index region, and every surviving stored tile is untouched."
> (line 3056)

Hunk 1 now states the fill-padding ground as one of three independent grounds and
adds "One shrink can do several of these at once" — which entails that a shrink may
rest on that ground alone. Hunk 2 states the same case as a case in its own right:
"**Where it does not** — a shrink turning real positions into padding of a tile the
new state still stores".

Instantiate it. E = 1000, T = 256, so G = ⌈1000/256⌉ = 4 and coordinates 1000–1023
are already padding. Shrink E to 999: G = ⌈999/256⌉ = 4, unchanged. Coordinate 999
becomes a new padding position; §20.3 permits the shrink iff its stored byte already
holds the fill. No tile is de-addressed. N is unchanged, so the addressed-tile count
is unchanged, so [R-CNT-17] obliges the *same* entry_count, and §20.3's own
re-emission trigger — "Every layer whose stored-tile set or index content this commit
changes has its tile-index region re-emitted in full" — is not tripped. The layer's
record alone changes.

So the first clause says keep the extent slot and re-emit the directory alone; the
second says re-emit the index region. They cannot both be followed. Worse, the second
clause's "the smaller entry_count" is not merely inapplicable here — a writer that
took it literally would emit entry_count < N and fire L21.

Note the asymmetry the repair left standing. Three sentences above hunk 1's edit, in
the very Rationale it landed in, growth gets an explicit dichotomy: "Growth that
leaves every grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) unchanged touches the directory alone;
growth that raises one changes entry_count and with it extent_length
(`[R-CNT-17]`)…". The shrink counterpart of that dichotomy is stated nowhere — not in
§11.1, not in §20.3, not in §20.3's shape Example, whose (c) lists "clearing a slab
declaration, renaming a layer, or changing a channel's fill value on a layer with no
padding position and no pad bit" and does not include a shrink within a grid count. A
whitespace-normalised search for "touches the directory" finds exactly one hit, the
growth sentence.

Repair: split §20.3's consequence sentence the way §11.1 splits growth — "A shrink
that leaves every grid count unchanged touches the directory alone, its layer keeping
its extent slot; where a shrink de-addresses tiles their extents become slack
([R-CNT-21]), [R-CNT-17] obliges the smaller entry_count and so a re-emitted index
region" — and add the shrink counterpart to §11.1's growth dichotomy.

Byte-level: **yes**. Writer A follows line 2993 and emits a directory-only commit,
extent slot unchanged. Writer B follows line 3056 and re-emits the index region at a
new placement (at the correct, unchanged entry_count — the smaller one is barred by
L21). The two files differ in bytes: B's carries a second copy of the index region
and a re-pointed extent slot, and B's F is larger. Both files are conforming: no
§21.2–§21.5 row fires on either, and [R-WRT-04]/[R-WRT-05]'s placement obligations
have no file-level witness (§21.7 is explicit that history properties are not
reconstructed by §9.7). So the disputed file is conforming and only one reading
permits an appender to produce it — the emittable set moves.

### B-02 — §20.1's appender tier still enumerates the pre-repair operation set

> "- **appender** — extends an existing file by commits (§9.2): adding layers or
> records, superseding tiles, growing extents, amending metadata." (line 2905)

Four operations, of which exactly one — superseding tiles — appears in the repaired
§23.1's list of five. Shrinking extents is absent although §20.3 step 4 says "An
extent MAY also **shrink**"; unstoring a tile is absent although §20.3 step 4 says
"entries for tiles that become unstored written as the sentinel" and hunk 2 now names
it as an operation in its own right; dropping a droppable record is absent although
§20.4's table licenses it and hunk 2 names it. This is normative prose, not a Note.

Not false as written — the bullet carries no BCP 14 keyword and no "only" — but it is
the document's one summary of what an appender does, it is where an implementer looks
first, and it now disagrees with the repaired normative account two subsections later.

Repair: "…adding layers or records, superseding or unstoring tiles, growing or
shrinking extents, dropping a droppable record (§20.4), amending metadata."

Byte-level: no. The bullet states no requirement and grants no permission; §20.3's
explicit "MAY also **shrink**" governs, and a file produced by a shrinking or
unstoring commit is conforming under both readings.

### B-03 — §21.7's unwitnessed-bar sentence names only supersession

> "And a commit that supersedes every tile it would have damaged leaves the live
> state clean, so the bar is unwitnessed there for the same reason `[R-LIF-01]` is:
> it is a property of the prior generation, which §9.7 does not reconstruct" (line
> 3703)

§20.3 names three routes to a clean live state, not one: superseding ("superseding
every tile of a layer and re-declaring it are one operation, and this bars it"),
unstoring ("Unstoring that tile in the same commit does not rescue it either"), and
de-addressing ("a shrink that alters what §14 fixes for a tile stored there is barred
whether or not the new state still stores it"). The repaired §23.1 now names all
three as distinct operations, which is what makes §21.7's single-route sentence
visible as short. §21.7's own general clause earlier in the paragraph — "witnessed
only where the affected tiles remain stored" — is correct and complete; it is the
worked example that under-enumerates, and §20.3 line 3053 points at §21.7 by name
("§21.7 records the consequence"), so the pointer lands on a passage covering one of
the three cases it was written to cover.

Repair: "a commit that supersedes, unstores or de-addresses every tile it would have
damaged leaves the live state clean".

Byte-level: no. §21.7 describes what has no witness; it assigns no obligation and no
register row. Under both readings the same files verify and the same files are
emittable.

### B-04 — §13.3's sparse-writing Note states the index re-emission trigger short, and cites §11.1 for it

> "each commit that changes a layer's stored-tile set, or that grows its extents
> across a grid boundary, re-emits that layer's whole tile-index region (§11.1,
> §20.3, `[R-WRT-04]`)." (line 1786)

The normative trigger is "stored-tile set **or index content**" (§20.3 line 2984),
and §5.1's Example states it in those words. A shrink that de-addresses only tiles
that were already sentinels changes neither the stored-tile set nor grows any extent,
yet entry_count falls, so [R-CNT-17]/L21/L22 oblige a re-emitted index region. Hunk 1
is what makes this case reachable in plain sight: its new second ground, "a tile the
superseded generation did not store carries none either", is exactly the licence to
de-address unstored tiles.

The citation is also wrong on its own terms: it sends the reader to §11.1 for the
index-re-emission rule, and §11.1 — after the repair as before it — states that
consequence for **growth only**. The repair added three shrink grounds to that
Rationale without adding the shrink counterpart of its index sentence (see B-01).

Repair: "each commit that changes a layer's stored-tile set or its index content".

Byte-level: no. The correct rule is stated normatively in §20.3 and a file with
entry_count ≠ the geometry-derived count fires L21 under either reading, so
[R-CNF-05] bars it both ways.

### B-05 — §20.3's shape (c) Example restates the free-re-declaration permission without the tense the repair turns on

> "A fill change on a layer that **stores** a tile carrying either is not an
> appender's operation at all (step 4): it would invalidate every stored tile it
> reaches. A layer **storing** no tile is re-declared freely, subject to every rule
> its new geometry is subject to, which is the same step's permission." (line 3131)

The normative sentence it restates carries the tense explicitly and warns against
dropping it:

> "A layer that stores no tile **in the generation this commit supersedes** MAY be
> re-declared freely, which is what schema-first creation needs (§11.1) — the tense
> is the bar's, so a commit does not earn this permission by emptying the layer as
> it re-declares it" (line 3021)

Hunk 1's counterpart sentence is in the past tense and is right: "A layer that
**stored** nothing may be re-declared freely." The Example's present participle
admits precisely the reading §20.3 forecloses — a commit that unstores every tile as
it re-declares the layer — and §20.3's "a commit does not escape this by unstoring in
the same breath" is the sentence that bars it. Hunk 2's newly explicit "unstoring a
tile so its entry becomes the sentinel" as a first-class operation is what makes the
Example's ambiguity newly load-bearing: the reader now has a named operation to
plug into it.

Repair: "A layer storing no tile **in the generation the commit supersedes** is
re-declared freely".

Byte-level: no — but narrowly. The file at issue (a layer re-declared while every one
of its tiles is unstored in the same commit) is conforming: all entries are sentinels,
no T-row fires, entry_count matches the new geometry. Under the Example's reading a
writer may emit it; under §20.3's it MUST NOT. What keeps this off the byte-level list
is [R-CNF-01]: the Example is non-normative and cannot license anything, and the
normative sentence resolving it sits ten lines above and names this exact misreading.
Two competent implementations should not diverge here. It is still a restatement the
tense-sensitive repair should have swept.

## 6. Checks that passed with nothing to report

- Hunk 2's "Those two cases are exhaustive" survived every falsification attempt
  (§5 above).
- Hunk 1's three grounds are complete for shrink (§5 above); [R-COD-10]'s
  identity-stride carve-out is unreachable by a shrink, so its omission from the
  Rationale is correct rather than an undershoot.
- Every citation into §11.1 and §23.1 resolves except §13.3's (B-04).
- No count elsewhere in the document still matches an old number: I searched for
  "three ways", "two ways", "two cases", "three cases", "the other" and placed
  every hit; none refers to either repaired passage. The two counts that do sit
  near this material — §22.3's "Four residues" and §21.6's two closing "two"s —
  are about other sets and are unaffected.
- Neither repair overshot. Hunk 2 widened the operation list and immediately hedged
  it open; hunk 1 widened a closed two-item list to three and added the
  "several at once" clause, both of which §20.3 already supported.
