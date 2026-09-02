# Audit transcript — §21.7 "What no check detects", hunks 08 (and 09, missing)

Auditor lane: "§21.7's account of what no check detects, and the register's
relationship to the two new requirements."

## 0. Disclosure — what I read, what I ran, what was missing

Read:

- `/private/tmp/.../scratchpad/case-adr0113/hunk-08.diff` (19 lines).
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, in
  these passages: lines 100–110 (`[R-CNF-01]`), 1224–1240 (§9.1,
  `[R-LIF-01]`), 1440–1500 (§9.7, `[R-LIF-08]` + its closing Note), 1590–1625
  (§13-area Rationale that speaks of "three bars"), 2057–2110 (§14.4, §14.5),
  3072–3120 (§20.3 opening + steps 1–4 head), 3120–3275 (§20.3 step 4 in
  full), 3275–3365 (§20.3 steps 5–6 and its Note/Example blocks), 3422–3510
  (§20.5), 3556–3660 (§21 head, §21.1 in full, §21.2 head), 3830–3884 (§21.6
  in full), 3884–3990 (§21.7 in full, §21.8, §21.9 head).
- Whole-file greps as listed in §1 below.

Ran: `grep`, `sed`, `awk`, `wc`, and one `python3` heredoc that reads only
`spec/tarn.md` and computes row/instance counts. No network. No `git`. No
`docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`,
`conformance/`, `spec/registry.json`. I did not open `full.diff` and did not
open any hunk file other than hunk-08. I did not list the case directory.

**Missing charter input.** My charter named two hunk files. `hunk-09.diff`
does not exist:

```
$ test -f ".../case-adr0113/hunk-09.diff" && echo EXISTS || echo MISSING
MISSING
```

`hunk-08.diff`'s own header says `# hunk 8 of 8`, so the set ends at 8 and the
charter's second filename is spurious. I did not go looking for a ninth hunk
elsewhere. Everything below concerns hunk 08 and the passage it lands in.

**Context I did not ask for.** Material was placed in my context before I
began: a project instruction file pointing at another file, and an index of
maintainer memory notes with titles referring to this project's harness and to
a "lineage gate word list". I did not open any of it, and I have not used any
of it. Naming that it appeared, not its contents, per the charter.

**Header check.** hunk-08 says its nearest preceding heading is line 3884,
"21.7 What no check detects". Verified: `grep -n "^#\{1,4\} 21"` puts
`#### 21.7 What no check detects` at line 3884 and `#### 21.8` at 3969. The
changed line is 3953. Header is correct; no mismatch to report.

## 1. Sweeps run, verbatim, with hit counts

All run from the repo root against `spec/tarn.md`. The file is hard-wrapped, so
every search fragment below is short enough not to wrap (`§14 bar`,
`unwitnessed`, `escape`, `supersede`, `history`, `reconstruct`, `prior
generation`, `no witness`).

| Command | Hits |
|---|---|
| `grep -n "^#\{1,4\} 21" spec/tarn.md` | 9 (3564, 3566, 3648, 3702, 3759, 3796, 3830, 3884, 3969, 3976 — 10 lines; §21 + 9 subsections) |
| `grep -n "^#\{1,4\} 14" spec/tarn.md` | 6 |
| `grep -n "^#\{1,4\} 20" spec/tarn.md` | 6 |
| `grep -n "^#\{1,4\} 9" spec/tarn.md` | 8 |
| `grep -n "§14 bar" spec/tarn.md` | 10 (1606, 3139, 3159, 3198, 3237, 3252, 3257, 3262, 3929, 3953) |
| `grep -n "the bar" spec/tarn.md` | 6 (1252, 2608, 2686, 3008, 3065, 3826) — none of them the §21.7 sentence any more, which is the point of the hunk |
| `grep -n "unwitnessed" spec/tarn.md` | 3 (3942, 3953, 3958) |
| `grep -n "no witness" spec/tarn.md` | 3 (2609, 3903, 3948) |
| `grep -n "live state clean\|state clean\|being clean" spec/tarn.md` | 2 (3263, 3953) |
| `grep -n "escape" spec/tarn.md` | 11 (1541, 2466, 2469, 2698, 2744, 3142, 3231, 3823, 3928, 3929, 4146) |
| `grep -n "supersede" spec/tarn.md` | 31 |
| `grep -n "prior generation" spec/tarn.md` | 4 (629, 1260, 3140, 3954) |
| `grep -n "history" spec/tarn.md` | 7 (1486, 3417, 3781, 3906, 3907, 4223, 4233, 4470 — 8 lines) |
| `grep -n "reconstruct" spec/tarn.md` | 4 (1486, 3418, 3906, 3955) |
| `grep -n "§21\.7\|21\.7" spec/tarn.md` | 8 (2520, 2612, 3261, 3478, 3581, 3600, 3794, 3884) |
| `grep -n "conditions" spec/tarn.md` | 12 |
| `grep -n "R-WRT-06\|R-ERR-01\|R-CNF-01\`\]" spec/tarn.md` | 10 |
| `grep -n "R-CNF-01" spec/tarn.md` | 1 (106) |
| `grep -n "All text in this document is normative" spec/tarn.md` | 1 (104) |
| `grep -c "^\| [FLTR][0-9]" spec/tarn.md` (over 3648–3830) | 120 |

