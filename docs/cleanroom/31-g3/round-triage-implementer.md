# Triage pass — implementer-consequence lens — cleanroom round 31

## Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, in full, in
sequential chunks (lines 1–3400 read directly; 3400–4100 partly via
persisted tool output where a chunk exceeded the inline cap, then re-read
in narrower ranges 3400–3700 and 3880–4093; 4093–4790 read directly).
Two persisted tool-output files were written by the Bash tool itself when
a `sed` range exceeded the inline cap; I read the §21.2/§21.3 register rows
only through targeted `grep`, not in full.

Ran three greps over `spec/tarn.md`:

- `grep -n "tile extent"` with a filter for line ≥ 3070 (start of §20) — to
  test writer-01's corroboration that §20 never mentions tile extents.
- `grep -n "re-declared freely\|MAY be re-declared\|declared tile extents\|change.*tile extent\|tile extents.*chang"` —
  to test whether any rule anywhere constrains a change to declared tile extents.
- `grep -n "^#### 21\.\|^### 2[0-9]\|^## \|^### Appendix"` — section boundaries.

Did NOT read: any walk transcript in `r31-round/out/`; any other triage
pass's notes; `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`,
`spec/registry.json`, git history, the web. I did not list any directory
in `r31-round/`; the only directory operation was `mkdir -p` on my own
output path.

No input finding was left unevaluated.

---

## Grouping

24 input ids → 20 groups. Every id in exactly one group.

| group | members |
|---|---|
| acceptance-duty-omits-top-level | reader-01, writer-03, adversary-01, quiz-02 |
| bar-misses-tile-extent-permutation | writer-01 |
| growth-gloss-drops-filter-limb | writer-02, verifier-01 |
| carve-out-worded-over-bytes-not-bits | diagrams-01 |
| trailer-table-flags-cell-no-values | diagrams-02 |
| zero-layers-entry-fuses-empty-directory | diagrams-03 |
| sparse-note-keys-reemission-to-growth | diagrams-04 |
| three-shapes-figure-and-pe0-drop | diagrams-05 |
| appendix-h-omits-flags-obligation | diagrams-06 |
| err04-decline-scope-enumeration | register-01 |
| lz4-cap-restatement-drops-quantifier | register-02 |
| experimental-type-entry-undercited | register-03 |
| geo-rationale-omits-growth-permission | adversary-02 |
| renumbering-parenthetical-incomplete | adversary-03 |
| such-a-tile-antecedent | adversary-04 |
| ser08-returned-encoding-and-one-byte | adversary-05 |
| partial-total-causes-omit-resource-decline | verifier-02 |
| relies-on-two-senses | quiz-01 |
| preservation-table-keyed-to-stored-flags | quiz-03 |
| doubled-reverification-trigger | quiz-04 |

Merge rationale for the four-member group: reader-01, writer-03,
adversary-01 and quiz-02 all report that [R-CNF-03]'s acceptance-duty
exclusion is stated over "record" with no placement qualifier while
§21.6's closing paragraph calls the "top-level" qualifier load-bearing.
adversary-01 additionally names §21.9's restatement ("an unimplemented
MU = 1 type"), which is the same omission at a second site and is repaired
by the same edit. reader-01's "residue" (whether the reader owes service on
undamaged layers) is not a separate defect — it is the consequence of the
same omitted qualifier.

Merge rationale for the two-member group: writer-02 and verifier-01 both
report that §20.3's growth paragraph glosses the §14 bar's carve-out as
single-membered after it was widened to two limbs. verifier-01 adds the
n = 1 (all tile extents 1) class where neither named limb reaches by its
own words — supporting detail on the same defect, not a second one.

I did NOT merge writer-01 with writer-02/verifier-01/diagrams-01 even
though all four sit in §20.3 step 4. They are three distinct repairs:
what the bar *reaches* (writer-01), how a downstream sentence *describes*
the carve-out (writer-02/verifier-01), and the *granularity* the carve-out
is worded at (diagrams-01).

---

## Verifications performed against the document

### writer-01's witness, recomputed from the spec

Layer: interleaved, rank 2, E = (4,4), one uint8 channel, codec 1, filter 1.

T = (4,1): G = (⌈4/4⌉, ⌈4/1⌉) = (1,4) [§11.2]; N = ∏Gᵢ = 4; P = ∏Tᵢ = 4;
Q = 1; decoded size = P·Q = 4 [§14.2]; entry_count = N = 4 [§11.2];
extent_length = 4·20 + ⌈4/2¹⁶⌉·4 = 84 [R-CNT-17]; offset of value k = k·1
[§14.2, interleaved row with C = 1]. Padding positions: 4 mod 4 = 0,
4 mod 1 = 0 → none [§11.3].

T = (1,4): G = (4,1); N = 4; P = 4; Q = 1; decoded size 4; entry_count 4;
extent_length 84; offset of value k = k. Padding: 4 mod 1 = 0, 4 mod 4 = 0
→ none.

So every enumerated item of the §14 bar is unchanged, in both directions.

Coordinate map [R-GEO-06]. Before (T = (4,1)): t₀ = x₀ div 4 = 0,
t₁ = x₁ div 1 = x₁; s = t₀·G₁ + t₁ = x₁. In-tile ordinal
= u₀·T₁ + u₁ = (x₀ mod 4)·1 + (x₁ mod 1) = x₀. So byte (s, k) ↔ (x₀, x₁) = (k, s).

After (T = (1,4)): t₀ = x₀, t₁ = 0; s = t₀·G₁ + t₁ = x₀. In-tile ordinal
= u₀·T₁ + u₁ = 0·4 + (x₁ mod 4) = x₁. So byte (s, k) ↔ (x₀, x₁) = (s, k).

The array is transposed. Twelve of sixteen byte positions change meaning.
Confirmed by computation, not by accepting the reporter's account.

Index re-emission: the stored-tile set is {0,1,2,3} both ways and every
entry is byte-identical, so §20.3 step 4's "Every layer whose stored-tile
set or index content this commit changes" is not triggered. Directory-only
commit. Confirmed.

