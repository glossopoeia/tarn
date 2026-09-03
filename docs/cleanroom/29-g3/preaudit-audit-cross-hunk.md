# Cross-hunk consistency audit — r29 pre-audit

## Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (whole
file, in sections, via `sed -n`), and all nine hunk files
`hunk-01.diff` … `hunk-09.diff` in
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-preaudit/case/`.
Did NOT read `full.diff`; did NOT read docs/, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, README.md, conformance/, spec/registry.json; ran no git command; no
web. Did not `ls` the case directory contents beyond the single `ls -la` used to
confirm the nine hunk files exist (the listing incidentally showed `full.diff`
exists; its contents were not read).

Unrequested context appeared before I began: a CLAUDE.md pointer, an index of the
maintainer's auto-memory files (titles only, listing topics such as a naming
constraint, a working cadence, workflow-verifier failure shapes, and a claim about
§21 and a vector corpus), and a session date. None of it is specification
evidence; I did not open any of the named memory files and drew no conclusion from
the index. Disclosed here as required.

Files written: only this transcript, plus the scratch directory
`.../scratch/cross-hunk/` (created; no working files ultimately needed — all
computation was done inline in `python3 - <<EOF` heredocs through Bash, which
wrote nothing to disk).

## Grouping (by rule touched, not by section)

**Group A — the two bars of §20.3 step 4.** Hunks 2, 3, 4, 5 (in §20.3 step 4
itself), 1 (§11.1 Rationale, a distant restatement), 6 (§20.3's "three shapes"
Example, a distant restatement), 9 (§21.7 Rationale, a distant restatement of
their witness status).
  - hunk 2 names the existing declaration-change prohibition the **§14 bar** and
    adds *sample type* to its enumerated list.
  - hunk 3 elaborates sample type, and inserts a **second, new bar**: a planar
    layer's channel declarations MUST NOT move a stored tile's disk ordinal.
  - hunk 4 narrows "the bar above is the whole of the test" to "the §14 bar is
    the whole of the test **of what a shrink alters**" and lists other
    obligations that bind a shrink.
  - hunk 5 re-points two anaphors to "the §14 bar" and states that the second bar
    does not reach a shrink.
  - hunks 1 and 6 sweep the two distant restatements of the empty-layer
    permission and of what the bars reach.
  - hunk 9 rewrites §21.7 and restates both bars' witness status.

**Group B — the detectability test.** Hunks 7, 8 (§21.1, describing §21.7 from a
distance), 9 (§21.7, which is where the test now lives). §21.7 was converted from
an inventory of omitted obligations into a stated test, with the inventory
demoted to a `> **Rationale.**` block.

Hunk 9 is in both groups.

## Rule each repair adopts (my words)

- h1: §11.1's Rationale now asserts §20.3 holds exactly two bars, that only the
  §14 bar reaches a shrink or a growth, that the empty-layer permission is
  quantified over the superseded generation, and that re-typing is the §14 bar's
  subject.
- h2: the §14 bar's enumerated list gains "the sample type each value in the
  image is read under"; the prohibition acquires a name.
- h3: re-typing a channel is barred wherever the superseded generation stored a
  tile carrying that channel, decided from declarations rather than stored
  values; and, separately, a planar layer's channel declarations may not move a
  stored tile's disk ordinal.
- h4: the §14 bar is necessary-and-sufficient only for the question *what does a
  shrink alter*; the step's other obligations bind a shrink as they bind any
  commit.
- h5: the second bar does not reach a shrink.
- h6: the Example's empty-layer sentence takes the superseded generation's tense.
- h7: §21.1 now states, inline, what it says §21.7's test is.
- h8: §21.7 is a test, not an account.
- h9: §21.7 states a two-sided definition of unwitnessed/detectable, keyed to the
  checks the specification obliges; the old inventory becomes an illustration.

## Searches run (whitespace-normalised, so hard wraps cannot hide a hit)

All via `python3` with `flat = re.sub(r'\s+',' ',text)` or
`re.sub(r'[ \t]*\n[ \t]*',' ',text)`.

| fragment | hits |
|---|---|
| `meaning exactly what they meant` | 1 |
| `live state` | 20 |
| `the bar above` | 0 (fully swept by h4/h5) |
| `R-COD-07` | 7 |
| `R-ERR-01` | 1 |
| `R-CNF-07` | 3 |
| `R-CNF-13` | 4 |
| `R-CNT-06` | 24 |
| `the §14 bar` | 8 |
| `§14 bar` | 10 |
| `both bars` | 1 |
| `two bars` | 1 |
| `disk ordinal` | 16 |
| `re-declared freely` | 3 |
| `sample type` | 10 |

Line-scoped scans (`kw in line`, with the enclosing heading resolved by bisect):
`detectab` (14 hits), `unwitnessed` (7), `witness` (22), `no check detects` (2),
`re-declar` (6), `declaration` (46), `stores no tile` (2), `stored no tile` (4),
`empt` (24), `R-GEO-06` (6).

Sections opened in full: §2.3, §2.4 (via R-CNF-07/R-CNF-13 windows), §4.2, §7.4
(closing Notes), §11.1, §11.2, §11.4, §12.1, §14 preamble, §14.1, §14.2, §14.5,
§16.2, §17.2, §17.3, §18.2, §19.3, §19.4 (partial), §20.3 (steps 1–6 plus its
Examples), §20.5 (R-WRT-06 window), §21.1, §21.2/21.4 rows T2/T3/T4/T5/T14/T26,
L44, §21.6, §21.7, §21.8 opening, §21.9.

## Derived numbers

- `[R-CNT-06]` states nine conditions — §2.3 corroborates independently: "two ...
  and the other seven", 2 + 7 = 9. §21.7's "as `[R-CNT-06]` shows by stating
  nine" **passes**.
- §20.5's "Neither obligation has a witness in the output alone" counts **two**
  (the ignore-lane carry-forward and the version_minor floor, the two obligations
  immediately preceding it); §21.7's Rationale counts **three** by adding the
  fresh file_id draw. Not a contradiction — §20.5's "Neither" is scoped to the
  two it follows. **Passes.**
- `[R-GEO-06]` disk ordinal = `c · N + s` for planar, `s` for interleaved; `s = Σ
  tᵢ · ∏_{j>i} Gⱼ` in **declared dimension order**. Hunk 3's arithmetic (N is the
  spatial-tile count, channel count enters `C · N` but no individual ordinal; a
  layer with N = 2 and channels (a,b) places a at 0,1 and b at 2,3, appending c
  adds 4,5) **checks out**: 0·2+0=0, 0·2+1=1, 1·2+0=2, 1·2+1=3, 2·2+0=4, 2·2+1=5.
- §12.1: bool element size 1, uint8 element size 1, planar bool plane sized by
  packing (⌈P/8⌉). Hunk 9's "a planar `uint8` channel re-declared `bool` keeps its
  element size of 1 while its plane goes from P · Bᶜ bytes to ⌈P/8⌉" **passes**.
- Hunk 3's "that cap is quantified over addressed tiles": `[R-COD-07]`'s own Note
  reads "The cap is quantified over the layer's *addressed* tiles". **Passes.**
- §21.8's "120 conditions over 275 instances" is untouched; hunk 3's new bar adds
  no row (§21.7 places it outside the register), so the counts are undisturbed.

## Citations checked

| citation | in | verdict |
|---|---|---|
| §21.7 (as the source of §21.1's stated test) | h7 | **FAIL** — see X-01 |
| `[R-CNF-07]` "the gate ... already applies" | h7, h9 | pass — §2.4: "Every detectable file-conformance violation named by this specification is assigned exactly one reader outcome" |
| `[R-CNF-13]` "individuates them" | h9 | pass on its face (§2.3: "one malformed state ... and not the requirement that defines it"; "Reach is per condition"), but see X-07 — §2.3 individuates *as §21.1 does*, i.e. by rows |
| `[R-CNT-06]` "by stating nine" | h9 | pass |
| `[R-ENC-06]` "fixed field widths are not a state a file can be in" | h9 | pass — §4 "No field's width is ever a writer choice" |
| `[R-ERR-01]` label placement | h9 | pass — sits at the close of the normative prose, not inside the Rationale |
| §21.6 "defined non-violations" | h8 | pass as a pointer; but see X-04 |
| §21.9 "limits" | h8 | pass |
| `[R-GEO-06]` "assigns any tile the layer stores" | h3 | pass — §11.4 |
| §11.2 "the addressed-tile count C · N" | h3 | pass — §11.2 |
| §14.5 (fill at a position that becomes real) | h3 | pass — §14.5: "at every padding position, a writer MUST encode, for each channel the position carries, that channel's fill value" |
| `[R-COD-07]` "(L44)" and "quantified over addressed tiles" | h3 | pass — L44 is the lz4 row; the Note quantifies over addressed tiles |
| `[R-ENC-04]` "on every quantity it designates" | h3 (untouched) | pass — §4.2 makes designation express |
| `[R-SLB-04]`, `[R-SLB-01]` | h4 | pass — both stated below in the same step |
| `[R-CNT-21]`, `[R-CNT-17]` (slack, entry_count) | h4 | pass — both stated below in the same step |
| `[R-SER-05]` carve-out | h5 | pass — §14.5 |
| §21.7 "records the consequence" | h5 | pass — §21.7's Rationale does say the §14 bar is unwitnessed where the live state is clean |
| T3, T14 (plane length) | h9 | pass — T3 decoded-payload length, T14 codec-1 entry length |
| T4, T5 (fills) | h9 | pass as row identities, **FAIL as an exhaustive claim** — see X-06 |
| §12.1 element sizes | h9 | pass |
| §9.7 (does not reconstruct history) | h9 (untouched) | pass |
| §11.1 "which is what schema-first creation needs" | h3 (untouched) | pass |
| §3.1 "defines *stored* against a generation" | h2 (untouched) | pass |

## Normative-force test (by LABEL, not by ">")

- h1 lands in a block opening `> **Rationale.**` → **non-normative** by
  `[R-CNF-01]`. Its content is a restatement; the normative statement is §20.3's.
  Correct placement.
- h6 lands in a block opening `> **Example — the three shapes a commit takes.**`
  → **non-normative**. Correct placement.
- h9's demoted block opens `> **Rationale.**` → **non-normative**; its new prose
  above (the test, the subject clause, the `[R-ENC-06]` distinction) carries no
  label and sits outside any block → **normative**, and carries `[R-ERR-01]`.
  The conversion moved the rule *up* into normative text, which is the right
  direction.
- h2, h3, h4, h5 are unblocked prose inside numbered step 4 → **normative**.
- h7, h8 are unblocked prose in §21.1 → **normative**. §21.1 says its own
  completeness is normative, so h7's inserted gloss binds.

No repair's only statement sits in a labelled block. **Check 3 passes for all
nine hunks.**

## Back-references checked (check 8)

| anaphor | before insertion | after | verdict |
|---|---|---|---|
| "Where a change does reach **them**" (§20.3, after h3) | "every one of those tiles' stored bytes" / the superseded generation's stored tiles, one sentence back | now two paragraphs back; nearest plural candidates are "the declared types", "the values a tile happens to hold", "a planar channel none of whose own tiles are stored" | **changed** — X-10 |
| "One effect is barred beside **it**" (h3) | n/a (new) | the §14 bar, named in the immediately preceding paragraph | ok |
| "exactly as **above**" (h3, twice) | n/a | the §14-bar consequence sentence | ok |
| "the tense is **both bars'**" (h3) | was "the bar's" — h3 swept it | both bars | ok, correctly swept |
| "the **§14 bar** is the whole of the test" (h4) | was "the bar above", which after h3 would have resolved to the ordinal bar | swept | ok, correctly swept |
| "What counts as such an alteration is the **§14 bar**" (h5) | was "the bar above" | swept | ok, correctly swept |
| "Of **its** two bars" (h1) | n/a (new) | nearest antecedent is "a layer that already stored tiles in the generation a commit supersedes"; intended antecedent is §20.3 | **degraded** — X-09 |
| "**that bar's** own tense" (h4) | "the bar's own tense" | the §14 bar | ok |
| "which is **the same step's** permission" (h6) | unchanged | §20.3 step 4 | ok |
| "**that clause's** own terms" (h9) | n/a (new) | §21.1's completeness clause | resolves, but misstates it — X-04 |
| "**this bars**" / "**this** bars nothing" (h3) | n/a | the §14 bar | ok |
| "the recommendation ... **below**" (h4) | n/a | the SHOULD later in the step | ok, forward reference is explicit |
| "the **re-emission rule above**" (h3) | n/a | the parenthetical in the same step | resolves, but its scope is misread — X-05 |
| "**those four**" (h3's worked example) | n/a | ordinals 0,1,2,3 | ok |

## Findings

X-01 … X-10 as returned in the structured result. Summary of the two
byte-level ones:

- **X-02** (hunks 2, 3 vs untouched carve-out): a `uint8` → `int8` re-typing of a
  planar channel all of whose stored bytes are ≤ 0x7F. The carve-out's principle
  permits the commit ("leaves every one of those tiles' stored bytes meaning
  exactly what they meant"); h3's declared-types test bars it. The post-commit
  file is fully conforming — plane length unchanged, padding positions still
  carry the recorded fill bytes, index lengths and crcs unchanged, no register
  row fires — so `[R-CNF-05]` does not bar it under the permissive reading and
  the emittable set moves.
- **X-05** (hunk 3 vs the untouched re-emission parenthetical): a commit that
  grows an extent *and* exchanges two planar channels. The parenthetical
  "(a geometry change renumbers ordinals wherever `[R-GEO-06]` moves them)"
  licenses the entries to be moved to their new ordinals — `[R-GEO-06]` moves
  them by both `N` and `c` — and the resulting file is conforming. h3's new bar
  forbids the commit outright.

## Rejected candidates

- *A dimension-declaration reorder can move a stored tile's disk ordinal without
  touching anything §14 fixes, and the new bar names only channel declarations.*
  Constructed the witness: d = 2, E = (4,4), T = (1,2) declared (y,x) → G = (4,2),
  s = t_y·2 + t_x, in-tile ordinal = u_x; re-declared (x,y) with T = (2,1) →
  G = (2,4), s = t_x·4 + t_y, in-tile ordinal = u_x. Same P, same decoded size,
  same in-tile offsets, no padding positions either way — yet tile (t_y=1,t_x=0)
  moves from s = 2 to s = 1. **Dropped**: this is a geometry change, and the
  re-emission parenthetical expressly renumbers for one, so the entries move with
  the tiles and nothing is lost. (It is the *combination* with a channel edit that
  bites — kept as X-05.)
- *Flipping a layer's `layout` field between planar and interleaved escapes both
  bars when C = 1.* **Dropped**: at C = 1 the disk ordinal is `s` under both
  (`0·N + s`) and the tile image is byte-identical, so the change alters nothing
  and is harmless. At C > 1 the decoded size changes and the §14 bar reaches it.
- *§20.5's "Neither obligation" (two) contradicts §21.7's "three obligations".*
  **Dropped**: §20.5's "Neither" is scoped to the two obligations it immediately
  follows; the fresh file_id draw is stated earlier in §20.5. No conflict.
- *Hunk 4 calls a SHOULD an "obligation" that "binds".* **Dropped**: BCP 14
  SHOULD does bind its actor, subject to stated exception; the sentence does not
  upgrade it to MUST.
- *Hunk 1 forward-references "the §14 bar" before §20.3 defines it.* **Dropped**:
  the preceding sentence in the same block names §20.3 explicitly, so the
  reference is anchored.
- *Hunk 3's "An interleaved layer is unaffected" could be read as immunity from
  every channel-declaration change.* **Dropped**: the sentence's stated ground is
  "its disk ordinal being s, which no channel declaration enters", which confines
  it to the ordinal bar; and the §14 bar's "byte offset of any sample within the
  decoded tile image" plainly reaches an interleaved channel reorder.
- *Hunk 2's "the sample type each value in the image is read under" is not
  something §14 fixes.* **Dropped**: the bar's preamble is "what §14 fixes for its
  stored bytes **or how they decode**", and §14.1/§14.2 read each value under its
  channel's declared type, so the item sits under "how they decode".
