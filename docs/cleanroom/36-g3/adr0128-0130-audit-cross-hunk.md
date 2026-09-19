# Cross-hunk consistency audit — working transcript

## Disclosure

Before starting the task I was shown, as ambient context and not as part of
the brief: the project's `CLAUDE.md` (which only points to `AGENTS.md`, which
I did not read), a user auto-memory file (`MEMORY.md`) containing ~20 one-line
titles of prior findings about this same TARN project (e.g. "TARN repair
prose vs rules", "TARN closed-list exceptions compose", "TARN no lowercase
keywords", "TARN ADR status change gates quotes", etc.), a git status/log
snippet naming five recent commit subjects (ADR-0130, ADR-0128, ADR-0129,
Q-A8, "round 35's repairs"), and standard tool/skill/environment boilerplate.
None of this was used as evidence about the specification's text. I did not
open any memory file beyond its listed title, did not read AGENTS.md, and did
not treat the commit-subject list as informative about which of the three
commits I am auditing did what — I derived everything below from the 49 hunk
files and the spec text itself. Flagging this per the brief's instruction:
"If any appeared, say so in disclosure."

Paths matched the brief exactly: spec at
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, and
49 files matching `case/hunk-NN.diff` at the given path. I did not run a bare
`ls` on the case/ directory; I only globbed `hunk-*.diff` (which the brief's
"read every hunk-NN.diff file" instruction requires me to enumerate) and did
not open `full.diff` or any other auditor's working file.

## What I read

- `spec/tarn.md` in full, in chunks (offset/limit reads), plus many
  targeted re-reads of specific line ranges after grepping.
- All 49 `hunk-NN.diff` files in `case/`, in full (`cat`), grouped in six
  `Bash` calls.
- No other files. No `docs/`, no `PLAN.md`, no `OPEN-QUESTIONS.md`, no
  `AGENTS.md`, no `README.md`, no `conformance/`, no `registry.json`, no git
  history, no web.

## Grouping (by rule, not by section)

1. **Layer-record registry flags** (MU=1,PE=1 → MU=0,PE=0): hunk 12 (§7.3
   table), hunk 42 (Appendix C), hunk 27 (§20.4 flags paragraph), plus every
   rule that reads a record's flags: R-CNT-12, R-CNT-15, R-CNT-18, R-CNT-22.
2. **The drop**, every site: hunk 26 (shape (c)), hunk 23/24 (§20.3 step 4
   scope sentence), hunk 27/28 (§20.4 table + paragraph below it), hunk 29
   (§20.5 opening, "dropping" named case), hunk 31 (regeneration paragraph's
   "two disposals"), hunk 39 (§23.1), hunk 48/49 (Appendix H, writer and
   updater/rewriter checklist entries).
3. **Step 4's bar vs. its new scope sentence and the drop-and-add route**:
   hunk 22 (original bar restated), hunk 23 (new scope sentence), hunk 26
   (shape (c) cross-reference), hunk 28 (name freed for reuse).
4. **§20.1's writer-tier restatement** (creator/appender/rewriter as "shapes
   of operation" vs. the decode-based test): hunk 19, checked against §2.3
   (already read at lines 152–250), R-CNF-06, R-CNF-11, R-LIF-01, and against
   §20.5's obligations (hunks 29–33) and Appendix G item 2 (hunk 43).
5. **R-WRT-06 / R-WRT-07 / R-WRT-09**, each split between carried and
   re-created content: hunks 29, 30, 31, 33.
6. **Renamed actor sweep** (compactor → rewriter / appender+rewriter):
   checked every hunk that touches the word, then grepped the whole document
   for stragglers.
7. **First-commit's 17 wording repairs against the rules they restate**:
   hunks 1–18 individually checked against the sections/rules they cite
   (§4.7/R-ENC-15, §6.1/§6.4/§19.1/R-CNT-10, §10.2/§10.3/§19.3/§7.4 value
   sets, §20.3 step 4's T-code additions, §21.1/§21.5/§21.6 wording, §22.3
   vs. §5.2/R-CNT-02, Appendix G item 5 vs. §14.4's Note).

## Searches run (verbatim) and results

```
grep -n "compactor" tarn.md        -> 1 hit (line 438, a Note under §3.3)
grep -n "compaction" tarn.md       -> 8 hits, all uses of the *operation* noun
                                       (fine: "compaction" survives as the
                                       named rewrite case per hunk 29)
grep -c "compactor" tarn.md        -> 1
grep -c "compaction" tarn.md       -> 8
```
Control for the above: I confirmed the search terms are not wrap-sensitive
(both are single words, never split by the hard wrap), so a zero would have
been trustworthy; the 1 and 8 counts are exact hit counts on unbroken tokens.

```
grep -n "updater's or" tarn.md     -> 0 hits (confirms hunk 1 fully removed
                                       the "updater's or compactor's" phrase
                                       and nothing else uses that pattern)
grep -n "MU = 1, PE = 1" tarn.md   -> 0 hits (no stale flag pair remains)
grep -n "both registered" tarn.md  -> 1 hit, line 3474, about *implementing*
                                       both registered types, not about their
                                       flags — not a stale PE=1 claim
grep -n "never remov" tarn.md      -> 2 hits: line 3485 ("...drop a layer
                                       record, and never removes a
                                       user-metadata record...") and line
                                       4905 (Appendix H, same claim) — both
                                       correctly narrowed to user-metadata
                                       only, consistent with the new flags
grep -n "no commit remov\|No commit remov" tarn.md -> 0 hits (the old
                                       "No commit therefore removes a layer
                                       record" sentence, hunk 28's "-" side,
                                       is gone)
grep -n "critical" tarn.md         -> 2 hits, both about *unknown* MU=1
                                       records generically, never claiming
                                       the layer type itself is critical
```
Control: "critical" is a whole, unwrapped word; a zero here would have been
suspicious given the document's frequent use of it, so the 2-hit result was
cross-checked by reading both lines (3481, 4906) in full — confirmed neither
asserts the *layer* record is critical.

```
grep -n "R-CNT-12\]\|R-CNT-15\]\|R-CNT-18\]\|R-CNT-22\]" tarn.md
```
— read every citing sentence (13 for R-CNT-12, 12 for R-CNT-15, 9 for
R-CNT-18, 6 for R-CNT-22) in place; none still assert PE=1/MU=1 specifically
for the layer type, all are generic per-registered-type or per-unknown-type
rules that are unaffected by the flag change, or are the row citations
(F24–F29, L13/L14, L46/L47, L49, F28) which are already flag-value-agnostic.

```
grep -n "R-WRT-06" tarn.md   -> 8 hits, all read in place (§6.3 hunk-9
                                  region, §20.4 table MU=1 row, §20.5 x4,
                                  §23.2, Appendix G item 2 and item 8,
                                  Appendix H)
```
Only one closing definition (`\`[R-WRT-06]\`` alone at end of a paragraph,
line 3592); every other occurrence is an inline citation. No duplicate
"defining" tag found — the pattern matches this document's normal citation
style (e.g. R-WRT-01, R-WRT-07, R-WRT-09 all show the same one-definition/
many-citations shape on inspection).

```
grep -n "index_encoding" tarn.md; grep -n "^#### 15.1\|^#### 7.4" tarn.md
```
Confirmed §7.4 (line 1129) is where index_encoding's actual value set (1
valid; 2–0x7F reserved; ≥0x80 experimental) is defined inline in the layer
record's field table; §15.1 (line 2185) only *consumes* the value ("... the
only encoding this format major version defines ..."). So hunks 15/16/18,
which swap the §10.2/§10.3/§19.3 citations from §15.1 to §7.4, correct a
citation rather than introduce an error; L31's row (line 3891) already cited
§7.4, confirming the correction's direction.

```
grep -n "single-channel" tarn.md; read §14.4 in full (lines 2121-2150)
```
Confirmed the Note at line 2134 says exactly what Appendix G item 5's new
sentence (hunk 45) attributes to it ("A single-channel numeric layer produces
byte-identical tile images under either layout") — correct citation, and the
added sentence closes a real gap (the layer record's layout *field* still
needs pinning even where the tile bytes don't differ).

```
grep -n "R-CNT-10" tarn.md
```
Read all 6 hits (§6.1 hunk-7, §6.4 hunk-10 x2, §19.1 hunk-17, F17 row,
Appendix bibliography). §6.1, §6.4 and §19.1 now agree with each other and
with R-CNT-10's own text: F is carried in the suffix-range response only
"where the transport discloses a range response's complete length"; where it
doesn't, R-CNT-10's probe-or-fail rule governs. This is a genuine, consistent
three-site fix of what was an overclaim ("carries F" unconditionally, and
"[the local/remote distinction governs §6.4] and nothing else" — falsified by
R-CNT-06's own text at line 864-865, which is local/remote-sensitive).

## Detailed cross-hunk checks

### A. Registry flags (Group 1) — consistent

§7.3 (hunk 12), Appendix C (hunk 42) and §20.4's flags paragraph (hunk 27)
all now agree: layer = MU=0/PE=0, user-metadata = MU=0/PE=1. Every reader of
R-CNT-12/15/18/22 I found is flag-value-agnostic language (applies to
"a type §7.3 registers" or "an unknown type" generically) and needed no
edit. No stray "critical"/"MU=1"/"PE=1"/"never removed" claim about the layer
type survives. **No defect found in this group.**

### B. The drop, every site (Group 2) — consistent, with one caveat

§20.4's table row (MU=0,PE=0) generalizes to *any* such record; the paragraph
below it (hunk 28) narrows back to the two registered types by name ("A
commit MAY therefore drop a layer record, and never removes a user-metadata
record") — this is *not* an overclaim, because it is explicitly a
consequence of the registered-type-specific paragraph it concludes (line
3460-3465 sets up "For a type §7.3 registers ..."), not a restatement of the
general MU=0/PE=0 rule; the general rule is separately and correctly restated
in shape (c) (hunk 26: "dropping a layer or *another* PE = 0 record"). §20.5's
opening (hunk 29) names dropping as one of three rewrites; the regeneration
paragraph (hunk 31) gives "two disposals" (drop the layer, or refuse) for an
un-repointable index entry — checked this against §20.5's opening sentence
("Dropping is the one disposal that answers, and only where §20.4's table
licenses it ... Where the table does not license a drop the rewriter MUST
refuse") and it is the same rule restated for a concrete case, not a
contradiction: both readings agree dropping is available only where licensed,
and refusal is the fallback. §23.1 (hunk 39) and Appendix H (hunks 48-49) both
correctly narrowed from "no commit removes a layer at all" to "a commit that
drops a layer strands every tile it stored" / "drops a layer record only
under §20.4's PE = 0 licence." **No contradiction found in this group.**

### C. Step 4's bar vs. the new scope sentence (Group 3) — real but
non-byte-level ambiguity (reported as finding X-01)

See finding X-01 below.

### D. §20.1's two tests (Group 4) — contradiction (reported as finding X-02)

See finding X-02 below.

### E. R-WRT-06/07/09 split between carried and re-created content
(Group 5) — consistent

R-WRT-07 (hunk 31) now explicitly splits: "MUST preserve the content of
every structure it carries forward" vs. "what a re-created layer denotes is
the rewriter's to declare," and the bit-for-bit R-MDL-02 equality is narrowed
to "every layer the output carries forward." R-WRT-09 (hunk 33) splits the
same way: the checksum-chain verification duty is over "what it carries," and
"what it re-creates it decodes as a reader first, owing every check §19.3 and
§19.4 place at that use." Both splits are well-formed and consistent with
each other and with hunk 30's "A layer the rewrite re-creates is new output
... nothing of the input's copy of that layer is carried forward." T17 (zstd
frame-magic check) exists in the register exactly where hunk 24 cites it.
**No defect found in this group**, other than the file_id/flags interaction
with Group 4's finding (X-02), which is really about R-WRT-06 specifically.

### F. Renamed-actor sweep (Group 6) — two stragglers found

See findings X-03 and X-04 below.

### G. First commit's 17 wording repairs vs. what they restate (Group 7)
— consistent, with the citation checks recorded above

§4.7 (hunk 3/4): the name-length-prefix sentence now correctly separates "a
name's value, which includes its structural role" from "the length prefix
is §7.4's framing, not its value" — checked against R-ENC-15 (duplicate
name is a validity error) and R-ENC-12 (name uses a u8 prefix), consistent.
§21.1 (hunks 34-36): the "quarantine ... every way a §21.5 row makes the
document unreadable" language now matches §21.5's own text almost verbatim
("every way its document can be unreadable takes this outcome," line
3953-3954) — this fixed what would otherwise have been a quantifier mismatch
("every §21.5 row" vs. "every way ... unreadable," since not every one of
R1-R10 individually is phrased as a way of being unreadable, R2's CRC failure
and R4's frame-constraint rows are two different mechanisms of the same
"unreadable" outcome). §22.3 (hunk 38) now matches §5.2/R-CNT-02's own
partition definition exactly (front signature block is *not* itself a
"named structure" in that partition — checked verbatim, line 703). Appendix
G (hunks 43-47) items 1-10 and the closing "everything else" paragraph now
list matching sets of degrees of freedom (item 5's filter/tile-extent/layout
additions are mirrored in the closing paragraph). **No defect found in this
group** except the actor-word slip inside item 8, reported as X-04 (also
counted under Group 6, since it's a rename-sweep casualty).

## Findings

Reported via the structured tool. Summary:

- **X-01** (NEW_AMBIGUITY, non-byte-level): §20.3 step 4's new "scope
  sentence" (hunk 23) plus the layer-drop licence (hunks 27/28) let a commit
  achieve, under one file_id and with byte-for-byte identical resulting
  bytes, exactly what the fixed-declaration bar forbids (silently
  re-declaring a stored tile's meaning) by relabeling it "drop layer X, add
  new layer X," reusing the same physical tile/index bytes. Confirmed
  non-byte-level under the document's own R-CNF-02 framework (the bar is
  conduct, not file-conformance), but it is a genuine new ambiguity this
  round's changes introduced (the prior text required a *whole-file* rewrite
  with a fresh file_id for this case, which made old-file/new-file
  unambiguous; now the same-file_id commit path reopens the ambiguity).

- **X-02** (LOCAL_CONTRADICTION, byte-level): §20.1's new "two tests"
  sentence (hunk 19) — "one that decodes everything it writes is a creator,
  whatever it read" — can reclassify a legitimate, fully re-creating rewrite
  (§20.5's own "re-declaring" case, applied to every layer, with nothing
  carried forward undecoded) as a *creator* rather than a *rewriter*. That
  reclassification changes what the output's trailer `flags` field MUST
  contain (creator: 0, vs. rewriter: the input's carried-forward ignore-lane
  bits per R-CNT-08/hunk 9) and how file_id MUST be derived (creator: a mere
  SHOULD toward randomness, permitting Appendix G item 2's deterministic
  content-hash derivation; rewriter: R-WRT-06's mandatory "new draw," and
  Appendix G item 2 (hunk 43) explicitly says a rewriter must NOT use the
  derived-hash rule because on an already-compact input it "would reproduce
  the input's own file_id" — exactly the cache-contract violation R-WRT-06
  exists to prevent). This is a genuine byte-level fork for the same
  underlying operation.

- **X-03** (UNSWEPT_RESTATEMENT, non-byte-level — inside a Note, §1 exempt
  rule doesn't apply but Note-labeling does): line 438, §3.3's Note, still
  reads "verifiers, appenders, and compactors operate on files whose layers
  they cannot decode" — "compactors" was not swept to "rewriters" (or
  "appenders and rewriters") along with the other fifteen renamed sections.

- **X-04** (LOCAL_CONTRADICTION, non-byte-level — Appendix G is explicitly
  non-normative): line 4800, Appendix G item 8 — "A compaction's output is
  therefore reproducible only modulo its trailer and the records §20.4 lets
  it drop" — uses "compaction" (which hunk 29's own new definition fixes as
  carrying *every* structure forward and dropping nothing) as the subject of
  a sentence about dropping records, while the same sentence's later clauses
  correctly say "the rewriter implements" / "the rewriter's choice." An
  apparent renaming-sweep slip: "compactor's" should have become "the
  rewriter's" (as it did two lines later), not "compaction's."

## Rejected candidates

- Considered flagging the "two disposals" (hunk 31) vs. "Dropping is the one
  disposal that answers" (hunk 29) as a contradiction; on close reading both
  agree (drop where licensed, refuse otherwise; "two disposals" just
  enumerates the two branches of the same rule already stated). Dropped.
- Considered flagging §20.4's "never removes a user-metadata record" (hunk
  28) as an overclaim once the general MU=0/PE=0 drop rule exists for other
  record types too; on checking, this sentence is explicitly scoped to the
  two *registered* types by its own preceding clause, and the general rule
  is separately and correctly stated in shape (c) (hunk 26). Dropped.
- Considered flagging Appendix H's "as a new layer or a whole-file rewrite"
  (line 4896, untouched by any hunk) as stale, since it doesn't mention the
  drop-and-add mechanism by name; on checking, "a new layer" already covers
  that route (it's the same phrase hunk 22 uses for the same option), so no
  edit was actually needed there. Dropped.
- Looked for a NESTED_DASH defect across all "+" lines of every hunk with
  ≥6 em-dashes (hunks 19, 28, 29, 30, 31, 33, 34, 37, 38, 44, 48); found
  several single open-dash asides and several ordinary dash *pairs*, but no
  case of a dash pair sitting inside another dash-delimited clause. None
  reported.
