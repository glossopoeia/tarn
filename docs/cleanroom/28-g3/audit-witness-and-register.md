# Repair audit — hunks 7 and 8, §21.7 "What no check detects"

Auditor lane: witness-and-register.
Charter: §21.7's account of what no check detects, and the register's relationship
to §20.3 step 4's bars.

---

## 0. Disclosure

Files opened:

- `/private/tmp/.../case-adr0113/hunk-07.diff` (my charter's hunk)
- `/private/tmp/.../case-adr0113/hunk-08.diff` (my charter's hunk)
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (the specification)

Nothing else. I did not open `full.diff`, any other hunk file, `docs/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`, `spec/registry.json`,
git history, or the web. I did not list the case directory. I wrote exactly one file,
this transcript.

Commands run: `sed -n` range reads of spec/tarn.md; `grep -n`; `awk` line filters;
two `python3` heredocs that read only `spec/tarn.md` (one to count register rows and
instances, one to run whitespace-normalised phrase sweeps). No network. No other file
was read by any script.

**Context I did not ask for.** Material appeared in my context before I began: a
project-instructions pointer (CLAUDE.md → AGENTS.md), a user auto-memory index with
two entries naming prior-round subjects, a list of MCP servers/skills, and an
environment/git-status block that printed the subject lines of five recent commits.
I name that it appeared; I do not repeat its contents, and no conclusion below
depends on it. Every finding is grounded in a quotation from `spec/tarn.md` or from
the two hunk files, and I re-derived each from the document. In particular I did not
use the commit subject lines as evidence about what the repairs were for.

---

## 1. The two hunks, and the rule each adopts

### Hunk 7 — lands at spec/tarn.md 3896-3916

Verified landing: line 3896 is `§20.3 step 4's **§14 bar** is witnessed only where the affected tiles`.
Verified nearest preceding heading: line 3862 `#### 21.7 What no check detects`. The
header in the hunk file is correct; no mismatch to report.

Deleted (5 lines):

> §20.3 step 4's bar on a declaration change is witnessed only where
> the affected tiles remain stored, and then only for part of what it
> bars. A change reaching a byte §14 structurally constrains — a
> padding position, a pad bit, or a boolean byte — fires §21.4's
> content rows. A change reaching the decoded size is witnessed by T3

Inserted (21 lines), as it now reads in the file at 3896-3917:

> §20.3 step 4's **§14 bar** is witnessed only where the affected tiles
> remain stored, and then only for part of what it bars — a re-typed
> channel among the cases it does not reach, since the prior
> generation's declarations are not part of the live state, which is
> all §9.7 walks, and no check can know which type a channel carried
> before. Its companion bar on a planar layer's disk ordinals is
> witnessed indirectly and only sometimes, and for the same reason no
> check knows which ordinal a stored tile used to occupy: a permutation
> among channels whose planes are the same length disturbs nothing a
> row can see, while one that leaves a plane of one length at an
> ordinal the new declarations size differently is caught by T3, or by
> T14 under codec 1. Where
> the change does touch something §14 fixes, the rows below reach it
> on the terms they state there and no better, and a commit that
> supersedes every tile it would have damaged escapes them exactly as
> it escapes the §14 bar. Which case a type change falls in is not
> decided by the element sizes of §12.1: a planar `uint8` channel re-declared
> `bool` keeps its element size of 1 while its plane goes from
> P · Bᶜ bytes to ⌈P/8⌉. A change reaching a byte §14 structurally
> constrains — a padding position, a pad bit, or a boolean byte — fires
> §21.4's content rows. A change reaching the decoded size is witnessed by T3

**The rule hunk 7 adopts, in my words.** It makes six assertions of fact about what a
single-file check can see, and those assertions constrain nobody's bytes directly but
do fix, for an implementer, the boundary between "the register omits this because it
is undetectable" and "this is registered":

1. The §14 bar of §20.3 step 4 is witnessed only for tiles still stored in the new
   generation, and then only partly.
2. A re-typed channel is one of the cases *it* — antecedent disputed, see §3 — does
   not reach, on the ground that no check can know the prior generation's declarations.
3. The companion bar (planar disk ordinals) is witnessed indirectly and sometimes.
4. A same-plane-length channel permutation is invisible to every register row.
5. A permutation that leaves a plane of one length at an ordinal now sized differently
   is caught by T3, or T14 under codec 1.
6. A commit that supersedes every tile it would have damaged **escapes the §14 bar**
   as it escapes the rows.
7. Element size does not decide which case a type change falls in: planar `uint8` →
   `bool` holds element size 1 while the plane goes P·Bᶜ → ⌈P/8⌉.

### Hunk 8 — lands at spec/tarn.md 3935

Verified: line 3935 is `live state clean, so the §14 bar is unwitnessed there for the same`.
Nearest preceding heading 3862, as stated. Correct.

The whole change is `the bar` → `the §14 bar`, disambiguating a bare reference that
became ambiguous the moment hunk 7 introduced a second bar into the paragraph.

**The rule hunk 8 adopts.** None new. It fixes the referent of one noun phrase.

---

## 2. Passages read in full

- §21.7 entire, spec/tarn.md 3862-3949.
- §20.3 entire, 3073-3280 (the append procedure, all six steps, both bars, the
  growth/shrink paragraphs, and the Note/Example blocks that close it).
- §21.1, 3544-3625 (how to read the register, the completeness clause, the Instances
  rule).
- §21.2/§21.3/§21.4/§21.5 preambles and the whole §21.4 table (3745-3773).
- §21.8, 3951-3957. §21.9, 3958-3990 (its per-instance paragraph, for the
  "individuated differently" language).
- §11.1 (1582-1630) including the **Rationale.** block at 1600-1628 that restates
  both bars.
- §11.2 (grid arithmetic, N, P, C·N), §11.4/§11.3 as reached.
- §12 entire (1720-1824): the sample-type table with element sizes.
- §14 entire (1922-2119): §14.1 value sequence, §14.2 byte layout and decoded size,
  §14.3 packed boolean planes, §14.4, §14.5 padding content.
- §9.1 (`[R-LIF-01]`, 1222-1240) and §9.7 (coverage verification, 1440-1490).
- §11.4 disk-ordinal rule `[R-GEO-06]` (1690-1705).
- §2.2 `[R-CNF-01]` at 104-106; `[R-CNF-05]` at 199-202.
- §16 slab invariants `[R-SLB-03]`/`[R-SLB-04]` (2290-2320), for L41/L42.

---

## 3. Check-by-check

### Check 3 first (normative placement), because everything else depends on it

I applied the **label** test, not the ">" test.

```
awk 'NR>=3862 && NR<=3950 && /^>/ {print NR": "$0}' spec/tarn.md   → no output
awk 'NR>=3862 && NR<=3950' spec/tarn.md | grep -c '^>'             → 0
```

§21.7 contains **no blockquote at all**, hence no *Note*, *Example* or *Rationale*
label. `[R-CNF-01]` (line 104-106, verbatim): "All text in this document is normative
except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and
appendices identified as non-normative." §21.7 is therefore **normative text**, and
both hunks land in normative text. The repair lands.

§20.3 step 4 is likewise unblockquoted numbered-list prose; both bars are normative
MUST NOTs there.

The one restatement of the same subject matter that *is* label-exempt is the
**Rationale.** block at §11.1 (1600-1628). It is non-normative, so it cannot itself
contradict anything normatively — but it is direct evidence of what the document
means, and it says the opposite of hunk 7's assertion 2. Recorded under check 4.

**Verdict: passes.** No rule whose only statement is in a labeled block; no labeled
block edited while a normative statement elsewhere kept the old rule.

### Check 2 — citations resolve

Every identifier and section number in the repaired text, opened and read:

| Citation | Claim made about it | Verdict |
|---|---|---|
| §20.3 step 4 | has a "§14 bar" and a companion bar on a planar layer's disk ordinals | **passes.** 3141-3147 defines and names the §14 bar ("Call this the **§14 bar**."); 3175-3182 states the companion: "For a **planar** layer, a commit MUST NOT change the channel declarations in a way that alters the disk ordinal `[R-GEO-06]` assigns any tile the layer stores in the generation this commit supersedes." §20.3 never uses the word *companion* — it says "One effect is barred beside it" and "The bar beside the §14 bar" — but the referent is unambiguous. |
| §9.7 | "the live state … is all §9.7 walks" | **passes.** §9.7 opens "A verifier checking `[R-CNT-02]`'s partition walks the live state only", and its closing Note: "Nothing here enumerates prior commits." |
| §14 ("what §14 fixes") | padding content, decoded size, sample byte offsets | **passes.** §14.2 table (decoded size, offset of value k), §14.3 (⌈P/8⌉, pad bits), §14.5 (`[R-SER-05]` padding content). §20.3's own list at 3143-3147 matches. |
| §12.1 ("the element sizes of §12.1") | bool element size 1, uint8 element size 1 | **passes.** §12.1 table: `bool` id 1 element size 1; `uint8` id 6 element size 1. And §12.1 explicitly: element size "enters §14's byte-layout arithmetic, **except that a planar bool plane is sized by packing (§14.3)**". The repaired sentence is exactly this point, correctly made. |
| P · Bᶜ → ⌈P/8⌉ | planar numeric plane length vs packed planar bool plane length | **passes.** §14.2 table row "planar, numeric channel c | P · Bᶜ"; §14.3 "the decoded size is ⌈P/8⌉ bytes". |
| T3 | "caught by T3" for a plane landing at an ordinal the new declarations size differently | **passes.** T3 (3748): "The decoded payload's byte length is not exactly the tile's decoded size derived from the layer's declarations", reader / tile use, `[R-SER-07]`. A plane of length X sitting at an ordinal whose channel now sizes ≠ X is exactly this. |
| T14 | "or by T14 under codec 1" | **passes.** T14 (3761): "Codec 1 (none) declared and a non-sentinel index entry's length differs from the tile's decoded size", `[R-COD-04]`. The codec-1 restriction in the repaired text matches the row's own restriction. |
| §21.4's content rows (in the untouched sentence immediately after the insertion) | fired by a change reaching a byte §14 structurally constrains | **passes.** T2, T4, T5 are the §21.4 content rows; T4 is `[R-SER-05]`, T5 is `[R-SER-05]` (R-SER-03), T2 is `[R-SER-08]`. |
| `[R-LIF-01]` (hunk 8's sentence) | "it is a property of the prior generation, which §9.7 does not reconstruct" | **passes.** §9.1: bytes in [0, F) are immutable; establishing a violation needs the prior bytes, which §9.7's live-state-only walk does not hold. |
| `[R-WRT-06]`, §20.5, `[R-ENC-06]`, `[R-CNT-13]`, `[R-CNT-18]`, `[R-GEO-06]`, `[R-SER-01]`, `[R-COD-10]` | all in untouched neighbouring text | not re-verified in depth; out of hunk. `[R-GEO-06]` I did open (1701-1704), because finding C-04 turns on it: "**c · N + s** for a planar layer … where c is the channel's index — channel-major grouping". |

No citation in the repaired text points at a rule that fails to say what the sentence
claims. **Check 2 passes clean.** The defects below are all internal.

### Check 1 — tense and quantifier

The two normative rules being restated, quoted:

§14 bar, spec/tarn.md 3141-3147:

> A commit MUST NOT change a layer's declarations in a way that alters, for any tile
> that layer stores **in the generation this commit supersedes**, what §14 fixes for
> its stored bytes or how they decode — the set of padding positions (§11.3) and the
> content `[R-SER-05]` fixes there, the decoded size, the byte offset of any sample
> within the decoded tile image, or the codec and filter that produced the stored
> bytes. Call this the **§14 bar**.

Companion bar, 3175-3182:

> For a **planar** layer, a commit MUST NOT change the channel declarations in a way
> that alters the disk ordinal `[R-GEO-06]` assigns any tile the layer stores in the
> generation this commit supersedes.

Generation-by-generation comparison of each repaired clause:

- "witnessed only where the affected tiles **remain stored**" — new generation. This
  is *not* the bar's quantifier (the bar's is the superseded generation) and it should
  not be: witnessing needs a live tile. Correct, and pre-existing text.
- "no check can know which type a channel carried **before**" — prior generation.
  Correct.
- "no check knows which ordinal a stored tile **used to occupy**" — prior generation.
  Correct.
- "a commit that supersedes **every tile it would have damaged**" — the damaged set is
  quantified over the superseded generation ("would have damaged" = would have damaged
  had they survived), and "supersedes" is this commit's act. Correct.
- "a permutation among channels whose planes are the same length" — quantifier problem,
  but of *range*, not tense: see check 6 / C-05. §20.3's companion bar ranges over
  reordering **and** insertion **and** removal; the repair ranges over permutations only.
- "a re-typed channel among the cases it does not reach" — quantifier over re-typings is
  unrestricted, and §20.3's own text restricts nothing that would save it. See C-01/C-02.

**Verdict: the tense discipline holds throughout; the quantifier discipline fails twice
(C-02's unrestricted "a re-typed channel", C-05's "a permutation").**

### Check 4 — contradiction in the same passage, including untouched text

I read the whole of §21.7 (3862-3949) and the whole of §20.3 step 4 (3117-3260).
Three collisions.

**(a) Untouched sentence, three sentences earlier in the same paragraph** (3885-3891):

> the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a structurally
> valid tile whatever values it carries, except where §14 constrains a byte's content —
> a padding position, a pad bit, or an interleaved boolean — **and a mis-ordered image
> is then witnessed by T2, T4 or T5**, exactly as a mis-strided filter is;

against the inserted (3906-3908):

> a permutation among channels whose planes are the same length **disturbs nothing a
> row can see**

The earlier sentence is precisely about `[R-GEO-06]`'s ordinal mapping — the same rule
the companion bar cites — and says the mis-ordering *is* witnessed wherever §14
constrains a byte's content. The insertion says an equal-length permutation disturbs
nothing. Constructed counterexample in §4 below. → **C-04**.

**(b) §20.3 step 4, 3148-3152**, verbatim:

> The tense is the prior generation's (§3.1 defines *stored* against a generation), so
> **a commit does not escape this by unstoring in the same breath: superseding every
> tile of a layer and re-declaring it are one operation, and this bars it.**

against the inserted (3910-3912):

> and a commit that supersedes every tile it would have damaged escapes them **exactly
> as it escapes the §14 bar**.

§20.3 exists to forbid that exact inference. Note also that §20.3's forward reference to
§21.7 uses the careful formula and not this one (3241-3243): "§21.7 records the
consequence — **that this is precisely where the §14 bar has no witness**, the live state
being clean". *Has no witness*, not *is escaped*. And hunk 8's own sentence 20 lines
later gets it right: "so the §14 bar is unwitnessed there". → **C-03**.

**(c) §20.3 step 4, 3159-3162**, verbatim:

> A channel's declared **sample type** is such a declaration, and changing it is such a
> change wherever the layer stores a tile that carries that channel

and the §11.1 **Rationale.** restatement (1616-1618), non-normative but unambiguous:

> Re-typing a channel is the §14 bar's own subject, barred wherever the layer stores a
> tile that carries that channel, and free where it does not.

against the inserted (3897-3899):

> and then only for part of what it bars — **a re-typed channel among the cases it does
> not reach**

→ **C-01** (on the pronoun's nearest-antecedent reading) and **C-02** (on the charitable
reading).

I looked for and did **not** find: a carve-out sentence in §21.7 that the insertion's
breadth collides with; a MUST elsewhere in §21.7 (there is none — §21.7 states no
normative keyword at all, it is descriptive normative prose); a sentence in §21.7
written to be true only under the pre-hunk single-bar wording other than the bare
"the bar" hunk 8 already fixed.

### Check 5 — exhaustive claims

Every completeness word in the repaired text, and my attempt to falsify it:

| Word / phrase | Falsifiable? |
|---|---|
| "witnessed **only** where the affected tiles remain stored" | pre-existing; survives. A witness needs bytes a reader reaches, and §9.7 reaches live state only. |
| "**only** for part of what it bars" | survives (weakest possible claim). |
| "which is **all** §9.7 walks" | survives — §9.7 first sentence. |
| "**no** check can know which type a channel carried before" | survives. No field records a prior declaration; §9.7's Note: "Nothing here enumerates prior commits." |
| "**no** check knows which ordinal a stored tile used to occupy" | survives, same ground. |
| "disturbs **nothing** a row can see" | **FALSIFIED.** T4 / T5. See §4. → C-04 |
| "a re-typed channel among the cases it does not reach" (an unqualified class claim) | **FALSIFIED by the insertion's own next-but-one sentence.** → C-02 |
| "**Which case** a type change falls in" (presupposes exactly two) | survives as a dichotomy, but its antecedent is wrong → C-07 |
| "the rows below reach it … **and no better**" | survives. |
| "**every** tile it would have damaged" | survives. |
| "is caught by T3, **or** by T14 under codec 1" | survives as stated (both rows verified). Note it is stated as sufficient, not exhaustive — T21/T22 could also fire under codec 3 — and "or" does not close the list, so no overclaim. |

### Check 6 — what the repair left open in the same structure

**The structure:** §20.3 step 4's obligations on a commit, and specifically the subject
matter each bar ranges over.

*Members of the companion bar's subject*, per §20.3 3182-3187, verbatim:

> A channel's tiles move exactly when its index does: **reordering** moves those channels
> the reorder re-indexes, and **inserting or removing one** moves every channel after the
> affected position. **Either** is such a change wherever the layer stores a tile for a
> channel that moved.

Two members. The repair's account names one — "a permutation among channels" — and then
partitions *that* one exhaustively (same plane length / different plane length). Channel
insertion and channel removal at a non-terminal position are governed by the bar and
unaccounted for in §21.7. They behave differently, too: they change C, hence the
addressed-tile count C·N (§11.2) and hence entry_count, so an offending commit shows up
against a different set of rows (L21's `planar C·N` instances) than a permutation does.
→ **C-05**.

*Members of step 4's other unwitnessed obligations.* The paragraph the repair rewrote is
introduced by a stated criterion — "A second set of obligations is omitted from the
register because a single file exhibits no witness of their violation" (3879-3881) — and
the repair converted a vague singular ("step 4's bar on a declaration change") into an
enumeration ("the §14 bar" … "Its companion bar"). Step 4 carries at least two further
obligations that meet the same criterion and are enumerated nowhere:

- "**every other entry byte-identical at its disk-ordinal position**" (3128-3129), read
  together with step 2's "a malformed index entry an appender meets while re-emitting a
  region is carried forward byte-identically at its disk-ordinal position under step 4,
  **not repaired to a sentinel**" (3084-3087). A file in which the appender repaired one
  to a sentinel is structurally perfect; nothing in the live state records what the entry
  used to be.
- "A layer whose record alone changes **keeps its extent slot**, pointing at the existing
  region … relocating a live index region is compaction's operation (§20.5,
  `[R-WRT-07]`), not an appender's" (3130-3136). An appender that relocates one produces
  a file indistinguishable from a legitimate commit.

I checked whether the document hedges this list open. It does not. The document hedges
open lists explicitly when it means to — `grep` for "not offered as exhaustive" (1 hit,
§20.3's growth list) and "not offered as closed" (2 hits, §21.1's specialization list and
§23's operations list) — and §21.7 carries no such hedge, while §21.1 calls it "**the**
account, by class, of what fails it". I report this at PLAUSIBLE, not CONFIRMED: "by
class" may be doing the hedging work. → **C-05** covers the companion-bar half; I fold
the step-4 half into C-05's detail rather than raising a separate low-confidence finding,
because the two are one omission of the same shape.

### Check 7 — analogies, verb against verb

Three analogy markers in the repaired text. All three compared word for word.

**(i) "escapes them exactly as it escapes the §14 bar"** — marker: *exactly as*.

| side | governing verb + object | relation asserted |
|---|---|---|
| repair, first half | "**escapes them**" — *them* = "the rows below", i.e. T3, T14, T2/T4, T15/T17/T23/T25 | **detection**: a row is a check; escaping it means no check fires |
| repair, second half | "**escapes the §14 bar**" | the §14 bar is not a check. §20.3: "A commit **MUST NOT** change a layer's declarations…". Escaping a MUST NOT means **not being prohibited** |

The two do not range over the same relation at all. A commit can fail to be detected
while being flatly prohibited — that is the entire subject of §21.7. The analogy
transfers a true statement about rows onto a false statement about a prohibition. This
is the check-7 shape exactly, and it is the finding I rate highest. → **C-03**.

**(ii) "for the same reason no check knows which ordinal a stored tile used to occupy"**
— marker: *for the same reason*.

| side | verb | set |
|---|---|---|
| §14 bar's reason | "no check **can know** which **type** a channel **carried** before" | prior-generation channel declarations |
| companion bar's reason | "no check **knows** which **ordinal** a stored tile **used to occupy**" | prior-generation disk-ordinal assignment |

Both range over prior-generation declaration state, which §9.7 does not reconstruct.
Same set, same verb sense. **The analogy holds.** Reported as passing. (The *conclusions*
drawn on each side differ — "does not reach" vs "witnessed indirectly and only sometimes"
— which is the asymmetry C-02 turns on, but the shared reason is genuinely shared.)

**(iii) hunk 8's "for the same reason `[R-LIF-01]` is"** — marker: *for the same reason*.

| side | governing verb | set |
|---|---|---|
| `[R-LIF-01]` | "a writer **MUST NOT modify** them" (bytes in [0, F)) | the committed prefix as it stood before this commit |
| §14 bar | "A commit **MUST NOT change** a layer's declarations in a way that **alters** … for any tile that layer **stores in the generation this commit supersedes**" | the superseded generation's stored tiles |

Both quantify over state the current file no longer exhibits, and the shared reason
given — "it is a property of the prior generation, which §9.7 does not reconstruct" — is
true of both. **The analogy holds.** Reported as passing. Hunk 8's whole contribution is
to make clear which bar is the subject of this sentence, and it is the right one: §20.3
itself points here for the §14 bar ("§21.7 records the consequence — that this is
precisely where the §14 bar has no witness, the live state being clean").

Testing analogy (i) against **each** row it carries, as the charter requires, since one
sentence carries it for a whole set:
- against T3: a commit superseding every damaged tile leaves no tile whose payload length
  T3 can compare → escapes T3. True.
- against T14: same, no surviving entry → escapes T14. True.
- against T2/T4/T5: no surviving padding to check → escapes them. True.
- against T15/T17/T23/T25 ("the rows for the codec now declared"): no surviving stored
  bytes under the new declaration → escapes them. True.
- against **the §14 bar**: FALSE, per §20.3 3148-3152. One member of the set the analogy
  is carried over breaks it — and it is the member the analogy names as its warrant.

### Check 8 — what the insertion did to its neighbours

Hunk 7 inserts. Every back-reference from the insertion point forward to the end of
§21.7, with its pre- and post-insertion resolution:

| Back-reference (line) | Before the insertion | After the insertion | Changed? |
|---|---|---|---|
| "**it** bars" (3897) | "§20.3 step 4's bar on a declaration change" | "§20.3 step 4's **§14 bar**" | no (same bar, renamed) |
| "the cases **it** does not reach" (3898) | did not exist | nearest antecedent is "**it**" in "what it bars" three words earlier = the §14 bar; intended is evidently the *witnessing* | **new, and wrong** → C-01 |
| "**Its** companion bar" (3901) | did not exist | nearest antecedent "the §14 bar" → reads "the §14 bar's companion bar"; intended "§20.3 step 4's". Harmless in sense; recorded, not filed. | new, benign |
| "**the change**" in "Where the change does touch something §14 fixes" (3909-3910) | n/a | nearest is the permutation of the previous clause; intended is any declaration change | ambiguous, minor; folded into C-07 |
| "**the rows below**" (3910) | n/a | §21.7's rows are *above* it (§21.2-§21.5, lines 3626-3808); "below" can only mean "named later in this paragraph", against the document's only other use of the phrase | **new** → C-06 |
| "**them**" in "escapes them" (3911) | n/a | "the rows below" | resolves fine |
| "**Which case**" (3913) | n/a | nearest "cases" are the permutation dichotomy of 3906-3909, which is not about type changes; intended is the touches-§14 / does-not dichotomy of 3909-3910 | **new** → C-07 |
| "A change reaching a byte §14 structurally constrains…" (3915-3917, untouched) | continued directly from "part of what it bars", one bar in play | now follows 21 lines about two bars and a type-change example; the series "A change reaching X" no longer says which bar it is scoped to | changed, but each member is still true of the §14 bar and the decoded-size member is true of the companion bar too (the insertion itself says T3/T14 for both). Recorded; **not filed as a defect.** |
| "the change is unwitnessed **there**" (3925) | in the codec case | unchanged | no |
| "**Neither** change" (3930) | filter change / sample-offset move, both named in the preceding sentence | unchanged | no |
| "so **the bar** is unwitnessed there" (3935) | the single bar | would now have re-resolved ambiguously — **this is exactly what hunk 8 fixes** | fixed by hunk 8 |
| "**it** is a property of the prior generation" (3936) | the bar | the §14 bar | correct |
| "are unwitnessed for a reason all **three** share" (3938-3940) | §20.5's three `[R-WRT-06]` obligations | unchanged | no |
| "For **the last two** there is a second" (3941) | the ignore-lane bits and the version_minor floor | unchanged | no |

Backwards direction (does the inserted text lean on an antecedent further away than the
reader will look): yes, twice — "Which case" (C-07) and "the rows below … there" (C-06).

Sweep for stale bare references hunk 8 might have missed:

```
"the bar"   → 9 hits document-wide, NONE of them in §21.7 after hunk 8.
"§14 bar"   → 11 hits: 8 in §20.3/§11.1, 3 in §21.7 (3896, 3912, 3935).
```

Hunk 8's sweep is **complete** for the phrase it targets. That is a clean repair.

---

## 4. The constructed cases

The charter asks for files, not arguments. Both bars, one at a time.

### Case A — the §14 bar, re-typing, tiles remaining stored

Planar layer L, d = 1, E₀ = 8, T₀ = 8 → G₀ = 1, N = 1, P = 8. Channels
`a` (`uint8`, fill `0x00`) and `b` (`uint8`, fill `0x00`). C = 2, addressed tiles
C·N = 2, disk ordinals 0 (`a`) and 1 (`b`). Both stored, codec 1, filter 1. Each plane
is P·Bᶜ = 8 bytes. No padding positions (E₀ mod T₀ = 0).

Generation 2 re-declares `a` as `int8`, fill byte unchanged `0x00`, and stores nothing new.

Is this barred? §20.3: "A channel's declared **sample type** is such a declaration, and
changing it is such a change wherever the layer stores a tile that carries that channel."
Layer L stores a tile carrying `a` in the superseded generation. **Barred.**

Is it witnessed? Element size 1 → 1; decoded size 8 → 8; padding: none; `[R-SER-08]`:
not a bool channel; codec/filter unchanged. T3 no, T14 no, T4/T5 no (no padding
positions), T2 no. The generation-2 file is **fully conforming**. This is the case in
which §21.7's "no check can know which type a channel carried before" is exactly right,
and it is also the case that makes C-01 byte-level: reading hunk 7's clause with "it" =
the §14 bar, a writer concludes this commit is permitted; reading §20.3, it is
prohibited; and the file it produces carries no register-row violation, so `[R-CNF-05]`
does not bar it under either reading. The bytes fork.

### Case B — the §14 bar, re-typing, witnessed

Same layer, `a` re-declared from `uint8` to `bool`. Element size stays 1 (§12.1); the
plane goes from P·Bᶜ = 8 bytes to ⌈P/8⌉ = 1 byte (§14.3). The stored 8-byte payload at
ordinal 0 now fails T3 ("payload longer", the row's `packed planar bool ⌈P/8⌉, payload
longer` instance) and, codec 1 being declared, T14 as well.

So a re-typed channel is **not** uniformly "among the cases it does not reach" — this is
the case the repair's own next-but-one sentence constructs, for the express purpose of
saying the element sizes do not decide it. → C-02.

### Case C — the companion bar, equal plane lengths, witnessed

Planar layer M, d = 2, extents (5, 5), tile extents (4, 4) → G = (2, 2), N = 4,
P = 16. Padding positions exist (§11.3: E mod T ≠ 0 on both axes). Channels
`a` (`uint8`, **fill `0x00`**) and `b` (`uint8`, **fill `0xFF`**). C = 2, addressed
tiles 8, ordinals 0-3 = `a` (c=0), 4-7 = `b` (c=1) by `[R-GEO-06]`'s c·N + s. All eight
stored. Both planes are P·Bᶜ = 16 bytes — **the same length**, which is the repair's
stated case.

Generation 2 exchanges the two channel entries: `b` first, `a` second. Disk ordinals of
every stored tile move (§20.3: "exchanging `a` and `b` moves all four"). **Barred** by
the companion bar. Per step 4's re-emission rule — a channel permutation is not a
geometry change, and "a geometry change renumbers ordinals wherever `[R-GEO-06]` moves
them" names the only occasion — the entries are re-emitted byte-identical at their
disk-ordinal positions. So the extent at ordinal 0 still holds `a`'s old plane.

A verifier now reads ordinal 0 as channel index 0 = `b`, fill `0xFF`. §14.5 /
`[R-SER-05]`: "at every padding position, a writer MUST encode, for each channel the
position carries, that channel's fill value", and "a verifier MUST check it, and a
violation is a validity error at tile scope". The plane's padding bytes hold `0x00`.
**T4 fires** — its `planar numeric plane fill bytes` instance.

Lengths are equal throughout, so T3 and T14 see nothing. The row that sees it is T4, and
the repaired sentence says no row can. → **C-04.** With `a` and `b` both `bool` and
differing fill *bits*, T5 fires instead (final-byte pad bits, `[R-SER-05]` (R-SER-03)) —
so the falsification is not an artifact of one type.

The claim is true only when the permuted channels' recorded fills coincide, or the layer
has no padding positions and no pad bits. It is stated without either condition.

### Case D — the companion bar, unequal plane lengths

Same layer M with `a` (`uint8`, plane 16 bytes) and `b` (`bool`, plane ⌈16/8⌉ = 2 bytes);
exchange them. Ordinal 0 now belongs to `b`, whose decoded size is 2, and holds a 16-byte
payload. T3 fires; under codec 1, T14 too. **The repair is correct here.** Both citations
verified against the row text.

### Case E — the companion bar, genuinely unwitnessed

Same as Case D, except the offending writer *also* renumbers, moving each channel's
entries to follow it. That violates step 4's re-emission rule rather than being rescued
by it, and the resulting file is byte-consistent: every plane sits at an ordinal its own
channel sizes. Nothing fires. The repair's hedge "**only sometimes**" covers this, and I
record it as the sentence earning its hedge.

### Case F — the supersede-everything case

Layer L of Case A. Generation 2 supersedes both stored tiles (writes new payloads for
ordinals 0 and 1) **and** re-types `a` from `uint8` to `bool` in the same commit, sizing
the new payloads to the new declarations (1 byte for `a`'s plane).

§20.3: "so a commit does not escape this by unstoring in the same breath: superseding
every tile of a layer and re-declaring it are one operation, **and this bars it**."
**Barred.** The generation-2 file, however, is entirely conforming: every live plane
matches its live declaration.

Writer P follows hunk 7's "a commit that supersedes every tile it would have damaged
escapes them exactly as it escapes the §14 bar" and emits this commit. Writer Q follows
§20.3 and refuses, emitting instead a new layer (§20.3: "Such a change is a new layer, or
a whole-file rewrite under a fresh file_id"). The two files differ from the first appended
byte onward: P's file has a new layer-L index region and re-typed channel entry at F; Q's
has an additional layer record and a second index region, and layer L's declarations
unchanged. Both are `[R-CNF-05]`-conforming files. **The emittable set moves.** → C-03,
byte-level.

I checked for a precedence rule that would settle P against Q. §21.1 supplies one only
for rows ("where a row and the rule it cites diverge, **the rule governs**") and extends
it only to §21.6 ("§21.6's entries restate their governing rules on the same terms a row
does, and where such an entry and the rule it cites diverge, the rule governs there
too"). §21.7 is named in the very same sentence that limits the completeness clause —
"neither this completeness clause nor the instance arithmetic below reaches … §21.7's
account of what no check detects" — and is given **no** such tie-breaker. So a §21.7-vs-
§20.3 divergence has no stated resolution, and both texts are normative under
`[R-CNF-01]`. That is what makes C-01 and C-03 byte-level rather than editorial.

---

## 5. Does either bar owe a register row? — §21.1 applied

§21.1's completeness clause, verbatim (3554-3560):

> Its **completeness is normative** — a *detectable* file-conformance violation this
> specification names and the register omits is a defect in this document, detectability
> being the gate `[R-CNF-07]` already applies and §21.7 the account, by class, of what
> fails it

Applying it to each bar:

- **§14 bar.** A violation of it is a property of a *commit*, not a condition a single
  file exhibits. Where its effect surfaces (Case B), the file exhibits T3's condition and
  T14's — both already rows. There is no residue that is a detectable file condition and
  unregistered. **No row owed.**
- **Companion bar.** Same analysis, and the document already treats the neighbouring case
  identically: §21.7's untouched sentence at 3885-3891 gives `[R-GEO-06]`'s and
  `[R-SER-01]`'s ordinal mappings no row of their own, saying instead "a mis-ordered image
  is then witnessed by T2, T4 or T5". Case C's file exhibits T4; Case D's exhibits T3 and
  T14. All rows. **No row owed.**

There is a precedent for exactly this reasoning being made explicit: §16's Note on
`[R-SLB-04]` — "Because this rule's detection *is* `[R-SLB-03]`'s, a stale declaration
carries no register row of its own: every file exhibiting one exhibits a run whose tiles
are unpacked or whose first stored tile is misaligned, which §21.3 registers." The bars
stand in the same relation to T3/T4/T5/T14.

**Conclusion: no row is owed, and the counts stand.** Confirmed by recount below.

---

## 6. The recount

Script: parse every table row in the register subsections; a row's instance count is the
number of `;`-separated items in its Instances cell, and a cell reading `—` is one
instance (§21.1: "a cell reading — is one instance; the count is therefore mechanical
once the cell is written").

```
21.2  rows= 35   instances= 56
21.3  rows= 49   instances= 116
21.4  rows= 26   instances= 55
21.5  rows= 10   instances= 48
TOTAL rows 120   instances 275
```

Arithmetic: 35 + 49 + 26 + 10 = **120**. 56 + 116 + 55 + 48 = **275**.

Printed figures:

| Location | Printed | Derived | Verdict |
|---|---|---|---|
| §21.2 preamble | "35 conditions" | 35 | matches |
| §21.3 preamble | "49 conditions" | 49 | matches |
| §21.4 preamble | "26 conditions" | 26 | matches |
| §21.5 preamble | (no count stated) | 10 | n/a |
| §21.8 | "120 conditions over 275 instances" | 120 / 275 | **matches** |

Spot-checks of the mechanical count against §21.1's Instances rules, since a bad cell
would propagate: R4 = 16 (4 conditions × 2 containers × 2 = the cell lists 16 items,
counted); L1 = 8; L2 = 9; T3 = 6 (3 layout formulas × 2 magnitude directions — §21.1:
"Where the quantity a condition derives varies by layout, the layout formulas are
materially different shapes" and "Where the condition compares two **magnitudes** either
of which can be the greater … the two directions are likewise enumerated"); T14 = 6
identically; T22 = 6 identically; T21 = 3 (an *exceeds*: "larger than the tile's decoded
size" bounds the comparison in one direction, so no direction split — consistent);
T24 = 1 ("any codec", the §21.1 example). All consistent.

**Neither hunk disturbs the counts, and the counts are right.**

---

## 7. Findings

### C-01 — "the cases it does not reach": the pronoun makes §21.7 deny that the §14 bar reaches a re-typed channel

Check: LOCAL_CONTRADICTION. Location: §21.7, spec/tarn.md 3896-3901.

Quotation (repaired text): "§20.3 step 4's **§14 bar** is witnessed only where the
affected tiles remain stored, and then only for part of what it bars — a re-typed channel
among the cases it does not reach"

Contradicting text: §20.3 step 4, spec/tarn.md 3159-3162: "A channel's declared **sample
type** is such a declaration, and changing it is such a change wherever the layer stores a
tile that carries that channel". Corroborated non-normatively at §11.1's **Rationale.**
block, 1616-1618: "Re-typing a channel is the §14 bar's own subject, barred wherever the
layer stores a tile that carries that channel, and free where it does not."

Detail. The clause contains one pronoun, twice: "what **it** bars" and "the cases **it**
does not reach". The first is unambiguously the §14 bar. The second, by nearest-antecedent
resolution, is the same. On that reading §21.7 states, in normative text, that the §14 bar
does not reach a re-typed channel — the precise opposite of §20.3, which names re-typing as
the bar's paradigm case and spends five sentences on it. The intended referent is evidently
the *witnessing*, not the bar; but the sentence never introduces a noun for the witnessing
that "it" could pick up, and it re-uses the pronoun that four words earlier meant the bar.

Both readings are permitted. Under the bar reading an implementer concludes Case A's
commit is legal; under the witnessing reading it is illegal but undetected. §21.1 gives no
tie-breaker for a §21.7-vs-rule divergence (it supplies one for rows and extends it only to
§21.6, and the same sentence expressly says the completeness clause "does not reach …
§21.7's account of what no check detects"). Both texts are normative under `[R-CNF-01]`.

Byte-level: **yes.** Case A. Writer P (bar reading) emits generation 2 of layer L with `a`
re-typed `uint8`→`int8`, both tiles left stored and untouched. Writer Q (§20.3) refuses and
creates a new layer instead. P's file is conforming — no register row fires (verified row
by row in Case A) — so `[R-CNF-05]` does not bar it under either reading, and the set of
emittable files differs by exactly this file.

Repair: replace "a re-typed channel among the cases it does not reach" with a phrase that
names the witnessing rather than borrowing the bar's pronoun — e.g. "a re-typed channel
among the cases **no witness reaches**, though the bar reaches it" — or, better, fix the
substantive claim as C-02 requires and write "a re-typed channel that alters no length
among the cases no witness reaches".

### C-02 — the unqualified "a re-typed channel … does not reach" is falsified two sentences later by the repair's own example

Check: OVERCLAIM. Location: §21.7, 3897-3899 against 3913-3918.

Quotation: "a re-typed channel among the cases it does not reach"

Contradicting text (same insertion, 3913-3918, plus untouched 3918-3919): "Which case a
type change falls in is not decided by the element sizes of §12.1: a planar `uint8` channel
re-declared `bool` keeps its element size of 1 while its plane goes from P · Bᶜ bytes to
⌈P/8⌉." … "A change reaching the decoded size is witnessed by T3 or T14".

Detail. Read charitably ("the *witnessing* does not reach a re-typed channel"), the clause
is a class claim over re-typings and is false for every re-typing that changes the plane
length. The repair itself supplies the counterexample and states why: `uint8` → `bool`
takes a planar plane from P·Bᶜ to ⌈P/8⌉, which is a change reaching the decoded size,
which the very next sentence says T3 or T14 witnesses. Case B constructs the file. The
correct claim is narrower: a re-typing that alters no length and reaches no §14-constrained
byte is unwitnessed — which is Case A, and which is what "no check can know which type a
channel carried before" is actually about.

The asymmetry matters because the same sentence-pair treats the companion bar correctly
("witnessed indirectly and only sometimes") using the identical T3/T14 mechanism. One
sentence gives one bar an unqualified negative and its neighbour a hedge, for the same
detection mechanism.

Byte-level: **no.** On this reading the sentence makes a claim about detection, not about
permission; a verifier's obligation to apply T3 comes from `[R-SER-07]` and the row, which
this sentence does not touch. The bytes do not move on the charitable reading. (They move
on C-01's reading, which is why C-01 is filed separately.)

Repair: "a re-typing that alters no length and no byte §14 constrains among the cases no
witness reaches".

### C-03 — "escapes … the §14 bar" says a commit is not barred where §20.3 says it is

Check: LOCAL_CONTRADICTION (also the check-7 analogy failure). Location: §21.7, 3909-3913.

Quotation: "and a commit that supersedes every tile it would have damaged escapes them
exactly as it escapes the §14 bar."

Contradicting text: §20.3 step 4, 3148-3152: "The tense is the prior generation's (§3.1
defines *stored* against a generation), so **a commit does not escape this by unstoring in
the same breath: superseding every tile of a layer and re-declaring it are one operation,
and this bars it.**"

Detail. This is the same verb, the same subject, and the opposite predicate. "Escape" is
used across this document to mean *not being subject to a rule* — §20.3's own other use,
3206-3208: "`[R-COD-07]`'s lz4 decoded-size cap among them (L44), which an empty layer
**escapes** only because that cap is quantified over addressed tiles" — so the reading is
not strained.

The analogy is what carries the error. "Escapes **them**" (the rows) asserts non-detection;
a row is a check. "Escapes **the §14 bar**" asserts non-prohibition; the bar is
"A commit MUST NOT…". The *exactly as* transfers a true statement about checks onto a
prohibition, and the two governing verbs are "test"/"detect" against "MUST NOT". Tested
against each row the sentence carries the analogy for — T3, T14, T2/T4/T5, T15/T17/T23/T25
— it holds for every one; it fails only for the member named as its warrant.

The document supplies the correct formula twice. §20.3, 3241-3243: "§21.7 records the
consequence — that **this is precisely where the §14 bar has no witness**, the live state
being clean". And hunk 8's own sentence 20 lines below: "so the §14 bar is **unwitnessed**
there". The insertion and the pre-existing sentence therefore state the same fact about the
same case in the same paragraph with different force — which is also why this is an
unswept restatement: hunk 7 added a second account of a case the paragraph already
covered, and hunk 8 then carefully disambiguated only the older one.

Byte-level: **yes.** Case F. Writer P emits a commit that supersedes every stored tile of
layer L while re-typing a channel; writer Q refuses and creates a new layer. P's output is
a conforming file — its live state is clean by the paragraph's own admission ("leaves the
live state clean") — so `[R-CNF-05]` bars neither reading from the emittable set, and the
two writers put different bytes on disk from offset F onward.

Repair: "…escapes them, and the §14 bar has no witness there either" — dropping "escapes"
in the second position entirely. Or delete the clause and let the paragraph's existing
sentence at 3933-3936 carry the case, which it already does correctly.

### C-04 — "disturbs nothing a row can see" is false wherever the permuted channels' fills differ

Check: OVERCLAIM (and LOCAL_CONTRADICTION with untouched text in the same paragraph).
Location: §21.7, 3906-3908.

Quotation: "a permutation among channels whose planes are the same length disturbs nothing
a row can see"

Contradicting text: §21.7 itself, untouched, 3885-3891: "the ordinal mappings of
`[R-GEO-06]` and `[R-SER-01]` are satisfied by a structurally valid tile whatever values it
carries, **except where §14 constrains a byte's content** — a padding position, a pad bit,
or an interleaved boolean — **and a mis-ordered image is then witnessed by T2, T4 or T5**".

Detail. Case C constructs it: a planar layer with padding positions and two `uint8`
channels of differing recorded fill. Their planes are the same length, so the repair's
stated condition is met. Exchange them; step 4's re-emission rule keeps every entry
byte-identical at its disk-ordinal position (a channel permutation is not a geometry
change, and §20.3 names a geometry change as the only occasion for renumbering). The plane
now read as channel `b` carries `a`'s fill in its padding positions. `[R-SER-05]`: "at
every padding position, a writer MUST encode, for each channel the position carries, that
channel's fill value … a verifier MUST check it, and a violation is a validity error at
tile scope." **T4** fires — instance `planar numeric plane fill bytes`. With two `bool`
channels of differing fill bit, **T5** fires instead. Both are rows; both can see it.

The claim is true only under two unstated conditions: the permuted channels' recorded fills
coincide, or the layer has neither padding positions nor pad bits. The document elsewhere
states exactly this carve-out for exactly this mechanism, three sentences earlier, which is
why I rate it CONFIRMED rather than a matter of judgement.

Byte-level: **no.** The file in Case C exhibits T4's condition, a registered violation, so
`[R-CNF-05]` bars every conforming writer from emitting it under both readings, and the
verifier's obligation to check padding content comes from `[R-SER-05]` and T4, which this
sentence does not amend. The emittable set does not move; the sentence is false rather than
permissive. (It would mislead a verifier author into skipping a check `[R-SER-05]` makes a
MUST, which is a real cost, but not one that forks the conforming set.)

Repair: "a permutation among channels whose planes are the same length and whose recorded
fills agree disturbs nothing a row can see — where the fills differ, the padding positions
and pad bits of §14.5 do, and T4 or T5 sees it".

### C-05 — the companion-bar account covers permutations only; §20.3's bar equally reaches channel insertion and removal

Check: UNDERSHOT (check 6). Location: §21.7, 3901-3909.

Quotation: "Its companion bar on a planar layer's disk ordinals is witnessed indirectly and
only sometimes … a permutation among channels whose planes are the same length disturbs
nothing a row can see, while one that leaves a plane of one length at an ordinal the new
declarations size differently is caught by T3, or by T14 under codec 1."

Contradicting/omitted text: §20.3 step 4, 3182-3187: "A channel's tiles move exactly when
its index does: **reordering** moves those channels the reorder re-indexes, and
**inserting or removing one** moves every channel after the affected position. **Either**
is such a change wherever the layer stores a tile for a channel that moved."

Detail. The structure the repair governs is the companion bar's subject: changes to a
planar layer's channel declarations that move a stored tile's disk ordinal. §20.3 names two
members. §21.7 accounts for one — permutation — and then partitions *that* one exhaustively
into two cases. Insertion and removal at a non-terminal position are the sibling member,
they are barred on identical terms, and §21.7 says nothing about whether they are
witnessed. They are not the same case: they change C, hence the addressed-tile count C·N
(§11.2) and hence entry_count, so an offending commit is measured against a different row
family (L21's `planar C·N, entry_count larger` / `smaller` instances) as well as T3/T14,
and the ordinal displacement is a uniform shift by N rather than a swap. A reader working
out whether the register owes a row for a mid-list channel insertion gets no answer here.

The same shape recurs one level up. The paragraph's stated criterion is "A second set of
obligations is omitted from the register because a single file exhibits no witness of their
violation", and this repair converted a vague singular ("step 4's bar on a declaration
change") into an enumeration of step 4's bars. Step 4 carries at least two further
obligations meeting the same criterion and enumerated nowhere: "every other entry
byte-identical at its disk-ordinal position" (3128-3129, with step 2's "not repaired to a
sentinel" at 3086-3087), and "A layer whose record alone changes keeps its extent slot …
relocating a live index region is compaction's operation (§20.5, `[R-WRT-07]`), not an
appender's" (3130-3136). A file violating either is structurally perfect. The document
hedges open lists explicitly when it means to — "not offered as exhaustive" (1 hit),
"not offered as closed" (2 hits) — and §21.7 carries no hedge, while §21.1 calls it "the
account, by class, of what fails it". "By class" may be doing that work, which is why I
mark this PLAUSIBLE rather than CONFIRMED.

Byte-level: **no.** The omission licenses nothing; §20.3's MUST NOTs stand for insertion,
removal, and the carry-forward obligations whether or not §21.7 mentions them.

Repair: extend the sentence to the bar's whole subject — "a **reordering** among channels
whose planes are the same length … while a reordering that leaves a plane of one length at
an ordinal the new declarations size differently, or an insertion or removal that shifts
one there, is caught by T3, or by T14 under codec 1" — and, separately, decide whether
§21.7's list is closed and say so.

### C-06 — "the rows below … on the terms they state there": the rows are above, and "below" and "there" point in opposite directions

Check: NEW_AMBIGUITY. Location: §21.7, 3909-3911.

Quotation: "Where the change does touch something §14 fixes, the rows below reach it on the
terms they state there and no better"

Contradicting text: §21.5's preamble, spec/tarn.md 3778-3780, the document's only other use
of the phrase: "every way its document can be unreadable takes this outcome, whatever the
containing scope — as a violation in **the rows below**" — where the rows genuinely are
below, in the table that follows on the next line.

Detail. §21.7 begins at line 3862. The register's rows occupy §21.2-§21.5, lines 3626-3808:
they are 90 to 280 lines **above**. §21.7 contains no table. Two readings: "the rows below"
means "the rows named later in this paragraph" (T3, T14, T2/T4, T15/T17/T23/T25 are indeed
named below), or it means the register, misdescribed. The second half of the same clause —
"on the terms they state **there**" — is a locative pointing away from "below", which is
the tell: a row states its terms in the register, not later in this paragraph. Whichever
was meant, the sentence uses two locatives for one referent and one of them is wrong.
Sweep run: `"rows below"` → 2 hits, both quoted above.

Byte-level: **no.** Both readings pick out the same rows in the end.

Repair: "the rows of §21.2 through §21.5 reach it on the terms they state and no better".

### C-07 — "Which case a type change falls in": the nearest "cases" are the permutation dichotomy, which is not about type changes

Check: NEW_AMBIGUITY (check 8, backwards). Location: §21.7, 3913-3918.

Quotation: "Which case a type change falls in is not decided by the element sizes of §12.1:
a planar `uint8` channel re-declared `bool` keeps its element size of 1 while its plane goes
from P · Bᶜ bytes to ⌈P/8⌉."

Contradicting text: the nearest antecedent, §21.7 3906-3909 (inserted in the same hunk):
"a permutation among channels whose planes are the same length disturbs nothing a row can
see, while one that leaves a plane of one length at an ordinal the new declarations size
differently is caught by T3, or by T14 under codec 1."

Detail. The insertion orders its material bar-first: §14 bar, then companion bar and its
two-case split, then a sentence about what "the change" does when it touches §14, then
"Which case a type change falls in". The only place the word *case* has been given a
partition is the companion bar's permutation dichotomy two sentences back — and a type
change is not a permutation and does not move ordinals at all (§20.3: "a disk ordinal is
c · N + s, and N is the spatial-tile count, so the channel count enters the addressed-tile
count C · N (§11.2) but no individual ordinal"). The intended antecedent is the
touches-§14 / does-not-touch dichotomy of the preceding sentence, one further back and
never called a "case". A reader who resolves to the nearest partition concludes the
sentence is telling them how to classify a type change as a permutation, which is
incoherent, and may re-read the ordinal bar as reaching type changes.

Before the insertion this sentence did not exist, and the untouched sentences that follow
it ("A change reaching a byte §14 structurally constrains…") attached directly to the §14
bar with one bar in play; they now attach to a type-change example sitting behind 15 lines
about a second bar.

Byte-level: **no.** No reading changes an obligation; the sentence's substantive content
(element size does not determine plane length for bool) is correct and verified against
§12.1 and §14.3.

Repair: move the sentence to sit immediately after the §14-bar clause it belongs to, and
name its partition: "Whether a type change touches something §14 fixes is not decided by
the element sizes of §12.1: …".

---

## 8. Candidates opened and dropped

1. **"§20.3 step 4's §14 bar"** — does §20.3 actually name it that? Opened 3141-3147:
   "Call this the **§14 bar**." Dropped: the name is the document's own.
2. **"Its companion bar"** — §20.3 never says *companion*; it says "One effect is barred
   beside it" and "The bar beside the §14 bar". Dropped: a third informal name for an
   unnamed bar is a style matter, the referent is unambiguous, and no rule turns on the
   word. Also "Its" grammatically picks up "the §14 bar", giving "the §14 bar's companion
   bar", which is true.
3. **Does the companion bar being "witnessed … only sometimes" break §21.7's own opening
   criterion** — "omitted from the register because a single file exhibits no witness of
   their violation"? Dropped as pre-existing, not introduced: the untouched text already
   lists `[R-GEO-06]`/`[R-SER-01]` with "a mis-ordered image is then witnessed by T2, T4
   or T5", and the pre-hunk §14-bar sentence already said "witnessed only where the
   affected tiles remain stored". The paragraph's list has always held partly-witnessed
   members.
4. **Is a register row owed for either bar, and are the counts therefore wrong?** Opened;
   applied §21.1's completeness clause; found the detectable residue is in every case
   already T3/T14/T4/T5, exactly as §16's Note reasons for `[R-SLB-04]`. Recounted anyway:
   120 conditions, 275 instances, matching §21.8 and the three per-subsection figures.
   Dropped.
5. **Could a same-length permutation also break a slab invariant (L41, L42)?** Opened
   §16 and the rows. Dropped: the entries are re-emitted byte-identical at their
   disk-ordinal positions, so the offset/length sequence read by ordinal is unchanged and
   `[R-SLB-03]`'s packing relation sees exactly what it saw before. Not a witness.
6. **"caught by T3, or by T14 under codec 1" — does it under-name the catchers?** Under
   codec 3 a plane of the wrong size would also trip T21 or T22. Dropped: the sentence uses
   "or" and claims sufficiency, not exhaustiveness, so no completeness word is at risk.
7. **Does the untouched "A change reaching…" series now mis-scope to the companion bar?**
   Opened; each member checked. "byte §14 structurally constrains", "the codec", "the
   filter" cannot arise from the companion bar (it moves ordinals, it does not alter a
   stored tile's bytes — §20.3: "an ordinal move being no effect on any stored tile's
   bytes"); "the decoded size" is shared, and the insertion itself already assigns T3/T14
   to the companion case, so the two accounts agree. Dropped as recorded-but-benign.
8. **Did hunk 8 undershoot — are there other bare "the bar" references left in §21.7?**
   Swept: `"the bar"` → 9 hits document-wide, none in §21.7. Dropped; hunk 8 is complete
   for what it set out to fix.
9. **Do the hunk headers' stated landing lines and nearest heading match the body?**
   Checked both: 3896 and 3935 are the first changed lines, and 3862 is `#### 21.7 What no
   check detects` for both. No mismatch. Dropped.

## 9. Sweeps run, verbatim, with hit counts

Whitespace-normalised over the whole file (the document is hard-wrapped, so these were run
against `re.sub(r'\s+',' ', text)`, not line-oriented):

```
"the bar"                      →  9 hits
"rows below"                   →  2 hits
"not offered as exhaustive"    →  1 hit
"not offered as closed"        →  2 hits
"§14 bar"                      → 11 hits
"companion"                    →  1 hit
"escapes"                      →  4 hits
"escape this"                  →  1 hit
"unwitnessed"                  →  3 hits
"disturbs nothing"             →  1 hit
"which case"                   →  1 hit  (§20.3 step 1, unrelated; the §21.7 one is
                                          capitalised "Which case" and so not matched —
                                          noted, and confirmed by eye at 3913)
"the cases it does not reach"  →  1 hit
```

Line-oriented (safe, short, cannot wrap):

```
grep -n "20.3"            → 12 hits
grep -n "R-CNF-05|R-GEO-06|R-SER-01]"  → 20 hits
grep -n "R-SLB-03"        →  7 hits
grep -n "Of its"          →  1 hit  (§11.1 Rationale, line 1605)
grep -n "^| L39|^| L40|^| L41"         →  3 hits
awk '/`\[R-LIF-01\]`/'    → 10 hits
awk NR 3862..3950 /^>/    →  0 hits  (§21.7 has no blockquote)
```

## 10. Confidence

I ran all eight checks against both hunks. Checks 2 and 3 pass cleanly and I say so
above with the evidence. Check 1 passes on tense and fails on quantifier range twice.
Checks 4, 5, 7 and 8 each produced a finding. Check 6 produced C-05.

Hunk 8 is a good repair: it fixes a referent that hunk 7 made ambiguous, it names the
right bar (corroborated by §20.3's own forward reference at 3241-3243), and the sweep for
other bare "the bar" references in §21.7 comes back empty. I have no finding against it
except that it disambiguated the *older* of two sentences about the same case while
leaving the newer one (C-03) saying something stronger and wrong.

Hunk 7 is where the defects are, and they cluster in the two sentences that carry the
insertion's new claims: the re-typing clause and the "escapes the §14 bar" clause. Two of
the seven findings fork the bytes, and both do so the same way — a sentence in §21.7 that
was meant to describe non-detection instead describes non-prohibition, in a document
where §21.7 is normative and no precedence rule settles it against §20.3.