## 2. The hunk

```
@@ -3857,7 +3950,7 @@
 a sample within an image of unchanged length alters no declared
 quantity. And a
 commit that supersedes every tile it would have damaged leaves the
-live state clean, so the bar is unwitnessed there for the same
+live state clean, so the §14 bar is unwitnessed there for the same
 reason `[R-LIF-01]` is: it is a property of the prior generation,
 which §9.7 does not reconstruct; §20.5's three obligations on a
```

One word pair inserted: `the bar` → `the §14 bar`. Nothing else.

### The rule the repair adopts, in my words

For an implementation, the repaired sentence makes this true: *when a commit
re-declares a layer and, in the same commit, supersedes every tile whose
stored bytes that re-declaration would have damaged, the resulting file
carries nothing that any conforming reader or verifier can test to discover
that §20.3 step 4's §14 bar was violated.* It names one of §20.3 step 4's
three bars as the bar so escaping detection, and it grounds that on the §14
bar being "a property of the prior generation", which §9.7's walk does not
reconstruct.

It is an epistemic claim (nothing is detectable), not a permission. Whether
the paragraph keeps it that way is the subject of finding C-01.

## 3. The passage in full (spec/tarn.md 3884–3967)

§21.7 is plain paragraph text: no `>` markers, no **Note.**/**Example.**/
**Rationale.** label, not §1, not an appendix. It closes with `[R-ERR-01]` at
line 3967. §20.3 step 4 is a numbered list item indented three spaces, likewise
unmarked, closing with `[R-WRT-04]` at line 3289.

Second paragraph of §21.7, with the lines that matter:

- 3902–3903 "A second set of obligations is omitted from the register because a
  single file exhibits no witness of their violation."
- 3903–3907 `[R-LIF-01]`/`[R-LIF-02]` "are properties of a file's history,
  which §9.7 does not reconstruct, and no field of a file records how many
  commits that history holds"
- 3918–3925 "§20.3 step 4's bar on a declaration change is witnessed only where
  the affected tiles remain stored, and then only for part of what it bars, and
  its two companion bars are witnessed not at all where the change leaves
  untouched everything §14 fixes for a tile the layer stores in the generation
  the commit supersedes — the prior generation's channel declarations are not
  part of the live state, which is all §9.7 walks, so no check can know which
  ordinal a stored tile used to occupy, or which type its channel carried
  before."
- 3925–3929 "Where the change does touch something §14 fixes, the rows below
  reach it on the terms they state there and no better, and a commit that
  supersedes every tile it would have damaged **escapes them exactly as it
  escapes the §14 bar**."
- 3929–3950 the enumeration of which changes are witnessed (element sizes /
  §14-constrained bytes → §21.4 content rows; decoded size → T3, T14; codec →
  T15, T17, T23, T25 or T14, "sometimes"; filter or sample offset → T26's
  terms, i.e. T2's or T4's check; neither caught by a length).
- 3951–3955 **the repaired sentence.**
- 3955–3962 §20.5's three `[R-WRT-06]` obligations.
- 3962–3967 `[R-ENC-06]`.

## 4. Check 3 — normative placement (label test, not marker test)

Test applied: **label**, per `[R-CNF-01]` at line 104–106 — "All text in this
document is normative except: §1 (Introduction); any text labeled *Note*,
*Example*, or *Rationale*; and appendices identified as non-normative."

- The repaired sentence, §21.7 line 3953: no `>` prefix, no label. **Normative.**
  The repair lands with force.
- The rule it is about, the §14 bar, §20.3 step 4 lines 3132–3139: numbered
  list item, no `>`, no label, closes `[R-WRT-04]`. **Normative.** Not a Note.
- The only other place the "three bars" story is told is line 1600–1620, which
  opens `> **Rationale.**` — **non-normative**, and it merely restates. So the
  normative statement is not stranded in a labeled block, and the repair did
  not edit a labeled block while leaving the normative statement saying the old
  thing.
- The §14 bar's definition ("Call this the **§14 bar**.", 3139) is normative;
  `grep -n "§14 bar"` gives 10 hits and exactly one of them (1606) is inside a
  labeled block.

**Check 3 passes.**

## 5. Check 2 — citations in the repaired sentence

