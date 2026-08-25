# Cross-hunk consistency audit — r26b

## 0. Disclosure

Read: the four hunk files (hunk-01.diff … hunk-04.diff) and
/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (headings; §6.2–§6.4;
§7.1 [R-CNT-25]; §9.4–§9.7; §11.1–§11.3; §15.3; §16 whole; §17.2 [R-COD-06]–
[R-COD-08]; §19.1–§19.2; §20.3 whole; §20.4; §21.1; §21.2 whole; §21.3 rows
L1–L49; §21.6; §21.7 tail; §21.8; §21.9; §23.1–§23.2; Appendix G; Appendix H).
Ran: `wc`, `grep -n`, and three python3 whitespace-normalising searches over
spec/tarn.md only (no other file read). Did NOT read full.diff, docs/, PLAN.md,
OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, spec/registry.json, git
history, or the web; did not list the hunk directory beyond globbing
`hunk-*.diff`.

Unrequested context appeared before I began: a project-instruction pointer
(CLAUDE.md → AGENTS.md) and an index of the maintainer's memory files naming
prior rounds and prior findings. I did not open any of them and did not use
their contents; every conclusion below is anchored to a quotation from
spec/tarn.md or from a hunk file.

Note on the hunk headers: hunk-01's header says "line 1289, in §11.1's growth
Rationale" but line 1289 is inside §9.6 and its body is the recovery-scan
prose; hunk-02's header says "line 1489, in §9.6's recovery-scan note" but its
body is §11.1's growth Rationale. The two headers' *descriptions* are swapped
relative to their bodies and their line numbers. This is diff-file metadata,
not spec text, so it is not a finding. I audited by body, not by header.

## 1. The rule each repair adopts

**H1 — §9.6, [R-LIF-06] paragraph (normative prose).**
> "a file whose final 64 bytes are not a valid trailer fails `[R-CNT-06]`'s
> gates on the bytes handed over (§21.2 rows F8, F14 and F17 — the magic, the
> trailer CRC and the length cross-check)"

Rule made true of an implementation: a file handed to a reader or verifier
whose last 64 bytes fail the probe's three criteria is reject-file, and the
register records it at F8 and/or F14 and/or F17. Generation: the state handed
over, not the earlier state the probe finds (the next clause says so).

**H2 — §11.1 Rationale (blockquote, non-normative under [R-CNF-01]).**
> "growth that raises one changes entry_count and with it extent_length
> (`[R-CNT-17]`) — save where another dimension's grid count is 0, which holds
> the product at 0 and adds no entry — so where it does change, the layer's
> whole tile-index region is re-emitted"

Rule: raising a grid count Gᵢ does not by itself change entry_count; if some
other Gⱼ = 0 then N = ∏Gᵢ = 0 and the addressed-tile count (N or C·N) stays 0.

**H3 — §21.3 row L41 (register row).**
> "a stored tile's offset ≠ the previous stored tile's offset plus **the
> previous stored tile's** length"

Rule: inside a slab run, offset(k) = offset(k−1) + length(k−1) over stored
tiles in ordinal order. Pre-repair the row read "plus that tile's length",
which a reader could bind to the *current* tile.

**H4 — §23.1 (prose, [R-PRV-01] paragraph).**
> "editing a user-metadata document appends a new extent and strands the old
> one (§20.3 places this with shape (b))"

Rule: nothing about implementation behaviour; a cross-reference correction
asserting that §20.3 classifies metadata supersession under shape (b).

## 2. Grouping — by rule touched, not by section

Section numbers would group these 9.6 / 11.1 / 21.3 / 23.1. That is not the
grouping. Working from the text:

**Group α — "which register row records this failure".** H1 and H3. H1 names
three §21.2 rows as the registration of a trailer-gate failure; H3 rewrites a
§21.3 row so it registers the slab-packing failure precisely. Both are
completeness claims about register rows, and both are governed by §21.1:
> "each row *restates* its governing rule, and where a row and the rule it
> cites diverge, **the rule governs**."

**Group β — "where in the commit model this case is established".** H2 and H4.
Both point at §20.3 and assert where a consequence is fixed. H2's whole
paragraph opens "§20.3 states normatively, and governs, what a commit may do
to a layer that already stored tiles"; H4 corrects which §20.3 shape a
metadata supersession is placed with.

### 2a. Group α, internal agreement — and the disagreement

H1 and H3 do not touch the same rule, so they cannot contradict each other on
content. They disagree on **method**, and the disagreement is diagnostic.

H1 puts the authority in the rule and uses the rows as pointers: the sentence
reads "fails **`[R-CNT-06]`'s gates** … (§21.2 rows F8, F14 and F17 …)". That
is exactly what §21.1 licenses.

