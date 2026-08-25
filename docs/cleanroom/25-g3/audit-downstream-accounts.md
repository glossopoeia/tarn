# Round 25 — downstream-accounts audit (auditor B)

Charter: three hunks, but the question is what *outside* them depended on the
old answers, and what hunk 2's reversal stranded.

## 0. Disclosure

Read, in full or in the ranges named:

- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/f4334f8b-602f-4a50-9c17-a97272554180/scratchpad/r25audit-b/hunk-01.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/f4334f8b-602f-4a50-9c17-a97272554180/scratchpad/r25audit-b/hunk-02.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/f4334f8b-602f-4a50-9c17-a97272554180/scratchpad/r25audit-b/hunk-03.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, ranges:
  55–70, 134–280, 282–345, 596–690, 735–830, 928–942, 1000–1060, 1156–1260,
  1288–1300, 1358–1370, 1463–1600, 1693–1745, 1889–1990, 1989–2035,
  2894–2936, 2936–3200, 3199–3340, 3595–3730, 3945–3998, 4198–4212,
  4256–4467.

Ran only `grep`/`sed`/`tr`/`wc` against `spec/tarn.md`. Read nothing under
`docs/`, `conformance/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`README.md`, `spec/registry.json`; ran no git command; did not open
`full.diff`; did not list the hunk directory; no web access.

**Context I did not ask for.** Material appeared in my context before I began:
a project-instruction pointer (`CLAUDE.md` → `AGENTS.md`) and an index of the
maintainer's memory notes naming several TARN-specific topics, plus an
environment/git-status header listing recent commit subject lines. I did not
open any of it and I have not used it: every conclusion below is traced to a
line of `spec/tarn.md` or of a hunk file, quoted in place. I name its
appearance here because disclosure is mandatory; I do not repeat its contents.

---

## 1. What each hunk changes about the document's content

### Hunk 1 — §11.1 shrink Rationale (a `>` block; non-normative per [R-CNF-01])

Before: a shrink is "permitted where it only drops tiles out of the addressed
set, whose extents then become slack."

After: a shrink is "permitted wherever it does not [alter what §14 fixes]:
dropping tiles out of the addressed set, whose extents then become slack, is
the ordinary case, and a new padding position whose stored byte already holds
the fill is the other."

**Content change:** the Rationale stops presenting de-addressing as the *only*
permitted shrink and promotes §20.3 step 4's carve-out — the shrink that
converts real positions to padding inside a *surviving, still-stored* tile — to
a co-equal named case. Nothing new is *required*; a shape of commit that the
old Rationale implied was barred is now stated as permitted.

### Hunk 2 — §20.5 compactor obligations (normative; inside [R-WRT-06])

Before (one day old): "[R-LIF-02]'s commit protocol does not bind a compactor
… Two consequences follow and are intended. **The output's pre-trailer gap is
fixed by nothing.** … two conforming compactors given one input MAY emit
outputs of different lengths … **And no barrier ordering is owed within the
output.** … A compactor SHOULD make its output durable before anything
discards the input."

After: "A compactor MUST follow `[R-LIF-02]`'s **creation path**, as §20.2
obliges a creator … The pad of step 5 and the barriers of steps 4 and 6 —
both, not one — are owed here as they are of a creator."

**Content change:** three things move. (a) A compactor's output pre-trailer gap
is now pinned to `[R-LIF-02]` step 5's pad-to-64 rather than free; outputs of
two conforming compactors can no longer differ in length on that account.
(b) Two storage barriers are now owed inside the compaction write, where none
were. (c) The `SHOULD` on making the output durable before the input is
discarded is deleted outright, not replaced (subsumed: step 6's barrier makes
the output durable at completion, and [R-PRV-02] still says the input persists
"until something outside this specification deletes it").

### Hunk 3 — §23.1 [R-PRV-01] (normative)

Before: "A commit removes sample data two ways — superseding it, and a shrink
that de-addresses tiles (§20.3 step 4) … In each case the bytes remain in the
file as slack."

After: "three ways — superseding it, a shrink that de-addresses tiles, and a
shrink that turns a stored tile's real positions into padding without
de-addressing it (§20.3 step 4) … The first two leave the bytes in the file as
slack … The third leaves them inside a live stored tile, as its padding
content, and discloses nothing a reader could not already derive: §20.3 step 4
permits that shrink only where those bytes already hold the channel's recorded
fill, which the layer record publishes."

**Content change:** the same promotion as hunk 1, in normative text, plus a new
factual claim about disclosure (the third way exposes nothing new because the
bytes were already the published fill). The `MUST NOT`-represent-as-erasure
rule is unchanged and its quantifier ("any commit that makes sample data
unreachable") is unchanged.

**Common thread:** hunks 1 and 3 both take one previously-incidental carve-out
in §20.3 step 4 and make it a first-class, enumerated case. That is exactly the
kind of change that strands *consequence* sentences written when only the other
case existed. Section 3 is where I went looking.

---

## 2. The seven checks, per hunk

### Check 1 — tense and quantifier

**Hunk 1.** The Rationale's antecedent is "a layer that already stored tiles in
the generation a commit supersedes"; "such a tile" therefore ranges over tiles
the layer stored in the **superseded** generation. The normative rule it
restates, §20.3 step 4 (line 3036):

> "a shrink is permitted exactly where it alters nothing §14 fixes for any tile
> the layer stores in the generation this commit supersedes."

Same generation, same quantifier ("any tile … stores in the generation this
commit supersedes" vs "such a tile"). The "whether or not the new state still
stores it" clause matches §20.3 line 3045–3047 word for word in force. **PASS.**

**Hunk 2.** Generation question: which file? The repair speaks about the
*output*, at generation 1, with no prior trailer. `[R-LIF-02]`'s creation
paragraph (lines 1182–1185) is quantified over exactly that case: "On creation
there is no prior trailer: the writer first emits the front signature block
… then performs steps 2–6, writing beginning at offset 16, with generation 1."
The repair's own words — "the output has no prior trailer and stands at
generation 1, which is the case that path states" — match. **PASS.**

**Hunk 3.** Tense: "a shrink that turns a **stored** tile's real positions into
padding without de-addressing it". §3.1: "unqualified *stored* means stored in
the live generation." §20.3's bar is quantified over the *superseded*
generation. For the third way the two coincide (the tile survives the commit
still stored), so the loose "stored" is harmless here. **PASS**, noted.

### Check 2 — citations resolve

Every identifier and section number in the three `+` sides, opened and read:

| Cite | Where it appears | Verdict |
|---|---|---|
| §20.3 | hunk 1, hunk 3 | PASS — §20.3 step 4 is where the shrink bar and its carve-out are stated normatively |
| §14 | hunk 1 | PASS — §14.5 [R-SER-05] fixes padding content; §14.2/§14.3 fix decoded size and offsets |
| §11.2 / ⌈Eᵢ/Tᵢ⌉ | hunk 1 | PASS — §11.2 defines the grid count in that form |
| [R-CNT-17] | hunk 1 | PASS — §7.4: "extent_length MUST equal entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4"; entry_count "equals the addressed-tile count" |
| [R-GEO-06] | hunk 1 | PASS — §11.4 disk tile ordinal |
| [R-WRT-04] | hunk 1 | PASS — the append procedure, whose step 4 renumbers ordinals |
| [R-LIF-02] "creation path" | hunk 2 | PASS — the paragraph at 1182–1185 exists and states the no-prior-trailer, generation-1 case |
| §20.2 | hunk 2 | PASS — [R-WRT-02]: "A creator MUST follow `[R-LIF-02]`'s creation path … (`[R-LIF-02]` steps 4–6 — both barriers, not one)". The repair's "both, not one" is that idiom verbatim |
| [R-WRT-01] | hunk 2 | PASS — §20.1: "An appender and a compactor satisfy every writer requirement for the bytes they produce". The repair's gloss ("already has a compactor satisfying every writer requirement for the bytes it produces") is accurate |
| [R-LIF-01] | hunk 2 | PASS — §9.1: "every conforming mutation … is either a commit (§9.2) or a whole-file rewrite under a new file_id (compaction, §20)" |
| [R-LIF-03] | hunk 2 (context) | PASS — §9.3 states the (file_id, range) cache contract |
| step 5 / steps 4 and 6 | hunk 2 | PASS — §9.2: (4) barrier, (5) pad to next 64-byte boundary + trailer, (6) barrier |
| §20.3 step 4 | hunk 3 | PASS — the carve-out is there: "a new padding position whose stored byte already holds the fill `[R-SER-05]` fixes is not one" |
| §20.4 | hunk 3 | PASS — the MU=0/PE=0 row is the dropped-ancillary case, extent "becoming slack" |
| [R-CNT-21] | hunk 3 | PASS — §5.2 defines slack and its unconstrained content |
| §9.6 | hunk 3 | PASS — "probe backward at 64-aligned offsets o for the trailer magic … The nearest-to-end valid candidate is the last committed state" |
| "which the layer record publishes" (fill) | hunk 3 | PASS — §7.4's channel entries carry `fill (u8 len + bytes)`; [R-TYP-06] makes it authoritative |
| "no commit removes a layer at all" | hunk 3 (retained) | PASS — §20.4: "No commit therefore removes a layer record" / "an appender never removes one" |

No citation in any `+` line points at a rule that only nearly says the claimed
thing. **Check 2 clean.**

### Check 3 — the repair sits in normative text

Grepped the distinctive terms rather than the IDs (whitespace-normalised,
because the file is hard-wrapped):

```
$ grep -n -i "shrink\|de-address" spec/tarn.md
1487:> shrink is barred wherever it alters what §14 fixes for such a     <- hunk 1, inside a ">" block
3035:   An extent MAY also **shrink**, and the bar above is the whole of  <- §20.3, normative
3036-3057 (normative, [R-WRT-04])
3929/3931/3938/3941  <- hunk 3, §23.1, normative, [R-PRV-01]
```

```
$ tr '\n' ' ' < spec/tarn.md | tr -s ' ' | grep -o "new padding position whose stored byte[^§]*"
… "or a new padding position whose stored byte already holds the fill `[R-SER-05]` fixes — is not what this bars." (§20.3, line ~3011, NORMATIVE)
… "a new padding position whose stored byte already holds the fill `[R-SER-05]` fixes is not one, so a shrink producing only those is permitted here exactly as it is there" (§20.3, line ~3048, NORMATIVE)
```

Hunk 1 edits a `>` block, so it has no force of its own — but the rule it now
restates *does* have a normative home at §20.3 step 4, stated the same way, so
the repair did land. This is the reverse of the failure signature: the
Rationale was the stale half and §20.3 was already correct. **PASS.**

Hunk 2 sits between "…relocation puts different bytes at the same ranges." and
the `[R-WRT-06]` tag at line 3252 — inside the requirement, with `MUST`.
**PASS.** Hunk 3 sits inside `[R-PRV-01]`, above its tag. **PASS.**

### Check 4 — contradiction in the same passage, including untouched text

This is where the audit's one strong finding is. Details in §3.1 below
(**B-01**). Summarising the collisions I looked for and what I found:

- §11.1 (hunk 1's passage), whole subsection read: [R-GEO-01], [R-GEO-02], the
  Rationale, §11.2. No carve-out or MUST collides with the widened permission.
  The Rationale's growth half is untouched and independent. Clean.
- §20.5 (hunk 2's passage), whole section read, 3201–3333. Placement freedom
  ("preserves no placement … free to place structures anywhere §5.2 admits")
  does **not** collide: §20.2's creation path also leaves placement free
  ([R-SLB-05]). The MU=1 refusal, the regeneration rules, [R-WRT-09]'s depth —
  none collides with a pad or a barrier. One residual ambiguity, **B-05**.
- §23.1 (hunk 3's passage), whole subsection read. The `MUST NOT` that follows
  is quantified over "any commit that makes sample data unreachable", strictly
  wider than the three-way list, so the list cannot narrow the rule. Clean.
- §20.3 step 4, which hunks 1 and 3 both cite as their normative authority:
  **collision found**, see B-01.

### Check 5 — exhaustive claims

Words promising completeness, in the `+` text, each tested:

- hunk 1: "**the other**" — a closed two-item list of permitted shrinks.
  **FALSIFIED**, see **B-04**.
- hunk 1: "every grid count ⌈Eᵢ / Tᵢ⌉ … unchanged" (retained text) — fine.
- hunk 2: "**both**, not one" (barriers) — §9.2 has exactly two barriers, steps
  4 and 6. TRUE.
- hunk 2: "the **two** of §10.1's four vehicles §21.6 makes conforming"
  (retained context, not a `+` line, but re-checked): §21.6 does carry exactly
  two such rows — "An ignore-lane flag bit (16–31) is set" and "A
  user-metadata document carries an unrecognized `tarn.`-prefixed key". TRUE.
- hunk 2: "fixes what the output *is*, not which rules govern the writing of
  it" — no count. Fine.
- hunk 3: "**three** ways" — a count. **FALSIFIED on a reading**, see **B-06**.
- hunk 3: "**only** where those bytes already hold the channel's recorded
  fill" — tested against §20.3: a shrink that damages a prior-generation stored
  tile is barred "whether or not the new state still stores it", and
  superseding in the same commit does not rescue it ("superseding every tile of
  a layer and re-declaring it are one operation, and this bars it"). So there
  is no escape route and the "only" holds. TRUE — but the *unit* is wrong, see
  **B-03**.
- hunk 3: "no commit removes a layer at all" — §20.4 confirms. TRUE.
- hunk 3: "discloses nothing a reader could not already derive" — the fill is
  in the layer record's channel entry ([R-TYP-06]), so a reader can derive the
  byte values. TRUE for numeric and interleaved bool; for a packed bool plane
  the "bytes" framing is what B-03 is about.

### Check 6 — what else in this structure is still unconstrained?

**Hunk 2's structure — the compaction output's trailer and pre-trailer region.**
Enumerated every quantity the output can carry and asked what fixes it:

| Quantity | Fixed by | Status |
|---|---|---|
| front signature block | §6.1; now also the creation path | fixed (the repair *adds* an explicit warrant) |
| structure placement | free by §20.5, §5.2, [R-SLB-05] | deliberately free |
| directory + its CRC | [R-LIF-02] step 3, §20.4 | fixed |
| **pre-trailer pad length** | **[R-LIF-02] step 5, newly, via this repair** | **fixed — this is the repair** |
| pre-trailer pad content | unconstrained ([R-CNT-03] advises zero) | deliberately free |
| trailer magic / version_major | §6.2 | fixed |
| version_minor | §20.5 SHOULD ≥ input's, else [R-CNT-26] | fixed |
| flags (ignore lane) | [R-CNT-08] carry-forward | fixed |
| flags (incompat lane) | a conforming input has none set (§6.3 → compactor is a reader first) | fixed |
| generation | 1 | fixed |
| dir_offset / dir_length / committed_file_length | derived, §6.2 | fixed |
| file_id | fresh draw | fixed |
| reserved / trailer CRC | §6.2 | fixed |
| barriers 4 and 6 | newly owed | fixed |

No sibling quantity of the pad is left dangling: the repair pinned the one
member that was loose and everything adjacent was already pinned. **PASS.**

**Hunks 1 and 3's structure — a permitted shrink of a layer's geometry.**
Members: rank d, each Eᵢ, each Tᵢ, channel count, channel types, fills, layout,
linearization, codec, filter, A / S / A_slab, index_encoding, entry_count,
crc_of_crc_array, the extent slot. A shrink touches Eᵢ only, and its knock-ons
are: grid counts Gᵢ, N, the addressed-tile set, the padding-position set,
entry_count, extent_length, disk ordinals, the reference array. Two of those
are where the audit found something:

- the **padding-position set**: the repairs govern it in units of *bytes*, and
  R-SER-05 governs it in three units — "the recorded fill bytes for a numeric
  channel, the recorded fill byte for an interleaved bool channel, **the fill
  bit in a packed plane**". The bit sibling is unaddressed → **B-03**.
- **entry_count / extent_length**: unchanged under a padding-only shrink, but
  §20.3's consequence sentence says they must fall → **B-01**.

### Check 7 — analogies, verb against verb

**Hunk 2** carries the only explicit analogies. Three of them:

1. "A compactor **MUST follow** `[R-LIF-02]`'s creation path, **as §20.2
   obliges a creator**."
   - repair's governing verb: `MUST follow … [R-LIF-02]'s creation path`
   - cited rule's governing verb ([R-WRT-02], §20.2): `A creator **MUST
     follow** [R-LIF-02]'s creation path`
   - Same verb, same object, same modality. The two range over different
     actors, which is the point of the analogy, not a defect in it. **PASS.**
