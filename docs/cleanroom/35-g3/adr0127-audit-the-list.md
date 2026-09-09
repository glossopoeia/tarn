# Audit transcript — hunks 03, 06, 09, 18 ("the fifth member" and its delegated clause)

## Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (multiple ranges,
listed below with line numbers), and my four assigned hunk files:
`hunk-03.diff`, `hunk-06.diff`, `hunk-09.diff`, `hunk-18.diff` under
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r35-audit/case/`.
I did not open `full.diff`, any other `hunk-*.diff`, and did not list the `case/` directory.
I did not open `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`,
`spec/registry.json`, or any git history/diff/log, and did not browse the web.

Ran only `grep`/`rg`/`python3` (local, read-only, no files read besides `tarn.md`) and `sed -n` to
view spec ranges. Wrote no scratch files — all computation was done inline via `python3 - <<'EOF'`
heredocs reading only `tarn.md`, so nothing under
`/private/tmp/.../r35-audit/scratch/the-list/` was created; noting this explicitly since the
charter names that directory for any working file, and I produced none.

**Context contamination disclosure.** Before I did any reading, my context already contained: (a)
`CLAUDE.md`'s pointer to `AGENTS.md` (not read, per the access rule); (b) the user's auto-memory
file `MEMORY.md`, which lists prior-round lessons under titles like "TARN repair prose vs rules",
"TARN closed-list exceptions compose", "TARN permissions, not carve-outs", etc. — these look like
they describe exactly this kind of round; (c) a `gitStatus` block naming five recent commit
subjects, including "Cleanroom round 34: charter", "ADR-0126: decision 1 confirmed", and "one
byte-level flag, new — the closed list's slab and alignment verbs do not reach a changed value".
None of this is the specification and none of it is evidence about the specification's current
text. I have not used any of it to decide what to look for or what verdict to reach; every claim
below is grounded in the hunk files and the spec text quoted. I flag this because the rules require
disclosure of any such material, not because I relied on it.

## Hunk headers vs. body — verification

All four hunks claim a landing line in "current file" terms and a nearest preceding heading. I
verified each by grepping the post-repair text and the heading line directly:

```
grep -n 'or cleared; several of these in one commit'            -> 1666
grep -n 'declared, changed or cleared as this step provides below' -> 3219
grep -n 'satisfied over every run of the new state'              -> 3322
grep -n 'declared, changed or cleared —'                          -> 4808
sed -n '1640p;3148p;4761p' tarn.md ->
  1640: #### 11.1 Geometry and its validity floor
  3148: #### 20.3 The append procedure
  4761: ### Appendix H — Conformance checklists (non-normative)