H3 puts the disambiguation **only in the row**. The governing rule is
[R-SLB-03] at §16.2, and it still reads (spec/tarn.md:2157–2159):
> "each stored tile's offset equals the previous stored tile's offset plus
> **its** length"

"its" is precisely the pronoun L41 was repaired to remove. So the same commit
demonstrates the correct convention in H1 and violates it in H3. Under §21.1's
own precedence clause the row cannot carry the fix. → finding X-01.

Direction: §16.2 is the text that must change, not L41. Appendix G item 3
independently confirms which reading the document intends — "each later
structure begins where the previous one ended" — as does §16.2's own
"contiguous and packed".

### 2b. Group β, internal agreement

H2 implies the carve-out commit re-emits no index region, i.e. it is §20.3's
shape (c) "A change confined to the directory". H4 implies a metadata
supersession is shape (b). §20.3 shape (c) already contains both halves:
> "A layer storing no tile is re-declared freely, subject to every rule its new
> geometry is subject to, which is the same step's permission. Editing user
> metadata is not this shape: its document lives in an extent (`[R-CNT-25]`),
> so a new extent is appended and the old one becomes slack, as in (b)."

H2's carve-out case is a layer storing no tile (addressed-tile count 0 ⇒ no
stored tile), so (c) covers it; H4's case is explicitly routed to (b). **The
two repairs agree.** No contradiction between them. Their shared blind spot is
what neither says — see X-05.

## 3. Search log — restatements of each repaired rule

Searches were run on a whitespace-normalised copy (newlines and leading "> "
collapsed), because the file is hard-wrapped.

### The slab-packing relation (H3)
Terms searched: `previous stored tile`, `plus its length`, `packed in ordinal
order`, `contiguous and packed`, `offset plus`.
Hits: exactly two loci — §16.2 [R-SLB-03] (says "plus **its** length") and
§21.3 L41 (repaired). Appendix G item 3 restates the idea for structures
generally ("begins where the previous one ended"); Appendix H says only
"alignment and slab invariants (§16)". §15.3/[R-IDX-03] restates the
transparency clause and matches L41's parenthetical verbatim in substance
("`[R-SLB-03]`'s run continuity closes over it as it does over a sentinel").
Conclusion: one unswept restatement, and it is the normative one. → X-01.

### The trailer gates (H1)
Terms: `trailer magic`, `transport-authoritative`, `fails its gates`.
Restatements found and checked:
- §6.2 [R-CNT-06] — "validate, in order: the trailer magic; the trailer CRC;
  the version gate … committed_file_length equals the file size". Agrees.
- §9.5 Note — "the magic, the CRC, or committed_file_length against the
  transport size, each of which §21.2 already registers". Same triple, no row
  numbers. Agrees with H1.
- §19.1 step 2 — "magic, trailer CRC, version gate, then the remaining field
  gates". Agrees.
- §21.2 preamble — "**F8 and F1's trailer-magic instance**, F14's trailer CRC
  — the two checks §6.2 places before the gate". Uses **four** row references
  for the same two pre-gate checks. H1 uses one for the magic. → X-04.

### entry_count under growth (H2)
Terms: `entry_count`, `zero-extent`, `empty layer`, `addresses no tile`,
`grid count is 0`, `grid count falls`, `touches the directory alone`.
Restatements found and checked:
- §7.4 field table — "entry_count | u64 | equals the addressed-tile count
  (§11.2, `[R-CNT-17]`)". Agrees with the carve-out.
- §7.4 [R-CNT-17] — "extent_length MUST equal entry_count × 20 + ⌈entry_count /
  2¹⁶⌉ × 4 (**and 0 when entry_count is 0**)". Agrees; the carve-out is the
  case this parenthesis already anticipates.
