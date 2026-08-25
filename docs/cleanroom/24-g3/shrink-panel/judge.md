# Judge transcript — §20.3 step 4, fill-valued real→padding shrink

## Access

Read: spec/tarn.md only, via sed/grep/python over that one file.
Ran: wc, sed, grep, and one python3 regex pass over spec/tarn.md.
Read nothing else. Did not list or read the panel output directory.
Context I did not ask for: the runtime injected CLAUDE.md (which only
points at AGENTS.md) and an index of the maintainer's auto-memory files.
Both appeared before I began; I did not open the files they name and did
not use them. Disclosed, not acted on.

## Quotation check

Charter's Sentence A: accurate except it drops "(`[R-COD-10]`)" after
"makes it the identity". Lines 3005-3011.
Charter's Sentence B: verbatim. Lines 3041-3045.
Neither is inside a blockquote — both are indented list-item prose in
§20.3 step 4, no ">" prefix. Both normative.

Verified verbatim (all spec/tarn.md):

- 2994-3001 the bar: "A commit MUST NOT change a layer's declarations in
  a way that alters, for any tile that layer stores **in the generation
  this commit supersedes**, what §14 fixes for its stored bytes or how
  they decode — the set of padding positions (§11.3) and the content
  `[R-SER-05]` fixes there, the decoded size, the byte offset of any
  sample within the decoded tile image, or the codec and filter that
  produced the stored bytes."   VERIFIED
- 3011-3013: "Where a change does reach them it makes each stored tile it
  reaches nonconforming"  VERIFIED
- 3013-3018: "...re-emitting those tiles would strand the originals as
  slack ... Such a change is a new layer, or a whole-file rewrite under a
  fresh file_id"  VERIFIED
- 3022-3024 grow: "an extent MAY **grow**, since a position that becomes
  real held that channel's fill and fill is a legal sample value"  VERIFIED
- 3033-3036 shrink opener: "An extent MAY also **shrink**, and the bar
  above is the whole of the test, **in the bar's own tense**: a shrink is
  permitted exactly where it alters nothing §14 fixes for any tile the
  layer stores in the generation this commit supersedes."  VERIFIED
- 3036-3040: "Dropping a tile out of the addressed set (§11.2's grid
  count falls) is not itself such an alteration ... but neither does it
  rescue a commit that damages a prior-generation stored tile."  VERIFIED
- 3048-3051 cost sentence  VERIFIED
- 3051-3052: "Discarding data is the caller's operation and this
  specification does not bar it."  VERIFIED
- §14.2 [R-SER-02] table, lines ~1834-1836: decoded size P·Bᶜ / P·Q,
  offsets k·Bᶜ and (k div C)·Q + F_{k mod C}  VERIFIED — extent-free
- §11.2: "sample-position count per tile is P = ∏ Tᵢ"  VERIFIED
- §14.5 [R-SER-05] 1953-1963  VERIFIED
- §11.3 [R-GEO-04] 1524-1532  VERIFIED
- §3.2 [R-MDL-01]/[R-MDL-02] 343-360  VERIFIED
- §2.3 [R-CNF-02] "File conformance is a pure predicate on bytes"
  lines ~139-141  VERIFIED
- §21.4 T4 line 3541  VERIFIED — condition is "does not encode ... fill"
- §21.1 completeness clause, lines ~3352-3372, INCLUDING the sentence the
  A-advocates omit: "neither this completeness clause nor the instance
  arithmetic below reaches §21.6's defined non-violations, §21.7's
  account of what no check detects, or §21.9's limits."  VERIFIED
- §21.7 lines 3685-3689 and 3706-3710  VERIFIED
- §23.1 [R-PRV-01] lines 3931-3941  VERIFIED
- §11.1 Rationale lines 1484-1490 — blockquoted, non-normative  VERIFIED
- §20.3 Example (c) lines 3120-3127 — blockquoted  VERIFIED

Whitespace-normalised sweep: "turns real positions into padding" and
"already holds the fill" each occur exactly once. "becomes real" once
(the grow clause). There is no third site stating a real→padding rule.

## Mechanics of the construction

Only the padding set moves. P = ∏Tᵢ, and [R-SER-02] derives decoded size
and every byte offset from P, Bᶜ, Q, C — extents enter none of them. So
of the bar's four list items, three are untouched by an extent shrink
that leaves the grid count unchanged; the fourth (padding set + content)
gains a position whose required content is the byte already stored.

Also established: extent shrink is the ONLY producer of "a new padding
position" on a tile whose other §14 quantities are unchanged. A tile-
extent change moves P (decoded size). A rank, dimension-order, layout or
channel change moves offsets or decoded size. Growth removes padding, it
never creates it. This is the premise the dead-letter test needs and it
holds.

## Decision

READING_A_GOVERNS.

### 1. The document names which passage controls (3033-3034)

