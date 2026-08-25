# Repair audit — hunks 1 and 2 (r26audit-b)

Working transcript. Verbatim record of what was opened, what was run, what was
concluded, and what was looked for and not found.

---

## 0. Disclosure

Read, in full or in the ranges named:

- `/private/tmp/.../r26audit-b/hunk-01.diff`
- `/private/tmp/.../r26audit-b/hunk-02.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — ranges 618–665,
  934, 1019–1046, 1156–1200, 1240–1360, 1400–1520, 1700–1730, 1955–1990,
  2014–2070, 2113–2200, 2895–3200, 3300–3340, 3414–3625, 3650–3725, 3850–3995,
  4375–4460, plus grep hits listed below.

Nothing else was opened. `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`README.md`, `conformance/`, `spec/registry.json`, git history, `full.diff` and
the other auditor's hunk files were **not** read, and the hunk directory was not
listed.

**Context that arrived unasked.** The runtime placed a `CLAUDE.md` pointer to
`AGENTS.md`, and an index of the maintainer's private memory files, into context
before this audit began. I did not open any of them. One index line, in
particular, named a conclusion about a recent decision; I noted the collision
while reading §9.1/§20.5 and deliberately re-derived that point from §9.1's own
text ("every conforming mutation of a file is either a commit (§9.2) or a
whole-file rewrite under a new file_id (compaction, §20)") rather than relying on
it. No finding below rests on that material. Disclosed rather than acted on.

Commands run were `sed -n`, `awk`, `grep -n`, and `tr '\n' ' ' | grep -o` against
`spec/tarn.md` only. The `tr` form was used wherever the phrase could wrap; the
one failed invocation (`ugrep` rejected an empty subexpression in
`channel entry\(\| \)`) produced no conclusion — the point it was meant to test
was re-tested by `grep -n "channel entries"`, which succeeded (line 1019).

---

## 1. Hunk 1 — §11.1 shrink Rationale, lines 1483–1500

### 1.1 The text as it now stands (lines 1483–1494, verbatim)

```
> **Rationale.** Empty layers serve schema-first workflows: declare
> layers at creation, grow extents as data arrives. §20.3 states
> normatively, and governs, what a commit may do to a layer that
> already stored tiles in the generation a commit supersedes: a
> shrink is barred wherever it alters what §14 fixes for such a
> tile — whether or not the new state still stores it — and permitted
> wherever it does not: a tile dropped out of the addressed set
> carries no §14 obligation and its extent becomes slack, a tile the
> superseded generation did not store carries none either, and a new
> padding position whose stored byte already holds the fill alters
> nothing. One shrink can do several of these at once. A layer that stored nothing may be re-declared
> freely.
```

The `-` side had: "wherever it does not: dropping tiles out of the addressed set,
whose extents then become slack, is the ordinary case, and a new padding position
whose stored byte already holds the fill is the other." — a closed two-item count
that also implied the two were alternatives rather than combinable.

### 1.2 The rule the repair adopts, in my words

For a shrink, an implementation is permitted where, tile by tile, the shrink
alters nothing §14 fixes for a tile the *superseded* generation stored. Three
grounds on which a tile contributes no such alteration are named: (a) the new
state does not address the tile; (b) the superseded generation did not store the
tile; (c) the shrink makes a position padding whose stored byte already holds the
fill. Different tiles of one layer may rest on different grounds in one commit.
The Rationale asserts no force of its own — it delegates to §20.3 explicitly.

### 1.3 Check 3 first: does this sit in normative text?

No, and it does not claim to. §2.1 `[R-CNF-01]`, quoted from the document:

> All text in this document is normative except: §1 (Introduction); any text
> labeled *Note*, *Example*, or *Rationale*; and appendices identified as
> non-normative. `[R-CNF-01]`

Lines 1483–1500 are a `>` block labelled **Rationale**. It carries no force. The
question is therefore only the second half of check 3: does the normative
statement elsewhere still say the old thing? It does not — §20.3 step 4 (lines
3040–3055) is the normative home and it was not written as a closed count:

> What counts as such an alteration is the bar above and nothing
> else, its carve-out included — a new padding position whose stored
> byte already holds the fill `[R-SER-05]` fixes is not one, so a
> shrink producing only those is permitted here exactly as it is
> there, and this sentence answers the rescue question rather than
> restating the test.

So the repair had nothing to sweep normatively. Check 3: **pass**.

### 1.4 Deriving the list from the normative rule

§20.3 step 4, lines 3040–3049, verbatim:

> An extent MAY also **shrink**, and the bar above is the whole of
> the test, **in the bar's own tense**: a shrink is permitted
> exactly where it alters nothing §14 fixes for any tile the layer
> stores in the generation this commit supersedes. Dropping a tile
> out of the addressed set (§11.2's grid count falls) is not itself
> such an alteration — a tile the new state does not address carries
> no §14 obligation and its extent becomes slack — but neither does
> it rescue a commit that damages a prior-generation stored tile.

A shrink changes exactly two things a `[R-SER-05]`/§14 obligation could ride on:
which tiles are addressed (grid count `⌈Eᵢ / Tᵢ⌉` falls, §11.2 line 1503), and
which positions inside a still-addressed tile are padding (§11.3). Nothing else
§20.3's bar names moves under a pure shrink:

- **decoded size** — §14.2 fixes it from `P = ∏Tᵢ` and the channel set; `Eᵢ` does
  not enter. Unmoved.
- **byte offset of a sample within the decoded image** — `[R-GEO-06]` (line 1573)
  gives the in-tile ordinal as `Σᵢ uᵢ · ∏_{j>i} Tⱼ`, again `T` only. Unmoved.
- **codec / filter** — not a geometry field. Unmoved.
- **pad bits** (§14.3) — positions `P mod 8 … 7`, `P = ∏Tᵢ`. Unmoved.

So the ground set is {de-addressed, new-padding-holding-fill}, plus the trivial
"tile outside the bar's quantifier". The list of three matches. Nothing is
missing. Dropping a whole dimension to `Eᵢ = 0` (`[R-GEO-02]`, line 1478) is the
degenerate case of ground (a) and needs no separate item.

### 1.5 "One shrink can do several of these at once" — checked

True, and it fixes a real defect in the `-` side. Worked example against §11.2's
arithmetic: `E = 10, T = 4` gives `G = ⌈10/4⌉ = 3` (tiles covering 0–3, 4–7,
8–11, with 8 and 9 real). Shrink to `E = 5`: `G = 2`. Tile 2 leaves the addressed
set (ground a); tile 1 keeps positions 5, 6, 7, which were real and are now
padding (ground c). One shrink, two grounds, simultaneously. §20.3 permits the
combination: the bar is per-tile, and neither ground alters anything §14 fixes.

I checked whether §20.3's phrase "a shrink producing **only** those is permitted"
forecloses the combination — it does not: the sentence immediately before it
already established that de-addressing "is not itself such an alteration", so
"only those" ranges over alterations, not over the whole commit's effects.

### 1.6 Check 1 — tense and quantifier

- "a layer that **already stored tiles in the generation a commit supersedes**" —
  superseded generation. Matches §20.3's "any tile that layer stores in the
  generation this commit supersedes". **Pass.**
- "barred wherever it alters what §14 fixes for such a tile — **whether or not
  the new state still stores it**" — word-for-word §20.3 line 3047: "barred
  whether or not the new state still stores it". **Pass.**
- "a tile **dropped out of the addressed set**" vs §20.3's "a tile **the new
  state does not address**" — different phrasings, same set under a shrink (a
  tile the new state does not address, in a layer whose grid count fell, is
  exactly one dropped out). **Pass.**
- "a tile **the superseded generation did not store**" — superseded generation.
  Correct tense. But see 1.7: §20.3 states this permission **at layer
  granularity**, and the per-tile version the Rationale supplies carries a phrase
  that is false of one sub-class. This is finding **A-03**.

### 1.7 Check 5 — the exhaustive claim it cannot carry: "carries none either"

§20.3 states the not-stored permission only at layer scope (lines 3033–3037):

> A layer that stores no tile **in the
> generation this commit supersedes** MAY be re-declared freely,
> which is what schema-first creation needs (§11.1) — the tense is
> the bar's, so a commit does not earn this permission by emptying
> the layer as it re-declares it

The per-tile generalisation is sound *as a statement about the bar* — the bar's
quantifier is "any tile that layer stores in the generation this commit
supersedes", so a tile outside it constrains nothing. What is not sound is the
predicate the Rationale reuses: "**carries no §14 obligation**".

That predicate is §20.3's own, and in §20.3 it is applied only to "a tile the new
state does not address" — a class that, by §15's construction, cannot be stored
at all in the new state and therefore genuinely carries no §14 obligation. The
repair transplants it onto "a tile the superseded generation did not store",
which **can** be stored by this very commit: §20.3 step 4 line 2985 says the
re-emitted index carries "entries for tiles this commit **stores** or supersedes
written to their new state". For such a tile, §14 obligations attach in full —
`[R-SER-05]` (§14.5, line 1957):

> at every padding position, a writer
> MUST encode, for each channel the position carries, that channel's
> fill value

Concrete case: one commit shrinks `E` from 10 to 5 (`T = 4`) **and** stores tile
1, whose entry was the sentinel in the superseded generation. Tile 1 now has one
real position (4) and three padding positions (5, 6, 7). Under `[R-SER-05]` those
three must be written as fill. Under the Rationale's new clause the tile "carries
none either". Finding **A-03**.

### 1.8 Check 4 — contradiction in the passage, including untouched text

Read lines 1466–1500 whole.

- `[R-GEO-01]` (1470–1476) and `[R-GEO-02]` (1478–1481) — geometry floor and the
  extent-0 rule. Neither speaks to shrink; the Rationale's new breadth cannot
  collide with them. No contradiction.
- The untouched tail (1494–1500) covers **growth** only, and mentions index
  re-emission and ordinal renumbering there. §20.3 line 3057 says a permitted
  shrink also forces "the smaller entry_count and so a re-emitted index region".
  The Rationale's silence on shrink-side re-emission is an asymmetry in untouched
  text, not a contradiction, and §20.3 carries it normatively. **Not reported.**
- The sentence immediately after the repair, "A layer that stored nothing may be
  re-declared freely", is now the layer-level twin of the repair's new per-tile
  clause. Redundant, not contradictory.

No carve-out, no MUST, no old-wording-only sentence found in the passage that the
repair collides with. Check 4: **pass**, with A-03 standing on check 5 instead.

### 1.9 Check 7 — analogy

The Rationale argues by delegation ("§20.3 states normatively, and governs"),
which is a pointer, not an analogy. No "exactly as", "the same way", "following",
"transposed from" appears in the repaired span. The one near-analogy is the reuse
of §20.3's predicate discussed in 1.7, which is reported.

Verb comparison for the record:

| Rationale | §20.3 step 4 |
|---|---|
| "carries no §14 obligation" (of a tile the superseded generation did not store) | "carries no §14 obligation" (of "a tile the new state does not address") |
| "alters nothing" (new padding position holding fill) | "is not one [such an alteration]" |
| "is barred wherever it **alters**" | "is permitted exactly where it **alters** nothing" |

The second and third rows range over the same sets. The first does not.

### 1.10 Check 6 — what the repair left unconstrained here

Structure governed: a layer's geometry declaration under a commit — the fields
`d`, each `Eᵢ`, each `Tᵢ`, channel count `C`, channel types and fills,
linearization, index_encoding, entry_count, alignment/slab. The repair speaks
only to `Eᵢ` decreasing. Every sibling is pinned elsewhere and I checked each:
`Tᵢ`, `C`, types, linearization and the codec/filter are frozen for a layer
storing prior-generation tiles by the §20.3 bar's enumerated list (line 3000–3006);
`entry_count` and `extent_length` by `[R-CNT-17]` (L21, L22 at lines 3498–3499);
`d` and the floors by `[R-GEO-01]`; alignment and slab by `[R-SLB-01]`/`[R-SLB-04]`.
Nothing left unpinned. **Pass.**

### 1.11 Cosmetic

Line 1493 is 101 characters in a document hard-wrapped near 70. Line 3946 in
hunk 2 is 104. Not defects; noted so a later reader does not mistake them for
intentional.

---

## 2. Hunk 2 — §23.1, lines 3928–3950

### 2.1 The text as it now stands (verbatim, 3928–3950)

```
The append-only model (§9.1) means that what a commit removes, it
removes only from *reachability*. It removes sample data by making it
unreachable and never by erasing it: superseding a stored tile's
payload, unstoring a tile so its entry becomes the sentinel (§15.2),
and a shrink that either drops tiles out of the addressed set or turns
real positions into padding (§20.3 step 4) all do it, and a dropped
ancillary record's extent (§20.4) goes the same way; no commit removes
a layer at all. **Where the structure carrying the bytes leaves the
live state**, they remain in the file as slack (`[R-CNT-21]`),
readable by anyone with the bytes and a hex editor, and recoverable
by any tool that scans backward for an earlier trailer (§9.6).
**Where it does not** — a shrink turning real positions into padding
of a tile the new state still stores — they remain inside that tile
as its padding content, and disclose nothing a reader could not
already derive: §20.3 step 4 permits that shrink only where those
bytes already hold the channel's recorded fill, which the layer
record publishes. Those two cases are exhaustive because the bytes
either travel out of the live state or stay in the structure that
carried them; the list of operations above is not offered as closed. Writers and the tools built on them
MUST NOT represent any commit that makes sample data unreachable as
erasure of it — a shrink reported as erasure misleads exactly as a
supersede so reported does.
`[R-PRV-01]`
```

### 2.2 The rule the repair adopts, in my words

For any commit, every byte of sample data the commit renders unreachable ends up
in exactly one of two states, and an implementation may rely on that dichotomy:
either the structure that claimed the byte is no longer part of the live state,
in which case the byte is slack — freely readable, and restorable by rolling the
file back to an earlier trailer — or the structure is still live, in which case
the byte sits at a padding position of a live stored tile and, because §20.3 only
permits that transition where the byte already held the fill, it exposes nothing
the layer record does not already publish. The enumeration of operations that
produce the first state is illustrative; the dichotomy is not.

### 2.3 Check 3 — normative?

§23.1 is plain prose, no `>` prefix on any line 3928–3950, terminating in
`[R-PRV-01]`. Normative under `[R-CNF-01]`. **Pass.** Grep confirms `R-PRV-01`
occurs at exactly one line:

```
$ grep -n "R-PRV" spec/tarn.md
3950:`[R-PRV-01]`
3958:`[R-PRV-02]`
3975:history itself is sensitive. `[R-PRV-03]`
3987:input by content. `[R-PRV-04]`
4000:visible to anyone on the path. `[R-PRV-05]`
```

No §21 register row cites any `R-PRV-` identifier, so there is no row to sweep
and no row/prose divergence for §21.1 to arbitrate.

### 2.4 Check 2 — every citation opened

| Citation | Claimed | Verdict |
|---|---|---|
| §9.1 | append-only model | **Pass.** Line 1158: "an append-only transaction that extends the file and never modifies a committed byte." |
| §15.2 | unstoring makes the entry the sentinel | **Pass.** Line 2016 `[R-IDX-02]`: "An addressed tile that is not stored has the **sentinel entry**". |
| §20.3 step 4 (for the shrink operations) | drops tiles out of the addressed set / turns real positions into padding | **Pass.** Lines 3040–3055 are inside step 4 ("**Write payloads and indexes**", line 2977). |
| §20.4 | a dropped ancillary record's extent | **Pass.** §20.4 table, MU = 0 / PE = 0 row: "Retain byte-identical, or drop it — its extent becoming slack." |
| `[R-CNT-21]` | the bytes remain as slack | **Pass.** The requirement spans lines ~630–657; it opens "Every byte the live state does not claim is **slack**: alignment and slab gaps, the pre-trailer pad, and everything an earlier commit superseded" and closes "Slack that holds superseded data is a privacy consideration (§23)." |
| §9.6 | recoverable by a tool that scans backward for an earlier trailer | **Pass**, and the qualifier is load-bearing: §9.6 line 1294 gives the end-anchored probe as finding "the last committed state", and only "A recovery tool enumerating a file's commit states continues the same probe to offset 0." The repair says "any tool that scans backward **for an earlier trailer**", which is that second class. |
| §20.3 step 4 (for the fill precondition) | "permits that shrink only where those bytes already hold the channel's recorded fill" | **Pass on the predicate, near-miss on the quantifier** — see 2.7. |
| "which the layer record publishes" | the fill is in the layer record | **Pass.** §7.4 layout, line 1019: "C channel entries \| name … · type u16 · fill (u8 len + bytes)", inside the layer record's inline payload; §13.1 `[R-TYP-06]` line 1704: "Every channel entry records a fill value". |
| §20.5 (next paragraph, untouched) | compaction the only slack remover | **Pass**, and §20.5's own Note at 3316–3318 agrees: "truncation past F (`[R-LIF-04]`) and recovery to an earlier commit boundary (`[R-LIF-06]`) also shorten a file, but neither reclaims any." |
| "no commit removes a layer at all" | | **Pass.** §20.4: "No commit therefore removes a layer record, or a user-metadata record at either scope"; and "an appender never removes one (`[R-CNT-22]`, §7.3)". Compaction is not a commit — §9.1: "every conforming mutation of a file is either a commit (§9.2) or a whole-file rewrite under a new file_id (compaction, §20)". |

### 2.5 Check 5, part one — is the operation list now right?

The `-` side said "A commit removes sample data three ways" and named supersede,
shrink-de-address, shrink-to-padding. The `+` side drops the count and adds
**unstoring to the sentinel**. That addition is correct and was owed: §20.3 step
4 line 2986 distinguishes "entries for tiles this commit stores or supersedes"
from "entries for tiles that **become unstored** written as the sentinel", and
§23.2 (line 3966, untouched) already relied on the missing case — "a tile
unstored by a later commit leaves its earlier payload in the file as slack
(§23.1)". So the repair also swept the restatement that would otherwise have
contradicted the closed count. Good.

I looked for further omissions the not-closed disclaimer would have to absorb and
found three, all landing correctly in branch 1: a **modified** (not dropped)
record's superseded extent — §20.3 example (c), line 3193: "Editing user metadata
is not this shape: its document lives in an extent (`[R-CNT-25]`), so a new
extent is appended and the old one becomes slack"; a superseded **tile-index
region**; the superseded **directory** with every record header and inline
payload in it. The disclaimer covers their omission from the *list*. Their
omission from the **MUST NOT** is a different matter — finding **A-02**.

### 2.6 Check 5, part two — testing the asserted exhaustiveness

Claim: "the bytes either travel out of the live state or stay in the structure
that carried them."

I tried to construct a third case.

**Bytes whose carrying structure is itself new.** A commit re-emitting a tile
under a shrunk geometry writes a *new* payload; the removed bytes are in the old
payload, which is no longer claimed. Branch 1. The new payload's padding is
authored under `[R-SER-05]`, so it is not removed data at all. No third case.

**Bytes in a structure that is partly superseded.** I looked for a structure that
can be half-live. Candidates checked and rejected:
- *Slab runs* (§16.2 `[R-SLB-03]`): a run is a set of separately-claimed tile
  extents, not one structure; a commit touching one tile must re-establish or
  clear (`[R-SLB-04]`), and every superseded tile's extent falls to slack whole.
- *The directory*: re-emitted whole every commit (§9.2 step 3, and its Note: "A
  writer that re-points a new trailer at a prior generation's directory region
  has left step 3 unperformed"). Whole, never partly.
- *A tile-index region*: §20.3 step 4 — re-emitted "in full … necessarily at a new
  placement (`[R-LIF-01]`)". Whole.
- *A tile payload*: atomic; there is no partial supersede of one.

**Any operation the passage does not name.** Compaction — not a commit (§9.1),
and handled by the next paragraph. Growth — adds reachability rather than
removing it, and §20.3 line 3030 notes "a position that becomes real held that
channel's fill". Dropping a layer — barred (§20.4). Truncation past F — see 2.10.

**Can a byte stay live but move to a different structure?** Committed bytes are
frozen (`[R-LIF-01]`) and appends begin at F, so a structure created by a commit
cannot claim any byte below the old F. Structures do not overlap (`[R-CNT-02]`,
and §15.3's overlap rows). Relocating a live index region is explicitly
compaction's, not an appender's (§20.3 step 4). So the only way a byte leaves one
structure's claim in a commit is for that structure to leave the live state.

I also checked the stronger warrant the passage could have used and did not:
§5.2 `[R-CNT-02]` already partitions every byte into live-claimed or slack —
"Every byte the live state does not claim is **slack**". That makes the dichotomy
airtight independent of the "stays in the structure that carried it" gloss. The
weaker warrant the repair chose is nonetheless sound, per the paragraph above.

**Which unreachable-but-live sample bytes exist?** Only padding positions (§11.3;
never returned, `[R-GEO-04]`, and Appendix line ~4424 "never returns padding
positions (§11.3)") and pad bits (§14.3). Pad-bit positions depend on
`P = ∏Tᵢ`, and `Tᵢ` cannot change for a layer storing prior-generation tiles
(§20.3's bar reaches "the decoded size" and "the byte offset of any sample"). A
channel drop, a type change, a linearization change and a rank change are all
reached by the same bar. So padding is the only route, and branch 2's stated
consequence is the only consequence available in branch 2 — **for the tiles
branch 2 should cover.** It does not stay that way once the tile is superseded:
finding **A-01**.

Verdict on exhaustiveness: the dichotomy holds over bytes. **No third case
found.** The defect is in the assignment, not the count.

### 2.7 Checks 1 and 7 — tense, quantifier, and the warrant compared word for word

The two quantifiers, side by side, actual words:

| §23.1 branch 2 (line 3939–3943) | §20.3 step 4 (line 3042–3050) |
|---|---|
| "a shrink turning real positions into padding of **a tile the new state still stores**" | "a shrink **is permitted** exactly where it alters nothing §14 fixes for **any tile the layer stores in the generation this commit supersedes**" |
| "§20.3 step 4 **permits** that shrink only where those bytes **already hold** the channel's recorded fill" | "a new padding position whose stored byte **already holds** the fill `[R-SER-05]` fixes is not one" |

Governing verbs: "**permits** … only where … **already hold**" against "**is
permitted** exactly where … **already holds**". The predicate matches exactly.
The **sets do not**. §20.3's is the superseded generation's stored set; §23.1's is
the new state's stored set. Two residues:

- *New-state-stored, superseded-generation-unstored* (a tile this commit newly
  stores). §20.3 imposes no fill precondition there at all — the bar does not
  reach outside its quantifier. The disclosure conclusion survives, but on
  `[R-SER-05]`, which the passage does not cite. The word "still" arguably
  excludes this class; it is not said, so I record it here rather than as its own
  finding.
- *Stored in both, but re-emitted by this commit.* "still stores" is satisfied —
  the new state does store that tile. But the removed bytes are in the old
  payload, which is slack. Branch 2's consequence — "they remain inside that tile
  as its padding content, and disclose nothing" — is **false** of it. Finding
  **A-01**.

I checked whether §20.3 forbids the combination, which would make A-01 vacuous.
It does not. §20.3 line 3045: "Unstoring that tile in the same commit does not
rescue it either, and for the same reason: the quantifier is the superseded
generation's" — that bars a shrink that *damages* the tile even if the tile goes
away. It does not bar a shrink that is independently permitted (the new padding
positions already hold fill) on a tile the commit also supersedes for an
unrelated reason. A writer shrinking a layer and updating a sample of the edge
tile in one commit is the ordinary instance.

Tense verdict elsewhere in the hunk:
- "**leaves** the live state" (branch 1) — transition out of the new generation's
  live state. Right phrase, right generation.
- "the generation … supersedes" never appears in the repaired text. That is the
  gap A-01 names: nothing in §23.1 pins the tile to the superseded generation,
  which is what makes the cited warrant apply.

### 2.8 Check 4 — contradiction in the passage, including untouched text

Read §22.5 through §23.3 (lines 3915–4000) whole, looking for a carve-out, a
countervailing MUST, or a sentence written only for the old wording.

- §23.1 ¶2 (`[R-PRV-02]`, untouched): "Compaction (§20.5) is the only operation
  that removes slack, and it does so by writing a new file". No collision — ¶1
  now says the bytes *become* slack, which is what ¶2 presupposes.
- §23.2 (`[R-PRV-03]`, untouched, line 3966): "a tile unstored by a later commit
  leaves its earlier payload in the file as slack (§23.1)". Previously in tension
  with the closed count of three; the repair resolves it. **The repair swept
  this restatement correctly.**
- §22.3 `[R-SEC-03]` line 3859: "slack is unconstrained and can hold anything
  (§23.1)". Consistent.
- §20.5's Note line 3332: "logical deletion supersedes bytes but leaves them in
  the file as slack (`[R-CNT-21]`) — a privacy consideration (§23)". Consistent;
  it is a `>` block and so states nothing normatively that could conflict.
- §21.6's slack row (line 3610) and §5.2's slack paragraph — consistent.
- §21.7 (line 3705): "a commit that supersedes every tile it would have damaged
  leaves the live state clean, so the bar is unwitnessed there". Read against the
  repair, this is the *same* combination A-01 turns on (shrink plus supersede) and
  §21.7 treats it as a live possibility. That corroborates A-01 rather than
  contradicting the repair.

Two greps for citations of §23.1 that might treat its list as closed:

```
$ grep -n "23\.1\|erasure\|unreachab" spec/tarn.md
3859:hold anything (§23.1) — so coverage makes bytes reachable by a reader
3926:#### 23.1 Deletion is not erasure
3930:unreachable and never by erasing it: superseding a stored tile's
3947:MUST NOT represent any commit that makes sample data unreachable as
3948:erasure of it — a shrink reported as erasure misleads exactly as a
3956:media. A deployment whose obligation is erasure MUST treat that
3967:slack (§23.1) — so the index
```

Neither external citation enumerates the list or depends on its length.
Check 4: **pass**, no contradiction found.

### 2.9 Check 6 — what the repair left unconstrained in this structure

Structure the repair governs: the set of live-state members a commit can render
unreachable, per `[R-CNT-02]` (§5.2, line 623) — "the front signature block; or a
**structure** — a stored-tile extent, a record extent …, the directory, or the
trailer." Member by member:

| Member | Can a commit make its bytes unreachable? | Named by the repair? | Reached by the MUST NOT? |
|---|---|---|---|
| front signature block | no (never superseded) | n/a | n/a |
| stored-tile extent | yes — supersede, unstore, de-address | yes | yes ("sample data") |
| record extent, **dropped** ancillary | yes (§20.4 MU=0/PE=0 row) | yes | **no** |
| record extent, **modified** — user metadata above all (§20.3 (c), `[R-CNT-25]`) | yes | no | **no** |
| record extent, **tile-index region** (a record extent per §5.2, §9.7) | yes, every commit that touches the layer | no | **no** |
| the directory (every record header + inline payload: names, geometry, fills) | yes, every commit | no | **no** |
| the trailer | yes, every commit | no | n/a |

The dichotomy in the repaired sentences covers all of these correctly (they are
all branch 1). But `[R-PRV-01]`'s operative prohibition — untouched by the
repair — remains "MUST NOT represent any commit that makes **sample data**
unreachable as erasure of it." So a tool may still report the replacement of a
user-metadata document as erasure, when §23.2 `[R-PRV-03]` (line 3973) itself
directs "Writers handling sensitive material SHOULD treat names and metadata as
published content", and §20.3 (c) confirms the old document persists as slack.
The repair widened the description over "the bytes" generally, added the
not-closed disclaimer, and left the sibling members outside the bar. That is the
one-quantity-named-where-several-are-in-play shape. Finding **A-02**.

I record that the MUST NOT's narrowness is pre-existing; what the repair changed
is that the surrounding description now ranges over all removed bytes, which
makes the mismatch a live reading question rather than a scoping choice.

### 2.10 Considered and rejected: "never by erasing it"

The repair introduces the absolute "It removes sample data by making it
unreachable **and never by erasing it**". I tested it against §9.4 `[R-LIF-04]`
(line 1252): a writer whose physical file is longer than F "MUST either truncate
to F before step 1 of `[R-LIF-02]`, or **overwrite from F** and truncate the
physical file to the new committed_file_length no later than step 6". The
overwrite path destroys residue bytes *inside* steps 1–6 of the commit, and a
torn commit's residue can be sample data. So a commit can destroy bytes that
encode samples.

I do not report this. The paragraph's first sentence fixes the sense of
"removes": "what a commit removes, it removes **only from reachability**". The
residue past F was never reachable and is not data any commit removed; §9.5's
Note names it "residue", a category §5.2 keeps distinct from slack, and §20.5's
Rationale (line 3316) already records that truncation past F shortens a file
without reclaiming slack. The reading that falsifies "never" requires taking
"sample data" as "any bytes that encode samples" against the paragraph's own
stipulation. Recorded here so a later reader knows it was tested, not missed.

### 2.11 Considered and rejected: "readable by anyone with the bytes and a hex editor"

§5.2 says "A reader MUST NOT interpret it (§9.5)". That binds a conforming
reader, not a hex editor, and §9.6 exempts "Recovery tools and verifiers — never
conforming readers on the default path". No contradiction.

---

## 3. Findings

- **A-01** (hunk 2, NEW_AMBIGUITY, not byte-level) — branch 2's defining
  appositive, "a tile the new state still stores", is satisfied by a tile this
  commit supersedes, for which branch 2's consequence is false: the removed bytes
  are slack, hex-readable and rollback-recoverable, not padding content of a live
  tile. The bolded test and the appositive partition the cases differently, so
  "Those two cases are exhaustive" mis-assigns that case, and the warrant cited
  for branch 2 is quantified over the superseded generation while the branch is
  quantified over the new state.

- **A-02** (hunk 2, UNDERSHOT, not byte-level) — the repair generalised the
  description to "the bytes" and declared the operation list open, while
  `[R-PRV-01]`'s MUST NOT stays quantified over "sample data", leaving a
  superseded user-metadata extent, a superseded tile-index region and a
  superseded directory — all persisting verbatim as slack, all named disclosive
  by §23.2 — unreached by the misrepresentation bar.

- **A-03** (hunk 1, OVERCLAIM, not byte-level) — "a tile the superseded
  generation did not store carries none either" transplants §20.3's predicate
  "carries no §14 obligation" from a class that cannot be stored (a tile the new
  state does not address) onto a class that this very commit can store, for which
  `[R-SER-05]` obligations attach in full.

## 4. Byte-level test, applied to each

For all three the answer is **no**, and the discriminating question decides it
the same way each time: the file a permissive reading would let a writer produce
already carries a register-row violation, so `[R-CNF-05]` ("A writer MUST emit
only conforming files") bars every conforming writer from emitting it under both
readings.

- A-01 and A-02 concern how a tool *describes* a commit and what it *discloses*
  to an operator. No byte of any file changes, and no accept/reject verdict
  moves — a file is conforming or not independently of what its producer called
  the operation.
- A-03: the file a writer following the loose reading would emit has non-fill
  bytes at a padding position, which is §21.4 row T4 ("A padding position does
  not encode, for each channel it carries, that channel's recorded fill value …
  `[R-SER-05]`"). Nonconforming under both readings. The emittable set does not
  move.

## 5. Per-check summary

| Check | Hunk 1 | Hunk 2 |
|---|---|---|
| 1 tense/quantifier | pass on three of four clauses; A-03 on the fourth | **A-01** |
| 2 citations | n/a (delegation only, verified §20.3 says what is claimed) | all ten opened; nine pass, the §20.3 warrant is the near-miss inside A-01 |
| 3 normative placement | pass (Rationale, correctly delegating; §20.3 already carries the new rule) | pass (plain prose, `[R-PRV-01]`) |
| 4 contradiction in passage | pass | pass; the §23.2 restatement was correctly swept |
| 5 exhaustive claims | **A-03** | count correctly removed; dichotomy holds over bytes; no third case found |
| 6 unconstrained siblings | pass | **A-02** |
| 7 analogy | pass (predicate reuse reported under check 5) | verbs match, sets do not — inside A-01 |
