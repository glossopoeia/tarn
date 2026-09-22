# Transcript — verifier comparator

## Disclosure

**Access.** I read exactly the four files the brief names:
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (4,981 lines)
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/b/tarn.md` (4,977 lines)
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/out/transcript-verifier-a.md`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/out/transcript-verifier-b.md`

I did not open docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md,
conformance/, spec/registry.json, git history, or the web, and I did not
list any directory other than creating my own scratch directory with
`mkdir -p` (no listing of its prior contents beyond that creation, which
also serves as an existence check).

**Method.** The two edition files are 295 KB / ~5,000 lines each, over the
per-call read limits, so instead of re-reading each end to end I:
1. Ran `wc -l` on both (a file-size check on named files, not a directory
   listing).
2. Ran `diff a/tarn.md b/tarn.md` — a computation over exactly the two
   named files — and got a *complete, exhaustive* list of every byte
   difference between the two editions: six hunks, all of them small
   (single lines or a few adjacent lines), totalling a 4-line difference
   in overall length (4,981 vs 4,977), which matches exactly (two hunks
   each remove one more line than they add). I saved this diff to my
   scratch directory (`full.diff`, `full.udiff`).
3. For every hunk, and for every passage either transcript cited for V1–V6
   or for its own findings, I read the surrounding context in *both*
   editions with the Read tool at matching offsets, to see the change (or
   confirm the identity) in situ rather than trust the diff's bare lines.
4. I cross-checked line-number arithmetic: each `diff` hunk shifts the
   line count of every subsequent line by a fixed, computable amount
   (−1, −1, 0, 0, −2, and then constant to EOF), and I verified this
   against independent `grep -n` line numbers for a dozen unrelated
   anchors (`R-CNF-11`, `R-COD-11`, `R-LIF-08`, `R-WRT-04`, F25/F35/F36/L46
   register rows, the R-CNT-17 index-size formula, the §20.3 step-4
   "binds the commit as an actor" sentence, §9.7's "reconstructing the
   file's history" sentence) landing at exactly the offsets the diff
   predicts, in both directions. This gives me confidence the six-hunk
   diff is the complete and only set of differences — not an artifact of
   `diff`'s own heuristics failing to align a larger rewritten region.
5. I did not rely on line-oriented `grep` alone for any *prose* fragment
   that could straddle a hard-wrap break; every quotation below was
   copied from a `Read` result showing the surrounding lines, not
   reconstructed from a grep match. Section headings (`#### N.N Title`)
   do not wrap and were grepped directly for navigation only.
6. Both transcripts were read in full via the Read tool (764 and 704
   lines respectively, each in one call).

**Control searches proving negatives.** Because `diff` gives a complete,
literal accounting, "zero differences in section X" is not an inference
from absence of a grep hit but a direct read of `diff`'s output: if a
passage does not appear as a hunk, it is byte-identical, full stop. As a
second, independent check I re-verified byte-identity at nine specific
anchors central to the probes (see item 4) by grepping each anchor in
*both* files and confirming (a) both files contain it and (b) the line
numbers differ by exactly the cumulative offset the six hunks predict at
that point in the file — a positive control that would have shown a
mismatch had the diff missed anything upstream of that anchor.

**Context that arrived unrequested.** My context contained, before I
began: a CLAUDE.md pointer to AGENTS.md; a user memory index of
editorialized note titles about a "TARN" project (harness spec paths,
lineage gates, repair defects, ADR audits, subagent models, refute-phase
triggers, and similar); a git-status block naming five recent commit
subjects (ADR-0133 accepted/proposed, ADR-0132's repair and audit,
inventory/equivalence tooling); a user-email field; and an
attribution/formatting instruction block. None of this is part of the
specification, none of it is evidence about either edition's content, and
I have not treated it as such or let it steer any judgment below. The
harness's outer "user request" framing ("Accept ADR-0133 and run the
calibration round") is likewise not evidence about the document; I note
its existence only because the brief requires disclosing unrequested
context, not because it informed any finding.

**Scratch directory.** `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/scratch/compare-verifier/`
was created fresh by me this session (`mkdir -p`) and holds: `full.diff`,
`full.udiff` (the complete diff, two formats), and this transcript before
its copy to the output path.

---

## Headline observation, stated up front

