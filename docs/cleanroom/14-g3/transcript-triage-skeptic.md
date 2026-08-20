# Round 14 triage — skeptic lens — working transcript

## Access log

Read: `spec/tarn.md` only (§2.1–2.5, §4.7, §5.1, §5.2, §6.1–6.4, §7.1–7.4,
§9.5–9.7, §10.1–10.4, §11.1–11.4, §13.1–13.2, §15.3–15.4, §16.2, §17.2,
§18.1–18.2, §19.1–19.2, §20.3–20.5, §21.1–21.9, §24, Appendix G, Appendix H).
Ran two `python3` extractions over the register tables (below).
Listed `scratchpad/round14/` once (file names only — no `transcript-triage-*`
file was opened; the listing showed six walk transcripts and three quiz
transcripts and no triage files). Opened **no** walk transcript: every claim
below was checked against the spec text directly. Did not read `docs/`,
`PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`, git history, web.

## Mechanical check of the register

```
{'F': 56, 'L': 111, 'T': 57, 'R': 44} sum=268 rows=121
```

Cells sum to exactly 268 over 121 rows, matching §21.8's "121 conditions over
268 instances". So the register is internally consistent with itself; any
error is between the cells and §21.1's criterion, not in the addition.

Second pass: every row whose Condition carries `differs from` / `does not
equal` / `≠` / `is not exactly` / `other than` / `not a multiple`, with its
instance count. Applying §21.1's direction axis ("compares two quantities and
either can be the greater"):

- CRC comparisons (F14, F20, L37, L38, R2): no greater/lesser. Correctly 1.
- Value-set membership (L29, L31, L33, L35, L36, L43, L45): not magnitude
  comparisons; alternatives already enumerated. Correct.
- Multiple-of tests (F13, L40, L42): not two-quantity ordering. Correct.
- One-sided (F2, T12, T21 "larger than", L44 "exceeds"): correctly 1 direction.
- **L41** `offset ≠ previous offset + length` → cell enumerates `gap; overlap;
  out-of-ordinal placement`. The direction axis IS applied here, with no
  layout axis in the same cell. This kills the "direction axis only refines
  rows the layout axis already split" defence.
- **T3 / T14 / T22**: 6 each = 3 layouts × 2 directions.
- **F17, L21, L22, L30**: trigger the axis, cells do not enumerate directions.
- Marginal: **T26** ("a stride other than the mandated one") — either stride
  can be the greater; cell gives 3 (the layouts). Not named by any reporter.
  Flagged to the maintainer, not asserted.

## Group-by-group

### G1 instance-criterion (reader-01, writer-01, verifier-01, diagrams-02, register-01, adversary-01, quiz-01)

Seven reporters, same defect, four rows named by six of them (diagrams-02
omits L22). I tried hard to kill this and could not. Candidate killers:

