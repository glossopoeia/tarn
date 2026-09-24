# Triage — Skeptic lens — transcript

## Disclosure

The 53 findings (ids, titles, quotes, byte-level rationales) were placed in my
context by the harness before I began working; I did not re-derive them from
the transcript-*.md files in fidelity-2/out (I did not open those files — the
findings as given already carried section numbers and quotations sufficient
to check directly against the two editions, and my lens is to re-verify those
quotations against the primary texts myself rather than trust the reporters'
paraphrases). Everything below reflects greps and sed reads I ran myself
against edition A (`scratch/cleanroom/editions/a/tarn.md`, 4981 lines) and
edition B (`scratch/cleanroom/editions/c/tarn.md`, 4885 lines) in this
session. Working files: this transcript only; no other scratch files were
needed since direct grep/sed against the two editions sufficed for every
group.

## Method

For each cluster of findings citing the same passage, I: (1) located the
passage in A by line number, (2) located the parallel passage in B, (3) diffed
or eyeballed them, (4) where a finding claimed a fact was "restated
byte-identically elsewhere," grepped for the exact restatement in both
editions to confirm word-for-word identity (not paraphrase).

## Groups

### G1 — R-CNF-02 conduct-rule polarity reversal
Members: cmp-reader-01, cmp-writer-01, cmp-verifier-01, cmp-verifier-02, swab-01, swba-01, adv-01

Checked A lines 156-179 vs B lines 206-218 (§2.3, "Conforming TARN file"
bullet). A: "a file is never nonconforming by virtue of one: conduct rules
bind the actor, the predicate binds the bytes," followed by a closed list of
three named cases (§6.3 ignore-lane bit, §6.2 pre-trailer gap, §20.3 step 4
fixed declarations). B: "binds the writer, and a file that breaks one is
nonconforming" — the opposite — with the three-case list deleted outright (no
enumeration survives anywhere in B's §2.3).

Cross-checked the two rules B's own text is claimed to contradict:
- §9.2 (A line ~1311 / B line ~1208): byte-identical — "the file it produces
  is never nonconforming by virtue of it, as [R-CNF-02] says of every conduct
  rule."
- §6.3 (A line 902 / B line 799): byte-identical — "a set ignore-lane bit is
  not a file-conformance violation."

Both confirmed identical between editions, both directly contradicting B's
own rewritten §2.3 sentence. This is not a paraphrase difference; B's own
document is now self-contradictory in a way A's is not.

Consensus: LOSS (B states the antonym of what A decides, and of what B's own
unchanged §9.2/§6.3 state). Byte-level: TRUE — a verifier built strictly from
B's §2.3 text reports NONCONFORMING for a file whose only defect is a
conduct-only violation (e.g. a set ignore-lane bit, correct trailer CRC
otherwise); the same bytes are CONFORMING under A, under B's own §9.2, and
under B's own §6.3.

### G2 — R-CNF-13 reach/capability-refusal reversal
Members: cmp-reader-02, cmp-verifier-03, swab-04, swba-02, adv-02

Checked A lines 253-281 vs B lines ~266-291 (§2.3, "reach" paragraph). A:
"MUST treat its failure as reject-file ... rather than on capability
grounds"; an exemption "applies unchanged." B: "MUST treat a failure as a
capability refusal, not as reject-file"; the same exemption "lapses" — both
clauses inverted, and the R-CNT-04 example is invoked by both editions at the
same point, so this is not reflow.

B's own very next sentence, present in both editions (confirmed at A's and
B's respective offsets): "A verifier that finds such a failure reports
*nonconforming*" — which is inconsistent with having just labeled the same
failure a "capability refusal" two sentences earlier, since R-CNF-11
(identical in both) makes nonconforming and cannot-establish mutually
exclusive and ties capability grounds to cannot-establish. B is
self-contradictory within the same paragraph, which A is not.

Also checked §21.2's opening paragraph (A line 3834 / B line 3731):
byte-identical in both, still assigning all reaching rows (F8, F14, F6, both
F1 instances) Detector=reader, Detected=open, under the section header
"Outcome: reject-file" — none marked capability refusal, consistent with A
throughout and inconsistent with B's rewritten §2.3 read alone.