`diff` shows the two "editions" are **byte-identical except for six small,
localized edits** (a four-line net length difference across a ~295 KB,
~4,980-line document). This is not what "edition B, a rewrite meant to say
the same thing more readably" would predict — a genuine readability
rewrite would reorder, reword, and restructure prose throughout, and a
diff between such editions would be enormous. What the diff actually shows
is a document copied verbatim with a handful of injected point changes.
None of the six changed spots falls inside any passage either
verifier-implementer transcript cites for V1–V6 or for its own findings
(verified in the "Probes" and "Each walk's own findings" sections below).
Consequently:

- Every probe where the two transcripts' answers differ in wording, is a
  difference of **wording only** (the source text is identical), i.e.
  EQUIVALENT — not a text-driven divergence.
- Every finding a walker raised as an OBSERVATION about "its" edition
  applies with equal force to the other edition, because the passages it
  rests on are byte-identical.
- The substantive fidelity findings in this round come entirely from the
  six diff hunks themselves — real, small, textual differences the probes
  did not happen to touch, surfaced only by the "go past the probes"
  charter step (§5) and by running an exhaustive diff rather than sampling.

---

## The six hunks, examined in context

### Hunk 1 — §6.3 Flags, updater ignore-lane obligation (A:907–909 / B:906–908)

A: "A rewriter... carries the input's unknown ignore-lane bits into its
output trailer rather than writing flags = 0, and sets no other (§20.5,
`[R-WRT-06]`). An updater MUST copy forward unknown ignore-lane bits of
its input file, **MUST NOT clear them, and** MUST NOT set any other..."

B: "...An updater MUST copy forward unknown ignore-lane bits of its input
file, MUST NOT set any other..."

**Kind: EQUIVALENT.** "Copy forward X" already means X's value is
preserved into the output; "MUST NOT clear them" restates that
obligation's contrapositive rather than adding a new one. I looked for a
reading under which an updater could satisfy "copy forward" while also
clearing a bit (e.g., by writing 0 and calling that "forwarding" a bit
whose value happened to be 0) and found none that the surrounding
sentence supports — "copy forward" is used throughout this document as
"reproduce unchanged." No behavior a conforming implementation performs
differs between A and B here.
**Byte-level test:** No — the same obligation is enforceable from either
text; an implementation built from B alone still must not clear an
unknown ignore-lane bit, because "copy forward" already requires that.

### Hunk 2 — §20.3 step 2, appender's drop prohibition (A:3219–3220 / B:3218)

A: "Against any other structure the appender carries forward, it MUST NOT
repair the defect — `[R-LIF-01]` freezes the committed prefix — and MUST
NOT drop the record **save where §20.4 licenses the drop**."

B: "Against any other structure the appender carries forward, it MUST NOT
repair the defect — `[R-LIF-01]` freezes the committed prefix — and MUST
NOT drop the record."

Both editions' §20.4 (unchanged, byte-identical, confirmed by the same
diff run) states, for an MU=0/PE=0 record: "an appender MAY drop the
record in any commit it is otherwise free to make." A reconciles this
with step 2's blanket "MUST NOT drop" by explicit cross-reference
("save where §20.4 licenses the drop"). B states step 2's prohibition
with no such carve-out, leaving it in unremarked tension with §20.4's
explicit license two subsections later.

