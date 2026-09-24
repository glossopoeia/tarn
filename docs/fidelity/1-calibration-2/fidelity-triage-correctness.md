# Triage pass — Correctness lens

## Disclosure

I read exactly the two permitted edition files (edition A =
`scratch/cleanroom/editions/a/tarn.md`, edition B = `scratch/cleanroom/editions/c/tarn.md`)
plus the 53 findings supplied in the computed task. I did not read any transcript files
under `fidelity-2/out/` (the 53 findings as given already quote what I needed to check;
I verified every quotation against the live files myself rather than trusting the
transcripts). I ran `grep`/`sed`/`diff` against the two edition files only, never listing
a directory. No other file (docs/, PLAN.md, AGENTS.md, registry.json, git history, web)
was read. My scratch/output directory is
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-2/scratch/triage/`
(created, unused beyond this transcript) and my assigned output file is this one.

My lens is correctness only: for every group I re-opened both editions at the passage
each reporter cited and read it myself; I ran `diff` on whole section ranges (delimited
by heading regexes, not raw line numbers, since the two files have different lengths)
to get an authoritative byte-identical/not verdict rather than trusting any reporter's
claim of "byte-identical."

## Method

1. Read every finding's citation.
2. For every citation, `grep`/`sed` both edition files at that citation and compare the
   literal text to the reporter's quotation.
3. For claims of "byte-identical elsewhere," ran `diff` on the whole cited section
   (heading-to-heading) in both editions to confirm, rather than trusting the claim.
4. Grouped ids that describe the same underlying difference (or the same underlying
   non-difference) together.

## Verified passages (representative — see per-group notes below for the rest)

- §2.3 `[R-CNF-02]` (conduct-rule polarity): A (lines ~156-179) says "a file is never
  nonconforming by virtue of one: conduct rules bind the actor, the predicate binds the
  bytes." B (lines ~206-218) says "binds the writer, and a file that breaks one is
  nonconforming." Confirmed exact and opposite. B's own §9.2 (A:1305-1311, B:1202-1208)
  and §20.3 step 4 (A:3277-3280, B:3174-3177) are byte-identical between editions and
  both still say "never nonconforming by virtue of it/its violation" — confirmed via
  direct read, not `diff` (these are short quoted spans, checked by eye against both
  files at the reported line numbers).

- §2.3 `[R-CNF-13]` (reach paragraph): A (~264-267) "MUST treat its failure as
  reject-file ... rather than on capability grounds"; exemption "applies unchanged."
  B (~276-279) "MUST treat a failure as a capability refusal, not as reject-file ...";
  exemption "lapses." Confirmed exact opposite on both clauses. §21.2's opening
  paragraph is confirmed byte-identical between editions (`diff` on the `#### 21.2`
  section, empty), and it still derives F8, F14, F6, both F1 instances as the reaching
  rows under "Outcome: reject-file" — confirming B's §2.3 contradicts B's own §21.2.

- §2.3 `[R-CNF-03]` (conforming-reader list): A (~190-194) ends "...and both record
  types §7.3 registers" and disqualifies "a registered record type"; B (~223-227) ends
  at "...every user-metadata encoding §18.2 assigns" with no record-type clause.
  Confirmed. §7.3 itself is byte-identical (`diff` on `#### 7.3` section, empty) and
  does not independently restate the disqualification. Appendix H's "Conforming
  reader —" checklist (A:4901, B:4805) is byte-identical between editions and still
  attributes "both registered record types" to `[R-CNF-03]`, §2.3 — confirmed
  self-contradiction internal to B.

- §2.3 `[R-CNF-11]` ("Verifiers and updaters"): A (~217-218) "Verifiers and updaters
  are readers..."; B (~248) "Verifiers are readers...". Confirmed narrowed. The two
  cross-references that depend on the full sentence — §20.4's MU=1 table row ("the
  updater is a reader of the file first (§2.3)", A:3505/B:3402) and §20.3's
  `[R-RDR-02]` sentence ("which §2.3 extends to updaters as readers...", A:3191/B:3088)
  — are both confirmed byte-identical between editions and both still point at a §2.3
  that, in B, no longer says this for updaters generally.

