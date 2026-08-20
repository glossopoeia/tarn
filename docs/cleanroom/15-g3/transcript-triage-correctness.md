# Round 15 triage — correctness lens — working transcript

Lens: *is this true of the document?* Every quotation checked against
`spec/tarn.md` at head. I did not open any `transcript-triage-*.md`.

## What I read

- `spec/tarn.md` in full (4227 lines, read in five contiguous passes).
- `transcript-adversary.md` lines 295–334 and 415–474 (finding `adversary-01`
  arrived truncated mid-sentence — "§17.2's Note states this outcome in term" —
  and its header said *self-flagged byte-level: no* while the transcript says
  **"Byte-level: yes."** I read the transcript to judge the actual claim).
- `transcript-writer.md`, `transcript-diagrams.md` greps for the shrink finding.
- `grep -n -i "shrink|grow|growth" spec/tarn.md` — one occurrence of "shrink",
  in §11.1's Rationale (line 1476). This is load-bearing for group C.

Not read: `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`, `registry.json`, git
history, the web, any triage transcript.

## Method

For each finding: locate the quoted text, read it in context, ask whether the
reporter's second reading is actually licensed by the words or only by a reader
who stops early. Then the byte-level test, with the explicit round-14
discrimination: *if the fork is in writer conduct only, can some other
conforming actor emit the disputed byte sequence?* If yes, the emittable set is
unchanged and the finding is not byte-level; if no, it is.

---

## Group-by-group

### A — §20.5's "anywhere §5.2 admits" (writer-01, diagrams-01)

Line 3132 verbatim: "A compactor preserves content but not placement —
placement is not among the things it carries forward, and it is free to place
structures anywhere §5.2 admits". §5.2 constrains only the partition; §16.1's
"every stored tile's offset satisfies offset mod A = 0" and §16.2's packing are
not §5.2's subject. §20.2 (line 2868) carries the qualifier the twin omits:
"in any order satisfying §5.2's coverage classes … and every declared layout
invariant (`[R-SLB-01]`, `[R-SLB-03]`)". Both reporters correct. Twin-sentence
divergence confirmed.

Byte-level: no. Four sentences decide the output, three of them in §20.5's own
paragraph: "Given a conforming input the output is a conforming file"
(line 3106); `[R-CNF-06]`; `[R-WRT-01]` "An appender and a compactor satisfy
every writer requirement for the bytes they produce"; `[R-CNF-05]`.

