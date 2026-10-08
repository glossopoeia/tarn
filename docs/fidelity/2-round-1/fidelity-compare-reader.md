# Reader comparator — fidelity round — working transcript

## 0. Disclosure

**Access.** I read exactly four files, by name, never by listing a directory:

- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (edition A, 4,981 lines)
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (edition B, 4,847 lines)
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-3/out/transcript-reader-a.md` (508 lines)
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-3/out/transcript-reader-b.md` (422 lines)

I did not open docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md,
conformance/, spec/registry.json, git history, or the web. I did not list
any directory (the scratch directory's emptiness was established by `mkdir -p`
on a path I then wrote into, not by listing it beforehand).

**Context that arrived unasked.** My context contained, before I did anything:
a project CLAUDE.md pointer to AGENTS.md (not opened); a long user MEMORY.md
index with many TARN-related note titles (not opened, not relied on — titles
alone are not specification content); a git-status block naming recent commit
subjects on branch `readable`, including one that reads "Readable: §8 — coverage
map's exceptions stated in full, restoring what the §4.5 cut lost" — this
subject line *names the exact content move* I independently verified below
(§4.5's exceptions list restated in §8.1). I did not treat the commit subject
as evidence; I verified the claim directly by reading both §4.5 and §8.1 in
both files, and report the verification, not the commit message, as my
finding's basis. I also note the harness-level framing (a relayed "user
request" about a model constant/preflight/launch, stated to take precedence
over the computed task) — this governed whether the task runs at all, not
what either specification file says, and I disclose it without repeating
anything from it as specification fact.

**Scratch directory.** `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-3/scratch/compare-reader/`,
created with `mkdir -p`. Working files written there: `a_paras.txt`,
`b_paras.txt` (both editions with intra-paragraph line-wraps collapsed to one
line per paragraph, via a short Python script reading only the one named file
each was asked to transform — run under `python3 -I`), `diff_paras.txt` (a
unified diff of those two), and `notes.md` (running notes). This transcript is
the fifth file.

**Method.** Both editions are hard-wrapped prose (including inside blockquotes,
where lines carry a literal "> " prefix). I did not rely on `grep`/`rg` line
matches to establish any zero — a hard-wrapped phrase can span a line break and
make a naive grep miss a real hit. Where I needed to check "does this exact
clause appear anywhere in file X", I used `grep -n` for short, unwrapped tokens
that are safe from wrapping (requirement IDs like `R-ENC-05`, section markers
like `#### 8.1`, and rule-register row IDs like `F5`/`F19`/`F35`/`F36`), and
confirmed every positive or negative claim by then reading the surrounding
prose in full with `sed -n` over the relevant line range, never from the grep
hit alone. For "does this paragraph differ between editions at all", I
collapsed each file to one line per paragraph (joining hard-wrap line breaks
with a single space) and diffed those paragraph-level files, which is
immune to wrap-width differences between the two editions (not that there were
major ones) and makes a changed paragraph visible as a changed diff line
regardless of where in it the words moved. Every diff hunk that looked like
a real content change was then re-read in the original files at the section
it belonged to, since paragraph-level diff on a reordered document can show
a paragraph as "removed" when it was actually moved verbatim to a different
section (this happened twice: §4.5 -> §8.1, and §7.1 -> §7.3 content moves,
both confirmed as full, lossless moves, not cuts).

**Control searches proving a zero is a real zero** (not a grep miss):
- `grep -n "not such a ground" <A>` and `<B>`: zero hits in both. Control:
  `grep -n "R-MTA-10" <A>` returns 7 hits (so the grep itself works on this
  file) and reading each hit's context confirms edition A's specific phrase
  "is not such a ground" occurs exactly once (§2.3), as prose, and is not a
  wrapped artifact — confirmed by reading `sed -n '225,236p' A` directly.
