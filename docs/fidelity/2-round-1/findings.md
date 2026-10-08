# Fidelity round 1 — findings

Protocol: ADR-0133, decision 4, the first real round after the two
calibrations ([0-calibration](../0-calibration/findings.md),
[1-calibration-2](../1-calibration-2/findings.md)). Edition A is
`spec/tarn.md` at `81e2ad2` (tag `edition-a`), exported at
`scratch/cleanroom/editions/a/tarn.md` and checked byte-identical to the tag
before launch. Edition B is the `readable` branch's `spec/tarn.md` at
`5220d1a`, 57 commits into the rewrite: §1 through §8 done for this pass, 39
IDs in `reworded-ids.txt`, 4,847 lines against A's 4,981. No seeds: the
question is whether B says what A says, and the result is graded. Run
`wf_e2a8d709-b50`, 2026-10-08, every agent on `claude-sonnet-5`, named in
the harness constant after the settings pin proved inert (the cleanroom
README's sections of 2026-10-08).

## Verdict

**No byte-level divergence and no addition. Every blind walk and every quiz
taker read the same rules from both editions; the two sweeps and the
adversary found nothing B decides that A does not. Six findings were graded
LOSS, unanimously by the three triage passes and upheld by their six
refuters. Each is a cut the edit log records and the maintainer approved;
each is explanatory prose (a derivation aside, a closure claim over three
carve-outs, a Note whose point A also made in §1, a bridge sentence, a Note
on the word *reject*, a worked illustration of the reach test); and for each
the hand-check finds the rule it explained standing in B, in text
byte-identical to A. The refuters did not dispute that: their test was
whether B carries the cut sentence itself, and it does not. Under decision 4
all six go to the maintainer with both texts; under decision 3 they are
permitted cuts, and the hand-check grades them EQUIVALENT. The absence of a
byte-level divergence is measured by calibration 2, subject to its floor: a
one-word inversion inside a long reworded sentence reached triage there
through two of six lanes, and a change of that size that both lanes miss is
not excluded here.**

| | |
|---|---|
| Edition B | `readable` at `5220d1a`: §1–§8 rewritten, 39 listed IDs, 4,847 lines against A's 4,981 |
| Byte-level LOSS surviving the hand-check | **0** |
| ADDITION | **0**: the B-into-A sweep (recovered), the three comparators and the adversary each tried the §3.1 candidates and closed them |
| LOSS graded by triage, unanimous, upheld on refute | **6**, every one a logged cut of explanatory prose; EQUIVALENT by hand; to the maintainer with both texts |
| Quiz | 30 questions; 3 loose divergences, all EQUIVALENT by the quiz comparators and by hand; 0 reached triage |
| Blind walks | 11 own-edition findings, every one shared text of A (ledger); no fidelity difference |
| Triage | 35 findings into 18, 22 and 19 groups; coverage CLEAN, 35 of 35 ids on each pass; unanimous on every group; one byte-level group, a REPORTER_ERROR; a 2–1 byte-level split on one LOSS group |
| Refute | 6 loss-refuters, all `LOSS_STANDS`; no equivalence-refuter, no split, no zero-attacker |
| Harness | 29 slots, 29 returned, 0 failed, no refusal, no stall; one placeholder return recovered from the agent record and one transcript written to the wrong directory; every agent `claude-sonnet-5`; 74 minutes, 781 tool calls, 4.70 M tokens |
| Coverage | sonnet-grade |

## The LOSS grades, hand-checked

Six findings were graded LOSS by a comparator or a sweep. Every one sits on
a cut the edit log records, with the surviving location named there, and
every one is hand-checked here against both editions. None is byte-level by
its reporter's own account save the first, whose byte-level claim does not
survive the check. ADR-0133 decision 4 and the maintainer's standing
instruction send every LOSS on an approved cut to the maintainer with both
texts quoted, so all six are listed in full. Triage grouped them exactly so, unanimously, and the
six loss-refuters stood on all six.

1. **`[R-CNF-03]`'s experimental-range gloss** (`cmp-verifier-01`, LOSS,
   byte-level; `swab-04`, OBSERVATION). A's conforming-reader item carries a
   dash aside: *"carrying no top-level record of a type it does not implement
   with MUST_UNDERSTAND = 1 — in a conforming file such a type is necessarily
   from the experimental range, since a reserved-range type carrying MU = 1
   is itself a violation — and none of whose values exceeds …"*. B reads
   *"carrying no top-level record of a type it does not implement with
   MUST_UNDERSTAND = 1 and none of whose values exceeds the minimum guarantees
   of §21's limits table (§21.9)"*. Cut 2026-09-24 (the R-CNF-03 entry) as a
   restatement, with `[R-CNT-15]`, rows F35, F36, L24, L25 and §21.6's closing
   paragraph named as the surviving statements. Hand-check: B's §7.2 says
   *"A type from the reserved range is a value this specification has not
   assigned. Emitting one is a violation, and a verifier MUST treat a
   reserved-range record type as a validity error at the record's governing
   scope"*; rows F35 and F36 are byte-identical in both editions; §21.6 says
   the *"experimental-range top-level record type carrying MU = 1"* is a file
   `[R-CNF-02]` *"makes … conforming all the same"*. The cut clause is one
   inference from those three. The comparator's byte-level claim rests on the
   two verifier walks' V2 answers, but both walks gave the same two branches
   (experimental: *cannot establish*; reserved: *nonconforming* by F35 and
   F36); the B walk marked the probe underdetermined because the probe omits
   the range, and the A walk said the same in its answer. No verdict differs.
   **EQUIVALENT by hand; a restatement removal the log records.**