writer-01's second edge — §16.2 `[R-SLB-04]` offering "clear the declaration"
against `[R-WRT-07]`'s closed exception list — does not hold on the words.
`[R-SLB-04]` binds "A writer or updater whose **commit** changes …"; §9.1 makes
compaction "a whole-file rewrite", expressly *not* a commit ("every conforming
mutation of a file is either a commit (§9.2) or a whole-file rewrite under a new
file_id (compaction, §20)"). So `[R-SLB-04]` does not reach a compactor and the
alleged §16.2/§20.5 conflict is not one. Grouped anyway; noted in the repair.

### B — §20.3 step 4's alignment clause (writer-02)

Line 2972: "an aligned layer's new tiles satisfy its invariant or the
declaration is cleared (`[R-SLB-01]`, `[R-CNF-05]`)". `[R-SLB-01]` carries no
such quantifier, and L40 restates it unquantified. The reachable gap is a commit
that *newly declares* A on a layer with retained stored tiles: the step-4 bar
does not reach it (alignment is not among the §14 loci), so the commit is
otherwise permitted, and the summary asks the writer to align only what it
writes. (For a layer already carrying A, retained tiles already satisfy it, so
there the sentence under-states without consequence.) Real, and narrower than
writer-02 frames it — but writer-02 identifies the same reachable case.

Byte-level: no. The sentence's own citation decides it: `[R-CNF-05]` "A writer
MUST emit only conforming files", with `[R-SLB-01]`'s unquantified invariant.

### C — the de-addressing shrink (writer-03, diagrams-05, quiz-01) — UPHELD

This is the one I uphold and I want the reasoning on the record.

`grep -c shrink spec/tarn.md` = 1. The single occurrence is line 1476, inside a
block quote §2.1 labels *Rationale* and therefore denies force: "Extents grow; a
shrink is barred wherever it alters what §14 fixes for a tile the layer already
stores (§20.3, which states the tense normatively and governs), which is the
ordinary case". It defers to §20.3, and §20.3 never mentions shrinking.

I searched for deciding text as hard as I searched to refute:

- §20.3 step 4's bar quantifies over "any tile that layer stores **in the
  generation this commit supersedes**", tested by whether the change "alters …
  what §14 fixes for its stored bytes or how they decode".
- Its enumerated loci — padding set, padding content, decoded size, sample byte
  offset, codec and filter — every one presupposes a tile that still exists.
- Its gloss: "a change that leaves every one of those tiles' stored bytes
  meaning exactly what they meant … is not what this bars." This is a
  *sufficient* condition for not being barred; it does not entail that
  everything else is barred, so it points toward "barred" without forcing it.
- §20.3's index-re-emission enumeration names only growth among geometry
  changes: "entries new to this generation (added tiles, grown extents)". It has
  no case for an entry that vanishes.
- §20.1's appender tier (line 2849): "adding layers or records, superseding
  tiles, growing extents, amending metadata" — shrinking absent, but the list
  reads illustrative and is not a MUST.
- §13.3's Note (line 1773): "grows its extents across a grid boundary" — growth
  again, and a Note.

Nothing decides it. Four of the six walkers reached the question independently
and split: writer and diagrams read it barred, adversary reads it "genuinely
unclear from step 4's text" and leans permitted (transcript line 311), quiz
calls it two defensible readings. That split is itself evidence the words carry
both.

**Byte-level: yes, on the emit half of the test.** Take the layer writer-03
built: extents (5,5), tile extents (4,4), tiles 0, 1, 3 stored at generation 1;
generation 2 shrinks E_y 5→4, giving G=(1,2), entry_count 2, tile 3's 80 bytes
falling to slack. Call that file X.

- Under the barred reading, no conforming updater may emit X: `[R-CNF-06]`
  makes `[R-WRT-04]` binding on it, and the escape route — unstore tile 3 in an
  earlier commit, shrink in the next — produces generation 3 and different
  bytes. §20.3 forecloses doing both at once: "a commit does not escape this by
  unstoring in the same breath".
- Under the permitted reading, a conforming updater may emit X.
- **No other conforming actor can emit X.** X's trailer carries generation 2.
  `[R-LIF-02]`'s creation path fixes "generation 1"; `[R-WRT-06]` fixes a
  compactor's output at "generation 1". Generation 2 comes only from an
  appender's commit on X's own generation-1 prefix, and that prefix declares
  E_y = 5, so any commit producing X is this shrink.

That is precisely the discrimination the round-14 note asks for, and it comes
out the other way from group O below, where the disputed output is generation 1
and a creator could emit the identical bytes.

The counter I considered and rejected: §21.7 declares the step-4 bar unwitnessed
where the damaged tiles are superseded, so no verifier verdict on X forks and X
is a conforming file as a pure predicate on bytes (`[R-CNF-02]`). True — and it
disposes of the *accept/reject* half only. The test has two halves. Adversary's
"foreclosed for verdict purposes" is right about verdicts and silent about
emission.

Note also that `[R-CNF-02]`'s conduct carve-out does not cover this bar: it
names "where a value is published, or which registry version a writer targets
(§10.3, §18.3)" and "§6.3's flags = 0 … and §6.2's pre-trailer gap", and says
each such case "is declared where it arises". §20.3 step 4 is not declared to be
one.

### D — Appendix G item 3's first structure (writer-04)

Line 4100: "The first structure begins at 16 … each later structure begins where
the previous one ended, save where alignment forces a gap". The proviso attaches
to the later-structures clause; item 5 licenses "fixed declared values" of A;
item 3's order puts the alphabetically-first layer's first stored tile first;
`[R-SLB-01]` then forbids offset 16 for A ≥ 512. Accurate. (The index region is
not caught — `[R-SLB-01]` binds stored tiles only — so the collision needs the
first layer to store a tile, which is the ordinary case.)

Byte-level: no. Appendix G is "non-normative" and "adds no requirement to any
actor: a writer ignoring it is fully conforming" (line 4046).

### E — Appendix G's completeness claim (writer-05)

"can adopt this profile, which closes the degrees of freedom this format
deliberately leaves open" (line 4044) against §20.4's "A compactor may drop it
whenever it rewrites the file", which no numbered item pins. Item 2 puts
compactors in scope explicitly. Claim accurate.

Sharper than writer-05 states it: item 2 already destroys byte-identity for
compactors on its own — "a compactor adopting the profile takes `[R-WRT-06]`'s
fresh draw instead", and a fresh random draw is not reproducible at all. So the
opening claim fails for compactors twice over, and the honest repair may be to
scope the profile to creators rather than to add a tenth item.

Byte-level: no, same non-normativity quote as D.

### F — partial slack total (verifier-01) — PARTIAL

The MUST's antecedent is the general clause, not the pair: "Where the walk of
§9.7 does not enumerate every region's claimants — whether because … or
because … — the verifier MUST report the total as partial." A resource decline
under `[R-ERR-04]` satisfies that antecedent, so the MUST fires and reading (2)
is not on the words; §9.7's parallel is an em-dash apposition to "Where the walk
does not complete", same structure. Appendix H corroborates: "naming the scope
or violation that stopped the walk" admits a scope with no violation.

So verifier-01's alleged unsatisfiable MUST is refuted, and what survives is
that the aside under-enumerates. That is a PARTIAL, not a CONFIRMED.

### G — §21.2's preamble (verifier-02, register-01, adversary-03)

Preamble (line 3268): "Every row here presupposes a file this specification
judges: one declaring format major 1 … no row below reaches it — §6.2's ordered
validation puts the version gate ahead of every check but the trailer magic and
the trailer CRC".

Checked each escapee:

- **F6/F1's front-block instance.** §19.1 step 1 places the equality check
  before step 2's trailer; F6's own cell says "a verifier holds no such
  exemption (§2.3)"; Appendix H repeats it naming F1 and F6; `[R-CNT-24]` makes
  the front block constant "in every format major version". Escapes. Confirmed.
- **F18.** §6.2's Valid-values cell reads "1 (0 invalid; others: §6.3)" — zero
  is *invalid*, not another major — and §21.6 points at F18 for "version_major
  = 0, permanently invalid in every format major version". So F18 is a row about
  a file that does not declare major 1, which the preamble's first sentence
  excludes. This is the sharpest form and only register-01 and adversary-03
  reach it. Confirmed.
- **F5** (register-01 only). `[R-CNT-27]`'s 128-byte floor is nowhere placed in
  §6.2's order, so it is not "ahead of" or "behind" the version gate by any
  stated rule. Weaker than the other two but not wrong.

Byte-level: no. `[R-CNT-07]` "A reader MUST reject-file when version_major is 0
(invalid) or is a major it does not implement" fixes the reader's verdict on the
F18 file; `[R-CNT-04]` fixes it on the corrupt-front-block file. On the verifier
side both candidate verdicts bar certification: §2.3 "a verifier MUST NOT
certify a file it reports that way". No accept/reject forks.

§21.1's standing tiebreak genuinely does not reach this — it is scoped to "a row
and the rule it cites" and extended only to §21.6's entries. verifier-02 is right
about that and it is why this is not the register-row-versus-rule pattern earlier
rounds over-claimed on.

### H — §11.1's parenthetical at E=0 (verifier-03, diagrams-03, adversary-02)

"A tile extent MAY exceed its dimension's extent (the grid is then a single
padded tile along that axis)." Antecedent satisfied at Eᵢ = 0 (Tᵢ ≥ 1 by the
same requirement); consequent false. Next paragraph, `[R-GEO-02]`: "A dimension
with extent 0 is valid: its grid count is 0 …". `[R-GEO-03]`: ⌈0/T⌉ = 0. All
three reporters correct, and all three decline to inflate it.

