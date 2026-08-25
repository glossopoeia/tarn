# Cross-hunk consistency audit — ADR-0099 (3 hunks)

> *Editorial substitution for the repository's vocabulary gate: an ordinary-English
> use of a gate word has been replaced with an exact synonym. The substitution is
> recorded here and changes no finding, quotation or verdict.*

## Access / disclosure

Read: spec/tarn.md (targeted ranges + whole-file normalised regex searches);
hunk-01.diff, hunk-02.diff, hunk-03.diff. Did NOT read full.diff, docs/,
conformance/, registry.json, git history, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, README.md. Did not list the case directory (globbed only the
three hunk-NN.diff names I was told exist).

Unrequested context appeared before I began: a project CLAUDE.md pointer, a
user auto-memory index naming several memory files, and a git-status/recent-
commits block including commit subject lines. I did not open any of those
files. The recent-commit subject line for this commit was visible in that
block; I did not use it to decide anything — every grouping and finding below
is derived from the hunk text and the spec — but it is disclosed as a breach
of the clean-room boundary because it named the commit's own intent.

## Grouping (derived from the text, not the section numbers)

Group A — "the same named header quantity": **entry_count** (layer record
trailing fixed field, §7.4; = the addressed-tile count, §11.2).
  - hunk-01, §11.1 Rationale (inside a ">" block — non-normative, [R-CNF-01])
  - hunk-02, §13.3 "Note — sparse writing" (inside a ">" block — non-normative)
Both rewrite the *growth* trigger for "the layer's whole tile-index region is
re-emitted" from a grid-count formulation to an entry_count formulation.

Group B — the slab packing invariant.
  - hunk-03, §16.2 [R-SLB-03] (normative body text, not a ">" block)