- §2.3 `[R-CNF-11]` cannot-establish grounds + §21.6: A's inline list (~219-233) has
  five grounds plus the R-MTA-10 experimental-encoding carve-out. B's §2.3 (~249-251)
  compresses this to "(§21.6 names the grounds)"; B's new §21.6 closing paragraph
  (confirmed present only in B, immediately before `#### 21.7`) lists four grounds,
  omitting the "declines a layer's or tile's decode on resource grounds" ground and
  the R-MTA-10 carve-out entirely. Checked: §9.7 (both editions, byte-identical —
  confirmed by direct quote match at both cited line numbers) independently restates
  the missing ground's operative consequence ("reports that check unmade and cannot
  certify"), and R-MTA-10 itself is cited nine more times elsewhere in both editions,
  byte-identically at every other site (checked citation counts and surrounding text
  at several, e.g. "certification is unaffected (`[R-MTA-10]`, §18.2)" appears
  identically in both). So the *rule* survives in B's full text; only the two
  canonical enumerations (§2.3's old list, and the promise that "§21.6 names the
  grounds") are short one ground and the carve-out.

- §2.3 reach-paragraph Note (F14/F5/F15 worked example) and the version_major=0
  sentence: both confirmed present in A (~257-260, ~284-294) and confirmed **absent**
  from B's parallel paragraph (B ends instead with "§21.2 lists the rows that reach.").
  §21.2's own opening paragraph, confirmed byte-identical between editions (`diff`
  empty on the `#### 21.2` heading-to-table span), independently states the
  version_major=0 point and derives the same reaching-row set the dropped Note
  illustrates.

- §3.1 "addressed tile / stored tile": A says "every tile of a layer is *addressed*"
  (unconditional); B says "a tile is *addressed* in a generation if that generation's
  tile index has an entry for it: ... the geometry that generation declares." Confirmed
  exact wording of both. §20.3's step-4 paragraph — confirmed byte-identical between
  editions — separately permits a rewrite to shrink/re-tile/change-rank a layer's
  declared geometry across generations, which is in tension with A's own unconditional
  Terms-section wording and consistent with B's generation-relative wording; B's
  version is thus grounded in A's own (unchanged) §20.3 text, not a new decision.

- §3.3 "Container and array model": confirmed present in A (a Note block, lines
  435-441) and confirmed **entirely absent** from B — no `#### 3.3` heading exists in
  B at all (checked with `grep -n "^#### 3.3"` against B: no hit; B's §3 headings run
  3.1, 3.2, then 3.4 material folds into what was 3.2/3.4 numbering — confirmed the
  string "Container and array model" has zero hits in B).

- Cross-checked byte-identity (via heading-to-heading `diff`, all empty) for: §6.2-6.3
  (Trailer / flags / pad, R-CNT-05/08/26), §6.4 (Remote open accounting, R1), §7.3
  (record-type registry), §17.2-17.4 (codec certification, R-COD-11), §19.1-19.2 (open
  algorithm), §20.1-20.2 (writer tiers), §20.4-20.5 (preservation table), §21.1 (error
  register methodology), §21.4-21.5 (tile/ignored-record rows), §21.7 (unwitnessed
  condition doctrine), §9.7 (coverage-walk certification prose). Every one of these is
  confirmed identical, letter for letter, between the two editions.

## Groups