Corroboration grep: `grep -n "tile extent"` returns 23 hits; every one at
line ≥ 3070 (i.e. §20 onward) is a §21 register-table cell (F7, F33, L1,
L18, L32) or Appendix G item 5 (lines 4653, 4656). §20 itself — lines
3070–3609 — contains no occurrence. Confirmed.

Second grep: no sentence anywhere constrains a change to declared tile
extents on a layer that stored tiles. The three hits for "re-declared
freely" are all the *permission* for a layer that stored nothing.

### verifier-01's identity-filter algebra

[R-COD-10]: the shuffle maps byte i of group j from offset j·s + i to
offset i·n + j, with n = L/s. Identity ⟺ j·s + i = i·n + j for all
i < s, j < n. Take i = 1, j = 0 → 1 = n. Take i = 0, j = 1 → s = 1. So
identity ⟺ s = 1 or n = 1. n = 1 means L = s, which for a planar numeric
channel (L = P·Bᶜ, s = Bᶜ) means P = 1, i.e. every Tᵢ = 1 — legal, since
[R-GEO-01] requires only Tᵢ ≥ 1. Confirmed.

### diagrams-01's packed-plane witness

Planar, one bool channel, d = 1, T₀ = 16, E₀ = 16. P = 16, G₀ = 1, N = 1,
entry_count = C·N = 1, decoded size ⌈16/8⌉ = 2 [§14.3], P mod 8 = 0 so no
pad bits, E mod T = 0 so no padding positions. Shrink E₀ to 15: G₀ =
⌈15/16⌉ = 1 still, so N = 1, entry_count 1, extent_length 24 — all
unchanged; P still 16 (P is ∏Tᵢ, not a function of E), decoded size still
2, still no pad bits. In-tile ordinal 15 now has coordinate 15 ≥ E₀ = 15,
so it becomes a padding position, and [R-SER-05] now requires its *bit* to
be the fill bit. Confirmed.

### adversary-03's channel-removal witness

Planar C = 3 (a, b, c), N = 2, entry_count 6. Remove b: c re-indexes 2 → 1,
its ordinals move 4,5 → 2,3. entry_count 4, extent_length 4·20 + 4 = 84
[R-CNT-17]. Under reading (b) the surviving entries must stay at positions
4 and 5, which no longer exist — unsatisfiable. Every moved entry is a
sentinel (`FF ×16 00 ×4`), byte-identical wherever it lands, so the emitted
region is the same under either satisfiable reading. Confirmed.

### diagrams-02's table row

§6.2's ten rows: magic gives its eight bytes; version_major "1 (0 invalid;
others: §6.3)"; version_minor "any (see §6.3)"; dir_offset "≥ 16";
dir_length "≥ 4; dir_offset + dir_length ≤ F − 64"; committed_file_length
"= F; multiple of 64"; file_id "≠ 0"; reserved "zero"; trailer CRC its
covered range. flags: "bits 0–15 incompat lane; bits 16–31 ignore lane
(§6.3)". Confirmed — the flags cell alone gives a decomposition, not a
value set.

### adversary-01's second site

§21.9 [R-ERR-04]: "the two capability refusals §21.6's closing paragraph
names, a foreign format major and an unimplemented MU = 1 type, are not
this ground". Unqualified. Confirmed as a second occurrence of the same
omission.

---

## Judgements, with the quotation behind every downgrade

### 1. acceptance-duty-omits-top-level — CONFIRMED, not byte-level, editorial

Members: reader-01, writer-03, adversary-01, quiz-02.

The defect is real: [R-CNF-03] withdraws the acceptance duty for a file
"carrying no record of a type it does not implement with
MUST_UNDERSTAND = 1", with no placement qualifier, while §21.6 says
"The qualifier is load-bearing — the same type as a layer sub-record is
reject-layer and never a ground to refuse the file (`[R-CNT-18]`), so only
the top-level case is a file a reader refuses". §7.2 frames sub-records as
records and §7.4 calls them records, so the clause reaches both scopes.

Downgrade quotation, §7.4 [R-CNT-18]:

> an unknown sub-record type with MU = 1 is reject-layer, and where the
> file is otherwise conforming a reader MUST NOT reject the file for it

That is unconditional and it is the accept/reject verdict on the disputed
byte sequence. Withdrawing a duty is not granting a permission, so no
conforming reader may refuse the file under either reading.

reader-01's residue — whether a reader that opens the file owes service on
its undamaged layers, [R-CNF-03] being the only source of that duty — is
answered by a second sentence the reporter did not cite, §2.4's outcome
table:

> **reject-layer** | The affected layer's data and metadata are not
> usable; all other layers are unaffected.

and [R-CNF-04]'s "A reader MUST detect every violation the error register
(§21) assigns to the reader as its detector, and apply the outcome class
this specification assigns to each". A reader that declines every layer is
not applying reject-layer. So the residue does not fork either.

Premise of my downgrade, stated so it can be attacked: I take
[R-CNT-18]'s MUST NOT to bind independently of [R-CNF-03], i.e. that a
reader's permission to reject is never inferred from the absence of a duty
to accept. If someone held instead that [R-CNF-03] is the *exhaustive*
statement of what a reader must take, and that a file outside it is a file
a reader may decline whatever [R-CNT-18] says elsewhere, then the two
readings would fork the accept/reject verdict and this would be byte-level.
I reject that because [R-CNT-18] is an express MUST NOT on the file-level
move, not a silence.

Implementer consequence, both sides concretely: implementation R1 builds
its acceptance duty from §2.3 alone, meets a conforming file whose only
unimplemented MU = 1 record is a layer sub-record, and returns
"unsupported record type — file rejected". Implementation R2 opens the
file, marks that one layer rejected, and serves the rest. R1 is
nonconforming — [R-CNT-18] forbids exactly what it did — so this is one
implementation being wrong, not two being permitted. §2.3 is the section
the document itself calls "worth reading first", which is what makes the
mistake likely rather than exotic.

Repair: insert "top-level" into [R-CNF-03]'s exclusion, and into §21.9's
"an unimplemented MU = 1 type".

### 2. bar-misses-tile-extent-permutation — CONFIRMED, **BYTE-LEVEL**

Member: writer-01.

I could not find a sentence that decides this, and I looked for one.

