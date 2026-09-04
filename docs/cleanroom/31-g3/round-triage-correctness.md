# Triage pass — correctness lens — cleanroom round 31

## What I read and ran

- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` — the whole
  file, lines 1–4791, in six Read calls.
- Three `grep`/`tr` commands, all confined to `spec/tarn.md`:
  1. `grep -n "tile extent" tarn.md | awk -F: '$1>=3070'` — to test writer-01's
     corroboration that §20 never mentions tile extents.
  2. `grep -c "fill bit in a packed plane"`, `grep -n "stored byte already holds the fill"`,
     and whitespace-normalised (`tr '\n' ' ' | tr -s ' '`) counts of both — to test
     diagrams-01's own grep note.
  3. Context extraction of the five byte-shaped carve-out phrasings and §23.1's
     lines 4217–4232.
- I did **not** open any walk transcript, did not list any directory, and did not
  read any other triage pass's notes. I opened nothing under
  `.../r31-round/out/`.

## Verification results before grading

**writer-01's corroboration holds.** `tile extent` at line ≥ 3070 occurs only at
3716 (F7), 3741 (F33), 3759 (L1), 3776 (L18), 3790 (L32) — all §21 register cells —
and at 4653/4656, Appendix G item 5. §20 (lines 3070–3609) contains no occurrence.
So §20 states no rule about a change to a layer's declared tile extents.

**diagrams-01's grep note is substantially right, its count slightly off.** Line-oriented
`grep` for `fill bit in a packed plane` returns 0 (confirmed). `stored byte already
holds the fill` returns 2 lines (3193, 3264); whitespace-normalised it returns 3 in
§20.3. §11.1's Rationale carries a fourth ("a new padding position whose stored
byte already holds the fill alters nothing", lines 1639–1640 — missed by the
normalising grep because of the blockquote `> ` prefixes), and §23.1 a fifth in
different words ("those bytes already hold the channel's recorded fill", line 4224).
Five byte-shaped occurrences, as the finding says; the "two of the four" aside is
the imprecise part and it does not bear on the finding.

**verifier-01's algebra holds.** The shuffle map `j·s + i -> i·n + j` is the identity
exactly when `s = 1` or `n = 1`: take `i = 1, j = 0` (forces `n = 1`) and `i = 0,
j = 1` (forces `s = 1`). For every layout `n = L/s = P`, so `n = 1` iff `P = ∏Tᵢ = 1`
iff every tile extent is 1, which `[R-GEO-01]`'s `Tᵢ ≥ 1` permits. `[R-COD-10]`
states the identity only for `s = 1` ("for a packed boolean plane s = 1 and the
filter is the identity"), so the carve-out's first limb — "a filter whose mandated
stride makes it the identity (`[R-COD-10]`)" — does not by its words reach the
`n = 1` case. Only the general test above the limbs does. Verified.

**writer-01's worked case recomputed independently.**
Interleaved, d = 2, E = (4,4), one uint8 channel, codec 1, filter 1.
- T = (4,1): G = (1,4), N = 4, P = 4, Q = 1, decoded size P·Q = 4, entry_count = N = 4,
  extent_length = 4·20 + ⌈4/2¹⁶⌉·4 = 84, offset of value k = k. 4 mod 4 = 0 and
  4 mod 1 = 0, so no padding positions.
- T = (1,4): G = (4,1), N = 4, P = 4, Q = 1, decoded size 4, entry_count 4,
  extent_length 84, offset of value k = k. 4 mod 1 = 0 and 4 mod 4 = 0, no padding.
- Coordinate map. Before: s = t₀·G₁ + t₁ = t₀·4 + t₁, and G₀ = 1 forces t₀ = 0, so
  t₁ = s; in-tile ordinal = u₀·T₁ + u₁ = u₀ (T₁ = 1 forces u₁ = 0). Value k of tile s
  is coordinate (k, s). After: G₁ = 1 forces t₁ = 0, so t₀ = s; in-tile ordinal =
  u₀·T₁ + u₁ = u₁ (T₀ = 1 forces u₀ = 0). Value k of tile s is coordinate (s, k).
  Twelve of sixteen positions move. The array is transposed.

Every item the §14 bar enumerates is unchanged: padding-position set (empty both
ways), pad bits (none — not a packed plane), `[R-SER-05]` content at both, decoded
size (4), byte offset of value k (k), sample type (uint8), codec and filter. The
disk-ordinal set is {0,1,2,3} both ways and no entry's bytes change, so `[R-CNT-17]`
is satisfied and §20.3 step 4 does not even oblige re-emitting the index region.
The resulting file is conforming: no §21 row applies, `[R-COD-04]`'s codec-1 equality
holds (length 4 = decoded size 4), and §21.7 leaves wrong content unwitnessed.

**adversary-03's worked case recomputed.** Planar C = 3 (a,b,c), N = 2, entry_count 6;
gen 1 stores only a's tiles, at disk ordinals 0 and 1. Removing b: c re-indexes
2 -> 1, its ordinals 4,5 -> 2,3; entry_count 4; extent_length 4·20 + 4 = 84. Permitted
— the ordinal bar reaches only "a tile the layer stores in the generation this commit
supersedes", and §20.3 says in terms "a commit that moves only the ordinals of channels
the superseded generation stored no tile for alters nothing this bars". No geometry
changed. Confirmed.

**diagrams-01's witness recomputed.** Planar, one bool channel, d = 1, T₀ = 16,
E₀ = 16: P = 16, G₀ = 1, N = 1, entry_count = C·N = 1, decoded size ⌈16/8⌉ = 2,
P mod 8 = 0 so no pad bits, E mod T = 0 so no padding positions. Shrink E₀ to 15:
G₀ = ⌈15/16⌉ = 1 still, entry_count 1, extent_length 24 — unchanged, so the index
region need not be re-emitted; P is a function of T alone, so decoded size is still
2; still no pad bits; in-tile ordinal 15 becomes a padding position and `[R-SER-05]`
requires its **bit** to be the fill bit, which it already is. Confirmed.

## Grouping decisions

**One group for four findings.** reader-01, writer-03, adversary-01 and quiz-02 all
locate the same defect: `[R-CNF-03]`'s acceptance-duty exclusion reads "no record of
a type it does not implement with MUST_UNDERSTAND = 1" with no placement qualifier,
while §21.6's closing paragraph calls the "top-level" qualifier load-bearing. Same
sentence, same repair, one group.

**writer-02 and verifier-01 are one group.** Both are about the growth paragraph
describing the carve-out as one mechanism after it was widened to two, and both
quote the identical sentence. verifier-01 adds the `n = 1` observation, which is a
corroboration of the same defect rather than a second one.

**diagrams-01 stays separate from that group** although it also concerns the §14
bar's carve-out. Its defect is that the carve-out is worded over *bytes* where a
packed plane's padding content is a *bit*; the repair is a different word in three
places. Distinct defect, distinct repair.

Everything else is one finding to a group.

## Byte-level judgements, and the text behind each downgrade

The test I applied throughout is the house discriminator the reporters themselves
use: **is the disputed file itself conforming, and does only one reading permit a
conforming actor to produce it (or oblige a reader to accept or reject it)?**

### Upheld byte-level: writer-01

The disputed file — prior generation plus a commit whose only change is the two
tile-extent `u64` fields of one layer record — is fully conforming, and nothing any
actor is obliged to check separates it from a file whose bytes really were stored
under the new tiling (§21.7). So `[R-WRT-04]`'s §14 bar is the only thing that can
forbid producing it, and the bar's reach is genuinely disputable:

> "A commit MUST NOT change a layer's declarations in a way that alters, for any tile
> that layer stores **in the generation this commit supersedes**, what §14 fixes for
> its stored bytes or how they decode"

§14's own heading states its subject: "This section defines the **decoded tile
image**: the byte sequence a stored tile's payload decodes to". The decoded tile
image, its length, its per-value offsets, its sample types and its value-sequence
order are all unchanged under the permutation. The map from in-tile ordinal to
*coordinate* lives in §11.4 `[R-GEO-06]` and §11.3, which §14.1 cites rather than
states. So an updater reading "what §14 fixes for its stored bytes" at its word
concludes nothing §14 fixes has moved, and commits. An updater reading §14.1's "the
tile at spatial ordinal s carries all C channels at **the tile's P positions**" as
including *which* positions those are concludes the bar reaches it, and refuses.

I looked for a sentence that decides this and did not find one. The candidates and
why each fails:

- "The test is the effect on such a tile, and the list names where that effect
  arises rather than standing on its own" — this refutes taking the enumerated list
  as the test, which is writer-01's framing of reading (A), but it does not tell you
  whether the *general* test reaches a coordinate relabelling. Both disputants can
  quote it.
- §20.3 works the parallel question through for a channel's declared sample type —
  "the type is what fixes the value a stored bit pattern denotes, so under a new one
  the same bytes denote different values" — and never applies the same reasoning to
  the tile extents, which fix the coordinate a stored byte denotes.
- Appendix G item 5 knows tile extents are load-bearing ("the tile extents fix every
  tile's shape and with it the grid count") but Appendix G is non-normative.
- §20.3's permissions are stated for growth, shrink, planar channel reordering and
  re-typing. A tile-extent permutation at constant ∏Tᵢ is none of those, and no
  contrapositive is stated for the "A layer that stores no tile ... MAY be re-declared
  freely" permission.
- `[R-WRT-07]`'s reference-array preservation binds a **compactor** only; no commit
  rule preserves the reference array.

I confirmed mechanically that §20 (lines 3070–3609) never uses the phrase "tile
extent". So the gap is a silence, not a decided question, and the two readings emit
different byte sequences. **Byte-level: yes.**

Where writer-01 is imprecise: its reading (A) as stated ("the enumerated list is the
test") *is* refuted by the not-standing-on-its-own sentence, and writer-01 says so
itself. The live fork is narrower and stronger than its framing — it is over the
scope of "what §14 fixes for its stored bytes", not over whether the list is
exhaustive. Graded CONFIRMED because the finding's own body states that narrower
fork explicitly.

### Downgrades, each with the sentence that decides it

**`[R-CNF-03]`'s missing "top-level" (reader-01, writer-03, adversary-01, quiz-02).**
The defect is real — the quotations are accurate and in context. It is not byte-level
because the file-level verdict is fixed twice over:

> `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer, and where the
> file is otherwise conforming a reader MUST NOT reject the file for it"