- §21.3 L21, L22, L27 — pin entry_count to the geometry-derived count,
  extent_length to the formula (including "a nonzero slot with entry_count =
  0"), and crc_of_crc_array to 0 at entry_count = 0. Agree.
- §20.3 growth clause — "`[R-COD-07]`'s lz4 decoded-size cap …, which an empty
  layer escapes **only because that cap is quantified over addressed tiles**".
  Agrees: stated as a property of the quantifier, which survives the carve-out.
- §21.9 — "A layer **addressing no tile** (§11.2) therefore has no tile whose
  decoded size the table bounds." Agrees, same reason.
- §17.2 Note (spec/tarn.md:2337–2339) — "The escape is not durable: **a later
  commit that grows an extent addresses tiles**, and the same declarations are
  then measured against the cap." **Does not agree.** → X-02.
- §11.1's own trailing clause — "the first growth of a zero-extent layer
  included". **Does not agree.** → X-03.

### Metadata supersession / shape (b) (H4)
Terms: `shape (b)`, `shape (c)`, `becomes slack`, `removes a layer`.
- §20.3 (c): "Editing user metadata is not this shape … as in (b)." Citation
  resolves; H4 is faithful.
- §20.4: "No commit therefore removes a layer record, or a user-metadata
  record at either scope." Agrees with §23.1's "no commit removes a layer at
  all".
- Appendix H, conforming updater: "never removes a layer record, or a
  user-metadata record at either scope (§20.4)". Agrees.
- §20.5: a compactor "carries every layer of its input forward". Agrees.
No unswept restatement for H4. It is clean.

## 4. The seven checks, per hunk

### H1
1. Tense/quantifier — speaks of the state handed over, correctly, and the next
   clause distinguishes "the earlier state the probe finds is a different
   artifact". The quantifier "a file whose final 64 bytes are not a valid
   trailer" ranges over the handed-over generation. Matches [R-CNT-06], which
   is quantified over the reader's own file. PASS.
2. Citations — §21.2 exists (file-scope). F8 = trailer magic, [R-CNT-06]. ✓
   F14 = "The u32 at trailer offset 60 does not equal the CRC-32C of trailer
   bytes [0,60)", [R-CNT-06] (R-CNT-20, R-ENC-09). ✓ F17 = committed_file_length
   vs transport-authoritative size, [R-CNT-06] (R-LIF-04, R-CNT-10). ✓
   [R-CNT-06] does state all three. ✓ All PASS.
3. Normative siting — the repair is in plain prose closing "`[R-LIF-06]`", not
   in a ">" block. PASS.
4. Same-passage contradiction — none found; the sentences either side ("no
   verdict turns on the probe", "For a verifier the probe is diagnosis") are
   reinforced, not collided with.
5. Exhaustive claim — "the magic, the trailer CRC and the length cross-check"
   is a closed triple. Falsifiable: a file whose last 64 bytes carry the
   trailer magic **byte-reversed** is not a valid trailer, and §21.1 records it
   against F1, not F8. → X-04.
6. What is left unconstrained — structure = the 11 trailer fields. magic
   F8/F1; version_major F18 + §6.3 gate; version_minor deliberately free
   ([R-CNT-07]); flags F19; generation F11; dir_offset F9; dir_length F10,
   F16; committed_file_length F13, F17; file_id F12; reserved F15; CRC F14.
   Every field is pinned. Nothing left open.
7. Analogy — none ("— the magic, …" is apposition, not warrant). N/A.

### H2
1. Tense/quantifier — "another dimension's grid count is 0" is present-tense
   over the **new** state, which is the right generation: the product that
   fixes the new entry_count is the new geometry's. "adds no entry" ranges
   over the layer's index entries. Matches §11.2's N = ∏Gᵢ and [R-CNT-17]'s
   "equals the addressed-tile count". PASS.
2. Citations — [R-CNT-17] ✓ (ties extent_length to entry_count *and*
   entry_count to the geometry-derived count, and already carries "and 0 when
   entry_count is 0"). §11.2 ✓. PASS.
3. Normative siting — the repair is inside a ">" Rationale, so it carries no
   force. This is acceptable here **only because** the carve-out is an
   arithmetic consequence of [R-GEO-03] and [R-CNT-17] rather than a new rule:
   nothing needed normative force. But it is what makes X-02 and X-03
   non-byte-level.
4. Same-passage contradiction — "the first growth of a zero-extent layer
   included", eleven words later in the same sentence. → X-03.
5. Exhaustive claim — "every grid count", "holds the product at 0". Both
   check out against §11.2 for interleaved (N) and planar (C·N) alike.
6. Left unconstrained — structure = the layer's index-side quantities:
   entry_count, extent_offset, extent_length, crc_of_crc_array. H2 pins
   entry_count and extent_length. The siblings are pinned elsewhere: L22 bars
   "a nonzero slot with entry_count = 0" (so extent_offset must be 0 too), L27
   bars a nonzero crc_of_crc_array at entry_count = 0. Nothing left open on
   the structure. What *is* left open is the sentence's own consequent — see
   X-05.
7. Analogy — none by keyword. The implicit warrant is §11.2's product. Verbs
   compared: repair "another dimension's **grid count is** 0, which **holds
   the product** at 0 and **adds no entry**"; §11.2 "The layer's
   spatial-tile count **is** N = ∏ Gᵢ" and "addressed-tile count — the number
   of its tile-index entries (§15) — **is** N for an interleaved layer and
   C · N for a planar layer". Same set (the layer's dimensions), and the C
   factor cannot rescue a zero product. PASS for both layouts, tested
   separately.

### H3
1. Tense/quantifier — "a stored tile's offset" ranges over the stored tiles of
   the live state, and the row's transparency clause fixes what "previous"
   skips. The rule it restates is [R-SLB-03], quoted above; the quantifiers
   match ("each stored tile's offset" ↔ "a stored tile's offset", with the
   register's negated-condition convention). PASS on quantifier, FAIL on the
   pronoun — the rule's "its" and the row's "the previous stored tile's" are
   not the same referent under one available reading of the rule. → X-01.
2. Citations — [R-SLB-03] ✓ exists at §16.2 and is the packing rule. (R-IDX-03)
   ✓ §15.3, and its prose names [R-SLB-03] reciprocally. §15.3 ✓ is where the
   *structural* classification lives. All resolve; the governing citation
   resolves to a rule that *almost* says the claimed thing — the exact failure
   mode check 2 warns about.
3. Normative siting — a register row is normative-adjacent but subordinate:
   §21.1 makes the rule govern on divergence. → X-01.
4. Same-passage contradiction — L40 (per-tile A) and L42 (first stored tile
   mod A_slab) do not collide; L20/[R-CNT-16] makes A and S mutually
   exclusive. §16.2's "The runs themselves are not mutually ordered or joined"
   does not collide, because L41 says "Inside a slab run". PASS.
5. Exhaustive claim — "(gap, overlap, or out-of-ordinal placement)" is the
   Instances cell's triple and matches it; 3 instances, unchanged by the
   repair, so §21.3's "49 conditions" and §21.8's "121 conditions over 277
   instances" are untouched. PASS.
6. Left unconstrained — structure = one slab run. Members: each stored tile's
   offset (L41 + L42), each stored tile's length (a payload size; nothing
   constrains it, correctly), the run's first offset mod A_slab (L42), A_slab
   itself (L29), S (L28, [R-CNT-23]), the run partition (R-SLB-02), the run's
   end relative to the next run's start (deliberately free — "The runs
   themselves are not mutually ordered or joined", [R-SLB-05]). Nothing is
   silently unpinned.
7. Analogy — none in the repaired words. N/A.

### H4
1. Tense/quantifier — "editing a user-metadata document appends a new extent
   and strands the old one" is a present-tense generic over commits; §20.3 (c)
   uses the same tense. PASS.
2. Citations — §20.3 ✓; shape (b) ✓ and §20.3 (c) states "as in (b)" in its
   own words. [R-CNT-25] (cited in §20.3's clause, relied on here) ✓ — §7.1
   forbids the inline placement, so the document is always in an extent.
   [R-CNT-21] ✓ (slack). §20.4 ✓ (drop). PASS.
3. Normative siting — the repair is plain prose in §23.1 under [R-PRV-01]; the
   thing repaired is a cross-reference, and cross-references are not rules, so
   siting is not at issue. PASS.
4. Same-passage contradiction — checked the whole of §23.1. "Those two cases
   are exhaustive because the bytes either travel out of the live state or
   stay in the structure that carried them; the list of operations above is
   not offered as closed." The repair does not widen or narrow either case; it
   only re-labels which §20.3 picture the metadata case matches. "no commit
   removes a layer at all" is corroborated by §20.4 and Appendix H. PASS.
5. Exhaustive claim — "Those two cases are exhaustive" is pre-existing and
   still holds; the repair introduces no new closed list. PASS.
6. Left unconstrained — structure = the operations that make data unreachable.
   Listed: supersede a payload, unstore a tile, shrink (drop or pad-ify), drop
   a record, supersede a record extent. Unlisted but stranding: a superseded
   tile-index region, and the old directory/pad/trailer of every commit.
   Neither carries sample data and §23.1 says "the list of operations above is
   not offered as closed", so this is covered by construction. Nothing to
   report.
7. Analogy — "a record's extent **goes the same way** whether a commit drops
   the record (§20.4) or supersedes it". Verbs side by side: §20.4 drop —
   "Retain byte-identical, or **drop** it — its extent **becoming slack**";
   §20.3 (c) supersede — "a new extent is appended and the old one **becomes
   slack**". Both range over one record's extent bytes and both land in
   [R-CNT-21] slack. Same set, same verb. PASS.

## 5. Findings

X-01 (hunks 1, 3) — L41's disambiguation is unreachable: [R-SLB-03] still says
"plus its length", and §21.1 makes the rule govern. Byte-level.
X-02 (hunk 2) — §17.2's Note asserts what H2's carve-out denies. Not
byte-level (both non-normative), but a live contradiction between two
statements of one fact.
X-03 (hunk 2) — "the first growth of a zero-extent layer included" contradicts
the carve-out inserted eleven words earlier.
X-04 (hunk 1) — the closed triple omits F1's trailer-magic instance, against
§21.1's specialization rule and §21.2's own preamble.
X-05 (hunks 2, 4) — the carve-out case's consequent is left unstated in a
sentence whose sibling repair, in the same commit, is precisely a
shape-placement correction.
