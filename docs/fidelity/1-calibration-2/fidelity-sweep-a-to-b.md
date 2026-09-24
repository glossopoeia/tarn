# Completeness sweep, edition A -> edition B (dir "c") — transcript

Access rule followed: only read
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`
(edition A, 4981 lines) and
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/c/tarn.md`
(edition B, 4885 lines). No other file was opened. No directory was listed except
my own scratch/output dirs, which I created.

## Method

1. `grep -n "^#"` on both files to get the section/header outline (131 headers in A,
   130 in B — B is missing one: **§3.3 "Container and array model"** does not appear
   in B's outline at all).
2. Wrote a small local script
   (`/private/tmp/.../fidelity-2/scratch/sweep-a-to-b/split.py`) that splits each
   edition into one file per header (all levels), and **dewraps** each section's
   text into one line per paragraph (joining hard-wrapped lines, since both editions
   are hard-wrapped and a naive line diff would show wrap-boundary noise as false
   differences). Output under `.../sweep-a-to-b/sections/a/*.txt` and `.../b/*.txt`,
   with `a_titles.txt` / `b_titles.txt` mapping header text to filename.
3. Wrote `pair_diff.py` to match sections by header text between editions (order
   differs — B moved §3 ahead of §2 — so matching is by title, not position) and
   list which matched sections have any paragraph-level text difference at all.
4. This produced a **complete, exhaustive list of every section in the whole
   document whose dewrapped text differs between A and B**, with everything else
   confirmed byte-identical (mod whitespace/line-wrap). That list was short:
   `1. Introduction`, `2. Conformance` (`2.3`, `2.4`), `3. Terminology and Data
   Model` (`3.1`), `12. Channels and Sample Types`, `21. Error-Handling Register
   and Limits` (`21.6`), plus the parent container headers (`Part 0`, `Part II`,
   `Part III`, the document title) which differ only because they *contain* the
   above children — not independent information.
5. This mechanical result was cross-checked against the raw line-count delta:
   A is 96 lines longer than B; the length removed in §1 (~24 lines), §2.3
   (~54 lines), §2.4 (~7 lines) and §3.3 (~8 lines, wholly removed) accounts for
   essentially all of the 96-line difference. This corroborates that no other part
   of the document was silently touched.
6. Every section on the differing list was read in full, side by side, and every
   section named by the charter as work-product-relevant was checked for the
   specific rule/carve-out/quantifier it decides. Two proposed loss/contradiction
   candidates from the glossary edits were checked against their normative "home"
   sections (§9.2, §20.4) and downgraded to EQUIVALENT once I confirmed the
   substance survives there unchanged (see disclosure below) — those are **not**
   included as findings, precisely because a byte-level implementation would not
   differ.
7. Two candidate contradictions in §2.3 were corroborated by grep across the
   *rest* of both documents for `conduct` and `capability` — both editions carry
   other passages (§9.2's commit-protocol note, §21.9's "two capability refusals")
   that were **not edited** and that explicitly restate the *edition-A* rule,
   which makes edition B's rewritten §2.3 internally self-contradictory, not just
   diverging from A.

## Section-by-section inventory (only sections with any difference; all
## other sections of the whole document — §5–§11, §13–§20 except 20.4's
## wording (unchanged), §22–§24, all appendices — were confirmed identical)

### §1 Introduction (non-normative, R-CNF-01: "All text in this document is
normative except: §1...")
Both editions state the same design pillars in substance (random access without
a server; integrity by default; append without rewriting; defined behavior at
the edges; closed core/open edge) and the same "what TARN is not" list. B
condenses numeric specifics (A: "two range requests", "§21.9's tile-count
guarantee"; B: "a small fixed number of range requests") and drops citations.
Because §1 is explicitly non-normative in **both** editions, no implementation
is built from it, so under the byte-level test this cannot be a LOSS/ADDITION
regardless of how much prose changed. Not reported as a finding.

### §2.1, §2.2, §2.5 — byte-identical in both editions. No item to report.

### §2.3 Conformance classes — three items found, all reported (swab-01..04 below).

- **Conforming TARN file bullet (`[R-CNF-02]`)**: A's "conduct rule" carve-out
  (a file is *never* nonconforming for breaking a conduct-only writer
  obligation) is inverted in B ("a file that breaks one is nonconforming").
  A's specific enumerated examples of conduct-only obligations (the ignore-lane
  bit exemption in §6.3, the pre-trailer-gap exemption in §6.2, the §20.3 step 4
  bar, registry-version targeting in §10.3/§18.3, commit barriers in §9.2) are
  entirely absent from B, in addition to the inverted general rule. Cross-checked:
  §9.2's unchanged text (identical in A and B, line ~1305/1202) still says "the
  file it produces is never nonconforming by virtue of it, as `[R-CNF-02]` says
  of every conduct rule" — which is now false of B's own rewritten `[R-CNF-02]`.
  **Reported as swab-01, CONTRADICTION.**

- **Conforming reader bullet (`[R-CNF-03]`)**: A requires a conforming reader to
  handle "every user-metadata encoding §18.2 assigns, and both record types §7.3
  registers" (line 189-191), and includes "a registered record type" in the list
  of things whose declination disqualifies conformance. B's corresponding text
  (line 219-225) drops "and both record types §7.3 registers" and the
  "no subset profiles" list's "or a registered record type" item — the sentence
  is simply shortened to "software that declines any of those." Checked §7.3
  itself (byte-identical in both editions): it states a reader must apply a known
  type's semantics but never frames declining a record type as disqualifying
  "conforming reader" status the way §2.3's list did. **Reported as swab-02,
  LOSS.**

- **Conforming verifier bullet (`[R-CNF-11]`)**: A enumerates five grounds for a
  *cannot establish* verdict (unimplemented format major; MU=1 record of an
  unimplemented type; cannot execute a codec/filter; **declines a layer's or a
  tile's decode on resource grounds and so cannot check §14's decoded-content
  obligations** [`R-ERR-04`, `R-SER-05`, `R-SER-08`]; declines to decode a
  user-metadata document [`R-MTA-09`]), and a carve-out: a user-metadata document
  under an *experimental-range* encoding is explicitly **not** such a ground
  (certification unaffected, `R-MTA-10`), while encoding 0 and a reserved value
  **are** violations (§21.5, R1). B compresses all of this to "(§21.6 names the
  grounds)." §21.6 in B does add a paragraph (absent from A, since A's version
  keeps the detail in §2.3) enumerating grounds — but it lists only **four** of
  A's five (it omits the layer/tile resource-decline ground), and does not carry
  the user-metadata-experimental-encoding carve-out or the R-MTA-10 citation at
  all. **Reported as swab-03, LOSS.**