> §21.6: "the same type as a layer sub-record is reject-layer and **never a ground to
> refuse the file** (`[R-CNT-18]`), so only the top-level case is a file a reader
> refuses"

Both unconditional, both normative (§21.6's closing paragraph carries no *Note*,
*Example* or *Rationale* label).

**The premise my downgrade rests on, stated so it can be attacked:** that "refuse
the file" in §21.6 reaches a reader which opens the file and then declines to serve
any layer of it, and not only a reader that reports reject-file in §2.4's vocabulary.
reader-01 isolates exactly this residue: `[R-CNF-03]` is the only source of the
positive duty to serve, and reading (a) withdraws it wholesale, leaving a reader
free to open a conforming file and serve nothing without ever "rejecting" it. If a
maintainer reads "refuse the file" narrowly — as reject-file only — then reading (a)
lets a conforming reader decline a byte sequence that reading (b) obliges it to
accept, and the group becomes byte-level. I judge the broad reading correct because
§2.4's reject-layer entry ("all other layers are unaffected"), `[R-VEC-04]`'s pairing
of a damaged scope with "the content a reader that serves anything at all owes", and
§21.6's own "never a ground to refuse the file" all treat serve-nothing as the thing
being excluded. But this is the group I would put money on a later phase attacking,
and I am naming it rather than burying it.