The bar: "A commit MUST NOT change a layer's declarations in a way that
alters, for any tile that layer stores **in the generation this commit
supersedes**, what §14 fixes for its stored bytes or how they decode —
[six-item list] — ... Call this the **§14 bar**." Then: "The test is the
effect on such a tile, and the list names where that effect arises rather
than standing on its own: a change that leaves every one of those tiles'
stored bytes meaning exactly what they meant — [two carve-outs] — is not
what this bars."

Reading (A). "What §14 fixes for its stored bytes or how they decode" is
the §14 byte-layout arithmetic: which value of the value sequence lies at
which byte offset, at what element size, under what codec and filter. In
the witness every one of those is unchanged, because P, Q, C, the type,
the codec and the filter are all unchanged. The map from in-tile ordinal
to *coordinate*, and from tile coordinates to *spatial ordinal*, is
[R-GEO-06]'s and §11.4's — not §14's. The bar names §14 and does not name
§11.4. The carve-out states a sufficient condition for permission; its
contrapositive is nowhere stated, so failing it does not entail the bar.
On (A) the commit is permitted.

Reading (B). §14.1 [R-SER-01] says the interleaved "tile at spatial
ordinal s carries all C channels at the tile's P positions", and which
positions those are is a function of T. So §14 does fix something about
these stored bytes that the permutation alters, and the general test —
"a change that leaves every one of those tiles' stored bytes meaning
exactly what they meant" — is failed. On (B) the commit is barred and the
operation is a new layer or a whole-file rewrite.

Both readings are supported by text and neither is refuted by any. The
governing sentence tells you the list does not stand on its own; it does
not tell you that the test reaches beyond §14 into §11.4, and the bar's
own noun is "§14".

Byte-level under the stated test. Updater U1 (reading A) is told to
re-tile layer `sst` from (4,1) to (1,4) and emits a commit: the appended
directory carries that layer record with its two tile-extent u64 fields
swapped, plus a pad and a trailer. Nothing else moves — not one index
entry, not one payload byte. The resulting file is conforming: every
register row is satisfied, [R-CNT-17]'s 84 holds, [R-COD-04]'s
length-equals-decoded-size holds at 4, every checksum verifies. Updater U2
(reading B) refuses and writes a new layer or a fresh-file_id rewrite —
different bytes. So the *emittable set of a conforming updater* differs
between the readings on a file that is itself conforming. That is the
byte-level test met exactly.

Unwitnessed by construction, which is what makes it expensive rather than
academic. §21.7: this format "detects *corruption of structure*, not
*incorrectness of content*". Nothing in the file records which generation
it superseded, §9.7 does not reconstruct history, and the transposed file
is byte-indistinguishable from a file whose bytes really were written
under the new tiling. Every checksum in §8 certifies the result. The §14
bar is the only thing standing between an updater and the transpose; if
it does not reach, nothing does.