| Citation | Where it resolves | Does it say what the sentence claims? |
|---|---|---|
| "the §14 bar" | §20.3 step 4, 3132–3139: "A commit MUST NOT change a layer's declarations in a way that alters, for any tile that layer stores **in the generation this commit supersedes**, what §14 fixes for its stored bytes or how they decode — the set of padding positions (§11.3) and the content `[R-SER-05]` fixes there, the decoded size, the byte offset of any sample within the decoded tile image, or the codec and filter that produced the stored bytes. Call this the **§14 bar**." | **Resolves.** The narrowed subject names a real, defined term with the tense the sentence needs. |
| `[R-LIF-01]` | §9.1, 1224–1232: "Bytes in [0, F) — F being the live trailer's committed file length — are immutable: a writer MUST NOT modify them, and every conforming mutation of a file is either a commit (§9.2) or a whole-file rewrite under a new file_id (compaction, §20)." | **Resolves as an identifier; fails as an analogy.** `[R-LIF-01]` ranges over every committed byte across the whole history of a file_id, and §21.7 itself says so eleven lines earlier ("properties of a file's history"). The repaired sentence glosses the shared reason as "a property of *the prior generation*". See C-02. |
| §9.7 | §9.7 Coverage verification, 1440–1483, `[R-LIF-08]`: "A verifier checking `[R-CNT-02]`'s partition walks the live state only"; closing Note "Nothing here enumerates prior commits." | **Resolves.** §9.7 does not reconstruct anything but the live state. |

Citations checked beyond the sentence, because the clause it is joined to by a
semicolon depends on them:

| Citation | Verdict |
|---|---|
| §20.5 / `[R-WRT-06]` "three obligations on a compacted file's trailer" | **Resolves.** §20.5 3440–3448 "It MUST mint a fresh file_id"; 3463–3466 "The output trailer MUST copy the input's unknown ignore-lane flag bits forward"; 3474 "the output's version_minor SHOULD be at least the input's". Three, and `[R-WRT-06]` is §20.5's identifier (3482). |
| §20.5's "no field counts commits" ground | **Resolves.** 3449–3452: "nothing in the output's trailer records that it is a first committed state — no field counts commits". |
| §14.4 `[R-SER-09]` | **Resolves and closes a candidate.** "Every combination of layout and channel types is defined… A reader MUST NOT reject a layer for its combination of layout and channel types." So a sample-type change can never manufacture a layout/type witness. |
| §21.1's completeness clause | **Resolves.** 3578–3583 and 3597–3601, quoted in §7 below. |
| `[R-CNF-01]` | **Resolves** (line 104–106). |

## 6. Check 1 — tense and quantifier of the repaired sentence itself

- Generation spoken about: two, correctly distinguished. "leaves the **live
  state** clean" = the new generation the commit produces; "a property of the
  **prior generation**" = the generation the commit supersedes. §20.3's bar is
  quantified "for any tile that layer stores **in the generation this commit
  supersedes**" (3133–3134). The repair's tense matches the rule it restates.
- Set ranged over: "**every** tile it would have damaged" — the damaged subset
  of the superseded generation's stored tiles, not every tile of the layer.
  §20.3's own escape-attempt sentence at 3142 says "superseding **every tile of
  a layer** and re-declaring it". The narrower set is the right one for the
  witness claim: what matters is that no damaged tile survives into the live
  state.
- Verb: "supersedes". §20.3 uses this verb two ways inside one step — see C-04.

Check 1 finds no defect in the repair's own tense. The quantifier issue is
C-04's, and the analogy quantifier is C-02's (check 7).

## 7. The charter's register question — does either new obligation owe a row?

§21.1, lines 3578–3583: "Its **completeness is normative** — a *detectable*
file-conformance violation this specification names and the register omits is a
defect in this document, detectability being the gate `[R-CNF-07]` already
applies and §21.7 the account, by class, of what fails it".

§21.1, lines 3597–3601: "The subsections after §21.5 are not part of the
register and carry no rows: neither this completeness clause nor the instance
arithmetic below reaches §21.6's defined non-violations, §21.7's account of
what no check detects, or §21.9's limits."

