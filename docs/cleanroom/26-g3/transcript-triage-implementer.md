# Round 26 triage — implementer-consequence lens

## Disclosure of what I read

Read only `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, via `sed -n`/`grep`
over these ranges: §2.1–2.5 (96–280), §3.1–3.2 (282–345), §4.2–4.5 (382–435),
§5.1–5.2 (557–692), §6.1–6.3 (693–800), §9.2 (1166–1225), §9.6–9.7 (1288–1375),
§11.1–11.4 (1466–1600), §13.3–14 (1748–1800), §15.1–15.4 (1993–2120),
§16–16.2 (2116–2225), §17.2–17.4 (2242–2410), §19–19.4 (2685–2900),
§20.3–20.5 (2943–3210), §21.1–21.9 (3343–3760), Appendix A (4099–4150),
Appendix G (4273–4415), plus a `grep -n '^#'` header index and a
`grep -n 'Gᵢ\|G_i\|Gⱼ\|grid count'` census.

I listed the round26 scratchpad directory once with `ls` (before reading the
instruction not to). The listing showed only the six walk transcripts, the three
quiz transcripts, and two scratch .py files; **no `transcript-triage-*.md` file
existed at that moment and I opened none of them.** I opened no walk transcript
either — every claim below is checked against the spec directly.

Did not read: docs/, PLAN.md, AGENTS.md, conformance/, spec/registry.json,
git history, the web.

## Grouping (25 ids → 17 groups)

| group | members |
|---|---|
| last-zero-grid-count | reader-02, writer-01, verifier-03, adversary-02, quiz-02 |
| sparse-note-reemission-trigger | reader-01, writer-02, diagrams-03, quiz-03 |
| cost-note-stored-tile-set | diagrams-02 |
| alignment-structural-transparency | reader-03 |
| profile-summary-omits-filter | writer-04 |
| profile-filter-identity-stride | writer-05 |
| profile-input-undefined | diagrams-04 |
| commit-channel-set-and-rank | writer-06 |
| grid-times-tile-extent-overflow | verifier-01 |
| partial-slack-sum-vs-union | verifier-02 |
| appendix-a-local-vs-resident | diagrams-01 |
| file-scope-geometry-carve-out | register-01 |
| two-senses-of-F | register-02 |
| l23-detection-tier | register-03 |
| unwitnessed-obligations-account | writer-03, register-04 |
| codec-1-length-vs-sentinel | adversary-01 |
| recovery-rejected-count | quiz-01 |

Splits I deliberately did NOT make into one group:
- §13.3's Note and §20.3's cost Note are the same *shape* of defect in two
  passages with two separate repairs. diagrams-03 itself says "the same case as
  diagrams-02, reached through a different phrasing", i.e. the reporter treats
  them as two locations. Two groups.
- Appendix G item 5 is quoted by writer-04, writer-05 and diagrams-04, but the
  three defects are distinct: a missing member in the closing summary list; a
  factually false clause inside the item; and an unpinned degree of freedom the
  item's own argument reaches. Three groups, three repairs.
- writer-03 and register-04 are one group: writer-03's [R-LIF-02] step 3 is a
  member of register-04's swept family, and the repair is the same sentence.

## The one byte-level call: grid-times-tile-extent-overflow (verifier-01)

I confirm this as byte-level. Statement of the fork, checked:

[R-ENC-04] binds "any quantity this specification **defines** as a sum or product
of integers obtained from a file (offsets plus lengths, grid counts, tile counts,
sample-position counts, ordinals)". §11.3 writes `Gᵢ · Tᵢ` exactly once
(line 1533, `grep` census) and never names or defines it as a quantity — that is
the whole of reading A.

[R-GEO-03] says of N, P, addressed-tile count and N·P: "These products, **like all
geometry arithmetic**, are subject to `[R-ENC-04]`: a reader MUST treat a product
exceeding 2⁶³ − 1 as a validity error at layer scope." That is normative and it
reaches beyond the four it names — reading B. §17.2's Note reinforces B in the
one place the empty-layer case is discussed: "it binds any sum or product a file
yields — so P·Q and P·Bᶜ are checked in an empty layer even though this cap is
not." And L2's *row condition* is "A declaration-derived sum or product of a
layer exceeds 2^63 - 1 although every contributing field is in domain", which
covers Gᵢ·Tᵢ on its face; only the Instances cell omits it, and §21.1 says
"where a row and the rule it cites diverge, **the rule governs**" — so the cell
cannot decide it against [R-ENC-04].

I could not produce a sentence that decides between them, which is the bar the
charter sets for a downgrade. I checked §19.3 as a candidate decider: it obliges
"the geometry floor and its arithmetic (`[R-GEO-01]`–`[R-GEO-03]`), the 2⁶³ − 1
ceiling on every quantity that arithmetic derives". §11.3 is [R-GEO-04], outside
that cited range — a real argument for A at *reader* scope. It does not settle
file conformance, because §2.3 makes a verifier check "every file-level
requirement — including those ordinary readers are exempted from", so the
verifier's verdict and the writer's permission still fork.

Arithmetic re-derived independently: N·P = ∏(Gⱼ·Tⱼ) with every factor ≥ 1 when
every Eⱼ ≥ 1, so N·P ≥ Gᵢ·Tᵢ and L2's existing N·P instance already catches every
Gᵢ·Tᵢ overflow whenever no extent is 0. The readings can therefore diverge only
at N = 0. Reporter's witness re-checked: rank 2, E₀ = 0, T₀ = 1 → G₀ = 0;
E₁ = 2⁶³−1 (at the [R-ENC-03] ceiling, in domain), T₁ = 2 → G₁ = ⌈(2⁶³−1)/2⌉ =
2⁶². G₁·T₁ = 2⁶³, over by exactly 1. N = 0, P = 2, N·P = 0, C·N = 0,
entry_count = 0, extent slot (0,0), crc_of_crc_array = 0 — L21, L22, L27 all
hold, L44 does not apply at codec 1, §21.9's decoded-tile row does not bind.

Two implementations, concretely:
- Verifier A builds its layer-arithmetic checklist from L2's Instances cell —
  the natural corpus-driven route, since §21.8 counts instances and §24 builds
  one vector per instance. It never computes Gᵢ·Tᵢ, certifies the file, and its
  reader serves the layer under [R-GEO-02]'s "Readers MUST accept such a layer".
- Verifier B reads [R-GEO-03]'s "all geometry arithmetic" as written and computes
  every product §11 mentions, including §11.3's padded axis extent. It books a
  reject-layer under [R-ENC-04] and reports *nonconforming*. Its reader refuses
  the layer.
Same bytes, opposite verdicts; under [R-CNF-05] a conforming writer may emit that
file under A and must not under B. Corpus consequence: L2 gains a tenth instance
(277 → 278) or does not.

Repair is one line either way, and the maintainer must choose: add Gᵢ·Tᵢ to L2's
Instances cell and say in §11.3 that the product is subject to [R-ENC-04]
(picks B); or say in §11.3 that Gᵢ·Tᵢ is evaluated only for a layer that
addresses a tile, and confirm §4.2's parenthetical is the exhaustive gloss
(picks A).

## Downgrades, each with the sentence that decides it

### codec-1-length-vs-sentinel (adversary-01) — reporter flagged byte-level, I do not

The reporter's reading (a) — [R-COD-04]'s equality reaching sentinel entries —
makes [R-TYP-08] unsatisfiable in every codec-1 layer, and §19.4 leaves it no
step to apply at. Deciding text, in order of force:

1. §19.4 step 4 [R-RDR-04], the normative tile-read algorithm ("a conforming
   reader proceeds as follows"): "**Classify per §15.3.** A valid sentinel
   short-circuits steps 5 and 6 for that entry: every requested sample position
   of its tile reads as fill … A malformed entry rejects the tile." Classification
   precedes everything; [R-COD-04] appears nowhere in the eight steps, so there
   is no point in the reader path at which it can reach a classified sentinel.
2. §15.3's table, first row: "offset = S ∧ length = S ∧ crc = 0 | valid sentinel —
   reads as fill", under a rule that says "a reader MUST classify as follows".
3. §15.2 [R-IDX-02]: "Sentinel entries are a reserved pattern, **not offsets or
   lengths**." [R-COD-04] speaks of "The index entry's length"; a sentinel entry
   has no length for it to be about, and its premise clause — "The stored bytes
   are the filtered image verbatim … **therefore**" — presupposes stored bytes,
   which §3.1 makes exactly what a sentinel tile lacks.
4. §21.6, "Conditions that are not violations": "An index entry is the sentinel |
   The tile is addressed but not stored; every sample position it carries reads
   as the channel's fill". No codec qualification.
Under (a), [R-TYP-08]'s "MUST return … that channel's fill value" and
[R-CNF-09]'s "a read of a rejected tile MUST NOT silently return fill" are in
flat contradiction for every sparse codec-1 layer — the exact combination
Appendix G items 1 and 6 push a writer toward. A reading that makes two MUSTs
unsatisfiable is not a permitted reading where a consistent one exists.

**My premise, stated for attack:** that §19.4's numbered algorithm is exhaustive
of the reader's per-entry path, so a check the algorithm does not place cannot
fire against an entry the algorithm has already classified valid. Attack it by
arguing [R-COD-04] is a layer-validation check ("checkable from the entry and the
layer record alone, before any payload fetch") that runs outside §19.4 — which is
the reporter's bulk-sweep scenario. My answer: even outside §19.4, points 2–4
classify the entry as a defined non-violation, and (a) still breaks [R-TYP-08].

Not byte-level. But the omission of "(non-sentinel)" is a real house-style break
— T14 carries it, T8–T12 carry it, every structural row of §15.3 carries it — and
adding it to [R-COD-04] costs nothing and forecloses the sweep bug. Recommend the
edit.

### last-zero-grid-count (5 reporters, none flagged byte-level)

Decisive: [R-CNF-01] — "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*". The passage
is inside §11.1's Rationale block. The normative rules it glosses are
unambiguous and independently correct: [R-GEO-03] derives N = ∏Gᵢ, [R-CNT-17]
ties extent_length to entry_count, §20.3 step 4 keys re-emission to "stored-tile
set or index content".

On the merits the five reporters converge and I agree with them: the censuses
(three reporters ran independent ones; I spot-checked §11.4 "the last-declared
dimension varies fastest", §16.2's Note "a band along the last-declared
dimension", §11.2's "the last row of tiles", §21.9's "The last three rows") show
the house sense is positional, and under the positional sense the sentence is
false whenever two grid counts are 0 — raising the highest-indexed one leaves
∏Gᵢ = 0 and entry_count unchanged, which is the *preceding* sentence's class.
Implementer consequence is bounded and self-correcting: a writer that re-emits an
index region it did not need wastes bytes; one that emits a nonzero extent slot at
entry_count = 0 trips L22, and a nonzero crc_of_crc_array trips L27. Repair is two
words: "last **remaining** zero grid count". Editorial, and worth doing because
the word is bolded, i.e. marked load-bearing in the one sense the document never
uses elsewhere.

### sparse-note-reemission-trigger (§13.3 Note) and cost-note-stored-tile-set (§20.3 Note)

Same decisive quote, [R-CNF-01]'s Note exclusion, plus the normative rule stated
twice in full: §20.3 step 4 "Every layer whose stored-tile set **or index
content** this commit changes has its tile-index region re-emitted in full", and
§5.1's Example "A commit that changes a layer's stored-tile set or index content
re-emits that layer's whole tile-index region as well".

§3.1 is the term of art: "A tile is *stored in a generation* if and only if that
generation's tile-index entry for it is not the sentinel". Verified §20.4 uses the
strict sense where it matters — "Superseding a stored tile's bytes re-places that
layer's index region … and so modifying that layer's record" — a sentence that
would be redundant if a supersede changed the stored-tile set. So both Notes are
short of the rule, and §20.3's cost Note draws its 20 MB inference from a trigger
that its own example (editing one sample) does not fire.

Three commit shapes fall outside the §13.3 Note and inside the rule; I checked
each against §20.3 step 4:
(a) supersede-only — caught by "index content";
(b) a shrink changing entry_count — §20.3's shrink paragraph says so in terms,
    "`[R-CNT-17]` obliges the smaller entry_count and so a re-emitted index
    region";
(c) reader-01's ordinal renumbering at constant entry_count (extents (2,3) →
    (3,2), entry_count 6 both sides) — caught by §20.3 step 4's own parenthetical
    "(a geometry change renumbers ordinals wherever `[R-GEO-06]` moves them)".
Shape (c) is the one with teeth: a writer built from the Note alone emits a file
whose entries sit at wrong disk ordinals, structurally conforming, and §21.7
confirms [R-GEO-06] has no witness — every sample returned is wrong, silently.
That is not a fork between two defensible readings (the rule decides it) but it
IS the most expensive misreading in this batch, so the repair matters more than
"editorial" usually implies. Repair: restore "or index content" in §13.3 and
change "grows its extents so that" to "changes its extents so that"; in §20.3's
cost Note, restate the trigger as the rule states it.

### unwitnessed-obligations-account (writer-03 + register-04)

Decisive: §21.1 designates §21.7 as "the account, **by class**, of what fails
it", and §21.7's paragraph opens by naming the class — "A second set of
obligations is omitted from the register because a single file exhibits no
witness of their violation." A class account with worked examples is not an
inventory, and §21.1's normative completeness clause runs to *register rows*
("a *detectable* file-conformance violation this specification names and the
register omits is a defect in this document"), not to §21.7's citation list.

I checked writer-03's constructed file (skip [R-LIF-02] step 3, re-point the new
trailer at dir_n): the newly appended payloads are unreachable from the live
directory, so §5.2 makes them slack rather than structures, and [R-CNT-05]/F7 —
which bars a *structure* between the directory's end and the trailer — does not
bite. §9.2's own Note names the violation ("A writer that re-points a new trailer
at a prior generation's directory region has left step 3 unperformed") and §9.7
does not reconstruct history, so it is genuinely unwitnessed. That confirms the
class membership, not a gap in the register.

Not byte-level: every obligation in the family is *defined* by having no
byte-level witness, so file conformance ([R-CNF-02], "a pure predicate on bytes")
is identical either way. Real cost is a verifier author hunting for a check that
cannot exist ([R-WRT-05]'s byte-identical re-emission is the likeliest). Repair
is bookkeeping: add one clause marking the list illustrative, or name the
family — [R-CNT-08]'s updater clause, [R-WRT-05], [R-WRT-07], [R-WRT-08],
[R-WRT-03]/[R-WRT-09], [R-LIF-02] steps and step 3 — with [R-LIF-04]'s existing
treatment in §9.5's Note as the precedent for handling one elsewhere.

### appendix-a-local-vs-resident (diagrams-01)

Decisive: §6.1 [R-CNT-04], normative — "That distinction governs the request
accounting of §6.4 and nothing else; the obligation over the front block turns on
residency instead … **The test is residency, not transport.**" Appendix A is
labelled non-normative and self-corrects in the same sentence: "which
`[R-CNT-04]` requires of any reader holding them", and the next sentence works
the non-resident case explicitly. The over-binding is real — a local reader that
`pread`s only the tail is local and not resident, and §6.1 exempts it — but no
conforming file's verdict moves and the duty over-stated is verification, not
emission. Repair: write "a reader that holds bytes [0, 16)" for "a local reader".

### partial-slack-sum-vs-union (verifier-02)

Decisive, and it is in the sentence the reporter quotes: "A partial total is F
less the bytes claimed by the claimants the walk did enumerate — **an upper bound
on the file's true slack, never an under-count**". "The bytes claimed by X" names
a set of bytes, and only the union reading satisfies the qualification the same
clause imposes; reading A (sum of lengths) is provably not an upper bound, as the
reporter's own −415 shows. So the text decides it and this is not a live
ambiguity. It is a live *implementer trap* — `total -= len` is what the
accumulator loop writes — and the reporter's F33 witness is right that no discard
clause reaches a file-scope overlap (§5.2's discard is written for "a scope-level
rejection … L18's overlap or L40 through L42's placement", all layer scope).
Both verifiers report *nonconforming* either way, so no verdict and no byte
moves. Repair: "F less the size of the union of the byte ranges claimed by".

### file-scope-geometry-carve-out (register-01)

Decisive: the sentence immediately after the one quoted — "**Four rows are
outside that reasoning and do reach it**, because their subject is a field fixed
across every major (`[R-CNT-24]`): F8 and F1's trailer-magic instance, F14's
trailer CRC … and F6 with F1's front-block instance". Under the reporter's
reading (a) — "geometry" in the layer sense — the carve-out would range over zero
rows of a file-scope table and there would be nothing for four rows to be
"outside" of. The preamble's bookkeeping is exhaustive over all 36 rows (it even
handles F18 separately as "not an exception but a case outside the premise"), so
reading (b) is forced. §2.3 independently fixes the verdict for a foreign-major
file. The italicised *geometry* is nevertheless the only file-scoped use in 18
occurrences of the stem; repair is one word — "byte layout" or "structure".

### two-senses-of-F (register-02)

Decisive: §6.2's trailer table pins `committed_file_length | structural | = F`,
and [R-CNT-06] obliges "committed_file_length equals the file size … Any failure
is reject-file", validated in the same batch as the dir bounds. So in any file
that survives the open the two senses are the same number, and no accept/reject
verdict can turn on which is meant. §15.3 pins "with F the committed file length"
locally, §19.1 step 1 pins "the transport-authoritative file size F" locally, and
§21.1's "the rule governs" resolves F10/F32/L17 to their governing rules' sense.
What genuinely moves is a corpus manifest's row list on an already-nonconforming
file, which is register bookkeeping. Repair: one clause in §21.2's preamble.

### l23-detection-tier (register-03)

Decisive: §19.2 [R-RDR-02] — "**A reader MAY detect any violation earlier**
(`[R-CNF-12]`)". The *Detected* cell names the tier by which detection is due,
not the earliest permitted; §19.1 step 4's open-time determination is therefore
licensed, not contradicted. Outcome is reject-layer at either tier, F4 already
excludes such a record from the duplicate-name test ("both obtainable within
their records' inline_length"), and a reader that never touches the layer behaves
identically. Nothing to repair beyond, optionally, a cross-reference.

### commit-channel-set-and-rank (writer-06)

Not byte-level, and §21.7 says so in terms: "§20.3 step 4's bar on a declaration
change is witnessed only where the affected tiles remain stored". A dropped
planar channel's tiles leave the live state — their extents become slack — so
the output file is conforming under both readings and no verdict moves.

On the merits, the reporter overstates "never says". §20.3's carve-out gives a
*general* reason — "a tile the new state does not address carries no §14
obligation and its extent becomes slack" — and the parenthetical "(§11.2's grid
count falls)" names one instance of de-addressing, not the class. The bar's own
quantifier settles the surviving channels: their decoded size, padding set,
in-plane offsets, codec and filter are all untouched. What is genuinely absent is
any sentence saying that C and d are declarations a commit may change at all,
which is a maintainer decision rather than a reading. The reporter's combined
example (C=4,N=2 → C=2,N=4, entry_count fixed at 8, every surviving tile moving
from ordinal c·2+s to c·4+s) is the one shape that separates entry_count from its
factors, and §20.3 step 4's "index content" trigger does catch it — §11.1's
Rationale, keyed to entry_count, does not describe it, which is another reason
that Rationale should not be read as the rule.

### profile-* (writer-04, writer-05, diagrams-04)

Common decisive quote, Appendix G's opening: "It adds no requirement to any
actor: a writer ignoring it is fully conforming", reinforced by [R-CNF-05] —
"this specification does not promise canonical bytes, and two conforming writers
given identical input MAY produce different conforming files." Every file either
reading of the profile produces is conforming. The format's emittable set does
not move; a private profile's byte-identity promise does.

- **writer-04**: verified by walking the ten items against the closing sentence.
  Items 1/9 → "the producer pinning of items 1 and 9"; 2 → "a derived `file_id`";
  3 → gap content, gap extent, record and sub-record order; 4 → "a single
  generation"; 5 first half → "the absence or fixing of a declared alignment and
  slab"; 6 → "the sentinel for every all-fill tile"; 7 → "the fill a writer
  records when its caller chooses none"; 8 → "`version_minor` at its floor";
  10 → "NFC-normalized names". Item 5's second half, the fixed filter value, is
  the one member with no counterpart. The paragraph's disclaimer — "this
  paragraph names what they are for, not how many there are" — disclaims the
  count and undertakes the membership. Repair: add "; a fixed filter value, which
  `[R-COD-09]` leaves to the writer" to the list.
- **writer-05**: item 5 says the filter "changes the stored bytes of every tile
  it touches". [R-COD-10]: "for a packed boolean plane s = 1 and the filter is
  the identity", and the transform "byte i of group j at offset i · n + j"
  degenerates to the identity at s = 1 generally — every packed planar bool
  plane, every planar plane of a 1-byte channel (int8/uint8/bool), every
  interleaved layer with sample stride Q = 1. §20.3 step 4 relies on exactly this
  in *normative* text: "a filter whose mandated stride makes it the identity
  (`[R-COD-10]`)" is named as a change the declaration bar does not reach. So the
  appendix denies in a non-normative item what §20.3 asserts normatively. The
  item's conclusion survives by a mechanism it does not state — the layer
  record's filter field itself differs, 01 vs 02, and that is a byte. Repair:
  "it changes the stored bytes of every tile whose mandated stride exceeds 1, and
  the layer record's filter field in every case".
- **diagrams-04**: the sharpest form is that item 5 and the closing paragraph
  cannot both be right about what "the same input" fixes. If input = the logical
  arrays, the filter needs pinning (item 5 is doing work) but so do layout
  (§14.1 [R-SER-06] leaves interleaved and planar to the writer; the choice
  changes every tile's byte image *and* entry_count, N vs C·N) and tile extents
  (§11.3's Note: "Tile extents are a writer's choice, and this specification
  imposes none") — and "Everything else the profile needs is already mandatory"
  is false. If input = arrays plus the full declared schema, the paragraph is
  true but item 5's filter clause is pinning something input already fixed. Item
  2's parenthetical — "two files carrying the same arrays can legitimately differ
  in tiling, layout, and codec" — reads with the first. This is a maintainer
  decision, not a wording slip: either add layout and tiling to the profile, or
  state in the opening what "the same input" comprises.

### alignment-structural-transparency (reader-03)

Decisive: [R-IDX-03] in §15.3 — "Such an entry contributes no stored extent to
the *verifier* rows, **which bind over well-formed entries' extents only**". The
§15.3 table's verifier rows are three, and the third is "alignment or slab
invariant violated (§16)", so the exclusion reaches L40's per-tile alignment as
well as L41/L42's slabs. The "as it does over a sentinel — `[R-SLB-03]`" clause
is an illustration; "the verifier rows" is the operative quantifier. So the
document does settle it. What it does not do is say so in §16.1, where §16.2
says exactly this for its own invariant ("So are the entries §15.3 classifies
reject-tile on a *structural* ground: they address no usable extent, and the
run's stored tiles close over them"). Same twenty bytes are reject-tile (T10)
under either reading, so no conforming file's verdict moves; only the scope a
conformance vector records under [R-VEC-02]. Repair: mirror §16.2's sentence in
§16.1.

### recovery-rejected-count (quiz-01)

Decisive: §9.6 itself — "**no verdict turns on the probe**: … For a verifier the
probe is diagnosis — which commit state is recoverable — not a finding about the
file it was given", and "recovery output MUST be re-verified as a whole file
(§8) before being trusted". The count appears only in a recovery tool's report;
the candidate it settles on, which does decide recovered bytes, is fixed by the
CRC + length + re-verification requirements the disputed clause leaves alone.
The ambiguity is real — §9.6 calls a magic match a *candidate* and speaks of "the
nearest-to-end **valid** candidate", presupposing invalid ones, while the closing
sentence's grammatical subject is only "a candidate whose whole-file
re-verification fails". Two conforming tools report different counts for the same
torn file. Inert as to bytes. Repair: "how many candidates it rejected, counting
every 64-aligned magic match that failed any of the three tests".

## Count check

reader-01, reader-02, reader-03, writer-01, writer-02, writer-03, writer-04,
writer-05, writer-06, verifier-01, verifier-02, verifier-03, diagrams-01,
diagrams-02, diagrams-03, diagrams-04, register-01, register-02, register-03,
register-04, adversary-01, adversary-02, quiz-01, quiz-02, quiz-03 = 25 ids.
Group member counts: 5+4+1+1+1+1+1+1+1+1+1+1+1+1+2+1+1 = 25. No id repeated.
Byte-level groups: 1 (grid-times-tile-extent-overflow).
