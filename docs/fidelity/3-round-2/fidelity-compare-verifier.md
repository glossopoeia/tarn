# Verifier comparator — working transcript

## Disclosure (mandatory)

- A relayed "user request" (the single word "Go") was prepended above the brief by the
  harness. It is the launcher's message to the orchestrator, carried out before this
  session was spawned. It is not a task for me, needs no reconciliation with this brief,
  and does not widen the access rule.
- My runtime placed material in context before I began that I did not ask for: a
  CLAUDE.md pointer, a long user auto-memory index (many TARN-titled entries), a
  git-status block, attribution instructions for commits/PRs, and tool-availability
  reminders. None of it is part of the TARN specification. I disregarded all of it for
  every substantive judgment below and did not open the memory file or let its entry
  titles (several of which name methods similar to this brief's own, e.g. grepping a
  rule's every phrasing) shape which checks I ran; every method below comes from this
  brief alone.
- I read exactly the four permitted files and nothing else: edition A
  (`scratch/cleanroom/editions/a/tarn.md`, 4,981 lines), edition B (`spec/tarn.md`, 4,755
  lines), and the two transcripts (`transcript-verifier-a.md`, 745 lines;
  `transcript-verifier-b.md`, 583 lines). I did not list any directory other than
  creating my own scratch directory with `mkdir -p`. All reads were done with the Read
  tool directly (full files were read via the earlier large Bash `cat -n` attempts, whose
  oversized output was persisted to tool-result files and then read with the Read tool —
  these tool-result files are local copies of the exact same permitted files' content,
  not a different file); all comparisons below are grep/sed excerpts of the two
  permitted spec files plus the two permitted transcripts.

## Sweeps run (with hit counts and controls)

1. `grep -n "cannot establish"` — A: 6 hits (lines 220,239,249,2618,2621,2729); B: 8 hits
   (252,266,2461,2464,2574,3869,3892/4752-ish). Both nonzero; read in context.
2. `grep -n "R-CNF-11"` — A: 15 hits; B: 14 hits. Read every §2.3/§21.6/§21.7 occurrence
   in context in both files (see below).
3. `grep -n "F35\|L24 of L25\|strict specialization\|is an instance of"` in both files —
   confirmed the specialization-list sentence ("F1's front-block instance of F6... F35 of
   F36, L24 of L25, F21 of F22 and L10 of L11... this list is not offered as closed") is
   byte-for-byte identical in both editions (A lines ~3766-3772; B lines ~3561-3568),
   modulo one punctuation substitution (A's em-dash "—" vs B's parenthetical, and A's
   "declares" wording difference noted separately below).
4. `grep -n "R-WRT-04\|R-WRT-05"` and `grep -n "R-LIF-02"` in both — same line counts and
   same citing contexts; read the full §20.3 step 4-6 block and the three worked-example
   call-outs side by side (A lines 3380-3470; B lines 3186-3270) — identical prose
   (punctuation-only differences: em-dash vs parenthesis, "is" vs ":" before a list).
5. `grep -n "declared where it arises\|binds the writer and never makes"` — A: 1 hit
   (line 179, "declared where it arises rather than enumerated here"); B: 1 hit (line
   218, "binds the writer and never makes a file nonconforming") — **zero overlap**: this
   is the one substantive textual difference found (see cmp-verifier-02 below). Control:
   re-ran as `grep -n "R-CNF-02"` in both (A: 7 hits, B: 7 hits) and read the full
   enclosing bullet in both (A lines 160-179; B lines 208-219) to confirm the zero is a
   real textual absence and not a hard-wrap artifact — the surrounding bullet in B simply
   never names the three illustrative cases A names.
6. `grep -n "gap longer than\|longer than.*pad"` — A: 2 hits; B: 0 hits. **Control run**
   before treating this as a loss: re-read A's and B's full pre-trailer-pad paragraphs
   (§6.2, A lines ~847-856, B lines ~714-721) side by side. B states the same rule with
   different wording ("a longer gap is conforming, though no conforming commit produces
   one" vs A's "a longer gap is conforming, and no conforming commit produces one") — the
   zero was a wording artifact, not a loss; confirmed EQUIVALENT and dropped as a
   candidate finding.
7. `grep -n "ignore-lane bit\|set-no-other\|flags = 0"` in both — both nonzero, read in
   context (A lines ~902-910; B lines ~767-773): "A set ignore-lane bit is nevertheless
   not a file-conformance violation" is present in B too. Confirms the specific
   conduct-rule content R-CNF-02 illustrates in A is independently and identically stated
   at its own section in B, even though R-CNF-02's own paragraph in B omits the
   cross-reference.
8. `grep -n "does not depend on reconstructing\|Nothing here enumerates prior"` — A: 1
   hit; B: 1 hit; read the whole §9.7 closing Note in both — identical text.
9. `grep -n "R-CNT-12"` — same count pattern, read full defining paragraph (A lines
   1020-1034; B lines 850-865*, actually confirmed at the printed excerpt) — byte-
   identical.
10. `grep -n "120 conditions\|277 instances"`, `grep -n "entry_count.*20\|65,536"` — both
    present in both files with identical formulas and figures.
11. `grep -n "how many commits\|not recoverable from the live trailer"` — same count and
    context in both.
12. §17.4/R-COD-11 full paragraph (A lines 2595-2630; B lines 2440-2473) read side by
    side in full — byte-identical except two purely typographic substitutions (em-dash
    vs comma before a clause).
13. §21.6 full table and closing paragraphs (A lines 4016-4090; B lines 3807-3880) read
    side by side in full — the inline grounds-enumeration that sits inside R-CNF-11's own
    paragraph in A (the "as when the file names a format major version..." clause) is
    absent from B's R-CNF-11 paragraph but present, essentially verbatim, as §21.6's own
    closing paragraph in B ("A verifier is unable to check a requirement on a capability
    or resource ground, and so reports *cannot establish* (`[R-CNF-11]`), as when the
    file names a format major version it does not implement..."). This is a
    relocation/compression, not a loss — confirmed by reading both completely; see
    cmp-verifier-03 below (EQUIVALENT).

No web search, no other file read, no git command, no directory listing beyond my own
scratch directory's creation.

## Probe-by-probe comparison

### V1 — verdict vocabulary

Both walkers answer identically in substance (three verdicts; unexamined is not a
verdict; priority rule). The texts differ only in *where* the grounds for "cannot
establish" are spelled out: A's R-CNF-11 (§2.3) paragraph inlines the five grounds and
the experimental-range-encoding carve-out directly; B's R-CNF-11 paragraph says only
"(§21.6 names the grounds)" and the same five grounds (word for word, modulo the
inline/table split) are given in §21.6's own closing paragraph in B. Read side by side in
full (see sweep 13), these are the same rule, reorganized — EQUIVALENT. Both walkers
quoted their own edition correctly and neither mis-stated the rule. No finding beyond the
reorganization noted at cmp-verifier-03.

### V2 — reserved vs. experimental range

Substantive agreement on outcomes (reserved → nonconforming; experimental → conforming
file, reader rejects, verifier reports cannot establish). But the two walkers'
*register-row* reasoning diverges: verifier-a's answer says F35 and F36 "both fire"
as if they are two independent findings on the reserved-range/MU=1 case; verifier-b's
answer explicitly invokes §21.1's specialization rule and says the file is "recorded
against the narrower row F35" alone (F36 not separately recorded).

I checked §21.1's specialization-list sentence in both editions (sweep 3) and it is
byte-for-byte identical: "...F35 of F36, L24 of L25, F21 of F22 and L10 of L11 stand in
that relation... the file is recorded against the narrower row." Edition A's own text
therefore states the same narrowing rule verifier-b used, and verifier-a's own charter
write-up (its "Every register row's detector and outcome" section) *also* lists "F35
within F36" as one of the specialization pairs — so verifier-a's V2 answer is
inconsistent with a rule verifier-a itself correctly identified elsewhere in the same
transcript, from the same (A) text. This is a **REPORTER_ERROR** by verifier-a, not a
text difference: both editions say the same thing, and only one walker applied it
correctly at V2. It does not change the byte-level verdict (nonconforming either way,
since F35 alone already fixes reject-file), so it is not byte-level-divergent, but it is
a genuine misreading. → **cmp-verifier-01**.

### V3 — three-generation arithmetic

Both walkers produce identical numbers (F1=4,480; F2=13,120; F3=14,528; live=12,816;
slack=1,712), from identical rule citations (R-LIF-02 step 5, R-WRT-04, R-WRT-05,
R-CNT-17's entry_count formula, R-CNT-05/R-CNT-03 for the pad). I verified the governing
texts (§20.3 steps and worked examples, §15.1's formula, §6.2's pad paragraph) are
identical in both editions (sweeps 4, 6, 10). EQUIVALENT; no finding.

### V4 — codec the verifier cannot execute

Both walkers give the same verdict (cannot establish, MUST NOT certify) and both flag the
identical tension between R-CNF-03's absolute "no subset profiles" bar and R-CNF-11/
R-COD-11's apparently unconditional cannot-establish ground for an unexecutable codec, as
their respective ambiguity finding (verifiera-01 / verifierb-01). I read §2.3's
Conforming-reader bullet (R-CNF-03) and §17.4 (R-COD-11) in full, side by side, in both
editions (sweep 7, sweep 12) — they are identical (modulo cosmetic punctuation). This is
the same textual gap present equally in both editions; the rewrite neither introduced nor
resolved it. → **cmp-verifier-04** (EQUIVALENT: identical ambiguity, carried over
unchanged — not an edition-specific LOSS or ADDITION).

### V5 — cross-generation declaration change

Both walkers reach the same conclusion (invisible to certification in general; one
narrow class of symptomatic rows can incidentally surface it; no verdict follows from the
unwitnessed case itself). I verified §9.7's closing Note, §20.3 step 4's bar and its
"no register row records the violation itself" sentence, and §21.7's "unwitnessed"
definition are byte-identical between editions (sweeps 4, 8, and the direct §21.7 text
read in full). The one real textual difference I found anywhere in this probe's
supporting material is R-CNF-02's own definition bullet (§2.3): edition A gives three
named illustrative examples of writer-conduct rules (the ignore-lane-bit rule, the
pre-trailer-pad-length rule, and the §20.3 step 4 bar on changing a layer's fixed
declarations) and closes with "...and each is declared where it arises rather than
enumerated here." Edition B's R-CNF-02 bullet states only the general rule ("A writer
obligation that governs conduct rather than output... binds the writer and never makes a
file nonconforming") with no illustrative list and no "declared where it arises" framing
sentence.

I then checked whether the three examples' own normative content survives at its own
point in B (sweep 7 for the ignore-lane bit; sweep 6 for the pre-trailer pad; sweep 4/the
full §20.3 step 4 text for the declaration-change bar) — in every case it does, word for
word or with only cosmetic rewording. So this is a loss of an *aggregating cross-
reference and its illustrative list*, not a loss of any rule a verifier implementation
would need: an implementer who reads all of B (not just §2.3) still learns, at each
example's own place, that it is a conduct rule that never makes a file nonconforming. By
the byte-level test, this changes no implementation's accept/reject output. →
**cmp-verifier-02** (EQUIVALENT in effect, though a real prose/organization difference —
reported because the brief asks for every difference found, not only the ones that bite).

### V6 — MU=1, PE=0

Both walkers agree in full (verifier treats the combination as a validity error at the
record's governing scope; file scope/F25 for a non-layer top-level record, layer scope/
L46 for a layer record or sub-record; ordinary readers/updaters merely read PE as 1 and
are not obliged to reject). I read §7.2's full R-CNT-12 paragraph and the F25/L46 register
rows in both editions (printed above) — byte-identical. EQUIVALENT; no finding.

## Each walk's own findings, checked against the other edition

- **verifiera-01 / verifierb-01** (same ambiguity, independently found by both walkers):
  whether software lacking a core/assigned codec or filter can be a "conforming
  verifier" at all, given R-CNF-03's absolute bar vs. R-CNF-11/R-COD-11's apparently
  unconditional cannot-establish ground. I confirmed above (V4) that the supporting text
  is identical in both editions. This is not a defect either edition introduced or
  removed; it is in the source material both editions carry forward unchanged. →
  recorded as cmp-verifier-04, EQUIVALENT.
- **verifierb-02** (OBSERVATION; no edition-A counterpart listed as a standalone
  finding): that a cross-generation declaration change is, by design, invisible to
  certification except via a short list of symptomatic rows. Verifier-a's transcript
  covers the identical substance within its V5 answer (same quotations, same rows T2-T5/
  T14/T17/T21/T22/T24/T25, same §21.7 "unwitnessed" framing) but did not promote it to a
  separate "Findings" entry — a difference in what each walker chose to write up as a
  finding, not a difference in what the two texts say. I re-read §21.7's full text in
  both editions (printed above) and it is identical. Not an edition-specific defect. →
  folded into cmp-verifier-04's EQUIVALENT note; not a separate LOSS/ADDITION.

## Places a walker had to guess or re-read, checked against the other walker

- Verifier-a's transcript explicitly budgets attention away from §24's vector table
  ("§24's header was located but its vector table itself was not needed... time/scope
  budget spent on §21's register instead"). Verifier-b does not mention skipping
  anything comparable; it claims a full five-chunk read of all 4,755 lines with no gaps.
  This is a difference in reported thoroughness, not a text difference — §24 is not cited
  by either walker's probe answers or findings, so it does not bear on any probe or
  finding above. No finding raised.
- Verifier-b self-reports a disclosed access breach (ran `ls` on the shared output
  directory) that verifier-a does not have a counterpart for (verifier-a instead
  discloses running `ls -la` on the output directory after copying its own transcript in
  — a comparable, separately-disclosed breach of the same "don't list that directory"
  instruction). Both breaches are disclosed, scoped to filenames only, and neither walker
  reports reading another agent's file contents or letting the listing affect any
  substantive answer. This is procedural, not textual, and outside this brief's charter
  (which is about the two *editions*, not the two walkers' access discipline); noted here
  for completeness but not raised as a cmp-verifier finding.

## Evidence summary (also given in the structured result)

See the `evidence` object in the structured result for the four required sentences.