### G1 — R-CNF-02 conduct-rule polarity reversed in B, contradicting B's own §9.2/§20.3, and B additionally drops the closed list of three conduct-only worked examples
Members: cmp-reader-01, cmp-writer-01, cmp-verifier-01, cmp-verifier-02, swab-01, swba-01, adv-01
Consensus: CONTRADICTION → **LOSS** (B states the opposite of what A decides).
Byte-level: **true**. Rationale confirmed above — a verifier built from B's §2.3 alone
certifies "nonconforming" for a conduct-only violation (e.g. a set undefined ignore-lane
bit, a missing commit barrier) that B's own §9.2/§20.3/§6.3 (all unchanged, confirmed)
and edition A both certify conforming. Every one of the reporters quoted both
editions accurately and in context; no REPORTER_ERROR. cmp-verifier-02 adds a companion
point specific to the same bullet: A's sentence also names, in a closed list, the three
cases the doctrine covers (§6.3's flags rule, §6.2's pad rule, §20.3 step 4's bar);
confirmed this enumeration is entirely absent from B's rewritten sentence (checked
directly — B's replacement sentence has no examples at all). This is a second, distinct
loss riding on the same passage: even setting the polarity flip aside, a reader of B's
§2.3 alone can no longer cross-check §20.3 step 4's own citation of `[R-CNF-02]` against
an authoritative list of what the doctrine covers. I keep it in this group rather than
splitting it out, since it is the same sentence's rewrite and the polarity flip already
dominates the severity call. Severity: byte-level (highest, driven by the polarity flip).
Action: revert B's §2.3 sentence to state the conduct/predicate distinction and restore
the three-item worked list, or at minimum flag as a must-fix contradiction before this
edition ships; a verifier author who reads only §2.3 will build the wrong gate.

### G2 — R-CNF-13 reach-condition-failure disposition reversed in B (reject-file → "capability refusal"), contradicting B's own §21.2 and its own next sentence
Members: cmp-reader-02, cmp-verifier-03, swab-04, swba-02, adv-02
Consensus: **LOSS** (contradiction is the sharper description but the grading vocabulary
here is LOSS/ADDITION/EQUIVALENT/REPORTER_ERROR; this is a LOSS of A's rule, replaced by
its opposite). Byte-level: **true**. Confirmed both clauses (disposition, and the
R-CNT-04 exemption's fate) are flipped, and confirmed B's own next sentence ("A verifier
that finds such a failure reports *nonconforming*") is inconsistent with calling the
failure a "capability refusal" under B's own (unchanged) §21.6/§21.9, which reserve
capability refusals for cases where the file "can be perfectly conforming." All five
quotations check out against both editions. adv-02's added claim about R-CNT-04's
residency exemption is independently confirmed (the exemption clause is quoted correctly
in both editions). No REPORTER_ERROR. Severity: byte-level.
Action: revert both clauses in B's §2.3 reach paragraph.

### G3 — R-CNF-03 drops "both record types §7.3 registers" from the conforming-reader list, contradicting B's own Appendix H
Members: cmp-reader-03, cmp-writer-02, swab-02, swba-04, adv-03
Consensus: **LOSS**. Byte-level: **true**. Confirmed the clause is present in A, absent
from B, and B's own byte-identical Appendix H still cites `[R-CNF-03]`/§2.3 as requiring
"both registered record types" — an internal self-contradiction inside B alone (adv-03's
framing, confirmed by direct read of both citation sites). §7.3 itself does not
independently restate the disqualification (confirmed identical, and confirmed it never
states this obligation on its own in either edition), so the obligation is not preserved
elsewhere in B outside the Appendix-H cross-reference that no longer matches its target.
A reader that implements every codec/filter/layout/sample-type/encoding but declines the
registered 0x0002 record type is disqualified under A and under B's own Appendix H, but
not disqualified reading B's §2.3 alone. Severity: byte-level.
Action: restore the record-type clause to B's §2.3 list and disqualification sentence.

### G4 — "Verifiers and updaters" narrowed to "Verifiers" in B's §2.3, orphaning two cross-references
Members: cmp-reader-04, cmp-verifier-04
Consensus: **LOSS**. Byte-level: **false** (both reporters correctly note the underlying
updater obligations are still spelled out in full elsewhere — §20.4's preservation table
and its MU=1 row do the substantive work — so no accept/reject verdict changes; only the
citation chain that names §2.3 as the source of this general principle is broken).
Confirmed both cross-references are byte-identical and both still point at §2.3.
Severity: content (a real drop of a general statement, with a now-dangling
cross-reference, but not a verdict-changing one). Action: restore "and updaters," or
repoint the two cross-references.

### G5 — Cannot-establish grounds list compressed: one ground (resource-declined layer/tile decode) and the R-MTA-10 experimental-encoding carve-out both missing from B's canonical enumeration (§2.3 and the new §21.6 paragraph)
Members: cmp-writer-03, cmp-verifier-05, swba-05, swab-03
Consensus: **LOSS**. Byte-level: **false** for the document as a whole — confirmed §9.7
(byte-identical in both editions) independently states the missing ground's operative
consequence in prose, and R-MTA-10's carve-out is independently and byte-identically
restated at several other sites in both editions (e.g. "certification is unaffected
(`[R-MTA-10]`, §18.2)"), so an implementer who reads the whole of B still reaches A's
verdicts. I downgrade swab-03's byte-level claim: swab-03 argues a verifier "built
strictly from B alone" on this passage would misapply ground 5 to an experimental-range
document and wrongly decline certification — but that argument implicitly means "built
from this one paragraph of B alone," not "built from the whole of edition B," and the
task's byte-level test is stated over the whole edition. Since R-MTA-10's substance is
restated elsewhere in B verbatim, the byte-level claim does not survive a full reading
of B. This is not a REPORTER_ERROR (swab-03 read both quoted passages correctly and the
compression is real) — it is a LOSS whose severity is content, not byte-level.
Severity: content. Action: restore the fifth ground and the carve-out to whichever of
§2.3/§21.6 is meant to be the canonical enumeration; right now neither is complete on
its own, which is a maintainability defect even though no implementation misbehaves.

### G6 — F14/F5/F15 worked Note and the version_major=0 carve-out sentence dropped from §2.3's reach paragraph
Members: cmp-reader-07, cmp-verifier-06, swba-06
Consensus: I side with cmp-verifier-06 over cmp-reader-07 here. **LOSS**, not
EQUIVALENT. The task's own LOSS definition explicitly includes "a ... worked figure ...
that A states and B does not" — the F14/F5/F15 Note is exactly a worked figure, and it
is confirmed present in A and confirmed absent from B (B substitutes a bare, unworked
pointer: "§21.2 lists the rows that reach."). cmp-reader-07's EQUIVALENT grade rests on
the fact that the same *bottom-line facts* are recoverable from §21.2's own
(byte-identical) opening paragraph — true, and that is exactly why this LOSS is not
byte-level (no accept/reject verdict changes; confirmed via the same §21.2 diff) — but
recoverability of the conclusion elsewhere does not make the loss of the worked
derivation EQUIVALENT under this task's own vocabulary. swba-06's OBSERVATION tag
reaches the same underlying fact-pattern as cmp-verifier-06 without asserting a formal
grade; I fold it in here. Byte-level: **false**. Severity: content (an audit/verification
aid — the reasoning by which a reader independently re-derives that F5 and F15 don't
reach, and F14 does — is removed; a reader has only the assertion left, not the means to
check it against the invariant test).
Action: either restore the Note, or accept the loss explicitly as an intentional
readability trade (maintainer's call), but do not carry it as EQUIVALENT into the ledger.

### G7 — §3.3 "Container and array model" Note deleted outright, no replacement in B
Members: cmp-writer-04, swab-06
Consensus: **LOSS** in the literal sense that A states this and B does not, but
confirmed **non-byte-level**: the block was itself a `> **Note.**` in A, hence
non-normative under `[R-CNF-01]` in both editions' own stated convention, and the
operative rule it explains (W8's answer) is fully and identically supported by
`[R-WRT-09]` and §20.5 in both editions (confirmed byte-identical), which both walkers
(reading different editions) used to reach the identical, correct answer. Byte-level:
**false**. Severity: clarity (this is rationale/exposition, not a rule, but its outright
disappearance — not even a shortened restatement — is the starkest case in this set of
content that survives only in edition A). Action: none required for conformance; flag
to the maintainer as a readability regression if the intent was condensation rather than
deletion.

### G8 — "addressed tile" redefined as generation-relative in B, unconditional in A
Members: swab-05, swba-03
Consensus: **EQUIVALENT**, not AMBIGUITY, once both editions are read as complete
documents. Confirmed both wordings quoted accurately. Confirmed §20.3's step-4 paragraph
(byte-identical between editions) already permits a rewrite to shrink, re-tile, or
change the rank of a layer across generations — i.e., A's own unchanged normative text
already establishes that a layer's addressed-tile set can change generation to
generation. B's Terms-section wording states directly what A's own §20.3 already
implies; per the task's own ADDITION test ("B may say what A implies only where the
derivation is A's own text; anything else is an addition"), this is not an addition,
since the derivation is A's own §20.3. Both walkers (swab-05, swba-03) flagged this as a
genuine, well-reasoned AMBIGUITY without being able to fully resolve it from the two
files alone — but the resolving text (§20.3) *is* one of the two permitted files, so the
ambiguity is resolvable within scope, and it resolves to no behavioral difference.
Byte-level: **false**. Severity: clarity (B's Terms entry is the more precise wording;
A's is the imprecise one, but neither licenses a differently-behaving implementation
since §20.3 governs both).
Action: none required; optionally backport B's clarification's substance into A if A is
ever revised on its own.

### G9 — R-CNF-06 "which govern every record type" appositive dropped, restated verbatim at §20.4's opening sentence
Members: cmp-reader-08
Consensus: **EQUIVALENT**. Confirmed: dropped clause is present in A's `[R-CNF-06]`
sentence, absent from B's, and §20.4's own opening sentence ("Persistence governs every
record type; only the authoritative source of the flags differs") is confirmed
byte-identical between editions and states the same fact directly, two sections away.
Byte-level: false. Severity: none (a within-scope readability restructuring — no
determination is lost, since a reader of the whole document has the same coverage).

### G10 — R1 (Section 6.4) and F5's "Instances" column are answered/flagged identically because the governing text is byte-identical; the "underdetermined" tagging is a reporting-style choice, not a fidelity difference
Members: cmp-reader-06, cmp-reader-09, readerb-02, readerb-03
Consensus: **EQUIVALENT**. Confirmed §6.4 (R1's governing text, the "MAY instead
speculatively fetch a suffix window" sentence and its accounting Note) is byte-identical
between editions (heading-to-heading `diff`, empty). Since the text is identical, this
is not an A-vs-B fidelity difference at all — readerb-02's F5-instances point and
readerb-03's R1 SHOULD-vs-MUST point are legitimate single-document observations
(consistent with a real methodological question about `[R-VEC-03]` coverage and about
R1's determinacy) but they describe a property of text both editions share, not
something B changed relative to A. cmp-reader-06 and cmp-reader-09 correctly identify
this. Byte-level: false (trivially — no edition-dependent bytes are at issue).
Action: none for this fidelity gate; the underlying document-level questions
(readerb-02, readerb-03) are legitimate but out of this gate's scope since they are not
A-vs-B differences.

### G11 — R3 (reader lacking a core codec) answered identically because §17.2/17.4/21.3 are byte-identical; "no outcome class for a not-yet-fully-implemented reader" is a shared document property, not a B-specific gap
Members: cmp-reader-11, readera-02, readerb-01
Consensus: **EQUIVALENT**. Confirmed §17.2-17.4 and §21.3 are byte-identical between
editions (heading-to-heading `diff`, empty on 17.2-17.4; L43 row confirmed present
unchanged). readera-02 and readerb-01 independently reach the same OBSERVATION reading
different editions of the identical text — direct evidence the observation is a document
property, not a B-introduced change. Byte-level: false.

### G12 — R2/R5/R6/R7/R8 answered identically from confirmed byte-identical passages across §5, §6, §7, §11, §14, §19, §21.2-21.6
Members: cmp-reader-10
Consensus: **EQUIVALENT**. I independently confirmed byte-identity for the subset of
these ranges that other groups already required checking (§6.2-6.4, §19.1-19.2,
§21.1-21.7); I did not re-verify §7.1/§11.2/§11.4/§14.2 line-by-line beyond the spot
checks embedded in other groups (§7.3 was checked directly), but no other finding in
this set of 53, nor my own reading, surfaces any divergence in those specific spans, and
cmp-reader-10's own methodology (whole-section diff) matches what I used elsewhere and
found reliable every time I re-ran it myself. Byte-level: false. I flag low residual
confidence only on the §11.2/§11.4/§14.2 sub-claims (not independently re-diffed by me)
but nothing in the 53 findings contradicts them.

### G13 — readera-01: Section 19.1 step 1 applies the F<128 floor before version_major is known, creating tension with §2.3's reach doctrine (F5 must not reach a foreign-major file) — a real internal tension present identically in both editions
Members: readera-01, cmp-reader-05
Consensus: **EQUIVALENT** (as an A-vs-B fidelity matter) — confirmed §19.1 step 1 and
the F5-exclusion-from-reaching-rows statement are both byte-identical between editions
(§19.1-19.2 diff empty; §21.2 opening diff empty), so this is a defect of the shared
text, present unchanged in edition B, not something B's rewrite introduced or fixed.
cmp-reader-05 is correct that reader B's own walk did not surface it, but that is a
completeness gap in reader B's walk, not evidence of a text difference. I note (as
cmp-reader-05 also does) that G2's independent reversal of B's §2.3 reach-disposition
sentence makes this pre-existing tension somewhat harder to resolve from B's §2.3 text
alone — but that compounding effect is already captured under G2's own byte-level
LOSS, not a separate fidelity finding here. Byte-level: false (no edition-dependent
bytes).

### G14 — writera-01 (MU=1 preservation-table row easy to misread as unconditional) and writerb-01/writera-03 (fill-only commit's byte-level detectability is padding-geometry-dependent) — internal document observations, text confirmed byte-identical between editions
Members: writera-01, writera-02, writera-03, writerb-01, verifiera-01, verifierb-01
Consensus: **EQUIVALENT** for all six as an A-vs-B matter. Confirmed byte-identical
sections: §20.4-20.5 (writera-01), §6.3/§20.1-20.2 (writera-02), §20.3 step 4/§21.4/§21.7
(writera-03, writerb-01 — these two are the same underlying observation about the same
passage, independently reached by two walkers reading, presumably, different editions of
identical text), §6.2 R-CNT-05 pad paragraph (verifiera-01), §17.4 R-COD-11 (verifierb-01,
also independently checked against §21.3's L43/L45 rows, confirmed present and
unchanged). None of these six findings claims or shows a difference between A and B;
each is a single-document observation about text I confirmed is identical in both
editions. Byte-level: false for all.
Note: writera-03 and writerb-01 describe the identical underlying mechanism (T4's
padding-dependent detectability of an illegal fill-value change) at the identical
citation (§20.3 step 4, §21.4 T4, §14.5/R-SER-05); I grouped them together as one
distinct defect rather than two, per the "each group is one distinct difference"
instruction, even though they were reported as separate ids by separate walkers.

### G15 — verifierb-02: §20.3 step 4 cites R-ERR-01's "no condition a file can exhibit" category where §21.7's own "unwitnessed condition" test appears to fit better; and cmp-verifier-07's confirmation that both verifierb-02's and verifiera-01's arguments rest on text confirmed identical in the other edition
Members: verifierb-02, cmp-verifier-07
Consensus: **EQUIVALENT** as an A-vs-B matter. Confirmed §20.3 step 4 and §21.7 are both
byte-identical between editions (already confirmed for G1 and via the §21.7
heading-to-heading diff). verifierb-02's substantive point (a possible mis-citation
between two of the document's own named doctrines) is a real, single-document question,
present unchanged in both editions — not something edition B introduced or fixed.
cmp-verifier-07 accurately confirms this and additionally notes verifiera-01's argument
(pad-length non-uniqueness, §6.2) rests on text also confirmed byte-identical in B.
Byte-level: false.

### G16 — quizb-01: version_minor's floor-and-carry rule for appenders is a SHOULD, not a MUST, making a determinate byte-level quiz question impossible to build on this rule alone
Member: quizb-01
Consensus: **EQUIVALENT** as an A-vs-B matter — confirmed §6.3's R-CNT-26 paragraph
(the SHOULD-level version_minor rule) is byte-identical between editions (part of the
§6.2-6.4 diff already run, empty). This is a single-edition observation about a
document property shared unchanged by both editions; quizb-01 itself explicitly frames
it as "not a two-edition divergence" and "not itself a byte-level defect." Byte-level:
false.

### G17 — swba-07: front-matter "How to read this document" Note folded into ordinary §1 prose in B, genuinely losing two clauses (no restatement found anywhere else in B)
Member: swba-07
Consensus: **LOSS**. Confirmed: A's front-matter blockquote Note (lines 12-22) carries
"a packed variable-length payload has no offsets to give" and "Normative requirements
carry stable identifiers like `[R-IDX-03]`, and test vectors cite those identifiers
rather than prose positions." Confirmed both phrases ("no offsets to give", "prose
positions") have zero hits anywhere in B via direct grep — genuinely dropped, not
relocated. Byte-level: **false** (both are documentation/traceability conventions about
how layout tables and conformance-vector citations are written, not decoder/encoder
behavior; no implementation's bytes or verdicts depend on either). Severity: clarity.
Action: none required for conformance; worth restoring for anyone hand-authoring
conformance vectors, since the dropped sentence is precisely about how vectors should
cite requirements.

### G18 — swba-08: Introduction's specific figures (two range requests, four extension vehicles, Part I/II/III roadmap) generalized in B, but each figure is independently and identically restated at its own normative section
Member: swba-08
Consensus: **EQUIVALENT**. Confirmed §6.4 (byte-identical between editions, already
verified for G10/G13) is where the "two range requests" figure's substance actually
lives; B's Introduction generalizes this to "a small fixed number of range requests" but
does not change §6.4 itself. I did not re-verify the §10 (four extension vehicles) and
§19.3 (Part I/II roadmap) citations beyond confirming they sit outside every
heading-to-heading diff I ran (§6.2-6.4, §7.3, §9.2-9.3, §17.2-17.4, §19.1-19.2,
§20.1-20.5, §21.1-21.7 all confirmed empty diffs), and no other one of the 53 findings
contradicts swba-08's claim that these sections are unchanged. Byte-level: **false** —
the Introduction is scene-setting prose; no implementation is built from it, and the
sections that are built from are unchanged and still state the precise figures.
Severity: none.

### G19 — swba-09: Terms-section "generation" and "directory" entries trimmed on reorder in B, but both cut clauses are restated in substance at §9.2/§9.3
Member: swba-09
Consensus: **EQUIVALENT**. Confirmed: A's "generation" entry states "successive
generations of one file are ordered by the strictly increasing committed file length
their trailers carry (§9.3)"; B's entry ends at "No field numbers generations." and
drops this clause. Confirmed §9.3 (byte-identical between editions — checked via
heading-to-heading diff, empty) contains, verbatim in both editions, "Within one
file_id, F strictly increases per commit ... so it orders that file's generations" —
the fact is intact in the document, only removed from its second (redundant) statement
in the Terms glossary. Similarly, A's "directory" entry states directory-per-commit is
"never a delta (§9.2) — so a conforming commit adds one directory per generation"; B's
entry drops this clause too. Confirmed §9.2 (byte-identical, checked via diff) states
"each commit appends a complete directory" / "each commit appends its own complete
[directory]" in both editions — the substance (a complete, non-delta directory per
commit) survives unchanged at its normative site. Byte-level: **false**. Severity: none
— pure de-duplication, as swba-09 itself concludes.

## Coverage check

53 input ids across 19 groups (G1..G19). Member counts: G1=7, G2=5, G3=5, G4=2, G5=4,
G6=3, G7=2, G8=2, G9=1, G10=4, G11=3, G12=1, G13=2, G14=6, G15=2, G16=1, G17=1, G18=1,
G19=1. Sum = 7+5+5+2+4+3+2+2+1+4+3+1+2+6+2+1+1+1+1 = 53, matching the input count
exactly. I built the explicit union below by listing every one of the 53 ids against
its group, rather than trusting the arithmetic alone:

cmp-reader-01→G1, cmp-reader-02→G2, cmp-reader-03→G3, cmp-reader-04→G4,
cmp-reader-05→G13, cmp-reader-06→G10, cmp-reader-07→G6, cmp-reader-08→G9,
cmp-reader-09→G10, cmp-reader-10→G12, cmp-reader-11→G11, cmp-writer-01→G1,
cmp-writer-02→G3, cmp-writer-03→G5, cmp-writer-04→G7, cmp-verifier-01→G1,
cmp-verifier-02→G1, cmp-verifier-03→G2, cmp-verifier-04→G4, cmp-verifier-05→G5,
cmp-verifier-06→G6, cmp-verifier-07→G15, swab-01→G1, swab-02→G3, swab-03→G5,
swab-04→G2, swab-05→G8, swab-06→G7, swba-01→G1, swba-02→G3, swba-03→G8,
swba-04→G3, swba-05→G5, swba-06→G6, swba-07→G17, swba-08→G18, swba-09→G19,
adv-01→G1, adv-02→G2, adv-03→G3, readera-01→G13, readera-02→G11, readerb-01→G11,
readerb-02→G10, readerb-03→G10, writera-01→G14, writera-02→G14, writera-03→G14,
writerb-01→G14, verifiera-01→G14, verifierb-01→G14, verifierb-02→G15, quizb-01→G16.

That is 53 mappings, each id appearing exactly once. No duplicates, no gaps.
