# Repair audit — lane "the-test" — hunks 07, 08, 09

## 0. Disclosure

Read, in full or in the ranges named:

- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-preaudit/case/hunk-07.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-preaudit/case/hunk-08.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-preaudit/case/hunk-09.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` — lines 95-115, 195-300, 465-480, 685-760, 860-875, 1067-1180, 1140-1180, 1222-1240, 1375-1396, 1440-1480, 1728-1775, 2020-2058, 2087-2130, 2305-2325, 2405-2425, 2496-2545, 2600-2620, 3160-3262, 3340-3420 (via the 20.4 section pull), 3440-3465, 3540-3780, 3810-4010; plus §20.4 and §20.5 pulled whole by sed range.

Commands run: `wc -l`, `sed -n`, `grep -n`, `grep -c`, `grep -o`, and one inline `python3` heredoc that read only `spec/tarn.md` and printed whitespace-normalised substring counts. No file was written under the repository. No scratch file was created (the python was a heredoc; the scratch dir
`/private/tmp/.../scratch/the-test/` was created by `mkdir -p` and left empty).

I did NOT read: `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`, `spec/registry.json`, `full.diff`, any other hunk file, git history, or the web. I did not list the case directory.

**Context I did not ask for.** Material appeared in my context before I began: a project instruction file pointer (CLAUDE.md → AGENTS.md), and an index of the maintainer's auto-memory naming several notes about this project's cadence, register, and prior workflow failures. I did not open any of those files and I have not used their contents. One line of my charter briefing describes §21.7's test as speaking of "two files presenting identical live states"; §21.7's actual test speaks of checks, not live states, and §21.1's does speak of live state. I noticed the mismatch only after deriving finding A-01 from the two passages independently, and I record it here rather than treating it as evidence.

---

## 1. The rule each repair adopts, in my own words

**Hunk 07 (§21.1, line ~3560).** Replaces the pointer "§21.7 the account, by class, of what fails it" with a pointer plus an inline statement of the test: a violation is detectable iff **some** file exhibiting it **differs in its live state** from **every** file that does not. What it makes true of an implementation: an implementer can now decide, without leaving §21.1, whether an omission from the register is a document defect — by comparing live states.

**Hunk 08 (§21.1, line ~3580).** Pure renaming: "§21.7's account of what no check detects" → "§21.7's test for what no check detects". Makes nothing new true of an implementation; it re-describes §21.7's character to match hunk 09.

**Hunk 09 (§21.7, lines ~3882-3994).** Replaces a 926-word inventory with (a) a normative definition of **unwitnessed** and its negation **detectable**, quantified over files and instrumented by "any check this specification obliges a reader or a verifier to perform"; (b) a normative statement that the register carries a row for a condition *exactly where* it is detectable; (c) a normative statement that the subject is the condition, not the requirement, and that being unwitnessed bears on detection, not permission; (d) a normative carve-out for a requirement that states no condition a file can exhibit (`[R-ENC-06]`); and (e) the old inventory, plus new material on §20.3 step 4's companion ordinal bar and on §12.1 element sizes, moved into a block labelled **Rationale.** What it makes true of an implementation: an implementer can classify any named condition from first principles instead of consulting a list, and the list itself now binds nothing.

---

## 2. Check 3 first — where does each repair sit, and what is the block's label?

I applied the **label** test from `[R-CNF-01]` (line 104-106), quoted: "All text in this document is normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices identified as non-normative."

- Hunk 07's text sits at spec/tarn.md:3557-3563, in the running paragraph of §21.1. No `>` marker, no label. **Normative.**
- Hunk 08's text sits at 3580, same paragraph family. No marker, no label. **Normative.**
- Hunk 09's items (a)-(d) sit at 3882-3919. No `>` marker, no label. **Normative.** Item (e) sits at 3921-3994; every line begins `> ` and the first two words are `**Rationale.**`. **Non-normative by label.**
- §21.6 (3810-3862) — its table and both prose blocks carry no `>` and no label. **Normative.** This matters for A-02.
- §7.4's closing block (1169-1178) begins `> **Note.**`. **Non-normative.**
- §14.3's block at 2035-2042 begins `> **Note.**`. **Non-normative** (I used it only as a factual cross-check, and re-derived its content from `[R-SER-03]` and §11.3 which are normative).

**Does anything the rest of the document need now sit inside the Rationale?** I traced every inbound pointer to §21.7:

| Site | Text | Label at the citing site | Does it depend on the Rationale? |
|---|---|---|---|
| 2521 (`[R-COD-10]`) | "the consequence is wrong sample content — undetectable by construction (§21.7)" | normative | No — supported by §21.7's normative opening paragraph (3866-3880) |
| 2613 (§17.2 zstd) | "a writer violation nothing in the extent shows, exactly as `[R-COD-06]` has it for a tile (§21.7)" | normative | No — same opening paragraph |
| 3240-3242 (§20.3 step 4) | "§21.7 records the consequence — that this is precisely where the §14 bar has no witness, the live state being clean" | normative | The *record* is now non-normative, but §20.3's own sentence asserts the substance normatively and the new test derives it. No loss. |
| 3457 (§20.5 / `[R-WRT-06]`) | "Neither obligation has a witness in the output alone (§21.7)" | normative | Same — §20.5 asserts it itself; the test derives it. No loss. |
| 3774 (T26, register row) | "a wrong stride with no such structural constraint is undetectable, §21.7" | normative table row | No — opening paragraph |
| 1170 (§7.4) | "no reader-detectable witness, and so no register row" | **Note** | Non-normative both ends; see A-05 |

**Verdict on check 3: the relocation into a Rationale did not orphan any normative dependency.** Every inbound citation is either served by §21.7's still-normative opening paragraph or restates its own substance in place. This is the direction of check 3 I expected to fail and it passes.

The opposite direction — did a repair edit a labelled block while the normative statement elsewhere still says the old thing? — also passes: the whole of the new test is in unlabelled text, and the whitespace-normalised sweeps in §5 show each of its distinctive phrases occurring exactly once.

---

## 3. Check 1 — tense and quantifier; and check 7 — the analogy

### 3.1 The two statements of the test, side by side

§21.7 (3882-3888), normative:

> "A condition this specification names is **unwitnessed** where, for every file exhibiting it, some file that does not exhibit it cannot be told apart from it by any check this specification obliges a reader or a verifier to perform. It is **detectable** in the contrary case: where some file exhibiting it **is separated by such a check** from every file that does not."

§21.1 (3559-3563), normative, inserted by hunk 07:

> "detectability being the gate `[R-CNF-07]` already applies and **§21.7 states the test for**: a violation is detectable exactly where some file exhibiting it **differs, in its live state,** from every file that does not"

Governing verbs, quoted, not paraphrased:

- §21.7: **"is separated by such a check"** — where "such a check" resolves to "any check this specification obliges a reader or a verifier to perform".
- §21.1: **"differs, in its live state,"** — no check named, no actor named, no obligation named.

Quantifier structure is identical in both (∃ a file exhibiting it, ∀ files that do not). **The predicate is not.** Separation-by-an-obliged-check entails difference-of-live-state; difference-of-live-state does not entail separation-by-a-check. §21.1's version is therefore strictly the wider test, and §21.1 presents it under the warrant "§21.7 states the test for" — the analogy fails at exactly the point check 7 asks about.

§21.7 is explicit that the instrument is the load-bearing part, at 3897-3902: "The instrument is the checks this specification obliges an actor to perform, and deliberately not the register's own rows — a test keyed to the rows would make §21.1's completeness clause vacuous". §21.1 substitutes a third instrument the section never contemplates.

### 3.2 Does the divergence bite? A worked counterexample

I need a condition that (i) produces a difference in the live state and (ii) no obliged check reads.

**`[R-CNT-18]`'s prohibition on a sub-record containing records.** The §21.7 Rationale itself classifies it as unwitnessed: "detectable only by parsing a payload no format-major-1 reader parses as a record sequence (§7.4's closing Note)" (3941-3943). §7.4's Note (1169-1178) confirms no reader parses it, and `[R-CNF-11]` makes verifiers readers ("Verifiers and updaters are readers of the files they process and inherit every reader obligation"), so no verifier parses it either. Under §21.7's test: **unwitnessed.**

Now apply §21.1's test. "Live state" is fixed by `[R-CNT-02]` at 685-694: "the front signature block, and every structure reachable from the live trailer through the live directory's records, extent slots, and tile-index entries, together with the live directory and the live trailer". A sub-record's inline payload lies inside the directory region, which §9.7 names as a claimant (1449-1452). So the payload bytes are part of the live state.

Take f = a conforming-looking file whose unknown-type MU=0 sub-record's payload is a valid record sequence. Take any g that does not exhibit the condition. If g's live state were identical to f's, g would carry the same payload bytes at the same place, and that payload *is* a record sequence — so g would exhibit the condition. Contradiction. Hence f differs in live state from **every** g that does not exhibit it. Under §21.1's test: **detectable.**

§21.1's completeness clause is normative and says "a *detectable* file-conformance violation this specification names and the register omits is a defect in this document". Under §21.1's own wording, the register's omission of the nesting condition is a defect in the document; under §21.7's wording it is exactly what the clause's terms require. **The two normative passages give opposite verdicts on the same condition.**

I checked whether the divergence is an artefact of my choice: it is not. It bites for any condition that is a genuine byte-property of a claimed structure and that no obliged check reads. It does **not** bite for the content-wrongness class (`[R-COD-10]` mis-stride, `[R-COD-06]` undisclosed dictionary, `[R-MTA-09]` wrong document content, plain wrong data): those conditions are not fixed by the bytes at all — a legitimate writer could have produced byte-identical output — so no file exhibiting them differs in live state from every file that does not, and both tests agree they are unwitnessed. Likewise `[R-LIF-01]`, `[R-LIF-02]`, `[R-WRT-06]`'s three: all history properties, both tests agree.

This is **A-01**.

### 3.3 The other analogy in hunk 09

"**The subject is the condition and not the requirement**, as `[R-CNF-13]` individuates them and as `[R-CNT-06]` shows by stating nine."

- `[R-CNF-13]`'s verb: "A **condition** this specification names — one malformed state, **as §21.1 individuates them**, and not the requirement that defines it". So `[R-CNF-13]` does draw the condition/requirement distinction (passes), though it delegates individuation onward to §21.1; §21.7 credits `[R-CNF-13]` with individuating. Circular but not false.
- `[R-CNT-06]`'s warrant: `[R-CNF-13]` says "`[R-CNT-06]` states nine, of which the trailer magic and the trailer CRC assert invariants `[R-CNT-24]` fixes and the other seven do not." I verified the nine mechanically (§6 below). Passes.
- Note the scope: `[R-CNT-06]` warrants only "a requirement can state several conditions". The **next** sentence ("A single requirement states conditions of both kinds") is a different claim, and `[R-CNT-06]` does not warrant it — all nine of its conditions are registered, hence all detectable. I checked whether the claim is nonetheless true and it is: `[R-CNT-13]` governs F2, F3, F30, F31, F32, F33 (detectable) and also states the MU=0 offsets-in-payload prohibition the Rationale classifies as unwitnessed. So the claim survives; only the placement of the citation is loose. Not filed as a finding — recorded in rejected candidates.

### 3.4 "The two are stated over the same subject and with matching quantifiers, so each is exactly the negation of the other"

Conclusion true; warrant false. Writing U = ∀f∈Exh ∃g∉Exh ¬sep(f,g) and D = ∃f∈Exh ∀g∉Exh sep(f,g), ¬U = ∃f∈Exh ¬∃g∉Exh ¬sep = ∃f∈Exh ∀g∉Exh sep = D. They are exact negations **because the quantifiers are dual, not because they match**. If the quantifiers actually matched — both ∀∃ or both ∃∀ — the two would not be negations. The sentence offers as its reason the very thing that would defeat it. This is **A-06**; minor, but it is a warrant sentence in a definition the section calls load-bearing, and a reader who trusts it will mis-transcribe the test.

(I also checked the empty-extension edge: if no file can exhibit the condition, U is vacuously true and D vacuously false, so ¬D = U still holds. The negation claim survives that case.)

---

## 4. Check 4 — contradiction in the same passage, including untouched text

### 4.1 §21.7's new biconditional against §21.6

Hunk 09, 3890-3894, normative:

> "The register carries a row for a condition **exactly where** it is detectable, so an unwitnessed condition is absent from it by that clause's own terms rather than in breach of them."

§21.6 (3810-3862), normative, immediately above, and untouched by this repair:

> "Two structural cases are **conforming files a reader nevertheless refuses**. The first is **version_major naming a major this reader does not implement**: the reader rejects the file (`[R-CNT-07]`)... The second is an **experimental-range top-level record type carrying MU = 1** (§10.2, §10.3): `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]` makes the file conforming all the same. ... **Neither is a register row**: the register enumerates file-conformance violations (§21.1), and a file this document declines to judge is not one."

Put §21.7's test to those two cases. Take f = a file declaring version_major 7, and any g declaring 1. `[R-CNT-07]` **obliges** the reader to reject f and not g: an obliged check separates f from every g that does not exhibit the condition. Under §21.7's own definition, f's condition is **detectable**. Same for the experimental MU=1 top-level record: `[R-CNT-15]` obliges rejection. Both are detectable; **neither has a row**; §21.7 says a row exists exactly where detectable. Direct contradiction with a normative passage four lines above the insertion.

§21.6's fourteen table rows are worse still, because §21.6's own column heading is **"Condition"**. "An index entry is the sentinel", "A dimension has extent 0", "version_minor is higher than this text defines" — every one is a condition this specification names, every one is observable, none has a row.

The escape route is that `[R-CNF-13]` defines "condition" narrowly as "one malformed state", so §21.6's entries would not be conditions in the technical sense. But (i) §21.6 uses the word contrarily, in a normative section heading and a normative table column, and (ii) the escape does not save the two reader-refusal cases, because those turn on whether "detectable" is satisfied, not on whether the file is malformed — and a reader is *obliged* to reject, which is precisely §21.7's instrument.

§21.1's parallel clause is careful where §21.7's is not. §21.1 says "a *detectable* **file-conformance violation** this specification names and the register omits is a defect", and hunk 08's own sentence at 3578-3580 says "neither this completeness clause nor the instance arithmetic below reaches §21.6's defined non-violations". §21.7's new sentence dropped the qualifier §21.1 keeps. The minimal repair is to restore it: "The register carries a row for a **file-conformance violation** exactly where it is detectable."

This is **A-02**.

I also note that under the second available reading of "told apart by a check" — the check's *verdict* differs, rather than the check *observes* a difference — the sentinel and the extent-0 dimension come out **unwitnessed**, a word §21.7's own heading glosses as "what no check detects", even though `[R-IDX-02]` obliges a reader to read the sentinel and return fill. The test does not say which reading applies, and the two give opposite classifications for §21.6's table. That ambiguity is part of A-02.

### 4.2 §20.3 step 4, read whole

I read 3160-3262 in full, looking for a carve-out the repair's new breadth collides with. Findings:

- §20.3 states two bars. The §14 bar (a commit MUST NOT alter what §14 fixes for a tile stored in the superseded generation) and, at 3174-3186, the companion: "For a **planar** layer, a commit MUST NOT change the channel declarations in a way that alters the disk ordinal `[R-GEO-06]` assigns any tile the layer stores in the generation this commit supersedes." §20.3 is explicit that the two are distinct: "the §14 bar does not reach it, an ordinal move being no effect on any stored tile's bytes".
- The old §21.7 text said only "§20.3 step 4's bar on a declaration change", which was ambiguous between them. The repair disambiguated to "**§14 bar**" in both places (3944, 3985) and added the companion. **That is a genuine repair of an anaphor and it lands correctly.** I checked both occurrences.
- §20.3's tense: "the generation this commit supersedes", and "the tense is both bars'". The Rationale's new sentence adopts the same tense — "the prior generation's declarations are not part of the live state" and "no check knows which ordinal a stored tile used to occupy". **Tenses agree.** No check-1 defect here.
- No MUST in §20.3 is loosened, and no MAY widened, by anything in hunk 09: hunk 09 says nothing about permission at all, and says so ("Being unwitnessed bears on detection and not on permission").

### 4.3 §20.5 "Neither obligation" against the Rationale's "three obligations"

§20.5 at 3457: "Neither obligation has a witness in the output alone (§21.7)." The Rationale at 3986-3990 names **three**: the fresh `file_id` draw, the ignore-lane carry-forward, the version_minor floor. I checked whether this is a count contradiction. It is not: §20.5's "Neither" is local to the two obligations stated in that paragraph (ignore-lane carry-forward, version_minor floor); the fresh `file_id` MUST is stated much earlier in §20.5 ("It MUST mint a fresh file_id for the output"). The Rationale's "For the last two there is a second [reason]" matches §20.5's pairing exactly. **No finding.**

---

## 5. Check 5 — exhaustive claims

Every completeness-promising word in the repaired text, and what I did with it:

| Claim | Where | Verdict |
|---|---|---|
| "**every** file exhibiting it" / "**every** file that does not" | 3883, 3886 | Correct; they are the dual quantifiers the negation needs |
| "**any** check this specification obliges a reader or a verifier to perform" | 3884-3885 | Passes for the actor set: `[R-CNF-11]` makes verifiers and updaters readers, so reader ∪ verifier covers every checking actor the document names |
| "each is **exactly** the negation of the other" | 3888-3889 | True; warrant false — **A-06** |
| "the register carries a row for a condition **exactly where** it is detectable" | 3890-3892 | **False** against §21.6 — **A-02** |
| "That is the **whole** of the test, and it decides **any** condition put to it without appeal to a list" | 3895-3896 | Survives for violations; fails for §21.6's conditions — folded into A-02 |
| "**every** omitted condition being undetectable by construction" | 3902 | Correct as a reductio of the rejected alternative |
| "`[R-CNT-06]` shows by stating **nine**" | 3905-3906 | Verified — see §6 |
| "**no** condition a file can exhibit" | 3913-3914 | Consistent with `[R-ENC-06]`, though see rejected candidates |
| "**Nothing** is omitted from the register on its account" | 3917-3918 | Follows from the preceding sentence |
| "**The** obligations this test places outside the register, as the document stands" | 3922-3923 | **Presented as closed and is not** — **A-04** |
| "a permutation ... **disturbs nothing a row can see**" / "**Where the fills differ**, ... T4 or T5 sees it" | 3952-3958 | **False** for a layer with no padding positions — **A-03** |
| "a violation is detectable **exactly where** ..." | 3561 | The biconditional is the wrong one — **A-01** |
| "both filter values are length-preserving (§17.3)" | 3981-3982 | Verified: `[R-COD-09]` admits only 1 and 2; §17.3 says of filter 2 "Length is unchanged"; filter 1 is none. **Passes** |

### A-03 worked out

The inserted sentence at 3952-3958 offers a trichotomy for a planar disk-ordinal permutation: same-length planes with agreeing fills → nothing sees it; different-length planes → T3, or T14 under codec 1; fills differ → "§14.5's padding positions and §14.3's pad bits carry the wrong channel's fill and T4 or T5 sees it."

Counterexample, decidable from the document. `[R-GEO-04]` (§11.3, 2 lines from the heading): padding positions arise only "Where Eᵢ mod Tᵢ ≠ 0 — equivalently, where the grid overhangs the extent". `[R-SER-03]` (§14.3): pad bits exist only "when P mod 8 ≠ 0", and only in a **packed planar bool** plane.

Construct: a planar layer, rank 1, E₀ = 64, T₀ = 64 — no overhang, therefore **no padding positions anywhere in the layer**. Two `uint8` channels `a` (recorded fill 0x00) and `b` (recorded fill 0xFF). Both planes are P·Bᶜ = 64 bytes — same length. Swap `a` and `b` in the channel declarations; the stored tiles do not move. Fills differ, so we are in the sentence's third case. But: T4's instances are all padding-position fills, and there are none; T5 needs a packed bool plane, and there is none; T3 sees 64 = 64; T14 sees 64 = 64. **No row sees it.** The sentence's third case is false here, and the trichotomy is not exhaustive — there is a fourth case (same length, fills differ, no padding positions and no pad bits) in which nothing witnesses the change.

The block's umbrella hedge — "witnessed indirectly and only sometimes" — remains true, so this is a defect in the enumeration and not in the umbrella. The block's own charter ("an item found stale is a defect in this block") makes it a defect in the block.

### A-04 worked out

Lead-in, 3922-3923: "**The** obligations this test places outside the register, as the document stands." Definite article plus "as the document stands" reads as the complete set. The old text's opener was the indefinite "A second set of obligations is omitted from the register because...". The repair upgraded a partial list into a claimed-complete one without adding the missing members.

Obligations the test places outside the register that the walk-through does not list:

1. **§20.4's preservation obligations** (`[R-WRT-05]`'s byte-identical re-emission; the MU=0/PE=1 "Retain byte-identical" row; the appender's bar on dropping an MU=0/PE=0 record outside an independently-changing commit; `[R-WRT-08]`). A file gives no witness of which records its superseded directory carried. §20.4's own Rationale says so, at 3390-3398: "the live state names one generation, and two trailers of one file_id are ordered by committed_file_length without being counted, so nothing in either says how many commits separate them. Adjacency is a fact about a file's history, which §9.7 does not reconstruct". That is *verbatim the same ground* the walk-through gives for `[R-LIF-01]`/`[R-LIF-02]` — "properties of a file's history, which §9.7 does not reconstruct" — and it is not listed. I checked the register for a proxy row and found none: F25 registers the MU=1/PE=0 flag *combination*, not a dropped record.
2. **`[R-CNT-03]`'s zeroing SHOULD.** "Writers SHOULD zero the gaps they create... no conformance requirement rides on slack content either way" (761-766). Slack is not part of the live state (`[R-CNT-02]`), and no obliged check reads it, so a writer that skips it is unwitnessed on both tests. Not listed.
3. **`[R-SLB-04]`'s staleness element** (2314-2320's Note: "a stale declaration carries no register row of its own"). The staleness itself is a prior-generation property; the invariant failure it causes is registered. The test decides this one correctly, which makes it exactly the sort of item the walk-through exists to display. Not listed. (Weaker than 1 and 2, since its detection is another row's.)

One omission would be enough. Two independent ones make the closed-set framing untenable.

---

## 6. Check 2 — every citation opened

| Citation in repaired text | What the repair claims | What it says | Verdict |
|---|---|---|---|
| `[R-CNF-07]` (3560, 3890) | detectability is the gate it applies in assigning an outcome | line 285-288: "Every **detectable** file-conformance violation named by this specification is assigned exactly one **reader outcome**: reject-file, reject-layer, reject-tile, or ignore-record." | **PASS** — and note its subject is "violation", not "condition", which is A-02's point |
| `[R-CNF-11]` (3878-3880, pre-existing) | "unable to check" | 209-242: *cannot establish* limited to "a capability or resource ground" | **PASS** |
| `[R-CNF-13]` (3905) | individuates conditions rather than requirements | 244-269: "A **condition** this specification names — one malformed state, as §21.1 individuates them, and not the requirement that defines it" | **PASS**, with the circularity noted in §3.3 |
| `[R-CNT-06]` (3905) | "shows by stating nine" | `[R-CNF-13]` at 251-253: "`[R-CNT-06]` states nine". Register cross-check below | **PASS** |
| §2.4 (3910) | outcome classes | §2.4 is 284-300, headed "Outcome classes and owning scope", containing `[R-CNF-07]` | **PASS** |
| `[R-ENC-06]` (3914) | fixed field widths are not a state a file can be in | 475-477: "No field's width is ever a writer choice: every field's width is fixed by this specification, and a structure whose fields appear at any other width is invalid at its owning scope." | **PASS** for the widths claim; see rejected candidates for the tension with "invalid at its owning scope" |
| `[R-ERR-01]` (3919) | paragraph-final identifier for §21.7's normative prose | Sole occurrence in the file (sweep below) | **PASS** — the identifier now labels the test rather than the inventory, which is the intent |
| §21.1's completeness clause (3891) | detectability is what it turns on | 3556-3560 | **PASS** |
| §9.7 (3934, 3948) | does not reconstruct history; "all §9.7 walks" is the live state | 1440-1480: "A verifier checking `[R-CNT-02]`'s partition walks the live state only." | **PASS** |
| §7.4's closing Note (3943) | no format-major-1 reader parses a sub-record payload as records | 1169-1178 is §7.4's last block before "### 8. Integrity" and says exactly that | **PASS** — it is the closing Note |
| §12.1 (3961-3965) | element sizes do not decide the case; planar uint8 → bool keeps element size 1 while the plane goes P·Bᶜ → ⌈P/8⌉ | §12.1's table gives bool = 1 and uint8 = 1, and the prose says "except that a planar bool plane is sized by packing (§14.3)"; §14.3 gives ⌈P/8⌉ | **PASS** — new, and correct |
| §14.3 (3956) | pad bits | 2028-2030 | **PASS** |
| §14.5 (3955, 3966, 3978) | padding positions carry the channel's fill | 2089-2098 (`[R-SER-05]`) | **PASS** on content; the *availability* of padding positions is A-03 |
| §17.3 (3982) | both filter values length-preserving | 2508-2517 "Length is unchanged"; `[R-COD-09]` admits only 1 and 2 | **PASS** |
| §20.3 step 4 (3944, 3949) | a §14 bar and a companion bar on planar disk ordinals | 3216-3239 and 3174-3186 | **PASS** — both bars exist and are distinct |
| §20.5 / `[R-WRT-06]` (3986-3990) | three trailer obligations | fresh file_id MUST (§20.5, "It MUST mint a fresh file_id"); ignore-lane MUST carry forward (3441-3444); version_minor SHOULD floor (3446-3456) | **PASS** — all three exist |
| §21.4's content rows (3966) | fire on a byte §14 constrains | T2, T4, T5 | **PASS** |
| T3, T14 (3953-3954, 3967-3971) | test lengths, T14 the declared, T3 the decoded | T3: "The decoded payload's byte length is not exactly the tile's decoded size"; T14: "Codec 1 (none) declared and a non-sentinel index entry's length differs from the tile's decoded size" | **PASS** |
| T15, T17, T23, T25 (3971) | rows for the codec now declared, testing stored bytes as a stream of it | T15 deflate wrapper, T17 zstd magic, T23 lz4 frame-vs-block, T25 malformed stream | **PASS** |
| T26 (3977-3979) | states the same terms for a wrong stride | 3774: "where the resulting image breaks §14.5's padding content or `[R-SER-08]`'s bool bytes ... the check that detects it is T2's or T4's" | **PASS** |
| T2, T4, T5 (3938, 3957, 3979) | witness a mis-ordered image / wrong fill | 3752-3755 | **PASS** |
| `[R-LIF-01]`, `[R-LIF-02]` (3930-3934) | history properties | classified the same way at §20.4's Rationale 3390-3398 | **PASS** |
| `[R-GEO-06]`, `[R-SER-01]` (3935) | ordinal mappings satisfied whatever values a valid tile carries | consistent with §20.3's "an ordinal move being no effect on any stored tile's bytes" | **PASS** |
| `[R-CNT-13]` (3939) | MU=0 record encoding file offsets in its payload | consistent with §20.4's "the no-embedded-offsets rule (§7.2) makes safe for MU = 0 records" | **PASS** |
| `[R-CNT-18]` (3941) | nesting prohibition | 1120-1126 | **PASS** on the citation; A-01 is about whether the classification survives §21.1's wording |
| `[R-SER-08]` (3978) | bool bytes | T2's governing rule | **PASS** |
| §21.7 (hunk 08, 3580) | "test for what no check detects" | §21.7's heading is "What no check detects" and it now states a test | **PASS** |

**Every citation in the repaired text resolves and says what the repairing sentence claims.** Not one bad citation. The defects are elsewhere.

---

## 7. Check 6 — what is still unconstrained in this structure

The structure the repair governs is §21.7's classification apparatus: the partition of everything this specification names into register-bearing and register-free. Its members, and whether a rule fixes each:

1. **Detectable file-conformance violation → row.** Fixed, by §21.1's completeness clause (normative) and now by §21.7's biconditional. Over-fixed: A-02.
2. **Unwitnessed condition → no row.** Fixed by §21.7's new sentence. ✔
3. **Requirement stating no condition a file can exhibit → nothing omitted.** Fixed, with one exemplar (`[R-ENC-06]`). ✔
4. **Condition that is not a violation at all** (§21.6's fourteen table rows, plus the two reader-refusal cases). **Mis-fixed** — §21.7's biconditional sweeps them in; §21.6 and §21.1 keep them out. This is the sibling the repair left in the wrong bin: A-02.
5. **Detectable violation whose detection is another row's** (`[R-SLB-04]`'s stale declaration, `[R-LIF-04]`'s residue, T13/T15/T16/T23/T26's "the check that detects it is X's"). Fixed by §21.1's strict-specialization clause and by the rows' own text, not by §21.7. Unaffected by the repair.
6. **The instrument's actor set.** "a reader or a verifier". Updaters are covered through `[R-CNF-11]`. Writers are not, correctly — a writer performs no checks.
7. **The instrument's conditionality.** Several checks are obliged only conditionally (`[R-CNT-04]`'s residency exemption, `[R-CNF-11]`'s resource declines, `[R-COD-11]`'s codec capability). "Obliges ... to perform" is not qualified. I considered filing this and did not — see rejected candidates.

The check-6 shape the charter warns about — one quantity of a structure pinned and its sibling left free — is present here as item 4, and I have filed it.

---

## 8. Check 8 — what the insertion did to the sentences around it

### Hunk 07 (insertion into §21.1's running paragraph)

Back-references forward from the insertion to the end of the paragraph:

- "**but each row *restates* its governing rule**" — no anaphor.
- "subject to **the same exception stated above**, a rule that assigns an outcome expressly" (3565-3567). Before the insertion this resolved to "except where a rule assigns one expressly, as `[R-CNT-25]`'s quarantine does for every §21.5 row" at 3549-3551. After the insertion, the nearest preceding candidate is the detectability test, which states no exception. **The referring sentence carries its own appositive gloss — "a rule that assigns an outcome expressly" — which re-anchors it correctly.** No re-resolution. ✔
- "**Its** completeness is normative" — precedes the insertion. ✔
- "Conditions attach to the finest structure **they** damage" — internal. ✔
- Backwards: does the inserted text use a distant back-reference? "some file exhibiting **it**" and "every file that does not [exhibit it]" — "it" is "a violation", named in the same clause. ✔

### Hunk 08

No sentence inserted; a noun replaced. No back-reference in the sentence or after it changes referent. ✔

### Hunk 09

Forward from the insertion to the end of §21.7 and into §21.8:

- "**It** is detectable in the contrary case" → the condition. ✔
- "**The two** are stated over the same subject" → unwitnessed and detectable. ✔
- "**such a check**" → "any check this specification obliges a reader or a verifier to perform". ✔ (load-bearing, and A-01 turns on §21.1 dropping it)
- "absent from **it** by **that clause's** own terms" → the register; §21.1's completeness clause. ✔
- "**That** is the whole of the test" → the two preceding definitions. ✔
- "conditions of **both kinds** ... classified as a whole by **neither**" → unwitnessed and detectable. ✔
- "Nothing is omitted from the register on **its** account" (3917). Nearest candidates are "a structure written at any other [width]" and "the rows for the fields that hold them"; intended is `[R-ENC-06]`, five clauses back. Recoverable but loose. Not filed.
- "Beyond the content-wrongness **this section opens with**, **these obligations**" (3927-3928). Old text: "A second set of obligations is omitted..." — "second" contrasted with the opening paragraph's first set. New text keeps the contrast explicitly and anchors "these obligations" to the block's own lead-in. ✔
- "**Its** companion bar on a planar layer's disk ordinals" (3949). Nearest possessive is "§20.3 step 4's **§14 bar**"; "companion bar" correctly implies a sibling of it, and §20.3 itself says "The bar beside the §14 bar". ✔
- "for the same reason no check knows which ordinal a stored tile **used to occupy**" (3950-3951) — tense correct, prior generation. ✔
- "Where **the change** does touch something §14 fixes" (3959-3960). Ambiguous between the re-typing (the paragraph's earlier subject) and the ordinal permutation (its immediate subject). Both readings yield true statements, so I did not file it separately.
- **"Which case a re-typing falls in is not decided by the element sizes of §12.1"** (3961-3962) — this inserted sentence became the topic sentence of the paragraph that carries the untouched taxonomy: "A change reaching a byte §14 structurally constrains...", "A change reaching the decoded size...", "**A change reaching the codec**...", "**A change reaching the filter**...". Before the insertion those four sentences followed directly on "§20.3 step 4's bar on a declaration change is witnessed only where the affected tiles remain stored", so "A change" resolved to *a declaration change barred by §20.3 step 4* — which covers type, codec, filter and geometry alike. After the insertion the paragraph opens on re-typing, and a re-typing cannot reach the codec or the filter. Neither the referring sentences nor the referred-to bar changed a word. This is **A-07**.

Backwards into §21.8: "Every row of §21.2 through §21.5 — 120 conditions over 275 instances" — no anaphor reaching back into §21.7. ✔

---

## 9. Putting the test to requirements myself

| Requirement / condition | §21.7's test says | Register says | Agree? |
|---|---|---|---|
| `[R-CNT-06]` trailer CRC (F14) | detectable — the obliged CRC check separates a bad-CRC file from every good one | row F14 | ✔ |
| `[R-CNT-04]` front block (F6) | detectable — a verifier holds no residency exemption | row F6 | ✔ |
| `[R-ENC-15]` duplicate layer names (F4) | detectable — obliged at open | row F4 | ✔ |
| `[R-MTA-05]` unsorted document (F27) | detectable — verifier obliged, detector *verifier* | row F27 | ✔ |
| `[R-CNT-22]` registered-type flags (F28) | detectable — verifier obliged | row F28 | ✔ |
| `[R-SER-05]` padding fill (T4) | detectable | row T4 | ✔ |
| `[R-COD-10]` mis-stride, no structural constraint | unwitnessed — a legitimate writer could emit byte-identical output | no row (T26 covers only the structurally-constrained half) | ✔ |
| `[R-COD-06]` undisclosed dictionary | unwitnessed | no row; §17.2 at 2610-2613 says so of the metadata analogue | ✔ |
| `[R-LIF-01]` committed-prefix immutability | unwitnessed — history | no row | ✔ |
| `[R-LIF-02]` strict growth of committed_file_length | unwitnessed — history | no row | ✔ |
| `[R-GEO-06]`/`[R-SER-01]` ordinal mappings | unwitnessed except where §14 constrains a byte | no row | ✔ |
| `[R-CNT-13]` MU=0 offsets in payload | unwitnessed — not fixed by the bytes | no row | ✔ |
| `[R-CNT-18]` nesting | unwitnessed under §21.7; **detectable under §21.1's wording** | no row | **✗ — A-01** |
| `[R-WRT-06]` fresh file_id | unwitnessed — no field counts commits (§20.5 says so) | no row | ✔ |
| `[R-ENC-06]` field widths | no condition; test not reached | no row | ✔ |
| `[R-SLB-04]` stale slab declaration | unwitnessed as to staleness; the invariant failure is registered | no row of its own | ✔ (and unlisted — A-04) |
| §20.4 preservation (`[R-WRT-05]`, `[R-WRT-08]`) | unwitnessed — no file records its predecessor's directory | no row | ✔ (and unlisted — A-04) |
| `[R-IDX-02]` sentinel entry (§21.6) | ambiguous; either "unwitnessed" (absurd — a reader must act on it) or "detectable" (then §21.7 demands a row §21.6 denies) | no row | **✗ — A-02** |
| `[R-CNT-07]` unimplemented major (§21.6) | **detectable** — the reader is obliged to reject | **no row**, §21.6 says so expressly | **✗ — A-02** |
| `[R-CNT-15]` experimental top-level MU=1 (§21.6) | **detectable** — `[R-CNT-15]` obliges rejection | **no row**, §21.6 says so expressly | **✗ — A-02** |

**Sixteen right, five wrong, and the five wrong are two defects.** The test is largely sound; it fails at the boundary with §21.6 and it is mis-transcribed in §21.1.

### Is the test complete? What "live state" is fixed by

§21.7's test does **not** speak of live state; §21.1's inserted gloss does, and that is A-01. For the record: "live committed state" is fixed by `[R-CNT-02]` (685-694) as a set of byte-claiming structures — the front block, every structure reachable from the live trailer, the directory, the trailer. It is a coverage notion. Two files can differ in ways it does not reach: slack content (`[R-CNT-21]` puts slack outside it entirely), physical file length beyond the committed prefix, and — crucially — everything about the *prior* generation. §21.1's gloss inherits all of that as unexamined baggage, which is a second reason its predicate is the wrong one.

---

## 10. Sweeps run, verbatim, with hit counts

Line-oriented (`grep -n` unless noted). The file is hard-wrapped, so for the multi-word rule phrases I used a whitespace-normalising python pass instead.

```
grep -n "R-CNF-01\]\|R-CNF-05\]\|R-CNF-07\]\|R-CNF-11\]\|R-CNF-13\]\|R-ERR-01\]\|R-ERR-02\]\|R-ENC-06\]" spec/tarn.md     -> 27 hits
grep -n "21\.7" spec/tarn.md                                        -> 6 hits (2521, 2613, 3240, 3457, 3560, 3580) + heading 3864
grep -n "detectab" spec/tarn.md                                     -> 13 hits
grep -n -i "unwitness\|witness" spec/tarn.md                        -> 21 hits
grep -n "live state" spec/tarn.md                                   -> 15 hits
grep -n "^#### 21\." spec/tarn.md                                   -> 9 hits
grep -n "^#### 12\.\|^#### 14\.\|^#### 17\.\|^#### 7\.4" spec/tarn.md -> 12 hits
grep -n "no witness\|no register row\|omitted from the register\|outside the register" spec/tarn.md -> 8 hits
grep -n "R-CNT-18" spec/tarn.md                                     -> 13 hits
grep -c "^| L[0-9]" spec/tarn.md                                    -> 49
grep -c "^| F[0-9]" spec/tarn.md                                    -> 35
grep -c "^| T[0-9]" spec/tarn.md                                    -> 26
grep -c "^| R[0-9]" spec/tarn.md                                    -> 10
grep -c "reader | open | \`\[R-CNT-06\]\`" spec/tarn.md             -> 9
grep -o "^| F[0-9]* |.*\`\[R-CNT-06\]\`" spec/tarn.md | sed 's/ |.*//'  -> F1 F8 F9 F10 F12 F13 F14 F15 F16 F17
```

Whitespace-normalised substring counts (python heredoc, reading only spec/tarn.md):

```
'is separated by such a check'            1
'differs, in its live state'              1
'told apart'                              1
'obliges a reader or a verifier'          1
'the whole of the test'                   2
'carries a row for a condition'           1
'exactly where it is detectable'          1
'no condition a file can exhibit'         1
'the instrument is'                       1
"register's own rows"                     1
'reader-detectable'                       1
'the obligations this test places outside' 1
```

Reading of the two "the whole of the test" hits: 3895 (§21.7, the detectability test) and 3216 (§20.3, "the §14 bar is the whole of the test of what a shrink **alters**"). Different subjects, no collision.

The single-hit counts are what matter for check 3: each distinctive phrase of the new rule occurs once, in unlabelled text. No competing statement of the rule survives anywhere — the defect is that the *one other* statement, §21.1's, uses different words for the same thing.

---

## 11. Numbers I derived myself

| Quantity | My arithmetic | Document figure | Match? |
|---|---|---|---|
| Register rows citing `[R-CNT-06]` as **governing** rule | F8, F9, F10, F12, F13, F14, F15, F16, F17 = **9**. (F1 was excluded: its cell is "`[R-ENC-02]` (R-CNT-04, R-CNT-06)", so R-CNT-06 is a *read* rule there, not the governing one — §21.1: "A Governing rule cell names that requirement first; any identifiers following it in parentheses are the further rules the condition reads") | `[R-CNF-13]`: "`[R-CNT-06]` states nine"; §21.7: "shows by stating nine" | ✔ |
| §21.2 row count | F1–F36 minus struck F11 = **35** | "35 conditions" | ✔ |
| §21.3 row count | **49** | "49 conditions" | ✔ |
| §21.4 row count | **26** | "26 conditions" | ✔ |
| §21.5 row count | **10** | (not stated separately) | n/a |
| Total register conditions | 35 + 49 + 26 + 10 = **120** | §21.8: "120 conditions over 275 instances" | ✔ |
| `[R-WRT-06]` trailer obligations | fresh file_id (MUST), ignore-lane carry-forward (MUST), version_minor floor (SHOULD) = **3** | §21.7 Rationale: "three obligations" | ✔ |
| §20.5's "Neither obligation" | the **2** stated in that paragraph | "Neither" | ✔, not a contradiction with the 3 |
| A-03 counterexample sizes | E₀ = T₀ = 64, so E mod T = 0 → 0 padding positions; two uint8 planes, P·Bᶜ = 64·1 = 64 each; T3 compares 64 vs 64; T14 compares 64 vs 64 | T3/T14's own formulas | the permutation passes every row |
| A-03 §12.1 arithmetic in the repaired text | uint8 element size 1, bool element size 1; plane P·Bᶜ = P → ⌈P/8⌉ | §12.1 table + §14.3 | the repair's own number is **correct** |

---

## 12. Byte-level test, per finding

The discriminating question in each case: is the disputed file conforming, and does only one reading permit an actor to produce it?

- **A-01.** The disputed condition is `[R-CNT-18]` nesting. A file exhibiting it is nonconforming under both readings, so `[R-CNF-05]` bars every conforming writer from emitting it either way. On the reading side, neither reading creates a check: the divergence is about whether the *register* is defective for omitting a row, and no row exists under either reading, so no reader acquires an obligation. `[R-CNF-11]`'s *cannot establish* is limited to capability and resource grounds, so the verifier's verdict does not move. **Not byte-level.** It is a normative contradiction between two normative passages about a definition the section itself calls load-bearing.
- **A-02.** Files with a sentinel entry, an extent-0 dimension, an unimplemented major, or an experimental MU=1 top-level record are all conforming, and §21.6 normatively fixes what a reader does with each ("A reader that treats any of them as a failure is the nonconforming party"). §21.7's sentence does not create rows; it only asserts that rows exist. No implementation would invent one against §21.6's explicit text. **Not byte-level.**
- **A-03, A-04, A-06, A-07.** All inside or about a block labelled **Rationale.**, hence non-normative by `[R-CNF-01]`, and the block subordinates itself to the test. **Not byte-level.**
- **A-05.** Inside a block labelled **Note.** **Not byte-level.**

I found nothing in these three hunks that moves the set of emittable bytes or any accept/reject verdict, and I say that plainly rather than inflating A-01 or A-02 to reach it.

---

## 13. Findings

**A-01** — §21.1's restatement of the detectability test uses a different instrument from §21.7's, and the two give opposite verdicts on `[R-CNT-18]`. (hunk 07, CITATION/quantifier-warrant, CONFIRMED)

**A-02** — §21.7's new "the register carries a row for a condition exactly where it is detectable" contradicts §21.6, which normatively denies rows to conditions a reader is obliged to reject on. (hunk 09, LOCAL_CONTRADICTION, CONFIRMED)

**A-03** — the inserted disk-ordinal trichotomy claims T4 or T5 sees a fill mismatch, but a layer with no padding positions and no pad bits has neither witness. (hunk 09, OVERCLAIM, CONFIRMED)

**A-04** — the Rationale's lead-in presents itself as the complete set of obligations the test places outside the register, and omits §20.4's preservation obligations and `[R-CNT-03]`'s zeroing SHOULD. (hunk 09, OVERCLAIM, CONFIRMED)

**A-05** — §7.4's Note still grounds the omission of `[R-CNT-18]` on "no reader-detectable witness", an inference the new test invalidates because six register rows are verifier-only. (hunk 09, UNSWEPT_RESTATEMENT, PLAUSIBLE)

**A-06** — "with matching quantifiers, so each is exactly the negation of the other" gives as its reason the very thing that would defeat it; the quantifiers are dual, not matching. (hunk 09, LOCAL_CONTRADICTION, CONFIRMED)

**A-07** — the inserted §12.1 sentence became the topic sentence of the untouched "A change reaching the codec / the filter" taxonomy, whose antecedent was a declaration change of any kind, not a re-typing. (hunk 09, NEW_AMBIGUITY, PLAUSIBLE)

---

## 14. Candidates I opened and closed

- **"§20.3 step 4's bar" left ambiguous between the two bars.** Closed: the repair fixed this, disambiguating both occurrences to "**§14 bar**" and adding the companion. It is a repair, not a defect.
- **§20.3's and §20.5's normative pointers into §21.7 now land in non-normative text.** Closed: both citing sentences assert the substance normatively in place, and the new normative test derives what they cite. Nothing normative is orphaned.
- **"`[R-CNT-06]` shows by stating nine" cited for the wrong half of the sentence.** Closed: the citation attaches to "the subject is the condition and not the requirement", which it does warrant; the "both kinds" claim in the next sentence is separately true via `[R-CNT-13]`.
- **`[R-ENC-06]` says "invalid at its owning scope", which sounds like a condition even though §21.7 says there is none.** Closed: this wording predates the repair (the old text carried the same "not a state a file can be in" claim), and §21.7's argument — the parse is always at the fixed widths, so a mis-width structure yields different *values*, caught by the field rows — is unchanged. Not a repair defect.
- **"obliges a reader or a verifier" might exclude conditionally-obliged checks** (`[R-CNT-04]` residency, `[R-CNF-11]` resource declines, `[R-COD-11]` codec capability), which would strip §14's content rows out of the register. Closed: "obliges ... to perform" states that an obligation exists, not that it is unconditional, and `[R-CNT-04]` itself says a verifier holds no exemption. Reading it the other way would make §21.4 incoherent, which is not a competent reading.
- **The test classifies a condition with empty extension as vacuously unwitnessed, which the `[R-ENC-06]` paragraph then denies.** Closed: the test's subject is "a condition this specification names", and §21.7's position is that `[R-ENC-06]` names none — so the test is never reached. Coherent.
- **`[R-SLB-04]`'s stale declaration and `[R-LIF-04]`'s residue carry no rows although they are violations.** Closed as separate findings: their detection is another row's (`[R-SLB-03]`'s invariants; F17's committed_file_length gate), which §21.1's strict-specialization clause covers; both Notes predate the repair. Folded into A-04 only as supporting weight.
- **"Nothing is omitted from the register on **its** account" has a loose antecedent.** Closed: recoverable within the sentence, and unchanged in substance from the pre-repair text.
- **"Where **the change** does touch something §14 fixes" is ambiguous between re-typing and ordinal permutation.** Closed: both readings are true statements about the register's reach, so nothing turns on it. Folded into A-07's neighbourhood rather than filed separately.
- **§20.5's "Neither obligation" against the Rationale's "three".** Closed by reading §20.5 whole: "Neither" is local to that paragraph's two; the fresh file_id MUST is stated 15 lines earlier.
- **Row counts and the 120/275 figure.** Closed: recomputed and they match.

## 15. Where I found little, and what would have found it

Hunk 08 is a one-word rename and I filed nothing against it. What I did that would have found something: I confirmed §21.7's heading is literally "What no check detects" so the new noun phrase reads correctly; I confirmed §21.7 now does state a test rather than an account, so the rename is not a mis-description; I checked the enclosing sentence's other three items (§21.6's non-violations, §21.9's limits, the register subsections) still hold after hunk 09 moved §21.7's inventory into a Rationale — the sentence says the completeness clause and the instance arithmetic do not reach §21.7, which is now more obviously true, not less; and I ran the back-reference pass over the sentence and its neighbours. There is nothing there.

Where my coverage is thinner than I would like: I did not exhaustively put the test to all 120 register rows, only the twenty in §9's table. I did not audit §21.3's L-rows individually for verifier-only detectors beyond the ones I named. And A-05 rests on my reading that "reader-detectable" in §7.4's Note excludes verifier-only detection, which is a reading of a Note rather than of a normative rule — hence PLAUSIBLE rather than CONFIRMED.