Corroboration that §20 does not address it separately: §20 contains no
occurrence of "tile extent" (grep, lines 3070–3609). §20.3 reasons
explicitly about a channel's declared *type* — "the type is what fixes the
value a stored bit pattern denotes, so under a new one the same bytes
denote different values" — and never runs the same argument for the tile
extents, which fix the *coordinate* a stored byte denotes. Appendix G item
5 knows they are load-bearing ("the tile extents fix every tile's shape
and with it the grid count") but is non-normative and is about
reproducibility, not about commits. §20.3's growth and shrink permissions
are stated over dimension extents E, not tile extents T.

Implementer consequence, both sides concretely: team A ships
`tarn append --retile sst 1x4` in its appender, on the strength of the
enumerated list, because nothing on that list changes; every array it
touches is silently transposed and every verifier certifies the result.
Team B's appender refuses the same request and forces a whole-file
rewrite. Only one of the two files exists on disk afterwards, and the
document does not say which.

The same gap reaches a reordering of a layer's dimension entries, which
permutes T and the declared dimension order together and transposes by the
same mechanism, and the repair should cover it.

Repair (an edit, not a maintainer decision): extend the §14 bar's subject
from "what §14 fixes for its stored bytes or how they decode" to what §14
*and §11.3–§11.4* fix — i.e. name the tile extents and the declared
dimension order alongside the sample type as declarations a commit may not
change while the layer stores a tile, since they fix the coordinate a
stored byte denotes exactly as the type fixes the value it denotes. The
cleanest form is to state the contrapositive of the carve-out as the rule:
a commit MUST NOT change a layer's declarations in a way that makes any
stored byte of a prior-generation stored tile denote a different value at
a different coordinate.

### 3. growth-gloss-drops-filter-limb — CONFIRMED, not byte-level, editorial

Members: writer-02, verifier-01.

The gloss: "The bar's carve-out does not reach a growth: it covers a
position whose stored byte already holds the fill it keeps, not one that
ceases to be padding, so this is an exception the permission states rather
than one the carve-out supplies." Read as a definition, the carve-out has
one limb and a filter-declaration change is barred wherever the layer
stores any tile — even where [R-COD-10]'s mandated stride makes the
permutation the identity for every one of them.

Downgrade quotation, §20.3 step 4, two paragraphs above, in the same
numbered step:

> The test is the effect on such a tile, and the list names where that
> effect arises rather than standing on its own: a change that leaves
> every one of those tiles' stored bytes meaning exactly what they meant —
> a filter whose mandated stride makes it the identity (`[R-COD-10]`), or
> a new padding position whose stored byte already holds the fill
> `[R-SER-05]` fixes — is not what this bars.

Both limbs, stated primarily, with an express instruction that the
enumeration does not stand on its own. A gloss three paragraphs downstream
whose only job is to answer "does the carve-out reach a growth?" cannot
narrow it.

Premise of my downgrade, stated so it can be attacked: I take a general
statement of a rule, expressly flagged as not standing on its own, to
govern a later narrower gloss in the same numbered step. If someone
instead read the later, more specific sentence as the operative one — it
is normative text, it is not labelled, and "it covers X, not Y" is
definitional in form — reading (A) revives, and the fork would then be
byte-level, since it decides whether a conforming updater may emit a
directory-only filter-change commit or must instead write a fresh-file_id
rewrite. I judge the primary statement decisive because the step's own
words disclaim the enumeration's self-sufficiency.

verifier-01's n = 1 observation is worth keeping in the repair: where every
tile extent is 1 the permutation is the identity, but neither named limb
reaches that case by its own words — only the general condition does. So
the general condition is load-bearing here, which is the reason the
incomplete gloss is worth fixing rather than tolerating.

Implementer consequence, both sides concretely: updater U1 changes a
layer's filter declaration from 1 to 2 on a layer all of whose stored
tiles are packed bool planes (s = 1) in a directory-only commit — one
record, one pad, one trailer. U2, reading the growth gloss as the
carve-out's definition, refuses and rewrites the whole file under a fresh
file_id. Both outputs are conforming files; only one is a commit. The
document permits U1.

Repair: in the growth sentence write "it covers, among other things, a
position whose stored byte already holds the fill it keeps" — or better,
"the carve-out reaches a position whose stored byte already holds the fill
it keeps, not one that ceases to be padding", dropping the word "covers"
that reads as an extent claim.

### 4. carve-out-worded-over-bytes-not-bits — CONFIRMED, not byte-level, editorial

Member: diagrams-01.

Real: the §14 bar's own list is bit-aware ("the pad bits `[R-SER-03]`
gives a packed planar bool plane"), [R-SER-05] enumerates three
representations ("the recorded fill bytes for a numeric channel, the
recorded fill byte for an interleaved bool channel, the fill bit in a
packed plane"), and the carve-out is worded over "stored byte" at all five
occurrences. A padding position in a packed plane has no stored byte of
its own.

Downgrade quotation, §20.3 step 4:

> The test is the effect on such a tile, and the list names where that
> effect arises rather than standing on its own: a change that leaves
> every one of those tiles' stored bytes meaning exactly what they meant
> ... is not what this bars.

The witness satisfies that general condition: the tile's two stored bytes
are untouched and every bit still decodes to the same bit value; only
position 15's sample/padding status changes, which is equally true of the
numeric case the document expressly permits. Reading R2 requires two moves
against express text — taking the illustration as the rule *and* letting
the first list item stand on its own — where the step says the list does
not stand on its own.

The shrink paragraph's "What counts as such an alteration is the §14 bar
and nothing else, its carve-out included" does not narrow it either: it
incorporates the whole carve-out by reference and then gives one instance
of it.

Premise of my downgrade, stated so it can be attacked: I read "every one
of those tiles' stored bytes" at the granularity of the tile's whole
stored byte string, whose meaning is unchanged, rather than at the
granularity of "the stored byte of a position", which a packed position
lacks. If a judge reads the general condition per-position, the packed
case fails it, the first list item bites, and the group becomes
byte-level — an updater that emits the one-record append versus one that
refuses it, on a conforming file. The plural possessive "those tiles'
stored bytes", not "each position's stored byte", is what decides it for
me.

Implementer consequence, both sides concretely: U1 shrinks E₀ from 16 to
15 on the packed-bool layer with a directory-only commit — the index
region is not even re-emitted, since entry_count and extent_length are
unchanged. U2 refuses and tells its caller to rewrite the file whole, for
a change that touches one record and not one stored byte.

Repair: at the three normative occurrences in §20.3 (and the two in §11.1
and §23.1), write "stored representation", or name the three cases as
[R-SER-05] already does.

Noted for the record: diagrams-01 warns that a line-oriented grep for
"fill bit in a packed plane" returns zero and for "stored byte already
holds the fill" returns two of four occurrences, so the finding is
invisible without whitespace normalisation. I did not need the grep — I
read the passages.

### 5. trailer-table-flags-cell-no-values — CONFIRMED, not byte-level, editorial

Member: diagrams-02.

Real, and verified against all ten rows: flags is the only cell in the
Valid values column that gives a structural decomposition instead of a
value set.

Downgrade quotation, §6.2 [R-CNT-06], immediately below the same table:

> A reader MUST validate, in order: the trailer magic; the trailer CRC;
> the version gate (§6.3) ... and then, those gates passed, MUST validate
> all of the following before acting on the fields involved: the flag
> gates (§6.3); ...

plus §6.3 [R-CNT-08]: "a writer creating a file under this text MUST write
flags = 0". Both normative, both in the same section, and §19.1 step 2
cites [R-CNT-08] again in the reader algorithm.

Implementer consequence: an implementer who builds a trailer validator
from the layout table alone omits the incompat-lane rejection. But the
paragraph five lines below the table enumerates it, and §19.1's open
algorithm cites it a third time. Practically inert: a writer has no
prompting to emit anything but zero, and the reader check is stated three
times outside the table.

Repair: give the cell "0 (§6.3); a set ignore-lane bit (16–31) is
conforming and ignored".

### 6. zero-layers-entry-fuses-empty-directory — CONFIRMED, not byte-level, register-bookkeeping

Member: diagrams-03.

Real: [R-CNT-14] states two things — "any number of layer records (zero is
valid: an empty directory is a conforming generation)" and "at most one
file-scope user-metadata record" — and §21.6's cell fuses them into "A
conforming file with an empty directory". A file with no layer record and
one top-level user-metadata record is conforming and its directory is not
empty.

Downgrade quotation, §21.1:

> §21.6's entries restate their governing rules on the same terms a row
> does, and where such an entry and the rule it cites diverge, the rule
> governs there too.

Implementer consequence: essentially none. §21.6 is "conditions that are
not violations" — a reader consulting it learns not to reject; it is not a
check list. A verifier is built from [R-CNT-14] and F-row/L-row
conditions. No file's verdict moves.

Repair: "A conforming file; its directory carries no layer record."

### 7. sparse-note-keys-reemission-to-growth — CONFIRMED, not byte-level, editorial

Member: diagrams-04.

Real, and both of the reporter's two cases check out. A shrink dropping
only sentinel tiles leaves the stored-tile set unchanged while entry_count
falls, and §20.3 says so in terms: "`[R-CNT-17]` obliges the smaller
entry_count and so a re-emitted index region". Removal of a planar channel
that stored nothing drops entry_count from C·N to (C−1)·N and is expressly
permitted.

Downgrade quotations. §2.3 [R-CNF-01]:

> All text in this document is normative except: §1 (Introduction); any
> text labeled *Note*, *Example*, or *Rationale* ...

and the rule itself, §20.3 step 4:

> Every layer whose stored-tile set or index content this commit changes
> has its tile-index region re-emitted in full

Implementer consequence: a writer built from the Note alone omits the
re-emission on those two commits and emits a layer record whose
entry_count and extent_length disagree — an L-row violation under
[R-CNT-17]. That writer is simply nonconforming under both readings, so
the emittable set does not move; the cost is one bug, not a fork.

Repair: "...or that changes its entry_count, ...".

### 8. three-shapes-figure-and-pe0-drop — PARTIAL, not byte-level, figure

Member: diagrams-05.

The premise is real: §20.4 now licenses dropping a PE = 0 record "in any
commit it is otherwise free to make — one whose only effect is the drop
included", and the case is constructible (§7.3 registers only PE = 1
types, so a PE = 0 record is of an unassigned type, and §21.6's
experimental-range row makes an MU = 0 record of such a type conforming).

