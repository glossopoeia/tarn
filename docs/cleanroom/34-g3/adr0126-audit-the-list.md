# Audit transcript — hunks 09, 10, 11 (§20.3 step 4, the closed list)

## Access disclosure

Read exactly:
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (via `sed -n` / `grep` / `python3` over it — never opened anything else with Read).
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r34-audit/case/hunk-09.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r34-audit/case/hunk-10.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r34-audit/case/hunk-11.diff`

Did not read `full.diff`, other hunk files, docs/, PLAN.md, AGENTS.md, README.md,
conformance/, spec/registry.json, git history/log/diff, or the web. Did not list
the case/ or out/ directories (only scratch/ was listed, to confirm/create it).

**Contamination disclosure.** My system context (outside the charter) contained a
project CLAUDE.md pointer, a MEMORY.md index of past-session note titles (e.g.
"TARN repair prose vs rules", "TARN permissions, not carve-outs", "No nested
em-dash phrases"), a userEmail block, a currentDate block, and — mid-session —
an unrelated environment/tooling reminder block (browser/skill tooling
instructions, an "Auto Mode Active" notice suggesting I prefer Bash over
Read/Edit). None of this is part of the specification or evidence about it. I
did not use the MEMORY.md titles as leads or conclusions — every claim below is
derived only from the spec text and the three hunk files, re-derived from
`grep`/`sed`/`python3` output shown here. Where the "Auto Mode" reminder
suggested preferring Bash to Read, I used both interchangeably per the harness's
own file-access rules; it authorized no new file access and I did not treat it
as such.

**Scratch files written:** none needed keeping — all `python3` work below was run
inline via heredocs through Bash and its stdout is quoted here; no file was
written under `scratch/the-list/`.

## Hunk file headers vs. bodies

All three hunk files' headers say "nearest preceding heading ... line 3141,
'20.3 The append procedure'" and each names a landing-line range. I opened
`spec/tarn.md` at those ranges and confirmed the body of each hunk's `-`/`+`
lines is present verbatim in the live document in its post-repair (`+`) form,
at the stated location, inside numbered step 4 of §20.3. No header/body
mismatch found for any of the three.

One cross-reference note: the charter's "Hunk 09" bullet discusses the clause
"the position of every planar channel the new state keeps" as if it belongs to
hunk 09. On inspection this clause's `-`/`+` lines are actually inside
**hunk-10.diff**, not hunk-09.diff (hunk 09 only touches the "declared,
changed, re-established or cleared" line). I flag this discrepancy per the
access rule's instruction, but treat the charter's request as intentional
cross-referencing (the position clause and the slab/alignment member interact
in the same paragraph), and attribute any finding about that clause to hunk 10,
where its diff lines actually are.

## The full passage read in full

Read `spec/tarn.md` lines 3141–3340 in full (the whole of §20.3's lead-in and
all of step 4 through step 6, plus the Note/Example that follow) before judging
any hunk, per instructions. Quoting the load-bearing parts inline below rather
than repeating the whole block.

Step 4's structure, in order:
1. Opening mechanics paragraph (payload/index write, re-emission rule,
   "every other entry byte-identical at its disk-ordinal position ... and
   nothing else this step permits moves one").
2. Paragraph A — the **permitted-changes list** (five members: name/dim/channel
   names; extent growth; planar channel-list extend/shorten; **the fifth
   member, hunk 09**: slab/alignment declared/changed/re-established/cleared),
   plus the "several at once" combination rule and its one exception.
3. Paragraph B — the **fixed (MUST NOT) list**, ending in the MUST NOT bar,
   **hunk 10's insertion** right after the bar, then "Between them the two
   lists reach every declaration field of §7.4 ...".
4. "The tense is the prior generation's ..." paragraph (empty-layer carve-out).
5. "The line is drawn where a stored tile's meaning is fixed" paragraph — this
   is the paragraph that states the **T-row exceptions** central to my hunk-10
   finding below.
6. The bounds paragraph (`[R-COD-07]`, `[R-ENC-04]`, `[R-GEO-01]`, §4.6,
   `[R-ENC-15]`).
7. The closing paragraph: slack, **hunk 11's slab sentence**, and the
   (untouched) alignment sentence beside it.

## Hunk 09 — the fifth member

### The rule it adopts

Before: "a slab or alignment declaration MAY be declared, re-established or
cleared as this step provides below." After: adds "changed" as a fourth verb.
The rule made true of an implementation: a commit that already has a
slab-or-alignment declaration on a tile-storing layer MAY set it to a
*different* value in one step, not only re-affirm the same value, first
establish one, or remove it.

### Check 1 (tense/quantifier) and check 6 (transitions)

Per charter, enumerated every transition of A (alignment), S/A_slab (slab) and
ran the check-5-style completeness test, then checked whether "as this step
provides below" (→ the closing paragraph, hunk 11 + the untouched alignment
sentence) and `[R-SLB-01]`/`[R-SLB-04]` give the obligation for each:

| Transition | Verb | Reached by "below"? | Obligation source |
|---|---|---|---|
| none→some (declare) | declared | yes | `[R-SLB-04]` applies because "layer slab-declared in ... the new generation"; alignment sentence's "aligned layer's stored tiles ... satisfy its invariant" applies since the layer is now aligned |
| some(v)→some(v) (no value change, but tiles/placement change) | re-established | yes | both cited rules trigger on stored-tile-set/placement changes independent of whether the value itself changed |
| some(v1)→some(v2) (changed) | changed | yes | `[R-SLB-04]`'s trigger list explicitly includes "the slab declaration itself" changing; the alignment sentence's invariant test automatically uses the *new* A, so a changed A is covered without needing a separate clause |
| some(v)→none | cleared | yes | `[R-SLB-04]`'s "or clear the declaration"; alignment sentence's "or the declaration is cleared" |
| switch A→S or S→A in one commit (`[R-CNT-16]` exclusivity) | decomposes into "cleared" (for A) + "declared" (for S), or the reverse | yes, as a composition of two already-covered transitions | `[R-CNT-16]` (verified: "Declaring both A ≠ 0 and S ≠ 0 is a validity error at layer scope: the per-tile alignment and slab declarations are mutually exclusive") only constrains the *final* state, which the decomposition satisfies (one field ends at 0, the other nonzero) |

Confirmed `[R-CNT-16]`'s exact text at spec/tarn.md:1136 ("Declaring both A ≠ 0
and S ≠ 0 is a validity error at layer scope ... `[R-CNT-16]`") and its
register row at line 3787 ("L20 | A layer record declares both a per-tile
alignment A ≠ 0 and a slab S ≠ 0 | ... | `[R-CNT-16]`").

Read `[R-SLB-01]` (§16.1) and `[R-SLB-04]` (§16.2, end) in full — quoted above
in the passage read. `[R-SLB-04]`'s own verbs are only "re-establish [the
invariants]" and "clear [the declaration]" — it never itself says "declared" or
"changed" of a declaration. I checked whether this is a problem for the
"changed" transition specifically (the one this hunk adds) and concluded it is
not: `[R-SLB-04]`'s applicability clause ("of a layer slab-declared in either
the superseded or the new generation") and its explicit trigger ("or the slab
declaration itself [changes]") together reach exactly the "changed" case, and
its outcome (re-establish the run invariants, or clear) is stated as a single
test that does not need to vary by which of the four verbs describes the
transition. No gap found.

### Check 5 (exhaustiveness of the four verbs)

Tested whether {declared, changed, re-established, cleared} exhausts the
possible transitions of a scalar-valued declaration (none↔some, some↔different
some). It does. For the compound slab declaration (S, A_slab together per
§16.2: "A layer MAY declare a slab run length S ≥ 1 with slab alignment
A_slab"), a change to either component alone still falls under "changed" since
`[R-SLB-04]` treats "the slab declaration itself" as one entity. No falsifying
transition found.

### Check 4 (the safety-explanation sentence, per charter's specific hint)

Charter's checklist for hunk 09 warns to check for "a sentence explaining why
the member is safe that is true of the old verbs and unexamined for the new."
Found the candidate, in "the line is drawn" paragraph (untouched by any of the
three hunks): "a slab or alignment declaration governs placement (§16), not a
value, its coordinate or its padding." Tested this against the new "changed"
verb specifically: changing S, A_slab or A only ever moves *where* bytes sit,
never what they decode to — this holds identically whether the declaration is
freshly declared, changed to a new value, re-established, or cleared. The
sentence is not verb-specific in its own wording and remains true under
"changed." No defect found here.

### The position clause (hunk 10's diff, discussed here per charter cross-reference)

Old: "the position of every planar channel but the last." New: "the position of
every planar channel the new state keeps."

Constructed, per charter:
- **Extension** (add k≥1 channels at the end): new-state set includes both the
  retained old channels and the new ones. The MUST-NOT-change bar, applied to
  a genuinely new channel, is vacuous (no prior position exists to violate),
  so old and new phrasing behave identically for a 1-channel extension, but
  **old phrasing was actually ambiguous/wrong for a k≥2-channel extension**:
  "but the last" (singular) would still nominally include the second-to-last
  channel in the fixed-position set even though it too is new this commit
  (never had a prior position). New wording sidesteps this by naming the set
  directly rather than by exclusion-by-ordinal.
- **Shortening** (remove k≥1 channels from the end — confirmed multi-channel
  shortening is licensed: "one that extends it removes none, whatever the
  counts"): new-state set excludes every removed channel. Both old and new
  phrasing are functionally equivalent here since a removed channel has no
  observable position either way, but old "the last" was ambiguous about
  *which generation's* last channel was meant (the new state's remaining last,
  or the superseded state's removed last) — new wording removes this ambiguity
  by keying off "the new state" explicitly.
- **Shortening with a growth in the same commit** (both licensed
  simultaneously — extend/shorten is only forbidden in combination with itself
  on the *same* channel list, not with an extent growth): growth renumbers
  disk ordinals ("a growth renumbers ordinals wherever `[R-GEO-06]` moves
  them"), but "position" here denotes a channel's *index* in the channel list,
  a different quantity from its *disk ordinal* (which is a function of index
  and N together, c·N+s). The two do not collide: the fixed-position bar still
  binds only the retained channels' list-index, and index renumbering across a
  growth is a separately licensed operation.

Confirmed via grep that the old phrasing has zero remaining occurrences in the
document (see Sweeps), so there is no stale restatement of the superseded
wording left uncorrected.

**Verdict on the position clause: no defect found.** New wording is strictly
better (removes the generation ambiguity of "the last") and does not lose
anything the old wording excluded.

## Hunk 10 — the bar's category sentence

### The rule it adopts

Inserted after "... the change is a new layer, or a whole-file rewrite under a
fresh file_id (`[R-LIF-01]`, §20.5)." and before "Between them the two lists
...": "This bar binds the commit as an actor: the file a violating commit
would produce is conforming, the violation is not a file-conformance violation
(`[R-CNF-02]`), and no register row records it (§21.7)."

The rule this makes true of an implementation, read literally: for *any*
violation of the fixed-declarations bar (changing any of layout,
linearization, index encoding, codec, filter, rank, dimension order, tile
extent, channel type/fill, interleaved channel list, or planar channel
position on a layer that still stores a tile from the superseded generation),
the resulting file is conforming, and no register row ever fires because of it.

### Check 2 — citations

- **`[R-CNF-02]`** (opened at spec/tarn.md:160–178). It states: "A writer
  obligation whose violation this specification expressly declares not to be
  a file-conformance violation binds the actor in the same way [as a conduct
  rule] ... §6.3's flags rules ... §6.2's pre-trailer gap ... and
  `[R-LIF-02]`'s barriers ... are the cases this text states, **and each is
  declared where it arises rather than enumerated here**." So `[R-CNF-02]`
  does **not** itself say the fixed-declarations bar is such a case — it
  explicitly disclaims completeness and defers to wherever such a declaration
  is made. Read this way, hunk 10's sentence is functioning as exactly the
  kind of "declared where it arises" instance `[R-CNF-02]` anticipates, which
  is a legitimate pattern. **This part of the citation checks out as a
  pattern-match, not as a false pointer** — `[R-CNF-02]`'s own enumeration is
  not "short by this one" in any defect sense, since it was never meant to be
  exhaustive. (Answering the charter's specific question: no defect here.)
- **§21.7** (opened in full at spec/tarn.md:3949–3993, "What no check
  detects"). This section states the *general test* for
  unwitnessed-vs-detectable, and crucially states: **"The subject is the
  condition and not the requirement, as `[R-CNF-13]` individuates them and as
  `[R-CNT-06]` shows by stating nine. A single requirement states conditions
  of both kinds where it states several, and is classified as a whole by
  neither."** This is the opposite of what hunk 10 does with it: hunk 10 cites
  §21.7 to classify "this bar" — a single requirement that states many
  conditions (one per fixed declaration) — as a whole ("no register row
  records it," unqualified). §21.7 itself says a single requirement stating
  several conditions **cannot** be classified as a whole. The specific,
  per-condition classification for this exact bar is not done by §21.7 at all
  — it is done three paragraphs later in the very same step 4, by "the line is
  drawn" paragraph, and *that* paragraph's classification is not uniform (see
  Check 4 below). **Citation does not carry the claim it is attached to
  support** — this is the "citation that points at a rule which almost says
  the claimed thing" trap called out in the charter.

### Check 4 — contradiction within the same passage (not touched by the hunk)

Read forward to "the line is drawn where a stored tile's meaning is fixed"
paragraph, still inside step 4, untouched by any of the three hunks:

> "... with every checksum in §8 certifying the result and, but for a decoded
> size, a padding position or pad bit, or a boolean byte the register
> witnesses (T3, T14, T21, T22, T4, T5, T2) and a decode that fails outright
> under a changed codec or filter (T24, T25), no check any actor owes able to
> see it (§21.7)."

This is an explicit, *non-uniform* application of the very same §21.7 test to
the very same bar: it says most violations of the bar are unwitnessed (no
check sees them) **but for** the nine enumerated exceptions — which are
exactly the register rows T2, T3, T4, T5, T14, T21, T22, T24, T25. I confirmed
each of these rows exists in §21 and is about exactly the kind of consequence
an illegitimate codec/filter/fill change on the bar would produce:

```
T2  | interleaved bool byte not 0x00/0x01 at a real sample position | R-SER-08
T3  | decoded payload length ≠ declared decoded size                 | R-SER-07 (R-COD-08)
T4  | padding position doesn't encode the recorded fill value        | R-SER-05
T5  | packed planar bool pad bit isn't the fill bit                  | R-SER-05 (R-SER-03)
T14 | codec 1 (none), entry length ≠ decoded size                    | R-COD-04
T21 | zstd window size larger than decoded size                      | R-COD-06
T22 | zstd Frame_Content_Size ≠ decoded size                         | R-COD-06
T24 | decode doesn't consume the entry's length exactly               | R-COD-08
T25 | stored bytes are a malformed stream that fails to decode        | R-COD-08
```

(All nine rows opened and quoted at spec/tarn.md:3829–3852.)

So: a commit that illegitimately changes a layer's *codec* or *filter* (both
explicitly named members of the fixed list this bar governs) while the layer
still stores unsuperseded tiles from the prior generation, in a way that
causes a decode failure against the old bytes, **does** trip T24 or T25 —
register rows, with assigned detector "reader," detected at "tile use." Per
§21.1 ("the register enumerates every detectable file-conformance violation
this specification names ... its completeness is normative"), these ARE
file-conformance violations. This directly contradicts hunk 10's unqualified
"the violation is not a file-conformance violation ... and no register row
records it": for this subset of the bar's members, a register row does record
it, and the resulting file is not conforming.

**Contradicting quotation** (unchanged text, same step 4, a few paragraphs
after the hunk's insertion): "...and a decode that fails outright under a
changed codec or filter (T24, T25), no check any actor owes able to see it
(§21.7)" — the "but for" clause preceding it makes T24/T25 the explicit
exception to "no check sees it," which is the opposite of hunk 10's blanket
claim.

### Byte-level test

Checked whether this contradiction moves the emittable-byte set or an
accept/reject verdict. Opened `[R-CNF-05]` ("Conforming writer. A writer MUST
emit only conforming files") and its restatement at spec/tarn.md:1019
("writer violations make the file nonconforming (`[R-CNF-05]`)"). Under
*either* reading of hunk 10's sentence, a writer that changes a fixed
declaration in a way that trips T24/T25 (etc.) was already barred from
emitting that file by `[R-CNF-05]`, because T24/T25 are pre-existing,
unmodified register rows independent of this hunk. A reader/verifier facing
such a file must still reject-tile per T24/T25 regardless of how "this bar"
itself is classified, because T24/T25 are tile-scope obligations that do not
depend on the bar's own classification. So the disputed file (one produced by
a bar-violating, decode-breaking codec change) is nonconforming under both
readings, and the set of bytes a conforming writer may emit, and the
verdicts a conforming reader must reach, do not move. **Not byte-level** —
per this audit's own discriminating test (a register-row violation is barred
by `[R-CNF-05]` regardless of how a separate, contradicting sentence
classifies it), this is a genuine internal self-contradiction in the
document's own prose, and a real overclaim/miscitation, but it does not fork
actual conforming bytes because the authoritative rule (`[R-CNF-05]` +
T24/T25 etc.) is untouched and still controls.

### Check 8 — anaphora around the insertion

- "This bar" (start of inserted sentence) → nearest preceding sentence, "A
  commit MUST NOT change one of these ...". Correct both before and after
  insertion (it's the insertion's own opening reference, resolves to what
  immediately precedes it either way).
- "these" (in "A commit MUST NOT change one of these", *before* the
  insertion point) → the fixed list enumerated in the paragraph above. Not
  affected by the insertion (it's textually prior to the inserted material).
- "the change" (same sentence, before insertion) → "the change [that violates
  the bar]" — self-contained within its own sentence, unaffected.
- "Between them the two lists" (*after* the insertion) → checked whether the
  insertion changed what "the two lists" resolves to. The inserted sentence
  introduces no new "list" ("declaration," "bar," "actor," "commit," "file,"
  "violation," "register row" — no noun that could compete as an antecedent
  for "lists"). Before insertion, "the two lists" = the permitted-changes list
  (paragraph A) and the fixed list (paragraph B), both stated earlier in the
  step. After insertion, same resolution — unaffected. No anaphor drift found.

### NESTED_DASH / BCP14

Inserted sentence: "This bar binds the commit as an actor: the file a
violating commit would produce is conforming, the violation is not a
file-conformance violation (`[R-CNF-02]`), and no register row records it
(§21.7)." No em-dashes at all (one colon, parenthetical citations). No
NESTED_DASH. No BCP-14 keyword in the inserted sentence to check casing on.
The adjacent, only-reflowed "A commit MUST NOT change one of these" retains
correct casing (reflow only moved the line-wrap point, verified against both
diff sides).

## Hunk 11 — the closing paragraph's slab sentence

### The rule it adopts

Before: "a slab declaration is re-established or cleared (`[R-SLB-04]`)."
After: "a slab declaration is declared, changed, re-established or cleared
(`[R-SLB-04]`)." Brings this restatement's verb list into parity with hunk
09's fifth-member verb list.

### Check 2 — citation

`[R-SLB-04]`'s own verbs, quoted in full above, are only "re-establish [the
invariants]" and "clear [the declaration]" — it never itself uses "declared"
or "changed" of a "declaration." Checked whether citing it for all four verbs
is a false pointer: `[R-SLB-04]`'s trigger list ("... or the slab declaration
itself [changing] ... of a layer slab-declared in either the superseded or the
new generation ...") does functionally reach "declared" (new-generation
slab-declared triggers applicability) and "changed" (explicit trigger) as
*conditions* that invoke its obligation, even though its own prose states the
*outcome* using only two verbs. I judge this an acceptable compressed
citation, not a false pointer, since the obligation is genuinely the same
single test regardless of which of the four transitions produced it — verified
identically for hunk 09 above.

### Check 4 / check 6 — parity with the untouched alignment sentence

Read the full sentence this sits in, unchanged parts included:

> "Extents this commit supersedes become slack (`[R-CNT-21]`); a slab
> declaration is declared, changed, re-established or cleared
> (`[R-SLB-04]`), and an aligned layer's stored tiles — every one the new
> state keeps, not only those this commit adds — satisfy its invariant or the
> declaration is cleared (`[R-SLB-01]`, `[R-CNF-05]`)."

The alignment clause carries an explicit parenthetical-by-dash reminder that
the invariant test reaches **already-placed, non-superseded tiles**, not only
ones the commit adds — this is exactly the clarification a *changed*
alignment value needs (a newly-declared A_new must be satisfied by tiles whose
offsets were fixed under the old regime and cannot move unless superseded).
The slab clause, even after hunk 11 added "changed," carries **no analogous
clarification** — it is a bare citation to `[R-SLB-04]`.

Checked whether `[R-SLB-04]`'s own text supplies this coverage implicitly:
yes — §16.2's slab invariant (`[R-SLB-03]`, quoted in full above) is stated
per-*run*, not per-tile ("the run's stored tiles are contiguous and packed in
ordinal order"), so "re-establish the invariants for every such run"
necessarily draws on every tile currently in that run, new or carried-over,
without needing a tile-level "not only those this commit adds" reminder.
Also checked the step 4 opening paragraph's constraint that a tile the commit
does not supersede is carried forward "byte-identical at its disk-ordinal
position ... and nothing else this step permits moves one" — meaning a
"changed" slab run length can only be satisfied for already-placed,
unsuperseded tiles if they happen to already fit the new run partition, or the
writer supersedes (rewrites) them; this mechanism is not stated anywhere
locally, but is not new to hunk 11 either — `[R-SLB-04]` was silent on the
mechanism before this repair too.

**Verdict:** the underlying rule (`[R-SLB-04]`, unmodified) does correctly
reach already-placed tiles for a "changed" slab run length, so this is **not
byte-level** — no implementation gets a different accept/reject verdict from
it. But hunk 11 was the exact opportunity, and the exact place, to give the
slab clause the same explicit "not only those this commit adds" parity the
neighboring alignment clause has, especially since "changed" is the newly
licensed transition that most needs it (an already-established value simply
being *re-affirmed* raises no such question; a *changed* run length does). Its
absence is a real, reportable NEW_AMBIGUITY: a reader who takes this summary
sentence as the operative statement (rather than tracing all the way into
`[R-SLB-04]`'s per-run wording) could plausibly conclude, by the asymmetry with
its neighbor, that a changed slab declaration's invariant need only be
satisfied going forward for newly-stored tiles — the wrong conclusion, but one
the sentence's own asymmetry invites.

### NESTED_DASH / BCP14

Hunk 11's own inserted text ("declared, changed,") has no dashes and no BCP-14
keyword. Checked the full sentence it lands in (quoted above): one em-dash
pair around "— every one the new state keeps, not only those this commit adds
—", not nested inside another dash-delimited clause (the sentence's other
clauses are semicolon/comma-delimited, not dash-delimited). No NESTED_DASH.

## Sweeps run (verbatim, with hit counts, and controls)

All run against `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, normalizing hard-wrap whitespace before matching (per the access-rule warning), with a control phrase run alongside each search that could report a false zero.