Byte-level: no — `[R-GEO-02]` is normative, adjacent, and specific to exactly
this case; `[R-GEO-03]` gives the arithmetic. Quoted in the group entry.

### I — §21.1's "serve the structure unchanged" (diagrams-02, register-02, reader-02, quiz-03)

Line 3262: "for several such rows it obliges the reader to serve the structure
unchanged (`[R-SER-08]`, `[R-CNT-22]`, and `[R-MTA-05]` …)". Two independent
errors for `[R-SER-08]`, both real:

1. It is the document's one *resolved* byte. §14.2: "MUST report 0x00 as false
   and every other byte as true"; §12.3 calls it "the one case where a reader
   resolves a byte to a value rather than passing it through"; Appendix H "the
   sole resolved byte".
2. It obliges nothing unconditionally — "A reader that neither detects the
   violation nor rejects the tile, and returns the value, MUST …", with
   `[R-CNF-12]` licensing rejection.

True for `[R-CNT-22]` and `[R-MTA-05]`, false for `[R-SER-08]`.

Byte-level: no. §14.2 states the obligation directly and §21.1's own clause
defers ("the governing rule states what a reader does"). Both readings concern a
returned sample value in a file that is accepted either way; §14.2 records that
"it never arises in a conforming file". register-02 is scrupulous in flagging
that §14.2's Rationale calls exactly this returned-value fork the thing the
format exists to prevent — noted, but a returned value is not a byte a file
carries, and the rule that fixes it is unambiguous.

