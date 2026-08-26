# Cleanroom round 27 — findings

Protocol: ADR-0034, four phases, preceded by the ADR-0106 and ADR-0107 repair
audits recorded in `../26-g3/`. Charter: [prompt.md](prompt.md).

## Verdict

**Two byte-level ambiguities. G3 is not met.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** — twenty-first round running |
| Findings | **23**, from 7 reporters |
| Distinct defects | **16** by union-find; all three passes independently said 16 |
| Self-flagged byte-level | 4 |
| Surviving refute **and** an independent hand-check | **2** |
| Harness | 15 agents, **15 returned, 0 errors, 0 empty**; one degenerate return, recovered |

Byte-level history: … → 2 → 0 → 1 → **2**.

**This is the widest surface any round has been given** — thirteen passages, 117
lines inserted and 52 deleted over fifteen hunks, from six commits — and it
returned the highest byte-level count since round 21. Neither survivor is in
text this cycle touched.

**G3's criterion does not even reach its second half.** Round 26 returned one, so
round 27 was a fresh first half — the sixth. It returned two.

## The survivors

### 1. `appender-flags-origination` — `writer-02`, §6.3 `[R-CNT-08]`

**Nothing bars an appender from originating an ignore-lane flag bit absent from
the file it extends.**

`[R-CNT-08]`'s MUST is scoped to **"a writer creating a file"**: "In this
specification's text no flag bits are defined: a writer creating a file under
this text MUST write flags = 0". The next sentence shows the drafters read that
phrase as *producing a new file*, because a compactor needed an express carve-out
on exactly that ground — "A compactor, **though its output is a new file**,
carries the input's unknown ignore-lane bits into its output trailer rather than
writing flags = 0". An appender does not create a file. Its only stated flags
obligation is the one that follows: "An updater MUST copy forward unknown
ignore-lane bits of the file it modifies and MUST NOT clear them." Nothing says
it may not originate one.

**The two readings.** (1) *Strict scope* — flags = 0 binds creators and, but for
its exception, compactors; an appender may set an ignore-lane bit of its own.
(2) *Step 6 exhaustive* — §20.3 step 6 specifies the appended trailer as
"generation one greater, the same file_id, unknown ignore-lane flag bits copied
forward (`[R-CNT-08]`), and version_minor per `[R-CNT-26]`", and that enumeration
completely fixes the flags field, so the appended flags are exactly the input's.
The reporter picked (2) and graded itself byte-level.

**Why the emittable set moves.** The disputed file is **conforming** — §21.6
line 3676 says so in terms: "An ignore-lane flag bit (16–31) is set | Ignored;
the file is conforming". So `[R-CNF-05]` bars nothing under either reading, and
the charter's discriminator applies in the direction that moves the set. The
producer enumeration closes: a creator emits **generation 1** (§20.1, line 2981),
a compactor mints a fresh `file_id` **and generation 1** (§20.5, line 3294), and
`[R-LIF-01]` freezes bytes [0, F) so the prior generation's trailer carrying
flags = 0 stays inside the output. A generation-2 file whose live trailer sets a bit its
own embedded generation-1 trailer does not is therefore producible **only** by an
appender, and only under reading (1). Two conforming appenders, one input, one
instruction, trailers differing at offset 12 and consequently at offset 60.

**`[R-CNF-02]` does not save it — it sharpens it.** That rule places "§6.3's
flags = 0 against a set ignore-lane bit" among the obligations that "bind the
actor" while "the predicate binds the bytes". So the file stays conforming and
the *writer* does not: which is precisely a claim about what a conforming writer
may emit.

**Swept for a deciding sentence and found none.** Every occurrence of `flags = 0`
in the document is at lines 172, 873, 878 and 3312, and every mention of
`ignore-lane` at fourteen further lines; none binds an appender, and the only
appender-facing flags rule is copy-forward. Line 3312 restates the obligation as
one §6.3 requires "of a file created under this text", which shifts the framing
from actor to file without settling which actors it reaches.

### 2. `pe0-drop-adding-a-record` — `writer-03`, §20.4 `[R-WRT-08]`

**§20.4's MU = 0 / PE = 0 cell does not say whether adding a top-level non-layer
record licenses dropping a PE = 0 record.**

The cell licenses a drop only "in a commit that *independently* changes the scope
the record attaches to: … for a top-level record, the file's layer set, any layer
record's content, or another *non-layer* top-level record." It then resolves the
first item for addition — "A commit changes the layer set by adding a layer" —
and resolves the third for one operation only: "Dropping the record, or dropping
another record in the same commit, is not itself such a change." **Adding a
top-level non-layer record is addressed nowhere.**

The asymmetry looks deliberate: item one names a **set** and the text extends it
to addition; item three names an **individual record**, and changing a record
presupposes one existing before and after. So (1) the set reading licenses the
drop and (2) the individual reading bars it, and the reporter picked (1) on the
rule's evident purpose while conceding (2) is the better fit to the words.

