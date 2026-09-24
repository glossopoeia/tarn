# Verifier comparator — working transcript

## Disclosure

**Files read, exactly the four permitted, nothing else:**
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (edition A, 4,981 lines) — read via the `Read` tool in overlapping windows covering the whole file, plus targeted `sed -n` extractions (same file, no other) once I knew which line ranges I needed a second time.
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/c/tarn.md` (edition B in this task's naming, 4,885 lines) — same method.
- `.../fidelity-2/out/transcript-verifier-a.md` and `.../transcript-verifier-b.md` — read whole, via `Read`.

I did not list any directory other than creating my own scratch directory with `mkdir -p` (no `ls`). I did not open docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, spec/registry.json, git history, or the web.

**Commands run against the two spec files only:** `grep -n '^#'` (heading index only, immune to hard-wrap), `wc -l`, `sed -n '<range>p'` to pull exact line ranges after locating them by heading or by a short `grep -n` anchor, and `diff` between corresponding `sed`-extracted ranges of the two files. I never ran a content-bearing `grep` pattern that spans a hard-wrap boundary without first confirming via `sed` context; every zero-hit grep below has a paired positive-hit control run in the same file to prove the string-matching itself works (documented inline as I used it — e.g. `grep -n "MUST NOT change one of these"` returned nothing because the sentence is hard-wrapped across lines, so I switched to `grep -n "binds the commit as an actor"`, a fragment that does not straddle a line break, which hit both files at the same relative offset).

**Sweeps and their controls, with hit counts:**
- `grep -n "R-CNF-02"` on A: 8 hits (lines 179, 1089, 1306, 1311, 2726, 2818, 3280, 4034, 4061 — 9 actually). On B: 9 hits (218, 986, 1203, 1208, 2623, 2715, 3177, 3931, 3958). Used to find every place R-CNF-02 is invoked, to check the §2.3 bullet's claim against its own downstream uses.
- `grep -n "R-ERR-04"` on A: 9 hits; on B: 9 hits, at parallel offsets — used to confirm the resource-decline machinery is otherwise untouched.
- `grep -n "R-SER-05\|R-SER-08"` on A: 21 combined hits; on B: 20 — the one hit A has and B lacks is exactly A's §2.3 line 228 (see Finding cmp-verifier-05). Control: every other R-SER-05/08 hit in A has a same-content match in B at a parallel offset, confirmed by inspection, so the count delta is that one line, not a wrapping artifact.
- `grep -n "F14 reaches"` on A: 1 hit (line 285, inside the §2.3 Note). On B: 0 hits. Control: `grep -n "lists the rows that reach"` on B: 1 hit (line 289) — proves grep against this file's prose does work and the zero above is a real absence, not a tooling miss.
- `grep -n "readers of the files they process"` on A: 1 hit (218); on B: 0 by that exact fragment, but `grep -n "Verifiers are readers"` on B: 1 hit (248) with the parallel sentence intact minus "and updaters" — confirms deliberate wording, not truncation.
- Full-file structural diff: `sed -n '443,$p' A | diff - <(sed -n '340,$p' B)` (i.e., diffing every line of both documents from "### 4. Encoding Conventions" — the first heading whose ordinal and content re-align after B's §2/§3 reorder — to end of file). Result: exactly two hunks (a one-line wording change at old-§12 "channels are declared in order," and a six-line paragraph present at the end of B's §21.6 with no counterpart at that position in A). This is the control that lets me assert, rather than merely sample-check, that **every other byte from §4 onward is identical between the two editions** — I did not have to guess whether some other section also diverged; the diff proves it did not.
- Section-by-section `diff` on `sed`-extracted ranges for §5.2, §6.2, §7.2, §9.2, §9.7, §17.4, §20.3 (the append procedure's fixed-declaration bar), §21.6, §21.7: all exit 0 (byte-identical), confirmed individually as well as by the full-tail diff above.

**Confidence there is little else hiding:** the full-tail diff (§4 onward, essentially the whole container/array-model/behavior/register body of the specification) returning only two hunks is the strongest evidence I have that the fidelity-relevant differences are concentrated in §1–§3 (introduction, terminology, and — most importantly — §2.3/§2.4's conformance-class definitions), plus the one relocated paragraph in §21.6 and one cosmetic wording change in §12. I read all of §1–§3 in both editions directly (not by diff, since B reorders §3 ahead of §2) to find the remaining divergences documented below.

**Context that arrived unbidden.** My context contained a CLAUDE.md pointer, a user memory-file index of many "TARN ..." note titles, a `gitStatus` block (branch `readable`, five recent commit subjects — several of which describe exactly the §2.3 rewrite I independently found broken, e.g. "Readable: §2.4 — preserve-verbatim gloss and the reject Note cut" and "condition and reach defined in plain words; invariant is property"), environment/skill-listing boilerplate, and the harness's own framing paragraphs. None of this is the specification; I did not open any file it names, and the two commit-subject lines above are cited here only to disclose that they appeared, not used as evidence for any finding — every finding below is sourced to the two `tarn.md` files by line number and quotation.

**Scratch directory.** `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-2/scratch/compare-verifier/` — created with `mkdir -p`; I wrote one placeholder note file there (`notes.md`) and did no other scratch work requiring a file (all diffing was done via inline `sed`/`diff`/process substitution, no intermediate files needed except the two `_tail.txt` extractions used for the full-body diff, also in that directory).

**Paths.** Both spec files and both transcripts were exactly where the brief said.

---

## Part 1 — Reading the two walks' probe answers against the two texts

### V1 (verdict vocabulary)
§2.3's core R-CNF-11 paragraph (three verdicts, priority rule, *unexamined*) is **byte-identical** between A and B (confirmed by direct comparison of both full bullets). Both walkers quote it correctly and answer the same way. Where the editions actually diverge on "cannot establish" is the *enumeration of grounds* — see cmp-verifier-05 below, a LOSS neither walker's V1 answer surfaced (walker A quoted A's five-ground list in Part 1 step 8/§2.3; walker B, reading B, could only ever have found four, since B's own list is four items — walker B's V1 answer names three examples generically and does not claim completeness, so it is not itself wrong, but it could not have reported the fifth ground because B's text does not state it in enumerated form).

### V2 (unimplemented top-level type, MU=1)
§10.2, §10.3, §21.6, F35/F36 are all byte-identical between A and B (within the confirmed-identical §4-onward body). Both walkers gave the same bifurcated, `underdetermined`-tagged answer, citing the same rows and the same §2.3 parenthetical about a conforming file's MU=1 type necessarily being experimental-range. **REPORTER_ERROR is not applicable here — both are correct — and this is EQUIVALENT**: the texts do not differ at any passage either walker cites for V2.

### V3 (three-generation trace)
§5.2, §6.2, §9.2 (R-LIF-02), §20.3 step 4 (R-WRT-04's whole-index-reemission rule), and §21.6's slack row are all confirmed byte-identical. Both walkers built the identical arithmetic (F₁=4,480, F₂=13,120, F₃=14,528, live=12,816, slack=1,712) from identical text, and both used the identical "minimal pad" assumption, citing the identical R-LIF-02 step 5 language and the identical "a longer gap is conforming" sentence (walker A explicitly, walker B via R-SLB-05, itself confirmed byte-identical). **EQUIVALENT.**

### V4 (inexecutable codec/filter)
§17.4/R-COD-11 is byte-identical between A and B (confirmed directly, not just via the tail diff). Walker A's formal probe answer and walker B's formal probe answer are compatible on the facts (both name L43/L45, R-CNF-03, R-CNF-11's priority rule); walker B additionally states, as a numbered finding, that the "cannot establish" branch is consequently unreachable for a genuinely conforming verifier, while walker A raises exactly this idea in its own internal `rejected_candidates` and argues it is not a defect because R-COD-11 still binds non-conforming verifier *tools* encountering the situation in the wild. I read the passage again specifically to adjudicate this: R-CNF-03 makes any software that cannot execute an *assigned* codec/filter not a conforming reader at all, so the "cannot execute" state R-COD-11 opens with, restricted to a conforming reader/verifier, is indeed reachable only at a reserved/experimental value — which L43/L45 already flags before decode is attempted. Walker A's rebuttal ("R-COD-11 is a floor for any tool, conforming or not") is a different, also-true claim about a different scope (non-conforming tools), not a refutation of walker B's narrower claim about conforming ones. **This is not a text divergence (§17.4 is identical) and not a clean REPORTER_ERROR** — both walkers are reasoning correctly about different scopes of the same identical sentence. I record it as an OBSERVATION rather than a scored finding, since no edition text differs and no implementer's bytes differ either way (see cmp-verifier-07's disposition below; I did not promote this to a numbered finding for that reason — it is folded into the evidence notes only).

### V5 (last commit changed a fixed declaration)
§20.3 step 4 and §21.7 are both confirmed byte-identical, word for word (diff exit 0 on each). Both walkers reach the same conclusion (verifier cannot see it; no register row; §21.7's four named exceptions govern what little symptom-detection is possible) from identical text. Walker B's own Finding V-2/verifierb-02 (that §20.3 step 4 cites R-ERR-01's "no condition a file can exhibit" category when the fact pattern actually fits §21.7's *unwitnessed condition* test one paragraph earlier) is argued entirely from text that is **identical in edition A** — I reread both §20.3 step 4's citation clause and §21.7's two-category test in edition A side by side and the same argument applies word for word. See cmp-verifier-06: this is a real candidate document defect, but it is **not a fidelity divergence between A and B** — it is a defect (if it is one) that both editions share equally, inherited unchanged from A, not introduced or fixed by B's rewrite.

### V6 (MU=1/PE=0)
§7.2 (R-CNT-12) is confirmed byte-identical. Both walkers give the same two-actor analysis from the same quoted text. **EQUIVALENT.**

---

## Part 2 — Findings from the two walks' own self-reported findings, checked against the other edition

- **verifiera-01** (pad-length underdetermination, §6.2/R-CNT-05): §6.2 is confirmed byte-identical between A and B. The non-uniqueness of slack totals across conformingly-equal files is therefore present identically in edition B. Walker B's transcript does not name this as a formal finding, but it used the identical minimal-pad assumption and cited the identical governing language (R-SLB-05, R-LIF-02 step 5) without flagging the underdetermination as a documentation gap. This is not an edition difference — see cmp-verifier-07.
- **verifierb-01** (R-COD-11's cannot-establish branch practically unreachable): argued from §17.4, confirmed identical in A. Discussed under V4 above; not scored as a numbered finding since it is not a text divergence and does not change any implementer's bytes.
- **verifierb-02** (R-ERR-01 vs. unwitnessed-condition miscategorization at §20.3 step 4): argued from §20.3/§21.7, confirmed identical in A. See cmp-verifier-06.

---

## Part 3 — Reading past the probes: §2.3 side by side, in full

This is where the real divergence lives. §2.3 ("Conformance classes") is the single most heavily rewritten passage in the whole document — everything else from §4 onward is a byte-for-byte match (see the full-tail diff in Disclosure) — and reading the two versions of §2.3 side by side line by line turned up four separate substantive losses, two of which are outright self-contradictions internal to edition B (the rewrite inverts a rule at the point it is defined, while an unchanged sentence elsewhere in the same edition — sometimes a few lines away, sometimes in an untouched later section — still states the original, correct rule). These are exactly the kind of defect the byte-level test is built to catch: an implementer who builds strictly from the local sentence in edition B, without independently reconciling it against a different section, gets the wrong verdict.

### cmp-verifier-01 — "Conforming TARN file" bullet: B inverts R-CNF-02's rule at its own point of definition

Edition A (lines 166–179), the "Conforming TARN file" bullet's second half:
> "A few obligations this specification places on writers govern their *conduct* rather than their output — where a value is published, which registry version a writer targets (§10.3, §18.3), or the barriers a commit performs (§9.2) — and a file is never nonconforming by virtue of one: conduct rules bind the actor, the predicate binds the bytes. A writer obligation whose violation this specification expressly declares not to be a file-conformance violation binds the actor in the same way; §6.3's flags rules against a set ignore-lane bit (a creator's flags = 0, and an updater's copy-forward and set-no-other, §20.3 step 6 and §20.5), §6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad, and §20.3 step 4's bar on the fixed declarations of a layer that stores a tile are the cases this text states, and each is declared where it arises rather than enumerated here. `[R-CNF-02]`"

Edition B (lines 214–218), the same bullet's second half, in full:
> "A writer obligation that governs conduct rather than output, or whose violation this specification expressly declares not to be a file-conformance violation, binds the writer, and a file that breaks one is nonconforming. `[R-CNF-02]`"

B says the opposite of A: A says such a file "is never nonconforming by virtue of" a conduct-rule breach; B says "a file that breaks one is nonconforming." This is not a paraphrase — it is the rule's polarity flipped at the exact sentence that carries the `[R-CNF-02]` tag, i.e. at the point of definition.

It is also a **self-contradiction internal to edition B**: at §9.2 (byte-identical to A), B still reads —
> "Steps 4 and 6 bind a writer's **conduct** rather than its output, and are declared so here on the model `[R-CNF-02]` states: a barrier orders writes against power loss and leaves no trace in the bytes, so a file committed without one can be byte-identical to a file committed with it. A writer that omits a barrier violates this requirement as an actor, and the file it produces is never nonconforming by virtue of it, as `[R-CNF-02]` says of every conduct rule." (B, lines 1202–1208; identical text at A, lines 1305–1311.)

So edition B contains, in the same document, one sentence saying `[R-CNF-02]` makes a conduct-rule-violating file "never nonconforming by virtue of it" and another (the rule's own defining bullet) saying such a file "is nonconforming." A's two corresponding passages agree with each other; B's do not.

- **Kind: LOSS** (of the "never nonconforming for conduct" rule, at the passage that defines it) with an internal **CONTRADICTION** as corroborating proof this is a slip, not an intentional new rule.
- **Byte-level test:** yes. A verifier built strictly from B's §2.3 bullet would classify a file with, say, a conforming-but-over-minimal pre-trailer pad, or a set ignore-lane flag bit, or a commit that changed a layer's fixed declaration under §20.3 step 4 (all three of which A's version *names by name* as conduct-only, non-file-defects) as **nonconforming**, where an implementation built from A (or from B's own §9.2) would correctly certify the file. That is a different accept/reject verdict on an identical file.

### cmp-verifier-02 — the closed list of three named conduct-rule examples is dropped from B's §2.3 entirely

Beyond the polarity flip above, A's bullet names, by cross-reference, the closed list of cases the "conduct, not predicate" doctrine actually covers: §6.3's flags-lane rule, §6.2's pre-trailer-gap-longer-than-minimum rule, and §20.3 step 4's bar on changing a layer's fixed declarations. B's rewritten bullet (quoted in full above) contains no such list — the entire enumerating clause is gone, along with the tie back to §20.3 step 4 specifically. This matters because §20.3 step 4 (identical text in both editions) separately cites "no condition a file can exhibit (§21.7, `[R-ERR-01]`, `[R-CNF-02]`)" for its own bar — a reader of B alone, arriving at §20.3 step 4 first, has to take that citation on faith, since B's own definition of what `[R-CNF-02]` covers no longer names this case as one of the instances "this text states."
- **Kind: LOSS.**
- **Byte-level test:** no on its own (the underlying rule at §20.3 step 4 is unchanged and still correctly stated there); it compounds cmp-verifier-01 by removing the one place a reader could have caught that inversion by cross-reference.

### cmp-verifier-03 — the §2.3 "reach" paragraph: B inverts the reject-file/capability-refusal polarity, then contradicts itself two sentences later

Edition A (lines 265–273), on what a reader does with a *reaching* condition's failure under a foreign format major:
> "A reader MUST apply every reaching condition to a file whatever major it declares — an exemption the condition's governing requirement grants on a ground other than the declared major applies unchanged, `[R-CNT-04]`'s residency exemption among them — and MUST treat its failure as reject-file on the ground of the requirement stating it rather than on capability grounds; the distinct diagnostic `[R-CNT-07]` asks for is owed where every reaching condition is satisfied and the declared major is one the reader does not implement."

Edition B (lines 275–281), the same clause:
> "A reader MUST check every reaching condition whatever major the file declares, and MUST treat a failure as a capability refusal, not as reject-file under the requirement that states the condition; an exemption that the condition's own requirement grants for a reason other than the declared major lapses, `[R-CNT-04]`'s residency exemption among them. `[R-CNT-07]`'s distinct diagnostic is given where every reaching condition is satisfied and the declared major is one the reader does not implement."

Again the polarity is exactly flipped: A says treat the failure **as reject-file, not on capability grounds**; B says treat it **as a capability refusal, not as reject-file**. And again B immediately contradicts its own new sentence — two sentences later, in text also present (verbatim) in A:
> "A verifier that finds such a failure reports *nonconforming*, whatever major the file declares and whether or not it implements that major: the property broken is one shared among all majors (`[R-CNT-24]`)." (B, lines 282–285; parallel wording at A, lines 274–277 with "the invariant broken" for "the property broken.")

A "capability refusal" is definitionally a *cannot-establish* ground elsewhere in this same document (§2.3's R-CNF-11 paragraph, identical in both editions, ties capability/resource grounds to *cannot establish*, never to *nonconforming*); an established violation is what forces *nonconforming* under R-CNF-11's own priority rule. B's rewritten sentence tells an implementer to treat a reaching-condition failure (e.g. F14's trailer-CRC mismatch under a file declaring format major 2) as the former, then its next sentence says the verifier reports the latter for that same failure — a direct internal contradiction, and directly relevant to V1's core certification algorithm (both walkers built the version-major reach test as an explicit step, citing exactly this rule) and to V2's discussion of F35/F36's reserved-vs-experimental split, which depends on the same reject-file/capability-ground distinction being drawn correctly.
- **Kind: LOSS / CONTRADICTION.**
- **Byte-level test:** yes. An implementer following B's literal instruction ("capability refusal, not reject-file") would not count a reaching-condition failure as an *established violation*, and so — following R-CNF-11's priority rule correctly on that (mistaken) premise — would report *cannot establish* rather than *nonconforming* for a file whose trailer CRC fails to match under a declared-but-unimplemented format major. An implementer following A, or following B's own very next sentence, reports *nonconforming*. That is a different verdict on the same bytes.

### cmp-verifier-04 — "Verifiers and updaters are readers…" loses "and updaters," breaking an unchanged cross-reference in §20.3

Edition A, §2.3, Conforming verifier bullet (line 217–218):
> "Verifiers and updaters are readers of the files they process and inherit every reader obligation."

Edition B, the same sentence (line 248–249):
> "Verifiers are readers of the files they process and inherit every reader obligation."

"and updaters" is dropped. This is the *only* place in either document (confirmed: `grep -n "readers of the files they process"` — 1 hit in A, and the parallel sentence in B checked directly since the exact fragment doesn't match after the edit) that states this general principle for both classes at once. §20.3 (byte-identical in both editions) relies on it explicitly:
> "An updater's verification depth follows reliance (`[R-RDR-02]`'s principle, which §2.3 extends to updaters as readers of what they process, `[R-CNF-11]`): …" (A line 3189–3191 / B line 3086–3088, identical.)

`[R-CNF-11]` is precisely the tag on the Conforming-verifier bullet quoted above. In edition B, the sentence §20.3 attributes this extension to no longer says it — B's §20.3 now cites a paragraph that, in B's own text, does not do what §20.3 says it does.
- **Kind: LOSS** (of scope: A states the reader-obligation-inheritance principle for both verifiers and updaters at the one place it is stated generally; B narrows it to verifiers alone) with a resulting dangling cross-reference in the (unchanged) §20.3.
- **Byte-level test:** no direct effect on a verifier's own accept/reject output (a verifier's obligations are unaffected — the dropped word concerns updaters), but it does leave an appender/updater's exact obligation-depth argument in B under-supported at its cited source, which matters for reasoning about how a file's later generations were legitimately produced (relevant background for V3's multi-generation trace, where both A and B's identical §20.3 language is what actually carries the obligation, so no walker's answer differed here in practice).

### cmp-verifier-05 — B's "cannot establish" grounds list, relocated to §21.6, drops one of A's five grounds

Edition A states this list inline in §2.3's Conforming-verifier bullet (lines 219–229):
> "…*cannot establish* — the last where some requirement is one it is unable to check on a capability or resource ground, as when the file names a format major version it does not implement, when a record carries MUST_UNDERSTAND = 1 with a type it does not implement (§21.6), when it cannot execute a codec or filter (`[R-COD-11]`), **when it declines a layer's or a tile's decode on resource grounds and so cannot check §14's decoded-content obligations (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`)**, or when it declines to decode a user-metadata document (`[R-MTA-09]`)."

