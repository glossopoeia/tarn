# Round 25 audit — downstream-accounts charter (hunks 01 and 02)

## 0. Disclosure

Files opened:
- `/private/tmp/.../r25audit/hunk-01.diff` (my charter)
- `/private/tmp/.../r25audit/hunk-02.diff` (my charter)
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (many ranges, listed below)

Nothing else. I did not open `full.diff`, other hunk files, `docs/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`, `spec/registry.json`,
git history, or the web. I did not list the r25audit directory (I `cat`'d the two
named files by their full paths and wrote this one file with a heredoc).

Unrequested context that appeared before I began: a project-instruction block
pointing at `AGENTS.md`, and an index of the maintainer's memory files naming
several topics including one about a register/corpus relationship and one about
propagation checks. I did not open any of those files and drew no conclusion from
their titles. Their presence is disclosed here; nothing in this audit rests on them.

Commands run:
- `wc -l spec/tarn.md`
- `sed -n` over spec/tarn.md line ranges: 120-180, 180-235, 548-600, 735-800,
  825-845, 1140-1210, 1240-1280, 1455-1510, 2895-2940, 2960-3080, 3150-3300,
  3340-3400, 3658-3760, 3930-3975, 4300-4400, 4400-4471.
- Built a whitespace-normalised stream of spec/tarn.md plus a char->line map in
  `/private/tmp/.../scratchpad/norm.txt` and `pos.json` (python3, reads only
  spec/tarn.md), then ran a regex query script `q.py` against it. This is the
  hard-wrap workaround: every phrase search below is wrap-insensitive.
- `grep -n` for a set of short unwrappable fragments to fix line numbers.

Normalised-search queries run (hit counts in brackets):
  `R-LIF-02` [13], `21\.7` [8], `shrink|shrunk|shrinking` [8], `§20\.3` [12],
  `barrier` [13], `pre-trailer` [13], `durab|fdatasync|torn` [20],
  `compactor|compaction` [55], `R-SER-05` [13], `R-CNT-17` [13].

---

## 1. What each repair changed about the document's CONTENT

### Hunk 1 (§20.3 step 4, shrink paragraph, line 3029ff)

Removed: "a shrink that turns real positions into padding of a tile stored there
is barred whether or not the new state still stores it."

Added: "a shrink that alters what §14 fixes for a tile stored there is barred
whether or not the new state still stores it. What counts as such an alteration
is the bar above and nothing else, its carve-out included — a new padding position
whose stored byte already holds the fill `[R-SER-05]` fixes is not one, so a
shrink producing only those is permitted here exactly as it is there, and this
sentence answers the rescue question rather than restating the test."

**Content change.** The old rescue sentence barred *any* shrink that converts real
positions to padding on a prior-generation stored tile. The main bar three
paragraphs up (line 3009-3012) carves out exactly that case when the stored byte
already holds the fill. The two collided. The repair resolves the collision in
favour of the carve-out.

What is now permitted that was not: **a commit MAY shrink a dimension extent of a
layer that stored tiles in the superseded generation, where every position the
shrink turns into padding already holds that channel's recorded fill.** The
smallest witness: Eᵢ = 10, Tᵢ = 16 (Gᵢ = 1, one addressed tile, positions 10..15
already padding). Shrink Eᵢ to 9. Position 9 becomes padding; if its stored byte
already equals fill, the carve-out applies and the shrink is permitted. Note
Gᵢ = ⌈9/16⌉ = 1 is **unchanged**: no tile is de-addressed and entry_count does not
move.

Nothing is newly barred. Nothing previously fixed became unfixed.

### Hunk 2 (§20.5, line 3223ff)

Added a whole paragraph: `[R-LIF-02]`'s commit protocol does not bind a compactor;
neither its barrier ordering nor its step 5 pad reaches the compactor tier. Two
named consequences: (a) the output's pre-trailer gap "is fixed by nothing", so two
conforming compactors given one input MAY emit outputs of different lengths and a
longer-than-a-commit gap is conforming; (b) no barrier ordering is owed within the
output, justified by "a torn output is an unreadable file rather than a damaged
one". Plus a new obligation: "A compactor SHOULD make its output durable before
anything discards the input."