1. "a row whose check ranges over a family without the condition changing
   shape states that range as a single instance (T24's *any codec*)" — could
   cover L30. Fails: the axis sentence is introduced as removing exactly this
   judgement ("Two axes recur often enough to be stated rather than judged
   each time"), and T14 uses the identical phrase "differs from" and
   enumerates the directions.
2. "where a row and the rule it cites diverge, **the rule governs**" — reaches
   a row's Condition against its governing requirement. The Instances column
   restates no requirement; §21.1 is its only authority. No rescue.
3. "One instance is one *distinguishable* file … the fields it reads are not
   instances, because no two files could differ." Fails: both directions of
   all four conditions are distinguishable files (fill prefix 3 vs 5 against
   element size 4; committed_file_length 256 vs 384 in a 320-byte file;
   entry_count N±1; extent_length above/below the formula).
4. A "coupled axes" reading (direction only where layout also splits) — refuted
   by L41, L39, L29, which enumerate alternatives with no layout axis, and by
   L21, which applies the layout axis and not the direction one in one cell.

Verdict CONFIRMED. Arithmetic: F17 +1, L21 +2, L22 +1, L30 +1 = 273, not the
268 §21.8 states. (Reporters variously said 272/273/274; 273 is what the
criterion yields on the four rows. 276 if T26 also triggers.)

Byte-level: no. Deciding text — §21.1: "The **Instances** column enumerates
what a conformance corpus builds for that row (§21.8): the row is the rule,
and each instance is one file." And §24 `[R-VEC-01]`: "The corpus is
**derivative**: a conforming implementation is one that satisfies this
specification's requirements, and where a vector's recorded expectation and
this specification disagree, this specification governs and the vector is
corrected." Both directions of each of the four conditions are already
rejected by the same governing rule at the same scope and tier, so no reader
and no writer forks. Severity: register-bookkeeping.

### G2 Example (c) vs step 4 (reader-02, diagrams-01)

Checked both texts. Step 4's bar is quantified over stored tiles ("for any
tile that layer stores") and closes "A layer that stores no tile MAY be
re-declared freely". The Example's test is geometric: "a layer with no padding
position and no pad bit", and §11.3 makes padding positions a property of
geometry ("Where Gᵢ · Tᵢ > Eᵢ, the tiles at the high edge of dimension i
contain **padding positions**"), not of which tiles are stored. Both
separating files (padding-bearing geometry, nothing stored; padding-bearing
geometry, only an interior tile stored) fall in the gap, and the Example's own
justification is conditional ("every stored tile it reaches" — it reaches
none). CONFIRMED.

Byte-level: no. §2.1: "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*". The
Example can only make an appender refuse an operation the format permits; the
files either appender emits are conforming. Severity: editorial.

### G3 quiz-02 — the tense of "any tile that layer stores"

This is the one I most wanted to refute and could not. Searched every
occurrence of "stores"/"stored tile" in the document. Findings:

- The only text that names a tense is §11.1's **Rationale**: "a shrink is
  barred wherever it alters what §14 fixes for a tile the layer *already*
  stores (§20.3)" — non-normative by §2.1, and it reads for the prior
  generation.
- Step 4 is demonstrably tense-aware elsewhere in the same paragraph —
  "entries for tiles this commit stores or supersedes", "entries for tiles
  that become unstored written as the sentinel", "entries new to this
  generation" — and then writes the bar with a bare "stores".
- Step 4's own gloss cuts the other way: "a change that reaches none of these
  for any tile the layer stores … leaves every stored tile conforming and is
  not what this bars." A commit that unstores every tile leaves every stored
  tile (of the committed generation: none) conforming.
- And the sentence after cuts back toward the prior generation: "re-emitting
  those tiles would strand the originals as slack … Such a change is a new
  layer, or a whole-file rewrite under a fresh file_id" — i.e. re-emitting the
  tiles inside the commit is contemplated and refused, which only makes sense
  if "stores" is read against the incoming generation.

So the normative text pulls both ways and the only tense-fixing sentence is a
Rationale. No deciding sentence found. CONFIRMED.

Byte-level: **yes**. Two separating operations, not one:
(a) quiz's own: change declarations and sentinel every entry in one commit.
(b) the bigger one: change a layer's codec while superseding every stored tile
    with re-encoded bytes in one commit — a routine "recompress this layer".
Under the prior-generation reading a conforming updater MUST NOT emit either
commit and must instead rewrite the file under a fresh file_id at generation 1;
under the committed-outcome reading it may. The appended byte sequence in (a)
and (b) is reachable by a conforming implementation under one reading and by
none under the other — no conforming updater can reach it from the same input
by any other route, since the alternative (unstore in commit 1, re-declare in
commit 2) yields a different file at generation g+2. No reader or verifier
verdict forks: §21.7 puts history properties beyond what a single file
witnesses, and both outputs are conforming files on their own bytes. That
leaves the "may emit" half of the test forked, which is enough.

### G4 adversary-02 — "an extent MAY always grow" vs `[R-COD-07]`

`[R-COD-07]` is unconditional on both sides ("Writers MUST NOT declare this
codec for a layer any of whose addressed tiles' decoded size exceeds
0x7E000000 … and a reader MUST treat such a declaration as a validity error at
layer scope, checkable from declarations alone"), and §2.3's `[R-CNF-05]` — "A
writer MUST emit only conforming files" — plus §20.4's "a record it modifies
is new output under its writer obligations" settle it: a permission inside
step 4 cannot license output another MUST NOT forbids. The reporter agrees the
question is decidable. What survives is that the only cross-reference is a
Note. PARTIAL, editorial, not byte-level.

### G5 Appendix G item 2 — "low eight digest bytes" (writer-02, diagrams-03)

The two reporters independently picked **opposite** readings — writer-02 the
trailing eight (0xD44980B7CE79C479), diagrams-03 the leading eight
(0xC0A188DEDE9C8C78) — from the same sentence and, in writer-02's case, an
actual sha256 over an actual file. That is as good a demonstration of
ambiguity as this process can produce. CONFIRMED.

Byte-level: no. Appendix G's own preamble: "It adds no requirement to any
actor: a writer ignoring it is fully conforming." §6.2 admits any nonzero
file_id, and no rule derives behaviour from its value. Severity:
design-decision (one word: "leading"/"trailing").

### G6 writer-05 — Appendix G item 3 leaves the first structure's offset free

§5.2 makes "structure" a defined term that excludes the front block: "Every
byte of the live committed state belongs to exactly one of: the front
signature block; **or** a **structure** — a stored-tile extent, a record
extent …, the directory, or the trailer." So "Each structure begins where the
previous one ended" has no antecedent for the first one, and nothing else in
item 3 or §5 fixes where it begins. Searched Appendix G, §5.1, §6.1 for a
head-of-file anchor; none. CONFIRMED, not byte-level (same preamble quote as
G5), editorial — the intended fix ("the first structure begins at offset 16")
is five words.

### G7 diagrams-04 — the recap omits item 10

The omission is real (I mapped all ten recap entries onto items 1–9). But the
paragraph carries its own guard: "**Read the numbered items as the list**;
this paragraph names what they are for, not how many there are." The reporter
reads the guard as disclaiming only the count. It disclaims more than that: it
tells the reader which text is the list, which is exactly the reliance the
finding posits ("a reader auditing that closure against the recap alone").
REFUTED, editorial.

### G8 writer-03 — no F, no slack total

`[R-CNT-21]`'s "a verifier MUST report the total number of slack bytes" is
unconditional; F is defined only as the live trailer's committed_file_length
(§5.1 "The file size of a conforming file equals the live trailer's committed
file length F"; §6.2's table "= F"); §9.7's walk starts "From the live trailer
it reads the live directory". At F8 (no trailer magic) or F14 (trailer CRC
fails, `[R-ENC-10]` bars acting on the field) there is no F and no walk, so
neither the total nor the partial-total formula evaluates. The nearest thing
to a foreclosure is `[R-CNT-02]`'s opening — "Coverage is a property of the
**live committed state**" — which does imply the obligation presupposes one;
it is an implication, not a stated precondition, and Appendix H's verifier
checklist restates the obligation with the same gap. CONFIRMED,
design-decision. Not byte-level: §2.3 — "An established violation takes
priority: a verifier that has established any violation reports
*nonconforming*, however many requirements it was unable to check" — so the
verdict is fixed and only the report's shape moves.

### G9 verifier-02 — the walk's own checks (L18, L40, L41, L42, L48)

The deciding sentence is inside `[R-CNT-21]` and the reporter quotes it
without letting it decide: "(a rejected layer's claimants are **not
enumerated, whether or not the rejection impeded reading them**)". The
qualifier exists for precisely the case where the claimants were readable —
and were in fact read, since L18/L40/L41 are detected by reading them. So the
layer's claimants drop out, the total is partial, and the verifier names the
scope that stopped the walk. Reading A (the walk "did enumerate" them, so no
partial arises) survives only by reading the gating clause as a description of
what happened operationally, which the parenthetical forecloses. The
reporter's sub-point (i) (sum vs union) is likewise decided in the text: "an
upper bound on the file's true slack, **never an under-count**" rules out
summing lengths when claimants overlap. REFUTED. One editorial residue worth
passing on: §9.7 says "a scope-level rejection **blocks** enumeration", which
reads narrower than `[R-CNT-21]`'s categorical parenthetical; aligning the two
phrasings would remove the reading the reporter found.

### G10 verifier-03 — foreign major

Two foreclosures, both quotable. §6.2's ordered validation: "A reader MUST
validate, in order: the trailer magic; the trailer CRC; the version gate
(§6.3) … and then, **those gates passed**, MUST validate all of the following
…: … committed_file_length equals the file size … dir_offset ≥ 16;
dir_length ≥ 4 …" — so F9/F10/F13/F16/F17 are unreachable behind a failed
version gate, and §19.1 step 2 repeats the order. And §2.3, on the verdict:
"a file declaring another major is neither conforming nor nonconforming under
it … that refusal is not a finding about its bytes", with *cannot establish*
named for exactly this ground ("as when the file names a format major version
it does not implement"). No violation can be *established* about such a file,
so the established-violation priority never engages. F5 alone is stated
flatly, but its verdict is decided by the same §2.3 sentence and a reader
rejects either way. REFUTED, editorial.

### G11 register-02 — §21.1's outcome-follows-from-scope vs §21.5

Checked: `[R-CNF-07]` lists four outcome classes; `[R-CNF-08]` maps the three
owning scopes (file/layer/tile) to three outcomes; §2.4 says "Every structure
this specification defines has exactly one **owning scope** — file, layer, or
tile". There is no scope that yields ignore-record, so §21.1's two general
statements are literally over-broad for ten of 121 rows. I looked for a
rescue in "Conditions attach to the finest structure they damage" (a record
is not an owning scope) and found none. The outcome itself is decided three
times over — `[R-CNT-25]` "notwithstanding the owning-scope mapping of
`[R-CNF-08]`", `[R-MTA-02]`, and §21.5's preamble — so nothing is
undetermined. CONFIRMED, editorial, not byte-level (`[R-CNF-12]`: "For a
nonconforming file no acceptance obligation exists — a reader MAY reject it
upon detecting any violation").

### G12 register-03 — the Governing rule cell's parenthetical convention

True that the convention is stated nowhere (I checked §21.1, §4.7's
presentation Note, §2.2). But which identifier governs is decided: §2.2
"Normative requirements carry identifiers of the form `[R-<PREFIX>-<NN>]`" —
the bare parenthesised forms are not identifiers of that form; §21.1 is
singular throughout ("the requirement that defines it", "the rule it cites");
and L26's parenthetical is "(§7.3 registry table)", which cannot co-govern.
`[R-VEC-02]`'s singular "that row's governing requirement identifier"
therefore has exactly one referent per row. PARTIAL (real editorial gap, no
operative ambiguity), editorial.

### G13 register-04 — `[R-MTA-05]` missing from §21.1's parenthetical

Factually right: `[R-MTA-05]` says "readers process the document unchanged"
and governs F27/L48, and §21.1's parenthetical names only `[R-SER-08]` and
`[R-CNT-22]`. But the clause the parenthetical hangs off is general — "For a
row whose Detector is *verifier*, the outcome names the scope at which the
damage is recorded, **not an obligation on any reader**" — and §2.3's
`[R-CNF-04]` states it independently: "a violation whose assigned detector is
the verifier imposes no reader obligation". Reading (b) is dead on arrival.
PARTIAL, editorial.

### G14 writer-04 — `[R-WRT-07]`'s two-case enumeration

The third case is real on this text's face. But §7.2 already puts it under its
registration — "Records with MU = 1 carry further references only where this
specification or **registry review (§10) defines them**" — and `[R-EXT-04]`
requires a registration to carry "an unambiguous specification of its
semantics — sufficient for independent implementation without consulting any
implementation". A compactor that implements such a type implements it from
that definition. So nothing is undetermined for any implementation of this
text; the sentence's justification is just stated as complete when it is
complete only for major 1's assigned types. PARTIAL, editorial.

### G15 quiz-03 — "decidable from index bytes alone"

Verified against §15.3: the six *structural* rows include "offset + length
overflows, or offset + length > F − 64 (non-sentinel)", and §15.3's own
preamble supplies F from outside the index ("For each entry, with F the
committed file length…"). So the sentence over-claims. In context it is
plainly contrasting with fetching stored payloads, and every reader has F by
§19.1 step 2, so no actor is misled about what to fetch. CONFIRMED,
editorial, not byte-level.

## Coverage

23 input ids, 15 groups, union checked by hand and by list length:
7+2+1+1+2+1+1+1+1+1+1+1+1+1+1 = 23. No id appears twice; none dropped.

Groups I tried hardest to kill and failed: G1 (four separate attempted
foreclosures, all fail — L41 is the row that breaks the best defence), G3
(searched every "stores" in the document; the only tense-fixing sentence is
non-normative), G5 (two reporters, opposite readings, one with a real digest).
Groups I killed: G7 (the guard sentence), G9 (the "whether or not"
parenthetical), G10 ("those gates passed" plus §2.3).

---
*Editorial note: one ordinary-English word meaning "the thing that came before" was substituted throughout this verbatim transcript (to "antecedent"), per the repository's vocabulary gate. No other change was made.*
