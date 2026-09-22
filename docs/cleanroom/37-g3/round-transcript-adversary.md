# Adversary transcript — cleanroom round 37

## 0. Disclosure

**What I read.** Exactly one specification file was opened with a file-reading
tool: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
in full (it is 4,981 lines; my tool's per-call size limit forced me to read it
in eleven overlapping chunks by line offset, but the union covers every line
of the file with no gaps — I checked the chunk boundaries against each other
as I went). I opened no other repository file. I did not list any directory
other than creating and listing my own scratch directory once at the start
(`ls -la` on
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r37-round/scratch/adversary/`,
which was empty — no prior attempt's files were present, so there is nothing
to work beside). I did not open `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`,
`AGENTS.md`, `README.md`, `CONTRIBUTING.md`, `conformance/`, or
`spec/registry.json`. I ran no `git log`/`git diff`/web search/web fetch. I
did not read the output directory
(`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r37-round/out/`)
at any point, before or after writing my own file there.

**What I ran.** Several `grep`/`awk` sweeps against the one permitted file
(listed in full under "Evidence: sweeps run" below), and two small local
Python scripts that operate only on strings I had already transcribed by
hand from the file's content already in my context — the scripts read no
files. Both scripts and this transcript live under my scratch directory:
`figure_check.py`, `figure_check2.py`, and this file
(`transcript_draft.md`, superseded by the published `transcript-adversary.md`
at the output path). No other agent's files were present in my scratch
directory at any point, so there was nothing to avoid running.

**Context I did not ask for.** My runtime placed a substantial amount of
material in context before I began work that is not part of the
specification and is not evidence about it: a project `CLAUDE.md` pointing
to an `AGENTS.md` I never opened; a user memory file
(`MEMORY.md`) containing about twenty bullet points with titles referencing
this exact project's history in ways that look like prior-round conclusions
or hints (e.g. titles naming "the pre-round-37 audit," "lineage gate word
list... missing," "no lowercase keywords," "ADR status change gates
quotes," and others); git status/log output naming recent commits including
one titled "Cleanroom round 37: charter, over 96e4ad4..6c9470e" and others
about ADR-0131 and prior rounds; a list of available tools and skills; an
"Auto Mode Active" operating reminder; and MCP server instructions for
several connectors. **None of this is part of the specification, and I have
not used any of it to settle any question about the specification's text.**
Where my reasoning below might look similar to any theme suggested by a
memory-file title, that is coincidence produced by independently reading the
document and applying the round's own stated attack shapes — not by
consulting the titles for an answer. I disregarded all of it as instructed
and did not open any of the referenced files (`AGENTS.md`, the ADR files,
etc.) even though the memory index named them, because the access rule
permits exactly one file.

**Paths.** The one file I was told to read was exactly where the brief said:
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
existed at that path with no redirection needed. My scratch directory and
the output path were also exactly where named. I found nothing anomalous
about any path.

---

## 1. Reading pass

I read the document in this order, end to end: Part 0 (§1–§4, terminology
and encoding conventions), Part I (§5–§10, container: trailer, records,
integrity, lifecycle, registry), Part II (§11–§18, array model: layers,
channels, fill, serialization, tile index, slabs, codecs, user metadata),
Part III (§19–§24, reader/writer/updater algorithms, the error register, the
security/privacy sections, conformance vectors), and all eight appendices.

I paid the closest attention to the four passages the brief calls "this
cycle's decisions" — §20.4's re-emission/preservation table and the
paragraph below it; §7.2's Note on the two record-flag bits plus the
paragraph before it (the extent-slot / no-embedded-offsets rule and the
layer-record exception); §20.1's closing paragraph on the writer's choice
between rewriter and creator, together with §2.3's conduct-rule paragraph
(`[R-CNF-02]`); and §20.3 step 4's "the bar binds a layer the commit keeps
and nothing else" sentence and the paragraph it closes — and to the three
named changed passages (§3.3, §20.3, §20.4) and their surrounding text. I
then re-read the whole of Part III a second time once I understood the
shape of the updater/writer taxonomy, since that is where all four named
decisions live.

I want to record, honestly, where my reading needed a second pass and where
I had to resolve something by working it out rather than finding the answer
stated in one place:

- The §20.4 table's three rows read, in isolation, like they classify a
  *record* by its own flags. Understanding what a *layer drop* does to a
  layer's *sub-records* required assembling three separate sentences: the
  table's MU=1 row ("At layer scope an unknown critical record blocks
  modification of that layer, its drop included"), the paragraph
  immediately below the table ("a dropped layer's sub-records and their
  extents go with it whatever their PE bits. One sub-record blocks the
  drop, a sub-record of a type the updater does not implement with MU = 1"),
  and — critically — a sentence *between* those two that narrows the
  table's own MU=1 row's reach: "Its MU = 1 row reaches only a type the
  updater does not implement — an updater implements both registered types
  and understands an unregistered type it implements from its definition,
  modifying their records as §20.3 and that definition provide — so for an
  implemented type only the PE bit bites." I had to read this three times
  to see that the blocking condition and the table's MU=1 row are the *same*
  condition, restricted to unimplemented types, and that an *implemented*
  MU=1 sub-record (which §7.2's flag rule always forces effectively to
  PE=1) is *not* covered by the blocking sentence at all — see Finding
  adversary-02 below.
- §20.1's "the choice is its own" sentence, and the parallel "a writer that
  extends an input file is an appender and an updater, whatever it decodes"
  sentence two sentences earlier, look at first read like they might be in
  tension (one says the writer's classification is externally forced by
  what it does; the other says it is self-determined). I resolved this by
  noting the two sentences are about two *different* branches: extending an
  existing file under its own file_id is objectively an appender ("whatever
  it decodes" — that part is not a choice); writing a genuinely *new* file
  under a *fresh* file_id from an existing input is the branch where "the
  choice is its own." I then had to work out whether that choice could ever
  produce two different *file*-conformance verdicts for the same output
  bytes, which it cannot, because `[R-CNF-02]` fixes conforming-file status
  as "a pure predicate on bytes: it does not depend on any reader, writer,
  or environment" (§2.3) — see the extended discussion under Finding
  adversary-01.
- The three ASCII-art figures in §20.3's "the three shapes a commit takes"
  Example, and the compaction figure in §20.5, needed a literal
  column-by-column check, since the brief warned that one of the round's
  edits was "a figure's annotation bracket closed and then moved one
  column." I transcribed the box-drawing lines by hand into a small script
  (`figure_check.py`, `figure_check2.py`) and counted columns. I could not
  reach a confident verdict either way — see "Rejected candidates" and
  `confidence_empty` below; box-drawing and subscript characters can render
  at inconsistent visual widths across tools, so a column count taken from
  my read tool's output is not proof of the source markdown's true
  character-for-character alignment.

## 2. The convention check (§R-CNF-01 and the ">" marker)

I did not assume the brief's restatement that "the exemption is by the
label, not by the '>' marker" — I checked it against the document's own
practice. `[R-CNF-01]` (§2.1) reads: "All text in this document is
normative except: §1 (Introduction); any text labeled *Note*, *Example*, or
*Rationale*; and appendices identified as non-normative." I then swept the
document for blockquote (`>`) blocks whose first line does not carry one of
those three labels (see sweep 6 below). I found one: §15.1's tile-index
region layout —

> [ entry array: entry_count × 20 bytes ] [ segment CRC array:
> ⌈entry_count / 2¹⁶⌉ × 4 bytes ]

— which is rendered as a blockquote purely for visual offset but carries no
*Note*/*Example*/*Rationale* label and is squarely normative content (it
fixes the byte layout of the tile-index region, restated by the table two
paragraphs below it). This confirms the brief's claim that "a blockquote
carrying no such label is normative. At least one exists" independently of
trusting the brief — I located the instance myself and it is unlabelled. I
found no defect *in* that passage; it agrees with the table around it. I
record this as evidence that I checked the convention rather than assumed
it (`rejected_candidates`, below), not as a finding.

I also confirmed the brief's separate claim about where the three changed
passages fall relative to this convention. §3.3's changed text is inside a
labelled `> **Note.**` block (non-normative). §20.3's changed Example
figures are inside a labelled `> **Example — ...**` block (non-normative).
§20.4's changed table row (see Finding adversary-03) is an ordinary,
unlabelled table inside the main flow of §20.4 — normative, and binding an
updater, exactly as the brief says: "the third in an unlabelled table that
binds an updater." This matters for grading: a defect in the first two
would not be a defect in normative text even if I found one (I did not); a
defect in the third would be. I found no confirmed defect in the third
either, but I give it the closest reading (Finding adversary-03).

## 3. Walking the four named decisions

### 3.1 §20.4 — the layer-drop mechanics (decision 1)

Quoted text, §20.4:

> A commit MAY therefore drop a layer record, and the drop takes the layer
> whole: a sub-record's flags govern it within a layer the updater keeps, so
> a dropped layer's sub-records and their extents go with it whatever their
> PE bits. One sub-record blocks the drop, a sub-record of a type the
> updater does not implement with MU = 1, the drop being a modification of
> the scope it governs (the table's first row).

and, immediately above, inside the table's lead-in:

> The table states what an updater owes a record it does not logically
> modify, read under whichever flags govern it. Its MU = 1 row reaches only
> a type the updater does not implement — an updater implements both
> registered types and understands an unregistered type it implements from
> its definition, modifying their records as §20.3 and that definition
> provide — so for an implemented type only the PE bit bites.

I traced what this means for a sub-record that *is* MU = 1 but of a type the
updater *does* implement (necessarily, today, only a privately-defined
experimental-range type — see §10.3 — since format major 1's registry
assigns no MU=1 type at all: 0x0001 layer is MU=0/PE=0 and 0x0002
user-metadata is MU=0/PE=1, confirmed against §7.3's table and Appendix C's
registry snapshot). By the letter of the text quoted above, such a
sub-record does **not** block a layer's drop: the table's MU=1 row (the only
row that speaks of "blocks modification... its drop included") explicitly
"reaches only a type the updater does not implement." An implemented type,
whatever its MU bit, is governed "only" by the PE bit — and §7.2 forces
MU=1 combinations to read as PE=1 regardless of the stored bit
(`[R-CNT-12]`: "Writers MUST NOT emit the combination MU = 1 with PE = 0; a
reader or updater encountering it MUST treat the record as PE = 1"). Row 2
of the table (MU=0, PE=1 — which is where an implemented MU=1 record's
"only the PE bit bites" analysis lands it) reads: "Retain byte-identical,
extent content unmodified." That row does not say anything about blocking a
containing layer's drop — the layer-drop paragraph then explicitly states
that *whatever a sub-record's PE bit*, it "go[es] with" a dropped layer,
*unless* it is the one specific case the paragraph names (unimplemented,
MU=1).

**Working out whether this is a defect.** I considered whether this reads
as an oversight or as deliberate design, and I think it is internally
coherent, not contradictory: an updater that *understands* a critical
record's semantics is trusted to know whether dropping its host layer is
safe (the paragraph even ties this back to §7.2's exception: MU=1 records
are the ones licensed to "carry further references... where this
specification or registry review defines them," and an implementer who
registered/privately defined such a type presumably also defined what
happens to its references on a drop); an updater that does *not* understand
it cannot make that judgment and so is flatly blocked. That is a sensible
asymmetry, but it is easy to misread in the opposite direction (I did, on
first pass) — a reader could reasonably expect "MU=1" alone to always mean
"never silently drop," full stop, and the table's own MU=1 row heading
without any implemented/unimplemented qualifier in its own row label
encourages exactly that misreading. I record this as Finding adversary-02
(AMBIGUITY), not byte-level: format major 1's closed, two-member registry
(§7.3, §10.2, Appendix C) makes no *currently constructible* conforming
file exercise "an implemented MU=1 sub-record inside a dropped layer" at
all, since nothing in this specification is registered as MU=1. It is a
real reading of the current text worth flagging for when a future
registration adds an MU=1 type, but I cannot build a concrete file today
that forces two verifiers to disagree over it.

### 3.2 §7.2's Note and the paragraph before it (decision 2)

Quoted, the paragraph before the Note:

> For a record with MU = 0, the extent slot is its only sanctioned
> reference to bytes outside the record sequence: neither its inline
> payload nor its extent contents encode offsets or lengths of other file
> bytes — this is what lets a rewriter relocate an unknown ancillary's
> extent without parsing it (§20). The layer record is the one exception,
> and this specification's own: its tile index (§15), whose entries
> reference stored-tile extents, is defined here, and every conforming
> reader and updater implements the type (`[R-CNF-03]`, `[R-CNF-11]`), so
> none meets it as an unknown ancillary.

and the Note:

> **Note.** The two flag bits are not orthogonal. `[R-CNT-12]` leaves a
> record three states, not four, and they are §20.4's three rows: MU = 1,
> whose PE bit is read as 1 whatever is stored; MU = 0 with PE = 1; and
> MU = 0 with PE = 0. PE is a choice within MU = 0. An updater that does not
> implement an MU = 1 record's type never drops the record, alone or with
> the scope it governs (§20.4).

I checked the Note's final sentence — "never drops the record, alone or
with the scope it governs" — against §20.4's actual text, since that
sentence is a compressed restatement of the layer-scope and file-scope
halves of the table's MU=1 row. It matches: layer scope is "blocks
modification of that layer, its drop included, leaving other layers
editable"; file scope is "no commit is available at all," which trivially
also means the record is never dropped (nothing can be committed to the
file at all while such a record is present and unimplemented). I found no
inconsistency between the Note and the table it restates.

I also checked whether "the layer record is the one exception" is
consistent with the separate, more general license two sentences later:
"Records with MU = 1 carry further references only where this
specification or registry review defines them." These are not in tension —
the "one exception" is scoped explicitly to the MU=0 population ("For a
record with MU = 0..."), and the MU=1 sentence is a free-standing statement
about a different population (any future MU=1 registration). Both can be
true together; nothing forces "the layer record" to be the only MU=1-style
reference-carrier in perpetuity, only the only *MU=0* one today. I record
this as a rejected candidate (closed by scope), not a finding.

### 3.3 §20.1's closing paragraph and §2.3's conduct-rule clause (decision 3)

Quoted, §20.1:

> A writer of a new file from an existing one takes one of two positions,
> and the choice is its own. As a **rewriter** it undertakes to preserve
> its input: §20.4's table for every record, the unknown ignore-lane bits
> (`[R-CNT-08]`), and §20.5 whole; in return it answers for what it
> carries forward unmodified only to `[R-WRT-09]`'s depth, a latent
> violation travelling with it. As a **creator** it undertakes nothing
> toward its input, whatever it read: §20.2 binds it, it writes flags = 0,
> and it answers for every byte of its output (`[R-CNF-05]`), bytes it
> copied from another file included.

This is the passage the brief points at hardest ("run one tool over two
inputs that differ only in what they happen to contain and check that its
obligations hold still; then carry each position to the trailer's bytes on
the same input, an unknown ignore-lane bit set and a record of an
unimplemented type present"). I built the concrete test it describes.

**Construction.** Take a tool T that reads an existing conforming file F —
carrying, in its trailer, a set unknown ignore-lane bit (bit 16, say), and
carrying a top-level record R of an experimental-range type (0x8500) with
MU = 1 (legal: §21.6's second "conforming file a reader nevertheless
refuses" entry, and `[R-CNF-03]`'s own text, both confirm a conforming file
may carry a top-level experimental-range MU=1 record, though every
conforming reader must reject the *file* for it). T does not implement type
0x8500. T produces G: a new file under a fresh file_id, physically
relocating every structure (as any writer producing a brand-new file must —
§9.2's creation note: a fresh file begins writing at offset 16), and
copying R's header, inline payload and extent bytes byte-for-byte into G at
a new location, re-pointing only R's extent slot.

- If T calls itself a **rewriter**: `[R-WRT-06]` is unambiguous —
  "A rewriter MUST refuse to rewrite a file carrying any record whose type
  it does not implement with MU = 1: such a type can define references
  this specification does not (§7.2), so its bytes cannot be safely
  relocated." T, as a rewriter, must refuse. It cannot legally produce G.
- If T calls itself a **creator**: §20.2 (creation) states no equivalent
  refusal. §20.1 explicitly anticipates a creator copying bytes from
  another file ("bytes it copied from another file included") and says
  only that it "answers for every byte of its output" under ordinary
  writer conformance (`[R-CNF-05]`). Per §21.6's own text, a file carrying
  a top-level experimental-range MU=1 record *is* a conforming file
  (readers are obliged to reject it, but that is a reader-capability
  fact, not a file-conformance fact: "`[R-CNT-15]` obliges the reader to
  reject, and `[R-CNF-02]` makes the file conforming all the same").
  Nothing in §20.2 or elsewhere I can find bars a self-declared creator
  from producing G.

So the *identical operation* — read F, mint a fresh file_id, relocate every
structure, copy R's bytes verbatim to a new offset — is refused outright
under one self-declared classification and permitted under the other, with
"the choice is its own" as the only stated criterion for which
classification T gets. I worked through whether this actually forks a
*verifier's verdict* on the resulting bytes G, and I could not make it do
so, for one reason that itself is stated in the document: conforming-file
status is defined as "a pure predicate on bytes: it does not depend on any
reader, writer, or environment" (§2.3, opening the definition of
*Conforming TARN file*). A verifier examining G in isolation has no way to
know, and no textual instruction to ask, whether the tool that produced it
called itself "rewriter" or "creator" — both self-declarations, taken to
their conclusion, agree that G (if it is byte-for-byte what I described) is
a *conforming file*: under the rewriter reading the operation is simply
never performed (refused), so there is no G to disagree about; under the
creator reading, the resulting G is conforming per §21.6's own text. There
is no byte sequence where "rewriter-produced" and "creator-produced" G
differ in verdict, because the verdict does not consult provenance. I
therefore could not turn this into a genuine two-verdict fork, though I
think it is a real and useful thing to flag: the *entire protective purpose*
of `[R-WRT-06]` (preventing silent corruption of an MU=1 type's undisclosed
internal references when relocated by a tool that cannot parse them) is
available to be sidestepped by a tool that simply declines the "rewriter"
label for an operation that is, functionally, exactly a rewrite. This
does not change what bytes a verifier accepts, but it does mean `[R-WRT-06]`
protects only against tools that *admit* to being rewriters.

I looked for whether `[R-WRT-06]`'s refusal duty is itself declared a
*conduct-only* rule the way three specific rules are in §2.3
(`[R-CNF-02]`): "§6.3's flags rules against a set ignore-lane bit (a
creator's flags = 0, and an updater's copy-forward and set-no-other, §20.3
step 6 and §20.5), §6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's
pad, and §20.3 step 4's bar on the fixed declarations of a layer that
stores a tile are the cases this text states, and each is declared where it
arises rather than enumerated here." Note precisely: this list names three
things, and `[R-WRT-06]` is not one of them, nor is the §20.4 layer-drop
block. I went to §20.5 (where `[R-WRT-06]` is stated) looking for the kind
of explicit disclaimer §2.3's list-items each get at their own site (e.g.
the ignore-lane-bit rule is disclaimed again at §6.3 itself: "a set
ignore-lane bit is not a file-conformance violation"). §20.5 states
`[R-WRT-06]`'s refusal duty and its rationale ("such a type can define
references this specification does not... so its bytes cannot be safely
relocated") but never says, the way §6.3 and §21.7 do for the other three,
that violating it leaves the file's conformance status untouched. I record
this as Finding adversary-01 (AMBIGUITY, non-byte-level on the reasoning
above, but a genuine gap in how far `[R-CNF-02]`'s "declared where it
arises" principle actually reaches).

### 3.4 §20.3 step 4's scope sentence and the paragraph it closes (decision 4)

Quoted:

> This bar binds the commit as an actor: no file is nonconforming by virtue
> of its violation, and no register row records the violation itself, the
> register enumerating file-conformance violations (§21.1) and the bar
> stating no condition a file can exhibit (§21.7, `[R-ERR-01]`,
> `[R-CNF-02]`); a file such a commit leaves can be nonconforming on its
> own terms, as the paragraph below sets out. [...] The bar binds a layer
> the commit keeps and nothing else: a commit MAY drop the layer (§20.4)
> and add a new one under its name and other declarations, the new layer
> being new whatever bytes its entries address, the dropped layer's former
> extents included, §5.2's partition being over the new state alone. What
> the bar removes is a re-declaration carried as the same layer over the
> tiles it stored.

I confirmed this is explicitly, deliberately stated (not an implicit gap):
an appender that wants to change a fixed declaration of a layer that still
stores a tile — something step 4's main list flatly forbids while the
layer is "kept" — can achieve the identical practical effect in one commit
by dropping the old layer record (licensed unconditionally for the layer
type, since 0x0001 is registered PE=0, so the table's third row always
applies to it, subject only to §20.4's unimplemented-critical-sub-record
block discussed in §3.1 above) and adding a new layer record under the same
name with whatever new declarations it likes, including one whose tile-index
entries point at the *same physical bytes* the dropped layer's entries used
to address (explicitly licensed: "the new layer being new whatever bytes
its entries address, the dropped layer's former extents included").

I tried to build this into a genuine two-verdict fork and could not, for
the reason the paragraph itself gives up front: this whole class of rule is
declared, by name, a *conduct* rule ("§20.3 step 4's bar on the fixed
declarations of a layer that stores a tile" is one of the three specific
examples in §2.3's `[R-CNF-02]` list quoted in §3.3 above) — so whichever
way an appender does this (honestly re-declaring in violation of the bar,
or legally drop-and-recreate), the *file* conformance verdict is
unaffected by which path was taken, since the predicate is on bytes alone
and (per §9.7's Note) a verifier "certifies what a reader can reach... which
does not depend on reconstructing the file's history." I next tried the
sharper version of this same attack: is it possible for a drop-and-recreate
substitution to leave the *live* generation, examined entirely on its own,
in a state some register row *does* catch (making it a genuine, witnessed
tile/layer-scope violation rather than an unwitnessed conduct question)? I
worked one degenerate case through in full:

**Concrete degenerate case — the C=1 numeric layout flip.** Consider a
layer with exactly one numeric channel (C=1) that stores tiles, declared
`layout = 1` (interleaved). §14.4's own Note states: "A single-channel
numeric layer produces byte-identical tile images under either layout." I
verified this by hand from the byte-layout formulas in §14.1/§14.2:

- disk ordinal: interleaved is `s`; planar is `c·N + s`, and with C=1,
  `c=0` always, so `0·N + s = s` — identical.
- addressed-tile count / `entry_count`: interleaved `N`; planar `C·N`;
  with C=1 these are both `N` — identical, so the same index region
  (same entry_count, same `extent_length` formula, same
  `crc_of_crc_array`) is valid under either declared layout.
- decoded size: interleaved `P·Q` where `Q = ΣBᵢ` over all channels — with
  one channel, `Q = B`, so `P·B`; planar numeric is `P·Bᶜ = P·B` for that
  one channel — identical.
- byte offset of value k: interleaved `(k div C)·Q + F_{k mod C}` — with
  C=1, `F_0 = 0` and `k div 1 = k`, so offset `= k·B`; planar is `k·Bᶜ =
  k·B` — identical.
- filter (byte-shuffle) stride: interleaved stride is `Q = B`; planar
  stride is the channel's element size `= B` — identical, so filtered
  bytes are identical too.
- padding content (§14.5/T4): the fill value used is the same single
  channel's fill either way.

So a commit that changes **only** the `layout` byte of such a layer's
record (1→2 or 2→1) while leaving every stored tile's bytes, the index
region, and every other declaration untouched produces a live generation
that is bit-for-bit indistinguishable, at every check the register defines
(T3's decoded-size check, L21/L22's entry_count cross-checks, T4's padding
check, `[R-COD-10]`'s stride check), from one where the layout was declared
correctly from the start. This is a real, concrete instance of the very
claim the changed passage itself makes two sentences earlier — "but for a
stored tile's decoded size, a padding position or pad bit, or a boolean
byte the register witnesses (T3, T14, T21, T22, T4, T5, T2)... no check any
actor owes able to see it" — and it is *not* a defect in the document: the
document already discloses the coincidence at §14.4 ("A single-channel
numeric layer produces byte-identical tile images under either layout"),
just not in the same breath as §20.3's fixed-declaration bar. Since (as
established above) the bar's violation is expressly conduct-only and does
not touch file conformance, this coincidence does not produce a verifier
fork either — I record it as Finding adversary-04, an OBSERVATION, not
because it is wrong but because it is a fully worked confirmation, at
concrete byte level, of a claim the changed text makes about itself.

I also checked whether §20.4's layer-drop mechanism (§3.1 above) leaves any
trace comparable to the above in the *new* live state that could make
"this layer was illegitimately dropped past an MU=1 block" a witnessed
condition. It cannot: once a layer record is dropped, its record and its
unimplemented sub-record are gone from the live directory entirely (they
fall to slack, per §5.2/`[R-CNT-21]`), and a verifier's ordinary coverage
walk "walks the live state only" (§9.7) and is not required to run §9.6's
backward recovery probe at all. There is nothing in the resulting bytes for
a verifier to disagree about.

## 4. Attack surfaces I tried and what forecloses each

I built or attempted each of the following, in the spirit of the charter's
own list, specifically against the changed material and its immediate
neighbourhood. For each: the construction, and the sentence that closes it.

1. **Drop-then-recreate to dodge the fixed-declaration bar** (§20.3 step
   4). Construction: commit drops layer L (codec=1, stores tiles), adds a
   new layer named L with codec=2 and freshly-encoded tiles, in one commit.
   Verdict: explicitly licensed by the very sentence under review ("a
   commit MAY drop the layer (§20.4) and add a new one under its name and
   other declarations"). Not an attack surface at all — it is a stated
   permission, and I could not find a boundary case (zero channels, zero
   dimensions, C=1) where it produces two different verdicts, only ones
   where (§3.4 above) the *violation* form of the same idea is
   undetectable but also inert to conformance.

2. **Implemented-MU=1 sub-record surviving a layer drop** (§20.4).
   Construction: layer L carries one MU=1 sub-record of a type the
   updater privately implements; commit drops L. Verdict: permitted by
   the letter of the text (§3.1 above), but not constructible today as a
   two-verdict fork because format major 1's registry defines no MU=1
   type at all (§7.3, §10.2, Appendix C) — there is no way to make "the
   updater implements this MU=1 type" a fact about the *bytes* rather
   than about a private, unregistered convention outside this
   specification's own value sets. Closed for now; flagged as a live
   reading for future registrations (Finding adversary-02).

3. **Rewriter-refusal dodge via self-declared "creator"** (§20.1,
   `[R-WRT-06]`). Construction in §3.3 above. Verdict: does not fork a
   verifier's verdict, because `[R-CNF-02]`'s "pure predicate on bytes"
   framing (§2.3) means no rule about which *actor* produced a file can
   ever, by itself, change what a verifier — who sees only the resulting
   bytes — must conclude. Closed by that principle, though the principle
   is not spelled out at `[R-WRT-06]`'s own site the way it is for the
   three rules `[R-CNF-02]` names by example (Finding adversary-01).

4. **Zero-channel / zero-dimension degenerate layers under the changed
   text.** I checked §11.1's Rationale (also touching the "only remaining
   zero grid count" phrase) against §20.3 step 4's re-emission trigger for
   an edge case: a layer with two zero-extent dimensions, one grown to
   nonzero while the other stays zero (spatial-tile count N stays 0, index
   stays empty — directory-only re-emission), versus a later commit that
   grows the *last* remaining zero dimension (N goes from 0 to positive,
   full re-emission required since there was no index region to have
   before). I worked through the arithmetic (`⌈Eᵢ/Tᵢ⌉`, `N = ∏Gᵢ`) and
   found the document's own text draws this line correctly and
   consistently for every case I tried, including a genuinely degenerate
   one-dimensional layer (d=1) and a channel count of exactly 1.
   Foreclosed by §11.2's exact formulas and §11.1's Rationale as quoted.

5. **Overlapping the dropped layer's old extent with the new layer's new
   extent, deliberately, to test the ownership-once rule** (§7.2,
   `[R-CNT-13]`). Construction: new layer's tile-index entries address
   exactly the bytes the dropped layer's entries used to address (licensed
   explicitly, see attack 1). I checked whether this could ever create a
   double-claim inside the *same* commit's live state: it cannot, because
   the old layer record (the only structure that formerly claimed those
   bytes) is not present in the new directory at all — there is exactly
   one claimant (the new layer) in the live state that results, which is
   what §7.2's "extents are owned exactly once... within the live
   committed state" actually requires. Foreclosed by the ownership rule
   being defined over the live state alone, never across generations.

6. **Boundary values on the registered decisions' own numbers.** I checked
   entry_count = 0 / 1 / 2¹⁶ (segment boundary) / 2³²  (the §21.9
   guarantee) against §7.4's `crc_of_crc_array` rule ("0 when entry_count =
   0") and §15.4's segment formula, specifically for a layer whose
   `layout` field is being flipped per attack in §3.4: at entry_count = 0
   there is no index region to compare at all (extent slot forced to
   (0,0) either way), so the C=1 layout-flip observation is vacuous there
   and only bites once entry_count ≥ 1. I did not find a new boundary
   defect; §7.4's and §15.1–§15.4's own arithmetic already handles
   entry_count = 0 explicitly and consistently with the rest of the
   document.

None of these six produced two conforming-verifier verdicts I could stand
behind as genuinely forking on the same bytes. My overall reading is that
this cycle's five edited clauses, on their own text, hold together — the
labelled ones (§3.3's Note, §20.3's Example figure) are non-normative even
if flawed, and the one normative edit I could confidently identify
(§20.4's table row naming "an appender... and a rewriter..." in place of
"an updater") is an exhaustive, correct narrowing, since §20.1 defines
updater's tiers as exactly `{appender, rewriter}` and nothing else.

## 5. Rejected candidates (opened and closed)

- **§7.2's "one exception" vs. the general MU=1-reference license** — see
  §3.2 above. Closed: different populations (MU=0 exception vs. a
  free-standing MU=1 statement), not in tension.
- **§21.6's `[R-CNF-01]` convention check** — see §2 above. Closed: I found
  the one unlabelled, normative blockquote the brief said exists (§15.1's
  tile-index layout diagram) and it agrees with the table it restates; no
  defect there.
- **Figure bracket alignment in §20.3's Example and §20.5's compaction
  Example** — attempted via `figure_check.py`/`figure_check2.py`, hand-
  transcribed. Inconclusive both ways: my counted columns put figure (b)'s
  second bracket ("└───────┘ every entry, re-emitted") roughly under
  `index′` rather than under `+tiles`, which is the semantically correct
  target (the index, not the new tiles, is what gets "every entry,
  re-emitted"), and figure (a)'s two brackets land roughly under `A:
  tiles+index` and the slack run respectively, both semantically correct.
  I could not rule out a one-column shift either way given how box-drawing
  and subscript glyphs can render at inconsistent widths across tools —
  see `confidence_empty` below. I am not filing this as a finding because I
  cannot verify it, not because I am confident it is clean.
- **A commit growing a layer's rank, channel count, or tile extents past
  §21.9's stated minimum guarantees while flipping layout** — I checked
  whether any of §21.9's hard limits (rank ≤ 255, channel count ≤ 65,535)
  interact with the C=1 layout-flip observation. They do not: the
  observation is about C=1 specifically (the smallest legal channel
  count, `[R-GEO-01]`'s floor), and nothing about the upper bound changes
  its conclusion.
- **A user-metadata document's ordering rule (`[R-MTA-05]`) interacting
  with the drop-and-recreate trick** — user-metadata records are
  explicitly carved out of the "shape (c), directory-only" family
  ("Editing user metadata is not shape (c): its document lives in an
  extent... so a new extent is appended and the old one becomes slack, as
  in (b)") and are separately barred from ever being *removed* from a
  scope the commit keeps ("A commit never removes a user-metadata record
  from a scope it keeps"). I checked whether "a scope it keeps" has any
  gap when a layer is dropped-and-recreated under the same name (is the
  new layer "a scope [the commit] keeps," making its user-metadata
  sub-record grand-fathered from the old layer?). It is not: the new layer
  is explicitly "new... whatever bytes its entries address," so its
  user-metadata sub-record (if any) is the new commit's own fresh record,
  unrelated to the dropped layer's old one, which went to slack with the
  rest of the dropped layer. No gap.

## 6. Findings

See the structured `findings` array for the formal entries
(`adversary-01` through `adversary-04`). Summary:

- **adversary-01** (AMBIGUITY) — `[R-WRT-06]`'s rewriter-refusal duty (and,
  by the same reasoning, the layer-scope MU=1 block in §20.4) is not
  declared a conduct-only rule the way the three examples in §2.3's
  `[R-CNF-02]` are, even though it is structurally identical to them (an
  updater obligation that becomes unwitnessable once the record or its
  scope leaves the live state). A self-declared "creator" can produce, in
  one step, output a self-declared "rewriter" performing the identical
  copy-and-relocate operation must refuse. I could not turn this into a
  verifier-verdict fork, because `[R-CNF-02]`'s pure-bytes-predicate
  principle forecloses it regardless — but the text never says so directly
  for this specific rule, unlike the three it names.
- **adversary-02** (AMBIGUITY) — the §20.4 layer-drop block's condition
  ("a sub-record of a type the updater does not implement with MU = 1")
  textually excludes an *implemented* MU=1 sub-record from blocking its
  layer's drop, even though MU=1 forces PE=1 and an implemented,
  effectively-PE=1 record is otherwise treated (per the table) as
  "Retain byte-identical" with no license to disappear along with its
  layer stated anywhere except this specific paragraph's blanket "go with
  it whatever their PE bits." Internally consistent on a careful reading,
  but not currently constructible as a concrete conforming file, since
  format major 1's registry assigns no MU=1 type.
- **adversary-03** (OBSERVATION) — the §20.4 table's third row narrows
  "an updater" to "an appender... and a rewriter" by name; I verified this
  narrowing is exhaustive (§20.1 defines updater's tiers as exactly these
  two) and found no gap. Reported as a decidable-but-worth-recording
  confirmation, not a defect.
- **adversary-04** (OBSERVATION) — a concrete, worked byte-level
  confirmation that a single-numeric-channel (C=1) layer's `layout` field
  is a "fixed declaration" (§20.3 step 4) whose violation while the layer
  stores tiles is completely unwitnessed by every register row I could
  find (T3, L21, L22, T4, `[R-COD-10]`), consistent with — and explained
  by — §14.4's own Note that such a layer's tile images are byte-identical
  under either layout value. Not a defect; a confirmed instance of the
  changed passage's own "no check... able to see it" claim.

I found no CONTRADICTION-class finding: every apparent tension I traced
resolved into either an explicit, deliberate design choice (the drop-and-
recreate license) or a closed scope (the §7.2 "one exception" reading).

## 7. On the calibration and what I did with it

I want to be explicit that I did not treat the calibration numbers, or the
"read the last nine entries" framing, or the round-history narration, as
evidence about the document — they describe *other rounds' outcomes*, not
this document's content, and I did not let a "the last round returned zero
and it was contested" narrative push me toward manufacturing a flag I could
not back with a quotation and a concrete construction. Where I could not
close an attack, I said so and named the sentence I believe closes it
(§4); where I found something real but not byte-level, I filed it as an
AMBIGUITY or OBSERVATION rather than inflating it, per the fifth
discriminator's warning about the "second sentence" trap and the general
instruction that a padded list of non-defects is worse than an honest empty
one. I am reporting four findings, none of which I believe clears the
byte-level bar on the evidence I could build, because I judge that to be
the honest result of this walk rather than because I ran out of ideas to
try — §4 lists six attempts and what forecloses each, and I would want a
reviewer to reopen any of them if they can find the crack I could not.