Applying it to the two companion bars of §20.3 step 4 — the sample-type bar
(3171–3176: "a commit MUST NOT change the declared sample type of any channel
of a layer that stores a tile in the generation this commit supersedes,
whatever the layer's layout and whether or not the element size moves") and the
planar-ordinal bar (3200–3205: "For a **planar** layer, a commit MUST NOT
change the channel declarations in a way that alters the disk ordinal
`[R-GEO-06]` assigns any tile the layer stores in the generation this commit
supersedes"):

- **Ordinal bar.** A violating commit yields a *conforming* file. Nothing in
  the output records the prior ordinal assignment; the tiles sit where the new
  declarations address them and carry wrong content, which is §21.7's first
  paragraph exactly ("this format detects *corruption of structure*, not
  *incorrectness of content*"). Not a detectable file-conformance violation →
  **no row owed.**
- **Sample-type bar, where the change leaves §14 untouched** (`int8`→`uint8`,
  `float32`→`int32`, per 3161–3165). Conforming file, wrong interpretation.
  **No row owed.**
- **Sample-type bar, where the change does touch §14** (`uint8`→`bool` planar,
  P·Bᶜ → ⌈P/8⌉). The file *is* nonconforming — but only because the §14 bar is
  violated too, and that nonconformity is already a registered condition (T3
  decoded payload length, T14 declared entry length, T2/T4 content rows). The
  register does not owe a *second* row for the same file state, and §21.1's
  own specialization clause ("Some rows are strict specializations of others")
  points the same way. **No row owed.**
- **§14 bar itself**: already reached by existing rows where witnessed, which
  is what 3925–3927 says.

So: **no row is owed, the counts do not move, and §21.7 is the right home.**
This much of the change is sound. Recount below confirms nothing needs
adjusting.

## 8. Recount — the arithmetic

Rows, counted mechanically as table lines matching `^\| [FLTR][0-9]`:

```
3648-3701 rows=35     §21.2 states "35 conditions."      (3650)   MATCH
3702-3758 rows=49     §21.3 states "49 conditions."      (3705)   MATCH
3759-3795 rows=26     §21.4 states "26 conditions."      (3765)   MATCH
3796-3829 rows=10     §21.5 states "10 conditions."      (3815)   MATCH
                      ------
sum                     120     §21.8 states "120 conditions"    MATCH
```

Instances, counted by splitting each row's third cell on `;`, a cell reading
`—` counting as one, per §21.1 ("Instances within a cell are separated by
semicolons, and a cell reading — is one instance; the count is therefore
mechanical once the cell is written"):

```
$ python3 (reads spec/tarn.md only)
total instances 275 rows 120
```

§21.8 states "120 conditions over 275 **instances**". **MATCH.** Every row
parsed into exactly six cells; no row was skipped as malformed.

§21.9's table was not counted — §21.1 excludes it from the arithmetic.

**Conclusion: the printed figures are right and the hunks require no
recount.** This is a null result, and it is a real one: the charter's "if a
row is owed the counts are wrong" branch does not fire, because no row is
owed (§7).

## 9. Check 4 — contradiction in the same passage, including untouched text

This is where the passage fails.

**(a) "escapes the §14 bar" versus §20.3's "does not escape this".** Lines
3927–3929, untouched by this hunk:

> "…and a commit that supersedes every tile it would have damaged **escapes
> them exactly as it escapes the §14 bar**."

Against §20.3 step 4, lines 3140–3144:

> "The tense is the prior generation's (§3.1 defines *stored* against a
> generation), so **a commit does not escape this by unstoring in the same
> breath: superseding every tile of a layer and re-declaring it are one
> operation, and this bars it.**"

Same actor, same commit shape, opposite verdict on the same verb. "Escape" is
this document's word for evading a *rule*, not for evading detection —
`grep -n "escape"` shows it used that way at 3142 ("escape this by unstoring")
and at 3231 ("which an empty layer escapes only because that cap is quantified
over addressed tiles"). Nothing in the paragraph glosses "escapes the §14 bar"
as "escapes the §14 bar's witness".

Hunk-08 is what makes this unavoidable. Before the change, line 3953 read "so
the bar is unwitnessed there", and a reader could take 3927–3929's "escapes the
§14 bar" and 3951–3953's "the bar is unwitnessed" as two remarks about
different things. After the change both sentences name **the §14 bar**, about
**the same commit** ("a commit that supersedes every tile it would have
damaged", word for word in both), and assert two different predicates of it:
*escapes* it, and *is unwitnessed* under it. Only the second is true.
See C-01.

**(b) The reason clause proves too much.** The repaired sentence's own
justification, 3953–3955:

> "so the §14 bar is unwitnessed there for the same reason `[R-LIF-01]` is: it
> is a property of the prior generation, which §9.7 does not reconstruct"

Against 3918–3919, eleven lines above, untouched:

> "§20.3 step 4's bar on a declaration change is **witnessed only where the
> affected tiles remain stored**, and then only for part of what it bars"

The §14 bar is a property of the prior generation in *every* case — including
the case where the affected tiles remain stored and T3/T14/T2/T4 do witness it.
So "it is a property of the prior generation" cannot be what makes it
unwitnessed *there*. The discriminator is the clause before the comma — "leaves
the live state clean" — and the appositive names the wrong ground. See C-03.

**(c) What I looked for and did not find.** No carve-out or "is not such a
case" sentence in §21.7 collides with the narrowed subject. No MUST elsewhere
in §21.7 is now permitted to be violated by the repaired sentence — the
sentence grants nothing. §21.6 (read in full, 3830–3883) contains no entry
touching either companion bar, and its two closing paragraphs ("Two conditions
that once sat in this table…", "Two structural cases are **conforming files a
reader nevertheless refuses**…") do not reach declaration changes at all.
§21.1's tiebreaker sentences ("where a row and the rule it cites diverge, **the
rule governs**"; and for §21.6 entries "the rule governs there too") are worth
noting for a different reason: **neither reaches §21.7.** §21.1 explicitly
excludes §21.7 from the completeness clause and states no precedence rule for
it. So the §21.7-versus-§20.3 divergence at (a) has no stated tiebreaker, which
is what makes C-01 byte-level rather than merely untidy.

## 10. Check 5 — exhaustive claims in the repaired sentence

Words promising completeness, and the falsification attempt for each:

- **"every tile it would have damaged"** — a universal over the damaged subset.
  Cannot be falsified from the document: if one damaged tile survives into the
  live state, §20.3 3150–3152 ("Where a change does reach them it makes each
  stored tile it reaches nonconforming") plus T2/T3/T4/T14 give a witness, and
  §21.7 3918–3919 already says so. The universal is doing exactly the work it
  should. **Passes.**
- **"leaves the live state clean"** — an absolute. Tested against §9.7: the
  verifier "walks the live state only", so a clean live state is a certified
  file. Tested against §20.3 3265–3268 for the shrink route: "the de-addressed
  tiles' extents become slack (`[R-CNT-21]`), `[R-CNT-17]` obliges the smaller
  entry_count and so a re-emitted index region, and every surviving stored tile
  is untouched" — slack is unconstrained (§21.6 row for slack), so it does not
  dirty the live state. **Passes.**
- **"the §14 bar"** — the definite article now closes what was open. That is
  the whole content of the hunk, and the closure is what C-01 and C-03 turn on.
- **"for the same reason `[R-LIF-01]` is"** — a claim of identity between two
  grounds. **Fails**; see C-02.
- **"three obligations"** in the adjoining clause — checked against §20.5:
  fresh file_id (MUST, 3440), ignore-lane bits (MUST, 3463), version_minor
  floor (SHOULD, 3474). Exactly three. **Passes.**

## 11. Check 6 — what the structure still leaves unconstrained

The structure the repair governs is not a header or a record; it is **§21.7's
inventory of unwitnessed obligations**, and specifically the slot in it for
**§20.3 step 4**. So: enumerate every normative obligation step 4 carries, and
ask which of them §21.7 accounts for.

| §20.3 step 4 obligation | Line | Witnessed? | Accounted in §21.7? |
|---|---|---|---|
| §14 bar (MUST NOT alter what §14 fixes for a superseded-generation stored tile) | 3132–3139 | only where affected tiles remain stored | **yes**, 3918–3919 and 3951–3955 |
| Sample-type bar (MUST NOT change a channel's declared sample type) | 3171–3176 | no, where §14 untouched | **yes**, 3920–3922 |
| Planar-ordinal bar (MUST NOT move a stored tile's disk ordinal) | 3200–3205 | no | **yes**, 3920–3922 |
| Growth permission and its geometry conditions | 3223–3236 | yes (L44, `[R-ENC-04]`, geometry rows) | n/a — witnessed |
| Shrink permission | 3237–3251 | the §14 bar's terms | partly — see C-04 |
| Slack, entry_count, `[R-SLB-04]`, `[R-SLB-01]` | 3275–3280 | yes (registered rows) | n/a |
| "every other entry byte-identical at its disk-ordinal position" | 3125–3127 | **no** — nothing records the prior entries | **no** |
| "A writer SHOULD instead produce a new file wherever a commit would strand a large share of a layer's stored bytes — **and always where it would re-emit every one of them**" | 3269–3273 | **no** — no field attributes slack to one commit | **no** |

The last of these is the one that bites, because it is the sibling quantity of
exactly the commit the repaired sentence describes. The repaired sentence's
subject is "a commit that supersedes every tile it would have damaged" — a
commit that re-emits every one of a layer's stored tiles. §20.3 3269–3273
directs a writer away from precisely that commit with a SHOULD, and that SHOULD
is as unwitnessed as anything §21.7 lists. §21.7 does account for SHOULD-level
obligations — two clauses later it lists "the floor its version_minor SHOULD
take" among §20.5's three — so the omission is not a policy of the section.
A reader of §21.7 alone comes away believing the supersede-everything commit is
merely undetectable; it is also, by §20.3, the shape a writer SHOULD NOT take.
See C-05.

I considered raising the "byte-identical entry" row too and rejected it: §21.7
accounts for no §20.4 re-emission obligation either, so the section plainly
does not aim at every writer-procedure duty, and the SHOULD at 3269 earns its
place only because it is about *this sentence's own commit*.

## 12. Check 7 — the analogy, verb against verb

The repaired text justifies itself by analogy once, with the marker "for the
same reason … is".

| | Governing verb, verbatim | Ranges over |
|---|---|---|
| The repair, 3953–3955 | "the §14 bar **is unwitnessed** there … **it is a property of the prior generation**, which §9.7 does not reconstruct" | one generation — the one this commit supersedes; and only in the sub-case "there" |
| The cited warrant, `[R-LIF-01]` as §21.7 itself states it at 3903–3907 | "Committed-prefix immutability and the strict growth of `committed_file_length` across the commits of one file_id (`[R-LIF-01]`, `[R-LIF-02]`) **are properties of a file's history**, which §9.7 does not reconstruct, **and no field of a file records how many commits that history holds**" | every commit of one file_id — the whole history |
| `[R-LIF-01]` at its own site, §9.1 1226–1231 | "Bytes in [0, F) … **are immutable**: a writer **MUST NOT modify** them" | every committed byte, unconditionally |

Three mismatches:

1. **"the prior generation" against "a file's history".** One generation
   against all of them. The document's own idiom for the second is fixed:
   `grep -n "reconstruct"` shows "which §9.7 does not reconstruct" attached to
   "a file's history" at 3906 and again at 3418; line 3955 is the only place it
   is attached to "the prior generation".
2. **Unconditional against conditional.** `[R-LIF-01]` is unwitnessed in every
   file, full stop. The §14 bar is unwitnessed only in the sub-case the
   sentence's own first clause carves out; §21.7 says at 3918–3919 that it is
   witnessed elsewhere. "For the same reason" imports an unconditional ground
   into a conditional claim.
3. **A second ground with no counterpart.** `[R-LIF-01]`'s unwitnessedness has
   two stated grounds at 3906–3907, the second being that no field counts
   commits. The §14 bar has no such second ground and does not need one.

Also, strictly, the §14 bar is not "a property of the prior generation" at all:
it is a *relation* between the superseded generation's declarations and the new
ones — §21.7 says so itself at 3922–3925 ("the prior generation's channel
declarations are not part of the live state"). Half of the relation is in the
live state. See C-02.

No other analogy marker appears in the repaired text. ("exactly as" appears
twice in the paragraph, at 3912 and 3947, both outside the hunk; I checked
both — 3912 "exactly as a mis-strided filter is" against T26 at line 3794, and
3947 "exactly as T26 has it" against the same row. T26 reads: "Filter 2 applied
at a stride other than the mandated one, **where the resulting image breaks
§14.5's padding content or `[R-SER-08]`'s bool bytes** (a wrong stride with no
such structural constraint is undetectable, §21.7); the check that detects it
is T2's or T4's". §21.7's gloss at 3945–3948 reproduces that condition word for
word, including its two-sided form. **Both analogies pass.**)

## 13. Check 8 — what the surrounding sentences now mean

hunk-08 deletes and inserts within one sentence; it inserts no new sentence
between two others. Still, it *changes an anaphor*, which is check 8's subject
from the other side. Every back-reference from 3918 to the end of the
subsection:

| Back-reference | Line | Before the change it resolved to | After the change it resolves to | Changed? |
|---|---|---|---|---|
| "its two companion bars" | 3920 | §20.3 step 4's bar on a declaration change | same | no |
| "**them**" in "escapes them" | 3928 | "the rows below" (3926) | same | no |
| "**it** escapes the §14 bar" | 3929 | the commit | same | no |
| "**there**" in "the change is unwitnessed there" | 3942 | a codec change whose stored bytes satisfy both declarations | same | no |
| "**it**" in "where it breaks neither" | 3947 | the resulting image | same | no |
| "**Neither change**" | 3948 | a filter change; a sample-offset move | same | no |
| **"the bar" → "the §14 bar"** | 3953 | nearest preceding "bar": "the §14 bar" at 3929, itself the nearest antecedent since the insertion at 3925–3929 | explicitly the §14 bar | **pinned, not moved** |
| "**there**" in "unwitnessed there" | 3953 | the supersede-everything case named in the same sentence | same | no |
| "**it** is a property of" | 3954 | "the bar" | "the §14 bar" | narrowed with its antecedent |
| "**a second**" (reason) | 3961 | "a reason all three share" (3958) | same | no |
| "**the last two**" | 3961 | ignore-lane bits; version_minor floor | same | no |
| "**them**" in "the rows for the fields that hold them" | 3966–3967 | `[R-ENC-06]`'s fixed field widths | same | no |

So the anaphor work of the hunk is correct as far as it goes: "the bar" at 3953
had drifted to resolve against "the §14 bar" at 3929, and pinning it makes that
explicit rather than accidental. The cost is that pinning it also welds 3953 to
3929, and 3929 is the sentence that contradicts §20.3 (C-01). Running check 8
backwards: the repaired sentence's own back-reference "for the same reason
`[R-LIF-01]` is" reaches 48 lines back, to 3903–3907. A reader will not look
that far, and when they do they find "a file's history", not "the prior
generation" (C-02).

## 14. Findings

### C-01 — §21.7 says a commit "escapes the §14 bar"; §20.3 says it does not (byte-level)

Location: §21.7 lines 3927–3929, against §20.3 step 4 lines 3140–3144;
sharpened by the hunk at 3951–3955.

The repaired sentence and the sentence twenty-four lines above it now share a
subject verbatim — "a commit that supersedes every tile it would have damaged"
— and a named object, "the §14 bar", and say two different things about the
pair: the earlier that the commit **escapes** the bar, the later that the bar
is **unwitnessed**. §20.3 settles which is right and says so in the same verb:
"a commit does not escape this by unstoring in the same breath: superseding
every tile of a layer and re-declaring it are one operation, and this bars it."

§21.1's tiebreakers do not reach here. They govern a row against its rule, and
a §21.6 entry against its rule. §21.7 is excluded from the completeness clause
by name (3597–3601) and no precedence is stated for it, so two normative
sentences stand in the document saying opposite things about the same commit.

**Byte-level: yes.** The disputed file is conforming — §21.7 itself says the
live state is left clean and the bar unwitnessed, so the file exhibits no
register-row condition and `[R-CNF-05]` does not bar it under either reading.
Only the reading of "escapes" moves. Writer A reads §20.3 and refuses: a
re-declaration reaching stored tiles "is a new layer, or a whole-file rewrite
under a fresh file_id (`[R-LIF-01]`, §20.5)" (3157–3159), so A emits a trailer
carrying a **freshly drawn file_id**. Writer B reads §21.7's "escapes the §14
bar" and appends a commit instead, emitting a trailer carrying the **input's
file_id** with a higher `committed_file_length`, over a directory whose layer
record holds the new declarations and payloads that are freshly written tiles.
The two disagree on the 16 bytes of the trailer's file_id field and on whether
the prior generation's bytes remain in the file as committed prefix. Both
outputs are conforming files. The emittable set moves.

Repair: change 3928–3929 to speak of the witness, not the bar — e.g. "…escapes
them, and escapes every check of the §14 bar, though not the bar itself
(§20.3)". Or delete the clause: the repaired sentence at 3951–3955 already
carries the claim, correctly.

### C-02 — the analogy to `[R-LIF-01]` compares two different quantifiers

Location: §21.7 lines 3953–3955, against §21.7 3903–3907 and §9.1 1226–1231.

"for the same reason `[R-LIF-01]` is: it is a property of the prior
generation" against "`[R-LIF-01]`, `[R-LIF-02]` are properties of a file's
history". One generation against every commit of one file_id; a conditional
claim against an unconditional one; and `[R-LIF-01]`'s second stated ground
("no field of a file records how many commits that history holds") has no
counterpart here. Strictly the §14 bar is not a property of the prior
generation but a relation between it and the live state, as 3922–3925 says.

Not byte-level: no reading of this sentence licenses any writer to emit
anything, and it identifies no accept/reject verdict.

Repair: "…for the same reason `[R-LIF-01]` is: what it is quantified over is
the superseded generation, which §9.7 does not walk."

### C-03 — the reason given would make the §14 bar unwitnessed everywhere

Location: §21.7 lines 3953–3955, against §21.7 3918–3919.

"the §14 bar is unwitnessed there … it is a property of the prior generation,
which §9.7 does not reconstruct" states a ground that holds in every case, and
therefore cannot explain a claim restricted to one. Eleven lines above, the
same subsection says the bar is "witnessed only where the affected tiles remain
stored". The clause that actually does the work is the one before the comma —
"leaves the live state clean" — and the appositive displaces it.

Not byte-level: the sentence's verdict is right, only its stated reason is
wrong, and a reader who follows the wrong reason reaches the same verdict about
the same files.

Repair: "…so the §14 bar is unwitnessed there — not because it is quantified
over the prior generation, which is equally true where it *is* witnessed, but
because the live state retains no tile the change damaged."

### C-04 — "supersedes" does not plainly cover the case §20.3 delegates here

Location: §21.7 lines 3951–3953, against §20.3 3120–3123, 3243–3251, 3261–3264.

§20.3's shrink paragraph hands this exact job to §21.7: "§21.7 records the
consequence — that this is precisely where the §14 bar has no witness, the live
state being clean". The case it means is a **shrink**: a commit that damages a
prior-generation stored tile and then drops it out of the addressed set. §21.7
records only "a commit that **supersedes** every tile it would have damaged" —
and step 4 uses "supersedes" at 3122 in a sense that *excludes* de-addressing:
"entries for tiles this commit stores or supersedes written to their new state,
entries for tiles that become unstored written as the sentinel". (Step 4 also
uses it inclusively at 3142, so the word carries both senses inside one step.)
A reader following §20.3's pointer arrives at a sentence about the wrong
operation, or at best an ambiguous one, in the one place the document promises
the shrink case is recorded.

Not byte-level: §20.3's shrink rule is complete on its own terms and bars the
damaging shrink regardless; §21.7 licenses nothing.

Repair: "a commit that leaves no tile it would have damaged in the live state —
whether by superseding it or by dropping it out of the addressed set — leaves
the live state clean, so…".

### C-05 — the account of §20.3 step 4 omits the SHOULD that governs this very commit

Location: §21.7 lines 3918–3922 and 3951–3955, against §20.3 3269–3273.

§21.7 now accounts for three of step 4's obligations. Step 4 carries a fourth
that is equally unwitnessed and is about the repaired sentence's own commit
shape: "A writer SHOULD instead produce a new file wherever a commit would
strand a large share of a layer's stored bytes — and always where it would
re-emit every one of them, which duplicates the layer rather than dropping part
of it." A commit that supersedes every damaged tile of a layer is that commit.
Nothing in a single file attributes its slack to one commit, so the SHOULD has
no witness; and §21.7 does account for SHOULDs — "the floor its version_minor
SHOULD take" appears four lines later. So the omission is not the section's
policy, and the effect is that §21.7's account of the supersede-everything
commit reads as "undetectable" where §20.3 says "undetectable, and a writer
SHOULD NOT".

Verdict PLAUSIBLE rather than CONFIRMED: §21.7 accounts for no §20.4
re-emission obligation either, so an editor may hold that the section aims only
at obligations whose *violation* is the thing omitted from the register.

Not byte-level: naming the SHOULD in §21.7 would not change what a conforming
writer may emit, since the SHOULD is already normative at §20.3.

## 15. Candidates I opened and closed

- **"Neither obligation has a witness in the output alone (§21.7)" (§20.5
  line 3478) against §21.7's "three obligations".** Two against three looked
  like an unswept restatement. Closed: "Neither" scopes to the two obligations
  in its own vicinity — the ignore-lane carry-forward and the version_minor
  floor — and §21.7 confirms that scoping explicitly with "**For the last two**
  there is a second, the output carrying no record of its input's flags or its
  input's minor either". The fresh file_id draw is handled in §20.5's earlier
  paragraph, on its own ground ("no field counts commits", 3450). No defect.
- **Could a sample-type change manufacture a layout/type witness?** §14.4
  `[R-SER-09]`: "Every combination of layout and channel types is defined…
  A reader MUST NOT reject a layer for its combination of layout and channel
  types." No such witness exists. §21.7's qualification survives this.
- **Could a sample-type change on a planar channel that stores nothing be
  witnessed?** §20.3 3187–3190 says the bar reaches it "where it disturbs no
  byte". Nothing in the file records the prior type, entry_count is unchanged,
  no ordinal moves. Unwitnessed. §21.7's claim holds.
- **Could a channel reorder be witnessed through entry_count or the index?**
  §20.3 3122–3127 has entries carried "byte-identical at their disk-ordinal
  position" and renumbered only for a geometry change; a reorder is not one, so
  the entries stay and the tiles are silently re-labelled. `[R-CNT-17]` binds
  entry_count to the addressed count C·N, which a reorder does not change.
  Unwitnessed. §21.7's claim holds.
- **Does either companion bar owe a register row?** §7 above. No. §21.1's
  completeness clause is quantified over *detectable* violations, and the
  companion bars' violations either leave a conforming file or leave a file
  whose nonconformity is already a registered condition.
- **Do the printed counts move?** §8 above. 35+49+26+10 = 120 rows, 275
  instances, against printed 35/49/26/10, 120 and 275. Every figure matches.
- **Does the repair sit in a labeled block?** §4 above. No — §21.7 is unmarked
  normative prose under `[R-ERR-01]`, and so is §20.3 step 4 under
  `[R-WRT-04]`. The one blockquote telling the same story (line 1600) is
  labeled **Rationale.** and merely restates.
- **Does the "three bars" Rationale at 1600–1620 now contradict §21.7?** Read
  in full. It says "The other two bars reach neither a shrink nor a growth" and
  "A layer that stored no tile in the generation the commit supersedes may be
  re-declared freely; a layer the commit itself empties does not qualify" —
  consistent with §20.3 and with §21.7 as repaired, and in any case
  non-normative. No defect.
- **Does T26's row need sweeping?** Line 3794 already carries the parenthetical
  "(a wrong stride with no such structural constraint is undetectable, §21.7)"
  and its own "the check that detects it is T2's or T4's". §21.7 3942–3948
  reproduces both halves. No unswept restatement.

## 16. Per-check verdicts

1. Tense and quantifier — **pass** on the repair's own words (§6); the analogy's
   quantifier fails, reported separately as C-02.
2. Citations resolve — **pass** for "the §14 bar", "§9.7", "`[R-WRT-06]`",
   "§20.5"; `[R-LIF-01]` resolves as an identifier but not as the warrant it is
   invoked as (C-02).
3. Normative placement, label test — **pass** (§4).
4. No contradiction in the same passage — **fail**, C-01 and C-03 (§9).
5. No exhaustive claim it cannot carry — **pass** except "for the same reason"
   (§10, C-02).
6. What is still unconstrained — **fail**, C-05 (§11).
7. Analogy quantifiers — **fail**, C-02; the two "exactly as" analogies outside
   the hunk pass (§12).
8. What the change did to the sentences around it — **pass** as anaphor work,
   but the pinning is what makes C-01 unavoidable (§13).

Charter-specific:

- Claim that neither companion bar is witnessed, and its qualifications:
  **holds**, tested against §14.4, planar/interleaved layouts, empty channels,
  entry_count and ordinal renumbering (§15).
- Register row owed: **no**, for either (§7).
- Counts: **all correct**, recounted (§8).
- Narrowed subject: **the right one for the local run of sentences**, and it
  fixes a drifting anaphor — but it welds the sentence to a neighbour that
  contradicts §20.3 (C-01) and it re-asserts a wrong ground (C-03) and a bad
  analogy (C-02) without noticing either.