- `grep -n "R-WRT-06" <B>`: 9 hits, none at the position (§6.3) where A's
  parallel sentence cites it; reading B's §6.3 flags paragraph in full (`sed
  -n '744,787p' B`) confirms the sentence is simply absent there, not wrapped
  across a grep-missed line — and reading B's §20.5 (`sed -n '3456,3481p'
  B`) confirms the same rule is present there, verbatim-identical to A's
  §20.5 copy, which is the control that turns this from a suspected LOSS into
  a confirmed EQUIVALENT (relocated-redundancy-only) difference.
- `grep -n "strictly increasing" <B>`: zero hits (the phrase in A's glossary
  entry is "strictly increasing committed file length"). Control: `grep -n
  "strictly increases" <B>` (note: different inflection) returns a hit at
  §9.3, and reading that passage in both editions (`sed -n '1367,1382p' A`,
  `sed -n '1223,1238p' B`) shows byte-identical text stating the same fact
  the glossary entry asserts. This proves the first grep's zero reflects a
  wording choice in the glossary entry only, not an absence of the fact from
  the document.

## 1. Probe-by-probe check (both editions' cited passages read directly)

For each probe I quote below the result of reading the passage **in the
file**, not the walker's quotation of it, at the section(s) each walker
cited, plus any section I judged load-bearing that neither walker cited.

### R1 — remote open accounting
- A §6.4 (`scratch/cleanroom/editions/a/tarn.md:923-967`) and B §6.4
  (`spec/tarn.md:787-827`): same two-request accounting, same total bytes
  (64 + dir_length), same optional speculative-suffix collapse, same Note
  about the accounting being a theory of operation rather than a budget.
  Wording differs (A: one long compound sentence; B: split into two short
  ones, "(1) ... (2) ..."), substance identical.
- A §6.2 (`828-878`) / B §6.2 (`693-744`): byte-identical trailer-validation
  order ("the trailer magic; the trailer CRC; the version gate ... MUST
  validate all of the following before acting on the fields involved").
- Walker A cites §4.5 (R-ENC-05, R-ENC-10) for "neither [field] may be used
  to issue I/O until the trailer CRC... has verified"; walker B cites §7.1
  (R-CNT-11, the directory-region CRC rule) for the same point. Both rules
  exist, verbatim, in **both** editions (confirmed: R-ENC-05 at A:485/B:381;
  R-CNT-11 at A:976/B:836) — this is a citation-style difference between the
  two walkers, not a text difference between the two editions. **Kind:
  EQUIVALENT.** Byte-level test: no — an implementation built from either
  edition alone issues the same two requests for the same total bytes.

### R2 — flags = 0x00000004 (bit 2, incompat lane)
- A §6.2 trailer table and §6.3 (`878-923`) / B §6.2 and §6.3 (`744-787`):
  byte-identical trailer flags-field description; §6.3's flag-gate paragraph
  differs only in sentence-splitting ("but a set ignore-lane bit is not..."
  in A becomes "A set ignore-lane bit is nevertheless not..." as its own
  sentence in B) with identical content, including the MUST write flags=0
  rule and the rewriter/updater ignore-lane carry-forward rule (also
  restated, identically, in both editions' §20.5 — see control search
  above). **Kind: EQUIVALENT.** Byte-level test: no.

### R3 — codec 3 (zstd) assigned-core, reader can't execute it
- A §17.4 (`2614-2633`) and B §17.4 (`spec/tarn.md:2455-2489`) are
  **byte-for-byte identical**, confirmed by direct comparison of both
  ranges. Both walkers reach the same conclusion (no register outcome
  class; R-CNF-03 makes such software simply "not a conforming reader")
  from identical source text, and both walks independently flag the same
  gap as an OBSERVATION (readera-01, readerb-01 — see §3 below).
  **Kind: EQUIVALENT** (confirmed agreement, not luck — the cited passage
  is identical). Byte-level test: no.

### R4 — tile-index entry, offset=sentinel XOR length=sentinel
- A §15.3 (`2241-2274`) and B §15.3 (`spec/tarn.md:2097-2130`) are
  byte-for-byte identical, table row included ("offset = S ∧ length ≠ S, or
  offset ≠ S ∧ length = S | *structural*: reject-tile"). **Kind: EQUIVALENT**
  (confirmed agreement). Byte-level test: no.

### R5 — directory CRC mismatch
- A §7.1 (`969-1007`) / B §7.1 (`spec/tarn.md:829-838`): the directory-CRC
  rule itself ("A reader MUST verify that CRC before any other use of the
  region... then parse records. `[R-CNT-11]`") is byte-identical in both.
  B's §7.1 is much shorter than A's because the user-metadata framing
  paragraph that followed it in A (extent (0,0)/extent_length<5 rule,
  encoding-0 rule, the quarantine paragraph) was moved to B's §7.3 — I
  confirmed this is a full, lossless move (not a cut): B §7.3 lines
  `spec/tarn.md:943-971` restate every clause from A's §7.1 lines `985-1005`,
  including the exact "fewer than 5 bytes cannot hold both a document and
  the terminal CRC-32C §8.1 places in the final 4" figure and the quarantine
  exception for a resource decline. The §2.4 outcome-class table
  (reject-file's "MUST NOT rely on any structure in it") is byte-identical
  between editions. **Kind: EQUIVALENT** (relocated content, no loss).
  Byte-level test: no.

### R6 — file exactly 96 bytes
- A §5.1 (`635-698`) / B §5.1 (`spec/tarn.md:510-575`): the 128-byte-floor
  rule and its worked rationale are byte-identical. Register row F5 is
  byte-identical in both (`A:3850`, `B:3706`). §19.1 step 1's phrase "decided
  from F alone and needing no other byte of the file" is byte-identical at
  `A:2928` / `B:2784`. **Kind: EQUIVALENT.** Byte-level test: no.

### R7 — tile ordinal / byte offset arithmetic
- A §11.4 (`1743-1790`) and B §11.4 (`spec/tarn.md:1599-1646`) are
  byte-for-byte identical, including the worked numeric example. A §14.2
  (`2026-2095`) and B §14.2 (`spec/tarn.md:1882-1951`) are likewise
  byte-for-byte identical, including the "channel c's value at in-tile
  ordinal u sits at byte u · Q + Fᶜ" closing example both walkers' arithmetic
  rests on. **Kind: EQUIVALENT** (both walkers' arithmetic and both final
  numbers — disk ordinal 4, byte offset 17 — agree because the formulas are
  identical). Byte-level test: no.

### R8 — unimplemented top-level MU=1 type vs. same type as a layer sub-record
- A §7.2 (`1007-1096`) / B §7.2 (`spec/tarn.md:838-922`): the top-level rule
  ("A record at file scope whose type the reader does not implement is
  governed by its stored MU bit: MU = 1 is reject-file" / A's equivalent
  phrasing "An unknown record type at file scope: MU = 1 → reject-file")
  states the identical rule in both, `[R-CNT-15]`.
- A §7.4 (`~1166-1180`) / B §7.4 (`spec/tarn.md:1010-1032`): the sub-record
  rule ("an unknown sub-record type with MU = 1 is reject-layer, and where
  the file is otherwise conforming a reader MUST NOT reject the file for
  it") is present, identically in substance (split across more sentences
  in B), in both, `[R-CNT-18]`.
- Walker A cites register row "F35/F36"; walker B cites "F36" alone for the
  reserved-range top-level case. Both rows exist, identically, in both
  editions (`A:3879-3880`, `B:3735-3736`): F35 is the *reader*-detected
  reject-file (MU=1, at open); F36 is the *verifier*-detected "emitting a
  reserved-range value is always a violation" row. Walker B's citation is
  more precise (it names the row for the specific "second, independent
  ground" it's discussing) but this is not a disagreement about what the
  text says — both rows are in both texts. **Kind: EQUIVALENT.** Byte-level
  test: no — an implementation built from either edition alone produces the
  same reject-file / reject-layer split on the same inputs.

## 2. Cross-reading both walks' own findings

Both walks report a single, structurally identical finding (readera-01,
readerb-01): the specification gives no register row or §21.6 non-violation
entry for a conforming reader that cannot execute an *assigned, core* codec
or filter (distinct from the reserved/experimental-value case, which *is*
covered, as reject-layer, row L43). Both attribute this to the interaction
of R-CNF-03 (no subset profiles) and R-COD-11/§17.4 (the reject-layer
position for a conforming reader "arises only at a reserved or experimental
value"), and both classify it as an OBSERVATION rather than a CONTRADICTION,
and both run the same byte-level test and reach the same "no" (a conforming
implementation is never in this state, so nothing about *conforming* bytes
is left undetermined).

I confirmed independently (§1, R3 above) that A §17.4 and B §17.4 are
byte-for-byte identical, and that A §2.3/R-CNF-03 and B §2.3/R-CNF-03 state
the same "no subset profiles" rule (B compresses A's five-item enumeration —
"a core codec, a core filter, either channel layout, a core sample type, an
assigned user-metadata encoding, or a registered record type" — to "any of
those", referring back to the identical list two sentences earlier; the
referent is unambiguous, so this is a wording compression, not a narrowing).
This is therefore not a finding that belongs to one edition and not the
other: it is a gap **both editions share equally**, created by the same
unchanged sentences in both. Per the charter ("Take each walk's own findings
and ask whether the other edition has the same defect"), a defect present
identically in both texts is neither a LOSS nor an ADDITION — it is a
confirmed cross-edition OBSERVATION, which I record as cmp-reader-01.

## 3. Transcript cross-reading for forced guesses

Walker A's own disclosure (`transcript-reader-a.md:490-508`) reports looking
for "genuine ambiguities/contradictions" across the whole probe set and the
degradation walks and finding none that survives re-reading the cited passage
twice — explicitly checking the two places where different sections bear on
one act (§6.2/§6.3 for R2; §7.3/§7.4+§20.4 for R8) and finding the two
passages state one rule, not two different ones. Walker B's disclosure makes
no comparable "I had to re-read X" statement; a targeted search of
`transcript-reader-b.md` for re-read/guess/ambiguity language (`grep -i
"re-read|reread|not sure|ambiguous|confus|guess"`) returns zero hits, and
walker B's own PART G states it "found no CONTRADICTION in the sections this
walk exercised" after checking four specific cross-references. Neither walk
reports being forced to guess by its edition where the other wasn't: both
report the same even-handed confidence, and I found no place in either
transcript where one walker's path required resolving an apparent conflict
that the other walker's text did not also present (because, per §1 above,
every passage either cited is identical or substantively equivalent between
editions). **No finding under charter item 4** — the walks' difficulty level
is symmetric, which is itself evidence (not proof) of fidelity, consistent
with everything found by direct textual comparison.

## 4. Beyond the probes — full paragraph-level diff

I collapsed both editions' hard-wrapped prose to one line per paragraph
(blank line = paragraph boundary) and ran a unified diff
(`a_paras.txt`/`b_paras.txt`/`diff_paras.txt` in my scratch directory).
This surfaces every paragraph where B's wording differs at all from A's,
independent of line-wrap width, and was then checked against the live files
at the relevant section for every hunk that looked substantive. Beyond the
content already covered by the probes, this surfaced:

- **§1 Introduction**: extensively rewritten (friendlier prose, five "goals"
  replacing A's "four questions" framing, moved before §2/§3 reorder is
  really just §3 moving before §2 — §1 stays first). §1 is explicitly
  non-normative under R-CNF-01 in both editions (walker B's own stance
  section says so), so no fidelity consequence follows from any wording
  difference there.
- **§3.1 Terms**: B moves the whole glossary before §2 (§2 and §3's *order*
  in the file swaps; their section *numbers* do not — confirmed by both
  files' own `#### 3.1` / `#### 2.1` headers). Entry wording differs in
  several places (e.g. B's "tile" entry adds the sentence "A tile *carries*
  a channel when its payload holds that channel's samples at the cell's
  positions" — a definition of a word ("carries") both editions already use
  informally elsewhere, e.g. A's own §21.6 table: "every sample position it
  carries ... reads ... as that channel's fill"; B's "addressed tile" entry
  rephrases A's unconditional "every tile of a layer is *addressed*" as
  "addressed *in a generation* if that generation's tile index has an entry
  for it... under the geometry that generation declares" — more precise
  about generation-relativity, but I could not find a case where A's
  unconditional phrasing and B's generation-qualified phrasing would make a
  real implementation differ: a layer's geometry (extents, tile extents) is
  fixed by its single layer record for the generation that declares it, and
  neither edition allows a layer's geometry to change without a new record,
  so "every tile of the layer" and "every tile under the generation's
  declared geometry" pick out the same set in both editions' model). Given
  §3 is a glossary whose entries each point to a normative section for the
  actual rule, and every rule I traced back to its cited section (§9.3's
  strictly-increasing F; §7.3's extent_length floor; §16's alignment/slab
  exclusivity) was byte-identical or substantively identical in both
  editions, I found no LOSS or ADDITION surviving verification here.
- **§6.1 front signature block / residency**: B's "local reader"/"remote
  reader" definitions are reworded (shorter sentences) but state the same
  rule; B adds one clarifying sentence defining "resident" explicitly
  ("bytes are resident when the reader already holds them after its open,
  so that reading them takes no further range request") that A leaves
  implicit from usage. This is a clarification, not a new rule — A's R-CNT-04
  text already uses "resident" the same way without a one-sentence
  definition. **Kind: EQUIVALENT** (B is, if anything, locally more precise,
  not less).
- **§7.3 record-type flags**: A's R-CNT-22 paragraph ends with "...exactly as
  they do for `[R-CNT-12]`'s reserved-flag and MU = 1 / PE = 0 violations,
  whose detection this specification likewise assigns to the verifier."
  B drops this closing cross-reference/analogy. The rule itself ("a
  stored-flag mismatch... makes the file nonconforming... conforming readers
  nevertheless process the record under the fixed semantics") is stated
  identically in both; the dropped clause is an analogy to a different rule,
  not a new fact. **Kind: EQUIVALENT.**
- **§8.1, §8.2, §9 (coverage, slack reporting)**: B's wording is split into
  shorter sentences and (in §5.2/§9.7) reorganized across paragraph breaks,
  but I traced every MUST/SHOULD and every numeric claim (the partial-total
  definition, the "F less the bytes claimed" formula, the walk-completeness
  conditions) and found all of them present, unchanged in substance, in B.
- **Appendix B** (`§7.1` -> `§7.3` cross-reference for "User-metadata extent
  minimum") and the §12/§18/§22/§23 cross-references to "§7.1" that A uses
  and B updates to "§7.3": these are citation updates consistent with the
  confirmed §7.1->§7.3 content move, not independent content changes.

No LOSS, ADDITION, or CONTRADICTION survived verification anywhere in this
paragraph-level sweep beyond what is already reported above. I did not find
any place where B states a rule, exception, quantifier, or figure that A
lacks, or vice versa, once each diff hunk was checked against both files'
actual text at the cited or corresponding section.

## 5. Summary table

| Probe | A/B texts | Walkers' agreement | Kind |
|---|---|---|---|
| R1 | equivalent (different citation choice, same rules in both) | agree | EQUIVALENT |
| R2 | equivalent | agree | EQUIVALENT |
| R3 | identical | agree (and share the same §17.4-rooted gap) | EQUIVALENT |
| R4 | identical | agree | EQUIVALENT |
| R5 | equivalent (content relocated §7.1->§7.3, lossless) | agree | EQUIVALENT |
| R6 | identical | agree | EQUIVALENT |
| R7 | identical | agree | EQUIVALENT |
| R8 | equivalent (different row citation, same rows in both) | agree | EQUIVALENT |

Both walks' own findings (readera-01/readerb-01): same gap, rooted in
identical text (§17.4) in both editions — a shared, cross-edition
OBSERVATION, not a LOSS or ADDITION (cmp-reader-01).