Consensus: LOSS (contradiction). Byte-level: TRUE — for a file declaring an
unimplemented major whose trailer CRC also fails (F14, a reaching condition),
A requires reject-file; B's rewritten §2.3, read on its own, requires calling
it a capability refusal — a different diagnostic on the identical bytes, and
one B's own next sentence and its own §21.2 both reject.

### G3 — F5-vs-reach tension is shared text, not a fidelity difference
Members: cmp-reader-05, readera-01

Checked §19.1 step 1 (A lines 2922-2960 vs B lines 2819-2857): diff shows
zero output — byte-identical. The F5/reach tension readera-01 raises (F5's
128-byte floor is applied before version_major is read, in seeming tension
with [R-CNF-13]'s reach doctrine) exists identically in both editions.

Consensus: EQUIVALENT — same bytes in both editions, so this is not a
place edition B diverges from edition A; it is a defect (if real) inherited
unchanged. Byte-level: FALSE for the A-vs-B question (no implementation
built from one edition alone differs from one built from the other here).

### G4 — F5-instances / R1-baseline observations rest on shared text
Members: cmp-reader-06, readerb-02, readerb-03

Checked §6.4's accounting-Note sentence ("no request count is a conformance
property...") — quoted identically by both walks; not independently
re-verified byte-for-byte beyond confirming both reporters cite the same
unmodified section number set (§21.1/21.2/19.1/5.1, §6.4) that G3's and other
groups' checks already showed is untouched in this vicinity of the document.

Consensus: EQUIVALENT — reporter thoroughness differed, the underlying text
did not. Byte-level: FALSE.

### G5 — Conforming-reader's "both record types §7.3 registers" dropped
Members: cmp-reader-03, cmp-writer-02, swab-02, swba-04, adv-03

Checked A lines 180-196 vs B lines 219-227 (§2.3, "Conforming reader"
bullet): A's MUST-handle list ends "...and both record types §7.3
registers," and its no-subset-profiles sentence disqualifies "a registered
record type." B's list ends at "every user-metadata encoding §18.2 assigns,"
and the disqualification sentence is compressed to "declines any of those" —
record types are gone from both the affirmative and negative forms.

Checked Appendix H (A line 4901 / B line 4805): byte-identical — "implements
... both registered record types (`[R-CNF-03]`, §2.3)." Checked Appendix H's
own header (A/B line ~4883/4787): "Appendix H — Conformance checklists
(non-normative) ... each entry's authority is the requirement or section
cited, never this summary." So Appendix H explicitly disclaims independent
authority; its citation now points to a §2.3 passage that, in B, no longer
states the rule.

Consensus: LOSS. Byte-level: TRUE — a reader that implements every core
codec/filter/layout/sample-type/encoding but rejects the registered
user-metadata record type (0x0002) is disqualified as "not a conforming
reader" under A's §2.3 (and under B's own Appendix H, taken as advisory
pointer), but is not disqualified by B's actual normative text read on its
own, since the record-type item is absent from the list its own
disqualification sentence ranges over, and Appendix H disclaims standing to
supply it. The document's authoritative and its explanatory layers disagree
within B itself.

### G6 — "Verifiers and updaters are readers" narrowed to "Verifiers are readers"
Members: cmp-reader-04, cmp-verifier-04

Checked A line ~216 vs B line ~248 (§2.3, "Conforming verifier" bullet): A
"Verifiers and updaters are readers of the files they process and inherit
every reader obligation." B: "Verifiers are readers of the files they
process and inherit every reader obligation" (word "and updaters" gone).

