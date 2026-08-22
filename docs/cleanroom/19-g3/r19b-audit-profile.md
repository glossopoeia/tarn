# R19 repair audit — auditor B (hunks 3, 4, 5)

Working transcript. Verbatim record of what was read, grepped, and concluded.

## Access disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` only, plus my three
charter hunk files:
- `.../r19audit2/hunk-03.diff`
- `.../r19audit2/hunk-04.diff`
- `.../r19audit2/hunk-05.diff`

Did NOT read: `full.diff`, any other hunk file, `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`,
`AGENTS.md`, `README.md`, `conformance/`, `spec/registry.json`, git history/log/diff,
the web. Did not list the scratchpad directory. Wrote exactly one file, this one.

Commands run (all against spec/tarn.md, via Bash):

```
sed -n '3770,3900p'                      # §22.3 tail through §24 head (incl. §23.1)
grep -n -i -E "erasur|erase|deletion|deleted|deletes|delete"
sed -n '3255,3285p' ; sed -n '3660,3690p' ; sed -n '2015,2030p'
grep -n "R-PRV-01\|R-PRV-02" ; grep -n "unreachable"
grep -n "^### Appendix\|^## "
sed -n '4152,4290p'                      # Appendix G entire
grep -n "R-CNT-26\|R-WRT-06\|R-WRT-07\|ignore-lane\|ignore lane"
sed -n '795,830p'                        # §6.3 flags + [R-CNT-08] + [R-CNT-26]
sed -n '3150,3250p'                      # §20.5 compaction, [R-WRT-06]/[R-WRT-07]
grep -n "creator" ; sed -n '2845,2900p'  # §20.1 writer tiers
awk 'NR>=4152 && NR<=4285' | grep -n -i "version_minor|flags|compactor|generation|creator|appender|updater"
grep -n "version_minor"
sed -n '3605,3645p'                      # §21.7 no-witness
grep -n "Appendix G\|reproducible-writer\|reproducible writer\|the profile"
sed -n '4286,4400p'                      # Appendix H entire
sed -n '1365,1400p'                      # §10.1 four vehicles
grep -n "shrink\|de-address" ; sed -n '655,670p' ; sed -n '2980,3012p'
grep -n "remov"
grep -n "^#### 20\.\|^#### 9\.3\|^#### 23\."
awk ... blockquote check on 3826-3848 and 4240-4285
```

Hard-wrap discipline: every grep used a short fragment that cannot wrap
(`erasur`, `remov`, `shrink`, `version_minor`, `ignore-lane`, `creator`,
requirement IDs). Multi-word phrases were never grepped directly; where I
needed a phrase I read the passage with `sed`/`awk` instead.

---

## HUNK 3 — §23.1, `a deletion` -> `erasure`

### Landing site (spec/tarn.md 3826-3847, verified all body text, no `>` lines)

```
#### 23.1 Deletion is not erasure

The append-only model (§9.1) means that what a commit removes, it
removes only from *reachability*. A commit removes sample data two
ways — superseding it, and a shrink that de-addresses tiles (§20.3
step 4) — and a dropped ancillary record's extent (§20.4) goes the
same way; no commit removes a layer at all. In each case the bytes remain in the
file as slack (`[R-CNT-21]`), readable by anyone with the bytes
and a hex editor, and recoverable by any tool that scans backward for
an earlier trailer (§9.6). Writers and the tools built on them
MUST NOT represent any commit that makes sample data unreachable as
erasure of it — a shrink reported as erasure misleads exactly as a
supersede so reported does.
`[R-PRV-01]`
```

### The rule this repair asserts, in my words

Nothing about the rule changed. [R-PRV-01]'s MUST NOT is untouched: a writer, or a
tool built on one, may not tell a user that a commit which made sample data
unreachable *erased* it. What changed is the illustrative half-sentence after the
em-dash, which previously named the wrong term as the misleading one. Post-repair
the illustration is a straight instance of the MUST NOT: reporting a shrink as
erasure is as misleading as reporting a supersede as erasure.

