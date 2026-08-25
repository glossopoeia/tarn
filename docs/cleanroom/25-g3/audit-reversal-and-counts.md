# Round 25 repair audit — auditor B (hunks 01, 02, 03)

## 0. Disclosure

Read, in full or in the ranges named:

- `/private/tmp/.../r25audit-b/hunk-01.diff`, `hunk-02.diff`, `hunk-03.diff` (one `cat`, all three).
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, ranges:
  100–110 (R-CNF-01), 120–230 (§2.2/§2.3 conformance classes, R-CNF-02..R-CNF-11),
  300–340 (§3.1 terminology), 555–575 (§5.1), 580–670 (§5.1 example, §5.2 R-CNT-02/21/03),
  740–775 (§6.2 trailer table, R-CNT-05), 800–820 (R-CNT-08 flags),
  1140–1290 (§8 close, §9.1–§9.6: R-LIF-01..R-LIF-05), 1400–1520 (§10.2–§11.2, hunk 1 landing),
  1520–1560 (§11.3), 1700–1800 (§13.1–§13.3), 1940–1980 (§14.4 close, §14.5 R-SER-05),
  2894–3150 (§20.1–§20.3), 3149–3335 (§20.4, §20.5, hunk 2 landing),
  3595–3725 (§21.6, §21.7), 3909–4000 (§22.5, §23.1–§23.3, hunk 3 landing),
  4275–4300 and 4300–4467 (Appendix G items 2–10, Appendix H checklists).
- Greps (all against spec/tarn.md only), output reproduced in §5 below.

Ran no other file. Did not open docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md,
conformance/, spec/registry.json, git history, full.diff, or any other hunk file. Did not
list the audit directory. No web access.

**Unrequested context that appeared before I began:** the runtime placed a project
instruction file (CLAUDE.md pointing at AGENTS.md), a memory index listing the
maintainer's private notes by title, and a git status/recent-commit list into my context.
I did not open any of the files they name and did not use any of their contents as
evidence. Naming only: the commit-subject lines visible in that block mention round
numbers and ADR numbers. I formed no conclusion from them; every finding below is
sourced to a line of spec/tarn.md quoted in this transcript.

---

## 1. Hunk 1 — §11.1 shrink Rationale (lines 1475–1499), non-normative

### 1.1 The rule the repair asserts

For a layer that stored at least one tile in the generation a commit supersedes: a
shrink is barred wherever it alters what §14 fixes for such a tile (regardless of
whether the new state still stores it), and permitted wherever it does not — and the
permitted set has exactly two shapes: (a) tiles drop out of the addressed set, their
extents becoming slack; (b) a new padding position arises whose stored byte already
holds the fill.

### 1.2 Check 3 — does it sit in normative text / is the normative statement swept?

The block begins `> **Rationale.**` at line 1484 and every line of the hunk begins `>`.
[R-CNF-01] (line 104–106): "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*". So the repair has
no force. Per the charter that is fine provided the normative statement elsewhere now
says the same thing. It does — §20.3 step 4, lines 3046–3050:

> "What counts as such an alteration is the bar above and nothing
> else, its carve-out included — a new padding position whose stored
> byte already holds the fill `[R-SER-05]` fixes is not one, so a
> shrink producing only those is permitted here exactly as it is
> there"

and the carve-out proper at lines 3008–3013:

> "a change that leaves every one of those tiles' stored bytes meaning exactly
> what they meant — a filter whose mandated stride makes it
> the identity (`[R-COD-10]`), or a new padding position whose
> stored byte already holds the fill `[R-SER-05]` fixes — is not
> what this bars."

So the Rationale now matches the normative text on the point it was repaired for. The
`-` side ("permitted **where it only drops tiles out of the addressed set**") did *not*
match: it omitted the fill-holding-padding case entirely and so contradicted §20.3.
The repair's direction is right.

### 1.3 Check 1 — tense and quantifier

Rationale: "what a commit may do to a layer that already stored tiles **in the
generation a commit supersedes**"; "alters what §14 fixes for **such a tile** — whether
or not the new state still stores it".

§20.3 lines 3036–3046: "a shrink is permitted exactly where it alters nothing §14 fixes
for **any tile the layer stores in the generation this commit supersedes**" … "the
quantifier is the superseded generation's, so a shrink that alters what §14 fixes for a
tile stored there is barred **whether or not the new state still stores it**."

Tense: superseded generation, both sides. Quantifier: "any tile" / "such a tile" —
matches. PASS.

### 1.4 Check 5 — exhaustive claims

Flagged words: "the ordinary case … and … **the other**" (a closed two-member list);
"every grid count … unchanged" (untouched context); "freely".

Falsification attempt on the two-member list. §20.3's bar and its carve-out are
quantified over tiles the layer **stores in the superseded generation**. A tile that is
addressed but *unstored* in that generation is outside the bar entirely — it has no §14
obligation and no stored byte. Construct: layer, one dimension, E = 512, T = 256, so
G = 2, tiles 0 and 1; tile 0 stored, tile 1 the sentinel. Commit shrinks E to 500.
G = ⌈500/256⌉ = 2 — no tile leaves the addressed set. Positions 500–511 become padding,
and they lie in tile 1, which stores nothing. Nothing §14 fixes for tile 0 changes.
The shrink is permitted.

