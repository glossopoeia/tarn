# Refute-only attack on the A-03 downgrade — lens: unswept restatement

## What I read / ran
Read: case/case-A-03.md; hunk-03.diff, hunk-09.diff, hunk-11.diff; spec/tarn.md
(2.1-2.4, 4.2, 11.1-11.3, 14.2 near [R-SER-02], 19 preamble, 19.2, 19.3, 19.4
steps 1-2, 21.1, 21.3 rows L1-L8, 21.6, 21.9). Built a whitespace-flattened copy
(tr '\n' ' ' | tr -s ' ') in scratchpad and grepped that; the source is hard-wrapped.
Not read: docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/,
registry.json, git history, full.diff, other hunks, the case dir listing, the web.

Unsolicited context: a project-instruction file and a memory index appeared before
I began, plus a git status/recent-commit block whose subject lines touch this
finding's subject matter. I opened none of them and reasoned from none.

## Greps run
1. '.{160}R-ENC-04.{200}' -> 13 hits. Surviving wide-form sites: 19.3 and row L2 only.
   17.2 Note / 20.3 step 4 / 22.2 now read "designates".
2. '.{200}the rule governs.{300}' -> 3 hits: 21.1 tiebreak; express extension to
   21.6 entries; 21.7 F-row note.
3. '.{120}intermediate.{200}' -> 2 hits, one is 11.2's Note (blockquote, non-normative).
4. 'evaluation order' -> ZERO hits. 'associat' -> ZERO hits. 'in any order' -> 3 hits,
   all about byte placement, none about arithmetic.
5. '.{300}forms no product.{200}' -> 1 hit, 11.3.
6. Per-requirement pulls: R-CNF-01/03/04/05/06/07/12, R-ERR-03/04, R-GEO-02/03, R-SER-02.
7. '.{150}MUST accept.{250}' -> 4 hits; two decide this case (R-GEO-02, R-ERR-03).

## Where the refutation is WRONG
Its pillar (point 1) fails. 21.1's tiebreak is scoped to register ROWS: "each row
restates its governing rule, and where a row and the rule it cites diverge, the rule
governs." The document extends that tiebreak past rows only by writing a sentence to
do it: "21.6's entries restate their governing rules on the same terms a row does,
and where such an entry and the rule it cites diverge, the rule governs there too."
No such sentence exists for 19's enumerations. If the tiebreak travelled by
implication (from 19's use of the word "restate"), the 21.6 extension sentence would
be surplus. So the auditor was right that 21.1 does not reach [R-RDR-03].
Also: 19's preamble says "It introduces no new STRUCTURES" — structures are file
structures here, not checks.

## Why the downgrade nevertheless stands
(a) The fork is structurally confined to zero-extent layers, and that class carries
an express MUST-accept. I enumerated every sum/product [R-ENC-04]/L2 reaches:
 - sums (extent_offset+extent_length, Q=SUM Bj, Fc, entry_count*20+ceil(...)*4): all
   terms non-negative, partials <= total. No fork.
 - P = PROD Ti: [R-GEO-01] bars Ti=0, factors >=1, partials non-decreasing. No fork.
 - P*Q, P*Bc: [R-SER-02] fixes Bc>=1 ("1 for bool"), so Q>=1, P>=1. No fork.
 - C*N, N*P, (C-1)*N+(N-1): C>=1 ([R-GEO-01] bars channel count 0); a zero factor can
   enter only through N.
 - N = PROD Gi with Gi = ceil(Ei/Ti): since Ti>=1, Gi=0 IFF Ei=0.
   => a partial product can exceed 2^63-1 while the designated product does not ONLY
   when some dimension has extent 0. Every instance of this fork is a zero-extent
   layer, not just the reporter's.
 [R-GEO-02]: "A dimension with extent 0 is valid: its grid count is 0, the layer has
 zero addressed tiles, its tile index has zero entries, and its reference array is
 empty. Readers MUST accept such a layer..."
 21.6 headnote, over the row "A dimension has extent 0 | A valid, empty layer ... |
 [R-GEO-02]": "These are defined behaviors, not errors. A reader that treats any of
 them as a failure is the nonconforming party."
 Implementation B rejects a layer whose only ground of complaint exists BECAUSE a
 dimension has extent 0 (remove the zero and N itself overflows, and both readings
 reject). B is the nonconforming party by 21.6's own headnote.

(b) 19's preamble caps 19 without needing 21.1: "Those enumerations are not the
complete inventory of what a reader detects at that tier: 21's register is..."
21.1: "Its completeness is normative — a detectable file-conformance violation this
specification names and the register omits is a defect in this document." L2's
Instances cell contains no intermediate. This cap does not depend on 19.3 being a
restatement of a row, so it survives the collapse of point 1.

(c) Even a size-balking reader is routed away from a validity error. [R-ERR-03]: "a
conforming reader MUST accept any conforming file whose quantities lie within these
bounds" — the construction is inside every row (rank 3<=32, C=1<=4096, entry_count
0<=2^32; 21.9 says expressly "A layer addressing no tile (11.2) therefore has no tile
whose decoded size the table bounds"), and 21.9 has no row for a dimension extent.
[R-ERR-04]: "A file exceeding any of these remains conforming, and a reader MAY
decline it ... a refusal on resource grounds MUST be reported as a resource limit and
not as a validity error." So the file stays conforming, [R-CNF-05] never bars a
writer, and the emittable set does not move.

(d) Reading B is not determinate. The spec writes N = PROD Gi and (grep 4) says
nothing about evaluation order or associativity. Under B the verdict depends on which
two factors an implementation multiplies first — two implementations both "following
B" reach opposite verdicts on the same bytes. [R-ENC-04] tests the "mathematical
value", which for PROD Gi is 0, and "A designation is express, made by the section
that defines the quantity" — 11.2 designates four products and names no partial.

On the anaphora argument (refutation point 3): right but weaker than claimed. "that
arithmetic" does point back to "the geometry floor and its arithmetic
([R-GEO-01]-[R-GEO-03])", and "the decoded sizes 14 derives from it" is ungrammatical
without that antecedent. But the phrase remains a PROCESS description ("every quantity
that arithmetic derives") where the repaired rule is a DESIGNATION description. The
anaphora narrows the fork to geometry; it does not close it. (a)-(d) close it.

Actors enumerated: reader / updater / verifier — [R-ENC-04] folds updaters and
verifiers into "reader" expressly, same disposal. Writer — reaches the file only via
[R-CNF-05], and the file is conforming under both readings once (a)-(d) bind.
Appender via 20.3 step 4 — swept in hunk 9, takes the narrow form directly.

## Answers
1. Real as text? Partly, editorially. [R-RDR-03] is the last surviving site, and the
   only numbered requirement among them, that characterises [R-ENC-04] in the words
   the repair removed, and the refutation's disposal route (21.1) is unavailable. It
   should be swept. But it is not a second normative statement: 19's own preamble and
   21.1's normative-completeness clause put what a reader detects in the register, and
   the register (via [R-ENC-04], which governs L2) does not reach intermediates.
2. Byte-level? No. Every file in the fork class is a zero-extent layer, which
   [R-GEO-02] makes MUST-accept and 21.6 makes a defined non-violation whose rejector
   "is the nonconforming party". Emittable set and accept/reject verdict identical.

Verdict: DOWNGRADE_STANDS — with the correction that the refutation's central
argument (point 1) is unsound; the downgrade survives on other text.