### Check 1 — tense and quantifier

The MUST NOT ranges over "any commit that makes sample data unreachable". The
illustration names two members of that set (shrink, supersede), matching the
preceding sentence's "two ways". No generation is at issue: the sentence is about
what a tool *says*, not about which generation stores what. The repair changes no
quantifier — it replaces a noun phrase in an apposition. `so reported` previously
resolved to "reported as a deletion" and now resolves to "reported as erasure",
which is the resolution the governing MUST NOT requires. PASS.

### Check 2 — citations

The changed word carries no citation. Citations in the sentence and its immediate
neighbours, opened anyway because the repair sits inside them:

- `[R-PRV-01]` — the trailing identifier, is the rule; nothing else in the document
  cites it (`grep -n "R-PRV-01"` returns only line 3839). PASS.
- §20.3 step 4 — read at 2980-3012. It does define a shrink that de-addresses
  tiles: "An extent MAY also **shrink** ... a tile the new state does not address
  carries no §14 obligation and its extent becomes slack ... Where a shrink is
  permitted the de-addressed tiles' extents become slack (`[R-CNT-21]`)". PASS.
- §20.4 (3099-3148) — the dropped-record table; a dropped MU=0/PE=0 record's
  "extent becoming slack". PASS.
- `[R-CNT-21]` — read at 655-668: "Slack that holds superseded data is a privacy
  consideration (§23)." PASS.
- §9.6 — cited for backward trailer scan; the sentence's claim is recovery
  tooling scans backward for an earlier trailer, which §22.3 (3780-3786)
  independently restates ("recovery tooling that scans backward can land on one").
  PASS.

### Check 3 — normative placement

Lines 3826-3848 checked line-by-line for a leading `>`: all body. The repaired
clause is in the same sentence as the MUST NOT, not in a Note or Rationale.
The clause itself carries no BCP 14 keyword — it is a gloss — but it is a gloss
on a MUST NOT in normative text, so a reader cannot take it as licence. PASS.

### Check 4 — contradiction in the same passage, including untouched text

Every occurrence of either term in the whole document (`grep -i -E
"erasur|erase|deletion|deleted|deletes|delete"`), with the sense each carries:

| line | text | sense |
|---|---|---|
| 2023 | "an all-0xFF region (erased flash) is invalid too" | hardware, unrelated |
| 3267 | "> **Note.** Compaction is the only true removal: logical deletion supersedes bytes but leaves them in the file as slack" | **deletion = the weak/accurate term** |
| 3673 | "a reader that reports 'too large' as 'corrupt' invites the deletion of intact data" | ordinary English, an operator destroying a file; unrelated context |
| 3826 | heading "Deletion is not erasure" | **fixes the contrast: deletion is the weak term, erasure the strong one** |
| 3837 | the repaired clause | erasure = strong term |
| 3843 | "until something outside this specification deletes it" | filesystem deletion |
| 3844 | "a filesystem-level deletion leaves the bytes recoverable" | filesystem deletion, explicitly *not* erasure |
| 3845 | "A deployment whose obligation is erasure MUST treat that obligation as belonging to its storage layer" | **erasure = strong term** |

The subsection heading and line 3267's Note both make *deletion* the term this
document accepts as accurate for a reachability removal. So the pre-repair
"a shrink reported as a deletion misleads" said the opposite of the heading it sits
under and of the MUST NOT it glosses. The repair removes that collision. I looked
specifically for a sentence written to be true only under the old wording and found
none: the only other sentence in §23.1 that names the strong term is [R-PRV-02]'s
"A deployment whose obligation is erasure ...", which the repair aligns with rather
than collides with. PASS.

`grep -n "remov"` (11 hits) turned up no restatement of [R-PRV-01] elsewhere; the
only near-neighbour is line 3267's Note, which is a `>` block and is consistent.
`grep -n "unreachable"` returns line 3836 alone — no restatement to sweep.

### Check 5 — exhaustive claims

