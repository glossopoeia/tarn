# Working transcript — §20.3 step 4, extent shrink turning a real position into padding

## Access
Read only /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (sed ranges + grep).
No docs/, no git, no conformance/, no registry.json, no web. No other panelist output.
Runtime placed unrequested context in my window (a project instruction pointer and an
index of maintainer memory notes). Disregarded; not used as evidence.

## The construction, in the document's own terms
- Layer L, tile T stored in generation g (the generation the commit supersedes).
- Dimension x: E_x 6 -> 5. T remains addressed (G_x = ceil(E/T) unchanged) and stored.
- One in-tile position p that was real becomes padding (§11.3: coordinate >= E_i).
- p's stored byte already equals the channel's recorded fill, i.e. exactly what §14.5 /
  [R-SER-05] requires of a padding position. No byte of T changes.

## What §14 fixes for T, checked item by item against the step-4 list
Decoded size: §14.2 [R-SER-02] table gives P·B^c (planar) / P·Q (interleaved), with
P = prod(T_i) (§11.2). Extents do not enter. UNCHANGED.
Byte offset of any sample: same table, k·B^c and (k div C)·Q + F_{k mod C}. Extents do
not enter; in-tile ordinal is row-major over T_i for every linearization (§11.4).
UNCHANGED.
Codec and filter: not touched by the commit. UNCHANGED.
Set of padding positions (§11.3): CHANGED — p joins it.
Content [R-SER-05] fixes there: at p the requirement is now "fill". The byte is already
fill. No required byte value changes anywhere in T.

So exactly one listed item moves, and it is the one the bar's next sentence addresses.

## The two sentences in tension (both normative prose, neither in a blockquote)

(1) The bar and its carve-out — lines 2995–3012:
"A commit MUST NOT change a layer's declarations in a way that alters, for any tile that
layer stores **in the generation this commit supersedes**, what §14 fixes for its stored
bytes or how they decode — the set of padding positions (§11.3) and the content
[R-SER-05] fixes there, the decoded size, the byte offset of any sample within the
decoded tile image, or the codec and filter that produced the stored bytes. ... The test
is the effect on such a tile, and the list names where that effect arises rather than
standing on its own: a change that leaves every one of those tiles' stored bytes meaning
exactly what they meant — a filter whose mandated stride makes it the identity
([R-COD-10]), or a new padding position whose stored byte already holds the fill
[R-SER-05] fixes — is not what this bars."

(2) The shrink paragraph — lines 3033–3046:
"An extent MAY also **shrink**, and the bar above is the whole of the test, **in the
bar's own tense**: a shrink is permitted exactly where it alters nothing §14 fixes for
any tile the layer stores in the generation this commit supersedes. ... Unstoring that
tile in the same commit does not rescue it either, and for the same reason: the
quantifier is the superseded generation's, so a shrink that turns real positions into
padding of a tile stored there is barred whether or not the new state still stores it."

Read flat, (2)'s last clause captures the construction and bars it; (1)'s carve-out names
the construction and permits it.

## Why (1) governs

a. (2) opens by incorporating (1) *in full and exclusively*: "the bar above is the whole
   of the test". A freestanding shrink test would be an addition to the test, which that
   sentence denies exists. (2) then states the biconditional in the bar's own vocabulary:
   permitted "exactly where it alters nothing §14 fixes". Under that biconditional the
   construction is permitted, because (1) tells us a new padding position already holding
   the fill is not an alteration in the relevant sense.

b. The clause is introduced by "so", drawn from one premise: "the quantifier is the
   superseded generation's". A premise about *tense* cannot generate a conclusion about
   *what counts as damage*. The derived content is the rider "whether or not the new
   state still stores it"; "is barred" is carried in from (1), exception and all. The
   antecedent chain confirms it: "that tile" refers back to "a prior-generation stored
   tile" that the commit *damages*. The whole paragraph answers the rescue question
   (does de-addressing or unstoring rescue? no), not the damage question.

c. Dead-letter test. Under the flat reading of (2), (1)'s second carve-out has no
   instance anywhere in the format. A new padding position on a prior-generation stored
   tile requires G_i·T_i - E_i to rise for a tile that stays addressed. Growth never
   creates padding (it converts padding to real). Any change to T_i, rank, or channel
   count moves decoded size or a sample's byte offset (§14.2 table) and so is barred by
   other list items and fails "meaning exactly what they meant". The only producer is an
   extent shrink of exactly this shape. So the flat reading of (2) repeals a clause of
   (1) entirely. The converse is not true: under the reading I adopt, every sentence of
   (2) still does work — it settles the tense/quantifier question. The asymmetry is
   decisive.
   (Contrast the sibling carve-out, which is plainly live: §17.3 [R-COD-10] makes
   byte-shuffle the identity at s = 1 for a packed boolean plane, so a filter
   redeclaration on such a layer changes nothing. Two carve-outs, one per list item.)

d. Corroboration, non-normative and used only as corroboration ([R-CNF-01]): §11.1's
   Rationale (line ~1487) states the shrink bar as "a shrink is barred wherever it
   alters what §14 fixes for such a tile — whether or not the new state still stores it".
   The alteration test, not a real-to-padding test; the rider travels with it exactly as
   in (2), which is what (2)'s clause is.

e. §21.7's cited consequence is about the unstore case, not this one: "a commit that
   supersedes every tile it would have damaged leaves the live state clean" — "would have
   damaged" presupposes damage established elsewhere, i.e. by (1). In the construction
   the live state is clean because there is nothing to witness, not because a witness is
   missing.

## Byte-level consequence
Yes, at byte level. Under (1) the appender emits a directory-only commit (§20.3's shape
(c)) — grid counts unchanged, so entry_count is unchanged and [R-CNT-17] compels no
index re-emission; the layer's extent slot still points at the existing index region;
the file grows by dir2 + pad + trailer. Under the flat (2) the commit is prohibited
outright: the writer must instead create a new layer or rewrite under a fresh file_id
([R-LIF-01], §20.5), producing an entirely different file. Two conforming implementations
reading only this document, one following (1) and one following (2), emit different bytes
for the same caller request — or one emits nothing at all.

## Verdict
READING_A_GOVERNS — permitted. The tension is real and is a drafting defect worth
flagging (an implementer reading the shrink paragraph alone answers "barred"), but the
document settles it: (2) expressly makes (1) the whole of the test, and only (1)'s
reading leaves every clause of both passages with work to do.
