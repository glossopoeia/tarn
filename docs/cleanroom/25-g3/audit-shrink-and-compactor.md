# Round 25 repair audit — hunk-01 (§20.3 step 4 shrink) and hunk-02 (§20.5 compactor)

Working transcript. Written for someone checking my work.

## 0. Disclosure

Files opened: the two hunk files named in my charter
(`.../r25audit/hunk-01.diff`, `.../r25audit/hunk-02.diff`) and
`/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`. Nothing else.
I did not read `full.diff`, other hunk files, `docs/`, `conformance/`,
`registry.json`, git history, or the web. I did not list the r25audit
directory. Commands run: `sed -n`, `awk`, `grep -n`, `wc -l`, `cut`,
`sort`, `uniq` — all against `spec/tarn.md` and the two hunk files only.

Context I did not ask for **did appear** before I began: a project
instruction file pointer (CLAUDE.md → AGENTS.md), a user auto-memory index
listing six memory-file titles about this project's working cadence,
naming rules, verifier-failure shapes, and the §21 register, and an
environment/git block naming the current branch and the five most recent
commit subjects. Those commit subjects name a round number, an ADR number,
and phrases including a shrink bar and a compactor. I did not open any of
those files and I have not used any of that material as evidence. Every
conclusion below is traced to a line of `spec/tarn.md` or of my hunk
files, quoted and line-numbered so it can be re-derived without them.
Disclosing rather than acting on it.

---

## 1. Hunk 1 — §20.3 step 4, the shrink paragraph (lands at line 3029)

### 1.1 What I read

Read §20.3 step 4 whole, lines 2977–3068, plus steps 5–6 and the Note and
Example that close §20.3 (to 3145). Read the bar paragraph (2993–3027) and
the shrink paragraph (3033–3060) as separate units before comparing them
to the diff.

The **bar** (lines 2993–3009), verbatim:

> A commit MUST NOT change a layer's declarations in a way that alters,
> for any tile that layer stores **in the generation this commit
> supersedes**, what §14 fixes for its stored bytes or how they decode —
> the set of padding positions (§11.3) and the content `[R-SER-05]` fixes
> there, the decoded size, the byte offset of any sample within the
> decoded tile image, or the codec and filter that produced the stored
> bytes.

and its **carve-out** (3005–3011):

> The test is the effect on such a tile, and the list names where that
> effect arises rather than standing on its own: a change that leaves
> every one of those tiles' stored bytes meaning exactly what they
> meant — a filter whose mandated stride makes it the identity
> (`[R-COD-10]`), or a new padding position whose stored byte already
> holds the fill `[R-SER-05]` fixes — is not what this bars.

So the bar's test is **effect on the meaning of a prior-generation stored
tile's bytes**, quantified over "any tile that layer stores in the
generation this commit supersedes". The listed items are sites where that
effect arises, not independent prohibitions. The carve-out has a general
clause plus two named instances.

The repair (3043–3050):

> generation's, so a shrink that alters what §14 fixes for a tile stored
> there is barred whether or not the new state still stores it. What
> counts as such an alteration is the bar above and nothing else, its
> carve-out included — a new padding position whose stored byte already
> holds the fill `[R-SER-05]` fixes is not one, so a shrink producing only
> those is permitted here exactly as it is there, and this sentence
> answers the rescue question rather than restating the test.

Replacing: "a shrink that turns real positions into padding of a tile
stored there is barred whether or not the new state still stores it."

### 1.2 The rule the repair adopts, in my words

A commit may shrink a layer's dimension extent even where the shrink turns
real sample positions of a **still-stored prior-generation tile** into
padding positions, provided every such newly-padding position's stored
bytes already hold that channel's fill. Unstoring the tile in the same
commit neither rescues nor is needed. What makes a shrink illegal is
determined solely by the bar above, carve-out and all; nothing in the
shrink paragraph adds to it.

### 1.3 Direction of the permission — WIDENS

