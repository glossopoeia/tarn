# R19 repair audit — hunk-01 (§20.5, compactor trailer)

Auditor scope: hunk-01.diff only. Working transcript, verbatim.

## 0. Access disclosure

Read:
- `/private/tmp/.../r19audit/hunk-01.diff` (my charter's hunk; nothing else in that directory)
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (many ranges, listed below)

Did NOT read: full.diff, other hunk files, the r19audit directory listing, docs/,
PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, spec/registry.json,
git history/log/diff, the web. No breach.

Ran (all against spec/tarn.md only):
- `wc -l spec/tarn.md` → 4348
- `grep -n "^#### 20\.\|^### 20\|^## 20\|^## 21\|^### 21\." spec/tarn.md`
- `sed -n '3099,3270p'` (§20.4 + §20.5 whole)
- `grep -n "R-CNT-08\|R-CNT-26" spec/tarn.md`
- `sed -n '780,840p'` (§6.3 whole, [R-CNT-07] [R-CNT-24] [R-CNT-08] [R-CNT-26])
- `grep -n "^#### 21\." spec/tarn.md`
- `sed -n '3577,3640p'` (§21.7, §21.8, top of §21.9)
- `sed -n '2891,3000p'` and `sed -n '3000,3100p'` (§20.3 whole incl. step 6)
- `grep -n "ignore-lane\|ignore lane" spec/tarn.md` ; `grep -n "version_minor" spec/tarn.md`
- `sed -n '4215,4290p'` (reproducible-writer profile items 8/10 + closing para; top of Appendix H)
- `grep -n "compactor\|Compaction\|compaction" spec/tarn.md`
- `sed -n '4170,4200p'`, `sed -n '2857,2892p'` (§20.1 writer tiers, §20.2)
- `sed -n '/^#### 2.3/,/^#### 2.4/p'` (§2.3 conformance classes, [R-CNF-02]…[R-CNF-11])
- `sed -n '96,134p'` (§2.1, §2.2) ; `sed -n '3270,3350p'` (§21.1)
- `sed -n '3526,3577p'` (§21.6 whole)
- `sed -n '3577,3628p' | grep -n "flag\|minor\|CNT-08\|WRT-06"` → only 2 hits, both the
  version_minor line. **[R-CNT-08] and the word "flag" do not occur in §21.7.**
- `sed -n '1355,1395p'` (§10.1 [R-EXT-01] four vehicles), `sed -n '412,435p'` ([R-ENC-07]),
  `sed -n '2560,2585p'` (§18.3 [R-MTA-06])
- `sed -n '/^#### 10.2/,/^#### 10.4/p'` (§10.2 [R-EXT-02], §10.3 [R-EXT-03])
- `awk 'NR>=3149 && NR<=3190 {...}' | grep QUOTE` → **no line in §20.5's first three
  paragraphs begins with ">"** (blockquote check for check 3)
- `sed -n '528,536p'`, `sed -n '4072,4082p'`, `sed -n '2662,2670p'` (residual
  version_minor / ignore-lane hits, sweep check)

Hard-wrap caution observed: every grep above used a short fragment that cannot wrap
(`version_minor`, `ignore-lane`, `R-CNT-26`, `compactor`) or was a range read, never a
multi-word phrase.

## 1. The repaired text, verbatim (spec/tarn.md 3173–3183)

> The output
> trailer MUST copy the input's unknown ignore-lane flag bits forward,
> in place of the flags = 0 §6.3 requires of a file created under this
> text (`[R-CNT-08]`). Where any such bit is set, the output's
> version_minor SHOULD be at least the input's: a compactor cannot know
> which minor version defined a bit it does not implement, and a lower
> minor states a feature floor the carried bit contradicts, misstating
> it to tooling as `[R-CNT-26]` describes. Where none is set,
> version_minor follows `[R-CNT-26]`, as it does for an appender (§20.3
> step 6). Neither has a witness in the output alone (§21.7).

Text it replaced:

> The output
> trailer copies the input's unknown ignore-lane flag bits forward
> (`[R-CNT-08]`) and carries the greater of `[R-CNT-26]`'s floor and
> the input's version_minor — a compactor cannot know which minor
> version defined an ignore-lane bit it does not implement, so it does
> not lower the floor beneath one.

## 2. The rule the repair adopts, in my words

Of an implementation acting as a compactor (§20.1's third writer tier), it makes true:

(a) **Obligation A, MUST.** Whatever bits of the input trailer's ignore lane (bits
16–31) the compactor does not implement, and which are set, appear set in the output
trailer. It may not write flags = 0 there, notwithstanding §6.3's flags = 0 rule for a
writer creating a file under this text.

(b) **Obligation B, SHOULD, conditional.** *If* at least one such bit was carried, the
output's `version_minor` ≥ the input's `version_minor`. *If* no such bit was carried,
the output's `version_minor` is whatever `[R-CNT-26]` yields — with an appeal to the
appender's step-6 treatment as the parallel.

(c) **Assertion C.** Neither (a) nor (b) is checkable from the output file alone, and
§21.7 is where that is recorded.

Note the generation/tense: both obligations range over *the output the compaction
produces*, read against *the input it consumed*. Neither speaks of a prior generation of
the same file — correct, since a compacted file is generation 1 under a fresh file_id
(same paragraph, `[R-LIF-01]`, `[R-LIF-03]`). Quantifier on (a): "the input's unknown
ignore-lane flag bits" — every such bit, universally. Quantifier on (b)'s guard: "any
such bit is set" / "none is set" — existential and its negation, over the same set. Both
tenses and quantifiers are internally consistent; see check 1 below for the one place
the quantifier is narrower than the rationale that motivates it.

## 3. Check 1 — tense and quantifier

**Generation.** Correct throughout: input vs output, not superseded vs new state of one
file. Cross-checked against §20.5's own framing three sentences earlier — "It MUST mint a
fresh file_id for the output ... and generation 1" — and against §20.1's "**compactor** —
rewrites a file whole under a new identity". No tense slip.

**Set for obligation A.** "the input's unknown ignore-lane flag bits" — universal over
unknown-and-set bits. Matches §6.3's own wording for the compactor ("carries the input's
unknown ignore-lane bits into its output trailer") and §20.3 step 6's for the appender
("unknown ignore-lane flag bits copied forward"). Same quantifier in all three. PASS.

Scope note (not a finding, and unchanged from the pre-repair text): nothing here or in
§6.3 says what a compactor does with an ignore-lane bit it *does* implement. Both the old
and new §20.5 text, and §6.3, speak only of *unknown* bits. The repair neither widened nor
narrowed this, so I do not charge it to the repair.

**Set for obligation B.** The guard partitions on the same set as (a): "any such bit is
set" vs "where none is set". That partition *is* exhaustive over that set. But the set is
narrower than the reason the repair gives for the rule — see finding A-01.

## 4. Check 2 — every citation opened

| Citation in the repaired text | Verdict |
|---|---|
| `§6.3` "requires ... flags = 0 ... of a file created under this text" | **PASS.** §6.3, [R-CNT-08], line 808: "a writer creating a file under this text MUST write flags = 0". The repair's "of a file created under this text" is the same rule restated from the file's side; nothing turns on the recasting. |
| §6.3's carve-out for a compactor | **PASS.** §6.3 lines 811–814: "A compactor, though its output is a new file, carries the input's unknown ignore-lane bits into its output trailer rather than writing flags = 0 (§20.5, `[R-WRT-06]`)." The carve-out the repair asserts is the carve-out §6.3 states — same actor, same bits, same "rather than writing flags = 0". Force differs; see A-05. |
| `[R-CNT-08]` (cited for obligation A) | **PARTIAL.** [R-CNT-08] contains the compactor sentence, but as a bare declarative that defers to §20.5/[R-WRT-06]. The only MUST [R-CNT-08] states on this topic binds an *updater* over "the file it modifies", not a compactor over a new output. See A-05. |
| `[R-CNT-26]` (cited for "misstating it to tooling as [R-CNT-26] describes") | **FAIL.** See A-03. R-CNT-26 line 823–824: "a higher minor than needed costs readers nothing (minors never gate) but misstates the file's feature floor to tooling." The misstatement R-CNT-26 describes is the one a **higher** minor causes. The repair attributes it to a **lower** minor. |
| `[R-CNT-26]` (cited for the else-branch rule) | **AMBIGUOUS.** R-CNT-26 states two different rules for two actors. See A-02. |
| `§20.3 step 6` | **PASS as a locator, FAILS as a parallel.** Line 3024–3026 is indeed the appender's commit step and does read "version_minor per `[R-CNT-26]`". But it sits under "An appender MUST, in order:" (line 2903), and the R-CNT-26 clause it invokes for an appender is "the maximum of that floor and the prior trailer's minor" — a different rule and a different force from what a compactor gets. See A-02. |
| `§21.7` ("Neither has a witness in the output alone") | **FAIL for one of the two.** See A-04. §21.7 records the version_minor floor and nothing about the flag bits. |

Also opened, though not cited in the repaired sentence, because the repair's rule depends
on them: §2.1 [R-CNF-01] (blockquote rule; "every SHOULD states the consequence of
deviation"), §2.3 [R-CNF-02] (conduct-vs-bytes, and the two named conduct cases),
§2.3 [R-CNF-06], §20.1, §20.4's table, §21.1 (register governance and §21.7's role),
§21.6 (the two rows that make both disputed outputs conforming files), §10.1 [R-EXT-01]
(the four growth vehicles), §18.3 [R-MTA-06].

## 5. Check 3 — does the repair sit in normative text?

Yes. The awk/grep pass over lines 3149–3190 found no line beginning with ">". Both
obligations are plain paragraph prose inside the paragraph whose requirement identifier is
`[R-WRT-06]` (line 3186). §6.3's counterpart text (lines 807–818) is likewise unquoted
normative prose. §21.7's text (3577–3628) is unquoted normative prose under `[R-ERR-01]`.
Neither obligation lives only in a Note/Rationale/Example. PASS.

Distinctive-terms grep for the rule itself (not the requirement id), short fragments so
the hard wrap cannot hide a hit:

```
$ grep -n "ignore-lane\|ignore lane" spec/tarn.md
153, 424, 745, 807, 809, 813, 815, 1378, 2574, 3025, 3174, 3538, 3999, 4078
$ grep -n "version_minor" spec/tarn.md
532, 744, 793, 798, 820, 3026, 3177, 3181, 3539, 3621, 3998, 4242, 4270
```

Every hit read. The statements of obligation A: 807–818 (§6.3), 3025 (§20.3 step 6),
3174 (§20.5, the repair), 3538 (§21.6 row — the reader-side non-violation), 1378/424
(§10.1/§4.3 growth-vehicle lists), 2574 (§18.3's parallel), 745/3999/4078 (field tables).
The statements of obligation B: 820–824 (R-CNT-26), 3026 (§20.3 step 6), 3177/3181 (the
repair), 3539 (§21.6 row), 3621 (§21.7), 4242/4270 (Appendix G's reproducible profile,
which twice calls R-CNT-26 a SHOULD). No restatement of the *compactor's* version_minor
rule survives anywhere outside §20.5 and §21.7 — so the repair did not leave an old
compactor rule standing elsewhere. That part of the sweep is clean.

## 6. Check 4 — contradiction inside the passage, including untouched text

Read the whole of §20.5 (3149–3266) and the whole of §20.4 (3099–3148) either side.

Looked for and did **not** find:
- A carve-out the new MUST collides with. §20.5's opening "Given a conforming input the
  output is a conforming file" survives: an output carrying a set ignore-lane bit is a
  conforming file, §21.6 row "An ignore-lane flag bit (16–31) is set | Ignored; the file
  is conforming". No collision.
- A MUST the SHOULD now lets an actor violate. The only other version_minor rule is
  R-CNT-26, itself a SHOULD (Appendix G, line 4270: "`version_minor` at its floor, which
  `[R-CNT-26]` states as a SHOULD"). The SHOULD/SHOULD pairing is consistent.
- A sentence written to be true only under the old wording. §21.7's entry still reads
  "§20.5's floor on a compacted file's version_minor (`[R-WRT-06]`) is unwitnessed ... the
  output carrying no record of its input's minor". Post-repair the floor exists only in
  one branch, but §21.7 does not assert unconditionality, and the reason it gives still
  holds in the branch where the floor bites: the carried bit is in the output, but the
  *input's minor* is not, and the bit does not name the minor that defined it (a compactor
  that does not implement the bit cannot map it to a minor, and neither can a verifier
  under this text — §6.3: "In this specification's text no flag bits are defined"). So the
  §21.7 reason for obligation B holds. Not a finding.
- §20.5's "A compactor satisfies every writer requirement for the bytes it produces
  (`[R-CNF-06]`)" against the flags = 0 writer requirement: handled, the repair's "in place
  of the flags = 0 §6.3 requires" is precisely the exemption, and §6.3 states it.

The one contradiction-shaped thing I did find is inside the repaired sentence itself, not
around it: the else-branch, read through its own "as it does for an appender" parallel,
restores the pre-repair unconditional rule and so contradicts the branch structure the
repair just built. That is A-02, filed as NEW_AMBIGUITY since which of the two readings a
reader takes is what decides whether there is a contradiction.

## 7. Check 5 — exhaustive claims

Words promising completeness in the repaired text:
- **"the input's unknown ignore-lane flag bits"** (universal over that set) — carries.
- **"Where any such bit is set" / "Where none is set"** — a true dichotomy over that set;
  exhaustive as a partition. Carries *as a partition*. Does not carry as a partition of
  the problem: see A-01.
- **"Neither has a witness in the output alone (§21.7)"** — "Neither" is a count of two
  and a claim about both. Falsified for one half: §21.7 records one. See A-04.
- **"a compactor cannot know which minor version defined a bit it does not implement"** —
  true, and true for more than bits (A-01).

## 8. Findings

### A-01 — UNDERSHOT (byte-level). The input-minor floor is scoped to one of [R-EXT-01]'s four growth vehicles

The repair's own reason is: *a compactor cannot know which minor version defined a
[feature] it does not implement, and a lower minor states a feature floor the carried
[feature] contradicts.* The repair applies that reason only to unknown ignore-lane flag
bits. But §10.1 [R-EXT-01] says the format grows through **four** vehicles, and lists
ignore-lane flag bits as the third:

> This format grows through exactly four vehicles (`[R-ENC-07]`) ... 1. **New record
> types** (§7.3) ... 2. **New values in the ranges this specification reserves** (§10.2);
> 3. **New ignore-lane flag bits** in the trailer (§6.3); 4. **New standardized
> user-metadata keys** (§18.4).

Vehicle 4 survives compaction as a **conforming** file the compactor carries forward
blind, and §18.3 says so in terms that equate it with the flag-bit case:

> A file carrying an unrecognized `tarn.` key is **conforming** — later minor versions
> register keys, exactly as they define ignore-lane flag bits (§6.3), and this text's
> readers skip both harmlessly. `[R-MTA-06]`

The compactor must carry that record: §20.4 — "No commit therefore removes a layer record,
or a user-metadata record at either scope. Both registered types carry PE = 1, so neither
can be dropped" — and the table's MU = 0, PE = 1 row, "Retain byte-identical, extent
content unmodified". And it cannot inspect the key: §20.5, "its verification depth is
`[R-WRT-09]`'s and reaches no decoded content", and [R-WRT-09]'s enumeration at 3256–3262
reaches the open, layer records, the index chain and extent checksums — never a metadata
document.

So: input written under minor 2, carrying `tarn.somekeyregisteredin2`, version_minor = 2,
no ignore-lane bit set. The repair routes this to "Where none is set, version_minor follows
`[R-CNT-26]`". R-CNT-26's writer clause is "the lowest version_minor that defines every
feature present in the file — for a file expressible under this text, 0". This file is not
expressible under this text, so the "0" shortcut does not apply, and the true floor is 2 —
which the compactor cannot compute, since it does not recognise the key and nothing in the
file names the minor that registered it. The pre-repair text answered this exactly:
"carries the greater of `[R-CNT-26]`'s floor and the input's version_minor". The repair
withdrew that proxy in the one branch where it was still doing work.

I checked whether the other two vehicles also survive, and they mostly do not, which is
why I rest this on vehicle 4: a reserved-range record type or a reserved-range enum value
in the input fires a register row (§21.6: "a *reserved*-range type is read the same way,
but emitting one is a violation (F35, L25)"), [R-WRT-09]'s open/§19.3 checks meet it, and
§20.5's "MUST refuse to compact when any check `[R-WRT-09]` obliges fails" then bars the
compaction. Vehicle 4 is the one that reaches the output.

**Byte-level: yes.** Implementation A applies the else-branch literally and writes
`version_minor = 0` at F − 54; implementation B (or any implementation of the pre-repair
text) writes 2. Both output files are conforming — §21.6, "version_minor is higher than
this text defines | Accepted; minors never gate", and [R-CNT-07] forbids rejecting on
minor — so [R-CNF-05] bars neither, and the emittable set genuinely moves rather than
being clipped by a register row. The disagreement is a real two-byte disagreement about a
field every TARN file has.

**Repair:** restore the proxy in the general case, e.g. "Where the output carries any
feature the compactor does not implement — a carried ignore-lane bit, an unrecognized
`tarn.` key (§18.3) — the output's version_minor SHOULD be at least the input's"; or state
the floor unconditionally as the old text did and let the rationale name the flag bit as
the leading example. Resolving A-02 in favour of the appender-parity reading would also
cure this, at the cost of making the partition vacuous.

### A-02 — NEW_AMBIGUITY (byte-level). The else-branch does not decide the question

> Where none is set, version_minor follows `[R-CNT-26]`, as it does for an appender (§20.3
> step 6).

[R-CNT-26] states two rules, for two actors, that give different answers:

> A writer SHOULD emit the lowest version_minor that defines every feature present in the
> file — for a file expressible under this text, 0 — and an appender the maximum of that
> floor and the prior trailer's minor ... `[R-CNT-26]`

A compactor is a writer (§20.1 lists it as a writer tier; §2.3's writer class binds it)
but is not an appender, and its output has no "prior trailer" — it is generation 1 under a
fresh file_id, as this very paragraph insists. Two readings:

- **Reading 1** (writer clause): version_minor = 0 for an output expressible under this
  text. The trailing "as it does for an appender" is then merely noting that §20.3 step 6
  also defers to R-CNT-26.
- **Reading 2** (the parallel taken as substantive, which is the natural reading of "as it
  does for an appender"): the compactor does what an appender does under R-CNT-26 —
  max(floor, input's minor). This is the pre-repair rule, restored in the branch the
  repair created to *exclude* it, which makes the partition vacuous and, worse, inverts
  the strengths: the no-bit branch (nothing at stake) would bind harder than the bit-set
  branch, which is only a SHOULD.

The force is under-determined too. §20.3 step 6 sits under "An appender MUST, in order:"
(line 2903), so for an appender "version_minor per `[R-CNT-26]`" is carried by an enclosing
MUST — while Appendix G twice calls R-CNT-26 a SHOULD (lines 4242, 4270). Offering step 6
as the parallel therefore imports an unresolved MUST/SHOULD tension into a branch that
carries no keyword of its own and whose sibling is explicitly a SHOULD. A reader cannot
tell whether the else-branch is a MUST, a SHOULD, or a pointer.

**Byte-level: yes**, same field and same two implementations as A-01: compacting an input
with version_minor = 3 and no unknown ignore-lane bits, reading 1 writes 0 and reading 2
writes 3. Both outputs are conforming files (§21.6, [R-CNT-07]), so no register row clips
either and the set moves.

**Repair:** say the rule instead of pointing at an actor it does not apply to — "Where
none is set, the output's version_minor SHOULD be `[R-CNT-26]`'s floor for the output's own
content" — and drop "as it does for an appender (§20.3 step 6)", or keep the pointer only
if step 6's clause is the one intended, in which case A-01 is cured and the partition
should go.

### A-03 — CITATION (not byte-level). [R-CNT-26] describes the opposite deviation

> ... a lower minor states a feature floor the carried bit contradicts, misstating it to
> tooling as `[R-CNT-26]` describes.

[R-CNT-26]'s consequence clause, in full:

> a higher minor than needed costs readers nothing (minors never gate) but misstates the
> file's feature floor to tooling. `[R-CNT-26]`

R-CNT-26 states the misstatement for a **higher** minor, and pairs it with "costs readers
nothing" — a deliberately low-stakes framing. The repair claims it for a **lower** minor,
where the harm is the opposite in kind: tooling reading an understated floor concludes it
needs no support it in fact needs. R-CNT-26 nowhere describes that. The borrowed phrase
"misstates the file's feature floor to tooling" is R-CNT-26's; the deviation it is attached
to is not. This is the citation that reads as verified and is not: an implementer following
the pointer finds only a sentence about too-high minors and may read §20.5's SHOULD
backwards.

It matters more than a stray cite because §2.1's phrasing discipline makes the consequence
clause load-bearing — "every SHOULD states the consequence of deviation" — so this SHOULD's
consequence is required to be stated correctly here, not borrowed from a rule that states a
different one.

**Byte-level: no.** The SHOULD's own text ("SHOULD be at least the input's") is unambiguous
about direction; only the justification is mis-sourced. No file changes.

**Repair:** state the consequence in §20.5's own voice — "and a lower minor understates the
file's feature floor to tooling, which is the harm `[R-CNT-26]`'s floor exists to prevent" —
rather than attributing the description to R-CNT-26.

### A-04 — CITATION (not byte-level). §21.7 records one of the two, not "neither"

> Neither has a witness in the output alone (§21.7).

§21.7 in full contains exactly one clause on this subject:

> §20.5's floor on a compacted file's version_minor (`[R-WRT-06]`) is unwitnessed for that
> same reason, the output carrying no record of its input's minor

`grep -n "flag\|minor\|CNT-08\|WRT-06"` over lines 3577–3628 returns only that clause's two
lines. §21.7 says nothing about the ignore-lane carry-forward, and the reason it does give
— "the output carrying no record of its input's minor" — is a reason about the minor and
does not extend to the flags field.

Nor is the ignore-lane obligation covered elsewhere as a recognised no-witness case. §21.1
makes §21.7 "the account, by class, of what fails" the detectability gate for
file-conformance violations, and §2.3 [R-CNF-02] makes the *other* home — conduct rules —
an explicitly enumerated pair:

> A writer obligation whose violation this specification expressly declares not to be a
> file-conformance violation binds the actor in the same way; §6.3's flags = 0 against a
> set ignore-lane bit and §6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad are
> the cases this text states, and each is declared where it arises rather than enumerated
> here. `[R-CNF-02]`

A compactor that clears a bit it was obliged to carry emits flags = 0 — a plainly
conforming file, so no register row fires and nothing is left for a verifier to check. That
is a real no-witness obligation, and neither §21.7 nor [R-CNF-02]'s named pair records it.
The repair asserts a coverage the document does not have.

(I considered charging the repair with *creating* a third [R-CNF-02] conduct case by
turning a bare declarative into a MUST, and decided not to: §6.3's adjacent "An updater
MUST copy forward unknown ignore-lane bits ... and MUST NOT clear them" already was such a
case before this round, so the strain on [R-CNF-02]'s "are the cases this text states" is
pre-existing and not this repair's doing. Noted here rather than filed.)

**Byte-level: no.** It changes what the document claims about its own completeness, not
which bytes anyone may emit.

**Repair:** either add the carry-forward to §21.7 with its own reason (the output carrying
no record of its input's flags), or narrow the §20.5 sentence to the obligation §21.7
actually records — "The floor has no witness in the output alone (§21.7)" — and, if the
carry-forward is meant as a conduct rule, say so where it arises as [R-CNF-02] instructs.

### A-05 — LOCAL_CONTRADICTION / force (not byte-level). §6.3 states obligation A without a keyword and points back at §20.5, which points at §6.3

§20.5 (repaired): "The output trailer **MUST** copy the input's unknown ignore-lane flag
bits forward ... (`[R-CNT-08]`)."

§6.3, inside [R-CNT-08]: "A compactor, though its output is a new file, **carries** the
input's unknown ignore-lane bits into its output trailer rather than writing flags = 0
(§20.5, `[R-WRT-06]`)."

The two passages defer to each other: §20.5's MUST cites [R-CNT-08] as its authority, and
[R-CNT-08] cites §20.5/[R-WRT-06] as its authority, stating the rule itself with a bare
declarative. The next sentence of the same requirement uses MUST twice for the updater —
"An updater MUST copy forward unknown ignore-lane bits of the file it modifies and MUST NOT
clear them" — so the contrast in force is legible on the page as deliberate, and nothing
explains it.

The rule does have force: §20.5's sentence is normative prose inside [R-WRT-06]'s paragraph
and says MUST. So this is not a "repair with no force" failure. But an implementer auditing
by requirement identifier — which Appendix H directs ("each entry's authority is the
requirement or section cited") — is told by §20.5 that this MUST is [R-CNT-08]'s, opens
[R-CNT-08], and finds no MUST binding a compactor there. Given that these two passages
have pointed at each other before, the loop is worth closing rather than tightening.

**Byte-level: no.** Under either reading the compactor is bound by §20.5's MUST, and the
output with the bits cleared is a conforming file in both cases, so nothing an actor may
emit moves.

**Repair:** give §6.3's compactor sentence the same keyword as its updater neighbour ("A
compactor ... MUST carry the input's unknown ignore-lane bits into its output trailer
rather than writing flags = 0 (§20.5)"), and drop one leg of the mutual citation so the
rule has one home.

## 9. What I checked and did not file

- §21.7's "§20.5's floor" phrasing surviving a repair that made the floor conditional:
  checked, still true and its stated reason still holds. Not filed.
- §21.6's two rows ("An ignore-lane flag bit (16–31) is set" and "version_minor is higher
  than this text defines") against the repair: both consistent with it. Not filed.
- Appendix G's reproducible-writer profile items 8/10 (version_minor at the floor, flags =
  0): that profile is a one-generation creator's ("**One generation**, so that the file is
  the output of a single commit"), and its own compactor carve-out at line 4179 concerns
  file_id, not flags or minor. No unswept restatement there. Not filed.
- Whether the repair silently changed the appender's rule: §20.3 step 6 is untouched by
  this hunk and still reads "unknown ignore-lane flag bits copied forward (`[R-CNT-08]`),
  and version_minor per `[R-CNT-26]`". Not filed against this hunk, though A-02 turns on
  what that step means.
- Blockquote placement (check 3): clean, both for the repair and for every restatement.