That permitted shrink is neither member of the Rationale's closed pair: no tile drops
out of the addressed set, and there is no "stored byte" that "already holds the fill"
because the affected tile is unstored. So the pair is not exhaustive of the permitted
set the same sentence opens by describing correctly ("permitted **wherever** it does
not"). FINDING A-07.

Note that the normative §20.3 does not make this mistake: it states the open rule and
offers the carve-out as an instance ("the bar above and nothing else, its carve-out
included"), never as an enumeration of permitted shrinks. The Rationale narrows what
the normative text leaves open — non-normative, so editorial, but it is the block an
implementer reads for the shape of the rule.

### 1.5 Check 4 — contradiction in the untouched remainder of the block

Remaining sentences of the block:
- "A layer that stored nothing may be re-declared freely." Against §20.3 lines
  3020–3024: "A layer that stores no tile **in the generation this commit supersedes**
  MAY be re-declared freely … the tense is the bar's, so a commit does not earn this
  permission by emptying the layer as it re-declares it." The Rationale's "stored
  nothing" is past tense and so reads on the superseded generation. PASS (it is
  looser — it does not repeat the anti-emptying gloss — but it does not contradict).
- "Growth that leaves every grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) unchanged touches the
  directory alone". Checked against §20.3 lines 3024–3033 ("an extent MAY **grow**,
  since a position that becomes real held that channel's fill and fill is a legal
  sample value"). Growth within a grid count removes padding positions from stored
  tiles, which is a change to "the set of padding positions (§11.3)" named in the bar's
  list — but §20.3 permits growth expressly and by name, and [R-SER-05] guarantees the
  byte held fill, so the stored bytes mean what they meant. No contradiction.
- "changes entry_count and with it extent_length (`[R-CNT-17]`)" — [R-CNT-17] is cited
  by §20.3 line 3056 for the same proposition ("`[R-CNT-17]` obliges the smaller
  entry_count and so a re-emitted index region"). Consistent.

No carve-out in the block collides with the repair's new breadth.

### 1.6 Check 6 — what the block leaves unconstrained

Structure governed: an extent change on a layer, and the four things that can move with
it — grid count Gᵢ, the padding-position set, entry_count/extent_length, and disk
ordinals. The block names all four (drop-out-of-addressed-set = Gᵢ; new padding
position = padding set; entry_count/extent_length; "disk ordinals renumber wherever
[R-GEO-06] moves them"). Nothing in this structure is named by the repair and left
unpinned. The one member it mishandles is the *unstored high-edge tile* case above,
which is A-07 rather than an unconstrained sibling.

### 1.7 Check 7 — analogy

The block contains no "exactly as / the same way / for the same reason" construction of
its own; "as §20.3 states normatively" is a pointer, not an analogy. Nothing to compare.
(§20.3's own "permitted here exactly as it is there" is not in this hunk.)

### 1.8 Check 2 — citations in the repaired lines

- §20.3 — opened. States the shrink rule normatively at step 4. PASS.
- §14 ("what §14 fixes for such a tile") — §14 is "Tile Serialization"; §20.3's bar
  names §14 the same way. PASS.
- §11.2 (grid count) — line 1508 defines Gᵢ = ⌈Eᵢ/Tᵢ⌉. PASS.
- [R-CNT-17], [R-GEO-06], [R-WRT-04] — untouched context; [R-CNT-17] verified above via
  §20.3 line 3056. PASS.
- [R-SER-05] is *not* cited in the repaired lines even though the repair states its
  content ("already holds the fill"); §20.3's parallel sentence does cite it. Not a
  defect (non-normative block), noted only.

---

## 2. Hunk 2 — §20.5, lines 3223–3231, normative ([R-WRT-06])

### 2.1 The rule the repair adopts

A compactor is bound by [R-LIF-02]'s creation path exactly as a creator is. Concretely
it must now: pad the gap between its output's directory-CRC and its output trailer to
the next 64-byte boundary and no further, and issue two storage barriers — one after
the directory and its CRC, one after the trailer. Before the repair, on the removed
text's own account, neither was owed and two conforming compactors could emit outputs
of different lengths from one input.

### 2.2 Check 3 — normative placement

Lines 3199–3252 are plain prose closing at line 3252 with `[R-WRT-06]`. Not a
blockquote. The repair is normative and self-sufficient: "A compactor MUST follow
`[R-LIF-02]`'s **creation path**". PASS.

### 2.3 Check 2 — every citation opened

**[R-LIF-02] (§9.2, lines 1168–1186).** Body: "A writer performing a commit MUST, in
order: (1) begin writing at exactly F (§9.4); (2) append new stored-tile payloads and
tile-index regions for the layers it changes, and any new record extents …; (3) append
the new complete directory … followed by its CRC; (4) make steps 1–3 durable (a storage
barrier such as fdatasync …); (5) append the pad to the next 64-byte boundary — zeroed
by advice, `[R-CNT-03]` — and the new trailer, with generation one greater than the
prior trailer's and committed_file_length equal to the new end; (6) make the trailer
durable."
Creation path, lines 1182–1186: "On creation there is no prior trailer: the writer
first emits the front signature block (§6.1) — whose durability the barriers of steps
4 and 6 cover — then performs steps 2–6, writing beginning at offset 16, with
generation 1."

Repair's claim: "the output has no prior trailer and stands at generation 1, **which is
the case that path states**." VERIFIED — the path states exactly that case.
Repair's other question (charter): does the path state anything else the compactor must
now also do? YES, three further things: emit the front signature block first; begin
writing at offset 16 (step 1's "at exactly F" is displaced); and step 5's other half —
committed_file_length equal to the new end. All three are independently forced by
file-conformance rules the compactor already owes ([R-CNT-01] line 566 "The file size
of a conforming file equals the live trailer's committed file length F"; [R-CNT-27]
line 570; §6.1's front block), so none of them conflicts. Noted, no finding.

**§20.2 ([R-WRT-02], lines 2921–2934).** "A creator MUST follow `[R-LIF-02]`'s creation
path: the front signature block; each layer's stored tiles, tile-index region, and any
record extents, in any order satisfying §5.2's coverage classes … then the complete
directory and its CRC; then the barrier, the pad, the generation-1 trailer with a fresh
nonzero file_id (§9.3), and the barrier that makes the trailer durable (`[R-LIF-02]`
steps 4–6 — **both barriers, not one**). Content obligations travel with the
structures: fill-encoded edge padding (`[R-SER-05]`), boolean byte values
(`[R-SER-08]`), and gaps zeroed as `[R-CNT-03]` advises."
Repair's claim: "as §20.2 obliges a creator" and "both, not one". VERIFIED as to the
creator's obligation and the "both barriers, not one" phrasing, which is lifted from
§20.2 verbatim. But §20.2 also carries content obligations that §20.5 elsewhere
expressly does not place on a compactor for carried-forward bytes — see §2.6 below
(A-04).

**[R-WRT-01] (§20.1, lines 2911–2919).** "A creator emits only conforming files
(`[R-CNF-05]`). An appender and a compactor **satisfy every writer requirement for the
bytes they produce** and the preservation obligations of §20.4 for what they carry
forward (`[R-CNF-06]`) …"
Repair's claim: "`[R-WRT-01]` **already has** a compactor satisfying every writer
requirement for the bytes it produces." The quoted half is accurate. What the sentence
*does with it* is not — see check 7 (A-01).

**[R-LIF-01] (§9.1, line 1157–1163).** "every conforming mutation of a file is either a
commit (§9.2) or a whole-file rewrite under a new file_id (compaction, §20)." The
repair's last sentence cites it for "a compaction is a whole-file rewrite rather than a
commit". VERIFIED as to what [R-LIF-01] says; see A-03 for what the sentence then
claims follows.

**[R-CNF-06] (§2.3, lines 186–188)** — reached via [R-WRT-01]: "An updater MUST satisfy
every writer requirement for the bytes it produces, and additionally MUST honor the
preservation obligations of §20.4". Same quantifier as [R-WRT-01]. PASS as a citation.

**[R-CNF-02] (§2.3, lines 144–156).** "A few obligations this specification places on
writers govern their *conduct* rather than their output … and a file is never
nonconforming by virtue of one: **conduct rules bind the actor, the predicate binds the
bytes.** A writer obligation whose violation this specification expressly declares not
to be a file-conformance violation binds the actor in the same way; §6.3's flags = 0
against a set ignore-lane bit and **§6.2's pre-trailer gap longer than `[R-LIF-02]`
step 5's pad** are the cases this text states". Not cited by the repair — it was cited
by the removed text ("one of the writer obligations §2.3 names as no file-conformance
violation"), and the removed citation was accurate. This is the rule that defeats A-01.

**§6.2 / [R-CNT-05] (lines 754–765)** — see A-02.

### 2.4 Check 1 — tense and quantifier

Which generation: the output's, generation 1. The repair says so and [R-WRT-06]'s
preceding sentence already fixed generation 1. Consistent.
Which set: "the bytes it produces" (from [R-WRT-01]) vs. "the writing of it" (the
repair's last sentence) vs. "the pad of step 5 and the barriers of steps 4 and 6". The
repair moves between a set of *bytes* and a set of *acts* without marking the move.
That is the substance of A-01. The compactor-as-actor quantifier itself ("A compactor
MUST") is unambiguous and singular. No tense defect in the MUST itself.

### 2.5 Check 4 — contradiction in the same passage, including untouched text

(a) Same paragraph, four sentences earlier, lines 3217–3223:
> "It MUST mint a fresh file_id for the output … and generation 1: **a compacted file
> is a whole-file rewrite under a new file_id by definition (`[R-LIF-01]`)**, and
> reusing the input's would break the (file_id, range) cache contract of `[R-LIF-03]`"

Repair's last sentence, lines 3229–3231:
> "That a compaction is a whole-file rewrite rather than a commit (`[R-LIF-01]`) fixes
> what the output *is*, not which rules govern the writing of it."

The earlier sentence uses precisely that classification, "by definition ([R-LIF-01])",
as the warrant for two rules governing the writing (mint a fresh file_id; write
generation 1). The later sentence denies that the classification does that work.
FINDING A-03.

Corroborating restatements outside the paragraph, both deriving a *writing* rule from
the same classification:
- §20.4 table, MU = 0 / PE = 0 row (line 3173): "A compactor MAY drop it **whenever it
  rewrites the file**."
- §20.4 line 3181: "A producer that wants a file without a layer writes one: a
  whole-file rewrite under a fresh file_id, which `[R-LIF-01]` already sanctions."
- §20.3 step 4, line 3019–3021: "Such a change is a new layer, or a whole-file rewrite
  under a fresh file_id (`[R-LIF-01]`, §20.5)."
So the distinction the last sentence draws is not one the document keeps.

(b) §6.2 [R-CNT-05], lines 754–765 — untouched, and it is the sentence the repair
should have swept:
> "Those bytes — the **pre-trailer pad** — are slack (§5.2): a writer that ends its
> directory on a 64-byte boundary leaves none, this specification does not constrain
> their content, and **bounds their number only through step 5 of the commit protocol**,
> which pads to the next 64-byte boundary (`[R-LIF-02]`) — a longer gap is conforming,
> and **no conforming commit produces one**."
FINDING A-02.

(c) Carve-out hunt in the rest of §20.5. Checked:
- "A compactor MUST preserve content, and **preserves no placement** … free to place
  structures anywhere §5.2 admits" ([R-WRT-07], line 3254). Does the creation path's
  ordering collide? No: step 2 is "in any order satisfying §5.2's coverage classes",
  and §6.2 already forbids a structure between directory end and trailer. No collision.
- "The output trailer MUST copy the input's unknown ignore-lane flag bits forward, in
  place of the flags = 0 §6.3 requires of a file created under this text (`[R-CNT-08]`)"
  (lines 3232–3236). This is the one place where the "compactor is a creator for
  writing purposes" reading would have bitten, and it is expressly carved out, in the
  very next sentence. No collision. Corroborated at §6.3 line 812: "A compactor, though
  its output is a new file, carries the input's unknown ignore-lane bits into its output
  trailer rather than writing flags = 0 (§20.5, `[R-WRT-06]`)."
- "a violation latent in a structure it carries forward verbatim travels into its output
  (`[R-WRT-01]`) — its verification depth is `[R-WRT-09]`'s and **reaches no decoded
  content**" (lines 3205–3208). This collides with the *wide* reading of "as §20.2
  obliges a creator" — see A-04.
- The removed text's "A compactor SHOULD make its output durable before anything
  discards the input; what discards it is outside this specification." Deleted. Is the
  loss covered? The durability half is subsumed and strengthened by the barriers of
  steps 4 and 6. The "input persists" half survives normatively at §23.1 [R-PRV-02],
  lines 3945–3949: "the input persists, unmodified, until something outside this
  specification deletes it". No gap. No finding.

### 2.6 Check 5 — exhaustive claims in the repaired text

- "**every** writer requirement for the bytes it produces" — quoted from [R-WRT-01],
  accurate as a quotation, misapplied (A-01).
- "**both**, not one" (barriers) — [R-LIF-02] has exactly two barriers, steps 4 and 6.
  Verified. PASS.
- "**already** has" — an implicit completeness claim (nothing new is being imposed).
  False: three obligations are new. Part of A-01.
- "**which is the case that path states**" — verified above, PASS.
- "The pad of step 5 and the barriers of steps 4 and 6 … are owed here" — presented as
  the list of what the MUST delivers, while the MUST itself ranges over the whole
  creation path. Whether the list is exhaustive of the new obligation is left open;
  see A-04.

### 2.7 Check 6 — what else in this structure is unconstrained

Structure governed: the compacted output's tail — everything from the end of the last
carried structure to the physical end of file — plus the write ordering that produces
it. Members, and what fixes each after the repair:

| member | fixed by |
|---|---|
| directory placement (no structure after it) | §6.2 [R-CNT-05], file-level |
| directory CRC | §6.2 / §8 |
| pre-trailer pad **length** | NEW: [R-LIF-02] step 5 via this repair (was: nothing) |
| pre-trailer pad **content** | [R-CNT-03], SHOULD only — unchanged, still advisory |
| trailer magic/version_major/dir_offset/dir_length | §6.2 table, file-level |
| trailer flags | [R-CNT-08], §20.5 paragraph 2 |
| trailer version_minor | [R-CNT-26] floor + §20.5's SHOULD |
| trailer generation | §20.5 ("generation 1") |
| trailer committed_file_length | §6.2 table + [R-CNT-01] |
| trailer file_id | §20.5 ("fresh file_id … a new draw") |
| trailer reserved 4 bytes | §6.2 table, "zero", structural |
| barrier after directory (step 4) | NEW: this repair |
| barrier after trailer (step 6) | NEW: this repair |
| physical file length vs committed_file_length | [R-CNT-01] |

The pad's *content* is the one member of this structure that a sibling rule leaves
advisory while the repair pins its *length*. That asymmetry is deliberate and
pre-existing — [R-CNT-03] is a SHOULD for every writer, [R-CNT-05] says "this
specification does not constrain their content" — and Appendix G item 3 is the place
that takes it as a requirement. So this is not a "one quantity pinned, its sibling
loose" defect: the sibling is loose on purpose, document-wide, for creators and
appenders too. No finding.

Also checked whether the repair adds a member to a closed count elsewhere. §21.7 lines
3708–3714: "§20.5's **four obligations on a compacted file's trailer** (`[R-WRT-06]`) —
its fresh `file_id` draw, its generation, the unknown ignore-lane bits it MUST carry
forward, and the floor its version_minor SHOULD take — are unwitnessed". The pad is not
a trailer field and the barriers are not trailer fields, so the count of four still
holds after the repair. PASS — checked, no finding. (The new pad obligation is likewise
unwitnessed as a compaction obligation, but §21.7's sentence is scoped to the trailer,
so it is not falsified.)

Appendix H, "Conforming writer" (line 4427): "follows the commit protocol including
both barriers (§9.2)". "Conforming updater" (line 4438): "everything a writer does **for
the bytes it produces**, plus: …". The updater row therefore does not inherit the
barrier line, barriers not being bytes — the same quantifier gap as A-01, in a
non-normative appendix. Appendix H's preamble disclaims authority ("each entry's
authority is the requirement or section cited, never this summary"), so this is a
downstream editorial consequence of A-01 rather than a separate defect; recorded here,
folded into A-01's repair note.

### 2.8 Check 7 — the analogy, verbs side by side

Two analogies in the repaired text.

**(i) Repair → [R-WRT-01].**
- Repair's governing verb and object: "A compactor **MUST follow** `[R-LIF-02]`'s
  creation path" / "The pad of step 5 and the barriers of steps 4 and 6 … **are owed**
  here".
- Cited rule's governing verb and object: "an appender and a compactor **satisfy every
  writer requirement for the bytes they produce**".
- Do they range over the same set? No. [R-WRT-01] ranges over *requirements on bytes*.
  The two obligations the analogy is used to deliver are (a) two storage barriers,
  which emit no bytes at all — "make steps 1–3 durable", "make the trailer durable" —
  and (b) the pre-trailer pad's length, which [R-CNF-02] names *by name* as one of
  exactly two obligations this specification "expressly declares not to be a
  file-conformance violation", adding "conduct rules bind the actor, the predicate
  binds the bytes". A requirement the document expressly classifies as binding the
  actor and not the bytes cannot be among the "writer requirements for the bytes it
  produces" that [R-WRT-01] says a compactor already satisfies.
- The analogy carries one obligation for **three** members (pad, barrier 4, barrier 6)
  and is unsound for all three. FINDING A-01.

**(ii) Repair → §20.2.**
- Repair: "A compactor **MUST follow** `[R-LIF-02]`'s creation path, **as §20.2 obliges
  a creator**".
- §20.2: "A creator **MUST follow** `[R-LIF-02]`'s creation path".
- Same verb, same object, same modality. The analogy is sound *for the creation path
  itself*. PASS. What it does not settle is whether §20.2's own additions travel with
  it (A-04).

### 2.9 Findings from hunk 2

- **A-01** — warrant unsound; "already has" false.
- **A-02** — §6.2 [R-CNT-05] unswept.
- **A-03** — last sentence contradicts the same paragraph's file_id/generation warrant.
- **A-04** — scope of the new MUST ambiguous between the bare creation path and §20.2's
  rendering of it.

### 2.10 Was the removed text right?

Partly. Its premise — that [R-LIF-02] is stated for a commit and that §20.5 did not bind
a compactor to it by name — was accurate on the text as it then stood, and its citation
of §2.3 ([R-CNF-02]) for the pre-trailer gap was accurate and is still accurate. What
the new text gets right is that the earlier paragraph's *conclusion* was a policy choice
dressed as an entailment, and a MUST stated by name is the honest way to make the
opposite choice. My findings are that the honest MUST arrived with a warrant that does
not hold (A-01), a self-contradicting closing sentence (A-03), an unswept sibling
statement (A-02), and an ambiguous scope (A-04) — not that the reversal itself is wrong.

---

## 3. Hunk 3 — §23.1, lines 3927–3943, normative ([R-PRV-01])

### 3.1 The rule the repair asserts

There are exactly three ways a commit removes sample data from reachability. Two of
them (supersede, de-addressing shrink) leave the bytes as slack. The third — a shrink
that turns a stored tile's real positions into padding without de-addressing the tile —
leaves the bytes inside a live stored tile as padding content, and discloses nothing,
because §20.3 step 4 permits it only where those bytes already hold the recorded fill.

### 3.2 Deriving the members before reading either side

Ways a *commit* can make sample data unreachable, worked from §20.3 step 4 and §3.1:

1. Supersede a stored tile — new payload appended, old payload becomes slack (§5.2
   line 631: slack is "everything an earlier commit superseded").
2. Unstore a stored tile — its index entry becomes the sentinel (§20.3 line 2986–2987:
   "entries for tiles that become unstored written as the sentinel"); the tile still
   reads, as fill ([R-TYP-08]); the old payload becomes slack.
3. Shrink so a grid count falls — tiles leave the addressed set; §20.3 line 3055:
   "the de-addressed tiles' extents become slack (`[R-CNT-21]`)".
4. Shrink without a grid count falling — real positions in the high-edge tiles become
   padding. Permitted for tiles stored in the superseded generation only under the
   carve-out (bytes already hold fill); unconditional for tiles that stored nothing.
5. (not sample data) Drop an MU = 0 / PE = 0 record — §20.4 table: "its extent becoming
   slack". Named separately by §23.1 and correctly excluded from the count.
6. (not available) Remove a layer — §20.4: "No commit therefore removes a layer record".
   §23.1 says so.
7. (not a commit) Recovery to an earlier commit boundary, truncation past F — §20.5's
   example names both; out of §23.1's "a commit" scope.
8. (marginal) Change a channel's fill on a layer with no padding position and no pad
   bit (§20.3 example (c)) — the *values* unstored tiles read change, but no sample
   bytes leave reachability. Not a member.

So the derived list is 1, 2, 3, 4 — **four**, unless 2 is a species of 1.

Is unstoring a species of superseding? Evidence both ways:
- FOR the broad reading: §5.2 line 631 defines slack as "everything an earlier commit
  superseded", which must include an unstored tile's payload; §20.5's closing Note,
  line 3330–3332: "**logical deletion** supersedes bytes but leaves them in the file as
  slack (`[R-CNT-21]`) — a privacy consideration (§23)". "Logical deletion" is
  unstoring, and the Note calls it superseding.
- AGAINST: §20.3 step 4 line 2985–2987 distinguishes them in one sentence — "entries
  for tiles this commit **stores or supersedes** written to their new state, entries for
  tiles that **become unstored** written as the sentinel"; §3.1 line 316: "Superseded
  payload bytes from earlier generations do not make a tile stored"; and §23.2, line
  3957–3959, treats unstoring as its own case and points at §23.1 for it: "a tile
  **unstored by a later commit** leaves its earlier payload in the file as slack
  (§23.1)".

So the count of three is defensible only under the broad reading, and §23.2 — the very
section that cites §23.1 for this case — uses the narrow vocabulary. FINDING A-06.
The count was two before the repair and had the same gap; the repair reopened a closed
count without resolving it.

### 3.3 Check 1 — tense and quantifier on the new member

New member: "a shrink that turns **a stored tile's** real positions into padding
**without de-addressing it**".
Consequence: "The third leaves them inside **a live stored tile**, as its padding
content".
§3.1 line 315: "unqualified *stored* means stored in the live generation."
§20.3's bar quantifier, line 2997–2999: "for any tile that layer stores **in the
generation this commit supersedes**".

The two readings of "a stored tile" pick out different sets, and the sentence needs
both: the *permission* is quantified over the superseded generation (that is the only
generation in which the bar's carve-out can be evaluated), while the *consequence* is
quantified over the live generation (the bytes have to still be in a stored tile to be
"inside a live stored tile"). "Without de-addressing it" is the wrong hinge between
them: de-addressing is not the only way a tile stops being live-stored. A commit may
unstore the tile — §20.3 lines 3043–3046 contemplate exactly this and say only that it
does not *rescue* a barred shrink: "Unstoring that tile in the same commit does not
rescue it either … barred whether or not the new state still stores it."

Worked case. E = 1024, T = 1024, one tile, stored in the superseded generation, its
decoded positions 1000–1023 already holding the channel's recorded fill. One commit
(i) shrinks E to 1000 and (ii) writes the sentinel for that tile. The shrink is
permitted: the only §14 effect on the prior-generation stored tile is new padding
positions whose bytes already hold the fill, which the carve-out excludes. Unstoring is
independently permitted. The tile is **not** de-addressed — G = ⌈1000/1024⌉ = 1, same as
before — so it satisfies §23.1's third member as written. But its bytes are now slack,
not "inside a live stored tile". The consequence sentence is false of this instance.
FINDING A-05.

The same defect fires, more mildly, when the commit supersedes rather than unstores the
tile: the prior payload's copy of those bytes goes to slack while the new payload's
copy is live padding.

The privacy conclusion survives in both variants — the bytes hold fill either way — so
this is a precision defect, not a hole in the property. But it is the exact
tense/quantifier shape the charter names, and the fix is one clause.

### 3.4 Check 2 — citations

- **§9.1** ("the append-only model") — lines 1157–1163, committed-prefix immutability.
  PASS.
- **§20.3 step 4** — the parenthetical now sits at the end of the third member. §20.3
  step 4 runs lines 2979–3070 and contains the supersede/unstore clause, the bar, the
  carve-out and the whole shrink paragraph, so it supports all three members. PASS.
- **"§20.3 step 4 permits that shrink only where those bytes already hold the channel's
  recorded fill"** — the load-bearing citation. §20.3 lines 3046–3050: "What counts as
  such an alteration is the bar above and nothing else, its carve-out included — a new
  padding position whose stored byte already holds the fill `[R-SER-05]` fixes is not
  one". And the bar itself, line 2999–3003, names "the set of padding positions (§11.3)
  and the content `[R-SER-05]` fixes there" as things a commit MUST NOT alter for such
  a tile. So a new padding position in a prior-generation stored tile is an alteration
  of the padding set, barred unless the byte already holds fill. **"Only where" is
  correct.** I tried three escapes and all close:
  (a) re-writing the tile in the same commit — closed by lines 3004–3007 ("a commit does
      not escape this by unstoring in the same breath: superseding every tile of a layer
      and re-declaring it are one operation, and this bars it");
  (b) unstoring it in the same commit — closed by lines 3043–3046;
  (c) changing the fill in the same commit so the bytes "hold the fill" — a fill change
      alters "the content `[R-SER-05]` fixes there" for the tile's *existing* padding
      positions and is barred; §20.3 example (c) line 3130–3132 says so directly ("A
      fill change on a layer that **stores** a tile carrying either is not an appender's
      operation at all").
  PASS.
- **"which the layer record publishes"** — §7.4 record layout, line 1019: "C channel
  entries | name (u8 len + bytes) · type u16 · **fill** (u8 len + bytes)". §13.1 line
  1703–1710: "Every channel entry records a fill value … a reader MUST take a channel's
  fill from its channel entry". The fill is in the layer record, which is in the
  directory, which every reader parses. PASS.
- **[R-CNT-21]** (slack) — §5.2 lines 628–657. PASS.
- **§9.6** ("scans backward for an earlier trailer") — §9.6 is "Recovery scan (not a
  reader behavior)", line 1289 ff. PASS.
- **§20.4** (dropped ancillary record's extent) — table row MU = 0 / PE = 0: "Retain
  byte-identical, or drop it — **its extent becoming slack**". PASS.
- **§20.5** (only operation that removes slack) — untouched, [R-PRV-02]. PASS.

### 3.5 Check 3 — normative placement

§23.1's first paragraph is plain prose ending `[R-PRV-01]` at line 3943. Normative.
PASS. The MUST NOT it carries — "Writers and the tools built on them MUST NOT represent
any commit that makes sample data unreachable as erasure of it" — is quantified over
"**any** commit that makes sample data unreachable", not over the enumeration, so
neither A-05 nor A-06 lets an actor out of the MUST. This is what keeps both findings
below the byte-level line.

### 3.6 Check 4 — contradiction in the passage

- Second paragraph, [R-PRV-02]: "Compaction (§20.5) is the only operation that removes
  slack". The third way does not create slack, so no collision.
- Final clause of the repaired paragraph: "a shrink reported as erasure misleads exactly
  as a supersede so reported does." Under the new third member there is now a shrink
  whose bytes disclose nothing — so for that member the MUST NOT bars a
  representation whose harm the repair has just argued away. Not a contradiction (the
  MUST NOT's quantifier is unchanged and independent of the enumeration), but it is the
  answer to the charter's "does the new sentence weaken or strengthen the property":
  it weakens the *motivation* of §23.1 at the margin by admitting a member with no
  privacy content, while leaving the obligation's scope untouched. No finding.
- §23.2, lines 3955–3961 — the neighbouring subsection, which cites §23.1 for a case
  §23.1's count does not name. That is A-06's corroboration, not a separate defect.
- §20.5's closing Note line 3330: "logical deletion supersedes bytes but leaves them in
  the file as slack" — after the repair there is one logical deletion (the third way)
  that leaves them **not** as slack. The Note is non-normative and its subject is
  supersede/unstore, so I do not raise it as a finding; recorded here as the nearest
  restatement I checked and cleared.

### 3.7 Check 5 — exhaustive claims

- "**three ways**" — a closed count in normative prose. Falsified above (A-06) on the
  narrow reading of "superseding", which is the reading §20.3 step 4 and §23.2 use.
- "**The first two** leave the bytes in the file as slack" — verified for supersede
  (§5.2) and for de-addressing shrink (§20.3 line 3055). PASS.
- "**The third** leaves them inside a live stored tile" — falsified by the
  unstore-in-the-same-commit case (A-05).
- "**discloses nothing** a reader could not already derive" — verified: the padding
  content is the recorded fill ([R-SER-05], §14.5 lines 1955–1965), and the fill is
  published in the layer record. The claim is conditional on the carve-out, and the
  carve-out holds unconditionally for the case as scoped (see 3.4). PASS.
- "**no commit removes a layer at all**" — §20.4 line 3176: "No commit therefore removes
  a layer record". PASS.
- "**only** compaction … removes slack" — untouched, [R-PRV-02]. PASS.

### 3.8 Check 6 — what the repair leaves unconstrained

Structure governed: the enumeration itself — the set of commit effects that move sample
bytes out of reachability, and the disposal each effect gives those bytes. Members and
their disposal after the repair:

| effect | named? | disposal stated? |
|---|---|---|
| supersede a stored tile | yes | slack |
| unstore a stored tile (sentinel) | **no** (unless "supersede" is read broadly) | — (§23.2 supplies "slack") |
| shrink, grid count falls | yes | slack |
| shrink, padding created in a prior-gen stored tile that stays stored | yes | live padding |
| shrink, padding created in a prior-gen stored tile the same commit unstores/supersedes | **no** | wrongly gets "live padding" |
| shrink, padding created only in tiles the superseded generation did not store | no | no bytes move; correctly out of scope |
| drop an MU = 0/PE = 0 record extent | yes, separately | slack |

Two rows unnamed, both real: A-06 and A-05. No third quantity of this structure is left
dangling.

### 3.9 Check 7 — analogy

The repaired text contains one analogy: "a shrink reported as erasure misleads **exactly
as** a supersede so reported does." Verbs side by side — repair: "misleads"; the thing
compared: "a supersede **so reported**", i.e. also "misleads". Both range over the same
set (representations made by a writer or its tooling about a commit), and both are
governed by the same MUST NOT in the preceding sentence, whose quantifier is "any
commit that makes sample data unreachable". Same verb, same set. PASS.
The sentence is untouched by this hunk in any case, and the newly added third member
inherits the same MUST NOT quantifier, so the analogy still carries for it.

---

## 4. Byte-level determinations

- **A-01** — the MUST stands on its own words whichever way the warrant goes; fixing the
  warrant moves nothing. NOT byte-level.
- **A-02** — the disputed file is a generation-1 file with, say, a 4096-byte gap between
  its directory CRC and its trailer. §6.2 says in terms "a longer gap is conforming", so
  the file is conforming and no register row fires. A compactor written against §6.2's
  "bounds their number only through step 5 of the **commit** protocol" plus §9.1's "a
  compaction is not a commit" emits it; a compactor written against §20.5's new MUST
  emits at most 63 bytes there. Different bytes on disk, both files conforming, only one
  actor conforming under each reading. BYTE-LEVEL.
- **A-03** — a statement about what a classification does; no emission or verdict turns
  on it. NOT byte-level.
- **A-04** — the wide reading would forbid a compactor from carrying forward a tile whose
  padding does not hold fill. But such a tile fires T4 (§21.4: "A padding position does
  not encode, for each channel it carries, that channel's recorded fill value"), so the
  file is nonconforming and [R-CNF-05] bars every conforming writer from emitting it
  under both readings. The emittable set does not move. NOT byte-level.
- **A-05** — the enumeration and its consequences are descriptive; the MUST NOT is
  quantified independently of them. NOT byte-level.
- **A-06** — same. NOT byte-level.
- **A-07** — non-normative block; [R-CNF-01] gives it no force, and the normative §20.3
  states the open rule correctly. NOT byte-level.

---

## 5. Greps run, verbatim

```
$ wc -l spec/tarn.md
    4467 spec/tarn.md

$ grep -n -i "supersed" spec/tarn.md
61, 315, 602, 632, 657, 1200, 1486, 2907, 2986, 2998, 3005, 3021, 3038, 3044,
3086, 3092, 3113, 3114, 3173, 3331, 3609, 3703, 3929, 3942
  (each line inspected; 315, 632, 2986, 3005, 3044, 3331, 3929 quoted above)

$ grep -n -i "unstor" spec/tarn.md
1712, 1744, 1750, 1757, 1777, 2109, 2987, 3005, 3043, 3959, 4148
  (2987, 3043, 3959 are the load-bearing ones; all quoted above)

$ grep -n "R-SER-05\|pad bit\|padding position" spec/tarn.md
202, 1491, 1530, 1714, 1777, 1897, 1898, 1904, 1906, 1908, 1914, 1915, 1957,
1961, 1965, 1970, 2400, 2856, 2933, 3000, 3001, 3011, 3012, 3048, 3049, 3129,
3535, 3537, 3538, 3559, 3661, 3674, 3684, 4380, 4417, 4424, 4456

$ grep -n "pre-trailer\|pad to the next\|64-byte boundary" spec/tarn.md
153, 566, 631, 661, 755, 756, 759, 837, 1176, 1983, 3437, 3609, 4085, 4104, 4330
  (153 = R-CNF-02's conduct-rule list; 755-759 = R-CNT-05, the unswept sentence)

$ grep -n "creation path\|both barriers\|barrier" spec/tarn.md
783, 1174, 1183, 1193, 2923, 2929, 2930, 2931, 3073, 3076, 3224, 3228, 4428
  ("creation path" occurs at 2923 (§20.2) and 3224 (the repair) only —
   [R-LIF-02] itself never uses the phrase; the paragraph at 1182-1186 is what
   both sections mean by it.)

$ grep -n "R-LIF-0[1-6]" spec/tarn.md
154, 567, 759, 1163, 1180, 1215, 1234, 1239, 1253, 1258, 1270, 1275, 1277, 1313,
2081, 2712, 2897, 2923, 2931, 2951, 2955, 2966, 2979, 2985, 3017, 3020, 3072,
3073, 3181, 3221, 3222, 3224, 3230, 3315, 3316, 3449, 3614, 3669, 3670, 3705,
3882, 3972, 4323

$ grep -n "compactor\|compaction" spec/tarn.md   (first 80 hits listed; all of
  §20.5's inspected, plus 61, 63, 366, 611, 656, 812, 938, 1163, 1368, 2909,
  2913, 2995, 3093, 3173, 3178, 3182, 3609, 3711, 4205, 4288, 4353-4361, 4390)

$ grep -n "de-address\|reachability\|erasure" spec/tarn.md
3055, 3925, 3928, 3929, 3931, 3941, 3949
  (confirms §23.1 is the only place the enumeration is stated; no register row
   or appendix restates it, so nothing downstream needed sweeping for hunk 3
   beyond §23.2's cross-reference, which is A-06's corroboration)

$ grep -n "channel entr" spec/tarn.md
1019, 1046, 1093, 1591, 1686, 1703, 3480, 3483, 3484, 3485, 3499, 3506, 3510, 3783
  (1019 confirms fill lives in the layer record's channel entries)
```

Hard-wrap discipline: every search above used a fragment short enough not to wrap
("supersed", "unstor", "pre-trailer", "creation path", "de-address", "channel entr").
Where I needed a phrase that could wrap — "bounds their number only through step 5",
"already has a compactor", "which is the case that path states" — I read the surrounding
range with `sed -n` rather than grepping for it, so no conclusion here rests on a grep
that could not have matched.

## 6. Checks that passed with nothing to report

Recorded explicitly so the clean results are auditable:

- Hunk 1: checks 1, 2, 3, 4, 6, 7 pass. Only check 5 fires (A-07).
- Hunk 2: check 3 passes (normative). Check 1's tense passes. Check 6 passes — the
  structure's members are all fixed, the pad-content sibling is loose by document-wide
  design, and §21.7's closed count of four trailer obligations is not falsified.
  Check 7's second analogy (repair → §20.2, "MUST follow" against "MUST follow") passes.
  Checks 2, 4, 5, 7(i) fire (A-01..A-04).
- Hunk 3: checks 2, 3, 7 pass in full — every citation opened and verified, including
  the load-bearing "only where those bytes already hold the fill", which survived three
  attempted escapes. Check 4 passes. Checks 1, 5, 6 fire (A-05, A-06).