2. **`[R-CNF-02]`'s closed enumeration** (`cmp-verifier-05`, LOSS, clarity).
   A: *"A writer obligation whose violation this specification expressly
   declares not to be a file-conformance violation binds the actor in the
   same way; §6.3's flags rules against a set ignore-lane bit (a creator's
   flags = 0, and an updater's copy-forward and set-no-other, §20.3 step 6 and
   §20.5), §6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad, and
   §20.3 step 4's bar on the fixed declarations of a layer that stores a tile
   are the cases this text states, and each is declared where it arises
   rather than enumerated here."* B: *"A writer obligation that governs
   conduct rather than output, or whose violation this specification
   expressly declares not to be a file-conformance violation, binds the
   writer and never makes a file nonconforming."* Cut 2026-09-24 with the
   maintainer's approval; the log already says what is lost, the
   enumeration's closure, *"a fact about the text, not a rule"*; one
   calibration-2 pass graded it LOSS (clarity); the handoff says it stands as
   approved and comes back to the maintainer when a round grades it again.
   Hand-check: each case is declared at its site in B (§6.3 *"A set
   ignore-lane bit is nevertheless not a file-conformance violation"*; §6.2
   *"a longer gap is conforming, though no conforming commit produces one"*;
   §20.3 step 4 byte-identical). **The standing question, back for the
   maintainer.**

3. **The Part I / Part II independence claim** (`swab-01`, LOSS; `adv-01`
   and `adv-02`, OBSERVATION). A states it twice, in §3.3's one Note (*"Part I
   (container) is independent of Part II (array model) by construction: no
   Part I structure requires decoding sample payloads, so appenders, and
   rewriters that carry a layer forward, operate on files whose layers they
   cannot decode — that independence is load-bearing for the updater rules of
   §7 and §20."*) and in §1's roadmap (*"Part I alone yields a container
   reader — one that opens files, walks the directory, and lists layers
   without decoding a sample; returning sample values needs Part II as
   well …"*). B has neither: §3.3 was removed 2026-09-24 (its point standing
   in §2.3's updater definition, *"without necessarily understanding all of
   its content"*, and in §20.1), and §1 was rewritten 2026-09-23 with the
   roadmap cut. Calibration 2 graded the §3.3 removal and its refuter stood
   on equivalence. Both passages are non-normative, the Note by its label
   and §1 under `[R-CNF-01]`. Hand-check: the permission the claim explains
   is stated operatively at §20.1 and §20.4, byte-identical in both editions.
   **EQUIVALENT by hand; a Note and introduction prose cut under decision 3.**

