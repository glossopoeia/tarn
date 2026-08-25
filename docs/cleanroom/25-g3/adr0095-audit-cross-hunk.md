# Cross-hunk consistency audit — hunks 01 and 02

## 0. Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (whole file, in
slices: 26-135, 55-70, 96-135, 618-665, 1030-1050, 1244-1262, 1463-1590,
1890-1990, 2014-2070, 2937-3336, 3320-3336, 3650-3730, 3337-3415, 3851-3900,
3910-3995, 4199-4240, 4403-4474), and the two hunk files
`r26audit-b/hunk-01.diff`, `r26audit-b/hunk-02.diff`.

NOT read: `full.diff`, any other hunk file, `docs/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`,
`spec/registry.json`, git history, the web. I did not list the audit directory
beyond a single `ls` glob restricted to `hunk-*.diff` (which returned only my
two files).

Ran: `wc -l`, `grep -n` (several), and one Python script that whitespace-
normalises the whole spec and prints context around eleven short probe strings
(output reproduced in §5 below). No other files were opened by that script.

**Unrequested context that appeared before I began:** a project instruction
file (`CLAUDE.md`, pointing at `AGENTS.md`), an index of the maintainer's
memory notes with six entry titles, the user's email, the current date, a git
status block with five recent commit subject lines, and an MCP/skills listing.
I did not open any file they named and I have not used any claim they make as
evidence. One commit subject line visibly names a conclusion about a compactor
and a "shrink bar"; I flag that it appeared. Every conclusion below is derived
from the spec text and the two hunks, and each is quoted from the spec.

## 1. Grouping

Section numbers do **not** group these. §11.1 and §23.1 sit 2,400 lines apart
and neither is where the rule lives. Grouped by rule:

**Group S — the §20.3 step-4 shrink rule.** Both hunks are restatements of one
normative passage: §20.3 step 4's "An extent MAY also **shrink**…" paragraph
(spec lines 3036–3060). Neither hunk touches that paragraph. Hunk 01 restates
the *permission* side of it (which shrinks are legal); hunk 02 restates the
*effect* side of it (where the bytes go). `grep -n "shrink"` returns exactly
three sites in the whole document — §11.1's Rationale (hunk 01), §20.3 step 4
(untouched), §23.1 (hunk 02) — so the group is closed and complete.

Sub-grouping inside S:

- **S-a, "where is the rule established":** hunk 01. It is entirely inside a
  `>` Rationale block and its whole job is to defer — "§20.3 states
  normatively, and governs".