```

All four headers agree exactly with their bodies and with the claimed heading context. No
discrepancy to report on any of the four hunks.

## The whole of §20.3 step 4, and the steps either side

Read `tarn.md` lines 3148–3340 in full (steps 1–6 of the append procedure, all of step 4's
prose). Key structure of step 4, as it now stands (post-repair):

- Step 4 opens: "A layer that stores a tile **in the generation this commit supersedes** keeps
  its declarations, with these exceptions and no other: its name ... MAY change; an extent MAY
  grow ...; a planar layer's channel list MAY be extended ... or shortened ...; and **a slab or
  alignment declaration MAY be declared, changed or cleared as this step provides below**." (line
  ~3213–3219, hunk-06's site)
- "A commit MAY make several of these changes at once, an extension and a shortening of one
  channel list excepted: ..." (no exception carved out for slab/alignment combinations)
- "Every other declaration is fixed for as long as the layer stores a tile: ... A commit MUST NOT
  change one of these; the change is a new layer, or a whole-file rewrite ..."
- "... Between them the two lists reach every declaration field of §7.4, and where a field is on
  both sides ... the permitted side states the whole of what a commit MAY do to it ..."
- Later: "a slab or alignment declaration governs placement (§16), not a value, its coordinate or
  its padding." (the safety rationale for why this field is permitted to move at all)
- Bounds paragraph, then: "Extents this commit supersedes become slack (`[R-CNT-21]`); **a slab
  declaration declared, changed or kept has its invariants satisfied over every run of the new
  state, the runs this commit adds included, or is cleared (`[R-SLB-03]`, `[R-SLB-04]`,
  `[R-CNF-05]`)**, and an aligned layer's stored tiles — every one the new state keeps, not only
  those this commit adds — satisfy its invariant or the declaration is cleared (`[R-SLB-01]`,
  `[R-CNF-05]`)." (hunk-09's site, immediately followed by step 5)

Step 3 ("Validate what the commit touches, per `[R-WRT-03]`") and step 5 ("Re-emit the directory
per §20.4 ...") were read in full; neither references slab/alignment declarations and neither is
touched by any hunk.

## §16 (Slabs and Alignment) — the rules the closing clause cites

Read §16 in full (lines ~2302–2385).

- **§16.1, `[R-SLB-01]`** (per-tile alignment): "A layer MAY declare alignment A ...: a power of
  two with 512 ≤ A ≤ 2⁶² ... When declared: every stored tile's offset satisfies offset mod A = 0
  ... A verifier MUST check the invariant (violation: reject-layer, §15.3); readers are not
  obligated to." — a per-**tile** invariant.
- **§16.2, `[R-SLB-02]`** (the run partition): "A layer MAY declare a slab run length S ≥ 1 with
  slab alignment A_slab ... (§7.4; mutually exclusive with per-tile alignment, `[R-CNT-16]`). Runs
  partition each contiguous block of disk ordinals independently: for an interleaved layer the
  single block [0, N); for a planar layer each channel block [c·N, (c+1)·N) ... Run r of a block
  starts at ordinal block_start + r·S." — defines "run" purely as a function of a layer's current
  block geometry (N, channel count) and S; it does not itself talk about generations or about a
  run being "added" by a commit — that concept is the *closing clause's* construction, applied to
  R-SLB-02's static definition across two generations.
- **`[R-SLB-03]`** (the per-run invariants): "When declared, for every run: the run's stored tiles
  are contiguous and packed in ordinal order ... and the first stored tile's offset satisfies
  offset mod A_slab = 0 ... A verifier MUST check these invariants (violation: reject-layer,
  §15.3) ..." — explicitly "for every run", matching the closing clause's "over every run of the
  new state".
- **`[R-SLB-04]`** (the writer/updater obligation and its two discharges): "A writer or updater
  whose commit changes the stored-tile set, the run partition, the byte placement of any run, the
  disk ordinal of any tile the new state stores, or the slab declaration itself, of a layer
  slab-declared in either the superseded or the new generation, MUST either **re-establish the
  invariants for every such run** — or **clear the declaration** in the new generation; carrying
  a stale declaration forward is a validity error at layer scope, detected as the invariant
  failures of `[R-SLB-03]` are: by a verifier." — five-item trigger list, two discharges
  (re-establish-per-run / clear).
- **`[R-CNT-16]`**: "Declaring both A ≠ 0 and S ≠ 0 is a validity error at layer scope: the
  per-tile alignment and slab declarations are mutually exclusive (§16)." — confirms the
  brief's premise that A, S/A_slab are exclusive in the *resulting state* (not a same-commit
  simultaneity ban).
- **`[R-CNF-05]`**: "A writer MUST emit only conforming files. Writer conformance is semantic ..."
  — the general conformance backstop, idiomatically paired with a specific rule elsewhere in this
  document (e.g. the untouched alignment sentence right after hunk-09's site already reads
  "(`[R-SLB-01]`, `[R-CNF-05]`)"; similarly `F27`/`F28`/`L48`/`L49` table rows pair a specific rule
  with `(R-CNF-05)`).

## §7.4 — the full field list, to check nothing slab/alignment-related is left unconstrained

Read the layer-record field table (lines 1104–1128). The only three fields belonging to
"slab or alignment": `alignment A` (u64), `slab S` (u64), `slab alignment A_slab` (u64). No
fourth field exists in this group. `A` is governed by the alignment sentence (`[R-SLB-01]`); `S`
and `A_slab` jointly by the slab sentence (`[R-SLB-03]`, `[R-SLB-04]`). Nothing in this three-field
group is left ungoverned by the closing clause.

## Hunk-by-hunk analysis

### Hunk-06 — the fifth member (§20.3 step 4, line 3219)

**Rule the repair adopts:** A slab-or-alignment declaration on a layer that stored a tile in the
superseded generation is permitted, in one commit, to go from none to some ("declared"), from
some to a different some ("changed"), or from some to none ("cleared") — and nothing else is
listed as an exception to the step's opening default that a layer "keeps its declarations."

**Check 5 — transitions.** For the three quantities A, S, A_slab (never independently switching
mutual-exclusivity per `[R-CNT-16]`, so treat "the declaration" as one logical field with states
none / A-mode / S-mode):

| transition | named by |
|---|---|
| none → some (A or S/A_slab) | "declared" |
| some → a different some | "changed" |
| some → the **same** some (no-op value, but possibly re-triggered by other permitted changes, e.g. a channel-list shortening that alters the stored-tile set) | **not** named by declared/changed/cleared — named instead by step 4's own opening default, "keeps its declarations, with these exceptions and no other" — i.e. it is the case where *no* exception is invoked. This is the transition the removed verb "re-established" used to name redundantly (declaring it an *exception* when it is exactly the non-exception default). |
| some → none | "cleared" |
| A-mode → S-mode or S-mode → A-mode in **one** commit (`[R-CNT-16]` forbids only the *resulting* state having both nonzero, not a same-commit switch) | decomposes into "cleared" (old field) + "declared" (new field), both individually licensed, and licensed **together** by "A commit MAY make several of these changes at once, an extension and a shortening of one channel list excepted" — no exception is carved out for this combination, so the switch is reachable without needing a fourth verb |

**Does "as this step provides below" reach the some-to-same case?** Yes: the referenced text
(hunk-09's site) explicitly writes "a slab declaration declared, changed **or kept** has its
invariants satisfied ... or is cleared" — "kept" is the closing clause's own name for the
some-to-same case, and it is *not* one of the member's three verbs, nor does it need to be: the
member enumerates permitted *changes* (exceptions to the default), while the closing clause states
an obligation that attaches regardless of whether the declaration was touched. `[R-SLB-01]`,
`[R-SLB-03]`, `[R-SLB-04]` between them supply that obligation, keyed to whichever of the three
end-states (A-mode / S-mode / none) actually results.

**Was anything the removal left behind still needing "re-established"?** I checked (a) the
delegated clause (hunk-09's site) — it already used "kept", not "re-establish[ed]", for this
disposition (that "kept" wording was already present, unchanged by hunk-09's diff, as a context
line); (b) `[R-SLB-04]` — it uses "re-establish" but as a verb applied to *the invariants*, not to
*the declaration*, a different grammatical object serving a different purpose (an action a
writer/updater performs when a trigger fires, not a disposition of the declaration's value); (c) a
full-document sweep (below) found no other site using "re-establish[ed]" applied to a
declaration. So no, nothing was left needing the removed verb.

**Check 1 (tense/quantifier).** "in the generation this commit supersedes" (the prior generation)
correctly frames which layers this whole step-4 default+exceptions block governs, and is
unchanged by this hunk. The member's own quantifier ("a slab or alignment declaration") is a
per-layer field, singular, matching `[R-SLB-01]`/`[R-SLB-03]`'s per-layer declarations.

**Check 2 (citations).** No bracketed citation appears inside the diff span itself; the governing
citations are downstream at hunk-09's site and were checked there.

**Check 3 (label).** This sentence sits in unlabeled body text under "#### 20.3 The append
procedure", inside the numbered list governed by "An appender MUST, in order:" — normative. Not a
Note/Example/Rationale block, not in a non-normative appendix. It lands, and it is the sentence
`[R-WRT-04]` (the step's own tag) covers.

**Check 4 (contradiction).** No `[R-CNT-16]`-style bar is violated (checked above — the switch
case does not require both fields nonzero simultaneously in the same state). No other MUST in the
passage collides with the narrowed MAY list.

**Check 5 (overclaim).** No completeness word ("every", "only", etc.) appears in the diff span
itself beyond "no other" in the step's *opening* sentence — that "no other" is unchanged by this
hunk and I verified above that it still holds (every transition is reachable by some combination
of default+declared+changed+cleared).

**Check 6 (unconstrained siblings).** Done above via the §7.4 field sweep — A, S, A_slab are the
only three fields in this group, and all three are governed downstream.

**Check 7 (analogy).** N/A directly for this hunk — the member does not itself argue by analogy to
another rule; that comparison belongs to hunk-09.

**Check 8 (anaphora).** The very next sentence, unchanged, reads "A commit MAY make several of
**these** changes at once ..." — "these" resolves to the full step-4 exceptions list (name change,
extent growth, channel-list edit, and now the 3-verb slab/alignment list), which is exactly what
it resolved to before the edit (just one member short by one verb). No stray resolution.

**Verdict:** sound repair; no defect found.

### Hunk-09 — the closing slab clause (§20.3 step 4, line ~3319–3323)

**Rule the repair adopts:** whatever happens to a slab declaration in a commit (newly declared,
changed, or simply kept from the prior generation), the *resulting* state's declaration must have
`[R-SLB-03]`'s invariants satisfied over **every run of the new state** — explicitly including any
run this commit newly adds — or the declaration must be cleared; separately (unchanged by this
hunk) an aligned layer's *every* stored tile the new state keeps, not only newly-added ones, must
satisfy `[R-SLB-01]`'s invariant or have the declaration cleared.

**Check 1 (tense/quantifier — the central change).** Old text: "... re-established over every run
**the new state keeps**, or is cleared". "keeps" strongly suggests runs that were already present
in the superseded generation and persist — this reading would leave runs that are *brand new*
in the new state (e.g. because an extent grew, producing new ordinals beyond the old block end)
without an explicit textual requirement in *this* sentence. New text: "... satisfied over **every
run of the new state**, **the runs this commit adds included**, or is cleared." "of the new state"
is generation-correct (it is a claim about the state a conforming commit must produce, matching
`[R-SLB-04]`'s "in the new generation" framing) and the appositive "the runs this commit adds
included" removes the "keeps"-only reading. This exactly mirrors — and was almost certainly
modeled on — the untouched alignment sentence immediately after it: "an aligned layer's stored
tiles — every one the new state keeps, **not only those this commit adds** — satisfy its
invariant ...". Both sentences now use the identical rhetorical device (state the inclusive
quantifier, then name the newly-added subset explicitly as *included*, not excepted) for their
respective per-run / per-tile invariants.

**Is "the runs this commit adds" a set `[R-SLB-02]` defines?** Not as its own term — `[R-SLB-02]`
defines "run" as a static function of a block's ordinal range and S; it does not discuss two
generations or talk about a run being "added." "The runs this commit adds" is a derived notion (a
run that exists under the new state's partition but did not, as such, exist under the superseded
state's partition — e.g. because extent growth produced new ordinals past the old block end). I
looked for whether this phrase does any independent narrowing work beyond "every run of the new
state" — it does not: "every run of the new state" already is a total, unconditional quantifier
over the resulting state's runs, so "the runs this commit adds included" reads as a
non-restrictive clarifying appositive (closing the same "keeps"-only loophole the old wording
had), not a second, separately-scoped category needing its own definition. This is the correct
fix for the quantifier gap; I did not find an ambiguity in what set it denotes.

**Check 2 (citations).**
- `[R-SLB-03]` — checked above: states the invariants "for every run", the exact quantifier the
  repaired sentence uses. Resolves correctly.
- `[R-SLB-04]` — checked above: supplies the trigger-conditioned writer/updater obligation and its
  two discharges (re-establish-per-run / clear), which the sentence's "satisfied ... or is
  cleared" restates as an outcome rather than an action. I checked whether `[R-SLB-04]`'s
  conditional trigger list ("changes the stored-tile set...") already covers "the runs this
  commit adds" — yes: growing an extent to add new tiles changes "the stored-tile set", one of
  `[R-SLB-04]`'s five listed triggers, so the new phrase makes explicit (for the step-4 reader)
  something `[R-SLB-04]` already required via that trigger; it does not introduce a stronger
  requirement than `[R-SLB-04]` licenses. Resolves correctly.
- `[R-CNF-05]` — general writer-conformance backstop; resolves correctly and matches the
  document's own idiom of pairing a specific rule with `[R-CNF-05]` (seen unchanged one clause
  later, and in table rows F27/F28/L48/L49).

**Check 3 (label).** Unlabeled body text under the same "An appender MUST, in order:" numbered
list, step 4 — normative, and lands.

**Check 4 (contradiction).** Checked whether the antecedent-disposition mismatch the brief flags
(member: 3 dispositions declared/changed/cleared; this clause: "declared, changed **or kept**" =
3 antecedent states, plus "or is cleared" as the alternative outcome, i.e. 4 words total) is a
contradiction. It is not: the member is a permission grant over what may differ between
generations (3 verbs suffice because "kept" is the non-exception default, not an exception); the
closing clause is an obligation over the resulting declaration regardless of how it got there,
and correctly needs to name "kept" explicitly because `[R-SLB-04]`'s obligation can be triggered
(e.g. by a channel-list shortening) even when the slab declaration's own value was never touched.
The two lists serve different jobs and are consistent, not contradictory. ("kept" is unchanged
context in the diff, not new text from this repair.)

**Check 5 (overclaim).** "every run of the new state" is now a genuinely total claim — I checked
it is not an overclaim by confirming `[R-SLB-03]`'s own invariant is likewise stated "for every
run" unconditionally when a slab is declared, so the totality is inherited from the cited rule,
not manufactured.

**Check 6 (siblings).** Covered by the §7.4 sweep above — S and A_slab are the only two fields
this sentence's citations govern together (as "the slab declaration"), and both are covered.

**Check 7 (analogy — the round-of-record failure mode).** The repair's governing verb is
"satisfied ... over every run"; `[R-SLB-03]`'s governing phrase is "for every run: the run's
stored tiles are contiguous ... and the first stored tile's offset satisfies ...". Both range over
**every run** — the same quantifier, the same individuation unit (a run, as `[R-SLB-02]`
partitions it), unlike the historical L44/addressed-tiles defect where "contains" was glossed
against "addressed" (a different individuation). I also compared the slab sentence's device
("every run of the new state, the runs this commit adds included") against the alignment
sentence's device ("every one the new state keeps, not only those this commit adds") word for
word: both use "the new state" as the base quantifier and an appositive to fold in the
commit-added subset, so the analogy between the two sentences holds member-for-member, not just
in spirit.

**Check 8 (anaphora).** This hunk is a replace (deletion + insertion), not a pure insertion mid-
passage, so I checked forward and backward references anyway. Preceding sentence (unchanged):
"Extents this commit supersedes become slack (`[R-CNT-21]`);" — no anaphor into the edited
sentence. Following text (unchanged): the alignment sentence, then step 5 begins "**Re-emit the
directory**..." — no pronoun in either that could have silently re-resolved across this edit.

**Verdict:** sound repair; closes the "keeps"-only quantifier gap correctly and is grounded
correctly in `[R-SLB-01]`/`[R-SLB-03]`/`[R-SLB-04]`/`[R-CNF-05]`.

### Hunk-03 — §11.1's Rationale (line 1666)

**Rule the repair adopts:** none on its own — this block is a **Rationale**, explicitly labeled
"> **Rationale.**" at its start (verified by reading lines 1640–1672 in full). Under `[R-CNF-01]`
("All text in this document is normative except ... any text labeled *Note*, *Example*, or
*Rationale* ...") this whole block carries no normative force regardless of the ">" marker. I
applied the label test, not the marker test, per the explicit instruction in check 3.

**Word-for-word comparison to the member (hunk-06, post-repair).**

- Member: `a slab or alignment declaration MAY be declared, changed or cleared as this step
  provides below.` — comma after "declared", **no** comma before "or cleared".
- Rationale (post-repair): `a slab or alignment declaration may be declared, changed, or cleared;`
  — comma after "declared", **comma before** "or cleared" (Oxford-comma style).

These differ in punctuation. I traced why: pre-repair, the Rationale's context line (unchanged by
the diff) already ended "may be declared, changed," before the deleted "re-established or
cleared" — i.e. the pre-repair 4-item list was "declared, changed, re-established or cleared"
(non-Oxford, no comma before "or cleared" either). Removing the middle word "re-established" left
the pre-existing "changed," comma sitting immediately before "or cleared", which now *reads* as an
Oxford comma for the reduced 3-item list — an artifact of the surgical deletion, not a decision
anyone made about list style. It is a genuine textual mismatch against the charter's explicit
"hold ... word for word, including punctuation" instruction, but:
- it is non-normative (Rationale label, confirmed above), so it cannot fork any implementation's
  bytes or accept/reject verdict — **not byte-level**;
- it does not create a parsing ambiguity (no risk of the comma being read as separating a
  4th item, since "or cleared" unambiguously closes the list either way).

I report it as a minor, non-byte-level finding (A-01 below) because the charter asked for
punctuation-level fidelity specifically on this hunk, but it is not a defect in the sense of
changing what the passage asserts.

**Check 4/8.** The next clause, unchanged, "several of these in one commit, each subject to every
rule the declarations it produces are under" — "these" resolves to the (now 3-item) list either
way; no stray resolution. The paragraph's other sentences (about empty layers being freely
re-declared) are unaffected and still consistent with the member.

**Verdict:** correctly identified as non-normative; content matches the member in substance;
one purely cosmetic punctuation mismatch, not byte-level.

### Hunk-18 — Appendix H's updater entry (line 4808)

**Rule the repair adopts:** none on its own — Appendix H's own heading reads "### Appendix H —
Conformance checklists (**non-normative**)" (verified directly, line 4761), which is the second
of `[R-CNF-01]`'s exemption clauses ("appendices identified as non-normative"), independent of
whether the entry sits in a blockquote. I checked: this entry is plain body text, not inside a
">" block at all — confirming the check-3 instruction that force goes by label, not by marker, in
both directions (a marker-free block can still be non-normative, here by virtue of the appendix
header).

**Word-for-word comparison to the member.** Appendix H (post-repair): `a slab or alignment
declaration declared, changed or cleared —` — comma after "declared", **no** comma before "or
cleared". This matches the normative member's punctuation *exactly*, unlike hunk-03's Rationale.

**Check 4 — other clauses in the same entry, untouched by the hunk.** Read the full "Conforming
updater" bullet (lines 4805–4818). Its other clauses — "its names, a grown extent, a planar
channel list extended at its end or shortened from it (not both in one commit)" and "makes any
other change to it as a new layer or a whole-file rewrite (§20.3)" — still agree with step 4's
current text (name/extent/channel-list rules and the "new layer or whole-file rewrite" fallback
are all unchanged by any of this round's four hunks). The entry correctly cites "§20.3" (twice) as
its authority, consistent with Appendix H's own preamble: "each entry's authority is the
requirement or section cited, never this summary."

**Check 8 (anaphora).** "and makes any other change to **it**" — "it" resolves to "a layer that
stores a tile in the generation its commit supersedes" (this bullet's subject), unaffected by
removing "re-established" from the embedded list.

**NESTED_DASH check.** The entry's dash-delimited clause is "— its names, a grown extent, ...,
a slab or alignment declaration declared, changed or cleared — and makes any other change ...".
One em-dash pair, no second dash pair nested inside it. Not flagged.

**Verdict:** correctly non-normative by its appendix header; content matches the member verbatim,
including punctuation; no defect found.

## Document-wide sweeps

All sweeps were run against the raw file with blockquote markers stripped and all whitespace
(including hard-wrap newlines) collapsed to single spaces, specifically so a phrase spanning a
wrapped line is not missed. Every zero below is backed by a control search proving the method can
find a known-present string.

```
Sweep 1: r'declared, changed'  (bare, unwrapped grep)                    -> 3 lines (1665, 3218, 4807)
         same phrase, whitespace-normalized                              -> matches same 3 sites