Old text: turning a real position of a prior-generation stored tile into
padding was barred **flatly** ("turns real positions into padding … is
barred"). New text: barred only if it "alters what §14 fixes", and the
carve-out expressly says a fill-holding new padding position is not such
an alteration.

Files that move across the boundary: take a layer, extents (8, 8), tile
extents (4, 4), one uint16 channel, fill 0xABCD, interleaved. Grid counts
⌈8/4⌉ = 2 on both axes, N = 4, all four tiles stored in generation g.
Commit g+1 re-declares extents (7, 8). Grid counts are still ⌈7/4⌉ = 2 and
⌈8/4⌉ = 2, so **no tile is de-addressed**; the two tiles at tile-coordinate
1 on axis 0 each gain a plane of padding positions at coordinate 7. Suppose
every one of those positions already stores `CD AB`. Then:

- decoded size (P·Q) is unchanged — P = ∏Tᵢ and the tile extents did not
  move;
- every sample's byte offset is unchanged;
- codec and filter are unchanged;
- the set of padding positions changed, and the content at every new
  padding position is already the fill `[R-SER-05]` fixes.

Under the old sentence no conforming writer could emit generation g+1.
Under the new sentence a writer may. The resulting file is conforming: T4
("A padding position does not encode … that channel's recorded fill
value", line 3546) does not fire because the bytes are fill; no other row
is reachable. So the emittable set genuinely moves — this repair closes a
byte-level fork by widening.

### 1.4 Check 1 — tense and quantifier

Bar: "for **any** tile that layer stores **in the generation this commit
supersedes**".
Shrink paragraph, opening (unchanged, 3034–3036): "a shrink is permitted
exactly where it alters nothing §14 fixes for **any** tile the layer
**stores in the generation this commit supersedes**".
Repair (3043–3044): "a shrink that alters what §14 fixes for **a tile
stored there**" — "there" resolving to "the superseded generation" named in
the immediately preceding clause (3042–3043: "the quantifier is the
superseded generation's").

Generation: superseded, in all three. Set: any prior-generation stored tile
of the layer whose declarations changed, in all three. Verb: bar "alters …
what §14 fixes"; repair "alters what §14 fixes". Match. PASS.

The repair also *widens the restatement* relative to the sentence it
replaces — "turns real positions into padding" named one of the bar's list
items; "alters what §14 fixes" names all of them. That is a faithful
restatement of the bar, so the widening is a correction, not an error.

### 1.5 Check 2 — citations

- `[R-SER-05]` (§14.5, 1954–1962). Read. "at every padding position, a
  writer MUST encode, for each channel the position carries, that
  channel's fill value — the recorded fill bytes for a numeric channel,
  the recorded fill byte for an interleaved bool channel, the fill bit in
  a packed plane." The repair's phrase "the fill `[R-SER-05]` fixes" is
  accurate. PASS (with the sub-point at §1.9 below about "byte").
- §14 (1789–1984). Read all of §14.1–§14.5. The bar's list — padding-position
  set and content, decoded size, sample byte offsets, codec/filter — maps
  to `[R-SER-06]`/`[R-SER-02]`/`[R-SER-03]`/`[R-SER-07]`/`[R-SER-05]`.
  "what §14 fixes for its stored bytes or how they decode" is a fair
  handle for those. PASS.
- §21.7 (3658–3728). Read. The sentence the repair leaves standing —
  "§21.7 records the consequence — that this is precisely where the bar has
  no witness, the live state being clean" — resolves to 3711–3715: "a
  commit that supersedes every tile it would have damaged leaves the live
  state clean, so the bar is unwitnessed there for the same reason
  `[R-LIF-01]` is". PASS. §21.7 also says (3691–3694) "A change reaching a
  byte §14 structurally constrains — a padding position, a pad bit, or a
  boolean byte — fires §21.4's content rows", which is consistent with the
  widened permission: a new padding position that already holds fill fires
  nothing, so there is nothing for a row to catch. PASS.
- "the bar above" — the referent is unambiguous: the immediately preceding
  MUST NOT at 2993. PASS.
- `[R-CNT-21]`, `[R-CNT-17]` in the untouched sentences — read (630–655,
  and §15/§7.4 for extent_length). Not part of the repair; consistent.

### 1.6 Check 3 — normative placement

Lines 3029–3060 are a numbered-step continuation paragraph in §20.3. I
dumped the first four characters of every line in 3029–3060: no line
begins with `>`. The repair sits in normative text and the rule it states
has force. PASS.

### 1.7 Check 4 — contradiction inside the passage

I read the whole of step 4 (2977–3068) and steps 5–6 looking for a
carve-out the widened licence now collides with. Candidates examined:

- 3053–3055 "Where a shrink is permitted the de-addressed tiles' extents
  become slack (`[R-CNT-21]`), `[R-CNT-17]` obliges the smaller
  entry_count and so a re-emitted index region, and **every surviving
  stored tile is untouched**." Under the newly permitted shrink every
  surviving stored tile *is* untouched byte-for-byte, so this holds. It
  does mention only the de-addressing shape, but it does not deny the
  other. No contradiction.
- 3033–3034 "the bar above is the whole of the test" (untouched). This is
  an exhaustive claim that a shrink owes nothing beyond the bar, and step
  4's own closing sentences (3064–3068) require `[R-SLB-04]` re-establishment
  or clearing and `[R-SLB-01]` satisfaction after a commit; §16.2's
  `[R-SLB-04]` reads "A writer or updater whose commit changes the
  stored-tile set, the run partition, or the byte placement of any run of
  a slab-declared layer MUST either re-establish the invariants … or clear
  the declaration". A shrink that drops grid counts renumbers ordinals and
  so changes the run partition. Strictly, then, the bar is *not* the whole
  of what a shrinking commit owes. But: this sentence is untouched by the
  repair, the repair's own exhaustive claim is scoped narrowly ("what
  counts as **such an alteration**"), and the same step states the slab
  and alignment obligations explicitly four sentences later. I judged this
  a pre-existing infelicity, not a defect in this repair, and did not
  raise it.
- 3007–3011, the bar's carve-out: the repair imports it rather than
  colliding with it.
- 3059–3063, the SHOULD about producing a new file: consistent.

No contradiction inside the passage. PASS.

### 1.8 Check 5 — exhaustive claims in the repaired text

- "the bar above **and nothing else**" — a claim about the whole document.
  I grepped the test's own words rather than an identifier:
  `grep -n "14 fixes\|fixes for\|what §14\|alters\b\|alteration"` gives
  exactly: 1487, 2995–2997, 3035, 3038, 3043, 3045, 3710. 3710 is §21.7
  about a sample's byte offset, unrelated. **1487 is a third site stating
  the test** — §11.1's Rationale. See finding A-02.
- "its carve-out **included**" — true of the bar's carve-out at 3005–3011.
- "a shrink producing **only** those is permitted" — see §1.9.
- "this sentence answers the rescue question rather than restating the
  test" — a claim about its own function; true as written.

### 1.9 Check 6 — what the structure still leaves open

Structure governed: a layer's dimension-extent declaration and its effect
on the prior generation's stored tiles. Every quantity a shrink of Eᵢ can
move, and where each is fixed:

| Quantity | Fixed by |
|---|---|
| set of padding positions of a still-addressed tile | the bar + its carve-out — this repair |
| content required at a padding position | `[R-SER-05]`, unchanged |
| addressed-tile set / grid counts | 3037–3040 (untouched), `[R-GEO-03]` |
| entry_count, extent_length, index re-emission | `[R-CNT-17]`, 3054 |
| disk ordinals of surviving tiles | `[R-GEO-06]`, cited at 2987 |
| decoded size, value count | unmoved by an extent shrink (P = ∏Tᵢ) |
| sample byte offsets within the image | unmoved |
| codec, filter | unmoved |
| slab run partition | `[R-SLB-04]`, 3064–3065 |
| per-tile alignment | `[R-SLB-01]`, 3066–3068 |
| `[R-COD-07]` lz4 cap over addressed tiles | strictly loosened by a shrink |
| Eᵢ = 0 as a shrink target | `[R-GEO-01]`/`[R-GEO-02]` permit it |

One sibling is named by the repair's permission in a form that does not
describe it: **the packed planar bool plane**. `[R-SER-05]` fixes padding
content through four vehicles, and T4's Instances cell (line 3546)
enumerates them: "interleaved numeric fill bytes; interleaved bool fill
byte; planar numeric plane fill bytes; **packed planar bool plane fill
bit**". The repair's permission is quantified as "a new padding position
whose stored **byte** already holds the fill" and then "a shrink producing
only **those**". In a packed plane a padding position is one *bit* of a
byte that also carries seven real values; no byte "holds the fill". The
carve-out's general clause ("a change that leaves every one of those
tiles' stored bytes meaning exactly what they meant") does rescue it, and
the repair imports that clause by "its carve-out included" — so a careful
implementer gets there. Recorded as finding A-07, lowest severity, not
byte-level, because both readings are available only to a reader who
ignores the imported general clause.

### 1.10 Check 7 — the analogy

The repair argues by analogy once: "permitted **here exactly as it is
there**".

- Repair's governing verb (here): "a shrink producing only those **is
  permitted**".
- Cited passage's governing verb (there): "…**is not what this bars**".

Not the same verb. "Not barred by this bar" is narrower than "permitted",
because other rules could bar it. Within this paragraph the gap is closed
by the untouched opening clause "the bar above is the whole of the test",
which asserts the equivalence. So the analogy holds *given* that clause,
and I checked whether the clause is true for the constructed case: for the
(8,8)→(7,8) shrink above, no grid count falls, so no ordinals renumber, no
run partition changes, `[R-SLB-04]` is not triggered, entry_count is
unchanged, and the file is conforming. Both passages really do permit the
case. PASS.

Ranges compared: "a shrink producing only those" ranges over commits;
"a new padding position whose stored byte already holds the fill" ranges
over positions; the bar ranges over tiles. Each quantifier is over the
right thing for its sentence, and the chain composes: for every
prior-generation stored tile, for every position that newly becomes
padding, the stored byte already holds fill. One sentence, one shape —
this is not the several-rows-under-one-analogy shape. PASS, except for the
one vehicle at §1.9.

### 1.11 Restatements the repair should have swept

Two, found by grepping the rule's words, not its identifier.

**(a) §23.1, `[R-PRV-01]`, lines 3936–3946 — NORMATIVE.**

> A commit removes sample data two ways — superseding it, and a shrink
> that de-addresses tiles (§20.3 step 4) — and a dropped ancillary
> record's extent (§20.4) goes the same way; no commit removes a layer at
> all. In each case the bytes remain in the file as slack (`[R-CNT-21]`),
> readable by anyone with the bytes and a hex editor…

Under the old shrink sentence this enumeration was exactly right: a shrink
could only ever remove data by de-addressing tiles, because turning real
positions into padding was flatly barred. The repair creates a **third
way**: my (8,8)→(7,8) case removes a whole plane of sample positions from
the reference array while de-addressing no tile at all. And for that third
way the second sentence is false as well — those bytes do **not** remain
in the file as slack; they remain inside a live, addressed, checksummed
stored tile as padding content. Finding A-01. The MUST NOT that follows is
quantified over "any commit that makes sample data unreachable", so the
prohibition itself survives; the enumeration and the slack claim do not.

**(b) §11.1's Rationale, lines 1484–1490 — non-normative.**

> §20.3 states normatively, and governs, what a commit may do to a layer
> that already stored tiles in the generation a commit supersedes: a
> shrink is barred wherever it alters what §14 fixes for such a tile —
> whether or not the new state still stores it — and permitted where it
> only drops tiles out of the addressed set, whose extents then become
> slack.

This is the same "alters what §14 fixes" phrase the repair had to
disambiguate at §20.3 — and here it stands without the carve-out, followed
by a permission clause naming only the de-addressing shape. Finding A-02.

Other sites checked and clean: §20.3's own Note and Example (3076–3145);
§20.4 shape (c) at 3125–3132, which is about *fill* changes and remains
true; §21.7's account (3689–3715); §5.2's slack rules.

---

## 2. Hunk 2 — §20.5, the compactor paragraph (lands at line 3207)

### 2.1 What I read

Read §20.5 whole, 3197–3342 — `[R-WRT-06]` (3199–3261), `[R-WRT-07]`
(3263–3296), the Example, and `[R-WRT-09]` (3331–3338). Then §9.1–§9.4
(1154–1258), §6.2 (735–784), §6.3 (785–824), §6.4 (826–866), §5.1–§5.2
(555–690), §7.1 (868–898), §2.1–§2.5 (96–279), §20.1–§20.2 (2900–2932),
§21.7, Appendix G (4260–4399), Appendix H (4400–4471).

The repair, verbatim, lines 3223–3240 (no line begins with `>`; it sits
inside `[R-WRT-06]`, whose identifier closes at 3261):

> `[R-LIF-02]`'s commit protocol does not bind a compactor. That protocol
> is stated for a commit, and `[R-LIF-01]` makes a compaction a whole-file
> rewrite under a new file_id rather than a commit, so neither its barrier
> ordering nor its step 5 pad reaches this tier — where §20.2 binds a
> creator to that path by name and §20.3 step 6 binds an appender, this
> section deliberately does not. Two consequences follow and are intended.
> **The output's pre-trailer gap is fixed by nothing.** … **And no
> barrier ordering is owed within the output.** …

### 2.2 The rule the repair adopts, in my words

A compactor is under none of `[R-LIF-02]`'s six steps. Concretely: it need
not pad to the next 64-byte boundary before its output trailer (so the
output's pre-trailer gap may be arbitrarily long, subject only to the
trailer's 64-alignment), and it need not issue a durability barrier
between the output's content and the output's trailer, nor after the
trailer. It SHOULD make the output durable before anything discards the
input.

### 2.3 Check 2 — citations, one by one

- **`[R-LIF-01]`** (§9.1, 1158–1163). "every conforming mutation of a file
  is either a commit (§9.2) or a whole-file rewrite under a new file_id
  (compaction, §20)." The paragraph says `[R-LIF-01]` "makes a compaction a
  whole-file rewrite under a new file_id rather than a commit". The
  disjunction does say that — *about the mutation*. It classifies the
  **operation**, not the writing of the output file, and it is quantified
  over "mutation of a file". Producing a brand-new output file is not a
  mutation of any file, so `[R-LIF-01]` is silent on which rules govern the
  writing of the output. PARTIAL PASS — it supports "not a commit" and
  does not support "so `[R-LIF-02]` is silent here". Feeds A-03.
- **`[R-LIF-02]`** (§9.2, 1166–1185). First paragraph: "A writer
  performing a commit MUST, in order: …". Second paragraph, same
  requirement: "**On creation there is no prior trailer: the writer first
  emits the front signature block (§6.1) — whose durability the barriers
  of steps 4 and 6 cover — then performs steps 2–6, writing beginning at
  offset 16, with generation 1.**" The repair's warrant, "That protocol is
  stated for a commit", is true of the first paragraph and **false of the
  second**, which is stated for *creation* and is the only paragraph that
  fits a compactor's situation (no prior trailer, generation 1, front
  block first). FAIL. Finding A-03.
- **§20.2** (2919–2932). "A creator MUST follow `[R-LIF-02]`'s creation
  path". The paragraph's claim that §20.2 "binds a creator to that path by
  name" is textually correct. But §20's preamble (2896–2899) says this
  section "consolidates — each step cites the rule whose outcome governs
  it", so §20.2 is a consolidation of §9.2, not the source of the
  obligation; the expressio-unius inference from §20.5's silence is
  therefore weak. PASS as to the words, weak as warrant. Feeds A-03.
- **§20.3 step 6** (3071–3074). "**Commit** (`[R-LIF-02]` steps 4–6):
  barrier; pad; trailer …". Correct as cited. PASS.
- **§6.2** (753–762). "Writers MUST place the directory so that no
  structure lies between its end and the trailer. Those bytes — the
  pre-trailer pad — are slack (§5.2): … bounds their number only through
  step 5 of the commit protocol, which pads to the next 64-byte boundary
  (`[R-LIF-02]`) — a longer gap is conforming, and no conforming commit
  produces one." The repair's use ("requires the trailer to occupy the
  file's final 64 bytes and bounds the gap ahead of it only through step
  5") is accurate. PASS. Note that §6.2's closing clause "no conforming
  commit produces one" survives untouched, because a compaction is not a
  commit under the new rule.
- **§2.3 / `[R-CNF-02]`** (146–156). "A writer obligation whose violation
  this specification expressly declares not to be a file-conformance
  violation **binds the actor in the same way**; §6.3's flags = 0 against
  a set ignore-lane bit and §6.2's pre-trailer gap longer than
  `[R-LIF-02]` step 5's pad are the cases this text states". The repair
  cites this for "a gap longer than a commit would have produced is
  conforming". That much §2.3 does say. What §2.3 *also* says at that
  exact spot is that the obligation binds the actor — a general clause
  about writers, naming this very case. The paragraph's "fixed by nothing"
  has to clear it and does not name it. Folded into A-03.
- **"one of the writer obligations §2.3 names"** — a category slip (a gap
  is not an obligation), harmless in itself; the substance is in A-03.

### 2.4 Check 1 — tense and quantifier

The paragraph ranges over "a compactor" (the tier §20.1 defines at
2907–2909) and over "the output". Both are the right sets: §20.5 is the
compactor's section and the claims are about the output file, not the
input. "Two conforming compactors given one input MAY emit outputs of
different lengths" — note this was already true before the repair, since
`[R-WRT-06]`/`[R-WRT-07]` at 3263 give the compactor free placement
("preserves no placement … free to place structures anywhere §5.2
admits"), so slack between structures already varies the length. The
sentence adds a *further* degree of freedom (the gap), which is the part
that needs a warrant. PASS on quantifiers.

### 2.5 Check 3 — normative placement

Lines 3223–3240 contain no `>`-prefixed line and sit inside `[R-WRT-06]`.
Normative, in force. PASS.

### 2.6 Check 4 — contradiction in the same passage, including untouched text

The very next sentence after the inserted paragraph (3242–3245, untouched):

> The output trailer MUST copy the input's unknown ignore-lane flag bits
> forward, **in place of the flags = 0 §6.3 requires of a file created
> under this text** (`[R-CNT-08]`).

and §6.3 itself (811–814):

> a writer creating a file under this text MUST write flags = 0 … A
> compactor, though its output is a new file, carries the input's unknown
> ignore-lane bits into its output trailer rather than writing flags = 0.

So §20.5 and §6.3 both treat a compactor as **a writer creating a file
under this text**, and §6.3 needed an express carve-out to release it from
one creation obligation. §9.2's creation paragraph is a creation obligation
with no such carve-out. The inserted paragraph asserts release from it by
an argument that never mentions it. That is a contradiction between the
repair and text one sentence away from it. Finding A-03.

Also examined and clean: `[R-WRT-09]` (3331–3338) is about verification
depth, not writing order; `[R-WRT-07]`'s placement freedom is consistent
with an unconstrained gap; the §20.5 Example (3298–3329) shows `│ dir │pad│
tr │` in the output, which *depicts* a pad but is inside a `>` block and so
non-normative — I checked, lines 3298–3329 all begin with `>`.

### 2.7 Check 5 — "fixed by nothing", tested to destruction

The exhaustive claim is "**The output's pre-trailer gap is fixed by
nothing.**" I searched for every site that could fix it, by the rule's
terms rather than by identifier: `grep -n "pre-trailer"` → 153, 566, 631,
661, 755, 756, 759, 837, 1176, 1981, 3229, 3446, 3618, 4089, 4108, 4334;
`grep -n "64-byte boundary"` → 756, 759, 1176; `grep -n "barrier"` → 783,
1174, 1183, 1193, 2927–2929, 3071, 3074, 3225, 3234, 3237, 4432.

Results:

- **1176** — `[R-LIF-02]` step 5 itself. Reached via §9.2's creation
  paragraph. Finding A-03.
- **837 — §6.4, `[R-CNT-09]`**: "Writers SHOULD keep dir_length plus **the
  pre-trailer pad** plus 64 within 65,536 bytes so that a 64 KiB suffix
  fetch captures trailer and directory together". A general clause about
  *writers*, naming the pre-trailer pad by name, and a compactor is a
  writer. This fixes the gap advisorily for every writer including a
  compactor, so "fixed by nothing" is false. Finding A-04.
- **153 — §2.3**: names the case as a writer obligation that binds the
  actor. Folded into A-03.
- **566 — §5.1, `[R-CNT-01]`** (normative): "a commit appends its own
  directory, pre-trailer pad, and trailer last, in that order (§6.2,
  `[R-LIF-02]` steps 3 and 5)", within a sentence describing "the
  structures the file's **commits** appended". Under the new rule a
  compaction output's structures were appended by no commit, so §5.1's
  anatomy sentence simply fails to describe it. Descriptive, not
  obligation-creating; noted in A-03's detail rather than raised alone.
- **631, 661, 1981, 3618** — slack content rules; they constrain content,
  not extent. Clean.
- **3446 — F5**: 128-byte minimum. Unaffected.
- **4108, 4089 — Appendix A**: a creator's file, non-normative.
- **4334 — Appendix G item 3**: "save where alignment forces a gap — a
  declared A or A_slab, or §6.2's 64-byte trailer alignment, the
  pre-trailer pad included". The profile pins gap extent for anyone
  adopting it, compactors included, and its closing paragraph lists "gap
  *extent*, which placement freedom (`[R-SLB-05]`) leaves open" among what
  the profile adds. Non-normative and consistent either way. Clean.
- **4432 — Appendix H**: see A-05.

"And no barrier ordering is owed within the output" — I found no other
site that owes a compactor a barrier, so as an exhaustive claim about
barriers it survives the search. Its *reason* does not; see §2.9.

### 2.8 Check 6 — what `[R-LIF-02]` fixed, item by item, and where each lands now

| Step | What it fixed | Where it lands if the compactor is unbound |
|---|---|---|
| 1 | begin writing at exactly F | n/a for a new output; the creation paragraph's substitute is "beginning at offset 16" |
| creation | front signature block first | §6.1 (866–..): "Bytes [0, 16) of **every file**" — file-level, so `[R-CNF-05]` carries it. Covered. |
| 2 | payloads/index regions/record extents in any §5.2-satisfying order | `[R-CNT-02]` (file-level) + §20.5's own placement freedom at 3263. Covered. |
| 3 | complete directory then its CRC | §7.1 `[R-CNT-11]` (file-level) + §20.4 re-emission. Covered. |
| 4 | barrier: content durable before the trailer | **withdrawn** — named consequence 2 |
| 5, pad | pad to the next 64-byte boundary | **withdrawn** — named consequence 1 |
| 5, generation | generation one greater | replaced expressly by "generation 1" at 3215–3217 |
| 5, cfl | committed_file_length = new end | §6.2 table ("= F; multiple of 64") + `[R-CNT-01]` + `[R-CNT-06]`. Covered. |
| 6 | trailer durable | **withdrawn** — named consequence 2 |
| Note at 1186 | the trailer must address the directory *this* write appended | §6.2's dir_offset/dir_length + §7.1's CRC make a stale-pointing trailer detectable, and §20.5's "output contains only the structures reachable from the input's live trailer" constrains content. Covered, thinly. |

So the two named consequences are the complete list of what is actually
released, provided the front-block, coverage, directory and
committed_file_length obligations are file-level — which I verified they
are. No third unnamed consequence. PASS on completeness.

### 2.9 Attacking the reason offered for consequence 2

The reason (3235–3239):

> A compaction leaves its input intact and writes bytes that are not
> readable as a TARN file until the trailer completing them is present, so
> there is no committed prefix for a barrier to protect and a torn output
> is an unreadable file rather than a damaged one.

Three attacks, in increasing strength.

1. "leaves its input intact" is asserted, not required. `[R-LIF-01]` lists
   "a whole-file rewrite under a new file_id" as a **conforming mutation
   of a file**, which contemplates replacing a file's contents in place
   with a new identity. Nothing in §20.5 requires the output to occupy
   different storage from the input; the only related text is the SHOULD
   at 3239 and §23.1's `[R-PRV-02]` at 3949–3951 ("the input persists,
   unmodified, until something outside this specification deletes it"),
   which is a description in a normative-but-descriptive sentence, not a
   prohibition on the compactor. So the premise is unenforced.
2. "there is no committed prefix for a barrier to protect" misidentifies
   what step 4's barrier does. Step 4 is "make **steps 1–3** durable … the
   platform equivalent needed to order writes against power loss" — it
   orders *this write's own new content* ahead of the trailer that
   publishes it. It is not protecting an older generation's prefix; that
   protection comes from append-only-ness, not from the barrier. The
   purpose applies verbatim to a fresh output file.
3. Therefore "a torn output is an unreadable file rather than a damaged
   one" is false in exactly the case the barrier exists for. With no
   ordering, a storage stack may make the final 64 bytes durable before
   the interior. The result opens: trailer magic and trailer CRC verify,
   committed_file_length matches the physical size (the file having been
   extended to full length), and the reader proceeds — and then meets a
   directory CRC failure (reject-file), or, worse, a valid directory with
   an un-durable tile payload, which fails at that tile's entry crc
   (reject-tile) while every other layer serves normally. That is a
   readable, **damaged** file, precisely what the sentence says cannot
   arise. §9.2's own Note at 1193–1196 concedes the shape: "Where barriers
   are weaker than assumed, safety degrades from 'torn commits are
   invisible' to 'torn commits are detected'."

Finding A-06. Not byte-level: barriers order durability and change no byte
of a successful output.

### 2.10 Check 7 — the analogy

The paragraph argues by contrast rather than analogy: "where §20.2 binds a
creator to that path **by name** and §20.3 step 6 binds an appender, this
section deliberately does not."

- §20.2's verb: "A creator **MUST follow** `[R-LIF-02]`'s creation path".
- §20.3 step 6's verb: "**Commit** (`[R-LIF-02]` steps 4–6): barrier; pad;
  trailer …" under "An appender **MUST**, in order".
- §20.5's verb for the compactor: silence.

Ranges: §20.2 ranges over creators, §20.3 over appenders, §20.5 over
compactors — three disjoint tiers per §20.1. The contrast is well-formed
*as a contrast*. What it cannot carry is the inference, because §20's own
preamble makes these sections consolidations of rules stated elsewhere:
"like §19, it consolidates — each step cites the rule whose outcome governs
it" (2897–2899). A consolidating section's silence is not a release from
the consolidated rule. Reported inside A-03.

### 2.11 Registers, checklists, appendices that assume the withdrawn rule binds a compactor

- **Appendix H, Conforming writer, 4426–4433** (non-normative): "…
  **follows the commit protocol including both barriers (§9.2)**; honors
  any alignment or slab it declares (§16)." An unqualified checklist item
  for the writer class. A compactor is a writer (§20.1's heading is
  "Writer tiers"; 2910–2912 "An appender and a compactor satisfy every
  writer requirement for the bytes they produce"). The updater entry at
  4436 imports writer obligations only "for the bytes it produces", which
  arguably filters barriers out but not step 5's pad, since the pad is
  bytes. Finding A-05.
- §21.2–§21.5 register rows: I read §21.1's reading rules and searched for
  compactor-related rows. `grep -n "compactor|compaction"` returns no §21
  row; §21.7's 3714–3720 names "§20.5's four obligations on a compacted
  file's trailer (`[R-WRT-06]`) — its fresh `file_id` draw, its
  generation, the unknown ignore-lane bits it MUST carry forward, and the
  floor its version_minor SHOULD take". The repair adds a fifth obligation
  to `[R-WRT-06]` (the durability SHOULD at 3239) but it is not a trailer
  obligation, so §21.7's count of four **trailer** obligations still
  holds. Checked and clean.
- §21.6 (3604–3656): no entry touches the commit protocol or a compactor's
  output length. Clean.
- Appendix G items 3, 4 and 8: item 4 ("**One generation**, so that the
  file is the output of a single commit") again equates a one-generation
  file with a commit's output, which the new rule denies for a compactor;
  non-normative, and item 8 already treats compactors as a special case,
  so I did not raise it separately. Noted here for the record.

---

## 3. Byte-level determinations

- **A-03** — byte-level YES. Compactor A follows §9.2's creation path and
  pads to the next 64-byte boundary, so its output's pre-trailer gap is
  under 64 bytes and F is the least 64-multiple ≥ (directory end + 64).
  Compactor B, reading §20.5, emits a 4,096-byte gap and an F that is 4 KiB
  larger for the same input. The long-gap output is itself a **conforming
  file** — §6.2 says so in terms ("a longer gap is conforming") — so
  `[R-CNF-05]` does not bar it under either reading; only one reading
  permits a conforming compactor to produce it. The set moves.
- **A-01** — byte-level NO. `[R-PRV-01]`'s operative MUST NOT governs how
  a commit is *represented* to a caller, not what is emitted. The
  enumeration is wrong and the slack claim is wrong, but no byte or
  verdict forks on repairing them.
- **A-02** — byte-level NO. §11.1's text is a Rationale; `[R-CNF-01]`
  gives it no force, and it defers to §20.3 in its own first clause.
- **A-04** — byte-level NO. `[R-CNT-09]` is a SHOULD, and `[R-CNF-12]`
  makes SHOULD deviation no violation; both readings let the bytes exist.
  The claim "fixed by nothing" is nonetheless false.
- **A-05** — byte-level NO. Appendix H disclaims its own authority at 4402
  ("each entry's authority is the requirement or section cited, never this
  summary").
- **A-06** — byte-level NO. Durability ordering changes no byte of a
  successful output.
- **A-07** — byte-level NO. The repair imports the carve-out's general
  clause, which reaches the packed-bool case; a competent implementation
  lands in the same place.

## 4. Per-check verdicts, summarised

| Check | Hunk 1 | Hunk 2 |
|---|---|---|
| 1 tense/quantifier | PASS | PASS |
| 2 citations | PASS (§14, `[R-SER-05]`, §21.7, "the bar above") | FAIL on `[R-LIF-02]` (A-03); PARTIAL on `[R-LIF-01]`; PASS on §20.2, §20.3 step 6, §6.2, §2.3-as-quoted |
| 3 normative placement | PASS | PASS |
| 4 contradiction in passage | PASS | FAIL (A-03: line 3243 one sentence later) |
| 5 exhaustive claims | FAIL ("and nothing else" — A-02 is a third site) | FAIL ("fixed by nothing" — A-04) |
| 6 what is left open | one vehicle (A-07) | PASS — the two named consequences are complete |
| 7 analogy / warrant | PASS with a verb gap closed by untouched text | warrant weak — §20's preamble makes it a consolidation (in A-03) |
| unswept restatements | A-01 (normative), A-02 | A-05 |
| reason attacked | n/a | A-06 |