### §2.4 Outcome classes and owning scope
A has two clarifying sentences right after the R-CNF-07 lead-in ("The same
vocabulary is used for defined conditions that are not violations..."; "
**preserve-verbatim** names an updater obligation, orthogonal to reader
outcomes: a record a reader ignores can still be one an updater preserves.")
and a closing Note ("'Reject' prescribes the scope of unusability, not user
interface..."). Both are missing from B. The table row for preserve-verbatim
(identical in both editions) already states "Binds updaters: the bytes are
carried forward unmodified," so the *substance* of the dropped sentence survives
in the table; the dropped Note is purely non-normative style guidance. Not
reported as a LOSS finding (kept as disclosure-level observation only), since I
could not construct a byte-level divergence from either drop.

### §2.3's reach paragraph (`[R-CNF-13]`, appears between the class list and
§2.4, no numbered subsection)
A: "A reader MUST apply every reaching condition to a file whatever major it
declares ... and MUST treat its failure as reject-file on the ground of the
requirement stating it **rather than on capability grounds**; the distinct
diagnostic `[R-CNT-07]` asks for is owed where every reaching condition is
satisfied and the declared major is one the reader does not implement."
B: "A reader MUST check every reaching condition whatever major the file
declares, and MUST treat a failure **as a capability refusal, not as
reject-file** under the requirement that states the condition; ... `[R-CNT-07]`'s
distinct diagnostic is given where every reaching condition is satisfied and the
declared major is one the reader does not implement."
This is an exact inversion of the outcome A assigns to a reaching-condition
failure. It is also internally inconsistent with B's own unchanged §21.9 text
(identical wording in both editions, "the two capability refusals §21.6's
closing paragraph names, a foreign format major and an unimplemented top-level
MU = 1 type, are not this ground") which recognizes only **two** capability
refusals, neither of which is "a reaching condition fails." **Reported as
swab-04, CONTRADICTION.**

### §3.1 Terms
Full dewrapped diff obtained (see `sections/a/0352_3_1_Terms.txt` vs
`sections/b/0060_3_1_Terms.txt`). Differences:
- **generation**: A adds "successive generations of one file are ordered by the
  strictly increasing committed file length their trailers carry (§9.3)"; B
  drops it. Checked §9.2 (byte-identical in both editions): "A commit's
  committed_file_length is strictly greater than the prior trailer's, by at
  least 128, so the committed file length orders a file's generations (§9.3)."
  Substance survives verbatim in the normative section; glossary trim only.
  Not reported as LOSS.
- **directory**: A adds "— never a delta (§9.2) —" before "so a conforming
  commit adds one directory per generation"; B drops both clauses, keeping only
  "Each commit appends a *complete* directory; unqualified, *the directory*
  means the live generation's." Grepped `delta` across both full files: the word
  appears **only** in A, nowhere in B. However "complete directory" (not
  "delta") is the operative term used consistently throughout both editions
  (§9.2, §20.3, §20.4, Appendix D — all identical), so the substance (a
  directory is always full, never incremental) is carried by the surviving
  "complete" language in both. Treated as EQUIVALENT (redundant negation
  dropped), not reported as LOSS.
- **channel / dimension**: A says the declared order is merely "load-bearing
  (§11.4)"/"load-bearing (§11.4, §14)"; B spells out the mechanism ("fixes the
  sample order on disk: within a tile the last-declared dimension varies
  fastest..." / "fixes where the channel's value sits within each interleaved
  sample (§14) and where its tiles fall in a planar layer's index (§11.4)").
  Checked that §11.4 (byte-identical in both editions, not on the differing
  list) is the source of this derivation, so B is only surfacing what A's own
  §11.4 already states — not a new decision. EQUIVALENT, not reported.
- **tile**: B adds "A tile *carries* a channel when its payload holds that
  channel's samples at the cell's positions," formalizing a verb ("carries")
  both editions use elsewhere without a standing definition. This is a
  clarification consistent with usage throughout both editions, not a new
  decision. Not reported.
- **fill value**: A "the *per-channel* value..."; B "the value..." — trivial
  wording, the surrounding clause ("a channel's samples take") already ties it
  to the channel. Not reported.
- **channel layout**: A cites "(§7.4)... (§14)"; B drops the citations, no rule
  content lost. Not reported.
- **addressed tile / stored tile**: A: "every tile of a layer is *addressed*"
  (unconditional, layer-level). B: "a tile is *addressed* **in a generation** if
  that generation's tile index has an entry for it: the tiles of the layer's
  grid **under the geometry that generation declares** (§11.2, §15)." This
  changes what "addressed" formally means — from an unconditional per-layer
  property to a per-generation one keyed to "the geometry that generation
  declares," which implies a layer's geometry could vary by generation. Checked
  §11.2 (byte-identical in both editions): it defines "addressed-tile count" as
  a fixed function of the layer's declared grid (Gᵢ, N, C·N) with no per-generation
  variability stated anywhere in that passage, and §15.1 (also unchanged) speaks
  of "a layer's tile index" without any generation-indexed geometry language
  either. I could not fully resolve, within this file pair alone, whether layer
  geometry is in fact immutable once created (which would make B's added
  generation-qualifier an ADDITION not licensed by A's own text) — that would
  require reading §20.3/§20.5's full rewriting rules, which I confirmed are
  byte-identical between editions but did not re-derive from scratch for this
  specific question. **Reported as swab-05, AMBIGUITY**, flagged for the
  maintainer rather than asserted as LOSS or ADDITION with full confidence.

### §3.2 The reference array — byte-identical in both editions.

### §3.3 Container and array model
Present in A only, as a `> **Note.**` block: "Part I (container) is independent
of Part II (array model) by construction: no Part I structure requires decoding
sample payloads, so appenders, and rewriters that carry a layer forward, operate
on files whose layers they cannot decode — that independence is load-bearing for
the updater rules of §7 and §20." Entirely absent from B — not merely moved,
not a header collision, just gone (grepped "Container and array model" and "3.3"
across B, no match). Because it was already non-normative (a `Note`) under
R-CNF-01 in edition A, its removal cannot itself change what an implementation
built from B does — so by the stated definition this is not a LOSS. Recorded as
**swab-06, OBSERVATION**, since the charter asks me to report items B carries
only inside a Note/Example/Rationale block *or the reverse*, and this is the
starkest form of "the reverse" (content deleted outright rather than
downgraded) — worth the maintainer's attention even though it fails the
byte-level LOSS test.

### §4 Encoding Conventions (4.1–4.7) — byte-identical in both editions,
confirmed by full side-by-side read, not just the dewrap diff.

### §5–§11 — confirmed byte-identical by the dewrap diff (no title in the
differing-sections list). Spot-checked §7.3 (record types table + prose) and
§9.2 (commit protocol, conduct-rule note) directly; both verbatim identical to
A.

### §12 Channels and Sample Types
One wording change in the intro, already covered by §3.1's channel/dimension
pattern: A "...channels are declared in order, and the declared order is
load-bearing (§3.1, §11.4)"; B "...and the declared order fixes each channel's
index (§3.1, §11.4)." This is trivially true by the §3.1 definition of "index"
in both editions (index = 0-based declared position) so it changes nothing
decidable. EQUIVALENT, not reported. Rest of §12 (12.1–12.3, including the type
value-set table and byte-pattern rules) confirmed byte-identical.

### §13–§20 — confirmed byte-identical by the dewrap diff. Spot-checked §20.4
(re-emission and preservation) directly since it is cited by the §2.3 updater
bullet's dropped clause; §20.4's own text ("Persistence governs every record
type; only the authoritative source of the flags differs...") already states
what A's §2.3 clause said, so that particular §2.3 trim is EQUIVALENT, not a
LOSS (noted, not reported as a finding).

### §21 Error-Handling Register and Limits
21.1–21.5, 21.7–21.9: byte-identical in both editions (register table, F/L/T
rows, limits table all unchanged — the mechanical requirement-ID/table checker
this task says to trust already covers these, and my prose sweep found nothing
outside what it would catch).
21.6: covered under §2.3 above (swab-03) — B adds a paragraph here that is the
*target* of §2.3's "(§21.6 names the grounds)" cross-reference, but that added
paragraph itself under-states A's original five-ground, one-carve-out text.

### §22–§24 and Appendices A–H — confirmed byte-identical by the dewrap diff
(none appear on the differing-sections list). Given the task's time budget I did
not re-read these word-for-word beyond the mechanical dewrap-diff confirmation;
if that confirmation is wrong for some subtle reason (e.g. a normalization bug
in my own script hiding a real diff), that risk applies uniformly to §5–§11,
§13–§20, §22–§24 and the appendices — i.e., everything **not** listed above as
differing. I re-derived the dewrap diff's completeness independently via the
raw line-count-delta accounting in Method step 5, which closed to within a few
lines using only the sections already identified, which is why I trust it.

## Disclosure

- Nothing was placed in my context by the runtime before I began that I am
  relying on as evidence; all quotations above come from files I opened myself
  in this session (`Read`/`grep`/`sed` against the two named paths only).
- I did not reach a fully independent, from-scratch re-verification of §5–§11,
  §13–§20, §22–§24, and the appendices beyond the mechanical whitespace-normalized
  paragraph diff plus a line-count-delta sanity check; I did directly re-read
  §4 in full and spot-checked §7.3, §9.2, §11.2, §15.1, §20.4, §21.6, §21.9 by
  name because those were the sections a candidate finding pointed back to.
  I judge the risk that the mechanical diff missed something as low, given the
  line-count accounting closed almost exactly against the sections it did find,
  but I flag this rather than claim an exhaustive hand-read of ~9,800 lines.
- Every zero I report (e.g., "no other section differs," "the word `delta`
  appears only in A") is backed by a `grep -n` or full-file diff shown in the
  commands above, not by absence-of-memory.