Control: r're-emit'  (unwrapped grep, known-common word)                 -> 22 hits — proves grep is not silently broken

Sweep 2 (python, blockquote-stripped + whitespace-normalized):
  r're-?establish\w*'                                    -> 1 hit  (R-SLB-04, "MUST either re-establish
                                                                       the invariants for every such run")
  r'declared,\s*changed,?\s*(?:or\s+)?cleared'            -> 3 hits (11.1 Rationale, 20.3 member, Appendix H)
  r'declared,\s*changed,?\s*re-?establish\w*'             -> 0 hits (control: the same regex machinery just
                                                                       found the 3-hit pattern above and the
                                                                       1-hit R-SLB-04 pattern in the same run,
                                                                       so the zero is not a broken-match zero)

Sweep 3 (python, same normalization):
  r'slab or alignment'   -> 4 hits: 11.1 Rationale; 20.3 member; 20.3 "governs placement" sentence
                              (no verb list there); Appendix H entry. No fifth site.
  r'alignment or slab'   -> 4 hits, all about invariants/gaps/§16, none a restatement of the
                              declared/changed/(re-established)/cleared list.
  r'alignment and slab'  -> 4 hits, all about slack, R-CNT-16 mutual exclusivity, or Appendix
                              G/H summaries of *invariants*, none a restatement of the permitted-
                              changes verb list.

Sweep 4 (grep -n, line-oriented, as a spot check against sweep 1/2 for the same tokens):
  'or cleared; several of these in one commit'                    -> line 1666
  'declared, changed or cleared as this step provides below'      -> line 3219
  'satisfied over every run of the new state'                     -> line 3322
  'declared, changed or cleared —'                                -> line 4808
```

Conclusion: the removed verb "re-established," applied to a *declaration*, appears nowhere left in
the document. The one surviving "re-establish" (R-SLB-04) is applied to *invariants*, a different
object, and is not one of the three repaired sites — it was correctly left alone.

## BCP 14 casing, on every keyword the hunks touch

- Hunk-06's repaired sentence: `MAY` (capitalized) — consistent with the surrounding normative
  list ("MAY grow", "MUST NOT shrink", "MAY be extended").
- Hunk-09's repaired span: no BCP-14 keyword appears in the diff text itself; the obligation is
  carried by the enclosing "An appender MUST, in order: ... 4. Write payloads and indexes ..."
  list header, unchanged.
- Hunk-03 (Rationale): lowercase "may" throughout — correct, since BCP-14 force applies "when, and
  only when, they appear in all capitals" (`[R-CNF-01]`'s neighboring §2.1 text), and this block
  is non-normative prose describing the rule, not stating it.
- Hunk-18 (Appendix H): no BCP-14 keyword in the touched span (a summary list, not a permission
  statement).

No casing defects found in any of the four hunks.

## NESTED_DASH, on every sentence the hunks touched

- Hunk-03's edited sentence uses semicolons only, no em-dashes.
- Hunk-06's edited sentence uses no em-dashes.
- Hunk-09's edited span uses commas and parentheses only, no em-dashes; the single em-dash pair in
  the same normative sentence (the alignment clause, "— every one the new state keeps, not only
  those this commit adds —") is unchanged context, and is not nested inside another dash pair.
- Hunk-18's edited sentence sits inside one em-dash pair ("— its names, ..., a slab or alignment
  declaration declared, changed or cleared — and makes ..."); no second pair nests inside it.

No NESTED_DASH defects found in any of the four hunks.

## Derived numbers

- Counted list items in the member before/after repair: 4 → 3 (declared, changed, re-established,
  cleared → declared, changed, cleared). Matches the charter's description of the edit exactly.
- Counted antecedent-disposition words in the closing clause (hunk-09's untouched context):
  "declared, changed or kept" = 3, plus "or is cleared" as the alternative outcome = 4 words total
  naming dispositions/outcomes. Compared against the member's 3 — confirmed as a deliberate
  difference in job (permission-grant list vs. obligation list), not a numeric inconsistency,
  per the check-4 analysis above.
- Counted §7.4 fields in the "slab or alignment" group: 3 (`A`, `S`, `A_slab`) — confirmed all
  three are governed by the two closing-clause sentences (A by `[R-SLB-01]`; S/A_slab jointly by
  `[R-SLB-03]`/`[R-SLB-04]`). No unconstrained fourth field.
- Sweep counts double-checked: `declared, changed` bare grep gave 3 lines; the python
  whitespace-normalized sweep for the same concept independently gave 3 hits at the same three
  locations — the two methods agree.

## Rejected candidates

1. **Suspected R-SLB-04 restatement needing the same sweep.** Opened R-SLB-04 expecting it might
   be a fourth site still carrying "re-established" applied to the *declaration*. Closed: its
   "re-establish" governs *invariants*, a different noun serving a genuinely different, still-
   valid, unretouched rule (the writer/updater's trigger-conditioned obligation) — not a missed
   sweep site.
2. **Suspected disposition-count mismatch (3 vs. 4) between hunk-06's member and hunk-09's closing
   clause as a genuine contradiction.** Opened this because the charter flags the count
   difference explicitly. Closed after tracing that the member is a permission list (what MAY
   differ between generations) while the closing clause is an obligation list (what invariant
   attaches to the resulting declaration regardless of how it got there); "kept" necessarily
   appears only in the latter, and was already there before this round's repair (unchanged
   context in the diff) — not a new inconsistency introduced by this round.
3. **Suspected "the runs this commit adds" as an undefined term violating check-6.** Opened
   because `[R-SLB-02]` does not literally define a delta between two generations' run sets.
   Closed: the phrase is a non-restrictive appositive under the already-total quantifier "every
   run of the new state" and does no independent narrowing; and it is licensed by `[R-SLB-04]`'s
   existing "changes the stored-tile set" trigger, so it does not overclaim beyond what
   `[R-SLB-04]` already requires.
4. **Suspected A→S / S→A same-commit switch as an unreachable or forbidden transition.** Opened
   because `[R-CNT-16]` mandates mutual exclusivity. Closed: the exclusivity rule constrains only
   the *resulting* state (never both nonzero at once), and a same-commit switch produces a
   resulting state with exactly one nonzero; the switch decomposes into "cleared" + "declared" on
   two different fields, both independently licensed and jointly licensed by "several of these
   changes at once" (which carves out only the channel-list extend/shorten combination, not this
   one).

## Confidence / empty-result note

This audit's findings list is nearly empty (one non-byte-level punctuation nit). What I did to try
to find something real, specifically for this pairing (which the charter flags as the site of
this project's byte-level finding in twelve of the last rounds and the last three audits' byte-
level defects):

- Built the full 5-transition × 3-quantity matrix for hunk-06 and checked each cell against a
  named verb, the step's own default, or the delegated clause — not just the transitions the
  charter listed by name, but the A↔S switch case too.
- Independently verified `[R-SLB-01]`, `[R-SLB-02]`, `[R-SLB-03]`, `[R-SLB-04]`, `[R-CNT-16]`,
  `[R-CNF-05]` by opening and quoting each, rather than trusting the citations' plausibility.
- Ran the "kept"-vs-"changed" quantifier check on the closing clause's own text against
  `[R-SLB-04]`'s actual trigger list, specifically checking whether "the runs this commit adds"
  is licensed by an existing trigger (it is: "changes the stored-tile set") rather than assuming
  it because it reads well.
- Ran the check-7 analogy comparison word-for-word against the untouched sibling (alignment)
  sentence, since that is exactly the shape (one sentence's device modeled on another's) that
  produced this project's widest-convergence historical defect.
- Ran a full-document, wrap-safe, blockquote-aware sweep for the removed verb and for every
  "slab or alignment"/"alignment or slab"/"alignment and slab" occurrence, with controls proving
  each zero was a real zero.
- Checked all three §7.4 fields in this group against the closing clause, not just the ones named
  in the sentence, to rule out a fourth unconstrained quantity.

What I could not check: I have no access to the conformance vectors or any prior round's specific
byte-level counterexample file, so I cannot mechanically construct or run a candidate nonconforming
file against these rules; my check is textual/citation-based only, as the access rule requires.

## Summary

Read the whole of §20.3 step 4 (and steps 1–3, 5, 6 either side), §16 in full (`[R-SLB-01]`
through `[R-SLB-04]`, `[R-SLB-05]`), the §7.4 field table, `[R-CNT-16]`, `[R-CNF-05]`, `[R-CNF-01]`
and its neighboring §2.1 casing rule, and the full text of §11.1 (through its Rationale block) and
the Appendix H "Conforming updater" entry (through Appendix H's own non-normative heading).

Hunk-06 removes "re-established" from the closed list's fifth member. I built the full transition
matrix the charter asks for and found every transition still named: none→some by "declared",
some→different-some by "changed", some→none by "cleared", some→same-some by the step's own
opening default ("keeps its declarations, with these exceptions and no other") together with the
delegated closing clause's explicit "kept," and the A↔S same-commit switch by composing "cleared"
+ "declared" on the two different fields (licensed by the "several of these changes at once"
sentence, which carves out only the channel-list combination). Nothing the removal left behind
still needs the removed verb: `[R-SLB-04]`'s own surviving "re-establish" governs a different
object (invariants, not the declaration) and was correctly left untouched.

Hunk-09 changes the delegated clause's slab half from an action verb over a narrower range
("re-established over every run **the new state keeps**") to a state description over the correct,
inclusive range ("satisfied over every run **of the new state**, the runs this commit adds
included"), grounded correctly in `[R-SLB-03]` (which itself is quantified "for every run"),
`[R-SLB-04]` (whose "changes the stored-tile set" trigger already covers commit-added runs), and
`[R-CNF-05]` (the document's standard general-conformance pairing). It mirrors, word for word in
structure, the untouched sibling alignment sentence beside it. I did not find a contradiction
between the member's 3 permission-verbs and the closing clause's "declared, changed or kept" —
these are different jobs (what MAY differ vs. what invariant attaches regardless), and "kept" was
already present before this round, unchanged.

Hunk-03 (§11.1's Rationale) and hunk-18 (Appendix H's updater entry) both correctly carry the
member's post-repair verb list; both blocks are non-normative (by *Rationale* label, and by
Appendix H's own "(non-normative)" header, respectively — checked by label per `[R-CNF-01]`,
never by the presence or absence of a ">" marker alone). Appendix H's copy matches the member's
punctuation exactly. The Rationale's copy has picked up an extra comma before "or cleared" as a
side effect of deleting the middle list item — a genuine but purely cosmetic mismatch inside
non-normative prose; it cannot fork any implementation's bytes.

A full-document, wrap-safe sweep (with controls proving the searches actually run) found exactly
one surviving "re-establish[ed]" anywhere in the document (`[R-SLB-04]`, applied to invariants,
not to a declaration — correctly untouched) and exactly the three expected sites of the
"declared, changed, cleared" pattern, with no fourth. BCP-14 casing and NESTED_DASH were checked
on every sentence each hunk touches; no defects found in either category.

I found no byte-level defect in any of these four hunks. All eight checks were run against all
four hunks; results are recorded above per check, per hunk, including the passing ones.
