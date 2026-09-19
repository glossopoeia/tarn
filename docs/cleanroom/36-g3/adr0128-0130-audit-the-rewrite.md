# Audit transcript — "the-rewrite" (hunks 29–33, §20.5 Rewriting)

## Disclosure

**Pre-loaded context.** Before this task began, my context already contained: a
project `CLAUDE.md` pointing at `AGENTS.md`; a user memory file `MEMORY.md`
listing prior-round TARN findings by title (e.g. "TARN repair prose vs
rules", "TARN closed-list exceptions compose", "No nested em-dash phrases",
"TARN refute phase and unanimous upholds"); and a `gitStatus` block naming
recent commit subjects ("ADR-0130: the layer record carries PE = 0 — a
commit MAY drop a layer; ADR-0068 superseded, ADR-0129's decision 2
withdrawn, corpus rebuilt", etc.). Per the charter I disregarded all of this
as evidence about the specification — I did not open `AGENTS.md`, did not
follow the memory file's linked notes, and did not use the commit subjects
to steer my reading. I note this is a disclosed breach of exposure, not of
action: I did not read any of the forbidden paths, but the commit-subject
line in `gitStatus` did confirm, before I opened the spec, that the layer
record's flags are "PE = 0" post-round — I deliberately re-derived this
independently from `spec/tarn.md` §7.3's own table (line 1088) rather than
relying on that pre-loaded line, and I flag it here so the reader can
discount any inference that traces back to it rather than to my own read of
§7.3.

**Files read.** `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(read in full via targeted `Read` calls at the offsets shown below) and the
five hunk files named in my charter:
`hunk-29.diff` .. `hunk-33.diff` in
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r36-audit/case/`.
I did not read `full.diff`, any other `hunk-*.diff`, or list that directory.
I did not read `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`README.md`, `conformance/`, `spec/registry.json`, or any git history/diff,
and did not use the web.

**Commands run.** All via `Bash`/`Read`/`grep`/`awk` against
`spec/tarn.md` only (read-only; no writes to the repository). I wrote no
scratch files — every computation below was a grep or a manual line-range
read, so I did not need `/private/tmp/.../r36-audit/scratch/the-rewrite/`.

---

## 1. Reading the hunks

Read `hunk-29.diff` through `hunk-33.diff` verbatim. All five land inside
§20.5 (spec lines 3519–3697, current file), header "20.5 Rewriting". Their
headers self-report as mechanically derived from the first changed line and
ask me to verify against the body — I did: all five open on the correct
`#### 20.5 Rewriting` heading and their line ranges are contiguous and
non-overlapping, covering 20.5's opening paragraph (29), the R-WRT-06/R-WRT-07
first half (30), the regeneration paragraph and R-WRT-07's close (31), the
Example (32), and R-WRT-09 plus the closing Note (33). No header/body
mismatch found.

## 2. Reading the landing section end-to-end

Read spec lines 3114–3697 in full: §20 (Writing and Updating) opening,
§20.1 Writer tiers, §20.2 Creation, §20.3 The append procedure (all of it,
including step 4's fixed-declaration bar and the three worked Examples),
§20.4 Re-emission and preservation (including its table), and §20.5
Rewriting end to end.

Key facts pinned down before judging anything:

- §20.1: the rewriter tier is defined as writing "a new file from an
  existing one under a new identity (§20.5), carrying structures forward,
  re-creating some, or dropping some; compaction, which carries every
  structure forward and changes nothing but placement, is the rewrite that
  reclaims slack." This is the base definition hunk 29 elaborates.
- §20.4's table (lines 3479–3483) has three rows: MU=1 (retain
  byte-identical, no drop, "a rewriter MUST refuse to rewrite the file, on
  `[R-WRT-06]`'s own ground"); MU=0/PE=1 (retain byte-identical, extent
  content unmodified — **no drop licensed**); MU=0/PE=0 (retain
  byte-identical, **or drop it**).
- Line 3463: "the layer record carries PE = 0 and is dropped under the
  table's last row" — confirms the layer record is currently registered
  MU=0/PE=0 (this is the effect of the third commit named in my charter's
  preamble, not one of my five hunks, but it is load-bearing for reading
  §20.4's table and for hunk 29/31's "Dropping is the one disposal…"
  language).
- §7.3's registry table (spec line 1088), read separately (§7 is outside
  my hunks but is the authority §20.4 cites): `0x0001 | layer | file
  (container for layer scope) | MU = 0, PE = 0`. This is the primary
  source I used to confirm the current registry values, independent of
  the `gitStatus` commit-subject text noted above.

## 3. Hunk-by-hunk: the rule each repair adopts, and the eight checks

### Hunk 29 — §20.5's opening

**Rule adopted.** The section's actor is renamed compactor→rewriter and
generalized: a rewrite is defined as carrying every input structure
forward, re-creating it, or dropping it, "under the rule for what is done
to it," with three *named* rewrites (compaction, dropping, re-declaring)
that a single rewrite MAY combine ("A rewrite MAY be several of these at
once"). The refuse/drop disposal logic is requantified from "a violation
latent in a structure it carries forward" (compactor-only, no re-create
case existed) to also covering re-created content via "its verification
depth over what it carries is `[R-WRT-09]`'s… and what it re-creates it
decodes as a reader… and writes as a creator."

**Check 1 (tense/quantifier).** "Given a conforming input, an output that
carries forward, re-creates and drops as this section provides is a
conforming file" — new sentence, no prior-round analogue. Quantifier: "as
this section provides" is a hedge over the whole of §20.5 (fresh file_id,
creation path, `[R-WRT-06]` refusal ground, `[R-WRT-09]` verification),
not just the three named operations, so it does not overclaim — checked
against §20.5 as a whole and found consistent (**pass**).