The repaired text contains none. "two ways" and "no commit removes a layer at all"
sit two sentences earlier and are untouched context; "two ways" is true as stated
for sample data (supersede, shrink), with the ancillary-extent case correctly
excluded from the count by "and ... goes the same way".

### Verdict, hunk 3

Clean. No finding. The one-word swap moves the illustration onto the same term the
governing MUST NOT uses and onto the same side of the heading's contrast pair.

---

## HUNKS 4 and 5 — Appendix G, item 8 and the summary paragraph

Appendix G in full read at 4152-4285. Heading: "Appendix G — Reproducible-writer
profile (non-normative)". No `>` lines anywhere in 4240-4285. Intro: "It adds no
requirement to any actor: a writer ignoring it is fully conforming, and conformance
to the profile can be refuted cheaply but confirmed only by reproducing the file."

### Current item 8 (4247-4252), post-repair

```
8. **`version_minor` at the floor** `[R-CNT-26]` states, and
   `flags` = 0. Both are creator's rules, as item 2's identifier is: a
   compactor adopting the profile carries its input's unknown
   ignore-lane bits forward instead, and where it carries any feature
   it does not implement takes §20.5's floor rather than
   `[R-CNT-26]`'s (`[R-WRT-06]`).
```

### Current summary sentence (4278-4280), post-repair

```
writer; `version_minor` at its floor, which `[R-CNT-26]` states as a
SHOULD — item 8's creator's rule, not a compactor's (§20.5); a derived `file_id`, where §9.3 states only advice; NFC-normalized
```

### The model the carve-out was written from — item 2 (4183-4187)

```
   ... This is a creator's rule: a compactor
   adopting the profile takes `[R-WRT-06]`'s fresh draw instead, since
   a derived value is not a draw and re-deriving it on an already-
   compact input would reproduce the input's own `file_id`.
```

Shape of the model: `This is a creator's rule:` + `a compactor adopting the profile
[does X] instead` + `since [rationale]`. Item 8 reproduces the first two limbs and
drops the third. The dropped rationale is not itself a defect.

### The rule hunk 4 asserts, in my words