- **S-b, "completeness of an enumeration":** hunk 02. It replaces a closed
  three-item list ("A commit removes sample data three ways") with an open one
  plus a *new* closed two-case classification ("Those two cases are
  exhaustive"). Hunk 01 also carries an enumeration (three items) but adds no
  closure hedge.

So the two hunks are one group under two views, which is exactly the condition
the charter describes: one commit, two restatements of one rule, written
together.

## 2. The rule each repair adopts, in my words

**Hunk 01 (§11.1 Rationale, non-normative).** Of a layer that stored tiles in
the superseded generation: a shrink is barred iff it alters what §14 fixes for
one of *those* tiles, regardless of whether the new state still stores it.
Three things are named as *not* such alterations: (i) de-addressing a tile,
(ii) a tile the superseded generation did not store, (iii) a new padding
position whose stored byte already holds the fill. A single shrink may combine
them.

**Hunk 02 (§23.1, normative prose ending `[R-PRV-01]`).** A commit never
erases sample data; it only makes it unreachable. Four operations are named
(supersede a payload, unstore a tile to the sentinel, a shrink that
de-addresses, a shrink that turns real positions into padding), the list is
explicitly open, and the *destinations* are claimed to be exactly two: bytes
whose carrying structure leaves the live state become slack; bytes whose
structure stays become that tile's padding content, which is fill and so
discloses nothing.

## 3. Check-by-check

### Check 1 — tense and quantifier

Hunk 01's governing quantifier: "a layer that **already stored tiles in the
generation a commit supersedes**" … "such a tile" … "whether or not the new
state still stores it".
The normative rule, §20.3 line 3038: "a shrink is permitted exactly where it
alters nothing §14 fixes for **any tile the layer stores in the generation this
commit supersedes**", and line 3045: "the quantifier is the superseded
generation's … barred **whether or not the new state still stores it**".
**Match.** Same generation, same set, same guard clause. PASS.

Hunk 02's case-2 quantifier: "a tile **the new state still stores**". The
document uses "still stores" in §20.3 line 3046 in the negated form ("whether
or not the new state still stores it") where it plainly means *stored in the
superseded generation and stored again now*. Reading hunk 02's "still" the same
way, case 2 ranges over tiles stored in both generations, and the warrant it
cites is quantified over exactly that set intersected with the bar's range.
PASS, but see check 7 — the gloss is narrower than the rule it cites, and the
residue is empty only because `[R-SER-05]` independently covers it.

Hunk 01's item (ii), "a tile the superseded generation did not store carries
none either", is a statement about a set *outside* the antecedent "such a
tile", spliced into a list of things that are not alterations *of* such a tile.
It is substantively right (the bar does not range over that set) but it is a
category shift mid-list. The preceding guard "whether or not the new state
still stores it" forecloses the dangerous misreading (that unstoring rescues a
shrink), which §20.3 line 3044 also forecloses expressly. Not filed.

### Check 2 — citations

| Citation | In | Verdict |
|---|---|---|
| §20.3 ("states normatively, and governs") | hunk 01 | PASS — §20.3 step 4 lines 2999–3060 is normative and is where the bar and the shrink permission live. |
| §14 ("what §14 fixes") | hunk 01 | PASS — §14.2/14.3/14.5 fix decoded size, byte offsets, and padding content. |
| §11.2 (grid count ⌈Eᵢ/Tᵢ⌉) | hunk 01 | PASS — line 1504. |
| `[R-CNT-17]` (entry_count → extent_length) | hunk 01 | PASS for the *growth* sentence it is attached to. Line 1038: "extent_length MUST equal entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 … or an entry_count that does not equal the geometry-derived addressed-tile count". Growth raising a grid count does raise entry_count. |
| `[R-GEO-06]` (disk ordinals renumber) | hunk 01 | PASS — line 1571 defines disk tile ordinal as s or c·N + s; N changes when a grid count changes. |
| `[R-WRT-04]` (§20.3) | hunk 01 | PASS — §20.3's terminal identifier, line 3078. |
| §9.1 (append-only) | hunk 02 | PASS. |
| §15.2 ("its entry becomes the sentinel") | hunk 02 | PASS — line 2016: "An addressed tile that is not stored has the **sentinel entry**". |
| §20.3 step 4 (shrink) | hunk 02 | PASS as a locator; see F-02 for what step 4 also says about index re-emission. |
| §20.4 ("a dropped ancillary record's extent") | hunk 02 | PASS — §20.4's MU=0/PE=0 row: "Retain byte-identical, or drop it — its extent becoming slack." |
| `[R-CNT-21]` ("remain in the file as slack") | hunk 02 | PASS — line 630: "Every byte the live state does not claim is **slack**: … and everything an earlier commit superseded." |
| §9.6 (backward trailer scan) | hunk 02 | PASS. |
| "the channel's recorded fill, which the layer record publishes" | hunk 02 | PARTIAL — the layer record does publish fill (`[R-TYP-06]`, layer-record channel entries), but "the channel's recorded fill" is singular and byte-shaped where §14.5 gives four shapes. See F-01. |
| §20.5, `[R-CNT-21]` in ¶2 | hunk 02 | PASS (untouched text). |

### Check 3 — does the repair sit in normative text?

Hunk 01 lands **entirely inside a `>` Rationale block**. Under `[R-CNF-01]`
(line 105) it carries no force. That is *correct* here, and deliberately so:
the block's first move is to hand governance away — "§20.3 states normatively,
and governs". The normative statement it defers to (§20.3 step 4) still says
the same thing after the repair, so this is not the "repair written into a
Rationale while the normative statement stands" failure. PASS.

Hunk 02 lands in ordinary prose terminating in `[R-PRV-01]` — normative. Its
`MUST NOT` is intact and unmodified. PASS.

### Check 4 — contradiction inside the passage, including untouched text

This is where the group fails. See F-02: §20.3 step 4's own consequence
sentence (untouched) is written to be true only of a shrink that de-addresses
tiles, and both repairs now make the *non*-de-addressing shrink explicit.

### Check 5 — exhaustive claims

Hunk 01: "a tile dropped out of the addressed set carries no §14 obligation and
**its extent** becomes slack" — a de-addressed tile that was *unstored* has no
extent; the claim is vacuous rather than false there, and §20.3 line 3042 words
it identically. Not filed.
Hunk 01's three-item list is joined by "and" with no closure hedge, while
§20.3's corresponding text is expressly a test and not a list — "the list names
where that effect arises rather than standing on its own" (line 3011) and "the
list is not offered as exhaustive" (line 3033). §20.3 names a *fourth*
non-alteration the §11.1 list omits: "a filter whose mandated stride makes it
the identity (`[R-COD-10]`)". See F-03.
Hunk 02: "Those two cases are exhaustive" — I tried five falsifications
(supersede+shrink in one commit; fill change on a sparse layer; de-address of
an unstored tile; a newly-stored tile gaining padding; `[R-LIF-04]` overwrite
past F) and the dichotomy survived all of them, because `[R-LIF-01]` makes
"leaves the live state" and "stays in the structure" jointly exhaust the
possibilities for any byte a commit touches. **PASS** — this is a real
improvement over the `-` side's closed "three ways".
Hunk 02: "no commit removes a layer at all" — PASS, §20.4 line 3176: "No commit
therefore removes a layer record".
Hunk 02: "never by erasing it" — PASS for commits; the two operations that do
shorten a file (`[R-LIF-04]` truncation past F, `[R-LIF-06]` recovery) are not
commits, and §20.5 line 3231 confirms "a compaction is a whole-file rewrite
rather than a commit".

### Check 6 — what the repairs leave unconstrained

The structure both repairs govern is **a padding position** and the carve-out
that turns on its stored content. §14.5 says a padding position carries **one
value per channel**, in four shapes, and the register's T4 row enumerates
exactly those four as its instances:

> `| T4 | A padding position does not encode, for each channel it carries, that channel's recorded fill value | interleaved numeric fill bytes; interleaved bool fill byte; planar numeric plane fill bytes; packed planar bool plane fill bit | verifier | certification | [R-SER-05] |`

Members, and whether the carve-out reaches each:

1. interleaved numeric — several fill bytes per channel, several channels per
   position. "the stored **byte**" (singular) under-describes it.
2. interleaved bool — one fill byte per channel; still several channels.
3. planar numeric — fill bytes; one channel per plane. Reached cleanly.
4. **packed planar bool — a fill BIT.** Not reached at all: the byte holding
   that bit also holds real values, so "the stored byte already holds the fill"
   is unsatisfiable however the bits sit. See F-01.

Second structure, hunk 02's: the *content classes a commit can strand*.
Members: stored-tile payloads (covered), padding content in a live tile
(covered), a dropped ancillary record's extent (covered), and a **superseded
record extent** — notably the user-metadata document, which §20.3's shape-(c)
Example says "lives in an extent (`[R-CNT-25]`), so a new extent is appended
and the old one becomes slack". Uncovered. See F-04.

### Check 7 — analogies, verb against verb

Hunk 02, "**goes the same way**": repair verb — a dropped ancillary record's
extent *goes the same way*; warrant verb — §20.4, "drop it — its **extent
becoming slack**". Same set (one record extent), same destination. PASS.

Hunk 02, "**misleads exactly as** a supersede so reported does" (untouched
half-sentence): both are "makes sample data unreachable", the `MUST NOT`'s own
range. PASS.

Hunk 02's warrant for case 2, quoted side by side:

- repair: "a shrink turning real positions into padding of a tile **the new
  state still stores** … §20.3 step 4 **permits** that shrink **only where
  those bytes already hold** the channel's recorded fill"
- §20.3 step 4: "a shrink is **permitted exactly where it alters nothing §14
  fixes for any tile the layer stores in the generation this commit
  supersedes**"; carve-out: "a new padding position whose stored byte already
  holds the fill `[R-SER-05]` fixes is not one"

"still stores" vs "stores in the generation this commit supersedes": the sets
coincide only if "still" is read as *stored then and now*. The residue — a tile
the new state stores that the superseded generation did **not** store — is
outside §20.3's bar entirely, so the "only where" claim is false of it; the
padding is fill anyway, but by `[R-SER-05]` authoring the bytes, not by §20.3
permitting the shrink. The document's own use of "still stores" (§20.3 line
3046) supports the narrow reading, so I report the comparison rather than file
it.

