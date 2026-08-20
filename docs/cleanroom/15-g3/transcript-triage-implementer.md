# Round 15 triage — implementer-consequence pass

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` in full-section
  chunks: §2.1, §2.3, §2.4, §2.5, §3.1, §3.2, §4.2, §4.6, §5.2, §6.1–§6.3,
  §7.2–§7.4, §9.7, §11.1–§11.4, §12.3, §14.1, §14.2, §14.5, §15.3, §15.4,
  §16 (all), §17.2, §17.3, §17.4, §18.2, §19.1, §19.2, §20 (all), §21 (all,
  including every register row), Appendix G, and the head of Appendix H.
- I opened **no** `transcript-*.md`, walk or triage. I never listed
  `round15/` for triage files; the one `ls` I ran was to confirm the
  directory existed and it printed the whole directory, including the six
  walk transcript filenames and the three quiz filenames. No
  `transcript-triage-*.md` appeared in that listing and I opened none.
- Every claim below is checked against the spec text, not the reporter's
  paraphrase. Where a reporter quoted selectively I say so.

## Method

For each finding I asked my lens question first: *name the wrong thing an
implementation does.* Then the byte-level test, with the round-14
refinement the brief supplies — when a fork is only about writer conduct,
ask whether the disputed byte sequence is emittable by **some other
conforming actor**. If it is, the set of conforming byte sequences and
every verdict on them is unchanged, and the fork is conduct. If it is not,
one reading removes a byte sequence from the emittable set entirely, and
that is byte-level.

That distinction does real work this round: it separates `reader-01`
(compactor drop) from the shrink group, which are otherwise the same shape.

---

## Group-by-group

### G1 `compactor-placement-license` — writer-01, diagrams-01

§20.5: "A compactor preserves content but not placement — placement is not
among the things it carries forward, and it is free to place structures
anywhere §5.2 admits". §5.2 constrains only the partition. §20.2, the
creation twin, carries the qualifier: "in any order satisfying §5.2's
coverage classes (`[R-CNT-02]`, `[R-CNT-03]`) and every declared layout
invariant (`[R-SLB-01]`, `[R-SLB-03]`)". Verified both verbatim. The
omission is real.

Implementer consequence: a compactor that repacks an A=4096 layer's tiles
contiguously from 16 emits a file a verifier rejects at L40. That is a
*wrong* implementation, not a *divergent* one — three sentences force the
aligned output, one of them four sentences earlier in the same subsection:
"Given a conforming input the output is a conforming file." Plus
`[R-CNF-05]` and `[R-WRT-01]`. No verifier's verdict is in doubt (L40 fires
either way) and no conforming compactor may emit the misaligned bytes.
Not byte-level. Editorial: give §20.5 §20.2's qualifier.

writer-01's second edge is right and worth recording: `[R-SLB-04]` offers a
writer that moves a slab run the alternative of clearing the declaration,
but `[R-WRT-05]` requires byte-identical re-emission of retained records and
`[R-WRT-07]`'s exception list does not include the layer record's S/A_slab
fields. So a compactor cannot clear; it must re-establish the slab
invariants at the new placement. That is determinate, not contradictory —
it just makes §20.5's sentence doubly wrong.

### G2 `commit-alignment-quantifier` — writer-02

§20.3 step 4: "an aligned layer's new tiles satisfy its invariant or the
declaration is cleared". `[R-SLB-01]`: "every stored tile's offset satisfies
offset mod A = 0". L40 is unquantified. Verified all three.

Reachable case: a commit that *newly declares* A on a layer with retained
stored tiles at arbitrary offsets. §20.3 step 4's declaration-change bar
does not reach it (A does not alter what §14 fixes or how bytes decode), so
the commit is otherwise legal, satisfies §20.3's sentence exactly as
written, and produces a layer any verifier rejects at L40. The summary is
narrower than the rule it cites in the same breath. Distinct from G1 —
different section, different actor, different rule.

Not byte-level: `[R-SLB-01]` and L40 fix the emitted file's verdict; no
conforming writer may emit the misaligned file under either reading.
Editorial: quantify over every stored tile, matching `[R-SLB-04]`'s
parallel half.

### G3 `extent-shrink-de-addressing` — writer-03, diagrams-05, quiz-01

**This is my byte-level call.** Reasoning at length because I disagree with
two of the three reporters' own gradings.

The text. §20.3 step 4 bars a declaration change that "alters, for any tile
that layer stores **in the generation this commit supersedes**, what §14
fixes for its stored bytes or how they decode", lists four loci, and says
"The test is the effect on such a tile, and the list names where that
effect arises rather than standing on its own". It then grants growth
expressly. The word *shrink* occurs once in the whole document, at line
1476, inside a §11.1 **Rationale**, which §2.1 gives no force.

I searched hard for deciding text, as instructed:
- §3.1's *stored* definition ("A tile is *stored in a generation* if and
  only if that generation's tile-index entry for it is not the sentinel")
  confirms the quantifier reaches a tile that later ceases to be addressed.
  It does not decide whether de-addressing is an *alteration*.
- The tense clause — "a commit does not escape this by unstoring in the
  same breath: superseding every tile of a layer and re-declaring it are
  one operation, and this bars it" — is the closest thing to deciding text,
  and it does not close the case. An unstored tile is still **addressed**:
  it has a sentinel entry, a decoded image (fill), a padding-position set
  and a decoded size. A de-addressed tile has none of these. The sentence
  reaches storage changes, not address-space changes.
- Step 4's own enumeration of the re-emitted index region names four
  categories — stored/superseded, become-unstored, "entries new to this
  generation (added tiles, grown extents)", and "every other entry
  byte-identical". A shrink produces a fifth: entries that cease to exist.
  The enumeration has no slot for it. That is affirmative evidence the
  drafters did not contemplate this case here.
- §11.1's Rationale answers it ("a shrink is barred wherever it alters what
  §14 fixes for a tile the layer already stores … which is the ordinary
  case") and then defers to §20.3, which never mentions shrinking. A
  Rationale that defers to normative text which is silent decides nothing.

So the question is open. Now the byte-level test.

Accept/reject: unchanged. The shrunk file is structurally clean —
entry_count matches the new N, `[R-CNT-17]` holds, every CRC verifies — and
§21.7 places the bar in the class with no single-file witness. Every reader
and verifier says the same thing about it under either reading.

Emit: **this is where it forks, and the forked bytes are emittable by no
other conforming actor.** The disputed artifact is a *generation-2* file
whose committed prefix is a specific conforming generation-1 file. Only an
appender produces generation ≥ 2: `[R-WRT-02]` fixes a creator at
generation 1 and `[R-WRT-06]` fixes a compactor at generation 1. Given that
prefix, the only legal generation-2 continuations are the ones §20.3 step 4
permits. So under reading (A) that byte sequence is producible by nothing
conforming; under (B) it is ordinary appender output. Contrast `reader-01`
below, where the disputed compaction output is a plain generation-1 file a
creator could emit byte-for-byte — which is exactly why that one is not
byte-level and this one is.

Downstream this is visible, not notional. Under (A) the caller must do a
whole-file rewrite under a fresh file_id (`[R-LIF-01]`, §20.5), so every
consumer sees a new file_id and generation 1 and every (file_id, range)
cache entry invalidates (`[R-LIF-03]`). Under (B) they see the same file_id
at generation 2 and keep every fetched range. Two teams shipping
`resize(layer, extents)` — one refusing when a stored tile would be
de-addressed, one appending — hand their users different trailers for the
same operation. Truncating a time series is not an exotic request.

CONFIRMED, byte-level. The repair is a maintainer decision, not an edit:
decide whether a shrink that de-addresses a tile stored in the superseded
generation is inside the bar, state it normatively in §20.3 step 4 beside
the growth permission, and add the removed-entry case to step 4's index
re-emission enumeration. My recommendation is that it be barred — it
strands a whole tile's payload as slack for what reads like a directory
edit, which is the harm the bar's own closing sentences name — but the
document has to say so.

### G4 `appendix-g-first-structure-at-16` — writer-04

Item 3: "The first structure begins at 16 … each later structure begins
where the previous one ended, save where alignment forces a gap". The
proviso is attached to the later-structures clause; item 5 licenses fixed
declared A/A_slab; under item 3's own order the first structure is the
alphabetically-first layer's first stored tile. If that layer declares
A ≥ 512, `[R-SLB-01]` forbids offset 16. Verified. Appendix G is
non-normative and "adds no requirement to any actor", and `[R-SLB-01]`
forces the aligned offset either way. Not byte-level; editorial.

### G5 `appendix-g-compactor-drop-discretion` — writer-05

Opening: the profile "closes the degrees of freedom this format
deliberately leaves open". Item 2 names compactors explicitly; item 4's one
generation is satisfied by a compaction output. §20.4: "A compactor may
drop it whenever it rewrites the file", and no numbered item pins it.
Verified. Two profile-conforming compactors therefore emit different record
sets, different dir_length, and — item 2 deriving file_id from the emitted
bytes — different file_ids. The completeness claim is false for that case.
Both outputs are conforming files (`[R-CNF-05]` already licenses two writers
to differ), so not byte-level; editorial. Concrete cost: a content-addressed
store that treats "compacted under the profile" as reproducible and finds
two digests for one input.

### G6 `partial-slack-total-grounds` — verifier-01

`[R-CNT-21]`'s and §9.7's grounds lists both name exactly two: scope-level
rejection, and an elective `[R-CNF-11]` stop. A `[R-ERR-04]` resource
decline of a layer is neither, and §5.2 says flatly "a verifier that
reaches a live state MUST report the total number of slack bytes".
Verified. The gap is real.

But the sentence is not exhaustive on its face: the governing clause is
"Where the walk of §9.7 does not enumerate every region's claimants … the
verifier MUST report the total as partial", with the "whether … or …" pair
inside em-dashes as gloss; and the following sentence — "a verifier
reporting one MUST say which scope or violation stopped the walk" — admits
naming a scope with no violation attached. So the general clause covers the
resource decline and the MUST stays satisfiable. Not byte-level (no
accept/reject moves; `[R-CNF-11]` fixes the verdict as *cannot establish*
either way). Editorial, with a real operational consequence worth the fix:
under the exhaustive reading a verifier reports a *complete* total inflated
by a declined layer's whole live payload, and §22.3 makes that number the
one an operator acts on.

### G7 `21.2-preamble-overreach` — verifier-02, register-01, adversary-03

The preamble claims no §21.2 row reaches a file declaring another major,
excepting only the trailer magic and trailer CRC. Verified against §19.1
step 1 ("MUST verify the front signature block by byte equality before
other processing"), F6's own Condition cell ("a verifier holds no such
exemption (§2.3)"), F1's front-block instance, F5's 128-byte floor, and
§6.3 `[R-CNT-24]` making the front block constant across majors. Also
register-01's sharpest point, which the other two under-weight: F18 is
version_major = 0, which §6.3 and §21.6 both call *invalid*, not another
major — so the preamble's presupposition excludes the row §21.6 explicitly
points back to.

The fork is verifier-verdict labelling: *nonconforming* (F6 established)
versus *cannot establish* (capability). `[R-CNF-11]` decides it — "An
established violation takes priority: a verifier that has established any
violation reports *nonconforming*, however many requirements it was unable
to check, and *cannot establish* is available only to a traversal that
established no violation." Both verdicts bar certification. Readers reject
under `[R-CNT-04]`/`[R-CNT-07]` either way. Not byte-level. Editorial:
narrow the preamble to the checks §6.3 `[R-CNT-24]` fixes across all majors,
and say version_major = 0 is not such a declaration.

### G8 `geo01-parenthetical-at-extent-zero` — verifier-03, diagrams-03, adversary-02

"A tile extent MAY exceed its dimension's extent (the grid is then a single
padded tile along that axis)." Not labelled Note/Example/Rationale, so §2.1
makes it normative. Its antecedent holds at every Eᵢ = 0 (Tᵢ ≥ 1 is
required by the same requirement) and its consequent is false there, per
the next paragraph and §11.2's formula. Verified all three. A false
normative sentence.

Not byte-level: `[R-GEO-02]` ("its grid count is 0, the layer has zero
addressed tiles, its tile index has zero entries") and `[R-GEO-03]`'s
formula are what an implementation computes from, and they are adjacent,
explicit, and restated in §21.6, §17.2's Note and §15.4. Editorial: guard
the parenthetical to 0 < Eᵢ < Tᵢ, or move it to the Rationale.

### G9 `21.7-step4-rows-fire` — verifier-04, register-03, reader-03

§21.7 ¶2: "§20.3 step 4's bar … is witnessed only where the affected tiles
remain stored — the §21.4 rows then fire". I ran both counterexamples
against every §21.4 row myself.

register-03's filter change: interleaved, rank 1, one float32, E = T = 256,
G = N = 1, P = 256, Q = 4, decoded size 1024, G·T = E so no padding, no
bool, codec 1 filter 1, one tile stored. Change filter to 2. `[R-COD-10]`
says "Length is unchanged", so T3 and T14 stay silent at 1024; T4/T5 have
no padding position or pad bit; T2 has no bool channel; T24/T25 are codec-1
vacuous; T26 needs a wrong *stride* breaking a structural constraint and
there is none. No row fires. The bar is violated ("the codec and filter
that produced the stored bytes") and the escape does not apply — the
mandated interleaved stride is Q = 4 and a stride-4 shuffle on 1024 bytes
is not the identity.

reader-03/verifier-04's channel permutation: two uint8 channels with equal
fills, swapped. Q = 2 either way; F⁰,F¹ swap. Note the bar's list says "the
byte offset of any **sample**", and a sample's offset (u·Q) does not move —
only each *value*'s does — so even the list is not hit; the general test is,
via "or how they decode". Again no §21.4 row fires.

So the em-dash clause over-claims. CONFIRMED. Not byte-level: the
counterexample file is conforming under `[R-CNF-02]` and every
implementation returns the same verdict on it under either reading. The
cost is a verifier author who believes running §21.4 discharges step 4, and
a corpus builder who tries to construct a vector that cannot exist.
Editorial: carry §21.7 ¶1's own qualification down — the rows fire only
where the change reaches a structurally constrained byte, exactly as
`[R-COD-10]` states for its own case.

### G10 `21.1-serve-unchanged` — diagrams-02, register-02, reader-02, quiz-03

§21.1's closing clause: "for several such rows it obliges the reader to
serve the structure unchanged (`[R-SER-08]`, `[R-CNT-22]`, and
`[R-MTA-05]` …)". Wrong twice for `[R-SER-08]`. Not *unchanged*: §14.2
requires "0x00 as false and every other byte as true", and §12.3
`[R-TYP-04]` calls it "the one case where a reader resolves a byte to a
value rather than passing it through". Not *obliged to serve*: `[R-SER-08]`
is conditioned on "A reader that neither detects the violation nor rejects
the tile", and `[R-CNF-12]` licenses rejection. Accurate for `[R-CNT-22]`
and `[R-MTA-05]`. Verified.

Implementer consequence is concrete: a reader built from the summary
returns raw 0x7F for a malformed interleaved bool, or believes it may not
exercise `[R-CNF-12]`. But the divergence is a returned sample value in a
file §14.2 says "never arises in a conforming file", not a byte on disk or
an accept/reject verdict, and §21.1 defers in the same sentence — "the
governing rule states what a reader does" — while §14.2 states it
explicitly. Not byte-level. Editorial: drop `[R-SER-08]` from the list, or
restate the clause as "does not oblige the reader to refuse the structure".

I note for the record what register-02 flags honestly: §14.2's Rationale
says a returned-value fork is "the divergence this document exists to
prevent". That is an argument for fixing it promptly, not for calling the
byte-level test met — §14.2 already prevents the fork; §21.1's summary is
merely a wrong report of it.

### G11 `appendix-g-directory-record-order` — diagrams-04

Item 3 defines a total order over records and applies it to "any record
extents in ascending record order"; it never says the directory emits its
record sequence in that order, while the closing paragraph claims the items
add "record and sub-record order, which `[R-CNT-14]` leaves free".
Verified. Two supporting details the reporter is right about: the
type-0x0001 layer-name tie-break is dead unless the key orders the
directory (a layer record's extent is placed in the earlier per-layer
stage), and "otherwise free to vary" has no antecedent otherwise. Against
that, "emitting them in either order yields the same file" reads as being
about directory emission, so reading (A) is intended. Non-normative, both
readings conforming; not byte-level. Editorial: say it in terms.

### G12 `L40-L42-structural-entry-transparency` — diagrams-06

L41's cell carries the carve-out; L40 and L42 use a bare "a stored tile".
§15.3: "Such an entry contributes no stored extent to the *verifier* rows,
which bind over well-formed entries' extents only" — and §15.3's own
verifier rows include "alignment or slab invariant violated (§16)".
Verified. §21.1's "where a row and the rule it cites diverge, the rule
governs" settles the verdict, so nothing is open; the table is wrong.
Register-bookkeeping: carry L41's parenthetical into L40 and L42, or state
the transparency once in §21.3's preamble. (The reader walk reached the
same conclusion independently and filed it as not-a-defect; the row cells
are still worth fixing.)

### G13 `zstd-frame-rows-granularity` — diagrams-07, register-04

Same defect from two distances. R4 gives 12 instances (6 constraints × 2
containers) and folds all skippable-frame placements into one; T18 gives 4,
enumerating three placements plus a second frame; T17/T19/T20 split what R4
bundles. Both police `[R-COD-06]`, whose text I checked: "a payload … that
contains a skippable frame **anywhere** or more than one frame". §18.2
carries it over as "no skippable frame and no second frame". R4's governing
rule is `[R-MTA-09]` citing `[R-COD-06]`, so the row inherits the "anywhere"
text while its cell is written to §18.2's wording.

§21.1's criteria do not settle it: "each row is one malformed condition"
pushes toward splitting R4 into five, "the count is therefore mechanical
once the cell is written" makes writing the cell the free step, and
"materially different shapes" is exactly the phrase that bought T18 its
three placements. Not byte-level — the same predicates are checked by the
same actor at the same tier with the same ignore-record outcome, so a file
with a skippable frame in any position is caught identically. What moves is
§21.8's 273 (to 277 under T18's reading, 271 under R4's, further under
register-04's row-split reading) and, through `[R-ERR-02]`/`[R-VEC-03]`, the
corpus. Register-bookkeeping, and it needs a maintainer decision:
`[R-COD-06]` is the governing constraint in both places, so I would fix R4
to T18's enumeration and restate 277.

### G14 `F27-L48-nesting-depth` — register-05

`[R-MTA-05]` verified at line 2517: "Writers MUST serialize object members,
**at every nesting depth**, in ascending order of their keys' UTF-8 bytes."
F27 and L48 both drop the depth clause, and F27's "top-level" — which L48
does not need, since "top-level" there distinguishes the *record*, not the
object — makes the narrow reading available in the row read alone.
Verified. §21.1's rule-governs tiebreak applies squarely (these are rows),
so the verifier's finding is not open. Register-bookkeeping: restore "at
every nesting depth" to both cells. Cost if unfixed: a verifier that checks
only the outermost object certifies a nonconforming file, and a corpus
vector records the wrong expectation.

### G15 `4.2-u64-overgeneralization` — register-06

§4.2: "All file offsets, byte lengths, dimension extents, and tile extents
are `u64`." §7.2's header table: "| 4 | 4 | u32 | inline_length |
structural |". §4.6: "at most 255 bytes of UTF-8 (so every name's length
prefix is a single byte)". Both verified; both are byte lengths. The
universal is false twice.

Not byte-level: `[R-ENC-06]` — "No field's width is ever a writer choice:
every field's width is fixed by this specification" — plus the layout
tables mean no implementation parses inline_length at eight bytes. I could
not construct one either. Editorial: narrow §4.2's sentence to the fields
it holds for, or qualify it as yielding to a layout table.

The reporter's second half — that `[R-ERR-05]` omits inline_length's
2³²−1 ceiling — is answered by §21.9's own text: "The hard limits it
restates are a finding aid rather than an inventory." So that half is not a
defect, and I say so rather than carrying it as one.

### G16 `compactor-drop-vs-refuse` — reader-01

The only finding whose author graded it byte-level, and the one where the
emittable-by-another-actor test earns its keep.

Verified: §20.5's opening — "less any record §20.4 lets it drop"; §20.5's
`[R-WRT-06]` — "MUST NOT emit a file carrying a violation it has detected:
it can neither drop the structure (§20.4, `[R-WRT-07]`), nor re-emit it
corrected"; §20.4's MU=0/PE=0 row — "A compactor may drop it whenever it
rewrites the file." Three statements in two adjacent subsections, two of
which say drop is available and one of which says it is not, the dissenting
one citing the section that grants it. A flat contradiction, and the
reachable case (a reserved-range type value, F36, MU = 0, PE = 0, detected
by a compactor built into a verifying tool) is ordinary.

Consequence: implementation A refuses to compact a healthy file forever
because of one ancillary record's type value; implementation B drops the
record and emits a clean file. Real and annoying.

Not byte-level. B's output is a generation-1 file with a fresh file_id and
no history obligation — a conforming creator given the same layers and
records emits it byte-for-byte (placement is free under `[R-SLB-05]`,
file_id is any nonzero value, and a flags = 0 input removes the only
wrinkle). So under both readings those bytes are conforming and emittable;
what forks is one tool's licence, and nothing about any file. That is
precisely the distinction that separates this from G3.

Severity design-decision: the maintainer should affirm that dropping cures,
and narrow the parenthetical to structures §20.4 does not let a compactor
drop.

### G17 `ordinal-renumber-rationale` — reader-04

`[R-GEO-06]` verified: "s = Σᵢ tᵢ · ∏_{j>i} Gⱼ". The i = 0 term is
t₀·∏_{j>0}Gⱼ, so G₀ appears in no product and raising it moves no spatial
ordinal. For d = 1 the empty product is 1 and s = t₀, so growth never
renumbers. §11.1's Rationale says growth that raises a grid count makes
"disk ordinals renumber … the first growth of a zero-extent layer
included", which is false for interleaved growth along the first-declared
dimension, false for every rank-1 interleaved growth, and vacuous for the
zero-extent case it names — a layer with any Eᵢ = 0 has N = 0 and no
existing ordinals to renumber at all. It is correct for planar layers
(c·N + s moves with N) and for interleaved growth along any later axis.

Not byte-level: Rationale text (§2.1), §20.3 step 4 states it correctly and
normatively ("a geometry change renumbers ordinals wherever `[R-GEO-06]`
moves them"), and the whole index region is re-emitted regardless.
Editorial.

### G18 `grow-bounds-exhaustiveness` — reader-05, adversary-05

§20.3 step 4: growth is permitted "provided the grown geometry stays within
every bound the layer's own declarations impose, `[R-COD-07]`'s lz4
decoded-size cap being the one such bound in format major 1 (L44)".
Verified. But L2's Instances cell registers by name "N = ∏⌈Eᵢ/Tᵢ⌉; … N·P;
C·N …; entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4", every one of which rises
with an extent, and §11.2 says "These products, like all geometry
arithmetic, are subject to `[R-ENC-04]`". adversary-05's construction
(d = 1, T = 1, C = 1, E → 2⁶², codec 1) breaches the index-region length
bound with the lz4 cap not in play at all.

Two readings of "bounds the layer's own declarations impose":
declaration-*conditional* bounds (true, and the lz4 cap is the only one) or
any bound the declared values are measured against (false). Not byte-level:
`[R-ENC-04]` binds independently and L2 fires on the emitted bytes either
way, so no two verifiers disagree. Editorial, with a real cost — an
appender that reads the sentence as its pre-flight checklist skips the
overflow checks, and since `[R-LIF-01]` freezes the committed prefix, the
wasted commit cannot be undone in place.

### G19 `compactor-malformed-index-entry` — reader-06, quiz-02

`[R-WRT-07]`'s regeneration recipe — "entry offsets new; entry lengths,
entry crcs, and sentinel entries unchanged; segment CRCs recomputed" — has
no case for a non-sentinel entry §15.3 classifies reject-tile on a
structural ground (length 0, offset < 16, one half sentinel, extent past
F − 64). Such an entry is not a sentinel and has no relocatable extent.
Verified, and the state is provided for on the append path — §20.3 step 2:
"a malformed index entry an appender meets while re-emitting a region is
carried forward byte-identically at its disk-ordinal position under step 4,
**not repaired to a sentinel**" — so a compactor's input can certainly hold
one.

The answer is derivable: writing a sentinel is repair, foreclosed by
`[R-CNF-04]`; copying the 20 bytes emits a file carrying a violation the
compactor necessarily detected (it must read every entry's offset and
length to relocate), which §20.5 bars and `[R-CNF-05]` bars again; so it
refuses. Not byte-level — the copy-verbatim output is nonconforming under
both readings, so no conforming implementation may emit it. Editorial: give
§20.5 the sentence §20.3 step 2 already has. Both reporters filed this as
an observation and both were right to.

### G20 `empty-layer-decoded-size-overflow` — adversary-01

The one finding I grade REFUTED, and the finding text itself is truncated
mid-sentence at the point where reading B would have appeared.

The construction is sound as arithmetic — E = 0, T = 2⁶², one float64
channel, P·Q = 2⁶⁵ — and the file is clean on every other axis. But the
document decides the question the reporter frames as open, and the reporter
quotes the deciding passage. §17.2's Note is labelled *Note* and so carries
no force under §2.1, but the normative chain behind it is complete without
it: `[R-ENC-04]` is unquantified ("any quantity this specification defines
as a sum or product of integers obtained from a file"); `[R-SER-02]` closes
"These products and sums are declaration-derived quantities under
`[R-ENC-04]`"; `[R-SER-07]` makes decoded size "a function of the layer's
declarations alone … never of payload content"; and L2's Instances cell
names "P·Q (which dominates V = P·C); P·Bᶜ" at detection point *layer
access* with no addressed-tile qualifier. So the check applies, the layer is
reject-layer at L2, and the built file is nonconforming. One reading, no
fork, no repair owed.

### G21 `21.7-second-class-disclaimer` — adversary-04

The asymmetry is real: ¶1 ends "None of these is a requirement a verifier
is *unable to check* within the meaning of `[R-CNF-11]`" and ¶2 has no
counterpart. Verified. The alarming reading — that ¶2's obligations *are*
unable-to-check, making every file *cannot establish* — is foreclosed by
`[R-CNF-11]`'s own qualifier, which §2.3 states twice: "unable to check on a
capability or resource ground". Absence of a witness is neither. No
competent verifier lands there. Not byte-level; editorial, one sentence.

### G22 `21.7-ordinal-mappings-unwitnessed` — adversary-06

A different sentence of ¶2 from G9's, so a separate defect: "the ordinal
mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a structurally
valid tile whatever values it carries". I re-derived the counterexample.
Interleaved, d = 1, E = 5, T = 4, one uint8 channel, fill 0x5A. G = 2,
P = 4. The tile at tile coordinate 1 covers x ∈ [4,8): in-tile ordinal 0 is
real, 1–3 are padding, and `[R-SER-05]` fixes them to 0x5A. A writer that
implements `[R-SER-01]`'s value sequence in reverse in-tile order emits
`5A 5A 5A v`; a verifier applying the correct mapping reads ordinal 3, finds
v, and T4 fires whenever v ≠ 0x5A. So the mapping violation *is* witnessed —
in exactly the places ¶1 names for `[R-COD-10]` ("padding positions, pad
bits, and boolean bytes"), and `[R-COD-10]`'s own text draws the same line.

Not byte-level: the mis-ordered file is nonconforming via T4 under either
account, and every verifier discharging `[R-SER-05]` finds it. But the
consequence reaches the register, not just the prose: `[R-COD-10]`'s
partially-detectable case carries a cause row (T26, "the check that detects
it is T2's or T4's, and this row records the cause rather than a procedure
of its own"), and on the parallel `[R-SER-01]` carries none. §21.1 makes the
register's completeness normative with detectability as the gate, so either
§21.7 gets `[R-COD-10]`'s qualification or §21.4 gets a T26-shaped row —
and the second moves §21.8's counts and the corpus. Register-bookkeeping,
maintainer decision.

### G23 `instance-criterion-value-vs-magnitude` — adversary-07

Graded PARTIAL: something is genuinely loose in §21.1's criterion, but the
reporter's conclusion (F23 and L12 owe two instances each; §21.8 becomes
275) does not follow.

The criterion's carve-out reads: "A comparison with no magnitude ordering
enumerates no direction … Nor does a field tested only for being nonzero —
an *A ≠ 0*, an *S ≠ 0* — which is a value test **and not a comparison of two
quantities at all**." F23's "inline_length is not 1" tests one quantity from
the file against a constant this specification fixes. It is not a comparison
of two quantities, so the carve-out's stated *reason* covers it; only the
carve-out's stated *scope* ("tested only for being nonzero") does not.

I checked the register's actual practice against that distinction and it is
consistent, which the reporter did not do. Two-quantity comparisons
enumerate directions: L21 (entry_count against the geometry-derived count),
L22 (extent_length against the formula), L30 (fill prefix against the
declared type's element size). Field-against-a-fixed-constant tests take one
instance: F11 (generation is 0), F13 (not a multiple of 64), F16
(dir_length < 4, also directionally bounded), F23, L12. Rows of the form
"a value other than X" enumerate the *value ranges* §10.2 defines rather
than directions — L31, L33, L34, L36, L43, L45 — and F23 has no such ranges,
which is why its cell is "—".

So the register is right and the criterion's wording is incomplete.
Register-bookkeeping, no count change: widen the carve-out from "tested only
for being nonzero" to "tested against a constant this specification fixes",
which confirms F23 and L12 at one instance each and leaves 273 standing —
subject to G13 and G22, which move it for other reasons.

---

## Coverage check, counted not asserted

38 input ids, 23 groups. Members per group: 2, 1, 3, 1, 1, 1, 3, 3, 3, 4, 1,
1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1. Running sum: 2, 3, 6, 7, 8, 9, 12, 15,
18, 22, 23, 24, 26, 27, 28, 29, 30, 32, 34, 35, 36, 37, 38. Each id appears
once; no id appears twice; none dropped.

Byte-level count: 1 (G3).