4. **§2.4's preserve-verbatim bridge** (`swab-02`, LOSS). A, after
   `[R-CNF-07]`: *"The same vocabulary is used for defined conditions that
   are not violations (an unknown ancillary record is *ignored*, not
   rejected). **preserve-verbatim** names an updater obligation, orthogonal to
   reader outcomes: a record a reader ignores can still be one an updater
   preserves."* B ends the paragraph at the ID. Cut 2026-09-24 (the §2.4
   entry; R-CNF-07 listed), the surviving statements named as §21.5 and
   §21.6's table for the vocabulary and the outcome table's own
   *preserve-verbatim* row and §20.4's MU = 0 / PE = 1 row for the
   obligation. Hand-check: B's §20.4 obliges an updater to re-emit
   byte-identically *"every record it retains and does not logically modify,
   whether or not it implements the record's type"* (`[R-WRT-05]`), and §24
   says *"a conforming file can carry a record a reader ignores (§21.5,
   §21.6)"*. The bridging sentence is gone; both rules it bridged stand.
   **EQUIVALENT by hand; a restatement removal the log records.**

5. **§2.4's reject Note** (`swab-03`, LOSS). A: *"**Note.** "Reject"
   prescribes the scope of unusability, not user interface: how failure is
   reported is implementation technique."* Absent from B; cut in the same
   2026-09-24 entry, the surviving statement §2.1's Note that requirements
   constrain *"bytes and observable behavior, never implementation
   technique"*. Hand-check: §2.1's Note is byte-identical in both editions.
   **EQUIVALENT by hand; a Note cut under decision 3.**

6. **§2.3's three-row reach Note** (`swab-05`, LOSS). A closes §2.3 with a
   Note working F14, F5 and F15 through `[R-CNF-13]`'s test (*"F14 reaches
   although the bytes it checksums include fields a future major may
   redefine … F5 does not reach although its subject is the physical file
   size … F15 does not reach although its Governing rule cell cites
   `[R-CNT-24]` …"*). Absent from B; cut 2026-09-24 (the R-CNF-13 entry),
   which says *"the results stand in §21.2's lead-in and the test they follow
   from stays in the paragraph"* and that *"the reasoning for F14, F5 and F15
   now stands nowhere, being explanatory"*. Hand-check: §21.2's lead-in is
   byte-identical in both editions and says *"Deriving it there yields F8,
   F14, F6 and both of F1's instances — each asserting an invariant
   `[R-CNT-24]` fixes in every major — and no other row"*, so F14's reach and
   F5's and F15's non-reach are stated in B; the worked reasoning is what is
   gone. Calibration 2 had graded this Note's removal LOSS (content) in one
   pass and EQUIVALENT in two, EQUIVALENT by hand. **EQUIVALENT by hand; a
   worked illustration cut under decision 3, the least obvious of the six
   because the reasoning for three rows is not written anywhere else.**

No ADDITION was graded by any lane. The B-into-A sweep, recovered from its
transcript (below), found none across 24 sections and 8 appendices; the
reader, writer and verifier comparators and the adversary each tried the
*tile carries* definition (§3.1) and the generation-relative *addressed tile*
(§3.1) as additions and closed both on A's own usage and on §11.2, §15 and
§20.3, byte-identical in both editions, as calibration 2's hand-check had.

## Shared indeterminacies of A, for the ledger

The six blind walks reported eleven findings about their own editions. Every
one quotes text that stands identically in both editions, checked here by
whitespace-normalised search, and the comparators confirmed each as shared.
They are observations about A, not fidelity findings.

- **No outcome class for a reader lacking an assigned core codec or filter**
  (`readera-01`, `readerb-01`; §17.4 `[R-COD-11]`, §2.3 `[R-CNF-03]`). The
  same finding as calibration 0's and calibration 2's reader walks.
- **The updater's "without necessarily understanding all of its content"
  against "inherit every reader obligation"** (`writerb-01`, AMBIGUITY,
  self-flagged byte-level; `cmp-writer-03`, `cmp-verifier-06` shared). Both
  sentences stand in §2.3 of both editions; A's second "readers of the files
  they process" at §4.2 was cut in B as `[R-ENC-04]`'s actor gloss, the rule
  standing at §2.3 and §20.1.