But the reporter's claim that it fits none of the three shapes overreads
shape (c). (c) is "**A change confined to the directory** ... Only the
directory is re-emitted." A drop-only commit re-emits only the directory,
so it *is* (c). The exclusion the reporter invokes is specific and
reasoned: "Editing user metadata is not this shape: its document lives in
an extent (`[R-CNT-25]`), so a new extent is appended and the old one
becomes slack, as in (b)." A drop appends no extent, so the stated ground
of the exclusion does not apply and (c) is not excluded. What is actually
missing is only the *drawing*: (c)'s diagram hatches the old directory,
pad and trailer, and does not hatch the dropped extent. Hence PARTIAL.

Downgrade quotation, [R-CNF-01] ("any text labeled ... *Example*") plus
§20.4's own licence, which states the outcome without the figure:
"Retain byte-identical, or drop it — its extent becoming slack."

Implementer consequence: none. Nobody builds a commit planner from a
figure whose three shapes are illustrative; the rules are §20.3 step 4 and
§20.4.

Repair: add a hatched run to (c)'s diagram, or one clause — "a drop of a
PE = 0 record whose extent becomes slack is this shape too, with that
extent hatched".

### 9. appendix-h-omits-flags-obligation — CONFIRMED, not byte-level, editorial

Member: diagrams-06.

Verified: Appendix H's writer entry lists seven writer MUSTs and one
advisory, none about flags; the updater entry lists five obligations and
inherits "everything a writer does for the bytes it produces", which
cannot supply the flags rule since §6.3 exempts an updater from the
creator's flags = 0.

Downgrade quotations. Appendix H's own header: "each entry's authority is
the requirement or section cited, never this summary." And §6.3
[R-CNT-08]:

> An updater MUST copy forward unknown ignore-lane bits of the file it
> modifies, MUST NOT clear them, and MUST NOT set any other

Implementer consequence, both sides concretely: updater U1 copies the
inherited ignore-lane bits forward; U2 writes flags = 0. U2's output is a
*conforming file* — [R-CNF-02] declares this obligation expressly not a
file-conformance violation — so no verifier ever tells U2 it is wrong, and
a later minor-version reader loses a feature flag silently. That is a real
divergence in emitted bytes between two tools, but it is not an ambiguity:
§6.3 is unambiguous and U2 is violating a conduct rule it did not read.
The rule is stated in five normative places; only the checklist omits it.

Repair: one line in each of the two Appendix H entries.

### 10. err04-decline-scope-enumeration — CONFIRMED, not byte-level, editorial

Member: register-01.

Real: [R-ERR-04] licenses a decline "at the whole file, or at the narrowest
scope whose stated or derived quantities exceed what it can serve: a
layer, a tile, or the record carrying a user-metadata document". A zstd
frame's Window_Size lives in a tile's stored extent — §21.9's per-instance
paragraph individuates that row over "the ... compressed frames a file
actually contains, neither of which exists except as stored bytes" — so
for that excess the narrowest such scope is the tile, and the layer's own
declared quantities exceed nothing. Yet [R-COD-06] says a wide window
"permits a conforming reader to decline the tile or the layer", and
[R-CNF-11] names "when it declines a layer's or a tile's decode on
resource grounds".

Downgrade quotations. [R-ERR-04]'s own first alternative already offers a
scope broader than the narrowest — "at the whole file, or at the narrowest
scope ..." — so the sentence is not confining a reader to the narrowest.
And §18.2's Note works the mechanism through:

> A reader whose own bound it exceeds takes ignore-record for that record,
> which is also the narrowest scope at which `[R-ERR-04]` lets it decline
> the document on resource grounds; it MAY instead decline the whole file.

"the narrowest scope at which [R-ERR-04] lets it decline" presupposes that
[R-ERR-04] lets it decline at broader ones.

Not byte-level, on a second ground the reporter states correctly: once a
quantity exceeds a §21.9 guarantee, [R-CNF-03]'s duty has lapsed for that
file — "A reader MUST accept every conforming file ... and none of whose
values exceeds the minimum guarantees of §21's limits table" — so no
accept obligation moves under either reading, and the file is conforming
under both.

Implementer consequence: reader R1 declines the layer and reports "layer
`sst`: zstd window 64 MiB exceeds this reader's 8 MiB bound"; R2 declines
only the tile. A verifier built on reading (a) would call R1's diagnostic
an overreach. Nothing about which files either accepts changes; only the
granularity of the diagnostic. Report-level.

Repair: "at the whole file, at any scope containing the excess, or at the
narrowest scope whose stated or derived quantities exceed what it can
serve" — making the narrowest the floor rather than the only option.

### 11. lz4-cap-restatement-drops-quantifier — CONFIRMED, not byte-level, register-bookkeeping

Member: register-02.

Real: §21.9's hard-limit clause says "a layer declaring codec 4 at decoded
tile size at most `0x7E000000` (`[R-COD-07]`)", dropping both
[R-COD-07]'s "addressed tiles" quantifier and its planar
largest-plane rule. Read alone it invalidates the very file [R-COD-07]'s
Note exempts.