1. `grep -n "R-SLB-01"` → 6 hits (2321, 3132, 3316, 3528, 3806, 3807, 4098 — 7 actually, listed). Control: same command against a term I knew was absent from this project's citation style, `R-SLB-99` → 0 hits, confirming grep isn't silently failing.
2. `grep -n "R-SLB-04"` → 2 hits (2369, 3313).
3. `grep -n "R-CNT-16"` → 4 hits (1138, 2332, 3002, 3787).
4. `grep -n "R-CNF-02"` → 9 hits (178, 1068, 1285, 1290, 2703, 2793, 3229, 3907, 3934).
5. `grep -n "^#### 21.7"` → 1 hit (3949).
6. Whitespace-normalized phrase search (python3, normalizing all runs of
   whitespace to a single space before `.find`) for `"declared, re-established or cleared"` (the pre-repair 3-verb phrase) → **0 hits** anywhere in the live document — confirms no stale copy of the un-repaired phrasing survives. Control, same script, searching for `"re-established or cleared"` (the shared suffix, which must be present since the repaired phrase contains it) → **4 hits**, proving the normalization and search were actually functioning (a zero on the full phrase wasn't a broken-search artifact).
7. Same technique for `"declared, changed, re-established or cleared"` (the post-repair 4-verb phrase) → **3 hits**, at lines 3212 (hunk 09's landing), 3312–3313 (hunk 11's landing), and **4785** — a restatement in the "Conforming updater" bullet list (§ near line 4780) that I did not know about in advance and that is *not* one of my three hunks. Read it in context (spec/tarn.md:4779–4787): "... a slab or alignment declaration declared, changed, re-established or cleared — and makes any other change to it as a new layer or a whole-file rewrite (§20.3);" — already matches the 4-verb phrasing. Also found a second restatement at line ~1662, inside a block headed `> **Rationale.**` (spec/tarn.md:1653, confirmed non-normative by its label, and confirmed it explicitly defers to §20.3 as the normative source: "§20.3 states normatively, and governs, what a commit may do..."), also already at 4 verbs. **Neither is a sweep-miss** — both were already updated (presumably by other hunks in this round, out of my charter's scope), so I do not file a finding here, but I record the search since it could have found one.
8. `grep -n "position of every planar channel but the last"` (normalized) → **0 hits** — confirms the pre-repair position-clause wording has no surviving stale copy anywhere.
9. `grep -n "not a file-conformance violation"` → 2 hits: line 895 (a different, pre-existing example — the ignore-lane-bit case cited inside `[R-CNF-02]`'s own text) and line 3229 (hunk 10's own insertion). **No other restatement exists that hunk 10 needed to sweep**, and no stale restatement contradicts it directly other than the "line is drawn" paragraph discussed under Check 4 (which is not a restatement of this exact clause, but an independent, more careful application of the same underlying test to the same bar).
10. `grep -n "no register row records"` → 1 hit (line 3230, hunk 10's own insertion only). Confirms this specific formulation is not restated or cross-checked anywhere else in the document.
11. `grep -n "binds the commit"` → 1 hit (line 3227, hunk 10's own insertion). Confirms novelty of this framing sentence — no sibling instance elsewhere to compare it against for consistency.
12. T-row register lookups: `grep -n "| T2 \|| T3 \|| T4 \|| T5 \|| T14 \|| T21 \|| T22 \|| T24 \|| T25 "` → 9 hits, all in §21 (lines 3829–3852), matching the nine instances "the line is drawn" paragraph names as exceptions. Confirms those rows genuinely exist and are genuinely about codec/filter/fill/padding consequences.
13. `grep -n "R-CNT-16"` cross-checked against its own stated text (line 1136-1138) and its register row L20 (line 3787) — both confirm mutual exclusivity of A and S, consistent with the charter's framing.
14. `sed -n '3195,3325p' tarn.md | grep -n "^>"` → 0 hits — confirms none of the text any of the three hunks touch, nor the surrounding step-4 prose I read for context, sits inside a blockquote (Note/Example/Rationale label check moot here — it's plain normative prose throughout, consistent with `[R-CNF-01]`'s default).

## Derived numbers

- Counted the T-row exception list "the line is drawn" paragraph names:
  "(T3, T14, T21, T22, T4, T5, T2)" = 7, plus "(T24, T25)" = 2, for a total of
  **9** named exception rows. Cross-checked against my own `grep` for those
  nine exact row labels in §21 → 9 matches, one per label, no duplicates and
  none missing. Matches.
- Counted verbs in the closed list's fifth member post-repair: "declared,
  changed, re-established, cleared" = **4**, matching the closing paragraph's
  post-hunk-11 slab sentence (also 4) and the two out-of-scope restatements at
  lines 1662 and 4785 (also 4 each). Internally consistent across all four
  sites I found.
- Counted transitions enumerated in my own transition table above: 5 (declare,
  re-establish, change, clear, switch) against the charter's own list of 5
  ("none to some, some to another some, some to the same some, some to none,
  and a switch") — same count, one-to-one correspondence confirmed.

## Rejected candidates

1. **Suspected**: `[R-SLB-04]`'s use of "re-establish" for a brand-new
   ("declared," none→some) slab declaration is a felicity problem (nothing was
   previously "established" to re-establish). **Closed**: this wording is
   pre-existing in `[R-SLB-04]`'s own untouched text, not something either
   hunk 09 or hunk 11 introduced or could have introduced without rewriting a
   requirement outside my charter; and it does not change the actual
   obligation (the run invariants must hold for the new state regardless of
   which verb names the transition). Not filed.
2. **Suspected**: the "switch from A to S (or S to A) in one commit" transition
   might be silently disallowed somewhere, making the fifth member's implicit
   promise that it's permitted an overclaim. **Closed**: traced it as a
   composition of two already-individually-licensed transitions (clear one
   field, declare the other), checked the "commit MAY make several of these
   changes at once" combination rule and its one stated exception (channel
   list extend+shorten only), and found no rule forbidding this specific
   pairing; `[R-CNT-16]` only constrains the *final* declared state, which the
   composition satisfies. Not filed.
3. **Suspected**: `[R-CNF-02]`'s own three named cases might now be "short by
   one" now that hunk 10 adds a fourth conduct-only case elsewhere. **Closed**:
   `[R-CNF-02]`'s own text explicitly disclaims exhaustiveness ("each is
   declared where it arises rather than enumerated here"), so this is by
   design, not a defect — the actual problem with hunk 10 is not that
   `[R-CNF-02]` is incomplete but that the *new declaration itself* is not
   true for the full scope it claims (filed as the main hunk-10 finding
   instead).
4. **Suspected**: the position clause ("the new state keeps") might mis-handle
   a multi-channel extension combined with a mid-commit rename. **Closed**:
   position (list index) and name are governed by entirely separate clauses
   (position by the fixed list, name by the always-permitted first member),
   and nothing in either clause's wording makes one contingent on the other;
   constructed a concrete rename+extend case and found no interaction.
5. **Suspected**: hunk 10's insertion might have stranded a back-reference
   later than "Between them the two lists" — read forward through the rest of
   step 4 (the tense/empty-layer paragraph, "the line is drawn" paragraph, the
   bounds paragraph, the closing paragraph) looking for any further "it,"
   "this," "that," or "such" whose nearest antecedent could have shifted.
   **Closed**: none found; the next candidate back-references ("The permitted
   changes touch none of that" — "that" resolves to "a stored tile's meaning,"
   stated two sentences earlier in the same paragraph the hunk did not touch)
   are all local to paragraphs the hunk 10 insertion does not sit inside.

## Confidence / what an empty result would have meant

Findings were not empty for these three hunks. Where I concluded "no defect"
(hunk 09's transition table, the position clause, hunk 09's safety-explanation
sentence, hunk 11's citation choice), I did so only after constructing the
specific counterexamples the charter asked for (all four transitions, the
A↔S switch, an extension, a shortening, a shortening+growth) and checking each
against the cited rule's actual text, not just the repaired sentence's own
wording — for exactly the reason check 7 in the charter describes (an analogy
or citation can be right about the thing it names and still wrong about
scope). I did not find an occasion to apply check 7 (explicit analogy
language — "exactly as," "the same way," "on the model," etc.) to any of the
three hunks' own inserted/changed text; none of the three uses such phrasing.
Check 3 (label test) passed trivially for all three — confirmed by grep that
no line in the touched range begins with `>` — this text is plain normative
prose throughout, not inside any Note/Example/Rationale block.