### J — §21.7's "the §21.4 rows then fire" (verifier-04, register-03, reader-03)

Two independent counterexamples, both of which I checked row by row:

- register-03's filter 1→2 on interleaved float32, E=T=256, G=N=1, P=256, Q=4,
  decoded size 1024, codec 1, no padding (G·T = E), no bool. T1 crc unchanged;
  T3 length preserved (`[R-COD-10]` "Length is unchanged"); T14 1024 = decoded
  size; T4/T5 no padding, no pad bits; T2 no bool; T17–T22 not zstd; T24/T25
  codec 1; T26 needs a broken structural constraint and there is none. No row
  fires, and the change is squarely inside the bar ("the codec and filter that
  produced the stored bytes"), with the identity escape unavailable at stride 4.
- verifier-04/reader-03's channel permutation with equal fills and no padding.
  Note that this one is barred by the *general* test rather than by an
  enumerated locus: the byte offset of a **sample** is unchanged (Q is the same);
  what moves is Fᶜ, the in-sample channel offset. §20.3's "The test is the
  effect on such a tile, and the list names where that effect arises rather than
  standing on its own" is what catches it.

So the appositive asserts something false. verifier-04's framing as a two-reading
ambiguity is the weaker description; register-03 and reader-03 name it correctly
as a misclassification. The register's contents do not change either way — the
condition is genuinely undetectable and so outside `[R-CNF-07]`'s gate.

Byte-level: no — the counterexample file is conforming under either reading
(`[R-CNF-02]`; §21.7 ¶1's own "produces a file that every checksum in §8
certifies"), and §20.3's bar binds the writer identically under either.

### K — L40/L42 missing L41's transparency (diagrams-06)

L41 carries "sentinels and entries §15.3 classifies reject-tile on a structural
ground are transparent"; L40 and L42 say only "a stored tile". §15.3's carve-out
is general — "Such an entry contributes no stored extent to the *verifier* rows,
which bind over well-formed entries' extents only" — and its own table lists
"alignment or slab invariant violated (§16)" as one of those verifier rows.
So the rows under-state and §21.1's tiebreak decides.

reader-06's §8 list reaches the opposite disposition ("§15.3's clause is
general … so L40 is covered. Not a defect"). Both are right about the verdict;
they differ on whether a row that needs §15.3 to be read into it is worth
repairing. It is, on the same ground L41 already concedes.

### L — R4 against T17–T20/T18 (diagrams-07, register-04)

Grouped as one: both are the same asymmetry — the same `[R-COD-06]` constraint
set is one compound row with 12 instances at extent scope and five rows with
T18's four positional instances at tile scope — seen at the row level
(register-04) and the instance level (diagrams-07).

§21.1 supplies two sentences that pull opposite ways: "each row is one malformed
condition" (R4 is six) and "the count is therefore mechanical once the cell is
written" (which makes writing the cell the free step). Neither settles when a
requirement's alternatives become rows and when they stay instances.

One correction to diagrams-07's arithmetic: for a *document* there is no
"between two frames" placement that is not already a second-frame violation, so
the parallel to T18 is at most two extra placements per container, not three.
The asymmetry stands; the number does not follow mechanically.

reader's §8 audit asserts "every cell obeys §21.1's instance criterion as
written" — which is true only if R4's condition text ("a skippable frame") is
taken as the criterion's input rather than `[R-COD-06]`'s "anywhere". That is
the ambiguity.

Byte-level: no — same outcome, same detector, same tier either way; and
`[R-VEC-01]` makes the corpus derivative.

### M — F27/L48 omit "at every nesting depth" (register-05)

`[R-MTA-05]` reads "Writers MUST serialize object members, **at every nesting
depth**, in ascending order". Neither row carries it, and F27's "top-level"
(which distinguishes the record from L48's sub-record) can be misparsed onto the
object. Accurate; §21.1's tiebreak decides; both rows under-state.

### N — §4.2's "All … byte lengths … are u64" (register-06)

False twice: §7.2 gives inline_length as "| 4 | 4 | u32 | inline_length |", and
§4.6 makes every name length prefix a u8 ("so every name's length prefix is a
single byte"), with §7.4 spelling "u8 len + bytes" for the layer, dimension and
channel names and the fill field. Confirmed.

The finding's second half — that `[R-ERR-05]`'s hard-limit list omits
inline_length's 2³² − 1 ceiling — is answered by `[R-ERR-05]` itself: "The hard
limits it restates are a finding aid rather than an inventory". Not a defect.

Byte-level: no. `[R-ENC-06]` "No field's width is ever a writer choice: every
field's width is fixed by this specification" plus §7.2's row.

### O — §20.5's "it can neither drop the structure" (reader-01)

Verified the three texts. §20.5 line 3112: "MUST NOT emit a file carrying a
violation it has detected: it can neither drop the structure (§20.4,
`[R-WRT-07]`), nor re-emit it corrected". §20.4's MU=0/PE=0 row: "A compactor
may drop it whenever it rewrites the file." §20.5's own opening: "less any
record §20.4 lets it drop". The parenthetical cites §20.4 for a proposition
§20.4 denies in one of its three rows. Confirmed, and reachable exactly as
reader-01 says (F36 or F26 on a droppable ancillary).

**Byte-level: no**, and this is the case that contrasts with group C. Under the
refuse reading the compactor emits nothing; under the drop reading it emits a
generation-1 file with a fresh file_id and free placement. That byte sequence is
one a **creator** may emit — `[R-LIF-02]`'s creation path produces exactly a
generation-1 file, placement is free (`[R-SLB-05]`), and the output carries no
violation. So the set of byte sequences a conforming implementation may emit is
the same under both readings, and only the compactor's conduct forks. reader-01
argues byte-level on the ground that "implementation A emits nothing for an
input that implementation B compacts"; that is a fork in conduct, and the
emittable set is what the test names.

### P — the compactor and a structurally malformed entry (reader-06, quiz-02)

`[R-WRT-07]`'s enumeration — "entry offsets new; entry lengths, entry crcs, and
sentinel entries unchanged" — has no case for a non-sentinel entry §15.3
classifies reject-tile structurally. The state is real: §20.3 step 2 provides for
it on the append path ("carried forward byte-identically at its disk-ordinal
position under step 4, **not** repaired to a sentinel").

The answer is derivable, and I traced the chain to be sure: §2.3 makes an
updater a reader of what it processes; `[R-WRT-09]` makes a compactor rely on
every entry ("each relocated extent's checksum, including every stored tile's
entry crc"), so §19.2's reliance rule puts `[R-IDX-03]`'s classification on it;
having detected, §20.5's "MUST NOT emit a file carrying a violation it has
detected" forces refusal; and `[R-CNF-04]` "A reader MUST NOT heuristically
repair a violating structure" forecloses the sentinel substitution independently.

Four hops. Both reporters file it as an observation and both are right: the
enumeration reads complete when it is not.

### Q — the Rationale's "disk ordinals renumber" (reader-04)

`[R-GEO-06]`: s = Σᵢ tᵢ · ∏_{j>i} Gⱼ. G₀ appears in no product, so raising G₀
moves no spatial ordinal. Interleaved disk ordinal = s, so growth along the
first-declared dimension renumbers nothing; planar disk ordinal = c·N + s does
move with N. reader-04's "false for every rank-1 growth whenever d = 1" is
imprecise — a rank-1 *planar* layer with C ≥ 2 does renumber — but reader-04
names that exception in its own parenthetical, and the core claim holds for the
interleaved case and for planar C = 1.

"the first growth of a zero-extent layer included" is worse than imprecise: at
entry_count 0 there are no ordinals to renumber at all.

Byte-level: no — §2.1 denies Rationale text force, and §20.3 states it correctly
and normatively: "(a geometry change renumbers ordinals **wherever**
`[R-GEO-06]` moves them)".

### R — "the one such bound in format major 1" (reader-05, adversary-05)

Checked adversary-05's construction: d=1, T=1, C=1, E grown to 2⁶². G = N =
entry_count = 2⁶², in domain; `[R-CNT-17]`'s region length 20·2⁶² + ⌈2⁶²/2¹⁶⌉·4
≈ 2⁶⁶ ≫ 2⁶³ − 1, which L2's Instances cell registers by name. Codec 1, so
`[R-COD-07]` is not in play. The exhaustiveness claim is false on reading (i).

Reading (ii) — that "bounds the layer's own declarations impose" means
declaration-*conditional* bounds — is available but strained: N·P and P·Q are
imposed by the layer's own T's and E's as directly as the lz4 cap is imposed by
its codec field. Either way the sentence is misleading writer guidance.

Byte-level: no. `[R-GEO-03]` "These products, like all geometry arithmetic, are
subject to `[R-ENC-04]`: a reader MUST treat a product exceeding 2⁶³ − 1 as a
validity error at layer scope", with `[R-CNF-05]`. L2 fires on the bytes under
either reading.

### S — §21.7 ¶2's missing disclaimer (adversary-04) — PARTIAL

The asymmetry is real: ¶1 closes with the `[R-CNF-11]` disclaimer and ¶2 does
not. But adversary-04's reading (ii) is foreclosed by the text adversary-04
itself quotes: `[R-CNF-11]` qualifies its ground twice as "a capability or
resource ground" ("the last where some requirement is one it is unable to check
on a capability or resource ground"; "MUST report each requirement it was unable
to check on a capability or resource ground"). Absence of a witness is neither.
So there is no permitted second reading, and the finding is an observation about
parallel structure, not an ambiguity. PARTIAL.

### T — "satisfied … whatever values it carries" (adversary-06)

Checked the construction: interleaved, d=1, E=5, T=4, one uint8 channel, fill
0x5A. G=2, N=2, P=4; the tile at tile coordinate 1 covers x ∈ [4,8), so in-tile
ordinal 0 is real and 1–3 are padding, and `[R-SER-05]` fixes the decoded image
to `v 5A 5A 5A`. A writer that implements `[R-SER-01]` in reverse in-tile order
emits `5A 5A 5A v`; a verifier applying the correct mapping reads ordinal 3, a
padding position, and finds v. T4 fires whenever v ≠ 0x5A. So the mapping *is*
witnessed, in exactly the place §21.7 ¶1 already concedes for `[R-COD-10]`:
"padding positions, pad bits, and boolean bytes". The same argument reaches
`[R-GEO-06]` — a wrong spatial-ordinal mapping puts a non-edge tile's content at
the edge ordinal's entry, and T4 fires there too.

Confirmed. Byte-level: no — the mis-ordered file is nonconforming via T4 and
`[R-SER-05]` obliges every verifier to look ("a verifier MUST check it, and a
violation is a validity error at tile scope").

### U — F23/L12 against L30 (adversary-07)

§21.1's criterion: "Where the condition compares two **magnitudes** either of
which can be the greater — a *differs from* or *does not equal* — the two
directions are likewise enumerated". "inline_length is not 1" is such a
comparison: 0 (encoding byte absent) and ≥ 2 (extra bytes) are distinguishable
files and greater names something. The carve-out is for comparisons with **no**
magnitude ordering — "a stored checksum against a computed one, or a byte
pattern against a constant" — which this is not.

Corroborating asymmetry adversary-07 does not cite: **L39** splits "A below 512"
from "A above 2^62", so the register does enumerate directions against literal
constants elsewhere. That strengthens the finding.

The counter-reading — that F23's clause "not a growable one" bounds the
comparison — fails on §21.1's own words: "where its own **text** bounds the
comparison", and the condition text is the unbounded "is not 1".

Byte-level: no — `[R-MTA-03]` "A record whose inline_length is not 1 is a
validity error at the record's containing scope" catches 0 and 2 alike. What
moves is §21.8's 273 and the corpus size under `[R-ERR-02]`/`[R-VEC-03]`.

### V — P·Q in a layer that addresses no tiles (adversary-01) — PARTIAL

The input arrived truncated before Reading B; I read the transcript. The
construction (192 bytes, E = 0, T = 2⁶², one float64 channel, codec 1, P·Q =
2⁶⁵) is sound and I re-derived every stated quantity.

The reporter's byte-level claim rests on the proposition that the *only* sentence
addressing the empty-layer case for `[R-ENC-04]` sits in a Note. That is not
quite so, and finding the deciding text is this pass's job:

1. `[R-SER-02]` closes "These products and sums are declaration-derived
   quantities under `[R-ENC-04]`" — normative, unqualified, immediately under
   the table that defines P·Q.
2. `[R-SER-07]`: "decoded size is a function of the layer's declarations
   alone — geometry, layout, and channel types — never of payload content …
   Every decoded size, and the value count V, is a declaration-derived quantity
   under `[R-ENC-04]`." This severs decoded size from any stored tile, which is
   exactly what Reading B needs and does not get.
3. The register carries the contrast in **normative** text, not a Note: L44's
   condition is expressly quantified ("a layer any of whose **addressed** tiles'
   decoded size exceeds 0x7E000000") while L2's instance cell — "P·Q (which
   dominates V = P·C); P·Bᶜ" — carries no quantifier, at detection point layer
   access.
4. §20.3 step 4, normative: "`[R-COD-07]`'s lz4 decoded-size cap being the one
   such bound in format major 1 (L44), which an empty layer **escapes only
   because that cap is quantified over addressed tiles**." The escape is
   attributed to the quantifier; a rule without one does not escape.

Reading B's remaining leg — §19.3's checklist not citing `[R-SER-02]` — is
removed by §19's own preamble: "Those enumerations are not the complete
inventory of what a reader detects at that tier: §21's register is."

So the document does decide it, and the fork is not open. What survives is the
reporter's repair, which is worth taking: the clearest statement is in a Note and
should be normative. PARTIAL, byte-level downgraded.

I record that this was the second-closest call in my set.

### W — Appendix G and the directory's record order (diagrams-04)

Item 3 applies "ascending record order" to exactly one thing: "then any record
extents in ascending record order". It never says the directory emits records in
that order, while the closing paragraph lists among what the items add "record
and sub-record order, which `[R-CNT-14]` leaves free".

diagrams-04's sharpest evidence checks out: item 3's tie-break "type 0x0001 ties
by layer name" is dead for extent placement, because a type-0x0001 record's
extent is the tile-index region, which item 3 places in the earlier per-layer
stage ("For each layer in ascending layer-name byte order: its stored tiles in
disk-ordinal order, then its tile-index region"). The clause has work to do only
if the key also orders the directory. And "so it is otherwise free to vary" has
no antecedent under the narrow reading.

Byte-level: no — Appendix G "adds no requirement to any actor".

---

## Coverage check

Counted twice, by reporter and by group.

Reporter roll-call: writer 01→A 02→B 03→C 04→D 05→E; verifier 01→F 02→G 03→H
04→J; diagrams 01→A 02→I 03→H 04→W 05→C 06→K 07→L; register 01→G 02→I 03→J
04→L 05→M 06→N; reader 01→O 02→I 03→J 04→Q 05→R 06→P; adversary 01→V 02→H 03→G
04→S 05→R 06→T 07→U; quiz 01→C 02→P 03→I.

Group sizes: A2 B1 C3 D1 E1 F1 G3 H3 I4 J3 K1 L2 M1 N1 O1 P2 Q1 R2 S1 T1 U1 V1
W1 = 38. Ids: 5+4+7+6+6+7+3 = 38. No id in two groups; no group empty.

Byte-level upheld: 1 (group C).