**Kind: LOSS.** This is a carve-out A states and B does not (the fidelity
test's own first bullet: "a rule, a carve-out, an exception... that A
states and B does not"). B is not simply silent where A is explicit in a
way that changes nothing — an implementer who takes step 2 at face value
in B, without independently noticing and resolving the conflict against
§20.4 three subsections later, could conclude that an appender may never
drop *any* record while carrying it forward, PE=0-licensed or not,
which contradicts §20.4's unqualified "MAY drop."
**Byte-level test:** Yes, for an appender/updater implementation (not the
verifier itself, which never writes): an implementation built from B's
step 2 read literally, and not independently cross-checked against §20.4,
would retain a PE=0 record some other implementation (reading either A,
or B's own §20.4) correctly drops — a different set of bytes in the
committed output. I flag this as tangential to the *verifier's* own
conformance obligations (a verifier only reads and reports; it is not
itself bound by step 2), but it is squarely inside "an implementation
built from the document," which is the test as stated, and it is the kind
of thing the walkers' own methodology (reading §20.3 end-to-end) would
have caught only if they had happened to also read the intervening §20.4
table with this specific tension in mind — neither transcript's V-probes
touch §20.3 step 2 or this specific clause at all.

### Hunk 3 — §20.3's worked example, index-region arithmetic (A:3400 / B:3398)

A: "> **Example.** Superseding one 100,000-byte stored tile of a 32-tile
interleaved layer appends: the new payload (100,000 bytes), the layer's
full new index region (32 · 20 + 4 = **644** bytes — one entry re-pointed,
31 byte-identical)..."

B: "...the layer's full new index region (32 · 20 + 4 = **664** bytes —
one entry re-pointed, 31 byte-identical)..."

The index-region-size formula is stated identically, and unchanged, in
both editions elsewhere (`[R-CNT-17]`, quoted at A:1160/B:1159 and again
at register row L22, A:3916/B:3912): "entry_count × 20 +
⌈entry_count/2¹⁶⌉ × 4." For entry_count = 32: 32 × 20 = 640, plus
⌈32/65536⌉ × 4 = 1 × 4 = 4, giving **644** — matching A's worked figure
and the formula both editions state. B's "664" is arithmetically wrong by
the formula B itself states unchanged three sections earlier, and is
inconsistent with the *other* worked instance of the very same formula
present, byte-identical, in both editions (A:1220/B:1219: "an extent slot
of length 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84 bytes").

**Kind: LOSS** (a worked figure A states correctly and B does not — the
fidelity test's own first bullet names "a worked figure... that A states
and B does not, or states more narrowly or more widely"; here B simply
misstates it against its own unchanged formula).
**Byte-level test:** Yes. An implementer or conformance-vector author who
built a test file from this example by trusting the stated total (as
opposed to re-deriving it from the formula) would produce a file 20 bytes
short of what B's own §7.4/`[R-CNT-17]` formula requires for that index
region — a file that a verifier built from either edition would then
reject (L22, extent_length ≠ formula) even though the example intends a
conforming result. This is exactly the sort of worked-figure error the
brief's charter step 5 asks a comparator to look for past the probes;
none of V1–V6 touches this specific example.

### Hunk 4 — §20.4, scope of the MU=1 preservation row (A:3497–3498 / B:3495–3496)

A: "The table states what an updater owes a record it does not logically
modify, read under whichever flags govern it. Its MU = 1 row reaches
**only a type the updater does not implement** — an updater implements
both registered types and understands an unregistered type it implements
from its definition, modifying their records as §20.3 and that
definition provide — so for an implemented type only the PE bit bites:"

B: "...Its MU = 1 row reaches **every type, implemented or not** — an
updater implements both registered types and understands an unregistered
type it implements from its definition, modifying their records as §20.3
and that definition provide — so for an implemented type only the PE bit
bites:"

**Kind: LOSS**, and worse, an internal defect unique to B. A's sentence
is a coherent argument: the MU=1 row (in the table that follows) governs
only *unimplemented* types, and *therefore* ("so") for an implemented
type only the PE bit determines the updater's obligation. B replaces the
premise with its opposite ("every type, implemented or not") while
leaving the "so... only the PE bit bites" conclusion intact — a
conclusion that no longer follows from, and directly contradicts, the
premise B now states. This is not a stylistic rewording; it inverts the
scope of a normative statement (which records the MU=1 row in the very
next table applies to) and, in doing so, makes edition B self-contradictory
in a way A is not.
**Byte-level test:** Yes, for an updater/appender/rewriter implementation
(again not the verifier itself): whether an updater treats an
*implemented*-type record with MU=1 as bound by the table's "MU=1: retain
byte-identical, MUST NOT modify the scope it governs" row, or as governed
only by the PE bit, changes which commits (which output byte sequences)
an updater built from B alone would refuse to produce versus one built
from A alone — B's stated premise, taken literally, would forbid
modifying/dropping *any* MU=1 record's governing scope regardless of
implementation status, which is stricter than A's rule and than B's own
following clause assumes.

### Hunk 5 — §20.4, the sentence naming which sub-record blocks a layer drop (A:3512–3514 / B:3510)

A: "A commit MAY therefore drop a layer record, and the drop takes the
layer whole: a sub-record's flags govern it within a layer the updater
keeps, so a dropped layer's sub-records and their extents go with it
whatever their PE bits. **One sub-record blocks the drop, a sub-record of
a type the updater does not implement with MU = 1, the drop being a
modification of the scope it governs (the table's first row).** A commit
never removes a user-metadata record from a scope it keeps..."

B: "...so a dropped layer's sub-records and their extents go with it
whatever their PE bits. A commit never removes a user-metadata record
from a scope it keeps..."

**Kind: LOSS.** A states, in one explicit sentence, exactly which
sub-record condition blocks an otherwise-permitted layer drop (an
unimplemented-type MU=1 sub-record, because dropping the layer would
modify the scope that sub-record's MU=1 row governs). B omits this
sentence entirely — not rephrased, simply absent — leaving no statement
anywhere in the paragraph of what, if anything, can block a layer drop
that would otherwise strand its sub-records. Read together with Hunk 4
(which also erased the "only... does not implement" qualifier the omitted
sentence depends on), edition B has lost both the general rule and its
specific consequence for layer-drop blocking, in the same local edit.
**Byte-level test:** Yes, for an updater implementation: whether a commit
that would drop a layer containing an unimplemented-type MU=1 sub-record
is itself a violation (blocked) or permitted is a rule A states and B
does not state at all — an implementer of an updater/appender built from
B alone has no textual basis for refusing such a drop, where one built
from A does.

### Hunk 6 — §21.2 register, F19's "Instances" cell (A:3863 / B:3859)

A: "| F19 | Any bit of the flags incompat lane (bits 0-15) is set... |
**flags bits 0-15** | reader | open | `[R-CNT-08]` |"

B: "| F19 | Any bit of the flags incompat lane (bits 0-15) is set... |
**flags bits 0-7** | reader | open | `[R-CNT-08]` |"

The row's own Condition cell — unchanged, identical in both editions —
says "bits 0-15" in the same row. B's Instances cell ("bits 0-7") directly
contradicts B's own Condition cell in the same table row. The operative,
normative statement of the incompat lane's width ("bits 0–15") appears
verbatim, unchanged, in the running §6.3 prose in both editions (A:899,
B:898, confirmed identical above) and again inside F19's own Condition
text — so the actual reader/verifier check ("reject on any set bit in
0–15") is stated correctly and identically in both editions; only the
register's bookkeeping "Instances" cell for F19 is wrong in B.

**Kind: LOSS** (of a correct, self-consistent register in B), but with a
narrower byte-level footprint than Hunks 3–5: the check a conforming
reader/verifier actually implements is driven by the Condition cell and
the running §6.3 text, both unchanged, so no reader or verifier built
correctly from B's normative prose would fail to reject a file with, say,
bit 10 set. Where it matters is exactly the register's own
completeness/bookkeeping purpose — the same purpose walker A's
verifiera-02 finding (below) flags for the open-ended subsumption list:
a conformance-vector author enumerating F19's instances bit-by-bit
(`[R-VEC-02]`/`[R-VEC-03]`) from B's table alone, rather than from the
Condition prose, would only construct test vectors for bits 0–7 and miss
bits 8–15 as a distinct instance of F19 — a real gap in test coverage,
though not a divergence in what a verifier reading B's *prose* would
accept or reject.
**Byte-level test:** Marginal/No for the verifier's own accept-reject
behavior (the operative rule is unchanged); **yes** for the completeness
of a test-vector corpus built by mechanically enumerating the Instances
column rather than re-deriving it from the Condition text.

---

## The probes (V1–V6): every citation checked in both editions

For each probe I located, in both editions, every passage either
transcript cited (section number, requirement ID, or quoted sentence) and
confirmed byte-identity via the exhaustive diff plus a direct read at the
matching offset. None of the six hunks above falls inside any of these
citations. Results:

- **V1** — both cite §2.3/`[R-CNF-11]` and §19.2's "unexamined" note.
  §2.3 read in full in both editions above: byte-identical (A:152–271,
  B:152–271, no diff hunk in range). Both answers restate the same three
  verdicts and the same priority rule in different words.
  **Kind: EQUIVALENT** — wording difference only, source identical.
- **V2** — both cite §10.2's range partition, F35/F36, §21.6, `[R-CNF-11]`,
  `[R-CNT-15]`. F35/F36 register rows confirmed byte-identical (A:3879–3880
  / B:3875–3876, both "F35...reader...open", "F36...verifier...
  certification" — matching both transcripts' attributions exactly, so
  neither transcript mis-assigned a detector here). §21.6's closing
  paragraph and §10.2 fall outside any hunk.
  **Kind: EQUIVALENT.**
- **V3** — both derive the same three-generation arithmetic (F₃ = 14,528;
  live = 12,816; slack = 1,712) from `[R-LIF-02]` step 5, `[R-WRT-04]`,
  `[R-CNT-17]`'s formula, and `[R-CNT-21]`. All of §9.2/§20.3/§5.1/§5.2's
  cited passages, and the R-CNT-17 formula itself, are byte-identical
  (confirmed above); neither of the changed worked examples (Hunk 3's
  644/664 figure, a *different* scenario — 32-tile layer, 100,000-byte
  tile — from the V3 probe's own 4-tile/1,024-byte-tile scenario) is what
  either transcript actually computed from. Both transcripts' own
  arithmetic is internally correct and matches the (identical) formula in
  both editions.
  **Kind: EQUIVALENT.**
- **V4** — both cite §17.4/`[R-COD-11]` in full; confirmed byte-identical
  above (A:2614–2631, B:2613–2630). Both walks reach the same layered
  answer (cannot-establish in general; nonconforming via L43/L45 once the
  codec/filter value is itself reserved/experimental) from the same text.
  **Kind: EQUIVALENT.**
- **V5** — both cite §20.3 step 4's fixed-declaration bar and §9.7's
  no-history-reconstruction note; both confirmed byte-identical above
  (A:3260–3289/B:3258–3287 for the bar itself, plus A:1554/B:1553 area for
  `[R-LIF-08]`, A:1559/B:1558 for the "reconstructing the file's history"
  sentence). Both walks give the identical case analysis (T3/T4/T5/T2/
  T17/T24/T25 as the only incidental symptoms).
  **Kind: EQUIVALENT.**
- **V6** — both cite `[R-CNT-12]`, F25, L46; F25/L46 confirmed
  byte-identical above (A:3869/B:3865 and A:3940/B:3936). Both walks agree
  on the file-scope/layer-scope split and its rationale.
  **Kind: EQUIVALENT.**

No probe shows a REPORTER_ERROR, AMBIGUITY, LOSS, or ADDITION driven by
the document text: every citation checked is byte-identical, and both
transcripts' readings of those identical passages agree with each other
and with the text.

## Each walk's own findings, checked against the other edition

- **verifiera-01** (the `[R-CNF-11]`/§21.6 "conforming file vs. verifier
  can never certify conforming" tension) rests entirely on §2.3 and
  §21.6, both confirmed byte-identical. The identical tension exists,
  verbatim, in edition B. **Not a defect unique to A** — reclassified:
  **EQUIVALENT** (a valid document-level observation, but one edition B
  shares in full, not a LOSS or ADDITION of B's).
- **verifiera-02** (§21.1's subsumption-pair list declared open, "not
  offered as closed") rests on §21.1, confirmed byte-identical
  (`§21.1` heading at A:3735/B:3731, both past only Hunks 1–2's small
  offset, content unaffected). Applies equally to B.
  **Kind: EQUIVALENT.**
- **verifierb-01** (`[R-COD-11]`'s codec-execution decline is absent from
  §5.2/§9.7's own list of what makes the coverage walk's total "partial")
  rests on §5.2, §9.7, and §17.4, all confirmed byte-identical. The same
  gap (if it is one — walker B itself calls its own conclusion an
  inference, not a stated rule) exists, verbatim, in edition A.
  **Kind: EQUIVALENT.**
- **verifierb-02** (a commit that silently violates the fixed-declaration
  bar is undetectable except by accident) rests on §20.3 step 4, §9.3's
  third note, §9.7's note, and §21.7 — all confirmed byte-identical
  (the §20.3 step-4 paragraph is quoted and compared in full above).
  Applies equally to A. **Kind: EQUIVALENT.**

## Guesses, re-reads, and asymmetric difficulty (charter item 4)

Both transcripts read their file end-to-end in full before answering any
probe, both flagged V2 and V5 as "underdetermined by the probe's own
wording" (not by the document) for the identical reason (the probe omits
a fact the document conditions its answer on), and both used one or two
confirmatory `grep`s over short fragments rather than relying on them as
primary evidence, citing the same hard-wrap caution. Neither transcript
reports having to search elsewhere in the document for a fact the other
walker found immediately, or vice versa — consistent with the two texts
being identical at every point either walker actually needed. I found no
asymmetry to report here.

## Sections read past the probes (charter item 5)

Beyond the probe citations, I read, in both editions: all of §20.3 (the
append procedure, steps 1–6, in full) and §20.4 (re-emission and
preservation, in full) end to end, since these are the sections the two
edits at Hunks 2, 4 and 5 sit inside, to make sure I had each edit's
complete governing paragraph rather than an isolated line; the full
register excerpt spanning F1–F36 (§21.2) to place Hunk 6 in its row and
confirm neighboring rows are unaffected; and both instances of the
`[R-CNT-17]` index-size formula and its two worked applications (the
84-byte and would-be-644-byte examples) to establish Hunk 3 is a genuine
arithmetic error rather than a difference in stated assumptions. I did
not find any further undiffed-but-substantive divergence in these
readings beyond the six hunks `diff` already identified — which is
expected, since `diff` is exhaustive over the two files as given.