The disputed file — generation *n*+1 carrying a newly added metadata record and
not carrying the dropped PE = 0 record — is an ordinary conforming file,
producible only by an appender for the same generation-and-`file_id` reasons as
above. Two conforming updaters emit directories differing by one 24-byte header
plus its inline payload, and therefore differ in `dir_length` at trailer offset
32, in `committed_file_length` at offset 40, and in F.

**This cell has now produced a byte-level defect in rounds 10, 14, 16, 17 and
27.** ADR-0081 measured it as the document's most defect-prone passage and it has
not stopped being one.

## The one that did not survive — `sec02-allocation-scope`

**`[R-SEC-02]`'s closing MUST NOT is unscoped and literally forbids the
decode-buffer allocation `[R-SER-07]` requires** — reported by **four** readers
independently (`reader-01`, `writer-01`, `verifier-01`, `quiz-01`), two of them
grading it byte-level, with two independently constructed conforming files.

§22.2 opens "a reader allocates from geometry and never from a length embedded in
a payload" and closes, four sentences later, "A reader MUST NOT size an
allocation, fetch, or index walk in proportion to a declared magnitude it has not
corroborated against the file's actual length". A tile's decoded size is a
declared magnitude, and under codecs 2–4 §17.2's Note says outright that "no
bound relates a stored length to its decoded size in either direction" — so
nothing corroborates it. `[R-SER-07]` nevertheless commands the allocation:
"readers allocate from those declarations, not from stored data."

**All three passes downgraded it; the refute phase returned DOWNGRADE_STANDS; the
hand-check agrees, and the reason is `[R-ERR-04]`.** A reader taking the literal
reading declines a tile whose every quantity lies inside §21.9's table, and
§21.9 line 3835 says "Software that declines **on that ground** a file whose
every quantity lies within the table is not a conforming reader (`[R-CNF-03]`)"
— and that the refusal "MUST be reported as a resource limit and not as a
validity error", which is the ground such a reader is on. So the two positions
are not two *conforming* readers: the document decides against the literal
reading, and the emittable set does not move.

**Two cautions recorded against that verdict.** First, the refuter's headline
citation — "requirements constrain bytes and observable behavior, never
implementation technique" — is at lines 113–114 **inside a blockquote labeled
`Note.`**, and is therefore non-normative under `[R-CNF-01]`. It cannot bound a
normative MUST NOT, and the verdict rests entirely on the `[R-ERR-04]` chain,
which is normative. Second, the skeptic's census found that "corroborated" and
"declared magnitude" each occur **exactly once in the document**, in the disputed
sentence — the rule defines neither term it turns on.

The defect is real and confirmed by every pass. What it is not is a fork.

## What the round says about the ledger

Three defects were already owned, by entries their reporters had never seen:

| Defect | Reporters | Sweep result |
|---|---|---|
| Appendix G item 5's shuffle universal | `writer-04`, `diagrams-02`, `adversary-01` — **three** | **Already Q-I6**, which records this sentence's three previous failures verbatim. This is the fourth. |
| §20.3 step 4's enumeration omits a channel's in-sample offset Fᶜ | `quiz-02` | **Q-B6 territory** — the same list, the same class; Q-B6's option (b) reaches it. Held with it rather than split off. |
| §20.4's PE = 0 drop and adding a record | `writer-03` | **Already Q-B7**, opened after round 25. Round 27 found it cold and supplied the construction the entry lacked. |

**Q-B7 is now byte-level and gates G3.** It was opened `[shaping]` on a walk that
did not grade it; this round grades it, with a conforming file and a producer
enumeration. That is a change in the entry's standing, not a new entry.

## Harness integrity

- **15 agents started, 15 returned, no error line beyond the one below.**
- **Every walk's transcript matches its structured return exactly**, by
  independent id-scrape: reader 3, writer 4, verifier 2, diagrams 4, register 4,
  adversary 3 — each equal to its own `transcript_finding_count`.
- **All three triage passes CLEAN on mechanical coverage** — 23 of 23 ids, exact,
  by set difference against the reporters' ids rather than any pass's
  `all_input_ids_seen`.
- **Union-find gives 16** against pass counts of 16, 16 and 16.
- The reconciler flagged all three byte-level groups **HAND-CHECK REQUIRED**; all
  three were hand-checked against the document, every construction fact
  re-verified by citation, and the survivors' producer enumerations re-derived.

### One degenerate return, recovered rather than inferred

`parallel[0]` of the refute phase tripped the degeneracy guard: its `reasoning`
field read *"See the reasoning field content above."* — 38 characters. **The
verdict was not lost.** Recovered from `journal.jsonl`, the agent returned
`DOWNGRADE_STANDS` with a 3,862-character argument that it had written into
`decisive_quotes` instead — ten citations, against 38 characters of `reasoning`. A transcript that shows the work and states no verdict
is not a verdict; this one states its verdict, and it is the safe direction — the
refuter declined to manufacture a refutation. It is counted.

