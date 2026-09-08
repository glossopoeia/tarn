# Cross-hunk consistency audit — round 32 (25 hunks, one decision record + one next-day restructure)

## 0. Disclosure

Read: all 25 hunk files in
/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit/case/
(hunk-01.diff … hunk-25.diff) and /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md.
NOT read: full.diff, docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md,
conformance/, spec/registry.json, git history, the web.

I ran `ls -la` on the case directory before I had read the brief's "do not list
that directory" line. The listing showed 26 files: full.diff plus hunk-01..25.
I did not open full.diff. Disclosed as a breach; nothing in it informed a finding
beyond confirming the hunk count the brief already stated.

Context I did not ask for and did not use: a CLAUDE.md/AGENTS.md pointer, a
user auto-memory index naming TARN-specific memory files, an environment block
naming five recent commit subjects (which name ADR numbers and a prior audit's
defect count), and an MCP server instruction block. None of it is the
specification. I disregarded all of it; where the environment block named
things that look like answers (a "PE = 0 licenses the drop" commit subject,
an "ignore-lane flag bit" commit subject, a "de-addresses its tiles" commit
subject) I deliberately re-derived every claim from spec/tarn.md and the hunk
bodies, and no finding below rests on those subjects.

Wrote:
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit/scratch/cross-hunk/nsearch.py
  (whitespace-normalising, blockquote-marker-stripping search over spec/tarn.md,
   returning source line numbers)
- this file.

Hunk header check: every hunk header's "nearest preceding heading" matched the
body I found at the stated lines. No mismatch to report.

## 1. Grouping (worked out from the text, not from headers)

**Group A — the §14 bar and the bar beside it (hunks 5, 10, 11, 12, 13, 14, 15, 16;
§11.1 Rationale + §20.3 step 4).**
Hunk 11 widens the bar's subject clause and its list; hunk 12 rewrites the gloss;
hunk 13 inserts a whole new paragraph (tile extents / dimension order) and rewrites
the ordinal bar's ground; hunks 14, 15, 16 touch the restatements; hunk 10 widens
the re-emission parenthetical; hunk 5 restates the whole case in §11.1's
**Rationale.** block.

**Group B — "stored byte" widened to "or bit in a packed plane" (hunks 5, 12, 15, 16, 24).**
Five landings, at L1642, L3207, L3293, L3328, L4263. Warrant is §14.5/[R-SER-05]
("the fill bit in a packed plane"), which already covered it. All five agree.

**Group C — occasions for a renumbering (hunks 10, 13).**
Parenthetical at L3177, gloss at L3252.

**Group D — the "top-level" qualifier (hunks 1, 21), against §21.6's closing paragraph.**

**Group E — resource declines and the partial total (hunks 2, 4, 21), against
[R-CNF-11], [R-MTA-09], §21.6's document row, and §21.6's opening sentence.**

**Group F — [R-SER-08]'s one resolved byte (hunks 7, 8, 19), against §12.3
[R-TYP-04] and Appendix H's reader checklist (untouched).**

**Group G — flags (hunks 3, 25), against [R-CNT-08] and [R-CNF-02].**

**Group H — record persistence and the drop licence (hunks 9, 17, 18, 20, 25),
against §20.4's table, [R-WRT-01], [R-WRT-03], [R-CNT-14], [R-CNT-18].**

**Group I — standalone (hunks 22, 23).**

## 2. Force test — label, not marker ([R-CNF-01])

| passage | block | label | force |
|---|---|---|---|
| §11.1, L1628–1662 (hunk 5) | `>` blockquote | **Rationale.** | NON-normative |
| §20.3 step 4, L3183–3345 (hunks 9–16) | plain numbered list | none | NORMATIVE |
| §20.3, L3400–3440 (hunk 17) | `>` blockquote | **Example — the three shapes a commit takes.** | NON-normative |
| §20.4 table, L3462–3466 (hunk 18) | plain table, no `>` | none | NORMATIVE |
| §6.2 trailer table (hunk 3) | plain table | none | NORMATIVE |
| §21.6 table (hunk 20) | plain table | none | NORMATIVE (but §21.1: the rule governs on divergence) |
| §21.9 (hunks 21, 22) | plain prose | none | NORMATIVE |
| §5.2, §9.7, §14.2, §19.4, §21.1, §22.3, §23.1, §2.3 | plain prose | none | NORMATIVE |
| Appendix H (hunk 25) | heading says "(non-normative)" | — | NON-normative |