**Growth paragraph understates the carve-out (writer-02, verifier-01).** Decided by
the definitional sentence three paragraphs above, in the same numbered step:

> "The test is the effect on such a tile, and the list names where that effect arises
> rather than standing on its own: a change that leaves every one of those tiles'
> stored bytes meaning exactly what they meant — **a filter whose mandated stride
> makes it the identity (`[R-COD-10]`), or a new padding position whose stored byte
> already holds the fill `[R-SER-05]` fixes** — is not what this bars."

Premise: that a sentence opening "The bar's carve-out does not reach a growth:" is
read as answering the growth question with the limb relevant to it, not as
redefining the carve-out's extent — and that a definitional sentence governs its own
extent against a later gloss. Attackable by anyone who holds that a later normative
sentence in the same requirement narrows an earlier one. Note the shrink paragraph
gets this right ("its carve-out included — a new padding position ... is not one"),
which is evidence the growth sentence is a stale neighbour rather than a narrowing.

**Byte-worded carve-out vs a packed plane's fill bit (diagrams-01).** Decided by what
the carve-out points at. `[R-SER-05]`, which the carve-out cites by identifier,
enumerates the three representations itself:

> "at every padding position, a writer MUST encode, for each channel the position
> carries, that channel's fill value — the recorded fill bytes for a numeric channel,
> the recorded fill byte for an interleaved bool channel, **the fill bit in a packed
> plane**."

