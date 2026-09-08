# Audit transcript — hunk-03.diff ("the list")

## Disclosure of unbidden context

Before I did anything, the harness placed into my context: (1) two
`<system-reminder>` blocks quoting `/Users/robertkleffner/.../CLAUDE.md`
(which just points to AGENTS.md) and the user's `MEMORY.md`, the latter
containing bullet-point titles like "TARN harness spec path", "TARN
lineage gate word list", "TARN repair prose vs rules", "TARN harness vs
charter", "TARN repair list vs diff", "Shell gates need explicit exit
checks", "TARN subagents on Opus"; (2) a userEmail block; (3) a
currentDate block (which changed mid-session from 2026-09-03 to
2026-09-08); (4) a large "deferred tools" list and MCP server
instructions (claude-in-chrome) and an "Auto Mode Active" reminder. None
of this is part of the specification or the hunk file. I did not open
any of the files MEMORY.md names (I did not read AGENTS.md, PLAN.md,
OPEN-QUESTIONS.md, docs/, git history, etc.), and none of my findings
below rest on anything from that material — every claim below is
supported by a quotation from spec/tarn.md or the hunk file, given
inline. Flagging this per the charter's disclosure requirement.

## Files read

- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit2/case/hunk-03.diff` (the only hunk file for this charter)
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, read in full sections around: 190-210 (R-CNF-03/04/05), 346-437 (§3.1 terms, §3.2 reference array), 468-485 (R-ENC-04/05/06), 627-740 (§5.2 byte coverage, R-CNT-21), 946-1230 (§7.2 record framing/extent slot, §7.4 layer record + example, §8 integrity), 1600-1740 (§10.3 registry note, §11.1 geometry + Rationale block, §11.2 grid arithmetic, §11.4 linearization/R-GEO-06), 2151-2200 (§15.2 sentinel), 2280-2350 (§16.1/§16.2 alignment/slab, R-SLB-01/02/03/04), 2475-2510 (R-COD-07 + its Note on the addressed-tiles quantifier), 3084-3330 (§20.3 the whole append procedure including my hunk's landing site and the surrounding numbered steps and Examples), 3331-3360 (start of §20.4), 3640-3735 (relevant error-register rows F21/F30/F31/F33, L10/L15-L17/L39/L40/L44), 4135-4165 (§23.1 deletion-is-not-erasure, which cross-references step 4 directly).

No other files were opened. I ran no code; only `grep`/`awk`/`sed -n`
against tarn.md, shown below with exact output.

## The rule this hunk's own text asserts (in my own words)

My charter assigns me: the exceptions/fixed two-list structure (spec
lines 3178-3200), the "partition" claim, the tense clause, the
empty-layer permission, the re-emission parenthetical (lines 3164-3171,
the small in-place edit to the untouched intro), and the closing
paragraph on growth bounds / channel-removal slack / SHOULD-produce-new-
file / unstoring-as-discard / slab and alignment maintenance (lines
3224-3246). (The "principle" paragraph at 3202-3222, explaining *why*
the line is drawn where it is and enumerating what's given up, is
explicitly the other lane's.)

What my text makes true of an implementation:

- Given a layer that stored at least one tile in the generation this
  commit supersedes, the commit's freedom to change that layer's
  declarations is now a **closed list** of five items (name/dimension-
  name/channel-name changes; extent growth; planar channel-list
  append/remove at the end; slab-or-alignment re-establish-or-clear),
  with everything else enumerated as explicitly fixed, and a violation
  forces the operation to be "a new layer, or a whole-file rewrite under
  a fresh file_id".
- The two lists are asserted to **partition** §7.4's field table (minus
  three named derived quantities).
- The freeze is scoped to the **prior** generation ("stores a tile in
  the generation this commit supersedes"), and a commit cannot dodge it
  by unstoring-and-redeclaring in the same commit; an already-empty
  layer is free.
- The re-emission parenthetical says only a **growth** (via
  `[R-GEO-06]`) moves an existing entry's ordinal — nothing else this
  step permits does.
- The closing paragraph pins the growth bound test, what channel-removal
  does to slack/entry_count, the SHOULD-new-file threshold, unstoring as
  the in-place discard mechanism, and the alignment/slab maintenance
  obligation.

## Check 5 — the partition claim, run against §7.4's actual table

I re-read §7.4 in full (spec lines 1083-1193) and enumerated every row
of its field table, then assigned each to a list:

| §7.4 field | Assignment | Where |
|---|---|---|
| name | MAY change | "its name ... MAY change" (3180) |
| layout | fixed | "the layout" (3185) |
| linearization | fixed | "the linearization" (3185) |
| codec | fixed | "the codec" (3186) |
| filter | fixed | "and the filter" (3186) |
| alignment A | MAY (re-establish/clear) | "a slab or alignment declaration is re-established or cleared" (3182-3183) |
| slab S | MAY (re-establish/clear) | same |
| slab alignment A_slab | MAY (re-establish/clear), bundled with S | same — R-CNT-23 ties A_slab to S so this is one declaration |
| rank d | fixed | "the rank" (3186) |
| channel count C | fixed for interleaved (part of "channel list"); MAY for planar (extend/shorten at end) | 3186-3188, 3181-3182 |
| dimension name | MAY change | "dimension ... names MAY change" (3180) |
| dimension extent | MAY (grow only) | "an extent MAY grow" (3180-3181) |
| dimension tile extent | fixed | "every tile extent" (3186) |
| channel name | MAY change | "channel names MAY change" (3180) |
| channel type | fixed | "every channel's type and fill" (3186-3187) |
| channel fill | fixed | same |
| index_encoding | fixed | "the index encoding" (3185) |
| entry_count | derived, set aside | "the derived ones aside — entry_count..." (3191-3192) |
| crc_of_crc_array | derived, set aside | same |
| **sub-records** | **unassigned** | not named anywhere in either list, and not one of the three named "derived" items |

`sub-records` is unambiguously one of "§7.4's fields" — it is the last
row of the table at line 1106 ("sub-records \| zero or more records
(§7.2 framing) to the end of the inline payload \| layer scope by
containment"), under a table column literally headed **Field** (line
1089: "\| Field \| Type \| Constraint \|"). It is not a computed
quantity like entry_count or crc_of_crc_array, so it cannot be folded
into "the derived ones aside" either. The claim at 3191: "The two lists
partition §7.4's fields, the derived ones aside" is therefore false as
stated — a field of the set it claims to partition is a member of
neither part.

I checked whether this is merely academic. Sub-records are governed
independently by §20.4's whole preservation-and-persistence apparatus
(the PE/MU flag table, spec lines 3331-3360+), which has no dependency
on whether the owning layer stores a tile. The Example at 3307-3309
even names the concrete case: "**(c) A change confined to the
directory** — clearing a slab declaration, renaming a layer, or
**dropping a PE = 0 record where §20.4 licenses the drop**" — with no
qualification that the layer must be tile-empty. So the actual,
correctly-governing rule for sub-records is unaffected by this
passage's overclaim; a careful implementer who reads §20.4 (and this
worked example) is not misled. I therefore call this a real but
non-byte-level defect: the partition claim is false on its own terms,
even though the true governing rule for the omitted field is stated
correctly elsewhere in the document. See A-01 below.

## Check 1 — every quantifier, against the four degenerate members the charter names

**"a layer that stores a tile in the generation this commit
supersedes"** (3178-3179) — existential ("a tile", not "every tile"),
and explicitly the *prior* generation. Confirmed against §3.1's
definition: "A tile is *stored in a generation* if and only if that
generation's tile-index entry for it is not the sentinel... unqualified
*stored* means stored in the live generation" (spec 378-381) —
"the generation this commit supersedes" is a live-generation-minus-one
reference, consistent throughout the passage.

- *One tile.* The premise is existential over tiles ("a tile", not "the
  tiles" or "every tile"), so even a layer with only one of its N tiles
  stored in the prior generation has its full declaration set frozen
  (subject to the exceptions). This matches the intent (§14 decoding
  correctness for that one tile depends on the same declarations as for
  any other) and is unchanged from the old bar's per-tile trigger. No
  defect.

- *Interleaved layer.* The fixed list names "an interleaved layer's
  channel list" as frozen outright (3187-3188), distinct from "the
  position of every planar channel but the last" which is the only
  planar-specific carve-out (a planar layer's *last* channel's position
  is not frozen, consistent with append/remove-at-end being legal only
  for planar layers per 3181-3182, "a planar layer's channel list MAY
  be extended at its end, or shortened from its end"). I checked this
  against `[R-GEO-06]` (spec 1727-1730): "The **disk tile ordinal**...
  is s for an interleaved layer, and **c · N + s** for a planar layer".
  An interleaved layer's ordinal doesn't depend on channel index at
  all, so there is no analogous "append at the end is ordinal-neutral"
  argument available for interleaved channels — consistent with why the
  fixed list freezes the *whole* interleaved channel list rather than
  offering an end-exception the way it does for planar. No
  contradiction between "an interleaved layer's channel list" being
  frozen and "channel names MAY change" (3180): the latter permits
  renaming a channel *in place*, the former bars adding, removing, or
  reordering channels of an interleaved layer — different axes of the
  same entries, both stated, not in tension.

- *Planar layer storing a tile for one channel and none for another.*
  I checked this specifically because the **deleted** old text had an
  explicit carve-out for exactly this case: "Where the superseded
  generation stored no tile carrying that channel there is nothing to
  reinterpret, and this bars nothing: re-typing a channel of a layer
  that stores nothing, or **a planar channel none of whose own tiles
  are stored, is a declaration edit like any other**" (hunk lines
  64-71, deleted). The new premise clause is scoped at the *layer*
  level only ("A layer that stores a tile... keeps its declarations"),
  and the fixed list's "every channel's type and fill" (3186-3187)
  carries no per-channel storedness qualifier. So under the new text, a
  planar layer with channel `a` storing tiles and channel `b` storing
  none has channel `b`'s type frozen too — narrower than the old rule.
  I confirmed this is a **deliberate, disclosed** design choice, not a
  silent narrowing: the paragraph immediately after mine (the other
  lane's "principle" paragraph, 3216-3222) states outright: "a re-type,
  a re-tiling... are rewrites even where a particular file would
  survive them in place, because deciding which files would is the
  edge this list exists to remove." I ran a control search to confirm
  the old per-channel carve-out doesn't survive as an unswept
  restatement elsewhere:
  `grep -n "none of whose own tiles\|nothing to reinterpret\|declaration edit like any other\|re-typing a channel" tarn.md` → **0 hits**. So this is
  intentional and swept cleanly; I record it as a checked-and-passed
  item, not a finding (see `rejected_candidates`).

**"with these exceptions and no other"** (3180) and **"Every other
declaration is fixed for as long as the layer stores a tile"**
(3184-3185) — I checked whether "stores a tile" in the second clause
silently drops the "in the generation this commit supersedes"
qualifier from the first sentence of the same paragraph, which would be
exactly the tense-shift shape this project has repeatedly lost rounds
to. Reading on, the paragraph's very next sentences pin the tense
explicitly: "The tense is the prior generation's (§3.1 defines *stored*
against a generation)..." (3193-3194). Given this sits in the same
paragraph, immediately after the fixed list, I read "stores a tile"
(3184) as inheriting the same (prior-generation) sense established one
sentence earlier and confirmed one sentence later — not a competing
present-tense reading. I also checked whether "for as long as" reads
as a *per-commit* test or an *enduring, cross-commit* invariant; the
latter is actually the more natural reading and is consistent with
each subsequent commit independently re-testing against its own
superseded generation — not a defect, just phrasing that generalizes
correctly.

## Re-emission parenthetical (lines 3169-3171)

Text: "(a growth renumbers ordinals wherever `[R-GEO-06]` moves them,
and nothing else this step permits moves one)."

I derived, from `[R-GEO-06]`'s formula (disk ordinal = s for
interleaved; c·N+s for planar, s = Σᵢ tᵢ·∏_{j>i}Gⱼ under linearization
1, spec 1717-1730), what each of the charter's four cases does:

1. **Appended planar channel.** New tiles land at c = C_old (the new
   channel's index), ordinals C_old·N through C_old·N+N-1. Every
   existing channel's c is unchanged and N is unaffected by a channel
   append (N depends only on geometry, not channel count, per §11.2:
   "N = ∏ Gᵢ"). No existing ordinal moves. Matches "an appended planar
   channel adds tiles at ordinals after every existing one" (3212-3213,
   the other lane's paragraph, but consistent with what I need to
   verify here).
2. **Channel removed from the end.** Symmetric to (1): removes only
   ordinals [C_old-1)·N, C_old·N), doesn't touch any other channel's
   ordinals. No move.
3. **Grown extent whose grid count does not change.** ⌈Eᵢ/Tᵢ⌉
   unchanged for every dimension ⇒ every Gⱼ in R-GEO-06's formula is
   unchanged ⇒ every existing tile's s (and c·N+s) is unchanged. No
   move, and (per the §11.1 Rationale, spec 1647-1651: "Growth that
   leaves entry_count unchanged touches the directory alone") the
   index isn't even re-emitted in this case, so the "entries new to
   this generation" list doesn't even apply to it.
4. **Grown extent whose grid count does change.** Some Gⱼ changes.
   Because s = Σᵢ tᵢ·∏_{j>i}Gⱼ, a changed Gⱼ can move the ordinal of
   *every* tile whose dimension index precedes j (their term's product
   includes Gⱼ) — including tiles in dimensions other than the one that
   grew, and (for a planar layer) with N itself shifting, every
   channel's block start c·N moves too. The parenthetical doesn't try
   to enumerate which tiles move — it correctly defers entirely to
   `[R-GEO-06]`ows moves them" — which is the right level of
   generality given how broadly a grid-count change can propagate.

I also checked the other three exceptions (name change, dimension/
channel-name change, slab/alignment re-establish-or-clear) against
`[R-GEO-06]`'s formula: none of them enters c, N, or s, so none of them
can move an ordinal — "nothing else this step permits moves one" holds
for all of the exceptions list's remaining members. **Passed** — no
defect found in the parenthetical.

## Tense clause and empty-layer permission (lines 3193-3200)

> "The tense is the prior generation's (§3.1 defines *stored* against a
> generation), so a commit does not earn an empty layer's freedom by
> emptying the layer as it re-declares it: superseding every tile of a
> layer and re-declaring it are one operation, and it is a rewrite. A
> layer that stores no tile in the generation this commit supersedes
> MAY be re-declared freely, which is what schema-first creation needs
> (§11.1)."

Constructed both cases the charter asks for:

- **Commit unstores every tile of a layer and re-tiles it, in one
  commit.** The *prior* generation (before this commit) still stored
  every one of those tiles, so the opening premise ("a layer that
  stores a tile in the generation this commit supersedes keeps its
  declarations") is triggered regardless of what this same commit does
  to those tiles. The tense clause makes this explicit and rules out
  the obvious dodge. Decision: **barred**, must be a rewrite.
- **Commit re-tiles a layer that stored nothing in the prior
  generation.** The last sentence covers this directly and grants free
  re-declaration. Decision: **permitted**.

These two sentences and the list agree: the list's premise is itself
conditioned on the prior generation, and the two added sentences are
exactly its converse cases (barring the same-commit escape, and
confirming the genuinely-already-empty case), not competing rules.

I also checked a case the charter doesn't name but that the wording
invites: a **two-commit** sequence — commit A unstores every tile
(nothing else), commit B (later) re-declares freely. By the text as
written, commit B's superseded generation (A's output) stores no tile,
so commit B's freedom is licensed by the last sentence. The tense
clause bars only earning the freedom "by emptying the layer **as it
re-declares it**" — i.e., in the *same* commit. I checked this against
the deleted old text to see whether this is a new gap or an inherited
design point: the old text used identical structure ("the tense is
both bars', so a commit does not earn this permission by emptying the
layer as it re-declares it", hunk lines 143-144, deleted) — so the
same two-commit workaround was equally available under the old rule.
Not a defect introduced here.

## Closing paragraph (lines 3224-3246)

Quoted qualifiers/citations checked one by one:

1. **"A growth holds provided the grown geometry stays within every
   bound the layer's own declarations impose, `[R-COD-07]`'s lz4
   decoded-size cap among them (L44), which an empty layer escapes
   only because that cap is quantified over addressed tiles."**
   Verified `[R-COD-07]` (spec 2485-2495): "Writers MUST NOT declare
   this codec for a layer any of whose **addressed** tiles' decoded
   size exceeds 0x7E000000 bytes." Verified its own Note (2497-2499):
   "The cap is quantified over the layer's *addressed* tiles, so a
   layer that addresses none... satisfies it whatever its tile shape
   declares." Verified L44's row (3731): "Codec 4 (lz4) declared on a
   layer any of whose addressed tiles' decoded size exceeds
   0x7E000000 bytes... `[R-COD-07]`." All three match the sentence's
   claim exactly, word for word on the "addressed" quantifier.
   **Citation passes.**
2. **"`[R-ENC-04]`'s 2⁶³ − 1 ceiling on every quantity it designates is
   another, and the list is not offered as exhaustive."** Verified
   `[R-ENC-04]` (spec 468-478): "MUST treat any quantity this
   specification **designates**... whose mathematical value would
   exceed 2⁶³ − 1 as a validity error", and its own Note at 2505-2509:
   "`[R-ENC-04]`'s overflow rule carries no such quantifier — it binds
   every quantity it designates, whether or not the layer addresses a
   tile." Matches exactly ("addressed" vs "every quantity it
   designates" — the two rules are correctly distinguished, not
   conflated). **Citation passes.**
3. **"A channel removed from the end leaves its stored tiles' extents
   as slack (§5.2), and `[R-CNT-17]` obliges the smaller entry_count
   and so a re-emitted index region."** Verified §5.2 (690-704): "Every
   byte the live state does not claim is **slack**... everything an
   earlier commit superseded" — a channel's tiles that fall out of the
   addressed set are no longer claimed by the live state, so they are
   slack by this definition. Verified `[R-CNT-17]` (1121-1126): "an
   entry_count that does not equal the **geometry-derived**
   addressed-tile count, is a validity error at layer scope" and
   §11.2's own definition of addressed-tile count as "N for an
   interleaved layer and **C · N** for a planar layer" (1663-1665) —
   removing a channel reduces C, hence C·N, hence the entry_count the
   record must declare. **Citation passes**, and channel count is
   correctly treated as part of the "geometry-derived" quantity R-CNT-17
   names (this phrasing is pre-existing in §7.4, not something this
   hunk introduced).
4. **"a writer SHOULD instead produce a new file wherever a commit
   would strand a large share of a layer's stored bytes — and always
   where it would re-emit every one of them, which duplicates the
   layer rather than dropping part of it."** This sentence is
   byte-for-byte identical to the deleted old text (hunk lines
   199-202). I checked whether "dropping part of it" still has a
   referent now that general extent-shrink is eliminated as a
   permitted operation (the other lane's paragraph states outright: "a
   shrink... are rewrites", 3217-3218) — I confirm channel-removal
   still legitimately supplies this referent (removing one channel
   among several *is* "dropping part of" the layer, as opposed to a
   full rewrite that duplicates the whole thing), so the phrase is not
   left dangling by the loss of general shrink as a category.
5. **"Unstoring a tile (§15.2) is how a commit discards data in place;
   discarding is the caller's operation and this specification does
   not bar it."** Verified §15.2 (2177-2185) defines the sentinel
   mechanism; this citation is used identically elsewhere (line 4144:
   "unstoring a tile so its entry becomes the sentinel (§15.2)"), so
   the citation itself is sound. I checked this against §23.1
   ("Deletion is not erasure", 4139-4163), which was **not** touched by
   this hunk but is directly on point: it lists three *separate*
   mechanisms that remove sample data from reachability — "superseding
   a stored tile's payload, unstoring a tile so its entry becomes the
   sentinel (§15.2), and removing a planar layer's last channel...
   all do it" (4143-4146) — and explicitly cross-references "(§20.3
   step 4)" for the channel-removal item, confirming §23.1 has already
   been sw ept to match this hunk's new rule and is internally
   consistent with it. Given §23.1 treats "unstoring" and "channel
   removal" as two of three distinct discard mechanisms, I considered
   whether "is how a commit discards data in place" overclaims
   exclusivity against the immediately preceding sentence about channel
   removal in the same paragraph. I judge this weak: "is how X does Y"
   is used elsewhere in the document (e.g. line 1608, 1853, 3511) in a
   descriptive, non-exclusive sense, and no accept/reject outcome turns
   on it — channel removal's mechanics were already fully and
   separately specified in the prior sentence, so no implementer is
   actually misled about what's permitted. I record this as a
   considered-and-rejected candidate, not a finding.
6. **"Extents this commit supersedes become slack (`[R-CNT-21]`)."**
   General statement, true of any commit that supersedes any extent
   (tile payload or otherwise), not scoped to channel-removal or growth
   specifically. Verified `[R-CNT-21]` (spec 733-734, 702-704) —
   matches. Not shrink-specific, so its survival after shrink's removal
   as a category is unproblematic; it remains fully general.
7. **"a slab declaration is re-established or cleared (`[R-SLB-04]`),
   and an aligned layer's stored tiles — every one the new state
   keeps, not only those this commit adds — satisfy its invariant or
   the declaration is cleared (`[R-SLB-01]`, `[R-CNF-05]`)."** See the
   dedicated section below — this is where I found finding A-02.

### Checking for orphaned "shrink" language (charter's specific ask)

I compared the closing paragraph sentence-by-sentence against the
deleted old shrink paragraph (hunk lines 162-210) and did not find any
sentence that still assumes general extent-shrink is a live category.
Every quantity the old shrink paragraph bound ("slack, entry_count, a
slab or alignment declaration... and the recommendation to produce a
new file") reappears in the new paragraph, cleanly re-attached to
"a channel removed from the end" instead of "a shrink" — a legitimate
substitution, not a dangling reference. **Passed.**

## Finding A-02 — slab/alignment "re-established" and first-time establishment

Text (mine, 3182-3183, in the exceptions list): "...and a slab or
alignment declaration is re-established or cleared as this step
provides below." And in the closing paragraph (3243-3246): "a slab
declaration is re-established or cleared (`[R-SLB-04]`), and an aligned
layer's stored tiles... satisfy its invariant or the declaration is
cleared (`[R-SLB-01]`, `[R-CNF-05]`)."

I checked what happens to a layer that stores a tile and currently has
**no** alignment or slab declared (A=0, S=0), where this commit wants
to declare one for the **first time**.

Verified `[R-SLB-04]` (spec 2339-2347) explicitly covers this case on
its own: "A writer or updater whose commit changes... **or the slab
declaration itself**, of a layer slab-declared in **either the
superseded or the new generation**, MUST either re-establish the
invariants for every such run — or clear the declaration" — "in either
the superseded or the new generation" is written precisely so that a
layer newly slab-declared in the new generation (but not in the
superseded one) is covered. So R-SLB-04 itself does license first-time
declaration.

But note R-SLB-04's own verb: it requires a writer to "**re-establish
the invariants**" — not "re-establish the declaration." The exceptions
list at 3182-3183 instead makes "declaration" the object of
"re-established": "a slab or alignment declaration is re-established or
cleared." Read in isolation (and it is the *first* place a reader
meets this permission, under the governing frame "keeps its
declarations, with these exceptions and no other"), "re-established"
most naturally reads as *restoring a declaration that already existed*,
not as licensing a *fresh* one. I checked why this matters more here
than it would have under the old rule: I confirmed (by reading the
entire deleted block) that alignment and slab were **never** part of
the old "§14 bar" declarations-freeze apparatus at all — they were
governed purely by R-SLB-01/R-SLB-04, with no "is this layer
tile-storing" gate whatsoever. The old closing-paragraph mentions of
"a slab or alignment declaration is re-established or cleared" (hunk
lines 164-165, 206) were incidental — obligations binding a shrink "as
they bind any commit", not the thing granting the freedom to touch
alignment/slab in the first place, because nothing needed to grant that
freedom under the old regime.

Under the new regime, alignment/slab are now **inside** the closed list
("with these exceptions and no other") for the first time, so this
exact wording is now load-bearing for a case (first-time declaration on
a tile-storing layer) that the old text never had to make this wording
carry. Whether a hasty implementer, reading only the exceptions-list
sentence and not chasing the `[R-SLB-04]` citation through to its own
"either the superseded or the new generation" language, would
conclude first-time alignment/slab declaration on a tile-storing layer
is barred, is a real (if second-order) ambiguity this specific
rewrite newly creates by relocating alignment/slab into the closed-list
frame.

**Byte-level assessment.** I lean toward **not** byte-level: the cited
authority (`[R-SLB-04]`) is unambiguous on its own terms and directly
adjacent (cited twice in the very passage under audit), so a careful
reader does resolve it correctly; and I found no error-register row
gating this rule at all (`grep -n "re-declar\|declarations.*fixed\|MUST NOT change one of these"` — see sweep log below), consistent with the whole
declarations-freeze apparatus being a writer-conduct rule rather than a
structurally-detectable one, like the barrier/durability rules R-CNF-02
explicitly carves out as not affecting file conformance by themselves.
I report it as a real prose ambiguity worth tightening (e.g. "a slab or
alignment declaration is (re-)established or cleared", or explicitly
saying "may be declared for the first time, re-established, or
cleared"), not a confirmed byte-fork.

## Checks 2, 3, 4, 6, 7, 8 — summary of what else I ran

**Check 2 (citations).** Every requirement ID and section number in my
assigned text was opened and checked against its actual definition;
results tabulated above. All passed except where noted (A-02's citation
itself is sound; the ambiguity is in the exceptions-list prose that
introduces it, not in R-SLB-04).

**Check 3 (normative placement).** My assigned text (3178-3246) sits in
plain body prose under numbered step 4 of "An appender MUST, in order:"
— no ">" blockquote anywhere in it, hence trivially normative; no
Note/Example/Rationale label issue arises for this hunk's own added
text. I did check whether any *restatement* of my rule sits in a
labeled block: the §11.1 **Rationale** block (spec 1636-1655) restates
this exact rule ("§20.3 states normatively, and governs, what a commit
may do..."), but that block explicitly says the rule is stated
*normatively* in §20.3, i.e. it's a rationale *for* the normative rule,
not the rule's only statement — the normative statement is squarely in
my (unlabeled) step-4 text. No defect.

**Check 4 (contradiction).** Beyond A-01 and A-02 (both self-consistency/
overclaim issues rather than direct MUST-vs-MAY collisions), I found no
sentence in the passage or its immediate neighbors that a reading of my
hunk's new text puts at odds with a MUST elsewhere. Specifically
checked: the Example (c) at 3307-3317 (matches, uses the same "fixed
declaration" vocabulary and the same fill/type/tile-extent examples);
the §11.1 Rationale (matches, already swept); §23.1 (matches, already
swept and cross-references step 4 by name).

**Check 6 (unconstrained siblings).** This is the same exercise as
Check 5's field-by-field pass; sub-records (A-01) is the one true gap.
I also checked entry_count/crc_of_crc_array/extent-slot's exclusion
from the two lists — legitimate, they're consequences of the tile-store
state rather than independent declarations, unlike sub-records.

**Check 7 (analogy).** Swept my assigned lines for "exactly as", "the
same way", "on the model", "transposed from", "likewise", "following
§", "same ground" — zero hits (see sweep log). No analogy-by-citation
construction appears in my paragraphs; this check is the other lane's
(principle paragraph) territory, where "exactly as" language does
appear, but that paragraph is out of my charter.

**Check 8 (anaphora).** Traced every back-reference my inserted text
introduces or that follows it in the rest of §20.3/§20.4:
- "with these exceptions and no other" — forward to the list that
  immediately follows; clear.
- "as this step provides below" (3183) — forward to the closing
  paragraph's slab/alignment sentence (3243-3246); confirmed it
  resolves there and nowhere else.
- "The two lists" (3191) — back to the two lists just stated; clear,
  unambiguous, no competing antecedent.
- "step 4" at Example (c), line 3313 (untouched text, downstream of my
  insertion) — still resolves correctly to the same numbered step,
  since the step's number/position didn't change, only its content.
- "the same step's permission" at line 3316 (untouched) — resolves to
  my empty-layer-permission sentence (3198-3200); confirmed unchanged
  meaning post-hunk.
- "which is what schema-first creation needs (§11.1)" (3199) — forward
  citation, verified against §11.1's own Rationale block, which
  explicitly discusses "schema-first workflows" (1636).

No anaphor was found to have silently re-resolved to newly-inserted
text at the expense of its old antecedent, and no anaphor in my
inserted text points further back than the reader will look.

## BCP 14 casing

`awk 'NR==3164,NR==3246' tarn.md | grep -noiE "must|shall|should|may"`
→ 6 hits, all already correctly capitalized (MAY ×4, MUST ×1, SHOULD
×1) — see sweep log. No casing defects in this hunk.

## NESTED_DASH

Swept lines 3178-3246 for em-dashes: 6 occurrences, forming at most one
open/close pair per sentence (3203-3205 is one pair; 3244-3245 is one
pair; the rest are single, unpaired dashes introducing a trailing
clause). No sentence has a dash-pair nested inside another dash-set-off
clause. No finding.

## Sweeps run (verbatim, with hit counts)

1. `grep -n "§14 bar\|the §14 bar\|the bar below\|the bar above\|the bar beside" tarn.md` → 0 hits. **Control**: I confirmed the search mechanism works by first re-finding a phrase I already knew was present verbatim without wrapping, `grep -n "re-declared freely" tarn.md`, which returned 3 hits (1645, 3198-3199 straddled, 3315) — confirming grep does find real hits in this file when the phrase doesn't wrap, and the 0-hit result above is a genuine zero, not a search failure. (The literal phrase "§14 bar" cannot wrap across a hard-wrap boundary — it's short — so a line-oriented grep is safe for it specifically, per the access-rule caution.)
2. `grep -n "re-declared freely\|generation this commit supersedes\|stores a tile in the generation\|stored no tile in the generation\|shortened from its end\|extended at its end\|shortened at its end" tarn.md` → 5 hits (1645, 1646(cont'd), 3182, 3198-3199, 3315) — used to find restatements; all consistent with the new rule.
3. `grep -n "channel list" tarn.md` → 3 hits (1641, 3181, 3188) — used to locate the §11.1 Rationale restatement and check it against the new rule; matched.
4. `grep -n "none of whose own tiles\|nothing to reinterpret\|declaration edit like any other\|re-typing a channel\|stores nothing, or a planar channel" tarn.md` → 0 hits. Control: same file, `grep -n "re-declared freely" tarn.md` already proven non-broken above (same grep invocation style); also directly cross-checked by reading the §7.4/§11.1 region by eye, confirming the old carve-out text is genuinely gone, not just unmatched by an unlucky pattern.
5. `grep -n "stores no tile\|store no tile\|carries no obligation\|no §14 obligation\|carries no §14\|carries that channel" tarn.md` → 3 hits (3198, 3216(cont'd), 4597) — none of them a stray restatement of the deleted per-channel carve-out; 4597 is an unrelated worked example about a fill value.
6. `grep -n "R-GEO-06\]" tarn.md` → 3 hits (1653, 1730, 3170) — used to verify the ordinal-formula citation.
7. `grep -n "R-COD-07\]\|R-ENC-04\]\|R-CNT-21\]\|R-SLB-04\]\|R-SLB-01\]\|R-CNF-05\]" tarn.md` → 27 hits total across all six IDs — used to locate every definition site for citation-checking; each relevant one opened and read (see Files read).
8. `grep -n "extent slot" tarn.md` → 15 hits — used to confirm the extent slot is defined in §7.2 (record framing, line 1008), not as a §7.4 inline-payload field, supporting finding A-01.
9. `grep -n "supersed" tarn.md` → 21 hits — used to check "superseding" vs "unstoring" terminology consistency (see rejected candidate below); read the §23.1 hit (4143-4146) in full.
10. `grep -n "alignment declaration\|clear the declaration\|declaration is cleared\|clears the declaration\|clearing a slab\|clearing an alignment" tarn.md` → 4 hits — used to check whether any rule elsewhere states an explicit "first-time declaration" allowance for alignment (none found outside R-SLB-04 itself), supporting A-02.
11. `awk 'NR==3164,NR==3246' tarn.md | grep -noiE "must|shall|should|may"` → 6 hits, all correctly cased (BCP 14 check).
12. `sed -n '3178,3200p;3224,3246p' tarn.md | grep -n "exactly as\|the same way\|on the model\|transposed from\|likewise\|following §\|same ground"` → 0 hits (Check 7 sweep of my own paragraphs; the analogy-bearing language lives in the other lane's principle paragraph, confirmed absent from mine).
13. `grep -n "re-declar\|declarations.*fixed\|new layer, or a whole-file rewrite\|MUST NOT change" tarn.md` → 6 hits, none an error-register row — supports A-02's "this rule carries no register row" observation.
14. `awk 'NR==3178,NR==3246{print NR": "$0}' tarn.md | grep "—"` → 6 em-dash lines, inspected individually for nesting (NESTED_DASH check).
15. `wc -l tarn.md` → 4729 (orientation only).

## Derived numbers

- Counted §7.4's table rows by hand against the hunk's two lists: 16
  distinguishable field-slots (name; layout; linearization; codec;
  filter; alignment A; slab S; slab alignment A_slab; rank d; channel
  count C; dimension name; dimension extent; dimension tile extent;
  channel name; channel type; channel fill; index_encoding;
  entry_count; crc_of_crc_array; sub-records — 20 total counting each
  dimension/channel sub-field separately). Assigned all 20 except
  sub-records to one of {MAY list, fixed list, derived-aside}. Compared
  against the document's own claim of a full partition ("The two lists
  partition §7.4's fields, the derived ones aside") — 19/20 assigned,
  1/20 (sub-records) unassigned. This 19-of-20 count is the basis for
  finding A-01.
- Re-derived `[R-GEO-06]`'s ordinal formula by hand for the four
  charter-specified growth/channel cases (see "Re-emission
  parenthetical" section) and confirmed the parenthetical's claim
  against each; no numeric mismatch found.

## Rejected candidates

1. **"superseding every tile of a layer" (tense clause, 3195-3196) vs.
   §23.1's three-way distinct enumeration of superseding / unstoring /
   channel-removal (4143-4146).** I initially suspected a genuine term
   confusion (the tense clause uses "superseding" to describe what
   should be "unstoring," since only unstoring empties a layer while
   superseding a tile's payload keeps it stored). I closed this: the
   identical wording ("superseding every tile of a layer and
   re-declaring it are one operation, and this bars it") is present
   verbatim in the **deleted** old text (hunk lines 41-44), immediately
   after an explicit mention of "unstoring" in the same old sentence —
   so the old text already used "supersede" in this broad,
   informal sense (anything that causes a prior tile state to no
   longer be current), and this hunk did not introduce the usage or
   change it. Not attributable to this repair.
2. **"Unstoring... is how a commit discards data in place" possibly
   overclaiming exclusivity against channel-removal in the same
   paragraph.** Closed above (Check 5, item 5) — no accept/reject
   consequence, "is how" used non-exclusively elsewhere in the
   document, channel removal's mechanics fully specified separately.
3. **Planar layer with one channel stored, one not — type/fill now
   frozen for the unstored channel too, versus the old per-channel
   carve-out.** Closed as intentional and disclosed by the adjacent
   (other lane's) "giving-up" paragraph, and confirmed the old
   carve-out text doesn't survive elsewhere (sweep #4, 0 hits). Not a
   finding against my hunk.
4. **Channel count C not literally named as a field in either list.**
   Closed: adequately covered indirectly via "an interleaved layer's
   channel list" (fixed) and the planar append/remove-at-end exception,
   both of which entail channel count; unlike sub-records there is no
   scenario left genuinely unaddressed.
5. **Dimension extent (Eᵢ) not literally named in the fixed list.**
   Closed: it is a genuine member of the MAY-list ("an extent MAY
   grow"), just with a narrower permitted operation (growth only) than
   unrestricted change — structurally identical in form to the planar
   channel-list exception's own "at its end" restriction. Not a gap.

## Confidence / where I found little

I ran all eight checks against every sentence in my assigned scope and
did not additionally flag: the growth-bound citations (R-COD-07,
R-ENC-04 — both verified word-for-word against their definitions and
Notes); the channel-removal entry_count/slack citations (R-CNT-17,
§5.2, R-CNT-21 — verified); the SHOULD-new-file threshold (verbatim
carryover, unchanged); BCP 14 casing (verified clean); NESTED_DASH
(verified clean); anaphora after the insertion (traced every one,
none re-resolved wrongly). Where I found nothing, it is because I
opened the cited section and compared it word-for-word against the
citing sentence, not because I skipped the check — the sweep log above
records the actual searches and their hit counts for each.