Downgrade quotations, §21.9, both in the same paragraph as the clause:

> The hard limits it restates are a finding aid rather than an inventory —
> each is normative where the structure forcing it is defined.

> They are stated where the structures forcing them are defined

Two express disclaimers of authority. Add that §21.9's own per-instance
paragraph forty lines earlier states the quantifier correctly ("ranges
over a layer's **addressed** tiles, stored or not, exactly as
`[R-COD-07]`'s cap is") and L44 states it correctly. Three passages in §21
agree with the rule against one compressed restatement that disclaims its
own authority.

Implementer consequence: an implementer would have to read one clause past
two explicit disclaimers and two agreeing passages in the same section to
reject a conforming empty layer declaring codec 4. Inert.

Repair: "a layer any of whose addressed tiles' decoded size is at most
`0x7E000000` under codec 4, the largest channel plane governing in a
planar layer".

### 12. experimental-type-entry-undercited — CONFIRMED, not byte-level, register-bookkeeping

Member: register-03.

Real: the entry's Defined-behavior cell names L25, a sub-record row, but
its Rule cell cites [R-CNT-15] (file scope) and [R-WRT-08], not
[R-CNT-18], which is the rule that gives an unassigned sub-record type
with MU = 0 its ignore-record outcome. §10.3 keeps the two apart where it
needs the distinction, and §21.6's own closing paragraph relies on the
split for the MU = 1 case.

Downgrade quotation, §21.1:

> §21.6's entries restate their governing rules on the same terms a row
> does, and where such an entry and the rule it cites diverge, the rule
> governs there too.

And both rules assign the same outcome at MU = 0 — [R-CNT-15]
"MU = 0 → ignore-record", [R-CNT-18] "with MU = 0 it is ignore-record" —
so no outcome moves whichever is cited.

Implementer consequence: a reader tracing the entry to its authority for a
sub-record follows [R-CNT-15] into a rule that speaks only of file scope
and must find [R-CNT-18] via §10.3 or §7.4. A navigation cost, not a
behaviour change.

Repair: add `[R-CNT-18]` to the Rule cell.

### 13. geo-rationale-omits-growth-permission — CONFIRMED, not byte-level, editorial

Member: adversary-02.

Real: §11.1's Rationale says "Of its two bars the one reaching a shrink or
a growth is the §14 bar", then works only the shrink through and gives
three carve-outs grammatically attached to the shrink, and discusses growth
only via entry_count and index re-emission. It never states §20.3's
express growth permission. An ordinary growth of a layer with an edge tile
alters the padding-position set of a prior-generation stored tile — the
first item in the §14 bar's own list — so a reader taking those three
carve-outs as the whole test bars almost every growth.

Downgrade quotation, from inside the block itself:

> §20.3 states normatively, and governs, what a commit may do to a layer
> that already stored tiles in the generation a commit supersedes.

plus [R-CNF-01]: text labeled *Rationale* is not normative. And §20.3's
permission is unambiguous: "an extent MAY **grow**, since a position that
becomes real held, for each channel the position carries, that channel's
fill (§14.5), and fill is a legal sample value."

Implementer consequence: an implementer building from §11.1 alone refuses
ordinary extent growth on any layer with an edge tile — which breaks
declare-then-fill, the workflow §11.1's Rationale exists to justify. Real
but self-correcting: the block defers in its own second sentence.

Repair: one clause in the Rationale naming the growth permission, or scope
the three carve-outs to the shrink explicitly.

### 14. renumbering-parenthetical-incomplete — CONFIRMED, not byte-level, editorial

Member: adversary-03.

Real: the re-emission clause's parenthetical is "(a geometry change
renumbers ordinals wherever `[R-GEO-06]` moves them)", and the paragraph
two below says the ordinal bar exists because a planar channel-declaration
change disturbs "the re-emission rule above, whose only stated occasion for
a renumbering is a geometry change". But a permitted planar channel
removal — of channels the superseded generation stored no tile for —
renumbers disk ordinals with no geometry change.

Downgrade quotation, §20.3 step 4, the operative clause the parenthetical
attaches to:

> and every other entry byte-identical **at its disk-ordinal position**

The position is whatever the new declarations assign; the parenthetical is
one illustration. Reading (b) is unsatisfiable on the worked case —
entry_count falls from 6 to 4 and positions 4 and 5 do not exist — so it
cannot be the rule for a commit §20.3 expressly licenses ("a commit that
moves only the ordinals of channels the superseded generation stored no
tile for alters nothing this bars").

Not byte-level for a second, independent reason I verified: every moved
entry is necessarily a sentinel (only channels that stored no tile may
move), and a sentinel is `FF ×16 00 ×4` — byte-identical wherever it
lands. So wherever both readings are satisfiable the emitted index region
is identical.

Implementer consequence: an implementer taking (b) cannot emit the index
region for a commit the document licenses, and would either crash or
refuse. One implementation is stuck, not two diverging on bytes.

Repair: "(a geometry change, or a permitted channel-declaration change,
renumbers ordinals wherever `[R-GEO-06]` moves them)".

### 15. such-a-tile-antecedent — CONFIRMED, not byte-level, editorial

Member: adversary-04.

Real: "As there, de-addressing rescues nothing: a commit that also alters
what §14 fixes for such a tile is barred." The nearest noun phrases are the
de-addressed tiles of the removed channel, which the immediately preceding
clause has just said "carry no §14 obligation afterwards".

Downgrade quotation, the shrink paragraph the "As there" points at, which
states the same thing explicitly:

> Dropping a tile out of the addressed set is not itself such an
> alteration ... but neither does it rescue a commit that damages a
> prior-generation stored tile.

Reading (b) would have the sentence bar alteration of what §14 fixes for a
tile the sentence before it says carries no §14 obligation —
self-contradictory. So (a) is the only coherent reading and "As there"
supplies the antecedent.

I do NOT accept adversary-04's second argument, that "both bars govern an
updater's commit, not a file ... so no verifier verdict differs" therefore
nothing byte-level is at stake. That argument would equally defeat
writer-01, and it is wrong: a bar on a commit is a bar on an actor's
emitting a byte sequence, which is exactly the byte-level test. The
downgrade rests on incoherence plus "As there", not on that.