So "whose stored byte already holds the fill `[R-SER-05]` fixes" reads as "whose
stored byte already holds the fill `[R-SER-05]` fixes *at that position*" — which in
a packed plane is a bit inside that byte. Combined with "the list names where that
effect arises rather than standing on its own", reading R2 requires taking an
illustration as the rule against an express instruction not to. Premise: that the
carve-out's citation of `[R-SER-05]` imports `[R-SER-05]`'s own per-representation
enumeration. Attackable if one holds the carve-out states an independent
byte-shaped condition the packed case simply cannot satisfy.

**Partial-slack-total's two enumerated causes (verifier-02).** The finding is accurate:
§5.2 and §9.7 both name exactly two causes and a resource decline under `[R-ERR-04]`
is a third that is neither a rejection ("a refusal on resource grounds MUST be
reported as a resource limit and not as a validity error") nor an election to stop
at a violation. Not byte-level: the same two general statements of the obligation
name no causes at all —

> §21.6: "counted and reported by a verifier — as a partial total — an upper bound
> naming what stopped the walk — **where its walk did not complete**"

— the disputed file is conforming under both readings, and §2.4's Note puts the
whole subject outside reader obligations: "Coverage is checked by verifiers, never
by readers."

**Trailer table's flags cell (diagrams-02).** Verified: of the ten rows, only flags
gives a decomposition where the others give a value or a value set. Not byte-level —
`[R-CNT-06]` names "the flag gates (§6.3)" in its ordered validation and §21.2's F19
registers the condition, so no verdict is left open.

**§21.6 zero-layers cell (diagrams-03).** Verified against `[R-CNT-14]`, which makes
two statements the cell fuses. Decided by §21.1 in terms:

> "§21.6's entries restate their governing rules on the same terms a row does, and
> where such an entry and the rule it cites diverge, **the rule governs** there too."

**§13.3's sparse-writing Note (diagrams-04).** Both omitted commits verified against
§20.3 ("`[R-CNT-17]` obliges the smaller entry_count and so a re-emitted index
region"; "a commit that moves only the ordinals of channels the superseded
generation stored no tile for alters nothing this bars"). Not byte-level: the block
is labelled *Note* and `[R-CNF-01]` exempts labelled Notes from normativity, while
§20.3 step 4 and `[R-CNT-17]` state the obligation.

**Three-shapes figure and a drop-only commit (diagrams-05) — PARTIAL.** §20.4's
licence and the constructibility of the case check out. But the finding's central
claim — that shape (c)'s own exclusion test rules the drop out of (c) — does not
survive reading (c). The exclusion is stated of one operation and turns on one fact:

> "Editing user metadata is not this shape: its document lives in an extent
> (`[R-CNT-25]`), so **a new extent is appended** and the old one becomes slack, as
> in (b)."

A drop appends no extent, so the exclusion does not reach it, and the drop satisfies
(c)'s own heading and body — "A change confined to the directory ... Only the
directory is re-emitted." What is actually incomplete is the *diagram*: (c)'s
"after" row hatches only the old dir/pad/trailer and draws no hatched run where the
dropped extent was. Right observation, wrong reason; the taxonomy is not short a
shape.

**Appendix H's missing flags obligation (diagrams-06).** All five cited restatement
sites verified word for word (§2.3 `[R-CNF-02]`, §6.3 `[R-CNT-08]`, §20.3 step 6,
§20.5 `[R-WRT-06]`, Appendix G item 8) and Appendix H's writer and updater entries
carry nothing. Not byte-level: Appendix H disclaims its own authority — "each
entry's authority is the requirement or section cited, never this summary" — and
§6.3 states the obligation plainly.

**`[R-ERR-04]`'s decline scopes (register-01).** The divergence is real:
`[R-ERR-04]` enumerates "the whole file, or ... the narrowest scope whose stated or
derived quantities exceed what it can serve", §21.9's per-instance paragraph puts a
frame's `Window_Size` in the tile ("compressed frames a file actually contains,
neither of which exists except as stored bytes"), and yet `[R-COD-06]` licenses
declining "the tile **or the layer**" and `[R-CNF-11]` names "a layer's or a tile's
decode". But the reporter's decisive support does not do the work it claims: §18.2's
"it MAY instead decline the whole file" offers exactly what reading (a) already
allows (narrowest, or whole file), so it is no evidence for reading (b). The real
reason this is not byte-level is stronger than the reporter's: `[R-ERR-04]` states a
**MAY**, and once a quantity exceeds a guarantee `[R-CNF-03]`'s duty has lapsed —

> "A reader MUST accept every conforming file ... **none of whose values exceeds the
> minimum guarantees** of §21's limits table"

— so no MUST is broken by an over-broad decline under either reading, and the file
is conforming under both. The divergence is diagnostic only.

**§21.9's lz4 hard-limit restatement (register-02).** Verified: `[R-COD-07]`, its
Note, L44 and §21.9's per-instance paragraph all carry the "addressed tiles"
quantifier; only §21.9's hard-limit clause drops it, along with the planar
largest-plane rule. Not byte-level because the paragraph disclaims its own authority
twice:

> "The hard limits it restates are **a finding aid rather than an inventory** — each
> is normative where the structure forcing it is defined" and "They are stated where
> the structures forcing them are defined".

**§21.6's under-cited experimental-type entry (register-03).** Verified: the entry's
Defined-behavior cell names L25, a sub-record row, while its Rule cell cites only
`[R-CNT-15]` (whose text is "An unknown record type **at file scope**") and
`[R-WRT-08]`. `[R-CNT-18]` supplies the sub-record half and §10.3 keeps the pair
apart. Not byte-level: both rules assign MU = 0 the same ignore-record outcome, and
§21.1's rule-governs clause covers the entry.

**§11.1's Rationale on growth (adversary-02).** Verified: the block asserts the §14
bar reaches a growth, gives three carve-outs, and never states §20.3's express
growth permission ("an extent MAY **grow**, since a position that becomes real
held ... that channel's fill (§14.5), and fill is a legal sample value"). Not
byte-level: the block is labelled *Rationale* (`[R-CNF-01]`) and defers in its own
first sentence — "§20.3 states normatively, and governs".

**Renumbering parenthetical (adversary-03).** Verified, including the document's own
self-description "whose only stated occasion for a renumbering is a geometry change",
which is now inaccurate. Not byte-level, and adversary-03's reasoning is sound and
worth restating: reading (b) is unsatisfiable on the worked case (entry_count falls
6 -> 4, so ordinals 4 and 5 do not exist to keep entries at), and wherever both
readings are satisfiable the moved entries belong to channels the superseded
generation stored no tile for — whose entries are therefore sentinels by §3.1's
definition of *stored* — so they are byte-identical wherever they land. I checked the
one case that could break this: a **malformed** non-sentinel entry makes its tile
*stored* under §3.1 ("not the sentinel"), so moving that channel is barred by the
ordinal bar and never reaches the disputed clause.

**"such a tile" (adversary-04).** The demonstrative is loose; reading (a) is decided
by the explicit back-pointer and the shrink paragraph it points at:

> "**As there**, de-addressing rescues nothing" — and there: "but neither does it
> rescue a commit that damages **a prior-generation stored tile**."

Reading (b) makes the sentence bar what the clause immediately before it permits.
I did **not** rely on adversary-04's second rationale ("both bars govern an updater's
commit, not a file"), which is too broad — taken generally it would also defeat
writer-01's flag, and the byte-level test asks what a conforming implementation may
*emit*, not only what a verifier can establish.

**`[R-SER-08]`'s returned byte (adversary-05).** The finding is accurate and the
aside is too: §19.4 step 8 and §21.1 both say "the one byte" where 254 bytes are
excluded, while §12.3's "the one case" is the accurate form. Not byte-level — the
disputed file is nonconforming (T2 registers it), both readers accept it, and the
return encoding is decided by assembling `[R-TYP-04]` with §14.2:

> `[R-TYP-04]`: "Wherever this specification treats two sample or fill values as the
> same value, **it means their encoded bytes are identical**"

with §14.2's "0x00 = false, 0x01 = true", and §21.1's "it **resolves** a nonconforming
interleaved boolean byte to a value rather than serving it through". Reporting *true*
is therefore returning 0x01.

**Two senses of "relies on" (quiz-01).** The collision is real: `[R-WRT-03]` says
"re-emission (§20.4) relies on every directory byte" while step 2 applies
`[R-WRT-01]`'s "neither modifies nor relies on" shelter to "a record re-emitted
byte-identically". Not byte-level by the house discriminator: the disputed output
file — a generation whose directory re-emits a record carrying a register-row
violation — is **nonconforming under both readings**, so no conforming byte
sequence's status moves and no reader or verifier verdict differs. What forks is
whether one actor performs the operation, and step 2 answers that in terms ("An
appender that carries a violation forward SHOULD report it"). This is where my
grading of writer-01 and quiz-01 diverge on purpose: writer-01's disputed file is
**conforming** and only one reading lets a conforming actor produce it; quiz-01's is
nonconforming either way.

**Preservation table keyed to "Stored flags" (quiz-03).** Verified: the column
heading is "Stored flags" and the introducing clause is scoped to one of three cases.
Decided by the lead sentence, which is express rather than implicit:

> "**Persistence governs every record type**; only the authoritative source of the
> flags differs."

Premise: that "governs every record type" reaches the obligations in the table and
not merely the concept of persistence. Attackable, but the sentence exists precisely
to carry the table to the other two cases, and the class in dispute (an unregistered
type an updater implements from an outside definition) is one this specification does
not define.

**§22.3's doubled recovery trigger (quiz-04).** Verified verbatim: "which is why
recovery output is re-verified as a whole file before being trusted (`[R-LIF-06]`)
**before any use**" — the trailing phrase attaches to nothing — followed three
clauses later by a third wording of the same obligation. Normative text (§22.3
carries no label). Not byte-level: `[R-LIF-06]` states it once and cleanly —
"recovery output MUST be re-verified as a whole file (§8) before being trusted" —
and §9.6 places the recovery scan outside conforming reader behaviour entirely.

## Coverage

24 input ids, 20 groups, each id in exactly one group:
cnf03 group (4): reader-01, writer-03, adversary-01, quiz-02.
Singletons (18): writer-01, diagrams-01, verifier-02, diagrams-02, diagrams-03,
diagrams-04, diagrams-05, diagrams-06, register-01, register-02, register-03,
adversary-02, adversary-03, adversary-04, adversary-05, quiz-01, quiz-03, quiz-04.
Pair (2): writer-02, verifier-01.
4 + 18 + 2 = 24. Counted, not asserted.

One byte-level group upheld: writer-01.
