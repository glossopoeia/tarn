# Triage pass — implementer-consequence lens

## Disclosure

A relayed "user request" ("Go") was prepended above the computed brief by the
harness. Per the brief's own instructions this is the launcher's message that
started this round, carried out before this pass was spawned; it is not a task
for this pass, needed no reconciliation with the brief, and was not treated as
widening the access rule below. Disclosed per the brief's instruction, not
repeated further. Separately, this session's environment carries a project
CLAUDE.md/AGENTS.md pointer and a user memory index (MEMORY.md) that were
present in context before this task began; neither was read as part of this
task (the access rule names only edition A, edition B, and the transcript
glob), and neither is treated as evidence for any finding below.

## Access actually used

- Edition A: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`
- Edition B: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
- No transcript file was opened this pass beyond what the brief itself quotes;
  the 29 findings' quotes, line numbers and reasoning as given in the brief
  were taken as the reporters' claims to verify, and verification was done by
  reading edition A and edition B directly (grep for short fragments, with
  whitespace/hard-wrap allowance, plus `sed -n` line windows), not by reading
  the walk transcripts a second time. No directory was listed; files were
  opened by the exact names the brief and the `out/` listing gave.

## Method

For every finding whose consensus could plausibly be LOSS, ADDITION, or a
disputed REPORTER_ERROR, the cited passage was pulled from both editions by
line number and compared directly, with a control grep for a key phrase to
confirm presence or genuine absence (never inferring absence from one `sed`
window). Findings that already rested on two reporters agreeing the text is
byte-identical were spot-checked rather than independently re-derived from
zero, given 29 findings and a shared budget across three independent passes.

Checks performed, with results:

1. **§17.4 / R-COD-11** (A:2630-2647, B:2509-2524) — pulled in full both
   editions: byte-identical (only wrap differs). Confirms cmp-reader-01's
   claim that the reader-capability sentence is present, unchanged, in both,
   and that readera-01's "no equivalent text binds an ordinary reader" claim
   is simply wrong — the sentence is in the very paragraph readera-01 cites.
   Also confirms cmp-verifier-03's and cmp-verifier-06's claims that the
   verifier-vs-reader reading trap (if real) is edition-neutral, and
   verifierb-01's "two meanings" point rests on the same identical text.

2. **Incompat lane / §10.1 vehicle list** (readera-02, cmp-reader-03) — the
   vehicle-list entry and F19 are architectural/register content unrelated to
   the readable-prose pass; spot-checked that §10.1's four-item list and the
   trailer flags row are unchanged between editions (consistent with the
   edit log's scope, which does not touch §10.1 or the register).

3. **§2.4 R-CNF-07 vs §21.1 Detector-is-verifier** (verifiera-01,
   cmp-verifier-02) — pulled both: the operative sentence ("the outcome
   names\nthe scope at which the damage is recorded, not an obligation on any
   reader") is at A:3837-3838 and B:3662-3663, byte-identical.

4. **§20.3 step 4 fixed-declaration bar** (verifiera-02, verifierb-02,
   cmp-verifier-04, writerb-01) — pulled A:3207-3300 and B:3059-3150 in full:
   byte-identical in substance (only wrap/dash-vs-comma differs). The
   "unwitnessed" property, the T-row symptom list, and the no-padding/no-edge
   -tile case writerb-01 works out all rest on this same unchanged text.

5. **§7.2 R-CNT-12 Note vs §20.4 governing-flags table** (writerb-02) —
   pulled A:1038-1044 and B:872-877 (Note) and A:3503-3519 / B:3338-3354
   (table paragraph): byte-identical between editions. Re-reading the Note
   itself: its operative sentence is "An updater that **does not implement**
   an MU = 1 record's type never drops the record" — already scoped to the
   not-implemented case, matching §20.4's "so for an implemented type only
   the PE bit bites" exactly. The two passages do not in fact disagree; the
   apparent contradiction in writerb-02 comes from quoting only the Note's
   three-state classification sentence and dropping the sentence right after
   it that supplies the scope. Graded REPORTER_ERROR, not LOSS/ADDITION, and
   in any case edition-neutral (identical text, so not an A-vs-B question).

6. **R-SLB-05 / §20.1 Writer tiers** (writera-01, writera-02) — pulled A:3150
   -3180 vs B:3004-3034 (creator/rewriter) and spot-checked R-SLB-05's six
   occurrences in each file: all identical in substance. Both findings are
   genuine single-edition observations about freedom the document grants, not
   fidelity differences.

7. **§6.2 trailer gates** (quizb-01) — pulled A:849-862 vs B:725-738: the
   three-gate ordered list, then the unordered "MUST validate all of the
   following" list, is byte-identical in both editions. The reported
   ambiguity (no stated priority inside the second list) exists equally in A,
   so it is not something B introduced or removed.

8. **§3.3 "Container and array model"** (swab-03, adv-01) — confirmed by
   heading grep (`^#### 3\.`): A has 3.1, 3.2, 3.3; B has only 3.1, 3.2.
   Confirmed by content grep: "load-bearing", "independent of Part",
   "cannot decode" all return zero hits in B outside the unrelated
   §11.4/§14/§12.3 "load-bearing" uses that also exist in A. Genuine,
   confirmed LOSS of an explanatory (non-normative, no requirement ID) block
   with no restatement anywhere in B.