**Two of the three refuters wrote pointer-style reasoning fields**, and only one
tripped the guard: the third returned *"See the reasoning captured in this
field's companion narrative above."* at 69 characters, over the 40-character
threshold. **The guard measures length, and the defect is not length.** It should
also reject a `reasoning` that matches a pointer phrase, and the refute schema
should stop offering `decisive_quotes` as a place an argument can hide.

**The quiz author's return is not mechanically checkable against its transcript.**
`WALK_SCHEMA` carries `transcript_finding_count`; the quiz-author schema does
not. It returned three findings and its transcript labels one by id — the
substance of a second is there unlabelled, and the transcript states "Three,
recorded in the structured result", so nothing is lost. Nothing compared them,
though, which is the condition that lost seven findings in an earlier round.

### The relocation worked

Round 26 disclosed that all three triage passes ran an orienting listing of the
output directory before internalising their brief. This round the passes'
transcripts were written to three separate directories outside `OUT`, and **no
pass ran any listing** — the skeptic said so unprompted: "no directory listing —
I did not run any orienting listing this round, and I opened no walk
transcript." All three confirm they opened no walk transcript and no other pass's
notes. The fix was to the harness, as the finding said it should be.

## Disclosures

All ten spec-reading agents disclosed injected context: a project instruction
pointer, an index of the maintainer's notes, and an environment block naming the
branch and recent commit subjects. The register hunter and the adversary each
noted that the commit subjects name ADR numbers and, in outline, the subject
matter of recent decisions. **This is the sixth round in which the channel has
been disclosed and no mechanical check in this project can see any of it.**

**The quiz author reported a discrepancy in its own brief**, unprompted and
correctly: "the brief said the document is 4,550 lines; `wc -l` reports 4,549. I
took no action on the discrepancy beyond recording it." Both numbers are right —
4,550 is the count the charter and round 26's charter both use, which is the
length of `split('\n')`, one more than `wc -l` on a newline-terminated file. The
charter is not wrong; it is unstated which convention it uses. An agent told to
distrust its inputs found the one arithmetic claim in its brief it could check.

Both parts of the lineage gate return clean.

## Disposition

The document and the ledger were swept before any repair was proposed.

**To the ledger — byte-level, and ADR-0091 forbids settling a rule's reach in a
repair slot.**

| Defect | Disposition |
|---|---|
| `appender-flags-origination` | **New entry, Q-B9** — which actors the flags = 0 obligation binds. Options: state it over every writer producing a trailer under this text; state it over creators only and say so; or make §20.3 step 6's enumeration expressly exhaustive. Byte-level, so it gates G3. |
| `pe0-drop-adding-a-record` | **Already Q-B7**, whose standing changes: byte-level, gating G3, with this round's construction attached. |

**To the ledger — recommended, not byte-level.**

| Defect | Disposition |
|---|---|
| `sec02-allocation-scope` | Bounding `[R-SEC-02]`'s MUST NOT is a claim about the whole passage, and this week produced two repairs that replaced a false universal with a narrower false one (ADR-0106). Four reporters, and the rule defines neither term it turns on. **Recommend a ledger entry** rather than a repair written in the same shape that has just failed twice. |

**Repairable, each checkable against a named rule.** None is byte-level; four
touch register cells and so need an ADR under ADR-0104.

| Defect | Checkable against |
|---|---|
| `appendix-g10-nfd-length-universal` | §4.6 `[R-ENC-13]`, `[R-ENC-14]` — NFD/NFC forms of equal length falsify "a different length" |
| `bool-layout-note-degenerate-p` | §11.1 `[R-GEO-01]` — the Note is false at P = 1, where ⌈P/8⌉ = P |
| `specialization-list-omits-f21-f22` | §21.1's own specialization clause against rows F21 ⊂ F22, L10 ⊂ L11 *(register)* |
| `sentinel-row-drops-qualifiers` | §13.3 `[R-TYP-08]`'s two qualifications, dropped by §21.6's row *(register)* |
| `r3-r4-overlap` | §18.2 `[R-MTA-09]` — R3 and R4 both register the same condition *(register)* |
| `f21-inline-gloss` | §7.1 `[R-CNT-25]` — the gloss describes a state record framing makes unrepresentable *(register)* |
| `tile-outcome-header-drops-qualifier` | §2.4 `[R-CNF-09]`'s obliged-to-detect qualifier |
| `wrt06-same-ground-antecedent` | §20.5 `[R-WRT-06]` — the cell borrows an anaphor whose nearest antecedent is the wrong ground |

**Deferred with named owning sections.**

| Defect | Owning section |
|---|---|
| `appendix-g3-leading-gap` | Appendix G — split verdict (two PARTIAL, one REFUTED); the leading run from 16 to the first structure is reachable only by following a citation |
| `mta10-report-scope` | §18.2 — which encodings `[R-MTA-10]`'s report duty ranges over; decides a rule's reach, so it is a decision rather than a repair |
| `mta10-uninspected-bytes-aphorism` | §18.2 — split verdict (skeptic PARTIAL); the choice between bounding the aphorism and honouring it is the maintainer's |

Zero findings are left without a disposition.