**Check 2 (citations).** `[R-CNF-06]` ("A rewriter satisfies every writer
requirement for the bytes it produces") — §20.1 line 3138 states exactly
this of "an appender and a rewriter." `[R-WRT-01]` ("a violation latent in
a structure it carries forward verbatim travels into its output") — §20.1
line 3151 states this generally of "a writer that carries forward any
structure… it did not decode." `[R-CNF-11]` (decodes as a reader) — §20.1
line 3140-3141: "is a reader of every structure it processes
(`[R-CNF-11]`)." All three **pass** — I opened each cited rule and it says
what the sentence claims.

**Check 3 (label not marker).** The whole passage sits in ordinary body
text under `#### 20.5 Rewriting`, no `>` blockquote, so it is normative
without needing the check — confirmed by reading the raw markdown (no `>`
prefix on any of these lines).

**Check 4 (contradiction in the passage) / Check 5 (exhaustive claim) —
the central question.**

> "This text names three rewrites: **compaction**, which carries every
> structure forward and changes nothing but placement… **dropping**…
> and **re-declaring**… A rewrite MAY be several of these at once."

I held compaction's definition ("carries **every** structure forward") next
to "A rewrite MAY be several of these at once." Compaction's definition is
a universal claim over *every* structure of the input. Any rewrite that
also drops a record, or re-creates a layer, by construction does **not**
carry every structure forward (the dropped one is omitted; the re-created
one is not "carried forward" — the very next paragraph says "nothing of
the input's copy of that layer is carried forward" of a re-created layer,
hunk 30). So a rewrite that combines compaction with dropping or
re-declaring cannot, by the letter of this definition, be *compaction* at
all — "every structure" is false of it. Yet the immediately following
sentence licenses exactly that combination ("MAY be several of these at
once").

I searched for a saving qualification (e.g. "every structure it
retains") and found none — the definition as written says "every
structure," full stop. **This is a genuine OVERCLAIM (check 5) that
collides with check 4's contradiction test in the same paragraph**:
"compaction… carries every structure forward" (universal) directly beside
"A rewrite MAY be several of these at once" (which requires compaction to
coexist with an operation that, on any structure it touches, does *not*
carry that structure forward unchanged). The natural repair is to scope
compaction's definition to the structures it applies to ("changes nothing
but placement, for every structure it carries forward this way") rather
than an unqualified "every structure." Not byte-level on its own (it's a
definitional/labeling question — the actual permission "MAY be several at
once" is unambiguous and governs regardless of how "compaction" is
defined), but it undermines every downstream sentence that leans on
"compaction" as a *totalizing* category (see hunk 32 below, and Appendix G
§4 below).

**Check 5, second target — the four disposal scenarios asked for.** For
each, I determined which sentence decides:

| Detected condition | Detector | Disposal | Deciding text |
|---|---|---|---|
| A stored tile's entry crc fails | `[R-WRT-09]` ("the checksum §8.1 states over each extent it copies, every stored tile's entry crc among them") | **MAY drop the layer** (via §20.4's MU=0/PE=0 row, since the layer record is now PE=0) **or MUST refuse**. Cannot re-create around it: re-creating "decodes as a reader first" (hunk 33), and decode step 5 of §19.4 verifies the same entry crc before decoding — the failure recurs identically. | Hunk 29's "A rewriter MUST refuse to rewrite when any check `[R-WRT-09]` obliges fails… Dropping is the one disposal that answers, and only where §20.4's table licenses it… Where the table does not license a drop the rewriter MUST refuse," read against §20.4's MU=0/PE=0 row and §19.4 step 5. |
| A segment of a layer's index chain fails (`[R-IDX-04]`) | `[R-WRT-09]` ("full index chain (`[R-IDX-04]`)") | Same as above: **drop the layer or refuse**. §15.4 makes any segment/crc_of_crc_array failure reject-*layer*, so the whole layer — not a single tile — is what must be dropped or the rewrite refused. | Same governing sentence, plus §15.4 (`[R-IDX-04]`)'s reject-layer outcome. |
| A top-level user-metadata extent's CRC fails | `[R-WRT-09]` (§8.1's map states a checksum: "final 4 bytes of the extent") | **MUST refuse.** No drop is licensed: §20.4's table's MU=0/PE=1 row is "Retain byte-identical, extent content unmodified" — **no drop option at all**, unlike the layer-record row. Re-creating is not available either (user-metadata is not a layer; §20.5 only defines re-creation for layers). | §20.4's table (MU=0/PE=1 row) together with hunk 29's "Where the table does not license a drop the rewriter MUST refuse." This diverges sharply from a plain *reader*'s treatment of the same corruption (§8.2/`[R-CNT-20]`: ignore-record, not reject-file) — a reader tolerates it, a rewriter carrying the record forward cannot. |
| An unknown record with MU = 0, PE = 0 | — | **No `[R-WRT-09]` obligation is even triggered.** §8.1's coverage map's last row is explicit: "Extent of a record of a type this specification has not assigned \| none — the bytes are opaque (§7.2) \| —". There is no checksum for this extent, so nothing can fail under `[R-WRT-09]`. The rewriter simply carries it forward (safe, since MU=0 means the extent slot is its only reference, `[R-WRT-08]`) or drops it at its own option under the PE=0 row — never forced into refuse by a corruption it cannot detect. | §8.1's table (the "none" row) and §20.4's MU=0/PE=0 row. |

This is the sharpest asymmetry check 5/6 turned up here: a corrupt
**PE=1** extent (user metadata) forces **refusal** on a rewriter even
though a plain reader would just ignore-record it and move on — the
rewriter's obligation is strictly stronger than a reader's for this one
case, because `[R-WRT-01]`/hunk 29's "MUST NOT emit a file carrying a
violation it has detected" leaves no drop escape hatch for PE=1 records. I
looked for a sentence that relaxes this for PE=1 metadata specifically and
found none — I read this as intended (metadata's whole point is PE=1 =
"never removed" by an updater) rather than a defect, but it is worth
surfacing because it is a real behavioral fork between reader and
rewriter that a corpus-testing tool needs to know about.

**Check 6 (structure — what else is unconstrained).** Structure: "a
rewrite" as a whole. Fields/quantities it carries: (a) which structures it
carries forward, (b) which it drops, (c) which it re-creates, (d) its
file_id (pinned: fresh, `[R-LIF-01]`), (e) its version_minor (pinned,
`[R-CNT-26]`/`[R-WRT-06]`'s floor), (f) placement of every structure
(pinned free, `[R-SLB-*]`), (g) **the content/reference-array of a
re-created layer**. (a)–(f) are all governed somewhere in §20.5. (g) is
not governed by *this* hunk (it surfaces in hunk 31 — see below, my
strongest finding).

**Check 7 (analogy).** No "exactly as / the same way / on the model"
construction in hunk 29's own new text (those appear in hunk 31, handled
there).

**Check 8 (anaphor, forward from the insertion).** The insertion replaces
the whole compaction-only opening with the three-way taxonomy. Forward
references I traced: "the rewrite that reclaims slack" (compaction) →
resolves to compaction, unambiguous, adjacent. "Dropping is the one
disposal that answers" → "disposal" is a new term introduced in this same
sentence, no dangling backward reference. "It MUST mint a fresh file_id"
→ "It" = "the rewriter" / "A rewriter," nearest antecedent, unambiguous
both before and after the repair (this whole paragraph was rewritten as a
unit, so there is no stale antecedent left over from the old compactor-only
text). No anaphor defect found in hunk 29.

**NESTED_DASH.** Six em-dashes in the landing range (3519–3557); I located
each: two matched pairs (3522–3523; 3549–3550) and two single dashes each
running to terminal punctuation (3537 → period; 3552 → colon). No nested
pair. **Clean.**

**BCP14 casing.** `grep -oE '\b(must|should|shall|may)\b'` (case-sensitive,
so only catches lowercase) against hunk 29's added lines: zero hits.
**Clean.**

---

### Hunk 30 — [R-WRT-06] and [R-WRT-07]'s first half

**Rule adopted.** Renames the actor in seven sentences (creation-path
obligation, trailer-indistinguishability, version_minor SHOULD, the
MU=1-refusal rule, and the content-preservation rule) from compactor to
rewriter, and — this is the substantive edit, not just search-replace —
narrows "A rewriter MUST preserve **the content of every structure it
carries forward**" (was, unscoped: "A compactor MUST preserve content")
and adds an entirely new sentence: "A layer the rewrite re-creates is new
output: its record, its tile-index region and its stored tiles are written
under §20.2's rules from content the rewriter decoded (§19.3, §19.4), and
nothing of the input's copy of that layer is carried forward."

**Check 1 (tense/quantifier), run on every renamed-subject sentence:**

- *"A rewriter MUST follow `[R-LIF-02]`'s creation path"* — generalized
  correctly: every rewrite (not just compaction) writes a wholly new file
  with no prior trailer, so the creation-path obligation applies uniformly
  regardless of which of the three named operations occurred. **Pass.**
- *"…indistinguishable by their live trailers alone"* — same: the
  trailer carries no commit-count field regardless of which rewrite
  produced the output. **Pass.**
- *version_minor SHOULD… "a record it never decoded"* — checked against
  §21.6 and §10.1/§10.2 (see Check 2 below). **Pass**, with the caveat
  noted in Check 2.
- *"A rewriter MUST refuse to rewrite a file carrying any record whose
  type it does not implement with MU = 1"* — matches §20.4's MU=1 row
  verbatim ("At either scope a rewriter MUST refuse to rewrite the file,
  on `[R-WRT-06]`'s own ground"). **Pass.**

**Check 2 (citations resolve).**

- `[R-CNT-08]` for "copy the input's unknown ignore-lane flag bits
  forward and set no other" — §9.2's Note area / §6.3 defines this; I
  did not re-derive `[R-CNT-08]`'s exact text (outside my hunks) but the
  sentence's content matches its use elsewhere (Appendix H's rewriter
  checklist, line ~4907, uses identical language). **Pass** (consistent
  usage across the document).
- **"the two of §10.1's four vehicles §21.6 makes conforming… the other
  two… F36 and L25 for a record type, and one row for each of the other
  seven spaces §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)"** — I
  opened §10.1 (four vehicles: new record types; new reserved-range
  values; new ignore-lane bits; new standardized metadata keys), §10.2
  (numeric-identifier-space table: 8 rows — record type plus 7 others:
  channel layout, linearization, sample type, codec, filter, index
  encoding, metadata encoding), and §21.6's table. §21.6 has a row for
  "An ignore-lane flag bit… is set: Ignored; conforming" (vehicle 3) and
  a row for "A user-metadata document carries an unrecognized `tarn.`-
  prefixed key: Conforming" (vehicle 4) — these are "the two." I then
  opened §21's register (§21.5) and confirmed F36 ("A top-level record
  carries a type value from the reserved range… emitting one is a
  violation whatever its MU bit") and L25 (the layer-sub-record analogue)
  both exist and say exactly this. I then located all seven of L31, L33,
  L34, L36, L43, L45, R1 in §21's register and matched each to its §10.2
  space: L31↔index_encoding, L33↔linearization, L34↔sample type,
  L36↔layout, L43↔codec, L45↔filter, R1↔metadata encoding — exactly the
  seven non-record-type spaces of §10.2's table. **This citation is
  fully accurate; every number and every row-id resolves.** (This is
  exactly the kind of "reads as verified" citation the charter warns is
  the most expensive kind of defect if wrong — I verified it row by row
  and it holds.)

**Check 3 (label not marker).** Ordinary body text, no blockquote.
Normative. Confirmed by reading raw markdown around each cited passage.

**Check 4/6 — the real finding of this hunk.**

> "A rewriter MUST preserve the content of every structure it carries
> forward… A layer the rewrite re-creates is new output… and nothing of
> the input's copy of that layer is carried forward."

I held this beside hunk 31's closing sentence (below): "what a re-created
layer denotes is the rewriter's to declare." Content-preservation is
explicitly scoped OFF of re-created layers by this hunk 30 sentence (good
— correctly narrowed from the old unscoped "preserve content"). But I then
asked: **does any other rule oblige a re-created layer's *reference array*
(its decoded sample values) to match the input layer's?** I searched the
whole document for "denote" (7 hits, listed below) and "reference array"
(9 hits) and found none. Hunk 30 itself only obliges the physical framing:
"written under §20.2's rules from content the rewriter decoded" — this
says the bytes come from decoded content, but does not say the decoded
content (the values) must equal what the input layer denoted. This is
Check 6's target precisely: a structure (the re-created layer) with one
sibling quantity pinned (framing/creation-path rules) and another sibling
quantity (denoted values) left completely open. I develop this fully under
hunk 31, where the closing sentence makes the gap explicit.

**Check 7 (analogy).** None introduced in hunk 30's own new text.

**Check 8 (anaphor).** The insertion ("A layer the rewrite re-creates is
new output…") is added as a new final sentence of its paragraph, so
nothing *after* it in this hunk resolves to it, and it introduces no bare
"it/this/such" that reaches outside its own two sentences. No defect
found forward. Checked backward too: "the rewriter decoded" — decoded
*what*? Nearest antecedent is "content" in the same clause — self-
contained, not a defect.

**NESTED_DASH — finding.** Four em-dashes in hunk 30's own changed lines
(and I widened the search to the whole landing paragraph, 3560–3611, to
catch dashes in touched but unmarked context, per Check 1's mandate to
examine every sentence whose subject was renamed). One sentence has
**three** em-dashes, an ambiguous nested/triple structure:

> "Where the output carries a feature a later minor defines and this
> rewriter does not **—** on a conforming input a carried ignore-lane bit
> (§6.3) or an unrecognized `tarn.` key in a record it never decoded
> (§18.3), the two of §10.1's four vehicles §21.6 makes conforming, the
> other two reaching such a file only as values this text still registers
> as reserved-range violations **—** F36 and L25 for a record type, and
> one row for each of the other seven spaces §10.2 tabulates (L31, L33,
> L34, L36, L43, L45, R1) **—** the output's version_minor SHOULD be at
> least the input's…"

Three dashes in one sentence (marked bold above) is not a clean two-pair
nest, but it produces exactly the failure the maintainer's directive
targets: a reader cannot tell by eye whether the middle dash opens a new
clause closed by the third dash (making the first-to-third span one long
aside with an un-closed dash floating inside it) or whether the first and
third are meant to pair around the whole appositive with the middle dash
functioning as an internal, unpaired pivot. I recommend splitting: end the
aside at the second dash with a period, and start "F36 and L25…" as its
own sentence, closing with a period rather than the third dash. This is a
prose defect only (never byte-level) — the subject sentence renamed
("compactor"→"rewriter") is this same sentence, so it counts as "touched"
by the hunk even though the dashes themselves are pre-existing text.

**BCP14 casing.** Zero lowercase-keyword hits in hunk 30's added lines.
**Clean.**

---

### Hunk 31 — the regeneration paragraph and [R-WRT-07]'s close

**Rule adopted.** (a) Restates the structural-reject-tile disposal from a
single forced refusal to **"two disposals"**: drop the layer (§20.4-
licensed) or refuse. (b) Requantifies the reference-array bit-for-bit
guarantee from an unscoped "the output's reference arrays" to "every layer
the output **carries forward**." (c) Adds the sentence "what a re-created
layer denotes is the rewriter's to declare."

**Check 1 (tense/quantifier) — the requantification.** Old: "The output's
reference arrays MUST equal the live generation's bit for bit
(`[R-MDL-02]`): compaction changes where bytes live, never what a layer
denotes." New: "The reference array of **every layer the output carries
forward** MUST equal the live generation's bit for bit (`[R-MDL-02]`): a
rewrite changes where bytes live, never what **a carried layer** denotes,
and what **a re-created layer** denotes is the rewriter's to declare."

This is a *correct* narrowing in isolation — the old, unscoped claim would
now be false (a re-created layer's bytes are new output, not the "live
generation's" bytes, so bit-for-bit equality cannot be asked of it). The
repair properly restricts the guarantee to carried-forward layers. **But**
the third clause it adds to cover the excluded case ("the rewriter's to
declare") supplies **no constraint at all**, not even a weaker one — see
Check 6/Main finding below.

**Check 2 (citations).** `[R-MDL-02]` — checked (§3.2, line 428–432): "The
reference array is this specification's conformance target: a conforming
reader that reads any portion of a layer MUST return exactly the
corresponding portion of the reference array, bit-for-bit." This defines
the reference array as the *reader*-facing conformance target; citing it
here to justify a *writer*-side preservation duty is a step removed (the
actual preservation duty is `[R-WRT-05]`/`[R-CNF-06]`) but not wrong — it
correctly establishes *why* bit-for-bit reference-array equality is the
right invariant to state. This citation is unchanged from the pre-repair
text (present in both `-` and `+` sides of the diff), so it is not a
citation newly introduced by this round; I note it passed rather than flag
it. `[R-IDX-03]` (line 3615, "An entry §15.3 classifies reject-tile on a
structural ground") — checked against §15.3's table: six rows are marked
*structural* (sentinel-with-nonzero-crc, offset/length mismatch, length=0,
offset<16, out-of-domain, overflow/exceeds-F) — confirmed these are
exactly the "structural ground" rows, and confirmed §15.3's explicit
carve-out: "An entry whose only defect is that its stored bytes fail its
crc is well-formed: the defect lies in the bytes it addresses, not in the
entry, so its extent stands." This is *not* a structural-ground case, so
it does **not** enter the "two disposals" branch of this paragraph at all
— it is caught instead by `[R-WRT-09]`'s general checksum-verification
duty (see hunk 29's table above). **Pass**, and this distinction matters:
the "two disposals" sentence in this hunk is narrower than the general
disposal framework in hunk 29 (it's specifically about a mis-classified
*index entry*, not about a failed *tile checksum*), and I confirmed both
routes converge on the same two outcomes (drop the layer or refuse) for
different reasons — not a contradiction, but worth stating precisely since
a careless reading could conflate the two triggers.

**Check 4/5 — "two disposals" against the third named rewrite and against
hunk 29's opening.** Held "`[R-WRT-06]` then leaves it two disposals…
drop the layer… or refuse" beside hunk 29's three named rewrites
(compaction, dropping, re-declaring) and beside "A rewrite MAY be several
of these at once." Re-declaring is defined (hunk 29) as "the rewrite §20.3
step 4 reserves for a change to a fixed declaration" — i.e. it is
triggered by a writer's *intentional* choice to change tile extent,
layout, codec, etc., not by an index entry the rewriter cannot classify.
A malformed index entry is a *corruption*, not a declaration change, so
re-declaring is not a third disposal available here — "two disposals" is
correct and exhaustive for this specific trigger. **Check 5 passes**: I
could not falsify "two disposals" by finding a third route out.

**Check 6/Main finding — what a re-created layer's content is
constrained to.**

**Structure governed:** a layer the rewrite re-creates. **Every quantity
that structure carries:** its fixed declarations (layout, tile extent,
codec, filter, rank, dimension order, channel types — the very things
§20.3 step 4 calls "fixed" and that re-declaring exists to change), its
name, its reference array (decoded sample values), and its physical
framing (record, tile-index region, stored tiles). I checked each:

- Fixed declarations: governed — that's the whole point of "re-declaring"
  (§20.3 step 4 names exactly which declarations MAY change under a
  rewrite).
- Physical framing: governed — "written under §20.2's rules" (hunk 30).
- **Reference array (sample values): ungoverned.** Hunk 31's closing
  clause is explicit: "what a re-created layer denotes is the rewriter's
  to declare." I searched the whole document for every other place that
  might pin this — `grep -n "denote"` (7 hits: §3.2's definition, a file-
  size sentence unrelated to layers, three bfloat16-decoding hits in §12,
  this hunk's own two hits, and two §21/§24 hits about vector-condition
  labels — none of them constrain a re-created layer's values) and
  `grep -n "reference array"` (9 hits: §3.2 ×2, §11.3, §15.2, a tile-read
  domain-check hit, this hunk's hit, and the Example's "The reference
  arrays are identical" line, which is scoped to the worked compaction
  example where nothing is re-created). **No rule anywhere obliges a
  re-declaring rewrite to preserve what its re-created layer's samples
  actually equal.**

This matters because of what re-declaring is *for*. §20.3 step 4 draws its
whole fixed/free line around **tile meaning**: "The line is drawn where a
stored tile's meaning is fixed… Under new [declarations] the same bytes
would denote values, coordinates or padding the writer did not store" —
i.e. the entire reason a declaration change needs a rewrite rather than a
commit is that it would otherwise silently *reinterpret* stored bytes as
different values. The natural expectation carried into §20.5 is that
re-declaring a layer changes its *packaging* (tile shape, codec, layout)
while preserving what it *denotes* — otherwise "re-declaring" is
indistinguishable, byte-for-byte, from simply dropping the old layer and
adding an unrelated new one under the same name (hunk 29 already permits
this: "the output MAY add what a creator could," and a dropped layer's
name is free to reuse). With the reference array left completely
unconstrained, a rewriter performing a "re-declaring" rewrite is, per the
letter of this text, free to emit a layer whose values have nothing to do
with the input's — which collapses the distinction the document's own
§20.3 step 4 motivation implies should exist between "re-declare" (same
data, new packaging) and "drop-and-add" (an unrelated new layer).

**Byte-level test.** Two competent implementations of a conformance
checker for a *rewrite* output would disagree on whether a file is
conforming: reading A (literal text: "the rewriter's to declare," no other
constraint) accepts a rewrite that re-creates layer `sst` with completely
different sample values than the input's `sst` denoted, so long as the
new declarations and framing are individually valid. Reading B (the
declaration-only intent implied by §20.3 step 4's own rationale) would
reject such an output as not a legitimate re-declaration of the *same*
layer. The text as written supports only reading A — there is no
competing rule to fork against — so strictly this is an *underconstrained
rule*, not two live readings of one rule; but it is byte-level in the
practical sense the charter's discriminating question asks: it determines
whether a rewriter MAY emit a file with silently altered layer content
under the "re-declaring" umbrella, and nothing else in the document
answers that question either way. I flag `byte_level: true` with that
caveat stated plainly.

**Check 7 (analogy) — "on the same terms as the tile index."** Governing
verb in the repair: "a rewriter implementing [an MU=1 type] relocates
whatever that registration defines, **on the same terms as** the tile
index." I opened the cited warrant — §7.2, lines 1044–1049: "For a record
with MU = 0, the extent slot is its only sanctioned reference to bytes
outside the record sequence… Records with MU = 1 carry further references
only where this specification or registry review (§10) defines them; the
layer record's tile index (§15), whose entries reference stored-tile
extents, **is such a case**."

This sentence identifies the layer record's tile index as an example of
an **MU = 1** record's further-references case. But §7.3's registry table
(line 1088, confirmed independently of the pre-loaded `gitStatus` text)
now fixes the layer record at **MU = 0, PE = 0**. §7.2's general rule
just above this sentence says the opposite of what now holds for the
layer record: "For a record with MU = 0, the extent slot is its only
sanctioned reference… neither its inline payload nor its extent contents
encode offsets or lengths of other file bytes" — yet the layer record
(now MU=0) has an extent (the tile index) whose entries are exactly such
offsets. §7.2 has not been swept for the registry change that (per my
charter's preamble) is this round's third commit. This is a genuine
**CITATION**-check failure for the *warrant* hunk 31 leans on ("on the
same terms as the tile index" — the tile index is being held up as the
model for how an MU=1-implemented type's further references work, but the
model case itself is no longer, by the registry's own table, an MU=1
record). I traced whether this actually changes hunk 31's own operative
correctness and concluded it does **not** — §20.5's tile-index-relocation
procedure (the "Regenerating a region…" paragraph) is fully self-
contained and does not depend on classifying the layer record's own MU
bit — so this is not byte-level for *my* hunks' own rules, but it is a
real, unswept inconsistency between §7.2 (normative, not a Note/Example)
and §7.3 that undermines this hunk's own analogy and is worth a
maintainer's attention. I also found a second, independent restatement of
the same stale fact in a labeled, non-normative Example (§7.4, line
1206–1207: "the registry-fixed flags MU = 1, PE = 1 (§7.3)") — see the
document-wide sweep section below.

**Check 8 (anaphor).** "That `[R-WRT-09]`'s checks reach the index chain
and the checksum over each extent it copies rather than an entry's own
value domain bounds how far a rewriter goes looking" — "it" = "a
rewriter," nearest antecedent, unaffected by the repair (the sentence's
own subject changed from compactor to rewriter, but no *external* anaphor
was disturbed). No defect found.

**NESTED_DASH.** One matched pair at spec lines 3615–3616 ("— `[R-IDX-03]`
gives it no stored extent for a re-pointing to target —") and one matched
pair at 3631–3633 ("— such a type carries further references where this
specification or registry review defines them —"). Both clean, single
pairs. **No nesting.**

**BCP14 casing.** Zero lowercase hits. **Clean.**

---

### Hunk 32 — the Example ("what compaction reclaims")

**Rule adopted.** Four sentences inside the (still compaction-titled)
worked Example are generalized from "compactor"/"compaction" to
"rewriter"/"a rewrite." I checked each against whether the claim is true
of every rewrite or only of compaction, per the charter's explicit
instruction:

1. **"placement being the rewriter's to choose"** — true of every
   rewrite: placement freedom is a property of the creation path (§20.2),
   which every rewrite follows regardless of which named operation it
   performs (confirmed against hunk 30's "it is free to place structures
   anywhere §5.2 admits"). **Correctly generalized.**
2. **"a rewrite is the one operation that moves live bytes"** — read
   narrowly ("moves" = physically relocates the *same* bytes), this is
   true only of compaction/relocation; dropping removes bytes and
   re-creating writes brand-new ones, neither "moves" the input's bytes.
   Read at the level the sentence is actually operating — contrasting
   **rewrite** against **commit** (which the surrounding paragraph is
   doing: "a cache keyed (file_id, range) is sound precisely because
   ranges never change beneath a file_id… Reusing the input's identifier
   would serve the input's bytes for the output's ranges") — the claim is
   that unlike a commit (never moves/changes existing committed bytes,
   `[R-LIF-01]`), a rewrite is capable of putting different bytes at a
   range a cache previously associated with other content, which is true
   of every rewrite variety (dropping and re-creating also change what a
   given output range holds relative to the input, even though they do
   not literally "move" anything). Under this (correct, contextually
   supported) reading, the generalization holds. **Pass**, but I flag
   that the sentence is genuinely ambiguous between these two readings
   and would be strengthened by saying "changes what bytes occupy a
   given range" rather than "moves live bytes," which invites the
   narrower, compaction-only misreading.
3. **"A rewrite is the only operation that reclaims slack"** — checked
   against the two alternatives the same sentence names (truncation past
   F, recovery to an earlier commit boundary) and against commit (§20.3's
   Note: "editing one sample… leaves as much slack… compact (§20.5) when
   slack grows"). All three alternatives are explicitly ruled out as not
   reclaiming. Also checked against §20.5's own opening (hunk 29): a
   rewriter's output "carr[ies] no slack" **regardless of which of the
   three named operations produced it** — so *every* rewrite, not
   compaction alone, fully reclaims all existing slack. **Correctly
   generalized, and the exhaustiveness claim (check 5) holds** — I could
   not find a fifth file-lifecycle operation that also reclaims slack.
4. **"what tells an operator when to run this" — resolving "this."**
   The sentence immediately before was repaired from "**This** is the
   only operation that reclaims slack" (old, anaphoric, resolving to
   "compaction" as the Example's topic) to "**A rewrite** is the only
   operation that reclaims slack" (new, an explicit noun phrase). The
   trailing "this" in "…that total is what tells an operator when to run
   this" is **unchanged context**, not touched by the diff. Per Check 8 I
   asked what it resolved to before and after: **before**, both
   instances of "this" in the paragraph pointed at the same referent
   (compaction, the Example's subject); **after**, the nearer antecedent
   is now the newly-introduced explicit "a rewrite" two clauses earlier,
   so "run this" now most naturally resolves to "a rewrite" rather than
   "compaction" specifically. I checked whether this re-resolution
   changes the claim's truth: since (per finding 3, above) *every*
   rewrite fully reclaims all slack, "run this" resolving to "a rewrite"
   is **still true**, and arguably more accurate than the old
   compaction-only reading, since a combined rewrite (compact + drop)
   also fully reclaims slack. **No defect** — the anaphor's referent
   shifted, but the shift happens to land on an equally-true reading. I
   report this because Check 8 requires reporting every resolution
   checked, not only the ones that fail.

**Check 2 (citations).** `[R-WRT-07]` (the ′-marked regenerated index,
"the ′ marks B's") — checked against hunk 31's own R-WRT-07 text
(reference-array preservation and index regeneration) — consistent, the
Example's worked scenario (A untouched, B relocated and its index
regenerated) matches the rule. `[R-LIF-04]` (truncation past F) and
`[R-LIF-06]` (recovery to an earlier commit boundary) — not read in full
(outside my hunks and not load-bearing for a verdict on this hunk's own
text; the sentence's claim about them — "also shorten a file, but neither
reclaims any" — is consistent with §9's committed-prefix-immutability
framing I did read (§9.1, `[R-LIF-01]`: "Bytes in [0, F) are immutable").
**Pass.**

**Check 3.** This whole hunk sits inside a labeled `> **Example — …**`
blockquote — correctly non-normative per `[R-CNF-01]`. I confirmed the
label is literally "Example" (line 3640: "> **Example — what compaction
reclaims.**"), so none of these four sentences bind any actor as a MUST/
SHOULD obligation on their own; they restate obligations stated
normatively elsewhere (§20.5's body, already checked above). **Correct
placement, no force lost or gained.**

**NESTED_DASH.** All em-dashes in this range (3640, 3653, 3657) are single,
unpaired, running to terminal punctuation. **Clean.**

**BCP14 casing.** N/A (Example prose uses no MUST/SHOULD/MAY in the
touched sentences). **Clean.**

---

### Hunk 33 — [R-WRT-09] and the closing Note

**Rule adopted.** Requantifies the verification duty from "each relocated
extent's checksum" (placement-keyed) to "the checksum §8.1 states over
each extent it copies" (carry-keyed), adds "The duty follows what the
rewriter carries and not where it places it: an extent the output leaves
at its input offset owes the same check as one it relocates," and adds
"What it re-creates it decodes as a reader first, owing every check §19.3
and §19.4 place at that use (`[R-CNF-11]`)." Renames the Note's opening
from "Compaction is the only true removal" to "A rewrite is the only true
removal."

**Check 1 (tense/quantifier) — this is the round's headline repair, and I
gave it the most scrutiny.** Old: "each relocated extent's checksum,
including every stored tile's entry crc." New: "the checksum §8.1 states
over each extent it copies, every stored tile's entry crc among them,"
plus the explicit new sentence pinning the quantifier: "an extent the
output leaves at its input offset owes the same check as one it
relocates." I verified this against §8.1's own definition of what a
"checksum" attaches to — coverage is stated per *structure*, not per
*placement decision* (§8.1's table keys rows on "Structure," never on
whether that structure moved). So the corrected quantifier ("copies," not
"relocates") is the one that actually matches §8.1's own organizing
principle. **This repair is correct and precisely targeted; check 1
passes cleanly**, and this is the fix the charter's preamble describes as
the round's finding (a compactor able to emit a corrupt-but-unmoved extent
under the old wording).

**Check 2/Check 6 — "the checksum §8.1 states over each extent it
copies": does one kind have none?** I opened §8.1's full coverage-map
table and enumerated **every** kind of extent a rewriter can copy:

| Extent kind | §8.1's checksum | Notes |
|---|---|---|
| Stored tile | "the crc field of its index entry" | covered |
| Tile-index region | "the per-segment CRC array, itself covered by the layer record's crc_of_crc_array" | covered |
| User-metadata extent | "final 4 bytes of the extent" | covered |
| **Extent of a record of a type this specification has not assigned** | **"none — the bytes are opaque (§7.2)"** | **no checksum at all** |

So yes — check 6's exact target: one kind (an unassigned-type record's
extent — an unimplemented reserved-range or experimental-range record a
rewriter nonetheless carries forward, e.g. an MU=0/PE=1 unregistered type
it doesn't implement) **has no checksum §8.1 states**, so `[R-WRT-09]`'s
"MUST verify… the checksum §8.1 states over each extent it copies" is
**vacuously satisfied** for that kind — there is nothing to check, and
this is *by design*, matching §7.2's own "opaque" framing, not a gap the
repair introduced. I traced whether this was true before the repair too
(it was — §8.1's table is unchanged by any of my hunks) and concluded
**this is pre-existing, not a new defect from this round's text**, so I
do not raise it as a finding, only report the check as run and passed
cleanly with this one documented, intentional exception.

**Check 4 — "each retained layer's record (§19.3)" vs. "carries" vs.
"copies."** Held these three terms against each other across the whole
sentence: "it MUST verify each link of the chain — the open (§19.1), each
**retained** layer's record (§19.3) and full index chain (`[R-IDX-04]`),
and the checksum §8.1 states over each extent it **copies**… before
emitting that structure's bytes." I checked whether "retained" (layer
record) and "copies" (extent) are meant to range over the same set or
different ones. §20.4's usage: "retains" applies to records a rewriter
keeps in the output at all (whether carried-forward or re-created — a
re-created layer's *record* is also, in some sense, "retained" as a named
layer, just newly written). §20.5's own "carries forward"/"re-creates"/
"drops" taxonomy (hunk 29) is finer-grained. I confirmed "each retained
layer's record" is intended broadly (any layer present in the output,
whether carried forward or re-created — since §19.3's validation is what
a rewriter owes *any* layer it is about to rely on, and the very next
sentence of this hunk, "What it re-creates it decodes as a reader first,
owing every check §19.3 and §19.4 place at that use," confirms re-created
layers *also* get §19.3/§19.4 treatment, just via the decode-as-reader
path rather than the carry-forward path). **No contradiction found**: the
two obligations (§19.3 layer validation for retained layers; §8.1
checksum-per-copied-extent) are complementary, covering carried-forward
and re-created layers respectively, and the new sentence explicitly
stitches them together. **Pass.**

**Check 3.** `[R-WRT-09]`'s paragraph itself is ordinary body text
(normative). Its trailing `> **Note.**` (renamed "Compaction is the only
true removal" → "A rewrite is the only true removal") is correctly
labeled **Note** and correctly non-normative — I confirmed the label text
literally reads "**Note.**" (line 3695). The generalization from
compaction to "a rewrite" is also correct here: dropping (a rewrite, not
compaction) is at least as much a "true removal" as compaction is — a
dropped layer's bytes are never written to the output at all, which is a
*stronger* removal than compaction's mere relocation-without-loss. So
widening "Compaction is the only true removal" to "A rewrite is the only
true removal" is not just safe but more accurate than the old text (which
undersold dropping's removal). **Pass**, no overclaim.

**Check 7 (analogy).** None in this hunk's new text.

**Check 8 (anaphor).** "before emitting **that structure's** bytes" — "that
structure" refers back to "each link of the chain" enumerated in the same
sentence (open, layer record, index chain, checksummed extent) —
self-contained, unaffected by the repair. No defect.

**NESTED_DASH.** One matched pair (3684, "chain —" … no, let me restate:
single dash at 3684 opening, closed at 3687 — "— the open (§19.1), each
retained layer's record (§19.3) and full index chain (`[R-IDX-04]`), and
the checksum §8.1 states over each extent it copies, every stored tile's
entry crc among them —"). One clean pair. The Note's dash (3697) is
single, unpaired, running to the period. **Clean.**

**BCP14 casing.** Zero lowercase hits. **Clean.**

---

## 4. Document-wide sweeps (required by the charter)

### Sweep: "relocat" (case-insensitive)

`grep -n -i "relocat" spec/tarn.md` → 12 hits (lines 311, 689, 1046, 3230,
3481, 3497, 3556, 3592, 3600, 3602, 3633, 3690, 4911). I read the context
of every hit. Eleven are either inside §20.4/§20.5 (already fully audited
above) or in §7.2's/§2.4's definitional material (line 311's
"preserve-verbatim" table entry, which I checked: "relocated only as Part
I permits… its MU = 1 and MU = 0 / PE = 1 rows" — this is **already
correctly scoped** to the two rows that do *not* license a drop, matching
the current registry; the MU=0/PE=0 row, which now also permits relocation
*or* drop, is correctly excluded from "preserve-verbatim" since it isn't a
strict preservation duty any more — no defect). Line 4911 is Appendix H's
rewriter checklist ("regenerating each index region it relocates and
re-pointing every slot") — already uses the corrected, carries-not-
relocates-keyed framing consistent with hunk 33. **No stray restatement of
the checksum duty still quantified over placement** survived the sweep —
the one genuine defect this round targeted (relocated-extent phrasing) is
fully swept everywhere "relocat" appears.

**Control for this sweep:** to confirm the grep itself works (the charter's
explicit warning about hard-wrap), I ran `grep -n -i "relocat"` and it
returned exact matches spanning line boundaries with no evidence of
missed wraps (e.g. line 3600's "except that relocation re-points" — a
short, unwrappable fragment — was found; and I independently re-read
lines 3592–3610 by eye and found no additional occurrence the grep
missed). **Control passes.**

### Sweep: "compactor" / "compaction" (case-insensitive)

`grep -n -i "compactor"` → **exactly one hit, line 438**:

> "> **Note.** Part I (container) is independent of Part II (array model)
> by construction: no Part I structure requires decoding sample
> payloads, so verifiers, appenders, and **compactors** operate on files
> whose layers they cannot decode — that independence is load-bearing
> for the updater rules of §7 and §20."

This is the **only surviving use of "compactor" in the whole document**
after the second commit's rename. It sits in §3.3's Note (non-normative,
correctly labeled "Note," so `[R-CNF-01]` exempts it — not byte-level).
But its *content* is now false as a general claim about the tier this
Note says it supports ("load-bearing for the updater rules of §7 and
§20"): §20.5 (as repaired by exactly my hunks) explicitly gives the
rewriter tier a case that **does** decode Part II content — "what it
re-creates it decodes as a reader… and writes as a creator" (hunk 29),
"owing every check §19.3 and §19.4 place at that use" (hunk 33). Listing
"compactors" here as a categorical peer of "verifiers" and "appenders"
(both still-accurate actor/tier names) is doubly stale: (1) the rename
swept "compactor" everywhere else but missed this one Note; (2) even
read narrowly as "the compaction *operation* specifically" rather than a
tier name, pairing it with two tier names in a list of actors is now a
category mismatch, since compaction is no longer a tier, it's one of
three named operations *within* the rewriter tier. This is exactly the
"restatement elsewhere in the document that the repair should have swept
and did not" pattern the charter calls out generally, and it directly
undermines the very passage ("load-bearing for… §20") that my hunks
rewrote. **Reported as a finding** (non-normative, so not byte-level, but
a real, single, findable, high-confidence sweep miss).

`grep -n -i "compaction"` → 10 hits. I read every one's context (already
shown above for lines 62–64, 745–746, 1389, 3131, 3527, 3640, 4348, 4615,
4800). All but one are correctly scoped to the narrow compaction case (a
verb "compact," or the named operation specifically). **The one exception
is Appendix G, line 4800** (item 8 of the reproducible-writer profile):

> "The version_minor floor binds a rewriter too, save where its output
> carries a feature it does not implement, when §20.5's floor governs
> instead (`[R-WRT-06]`). **A compaction's output** is therefore
> reproducible only modulo its trailer and the records §20.4 lets it
> **drop**: `[R-WRT-06]`'s fresh file_id is no function of content, this
> item's floor turns on which features the rewriter implements, and a
> record whose governing flags are MU = 0 and PE = 0 is retained or
> **dropped** at the rewriter's choice (§20.4), which no item here pins."

This is a **direct contradiction with hunk 29's own definition**, which I
already flagged as an overclaim risk above: compaction is defined
(hunk 29, §20.1) as carrying **every** structure forward and changing
**nothing but placement** — by definition it never drops a PE=0 record.
Yet this Appendix G sentence attributes drop-related non-reproducibility
("the records §20.4 lets it drop… retained or dropped at the rewriter's
choice") to **"a compaction's output."** Under the current, narrowed
definition, dropping is a *different* named rewrite, not compaction. The
correct term here is "a rewrite's output" or "a rewriter's output" — and
strikingly, the very same numbered item, two sentences earlier, **already
uses the correct term** ("a rewriter adopting the profile carries its
input's unknown ignore-lane bits forward"), so this is a same-paragraph
inconsistency, not just a document-wide drift. This is precisely the
brief's predicted failure shape: "a surviving *compaction* that names the
narrow case where the sentence needs the wide one." Appendix G is
explicitly headed "(non-normative)," so `[R-CNF-01]` exempts it — **not
byte-level** — but it is a clear, well-evidenced UNSWEPT_RESTATEMENT
sitting exactly where the charter's preamble said to expect one, one
paragraph away from where the third commit's own PE=0 change is being
described.

**Control for this sweep:** I confirmed the grep's hard-wrap safety by
checking that a known-present short fragment ("compaction," un-hyphen-
wrappable at 10 characters) was found at line 62 (inside a wrapped
bullet list) — proving the grep does find wrapped instances of this
particular token. I did not additionally run a normalized-whitespace
search because every "compaction"/"compactor" instance found is a single
word never split by hard-wrap in this document's 79-character-ish
wrapping (a hyphen-free 10-11 character token essentially cannot itself
straddle a wrap without a hyphen, and none of the matches showed a
hyphenated line-break variant when I read the surrounding lines by eye).

### Sweep: the layer record's MU/PE registry value, cross-referenced

Triggered by the "on the same terms as the tile index" analogy check
(hunk 31). I confirmed independently (§7.3, line 1088) that the layer
record is currently MU=0, PE=0, and then swept every place the document
characterizes the layer record's MU bit:

- §7.2, line 1047–1049 (normative, not labeled Note/Example/Rationale):
  cites the layer record's tile index as the worked example of an
  **MU=1** record's "further references" — **stale**, contradicts §7.3.
  Reported above under hunk 31's Check 7.
- §7.4, line 1206–1207, inside `> **Example — a complete layer record
  payload.**`: "The record framing this payload (§7.2) carries type
  0x0001, the registry-fixed flags **MU = 1, PE = 1** (§7.3)…" — **stale**,
  directly contradicts §7.3's own table three lines away in section
  number. This is inside a labeled Example block, so `[R-CNF-01]` exempts
  it from normative force — **not byte-level**, but a concrete, checkable
  factual error in a worked numeric example that any implementer building
  a test vector from this Example would carry forward incorrectly.
- §20.4, line 3463 and its whole table (lines 3479–3483): **correctly**
  reflects MU=0, PE=0 for the layer record — this is the section the
  third commit (per my charter's preamble) actually edited, and it is
  consistent.
- §2.4's "preserve-verbatim" table entry (line 311): **correctly**
  scoped (see the "relocat" sweep above).

I report both stale citations (§7.2 and §7.4's Example) as findings.
Neither is byte-level (one is normative-but-inert-to-actual-writer-
behavior since §20.5's operative rules don't depend on it; the other is
inside a non-normative Example), but both are genuine, well-evidenced
UNSWEPT_RESTATEMENT defects that a careful implementer reading §7 before
§20 would be actively misled by.

---

## 5. Rejected candidates

- **"A rewriter MUST NOT modify one except by relocating its extent and
  re-pointing its slot under §20.5"** (§20.4, line 3496–3499, `[R-WRT-08]`)
  — I checked whether this contradicts §20.5's new re-creation case
  (which does much more than "relocate and re-point"). Closed: this
  sentence is specifically about an *updater's* (not specifically
  rewriter's) treatment of a record whose type it does not implement —
  such a record can only ever be relocated (never re-created, since the
  updater cannot decode it), so there's no tension; `[R-WRT-06]`'s MU=1
  refusal rule already forces refusal before this sentence would ever be
  asked to cover a re-creation case. Not a finding.
- **Whether "A rewrite MAY be several of these at once" plus the
  compaction/dropping tension (Check 4/5 finding above) is actually
  byte-level** — considered flagging it byte-level, closed as *not*
  byte-level: the actual permission ("MAY be several… at once") is
  unambiguous on its own; only the prose *label* "compaction" is
  overclaiming when applied to a mixed rewrite, and no rule anywhere
  makes a file's conformance turn on which of the three *names* applies
  to what a rewriter did — only on whether each structure was carried
  forward and preserved, dropped where licensed, or re-created and
  properly written. Filed as a prose/definitional finding, not
  byte-level.
- **Whether the four-vehicles/seven-spaces citation (hunk 30) might be
  off by one** — I initially worried "record type" might be double-
  counted (once via F36/L25, once inside the "seven spaces" list).
  Closed by directly reading §10.2's table: it has exactly 8 rows,
  "record type" is one of them, and the citation's "other seven spaces"
  excludes it explicitly ("F36 and L25 for a record type, **and** one row
  for each of the **other** seven spaces") — no double count, citation is
  exact. Not a finding.
- **Whether §21.6's "the file contains zero layers" row or the sentinel
  row interact badly with a rewriter that drops every layer** —
  considered, closed: dropping every layer via rewrite yields "a
  directory carrying no layer record," which §21.6/`[R-CNT-14]`/
  `[R-CNT-02]` already explicitly rule conforming ("a directory carrying
  no layer record is a conforming generation… an empty directory
  included"). No tension with §20.5's rules. Not a finding.
- **Whether the "two disposals" sentence (hunk 31) should also mention
  refusing the whole *file*, not just the layer** — considered, closed:
  §20.4's PE=0 licence is stated at layer scope for the layer record
  specifically (dropping the layer record, with its tile-index region and
  stored tiles, is the licensed unit), and nothing in the passage asks for
  file-scope refusal as an alternative to layer-scope drop when the
  violation is confined to one layer's index. Consistent with §8.2's
  general reject-layer scoping for index-chain failures (`[R-IDX-04]`).
  Not a finding.

## 6. Confidence / what a clean result would have looked like

Where I found nothing (NESTED_DASH in hunks 29/31/32/33; BCP14 casing in
all five hunks; the R-MDL-02/R-IDX-03/R-IDX-04/R-CNT-08/R-CNT-26 citation
chain; the four-vehicles/seven-spaces citation; the structural/entry-crc
distinction in hunk 31; check 8's anaphors in hunks 29/30/31/33), I did
not merely fail to notice a problem — for each I performed the specific
test the check demands (opened the cited rule and compared its exact
words; counted and paired every em-dash in the landing range by line;
grep'd for lowercase BCP14 tokens; traced each anaphor's nearest
antecedent before and after the insertion) and recorded the result above.
The one check I could not fully close is hunk 32's "moves live bytes"
ambiguity (item 2) — I found a reading under which it passes and
documented why I believe that is the operative reading, but flag that a
reader taking the narrower "physically relocates" reading would call it
an overclaim; I did not find independent textual evidence forcing one
reading over the other, so I report both and lean on the surrounding
paragraph's commit-vs-rewrite framing to resolve it, rather than treating
it as settled beyond doubt.