For an adopter of the profile that is a *creator*, both trailer fields are pinned:
version_minor = [R-CNT-26]'s floor (0 for a file expressible under this text) and
flags = 0. For an adopter that is a *compactor*: flags = the input's unknown
ignore-lane bits carried forward, unconditionally; and version_minor = §20.5's floor
(the input's version_minor) *only where* the output carries a feature the compactor
does not implement, with [R-CNT-26]'s floor governing otherwise.

### The rule hunk 5 asserts, in my words

That the degree of freedom "version_minor at its floor" is closed by item 8 for a
creator and *not* for a compactor — stated flatly, with no condition.

### Check 2 — every citation in the repaired text, opened

- **item 2** (Appendix G, 4177-4196). Claim: "as item 2's identifier is [a
  creator's rule]". Item 2 says verbatim "This is a creator's rule". PASS.
- **`[R-CNT-26]`** (§6.3, 820-824): "A writer SHOULD emit the lowest version_minor
  that defines every feature present in the file — for a file expressible under
  this text, 0 — and an appender the maximum of that floor and the prior trailer's
  minor; a higher minor than needed costs readers nothing (minors never gate) but
  misstates the file's feature floor to tooling." Note the subject: **"A writer"**,
  not "a creator". PASS as a citation for "the floor", **FAIL** as support for
  "creator's rule" — see finding B-02.
- **`[R-WRT-06]`** (§20.5, 3149-3189). Two relevant sentences, verbatim:
  - "The output trailer MUST copy the input's unknown ignore-lane flag bits
    forward, in place of the flags = 0 §6.3 requires of a file created under this
    text (`[R-CNT-08]`)." — supports the flags limb exactly, including the word
    *unknown*. PASS.
  - "Where the output carries any feature the compactor does not implement — by any
    of the four vehicles §10.1 enumerates (`[R-EXT-01]`), a carried ignore-lane bit
    and an unrecognized `tarn.` key in a record it never decoded being the two it is
    likeliest to meet — the output's version_minor SHOULD be at least the input's:
    ... **Otherwise version_minor follows `[R-CNT-26]`'s floor.**" — supports the
    conditional limb of item 8. PASS for hunk 4; **FAIL** for hunk 5, whose note
    cites this very section for an unconditional claim the section's next sentence
    contradicts. See finding B-01.
- **§20.5** in hunk 5's "not a compactor's (§20.5)". Opened above. §20.5's final
  word on the matter is "Otherwise version_minor follows `[R-CNT-26]`'s floor",
  i.e. in the ordinary case it *is* a compactor's rule. **FAIL.** Finding B-01.
- **§20.5** in hunk 4's "takes §20.5's floor". §20.5's bound is "at least the
  input's". Is calling that "§20.5's floor" sound? §21.7 (3624-3626) independently
  names it a floor: "§20.5's two obligations on a compacted file's trailer
  (`[R-WRT-06]`) — the unknown ignore-lane bits it MUST carry forward, and **the
  floor its version_minor SHOULD take**". So the term is the document's own, and
  "takes §20.5's floor" resolves to exactly one value, the input's version_minor.
  PASS. (I had this on my list as a possible new ambiguity — "at least the input's"
  is a bound, not a value — and §21.7 retires it.)
- **§6.3 / `[R-CNT-08]`** (805-818), not cited by the repair but the normative home
  of the flags limb: "a writer creating a file under this text MUST write flags = 0
  ... A compactor, though its output is a new file, carries the input's unknown
  ignore-lane bits into its output trailer rather than writing flags = 0 (§20.5,
  `[R-WRT-06]`)." Exactly the repair's flags limb. PASS.
- **§10.1** (1371-1385), reached from §20.5's parenthetical, which the repair drops:
  "This format grows through exactly four vehicles (`[R-ENC-07]`) ... Nothing else
  extends this format." Dropping the enumeration therefore widens nothing —
  "any feature" and "any feature by one of the four vehicles" have the same extension.
  No finding.

### Check 1 — tense and quantifier

- flags limb: "its input's unknown ignore-lane bits". Generation named correctly —
  the *input* file, not the output; a compactor's output is a new file at
  generation 1, so there is no prior generation of the output to confuse it with.
  Quantifier "unknown ... bits" matches §20.5's "the input's unknown ignore-lane
  flag bits" exactly. PASS.
- version_minor limb: "where it carries any feature it does not implement". §20.5:
  "Where the output carries any feature the compactor does not implement". The
  repair's "it" is the compactor in both slots; a compactor carries features into
  its output, so the two range over the same set. Quantifier "any" matches "any".
  PASS.
- The floor value itself is delegated to §20.5 rather than restated, so the repair
  cannot get its generation wrong. PASS.
- Actor set: does the profile need a third branch for an appender/updater?
  [R-CNT-26] gives an appender a different rule ("the maximum of that floor and the
  prior trailer's minor") and [R-CNT-08] gives an updater a MUST ("An updater MUST
  copy forward unknown ignore-lane bits ... and MUST NOT clear them"). Both would
  collide with a bare "flags = 0 / floor" item 8. But item 4 of the profile is
  "**One generation**, so that the file is the output of a single commit", and §20.1
  (2859-2864) makes creator and compactor the only tiers that produce a generation-1
  whole file. So creator + compactor is the complete adopter set and the two-branch
  treatment is right. No finding. (This is the one place where the repair could have
  undershot and did not.)

### Check 3 — normative placement

Nothing in Appendix G is normative; the heading says so and the intro says "It adds
no requirement to any actor". So neither the pre- nor the post-repair item 8 has
force, and the R-CNF-01 failure mode (a rule stated only in a `>` block) does not
apply — there is no normative twin of item 8 that the repair needed to sweep. I did
check the converse: is the normative layer already correct, so that the repair only
had to bring the profile into line? Yes — [R-CNT-08] and [R-WRT-06] both already
carve the compactor out for flags, and §20.5 already carves it out conditionally for
version_minor. Item 8 was the outlier and the repair moved the outlier. PASS.

### Check 4 — contradiction in the same passage, including untouched text

Everything in Appendix G naming either field or the compactor
(`awk 'NR>=4152 && NR<=4285' | grep -i ...`):

- 4184-4185 (item 2) — "This is a creator's rule: a compactor adopting the profile
  takes `[R-WRT-06]`'s fresh draw instead". Consistent with item 8 in shape.
  **Inconsistent with the summary paragraph after hunk 5** — finding B-03.
- 4215 (item 3) — "byte-identical in type, flags, lengths, payload and extent
  content". This is a *record header* flags field, not the trailer's. Different
  field, no collision. Confirmed by §7.3's record header vs §6.2's trailer layout
  (line 745: trailer offset 12, u32 flags).
- 4229-4230 (item 4) — "**One generation**, so that the file is the output of a
  single commit." Compatible: a compactor's output is generation 1 (§20.5: "It MUST
  mint a fresh file_id for the output ... and generation 1").
- 4247-4252 (item 8) — the repair.
- 4277 (summary) — "a single generation, which §9 nowhere constrains".
- 4279-4280 (summary) — the repair.
- 4269-4271 — "Everything else the profile needs is already mandatory". This is why
  `flags` = 0 does not appear in the summary list: it is [R-CNT-08]'s MUST for a
  creator, not a degree of freedom the profile closes. The summary is correct to omit
  it, and hunk 5 correctly does not add a flags note. No finding.
- Appendix H (4286-4360) read in full: no mention of version_minor, flags, the
  profile, or a compactor's trailer. Nothing to sweep there.

Contradictions found:

1. **Hunk 5 against §20.5 and against hunk 4.** The summary says
   "item 8's creator's rule, not a compactor's (§20.5)" — unconditional. Item 8 says
   the compactor departs only "where it carries any feature it does not implement",
   and §20.5 says "Otherwise version_minor follows `[R-CNT-26]`'s floor". For a
   compactor that implements every feature its output carries — the ordinary case,
   and the only case in which a compactor can proceed at all for an MU = 1 type
   ("A compactor MUST refuse to compact a file carrying any record whose type it does
   not implement with MU = 1") — version_minor at [R-CNT-26]'s floor *is* the
   compactor's rule. The summary states the exception as the rule. Finding B-01.
2. **Hunk 4's topic sentence against its own qualification.** "Both are creator's
   rules" is exact for flags and false-as-stated for version_minor, which
   [R-CNT-26] states over "A writer" and which §20.5 keeps for a compactor except
   in the carved-out case. The sentence retracts it three clauses later, but the
   summary paragraph plainly read the topic sentence and not the retraction — which
   is how B-01 got written. Finding B-02.
3. **Hunk 5's asymmetry with item 2.** The summary now marks exactly one entry as
   creator-only. Two entries away sits "a derived `file_id`, where §9.3 states only
   advice" with no such mark, although item 2 carries the identical carve-out — and
   item 2's is *unconditional*, so it is the stronger of the two. A reader of the
   summary infers that a profile-adopting compactor derives its file_id, which item 2
   forbids. Finding B-03.

I also looked for and did **not** find:
- a MUST elsewhere in Appendix G that item 8's new licence lets an adopter violate —
  Appendix G contains no BCP 14 keywords in normative position at all;
- a sentence in items 1-7, 9, 10 written to be true only under the pre-repair item 8;
- any register row bearing on either field. `grep -n "version_minor"` gives one §21
  row, line 3542: "| version_minor is higher than this text defines | Accepted;
  minors never gate | `[R-CNT-07]` |", i.e. an overstating minor is *conforming*.
  Line 744's field table gives version_minor value domain "any (see §6.3)". Line 3541:
  "| An ignore-lane flag bit (16–31) is set | Ignored; the file is conforming ... |".
  So neither of the two files a disputed reading would produce carries a register-row
  violation — relevant to the byte-level test below.

### Check 5 — exhaustive / completeness claims in the repaired text

- **"Both"** (hunk 4). A closed count over item 8's two halves, asserting the same
  property of each. Falsified for the version_minor half by §20.5's "Otherwise"
  sentence. Finding B-02.
- **"not a compactor's"** (hunk 5). A universal negative. Falsified by the same
  sentence. Finding B-01.
- **"any feature it does not implement"** (hunk 4). Tried to falsify by finding a
  feature vehicle outside §10.1's four; §10.1 says "exactly four vehicles ...
  Nothing else extends this format." Survives. No finding.
- **"its input's unknown ignore-lane bits"** (hunk 4). Tried to falsify by finding a
  *known* ignore-lane bit a compactor might treat differently; under this text no
  flag bits are defined (§6.3: "In this specification's text no flag bits are
  defined"), so the set is all set ignore-lane bits and the phrase is complete.
  Survives. No finding.
- **"creator's rules"** as a term: §20.1's tiers are creator / appender / compactor,
  so "creator" is a defined term and the label is well formed. No finding.

### The appendix's own terms — byte-identity

The charter asks whether any of this leaves an adopter a choice. Working it through:

- Under B-01's misreading, two profile-adopting compactors with identical inputs and
  identical feature coverage emit different version_minor: one follows [R-CNT-26]'s
  floor (0 for an input expressible under this text), the other follows the summary's
  instruction and takes §20.5's floor, the input's minor, which for an input whose
  own writer overstated is nonzero. Bytes at trailer offset 10 (F − 54) differ.
  Both files are conforming — [R-CNT-26] is a SHOULD and §21's row for a high
  version_minor is "Accepted". That is a byte fork **between profile adopters**, and
  it is exactly the failure the profile exists to prevent. It is *not* byte-level in
  the sense this audit's test defines, because Appendix G binds no conforming
  implementation: the set of files a conforming writer may emit is the same under
  both readings. I record it as not byte-level and say why, rather than inflating it.
- A structural observation I considered and am reporting at low weight: even with
  hunk 4 read correctly, item 8's compactor branch makes version_minor a function of
  the *compactor's feature coverage*, not of the input's content. The appendix's own
  technique for a producer-dependent value is to pin the producer — item 1 ("a named
  codec implementation at a named version"), item 9 ("a named JSON writer at a named
  version") — and item 8 neither pins nor acknowledges. What keeps this from being a
  significant defect is item 2: a profile-adopting compactor takes "[R-WRT-06]'s
  fresh draw", i.e. eight random bytes, so compactor output was never byte-
  reproducible under this profile in the first place and item 8 costs nothing it had.
  But the appendix nowhere says that, and hunk 4 enlarges the compactor's presence in
  the profile without saying it. Finding B-04, reported as a shape defect with a
  one-clause repair, not as a wrong statement.

### Verdict, hunks 4 and 5

Hunk 4: substantially correct — it covers both halves, matches item 2's shape, cites
accurately, gets the quantifiers right, and closes a genuine collision (pre-repair
item 8 told a compactor to write flags = 0, against a MUST in [R-CNT-08] and §20.5).
One overclaim in its topic sentence (B-02) and one unstated limit (B-04).

Hunk 5: wrong as written (B-01) and incompletely swept (B-03).

---

## Findings, in order of weight

- **B-01** hunk 5 — the summary's "not a compactor's (§20.5)" states §20.5's
  exception as its rule and contradicts both §20.5's "Otherwise" sentence and item 8's
  own condition.
- **B-02** hunk 4 — "Both are creator's rules" is false for the version_minor half;
  [R-CNT-26] states the floor over "A writer" and §20.5 keeps it for a compactor
  outside the carved-out case. This is the sentence B-01 was written from.
- **B-03** hunk 5 — the sweep marked item 8 creator-only and left item 2's
  unconditional carve-out unmarked two entries away, implying a compactor derives its
  file_id.
- **B-04** hunk 4 — the compactor branch introduces a producer-dependent value into a
  profile whose claim is byte-identity, with neither producer pinning (items 1, 9's
  technique) nor an acknowledgement that compactor output is unreproducible anyway
  (item 2's random file_id).