9. **F14/F5/F15 worked Note after R-CNF-13** (swab-01, cmp-reader-02) —
   pulled A:285-296 vs B's corresponding position (B:295-297): A's three-row
   worked derivation is replaced in B by the single sentence "§21.2 lists the
   rows that reach." Confirmed genuine LOSS; confirmed the register's own
   enumeration of which rows reach (§21.2) is unaffected, so no currently
   -registered row's outcome changes.

10. **§2.4 "reject"-scope Note** (swab-02) — grepped "implementation
    technique" / "unusability": A has two hits (the §2.1 phrasing-discipline
    Note, and this one at A:341-342); B has only the §2.1 hit. Confirmed
    genuine LOSS, no normative consequence (no MUST/SHOULD inside the Note).

11. **R-ENC-08 Note** (swab-04) — pulled A:505-511 vs B:404-410 (the
    `#### 4.4 Bit numbering` section): A's clarifying Note is present, B's is
    absent, confirmed by R-ENC-08's single remaining citation in each file
    being the defining paragraph only. Confirmed genuine LOSS, no normative
    consequence given §14.3's own explicit (§4.4) cross-reference survives
    unchanged in both editions.

12. **Negative carve-out: experimental-range user-metadata is not a
    cannot-establish ground** (swab-05) — pulled A:230-237 (full §2.3
    Conforming-verifier bullet) and the corresponding relocated paragraph in
    B's §21.6 (B:3905-3930). Confirmed: B's §21.6 paragraph lists the five
    positive grounds and stops; a control grep for "not such a ground" /
    "nothing is left unchecked" returns zero hits anywhere in B. Confirmed
    genuine LOSS. The underlying table row (the one that actually decides the
    verdict for this case) is unchanged, word-for-word, at B:3877 and
    A:4053, so the verdict itself does not change; what is missing is the
    sentence that would let a reader derive it from §21.6's prose alone
    rather than cross-checking the table.

13. **MU=1-unimplemented-type / experimental-range derivation clause**
    (cmp-verifier-01, cmp-verifier-05) — pulled A:180-190 vs B:223-231 (the
    Conforming-reader bullet): confirmed A's italicized derivation clause
    ("— in a conforming file such a type is necessarily from the
    experimental range, since a reserved-range type carrying MU = 1 is
    itself a violation —") and its citation breakdown ("§21.9's R-ERR-04
    governs... §21.6's closing paragraph names the other two") are both
    absent from B, replaced by the bare "(§21.9)". Confirmed genuine LOSS.
    F35/F36 (register rows that independently license the same conclusion)
    are unchanged, word for word, in both editions' §21.2, which is why
    cmp-verifier-05's observation holds: both walks' V2 answers converge on
    the same verdict via different citation routes.

14. **New §15.4 Rationale with two worked MiB figures** (swab-06) — matches
    the repository's own commit history (`39c2ff5 Readable: §15.4 — a
    Rationale for segments...`), i.e. a maintainer-reviewed intentional
    addition, not an accidental drift. The two figures (≈19 MiB / 190 MiB)
    follow by arithmetic from §15.1's unchanged 20-bytes-per-entry fact.
    Graded ADDITION, byte-level false (non-normative Rationale explaining an
    unchanged, already-normative design).

15. **§16.2 Note→Rationale relabel with added material** (swab-07) — matches
    commit `03b5329 Readable: §16.2 — the slab-scope Note made a Rationale
    that says what slabs are for`. The underlying R-SLB-01..05 rules are
    unchanged; the block gains explanatory sentences. Graded ADDITION
    (new prose stating a consequence/role — A_slab's job — that A's Note did
    not spell out, though the rules themselves are unaffected),
    byte-level false.

16. **Preface "how to read this document" relocated and trimmed** (swab-08)
    — the dropped sentence's two component facts (identifier stability;
    vectors citing requirement identifiers) are independently, unchangedly
    present at §2.2 and §24/R-VEC-02 in both editions (not independently
    re-verified line-by-line this pass, given swab-08 already names the exact
    surviving locations and both are outside this pass's §3/§15-17 spot
    checks); graded EQUIVALENT as reported.

## Groups, verdicts and severities

See the structured result for the 17 groups, their member ids, the quoted
locations, consensus, byte-level call and recommended action. Headline: of
the 29 reported findings, **zero** describe a difference that would make an
implementation built from edition B alone emit different bytes or reach a
different accept/reject/cannot-establish verdict than one built from edition
A alone, on any file. Every confirmed LOSS is explanatory/non-normative
content (a Note, Rationale, or derivation clause) whose removal leaves the
governing requirement, register row, or table unchanged and still decisive;
every confirmed ADDITION is non-normative Rationale text explaining an
already-decided, unchanged design; and a large fraction of the raw findings
(§17.4/R-COD-11, the incompat lane, §2.4 vs §21.1, §20.3 step 4's
unwitnessed-change cluster, the MU=1/PE=0 reading, writer-chosen offsets,
creator/rewriter self-declaration, and §6.2's unordered check group) are
single-edition ambiguities/observations that exist, word-for-word, in both
editions, and so are not fidelity differences between A and B at all — some
are reporter misreadings (the R-COD-11 one demonstrably so; the MU=1/PE=0
one on closer reading of the full Note sentence), the rest genuine but
edition-neutral drafting questions for the maintainer to resolve in both
editions alike, not a B-only defect.

## Coverage

All 29 input ids are listed as group members exactly once; counted by hand
against the id list in the brief and against each group's member_ids before
submitting.