This is the "fix moved from a register row into the rule": row L41 (§21.3)
already read "plus **the previous stored tile's** length"; the rule read
"plus **its** length". Under §21.1 ("where a row and the rule it cites
diverge, **the rule governs**") the row's disambiguation had no force, so the
sweep direction is correct.

## Rule each repair adopts, in my words

hunk-01: For a layer, a commit that grows extents and leaves entry_count at
the same value changes nothing outside the directory; a commit that grows
extents and changes entry_count necessarily changes extent_length too
([R-CNT-17]'s formula), hence re-emits the whole tile-index region and
renumbers disk ordinals per [R-GEO-06]. The zero-product case (one grid count
rises while another stays 0) is the named instance of the first class; the
growth that clears the *last* zero grid count is the named instance of the
second.

hunk-02: A commit re-emits a layer's whole tile-index region when it changes
that layer's stored-tile set, or when it grows extents such that entry_count
changes.

hunk-03: Inside a declared slab run, a stored tile's offset equals its
ordinally-preceding stored tile's offset plus *that preceding tile's* length
(not its own).

## Searches run (whitespace-normalised, so hard wrap cannot hide a hit)

python3 regex over a flattened copy of spec/tarn.md for:
  entry_count (grep -n, 30 hits), grid count, addressed-tile count,
  addressed tile, zero addressed, extent_length, extent slot, grow,
  tile-index region, index region, re-emit, grid boundary (0 hits anywhere),
  packed/packing/contiguo, previous, R-SLB-0[1-5], R-CNF-01,
  "stored-tile set or index" (2 hits: line 606 and line 2987).

Key outputs:
  - "grid boundary" now appears nowhere in the document (the old §13.3
    phrase was the only occurrence) — nothing left to sweep on that phrase.
  - "previous" appears at 4 places only: 58 (unrelated), 2159 (the repaired
    rule), 3522 (L41), 3551 (T13, unrelated), 4342 (Appendix reproducible-
    build profile, a different rule about whole-file emission order).
    => hunk-03's sweep is complete; no other restatement of the packing
    arithmetic exists in the document.
  - Restatements of the re-emission trigger:
      line 606  (§5.1 Example, ">" block): "A commit that changes a layer's
        stored-tile set or index content re-emits that layer's whole
        tile-index region as well, at a new placement (§20.3, [R-WRT-04])."
      line 2987 (§20.3 step 4, NORMATIVE, under "An appender MUST, in order"):
        "Every layer whose stored-tile set or index content this commit
        changes has its tile-index region re-emitted in full ... (a geometry
        change renumbers ordinals wherever [R-GEO-06] moves them)."
      line 1496 (hunk-01), line 1791 (hunk-02).
      line 3102 (§20.3 Note): "any change to a layer's stored-tile set
        re-emits that layer's whole tile-index region" — cost commentary,
        no exhaustiveness claim.

## Check 2 — citations opened and read

[R-CNT-17] (line 1038): "Under index_encoding 1, extent_length MUST equal
entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 (and 0 when entry_count is 0); a
mismatch, or an entry_count that does not equal the geometry-derived
addressed-tile count, is a validity error at layer scope."
  hunk-01 claims: "Growth that changes entry_count changes extent_length with
  it ([R-CNT-17])". PASS. The formula is strictly increasing in entry_count,
  so distinct entry_counts force distinct extent_lengths. Note the quantifier
  shift: [R-CNT-17] is a static per-file predicate; the repair uses it
  diachronically across two generations. The shift is safe *only* because the
  function is injective — worth recording, it passes.

[R-GEO-06] (§11.4): "The disk tile ordinal, which orders tile-index entries
(§15), is s for an interleaved layer, and c · N + s for a planar layer".
  hunk-01: "disk ordinals renumber wherever [R-GEO-06] moves them". PASS
  (the "wherever" hedge is correct: growth of the first-declared dimension
  alone moves no existing ordinal).

§11.2: defines Gᵢ = ⌈Eᵢ / Tᵢ⌉, N = ∏Gᵢ, addressed-tile count = N interleaved /
C·N planar. PASS for hunk-01's "grid count ⌈Eᵢ / Tᵢ⌉ (§11.2)" and for
"the product holding at 0".

§20.3 / [R-WRT-04]: PASS as a citation for "the region is re-emitted" in the
entry_count-changes direction (entry_count change ⇒ entry-array length change
⇒ index content change). FAILS as a warrant for the *converse* (hunk-01's
first sentence) — see finding X-02.

§11.1 as cited by hunk-02: FAIL. §11.1 contains [R-GEO-01] and [R-GEO-02];
neither mentions re-emission, entry_count, or extent_length. §11.1's only
statement of the cited proposition is the Rationale blockquote that hunk-01
rewrote in this same commit — a non-normative citation target. See X-03.

§21.1 (row-vs-rule precedence): "where a row and the rule it cites diverge,
**the rule governs**". Opened, PASS, and it is what makes hunk-03 necessary.

L41 (§21.3, line 3522): "Inside a slab run, a stored tile's offset ≠ the
previous stored tile's offset plus the previous stored tile's length (gap,
overlap, or out-of-ordinal placement; sentinels and entries §15.3 classifies
reject-tile on a structural ground are transparent, an entry failing only its
stored bytes' crc is not) | gap; overlap; out-of-ordinal placement | verifier
| certification | [R-SLB-03] (R-IDX-03)". PASS — row and repaired rule now
state the same relation, same transparency carve-outs, same three instances.
L42 ("A slab run's first stored tile's offset is not a multiple of A_slab")
also matches the untouched second half of the repaired sentence. PASS.

[R-CNF-01] (line 104): "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*; and
appendices identified as non-normative." Confirms hunks 1 and 2 carry no
force; hunk 3 is normative body text.

## Check 3 — where the rules sit

hunk-01: every line of the hunk begins ">" and the block is headed
"> **Rationale.**". Non-normative.
hunk-02: every line begins ">" and the block is headed "> **Note — sparse
writing.**". Non-normative.
The normative statement of the same rule is §20.3 step 4 (line 2987) and it
was NOT edited by this commit. So both repairs are restatement maintenance,
and a divergence between them and line 2987 leaves line 2987 in force.
hunk-03 is normative ([R-SLB-03] body), and its register row already agreed.

## Check 4 — contradiction inside the passage, untouched text included

§11.1 Rationale, sentences immediately before hunk-01's edit (untouched):
"a shrink is barred wherever it alters what §14 fixes for such a tile ...
One shrink can do several of these at once. A layer that stored nothing may
be re-declared freely."
§20.3 (untouched, normative): "an extent MAY **grow** ... An extent MAY also
**shrink**". A single commit may therefore do both, to different dimensions
of one layer.
Worked counterexample (all values legal under [R-GEO-01]): rank-2
interleaved layer, C = 1, T = (1,1), E = (2,3) → G = (2,3), N = 6,
entry_count = 6. One tile stored, at tile coordinates (1,0); under
[R-GEO-06] its disk ordinal is 1·3 + 0 = 3.
Commit grows E₀ 2→3 and shrinks E₁ 3→2. New G = (3,2), N = 6,
entry_count = 6 — unchanged. The stored tile is still addressed and still
stored; its disk ordinal is now 1·2 + 0 = 2.
Legality: the shrink de-addresses only tiles at t₁ = 2, none of them stored;
Gᵢ·Tᵢ = Eᵢ in both states so there is no padding at all, P = 1 so decoded
size and every sample's byte offset are unchanged, codec and filter
unchanged — so it "alters nothing §14 fixes for any tile the layer stores in
the generation this commit supersedes" and §20.3 permits it.
Consequence: index content changes (entry 3 was non-sentinel, entry 2 is
now), entry_count does not. §20.3 step 4 MUST re-emit. hunk-01 says such a
commit "touches the directory alone". Contradiction. See X-02.
§21.7 confirms the resulting file has no witness: "the ordinal mappings of
[R-GEO-06] and [R-SER-01] are satisfied by a structurally valid tile
whatever values it carries" — so a writer misled by the Rationale ships a
file that verifies clean and reads the wrong tile.

§16.2, whole [R-SLB-03] paragraph re-read around hunk-03: the transparency
carve-outs ("Sentinel tiles are transparent to run continuity"; structural
reject-tile entries transparent; "An entry whose only defect is that its
stored bytes fail its crc is not transparent — its offset and length stand,
and the packing relation reads them as it does any other stored tile's"; "A
run with no stored tiles imposes nothing") all remain coherent with the
disambiguated relation: "the previous stored tile" skips transparent
entries, and a crc-failing entry supplies the length term for its successor.
No collision. hunk-03 passes check 4.

## Check 5 — exhaustive words

hunk-01: "every grid count" is GONE (that was the old text's exhaustive
claim). Remaining: "unchanged", "alone" ("touches the directory alone" — an
exhaustiveness claim about what the commit touches; falsified by the
counterexample above), "**last** zero grid count" (a definite description
implying a unique such growth; see X-04).
hunk-02: "each commit that ..." — a positive list of two triggers, not
closed by an "only", so it undershoots rather than overclaims.
hunk-03: "for every run", "each stored tile", "the first stored tile" — all
carry. ("each stored tile" is vacuous for a run's first stored tile, which
the following clause governs instead; pre-existing and harmless.)

## Check 6 — what the repairs left unconstrained

Structure: the layer record's geometry + index-addressing group —
{d dimension entries (Eᵢ, Tᵢ), rank d, layout, channel count C,
index_encoding, entry_count, crc_of_crc_array, extent_offset, extent_length}
plus the derived {G₀…G_{d−1}, N, disk-ordinal map}.

Pinned by the repairs: entry_count (named), extent_length (via [R-CNT-17]).
Pinned elsewhere, checked: extent_offset — §20.3 "necessarily at a new
placement ([R-LIF-01])" for a re-emitted region, and "A layer whose record
alone changes keeps its extent slot" for the unchanged case. OK.
crc_of_crc_array — [R-CNT-23] (static: CRC over the segment-CRC array; 0 when
entry_count = 0) plus row L37. OK, statically constrained in the new
generation whether or not the Rationale mentions it.

NOT pinned: **the factorisation (G₀ … G_{d−1}) / the disk-ordinal map.**
entry_count is the *product*; [R-GEO-06] reads the *factors*. Two states can
share entry_count and have completely different ordinal maps. For a
pure-growth commit the factors are recoverable from the product (grid counts
are monotone non-decreasing under growth, so an unchanged non-zero product
forces every factor unchanged), which is why the repair looks sound; the
moment one dimension shrinks in the same commit the product stops
determining the factors. The old wording pinned the factors and mishandled
the zero product; the repair fixes the zero product and unpins the factors.
That is the sibling-quantity shape, and it is X-02.

Also unpinned by the repaired passage, though covered by rules elsewhere:
a *re-declaration* of a layer that stored nothing — the sentence
"A layer that stored nothing may be re-declared freely" sits immediately
before hunk-01's text, and such a re-declaration can change Tᵢ, C, layout or
rank and so change entry_count with no growth at all (E = 100, T 32→16 takes
entry_count 4→7). Neither repaired sentence reaches it, since both are
quantified over "growth". [R-CNT-17] still forces the new extent_length and
§20.3 still forces the re-emission, so nothing is left undetermined — but
the Rationale, read straight through, invites the opposite conclusion.

hunk-03's structure (a slab run): stored-tile offsets (pinned by the repaired
relation), stored-tile lengths (index entries, §15.2), first stored tile's
A_slab residue (pinned), run partition and block boundaries ([R-SLB-02]),
inter-run bytes (slack, [R-SLB-05], §5.2), staleness after a commit
([R-SLB-04]). Every member of the set is governed. hunk-03 passes check 6.

## Check 7 — analogies / warrants, verb by verb

hunk-01: "Growth that changes entry_count **changes** extent_length with it
(`[R-CNT-17]`)" vs [R-CNT-17]'s "extent_length **MUST equal** entry_count ×
20 + ⌈entry_count / 2¹⁶⌉ × 4". Different verbs, different ranges: the cited
rule quantifies over one file's layer record (a static equality), the repair
over an ordered pair of generations (a difference). The inference is
nevertheless valid because the cited function is strictly increasing.
REPORTED AS PASSING.

hunk-01: "so the layer's whole tile-index region **is re-emitted**"
vs [R-WRT-04]'s "Every layer whose stored-tile set or index content this
commit **changes** has its tile-index region re-emitted in full". Ranges:
the repair keys on entry_count; the cited rule keys on index content.
entry_count-changes ⊂ index-content-changes, so this direction PASSES. The
repair's *first* sentence asserts the complement of the same analogy
(entry_count unchanged ⇒ nothing but the directory), and there the two sets
come apart. FAILS — X-02.

hunk-02: "so that entry_count changes, **re-emits** that layer's whole
tile-index region (§11.1, §20.3, [R-WRT-04])" — same comparison; the
positive direction passes, and the citation to §11.1 fails (X-03).

hunk-03: no analogy, no warrant citation added. Nothing to compare.

## Cross-vocabulary sweep (the checker's blind spot #1)

The proposition both hunks now rest on — *a growth that raises one grid count
while another dimension's extent stays 0 leaves the layer addressing no
tile* — is restated elsewhere in words that share no vocabulary with either
hunk (no "entry_count", no "grid count", no "re-emit"):

  §17.2, Note under [R-COD-07] (line ~2335, a ">" block):
  "> **Note.** The cap is quantified over the layer's *addressed* tiles,
  > so a layer that addresses none — any dimension extent 0
  > (`[R-GEO-02]`, §21.6) — satisfies it whatever its tile shape
  > declares, and codec 4 is conforming there. The escape is not
  > durable: a later commit that grows an extent addresses tiles, and
  > the same declarations are then measured against the cap."

The first half is right ("*any* dimension extent 0"). The second half is
exactly the claim hunk-01 was rewritten to deny: on a rank-2 layer with
E = (0, 0), a commit that grows E₁ to 100 grows an extent and the layer still
addresses no tile (N = 0·G₁ = 0), so the lz4 escape survives. Compare §20.3's
own untouched normative-adjacent sentence, which is careful and correct:
"[R-COD-07]'s lz4 decoded-size cap among them (L44), which an empty layer
escapes only because that cap is quantified over addressed tiles."
Unswept restatement — X-01.

## Direction of every disagreement

X-01: §17.2's Note changes. §11.1's arithmetic is right; §20.3 and [R-COD-07]
are right; only the Note overstates.
X-02: §11.1's Rationale and §13.3's Note change. §20.3 step 4 and §5.1's
Example ("stored-tile set or index content") are the correct rule and already
agree with each other.
X-03: §13.3's Note changes (drop §11.1 from the citation, or point it at
[R-CNT-17] which is where the entry_count arithmetic actually lives).
X-04, X-05, X-06: §11.1's Rationale changes.
hunk-03: nothing changes. Row and rule agree; the sweep is complete.

## Byte-level determination

hunks 1 and 2 sit inside ">" blocks; [R-CNF-01] makes them non-normative, so
an implementer who follows them against §20.3 is simply nonconforming under
[R-WRT-04], not exercising a second permitted reading. §17.2's Note is
likewise a ">" block against the normative [R-COD-07] and row L44. In every
finding below the normative text admits exactly one reading, so the set of
byte sequences a conforming writer may emit does not move: none of these are
byte-level. (X-02 is the one worth naming the near-miss on: the file a
misled writer produces — index region not re-emitted after an ordinal
renumber — is structurally conforming and unwitnessed per §21.7, so had the
defect sat in normative text it would have forked the bytes. It does not.)