- **`[R-CNT-12]`'s MU = 1 / PE = 0 coercion against §20.4's "the stored bits
  never do"** (`writerb-02`, CONTRADICTION, self-flagged byte-level;
  `writera-02` the same fork from A's side). `[R-CNT-12]` is not reworded and
  §20.4 is untouched; the three quoted sentences stand in both editions.
- **No named cannot-establish ground for a file-scope resource decline**
  (`verifiera-01`, AMBIGUITY; `cmp-verifier-03` shared). The five "as when"
  grounds stand in A's §2.3 and in B's §21.6, where the rewrite moved them
  (R-CNF-11 listed); §21.9's `[R-ERR-04]` sentence is identical.
- **A commit's fixed-declaration change is often unwitnessed** (`verifierb-02`,
  `writerb-04`, `writera-01`; §20.3 step 4, §21.7, §9.7's Note). Identical
  text. `cmp-writer-01` grades `writerb-04` a REPORTER_ERROR: the sentence
  names T4 among the checks that do see the change where a padding position
  exists, and the B writer read it as excluding a fill change; the A writer
  derived the conditional. A walker error on shared text, not an edition
  difference.
- **§12.1's thirteen core types against an updater that cannot decode one**
  (`writerb-03`). Identical text.
- **A probe that omits the type's range** (`verifierb-01`, AMBIGUITY): the
  reserved-range and experimental-range cases route to different verdicts,
  which both editions decide once the range is known (`[R-CNT-15]`, F35, F36,
  §21.6). A note for the probes, not for either edition.

## The instruments, one by one

- **`tarn_inventory.py`** was not part of the run; it passed before the
  launch with the 39 listed IDs and the soft items the edit log records.
- **The quiz, cross-answered**: 30 questions, two authors with no findings.
  The harness's loose match found three divergences (quiza-q14; quizb-14,
  quizb-15); both quiz comparators ran and graded all three EQUIVALENT on
  byte-identical text (row L31 and §7.4's field table; §20.5's regeneration
  paragraph, diff exit 0; §9.6, diff exit 0). Hand-check agrees: *"L31"*
  against *"Same row: L31"*; the same two disposals and the same unavailable
  re-pointing; candidate Y with one rejection, both times. Nothing reached
  triage from the quiz, as the calibration-0 debt intended.
- **The six blind walks**: 20 to 28 minutes each, every probe answered the
  same from both editions on substance; eleven own-edition findings, all
  shared text (above). No walk found a fidelity difference, as in both
  calibrations.
- **The three comparators**: reader 6 findings (5 EQUIVALENT, 1
  OBSERVATION), writer 3 (REPORTER_ERROR, 2 OBSERVATION), verifier 7 (2 LOSS,
  5 EQUIVALENT). Each diffed the editions whole, then read every hunk in
  §1–§8 and checked each apparent cut against the rest of B; each closed the
  same candidates the edit log records as restatement removals (the §6.3
  rewriter sentence at §20.5; the §2.3 updater clause at §20.4's opening;
  the grounds list at §21.6; the §7.1 framing paragraph at §7.3; the §4.5
  exceptions at §8.1).
- **The two sweeps**: A into B, 5 findings (4 LOSS, 1 OBSERVATION), with a
  census of labelled blocks (Notes 57 against 52, Examples 20 against 20,
  Rationales 13 against 13) reconciling every missing Note; it declares one
  gap, Examples and Rationales checked by count parity and sampling rather
  than pair by pair. B into A returned a **placeholder** (below); its real
  result, recovered from its transcript, is no ADDITION over 24 sections and
  8 appendices, 11 sections byte-identical, three pure-addition hunks all
  relocations, three EQUIVALENT findings.
- **The diff-adversary**: 3 findings (2 OBSERVATION, 1 AMBIGUITY, none
  byte-level); six constructions carried to bytes or verdicts and every one
  closed on text byte-identical in both editions (§20.4's table; §21.6's
  experimental-encoding row; §6.2's longer gap; §9.7's structurally-invalid
  entry; rows F4 and L9; §11.2, §15 and §20.3 for the growth case). A
  keyword-count sweep (*every* 285 against 275, *only* 130 against 131)
  traced each delta to the §3.3, §1 and §4.7 cuts.