So hunk 5's and hunk 17's edits carry no force; hunk 18's table edit does.

## 3. Searches run (all through nsearch.py, which strips leading "> " and
normalises whitespace, so wrapped phrases match)

```
  1  'An extent MAY also **shrink**'  lines=[3306]
  1  'an extent MAY **grow**'  lines=[3289]
  4  'the coordinate'  lines=[3187, 3194, 3204, 3238]
  5  '§14 fixes'  lines=[1634, 3186, 3271, 3313, 3324]
  8  'the §14 bar'  lines=[1633, 1647, 3249, 3282, 3306, 3326, 3332, 3336]
  3  '§14 obligation'  lines=[1639, 3266, 3316]
  3  'geometry change'  lines=[3177, 3246, 3252]
  2  'unknown critical'  lines=[3464, 4802]
  1  'sole resolved byte'  lines=[4779]
  0  'the one byte'  lines=[]                       <- swept by hunks 8 and 19
  1  'Whichever source governs'  lines=[3459]
  0  'Stored flags'  lines=[]                       <- swept by hunk 18
  1  'Governing flags'  lines=[3462]
  1  'permitted outright'  lines=[1651]
  1  'an empty directory is a conforming generation'  lines=[1037]
  4  'dimension order'  lines=[371, 1650, 1727, 1749]
 16  'tile extents'  lines=[454,1020,1649,1686,1726,2047,2081,2139,3235,3241,3750,3775,3810,4688,4691,4694]
  0  'ZZZ-CONTROL-ABSENT'  lines=[]                 <- CONTROL: the tool can return 0
  7  'renumber'  lines=[120,122,1662,3178,3252,3782,4350]
  2  'the narrowest scope'  lines=[2713, 4072]
  3  'top-level MU = 1'  lines=[3464, 4080, 4804]
  5  'bit in a packed plane'  lines=[1642, 2132, 3207, 3293, 3328]
  4  'already holds the fill'  lines=[1642, 3207, 3293, 3328]
  1  'or bits in a packed plane'  lines=[4263]
  0  'hold the fill' / 'held the fill' / 'holding the fill'
 21  'padding position'  (21 hits, listed in working notes)
 15  '`[R-COD-06]`' ; 12 '`[R-ERR-04]`' ; 6 '`[R-MTA-09]`' ; 10 '`[R-CNT-14]`' ;
 10 '`[R-CNT-18]`' ; 16 '`[R-CNT-15]`'
```

Controls proving the zeros: `ZZZ-CONTROL-ABSENT` = 0 against `tile extents` = 16
(which includes L1649, inside the `>`-prefixed **Rationale.** block, and L4688–4694
in an appendix), and `the one byte` = 0 against `sole resolved byte` = 1 at L4779
(same appendix, same subject matter) — so the zero for `the one byte` is a real
absence and not a search that could not reach the appendix.

## 4. Findings — per hunk group

### Group A. The §14 bar

The rule hunk 11 adopts: a commit may not change a layer's declarations so as to
alter, for a tile stored in the superseded generation, (i) what §14 fixes for its
stored bytes or how they decode, **or (ii) the coordinate §11.4 assigns any value
they decode to.** Limb (ii) is new.

The rule hunk 13's new paragraph adopts: changing a layer's declared tile extents,
or the declared order of its dimensions, is such a change wherever the layer stores
any tile, because those two declarations "are what fix the coordinate each stored
value denotes".