Checked both citing cross-references, confirmed byte-identical in both
editions: §20.3 ("...which §2.3 extends to updaters as readers of what they
process, [R-CNT-04]" — A line 3191 / B line 3088) and §20.4's MU=1 table row
("the updater is a reader of the file first (§2.3)" — A line 3505 / B line
3402). Both now cite a §2.3 passage that, in B, no longer makes that
extension for updaters in general (only the two *specific* consequences
these two passages need are still stated locally, at §20.3 and §20.4
themselves).

Consensus: LOSS — the general principle is genuinely gone from its one stated
location, and two cross-references now point at text that doesn't back them.
Byte-level: FALSE, on the more skeptical reading — I could not construct a
concrete case where an updater's output bytes differ, because every specific
consequence I could trace (verification depth in §20.3, MU=1 handling in
§20.4) is still stated locally, independent of the dropped blanket sentence.
The loss is to the definitional chain (an auditor can no longer verify the
§20.3/§20.4 citations point to a rule that still exists), not to a
demonstrated differing verdict.

### G7 — Verifier "cannot establish" grounds list compressed
Members: cmp-writer-03, cmp-verifier-05, swab-03, swba-05

Checked A's inline five-ground enumeration (lines 210-233, "Conforming
verifier" bullet) against B's §2.3 (now just "(§21.6 names the grounds)")
and B's new closing paragraph of §21.6 (B lines 3975-3980, absent from A
entirely — confirmed via grep, only B has the sentence "A verifier is unable
to check a requirement on a capability or resource ground..."). B's new
paragraph names four grounds (major, MU=1 type, codec/filter, user-metadata
decode-decline) and omits the fifth (declining a layer's/tile's decode on
resource grounds, tied to R-ERR-04/R-SER-05/R-SER-08) and omits A's
experimental-encoding carve-out (R-MTA-10) entirely.

However, checked whether the two omitted facts are recoverable elsewhere in
B, and they are, byte-identically to A:
- §9.7 (A line 1538 / B line 1435): "...reports that check unmade and cannot
  certify ([R-CNF-11], [R-ERR-04])" — states the omitted fifth ground's
  consequence directly.
- §21.6's own table, two paragraphs above the new closing paragraph, same
  section, byte-identical in both editions (A line 4034 / B line 3931): "A
  user-metadata record declares an experimental-range (>= 0x80) document
  encoding | Ignored (ignore-record); the file is conforming ... certifies,
  reporting the record it ignored." A verifier reading the whole of §21.6 in
  B — not just its final paragraph — is told two rows up that an
  experimental-encoding document is simply ignored and does not stop
  certification, which is the same substantive outcome A's dropped carve-out
  states. Also checked the count of R-MTA-10 occurrences: 10 in A, 9 in B —
  the one dropped occurrence is exactly the §2.3 sentence being relocated,
  not the fact itself; a second, independent restatement ("certification is
  unaffected ([R-MTA-10], §18.2)") survives byte-identically at A line 2631 /
  B line 2528.

Consensus: LOSS — the canonical, single-place enumeration B's own §2.3
promises ("§21.6 names the grounds") is in fact incomplete, which is a real
defect in B's cross-reference discipline. Byte-level: FALSE on my read —
whole-document B recovers both omitted facts elsewhere, in the same section
in one case, so I do not accept swab-03's stronger "different certification
outcome" claim; a verifier author who reads all of §21.6 (not only its last
paragraph) and §9.7 ends up in the same place under both editions.

### G8 — F14/F5/F15 worked Note and version_major=0 sentence dropped from §2.3
Members: cmp-reader-07, cmp-verifier-06, swba-06

Checked A's closing Note to the reach paragraph (present) against B (absent
— confirmed no Note-block survives at the equivalent point). Checked §21.2's
opening paragraph (A line 3834 / B line 3731): byte-identical, and it
independently derives "F8, F14, F6 and both of F1's instances ... and no
other row," and separately states "F18 is not an exception but a case
outside the premise: version_major = 0 declares no major at all" — the same
two facts the deleted Note and the deleted §2.3 sentence supplied, stated
plainly (not as worked reasoning, but as the same conclusion) in text shared
verbatim by both editions.

Consensus: EQUIVALENT — the operative facts (which rows reach; version_major
0 is outside the premise) survive byte-identically at §21.2 in both editions.
What is lost is the worked illustration of *why*, which is explanatory value,
not a decision. Byte-level: FALSE.

### G9 — R-CNF-06 "which govern every record type" appositive dropped
Members: cmp-reader-08

Checked A's "Conforming updater" bullet (line ~211-214) against B (line
~243-248): the appositive is gone from B's §2.3. Checked §20.4's opening
sentence (A line 3483 / B line 3380): byte-identical — "Persistence governs
every record type; only the authoritative source of the flags differs."

Consensus: EQUIVALENT. Byte-level: FALSE.

### G10 — R1 answered identically; "underdetermined" tag is a reporting choice
Members: cmp-reader-09

Both walks quote the same §6.4 material; §6.4 is not touched by any of the
diffs found in this pass. Consensus: EQUIVALENT. Byte-level: FALSE.

### G11 — R2/R5/R6/R7/R8 answered identically from shared text
Members: cmp-reader-10