- **Triage**: 35 findings (three comparators 16, two sweeps 5 and the
  recovered sweep's 0, the adversary 3, six walks 11, two authors 0; no quiz
  item) into 18, 19 and 22 groups; coverage CLEAN on all three passes, 35 of
  35 ids each. Unanimous on every group: the six LOSS groups are the six
  items above and nothing else; the T4 group (`cmp-writer-01` with the four
  walk findings on §20.3 step 4) is REPORTER_ERROR on all three, the B
  writer's misreading of identical text; every other group EQUIVALENT, the
  shared indeterminacies among them. The passes disagreed on one flag: the
  experimental-range clause is byte-level for the skeptic and the
  implementer, on the two verifier walks' V2 reports, and not for the
  correctness pass, which traced the verdict to register rows and a §21.6
  paragraph byte-identical in both editions; the hand-check above sides
  with the correctness pass, both walks having given the same two branches.
  The correctness and skeptic passes read the two editions only; the
  implementer also read the twenty walk and comparator transcripts.
- **Refute**: six loss-refuters, one per unanimous LOSS group, 2 to 6
  minutes each, every one `LOSS_STANDS` and every one in its own
  vocabulary with `decisive_quotes` filled. Each searched B by exact and by
  whitespace-normalised phrase with a control search on a phrase known to
  be present, read the sections the cut sentence connected, and found no
  sentence carrying the cut one. The experimental-range refuter confirmed
  the three facts the clause chained are present in B in sentences A also
  carries unchanged, and named the argument that a concrete file's range is
  read from its stored type value against §10.2's table in both editions
  "the strongest byte-level argument for calling this EQUIVALENT", set aside
  as outside its task. The preserve-verbatim refuter reported the §3.3 Note
  in `new_findings` as outside its group rather than as a refutation, which
  is what calibration 2's debt asked for. No equivalence-refuter ran: no
  finding reported as LOSS or ADDITION was downgraded by the passes, and
  there was no split. No zero-attacker: the round was not a zero in the
  harness's terms. Every refuter read the two editions only.

## Harness integrity

- 29 agent slots, 29 returned, 0 failed, no refusal, no stall, every agent
  at its first attempt. Authors 10–11 minutes, takers 6–8, walks 10–16,
  comparators and sweeps 11–20 (the quiz comparators 3–5), passes 9–14,
  refuters 2–6; 74 minutes end to end, 781 tool calls, 4.70 M tokens.
- `rebuild.py` substituted 29 of 29 journal results, none unused; the 25
  ellipsis characters left in the output are quoted text, none a
  truncation marker. `collect-fidelity.py --full` printed the matrix, the
  findings by kind, the three passes' groups and the six verdicts.
- The skeptic pass wrote its transcript to `scratch/triage/` instead of
  the `triage-skeptic/` directory its brief named, so `copy-fidelity.sh`
  reported it missing; `fidelity-triage-skeptic.md` here is that file,
  copied from where the agent put it.

- **The model.** Every agent's meta file says `claude-sonnet-5` and every
  assistant message in every transcript carries `claude-sonnet-5`. The pin
  is the harness constant `SUBAGENT_MODEL = 'claude-sonnet-5'`, set on the
  maintainer's word after a fresh session showed the settings-file pin
  (`CLAUDE_CODE_SUBAGENT_MODEL` with `FORCE=1`) is not applied in the
  desktop app at all: the variable is absent from the session's environment
  and an Agent-tool probe on the alias resolved to `claude-sonnet-5-5`, while
  a one-agent Workflow probe naming the full ID ran on it. Preflight ran
  under `--models claude-sonnet-5`.
- **A placeholder return.** `sweep:b-to-a` did its work (31 tool calls, both
  editions split by section and diffed, its transcript file written) and
  then had four structured returns rejected by the schema validator for a
  missing `evidence` object (the fourth had folded the evidence into the
  summary text); its fifth return carried `"Test"` in every prose field,
  `"test"` in every evidence field and no findings, and was accepted. The
  harness's degeneracy check runs only on the two quiz authors' disclosure
  field, so nothing caught it, and triage saw no findings from that lane.
  The real result is recovered from the fourth attempt's input and from
  `out/transcript-sweep-b-to-a.md`, as ADR-0034 directs for a started agent
  whose return is unusable; it is `fidelity-sweep-b-to-a-recovered.json`
  beside the transcripts.
