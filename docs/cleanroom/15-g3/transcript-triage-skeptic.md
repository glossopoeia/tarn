# Round 15 triage — skeptic pass

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` in full (all 4227
  lines, in five reads plus targeted greps for Appendix G and the §11.x/§20.x
  passages).
- `round15/transcript-adversary.md`, lines ~405–500 only, to recover the
  truncated tail of adversary-01 (the input cut off mid-sentence at "§17.2's
  Note states this outcome in term"). I needed the finding's Reading B and its
  own byte-level rationale to judge it.
- I opened no `transcript-triage-*.md` and did not list the round15 directory
  for them (I listed the directory once, at the start, before reading the
  instruction not to — the listing showed the six walk transcripts, three quiz
  transcripts, and some build scripts; no triage file was present in it, and I
  opened none).

Nothing else. No `docs/`, no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no
`registry.json`, no git history, no web.

## Grouping

23 groups over 38 ids. The merges that took judgement:

- **diagrams-07 + register-04** — both are R4-versus-§21.4 on the same
  `[R-COD-06]` frame constraints. register-04 is the wider statement (R4 is five
  rows collapsed into one) and diagrams-07 the narrower (R4's skippable-frame
  instance under-enumerates against T18's four). Same defect seen at two
  granularities; the repair is one maintainer decision about R4.
- **reader-05 + adversary-05** — identical: §20.3 step 4's "the one such bound
  in format major 1" against `[R-ENC-04]`'s overflow bounds. adversary-05 supplies
  the worked construction (E → 2⁶², index region length ≈ 2·2⁶⁶).
- **reader-06 + quiz-02** — both are "`[R-WRT-07]`'s regeneration enumeration has
  no case for a structurally malformed non-sentinel entry, and the answer takes
  four hops to derive".
- **verifier-04 + register-03 + reader-03** — all three attack the same
  appositive in §21.7 ¶2, "— the §21.4 rows then fire —", with three different
  counterexamples (channel permutation, filter 1→2 on a padding-free numeric
  layer, channel-order swap with equal fills). One defect.
- **adversary-06 kept separate from that group.** It attacks a *different*
  sentence of §21.7 ¶2 ("the ordinal mappings … are satisfied by a structurally
  valid tile whatever values it carries") and in the opposite direction — that
  §21.7 claims *no* witness where one exists, rather than claiming a witness
  where none does. Merging them would hide that the paragraph is wrong twice, in
  two directions.
- **writer-03 + diagrams-05 + quiz-01** — the extent-shrink question. adversary's
  §5 ("What I could not determine") names it too, but the filed id adversary-07
  is the F23/L12 magnitude criterion, so adversary-07 is grouped by its own
  claim.
- **diagrams-02 + register-02 + reader-02 + quiz-03** — §21.1's closing
  parenthesis citing `[R-SER-08]` for "serve the structure unchanged". Four
  reporters, one clause.

## The ones I tried hardest to kill

### adversary-01 (P·Q overflow in a zero-extent layer) — killed

This was the strongest byte-level candidate on the sheet: the reporter built a
192-byte file, checked it on every other axis, and argues the only text settling
whether `[R-ENC-04]` reaches P·Q in a layer with no addressed tiles is a **Note**
that §2.1 strips of force. If that were so, two verifiers genuinely fork on
accept/reject over a concrete file. Four pieces of normative text decide it:

1. `[R-SER-07]`: "decoded size is a function of the layer's declarations
   alone — geometry, layout, and channel types — never of payload content …
   Every decoded size, and the value count V, is a declaration-derived quantity
   under `[R-ENC-04]`." A zero-extent layer declares geometry, layout and channel
   types, so its decoded size is defined. Reading B ("no tile, hence no decoded
   size") contradicts this sentence directly.
2. `[R-SER-02]`: "These products and sums are declaration-derived quantities
   under `[R-ENC-04]`" — unqualified by the existence of a tile.
3. L2 registers "P·Q (which dominates V = P·C); P·Bᶜ" with detector *reader* at
   *layer access*, and `[R-CNF-04]` binds: "A reader MUST detect every violation
   the error register (§21) assigns to the reader as its detector." Reading B
   makes a reader nonconforming. The reporter's §19.3 argument (the layer-access
   checklist does not cite `[R-SER-02]`) is foreclosed by §19's own preamble:
   "Those enumerations are not the complete inventory of what a reader detects at
   that tier: §21's register is … A row this section does not restate is due at
   its own tier all the same."
4. §20.3 step 4, normative text in `[R-WRT-04]`: the lz4 cap "which an empty
   layer escapes **only because** that cap is quantified over addressed tiles."
   That sentence makes the quantifier the reason for the escape, which is exactly
   the contrast §17.2's Note draws — so the contrast is not Note-only.

Verdict REFUTED. The file is nonconforming at L2, reject-layer, and every
conforming reader must say so.

### writer-03 / diagrams-05 / quiz-01 (extent shrink) — survived

I tried four routes to kill it and failed.

*Route 1 — the bar's own purpose.* §20.3 step 4 says "Where a change does reach
them it makes each stored tile it reaches nonconforming". A shrink that
de-addresses whole tiles makes no *surviving* stored tile nonconforming, so on
that gloss the change does not "reach" any tile and is permitted. Good argument;
not decisive, because the operative sentence is the MUST NOT and its test is
"alters … what §14 fixes for **its stored bytes** or how they decode", and going
from "§14 fixes decoded size 80 and padding set X" to "§14 fixes nothing, these
are slack" is an alteration on a plain reading.

*Route 2 — §11.1's Rationale.* "a shrink is barred wherever it alters what §14
fixes for a tile the layer already stores (§20.3, which states the tense
normatively and governs), which is the ordinary case". §2.1 gives Rationale text
no force, and this one defers back to §20.3, which never says "shrink". Worse,
the Rationale's carve-out has plenty of work to do without touching the disputed
case: a shrink from E=8 to E=7 with T=4 turns x=7 into a padding position, which
is barred iff the edge tile is *stored* — so "which is the ordinary case" is fully
explained by that reading and settles nothing about de-addressing.

*Route 3 — the step-4 enumeration.* "entries new to this generation (added tiles,
grown extents)" names only growth among geometry changes; "(a geometry change
renumbers ordinals wherever `[R-GEO-06]` moves them)" acknowledges geometry
changes generally. These pull opposite ways and neither decides.

*Route 4 — reachability of the disputed bytes.* This is where it turns
byte-level. Under reading (A) no conforming writer may emit the one-commit shrink
output. Can any *other* conforming actor emit those exact bytes? A creator
cannot: `[R-LIF-02]`'s creation path writes generation 1, and the disputed file's
live trailer carries generation 2. A compactor cannot: `[R-WRT-06]` fixes its
output at generation 1 with a fresh file_id. Any appender reaching those bytes
must append exactly index₂ + dir₂ + pad + tr₂ over the prior generation-1
prefix — which *is* the disputed commit. Two commits (unstore, then shrink) reach
the same live state but a different byte sequence, at generation 3. So the
disputed byte sequence is emittable under (B) and by nobody under (A).

That is the distinction last round's calibration asked to be made explicitly,
and it separates this finding from reader-01 below, where the disputed output
*is* creator-emittable. The second half of the byte-level test — "must accept or
reject" — is unaffected: the shrunk file is conforming as a pure predicate on
bytes (`[R-CNF-02]`) and every reader and verifier treats it identically. The
first half is not. I flag it byte-level and say so plainly.

Corroboration that the question is genuinely open rather than merely
under-read: four independent walkers hit it (writer, diagrams, quiz author, and
adversary's §5 "What I could not determine"), and the two who picked a side
picked opposite ones — writer-03 picked (A)/barred, diagrams-05 picked (i)+(b)
which is also barred, while the permissive reading is what the §11.1 Rationale's
"wherever" implies. The repair is one sentence in §20.3 step 4 beside the growth
permission.

### reader-01 (compactor: refuse vs drop) — real contradiction, not byte-level

`[R-WRT-06]` says the compactor "can neither drop the structure (§20.4,
`[R-WRT-07]`)". §20.4's MU = 0 / PE = 0 row says "A compactor may drop it whenever
it rewrites the file", and §20.5's *own opening sentence*, four sentences earlier,
says the output is the live committed state "less any record §20.4 lets it drop".
So the parenthetical cites §20.4 for a proposition §20.4 denies, and contradicts
its own paragraph. The case is reachable: a MU = 0 / PE = 0 record with a
reserved-range type (F36) or a set reserved flag bit (F26) — both verifier-detected,
so `[R-WRT-09]`'s obliged checks (the open, each retained layer's record and index
chain, each relocated extent's checksum) do not fail and the first MUST does not
fire.

Not byte-level, by the same emittability test that made the shrink byte-level: the
compacted output is generation 1 with a fresh file_id, flags = 0 (take an input with
no ignore-lane bits set), and only ordinary records — a **creator** can emit it
byte-identically. So the set of byte sequences a conforming implementation may emit
is unchanged; what changes is whether *this* tool refuses. It still needs a
maintainer's decision, because two normative sentences in one subsection give
opposite answers.

### verifier-01 (partial slack total omits the resource decline) — mostly killed

The reporter reads "whether because A … or because B …" as exhaustive, which would
make §5.2's MUST unsatisfiable. The lead clause is the operative condition and it
is general: "**Where the walk of §9.7 does not enumerate every region's
claimants** — whether because … or because … — the verifier MUST report the total
as partial." §9.7 has the same shape ("Where the walk does not complete —"), and
Appendix H restates it generally ("where its walk did not complete"). "Whether
because A or because B" is concessive, not definitional. Reading 2 is foreclosed;
what survives is that a third ground would read better named than inferred.

### adversary-04 (§21.7 ¶2 lacks ¶1's disclaimer) — mostly killed

Reading (ii) would make no file certifiable. `[R-CNF-11]` forecloses it twice on
its face: *cannot establish* is "the last where some requirement is one it is
unable to check **on a capability or resource ground**", and the verifier "MUST
report each requirement it was unable to check **on a capability or resource
ground**". Absence of a witness is neither. The asymmetry is a real editorial
wobble; the catastrophe is not reachable.

### diagrams-04 (Appendix G item 3 doesn't pin directory record order) — mostly killed

Item 3 does pin it, in a sentence the finding does not quote: "**Records** and a
layer record's sub-records **alike are ordered by type**; within a type, type
0x0001 ties by layer name, and every other type by the record's header with
extent_offset masked to zero, then its inline payload, then the contents of its
extent, compared lexicographically." That is a general ordering over records, not
one scoped to record extents. The closing paragraph confirms it ("record and
sub-record order, which `[R-CNT-14]` leaves free" is listed among what the items
add), and the reporter's own observation that the 0x0001 tie-break is otherwise
dead points the same way. What survives is that "in ascending record order" first
appears attached to extents, so the key's scope has to be assembled.

### register-05 (F27/L48 and "at every nesting depth") — mostly killed

Reading B (outermost object only) is available in F27 read alone but is
foreclosed the moment the twin rows are read together — L48 has no "top-level" at
all, so "top-level" in F27 must modify the *record*, not the object — and
§21.1's tiebreak plus `[R-MTA-05]`'s "at every nesting depth" decide the
predicate. The rows do under-state the rule, which is worth fixing.

## The ones where I searched and found nothing

For each of these I hunted for the foreclosing sentence and could not produce
one, and I record that the absence is the evidence:

- **§20.5's "anywhere §5.2 admits"** — no sentence in §20.5 qualifies the
  placement freedom by the layout invariants. What *does* decide the bytes is
  the preceding sentence, "Given a conforming input the output is a conforming
  file", plus `[R-CNF-05]` and `[R-WRT-01]`, so the emitted bytes do not fork —
  but §20.2's twin carries the qualifier and §20.5 does not. writer-01's second
  edge (that `[R-SLB-04]` lets a compactor clear a slab while `[R-WRT-07]`'s
  closed list forbids it) is *not* a contradiction: `[R-SLB-04]` states a
  disjunction, and `[R-WRT-05]`/`[R-WRT-07]` independently eliminate one
  disjunct, forcing the other. That is ordinary, not contradictory.
- **§21.2's preamble** — §21.1's tiebreak is scoped to rows and to §21.6's
  entries; the preamble is neither and cites no governing rule of its own, so
  nothing in the document adjudicates preamble-versus-row. Its ordering claim is
  simply wrong: §19.1 step 1 and `[R-CNT-04]` put the front-block equality check
  ahead of the trailer, `[R-CNT-24]` makes the front block constant across
  majors, and F6's own Condition cell says a verifier "holds no such exemption".
  register-01's F18 half *is* decided against it — §6.2's table reads "1 (0
  invalid; …)" and §21.6 says "version_major = 0, permanently invalid in every
  format major version", so 0 is not "another major" and the preamble's second
  sentence never reached F18. Not byte-level: `[R-CNT-07]` and `[R-CNT-04]` fix
  every reader's reject, and both candidate verifier verdicts bar certification
  (`[R-CNF-11]`).
- **§21.7 ¶2's "the §21.4 rows then fire"** — verified register-03's
  counterexample by hand: d=1, one float32 channel, E=T=256, so G=N=1, P=256,
  Q=4, decoded size 1024, codec 1, no padding (G·T = E), no bool. Filter 1→2:
  T1 passes (bytes unchanged), T3 passes (`[R-COD-10]`: "Length is unchanged"),
  T14 passes (1024 = 1024), T4/T5 vacuous, T2 vacuous, T26 needs a broken
  padding or bool byte and there are none. No row fires. §21.7 ¶1 already
  carries the qualification the appositive omits ("narrow this only where
  content is structurally constrained").
- **§21.7 ¶2's "the ordinal mappings … whatever values it carries"** — verified
  adversary-06's counterexample: E=5, T=4, one uint8 channel, fill 0x5A, G=2,
  the t=1 tile has ordinal 0 real and 1–3 padding, so a reversed in-tile order
  puts the stored sample at a padding position and T4 fires. Exactly the shape
  T26 already records for `[R-COD-10]`, and §21.7 gives that case an honest
  qualification in ¶1 while giving this one none.
- **§21.1's instance criterion at F23/L12** — "is not 1" is a *does not equal*
  over two magnitudes either of which can be the greater (0 = the encoding byte
  absent; ≥2 = extra bytes), and §21.1's carve-out is for "a byte pattern
  against a constant", where "greater names nothing". Here greater names
  something. Every comparable row (F17, L21, L22, L30, T3, T14, T22) enumerates
  both directions. I checked the rest of the register for a second instance of
  this and agree with the reporter that there is none. reader-06's audit claim
  ("every cell obeys §21.1's instance criterion as written") does not survive
  this one.
- **§4.2's "All file offsets, byte lengths … are `u64`"** — inline_length is
  `u32` (§7.2's table) and every name prefix is `u8` (§4.6, §7.4), and both are
  byte lengths on this document's own definitions. `[R-ENC-06]` and the layout
  tables decide the parse, so nothing forks; the sentence is just false. The
  reporter's second half — that `[R-ERR-05]` omits inline_length's real
  ceiling — is weaker: `[R-ERR-05]`'s 2⁶³−1 statement is *true* of a `u32` field,
  merely not tight, and `[R-ERR-05]` calls itself "a finding aid rather than an
  inventory".
- **§11.1's Rationale "disk ordinals renumber"** — `[R-GEO-06]`'s i = 0 term is
  t₀·∏_{j>0} Gⱼ, in which G₀ does not appear, so interleaved growth along the
  first-declared dimension moves no ordinal; at d = 1 that is every growth. The
  named case ("the first growth of a zero-extent layer") is worse than false, it
  is vacuous — there were no ordinals to renumber. §20.3 step 4 states it
  correctly and normatively ("wherever `[R-GEO-06]` moves them").

## Byte-level tally

One: the extent-shrink group. Everything else either has its bytes fixed by a
sentence I quote in the group, or moves only a report label, a returned value in
an already-nonconforming file, or the corpus's row and instance counts.