"the bar above is the whole of the test, **in the bar's own tense**" is
an express incorporation clause, stated as a biconditional ("permitted
exactly where"). "The bar above" is the preceding paragraph, and Sentence
A is in it — indeed Sentence A is that paragraph's instruction on how the
bar's predicate applies. Sentence B sits inside the paragraph governed by
the incorporation clause. A paragraph that declares the prior passage the
whole of its test cannot then enlarge it. The bolded "in the bar's own
tense" names the single dimension being adjusted: the quantifier. That is
also the only premise Sentence B offers for itself ("the quantifier is
the superseded generation's"), and a premise about which tiles are tested
cannot yield a conclusion about what counts as damage.

This is the answer to "is there a rule that picks between them". §21.1's
divergence rules reach rows and §21.6 entries only, so they do not; but
3033-3034 does, and it is normative.

### 2. The consequence test — decisive, and Reading B fails it

3011-3013: "Where a change does reach them it makes each stored tile it
reaches nonconforming." §20.3's own Example (c) restates the same
causation: a fill change on a layer storing a padded tile "would
invalidate every stored tile it reaches". And [R-CNF-02]: "File
conformance is a pure predicate on bytes."

T's bytes after the commit satisfy §14.1-§14.5 in every particular,
§14.5 at the new padding position included. T is therefore conforming.
By the contrapositive of 3011-3013, the change does not reach T. Reading
B must hold that a change is barred, reaches a stored tile, and yet
leaves it conforming — severing the bar from the consequence the section
states for it, and from the rationale that follows (re-emitting the
reached tiles strands the originals as slack). Under Reading B nothing
would need re-emitting, so the whole stated ground of the bar is idle.

### 3. Dead-letter asymmetry

Under Reading B, Sentence A's second carve-out has no instance anywhere
in the format (see mechanics above). It is repealed outright by a clause
two paragraphs down.

Under Reading A nothing is repealed. Sentence B keeps its whole job — the
rescue point, "whether or not the new state still stores it" — and its
antecedent remains a true description of a nonempty class (shrinks that
turn a real position holding non-fill data into padding, which are barred
and which fire T4). The bar's padding-set item is emphatically alive
under Reading A. Reading A costs one over-broad clause; Reading B costs
an express carve-out its entire application.

### 4. Reading B's best sites, weighed

(a) [R-PRV-01]'s "two ways". Real cost — Reading A adds a third way a
commit removes sample data, and uniquely there the byte does not become
slack. But the count is already inexact under Reading B: a shrink that
turns real positions into padding of an addressed-but-UNSTORED tile is
permitted under both readings, removes reachable sample data, de-
addresses nothing and puts no bytes in slack. And §23.1's operative
MUST NOT is quantified over "any commit that makes sample data
unreachable", so the requirement itself is unaffected under either
reading. A descriptive premise in a privacy section does not outweigh an
express carve-out in the operative bar.

(b) The cost sentence (3048-3051). Fails for the same reason: the
unstored-tile shrink is permitted under Reading B too, de-addresses
nothing and lowers no entry_count. The sentence describes the typical
shrink, not the permitted set, on either reading.

(c) §11.1's "permitted where it **only** drops tiles". Blockquoted
Rationale, non-normative under [R-CNF-01], and it defers in the same
breath ("§20.3 states normatively, and governs"). Its barred half states
an alteration test with the unstoring rider attached as a modifier —
which is exactly Reading A's grammar for Sentence B. Its permitted half
is over-narrow under both readings.

(d) B1's "meaning changed" (real→padding flips MUST-return to
MUST-NOT-return). The best B argument, and the document refutes it two
sentences before Sentence B: dropping a tile out of the addressed set
strips far more positions out of the reference array and "is not itself
such an alteration"; and "Discarding data is the caller's operation and
this specification does not bar it." Reference-array membership is not
the interest the bar protects. "Meaning" is scoped by the bar's own head
to "what §14 fixes for its stored bytes or how they decode" — and that
is satisfied by the byte already there.

(e) B2's "the grow MAY would be redundant under Reading A". False.
Sentence A's carve-out runs one direction only — a NEW PADDING position
whose byte already holds fill. Growth is padding→real and is not covered
by it; it needs and has its own express MAY. No redundancy.

### 5. §21.7 — both sides overstate it

A1, A2 and the control all argue §21.7 is falsified by Reading B. I do
not accept that. §21.7 hedges first — the bar "is witnessed only where
the affected tiles remain stored, and then only for part of what it
bars" — and then enumerates the witnessed parts. Reading B leaves an
unenumerated unwitnessed class, which is an omission, not a falsehood;
and §21.1 expressly excludes §21.7 from the completeness clause
("neither this completeness clause ... reaches ... §21.7's account of
what no check detects"). §21.7 gives Reading A mild corroboration
(its "a commit that supersedes every tile it WOULD HAVE damaged"
presupposes damage fixed elsewhere, matching Sentence B's rescue job)
and nothing stronger. My verdict does not rest on it.

### Register check

No row fires under either reading. T4 is satisfied (the padding position
does encode fill). T2/T5 are bool-specific. T3/T14 test lengths, which
are extent-independent. T15/T17/T23/T25/T26 need a codec, filter or
stride change. L21 wants entry_count = geometry-derived count: the grid
count is unchanged, so it holds. L22's extent_length formula is
unchanged. §21.6's entry at 3607 (coordinate outside extents → the
request fails as a request, no verdict on the file) is the only
reader-visible effect.

### Byte level

Yes. Under Reading A an appender emits a directory-only generation-2
append at the same file_id: re-emitted directory (one u64 extent field
6→5, every other record byte-identical per [R-WRT-05]), CRC, barrier,
pad, trailer; no tile byte and no index byte written; the layer keeps its
extent slot pointing at the existing index region. Under Reading B the
appender MUST NOT commit and is routed to "a new layer, or a whole-file
rewrite under a fresh file_id" — either a two-layer file with the payload
duplicated, or a fresh-file_id generation-1 rewrite. Different bytes.

### Finding for the maintainer

The document determines Reading A, but the collision is a genuine defect
and Sentence B is the sentence to repair: it states "is barred" flat where
the bar it incorporates carries an express exception. The minimal repair
is to carry the damage qualifier Sentence B's own preceding sentence and
§21.7 already use — e.g. "a shrink that damages a tile stored there by
turning real positions into padding is barred whether or not the new
state still stores it". §11.1's Rationale should lose "only" for the same
reason. Do not repair by striking Sentence A's second example: that
example is the sole thing reconciling the bar's list with the express
grow permission's neighbourhood, and striking it re-opens whether the
list stands on its own.