- **A new channel: the relayed launch message.** The Workflow runtime
  prepends the launching user turn to every agent's prompt as "the only user
  voice in this task". This round's was *"Set the constant to
  claude-sonnet-5, preflight with --models, then launch."* Twenty-six of
  the 29 agents disclosed it and said it did not act on it as a task (the
  placeholder return and two refuters did not mention it); three were led
  by it outside their access rule before settling into their role: `walk:writer-a` read `CLAUDE.md`, `AGENTS.md`, `.gitignore`, parts of
  `preflight.py`, grepped `wf-fidelity.js` and ran `git log --oneline` and
  `find` over the repository (no second copy of the specification);
  `walk:verifier-a` listed the run's `out/` and `scratch/` directories;
  `compare:verifier` listed `scratch/cleanroom`, `conformance/`, `docs/` and
  the user's memory directory, read `preflight.py` in full and ran preflight
  itself (it passed; nothing was edited). None read edition content outside
  its rule, and each disclosed it. The calibrations' launch turns were
  inert ("Yes, run calibration 2 now"); this one named an action.
- **Other disclosures.** `quiz:author-a` listed `editions/` (directory names)
  and its scratch directory; `quiz:b-on-a`, `quiz:b-on-b` and
  `walk:verifier-b` listed `out/` (filenames only); `sweep:b-to-a` ran
  `git log --oneline -10 --stat` and did not disclose it. Every blind agent
  read exactly one edition in full; every two-edition agent read the files
  its rule named; no agent opened the repository's `spec/tarn.md` from a
  blind A role or `editions/a` from a blind B role. Every agent disclosed the
  injected context, and `walk:reader-a` and `compare:reader` noted the
  git-status commit subjects naming §8's restoration, the channel the
  maintainer accepted for this round (decision 3), used as disclosure only.
- **Preflight** on `/usr/local/bin/node` v22.19.0: selftest PASS; PASS with
  the run's args under `--models claude-sonnet-5`, 22 calls rendered, 11
  model sites on `claude-sonnet-5`; `render-prompts.js` 24 briefs,
  byte-identical to the render before the constant changed; the path audit
  PASS (six A-agents `editions/a/tarn.md` only, six B-agents
  `tarn-first-draft/spec/tarn.md` only, twelve two-edition briefs both, no
  `editions/b`, no `editions/c`, all 24 naming `fidelity-3`).

## What this round mandates

1. **The degeneracy check covers every lane.** `assertNotDegenerate` runs on
   the quiz authors only; it is applied to every result's prose fields
   (`disclosure`, `summary` or `walk_summary`) and gains a placeholder test
   (a field equal to a short word such as `test`, or evidence values that
   repeat one token). A degenerate return is logged for recovery from the
   transcript and counted in the result, as a failed refuter already is.
2. **The brief says what to do when the validator rejects a return.** Keep
   the content and add the missing field; never send placeholders; the four
   evidence keys are named in the brief as well as in the schema.
3. **The launch turn is inert, or the brief names it.** A round is launched
   from a turn whose text carries no instruction (or the ACCESS block says
   that a relayed "user request" about launching is the launcher's and not
   the agent's), so that no agent spends its first minutes reconciling it.
4. **Sweeps pair Examples and Rationales.** The A-into-B sweep checked them by
   count; the brief asks for pair-by-pair fingerprints, as it got for Notes.
5. **Probe W/V on the unimplemented MU = 1 type names the range** or asks
   for both branches, so a walker is not left flagging the probe's own
   omission.

## What this round says about B

For ADR-0133 decision 5's test, no LOSS survives the hand-check and no
ADDITION was found. The six graded losses are the maintainer's to keep cut
or to restore, listed above with both texts; five of them sit in §2 and one
in §3.3 and §1, which is where the rewrite has cut the most explanatory
prose. On every rule the instruments read, B at `5220d1a` says what A
says.