Hunk 01, item (ii) "carries **none either**": this is an analogy from item (i).
Item (i)'s warrant verb: §20.3, "a tile the new state **does not address**
carries no §14 obligation". Item (ii)'s warrant verb: §20.3's quantifier, "any
tile the layer **stores** in the generation this commit supersedes". *Addresses*
against *stores*, and *new state* against *superseded generation* — two
different axes carried by one "either". Both conclusions are nonetheless true,
because the bar reaches neither set. PASS on outcome; the shared "either"
carries more weight than its two warrants jointly support, which is why the
guard clause before the list is doing all the real work.

## 4. Direction of each disagreement

- F-01: §20.3 step 4's carve-out is the text that should change (both
  restatements then follow). The repairs are faithful; the source is
  under-specified.
- F-02: §20.3 step 4's consequence sentence is the text that should change. The
  repairs are right that a shrink need not de-address anything.
- F-03: hunk 01 is the text that should change (add the hedge §20.3 and hunk 02
  both carry).
- F-04: hunk 02 / `[R-PRV-01]` is the text that should change.

## 5. Searches run, with output

`grep -n "shrink\|shrunk\|de-address\|deaddress" spec/tarn.md` →
lines 1487, 1493 (hunk 01), 3036, 3037, 3046, 3051, 3056 (§20.3, untouched),
3932, 3939, 3942, 3948 (hunk 02). No other site in the document.