Implementer consequence: an implementer taking (b) refuses commits §20.3
permits — removing a planar channel while re-typing a different channel
none of whose own tiles are stored, which §20.3 elsewhere calls "a
declaration edit like any other". Conservative failure, one implementation
wrong.

Repair: replace "such a tile" with "a tile the layer stores in the
generation this commit supersedes", matching the shrink paragraph.

### 16. ser08-returned-encoding-and-one-byte — CONFIRMED, not byte-level, editorial

Member: adversary-05.

Two halves. The first — that [R-SER-08] alone fixes the logical value but
not the encoding a reader hands back — is true of the rule read in
isolation, and the reporter itself calls it decidable. It is decided more
cheaply than the reporter's three-passage assembly suggests, by one
sentence in §12.3 [R-TYP-04]:

> the one case where a reader resolves a byte to a value rather than
> passing it through arises only in a nonconforming file, and
> `[R-SER-08]` states it

"resolves a byte to a value rather than passing it through" settles it
directly: the reader returns the value true, not the byte 0x7F. §21.1 says
the same — "`[R-SER-08]` is the one rule that goes the other way: it
resolves a nonconforming interleaved boolean byte to a value rather than
serving it through" — and Appendix H a third time. Combined with §14.2's
encoding (0x01 = true) and [R-TYP-04]'s "their encoded bytes are
identical", the returned byte is 0x01.

The second half — "the one byte a conforming file cannot" in §19.4 step 8
and "the one byte a reader resolves" in §21.1, where 254 bytes are
excluded and §12.3's "the one *case*" is the accurate form — stands as a
plain miscount and is the durable part of the finding.

Not byte-level: the file in dispute is nonconforming (§14.2 makes the byte
a writer violation, T2 registers it), so [R-CNF-05] bars every conforming
writer from emitting it under both readings; both readers accept it, so no
verdict forks; and what differs is only what a reader hands its caller.

Implementer consequence: R1 returns 0x01, R2 returns 0x7F. Both are
serving a file no conforming writer produced. Downstream code comparing
returned bool bytes would see them differ — but §12.3 and §21.1 both say
R2 is wrong.

Repair: say in [R-SER-08] that the reader returns the value's encoded byte
(0x00 or 0x01), and change "the one byte" to "the one case" in §19.4 and
§21.1.

### 17. partial-total-causes-omit-resource-decline — CONFIRMED, not byte-level, editorial

Member: verifier-02.

Real, and the third cause is reachable: §2.3 makes a verifier a reader of
the files it processes; §21.9's figures are minimum guarantees not caps, so
a layer declaring entry_count = 2⁴⁰ is conforming; [R-ERR-04] lets the
verifier decline that layer; §21.9 insists the refusal "MUST be reported as
a resource limit and not as a validity error", so it is not a scope-level
*rejection*; no violation is established, so it is not the [R-CNF-11]
stop-at-first-violation election either. Both statements of the rule
enumerate exactly the two causes that presuppose an established violation.

Downgrade quotation, from inside [R-CNT-21] itself, immediately after the
enumeration:

> It is not the file's slack total but a bound on it, tightening to the
> exact total when the walk completes.

That is definitional: a total from an incomplete walk is a bound, and it
becomes the exact total only on completion. It cannot be reported unmarked
as the exact total after a walk that did not complete, whatever stopped it.
§21.6's slack row states the obligation on the general condition with no
cause list at all — "counted and reported by a verifier — as a partial
total — an upper bound naming what stopped the walk — where its walk did
not complete" — and Appendix H does the same. Grammatically, "whether
because A ... or because B" is a concessive appositive disclaiming
dependence on which cause, not an exhaustive gate.

Not byte-level: both readings give the same verdict on the same file
(cannot establish), the file is conforming under both, §2.4 places the
slack total outside every reader obligation ("Coverage is checked by
verifiers, never by readers"), and no writer's emittable set moves.

Implementer consequence, both sides concretely: verifier V1 declines a
2⁴⁰-entry layer on resource grounds and reports "slack: 4.1 GB (partial —
layer `sst` declined on resource grounds)". V2 reports "slack: 4.1 GB". An
operator reading V2's line runs a compaction the file does not need, since
§22.3 makes that number "what distinguishes a working file from a padded
one" and §20.3's note and §20.5's example both make it the compaction
trigger. Report-level, and the operator-facing cost is real.

Repair: at both sites, either drop the enumeration or add the third cause —
"or because the verifier declined a scope on resource grounds
(`[R-ERR-04]`)".

### 18. relies-on-two-senses — CONFIRMED, not byte-level, editorial

Member: quiz-01.

Real: [R-WRT-03] fixes verification depth by reliance and says
"re-emission (§20.4) relies on every directory byte", while step 2 shelters
the appender by invoking [R-WRT-01]'s clause for structures it "neither
modifies nor relies on" and extends that shelter in terms to "a record
re-emitted byte-identically". By the section's own definition of reliance a
re-emitted record is a structure the appender relies on.

Downgrade quotations, both in §20.3 step 2 and §20.1:

> An appender that carries a violation forward SHOULD report it, and a
> caller that is not told cannot know the file it extended was already
> damaged.

A SHOULD to *report* what it carried forward presupposes that carrying it
forward is permitted; under reading (2) the appender must refuse and there
is nothing to report. And §20.1 [R-WRT-01]:

> An appender and a compactor satisfy every writer requirement for the
> bytes they produce and the preservation obligations of §20.4 for what
> they carry forward ... a violation latent in a structure they neither
> modify nor rely on travels with it, and certifying the whole file is a
> verifier's office.

[R-CNF-05] is scoped to "the bytes they produce", so it does not bar the
appender from extending a file that already carried a latent violation.
The contrast is deliberate and stated for the compactor alone: §20.5 says
a compactor "MUST refuse to compact when any check `[R-WRT-09]` obliges
fails, and MUST NOT emit a file carrying a violation it has detected". No
such sentence is written for the appender.