Edition B moves this enumeration out of §2.3 (whose own version just says "(§21.6 names the grounds)") down to §21.6's closing paragraph (lines 3927–3933 in B — the one paragraph the full-tail diff shows added there relative to A's structure):
> "A verifier is unable to check a requirement on a capability or resource ground, and so reports *cannot establish* (`[R-CNF-11]`), as when the file names a format major version it does not implement, a record carries MUST_UNDERSTAND = 1 with a type it does not implement, it cannot execute a codec or filter (`[R-COD-11]`, §17.4), or it declines to decode a user-metadata document (`[R-MTA-09]`)."

Four grounds, not five: the "declines a layer's or a tile's decode on resource grounds" ground — with its citations to R-ERR-04, R-SER-05, and R-SER-08 — is simply absent from B's enumeration. Confirmed by `grep -n "R-SER-05\|R-SER-08"`: 21 hits in A, 20 in B, the missing one being exactly A's line 228; every other hit pairs up at a parallel offset. The underlying rule is not entirely lost from B — §9.7 (byte-identical in both editions) separately says "one that declines a tile's decode on resource grounds reports that check unmade and cannot certify (`[R-CNF-11]`, `[R-ERR-04]`)" — but B's canonical, purportedly complete list of cannot-establish grounds (the passage that answers "what are the grounds," which is exactly V1's second half) is short one entry relative to A's canonical list.
- **Kind: LOSS** (of completeness in an enumerated, closed-seeming list; A states five grounds, B's parallel list states four, and B's list is the one both walkers' own algorithms cite as authoritative for "the grounds").
- **Byte-level test:** partial. Because §9.7 (identical in both editions) independently states the same substantive rule in prose, an implementer who reads the *whole* document, not just the enumerated list, reaches the same behavior either way — which is exactly what walker B's own V1 answer did (citing "§21.9's closing paragraph" / "step 10" rather than an explicit ground-5 in its list). An implementer who trusts B's §21.6 list as exhaustive (a reasonable reading, since it is phrased as the "cannot establish" grounds), and does not separately notice §9.7's "cannot certify" language implies the same verdict, could under-enumerate the grounds it reports by name under R-CNF-11's per-requirement reporting duty — a difference in the *report*, not necessarily in the accept/reject/certify verdict itself.

### cmp-verifier-06 — a worked figure (F14/F5/F15) illustrating the "reach" test is dropped from B, though the concrete reaching-row list survives elsewhere unchanged

Edition A closes §2.3's "reach" paragraph with a Note (lines 283–294):
> "**Note.** The test is the invariant a condition violates, not the fields it reads, and three rows show why the distinction carries the weight. §21.2's F14 reaches although the bytes it checksums include fields a future major may redefine: it consumes them as CRC input and asserts only `[R-CNT-24]`'s CRC-32C at F − 4 over [F − 64, F − 4). F5 does not reach although its subject is the physical file size, which no major can redefine: the 128-byte floor it asserts is derived from a directory of at least 4 bytes at an offset of at least 16 and a 64-aligned F (`[R-CNT-27]`), and those are format major 1's. F15 does not reach although its Governing rule cell cites `[R-CNT-24]`: the trailer bytes it requires be zero are inside the 48 that rule lets a future major redefine."

Edition B's parallel paragraph ends instead with a single terse sentence and no Note at all: "…no §21 row records such a file. §21.2 lists the rows that reach. `[R-CNF-13]`" (B lines 288–290). Confirmed by `grep -n "F14 reaches"`: 1 hit in A, 0 in B (control: `grep -n "lists the rows that reach"` hits B once, proving the search mechanics work and this really is an absence).

Mitigating factor, checked directly: §21.2's own opening paragraph — byte-identical in both editions — already states the concrete answer ("Deriving it there yields F8, F14, F6 and both of F1's instances… and no other row"), so an implementer who reads §21.2 (which every implementer must, to build the register) gets the correct, complete list of reaching rows regardless of edition. What B's rewrite drops is only the *worked, negative* half of the explanation — why F5 and F15, which look like plausible reach candidates on a superficial reading, do not reach — a "worked figure" per the fidelity test's own definition of LOSS, even though it sits inside a `Note` (non-normative under R-CNF-01 in both editions) and does not, on the evidence available, change any accept/reject verdict since the operative list is preserved verbatim at §21.2.
- **Kind: LOSS** (of a worked, explanatory figure; low severity given the mitigating factor).
- **Byte-level test:** no, on present evidence — the operative reaching-row list an implementer would actually code against (§21.2's opening paragraph) is unchanged. The loss is pedagogical/audit value (an implementer extending the registry for a hypothetical format major 2, or double-checking F5/F15's classification independently rather than trusting §21.2's assertion, has to redo the invariant-vs-bytes-read reasoning from scratch in B).

### cmp-verifier-07 — shared, not introduced: verifierb-02 and verifiera-01 are each present in the other edition too

Documented under Part 1/Part 2 above; restated here as its own item because the charter asks explicitly whether a walk's own finding is edition-specific. Neither is:
- **verifierb-02** (§20.3 step 4 cites R-ERR-01 where §21.7's own unwitnessed-condition test seems to fit better) is argued entirely from §20.3 step 4 and §21.7, both confirmed byte-identical in edition A. If it is a real document defect, it is A's defect too, inherited unchanged, not something B's rewrite introduced.
- **verifiera-01** (the pre-trailer pad's minimum-but-not-exact length means verifier-reported slack totals are not unique across conforming writers) is argued entirely from §6.2/R-CNT-05, confirmed byte-identical in edition B. It applies to B's files identically; walker B simply did not name it as a formal finding despite relying on the identical minimal-pad assumption for its own V3 arithmetic.
- **Kind: EQUIVALENT** (no divergence between the editions at the passages either finding depends on) / **OBSERVATION** (about walker coverage, not about the specification). **Byte-level test:** not applicable — there is no edition difference to test.

---

## Evidence summary (see also the structured `evidence` object)

Every quotation above was taken directly from a `Read`/`sed` pass over one of the two permitted spec files, at the line numbers cited (which I verified are stable against the actual file — I re-`sed`'d each quoted range immediately before writing it into this transcript, rather than trusting an earlier paraphrase). No quotation is reconstructed from memory or from the two transcripts' own quotations without re-checking against the source file.