**Content change.** Before, §20.5 said nothing about the commit protocol, and the
natural reading — a compaction output is a generation-1 file, and §9.2's creation
path is how generation-1 files get written — bound a compactor to steps 4-6 (both
barriers) and step 5 (minimal pad). The repair severs that. Now permitted that was
not: **a compactor may emit an output whose pre-trailer gap exceeds the minimal
64-byte-boundary pad, and may write its output's bytes in any order.** Newly
fixed by nothing that was fixed before: the write ordering of a compaction output.
Newly created: a SHOULD-level durability obligation replacing what was a
MUST-level barrier pair.

---

## 2. Passages that depended on the old answers

Method: grep the *terms*, not the identifiers; then read where every hit sits.

### 2a. Depending on hunk 1's old answer (a real→padding shrink is barred)

Query `shrink|shrunk|shrinking` [8 hits]: lines 1487, 3033, 3034, 3043, 3048,
3053, 3938, 3945.

**Line 3053, §20.3 step 4, SAME PARAGRAPH, unchanged by the repair:**

> "Where a shrink is permitted the de-addressed tiles' extents become slack
> (`[R-CNT-21]`), `[R-CNT-17]` obliges the smaller entry_count and so a
> re-emitted index region, and every surviving stored tile is untouched."

Universally quantified over permitted shrinks. For the class the repair newly
names — a grid-count-preserving shrink producing only fill-holding padding
positions — every clause but the last is false: there are no de-addressed tiles,
`[R-CNT-17]` obliges no smaller entry_count, and no index region is re-emitted.

Checked `[R-CNT-17]` at line 1042: "Under index_encoding 1, extent_length MUST
equal entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 ... or an entry_count that does
not equal the geometry-derived addressed-tile count, is a validity error at layer
scope." The addressed-tile count is N (interleaved) or C·N (planar), N = ∏Gᵢ
(§11.2, line 1502). Gᵢ unchanged ⟹ entry_count unchanged. Confirmed.

This collides with two other unchanged statements:

- §20.3 step 4 opening, line 2980: "Every layer whose stored-tile set or index
  content this commit changes has its tile-index region re-emitted in full". A
  grid-count-preserving shrink changes neither.
- §20.3 step 4, line 2989-2993: "A layer whose record alone changes **keeps its
  extent slot, pointing at the existing region**, as does a layer the commit
  leaves untouched (`[R-WRT-05]`); **relocating a live index region is
  compaction's operation (§20.5, `[R-WRT-07]`), not an appender's**." So an
  appender that follows line 3053 and re-emits the index region for this shrink
  performs an operation this same subsection reserves to a compactor.
- §11.1 Rationale, line 1491-1497, states the growth half correctly and
  symmetrically: "Growth that leaves every grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) unchanged
  **touches the directory alone**; growth that raises one changes entry_count and
  with it extent_length (`[R-CNT-17]`), so the layer's whole tile-index region is
  re-emitted". The document already knows a grid-count-preserving extent change
  touches the directory alone. Line 3053 says the opposite for shrinks.

=> FINDING B-01. Byte-level: yes (worked below).

Honesty note: line 3053 was already imprecise pre-repair for a layer that stored
nothing in the superseded generation (freely re-declarable, line 3020-3024) — such
a shrink can also preserve the grid count. But that case is handled by a different
sentence and the paragraph's subject is a layer with prior-generation stored tiles.
The repair puts the non-empty case squarely against line 3053, three sentences
after the widening.

**Line 1487-1490, §11.1 Rationale (inside a ">" block, non-normative):**

> "§20.3 states normatively, and governs, what a commit may do to a layer that
> already stored tiles in the generation a commit supersedes: a shrink is barred
> wherever it alters what §14 fixes for such a tile — whether or not the new state
> still stores it — and **permitted where it only drops tiles out of the addressed
> set**, whose extents then become slack."

The bar half matches the repaired wording verbatim in substance. The permission
half is a two-case partition ("barred wherever X ... and permitted where only Y")
that names de-addressing as the whole of the permitted class. Under the repair the
permitted class is strictly larger: a shrink that de-addresses nothing at all is
permitted when the new padding positions already hold the fill. Under the OLD
rescue sentence this restatement was exactly right; the repair invalidated it and
did not sweep it.

=> FINDING B-02.

**Line 3938-3940, §23.1 `[R-PRV-01]`, normative:**

> "A commit removes sample data **two ways** — superseding it, and a shrink that
> de-addresses tiles (§20.3 step 4) — and a dropped ancillary record's extent
> (§20.4) goes the same way"