I note that quiz-01's own byte-level rationale is unsound — it argues
[R-CNF-05] bars the output under both readings, which §20.1's scoping
contradicts — but the conclusion is right on the grounds above. This
matters: the shape *would* be byte-level (one reading permits an actor to
emit a byte sequence the other forbids) if the text did not decide it.

Premise of my downgrade, stated so it can be attacked: I read the
SHOULD-report sentence as presupposing the commit, and §20.1's "for the
bytes they produce" as scoping [R-CNF-05] away from carried-forward
structures. If someone read the SHOULD as conditional on a commit the
appender is separately permitted to make, and read [R-CNF-05] as
unqualified over the whole output file, reading (2) revives and the
emittable set forks. Two independent grounds is why I am comfortable.

Implementer consequence, both sides concretely: appender A1 extends an
archive whose one damaged layer record it re-emits verbatim, logs a
warning, and commits. A2 refuses every append against any file it found a
defect in — the compactor's behaviour — so a caller with a
damaged-but-extendable archive gets no new generation. A1 is right.

Repair: drop step 2's appeal to [R-WRT-01] and rest it on its own first
half ("Reproducing a structure's bytes unchanged is not authoring them"),
or say which sense of "relies on" step 2 uses.

### 19. preservation-table-keyed-to-stored-flags — CONFIRMED, not byte-level, editorial

Member: quiz-03.

Real, and the strongest of the near-misses. §20.4's obligations appear
only in a table whose column heading is "Stored flags" and whose
introducing clause is "For a type the updater does not implement, the
stored flags are authoritative ... and carry these obligations". The
subject of "carry these obligations" is the stored flags in that one case.

Downgrade quotations, both normative and both in the same paragraph:

> Persistence governs every record type; only the authoritative source of
> the flags differs.

> For a type the updater implements that this specification does not
> register, the definition it implements the type from supplies the flags,
> and the stored bits never do

The first says the persistence regime attaches to every type with the flag
source as the only variable — which is false if the table binds one case.
The second says an outside definition "supplies the flags"; supplies them
for a purpose, and the only purpose in this paragraph is the table's
obligations. Reading (2) makes both sentences vacuous. Reading (1) makes
only a column heading loose.

I record that quiz-03's own byte-level rationale understates the stakes.
The reporter says both readings agree on every record type format major 1
defines, which is true of the type list but not of the *commit*: under
reading (2) §20.3 step 2's "MUST NOT drop the record save where §20.4
licenses the drop" bites, since §20.4 would license no drop for an
implemented-unregistered PE = 0 record, and a directory with that record
dropped becomes a byte sequence one reading permits an updater to emit and
the other forbids — a conforming file either way. So this is a byte-level
*shape*, decided by the two sentences quoted, not a shape that could not
fork.

Premise of my downgrade, stated so it can be attacked: I take the
paragraph's topic sentence to generalize the table over all three flag
sources. If someone instead held that a table's own heading and its
immediate introducing clause fix its scope — the ordinary reading of a
table — reading (2) revives and this is byte-level. I judge the topic
sentence decisive because it is placed exactly to generalize and says
nothing otherwise.

Implementer consequence: confined to a private experiment. The class is an
unregistered type an updater implements from an outside definition, and
§10.3 forbids emitting experimental values "in released software or
published data", so the divergence cannot reach circulation without a
separate violation. U1 drops such a record and reports the loss; U2
refuses and carries it forward. Both outputs are conforming files.

Repair: relabel the column "Governing flags" and change the introducing
clause to "and the governing flags carry these obligations, whatever their
source".

### 20. doubled-reverification-trigger — CONFIRMED, not byte-level, editorial

Member: quiz-04.

Real, and it is normative text — §22.3 carries no *Note*, *Example* or
*Rationale* label. The sentence reads "... which is why recovery output is
re-verified as a whole file before being trusted (`[R-LIF-06]`) before any
use", with "before any use" attaching to nothing, and the same obligation
is then restated three clauses later in a third wording.

Downgrade quotation, §9.6 [R-LIF-06], the requirement §22.3 cites:

> a tile payload can deliberately contain a byte string that mimics a
> valid trailer, so recovery output MUST be re-verified as a whole file
> (§8) before being trusted

One trigger, stated once, in the governing rule. Reading (b) — that
"before any use" bars a recovery tool from so much as parsing its own
output — is self-defeating: re-verifying the output as a whole file *is*
using it. So "before any use" can only mean "before any use other than the
verification itself", i.e. before being trusted.

Not byte-level: the obligation binds a tool's procedure; §9.6 places the
recovery scan outside conforming reader behaviour entirely ("Recovery tools
and verifiers — never conforming readers on the default path"); and no
file is accepted or rejected differently.

Implementer consequence: none that separates two implementations. Every
recovery tool re-verifies its output whole before handing it over.

Repair: delete the trailing "before any use", and delete one of the two
restatements.

---

## Counts

Input ids: 24. Groups: 20. Union of member_ids = the 24 input ids, no
duplicates, counted by hand against the id list in the brief:

reader-01 (g1), writer-01 (g2), writer-02 (g3), writer-03 (g1),
verifier-01 (g3), verifier-02 (g17), diagrams-01 (g4), diagrams-02 (g5),
diagrams-03 (g6), diagrams-04 (g7), diagrams-05 (g8), diagrams-06 (g9),
register-01 (g10), register-02 (g11), register-03 (g12), adversary-01 (g1),
adversary-02 (g13), adversary-03 (g14), adversary-04 (g15),
adversary-05 (g16), quiz-01 (g18), quiz-02 (g1), quiz-03 (g19),
quiz-04 (g20).

4 + 1 + 2 + 17×1 = 24.

Byte-level upheld: 1 (group 2, writer-01).
Reporter self-flagged byte-level: 1 (writer-01). Upheld.

Two groups I flag to the reconciler as the likeliest places a later phase
lands, because my downgrade there rests on a premise rather than on an
express contrary sentence: group 4 (carve-out-worded-over-bytes-not-bits,
where the premise is the granularity of "those tiles' stored bytes") and
group 19 (preservation-table-keyed-to-stored-flags, where the premise is
that a topic sentence generalizes a table over its own column heading).
Both are byte-level in shape and are held below it only by a reading.