2. "the output has no prior trailer and stands at generation 1, **which is the
   case that path states**."
   - repair: `has no prior trailer` / `stands at generation 1`
   - [R-LIF-02]: `On creation there **is** no prior trailer … **with**
     generation 1`
   - Same predicates. The one gap the analogy has to jump is that R-LIF-02's
     opening subject is "A writer performing a **commit**", and §20.5 itself
     says a compaction is "a whole-file rewrite rather than a commit". The
     repair does not need the analogy to carry that weight: it states its own
     `MUST`, so the creation path is imported by §20.5's authority, not by
     R-LIF-02's own reach. **PASS.**
3. "The pad of step 5 and the barriers of steps 4 and 6 — both, not one — **are
   owed here as they are of a creator**."
   - repair: `are owed here`
   - §20.2: `the barrier, the pad, the generation-1 trailer …, and the barrier
     that makes the trailer durable ([R-LIF-02] steps 4–6 — both barriers, not
     one)`
   - Identical scope: steps 4, 5, 6. **PASS.**

Tested separately for each member the one sentence carries (pad; barrier 4;
barrier 6): the analogy holds for all three, because §20.2 states all three of
a creator and the compaction output satisfies the creation path's case
condition for all three.

**Hunk 3** has one: "§20.3 step 4 **permits** that shrink **only where** those
bytes already hold the channel's recorded fill".
- repair's verb: `permits … only where those **bytes** already **hold** the
  channel's recorded **fill**`