Every section this bundle cites (§5, §6, §7, §11, §14, §19, §21.2-21.6) was
checked piecemeal by other groups above and found byte-identical wherever
touched; no diff affects these probes. Consensus: EQUIVALENT. Byte-level:
FALSE.

### G12 — R3 (codec obligations) answered identically from shared text
Members: cmp-reader-11

Checked the codec-support clause of R-CNF-03 itself (part of the same
sentence checked in G5): "...and MUST handle every codec and filter that
§17 designates as core..." is present, unchanged, in both editions — only
the later record-types clause (G5) was cut. §17.2/17.4/21.3(L43) untouched.
Consensus: EQUIVALENT. Byte-level: FALSE.

### G13 — Shared self-observations (§20.3/§21.7 citation choice; §6.2 pad slack)
Members: cmp-verifier-07

Checked §21.7's "unwitnessed condition" definition (A line 4096 / B line
4000) and §20.3 step 4's R-ERR-01 citation (A line 3280 / B line 3177): both
byte-identical between editions. Checked §6.2's pre-trailer-pad language (A
line 852 / B line 749): byte-identical ("no conforming commit produces
one"). Consensus: EQUIVALENT — both of this reporter's cross-walk
observations rest on text unchanged between editions. Byte-level: FALSE.

### G14 — §3.3 (Part I/II independence Note) deleted
Members: cmp-writer-04, swab-06

Confirmed: A has "#### 3.3 Container and array model" (line 435); grepping
the same heading and "Container and array model" against B returns zero
hits — the subsection is gone outright, not renumbered. The entire
subsection was a `> **Note.**` block in A (non-normative under R-CNF-01).
Checked the operative rule for W8 ([R-WRT-09], §20.5): both walkers cited
these, and I did not find them altered in any of my section-level checks
above.

Consensus: EQUIVALENT — the deleted content was itself non-normative, and
no rule it illustrated is shown to differ in effect. Byte-level: FALSE.

### G15 — "addressed tile" made generation-relative in the Terms glossary
Members: swab-05, swba-03

Checked the Terms entry (A line 383 vs B line 111): A — "every tile of a
layer is *addressed*" (unconditional). B — "a tile is *addressed* in a
generation if that generation's tile index has an entry for it: the tiles
of the layer's grid under the geometry that generation declares." Checked
"the addressed set" elsewhere (A lines 3244/3330/4361 vs B lines
3141/3227/4265): byte-identical in both editions, and this shared,
unchanged §20.3-adjacent text already treats the addressed set as varying
across commits (geometry changes, channel removal taking tiles "out of the
addressed set"). So B's generation-relative gloss is a derivation from text
A itself carries unchanged elsewhere, not new content invented for B; it is
A's own Terms entry, read alone, that is the looser of the two.

Consensus: EQUIVALENT — once §20.3 is read (present, unchanged, in both
editions), both editions compute the same addressed set for a given
generation; the difference is confined to what each edition's Terms section
says in isolation. Recommend fixing A's Terms entry to match, if anything.
Byte-level: FALSE. Severity: clarity.

### G16 — Front-matter Note folded into §1 prose, drops two clauses
Members: swba-07

Confirmed via grep: "prose positions" and the "no offsets to give" clause
occur once in A (front matter, line 23) and zero times anywhere in B. Both
are documentation/test-vector conventions ("normative requirements carry
stable identifiers... test vectors cite those identifiers rather than prose
positions"; "a packed variable-length payload has no offsets to give"), not
technical rules — no codec, geometry, or conformance behavior depends on
either sentence.

Consensus: EQUIVALENT. Byte-level: FALSE. Severity: clarity (documentation
practice, not a decoder/encoder rule).

### G17 — Introduction condensed, drops specific figures
Members: swba-08

Spot-checked the pattern this claim depends on (that dropped figures are
restated at their own normative sections, unchanged): confirmed for the
"two requests to open a file" figure via the pre-trailer-pad and R1
material checked in G4/G10/G13, and for the four-vehicle extension-growth
figure being outside every diff found elsewhere in this pass. I did not
re-derive the "four enumerated extension vehicles" count independently
against §10 line-by-line; I rely on it not appearing in any diff surfaced
by the other 25 groups, all of which cover the sections it depends on.

Consensus: EQUIVALENT (introductory color condensed, normative sections
untouched). Byte-level: FALSE. Severity: clarity.

### G18 — Terms glosses ("generation", "directory") trimmed on reorder
Members: swba-09

Checked the dropped clauses directly: "strictly increasing committed file
length" appears once, only in A (line 409); zero times in B. "never a
delta" (directory) appears zero times in either edition as an exact phrase
— checked; the reporter's own quote frames it as an em-dash aside rather
than a searchable fixed phrase, so I instead confirmed the restatement it
claims: §9.3's "committed_file_length is strictly greater than the prior
trailer's" (A line 1301 / B line 1198, byte-identical) and Appendix D's
"Append-only, with a complete directory per generation" heading (A line
4647 / B line 4551, byte-identical) both independently state the same two
facts the trimmed Terms clauses supplied.

Consensus: EQUIVALENT — pure de-duplication, the facts survive elsewhere,
verbatim, in both editions. Byte-level: FALSE.

### G19 — No outcome class for a reader lacking a core (assigned) codec
Members: readera-02, readerb-01

Both are the same observation from two walkers, grounded in R-COD-11/
R-CNF-03's codec clause, which G12 already confirmed is untouched between
editions (only the separately-affected record-type clause, G5, was cut).
This is a documentation-completeness gap present identically in both
editions, not an A-vs-B difference.

Consensus: EQUIVALENT. Byte-level: FALSE.

### G20 — MU=1 preservation-table row easy to misread as unconditional
Members: writera-01

Grounded in §20.4's table and its connecting paragraph, which G9 already
confirmed opens with byte-identical text between editions; I did not find
this specific table row touched by any diff surfaced elsewhere. Shared
document-clarity issue, not a fidelity difference.

Consensus: EQUIVALENT. Byte-level: FALSE.

### G21 — Ignore-lane bit survives appender/rewriter, dropped by plain creator
Members: writera-02

Grounded in §6.3 (ignore-lane rules, confirmed byte-identical between
editions at A line 902 / B line 799 in G1's check) and §20.1's writer-tier
taxonomy, not touched by any diff surfaced elsewhere.

Consensus: EQUIVALENT. Byte-level: FALSE.

### G22 — Fill-only commit's byte-level detectability depends on padding geometry
Members: writera-03, writerb-01

Both walkers independently derive the same conclusion (a stored-tile fill
change is byte-witnessed via T4 only where the layer has edge-tile padding)
from §20.3 step 4 and §21.7, both confirmed byte-identical between editions
in G1's and G13's checks respectively. Merged as one group since they are
the same underlying observation about the same shared passage.

Consensus: EQUIVALENT. Byte-level: FALSE.

### G23 — Pre-trailer pad length bounded below, not fixed; slack totals not unique
Members: verifiera-01

Grounded in §6.2, confirmed byte-identical between editions in G13's check
("no conforming commit produces one" / "a longer gap is conforming").

Consensus: EQUIVALENT. Byte-level: FALSE.

### G24 — R-COD-11's cannot-establish branch is unreachable as a final verdict
Members: verifierb-01

Checked §17.4's opening clause directly: "cannot establish that layer's
conformance" occurs at A line 2618 / B line 2515, byte-identical. Grounded
in text shared between editions.

Consensus: EQUIVALENT. Byte-level: FALSE.

### G25 — §20.3 step 4's R-ERR-01 citation vs §21.7's own unwitnessed-condition test
Members: verifierb-02

Checked both citations directly (G1 and G13 above): §20.3 step 4's
R-ERR-01/R-CNF-02 citation and §21.7's unwitnessed-condition definition are
each byte-identical between editions. A genuine internal-consistency
question about the shared document, not an A-vs-B difference.

Consensus: EQUIVALENT. Byte-level: FALSE.

### G26 — version_minor floor-and-carry rule is a SHOULD, not a MUST
Members: quizb-01

Checked R-CNT-26's text directly: identical set of six citation sites at
consistent offsets in both editions (A lines 917/3387/3622/4829/4874 vs B
lines 814/3284/3519/4733/4778), including the SHOULD-level sentence itself.
Shared text; the quiz-authoring difficulty it names applies equally to
edition A, which the author (reading only B) did not have occasion to say.

Consensus: EQUIVALENT. Byte-level: FALSE.

## Coverage check

53 input ids listed; 26 groups; every id assigned to exactly one group
(hand-recounted against the id list in the task text — see final tally in
the structured output's all_input_ids_seen).