**A.1 — limb (ii) destroys the shrink permission (X-01).**
§3.1 defines *coordinate* as "a d-tuple (x₀, …, x_{d−1}), in declared dimension
order, **with 0 ≤ xᵢ < Eᵢ**, identifying one sample position of a layer with
extents (E₀, …, E_{d−1})". §11.4's ordinals use Gᵢ = ⌈Eᵢ/Tᵢ⌉. The **extents** are
therefore a determinant of the coordinate, on both the §3.1 definition and the
§11.4 arithmetic. A shrink changes the extents. So limb (ii) reaches every shrink
of a layer that stores a tile — and the same step says at L3306 "the §14 bar is
**the whole of the test** of what a shrink alters" and at L3313 "An extent MAY also
**shrink**". Under limb (ii) read plainly, no shrink of a non-empty layer is ever
permitted, and L3336–3345 ("Where a shrink is permitted the de-addressed tiles'
extents become slack…") describes an empty case. Hunk 13's gloss — "they are what
fix the coordinate each stored value denotes" — is the only thing narrowing limb
(ii) to the tile extents and dimension order, and neither §11.4 nor §3.1 supports
excluding the extents. Two repairs in the same step bound the same limb by
different properties. Direction: hunk 11's limb needs the qualifier hunk 13's gloss
is trying to supply, stated in the bar itself (evaluate the coordinate at the disk
ordinal the re-emitted index assigns the tile; the extents move a tile's ordinal,
never the coordinate its values denote).

**A.2 — the bar now reaches past "what §14 fixes", and every shorthand still says
"what §14 fixes" (X-02).**
`§14 fixes` occurs 5×: L3186 (the bar itself, now two limbs), and four
restatements — L1634 (hunk 5), L3271 (hunk 14, edited this commit), L3313
(untouched), L3324 (untouched). Plus three `§14 obligation` at L1639, L3266, L3316.
L3313 is exhaustive — "A shrink is permitted **exactly where** it alters nothing
§14 fixes for any tile the layer stores in the generation this commit supersedes" —
and four lines later L3326 (hunk 16, edited this commit) says "What counts as such
an alteration is **the §14 bar and nothing else**". Since hunk 11 made the bar
strictly larger than "what §14 fixes", those two sentences now state different
tests in one paragraph. Hunks 14 and 16 were both edited in this commit and both
kept the narrow formula.

**A.3 — the ordinal bar's ground went circular and lost its exhaustive quantifier (X-06).**
Before: "the re-emission rule above, whose **only stated occasion** for a
renumbering **is** a geometry change." After (hunk 13): "whose **stated occasions**
for a renumbering **are** a geometry change **and a permitted change to a planar
layer's channel declarations**." The ground for barring an ordinal-moving channel
change was that such a change is not an occasion at all. Now the occasions include
"a *permitted* change to a planar layer's channel declarations" — permitted meaning
not barred by the bar this sentence is grounding — and "only" is gone, so the list
no longer excludes anything. The bar's own MUST NOT (L3253–3257) is unaffected;
its stated ground is.

**A.4 — "the geometry changes this step permits" is not exhaustive (X-07).**
"An extent's growth and shrink, below, are the geometry changes this step permits."
§11.1 puts a dimension's **name** and the layer's **rank** among the geometry
fields ("The owning scope of a layer's geometry and linearization fields is the
layer. A layer has rank d ≥ 1; each of its d dimensions has a name (§4.6), an
extent Eᵢ ≥ 0, and a tile extent Tᵢ ≥ 1"). A dimension rename touches no stored
byte, no decode, no coordinate and no ordinal, so neither bar reaches it — yet this
sentence says it is not permitted. And L3286 permits a layer that stored no tile to
be "re-declared **freely**", which is every geometry change there is.

**A.5 — hunk 5's "permitted outright" against hunk 15's proviso (X-08).**
Hunk 5 (Rationale, no force): "A growth is permitted **outright**".
Hunk 15, same commit, normative: "…this is an exception the permission states
rather than one the carve-out supplies. **It holds provided** the grown geometry
stays within every bound the layer's own declarations impose, `[R-COD-07]`'s lz4
decoded-size cap among them (L44)".

**A.6 — anaphor (X-13).** Hunk 13's inserted paragraph sits between "Such a change
is a new layer, or a whole-file rewrite under a fresh file_id" and "One effect is
barred beside **it**". Before the insertion the nearest antecedent for that "it"
was the §14 bar. Now the nearest noun phrases are "the geometry changes this step
permits", "this step", "the re-type's [escape]". (The second "it" in the same
sentence — "the §14 bar does not reach it" — is the effect, not the bar, which
makes the first one harder still.)

**Back-references checked and unaffected in Group A:** "such a tile" at L1634
(→ a tile of a layer that already stored tiles in the superseded generation,
unchanged); "the other bar" at L1653 (→ the planar-ordinal bar, unchanged);
"the bar beside this one" at L3318 (→ the ordinal bar, unchanged); "as it is there"
at L3330 (→ the growth carve-out passage above, unchanged); "As there" at L3269
(→ the shrink passage below, unchanged — a forward "there", but the sentence names
it); "its padding limb" at L3292 (hunk 15's own insertion; resolves to the §14
bar's carve-out named in the previous sentence, correct).

### Group B. "or bit in a packed plane"

Warrant: §14.5/[R-SER-05], L2129–2133 — "at every padding position, a writer MUST
encode, for each channel the position carries, that channel's fill value — … **the
fill bit in a packed plane**." All five landings agree with it and with each other.
Hunk 24's variant ("bits in a packed plane", plural, matching its plural "bytes")
is the only wording difference and is correct in its sentence. **No finding.**
Note for the record: the phrase landed 3× in §20.3 step 4 (L3207, L3293, L3328),
1× in §11.1's Rationale (L1642) and 1× in §23.1 (L4263). I searched for a fourth
step-4 site with the old wording — `holds the fill`/`hold the fill`/`held the
fill`/`holding the fill` return 4/0/0/0 and all four are the swept ones — so
nothing in the step was left behind.

### Group C. Renumbering occasions
Hunk 10 (L3177) and hunk 13 (L3252) agree word for word: "a geometry change" +
"a permitted change to a planar layer's channel declarations". See A.3 for the
consequence.

### Group D. "top-level"
Hunk 1 (§2.3, L179): "carrying no **top-level** record of a type it does not
implement with MUST_UNDERSTAND = 1".
Hunk 21 (§21.9, L4079): "a foreign format major and an unimplemented **top-level**
MU = 1 type".
§21.6's closing paragraph (untouched, L3952): "an **experimental-range top-level
record type carrying MU = 1** … The qualifier is load-bearing — the same type as a
layer sub-record is reject-layer and never a ground to refuse the file
(`[R-CNT-18]`)".
[R-CNT-18] (L1138): "an unknown sub-record type with MU = 1 is reject-layer, and
where the file is otherwise conforming a reader **MUST NOT reject the file for it**".
[R-CNT-15] (L1052): "An unknown record type **at file scope**: MU = 1 → reject-file".
§2.4's reject-layer row: "all other layers are unaffected".
All consistent. The §2.3 verifier sentence at L222 ("when a record carries
MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)") correctly carries
no "top-level" qualifier, because *cannot establish* arises at either scope.
**No finding.** Checked exhaustive claim: "**the two** capability refusals §21.6's
closing paragraph names" — §21.6's closing paragraph opens "**Two** structural cases
are conforming files a reader nevertheless refuses" and names exactly two. Passes.

### Group E. Resource declines and the partial total

Hunk 21's rule: a reader may decline a file exceeding a §21.9 guarantee at the
whole file, at the narrowest offending scope (a layer, a tile, or a user-metadata
record), **or at any scope containing the narrowest one.**
Hunks 2 and 4's rule: a verifier that "declined a scope on resource grounds" has
not completed its walk and MUST report the slack total as partial.

**E.1 — a decline at two of the three scopes does not stop the walk (X-04).**
§9.7's walk reaches "the stored extent of each non-sentinel tile-index entry" and
"each record's extent" — from the index entry and the extent slot, not from
decoding. Declining a **tile**'s decode, or taking ignore-record on a
**user-metadata record** ([R-MTA-09] / §21.6's row), leaves every claimant
enumerable. Only a layer-level decline blocks enumeration. So hunks 2 and 4 force
"partial" on a total that is exact.

**E.2 — hunk 4's insertion collides with an untouched MUST four sentences above (X-05).**
§9.7, untouched, L1490: "**A verifier decodes every stored tile**, whatever content
obligations §14 places on the layer: §21.4's codec rows are file-conformance
violations, and a verifier MUST NOT certify past a violation it has not looked for."
Hunk 4 inserts into the same paragraph "the verifier declines a scope on resource
grounds (`[R-ERR-04]`)". [R-CNF-11] does license the decline (with *cannot
establish*), so the licence pre-existed — but the repair put it in the same
paragraph as the flat "decodes every stored tile" and reconciled nothing.

**E.3 — hunk 21's "which is" hardened a list into a false claim (X-09).**
"the narrowest scope whose stated or derived quantities exceed what it can serve,
**which is** a layer, a tile, or the record carrying a user-metadata document".
Two of §21.9's own eight rows — *layers per file* and *size of the directory
region, dir_length* — have the **file** as their narrowest offending scope. The
pre-repair colon read as a loose apposition; "which is" asserts.

**Citations checked in this group:** `[R-COD-06]` — L2473: "a wider window is
conforming and merely permits a conforming reader to decline **the tile or the
layer** on resource grounds (`[R-ERR-04]`)". PASSES: it does provide for a
containing scope. `[R-CNF-11]` — L222: "when it declines **a layer's or a tile's**
decode on resource grounds". PASSES as a presupposition. `[R-ERR-04]` from §5.2 and
§9.7 — PASSES (it is the resource-decline rule). `[R-CNT-21]` from §9.7 — PASSES
("governs what such a total counts and what the verifier reports beside it";
[R-CNT-21] states both). §18.2 from §21.9 — PASSES (§18.2 L2713 assigns
ignore-record as the narrowest scope for a document).

### Group F. [R-SER-08]'s one resolved byte

Hunk 7 (§14.2, normative): "MUST **return** 0x00 as false and every other byte as
true — the value, encoded 0x00 or 0x01 as above, and not the stored byte."
Hunk 8 (§19.4 step 8, normative): "`[R-SER-08]` fixes what a reader returns for
**a** byte a conforming file cannot carry".
Hunk 19 (§21.1, normative): "`[R-TYP-04]` (§12.3) makes it **the one case where a
reader resolves a byte rather than serving it through**."
Citation check: §12.3 [R-TYP-04], L1842: "**the one case where a reader resolves a
byte to a value rather than passing it through** arises only in a nonconforming
file, and `[R-SER-08]` states it." PASSES, near word for word.
Appendix H, L4779, **untouched**: "returns sample bit patterns unaltered (§3.2),
**the sole resolved byte** (`[R-TYP-04]`, §12.3) being a nonconforming interleaved
boolean…" — the pre-repair singular-byte framing, twelve lines above the paragraph
hunk 25 edited. **(X-10)**
Check 6 on hunk 7 — siblings of the interleaved bool value byte: the bool **fill**
byte (§13.2, [R-TYP-07], reject-layer — the §14.2 Note names it), **pad bits**
(§14.3, no illegal value exists), packed-plane bits (no illegal value), and the
same byte at a **padding position** (T2's row assigns it to T4, and [R-GEO-04] bars
returning it). All governed. No unconstrained sibling.

### Group G. Flags

Hunk 3's trailer cell against [R-CNT-08] (L2..L881) and F19 (L3757):
"bits 0–15 (incompat lane) all zero, a set bit being reject-file (F19)" — F19 reads
"Any bit of the flags incompat lane (bits 0-15) is set; this text defines no flag
bits, so every such bit is unimplemented | reader | open | `[R-CNT-08]`". PASSES.
"bits 16–31 (ignore lane) 0 when created under this text, a set bit carried and
ignored (§6.3)" — [R-CNT-08]: "a writer creating a file under this text MUST write
flags = 0, but a set ignore-lane bit is not a file-conformance violation". PASSES;
the conduct qualifier keeps the cell out of conflict with [R-CNF-02].
Hunk 25's writer line "writes flags = 0 on creation (`[R-CNT-08]`, §6.3)" PASSES
against the same rule; its updater line "copies forward the input's unknown
ignore-lane flag bits, clears none and sets no other" PASSES against "An updater
MUST copy forward unknown ignore-lane bits of the file it modifies, MUST NOT clear
them, and MUST NOT set any other".
**Unconstrained sibling (X-12):** the third writer tier. §6.3 states a distinct
compactor rule — "A compactor, though its output is a new file, carries the input's
unknown ignore-lane bits into its output trailer **rather than writing flags = 0**,
and sets no other (§20.5, `[R-WRT-06]`)" — and §2.3's [R-CNF-02] names "an
updater's **or compactor's** copy-forward". Hunk 25 wrote the creator rule into the
writer checklist and the updater rule into the updater checklist and left the
compactor with neither; a compactor reading Appendix H finds only "writes
flags = 0 on creation", and its output *is* a new file.

### Group H. Persistence, the drop licence, and what "governing flags" reaches

**H.1 — hunk 18 makes the MU = 1 row bind the layer record (X-03).**
Old: header "**Stored flags**", lead-in "…the stored flags are authoritative (§7.3,
`[R-CNT-15]`; MU = 1 with PE = 0 is read as PE = 1, `[R-CNT-12]`), **and carry these
obligations:**" — the table applied to a type the updater does not implement.
New: header "**Governing flags**", lead-in "**Whichever source governs, its flags
carry these obligations:**". §7.3 fixes the **layer** record at MU = 1, PE = 1, and
the paragraph above says "For a type §7.3 registers, the registry's fixed flags
govern rather than the stored ones (`[R-CNT-22]`)". So the MU = 1 row now governs
every layer record in every file, and it reads: "Retain byte-identical. **The
updater MUST NOT modify the scope the record governs.** … At either scope **a
compactor MUST refuse to compact the file**." That forbids every layer edit §20.3
describes and every compaction of any file containing a layer.
The row's own body was written for the other case and still says so: "an **unknown
critical** record blocks modification of that layer"; "`[R-CNT-15]` makes an
**unimplemented** top-level MU = 1 record reject-file". And hunk 25's own Appendix H
updater entry, in the same commit, says "validates … **every layer it modifies**
(§20.3)" and "never modifies a scope governed by an **unknown critical** record".
Two repairs in one commit, opposite positions.

**H.2 — hunk 9 widens past its cited warrant (X-02b; check 7).**
Repair (§20.3 step 2): "a violation latent in a structure it **carries forward
unmodified** travels with that structure (§20.1, `[R-WRT-01]`)".
Warrant ([R-WRT-01], §20.1, L3100): "a violation latent in a structure they
**neither modify nor rely on** travels with it".
Governing verbs side by side: repair "carries forward unmodified"; warrant "neither
modify **nor rely on**". The repair dropped the reliance condition while citing the
rule that carries it. [R-WRT-03], which the same sentence now cites ("validating
either to `[R-WRT-03]`'s depth is not authoring it"), is entirely about reliance —
"§19.3's layer validation for every layer whose record, index, or extents the
commit **modifies**, and the §19.4 index chain for every segment whose entries the
commit **reuses**… Structures the commit **neither modifies nor relies on** impose
no further obligation." So the repair extends the travel-with excuse to exactly the
structures [R-WRT-01] withholds it from. I record this as part of X-02's family but
grade it separately below.

**H.3 — hunk 17's insertion and the "either" behind it (X-14).**
(c)'s list ended "…changing a channel's fill value where that channel carries no
padding position and no pad bit in any tile the layer stores in the generation the
commit supersedes." The next sentence: "A fill change on a channel that carries
**either** in a tile the layer **stored** in that generation is not an appender's
operation at all". Hunk 17 appended a fourth item after that clause — "or dropping
a PE = 0 record where §20.4 licenses the drop, any extent it owned becoming slack"
— so "either" must now reach back over a whole new item to find its pair.
Citation check: §20.4's MU = 0 / PE = 0 row, L3466: "Retain byte-identical, **or
drop it — its extent becoming slack**." PASSES, and hunk 17's "any extent it owned
becoming slack" matches it.

**H.4 — hunk 20's zero-layers row against its own governing rule (X-11).**
Row: "A conforming file: a directory carrying no layer record is a conforming
generation **whether or not it carries other records**, an empty directory
included | `[R-CNT-14]` (R-CNT-02)".
[R-CNT-14], L1037, untouched: "any number of layer records (**zero is valid: an
empty directory is a conforming generation**)" — the very conflation the row was
repaired to remove. §21.1: "§21.6's entries restate their governing rules on the
same terms a row does, and where such an entry and the rule it cites diverge,
**the rule governs there too**." The repair landed on the side §21.1 subordinates.
Hunk 20's other edit — adding `[R-CNT-18]` to the experimental-MU = 0 row — PASSES:
[R-CNT-18] L1138 is where the layer-sub-record half of that behaviour lives ("with
MU = 0 it is ignore-record"), and the row's condition is not scope-qualified.

### Group I. Standalone

Hunk 22 against [R-COD-07] (L2530): "Writers MUST NOT declare this codec for a
layer **any of whose addressed tiles'** decoded size exceeds 0x7E000000 bytes …
in a planar layer **each channel's plane carries its own decoded size** (§14.2,
§14.3), and **the largest governs**". Repair: "a layer declaring codec 4 with
**every addressed tile's** decoded size at most `0x7E000000`, **the largest channel
plane governing in a planar layer**". Word for word on both quantifiers.
Cross-check with §21.9's own per-instance paragraph, untouched: "*Decoded size of
one tile* ranges over a layer's **addressed** tiles, stored or not, **exactly as
`[R-COD-07]`'s cap is**". Consistent. And §11.2 makes a planar layer's addressed
tile count C·N, so an addressed tile of a planar layer *is* one channel's plane —
which is why the appositive is a gloss and not a second rule. **No finding**
(considered and dropped; see rejected candidates).

Hunk 23: the repair deletes a duplicated "before any use" and a duplicated "which
is why its output is re-verified whole", collapsing two sentences into one colon
construction. Citation `[R-LIF-06]` still governs recovery re-verification; §21.6's
mimic row (untouched) says "a recovery tool re-verifies its output whole (§9.6)".
Consistent. Em-dash count in the repaired sentence: one pair. **No finding.**

## 5. Em-dash sweep over the repaired sentences

- Hunk 2, L718–724: outer pair "— whether because … — the verifier MUST report",
  containing an em-dash inside the parenthesis ("…impeded reading them — and where
  the rejection is one the walk itself established…"). Three dashes, inner one
  unpaired. **(X-15)**
- Hunk 11, L3185–3196: "…or how they decode, or the coordinate §11.4 assigns any
  value they decode to **—** the set of padding positions …, the byte offset **—**
  or, in a packed plane, the bit position **—** of any value within the decoded tile
  image…". Three dashes; the reader who pairs 1–2 loses the sentence. Hunk 11
  lengthened the clause before the first dash and added an item after the third.
  **(X-16)**
- Hunks 5, 12, 13, 15, 16, 21, 23, 24: one pair each, or none. Clean.
- Two three-dash sentences I did **not** file because no hunk touched them:
  §21.6's slack row ("counted and reported by a verifier — as a partial total — an
  upper bound naming what stopped the walk — where its walk did not complete") and
  Appendix H's verifier entry ("the slack total (§9.7) — reported as partial — an
  upper bound, naming the scope or violation that stopped the walk — where its walk
  did not complete").

## 6. Derived numbers

My charter names no checksum, offset or count to recompute. The only arithmetic I
performed was structural, not numeric: §11.4's disk ordinal c · N + s and spatial
ordinal s = Σ tᵢ · ∏_{j>i} Gⱼ, used to establish that Gᵢ = ⌈Eᵢ/Tᵢ⌉ — and therefore
the extents Eᵢ — appear in the map §11.4 states, which is the basis of X-01.
Worked instance, from §11.4's own Example: grid (G_y, G_x) = (4, 8); disk ordinal 8
is tile (1, 0), since 1·8 + 0 = 8. Grow G_x to 16 and ordinal 8 becomes tile (0, 8),
since 0·16 + 8 = 8. Both figures are mine; §11.4's Example gives 1·8 + 0 = 8 and I
checked mine against it. Counts I derived and checked against the document: §21.6's
closing paragraph names 2 capability refusals (it says "Two structural cases");
§21.9's minimum-guarantee table has 8 rows and the text says "The last three rows"
+ "The first five rows" = 8 (consistent); of those 8, 2 (layers per file,
dir_length) have the file as their narrowest scope, which is the basis of X-09.

## 7. Findings index

X-01 hunks 5,11,13   LOCAL_CONTRADICTION  coordinate limb vs the shrink permission
X-02 hunks 5,11,14,16 UNSWEPT_RESTATEMENT "what §14 fixes" is no longer the bar
X-03 hunks 18,25     OVERSHOT             "Whichever source governs" binds the layer record
X-04 hunks 2,4,21    OVERCLAIM            a tile/record decline does not stop the walk
X-05 hunk 4          LOCAL_CONTRADICTION  "A verifier decodes every stored tile"
X-06 hunks 10,13     UNDERSHOT            the ordinal bar's ground lost "only"
X-07 hunk 13         OVERCLAIM            "the geometry changes this step permits"
X-08 hunks 5,15      OVERCLAIM            "permitted outright" vs "It holds provided"
X-09 hunk 21         OVERCLAIM            "which is a layer, a tile, or the record"
X-10 hunks 8,19,25   UNSWEPT_RESTATEMENT  Appendix H's "the sole resolved byte"
X-11 hunk 20         UNSWEPT_RESTATEMENT  [R-CNT-14]'s own empty-directory gloss
X-12 hunk 25         UNCONSTRAINED_SIBLING the compactor's flags rule
X-13 hunk 13         ANAPHOR              "One effect is barred beside it"
X-14 hunk 17         ANAPHOR              "a channel that carries either"
X-15 hunk 2          NESTED_DASH
X-16 hunk 11         NESTED_DASH
X-17 hunk 9          ANALOGY              "carries forward unmodified" vs [R-WRT-01]

(17 findings; X-17 is H.2 above, filed separately from X-02.)