A closed count. The repair adds a third way: a shrink that converts real positions
to padding without de-addressing anything. Those positions leave the layer's
addressable extent; §11.3/§2.4 keep a reader from ever returning a padding
position, and the bytes remain in the file. Under the old rescue sentence that
route was barred for any layer with prior-generation stored tiles, so "two ways"
was complete.

=> FINDING B-03. The MUST NOT that follows ("Writers ... MUST NOT represent any
commit that makes sample data unreachable as erasure of it") is quantified over
"any commit", so the normative force survives; the count does not.

**Line 3945 (§23.1, same requirement) and line 3690 (§21.7):** checked, unaffected.
§21.7's "§20.3 step 4's bar on a declaration change is witnessed only where the
affected tiles remain stored, and then only for part of what it bars" plus "A
change reaching a byte §14 structurally constrains — a padding position, a pad bit,
or a boolean byte — fires §21.4's content rows" remains correct after the repair:
a barred real→padding shrink (byte NOT holding fill) is witnessed by T2/T4 where
the tile remains stored; the newly-permitted one is not a violation and needs no
witness. No finding.

Query `§20\.3` [12 hits]: 65, 604, 608, 1484, 1497, 1787, 3171, 3227, 3327, 3690,
3938, 4438. Line 1787's Note ("each commit that changes a layer's stored-tile set,
or that grows its extents across a grid boundary, re-emits that layer's whole
tile-index region") is about growth and stored-tile-set change; unaffected.
Line 4438 (Appendix H updater) unaffected. Others read and unaffected.

### 2b. Depending on hunk 2's old answer (a compactor follows [R-LIF-02])

Query `barrier` [13 hits]: 783, 1174, 1183, 1193, 2927, 2928, 2929, 3071, 3074,
3225, 3234, 3237, **4432**.

**Line 4429-4433, Appendix H, "Conforming writer" checklist (non-normative):**

> "**Conforming writer** — emits only conforming files (§2.3); ... **follows the
> commit protocol including both barriers (§9.2)**; honors any alignment or slab
> it declares (§16)."

Quantified over the §2.3 "Conforming writer" class. §20.1 line 2909-2913 places the
compactor inside it: "An appender and a compactor satisfy every writer requirement
for the bytes they produce". Post-repair a compactor follows neither the barriers
nor step 5's pad, so this checklist line is false for one of the three writer tiers.
Pre-repair it was true under the natural reading. Unswept.

=> FINDING B-04. Non-normative (Appendix H's own header: "each entry's authority is
the requirement or section cited, never this summary"), so no normative conflict —
but it is a restatement the repair should have swept, and it is the passage an
implementer auditing a compactor is pointed at.

Query `pre-trailer` [13 hits]: 153, 566, 631, 661, 755, 837, 1981, 3229, 3446,
3618, 4089, 4108, 4334.

**Line 836-838, §6.4 `[R-CNT-09]`, normative:**

> "Writers SHOULD keep dir_length plus **the pre-trailer pad** plus 64 within
> 65,536 bytes so that a 64 KiB suffix fetch captures trailer and directory
> together"

Quantified over "Writers", which includes a compactor. This is a live bound on the
compactor's pre-trailer gap. The repair's bolded thesis is "**The output's
pre-trailer gap is fixed by nothing.**"

**Line 660-661, §5.2 `[R-CNT-03]`, normative:** "Writers SHOULD zero the gaps they
create — the run before an aligned tile or slab run, and **the pre-trailer pad**."
Also binds a compactor; also constrains the gap (its content).

**Line 754-757, §6.2 `[R-CNT-05]`, normative:** "Writers MUST place the directory so
that no structure lies between its end and the trailer." A MUST on the gap's
occupancy, binding every writer. Register row F7 (line 3448) is its witness.

**Line 566-568, §5.1 `[R-CNT-01]`, normative:** "The file size of a conforming file
equals the live trailer's committed file length F, and **F is a multiple of 64**
(§6.2)." With §6.2's "The trailer occupies the final 64 bytes ... beginning at a
64-aligned offset (equivalently: F mod 64 = 0)", the gap's length mod 64 is fixed
by where the directory ends. A compactor cannot choose an arbitrary gap length —
only multiples of 64 above the minimum.

=> FINDING B-05: "fixed by nothing" is falsified four ways by unchanged text.

Verified the repair's own sub-claim: "§6.2 ... bounds the gap ahead of it only
through step 5". §6.2 line 756-760: "bounds their number only through step 5 of the
commit protocol, which pads to the next 64-byte boundary (`[R-LIF-02]`) — a longer
gap is conforming, and no conforming commit produces one." That sub-claim about
§6.2 in particular is CORRECT. The overclaim is the bolded thesis, which ranges
over the document.

Also checked §6.2's "no conforming commit produces one": still true after the
repair, since a compaction is not a commit ([R-LIF-01], line 1162-1164). No finding.

**Line 148-157, §2.3 `[R-CNF-02]`, normative:**

> "A writer obligation whose violation this specification expressly declares not to
> be a file-conformance violation **binds the actor in the same way**; §6.3's
> flags = 0 against a set ignore-lane bit and **§6.2's pre-trailer gap longer than
> `[R-LIF-02]` step 5's pad** are the cases this text states"

The repair cites this: "a gap longer than a commit would have produced is
conforming — **one of the writer obligations §2.3 names as no file-conformance
violation**." Two problems, one inside and one outside the hunk.

Inside: the citation defeats the thesis. §2.3's carve-out is for a writer
obligation that IS violated but does not make the file nonconforming; it says
such an obligation "binds the actor". If the compactor's long gap is that case,
the compactor is conduct-bound not to produce it, contradicting "fixed by nothing"
and "MAY emit outputs of different lengths". If it is not that case (nothing binds
a compactor here), the citation misfires — the long gap is simply permitted, not a
declared non-violation.

Outside: §2.3 is unchanged and its statement is unqualified. Read on its own it
makes a compactor emitting a long gap a nonconforming *writer* (conforming file,
nonconforming actor). The repair needed to except the compactor tier there and
did not.

Third-order: §21.7 (line 3717-3721) accounts for the compactor obligations that
have no witness — "§20.5's four obligations on a compacted file's trailer
(`[R-WRT-06]`) ... are unwitnessed for a reason all four share: the output carries
no record that it is a compaction output at all". After the repair, a long
pre-trailer gap has exactly that property for a *different* rule: a verifier
meeting one cannot tell whether the producer was a compactor (permitted) or a
committer (a §2.3 conduct violation). Before the repair a long gap always meant a
conduct violation. §21.7 names rules by identifier, so it did not move.

=> FINDING B-06.

Query `durab|fdatasync|torn` [20 hits]: 58, 60, 1174(×2), 1180, 1183, 1194(×2),
1214, 1248, 1269, 1283, 1317, 1457, 2332, 2929, 3238, 3239, 4206.

**Repair's own justification, line 3235-3239:** "A compaction leaves its input
intact and writes bytes that are **not readable as a TARN file until the trailer
completing them is present**, so there is no committed prefix for a barrier to
protect and **a torn output is an unreadable file rather than a damaged one**."

The premise holds only if the trailer is written last — which is exactly the
ordering the sentence before it declares not owed. Nothing else fixes write order:
§6.2 fixes the trailer's *position* (final 64 bytes), not when it is written;
`[R-LIF-04]` (line 1246-1258) is scoped to "A writer beginning a commit against an
existing file" and does not reach a compactor writing a new file. A compactor that
writes the trailer and directory first and the tile payloads after, then crashes,
leaves a file that passes §6.2's trailer gates and the directory CRC and fails only
at each stored tile's CRC — reject-tile, §8's chain, line 1140-1143. That file is
readable and damaged, which is what the sentence says cannot happen.

=> FINDING B-07.

Checked the neighbouring Note at line 1193-1196 ("Where barriers are weaker than
assumed, safety degrades from 'torn commits are invisible' to 'torn commits are
detected': §8's chain still catches every inconsistent state loudly"). Consistent
with the damaged-file case being *detected*; it does not rescue the repair's
"unreadable rather than damaged". No separate finding.

Query `compactor|compaction` [55 hits]. Read every one. Others checked and clean:
- line 812 §6.3 (compactor carries ignore-lane bits) — consistent.
- line 3199-3202 §20.5 opening ("so slack is never carried"; "Given a conforming
  input the output is a conforming file") — a longer gap is still conforming, and
  "carried" is about the input's slack. No finding.
- line 3949-3952 `[R-PRV-02]` ("the input persists, unmodified, until something
  outside this specification deletes it") — the repair's "what discards it is
  outside this specification" restates this. Duplication, not contradiction.
- Appendix G items 2, 3, 8 (lines 4290-4295, 4330-4338, 4355-4365). Item 3 pins the
  pre-trailer pad to the forced 64-byte alignment for profile adopters, so item 8's
  "A compactor's output is therefore reproducible only modulo its trailer" survives
  the repair. Item 4's gloss "One generation, so that the file is the output of a
  single commit" now sits awkwardly against item 8's compactor-adopter language,
  but `[R-LIF-01]` already excluded compaction from "commit" before this repair, so
  the repair did not create it. Not reported.
- line 3331-3339 `[R-WRT-09]` Note (verification depth) — unaffected.

---

## 3. The seven checks, per hunk

### HUNK 1

**Rule the repair adopts.** For a layer storing tiles in the superseded generation,
a shrink is barred iff it alters, for such a tile, what §14 fixes for its stored
bytes or how they decode — and the main bar's carve-out is part of that test, so a
shrink whose only effect is to create padding positions whose stored bytes already
hold the fill is permitted, and unstoring/de-addressing neither rescues a barred
shrink nor is required to license a permitted one.

**1 TENSE AND QUANTIFIER — PASS.** The repair speaks about the superseded
generation ("a tile stored **there**", antecedent "the superseded generation's").
The normative rule it restates, line 2996-3001: "A commit MUST NOT change a layer's
declarations in a way that alters, for **any tile that layer stores in the
generation this commit supersedes**, what §14 fixes for its stored bytes or how
they decode". Repair: "a shrink that **alters what §14 fixes for a tile stored
there**". Same generation, same predicate; "a tile" existential against the bar's
"any tile" universal-under-negation — equivalent. The repair is a restatement, not
the normative rule; the normative rule is line 2996.

**2 CITATIONS — PASS (2 of 2).**
- `[R-SER-05]` (line 1961-1966): "Every padding position MUST encode ... that
  channel's fill ... Every pad bit (§14.3) MUST carry the plane's channel's fill
  bit." The repair says "the fill `[R-SER-05]` fixes". Resolves.
- §21.7 (line 3658ff): the repair claims it "records the consequence — that this is
  precisely where the bar has no witness, the live state being clean". §21.7 line
  3690: "§20.3 step 4's bar on a declaration change is witnessed only where the
  affected tiles remain stored"; and line 3712-3716: "a commit that supersedes
  every tile it would have damaged leaves the live state clean, so the bar is
  unwitnessed there". Resolves — via the first clause. See check 7 for the verb
  mismatch on the second.
- §11.2, §11.3, §14 appear in surrounding unchanged text; §11.2's grid count
  (line 1500-1502) and §11.3 padding read and consistent.

**3 NORMATIVE SITING — PASS.** The repair sits in §20.3's numbered step 4, ordinary
prose, no ">" prefix. `[R-WRT-04]` closes the step at line 3074. The only ">"-block
restatement of the shrink rule is §11.1's Rationale at line 1484-1490, and it is
now stale — B-02, which is the mirror-image signature (repair landed in normative
text, the non-normative restatement still says the old thing).

**4 NO CONTRADICTION IN THE SAME PASSAGE — FAIL.** Line 3053, three sentences
later, unchanged. B-01.

**5 EXHAUSTIVE CLAIMS.** Words flagged: "nothing else", "only those", "exactly as".
- "What counts as such an alteration is the bar above **and nothing else**" — tried
  to falsify. Searched for any other rule that makes an extent shrink a violation
  for a prior-generation stored tile: `[R-COD-07]`'s lz4 cap and `[R-ENC-04]`'s
  2⁶³−1 ceiling (both named in the growth paragraph, line 3026-3033) bound a
  *grown* geometry, not a shrunk one; `[R-SLB-01]`'s alignment invariant is
  re-tested at line 3068-3071 for the whole new state, and that sentence is
  separate from the bar and unchanged, so "nothing else" is scoped to *what counts
  as an alteration under the bar*, not to what else can make the commit illegal.
  Reads as sound. No finding.
- "a shrink producing **only those**" — the class is well-defined (new padding
  positions whose stored bytes already hold the fill). No finding.

**6 WHAT ELSE IN THIS STRUCTURE IS UNCONSTRAINED.** Structure governed: a layer's
geometry declaration as re-declared by a commit. Quantities it carries: rank d;
per-dimension name, extent Eᵢ, tile extent Tᵢ; channel count C; per-channel sample
type and fill; layout (interleaved/planar); codec; filter; index_encoding;
entry_count; crc_of_crc_array; declared alignment A / slab.
- Eᵢ: governed — growth paragraph (3020-3033) and shrink paragraph (3034-3057).
- Tᵢ, C, d, sample type, layout, codec, filter: governed by the main bar at 2996
  (each alters decoded size, sample offsets, or the codec/filter) plus the
  free-re-declaration licence at 3020 for an empty layer. Note the shrink and
  growth paragraphs both say "an extent", which §11.1 line 1471-1473 distinguishes
  from "a tile extent" — so Tᵢ is NOT covered by either paragraph, but it is
  covered by the main bar. Not a gap.
- entry_count / crc_of_crc_array / extent_length: governed by `[R-CNT-17]` and
  `[R-CNT-23]` as derived quantities. The repair's newly-permitted class leaves
  them unchanged — which is precisely what line 3053 gets wrong (B-01).
- fill: a change of a channel's recorded fill alters "the content `[R-SER-05]`
  fixes" at every padding position of a prior-generation stored tile, so the main
  bar reaches it. Covered.
No unconstrained sibling found beyond what B-01 already names.

**7 ANALOGY — PASS, with the verbs recorded.** The repair argues by analogy twice.
- "permitted **here exactly as it is there**". Repair's governing verb: a shrink
  "**producing** only those [new padding positions whose stored byte already holds
  the fill]". Cited rule's governing verb (line 3009-3012): "a change that
  **leaves** every one of those tiles' stored bytes **meaning exactly what they
  meant** ... is not what this bars". Different sets: the repair ranges over
  padding positions the shrink creates; the carve-out ranges over every stored byte
  of every prior-generation stored tile of the layer. Tested the entailment: a pure
  Eᵢ shrink changes ∏Tᵢ not at all, so decoded size, sample byte offsets, codec and
  filter are all untouched; the only §14-fixed quantity that moves is the padding
  set and its content, and the "only those" restriction makes each new member
  already correct. Entailment holds. The analogy carries one class only (padding
  positions), so there is no second member to test it against separately. PASS.
- "the same reason: the quantifier is the superseded generation's" — repair's verb
  "the layer **stores** in the generation this commit supersedes" against §3.1's
  definition of *stored* against a generation (cited at line 3003). Same set. PASS.
- The §21.7 citation is a near-analogy worth recording: repair says the bar has no
  witness because "the live state being clean"; §21.7's matching sentence says "a
  commit that **supersedes** every tile it would have damaged leaves the live state
  clean". The shrink paragraph's case is **de-addressing / unstoring**, not
  superseding. Different verbs over different sets. It still resolves, because
  §21.7's earlier and broader clause — "witnessed only where the affected tiles
  **remain stored**" — covers de-addressing too. Recorded as a pass; not reported.

### HUNK 2

**Rule the repair adopts.** A compactor is bound by none of `[R-LIF-02]`: it owes
no barrier before or after its trailer, owes no minimal pad, and may write its
output's bytes in any order; it SHOULD make the output durable before anything
discards the input.

**1 TENSE AND QUANTIFIER — PASS.** `[R-LIF-02]` line 1168: "A writer **performing a
commit** MUST, in order ...". The repair's "That protocol is stated for a commit"
matches word for word. `[R-LIF-01]` line 1162-1164: "every conforming mutation of a
file is either a commit (§9.2) or a whole-file rewrite under a new file_id
(compaction, §20)". The repair's "makes a compaction a whole-file rewrite under a
new file_id rather than a commit" matches. Ranges over "a compactor", the §20.1
tier (line 2907-2908). Correct set.

**2 CITATIONS — 5 pass, 1 fails.**
- `[R-LIF-02]` (line 1168-1181): steps 4 and 6 are the barriers, step 5 is "append
  the pad to the next 64-byte boundary ... and the new trailer". "barrier ordering
  nor its step 5 pad" resolves. PASS.
- `[R-LIF-01]` (line 1160-1164): quoted above. PASS.
- §20.2 (line 2921-2932) "binds a creator to that path by name": "A creator MUST
  follow `[R-LIF-02]`'s creation path ... (`[R-LIF-02]` steps 4-6 — both barriers,
  not one)". PASS, verbatim support.
- §20.3 step 6 (line 3072-3074) "binds an appender": "**Commit** (`[R-LIF-02]`
  steps 4-6): barrier; pad; trailer ...; barrier." PASS.
- §6.2 (line 737-738, 754-760) "requires the trailer to occupy the file's final 64
  bytes and bounds the gap ahead of it only through step 5": both halves verbatim
  supported. PASS.
- §2.3 "one of the writer obligations §2.3 names as no file-conformance violation"
  (line 148-157): §2.3 does name exactly this case, so the pointer lands — but what
  §2.3 says about it ("binds the actor in the same way") is the opposite of what
  the repair uses it for. FAIL. B-06.
- `[R-WRT-05]`, `[R-WRT-09]`, `[R-CNT-08]`, `[R-CNT-26]`, `[R-LIF-03]`, §9.3, §6.3,
  §18.3, §10.1, §10.2, §21.6, §7.2 all appear in the hunk's *context* lines, not in
  the repaired text; not re-audited under this charter.

**3 NORMATIVE SITING — PASS.** The new paragraph is ordinary prose inside §20.5,
within the span closed by `[R-WRT-06]` at line 3263. Not a ">" block. Searched for
a competing normative statement that still binds a compactor to the protocol: the
only candidates are §20.2 (creator, by name — §20.1 line 2907 makes creator and
compactor distinct tiers) and Appendix H's checklist (line 4431), which is
explicitly non-normative. So the repair lands; but Appendix H still says the old
thing to any reader who consults it — B-04.

**4 NO CONTRADICTION IN THE SAME PASSAGE — FAIL.** The paragraph's own second half
contradicts its first: no ordering is owed, yet the justification assumes the
trailer arrives last. B-07.

**5 EXHAUSTIVE CLAIMS.** Flagged: "fixed by nothing", "Two consequences follow",
"no barrier ordering is owed", "rather than", "outside this specification".
- "**fixed by nothing**" — falsified by `[R-CNT-09]` (SHOULD bound on
  dir_length + pad + 64), `[R-CNT-03]` (SHOULD-zeroed content), `[R-CNT-05]` (MUST:
  no structure in it), `[R-CNT-01]`/§6.2 (F mod 64 = 0 fixes the gap length modulo
  64). B-05.
- "**Two consequences follow and are intended**" — a count of two over the
  consequences of not being bound by `[R-LIF-02]`. A third follows and is not
  named: step 5 also fixes *generation* ("generation one greater than the prior
  trailer's") and *committed_file_length*. Both are separately pinned in §20.5
  ("and generation 1") and by `[R-CNT-01]`, so the count is defensible. No finding.
- "**a torn output is an unreadable file rather than a damaged one**" — falsified.
  B-07.
- "what discards it is **outside this specification**" — consistent with
  `[R-PRV-02]` line 3950-3953. PASS.

**6 WHAT ELSE IN THIS STRUCTURE IS UNCONSTRAINED.** Structure governed: the tail of
a compaction output — everything after the directory's CRC — plus the act of
writing the output. Every quantity it carries:
1. gap **length** — repair: nothing. Actually: `[R-CNT-09]` SHOULD, `[R-CNT-01]`
   F mod 64 = 0. B-05.
2. gap **content** — repair: silent, and swept up by "fixed by nothing". Actually:
   `[R-CNT-03]`'s SHOULD-zeroing binds a compactor as a writer; §6.2 says content is
   otherwise unconstrained. Folded into B-05.
3. gap **occupancy** — `[R-CNT-05]`'s MUST (no structure), row F7. Repair does not
   except it and could not; folded into B-05.
4. **write order** — repair: nothing owed. Genuinely nothing else fixes it
   (`[R-LIF-04]` is commit-scoped, line 1246). This is the real gap, and B-07 is
   its consequence.
5. **durability** — repair: new SHOULD. Nothing else.
6. **physical length vs committed_file_length** — `[R-LIF-04]`'s truncation rule is
   commit-scoped and does not reach a compactor; `[R-CNT-01]`'s "The file size of a
   conforming file equals ... F" covers it as a file predicate. Covered, no gap.
7. trailer fields: generation (pinned, "and generation 1"); file_id (pinned, fresh
   draw); flags ignore lane (pinned, `[R-CNT-08]`); flags incompat lane and
   version_major (§6.2/§6.3 field table); version_minor (SHOULD ≥ input's, else
   `[R-CNT-26]`); reserved bytes (§6.2 table: zero); trailer CRC (§6.2 table).
   All covered.
So the one quantity the repair frees and nothing else catches is write order, and
the repair's own justification for freeing it is the thing that is false.

**7 ANALOGY.** The repair argues by analogy once, and by contrast twice.
- "**exactly as** it is there" does not appear in hunk 2. The analogy is
  "**where** §20.2 binds a creator to that path by name **and** §20.3 step 6 binds
  an appender, **this section deliberately does not**." Verbs side by side:
  §20.2 "A creator **MUST follow** `[R-LIF-02]`'s creation path"; §20.3 step 6
  "**Commit** (`[R-LIF-02]` steps 4-6): barrier; pad; trailer ...; barrier";
  repair "this section **deliberately does not**". Sets: creator tier, appender
  tier, compactor tier — three disjoint tiers per §20.1 line 2902-2909. The
  argument from silence is sound because §20.1 makes the tiers disjoint and §20.2's
  and §20.3's bindings are by tier name. PASS. Recorded.
- "one of the writer obligations §2.3 names" carries the analogy for a single
  quantity (the gap), so there is no second member to test — but the two governing
  verbs do not match: repair "**is conforming** ... [and nothing binds the
  compactor]" against §2.3 "**binds the actor** in the same way". FAIL, B-06.
- "the mirror of the overstatement `[R-CNT-26]` names" is in unchanged context
  text, not the repair. Not audited.

---

## 4. Reverse check — does any repaired sentence duplicate or contradict something
   that already existed?

- "two conforming compactors given one input MAY emit outputs of different lengths"
  duplicates §2.3 `[R-CNF-05]` line 181-183: "this specification does not promise
  canonical bytes, and two conforming writers given identical input MAY produce
  different conforming files." Harmless restatement, no contradiction. Not reported.
- "A compactor SHOULD make its output durable before anything discards the input;
  what discards it is outside this specification" restates `[R-PRV-02]` line
  3950-3953 from the durability side. Consistent.
- Hunk 1's "this sentence answers the rescue question rather than restating the
  test" is self-describing and adds no rule. It does not duplicate anything.
- Hunk 1's "What counts as such an alteration is the bar above and nothing else"
  restates line 3007-3012's "The test is the effect on such a tile, and the list
  names where that effect arises rather than standing on its own". Consistent.

## 5. Checks that passed with nothing to report

Hunk 1: checks 1, 2, 3, 5, 6, 7 pass; check 4 fails (B-01).
Hunk 2: checks 1, 3 pass; check 2 fails on one of six citations (B-06); check 4
fails (B-07); check 5 fails on one of four flagged claims (B-05); check 6 finds
the write-order gap (folded into B-07); check 7 fails on the §2.3 comparison (B-06).
Downstream sweep produces B-02, B-03, B-04 in addition.

## 6. Byte-level determinations

- B-01 **YES**. Implementation A reads line 3053 as universal and, on a
  grid-count-preserving fill-holding shrink, re-emits the layer's whole tile-index
  region at a new placement and re-points the extent slot; implementation B reads
  §20.3's "A layer whose record alone changes keeps its extent slot, pointing at
  the existing region" and re-emits only the directory. A's file contains a second
  index region for that layer plus the old one as slack; B's does not. Both files
  are conforming — nothing in either records which operation produced it — so
  `[R-CNF-05]` does not close the fork, and only one reading permits an actor to
  produce A's bytes. The set moves.
- B-02 no. Non-normative ">" block per `[R-CNF-01]`; it cannot bar a writer, so the
  emittable set is the same under both readings.
- B-03 no. A count in explanatory position; the MUST NOT that follows is quantified
  over "any commit" independently.
- B-04 no. Appendix H disclaims its own authority.
- B-05 no. `[R-CNT-09]` and `[R-CNT-03]` are SHOULDs, so a file violating them is
  conforming under both readings; `[R-CNT-05]` and F mod 64 = 0 are MUSTs that
  `[R-CNF-05]` enforces on every conforming writer under both readings. The
  emittable set does not move; what moves is only how the paragraph reads.
- B-06 no. The disputed verdict is about the *actor* (conforming writer or not),
  not about bytes: a long-gap file is conforming under both readings.
- B-07 no. For a completed output the bytes are identical either way; the fork
  appears only in crash residue, whose accept/reject verdict is determined by its
  own bytes and on which no two readers disagree.
