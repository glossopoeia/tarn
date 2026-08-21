# R19 repair audit — witness transcript

Auditor scope: hunk-02.diff (§21.7 insertion) and hunk-03.diff (§23.1 rewrite).

## 0. Disclosure — what I read and ran

Read (files):
- `/private/tmp/.../r19audit/hunk-02.diff`
- `/private/tmp/.../r19audit/hunk-03.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — in slices, via `sed -n`:
  lines 96–240 (§2.1–§2.4), 305–325 (§3.1 vocabulary), 625–665 ([R-CNT-02]/[R-CNT-21]/[R-CNT-03]),
  786–832 (§6.3 version/flags/[R-CNT-26]), 1152–1170 (§9.1–§9.2), 1220–1245 (§9.3),
  1286–1320 (§9.6), 1319–1370 (§9.7), 1435–1445 ([R-EXT-04] "ancillary"),
  1478–1495 (§11.1 Rationale), 1520–1575 (§11.3–§11.4, [R-GEO-06]),
  2891–3040 (§20.3 whole append procedure), 3099–3150 (§20.4), 3149–3280 (§20.5),
  3272–3330 (§21.1), 3500–3580 (§21.5 tail, §21.6, §21.7 opening),
  3560–3640 (§21.6 tail + §21.7 entire + §21.8/§21.9 head), 3790–3870 (§22.4–§23.2),
  3973–4280 (spot: Appendix G item list 4232–4280).

Ran (grep/rg and one python3 whitespace-normaliser over tarn.md only):
- `grep -n '^#### 20\|^#### 9\|^### 20\|^### 9'`
- `grep -n 'R-WRT-06\|R-WRT-07\|R-PRV-01\|R-CNT-21'`
- `grep -n 'R-CNT-26'`, `grep -n -i 'version_minor'`
- `grep -n -i 'erasure\|erase'`, `grep -n -i 'unreachab\|reachab'`, `grep -n -i 'de-address\|deaddress'`
- `grep -n -i 'supersed'`
- `grep -n 'R-LIF-03\|R-CNF-07\|R-CNF-05\|R-CNF-02\b'`
- `grep -n 'BCP 14\|non-normative\|R-CNF-01'`
- `grep -n 'R-GEO-06'`, `grep -n 'R-PRV\|ancillary'`, `grep -n -i 'privacy'`
- `sed -n '3330,3470p' tarn.md | grep -n -i 'compact\|minor'` (register rows F/L for a
  compaction or version_minor row) → **no output**.
- a `python3` heredoc that joined hard-wrapped line ranges and printed them verbatim, so
  every quotation below is whitespace-normalised from the file, not retyped.

Not read: docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/,
spec/registry.json, git history, full.diff, hunk-01.diff, the web. I did not list the
r19audit directory. No breach.

Note on hard wrap: every conclusion below that rests on a phrase spanning a line break was
re-checked with the python3 normaliser above, not with a line-oriented grep.

---

## 1. Hunk 2 — §21.7 insertion

### 1.1 The text as it now stands (line 3593 onward, unwrapped)

Paragraph opener (unchanged):

> "A second set of obligations is omitted from the register because a single file exhibits
> no witness of their violation. Committed-prefix immutability and the generation sequence
> (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a file's history, which §9.7 does not
> reconstruct; …"

The tail, with the insertion (unwrapped from lines 3616–3624):

> "… and a commit that supersedes every tile it would have damaged leaves the live state
> clean, so the bar is unwitnessed there for the same reason `[R-LIF-01]` is: it is a
> property of the prior generation, which §9.7 does not reconstruct; **§20.5's floor on a
> compacted file's version_minor (`[R-WRT-06]`) is unwitnessed for that same reason, the
> output carrying no record of its input's minor;** and `[R-ENC-06]`'s fixed field widths
> are not a state a file can be in, since the parse is always at the widths this
> specification fixes … `[R-ERR-01]`"

### 1.2 The rule the repair asserts, in my words

Of an implementation: nothing. It asserts a *meta*-fact about the document — that the
obligation "a compacted output's version_minor is at least its input's" has no file-level
witness, and is therefore absent from the §21.2–§21.5 register by design rather than by
oversight. It creates no obligation, removes none, and licenses nothing.

### 1.3 Check 1 — tense and quantifier

Generation: the clause it hangs off ("a commit that supersedes every tile…") speaks of a
*prior generation of the same file*. The inserted clause speaks of a compactor's *input
file*, which is a different artifact: §20.5 (line 3169) — "a compacted file is a whole-file
rewrite under a new file_id by definition (`[R-LIF-01]`)" — and it is generation 1. So the
output has no prior generation at all. "for that same reason" therefore imports a ground
(§9.7 not reconstructing prior generations) that cannot literally apply. The repair
immediately supplies the correct ground in apposition — "the output carrying no record of
its input's minor" — which is why I did not raise this as a standalone finding; it is
folded into B-02's detail.

Quantifier: "§20.5's floor on a compacted file's version_minor" reads unconditional. The
actual floor is conditional. §20.5 (unwrapped, lines 3175–3183):

> "Where any such bit is set, the output's version_minor SHOULD be at least the input's: a
> compactor cannot know which minor version defined a bit it does not implement, and a
> lower minor states a feature floor the carried bit contradicts, misstating it to tooling
> as `[R-CNT-26]` describes. Where none is set, version_minor follows `[R-CNT-26]`, as it
> does for an appender (§20.3 step 6). **Neither has a witness in the output alone
> (§21.7).**"

The apposition ("no record of its input's minor") pins the entry to the first sentence
only. That is the undershoot recorded as B-01.

### 1.4 Check 2 — citations

| Citation in repaired text | Verdict |
|---|---|
| §20.5 — "floor on a compacted file's version_minor" | **PASS as to existence.** §20.5 does state a floor relative to the input. But it is a **SHOULD**, and it is conditional on a carried unknown ignore-lane bit. The entry states it flatly. |
| `[R-WRT-06]` | **PASS.** §20.5's first paragraph, which contains the floor sentence, closes with `` `[R-WRT-06]` `` at line 3186. Correct id. |
| "for that same reason" → `[R-LIF-01]` / §9.7 | **FAIL as stated, self-corrected in apposition.** §9.7 ([R-LIF-08], lines 1319–1364) walks the live state of one file and does not reconstruct that file's prior generations; its Note adds "compaction is expected to discard" history. A compactor's *input* is not a prior generation of its output. |
| §9.7 (inherited from the clause the entry attaches to) | **PASS for the clause it belongs to**, not for the new one. |
| `[R-ERR-01]` sentence terminator | **PASS**, still present and still terminating the same sentence. |

### 1.5 Check 3 — does the repair sit in normative text?

§21.7 lines 3590–3625 carry no ">" prefix (verified by eye on the `sed` output, and the
python3 join shows no ">" characters). §21.7 is inside §21, not §1, not an appendix, so
`[R-CNF-01]` leaves it normative. **Sits in normative text.** (Nothing normative is being
*created* here, but the placement is right for the kind of statement it is.)

### 1.6 Check 4 — contradiction in the same passage, including untouched text

Structure read in full: §21.7 both paragraphs (3589–3625), plus §21.1 (3272–3302), plus
§21.6 (3535–3577), plus §20.5 (3149–3266).

Collisions looked for and the result:

1. **§20.5 says "Neither"; §21.7 now answers one.** §20.5's forward reference "(§21.7)"
   covers two obligations: the input-relative floor (bit set) and "version_minor follows
   `[R-CNT-26]`" (no bit set). The insertion accounts only for the first. §21.7 contains no
   occurrence of `R-CNT-26` at all (`grep -n 'R-CNT-26'` → 824, 3026, 3180, 3181, 4242,
   4270 — none inside §21.7's range 3589–3625). The half of the forward reference concerning
   an appender's step-6 version_minor (line 3026, "version_minor per `[R-CNT-26]`; barrier.
   `[R-WRT-04]`") is likewise unaccounted for. → **B-01**.
2. **The list's stated ground vs. the item's keyword.** §21.7's ground is "no witness of
   **their violation**"; §21.1 makes §21.7 "the account, by class, of what fails" the
   detectability gate for "a *detectable* **file-conformance violation** this specification
   names". [R-CNT-26] and §20.5's floor are both **SHOULD** (§6.3, line 820: "A writer
   SHOULD emit the lowest version_minor that defines every feature present in the file";
   Appendix G line 4270 confirms: "`version_minor` at its floor, which `[R-CNT-26]` states
   as a SHOULD"). A SHOULD-departure is not a file-conformance violation, so it could not be
   a register row whatever the witness situation. §21.6 already carries the reader-side row
   "version_minor is higher than this text defines | Accepted; minors never gate |
   `[R-CNT-07]`" (line 3539). Every other member of §21.7's second paragraph that I checked
   is a MUST-shaped obligation ([R-LIF-01] §9.1 "a writer MUST NOT modify them";
   [R-CNT-13], [R-CNT-18], §20.3 step 4's "A commit MUST NOT change a layer's
   declarations…"). → **B-02**.
3. Any MUST the entry now lets an actor violate? No — the entry licenses nothing.
4. Any sentence written to be true only under the old wording? The preceding clause ("for
   the same reason `[R-LIF-01]` is…") was written about prior generations and is now the
   antecedent of "that same reason" for a case that has none — covered in B-02's detail.
5. Sentence parse end to end: the run is `…; and a commit that supersedes … does not
   reconstruct; §20.5's floor … input's minor; and [R-ENC-06]'s fixed field widths are not a
   state a file can be in …`. The new item is a bare semicolon-item between an "and"-item
   and the final "and"-item. That was already the shape of the run before the insertion (the
   pre-repair text had "and a commit that supersedes…; and `[R-ENC-06]`'s…"). It parses; the
   sentence still terminates in `[R-ERR-01]`. **No parse defect.**

### 1.7 Check 5 — exhaustive claims

Words scanned in the inserted text: "no record" ("the output carrying **no** record of its
input's minor").

I tried to falsify it. Candidate witnesses in the output alone:

- The carried unknown ignore-lane flag bits (§20.5: "The output trailer MUST copy the
  input's unknown ignore-lane flag bits forward"). Could a verifier argue "bit set ⇒ input's
  minor ≥ 1 ⇒ output's minor must be ≥ 1"? **No.** [R-CNT-26] is a SHOULD for the input's
  writer too, so a conforming input may carry a set ignore-lane bit *and* version_minor 0.
  §6.3's [R-CNT-08] confirms a set ignore-lane bit is "not a file-conformance violation".
  So nothing about the output bounds the input's minor from below.
- generation and file_id: §20.5 mints a fresh file_id and generation 1, so no linkage.
- Records carried forward: §20.4/§20.5 carry record bytes, not provenance; nothing this
  specification defines records the producing file's minor.
- The recovery probe of §9.6 scans *within one file*; a compaction output contains none of
  its input's trailers (only live structures are carried, §20.5 first sentence).

**The "no record" claim survives falsification.** It is true.

Also scanned: "unwitnessed" — see B-01 for the case it silently drops.

Register-row cross-check: `sed -n '3330,3470p' tarn.md | grep -i 'compact\|minor'` produced
no output, so the premise that this obligation is absent from §21.2–§21.5 is true.

---

## 2. Hunk 3 — §23.1 rewrite

### 2.1 The text as it now stands (lines 3823–3834, unwrapped)

> "The append-only model (§9.1) means that what a commit removes, it removes only from
> *reachability*. A commit removes sample data two ways — superseding it, and a shrink that
> de-addresses tiles (§20.3 step 4) — and a dropped ancillary record's extent (§20.4) goes
> the same way; no commit removes a layer at all. In each case the bytes remain in the file
> as slack (`[R-CNT-21]`), readable by anyone with the bytes and a hex editor, and
> recoverable by any tool that scans backward for an earlier trailer (§9.6). Writers and the
> tools built on them MUST NOT represent any commit that makes sample data unreachable as
> erasure of it — a shrink reported as a deletion misleads exactly as a supersede so
> reported does. `[R-PRV-01]`"

### 2.2 The rule the repair adopts, in my words

Of an implementation: a writer, or any tool layered on one, is forbidden from telling its
user that a commit **erased** data, for *every* commit that makes sample data unreachable —
not merely a supersede. The old rule bound only "a commit that supersedes data". The old
scope was one operation; the new scope is a property ("makes sample data unreachable") that
quantifies over all commits.

### 2.3 Check 1 — tense and quantifier

- Old subject: "a commit that supersedes data". New subject: "any commit that makes sample
  data unreachable". Quantifier widened from a named operation to a universally quantified
  property over commits. Correct direction: the defect being repaired was a false "only".
- Generation: the data made unreachable is the *superseded* generation's. §3.1 (line 313):
  "A tile is *stored in a generation* if and only if that generation's tile-index entry for
  it is not the sentinel … Superseded payload bytes from earlier generations do not make a
  tile stored." The repair's "removes … from *reachability*" is correctly about the new
  live state's reach over the prior generation's bytes. No tense slip found here.
- Object narrowed from "data" to "**sample** data" in the MUST NOT. Checked whether that
  loses coverage of the ancillary-record drop: under the old wording the prohibition was
  "a commit that supersedes data", and a §20.4 drop is not a supersede, so the old text did
  not cover it either. **No narrowing in practice.** Not a finding.
- Actor unchanged: "Writers and the tools built on them". Compaction is not a commit
  (§9.1: "either a commit (§9.2) or a whole-file rewrite under a new file_id (compaction,
  §20)"), so the widened subject does not reach a compactor, which §23.1's second paragraph
  handles separately. **The widening reaches no actor it was not meant to reach.**

### 2.4 Check 2 — citations

| Citation | Verdict |
|---|---|
| §9.1 "append-only model" | **PASS.** §9.1/[R-LIF-01] line 1156: "an append-only transaction that extends the file and never modifies a committed byte." |
| §20.3 step 4, cited for "a shrink that de-addresses tiles" | **PASS.** Step 4 (lines 2989–3006): "An extent MAY also **shrink** … Dropping a tile out of the addressed set (§11.2's grid count falls) is not itself such an alteration — a tile the new state does not address carries no §14 obligation and its extent becomes slack … Where a shrink is permitted the de-addressed tiles' extents become slack (`[R-CNT-21]`)". The word *de-address* appears nowhere else in the document (`grep -i 'de-address'` → 3005 and 3825 only), so the cite is exact. |
| §20.4, cited for "a dropped ancillary record's extent" | **PASS.** §20.4's table, MU = 0 / PE = 0 row (line 3123): "Retain byte-identical, or drop it — its extent becoming slack." "Ancillary" = MU = 0 per [R-EXT-04] (line 1441: "no record carrying them registers as ancillary") and §2.4 line 230 ("an unknown ancillary record is *ignored*"). Note the repair dropped the old "unknown" qualifier; §20.4's opening ("Persistence governs every record type; only the authoritative source of the flags differs") makes the unqualified form the more accurate one, so this is a small improvement, not a defect. |
| "no commit removes a layer at all" | **PASS.** §20.4 line 3126: "No commit therefore removes a layer record, or a user-metadata record at either scope"; and line 3123: "A commit changes the layer set by adding a layer; an appender never removes one (`[R-CNT-22]`, §7.3)." |
| `[R-CNT-21]` for "remain in the file as slack" | **PASS.** Line 630: "Every byte the live state does not claim is **slack**: alignment and slab gaps, the pre-trailer pad, and everything an earlier commit superseded." |
| §9.6 for "scans backward for an earlier trailer" | **PASS.** §9.6 line 1288: "probe backward at 64-aligned offsets o for the trailer magic". |
| §20.5 (second paragraph, untouched) | **PASS**, still true and undisturbed. |

### 2.5 Check 3 — does the repair sit in normative text?

Lines 3823–3834 carry no ">" prefix; §23 is not §1 and not an appendix; the paragraph is
not labelled Note/Example/Rationale. Under [R-CNF-01] it is **normative**. The MUST NOT is
in the same paragraph as the enumeration, so the widened prohibition has force. **Passes.**

Cross-check that no ">" block elsewhere is the sole statement of the widened rule: the only
occurrences of "erasure"/"erase" in the whole document are lines 2023 (an unrelated
"erased flash" example), 3821 (the §23.1 heading), 3832 (the repair), 3840 ([R-PRV-02]).
So [R-PRV-01] is stated once, in normative text, here. Good.

### 2.6 Check 4 — contradiction in the same passage, including untouched text

Read in full: §22.5, §23.1 both paragraphs, §23.2 in full, §20.3 step 4 in full, §20.4 in
full, §20.5's closing Note.

1. **Carve-out collision — "Discarding data is the caller's operation and this
   specification does not bar it"** (§20.3 step 4, line 3017). The widened prohibition does
   not bar the *operation*, only the *representation*, so these do not collide directly.
   Not a finding on its own — but see 2.
2. **The repair's own gloss contradicts the subsection's title and the document's
   vocabulary.** The rule bars representing something as **erasure**. The gloss says a
   shrink "reported as a **deletion** misleads". The subsection is titled "**23.1 Deletion
   is not erasure**" — i.e. *deletion* is the accurate word for a reachability removal and
   *erasure* is the forbidden claim. §20.5's closing Note (line 3263): "Compaction is the
   only true removal: **logical deletion** supersedes bytes but leaves them in the file as
   slack (`[R-CNT-21]`) — a privacy consideration (§23)." [R-PRV-02] (line 3840) uses
   "erasure" for the byte-destroying sense and "a filesystem-level deletion" for the
   reachability sense. The gloss therefore asserts that the document's own accurate label
   misleads. → **B-04**.
3. Any MUST elsewhere in the passage the new breadth lets someone violate? None found.
   [R-PRV-02] and [R-PRV-03] are unaffected; §23.2's SHOULD ("SHOULD compact before
   publication") is unaffected.
4. A sentence written to be true only under the old wording: **§23.2's sentinel clause**
   (line 3846, unwrapped): "a sentinel entry (§15.2) marks each addressed tile not stored in
   the live generation — **a tile unstored by a later commit leaves its earlier payload in
   the file as slack (§23.1)**". §23.2 names a removal in its own words, and points at §23.1
   as the account of it — §23.1 now says there are exactly two ways and does not name it. →
   **B-03**.

### 2.7 Check 5 — exhaustive claims, and the enumeration sweep the charter asked for

Completeness words in the repaired text: "**only** from reachability", "**two** ways",
"**In each case**", "**no** commit removes a layer at all", "**any** commit".

- "only from reachability" — falsification attempt: is there a commit that destroys bytes?
  §9.1 forbids modifying [0, F). §20.5's compaction is not a commit. **Holds.**
- "no commit removes a layer at all" — §20.4 line 3126 states it flatly. **Holds.**
- "**two** ways" — this is the closed count. Sweep of every way a commit can make sample
  data or a structure unreachable (from §20.3 step 4, §20.4, §15, §11):
  1. **Supersede a stored tile** — new bytes written for a tile, old extent slack.
     Enumerated. ✔
  2. **Unstore a stored tile** — its entry becomes the sentinel while the tile stays
     addressed; the tile thereafter reads as fill (§13, [R-IDX-02]) and the old payload is
     slack. §20.3 step 4 (line 2938, unwrapped) lists this as its own case, contrasted with
     supersede: "with entries for tiles this commit **stores or supersedes** written to
     their new state, **entries for tiles that become unstored written as the sentinel**,
     entries new to this generation…". §23.2 names it as "a tile unstored by a later
     commit". **Not enumerated in §23.1.** → **B-03**.
  3. **Shrink that de-addresses tiles** (§20.3 step 4). Enumerated. ✔
  4. **Drop an ancillary record** (§20.4) — not sample data; handled by the "goes the same
     way" clause. ✔
  5. **Remove a layer** — impossible (§20.4). ✔ Correctly stated.
  6. **Re-declare an empty layer freely** (§20.3 step 4) — a layer that stored no tile in
     the superseded generation has no sample data to lose. Not a way. ✔
  7. **Change a layer's declarations so prior-generation stored tiles decode differently** —
     barred outright by §20.3 step 4's MUST NOT. Not a way. ✔
  8. **Remove a channel from a planar layer** (which would de-address that channel's tiles,
     since [R-GEO-06] gives disk ordinal c·N + s). Considered and **not reported**: §20.3
     step 4 licenses only "grow", "shrink" (of extents) and free re-declaration of an empty
     layer; nothing in §11 or §20.3 states that a non-empty layer's channel set may change,
     so I cannot establish this is an available operation without reading beyond my scope.
     Recorded here for the maintainer, not raised as a finding.

  On whether item 2 is really distinct: the document uses "supersede" in two senses. Broad
  — [R-CNT-21] line 630, "everything an earlier commit superseded", which does cover an
  unstored tile's payload; and §21.7 line 3617, "a commit that supersedes every tile it
  would have damaged", which §20.3's "does not escape this by unstoring in the same breath"
  shows includes unstoring. Narrow — §20.3 step 4's index sentence quoted above, which
  contrasts "stores or supersedes" against "become unstored". Because both senses are live
  in the document, a closed count of "two" that names one of them cannot be read
  unambiguously, and §23.2's independent naming of the third operation settles it against
  the repair. This is the same shape as the defect the repair was fixing (the old text's
  "the only removal of sample data a commit performs"), one costume along.
- "**any** commit that makes sample data unreachable" — the MUST NOT itself is *not* short
  by one: unstoring makes sample data unreachable, so the prohibition covers it even though
  the enumeration does not. This is why B-03 is a defect of the enumeration, not of the
  prohibition, and why it is not byte-level.

### 2.8 Overshoot / undershoot / new ambiguity for hunk 3

- Overshoot: does the widened prohibition forbid something a writer legitimately needs?
  Tested against §20.3 step 4's "Discarding data is the caller's operation and this
  specification does not bar it" — the widened rule constrains only the *representation*,
  so a writer may still shrink, unstore and supersede freely and may still report the
  operation. **No overshoot in the MUST NOT.** The gloss, however, over-reaches into the
  word "deletion" — B-04.
- Undershoot: the enumeration — B-03.

---

## 3. Restatement sweep (both hunks)

Places that restate what these two repairs touch, and whether they were swept:

| Location | Text | Swept? |
|---|---|---|
| §23.2, line 3846 | "a tile unstored by a later commit leaves its earlier payload in the file as slack (§23.1)" | **No** — B-03 |
| §20.5 closing Note, line 3263 | "logical deletion supersedes bytes but leaves them in the file as slack" | Non-normative; still narrow (supersede only) and uses "deletion" for the accurate label — cited as the contradicting text in B-04 |
| §1 overview, line 61 | "Superseded bytes remain as slack until compaction reclaims" | §1 is non-normative ([R-CNF-01]); narrow but harmless |
| §21.6 row, line 3540 | "Bytes the live state does not claim — alignment gaps, the pre-trailer pad, superseded structures" | Consistent; no change owed |
| [R-CNT-21], line 657 | "Slack that holds superseded data is a privacy consideration (§23)" | Consistent |
| §20.5, line 3182 | "Neither has a witness in the output alone (§21.7)" | **Half-swept** — B-01 |
| §20.3 step 6, line 3026 | "version_minor per `[R-CNT-26]`; barrier" | Not in §21.7 — part of B-01 |
| Appendix H / Appendix G | `grep -i 'privacy'` → no hits in Appendices; `grep 'R-PRV'` → 3834, 3842, 3859, 3871, 3884 only, all inside §23 | Nothing to sweep |
| §21.2–§21.5 register | `sed -n '3330,3470p' | grep -i 'compact\|minor'` → no output | Nothing to sweep |

---

## 4. Byte-level test, per finding

The discriminating question in each case: does the disputed reading change which bytes a
conforming writer may emit, or a reader's accept/reject verdict?

- **B-01, B-02**: both are statements *about* the register's coverage. Neither reading
  changes any obligation on bytes. A compactor's version_minor obligation is a SHOULD either
  way; a file departing from it is conforming either way ([R-CNT-26] is a SHOULD, §21.6
  records "version_minor is higher than this text defines | Accepted"). **Not byte-level.**
- **B-03**: the MUST NOT already reaches an unstoring commit under both readings, so no
  actor's conduct forks. The enumeration governs prose, not bytes; and [R-PRV-01] governs
  what a tool *says*, never what it writes. **Not byte-level.**
- **B-04**: same — [R-PRV-01] constrains representation to a user, not emitted bytes. Two
  implementations could disagree about whether their UI may print the word "delete", which
  is not a byte on disk and not an accept/reject verdict. **Not byte-level.**

No finding in this audit forks the emittable set. I state that plainly rather than inflating
any of them.

---

## 5. Per-check verdicts

Hunk 2: check 1 — defect (quantifier drops one of two cases; anaphora imports the wrong
ground) → B-01, B-02. check 2 — citations resolve except "that same reason" → folded into
B-02. check 3 — passes, sits in normative text. check 4 — defect against untouched §20.5
text → B-01. check 5 — "no record" survives falsification; passes.

Hunk 3: check 1 — passes (widening is in the right direction, tense correct, actor scope
correct). check 2 — all six citations resolve, verified individually. check 3 — passes,
normative, and [R-PRV-01] is stated nowhere else. check 4 — defect: the gloss collides with
the subsection title and §20.5's vocabulary → B-04. check 5 — defect: "two ways" is short by
one, and §23.2 names the missing one → B-03.