- cited rule's verb (§20.3): `a new padding position whose stored **byte**
  already **holds** the **fill `[R-SER-05]` fixes** … is not one`
- Same verb ("holds"). Same unit ("byte"/"bytes"). But **[R-SER-05]**, which
  §20.3 names as the thing that fixes it, does not range over bytes uniformly:
  "the recorded fill **bytes** for a numeric channel, the recorded fill **byte**
  for an interleaved bool channel, **the fill bit in a packed plane**." So the
  analogy is sound for two of the three units R-SER-05 distinguishes and
  unsound for the third → **B-03**. This is the check-7 shape exactly: one
  sentence supplying a quantifier for several instances individuated
  differently.

**Hunk 1** argues by no analogy; its relation to §20.3 is restatement, handled
under check 1.

---

## 3. The downstream sweep — passages outside every hunk

### 3.1 FINDING B-01 — §20.3 step 4's shrink-consequence sentence, quietly invalidated

Grep (whitespace-normalised, because the sentence wraps four times):

```
$ tr '\n' ' ' < spec/tarn.md | grep -o "Where a shrink is permitted[^.]*\."
Where a shrink is permitted the de-addressed tiles' extents become slack
(`[R-CNT-21]`), `[R-CNT-17]` obliges the smaller entry_count and so a
re-emitted index region, and every surviving stored tile is untouched.
```

That sentence is at spec/tarn.md:3055–3058, three sentences below the
carve-out both repairs now lean on, and in neither hunk.

It states, universally over permitted shrinks, three consequences:
(i) de-addressed tiles' extents become slack; (ii) [R-CNT-17] obliges a
smaller entry_count and therefore a re-emitted index region; (iii) surviving
stored tiles are untouched.

Under the padding-only shrink that hunks 1 and 3 promote, (ii) is **false**:

- [R-CNT-17] / §7.4: `entry_count` "equals the addressed-tile count (§11.2)";
  §11.2: the addressed-tile count is N (interleaved) or C·N (planar) with
  N = ∏ Gᵢ and Gᵢ = ⌈Eᵢ / Tᵢ⌉.
- A padding-only shrink is by construction one where no Gᵢ falls. Concretely:
  d = 1, T = 4, E from 10 to 9. G = ⌈10/4⌉ = 3 before and ⌈9/4⌉ = 3 after.
  Tile 2 covers positions 8–11; position 9 was real and is now padding. No
  tile leaves the addressed set. entry_count stays 3. extent_length stays
  3 × 20 + 4 = 64.
- So [R-CNT-17] obliges *nothing*, and the index region need not move. §20.3
  says so twice, itself, in the same step:
  - "**Every layer whose stored-tile set or index content this commit changes**
    has its tile-index region re-emitted in full" — this commit changes
    neither.
  - "A layer **whose record alone changes keeps its extent slot, pointing at
    the existing region**".
  A padding-only shrink is precisely the "record alone changes" case: the
  dimension entry's `extent u64` changes and nothing else does.

And (i) is vacuous under that shrink (the de-addressed set is empty), so the
sentence's whole apparatus describes only the de-addressing case. That is what
the pre-repair §11.1 Rationale also described — "permitted where it **only**
drops tiles out of the addressed set". Hunk 1 removed that framing from §11.1
and hunk 3 promoted the other case in §23.1; the §20.3 consequence sentence was
left standing at the old framing. Classic unswept restatement.

Two readings a competent implementer can take:

- **R1:** "Where a shrink is permitted … a re-emitted index region" is an
  obligation. An appender doing a padding-only shrink re-emits the layer's
  whole index region at a new placement (entries byte-identical), strands the
  old one as slack, re-points the extent slot.
- **R2:** the sentence describes the de-addressing case only; a padding-only
  shrink keeps its extent slot, and the file grows by a directory, a pad and a
  trailer alone.

Both outputs are conforming files: entry_count and extent_length are correct
in both, and re-emitting an identical index region at a new placement is
permitted (placement is free; the old region becomes slack, [R-CNT-21]). So the
**disputed file — the R2 output — is conforming**, and only R2 permits a
conforming appender to produce it. By the stated discriminating test, the
emittable set moves: **byte-level.** Two implementations given the identical
call ("shrink E from 10 to 9") differ on whether the appended bytes include a
64-byte index region and a re-pointed extent slot, and on the file's length.

A third reading is worse: an implementer may take the consequence sentence as
*definitional* of a permitted shrink — since its consequences cannot hold for a
padding-only shrink, that shrink is not permitted — which flatly contradicts
the two sentences above it and the two repairs.

Repair: bound the sentence to the case it describes, and state the other case's
consequences. E.g. "Where a permitted shrink drops tiles out of the addressed
set, their extents become slack ([R-CNT-21]) and [R-CNT-17] obliges the smaller
entry_count and so a re-emitted index region; where it only converts real
positions to padding, no grid count falls, entry_count is unchanged, and the
layer keeps its extent slot (§20.3's shape (c)). In both, every surviving
stored tile is untouched."

Related, and worth sweeping in the same edit: §20.3's **Example — shape (c)**
enumerates the directory-only commits as "clearing a slab declaration, renaming
a layer, or changing a channel's fill value on a layer with no padding position
and no pad bit". A padding-only shrink is now a fourth member of that list and
is not named. Non-normative, so I report it here rather than as its own
finding.

### 3.2 FINDING B-02 — §6.2 [R-CNT-05] stranded by hunk 2's reversal

```
$ tr '\n' ' ' < spec/tarn.md | grep -o "a longer gap is conforming[^.]*\."
a longer gap is conforming, and no conforming commit produces one.
```

spec/tarn.md:753–763, in [R-CNT-05]:

> "Those bytes — the **pre-trailer pad** — are slack (§5.2): … this
> specification does not constrain their content, and **bounds their number
> only through step 5 of the commit protocol**, which pads to the next 64-byte
> boundary (`[R-LIF-02]`) — **a longer gap is conforming, and no conforming
> commit produces one**."

The word "commit" there is load-bearing and deliberately narrow: §9.1 makes
commit and whole-file rewrite disjoint ("every conforming mutation of a file is
either a commit (§9.2) or a whole-file rewrite under a new file_id (compaction,
§20)"), and §20.5 itself says "a compaction is a whole-file rewrite rather than
a commit". Under the paragraph hunk 2 reverted, that narrowing had exact
residue — the reverted text said, in so many words, "two conforming compactors
given one input MAY emit outputs of different lengths, and a gap longer than a
commit would have produced is conforming — one of the writer obligations §2.3
names as no file-conformance violation." The two sentences were companions.

After the reversal, the compactor owes step 5's pad, so **no conforming actor
of any tier produces a longer gap**, and §6.2's exclusion of non-commits is
empty. The sentence remains literally true and its implicature — that
something conforming *does* produce one — is now false. §2.3's [R-CNF-02],
which names "§6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad" as
one of the two conduct carve-outs "this text states", still works: the carve-out
now says only that a file with an over-long gap is conforming even though the
writer that made it violated a writer obligation. That is coherent, so I do not
report §2.3.

Not byte-level: §20.5 now says `MUST`, and a descriptive sentence in §6.2 about
what a *commit* produces cannot be read as a licence overriding it. The cost is
a reader who consults §6.2 for the pad's scope and infers a compactor freedom
that no longer exists.

Repair: "…and no conforming writer produces one — a commit pads under
[R-LIF-02] step 5, and a compactor is held to the same step (§20.5,
[R-WRT-06])."

I also checked the two places that *were* wrong under the reverted paragraph
and are right again after it, as evidence the reversal is the correct
direction:

- **Appendix H, "Conforming writer"**: "follows the commit protocol **including
  both barriers** (§9.2)". Under the reverted paragraph a compactor owed
  neither barrier and this checklist line over-claimed for that tier. Now
  correct.
- **Appendix G item 8**: "A compactor's output is therefore reproducible **only
  modulo its trailer**". Under the reverted paragraph the output's *length* was
  free as well, so "modulo its trailer" was false. Now correct.

Neither needs an edit.

### 3.3 FINDING B-03 — the carve-out is stated in bytes; R-SER-05 has a bit

Both repairs state the padding carve-out over bytes:

- hunk 1: "a new padding position whose **stored byte** already holds the fill"
- hunk 3: "permits that shrink only where **those bytes** already hold the
  channel's recorded fill"

§14.5 [R-SER-05], the rule that fixes the content in question:

> "at every padding position, a writer MUST encode, for each channel the
> position carries, that channel's fill value — the recorded fill **bytes** for
> a numeric channel, the recorded fill **byte** for an interleaved bool
> channel, **the fill bit in a packed plane**."

And §21.4's row T4 enumerates the four instances explicitly:

> "| T4 | A padding position does not encode, for each channel it carries, that
> channel's recorded fill value | interleaved numeric fill bytes; interleaved
> bool fill byte; planar numeric plane fill bytes; **packed planar bool plane
> fill bit** | verifier | certification | `[R-SER-05]` |"

In a planar bool layer (§14.3) the decoded plane is "the tile's P values
bit-packed LSB-first: value k occupies bit k mod 8 of byte k div 8", so a
padding position there has **no stored byte of its own** — it is one bit of a
byte shared with up to seven other positions, real ones included. A shrink
that turns a real position into padding in such a plane is perfectly reachable:
extents (10,), tile extent (16,), one bool channel, fill false, one stored
tile; shrink E to 9. Position 9 becomes padding; R-SER-05 requires its *bit* to
be the fill bit; if that bit is already 0, nothing §14 fixes for the stored
tile changes and §20.3's carve-out ought to apply.

But the carve-out as restated names a byte. Two readings:

- **R1:** "stored byte" is loose for "the stored bits at that position"; the
  shrink is permitted whenever the governing bit already holds the fill bit.
- **R2:** the carve-out speaks of a byte because it means a byte; a packed
  plane has no per-position byte, so the carve-out names no case there and any
  shrink creating a new padding position in a bool plane is barred, forcing a
  new layer or a whole-file rewrite ([R-LIF-01], §20.5).

The disputed file — layer at E = 9, the stored plane's bytes unchanged, its
padding bits all fill — is **conforming**: T4 and T5 are satisfied and no other
row fires. Only R1 lets a conforming appender produce it as a commit. The set
moves: **byte-level.** Implementation A appends a directory, pad and trailer;
implementation B refuses the commit and rewrites the file under a fresh file_id
at generation 1.

The document is precise about this distinction everywhere else — §14.3's Note
("Pad bits are not padding positions … A plane can have many padding positions
and no pad bits — §14.5 gives both their content"), §21.7's triple ("a padding
position, a pad bit, or an interleaved boolean"), T4's four-instance list — so
the byte framing reads as an oversight rather than a deliberate narrowing.

Repair: in both repaired sentences and in §20.3's two normative occurrences,
replace "whose stored byte already holds the fill" with "whose stored content
at that position already holds the fill `[R-SER-05]` fixes there — the fill
bytes, the fill byte, or the fill bit, per §14.5". (§20.3's occurrences are
outside the hunks but must be swept in the same edit or the normative text and
the restatements diverge again.)

Note this is also the check-6 shape in its pure form: the repair pinned the
numeric and interleaved-bool members of a set and left the packed-plane sibling
governed by nothing, and the text reads as perfectly correct about the members
it mentions.

### 3.4 FINDING B-04 — hunk 1's "the other" is a closed list with a third member

Hunk 1: "…and permitted wherever it does not: dropping tiles out of the
addressed set, whose extents then become slack, **is the ordinary case, and** a
new padding position whose stored byte already holds the fill **is the other**."

Two items, presented as covering the field. §20.3's bar is quantified over
"any tile the layer **stores** in the generation this commit supersedes", so a
third case is permitted with no fill precondition at all: **a shrink whose new
padding positions all fall in tiles the superseded generation did not store**
(sentinel entries, §15.2). Such a tile "carries no §14 obligation" — §20.3's own
words for the de-addressed case apply a fortiori to a tile that was never
stored — so the shrink alters nothing §14 fixes for any stored tile and is
permitted outright.

Worked instance: d = 1, T = 4, E from 10 to 9, tiles 0 and 1 stored, tile 2
(covering 8–11) unstored. Position 9 becomes padding. No tile leaves the
addressed set, so item one does not apply; there is no stored byte at that
position, so item two does not apply. Yet the shrink is plainly permitted.

Also, the two named items are presented as alternatives ("the ordinary case …
the other") when they routinely co-occur: E from 10 to 5 at T = 4 drops tile 2
*and* turns positions 5–7 of tile 1 into padding.

Not byte-level: [R-CNF-01] makes the Rationale non-normative, so an
implementer may conform while ignoring it, and §20.3's normative text is
correct. It is still a false statement in the document, in the exact block this
round repaired, and this project's stated history is that Rationale/normative
divergence is how rounds are lost.

Repair: drop the closure. "…and permitted wherever it does not — a tile dropped
out of the addressed set carries no §14 obligation and its extent becomes
slack; neither does a tile the superseded generation did not store; and a new
padding position whose stored content already holds the fill alters nothing.
A shrink can do several of these at once."

### 3.5 FINDING B-05 — hunk 2's "as §20.2 obliges a creator" is wider than its next sentence

The repair's first sentence is blanket:

> "A compactor MUST follow `[R-LIF-02]`'s **creation path**, as §20.2 obliges
> a creator"

§20.2's [R-WRT-02] does not stop at the path. It closes:

> "Content obligations travel with the structures: fill-encoded edge padding
> (`[R-SER-05]`), boolean byte values (`[R-SER-08]`), and gaps zeroed as
> `[R-CNT-03]` advises."

Does "as §20.2 obliges a creator" import those? The next sentence narrows to
"the pad of step 5 and the barriers of steps 4 and 6", which argues no. But the
narrowing sentence is offered as a *consequence* ("The pad … and the barriers …
are owed here"), not as a limit, and a reader can take the blanket sentence at
its word.

If imported, it collides with two statements in the same passage, neither
touched:

> "a violation latent in a structure it carries forward verbatim travels into
> its output (`[R-WRT-01]`) — its verification depth is `[R-WRT-09]`'s and
> **reaches no decoded content**."

A creator owing [R-SER-05] must get its padding right; a compactor that must
*guarantee* [R-SER-05] for tiles it copies would have to decode every tile,
which [R-WRT-09] expressly does not require, and would have to refuse an input
whose padding is wrong, which §20.5's own "a violation … travels into its
output" says it does not.

Not byte-level: the output at issue carries a T4 or T5 register-row violation,
so it is nonconforming under both readings and the emittable set does not move.
The fork is over whether the compactor emits it or refuses — a behaviour
difference on a nonconforming input, which the stated test excludes.

Repair: make the blanket sentence explicit about what it imports. "A compactor
MUST follow `[R-LIF-02]`'s **creation path** — its ordering, not §20.2's
content obligations, which [R-WRT-01] and [R-WRT-09] already settle for a
compactor — the output having no prior trailer and standing at generation 1,
which is the case that path states."

### 3.6 FINDING B-06 — hunk 3's "three ways" and §23.2's cross-reference

§20.3 step 4 distinguishes two dispositions of a stored tile in the same
clause:

> "with entries for tiles this commit **stores or supersedes** written to their
> new state, entries for tiles that **become unstored** written as the
> sentinel"

Unstoring a tile — writing the sentinel where a payload was addressed — makes
its samples read as fill and drops its payload to slack. It is neither
superseding (no new bytes are written for it), nor a shrink, in that clause's
vocabulary. §23.2 [R-PRV-03] treats it as a distinct case and sends the reader
to §23.1 for it:

```
$ tr '\n' ' ' < spec/tarn.md | grep -o "unstored by a later commit[^;]*;"
unstored by a later commit leaves its earlier payload in the file as slack
(§23.1) — so the index publishes which regions were written without disclosing
what is in them;
```

Hunk 3's enumeration is "three ways — superseding it, a shrink that
de-addresses tiles, and a shrink that turns a stored tile's real positions into
padding without de-addressing it". Unstoring is in none of them unless
"superseding it" is read in §5.2's broad sense ("everything an earlier commit
superseded"), which conflicts with §20.3's narrow use two sections earlier.

This is pre-existing — the "two ways" text had the same gap — but the repair
re-authored the count and had the sweep in front of it, and §23.2's citation
into §23.1 now points at a list that does not contain the case it cites for.

Not byte-level: [R-PRV-01]'s `MUST NOT` is quantified over "any commit that
makes sample data unreachable", which covers unstoring regardless of the
enumeration, so no implementation's accept/reject or emitted bytes turn on it.

Repair: "A commit removes sample data four ways — superseding a stored tile's
bytes, unstoring it (§20.3 step 4 writes the sentinel), a shrink that
de-addresses tiles, and a shrink that turns a stored tile's real positions into
padding without de-addressing it — and a dropped ancillary record's extent
(§20.4) goes the same way… The first three leave the bytes in the file as slack
([R-CNT-21])…"

### 3.7 Dependent passages checked and found still correct

Every place I could reach that could plausibly have depended on the old
answers, with the verdict:

Depending on hunk 2's reversed paragraph (compactor freedoms):

- **§2.3 [R-CNF-02]**, the two named conduct carve-outs. Still correct: a
  writer that over-pads still violates a writer obligation without making the
  file nonconforming. **Still correct.**
- **§6.3 [R-CNT-08]**, "A compactor, though its output is a new file, carries
  the input's unknown ignore-lane bits into its output trailer rather than
  writing flags = 0". Survives the creation-path binding, because §20.2's own
  text does not mention flags and §20.5 states the carry-forward explicitly.
  **Still correct.**
- **§9.4 [R-LIF-04]** ("A writer beginning a commit against an existing file
  MUST establish F…"). Scoped to commits against an existing file; a compactor
  writes a new file. **Still correct.**
- **§21.6's slack row** ("alignment gaps, the pre-trailer pad, superseded
  structures | Slack: unconstrained content, no conformance requirement").
  About content, not length. **Still correct.**
- **§5.2 [R-CNT-21] / [R-CNT-03]** ("Writers SHOULD zero the gaps they
  create — … and the pre-trailer pad"). Unaffected by pinning the pad's length.
  **Still correct.**
- **§21.7's compactor accounting**: "§20.5's **four** obligations on a
  compacted file's trailer (`[R-WRT-06]`) — its fresh `file_id` draw, its
  generation, the unknown ignore-lane bits it MUST carry forward, and the floor
  its version_minor SHOULD take — are unwitnessed…". I counted §20.5's trailer
  obligations after the repair: fresh file_id, generation 1, ignore-lane
  carry-forward, version_minor floor. Still exactly four; the pad is not a
  trailer field and the barriers are not bytes. And the shared reason ("the
  output carries no record that it is a compaction output at all") still holds
  for all four. The two obligations the repair adds are unwitnessed too, but
  they are unwitnessed for reasons §21.7 does not owe an entry for — a commit's
  step-5 pad and its barriers are equally unwitnessed for creators and
  appenders and §21.7 lists neither, so no new *class* appears. **Still
  correct.** Checked deliberately, because this is the passage the charter
  flags and because it names rules by identifier.
- **§20.5's own "Neither obligation has a witness in the output alone
  (§21.7)"** — refers to the two version_minor obligations, unchanged.
  **Still correct.**
- **Appendix H, "Conforming updater"** — lists no compaction-specific
  obligation, so the reversal does not reach it. **Still correct.**
- **Appendix H, "Conforming writer"** and **Appendix G item 8** — see §3.2;
  the reversal restores both. **Still correct.**
- The removed `SHOULD` ("A compactor SHOULD make its output durable before
  anything discards the input; what discards it is outside this
  specification"). Its first half is subsumed by step 6's barrier, which now
  applies; its second half survives verbatim in spirit at §23.1 [R-PRV-02] —
  "the input persists, unmodified, until something outside this specification
  deletes it". **No gap left.**

Depending on hunks 1 and 3 (the promoted padding-only shrink):

- **§20.3 step 4's shrink-consequence sentence** — **B-01**, invalidated.
- **§20.3's Example shape (c)** — now under-enumerates; folded into B-01.
- **§20.3's "Every layer whose stored-tile set or index content this commit
  changes has its tile-index region re-emitted in full"** — correct, and it is
  what B-01's sentence contradicts.
- **§21.7's account of the step-4 bar** ("witnessed only where the affected
  tiles remain stored, and then only for part of what it bars … A change
  reaching a byte §14 structurally constrains — a padding position, a pad bit,
  or a boolean byte — fires §21.4's content rows"). A permitted padding-only
  shrink produces no violation, so there is nothing for it to witness, and the
  passage does not claim otherwise. **Still correct**, though I note in passing
  that §21.7's closing clause covers only "a commit that **supersedes** every
  tile it would have damaged", while §20.3 sends the reader to §21.7 for the
  de-addressing and unstoring rescue cases too ("§21.7 records the
  consequence"). That is a pre-existing narrowness with no connection to these
  three repairs, so I record it here rather than as a finding.
- **§23.2 [R-PRV-03]** — the disclosure inventory. The third way discloses
  nothing new (the bytes were already the published fill), so no line needs
  adding; its unstoring cross-reference is **B-06**.
- **§13.3, §15.2, §21.6's sentinel row** — about unstored tiles reading as
  fill; untouched by any of this. **Still correct.**
- **§11.2, §11.3, §11.4** — grid arithmetic, padding positions, ordinals. A
  shrink that leaves every Gᵢ unchanged renumbers no ordinal ([R-GEO-06]), so
  nothing there moves. **Still correct.**
- **§16 slab/alignment consequences in step 4** ("an aligned layer's stored
  tiles — every one the new state keeps … satisfy its invariant"). A
  padding-only shrink moves no tile, so the invariant is preserved
  automatically. **Still correct.**

### 3.8 The reverse direction — does any repaired sentence duplicate or contradict what existed?

- Hunk 1 duplicates §20.3 step 4 by design; a Rationale restating its
  normative rule is this document's convention and [R-CNF-01] handles the
  force question. No contradiction with §20.3's text, only with §20.3's
  consequence sentence (B-01) and only by way of under-enumeration (B-04).
- Hunk 2's "It MUST mint a fresh file_id … and generation 1" (retained) and the
  new "stands at generation 1" say the same thing twice within four lines.
  Harmless: the second is the premise of the case argument, not a second rule.
- Hunk 2's new material does not contradict §20.5's placement freedom, its
  refusal rules, its regeneration rules, or [R-WRT-09]'s depth — checked each.
  The one live tension is B-05.
- Hunk 3 does not duplicate §20.3; it accounts for it in privacy terms, which
  is §23's job.

---

## 4. Verdict

Six findings. One (B-01) is a passage in no hunk, unchanged, and made false by
the repairs — the shape this role exists to catch; it is byte-level. Two more
are byte-level (B-03) or stranded-by-reversal (B-02). Three are documentation
defects in or beside the repaired text (B-04, B-05, B-06).

Checks that passed cleanly, per hunk: citations (all 18 opened, all resolve),
normative placement (all three land where they must, and hunk 1's Rationale has
a correct normative home), tense and quantifier (all three), analogy verbs (all
four analogies, member by member).