`grep -n "erasure\|erase\|unreachable\|reachab\|hex editor\|recoverab"` →
only §23.1/§23.2 carry the reachability framing; §22.3 line 3859 cites §23.1
for "slack is unconstrained and can hold anything" (consistent with hunk 02).

`grep -n "re-declar\|redeclar\|addressed set\|slack"` → 60 hits; the ones that
restate the rules under audit are 3056–3067 (§20.3), 3134 (shape (c) Example),
3179 (§20.4), 3332 (§20.5 Note), 3610 (§21.6 row), 3967 (§23.2). Each checked:
§23.2's "a tile unstored by a later commit leaves its earlier payload in the
file as slack (§23.1)" now agrees with hunk 02's newly added second operation —
that is a sweep in the right direction and I record it as a pass.

`grep -n "R-CNT-17\|R-GEO-06\|R-CNT-21"` → 1021, 1042, 1498-1499 (hunk 01),
3057 (§20.3 consequence sentence), 3498 (L21), 3499 (L22), plus verifier text.
L21 and L22 restate `[R-CNT-17]` as register rows; both are conditions on a
*file*, not on a commit, and neither says anything about re-emission, so
neither is affected by F-02.

Whitespace-normalised probe run (Python, whole file flattened) — the eleven
probes and their hit counts:

```
'already holds the fill'                 3   (§11.1 hunk 01; §20.3 bar carve-out; §20.3 shrink paragraph)
'recorded fill'                          6   (§14.5 ×2; §19.4; T4 row; §23.1 hunk 02; Appendix G)
'fill bit'                               5   (§13.1; §14.5 ×2; T4 row; T5 row)
'pad bit'                               13
'obliges the smaller entry_count'        1   (§20.3 line 3057 — the unswept sentence)
'relocating a live index region'         1   (§20.3 line 2996)
'stored-tile set or index content'       1   (§20.3 line 2984 — the re-emission trigger)
'confined to the directory'              1   (§20.3 shape (c) Example)
'not offered as'                         2   (§20.3 growth; §23.1 hunk 02)
'One shrink can do several'              1   (hunk 01)
'for each channel the position carries'  1   (§14.5)
```

The three-hit result for `'already holds the fill'` is the load-bearing one:
every statement of the carve-out in this document — the normative one and both
repairs — says "stored **byte**", and none of the three reaches T4's fourth
instance.

## 6. Worked counterexamples

**F-01.** Rank-1 planar layer, one bool channel, T₀ = 8, E₀ = 8, fill = false.
P = 8, decoded size ⌈8/8⌉ = 1 byte, no pad bits, G₀ = 1, one addressed tile,
stored with byte `0x0B` (positions 0, 1, 3 true). Commit shrinks E₀ to 5.
G₀ = ⌈5/8⌉ = 1, unchanged; positions 5, 6, 7 become padding positions, and
bits 5–7 of `0x0B` are already 0 = the fill bit, so §14.5 holds in the new
generation and the resulting file is conforming. Writer A applies the carve-out
literally: byte `0x0B` does not "hold the fill" (`0x00`), so the shrink alters
what §14 fixes and is barred — A must write a new file under a fresh file_id.
Writer B applies it at the granularity §14.5 uses: the fill *bit* is already
there, so the shrink is permitted and B appends generation 8. Same logical
operation, different bytes on disk, and B's file is conforming.

**F-02.** Rank-1 interleaved layer, one u8 channel, T₀ = 4, E₀ = 8. G₀ = 2,
entry_count = 2, both tiles stored. Tile 1 covers positions 4–7 and its stored
bytes at 5, 6, 7 already hold the fill. Commit shrinks E₀ to 5. G₀ = ⌈5/4⌉ = 2
— **unchanged** — so entry_count stays 2, `[R-CNT-17]`'s extent_length formula
gives the same value, no tile is de-addressed, and no tile becomes unstored.
Step 4's re-emission trigger ("Every layer whose stored-tile set or index
content this commit changes") does not fire, and step 4 adds "A layer whose
record alone changes keeps its extent slot, pointing at the existing region"
and "relocating a live index region is compaction's operation … not an
appender's". But the shrink paragraph's own last consequence sentence says of
*every* permitted shrink: "the de-addressed tiles' extents become slack
(`[R-CNT-21]`), `[R-CNT-17]` obliges the smaller entry_count and so a
re-emitted index region". Writer A follows that sentence and appends a
re-emitted 44-byte index region at a new placement, stranding the old one as
slack; writer B follows the trigger and appends only directory + pad + trailer.
Both outputs are conforming files; only one of the two writers is a conforming
appender, and the two readings disagree about which. The same Example's shape
(c) — "A change confined to the directory — clearing a slab declaration,
renaming a layer, or changing a channel's fill value on a layer with no padding
position and no pad bit" — omits this shrink from its enumeration of
directory-only commits, which is the non-normative half of the same omission.

**F-04.** A writer supersedes a user-metadata document to remove a subject's
name, appends the new extent, and reports the operation to its caller as
erasure. §20.3 shape (c): "its document lives in an extent (`[R-CNT-25]`), so a
new extent is appended and the old one becomes slack". The old document is
readable with a hex editor exactly as §23.1's case 1 describes. `[R-PRV-01]`'s
`MUST NOT` reaches only "any commit that makes **sample data** unreachable", so
the writer violates nothing. Hunk 02 widened the *list* (adding unstoring, and
keeping the dropped-ancillary-record clause) without widening the prohibition
the paragraph exists to state.
